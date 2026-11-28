import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from catalog_coverage import coverage, validate_execution_evidence
from catalog_scope import companion_source, is_eligible
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

    def test_schema_nine_alias_does_not_override_implemented_evidence(self):
        index=copy.deepcopy(self.index)
        index["recipes"][0].update(tag="v1",sha256="a"*64)
        record=self._execution("automated_installation_implemented",status="implemented",data_kind="code_review")
        actual=coverage(self.catalog,self.empty,index,evidence=record)
        row=actual["rows"][0]
        self.assertTrue(row["uses_closed_preparation_profiles"])
        self.assertEqual(row["dimensions"]["automated_installation_implemented"]["status"],"implemented")
        self.assertEqual(actual["uses_closed_preparation_profiles"],actual["preparation_only"])
        self.assertIn("does not imply",actual["legacy_preparation_only_semantics"])

    def test_disabled_contract_preserves_specific_blocker_and_evidence(self):
        index=copy.deepcopy(self.index)
        index["recipes"][0].update(tag="v1",sha256="a"*64,status="disabled")
        record=self._execution("automated_installation_implemented",status="blocked",data_kind="code_review")
        blocked=record["projects"]["p"]["dimensions"]["automated_installation_implemented"]
        blocked["reason"]="Required upstream runtime exports a different target; no intact Windows contract verified."
        actual=coverage(self.catalog,self.empty,index,evidence=record)
        self.assertEqual(actual["rows"][0]["dimensions"]["automated_installation_implemented"],blocked)

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

    def _assessment(self):
        return {"eligible": True, "classification": "functional_with_limitations",
                "official_install_method": "Use the official documented installer and original game data.",
                "provenance_review": "official_source",
                "gameplay_evidence": [{"url": "https://example.invalid/issues/1",
                    "kind": "user_gameplay_report", "observed": "Player reaches the second level using the official release."}]}

    def _execution(self, name, status="passed", data_kind="synthetic", scope="getall"):
        return {"projects": {"p": {"recipe_revisions": [{"tag": "v1", "sha256": "a"*64}],
            "dimensions": {name: {"status": status, "evidence": [{
                "url": "https://example.invalid/test-report", "observed": "Fixture result, limited to the recorded operation.",
                "data_kind": data_kind, "scope": scope}]}}}}}

    def test_upstream_gameplay_and_synthetic_test_do_not_prove_getall_boot(self):
        index=copy.deepcopy(self.index)
        index["recipes"][0].update(tag="v1",sha256="a"*64,status="validated")
        eligibility={"projects": {pid: self._assessment() for pid in ("p","q")}}
        actual=coverage(self.catalog,index,index,eligibility=eligibility,
                        evidence=self._execution("synthetic_validation"))
        dims=actual["rows"][0]["dimensions"]
        self.assertEqual(dims["upstream_functional"]["status"],"evidenced")
        self.assertEqual(dims["synthetic_validation"]["status"],"passed")
        for name in ("original_media_installation","first_boot","gameplay"):
            self.assertEqual(dims[name]["status"],"unknown")
        self.assertFalse(actual["legacy_validated_is_execution_evidence"])

    def test_original_media_dimensions_reject_synthetic_and_upstream_scope(self):
        for name in ("original_media_installation","first_boot","gameplay"):
            for data_kind,scope in (("synthetic","getall"),("original_media","upstream_external")):
                with self.subTest(name=name,data_kind=data_kind,scope=scope):
                    with self.assertRaisesRegex(ValueError,"requires original-media GetAll"):
                        validate_execution_evidence(self._execution(name,data_kind=data_kind,scope=scope))

    def test_changed_recipe_hash_invalidates_current_execution_credit(self):
        index=copy.deepcopy(self.index)
        index["recipes"][0].update(tag="v1",sha256="b"*64)
        actual=coverage(self.catalog,index,index,evidence=self._execution("synthetic_validation"))
        self.assertEqual(actual["rows"][0]["dimensions"]["synthetic_validation"]["status"],"historical")
        unbound=self._execution("synthetic_validation")
        del unbound["projects"]["p"]["recipe_revisions"]
        with self.assertRaisesRegex(ValueError,"exact recipe tag"):
            validate_execution_evidence(unbound)

    def test_disabled_registered_exclusion_is_history_but_active_orphan_fails(self):
        catalog=copy.deepcopy(self.catalog)
        catalog["games"][0]["projects"]=[catalog["games"][0]["projects"][1]]
        exclusions={"projects":{"p":{"game_id":"g","project":self.catalog["games"][0]["projects"][0],
                                       "assessment":{"eligible":False}}}}
        disabled=copy.deepcopy(self.index)
        disabled["recipes"][0]["status"]="disabled"
        result=coverage(catalog,self.empty,disabled,exclusions=exclusions)
        self.assertEqual(result["projects"],1)
        self.assertEqual(len(result["historical_excluded_recipes"]),1)
        for main,development in ((self.index,self.empty),(self.empty,self.index)):
            with self.assertRaisesRegex(ValueError,"Orphan active/unregistered"):
                coverage(catalog,main,development,exclusions=exclusions)

    def test_readme_release_and_build_are_not_gameplay_eligibility(self):
        for kind in ("readme","release_exists","build_success","synthetic_test","title_screen"):
            assessment=self._assessment()
            assessment["gameplay_evidence"][0]["kind"]=kind
            self.assertFalse(is_eligible(assessment),kind)
            with self.assertRaisesRegex(ValueError,"functional assessment"):
                coverage(self.catalog,self.empty,self.index,eligibility={"projects":{"p":assessment}})

    def test_registry_companions_keep_catalog_revision(self):
        source="https://raw.githubusercontent.com/owner/catalog/"+"a"*40+"/catalog.json"
        self.assertEqual(companion_source(source,"eligibility.json"),source.replace("catalog.json","eligibility.json"))
        with self.assertRaises(ValueError):
            companion_source(source,"../../main/eligibility.json")

    def test_local_evidence_requires_matching_file_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"report.txt"
            p.write_text("actual report",encoding="utf-8")
            record=self._execution("synthetic_validation")
            proof=record["projects"]["p"]["dimensions"]["synthetic_validation"]["evidence"][0]
            proof.update(path="report.txt",sha256="0"*64)
            with self.assertRaisesRegex(ValueError,"Evidence file hash mismatch"):
                validate_execution_evidence(record,tmp)
            proof["path"]="../outside-report.txt"
            with self.assertRaisesRegex(ValueError,"Missing/unsafe evidence"):
                validate_execution_evidence(record,tmp)

if __name__=="__main__":unittest.main()
