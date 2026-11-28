"""Pinned official launcher script preflight without commercial game data."""
import pathlib,subprocess,hashlib,json,os,time,zipfile
ROOT=pathlib.Path(__file__).resolve().parent;BASE=ROOT.parents[3];stage=BASE/"g-msys-official-test"
owner=json.loads((ROOT/"sm64plus-msys-bootstrap-result.json").read_text())
assert owner["stage"]==str(stage) and (stage/".owner").read_text()==owner["owner"]
kit=stage/"launcher";kit.mkdir(exist_ok=False)
with zipfile.ZipFile(ROOT/"research-cache/sm64plus-release/SM64Plus.zip") as z:
 z.extractall(kit)
env=os.environ.copy()
for name in ["APPDATA","LOCALAPPDATA","USERPROFILE","TEMP","TMP"]:env[name]=str(stage/("profile-"+name.lower()))
env["MSYSTEM"]="MINGW64";env["CHERE_INVOKING"]="yes";env["GIT_CONFIG_NOSYSTEM"]="1";env["GIT_CONFIG_GLOBAL"]="/dev/null"
env["PATH"]=str(pathlib.Path(env.get("SystemRoot","C:/Windows"))/"System32")
bash=stage/"msys64/usr/bin/bash.exe"
report={"scope":"official clone and missing-media negative preflight; no original ROM, game build, boot or gameplay","commit":"44fccee2fc4bd4768ae4eff1e5c47b21abe5d85d","steps":[]}
def step(label,args,limit=300):
 start=time.monotonic();p=subprocess.run([str(bash),*args],cwd=kit,env=env,stdin=subprocess.DEVNULL,capture_output=True,timeout=limit,encoding="utf-8",errors="replace")
 log=ROOT/("sm64plus-official-"+label+".log");log.write_text(p.stdout+p.stderr,encoding="utf-8",newline="\n")
 row={"name":label,"arguments":args,"exit_code":p.returncode,"seconds":round(time.monotonic()-start,2),"log":log.name,"log_sha256":hashlib.sha256(log.read_bytes()).hexdigest()};report["steps"].append(row)
 print(json.dumps(row),flush=True);return p
assert step("clone",["-lc","git clone --depth 1 --branch master https://github.com/MorsGames/sm64plus.git sm64plus"]).returncode==0
head=step("head",["-lc","git -C sm64plus rev-parse HEAD"]).stdout.strip()
assert head==report["commit"],"Pinned source changed; review required"
step("syntax-crlf",["-lc","bash -n build.sh"])
assert step("syntax-igncr",["-lc","bash -o igncr -n build.sh"]).returncode==0
result=step("missing-rom",["-lc","exec bash -o igncr build.sh 1"],300)
report["missing_rom_rejected"]=result.returncode!=0 and "baserom.us.z64" in result.stdout+result.stderr
report["script_sha256_after"]=hashlib.sha256((kit/"build.sh").read_bytes()).hexdigest()
report["tracked_sources_unchanged"]=step("source-integrity",["-lc","git -C sm64plus diff --exit-code; git -C sm64plus status --porcelain --untracked-files=no"]).returncode==0
report["produced_game"]=any((kit/"sm64plus/build/us_pc").glob("*.exe")) if (kit/"sm64plus/build/us_pc").exists() else False
(ROOT/"sm64plus-official-script-result.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8",newline="\n")
print(json.dumps({k:v for k,v in report.items() if k!="steps"},indent=2))
