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
            stats["recipe_count"] - 1,
        )

    def _make_temp_repo(self) -> Path:
        tmp = Path(tempfile.mkdtemp(prefix="getall_val_test_"))
        self.addCleanup(lambda: shutil.rmtree(tmp, ignore_errors=True))
        shutil.copytree(REPO_ROOT / "schemas", tmp / "schemas")
        shutil.copytree(REPO_ROOT / "addons", tmp / "addons")
        shutil.copytree(REPO_ROOT / "recipes", tmp / "recipes")
        shutil.copy2(REPO_ROOT / "index.json", tmp / "index.json")
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


if __name__ == "__main__":
    unittest.main()
