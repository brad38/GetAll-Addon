import pathlib,urllib.request,hashlib,json,concurrent.futures
root=pathlib.Path(__file__).resolve().parent;repo="FH1-ReImagined/ForzaHorizon1-ReImagined";commit="46d5ed62866af68700d15c61748df8c29ad0248d"
files=["launcher/forza_launcher/ui/pages.py","launcher/forza_launcher/build_env.py","launcher/forza_launcher/pins.py","launcher/forza_launcher/ui/window.py"]
def get(p):
 url=f"https://raw.githubusercontent.com/{repo}/{commit}/{p}"
 data=urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"AllFix-Official-Scope-Audit"}),timeout=60).read()
 out=root/"research-cache/fh1"/p;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data)
 rows=[]
 lines=data.decode().splitlines()
 for i,line in enumerate(lines):
  if any(x in line.lower() for x in ["license-terms","aka.ms","xwin","msvc","license","visualstudio.com"]):
   rows.append({"line":i+1,"excerpt":"\n".join(lines[max(0,i-2):min(len(lines),i+3)])})
 return {"path":p,"url":url,"sha256":hashlib.sha256(data).hexdigest(),"bytes":len(data),"matches":rows}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(get,files))
(root/"fh1-microsoft-license-sources.json").write_text(json.dumps(rows,indent=2)+"\n",encoding="utf-8",newline="\n")
for r in rows:
 for x in r["matches"]:
  if any(w in x["excerpt"].lower() for w in ["https:","licen","accept"]):print(r["path"],x["line"],x["excerpt"])
