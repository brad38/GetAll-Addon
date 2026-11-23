# Validação experimental — sssv-recomp v0.2.0

Jogo: space-station-silicon-valley
Projeto oficial: sssv-recomp
Repositório: https://github.com/Cellenseres/SSSV_Recomp
Release: https://github.com/Cellenseres/SSSV_Recomp/releases/tag/v0.2.0
ZIP oficial: SSSVRecompiled_v0.2.0_Windows.zip
Tamanho do ZIP baixado: 46548721 bytes
SHA-256 ZIP: c5111d552c8440746a846d634d36c1249e250c0b4e06912aeb6248c7001d35f2
Executável: SSSVRecompiled.exe
Required files: SSSVRecompiled.exe, SDL2.dll, dxcompiler.dll, dxil.dll
Caminho da receita: recipes/space-station-silicon-valley/sssv-recomp/v0.2.0.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros.
Não testado: instalação ponta a ponta no AllFix.exe com ROM original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial de Space Station Silicon Valley (v0.2.0) foi extraido. Execute SSSVRecompiled.exe na pasta instalada e Forneca sua ROM original de Space Station Silicon Valley no menu inicial. Nenhuma ROM e fornecida pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:17:08Z`
- **Pacote baixado e conferido:** `SSSVRecompiled_v0.2.0_Windows.zip` (`46548721` bytes, SHA-256 `c5111d552c8440746a846d634d36c1249e250c0b4e06912aeb6248c7001d35f2`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 4/4 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
