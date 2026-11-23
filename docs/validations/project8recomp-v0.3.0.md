# Validação experimental — project8recomp v0.3.0

Jogo: tony-hawk-s-project-8
Projeto oficial: project8recomp
Repositório: https://github.com/theokyr/Project8Recomp
Release: https://github.com/theokyr/Project8Recomp/releases/tag/v0.3.0
ZIP oficial: Project8Recomp-v0.3.0-windows-x86_64.zip
Tamanho do ZIP baixado: 21674894 bytes
SHA-256 ZIP: f255842b916a98c8188259fa3da5931bcea639b6c656e82d26f8b274b69be436
Executável: Project8Recomp-v0.3.0-windows-x86_64/Project8Recomp.exe
Required files: Project8Recomp-v0.3.0-windows-x86_64/Project8Recomp.exe, Project8Recomp-v0.3.0-windows-x86_64/thps_p8.exe, Project8Recomp-v0.3.0-windows-x86_64/thps_p8_gui.exe, Project8Recomp-v0.3.0-windows-x86_64/SDL3.dll
Caminho da receita: recipes/tony-hawk-s-project-8/project8recomp/v0.3.0.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial Project8Recomp (v0.3.0) foi extraido. Execute Project8Recomp.exe em Project8Recomp-v0.3.0-windows-x86_64/ e aponte sua imagem .iso original de Tony Hawk's Project 8 (Xbox 360). Nenhum arquivo comercial e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:18:24Z`
- **Pacote baixado e conferido:** `Project8Recomp-v0.3.0-windows-x86_64.zip` (`21674894` bytes, SHA-256 `f255842b916a98c8188259fa3da5931bcea639b6c656e82d26f8b274b69be436`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 4/4 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
