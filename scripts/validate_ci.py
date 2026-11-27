"""Validate the selected recipe channel without allowing preview into main."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any, Mapping


PUBLIC_CATALOG = "https://raw.githubusercontent.com/brad38/AllFix-Repo/main/catalog.json"
# Preview identities staged for review in AllFix-Repo issue #8 (148 projects).
PREVIEW_CATALOG = (
    "https://raw.githubusercontent.com/brad38/AllFix-Repo/"
    "3f4603cf42ef43402b4a0a9470232e7d4fcd9eb9/catalog.json"
)


def select_catalog(index: Any, context: Mapping[str, str]) -> str:
    if not isinstance(index, dict):
        raise ValueError("index.json must contain a JSON object")
    channel = index.get("channel", "public")
    if channel not in ("public", "preview"):
        raise ValueError("index.json has an invalid channel")

    targets_main = context.get("GITHUB_REF") == "refs/heads/main" or (
        context.get("GITHUB_EVENT_NAME") in ("pull_request", "pull_request_target")
        and context.get("GITHUB_BASE_REF") == "main"
    )
    if targets_main and channel != "public":
        raise ValueError("Preview index must not be served as production")

    return PREVIEW_CATALOG if channel == "preview" else PUBLIC_CATALOG


def run_validation(repo_root: Path, context: Mapping[str, str]) -> int:
    index = json.loads((repo_root / "index.json").read_text(encoding="utf-8"))
    catalog = select_catalog(index, context)
    return subprocess.call(
        [
            sys.executable,
            str(repo_root / "scripts" / "validate_recipes.py"),
            "--strict-lf",
            "--require-jsonschema",
            "--check-git-blobs",
            "--check-catalog",
            catalog,
        ],
        cwd=repo_root,
    )


def main() -> int:
    try:
        return run_validation(Path(__file__).resolve().parents[1], os.environ)
    except (OSError, ValueError) as exc:
        print(f"CI validation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
