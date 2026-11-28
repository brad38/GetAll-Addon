import pathlib,json,hashlib,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[3];e=ROOT/"docs/validations/official-scope"
def save(path,v):path.write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
sources=json.loads((e/"vandal-official-source-review.json").read_text())
archive=e/"research-cache/vandal-source/source.zip";tree=e/"research-cache/vandal-source/source"
unchanged=True;count=0
with zipfile.ZipFile(archive) as z:
 for v in z.infolist():
  rel="/".join(v.filename.split("/")[1:])
  if not rel or rel.endswith("/"):continue
  count+=1;unchanged=unchanged and (tree/rel).read_bytes()==z.read(v)
report={"reviewed_at":"2026-11-28","scope":"Official-procedure gaps, never a determination of illegality or lack of upstream gameplay","projects":[
 {"project_id":"strikersrecomp","decision":"blocked","source_commit":"cd88f71f5a836c103484c038454b4143000d883c","reason":"O bootstrap oficial fixa GXRuntime v0.1.0, mas essa versão exporta DolRuntime enquanto o Strikers exige GXRuntime. A embalagem RecompCore oficial não contempla .dll no Windows e o GXRuntime lista suporte Windows no roadmap. A integração anterior recorria a alterações próprias; não há contrato Windows íntegro validado nesta revisão.","official_alternative":"Procedimento upstream: bootstrap.sh, tools/generate.py com ISO própria; módulo RecompCore ou build standalone nos hosts oficialmente documentados. Não foi afirmado que o projeto seja impossível de compilar no Windows.","restore_when":"Validar uma combinação oficial compatível de dependências e embalagem Windows, ou integrar um ambiente oficialmente suportado sem modificar código/runtime do jogo.","receipts":["strikers-official-procedure-review.json","strikers-gxruntime-v0.1.0-sources.json"]},
 {"project_id":"vandalhearts-pcport","decision":"blocked","source_commit":"14552fffa0e0b47e02b57592e274fc6e7a649923","release_tag_commit":"7450a2462c0d437740da2ec438a7d8d55c27fadf","reason":"O NOTICE declara dados do jogo/BIOS incorporados nos binários. A alternativa fonte foi verificada e usa executável PS-X e BIOS próprios; o teste nativo CMake intacto falhou na criação obrigatória de symlinks por falta de privilégio. O procedimento Windows documentado usa cross-compilação Linux/macOS e dependências próprias, ainda sem integração validada no Desktop.","official_alternative":"CMake VH_PSX_EXE + VH_KROM_SOURCE, mantendo VH_WEBP/VH_HDVIDEO ligados. A fonte atual pode ler diretamente PS-X EXE sem ELF/PsyQ; o gerador aceita BIOS próprio e valida o hash da região de fonte. A embalagem unificada oficial compila os dois cores regionais US/JP e usa libav estático.","restore_when":"Integrar e verificar ambiente oficial de compilação que suporte o staging de symlinks, gerando todos os dados necessários exclusivamente das mídias/BIOS fornecidos pelo usuário. Não substituir por binário que já incorpora esses dados.","native_configuration_exit":1,"source_files_checked":count,"source_files_unchanged":unchanged,"receipts":["payload-provenance-review.json","vandal-official-source-review.json","vandal-native-configure-result.json","vandal-native-configure.log"]},
 {"project_id":"redriver2","decision":"blocked","source_commit":"acca6b139302dd72c1fbff52556f3493aafda2dd","reason":"A compilação oficial copia os mesmos 76 arquivos rastreados data/DRIVER2 ao pacote. Os conversores oficiais geram apenas vídeo e áudio da mídia própria; não fornecem reconstrução dos extras LANG/GFX/GAL/REPLAYS questionados na issue234. Compilar somente o executável não resolve a lacuna de procedência desses dados.","official_alternative":"Método Windows oficial com ambos CDs próprios, launcher Java ou _convert_cd_fmv_xa.bat. A via de fonte VS2019/premake permanece documentada, porém sua embalagem usa o mesmo diretório de dados; não foi verificada uma rota que derive todos os extras dos discos.","restore_when":"Documentar a procedência dos extras ou validar uma reconstrução oficial desses dados a partir das mídias próprias, preservando as funcionalidades do upstream.","receipts":["payload-provenance-review.json","redriver2-official-data-tree-review.json","redriver2-packaging-conversion-sources.json","redriver2-wiki-procedure-sources.json"]}
]}
for p in report["projects"]:
 p["receipt_hashes"]={name:hashlib.sha256((e/name).read_bytes()).hexdigest() for name in p["receipts"]}
save(e/"remaining-official-blockers.json",report)
index=json.loads((ROOT/"index.json").read_text());policy=json.loads((ROOT/"docs/official-install-policy.json").read_text())
for project in report["projects"]:
 for entry in index["recipes"]:
  if entry["project_id"]==project["project_id"] and entry["status"]=="disabled":
   entry.update(disabled_reason=project["reason"],audit_reference="docs/validations/official-scope/remaining-official-blockers.json")
 for block in policy["blocked_recipes"]:
  if block["project_id"]==project["project_id"]:
   block.update(reason=project["reason"],audit_reference="docs/validations/official-scope/remaining-official-blockers.json")
save(ROOT/"index.json",index);save(ROOT/"docs/official-install-policy.json",policy)
print(json.dumps({"source_files_checked":count,"vandal_source_unchanged":unchanged,"projects":[p["project_id"] for p in report["projects"]]}))
