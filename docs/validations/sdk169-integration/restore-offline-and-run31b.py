import base64,datetime,hashlib,importlib.util,json,os,subprocess,sys,time,types,xml.etree.ElementTree as ET
from pathlib import Path
B=Path(r'C:\Users\bradg\Downloads\GetAll-R18');R=B/'desktop-continuation-20261127';F=B/'evidence-r18'/'flow-completion-20261127'
spec=importlib.util.spec_from_file_location('runner31',F/'run-build31.py');runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
args=types.SimpleNamespace(git=Path(r'C:\Program Files\Git\cmd\git.exe'),desktop=R)
cache=Path(r'C:\Users\bradg\.nuget\packages');out=F/'restore-offline31';out.mkdir()
env=dict(os.environ,DOTNET_CLI_UI_LANGUAGE='en',DOTNET_CLI_TELEMETRY_OPTOUT='1',DOTNET_NOLOGO='1')
projects=[R/'Tests'/'AddonInfrastructure'/'AddonInfrastructure.csproj',R/'AddonSdk'/'AllFix.Addons.Sdk.csproj']
expected=[('SharpCompress','0.50.4'),('System.IO.Hashing','8.0.0')]
actual=[(x.attrib['Include'],x.attrib['Version']) for x in ET.parse(projects[0]).findall('.//PackageReference')]
assert actual==expected and not ET.parse(projects[1]).findall('.//PackageReference')
package_dirs=[cache/name.lower()/version for name,version in expected]
for (name,version),p in zip(expected,package_dirs):
 archive=p/(name.lower()+'.'+version+'.nupkg');stamp=p/(name.lower()+'.'+version+'.nupkg.sha512')
 assert archive.is_file() and stamp.is_file()
 assert hashlib.sha512(archive.read_bytes()).digest()==base64.b64decode(stamp.read_text().strip())
 root=ET.parse(p/(name.lower()+'.nuspec')).getroot()
 groups=[n for n in root.iter() if n.tag.endswith('group') and n.attrib.get('targetFramework')=='net8.0']
 assert len(groups)==1 and len(groups[0])==0
def cached():
 rows=[]
 for d in package_dirs:
  for p in sorted(d.rglob('*')):
   if p.is_file():rows.append({'path':str(p),'bytes':p.stat().st_size,'sha256':runner.digest(p)})
 return rows
before_sources=runner.source_manifest(args);before_git=runner.git_state(args);before_cache=cached()
runner.write_json(out/'sources-before.json',before_sources);runner.write_json(out/'git-before.json',before_git);runner.write_json(out/'cache-before.json',before_cache)
config=out/'NuGet.Config'
with config.open('x',encoding='utf-8',newline='\n') as stream:stream.write('<?xml version="1.0" encoding="utf-8"?>\n<configuration><packageSources><clear /></packageSources><fallbackPackageFolders><clear /></fallbackPackageFolders></configuration>\n')
command=[r'C:\Program Files\dotnet\dotnet.exe','restore',str(projects[0]),'--configfile',str(config),'--packages',str(cache),'--disable-parallel','--nologo','--verbosity','minimal','-p:NuGetAudit=false']
runner.write_json(out/'request.json',{'command':command,'cache':str(cache),'package_pins':expected,'started_utc':runner.utc(),'sources_cleared':True,'audit_network_disabled':True})
start=time.monotonic()
with (out/'restore.log').open('xb') as stream:completed=subprocess.run(command,cwd=R,env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=120)
after_sources=runner.source_manifest(args);after_git=runner.git_state(args);after_cache=cached()
runner.write_json(out/'sources-after.json',after_sources);runner.write_json(out/'git-after.json',after_git);runner.write_json(out/'cache-after.json',after_cache)
text=(out/'restore.log').read_text(encoding='utf-8-sig',errors='replace')
assets=[p.parent/'obj'/'project.assets.json' for p in projects]
result={'status':'PASS' if completed.returncode==0 and before_sources==after_sources and before_git==after_git and before_cache==after_cache and all(p.is_file() for p in assets) else 'FAILED',
'exit_code':completed.returncode,'seconds':round(time.monotonic()-start,3),'source_inputs_unchanged':before_sources==after_sources,'git_state_unchanged':before_git==after_git,'used_package_cache_unchanged':before_cache==after_cache,
'cache_files':len(before_cache),'assets':[runner.file_info(p) for p in assets if p.is_file()],'log':runner.file_info(out/'restore.log'),'tail':text.splitlines()[-8:],'finished_utc':runner.utc()}
runner.write_json(out/'result.json',result);print(json.dumps(result),flush=True)
assert result['status']=='PASS','Offline restore metadata failed; preserved all evidence.'
command=[sys.executable,str(F/'run-build31.py'),'--getall',str(F/'getall-sdk169-snapshot'),'--expected-index-sha256','2e3ee9a442015c492c84cc28f92f7da75dfffdbbe817d42dc0f3b311cbfac9eb','--run-id','31b','--execute']
print(json.dumps({'starting':'BUILD31b','command':command}),flush=True)
raise SystemExit(subprocess.call(command,cwd=R,env=env))
