# Validação experimental — ctr-native beta-7.1

Jogo: crash-team-racing
Projeto oficial: ctr-native
Repositório: https://github.com/CTR-tools/ctr-native
Release: https://github.com/CTR-tools/ctr-native/releases/tag/beta-7.1
ZIP oficial: ctr-native-beta-7_1-windows-x86.zip
Tamanho do ZIP baixado: 8746455 bytes
SHA-256 ZIP: af0d23c7b41925917b5eaf6fc292bd172368efc1c68918755de527a664049dad
Executável: ctr-native-beta-7_1-windows-x86/ctr_native.exe
Required files: ctr-native-beta-7_1-windows-x86/ctr_native.exe
Caminho da receita: recipes/crash-team-racing/ctr-native/beta-7.1.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial de Crash Team Racing (beta-7.1) foi extraido. Para jogar, copie sua imagem BIN NTSC-U bruta (MODE2/2352) como assets/ctr-u.bin dentro de ctr-native-beta-7_1-windows-x86/ antes de iniciar ctr_native.exe. Nenhum arquivo comercial ou ROM e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:17:33Z`
- **Pacote baixado e conferido:** `ctr-native-beta-7_1-windows-x86.zip` (`8746455` bytes, SHA-256 `af0d23c7b41925917b5eaf6fc292bd172368efc1c68918755de527a664049dad`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `1/1` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 1/1 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
