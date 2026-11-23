# Validação experimental — open-nectar 1.3

Jogo: pikmin-pikmin-2
Projeto oficial: open-nectar
Repositório: https://github.com/SSunnKing/Open-Nectar---Pikmin-Native-PC-Mobile-Port
Release: https://github.com/SSunnKing/Open-Nectar---Pikmin-Native-PC-Mobile-Port/releases/tag/1.3
ZIP oficial: nectar-windows.zip
Tamanho do ZIP baixado: 25708831 bytes
SHA-256 ZIP: d1de1aab9e38d90339c1a7bf584f83509e404a6b961331d6832fa004d204c078
Executável: nectar-windows/nectar-launcher.exe
Required files: nectar-windows/nectar-launcher.exe, nectar-windows/nectar.exe, nectar-windows/pikmin2_pc.exe, nectar-windows/manifest.json
Caminho da receita: recipes/pikmin-pikmin-2/open-nectar/1.3.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial Open Nectar (1.3) foi extraido. Execute nectar-launcher.exe na pasta nectar-windows/ e clique em Install para apontar suas imagens originais de Pikmin e/ou Pikmin 2 (.iso). Nenhum arquivo comercial e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:18:10Z`
- **Pacote baixado e conferido:** `nectar-windows.zip` (`25708831` bytes, SHA-256 `d1de1aab9e38d90339c1a7bf584f83509e404a6b961331d6832fa004d204c078`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 4/4 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
