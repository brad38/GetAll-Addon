"""Promote only publication/preview metadata; preserve the 140-project evidence."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys

root = Path(sys.argv[1])
evidence = root / "evidence-r18/preview-sdk168-20261127"
old_root = root / "evidence-r18/flow-completion-20261127"
def sha(data):
    return hashlib.sha256(data).hexdigest()
def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))
def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()
def atomic(path, payload):
    temp = path.with_name(path.name + ".sdk168-published.tmp")
    with temp.open("xb") as stream:
        stream.write(payload)
    os.replace(temp, path)

source = old_root / "work-progress-final-sdk168.json"
source_bytes = source.read_bytes()
if sha(source_bytes) != "ddeb9ffffadeb0f92767901969b4aebf5623b7c650e17c83dd9d100457419f28":
    raise ValueError("Final SDK168 evidence changed")
numbered = old_root / "work-progress-140.json"
numbered_sha = sha(numbered.read_bytes())
if numbered_sha != "cb254ea6a9da175851557fc98a0754164b05afd70dbb0137b49443325880ab14":
    raise ValueError("Numbered checkpoint changed")
preview = read(evidence / "preview-result.json")
remote = read(evidence / "remote-pins.json")
if preview["status"] != "PASS" or preview["manifest_sha256"] != sha(
        (root / "publish-getall-sdk168-20261127/ARTIFACT-MANIFEST.json").read_bytes()):
    raise ValueError("Preview result changed")
block = """## Publicação e prévia completas · SDK 1.5.68 · 27/11/2026

**140/148 fluxos integrais implementados**, com a mesma classificação de homologação:
um histórico, 139 aguardando mídia original, um parcial e sete sem receita.
Nenhum novo primeiro boot comercial.

Fontes confirmadas no GitHub, branch work/complete-install-flows-20261127:
Desktop 8ba34eb51ee0ab93accef3da5e1689c68825977d, PR3 draft e CI46059165665
aprovado; GetAll 5b7fea8fb8d2b77df5a6cfd7e9efb6b463fba75b, PR20 draft e
CI46059162398 aprovado. Os registros de envio pendente abaixo são históricos.
Não é necessário pedir autorização para reenviar esses commits já publicados.

A prévia completa está em publish-getall-sdk168-20261127: Desktop 3.0.0,
SDK 1.5.68 e addon 1.5.73, incluindo SotC e Savage Wind. Foram verificados
74 arquivos, 34 recursos nativos, 66 avisos e 12 propriedades, sem recompilar
o executável. AllFix.exe SHA256
3ce6d4ec0e182a450fa621cc8f7a2288250e1485d6be539513f9b8a705a099da;
GetAll-Preview.zip SHA256
656fe2fd35cbda71b3e7974f3c8510ee75edf33b53f7a6c2c29d8e8ef3696914;
manifesto SHA256
0220e843125b9223435d671fcbb834df1d13ce653fb770e6599989f7efd1c95a.
Recibos, hashes e reprodução: evidence-r18/preview-sdk168-20261127.
A instalação corrente e as prévias anteriores foram preservadas.

A instrução vigente do usuário exige gerenciamento contínuo de armazenamento:
remover automaticamente intermediários, mídias sintéticas e extrações
comprovadamente descartáveis após validação, preservando código, receitas,
scripts de reprodução, logs, resultados, originais, dados pessoais e
dependências ativas. Usar caches e toolchains compartilhados. O registro da
limpeza está em LIMPEZA-ARMAZENAMENTO.md.

A investigação continua pelos oito IDs restantes. Metaforce teve uma revisão
oficial localizada no Software Heritage; as fontes e dependências estão em
verificação/compilação. MKW está em prova de um decoder SM86 independente.
Essas investigações não alteram a contagem sem implementação comprovada.

Sem merge, release pública ou promoção adicional a validated. Os checkpoints
numerados 139/140 e o fechamento local final foram preservados. O estado
de publicação está em work-progress-published-sdk168.json e no latest.

---

"""
changes = []
for name in ("CONTINUIDADE.md", "PENDENCIAS.md"):
    path = root / name
    before = path.read_bytes()
    text = before.decode("utf-8-sig")
    if "## Publicação e prévia completas · SDK 1.5.68" in text:
        raise ValueError("Metadata already promoted")
    first, rest = text.split("\n", 1)
    after = (first + "\n\n" + block + rest.lstrip("\n")).encode()
    changes.append((path, before, after))
matrix = root / "MATRIZ-FUNCIONAL.md"
matrix_before = matrix.read_bytes()
changes.append((matrix, matrix_before, matrix_before.rstrip(b"\r\n") + b"\n\n" + block.encode()))
old = json.loads(source_bytes)
if (old["implemented"], old["total"], old["recipes"], old["recipe_projects"]) != (140,148,143,141):
    raise ValueError("Coverage changed")
updated = json.loads(source_bytes)
updated["metadata"] = block
updated["newly_closed"] = []
updated["previous_metadata_checkpoint"] = "work-progress-final-sdk168.json"
updated["publication_verified_utc"] = datetime.now(timezone.utc).isoformat()
updated["finalization"]["status"] = "published_ci_pass_preview_complete"
updated["finalization"]["remote_publication"] = remote
updated["finalization"]["complete_preview"] = preview
updated["storage_policy"] = {
    "automatic_cleanup_authorized": True,
    "preserve": ["source", "recipes", "reproduction_scripts", "relevant_logs",
                 "test_results", "original_media", "personal_data", "active_dependencies"],
    "dispose_after_validation": ["intermediate_builds", "synthetic_media", "temporary_extractions"],
    "reuse_shared_caches_and_toolchains": True,
}
for key in ("counts","implemented","total","recipes","recipe_projects","closed_this_round","promotion_validation"):
    if updated[key] != old[key]:
        raise ValueError("Coverage or validation evidence was modified")
latest = old_root / "work-progress-latest.json"
changes.append((latest, latest.read_bytes(), encoded(updated)))
destination = old_root / "work-progress-published-sdk168.json"
if destination.exists():
    raise ValueError("Published checkpoint already exists")
backup = evidence / "continuity-before-publication"
backup.mkdir()
records = []
for path, before, after in changes:
    (backup / path.name).write_bytes(before)
    records.append({"path":str(path),"before_sha256":sha(before),"after_sha256":sha(after),
                    "backup":str(backup / path.name)})
destination.write_bytes(encoded(updated))
for path, before, after in changes:
    if path.read_bytes() != before:
        raise ValueError("Concurrent edit: " + str(path))
    atomic(path, after)
if sha(numbered.read_bytes()) != numbered_sha or source.read_bytes() != source_bytes:
    raise ValueError("Historical evidence changed")
result = {"status":"PASS","published_checkpoint":str(destination),
          "published_checkpoint_sha256":sha(destination.read_bytes()),
          "checkpoint140_unchanged_sha256":numbered_sha,"changes":records}
(evidence / "continuity-result.json").write_bytes(encoded(result))
print(json.dumps(result, ensure_ascii=False))
