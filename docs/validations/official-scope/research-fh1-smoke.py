import pathlib,json,hashlib,subprocess,os
ROOT=pathlib.Path(__file__).resolve().parent;BASE=ROOT.parents[3]
kit=BASE/"evidence-r18/forza-svod/05f3d8f5b259453f82975a56c3005200/games/Forza Horizon - fh1-reimagined v0.3.9"
manifest=json.loads((kit/"windows-build-manifest.json").read_text(encoding="utf-8-sig"))
failures=[];total=0
for entry in manifest["files"]:
 p=kit/entry["path"]
 if not p.is_file() or p.stat().st_size!=entry["size"] or hashlib.sha256(p.read_bytes()).hexdigest()!=entry["sha256"]:failures.append(entry["path"])
 else:total+=entry["size"]
result={"kit":str(kit),"source_commit":manifest["source_commit"],"manifest_sha256":hashlib.sha256((kit/"windows-build-manifest.json").read_bytes()).hexdigest(),"files_verified":len(manifest["files"])-len(failures),"payload_bytes_verified":total,"failures":failures,"tests":[]}
if not failures:
 env=os.environ.copy();env["APPDATA"]=str(ROOT/"research-cache/fh1/cli-test/config");env["LOCALAPPDATA"]=str(ROOT/"research-cache/fh1/cli-test/data")
 for args in [["--version"],["--build","--help"]]:
  try:
   p=subprocess.run([str(kit/"forza-launcher.exe"),*args],cwd=kit,env=env,capture_output=True,timeout=30,text=True,encoding="utf-8",errors="replace")
   result["tests"].append({"arguments":args,"exit_code":p.returncode,"stdout":p.stdout,"stderr":p.stderr,"classification":"official-cli-only; no game build, media, boot or gameplay"})
  except Exception as e:result["tests"].append({"arguments":args,"error":repr(e)})
(ROOT/"fh1-official-cli-smoke.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8",newline="\n")
print(json.dumps(result,indent=2))
