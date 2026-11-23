# Validação experimental — phase-distorter 0.5

Jogo: earthbound-mother-2
Projeto oficial: phase-distorter
Repositório: https://github.com/TheRunaway5/Phase-Distorter
Release: https://github.com/TheRunaway5/Phase-Distorter/releases/tag/0.5
ZIP oficial: Phase-Distorter-0.5-windows-x86_64.zip
Tamanho do ZIP baixado: 14353099 bytes
SHA-256 ZIP: 195d8b2fa4a05753d5330fef4d9030939074763ff3bedc41c5dcc2d9181b28ad
Schema da receita: v5 (`schema_version: 5`)
Executável (`launch_file`): Phase-Distorter-0.5-windows-x86_64/Phase Distorter.exe
Pré-requisitos declarados: nenhum
Required files: Phase-Distorter-0.5-windows-x86_64/Phase Distorter.exe, Phase-Distorter-0.5-windows-x86_64/SDL2.dll, Phase-Distorter-0.5-windows-x86_64/MANIFEST.json
Caminho da receita: recipes/earthbound-mother-2/phase-distorter/0.5.json

Testado estaticamente: JSON Schema v5 (`installation-recipe-v5.schema.json`), `scripts/validate_recipes.py --require-jsonschema --check-git-blobs --check-catalog`, IDs/tag exatos, presença dos `required_files` no ZIP oficial e regras de caminhos v5.
Não testado: instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário nem inicialização real do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial Phase Distorter (0.5) foi extraido em Phase-Distorter-0.5-windows-x86_64/. Execute 'Phase Distorter.exe' e importe sua ROM legitima de EarthBound (US) ou Mother 2 (JP) no assistente inicial; os pacotes de ativos e saves ficam gravados em %APPDATA%/ebsrc/EarthBoundCpp/. Nenhuma ROM e fornecida.

## Teste de instalação no motor `AllFix.dll` 1.3.0

- **Data (UTC):** `2026-11-23T16:13:46Z`
- **Pacote baixado e conferido:** `Phase-Distorter-0.5-windows-x86_64.zip` (`14353099` bytes, SHA-256 `195d8b2fa4a05753d5330fef4d9030939074763ff3bedc41c5dcc2d9181b28ad`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `3/3` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e operações declaradas concluídas pelo motor oficial `AllFix.dll` 1.3.0 (`Status=PartiallyCompleted`, `3/3` `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
