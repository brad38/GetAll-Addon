"""Small complete authored programs for control, atomics and task/mesh.

Words are authored from pinned Mesa encoders or repacked public CuAssembler
templates. NVIDIA's normal CLI must decode every word before any frontend field
is constructed. No shader/game dump is an input.
"""
from __future__ import annotations

import hashlib
import json
import struct

from cli_decoder import CliDecoder
from coverage_contract import ROOT, cu_records
from probe_graphics import make, put, glsl


def main():
    records = cu_records()
    output = ROOT / "proof/program-chain"
    output.mkdir(exist_ok=True)
    decoder = CliDecoder(work=output)

    def schedule(word):
        word = put(word, 12, 4, 7)
        return put(word, 105, 17, 0x7e2)

    def template(key, match=lambda text: True):
        return schedule(next(word for _, word, text in records[key] if match(text)))

    def move(rd, value, uniform=False):
        word = template("UMOV_UR_II" if uniform else "MOV_R_II")
        word = put(word, 16, 6 if uniform else 8, rd)
        return put(word, 32, 32, value & 0xffffffff)

    def branch(key, pc, target, reg=None, displacement=False):
        word = template(key)
        if reg is not None:
            word = put(word, 24, 6 if key.startswith("BRXU") else 8, reg)
        value = target if displacement else target - pc - 16
        assert value % 4 == 0
        return put(word, 34, 48, (value // 4) & ((1 << 48) - 1))

    def isbe(write=False, off=0, output_access=False, attr=True, skew=False, size=2, reg=0):
        word = (0x927 if write else 0x923) | (7 << 12)
        word = put(word, 24, 8, 255)
        word = put(word, 32 if write else 16, 8, reg)
        for start, width, value in ((40, 16, off), (74, 2, size), (76, 2, 3 if attr else 0), (78, 1, int(skew)), (79, 1, int(output_access))):
            word = put(word, start, width, value)
        return schedule(word)

    def atomic(reduction=False):
        # Mesa OpAtom global UGPR path, ADD/U32, ordinary uniform64-bit base.
        word = (0x98e if reduction else 0x9a8) | (7 << 12)
        for start, width, value in ((16, 8, 255 if reduction else 6), (24, 8, 255), (32, 8, 4),
                                    (64, 6, 4), (72, 1, 1), (77, 4, 0), (84, 3, 1), (91, 1, 1)):
            word = put(word, start, width, value)
        if not reduction:
            word = put(word, 81, 3, 7)
        return schedule(word)

    uldc = template("ULDC_UR_cAI", lambda s: ".64" in s)
    uldc = put(put(put(uldc, 16, 6, 4), 38, 16, 0x200), 54, 5, 0)
    nop, exit_word = template("NOP"), make("EXIT")
    # An untracked 64-bit address exercises the signed fallback correction,
    # rather than the separate constant-buffer-relative addressing fast path.
    negative_load = put(template("LDG_R_ARI"), 40, 24, (-0x100) & 0xffffff)
    programs = {
        "branch": ("cs", [branch("BRA_II", 0, 32), nop, exit_word]),
        "branch-register": ("cs", [move(0, 16), branch("BRX_R_II", 16, 0, 0, True), nop, exit_word]),
        "branch-uniform": ("cs", [move(0, 16, True), branch("BRXU_UR_II", 16, 0, 0, True), nop, exit_word]),
        "call-return": ("cs", [move(0, 32), branch("CALL_II", 16, 48), exit_word,
                                  move(1, 7), branch("RET_R_II", 64, 0, 0)]),
        "return-dispatch": ("cs", [move(0, 48), branch("RET_R_II", 16, 0, 0), nop, exit_word]),
        "atomics": ("cs", [uldc, atomic(False), atomic(True), exit_word]),
        "negative-global-offset": ("cs", [uldc, atomic(False), move(4, 0x100), move(5, 1), negative_load, exit_word]),
        "task": ("vs", [isbe(), isbe(True, off=4, output_access=True), exit_word]),
        "mesh": ("tes?", [isbe(), isbe(True, output_access=True, skew=True),
                            isbe(True, off=3, output_access=True, attr=False), exit_word]),
        "kill": ("ps", [schedule(0x95b | (7 << 87)), exit_word]),
        "attributes": ("vs", [make("ALD", addr=0x80), make("FMUL"), make("AST", addr=0x70), make("AST", addr=0x80), exit_word]),
        "interpolation": ("ps", [*(make("IPA", addr=0x80+4*k, rd=k) for k in range(4)), make("FADD"), exit_word]),
    }
    report = []
    for name, (stage, words) in programs.items():
        body = b"".join(word.to_bytes(16, "little") for word in words)
        header = [0] * 32
        header[0] = (2 if stage == "ps" else 1) | (4 << 5) | ({"vs": 1, "tes?": 3, "ps": 5}.get(stage, 0) << 10)
        header[6] = 0xaa
        header[18] = 15 if stage == "ps" else 0
        binary = (struct.pack("<32I", *header) if stage != "cs" else b"") + body
        row = {"name": name, "stage": stage, "words": len(words), "sha256": hashlib.sha256(binary).hexdigest(),
               "authored_words": [f"{x:032x}" for x in words]}
        try:
            sph, instructions = decoder.program(binary, stage)
            row["decoded"] = [i.op for i in instructions]
            text, resources = glsl.translate(sph, instructions, stage)
            suffix = "task" if name == "task" else "mesh" if name == "mesh" else {"cs": "comp", "vs": "vert", "ps": "frag"}[stage]
            (output / (name + "." + suffix)).write_text(text)
            (output / (name + ".res.json")).write_text(json.dumps(resources, indent=2) + "\n")
            row.update(status="GLSL_PASS", glsl_sha256=hashlib.sha256(text.encode()).hexdigest(), glsl_bytes=len(text.encode()))
        except Exception as error:
            row.update(status="REJECTED", error=type(error).__name__ + ": " + str(error))
        (output / (name + ".sass")).write_text(decoder.last_text)
        report.append(row)
        print(name, row["status"], row.get("decoded"), row.get("error", ""))
    (ROOT / "proof/program-chain-result.json").write_text(json.dumps({"programs": report, "production_ready": False}, indent=2) + "\n")
    if any(row["status"] != "GLSL_PASS" for row in report):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
