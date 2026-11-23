# Validação experimental — chameleontwist1-jp-recomp v0.1

Jogo: chameleon-twist
Projeto oficial: chameleontwist1-jp-recomp
Repositório: https://github.com/Rainchus/ChameleonTwist1-JP-Recomp
Release: https://github.com/Rainchus/ChameleonTwist1-JP-Recomp/releases/tag/v0.1
ZIP oficial: ChameleonTwistJPRecompiled.zip
Tamanho do ZIP baixado: 23929489 bytes
SHA-256 ZIP: 8e705d3826ab413afac92ea753d7f11dbc93be9ea507a3ef86bb6003019b5c56
Executável: ChameleonTwistJPRecompiled.exe
Required files: ChameleonTwistJPRecompiled.exe, SDL2.dll, dxcompiler.dll, dxil.dll
Caminho da receita: recipes/chameleon-twist/chameleontwist1-jp-recomp/v0.1.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros.
Não testado: instalação ponta a ponta no AllFix.exe com ROM original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial de Chameleon Twist (v0.1) foi extraido. Execute ChameleonTwistJPRecompiled.exe na pasta instalada e Forneca sua ROM original de Chameleon Twist (JP) no menu inicial. Nenhuma ROM e fornecida pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:17:16Z`
- **Pacote baixado e conferido:** `ChameleonTwistJPRecompiled.zip` (`23929489` bytes, SHA-256 `8e705d3826ab413afac92ea753d7f11dbc93be9ea507a3ef86bb6003019b5c56`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 4/4 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
