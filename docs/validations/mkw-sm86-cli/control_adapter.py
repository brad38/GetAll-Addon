"""Closed normal-SASS bindings for control flow and synchronization."""
from adapter_fields import Fields, number, register
from adapter_model import UncoveredEncoding, bits

OPS = set("BAR BRA BREAK BRX BRXU BSSY BSYNC CALL DEPBAR ERRBAR EXIT KILL MEMBAR NOP RET WARPSYNC".split())


def decode_control(word: int, pc: int, parsed: dict):
    op = parsed["base_name"]
    if op not in OPS:
        return None
    f = Fields(word, pc, parsed)
    args = list(f.operands)

    def pop():
        if not args:
            raise UncoveredEncoding(f"{op}: missing operand")
        return args.pop(0)

    def psrc():
        if args and args[0].get("reg_type") in ("P", "UP"):
            operand = pop()
            if operand["reg_type"] != "P":
                raise UncoveredEncoding("Secondary uniform condition requires a separate lowering proof")
            f.pred("Pp", operand)
        else:
            f.put("Pp", 7, 3); f.put("Pp@not", 0, 1)

    def relative(name, target, width=48, absolute=True):
        delta = target - pc - 16 if absolute else target
        if delta % 4 or not -(1 << (width-1)) <= delta // 4 < 1 << (width-1):
            raise UncoveredEncoding("Control target cannot be represented by the consumed signed word displacement")
        f.put(name, delta // 4, width)

    if op == "BRA":
        psrc(); relative("sImm", number(pop()))
    elif op in ("BRX", "BRXU"):
        psrc()
        kind = "UR" if op == "BRXU" else "R"
        f.reg("URa" if kind == "UR" else "Ra", pop(), (kind,))
        relative("UR_offset" if kind == "UR" else "Ra_offset", number(pop()) if args else 0, absolute=False)
    elif op == "CALL":
        if f.choose("addr", ("REL", "ABS")) != "REL" or f.choose("depth", ("NOINC", "INC")) != "NOINC":
            raise UncoveredEncoding("Pinned MKW only lowers CALL.REL.NOINC")
        relative("Sa", number(pop()))
    elif op == "RET":
        if f.choose("addr", ("REL", "ABS")) != "REL" or f.choose("depth", ("NODEC", "DEC")) != "NODEC":
            raise UncoveredEncoding("Pinned MKW only lowers RET.REL.NODEC")
        f.reg("Ra", pop(), ("R",)); relative("Ra_offset", number(pop()))
    elif op in ("EXIT", "KILL"):
        psrc()
    elif op in ("BREAK", "BSYNC", "BSSY"):
        psrc()
        barrier = pop()
        if barrier.get("type") != "RegOperand" or barrier.get("reg_type") != "B" or barrier.get("modifiers") or not 0 <= int(barrier["ident"]) < 16:
            raise UncoveredEncoding("Unknown convergence barrier operand")
        f.put("barrier", int(barrier["ident"]), 4)
        if op == "BSSY":
            relative("sImm", number(pop()), 30)
    elif op == "BAR":
        if f.choose("barmode", ("SYNC", "ARV", "RED", "SCAN")) != "SYNC":
            raise UncoveredEncoding("Only BAR.SYNC is lowered by the pinned frontend")
        f.put("Sb", number(pop()), 32)
        f.flag("defer", "DEFER_BLOCKING")
    elif op == "MEMBAR":
        if f.choose("mode", ("SC",)) != "SC":
            raise UncoveredEncoding("Unknown memory barrier ordering")
        f.choose("sco", ("CTA", "GPU", "SYS", "VC"))
    elif op == "DEPBAR":
        f.flag("le", "LE")
        scoreboard = pop()
        if scoreboard.get("reg_type") != "SB" or scoreboard.get("modifiers") or not 0 <= int(scoreboard["ident"]) < 6:
            raise UncoveredEncoding("Unknown dependency scoreboard")
        f.put("scoreboard", int(scoreboard["ident"]), 3)
        f.put("threshold", number(pop()), 6)
        if args:
            f.put("scoreboard_mask", number(pop()), 6)
    elif op == "WARPSYNC":
        f.operand("b", pop())
    elif op not in ("NOP", "ERRBAR"):
        raise AssertionError("Unimplemented control opcode")
    if args:
        raise UncoveredEncoding(f"{op}: trailing operands {args}")
    return f.finish()
