"""Record the verified 142-project checkpoint without changing historical evidence."""
from collections import Counter
from datetime import datetime, timezone
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

DESKTOP = "921295de12349e726f7ca21a5edd8a8ecee123d8"
GETALL = "37fbc54ee2d137952d8f1ca2b06f3602410870c9"
PREVIEW = "18cbb75144560fbacbe20708b0b3a63a95577d85490a814cc4dece4d770d9590"
HISTORICAL140 = "cb254ea6a9da175851557fc98a0754164b05afd70dbb0137b49443325880ab14"
STORE = "22804295925878e3a43bb1173109bd68a5728dc48db63723a1347862abd8c69f"
BUILD = "51f98c91d7a0ff2a925ac0a5043217e795ece487fa5478347acfa0f3277229a9"
IMPLEMENTED = "Instalação integral implementada, aguardando mídia original"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def atomic(path, payload):
    temp = path.with_name(path.name + ".sdk169.tmp")
    with temp.open("xb") as stream:
        stream.write(payload)
    os.replace(temp, path)


def prepend(path, block):
    before = path.read_bytes()
    first, rest = before.decode("utf-8-sig").split("\n", 1)
    return before, (first.rstrip("\r") + "\n\n" + block + rest.lstrip("\r\n")).encode("utf-8")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--task-root", type=Path, required=True)
    p.add_argument("--storage-summary", type=Path, required=True)
    p.add_argument("--storage-sha256", required=True)
    a = p.parse_args()
    b = a.task_root.absolute()
    f = b / "evidence-r18/flow-completion-20261127"
    e = b / "evidence-r18/preview-sdk169-20261127"
    numbered140 = f / "work-progress-140.json"
    require(digest(numbered140.read_bytes()) == HISTORICAL140, "Historical checkpoint changed")
    preview_path = b / "publish-getall-sdk169-20261127/ARTIFACT-MANIFEST.json"
    require(digest(preview_path.read_bytes()) == PREVIEW, "Verified preview changed")
    preview = read(e / "preview-result.json")
    require(preview["status"] == "PASS" and preview["manifest_sha256"] == PREVIEW and
            preview["desktop_commit"] == DESKTOP and preview["getall_commit"] == GETALL and
            preview["files"] == 79, "Preview receipt differs")
    remote = read(e / "remote-pins.json")
    for repo, commit in (("brad38/Allfix", DESKTOP), ("brad38/GetAll-Addon", GETALL)):
        item = next(x for x in remote["repositories"] if x["repository"] == repo)
        require(item["commit"] == commit and item["draft"] and not item["merged"] and
                any(x["status"] == "completed" and x["conclusion"] == "success"
                    for x in item["workflow_runs"]), "Remote publication evidence differs")
    store_path = f / "store-assembly-proof-sdk169-result/result.json"
    require(digest(store_path.read_bytes()) == STORE, "Store proof changed")
    store = read(store_path)
    require(store["status"] == "PASS" and store["checks"] == 20 and
            store["desktop_commit"] == DESKTOP and store["git_state_unchanged"] and
            store["desktop_assembly_unchanged"] and store["candidate_unchanged"], "Store gates failed")
    build_path = f / "build31d-result.json"
    require(digest(build_path.read_bytes()) == BUILD, "Integrated gate changed")
    build = read(build_path)
    require(build["status"] == "PASS" and build["sources_checked"] == 538, "Integrated gate failed")
    for root, revision in ((b / "desktop-continuation-20261127", DESKTOP),
                           (b / "getall-sdk169-final-20261127", GETALL)):
        git = [r"C:\Program Files\Git\cmd\git.exe", "-C", str(root)]
        require(subprocess.check_output(git + ["rev-parse", "HEAD"], text=True).strip() == revision,
                "Source checkout moved")
        require(not subprocess.check_output(git + ["status", "--porcelain"], text=True).strip(),
                "Source checkout is not clean")
    storage_bytes = a.storage_summary.read_bytes()
    require(digest(storage_bytes) == a.storage_sha256, "Storage summary changed")
    storage = json.loads(storage_bytes)
    total = storage["total"]
    added = [value for key, value in storage.items() if key.startswith("added_")]
    require(total["logical_bytes_removed"] == storage["baseline"]["logical_bytes_removed"] +
            sum(x["logical_bytes_removed"] for x in added), "Storage byte total differs")
    require(total["removed_files"] == storage["baseline"]["removed_files"] +
            sum(x["removed_files"] for x in added), "Storage file total differs")
    storage_gb = f"{total['logical_bytes_removed'] / 1e9:.2f}".replace(".", ",")
    block = f"""## Fechamento publicado · SDK 1.5.69 · 27/11/2026

**142/148 fluxos integrais implementados**: um homologado histórico,
141 aguardando mídia original, zero parciais e seis sem receita. Metaforce
e a preparação automática de Mario Kart World foram integrados. O índice
tem 145 receitas para 142 projetos, com 144 entradas experimentais e uma
homologação histórica. Nenhum novo primeiro boot comercial foi comprovado.

Desktop {DESKTOP}, PR 3 draft, CI 46089235002 aprovado.
GetAll {GETALL}, PR 20 draft, CI 46089870630 aprovado.
Branch work/complete-install-flows-20261127, sem merge ou release pública.
As atualizações documentais posteriores não mudam esses pins da prévia.

BUILD31d: 0 erros/0 avisos, 1.967 verificações aprovadas, parser 145/145,
Metaforce Policy 52 e Store real 20. NativeStage Metaforce 19 e MKW Native8
77 verificações/14 SPIR-V foram preservados, sem repetir os builds nativos.
As provas autorais e de --help não equivalem a boot comercial nem execução GPU.

Prévia pronta: publish-getall-sdk169-20261127, Desktop 3.0.0, SDK 1.5.69,
addon 1.5.74, 79 arquivos, 35 recursos, 71 avisos e 12 propriedades auditadas.
Manifesto SHA256 {PREVIEW}.
AllFix.exe SHA256 b558afccf6fa50ec9a3899b66055009f04f8ce71cfc4dbcc6ab3886bd0433fcd.
Addon SHA256 dbc36433b462070682949fc211ce8ce2c51b8477141d55251ce440fbc57d9a2e.
Prévia SDK 167/168 e instalação corrente preservadas. O candidato intermediário
redundante foi removido após a cópia verificada; seus recibos foram conservados.

Restam seis contratos externos: Courage Reborn sem fonte acessível; Project 2099
sem runtime e preparação completos; MKDD/TMC/MML1 base sem port Windows
correspondente; Wind Waker Recomp com sucessor BlueWake já coberto. Os 148 IDs
foram preservados. Não duplicar sucessores nem contar um kit como jogo pronto.

Armazenamento: {total['batches']} lotes, {total['removed_files']} arquivos,
{total['logical_bytes_removed']} bytes lógicos removidos (aproximadamente
{storage_gb} GB). Fontes, receitas, reprodução, logs, resultados, mídia original,
dados pessoais e dependências em uso foram preservados. Caches/toolchains
continuam compartilhados. Detalhes em LIMPEZA-ARMAZENAMENTO.md e nos recibos.

Os registros abaixo são históricos. Metaforce/MKW e seus antigos bloqueios
foram atualizados neste fechamento; não substituir 142 por uma contagem antiga.

---

"""
    latest = f / "work-progress-latest.json"
    latest_before = latest.read_bytes()
    old = json.loads(latest_before)
    require((old["implemented"], old["total"], old["recipes"], old["recipe_projects"], old["sdk_version"]) ==
            (140, 148, 143, 141, "1.5.68"), "Unexpected previous checkpoint")
    catalog_path = b / "evidence-r18/complete-flows-publish-20261127/catalog.json"
    require(digest(catalog_path.read_bytes()) == read(preview_path)["catalog_sha256"], "Catalog changed")
    ids = {p["id"] for g in read(catalog_path)["games"] for p in g["projects"]}
    require(len(ids) == 148, "Catalog identity count changed")
    matrix = b / "MATRIZ-FUNCIONAL.md"
    matrix_before = matrix.read_bytes()
    lines = matrix_before.decode("utf-8-sig").splitlines()
    rows = {}
    changes_by_id = {
        "metaforce": ("SDK 1.5.69; perfil fixo de8fc69, leitor DOL/FST, ferramentas compartilhadas, build/transação, recuperação e Jogar com ISO externa e saves separados.",
                      "Metaforce nativo compilado; Media44, Policy 52, NativeStage19; BUILD31d/CI 115; nenhuma ISO comercial ou boot executado."),
        "mkw-recomp": ("SDK 1.5.69; variante local v0.1.18-allfix-cli, CLI nvdisasm fixada, fontes e descritor verificados, retomada/registro/Jogar; receita legada preservada.",
                       "Native8:77 verificações,14 SPIR-V válidos em 5 estágios; alias 43 e Store real 20; BUILD31d/CI 115; sem execução GPU ou boot comercial."),
    }
    for index, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        cells = [x.strip() for x in line.split("|")[1:-1]]
        if len(cells) != 5 or cells[1] not in ids:
            continue
        require(cells[1] not in rows, "Duplicate matrix project")
        if cells[1] in changes_by_id:
            cells[2] = IMPLEMENTED
            cells[3], cells[4] = changes_by_id[cells[1]]
            lines[index] = "| " + " | ".join(cells) + " |"
        rows[cells[1]] = cells
    require(set(rows) == ids, "Matrix must preserve all 148 IDs")
    counts = dict(Counter(x[2] for x in rows.values()))
    require(counts == {IMPLEMENTED: 141, "Instalação integral homologada": 1, "Sem receita, bloqueado": 6},
            "Unexpected matrix counts")
    counts["Instalação parcialmente automatizada"] = 0
    first, rest = "\n".join(lines).split("\n", 1)
    matrix_after = (first + "\n\n" + block + rest.lstrip("\n") + "\n").encode("utf-8")
    changes = [(matrix, matrix_before, matrix_after)]
    for name in ("CONTINUIDADE.md", "PENDENCIAS.md"):
        path = b / name
        before, after = prepend(path, block)
        changes.append((path, before, after))
    storage_log = b / "LIMPEZA-ARMAZENAMENTO.md"
    storage_block = f"""## Consolidação SDK 1.5.69 · 27/11/2026

{total['batches']} lotes concluídos: **{total['removed_files']} arquivos e
{total['logical_bytes_removed']} bytes lógicos removidos**, aproximadamente
{storage_gb} GB. Os valores são tamanhos de arquivos descartados, não uma
medição atual do espaço livre. O resumo estruturado tem SHA256
{a.storage_sha256} e foi preservado em evidence-r18/preview-sdk169-20261127/storage-summary.json.

Os lotes novos incluem cópias verificadas de nvdisasm, fixtures autorais,
transporte temporário e os intermediários descritos nos respectivos recibos.
Código, receitas, scripts, logs, testes e manifestos foram preservados.
Prévia completa 169, prévias 167/168, caches/toolchains, originais, dados
pessoais e dependências ativas ficaram fora da exclusão. O candidato 169
redundante foi removido após comparação byte/hash com a prévia completa.

---

"""
    before, after = prepend(storage_log, storage_block)
    changes.append((storage_log, before, after))
    updated = json.loads(latest_before)
    updated.update(date="2026-11-27", sdk_version="1.5.69", implemented=142, total=148,
                   recipes=145, recipe_projects=142, counts=counts,
                   newly_closed=["metaforce", "mkw-recomp"], metadata=block,
                   previous_checkpoint=140, previous_metadata_checkpoint="work-progress-published-sdk168.json")
    updated["closed_this_round"] += ["metaforce", "mkw-recomp"]
    require(len(updated["closed_this_round"]) == len(set(updated["closed_this_round"])) == 28,
            "Closed project list differs")
    updated["promotion_validation"].update({
        "metaforce": {"media_checks": 44, "build_policy_checks": 52, "native_stage_checks": 19,
                      "evidence": "docs/validations/metaforce-de8fc69", "commercial_boot": False},
        "mkw-recomp": {"native_checks": 77, "spirv_validated": 14, "release_policy_checks": 43,
                       "store_assembly_checks": 20, "evidence": "docs/validations/mkw-sm86-cli", "commercial_boot": False},
    })
    updated["publication_verified_utc"] = datetime.now(timezone.utc).isoformat()
    updated["finalization"] = {
        "status": "published_ci_pass_preview_complete", "desktop_commit": DESKTOP,
        "getall_recipe_commit": GETALL, "remote_publication": remote, "complete_preview": preview,
        "integrated_gate_sha256": BUILD, "store_gate_sha256": STORE,
        "numbered140_preserved": True, "numbered140_sha256": HISTORICAL140,
        "storage_summary_sha256": a.storage_sha256, "storage_totals": total,
        "matrix_project_rows_sha256": digest(encoded(rows)),
        "previous_finalization_checkpoint": "work-progress-published-sdk168.json",
    }
    changes.append((latest, latest_before, encoded(updated)))
    destinations = [f / "work-progress-142.json", f / "work-progress-published-sdk169.json"]
    require(all(not x.exists() for x in destinations), "SDK169 checkpoint already exists")
    evidence_outputs = [e / "storage-summary.json", e / "continuity-result.json"]
    require(all(not x.exists() for x in evidence_outputs), "Continuity evidence output already exists")
    require(a.storage_summary.absolute() != evidence_outputs[0].absolute(),
            "Storage summary input must be separate from the preserved output")
    require(all(not path.with_name(path.name + ".sdk169.tmp").exists() for path, _, _ in changes),
            "A continuity temporary file already exists")
    backup = e / "continuity-before-sdk169"
    require(not backup.exists(), "Continuity backup already exists")
    require(all(path.read_bytes() == before for path, before, _ in changes), "Concurrent continuity edit")
    backup.mkdir()
    records = []
    for path, before, after in changes:
        (backup / path.name).write_bytes(before)
        records.append({"path": str(path), "before_sha256": digest(before), "after_sha256": digest(after)})
    for path in destinations:
        with path.open("xb") as stream:
            stream.write(encoded(updated))
    with (e / "storage-summary.json").open("xb") as stream:
        stream.write(storage_bytes)
    for path, before, after in changes:
        require(path.read_bytes() == before, "Concurrent edit: " + str(path))
        atomic(path, after)
    require(digest(numbered140.read_bytes()) == HISTORICAL140, "Historical checkpoint was altered")
    result = {"status": "PASS", "implemented": 142, "projects": 148, "recipes": 145,
              "counts": counts, "newly_closed": ["metaforce", "mkw-recomp"],
              "checkpoint_sha256": digest(destinations[0].read_bytes()),
              "storage_totals": total, "changes": records,
              "completed_utc": datetime.now(timezone.utc).isoformat()}
    with (e / "continuity-result.json").open("xb") as stream:
        stream.write(encoded(result))
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
