import pathlib,urllib.request,hashlib,json,concurrent.futures
root=pathlib.Path(__file__).resolve().parent;cache=root/"research-cache/mario-official-kits";cache.mkdir(parents=True,exist_ok=True)
items=[
 ("sm64ex","sm64pc/sm64ex","d7ca2c04364a6dd0dac58b47151e04e26887e6f0",11541633,"9c9fad7d6d027971ee6c3447bf36c95aae7e1dc4a2715dabb8106c771b696bee"),
 ("render96ex","Render96/Render96ex","48da5c491c8abfb2f5192b59278c1c269411e533",11615689,"43091630151c8023b72e7faa2726c3914376fee2cc3becbfefba30423b71b403"),
 ("sm64rt","DarioSamo/sm64rt","20e618b75ae4a6810bd92ac6a937cb167517aac5",76969492,"a742cdb0879c073c697099ef60ed8014b00e2d7104797f2cbbde28bc59917acb")]
def fetch(x):
 name,repo,commit,size,digest=x;out=cache/(name+".zip");url=f"https://codeload.github.com/{repo}/zip/{commit}"
 if not out.exists():out.write_bytes(urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"AllFix-Official-Scope-Audit"}),timeout=120).read())
 assert out.stat().st_size==size and hashlib.sha256(out.read_bytes()).hexdigest()==digest
 row=dict(project=name,url=url,bytes=size,sha256=digest,local=str(out));print(json.dumps(row),flush=True);return row
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(fetch,items))
(root/"mario-official-kit-downloads.json").write_text(json.dumps(rows,indent=2)+"\n",encoding="utf-8",newline="\n")
