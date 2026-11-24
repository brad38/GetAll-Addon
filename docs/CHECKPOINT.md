# Rodada 15 — situação atual (2026-11-23)

**105 receitas propostas (1 validated histórico, 104 experimental); 4 apenas preparação v9.** Escopo original 101/124; catálogo atualizado por outro agente 105/146, 111 jogos. Main GetAll permanece 92. 23 IDs do escopo inicial e 18 novos ainda sem receita. [Relatório R15: evidências individuais, implementação, testes e prévia](RODADA-15-2026-11-23.md). SDK 1.5.0 / app 3.0.0. Sem merge, release ou publicação. A matriz abaixo registra o estado histórico R14, não a cobertura atual.

---

# Checkpoint atual — Rodada 14 / 124 projetos (2026-11-23)

## Estado ao encerrar a execução

- Catálogo oficial `AllFix-Repo/main`: **91 jogos / 124 projetos** (o incremento de cinco IDs foi incorporado independentemente).
- `GetAll-Addon/main` (**ainda não foi feito merge de PRs**): **92 receitas, 1 validated, 91 experimental**, 32 projetos sem receita diante do catálogo atual.
- Branch `feat/round-14-savagewind-and-124` (PR [#15](https://github.com/brad38/GetAll-Addon/pull/15), encadeada com PRs [#12](https://github.com/brad38/GetAll-Addon/pull/12) e [#14](https://github.com/brad38/GetAll-Addon/pull/14)): **96 receitas propostas, 1 validated histórico, 95 experimental, 28 sem receita**.
- R14: `savagewindrecomp` e `shadow-of-the-colossus-pc` v0.6.0-alpha.6/v0.77 — ZIPs completos oficiais Windows inspecionados com SHA-256 exato, instalados pelo motor local em estado `PartiallyCompleted` sem mídia comercial e sem execução dos binários. Os 28 bloqueios restantes constam individualmente no [relatório R14](RODADA-14-GETALL-124-2026-11-23.md) e na [matriz completa de 124 projetos](COBERTURA-CATALOGO.md).
- GitHub PRs do catálogo [#1](https://github.com/brad38/AllFix-Repo/pull/1) (Picori), [#3](https://github.com/brad38/AllFix-Repo/pull/3) (Team Forever) e [#6](https://github.com/brad38/AllFix-Repo/pull/6) (Leonida transferido) continuam em rascunho, sem merge. PRs #1 e #3 tiveram suas branches reconciliadas com o catálogo de 124, preservando histórico e IDs.
- AllFix Desktop local: versão **3.0.0**, SDK **1.4.1**, schemas v1-v8; pesquisa de jogo/port/ID/repositório com seleção do port, refresh manual `force=true`, cache offline e provedor CI restrito. Em Release e sintéticos, 96/96 parse C#, 38/38 Python, 12 casos Node e a suite C# passaram. Teste C# real da API comprovou `force=true` = remoto 124 projetos e `force=false` = cache 124 projetos.
- Executável de revisão **não publicado**: `C:\Users\bradg\Downloads\AllFixDesktop-R14-20261123\publish\AllFix.exe`, versão 3.0.0, SHA-256 `29a4acbe98c512336e7715dac6f4bfc7866a178c521522fee571fbc0d699b127`.
- ZIP de prévia: `C:\Users\bradg\Downloads\AllFixDesktop-R14-20261123\AllFix-v3.0.0-GetAll-R14-preview.zip`, SHA-256 `cf7ce39ebe1f8c28d0b365672869759ebd1df861777305c1e91c9a03abae1c87`.
- ZIP de fontes alteradas/8 backups originais: `C:\Users\bradg\Downloads\AllFixDesktop-R14-20261123\AllFixDesktop-R14-Source-and-Backups.zip`, SHA-256 `b0f7ae90d5dca6a84c7ba2c8e31282f792f5ae6ce65a028491b64ab19b679900`. Os 2 ZIPs foram abertos e verificados, inclusive hash do EXE dentro do pacote.
- Limpeza: removido somente `%TEMP%\AllFix-R14-20261123`, 11 entradas explícitas. Verificados como preservados tanto o Desktop principal quanto os backups R13/R14 e os ZIPs de publicação.
- Sem execução de ROMs/ISOs/jogos/instaladores de terceiros, sem merge, sem promoção a `validated`, sem substituir EXE instalado e sem publicar release/version.json.

## Próximas decisões legítimas

1. Revisar os PRs #1/#3/#6 do catálogo, os PRs #12/#14/#15 do GetAll, as dependências de origem, os hashes e a branch do Desktop antes de autorizar merges/publicação. A versão de aplicativo distribuída precisa do provedor CI e `store-search.js` incorporados.
2. Se houver mídia original legítima fornecida pelo usuário e autorização de testes funcionais, homologar primeiro boot e gerar evidências em `docs/validations/`. Não promover receita a `validated` só por JSON/parser/staging.
3. Acompanhar novos releases oficiais dos 28 faltantes. Para instaladores e kits de build, exigir perfil de execução local estritamente auditado e isolamento seguro; nunca executar arbitrariamente scripts/EXEs externos nem contabilizar builder como instalação funcional.
4. Verificar impacto de teclado virtual iOS/Android em dispositivos reais quando houver acesso; `VisualViewport` só foi verificado por inspeção de código.
5. Após aprovação, conferir a release e o SHA-256 exato de `version.json` e executar a implantação de acordo com a política do All-Fix.

---

## Histórico preservado — Rodada 11B


## Base e entrega

- Main confirmada em 6cded08c2742ecc19882ea2ef1938bf040753897 (PR #10 integrado).
- Branch: feat/round-11b-sdk141-severed-chains, criada a partir dessa main.
- Somente brad38/GetAll-Addon foi modificado; nenhuma DLL instalada foi substituida, nenhum aplicativo principal, SDK, catalogo ou release foi alterado. PR somente para revisao, sem merge automatico.
- Pacote de integracao GetAll-Rodada11A-SDK141-Integration.zip SHA-256 calculado **87abe60e00634749a4d3aaa5a2ce71b72e252953bf5bd43c1baa435af94cc4c4**; 41 arquivos. Contrato de SDK 1.4.1 de desenvolvimento, nao release.

## Cobertura

| Indicador | Main PR #10 | Branch Rodada 11B |
|---|---:|---:|
| Jogos / projetos | 87 / 119 | 87 / 119 |
| Receitas | 91 | **92** |
| v3 / v5 / v6 / v7 / v8 | 70 / 17 / 1 / 3 / 0 | **70 / 17 / 1 / 3 / 1** |
| validated | 1 | **1** |
| experimental | 90 | **91** |
| Projetos sem receita | 28 | **27** |
| Novos boots de jogos comerciais | 0 | **0** |

## Mudanca concreta

**Severed Chains release-3.0.0 experimental v8**, caminho recipes/the-legend-of-dragoon/severed-chains/release-3.0.0.json.
- ZIP oficial 131446655 B, SHA-256 164716cba1899cadf834506636de8da56721d695457c3b53c93c533999ef9bb4; 769 entradas.
- Classe legend.game.MainWindows, major bytecode 69 (Java25).
- 96 JARs locais em classpath exatamente conforme launch.bat oficial; 6 jvm_options da whitelist e programa perfil fechado severed-chains-3; nenhuma execucao de BAT, instalador ou shell.
- Dados originais NTSC-U para isos/ permanecem manuais. A evidencia anterior do SDK 11A registra staging PartiallyCompleted e ausencia de boot; nenhuma instalacao jogavel foi homologada.

**SDK v8:** schema oficial importado, docs e exemplo sintetico, validador Python com allowlist e verificacoes cruzadas por versao (v1-v7 preservados), testes positivos e negativos. Nao migrar outras 91 receitas.

## Testes executados

- Hash SHA-256 do pacote de integracao e ZIP original; bytecode e 96 ZIPs JAR inspecionados estaticamente.
- JSON Schema 2020-12, semantica e indices: **92/92 PASS** com checks Git blobs, LF e catalogo.
- Unit tests Python: **34/34 PASS** (25 mantidos e 9 novos).
- Parser nativo AllFix.dll SDK 1.4.1: **92/92 receitas**; harness **92/92 assertions**.
- JavaJarLauncher.ValidateClasspath: **96 JARs oficiais aceitos** e testes negativos de classe inexistente, bytecode Java25 com runtime Java21 e JAR faltante rejeitados. Nenhum jogo executado.
- GitHub Actions sera conferido no PR. Resultado funcional final com midia legitima permanece pendente.

## Bloqueios mantidos (27)

- 3 instaladores/EXEs nao portateis sem perfil aprovado.
- 3 kits dependentes de build nativo/isolamento.
- 14 bases de codigo sem release utilizavel.
- 7 problemas de fonte, origem no catalogo ou release sem assets.
- Project Picori tem tar.gz Windows oficial v0.9.6, mas seu catalogo aponta perfil GitHub, nao repo; **nao corrigir AllFix-Repo nesta rodada**.

Documentacao: [Rodada 11B](RODADA-11B-SDK141-2026-11-23.md), [Matriz 119](COBERTURA-CATALOGO.md), [validacao Severed Chains](validations/severed-chains-release-3.0.0.md), [guia de homologacao](HOMOLOGACAO-MIDIA-NECESSARIA.md), [spec Codex](ESPECIFICACAO-CODEX-SDK.md), [limpeza](LIMPEZA-RODADA-11B.md).

## Proximos passos

Revisar o PR, verificar CI e homologar Severed Chains apenas com Java25 configurado e copia legitima dos discos do usuario. Para automacao futura, solicitar ao Codex importacao/verificacao segura de midia e pos-condicoes; nenhuma hipotese de ROM hash deve ser inventada. Nao fazer merge nem publicar release.
