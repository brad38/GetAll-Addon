import pathlib,subprocess,json,hashlib,os,time,shutil
root=pathlib.Path(__file__).resolve().parent;stage=root.parents[3]/"g-msys-official-test"
source=root/"research-cache/vandal-source/source";build=stage/"vandal-cmake-configure"
env=os.environ.copy();msys=stage/"msys64";env["PATH"]=str(msys/"mingw64/bin")+";"+str(msys/"usr/bin")+";"+env["PATH"]
for k in ["APPDATA","LOCALAPPDATA","USERPROFILE","TEMP","TMP"]:env[k]=str(stage/("profile-"+k.lower()))
cmake=shutil.which("cmake");ninja=shutil.which("ninja")
args=[cmake,"-S",str(source/"platform/pc"),"-B",str(build),"-G","Ninja","-DCMAKE_MAKE_PROGRAM="+str(ninja),
 "-DCMAKE_C_COMPILER="+str(msys/"mingw64/bin/gcc.exe"),"-DCMAKE_PREFIX_PATH="+str(msys/"mingw64")]
t=time.monotonic();p=subprocess.run(args,env=env,cwd=stage,stdin=subprocess.DEVNULL,capture_output=True,timeout=180)
def decode_output(data):
 try:return data.decode("utf-8")
 except UnicodeDecodeError:return data.decode("cp1252")
p.stdout=decode_output(p.stdout);p.stderr=decode_output(p.stderr)
log=root/"vandal-native-configure.log";log.write_text((p.stdout+p.stderr).replace("\r\n","\n").replace("\r","\n"),encoding="utf-8",newline="\n")
r=dict(scope="unmodified native-Windows CMake configuration only; no game/BIOS data or build",arguments=args,exit_code=p.returncode,seconds=round(time.monotonic()-t,2),log=log.name,log_sha256=hashlib.sha256(log.read_bytes()).hexdigest())
(root/"vandal-native-configure-result.json").write_text(json.dumps(r,indent=2)+"\n",encoding="utf-8",newline="\n");print(json.dumps(r));print((p.stdout+p.stderr)[-8000:])
