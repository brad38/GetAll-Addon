# Validação experimental — quest64-recomp v0.1

Jogo: quest-64
Projeto oficial: quest64-recomp
Repositório: https://github.com/Rainchus/Quest64-Recomp
Release: https://github.com/Rainchus/Quest64-Recomp/releases/tag/v0.1
ZIP oficial: Quest64Recompiledv0.1.zip
Tamanho do ZIP baixado: 22220405 bytes
SHA-256 ZIP: 7ad69b69c3d83d73edbaa3beb2e0a1cb8d66c022761fd7e61f6c3ed7c4d9fd30
Executável: Quest64Recompiled.exe
Required files: Quest64Recompiled.exe, SDL2.dll, dxcompiler.dll, dxil.dll
Caminho da receita: recipes/quest-64/quest64-recomp/v0.1.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros.
Não testado: instalação ponta a ponta no AllFix.exe com ROM original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial de Quest 64 (v0.1) foi extraido. Execute Quest64Recompiled.exe na pasta instalada e Forneca sua ROM original de Quest 64 (US) no menu inicial. Nenhuma ROM e fornecida pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:17:11Z`
- **Pacote baixado e conferido:** `Quest64Recompiledv0.1.zip` (`22220405` bytes, SHA-256 `7ad69b69c3d83d73edbaa3beb2e0a1cb8d66c022761fd7e61f6c3ed7c4d9fd30`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 4/4 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
