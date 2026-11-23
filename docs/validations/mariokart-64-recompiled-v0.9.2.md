# Validação experimental — mariokart-64-recompiled v0.9.2

Jogo: mario-kart-64
Projeto oficial: mariokart-64-recompiled
Repositório: https://github.com/sonicdcer/MarioKart64Recomp
Release: https://github.com/sonicdcer/MarioKart64Recomp/releases/tag/v0.9.2
ZIP oficial: MarioKart64Recompiled-v0.9.2-Windows-RelWithDebInfo.zip
Tamanho do ZIP baixado: 23847630 bytes
SHA-256 ZIP: 4b41226ad7d4c6012878194fa88fe1a83c1fa8f425dfbaa2a7ea87eb01c1c2b4
Executável: MarioKart64Recompiled.exe
Required files: MarioKart64Recompiled.exe, SDL2.dll, dxcompiler.dll, dxil.dll
Caminho da receita: recipes/mario-kart-64/mariokart-64-recompiled/v0.9.2.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros.
Não testado: instalação ponta a ponta no AllFix.exe com ROM original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial de Mario Kart 64 (v0.9.2) foi extraido. Execute MarioKart64Recompiled.exe na pasta instalada e Escolha sua ROM original de Mario Kart 64 no menu inicial. Nenhuma ROM e fornecida pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:16:51Z`
- **Pacote baixado e conferido:** `MarioKart64Recompiled-v0.9.2-Windows-RelWithDebInfo.zip` (`23847630` bytes, SHA-256 `4b41226ad7d4c6012878194fa88fe1a83c1fa8f425dfbaa2a7ea87eb01c1c2b4`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 4/4 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
