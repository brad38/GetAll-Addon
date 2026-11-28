"""Experimental whole-program decoder using only NVIDIA's documented CLI.

No global encoding table, process inspection, library injection, or guessed
instruction terminator is used. An unknown form raises a diagnostic; it never
becomes cls=None. Temporary authored input is removed after every subprocess.
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import re
import struct
import subprocess
import tempfile
import threading

from adapter_fields import UncoveredEncoding
from cli_parse import parse_sass
from control_adapter import decode_control
from memory_adapter import decode_memory
from scalar_adapter import decode_scalar
from texture_adapter import decode_texture
from adapter_model import ROOT, NVDISASM_SHA, Sph, STAGES
from lea_overlay import decode_lea, install as install_lea
from memory_overlay import install as install_memory

ADAPTERS = (decode_lea, decode_scalar, decode_control, decode_memory, decode_texture)
MAX_PROGRAM_BYTES = 1024 * 1024
MAX_STDOUT_BYTES = 16 * 1024 * 1024
MAX_STDERR_BYTES = 64 * 1024


def capture_limited(arguments, *, environment, work, timeout=30):
    """Drain both pipes concurrently, killing a child before retaining excess output."""
    with subprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          cwd=work, env=environment) as process:
        outputs = [bytearray(), bytearray()]
        overflow = threading.Event()

        def reader(index, stream, maximum):
            while block := stream.read(16384):
                if len(outputs[index]) + len(block) > maximum:
                    overflow.set()
                    process.kill()
                    return
                outputs[index].extend(block)

        threads = [threading.Thread(target=reader, args=(0, process.stdout, MAX_STDOUT_BYTES), daemon=True),
                   threading.Thread(target=reader, args=(1, process.stderr, MAX_STDERR_BYTES), daemon=True)]
        for thread in threads:
            thread.start()
        try:
            status = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired as error:
            process.kill()
            process.wait()
            raise UncoveredEncoding("nvdisasm exceeded its per-program deadline") from error
        finally:
            for thread in threads:
                thread.join(timeout=2)
        if overflow.is_set() or any(thread.is_alive() for thread in threads):
            raise UncoveredEncoding("nvdisasm exceeded its bounded output contract")
        return status, outputs[0].decode("utf-8", errors="strict"), outputs[1].decode("utf-8", errors="replace")


def decode_text(word: int, pc: int, text: str):
    try:
        parsed = parse_sass(text)
        for adapter in ADAPTERS:
            value = adapter(word, pc, parsed)
            if value is not None:
                return value
    except UncoveredEncoding:
        raise
    except (ValueError, TypeError, AttributeError, IndexError, KeyError, OverflowError) as error:
        raise UncoveredEncoding(f"SM86 at{pc:#x}: unrecognized CLI syntax ({type(error).__name__})") from error
    raise UncoveredEncoding(f"SM86 at{pc:#x}: opcode {parsed['base_name']} is outside the pinned consumer")


class CliDecoder:
    def __init__(self, executable: Path | None = None, work: Path | None = None, expected_sha: str = NVDISASM_SHA,
                 capture_text: bool = True):
        self.executable = executable or ROOT / "tools/nvdisasm"
        self.work = work or ROOT / "proof"
        if hashlib.sha256(self.executable.read_bytes()).hexdigest() != expected_sha:
            raise ValueError("NVIDIA executable pin changed")
        self.work.mkdir(parents=True, exist_ok=True)
        self.last_text = ""
        self.capture_text = capture_text
        install_lea()
        install_memory()

    def program(self, code: bytes, stage: str):
        if stage not in ("cs", "vs", "ps", "gs", "tcs", "tes", "tes?"):
            raise ValueError("Unknown shader stage")
        sph = None
        if stage != "cs":
            if len(code) < 128:
                raise ValueError("Truncated shader header")
            words = struct.unpack_from("<32I", code)
            sph = Sph(STAGES.get((words[0] >> 10) & 0xf, stage), words)
            code = code[128:]
        if len(code) % 16 or len(code) > MAX_PROGRAM_BYTES:
            raise ValueError("Invalid instruction-buffer bounds")
        words = [int.from_bytes(code[k:k+16], "little") for k in range(0, len(code), 16)]
        if 0 in words:
            end = words.index(0)
            if any(words[end:]):
                raise UncoveredEncoding("Nonzero trailing data after a zero instruction requires an explicit extraction boundary")
            words = words[:end]
            code = code[:end*16]
        if not words:
            raise ValueError("Empty instruction program")
        with tempfile.NamedTemporaryFile(prefix="allfix-sm86-", suffix=".bin", dir=self.work, delete=False) as handle:
            handle.write(code)
            temporary = Path(handle.name)
        try:
            environment = {"PATH": "/usr/bin:/bin"}
            if os.name == "nt":
                environment = {k: v for k, v in os.environ.items() if k.upper() in ("SYSTEMROOT", "WINDIR")}
                system = Path(environment.get("SystemRoot", environment.get("SYSTEMROOT", "C:/Windows"))) / "System32"
                environment["PATH"] = str(self.executable.parent) + os.pathsep + str(system)
                environment["TEMP"] = environment["TMP"] = str(self.work)
            status, stdout, stderr = capture_limited(
                [str(self.executable), "--binary", "SM86", "--no-dataflow", str(temporary)],
                environment=environment, work=self.work)
            if status:
                raise UncoveredEncoding(f"nvdisasm rejected the buffer (exit{status}): {stderr[:600]}")
            rows = re.findall(r"/\*([0-9a-fA-F]+)\*/\s*(.*?)\s*;", stdout)
            if len(rows) != len(words) or [int(pc, 16) for pc, _ in rows] != list(range(0, len(code), 16)):
                raise UncoveredEncoding("Disassembly addresses are not a complete, contiguous instruction sequence")
            self.last_text = stdout if self.capture_text else ""
            return sph, [decode_text(word, k * 16, text) for k, (word, (_, text)) in enumerate(zip(words, rows))]
        finally:
            temporary.unlink(missing_ok=True)
