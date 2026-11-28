"""Read the reviewed catalog scope without confusing a release with gameplay."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any
import urllib.request

ELIGIBLE_CLASSES = frozenset({
    "functional_eligible", "functional_with_limitations", "functional_manual_install",
})
GAMEPLAY_EVIDENCE = frozenset({
    "gameplay_demo", "maintainer_gameplay_report", "user_gameplay_report",
    "original_media_play_test", "gameplay_video", "gameplay_issue",
    "gameplay_screenshot_with_context", "documented_playthrough",
})
ACTIVE_STATUSES = frozenset({"experimental", "validated"})


def load_document(source: str | Path) -> dict[str, Any]:
    source = str(source)
    if source.startswith("https://"):
        request = urllib.request.Request(source, headers={"User-Agent": "GetAll-Scope/1.0"})
        with urllib.request.urlopen(request, timeout=25) as response:
            data = json.loads(response.read().decode("utf-8-sig"))
    else:
        data = json.loads(Path(source).read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected an object in {source}")
    return data


def companion_source(catalog_source: str | Path, filename: str) -> str:
    # Decisions must belong to the same catalog revision, not a moving main.
    if filename not in {"eligibility.json", "excluded-projects.json"}:
        raise ValueError(f"Unsupported catalog companion: {filename}")
    source = str(catalog_source)
    if source.startswith("https://"):
        return source.rsplit("/", 1)[0] + "/" + filename
    return str(Path(source).parent / filename)


def assessments(document: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if document is None:
        return {}
    projects = document.get("projects")
    if not isinstance(projects, dict) or any(not isinstance(v, dict) for v in projects.values()):
        raise ValueError("Eligibility/exclusion registry must contain a projects object")
    return projects


def is_eligible(assessment: dict[str, Any] | None) -> bool:
    if not isinstance(assessment, dict):
        return False
    evidence = assessment.get("gameplay_evidence")
    return (assessment.get("eligible") is True
            and assessment.get("classification") in ELIGIBLE_CLASSES
            and isinstance(evidence, list)
            and any(isinstance(e, dict) and e.get("kind") in GAMEPLAY_EVIDENCE
                    and isinstance(e.get("url"), str) and e["url"].startswith("https://")
                    and isinstance(e.get("observed"), str) and len(e["observed"].strip()) >= 20
                    for e in evidence)
            and isinstance(assessment.get("official_install_method"), str)
            and len(assessment["official_install_method"].strip()) >= 20
            and assessment.get("provenance_review") in {
                "official_source", "official_distribution", "official_source_and_distribution"}
            and not assessment.get("requires_allfix_game_changes", False))


def repository_of(project):
    source = project.get("source") or {}
    repository = source.get("github_repository") or ""
    if not repository and source.get("provider") == "gitlab":
        url = source.get("url") or ""
        if url.startswith("https://gitlab.com/"):
            repository = "gitlab:" + url.removeprefix("https://gitlab.com/").split("/-/", 1)[0].strip("/")
    return repository


def excluded_identities(document: dict[str, Any] | None) -> dict[tuple[str, str], str]:
    result = {}
    for pid, record in assessments(document).items():
        game_id = record.get("game_id") or record.get("game", {}).get("id")
        project = record.get("project", {})
        if not game_id or project.get("id", pid) != pid:
            raise ValueError(f"Invalid excluded project identity: {pid}")
        if record.get("assessment", {}).get("eligible") is not False:
            raise ValueError(f"Excluded project must explicitly be ineligible: {pid}")
        result[(game_id, pid)] = repository_of(project)
    return result


def load_scope(catalog_source, *, eligibility_source=None, exclusions_source=None):
    catalog = load_document(catalog_source)
    declared = catalog.get("eligibility_file")
    if eligibility_source is None and declared:
        eligibility_source = companion_source(catalog_source, declared)
    if exclusions_source is None and declared:
        exclusions_source = companion_source(catalog_source, "excluded-projects.json")
    return (catalog, load_document(eligibility_source) if eligibility_source else None,
            load_document(exclusions_source) if exclusions_source else None)


def catalog_identities(catalog):
    result = {}
    for game in catalog.get("games", []):
        for project in game.get("projects", []):
            key = (game.get("id"), project.get("id"))
            if key in result:
                raise ValueError(f"Duplicate catalog project: {key}")
            result[key] = repository_of(project)
    return result
