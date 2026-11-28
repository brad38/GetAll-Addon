import pathlib,json,subprocess,os,hashlib,time,concurrent.futures
root=pathlib.Path(__file__).resolve().parent;stage=root.parents[3]/"g-msys-official-test"
env=os.environ.copy()
for k in ["APPDATA","LOCALAPPDATA","USERPROFILE","TEMP","TMP"]:env[k]=str(stage/("profile-"+k.lower()))
env.update(MSYSTEM="MINGW64",CHERE_INVOKING="yes",GIT_CONFIG_NOSYSTEM="1",GIT_CONFIG_GLOBAL="/dev/null")
env["PATH"]=str(pathlib.Path(env.get("SystemRoot","C:/Windows"))/"System32")
def check(name):
 src=stage/name;t=time.monotonic();cmd="make -C tools -j2 all"
 p=subprocess.run([str(stage/"msys64/usr/bin/bash.exe"),"-lc",cmd],cwd=src,env=env,stdin=subprocess.DEVNULL,capture_output=True,encoding="utf-8",errors="replace",timeout=600)
 log=root/(name+"-official-tools-all.log");log.write_text(p.stdout+p.stderr,encoding="utf-8",newline="\n")
 r=dict(project=name,command=cmd,exit_code=p.returncode,seconds=round(time.monotonic()-t,2),log=log.name,log_sha256=hashlib.sha256(log.read_bytes()).hexdigest())
 q=subprocess.run([str(stage/"msys64/usr/bin/bash.exe"),"-lc","git diff --exit-code && git status --porcelain --untracked-files=no"],cwd=src,env=env,capture_output=True)
 r["tracked_sources_unchanged"]=q.returncode==0 and not q.stdout
 print(json.dumps(r),flush=True);return r
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(check,["sm64ex","render96ex","sm64rt"]))
(root/"mario-official-tools-all-result.json").write_text(json.dumps({"scope":"Official all target; earlier all-except-recomp probe was inapplicable outside SM64Plus","projects":rows},indent=2)+"\n",encoding="utf-8",newline="\n")
