# Validação experimental — megaman64recompiled v0.9.1

Jogo: mega-man-64
Projeto oficial: megaman64recompiled
Repositório: https://github.com/MegaMan64Recomp/MegaMan64Recompiled
Release: https://github.com/MegaMan64Recomp/MegaMan64Recompiled/releases/tag/v0.9.1
ZIP oficial: MegaMan64Recompiled-v0.9.1-Windows.zip
Tamanho do ZIP baixado: 24721093 bytes
SHA-256 ZIP: 21e31bda2cb09808c0ed18c63b89faa6c2328c082fd8880c4acbdf3c6390931a
Executável: MegaMan64Recompiled.exe
Required files: MegaMan64Recompiled.exe, SDL2.dll, dxcompiler.dll, dxil.dll
Caminho da receita: recipes/mega-man-64/megaman64recompiled/v0.9.1.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros.
Não testado: instalação ponta a ponta no AllFix.exe com ROM original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial de Mega Man 64 (v0.9.1) foi extraido. Execute MegaMan64Recompiled.exe na pasta instalada e Forneca sua ROM original de Mega Man 64 (US) no menu inicial. Nenhuma ROM e fornecida pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:17:13Z`
- **Pacote baixado e conferido:** `MegaMan64Recompiled-v0.9.1-Windows.zip` (`24721093` bytes, SHA-256 `21e31bda2cb09808c0ed18c63b89faa6c2328c082fd8880c4acbdf3c6390931a`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 4/4 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
