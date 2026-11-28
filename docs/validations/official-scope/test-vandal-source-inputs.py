"""Exercise Vandal Hearts' upstream input guards without proprietary inputs."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile

SOURCE_COMMIT = "14552fffa0e0b47e02b57592e274fc6e7a649923"
TOOL_HASHES = {
    "build_data_segment.py": "b3c88fac5179b255b576a63e698b612102a9855dac84e6c33adbdb2c22fae186",
    "gen_kanji_font.py": "43057f32dfcd96d6c324175f6ea397ad518db1e5bc16fa54e1e205b916d05242",
    "check_shared.py": "d5d7fac138906d3a56a9de89375de1ae22424aea07c28418fb6c0e35507061fb",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    args = parser.parse_args()
    tools = args.source.resolve() / "platform/pc/tools"
    for name, expected in TOOL_HASHES.items():
        actual = hashlib.sha256((tools / name).read_bytes()).hexdigest()
        if actual != expected:
            parser.error(f"{name}: SHA-256 {actual} != {expected}")

    results = []
    with tempfile.TemporaryDirectory(prefix="GetAll Vandal teste com espaço ") as path:
        fixture = Path(path)
        short_exe = bytearray(0x800)
        short_exe[:8] = b"PS-X EXE"
        struct.pack_into("<I", short_exe, 0x1C, 0x40)
        payloads = {
            "synthetic-short.exe": short_exe,
            "synthetic-complete.exe": short_exe + bytes(0x40),
            "invalid.exe": b"Not a PlayStation executable",
            "invalid-bios.bin": bytes(512 * 1024),
            "short-krom.bin": bytes(64),
        }
        for name, data in payloads.items():
            (fixture / name).write_bytes(data)
        output = fixture / "generated.c"
        env = {k: v for k, v in os.environ.items() if not k.upper().startswith("VH_")}

        def run(case, program, args, expected_exit, expected_message, **overrides):
            process = subprocess.run(
                [sys.executable, "-B", str(tools / program), *args],
                cwd=fixture,
                env={**env, "PYTHONIOENCODING": "utf-8", **overrides},
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                encoding="utf-8",
                errors="replace",
                timeout=30,
                check=False,
            )
            results.append({
                "case": case,
                "exit_code": process.returncode,
                "output": process.stdout.strip().replace(str(fixture), "<fixture>"),
                "passed": (
                    process.returncode == expected_exit
                    and expected_message in process.stdout
                    and not output.exists()
                ),
            })

        exe_cases = (
            ("missing.exe", "PSX_EXE not found"),
            ("invalid.exe", "not a PS-X EXE"),
            ("synthetic-short.exe", "looks truncated"),
            ("synthetic-complete.exe", "does not match the known {region} retail"),
        )
        for region in ("us", "jp"):
            for name, message in exe_cases:
                run(
                    f"{region}-{name}", "build_data_segment.py", ["--validate-only"], 1,
                    message.format(region=region.upper()), VH_REGION=region,
                    VH_PSX_EXE=str(fixture / name),
                )
            for name, message in (
                ("invalid-bios.bin", "unsupported or invalid KROM/BIOS charset-2 data"),
                ("short-krom.bin", "KROMDAT.BIN too small"),
            ):
                run(
                    f"{region}-{name}", "gen_kanji_font.py", [], 1, message,
                    VH_REGION=region, VH_KROM_SOURCE=str(fixture / name),
                    VH_GENERATED_OUT=str(output),
                )
        run(
            "shared-source-parity", "check_shared.py", [], 0,
            "54 TUs + 11 headers identical after gate-stripping",
        )

    print(json.dumps({
        "source_commit": SOURCE_COMMIT,
        "source_tool_sha256": TOOL_HASHES,
        "scope": "Upstream source parity and negative input guards using synthetic files",
        "results": results,
    }, indent=2))
    return 0 if all(result["passed"] for result in results) else 1


if __name__ == "__main__":
    sys.exit(main())
