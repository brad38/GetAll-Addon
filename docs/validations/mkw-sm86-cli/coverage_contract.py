"""Read-only source census; availability is deliberately not decoder support."""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent


def cu_records():
    path = ROOT / "references/CuAsm/DefaultInsAsmRepos.sm_86.txt"
    data = path.read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    if blob != "a1465fd953942fc77c1b0a1a8c37ebe6b91b2b68":
        raise ValueError("CuAssembler source pin changed")
    tree = ast.parse(data.decode(), mode="eval").body
    if not isinstance(tree, ast.Call) or not isinstance(tree.func, ast.Name) or tree.func.id != "CuInsAssemblerRepos":
        raise ValueError("Unexpected repository expression")
    result = {}
    for key, value in zip(tree.args[0].keys, tree.args[0].values):
        if not isinstance(value, ast.Call) or value.func.id != "CuInsAssembler":
            raise ValueError("Unexpected instruction expression")
        attrs = {ast.literal_eval(k): v for k, v in zip(value.args[1].keys, value.args[1].values)}
        result[ast.literal_eval(key)] = ast.literal_eval(attrs["InsRecords"])
    return result


def source_contract():
    source = ROOT / "upstream/sm86/translate"
    opcodes, accesses, classes = {}, [], []
    for path in sorted(source.glob("**/*.py")):
        tree = ast.parse(path.read_text())
        for fn in ast.walk(tree):
            if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            op_alias = any(isinstance(x, ast.Assign) and isinstance(x.value, ast.Attribute)
                           and x.value.attr == "op" and any(isinstance(y, ast.Name) and y.id == "op" for y in x.targets)
                           for x in ast.walk(fn))
            for node in ast.walk(fn):
                if not hasattr(node, "lineno"):
                    continue
                location = {"file": str(path.relative_to(ROOT)), "function": fn.name, "line": node.lineno}
                if isinstance(node, ast.Compare) and (
                    isinstance(node.left, ast.Attribute) and node.left.attr == "op" or
                    op_alias and isinstance(node.left, ast.Name) and node.left.id == "op"
                ):
                    for expr in node.comparators:
                        for v in ast.walk(expr):
                            if isinstance(v, ast.Constant) and isinstance(v.value, str) and v.value.isupper():
                                opcodes.setdefault(v.value, []).append(location)
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.args:
                    if node.func.attr in ("v", "sv", "sym", "has"):
                        arg = node.args[0]
                        accesses.append({**location, "access": node.func.attr,
                                         "expression": ast.unparse(arg),
                                         "literal": arg.value if isinstance(arg, ast.Constant) else None})
                if isinstance(node, (ast.Compare, ast.Call)) and any(
                    isinstance(x, ast.Attribute) and x.attr == "cls" for x in ast.walk(node)
                ):
                    classes.append({**location, "expression": ast.unparse(node)})
    if len(opcodes) != 99:
        raise AssertionError(f"Pinned frontend mnemonic census changed: {len(opcodes)}")
    return opcodes, accesses, classes


def main():
    opcodes, accesses, classes = source_contract()
    records = cu_records()
    mesa = (ROOT / "references/mesa-sm70_encode.rs").read_text()
    mesa_methods = {m[1]: mesa[:m.start()].count("\n") + 1
                    for m in re.finditer(r"impl SM70Op for (Op\w+) \{", mesa)}
    # These are source method names, not a claim that every encoding/form exists.
    aliases = {
        "ALD": ["OpALd"], "AST": ["OpASt"], "ATOMG": ["OpAtom"], "RED": ["OpAtom"],
        "ISBERD": ["OpIsberd"], "ISBEWR": ["OpIsbewr"], "SURED": ["OpSuAtom"],
        "LDG": ["OpLd"], "LDL": ["OpLd"], "LDS": ["OpLd"],
        "STG": ["OpSt"], "STL": ["OpSt"], "STS": ["OpSt"],
        "UIMAD": ["OpIMad", "OpIMad64"], "IMAD": ["OpIMad", "OpIMad64"],
        "IADD3": ["OpIAdd3", "OpIAdd3X"], "UIADD3": ["OpIAdd3", "OpIAdd3X"],
        "ULEA": ["OpLea", "OpLeaX"], "LEA": ["OpLea", "OpLeaX"],
        "UBREV": ["OpBRev"], "UFLO": ["OpFlo"], "UISETP": ["OpISetP"],
        "ULDC": ["OpLdc"], "ULOP3": ["OpLop3"], "UMOV": ["OpMov"],
        "UPLOP3": ["OpPLop3"], "UPOPC": ["OpPopC"], "USEL": ["OpSel"],
        "USHF": ["OpShf"], "VOTEU": ["OpVote"], "S2UR": ["OpS2R"],
    }
    normalized = {name[2:].upper(): name for name in mesa_methods}
    rows = []
    for op in sorted(opcodes):
        forms = {k: len(v) for k, v in records.items() if k.split("_")[0] == op}
        names = aliases.get(op, [normalized[op]] if op in normalized else [])
        rows.append({"opcode": op, "consumer": opcodes[op], "cuasm_forms": forms,
                     "cuasm_records": sum(forms.values()),
                     "mesa_methods": [{"name": n, "line": mesa_methods[n]} for n in names],
                     "implemented_proof": op in ("ALD", "AST", "IPA", "FADD", "FMUL", "EXIT")})
    literals = sorted({x["literal"] for x in accesses if isinstance(x["literal"], str)})
    dynamic = sorted({x["expression"] for x in accesses if x["literal"] is None})
    report = {"status": "STATIC_CONSUMER_CONTRACT", "mnemonics": 99,
              "cuasm_mnemonics": sum(bool(x["cuasm_forms"]) for x in rows),
              "cuasm_missing": [x["opcode"] for x in rows if not x["cuasm_forms"]],
              "source_missing": [x["opcode"] for x in rows if not x["cuasm_forms"] and not x["mesa_methods"]],
              "literal_fields": literals, "dynamic_field_expressions": dynamic,
              "field_accesses": accesses, "class_dependencies": classes, "rows": rows,
              "qualification": "Source availability does not prove compatible forms, mappings, or production coverage."}
    (ROOT / "proof/consumer-contract.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k not in
                      ("rows", "field_accesses", "class_dependencies", "literal_fields", "dynamic_field_expressions")}, indent=2))
    print("Literal field names:", len(literals), "dynamic expressions:", len(dynamic))


if __name__ == "__main__":
    main()
