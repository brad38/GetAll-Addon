"""Complete the upstream-documented CTR disc placement through the generic importer."""
import pathlib,json,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[3]
path=ROOT/"recipes/crash-team-racing/crash-team-racing-turbocharged/ci-07d0c49.json"
raw=path.read_bytes();recipe=json.loads(raw)
target="ctr-turbocharged-turbocharged-07d0c49-windows-x86/assets/ctr-u.bin"
recipe["operations"]=[{"kind":"import_input","scope":"installation","source":"original-ctr-us-bin","target":target}]
recipe["inputs"]=[{"id":"original-ctr-us-bin","kind":"file","name":"Imagem original Crash Team Racing NTSC-U 926",
 "description":"Selecione o BIN bruto MODE2/2352 da sua própria cópia de Crash Team Racing USA NTSC-U 926. O All-Fix confere o tamanho e SHA-256 do perfil oficial e copia a imagem para assets/ctr-u.bin, conforme o procedimento do Turbocharged. A mídia original é preservada.",
 "extensions":[".bin"],"required":True,"size":605698800,
 "sha256":"f780bf2331476aabfc00772fa758b12dd95ebfbc907968132cbd3cdd4e2c07c0"}]
recipe.pop("manual_steps",None)
path.write_text(json.dumps(recipe,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
index_path=ROOT/"index.json";index=json.loads(index_path.read_text(encoding="utf-8"))
entry=next(e for e in index["recipes"] if e["project_id"]==recipe["project_id"] and e["tag"]==recipe["tag"])
entry["sha256"]=hashlib.sha256(path.read_bytes()).hexdigest();entry["has_inputs"]=True;entry["has_manual_steps"]=False
index_path.write_text(json.dumps(index,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
review={"project_id":recipe["project_id"],"tag":recipe["tag"],"previous_sha256":hashlib.sha256(raw).hexdigest(),"recipe_sha256":entry["sha256"],
 "upstream_commit":"07d0c49f01d62dcb9887b455be27ce65728ee893",
 "upstream_procedure":"README.md explicitly permits copying the player's own raw NTSC-U MODE2/2352 image to assets/ctr-u.bin next to the unchanged official executable.",
 "media_profile":{"source":"https://github.com/CTR-tools/ctr-native/blob/79d6f1e925c62e85cef2c0f6514e56584e9eb67b/metadata/retail/ntsc-u-926/matching.json",
 "target":"ntsc-u-926","size":605698800,"sha256":recipe["inputs"][0]["sha256"]},
 "implementation":"Existing schema-v5 import_input verifies size/hash, stages the copy and preserves the original. The game keeps its own optional font, graphics and update-check settings.",
 "limits":["Only the documented canonical NTSC-U 926 BIN is automated. Other structurally valid dumps remain supported by the upstream interactive importer, outside this exact GetAll input contract.",
 "The CI download remains pinned to its official artifact; expiry must be handled as an unavailable source, never replaced by a mirror.",
 "No original-media import, first boot or gameplay was performed in this review."]}
(ROOT/"docs/validations/official-scope/ctr-ci-import-review.json").write_text(json.dumps(review,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
print(json.dumps({"recipe":entry["path"],"sha256":entry["sha256"]}))
