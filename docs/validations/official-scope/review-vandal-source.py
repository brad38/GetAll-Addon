import pathlib,urllib.request,json,hashlib,zipfile
root=pathlib.Path(__file__).resolve().parent;cache=root/"research-cache/vandal-source";cache.mkdir(parents=True,exist_ok=True)
repo="HalmyLyseas/VandalHearts-PcPort";commit="14552fffa0e0b47e02b57592e274fc6e7a649923"
url=f"https://codeload.github.com/{repo}/zip/{commit}"
data=urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"AllFix-Official-Scope-Audit"}),timeout=120).read()
(cache/"source.zip").write_bytes(data)
receipt={"repository":repo,"commit":commit,"url":url,"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),"sources":[]}
with zipfile.ZipFile(cache/"source.zip") as z:
 for info in z.infolist():
  rel="/".join(info.filename.split("/")[1:])
  if not rel or rel.endswith("/"):continue
  out=cache/"source"/rel;out.parent.mkdir(parents=True,exist_ok=True);buf=z.read(info);out.write_bytes(buf)
  if rel.lower().endswith((".md",".ps1",".sh",".yml",".yaml")) or rel.endswith("CMakeLists.txt") or rel=="NOTICE":
   receipt["sources"].append({"path":rel,"url":f"https://github.com/{repo}/blob/{commit}/{rel}","bytes":len(buf),"sha256":hashlib.sha256(buf).hexdigest()})
   if rel.lower().startswith("readme") or rel=="CMakeLists.txt" or ("workflow" in rel and "build" in rel):print(rel,buf.decode("utf-8",errors="replace")[:20000])
(root/"vandal-official-source-review.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8",newline="\n")
print("archive",receipt["bytes"],receipt["sha256"])
