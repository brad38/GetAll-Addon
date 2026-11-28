"""Pinned text parser boundary with lossless immediate serialization.

The upstream solver's to_json_obj omits IntIMMOperand.modifiers. Copying that
JSON directly drops a leading minus. Preserve the object modifiers recursively
and fold integer literal signs into the literal value before exposing fields.
"""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
PARSER = ROOT / "references/nv_isa_solver/parser.py"
if not PARSER.is_file():
    PARSER = ROOT / "vendor/nv_isa_parser.py"
raw = PARSER.read_bytes()
if hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() != "1f1bf14e69c3c9f86456bdca714d4a95e82d2557":
    raise ValueError("Parser source pin changed")
_spec = importlib.util.spec_from_file_location("_allfix_sm86_nv_parser", PARSER)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
InstructionParser = _module.InstructionParser


def serialize_operand(value):
    output = value.to_json_obj()
    mods = list(value.modifiers)
    if output["type"] == "IntIMMOperand":
        if "cNEG" in mods:
            output["constant"] = -output["constant"]
            mods.remove("cNEG")
        if "cINV" in mods:
            output["constant"] = ~output["constant"]
            mods.remove("cINV")
    output["modifiers"] = mods
    if value.sub_operands:
        output["sub_operands"] = [serialize_operand(x) for x in value.sub_operands]
    return output


def parse_sass(text: str) -> dict:
    # The upstream parser explicitly does not support the braced DEPBAR mask.
    # This grammar is the exact syntax in the public CuAssembler SM86 records.
    depbar = re.fullmatch(r"\s*(@!?U?P[0-7T]\s+)?DEPBAR(\.LE)?\s+SB([0-5]),\s*(0x[0-9a-fA-F]+)(?:,\s*\{([0-5](?:\s*,\s*[0-5])*)\})?\s*;?\s*", text)
    if depbar:
        return {"base_name": "DEPBAR", "modifiers": ["LE"] if depbar[2] else [],
                "predicate": depbar[1].strip() if depbar[1] else None,
                "operands": [{"type": "RegOperand", "reg_type": "SB", "ident": depbar[3], "modifiers": []},
                             {"type": "IntIMMOperand", "constant": int(depbar[4], 16), "modifiers": []},
                             {"type": "IntIMMOperand", "constant": sum(1 << int(x.strip()) for x in depbar[5].split(",")) if depbar[5] else 0,
                              "modifiers": []}]}
    # The pinned parser recognizes only P/N swizzle letters. SM86's ordinary
    # CLI also emits ZP (zero times the first operand plus the second). Parse
    # the surrounding instruction unchanged and replace only this exact final
    # token after serialization; malformed pairs remain explicit failures.
    swizzle = None
    if re.match(r"\s*(?:@!?U?P[0-7T]\s+)?FSWZADD(?:\.|\s)", text):
        match = re.search(r",\s*((?:PP|PN|NP|ZP){4})\s*;?\s*$", text)
        if match is None:
            raise ValueError("Invalid SM86 quad-swizzle pattern")
        swizzle = match[1]
        text = text[:match.start(1)] + "PPPPPPPP" + text[match.end(1):]
    obj = InstructionParser.parseInstruction(text.strip())
    output = obj.to_json_obj()
    output["operands"] = [serialize_operand(x) for x in obj.operands]
    if swizzle is not None:
        operand = output["operands"][-1]
        if operand.get("reg_type") != "SwzAdd" or operand.get("modifiers"):
            raise ValueError("Unexpected parsed quad-swizzle shape")
        operand["ident"] = swizzle
    return output
