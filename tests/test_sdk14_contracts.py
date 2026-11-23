"""SDK 1.4.0 v6/v7 positive and negative contracts; no ROMs or external code are executed."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import validate_recipes as val


class SDK14ContractsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schemas, cls.registry = val.load_schema_registry(ROOT / "schemas")

    def sample(self, name):
        return json.loads((ROOT / "examples" / "sdk14-synthetic" /
                           (name + ".synthetic.json")).read_text(encoding="utf-8"))

    def errors(self, item):
        from urllib.parse import urlsplit
        parts = urlsplit(item["source_url"]).path.strip("/").split("/")
        repository = "/".join(parts[:2])
        entry = dict(schema_version=item["schema_version"],
                     project_id=item["project_id"], tag=item["tag"],
                     repository=repository,
                     has_inputs=bool(item["inputs"]),
                     has_manual_steps=bool(item.get("manual_steps")))
        # Synthetic handoff examples use a repository root URL; our strict GetAll
        # contract requires a release/source path beneath the declared repository.
        semantic_document = copy.deepcopy(item)
        if semantic_document["source_url"].rstrip("/") == f"https://github.com/{repository}":
            semantic_document["source_url"] += "/"
        errors = val.validate_recipe_semantics(semantic_document, entry, "synthetic")
        schema_version = item["schema_version"]
        if val.HAS_JSONSCHEMA:
            validator = val.Draft202012Validator(self.schemas[schema_version], registry=self.registry)
            errors += [f"schema: {e.message}" for e in validator.iter_errors(item)]
        return errors

    def test_valid_synthetic_contract_examples(self):
        for name in ("v6-portable-multiasset", "v7-java", "v7-arcade-romset",
                     "v7-multitrack", "v7-nested-profile"):
            with self.subTest(name=name):
                self.assertEqual(self.errors(self.sample(name)), [])

    def test_v6_rejects_executable_payload_and_malformed_assets(self):
        doc = self.sample("v6-portable-multiasset")
        for mutation in [
            lambda d: d["assets"][1].update(target="payload.exe"),
            lambda d: d["assets"][0].update(target="something.exe"),
            lambda d: d["assets"][0].update(sha256="not-hex"),
            lambda d: d["assets"][0].update(size=0),
            lambda d: d["assets"][0].update(extra="forbidden"),
            lambda d: d["assets"].append(dict(d["assets"][0])),
            lambda d: d["assets"][1].update(target="../escape.dat"),
        ]:
            candidate = copy.deepcopy(doc)
            mutation(candidate)
            self.assertTrue(self.errors(candidate), candidate)

    def test_v7_java_rejects_command_bypass_and_missing_jar(self):
        doc = self.sample("v7-java")
        for mutation in [
            lambda d: d["java_launcher"].update(jar="unknown.jar"),
            lambda d: d["java_launcher"].update(jar="../evil.jar"),
            lambda d: d["java_launcher"].update(runtime="java-17"),
            lambda d: d["java_launcher"].update(args=["-cp", "foo"]),
            lambda d: d.update(launch_file="game.exe"),
            lambda d: d.update(prerequisites=[]),
            lambda d: d.update(installer_profile="unapproved"),
            lambda d: d.update(build_profile="unapproved"),
        ]:
            candidate = copy.deepcopy(doc)
            mutation(candidate)
            self.assertTrue(self.errors(candidate), candidate)

    def test_v7_arcade_rejects_unverified_and_escaped_members(self):
        doc = self.sample("v7-arcade-romset")
        member = doc["inputs"][0]["files"][0]
        self.assertEqual((member["path"], member["size"], member["crc32"]),
                         ("epr-test.88", 9, "CBF43926"))
        for mutation in [
            lambda d: d["inputs"][0]["files"][0].pop("crc32"),
            lambda d: d["inputs"][0]["files"][0].pop("size"),
            lambda d: d["inputs"][0]["files"][0].update(crc32="zzzzzzzz"),
            lambda d: d["inputs"][0]["files"][0].update(path="../ROM.88"),
            lambda d: d["inputs"][0]["files"].append(dict(d["inputs"][0]["files"][0])),
            lambda d: d["inputs"][0].update(kind="directory"),
        ]:
            candidate = copy.deepcopy(doc)
            mutation(candidate)
            self.assertTrue(self.errors(candidate), candidate)

    def test_v7_multitrack_requires_cue_and_bin_entries(self):
        doc = self.sample("v7-multitrack")
        for mutation in [
            lambda d: d["inputs"][0]["files"].__setitem__(slice(None),
                [x for x in d["inputs"][0]["files"] if not x["path"].endswith(".cue")]),
            lambda d: d["inputs"][0]["files"].__setitem__(slice(None),
                [x for x in d["inputs"][0]["files"] if not x["path"].endswith(".bin")]),
            lambda d: d["inputs"][0]["files"][0].update(path="../evil.cue"),
        ]:
            candidate=copy.deepcopy(doc);mutation(candidate)
            self.assertTrue(self.errors(candidate), candidate)

    def test_v7_profile_blocks_traversal(self):
        doc=self.sample("v7-nested-profile")
        for bad in ("Vendor/../../escape", "C:/Vendor", "//server/share", "Vendor/CON",
                    "Vendor\\evil"):
            candidate=copy.deepcopy(doc)
            candidate["operations"][0]["profile_folders"]=[bad]
            self.assertTrue(self.errors(candidate), candidate)

    def test_real_v6_v7_recipes_strong_sources(self):
        index=json.loads((ROOT/"index.json").read_text(encoding="utf-8"))
        entries={e["project_id"]:e for e in index["recipes"]}
        self.assertEqual(len(index["recipes"]), 93)  # Project Picori v7 added in Round 12
        self.assertEqual(entries["autotmc-auto-tmc"]["schema_version"],6)
        self.assertEqual(entries["cannonball"]["schema_version"],7)
        for name in ("cannonball","zelda3","smw","autotmc-auto-tmc"):
            rec=json.loads((ROOT/entries[name]["path"]).read_text(encoding="utf-8"))
            self.assertEqual(self.errors(rec),[],name)
            self.assertEqual(entries[name]["status"],"experimental")
        cannon=json.loads((ROOT/entries["cannonball"]["path"]).read_text(encoding="utf-8"))
        members=cannon["inputs"][0]["files"]
        self.assertEqual(len(members),31)
        self.assertEqual(len({m["path"].lower() for m in members}),31)
        self.assertIn(dict(path="epr-10381b.132",size=65536,crc32="BE8C412B"),members)
        smw=json.loads((ROOT/entries["smw"]["path"]).read_text(encoding="utf-8"))
        self.assertEqual(smw["inputs"][0]["sha1"],"6b47bb75d16514b6a476aa0c73a683a2a4c18765")
        zelda=json.loads((ROOT/entries["zelda3"]["path"]).read_text(encoding="utf-8"))
        self.assertEqual(zelda["inputs"][0]["sha256"],"66871d66be19ad2c34c927d6b14cd8eb6fc3181965b6e517cb361f7316009cfb")


    def test_picori_v7_imports_verified_usa_rom(self):
        index = json.loads((ROOT / "index.json").read_text(encoding="utf-8"))
        entry = next(e for e in index["recipes"] if e["project_id"] == "project-picori-999sian-tmc")
        self.assertEqual(entry["repository"], "999sian/tmc")
        self.assertEqual(entry["status"], "experimental")
        self.assertEqual(entry["schema_version"], 7)
        self.assertTrue(entry["has_inputs"])
        recipe = json.loads((ROOT / entry["path"]).read_text(encoding="utf-8"))
        self.assertEqual(self.errors(recipe), [])
        self.assertEqual(recipe["source_url"], "https://github.com/999sian/tmc/releases/tag/v0.9.6")
        self.assertEqual(recipe["launch_file"], "tmc_pc.exe")
        self.assertIn("baserom.gba", recipe["required_files"])
        self.assertEqual(recipe["inputs"][0]["sha1"], "b4bd50e4131b027c334547b4524e2dbbd4227130")
        self.assertEqual(recipe["operations"][0], {
            "kind": "import_input", "source": "original-minish-cap-usa",
            "target": "baserom.gba", "scope": "installation",
        })
        for mutate in [
            lambda d: d["inputs"][0].pop("sha1"),
            lambda d: d["operations"][0].update(target="../outside.gba"),
            lambda d: d.update(installer_profile="powershell"),
        ]:
            invalid = copy.deepcopy(recipe)
            mutate(invalid)
            self.assertTrue(self.errors(invalid))



if __name__=="__main__":
    unittest.main()
