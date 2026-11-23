# Checkpoint — GetAll-Addon Rodada 11B, SDK 1.4.1 (2026-11-23)

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
