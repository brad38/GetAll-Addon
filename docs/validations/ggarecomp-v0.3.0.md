# Validação experimental — ggarecomp v0.3.0

Jogo: goemon-s-great-adventure
Projeto oficial: ggarecomp
Repositório: https://github.com/DreaXer/GGARecomp
Release: https://github.com/DreaXer/GGARecomp/releases/tag/v0.3.0
ZIP oficial: GGARecompiled-v0.3.0-windows.zip
Tamanho do ZIP baixado: 40258542 bytes
SHA-256 ZIP: 19c8e7fd7a009e48675742a6af453a8e7e8934adac4a4d7f0fa41bb084241e3c
Executável: GGARecompiled.exe
Required files: GGARecompiled.exe, SDL2.dll, dxcompiler.dll, dxil.dll
Caminho da receita: recipes/goemon-s-great-adventure/ggarecomp/v0.3.0.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros.
Não testado: instalação ponta a ponta no AllFix.exe com ROM original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial de Goemon's Great Adventure (v0.3.0) foi extraido. Execute GGARecompiled.exe na pasta instalada e Forneca sua ROM original de Goemon's Great Adventure (US SHA-1 9f9e860816f9e2a68bb5f4f56086e0c7450c64d7) no launcher. Nenhuma ROM e fornecida pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:17:01Z`
- **Pacote baixado e conferido:** `GGARecompiled-v0.3.0-windows.zip` (`40258542` bytes, SHA-256 `19c8e7fd7a009e48675742a6af453a8e7e8934adac4a4d7f0fa41bb084241e3c`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 4/4 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
