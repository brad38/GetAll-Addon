"""Register official MSYS2/MSVC/GT5 contracts; preserve prior recipes verbatim."""
import json,pathlib,hashlib,re
ROOT=pathlib.Path(__file__).resolve().parents[3]
desktop=ROOT.parent/"desktop-scope-20261127"
def save(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
index=json.loads((ROOT/"index.json").read_text(encoding="utf-8"))
policy=json.loads((ROOT/"docs/official-install-policy.json").read_text(encoding="utf-8"))
schema=json.loads((ROOT/"schemas/installation-recipe-v9.schema.json").read_text(encoding="utf-8"))
validator=(ROOT/"scripts/validate_recipes.py").read_text(encoding="utf-8")
cs=(desktop/"Services/GameInstallationSm64PlusOfficial.cs").read_text(encoding="utf-8")
def const(name):return re.search(r'const string '+name+r' = "([^"]+)";',cs)[1]
media=[dict(id="original-rom",kind="file",extensions=[".z64"],version=const("MarioOfficialMediaVersion"))]
specs=[]
for project,tag,symbol,commit in [
 ("sm64ex","build-d7ca2c0","Sm64exOfficialProfile","d7ca2c04364a6dd0dac58b47151e04e26887e6f0"),
 ("render96ex","build-48da5c4","Render96OfficialProfile","48da5c491c8abfb2f5192b59278c1c269411e533"),
 ("sm64rt","build-20e618b","Sm64rtOfficialProfile","20e618b75ae4a6810bd92ac6a937cb167517aac5")]:
 manual=re.search(symbol+r' => "([^"]+)",',cs)[1]
 specs.append(dict(project_id=project,tag=tag,build_profile=const(symbol),required_files=["source.zip","README.md"],manual_steps=manual,preparation_media=media,upstream_commit=commit))
kit=json.loads((ROOT/"docs/validations/official-scope/sm64plus-bootstrap-inputs.json").read_text(encoding="utf-8"))
specs.append(dict(project_id="sm64plus",tag="LauncherMirror",build_profile=const("Sm64PlusOfficialProfile"),
 required_files=[f["path"] for f in kit["launcher_asset"]["files"]],manual_steps=const("Sm64PlusOfficialManual"),
 preparation_media=media,upstream_commit=kit["game_commit"]))
sm_manual="Selecione sua ROM original norte-americana de Super Metroid sem cabeçalho. O All-Fix compila as fontes oficiais intactas com Visual Studio 2022; se as ferramentas não estiverem instaladas, será necessário aceitar os termos da Microsoft para obtê-las. O primeiro boot ainda não foi homologado."
sm_media=[dict(id="original-rom",kind="file",extensions=[".smc",".sfc"],version="Super Metroid USA sem cabeçalho; 3145728 bytes; SHA-1 da957f0d63d14cb441d215462904c4fa8519c613")]
for project,tag,profile,commit,first in [
 ("sm","build-578f90b","sm-official-msvc-source-578f90b","578f90b3cc49557bb70060ad033bb90b8cf8ac50",["source/sm.sln","source/src/sm.vcxproj","source/src/packages.config"]),
 ("sm-rewrite","build-5237873","sm-rewrite-official-msvc-source-5237873","523787384a7c912153883b21714f5edabf4e2406",["source/CMakeLists.txt","source/CMakePresets.json","source/vcpkg.json"])]:
 specs.append(dict(project_id=project,tag=tag,build_profile=profile,required_files=first+["source/sm.ini","source/README.md","source/BUILDING.md","source/LICENSE.txt"],manual_steps=sm_manual,preparation_media=sm_media,upstream_commit=commit))
specs.append(dict(project_id="gt5-recomp",tag="build-64ca169",build_profile="gt5-64ca169-official-installer",
 required_files=["source.zip","README.md"],
 manual_steps="Selecione sua ISO decifrada ou pasta PS3_GAME original de Gran Turismo 5 e o firmware PS3 obtido legalmente. O All-Fix executa o instalador oficial, preservando DirectX 12, Vulkan e os complementos gráficos oficiais. Dependências Microsoft e NVIDIA são obtidas somente quando necessárias e após aceite explícito. Ao concluir, use Jogar. Nenhum jogo ou firmware está incluído.",
 preparation_media=[dict(id="original-game",kind="file_or_directory",extensions=[".iso"],version="GT5: ISO decifrada ou pasta PS3_GAME BCES00569/BCUS98114 v01.00"),dict(id="original-firmware",kind="file_or_directory",extensions=[".pup"],version="GT5: pasta dev_flash ou firmware PS3UPDAT.PUP local obtido legalmente")],
 upstream_commit="64ca1697c5f9bb513bfe0414d9a36c10dafd0a37"))
specs.append(json.loads('{"project_id": "god-of-war-recomp", "tag": "build-d1d11ec", "build_profile": "god-of-war-kiexster-d1d11ec-official-installer", "required_files": ["source.zip", "README.md"], "manual_steps": "Selecione sua ISO original americana de God of War para PS2 (SCUS_973.99). O All-Fix executa os scripts oficiais de extração, compilação e execução da KIexster, sem alterar os fontes do projeto. Se faltarem ferramentas Microsoft, o download exige aceite explícito dos termos. A primeira compilação pode demorar; nenhum jogo está incluído.", "preparation_media": [{"id": "original-disc", "kind": "file", "extensions": [".iso"], "version": "ISO original americana de God of War PS2 (SCUS_973.99)."}], "upstream_commit": "d1d11ec545c3baf2f3fc17e2df4247ac4b732d5c"}'))
replacements=policy["approved_recipe_replacements"];blocked={(x["project_id"],x["tag"]) for x in policy["blocked_recipes"]}
results=[]
for spec in specs:
 entry=next(e for e in index["recipes"] if e["project_id"]==spec["project_id"] and e["tag"]==spec["tag"])
 path=ROOT/entry["path"]; archived_path="docs/retired-recipes/"+entry["path"].removeprefix("recipes/");archived=ROOT/archived_path
 if not archived.exists():archived.parent.mkdir(parents=True,exist_ok=True);archived.write_bytes(path.read_bytes())
 old=json.loads(archived.read_bytes());current=json.loads(path.read_bytes())
 recipe=dict(schema_version=9,project_id=spec["project_id"],tag=spec["tag"],source_url=current["source_url"],operations=[],
  required_files=spec["required_files"],inputs=[],manual_steps=spec["manual_steps"],build_profile=spec["build_profile"],preparation_media=spec["preparation_media"])
 save(path,recipe);digest=hashlib.sha256(path.read_bytes()).hexdigest()
 entry.update(sha256=digest,schema_version=9,status="experimental",min_sdk_version="1.5.70",has_inputs=False,has_manual_steps=True)
 for key in ("disabled_reason","disabled_at","audit_reference"):entry.pop(key,None)
 approved=dict(project_id=entry["project_id"],tag=entry["tag"],path=entry["path"],sha256=digest,build_profile=spec["build_profile"],
  retired_path=archived_path,retired_sha256=hashlib.sha256(archived.read_bytes()).hexdigest(),retired_build_profile=old.get("build_profile"),
  upstream_commit=spec["upstream_commit"],audit_reference="docs/OFFICIAL-CONTRACT-RESTORATION-20261128.md")
 if (entry["project_id"],entry["tag"]) in blocked:
  replacements[:]=[v for v in replacements if (v["project_id"],v["tag"])!=(entry["project_id"],entry["tag"])]
  replacements.append(approved)
 schema["oneOf"][:]=[v for v in schema["oneOf"] if v.get("const",{}).get("build_profile")!=spec["build_profile"]]
 schema["oneOf"].append({"const":recipe})
 validator="\n".join(line for line in validator.splitlines() if not(line.startswith("        profiles.append(json.loads(") and spec["build_profile"] in line))+"\n"
 marker="        identities = {";assert marker in validator
 validator=validator.replace(marker,"        profiles.append(json.loads('''"+json.dumps(recipe,ensure_ascii=False)+"'''))\n"+marker,1)
 identity=json.dumps(spec["build_profile"])+":"
 if identity not in validator:validator=validator.replace(marker,marker+"\n            "+identity+" ("+json.dumps(entry["game_id"])+", "+json.dumps(entry["repository"])+"),",1)
 assert "?" not in recipe["manual_steps"]
 results.append(approved);print(json.dumps(approved,ensure_ascii=True))
save(ROOT/"index.json",index);save(ROOT/"docs/official-install-policy.json",policy);save(ROOT/"schemas/installation-recipe-v9.schema.json",schema)
(ROOT/"scripts/validate_recipes.py").write_text(validator,encoding="utf-8",newline="\n")
save(ROOT/"docs/validations/official-scope/official-msys-msvc-gt5-recipe-contracts.json",results)
