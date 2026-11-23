# Validação experimental — gsrecomp 0.8.4

Jogo: golden-sun-golden-sun-the-lost-age
Projeto oficial: gsrecomp
Repositório: https://github.com/Shmargus/GSRecomp
Release: https://github.com/Shmargus/GSRecomp/releases/tag/0.8.4
ZIP oficial: GoldenSunRecompiled-0.8.4-windows.zip
Tamanho do ZIP baixado: 63779736 bytes
SHA-256 ZIP: 602ea651285a5a31f0cfc8917d1b892fe6d35a18ab5435f64852558df5e232b6
Schema da receita: v5 (`schema_version: 5`)
Executável (`launch_file`): Golden Sun Recompiled/GoldenSunLauncher.exe
Pré-requisitos declarados: nenhum
Required files: Golden Sun Recompiled/GoldenSunLauncher.exe, Golden Sun Recompiled/SDL2.dll, Golden Sun Recompiled/games/The Broken Seal/GoldenSunRecomp.exe, Golden Sun Recompiled/games/The Lost Age/TLARecomp.exe
Caminho da receita: recipes/golden-sun-golden-sun-the-lost-age/gsrecomp/0.8.4.json

Testado estaticamente: JSON Schema v5 (`installation-recipe-v5.schema.json`), `scripts/validate_recipes.py --require-jsonschema --check-git-blobs --check-catalog`, IDs/tag exatos, presença dos `required_files` no ZIP oficial e regras de caminhos v5.
Não testado: instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário nem inicialização real do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial Golden Sun Recompiled (0.8.4) foi extraido em 'Golden Sun Recompiled/'. Execute 'GoldenSunLauncher.exe', escolha The Broken Seal ou The Lost Age e selecione sua ROM GBA original; na primeira inicializacao o launcher compila o codigo usando o MinGW embutido no pacote. Nenhuma ROM e fornecida.

## Teste de instalação no motor `AllFix.dll` 1.3.0

- **Data (UTC):** `2026-11-23T16:13:47Z`
- **Pacote baixado e conferido:** `GoldenSunRecompiled-0.8.4-windows.zip` (`63779736` bytes, SHA-256 `602ea651285a5a31f0cfc8917d1b892fe6d35a18ab5435f64852558df5e232b6`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e operações declaradas concluídas pelo motor oficial `AllFix.dll` 1.3.0 (`Status=PartiallyCompleted`, `4/4` `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
