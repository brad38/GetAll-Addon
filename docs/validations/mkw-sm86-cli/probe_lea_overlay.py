"""Normal CLI plus executed numerical proof of the LEA/ULEA overlay.

The emitted GLSL arithmetic is valid C++ with uint=uint32_t. Compile that exact
body and compare its results/carry to the independent Mesa IR folding algorithm
over boundaries and deterministic random inputs. No GPU/game inputs are used.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import random
import re
import subprocess

from cli_parse import parse_sass
from coverage_contract import cu_records
from lea_overlay import decode_lea, emit_lea, install
from probe_graphics import ROOT, NVDISASM_SHA, Sph, glsl, decode, make, put
from glsl.core import Builder

MASK = 0xFFFFFFFF
MESA_IR_SHA = "d297a3b1c2148d0f9875d6c099e34e4c9780afc56f49998468be509dc4e75485"


def reference(a, b, high_word, carry, shift, high, sx, extended, modifier, invert_carry):
    # Transcribed from Mesa ir.rs OpLea/OpLeaX Foldable, retaining its two
    # independent overflowing_add operations. This does not evaluate GLSL.
    if sx:
        high_word = MASK if a & 0x80000000 else 0
    temp = (((high_word << 32) | a) >> (32 - shift)) & MASK if high else (a << shift) & MASK
    overflow = False
    if modifier == "a":
        if extended:
            temp ^= MASK
        else:
            overflow = temp == 0
            temp = (-temp) & MASK
    if modifier == "b":
        if extended:
            b ^= MASK
        else:
            overflow = b == 0
            b = (-b) & MASK
    added = temp + b
    overflow |= added > MASK
    result = added & MASK
    if extended:
        added = result + int(bool(carry) ^ invert_carry)
        overflow |= added > MASK
        result = added & MASK
    return result, int(overflow)


def templates():
    output = []
    for uniform in (False, True):
        for high, sx in ((False, False), (True, False), (True, True)):
            for extended in (False, True):
                for modifier in ("none", "a", "b"):
                    for shift in (0, 1, 16, 31):
                        for invert_carry in ((False, True) if extended else (False,)):
                            word = (0x291 if uniform else 0x211) | 7 << 12 | 1 << 24 | 2 << 32 | 3 << 64
                            word |= 1 << 81 | shift << 75 | 0x7E2 << 105
                            if uniform:
                                word |= 1 << 91
                            word = put(word, 80, 1, int(high))
                            word = put(word, 73, 1, int(sx))
                            word = put(word, 74, 1, int(extended))
                            word = put(word, 72, 1, int(modifier == "a"))
                            word = put(word, 63, 1, int(modifier == "b"))
                            word = put(word, 87, 3, 0 if extended else 7)
                            word = put(word, 90, 1, int(invert_carry) if extended else 1)
                            output.append((word, dict(uniform=uniform, shift=shift, high=high, sx=sx,
                                                      extended=extended, modifier=modifier, invert_carry=invert_carry)))
    return output


def main():
    for path, expected in ((ROOT / "references/mesa-ir.rs", MESA_IR_SHA),
                           (ROOT / "tools/nvdisasm", NVDISASM_SHA)):
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError("Pinned numerical reference/tool changed")
    install()
    cases = templates()
    public = [(key, word | 0x7E2 << 105) for key, rows in cu_records().items()
              if key.startswith(("LEA_", "ULEA_")) for _, word, _ in rows]
    words = [w for w, _ in cases] + [w for _, w in public]
    raw = b"".join(word.to_bytes(16, "little") for word in words)
    public_count, rejected = len(public), []
    tmp = ROOT / "proof/lea-overlay-input.tmp"
    cpp = ROOT / "proof/lea-overlay-evaluate.tmp.cpp"
    exe = ROOT / "proof/lea-overlay-evaluate.tmp"
    result_file = ROOT / "proof/lea-overlay-result.json"
    try:
        for attempt in range(4):
            tmp.write_bytes(raw)
            p = subprocess.run([str(ROOT / "tools/nvdisasm"), "--binary", "SM86", "--no-dataflow", str(tmp)],
                               capture_output=True, text=True, timeout=30, env={"PATH": "/usr/bin:/bin"})
            if p.returncode == 0:
                break
            indices = {int(x, 16) // 16 for x in re.findall(r"at address 0x([0-9a-fA-F]+)", p.stderr)}
            if not indices or any(x < len(cases) or x >= len(words) for x in indices):
                raise RuntimeError(p.stderr)
            for index in sorted(indices):
                rejected.append({"form": public[index-len(cases)][0], "word": f"{words[index]:032x}",
                                 "diagnostic": "\n".join(x for x in p.stderr.splitlines()
                                      if f"0x{index * 16:08x}" in x)})
            public = [row for i, row in enumerate(public) if i + len(cases) not in indices]
            words = [w for w, _ in cases] + [w for _, w in public]
            raw = b"".join(word.to_bytes(16, "little") for word in words)
        else:
            raise RuntimeError("Normal CLI did not settle within four bounded batches")
        texts = re.findall(r"/\*[0-9a-fA-F]+\*/\s*(.*?)\s*;", p.stdout)
        if len(texts) != len(words):
            raise AssertionError("Normal CLI lost instruction boundaries")
        insns = [decode_lea(word, 0, parse_sass(text)) for word, text in zip(words, texts, strict=True)]
        if any(x is None for x in insns):
            raise AssertionError("A LEA instruction left its dispatch family")
        counts, glsl_hashes = Counter(), []
        header = [0] * 32
        header[0], header[18] = 5 << 10, 15
        for index, insn in enumerate(insns):
            source, resources = glsl.translate(Sph("ps", tuple(header)), [insn, decode(make("EXIT"), 16)], "ps")
            counts[insn.op] += 1
            glsl_hashes.append(hashlib.sha256(source.encode()).hexdigest())
            if index in (0, 100, len(cases)//2, len(cases)-1):
                (ROOT / f"proof/lea-overlay-{index}.frag").write_text(source)
        code = ["#include <cstdint>\n#include <iostream>\nusing uint=uint32_t;\nstruct Result { uint value; bool carry; };\n"]
        for index, insn in enumerate(insns[:len(cases)]):
            body = emit_lea(Builder(None, "ps"), insn)
            uniform = cases[index][1]["uniform"]
            prefix, pp = ("ur", "up") if uniform else ("r", "p")
            code.append(f"Result f{index}(uint a,uint b,uint c,bool carry) {{ uint {prefix}0=0,{prefix}1=a,{prefix}2=b,{prefix}3=c; bool {pp}0=carry,{pp}1=false; {body} return {{{prefix}0,{pp}1}}; }}\n")
        code += ["using Fn=Result(*)(uint,uint,uint,bool);\nFn functions[]={",
                 ",".join(f"f{i}" for i in range(len(cases))), "};\n",
                 "int main(){unsigned n,a,b,c,carry,want,p; unsigned long count=0; while(std::cin>>n>>a>>b>>c>>carry>>want>>p){auto got=functions[n](a,b,c,carry); if(got.value!=want||got.carry!=bool(p)){std::cerr<<\"FAIL case=\"<<n<<\" value=\"<<got.value<<\" want=\"<<want<<\" carry=\"<<got.carry<<\" wantCarry=\"<<p<<\"\\n\";return 1;}++count;} std::cout<<\"PASS comparisons=\"<<count<<\"\\n\";}\n"]
        cpp.write_text("".join(code))
        built = subprocess.run(["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Wno-unused-variable", str(cpp), "-o", str(exe)],
                               capture_output=True, text=True, timeout=60)
        (ROOT / "proof/lea-overlay-compiler.log").write_text(built.stdout + built.stderr)
        if built.returncode:
            raise RuntimeError("Arithmetic harness compiler failed")
        boundaries = [0, 1, 2, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFE, MASK]
        rng, inputs = random.Random(0x26_30_1EA), []
        for index, (_, params) in enumerate(cases):
            numeric = {k: v for k, v in params.items() if k != "uniform"}
            values = [(a, b, c, carry) for a in boundaries for b in boundaries
                      for c, carry in ((0, 0), (MASK, 1), (0x12345678, 0), (0x80000000, 1))]
            values += [(rng.getrandbits(32), rng.getrandbits(32), rng.getrandbits(32), rng.randrange(2)) for _ in range(32)]
            for a, b, c, carry in values:
                value, outcarry = reference(a, b, c, carry, **numeric)
                inputs.append(f"{index} {a} {b} {c} {carry} {value} {outcarry}\n")
        evaluated = subprocess.run([str(exe)], input="".join(inputs), capture_output=True, text=True, timeout=30)
        (ROOT / "proof/lea-overlay-numeric.log").write_text(evaluated.stdout + evaluated.stderr)
        if evaluated.returncode:
            raise AssertionError(evaluated.stderr)
        report = {"status": "PASS", "authored_instruction_variants": len(cases), "public_cuasm_records": public_count,
                  "public_cli_accepted": len(public), "public_cli_rejected": rejected,
                  "normal_cli_exit": p.returncode, "glsl_generated": dict(counts),
                  "numeric_comparisons": len(inputs), "cpp_compile_exit": built.returncode,
                  "native_evaluate_exit": evaluated.returncode, "input_sha256": hashlib.sha256(raw).hexdigest(),
                  "generated_cpp_sha256": hashlib.sha256(cpp.read_bytes()).hexdigest(),
                  "mesa_ir_sha256": MESA_IR_SHA, "glsl_hashes": glsl_hashes,
                  "retained_binary_fixtures": False, "game_boot": False,
                  "qualification": "Executed integer arithmetic proof, not GPU performance or commercial shader validation."}
        result_file.write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps({k: v for k, v in report.items() if k != "glsl_hashes"}, indent=2))
    finally:
        tmp.unlink(missing_ok=True)
        exe.unlink(missing_ok=True)
        cpp.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
