import pathlib,urllib.request,hashlib,json
r=pathlib.Path(__file__).resolve().parent;out=r/"research-cache/soh-release/SoH-Dewey-Bravo-Win64.zip";out.parent.mkdir(parents=True,exist_ok=True)
url="https://github.com/HarbourMasters/Shipwright/releases/download/9.3.1/SoH-Dewey-Bravo-Win64.zip"
if not out.exists():out.write_bytes(urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"AllFix-Official-Scope-Audit"}),timeout=180).read())
assert out.stat().st_size==72980600 and hashlib.sha256(out.read_bytes()).hexdigest()=="429292a0bfbdfcda283b33c1538ecdc49163b9ed53e8702cac80b2489d9fe26c"
v=dict(url=url,bytes=out.stat().st_size,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),local=str(out))
(r/"soh-official-kit-download.json").write_text(json.dumps(v,indent=2)+"\n",encoding="utf-8",newline="\n");print(json.dumps(v))
