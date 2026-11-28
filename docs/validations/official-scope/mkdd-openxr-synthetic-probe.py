from pathlib import Path
import argparse, hashlib, json, os, shutil, struct, subprocess
from datetime import datetime, timezone

parser = argparse.ArgumentParser(description="Build the pinned Double Dash C++ OpenXR fixture with no commercial media.")
parser.add_argument("workspace", type=Path, help="GetAll workspace containing the pinned source and compiler evidence")
parser.add_argument("output", type=Path, help="isolated directory for test-only fixture files and build logs")
args = parser.parse_args()
base = args.workspace.resolve(strict=True)
proof = args.output.resolve()
proof.mkdir(parents=True, exist_ok=True)
prior = base / "evidence-r18/official-scope-20261127/mkdd-official"
source = prior / "source"
runtime = source / "gcn-recomp"
build = proof / "build"
fixture = proof / "AllFix Synthetic Fixture.iso"
clang = base / "evidence-r18/mkdd-llvm23/bin/clang.exe"
python = prior / "python/python.exe"
ninja = Path(shutil.which("ninja"))
git = Path(shutil.which("git"))
cmake = Path(shutil.which("cmake"))
vcvars = Path(r"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat")
sdl_prefix = Path(os.environ["LOCALAPPDATA"]) / "gcn-recomp/SDL2-2.30.9-Clang23_1_3_AMD64_Release"

def sha(path, algorithm="sha256"):
    return hashlib.new(algorithm, path.read_bytes()).hexdigest()

def source_differences():
    manifest = json.loads((prior / "combined-source-manifest.json").read_text())["files"]
    return [
        item["Path"] for item in manifest
        if not (source / item["Path"]).is_file() or sha(source / item["Path"]) != item["Sha256"]
    ]

assert not source_differences(), "The pinned source manifest does not match."
source_count = len(json.loads((prior / "combined-source-manifest.json").read_text())["files"])
assert sha(clang) == "9584244d83bb095c5a2983f814692cb50e0b8d2916585516cad8f3e8596d8261"
assert (sdl_prefix / "built").read_text().strip() == "2.30.9"
# A locally authored PowerPC function: load integer 7 into r3, then return.
entry = 0x80003100
dol = bytearray(0x110)
for offset, word in ((0, 0x100), (0x48, entry), (0x90, 16), (0xE0, entry), (0x100, 0x38600007), (0x104, 0x4E800020), (0x108, 0x38600000), (0x10C, 0x4E800020)):
    struct.pack_into(">I", dol, offset, word)
dol_sha1 = hashlib.sha1(dol).hexdigest()
image = bytearray(0x1000)
image[:6] = b"AFTEST"
struct.pack_into(">I", image, 0x1C, 0xC2339F3D)
struct.pack_into(">I", image, 0x420, 0x800)
image[0x800:0x800 + len(dol)] = dol
fixture.write_bytes(image)
(proof / "symbols.txt").write_text("allfix_test = .text:0x80003100; // type:function size:0x8\nOSSaveContext = .text:0x80003108; // type:function size:0x8\n", encoding="ascii")
(proof / "tables").mkdir(exist_ok=True)
(proof / "tables/hle.txt").write_text("OSSaveContext\n", encoding="ascii")
(proof / "CMakeLists.txt").write_text(f"""
cmake_minimum_required(VERSION 3.20)
project(allfix_openxr_fixture C CXX)
add_subdirectory("{runtime.as_posix()}" gcn-recomp)
gcn_enable_languages()
gcn_add_game(
  NAME allfix_openxr_fixture
  TITLE "All-Fix synthetic OpenXR fixture"
  DISC_ID AFTEST
  DOL_SHA1 {dol_sha1}
  SYMBOLS "${{CMAKE_CURRENT_SOURCE_DIR}}/symbols.txt"
  TABLES "${{CMAKE_CURRENT_SOURCE_DIR}}/tables"
  FPS 60
  SHADER_KEYS "{source.as_posix()}/src/shader_keys.bin"
  SOURCES "{source.as_posix()}/src/race.cpp" "{source.as_posix()}/src/vr_mkdd.cpp"
          "{source.as_posix()}/src/motion.cpp" "{source.as_posix()}/src/controls.cpp")
""".lstrip(), encoding="utf-8")
configure = [str(cmake), "-S", str(proof), "-B", str(build), "-G", "Ninja", "-DCMAKE_BUILD_TYPE=RelWithDebInfo",
             f"-DCMAKE_C_COMPILER={clang}", f"-DCMAKE_CXX_COMPILER={clang.with_name('clang++.exe')}",
             f"-DPython3_EXECUTABLE={python}", f"-DGAME_ISO={fixture}", f"-DGCN_SDL2_PREFIX={sdl_prefix}"]
compile_ = [str(cmake), "--build", str(build), "--target", "allfix_openxr_fixture", "--parallel", "3"]
cmd = proof / "build.cmd"
cmd.write_text(f'@echo off\ncall "{vcvars}"\nif errorlevel 1 exit /b %errorlevel%\n'
               f'{subprocess.list2cmdline(configure)}\nif errorlevel 1 exit /b %errorlevel%\n'
               f'{subprocess.list2cmdline(compile_)}\nexit /b %errorlevel%\n', encoding="utf-8")
env = dict(os.environ)
for name in ("CL", "_CL_", "CFLAGS", "CXXFLAGS", "LDFLAGS", "CC", "CXX", "CMAKE_TOOLCHAIN_FILE"):
    env.pop(name, None)
env["PATH"] = os.pathsep.join(map(str, [clang.parent, cmake.parent, ninja.parent, python.parent, git.parent,
    Path(os.environ["WINDIR"]) / "System32", Path(os.environ["WINDIR"])]))
env["VSLANG"] = "1033"
with (proof / "build.log").open("wb") as log:
    result = subprocess.run(["cmd.exe", "/d", "/c", str(cmd)], cwd=proof, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=1200)

output = build / "allfix_openxr_fixture.exe"
object_names = sorted(p.name for p in (build / "CMakeFiles/allfix_openxr_fixture.dir").rglob("*.obj"))
loader = build / "_deps/openxr_sdk-build/src/loader/openxr_loader.lib"
cache = build / "CMakeCache.txt"
smokes = {}
if result.returncode == 0:
    assert sha(build / "main.dol", "sha1") == dol_sha1
    tmp = proof / "launch-test"
    tmp.mkdir(exist_ok=True)
    smoke_env = {key: value for key, value in os.environ.items() if not key.startswith("GCN_")}
    smoke_env.update(TEMP=str(tmp), TMP=str(tmp))
    for label, media in (("missing-media", proof / "missing original disc.iso"), ("openxr", fixture)):
        command = [str(output), "--vr", "--hidden", "--no-input-log", str(media)]
        proc = subprocess.run(command, cwd=tmp, env=smoke_env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              timeout=25)
        logfile = proof / ("smoke-" + label + ".log")
        logfile.write_bytes(proc.stdout)
        smokes[label] = {"exit_code": proc.returncode, "log_sha256": sha(logfile)}
        if label == "missing-media":
            smokes[label]["expected_media_error"] = proc.returncode == 1 and b"No game image found" in proc.stdout
        else:
            smokes[label]["loader_reached"] = b"xrCreateInstance" in proc.stdout
            smokes[label]["no_active_openxr_runtime"] = b"could not start vr" in proc.stdout.lower() and b"active runtime file in registry" in proc.stdout
evidence = {
    "checked_at_utc": datetime.now(timezone.utc).isoformat(),
    "game_source_revision": "bd36eb982ea58c6651584cc48264876d1aba9546",
    "toolkit_source_revision": "b2193d7c7ce65c40959cf81859beaacafeebfd99",
    "artifact_type": "Synthetic game-independent PPC fixture, not original game media or a playable executable",
    "fixture_sha256": sha(fixture), "fixture_dol_sha1": dol_sha1,
    "configure": configure, "build": compile_, "exit_code": result.returncode,
    "original_source_count": source_count, "changed_original_sources": source_differences(), "launch_smokes": smokes,
    "openxr_enabled": cache.exists() and "GCN_OPENXR:BOOL=ON" in cache.read_text(encoding="utf-8"),
    "frontend_sources_compiled": sorted(set(object_names) & {"xr_frontend.cpp.obj", "xr_desktop.cpp.obj"}),
    "mkdd_host_sources_compiled": sorted(set(object_names) & {"race.cpp.obj", "vr_mkdd.cpp.obj", "motion.cpp.obj", "controls.cpp.obj"}),
    "static_loader_present": loader.is_file(),
    "fixture_executable_sha256": sha(output) if output.is_file() else None,
    "limitations": "Official retail build and first boot need a legitimate GM4E01 disc with the specified main.dol SHA-1. This uses the unchanged upstream CMake toolkit with a separate fixture project. The OpenXR loader ran, but no active OpenXR runtime or headset was available. No gameplay tested.",
}
(proof / "result.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
if result.returncode:
    raise SystemExit(result.returncode)
