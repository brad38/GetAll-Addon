import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

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
