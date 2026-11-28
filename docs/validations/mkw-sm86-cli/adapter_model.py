"""Small, portable bindings to the pinned MKW frontend's public Python model.

The development tree adds its exact source snapshot to sys.path. In the installed
package program.py has already defined Insn/Sph before importing this backend.
No encoding tables or fixtures are needed by the installed modules.
"""
from __future__ import annotations

from pathlib import Path
import sys
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent
_draft_consumer = ROOT / "upstream/sm86/translate"
if _draft_consumer.is_dir():
    sys.path[:0] = [str(_draft_consumer), str(_draft_consumer / "frontend")]
import program
from program import Insn, Sph, STAGES

CONSUMER_ROOT = Path(program.__file__).resolve().parents[1]
NVDISASM_SHA = "250ebe97dd86617574a30daf8d8ee433e6c5d9d10bafff922078779d1ba36073"
READS: set[tuple[str, str, str, bool]] = set()
TRACE_FIELDS = _draft_consumer.is_dir()


class UncoveredEncoding(ValueError):
    pass


def bits(word: int, start: int, width: int) -> int:
    return (word >> start) & ((1 << width) - 1)


def field(name: str, value: int, width: int, symbol: str | None = None):
    return SimpleNamespace(item=SimpleNamespace(name=name), value=value,
                           slot_values=[(SimpleNamespace(width=width), value)],
                           symbols=[symbol] if symbol is not None else None)


class TracedInsn(Insn):
    def v(self, name, default=None):
        if TRACE_FIELDS:
            READS.add((self.op, "v", name, name in self.f))
        return super().v(name, default)

    def sym(self, name):
        if TRACE_FIELDS:
            READS.add((self.op, "sym", name, name in self.f))
        return super().sym(name)

    def has(self, name):
        if TRACE_FIELDS:
            READS.add((self.op, "has", name, name in self.f))
        return super().has(name)
