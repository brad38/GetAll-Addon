"""Deterministic coverage report from the canonical catalog and recipe indexes."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

USABLE_STATUSES = frozenset({"experimental", "validated"})

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))

def project_map(catalog):
    result={}
    for game in catalog["games"]:
        for project in game["projects"]:
            key=game["id"],project["id"]
            if key in result:
                raise ValueError(f"Duplicate catalog project {key}")
            result[key]=(game.get("platform_group",""),project)
    return result

def index_map(index):
    result={}
    for entry in index["recipes"]:
        key=entry["game_id"],entry["project_id"]
        result.setdefault(key,[]).append(entry)
    return result

def coverage(catalog, main_index, development_index):
    projects=project_map(catalog)
    main=index_map(main_index)
    development=index_map(development_index)
    for label,entries in (("main",main),("development",development)):
        unknown=set(entries)-set(projects)
        if unknown:
            raise ValueError(f"Orphan recipe IDs in {label}: {sorted(unknown)}")
    rows=[]
    for (game,project),(platform,metadata) in projects.items():
        public=main.get((game,project),[])
        pending=development.get((game,project),[])
        usable_public=[x for x in public if x.get("status") in USABLE_STATUSES]
        usable_pending=[x for x in pending if x.get("status") in USABLE_STATUSES]
        rows.append({"game_id":game,"project_id":project,"platform_group":platform,
                     # Keep every indexed version for inspection, including inactive recipes.
                     "main":public,"development":pending,
                     "main_covered":bool(usable_public),
                     "development_covered":bool(usable_pending),
                     # This legacy schema metric does not establish installation or boot.
                     "preparation_only":bool(usable_pending) and all(x["schema_version"]==9 for x in usable_pending),
                     "validated":any(x["status"]=="validated" for x in usable_pending)})
    return {"games":len(catalog["games"]),"projects":len(projects),
            "main_covered":sum(r["main_covered"] for r in rows),
            "development_covered":sum(r["development_covered"] for r in rows),
            "missing":sum(not r["development_covered"] for r in rows),
            "preparation_only":sum(r["preparation_only"] for r in rows),
            "validated":sum(r["validated"] for r in rows),"rows":rows}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog",required=True)
    parser.add_argument("--main-index",required=True)
    parser.add_argument("--development-index",default="index.json")
    parser.add_argument("--output")
    args=parser.parse_args()
    report=coverage(load(args.catalog),load(args.main_index),load(args.development_index))
    encoded=json.dumps(report,ensure_ascii=False,indent=2)+"\n"
    if args.output:Path(args.output).write_bytes(encoded.encode("utf-8"))
    else: print(encoded,end="")

if __name__=="__main__":
    main()
