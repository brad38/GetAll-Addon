"""Read-only inventory for removal of the redundant SDK169 candidate and failed harness outputs."""
import base64, hashlib, json, stat, zlib
from datetime import datetime, timezone
from pathlib import Path
B=Path(r'C:\Users\bradg\Downloads\GetAll-R18');F=B/'evidence-r18/flow-completion-20261127'
C=B/'publish-desktop-final-sdk169-20261127';P=B/'publish-getall-sdk169-20261127'
def require(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):
    with p.open('rb') as s:return hashlib.file_digest(s,'sha256').hexdigest()
def safe(p):
    for x in [p,*p.parents]:
        st=x.lstat();require(not stat.S_ISLNK(st.st_mode) and not getattr(st,'st_file_attributes',0)&1024,'Linked path: '+str(x))
def info(p,root):return {'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)}
def inventory(root):
    safe(root);rows=[]
    for p in root.rglob('*'):
        safe(p)
        if p.is_file():rows.append(info(p,root))
    return sorted(rows,key=lambda x:x['path'])
require(sha(C/'ARTIFACT-MANIFEST.json')=='aa85bbe915f2a8d975a8fa0139dea79d145d8c0a0107464941505a7f528a01e3','Candidate pin changed')
require(sha(P/'ARTIFACT-MANIFEST.json')=='18cbb75144560fbacbe20708b0b3a63a95577d85490a814cc4dece4d770d9590','Final preview pin changed')
candidate=json.loads((C/'ARTIFACT-MANIFEST.json').read_text());complete=json.loads((P/'ARTIFACT-MANIFEST.json').read_text())
require((candidate['sdk_version'],candidate['desktop_commit'],candidate['addon_included'])==('1.5.69','921295de12349e726f7ca21a5edd8a8ecee123d8',False),'Unexpected candidate contract')
require(complete['sdk_version']=='1.5.69' and complete['desktop_commit']==candidate['desktop_commit'] and complete['addon_included'] is True,'Unexpected complete preview contract')
ci=inventory(C);pi=inventory(P)
def check_manifest(root,rows,manifest):
    expected=[{'path':x['name'],'bytes':x['bytes'],'sha256':x['sha256']} for x in manifest['artifacts']]
    actual=[x for x in rows if x['path'] not in ('ARTIFACT-MANIFEST.json','SHA256SUMS.txt')]
    require(actual==sorted(expected,key=lambda x:x['path']),'Artifact inventory changed: '+str(root))
check_manifest(C,ci,candidate);check_manifest(P,pi,complete)
final_map={x['path']:x for x in pi}
for item in candidate['artifacts']:
    require(final_map.get(item['name'])=={'path':item['name'],'bytes':item['bytes'],'sha256':item['sha256']},'Candidate payload missing/different in final preview: '+item['name'])
groups=[{'name':'desktop-candidate-duplicate','root':str(C),'files':ci}]
failed=[]
for suffix in ('31','31b','31c'):
    root=F/('harness-build'+suffix);gate=F/('build'+suffix+'-result.json')
    result=json.loads(gate.read_text());require(result['status']=='FAILED','Only failed outputs may be removed: '+suffix)
    require(root.is_dir(),'Failed output missing: '+str(root))
    rows=inventory(root)
    require(all(Path(x['path']).suffix.lower() in ('.dll','.exe','.pdb','.json') for x in rows),'Unexpected failed output member type')
    groups.append({'name':'failed-build'+suffix,'root':str(root),'files':rows})
    failed.append({'path':str(gate),'bytes':gate.stat().st_size,'sha256':sha(gate)})
preserve=[]
for root in (B/'publish-getall-complete-flows-20261127',B/'publish-getall-sdk168-20261127',P,F/'harness-build30',F/'harness-build31d'):
    preserve.append({'root':str(root),'files':pi if root==P else inventory(root)})
plan={'schema':1,'created_utc':datetime.now(timezone.utc).isoformat(),'action':'PREPARED_ONLY_NO_REMOVAL','task_root':str(B),'groups':groups,'candidate_payload_files_verified_identical':len(candidate['artifacts']),'candidate_receipts_to_archive':['ARTIFACT-MANIFEST.json','SHA256SUMS.txt','RESOURCE-AUDIT.json'],'preserved_roots':preserve,'preserved_failed_gate_results':failed,'candidate_manifest_sha256':sha(C/'ARTIFACT-MANIFEST.json'),'complete_preview_manifest_sha256':sha(P/'ARTIFACT-MANIFEST.json'),'execute_requires_coordinator_signal':True}
raw=(json.dumps(plan,ensure_ascii=False,indent=2)+'\n').encode()
summary={'groups':[{'root':x['root'],'files':len(x['files']),'bytes':sum(y['bytes'] for y in x['files'])} for x in groups],'files':sum(len(x['files']) for x in groups),'bytes':sum(y['bytes'] for x in groups for y in x['files']),'preserved_roots':len(preserve),'preserved_files':sum(len(x['files']) for x in preserve),'plan_bytes':len(raw),'plan_sha256':hashlib.sha256(raw).hexdigest()}
print('PLAN_B64='+base64.b64encode(zlib.compress(raw)).decode())
print('PLAN_SUMMARY='+json.dumps(summary,ensure_ascii=False))
