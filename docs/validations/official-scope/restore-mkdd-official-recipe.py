"""Register the reviewed upstream MKDD contract and archive retired bytes."""
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
def load(path): return json.loads((ROOT/path).read_text(encoding="utf-8"))
def save(path, value): (ROOT/path).write_text(json.dumps(value, ensure_ascii=False, indent=2)+"\n", encoding="utf-8", newline="\n")
index = load("index.json")
policy = load("docs/official-install-policy.json")
schema = load("schemas/installation-recipe-v9.schema.json")
entry = next(e for e in index["recipes"] if e["project_id"] == "mariokartdd-recomp" and e["tag"] == "build-bd36eb9")
path = ROOT/entry["path"]
archive_path = "docs/retired-recipes/"+entry["path"].removeprefix("recipes/")
archive = ROOT/archive_path
if not archive.exists():
    archive.parent.mkdir(parents=True, exist_ok=True)
    archive.write_bytes(path.read_bytes())
old = json.loads(archive.read_bytes())
profile = "mariokartdd-bd36eb9-official-msvc-clang"
recipe = dict(
    schema_version=9, project_id=entry["project_id"], tag=entry["tag"],
    source_url=old["source_url"], operations=[],
    required_files=["CMakeLists.txt","build.ps1","LICENSE","README.md","gcn-recomp/CMakeLists.txt","gcn-recomp/LICENSE","gcn-recomp/recomp/extract_dol.py","gcn-recomp/recomp/recomp.py"],
    inputs=[],
    manual_steps="Selecione sua ISO original americana de Mario Kart: Double Dash!! (GM4E01). O All-Fix executa build.ps1 oficial com Clang, Visual Studio 2022 e o submódulo fixado pelo autor, preservando OpenXR e as opções do projeto. Ferramentas Microsoft ausentes exigem aceite explícito antes da instalação. Primeiro boot ainda não homologado.",
    build_profile=profile,
    preparation_media=[dict(id="original-disc",kind="file",extensions=[".iso"],version="GameCube USA GM4E01; main.dol SHA-1 e389e50357d4a5076ab3d38672204658f411123d")])
save(entry["path"], recipe)
digest = hashlib.sha256(path.read_bytes()).hexdigest()
entry.update(sha256=digest,schema_version=9,status="experimental",min_sdk_version="1.5.70",has_inputs=False,has_manual_steps=True)
for key in ("disabled_reason","disabled_at","audit_reference"): entry.pop(key,None)
approved=dict(project_id=entry["project_id"],tag=entry["tag"],path=entry["path"],sha256=digest,build_profile=profile,
    retired_path=archive_path,retired_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),retired_build_profile=old.get("build_profile"),
    upstream_commit="bd36eb982ea58c6651584cc48264876d1aba9546",audit_reference="docs/OFFICIAL-CONTRACT-RESTORATION-20261128.md")
policy["approved_recipe_replacements"] = [v for v in policy["approved_recipe_replacements"] if (v["project_id"],v["tag"]) != (entry["project_id"],entry["tag"])] + [approved]
schema["oneOf"] = [v for v in schema["oneOf"] if v.get("const",{}).get("build_profile") != profile] + [{"const":recipe}]
validator_path=ROOT/"scripts/validate_recipes.py"
validator=validator_path.read_text(encoding="utf-8")
validator="\n".join(line for line in validator.splitlines() if not(line.startswith("        profiles.append(json.loads(") and profile in line))+"\n"
marker="        identities = {"
assert marker in validator
validator=validator.replace(marker,"        profiles.append(json.loads('''"+json.dumps(recipe,ensure_ascii=False)+"'''))\n"+marker,1)
if json.dumps(profile)+":" not in validator:
    validator=validator.replace(marker,marker+"\n            "+json.dumps(profile)+": ("+json.dumps(entry["game_id"])+", "+json.dumps(entry["repository"])+"),",1)
validator_path.write_text(validator,encoding="utf-8",newline="\n")
save("index.json",index)
save("docs/official-install-policy.json",policy)
save("schemas/installation-recipe-v9.schema.json",schema)
save("docs/validations/official-scope/mkdd-official-recipe-contract.json",approved)
print(json.dumps(approved))
print("INDEX_SHA256",hashlib.sha256((ROOT/"index.json").read_bytes()).hexdigest())
