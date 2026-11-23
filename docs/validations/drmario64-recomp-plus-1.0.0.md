# Validação experimental — drmario64-recomp-plus 1.0.0

Jogo: dr-mario-64
Projeto oficial: drmario64-recomp-plus
Repositório: https://github.com/theboy181/drmario64_recomp_plus
Release: https://github.com/theboy181/drmario64_recomp_plus/releases/tag/1.0.0
ZIP oficial: Dr.Mario.64.Recompiled-v1.0.0-Windows.zip
Tamanho do ZIP baixado: 24225142 bytes
SHA-256 ZIP: ba749f48725e23636845c9a79a89e17859172ac80fa7b98bf4523d12c1f0d2cf
Schema da receita: v5 (`schema_version: 5`)
Executável (`launch_file`): Dr. Mario 64 Recompiled x64-Release/drmario64_recomp.exe
Pré-requisitos declarados: nenhum
Required files: Dr. Mario 64 Recompiled x64-Release/drmario64_recomp.exe, Dr. Mario 64 Recompiled x64-Release/SDL2.dll, Dr. Mario 64 Recompiled x64-Release/dxcompiler.dll, Dr. Mario 64 Recompiled x64-Release/dxil.dll
Caminho da receita: recipes/dr-mario-64/drmario64-recomp-plus/1.0.0.json

Testado estaticamente: JSON Schema v5 (`installation-recipe-v5.schema.json`), `scripts/validate_recipes.py --require-jsonschema --check-git-blobs --check-catalog`, IDs/tag exatos, presença dos `required_files` no ZIP oficial e regras de caminhos v5.
Não testado: instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário nem inicialização real do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial de Dr. Mario 64 Recompiled Plus (1.0.0) foi extraido em 'Dr. Mario 64 Recompiled x64-Release/'. Execute 'drmario64_recomp.exe' e forneca sua ROM original americana (US) de Dr. Mario 64 no menu inicial. Nenhuma ROM ou ativo comercial e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll` 1.3.0

- **Data (UTC):** `2026-11-23T16:13:44Z`
- **Pacote baixado e conferido:** `Dr.Mario.64.Recompiled-v1.0.0-Windows.zip` (`24225142` bytes, SHA-256 `ba749f48725e23636845c9a79a89e17859172ac80fa7b98bf4523d12c1f0d2cf`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e operações declaradas concluídas pelo motor oficial `AllFix.dll` 1.3.0 (`Status=PartiallyCompleted`, `4/4` `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
