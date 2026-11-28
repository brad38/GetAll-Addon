"""Normal-SASS scalar/subgroup bindings for the pinned MKW frontend.

Operand order comes from the public CuAssembler records and NVIDIA normal CLI;
the named values follow the pinned frontend's documented logical slots. Unknown
operands and modifiers are rejected rather than silently treated as defaults.
"""
from __future__ import annotations

from copy import deepcopy

from adapter_fields import Fields, number, register
from adapter_model import UncoveredEncoding, bits

OPS = set("""FADD FMUL FFMA MOV UMOV MUFU FMNMX FSEL SEL USEL FSETP ISETP UISETP
F2FP R2UR I2F UP2UR P2R FLO SGXT IABS UBREV PRMT UFLO R2P ULEA UPLOP3 HADD2
HMNMX2 HSETP2 PLOP3 LEA IADD3 UIADD3 IMAD UIMAD SHF USHF LOP3 ULOP3 F2I I2FP
FRND FSET IMNMX UPOPC POPC CS2R S2R S2UR FSWZADD SHFL VOTE VOTEU REDUX MATCH
HMMA MOVM""".split())
FLOAT_CMP = set("F LT EQ LE GT NE GE NUM NAN LTU EQU LEU GTU NEU GEU T".split())
INT_CMP = set("F LT EQ LE GT NE GE T".split())
ROUND = set("RN RM RP RZ ROUND FLOOR CEIL TRUNC".split())


def is_pred(x):
    return x.get("type") == "RegOperand" and x.get("reg_type") in ("P", "UP") and x.get("ident") != "R"


def decode_scalar(word: int, pc: int, parsed: dict):
    op = parsed["base_name"]
    if op not in OPS:
        return None
    f = Fields(word, pc, parsed)
    args = deepcopy(f.operands)
    cls = None

    def pop():
        if not args:
            raise UncoveredEncoding(f"{op}: missing operand")
        return args.pop(0)

    def src(slot):
        return f.operand(slot, pop())

    def sources(slots):
        for slot in slots:
            src(slot)

    def float_flags():
        f.flag("sat", "SAT")
        f.flag("ftz", "FTZ")
        f.choose("rnd", ROUND, "RN")

    def pred_default(name, uniform=False):
        f.put(("U" if uniform else "") + name, 7, 3)
        f.put(("U" if uniform else "") + name + "@not", 0, 1)

    def half(slot, symbol):
        operand = pop()
        if operand["type"] == "FloatIMMOperand":
            f.operand(slot, operand, float_bits=16)
            f.operand(slot + "1", pop(), float_bits=16)
            f.symbol(symbol, "H1_H0")
        else:
            swizzles = [x for x in operand.get("modifiers", []) if x in ("H1_H0", "H0_H0", "H1_H1", "F32")]
            if len(swizzles) > 1:
                raise UncoveredEncoding("Ambiguous half swizzle")
            operand["modifiers"] = [x for x in operand.get("modifiers", []) if x not in swizzles]
            f.symbol(symbol, swizzles[0] if swizzles else "H1_H0")
            f.operand(slot, operand)

    if op in ("FADD", "FMUL", "FFMA"):
        f.dst(pop())
        sources("ac" if op == "FADD" else "ab" if op == "FMUL" else "abc")
        float_flags()
        if op == "FMUL":
            f.choose("scale", ("D2", "D4", "D8", "M2", "M4", "M8"), "")
            f.flag("dnz", "DNZ")
    elif op in ("MOV", "UMOV"):
        f.dst(pop())
        source = pop()
        f.operand("b", source)
        if op == "MOV":
            cls = "mov__RR" if source["type"] == "RegOperand" and source["reg_type"] == "R" else "mov__RI" if source["type"] == "IntIMMOperand" else "cli_mov_constant"
        if args:
            if number(pop()) != 0xf:
                raise UncoveredEncoding("MOV with a partial byte mask")
    elif op == "MUFU":
        f.dst(pop()); src("b")
        f.choose("mufuop", ("COS", "SIN", "EX2", "LG2", "RCP", "RSQ", "RCP64H", "RSQ64H", "SQRT", "TANH"))
        float_flags()
    elif op in ("FMNMX", "FSEL", "SEL", "USEL", "IMNMX"):
        f.dst(pop()); sources("ab"); f.pred("Pp", pop())
        if op.startswith("F"):
            float_flags()
        if op == "IMNMX":
            f.choose("fmt", ("U32", "S32"), "S32")
    elif op in ("FSETP", "ISETP", "UISETP", "FSET"):
        if op == "FSET":
            f.dst(pop())
            if not f.flag("ofmt", "BF"):
                raise UncoveredEncoding("MKW only implements FSET.BF")
        else:
            f.pred("Pu", pop()); f.pred("Pv", pop())
        sources("ab"); f.pred("Pp", pop())
        f.choose("bop", ("AND", "OR", "XOR"))
        if op.startswith("F"):
            f.choose("fcomp", FLOAT_CMP); float_flags()
        else:
            f.choose("icmp", INT_CMP); f.choose("fmt", ("U32", "S32"), "S32")
            if f.flag("ex", "EX"):
                f.pred("Pr", pop())
    elif op in ("IADD3", "UIADD3", "IMAD", "UIMAD"):
        uniform = op.startswith("U")
        f.dst(pop())
        outputs = 0
        while args and is_pred(args[0]):
            if outputs >= (2 if "ADD3" in op else 1):
                raise UncoveredEncoding("Too many carry outputs")
            f.pred(("Pu", "Pv")[outputs], pop()); outputs += 1
        sources("abc")
        if f.flag("X", "X"):
            f.pred("Pp", pop())
            if "ADD3" in op:
                f.pred("Pq", pop())
        if "IMAD" in op:
            mode = f.choose("wide", ("WIDE", "HI"), "")
            f.choose("fmt", ("U32", "S32"), "S32")
            f.ignored("MOV", "IADD", "SHL")  # disassembler aliases of a*b+c
            cls = op.lower() + ("_" + mode.lower() if mode else "") + "__CLI"
    elif op in ("LEA", "ULEA"):
        f.dst(pop())
        if args and is_pred(args[0]):
            f.pred("Pu", pop())
        sources("ab")
        hi = f.choose("hilo", ("HI", "LO"), "LO")
        sx = f.flag("sx32", "SX32")
        if hi == "HI" and not sx:
            src("c")
        f.put("scaleU5", number(pop()), 5)
        if f.flag("X", "X"):
            # The pinned frontend has no carry-in implementation for LEA.X.
            # Preserve it and reject rather than silently dropping the carry.
            f.pred("Pp", pop())
            raise UncoveredEncoding("Pinned MKW LEA implementation does not consume X carry-in")
    elif op in ("LOP3", "ULOP3"):
        if args and is_pred(args[0]):
            f.pred("Pu", pop())
        f.dst(pop()); sources("abc")
        f.put("imm8", number(pop()), 8); f.pred("Pp", pop())
        f.ignored("LUT")
        # Mesa OpLop3: bit80 selects PAND, zero is POR; CLI omits POR.
        f.choose("pop", ("PAND", "POR", "PXOR"), "PAND" if bits(word, 80, 1) else "POR")
    elif op in ("PLOP3", "UPLOP3"):
        for role in ("Pu", "Pv", "Pp", "Pq", "Pr"):
            f.pred(role, pop())
        f.put("uimm8", number(pop()), 8); f.put("vimm8", number(pop()), 8)
        f.ignored("LUT")
    elif op in ("SHF", "USHF"):
        f.dst(pop()); sources("abc")
        f.choose("dir", ("L", "R")); f.choose("fmt", ("S32", "U32", "S64", "U64"))
        f.choose("hilo", ("HI", "LO"), "LO"); f.choose("cw", ("W", "C"), "C")
    elif op == "PRMT":
        f.dst(pop()); sources("abc")
        f.choose("pmode", ("IDX", "F4E", "B4E", "RC8", "ECL", "ECR", "RC16"), "IDX")
    elif op in ("FLO", "UFLO", "IABS", "UBREV", "UPOPC", "POPC", "SGXT", "R2UR"):
        if args and is_pred(args[0]):
            f.pred("Pu", pop())
        f.dst(pop())
        sources("ab" if op == "SGXT" else "a" if op == "R2UR" else "b")
        if op in ("FLO", "UFLO", "SGXT"):
            f.choose("fmt", ("U32", "S32"), "S32")
            f.flag("sh", "SH")
    elif op in ("P2R", "UP2UR"):
        f.dst(pop())
        mask = pop()
        if mask.get("reg_type") != ("UP" if op == "UP2UR" else "P") or mask.get("ident") != "R" or mask.get("modifiers"):
            raise UncoveredEncoding("Unknown predicate register mask")
        src("a"); f.put("Sb", number(pop()), 32)
        f.choose("insert", ("B0", "B1", "B2", "B3"), "B0")
    elif op == "R2P":
        mask = pop()
        if mask.get("reg_type") != "P" or mask.get("ident") != "R":
            raise UncoveredEncoding("Unknown R2P register mask")
        operand = pop()
        selects = [x for x in operand.get("modifiers", []) if x in ("B0", "B1", "B2", "B3")]
        operand["modifiers"] = [x for x in operand.get("modifiers", []) if x not in selects]
        f.symbol("a_bsel", selects[0] if selects else "B0"); f.operand("a", operand)
        if not args:
            raise UncoveredEncoding("R2P requires the immediate mask implemented by MKW")
        f.put("Sb", number(pop()), 32); cls = "r2p__RIR"
    elif op in ("F2FP", "F2I", "I2F", "I2FP", "FRND"):
        f.dst(pop())
        if op == "F2FP":
            sources("ab")
            f.choose("dstfmt", ("F16", "BF16"), "F16")
            f.choose("merge", ("PACK_AB", "MERGE_C", "MERGE_AB")); f.flag("relu", "RELU")
        else:
            operand = pop()
            selectors = [x for x in operand.get("modifiers", []) if x in ("B0", "B1", "B2", "B3", "H0", "H1")]
            operand["modifiers"] = [x for x in operand.get("modifiers", []) if x not in selectors]
            if selectors:
                f.symbol("bsel" if selectors[0].startswith("B") else "hsel", selectors[0])
            f.operand("b", operand)
            if op in ("I2F", "I2FP"):
                f.choose("dstfmt", ("F16", "F32", "F64"), "F32")
                f.choose("srcfmt", ("S8", "U8", "S16", "U16", "S32", "U32", "S64", "U64"), "S32")
            elif op == "F2I":
                f.choose("dstfmt", ("S8", "U8", "S16", "U16", "S32", "U32", "S64", "U64"), "S32")
                f.choose("srcfmt", ("F16", "F32", "F64"), "F32")
                f.flag("ntz", "NTZ")
            else:
                f.choose("fmt", ("F16", "F32", "F64"), "F32")
        float_flags()
    elif op in ("HADD2", "HMNMX2", "HSETP2"):
        if op == "HSETP2":
            f.pred("Pu", pop()); f.pred("Pv", pop())
        else:
            f.dst(pop())
        half("a", "iswzA"); half("b" if op == "HMNMX2" else "c", "iswzB")
        f.choose("ofmt", ("F32", "F16_V2"), "F16_V2")
        if op in ("HMNMX2", "HSETP2"):
            f.pred("Pp", pop())
        if op == "HSETP2":
            f.choose("cmp", FLOAT_CMP); f.choose("bop", ("AND", "OR", "XOR")); f.flag("h_and", "H_AND")
        f.flag("nan", "NAN"); f.flag("xorsign", "XORSIGN"); float_flags()
    elif op in ("S2R", "S2UR", "CS2R"):
        f.dst(pop()); special = pop()
        if special.get("type") != "RegOperand" or special.get("reg_type") != "SR":
            raise UncoveredEncoding("Expected a special register")
        symbol = "SRZ" if special["ident"] in ("0", "255") else "SR_" + special["ident"]
        if special.get("modifiers"):
            symbol += "." + ".".join(special["modifiers"])
        f.symbol("SRa", symbol)
        f.choose("sz", ("32", "64"), "64" if op == "CS2R" else "32")
    elif op == "FSWZADD":
        f.dst(pop()); sources("ac"); pattern = pop()
        if pattern.get("reg_type") != "SwzAdd":
            raise UncoveredEncoding("Unknown quad swizzle")
        # Mesa OpFSwzAdd writes the eight mask bits at32; the text spells pairs
        # from the most significant pair to the least significant pair.
        text = pattern["ident"]
        table = {"PP": 0, "PN": 1, "NP": 2, "ZP": 3}
        if len(text) != 8 or any(text[k:k+2] not in table for k in range(0, 8, 2)):
            raise UncoveredEncoding("Unknown quad swizzle pair")
        value = sum(table[text[k:k+2]] << (6-k) for k in range(0, 8, 2))
        if bits(word, 32, 8) != value:
            raise UncoveredEncoding("Quad swizzle text/encoding disagreement")
        f.put("npCtrl", value, 8); f.flag("ndv", "NDV"); float_flags()
    elif op == "SHFL":
        f.pred("Pu", pop()); f.dst(pop()); sources("abc")
        f.choose("shflmd", ("IDX", "UP", "DOWN", "BFLY"))
    elif op in ("VOTE", "VOTEU"):
        uniform = op == "VOTEU"
        if not is_pred(args[0]):
            f.dst(pop())
        else:
            f.put("URd" if uniform else "Rd", 63 if uniform else 255, 6 if uniform else 8)
        f.pred("Pu", pop()); f.pred("Pp", pop())
        f.choose("voteop", ("ALL", "ANY", "EQ"))
    elif op == "REDUX":
        f.dst(pop()); src("a")
        f.choose("op", ("SUM", "MIN", "MAX", "AND", "OR", "XOR")); f.choose("sz", ("U32", "S32"), "U32")
    elif op == "MATCH":
        if args and is_pred(args[0]):
            f.pred("Pu", pop())
        f.dst(pop()); src("a")
        f.choose("op", ("ANY", "ALL")); f.choose("sz", ("U32", "U64"), "U32")
    elif op == "MOVM":
        f.dst(pop()); src("a")
        f.choose("sz", ("16",)); f.choose("mode", ("MT88", "M832", "M864"))
    elif op == "HMMA":
        f.dst(pop()); sources("abc")
        f.choose("size", ("1688", "16816", "16832")); f.choose("dstfmt", ("F16", "F32"), "F32")
        f.choose("srcfmt", ("BF16", "TF32"), "F16")
    if args:
        raise UncoveredEncoding(f"{op}: unhandled trailing operands {args}")
    return f.finish(cls)
