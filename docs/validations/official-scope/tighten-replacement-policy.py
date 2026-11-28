from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
p=ROOT/"scripts/validate_recipes.py";s=p.read_text(encoding="utf-8")
old='''    blocked_recipes: set[tuple[str, str]] = set()
    policy_path = repo_root / "docs" / "official-install-policy.json"
    if index_data.get("execution_policy") == "official_upstream_only":
        try:
            policy = json.loads(policy_path.read_text(encoding="utf-8"))
            blocked_recipes = {(r["project_id"], r["tag"]) for r in policy["blocked_recipes"]}
        except (OSError, ValueError, KeyError, TypeError) as exc:
            errors.append(f"Missing/invalid official installation policy: {exc}")
'''
new='''    blocked_recipes: set[tuple[str, str]] = set()
    approved_replacements: dict[tuple[str, str], dict] = {}
    retired_files: list[Path] = []
    policy_path = repo_root / "docs" / "official-install-policy.json"
    if index_data.get("execution_policy") == "official_upstream_only":
        try:
            policy = json.loads(policy_path.read_text(encoding="utf-8"))
            blocked_recipes = {(r["project_id"], r["tag"]) for r in policy["blocked_recipes"]}
            for replacement in policy.get("approved_recipe_replacements", []):
                required = ("project_id", "tag", "path", "sha256", "build_profile",
                            "retired_path", "retired_sha256", "retired_build_profile",
                            "upstream_commit", "audit_reference")
                if not isinstance(replacement, dict) or any(
                        not isinstance(replacement.get(field), str) or not replacement[field]
                        for field in required):
                    raise ValueError("Incomplete approved recipe replacement")
                key = (replacement["project_id"], replacement["tag"])
                if key not in blocked_recipes or key in approved_replacements:
                    raise ValueError(f"Replacement must bind one unique retired identity: {key}")
                if (not RE_SHA256.fullmatch(replacement["sha256"])
                        or not RE_SHA256.fullmatch(replacement["retired_sha256"])
                        or re.fullmatch(r"[0-9a-f]{40}", replacement["upstream_commit"]) is None):
                    raise ValueError(f"Invalid immutable replacement revision: {key}")
                expected_retired = "docs/retired-recipes/" + replacement["path"].removeprefix("recipes/")
                if (not replacement["path"].startswith("recipes/")
                        or not RE_INDEX_PATH.fullmatch(replacement["path"])
                        or replacement["retired_path"] != expected_retired
                        or not (repo_root / expected_retired).resolve().is_relative_to(repo_root.resolve())):
                    raise ValueError(f"Unsafe or unbound retired recipe path: {key}")
                if not any((r["project_id"], r["tag"], r["path"]) ==
                           (*key, replacement["path"]) for r in policy["blocked_recipes"]):
                    raise ValueError(f"Replacement path differs from retired identity: {key}")
                archived = repo_root / expected_retired
                retired_raw, retired_errors = read_utf8_bytes(archived, strict_lf=strict_lf)
                errors.extend(retired_errors)
                retired = json.loads(retired_raw.decode("utf-8"))
                if (hashlib.sha256(retired_raw).hexdigest() != replacement["retired_sha256"]
                        or retired.get("project_id") != key[0]
                        or retired.get("tag") != key[1]
                        or retired.get("build_profile") != replacement["retired_build_profile"]
                        or replacement["sha256"] == replacement["retired_sha256"]
                        or replacement["build_profile"] == replacement["retired_build_profile"]):
                    raise ValueError(f"Retired bytes/profile were not preserved separately: {key}")
                retired_files.append(archived)
                approved_replacements[key] = replacement
        except (OSError, ValueError, KeyError, TypeError) as exc:
            errors.append(f"Missing/invalid official installation policy: {exc}")
'''
assert old in s;s=s.replace(old,new,1)
s=s.replace('checked_files: list[Path] = [index_path]','checked_files: list[Path] = [index_path, *retired_files]',1)
old='''        if (project_id, tag) in blocked_recipes and status != "disabled":
            errors.append(f"{loc}: source-integrity policy requires this recipe to remain disabled")
'''
assert old in s;s=s.replace(old,"",1)
marker='''        if sv in VALID_SCHEMA_VERSIONS:
            errors.extend(
'''
assert marker in s
s=s.replace(marker,'''        if (project_id, tag) in blocked_recipes and status != "disabled":
            replacement = approved_replacements.get((project_id, tag))
            if (replacement is None
                    or replacement["path"] != rel_path
                    or replacement["sha256"] != actual_sha
                    or replacement["build_profile"] != recipe_doc.get("build_profile")):
                errors.append(
                    f"{loc}: source-integrity policy requires this recipe to remain disabled; "
                    "only the exact reviewed replacement hash and profile may run"
                )

'''+marker,1)
p.write_text(s,encoding="utf-8",newline="\n")
p=ROOT/"tests/test_validate_recipes.py";s=p.read_text(encoding="utf-8")
marker='''        # Normalize copied files in temp repo to LF for strict_lf tests'''
s=s.replace(marker,'''        shutil.copytree(REPO_ROOT / "docs" / "retired-recipes", tmp / "docs" / "retired-recipes")
'''+marker,1)
marker='''    def test_disabled_history_still_requires_provenance_and_valid_hash(self) -> None:'''
tests='''    def test_reviewed_replacements_bind_exact_bytes_and_profile(self) -> None:
        tmp = self._make_temp_repo()
        policy = json.loads((tmp / "docs/official-install-policy.json").read_text(encoding="utf-8"))
        self.assertTrue(policy["approved_recipe_replacements"])
        index_path = tmp / "index.json"
        index = json.loads(index_path.read_text(encoding="utf-8"))
        replacement = policy["approved_recipe_replacements"][0]
        entry = next(e for e in index["recipes"] if
                     (e["project_id"], e["tag"]) ==
                     (replacement["project_id"], replacement["tag"]))
        # Even updating the index hash cannot make retired bytes executable.
        old = (tmp / replacement["retired_path"]).read_bytes()
        (tmp / entry["path"]).write_bytes(old)
        entry["sha256"] = hashlib.sha256(old).hexdigest()
        index_path.write_text(json.dumps(index), encoding="utf-8")
        ok, errors, _ = validate_recipes.validate_repository(tmp)
        self.assertFalse(ok)
        self.assertTrue(any("source-integrity policy" in e for e in errors), errors)

    def test_replacement_requires_preserved_retired_bytes(self) -> None:
        tmp = self._make_temp_repo()
        policy = json.loads((tmp / "docs/official-install-policy.json").read_text(encoding="utf-8"))
        archived = tmp / policy["approved_recipe_replacements"][0]["retired_path"]
        archived.write_bytes(archived.read_bytes() + b" ")
        ok, errors, _ = validate_recipes.validate_repository(tmp)
        self.assertFalse(ok)
        self.assertTrue(any("Retired bytes/profile" in e for e in errors), errors)

    def test_replacement_hash_does_not_allow_another_profile(self) -> None:
        tmp = self._make_temp_repo()
        policy_path = tmp / "docs/official-install-policy.json"
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
        policy["approved_recipe_replacements"][0]["build_profile"] = "other-official-profile"
        policy_path.write_text(json.dumps(policy), encoding="utf-8")
        ok, errors, _ = validate_recipes.validate_repository(tmp)
        self.assertFalse(ok)
        self.assertTrue(any("source-integrity policy" in e for e in errors), errors)

'''
assert marker in s;s=s.replace(marker,tests+marker,1);p.write_text(s,encoding="utf-8",newline="\n")
print("Exact replacement policy and regression tests updated")
