"""Assemble the verified SDK169 candidate and the immutable GetAll implementation."""
import json,subprocess,sys
from pathlib import Path
b=Path(r'C:\Users\bradg\Downloads\GetAll-R18')
f=b/'evidence-r18/flow-completion-20261127'
e=b/'evidence-r18/preview-sdk169-20261127'
e.mkdir()
with (e/'remote-pins.json').open('xb') as stream:
 stream.write((f/'sdk169-remote-pins.json').read_bytes())
command=[sys.executable,'-I','-B','-X','utf8',str(f/'sdk169-finalization/assemble-preview.py'),'assemble',
 '--task-root',str(b),'--evidence',str(e),
 '--desktop-commit','921295de12349e726f7ca21a5edd8a8ecee123d8',
 '--getall-commit','37fbc54ee2d137952d8f1ca2b06f3602410870c9',
 '--candidate-manifest-sha256','aa85bbe915f2a8d975a8fa0139dea79d145d8c0a0107464941505a7f528a01e3',
 '--executable-sha256','b558afccf6fa50ec9a3899b66055009f04f8ce71cfc4dbcc6ab3886bd0433fcd']
with (e/'assemble.log').open('x',encoding='utf-8',newline='\n') as log:
 r=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT)
print((e/'assemble.log').read_text(encoding='utf-8')[-7000:],flush=True)
sys.exit(r.returncode)
