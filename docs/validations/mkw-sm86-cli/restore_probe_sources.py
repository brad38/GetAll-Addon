"""Restore two public text inputs for optional corpus/numeric reproduction.

The default prints required pins. --cache copies only verified existing source;
--download explicitly fetches the two fixed official-source URLs. No program is
executed and no NVIDIA internal table is obtained by this script.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import urllib.request


def main():
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--cache", type=Path)
    mode.add_argument("--download", action="store_true")
    args = parser.parse_args()
    pins = json.loads((root / "probe-source-pins.json").read_text())
    if not args.cache and not args.download:
        print(json.dumps(pins, indent=2))
        return
    for pin in pins:
        target = root / pin["path"]
        if target.exists():
            data = target.read_bytes()
        elif args.cache:
            data = (args.cache / pin["path"]).read_bytes()
        else:
            with urllib.request.urlopen(pin["url"], timeout=45) as response:
                data = response.read(pin["bytes"] + 1)
        if len(data) != pin["bytes"] or hashlib.sha256(data).hexdigest() != pin["sha256"]:
            raise ValueError("Source pin mismatch: " + pin["path"])
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as output:
                output.write(data)
        print("VERIFIED", pin["path"], pin["sha256"])


if __name__ == "__main__":
    main()
