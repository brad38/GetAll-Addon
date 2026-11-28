"""Exercise only public interfaces and --help of the verified native build.

All fixture data and environment directories belong to a new evidence output.
This never selects commercial game media or requests a graphics adapter/device.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import time


CRT = {
    "msvcp140.dll": (557728, "0f885b509a685d2bbfa652fed26b5fb31d88fbdab0a978c641d1c7b8aa460aa9"),
    "msvcp140_atomic_wait.dll": (50304, "640b2aefced484d0368eea5bdd06addd0658a3a70a49256e560d6923b404a479"),
    "vcruntime140.dll": (124544, "d5e4d9a3e835fa679450145d6a7d94e36573a509317111904d9b3712c30d9066"),
    "vcruntime140_1.dll": (49792, "1f2d41c4aa5db0bc33ebf7b66d72943a817d7ce6cbe880502a9403823633093f"),
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def private_environment(root):
    system = Path(os.environ.get("SystemRoot", "C:/Windows"))
    for name in ("home", "roaming", "local", "temp"):
        (root / name).mkdir(parents=True)
    return {
        "SystemRoot": str(system), "WINDIR": str(system), "SystemDrive": system.drive,
        "COMSPEC": str(system / "System32/cmd.exe"), "PATHEXT": ".COM;.EXE;.BAT;.CMD",
        "PATH": os.pathsep.join(map(str, (system / "System32", system))),
        "USERPROFILE": str(root / "home"), "HOME": str(root / "home"),
        "APPDATA": str(root / "roaming"), "LOCALAPPDATA": str(root / "local"),
        "TEMP": str(root / "temp"), "TMP": str(root / "temp"),
        "PROCESSOR_ARCHITECTURE": "AMD64", "NUMBER_OF_PROCESSORS": "2",
    }


def run(argv, cwd, env, output, name, results, timeout=120):
    log = output / (name + ".log")
    start = time.monotonic()
    with log.open("wb") as handle:
        process = subprocess.run(list(map(str, argv)), cwd=cwd, env=env,
                                 stdout=handle, stderr=subprocess.STDOUT, timeout=timeout)
    row = {"step": name, "argv": list(map(str, argv)), "cwd": str(cwd),
           "exit": process.returncode, "seconds": round(time.monotonic() - start, 3),
           "log": str(log), "log_sha256": digest(log)}
    results.append(row)
    (output / "runtime-results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf8")
    print(json.dumps(row), flush=True)
    if process.returncode:
        raise RuntimeError(name + " failed: " + str(process.returncode))
    return log.read_text(encoding="utf8", errors="replace")


def pe_imports(path):
    data = path.read_bytes()
    if len(data) < 256 or data[:2] != b"MZ":
        raise ValueError("not a PE: " + str(path))
    pe = struct.unpack_from("<I", data, 0x3c)[0]
    if pe + 264 > len(data) or data[pe:pe+4] != b"PE\0\0":
        raise ValueError("invalid PE header")
    machine, section_count = struct.unpack_from("<HH", data, pe + 4)
    optional_size, characteristics = struct.unpack_from("<HH", data, pe + 20)
    optional = pe + 24
    if machine != 0x8664 or struct.unpack_from("<H", data, optional)[0] != 0x20b or optional_size < 240:
        raise ValueError("not AMD64 PE32+")
    if bool(characteristics & 0x2000) != (path.suffix.lower() == ".dll"):
        raise ValueError("PE DLL/executable classification mismatch")
    sections = []
    for i in range(section_count):
        pos = optional + optional_size + i * 40
        virtual_size, virtual_address, raw_size, raw_address = struct.unpack_from("<IIII", data, pos + 8)
        sections.append((virtual_address, raw_size, raw_address))
    def at(rva, length=1):
        for va, size, raw in sections:
            if va <= rva and rva + length <= va + size and raw + rva - va + length <= len(data):
                return raw + rva - va
        raise ValueError("RVA outside file: " + str(rva))
    def name_at(rva):
        pos = at(rva)
        end = data.find(b"\0", pos, min(len(data), pos + 260))
        if end < 0:
            raise ValueError("invalid import name")
        name = data[pos:end].decode("ascii")
        if "/" in name or "\\" in name or ":" in name or not name.lower().endswith(".dll"):
            raise ValueError("unsafe import name")
        return name.lower()
    imports, delay = set(), set()
    rva, length = struct.unpack_from("<II", data, optional + 112 + 8)
    if rva:
        for index in range(256):
            row = struct.unpack_from("<IIIII", data, at(rva + index * 20, 20))
            if not any(row):
                break
            imports.add(name_at(row[3]))
        else:
            raise ValueError("too many import descriptors")
    rva, length = struct.unpack_from("<II", data, optional + 112 + 13 * 8)
    image_base = struct.unpack_from("<Q", data, optional + 24)[0]
    if rva:
        for index in range(256):
            row = struct.unpack_from("<8I", data, at(rva + index * 32, 32))
            if not any(row):
                break
            name_rva = row[1] if row[0] & 1 else row[1] - image_base
            delay.add(name_at(name_rva))
        else:
            raise ValueError("too many delay imports")
    return {"file": path.name, "machine": "AMD64", "dll": bool(characteristics & 0x2000),
            "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
            "imports": sorted(imports), "delay_imports": sorted(delay)}


def copy(source, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() or not source.is_file() or source.is_symlink():
        raise ValueError("unsafe copy source or occupied destination: " + str(destination))
    shutil.copyfile(source, destination)
    if digest(source) != digest(destination):
        raise ValueError("copy hash mismatch")


def preserve_notices(base, work, output):
    root = output / "licenses"
    source = work / "game-src"
    deps = work / "dependencies"
    notice_names = ("LICENSE", "COPYING", "NOTICE", "COPYRIGHT", "OFL")
    for label, directory in [("Metaforce", source)] + [("dependencies/" + p.name, p) for p in deps.iterdir() if p.is_dir()]:
        count = 0
        for path in directory.rglob("*"):
            if not path.is_file() or not any(path.name.upper() == n or path.name.upper().startswith(n + ".") or path.name.upper().startswith(n + "-") for n in notice_names):
                continue
            if path.stat().st_size > 1024 * 1024 or count >= 512:
                raise ValueError("notice limit exceeded")
            copy(path, root / label / path.relative_to(directory))
            count += 1
    # Additional filenames required by the FreeType license selector.
    for name in ("FTL.TXT", "GPLv2.TXT"):
        copy(deps / "Freetype/docs" / name, root / "dependencies/Freetype/docs" / name)
    supplements = json.loads((work.parent / "supplemental-notices.json").read_text(encoding="utf8"))
    if len(supplements) != 4:
        raise ValueError("supplemental notices incomplete")
    (root / "runtime").mkdir(parents=True, exist_ok=True)
    for item in supplements:
        raw = item["text"].encode("utf8")
        if len(raw) != item["bytes"] or hashlib.sha256(raw).hexdigest() != item["sha256"] or Path(item["name"]).name != item["name"]:
            raise ValueError("supplemental notice pin mismatch")
        (root / "runtime" / item["name"]).write_bytes(raw)
    # SQLite includes its public-domain statement in the amalgamated header.
    sqlite = (deps / "sqlite3/sqlite3.h").read_text(encoding="utf8")
    end = sqlite.find("*/")
    if end < 0 or end > 8192 or "blessing" not in sqlite[:end]:
        raise ValueError("SQLite notice anchor mismatch")
    (root / "dependencies/sqlite3").mkdir(parents=True, exist_ok=True)
    (root / "dependencies/sqlite3/header-notice.txt").write_text(sqlite[:end+2] + "\n", encoding="utf8")
    old_notices = base / "strikers-gc-final/preflight-strikers-recomp/portable-check/licenses"
    for name in ("MSVC-en-US.rtf", "MSVC-pt-BR.rtf"):
        copy(old_notices / name, root / name)
    llvm = base / "gta-engine/preflight/llvm/llvm-mingw-20261020-ucrt-x86_64"
    copy(llvm / "LICENSE.TXT", root / "LLVM-MinGW/LLVM.txt")
    mingw_notices = list((llvm / "x86_64-w64-mingw32/share/mingw32").glob("COPYING*"))
    if len(mingw_notices) != 5:
        raise ValueError("MinGW notice inventory mismatch")
    for path in mingw_notices:
        copy(path, root / "LLVM-MinGW/MinGW" / path.name)
    return [{"path": p.relative_to(output).as_posix(), "bytes": p.stat().st_size, "sha256": digest(p)}
            for p in sorted(root.rglob("*")) if p.is_file()]


def finish(base, work, output, env, results, imports):
    # cxxopts hides the named dvd option because it is also the positional
    # argument. Exercise its actual parser with a deliberately absent authored
    # path and --help, which the official main handles before media or GPU.
    text = run([output / "metaforce.exe", "--dvd", output / "authored absent disc.iso",
                "--user-dir", output / "help-only-user", "--help"],
               output, env, output, "metaforce-help-argv", results)
    if "<disc image>" not in text or "--user-dir" not in text or "Usage:" not in text:
        raise ValueError("official help contract missing")
    if (output / "authored absent disc.iso").exists() or (output / "help-only-user").exists():
        raise ValueError("help unexpectedly created media or user data")
    print("METAFORCE_OFFICIAL_HELP_PASS", flush=True)
    notices = preserve_notices(base, work, output)
    resources = [{"path": p.relative_to(output).as_posix(), "bytes": p.stat().st_size, "sha256": digest(p)}
                 for p in sorted((output / "res").rglob("*")) if p.is_file()]
    receipt = {"status": "METAFORCE_PUBLIC_NATIVE_RUNTIME_PASS", "source_revision": "de8fc69bd7f345d6cf5f0c8fc2798295e22522d3",
               "output": str(output), "results": results, "runtime": imports, "resources": resources,
               "notices": notices, "media": "Only authored invalid bytes; no commercial disc or game boot.",
               "environment": env}
    (output / "runtime-proof.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf8")
    print(json.dumps({"status": receipt["status"], "runtime_files_including_probe": len(imports),
                      "resource_files": len(resources), "notice_files": len(notices),
                      "receipt_sha256": digest(output / "runtime-proof.json")}), flush=True)


def finish_existing(base, work, output):
    if output.parent != work or not output.is_dir():
        raise ValueError("unexpected proof output")
    results = json.loads((output / "runtime-results.json").read_text(encoding="utf8"))
    if [r["step"] for r in results] != ["runtime-probe-build", "runtime-interfaces", "metaforce-help"]:
        raise ValueError("unexpected prior proof steps")
    for row in results:
        if row["exit"] != 0 or digest(Path(row["log"])) != row["log_sha256"]:
            raise ValueError("prior successful proof log changed")
    if "METAFORCE_RUNTIME_INTERFACES_PASS" not in Path(results[1]["log"]).read_text(encoding="utf8"):
        raise ValueError("runtime interface proof is not complete")
    closure = json.loads((output / "pe-import-closure.json").read_text(encoding="utf8"))
    actual = [pe_imports(p) for p in sorted(output.iterdir()) if p.suffix.lower() in (".dll", ".exe")]
    if closure["missing"] or actual != closure["files"]:
        raise ValueError("verified native artifacts changed")
    env = private_environment(output / "finish-private-user")
    finish(base, work, output, env, results, actual)


def prove(base, work, output):
    if output.exists() or output.parent != work or not (work / "build/metaforce.exe").is_file():
        raise ValueError("proof needs a native executable and a new direct-child output")
    output.mkdir()
    env = private_environment(output / "private-user")
    results = []
    deps = work / "deps-build"
    copy(work / "build/metaforce.exe", output / "metaforce.exe")
    for name in ("webgpu_dawn.dll", "dxcompiler.dll", "dxil.dll"):
        copy(deps / "dawn_prebuilt/bin" / name, output / name)
    copy(deps / "nod_prebuilt/bin/nod.dll", output / "nod.dll")
    copy(deps / "sdl3_prebuilt/x86_64-w64-mingw32/bin/SDL3.dll", output / "SDL3.dll")
    for name, (length, expected) in CRT.items():
        original = base / "strikers-gc-final/preflight-strikers-recomp/portable-check" / name
        if original.stat().st_size != length or digest(original) != expected:
            raise ValueError("private CRT pin mismatch: " + name)
        copy(original, output / name)
    for path in (work / "game-src/res").rglob("*"):
        if path.is_file():
            copy(path, output / "res" / path.relative_to(work / "game-src/res"))
    llvm = base / "gta-engine/preflight/llvm/llvm-mingw-20261020-ucrt-x86_64/bin"
    source = work.parent / "metaforce_runtime_probe.cpp"
    args = [llvm / "clang++.exe", "-std=c++20", "-O2", "-static", "-DWEBGPU_DAWN",
            "-I", deps / "dawn_prebuilt/include", "-I", deps / "nod_prebuilt/include",
            "-I", deps / "sdl3_prebuilt/x86_64-w64-mingw32/include",
            "-I", work / "game-src/extern/borealis/include", "-I", work / "build/extern/borealis/generated",
            source, work / "build/extern/borealis/libborealis_io.a",
            deps / "dawn_prebuilt/lib/webgpu_dawn.lib", deps / "nod_prebuilt/lib/nod.lib",
            deps / "sdl3_prebuilt/x86_64-w64-mingw32/lib/libSDL3.dll.a",
            "-o", output / "metaforce-runtime-probe.exe"]
    run(args, output, env, output, "runtime-probe-build", results)
    imports = [pe_imports(p) for p in sorted(output.iterdir()) if p.suffix.lower() in (".dll", ".exe")]
    names = {p.name.lower() for p in output.iterdir() if p.is_file()}
    system = Path(env["SystemRoot"]) / "System32"
    missing = sorted({name for row in imports for name in row["imports"] + row["delay_imports"]
                      if name not in names and not name.startswith(("api-ms-", "ext-ms-")) and not (system / name).is_file()})
    (output / "pe-import-closure.json").write_text(json.dumps({"files": imports, "missing": missing}, indent=2) + "\n", encoding="utf8")
    if missing:
        raise ValueError("missing private runtime dependencies: " + ", ".join(missing))
    text = run([output / "metaforce-runtime-probe.exe"], output, env, output, "runtime-interfaces", results)
    for marker in ("NOD_AUTHORED_INVALID_FORMAT_PASS:", "DAWN_SDL_NOD_LOCAL_C_ABI_PASS",
                   "BOREALIS_ATOMIC_UNICODE_REPLACE_AND_FAILURE_PASS", "METAFORCE_RUNTIME_INTERFACES_PASS"):
        if marker not in text:
            raise ValueError("runtime marker missing: " + marker)
    text = run([output / "metaforce.exe", "--help"], output, env, output, "metaforce-help", results)
    if "<disc image>" not in text or "--user-dir" not in text:
        raise ValueError("official help contract missing")
    finish(base, work, output, env, results, imports)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("base", type=Path)
    parser.add_argument("work", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--finish-only", action="store_true")
    args = parser.parse_args()
    if args.finish_only:
        finish_existing(args.base, args.work, args.output)
    else:
        prove(args.base, args.work, args.output)
