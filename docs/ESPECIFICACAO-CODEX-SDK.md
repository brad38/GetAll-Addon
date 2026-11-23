# Especificação Técnica para o Codex — Evolução do All-Fix SDK e Motor (`AllFix.dll`)

Este documento consolida as capacidades já entregues pelo Codex no **All-Fix SDK 1.3.0** (`schema_version: 5`) e as limitações reais ainda pendentes para desbloquear os **29 projetos restantes** e ampliar a automação dos **90 projetos** com receita no catálogo `AllFix-Repo`. Nenhum arquivo do All-Fix, SDK ou `AllFix-Repo` é modificado neste repositório.

---

## Itens já entregues no SDK 1.3.0 (`schema_version: 5`) — Rodada 7

Os requisitos abaixo da versão anterior desta especificação foram implementados na `AllFix.dll` 1.3.0 e convertidos em **14 novas receitas `v5`** (`90/119` projetos cobertos):

1. **Caminhos relativos com espaços internos, `()` e `+`:** desbloqueou `sm64plus`, `drmario64-recomp-plus`, `zelda-3-launcher`, `super-metroid-launcher`, `phase-distorter`, `gsrecomp`, `crash-team-racing-high-octane`, `zeldawwhdrecomp`, `wipeout-phantom-edition` e `symphonyrecomp`.
2. **Suporte multi-forja para GitLab (`gitlab:<grupo>/<projeto>` e Package Registry):** desbloqueou `extremegrecomp` (`gitlab:sonicdcer/ExtremeGRecomp`, tag `v1.0.0`).
3. **Validação flexível em `inputs[]` v5 (`sha1` isolado, `md5 + size + magic_hex`, `magic_hex + size/min_size`) e XBLA `LIVE`/`PIRS`:** permitiu importação verificada em `vandalhearts-pcport` (`min_size` + `max_size` + `magic_hex`) sem SHA-256 fixo por região.
4. **Escopo `local_app_data` e `first_run_files` por `min_size` + `magic_hex` + `profile_folder`:** disponível para ports com cache/perfil fora da pasta instalada.
5. **Declaração passiva de `prerequisites` (`dotnet-desktop-10-x64`, `java-21`, `openal-x64`, `openal-x86`):** permitiu declarar requisitos oficiais em `symphonyrecomp` (`dotnet-desktop-10-x64`, `openal-x64`) e `redriver2` (`java-21`).

---

## Capacidades ainda necessárias ao Codex para os 29 bloqueios restantes e automação

### 1. Extensões adicionais e validação criptográfica em `import_input` (`AllFix.dll`)

- **Limitação real verificada na `AllFix.dll` 1.3.0:**
  - Durante a verificação real da Rodada 7, `StoreAddonProviders.ParseRecipe` rejeitou `zelda-3-launcher` e `super-metroid-launcher` ao tentar importar `zelda3.sfc` / `sm.sfc` via `import_input`, lançando `InvalidDataException: O destino da importação precisa ser um arquivo de dados.`. Embora o JSON Schema `v5` permita qualquer `$defs/path` no escopo `installation`, o código C# da `AllFix.dll` restringe extensões de destino.
  - Em receitas `v3`/`v4`, `import_input` ainda exige `sha256` ou `sha1`, e `inputs` baseados apenas em `size + magic_hex` continuam bloqueados fora de `v5`.
- **Projetos impactados (automação adicional sobre receitas já existentes):** `zelda-3-launcher` (`zelda3.sfc`), `super-metroid-launcher` (`sm.sfc`), `zelda3` (`zelda3.sfc`), `smw` (`smw.sfc`), `gsrecomp` (`.gba`), `perfect-dark-pc-port-perfect-dark` (migração opcional para `v5` usando `md5`).
- **Alteração necessária no motor:** ampliar a lista branca de extensões em `import_input` (`installation`) para incluir ROMs e imagens de cartucho/CD comuns (`.sfc`, `.smc`, `.gba`, `.gbc`, `.gb`, `.nds`, `.chd`, `.iso`, `.cue`, `.rvz`) além das atuais.
- **Critério de aceitação:** `StoreAddonProviders.ParseRecipe` e `GameInstallationService.Run` devem aceitar `import_input` para `zelda3.sfc` e `sm.sfc` com `sha256` verificado no escopo `installation`.

---

### 2. Executáveis portáteis avulsos (`.exe` direto), instaladores sem elevação e pacotes multi-parte

- **Projetos afetados (4 bloqueados diretamente):**
  1. `autotmc-auto-tmc`: publica apenas `AutoTMC-Windows.exe` (PyInstaller) sem arquivo `.zip`/`.7z`.
  2. `mega-man-legends-modernization-project`: publica apenas instalador `MML-Setup.exe` sem pacote portátil.
  3. `sarecomp-sonic-adventure-recompiled`: publica apenas instalador `SonicAdventureRecompiled-*-Windows.exe` sem pacote portátil.
  4. `project-2099`: publica instalador `Project2099-Beta5-Setup.exe` acoplado a `Project2099-Beta5-Payload.zip` (`1,36 GiB`) e pacotes 4K separados.
- **Comportamento necessário:**
  - Suportar download verificado por SHA-256 de executável único (`asset_kind: "executable"`) para criação controlada na pasta de destino sem exigir contêiner `.zip`/`.7z`.
  - Suportar downloads multi-parte declarados em receita (lista explícita de URLs/assets da mesma release oficial com SHA-256 obrigatório por parte).
  - Avaliar contrato auditado e sem elevação (UAC) para instaladores silenciosos confiáveis ou aguardar publicação de `.zip` portátil pelos autores originais.
- **Critérios de aceitação:** teste de integração baixando `.exe` único verificado por SHA-256 ou conjunto multi-arquivo verificado sem escrita fora da pasta de destino nem elevação.

---

### 3. Launchers baseados em `.bat` / Java sem `.exe` nativo (`launch_command`)

- **Projeto afetado (1 bloqueado):** `severed-chains` (`the-legend-of-dragoon`, `Legend-of-Dragoon-Modding/Severed-Chains`, release `release-3.0.0`, `Severed_Chains_Windows.zip` de `131.446.655` bytes, SHA-256 `164716cba1899cadf834506636de8da56721d695457c3b53c93c533999ef9bb4`).
- **Limitação real atual:** O pacote oficial Windows contém JRE embutido (`launch.bat` chamando Java sobre `lod-game-*.jar`), sem executável `.exe` na raiz. No SDK 1.3.0 (`INSTALACAO-V5.md`), `launch_file` exige obrigatoriamente um `.exe` presente em `required_files`, e scripts `.bat`/`.cmd` continuam proibidos.
- **Alteração necessária no motor:** contrato estrito de inicialização para JAR/JRE embutido (ex.: `launch_java` apontando para `.jar` e `jre` verificados dentro da pasta instalada) ou invocação restrita e auditada de `.bat` dentro da pasta instalada sem argumentos arbitrários.

---

### 4. Pipelines seguros de build/compilação local e repositórios apenas código-fonte (17 projetos)

- **Projetos afetados (17 bloqueados):**
  - **Kits Windows com toolchain de compilação embutido sem binário final pré-compilado (3):**
    - `doaxvb-re` (`DOAXBV-0.8.0.zip`, `109.788.899` B, SHA-256 `a4b80511a2d538b30a76358068fcc47ddb0837360b6fb952e0ef92358dd1f48c`): exige `BuildGame.cmd` / `Launcher.cmd` compilando o executável localmente com CMake/Git/Python/`extract-xiso.exe`.
    - `pinyon-shift` (`PinyonShift-Launcher.zip`, `69.162.260` B, SHA-256 `6ecf1b85f22f5c31284bc22e76c79f5c08d397f9aa36cb58a8fd70bff1316af3`): `PinyonShiftLauncher.exe` baixa LLVM/ShiftGlue e compila C++ localmente a partir da ISO (~30 GB).
    - `god-of-war-native-pc-port-gow-pc-port` (`God-Of-War-PC-Launcher_0.4.0_x64-portable.zip`, `19.725.266` B, SHA-256 `e3583f31d56d175b5aaaf34e4b89465274d77ebdac5259182ddc3a7027a29aa1`): executa `kit/install.ps1` / `ps2_recomp.exe` baixando toolchain C++ externo.
  - **Repositórios apenas código-fonte sem releases Windows compiladas no GitHub (14):** `render96ex`, `sm64ex`, `sm64rt`, `drmario64-recomp`, `strikers-wiicompiled`, `mariokartdd-recomp`, `mkdd-recomp`, `doldecomp-mkdd-decompilacao-base`, `sm`, `sm-rewrite`, `tmc-decompilacao-base`, `crash-team-racing-turbocharged`, `wipeout-rewrite`, `mml1-megaman-legends-decomp`.
- **Comportamento necessário:** caso o All-Fix passe a oferecer fluxos de build, criar ambiente isolado e auditável de compilação (ou manter esses 17 fora do escopo declarativo enquanto os projetos não publicarem binários Windows pré-compilados).

---

### 5. Subpastas multi-nível em `first_run_files` / `profile_folders`

- **Motivação verificada na Rodada 7 (`phase-distorter`):** o port cria ativos (`earthbound.ebpak` / `mother2.ebpak`) em `%APPDATA%\ebsrc\EarthBoundCpp\`, caminho com dois níveis (`ebsrc/EarthBoundCpp`). Como `first_run_files[].profile_folder` no schema `v5` aceita apenas segmento único (`not: {"pattern": "/"}`), não foi possível habilitar `first_run_files` automático em `%APPDATA%\ebsrc\EarthBoundCpp\`.
- **Alteração sugerida:** permitir `profile_folder` com até 2–3 segmentos seguros (`ebsrc/EarthBoundCpp`) ou alternativa `anyOf` em `first_run_files` (ex.: `earthbound.ebpak` OU `mother2.ebpak`).

---

## Correções exclusivas no `AllFix-Repo` ou upstream (7 dos 29 restantes)

Estes **7 projetos** dependem de correção de metadados no catálogo `brad38/AllFix-Repo` ou de publicação do primeiro asset Windows pelo projeto original (fora do escopo do `GetAll-Addon` e do SDK do Codex):

1. `metaforce` (`metroid-prime`): repositório `AxioDL/metaforce` retorna HTTP 404 na API do GitHub.
2. `wind-waker-recomp` (`the-legend-of-zelda-the-wind-waker`): catálogo aponta para `elliotttate/Wind-Waker-Recomp` (`0` releases; projeto migrado para `chrissotraidis/bluewake`, já atendido por receita).
3. `twilight-princess-courage-reborn` (`the-legend-of-zelda-twilight-princess`): catálogo aponta notícia (`pcgamer.com`) sem repositório/release.
4. `project-picori-999sian-tmc` (`the-legend-of-zelda-the-minish-cap`): catálogo aponta perfil `https://github.com/999sian` sem repositório específico.
5. `sonic-1-forever-sonic-2-absolute` (`sonic-the-hedgehog-1-2-2013`): distribuição externa em `teamforeveronline.wixsite.com` sem `github_repository`.
6. `foxhollow` (`star-fox-adventures`): tag `v1.0.30` sem assets anexados na release.
7. `strikersrecomp` (`super-mario-strikers`): tag `v0.1.0` sem assets anexados na release.


---

## Evidencias adicionais — Rodada 8 (SDK 1.3.0, 2026-11-23)

**Nenhuma alteração do motor é feita aqui.** A API GitHub de 26 origens cadastradas dos 29 projetos sem receita foi reconsultada e os bloqueios foram confrontados com o schema v5 e a DLL compilada. Nao houve um novo binario portatil instalavel, verificavel e autonomo para nenhum desses 29 IDs.

### 6. Extracao auditada de tar.gz na origem correta

- Projeto condicionado: project-picori-999sian-tmc, origem cadastrada somente como perfil GitHub https://github.com/999sian.
- Evidencia upstream: repositorio https://github.com/999sian/tmc publica release v0.9.6 com tmc-multi-windows-x86_64-v0.9.6.tar.gz (26.500.874 B). O host atual aceita .zip, .rar e .7z em GameInstallationService.Prepare e nao descompacta .tar.gz.
- Contrato proposto: suporte ao formato .tar.gz **somente para assets ligados a release oficial e repositorio coincidente com catalogo**, validacao do content-type, nomes e extensao, streaming com limites de bytes/entradas, rejeicao de symlinks/hardlinks, traversal, paths Windows reservados, duplicatas case-insensitive, tamanho/CRC quando aplicavel, rollback e staging atomico.
- **Dependencia independente obrigatoria:** correcao da identidade da fonte no AllFix-Repo pelo mantenedor do catalogo; nao substituir URL de perfil por outro repositorio na receita sem autorizacao.
- Regressao: pacote tar.gz valido com run.exe no subdiretorio; nome normalizado e SHA-256 reconhecido; rejeicao de caminhos ../ e symlink, excesso de arquivos/descompactacao bomb e pacote falso com extensao tar.gz.

### 7. Distinguir arquivo .exe baixado de instalador de jogo concluido

- StoreDownloadService.ValidateFileName permite arquivos .exe/.msi nos downloads; GameInstallationService.Prepare para esses formatos copia artefatos e **nao** instala o jogo nem executa instaladores.
- Projetos: autotmc-auto-tmc, mega-man-legends-modernization-project, sarecomp-sonic-adventure-recompiled e project-2099, com payloads externos separados neste ultimo.
- Contrato proposto: declaracao asset_kind=portable_exe vinculada a tag/asset SHA-256 e executavel autocontido; instaladores somente por provedor restrito confiavel com verificacao de assinatura, sem elevacao administrativa automatica, escrita confinada, confirmacao do usuario e pos-condicoes; suporte multi-assets com digests independentes e rollback.
- Regressao: binario avulso portatil, instalador sem modo silencioso, payload ausente/hash corrompido, cancelamento e escrita fora do destino devem ter resultados seguros, sem executar comandos declarados por terceiros.

### 8. Melhorias funcionais obtidas sem novas operações do SDK

O suporte v5 a MD5/size/magic e SHA-256/size/magic ja permite importar as ROMs canônicas de perfect-dark-pc-port-perfect-dark e automobililamborghini-recomp, além da imagem BIN canônica de ctr-native. As tres receitas foram migradas experimentalmente v3→v5, mantidos repositório, tag, executável, arquivos do ZIP e estado experimental. O parser real 1.3.0 aceitou as três. **Nao pedir nova capacidade ao Codex para estes tres casos**; resta somente teste ponta a ponta com copia legitima e inicializacao real.

[Registro individual da Rodada 8](RODADA-8-SDK13-2026-11-23.md).

---

## Priorização após a Rodada 9 — contratos faltantes no SDK 1.3.0

**Escopo deste documento:** especificação para o Codex, **sem modificação do All-Fix principal, DLL, SDK ou AllFix-Repo**. Estado da main confirmado em 4960e2a2f375fa8b929cf12f54770d65f183c1c9, PR #8 merged. Entre 119 IDs, 29 permanecem sem receita e as 90 existentes ainda exigem mídia legítima para homologação funcional, exceto sm64coopdx.

### P0. Instalação explícita de executáveis e instaladores, com múltiplos assets

**Motivo:** StonedModder/auto-tmc (AutoTMC-Windows.exe), Drakfix/MML_Modernization-Project (MML-Setup.exe), sonicfreak1337/SARecomp (instalador Windows de release anterior) e GenryTheFox0/Project-2099 (Setup.exe, Payload.zip e partes de expansão). StoreDownloadService.ValidateFileName aceita extensão .exe e .msi para o arquivo baixado, mas GameInstallationService.Prepare **copia o executável e retorna estado não instalável**; não há contrato de instalação de executáveis arbitrários e tal cópia nunca equivale a um jogo pronto.

**Contrato proposto:**
- Distinguir no manifesto do provedor, com lista fechada, **portable_executable**, **verified_installer** e **multi_asset_payload**, sem reaproveitar import_input, copy ou move para executar instaladores.
- Fonte vinculada a repo/tag/asset oficiais; hash SHA-256 e tamanho por parte; identificação de arquivos exigidos e versão de cada asset; rejeição de downgrade ou mismatch de manifesto; download de todos os assets com validação antes de qualquer etapa irreversível.
- Para portáteis, verificar se o EXE é de fato o jogo/launcher autocontido e não um programa de configuração; declarar launch_file, required_files e diretório de trabalho, verificando o estado final. Não promover ferramentas auxiliares a jogo instalado.
- Para instaladores, provedor separado auditado por projeto e explicitamente aprovado pelo usuário, com validação de assinatura quando aplicável, sem UAC automático, sem execuções arbitrárias de shell declaradas por JSON remoto; pós-condições auditáveis da instalação, cancelamento/rollback e isolamento de efeitos no sistema.
- Para multipartes, limitar número, tamanho e expansão, rejeitar redirecionamentos/arquivos duplicados/traversal, manter instalação atômica e somente marcar completa depois da verificação de todos os required_files e do executável final.

**Regressões mínimas:** EXE genuinamente portátil; EXE instalador indevidamente tratado como portátil; instalação sem modo silencioso; assinatura/hashes/tamanhos incorretos; falta de uma das partes; arquivo de destino fora da raiz; cancelamento; repetição sem duplicar efeitos; atualização e rollback; não executar arquivo apenas porque foi baixado.

### P0. Runtime Java/JAR com launcher fixo, sem scripts arbitrários

**Projeto demonstrativo:** Legend-of-Dragoon-Modding/Severed-Chains (Severed_Chains_Windows.zip, 131.446.655 B; inclui launcher .bat/JAR e runtime Java). O SDK 1.3.0 apenas declara java-21 como prerequisite passivo, mas StoreAddonProviders.ParseRecipe exige launch_file .exe.

**Contrato:** launch_kind=java_jar com entrypoint JAR relativo e caminhos confinados, versão mínima/máxima de Java, diretório de trabalho verificado, argumentos por lista estrita de tokens sem metacaracteres/expansão shell, timeout, verificações de required_files e first-run. NUNCA permitir executar launch.bat ou comandos dinâmicos fornecidos pelo repositório por simples receita JSON.

**Regressões:** JAR válido, JAR ausente, Java indisponível/versão errada, classpath fora da pasta, argumentos de injeção, link simbólico, cancelamento e erro de boot verificado.

### P1. Extração segura tar.gz para release oficial e origem de catálogo correta

**Caso:** Project Picori. Catálogo aponta somente para https://github.com/999sian; o repositório 999sian/tmc distribui Windows x86_64 v0.9.6 em tmc-multi-windows-x86_64-v0.9.6.tar.gz (26.500.874 B). Não assumir que perfil equivale automaticamente ao repo. A correção do AllFix-Repo tem de ser autorizada e feita fora deste repositório.

**Contrato:** aceita somente release/asset oficial com repo declarado e hash; interpreta gzip/tar com limites de expansão de arquivos, bytes, profundidade e tempo; rejeita entradas duplicadas case-insensitive, symlink/hardlink, reparse points, dispositivo especial, path absoluto, drive letter, UNC, segmentos '..', diretórios reservados Windows, decompression bombs. Extrai em staging, verifica required_files, publica de forma atômica.

**Regressões:** tar.gz verdadeiro, extensão falsa, link para fora, tar path com traversal, entrada repetida, extrato inválido/truncado e limites de recursos. Sem o ajuste de identidade, não criar receita Project Picori.

### P1. Importação de romsets arcade com nomes oficiais não convencionais (Cannonball)

O projeto djyt/cannonball v0.34 possui ZIP Windows válido e executável, mas o usuário ainda precisa copiar manualmente **31 ROMs de OutRun Revision B** para roms/. As 31 entradas obrigatórias estão em roms/roms.txt e o código oficial src/main/roms.cpp declara por arquivo **nome, tamanho e CRC32** em operações LOAD. Exemplo: epr-10187.88 e opr-10268.99. Os caminhos de import_input_set / verifiedDataFiles v5 aceitam somente extensões de dados pré-listadas; sufixos '.88', '.76', '.99' não passam. O schema não oferece crc32 por arquivo.

**Contrato:** uma operação import_input_set_arcade com lista fechada de nomes relativos fornecida pelo upstream oficial, formato de tamanho exato e checksum CRC32 + opção SHA-256 por item; validação de todos os arquivos antes de copiar; rejeição de nomes extras, links, diretórios aninhados não previstos, colisões no Windows, arquivo truncado e CRC divergente. Não permitir extensões numéricas globais sem whitelist associada ao romset oficial; confirmar sobrescrita e aplicar rollback do conjunto completo.

**Regressões:** conjunto sintético completo (31/31) com checksums corretos, uma ROM ausente, sufixo numérico errado, adulteração sem mudar tamanho, duplicatas case-insensitive, symlink para fora, ZIP de romset dentro de diretório não especificado e rollback transacional. Não importar ROMs de outro jogo.

### P2. Compilação controlada e requisitos de assets legítimos

Os 17 projetos classificados como kit/código-fonte, incluindo Render96ex, sm64ex, sm64rt, projetos MKDD, Super Metroid e DOAXBV, requerem build/recompilação, extração de dados e dependências externas. Não implementar uma operação genérica de shell/cmd/powershell. Preferir distribuição binária oficial verificada. Se Codex decidir suportar builds: pipelines versionadas **no host**, com toolchains oficiais e hashes fixos, regras de leitura da mídia, sandbox, limites de CPU/tempo/disco, diagnóstico, cancelamento, artefato final auditado e testes de regressão por plataforma. A receita remota seleciona apenas um pipeline aprovado pelo host, sem fornecer comandos ou URLs executáveis.

### P2. Outros contratos já documentados nas rodadas anteriores

- Destinos extras de import_input (.sfc/.smc/.gba) com lista fechada segura, extensões e magia reais, sem cópia de arquivos executáveis.
- first_run_files em LocalAppData/RoamingAppData com 2–3 subpastas seguras e verificações alternativas explicitamente declaradas (ex.: Phase Distorter).
- Mídias multi-track PS1 com nomes diversos e BIN/CUE, exigindo correspondência entre CUE e track names, validação de conteúdo sem hashes inventados e cancelamento; WipeOut Phantom Edition não pode ser considerado automatizado apenas por criar diskimages/.
- Recuperação de fonte/repo correto no AllFix-Repo para Metaforce, Wind Waker Recomp, Project Picori, Twilight Princess, Sonic Forever, Foxhollow e StrikersRecomp (ou publicação de assets pelo upstream).

## Melhorias já possíveis sem nova funcionalidade SDK (Rodada 9)

- **Crash Team Racing: High Octane v.1.5:** import_input verificado do BIN original NTSC-U 926 para assets/ctr-u.bin. Contrato v5 já existente, sem novo schema.
- **GGARecomp v0.3.0:** input original US verificado por SHA-1/magic, import_input para local_app_data/GGARecompiled/gga.us.z64. Usa suporte v5 existente. A configuração dos controles/launcher continua declarada e requer teste real de primeira inicialização.

Ambos permaneceram experimental; o parser SDK 1.3.0 aceitou as 90 receitas, e nenhum jogo foi iniciado com mídia original no ambiente desta rodada. **Não solicitar ao Codex uma operação que o SDK já oferece para estes dois casos.**

[Relatório e matriz de 29 projetos da Rodada 9](RODADA-9-SDK13-2026-11-23.md).
