"""Independent, deliberately bounded Mesa -> MKW frontend experiment.

This is a draft proof, not an installation backend or instructions.json producer.
The six encodings below are the inverse of the MIT-licensed Mesa 26.3.0
src/nouveau/compiler/nak/sm70_encode.rs methods named in each branch.
No DocumentSASS data, memory interception, game code, or shader dumps are inputs.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
from types import SimpleNamespace
from adapter_model import ROOT, Insn, Sph, TracedInsn, UncoveredEncoding, bits, field, READS, NVDISASM_SHA
import glsl

MESA_SHA = "cd45b5d3690316da9b991a5e5919c68833ab54ea04575c9f14cab41ea6784cd0"
OPCODES = {0x321: "ALD", 0x322: "AST", 0x326: "IPA", 0x221: "FADD", 0x220: "FMUL", 0x94D: "EXIT"}


def decode(word: int, pc: int) -> TracedInsn:
    opcode = bits(word, 0, 12)
    op = OPCODES.get(opcode)
    if op is None:
        raise UncoveredEncoding(f"opcode {opcode:#x} is outside this six-opcode proof")
    fields = {}
    consumed = (1 << 12) - 1

    def take(name, start, width, enums=None):
        nonlocal consumed
        consumed |= ((1 << width) - 1) << start
        value = bits(word, start, width)
        if enums is not None and value not in enums:
            raise UncoveredEncoding(f"{op}: {name} value {value} has no proved mapping")
        fields[name] = field(name, value, width, enums[value] if enums is not None else None)
        return value

    def fixed(start, width, expected):
        nonlocal consumed
        consumed |= ((1 << width) - 1) << start
        if bits(word, start, width) != expected:
            raise UncoveredEncoding(f"{op}: unproved fixed field {start}:{width}")

    take("Pg", 12, 3)
    take("Pg@not", 15, 1)
    # Only the scheduling region, not semantic modifiers, may be ignored.
    consumed |= ((1 << 23) - 1) << 105

    if op in ("ALD", "AST"):
        # Mesa OpALd / OpASt. Patch/physical addressing deliberately rejected.
        if op == "ALD":
            take("Rd", 16, 8)
            fixed(32, 8, 255)  # per-vertex index RZ in the proved ordinary VS
            take("io", 79, 1, {0: "I", 1: "O"})
        else:
            fixed(16, 8, 0)
            take("Rb", 32, 8)
            fixed(64, 8, 255)
        take("Ra", 24, 8)
        take("Ra_offset", 40, 10)
        take("sz", 74, 2, {0: "32", 1: "64", 2: "96", 3: "128"})
        fixed(76, 2, 0)
    elif op == "IPA":
        # Mesa OpIpa: attr is in four-byte units; frequency and location are distinct.
        take("Rd", 16, 8)
        fixed(24, 8, 0)
        take("Rb", 32, 8)
        take("attr", 64, 8)
        take("ipa_location", 76, 2, {0: "DEFAULT", 1: "CENTROID", 2: "OFFSET"})
        take("ipaop", 78, 2, {0: "PASS", 1: "CONSTANT", 2: "STATE"})
        fixed(81, 3, 7)
        if fields["ipa_location"].value != 0 or fields["ipaop"].value not in (0, 1):
            raise UncoveredEncoding("IPA: current MKW bridge proves default-location PASS/CONSTANT only")
    elif op in ("FADD", "FMUL"):
        # Mesa OpFAdd/OpFMul + encode_alu: only the all-register form is claimed.
        take("Rd", 16, 8)
        take("Ra", 24, 8)
        source = "Rc" if op == "FADD" else "Rb"  # MKW's logical operand names
        take(source, 32, 8)
        take(source + "@absolute", 62, 1)
        take(source + "@negate", 63, 1)
        fixed(64, 8, 255)
        take("Ra@negate", 72, 1)
        take("Ra@absolute", 73, 1)
        take("sat", 77, 1, {0: "", 1: "SAT"})
        take("rnd", 78, 2, {0: "RN", 1: "RM", 2: "RP", 3: "RZ"})
        take("ftz", 80, 1, {0: "", 1: "FTZ"})
        if fields["rnd"].value != 0 or fields["ftz"].value:
            raise UncoveredEncoding("proof does not claim non-default rounding/FTZ semantics")
        if op == "FMUL":
            fixed(76, 1, 0)  # no DNZ
            fixed(84, 3, 4)  # Mesa default PDIV; no scaling
            fields["scale"] = field("scale", 4, 3, "")
    else:
        # Mesa OpExit. Only its ordinary, unconditional secondary predicate.
        fixed(84, 2, 0)
        fixed(87, 3, 7)
        fixed(90, 1, 0)
    residue = word & ~consumed
    if residue:
        raise UncoveredEncoding(f"{op}: unaccounted semantic bits {residue:#x}")
    d = SimpleNamespace(mnemonic=op, cls=SimpleNamespace(name="MesaProof_" + op),
                        values=list(fields.values()), status="ok")
    return TracedInsn(pc, word, d, fields)


def put(word, start, width, value):
    if value < 0 or value >= 1 << width:
        raise ValueError("Authored field is out of range")
    mask = ((1 << width) - 1) << start
    return (word & ~mask) | (value << start)


def make(op, **values):
    word = next(code for code, name in OPCODES.items() if name == op) | (7 << 12)
    word |= 0x7E2 << 105  # a scheduling region; never executed by this experiment
    if op in ("ALD", "AST"):
        word = put(word, 24, 8, 255)
        word = put(word, 40, 10, values["addr"])
        word = put(word, 74, 2, values.get("components", 4) - 1)
        if op == "ALD":
            word = put(word, 16, 8, values.get("rd", 0))
            word = put(word, 32, 8, 255)
        else:
            word = put(word, 32, 8, values.get("rb", 0))
            word = put(word, 64, 8, 255)
    elif op == "IPA":
        word = put(word, 16, 8, values.get("rd", 0))
        word = put(word, 32, 8, 255)
        if values["addr"] % 4:
            raise ValueError("unaligned IPA address")
        word = put(word, 64, 8, values["addr"] // 4)
        word = put(word, 78, 2, values.get("freq", 0))
        word = put(word, 81, 3, 7)
    elif op in ("FADD", "FMUL"):
        word = put(word, 16, 8, values.get("rd", 0))
        word = put(word, 24, 8, values.get("ra", 0))
        word = put(word, 32, 8, values.get("src", 1))
        word = put(word, 64, 8, 255)
        if op == "FMUL":
            word = put(word, 84, 3, 4)
    else:
        word = put(word, 87, 3, 7)
    return word


def main():
    if hashlib.sha256((ROOT / "references/mesa-sm70_encode.rs").read_bytes()).hexdigest() != MESA_SHA:
        raise ValueError("Mesa source pin changed")
    nvdisasm = ROOT / "tools/nvdisasm"
    if hashlib.sha256(nvdisasm.read_bytes()).hexdigest() != NVDISASM_SHA:
        raise ValueError("nvdisasm pin changed")
    output = ROOT / "proof"
    output.mkdir(exist_ok=True)
    programs = {
        "vertex": ("vs", [make("ALD", addr=0x80), make("FMUL", rd=0, ra=0, src=1),
                            make("AST", addr=0x70), make("AST", addr=0x80), make("EXIT")]),
        "fragment": ("ps", [*(make("IPA", addr=0x80 + 4 * k, rd=k) for k in range(4)),
                              make("FADD", rd=0, ra=0, src=1), make("EXIT")]),
    }
    receipts = []
    for name, (stage, words) in programs.items():
        code = b"".join(word.to_bytes(16, "little") for word in words)
        binary = output / (name + ".bin")
        binary.write_bytes(code)
        process = subprocess.run([str(nvdisasm), "--binary", "SM86", str(binary)], capture_output=True,
                                 text=True, check=True, timeout=20, env={"PATH": "/usr/bin:/bin"})
        (output / (name + ".sass")).write_text(process.stdout)
        mnemonics = re.findall(r"/\*[0-9a-fA-F]+\*/\s*(?:@!?P\d\s+)?([A-Z][A-Z0-9]*)", process.stdout)
        expected = [OPCODES[word & 0xFFF] for word in words]
        if mnemonics != expected:
            raise AssertionError((name, mnemonics, expected, process.stdout, process.stderr))
        insns = [decode(word, k * 16) for k, word in enumerate(words)]
        header = [0] * 32
        header[0] = (1 if stage == "vs" else 5) << 10
        header[6] = 0xAA  # four ordinary interpolated components of attribute zero
        header[18] = 0xF if stage == "ps" else 0
        glsl_text, resources = glsl.translate(Sph(stage, tuple(header)), insns, stage)
        if name == "vertex" and not all(s in glsl_text for s in ("gl_Position[0]", "out_attr0[0]", "in_attr0[0]")):
            raise AssertionError("Vertex chain did not read/write the expected attributes")
        if name == "fragment" and not all(s in glsl_text for s in ("in_attr0[0]", "out_color0[0]", " + ")):
            raise AssertionError("Fragment chain did not read/write the expected colour")
        suffix = "vert" if stage == "vs" else "frag"
        (output / (name + "." + suffix)).write_text(glsl_text)
        (output / (name + ".res.json")).write_text(json.dumps(resources, indent=2) + "\n")
        receipts.append({"program": name, "stage": stage, "words": len(words), "opcodes": expected,
                         "binary_sha256": hashlib.sha256(code).hexdigest(),
                         "glsl_sha256": hashlib.sha256(glsl_text.encode()).hexdigest(),
                         "nvdisasm_exit": process.returncode})
    for bad in (0, make("IPA", addr=0x80) | 1 << 76, make("ALD", addr=0x80) | 1 << 76,
                make("FADD") | 1 << 78, make("AST", addr=0x80) | 1 << 77):
        try:
            decode(bad, 0)
        except UncoveredEncoding:
            pass
        else:
            raise AssertionError("Unproved form accepted")
    report = {"status": "DRAFT_GRAPHICS_GLSL_PASS", "production_ready": False,
              "source": "Mesa 26.3.0 SM70 encoder, verified by NVIDIA nvdisasm 12.8.90 ordinary CLI",
              "programs": receipts, "reads": sorted(READS), "negative_encodings_rejected": 5,
              "scope": "six opcodes; default register/attribute forms only; not an SM86 global model"}
    (output / "graphics-result.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "reads"}, indent=2))


if __name__ == "__main__":
    main()
