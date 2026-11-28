"""Reproducible normal-CLI -> adapter -> original GLSL proof, no game assets.

Authored words follow the pinned Mesa field layouts. Public CuAssembler words
are separately classified, including unsupported forms. Only tiny source,
diagnostics, hashes and representative GLSL are retained, not binary fixtures.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess

from cli_parse import parse_sass
from coverage_contract import cu_records
from probe_graphics import ROOT, MESA_SHA, NVDISASM_SHA, Sph, decode, glsl, make, put
from probe_graphics import UncoveredEncoding
from texture_adapter import OPCODES, decode_texture
from glsl.common import Unsupported


def authored():
    cases = []
    for op, code in OPCODES.items():
        word = code | 7 << 12 | 4 << 16 | 8 << 24 | 12 << 32 | 0x58 << 40
        word |= 6 << 64 | 7 << 81 | 1 << 84 | 0x7E2 << 105
        if op in ("SUATOM", "SURED"):
            word |= 3 << 61
        else:
            word |= 15 << 72
            word |= (3 if op in ("SULD", "SUST") else 1) << 61
        if op == "TXQ":
            for start, width in ((32, 8), (61, 3), (81, 3), (84, 3)):
                word = put(word, start, width, 0)
        if op == "TMML":
            word = put(word, 81, 3, 0)
        if op == "TLD":
            word |= 1 << 87
        cases.append(("base-" + op, word, True))
        fields = [(12, 4, [0, 1, 6, 8, 9, 14]), (24, 8, [0, 16, 64, 128]),
                  (40, 14, [0, 1, 0x3FFF]), (54, 5, [1, 15, 31])]
        if op in ("TEX", "TLD", "TLD4", "TMML"):
            fields += [(61, 3, [0, 2, 3, 4, 5, 7]), (72, 4, [1, 3, 5])]
        if op == "TEX":
            fields += [(87, 3, [1, 2, 3]), (60, 1, [1]), (79, 2, [1])]
        if op == "TLD":
            fields += [(87, 3, [3]), (60, 1, [1]), (79, 2, [1]), (78, 1, [1])]
        if op == "TLD4":
            fields += [(87, 2, [1, 2, 3]), (76, 2, [1, 2]), (79, 2, [1])]
        if op in ("SULD", "SUST", "SUATOM", "SURED"):
            fields += [(61, 3, [0, 2, 4, 5])]
        if op in ("SULD", "SUST"):
            fields += [(72, 4, [1, 3])]
        if op in ("SUATOM", "SURED"):
            fields += [(87, 3, [1, 2, 5, 6, 7])]
        for start, width, values in fields:
            for value in values:
                cases.append((f"{op}-{start}-{value}", put(word, start, width, value), None))
        if op in ("TEX", "TLD", "TLD4"):
            cases.append((op + "-half-round-toward-zero", put(word, 79, 2, 2), False))
        if op in ("TEX", "TLD", "TLD4", "SULD", "SUATOM"):
            cases.append((op + "-fault-predicate", put(word, 81, 3, 0), False))
    return cases


def disassemble(cases):
    path = ROOT / "proof/texture-adapter-input.tmp"
    pending = list(cases)
    rejected = []
    try:
        for _ in range(4):
            data = b"".join(word.to_bytes(16, "little") for _, word, _ in pending)
            path.write_bytes(data)
            p = subprocess.run([str(ROOT / "tools/nvdisasm"), "--binary", "SM86",
                                "--no-dataflow", str(path)], capture_output=True,
                               text=True, timeout=30, env={"PATH": "/usr/bin:/bin"})
            if p.returncode == 0:
                matches = re.findall(r"/\*([0-9a-fA-F]+)\*/\s*(.*?)\s*;", p.stdout)
                if len(matches) != len(pending):
                    raise AssertionError("CLI instruction boundaries changed")
                if [int(x[0], 16) for x in matches] != list(range(0, len(data), 16)):
                    raise AssertionError("CLI addresses are not contiguous")
                return pending, [x[1] for x in matches], rejected, hashlib.sha256(data).hexdigest()
            indices = {int(x, 16) // 16 for x in re.findall(r"at address 0x([0-9a-fA-F]+)", p.stderr)}
            if not indices or any(x >= len(pending) for x in indices):
                raise RuntimeError(p.stderr)
            for index in sorted(indices):
                name, word, expected = pending[index]
                if expected is True:
                    raise AssertionError(f"Required positive {name} failed normal CLI: {p.stderr}")
                rejected.append({"case": name, "word": f"{word:032x}", "outcome": "CLI_REJECTED",
                                 "diagnostic": "\n".join(x for x in p.stderr.splitlines()
                                    if f"0x{index * 16:08x}" in x)})
            pending = [x for i, x in enumerate(pending) if i not in indices]
        raise RuntimeError("More than four bounded rejection passes")
    finally:
        path.unlink(missing_ok=True)


def check_fields(word, insn):
    # Independent reference: Mesa encoder offsets, not adapter text positions.
    expected = {"bank5": (word >> 54) & 31, "tsPtrIdx": (word >> 40) & 0x3FFF,
                "Ra": (word >> 24) & 255, "Pg": (word >> 12) & 7,
                "Pg@not": (word >> 15) & 1}
    if insn.op not in ("SUST", "SURED"):
        expected["Rd"] = (word >> 16) & 255
    if insn.op in ("TEX", "TLD", "TLD4", "TMML", "TXQ"):
        expected["Rd2"] = (word >> 64) & 255
        expected["wmsk"] = (word >> 72) & 15
    if insn.op != "TXQ" and insn.op != "SULD":
        expected["Rb"] = (word >> 32) & 255
    for key, value in expected.items():
        if insn.v(key) != value:
            raise AssertionError(f"{insn.op}: {key} expected {value}, got {insn.v(key)}")


def main():
    for relative, expected in [("references/mesa-sm70_encode.rs", MESA_SHA), ("tools/nvdisasm", NVDISASM_SHA)]:
        if hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() != expected:
            raise ValueError("Source/tool pin changed: " + relative)
    cases = authored()
    authored_count = len(cases)
    for key, rows in cu_records().items():
        if key.split("_")[0] in OPCODES:
            for index, (pc, word, text) in enumerate(rows):
                cases.append((f"CuAssembler-{key}-{index}", word | 0x7E2 << 105, None))
    pending, texts, rejected, input_sha = disassemble(cases)
    results, counts, opcounts = list(rejected), Counter(), Counter()
    sample_dir = ROOT / "proof/texture-adapter"
    sample_dir.mkdir(exist_ok=True)
    header = [0] * 32
    header[0], header[18] = 5 << 10, 15
    sph = Sph("ps", tuple(header))
    for (name, word, expected), text in zip(pending, texts, strict=True):
        row = {"case": name, "word": f"{word:032x}", "sass": text}
        try:
            parsed = parse_sass(text)
            insn = decode_texture(word, 0, parsed)
            if insn is None:
                raise AssertionError("A texture case left its dispatch family")
            check_fields(word, insn)
            if expected is False:
                raise AssertionError(f"Required rejection unexpectedly decoded: {name}")
            counts["decoded"] += 1
            opcounts[insn.op] += 1
            try:
                translated, resources = glsl.translate(sph, [insn, decode(make("EXIT"), 16)], "ps")
                row["outcome"] = "GLSL_GENERATED"
                row["glsl_sha256"] = hashlib.sha256(translated.encode()).hexdigest()
                if name.startswith("base-"):
                    (sample_dir / (insn.op.lower() + ".frag")).write_text(translated)
                    (sample_dir / (insn.op.lower() + ".res.json")).write_text(json.dumps(resources, indent=2) + "\n")
            except Unsupported as error:
                row["outcome"], row["diagnostic"] = "CONSUMER_REJECTED", str(error)
                if expected is True:
                    raise AssertionError(f"Required base consumer rejected: {name}: {error}") from error
        except UncoveredEncoding as error:
            row["outcome"], row["diagnostic"] = "ADAPTER_REJECTED", str(error)
            if expected is True:
                raise AssertionError(f"Required base failed: {name}: {error}") from error
        counts[row["outcome"]] += 1
        results.append(row)
    # An unrecognized modifier, a wrong opcode, and an altered typed operand
    # must fail even when all other fields would produce valid-looking GLSL.
    base_word = authored()[0][1]
    base_text = texts[next(i for i, row in enumerate(pending) if row[0] == "base-TEX")]
    for name in ("unknown-modifier", "unknown-operand-modifier", "wrong-opcode"):
        parsed = parse_sass(base_text)
        word = base_word
        if name == "unknown-modifier":
            parsed["modifiers"].append("UNKNOWN_MODE")
        elif name == "unknown-operand-modifier":
            parsed["operands"][2]["modifiers"].append("UNKNOWN_MODE")
        else:
            word ^= 1
        try:
            decode_texture(word, 0, parsed)
        except UncoveredEncoding as error:
            results.append({"case": name, "outcome": "ADAPTER_REJECTED", "diagnostic": str(error)})
            counts["negative_boundary_pass"] += 1
        else:
            raise AssertionError(name + " was silently accepted")
    report = {"status": "PASS", "qualification": "Authored/public instruction proof; no commercial shaders or game boot.",
              "cases": len(cases), "authored": authored_count, "public": len(cases)-authored_count,
              "input_sha256": input_sha, "counts": dict(counts), "decoded_by_opcode": dict(opcounts),
              "cli_rejected": len(rejected), "binary_fixture_retained": False,
              "representative_glsl_files": 9, "spirv_validation": "separate native compiler receipt required",
              "source_pins": {"mesa_sha256": MESA_SHA, "nvdisasm_sha256": NVDISASM_SHA}, "results": results}
    (ROOT / "proof/texture-adapter-result.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "results"}, indent=2))


if __name__ == "__main__":
    main()
