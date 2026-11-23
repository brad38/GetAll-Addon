"""Offline unit tests for scripts/upstream_watch.py."""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import upstream_watch  # noqa: E402
import validate_recipes  # noqa: E402


class UpstreamWatchTests(unittest.TestCase):
    def _make_temp_repo(self) -> Path:
        tmp = Path(tempfile.mkdtemp(prefix="getall_watch_test_"))
        self.addCleanup(lambda: shutil.rmtree(tmp, ignore_errors=True))
        for d in ("schemas", "addons", "recipes", "docs"):
            shutil.copytree(REPO_ROOT / d, tmp / d)
        shutil.copy2(REPO_ROOT / "index.json", tmp / "index.json")
        for jf in tmp.rglob("*.json"):
            jf.write_bytes(jf.read_bytes().replace(b"\r\n", b"\n"))
        return tmp

    def _build_mock_zip(self, members: list[str]) -> tuple[Path, int, str]:
        tmp = Path(tempfile.mkdtemp(prefix="getall_mock_zip_"))
        self.addCleanup(lambda: shutil.rmtree(tmp, ignore_errors=True))
        zip_path = tmp / "release-win64.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            for member in members:
                zf.writestr(member, b"dummy")
        raw = zip_path.read_bytes()
        return zip_path, len(raw), hashlib.sha256(raw).hexdigest()

    def test_stages_compatible_experimental_update_and_preserves_all_14_recipes(self) -> None:
        tmp = self._make_temp_repo()
        zip_path, zsize, zsha = self._build_mock_zip(
            ["Ghostship.exe", "ghostship.o2r", "shaderc_shared.dll", "tcc.dll"]
        )

        mock_catalog = {"games": []}

        def mock_releases(repo: str) -> list[dict]:
            if repo == "HarbourMasters/Ghostship":
                return [
                    {
                        "tag_name": "3.1.0",
                        "draft": False,
                        "prerelease": False,
                        "html_url": "https://github.com/HarbourMasters/Ghostship/releases/tag/3.1.0",
                        "assets": [
                            {
                                "name": "Ghostship-3.1.0-Win64.zip",
                                "browser_download_url": "https://github.com/HarbourMasters/Ghostship/releases/download/3.1.0/Ghostship-3.1.0-Win64.zip",
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
            catalog_data=mock_catalog,
            releases_fetcher=mock_releases,
            asset_inspector=mock_inspector,
        )

        self.assertTrue(res["has_actionable_changes"])
        self.assertEqual(len(res["updated_recipes"]), 1)
        self.assertEqual(res["updated_recipes"][0]["new_tag"], "3.1.0")
        self.assertEqual(res["updated_recipes"][0]["zip_sha256"], zsha)

        # Ensure index now has 15 entries (all 14 preserved + new experimental 3.1.0)
        idx = json.loads((tmp / "index.json").read_text(encoding="utf-8"))
        self.assertEqual(len(idx["recipes"]), 15)
        self.assertEqual(
            [e["status"] for e in idx["recipes"] if e["project_id"] == "ghostship"],
            ["experimental", "experimental"],
        )

        ok, errs, _ = validate_recipes.validate_repository(tmp, strict_lf=True)
        self.assertTrue(ok, f"Generated recipe must pass strict validation: {errs}")

    def test_never_auto_updates_validated_recipe_and_blocks_incompatible_zip(self) -> None:
        tmp = self._make_temp_repo()
        # Missing Ghostship.exe and has space in name -> must NOT create recipe
        bad_zip_path, bad_size, bad_sha = self._build_mock_zip(
            ["Ghostship App.exe", "ghostship.o2r"]
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
            if repo == "HarbourMasters/Ghostship":
                return [
                    {
                        "tag_name": "3.2.0",
                        "draft": False,
                        "prerelease": False,
                        "html_url": "https://github.com/HarbourMasters/Ghostship/releases/tag/3.2.0",
                        "assets": [
                            {
                                "name": "Ghostship-Win64.zip",
                                "browser_download_url": "https://github.com/HarbourMasters/Ghostship/releases/download/3.2.0/Ghostship-Win64.zip",
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
            catalog_data=mock_catalog,
            releases_fetcher=mock_releases,
            asset_inspector=mock_inspector,
        )

        self.assertEqual(len(res["updated_recipes"]), 0)
        self.assertEqual(len(res["new_catalog_projects"]), 1)
        self.assertEqual(len(res["pending_reviews"]), 2)
        idx = json.loads((tmp / "index.json").read_text(encoding="utf-8"))
        self.assertEqual(len(idx["recipes"]), 14)

    def test_selects_stable_release_over_prerelease(self) -> None:
        releases = [
            {"tag_name": "v2.0.0-rc1", "draft": False, "prerelease": True},
            {"tag_name": "v1.1.7", "draft": False, "prerelease": False},
        ]
        chosen = upstream_watch.select_latest_release(releases, allow_prerelease=False)
        self.assertIsNotNone(chosen)
        self.assertEqual(chosen["tag_name"], "v1.1.7")

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
