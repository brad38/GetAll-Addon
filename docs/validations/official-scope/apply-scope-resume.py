"""Apply the reviewed recipe changes; retired variants remain preserved."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3]
def read(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def write(path,data):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
index=read("index.json")
policy=read("docs/official-install-policy.json")
recipe={
 "schema_version":9,"project_id":"ssx-recomp","tag":"v2.0.1",
 "source_url":"https://github.com/AmarilloNL/ssx-recomp/releases/tag/v2.0.1",
 "operations":[],"required_files":["ssx-recomp.exe","recomplauncher.json"],"inputs":[],
 "manual_steps":"Selecione sua ISO ou pasta original de SSX EA-2413. O instalador oficial compila o jogo sem alterações de fonte; a instalação pode baixar ferramentas e requer aceite explícito dos termos do Visual Studio Build Tools. Title Update e DLCs são opcionais.",
 "build_profile":"ssx-2.0.1-official-prepare",
 "preparation_media":[{"id":"original-disc","kind":"file_or_directory","extensions":[".iso"],"version":"Xbox 360 EA-2413 USA/Europe/Australia"}]
}
path="recipes/ssx-2012/ssx-recomp/v2.0.1.json"
write(path,recipe)
entry={"game_id":"ssx-2012","project_id":"ssx-recomp","repository":"AmarilloNL/ssx-recomp","tag":"v2.0.1","schema_version":9,"path":path,"sha256":sha(path),"status":"experimental","has_inputs":False,"has_manual_steps":True,"min_sdk_version":"1.5.70"}
if not any(e["project_id"]==entry["project_id"] and e["tag"]==entry["tag"] for e in index["recipes"]):index["recipes"].append(entry)
schema=read("schemas/installation-recipe-v9.schema.json")
if not any(x.get("const")==recipe for x in schema["oneOf"]):schema["oneOf"].append({"const":recipe})
write("schemas/installation-recipe-v9.schema.json",schema)
validator=ROOT/"scripts/validate_recipes.py"
text=validator.read_text(encoding="utf-8")
marker="        identities = {\n"
addition="        profiles.append(json.loads('''"+json.dumps(recipe,ensure_ascii=False)+"'''))\n"
if recipe["build_profile"] not in text:
    assert marker in text;text=text.replace(marker,addition+marker,1)
    identity='            "ssx-2.0.0-prepare": ("ssx-2012", "AmarilloNL/ssx-recomp"),'
    assert identity in text;text=text.replace(identity,identity+'\n            "ssx-2.0.1-official-prepare": ("ssx-2012", "AmarilloNL/ssx-recomp"),',1)
    validator.write_text(text,encoding="utf-8",newline="\n")
review={
"reviewed_at":"2026-11-27","scope":"Recipe payload provenance; not a legal determination or upstream gameplay reassessment",
"projects":[
 {"project_id":"vandalhearts-pcport","tag":"v2.1.0","decision":"suspend_binary_recipe",
 "source":"https://github.com/HalmyLyseas/VandalHearts-PcPort/blob/14552fffa0e0b47e02b57592e274fc6e7a649923/NOTICE",
 "observed":"The upstream NOTICE explicitly identifies static PS1 data, kanji glyphs derived from a PlayStation BIOS and tables embedded in binary releases; the source build regenerates the excluded inputs from the owner's executable/BIOS.",
 "reason":"O pacote binário declara dados de jogo/BIOS incorporados sem proveniência de redistribuição suficiente. A importação da BIN própria não regenera esses bytes. O projeto continua elegível por fonte e mídia/BIOS próprios; a receita binária fica suspensa.",
 "reinstate_when":"Implement and verify the official build generating all excluded inputs from the user's original game executable and compatible BIOS, or obtain an official redistributable payload with documented provenance."},
 {"project_id":"redriver2","tag":"7.4-rc2","decision":"suspend_binary_recipe_pending_payload_provenance",
 "source":"https://github.com/OpenDriver2/REDRIVER2/issues/234",
 "observed":"The upstream provenance issue identifies LANG/GFX/GAL/REPLAYS/ReChases/XA/DATA and credits supplied in data/DRIVER2 and asks how to reproduce them from the discs. No maintainer answer was present in the inspected issue; the current recipe consumes the release package before importing the user's discs.",
 "reason":"A origem de dados extras incluídos no pacote oficial continua sem confirmação suficiente no registro upstream; importar os dois discos não demonstra a procedência desses arquivos. A automação binária fica suspensa até comprovar a origem ou extraí-los pelo procedimento oficial.",
 "reinstate_when":"Document provenance of the release's extra data or verify an official install/build path that derives the needed data exclusively from the user's discs; do not replace missing data with AllFix gameplay changes."}
]}
write("docs/validations/official-scope/payload-provenance-review.json",review)
for item in review["projects"]:
    e=next(x for x in index["recipes"] if x["project_id"]==item["project_id"] and x["tag"]==item["tag"])
    e["status"]="disabled";e["disabled_reason"]=item["reason"]
    e["disabled_at"]="2026-11-27";e["audit_reference"]="docs/validations/official-scope/payload-provenance-review.json"
    if not any(x["project_id"]==e["project_id"] and x["tag"]==e["tag"] for x in policy["blocked_recipes"]):
        policy["blocked_recipes"].append({"project_id":e["project_id"],"tag":e["tag"],"path":e["path"],"reason":item["reason"],"audit_reference":e["audit_reference"]})
write("index.json",index);write("docs/official-install-policy.json",policy)
ignore=ROOT/".gitignore"
text=ignore.read_text(encoding="utf-8")
line="/docs/validations/official-scope/research-cache/"
if line not in text:ignore.write_text(text.rstrip()+"\n"+line+"\n",encoding="utf-8",newline="\n")
print(json.dumps({"ssx_new_recipe":entry,"suspended":[x["project_id"] for x in review["projects"]]},ensure_ascii=False,indent=2))
