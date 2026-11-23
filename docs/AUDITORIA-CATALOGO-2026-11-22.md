# GetAll-Addon — matriz integral de compatibilidade (2026-11-22)

**Fontes:** [AllFix-Repo](https://github.com/brad38/AllFix-Repo) — `catalog.json` (blob `9628931e87e1a9d5e2c9230d4ec56d2ea8ffc7f7`), `requirements.json` (blob `0ecb3807fba268271a67b011b954914d09ed5b9c`), `about.json` (blob `0c5c7795e7800356a75b5600ad9bb38ad7187a22`). O catálogo foi lido integralmente: **87 jogos, 119 projetos**, dos quais 115 apontam para repositórios GitHub e quatro para outras URLs. Foram consultadas as listas de releases e os READMEs padrão das 115 origens GitHub, com lacunas registradas e não ocultadas. As outras quatro origens foram verificadas separadamente na web. 

**Categorias:** A — contrato existente consegue representar o fluxo identificado; B — pacote Windows/executável encontrado, mas falta integrar o provisionamento dos dados originais, primeiro lançamento ou verificações; C — exige operação ou fonte não contemplada pelo SDK atual; D — documentação, origem ou release insuficientes para garantir instalação.

**Distribuição:** A=2, B=85, C=27, D=5 (total 119). A é compatibilidade **estrutural**, não aprovação funcional: GoldenEye está em A mas **não foi testado com ROM real** e sua receita permanece `experimental`. Somente SM64 Coop Deluxe v1.5.1 continua com `validated`, por testes integrados previamente confirmados pelo usuário. Nenhuma nova receita foi homologada como executável nesta rodada.

**Metodologia e limitações:** uma Release listada não prova instalação funcional. O nome do ativo foi cruzado com os metadados oficiais; os oito ZIPs de Starship, SpaghettiKart, Cannonball, Ghostship, Zelda64 Recompiled, GoldenEye, BattleTanx GA e Phase Distorter foram baixados e abertos sem executar código. O conteúdo dos demais assets não foi extraído nem testado. O campo `windows.installation_enabled` está falso em todos os 119 projetos e não foi usado como classificação. As notas do catálogo foram consideradas, mas o conteúdo binário/README oficial prevalece quando disponível. Não foram usados arquivos comerciais nem ROMs.

## Matriz de todos os 119 projetos

| # | Jogo | Projeto (ID do catálogo) | Tag examinada | A/B/C/D | Receita | Teste |
|---:|---|---|---|:---:|---|---|
| 1 | Super Mario 64 | [Ghostship](https://github.com/HarbourMasters/Ghostship) `ghostship` | `3.0.0` | **B** | Pendente | ZIP inspecionado; sem execução |
| 2 | Super Mario 64 | [sm64coopdx (Super Mario 64 Coop Deluxe)](https://github.com/coop-deluxe/sm64coopdx) `sm64coopdx-super-mario-64-coop-deluxe` | `v1.5.1` | **A** | Publicada (validated) | Relato do usuário: importação e execução |
| 3 | Super Mario 64 | [SM64Plus](https://github.com/MorsGames/sm64plus) `sm64plus` | `LauncherMirror` | **B** | Pendente | Sem teste integrado |
| 4 | Super Mario 64 | [Render96ex](https://github.com/Render96/Render96ex) `render96ex` | `—` | **C** | Pendente | Sem teste integrado |
| 5 | Super Mario 64 | [sm64ex](https://github.com/sm64pc/sm64ex) `sm64ex` | `—` | **C** | Pendente | Sem teste integrado |
| 6 | Super Mario 64 | [sm64rt](https://github.com/DarioSamo/sm64rt) `sm64rt` | `—` | **C** | Pendente | Sem teste integrado |
| 7 | The Legend of Zelda: Ocarina of Time | [Ship of Harkinian (SoH)](https://github.com/HarbourMasters/Shipwright) `ship-of-harkinian-soh` | `9.3.1` | **B** | Pendente | Sem teste integrado |
| 8 | The Legend of Zelda: Majora's Mask | [Zelda 64: Recompiled](https://github.com/Zelda64Recomp/Zelda64Recomp) `zelda-64-recompiled` | `v1.2.2` | **B** | Pendente | ZIP inspecionado; sem execução |
| 9 | The Legend of Zelda: Majora's Mask | [2 Ship 2 Harkinian (2S2H)](https://github.com/2ship2harkinian/2ship2harkinian) `2-ship-2-harkinian-2s2h` | `5.0.1` | **B** | Pendente | Sem teste integrado |
| 10 | Star Fox 64 | [Starship](https://github.com/HarbourMasters/Starship) `starship` | `v2.0.0` | **B** | Pendente | ZIP inspecionado; sem execução |
| 11 | Mario Kart 64 | [SpaghettiKart](https://github.com/HarbourMasters/SpaghettiKart) `spaghettikart` | `1.0.0` | **B** | Pendente | ZIP inspecionado; sem execução |
| 12 | Mario Kart 64 | [MarioKart 64: Recompiled](https://github.com/sonicdcer/MarioKart64Recomp) `mariokart-64-recompiled` | `v0.9.2` | **B** | Pendente | Sem teste integrado |
| 13 | Super Smash Bros. | [BattleShip](https://github.com/JRickey/BattleShip) `battleship` | `v1.6` | **B** | Pendente | Sem teste integrado |
| 14 | Paper Mario | [PaperBoat](https://github.com/HarbourMasters/PaperBoat) `paperboat` | `1.0.3` | **B** | Pendente | Sem teste integrado |
| 15 | Donkey Kong 64 | [Donkey Kong 64: Recompiled (DK64 Rekongpiled)](https://github.com/Rainchus/Donkey-Kong-64-Recompiled) `donkey-kong-64-recompiled-dk64-rekongpiled` | `v1.0.3` | **B** | Pendente | Sem teste integrado |
| 16 | Pokémon Snap | [Snap64 Recomp](https://github.com/JackandBeans/Snap64Recomp) `snap64-recomp` | `v1.1.8` | **B** | Pendente | Sem teste integrado |
| 17 | Dr. Mario 64 | [drmario64_recomp_plus](https://github.com/theboy181/drmario64_recomp_plus) `drmario64-recomp-plus` | `1.0.0` | **B** | Pendente | Sem teste integrado |
| 18 | Dr. Mario 64 | [drmario64_recomp](https://github.com/AngheloAlf/drmario64_recomp) `drmario64-recomp` | `—` | **C** | Pendente | Sem teste integrado |
| 19 | Banjo-Kazooie | [Banjo: Recompiled](https://github.com/BanjoRecomp/BanjoRecomp) `banjo-recompiled` | `v1.0.2` | **B** | Pendente | Sem teste integrado |
| 20 | Banjo-Kazooie | [Lighthouse](https://github.com/HarbourMasters/Lighthouse) `lighthouse` | `1.2.2` | **B** | Pendente | Sem teste integrado |
| 21 | Banjo-Tooie | [Banjo-Tooie: Recompiled](https://github.com/Vidanox/BanjoTooieRecompiled) `banjo-tooie-recompiled` | `v1.0.1` | **B** | Pendente | Sem teste integrado |
| 22 | Perfect Dark | [Perfect Dark PC Port (perfect_dark)](https://github.com/perfect-dark-pc-port/perfect_dark) `perfect-dark-pc-port-perfect-dark` | `ci-dev-build` | **B** | Pendente | Sem teste integrado |
| 23 | GoldenEye 007 | [Project Midas](https://github.com/murkantor/Project-Midas) `project-midas` | `1.0.2b` | **D** | Pendente | Sem teste integrado |
| 24 | GoldenEye 007 | [GoldenEye 007 PC Port](https://github.com/jkdansereau/goldeneye-pc-port) `goldeneye-007-pc-port` | `v0.5.0` | **A** | Candidata (experimental) | ZIP inspecionado; sem teste com ROM |
| 25 | Dinosaur Planet | [Dinosaur Planet: Recompiled (dino-recomp)](https://github.com/DinosaurPlanetRecomp/dino-recomp) `dinosaur-planet-recompiled-dino-recomp` | `v0.3.0` | **B** | Pendente | Sem teste integrado |
| 26 | Bomberman 64 | [BM64Recomp](https://github.com/RevoSucks/BM64Recomp) `bm64recomp` | `v1.0.0` | **B** | Pendente | Sem teste integrado |
| 27 | Bomberman Hero | [BMHeroRecomp](https://github.com/RevoSucks/BMHeroRecomp) `bmherorecomp` | `v0.7.1` | **B** | Pendente | Sem teste integrado |
| 28 | Mystical Ninja Starring Goemon | [Goemon64Recomp](https://github.com/klorfmorf/Goemon64Recomp) `goemon64recomp` | `v0.2.0-dev` | **B** | Pendente | Sem teste integrado |
| 29 | Goemon's Great Adventure | [GGARecomp](https://github.com/DreaXer/GGARecomp) `ggarecomp` | `v0.3.0` | **B** | Pendente | Sem teste integrado |
| 30 | Goemon's Great Adventure | [GGA64Recomp](https://github.com/StopSine/GGA64Recomp) `gga64recomp` | `v0.1.0` | **B** | Pendente | Sem teste integrado |
| 31 | Duke Nukem: Zero Hour | [DNZHRecomp](https://github.com/sonicdcer/DNZHRecomp) `dnzhrecomp` | `0.0.3` | **B** | Pendente | Sem teste integrado |
| 32 | Body Harvest | [Adam's Ant Farm](https://github.com/LunarLaurus/adams-ant-farm-recomp) `adam-s-ant-farm` | `v0.11.14` | **B** | Pendente | Sem teste integrado |
| 33 | Body Harvest | [body-harvest-recomp](https://github.com/danielgomesvieira2000/body-harvest-recomp) `body-harvest-recomp` | `v0.1.0` | **B** | Pendente | Sem teste integrado |
| 34 | Space Station Silicon Valley | [SSSV_Recomp](https://github.com/Cellenseres/SSSV_Recomp) `sssv-recomp` | `v0.2.0` | **B** | Pendente | Sem teste integrado |
| 35 | Quest 64 | [Quest64-Recomp](https://github.com/Rainchus/Quest64-Recomp) `quest64-recomp` | `v0.1` | **B** | Pendente | Sem teste integrado |
| 36 | Mega Man 64 | [MegaMan64Recompiled](https://github.com/MegaMan64Recomp/MegaMan64Recompiled) `megaman64recompiled` | `v0.9.1` | **B** | Pendente | Sem teste integrado |
| 37 | BattleTanx: Global Assault | [BattleTanx-Global-Assault-PC-Port](https://github.com/TheGh0stShip/BattleTanx-Global-Assault-PC-Port) `battletanx-global-assault-pc-port` | `v0.2.5` | **B** | Pendente | ZIP inspecionado; sem execução |
| 38 | BattleTanx: Global Assault | [btgarecomp](https://github.com/wootbeer/btgarecomp) `btgarecomp` | `v0.1.13` | **B** | Pendente | Sem teste integrado |
| 39 | Snowboard Kids 2 | [snowboardkids2-recomp](https://github.com/cdlewis/snowboardkids2-recomp) `snowboardkids2-recomp` | `v2.0.2` | **B** | Pendente | Sem teste integrado |
| 40 | Extreme-G | ExtremeGRecomp `extremegrecomp` | `—` | **C** | Pendente | Sem teste integrado |
| 41 | Rocket: Robot on Wheels | [Rocket-R](https://github.com/thatguymcd/rocket-r) `rocket-r` | `v.1.0.1` | **B** | Pendente | Sem teste integrado |
| 42 | Chameleon Twist | [ChameleonTwist1-JP-Recomp](https://github.com/Rainchus/ChameleonTwist1-JP-Recomp) `chameleontwist1-jp-recomp` | `v0.1` | **B** | Pendente | Sem teste integrado |
| 43 | Automobili Lamborghini | [automobililamborghini-recomp](https://github.com/alondero/automobililamborghini-recomp) `automobililamborghini-recomp` | `v0.11.1` | **B** | Pendente | Sem teste integrado |
| 44 | WCW vs. nWo: World Tour | [WCWvsNWOWorldTourRecomp](https://github.com/jessetbh/WCWvsNWOWorldTourRecomp) `wcwvsnwoworldtourrecomp` | `v0.3.2` | **B** | Pendente | Sem teste integrado |
| 45 | WCW/nWo Revenge | [WCWnWoRevengeRecomp](https://github.com/jessetbh/WCWnWoRevengeRecomp) `wcwnworevengerecomp` | `v0.3.2` | **B** | Pendente | Sem teste integrado |
| 46 | WWF WrestleMania 2000 | [WWFWrestleMania2000Recomp](https://github.com/jessetbh/WWFWrestleMania2000Recomp) `wwfwrestlemania2000recomp` | `v0.3.2` | **B** | Pendente | Sem teste integrado |
| 47 | Virtual Pro Wrestling 64 | [VPW64Recomp](https://github.com/jessetbh/VPW64Recomp) `vpw64recomp` | `v0.3.2` | **B** | Pendente | Sem teste integrado |
| 48 | WWF No Mercy | [WWFNoMercyRecomp](https://github.com/jessetbh/WWFNoMercyRecomp) `wwfnomercyrecomp` | `v0.3.2` | **B** | Pendente | Sem teste integrado |
| 49 | The Legend of Zelda: The Wind Waker | [BlueWake](https://github.com/chrissotraidis/bluewake) `bluewake` | `v0.12.0` | **B** | Pendente | Sem teste integrado |
| 50 | The Legend of Zelda: The Wind Waker | [Wind-Waker-Recomp](https://github.com/elliotttate/Wind-Waker-Recomp) `wind-waker-recomp` | `—` | **D** | Pendente | Sem teste integrado |
| 51 | The Legend of Zelda: The Wind Waker HD | [ZeldaWWHDRecomp](https://github.com/ZeldaWWHDRecomp/ZeldaWWHDRecomp) `zeldawwhdrecomp` | `v0.5.1` | **B** | Pendente | Sem teste integrado |
| 52 | The Legend of Zelda: Twilight Princess | [Dusklight (ex-Dusk)](https://github.com/TwilitRealm/dusklight) `dusklight-ex-dusk` | `v2.0.3` | **B** | Pendente | Sem teste integrado |
| 53 | The Legend of Zelda: Twilight Princess | Twilight Princess: Courage Reborn `twilight-princess-courage-reborn` | `—` | **D** | Pendente | Sem teste integrado |
| 54 | Star Fox Adventures | [FoxHollow](https://github.com/JackPriceBurns/foxhollow) `foxhollow` | `v1.0.30` | **C** | Pendente | Sem teste integrado |
| 55 | Animal Crossing | [Nookery (ex-ACGC-PC-Port)](https://github.com/flyngmt/Nookery) `nookery-ex-acgc-pc-port` | `v1.0.0` | **B** | Pendente | Sem teste integrado |
| 56 | Pikmin & Pikmin 2 | [Open Nectar](https://github.com/SSunnKing/Open-Nectar---Pikmin-Native-PC-Mobile-Port) `open-nectar` | `1.3` | **B** | Pendente | Sem teste integrado |
| 57 | Metroid Prime | [Metaforce](https://github.com/AxioDL/metaforce) `metaforce` | `—` | **D** | Pendente | Sem teste integrado |
| 58 | Super Mario Strikers | [Strikers](https://github.com/new-coke/strikers) `strikers` | `v2.0.0` | **B** | Pendente | Sem teste integrado |
| 59 | Super Mario Strikers | [StrikersRecomp](https://github.com/aharonahdoot/StrikersRecomp) `strikersrecomp` | `v0.1.0` | **C** | Pendente | Sem teste integrado |
| 60 | Mario Strikers Charged | [Recharged](https://github.com/previouslevelgames/recharged) `recharged` | `v1.1.7` | **B** | Pendente | Sem teste integrado |
| 61 | Mario Strikers Charged | [Strikers-WiiCompiled](https://github.com/BlackAndBlue95/Strikers-WiiCompiled) `strikers-wiicompiled` | `—` | **C** | Pendente | Sem teste integrado |
| 62 | Mario Kart: Double Dash!! | [mariokartdd-recomp](https://github.com/ethannicholas/mariokartdd-recomp) `mariokartdd-recomp` | `—` | **C** | Pendente | Sem teste integrado |
| 63 | Mario Kart: Double Dash!! | [MKDD-Recomp](https://github.com/LeftInWalmart/MKDD-Recomp) `mkdd-recomp` | `—` | **C** | Pendente | Sem teste integrado |
| 64 | Mario Kart: Double Dash!! | [doldecomp/mkdd (Decompilação-base)](https://github.com/doldecomp/mkdd) `doldecomp-mkdd-decompilacao-base` | `—` | **C** | Pendente | Sem teste integrado |
| 65 | The Legend of Zelda: A Link to the Past | [zelda3](https://github.com/snesrev/zelda3) `zelda3` | `v0.3` | **C** | Pendente | Sem teste integrado |
| 66 | The Legend of Zelda: A Link to the Past | [Zelda 3 Launcher](https://github.com/RadzPrower/Zelda-3-Launcher) `zelda-3-launcher` | `v1.3.7.0` | **B** | Pendente | Sem teste integrado |
| 67 | Super Metroid | [Super Metroid Launcher](https://github.com/RadzPrower/Super-Metroid-Launcher) `super-metroid-launcher` | `v1.0.1` | **B** | Pendente | Sem teste integrado |
| 68 | Super Metroid | [sm](https://github.com/snesrev/sm) `sm` | `—` | **C** | Pendente | Sem teste integrado |
| 69 | Super Metroid | [sm_rewrite](https://github.com/testyourmine/sm_rewrite) `sm-rewrite` | `—` | **C** | Pendente | Sem teste integrado |
| 70 | Super Mario World | [SuperMarioWorldRecomp](https://github.com/mstan/SuperMarioWorldRecomp) `supermarioworldrecomp` | `v0.15.11` | **B** | Pendente | Sem teste integrado |
| 71 | Super Mario World | [smw](https://github.com/snesrev/smw) `smw` | `v0.1` | **C** | Pendente | Sem teste integrado |
| 72 | EarthBound / Mother 2 | [Phase Distorter](https://github.com/TheRunaway5/Phase-Distorter) `phase-distorter` | `0.5` | **B** | Pendente | ZIP inspecionado; sem execução |
| 73 | The Legend of Zelda: The Minish Cap | [AutoTMC (auto-tmc)](https://github.com/StonedModder/auto-tmc) `autotmc-auto-tmc` | `1.0.1` | **C** | Pendente | Sem teste integrado |
| 74 | The Legend of Zelda: The Minish Cap | Project Picori (999sian/tmc) `project-picori-999sian-tmc` | `—` | **D** | Pendente | Sem teste integrado |
| 75 | The Legend of Zelda: The Minish Cap | [tmc (Decompilação-base)](https://github.com/zeldaret/tmc) `tmc-decompilacao-base` | `—` | **C** | Pendente | Sem teste integrado |
| 76 | Golden Sun & Golden Sun: The Lost Age | [GSRecomp](https://github.com/Shmargus/GSRecomp) `gsrecomp` | `0.8.4` | **B** | Pendente | Sem teste integrado |
| 77 | Jak and Daxter 1, 2 e 3 | [OpenGOAL](https://github.com/open-goal/jak-project) `opengoal` | `v0.3.9` | **B** | Pendente | Sem teste integrado |
| 78 | God of War (2005) | [God of War: native PC port (gow-pc-port)](https://github.com/danielalves96/gow-pc-port) `god-of-war-native-pc-port-gow-pc-port` | `launcher-v0.4.0` | **C** | Pendente | Sem teste integrado |
| 79 | Shadow of Rome | [Shadow of Rome Recompiled](https://github.com/Korvonordico/shadow-of-rome-recompiled) `shadow-of-rome-recompiled` | `v2.9.5` | **C** | Pendente | Sem teste integrado |
| 80 | Castlevania: Symphony of the Night | [SymphonyRecomp](https://github.com/BlackLabelHQ/SymphonyRecomp) `symphonyrecomp` | `v1.2.0p` | **C** | Pendente | Sem teste integrado |
| 81 | Crash Team Racing | [Crash Team Racing: High Octane](https://github.com/Rinnegatamante/Crash-Team-Racing-High-Octane) `crash-team-racing-high-octane` | `v.1.5` | **B** | Pendente | Sem teste integrado |
| 82 | Crash Team Racing | [Crash Team Racing: Turbocharged](https://github.com/CameronRedmore/Crash-Team-Racing-Turbocharged) `crash-team-racing-turbocharged` | `—` | **C** | Pendente | Sem teste integrado |
| 83 | Crash Team Racing | [CTR Native](https://github.com/CTR-tools/ctr-native) `ctr-native` | `beta-7.1` | **B** | Pendente | Sem teste integrado |
| 84 | Wipeout | [WipeOut Phantom Edition](https://github.com/wipeout-phantom-edition/wipeout-phantom-edition) `wipeout-phantom-edition` | `v1.2.256` | **B** | Pendente | Sem teste integrado |
| 85 | Wipeout | [wipEout Rewrite](https://github.com/phoboslab/wipeout-rewrite) `wipeout-rewrite` | `—` | **C** | Pendente | Sem teste integrado |
| 86 | Driver 2 | [REDRIVER2](https://github.com/OpenDriver2/REDRIVER2) `redriver2` | `7.4-rc2` | **B** | Pendente | Sem teste integrado |
| 87 | The Legend of Dragoon | [Severed Chains](https://github.com/Legend-of-Dragoon-Modding/Severed-Chains) `severed-chains` | `release-3.0.0` | **B** | Pendente | Sem teste integrado |
| 88 | Silent Hill | [Silent Hill - Native PC Port](https://github.com/SlickAmogus/silent-hill-decomp) `silent-hill-native-pc-port` | `uwp-alpha-1` | **C** | Pendente | Sem teste integrado |
| 89 | Vandal Hearts | [VandalHearts-PcPort](https://github.com/HalmyLyseas/VandalHearts-PcPort) `vandalhearts-pcport` | `v2.1.0` | **B** | Pendente | Sem teste integrado |
| 90 | Bloody Roar II | [BloodyRoar2Recomp](https://github.com/novapowers0/BloodyRoar2Recomp) `bloodyroar2recomp` | `v0.7.1` | **B** | Pendente | Sem teste integrado |
| 91 | WWF SmackDown! 2: Know Your Role | [KnowYourRoleRecomp](https://github.com/Comfubar/KnowYourRoleRecomp) `knowyourrolerecomp` | `v0.2.0` | **B** | Pendente | Sem teste integrado |
| 92 | King's Field (JP, 1994) | [kf1-enhanced](https://github.com/Acranon/kf1-enhanced) `kf1-enhanced` | `v0.1.0-pre.3` | **B** | Pendente | Sem teste integrado |
| 93 | Yu-Gi-Oh! Forbidden Memories | [Yu-Gi-Oh! Forbidden Memories Recompiled](https://github.com/krystalgamer/Yu-Gi-Oh-Forbidden-Memories-Recompiled) `yu-gi-oh-forbidden-memories-recompiled` | `v0.3.0` | **B** | Pendente | Sem teste integrado |
| 94 | Tomb Raider I–V | [TRX (Tomb Raider I–III Community Edition)](https://github.com/LostArtefacts/TRX) `trx-tomb-raider-i-iii-community-edition` | `trx-1.12` | **B** | Pendente | Sem teste integrado |
| 95 | Tomb Raider I–V | [OpenLara](https://github.com/XProger/OpenLara) `openlara` | `latest` | **B** | Pendente | Sem teste integrado |
| 96 | Mega Man Legends / Rockman DASH | [Mega Man Legends Modernization Project](https://github.com/Drakfix/MML_Modernization-Project) `mega-man-legends-modernization-project` | `v0.9.6-beta` | **B** | Pendente | Sem teste integrado |
| 97 | Mega Man Legends / Rockman DASH | [mml1 (Megaman Legends Decomp)](https://github.com/ChrisNonyminus/mml1) `mml1-megaman-legends-decomp` | `—` | **C** | Pendente | Sem teste integrado |
| 98 | Sonic Unleashed | [UnleashedRecomp](https://github.com/hedge-dev/UnleashedRecomp) `unleashedrecomp` | `v1.0.3` | **B** | Pendente | Sem teste integrado |
| 99 | Sonic the Hedgehog (2006) | [Marathon Recompiled](https://github.com/sonicnext-dev/MarathonRecomp) `marathon-recompiled` | `v1.0.0` | **B** | Pendente | Sem teste integrado |
| 100 | Shadow the Hedgehog | [Shadow Recompiled](https://github.com/FoxWorkshop/ShadowRecomp) `shadow-recompiled` | `v1.0.1` | **B** | Pendente | Sem teste integrado |
| 101 | Sonic Adventure | [SARecomp (Sonic Adventure Recompiled)](https://github.com/sonicfreak1337/SARecomp) `sarecomp-sonic-adventure-recompiled` | `v0.52.0` | **B** | Pendente | Sem teste integrado |
| 102 | Sonic the Hedgehog 1 & 2 (2013) | [RSDKv4-Decompilation](https://github.com/RSDKModding/RSDKv4-Decompilation) `rsdkv4-decompilation` | `1.3.3` | **B** | Pendente | Sem teste integrado |
| 103 | Sonic the Hedgehog 1 & 2 (2013) | Sonic 1 Forever & Sonic 2 Absolute `sonic-1-forever-sonic-2-absolute` | `—` | **C** | Pendente | Sem teste integrado |
| 104 | Sonic 3 & Knuckles | [Sonic 3 A.I.R. (Oxygen Engine)](https://github.com/Eukaryot/sonic3air) `sonic-3-a-i-r-oxygen-engine` | `v26.03.28.0-stable` | **B** | Pendente | Sem teste integrado |
| 105 | OutRun | [Cannonball](https://github.com/djyt/cannonball) `cannonball` | `v0.34` | **B** | Pendente | ZIP inspecionado; sem execução |
| 106 | Forza Horizon | [Pinyon Shift](https://github.com/arcanite24/pinyon-shift) `pinyon-shift` | `v0.9.5` | **C** | Pendente | Sem teste integrado |
| 107 | Blue Dragon | [re:Blue](https://github.com/zolaware/reblue) `re-blue` | `nightly-v1.4.0-d187173d8-s44b7fdc5` | **B** | Pendente | Sem teste integrado |
| 108 | The Darkness | [The-Darkness-Recomp](https://github.com/portingpete/The-Darkness-Recomp) `the-darkness-recomp` | `v0.1.10` | **B** | Pendente | Sem teste integrado |
| 109 | Silent Hill: Downpour | [DownpourRecomp](https://github.com/LittleBitUA/DownpourRecomp) `downpourrecomp` | `v1.1.8` | **B** | Pendente | Sem teste integrado |
| 110 | Deadly Premonition | [DPRecomp](https://github.com/LittleBitUA/DPRecomp) `dprecomp` | `v2.0.14` | **B** | Pendente | Sem teste integrado |
| 111 | Tony Hawk's Project 8 | [Project8Recomp](https://github.com/theokyr/Project8Recomp) `project8recomp` | `v0.3.0` | **B** | Pendente | Sem teste integrado |
| 112 | Spider-Man: Edge of Time | [Project 2099](https://github.com/GenryTheFox0/Project-2099) `project-2099` | `v2.0.0-beta.4.1` | **C** | Pendente | Sem teste integrado |
| 113 | Peter Jackson's King Kong | [King Kong: Recompiled](https://github.com/TekRantGaming/king-kong-recompiled) `king-kong-recompiled` | `v2.1.3` | **B** | Pendente | Sem teste integrado |
| 114 | Earthworm Jim HD | [Earthworm Jim HD: Recompiled](https://github.com/TekRantGaming/earthworm-jim-hd-recompiled) `earthworm-jim-hd-recompiled` | `v0.9.6` | **B** | Pendente | Sem teste integrado |
| 115 | The Simpsons Game | [TheSimpsonsGameRecomp](https://github.com/YesterMester/TheSimpsonsGameRecomp) `thesimpsonsgamerecomp` | `v0.0.7.1` | **B** | Pendente | Sem teste integrado |
| 116 | Dead Rising 2: Case Zero & Case West | [Dead_Rising_2_Case_Zero_Xenon_Recomp](https://github.com/wivi514/Dead_Rising_2_Case_Zero_Xenon_Recomp) `dead-rising-2-case-zero-xenon-recomp` | `v1.1.3` | **B** | Pendente | Sem teste integrado |
| 117 | Dead Rising 2: Case Zero & Case West | [Dead_Rising_2_Case_West_Xenon_Recomp](https://github.com/wivi514/Dead_Rising_2_Case_West_Xenon_Recomp) `dead-rising-2-case-west-xenon-recomp` | `v1.1.2` | **B** | Pendente | Sem teste integrado |
| 118 | Dead or Alive Xtreme Beach Volleyball | [doaxvb-re](https://github.com/NoRain211/doaxvb-re) `doaxvb-re` | `v0.8.0` | **B** | Pendente | Sem teste integrado |
| 119 | 3 on 3 NHL Arcade | [3on3NHL-recomp](https://github.com/Wndwsqrrl/3on3NHL-recomp) `3on3nhl-recomp` | `v0.1.1` | **B** | Pendente | Sem teste integrado |


## Detalhamento técnico e divergências

A tabela acima lista **todos** os IDs reais. A lista seguinte associa a classificação à evidência técnica e ao pacote Windows identificado (quando houver). A ausência de um ativo Windows nesta tabela significa que ele não foi confirmado na tag selecionada, não necessariamente que o projeto nunca publicou um.

| ID do projeto | Pacote de Release / distribuição | Motivo da classificação |
|---|---|---|
| `ghostship` | `Nautilus-Alfa-Win64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `sm64coopdx-super-mario-64-coop-deluxe` | `sm64coopdx_Windows.zip` | Receita v3 já publicada; importação da ROM US e lançamento testados anteriormente pelo usuário |
| `sm64plus` | `SM64Plus.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `render96ex` | `não confirmado` | Exige compilação, empacotamento, instalador específico ou operação não prevista pelo SDK 1.1 |
| `sm64ex` | `não confirmado` | Exige compilação, empacotamento, instalador específico ou operação não prevista pelo SDK 1.1 |
| `sm64rt` | `não confirmado` | Exige compilação, empacotamento, instalador específico ou operação não prevista pelo SDK 1.1 |
| `ship-of-harkinian-soh` | `SoH-Dewey-Bravo-Win64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `zelda-64-recompiled` | `Zelda64Recompiled-v1.2.2-Windows.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `2-ship-2-harkinian-2s2h` | `2Ship-Battler-Bravo-Win64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `starship` | `Starship-Barnard-Alfa-Windows.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `spaghettikart` | `spaghetti-windows.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `mariokart-64-recompiled` | `MarioKart64Recompiled-v0.9.2-Windows-RelWithDebInfo.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `battleship` | `BattleShip-JP-windows.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `paperboat` | `Paperboat-Mulberry-Delta-Win64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `donkey-kong-64-recompiled-dk64-rekongpiled` | `DK64Recompiled-Windows-Release-1-0-3.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `snap64-recomp` | `Snap64Recomp-1.1.8-win64.zip` | Pacote da Release identificado; instalação, dependências e lançamento ainda não homologados |
| `drmario64-recomp-plus` | `Dr.Mario.64.Recompiled-v1.0.0-Windows.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `drmario64-recomp` | `não confirmado` | Exige compilação, empacotamento, instalador específico ou operação não prevista pelo SDK 1.1 |
| `banjo-recompiled` | `BanjoRecompiled-v1.0.2-Windows.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `lighthouse` | `Lighthouse-Montauk-Charlie-Win64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `banjo-tooie-recompiled` | `BanjoTooieRecompiled-windows-x64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `perfect-dark-pc-port-perfect-dark` | `pd-i686-windows.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `project-midas` | `ProjectMidas-v1.0.2b-windows.zip` | Releases encontradas, mas README padrão retornou 404; fluxo de execução não homologado |
| `goldeneye-007-pc-port` | `goldeneye-pc-port-0.5.0-win64.zip` | Caminho data/ge007.ntsc-final.z64, SHA-1 da ROM e EXE da Release verificados; falta teste com ROM original |
| `dinosaur-planet-recompiled-dino-recomp` | `DinosaurPlanetRecompiled-v0.3.0-Windows-x64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `bm64recomp` | `BM64Recompiled-Windows-RelWithDebInfo.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `bmherorecomp` | `BMHeroRecompiled-Windows-RelWithDebInfo.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `goemon64recomp` | `Goemon64Recompiled-Windows-RelWithDebInfo.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `ggarecomp` | `GGARecompiled-v0.3.0-windows.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `gga64recomp` | `GGA64Recompiled-Windows-Debug.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `dnzhrecomp` | `DNZHRecompiled-0.0.3-Windows-RelWithDebInfo.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `adam-s-ant-farm` | `adams-ant-farm-windows-x86_64-v0.11.14.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `body-harvest-recomp` | `body-harvest-recomp-0.1.0-windows-x64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `sssv-recomp` | `SSSVRecompiled_v0.2.0_Windows.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `quest64-recomp` | `Quest64Recompiledv0.1.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `megaman64recompiled` | `MegaMan64Recompiled-v0.9.1-Windows.zip` | Pacote da Release identificado; instalação, dependências e lançamento ainda não homologados |
| `battletanx-global-assault-pc-port` | `BattleTanxGA-0.2.5-windows-x64-portable.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `btgarecomp` | `BattleTanxGARecompiled-0.1.13-windows.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `snowboardkids2-recomp` | `SnowboardKids2Recompiled-Windows.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `extremegrecomp` | `não confirmado` | GitLab; a descoberta de releases do host é GitHub, exige suporte genérico a outras origens |
| `rocket-r` | `Rocket-R-1.0.1-Windows-x64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `chameleontwist1-jp-recomp` | `ChameleonTwistJPRecompiled.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `automobililamborghini-recomp` | `lamborghini-recomp-windows-x64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `wcwvsnwoworldtourrecomp` | `WCWRecompiled-v0.3.2-Windows.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `wcwnworevengerecomp` | `RevengeRecompiled-v0.3.2-Windows.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `wwfwrestlemania2000recomp` | `Wm2kRecompiled-v0.3.2-Windows.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `vpw64recomp` | `Vpw64Recompiled-v0.3.2-Windows.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `wwfnomercyrecomp` | `NoMercyRecompiled-v0.3.2-Windows.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `bluewake` | `BlueWake-v0.12.0-windows-x64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `wind-waker-recomp` | `não confirmado` | README encaminha para BlueWake, mas IDs e repositórios do catálogo não coincidem |
| `zeldawwhdrecomp` | `WindWakerHD-v0.5.1-windows-x86_64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `dusklight-ex-dusk` | `Dusklight-v2.0.3-win32-x86_64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `twilight-princess-courage-reborn` | `não confirmado` | Catálogo aponta reportagem; release pública utilizável não identificada |
| `foxhollow` | `não confirmado` | README usa launcher baixado de site externo; não há ZIP Windows oficial associado à release GitHub |
| `nookery-ex-acgc-pc-port` | `Nookery-v1.0.0-windows-x86_64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `open-nectar` | `nectar-windows.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `metaforce` | `não confirmado` | Repositório AxioDL/metaforce retornou 404 na consulta de API |
| `strikers` | `strikers-windows-x86_64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `strikersrecomp` | `não confirmado` | Exige compilação, empacotamento, instalador específico ou operação não prevista pelo SDK 1.1 |
| `recharged` | `recharged-1.1.7+g053746ffc142-windows-x86_64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `strikers-wiicompiled` | `não confirmado` | Compilação via build.cmd e conversão de ISO; falta operação segura de build |
| `mariokartdd-recomp` | `não confirmado` | Processo de compilação/decompilação e ISO não coberto por operação declarativa |
| `mkdd-recomp` | `não confirmado` | Exige compilação, empacotamento, instalador específico ou operação não prevista pelo SDK 1.1 |
| `doldecomp-mkdd-decompilacao-base` | `não confirmado` | Exige compilação, empacotamento, instalador específico ou operação não prevista pelo SDK 1.1 |
| `zelda3` | `zelda3_v0.3.zip` | Port requer extrair recursos da ROM e compilar localmente |
| `zelda-3-launcher` | `Zelda_3_Launcher_v1.3.7.0.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `super-metroid-launcher` | `Super_Metroid_Launcher_v1.0.1.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `sm` | `não confirmado` | Exige compilação, empacotamento, instalador específico ou operação não prevista pelo SDK 1.1 |
| `sm-rewrite` | `não confirmado` | Exige compilação, empacotamento, instalador específico ou operação não prevista pelo SDK 1.1 |
| `supermarioworldrecomp` | `SuperMarioWorldRecomp-windows-x64-v0.15.11.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `smw` | `smw_0.1.zip` | Port requer extrair recursos da ROM e compilar localmente |
| `phase-distorter` | `Phase-Distorter-0.5-windows-x86_64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `autotmc-auto-tmc` | `AutoTMC-Windows.exe` | EXE/launcher requer ambiente externo e Python; não há contrato genérico de instalação executável |
| `project-picori-999sian-tmc` | `não confirmado` | Catálogo aponta perfil GitHub, não o repositório específico 999sian/tmc; requer correção da origem no catálogo |
| `tmc-decompilacao-base` | `não confirmado` | Repositório de decompilação, não pacote independente pronto para o motor |
| `gsrecomp` | `GoldenSunRecompiled-0.8.4-windows.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `opengoal` | `opengoal-lsp-windows-v0.3.9.exe` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `god-of-war-native-pc-port-gow-pc-port` | `God-Of-War-PC-Launcher_0.4.0_x64-portable.zip` | Distribuição inclui instalador/launcher com processo próprio; execução controlada não contemplada pelo schema v3 |
| `shadow-of-rome-recompiled` | `ShadowOfRome-2.9.5-windows.zip` | Geração de executável a partir de imagem de disco e etapas locais de build |
| `symphonyrecomp` | `SymphonyRecomp-v1.2.0p-windows-x64.zip` | Compilação/geração de código por scripts e ferramentas externas; não aceita execução arbitrária |
| `crash-team-racing-high-octane` | `ctr-high-octane-x64.win.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `crash-team-racing-turbocharged` | `não confirmado` | Compilação x86 e ferramentas de decompilação externas |
| `ctr-native` | `ctr-native-beta-7_1-windows-x86.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `wipeout-phantom-edition` | `wipeout-x64-release.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `wipeout-rewrite` | `não confirmado` | Exige extração múltipla de dados PS1/PC e estrutura externa; sem release Windows homologada |
| `redriver2` | `REDRIVER2_Win32_Release.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `severed-chains` | `Severed_Chains_Windows.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `silent-hill-native-pc-port` | `SilentHill_UWP_0.1.4.0_x64.appx` | Release APPX/UWP exige instalação de pacote Windows não suportada pelas operações atuais |
| `vandalhearts-pcport` | `VandalHearts-v2.1.0-windows-x64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `bloodyroar2recomp` | `BloodyRoar2-v0.7.1.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `knowyourrolerecomp` | `KnowYourRole-win-x64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `kf1-enhanced` | `KingsFieldEnhanced-v0.1.0-pre.3-windows.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `yu-gi-oh-forbidden-memories-recompiled` | `fm-editor-v0.3.0-windows.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `trx-tomb-raider-i-iii-community-edition` | `TRX-1.12-Windows_Installer.exe` | Pacote da Release identificado; instalação, dependências e lançamento ainda não homologados |
| `openlara` | `OpenLara_win.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `mega-man-legends-modernization-project` | `MML-Setup.exe` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `mml1-megaman-legends-decomp` | `não confirmado` | Exige compilação, empacotamento, instalador específico ou operação não prevista pelo SDK 1.1 |
| `unleashedrecomp` | `UnleashedRecomp-Windows.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `marathon-recompiled` | `MarathonRecomp-Windows-x64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `shadow-recompiled` | `ShadowRecomp-Windows-x64-v1.0.1-PDB.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `sarecomp-sonic-adventure-recompiled` | `SonicAdventureRecompiled-0.52.0-Windows.exe` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `rsdkv4-decompilation` | `v4-windows-x64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `sonic-1-forever-sonic-2-absolute` | `não confirmado` | Distribuição externa Team Forever sem release GitHub vinculada pelo catálogo |
| `sonic-3-a-i-r-oxygen-engine` | `artifacts.7z` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `cannonball` | `cannonball-v034-w64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `pinyon-shift` | `host-objects-0.9.5-windows-x64-base.zip` | Pipeline ISO e comandos PowerShell; operações v3 não executam conversão externa |
| `re-blue` | `reblue-1.4.0-dev-187173d8-44b7fdc5-win-amd64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `the-darkness-recomp` | `The-Darkness-Recomp-v0.1.10-windows-x64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `downpourrecomp` | `DownpourRecomp-v1.1.8.zip` | Pacote da Release identificado; instalação, dependências e lançamento ainda não homologados |
| `dprecomp` | `DPRecomp-2.0.14-win64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `project8recomp` | `Project8Recomp-v0.3.0-windows-x86_64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `project-2099` | `EOT-PC-Payload-v2.0.0-beta.4.1.zip` | Release disponível é Android APK, sem pacote Windows validado |
| `king-kong-recompiled` | `KingKong-v2.1.3-windows-x64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `earthworm-jim-hd-recompiled` | `EarthwormJimHD-v0.9.6-windows-x64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `thesimpsonsgamerecomp` | `TheSimpsonsGame-Recompiled-Windows-x64-NoAVX2.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `dead-rising-2-case-zero-xenon-recomp` | `CaseZeroRecomp-windows-x86_64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `dead-rising-2-case-west-xenon-recomp` | `CaseWestRecomp-windows-x86_64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `doaxvb-re` | `DOAXBV-0.8.0.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |
| `3on3nhl-recomp` | `3on3NHL-recomp-v0.1.1-win64.zip` | Pacote Windows identificado; recursos originais ou configuração inicial não integrados e não testados |


## Regras de aprovação

A entrada `validated` só será usada após verificar pacote, dependências, entrada original legítima, status `Completed`, binário íntegro e execução do jogo. O teste estático de JSON ou a existência de um arquivo ZIP **não** é suficiente. Candidatas `experimental` não são anunciadas como versões compatíveis pelo motor `RemoteRecipeCatalog.FindAsync`.

As operações `import_input` em `installation` usam caminhos relativos à pasta extraída sob a preferência do AllFix. Não criam seletor próprio nem sobrescrevem a preferência Padrão/Perguntar sempre. Operações sobre `roaming_app_data` são tratadas separadamente e exigem confirmação do host. 

Todos os arquivos originais permanecem sob controle do usuário; não publicar nem redistribuir ROMs, BIOS, ISO, dados de discos ou arquivos proprietários.
