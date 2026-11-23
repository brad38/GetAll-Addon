# Checkpoint de Manutenção — GetAll-Addon (2026-11-23)

## 1. Estado das Branches e Pull Requests

| PR | Branch origem (`head`) | Base (`base`) | Estado | CI (`Validate GetAll-Addon Recipes`) |
|---:|---|---|---|---|
| **#1** | `feat/github-actions-automation` | `main` | `merged` | `completed / success` |
| **#2** | `feat/round-1-sdk12-recipes` | `main` | `open` (`mergeable: true`, `clean`) | `completed / success` |
| **#3** | `feat/round-2-n64-recipes` | `feat/round-1-sdk12-recipes` | `open` (`mergeable: true`, `clean`) | `completed / success` |
| **#4** | `feat/round-3-classic-ports-recipes` | `feat/round-2-n64-recipes` | `open` (`mergeable: true`, `clean`) | `completed / success` |
| **#5** | `feat/round-4-full-catalog-coverage` | `feat/round-3-classic-ports-recipes` | `open` (`mergeable: true`, `clean`) | `completed / success` |
| **#6** | `feat/round-6-functional-homologation` | `feat/round-4-full-catalog-coverage` | `open` (em verificação nesta entrega) | Aguardando conclusão na entrega |

**Ordem obrigatória de merge (quando autorizada pelo proprietário):** `#2 → #3 → #4 → #5 → #6` (redirecionando cada base subsequente para `main` caso não seja atualizado automaticamente pelo GitHub após o merge anterior).

## 2. Estado Real da Cobertura (119 projetos / 87 jogos)

- **Homologada (`validated`) com boot real comprovado:** `1` (`sm64coopdx-super-mario-64-coop-deluxe` `v1.5.1`)
- **Receitas `experimental` no índice:** `75` (`9` idênticas em `origin/main` + `66` novas/evoluídas nos PRs #2–#6)
- **Instalação testada no motor oficial `AllFix.dll` (`GameInstallationService.Run` sobre os 75 ZIPs oficiais baixados):** **`75 / 75 PASS`**
  - `58 / 58` (`inputs: false`, `manual_steps: true`): extraídas e validadas pelo motor em `Status=PartiallyCompleted` com `100%` dos `required_files` e `launch_file` presentes em `Destination`.
  - `17 / 17` (`inputs: true`): ZIP baixado e verificado por SHA-256, `GameInstallationService.Run` avançou até a etapa de dependência obrigatória retornando `Status=Failed` com `"A dependência obrigatória não foi selecionada."` pela ausência de ROM comercial local, com `100%` dos `required_files`, `launch_file` e diretórios-pai de `import_input` verificados no pacote (incluindo comprovação empírica em `AllFix.dll` de criação automática de subpastas ausentes como `goldeneye-pc-port-0.5.0-win64/data/`).
- **Inicialização real comprovada nesta sessão:** `0` novas além da receita já homologada (`sm64coopdx`), pois nenhuma ROM/ISO comercial proprietária existe no ambiente.
- **Receita ausente / Bloqueio técnico comprovado:** `43` (todos os 43 reavaliados via API do GitHub e inspeção estática `zipfile`; nenhuma nova distribuição portátil compatível surgiu desde a última auditoria).

## 3. Artefatos Criados/Atualizados na Rodada 6

- [AGENTS.md](../AGENTS.md) e regra persistente de workspace [.agents/rules/getall-agents.md](../.agents/rules/getall-agents.md)
- [docs/COBERTURA-CATALOGO.md](COBERTURA-CATALOGO.md) atualizado com os 7 estados obrigatórios e evidências individuais dos 119 projetos
- [docs/HOMOLOGACAO-MIDIA-NECESSARIA.md](HOMOLOGACAO-MIDIA-NECESSARIA.md) listando exatamente os arquivos originais legítimos necessários para homologação ponta a ponta (`Prioridade 1` a `3`)
- [docs/ESPECIFICACAO-CODEX-SDK.md](ESPECIFICACAO-CODEX-SDK.md) com as especificações técnicas para o Codex e a separação dos 5+2 apontamentos exclusivos de origem do `AllFix-Repo`
- Atualização dos 75 arquivos em `docs/validations/*.md` com os registros reais de `GameInstallationService.Run`

## 4. Próximos Passos Exatos

1. **Autorizar e executar o merge em sequência dos PRs #2 → #3 → #4 → #5 → #6** (nenhum merge automático foi feito).
2. **Testes reais de homologação (`experimental` → `validated`):** executar instalação e boot real no `AllFix.exe` fornecendo as mídias originais descritas em [HOMOLOGACAO-MIDIA-NECESSARIA.md](HOMOLOGACAO-MIDIA-NECESSARIA.md), começando pelos **3 alvos puramente automáticos (`Prioridade 1`)**:
   - `goldeneye-007-pc-port` (`v0.5.0`)
   - `snap64-recomp` (`v1.1.8`)
   - `project-midas` (`1.0.2b`)
3. **Reavaliação contínua de SDK:** quando o Codex implementar as capacidades listadas em [ESPECIFICACAO-CODEX-SDK.md](ESPECIFICACAO-CODEX-SDK.md) (ex.: espaços em caminhos declarados, `sha1` isolado/`md5` em `inputs`, `local_app_data`, seletores PS1/XBLA LIVE, pipelines/instaladores e GitLab), reavaliar imediatamente os 43 projetos bloqueados e as 58 receitas hoje dependentes de `manual_steps`.
