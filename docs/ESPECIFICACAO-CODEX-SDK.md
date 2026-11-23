# Especificação Técnica para o Codex — Evolução do All-Fix SDK e Motor (`AllFix.dll`)

Este documento consolida todas as limitações reais do **All-Fix SDK 1.2.0** e do motor `AllFix.dll` verificadas durante a reavaliação completa dos **119 projetos** do catálogo `AllFix-Repo`. Nenhum arquivo do All-Fix, SDK ou `AllFix-Repo` foi modificado neste repositório; todas as alterações necessárias no motor são detalhadas abaixo para implementação pelo Codex.

---

## 1. Caminhos relativos com espaços em `recipe.json` (`IsSafeRelativePath`)

- **Projetos afetados (10 bloqueados diretamente + 2 bloqueios combinados):**
  - Bloqueios primários por espaços em executável ou diretório raiz: `sm64plus`, `drmario64-recomp-plus`, `zelda-3-launcher`, `super-metroid-launcher`, `phase-distorter`, `gsrecomp`, `crash-team-racing-high-octane`, `zeldawwhdrecomp`, `god-of-war-native-pc-port-gow-pc-port`.
  - Bloqueios combinados com faixas PS1 contendo espaços e parênteses: `wipeout-phantom-edition`, `symphonyrecomp`.
- **Comportamento necessário:** Permitir espaços internos (U+0020) e parênteses seguros nos caminhos declarados em `required_files`, `launch_file`, `operations[].target`, `inputs[].verify_file` e `first_run_files[].path`, mantendo bloqueio de travessia (`..`), caminhos absolutos, separadores `\`, dois-pontos (`:`), nomes reservados do Windows (`CON`, `PRN`, `AUX`, `NUL`, `COM1..9`, `LPT1..9`) e espaços nas extremidades de segmentos.
- **Limitação atual:** O validador `IsSafeRelativePath` em `StoreAddonProviders` e os JSON Schemas v1–v4 restringem caminhos declarados ao padrão `[a-zA-Z0-9_.+-]` sem espaços nem parênteses, embora o teste empírico realizado em `GameInstallationService.Run` na `AllFix.dll` comprove que `extract_archive` já extrai sem falhas arquivos auxiliares do ZIP que contêm espaços (permitindo `strikers`, `dprecomp` e `3on3nhl-recomp` via executável secundário sem espaços).
- **Evidências verificáveis (ZIPs oficiais inspecionados estaticamente):**
  - `sm64plus` (`MorsGames/sm64plus`, `LauncherMirror`): `SM64Plus.zip` (`6617082` bytes, SHA-256 `f3f930a822c80694fbb7faf0c82cea2b14290b83bad2e9823ff2f2433e46fdb7`) → executável `Super Mario 64 Plus.exe`.
  - `drmario64-recomp-plus` (`theboy181/drmario64_recomp_plus`, `1.0.0`): `Dr.Mario.64.Recompiled-v1.0.0-Windows.zip` (`24225142` bytes, SHA-256 `ba749f48725e23636845c9a79a89e17859172ac80fa7b98bf4523d12c1f0d2cf`) → pasta raiz `Dr. Mario 64 Recompiled x64-Release/drmario64_recomp.exe`.
  - `zelda-3-launcher` (`RadzPrower/Zelda-3-Launcher`, `v1.3.7.0`): `Zelda_3_Launcher_v1.3.7.0.zip` (`3792896` bytes, SHA-256 `2a92fc4e636b8ac008a3a1b31d8bbe7866bcdbc85622152bf36f9ea28d1c2cfc`) → `Zelda 3 Launcher.exe`.
  - `super-metroid-launcher` (`RadzPrower/Super-Metroid-Launcher`, `v1.0.1`): `Super_Metroid_Launcher_v1.0.1.zip` (`2092800` bytes, SHA-256 `06b4a698f5ec5ddebba55fb5464a9966b37f104c931f5ce7f799baf5db03b3c4`) → `Super Metroid Launcher.exe`.
  - `phase-distorter` (`TheRunaway5/Phase-Distorter`, `0.5`): `Phase-Distorter-0.5-windows-x86_64.zip` (`14353099` bytes, SHA-256 `195d8b2fa4a05753d5330fef4d9030939074763ff3bedc41c5dcc2d9181b28ad`) → `Phase-Distorter-0.5-windows-x86_64/Phase Distorter.exe`.
  - `crash-team-racing-high-octane` (`Rinnegatamante/Crash-Team-Racing-High-Octane`, `v.1.5`): `ctr-high-octane-x64.win.zip` (`2403121` bytes, SHA-256 `005924af516a3cb2bcdc19269422e2de77719600656e5b00df45424fe081693e`) → `Crash Team Racing - High Octane.exe`.
  - `zeldawwhdrecomp` (`ZeldaWWHDRecomp/ZeldaWWHDRecomp`, `v0.5.1` em assets Windows): `WindWakerHD-v0.5.1-windows-x86_64.zip` (`41201612` bytes, SHA-256 `2e8a8b29ed1b35e6d3cae370a7c9b6878a05d6269b28420dd492415da72f48c4`) → `WindWakerHD-v0.5.1-windows-x86_64/Wind Waker HD.exe`.
- **Alteração mínima necessária no SDK / motor:**
  - Introduzir `schema_version: 5` (ou evolução compatível) relaxando a regex de segmentos em `IsSafeRelativePath` e nos JSON Schemas para permitir espaço único interno e `()` quando o segmento não começa nem termina com espaço/ponto.
  - Garantir escaping com aspas seguras ao passar `launch_file` para `ProcessStartInfo` e normalização consistente na checagem de `required_files`.
- **Critérios de aceitação e testes sugeridos:**
  - `StoreAddonProviders.ParseRecipe` deve aceitar `"Super Mario 64 Plus.exe"`, `"Dr. Mario 64 Recompiled x64-Release/drmario64_recomp.exe"` e `"wipeout/Wipeout (USA) (Track 1).bin"`.
  - `StoreAddonProviders.ParseRecipe` deve continuar rejeitando `"../evil.exe"`, `"dir/ "` (espaço no fim), `"CON.exe"` e `"a/b\\c.exe"`.
  - Teste de integração com `GameInstallationService.Run` extraindo ZIP sintético com executável contendo espaço e verificando `Destination/<exe>` no disco.

---

## 2. Validação criptográfica por `sha1` isolado ou `md5` em `inputs` e alinhamento de `import_input`

- **Projetos afetados (redução de etapas manuais em >15 receitas experimentais + desbloqueio direto de automação):**
  - Apenas `SHA-1` oficial (sem `size` em bytes nem `SHA-256` publicados no upstream): `snap64-recomp` (antes da confirmação via `splat.yaml`), `ship-of-harkinian-soh`, `zelda-64-recompiled`, `2-ship-2-harkinian-2s2h`, `starship`, `spaghettikart`, `mariokart-64-recompiled`, `lighthouse`, `donkey-kong-64-recompiled-dk64-rekongpiled`, `king-kong-recompiled`, e diversos `N64Recomp` (`bm64recomp`, `bmherorecomp`, `goemon64recomp`, `ggarecomp`, `sssv-recomp`, `quest64-recomp`, `megaman64recompiled`, `snowboardkids2-recomp`, `chameleontwist1-jp-recomp`, `automobililamborghini-recomp`).
  - Apenas `MD5` oficial publicado pelo projeto: `perfect-dark-pc-port-perfect-dark` (PD NTSC 1.1 `MD5: e03b088b6ac9e0080440efed07c1e40f`), `opengoal`.
- **Comportamento necessário:**
  1. Aceitar `inputs[]` com `{ "sha1": "<40 hex>" }` (sem exigir `size` + `magic_hex` nem `sha256`), mantendo força criptográfica mínima.
  2. Suportar campo opcional `"md5": "<32 hex>"` (preferencialmente combinado com `size` > 0 + `magic_hex`) para casos onde o projeto oficial só publica MD5.
  3. Garantir paridade total entre JSON Schema e `StoreAddonProviders.ParseRecipe` para `import_input` (hoje o JSON Schema v3 aprova `size + magic_hex` sem `sha1`/`sha256`, mas a `AllFix.dll` lança `InvalidDataException: Operação incompatível.` ao parsing de `import_input` se faltar `sha1` ou `sha256`).
- **Evidências verificáveis:**
  - Em `AllFix.dll` (`StoreAddonProviders.ParseRecipe`), a tentativa na Rodada 3 de importar ROM do `perfect-dark-pc-port-perfect-dark` (`size: 33554432`, `magic_hex: "80371240"`, sem `sha1`/`sha256` porque o README oficial publica apenas MD5) falhou com `InvalidDataException: Operação incompatível.`.
  - O README de `TekRantGaming/king-kong-recompiled` publica `SHA-1: 075F43709E9C9A095E099AB5056CC04B768288D1` para a ISO de `7834892288` bytes.
- **Alteração mínima necessária no SDK / motor:**
  - Atualizar a cláusula `oneOf` / `anyOf` do schema de `inputs` para aceitar `required: ["sha1"]` e adicionar `"md5"` com cálculo em `ValidateSelectedInput` / `PrepareImport` usando `System.Security.Cryptography.MD5` (além de `SHA1` e `SHA256`).
- **Critérios de aceitação e testes sugeridos:**
  - Teste unitário em `StoreAddonProviders.ParseRecipe` aceitando `import_input` apontando para entrada com apenas `sha1` (40 hex) ou com `(md5, size, magic_hex)`.
  - Teste negativo garantindo rejeição de entradas sem nenhum identificador forte (`size` sem `magic_hex`/`sha1`/`sha256`/`md5`).

---

## 3. Escopo `local_app_data` (`%LOCALAPPDATA%`) e verificador flexível em `first_run_files`

- **Projetos afetados:** `phase-distorter` (gera assets em `%APPDATA%`/`%LOCALAPPDATA%`), ports `N64Recomp` sem `portable.txt` (`zelda-64-recompiled`, `mariokart-64-recompiled`, `starship`, `spaghettikart`) e gerações de `.o2r`/`.otr` cujo tamanho/hash final varia entre execuções (`ship-of-harkinian-soh`, `2-ship-2-harkinian-2s2h`, `ghostship`).
- **Comportamento necessário:**
  - Suportar `"scope": "local_app_data"` além de `"installation"` e `"roaming_app_data"`.
  - Permitir verificação de presença e integridade não exclusivamente por SHA-256 exato em `first_run_files` (por exemplo: extensão obrigatória + `min_size` + cabeçalho/`magic_hex` para archives `.o2r`/`.otr` reempacotados localmente).
- **Limitação atual:** `import_input.scope` no schema v3/v4 aceita apenas `installation` e `roaming_app_data`; `first_run_files` exige lista estática de `(path, size, sha256)` exatos na pasta instalada.
- **Alteração mínima necessária no SDK / motor:**
  - Adicionar `"local_app_data"` ao enum de `scope` usando `Environment.SpecialFolder.LocalApplicationData`.
  - Adicionar `first_run_patterns` ou tornar `sha256` opcional quando `min_size` + `magic_hex` estiverem presentes em `first_run_files`.
- **Critérios de aceitação e testes sugeridos:**
  - Teste de instalação validando importação segura em subpasta restrita sob `LocalApplicationData` sem escapar por travessia `..`.
  - Teste pós-execução (`RecheckFirstRun`) validando arquivo `.o2r` sintético pelo cabeçalho ZIP (`504B0304`) e `min_size`.

---

## 4. Seleção multi-arquivo de discos PS1/arcade, XBLA LIVE e diretórios sem SHA-256 fixo

- **Projetos afetados (4 bloqueados + 5+ experimentais com passos manuais):**
  - Bloqueados diretos: `wipeout-phantom-edition`, `redriver2`, `vandalhearts-pcport`, `cannonball` (+ `symphonyrecomp`).
  - Experimentais limitados a guia manual: `the-darkness-recomp`, `earthworm-jim-hd-recompiled`, `dead-rising-2-case-zero-xenon-recomp`, `dead-rising-2-case-west-xenon-recomp`, `3on3nhl-recomp`.
- **Comportamento necessário:**
  1. Permitir `kind: "directory"` ou `"input_set"` flexível baseado em extensão/padrão + assinaturas internas (ou verificação parcial) em vez de exigir todos os SHA-256 exatos antecipadamente em `import_input_set` v4.
  2. Para pacotes XBLA `LIVE`/`PIRS` (cujo cabeçalho contém licença individual do proprietário alterando o SHA-256 do contêiner externo, conforme documentado em `TekRantGaming/earthworm-jim-hd-recompiled`), permitir seletor de diretório/arquivo por `magic_hex` (`4C495645` `"LIVE"` / `50495253` `"PIRS"`) e `min_size`, opcionalmente verificando o `default.xex` após descompactação pela própria ferramenta oficial.
- **Evidências verificáveis:**
  - `wipeout-phantom-edition` (`v1.2.256`): `wipeout-x64-release.zip` (`3619822` B, SHA-256 `f63eca6d14ca4995083b2127fb8912d94a58437791da843e0899522c8664fb23`) requer 9 trilhas `.bin` + `.cue` com nomes espaciais (`Wipeout (USA) (Track 1).bin`..).
  - `vandalhearts-pcport` (`v2.1.0`): `VandalHearts-v2.1.0-windows-x64.zip` (`5771542` B, SHA-256 `365c7515e59f705ccb5942ab77270f0f9b98dbd3716e492d95266c226355868d`) requer imagem BIN/ISO PS1 em `game/` sem SHA-256 publicado no `SHA256SUMS.txt` (o `SHA256SUMS.txt` cobre apenas o próprio ZIP e o HD pack).
  - `cannonball` (`v0.34`): `cannonball-v034-w64.zip` (`790148` B, SHA-256 `2545d9b10cb10ed66bc5dc07aa5290577aa911370e79f06fafa5b561a846e303`) exige múltiplos arquivos ROM MAME (OutRun rev B) em `roms/` sem lista oficial de tamanhos e SHA-256.
  - `redriver2` (`8.0`): `REDRIVER2_Win32_Release.zip` (`9364906` B, SHA-256 `ddc0106858ad91c36cce8d305d0547c5601a57f6d8f0e82d71ef5a76b4b84e05`) exige Launcher externo em Java + dois discos CD1/CD2.
  - `earthworm-jim-hd-recompiled` (`v0.9.6`): `README.md` informa explicitamente que `8510D3A10187458FD69203D1E4067E736923865658` (`455823360` B) possui cabeçalho `LIVE` único por conta, mantendo SHA-1 fixo apenas no `default.xex` extraído (`62D9D28A3BCE42843607C26AB4B200E91CB31203`).
- **Alteração mínima necessária no SDK / motor:**
  - Introduzir modo `"match": "directory_copy"` ou `"pattern_glob"` em `inputs[]` v5 com verificação por `magic_hex` + `size_range`, sem depender de tabela fixa `sha256` por trilha.
- **Critérios de aceitação e testes sugeridos:**
  - Importação controlada de pasta com múltiplos `.bin`/`.cue` preservando extensão e subdiretório destino sem falha de permissão ou bloqueio artificial de parênteses/espaços.

---

## 5. Instaladores `.exe`, ambientes de runtime (`.NET 10`, Java) e pipelines locais de compilação

- **Projetos afetados (23 projetos):**
  - Instaladores/executáveis avulsos sem `.zip` portátil (4): `mega-man-legends-modernization-project` (`MML-Setup.exe`), `sarecomp-sonic-adventure-recompiled` (`SonicAdventureRecompiled-*-Windows.exe`), `project-2099` (`Project2099-Beta5-Setup.exe` + `Payload.zip` 1,36 GB), `autotmc-auto-tmc` (`AutoTMC-Windows.exe` v1.0.2).
  - Launcher baseado em Java / `.bat` ou dependência de runtime externo (2): `severed-chains` (`Severed_Chains_Windows.zip`, `131446655` B, SHA-256 `164716cba1899cadf834506636de8da56721d695457c3b53c93c533999ef9bb4`, sem `.exe` na raiz), `symphonyrecomp` (`SymphonyRecomp-v1.2.0p-windows-x64.zip`, `63884901` B, SHA-256 `3d3e5f0a46896737a6a0a3bcddbc9b1b0c58e0d5f91e0de16bd44f64451ef662`, requer `.NET 10 Runtime` + `OpenAL` + `disc/` multi-faixa).
  - Kits que exigem compilação local na máquina do usuário (17): `doaxvb-re` (`DOAXBV-0.8.0.zip`, `109788899` B, SHA-256 `a4b80511a2d538b30a76358068fcc47ddb0837360b6fb952e0ef92358dd1f48c`), `pinyon-shift` (`PinyonShift-Launcher.zip`, `69162260` B, SHA-256 `6ecf1b85f22f5c31284bc22e76c79f5c08d397f9aa36cb58a8fd70bff1316af3`), `god-of-war-native-pc-port-gow-pc-port` (`God-Of-War-PC-Launcher_0.4.0_x64-portable.zip`, `19725266` B, SHA-256 `e3583f31d56d175b5aaaf34e4b89465274d77ebdac5259182ddc3a7027a29aa1`), `render96ex`, `sm64ex`, `sm64rt`, `drmario64-recomp`, `strikers-wiicompiled`, `mariokartdd-recomp`, `mkdd-recomp`, `doldecomp-mkdd-decompilacao-base`, `sm`, `sm-rewrite`, `tmc-decompilacao-base`, `crash-team-racing-turbocharged`, `wipeout-rewrite`, `mml1-megaman-legends-decomp` (destes, os 14 últimos sequer possuem releases compiladas no GitHub).
- **Comportamento necessário:**
  - Suportar arquivos `.7z` e pacotes multi-parte declarados por lista de URLs/SHA-256.
  - Permitir declaração estruturada de pré-requisitos (`prerequisites`:ex. `.NET 10 Desktop Runtime`, `OpenAL`, `Java 21+`) verificáveis antes do lançamento, além de `launch_command` para scripts `.bat`/`.cmd` assinados pelo ZIP oficial quando não houver `.exe`.
  - Para executáveis portáteis únicos (`AutoTMC-Windows.exe`) ou instaladores com modo silencioso padronizado (`/DIR=...`), operação opcional segura sem execução arbitrária de scripts não verificados.
- **Alteração mínima necessária no SDK / motor:**
  - Adicionar seção opcional `"prerequisites": [...]` (checagem passiva de runtime instalado via registro/PATH) e avaliação segura de `.bat`/`.cmd` apenas dentro da pasta de instalação ou extração direta de executável único verificado por SHA-256.
- **Critérios de aceitação e testes sugeridos:**
  - Rejeitar qualquer comando fora da pasta instalada; permitir detecção clara de ausência de `.NET 10` / `Java` em testes simulados retornando diagnóstico amigável ao usuário.

---

## 6. Descoberta multi-forja além do GitHub

- **Projeto afetado (1):** `extremegrecomp` (`extreme-g`) — hospedado em `https://gitlab.com/sonicdcer/ExtremeGRecomp/-/releases/v1.0.0`.
- **Limitação atual:** `RemoteRecipeCatalog.ValidRepository` e a descoberta remota no All-Fix exigem formato `owner/repo` do GitHub e URLs `github.com`.
- **Alteração mínima necessária no SDK / motor:** Suportar provedor opcional (`"provider": "gitlab"`, API `/api/v4/projects/.../releases`) tanto no catálogo quanto na validação de `source_url`.
- **Critérios de aceitação e testes sugeridos:** Mock HTTP simulando payload de release da API GitLab v4 resolvendo asset Windows `.zip` e SHA-256 no fluxo de descoberta.

---

## Correções no `AllFix-Repo` (fora do escopo do GetAll-Addon e do Codex SDK)

Os **5 projetos** abaixo dependem exclusivamente de atualização de metadados no catálogo oficial `brad38/AllFix-Repo` ou da publicação de primeira release pública Windows pelo autor original:

1. `metaforce` (`metroid-prime`): repositório `AxioDL/metaforce` retorna HTTP 404 na API do GitHub.
2. `wind-waker-recomp` (`the-legend-of-zelda-the-wind-waker`): aponta para `elliotttate/Wind-Waker-Recomp` (0 releases; projeto migrado oficialmente para `chrissotraidis/bluewake`, já atendido por receita).
3. `twilight-princess-courage-reborn` (`the-legend-of-zelda-twilight-princess`): catálogo aponta notícia (`pcgamer.com`) sem `github_repository` nem release pública.
4. `project-picori-999sian-tmc` (`the-legend-of-zelda-the-minish-cap`): catálogo aponta perfil `https://github.com/999sian` em vez do repositório específico do projeto.
5. `sonic-1-forever-sonic-2-absolute` (`sonic-the-hedgehog-1-2-2013`): distribuição externa em `teamforeveronline.wixsite.com` sem `github_repository`.
6. *(Release vazia no GitHub até a data da auditoria)*: `foxhollow` (`JackPriceBurns/foxhollow`, tag `v1.0.30` sem assets) e `strikersrecomp` (`aharonahdoot/StrikersRecomp`, tag `v0.1.0` sem assets).
