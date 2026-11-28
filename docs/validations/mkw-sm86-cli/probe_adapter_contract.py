"""Exercise draft adapters with public source records; distinguish every failure."""
from __future__ import annotations

from collections import Counter, defaultdict
import importlib
import hashlib
import json
import re
import tempfile
from pathlib import Path

from coverage_contract import ROOT, cu_records, source_contract
from cli_parse import parse_sass
from probe_graphics import UncoveredEncoding, make, decode as decode_graphics, glsl
from glsl.core import Builder
from glsl.common import Unsupported
from scalar_adapter import decode_scalar
from lea_overlay import decode_lea, install as install_lea
from memory_overlay import install as install_memory
from cli_decoder import capture_limited
from adapter_model import NVDISASM_SHA


def main():
    install_lea()
    install_memory()
    adapters = [decode_lea, decode_scalar]
    for module, name in (("control_adapter", "decode_control"), ("memory_adapter", "decode_memory"), ("texture_adapter", "decode_texture")):
        if (ROOT / (module + ".py")).exists():
            adapters.append(getattr(importlib.import_module(module), name))
    required, _, _ = source_contract()
    corpus = [(key, pc, word, text) for key, values in cu_records().items()
              if key.split("_")[0] in required for pc, word, text in values]
    extra = json.loads((ROOT / "references/CuAsm/UP2UR-sm80-records.json").read_text())
    corpus += [(key, pc, word, text) for key, values in extra["records"].items() for pc, word, text in values]
    # Exercise the exact CLI text of the installed version, not merely the
    # public corpus's historical spelling. Known rejected source words remain
    # recorded negatives; no new failure is removed from this batch.
    cli_report = json.loads((ROOT / "proof/cli-corpus-result.json").read_text())
    excluded = {(x["form"], x["word"]) for x in cli_report["rejected_records"]}
    corpus = [x for x in corpus if (x[0], f"{x[2]:032x}") not in excluded]
    words = [x[2] | (0x7e2 << 105) for x in corpus]
    binary = b"".join(word.to_bytes(16, "little") for word in words)
    if hashlib.sha256(binary).hexdigest() != cli_report["input_sha256"]:
        raise ValueError("The pinned positive CLI corpus changed")
    executable = ROOT / "tools/nvdisasm"
    if hashlib.sha256(executable.read_bytes()).hexdigest() != NVDISASM_SHA:
        raise ValueError("Disassembler pin changed")
    with tempfile.NamedTemporaryFile(dir=ROOT / "proof", suffix=".bin", delete=False) as temporary:
        temporary.write(binary)
        input_path = Path(temporary.name)
    try:
        status, stdout, stderr = capture_limited([str(executable), "--binary", "SM86", "--no-dataflow", str(input_path)],
                                                environment={"PATH": "/usr/bin:/bin"}, work=ROOT / "proof")
        if status:
            raise RuntimeError(stderr)
        rows = re.findall(r"/\*([0-9a-fA-F]+)\*/\s*(.*?)\s*;", stdout)
        if len(rows) != len(corpus) or [int(pc, 16) for pc, _ in rows] != list(range(0, len(binary), 16)):
            raise ValueError("Unexpected normal-CLI boundaries")
        corpus = [(row[0], k * 16, word, text) for k, (row, word, (_, text)) in enumerate(zip(corpus, words, rows, strict=True))]
    finally:
        input_path.unlink(missing_ok=True)
    accepted, reject, upstream_reject, broken, first, first_text = Counter(), Counter(), Counter(), [], {}, {}
    samples = defaultdict(list)
    for key, pc, word, text in corpus:
        op = key.split("_")[0]
        try:
            parsed = parse_sass(text)
        except Exception as e:
            reject[op] += 1
            if len(samples[op]) < 3:
                samples[op].append({"type": "text-parser", "text": text, "error": str(e)})
            continue
        try:
            instruction = next((x for adapter in adapters if (x := adapter(word, pc, parsed)) is not None), None)
            if instruction is None:
                continue
        except UncoveredEncoding as e:
            reject[op] += 1
            if len(samples[op]) < 3:
                samples[op].append({"type": "closed-rejection", "text": text, "error": str(e)})
            continue
        try:
            b = Builder(None, "cs")
            statement = b.insn(instruction)
            b.track_ssbo(instruction)
        except Unsupported as e:
            upstream_reject[op] += 1
            if len(samples[op]) < 3:
                samples[op].append({"type": "upstream-rejection", "text": text, "error": str(e)})
            continue
        except Exception as e:
            broken.append({"opcode": op, "text": text, "type": type(e).__name__, "error": str(e)})
            continue
        accepted[op] += 1
        if op not in first and statement:
            first[op], first_text[op] = instruction, text
    result = {"status": "DRAFT_ADAPTER_CORPUS", "normal_cli_exit": status,
              "normal_cli_records": len(corpus), "normal_cli_input_sha256": hashlib.sha256(binary).hexdigest(),
              "retained_cli_rejections": len(excluded), "accepted_mnemonics": len(accepted),
              "accepted": dict(sorted(accepted.items())), "adapter_rejections": dict(sorted(reject.items())),
              "upstream_rejections": dict(sorted(upstream_reject.items())), "broken_bindings": broken,
              "samples": dict(samples), "first_accepted": first_text, "production_ready": False}
    (ROOT / "proof/adapter-corpus-result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("samples", "first_accepted", "broken_bindings")}, indent=2))
    print("Broken bindings", len(broken), broken[:12])
    if broken:
        raise SystemExit(1)
    if first:
        # A single authored composition of public instruction records. It is
        # compiled, never executed; no game input or commercial shader appears.
        instructions = list(first.values())
        for k, instruction in enumerate(instructions):
            instruction.pc = k * 16
        instructions.append(decode_graphics(make("EXIT"), len(instructions) * 16))
        text, resources = glsl.translate(None, instructions, "cs")
        (ROOT / "proof/scalar-composition.comp").write_text(text)
        (ROOT / "proof/scalar-composition.res.json").write_text(json.dumps(resources, indent=2) + "\n")
        print("SCALAR_COMPOSITION_GLSL", len(instructions), len(text))


if __name__ == "__main__":
    main()
