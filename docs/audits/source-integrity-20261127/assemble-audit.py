#!/usr/bin/env python3
"""Consolidate existing audit evidence. Writes only this audit directory."""
from pathlib import Path
from collections import Counter
import hashlib
import json

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
DESKTOP = REPO.parent / "audit-desktop-source"


def read(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


catalog = read("catalog-review.json")
routing = read("service-routing-review.json")
root = read("root-review.json")
helpers = read("native-helpers-review.json")
by_route = {p["project_id"]: p for p in routing["projects"]}
by_source = {i: g for g in root["source_change_groups"] for i in g["project_ids"]}
by_other = {i: g for g in root["other_reviewed_build_groups"] for i in g["project_ids"]}
by_helper = {}
for finding in helpers["findings"]:
    for project_id in finding["projects"]:
        by_helper.setdefault(project_id, []).append(finding)
# Both profiles invoke the same helper resource/hash and extraction command.
# GameInstallationPicori.cs:91-106 differs only in runtime acquisition.
by_helper["autotmc-auto-tmc"] = list(by_helper.get("project-picori-999sian-tmc", []))

translations = {
    "release_import_no_runtime_source_edit_observed_in_installer": "Release/importação; sem edição de fonte do runtime observada no instalador",
    "release_and_original_title_update_import_no_runtime_source_edit_observed": "Release e atualização original; sem edição de fonte observada no instalador",
    "release_plus_fixed_native_helper_not_rebuilt_in_this_review": "Release + auxiliar nativo; ver proveniência, sem reconstrução do binário",
    "release_plus_bundled_official_extraction_conversion_tool_not_rebuilt": "Release + ferramenta oficial de extração/conversão; binário não reconstruído",
    "custom_adapter_source_calls_upstream_unpacker": "Adapter próprio chama extrator oficial",
    "custom_extractor_adapter_with_build_source_edit": "Adapter de extração próprio com alteração de build",
    "custom_patcher_adapter_using_verified_upstream_patcher_sources": "Adapter próprio aplica patch oficial com fontes centrais comparadas",
    "generated_metadata_or_launch_configuration_changed": "Metadados/configuração de lançamento alterados",
    "official_generator_or_compiler_invoked_no_source_edit_observed_in_caller": "Gerador/compilador oficial; sem edição de fonte observada no chamador",
    "official_runtime_extraction_shader_cache_overlay_commands": "Comandos oficiais de extração/runtime/cache",
    "official_source_compile_with_local_feature_flags": "Fonte oficial compilado com opções locais",
    "original_media_language_configuration_rewritten": "Configuração de idiomas da mídia reescrita",
    "original_title_update_applied": "Atualização original aplicada",
    "upstream_binary_patch_delta_or_code_generation": "Patch binário/codegen do upstream",
    "upstream_feature_options_selected": "Seleção de opções de recursos do upstream",
    "no_indexed_recipe_no_build_route": "Sem receita/sem rota de build",
}

absent = {
    "twilight-princess-courage-reborn": "Pacote/fonte oficial não obtido; launcher não confirmado",
    "project-2099": "Instalador público; runtime completo e fluxo de mídia não comprovados",
    "doldecomp-mkdd-decompilacao-base": "Decompilação GameCube; não é port Windows",
    "tmc-decompilacao-base": "Decompilação GBA; distinta de Picori",
    "mml1-megaman-legends-decomp": "Decompilação PS1; distinta de Modernization Project",
    "wind-waker-recomp": "Sucessão/duplicidade com BlueWake",
}

rows = []
for original in catalog["projects"]:
    ident = original["project_id"]
    route = by_route[ident]
    detail = by_source.get(ident) or by_other.get(ident)
    categories = []
    for category in route["observed_categories"]:
        if category == "source_build_body_review_in_companion_report":
            continue
        categories.append(translations[category])
    if ident in by_source:
        categories.insert(0, by_source[ident]["classification"])
    elif ident in by_other:
        categories.insert(0, "Pipeline/build/configuração examinados no relatório de fontes")
    if not original["has_indexed_recipe"]:
        categories = [absent[ident]]
    if ident == "sm64plus":
        categories = ["Receita build: diretório de dados e build alterados; alias LauncherMirror: pacote oficial com etapa manual"]
    elif ident == "crash-team-racing-turbocharged":
        categories = ["Receita build: argumento de validação de disco acrescentado; alias CI: pacote oficial com etapa manual"]
    elif ident == "mkw-recomp":
        categories = ["Variante allfix-cli: funcionalidade nova no compilador de shaders e mudanças semânticas; alias legado separado"]
    sources = list(route["sources_read"])
    if detail:
        existing = {s["path"] for s in sources}
        for path in detail["sources"]:
            if path not in existing:
                sources.append({
                    "path": path,
                    "coverage": "body_and_production_consumers_reviewed",
                    "sha256": sha(DESKTOP / path),
                    "url": f'https://github.com/brad38/Allfix/blob/{root["desktop_commit"]}/{path}',
                })
    helper_findings = by_helper.get(ident, [])
    reports = ["catalog-review.json", "service-routing-review.json"]
    if detail:
        reports.append("root-review.json")
        if detail.get("detail_report"):
            reports.append(detail["detail_report"])
    if helper_findings:
        reports.append("native-helpers-review.json")
    if ident == "mega-man-legends-modernization-project":
        reports.append("mml-parity-review.json")
    if ident == "unleashedrecomp":
        reports.append("unleashed-helper-review.json")
    rows.append({
        "row": original["row"], "project_id": ident,
        "game_title": original["game_title"], "project_name": original["project_name"],
        "catalog_source": original["catalog_source"],
        "catalog_status": original["catalog_status"],
        "catalog_replaced_by": original["catalog_replaced_by"],
        "has_recipe": original["has_indexed_recipe"],
        "recipes": [{"path": x["path"], "sha256": x["sha256"], "tag": x["contract"]["tag"],
                     "index_status": x["index_status"]} for x in original["recipes"]],
        "routes": route["routes"], "classification": categories,
        "documented_game_runtime_build_source_change_group": by_source[ident]["id"] if ident in by_source else None,
        "source_change_scope": "Only the 19 IDs in root source_change_groups; excludes auxiliary importers. Null is not a source-purity certification. See helper_findings and binary limits.",
        "reviewed_pipeline_summary": detail["summary"] if detail else None,
        "helper_findings": helper_findings,
        "helper_scope_notes": "Same Picori helper/hash/command as project-picori-999sian-tmc; GameInstallationPicori.cs:91-106" if ident == "autotmc-auto-tmc" else None,
        "sources_read": sources,
        "shared_dispatch_read": route["shared_dispatch_read"],
        "coverage": "no_recipe" if not original["has_indexed_recipe"] else "recipe_route_and_handler_body_reviewed",
        "evidence_reports": reports,
        "boot_evidence": original["boot_evidence"],
        "binary_limit": route["helper_binary_reproduction"],
        "interpretation_limit": route["interpretation_limit"],
    })

result = {
    "schema_version": 1, "audit_date_local": root["audit_date_local"], "pins": catalog["pins"],
    "counts": {**catalog["counts"], "mapped_ids": sum(x["has_recipe"] for x in rows),
               "unmapped_ids": 0, "source_tree_change_ids": len(by_source),
               "additional_build_pipeline_ids": len(by_other), "route_families": len(routing["groups"])},
    "limits": root["limitations"], "projects": rows,
}
write("audit-matrix.json", result)

def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


helper_labels = {
    "H01-bluewake": "Fonte do importador alterado e wrapper próprio",
    "H02-nectar": "Wrapper próprio; leitor oficial sem mudança",
    "H03-kingsfield": "Wrapper/compatibilidade; perfil de extração japonês",
    "H04-know-your-role": "Launcher compilado com dependências fixadas",
    "H05-soh": "Patch de CLI admitido; diff correspondente não recuperado",
    "H06-twoship": "Build do extrator alterado; parsers comparados sem mudança",
    "H07-starship": "Fonte do extrator comparado; opções de perfil",
    "H08-paperboat": "Fonte do extrator comparado; opções de perfil",
    "H09-ghostship": "Fonte do extrator comparado; opções de perfil",
    "H10-spaghetti": "Fonte Torch comparado sem mudança; limites de defines.h",
    "H11-lighthouse": "Torch sem mudança; patch de pesquisa não atribuído ao produto",
    "H12-picori": "Extrator oficial em build separado; mesma ferramenta em AutoTMC",
    "H13-gt4": "Wrapper próprio da biblioteca oficial de disco",
}


lines = [
    "# Matriz de auditoria — 148 IDs do catálogo", "",
    "Referência: 27/11/2026, America/Fortaleza. **142 IDs têm receita; seis não têm.** "
    "A revisão de rotas e corpos dos handlers cobre os 142. Isso não certifica todos os binários "
    "nem todas as funções dos upstreams. O único `validated` é histórico; nenhum boot comercial foi executado nesta auditoria.", "",
    "Alteração de fonte refere-se aos 19 IDs documentados nos grupos do relatório principal; "
    "auxiliares de extração têm proveniência e limites próprios. Os aliases não são contados como projetos novos.", "",
    "A versão [JSON](audit-matrix.json) contém hashes das receitas, métodos, URLs fixadas, relatórios, "
    "resumos completos e achados específicos dos auxiliares. Leia também o [relatório principal](README.md).", "",
    "| Nº | Jogo / projeto e ID | Rota | Natureza observada | Auxiliar / limite | Boot |", 
    "|---:|---|---|---|---|---|",
]
for row in rows:
    title = f'{row["game_title"]} — {row["project_name"]}<br>`{row["project_id"]}`'
    helpers_text = "; ".join(f'{f["id"]}: {helper_labels[f["id"]]}' for f in row["helper_findings"])
    if not helpers_text:
        helpers_text = "Ver limites de fonte/binário no JSON" if row["has_recipe"] else "Sem implementação"
    boot = "Histórico: relato SM64 Coop Deluxe; não reexecutado" if row["project_id"] == "sm64coopdx-super-mario-64-coop-deluxe" else ("Não comprovado nesta rodada" if row["has_recipe"] else "Sem receita")
    vals = [row["row"], title, ", ".join(row["routes"]) or "—", "; ".join(row["classification"]), helpers_text, boot]
    lines.append("| " + " | ".join(cell(x) for x in vals) + " |")
(HERE / "MATRIZ-148.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

sources = sorted({s["path"] for row in rows for s in row["sources_read"]})
write("reviewed-source-manifest.json", {
    "commit": root["desktop_commit"],
    "note": "Named source entrypoints and additional reviewed files. Not a claim that all upstream functions were reviewed.",
    "files": [{"path": x, "size": (DESKTOP / x).stat().st_size, "sha256": sha(DESKTOP / x)} for x in sources],
})
print(json.dumps({"projects": len(rows), "recipes": sum(len(x["recipes"]) for x in rows),
                  "source_change_ids": len(by_source), "other_build_ids": len(by_other),
                  "named_source_files": len(sources)}, ensure_ascii=False))
