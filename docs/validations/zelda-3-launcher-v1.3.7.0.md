# Validação experimental — zelda-3-launcher v1.3.7.0

Jogo: the-legend-of-zelda-a-link-to-the-past
Projeto oficial: zelda-3-launcher
Repositório: https://github.com/RadzPrower/Zelda-3-Launcher
Release: https://github.com/RadzPrower/Zelda-3-Launcher/releases/tag/v1.3.7.0
ZIP oficial: Zelda_3_Launcher_v1.3.7.0.zip
Tamanho do ZIP baixado: 3792896 bytes
SHA-256 ZIP: 2a92fc4e636b8ac008a3a1b31d8bbe7866bcdbc85622152bf36f9ea28d1c2cfc
Schema da receita: v5 (`schema_version: 5`)
Executável (`launch_file`): Zelda 3 Launcher.exe
Pré-requisitos declarados: nenhum
Required files: Zelda 3 Launcher.exe, Zelda 3 Launcher.dll, SDL2.dll, LibGit2Sharp.dll
Caminho da receita: recipes/the-legend-of-zelda-a-link-to-the-past/zelda-3-launcher/v1.3.7.0.json

Testado estaticamente: JSON Schema v5 (`installation-recipe-v5.schema.json`), `scripts/validate_recipes.py --require-jsonschema --check-git-blobs --check-catalog`, IDs/tag exatos, presença dos `required_files` no ZIP oficial e regras de caminhos v5.
Não testado: instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário nem inicialização real do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O Zelda 3 Launcher (v1.3.7.0) foi extraido. Execute 'Zelda 3 Launcher.exe', clique em Download e selecione sua ROM original norte-americana (US) de The Legend of Zelda: A Link to the Past (SHA-256 oficial 66871d66be19ad2c34c927d6b14cd8eb6fc3181965b6e517cb361f7316009cfb) no seletor do launcher (ou copie-a como zelda3.sfc ao lado do executavel) para baixar e compilar localmente. Nenhuma ROM e fornecida.

## Teste de instalação no motor `AllFix.dll` 1.3.0

- **Data (UTC):** `2026-11-23T16:13:46Z`
- **Pacote baixado e conferido:** `Zelda_3_Launcher_v1.3.7.0.zip` (`3792896` bytes, SHA-256 `2a92fc4e636b8ac008a3a1b31d8bbe7866bcdbc85622152bf36f9ea28d1c2cfc`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e operações declaradas concluídas pelo motor oficial `AllFix.dll` 1.3.0 (`Status=PartiallyCompleted`, `4/4` `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
