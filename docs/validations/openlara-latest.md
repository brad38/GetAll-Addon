# Validação experimental — openlara latest

Jogo: tomb-raider-i-v
Projeto oficial: openlara
Repositório: https://github.com/XProger/OpenLara
Release: https://github.com/XProger/OpenLara/releases/tag/latest
ZIP oficial: OpenLara_win.zip
Tamanho do ZIP baixado: 359739 bytes
SHA-256 ZIP: d24cbf90ee4ef94414c64808d3aa13198079faf72d9ea3cae393675284929ad1
Executável: OpenLara.exe
Required files: OpenLara.exe
Caminho da receita: recipes/tomb-raider-i-v/openlara/latest.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial de Tomb Raider I (latest) foi extraido. Para jogar, copie os arquivos de nivel/audio da sua copia original de Tomb Raider para a mesma pasta de OpenLara.exe antes de jogar. Nenhum arquivo comercial ou ROM e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:17:55Z`
- **Pacote baixado e conferido:** `OpenLara_win.zip` (`359739` bytes, SHA-256 `d24cbf90ee4ef94414c64808d3aa13198079faf72d9ea3cae393675284929ad1`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `1/1` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 1/1 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
