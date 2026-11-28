"""Additional pinned source receipts for portable official launchers."""
import importlib.util,json,pathlib,concurrent.futures,hashlib,zipfile,subprocess
ROOT=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("contracts",ROOT/"review-launcher-contracts.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
TASKS=[
("fh1","FH1-ReImagined/ForzaHorizon1-ReImagined","46d5ed62866af68700d15c61748df8c29ad0248d","launcher/forza_launcher/datafolder.py"),
("pinyon","arcanite24/pinyon-shift","850518ce00c66d65557bcbf190a62d2e2a6bb0e3","tools/setup-preview.ps1"),
("pinyon","arcanite24/pinyon-shift","850518ce00c66d65557bcbf190a62d2e2a6bb0e3","tools/launch-preview.ps1"),
("pinyon","arcanite24/pinyon-shift","850518ce00c66d65557bcbf190a62d2e2a6bb0e3","tools/release-common.ps1"),
("pinyon","arcanite24/pinyon-shift","850518ce00c66d65557bcbf190a62d2e2a6bb0e3","release-toolchain.json"),
("pinyon","arcanite24/pinyon-shift","850518ce00c66d65557bcbf190a62d2e2a6bb0e3","launcher/PinyonShift.Launcher/MainWindow.xaml.cs"),
]
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for task,future in zip(TASKS,[pool.submit(m.fetch,t) for t in TASKS]):
  try: results.append(future.result())
  except Exception as e:results.append({"task":task,"error":str(e)})
(ROOT/"official-portable-launchers.json").write_text(json.dumps(results,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
print(json.dumps(results,indent=2))
