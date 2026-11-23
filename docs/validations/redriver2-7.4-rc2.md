# Validação experimental — redriver2 7.4-rc2

Jogo: driver-2
Projeto oficial: redriver2
Repositório: https://github.com/OpenDriver2/REDRIVER2
Release: https://github.com/OpenDriver2/REDRIVER2/releases/tag/7.4-rc2
ZIP oficial: REDRIVER2_Win32_Release.zip
Tamanho do ZIP baixado: 9772801 bytes
SHA-256 ZIP: 92c20bf6194af715a84c058783fa3095ed09d3aeeb4c41485b11c984d14d276c
Schema da receita: v5 (`schema_version: 5`)
Executável (`launch_file`): Launcher.exe
Pré-requisitos declarados: java-21
Required files: Launcher.exe, REDRIVER2.exe, SDL2.dll, OpenAL32.dll, config.ini, install/jpsxdec.jar
Caminho da receita: recipes/driver-2/redriver2/7.4-rc2.json

Testado estaticamente: JSON Schema v5 (`installation-recipe-v5.schema.json`), `scripts/validate_recipes.py --require-jsonschema --check-git-blobs --check-catalog`, IDs/tag exatos, presença dos `required_files` no ZIP oficial e regras de caminhos v5.
Não testado: instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário nem inicialização real do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial REDRIVER2 (7.4-rc2) foi extraido. Com Java instalado (jpsxdec), execute Launcher.exe, abra 'Setup wizard', selecione as imagens originais dos dois discos PS1 (CD1 e CD2 de Driver 2, formato .bin/.cue ou .iso) e conclua a extracao antes de clicar em 'Launch game'. Nenhuma imagem de disco e fornecida pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll` 1.3.0

- **Data (UTC):** `2026-11-23T16:14:01Z`
- **Pacote baixado e conferido:** `REDRIVER2_Win32_Release.zip` (`9772801` bytes, SHA-256 `92c20bf6194af715a84c058783fa3095ed09d3aeeb4c41485b11c984d14d276c`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `6/6` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e operações declaradas concluídas pelo motor oficial `AllFix.dll` 1.3.0 (`Status=PartiallyCompleted`, `6/6` `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
