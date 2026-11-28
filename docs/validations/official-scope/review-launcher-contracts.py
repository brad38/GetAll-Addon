"""Read launcher installation contracts at immutable upstream commits."""
import hashlib,json,pathlib,re,urllib.request,concurrent.futures
ROOT=pathlib.Path(__file__).resolve().parent
TASKS=[
("pinyon","arcanite24/pinyon-shift","850518ce00c66d65557bcbf190a62d2e2a6bb0e3","tools/build-preview.ps1"),
("pinyon","arcanite24/pinyon-shift","850518ce00c66d65557bcbf190a62d2e2a6bb0e3","tools/install-build-tools.ps1"),
("pinyon","arcanite24/pinyon-shift","850518ce00c66d65557bcbf190a62d2e2a6bb0e3","launcher/PinyonShift.Launcher.Desktop/Installation.cs"),
("fh1","FH1-ReImagined/ForzaHorizon1-ReImagined","46d5ed62866af68700d15c61748df8c29ad0248d","launcher/forza_launcher/builder.py"),
("fh1","FH1-ReImagined/ForzaHorizon1-ReImagined","46d5ed62866af68700d15c61748df8c29ad0248d","launcher/forza_launcher/installer.py"),
("fh1","FH1-ReImagined/ForzaHorizon1-ReImagined","46d5ed62866af68700d15c61748df8c29ad0248d","launcher/forza_launcher/game.py"),
("fh1","FH1-ReImagined/ForzaHorizon1-ReImagined","46d5ed62866af68700d15c61748df8c29ad0248d","launcher/forza_launcher/config.py"),
]
def fetch(task):
    short,repo,sha,path=task
    url=f"https://raw.githubusercontent.com/{repo}/{sha}/{path}"
    with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"GetAll-Official-Scope-Review"}),timeout=60) as response:data=response.read()
    out=ROOT/"research-cache"/short/path
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_bytes(data)
    return {"project":short,"repository":repo,"commit":sha,"path":path,"url":url,"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),"local":str(out)}
def main():
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for task,future in zip(TASKS,[pool.submit(fetch,x) for x in TASKS]):
            try:results.append(future.result())
            except Exception as exc:results.append({"task":task,"error":repr(exc)})
    (ROOT/"official-launcher-contracts.json").write_text(json.dumps(results,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    print(json.dumps(results,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
