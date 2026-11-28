"""Run the review branch's Python suite and the actual local CI entry point."""
import datetime, hashlib, json, os, re, subprocess, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/"docs/validations/official-scope"
environment=dict(os.environ,PYTHONUTF8="1",GITHUB_REF="refs/heads/work/official-install-scope-20261127",GITHUB_EVENT_NAME="workflow_dispatch")
environment.pop("GITHUB_BASE_REF",None)
results=[]
for name,args in [
 ("final-python-tests",[sys.executable,"-m","unittest","discover","-s","tests","-v"]),
 ("final-ci-local",[sys.executable,"scripts/validate_ci.py"]),
]:
    started=time.monotonic()
    result=subprocess.run(args,cwd=ROOT,env=environment,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    text=result.stdout.decode("utf-8").replace("\r\n","\n")
    log=OUT/(name+".log");log.write_text(text,encoding="utf-8",newline="\n")
    row=dict(test=name,command=args,exit_code=result.returncode,seconds=round(time.monotonic()-started,3),log=log.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(log.read_bytes()).hexdigest())
    if match:=re.search(r"Ran (\d+) tests",text):row["tests"]=int(match[1])
    results.append(row)
    print(json.dumps(row),flush=True)
    if result.returncode: print(text[-12000:],flush=True);break
record=dict(checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),catalog_commit="e4fdde9d7c128f79eb19cf99ea07e2e9b628127a",
    index_sha256=hashlib.sha256((ROOT/"index.json").read_bytes()).hexdigest(),results=results,
    scope="Local unit tests and the real CI validation entry point against the published exact catalog commit. Does not claim hosted GetAll CI, game execution or publication of this working tree.")
(OUT/"final-validation-results.json").write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8",newline="\n")
raise SystemExit(any(r["exit_code"] for r in results) or len(results)!=2)
