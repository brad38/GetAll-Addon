import sys,pathlib,subprocess,json,hashlib,zipfile,io,base64
r=pathlib.Path(r'C:\Users\bradg\Downloads\GetAll-R18\desktop-continuation-20261127')
out=pathlib.Path(r'C:\Users\bradg\Downloads\GetAll-R18\evidence-r18\source-integrity-audit-20261127')
git=r'C:\Program Files\Git\cmd\git.exe'
if len(sys.argv)>1:
    b=(out/'desktop-source.zip').read_bytes(); n=int(sys.argv[1]); part=b[n*90000:(n+1)*90000]
    print('AUDIT_CHUNK '+json.dumps(dict(index=n,sha256=hashlib.sha256(part).hexdigest(),data=base64.b64encode(part).decode())))
    raise SystemExit
out.mkdir(exist_ok=True)
head=subprocess.check_output([git,'-C',str(r),'rev-parse','HEAD']).decode().strip()
tree=subprocess.check_output([git,'-C',str(r),'ls-tree','-rlz',head])
rows=[]
for row in tree.split(bytes([0])):
    if not row:continue
    meta,p=row.split(b'\t',1); mode,typ,oid,size=meta.decode().split(); p=p.decode()
    rows.append(dict(path=p,mode=mode,type=typ,git_blob=oid,size=int(size)))
exclude={'.exe','.dll','.jpg','.jpeg','.png','.ico','.zip'}
selected=[x for x in rows if pathlib.Path(x['path']).suffix.lower() not in exclude or x['path'] in ['Tools/ForzaNative/source-support.zip','Tools/PinyonNative/source-support.zip','Tools/SsxNative/source-support.zip','Tools/MkwSm86/mkw-sm86-cli-support-v1.zip','Tools/UnleashedHelper/Unleashed-Xex-Helper-Sources.zip']]
raw=subprocess.check_output([git,'-C',str(r),'cat-file','--batch'],input=('\n'.join(x['git_blob'] for x in selected)+'\n').encode())
stream=io.BytesIO(raw); payload=io.BytesIO()
with zipfile.ZipFile(payload,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for row in selected:
        hdr=stream.readline().decode().split(); b=stream.read(int(hdr[2])); assert stream.read(1)==b'\n'
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()==row['git_blob']
        row['sha256']=hashlib.sha256(b).hexdigest(); z.writestr(row['path'],b)
    z.writestr('AUDIT-SNAPSHOT.json',json.dumps(dict(commit=head,repository='brad38/Allfix',entries=rows,included=[x['path'] for x in selected]),indent=2)+'\n')
b=payload.getvalue(); (out/'desktop-source.zip').write_bytes(b)
print(json.dumps(dict(commit=head,tracked_files=len(rows),included=len(selected),zip_bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),parts=(len(b)+89999)//90000)))

