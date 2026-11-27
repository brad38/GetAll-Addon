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

    def test_inactive_recipes_remain_visible_without_covering_a_project(self):
        for status in ("disabled","draft"):
            with self.subTest(status=status):
                inactive=copy.deepcopy(self.index)
                inactive["recipes"][0]["status"]=status
                actual=coverage(self.catalog,inactive,inactive)
                self.assertEqual(actual["main_covered"],0)
                self.assertEqual(actual["development_covered"],0)
                self.assertEqual(actual["missing"],2)
                self.assertEqual(actual["preparation_only"],0)
                self.assertEqual(actual["validated"],0)
                row=next(r for r in actual["rows"] if r["project_id"]=="p")
                self.assertEqual(row["main"],inactive["recipes"])
                self.assertEqual(row["development"],inactive["recipes"])
                self.assertFalse(row["main_covered"])
                self.assertFalse(row["development_covered"])

    def test_inactive_versions_do_not_mask_usable_preparation_recipes(self):
        mixed=copy.deepcopy(self.index)
        recipe=mixed["recipes"][0]
        mixed["recipes"].extend([
            dict(recipe,status="disabled",schema_version=3,tag="disabled"),
            dict(recipe,status="draft",schema_version=5,tag="draft"),
        ])
        actual=coverage(self.catalog,mixed,mixed)
        self.assertEqual(actual["main_covered"],1)
        self.assertEqual(actual["development_covered"],1)
        self.assertEqual(actual["missing"],1)
        self.assertEqual(actual["preparation_only"],1)
        self.assertEqual(actual["validated"],0)
        row=next(r for r in actual["rows"] if r["project_id"]=="p")
        self.assertEqual(row["main"],mixed["recipes"])
        self.assertEqual(row["development"],mixed["recipes"])
        self.assertTrue(row["main_covered"])
        self.assertTrue(row["development_covered"])

    def test_main_and_development_statuses_are_counted_independently(self):
        inactive=copy.deepcopy(self.index)
        inactive["recipes"][0]["status"]="disabled"
        for main,development,expected_main,expected_development in (
            (inactive,self.index,0,1),
            (self.index,inactive,1,0),
        ):
            with self.subTest(main_covered=expected_main):
                actual=coverage(self.catalog,main,development)
                self.assertEqual(actual["main_covered"],expected_main)
                self.assertEqual(actual["development_covered"],expected_development)
                self.assertEqual(actual["missing"],2-expected_development)

    def test_validated_versions_are_counted_once_per_project(self):
        recipe=self.index["recipes"][0]
        versions={"recipes":[
            dict(recipe,status="validated",schema_version=3,tag="v1"),
            dict(recipe,status="validated",schema_version=3,tag="v2"),
            dict(recipe,status="disabled",schema_version=3,tag="v3"),
            dict(recipe,project_id="q",repository="owner/other",tag="v1"),
            dict(recipe,project_id="q",repository="owner/other",status="draft",tag="v2"),
        ]}
        actual=coverage(self.catalog,versions,versions)
        self.assertEqual(actual["main_covered"],2)
        self.assertEqual(actual["development_covered"],2)
        self.assertEqual(actual["missing"],0)
        self.assertEqual(actual["validated"],1)
        self.assertEqual(actual["preparation_only"],1)
        rows={row["project_id"]:row for row in actual["rows"]}
        self.assertTrue(rows["p"]["validated"])
        self.assertFalse(rows["q"]["validated"])

if __name__=="__main__":unittest.main()
