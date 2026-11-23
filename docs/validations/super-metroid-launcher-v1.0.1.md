# Validação experimental — super-metroid-launcher v1.0.1

Jogo: super-metroid
Projeto oficial: super-metroid-launcher
Repositório: https://github.com/RadzPrower/Super-Metroid-Launcher
Release: https://github.com/RadzPrower/Super-Metroid-Launcher/releases/tag/v1.0.1
ZIP oficial: Super_Metroid_Launcher_v1.0.1.zip
Tamanho do ZIP baixado: 2092800 bytes
SHA-256 ZIP: 06b4a698f5ec5ddebba55fb5464a9966b37f104c931f5ce7f799baf5db03b3c4
Schema da receita: v5 (`schema_version: 5`)
Executável (`launch_file`): Super Metroid Launcher.exe
Pré-requisitos declarados: nenhum
Required files: Super Metroid Launcher.exe, Super Metroid Launcher.dll, SDL2.dll, git2-b7bad55.dll
Caminho da receita: recipes/super-metroid/super-metroid-launcher/v1.0.1.json

Testado estaticamente: JSON Schema v5 (`installation-recipe-v5.schema.json`), `scripts/validate_recipes.py --require-jsonschema --check-git-blobs --check-catalog`, IDs/tag exatos, presença dos `required_files` no ZIP oficial e regras de caminhos v5.
Não testado: instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário nem inicialização real do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O Super Metroid Launcher (v1.0.1) foi extraido. Execute 'Super Metroid Launcher.exe', clique em Download e selecione sua ROM original norte-americana (US) de Super Metroid (SHA-256 oficial 12b77c4bc9c1832cee8881244659065ee1d84c70c3d29e6eaf92e6798cc2ca72) no seletor do launcher (ou copie-a como sm.sfc ao lado do executavel) para concluir a compilacao local. Nenhuma ROM e fornecida.

## Teste de instalação no motor `AllFix.dll` 1.3.0

- **Data (UTC):** `2026-11-23T16:13:46Z`
- **Pacote baixado e conferido:** `Super_Metroid_Launcher_v1.0.1.zip` (`2092800` bytes, SHA-256 `06b4a698f5ec5ddebba55fb5464a9966b37f104c931f5ce7f799baf5db03b3c4`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e operações declaradas concluídas pelo motor oficial `AllFix.dll` 1.3.0 (`Status=PartiallyCompleted`, `4/4` `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
