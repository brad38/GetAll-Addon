import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from catalog_coverage import coverage
from validate_recipes import load_catalog_lookup

class CatalogCoverageTests(unittest.TestCase):
    def setUp(self):
        self.catalog={"games":[{"id":"g","platform_group":"Nintendo Switch e Wii U","projects":[
            {"id":"p","source":{"github_repository":"owner/repo"}},
            {"id":"q","source":{"github_repository":"owner/other"}}]}]}
        self.empty={"recipes":[]}
        self.index={"recipes":[{"game_id":"g","project_id":"p","repository":"owner/repo","schema_version":9,"status":"experimental"}]}

    def test_category_does_not_change_recipe_identity(self):
        changed=copy.deepcopy(self.catalog)
        changed["games"][0]["platform_group"]="Nintendo Switch"
        with tempfile.TemporaryDirectory() as tmp:
            a,b=Path(tmp)/"a.json",Path(tmp)/"b.json"
            a.write_text(json.dumps(self.catalog),encoding="utf-8")
            b.write_text(json.dumps(changed),encoding="utf-8")
            self.assertEqual(load_catalog_lookup(str(a)),load_catalog_lookup(str(b)))
        original=coverage(self.catalog,self.empty,self.index)
        actual=coverage(changed,self.empty,self.index)
        for key in ("games","projects","main_covered","development_covered","missing","preparation_only","validated"):
            self.assertEqual(original[key],actual[key])
        self.assertEqual(actual["preparation_only"],1)
        self.assertEqual(actual["validated"],0)

    def test_duplicate_catalog_and_orphan_recipe_rejected(self):
        duplicate=copy.deepcopy(self.catalog)
        duplicate["games"][0]["projects"].append(duplicate["games"][0]["projects"][0])
        with self.assertRaises(ValueError):coverage(duplicate,self.empty,self.index)
        orphan=copy.deepcopy(self.index)
        orphan["recipes"][0]["project_id"]="unknown"
        with self.assertRaises(ValueError):coverage(self.catalog,self.empty,orphan)

    def test_multiple_versions_do_not_inflate_coverage(self):
        doubled=copy.deepcopy(self.index)
        doubled["recipes"].append(dict(doubled["recipes"][0],tag="different"))
        actual=coverage(self.catalog,self.empty,doubled)
        self.assertEqual(actual["development_covered"],1)
        self.assertEqual(actual["missing"],1)

if __name__=="__main__":unittest.main()
