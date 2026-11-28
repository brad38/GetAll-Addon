"""Remove only the verified source-ZIP fixture duplicate and this run's transfer copy."""
import base64, hashlib, json, shutil, stat
from datetime import datetime, timezone
from pathlib import Path
B=Path(r"C:\Users\bradg\Downloads\GetAll-R18")
F=B/"evidence-r18/flow-completion-20261127"
W=B/"evidence-r18/three-upstreams-20261127/metaforce-policy-build31d"
CACHE=B/"console-cache/metaforce-de8fc69-source.zip"
TARGET=F/"cleanup-policy31d"
ZIP_SHA="e130131a1a41e8599541d8ab3dd2f31c6d8abaa9af03411f8bba25c3f5b63f21"
def require(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):
    with p.open("rb") as s:return hashlib.file_digest(s,"sha256").hexdigest()
def info(p):return {"path":str(p),"bytes":p.stat().st_size,"sha256":sha(p)}
def safe(p):
    for x in [p,*p.parents]:
        st=x.lstat();require(not stat.S_ISLNK(st.st_mode) and not getattr(st,"st_file_attributes",0)&1024,"Linked path: "+str(x))
def snapshot():
    rows=[]
    for p in sorted(W.rglob("*")):
        safe(p)
        if p.is_file():rows.append(info(p))
    return rows
require(not TARGET.exists(),"New cleanup receipt directory is required")
require((W/"AUTHORED_ONLY.txt").read_text()=="Official public source ZIP plus authored media/output fixtures. No native Metaforce build or commercial boot.\n","Unknown fixture owner")
proof=json.loads((W/"result.json").read_text());require(proof["passed"]==52 and proof["commercialMediaAccepted"] is False and proof["gameExecuted"] is False,"Policy proof did not pass")
gate=F/"build31d-result.json";gate_before=info(gate);require(json.loads(gate.read_text())["status"]=="PASS","Integrated gate did not pass")
before=snapshot();copies=list(W.rglob("source.zip"));require(len(copies)==1,"Ambiguous source fixture duplicate")
source=copies[0];cache_before=info(CACHE);safe(CACHE)
require(cache_before["bytes"]==21536851 and cache_before["sha256"]==ZIP_SHA,"Shared source cache changed")
require(info(source)["bytes"]==21536851 and sha(source)==ZIP_SHA,"Fixture is not an identical cache duplicate")
transfer=F/"evidence-transfer31d.zip.b64";safe(transfer)
raw=base64.b64decode(transfer.read_bytes(),validate=True)
require(transfer.stat().st_size==121832 and len(raw)==91372 and hashlib.sha256(raw).hexdigest()=="8de9f8dff45e0939846b6bbd8d1461b762cc28c1efc6301b56d48636d146ca4c","Unknown transfer copy")
removals=[info(source),info(transfer)];expected=[x for x in before if x["path"]!=str(source)]
free_before=shutil.disk_usage(B).free
TARGET.mkdir()
(TARGET/"before.json").write_text(json.dumps({"policy_files":before,"delete":removals,"source_cache":cache_before,"gate":gate_before},ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
for item in removals:
    p=Path(item["path"]);require(info(p)==item,"Disposable changed before deletion");p.unlink()
after=snapshot();require(after==expected,"Preserved policy files changed")
require(info(CACHE)==cache_before and info(gate)==gate_before,"Shared cache or gate changed")
result={"status":"PASS","completed_utc":datetime.now(timezone.utc).isoformat(),"removed_files":len(removals),"removed_bytes":sum(x["bytes"] for x in removals),"removed":removals,"policy_preserved_files":len(after),"policy_preserved_bytes":sum(x["bytes"] for x in after),"source_cache_preserved":cache_before,"integrated_gate_preserved":gate_before,"free_before":free_before,"free_after":shutil.disk_usage(B).free,"before_manifest":info(TARGET/"before.json"),"limits":"Only a task-owned source ZIP duplicate and base64 transport copy were removed. The old fixture kit is now intentionally incomplete; reproduce in a new work path. No original media, personal data, active build, harness, toolchain or shared dependency was removed."}
(TARGET/"result.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
print(json.dumps(result,ensure_ascii=False))
