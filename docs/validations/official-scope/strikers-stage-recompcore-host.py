"""Stage the local Windows RecompCore build with its pinned runtime data."""

import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import zipfile

REVISION = "283baee01e54b6c3f71e441bb78fc77b260512fa"
SOURCE = f"https://github.com/aharonahdoot/RecompCore/tree/{REVISION}"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def stage(repo, exe, output):
    def git(*args):
        return subprocess.check_output(["git", "-C", repo, *args])

    if git("rev-parse", "HEAD").decode().strip() != REVISION:
        raise ValueError("Checkout does not match the reviewed RecompCore revision")
    if git("status", "--porcelain", "--untracked-files=no"):
        raise ValueError("The RecompCore source or a tracked submodule has changed")
    # Confirm release identity before copying the known locally built host.
    version = subprocess.run([exe, "--version"], cwd=exe.parent, check=True,
                             capture_output=True, text=True, timeout=12,
                             creationflags=subprocess.CREATE_NO_WINDOW).stdout.strip()
    if not re.search(r"\b283baee\b", version):
        raise ValueError(f"Unexpected built host revision: {version}")
    members = git("archive", "--format=zip", REVISION, "Data/Sys", "COPYING", "LICENSES")
    with zipfile.ZipFile(io.BytesIO(members)) as archive:
        plan = []
        seen = set()
        for info in archive.infolist():
            if info.is_dir():
                continue
            name = PurePosixPath(info.filename)
            if (name.is_absolute() or any(part in (".", "..") or ":" in part or "\\" in part for part in name.parts)
                    or stat.S_ISLNK(info.external_attr >> 16)):
                raise ValueError(f"Unexpected runtime data path: {name}")
            if name.parts[:2] == ("Data", "Sys"):
                relative = PurePosixPath(*name.parts[1:])
            elif name.parts[0] == "LICENSES" or name.as_posix() == "COPYING":
                relative = name
            else:
                raise ValueError(f"Unexpected runtime archive entry: {name}")
            identity = relative.as_posix().casefold()
            if identity in seen:
                raise ValueError(f"Duplicate Windows path: {relative}")
            seen.add(identity)
            plan.append((info, relative))
        if not {"sys/approvedinis.json", "copying"} <= seen:
            raise ValueError("The tracked host data or license is incomplete")
        output.mkdir()
        for info, relative in plan:
            path = output.joinpath(*relative.parts)
            path.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(info) as source, path.open("xb") as target:
                shutil.copyfileobj(source, target)

    host = output / "DolphinNoGUI.exe"
    shutil.copyfile(exe, host)
    manifest = {"source_revision": REVISION, "source": SOURCE, "version": version,
                "scope": "Locally built host, pinned upstream Sys and licenses. No game or module.",
                "files": [{"path": path.relative_to(output).as_posix(),
                           "size": path.stat().st_size, "sha256": sha(path)}
                          for path in sorted(output.rglob("*")) if path.is_file()]}
    (output / "host-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Staged {len(manifest['files'])} files, host SHA-256 {sha(host)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ("repo", "exe", "output"):
        parser.add_argument(key, type=Path)
    args = parser.parse_args()
    stage(args.repo.resolve(strict=True), args.exe.resolve(strict=True), args.output.resolve())
