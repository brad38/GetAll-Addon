# Checkpoint de Manutenção — GetAll-Addon (2026-11-23 · Rodada 8 / SDK 1.3.0)

## 1. Estado das Branches e Pull Requests

| PR | Branch origem (`head`) | Base (`base`) | Estado | Escopo principal |
|---:|---|---|---|---|
| **#1** | `feat/github-actions-automation` | `main` | `merged` | Workflows CI e monitoramento diário |
| **#2** | `feat/round-1-sdk12-recipes` | `main` | `merged` | Evolução SDK 1.2.0 e receitas iniciais |
| **#3** | `feat/round-2-n64-recipes` | `main` | `merged` | Receitas N64 Recompiled |
| **#4** | `feat/round-3-classic-ports-recipes` | `main` | `merged` | Ports clássicos |
| **#5** | `feat/round-4-full-catalog-coverage` | `main` | `merged` | Cobertura completa SDK 1.2.0 |
| **#6** | `feat/round-6-functional-homologation` | `main` | `merged` | Testes no motor `AllFix.dll`, cobertura e specs Codex (`76` receitas) |
| **#7** | `feat/round-7-sdk13-v5-recipes` | `main` | **merged** (47d8e45f2e80b17b98c80864b6d485c8962f4f5b) | Integração **SDK 1.3.0** (`schemas` v5, validador e **14 novas receitas `v5`**) |
| **#8 (proposta)** | `feat/round-8-sdk13-perfect-dark` | `main` | **Aguardando PR/revisão (sem merge)** | Migração Perfect Dark, Automobili Lamborghini e CTR Native para importação automática verificada v5 |

**Regra de integração:** PR #7 já foi mesclado na main. A Rodada 8 prepara uma branch e um novo PR; não realizar merge sem aprovação do proprietário.

## 2. Estado Real da Cobertura (119 projetos / 87 jogos)

- **Homologada (`validated`) com boot real comprovado:** `1` (`sm64coopdx-super-mario-64-coop-deluxe` `v1.5.1`)
- **Receitas `experimental` no `index.json`:** `89` (as 89 publicadas na main após o PR #7; na proposta da Rodada 8: **72 v3 experimentais + 17 v5 experimentais**, mais 1 v3 validated; **90 / 119** indexadas)
- **Instalação testada no motor oficial `AllFix.dll` 1.3.0 (`GameInstallationService.Run` sobre pacotes oficiais reais):**
  - `89 / 89` receitas experimentais verificadas (`75 / 75` v3 da Rodada 6 + `14 / 14` v5 novas na Rodada 7; nenhum erro de infraestrutura; verificações de mídia pendentes).
  - Entre as **14 novas receitas `v5`**:
    - `13 / 13` (`inputs: []`, incluindo `extremegrecomp` baixado do GitLab Package Registry, `symphonyrecomp` com `prerequisites: ["dotnet-desktop-10-x64", "openal-x64"]` + `disc/`, `redriver2` com `prerequisites: ["java-21"]`, `wipeout-phantom-edition` com `wipeout/diskimages/`) concluíram em `Status=PartiallyCompleted` com `100%` dos `required_files` e `launch_file` no disco.
    - `1 / 1` (`vandalhearts-pcport`, com `create_directory: "game"` e `import_input` `min_size + max_size + magic_hex`) avançou até a etapa de dependência obrigatória (`Status=Failed`, `"A dependência obrigatória não foi selecionada."`) com `4/4` `required_files` e `launch_file` conferidos no ZIP oficial.
- **Inicialização real comprovada nesta rodada:** `0` novas além da receita já homologada (`sm64coopdx`), pois nenhuma ROM/ISO comercial proprietária existe no ambiente.
- **Receita ausente / Bloqueio técnico comprovado:** `29` (reavaliados na Rodada 7 após os 14 desbloqueios pelo SDK 1.3.0: `4` executáveis/instaladores sem `.zip` portátil, `1` launcher apenas `.bat`/Java em `severed-chains`, `17` kits/repositórios apenas de compilação local sem executável pré-compilado do jogo e `7` casos exclusivos de origem/metadados no `AllFix-Repo`).

## 3. Artefatos Criados/Atualizados na Rodada 7 (SDK 1.3.0)

- Schemas SDK 1.3.0 sincronizados em `schemas/` (`installation-recipe-v1.schema.json`, `installation-recipe-v5.schema.json`, `remote-recipe-index-v1.schema.json`, `addon-manifest-v1.schema.json`, `addon-responses-v1.schema.json`), preservando `v2`–`v4`.
- [scripts/validate_recipes.py](../scripts/validate_recipes.py), [scripts/upstream_watch.py](../scripts/upstream_watch.py) e [tests/test_validate_recipes.py](../tests/test_validate_recipes.py) atualizados para contratos `v5`, caminhos com espaços/`()`/`+`, `local_app_data`, `prerequisites`, `sha1`/`md5`/`min_size` e `gitlab:`.
- `14` novas receitas `v5` (`recipes/.../*.json`), entradas no `index.json` (`90` totais) e registros em `docs/validations/*.md`.
- Atualização de [AGENTS.md](../AGENTS.md), [docs/COBERTURA-CATALOGO.md](COBERTURA-CATALOGO.md), [docs/HOMOLOGACAO-MIDIA-NECESSARIA.md](HOMOLOGACAO-MIDIA-NECESSARIA.md) e [docs/ESPECIFICACAO-CODEX-SDK.md](ESPECIFICACAO-CODEX-SDK.md).

## 4. Próximos Passos Exatos

1. **Revisar o PR da Rodada 8** (`feat/round-8-sdk13-perfect-dark` → `main`); o PR #7 foi mesclado anteriormente. Não mesclar automaticamente.
2. **Homologação real (`experimental` → `validated`):** executar instalação e boot real no `AllFix.exe` fornecendo as mídias originais descritas em [HOMOLOGACAO-MIDIA-NECESSARIA.md](HOMOLOGACAO-MIDIA-NECESSARIA.md), começando pelos **6 alvos de importação automática na proposta (`Prioridade 1`)** (os 3 já publicados e as migrações `perfect-dark-pc-port-perfect-dark`, `automobililamborghini-recomp` e `ctr-native`), e depois validar em ambiente real com mídias/runtimes `vandalhearts-pcport` (`Prioridade 2`), `symphonyrecomp` (`.NET 10` + `OpenAL` + multi-track), `wipeout-phantom-edition` e `redriver2` (`Java 21`).
3. **Encaminhar ao Codex** os itens pendentes documentados em [ESPECIFICACAO-CODEX-SDK.md](ESPECIFICACAO-CODEX-SDK.md) (suporte a `.sfc`/`.smc`/`.gba` no destino de `import_input`, executáveis avulsos/instaladores/multi-parte, launchers `.bat`/Java sem `.exe`, e `profile_folder` multinível em `first_run_files`).


## 5. Rodada 8 — trabalho efetivo e checkpoint

- **Base exata da main antes das alterações:** 47d8e45f2e80b17b98c80864b6d485c8962f4f5b. PRs #1–#7 já merged.
- **Projetos sem receita reavaliados:** 29 (26 repositórios GitHub, 3 fontes externas/do catálogo). Ainda sem receita v5 compatível e segura; dependências no relatório [Rodada 8](RODADA-8-SDK13-2026-11-23.md).
- **Receitas melhoradas, mas não homologadas:** Perfect Dark PC Port ci-dev-build com MD5, 33554432 bytes, magic 80371240 e import_input para data/pd.ntsc-final.z64; Automobili Lamborghini v0.11.1 com SHA-256 da ROM USA, 4194304 bytes, magic 80371240, import_input para nome canônico ao lado do EXE. As três v3 → v5, permanecem experimental e dependem de ROM própria legítima.
- - **CTR Native beta-7.1:** o README oficial carrega assets/ctr-u.bin e o perfil metadata/retail/ntsc-u-926/matching.json fixa tamanho 605698800 bytes e SHA-256 f780bf2331476aabfc00772fa758b12dd95ebfbc907968132cbd3cdd4e2c07c0 (ver nota abaixo).
- **Arquivos oficiais:** ZIPs dessas três releases rebaixados e inspecionados estaticamente, hashes conferidos com registros da Rodada 6; ROMs não fornecidas.
- **Testes concluídos:** validação integral das 90 receitas pelo schema, hashes e catálogo; suite de 16 testes unitários; parser real da AllFix.dll 1.3.0 aceitou as 90 receitas; harness independente verificou 31 assertivas com entradas artificiais, incluindo rejeição de MD5/SHA-256 adulterados.
- **Sem boot real novo / sem mudança de validated:** uma validada; 89 experimentais; cobertura continua 90/119.
- **Pendências de SDK/catálogo:** suporte seguro a instaladores .exe e downloads multipartes, launchers JAR/JRE, build auditado, extensões adicionais import_input, verificadores de perfis multinível, .tar.gz para projeto 999sian/tmc após ajuste de identidade do catálogo.
- **Próximas ações:** revisão do PR #8 e merge somente mediante autorização; teste funcional das três mídias legítimas e outras prioritárias; Codex tratar contratos pendentes independentemente.
