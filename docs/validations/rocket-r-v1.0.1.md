# Validação experimental — rocket-r v.1.0.1

Jogo: rocket-robot-on-wheels
Projeto oficial: rocket-r
Repositório: https://github.com/thatguymcd/rocket-r
Release: https://github.com/thatguymcd/rocket-r/releases/tag/v.1.0.1
ZIP oficial: Rocket-R-1.0.1-Windows-x64.zip
Tamanho do ZIP baixado: 22735057 bytes
SHA-256 ZIP: d47ba319b8aa6bc3a348258a8cd1a5cf0f693eb129c87b2fc895d6f15dd87db1
Executável: Rocket-R.exe
Required files: Rocket-R.exe, SDL2.dll, dxcompiler.dll, dxil.dll
Caminho da receita: recipes/rocket-robot-on-wheels/rocket-r/v1.0.1.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial, caminhos relativos seguros. README oficial confirma 12 MiB (12582912 bytes) e SHA-1 622d71a44da0b81ea68092cac9198c66154a4f4a.
Não testado: instalação ponta a ponta no AllFix.exe com ROM original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima antes de promoção para validated).

Procedimento manual da receita: O pacote oficial Rocket-R e sua ROM verificada rocket-r.us.z64 foram instalados. Abra Rocket-R.exe na pasta do jogo e selecione rocket-r.us.z64 no menu inicial.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:16:38Z`
- **Pacote baixado e conferido:** `Rocket-R-1.0.1-Windows-x64.zip` (`22735057` bytes, SHA-256 `d47ba319b8aa6bc3a348258a8cd1a5cf0f693eb129c87b2fc895d6f15dd87db1`)
- **Resultado (`GameInstallationService.Run`):** `extraction_ok_awaiting_media` (`Status=Failed`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Execução interrompida na seleção de mídia obrigatória com retorno esperado `Status=Failed` (`A dependência obrigatória não foi selecionada.`) pois não há ROM/ISO comercial local; estrutura do ZIP oficial conferida integralmente (4/4 `required_files` e `launch_file` presentes).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
