"""Inspect fixed official launcher inputs; no game media, builds or installation."""
from __future__ import annotations
import hashlib, io, json, pathlib, subprocess, urllib.request, zipfile
ROOT=pathlib.Path(__file__).resolve().parent
CACHE=ROOT/"research-cache"
def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"GetAll-Official-Scope-Review"}),timeout=60) as response:
        return response.read()
def source(short,repo,sha,path):
    url=f"https://raw.githubusercontent.com/{repo}/{sha}/{path}"
    data=fetch(url)
    dest=CACHE/short/path
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(data)
    return {"path":path,"url":url,"sha256":hashlib.sha256(data).hexdigest(),"bytes":len(data),"local":str(dest)}
def main():
    url="https://github.com/AmarilloNL/ssx-recomp/releases/download/v2.0.1/ssx-recomp-v2.0.1-Windows-x64.zip"
    data=fetch(url)
    digest=hashlib.sha256(data).hexdigest()
    assert digest=="66f0188ca2ba84166574833dc01bd9dbad5d356f28babbed7dc8efe15ad185a4",(digest,len(data))
    dest=CACHE/"ssx"/"release"
    dest.mkdir(parents=True,exist_ok=True)
    (dest/"ssx-recomp-v2.0.1-Windows-x64.zip").write_bytes(data)
    members=[]
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        for entry in archive.infolist():
            if entry.is_dir(): continue
            path=pathlib.PurePosixPath(entry.filename.replace("\\","/"))
            assert not path.is_absolute() and ".." not in path.parts
            value=archive.read(entry)
            out=dest.joinpath(*path.parts)
            out.parent.mkdir(parents=True,exist_ok=True)
            out.write_bytes(value)
            members.append({"path":entry.filename,"bytes":len(value),"sha256":hashlib.sha256(value).hexdigest()})
    exe=dest/"ssx-recomp.exe"
    tests=[]
    for args,expect in [(["--prepare"],2),(["--prepare","--game",str(dest/"nonexistent.iso")],10)]:
        run=subprocess.run([str(exe),*args],cwd=dest,capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=20)
        assert run.returncode==expect,(run.returncode,run.stdout,run.stderr)
        tests.append({"arguments":args,"exit_code":run.returncode,"expected":expect,"stdout":run.stdout,"stderr":run.stderr,"scope":"official CLI negative fixture; not original-media installation, first boot or gameplay"})
    more=[
      source("fh1","FH1-ReImagined/ForzaHorizon1-ReImagined","46d5ed62866af68700d15c61748df8c29ad0248d","launcher/forza_launcher/cli.py"),
      source("pinyon","arcanite24/pinyon-shift","850518ce00c66d65557bcbf190a62d2e2a6bb0e3","launcher/PinyonShift.Launcher/App.xaml.cs"),
      source("pinyon","arcanite24/pinyon-shift","850518ce00c66d65557bcbf190a62d2e2a6bb0e3","launcher/PinyonShift.Launcher.Desktop/Program.cs"),
      source("gow","danielalves96/gow-pc-port","adebc00e69d4395318c94523f345b26c7daf3451","gow-launcher/crates/gow-core/src/installer.rs"),
      source("gow","danielalves96/gow-pc-port","adebc00e69d4395318c94523f345b26c7daf3451","gow-launcher/crates/gow-cli/src/main.rs"),
      source("ssx","AmarilloNL/ssx-recomp","bdef7c73d774b200ee97d4722c0c2c62ee58edf8","scripts/package.ps1"),
    ]
    report={"ssx":{"url":url,"bytes":len(data),"sha256":digest,"members":members,"negative_tests":tests,"local_directory":str(dest)},"additional_sources":more}
    (ROOT/"official-launcher-inputs.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
