"""Assemble the SDK 1.5.68 preview from the already audited Desktop candidate.

Only copies the fixed candidate and packages the published immutable GetAll
revision. It does not rebuild, launch AllFix, install an addon, or contact GitHub.
Run with Python 3.12 on Bradsson; the remote-pins receipt records the API check.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

DESKTOP = "8ba34eb51ee0ab93accef3da5e1689c68825977d"
GETALL = "5b7fea8fb8d2b77df5a6cfd7e9efb6b463fba75b"
CATALOG = "3f4603cf42ef43402b4a0a9470232e7d4fcd9eb9"
CANDIDATE = "8f9bbab4ab16b60b65d5e05ecc7cb2f823eff0670b80c478bed482afc3e279d8"
EXECUTABLE = "3ce6d4ec0e182a450fa621cc8f7a2288250e1485d6be539513f9b8a705a099da"
INDEX = "c82d450f0da6e067c80cc01141b677c950b43fbeac5c9303aededac266bcdee3"
PACKAGER = "2ffc3cd1bd322a7410253b3283d27816adccf4d6bc4f846011621a1b99df6b04"
OLD_MANIFEST = "0f2db05e027d27732451a4d1f29fffb0fb7b868f82c1c9fd23c00c9b329c8e96"
RECEIPTS = {"ARTIFACT-MANIFEST.json", "SHA256SUMS.txt"}
SDK = "1.5.68"
VERSION = "1.5.73"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path, value):
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def confined(root, relative):
    item = PurePosixPath(relative)
    require(relative and not item.is_absolute() and "\\" not in relative and
            all(p not in (".", "..") and ":" not in p for p in item.parts),
            "Unsafe candidate path: " + relative)
    path = root
    for part in (None, *item.parts):
        if part is not None:
            path /= part
        if path.exists() or path.is_symlink():
            info = path.lstat()
            require(not stat.S_ISLNK(info.st_mode) and
                    not getattr(info, "st_file_attributes", 0) & 1024,
                    "Linked path is not accepted: " + str(path))
    return path


def inventory(root):
    values = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        confined(root, relative)
        if path.is_file() and relative not in RECEIPTS:
            values.append({"name": relative, "bytes": path.stat().st_size,
                           "sha256": digest(path)})
    return values


def verify_zip(path):
    with zipfile.ZipFile(path) as archive:
        require(archive.namelist() == ["addon.json", "responses.json"], "Unexpected addon files")
        require(all(x.file_size < 65536 and not x.flag_bits & 1 for x in archive.infolist()),
                "Unexpected addon archive")
        manifest = json.loads(archive.read("addon.json"))
        responses = json.loads(archive.read("responses.json"))
    require(manifest == {"manifest_version": 1, "id": "allfix.install.universal.preview",
            "name": "GetAll de desenvolvimento", "version": VERSION, "api_version": "1.0",
            "entrypoint": "responses.json", "capabilities": ["installation.recipe.remote"],
            "permissions": [], "priority": 0, "min_sdk_version": SDK}, "Addon identity differs")
    require(responses == {"responses": [{"capability": "installation.recipe.remote", "match": {},
            "result": {"repository": "brad38/GetAll-Addon", "ref": GETALL,
                       "index_path": "index.json", "catalog_ref": CATALOG}}]},
            "Addon remote pins differ")


def verify_final(output):
    manifest = read_json(output / "ARTIFACT-MANIFEST.json")
    require((manifest["desktop_commit"], manifest["getall_commit"], manifest["sdk_version"],
             manifest["preview_version"], manifest["catalog_commit"]) ==
            (DESKTOP, GETALL, SDK, VERSION, CATALOG), "Preview identity differs")
    require(inventory(output) == manifest["artifacts"], "Preview files changed")
    verify_zip(output / "GetAll-Preview.zip")
    sums = [(x["name"], x["sha256"]) for x in manifest["artifacts"]]
    sums.append(("ARTIFACT-MANIFEST.json", digest(output / "ARTIFACT-MANIFEST.json")))
    expected = "".join(f"{value}  {name}\n" for name, value in sorted(sums))
    require((output / "SHA256SUMS.txt").read_text(encoding="utf-8") == expected,
            "Preview checksum manifest differs")
    return manifest


def assemble(args):
    root = args.task_root.absolute()
    source = root / "publish-desktop-final-sdk168-20261127"
    output = root / "publish-getall-sdk168-20261127"
    checkout = root / "getall-sdk168-final-20261127"
    evidence = args.evidence.absolute()
    require(not output.exists(), "The final preview already exists; use verify")
    require(evidence.is_dir(), "Evidence directory must already exist")
    for path in (source, checkout, evidence):
        confined(path, ".probe")
    remote = read_json(evidence / "remote-pins.json")
    for repository, commit, run in (("brad38/Allfix", DESKTOP, 46059165665),
                                   ("brad38/GetAll-Addon", GETALL, 46059162398)):
        entries = [x for x in remote["repositories"] if x["repository"] == repository]
        require(len(entries) == 1, "Missing unique remote verification")
        entry = entries[0]
        require(entry["commit"] == commit and entry["branch"] ==
                "work/complete-install-flows-20261127" and entry["draft"] and not entry["merged"],
                "Published commit receipt differs")
        require(any(x["id"] == run and x["status"] == "completed" and x["conclusion"] == "success"
                    for x in entry["workflow_runs"]), "CI success receipt differs")
    git = args.git
    def git_value(*arguments):
        return subprocess.check_output([git, "-C", str(checkout), *arguments],
                                       encoding="utf-8").strip()
    require(git_value("rev-parse", "HEAD") == GETALL and
            not git_value("status", "--porcelain", "--untracked-files=all"),
            "GetAll checkpoint must be clean and fixed")
    require(digest(checkout / "index.json") == INDEX, "Recipe index differs")
    require(digest(checkout / "scripts/package_preview.py") == PACKAGER, "Packager differs")
    require(digest(source / "ARTIFACT-MANIFEST.json") == CANDIDATE, "Candidate manifest differs")
    candidate = read_json(source / "ARTIFACT-MANIFEST.json")
    require(candidate["desktop_commit"] == DESKTOP and candidate["sdk_version"] == SDK and
            candidate["desktop_version"] == "3.0.0" and not candidate["addon_included"],
            "Desktop candidate identity differs")
    require(inventory(source) == candidate["artifacts"] and len(candidate["artifacts"]) == 73,
            "Desktop candidate file inventory differs")
    require(digest(source / "AllFix.exe") == EXECUTABLE, "Desktop executable differs")
    require((candidate["native_resources_verified"], candidate["notices_verified"],
             candidate["native_properties_verified"]) == (34, 66, 12), "Candidate audit differs")
    old_manifest = root / "publish-getall-complete-flows-20261127/ARTIFACT-MANIFEST.json"
    require(digest(old_manifest) == OLD_MANIFEST, "Previous preview manifest differs")
    old = read_json(old_manifest)
    require(old["catalog_commit"] == CATALOG, "Catalog checkpoint differs")
    needed = sum(x["bytes"] for x in candidate["artifacts"])
    require(shutil.disk_usage(root).free > needed + 256 * 1024**2, "Insufficient staging space")
    stage = Path(tempfile.mkdtemp(prefix="preview-sdk168-staging-", dir=root))
    try:
        for item in candidate["artifacts"]:
            source_file = confined(source, item["name"])
            target = confined(stage, item["name"])
            target.parent.mkdir(parents=True, exist_ok=True)
            with source_file.open("rb") as src, target.open("xb") as dst:
                shutil.copyfileobj(src, dst, length=1024*1024)
        env = dict(os.environ)
        env["PATH"] = str(Path(git).parent) + os.pathsep + env.get("PATH", "")
        command = [sys.executable, str(checkout / "scripts/package_preview.py"), GETALL, CATALOG,
                   VERSION, str(stage / "GetAll-Preview.zip"), "--min-sdk", SDK]
        completed = subprocess.run(command, capture_output=True, text=True, env=env)
        with (evidence / "package-preview.log").open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(completed.stdout + completed.stderr)
            stream.write(f"\nexit_code={completed.returncode}\n")
        require(completed.returncode == 0, "Package command failed; read package-preview.log")
        verify_zip(stage / "GetAll-Preview.zip")
        manifest = {"format": 1, "artifact_type": "desktop-getall-preview",
            "created_utc": datetime.now(timezone.utc).isoformat(), "desktop_commit": DESKTOP,
            "desktop_version": "3.0.0", "sdk_version": SDK, "getall_commit": GETALL,
            "preview_version": VERSION, "catalog_commit": CATALOG,
            "catalog_sha256": old["catalog_sha256"], "recipe_index_sha256": INDEX,
            "native_resources_verified": 34, "notices_verified": 66, "native_properties_verified": 12,
            "source_candidate_manifest_sha256": CANDIDATE,
            "remote_verification_sha256": digest(evidence / "remote-pins.json"),
            "desktop_recompiled": False, "addon_included": True,
            "integral_projects_implemented": 140, "catalog_projects": 148,
            "new_commercial_boot_verified": False, "resource_groups": candidate["resource_groups"],
            "artifacts": inventory(stage)}
        write_json(stage / "ARTIFACT-MANIFEST.json", manifest)
        values = [(x["name"], x["sha256"]) for x in manifest["artifacts"]]
        values.append(("ARTIFACT-MANIFEST.json", digest(stage / "ARTIFACT-MANIFEST.json")))
        with (stage / "SHA256SUMS.txt").open("x", encoding="utf-8", newline="\n") as stream:
            stream.writelines(f"{value}  {name}\n" for name, value in sorted(values))
        verify_final(stage)
        stage.rename(output)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    final = verify_final(output)
    require(digest(source / "ARTIFACT-MANIFEST.json") == CANDIDATE and
            digest(old_manifest) == OLD_MANIFEST, "Source preview receipts changed")
    result = {"status": "PASS", "output": str(output), "desktop_commit": DESKTOP,
              "getall_commit": GETALL, "sdk_version": SDK, "addon_version": VERSION,
              "files": len(final["artifacts"]), "copied_desktop_bytes": needed,
              "executable_sha256": digest(output / "AllFix.exe"),
              "addon_sha256": digest(output / "GetAll-Preview.zip"),
              "manifest_sha256": digest(output / "ARTIFACT-MANIFEST.json"),
              "script_sha256": digest(Path(__file__)),
              "completed_utc": datetime.now(timezone.utc).isoformat(),
              "storage": "Task-owned staging removed; source candidate and previous preview preserved."}
    write_json(evidence / "preview-result.json", result)
    print(json.dumps(result, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["assemble", "verify"])
    parser.add_argument("--task-root", type=Path, required=True)
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--git", default=r"C:\Program Files\Git\cmd\git.exe")
    args = parser.parse_args()
    if args.mode == "assemble":
        assemble(args)
    else:
        manifest = verify_final(args.task_root / "publish-getall-sdk168-20261127")
        print(f"PREVIEW_VERIFIED files={len(manifest['artifacts'])} sdk={SDK} addon={VERSION}")


if __name__ == "__main__":
    main()
