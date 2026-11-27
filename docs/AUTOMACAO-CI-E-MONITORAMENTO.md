# Automação de CI e Monitoramento Upstream — GetAll-Addon

Este documento descreve os dois workflows de automação configurados no repositório, seus scripts locais e as garantias de segurança adotadas.

## 1. Validação automática em Pull Requests (`validate-recipes.yml`)

- **Arquivo do workflow:** `.github/workflows/validate-recipes.yml`
- **Scripts:** `scripts/validate_ci.py` seleciona o catálogo e aplica a barreira de publicação; `scripts/validate_recipes.py` valida os documentos.
- **Testes:** `tests/test_ci_validation.py`, `tests/test_validate_recipes.py` e a suíte completa de `tests/`.
- **Gatilhos:** `pull_request`, `push` em `main` e `feat/marathon-xbox-media-import`, e `workflow_dispatch`.
- **Permissões no GitHub Actions:** `contents: read` (somente leitura).

### O que é verificado

1. Codificação UTF-8 sem BOM e finais de linha `LF` estritos em `index.json` e em todas as receitas (`recipes/**/*.json`).
2. Validação formal por **JSON Schema Draft 2020-12** (`jsonschema`) contra os contratos de `schemas/`:
   - `remote-recipe-index-v1.schema.json`
   - `installation-recipe-v1.schema.json` até `installation-recipe-v9.schema.json`
3. Correspondência exata de **SHA-256** entre `index.json` e os bytes UTF-8 publicados de cada receita.
4. Unicidade de `(project_id, tag)` e `path`, além da ausência de arquivos JSON órfãos em `recipes/`.
5. Consistência de `schema_version`, `project_id`, `tag`, `source_url`, `has_inputs` e `has_manual_steps`.
6. Segurança de caminhos conforme a versão do contrato, incluindo rejeição de traversal, barras invertidas, caminhos absolutos e nomes reservados do Windows. O schema v5 e posteriores permitem os caracteres adicionais documentados; as versões anteriores mantêm sua gramática.
7. Integridade semântica de `operations` (`copy`, `move`, `copy_input`, `import_input`, `import_input_set`), `inputs` e `first_run_files`.
8. Conferência cruzada de `game_id`, `project_id` e `repository` com o catálogo oficial `brad38/AllFix-Repo`.

O canal do índice determina o catálogo: `preview` usa o commit fixado
`3f4603cf42ef43402b4a0a9470232e7d4fcd9eb9` (148 projetos), enquanto `public`
ou um índice legado sem `channel` usa `main`. Assim, PRs de novas branches para
desenvolvimento e execuções manuais usam as mesmas identidades. Pushes e
execuções manuais de `main`, além de todos os PRs destinados a `main`, exigem
canal público, independentemente da branch de origem. Um índice de prévia é
rejeitado antes da chamada ao validador.

### Execução local

```bash
python scripts/validate_ci.py
python -m unittest discover -s tests -v
```

Para conferir um catálogo local explicitamente:

```bash
python scripts/validate_recipes.py --strict-lf --require-jsonschema --check-git-blobs --check-catalog ../allfix-repo/catalog.json
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
   - **Projetos com alguma receita `validated`, `disabled`, `draft`, de contrato diferente de v3 ou com `inputs`/`operations`:** a nova release é registrada para revisão antes de baixar o pacote, independentemente da ordem das versões no índice. A atualização automática não pode reativar receitas nem remover dependências, assets, launchers Java ou perfis de preparação/compilação ao converter um contrato mais recente em v3.
   - **Receitas v3 `experimental` com `manual_steps` explícitos (`operations: []`, `inputs: []`):** apenas se todos os `required_files` e `launch_file` forem localizados no ZIP e passarem na gramática de caminhos do SDK 1.2.0, uma nova receita `experimental` é gerada em novo arquivo preservando todas as entradas anteriores em `index.json`.
   - **Qualquer incompatibilidade (espaços no nome do executável, arquivo ausente, ausência de ZIP Windows):** nenhuma receita inválida é criada; o bloqueio técnico é registrado em `docs/MONITORAMENTO-UPSTREAM.md`.
4. Antes de publicar qualquer commit, executa `validate_recipes.py` e toda a suíte `unittest`.
5. Se não houver novidades acionáveis, ou se o mesmo `fingerprint` de novidades já constar em `docs/MONITORAMENTO-UPSTREAM.md` ou em um PR aberto da branch `automation/upstream-watch`, nenhuma alteração nem Pull Request duplicado é criado.
6. Não executa merge automático: todos os PRs ficam aguardando revisão humana.

### Permissão necessária no GitHub para criação automática de PRs

Para que o GitHub Actions consiga abrir o Pull Request na execução diária, verifique no repositório `brad38/GetAll-Addon`:

1. **Settings → Actions → General → Workflow permissions**.
2. Marque **"Allow GitHub Actions to create and approve pull requests"** e salve.

*(A permissão padrão de workflow do repositório pode permanecer restrita em leitura, pois o `upstream-watch.yml` declara explicitamente `contents: write` e `pull-requests: write` apenas no próprio workflow.)*

## 3. Prévia e contagem de cobertura

`scripts/package_preview.py` exige SHAs completos para receitas e catálogo.
As versões do complemento e de `--min-sdk` seguem o schema do manifesto:
três componentes numéricos, sem zeros iniciais em componentes de mais de um
dígito. Entradas inválidas são rejeitadas antes de ler o commit ou criar o ZIP.
O SDK mínimo padrão permanece `1.5.11`; isso não substitui os requisitos
individuais dos perfis de instalação do Desktop.

`scripts/catalog_coverage.py` conta projetos com pelo menos uma receita
`experimental` ou `validated`. Um projeto contendo somente `disabled` ou
`draft` permanece em `missing`. As listas `main` e `development` preservam
todas as versões; os booleanos `main_covered` e `development_covered` de cada
linha indicam a existência de receita utilizável. Várias versões do mesmo
projeto não aumentam a cobertura. A métrica legada `preparation_only` indica
apenas que todas as receitas utilizáveis daquele projeto são v9; não mede
instalação integral, registro, lançamento ou primeiro boot.
