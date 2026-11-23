# GetAll-Addon — Plano de Execução Priorizado e Relatório da Rodada 1 (2026-11-23)

## 1. Diagnóstico do catálogo (87 jogos / 119 projetos)

Cruzando os relatórios [AUDITORIA-CATALOGO-2026-11-22.md](AUDITORIA-CATALOGO-2026-11-22.md), [RODADA-B-2026-11-23.md](RODADA-B-2026-11-23.md), [RODADA-SDK-1.2.0-2026-11-23.md](RODADA-SDK-1.2.0-2026-11-23.md) e as evidências dos repositórios oficiais:

| Grupo | Antes da Rodada 1 | Após a Rodada 1 | Situação |
|---|---:|---:|---|
| Receitas `validated` (descoberta normal no All-Fix) | 1 | 1 | `sm64coopdx-super-mario-64-coop-deluxe` (`v1.5.1`) |
| Receitas `experimental` com `inputs` verificados (`import_input`) | 1 | **12** | `goldeneye-007-pc-port`, 3 evoluídas (`ghostship`, `banjo-tooie-recompiled`, `battletanx-global-assault-pc-port`) e 8 novas |
| Receitas `experimental` apenas com `manual_steps` (`inputs: []`) | 12 | **11** | 9 anteriores + `snap64-recomp` + `battleship` (aguardando tamanho/SHA-256 ou `sha1` puro no SDK) |
| Projetos sem receita | 105 | **95** | 63 Classe B, 27 Classe C, 5 Classe D |

**Observação sobre descoberta e promoção a `validated`:** o motor `RemoteRecipeCatalog.FindAsync` do All-Fix exibe na descoberta normal apenas entradas com status `validated`. Nenhuma receita é promovida para `validated` apenas por inspeção estática — todas as novas e evoluídas permanecem `experimental` até teste funcional ponta a ponta com mídia legítima do usuário.

---

## 2. Plano de execução em 5 rodadas

1. **Rodada 1 (concluída neste PR):**
   - Publicar receitas para 10 projetos N64 com pacote Windows `.zip` inspecionado (8 com `inputs` verificados por `size` + `magic_hex` + `sha1` oficial + `import_input` para a pasta instalada; 2 com `inputs: []` por não publicarem tamanho em bytes da ROM nos documentos oficiais).
   - Evoluir receitas experimentais já existentes cujos `size`, `magic_hex` e `sha1`/`sha256` oficiais estão comprovados nos repositórios (`ghostship`, `banjo-tooie-recompiled`, `battletanx-global-assault-pc-port`), reduzindo passos manuais.
   - Documentar bloqueios técnicos exatos para o Codex e checklist de homologação `validated`.

2. **Rodada 2 — Demais N64Recomp e Decomp portáteis (18 projetos Classe B):**
   - Alvos: `mariokart-64-recompiled`, `donkey-kong-64-recompiled-dk64-rekongpiled`, `drmario64-recomp-plus`, `ggarecomp`, `adam-s-ant-farm`, `dinosaur-planet-recompiled-dino-recomp`, `bm64recomp`, `bmherorecomp`, `goemon64recomp`, `gga64recomp`, `dnzhrecomp`, `sssv-recomp`, `quest64-recomp`, `megaman64recompiled`, `snowboardkids2-recomp`, `chameleontwist1-jp-recomp`, `automobililamborghini-recomp`, `sm64plus`.
   - Critério: inspecionar os ZIPs Windows oficiais, verificar tamanho/SHA-1 em `include/`/`disasm/`/`README.md` e adotar `import_input` sempre que confirmado.

3. **Rodada 3 — PS1, SNES, GBA e PC clássicos com ZIP Windows (18 projetos Classe B):**
   - Alvos principais: `perfect-dark-pc-port-perfect-dark`, `crash-team-racing-high-octane`, `ctr-native`, `kf1-enhanced`, `bloodyroar2recomp`, `knowyourrolerecomp`, `yu-gi-oh-forbidden-memories-recompiled`, `severed-chains`, `openlara`, `supermarioworldrecomp`, `gsrecomp`, `rsdkv4-decompilation`, `zelda-3-launcher`, `super-metroid-launcher`.

4. **Rodada 4 — GameCube/Wii e Xbox 360 Recomp com ZIP Windows (25 projetos Classe B):**
   - Alvos principais: `bluewake`, `zeldawwhdrecomp`, `dusklight-ex-dusk`, `nookery-ex-acgc-pc-port`, `open-nectar`, `strikers`, `unleashedrecomp`, `marathon-recompiled`, `shadow-recompiled`, `re-blue`, `the-darkness-recomp`, `downpourrecomp`, `dprecomp`, `project8recomp`, `king-kong-recompiled`, `earthworm-jim-hd-recompiled`, `thesimpsonsgamerecomp`, `dead-rising-2-case-zero-xenon-recomp`, `dead-rising-2-case-west-xenon-recomp`, `doaxvb-re`, `3on3nhl-recomp`.

5. **Rodada 5 — Projetos dependentes de evolução do SDK (Classe B bloqueada e Classe C/D revisada):**
   - Projetos com nomes com espaço (`phase-distorter`, `wipeout-phantom-edition`), instaladores `.exe`/`.7z`/`GitLab` (`trx-tomb-raider-i-iii-community-edition`, `opengoal`, `mega-man-legends-modernization-project`, `sarecomp-sonic-adventure-recompiled`, `sonic-3-a-i-r-oxygen-engine`, `extremegrecomp`) e discos/conversões multi-arquivo (`cannonball`, `redriver2`, `vandalhearts-pcport`).

---

## 3. Resultados verificados da Rodada 1

### 3.1 Dez novas receitas publicadas (`experimental`)

| Projeto | Tag | Asset Windows | SHA-256 ZIP | `inputs` / `import_input` | Fonte oficial da ROM |
|---|---|---|---|---|---|
| `snap64-recomp` | `v1.1.8` | `Snap64Recomp-1.1.8-win64.zip` | `7045e8c056a933c28d2311a9255e3011e88ceba81360d62a13a5a0d50d7e8fc4` | `false` (aguarda tamanho/SHA-256 ou `sha1` puro no SDK) | `README.md` (`edc7c49c...`) + `src/rom_picker.cpp` (`pokemonsnap.z64`) |
| `battleship` | `v1.6` | `BattleShip-windows.zip` | `a0c2ef997e7f561dc02da19b0e1134ecb9bfaac1d577d65ff04db3c7e27eadb4` | `false` (aguarda tamanho/SHA-256 ou `sha1` puro no SDK) | `README.md` (`e2929e10...`) |
| `rocket-r` | `v.1.0.1` | `Rocket-R-1.0.1-Windows-x64.zip` | `d47ba319b8aa6bc3a348258a8cd1a5cf0f693eb129c87b2fc895d6f15dd87db1` | **`true`** (`12582912` B, `rocket-r.us.z64`) | `README.md` (`12 MiB`, `622d71a4...`) |
| `btgarecomp` | `v0.1.13` | `BattleTanxGARecompiled-0.1.13-windows.zip` | `fa64ebd1407543754fc55f7a69c335953cb02cfaeef9f93b897e3cb1be3c877e` | **`true`** (`8388608` B, `BattleTanxGA.us.z64`) | `syms/rom_info.md` + `README.md` (`08a90374...`) |
| `body-harvest-recomp` | `v0.1.0` | `body-harvest-recomp-0.1.0-windows-x64.zip` | `dd1ab059cb729f8657b2efb352e535b60fad0881eb93e11c1f7a1775c94e693b` | **`true`** (`12582912` B, `body-harvest.us.z64`) | `include/bh/rom.h` (`bbb6666f...`) |
| `wcwvsnwoworldtourrecomp` | `v0.3.2` | `WCWRecompiled-v0.3.2-Windows.zip` | `69bc8d0bc6e288bafde838c4dcbf43543fa5c1850308aba605008523b282f284` | **`true`** (`12582912` B, `wcw.z64`) | `disasm/wcw.yaml` (`5ad2d835...`) |
| `wcwnworevengerecomp` | `v0.3.2` | `RevengeRecompiled-v0.3.2-Windows.zip` | `75f5b21e9c348b17d321c39ce2bffe6ea7f19aad7d17d0ce08c0ebb03e7f4c30` | **`true`** (`16777216` B, `revenge.z64`) | `disasm/revenge.yaml` (`e1711a25...`) |
| `wwfwrestlemania2000recomp` | `v0.3.2` | `Wm2kRecompiled-v0.3.2-Windows.zip` | `eed70bc4c57fcbc0f3331414850f549f50be0b0dae0ff98b89cc58497dc8ffe5` | **`true`** (`33554432` B, `wm2k.z64`) | `disasm/wm2k.yaml` (`442d417a...`) |
| `vpw64recomp` | `v0.3.2` | `Vpw64Recompiled-v0.3.2-Windows.zip` | `71bad5632916c5725f1d143207aeba36cd6889cf6c9072f1429a8e20e0492e82` | **`true`** (`16777216` B, `vpw64.z64`) | `disasm/vpw64.yaml` (`f9e9fa2e...`) |
| `wwfnomercyrecomp` | `v0.3.2` | `NoMercyRecompiled-v0.3.2-Windows.zip` | `8cefdcca49c582dc2a7e10ea925c16d761e1b0bb6249f49e8e80eb220ccf23bd` | **`true`** (`33554432` B, `nomercy.z64`) | `disasm/nomercy.yaml` (`91cee3d0...`) |

### 3.2 Três receitas experimentais evoluídas (`inputs: false` → `true`)

- `battletanx-global-assault-pc-port` (`v0.2.5`): agora valida `8388608` B + `magic_hex` + `sha1` + `sha256` oficiais e importa `BattleTanxGA-0.2.5-windows-x64-portable/BattleTanxGA.z64`.
- `banjo-tooie-recompiled` (`v1.0.1`): agora valida `33554432` B + `magic_hex` + `sha1` oficial e importa `banjo-tooie.us.z64`.
- `ghostship` (`3.0.0`): agora valida `8388608` B + `magic_hex` + `sha1` oficial e importa `baserom.us.z64` (detectado automaticamente por `GameExtractor.cpp`).

---

## 4. Novos bloqueios específicos documentados para o Codex

Além dos itens já descritos em [CAPACIDADES-PENDENTES-2026-11-22.md](CAPACIDADES-PENDENTES-2026-11-22.md) e [RODADA-SDK-1.2.0-2026-11-23.md](RODADA-SDK-1.2.0-2026-11-23.md), a Rodada 1 identificou estas limitações concretas no SDK 1.2.0:

1. **Validação de entrada apenas por `sha1` (sem `size` nem `sha256`):**
   - `installation-recipe-v3.schema.json` exige `sha256` **ou** `(size + magic_hex)` mesmo quando `sha1` está preenchido.
   - Projetos como `Snap64Recomp`, `BattleShip`, `Starship`, `SpaghettiKart`, `PaperBoat` e `Lighthouse` documentam oficialmente apenas o `SHA-1` (sem `size` em bytes nem `SHA-256` publicados). Permitir `{ "required": ["sha1"] }` (opcionalmente combinado com `magic_hex`) desbloqueia `import_input` direto com verificação criptográfica forte para todos eles — especialmente `Snap64Recomp`, onde o executável já lê `pokemonsnap.z64` sem nenhum passo manual.
2. **Suporte a `md5` em `inputs`:**
   - Projetos como `Perfect Dark PC Port` e `OpenGOAL` publicam apenas hashes `MD5` das imagens originais em seus READMEs.
3. **Escopo `local_app_data` (`%LOCALAPPDATA%`) em `import_input`:**
   - O schema v3 oferece apenas `installation` e `roaming_app_data` (`%APPDATA%`), enquanto vários ports `N64Recomp` armazenam configurações e ROMs copiadas em `%LOCALAPPDATA%` quando não há `portable.txt`.
4. **Caminhos com espaços e arquivos `.exe`/`.7z`:**
   - Mantém `Phase Distorter.exe`, `WipeOut` e pacotes `.7z`/instaladores (`opengoal`, `sonic-3-a-i-r-oxygen-engine`, `trx-tomb-raider-i-iii-community-edition`) dependentes do motor.

---

## 5. Candidatas prioritárias à homologação funcional (`validated`)

Para promover receitas de `experimental` para `validated`, é necessário teste ponta a ponta no `AllFix.exe` com uma cópia legítima do usuário:

1. **`goldeneye-007-pc-port` (`v0.5.0`):** já estruturada como Classe A (`has_inputs: true`, `has_manual_steps: false`); falta apenas validar importação da ROM US (`abe01e4aeb033b6c0836819f549c791b26cfde83`) e lançamento do jogo.
2. **`snap64-recomp` (`v1.1.8`):** já lê `Snap64Recomp-1.1.8-win64/pokemonsnap.z64` automaticamente sem diálogo; assim que confirmado o `size` / `sha256` oficial de `pokemonsnap.z64` com uma ROM legítima e testado o boot, passa direto a Classe A `validated`.
3. **As 11 receitas experimentais com `import_input` (`ghostship`, `battletanx-global-assault-pc-port`, `banjo-tooie-recompiled`, `rocket-r`, `btgarecomp`, `body-harvest-recomp`, e os 5 jogos AKI):** testar importação da ROM pelo All-Fix, comportamento no primeiro lançamento e eventual adoção de `first_run_files` (SDK v4) onde houver arquivo determinístico gerado na pasta instalada.
