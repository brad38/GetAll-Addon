# Validação experimental — bluewake v0.12.0

Jogo: the-legend-of-zelda-the-wind-waker
Projeto oficial: bluewake
Repositório: https://github.com/chrissotraidis/bluewake
Release: https://github.com/chrissotraidis/bluewake/releases/tag/v0.12.0
ZIP oficial: BlueWake-v0.12.0-windows-x64.zip
Tamanho do ZIP baixado: 212667573 bytes
SHA-256 ZIP: 3ff3915f5c893539a0ce9f1052d769d8c984826b140c907a61166508e6dc58b9
Executável: BlueWake/BlueWake.exe
Required files: BlueWake/BlueWake.exe, BlueWake/SDL3.dll, BlueWake/gGZLE01_recomp.dll, BlueWake/dxcompiler.dll, BlueWake/dxil.dll
Caminho da receita: recipes/the-legend-of-zelda-the-wind-waker/bluewake/v0.12.0.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial BlueWake (v0.12.0) foi extraido. Ao iniciar BlueWake.exe pela primeira vez, selecione sua imagem de disco legitima de The Legend of Zelda: The Wind Waker (GameCube, versao USA GZLE01 rev 0, em formato .iso ou .gcm; arquivos .rvz devem ser convertidos antes no Dolphin). Nenhum arquivo comercial e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:17:59Z`
- **Pacote baixado e conferido:** `BlueWake-v0.12.0-windows-x64.zip` (`212667573` bytes, SHA-256 `3ff3915f5c893539a0ce9f1052d769d8c984826b140c907a61166508e6dc58b9`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `5/5` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 5/5 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
