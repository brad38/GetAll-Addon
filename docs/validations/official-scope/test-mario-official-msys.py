"""Fetch pinned source trees and exercise official build prerequisites without a ROM."""
import pathlib,json,urllib.request,hashlib,subprocess,os,time,concurrent.futures
HERE=pathlib.Path(__file__).resolve().parent
BASE=HERE.parents[3]; STAGE=BASE/"g-msys-official-test"
BASH=STAGE/"msys64/usr/bin/bash.exe"
env=os.environ.copy()
for k in ["APPDATA","LOCALAPPDATA","USERPROFILE","TEMP","TMP"]:env[k]=str(STAGE/("profile-"+k.lower()))
env.update(MSYSTEM="MINGW64",CHERE_INVOKING="yes",GIT_CONFIG_NOSYSTEM="1",GIT_CONFIG_GLOBAL="/dev/null")
env["PATH"]=str(pathlib.Path(env.get("SystemRoot","C:/Windows"))/"System32")
def run(name,cwd,cmd,timeout=300):
 t=time.monotonic();p=subprocess.run([str(BASH),"-lc",cmd],cwd=cwd,env=env,stdin=subprocess.DEVNULL,capture_output=True,encoding="utf-8",errors="replace",timeout=timeout)
 log=HERE/(name+".log");log.write_text(p.stdout+p.stderr,encoding="utf-8",newline="\n")
 row=dict(name=name,command=cmd,exit_code=p.returncode,seconds=round(time.monotonic()-t,2),log=log.name,log_sha256=hashlib.sha256(log.read_bytes()).hexdigest())
 print(json.dumps(row),flush=True);return row
projects=[("sm64ex","sm64pc/sm64ex","d7ca2c04364a6dd0dac58b47151e04e26887e6f0","EXTERNAL_DATA=1"),("render96ex","Render96/Render96ex","48da5c491c8abfb2f5192b59278c1c269411e533","EXTERNAL_DATA=1"),("sm64rt","DarioSamo/sm64rt","20e618b75ae4a6810bd92ac6a937cb167517aac5","RENDER_API=RT64 EXTERNAL_DATA=1")]
def check(p):
 name,repo,commit,flags=p;src=STAGE/name;src.mkdir(exist_ok=False);rows=[]
 for label,cmd in [("init","git init"),("origin","git remote add origin https://github.com/"+repo+".git"),("fetch","git fetch --depth 1 origin "+commit),("checkout","git checkout --detach FETCH_HEAD")]:
  r=run(name+"-"+label,src,cmd);rows.append(r)
  if r["exit_code"]:return dict(project=name,repo=repo,commit=commit,steps=rows,blocked="clone")
 rows.append(run(name+"-head",src,"git rev-parse HEAD"))
 # This official tools Makefile is independent of extraction and commercial assets.
 rows.append(run(name+"-tools",src,"make -C tools -j2 all-except-recomp",600))
 rows.append(run(name+"-missing-rom",src,"make -j2 "+flags,120))
 rows.append(run(name+"-source-integrity",src,"git diff --exit-code && git status --porcelain --untracked-files=no"))
 return dict(project=name,repo=repo,commit=commit,flags=flags,steps=rows)
result={"scope":"official tools compilation and missing-ROM negatives; no original media, full game build, boot or gameplay","projects":[]}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for p in pool.map(check,projects):result["projects"].append(p)
result["sm64plus_tools"]=run("sm64plus-official-tools",STAGE/"launcher/sm64plus","make -C tools -j2 all-except-recomp",600)
(HERE/"mario-official-msys-preflight.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8",newline="\n")
