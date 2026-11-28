"""Fetch immutable official installation sources for the scope review; never execute them."""
from __future__ import annotations
import concurrent.futures, hashlib, json, pathlib, re, urllib.request
ROOT = pathlib.Path(__file__).resolve().parent
CACHE = ROOT / "research-cache"
TASKS = [
    ("ssx", "AmarilloNL/ssx-recomp", "v2.0.1"),
    ("pinyon", "arcanite24/pinyon-shift", "v0.9.5"),
    ("fh1", "FH1-ReImagined/ForzaHorizon1-ReImagined", "v0.3.9"),
    ("gow", "danielalves96/gow-pc-port", "launcher-v0.4.0"),
]
def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent":"GetAll-Official-Scope-Review"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()
def review(task):
    short, repo, tag = task
    base = "https://api.github.com/repos/" + repo
    obj = json.loads(fetch(base + "/git/ref/tags/" + tag))["object"]
    if obj["type"] == "tag":
        obj = json.loads(fetch(base + "/git/tags/" + obj["sha"]))["object"]
    sha = obj["sha"]
    tree = json.loads(fetch(base + "/git/trees/" + sha + "?recursive=1"))
    paths = [f["path"] for f in tree["tree"] if f["type"] == "blob"]
    selected = [p for p in paths if p.lower() in {
        "readme.md", "recomplauncher.json", "installer/ssxinstaller.cs",
        "docs/install.md", "docs/launcher.md", "install.ps1", "scripts/build-ssx.ps1",
    }]
    candidates = [p for p in paths if re.search(r"(launcher|installer|install|prepare|build).*\.(py|cs|cpp|rs|ps1|json)$", p, re.I)]
    records = []
    for path in selected:
        url = "https://raw.githubusercontent.com/" + repo + "/" + sha + "/" + path
        data = fetch(url)
        out = CACHE / short / path
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
        lines = data.decode("utf-8-sig", errors="replace").splitlines()
        hits = [i for i,line in enumerate(lines) if re.search(r"(--prepare|--game|--folder|--iso|headless|command.line|param\(|-IsoPath|-GamePath|dist[/\\]SSX|GamePath|Environment.GetCommandLineArgs)",line,re.I)]
        excerpts = [{"line":i+1,"text":"\n".join(lines[max(0,i-2):i+4])} for i in hits[:30]]
        records.append({"path":path,"url":url,"sha256":hashlib.sha256(data).hexdigest(),"bytes":len(data),"local":str(out),"excerpts":excerpts})
    return {"project":short,"repository":repo,"tag":tag,"commit":sha,"tree_truncated":tree.get("truncated"),"candidate_sources":candidates,"sources":records}
def main():
    CACHE.mkdir(parents=True,exist_ok=True)
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for task, future in zip(TASKS, [pool.submit(review,t) for t in TASKS]):
            try: results.append(future.result())
            except Exception as exc: results.append({"project":task[0],"error":repr(exc)})
    (ROOT/"official-alternative-sources.json").write_text(json.dumps({"projects":results},ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    for result in results:
        print(json.dumps({k:v for k,v in result.items() if k!="sources"},ensure_ascii=False))
        for record in result.get("sources",[]): print(json.dumps(record,ensure_ascii=False))
if __name__ == "__main__": main()
