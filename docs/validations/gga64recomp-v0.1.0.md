# Validação experimental — gga64recomp v0.1.0

Jogo: goemon-s-great-adventure
Projeto oficial: gga64recomp
Repositório: https://github.com/StopSine/GGA64Recomp
Release: https://github.com/StopSine/GGA64Recomp/releases/tag/v0.1.0
ZIP oficial: GGA64Recompiled-Windows-RelWithDebInfo.zip
Tamanho do ZIP baixado: 19956602 bytes
SHA-256 ZIP: ce2301089d964545db5d58ff04d68dccd8c79e078f53a353b3e56bbf86220883
Executável: GGA64Recompiled.exe
Required files: GGA64Recompiled.exe, SDL2.dll, dxcompiler.dll, dxil.dll
Caminho da receita: recipes/goemon-s-great-adventure/gga64recomp/v0.1.0.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros.
Não testado: instalação ponta a ponta no AllFix.exe com ROM original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial de Goemon's Great Adventure (v0.1.0) foi extraido. Execute GGA64Recompiled.exe na pasta instalada e Forneca sua ROM original de Goemon's Great Adventure no menu inicial. Nenhuma ROM e fornecida pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:17:03Z`
- **Pacote baixado e conferido:** `GGA64Recompiled-Windows-RelWithDebInfo.zip` (`19956602` bytes, SHA-256 `ce2301089d964545db5d58ff04d68dccd8c79e078f53a353b3e56bbf86220883`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 4/4 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
