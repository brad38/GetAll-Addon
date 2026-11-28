"""Normal nvdisasm CLI cross-check of public CuAssembler words and P2R mutations.

No injected libraries or process inspection. The transient instruction buffer is
deleted after its hashes and concise results are saved. No game inputs.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
import re
import subprocess

from coverage_contract import ROOT, cu_records, source_contract
from probe_graphics import NVDISASM_SHA


def main():
    exe = ROOT / "tools/nvdisasm"
    if hashlib.sha256(exe.read_bytes()).hexdigest() != NVDISASM_SHA:
        raise ValueError("nvdisasm pin changed")
    ops, _, _ = source_contract()
    data = cu_records()
    cases = [(key, pc, word, text) for key, values in data.items()
             if key.split("_")[0] in ops for pc, word, text in values]
    extra = json.loads((ROOT / "references/CuAsm/UP2UR-sm80-records.json").read_text())
    if extra["source_blob"] != "51208f1b5e6084c9d61411330c676bda7793af21":
        raise ValueError("Unexpected SM80 reference")
    cases += [(key, pc, word, text) for key, values in extra["records"].items()
              for pc, word, text in values]
    # CuSMVersion.splitCtrlCodeFromIntList_7x_8x removes the 17 scheduling bits.
    # Restore a normal stall=2 schedule. A zero schedule has a different encoding
    # interpretation for some reuse bits in nvdisasm12.8, as the retained failed
    # probe demonstrates. No operand or semantic bit is modified.
    words = [x[2] | (0x7e2 << 105) for x in cases]
    raw = b"".join(word.to_bytes(16, "little") for word in words)
    tmp = ROOT / "proof/cli-corpus.bin"
    tmp.write_bytes(raw)
    try:
        excluded = []
        for attempt in range(3):
            p = subprocess.run([str(exe), "--binary", "SM86", "--no-dataflow", "--emit-json", str(tmp)],
                               capture_output=True, text=True, timeout=30,
                               env={"PATH": "/usr/bin:/bin"})
            if p.returncode == 0:
                break
            # Preserve every rejection; removing a rejected reference from the
            # positive batch never changes its classification to supported.
            indices = {int(x, 16) // 16 for x in re.findall(r"at address 0x([0-9a-fA-F]+)", p.stderr)}
            if not indices or any(x >= len(cases) for x in indices):
                raise RuntimeError("CLI error did not identify closed per-word boundaries")
            for index in sorted(indices):
                key, pc, word, sass = cases[index]
                excluded.append({"form": key, "word": f"{word:032x}", "sass": sass,
                                 "diagnostic": "\n".join(x for x in p.stderr.splitlines()
                                      if f"0x{index * 16:08x}" in x)})
            cases = [x for k, x in enumerate(cases) if k not in indices]
            words = [x[2] | (0x7e2 << 105) for x in cases]
            raw = b"".join(word.to_bytes(16, "little") for word in words)
            tmp.write_bytes(raw)
        else:
            raise RuntimeError("CLI corpus did not settle after three bounded batches")
        doc = json.loads(p.stdout)
        functions = doc[1]
        if len(functions) != 1 or functions[0]["length"] != len(raw):
            raise AssertionError("Unexpected disassembler boundaries")
        rows = functions[0]["sass-instructions"]
        if len(rows) != len(cases):
            raise AssertionError("Missing disassembly rows")
        matched, failures = Counter(), []
        for (key, original_pc, word, original_sass), row in zip(cases, rows):
            expected = key.split("_")[0]
            observed = row.get("opcode", "").split(".")[0]
            if observed == expected:
                matched[expected] += 1
            else:
                failures.append({"form": key, "word": f"{word:032x}",
                                 "expected": expected, "actual": row,
                                 "public_record": original_sass})
        discovered = [{"word": f"{word:032x}", "disassembly": row}
                      for (_, _, word, _), row in zip(cases, rows)
                      if row.get("opcode", "").split(".")[0] == "UP2UR"]
        result = {"status": "NORMAL_CLI_PUBLIC_CORPUS", "input_bytes": len(raw),
                  "input_sha256": hashlib.sha256(raw).hexdigest(), "nvdisasm_exit": p.returncode,
                  "cases": len(cases), "matched_mnemonics": len(matched), "matched": dict(sorted(matched.items())),
                  "mismatches": failures, "rejected_records": excluded, "up2ur_reference": extra["source_url"],
                  "up2ur_confirmed_sm86": discovered, "schedule": "0x7e2 at bit105; operand bits unchanged",
                  "stderr": p.stderr, "production_model": False}
        (ROOT / "proof/cli-corpus-result.json").write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps({k: v for k, v in result.items() if k not in ("matched", "mismatches", "rejected_records")}, indent=2))
        print("Mismatches:", len(failures))
        print("Rejected records retained:", len(excluded))
    finally:
        tmp.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
