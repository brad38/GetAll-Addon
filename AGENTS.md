# AGENTS.md — Instruções Permanentes de Manutenção do GetAll-Addon

## 1. Missão do Projeto

Manter e expandir o **GetAll-Addon** até alcançar a maior cobertura **funcional** possível dos **119 projetos dos 87 jogos** listados no catálogo oficial `brad38/AllFix-Repo`.

- O critério de sucesso é a instalação e inicialização **funcionalmente verificadas** no All-Fix — **nunca** considere uma tarefa concluída apenas porque receitas JSON foram criadas ou bloqueios foram catalogados.
- Após concluir uma rodada ou projeto, avance automaticamente para o próximo item prioritário sem pedir autorização intermediária (pause apenas se precisar de mídia original legítima ausente no ambiente, credenciais/permissões, aprovação de merge ou decisão ambígua).
- Se a sessão atingir um limite operacional, registre o estado exato, pendências e próximos passos em [docs/CHECKPOINT.md](docs/CHECKPOINT.md).

## 2. Escopo Estrito e Restrições de Segurança

- **Repositório único de escrita:** modifique **exclusivamente** o `GetAll-Addon`.
- **Somente leitura fora deste repositório:** **nunca** altere o código-fonte ou dados do `AllFix-Repo`, do aplicativo `All-Fix` nem do `All-Fix SDK` (responsabilidades do Codex). Limitações reais do motor devem ser especificadas em [docs/ESPECIFICACAO-CODEX-SDK.md](docs/ESPECIFICACAO-CODEX-SDK.md).
- **Zero pirataria e zero execução insegura:** nunca distribua ROMs, ISOs, pacotes XBLA ou ativos comerciais; nunca execute binários baixados de releases de terceiros (utilize apenas inspeção estática via `zipfile` e o serviço oficial de instalação da `AllFix.dll` quando aplicável).
- **Proibido inventar dados:** jamais invente hashes (`sha256`, `sha1`), tamanhos em bytes, caminhos internos de ZIP ou resultados de testes. Toda receita deve refletir exatamente os arquivos e assinaturas verificados nos pacotes e repositórios oficiais.

## 3. Contratos do SDK 1.2.0 e Regras de Receitas

- Utilize apenas contratos suportados pelo All-Fix SDK 1.2.0 (`schemas/installation-recipe-v1.schema.json` a `v4.schema.json` e `schemas/remote-recipe-index-v1.schema.json`).
- Observe os contratos reais verificados na `AllFix.dll`:
  - `StoreAddonProviders.ParseRecipe` exige `sha256` ou `sha1` em toda entrada de `inputs` referenciada por `import_input` (além da regra `sha256` ou `size + magic_hex` do JSON Schema v3).
  - `IsSafeRelativePath` proíbe espaços e caracteres fora de `[a-zA-Z0-9_.+-]` nos caminhos declarados em `recipe.json` (`required_files`, `launch_file`, `operations[].target`, `inputs[].verify_file`), enquanto o extrator `GameInstallationService` extrai normalmente arquivos auxiliares não declarados do ZIP que contenham espaços.
- Todos os arquivos versionados (JSON, Markdown, Python, YAML) devem usar **UTF-8 sem BOM** e quebra de linha **`LF`** (`\n`), conforme [.gitattributes](.gitattributes).

## 4. Separação Rigorosa entre `experimental` e `validated`

- Toda nova receita nasce obrigatoriamente com `status: "experimental"` em `index.json`.
- Aprovação em JSON Schema, `scripts/validate_recipes.py`, `ParseRecipe` da `AllFix.dll` ou testes sintéticos **não** autoriza promoção a `validated`.
- Uma receita só pode ser promovida para `validated` após:
  1. Teste real de instalação pelo motor oficial do All-Fix com o pacote oficial do projeto e mídia legítima do usuário;
  2. Inicialização/boot real comprovado do jogo com os arquivos nos locais esperados;
  3. Registro objetivo das evidências em `docs/validations/<project_id>-<tag>.md`.

## 5. Controle Permanente de Cobertura (`docs/COBERTURA-CATALOGO.md`)

Mantenha [docs/COBERTURA-CATALOGO.md](docs/COBERTURA-CATALOGO.md) atualizado a cada rodada diferenciando explicitamente o estado de cada um dos **119 projetos**:

- **Receita ausente**
- **Receita criada, não integrada** (presente na branch de trabalho, ainda não incorporada em `origin/main`)
- **Experimental publicada** (presente em `origin/main` com `status: "experimental"`)
- **Instalação testada no motor** (`GameInstallationService` / `AllFix.dll` concluído sobre o pacote real)
- **Inicialização real comprovada** (boot real do jogo verificado)
- **Homologada (`validated`)**
- **Bloqueio técnico comprovado** (nunca contabilizado como instalação concluída)

## 6. Política de Branches, PRs, Validação e Reavaliação de SDK

- Crie uma branch dedicada e um Pull Request por rodada; se o PR anterior ainda estiver aberto, encadeie as branches via **`git merge --no-ff`** (nunca use `rebase`, `--force` ou exclusão/sobrescrita de receitas).
- **Nunca faça merge automático** de Pull Requests sem autorização explícita do proprietário.
- Execute sempre antes de publicar e após qualquer merge:
  - `validate_recipes.py --require-jsonschema --check-git-blobs --check-catalog`
  - `python -m unittest discover -s tests -v`
  - Verificação no parser/motor oficial `AllFix.dll` e validação no GitHub Actions (`.github/workflows/validate-recipes.yml`).
- **Reavaliação contínua de bloqueios e SDK:** sempre que uma nova versão do SDK/All-Fix for disponibilizada, reavalie imediatamente os projetos em [docs/ESPECIFICACAO-CODEX-SDK.md](docs/ESPECIFICACAO-CODEX-SDK.md) ligados às novas capacidades e converta os desbloqueados em receitas funcionais.
