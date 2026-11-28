"""Initialize the official private pacman keyring when an existing HOME skipped first-run hooks."""
import pathlib,subprocess,hashlib,json,os,time
ROOT=pathlib.Path(__file__).resolve().parent;BASE=ROOT.parents[3];stage=BASE/"g-msys-official-test"
receipt_path=ROOT/"sm64plus-msys-bootstrap-result.json";receipt=json.loads(receipt_path.read_text())
assert receipt["stage"]==str(stage) and (stage/".owner").read_text()==receipt["owner"]
env=os.environ.copy()
for name in ["APPDATA","LOCALAPPDATA","USERPROFILE","TEMP","TMP"]:
 directory=stage/("profile-"+name.lower());directory.mkdir(exist_ok=True);env[name]=str(directory)
env["MSYSTEM"]="MINGW64";env["CHERE_INVOKING"]="yes"
env["PATH"]=str(pathlib.Path(env.get("SystemRoot","C:/Windows"))/"System32")
bash=stage/"msys64/usr/bin/bash.exe"
def step(label,command,timeout=900):
 args=[str(bash),"-lc",command];start=time.monotonic()
 p=subprocess.run(args,cwd=stage,env=env,stdin=subprocess.DEVNULL,capture_output=True,timeout=timeout,encoding="utf-8",errors="replace")
 log=ROOT/("sm64plus-msys-"+label+".log");log.write_text(p.stdout+p.stderr,encoding="utf-8",newline="\n")
 row={"name":label,"arguments":args,"exit_code":p.returncode,"seconds":round(time.monotonic()-start,2),"log":log.name,"log_sha256":hashlib.sha256(log.read_bytes()).hexdigest()}
 receipt["steps"].append(row);receipt_path.write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8",newline="\n");print(json.dumps(row),flush=True);return p
if step("keyring","pacman-key --init && pacman-key --populate msys2").returncode:raise SystemExit(1)
step("resume-update-core","pacman --noconfirm -Syuu")
if step("resume-update-normal","pacman --noconfirm -Syuu").returncode:raise SystemExit(1)
packages="git make python3 mingw-w64-x86_64-gcc mingw-w64-x86_64-SDL2 mingw-w64-x86_64-glew"
if step("dependencies","pacman -S "+packages+" --noconfirm --needed").returncode:raise SystemExit(1)
step("versions","pacman -Q; printf '\\nSHELL OPTIONS\\n'; set -o; printf '\\nPATH\\n'; command -v gcc make python git")
print("Official isolated bootstrap and dependencies completed; no ROM or game execution.",flush=True)
