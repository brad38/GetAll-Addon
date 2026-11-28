import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_recipes import validate_recipe_semantics


class PreparationContractTests(unittest.TestCase):
    def setUp(self):
        self.entries = [e for e in json.loads((ROOT / "index.json").read_text(encoding="utf-8"))["recipes"] if e["schema_version"] == 9]
        self.assertGreaterEqual(len(self.entries), 4)

    def test_exact_contracts(self):
        for entry in self.entries:
            with self.subTest(project=entry["project_id"]):
                raw = (ROOT / entry["path"]).read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(), entry["sha256"])
                self.assertEqual(validate_recipe_semantics(json.loads(raw), entry, "test"), [])

    def test_reject_unapproved_execution_and_mutations(self):
        for entry in self.entries:
            recipe = json.loads((ROOT / entry["path"]).read_text(encoding="utf-8"))
            for key, value in {"launch_file": "game.exe", "arguments": ["--run"], "installer_profile": "unknown", "command": "cmd", "build_profile": "unknown", "source_url": "https://example.org/kit", "operations": [{"command": "run"}], "required_files": ["other.exe"]}.items():
                with self.subTest(project=entry["project_id"], key=key):
                    bad = copy.deepcopy(recipe)
                    bad[key] = value
                    self.assertTrue(validate_recipe_semantics(bad, entry, "test"))
            bad = copy.deepcopy(recipe)
            bad["preparation_media"][0]["command"] = "run"
            self.assertTrue(validate_recipe_semantics(bad, entry, "test"))

    def test_reject_changed_preparation_media_contract(self):
        for entry in self.entries:
            recipe = json.loads((ROOT / entry["path"]).read_text(encoding="utf-8"))
            for position, media in enumerate(recipe["preparation_media"]):
                for field, value in {
                    "id": "unapproved-input",
                    "kind": "unapproved",
                    "extensions": [".unapproved"],
                    "version": "unapproved edition",
                }.items():
                    with self.subTest(project=entry["project_id"], media=media["id"], field=field):
                        bad = copy.deepcopy(recipe)
                        bad["preparation_media"][position][field] = value
                        self.assertTrue(validate_recipe_semantics(bad, entry, "test"))
            media = recipe["preparation_media"]
            changes = {
                "missing": media[:-1],
                "duplicate": media + [copy.deepcopy(media[-1])],
            }
            if len(media) > 1:
                changes["reordered"] = media[1:] + media[:1]
            for change, value in changes.items():
                with self.subTest(project=entry["project_id"], media_list=change):
                    bad = copy.deepcopy(recipe)
                    bad["preparation_media"] = value
                    self.assertTrue(validate_recipe_semantics(bad, entry, "test"))

    def test_reject_wrong_index_identity_and_status(self):
        for entry in self.entries:
            recipe = json.loads((ROOT / entry["path"]).read_text(encoding="utf-8"))
            for key, value in {"status": "validated", "game_id": "wrong", "project_id": "wrong", "repository": "other/repo", "tag": "wrong", "has_inputs": True, "has_manual_steps": False}.items():
                with self.subTest(project=entry["project_id"], key=key):
                    self.assertTrue(validate_recipe_semantics(recipe, dict(entry, **{key: value}), "test"))


if __name__ == "__main__":
    unittest.main()
