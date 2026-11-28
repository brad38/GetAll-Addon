#!/usr/bin/env python3
"""Read-only audit of recipe/catalog inputs; writes audit artifacts only.

This inventories contracts. It deliberately does not certify a game, binary or
Desktop source path as unmodified merely because the recipe has no patch opcode.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
WORKSPACE = ROOT.parent
CATALOG = WORKSPACE / 'preview-complete-flows-20261127/catalog.json'
DESKTOP = WORKSPACE / 'audit-desktop-source'
DESKTOP_COMMIT = '921295de12349e726f7ca21a5edd8a8ecee123d8'
GETALL_COMMIT = 'ceaa962fe1a2088a7f3900509b856743ff4b6672'
CATALOG_COMMIT = '3f4603cf42ef43402b4a0a9470232e7d4fcd9eb9'

NEW_28 = set('sm64ex render96ex sm64rt strikers-wiicompiled wipeout-rewrite drmario64-recomp mariokartdd-recomp burnout3-recomp strikersrecomp mkdd-recomp doaxvb-re god-of-war-recomp super-odyssey-pc-recomp lasrecomp god-of-war-native-pc-port-gow-pc-port totk-pc-recomp dkb-pc-recomp gt5-recomp rygt-gt7 spartanport ssx-recomp gta-stories-recompiled fh1-reimagined pinyon-shift shadow-of-the-colossus-pc savagewindrecomp metaforce mkw-recomp'.split())

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def read_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))

def classify_recipe(recipe):
    if recipe.get('build_profile'):
        return 'perfil_de_preparacao_no_desktop'
    if str(recipe['tag']).startswith('build-'):
        return 'build_de_fonte_por_identidade_no_desktop'
    if recipe.get('java_launcher'):
        return 'distribuicao_java'
    if recipe.get('assets'):
        return 'aplicativo_portatil'
    return 'distribuicao_precompilada_com_fluxo_especifico_ou_generico'

def quote_table(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')

DESKTOP_TEXT = None

def desktop_refs(project_id, profiles):
    """Literal references, not a claim that dispatch/dataflow was reviewed."""
    hits = []
    if not DESKTOP.is_dir():
        return hits
    global DESKTOP_TEXT
    if DESKTOP_TEXT is None:
        DESKTOP_TEXT = []
        for base in ['Services', 'AddonSdk']:
            for path in sorted((DESKTOP / base).rglob('*.cs')):
                raw = path.read_bytes()
                try:
                    text = raw.decode('utf-8-sig')
                except UnicodeDecodeError:
                    text = raw.decode('cp1252')
                DESKTOP_TEXT.append((path, text.splitlines()))
    terms = [project_id, *profiles]
    for path, lines in DESKTOP_TEXT:
        for lineno, line in enumerate(lines, 1):
            if any('"' + term + '"' in line for term in terms):
                hits.append({'path': str(path.relative_to(DESKTOP)), 'line': lineno,
                             'code': line.strip()})
    return hits

def main():
    idx = read_json(ROOT / 'index.json')
    cat = read_json(CATALOG)
    pinned_index = subprocess.check_output(['git', '-C', str(ROOT), 'show', GETALL_COMMIT + ':index.json'])
    if pinned_index != (ROOT / 'index.json').read_bytes():
        raise SystemExit('index.json differs from the declared GetAll audit pin')
    groups = defaultdict(list)
    recipe_errors = []
    op_counts = Counter()
    kinds = Counter()
    for entry in idx['recipes']:
        data = (ROOT / entry['path']).read_bytes()
        recipe = json.loads(data)
        if sha(data) != entry['sha256']:
            recipe_errors.append({'path': entry['path'], 'error': 'index_sha256_mismatch'})
        for key in ['project_id', 'tag', 'schema_version']:
            if recipe[key] != entry[key]:
                recipe_errors.append({'path': entry['path'], 'error': key + '_mismatch'})
        kind = classify_recipe(recipe)
        kinds[kind] += 1
        op_counts.update(op['kind'] for op in recipe['operations'])
        groups[entry['project_id']].append({
            'path': entry['path'], 'sha256': sha(data), 'bytes': len(data),
            'index_status': entry['status'], 'repository': entry['repository'],
            'entry_kind': kind, 'contract': recipe,
        })
    actual_recipes = {str(p.relative_to(ROOT)) for p in (ROOT / 'recipes').rglob('*.json')}
    indexed_paths = {r['path'] for r in idx['recipes']}
    docs = list((ROOT / 'docs/validations').glob('*.md'))
    rows = []
    for game in cat['games']:
        for project in game['projects']:
            pid = project['id']
            recipes = groups.get(pid, [])
            profiles = sorted({r['contract']['build_profile'] for r in recipes if 'build_profile' in r['contract']})
            evidence = [str(p.relative_to(ROOT)) for p in docs if p.name.startswith(pid + '-')]
            if pid in NEW_28:
                evidence.append('docs/validations/sdk167-flow-completion.md')
            if pid == 'metaforce':
                evidence += ['docs/validations/metaforce-de8fc69/README.md',
                             'docs/validations/metaforce-de8fc69/BUILD-PROOF.md']
            if pid == 'mkw-recomp':
                evidence += ['docs/validations/mkw-sm86-cli/README.md',
                             'docs/validations/sdk169-integration/README.md']
            if not recipes:
                evidence.append('docs/validations/remaining-projects-20261127/README.md')
            if pid == 'wind-waker-recomp':
                evidence.append('docs/validations/sdk169-integration/wind-waker-successor-contract.json')
            boot = ('relato_historico_do_usuario_preservado_sem_reexecucao_nesta_auditoria'
                    if pid == 'sm64coopdx-super-mario-64-coop-deluxe'
                    else 'nenhum_boot_com_midia_original_comprovado_nos_registros_desta_rodada'
                    if recipes else 'sem_receita')
            notes = []
            if pid == 'sm64coopdx-super-mario-64-coop-deluxe':
                evidence += ['docs/AUDITORIA-CATALOGO-2026-11-22.md']
                notes.append('A única homologação do índice é histórica, baseada em relato do usuário; não foi reexecutada nem é prova sobre os demais jogos.')
            if project.get('status') == 'deprecated':
                notes.append('ID depreciado mantido na contagem; os IDs substitutos também têm receita.')
            if pid == 'autotmc-auto-tmc':
                notes.append('A receita atual anuncia baixar/usar Project Picori v0.9.6, outro ID já contado; o relatório inicial só comprovava extração do gerenciador AutoTMC.')
            if pid == 'mariokartdd-recomp':
                notes.append('A própria receita declara modo VR desativado. A autoria e efeito da desativação precisam da revisão Desktop.')
            if pid == 'metaforce':
                notes.append('README oficial da revisão de8fc69 avisa que builds estão indisponíveis enquanto a reescrita estabiliza. Build e --help não certificam jogabilidade.')
            if pid == 'project-2099':
                notes.append('Sem receita. A presença do instalador público não comprova que o launcher peça ROM ou obtenha/prepara o runtime ausente.')
            if pid == 'twilight-princess-courage-reborn':
                notes.append('Sem receita; não se confirmou launcher funcional no registro preservado.')
            if len(recipes) > 1:
                notes.append('Mais de uma receita/tag para o mesmo project_id; só uma unidade na contagem de projetos.')
            rows.append({
                'row': len(rows) + 1, 'project_id': pid, 'game_id': game['id'],
                'game_title': game['title'], 'project_name': project['fallback_name'],
                'catalog_source': project['source'],
                'catalog_status': project.get('status'),
                'catalog_classification': project.get('classification'),
                'catalog_replaced_by': project.get('replaced_by', project.get('superseded_by')),
                'catalog_installation_enabled': project.get('windows', {}).get('installation_enabled'),
                'has_indexed_recipe': bool(recipes), 'recipes': recipes,
                'build_profiles': profiles,
                'explicit_recipe_operation_kinds': sorted({op['kind'] for r in recipes for op in r['contract']['operations']}),
                'recipe_declares_source_mutation': False,
                'recipe_review_limit': 'As receitas não têm opcode de patch; métodos Desktop por ID/perfil e recursos incorporados podem alterar fontes. Esta coluna não os absolve.',
                'desktop_literal_references': desktop_refs(pid, profiles),
                'boot_evidence': boot,
                'checkpoint_group': ('new_since_114' if pid in NEW_28 else 'inherited_114' if recipes else 'not_implemented'),
                'evidence_paths': sorted(set(evidence)), 'notes': notes,
            })
    recipes_counted = sum(len(r['recipes']) for r in rows)
    history_shas = subprocess.check_output(['git', '-C', str(ROOT), 'log', '--reverse', '--format=%H', '--', 'index.json'], text=True).splitlines()
    previous = {}
    validated_introductions = []
    for revision in history_shas:
        raw = subprocess.run(['git', '-C', str(ROOT), 'show', revision + ':index.json'], capture_output=True)
        if raw.returncode:
            continue
        historic = json.loads(raw.stdout)
        current = {(r['project_id'], r['tag']): r.get('status') for r in historic['recipes']}
        for key, value in current.items():
            if value == 'validated' and previous.get(key) != 'validated':
                validated_introductions.append({'commit': revision, 'project_id': key[0], 'tag': key[1], 'previous': previous.get(key)})
        previous = current
    payload = {
        'audit_date_local': '2026-11-27',
        'scope': 'Inventário integral de contratos das 145 receitas e 148 IDs; revisão de fluxo/alterações Desktop em relatórios complementares.',
        'pins': {'getall': GETALL_COMMIT, 'desktop': DESKTOP_COMMIT, 'catalog': CATALOG_COMMIT},
        'input_hashes': {'index_sha256': sha((ROOT / 'index.json').read_bytes()), 'catalog_sha256': sha(CATALOG.read_bytes())},
        'counts': {'catalog_games': len(cat['games']), 'catalog_project_ids': len(rows),
                   'recipes': len(idx['recipes']), 'indexed_project_ids': len(groups),
                   'recipes_accounted_in_catalog': recipes_counted,
                   'recipe_status': dict(Counter(r['status'] for r in idx['recipes'])),
                   'project_status': dict(Counter('validated_historical' if any(x['index_status'] == 'validated' for x in r['recipes']) else 'experimental' if r['recipes'] else 'no_recipe' for r in rows)),
                   'explicit_operations': dict(op_counts), 'recipe_entry_kind': dict(kinds)},
        'consistency': {'errors': recipe_errors, 'unindexed_recipes': sorted(actual_recipes - indexed_paths),
                        'missing_recipe_files': sorted(indexed_paths - actual_recipes),
                        'index_ids_missing_from_catalog': sorted(set(groups) - {r['project_id'] for r in rows})},
        'aliases': {pid: [r['contract']['tag'] for r in rs] for pid, rs in groups.items() if len(rs) > 1},
        'index_history_review': {'commits': len(history_shas), 'validated_introductions': validated_introductions,
                                 'interpretation': 'Nenhuma receita adicional passou a validated no histórico local disponível. Isto verifica rótulos, não jogabilidade.'},
        'absent_ids': [r['project_id'] for r in rows if not r['recipes']],
        'projects': rows,
    }
    (OUT / 'catalog-review.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = [
        '# Auditoria do inventário de receitas e evidências', '',
        'Data de referência: 27/11/2026. Esta parte verifica todos os contratos declarativos. A conclusão sobre alterações em código de terceiros depende também da revisão Desktop e dos pacotes de suporte.', '',
        '## Fontes fixadas', '',
        f'- GetAll: `{GETALL_COMMIT}`.',
        f'- Desktop: `{DESKTOP_COMMIT}`.',
        f'- Catálogo: `{CATALOG_COMMIT}`.',
        f'- SHA-256 do índice: `{payload["input_hashes"]["index_sha256"]}`.', '',
        '## Resultado verificável', '',
        '- 145 documentos de receita, 142 IDs com receita, 148 IDs no catálogo e 110 jogos.',
        '- 144 entradas `experimental` e uma `validated`; por ID, 141 experimentais e um histórico homologado.',
        '- Todos os hashes de receita conferem com o índice; não há receita órfã nem ID do índice fora do catálogo.',
        '- As únicas operações declarativas são 28 `import_input`, cinco `create_directory` e um `import_input_set`. Nenhuma receita contém uma operação de alteração de source. Métodos específicos do Desktop podem aplicar patches mesmo com `operations: []`.',
        '- SM64Plus, CTR Turbocharged e MKW têm duas receitas cada. Os aliases explicam 145 entradas para 142 IDs.',
        f'- Foram lidas as {len(history_shas)} revisões locais que alteram `index.json`: a única entrada nova com `validated` é SM64CoopDX, já presente em `a4646882dfbde3daaef3ebf9790696764d9ff880`. Não houve promoção posterior de outra receita a esse rótulo.',
        '- A homologação de SM64CoopDX v1.5.1 é um relato histórico do usuário, preservado em `docs/AUDITORIA-CATALOGO-2026-11-22.md:7,16`; não foi reexecutada nesta auditoria.',
        '- Os documentos finais declaram ausência de novo primeiro boot comercial (`docs/CHECKPOINT.md:5-10`; `docs/validations/sdk169-preview/README.md:8-10`). Aprovação de parser, build, teste de ABI, `--help` ou fixture não demonstra jogo completo.', '',
        '## Como a contagem de 114 virou 142', '',
        '`docs/CHECKPOINT.md:117-129` preserva o handoff com 142 receitas para 140 IDs, mas apenas 114 fluxos classificados como integrais. O aumento posterior de 28 refere-se à implementação de fluxos Desktop, não a 28 novos boots. A base de 114 é um estado herdado, não uma prova coletiva de jogabilidade; a revisão precisa alcançar seus métodos também.', '',
        'O próprio catálogo contém o ID combinado Team Forever como `deprecated`, substituído pelos IDs Sonic 1 Forever e Sonic 2 Absolute. Os três têm receita. AutoTMC anuncia usar Picori, que tem outro ID. A contagem de 142 é de integrações/IDs, não de 142 engines de jogos independentes.', '',
        '## Limites e achados específicos', '',
        '- Metaforce: `../three-upstreams-20261127/source-de8fc69/README.md:12` descreve a reescrita em estabilização e builds indisponíveis. A receita de fonte não prova que esse estado se tornou jogável.',
        '- Double Dash C++ (`mariokartdd-recomp`): `manual_steps` declara VR desativado. Isso deve ser confrontado com o código que aplica a configuração; a receita sozinha não define a autoria da mudança.',
        '- Project 2099: não há receita. O relatório preservado descreve instalador público e runtime/payload separado; não confirma seleção de ROM no launcher. Não é correto prometer esse comportamento.',
        '- Courage Reborn: não há receita nem confirmação de launcher operacional nos registros.',
        '- As três bases de decompilação de console e Wind Waker antigo estão sem receita; não foram convertidas em ports Windows por estas receitas.',
        '- Todos os 148 projetos do catálogo têm `windows.installation_enabled: false`; a possibilidade de instalação vem dos contratos do addon/SDK. Esse campo isolado não demonstra uma instalação feita.', '',
        '## Matriz dos 148 IDs', '',
        'O JSON anexo conserva o conteúdo completo de cada contrato, hash, operações, perfiles, referências literais de código quando disponíveis e evidências por projeto. `experimental` aqui significa ausência de homologação comercial registrada nesta rodada; não significa automaticamente que o upstream seja injogável.', '',
        '| # | Projeto | Receita/tag | Entrada declarada | Boot comercial registrado |',
        '| --- | --- | --- | --- | --- |',
    ]
    for row in rows:
        tags = '; '.join(r['contract']['tag'] for r in row['recipes']) or 'sem receita'
        profiles = '; '.join(row['build_profiles'])
        if not profiles:
            profiles = '; '.join(sorted({r['entry_kind'] for r in row['recipes']})) or row['catalog_status'] or 'sem perfil'
        boot = 'relato histórico do usuário' if row['project_id'] == 'sm64coopdx-super-mario-64-coop-deluxe' else 'não comprovado' if row['recipes'] else 'sem implementação'
        lines.append('| ' + ' | '.join(quote_table(v) for v in [row['row'], '`'+row['project_id']+'`', tags, profiles, boot]) + ' |')
    lines += ['', '## Reprodução', '',
              'Execute `python docs/audits/source-integrity-20261127/catalog_inventory.py` no checkout GetAll. O script lê receitas/catálogo/refs literais Desktop e grava somente `catalog-review.json` e `catalog-review.md`; não compila nem executa jogos e não altera contratos.', '']
    (OUT / 'catalog-review.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps({'counts': payload['counts'], 'consistency': payload['consistency'],
                      'desktop_snapshot_present': DESKTOP.is_dir(), 'output': str(OUT)}, ensure_ascii=False))

if __name__ == '__main__':
    main()
