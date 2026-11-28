import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from jsonschema import Draft202012Validator

from scripts.package_preview import package


class PreviewPackageTests(unittest.TestCase):
    def test_package_pins_both_repositories(self):
        revision, catalog = "a" * 40, "b" * 40
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first, second = root / "first.zip", root / "second.zip"
            with patch("scripts.package_preview.subprocess.check_output", return_value=b'{"index_format_version":1,"channel":"preview"}'):
                package(root, revision, catalog, "1.1.0", first)
                package(root, revision, catalog, "1.1.0", second)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            with zipfile.ZipFile(first) as archive:
                self.assertEqual(archive.namelist(), ["addon.json", "responses.json"])
                manifest = json.loads(archive.read("addon.json"))
                schema_path = Path(__file__).resolve().parents[1] / "schemas" / "addon-manifest-v1.schema.json"
                Draft202012Validator(json.loads(schema_path.read_text(encoding="utf-8"))).validate(manifest)
                self.assertEqual(manifest["id"], "allfix.install.universal.preview")
                self.assertEqual(manifest["min_sdk_version"], "1.5.11")
                origin = json.loads(archive.read("responses.json"))["responses"][0]["result"]
                self.assertEqual((origin["ref"], origin["catalog_ref"]), (revision, catalog))

    def test_rejects_mutable_refs_and_public_index(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            output = root / "out.zip"
            with self.assertRaisesRegex(ValueError, "SHAs completos"):
                package(root, "main", "b" * 40, "1.1.0", output)
            with patch("scripts.package_preview.subprocess.check_output", return_value=b'{"index_format_version":1}'):
                with self.assertRaisesRegex(ValueError, "desenvolvimento"):
                    package(root, "a" * 40, "b" * 40, "1.1.0", output)
            self.assertFalse(output.exists())

    def test_official_scope_package_requires_sdk_with_fidelity_gates(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            output=root/"official.zip"
            index=b'{"index_format_version":1,"channel":"preview","execution_policy":"official_upstream_only"}'
            with patch("scripts.package_preview.subprocess.check_output",return_value=index):
                for minimum in ("1.5.11","1.5.69","1.4.99"):
                    with self.subTest(minimum=minimum):
                        with self.assertRaisesRegex(ValueError,"1.5.70"):
                            package(root,"a"*40,"b"*40,"1.5.75",output,minimum)
                        self.assertFalse(output.exists())
                package(root,"a"*40,"b"*40,"1.5.75",output,"1.5.70")
            with zipfile.ZipFile(output) as archive:
                self.assertEqual(json.loads(archive.read("addon.json"))["min_sdk_version"],"1.5.70")

    def test_rejects_noncanonical_versions_before_reading_git_or_creating_zip(self):
        invalid_versions = ("01.1.0", "1.01.0", "1.1.00", "1.2", "1.2.3.4",
                            "1.2.3-beta", "100000000.1.0", "1.2.3\n")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            output = root / "out.zip"
            for invalid in invalid_versions:
                for version, min_sdk in ((invalid, "1.5.11"), ("1.1.0", invalid)):
                    with self.subTest(version=version, min_sdk=min_sdk):
                        with patch("scripts.package_preview.subprocess.check_output") as git:
                            with self.assertRaisesRegex(ValueError, "sem zeros iniciais"):
                                package(root, "a" * 40, "b" * 40, version, output, min_sdk)
                        git.assert_not_called()
                        self.assertFalse(output.exists())

    def test_version_boundaries_generate_schema_valid_manifests(self):
        schema_path = Path(__file__).resolve().parents[1] / "schemas" / "addon-manifest-v1.schema.json"
        validator = Draft202012Validator(json.loads(schema_path.read_text(encoding="utf-8")))
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for version in ("0.0.0", "99999999.99999999.99999999"):
                with self.subTest(version=version):
                    output = root / (version + ".zip")
                    with patch("scripts.package_preview.subprocess.check_output", return_value=b'{"index_format_version":1,"channel":"preview"}'):
                        package(root, "a" * 40, "b" * 40, version, output, version)
                    with zipfile.ZipFile(output) as archive:
                        validator.validate(json.loads(archive.read("addon.json")))
