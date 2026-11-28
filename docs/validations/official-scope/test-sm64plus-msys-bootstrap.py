"""Isolated official MSYS2 bootstrap; no ROM, game boot or user MSYS2 mutation."""
import pathlib,subprocess,hashlib,json,os,uuid,time
ROOT=pathlib.Path(__file__).resolve().parent;BASE=ROOT.parents[3]
stage=BASE/"g-msys-official-test";archive=ROOT/"research-cache/sm64plus-msys/msys2-base-x86_64-20261120.sfx.exe"
if stage.exists():raise SystemExit("Refusing occupied staging path")
stage.mkdir();owner=str(uuid.uuid4());(stage/".owner").write_text(owner,encoding="ascii")
receipt={"scope":"isolated official toolchain bootstrap only; no original media","stage":str(stage),"owner":owner,"steps":[]}
env=os.environ.copy()
for name in ["APPDATA","LOCALAPPDATA","USERPROFILE","TEMP","TMP"]:
 directory=stage/("profile-"+name.lower());directory.mkdir();env[name]=str(directory)
env["MSYSTEM"]="MINGW64";env["CHERE_INVOKING"]="yes"
env["PATH"]=str(pathlib.Path(env.get("SystemRoot","C:/Windows"))/"System32")
def step(label,args,timeout=600):
 start=time.monotonic()
 p=subprocess.run([str(x) for x in args],cwd=stage,env=env,stdin=subprocess.DEVNULL,capture_output=True,timeout=timeout,encoding="utf-8",errors="replace")
 log=ROOT/("sm64plus-msys-"+label+".log");log.write_text(p.stdout+p.stderr,encoding="utf-8",newline="\n")
 row={"name":label,"arguments":[str(x) for x in args],"exit_code":p.returncode,"seconds":round(time.monotonic()-start,2),"log":log.name,"log_sha256":hashlib.sha256(log.read_bytes()).hexdigest()}
 receipt["steps"].append(row);(ROOT/"sm64plus-msys-bootstrap-result.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8",newline="\n")
 print(json.dumps(row),flush=True);return p
assert hashlib.sha256(archive.read_bytes()).hexdigest()=="4f6dadfdb2c9be5fc1938e30b635cb72bb4344c35e8b6fd225bc3250fcab5897"
if step("extract",[archive,"-y","-o"+str(stage)]).returncode:raise SystemExit(1)
bash=stage/"msys64/usr/bin/bash.exe"
if step("initialize",[bash,"-lc"," "]).returncode:raise SystemExit(1)
# The official CI setup explicitly repeats the update after a core-runtime restart.
step("update-core",[bash,"-lc","pacman --noconfirm -Syuu"],900)
if step("update-normal",[bash,"-lc","pacman --noconfirm -Syuu"],900).returncode:raise SystemExit(1)
packages="git make python3 mingw-w64-x86_64-gcc mingw-w64-x86_64-SDL2 mingw-w64-x86_64-glew"
if step("dependencies",[bash,"-lc","pacman -S "+packages+" --noconfirm --needed"],900).returncode:raise SystemExit(1)
step("versions",[bash,"-lc","pacman -Q; printf '\\nSHELL OPTIONS\\n'; set -o; printf '\\nPATH\\n'; command -v gcc make python git"])
print("Official isolated bootstrap and dependencies completed; no ROM or game execution.",flush=True)
