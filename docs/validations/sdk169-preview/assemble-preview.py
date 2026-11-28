"""Assemble the SDK 1.5.69 preview from the already audited Desktop candidate.

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

DESKTOP = None  # Required immutable pin supplied on the command line.
GETALL = None  # Required immutable pin supplied on the command line.
CATALOG = "3f4603cf42ef43402b4a0a9470232e7d4fcd9eb9"
CANDIDATE = None  # Required immutable pin supplied on the command line.
EXECUTABLE = None  # Required immutable pin supplied on the command line.
INDEX = "2e3ee9a442015c492c84cc28f92f7da75dfffdbbe817d42dc0f3b311cbfac9eb"
PACKAGER = "2ffc3cd1bd322a7410253b3283d27816adccf4d6bc4f846011621a1b99df6b04"
SDK168_MANIFEST = "0220e843125b9223435d671fcbb834df1d13ce653fb770e6599989f7efd1c95a"
OLD_MANIFEST = "0f2db05e027d27732451a4d1f29fffb0fb7b868f82c1c9fd23c00c9b329c8e96"
RECEIPTS = {"ARTIFACT-MANIFEST.json", "SHA256SUMS.txt"}
SDK = "1.5.69"
VERSION = "1.5.74"


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
    require(manifest["source_candidate_manifest_sha256"] == CANDIDATE,
            "Preview candidate pin differs")
    require(digest(output / "AllFix.exe") == EXECUTABLE, "Preview executable pin differs")
    require((len(manifest["artifacts"]), manifest["native_resources_verified"],
             manifest["notices_verified"], manifest["native_properties_verified"]) ==
            (79, 35, 71, 12), "Preview artifact/audit counts differ")
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
    source = root / "publish-desktop-final-sdk169-20261127"
    output = root / "publish-getall-sdk169-20261127"
    checkout = root / "getall-sdk169-final-20261127"
    evidence = args.evidence.absolute()
    require(not output.exists(), "The final preview already exists; use verify")
    require(evidence.is_dir(), "Evidence directory must already exist")
    for path in (source, checkout, evidence):
        confined(path, ".probe")
    remote = read_json(evidence / "remote-pins.json")
    for repository, commit, workflow in (("brad38/Allfix", DESKTOP, "Windows SDK and Desktop CI"),
                                        ("brad38/GetAll-Addon", GETALL, "Validate GetAll-Addon Recipes")):
        entries = [x for x in remote["repositories"] if x["repository"] == repository]
        require(len(entries) == 1, "Missing unique remote verification")
        entry = entries[0]
        require(entry["commit"] == commit and entry["branch"] ==
                "work/complete-install-flows-20261127" and entry["draft"] and not entry["merged"],
                "Published commit receipt differs")
        require(any(x["name"] == workflow and x["status"] == "completed" and x["conclusion"] == "success"
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
    require(inventory(source) == candidate["artifacts"] and len(candidate["artifacts"]) == 78,
            "Desktop candidate file inventory differs")
    require(digest(source / "AllFix.exe") == EXECUTABLE, "Desktop executable differs")
    require((candidate["native_resources_verified"], candidate["notices_verified"],
             candidate["native_properties_verified"]) == (35, 71, 12), "Candidate audit differs")
    old_manifest = root / "publish-getall-complete-flows-20261127/ARTIFACT-MANIFEST.json"
    require(digest(old_manifest) == OLD_MANIFEST, "Previous preview manifest differs")
    previous_manifest = root / "publish-getall-sdk168-20261127/ARTIFACT-MANIFEST.json"
    require(digest(previous_manifest) == SDK168_MANIFEST, "SDK168 preview manifest differs")
    old = read_json(old_manifest)
    require(old["catalog_commit"] == CATALOG, "Catalog checkpoint differs")
    needed = sum(x["bytes"] for x in candidate["artifacts"])
    require(shutil.disk_usage(root).free > needed + 256 * 1024**2, "Insufficient staging space")
    stage = Path(tempfile.mkdtemp(prefix="preview-sdk169-staging-", dir=root))
    try:
        for item in candidate["artifacts"]:
            source_file = confined(source, item["name"])
            target = confined(stage, item["name"])
            target.parent.mkdir(parents=True, exist_ok=True)
            with source_file.open("rb") as src, target.open("xb") as dst:
                shutil.copyfileobj(src, dst, length=1024*1024)
        require(inventory(stage) == candidate["artifacts"], "Copied candidate files differ")
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
            "native_resources_verified": 35, "notices_verified": 71, "native_properties_verified": 12,
            "source_candidate_manifest_sha256": CANDIDATE,
            "remote_verification_sha256": digest(evidence / "remote-pins.json"),
            "desktop_recompiled": False, "addon_included": True,
            "integral_projects_implemented": 142, "catalog_projects": 148,
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
            digest(old_manifest) == OLD_MANIFEST and digest(previous_manifest) == SDK168_MANIFEST,
            "Source preview receipts changed")
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
    global DESKTOP, GETALL, CANDIDATE, EXECUTABLE
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["assemble", "verify"])
    parser.add_argument("--task-root", type=Path, required=True)
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--git", default=r"C:\Program Files\Git\cmd\git.exe")
    parser.add_argument("--desktop-commit", required=True)
    parser.add_argument("--getall-commit", required=True)
    parser.add_argument("--candidate-manifest-sha256", required=True)
    parser.add_argument("--executable-sha256", required=True)
    args = parser.parse_args()
    DESKTOP, GETALL = args.desktop_commit, args.getall_commit
    CANDIDATE, EXECUTABLE = args.candidate_manifest_sha256, args.executable_sha256
    for value, length in ((DESKTOP, 40), (GETALL, 40), (CANDIDATE, 64), (EXECUTABLE, 64)):
        require(len(value) == length and all(c in "0123456789abcdef" for c in value), "Invalid immutable pin")
    if args.mode == "assemble":
        assemble(args)
    else:
        manifest = verify_final(args.task_root / "publish-getall-sdk169-20261127")
        print(f"PREVIEW_VERIFIED files={len(manifest['artifacts'])} sdk={SDK} addon={VERSION}")


if __name__ == "__main__":
    main()
