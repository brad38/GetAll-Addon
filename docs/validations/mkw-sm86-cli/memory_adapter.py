"""Closed address and attribute bindings for the pinned MKW consumer.

Scalar constant operands use word offsets; LDC/ULDC use byte offsets. The
different units are intentional and are consumed differently by upstream.
Class suffixes below are compatibility tags for upstream's address selectors,
not assertions that an NVIDIA internal instruction class was recovered.
"""
from __future__ import annotations

from copy import deepcopy
from types import SimpleNamespace

from adapter_fields import Fields, number, register
from adapter_model import UncoveredEncoding, field

OPS = set("LDG STG LDC ULDC LDS STS LDL STL ATOMG RED LDSM ISBERD ISBEWR ALD AST IPA".split())


def address_parts(operand):
    if operand.get("type") != "AddressOperand" or operand.get("modifiers"):
        raise UncoveredEncoding("Only an ordinary, unmodified address is supported")
    r, ur, off, stride, wide = None, None, 0, "X1", False
    seen_imm = False
    for item in operand["sub_operands"]:
        if item["type"] == "IntIMMOperand":
            if seen_imm or item.get("modifiers"):
                raise UncoveredEncoding("Ambiguous address displacement")
            off, seen_imm = number(item), True
        elif item["type"] == "RegOperand":
            kind, value = register(item)
            modifiers = list(item.get("modifiers", []))
            if kind == "R":
                if r is not None:
                    raise UncoveredEncoding("Two vector address registers")
                r = value
                if "64" in modifiers:
                    wide = True; modifiers.remove("64")
                if "U32" in modifiers:
                    if wide:
                        raise UncoveredEncoding("Conflicting vector address widths")
                    modifiers.remove("U32")
                choices = [m for m in modifiers if m in ("X1", "X4", "X8", "X16")]
                if len(choices) > 1:
                    raise UncoveredEncoding("Two address strides")
                if choices:
                    stride = choices[0]; modifiers.remove(stride)
            else:
                if ur is not None:
                    raise UncoveredEncoding("Two uniform address registers")
                ur = value
            if modifiers:
                raise UncoveredEncoding(f"Unhandled address modifiers {modifiers}")
        else:
            raise UncoveredEncoding("Unhandled address component")
    if not -(1 << 31) <= off < (1 << 31):
        raise UncoveredEncoding("Address displacement exceeds the consumer's32-bit model")
    return 255 if r is None else r, ur, off, stride, wide


def decode_memory(word: int, pc: int, parsed: dict):
    op = parsed["base_name"]
    if op not in OPS:
        return None
    f = Fields(word, pc, parsed)
    args = deepcopy(f.operands)
    cls = "cli_" + op.lower()

    def pop():
        if not args:
            raise UncoveredEncoding(f"{op}: missing operand")
        return args.pop(0)

    def address(operand, *, global_space=False, shared=False, uniform_allowed=True):
        # Descriptor operands have separate semantics. The consumer does not
        # implement descriptor validation; never reinterpret one as a pointer.
        r, ur, off, stride, wide = address_parts(operand)
        if ur is not None and not uniform_allowed:
            raise UncoveredEncoding(f"{op}: consumer does not read a uniform address component")
        if global_space and ur is not None and wide and r != 255:
            raise UncoveredEncoding("Consumer does not lower an independent64-bit vector offset plus uniform base")
        if wide and not global_space:
            raise UncoveredEncoding("A64-bit vector address is not consumed in this address space")
        if stride != "X1" and not shared:
            raise UncoveredEncoding("Address stride is unsupported in this address space")
        f.put("Ra", r, 8); f.put("Ra_offset", off, 32)
        if ur is not None:
            f.put("Ra_URb", ur, 6)
        f.symbol("stride", stride)
        return r, ur, off, wide

    def mem_modifiers(atomic=False):
        choices = ("U32", "32", "S32", "U64", "64", "S64", "F32", "F64", "F16x2") if atomic else ("U8", "S8", "U16", "S16", "32", "64", "128")
        f.choose("sz", choices, "U32" if atomic else "32")
        extended = f.flag("extended", "E")
        # Cache hints are value-independent. Strong/volatile ordering has no
        # proved lowering in this consumer and must not be silently discarded.
        f.choose("cache", ("EF", "EL", "LU", "EU", "NA", "LTC64B", "LTC128B"), "")
        ordering = f.choose("ordering", ("CONSTANT", "STRONG", "WEAK", "VOLATILE"), "WEAK")
        scope = f.choose("scope", ("CTA", "SM", "GPU", "SYS"), "")
        if ordering in ("STRONG", "VOLATILE") or scope:
            raise UncoveredEncoding("Ordered/scoped memory access has no proved lowering")
        if ordering == "CONSTANT" and op != "LDG":
            raise UncoveredEncoding("Immutable memory hint is valid only for the proved global load")
        return extended

    if op in ("LDC", "ULDC"):
        f.dst(pop())
        cb = pop()
        if cb.get("type") != "ConstantMemOperand" or cb.get("cx") or cb.get("modifiers"):
            raise UncoveredEncoding("Only a fixed constant-buffer bank is supported")
        bank, addr = cb["sub_operands"]
        bank = number(bank)
        r, ur, off, stride, wide = address_parts(addr)
        if not 0 <= bank < 32 or not 0 <= off < 1 << 16 or stride != "X1" or wide:
            raise UncoveredEncoding("Constant-buffer address outside the fixed bank/byte-offset contract")
        if op == "ULDC":
            if r != 255:
                raise UncoveredEncoding("ULDC has a vector address")
            if ur is not None:
                f.put("URa", ur, 6)
        else:
            if ur is not None:
                raise UncoveredEncoding("LDC uniform handle/address is not implemented by the consumer")
            f.put("Ra", r, 8)
        name = "ConstBankAddress_byte_offset"
        value = field(name, 0, 1)
        value.slot_values = [(SimpleNamespace(width=5), bank), (SimpleNamespace(width=16), off)]
        f.fields[name] = value
        f.choose("sz", ("U8", "S8", "U16", "S16", "32", "64"), "32")
    elif op in ("LDG", "STG", "LDS", "STS", "LDL", "STL", "LDSM", "ATOMG", "RED"):
        atomic = op in ("ATOMG", "RED")
        global_space = op in ("LDG", "STG", "ATOMG", "RED")
        if op == "ATOMG":
            f.pred("Pu", pop()); f.dst(pop())
        elif op in ("LDG", "LDS", "LDL", "LDSM"):
            f.dst(pop())
        r, ur, off, wide = address(pop(), global_space=global_space, shared=op in ("LDS", "STS"),
                                   uniform_allowed=op not in ("LDL", "STL", "LDSM"))
        if op in ("STG", "STS", "STL", "ATOMG", "RED"):
            f.operand("b", pop())
        if op == "LDSM":
            f.choose("sz", ("16",)); f.choose("mode", ("M88", "MT88", "M816", "M832")); f.choose("num", ("1", "2", "4"), "1")
        else:
            extended = mem_modifiers(atomic)
        if atomic:
            f.choose("op", ("ADD", "MIN", "MAX", "INC", "DEC", "AND", "OR", "XOR", "EXCH", "CAS"))
        if args and args[0].get("reg_type") in ("P", "UP"):
            # A read-enable/fault condition requires extra lowering. It cannot
            # be confused with the instruction's execution predicate.
            raise UncoveredEncoding("Memory instruction has an additional predicate operand")
        if global_space:
            if ur is None and not (wide or extended):
                raise UncoveredEncoding("A32-bit global pointer has no proved lowering; it cannot be promoted to a register pair")
            cls += "_sImmOffset" + ("Ra32" if not wide and ur is not None else "Ra64")
        elif op in ("LDL", "STL"):
            cls += "_sImmOffset"
    elif op in ("ALD", "AST"):
        if op == "ALD":
            f.dst(pop())
        attribute = pop()
        if attribute.get("type") != "AttributeOperand" or attribute.get("modifiers") or len(attribute["sub_operands"]) != 1:
            raise UncoveredEncoding("Expected ordinary attribute addressing")
        r, ur, off, stride, wide = address_parts(attribute["sub_operands"][0])
        if ur is not None or stride != "X1" or wide or not 0 <= off < 0x400:
            raise UncoveredEncoding("Unknown attribute address mode")
        f.put("Ra", r, 8); f.put("Ra_offset", off, 10)
        if op == "AST":
            f.operand("b", pop())
        f.choose("sz", ("32", "64", "96", "128"), "32")
        f.choose("io", ("O", "I"), "I" if op == "ALD" else "O")
    elif op == "IPA":
        f.dst(pop()); attribute = pop()
        if attribute.get("type") != "AttributeOperand" or attribute.get("modifiers"):
            raise UncoveredEncoding("IPA attribute form is not supported")
        r, ur, off, stride, wide = address_parts(attribute["sub_operands"][0])
        if r != 255 or stride != "X1" or wide or off % 4 or not 0 <= off < 0x400:
            raise UncoveredEncoding("IPA requires a word-aligned constant/uniform attribute address")
        if ur is None:
            f.put("attr", off // 4, 8)
        else:
            f.put("URa", ur, 6); f.put("URa_offset", off // 4, 8)
        mode = f.choose("ipaop", ("PASS", "CONSTANT", "MUL", "STATE"), "PASS")
        f.flag("sat", "SAT")
        if args:
            if mode != "MUL":
                raise UncoveredEncoding("An offset/interpolation operand is not consumed by this frontend mode")
            f.operand("b", pop())
        elif mode == "MUL":
            raise UncoveredEncoding("IPA.MUL multiplier is absent")
    elif op in ("ISBERD", "ISBEWR"):
        if op == "ISBERD":
            f.dst(pop())
        r, ur, off, stride, wide = address_parts(pop())
        if ur is not None or stride != "X1" or wide or not 0 <= off < 1 << 16:
            raise UncoveredEncoding("Unknown ISBE address form")
        f.put("Ra", r, 8); f.put("Ra_offset", off, 16)
        if op == "ISBEWR":
            f.operand("b", pop())
        f.choose("sz", ("8", "U8", "16", "U16", "32"), "8")
        f.choose("base", ("ATTR", "PATCH", "PRIM", "MAP"), "MAP")
        f.choose("io", ("I", "O"), "I"); f.flag("skew", "SKEW")
    if args:
        raise UncoveredEncoding(f"{op}: trailing operands {args}")
    return f.finish(cls)
