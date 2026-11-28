"""Preserve signed SM86 byte displacement in the consumer's 64-bit fallback.

The original fallback correctly adds the low 32 bits with carry, but a negative
32-bit displacement must also add 0xffffffff to the high word. This wrapper
changes only that emitted address expression, after pinning the original file.
"""
from __future__ import annotations

import hashlib

from adapter_model import CONSUMER_ROOT

ORIGINAL_MEM_SHA = "46cfe0f30f4c2af443261c33d65c1745a1cd3174a01a8e246c1ef1077fc66d12"
_original = None


def global_search(self, insn):
    from glsl.common import Unsupported
    if _original is None:
        raise ValueError("The signed-address overlay was not initialized")
    if any(insn.has(name) for name in ("Ra_URb", "Ra_URc")) or not insn.cls.endswith("Ra64"):
        raise Unsupported("global fallback requires one confirmed 64-bit vector address; an unresolved uniform base is not discarded")
    statement = _original(self, insn)
    if insn.sv("Ra_offset") >= 0:
        return statement
    high = insn.v("Ra") + 1
    before = f"gh = r{high} + gc;"
    if statement.count(before) != 1:
        raise ValueError("The pinned global-address emission shape changed")
    return statement.replace(before, f"gh = r{high} + gc - 1u;")


def install():
    from glsl.core import Builder
    global _original
    path = CONSUMER_ROOT / "glsl/mem.py"
    if hashlib.sha256(path.read_bytes()).hexdigest() != ORIGINAL_MEM_SHA:
        raise ValueError("Signed-address overlay requires the pinned MKW consumer")
    if Builder.global_search is global_search:
        return
    if Builder.global_search.__module__ != "glsl.mem" or Builder.global_search.__name__ != "global_search":
        raise ValueError("Unexpected existing global-address override")
    _original = Builder.global_search
    Builder.global_search = global_search
