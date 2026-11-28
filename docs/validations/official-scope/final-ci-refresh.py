from pathlib import Path
import os,subprocess,json,hashlib,time,datetime
root=Path(__file__).resolve().parents[3]
out=root/"docs/validations/official-scope"
p=out/"refresh-final-summary.py"
s=p.read_text(encoding="utf8")
s=s.replace('start=text.index("A pesquisa e os registros de catálogo")','start=text.index("A pesquisa e os registros de catálogo") if "A pesquisa e os registros de catálogo" in text else text.index("A revisão final registra")')
old="""As receitas desativadas preservam variantes antigas e duas identidades retiradas
do catálogo. A contagem de 12 receitas desativadas não significa 12 projetos
sem procedimento ativo: SM64Plus, SSX, CTR, Burnout 3, Dr. Mario, Metaforce e MKW
têm outra rota ativa. Os três projetos sem contrato ativo são StrikersRecomp,
VandalHearts-PcPort e REDRIVER2."""
new="""As 12 receitas desativadas se dividem em **cinco IDs arquivados** (GGA64,
Burnout 3, o agregado Sonic 1 Forever/Sonic 2 Absolute, Dr. Mario 64 base e
Metaforce), **quatro variantes antigas com outra receita ativa no mesmo projeto**
(SM64Plus, SSX, CTR e MKW) e **três projetos elegíveis bloqueados**
(StrikersRecomp, VandalHearts-PcPort e REDRIVER2). Dr. Mario 64 Plus é um projeto
distinto; sua presença não reativa o ID base. Burnout 3 e Metaforce não têm
uma rota ativa nem permanecem no catálogo atual."""
assert old in s
s=s.replace(old,new)
p.write_text(s,encoding="utf8",newline="\n")
exe=root.parent/".venv-validation-r18/Scripts/python.exe"
env=dict(os.environ,PYTHONUTF8="1",GITHUB_REF="refs/heads/work/official-install-scope-20261127",GITHUB_EVENT_NAME="workflow_dispatch")
env.pop("GITHUB_BASE_REF",None)
args=[str(exe),"scripts/validate_ci.py"]
start=time.monotonic()
r=subprocess.run(args,cwd=root,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
log=out/"final-ci-local.log"
log.write_text(r.stdout.decode("utf8").replace("\r\n","\n"),encoding="utf8",newline="\n")
result=dict(test="final-ci-local",command=args,exit_code=r.returncode,seconds=round(time.monotonic()-start,3),log=log.relative_to(root).as_posix(),sha256=hashlib.sha256(log.read_bytes()).hexdigest())
receipt=json.loads((out/"final-validation-results.json").read_text(encoding="utf8"))
receipt["results"][1]=result
receipt["checked_at"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
(out/"final-validation-results.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf8",newline="\n")
print(json.dumps(result),flush=True)
print(r.stdout.decode("utf8")[-2000:],flush=True)
assert r.returncode==0
subprocess.run([str(exe),str(out/"refresh-final-summary.py")],cwd=root,env=env,check=True)
