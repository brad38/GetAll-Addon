# Validação experimental — crash-team-racing-high-octane v.1.5

Jogo: crash-team-racing
Projeto oficial: crash-team-racing-high-octane
Repositório: https://github.com/Rinnegatamante/Crash-Team-Racing-High-Octane
Release: https://github.com/Rinnegatamante/Crash-Team-Racing-High-Octane/releases/tag/v.1.5
ZIP oficial: ctr-high-octane-x64.win.zip
Tamanho do ZIP baixado: 2403121 bytes
SHA-256 ZIP: 005924af516a3cb2bcdc19269422e2de77719600656e5b00df45424fe081693e
Schema da receita: v5 (`schema_version: 5`)
Executável (`launch_file`): Crash Team Racing - High Octane.exe
Pré-requisitos declarados: nenhum
Required files: Crash Team Racing - High Octane.exe, assets/dualshock.png
Caminho da receita: recipes/crash-team-racing/crash-team-racing-high-octane/v.1.5.json

Testado estaticamente: JSON Schema v5 (`installation-recipe-v5.schema.json`), `scripts/validate_recipes.py --require-jsonschema --check-git-blobs --check-catalog`, IDs/tag exatos, presença dos `required_files` no ZIP oficial e regras de caminhos v5.
Não testado: instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário nem inicialização real do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial de Crash Team Racing: High Octane (v.1.5) foi extraido. Para jogar, copie o arquivo .bin da sua copia PS1 NTSC-U original renomeado exatamente como assets/ctr-u.bin na pasta instalada antes de iniciar 'Crash Team Racing - High Octane.exe'. Nenhum arquivo comercial e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll` 1.3.0

- **Data (UTC):** `2026-11-23T16:13:51Z`
- **Pacote baixado e conferido:** `ctr-high-octane-x64.win.zip` (`2403121` bytes, SHA-256 `005924af516a3cb2bcdc19269422e2de77719600656e5b00df45424fe081693e`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `2/2` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e operações declaradas concluídas pelo motor oficial `AllFix.dll` 1.3.0 (`Status=PartiallyCompleted`, `2/2` `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
