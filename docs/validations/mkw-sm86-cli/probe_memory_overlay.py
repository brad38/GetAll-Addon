"""Execute the emitted signed 64-bit global-address calculation on the CPU.

Normal CLI validates authored displacements in a public LDG encoding. The
original emitter's actual address statement is then compiled as C++ and compared
against full-width addition, including carry, borrow and 64-bit wraparound.
"""
from __future__ import annotations

import hashlib
import json
import random
import re
import subprocess

from cli_parse import parse_sass
from coverage_contract import cu_records
from memory_adapter import decode_memory
from memory_overlay import install
from probe_graphics import ROOT, NVDISASM_SHA, put
from glsl.core import Builder


def main():
    if hashlib.sha256((ROOT / "tools/nvdisasm").read_bytes()).hexdigest() != NVDISASM_SHA:
        raise ValueError("Pinned disassembler changed")
    install()
    # Mesa OpLd stores this encoding's byte offset in signed bits40..63.
    offsets = [-0x800000, -0x10000, -0x100, -16, -1, 0, 1, 16, 0x100, 0x10000, 0x7FFFFF]
    seed = cu_records()["LDG_R_ARI"][0][1] | 0x7E2 << 105
    words = [put(seed, 40, 24, offset & 0xFFFFFF) for offset in offsets]
    data = b"".join(word.to_bytes(16, "little") for word in words)
    temporary = ROOT / "proof/memory-address-input.tmp"
    cpp = ROOT / "proof/memory-address-evaluate.tmp.cpp"
    exe = ROOT / "proof/memory-address-evaluate.tmp"
    try:
        temporary.write_bytes(data)
        p = subprocess.run([str(ROOT / "tools/nvdisasm"), "--binary", "SM86", "--no-dataflow", str(temporary)],
                           capture_output=True, text=True, timeout=20)
        if p.returncode:
            raise RuntimeError(p.stderr)
        texts = re.findall(r"/\*[0-9a-fA-F]+\*/\s*(.*?)\s*;", p.stdout)
        if len(texts) != len(words):
            raise AssertionError("Unexpected normal-CLI boundaries")
        code = ["#include <cstdint>\n#include <iostream>\nusing uint=uint32_t;\n",
                "uint uaddCarry(uint a,uint b,uint &c){uint64_t s=uint64_t(a)+b;c=uint(s>>32);return uint(s);}\n"]
        evidence = []
        for index, (word, offset, text) in enumerate(zip(words, offsets, texts, strict=True)):
            insn = decode_memory(word, index * 16, parse_sass(text))
            if insn.sv("Ra_offset") != offset:
                raise AssertionError("Signed byte displacement was lost before the overlay")
            statement = Builder(None, "cs").global_search(insn)
            address = re.search(r"uint gc, gl = .*?;", statement)
            if address is None:
                raise AssertionError("Address statement shape changed")
            ra = insn.v("Ra")
            code.append(f"uint64_t f{index}(uint64_t a){{uint r{ra}=uint(a),r{ra+1}=uint(a>>32); {address[0]} return (uint64_t(gh)<<32)|gl;}}\n")
            evidence.append({"offset": offset, "word": f"{word:032x}", "sass": text,
                             "emitted_address": address[0]})
        code += ["using Fn=uint64_t(*)(uint64_t);Fn funcs[]={", ",".join(f"f{i}" for i in range(len(offsets))), "};\n",
                 "int main(){unsigned i;uint64_t a,want;unsigned long n=0;while(std::cin>>i>>a>>want){auto got=funcs[i](a);if(got!=want){std::cerr<<\"FAIL offset_case=\"<<i<<\" address=\"<<a<<\" got=\"<<got<<\" want=\"<<want<<\"\\n\";return 1;}++n;}std::cout<<\"PASS comparisons=\"<<n<<\"\\n\";}\n"]
        cpp.write_text("".join(code))
        compiler = subprocess.run(["c++", "-std=c++17", "-O2", "-Wall", "-Wextra", str(cpp), "-o", str(exe)],
                                  capture_output=True, text=True, timeout=30)
        (ROOT / "proof/memory-address-compiler.log").write_text(compiler.stdout + compiler.stderr)
        if compiler.returncode:
            raise RuntimeError("Address evaluator did not compile")
        values = [0, 1, 0xFF, 0x100, 0x7FFFFFFF, 0x80000000, 0xFFFFFF00, 0xFFFFFFFF,
                  0x100000000, 0x100000100, 0x7FFFFFFF00000000, 0xFFFFFFFFFFFFFFFF]
        rng = random.Random(0x86_ADD)
        values += [rng.getrandbits(64) for _ in range(2000)]
        inputs = [f"{i} {a} {(a+offset)&0xFFFFFFFFFFFFFFFF}\n" for i, offset in enumerate(offsets) for a in values]
        run = subprocess.run([str(exe)], input="".join(inputs), capture_output=True, text=True, timeout=20)
        (ROOT / "proof/memory-address-numeric.log").write_text(run.stdout + run.stderr)
        if run.returncode:
            raise AssertionError(run.stderr)
        report = {"status": "PASS", "authored_cli_variants": len(offsets), "native_comparisons": len(inputs),
                  "normal_cli_exit": p.returncode, "compile_exit": compiler.returncode, "native_evaluate_exit": run.returncode,
                  "input_sha256": hashlib.sha256(data).hexdigest(), "generated_cpp_sha256": hashlib.sha256(cpp.read_bytes()).hexdigest(),
                  "known_regression": {"address": "0x100000100", "offset": -256, "expected": "0x100000000", "old_result": "0x200000000"},
                  "binary_fixtures_retained": False, "game_boot": False, "variants": evidence}
        (ROOT / "proof/memory-address-result.json").write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps({k: v for k, v in report.items() if k != "variants"}, indent=2))
    finally:
        temporary.unlink(missing_ok=True)
        cpp.unlink(missing_ok=True)
        exe.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
