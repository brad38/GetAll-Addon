"""Closed helpers for the experimental normal-CLI decoder adapter.

Input dictionaries come from the pinned MIT nv_isa_solver text parser. Field
names are the pinned MKW consumer's interface; they are not an NVIDIA SIDL model.
No caller may treat a failed/unknown parse as an end-of-program marker.
"""
from __future__ import annotations

import re
import struct
from types import SimpleNamespace

from adapter_model import TracedInsn, UncoveredEncoding, field


def number(operand: dict) -> int:
    if operand.get("type") != "IntIMMOperand":
        raise UncoveredEncoding(f"Expected an integer operand: {operand}")
    return operand["constant"]


def register(operand: dict, kinds=("R", "UR")) -> tuple[str, int]:
    if operand.get("type") != "RegOperand" or operand.get("reg_type") not in kinds:
        raise UncoveredEncoding(f"Unexpected register operand: {operand}")
    kind, ident = operand["reg_type"], operand["ident"]
    value = {("R", "Z"): 255, ("UR", "Z"): 63, ("P", "T"): 7, ("UP", "T"): 7}.get((kind, ident))
    value = int(ident) if value is None else value
    limit = 255 if kind == "R" else 63 if kind == "UR" else 7
    if not 0 <= value <= limit:
        raise UncoveredEncoding("Register index is out of range")
    return kind, value


class Fields:
    def __init__(self, word: int, pc: int, parsed: dict):
        self.word, self.pc, self.parsed = word, pc, parsed
        self.op = parsed["base_name"]
        self.mods = list(parsed["modifiers"])
        self.operands = parsed["operands"]
        self.fields = {}
        guard = parsed.get("predicate")
        if guard is None:
            self.put("Pg", 7, 3)
            self.put("Pg@not", 0, 1)
        else:
            match = re.fullmatch(r"@(!?)(U?P)([0-7T])", guard)
            if match is None:
                raise UncoveredEncoding(f"Unknown execution predicate {guard}")
            prefix = "UPg" if match[2] == "UP" else "Pg"
            self.put(prefix, 7 if match[3] == "T" else int(match[3]), 3)
            self.put(prefix + "@not", int(bool(match[1])), 1)

    def put(self, name: str, value: int, width=32, symbol: str | None = None):
        self.fields[name] = field(name, value & ((1 << width) - 1), width, symbol)
        return value

    def symbol(self, name: str, value: str):
        self.fields[name] = field(name, 0, 1, value)
        return value

    def flag(self, name: str, modifier: str):
        if modifier in self.mods:
            self.mods.remove(modifier)
            self.symbol(name, modifier)
            return True
        return False

    def choose(self, name: str, choices, default: str | None = None):
        found = [x for x in self.mods if x in choices]
        if len(found) > 1:
            raise UncoveredEncoding(f"{self.op}: ambiguous {name}: {found}")
        value = found[0] if found else default
        if found:
            self.mods.remove(found[0])
        if value is not None:
            self.symbol(name, value)
        return value

    def ignored(self, *modifiers):
        """Only callers documenting an irrelevant scheduling/encoding hint use this."""
        self.mods[:] = [x for x in self.mods if x not in modifiers]

    def reg(self, name: str, operand: dict, kinds=("R", "UR")):
        kind, value = register(operand, kinds)
        if operand.get("modifiers"):
            raise UncoveredEncoding(f"{self.op}: modified destination {operand}")
        self.put(name, value, 8 if kind == "R" else 6 if kind == "UR" else 3)
        return value

    def dst(self, operand: dict):
        kind, _ = register(operand)
        return self.reg("URd" if kind == "UR" else "Rd", operand)

    def pred(self, name: str, operand: dict):
        kind, value = register(operand, ("P", "UP"))
        modifiers = operand.get("modifiers", [])
        if any(x != "cNOT" for x in modifiers):
            raise UncoveredEncoding(f"Unknown predicate modifier: {modifiers}")
        name = ("U" + name) if kind == "UP" and not name.startswith("U") else name
        self.put(name, value, 3)
        self.put(name + "@not", int("cNOT" in modifiers), 1)
        return name

    def operand(self, slot: str, operand: dict, *, float_bits=32):
        kind = operand["type"]
        mods = operand.get("modifiers", [])
        if kind == "RegOperand":
            reg_kind, value = register(operand)
            name = reg_kind + slot
            self.put(name, value, 8 if reg_kind == "R" else 6)
        elif kind == "IntIMMOperand":
            name = "S" + slot
            self.put(name, operand["constant"], 32)
        elif kind == "FloatIMMOperand":
            name = "S" + slot
            text = operand["constant"]
            if re.fullmatch(r"-?0[fF][0-9a-fA-F]+", text):
                negative = text.startswith("-")
                value = int(text.lstrip("-")[2:], 16)
                if negative:
                    value ^= 1 << (float_bits - 1)
            else:
                code = "e" if float_bits == 16 else "f"
                value = int.from_bytes(struct.pack("<" + code, float(text)), "little")
            self.put(name, value, float_bits)
        elif kind == "ConstantMemOperand" and not operand.get("cx"):
            bank_op, address = operand["sub_operands"]
            bank = number(bank_op)
            if address["type"] != "AddressOperand" or address.get("modifiers") or len(address["sub_operands"]) != 1:
                raise UncoveredEncoding("ALU constant address must be a fixed bank and offset")
            byte = number(address["sub_operands"][0])
            if byte < 0 or byte % 4 or not 0 <= bank < 32:
                raise UncoveredEncoding("Unaligned/out-of-range constant operand")
            name = "S" + slot
            full = "ConstBankAddress_" + name + "_bank"
            value = field(full, 0, 1)
            value.slot_values = [(SimpleNamespace(width=5), bank), (SimpleNamespace(width=16), byte // 4)]
            self.fields[full] = value
        else:
            raise UncoveredEncoding(f"Unsupported source operand {operand}")
        for modifier in mods:
            if modifier == "reuse":
                continue  # register operand cache hint, no value-semantic effect
            flags = {"cNEG": "negate", "cABS": "absolute", "cINV": "invert"}
            if modifier not in flags:
                raise UncoveredEncoding(f"{self.op}: unknown operand modifier {modifier}")
            self.put(name + "@" + flags[modifier], 1, 1)
        return name

    def finish(self, cls: str | None = None) -> TracedInsn:
        if self.mods:
            raise UncoveredEncoding(f"{self.op}: unhandled modifiers {self.mods}")
        d = SimpleNamespace(mnemonic=self.op, cls=SimpleNamespace(name=cls or "cli_" + self.op.lower()),
                            values=list(self.fields.values()), status="ok")
        return TracedInsn(self.pc, self.word, d, self.fields)
