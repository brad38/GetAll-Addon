"""Run the real MKW shader preparation chain on a tiny authored BNSH archive.

Requires the verified official Windows kit and normal nvdisasm redistributable.
It never reads a game's ExeFS/RomFS, launches a game, or invokes spec.py. All
source copies and temporary shaders belong to the supplied new proof directory.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import zipfile

CHECKS = []


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(ok, label):
    if not ok:
        raise AssertionError(label)
    CHECKS.append(label)
    print("PASS " + label, flush=True)


def reject(action, label, fragment=None):
    try:
        action()
    except (ValueError, OSError) as error:
        if fragment and fragment not in str(error):
            raise AssertionError(label + ": wrong error: " + str(error)) from error
        check(True, label)
        return
    raise AssertionError(label + ": accepted unexpectedly")


def stage(kit: Path, game: Path, support: Path, expected_sha: str, nvdisasm: Path, official_archive: Path):
    check(sha(support) == expected_sha, "support archive pin")
    game.mkdir(parents=True, exist_ok=False)
    source = game / "setup/src"
    check(official_archive.stat().st_size == 221949886 and sha(official_archive) ==
          "ff655d6dc566d315c9f33f96b9b94b7dc7e9c1b383091ed36c7f35921b6444c8", "official kit ZIP pin")
    prefix = "mkw-recomp/setup/src/"
    with zipfile.ZipFile(official_archive) as original:
        for entry in original.infolist():
            if not entry.filename.startswith(prefix) or entry.is_dir():
                continue
            relative = entry.filename[len(prefix):]
            path = source / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(original.read(entry))
    with zipfile.ZipFile(support) as z:
        manifest = json.loads(z.read("manifest.json"))
        expected = {x["path"] for x in manifest["files"]} | {"manifest.json"}
        check(len(z.namelist()) == len(expected) and set(z.namelist()) == expected, "closed source package layout")
        for entry in manifest["files"]:
            data = z.read(entry["path"])
            check(len(data) == entry["bytes"] and hashlib.sha256(data).hexdigest() == entry["sha256"],
                  "support member " + entry["path"])
        for entry in manifest["overlays"]:
            path = source / entry["path"]
            check(sha(path) == entry["before_sha256"], "official overlay preimage " + entry["path"])
        for entry in manifest["overlays"]:
            path = source / entry["path"]
            path.write_bytes(z.read("overlays/" + entry["path"]))
            check(sha(path) == entry["after_sha256"], "overlay result " + entry["path"])
        for relative in manifest["modules"]:
            path = source / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(z.read("files/" + relative))
        descriptor = game / manifest["configuration"]["target"]
        descriptor.parent.mkdir(parents=True, exist_ok=True)
        descriptor.write_bytes(z.read(manifest["configuration"]["source"]))
        for name in expected:
            if name.startswith("notices/"):
                path = game / "licenses/MkwSm86" / name.removeprefix("notices/")
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(z.read(name))
    listing = source / "FILES"
    old = listing.read_text(encoding="utf-8").splitlines()
    listing.write_text("\n".join(dict.fromkeys([*old, *manifest["modules"]])) + "\n", encoding="utf-8")
    nv = manifest["nvdisasm"]
    check(nvdisasm.stat().st_size == nv["executable_bytes"] and sha(nvdisasm) == nv["executable_sha256"],
          "official NVIDIA normal CLI executable pin")
    dest = game / "sm86/nvdisasm"
    dest.mkdir()
    shutil.copy2(nvdisasm, dest / "nvdisasm.exe")
    license_file = nvdisasm.parent.parent / "LICENSE"
    check(sha(license_file) == nv["license_sha256"], "NVIDIA redistributable notice pin")
    shutil.copy2(license_file, dest / "LICENSE")
    return source


def program_bytes(case):
    words = [int(word, 16) for word in case["authored_words"]]
    code = b"".join(word.to_bytes(16, "little") for word in words)
    if case["stage"] != "cs":
        header = [0] * 32
        header[0] = ((2 if case["stage"] == "ps" else 1) | (4 << 5) |
                     ({"vs": 1, "tes?": 3, "ps": 5}[case["stage"]] << 10))
        header[6] = 0xaa
        header[18] = 15 if case["stage"] == "ps" else 0
        code = struct.pack("<32I", *header) + code
    return code


def make_archive(cases):
    # BNSH program/variation records follow the exact public extract.py reader.
    by_name = {x["name"]: x for x in cases}
    groups = [[x] for x in cases if x["name"] not in ("attributes", "interpolation")]
    if "attributes" in by_name and "interpolation" in by_name:
        groups.append([by_name["attributes"], by_name["interpolation"]])
    data = bytearray(0x100 + len(groups) * 64)
    data[:8] = b"BNSH\0\0\0\0"
    data[12:14] = b"\xff\xfe"
    data[0x60:0x64] = b"grsc"
    struct.pack_into("<IQ", data, 124, len(groups), 0x100)

    def allocate(blob):
        data.extend(bytes((-len(data)) % 16))
        at = len(data)
        data.extend(blob)
        return at

    for index, group in enumerate(groups):
        program = allocate(bytes(64))
        struct.pack_into("<Q", data, 0x100 + index * 64 + 16, program)
        for case in group:
            code = program_bytes(case)
            constants = bytes.fromhex(case.get("c1_hex", ""))
            control = bytearray(0xd8)
            control[:4] = b"\x34\x12\x76\x98"
            if constants:
                struct.pack_into("<2I", control, 0x3c, len(constants), len(code))
                code += constants
            struct.pack_into("<I", control, 0x44, len(code))
            struct.pack_into("<4I", control, 0x58, 32, 1, 1, 32768)
            control[0x56] = 6 if case["name"] == "task" else 7 if case["name"] == "mesh" else 0
            ctl_at, code_at = allocate(control), allocate(code)
            record = allocate(bytes(8) + struct.pack("<QQII", ctl_at, code_at, len(code), len(control)))
            slot = {"vs": 0x08, "tes?": 0x18, "ps": 0x28, "cs": 0x30}[case["stage"]]
            struct.pack_into("<Q", data, program + slot, record)
    struct.pack_into("<I", data, 28, len(data))
    return bytes(data)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kit", type=Path, required=True)
    ap.add_argument("--support", type=Path, required=True)
    ap.add_argument("--support-sha256", required=True)
    ap.add_argument("--nvdisasm", type=Path, required=True)
    ap.add_argument("--fixtures", type=Path, required=True)
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--staged-game", type=Path)
    ap.add_argument("--official-archive", type=Path)
    args = ap.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    game = args.staged_game or args.work / "game with spaces á"
    source = game / "setup/src" if args.staged_game else stage(args.kit, game, args.support, args.support_sha256, args.nvdisasm, args.official_archive)
    fixtures = json.loads(args.fixtures.read_text(encoding="utf-8"))
    subprocesses = []

    def audit(event, values):
        if event == "socket.connect":
            raise RuntimeError("This authored shader proof is offline")
        if event == "subprocess.Popen":
            command = values[1]
            text = str(command).lower().replace("\\", "/")
            if "sm86/spec/" in text or "spec.py" in text:
                raise RuntimeError("Excluded capture path attempted")
            subprocesses.append({"executable": str(values[0]), "arguments": list(command) if not isinstance(command, str) else command})
    sys.addaudithook(audit)
    sys.path[:0] = [str(source / "tools/prepare"), str(source / "sm86/translate"), str(source / "sm86/translate/frontend")]
    import shaderstep
    from program import Decoder
    from allfix_sm86.backend import CONFIGURATION
    from allfix_sm86.adapter_model import UncoveredEncoding
    from allfix_sm86.cli_decoder import MAX_PROGRAM_BYTES, capture_limited
    descriptor = shaderstep.sm86_spec(game, args.work, [])
    check(descriptor == game / "sm86/instructions.json" and Decoder.__module__ == "allfix_sm86.backend",
          "official shaderstep resolves the installed normal-CLI Decoder")
    check(not hasattr(shaderstep, "spec_command") and not hasattr(shaderstep, "crt_spec"),
          "capture fallback is absent from the prepared shader step")
    decoder = Decoder(descriptor)
    for case in fixtures["programs"]:
        _, instructions = decoder.program(program_bytes(case), case["stage"])
        check([i.op for i in instructions] == case["decoded"], "Decoder.program " + case["name"])
    # Windows subprocess.Popen reports executable=None when CreateProcess
    # resolves argv[0]; its command line still contains the exact pinned path.
    nv_path = str(game / "sm86/nvdisasm/nvdisasm.exe").lower().replace("\\", "/")
    check(any(nv_path in (x["executable"] + " " + str(x["arguments"])).lower().replace("\\", "/")
              for x in subprocesses), "actual ordinary CLI subprocesses observed")
    unknown = int(fixtures["negatives"]["unknown_mnemonic"], 16).to_bytes(16, "little")
    exit_word = int(fixtures["programs"][0]["authored_words"][-1], 16).to_bytes(16, "little")
    reject(lambda: decoder.program(exit_word + unknown + exit_word, "cs"),
           "unknown opcode fails instead of becoming EOF", "outside the pinned consumer")
    reject(lambda: decoder.program(exit_word + bytes(16) + exit_word, "cs"), "nonzero data after zero is not silently truncated")
    reject(lambda: decoder.program(exit_word[:-1], "cs"), "truncated instruction is rejected")
    reject(lambda: decoder.program(bytes(MAX_PROGRAM_BYTES + 16), "cs"), "oversized program rejected before spawning")
    narrow = int(fixtures["negatives"]["narrow_global_address"], 16).to_bytes(16, "little")
    reject(lambda: decoder.program(narrow + exit_word, "cs"),
           "a narrow global pointer is not promoted to a 64-bit address", "32-bit global pointer")
    uniform = int(fixtures["negatives"]["untracked_uniform_address"], 16).to_bytes(16, "little")
    _, uniform_instructions = decoder.program(uniform + exit_word, "cs")
    from glsl.core import Builder
    from glsl.common import Unsupported
    try:
        Builder(None, "cs").global_mem(uniform_instructions[0])
    except Unsupported as error:
        check("unresolved uniform base" in str(error), "an unresolved uniform address cannot lose its base in the fallback")
    else:
        raise AssertionError("A uniform address was silently changed into a vector pair")
    reject(lambda: capture_limited([sys.executable, "-I", "-c", "import sys; sys.stderr.write('x'*100000)"],
                                  environment=shaderstep.tool_env(str(args.kit / "setup/glslc/glslc.exe")), work=args.work),
           "child output is bounded before it can accumulate", "bounded output")
    reject(lambda: capture_limited([sys.executable, "-I", "-c", "import time; time.sleep(2)"],
                                  environment=shaderstep.tool_env(str(args.kit / "setup/glslc/glslc.exe")), work=args.work, timeout=0.1),
           "per-program deadline kills a stalled child", "deadline")
    with tempfile.TemporaryDirectory(prefix="negative-pin-", dir=args.work) as temporary:
        area = Path(temporary)
        bad = area / "instructions.json"
        bad.write_text(json.dumps({**CONFIGURATION, "backend_revision": "wrong"}), encoding="utf-8")
        reject(lambda: Decoder(bad), "different backend descriptor rejected", "different backend")
        bad.write_text(json.dumps(CONFIGURATION), encoding="utf-8")
        (area / "nvdisasm").mkdir()
        (area / "nvdisasm/nvdisasm.exe").write_bytes(b"not an executable")
        reject(lambda: Decoder(bad), "changed disassembler rejected before execution", "pin changed")

    from compression import zstd
    media = args.work / "authored"
    exefs, romfs = media / "exefs", media / "romfs"
    exefs.mkdir(parents=True)
    (romfs / "Shader").mkdir(parents=True)
    container = make_archive(fixtures["programs"])
    sys.path.insert(0, str(source / "tools/shaders"))
    from extract import bnsh_stages
    reject(lambda: list(bnsh_stages(container[:-16])), "a truncated BNSH container is rejected", "truncated BNSH")
    damaged = bytearray(container)
    variations = struct.unpack_from("<Q", damaged, 128)[0]
    program = struct.unpack_from("<Q", damaged, variations + 16)[0]
    rec = struct.unpack_from("<Q", damaged, program + 0x30)[0]
    ctl_at = struct.unpack_from("<Q", damaged, rec + 8)[0]
    struct.pack_into("<I", damaged, rec + 24, len(damaged) + 16)
    struct.pack_into("<I", damaged, ctl_at + 0x44, len(damaged) + 16)
    reject(lambda: list(bnsh_stages(damaged)), "a truncated BNSH code range is rejected", "truncated BNSH shader code")
    archive = romfs / "Shader/authored.bnsh.zs"
    archive.write_bytes(zstd.compress(container))
    work, output = args.work / "prepare-work", args.work / "prepared"
    work.mkdir()
    glslc = args.kit / "setup/glslc/glslc.exe"
    shaderstep.shaders(exefs, romfs, game, work, str(glslc), lambda: 2, [], dest=output)
    shaderstep.ensure_pack(output / "spirv")
    check(shaderstep.pairs_current(output / "pipeline-pairs.bin"), "official pipeline-pair output")
    check(shaderstep.pack.current(output / "spirv"), "official shader pack output")
    index = list(csv.DictReader((work / "shaders/index.csv").open(newline="")))
    check(len(index) == len(fixtures["programs"]), "all authored programs passed the official extractor")
    check((output / "spirv/failed.tsv").read_text() == "", "all extracted shaders translated and validated")
    stages = {json.loads(p.read_text())["stage"] for p in (output / "spirv").glob("*.res.json")}
    check({"vs", "ps", "cs", "task", "mesh"} <= stages, "real compute, vertex, fragment, task and mesh paths")

    # Incomplete output metadata must invalidate the real translator's cache.
    missing = next((output / "spirv").glob("*.res.json"))
    old_metadata = missing.read_bytes()
    missing.unlink()
    retry = subprocess.run([sys.executable, "-I", str(source / "tools/shaders/translate.py"),
                            "--shaders", str(work / "shaders"), "--out", str(output / "spirv"),
                            "--spec", str(descriptor), "--glslc", str(glslc), "--jobs", "2"],
                           capture_output=True, text=True, timeout=120, env=shaderstep.tool_env(str(glslc)))
    (args.work / "cache-resume.log").write_text(retry.stdout + retry.stderr, encoding="utf-8")
    check(retry.returncode == 0 and missing.is_file() and missing.read_bytes() == old_metadata,
          "a missing reflection file is rebuilt by the real cache path")

    # The extraction step itself must not hide an instruction after zero.
    from machine import Failed
    negative_media = args.work / "negative-boundary"
    (negative_media / "romfs/Shader").mkdir(parents=True)
    (negative_media / "exefs").mkdir()
    bad_case = {"name": "zero-tail", "stage": "cs", "authored_words": [exit_word.hex(), "0" * 32,
                fixtures["negatives"]["unknown_mnemonic"], exit_word.hex()]}
    # Word strings in this fixture are integers, unlike little-endian .code.
    bad_case["authored_words"][0] = bad_case["authored_words"][-1] = f"{int.from_bytes(exit_word, 'little'):032x}"
    (negative_media / "romfs/Shader/negative.zs").write_bytes(zstd.compress(make_archive([bad_case])))
    try:
        shaderstep.shaders(negative_media / "exefs", negative_media / "romfs", game,
                           negative_media / "work", str(glslc), lambda: 1, [], dest=negative_media / "output")
    except Failed:
        check(True, "official extraction refuses a nonzero instruction after zero")
    else:
        raise AssertionError("The official extraction silently truncated the negative boundary")
    truncated_media = args.work / "negative-container"
    (truncated_media / "romfs/Shader").mkdir(parents=True)
    (truncated_media / "exefs").mkdir()
    # A valid earlier container must not mask a later malformed one.
    (truncated_media / "romfs/Shader/truncated.zs").write_bytes(zstd.compress(container + damaged))
    try:
        shaderstep.shaders(truncated_media / "exefs", truncated_media / "romfs", game,
                           truncated_media / "work", str(glslc), lambda: 1, [], dest=truncated_media / "output")
    except Failed:
        check(True, "official extraction rejects a truncated declared BNSH code range")
    else:
        raise AssertionError("The official extraction accepted a truncated BNSH code range")

    # A form the adapter recognizes but the original consumer rejects must also
    # make the actual translator command fail, rather than print a warning/0.
    negative_root = args.work / "negative-consumer"
    negative_root.mkdir()
    word = fixtures["negatives"]["consumer_unsupported"]
    code = int(word, 16).to_bytes(16, "little") + exit_word
    (negative_root / "negative.code").write_bytes(code)
    (negative_root / "negative.ctl").write_bytes(bytes(0xd8))
    (negative_root / "index.csv").write_text("sha1,stage,code_bytes\nnegative,cs," + str(len(code)) + "\n")
    command = [sys.executable, "-I", str(source / "tools/shaders/translate.py"), "--shaders", str(negative_root),
               "--out", str(negative_root / "output"), "--spec", str(descriptor), "--glslc", str(glslc), "--jobs", "1"]
    negative = subprocess.run(command, capture_output=True, text=True, timeout=90, env=shaderstep.tool_env(str(glslc)))
    (args.work / "negative-consumer.log").write_text(negative.stdout + negative.stderr, encoding="utf-8")
    check(negative.returncode != 0 and "shader preparation is incomplete" in negative.stderr,
          "a real lowering failure returns nonzero from translate.py")
    check("unsupported:" in (negative_root / "output/failed.tsv").read_text(), "lowering failure retains its diagnostic")

    artifacts = []
    for path in sorted(args.work.rglob("*")):
        if path.is_file() and (path.suffix in (".spv", ".code", ".ctl", ".zs") or path.name in ("shaders.pack", "pipeline-pairs.bin")):
            artifacts.append({"path": path.relative_to(args.work).as_posix(), "bytes": path.stat().st_size, "sha256": sha(path)})
    report = {"status": "MKW_NORMAL_CLI_NATIVE_PASS", "checks": CHECKS, "programs": len(index),
              "stages": sorted(stages), "shaderstep": str(source / "tools/prepare/shaderstep.py"),
              "nvdisasm_sha256": sha(game / "sm86/nvdisasm/nvdisasm.exe"),
              "support_sha256": sha(args.support), "authored_container_sha256": hashlib.sha256(container).hexdigest(),
              "negative_translation_exit": negative.returncode, "artifacts": artifacts,
              "observed_parent_subprocesses": subprocesses, "commercial_media": False, "game_boot": False}
    (args.work / "result.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    # Keep recipes, logs, GLSL and manifests, not reproducible binary fixtures.
    for entry in artifacts:
        (args.work / entry["path"]).unlink()
    print("MKW_NORMAL_CLI_NATIVE_PASS", len(CHECKS), "checks", len(index), "authored programs", flush=True)


if __name__ == "__main__":
    main()
