"""Fetch and unpack the reviewed dependency manifest into a new evidence area.

Only exact SHA-256 matches are accepted. This script does not execute packages.
Archives are retained and sources go into per-package owned directories.
"""
import argparse
import concurrent.futures as cf
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import stat
import tarfile
import time
from urllib.request import Request, urlopen
import zipfile

MAX_ARCHIVE = 48 * 1024 * 1024
MAX_EXPANDED = 192 * 1024 * 1024
MAX_MEMBER = 48 * 1024 * 1024
MAX_ENTRIES = 16000


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def check_relative(name):
    path = PurePosixPath(name)
    if (path.is_absolute() or not path.parts or any(x in ("", ".", "..") for x in path.parts)
            or any("\\" in x or ":" in x or "\0" in x or x.endswith((" ", ".")) for x in path.parts)):
        raise ValueError("unsafe archive path: " + name)
    for part in path.parts:
        if part.split(".")[0].upper() in {"CON", "PRN", "AUX", "NUL", *("COM" + str(x) for x in range(1, 10)), *("LPT" + str(x) for x in range(1, 10))}:
            raise ValueError("reserved archive path: " + name)
    return path


def extract(archive, destination, prefix, exclude_prefixes=()):
    if destination.exists():
        raise ValueError("extraction directory already exists: " + str(destination))
    records = []
    seen = set()
    total = 0
    is_zip = archive.name.endswith(".zip")
    opened = zipfile.ZipFile(archive) if is_zip else tarfile.open(archive, "r:*")
    try:
        members = opened.infolist() if is_zip else opened.getmembers()
        if len(members) > MAX_ENTRIES:
            raise ValueError("archive entry cap")
        for m in members:
            name = m.filename if is_zip else m.name
            size = m.file_size if is_zip else m.size
            directory = m.is_dir() if is_zip else m.isdir()
            if directory and name.rstrip("/") == ".":
                continue
            p = check_relative(name.rstrip("/"))
            parts = p.parts
            if prefix:
                expected = tuple(PurePosixPath(prefix.rstrip("/")).parts)
                if parts[:len(expected)] != expected:
                    raise ValueError("unexpected archive root: " + name)
                parts = parts[len(expected):]
            if not parts:
                if not directory:
                    raise ValueError("file equals archive root")
                continue
            relative = "/".join(parts)
            if any(relative == x.rstrip("/") or relative.startswith(x.rstrip("/") + "/") for x in exclude_prefixes):
                continue
            if is_zip:
                mode = m.external_attr >> 16
                if mode and stat.S_IFMT(mode) not in (0, stat.S_IFREG, stat.S_IFDIR):
                    raise ValueError("archive link/special refused: " + name)
            elif not (m.isfile() or m.isdir()):
                raise ValueError("archive link/special refused: " + name)
            key = "/".join(parts).casefold()
            if key in seen:
                raise ValueError("duplicate archive path: " + name)
            seen.add(key)
            if size > MAX_MEMBER:
                raise ValueError("archive member cap")
            total += 0 if directory else size
            if total > MAX_EXPANDED:
                raise ValueError("expanded archive cap")
            records.append((m, parts, directory, size))
        destination.mkdir(parents=True)
        count = 0
        for member, parts, directory, size in records:
            path = destination.joinpath(*parts)
            if directory:
                path.mkdir(parents=True, exist_ok=True)
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            source = opened.open(member) if is_zip else opened.extractfile(member)
            with source, path.open("xb") as output:
                shutil.copyfileobj(source, output, 256 * 1024)
            if path.stat().st_size != size:
                raise ValueError("extracted length mismatch")
            count += 1
        return count, total
    finally:
        opened.close()


def prepare(item, work, cache):
    if len(item.get("sha256", "")) != 64:
        raise ValueError("dependency has no reviewed SHA-256: " + item["name"])
    archive = work / "archives" / item["file"]
    archive.parent.mkdir(exist_ok=True)
    if not archive.exists():
        found = None
        for alias in [item["file"], *item.get("cache_names", [])]:
            candidate = cache / alias if cache else None
            if candidate and candidate.is_file() and digest(candidate) == item["sha256"]:
                found = candidate
                break
        if found:
            shutil.copyfile(found, archive)
        else:
            temporary = archive.with_name(archive.name + ".partial")
            if temporary.exists():
                raise ValueError("partial archive already exists")
            with urlopen(Request(item["url"], headers={"User-Agent": "GetAll-pinned-native-dependency/1.0"}), timeout=40) as response, temporary.open("xb") as output:
                if int(response.headers.get("Content-Length", "0")) > MAX_ARCHIVE:
                    raise ValueError("compressed archive cap")
                size = 0
                while chunk := response.read(256 * 1024):
                    size += len(chunk)
                    if size > MAX_ARCHIVE:
                        raise ValueError("compressed archive cap")
                    output.write(chunk)
            if digest(temporary) != item["sha256"]:
                raise ValueError("download digest mismatch: " + item["name"])
            temporary.rename(archive)
    if digest(archive) != item["sha256"] or (item.get("bytes") and archive.stat().st_size != item["bytes"]):
        raise ValueError("dependency identity mismatch: " + item["name"])
    destination = work / "dependencies" / item["name"]
    receipt = work / "dependency-results" / (item["name"] + ".json")
    if receipt.exists():
        prior = json.loads(receipt.read_text())
        if prior["archive_sha256"] != item["sha256"]:
            raise ValueError("dependency receipt mismatch")
        return prior
    try:
        count, total = extract(archive, destination, item.get("prefix", ""), item.get("exclude_prefixes", []))
    except Exception as error:
        raise ValueError("dependency " + item["name"] + ": " + str(error)) from error
    result = {**item, "archive": str(archive), "archive_bytes": archive.stat().st_size, "archive_sha256": digest(archive), "source": str(destination), "files": count, "expanded_bytes": total}
    receipt.parent.mkdir(exist_ok=True)
    receipt.write_text(json.dumps(result, indent=2) + "\n", encoding="utf8")
    print(json.dumps({"name": item["name"], "files": count, "archive_bytes": archive.stat().st_size}), flush=True)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("work", type=Path)
    parser.add_argument("--cache", type=Path)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    rows = json.loads(args.manifest.read_text(encoding="utf8"))
    start = time.monotonic()
    with cf.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(lambda x: prepare(x, args.work, args.cache), rows))
    (args.work / "dependency-results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf8")
    print(json.dumps({"status": "DEPENDENCIES_VERIFIED", "packages": len(results), "seconds": round(time.monotonic() - start, 3)}), flush=True)
