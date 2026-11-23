# Validação experimental — the-darkness-recomp v0.1.10

Jogo: the-darkness
Projeto oficial: the-darkness-recomp
Repositório: https://github.com/portingpete/The-Darkness-Recomp
Release: https://github.com/portingpete/The-Darkness-Recomp/releases/tag/v0.1.10
ZIP oficial: The-Darkness-Recomp-v0.1.10-windows-x64.zip
Tamanho do ZIP baixado: 41776055 bytes
SHA-256 ZIP: 46773f866bbbaac51fec5f958d2dc7dcdc8cc7624503fbee771e7e89eb07dec3
Executável: build_native/Release/DarkRecomp.exe
Required files: build_native/Release/DarkRecomp.exe, build_native/Release/DarkRecompPreview.exe, build_native/Release/avcodec-darkxma-62.dll, build_native/Release/avutil-darkxma-60.dll, Launch.cmd
Caminho da receita: recipes/the-darkness/the-darkness-recomp/v0.1.10.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial The Darkness Recomp (v0.1.10) foi extraido. Antes de iniciar, copie todos os arquivos e pastas extraidos do seu dump original de The Darkness (Xbox 360), incluindo default.xex, Content e System, diretamente para a subpasta Darkness/ (nao use um arquivo .iso diretamente). Voce tambem pode usar Launch.cmd ou LaunchWithSettings.cmd na raiz instalada. Nenhum arquivo comercial e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:18:19Z`
- **Pacote baixado e conferido:** `The-Darkness-Recomp-v0.1.10-windows-x64.zip` (`41776055` bytes, SHA-256 `46773f866bbbaac51fec5f958d2dc7dcdc8cc7624503fbee771e7e89eb07dec3`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `5/5` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 5/5 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
