"""Run the official StrikersRecomp ISO conversion and module build on authored data."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import struct
import subprocess
import sys

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def fixture_iso(dol, output):
    # GameCube header, empty filesystem table, and only the authored test DOL.
    dol_offset = 0x3000
    fst_offset = 0x4000
    payload = dol.read_bytes()
    if len(payload) > fst_offset - dol_offset:
        raise ValueError("Fixture DOL does not fit in the synthetic ISO")
    image = bytearray(0x6000)
    image[:6] = b"QATX01"
    struct.pack_into(">I", image, 0x1c, 0xC2339F3D)
    struct.pack_into(">4I", image, 0x420, dol_offset, fst_offset, 13, 13)
    image[dol_offset:dol_offset + len(payload)] = payload
    struct.pack_into(">3I", image, fst_offset, 0x01000000, 0, 1)
    output.write_bytes(image)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ("source", "dolrecomp", "dol", "host_source", "cmake", "ninja", "clang", "output"):
        parser.add_argument(key, type=Path)
    args = parser.parse_args()
    tools = {key: value.resolve() for key, value in vars(args).items()}
    output = tools["output"]
    output.mkdir()
    source = output / "StrikersRecomp"
    shutil.copytree(tools["source"], source, ignore=shutil.ignore_patterns("generated", "__pycache__", ".git"))
    iso = output / "Disco de teste.iso"
    fixture_iso(tools["dol"], iso)
    original_hash = sha(iso)
    generated = source / "generated"
    module_dir = output / "module"
    abi = tools["host_source"] / "Source/Core/Core/PowerPC/StaticRecomp"
    steps = {
        "generate": [sys.executable, source / "tools/generate.py", "--iso", iso,
                     "--dolrecomp", tools["dolrecomp"], "--jobs", "2"],
        "configure": [tools["cmake"], "-S", source / "chassis-module", "-B", module_dir, "-G", "Ninja",
                      f"-DCMAKE_MAKE_PROGRAM={tools['ninja'].as_posix()}",
                      f"-DCMAKE_C_COMPILER={tools['clang'].as_posix()}",
                      f"-DCHASSIS_ABI_DIR={abi.as_posix()}", f"-DPython3_EXECUTABLE={sys.executable}"],
        "build": [tools["cmake"], "--build", module_dir, "--parallel", "2"],
    }
    for name, command in steps.items():
        with (output / f"{name}.log").open("wb") as log:
            subprocess.run(command, cwd=source, stdout=log, stderr=subprocess.STDOUT, timeout=90, check=True)
    extracted = generated / "main.dol"
    module = module_dir / "gG4QE01_recomp.dll"
    if sha(iso) != original_hash or sha(extracted) != sha(tools["dol"]):
        raise ValueError("The upstream generator altered the disc or extracted a different DOL")
    if not module.is_file() or module.stat().st_size == 0:
        raise ValueError("The upstream build did not produce the Strikers module")
    report = {"scope": "Authored synthetic GC ISO; no original game data or launch.",
              "iso_sha256": original_hash, "extracted_dol_sha256": sha(extracted), "module_sha256": sha(module),
              "source_files_unchanged": all(sha(source / path.relative_to(tools["source"])) == sha(path)
                  for path in (tools["source"] / "tools").glob("*.py"))}
    if not report["source_files_unchanged"]:
        raise ValueError("Generator changed an upstream Python source file")
    (output / "result.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
