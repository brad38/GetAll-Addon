# Validação experimental — extremegrecomp v1.0.0

Jogo: extreme-g
Projeto oficial: extremegrecomp
Repositório: https://gitlab.com/sonicdcer/ExtremeGRecomp
Release: https://gitlab.com/sonicdcer/ExtremeGRecomp/-/releases/v1.0.0
ZIP oficial: ExtremeGRecompiled-v1.0.0-Windows-RelWithDebInfo.zip
Tamanho do ZIP baixado: 18530070 bytes
SHA-256 ZIP: f72d1d2a77d1270b622e05e108fd30af408bd42c45e661552bff89ba339c1633
Schema da receita: v5 (`schema_version: 5`)
Executável (`launch_file`): ExtremeGRecompiled.exe
Pré-requisitos declarados: nenhum
Required files: ExtremeGRecompiled.exe, SDL2.dll, dxcompiler.dll, dxil.dll
Caminho da receita: recipes/extreme-g/extremegrecomp/v1.0.0.json

Testado estaticamente: JSON Schema v5 (`installation-recipe-v5.schema.json`), `scripts/validate_recipes.py --require-jsonschema --check-git-blobs --check-catalog`, IDs/tag exatos, presença dos `required_files` no ZIP oficial e regras de caminhos v5.
Não testado: instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário nem inicialização real do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial de Extreme-G: Recompiled (v1.0.0) foi extraido. Execute ExtremeGRecompiled.exe na pasta instalada e forneca sua copia original norte-americana (NTSC-U 1.0) de Extreme-G no menu inicial. Nenhuma ROM e fornecida pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll` 1.3.0

- **Data (UTC):** `2026-11-23T16:13:55Z`
- **Pacote baixado e conferido:** `ExtremeGRecompiled-v1.0.0-Windows-RelWithDebInfo.zip` (`18530070` bytes, SHA-256 `f72d1d2a77d1270b622e05e108fd30af408bd42c45e661552bff89ba339c1633`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e operações declaradas concluídas pelo motor oficial `AllFix.dll` 1.3.0 (`Status=PartiallyCompleted`, `4/4` `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
