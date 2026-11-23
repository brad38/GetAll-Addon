# Automação de CI e Monitoramento Upstream — GetAll-Addon

Este documento descreve os dois workflows de automação configurados no repositório, seus scripts locais e as garantias de segurança adotadas.

## 1. Validação automática em Pull Requests (`validate-recipes.yml`)

- **Arquivo do workflow:** `.github/workflows/validate-recipes.yml`
- **Script:** `scripts/validate_recipes.py`
- **Testes:** `tests/test_validate_recipes.py`
- **Gatilhos:** `pull_request` para `main`, `push` na `main` e `workflow_dispatch`.
- **Permissões no GitHub Actions:** `contents: read` (somente leitura).

### O que é verificado

1. Codificação UTF-8 sem BOM e finais de linha `LF` estritos em `index.json` e em todas as receitas (`recipes/**/*.json`).
2. Validação formal por **JSON Schema Draft 2020-12** (`jsonschema`) contra os contratos de `schemas/`:
   - `remote-recipe-index-v1.schema.json`
   - `installation-recipe-v1.schema.json` até `installation-recipe-v4.schema.json`
3. Correspondência exata de **SHA-256** entre `index.json` e os bytes UTF-8 publicados de cada receita.
4. Unicidade de `(project_id, tag)` e `path`, além da ausência de arquivos JSON órfãos em `recipes/`.
5. Consistência de `schema_version`, `project_id`, `tag`, `source_url`, `has_inputs` e `has_manual_steps`.
6. Segurança de caminhos do **SDK 1.2.0** (sem `..`, barras invertidas `\`, caminhos absolutos, espaços ou nomes reservados do Windows, com suporte ao `+` no interior de segmentos).
7. Integridade semântica de `operations` (`copy`, `move`, `copy_input`, `import_input`, `import_input_set`), `inputs` e `first_run_files`.
8. Conferência cruzada de `game_id`, `project_id` e `repository` com o catálogo oficial `brad38/AllFix-Repo`.

### Execução local

```bash
python scripts/validate_recipes.py --check-git-blobs --check-catalog
python -m unittest discover -s tests -v
```

## 2. Monitoramento diário (`upstream-watch.yml`)

- **Arquivo do workflow:** `.github/workflows/upstream-watch.yml`
- **Script:** `scripts/upstream_watch.py`
- **Testes:** `tests/test_upstream_watch.py`
- **Gatilhos:** agendamento diário (`cron: "0 9 * * *"`, 09:00 UTC / 06:00 BRT) e execução manual (`workflow_dispatch`).
- **Permissões no GitHub Actions:** `contents: write` e `pull-requests: write` (mínimo necessário para criar a branch `automation/upstream-watch` e abrir o Pull Request).

### Como funciona

1. Consulta `catalog.json` no repositório oficial `brad38/AllFix-Repo` e compara com a matriz auditada em `docs/AUDITORIA-CATALOGO-2026-11-22.md` e `docs/RODADA-B-2026-11-23.md`.
2. Consulta a API oficial de Releases do GitHub para os repositórios mapeados (respeitando `GITHUB_TOKEN` sem expor credenciais e tratando projetos `D` já documentados com repositório 404).
3. Quando encontra uma nova release estável:
   - Baixa o `.zip` oficial Windows em pasta temporária (limite de 250 MiB), calcula seu **SHA-256 real** e lê **somente o diretório central do ZIP** (`zipfile.ZipFile.infolist()`), **nunca extraindo ou executando binários**.
   - **Receitas `validated` ou com `inputs`/`operations`:** nunca são modificadas nem promovidas automaticamente; a nova release é registrada como pendência técnica no relatório para teste funcional manual.
   - **Receitas `experimental` com `manual_steps` (`operations: []`, `inputs: []`):** apenas se todos os `required_files` e `launch_file` forem localizados no ZIP e passarem na gramática de caminhos do SDK 1.2.0, uma nova receita `experimental` é gerada em novo arquivo preservando todas as entradas anteriores em `index.json`.
   - **Qualquer incompatibilidade (espaços no nome do executável, arquivo ausente, ausência de ZIP Windows):** nenhuma receita inválida é criada; o bloqueio técnico é registrado em `docs/MONITORAMENTO-UPSTREAM.md`.
4. Antes de publicar qualquer commit, executa `validate_recipes.py` e toda a suíte `unittest`.
5. Se não houver novidades acionáveis, ou se o mesmo `fingerprint` de novidades já constar em `docs/MONITORAMENTO-UPSTREAM.md` ou em um PR aberto da branch `automation/upstream-watch`, nenhuma alteração nem Pull Request duplicado é criado.
6. Não executa merge automático: todos os PRs ficam aguardando revisão humana.

### Permissão necessária no GitHub para criação automática de PRs

Para que o GitHub Actions consiga abrir o Pull Request na execução diária, verifique no repositório `brad38/GetAll-Addon`:

1. **Settings → Actions → General → Workflow permissions**.
2. Marque **"Allow GitHub Actions to create and approve pull requests"** e salve.

*(A permissão padrão de workflow do repositório pode permanecer restrita em leitura, pois o `upstream-watch.yml` declara explicitamente `contents: write` e `pull-requests: write` apenas no próprio workflow.)*
