# Validação experimental — strikers v2.0.0

Jogo: super-mario-strikers
Projeto oficial: strikers
Repositório: https://github.com/new-coke/strikers
Release: https://github.com/new-coke/strikers/releases/tag/v2.0.0
ZIP oficial: strikers-windows-x86_64.zip
Tamanho do ZIP baixado: 30176733 bytes
SHA-256 ZIP: 14888779c899d592358e6d54a392c7ce863d3ec476416f8af7c72602bc7a26c7
Executável: strikers.exe
Required files: strikers.exe, strikers-settings.exe, SDL3.dll, Qt6Core.dll, dxcompiler.dll, dxil.dll
Caminho da receita: recipes/super-mario-strikers/strikers/v2.0.0.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial Strikers (v2.0.0) foi extraido. Execute strikers.exe (ou strikers-settings.exe para configuracoes) e aponte sua imagem de disco original de Super Mario Strikers (.iso, .gcm, .ciso ou .gcz). Nenhum arquivo comercial e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:18:11Z`
- **Pacote baixado e conferido:** `strikers-windows-x86_64.zip` (`30176733` bytes, SHA-256 `14888779c899d592358e6d54a392c7ce863d3ec476416f8af7c72602bc7a26c7`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `6/6` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 6/6 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
