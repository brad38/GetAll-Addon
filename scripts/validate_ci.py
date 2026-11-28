"""Validate the selected recipe channel without allowing preview into main."""

from __future__ import annotations

import json
import hashlib
import os
from pathlib import Path
import subprocess
import sys
from typing import Any, Mapping


PUBLIC_CATALOG = "https://raw.githubusercontent.com/brad38/AllFix-Repo/main/catalog.json"
# Catalog, eligibility and exclusion companions are fetched at one revision.
# Reviewed eligibility scope committed on 2026-11-28 (137 projects, 11 exclusions).
PREVIEW_CATALOG = (
    "https://raw.githubusercontent.com/brad38/AllFix-Repo/"
    "6407730f9708de995175cd757ec41e871c3ebc62/catalog.json"
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


def watch_target(index: Any, context: Mapping[str, str]) -> dict[str, str]:
    """Keep preview automation on its review branch, never on production main."""
    catalog = select_catalog(index, context)
    ref = context.get("GITHUB_REF", "")
    if not ref.startswith("refs/heads/"):
        raise ValueError("Upstream watch requires an explicit branch context")
    base = ref.removeprefix("refs/heads/")
    if not base or base.startswith("automation/"):
        raise ValueError("Upstream watch must start from a maintained review/base branch")
    suffix = "" if base == "main" else "-" + hashlib.sha256(base.encode()).hexdigest()[:12]
    return {"base": base, "branch": "automation/upstream-watch" + suffix, "catalog": catalog}


def run_validation(repo_root: Path, context: Mapping[str, str]) -> int:
    index = json.loads((repo_root / "index.json").read_text(encoding="utf-8"))
    catalog = select_catalog(index, context)
    result = subprocess.call(
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
    if result:
        return result
    return subprocess.call(
        [sys.executable, str(repo_root / "scripts" / "catalog_coverage.py"),
         "--catalog", catalog, "--output", str(repo_root / "catalog-coverage-report.json")],
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
