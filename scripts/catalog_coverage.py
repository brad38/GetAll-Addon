"""Coverage by six independent dimensions, never by recipe count alone."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
try:
    from .catalog_scope import ACTIVE_STATUSES, assessments, excluded_identities, is_eligible, load_document, load_scope
except ImportError:
    from catalog_scope import ACTIVE_STATUSES, assessments, excluded_identities, is_eligible, load_document, load_scope

USABLE_STATUSES = ACTIVE_STATUSES
DIMENSIONS = (
    "upstream_functional", "automated_installation_implemented", "synthetic_validation",
    "original_media_installation", "first_boot", "gameplay",
)
POSITIVE = {"evidenced", "implemented", "passed"}
EVIDENCE_STATES = {"implemented", "partial", "blocked", "passed", "failed", "unknown", "historical", "not_applicable"}

def load(path):
    return load_document(path)

def project_map(catalog):
    result = {}
    for game in catalog["games"]:
        for project in game["projects"]:
            key = game["id"], project["id"]
            if key in result:
                raise ValueError(f"Duplicate catalog project {key}")
            result[key] = (game.get("platform_group", ""), project)
    return result

def index_map(index):
    result = {}
    for entry in index["recipes"]:
        result.setdefault((entry["game_id"], entry["project_id"]), []).append(entry)
    return result

def validate_execution_evidence(document, evidence_root=None):
    projects = assessments(document)
    for project_id, record in projects.items():
        revisions = record.get("recipe_revisions", [])
        if not isinstance(revisions, list) or any(not isinstance(r, dict)
                or not isinstance(r.get("tag"), str)
                or not re.fullmatch(r"[0-9a-f]{64}", str(r.get("sha256", ""))) for r in revisions):
            raise ValueError(f"Invalid recipe evidence binding for {project_id}")
        dimensions = record.get("dimensions", {})
        if not isinstance(dimensions, dict):
            raise ValueError(f"Dimensions must be an object for {project_id}")
        for name, value in dimensions.items():
            if name not in DIMENSIONS[1:] or not isinstance(value, dict):
                raise ValueError(f"Invalid execution dimension for {project_id}: {name}")
            state = value.get("status")
            if state not in EVIDENCE_STATES:
                raise ValueError(f"Invalid evidence status for {project_id}/{name}: {state}")
            proof = value.get("evidence", [])
            if not isinstance(proof, list):
                raise ValueError(f"Evidence must be a list for {project_id}/{name}")
            for p in proof:
                if not isinstance(p, dict) or not (p.get("path") or p.get("url")) or not p.get("observed"):
                    raise ValueError(f"Invalid proof for {project_id}/{name}")
                if evidence_root is not None and p.get("path"):
                    root = Path(evidence_root).resolve()
                    path = (root / p["path"]).resolve()
                    if not path.is_relative_to(root) or not path.is_file():
                        raise ValueError(f"Missing/unsafe evidence file: {p['path']}")
                    if p.get("sha256") != hashlib.sha256(path.read_bytes()).hexdigest():
                        raise ValueError(f"Evidence file hash mismatch: {p['path']}")
            if state in POSITIVE:
                if not revisions:
                    raise ValueError(f"Positive {project_id}/{name} requires exact recipe tag and SHA-256 binding")
                if not proof or not all(isinstance(p, dict) and (p.get("path") or p.get("url")) and p.get("observed") for p in proof):
                    raise ValueError(f"Positive {project_id}/{name} requires attributable evidence")
                if name in {"original_media_installation", "first_boot", "gameplay"}:
                    if any(p.get("data_kind") != "original_media" or p.get("scope") != "getall" for p in proof):
                        raise ValueError(f"{project_id}/{name} requires original-media GetAll evidence; upstream or synthetic proof is insufficient")
                if name == "synthetic_validation" and any(p.get("data_kind") != "synthetic" for p in proof):
                    raise ValueError(f"{project_id}/{name} requires synthetic-test evidence")
    return projects

def coverage(catalog, main_index, development_index, *, eligibility=None, exclusions=None, evidence=None, evidence_root=None):
    projects = project_map(catalog)
    main, development = index_map(main_index), index_map(development_index)
    excluded = excluded_identities(exclusions)
    decisions = assessments(eligibility)
    execution = validate_execution_evidence(evidence, evidence_root)
    historical_excluded = []
    for label, entries in (("main", main), ("development", development)):
        for key in set(entries) - set(projects):
            versions = entries[key]
            if key not in excluded or any(v.get("status") != "disabled" for v in versions):
                raise ValueError(f"Orphan active/unregistered recipe IDs in {label}: {key}")
            historical_excluded.append({"index": label, "game_id": key[0], "project_id": key[1], "recipes": versions})
    rows = []
    for (game, project), (platform, metadata) in projects.items():
        public, pending = main.get((game, project), []), development.get((game, project), [])
        usable_public = [x for x in public if x.get("status") in USABLE_STATUSES]
        usable_pending = [x for x in pending if x.get("status") in USABLE_STATUSES]
        assessment = decisions.get(project)
        if eligibility is not None and not is_eligible(assessment):
            raise ValueError(f"Active catalog project lacks a reviewed functional assessment: {project}")
        dimensions = {
            "upstream_functional": {
                "status": "evidenced" if is_eligible(assessment) else "unknown",
                "scope": "upstream_external",
                "evidence": (assessment or {}).get("gameplay_evidence", []),
            }
        }
        record = execution.get(project, {})
        for name in DIMENSIONS[1:]:
            item = dict(record.get("dimensions", {}).get(name, {"status": "unknown", "evidence": []}))
            tested = {(r["tag"], r["sha256"]) for r in record.get("recipe_revisions", [])}
            active = {(entry.get("tag"), entry.get("sha256")) for entry in usable_pending}
            if item["status"] in POSITIVE and not tested.intersection(active):
                item = {"status": "historical", "evidence": item.get("evidence", []),
                        "reason": "Evidence does not validate a currently active recipe version"}
            if name == "automated_installation_implemented" and not usable_pending:
                item = {"status": "blocked" if pending else "unknown", "evidence": [],
                        "reason": "No active installation contract; disabled history is retained"}
            dimensions[name] = item
        rows.append({
            "game_id": game, "project_id": project, "platform_group": platform,
            "main": public, "development": pending,
            # Legacy names mean indexed contracts only, never functional coverage.
            "main_covered": bool(usable_public), "development_covered": bool(usable_pending),
            "preparation_only": bool(usable_pending) and all(x["schema_version"] == 9 for x in usable_pending),
            "validated": any(x["status"] == "validated" for x in usable_pending),
            "dimensions": dimensions,
        })
    totals = {name: {} for name in DIMENSIONS}
    for row in rows:
        for name, item in row["dimensions"].items():
            state = item["status"]
            totals[name][state] = totals[name].get(state, 0) + 1
    return {
        "schema_version": 2,
        "meaning": "Recipe availability, upstream playability and GetAll execution are separate. Unknown is not failure or success.",
        "games": len(catalog["games"]), "projects": len(projects),
        "main_covered": sum(r["main_covered"] for r in rows),
        "development_covered": sum(r["development_covered"] for r in rows),
        "missing": sum(not r["development_covered"] for r in rows),
        "preparation_only": sum(r["preparation_only"] for r in rows),
        "validated": sum(r["validated"] for r in rows),
        "legacy_validated_is_execution_evidence": False,
        "dimension_counts": totals, "historical_excluded_recipes": historical_excluded, "rows": rows,
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--main-index")
    parser.add_argument("--development-index", default="index.json")
    parser.add_argument("--eligibility")
    parser.add_argument("--excluded-projects")
    parser.add_argument("--evidence", default="docs/installation-evidence.json")
    parser.add_argument("--evidence-root", default=".", help="Root used to verify local evidence hashes")
    parser.add_argument("--output")
    args = parser.parse_args()
    catalog, eligibility, excluded = load_scope(args.catalog, eligibility_source=args.eligibility, exclusions_source=args.excluded_projects)
    current = load(args.development_index)
    report = coverage(catalog, load(args.main_index) if args.main_index else {"recipes": []}, current,
                      eligibility=eligibility, exclusions=excluded,
                      evidence=load(args.evidence) if args.evidence else None, evidence_root=args.evidence_root)
    report["main_comparison"] = args.main_index or "not_requested"
    if not args.main_index:
        report["main_covered"] = None
        for row in report["rows"]:
            row["main_covered"] = None
    encoded = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")

if __name__ == "__main__":
    main()
