"""Offline unit tests for scripts/upstream_watch.py."""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import upstream_watch  # noqa: E402
import validate_recipes  # noqa: E402


class UpstreamWatchTests(unittest.TestCase):
    def test_candidate_discovery_excludes_catalog_forks_and_invalid_results(self) -> None:
        fetcher = Mock(return_value=({"items": [
            {"full_name": "Ports/ExampleRecomp"},
            {"full_name": "ports/examplerecomp"},
            {"full_name": "known/Active"},
            {"full_name": "known/Archived"},
            {"full_name": "fork/Port", "fork": True},
            {"full_name": "org/Secret", "private": True},
            {"full_name": "org/Archived", "archived": True},
            {"full_name": "org/.."},
            {"full_name": "org/port|bad"},
        ]}, {}))
        result, errors = upstream_watch.discover_candidate_repositories(
            ["Known/Active", "Known/Archived"], {"User-Agent": "test"}, fetcher=fetcher)
        self.assertEqual(result, [{"repository": "Ports/ExampleRecomp",
                                   "url": "https://github.com/Ports/ExampleRecomp",
                                   "status": "review_required"}])
        self.assertEqual(errors, [])
        self.assertEqual(fetcher.call_count, 3)
        for call in fetcher.call_args_list:
            self.assertIn("/search/repositories?", call.args[0])
            self.assertIn("per_page=20", call.args[0])

    def test_discovery_candidates_do_not_mutate_recipes_or_trigger_publication(self) -> None:
        tmp = self._make_temp_repo()
        before = (tmp / "index.json").read_bytes()
        search = Mock(return_value=({"items": [{"full_name": "new/Port"}],
                                     "incomplete_results": True}, {}))
        with patch.object(upstream_watch, "fetch_json", search):
            result = upstream_watch.run_upstream_watch(
                tmp, catalog_data={"games": []}, apply_updates=True,
                releases_fetcher=lambda _: [], discover_candidates=True)
        self.assertFalse(result["has_actionable_changes"])
        self.assertFalse(result["catalog_mutations"])
        self.assertFalse(result["eligibility_mutations"])
        self.assertEqual((tmp / "index.json").read_bytes(), before)
        self.assertEqual(len(result["discovery_candidates"]), 1)
        self.assertIn("Incomplete results", result["api_errors"][0]["error"])
        self.assertIn("https://github.com/new/Port", upstream_watch.render_markdown_report(result))

    def _make_temp_repo(self) -> Path:
        tmp = Path(tempfile.mkdtemp(prefix="getall_watch_test_"))
        self.addCleanup(lambda: shutil.rmtree(tmp, ignore_errors=True))
        for d in ("schemas", "addons", "recipes", "docs"):
            shutil.copytree(REPO_ROOT / d, tmp / d)
        shutil.copy2(REPO_ROOT / "index.json", tmp / "index.json")
        for jf in tmp.rglob("*.json"):
            jf.write_bytes(jf.read_bytes().replace(b"\r\n", b"\n"))
        return tmp

    def _reviewed_scope(self, tmp: Path, project_ids: list[str], extra_catalog=None) -> dict:
        index = json.loads((tmp / "index.json").read_text(encoding="utf-8"))
        games = copy.deepcopy((extra_catalog or {}).get("games", []))
        decisions = {}
        for pid in project_ids:
            entry = next(e for e in index["recipes"] if e["project_id"] == pid)
            games.append({"id": entry["game_id"], "title": entry["game_id"], "projects": [{
                "id": pid, "source": {"provider": "github", "github_repository": entry["repository"]},
                "added_at": "2025-01-02",
            }]})
            decisions[pid] = {
                "eligible": True, "classification": "functional_with_limitations",
                "official_install_method": "Official fixture installation procedure for regression testing.",
                "provenance_review": "official_source",
                "gameplay_evidence": [{"url": "https://example.invalid/gameplay",
                    "kind": "user_gameplay_report", "observed": "Fixture player completes a level with the official build."}],
            }
        return {"catalog_data": {"games": games}, "eligibility_data": {"projects": decisions}}

    def _build_mock_zip(self, members: list[str]) -> tuple[Path, int, str]:
        tmp = Path(tempfile.mkdtemp(prefix="getall_mock_zip_"))
        self.addCleanup(lambda: shutil.rmtree(tmp, ignore_errors=True))
        zip_path = tmp / "release-win64.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            for member in members:
                zf.writestr(member, b"dummy")
        raw = zip_path.read_bytes()
        return zip_path, len(raw), hashlib.sha256(raw).hexdigest()

    def test_stages_compatible_experimental_update_and_preserves_existing_recipes(self) -> None:
        tmp = self._make_temp_repo()
        initial_count = len(json.loads((tmp / "index.json").read_text(encoding="utf-8"))["recipes"])
        zip_path, zsize, zsha = self._build_mock_zip(["Starship.exe", "starship.o2r"])

        mock_catalog = {"games": []}

        def mock_releases(repo: str) -> list[dict]:
            if repo == "HarbourMasters/Starship":
                return [
                    {
                        "tag_name": "9.4.0",
                        "draft": False,
                        "prerelease": False,
                        "html_url": "https://github.com/HarbourMasters/Starship/releases/tag/9.4.0",
                        "assets": [
                            {
                                "name": "SoH-Test-Win64.zip",
                                "browser_download_url": "https://github.com/HarbourMasters/Starship/releases/download/9.4.0/SoH-Test-Win64.zip",
                                "size": zsize,
                            }
                        ],
                    }
                ]
            return []

        def mock_inspector(asset_name: str, url: str, declared_size=None):
            return upstream_watch.inspect_local_zip(
                zip_path,
                asset_name=asset_name,
                asset_url=url,
                size_bytes=zsize,
                sha256_hex=zsha,
            )

        res = upstream_watch.run_upstream_watch(
            tmp,
            scope="tracked",
            apply_updates=True,
            inspect_assets=True,
            **self._reviewed_scope(tmp, ["starship"]),
            releases_fetcher=mock_releases,
            asset_inspector=mock_inspector,
        )

        self.assertTrue(res["has_actionable_changes"])
        self.assertEqual(len(res["updated_recipes"]), 1)
        self.assertEqual(res["updated_recipes"][0]["new_tag"], "9.4.0")
        self.assertEqual(res["updated_recipes"][0]["zip_sha256"], zsha)

        # Ensure index now preserves all previous entries + adds new experimental 9.4.0
        idx = json.loads((tmp / "index.json").read_text(encoding="utf-8"))
        self.assertEqual(len(idx["recipes"]), initial_count + 1)
        self.assertEqual(
            [e["status"] for e in idx["recipes"] if e["project_id"] == "starship"],
            ["experimental", "experimental"],
        )

        ok, errs, _ = validate_recipes.validate_repository(tmp, strict_lf=True)
        self.assertTrue(ok, f"Generated recipe must pass strict validation: {errs}")

    def test_does_not_downgrade_extended_contracts_or_reactivate_recipes(self) -> None:
        # These real recipes have no top-level inputs/operations. Their newer
        # contracts still carry essential runtime, asset or build requirements.
        cases = [
            ("redriver2", "experimental"),
            ("autotmc-auto-tmc", "experimental"),
            ("severed-chains", "experimental"),
            ("marathon-recompiled", "experimental"),
            ("ship-of-harkinian-soh", "disabled"),
            ("ship-of-harkinian-soh", "draft"),
        ]
        for project_id, status in cases:
            with self.subTest(project_id=project_id, status=status):
                tmp = self._make_temp_repo()
                index_path = tmp / "index.json"
                index = json.loads(index_path.read_text(encoding="utf-8"))
                entry = next(e for e in index["recipes"] if e["project_id"] == project_id)
                entry["status"] = status
                index["recipes"] = [entry]
                index_path.write_text(json.dumps(index), encoding="utf-8")
                original_index = index_path.read_bytes()
                recipe_path = tmp / entry["path"]
                original_recipe = recipe_path.read_bytes()
                recipe = json.loads(original_recipe)
                inspection = upstream_watch.ZipInspection(
                    asset_name="Fixture-Windows.zip",
                    asset_url="https://example.invalid/fixture.zip",
                    size_bytes=1,
                    sha256="0" * 64,
                    files=recipe["required_files"],
                    executables=[],
                    invalid_sdk_paths=[],
                )
                inspector = Mock(return_value=inspection)
                release = {
                    "tag_name": "fixture-next-release",
                    "draft": False,
                    "prerelease": False,
                    "assets": [{
                        "name": inspection.asset_name,
                        "browser_download_url": inspection.asset_url,
                        "size": inspection.size_bytes,
                    }],
                }
                result = upstream_watch.run_upstream_watch(
                    tmp, scope="tracked", apply_updates=True, inspect_assets=True,
                    **self._reviewed_scope(tmp, [project_id]),
                    releases_fetcher=lambda _: [release],
                    asset_inspector=inspector,
                )

                self.assertEqual(result["updated_recipes"], [])
                self.assertEqual(len(result["pending_reviews"]), 1)
                self.assertEqual(result["pending_reviews"][0]["project_id"], project_id)
                self.assertEqual(index_path.read_bytes(), original_index)
                self.assertEqual(recipe_path.read_bytes(), original_recipe)
                inspector.assert_not_called()

    def test_mixed_project_versions_require_review_in_any_index_order(self) -> None:
        for schema, status in ((5, "experimental"), (3, "disabled"), (3, "draft")):
            for protected_first in (True, False):
                with self.subTest(schema=schema, status=status, protected_first=protected_first):
                    tmp = self._make_temp_repo()
                    index_path = tmp / "index.json"
                    index = json.loads(index_path.read_text(encoding="utf-8"))
                    entry = next(e for e in index["recipes"] if e["project_id"] == "starship")
                    recipe = json.loads((tmp / entry["path"]).read_text(encoding="utf-8"))
                    protected = copy.deepcopy(recipe)
                    protected["schema_version"] = schema
                    protected["tag"] = "fixture-protected-version"
                    protected["source_url"] = "https://github.com/HarbourMasters/Starship/releases/tag/fixture-protected-version"
                    if schema == 5:
                        protected["prerequisites"] = ["openal-x64"]
                    protected_path = str(Path(entry["path"]).with_name("fixture-protected-version.json"))
                    protected_bytes = json.dumps(protected).encode("utf-8")
                    (tmp / protected_path).write_bytes(protected_bytes)
                    protected_entry = dict(
                        entry, schema_version=schema, status=status,
                        tag=protected["tag"], path=protected_path,
                        sha256=hashlib.sha256(protected_bytes).hexdigest(),
                    )
                    index["recipes"] = [protected_entry, entry] if protected_first else [entry, protected_entry]
                    index_path.write_text(json.dumps(index), encoding="utf-8")
                    original_index = index_path.read_bytes()
                    inspection = upstream_watch.ZipInspection(
                        "Fixture-Windows.zip", "https://example.invalid/fixture.zip",
                        1, "0" * 64, recipe["required_files"], [], [],
                    )
                    inspector = Mock(return_value=inspection)
                    release = {
                        "tag_name": "fixture-next-release", "draft": False, "prerelease": False,
                        "assets": [{"name": inspection.asset_name,
                                    "browser_download_url": inspection.asset_url, "size": 1}],
                    }
                    result = upstream_watch.run_upstream_watch(
                        tmp, scope="tracked", apply_updates=True, inspect_assets=True,
                        **self._reviewed_scope(tmp, ["starship"]), releases_fetcher=lambda _: [release],
                        asset_inspector=inspector,
                    )
                    self.assertEqual(result["updated_recipes"], [])
                    self.assertEqual(len(result["pending_reviews"]), 1)
                    self.assertEqual(index_path.read_bytes(), original_index)
                    self.assertEqual((tmp / protected_path).read_bytes(), protected_bytes)
                    inspector.assert_not_called()

    def test_never_auto_updates_validated_recipe_and_blocks_incompatible_zip(self) -> None:
        tmp = self._make_temp_repo()
        initial_count = len(json.loads((tmp / "index.json").read_text(encoding="utf-8"))["recipes"])
        # Missing Starship.exe and has space in name -> must NOT create recipe
        bad_zip_path, bad_size, bad_sha = self._build_mock_zip(
            ["Ship App.exe", "starship.o2r"]
        )
        ok_zip_path, ok_size, ok_sha = self._build_mock_zip(
            ["sm64coopdx.exe", "coopdx_updater.exe", "discord_game_sdk.dll", "coop.map"]
        )

        mock_catalog = {
            "games": [
                {
                    "id": "new-test-game",
                    "title": "New Test Game",
                    "projects": [
                        {
                            "id": "brand-new-port",
                            "fallback_name": "Brand New Port",
                            "source": {
                                "provider": "github",
                                "github_repository": "example/brand-new-port",
                            },
                        }
                    ],
                }
            ]
        }

        def mock_releases(repo: str) -> list[dict]:
            if repo == "coop-deluxe/sm64coopdx":
                return [
                    {
                        "tag_name": "v1.6.0",
                        "draft": False,
                        "prerelease": False,
                        "html_url": "https://github.com/coop-deluxe/sm64coopdx/releases/tag/v1.6.0",
                        "assets": [
                            {
                                "name": "sm64coopdx_Windows.zip",
                                "browser_download_url": "https://github.com/coop-deluxe/sm64coopdx/releases/download/v1.6.0/sm64coopdx_Windows.zip",
                                "size": ok_size,
                            }
                        ],
                    }
                ]
            if repo == "HarbourMasters/Starship":
                return [
                    {
                        "tag_name": "9.5.0",
                        "draft": False,
                        "prerelease": False,
                        "html_url": "https://github.com/HarbourMasters/Starship/releases/tag/9.5.0",
                        "assets": [
                            {
                                "name": "SoH-Win64.zip",
                                "browser_download_url": "https://github.com/HarbourMasters/Starship/releases/download/9.5.0/SoH-Win64.zip",
                                "size": bad_size,
                            }
                        ],
                    }
                ]
            return []

        def mock_inspector(asset_name: str, url: str, declared_size=None):
            zp, sz, sh = (
                (ok_zip_path, ok_size, ok_sha)
                if "sm64coopdx" in url
                else (bad_zip_path, bad_size, bad_sha)
            )
            return upstream_watch.inspect_local_zip(
                zp, asset_name=asset_name, asset_url=url, size_bytes=sz, sha256_hex=sh
            )

        res = upstream_watch.run_upstream_watch(
            tmp,
            scope="tracked",
            apply_updates=True,
            inspect_assets=True,
            **self._reviewed_scope(tmp, ["starship", "sm64coopdx-super-mario-64-coop-deluxe"], mock_catalog),
            releases_fetcher=mock_releases,
            asset_inspector=mock_inspector,
        )

        self.assertEqual(len(res["updated_recipes"]), 0)
        self.assertEqual(len(res["new_catalog_projects"]), 1)
        self.assertEqual(len(res["pending_reviews"]), 2)
        idx = json.loads((tmp / "index.json").read_text(encoding="utf-8"))
        self.assertEqual(len(idx["recipes"]), initial_count)

    def test_selects_stable_release_over_prerelease(self) -> None:
        releases = [
            {"tag_name": "v2.0.0-rc1", "draft": False, "prerelease": True},
            {"tag_name": "v1.1.7", "draft": False, "prerelease": False},
        ]
        chosen = upstream_watch.select_latest_release(releases, allow_prerelease=False)
        self.assertIsNotNone(chosen)
        self.assertEqual(chosen["tag_name"], "v1.1.7")

    def test_unproven_and_excluded_projects_only_create_review_notes(self) -> None:
        for excluded in (False, True):
            with self.subTest(excluded=excluded):
                tmp=self._make_temp_repo()
                index_path=tmp/"index.json"
                index=json.loads(index_path.read_text(encoding="utf-8"))
                entry=next(e for e in index["recipes"] if e["project_id"]=="starship")
                index["recipes"]=[entry]
                index_path.write_text(json.dumps(index),encoding="utf-8")
                initial_index=index_path.read_bytes()
                source=self._reviewed_scope(tmp,["starship"])
                original_catalog=copy.deepcopy(source["catalog_data"])
                if excluded:
                    source["exclusions_data"]={"projects":{"starship":{
                        "game_id":entry["game_id"],"project":source["catalog_data"]["games"][0]["projects"][0],
                        "assessment":{"eligible":False}}}}
                    source["catalog_data"]={"games":[]}
                    original_catalog=copy.deepcopy(source["catalog_data"])
                else:
                    # Even a nominally eligible label cannot turn a README into play evidence.
                    source["eligibility_data"]["projects"]["starship"]["gameplay_evidence"][0]["kind"]="readme"
                initial_decisions=copy.deepcopy(source["eligibility_data"])
                inspector=Mock(side_effect=AssertionError("Review-only project must not download assets"))
                release={"tag_name":"v99.0.0","draft":False,"prerelease":False,
                         "html_url":"https://example.invalid/release","assets":[{
                         "name":"Starship-Windows.zip","browser_download_url":"https://example.invalid/port.zip","size":12}]}
                result=upstream_watch.run_upstream_watch(tmp,scope="all",apply_updates=True,inspect_assets=True,
                    **source,releases_fetcher=lambda _:[release],asset_inspector=inspector)
                self.assertEqual(result["updated_recipes"],[])
                self.assertEqual(len(result["pending_reviews"]),1)
                self.assertTrue(result["pending_reviews"][0]["review_only"])
                self.assertEqual(index_path.read_bytes(),initial_index)
                self.assertEqual(source["catalog_data"],original_catalog)
                self.assertEqual(source["eligibility_data"],initial_decisions)
                inspector.assert_not_called()

    def test_eligible_update_preserves_catalog_dates_and_eligibility_decisions(self) -> None:
        tmp=self._make_temp_repo()
        source=self._reviewed_scope(tmp,["starship"])
        original=copy.deepcopy(source)
        inspection=upstream_watch.ZipInspection("Starship-Windows.zip","https://example.invalid/port.zip",12,"a"*64,
            ["Starship.exe","starship.o2r"],["Starship.exe"],[])
        release={"tag_name":"v99.0.0","draft":False,"prerelease":False,"assets":[{
            "name":inspection.asset_name,"browser_download_url":inspection.asset_url,"size":12}]}
        result=upstream_watch.run_upstream_watch(tmp,scope="tracked",apply_updates=True,inspect_assets=True,
            **source,releases_fetcher=lambda repo:[release] if repo=="HarbourMasters/Starship" else [],
            asset_inspector=Mock(return_value=inspection))
        self.assertEqual(len(result["updated_recipes"]),1)
        self.assertEqual(source,original)
        self.assertFalse(result["catalog_mutations"])
        self.assertFalse(result["eligibility_mutations"])

    def test_catalog_watch_ignores_older_releases_and_deduplicates_fingerprint(self) -> None:
        releases = [
            {
                "tag_name": "nightly-v1.4.0",
                "draft": False,
                "prerelease": True,
                "published_at": "2026-11-22T17:51:20Z",
            },
            {
                "tag_name": "v1.3.1",
                "draft": False,
                "prerelease": False,
                "published_at": "2026-09-01T00:00:00Z",
            },
        ]
        self.assertIsNone(
            upstream_watch.select_newer_catalog_release(
                releases, {"nightly-v1.4.0"}, is_new_project=False
            )
        )

        # Verify deduplication via docs/MONITORAMENTO-UPSTREAM.md fingerprint
        tmp = self._make_temp_repo()
        mock_catalog = {
            "games": [
                {
                    "id": "new-test-game",
                    "title": "New Test Game",
                    "projects": [
                        {
                            "id": "brand-new-port",
                            "fallback_name": "Brand New Port",
                            "source": {
                                "provider": "github",
                                "github_repository": "example/brand-new-port",
                            },
                        }
                    ],
                }
            ]
        }
        res1 = upstream_watch.run_upstream_watch(
            tmp,
            scope="tracked",
            apply_updates=False,
            inspect_assets=False,
            catalog_data=mock_catalog,
            releases_fetcher=lambda repo: [],
        )
        self.assertTrue(res1["has_actionable_changes"])
        (tmp / "docs" / "MONITORAMENTO-UPSTREAM.md").write_text(
            upstream_watch.render_markdown_report(res1), encoding="utf-8"
        )
        res2 = upstream_watch.run_upstream_watch(
            tmp,
            scope="tracked",
            apply_updates=False,
            inspect_assets=False,
            catalog_data=mock_catalog,
            releases_fetcher=lambda repo: [],
        )
        self.assertTrue(res2["already_reported"])
        self.assertFalse(res2["has_actionable_changes"])


if __name__ == "__main__":
    unittest.main()
