import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts.validate_ci import PREVIEW_CATALOG, PUBLIC_CATALOG, run_validation, select_catalog


class CiValidationTests(unittest.TestCase):
    def test_preview_uses_pinned_catalog_for_development_events(self):
        contexts = [
            {"GITHUB_EVENT_NAME": "push", "GITHUB_REF": "refs/heads/feat/marathon-xbox-media-import"},
            {"GITHUB_EVENT_NAME": "pull_request", "GITHUB_REF": "refs/pull/42/merge",
             "GITHUB_BASE_REF": "feat/marathon-xbox-media-import",
             "GITHUB_HEAD_REF": "work/continuar-getall-20261127"},
            {"GITHUB_EVENT_NAME": "workflow_dispatch", "GITHUB_REF": "refs/heads/work/new-preview"},
        ]
        for context in contexts:
            with self.subTest(context=context):
                self.assertEqual(select_catalog({"channel": "preview"}, context), PREVIEW_CATALOG)

    def test_preview_is_rejected_for_main_without_source_exceptions(self):
        contexts = [
            {"GITHUB_EVENT_NAME": "push", "GITHUB_REF": "refs/heads/main"},
            {"GITHUB_EVENT_NAME": "workflow_dispatch", "GITHUB_REF": "refs/heads/main"},
        ]
        for event in ("pull_request", "pull_request_target"):
            for source in ("feat/round-17-restricted-installers", "work/new-preview"):
                contexts.append({"GITHUB_EVENT_NAME": event, "GITHUB_REF": "refs/pull/42/merge",
                                 "GITHUB_BASE_REF": "main", "GITHUB_HEAD_REF": source})
        for context in contexts:
            with self.subTest(context=context):
                with self.assertRaisesRegex(ValueError, "must not be served as production"):
                    select_catalog({"channel": "preview"}, context)

    def test_public_and_legacy_indexes_use_public_catalog(self):
        contexts = [
            {"GITHUB_EVENT_NAME": "push", "GITHUB_REF": "refs/heads/main"},
            {"GITHUB_EVENT_NAME": "pull_request", "GITHUB_BASE_REF": "main"},
            {"GITHUB_EVENT_NAME": "workflow_dispatch", "GITHUB_REF": "refs/heads/work/continuation"},
        ]
        for index in ({"channel": "public"}, {}):
            for context in contexts:
                with self.subTest(index=index, context=context):
                    self.assertEqual(select_catalog(index, context), PUBLIC_CATALOG)

    def test_invalid_indexes_do_not_select_a_catalog(self):
        for index in (None, [], {"channel": "unknown"}, {"channel": None}):
            with self.subTest(index=index):
                with self.assertRaises(ValueError):
                    select_catalog(index, {})

    def test_ci_runs_strict_validation_and_propagates_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "index.json").write_text(json.dumps({"channel": "preview"}), encoding="utf-8")
            context = {"GITHUB_EVENT_NAME": "pull_request", "GITHUB_BASE_REF": "feat/marathon-xbox-media-import"}
            with patch("scripts.validate_ci.subprocess.call", return_value=7) as validate:
                self.assertEqual(run_validation(root, context), 7)
            validate.assert_called_once_with(
                [sys.executable, str(root / "scripts" / "validate_recipes.py"),
                 "--strict-lf", "--require-jsonschema", "--check-git-blobs",
                 "--check-catalog", PREVIEW_CATALOG], cwd=root,
            )

    def test_main_gate_stops_before_running_validator(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "index.json").write_text(json.dumps({"channel": "preview"}), encoding="utf-8")
            context = {"GITHUB_EVENT_NAME": "pull_request", "GITHUB_BASE_REF": "main",
                       "GITHUB_HEAD_REF": "feat/round-17-restricted-installers"}
            with patch("scripts.validate_ci.subprocess.call") as validate:
                with self.assertRaisesRegex(ValueError, "must not be served as production"):
                    run_validation(root, context)
            validate.assert_not_called()


if __name__ == "__main__":
    unittest.main()
