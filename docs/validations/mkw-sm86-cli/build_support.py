"""Build the small, reproducible source overlay for the MKW normal-CLI profile.

This archive contains Python source, a closed descriptor and notices. NVIDIA's
redistributable and every authored/public binary fixture stay outside it.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parent
RUNTIME = ["adapter_model", "adapter_fields", "cli_parse", "scalar_adapter", "control_adapter",
           "memory_adapter", "texture_adapter", "lea_overlay", "memory_overlay", "cli_decoder", "backend"]
PREFIX = "sm86/translate/frontend/allfix_sm86/"
COMMIT = "006d48de08849495e01e151602690d0ec322af82"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def original(path: str, sha: str) -> bytes:
    data = (ROOT / "upstream" / path).read_bytes()
    if digest(data) != sha:
        raise ValueError("Pinned source changed: " + path)
    return data


def main():
    files: dict[str, bytes] = {}
    modules = []
    for name in RUNTIME:
        text = (ROOT / (name + ".py")).read_text()
        for dependency in RUNTIME:
            text = re.sub(r"(?m)^from " + dependency + r" import ", "from ." + dependency + " import ", text)
        target = PREFIX + name + ".py"
        files["files/" + target] = text.encode()
        modules.append(target)
    files["files/" + PREFIX + "__init__.py"] = b'"""All-Fix SM86 normal-CLI adapter for the pinned MKW consumer."""\n'
    modules.append(PREFIX + "__init__.py")
    vendor = (ROOT / "references/nv_isa_solver/parser.py").read_bytes()
    if digest(vendor) != "4db3ec6bcfab76f0480250183148b8c0b2357187a7bb6684dd92d99f9b00068e":
        raise ValueError("Parser pin changed")
    target = PREFIX + "vendor/nv_isa_parser.py"
    files["files/" + target] = vendor
    modules.append(target)

    # The original model remains byte-for-byte up to its Decoder implementation.
    path = "sm86/translate/frontend/program.py"
    before = original(path, "4e96445c14206a44ce4531ab5688c035de651981fa896b0441507d57db8e6a36")
    text = before.decode()
    anchor = "CACHE_WORDS = 20_000"
    if text.count(anchor) != 1:
        raise ValueError("Decoder boundary changed")
    after = text[:text.index(anchor)] + "# Closed All-Fix profile: normal NVIDIA CLI; no encoding-table extraction.\nfrom allfix_sm86.backend import Decoder\n"
    overlays = [{"path": path, "before_sha256": digest(before), "after_sha256": digest(after.encode())}]
    files["overlays/" + path] = after.encode()

    path = "tools/prepare/shaderstep.py"
    before = original(path, "1b5e8a528ff37163ed43381ff223108d0e91471c92c9698e988702572e9df788")
    text = before.decode()
    start, end = text.index("def spec_loads("), text.index("def tonemap_key(")
    replacement = '''def sm86_spec(game: Path, work: Path, cc: list[str]) -> Path:
    """Validate the internal normal-CLI backend; never invoke spec.py."""
    sys.path.insert(0, str(ROOT / "sm86/translate/frontend"))
    sys.path.insert(0, str(ROOT / "sm86/translate"))
    from program import Decoder

    descriptor = game / "sm86/instructions.json"
    Decoder(descriptor)
    return descriptor


'''
    text = text[:start] + replacement + text[end:]
    text = text.replace("from machine import Failed, crt_spec, run, tool_env", "from machine import Failed, run, tool_env")
    if text.count('"--no-validate", ') != 1:
        raise ValueError("Shader validation argument changed")
    text = text.replace('"--no-validate", ', "")
    after = text.encode()
    overlays.append({"path": path, "before_sha256": digest(before), "after_sha256": digest(after)})
    files["overlays/" + path] = after

    path = "tools/shaders/extract.py"
    before = original(path, "aed28f031c1af522d2c212c0119d844ad912a32803fce454601ced30ebcbc7e0")
    text = before.decode()
    start, end = text.index("def trim("), text.index("def bnsh_stages(")
    replacement = '''def trim(code: bytes, stage: str, control: bytes = b"") -> bytes:
    """Use explicit constant-data bounds; reject ambiguous instruction tails."""
    start = 0 if stage == "cs" else SPH_SIZE
    if control:
        if len(control) != CONTROL_SIZE:
            raise ValueError("All-Fix: invalid shader control bounds")
        size, offset = struct.unpack_from("<2I", control, C1_AT)
        if size:
            declared = struct.unpack_from("<I", control, CODE_SIZE_AT)[0]
            if offset < start or offset % 16 or (declared and offset + size > declared):
                raise ValueError("All-Fix: ambiguous shader constant-data bounds")
            # extract.py already removed the declared constants on a second
            # pass through translate.py.work; this operation is idempotent.
            if offset < len(code):
                if offset + size > len(code) or any(code[offset + size:]):
                    raise ValueError("All-Fix: ambiguous shader constant-data tail")
                code = code[:offset]
    if len(code) < start or (len(code) - start) % 16:
        raise ValueError("All-Fix: truncated shader instruction buffer")
    for at in range(start, len(code), 16):
        word = code[at:at + 16]
        if word == bytes(16):
            if any(code[at:]):
                raise ValueError("All-Fix: nonzero shader data after zero terminator")
            return code[:at]
        after_nop = at > start and int.from_bytes(code[at - 16:at - 14], "little") == NOP_LOW16
        if after_nop and sph_stage(word):
            raise ValueError("All-Fix: ambiguous second shader header inside declared program")
    return code


'''
    text = text[:start] + replacement + text[end:]
    old = "            code = trim(code, stage)"
    if text.count(old) != 1:
        raise ValueError("Extractor control boundary changed")
    text = text.replace(old, "            code = trim(code, stage, ctl)")
    start, end = text.index("def bnsh_stages("), text.index("def bahs_variations(")
    bounded_reader = '''def bounded_slice(data: bytes, offset: int, size: int, label: str) -> bytes:
    if offset < 0 or size < 0 or offset > len(data) or size > len(data) - offset:
        raise ValueError("All-Fix: truncated " + label)
    return data[offset:offset + size]


def bnsh_stages(bnsh: bytes):
    """Read complete, explicitly bounded BNSH records before decoding any code."""
    bounded_slice(bnsh, 0, 0x88, "BNSH header")
    if bnsh[:4] != b"BNSH" or bnsh[12:14] != b"\\xff\\xfe" or bnsh[0x60:0x64] != b"grsc":
        raise ValueError("unsupported BNSH header")
    declared = struct.unpack_from("<I", bnsh, 28)[0]
    if declared < 0x88:
        raise ValueError("All-Fix: invalid BNSH declared size")
    bnsh = bounded_slice(bnsh, 0, declared, "BNSH container")
    count, variations = struct.unpack_from("<IQ", bnsh, 124)
    bounded_slice(bnsh, variations, count * 64, "BNSH variation table")
    for i in range(count):
        program = struct.unpack_from("<Q", bnsh, variations + i * 64 + 16)[0]
        bounded_slice(bnsh, program, 64, "BNSH program record")
        for rel, stage in SLOT_STAGES.items():
            rec = struct.unpack_from("<Q", bnsh, program + rel)[0]
            if not rec:
                continue
            bounded_slice(bnsh, rec, 32, "BNSH stage record")
            ctl_off, code_off, code_size, ctl_size = struct.unpack_from("<QQII", bnsh, rec + 8)
            if ctl_size != CONTROL_SIZE or not code_size:
                raise ValueError("All-Fix: invalid BNSH shader sizes")
            ctl = bounded_slice(bnsh, ctl_off, ctl_size, "BNSH shader control")
            if ctl[:4] != CONTROL_MAGIC:
                raise ValueError(f"program {i} {stage}: control without magic")
            if struct.unpack_from("<I", ctl, CODE_SIZE_AT)[0] != code_size:
                raise ValueError("All-Fix: inconsistent BNSH code size")
            code = bounded_slice(bnsh, code_off, code_size, "BNSH shader code")
            yield i, stage, ctl, code


'''
    text = text[:start] + bounded_reader + text[end:]
    # The two other formats also carry explicit code/control bounds. Slicing
    # must not turn a truncated declared program into a valid shorter one.
    text = text.replace('    at, found, entry_of = start, {}, {}',
                        '    bounded_slice(data, pool, pool_size, "BAHS code pool")\n    at, found, entry_of = start, {}, {}')
    text = text.replace('        ctl = data[ctl_at : ctl_at + CONTROL_SIZE]',
                        '        ctl = bounded_slice(data, ctl_at, CONTROL_SIZE, "shader control")')
    text = text.replace('data[pool + code_off : pool + code_off + size]',
                        'bounded_slice(data, pool + code_off, size, "BAHS shader code")')
    text = text.replace('data[code_off : code_off + struct.unpack_from("<I", ctl, CODE_SIZE_AT)[0]]',
                        'bounded_slice(data, code_off, struct.unpack_from("<I", ctl, CODE_SIZE_AT)[0], "NDSR shader code")')
    old = ('            try:\n                found = list(bnsh_stages(data[4:]))\n'
           '            except ValueError, struct.error:\n                continue')
    if text.count(old) != 1:
        raise ValueError("BNSH failure boundary changed")
    text = text.replace(old, '            found = list(bnsh_stages(data[4:]))')
    after = text.encode()
    overlays.append({"path": path, "before_sha256": digest(before), "after_sha256": digest(after)})
    files["overlays/" + path] = after

    path = "tools/shaders/translate.py"
    before = original("translate.py", "f4a58cf8751925e8eb756e479c952bd3134c7ebdf29bc6ea0a7cc0eba415708b")
    text = before.decode()
    old = '    h.update(f"{spec.stat().st_size} {spec.stat().st_mtime_ns}".encode())'
    if text.count(old) != 1:
        raise ValueError("Translator identity boundary changed")
    text = text.replace(old, "    h.update(spec.read_bytes())")
    old = '    ctl = Path(shaders, f"{sha}.ctl").read_bytes()'
    if text.count(old) != 1:
        raise ValueError("Translator control read changed")
    text = text.replace(old + "\n", "")
    old_code = '    code = trim(Path(shaders, f"{sha}.code").read_bytes(), stage)  # a no-op on extract.py\'s output; cuts dumps'
    if text.count(old_code) != 1:
        raise ValueError("Translator input boundary changed")
    text = text.replace(old_code, old + '\n    code = trim(Path(shaders, f"{sha}.code").read_bytes(), stage, ctl)')
    old = 'if prev_th == th and (why != "ok" or Path(out, f"{key}.spv").exists()):'
    if text.count(old) != 1:
        raise ValueError("Translator cache boundary changed")
    text = text.replace(old, 'if prev_th == th and (why != "ok" or all(Path(out, f"{key}{suffix}").is_file() for suffix in (".spv", ".res.json", ".result"))):')
    old = "    if spv.exists() and gl.exists() and gl.read_text() == MESH_CS_VS:"
    if text.count(old) != 1:
        raise ValueError("Static mesh shader cache boundary changed")
    text = text.replace(old, '    if (spv.exists() and gl.exists() and gl.read_text() == MESH_CS_VS\n'
                       '            and (out / f"{MESH_CS_VS_KEY}.res.json").is_file()\n'
                       '            and (out / f"{MESH_CS_VS_KEY}.result").is_file()):')
    old = '["spirv-val", "--target-env", "vulkan1.3", str(spv)]'
    if text.count(old) != 1:
        raise ValueError("Private validator boundary changed")
    text = text.replace(old, '[str(Path(GLSLC).with_name("spirv-val.exe" if os.name == "nt" else "spirv-val")), '
                             '"--target-env", "vulkan1.3", str(spv)]')
    old = '    why = compile_check(gl, spv, "vs")'
    if text.count(old) != 1:
        raise ValueError("Static mesh shader result boundary changed")
    text = text.replace(old, old + '\n    put(out / f"{MESH_CS_VS_KEY}.result", why)')
    old = '        print(f"{n:>6}  {why}")'
    if text.count(old) != 1:
        raise ValueError("Translator completion boundary changed")
    text = text.replace(old, old + '\n    if failed or not jobs:\n        raise SystemExit("All-Fix: shader preparation is incomplete; see failed.tsv")')
    after = text.encode()
    overlays.append({"path": path, "before_sha256": digest(before), "after_sha256": digest(after)})
    files["overlays/" + path] = after

    # Import only after package-independent model initialization for the draft.
    from backend import CONFIGURATION
    files["configuration/instructions.json"] = (json.dumps(CONFIGURATION, sort_keys=True, indent=2) + "\n").encode()
    notices = {
        "mkw-MIT.txt": (ROOT / "upstream/LICENSE").read_bytes(),
        "nv-isa-solver-MIT.txt": (ROOT / "references/nv_isa_solver/LICENSE").read_bytes(),
        "CuAssembler-MIT.txt": (ROOT / "references/LICENCE.md").read_bytes(),
    }
    mesa = (ROOT / "references/mesa-sm70_encode.rs").read_text()
    header = mesa[:mesa.index("use ")]
    notices["Mesa-NAK-MIT.txt"] = header.encode() + (ROOT / "references/mesa-MIT.txt").read_bytes()
    notices["ORIGIN.txt"] = (
        "All-Fix authored normal-CLI adapter, 2026-11-27.\n"
        "MKW consumer: https://github.com/adriadam10/mkw-recomp/tree/" + COMMIT + "\n"
        "MIT text parser: https://github.com/kuterd/nv_isa_solver/tree/3640363b7d7f3ddd4a65b67502687d2d5f147d92\n"
        "Public encoding references: Mesa 26.3.0 NAK sm70_encode.rs / ir.rs (MIT);\n"
        "CuAssembler 96a9f72baf00f40b9b299653fcef8d3e2b4a3d49 (MIT).\n"
        "No global NVIDIA instruction table, game shader or media is distributed.\n"
        "nvdisasm12.8.90 is fetched separately from the official CUDA redistributable URL;\n"
        "its NVIDIA license accompanies the private executable.\n"
    ).encode()
    for name, data in notices.items():
        files["notices/" + name] = data
    files["proof/prove_backend.py"] = (ROOT / "prove_backend.py").read_bytes()
    files["proof/fixtures.json"] = (ROOT / "proof/backend-fixtures.json").read_bytes()
    manifest = {
        "format": 1, "consumer_commit": COMMIT,
        "modules": modules, "overlays": overlays,
        "configuration": {"source": "configuration/instructions.json", "target": "sm86/instructions.json"},
        "nvdisasm": {
            "url": "https://developer.download.nvidia.com/compute/cuda/redist/cuda_nvdisasm/windows-x86_64/cuda_nvdisasm-windows-x86_64-12.8.90-archive.zip",
            "bytes": 5368805,
            "sha256": "a348209c803fa67b7bc216a5b4d7a6f9a117ccc60a8c567eb94cf25ba737ec47",
            "executable": "cuda_nvdisasm-windows-x86_64-12.8.90-archive/bin/nvdisasm.exe",
            "executable_bytes": 5947392,
            "executable_sha256": "f0ab98df225b9f2568e8f56c24a919a4e1362425fb7c02101afbf85022324add",
            "license_sha256": "e2c71babfd18a8e69542dd7e9ca018f9caa438094001a58e6bc4d8c999bf0d07",
        },
        "files": [{"path": p, "bytes": len(data), "sha256": digest(data)} for p, data in sorted(files.items())],
    }
    files["manifest.json"] = (json.dumps(manifest, sort_keys=True, indent=2) + "\n").encode()
    out = ROOT / "support"
    out.mkdir(exist_ok=True)
    archive = out / "mkw-sm86-cli-support-v1.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in sorted(files.items()):
            entry = zipfile.ZipInfo(name, date_time=(2026, 11, 27, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            z.writestr(entry, data)
    (out / "manifest.json").write_bytes(files["manifest.json"])
    receipt = {"path": archive.name, "bytes": archive.stat().st_size, "sha256": digest(archive.read_bytes()),
               "files": len(files), "source_modules": len(modules), "overlays": overlays}
    (out / "package.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
