# God of War e Pinyon Shift: restauração dos procedimentos oficiais

Esta revisão substitui os fluxos locais que alteravam fontes/runtimes por chamadas às interfaces oficiais. O código de instalação está em `Services/GameInstallationGowOfficial.cs` e `Services/GameInstallationPinyonOfficial.cs`. Os perfis anteriores permanecem vetados; uma receita antiga em cache não adquire autorização apenas por compartilhar a mesma tag.

Os testes de contrato usam dados autorais sintéticos. Nesta revisão não foram executadas instalações completas com mídia comercial, primeiro boot ou gameplay destes dois projetos. A conclusão do instalador não deve atualizar essas categorias de evidência.

## God of War

- Projeto: [danielalves96/gow-pc-port](https://github.com/danielalves96/gow-pc-port/tree/adebc00e69d4395318c94523f345b26c7daf3451), tag `launcher-v0.4.0`.
- Perfil novo: `gow-0.4.0-official-installer`.
- Pacote: `God-Of-War-PC-Launcher_0.4.0_x64-portable.zip`, 19.725.266 bytes, SHA-256 `e3583f31d56d175b5aaaf34e4b89465274d77ebdac5259182ddc3a7027a29aa1`.
- Instalador distribuído (CRLF): 71.380 bytes, SHA-256 `d15eaac24dd4e0c703f7e846450aca6cfc86b7da57ea52f1008b1a1f7fbe281c`.
- Mídia: ISO ou CHD original USA SCUS-97399; o instalador oficial mantém sua validação de identidade do ELF.
- Entrada Jogar: launcher oficial, `God Of War - PC Launcher.exe --play`.

O GetAll usa o `install.ps1` intacto com `-Iso`, `-Destination`, `-NoPause` e `-Compiler clang`. Não passa `-AllowModifiedElf`, `-SkipCpuCheck`, `-NoOptimize`, `-FastDev`, `-Pgo off` ou `-InstallTools`. O compilador publicado pelo upstream é obtido sob demanda, pelo cache compartilhado, e o próprio instalador verifica o mesmo SHA-256 novamente.

### Registro equivalente ao wizard

A chamada direta ao executável do jogo omitia o ambiente construído pelo launcher e sua otimização. O novo fluxo conserva o launcher oficial:

1. Reproduz `optimizer::register_installation`: copia o runner de `build/ps2xRuntime` para `active`, preserva a data de modificação e copia `game-elf.sha256`.
2. Cria a pasta `vu1_captures` e conta os mesmos nomes de captura considerados pelo upstream.
3. Reproduz os campos de instalação de `install_complete`: ELF, runner ativo, destino da otimização, contagem já compilada e ISO vazia após extração completa.
4. Usa os caminhos definitivos na configuração, antes da publicação atômica.
5. Define `GOW_LAUNCHER_DATA_DIR` para a instalação registrada. As demais opções vêm de `Settings::default`/serde do launcher, sem cópia local dos seus parâmetros gráficos.

O kit, fontes geradas e ferramentas permanecem na instalação porque a otimização oficial continua a utilizá-los. A função upstream `Configure` detecta a mudança do caminho das fontes e descarta seu cache CMake obsoleto quando necessário. Esse comportamento permite a publicação por staging sem reescrever o projeto.

No Jogar, os arquivos fixos do kit, launcher e mídia permanecem verificados. Saves e preferências são mutáveis. O runner ativo também pode ser reconstruído pelo otimizador oficial: ele é validado como PE AMD64 e deve continuar acompanhado da identidade do mesmo ELF. Não se exige que uma recompilação legítima conserve o hash do primeiro build.

Fontes do contrato:

- [install.ps1](https://github.com/danielalves96/gow-pc-port/blob/adebc00e69d4395318c94523f345b26c7daf3451/install.ps1)
- [Registro e sincronização do optimizer](https://github.com/danielalves96/gow-pc-port/blob/adebc00e69d4395318c94523f345b26c7daf3451/gow-launcher/crates/gow-core/src/optimizer.rs)
- [install_complete e inicialização do launcher](https://github.com/danielalves96/gow-pc-port/blob/adebc00e69d4395318c94523f345b26c7daf3451/gow-launcher/src-tauri/src/lib.rs)
- [Configurações oficiais](https://github.com/danielalves96/gow-pc-port/blob/adebc00e69d4395318c94523f345b26c7daf3451/gow-launcher/crates/gow-core/src/settings.rs)
- [Diretório de dados](https://github.com/danielalves96/gow-pc-port/blob/adebc00e69d4395318c94523f345b26c7daf3451/gow-launcher/crates/gow-core/src/paths.rs)

## Pinyon Shift

- Projeto: [arcanite24/pinyon-shift](https://github.com/arcanite24/pinyon-shift/tree/850518ce00c66d65557bcbf190a62d2e2a6bb0e3), tag `v0.9.5`.
- Perfil novo: `pinyon-v0.9.5-official-installer`.
- Pacote oficial: `PinyonShift-Launcher.zip`, 69.162.260 bytes, SHA-256 `6ecf1b85f22f5c31284bc22e76c79f5c08d397f9aa36cb58a8fd70bff1316af3`.
- Fonte embutida: `pinyon-shift-source.zip`, 1.850.884 bytes, SHA-256 `0d0ef7fc980366c2564128f619aee2ecc859bd4fd2723c0dc32ab55769df3f81`.
- Mídia: ISO ou pasta extraída original USA MS-2505 / 4D5309C9.
- Runner registrado: `out/build/win-amd64-release/pinyon_shift.exe`. O comando Jogar executa o script oficial `tools/launch-preview.ps1`.

A fonte embutida da release é necessária: ela contém a configuração oficial dos kits binários, que difere da configuração do arquivo codeload. A extração nova nunca chama `ApplyPinyonNativeSourceOverlay`.

A instalação chama `tools/setup-preview.ps1` com `-IsoPath` ou `-ExtractedPath` e `-JsonEvents`. O script original verifica a mídia, obtém as ferramentas e o kit ShiftGlue publicado pelo projeto, gera os shaders e compila o runtime. O AllFix não altera flags FFX/FSR, renderizadores, CPU baseline, NGX ou SDK.

Apenas após o aceite explícito na interface é definido o parâmetro oficial `PINYON_SHIFT_ACCEPT_MICROSOFT_LICENSE=1`. O novo perfil não reutiliza escolhas de desenvolvimento do perfil aposentado.

O resultado precisa incluir os executáveis esperados, Python oficial, fontes/scripts fixados e o comprovante `.local/setup-state.json` com o estado `ready`. Os 2.400 arquivos do catálogo de mídia também são verificados antes da publicação. A pasta extraída tem `iso_sha256: null` no comprovante oficial: verificar os arquivos não prova o hash da ISO que os originou. O novo fluxo aceita essa distinção somente com verificação por catálogo.

### Jogar e recursos posteriores à instalação

O script de execução oficial prepara shaders, verifica Rally quando presente e aplica os procedimentos oficiais de DLCs/mods antes de abrir o jogo. O AllFix não usa opções de teste, `-SkipShaderPreparation` ou variante de desenvolvimento `-TitleUpdateV4`.

Fontes, configuração, scripts e Python são conservados porque o launcher e o jogo os utilizam. O layout preservado é reconhecido pelo launcher oficial como checkout, sem criar seu marcador de fonte extraída. Preferências, saves, DLCs e caches em `.local/preview` permanecem mutáveis. As dependências são obtidas apenas na instalação selecionada; nenhum desses componentes entra no complemento declarativo.

Fontes do contrato:

- [Setup oficial](https://github.com/arcanite24/pinyon-shift/blob/850518ce00c66d65557bcbf190a62d2e2a6bb0e3/tools/setup-preview.ps1)
- [Execução oficial](https://github.com/arcanite24/pinyon-shift/blob/850518ce00c66d65557bcbf190a62d2e2a6bb0e3/tools/launch-preview.ps1)
- [Toolchains e tratamento de diretórios movidos](https://github.com/arcanite24/pinyon-shift/blob/850518ce00c66d65557bcbf190a62d2e2a6bb0e3/tools/release-common.ps1)
- [Verificação de pasta extraída](https://github.com/arcanite24/pinyon-shift/blob/850518ce00c66d65557bcbf190a62d2e2a6bb0e3/tools/verify-extracted-game.ps1)

## Verificação e limites da evidência

Os testes `GowOfficialIntegration.Policy` e `PinyonOfficialIntegration.Policy` cobrem argumentos, identidade, rejeição dos perfis antigos, caminhos depois da publicação, dados mutáveis, configuração redirecionada, consentimento e comprovantes incompletos. O teste do registro GOW usa um arquivo autoral não executável apenas para conferir bytes/mtime; não é um teste de compilação do jogo.

A validação completa com mídia original continua pendente para ambos. O status da matriz deve ser **automação implementada / contratos sintéticos verificados**, sem promover original, boot ou gameplay. Falhas upstream futuras devem bloquear a instalação com seus logs, sem aplicação automática de patches locais.
