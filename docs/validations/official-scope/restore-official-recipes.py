"""Register reviewed official profiles without re-enabling retired contracts."""
import hashlib,json,pathlib,re
ROOT=pathlib.Path(__file__).resolve().parents[3]
def save(p,data):
 p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
index=json.loads((ROOT/"index.json").read_text(encoding="utf-8"))
policy=json.loads((ROOT/"docs/official-install-policy.json").read_text(encoding="utf-8"))
schema=json.loads((ROOT/"schemas/installation-recipe-v9.schema.json").read_text(encoding="utf-8"))
validator=(ROOT/"scripts/validate_recipes.py").read_text(encoding="utf-8")
specs=json.loads('''[{"project_id":"pinyon-shift","tag":"v0.9.5","build_profile":"pinyon-v0.9.5-official-installer","manual_steps":"Selecione sua ISO ou pasta original de Forza Horizon USA (MS-2505). O All-Fix executa a preparação oficial do Pinyon Shift, com verificação dos arquivos, download das ferramentas e compilação sem alterações de fonte. O uso das bibliotecas Microsoft exige aceite explícito dos termos. Ao concluir, use Jogar; configurações, shaders e DLCs seguem os procedimentos oficiais. Nenhum jogo está incluído.","preparation_media":[{"id":"original-disc","kind":"file_or_directory","extensions":[".iso"],"version":"Xbox 360 USA MS-2505 / 4D5309C9"}],"upstream_commit":"850518ce00c66d65557bcbf190a62d2e2a6bb0e3"},{"project_id":"fh1-reimagined","tag":"v0.3.9","build_profile":"fh1-0.3.9-official-prepare","manual_steps":"Selecione sua mídia original de Forza Horizon para Xbox 360. O launcher oficial importa a mídia e compila o jogo com fontes e SDK oficiais. O download das ferramentas Microsoft exige aceite explícito dos termos. A atualização TU4 é opcional.","preparation_media":[{"id":"original-disc","kind":"file_or_directory","extensions":[".iso",".god"],"version":"Xbox 360 original; Games on Demand ou pasta extraída"}],"upstream_commit":"46d5ed62866af68700d15c61748df8c29ad0248d"},{"project_id":"god-of-war-native-pc-port-gow-pc-port","tag":"launcher-v0.4.0","build_profile":"gow-0.4.0-official-installer","manual_steps":"Selecione sua ISO ou CHD original de God of War USA (SCUS-97399). O All-Fix verifica a mídia e executa o instalador oficial 0.4.0, com o compilador e as opções padrão do projeto. A primeira compilação pode demorar; ao concluir, use Jogar. Nenhum jogo está incluído.","preparation_media":[{"id":"original-disc","kind":"file","extensions":[".iso",".chd"],"version":"Disco original God of War USA (SCUS-97399), em ISO ou CHD."}],"upstream_commit":"adebc00e69d4395318c94523f345b26c7daf3451"},{"project_id":"ship-of-harkinian-soh","tag":"9.3.1","build_profile":"ship-of-harkinian-9.3.1-official-extractor","manual_steps":"Selecione sua ROM original compatível de Ocarina of Time em formato .z64. O extrator Torch oficial gera os recursos locais sem alterar as fontes do projeto. Ao concluir, use Jogar. Nenhuma ROM está incluída.","preparation_media":[{"id":"original-rom","kind":"file","extensions":[".z64"],"version":"Ocarina of Time .z64 big-endian de 32 MiB e SHA-1 oficial"}],"required_files":["soh.exe","soh.o2r"],"upstream_commit":"f0599f96f8d442f26d0fa1c5cedafddacd56633f"}]''')
replacements=policy.setdefault("approved_recipe_replacements",[])
for spec in specs:
 entry=next(e for e in index["recipes"] if e["project_id"]==spec["project_id"] and e["tag"]==spec["tag"])
 path=ROOT/entry["path"];retired_path="docs/retired-recipes/"+entry["path"].removeprefix("recipes/")
 archived=ROOT/retired_path
 if not archived.exists():
  archived.parent.mkdir(parents=True,exist_ok=True);archived.write_bytes(path.read_bytes())
 retired=archived.read_bytes();old=json.loads(retired)
 recipe=json.loads(path.read_bytes())
 # Schema 9 is a closed SDK profile, not an arbitrary command or script.
 recipe={k:v for k,v in recipe.items() if k in ("schema_version","project_id","tag","source_url","operations","required_files","inputs","manual_steps","build_profile","preparation_media")}
 recipe["schema_version"]=9;recipe["operations"]=[];recipe["inputs"]=[]
 for key in ("build_profile","manual_steps","preparation_media"):recipe[key]=spec[key]
 if "required_files" in spec:recipe["required_files"]=spec["required_files"]
 # Stable object order is part of the reviewed raw-byte hash.
 recipe={k:recipe[k] for k in ("schema_version","project_id","tag","source_url","operations","required_files","inputs","manual_steps","build_profile","preparation_media")}
 save(path,recipe)
 entry["sha256"]=hashlib.sha256(path.read_bytes()).hexdigest();entry["schema_version"]=9;entry["status"]="experimental";entry["min_sdk_version"]="1.5.70"
 entry["has_inputs"]=False;entry["has_manual_steps"]=True
 for key in ("disabled_reason","disabled_at","audit_reference"):entry.pop(key,None)
 approval=dict(project_id=entry["project_id"],tag=entry["tag"],path=entry["path"],sha256=entry["sha256"],
  build_profile=spec["build_profile"],retired_path=retired_path,retired_sha256=hashlib.sha256(retired).hexdigest(),
  retired_build_profile=old.get("build_profile"),upstream_commit=spec["upstream_commit"],
  audit_reference="docs/OFFICIAL-CONTRACT-RESTORATION-20261128.md")
 replacements[:]=[r for r in replacements if (r["project_id"],r["tag"])!=(entry["project_id"],entry["tag"])]
 replacements.append(approval)
 schema["oneOf"][:]=[c for c in schema["oneOf"] if c.get("const",{}).get("build_profile")!=spec["build_profile"]]
 schema["oneOf"].append({"const":recipe})
 lines=validator.splitlines()
 lines=[line for line in lines if not (line.startswith("        profiles.append(json.loads(") and spec["build_profile"] in line)]
 validator="\n".join(lines)+"\n"
 marker="        identities = {";assert marker in validator
 validator=validator.replace(marker,"        profiles.append(json.loads('''"+json.dumps(recipe,ensure_ascii=False)+"'''))\n"+marker,1)
 identity=json.dumps(spec["build_profile"])+":"
 if identity not in validator:
  validator=validator.replace(marker,marker+"\n            "+identity+" ("+json.dumps(entry["game_id"])+", "+json.dumps(entry["repository"])+"),",1)
 assert "?" not in recipe["manual_steps"]
 print(json.dumps(approval,ensure_ascii=True))
policy["reactivation"]="Retired pairs and profiles remain blocked. A reviewed replacement under a real upstream tag is accepted only for its exact recipe SHA-256, profile and identity; the old recipe remains archived byte for byte. New upstream versions do not clear the block."
save(ROOT/"index.json",index);save(ROOT/"docs/official-install-policy.json",policy);save(ROOT/"schemas/installation-recipe-v9.schema.json",schema)
(ROOT/"scripts/validate_recipes.py").write_text(validator,encoding="utf-8",newline="\n")
