import pathlib,urllib.request,json,hashlib,zipfile
root=pathlib.Path(__file__).resolve().parent;cache=root/"research-cache/strikers-official";cache.mkdir(parents=True,exist_ok=True)
repo="aharonahdoot/StrikersRecomp";commit="cd88f71f5a836c103484c038454b4143000d883c"
def get(url):return urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"AllFix-Official-Scope-Audit","Accept":"application/vnd.github+json"}),timeout=90).read()
url=f"https://codeload.github.com/{repo}/zip/{commit}";data=get(url)
assert len(data)==181877 and hashlib.sha256(data).hexdigest()=="1f361113dbfd35d0b0e6e1c5b98cbdf755cc28334f984cbdd95572a3be189a62"
archive=cache/"source.zip";archive.write_bytes(data)
receipt={"repository":repo,"commit":commit,"archive_url":url,"archive_sha256":hashlib.sha256(data).hexdigest(),"sources":[],"scope":"official procedure review; no original media or gameplay"}
with zipfile.ZipFile(archive) as z:
 for info in z.infolist():
  rel="/".join(info.filename.split("/")[1:])
  if not rel or rel.endswith("/"):continue
  f=cache/"source"/rel;f.parent.mkdir(parents=True,exist_ok=True);buf=z.read(info);f.write_bytes(buf)
  if rel.lower().endswith((".md",".ps1",".sh",".yml",".yaml",".toml",".txt")) or rel in [".gitmodules","CMakeLists.txt"]:
   row={"path":rel,"url":f"https://github.com/{repo}/blob/{commit}/{rel}","sha256":hashlib.sha256(buf).hexdigest(),"bytes":len(buf)};receipt["sources"].append(row)
   if rel.lower().startswith("readme") or rel=="CMakeLists.txt" or rel==".gitmodules" or rel.startswith(".github/workflows"):
    print(rel);print(buf.decode("utf-8",errors="replace")[:13000])
for endpoint in ["", "/commits/main", "/releases?per_page=5"]:
 try:
  obj=json.loads(get("https://api.github.com/repos/"+repo+endpoint));target=cache/("api"+endpoint.replace("/","_").replace("?","_")+".json");target.write_text(json.dumps(obj,indent=2)+"\n",encoding="utf-8")
  receipt.setdefault("api",[]).append({"url":"https://api.github.com/repos/"+repo+endpoint,"sha256":hashlib.sha256(target.read_bytes()).hexdigest()})
  if endpoint=="":print("default_branch",obj.get("default_branch"))
  elif endpoint.startswith("/commits"):print("head",obj["sha"],obj["commit"]["message"][:100])
  else:print("releases",[(r["tag_name"],[(a["name"],a["size"]) for a in r["assets"]]) for r in obj])
 except Exception as e:print("API",endpoint,str(e))
(root/"strikers-official-procedure-sources.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8",newline="\n")
