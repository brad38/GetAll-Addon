"""Closed SM86 texture/image adapter for the pinned MKW GLSL consumer.

Only constant-buffer handles supported by that consumer are admitted. The input
is normal nvdisasm text parsed by cli_parse, never a private instruction table.
Register/handle layouts are cross-checked against public Mesa/CuAssembler and
normal CLI probes in probe_texture_adapter.py. Unknown semantics fail closed.
"""
from __future__ import annotations

from adapter_fields import Fields, number, register
from adapter_model import TracedInsn, UncoveredEncoding


OPCODES = {"TEX": 0xB60, "TLD": 0xB66, "TLD4": 0xB63, "TMML": 0xB69,
           "TXQ": 0xB6F, "SULD": 0xB97, "SUST": 0xB9B,
           "SUATOM": 0x593, "SURED": 0x59F}
TEXTURE_DIMS = {("D", "1"): "1D", ("D", "2"): "2D", ("D", "3"): "3D",
                ("SNOWFLAKE", "CUBE"): "CUBE", ("ARRAY_D", "1D"): "ARRAY_1D",
                ("ARRAY_D", "2D"): "ARRAY_2D", ("ARRAY_D", "CUBE"): "ARRAY_CUBE"}
IMAGE_DIMS = {"1D", "1D_BUFFER", "1D_ARRAY", "2D", "2D_ARRAY", "3D"}


def _int(operand: dict, maximum: int, title: str) -> int:
    value = number(operand)
    if operand.get("modifiers") or not 0 <= value <= maximum:
        raise UncoveredEncoding(f"{title}: modified or out-of-range integer")
    return value


def _source(f: Fields, name: str, operand: dict) -> int:
    _, value = register(operand, ("R",))
    if any(x != "reuse" for x in operand.get("modifiers", [])):
        raise UncoveredEncoding(f"{f.op}: modified texture register")
    return f.put(name, value, 8)


def _handle(f: Fields, operands: list[dict]):
    if len(operands) != 2:
        raise UncoveredEncoding(f"{f.op}: requires a fixed bank and handle index")
    f.put("bank5", _int(operands[0], 31, "texture bank"), 5)
    # Mesa set_tex_cb_ref stores a byte offset divided by four. nvdisasm
    # already prints this 14-bit word index, as the public CuAssembler records
    # confirm; multiplying/dividing the printed value again would be wrong.
    f.put("tsPtrIdx", _int(operands[1], 0x3FFF, "texture handle index"), 14)


def _predicate(f: Fields, operands: list[dict]) -> list[dict]:
    if operands and operands[0].get("reg_type") == "P":
        f.pred("Pu", operands[0])
        operands = operands[1:]
        if f.fields["Pu"].value != 7 or f.fields["Pu@not"].value:
            raise UncoveredEncoding(f"{f.op}: consumer cannot produce texture fault predicates")
    else:
        f.put("Pu", 7, 3)
    return operands


def _cache_hints(f: Fields):
    # Eviction priority is a cache policy, and NODEP is dependency scheduling.
    # Neither changes sampled values. They are retained in the original word.
    f.ignored("EF", "EL", "LU", "EU", "NA", "NODEP")


def _image(f: Fields):
    operands = _predicate(f, list(f.operands))
    if f.op in ("SULD", "SUATOM"):
        if not operands:
            raise UncoveredEncoding(f"{f.op}: missing destination")
        f.reg("Rd", operands.pop(0), ("R",))
    if not operands:
        raise UncoveredEncoding(f"{f.op}: missing image coordinates")
    address = operands.pop(0)
    if (address.get("type") != "AddressOperand" or address.get("modifiers")
            or len(address.get("sub_operands", [])) != 1):
        raise UncoveredEncoding(f"{f.op}: image coordinates must be an unscaled register")
    _source(f, "Ra", address["sub_operands"][0])
    if f.op != "SULD":
        if not operands:
            raise UncoveredEncoding(f"{f.op}: missing image data")
        _source(f, "Rb", operands.pop(0))
    _handle(f, operands)
    dim = f.choose("dim", IMAGE_DIMS)
    if dim is None or dim == "1D_BUFFER":
        raise UncoveredEncoding(f"{f.op}: unsupported image dimension {dim}")
    clamp = f.choose("clamp", ("IGN", "TRAP", "CLAMP", "ZERO"), "")
    if clamp not in ("", "IGN"):
        raise UncoveredEncoding(f"{f.op}: consumer cannot reproduce {clamp} bounds handling")
    if f.op in ("SULD", "SUST"):
        # The original consumer handles formatted floating-point images only;
        # binary-address .D.BA operations cannot be silently mapped to those.
        if "P" not in f.mods:
            raise UncoveredEncoding(f"{f.op}: requires formatted .P image access")
        f.mods.remove("P")
        f.choose("rgba", ("R", "RG", "RGBA"), "RGBA")
    else:
        if "D" not in f.mods:
            raise UncoveredEncoding(f"{f.op}: requires integer .D image access")
        f.mods.remove("D")
        f.choose("op", ("ADD", "MIN", "MAX", "AND", "OR", "XOR"))
        f.choose("sz", ("U32", "32"), "U32")
        if not f.fields.get("op"):
            raise UncoveredEncoding(f"{f.op}: unsupported atomic operation")
    # Strong ordering, signed/64-bit atomics, byte-addressing, and unknown
    # modes remain unconsumed and are rejected by finish, never discarded.
    _cache_hints(f)
    return f.finish()


def decode_texture(word: int, pc: int, parsed: dict) -> TracedInsn | None:
    op = parsed["base_name"]
    if op not in OPCODES:
        return None
    if word & 0xFFF != OPCODES[op]:
        raise UncoveredEncoding(f"{op}: consumer requires a constant-buffer handle form")
    f = Fields(word, pc, parsed)
    if op in ("SULD", "SUST", "SUATOM", "SURED"):
        return _image(f)
    operands = _predicate(f, list(f.operands))
    if len(operands) < 6:
        raise UncoveredEncoding(f"{op}: missing texture operands")
    # SASS lists the second output register first (Rd2, Rd).
    f.reg("Rd2", operands.pop(0), ("R",))
    f.reg("Rd", operands.pop(0), ("R",))
    _source(f, "Ra", operands.pop(0))
    if op == "TXQ":
        query = operands.pop(0)
        if (query.get("type") != "RegOperand" or query.get("reg_type") != "TEX"
                or query.get("ident") != "HEADER_DIMENSION" or query.get("modifiers")):
            raise UncoveredEncoding("TXQ: only TEX_HEADER_DIMENSION is translated")
        f.symbol("query", "TEX_HEADER_DIMENSION")
        if len(operands) != 3:
            raise UncoveredEncoding("TXQ: expected bank, handle index and result mask")
        f.put("wmsk", _int(operands.pop(), 15, "texture component mask"), 4)
        _handle(f, operands)
    else:
        if operands[0].get("reg_type") == "R":
            _source(f, "Rb", operands.pop(0))
        else:
            f.put("Rb", 255, 8)  # normal CLI omits an unused RZ group
        if len(operands) not in (3, 4):
            raise UncoveredEncoding(f"{op}: expected bank, handle, dimension and optional mask")
        mask = _int(operands.pop(), 15, "texture component mask") if len(operands) == 4 else 15
        dimension = operands.pop()
        dim = TEXTURE_DIMS.get((dimension.get("reg_type"), dimension.get("ident")))
        if dim is None or dimension.get("modifiers"):
            raise UncoveredEncoding(f"{op}: unknown dimension operand {dimension}")
        f.symbol("paramA", dim)
        f.put("wmsk", mask, 4)
        _handle(f, operands)
        if op == "TMML":
            # Mesa OpTmml and the CLI call the query .LOD. Other query modes
            # have no matching operation in the pinned textureQueryLod emitter.
            if "LOD" not in f.mods:
                raise UncoveredEncoding("TMML: expected .LOD query")
            f.mods.remove("LOD")
        else:
            f.flag("scr", "SCR")
            f.flag("aoffi", "AOFFI")
            f.flag("dc" if op != "TLD" else "ms", "DC" if op != "TLD" else "MS")
            if "F16" in f.mods:
                f.mods.remove("F16")
                if "RN" not in f.mods:
                    raise UncoveredEncoding(f"{op}: only round-to-nearest half results are translated")
                f.mods.remove("RN")
                f.put("f16rm", 1, 2)
            else:
                f.put("f16rm", 0, 2)
            if op == "TLD4":
                f.choose("comp", ("R", "G", "B", "A"), "R")
                f.choose("toff", ("PTP",), "notoff")
                f.symbol("lodlc", "nolodlc")
            else:
                f.choose("lodlc", ("LL", "LZ", "LB"), "nolodlc")
        # NDV asserts nondivergent coordinates; GLSL derivatives have the same
        # values under that assertion. Do not discard .CL or other lod modes.
        f.ignored("NDV")
    _cache_hints(f)
    return f.finish()
