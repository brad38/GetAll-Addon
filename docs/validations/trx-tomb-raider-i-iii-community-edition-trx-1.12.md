# Validação experimental — trx-tomb-raider-i-iii-community-edition trx-1.12

Jogo: tomb-raider-i-v
Projeto oficial: trx-tomb-raider-i-iii-community-edition
Repositório: https://github.com/LostArtefacts/TRX
Release: https://github.com/LostArtefacts/TRX/releases/tag/trx-1.12
ZIP oficial: TRX-1.12-Windows.zip
Tamanho do ZIP baixado: 361171822 bytes
SHA-256 ZIP: db890625de2de0baf4f97802b65754af22f30a3f4b3307ef789537f09606fc0e
Executável: TRX.exe
Required files: TRX.exe
Caminho da receita: recipes/tomb-raider-i-v/trx-tomb-raider-i-iii-community-edition/trx-1.12.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial de Tomb Raider I-III (trx-1.12) foi extraido. Para jogar, copie os arquivos de dados originais do seu Tomb Raider I, II ou III para a pasta instalada do TRX conforme docs/trx/INSTALLING.md antes de executar TRX.exe. Nenhum arquivo comercial ou ROM e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:17:44Z`
- **Pacote baixado e conferido:** `TRX-1.12-Windows.zip` (`361171822` bytes, SHA-256 `db890625de2de0baf4f97802b65754af22f30a3f4b3307ef789537f09606fc0e`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `1/1` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 1/1 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
