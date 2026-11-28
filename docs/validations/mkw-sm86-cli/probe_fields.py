"""Cross-check the draft's consumed fields against normal nvdisasm text.

The reference parser is MIT-licensed kuterd/nv_isa_solver, pinned separately;
no part of its solver, cache, subprocess wrapper, or probing loop is executed.
"""
import hashlib
import importlib.util
import json
import re
import subprocess

import probe_graphics as draft

ROOT = draft.ROOT


def parser():
    path = ROOT / "references/nv_isa_solver/parser.py"
    raw = path.read_bytes()
    if hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest() != "1f1bf14e69c3c9f86456bdca714d4a95e82d2557":
        raise ValueError("Reference text parser changed")
    spec = importlib.util.spec_from_file_location("independent_sass_text", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.InstructionParser


def reference_fields(text, insn, text_parser):
    obj = text_parser.parseInstruction(text).to_json_obj()
    if obj["base_name"] != insn.op:
        raise AssertionError((text, insn.op))
    want_guard = None if insn.v("Pg") == 7 and not insn.v("Pg@not") else f"@{'!' if insn.v('Pg@not') else ''}P{insn.v('Pg')}"
    if obj["predicate"] != want_guard:
        raise AssertionError((text, "predicate", want_guard))
    operands = obj["operands"]

    def reg(node, field_name):
        if node["type"] != "RegOperand" or node["reg_type"] != "R":
            raise AssertionError((text, "register shape", node))
        expected = 255 if node["ident"] == "Z" else int(node["ident"])
        if insn.v(field_name) != expected:
            raise AssertionError((text, field_name, insn.v(field_name), expected))
        for modifier, suffix in (("cNEG", "@negate"), ("cABS", "@absolute")):
            if bool(insn.v(field_name + suffix, 0)) != (modifier in node["modifiers"]):
                raise AssertionError((text, field_name, modifier))
        if set(node["modifiers"]) - {"cNEG", "cABS"}:
            raise AssertionError((text, "unproved operand modifier"))

    def attribute(node, expected):
        if node["type"] != "AttributeOperand" or node["modifiers"]:
            raise AssertionError((text, "attribute shape", node))
        children = node["sub_operands"]
        if len(children) != 1 or children[0]["type"] != "AddressOperand" or children[0]["modifiers"]:
            raise AssertionError((text, "address shape"))
        values = children[0]["sub_operands"]
        if len(values) != 1 or values[0] != {"type": "IntIMMOperand", "constant": expected}:
            raise AssertionError((text, "attribute address", values, expected))

    modifiers = set(obj["modifiers"])
    if insn.op in ("FADD", "FMUL"):
        if len(operands) != 3:
            raise AssertionError((text, "arithmetic operand count"))
        for node, name in zip(operands, ("Rd", "Ra", "Rc" if insn.op == "FADD" else "Rb")):
            reg(node, name)
        if modifiers != ({"SAT"} if insn.sym("sat") == "SAT" else set()):
            raise AssertionError((text, "arithmetic modifiers", modifiers))
    elif insn.op in ("ALD", "AST"):
        if len(operands) != 2:
            raise AssertionError((text, "attribute operand count"))
        if insn.op == "ALD":
            reg(operands[0], "Rd")
            attribute(operands[1], insn.v("Ra_offset"))
        else:
            attribute(operands[0], insn.v("Ra_offset"))
            reg(operands[1], "Rb")
        size = insn.sym("sz")
        if modifiers != ({size} if size != "32" else set()):
            raise AssertionError((text, "attribute width", size))
    elif insn.op == "IPA":
        if len(operands) != 2:
            raise AssertionError((text, "IPA operand count"))
        reg(operands[0], "Rd")
        attribute(operands[1], 4 * insn.v("attr"))
        if modifiers != {insn.sym("ipaop")}:
            raise AssertionError((text, "IPA frequency", modifiers))
    elif insn.op == "EXIT" and (operands or modifiers):
        raise AssertionError((text, "EXIT ordinary form"))


def main():
    text_parser = parser()
    cases = []
    for op in ("ALD", "AST"):
        for address in (0x70, 0x80, 0x1A0):
            for components in (1, 2, 3, 4):
                for register in (0, 7, 31):
                    cases.append(draft.make(op, addr=address, components=components, rd=register, rb=register))
    for address in (0x7C, 0x80, 0x8C, 0x1A0):
        for frequency in (0, 1):
            for register in (0, 7, 31):
                cases.append(draft.make("IPA", addr=address, freq=frequency, rd=register))
    for op in ("FADD", "FMUL"):
        for registers in ((0, 1, 2), (4, 7, 31), (31, 254, 255)):
            base = draft.make(op, rd=registers[0], ra=registers[1], src=registers[2])
            for sign_bits in (0, 1 << 72, 1 << 73, (1 << 63) | (1 << 62),
                              (1 << 72) | (1 << 73) | (1 << 63) | (1 << 62)):
                for saturate in (0, 1 << 77):
                    cases.append(base | sign_bits | saturate)
    for pred, inv in ((7, 0), (0, 0), (2, 1)):
        cases.append(draft.put(draft.put(draft.make("EXIT"), 12, 3, pred), 15, 1, inv))
    raw = b"".join(v.to_bytes(16, "little") for v in cases)
    temp = ROOT / "proof/field-cases.bin"
    temp.write_bytes(raw)
    try:
        p = subprocess.run([str(ROOT / "tools/nvdisasm"), "--binary", "SM86", str(temp)],
                           capture_output=True, text=True, check=True, timeout=20,
                           env={"PATH": "/usr/bin:/bin"})
        rows = re.findall(r"/\*([0-9a-fA-F]+)\*/\s*([^\n]+)", p.stdout)
        if len(rows) != len(cases):
            raise AssertionError((len(rows), len(cases), p.stderr))
        counts = {}
        for k, ((address, text), word) in enumerate(zip(rows, cases)):
            if int(address, 16) != k * 16:
                raise AssertionError("nvdisasm omitted or changed instruction addresses")
            insn = draft.decode(word, k * 16)
            reference_fields(text, insn, text_parser)
            counts[insn.op] = counts.get(insn.op, 0) + 1
        (ROOT / "proof/field-contract.sass").write_text(p.stdout)
        report = {"status": "DRAFT_GRAPHICS_FIELDS_PASS", "cases": len(cases), "by_opcode": counts,
                  "input_sha256": hashlib.sha256(raw).hexdigest(), "nvdisasm_exit": p.returncode,
                  "reference": "nv_isa_solver parser, ordinary nvdisasm text, Mesa-authored encodings",
                  "global_model": False}
        (ROOT / "proof/field-result.json").write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps(report, indent=2))
    finally:
        temp.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
