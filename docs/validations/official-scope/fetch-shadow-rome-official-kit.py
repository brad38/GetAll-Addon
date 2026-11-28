"""Fetch only the pinned official Shadow of Rome release for a kit test."""
from pathlib import Path
import hashlib, json, urllib.request
ROOT=Path(__file__).resolve().parents[3]
target=ROOT/"docs/validations/official-scope/research-cache/shadow-rome-release/ShadowOfRome-2.9.5-windows.zip"
url="https://github.com/Korvonordico/shadow-of-rome-recompiled/releases/download/v2.9.5/ShadowOfRome-2.9.5-windows.zip"
expected="a416fcf346bba3be23a4b9753d9f1ab32925a65d5baa3f8b70d6752527aac508"
target.parent.mkdir(parents=True,exist_ok=True)
if not target.exists():
    partial=target.with_suffix(".download")
    with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"GetAll-official-scope-review"}),timeout=60) as response,partial.open("wb") as output:
        while chunk:=response.read(1024*1024): output.write(chunk)
    assert partial.stat().st_size==58027163
    assert hashlib.file_digest(partial.open("rb"),"sha256").hexdigest()==expected
    partial.rename(target)
assert target.stat().st_size==58027163
with target.open("rb") as source: actual=hashlib.file_digest(source,"sha256").hexdigest()
assert actual==expected
record=dict(url=url,bytes=target.stat().st_size,sha256=actual,local=str(target))
(ROOT/"docs/validations/official-scope/shadow-rome-official-kit-download.json").write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8",newline="\n")
print(json.dumps(record))
