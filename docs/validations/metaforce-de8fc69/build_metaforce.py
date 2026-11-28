"""Build the verified public Metaforce revision using private LLVM-MinGW.

This operates only under the supplied new evidence work area. It never opens a
disc image or starts Metaforce. Original extracted sources and archives remain.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
import uuid


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def patch(root, relative, before, after, records):
    path = root / relative
    original = path.read_bytes()
    text = original.decode("utf8").replace("\r\n", "\n")
    if text.count(before) != 1:
        raise ValueError("source adapter anchor mismatch: " + relative)
    path.write_text(text.replace(before, after), encoding="utf8", newline="\n")
    records.append({"path": str(path), "original_sha256": hashlib.sha256(original).hexdigest(), "adapted_sha256": sha(path), "before": before, "after": after})


def adapt(source):
    records = []
    aurora = source / "extern/aurora"
    patch(aurora, "lib/system_info.cpp", "#include <comutil.h>\n",
          "#include <oleauto.h>\n#include <memory>\nusing WmiString = std::unique_ptr<OLECHAR, decltype(&SysFreeString)>;\n", records)
    patch(aurora, "lib/system_info.cpp", '  hres = pLoc->ConnectServer(_bstr_t(L"ROOT\\\\CIMV2"), // Object path of WMI namespace',
          '  const WmiString namespaceName(SysAllocString(L"ROOT\\\\CIMV2"), &SysFreeString);\n  if (!namespaceName) return Unknown;\n  hres = pLoc->ConnectServer(namespaceName.get(), // Object path of WMI namespace', records)
    patch(aurora, "lib/system_info.cpp", '  hres = pSvc->ExecQuery(bstr_t(L"WQL"), bstr_t(L"select Name from Win32_Processor"),',
          '  const WmiString queryLanguage(SysAllocString(L"WQL"), &SysFreeString);\n  const WmiString queryText(SysAllocString(L"select Name from Win32_Processor"), &SysFreeString);\n  if (!queryLanguage || !queryText) return Unknown;\n  hres = pSvc->ExecQuery(queryLanguage.get(), queryText.get(),', records)
    patch(aurora, "cmake/aurora_core.cmake",
          "target_link_libraries(aurora_core PRIVATE wbemuuid.lib comsuppw.lib ntdll.lib DXGI.lib)",
          "target_link_libraries(aurora_core PRIVATE wbemuuid ole32 oleaut32 ntdll dxgi)", records)
    # Keep the portable C API's instance toggles, required features and the
    # complete renderer. Only the optional MSVC-native C++ diagnostic descriptor
    # is omitted across the incompatible C++ ABI boundary.
    patch(aurora, "lib/webgpu/gpu.cpp",
          "    dawn::native::DawnInstanceDescriptor dawnInstanceDescriptor{};\n",
          "#if defined(__MINGW32__)\n    instanceDescriptor.nextInChain = &instanceTogglesDescriptor;\n#else\n    dawn::native::DawnInstanceDescriptor dawnInstanceDescriptor{};\n", records)
    patch(aurora, "lib/webgpu/gpu.cpp",
          "    instanceDescriptor.nextInChain = &dawnInstanceDescriptor;\n#endif\n",
          "    instanceDescriptor.nextInChain = &dawnInstanceDescriptor;\n#endif // native diagnostic descriptor\n#endif\n", records)
    return records


def adapt_nod(work, deps):
    relative = "nod_prebuilt/lib/cmake/nod/nodConfig.cmake"
    receipt = work / "nod-import-adapter.json"
    if receipt.exists():
        records = json.loads(receipt.read_text())
        if sha(deps / relative) != records[-1]["adapted_sha256"]:
            raise ValueError("nod adapter changed after validation")
        return
    if sha(deps / relative) != sha(work / "dependencies" / relative):
        raise ValueError("nod config differs before adaptation")
    records = []
    patch(deps, relative,
          'set(_nod_dll "${PACKAGE_PREFIX_DIR}/bin/${CMAKE_SHARED_LIBRARY_PREFIX}nod${CMAKE_SHARED_LIBRARY_SUFFIX}")',
          'set(_nod_dll "${PACKAGE_PREFIX_DIR}/bin/nod.dll")', records)
    patch(deps, relative,
          'set(_nod_implib "${_nod_libdir}/${CMAKE_IMPORT_LIBRARY_PREFIX}nod${CMAKE_IMPORT_LIBRARY_SUFFIX}")',
          'set(_nod_implib "${_nod_libdir}/nod.lib")', records)
    receipt.write_text(json.dumps(records, indent=2) + "\n", encoding="utf8")


def adapt_borealis_windows(work, source):
    relative = "extern/borealis/CMakeLists.txt"
    receipt = work / "borealis-windows-api-adapter.json"
    if receipt.exists():
        records = json.loads(receipt.read_text())
        if sha(source / relative) != records[-1]["adapted_sha256"]:
            raise ValueError("Borealis Windows API adapter changed")
        return
    if sha(source / relative) != sha(work / "dependencies/borealis/CMakeLists.txt"):
        raise ValueError("Borealis CMake differs before adaptation")
    records = []
    patch(source, relative,
          "    add_library(borealis::io ALIAS borealis_io)\n",
          "    add_library(borealis::io ALIAS borealis_io)\n    if (WIN32)\n        # FileRenameInfoEx is the API already used by io.cpp.\n        target_compile_definitions(borealis_io PRIVATE _WIN32_WINNT=0x0A00 NTDDI_VERSION=0x0A000002)\n    endif ()\n", records)
    receipt.write_text(json.dumps(records, indent=2) + "\n", encoding="utf8")


def adapt_card_windows(work, source):
    relative = "extern/aurora/lib/card/DolphinCardPath.cpp"
    receipt = work / "aurora-card-windows-header-adapter.json"
    if receipt.exists():
        records = json.loads(receipt.read_text())
        if sha(source / relative) != records[-1]["adapted_sha256"]:
            raise ValueError("Aurora CARD header adapter changed")
        return
    if sha(source / relative) != sha(work / "dependencies/aurora/lib/card/DolphinCardPath.cpp"):
        raise ValueError("Aurora CARD source differs before adaptation")
    records = []
    patch(source, relative, "#include <shlobj_core.h>\n",
          "#if defined(__MINGW32__)\n#include <shlobj.h>\n#include <knownfolders.h>\n#else\n#include <shlobj_core.h>\n#endif\n", records)
    receipt.write_text(json.dumps(records, indent=2) + "\n", encoding="utf8")


def adapt_alloca_windows(work, source, original):
    paths = (
        ("src/MetroidPrime/CActorLights.cpp", "#if defined(_MSC_VER)\n#include <malloc.h>\n",
         "#if defined(_MSC_VER) || defined(__MINGW32__)\n#include <malloc.h>\n"),
        ("src/Kyoto/Particles/CElementGen.cpp", "#if defined(TARGET_PC) && defined(_MSC_VER)\n#include <malloc.h>\n",
         "#if defined(TARGET_PC) && (defined(_MSC_VER) || defined(__MINGW32__))\n#include <malloc.h>\n"),
    )
    receipt = work / "metaforce-alloca-windows-header-adapter.json"
    if receipt.exists():
        records = json.loads(receipt.read_text())
        if len(records) != 2 or any(sha(Path(r["path"])) != r["adapted_sha256"] for r in records):
            raise ValueError("Metaforce alloca header adapter changed")
        return
    records = []
    candidates = []
    for relative, before, after in paths:
        baseline = (original / "source-de8fc69" / relative).read_bytes()
        text = baseline.decode("utf8").replace("\r\n", "\n")
        if text.count(before) != 1:
            raise ValueError("Metaforce alloca anchor mismatch")
        expected = text.replace(before, after).encode("utf8")
        current = (source / relative).read_bytes()
        if current not in (baseline, expected):
            raise ValueError("Metaforce alloca source differs before adaptation")
        candidates.append((source / relative, expected))
        records.append({"path": str(source / relative), "original_sha256": hashlib.sha256(baseline).hexdigest(),
                        "adapted_sha256": hashlib.sha256(expected).hexdigest(), "before": before, "after": after})
    for target, expected in candidates:
        target.write_bytes(expected)
    receipt.write_text(json.dumps(records, indent=2) + "\n", encoding="utf8")


def build(work, base, original, resume):
    if not original.joinpath("metaforce-source-receipt.json").is_file():
        raise ValueError("verified source receipt missing")
    receipt = json.loads(original.joinpath("metaforce-source-receipt.json").read_text())
    if receipt["status"] != "PINNED_GIT_SOURCE_VERIFIED" or receipt["archive_sha256"] != "efc58779e6b3ff62853e5c1d4f084a8a7744dee056d1c28faf3748dad1df524a":
        raise ValueError("source receipt identity mismatch")
    source = work / "game-src"
    deps = work / "deps-build"
    rows = json.loads((work / "dependency-results.json").read_text())
    if len(rows) != 19:
        raise ValueError("incomplete verified dependencies")
    if not resume:
        if source.exists() or deps.exists():
            raise ValueError("build source destination already occupied")
        shutil.copytree(original / "source-de8fc69", source)
        shutil.copytree(work / "dependencies", deps)
        for name in ("aurora", "borealis", "musyx"):
            target = source / "extern" / name
            if target.exists():
                if any(target.iterdir()):
                    raise ValueError("gitlink destination is not empty")
                target.rmdir()
            shutil.copytree(deps / name, target)
        changes = adapt(source)
        (work / "source-adapters.json").write_text(json.dumps(changes, indent=2) + "\n", encoding="utf8")
    adapt_nod(work, deps)
    adapt_borealis_windows(work, source)
    adapt_card_windows(work, source)
    adapt_alloca_windows(work, source, original)
    private = work / "private-user"
    for relative in ("home", "local", "roaming", "temp"):
        (private / relative).mkdir(parents=True, exist_ok=True)
    llvm = base / "gta-engine/preflight/llvm/llvm-mingw-20261020-ucrt-x86_64/bin"
    cmake = base / "gta-engine/preflight/cmake/bin/cmake.exe"
    ninja = base / "gta-engine/preflight/ninja/ninja.exe"
    system = Path(os.environ.get("SystemRoot", "C:/Windows"))
    env = {
        "SystemRoot": str(system), "WINDIR": str(system), "SystemDrive": system.drive,
        "COMSPEC": str(system / "System32/cmd.exe"), "PATHEXT": ".COM;.EXE;.BAT;.CMD",
        "PATH": os.pathsep.join(map(str, (llvm, cmake.parent, ninja.parent, system / "System32", system))),
        "USERPROFILE": str(private / "home"), "HOME": str(private / "home"),
        "APPDATA": str(private / "roaming"), "LOCALAPPDATA": str(private / "local"),
        "TEMP": str(private / "temp"), "TMP": str(private / "temp"), "NUMBER_OF_PROCESSORS": "2",
        "PROCESSOR_ARCHITECTURE": "AMD64", "CC": str(llvm / "clang.exe"), "CXX": str(llvm / "clang++.exe"),
    }
    build_dir = work / "build"
    args = [str(cmake), "-S", str(source), "-B", str(build_dir), "-G", "Ninja",
        "-DCMAKE_BUILD_TYPE=Release", "-DCMAKE_C_COMPILER=" + (llvm / "clang.exe").as_posix(),
        "-DCMAKE_CXX_COMPILER=" + (llvm / "clang++.exe").as_posix(),
        "-DCMAKE_RC_COMPILER=" + (llvm / "x86_64-w64-mingw32-windres.exe").as_posix(),
        "-DCMAKE_AR=" + (llvm / "llvm-ar.exe").as_posix(),
        "-DCMAKE_RANLIB=" + (llvm / "llvm-ranlib.exe").as_posix(),
        "-DCMAKE_MAKE_PROGRAM=" + ninja.as_posix(), "-DCMAKE_EXE_LINKER_FLAGS=-static",
        "-DBUILD_SHARED_LIBS=OFF", "-DBUILD_TESTING=OFF", "-DAURORA_ENABLE_TESTS=OFF",
        "-DAURORA_ENABLE_EXAMPLES=OFF", "-DBOREALIS_BUILD_TESTS=OFF", "-DBOREALIS_ENABLE_SENTRY=OFF",
        "-DBOREALIS_APP_VERSION_OVERRIDE=de8fc69-allfix", "-DTRACY_ENABLE=OFF", "-DFT_DISABLE_BZIP2=ON",
        "-DZSTD_BUILD_TESTS=OFF", "-DZSTD_BUILD_PROGRAMS=OFF", "-DZSTD_BUILD_CONTRIB=OFF",
        "-DAURORA_DAWN_PROVIDER=package", "-DAURORA_DAWN_LINKAGE=shared",
        "-DAURORA_SDL3_PROVIDER=package", "-DAURORA_SDL3_LINKAGE=shared",
        "-DAURORA_NOD_PROVIDER=package", "-DAURORA_NOD_LINKAGE=shared",
        "-DAURORA_DAWN_PACKAGE_URL=" + (work / "archives/dawn-windows-amd64.tar.gz").as_posix(),
        "-DAURORA_SDL3_PACKAGE_URL=" + (work / "archives/SDL3-devel-3.4.10-mingw.tar.gz").as_posix(),
        "-DAURORA_NOD_PACKAGE_URL=" + (work / "archives/libnod-windows-x86_64.tar.gz").as_posix(),
        "-DFETCHCONTENT_FULLY_DISCONNECTED=ON", "-DFETCHCONTENT_UPDATES_DISCONNECTED=ON",
        "-DCMAKE_DISABLE_FIND_PACKAGE_Git=ON", "-DCMAKE_FIND_USE_PACKAGE_REGISTRY=OFF",
        "-DCMAKE_FIND_USE_SYSTEM_PACKAGE_REGISTRY=OFF", "-DCMAKE_FIND_USE_SYSTEM_ENVIRONMENT_PATH=OFF",
        "-DCMAKE_FIND_USE_CMAKE_SYSTEM_PATH=OFF"]
    for row in rows:
        if row["name"] in ("aurora", "borealis", "musyx"):
            continue
        args.append("-DFETCHCONTENT_SOURCE_DIR_" + row["name"].upper() + "=" + (deps / row["name"]).as_posix())
    commands = [args, [str(cmake), "--build", str(build_dir), "--target", "metaforce", "--parallel", "2"]]
    results = []
    run_id = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()) + "-" + uuid.uuid4().hex[:6]
    for name, argv in zip(("configure", "build"), commands):
        log = work / ("metaforce-" + name + "-" + run_id + ".log")
        start = time.monotonic()
        with log.open("wb") as output:
            process = subprocess.run(argv, cwd=source, env=env, stdout=output, stderr=subprocess.STDOUT, timeout=3600)
        row = {"step": name, "argv": argv, "cwd": str(source), "log": str(log), "exit": process.returncode, "seconds": round(time.monotonic() - start, 3)}
        results.append(row)
        result_file = work / ("metaforce-build-results-" + run_id + ".json")
        result_file.write_text(json.dumps(results, indent=2) + "\n", encoding="utf8")
        (work / "metaforce-build-latest.json").write_text(json.dumps({"run_id": run_id, "results": str(result_file), "log": str(log)}, indent=2) + "\n", encoding="utf8")
        print(json.dumps({k: v for k, v in row.items() if k != "argv"}), flush=True)
        if process.returncode:
            raise SystemExit(process.returncode)
    exe = build_dir / "metaforce.exe"
    print(json.dumps({"status": "METAFORCE_NATIVE_LINK_PASS", "exe": str(exe), "bytes": exe.stat().st_size, "sha256": sha(exe)}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("base", type=Path)
    parser.add_argument("work", type=Path)
    parser.add_argument("original", type=Path)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    build(args.work, args.base, args.original, args.resume)
