# Validação experimental — goemon64recomp v0.2.0-dev

Jogo: mystical-ninja-starring-goemon
Projeto oficial: goemon64recomp
Repositório: https://github.com/klorfmorf/Goemon64Recomp
Release: https://github.com/klorfmorf/Goemon64Recomp/releases/tag/v0.2.0-dev
ZIP oficial: Goemon64Recompiled-Windows-RelWithDebInfo.zip
Tamanho do ZIP baixado: 25007915 bytes
SHA-256 ZIP: f74041842f059e65be3cc2ba3d51a82c543a3b16406189afe45951cb40ac5896
Executável: Goemon64Recompiled.exe
Required files: Goemon64Recompiled.exe, SDL2.dll, dxcompiler.dll, dxil.dll
Caminho da receita: recipes/mystical-ninja-starring-goemon/goemon64recomp/v0.2.0-dev.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros.
Não testado: instalação ponta a ponta no AllFix.exe com ROM original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial de Mystical Ninja Starring Goemon (v0.2.0-dev) foi extraido. Execute Goemon64Recompiled.exe na pasta instalada e Forneca sua ROM original de Mystical Ninja Starring Goemon (US) no menu inicial. Nenhuma ROM e fornecida pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:16:57Z`
- **Pacote baixado e conferido:** `Goemon64Recompiled-Windows-RelWithDebInfo.zip` (`25007915` bytes, SHA-256 `f74041842f059e65be3cc2ba3d51a82c543a3b16406189afe45951cb40ac5896`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 4/4 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
