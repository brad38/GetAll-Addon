"""Read-only provenance replay for the three pinned native support overlays.
Reads existing archives and support files, applies upstream patches in memory, prints JSON.
No builds, downloads, source writes, or deletions. Run with Python 3.12+ on Bradsson.
"""
import pathlib,json,zipfile,hashlib,difflib,re,sys
B=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else r'C:\Users\bradg\Downloads\GetAll-R18');R=B/'desktop-continuation-20261127'
F=B/'evidence-r18/flow-completion-20261127/rex-native-source';H=B/'evidence-r18/fh1-native-20261127'
sha=lambda b:hashlib.sha256(b).hexdigest()
norm=lambda b:b.decode('utf-8','replace').replace('\r\n','\n')
out={}
for n,ap,gap in [('ForzaNative',B/'console-cache/FH1-ReImagined-ReIGlue-18fa1cc468d4.zip',None),('PinyonNative',F/'shiftglue-0c2187c.zip',B/'pinyon-engine/games/Pinyon - pinyon-shift v0.9.5/pinyon-shift-source.zip'),('SsxNative',F/'rexglue-bd833a2.zip',B/'console-cache/ssx-717a7a9.zip')]:
 z=zipfile.ZipFile(R/'Tools'/n/'source-support.zip');m=json.loads(z.read('manifest.json'));o=json.loads((R/'Tools'/n/'ORIGIN.json').read_text())
 oz=zipfile.ZipFile(ap);gz=zipfile.ZipFile(gap) if gap else None
 gp=('' if 'cmake/PinyonShiftRexGlue.cmake' in gz.namelist() else gz.namelist()[0].split('/')[0]+'/') if gz else None
 originals={};sources={};allrows=[]
 for group,prefix in [('files','sdk/'),('game_files','game/')]:
  for f in m.get(group,[]):
   rel=f['path'];after=z.read(prefix+rel);before=None;source=None
   if group=='files':
    member=m['source']['prefix']+rel
    if member in oz.namelist():before=oz.read(member);source=str(ap)+'!'+member
    else:
     for dep in m.get('dependencies',[]):
      if rel.startswith(dep['path']+'/'):
       da=F/'dependencies'/dep['file']
       if not da.exists():da=B/'console-cache'/dep['file']
       if not da.exists():continue
       dz=zipfile.ZipFile(da);dm=dep['prefix']+rel[len(dep['path'])+1:]
       if dm in dz.namelist():before=dz.read(dm);source=str(da)+'!'+dm
   elif gz:
    member=gp+rel
    if member in gz.namelist():before=gz.read(member);source=str(gap)+'!'+member
   new_absent = before is None
   if f.get('before') is None:before=b'';source='new file'
   if group=='files' and before is not None:originals[rel]=norm(before)
   aftertext=norm(after) if pathlib.Path(rel).suffix not in ['.dll','.lib'] else None
   allrows.append({'group':group,'path':rel,'before_sha256':sha(before) if before else None,'declared_before':f.get('before'),'before_matches':f.get('before') is None or (before is not None and sha(before)==f['before']),'new_absent':new_absent if f.get('before') is None else None,'after_sha256':sha(after),'after_matches':sha(after)==f['after'],'source':source,'diff':''.join(difflib.unified_diff(norm(before or b'').splitlines(True),aftertext.splitlines(True),fromfile='original/'+rel,tofile='allfix/'+rel)) if aftertext else '(binary)'})
   if group=='files' and aftertext is not None:sources[rel]=aftertext
 patches=[];patched=dict(originals)
 if n=='ForzaNative':
  for p in o['upstream_patches']:
   member=m['source']['prefix']+p['patch'];b=oz.read(member);patches.append({'name':p['patch'],'sha256':sha(b),'matches':sha(b)==p['sha256'],'source':str(ap)+'!'+member,'text':norm(b)})
 elif n=='SsxNative':
  for p in o['upstream_patches']:
   matches=[v for v in gz.namelist() if v.endswith('/'+p['name'])]
   b=gz.read(matches[0]);patches.append({'name':p['name'],'sha256':sha(b),'matches':sha(b)==p['sha256'],'source':str(gap)+'!'+matches[0],'text':norm(b)})
 errors=[]
 for p in patches:
  lines=p['text'].splitlines(True);i=0;dest=None;offset=0
  while i<len(lines):
   line=lines[i]
   if line.startswith('+++ '):
    dest=line[4:].strip().split('\t')[0]
    if dest.startswith('b/'):dest=dest[2:]
    if n=='ForzaNative' and not dest.startswith('thirdparty/'):
     dep='sdl3' if '/sdl3/' in p['name'] else 'FFmpeg'
     dest='thirdparty/'+dep+'/'+dest
    offset=0;i+=1;continue
   match=re.match(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@',line)
   if not match:i+=1;continue
   old=[];new=[];i+=1
   while i<len(lines) and lines[i][:1] in [' ','+','-','\\'] and not lines[i].startswith('--- '):
    l=lines[i]
    if l[:1] in [' ','-']:old.append(l[1:])
    if l[:1] in [' ','+']:new.append(l[1:])
    if l.startswith('\\ No newline'):
     if old:old[-1]=old[-1].rstrip('\n')
     if new:new[-1]=new[-1].rstrip('\n')
    i+=1
   data=patched.get(dest,'').splitlines(True);start=int(match[1])-1+offset
   if int(match[1])==0:start=0
   if data[start:start+len(old)]!=old:
    found=[k for k in range(len(data)+1) if data[k:k+len(old)]==old]
    if len(found)!=1:
     errors.append({'patch':p['name'],'path':dest,'line':int(match[1]),'matches':len(found)});continue
    start=found[0]
   data[start:start+len(old)]=new;patched[dest]=''.join(data);offset+=len(new)-len(old)
 residual=[]
 for rel,after in sources.items():
  b=patched.get(rel,'')
  residual.append({'path':rel,'equals_after_upstream_patches':b==after,'diff':''.join(difflib.unified_diff(b.splitlines(True),after.splitlines(True),fromfile='upstream_patched/'+rel,tofile='allfix/'+rel))})
 result={'manifest':m,'origin':o,'original_archive':{'path':str(ap),'sha256':sha(ap.read_bytes()),'matches':sha(ap.read_bytes())==m['source']['sha256']},'game_archive':{'path':str(gap),'sha256':sha(gap.read_bytes())} if gap else None,'diffs':allrows,'upstream_patches':patches,'patch_errors':errors,'residual_diffs':residual}
 out[n]=result
print(json.dumps(out,ensure_ascii=False,indent=2))

