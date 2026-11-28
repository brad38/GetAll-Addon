"""Inspect the published launcher source for documented non-interactive contracts."""
import pathlib,json,urllib.request,hashlib,concurrent.futures,re
ROOT=pathlib.Path(__file__).resolve().parent
repo="MorsGames/sm64plus-launcher"
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"GetAll-Official-Review"}),timeout=45) as r:return r.read()
meta=json.loads(get("https://api.github.com/repos/"+repo))
sha=json.loads(get("https://api.github.com/repos/"+repo+"/commits/"+meta["default_branch"]))["sha"]
tree=json.loads(get("https://api.github.com/repos/"+repo+"/git/trees/"+sha+"?recursive=1"))
files=[x["path"] for x in tree["tree"] if x["type"]=="blob" and (x["path"].endswith((".gml",".bat",".sh")) or x["path"]=="README.md")]
def inspect(path):
 url="https://raw.githubusercontent.com/"+repo+"/"+sha+"/"+path
 data=get(url);out=ROOT/"research-cache/sm64plus-launcher"/path;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data)
 matches=[]
 for number,line in enumerate(data.decode("utf-8-sig",errors="replace").splitlines(),1):
  if re.search(r"parameter_(?:count|string)|(?:baserom|\.z64|git clone|msys|--build|--prepare|\.bat)",line,re.I):
   matches.append({"line":number,"text":line[:800]})
 return {"path":path,"url":url,"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),"matches":matches}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(inspect,files))
report={"repository":repo,"commit":sha,"source_files_scanned":len(files),"tree_truncated":tree["truncated"],"files":results}
(ROOT/"sm64plus-launcher-source-review.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
print(json.dumps({"repository":repo,"commit":sha,"source_files_scanned":len(files),"files_with_matches":[x for x in results if x["matches"]]},ensure_ascii=True,indent=2)[:22000])
