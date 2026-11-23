# GetAll-Addon — Rodada 12 (2026-11-23): Project Picori e auditoria de bloqueios

## Estado e escopo

Base remota confirmada: `main` commit `dd820c008034a8e7598da5fb80ab17ca5951e81b` (PR #11 integrado). Total fixo de **87 jogos e 119 projetos**. Main: **92 receitas** (70 v3, 17 v5, 1 v6, 3 v7, 1 v8; uma `validated`, 91 `experimental`), **27 sem receita**. Proposta deste PR: **93 receitas**, **26 sem receita**, 70 v3 + 17 v5 + 1 v6 + 4 v7 + 1 v8; uma `validated` e 92 `experimental`. Nenhuma destas mudancas esta na main sem merge autorizado.

- Fonte atualizada do catálogo em branch/PR independente: [AllFix-Repo PR #1](https://github.com/brad38/AllFix-Repo/pull/1).
- Branch GetAll: `feat/round-12-picori-sdk141`.
- Aplicativo Windows/SDK: código-fonte principal somente local `C:\Users\bradg\Downloads\AllFixDesktop`; preservado, sem commit, instalacao ou release.
- Nenhuma ROM comercial, instalador desconhecido, script de build remoto ou jogo foi executado.

## Projeto desbloqueado: Project Picori

Fonte oficial: [999sian/tmc](https://github.com/999sian/tmc), README do branch `master` e [release v0.9.6](https://github.com/999sian/tmc/releases/tag/v0.9.6). A origem anterior no catalogo apontava incorretamente para o perfil `999sian`, nao para o repositorio. O PR de catalogo corrige o vinculo sem trocar IDs ou habilitar instalacao prematuramente.

**Asset** `tmc-multi-windows-x86_64-v0.9.6.tar.gz` de **26.500.874 bytes**, SHA-256 `5e30fc0068b827a5fe526f744438ec729c297d9315b1c4254d8db79ba7197498`, verificado no GitHub release e calculado novamente sobre o download. Conteudo TAR.GZ inspecionado, exatamente tres arquivos normais:

- `tmc_pc.exe` — 84.739.908 bytes.
- `voxel_shapes.json` — 13.328 bytes.
- `assets/rando/default.logic` — 509.321 bytes.

O README exige ROM original legitima e descreve selecao por SHA-1. A receita `recipes/the-legend-of-zelda-the-minish-cap/project-picori-999sian-tmc/v0.9.6.json` usa schema **v7 existente**, importa exclusivamente ROM USA `baserom.gba` SHA-1 `b4bd50e4131b027c334547b4524e2dbbd4227130` ao lado do executavel; usa `manual_steps` e `status=experimental`. A cadeia de download aceita `.tar.gz`; o motor implementa extracao TAR.GZ segura. Nenhum perfil novo ou comando generico e necessario. A receita esta indexada com SHA-256 `766e067433093424f974c787cc4db844826af416cf5413fa6e8566c195648618`.

**Limites:** sem ROM legitima nao houve instalacao real completa nem primeiro boot. A primeira execucao gera cache local de recursos. O README tambem aceita EU/JP, mas somente USA tem fluxo automatico declarado nesta candidata. `experimental` nao equivale a `validated`. `installation_enabled` no catalogo permanece `false`; uma promocao funcional exige homologacao independente.

## Validacoes realmente executadas

| Checagem | Resultado |
|---|---|
| JSON Schema Draft 2020-12, hashes index/receitas, caminhos, LF e catalogo proposto | **93/93 PASS**, `jsonschema=True` |
| `python -m unittest discover -s tests -v` | **35/35 PASS** (inclui novo teste Picori positivo/negativo; dois testes antigos deixaram de fixar contagem 92) |
| `dotnet build AddonSdk/AllFix.Addons.Sdk.csproj -c Debug --no-restore` | **PASS**, 0 errors/0 warnings |
| `dotnet run --project Tests/AddonInfrastructure/AddonInfrastructure.csproj -c Debug --no-restore -- --parse-getall <GetAll> <report>` | **93/93 PASS**, parser C# compilado 1.4.1 |
| `dotnet build AllFixDesktop.sln -c Debug --no-restore` | **PASS**, 0 errors/0 warnings |
| `dotnet run --project Tests/AddonInfrastructure/AddonInfrastructure.csproj -c Debug --no-restore` | **PASS** em casos sinteticos, inclusive extracao TAR.GZ, rejeicao de symlinks/traversal/duplicatas, rollback/cancelamento e importacao sem ROM comercial |

As provas de hash e parser nao demonstram homologacao funcional do Picori; testes de integridade, regressao e seguranca sao sinteticos. GitHub Actions do PR #12: workflow `Validate GetAll-Addon Recipes`, run `45265676061`, status `completed` e conclusão `success`, verificado após os commits de documentação (commit `57f948caf83afea8f5c37f94ec28abb59f666eff`).

## Matriz dos 26 projetos ainda sem receita

Os bloqueios iniciais vieram da auditoria Rodada 11B (2026-11-23). Esta rodada **reconsultou a API de releases de todos os 24 repositórios GitHub** do grupo; duas origens externas (Team Forever e Courage Reborn) foram investigadas por documentação pública. Os resultados das releases continuam compatíveis com os bloqueios registrados; nenhuma distribuição pronta e segura adicional foi comprovada. Não houve download ou execução dos binários desses 26 projetos. Prioridades são de planejamento, não garantias de desbloqueio. O projeto de origem deve ter correspondencia exata de identidade; somente instaladores autorizados/documentados, builds isolados reproduziveis e assets oficiais verificaveis poderao gerar novas receitas.

| Projeto | Origem documentada | Classe | Bloqueio documentado | Proxima acao/prioridade |
|---|---|---|---|---|
| `mega-man-legends-modernization-project` | [Drakfix/MML_Modernization-Project](https://github.com/Drakfix/MML_Modernization-Project) | Executavel/instalador avulso | v0.9.6-beta: so MML-Setup.exe (67.227.555 B), instalador | P2: perfil instalador oficial seguro e consentido |
| `project-2099` | [GenryTheFox0/Project-2099](https://github.com/GenryTheFox0/Project-2099) | Executavel/instalador avulso | v2.0.0-beta.5: Setup.exe + payload ZIP (1,36 GB) + tres partes 4K; exige multiplos assets/instalador | P2: perfil instalador oficial seguro e consentido |
| `sarecomp-sonic-adventure-recompiled` | [sonicfreak1337/SARecomp](https://github.com/sonicfreak1337/SARecomp) | Executavel/instalador avulso | v0.52.1 so AppImages; v0.52.0 tem instalador SonicAdventureRecompiled-0.52.0-Windows.exe (257.381.884 B), sem ZIP portatil | P2: perfil instalador oficial seguro e consentido |
| `doaxvb-re` | [NoRain211/doaxvb-re](https://github.com/NoRain211/doaxvb-re) | Kit de compilacao | v0.8.0: ZIP Windows do kit (109.788.899 B) requer BuildGame.cmd e toolchains; nao inclui EXE de jogo pronto | P3: binario oficial ou build isolado |
| `god-of-war-native-pc-port-gow-pc-port` | [danielalves96/gow-pc-port](https://github.com/danielalves96/gow-pc-port) | Kit de compilacao | launcher-v0.4.0: ZIP portatil do launcher, mas jogo compilado externamente (kit/install.ps1, ps2_recomp) | P3: binario oficial ou build isolado |
| `pinyon-shift` | [arcanite24/pinyon-shift](https://github.com/arcanite24/pinyon-shift) | Kit de compilacao | v0.9.5: launcher e arquivos LLVM/host-objects, exige build local a partir de ISO; nao e executavel do jogo final | P3: binario oficial ou build isolado |
| `crash-team-racing-turbocharged` | [CameronRedmore/Crash-Team-Racing-Turbocharged](https://github.com/CameronRedmore/Crash-Team-Racing-Turbocharged) | Somente codigo-fonte | Sem Releases; build e ferramentas de decompilacao | P4: nova distribuicao oficial ou reproducao isolada |
| `doldecomp-mkdd-decompilacao-base` | [doldecomp/mkdd](https://github.com/doldecomp/mkdd) | Somente codigo-fonte | Sem Releases; base decompilada nao e distribuicao portatil | P4: nova distribuicao oficial ou reproducao isolada |
| `drmario64-recomp` | [AngheloAlf/drmario64_recomp](https://github.com/AngheloAlf/drmario64_recomp) | Somente codigo-fonte | Sem Releases; recompilacao/build local do projeto base | P4: nova distribuicao oficial ou reproducao isolada |
| `mariokartdd-recomp` | [ethannicholas/mariokartdd-recomp](https://github.com/ethannicholas/mariokartdd-recomp) | Somente codigo-fonte | Sem Releases; compilacao/recompilacao e imagem original | P4: nova distribuicao oficial ou reproducao isolada |
| `mkdd-recomp` | [LeftInWalmart/MKDD-Recomp](https://github.com/LeftInWalmart/MKDD-Recomp) | Somente codigo-fonte | Sem Releases; kit de recompilacao | P4: nova distribuicao oficial ou reproducao isolada |
| `mml1-megaman-legends-decomp` | [ChrisNonyminus/mml1](https://github.com/ChrisNonyminus/mml1) | Somente codigo-fonte | Sem Releases; decompilacao original nao e port Windows pronto | P4: nova distribuicao oficial ou reproducao isolada |
| `render96ex` | [Render96/Render96ex](https://github.com/Render96/Render96ex) | Somente codigo-fonte | Nenhuma Release na API do GitHub; precisa build do codigo e dados originais | P4: nova distribuicao oficial ou reproducao isolada |
| `sm` | [snesrev/sm](https://github.com/snesrev/sm) | Somente codigo-fonte | Sem Releases; projeto de codigo-fonte e extracacao de ROM | P4: nova distribuicao oficial ou reproducao isolada |
| `sm-rewrite` | [testyourmine/sm_rewrite](https://github.com/testyourmine/sm_rewrite) | Somente codigo-fonte | Sem Releases; projeto de codigo-fonte | P4: nova distribuicao oficial ou reproducao isolada |
| `sm64ex` | [sm64pc/sm64ex](https://github.com/sm64pc/sm64ex) | Somente codigo-fonte | Sem Releases anexadas; compilacao e extracao da ROM | P4: nova distribuicao oficial ou reproducao isolada |
| `sm64rt` | [DarioSamo/sm64rt](https://github.com/DarioSamo/sm64rt) | Somente codigo-fonte | Sem Releases anexadas; build/patch de codigo dependente dos dados originais | P4: nova distribuicao oficial ou reproducao isolada |
| `strikers-wiicompiled` | [BlackAndBlue95/Strikers-WiiCompiled](https://github.com/BlackAndBlue95/Strikers-WiiCompiled) | Somente codigo-fonte | Sem Releases; fluxo usa compilacao e imagem de disco | P4: nova distribuicao oficial ou reproducao isolada |
| `tmc-decompilacao-base` | [zeldaret/tmc](https://github.com/zeldaret/tmc) | Somente codigo-fonte | Sem Releases; base decompilada de Minish Cap | P4: nova distribuicao oficial ou reproducao isolada |
| `wipeout-rewrite` | [phoboslab/wipeout-rewrite](https://github.com/phoboslab/wipeout-rewrite) | Somente codigo-fonte | Sem Releases; nao ha pacote Windows independente | P4: nova distribuicao oficial ou reproducao isolada |
| `foxhollow` | [JackPriceBurns/foxhollow](https://github.com/JackPriceBurns/foxhollow) | Origem ou release | v1.0.30 e anteriores mostram Releases sem assets Windows anexados | P2: identificar fonte oficial e release verificavel |
| `metaforce` | [AxioDL/metaforce](https://github.com/AxioDL/metaforce) | Origem ou release | AxioDL/metaforce retorna HTTP 404 no GitHub; identidade de catalogo nao utilizavel | P2: identificar fonte oficial e release verificavel |
| `sonic-1-forever-sonic-2-absolute` | [https://teamforeveronline.wixsite.com/home/sonic-1-forever](https://teamforeveronline.wixsite.com/home/sonic-1-forever) | Origem ou release | Link de distribuicao Team Forever externo sem github_repository oficial aprovado | P2: identificar fonte oficial e release verificavel |
| `strikersrecomp` | [aharonahdoot/StrikersRecomp](https://github.com/aharonahdoot/StrikersRecomp) | Origem ou release | v0.1.0 tem Release sem assets anexados | P2: identificar fonte oficial e release verificavel |
| `twilight-princess-courage-reborn` | [https://www.pcgamer.com/games/action/zelda-twilight-princess-pc-port-inches-closer-to-release-with-new-showcase-video-and-modders-have-already-added-linkle-into-the-game/](https://www.pcgamer.com/games/action/zelda-twilight-princess-pc-port-inches-closer-to-release-with-new-showcase-video-and-modders-have-already-added-linkle-into-the-game/) | Origem ou release | Catalogo fornece pagina de noticia, sem repositorio/release oficiais utilizaveis | P2: identificar fonte oficial e release verificavel |
| `wind-waker-recomp` | [elliotttate/Wind-Waker-Recomp](https://github.com/elliotttate/Wind-Waker-Recomp) | Origem ou release | elliotttate/Wind-Waker-Recomp: 0 Releases; BlueWake e outra identidade com receita propria | P2: identificar fonte oficial e release verificavel |

Soma por classe: **3** instaladores EXE, **3** kits/build, **14** sem binarios, **6** origem/release; **26** bloqueados. Nao converter para receitas `experimental` artificiais. A atualizacao do catalogo Picori e um PR separado porque `AllFix-Repo` nao pertence ao mesmo controle de versao do GetAll.

## Pesquisa complementar de fontes dos 26 bloqueios

- **24/24 origens GitHub**: listagens de releases consultadas novamente em 2026-11-23. Três instaladores continuam sem perfil confiável aprovado (MML, Project 2099, SARecomp); três kits não incluem o jogo final pronto (DOAXVB, God of War, Pinyon Shift). Os 14 repositórios classificados como somente código-fonte retornaram zero releases via API. FoxHollow v1.0.30 e StrikersRecomp v0.1.0 têm zero assets; Wind-Waker-Recomp retornou zero releases; AxioDL/metaforce retornou HTTP 404.
- **Team Forever:** além do site Wix de distribuição, foram localizados os repositórios públicos [TeamForeverDev/Sonic1Forever](https://github.com/TeamForeverDev/Sonic1Forever) e [TeamForeverDev/Sonic2Absolute](https://github.com/TeamForeverDev/Sonic2Absolute). Ambas as APIs de releases retornaram lista vazia. O ID do catálogo refere-se a dois jogos; não substituir sua origem por apenas um projeto nem executar scripts oficiais não auditados.
- **Courage Reborn:** a [documentação específica do projeto](https://docs.couragereborn.com/) descreve compilação, inclusive Docker e CMake, porém não foi comprovada release binária pública confiável com proveniência e hash. O repositório referenciado na documentação (linifadomra/Courage-Reborn) não ficou acessível via API GitHub nesta checagem. A notícia cadastrada no catálogo não demonstra distribuição instalável. Não associar Dusklight como se fosse Courage Reborn.
- **Outras distribuições:** ausência de releases GitHub não prova ausência de qualquer distribuição; nova pesquisa em fontes oficiais pode desbloquear um caso futuro. Sem binários oficiais ou isolamento adequado, manter bloqueios.

## SDK, compatibilidade e autorizacoes

**SDK 1.4.1 / schema v8 inalterados**: Picori usa v7, sem alteracoes de contrato. As 92 receitas preexistentes continuam indexadas; Severed Chains v8 permanece a mesma candidata experimental, sem receita duplicada. Nenhum launcher de terceiros foi iniciado. Nao foi alterada a versao **All-Fix Desktop 3.0.0**, nem DLL instalada, nem foi feito merge/release.

## Limpeza e artefatos

O unico workspace de trabalho desta rodada foi `%TEMP%\AllFix-Rodada12-20261123`, contendo clone GetAll, ambiente Python isolado, arquivo TAR.GZ oficial verificado, catalogo proposto e logs/testes sinteticos. O teste C# tambem criou seu proprio `%TEMP%\AllFixAddonTest-26ee5ffff3394ca398b29855a9a47c91`. **Limpeza executada e conferida:** os dois caminhos nomeados foram removidos individualmente e a verificacao final retornou `False` para ambos os testes `Test-Path`. A enumeracao previa encontrou 9 entradas na raiz da pasta de trabalho e 25 na raiz da pasta de testes sinteticos, todas produzidas nesta rodada. As evidencias essenciais, hashes, resultados e matrizes foram preservados neste relatorio e nos commits da branch. Nenhum arquivo de usuario, backup, instalacao ou diretorio de outro agente foi incluido na remocao. O diretorio principal `C:\Users\bradg\Downloads\AllFixDesktop`, seus arquivos modificados e backups de usuario devem ser preservados. Nenhum arquivo do usuario ou de outro agente foi designado para exclusao.

## Pendencias

1. Revisar CI e PRs de GetAll e catalogo; **nao fazer merge sem autorizacao**.
2. Homologar com ROM USA legitima a instalacao completa e o primeiro boot; entao avaliar eventual `validated`.
3. Reavaliar as distribuições e possiveis builds isolados dos 26 bloqueados com evidencias adicionais. Sem sandbox/proveniência aprovadas, manter bloqueios.
4. Registrar separadamente qualquer capacidade nova do SDK, sem liberar shell/instaladores arbitrarios.
