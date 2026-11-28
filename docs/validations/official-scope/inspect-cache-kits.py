import pathlib,hashlib,json,zipfile,subprocess
ROOT=pathlib.Path(__file__).resolve().parent;BASE=ROOT.parents[3]
result={}
for name in ["PinyonShift-Launcher.zip","pinyon-850518c.zip"]:
 p=BASE/"console-cache"/name
 with zipfile.ZipFile(p) as z:
  names=z.namelist()
  result[name]={"bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"files":len(names),"sample":names[:12],"important":[n for n in names if n.lower().endswith(("release-toolchain.json","supported-dumps.json","windows-build-manifest.json","pinyonshift.launcher.exe"))]}
  if name=="pinyon-850518c.zip":
   for n in names:
    if n.endswith(("config/release-toolchain.json","config/supported-dumps.json")):
     out=ROOT/"research-cache"/"pinyon"/pathlib.PurePosixPath(n).relative_to(n.split("/")[0]);out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(z.read(n))
found=[]
for man in (BASE/"evidence-r18"/"forza-svod").glob("*/games/*/windows-build-manifest.json"):
 root=man.parent; data=json.loads(man.read_text(encoding="utf-8-sig"))
 found.append({"path":str(root),"manifest_type":type(data).__name__,"keys":list(data)[:10],"files":len(data.get("files",[])) if isinstance(data,dict) else len(data),"exe":str(root/"launcher"/"forza-launcher.exe"),"exe_exists":(root/"launcher"/"forza-launcher.exe").exists()})
result["fh1_candidates"]=found
(ROOT/"official-cache-kit-inspection.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8",newline="\n")
print(json.dumps(result,indent=2))
