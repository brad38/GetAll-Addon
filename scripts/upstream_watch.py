#!/usr/bin/env python3
"""Daily upstream monitor for AllFix-Repo catalog changes and official GitHub releases.

Safety invariants:
- Never executes downloaded third-party binaries (reads ZIP central directory only).
- Never invents hashes or promotes any recipe to 'validated'.
- Preserves all existing entries in index.json and existing recipe files.
- Registers technical blockers instead of writing unsafe or invalid recipes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import validate_recipes  # noqa: E402
from catalog_scope import assessments, excluded_identities, is_eligible, load_scope  # noqa: E402
from validate_ci import select_catalog  # noqa: E402

GITHUB_API_BASE = "https://api.github.com"
MAX_ZIP_BYTES = 250 * 1024 * 1024  # 250 MiB cap for safe CI inspection
HTTP_TIMEOUT = 25
AUDIT_BASELINE_CUTOFF_UTC = "2026-11-22T23:59:59Z"
RE_REPORT_FINGERPRINT = re.compile(
    r"Fingerprint das novidades:\*\*\s*`([0-9a-f]{12})`"
)

NON_WINDOWS_TOKENS = (
    "linux",
    "macos",
    "darwin",
    "osx",
    "ubuntu",
    "debian",
    "fedora",
    "appimage",
    "flatpak",
    "android",
    "switch",
    "wiiu",
    "3ds",
    "vita",
    "ps3",
    "ps4",
    "freebsd",
    "source",
    "src",
)
WINDOWS_TOKENS = ("win64", "win32", "windows", "win-x64", "win_x64", "win", "x86_64", "x64")
DEBUG_TOKENS = ("debug", "pdb", "symbols", "syms", "asan")

RE_AUDIT_ROW = re.compile(
    r"^\|\s*\d+\s*\|\s*(?P<game>[^|]+?)\s*\|\s*.*?`(?P<project_id>[a-z0-9-]+)`\s*\|\s*`(?P<tag>[^`]+)`\s*\|\s*\*\*(?P<class>[ABCD])\*\*\s*\|"
)
RE_RODADA_B_ROW = re.compile(
    r"^\|\s*[^|]+?\s*\|\s*(?P<project_id>[a-z0-9-]+)\s*\|\s*(?P<tag>[^|]+?)\s*\|\s*(?P<status>experimental|pending)\s*\|"
)


@dataclass
class AuditBaseline:
    """Known project metadata parsed from existing docs/audit reports."""

    classes: dict[str, str] = field(default_factory=dict)
    known_tags: dict[str, set[str]] = field(default_factory=dict)


@dataclass
class ZipInspection:
    """Static inspection metadata from an official Windows ZIP asset."""

    asset_name: str
    asset_url: str
    size_bytes: int
    sha256: str
    files: list[str]
    executables: list[str]
    invalid_sdk_paths: list[str]


def load_audit_baseline(repo_root: Path) -> AuditBaseline:
    """Parse project IDs, classes (A/B/C/D), and previously audited tags from docs."""
    baseline = AuditBaseline()
    audit_path = repo_root / "docs" / "AUDITORIA-CATALOGO-2026-11-22.md"
    if audit_path.is_file():
        for line in audit_path.read_text(encoding="utf-8").splitlines():
            m = RE_AUDIT_ROW.match(line)
            if m:
                pid = m.group("project_id").strip()
                tag = m.group("tag").strip()
                baseline.classes[pid] = m.group("class").strip()
                if tag and tag != "—":
                    baseline.known_tags.setdefault(pid, set()).add(tag)

    rodada_b = repo_root / "docs" / "RODADA-B-2026-11-23.md"
    if rodada_b.is_file():
        for line in rodada_b.read_text(encoding="utf-8").splitlines():
            m = RE_RODADA_B_ROW.match(line)
            if m:
                pid = m.group("project_id").strip()
                tag = m.group("tag").strip()
                if tag and tag != "—":
                    baseline.known_tags.setdefault(pid, set()).add(tag)

    return baseline


def get_github_headers() -> dict[str, str]:
    """Build GitHub API headers without ever logging token values."""
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "GetAll-Addon-Upstream-Watch/1.0",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token.strip()}"
    return headers


def fetch_json(url: str, headers: dict[str, str] | None = None) -> tuple[Any, dict[str, str]]:
    """Perform HTTPS GET and decode JSON response along with lowercase response headers."""
    if not url.startswith("https://"):
        raise ValueError(f"Refusing non-HTTPS URL: {url}")
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "GetAll-Addon-Watch/1.0"})
    with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
        resp_headers = {k.lower(): v for k, v in resp.headers.items()}
        data = json.loads(resp.read().decode("utf-8"))
        return data, resp_headers


def load_existing_report_fingerprint(repo_root: Path) -> str | None:
    """Read the last recorded upstream-watch fingerprint from docs/MONITORAMENTO-UPSTREAM.md if present."""
    report_path = repo_root / "docs" / "MONITORAMENTO-UPSTREAM.md"
    if not report_path.is_file():
        return None
    text = report_path.read_text(encoding="utf-8")
    m = RE_REPORT_FINGERPRINT.search(text)
    return m.group(1) if m else None


def select_latest_release(
    releases: list[dict[str, Any]],
    *,
    allow_prerelease: bool = False,
) -> dict[str, Any] | None:
    """Pick the newest non-draft release, preferring stable releases unless none exist."""
    non_drafts = [r for r in releases if isinstance(r, dict) and not r.get("draft")]
    if not non_drafts:
        return None
    stable = [r for r in non_drafts if not r.get("prerelease")]
    if allow_prerelease:
        return non_drafts[0]
    return stable[0] if stable else non_drafts[0]


def select_newer_catalog_release(
    releases: list[dict[str, Any]],
    known_tags: set[str],
    *,
    is_new_project: bool,
) -> dict[str, Any] | None:
    """For catalog-only projects, return a release only if it is newer than audited tags and cutoff."""
    non_drafts = [r for r in releases if isinstance(r, dict) and not r.get("draft")]
    if not non_drafts:
        return None

    # If an audited tag appears in the release list, only look at releases strictly newer than it
    known_idx: int | None = None
    known_was_prerelease = False
    for idx, rel in enumerate(non_drafts):
        tag = str(rel.get("tag_name") or "").strip()
        if tag in known_tags:
            known_idx = idx
            known_was_prerelease = bool(rel.get("prerelease"))
            break

    if known_idx == 0:
        return None

    candidates = non_drafts[:known_idx] if known_idx is not None else non_drafts
    if not known_was_prerelease:
        stable_candidates = [r for r in candidates if not r.get("prerelease")]
        if stable_candidates:
            candidates = stable_candidates
        elif known_idx is not None:
            # Audited tag was stable; ignore newer prereleases for non-indexed catalog entries
            return None

    chosen = candidates[0] if candidates else None
    if not chosen:
        return None

    chosen_tag = str(chosen.get("tag_name") or "").strip()
    if not chosen_tag or chosen_tag in known_tags:
        return None

    # For projects already audited on 2026-11-22, ignore historical tags published before the audit
    if not is_new_project:
        pub = str(chosen.get("published_at") or "")
        if pub and pub <= AUDIT_BASELINE_CUTOFF_UTC:
            return None

    return chosen


def select_windows_zip_asset(assets: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Heuristically select the primary official Windows .zip release asset."""
    candidates: list[tuple[int, dict[str, Any]]] = []
    for asset in assets:
        name = str(asset.get("name") or "")
        lower = name.lower()
        if not lower.endswith(".zip"):
            continue
        if any(tok in lower for tok in NON_WINDOWS_TOKENS):
            continue

        score = 0
        if any(tok in lower for tok in ("win64", "windows-x64", "windows-x86_64", "win-x64", "windows")):
            score += 40
        elif "win" in lower or "x64" in lower or "x86_64" in lower or "w64" in lower:
            score += 25
        elif "win32" in lower or "x86" in lower or "i686" in lower:
            score += 15
        else:
            score += 5

        if "portable" in lower:
            score += 5
        if any(tok in lower for tok in DEBUG_TOKENS):
            score -= 20

        candidates.append((score, asset))

    if not candidates:
        return None
    candidates.sort(key=lambda pair: pair[0], reverse=True)
    return candidates[0][1]


def download_and_inspect_zip(
    asset_name: str,
    download_url: str,
    *,
    declared_size: int | None = None,
    max_bytes: int = MAX_ZIP_BYTES,
) -> ZipInspection:
    """Download a ZIP archive safely into temp storage and inspect central directory only."""
    if not download_url.startswith("https://"):
        raise ValueError(f"Refusing non-HTTPS asset URL: {download_url}")
    if declared_size is not None and declared_size > max_bytes:
        raise ValueError(
            f"Asset '{asset_name}' size {declared_size} exceeds inspection cap {max_bytes}"
        )

    tmp_dir = Path(tempfile.mkdtemp(prefix="getall_zip_inspect_"))
    try:
        zip_path = tmp_dir / "package.zip"
        req = urllib.request.Request(
            download_url,
            headers={"User-Agent": "GetAll-Addon-Upstream-Watch/1.0"},
        )
        hasher = hashlib.sha256()
        total = 0
        with urllib.request.urlopen(req, timeout=60) as resp, zip_path.open("wb") as out:
            while True:
                chunk = resp.read(1024 * 128)
                if not chunk:
                    break
                total += len(chunk)
                if total > max_bytes:
                    raise ValueError(
                        f"Downloaded bytes for '{asset_name}' exceeded cap {max_bytes}"
                    )
                hasher.update(chunk)
                out.write(chunk)

        return inspect_local_zip(
            zip_path,
            asset_name=asset_name,
            asset_url=download_url,
            size_bytes=total,
            sha256_hex=hasher.hexdigest(),
        )
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def inspect_local_zip(
    zip_path: Path,
    *,
    asset_name: str,
    asset_url: str,
    size_bytes: int | None = None,
    sha256_hex: str | None = None,
) -> ZipInspection:
    """Inspect ZIP archive entries without extracting or executing any file."""
    raw_size = size_bytes if size_bytes is not None else zip_path.stat().st_size
    if sha256_hex is None:
        hasher = hashlib.sha256()
        with zip_path.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 128), b""):
                hasher.update(chunk)
        sha256_hex = hasher.hexdigest()

    files: list[str] = []
    executables: list[str] = []
    invalid_sdk_paths: list[str] = []
    with zipfile.ZipFile(zip_path, "r") as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            member = info.filename.replace("\\", "/").lstrip("/")
            if not member or member.endswith("/"):
                continue
            files.append(member)
            if member.lower().endswith(".exe"):
                executables.append(member)
            ok, _ = validate_recipes.is_safe_relative_path(member)
            if not ok:
                invalid_sdk_paths.append(member)

    return ZipInspection(
        asset_name=asset_name,
        asset_url=asset_url,
        size_bytes=raw_size,
        sha256=sha256_hex,
        files=sorted(files),
        executables=sorted(executables),
        invalid_sdk_paths=sorted(invalid_sdk_paths),
    )


def map_required_files_to_zip(
    base_required_files: list[str],
    base_launch_file: str | None,
    zip_files: list[str],
) -> tuple[bool, list[str], str | None, str]:
    """Check if required_files and launch_file exist in the inspected ZIP (supporting single root folder remap)."""
    zip_set = set(zip_files)
    if all(rf in zip_set for rf in base_required_files):
        if base_launch_file and base_launch_file not in zip_set:
            return False, [], None, f"launch_file '{base_launch_file}' missing from ZIP"
        return True, list(base_required_files), base_launch_file, "exact path match"

    # Try remapping when the archive has a single versioned top-level directory
    zip_roots = {f.split("/", 1)[0] for f in zip_files if "/" in f}
    base_roots = {rf.split("/", 1)[0] for rf in base_required_files if "/" in rf}
    if len(zip_roots) == 1 and len(base_roots) == 1:
        old_root = next(iter(base_roots))
        new_root = next(iter(zip_roots))
        if all(rf.startswith(f"{old_root}/") for rf in base_required_files):
            remapped = [f"{new_root}/{rf[len(old_root) + 1:]}" for rf in base_required_files]
            remapped_launch = (
                f"{new_root}/{base_launch_file[len(old_root) + 1:]}"
                if base_launch_file and base_launch_file.startswith(f"{old_root}/")
                else base_launch_file
            )
            if all(rf in zip_set for rf in remapped) and (
                not remapped_launch or remapped_launch in zip_set
            ):
                return True, remapped, remapped_launch, f"remapped top-level dir '{old_root}' -> '{new_root}'"

    missing = [rf for rf in base_required_files if rf not in zip_set]
    return False, [], None, f"missing required_files in ZIP: {', '.join(missing[:5])}"


def sanitize_tag_filename(tag: str) -> str:
    """Create a safe JSON filename matching index.json path rules for a tag."""
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "-", tag).strip(".-")
    if not cleaned:
        cleaned = "release"
    if not re.match(r"^[A-Za-z0-9_]", cleaned):
        cleaned = f"v{cleaned}"
    return cleaned


def run_upstream_watch(
    repo_root: Path,
    *,
    scope: str = "all",
    apply_updates: bool = False,
    inspect_assets: bool = False,
    catalog_data: dict[str, Any] | None = None,
    eligibility_data: dict[str, Any] | None = None,
    exclusions_data: dict[str, Any] | None = None,
    catalog_source: str | None = None,
    releases_fetcher: Any = None,
    asset_inspector: Any = None,
) -> dict[str, Any]:
    """Compare catalog and GitHub releases against current repository state."""
    index_path = repo_root / "index.json"
    index_data = json.loads(index_path.read_text(encoding="utf-8"))
    index_entries: list[dict[str, Any]] = index_data.get("recipes", [])
    baseline = load_audit_baseline(repo_root)

    if catalog_data is None:
        catalog_data, loaded_eligibility, loaded_exclusions = load_scope(
            catalog_source or select_catalog(index_data, os.environ))
        eligibility_data = eligibility_data if eligibility_data is not None else loaded_eligibility
        exclusions_data = exclusions_data if exclusions_data is not None else loaded_exclusions
    decisions = assessments(eligibility_data)
    excluded_records = assessments(exclusions_data)
    excluded_identities(exclusions_data)  # Reject malformed archive identities.
    policy_projects = set()
    if index_data.get("execution_policy") == "official_upstream_only":
        policy = json.loads((repo_root / "docs" / "official-install-policy.json").read_text(encoding="utf-8"))
        policy_projects = {item["project_id"] for item in policy["blocked_recipes"]}

    headers = get_github_headers()
    if releases_fetcher is None:
        def releases_fetcher(repo: str) -> list[dict[str, Any]]:
            url = f"{GITHUB_API_BASE}/repos/{repo}/releases?per_page=10"
            data, resp_headers = fetch_json(url, headers=headers)
            remaining = resp_headers.get("x-ratelimit-remaining")
            if remaining is not None and int(remaining) < 15:
                raise RuntimeError(
                    f"GitHub API rate limit nearly exhausted (remaining={remaining})"
                )
            return data if isinstance(data, list) else []

    if asset_inspector is None:
        asset_inspector = download_and_inspect_zip

    # Index catalog projects
    catalog_projects: dict[str, dict[str, Any]] = {}
    for game in catalog_data.get("games", []):
        game_id = game.get("id")
        game_title = game.get("title") or game_id
        for proj in game.get("projects", []):
            pid = proj.get("id")
            if not pid:
                continue
            src = proj.get("source") or {}
            catalog_projects[pid] = {
                "game_id": game_id,
                "game_title": game_title,
                "project_id": pid,
                "name": proj.get("fallback_name") or pid,
                "provider": src.get("provider"),
                "repository": src.get("github_repository"),
                "url": src.get("url"),
                "eligible": is_eligible(decisions.get(pid)),
            }

    # 1. Detect new projects in AllFix-Repo not in the 119-project baseline
    new_catalog_projects: list[dict[str, Any]] = []
    metadata_changes: list[dict[str, Any]] = []
    for pid, pinfo in sorted(catalog_projects.items()):
        if pid not in baseline.classes:
            new_catalog_projects.append(pinfo)

    # Check if any indexed recipe has a changed repository in catalog
    indexed_by_project: dict[str, list[dict[str, Any]]] = {}
    for entry in index_entries:
        indexed_by_project.setdefault(entry["project_id"], []).append(entry)
        cat = catalog_projects.get(entry["project_id"])
        if cat and cat.get("repository") and cat["repository"].lower() != entry["repository"].lower():
            metadata_changes.append(
                {
                    "project_id": entry["project_id"],
                    "index_repository": entry["repository"],
                    "catalog_repository": cat["repository"],
                }
            )

    # 2. Decide which repositories to query for releases
    repos_to_check: dict[str, list[dict[str, Any]]] = {}
    for pid, entries in indexed_by_project.items():
        repo = entries[0]["repository"]
        if repo.startswith("gitlab:"):
            # GitHub release watcher does not query gitlab: repositories
            continue
        pinfo = catalog_projects.get(pid)
        if pid in excluded_records:
            reason = "Excluded project: new releases require a fresh gameplay/provenance review before catalog admission"
        elif not pinfo or not pinfo["eligible"]:
            reason = "Candidate/unreviewed project: README, release or build alone cannot establish gameplay eligibility"
        elif str(pinfo.get("repository") or "").lower() != repo.lower():
            reason = "Catalog repository changed; official identity and procedure need explicit review"
        else:
            reason = None
        repos_to_check.setdefault(repo, []).append({
            "kind": "review_only" if reason else "indexed", "project_id": pid,
            "entries": entries, "reason": reason,
            "class": "EXCLUDED" if pid in excluded_records else "CANDIDATE",
        })

    if scope in {"ab", "all"}:
        for pid, pinfo in catalog_projects.items():
            if pid in indexed_by_project:
                continue
            if pinfo.get("provider") != "github" or not pinfo.get("repository"):
                continue
            cls = baseline.classes.get(pid, "NEW")
            if scope == "ab" and cls not in {"A", "B", "NEW"}:
                continue
            repos_to_check.setdefault(pinfo["repository"], []).append(
                {"kind": "catalog" if pinfo["eligible"] else "review_only",
                 "project_id": pid, "info": pinfo, "class": cls,
                 "reason": "Candidate requires specific gameplay evidence and official installation review before admission"}
            )
    elif new_catalog_projects:
        for pinfo in new_catalog_projects:
            if pinfo.get("provider") == "github" and pinfo.get("repository"):
                repos_to_check.setdefault(pinfo["repository"], []).append(
                    {"kind": "catalog" if pinfo["eligible"] else "review_only",
                     "project_id": pinfo["project_id"], "info": pinfo, "class": "NEW",
                     "reason": "Candidate requires specific gameplay evidence and official installation review before admission"}
                )

    # Archived identities remain discoverable without ever becoming installable.
    if scope == "all":
        for pid, record in excluded_records.items():
            if pid in indexed_by_project:
                continue
            src = record.get("project", {}).get("source", {})
            repo = src.get("github_repository")
            if src.get("provider") == "github" and repo:
                repos_to_check.setdefault(repo, []).append({
                    "kind": "review_only", "project_id": pid, "class": "EXCLUDED",
                    "reason": "Excluded project: new releases require a fresh gameplay/provenance review before catalog admission",
                })

    updated_recipes: list[dict[str, Any]] = []
    pending_reviews: list[dict[str, Any]] = []
    api_errors: list[dict[str, str]] = []
    checked_repos = 0

    for repo, targets in sorted(repos_to_check.items()):
        checked_repos += 1
        try:
            releases = releases_fetcher(repo)
        except urllib.error.HTTPError as exc:
            # Class D projects with known missing/404 repos (e.g. AxioDL/metaforce) are already documented
            if exc.code == 404 and all(t.get("class") == "D" for t in targets):
                continue
            api_errors.append({"repository": repo, "error": f"HTTP {exc.code}"})
            continue
        except Exception as exc:
            api_errors.append({"repository": repo, "error": str(exc)})
            if "rate limit" in str(exc).lower():
                break
            continue

        for target in targets:
            pid = target["project_id"]
            if target["kind"] == "review_only":
                known = {e["tag"] for e in target.get("entries", [])} or baseline.known_tags.get(pid, set())
                latest_rel = select_newer_catalog_release(releases, known, is_new_project=not known)
                if latest_rel:
                    pending_reviews.append({
                        "project_id": pid, "class": target.get("class", "CANDIDATE"),
                        "repository": repo, "current_tags": sorted(known),
                        "latest_tag": latest_rel.get("tag_name"), "reason": target["reason"],
                        "release_url": latest_rel.get("html_url", ""),
                        "review_only": True, "eligible_for_automatic_update": False,
                    })
                continue
            if target["kind"] == "indexed":
                entries = target["entries"]
                current_tags = {e["tag"] for e in entries}
                # Retain the existing template order for compatible manual recipes;
                # eligibility below is checked across every version, not list order.
                base_entry = entries[-1]
                allow_pre = any(
                    any(tok in t.lower() for tok in ("alpha", "beta", "rc", "pre", "dev", "test"))
                    for t in current_tags
                )
                latest_rel = select_latest_release(releases, allow_prerelease=allow_pre)
                if not latest_rel:
                    continue
                latest_tag = str(latest_rel.get("tag_name") or "").strip()
                if not latest_tag or latest_tag in current_tags:
                    continue

                project_recipes = [
                    json.loads((repo_root / entry["path"]).read_text(encoding="utf-8"))
                    for entry in entries
                ]
                base_recipe = project_recipes[-1]

                # The generated document below is a v3 manual-step recipe. Never
                # downgrade a newer contract or reactivate a disabled/draft recipe.
                # In particular, v8 Java launchers and v9 preparation/build profiles
                # cannot be copied by checking ZIP filenames alone.
                review_reason = None
                if pid in policy_projects or any(e.get("disabled_reason") for e in entries):
                    review_reason = "Source-integrity suspension requires a reviewed official replacement; an upstream release cannot reactivate it"
                elif any(e.get("status") == "validated" for e in entries):
                    review_reason = "Validated recipe requires functional verification with original media"
                elif any(e.get("status") != "experimental" for e in entries):
                    review_reason = "Disabled or draft recipe requires explicit review before a new version"
                elif any(e.get("schema_version") != 3 for e in entries) or any(r.get("schema_version") != 3 for r in project_recipes):
                    review_reason = "Recipe contract is not v3; preserve its launcher, prerequisites and preparation/build profiles through manual review"
                elif any(r.get("inputs") or r.get("operations") for r in project_recipes):
                    review_reason = "ROM/input operations require functional verification with original media"
                elif any(not isinstance(r.get("manual_steps"), str) or not r["manual_steps"].strip() for r in project_recipes):
                    review_reason = "Automatic updates require a v3 recipe with explicit manual steps"
                if review_reason:
                    pending_reviews.append(
                        {
                            "project_id": pid,
                            "current_tags": sorted(current_tags),
                            "latest_tag": latest_tag,
                            "reason": review_reason,
                            "release_url": latest_rel.get("html_url", ""),
                        }
                    )
                    continue

                zip_asset = select_windows_zip_asset(latest_rel.get("assets", []))

                if not zip_asset:
                    pending_reviews.append(
                        {
                            "project_id": pid,
                            "current_tags": sorted(current_tags),
                            "latest_tag": latest_tag,
                            "reason": "New release detected without an identifiable Windows .zip asset",
                            "release_url": latest_rel.get("html_url", ""),
                        }
                    )
                    continue

                inspection: ZipInspection | None = None
                if inspect_assets:
                    try:
                        inspection = asset_inspector(
                            zip_asset["name"],
                            zip_asset["browser_download_url"],
                            declared_size=zip_asset.get("size"),
                        )
                    except Exception as exc:
                        pending_reviews.append(
                            {
                                "project_id": pid,
                                "current_tags": sorted(current_tags),
                                "latest_tag": latest_tag,
                                "asset": zip_asset["name"],
                                "reason": f"Failed safe ZIP inspection: {exc}",
                                "release_url": latest_rel.get("html_url", ""),
                            }
                        )
                        continue

                if not inspection:
                    pending_reviews.append(
                        {
                            "project_id": pid,
                            "current_tags": sorted(current_tags),
                            "latest_tag": latest_tag,
                            "asset": zip_asset["name"],
                            "reason": "Asset inspection disabled; manual ZIP verification required",
                            "release_url": latest_rel.get("html_url", ""),
                        }
                    )
                    continue

                mapped_ok, new_req_files, new_launch_file, map_note = map_required_files_to_zip(
                    base_recipe.get("required_files", []),
                    base_recipe.get("launch_file"),
                    inspection.files,
                )
                if not mapped_ok:
                    pending_reviews.append(
                        {
                            "project_id": pid,
                            "current_tags": sorted(current_tags),
                            "latest_tag": latest_tag,
                            "asset": zip_asset["name"],
                            "zip_sha256": inspection.sha256,
                            "reason": f"Incompatible package layout ({map_note})",
                            "release_url": latest_rel.get("html_url", ""),
                        }
                    )
                    continue

                bad_paths = [
                    p
                    for p in new_req_files
                    if not validate_recipes.is_safe_relative_path(p)[0]
                ]
                if bad_paths:
                    pending_reviews.append(
                        {
                            "project_id": pid,
                            "current_tags": sorted(current_tags),
                            "latest_tag": latest_tag,
                            "asset": zip_asset["name"],
                            "zip_sha256": inspection.sha256,
                            "reason": f"SDK 1.2.0 path grammar rejects files: {', '.join(bad_paths)}",
                            "release_url": latest_rel.get("html_url", ""),
                        }
                    )
                    continue

                # Stage new experimental recipe preserving all existing entries
                safe_tag_file = sanitize_tag_filename(latest_tag)
                parent_rel = Path(base_entry["path"]).parent.as_posix()
                new_rel_path = f"{parent_rel}/{safe_tag_file}.json"
                if (repo_root / new_rel_path).exists():
                    continue

                new_recipe = {
                    "schema_version": 3,
                    "project_id": pid,
                    "tag": latest_tag,
                    "source_url": f"https://github.com/{base_entry['repository']}/releases/tag/{latest_tag}",
                    "operations": [],
                    "required_files": new_req_files,
                    "inputs": [],
                    "manual_steps": base_recipe.get("manual_steps", ""),
                }
                if new_launch_file:
                    new_recipe["launch_file"] = new_launch_file

                recipe_bytes = (
                    json.dumps(new_recipe, indent=2, ensure_ascii=False) + "\n"
                ).encode("utf-8")
                recipe_sha = hashlib.sha256(recipe_bytes).hexdigest()

                new_index_entry = {
                    "game_id": base_entry["game_id"],
                    "project_id": pid,
                    "repository": base_entry["repository"],
                    "tag": latest_tag,
                    "schema_version": 3,
                    "path": new_rel_path,
                    "sha256": recipe_sha,
                    "status": "experimental",
                    "has_inputs": False,
                    "has_manual_steps": bool(new_recipe["manual_steps"].strip()),
                }

                if apply_updates:
                    target_file = repo_root / new_rel_path
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    target_file.write_bytes(recipe_bytes)

                    index_entries.append(new_index_entry)
                    index_data["recipes"] = index_entries
                    index_bytes = (
                        json.dumps(index_data, indent=2, ensure_ascii=False) + "\n"
                    ).encode("utf-8")
                    index_path.write_bytes(index_bytes)

                    val_doc_path = (
                        repo_root / "docs" / "validations" / f"{pid}-{safe_tag_file}.md"
                    )
                    val_doc_path.parent.mkdir(parents=True, exist_ok=True)
                    val_lines = [
                        f"# Validação experimental — {pid} {latest_tag}",
                        "",
                        f"Jogo: {base_entry['game_id']}",
                        f"Projeto oficial: {pid}",
                        f"Repositório: https://github.com/{base_entry['repository']}",
                        f"Release: {new_recipe['source_url']}",
                        f"ZIP oficial: {inspection.asset_name}",
                        f"Tamanho do ZIP baixado: {inspection.size_bytes} bytes",
                        f"SHA-256 ZIP: {inspection.sha256}",
                        f"Executável: {new_launch_file or 'N/A'}",
                        f"Required files: {', '.join(new_req_files)}",
                        f"Caminho da receita: {new_rel_path}",
                        "",
                        f"Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP ({map_note}), caminhos relativos seguros.",
                        "Não testado: instalação ponta a ponta, importação de mídia original, inicialização do jogo.",
                        "Status: experimental (gerado pelo monitoramento automático; aguarda revisão humana).",
                        "",
                    ]
                    val_doc_path.write_bytes(
                        ("\n".join(val_lines)).encode("utf-8")
                    )

                updated_recipes.append(
                    {
                        "project_id": pid,
                        "previous_tag": base_entry["tag"],
                        "new_tag": latest_tag,
                        "path": new_rel_path,
                        "recipe_sha256": recipe_sha,
                        "zip_asset": inspection.asset_name,
                        "zip_sha256": inspection.sha256,
                        "zip_size": inspection.size_bytes,
                        "note": map_note,
                        "applied": apply_updates,
                    }
                )
            else:
                # Catalog project not yet in index.json
                known = baseline.known_tags.get(pid, set())
                is_new_project = target["class"] == "NEW"
                latest_rel = select_newer_catalog_release(
                    releases, known, is_new_project=is_new_project
                )
                if not latest_rel:
                    continue
                latest_tag = str(latest_rel.get("tag_name") or "").strip()
                zip_asset = select_windows_zip_asset(latest_rel.get("assets", []))
                entry_note: dict[str, Any] = {
                    "project_id": pid,
                    "class": target["class"],
                    "repository": repo,
                    "audited_tags": sorted(known) if known else ["none"],
                    "latest_tag": latest_tag,
                    "asset": zip_asset["name"] if zip_asset else None,
                    "reason": "Catalog project has a newer or newly added release not yet covered by a recipe",
                    "release_url": latest_rel.get("html_url", ""),
                }
                if inspect_assets and zip_asset and target["class"] in {"A", "B", "NEW"}:
                    try:
                        insp = asset_inspector(
                            zip_asset["name"],
                            zip_asset["browser_download_url"],
                            declared_size=zip_asset.get("size"),
                        )
                        entry_note["zip_sha256"] = insp.sha256
                        entry_note["zip_size"] = insp.size_bytes
                        entry_note["executables"] = insp.executables[:5]
                        entry_note["sdk_paths_ok"] = len(insp.invalid_sdk_paths) == 0
                        if insp.invalid_sdk_paths:
                            entry_note["sdk_path_warnings"] = insp.invalid_sdk_paths[:5]
                    except Exception as exc:
                        entry_note["inspection_error"] = str(exc)
                pending_reviews.append(entry_note)

    has_actionable_changes = bool(
        updated_recipes or new_catalog_projects or metadata_changes or pending_reviews
    )

    fingerprint_payload = json.dumps(
        {
            "updated": [(u["project_id"], u["new_tag"]) for u in updated_recipes],
            "new_projects": [p["project_id"] for p in new_catalog_projects],
            "metadata": metadata_changes,
            "pending": [
                (p["project_id"], p.get("latest_tag"), p.get("reason")) for p in pending_reviews
            ],
        },
        sort_keys=True,
    )
    fingerprint = hashlib.sha256(fingerprint_payload.encode("utf-8")).hexdigest()[:12]
    previous_fingerprint = load_existing_report_fingerprint(repo_root)
    already_reported = (
        has_actionable_changes
        and not updated_recipes
        and previous_fingerprint == fingerprint
    )

    return {
        "checked_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "scope": scope,
        "checked_repositories": checked_repos,
        "catalog_project_count": len(catalog_projects),
        "reviewed_eligible_project_count": sum(p["eligible"] for p in catalog_projects.values()),
        "excluded_project_count": len(excluded_records),
        "catalog_mutations": False,
        "eligibility_mutations": False,
        "indexed_recipe_count": len(index_entries),
        "has_actionable_changes": has_actionable_changes and not already_reported,
        "already_reported": already_reported,
        "fingerprint": fingerprint,
        "updated_recipes": updated_recipes,
        "new_catalog_projects": new_catalog_projects,
        "metadata_changes": metadata_changes,
        "pending_reviews": pending_reviews,
        "api_errors": api_errors,
    }


def render_markdown_report(result: dict[str, Any]) -> str:
    """Render a deterministic technical Markdown report (without fluctuating timestamps in body)."""
    lines: list[str] = [
        "# GetAll-Addon — Relatório Técnico de Monitoramento Upstream",
        "",
        f"- **Escopo avaliado:** `{result['scope']}` ({result['checked_repositories']} repositórios consultados, {result['catalog_project_count']} projetos no catálogo `AllFix-Repo`)",
        f"- **Receitas no `index.json`:** {result['indexed_recipe_count']}",
        f"- **Fingerprint das novidades:** `{result['fingerprint']}`",
        "",
    ]

    if result["updated_recipes"]:
        lines.append("## Receitas experimentais propostas/atualizadas")
        lines.append("")
        lines.append("| Projeto | Tag anterior | Nova tag | Asset Windows | SHA-256 ZIP | Caminho |")
        lines.append("|---|---|---|---|---|---|")
        for u in result["updated_recipes"]:
            lines.append(
                f"| `{u['project_id']}` | `{u['previous_tag']}` | `{u['new_tag']}` | `{u['zip_asset']}` | `{u['zip_sha256']}` | `{u['path']}` |"
            )
        lines.append("")

    if result["new_catalog_projects"]:
        lines.append("## Novos projetos identificados no AllFix-Repo")
        lines.append("")
        lines.append("| Jogo | Projeto ID | Repositório | Provider |")
        lines.append("|---|---|---|---|")
        for p in result["new_catalog_projects"]:
            lines.append(
                f"| `{p['game_id']}` | `{p['project_id']}` | `{p.get('repository') or '—'}` | `{p.get('provider') or '—'}` |"
            )
        lines.append("")

    if result["metadata_changes"]:
        lines.append("## Divergências de repositório com o catálogo")
        lines.append("")
        for m in result["metadata_changes"]:
            lines.append(
                f"- `{m['project_id']}`: índice=`{m['index_repository']}` vs catálogo=`{m['catalog_repository']}`"
            )
        lines.append("")

    if result["pending_reviews"]:
        lines.append("## Pendências técnicas e atualizações que exigem revisão manual")
        lines.append("")
        lines.append("| Projeto | Classe/Origem | Nova tag | Asset Windows | Motivo técnico / Evidência |")
        lines.append("|---|---|---|---|---|")
        for p in result["pending_reviews"]:
            origin = p.get("class") or ", ".join(p.get("current_tags", []))
            details = p["reason"]
            if p.get("zip_sha256"):
                details += f" (ZIP SHA-256: `{p['zip_sha256'][:16]}...`"
                if p.get("executables"):
                    details += f", EXEs: `{', '.join(p['executables'][:3])}`"
                if p.get("sdk_path_warnings"):
                    details += f", SDK paths inválidos: `{', '.join(p['sdk_path_warnings'][:2])}`"
                details += ")"
            lines.append(
                f"| `{p['project_id']}` | `{origin}` | `{p.get('latest_tag', '—')}` | `{p.get('asset') or '—'}` | {details} |"
            )
        lines.append("")

    if result["api_errors"]:
        lines.append("## Erros transitórios de consulta")
        lines.append("")
        for err in result["api_errors"]:
            lines.append(f"- `{err['repository']}`: {err['error']}")
        lines.append("")

    if not result["has_actionable_changes"]:
        lines.append("Nenhuma novidade relevante detectada nesta verificação.")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Monitor AllFix-Repo catalog and GitHub releases.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
    )
    parser.add_argument(
        "--scope",
        choices=("tracked", "ab", "all"),
        default="all",
        help="Which repositories to check for new releases",
    )
    parser.add_argument(
        "--apply-updates",
        action="store_true",
        help="Write safe new experimental recipes and update index.json",
    )
    parser.add_argument(
        "--inspect-assets",
        action="store_true",
        help="Download official Windows ZIPs into temp storage to inspect central directory and compute real SHA-256",
    )
    parser.add_argument(
        "--catalog-file",
        type=Path,
        default=None,
        help="Optional local catalog.json path for offline runs",
    )
    parser.add_argument("--eligibility-file", type=Path, help="Eligibility registry from the same catalog revision")
    parser.add_argument("--excluded-projects-file", type=Path, help="Preserved exclusions, monitored only for review")
    parser.add_argument("--json-out", type=Path, default=None)
    parser.add_argument("--report-out", type=Path, default=None)
    args = parser.parse_args()

    catalog_data = None
    eligibility_data = None
    exclusions_data = None
    if args.catalog_file is not None:
        catalog_data, eligibility_data, exclusions_data = load_scope(
            args.catalog_file, eligibility_source=args.eligibility_file,
            exclusions_source=args.excluded_projects_file)
    elif args.eligibility_file or args.excluded_projects_file:
        parser.error("Registry file overrides require --catalog-file to keep revisions aligned")

    result = run_upstream_watch(
        args.repo_root.resolve(),
        scope=args.scope,
        apply_updates=args.apply_updates,
        inspect_assets=args.inspect_assets,
        catalog_data=catalog_data,
        eligibility_data=eligibility_data,
        exclusions_data=exclusions_data,
    )
    report_md = render_markdown_report(result)

    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_bytes(
            (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
        )
    if args.report_out is not None:
        args.report_out.parent.mkdir(parents=True, exist_ok=True)
        args.report_out.write_bytes(report_md.encode("utf-8"))

    print(
        f"Upstream watch complete: repos={result['checked_repositories']}, "
        f"actionable={result['has_actionable_changes']}, "
        f"updated={len(result['updated_recipes'])}, "
        f"pending={len(result['pending_reviews'])}, "
        f"new_projects={len(result['new_catalog_projects'])}, "
        f"api_errors={len(result['api_errors'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
