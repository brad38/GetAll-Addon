"""Bounded correction for LEA/ULEA carry and shifted-operand modifiers.

Semantics are the MIT Mesa 26.3.0 ir.rs Foldable implementations for OpLea and
OpLeaX, cross-checked with sm70_encode.rs and normal nvdisasm text. Source pins
are recorded in references/mesa-lea-sources.json. Original MKW files stay intact.
"""
from __future__ import annotations

import hashlib

from adapter_fields import Fields, number
from adapter_model import CONSUMER_ROOT, UncoveredEncoding

ORIGINAL_ALU_SHA = "6b2782ae58bcbd3743334c3bb37f5a86ba8bff923def70cc47e080bda6d1d97c"


def decode_lea(word: int, pc: int, parsed: dict):
    if parsed["base_name"] not in ("LEA", "ULEA"):
        return None
    f = Fields(word, pc, parsed)
    args = list(f.operands)

    def pop():
        if not args:
            raise UncoveredEncoding(f"{f.op}: missing operand")
        return args.pop(0)

    f.dst(pop())
    if args and args[0].get("reg_type") in ("P", "UP"):
        f.pred("Pu", pop())
    for slot in "ab":
        f.operand(slot, pop())
    hi = f.choose("hilo", ("HI", "LO"), "LO")
    sx = f.flag("sx32", "SX32")
    if sx and hi != "HI":
        raise UncoveredEncoding("LEA.SX32 requires the HI result")
    if hi == "HI" and not sx:
        f.operand("c", pop())
    shift = number(pop())
    if not 0 <= shift <= 31:
        raise UncoveredEncoding("LEA shift outside five-bit range")
    f.put("scaleU5", shift, 5)
    x = f.flag("X", "X")
    if x:
        f.pred("Pp", pop())
    if args:
        raise UncoveredEncoding("Unexpected LEA operands")
    for slot in "abc":
        name = next((n for n in ("R" + slot, "UR" + slot, "S" + slot) if n in f.fields), "S" + slot)
        modifiers = [n.rsplit("@", 1)[1] for n in f.fields if n.startswith(name + "@")]
        allowed = {"invert"} if x else {"negate"}
        if slot == "c":
            allowed = set()
        if any(m not in allowed for m in modifiers):
            raise UncoveredEncoding(f"LEA: unsupported {slot} modifiers {modifiers}")
    return f.finish()


def emit_lea(self, i) -> str:
    """Emit 32-bit folding and predicate carry exactly, including aliasing."""
    from glsl.common import PT, Unsupported, pred
    shift = i.v("scaleU5")
    if not 0 <= shift <= 31:
        raise Unsupported("LEA shift outside five-bit range")
    is_x = i.sym("X") == "X"
    is_high = i.sym("hilo") == "HI"
    uniform = i.has("URd")
    prefix = "U" if uniform else ""
    a, b = self.src_u(i, "a"), self.src_u(i, "b")
    aname, bname = self.operand(i, "a"), self.operand(i, "b")
    if is_high:
        c = f"uint(int({a}) >> 31)" if i.sym("sx32") == "SX32" else self.src_u(i, "c")
        shifted = f"uint(((uint64_t({c}) << 32u) | uint64_t({a})) >> {32 - shift}u)"
    else:
        shifted = f"({a} << {shift}u)"
    out = [f"uint lea_shifted = {shifted};", f"uint lea_b = {b};", "bool lea_negcarry = false;"]
    for name, variable in ((aname, "lea_shifted"), (bname, "lea_b")):
        negate, invert = i.v(name + "@negate", 0), i.v(name + "@invert", 0)
        if (negate and is_x) or (invert and not is_x) or i.v(name + "@absolute", 0):
            raise Unsupported("LEA modifier disagrees with the carry mode")
        if invert:
            out.append(f"{variable} = ~{variable};")
        if negate:
            # Mesa includes overflow from two's-complement negation of zero.
            out.append(f"lea_negcarry = lea_negcarry || ({variable} == 0u);")
            out.append(f"{variable} = 0u - {variable};")
    carry = (pred(i.v(prefix + "Pp"), i.v(prefix + "Pp@not", 0), uniform)
             if is_x else "false")
    out += [f"bool lea_carry = {carry};",
            "uint64_t lea_sum = uint64_t(lea_shifted) + uint64_t(lea_b) + uint64_t(lea_carry ? 1u : 0u);",
            self.dst(i, "uint(lea_sum)")]
    output_predicate = i.v(prefix + "Pu", PT)
    if output_predicate != PT:
        out.append(f"{'up' if uniform else 'p'}{output_predicate} = lea_negcarry || ((lea_sum >> 32u) != uint64_t(0));")
    return "{ " + " ".join(out) + " }"


def install():
    """Apply only to the fixed upstream consumer, never rewrite its source."""
    # translate.py imports glsl before program.Decoder. Defer this import until
    # the Decoder is instantiated, after the model and Builder are complete.
    from glsl.core import Builder
    path = CONSUMER_ROOT / "glsl/alu.py"
    if hashlib.sha256(path.read_bytes()).hexdigest() != ORIGINAL_ALU_SHA:
        raise ValueError("LEA overlay requires the pinned original MKW consumer")
    if Builder.lea is emit_lea and Builder.ulea is emit_lea:
        return
    if (Builder.lea.__module__ != "glsl.alu" or Builder.lea.__name__ != "lea"
            or Builder.ulea.__module__ != "glsl.alu" or Builder.ulea.__name__ != "ulea"):
        raise ValueError("Unexpected existing LEA override")
    Builder.lea = emit_lea
    Builder.ulea = emit_lea
