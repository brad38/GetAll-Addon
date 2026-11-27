# Checkpoint do GetAll-Addon

## Continuidade SDK 1.5.67 — em execução em 27/11/2026

Branch `work/complete-install-flows-20261127`, a partir de GetAll `f0942a6`
e Desktop `c209adc`, sem merge em main. O checkpoint confirmado registra
**136/148 fluxos integrais**, vinte e dois acima de 114: sm64ex, Render96ex, sm64rt,
Strikers Wii, WipEout, Dr. Mario, Double Dash C++, Burnout 3, Strikers GC, Double Dash Rust, DOAX, GOW KIexster, Odyssey, LAS, GOW 0.4.0, TotK, DKB, GT5, RyGT, Spartan, SSX e GTA Stories. Há um
homologado histórico, 135 integrais aguardando mídia, 3 parciais, dois
adiados pelo usuário e sete sem receita. Nenhum novo primeiro boot foi
comprovado. O índice tem **143 receitas para 141 projetos**, com uma entrada
validated histórica e 142 experimentais.

Desktop `6548ce0` está na PR3 draft, com CI Windows `46041444134`
aprovado. Pinyon/FH1 seguem
em verificação.

Build22 do harness: **0 erros, 0 avisos, 1.745 checks PASS**. O parser21
aprovou **143/143 receitas** do GetAll `9caef66`. WipEout passou
pela transação Run/Resume/registro/Jogar com compilação oficial e mídia
sintética. Dr. Mario passou pela preparação nativa real, Python e geradores.
Double Dash C++ passou pelo runtime completo e execução SDL/C++20 sem Visual
Studio. Burnout passou pelo fluxo e pelos quatro testes D3D8 reais. Evidências
e limites estão em [SDK 1.5.67](validations/sdk167-flow-completion.md).

A prévia anterior, os worktrees concorrentes e as fontes de mídia foram
preservados. GetAll `9caef66` está na PR20 draft, CI `46040722683` aprovado.
A nova prévia ainda está em fechamento.
As seções abaixo são históricas e mantêm as contagens da sua data.

## Integração da continuidade com SM64Plus — 27/11/2026

Branch isolada `work/getall-integration-20261127`: combina os commits
`bb07738`/`285d258` de `feat/sm64plus-handoff` com as correções de automação
de `e41f4a3`, preservando os dois históricos. O conflito do workflow foi
resolvido mantendo o gatilho de push de SM64Plus e a seleção de catálogo
pelo canal do índice em `scripts/validate_ci.py`.

O acesso autenticado ao Desktop privado e ao Bradsson foi restabelecido.
Leitura de arquivos, terminal, .NET SDK 8.0.425 e autenticação de escrita
do Git foram verificados. As alterações locais do workspace principal e
os worktrees anteriores foram preservados. O Desktop mais recente
verificado é `75defea0b71c1f3ed2c4a86d4391cd86e2a8d0a5`, SDK **1.5.65**, na
branch `feat/sm64plus-handoff`; contém SM64Plus e o cache verificado de
codegen do Pinyon.

### Estado integrado

- **142 receitas para 140 projetos**: 141 entradas experimentais e uma
  entrada `validated` histórica. CTR Turbocharged e SM64Plus têm duas
  receitas cada; a receita anterior LauncherMirror de SM64Plus foi mantida.
- O checkpoint do handoff SM64Plus registra **114/148 fluxos integrais**,
  incluindo um homologado. A matriz da raiz ainda registrava 113 antes
  desse handoff; sua próxima atualização deve incluir o fluxo SM64Plus,
  sem inferir integralidade a partir da contagem de receitas.
- O catálogo de desenvolvimento continua com 110 jogos e 148 projetos;
  a prévia usa o pin `3f4603cf42ef43402b4a0a9470232e7d4fcd9eb9`.
- Nenhum status foi promovido por esta integração. O build positivo de
  SM64Plus com ROM original e o primeiro boot continuam pendentes.

### Validações reexecutadas na integração

- **60/60 testes Python** aprovados.
- **142/142 receitas** no validador estrito, com JSON Schema, hashes,
  blobs Git, LF e catálogo de 148 projetos.
- Helper de CI aprovado com contexto de push em `feat/sm64plus-handoff`
  e catálogo oficial fixado; a prévia foi recusada ao simular PR para
  `main`, inclusive com a antiga branch de exceção.
- **142/142 receitas aprovadas pelo parser C# no Bradsson**, usando a
  árvore `getall-sm64plus-handoff`. `git diff` confirmou que `index.json`
  e todas as receitas são idênticos à árvore integrada. Evidência:
  `evidence-r18/continuation-20261127/getall-parser.json` e `.log`.
- `git diff --check` aprovado. O CI remoto deve ser consultado pelo
  commit desta integração; o CI das bases não substitui esse resultado.

Os registros abaixo descrevem etapas anteriores e seus bloqueios na data
da execução. Os bloqueios de acesso e envio registrados na etapa inicial
foram superados nesta integração.

## SM64Plus - continuidade isolada SDK 1.5.64

Nova receita experimental build-85c3e51; 142 receitas para 140 projetos. 114/148 fluxos integrais implementados, incluindo 1 homologado; SM64Plus aguarda ROM original e primeiro boot. Evidencias e limites em docs/validations/sm64plus-build-85c3e51.md. Branch isolada feat/sm64plus-handoff; nao modifica a branch concorrente.

## Etapa inicial de 27/11/2026 — contratos e isolamento da prévia

Esta continuidade usa o GetAll em `27966be0a0e7df41ab4b45f2252b4ac2f6031863`
(`feat/marathon-xbox-media-import`) e o catálogo em
`44bdb508842407d501e420457274eb4064f5d935` (`feat/catalog-release-dates`).
As alterações desta sessão estão na branch isolada
`work/continuar-getall-20261127`. O HEAD remoto do GetAll foi conferido novamente
antes do commit e permanecia em `27966be`.

### Estado confirmado e preservado

| Indicador | Resultado observado |
|---|---:|
| Jogos no catálogo de desenvolvimento | 110 |
| Projetos por ID | 148 |
| Receitas no índice de desenvolvimento | 141 |
| Projetos com receita utilizável | 140 |
| Projetos sem receita | 8 |
| Receitas experimentais | 140 |
| Receitas com status `validated` histórico | 1 |
| Novas instalações ou primeiros boots nesta sessão | 0 |

As duas receitas de `crash-team-racing-turbocharged` explicam a diferença entre
receitas e projetos. A cobertura utilizável conta somente `experimental` e
`validated`, sem promover nenhum status. Não foi possível recontar os fluxos
integrais: os 102 integrais e 38 incompletos do handoff pertencem ao checkpoint
anterior e dependem da matriz funcional atual no Bradsson. Não somar os seis
projetos mencionados nos commits posteriores como novos integrais sem essa
evidência.

Os commits `4d1d73f`, `efda491` e `27966be`, posteriores ao handoff `acc73ca`,
atualizam instruções de mídia para The Simpsons Game, Earthworm Jim HD,
3 on 3 NHL Arcade, PGR4, Blue Dragon e Sonic Unleashed. Foram preservados.
O catálogo de datas conserva os três commits de desenvolvimento `098d847`,
`3f4603c` e `44bdb50`, ainda separados de `main`; as 109 datas de lançamento,
o `null` de Dinosaur Planet, todas as datas de inclusão e GT4 como PS2 foram
preservados. Nenhum arquivo do catálogo foi alterado nesta sessão.

### Correções implementadas

- O CI seleciona o catálogo pelo canal do índice. Novas branches de prévia e
  PRs para desenvolvimento usam o catálogo fixado de 148 projetos. Todo PR
  destinado a `main` e toda execução na `main` rejeita índice de prévia antes
  da validação, inclusive a antiga exceção `feat/round-17-restricted-installers`.
- O empacotador rejeita versões e SDK mínimo com zeros iniciais que o schema
  do próprio manifesto não aceita, antes de criar arquivos. O SDK mínimo
  padrão existente foi preservado.
- A cobertura deixa de contabilizar receitas `disabled` e `draft` como
  utilizáveis, preservando todas as versões nos detalhes e contando cada
  projeto uma única vez. O campo legado `preparation_only` não comprova fluxo
  integral, instalação ou boot.
- O monitor de releases verifica os estados e contratos de todas as versões
  de um projeto antes de propor atualização automática. Encaminha contratos
  diferentes de v3, estados protegidos e entradas com operações ou mídia para
  revisão, sem baixar seus pacotes. Isso evita remover dependências, assets,
  launchers Java ou perfis de preparação/compilação e não depende da ordem do
  índice. Uma reprodução anterior com Severed Chains v8 gerava v3 e perdia
  `java_launcher` e `prerequisites`; a regressão agora está coberta.

### Validação desta sessão

- **60 testes Python aprovados**, incluindo 14 regressões novas de CI,
  empacotamento, cobertura e monitoramento. Fixtures e ZIPs de teste são
  sintéticos; nenhum executável de terceiros foi executado.
- **141 receitas aprovadas** em `validate_recipes.py --strict-lf
  --require-jsonschema --check-git-blobs --check-catalog`, usando o catálogo
  local de 148 projetos. Schemas, identidades, hashes e LF passaram.
- O helper de CI foi executado com contexto simulado de PR para desenvolvimento
  e catálogo oficial fixado: aprovado. O contexto de PR para `main` com índice
  de prévia foi rejeitado antes do validador, conforme esperado.
- O catálogo passou em `validate_catalog.py --require-dates --compare-with
  origin/main`. `git diff --check` também passou.
- [CI remoto do commit-base 27966be](https://github.com/brad38/GetAll-Addon/actions/runs/45935930815)
  confirmado `completed/success`. Esse resultado não é CI das alterações
  locais desta sessão.

### Oito projetos sem receita e condições de desbloqueio

| Projeto | Evidência ou condição atual |
|---|---|
| `drmario64-recomp` | Fonte arquivado, sem releases; exige geração de código a partir da ROM e perfil de build. Windows não foi verificado, não é incompatibilidade absoluta. |
| `metaforce` | Índice de releases acessível, mas os diretórios `continuous/`, `dev/` e o repositório retornaram 404 nesta consulta. Falta distribuição oficial verificável. |
| `twilight-princess-courage-reborn` | Documentação oficial de build Windows disponível; o repositório nela indicado e suas releases retornaram 404. Falta fonte/pacote fixável e integração do processamento. |
| `wind-waker-recomp` | Upstream orienta migrar para BlueWake e retirou as releases próprias. Preservar o ID sucedido, sem duplicar a receita do sucessor. |
| `project-2099` | Release beta5 declara mídia própria, mas também Title Update incluído. Não foi obtida evidência que resolva o bloqueio de distribuição ou um contrato de instalador aprovado. |
| `doldecomp-mkdd-decompilacao-base` | Base de decompilação de console no catálogo; não houve evidência nova de port Windows. |
| `tmc-decompilacao-base` | Base de decompilação de console no catálogo; não houve evidência nova de port Windows. |
| `mml1-megaman-legends-decomp` | Base de decompilação de console no catálogo; não houve evidência nova de port Windows. |

Fontes oficiais consultadas nesta retomada:
[Dr. Mario 64](https://github.com/AngheloAlf/drmario64_recomp/commit/7892264252fd662c140625ad35cab62825ab473b),
[releases Metaforce](https://releases.axiodl.com/),
[build Courage Reborn](https://docs.couragereborn.com/building/build/),
[Wind Waker Recomp](https://github.com/elliotttate/Wind-Waker-Recomp) e
[metadados da release Project 2099 beta5](https://api.github.com/repos/GenryTheFox0/Project-2099/releases/tags/v2.0.0-beta.5).
Nenhuma dessas verificações desbloqueou uma nova receita funcional nesta sessão.

### Bloqueio operacional registrado antes da conexão

GetAll e catálogo foram obtidos por leitura pública. `brad38/Allfix` continua
inacessível sem autenticação; o Bradsson não está conectado. Os arquivos locais
`CONTINUIDADE.md`, `PENDENCIAS.md`, `MATRIZ-FUNCIONAL.md` e
`LIMPEZA-ARMAZENAMENTO.md` não foram acessados nem substituídos. Não houve build
Windows, execução do parser/motor C#, validação WPF ou primeiro boot.

O teste de publicação `git push --dry-run` para a branch isolada falhou por
ausência de autenticação (`unable to get password from user`). Nenhum push,
PR, merge, release, alteração de `version.json` público ou troca de instalação
foi realizado. A próxima ação é disponibilizar acesso ao Desktop atual e aos
checkpoints do Bradsson, além da autenticação de escrita no GetAll; então
conferir novamente os HEADs, integrar esta branch e continuar a fila funcional
real, sem repetir os fluxos já implementados. DownloadAll permanece fora do
escopo.

## SDK 1.5.46

- `super-metroid-launcher` v1.0.1 e `zelda-3-launcher` v1.3.7.0 compartilham um perfil TCC baseado nos comandos upstream, com fontes e dependências fixados. Para Zelda 3, o motor prepara Python e wheels verificados e valida o arquivo de recursos produzido.
- Os dois executáveis Windows x64 foram compilados no motor com os kits oficiais. Cancelamento, rejeição de ROM e planos de lançamento foram testados. O extrator Zelda recusou mídia sintética no teste. As receitas seguem experimentais até a instalação com mídia original e primeiro boot.

## SDK 1.5.45

- `gsrecomp` 0.8.4 usa os compiladores do ZIP Windows fixado para preparar Golden Sun e The Lost Age. O motor identifica o jogo e a edição por SHA-1, importa a ROM com o nome esperado, valida a biblioteca resultante com o registro oficial e grava o fingerprint da release.
- O motor abriu o seletor com o ZIP oficial, rejeitou uma ROM incompatível e preservou o kit no cancelamento. Os fingerprints foram comparados com a árvore oficial. Os registros das DLLs e o plano de lançamento foram testados com fixtures. A receita segue experimental até uma instalação com mídia original e primeiro boot.
- `battletanx-global-assault-pc-port` v0.2.5 reutiliza a importação N64 e passa a ROM validada ao executável oficial com `--play BattleTanxGA.z64`. O perfil fixa o pacote portátil e verifica os hashes SHA-1 e SHA-256 da edição americana revisão 0. Este perfil é distinto de `btgarecomp` e aguarda teste com ROM original e primeiro boot.

## SDK 1.5.44

- `open-nectar` 1.3 aceita as quatro edições auditadas de Pikmin e Pikmin 2. O motor verifica o digest original e extrai os dados em staging com o leitor GameCube compilado a partir do fonte oficial. Um disco abre o executável correspondente. Uma pasta com os dois discos prepara os dois jogos e abre o seletor oficial.
- O kit oficial e seleção/cancelamento foram testados no motor. O registro de recursos e os planos de lançamento individual e combinado foram verificados com arquivos sintéticos. A receita segue experimental. Extração com mídia original e primeiro boot aguardam homologação.

## SDK 1.5.43

- `project-picori-999sian-tmc` v0.9.6 usa o extrator nativo integrado ao Desktop para gerar PAKs regionais a partir da ROM original dos EUA, Europa ou Japão. Builds sem o extrator preservam a importação da ROM americana.
- `nookery-ex-acgc-pc-port` v1.0.0, `dusklight-ex-dusk` v2.0.3 e `strikers` v2.0.0 reutilizam a importação transacional de discos GameCube. O motor valida edição, revisão e digest, e informa a imagem ao executável oficial com `--disc`, `--dvd` ou `STRIKERS_DATA`.
- Os pacotes oficiais passaram pelos testes de preparo, cancelamento e rejeição de mídia no motor. Os planos de inicialização foram conferidos com dados sintéticos. As quatro receitas continuam experimentais e aguardam instalação com mídia original e primeiro boot.

## Histórico do SDK 1.5.9

Desktop 3.0.0 / SDK 1.5.9 (`feat/round-17e-functional-installation`); GetAll-Addon (`feat/round-17-restricted-installers`). Catalogo oficial `brad38/AllFix-Repo`: 110 jogos, 145 projetos (Leonida removido pelo responsavel pelo catalogo). Cobertura alcancada: **136/145 projetos (93,79%)** contemplados por **137 receitas** (136 experimentais, 1 `validated` historico, 16 `v9`), cobrindo **100% dos projetos tecnicamente viaveis no Windows**. **504 PASS C#** (`AddonInfrastructure.dll`), **137/137 receitas** aprovadas pelo parser SDK (`--parse-getall`), **137/137** no validador estrito Python (`--strict-lf --require-jsonschema --check-git-blobs --check-catalog`), **44/44** `unittest`, regressao JavaScript (`STORE_R19_UI_OPTIONALS_PASS`) aprovada, e build x64 self-contained publicado em `C:\Users\bradg\Downloads\GetAll-R18\publish-r18-current\AllFix.exe` (`77654982` bytes, SHA256 `be4c025b58f9516bf7a1147e8fd9337f86f097c547d5eed04efef53a53264c82`; `Toolchains\allfix-r18-mario.tar` e rollback `publish-r18-gt5\AllFix.exe` preservados).

## Novos pipelines implementados e preflights reais aprovados (6/6)
- `god-of-war-recomp` (`KIexster/god-of-war-recomp` @ `build-d1d11ec`, v5): ISO PS2 `SCUS_973.99` / `SCES_531.33`, `PS2Recomp` com todos os 55 parches upstream em ordem, dependencias FetchContent offline (`ELFIO`, `toml11`, `fmt`, `libdwarf`, `rabbitizer`, `nlohmann_json`, `raylib`, `imgui`, `rlImGui`), FFmpeg n7.1, LLVM/Ninja/CMake (`EXTRA_PREFLIGHT_PASS gow-kiexster`: `ps2_recomp.exe` compilado).
- `strikers-wiicompiled` (`BlackAndBlue95/Strikers-WiiCompiled` @ `build-451e06b`, v5): ISO/WBFS/RVZ/DOL R4QE01, `nodtool v2.0.0-alpha.10`, `.NET 8` `Translator.Cli`, `llvm-mingw`, Dawn + SDL3 (`EXTRA_PREFLIGHT_PASS strikers-wii`: `Translator.Cli.dll` compilado).
- `strikersrecomp` (`aharonahdoot/StrikersRecomp` @ `build-cd88f71`, v5): ISO/DOL `G4QE01`, `DolRecomp` + `GXRuntime` + `smstrikers-decomp` + `Dawn` + `SDL3` + `-include atomic` (`EXTRA_PREFLIGHT_PASS strikers-recomp`: `dolrecomp.exe` + `sdk_symbols.inc` gerados).
- `mkdd-recomp` (`LeftInWalmart/MKDD-Recomp` @ `build-e173ce4`, v5): `.iso`/`.ciso` `GM4E01` (`main.dol` SHA-1 + FST), JDK 21 + Ghidra 12.1.4 + GameCubeLoader 1.3.1 headless (`CreateGapFunctions.java`, `ExportSheets.java`, `ExportPcode.java`), `build_sheets.py`, `gen_rust.py` e Cargo Rust `mkdd-bevy` (`EXTRA_PREFLIGHT_PASS mkdd-alt`).
- `wipeout-rewrite` (`phoboslab/wipeout-rewrite` @ `build-b425ecb`, v5): pasta `wipeout/` (`textures/`, `common/`) ou ISO original, `clang-cl` + Ninja + SDL2 2.30.11 + GLEW 2.2.0 (`EXTRA_PREFLIGHT_PASS wipeout`: `wipeout.exe` compilado).
- `hookshot-zelda-oot-port` (`ZuanCrisp/Zelda-OOT-Port` @ `v3.0.2`, v9 `hookshot-3.0.2-prepare`): kit oficial + 8 partes SHA-256 fixadas, `HookshotBuilder.exe --cli --prepare`, `.nup`/`.nx` ou pasta `exefs`/`romfs`, opt-in DLSS (`HOOKSHOT_STAGE_PASS`).

## Concluidos e testes em pipelines existentes e UI Desktop
- **GT5 PS3 (`gt5-recomp`)**: leitor UDF 2.50 limitado em `GameInstallationIso9660.cs`, seletor `.PUP` local (`SCEUF\0\0\0` + extracao `tar` limitada + verificacao SHA-256 mantendo TLS estrito), extracao de SELF debug (`SCE\0` -> ELF, rejeicao clara para SELF retail sem embutir chaves Sony) e stream AES-128-CBC `Ps3DecryptedDiscStream` com chave/arquivo `.dkey` estritamente em memoria (`CryptographicOperations.ZeroMemory` e prompt mascarado `PasswordBox` no Desktop).
- **SM64 Windows limpo (`sm64ex`, `render96ex`, `sm64rt`)**: deteccao portatil em `AllFix-ToolchainCache` e `Toolchains\`, diagnostico claro WSL2/Docker, fallback de assinatura oficial Docker Desktop e `Dockerfile` deterministico com exportacao atomica `.tar.tmp` e suporte preservado aos packs Render96.
- **GTA Stories (`gta-stories-recompiled`)**: opt-in experimental explicito `--oneproc` (`lcs_game.dll`/`vcs_game.dll`, `mode: "oneproc"`) ao lado do modo combinado em dois processos e checkbox/prompt no Desktop.
- **SSX / Pinyon / DOAX e Bananza (`dkb-pc-recomp`)**: opcionais upstream (SSX Title Update `.xexp` + pacotes STFS DLC em `userdata/dlc/`, Pinyon DLSS + baseline AVX2/SSE4.1, DOAX Vulkan + RTGI), retencao/validacao de checkpoints por fase em todos eles, e testes deterministicos para `KeepDkbDataPhase` no DKB.
- **Auditoria integral dos pacotes portateis (`R18-EVIDENCIAS-PORTATEIS.json`)**: todos os **38** pacotes portateis antes marcados `?` na matriz (`sm64plus`, `starship`, `perfect-dark-pc-port-perfect-dark`, `project-midas`, `ggarecomp`, `adam-s-ant-farm`, `extremegrecomp`, `chameleontwist1-jp-recomp`, `automobililamborghini-recomp`, os 5 titulos AKI, `foxhollow`, `zelda3`, `zelda-3-launcher`, `super-metroid-launcher`, `smw`, `autotmc-auto-tmc`, `project-picori-999sian-tmc`, `opengoal`, `symphonyrecomp`, `crash-team-racing-high-octane`, `ctr-native`, `wipeout-phantom-edition`, `redriver2`, `severed-chains`, `vandalhearts-pcport`, `trx-tomb-raider-i-iii-community-edition`, `openlara`, `unleashedrecomp`, `cannonball`, `re-blue`, `king-kong-recompiled`, `thesimpsonsgamerecomp`, `gt4recomp`, `pgr4-recomp`) passaram verificacao real SHA-256 e staging no SDK (`38/38`), elevando `R18-EVIDENCIAS-PORTATEIS.json` para **78 registros**, sem reter payloads comerciais em disco.

## Bloqueios externos reais e inconsistencias de catalogo (`brad38/AllFix-Repo#8`)
Os 9 projetos sem receita remanescentes foram auditados caso a caso e permanecem inviaveis como builds PC automatizados sem correcao upstream ou ajuste no catalogo:
1. `drmario64-recomp` (`AngheloAlf/drmario64_recomp` arquivado): exige clone de decomp externa (`AngheloAlf/drmario64`), Makefile Linux/MIPS com submodulos SSH (`git@`) e autor declara Windows nao suportado sem releases.
2. `project-2099`: pacote oficial mistura `Engine/Data/Mods` sem comprovacao de autorizacao de distribuicao do conteudo.
3. `sonic-1-forever-sonic-2-absolute`: ID unico no catalogo para dois projetos/instaladores upstream distintos (`Sonic 1 Forever` e `Sonic 2 Absolute`); requer desmembramento na issue `#8` antes da receita.
4. `wind-waker-recomp`: README upstream redireciona integralmente para `BlueWake` (`bluewake`, ja coberto no GetAll) e retirou suas releases.
5. `metaforce`: endpoints historicos (`releases.axiodl.com` / GitHub) retornam HTTP 404 sem release Windows distribuida.
6. `twilight-princess-courage-reborn`: projeto externo sem distribuicao Windows oficial verificavel.
7. `doldecomp-mkdd-decompilacao-base`: repositorio de decompilacao de console GameCube, nao um port PC executavel.
8. `tmc-decompilacao-base`: repositorio de decompilacao GBA, nao um port PC executavel.
9. `mml1-megaman-legends-decomp`: repositorio de decompilacao PS1, nao um port PC executavel.

---

# Rodada 18 — continuidade: GTA combinado, verificação e armazenamento (24/11/2026)

Desktop 3.0.0 / SDK 1.5.9; head privado 4b137a0eecfdd52fbb177d8f09a8c0eed1cec1bd. Código funcional no commit 2d22c4795b3bcb4a8227232cd72b7f6d10f2c4c6; commits posteriores somente documentação Render96. Cobertura 130/145 (89,66%), 131 receitas, 15 sem receita. Cinco kits prioritários com pipelines fechados e preflight real; GTA Stories modo combinado de dois processos integrado, com seleção de duas ISOs e cinco packs gerados das mídias próprias. Render96 seleção/download opt-in. 429 PASS C#, parser 131/131, validator Python 131/131, unittest 44/44, JS PASS. Windows CI #19 aprovado; #21 documentação em verificação no registro. GetAll CI #62 aprovado. Executável C:\Users\bradg\Downloads\GetAll-R18\publish-r18-current\AllFix.exe, 77614677 bytes, SHA256 d6326bd6208f378983687d4f0e2be52aaad0b6f21fdf5b93773f67dc08cf51b8; tar SM64 verificado, rollback anterior preservado. Removidos 4.436.232.759 bytes de scratch próprio após preservar evidências; workspace 19.055.709.787 bytes; disco C livre 116.451.659.776 bytes. Zero novas instalações jogáveis/boots comprovados. Pendências: homologação positiva dos cinco kits/GTA, MKW spec legítima, GTA oneproc experimental, opcionais SSX/Pinyon/DOAX, GT5 SELF/PUP/ISO cifrada/UDF, SM64 Windows limpo, Bananza recuperação positiva, WPF/UAC, 15 sem receita. TLS PS3: links Sony BR/US HTTP; HTTPS com validação normal rejeitado em ambos (curl 60 SEC_E_WRONG_PRINCIPAL). Issue catálogo #8 para identidades inconsistentes, sem alteração de IDs. Não é conclusão da Rodada 18. Sem merge PR, release, DownloadAll ou troca de instalado.

---

# Rodada 18 — continuidade dos cinco kits prioritários (24/11/2026)

Desktop 3.0.0 / SDK 1.5.9; privado 488436bbdefe38aa822b8574502fee9580eecbf7; receitas fixadas 714cec7f6bfa176ae69986be77c1b8aa23c175f8. Cobertura 130/145 (89,66%), 131 receitas, 15 sem receita. God of War PS2, RyGT, SpartanPort, Odyssey e MKW: perfis fechados de execução implementados, com preflights dos kits oficiais. MKW condicionado a especificação SM86 local legítima; não executa captura de memória NVIDIA. Render96: seleção independente e download opt-in dos packs fixados, reutilizando importador. 425 PASS C#, parser 131/131, JS PASS, publish x64. Candidato local C:\Users\bradg\Downloads\GetAll-R18\publish-r18-current\AllFix.exe, 77612501 bytes, SHA256 fe94d37421d51e2894ee01d81e6f7d008a3ad83f7e95aa62aee081717f6a892a. Windows CI #18 em andamento no momento do registro. Nenhuma nova instalação jogável, compilação integral de jogo ou primeiro boot comprovado. Pendências internas: modo combinado GTA, opcionais SSX/Pinyon/DOAX, GT5 SELF/PUP/ISO cifrada/UDF, 15 projetos sem receita, SM64 em Windows limpo, recuperação positiva Bananza, WPF/UAC e homologação com mídias legítimas. Não é conclusão da Rodada 18. Sem merge, release, DownloadAll, substituição do EXE instalado ou alteração de catálogo. [Detalhes](RODADA-18.md) e [matriz](COBERTURA-R18.md).

---

# Rodada 18 — checkpoint contínuo de 24/11/2026 (11:41 BRT)

SDK 1.5.9 / Desktop 3.0.0. Privado 8d4a6ea51b68ef229cc203cd87262fcfb133e7c7; receitas fixadas 714cec7f6bfa176ae69986be77c1b8aa23c175f8. Cobertura 130/145 (89,66%), 131 receitas, 15 sem receita e 15 kits v9. SSX, Pinyon, GTA Stories e DOAX integrados com preflights reais; Render96 packs importados; GT5 ISO9660 legível e validação uniforme de volumes GT.VOL inteiros ou segmentados. 402 PASS C# (7 novas verificações GT5, 395 anteriores); parser 131/131 e JS PASS anteriores sem mudança de contrato; Release x64 self-contained de worktree limpa. Candidato local C:\Users\bradg\Downloads\GetAll-R18\publish-r18-gt5\AllFix.exe, 77591285 bytes, SHA256 eaf253867205469cc024de0073746311dcddfaf09b8ea4201dd977a215a2a489. Zero novas instalações jogáveis, builds integrais ou boots. Windows CI #13 e GetAll CI #60 aprovados; #14 iniciada. Retomar God of War, RyGT, SpartanPort, Odyssey, MKW e projetos sem receita viáveis; GT5 SELF/PUP/ISO cifrada, SM64 Windows limpo, Bananza positiva, UI WPF pendentes. Sem merge, release, DownloadAll ou substituição da instalação. [Detalhes](RODADA-18.md) e [matriz](COBERTURA-R18.md).

---

# Rodada 18 — missão contínua de conclusão (24/11/2026)

SDK 1.5.9 / Desktop 3.0.0. Privado ce3edac8dea0b1d73e2568293a914358bb2d451f; receitas 714cec7f6bfa176ae69986be77c1b8aa23c175f8. 130/145 projetos, 131 receitas, 15 sem receita. SSX/Pinyon/GTA Stories/DOAX: pipelines integrados, preflights reais aprovados. GT5 ISO9660 legível e packs Render96 integrados. 395 PASS C#, parser 131/131, JS PASS e Release x64 limpo. Sem novos builds integrais, instalações jogáveis ou boots homologados. Executável publish-r18-continued/AllFix.exe; hash e pendências executáveis em [RODADA-18.md](RODADA-18.md). Retomar God of War, RyGT, SpartanPort, Odyssey, MKW e restantes viáveis, sem nova rodada.

---

# Rodada 18 — checkpoint contínuo de 24/11/2026 (11:33 BRT)

SDK 1.5.9 / Desktop 3.0.0. Receitas fixadas: 714cec7f6bfa176ae69986be77c1b8aa23c175f8. Desktop privado: 051e32c57052bac012184446b8212f8e4e56b316. Cobertura nominal permanece 130/145 (89,66%), 131 receitas, 15 sem receita e 15 kits v9. SSX, Pinyon Shift, GTA Stories e ISO9660 PS3 legível integrados nos commits posteriores a LAS; testes negativos oficiais e fixtures, não jogos completos. Render96ex: packs opcionais oficiais fixados e importados em teste real (121 modelos, 2360 texturas), integração local após build, sem redistribuição. 392 PASS C#, parser 131/131, JS PASS, Release x64 self-contained de árvore limpa. Windows CI #11 aprovado; #12 iniciado para 051e32c. Novo candidato local: C:\Users\bradg\Downloads\GetAll-R18\publish-r18-combined\AllFix.exe, 77585251 bytes, SHA256 f24cf8801c739a4e685209da97c63aaa16a66118fcdb679164e1ca11af994f4a. Nenhum jogo integral, instalação completa, boot ou homologação novos. Retomar diretamente DOAX/God of War, RyGT/SpartanPort, Odyssey/MKW, receitas restantes, GT5 SELF/PUP, SM64 Windows limpo, Bananza retomada positiva e UI WPF. [Detalhes](RODADA-18.md) e [matriz](COBERTURA-R18.md). Sem merge, release, DownloadAll ou alteração do EXE instalado.

---

# Rodada 18 — missão contínua de conclusão (24/11/2026)

SDK 1.5.9 / Desktop 3.0.0. Receitas 714cec7f6bfa176ae69986be77c1b8aa23c175f8; privado b09abdce69b213a40ecaaa777492357974c6d7b7. 130/145 projetos (89,66%), 131 receitas, 15 sem receita e 15 kits v9. TotK CLI integrada com rejeição real de chave sintética; GT5/Burnout pipelines implementados e runtimes reais compilados; Bananza retenção da fase de dados/limpeza e testes negativos. 368 PASS C#, parser 131/131, 44 Python, JS, Release x64 de clone limpo. Zero novos jogos integralmente compilados, instalações completas ou boots. Executável e próximos comandos em [RODADA-18.md](RODADA-18.md); [matriz](COBERTURA-R18.md). LAS pipeline nativo e fixture ABI Zig aprovados. Retomar diretamente SSX/Pinyon e demais kits, sem nova rodada e sem repetir preparação. CI fixado às receitas. Sem release/merge/DownloadAll.

---

# Rodada 18 — missão contínua de conclusão (24/11/2026)

SDK 1.5.8; Desktop 3.0.0; código 930d4be203a25bc703d26f7252ab1f21bdef241f; receitas 028745e1c015428135c3281e58df6de4ef13edc0. Catálogo 110 jogos/145 projetos. 128/145 projetos com receita (88,28%); 129 receitas, 17 sem receita, 15 v9, 1 validated histórico. 3 perfis SM64 e DKB CLI; 39 preparações novas, CoopDX negativo; 345 PASS C#, parser 129/129, Python 44/44, JS PASS. Sem jogo integral/instalação/boot novo. [Matriz completa](COBERTURA-R18.md) | [Evidências e próxima tarefa executável](RODADA-18.md) | [Pacotes oficiais](R18-EVIDENCIAS-PORTATEIS.json). Retomar diretamente as tarefas da Rodada 18, não abrir nova rodada. Sem merge/release/DownloadAll.

---

# Rodada 17G — checkpoint parcial (24/11/2026)

SDK 1.5.7; Desktop 3.0.0; código privado 272a97821fd693e7ae056f2d700746e64a46426c; receitas GetAll 70d97c69e8ee8aac7d6db69995729a6dbbc8e184. 125/146 (85,62%); 126 receitas, 15 v9, 21 sem receita, 1 validated histórico. SM Rewrite compilado pelo motor; MKDD fonte/runtime_check verificados, jogo pendente; 15 novas preparações portáteis; CTR expiração UI; Forza fixture aprovada. 324 C#, parser 126/126, Python 44/44, JS PASS, clone limpo Release x64. Zero instalações completas/boots/homologações novas. [Matriz](COBERTURA-R17G-2026-11-24.md) | [Relatório](RODADA-17G-2026-11-24.md). Sem merge/release/DownloadAll.

---

# Rodada 17F — checkpoint parcial (24/11/2026)

SDK 1.5.6; Desktop 3.0.0; código privado 7b77aab5ef8a1a3b7ad30db0833929997935bbc5. 123/146 projetos (84,25%); 124 receitas; 15 v9; 23 sem receita; 1 validated histórico. CTR e SM compilados pelo motor; 7 preparações reais; zero novas instalações completas/boots/homologações. CI Windows privado criado. [Matriz](COBERTURA-R17F-2026-11-24.md) | [Relatório](RODADA-17F-2026-11-24.md). Sem merge/release/DownloadAll.

---

# Rodada 17E — checkpoint parcial (24/11/2026)

SDK 1.5.5; Desktop 3.0.0; código privado f6ffb767e96be7dff5af2c80e8cc3c3d546e94bd. 122/146 (83,56%), 15 v9, 24 sem receita, 1 validated histórico. Toolchains reais e pipeline Forza integrado, fixture compilada; Sonic/MML recuperação atômica; CTR executável principal compilado com 11 CTest aprovados e 1 skip. Zero novas instalações completas/boots/homologações. [Matriz](COBERTURA-R17E-2026-11-24.md) | [Relatório](RODADA-17E-2026-11-24.md). Sem merge/release/DownloadAll.

---

# Rodada 17D - checkpoint parcial (23/11/2026)

122/146 (83,56%), main 92, 24 sem receita, 15 v9, 1 validated histórico. SDK 1.5.4 / Desktop 3.0.0. Sonic processamento integral implementado, sem GDI real; Forza decoder XEX e SDK ReXGlue extraído, sem codegen/build; MML paridade US/JP verificada, sem mídia real. Desktop/SDK privados versionados no commit 62f1cd614a2eb371b8ada3f154666e15abed477a. Clone limpo: 300 C#, 122 parser, 44 Python, JS e 3 regressões oficiais; Release x64. Nenhuma nova instalação completa comprovada; UI não homologada. [Matriz](COBERTURA-R17D-2026-11-23.md) | [Relatório](RODADA-17D-2026-11-23.md). PR #18 draft; sem merge/release/DownloadAll.

---

# Rodada 17C - estado atual (23/11/2026)

122/146 projetos com receita (83,56%); 92 main, 24 sem receita, 15 v9, 1 validated historico. SDK 1.5.3 / Desktop 3.0.0. Retomada transacional MML condicionada a midia genuina; Forza XDVDFS/XEX; Sonic GDI e verificacoes estruturais Switch/PS4. Oito binarios de componentes upstream compilados em cinco projetos, zero novos jogos completos ou homologados. 277 PASS C#, 122 parser, 44 Python, JS e regressao offline tripla aprovados. [Matriz](COBERTURA-R17C-2026-11-23.md) | [Relatorio](RODADA-17C-2026-11-23.md). PR #18 draft, sem merge/release. Historico preservado.

---

# Rodada 17B — estado atual (23/11/2026)

122/146 projetos com receita em desenvolvimento (83,56%), 92 na main, 24 sem receita, 15 kits v9 de preparação, 121 experimental e 1 validated histórico. SDK 1.5.2; Desktop 3.0.0. Forza Inno e MML PyInstaller preparados pelo motor real; patch local US/JP, retomada sem redownload e grupos multipart testados. Build Docker Windows x64 com fixture sintético aprovado, sem autorização de build real de jogo. Nenhuma nova instalação completa ou homologação. [Matriz R17B](COBERTURA-R17B-2026-11-23.md) | [Relatório R17B](RODADA-17B-2026-11-23.md). Histórico anterior preservado.

---

# Rodada 17 — checkpoint parcial (23/11/2026)

120/146 projetos em desenvolvimento; 92 na main (base R16); 26 sem receita; 13 kits v9, 1 validated histórico, 119 experimental. SDK 1.5.1 / aplicativo 3.0.0. Sem alterações nas receitas ou publicação. Refatoração local da extração NSIS e apresentação estruturada de mídia original; 201 verificações C#, 120/120 parser, regressão real SARecomp e Release x64 concluída. Workspace Bradsson: `C:\Users\bradg\Downloads\GetAll-R17-20261123\desktop`; prévia `C:\Users\bradg\Downloads\GetAll-R17-20261123\publish-final\AllFix.exe`. Artefatos, impedimentos e evidências em [RODADA-17-2026-11-23.md](RODADA-17-2026-11-23.md). Próximo: Inno Setup/Forza, build isolado e payloads multipart; nenhum merge ou release autorizado. Rodada 17 ainda não concluída.

---

## Rodada 16 (23/11/2026)

120/146 projetos em desenvolvimento, 92 na main, 26 pendentes, 13 kits v9, SDK 1.5.1. Consulte [matriz completa](COBERTURA-R16-2026-11-23.md) e [relatorio](RODADA-16-2026-11-23.md). Historico anterior preservado abaixo.

# Rodada 16 — estado atual

**120/146 projetos com receita em desenvolvimento**, 92 na main, 26 sem receita. 13 perfis v9 apenas preparação. SDK 1.5.1. Consulte [matriz e evidências completas](RODADA-16-2026-11-23.md). Histórico anterior preservado abaixo.

---

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

## Transferência para o Codex — 2026-11-24

- O trabalho interrompido consta do checkpoint recuperável em `GetAll-R18/evidence-r18/handoff-20261124-161606`, com HEADs, patches binários e arquivos não rastreados.
- As receitas Team Forever individuais e a combinada estão na branch existente. As duas individuais requerem o catálogo curado que declara `sonic-1-forever` e `sonic-2-absolute`.
- A origem padrão continua `main`. Para testar as receitas ainda em revisão, use um complemento de teste explícito com um SHA de commit do GetAll e o Desktop/SDK 1.5.10 correspondentes.
- Próxima validação funcional: primeiro clique em Instalar, mídia legítima, preparação e primeiro boot de Hookshot e dos dois Team Forever. Ship of Harkinian precisa de um `soh-torch` validado e integrado sob perfil fechado. Consulte [a matriz](COBERTURA-R18.md).
