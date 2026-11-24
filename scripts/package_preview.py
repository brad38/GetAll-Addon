"""Build the opt-in GetAll preview addon for a published immutable recipe commit."""

import argparse
import json
from pathlib import Path
import re
import subprocess
import zipfile


COMMIT = re.compile(r"[0-9a-fA-F]{40}")
VERSION = re.compile(r"[0-9]{1,8}\.[0-9]{1,8}\.[0-9]{1,8}")
REPOSITORY = "brad38/GetAll-Addon"
PREVIEW_ID = "allfix.install.universal.preview"
CAPABILITY = "installation.recipe.remote"


def package(root: Path, revision: str, catalog: str, version: str, output: Path) -> None:
    if not COMMIT.fullmatch(revision) or not COMMIT.fullmatch(catalog):
        raise ValueError("Use os SHAs completos dos commits do GetAll e AllFix-Repo.")
    if not VERSION.fullmatch(version):
        raise ValueError("A versão do addon precisa usar o formato x.y.z.")
    index = json.loads(subprocess.check_output(
        ["git", "-C", str(root), "show", revision + ":index.json"]
    ))
    if index.get("channel") != "preview" or index.get("index_format_version") != 1:
        raise ValueError("O commit precisa conter um índice GetAll de desenvolvimento.")

    manifest = {
        "manifest_version": 1, "id": PREVIEW_ID, "name": "GetAll de desenvolvimento",
        "version": version, "api_version": "1.0", "entrypoint": "responses.json",
        "capabilities": [CAPABILITY], "permissions": [], "priority": 0,
        "min_sdk_version": "1.5.11",
    }
    responses = {"responses": [{"capability": CAPABILITY, "match": {}, "result": {
        "repository": REPOSITORY, "ref": revision.lower(), "index_path": "index.json",
        "catalog_ref": catalog.lower(),
    }}]}
    with zipfile.ZipFile(output, "x") as archive:
        for name, document in (("addon.json", manifest), ("responses.json", responses)):
            archive.writestr(zipfile.ZipInfo(name), json.dumps(document, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("revision")
    parser.add_argument("catalog")
    parser.add_argument("version")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    package(Path(__file__).resolve().parents[1], args.revision, args.catalog, args.version, args.output)
