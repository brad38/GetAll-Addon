from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
from io import BytesIO
from pathlib import Path
import argparse
import json
import os
import shutil
import struct
import subprocess
from urllib.request import Request, urlopen
from zipfile import ZipFile

parser = argparse.ArgumentParser(description="Test upstream StrikersRecomp source variants with MSVC and authored PPC.")
parser.add_argument("workspace", type=Path, help="GetAll workspace containing the pinned Windows Clang evidence")
parser.add_argument("output", type=Path, help="isolated directory for test-only source, builds and logs")
args = parser.parse_args()
base = args.workspace.resolve(strict=True)
proof = args.output.resolve()
proof.mkdir(parents=True, exist_ok=True)
cache = base / "console-cache"
cmake = Path(shutil.which("cmake"))
ninja = Path(shutil.which("ninja"))
python = Path(shutil.which("python"))
git = Path(shutil.which("git"))
msvc = Path(r"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat")
clang = base / "evidence-r18/mkdd-llvm23/bin/clang.exe"
env = dict(os.environ)
for name in ("CL", "_CL_", "CFLAGS", "CXXFLAGS", "LDFLAGS", "CC", "CXX", "CMAKE_TOOLCHAIN_FILE"):
    env.pop(name, None)
env["PATH"] = os.pathsep.join(map(str, [clang.parent, cmake.parent, ninja.parent, python.parent, git.parent,
    Path(os.environ["WINDIR"]) / "System32", Path(os.environ["WINDIR"])]))
env["VSLANG"] = "1033"
home = proof / "private"
home.mkdir(exist_ok=True)
env.update(TEMP=str(home), TMP=str(home))
input_revisions = {
    "main": ("aharonahdoot/StrikersRecomp", "cd88f71f5a836c103484c038454b4143000d883c", base / "evidence-r18/complete-install-flows-20261127/strikers-gc-cd88f71.zip", "1f361113dbfd35d0b0e6e1c5b98cbdf755cc28334f984cbdd95572a3be189a62"),
    "release": ("aharonahdoot/StrikersRecomp", "67047edb69194a9642e3fbe2ba039db6e8c37c76", None, "1ab542f13472f04383fd464ce495d45f3a3f8346ab5eeaa081ccaf16f69125bc"),
    "runtime_tag": ("aharonahdoot/GXRuntime", "b4c85bba0ce6633a6d977dbb9595b6640784b8ba", None, "5b3f8b4b1a716975b0a353a50d0ab81a337f3d98a637503325ffbcfd80cce7e7"),
    "runtime_head": ("aharonahdoot/GXRuntime", "8a47b0e8ea7dfc39014a4cff4f7895d88494a611", None, "9e52c8873befa17161815a7cecfeef4c146e02d11816dfa36ea1e59d41ff2e0d"),
    "runtime_compatible": ("aharonahdoot/GXRuntime", "f83d25877c7b701468c978c09559d513c4971ddd", cache / "gxruntime-f83d258.zip", "b548b5b6a630fb7f49efb1c8fbaf8cc3fa54fbb22ffa80009b43cee9b5625b5f"),
    "compiler": ("aharonahdoot/DolRecomp", "c7af6c9e149833d12ae721e6e26714f099e62e52", cache / "dolrecomp-c7af6c9.zip", "c43cac41a1de238eef528fc292b8e0635f870906cf406f2ce973184cdbc77bfb"),
    "symbols": ("yannicksuter/smstrikers-decomp", "d1f357ffeb1d8e89311edebf9a4b304b05ece7bb", cache / "smstrikers-decomp-d1f357f.zip", "78c18e586f83d6f3a899a101167415cb923937b8d71529bbff2ddefe3a86608c"),
}

def short(log, pattern):
    return [line for line in log.read_text(encoding="utf-8", errors="replace").splitlines() if pattern in line and "including file" not in line and "incluindo arquivo" not in line][:12]

def source_archive(item):
    name, (repo, revision, local, expected) = item
    url = f"https://codeload.github.com/{repo}/zip/{revision}"
    if local is None or not local.is_file():
        local = proof / (name + ".zip")
        if not local.exists():
            with urlopen(Request(url, headers={"User-Agent": "AllFix-fidelity-validation"}), timeout=45) as response:
                local.write_bytes(response.read(20_000_001))
    data = local.read_bytes()
    digest = sha256(data).hexdigest()
    if expected is not None and digest != expected:
        with urlopen(Request(url, headers={"User-Agent": "AllFix-fidelity-validation"}), timeout=45) as response:
            data = response.read(20_000_001)
        assert sha256(data).hexdigest() == expected, (url, digest)
        digest = sha256(data).hexdigest()
    return name, ({"url": url, "sha256": digest, "bytes": len(data)}, data)

with ThreadPoolExecutor(max_workers=3) as pool:
    archives = dict(pool.map(source_archive, input_revisions.items()))

# Extract release archives into fresh test directories and track every original file.
source_hashes = {}
def unpack(name, target):
    target.mkdir(parents=True, exist_ok=True)
    with ZipFile(BytesIO(archives[name][1])) as archive:
        for item in archive.infolist():
            rel = Path(item.filename).parts[1:]
            if item.is_dir():
                continue
            assert rel and all(n not in (".", "..") and ":" not in n for n in rel)
            dest = target.joinpath(*rel)
            file = archive.read(item)
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not dest.exists():
                dest.write_bytes(file)
            assert dest.read_bytes() == file, str(dest)
            source_hashes[dest] = sha256(file).hexdigest()
    return target

def run(args, folder, logfile, vs=False, timeout=480):
    cmd = list(map(str, args))
    if vs:
        batch = logfile.with_suffix(".cmd")
        batch.write_text(f'@echo off\ncall "{msvc}"\nif errorlevel 1 exit /b %errorlevel%\n'
                         f'{subprocess.list2cmdline(cmd)}\nexit /b %errorlevel%\n', encoding="utf-8")
        cmd = ["cmd.exe", "/d", "/c", str(batch)]
    with logfile.open("wb") as log:
        cp = subprocess.run(cmd, cwd=folder, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=timeout)
    print(logfile.name, cp.returncode, flush=True)
    return cp.returncode

compiler = unpack("compiler", proof / "DolRecomp")
symbols = unpack("symbols", proof / "smstrikers-decomp")
setup = [cmake, "-S", compiler, "-B", compiler / "build", "-G", "Ninja",
         "-DCMAKE_BUILD_TYPE=Release", f"-DCMAKE_C_COMPILER={clang}"]
assert run(setup, proof, proof / "tool-config.log", vs=True) == 0
assert run([cmake, "--build", compiler / "build", "--parallel", 2], proof, proof / "tool-build.log", vs=True) == 0
fixture = proof / "synthetic-return.dol"
data = bytearray(0x10c)
for index in range(3):
    offset = index * 4
    struct.pack_into(">I", data, offset, 0x100 + offset)
    struct.pack_into(">I", data, 0x48 + offset, 0x80003100 + offset)
    struct.pack_into(">I", data, 0x90 + offset, 4)
    struct.pack_into(">I", data, 0x100 + offset, 0x4e800020)  # authored blr
struct.pack_into(">I", data, 0xe0, 0x80003100)
fixture.write_bytes(data)
results = []
for name, source_name, runtime_name in (
    ("tag_and_tag", "release", "runtime_tag"),
    ("main_and_tag", "main", "runtime_tag"),
    ("main_and_head", "main", "runtime_head"),
    ("main_and_compatible", "main", "runtime_compatible"),
):
    stage = proof / name
    src = unpack(source_name, stage / "StrikersRecomp")
    runtime = unpack(runtime_name, stage / ("DolRuntime" if source_name == "release" else "GXRuntime"))
    g = stage / "generate.log"
    gen_rc = run([python, src / "tools/generate.py", "--dol", fixture, "--jobs", 2, "--dolrecomp", compiler], src, g)
    names_rc = None
    cfg_rc = None
    bld_rc = None
    if gen_rc == 0:
        names_rc = run([python, src / "tools/symbols.py", "--decomp", symbols, "--aurora", runtime / "graphics/aurora"],
                       src, stage / "symbols.log")
    if names_rc == 0:
        build = stage / "windows"
        cfg_log = stage / "configure.log"
        cfg_rc = run([cmake, "-S", src, "-B", build, "-G", "Ninja",
                      "-DCMAKE_C_COMPILER=cl.exe", "-DCMAKE_CXX_COMPILER=cl.exe"],
                     stage, cfg_log, vs=True)
        if cfg_rc == 0:
            bld_rc = run([cmake, "--build", build, "--target", "StrikersRecomp", "--parallel", 3],
                         stage, stage / "build.log", vs=True, timeout=960)
    results.append({"name": name, "source": source_name, "runtime": runtime_name,
        "generate": gen_rc, "symbols": names_rc, "configure": cfg_rc, "build": bld_rc,
        "artifact": (stage / "windows/StrikersRecomp.exe").is_file(),
        "logs": {name: {"sha256": sha256((stage / name).read_bytes()).hexdigest(),
                         "errors": short(stage / name, "error")}
                 for name in ("generate.log", "symbols.log", "configure.log", "build.log") if (stage / name).is_file()}})
    out = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_archives": {name: data[0] for name, data in archives.items()},
        "synthetic_dol_sha256": sha256(fixture.read_bytes()).hexdigest(),
        "runs": results,
        "pristine_source_count": len(source_hashes),
        "changed_sources": [str(path.relative_to(proof)) for path, digest in source_hashes.items()
                            if not path.is_file() or sha256(path.read_bytes()).hexdigest() != digest],
        "limitations": "Unchanged sources, default Aurora enabled, probe DOL only. No game installation or gameplay."
    }
    (proof / "results.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
