# Validação experimental — silent-hill-native-pc-port crossplatform-beta

Jogo: silent-hill
Projeto oficial: silent-hill-native-pc-port
Repositório: https://github.com/SlickAmogus/silent-hill-decomp
Release: https://github.com/SlickAmogus/silent-hill-decomp/releases/tag/crossplatform-beta
ZIP oficial: SHPC_beta-2026.10.12.1.zip
Tamanho do ZIP baixado: 83061493 bytes
SHA-256 ZIP: b22a1c93e5a9537bfa9c676071a2d7f1c8df6069fc44f7419fb73379d8cec81d
Executável: SilentHillPC_Launcher.exe
Required files: SilentHillPC_Launcher.exe, SilentHillPC.exe, SDL2.dll, libopenal-1.dll, avcodec-62.dll, avformat-62.dll, avutil-60.dll
Caminho da receita: recipes/silent-hill/silent-hill-native-pc-port/crossplatform-beta.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial Silent Hill Native PC Port (crossplatform-beta, SHPC_beta-2026.10.12.1.zip) foi extraido. Execute SilentHillPC_Launcher.exe e selecione sua imagem de disco original de Silent Hill (PS1 USA, PAL ou NTSC-J) para carregar os dados do jogo. Nenhum arquivo comercial e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:19:10Z`
- **Pacote baixado e conferido:** `SHPC_beta-2026.10.12.1.zip` (`83061493` bytes, SHA-256 `b22a1c93e5a9537bfa9c676071a2d7f1c8df6069fc44f7419fb73379d8cec81d`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `7/7` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 7/7 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
