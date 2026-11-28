"""The installed Decoder(spec_path) boundary for the closed Windows profile.

instructions.json is an internal, versioned descriptor, not an NVIDIA encoding
table. The executable is a separately downloaded official redistributable. Its
exact hash is compiled into this backend and is checked before every worker uses
the ordinary CLI. No user-selected executable or memory capture is supported.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from cli_decoder import CliDecoder

CONSUMER_COMMIT = "006d48de08849495e01e151602690d0ec322af82"
WINDOWS_NV_SHA = "f0ab98df225b9f2568e8f56c24a919a4e1362425fb7c02101afbf85022324add"
CONFIGURATION = {
    "format": "allfix-sm86-cli-v1",
    "architecture": "SM86",
    "consumer_commit": CONSUMER_COMMIT,
    "backend_revision": "2026-11-27.1",
    "nvdisasm_version": "12.8.90",
    "nvdisasm_sha256": WINDOWS_NV_SHA,
}


def validate_descriptor(path: Path) -> dict:
    if not path.is_file() or path.stat().st_size > 4096:
        raise ValueError("The internal SM86 CLI descriptor is missing or oversized")
    configuration = json.loads(path.read_text(encoding="utf-8"))
    if configuration != CONFIGURATION:
        raise ValueError("The SM86 descriptor belongs to a different backend")
    return configuration


class Decoder(CliDecoder):
    def __init__(self, spec_path: Path):
        spec_path = Path(spec_path).resolve(strict=True)
        validate_descriptor(spec_path)
        if os.name != "nt":
            raise ValueError("This closed profile requires its Windows redistributable")
        executable = spec_path.parent / "nvdisasm/nvdisasm.exe"
        work = spec_path.parent / "temporary" / str(os.getpid())
        super().__init__(executable, work, WINDOWS_NV_SHA, capture_text=False)
