# Auditoria do inventário de receitas e evidências

Data de referência: 27/11/2026. Esta parte verifica todos os contratos declarativos. A conclusão sobre alterações em código de terceiros depende também da revisão Desktop e dos pacotes de suporte.

## Fontes fixadas

- GetAll: `ceaa962fe1a2088a7f3900509b856743ff4b6672`.
- Desktop: `921295de12349e726f7ca21a5edd8a8ecee123d8`.
- Catálogo: `3f4603cf42ef43402b4a0a9470232e7d4fcd9eb9`.
- SHA-256 do índice: `2e3ee9a442015c492c84cc28f92f7da75dfffdbbe817d42dc0f3b311cbfac9eb`.

## Resultado verificável

- 145 documentos de receita, 142 IDs com receita, 148 IDs no catálogo e 110 jogos.
- 144 entradas `experimental` e uma `validated`; por ID, 141 experimentais e um histórico homologado.
- Todos os hashes de receita conferem com o índice; não há receita órfã nem ID do índice fora do catálogo.
- As únicas operações declarativas são 28 `import_input`, cinco `create_directory` e um `import_input_set`. Nenhuma receita contém uma operação de alteração de source. Métodos específicos do Desktop podem aplicar patches mesmo com `operations: []`.
- SM64Plus, CTR Turbocharged e MKW têm duas receitas cada. Os aliases explicam 145 entradas para 142 IDs.
- Foram lidas as 97 revisões locais que alteram `index.json`: a única entrada nova com `validated` é SM64CoopDX, já presente em `a4646882dfbde3daaef3ebf9790696764d9ff880`. Não houve promoção posterior de outra receita a esse rótulo.
- A homologação de SM64CoopDX v1.5.1 é um relato histórico do usuário, preservado em `docs/AUDITORIA-CATALOGO-2026-11-22.md:7,16`; não foi reexecutada nesta auditoria.
- Os documentos finais declaram ausência de novo primeiro boot comercial (`docs/CHECKPOINT.md:5-10`; `docs/validations/sdk169-preview/README.md:8-10`). Aprovação de parser, build, teste de ABI, `--help` ou fixture não demonstra jogo completo.

## Como a contagem de 114 virou 142

`docs/CHECKPOINT.md:117-129` preserva o handoff com 142 receitas para 140 IDs, mas apenas 114 fluxos classificados como integrais. O aumento posterior de 28 refere-se à implementação de fluxos Desktop, não a 28 novos boots. A base de 114 é um estado herdado, não uma prova coletiva de jogabilidade; a revisão precisa alcançar seus métodos também.

O próprio catálogo contém o ID combinado Team Forever como `deprecated`, substituído pelos IDs Sonic 1 Forever e Sonic 2 Absolute. Os três têm receita. AutoTMC anuncia usar Picori, que tem outro ID. A contagem de 142 é de integrações/IDs, não de 142 engines de jogos independentes.

## Limites e achados específicos

- Metaforce: `../three-upstreams-20261127/source-de8fc69/README.md:12` descreve a reescrita em estabilização e builds indisponíveis. A receita de fonte não prova que esse estado se tornou jogável.
- Double Dash C++ (`mariokartdd-recomp`): `manual_steps` declara VR desativado. Isso deve ser confrontado com o código que aplica a configuração; a receita sozinha não define a autoria da mudança.
- Project 2099: não há receita. O relatório preservado descreve instalador público e runtime/payload separado; não confirma seleção de ROM no launcher. Não é correto prometer esse comportamento.
- Courage Reborn: não há receita nem confirmação de launcher operacional nos registros.
- As três bases de decompilação de console e Wind Waker antigo estão sem receita; não foram convertidas em ports Windows por estas receitas.
- Todos os 148 projetos do catálogo têm `windows.installation_enabled: false`; a possibilidade de instalação vem dos contratos do addon/SDK. Esse campo isolado não demonstra uma instalação feita.

## Matriz dos 148 IDs

O JSON anexo conserva o conteúdo completo de cada contrato, hash, operações, perfiles, referências literais de código quando disponíveis e evidências por projeto. `experimental` aqui significa ausência de homologação comercial registrada nesta rodada; não significa automaticamente que o upstream seja injogável.

| # | Projeto | Receita/tag | Entrada declarada | Boot comercial registrado |
| --- | --- | --- | --- | --- |
| 1 | `ghostship` | 3.0.0 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 2 | `sm64coopdx-super-mario-64-coop-deluxe` | v1.5.1 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | relato histórico do usuário |
| 3 | `sm64plus` | build-85c3e51; LauncherMirror | build_de_fonte_por_identidade_no_desktop; distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 4 | `render96ex` | build-48da5c4 | build_de_fonte_por_identidade_no_desktop | não comprovado |
| 5 | `sm64ex` | build-d7ca2c0 | build_de_fonte_por_identidade_no_desktop | não comprovado |
| 6 | `sm64rt` | build-20e618b | build_de_fonte_por_identidade_no_desktop | não comprovado |
| 7 | `ship-of-harkinian-soh` | 9.3.1 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 8 | `hookshot-zelda-oot-port` | v3.0.2 | hookshot-3.0.2-prepare | não comprovado |
| 9 | `zelda-64-recompiled` | v1.2.2 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 10 | `2-ship-2-harkinian-2s2h` | 5.0.1 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 11 | `starship` | v2.0.0 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 12 | `spaghettikart` | 1.0.0 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 13 | `mariokart-64-recompiled` | v0.9.2 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 14 | `battleship` | v1.6 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 15 | `paperboat` | 1.0.3 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 16 | `donkey-kong-64-recompiled-dk64-rekongpiled` | v1.0.3 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 17 | `snap64-recomp` | v1.1.8 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 18 | `drmario64-recomp-plus` | 1.0.0 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 19 | `drmario64-recomp` | build-7892264 | build_de_fonte_por_identidade_no_desktop | não comprovado |
| 20 | `banjo-recompiled` | v1.0.2 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 21 | `lighthouse` | 1.2.2 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 22 | `banjo-tooie-recompiled` | v1.0.1 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 23 | `perfect-dark-pc-port-perfect-dark` | ci-dev-build | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 24 | `project-midas` | 1.0.2b | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 25 | `goldeneye-007-pc-port` | v0.5.0 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 26 | `dinosaur-planet-recompiled-dino-recomp` | v0.3.0 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 27 | `bm64recomp` | v1.0.0 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 28 | `bmherorecomp` | v0.7.1 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 29 | `goemon64recomp` | v0.2.0-dev | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 30 | `ggarecomp` | v0.3.0 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 31 | `gga64recomp` | v0.1.0 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 32 | `dnzhrecomp` | 0.0.3 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 33 | `adam-s-ant-farm` | v0.11.14 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 34 | `body-harvest-recomp` | v0.1.0 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 35 | `sssv-recomp` | v0.2.0 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 36 | `quest64-recomp` | v0.1 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 37 | `megaman64recompiled` | v0.9.1 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 38 | `battletanx-global-assault-pc-port` | v0.2.5 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 39 | `btgarecomp` | v0.1.13 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 40 | `snowboardkids2-recomp` | v2.0.2 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 41 | `extremegrecomp` | v1.0.0 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 42 | `rocket-r` | v.1.0.1 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 43 | `chameleontwist1-jp-recomp` | v0.1 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 44 | `automobililamborghini-recomp` | v0.11.1 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 45 | `wcwvsnwoworldtourrecomp` | v0.3.2 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 46 | `wcwnworevengerecomp` | v0.3.2 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 47 | `wwfwrestlemania2000recomp` | v0.3.2 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 48 | `vpw64recomp` | v0.3.2 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 49 | `wwfnomercyrecomp` | v0.3.2 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 50 | `bluewake` | v0.12.0 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 51 | `wind-waker-recomp` | sem receita | superseded | sem implementação |
| 52 | `zeldawwhdrecomp` | v0.5.1 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 53 | `dusklight-ex-dusk` | v2.0.3 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 54 | `twilight-princess-courage-reborn` | sem receita | official_package_unavailable | sem implementação |
| 55 | `foxhollow` | v1.0.30 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 56 | `nookery-ex-acgc-pc-port` | v1.0.0 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 57 | `open-nectar` | 1.3 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 58 | `metaforce` | build-de8fc69 | build_de_fonte_por_identidade_no_desktop | não comprovado |
| 59 | `strikers` | v2.0.0 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 60 | `strikersrecomp` | build-cd88f71 | build_de_fonte_por_identidade_no_desktop | não comprovado |
| 61 | `recharged` | v1.1.7 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 62 | `strikers-wiicompiled` | build-451e06b | build_de_fonte_por_identidade_no_desktop | não comprovado |
| 63 | `mariokartdd-recomp` | build-bd36eb9 | build_de_fonte_por_identidade_no_desktop | não comprovado |
| 64 | `mkdd-recomp` | build-e173ce4 | build_de_fonte_por_identidade_no_desktop | não comprovado |
| 65 | `doldecomp-mkdd-decompilacao-base` | sem receita | console_decompilation | sem implementação |
| 66 | `zelda3` | v0.3 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 67 | `zelda-3-launcher` | v1.3.7.0 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 68 | `super-metroid-launcher` | v1.0.1 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 69 | `sm` | build-578f90b | build_de_fonte_por_identidade_no_desktop | não comprovado |
| 70 | `sm-rewrite` | build-5237873 | build_de_fonte_por_identidade_no_desktop | não comprovado |
| 71 | `supermarioworldrecomp` | v0.15.11 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 72 | `smw` | v0.1 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 73 | `phase-distorter` | 0.5 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 74 | `autotmc-auto-tmc` | 1.0.2 | aplicativo_portatil | não comprovado |
| 75 | `project-picori-999sian-tmc` | v0.9.6 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 76 | `tmc-decompilacao-base` | sem receita | console_decompilation | sem implementação |
| 77 | `gsrecomp` | 0.8.4 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 78 | `opengoal` | v0.3.9 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 79 | `god-of-war-native-pc-port-gow-pc-port` | launcher-v0.4.0 | gow-0.4.0-prepare | não comprovado |
| 80 | `god-of-war-recomp` | build-d1d11ec | build_de_fonte_por_identidade_no_desktop | não comprovado |
| 81 | `shadow-of-rome-recompiled` | v2.9.5 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 82 | `symphonyrecomp` | v1.2.0p | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 83 | `crash-team-racing-high-octane` | v.1.5 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 84 | `crash-team-racing-turbocharged` | ci-07d0c49; build-07d0c49 | build_de_fonte_por_identidade_no_desktop; distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 85 | `ctr-native` | beta-7.1 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 86 | `wipeout-phantom-edition` | v1.2.256 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 87 | `wipeout-rewrite` | build-b425ecb | build_de_fonte_por_identidade_no_desktop | não comprovado |
| 88 | `redriver2` | 7.4-rc2 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 89 | `severed-chains` | release-3.0.0 | distribuicao_java | não comprovado |
| 90 | `silent-hill-native-pc-port` | crossplatform-beta | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 91 | `vandalhearts-pcport` | v2.1.0 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 92 | `bloodyroar2recomp` | v0.7.1 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 93 | `knowyourrolerecomp` | v0.2.0 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 94 | `kf1-enhanced` | v0.1.0-pre.3 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 95 | `yu-gi-oh-forbidden-memories-recompiled` | v0.3.0 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 96 | `trx-tomb-raider-i-iii-community-edition` | trx-1.12 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 97 | `openlara` | latest | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 98 | `mega-man-legends-modernization-project` | v0.9.6-beta | mml-0.9.6-beta-pyinstaller-prepare | não comprovado |
| 99 | `mml1-megaman-legends-decomp` | sem receita | console_decompilation | sem implementação |
| 100 | `unleashedrecomp` | v1.0.3 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 101 | `marathon-recompiled` | v1.0.0 | marathon-1.0.0-xbox-import | não comprovado |
| 102 | `shadow-recompiled` | v1.0.1 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 103 | `sarecomp-sonic-adventure-recompiled` | v0.52.0 | sarecomp-0.52.0-prepare | não comprovado |
| 104 | `rsdkv4-decompilation` | 1.3.3 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 105 | `sonic-1-forever-sonic-2-absolute` | v1.5.2-v1.2.2 | teamforever-1.5.2-1.2.2-prepare | não comprovado |
| 106 | `sonic-1-forever` | v1.5.2 | teamforever-sonic1-1.5.2 | não comprovado |
| 107 | `sonic-2-absolute` | v1.2.2 | teamforever-sonic2-1.2.2 | não comprovado |
| 108 | `sonic-3-a-i-r-oxygen-engine` | v26.03.28.0-stable | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 109 | `cannonball` | v0.34 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 110 | `pinyon-shift` | v0.9.5 | pinyon-0.9.5-prepare | não comprovado |
| 111 | `fh1-reimagined` | v0.3.9 | fh1-0.3.9-inno-prepare | não comprovado |
| 112 | `re-blue` | nightly-v1.4.0-d187173d8-s44b7fdc5 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 113 | `the-darkness-recomp` | v0.1.10 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 114 | `downpourrecomp` | v1.1.8 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 115 | `dprecomp` | v2.0.14 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 116 | `project8recomp` | v0.3.0 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 117 | `project-2099` | sem receita | asset_redistribution_blocked | sem implementação |
| 118 | `edge-of-time-recomp` | v1.1 | edge-of-time-1.1-xbox-import | não comprovado |
| 119 | `king-kong-recompiled` | v2.1.3 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 120 | `earthworm-jim-hd-recompiled` | v0.9.6 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 121 | `thesimpsonsgamerecomp` | v0.0.7.1 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 122 | `dead-rising-2-case-zero-xenon-recomp` | v1.1.3 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 123 | `dead-rising-2-case-west-xenon-recomp` | v1.1.2 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 124 | `doaxvb-re` | v0.8.0 | doax-0.8.0-prepare | não comprovado |
| 125 | `3on3nhl-recomp` | v0.1.1 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 126 | `shadow-of-the-colossus-pc` | v0.77 | sotc-0.77-prepare | não comprovado |
| 127 | `savagewindrecomp` | v0.6.0-alpha.6 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 128 | `totk-pc-recomp` | v0.5.0 | totk-0.5.0-prepare | não comprovado |
| 129 | `gt4recomp` | v1.3.0-rc16 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 130 | `gt5-recomp` | build-64ca169 | build_de_fonte_por_identidade_no_desktop | não comprovado |
| 131 | `rygt-gt7` | rygt-2026-11-23 | rygt-2026-11-23-prepare | não comprovado |
| 132 | `lasrecomp` | v0.6.1 | las-0.6.1-prepare | não comprovado |
| 133 | `super-odyssey-pc-recomp` | v1.0.0 | odyssey-1.0.0-prepare | não comprovado |
| 134 | `god-hand-rearmed` | v0.6.9.5 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 135 | `gta-stories-recompiled` | v0.3.2 | gta-stories-0.3.2-prepare | não comprovado |
| 136 | `spartanport` | windows-v3.2.1 | spartanport-3.2.1-prepare | não comprovado |
| 137 | `tlg-pc` | v2026.11.14-ee3327d | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 138 | `iss-pc` | v1.0 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 139 | `pt-pc` | v1.1.1 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 140 | `gears-of-war-2-pc-port` | v0.4.8 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 141 | `ng2recomp` | v0.7.5 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 142 | `pgr4-recomp` | v2.0.2 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 143 | `burnout3-recomp` | build-3c85ed7 | build_de_fonte_por_identidade_no_desktop | não comprovado |
| 144 | `opence` | build-387 | build_de_fonte_por_identidade_no_desktop | não comprovado |
| 145 | `lost-odyssey-recomp` | v1.1.0 | distribuicao_precompilada_com_fluxo_especifico_ou_generico | não comprovado |
| 146 | `ssx-recomp` | v2.0.0 | ssx-2.0.0-prepare | não comprovado |
| 147 | `dkb-pc-recomp` | v0.5.1 | dkb-0.5.1-44ba6b1-prepare | não comprovado |
| 148 | `mkw-recomp` | v0.1.18; v0.1.18-allfix-cli | mkw-0.1.18-cli-prepare; mkw-0.1.18-prepare | não comprovado |

## Reprodução

Execute `python docs/audits/source-integrity-20261127/catalog_inventory.py` no checkout GetAll. O script lê receitas/catálogo/refs literais Desktop e grava somente `catalog-review.json` e `catalog-review.md`; não compila nem executa jogos e não altera contratos.
