"""Unit tests for scripts/validate_recipes.py."""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import validate_recipes  # noqa: E402


class ValidateRecipesTests(unittest.TestCase):
    def test_real_repository_passes(self) -> None:
        ok, errors, stats = validate_recipes.validate_repository(
            REPO_ROOT,
            strict_lf=False,
            check_git_blobs=True,
        )
        self.assertTrue(ok, f"Expected real repo to pass, got errors: {errors}")
        self.assertGreaterEqual(stats["recipe_count"], 24)
        self.assertEqual(stats["statuses"].get("validated"), 1)
        self.assertEqual(
            stats["statuses"].get("experimental"),
            stats["recipe_count"] - 1 - stats["statuses"].get("disabled", 0),
        )

    def _make_temp_repo(self) -> Path:
        tmp = Path(tempfile.mkdtemp(prefix="getall_val_test_"))
        self.addCleanup(lambda: shutil.rmtree(tmp, ignore_errors=True))
        shutil.copytree(REPO_ROOT / "schemas", tmp / "schemas")
        shutil.copytree(REPO_ROOT / "addons", tmp / "addons")
        shutil.copytree(REPO_ROOT / "recipes", tmp / "recipes")
        shutil.copy2(REPO_ROOT / "index.json", tmp / "index.json")
        (tmp / "docs").mkdir()
        shutil.copy2(REPO_ROOT / "docs" / "official-install-policy.json", tmp / "docs" / "official-install-policy.json")
        shutil.copytree(REPO_ROOT / "docs" / "retired-recipes", tmp / "docs" / "retired-recipes")
        # Normalize copied files in temp repo to LF for strict_lf tests
        for jf in tmp.rglob("*.json"):
            jf.write_bytes(jf.read_bytes().replace(b"\r\n", b"\n"))
        return tmp

    def test_rejects_sha256_mismatch(self) -> None:
        tmp = self._make_temp_repo()
        idx_path = tmp / "index.json"
        idx = json.loads(idx_path.read_text(encoding="utf-8"))
        idx["recipes"][0]["sha256"] = "0" * 64
        idx_path.write_bytes((json.dumps(idx, indent=2) + "\n").encode("utf-8"))

        ok, errors, _ = validate_recipes.validate_repository(tmp, strict_lf=True)
        self.assertFalse(ok)
        self.assertTrue(any("SHA-256 mismatch" in e for e in errors), errors)

    def test_retired_contract_cannot_be_reactivated_by_removing_its_reason(self) -> None:
        tmp=self._make_temp_repo()
        index_path=tmp/"index.json"
        index=json.loads(index_path.read_text(encoding="utf-8"))
        entry=next(e for e in index["recipes"] if e["project_id"]=="sm64plus" and e["tag"]=="build-85c3e51")
        entry["status"]="experimental"
        for key in ("disabled_reason","disabled_at","audit_reference"):
            entry.pop(key,None)
        index_path.write_text(json.dumps(index),encoding="utf-8")
        ok,errors,_=validate_recipes.validate_repository(tmp)
        self.assertFalse(ok)
        self.assertTrue(any("source-integrity policy" in e for e in errors),errors)

    def test_reviewed_replacements_bind_exact_bytes_and_profile(self) -> None:
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

    def test_disabled_history_still_requires_provenance_and_valid_hash(self) -> None:
        tmp=self._make_temp_repo()
        index_path=tmp/"index.json"
        index=json.loads(index_path.read_text(encoding="utf-8"))
        entry=next(e for e in index["recipes"] if e["status"]=="disabled")
        entry.pop("disabled_reason")
        entry["sha256"]="0"*64
        index_path.write_text(json.dumps(index),encoding="utf-8")
        ok,errors,_=validate_recipes.validate_repository(tmp)
        self.assertFalse(ok)
        self.assertTrue(any("disabled_reason" in e for e in errors),errors)
        self.assertTrue(any("SHA-256 mismatch" in e for e in errors),errors)

    def test_rejects_unsafe_paths_spaces_and_reserved_names(self) -> None:
        self.assertFalse(validate_recipes.is_safe_relative_path("../evil.exe")[0])
        self.assertFalse(validate_recipes.is_safe_relative_path("Phase Distorter.exe")[0])
        self.assertFalse(validate_recipes.is_safe_relative_path("dir/CON.txt")[0])
        self.assertFalse(validate_recipes.is_safe_relative_path("dir\\file.exe")[0])
        self.assertTrue(
            validate_recipes.is_safe_relative_path(
                "goldeneye-pc-port-0.5.0-win64/libstdc++-6.dll"
            )[0]
        )

    def test_rejects_orphan_recipe_file(self) -> None:
        tmp = self._make_temp_repo()
        orphan = tmp / "recipes" / "super-mario-64" / "sm64coopdx" / "orphan.json"
        orphan.write_bytes(b"{}\n")

        ok, errors, _ = validate_recipes.validate_repository(tmp, strict_lf=True)
        self.assertFalse(ok)
        self.assertTrue(any("Orphan recipe file" in e for e in errors), errors)

    def test_rejects_launch_file_missing_from_required_files(self) -> None:
        tmp = self._make_temp_repo()
        rec_rel = "recipes/super-mario-64/ghostship/3.0.0.json"
        rec_path = tmp / rec_rel
        rec = json.loads(rec_path.read_text(encoding="utf-8"))
        rec["launch_file"] = "missing.exe"
        new_bytes = (json.dumps(rec, indent=2) + "\n").encode("utf-8")
        rec_path.write_bytes(new_bytes)

        idx_path = tmp / "index.json"
        idx = json.loads(idx_path.read_text(encoding="utf-8"))
        for item in idx["recipes"]:
            if item["path"] == rec_rel:
                item["sha256"] = hashlib.sha256(new_bytes).hexdigest()
        idx_path.write_bytes((json.dumps(idx, indent=2) + "\n").encode("utf-8"))

        ok, errors, _ = validate_recipes.validate_repository(tmp, strict_lf=True)
        self.assertFalse(ok)
        self.assertTrue(
            any("launch_file 'missing.exe' must be present in required_files" in e for e in errors),
            errors,
        )

    def test_accepts_valid_v4_recipe_and_rejects_v4_without_manual_steps(self) -> None:
        tmp = self._make_temp_repo()
        rec_rel = "recipes/super-mario-64/v4-sample/1.0.0.json"
        rec_path = tmp / rec_rel
        rec_path.parent.mkdir(parents=True, exist_ok=True)
        v4_doc = {
            "schema_version": 4,
            "project_id": "v4-sample",
            "tag": "1.0.0",
            "source_url": "https://github.com/example/v4-sample/releases/tag/1.0.0",
            "operations": [
                {
                    "kind": "import_input_set",
                    "scope": "installation",
                    "source": "orig-files",
                    "target": "data",
                }
            ],
            "required_files": ["game.exe"],
            "inputs": [
                {
                    "id": "orig-files",
                    "kind": "directory",
                    "name": "Original Data",
                    "required": True,
                    "files": [
                        {
                            "path": "track01.bin",
                            "size": 1024,
                            "sha256": "a" * 64,
                        }
                    ],
                }
            ],
            "manual_steps": "Run game.exe once to prepare data.",
            "launch_file": "game.exe",
            "first_run_files": [
                {
                    "path": "data/prepared.dat",
                    "size": 512,
                    "sha256": "b" * 64,
                }
            ],
        }
        rec_bytes = (json.dumps(v4_doc, indent=2) + "\n").encode("utf-8")
        rec_path.write_bytes(rec_bytes)

        idx_path = tmp / "index.json"
        idx = json.loads(idx_path.read_text(encoding="utf-8"))
        idx["recipes"].append(
            {
                "game_id": "super-mario-64",
                "project_id": "v4-sample",
                "repository": "example/v4-sample",
                "tag": "1.0.0",
                "schema_version": 4,
                "path": rec_rel,
                "sha256": hashlib.sha256(rec_bytes).hexdigest(),
                "status": "experimental",
                "has_inputs": True,
                "has_manual_steps": True,
            }
        )
        idx_path.write_bytes((json.dumps(idx, indent=2) + "\n").encode("utf-8"))

        ok, errors, _ = validate_recipes.validate_repository(tmp, strict_lf=True)
        self.assertTrue(ok, f"Expected valid v4 recipe to pass, got: {errors}")

        # Now remove manual_steps and verify failure
        del v4_doc["manual_steps"]
        rec_bytes = (json.dumps(v4_doc, indent=2) + "\n").encode("utf-8")
        rec_path.write_bytes(rec_bytes)
        idx["recipes"][-1]["sha256"] = hashlib.sha256(rec_bytes).hexdigest()
        idx["recipes"][-1]["has_manual_steps"] = False
        idx_path.write_bytes((json.dumps(idx, indent=2) + "\n").encode("utf-8"))

        ok2, errors2, _ = validate_recipes.validate_repository(tmp, strict_lf=True)
        self.assertFalse(ok2)
        self.assertTrue(
            any("first_run_files" in e and "manual_steps" in e for e in errors2),
            errors2,
        )

    def test_rejects_import_input_without_sha1_or_sha256(self) -> None:
        tmp = self._make_temp_repo()
        rec_rel = "recipes/super-mario-64/v3-no-hash/1.0.0.json"
        rec_path = tmp / rec_rel
        rec_path.parent.mkdir(parents=True, exist_ok=True)
        v3_doc = {
            "schema_version": 3,
            "project_id": "v3-no-hash",
            "tag": "1.0.0",
            "source_url": "https://github.com/example/v3-no-hash/releases/tag/1.0.0",
            "operations": [
                {
                    "kind": "import_input",
                    "scope": "installation",
                    "source": "orig-rom",
                    "target": "rom.z64",
                }
            ],
            "required_files": ["game.exe"],
            "inputs": [
                {
                    "id": "orig-rom",
                    "kind": "file",
                    "name": "Original ROM",
                    "required": True,
                    "size": 8388608,
                    "magic_hex": "80371240",
                }
            ],
            "launch_file": "game.exe",
        }
        rec_bytes = (json.dumps(v3_doc, indent=2) + "\n").encode("utf-8")
        rec_path.write_bytes(rec_bytes)

        idx_path = tmp / "index.json"
        idx = json.loads(idx_path.read_text(encoding="utf-8"))
        idx["recipes"].append(
            {
                "game_id": "super-mario-64",
                "project_id": "v3-no-hash",
                "repository": "example/v3-no-hash",
                "tag": "1.0.0",
                "schema_version": 3,
                "path": rec_rel,
                "sha256": hashlib.sha256(rec_bytes).hexdigest(),
                "status": "experimental",
                "has_inputs": True,
                "has_manual_steps": False,
            }
        )
        idx_path.write_bytes((json.dumps(idx, indent=2) + "\n").encode("utf-8"))

        ok, errors, _ = validate_recipes.validate_repository(tmp, strict_lf=True)
        self.assertFalse(ok)
        self.assertTrue(
            any("requires sha256 or sha1" in e and "import_input" in e for e in errors),
            errors,
        )

    def test_accepts_valid_v5_recipe_features(self) -> None:
        tmp = self._make_temp_repo()
        rec_rel = "recipes/extreme-g/v5-sample/v1.0.0.json"
        rec_path = tmp / rec_rel
        rec_path.parent.mkdir(parents=True, exist_ok=True)
        v5_doc = {
            "schema_version": 5,
            "project_id": "v5-sample",
            "tag": "v1.0.0",
            "source_url": "https://gitlab.com/example/group/v5-sample/-/releases/v1.0.0",
            "operations": [
                {
                    "kind": "import_input",
                    "scope": "local_app_data",
                    "profile_folders": ["Port (v5) Profile"],
                    "source": "orig-rom",
                    "target": "Original (USA).z64",
                },
                {
                    "kind": "import_input",
                    "scope": "installation",
                    "source": "orig-disc",
                    "target": "game/disc.bin",
                },
                {
                    "kind": "import_input_set",
                    "scope": "installation",
                    "source": "track-set",
                    "target": "Disc Files",
                },
            ],
            "required_files": [
                "Binarios (x64)/Port de Exemplo.exe",
                "Disc Files/Disc (Track 1).bin",
            ],
            "inputs": [
                {
                    "id": "orig-rom",
                    "kind": "file",
                    "name": "Original ROM",
                    "sha1": "a" * 40,
                },
                {
                    "id": "orig-disc",
                    "kind": "file",
                    "name": "Original Disc BIN",
                    "magic_hex": "00FFFFFFFFFFFFFFFFFFFF00",
                    "min_size": 1048576,
                    "max_size": 734003200,
                    "extensions": [".bin"],
                },
                {
                    "id": "track-set",
                    "kind": "directory",
                    "name": "Track Set",
                    "files": [
                        {
                            "path": "Disc (Track 1).bin",
                            "min_size": 4,
                            "max_size": 65536,
                            "magic_hex": "00010203",
                        }
                    ],
                },
            ],
            "manual_steps": "Launch Port de Exemplo.exe once to prepare resources.",
            "launch_file": "Binarios (x64)/Port de Exemplo.exe",
            "first_run_files": [
                {
                    "scope": "local_app_data",
                    "profile_folder": "Port (v5) Profile",
                    "path": "resource.o2r",
                    "min_size": 128,
                    "magic_hex": "504B0304",
                }
            ],
            "prerequisites": ["dotnet-desktop-10-x64", "openal-x64"],
        }
        rec_bytes = (json.dumps(v5_doc, indent=2) + "\n").encode("utf-8")
        rec_path.write_bytes(rec_bytes)

        idx_path = tmp / "index.json"
        idx = json.loads(idx_path.read_text(encoding="utf-8"))
        idx["recipes"].append(
            {
                "game_id": "extreme-g",
                "project_id": "v5-sample",
                "repository": "gitlab:example/group/v5-sample",
                "tag": "v1.0.0",
                "schema_version": 5,
                "path": rec_rel,
                "sha256": hashlib.sha256(rec_bytes).hexdigest(),
                "status": "experimental",
                "has_inputs": True,
                "has_manual_steps": True,
            }
        )
        idx_path.write_bytes((json.dumps(idx, indent=2) + "\n").encode("utf-8"))

        ok, errors, _ = validate_recipes.validate_repository(
            tmp, strict_lf=True, require_jsonschema=True
        )
        self.assertTrue(ok, f"Expected valid v5 recipe to pass, got: {errors}")

    def test_perfect_dark_verified_md5_import_v5(self) -> None:
        """Upgrading a manual US ROM copy must preserve exact MD5, size and path."""
        rel = "recipes/perfect-dark/perfect-dark-pc-port-perfect-dark/ci-dev-build.json"
        recipe = json.loads((REPO_ROOT / rel).read_text(encoding="utf-8"))
        self.assertEqual(recipe["schema_version"], 5)
        self.assertNotIn("manual_steps", recipe)
        self.assertEqual(
            recipe["operations"][-1],
            {
                "kind": "import_input",
                "scope": "installation",
                "source": "original-us-rom",
                "target": "pd-x86_64-windows/data/pd.ntsc-final.z64",
            },
        )
        input_file = recipe["inputs"][0]
        self.assertEqual(input_file["md5"], "e03b088b6ac9e0080440efed07c1e40f")
        self.assertEqual(input_file["size"], 33554432)
        self.assertEqual(input_file["magic_hex"], "80371240")
        self.assertEqual(input_file["extensions"], [".z64"])

        tmp = self._make_temp_repo()
        altered = tmp / rel
        broken = json.loads(altered.read_text(encoding="utf-8"))
        broken["inputs"][0]["md5"] = "not-a-md5"
        raw = (json.dumps(broken, indent=2) + "\n").encode("utf-8")
        altered.write_bytes(raw)
        idx_path = tmp / "index.json"
        idx = json.loads(idx_path.read_text(encoding="utf-8"))
        match = next(e for e in idx["recipes"] if e["project_id"] == recipe["project_id"])
        match["sha256"] = hashlib.sha256(raw).hexdigest()
        idx_path.write_bytes((json.dumps(idx, indent=2) + "\n").encode("utf-8"))
        ok, errors, _ = validate_recipes.validate_repository(
            tmp, strict_lf=True, require_jsonschema=True
        )
        self.assertFalse(ok)
        self.assertTrue(any("md5" in e.lower() for e in errors), errors)

    def test_lamborghini_verified_sha256_import_v5(self) -> None:
        """A canonical USA cart is verified and copied to the filename the port loads."""
        rel = "recipes/automobili-lamborghini/automobililamborghini-recomp/v0.11.1.json"
        recipe = json.loads((REPO_ROOT / rel).read_text(encoding="utf-8"))
        self.assertEqual(recipe["schema_version"], 5)
        self.assertNotIn("manual_steps", recipe)
        self.assertEqual(
            recipe["operations"],
            [
                {
                    "kind": "import_input",
                    "scope": "installation",
                    "source": "usa-cart",
                    "target": "Automobili Lamborghini (USA).z64",
                }
            ],
        )
        original = recipe["inputs"][0]
        self.assertEqual(original["size"], 4194304)
        self.assertEqual(original["sha256"], "cab2467684a58bc19c787423d704a961aa497629763367d9fe691172de58591c")
        self.assertEqual(original["magic_hex"], "80371240")
        self.assertEqual(original["extensions"], [".z64"])

        tmp = self._make_temp_repo()
        altered = tmp / rel
        broken = json.loads(altered.read_text(encoding="utf-8"))
        broken["operations"][0]["target"] = "../outside.z64"
        raw = (json.dumps(broken, indent=2) + "\n").encode("utf-8")
        altered.write_bytes(raw)
        index_file = tmp / "index.json"
        index = json.loads(index_file.read_text(encoding="utf-8"))
        next(e for e in index["recipes"] if e["project_id"] == recipe["project_id"])["sha256"] = (
            hashlib.sha256(raw).hexdigest()
        )
        index_file.write_bytes((json.dumps(index, indent=2) + "\n").encode("utf-8"))
        ok, errors, _ = validate_recipes.validate_repository(
            tmp, strict_lf=True, require_jsonschema=True
        )
        self.assertFalse(ok)
        self.assertTrue(any("unsafe" in e.lower() or "../" in e for e in errors), errors)

    def test_ctr_native_verified_disc_import_v5(self) -> None:
        """Import only the canonical, cryptographically verified NTSC-U CTR BIN."""
        rel = "recipes/crash-team-racing/ctr-native/beta-7.1.json"
        recipe = json.loads((REPO_ROOT / rel).read_text(encoding="utf-8"))
        self.assertEqual(recipe["schema_version"], 5)
        self.assertNotIn("manual_steps", recipe)
        self.assertEqual(
            recipe["operations"][-1],
            {
                "kind": "import_input",
                "scope": "installation",
                "source": "original-us-disc",
                "target": "ctr-native-beta-7_1-windows-x86/assets/ctr-u.bin",
            },
        )
        disc = recipe["inputs"][0]
        self.assertEqual(disc["size"], 605698800)
        self.assertEqual(disc["sha256"], "f780bf2331476aabfc00772fa758b12dd95ebfbc907968132cbd3cdd4e2c07c0")
        self.assertEqual(disc["extensions"], [".bin"])
        self.assertEqual(recipe["launch_file"], "ctr-native-beta-7_1-windows-x86/ctr_native.exe")

        tmp = self._make_temp_repo()
        altered = tmp / rel
        modified = json.loads(altered.read_text(encoding="utf-8"))
        modified["inputs"][0]["sha256"] = "broken"
        raw = (json.dumps(modified, indent=2) + "\n").encode("utf-8")
        altered.write_bytes(raw)
        index_file = tmp / "index.json"
        index = json.loads(index_file.read_text(encoding="utf-8"))
        entry = next(e for e in index["recipes"] if e["project_id"] == recipe["project_id"])
        entry["sha256"] = hashlib.sha256(raw).hexdigest()
        index_file.write_bytes((json.dumps(index, indent=2) + "\n").encode("utf-8"))
        ok, errors, _ = validate_recipes.validate_repository(tmp, strict_lf=True, require_jsonschema=True)
        self.assertFalse(ok)
        self.assertTrue(any("sha256" in e.lower() or "sha-256" in e.lower() for e in errors), errors)

    def test_high_octane_ctr_native_canonical_disc_v5(self) -> None:
        """The common upstream CTR NTSC-U 926 image can be imported in High Octane."""
        rel = "recipes/crash-team-racing/crash-team-racing-high-octane/v.1.5.json"
        recipe = json.loads((REPO_ROOT / rel).read_text(encoding="utf-8"))
        self.assertEqual(recipe["schema_version"], 5)
        self.assertEqual(recipe["operations"], [
            {"kind": "import_input", "scope": "installation",
             "source": "original-ctr-us-bin", "target": "assets/ctr-u.bin"}
        ])
        self.assertNotIn("manual_steps", recipe)
        original = recipe["inputs"][0]
        self.assertEqual(original["size"], 605698800)
        self.assertEqual(original["sha256"], "f780bf2331476aabfc00772fa758b12dd95ebfbc907968132cbd3cdd4e2c07c0")
        self.assertEqual(original["extensions"], [".bin"])
        self.assertEqual(recipe["launch_file"], "Crash Team Racing - High Octane.exe")
        tmp = self._make_temp_repo()
        rec_path = tmp / rel
        broken = json.loads(rec_path.read_text(encoding="utf-8"))
        broken["operations"][0]["target"] = "../out-of-bounds.bin"
        raw = (json.dumps(broken, indent=2) + "\n").encode("utf-8")
        rec_path.write_bytes(raw)
        idxpath = tmp / "index.json"
        idx = json.loads(idxpath.read_text(encoding="utf-8"))
        next(e for e in idx["recipes"] if e["project_id"] == recipe["project_id"])["sha256"] = hashlib.sha256(raw).hexdigest()
        idxpath.write_bytes((json.dumps(idx, indent=2) + "\n").encode("utf-8"))
        ok, errors, _ = validate_recipes.validate_repository(tmp, strict_lf=True, require_jsonschema=True)
        self.assertFalse(ok)
        self.assertTrue(any("unsafe" in e.lower() or "../" in e for e in errors), errors)

    def test_ggarecomp_sha1_local_app_data_import_v5(self) -> None:
        """The verified original US Goemon ROM is imported under LocalAppData."""
        rel = "recipes/goemon-s-great-adventure/ggarecomp/v0.3.0.json"
        recipe = json.loads((REPO_ROOT / rel).read_text(encoding="utf-8"))
        self.assertEqual(recipe["schema_version"], 5)
        self.assertEqual(recipe["operations"], [
            {"kind": "import_input", "scope": "local_app_data",
             "profile_folders": ["GGARecompiled"], "source": "gga-us-original",
             "target": "gga.us.z64"}
        ])
        self.assertIn("LOCALAPPDATA/GGARecompiled/gga.us.z64", recipe["manual_steps"])
        original = recipe["inputs"][0]
        self.assertEqual(original["sha1"], "9f9e860816f9e2a68bb5f4f56086e0c7450c64d7")
        self.assertEqual(original["magic_hex"], "80371240")
        self.assertEqual(original["extensions"], [".z64"])
        tmp = self._make_temp_repo()
        rec_path = tmp / rel
        broken = json.loads(rec_path.read_text(encoding="utf-8"))
        broken["operations"][0]["profile_folders"] = ["GGARecompiled/../../escape"]
        raw = (json.dumps(broken, indent=2) + "\n").encode("utf-8")
        rec_path.write_bytes(raw)
        idxpath = tmp / "index.json"
        idx = json.loads(idxpath.read_text(encoding="utf-8"))
        next(e for e in idx["recipes"] if e["project_id"] == recipe["project_id"])["sha256"] = hashlib.sha256(raw).hexdigest()
        idxpath.write_bytes((json.dumps(idx, indent=2) + "\n").encode("utf-8"))
        ok, errors, _ = validate_recipes.validate_repository(tmp, strict_lf=True, require_jsonschema=True)
        self.assertFalse(ok)
        self.assertTrue(any("profile_folders" in e or "unsafe" in e.lower() for e in errors), errors)

    def test_rejects_invalid_v5_contracts(self) -> None:
        self.assertTrue(
            validate_recipes.is_safe_relative_path(
                "Golden Sun Recompiled/games/The Broken Seal/GoldenSunRecomp.exe",
                allow_v5_chars=True,
            )[0]
        )
        self.assertFalse(
            validate_recipes.is_safe_relative_path(
                "dir/Trailing Space ", allow_v5_chars=True
            )[0]
        )
        self.assertFalse(
            validate_recipes.is_safe_relative_path("CON .exe", allow_v5_chars=True)[0]
        )

        tmp = self._make_temp_repo()
        rec_rel = "recipes/extreme-g/v5-bad/v1.0.0.json"
        rec_path = tmp / rec_rel
        rec_path.parent.mkdir(parents=True, exist_ok=True)
        bad_v5 = {
            "schema_version": 5,
            "project_id": "v5-bad",
            "tag": "v1.0.0",
            "source_url": "https://github.com/example/v5-bad/releases/tag/v1.0.0",
            "operations": [],
            "required_files": ["run.bat"],
            "inputs": [],
            "manual_steps": "Run batch.",
            "launch_file": "run.bat",
            "first_run_files": [
                {
                    "scope": "local_app_data",
                    "path": "cache.o2r",
                    "min_size": 128,
                    "magic_hex": "504B0304",
                }
            ],
            "prerequisites": ["python-3.12"],
        }
        rec_bytes = (json.dumps(bad_v5, indent=2) + "\n").encode("utf-8")
        rec_path.write_bytes(rec_bytes)

        idx_path = tmp / "index.json"
        idx = json.loads(idx_path.read_text(encoding="utf-8"))
        idx["recipes"].append(
            {
                "game_id": "extreme-g",
                "project_id": "v5-bad",
                "repository": "example/v5-bad",
                "tag": "v1.0.0",
                "schema_version": 5,
                "path": rec_rel,
                "sha256": hashlib.sha256(rec_bytes).hexdigest(),
                "status": "experimental",
                "has_inputs": False,
                "has_manual_steps": True,
            }
        )
        idx_path.write_bytes((json.dumps(idx, indent=2) + "\n").encode("utf-8"))

        ok, errors, _ = validate_recipes.validate_repository(
            tmp, strict_lf=True, require_jsonschema=True
        )
        self.assertFalse(ok)
        joined = "\n".join(errors)
        self.assertIn(".exe", joined)
        self.assertIn("profile_folder", joined)
        self.assertIn("prerequisites", joined)


if __name__ == "__main__":
    unittest.main()
