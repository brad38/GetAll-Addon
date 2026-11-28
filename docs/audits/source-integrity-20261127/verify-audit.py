#!/usr/bin/env python3
"""Verify audit coverage, hashes and local references; never build or run games."""
from pathlib import Path
import argparse
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--desktop", type=Path, default=HERE.parents[2].parent / "audit-desktop-source")
parser.add_argument("--write-result", action="store_true")
args = parser.parse_args()
errors = []


def check(condition, label):
    if not condition:
        errors.append(label)


def read(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


catalog = read("catalog-review.json")
routing = read("service-routing-review.json")
root = read("root-review.json")
matrix = read("audit-matrix.json")
helpers = read("native-helpers-review.json")
rows = matrix["projects"]
ids = {r["project_id"] for r in rows}
check(len(rows) == len(ids) == 148, "148 unique catalog IDs")
check(sum(bool(r["has_recipe"]) for r in rows) == 142, "142 recipe-backed IDs")
check(sum(len(r["recipes"]) for r in rows) == 145, "145 recipe entries")
check(sum(not r["has_recipe"] for r in rows) == 6, "six missing recipes")
check({r["project_id"] for r in catalog["projects"]} == ids, "catalog reconciliation")
check({r["project_id"] for r in routing["projects"]} == ids, "routing reconciliation")
check(all(r["routes"] for r in rows if r["has_recipe"]), "every recipe ID has a route")
check(all(r["classification"] for r in rows), "every ID has classification")
source_ids = {i for g in root["source_change_groups"] for i in g["project_ids"]}
other_ids = {i for g in root["other_reviewed_build_groups"] for i in g["project_ids"]}
delegated = {r["project_id"] for r in routing["recipes"] if r["review_scope"].endswith("body_delegated")}
check(len(source_ids) == 19 and len(other_ids) == 14, "19 source-change and 14 additional build IDs")
check(not source_ids & other_ids, "source-change/additional groups disjoint")
check(source_ids | other_ids == delegated, "every delegated handler has body review")
check(all(i in ids for f in helpers["findings"] for i in f["projects"]), "helper project IDs valid")

repo = HERE.parents[2]
recipe_checked = 0
for row in rows:
    for recipe in row["recipes"]:
        path = repo / recipe["path"]
        check(path.is_file(), f'recipe exists: {recipe["path"]}')
        if path.is_file():
            check(hashlib.sha256(path.read_bytes()).hexdigest() == recipe["sha256"], f'recipe hash: {recipe["path"]}')
            recipe_checked += 1
    for report in row["evidence_reports"]:
        check((HERE / report).is_file(), f"report exists: {report}")

manifest = read("desktop-snapshot-manifest.json")
entries = {e["path"]: e for e in manifest["entries"]}
check(len(entries) == 538 and len(manifest["included"]) == 521, "snapshot inventory")
snapshot_checked = 0
if args.desktop.is_dir():
    for path in manifest["included"]:
        file = args.desktop / path
        check(file.is_file(), f"snapshot file exists: {path}")
        if not file.is_file():
            continue
        data = file.read_bytes()
        entry = entries[path]
        check(hashlib.sha256(data).hexdigest() == entry["sha256"], f"snapshot sha256: {path}")
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        check(blob == entry["git_blob"], f"snapshot Git blob: {path}")
        snapshot_checked += 1
    for group in root["source_change_groups"] + root["other_reviewed_build_groups"]:
        for path in group["sources"]:
            check((args.desktop / path).is_file(), f"root source reference: {path}")
else:
    errors.append("Desktop snapshot missing; pass --desktop")

markdown_rows = [x for x in (HERE / "MATRIZ-148.md").read_text().splitlines() if re.match(r"\| \d+ \|", x)]
check(len(markdown_rows) == 148, "148 Markdown matrix rows")
for name in ["README.md", "MATRIZ-148.md"]:
    for target in re.findall(r"\]\(([^)]+)\)", (HERE / name).read_text()):
        if "://" in target or target.startswith("#"):
            continue
        check((HERE / target.split("#")[0]).is_file(), f"local Markdown link: {name} -> {target}")

rex = read("rex-review.json")
check(rex["overlay_entries"] == 86 and rex["text_overlay_entries"] == 82 and rex["binary_overlay_entries"] == 4, "Rex overlay totals")
check(rex["upstream_exact_text_entries"] + rex["allfix_modified_or_added_overlay_entries"] == 86, "Rex attribution reconciliation")
check(rex["upstream_patch_replays"] == 22 and rex["patch_replay_errors"] == 0, "official patch replay evidence")

result = {"status": "pass" if not errors else "fail", "kind": "audit_artifact_consistency_not_gameplay_test",
          "catalog_ids": len(ids), "recipe_entries_verified": recipe_checked,
          "snapshot_files_blob_and_sha256_verified": snapshot_checked,
          "source_change_ids": len(source_ids), "other_build_ids": len(other_ids),
          "errors": errors}
if args.write_result:
    (HERE / "audit-validation.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))
