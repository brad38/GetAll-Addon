# Validação experimental — sm64plus LauncherMirror

Jogo: super-mario-64
Projeto oficial: sm64plus
Repositório: https://github.com/MorsGames/sm64plus
Release: https://github.com/MorsGames/sm64plus/releases/tag/LauncherMirror
ZIP oficial: SM64Plus.zip
Tamanho do ZIP baixado: 6617082 bytes
SHA-256 ZIP: f3f930a822c80694fbb7faf0c82cea2b14290b83bad2e9823ff2f2433e46fdb7
Schema da receita: v5 (`schema_version: 5`)
Executável (`launch_file`): Super Mario 64 Plus.exe
Pré-requisitos declarados: nenhum
Required files: Super Mario 64 Plus.exe, SDL2.dll, lib64Plus.dll, data.win
Caminho da receita: recipes/super-mario-64/sm64plus/LauncherMirror.json

Testado estaticamente: JSON Schema v5 (`installation-recipe-v5.schema.json`), `scripts/validate_recipes.py --require-jsonschema --check-git-blobs --check-catalog`, IDs/tag exatos, presença dos `required_files` no ZIP oficial e regras de caminhos v5.
Não testado: instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário nem inicialização real do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O launcher oficial do SM64Plus (LauncherMirror) foi extraido. Abra 'Super Mario 64 Plus.exe' na pasta instalada e selecione sua ROM legitima de Super Mario 64 (US, .z64) quando o launcher solicitar para extrair os ativos e gerar a build local. Nenhuma ROM e distribuida pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll` 1.3.0

- **Data (UTC):** `2026-11-23T16:13:42Z`
- **Pacote baixado e conferido:** `SM64Plus.zip` (`6617082` bytes, SHA-256 `f3f930a822c80694fbb7faf0c82cea2b14290b83bad2e9823ff2f2433e46fdb7`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e operações declaradas concluídas pelo motor oficial `AllFix.dll` 1.3.0 (`Status=PartiallyCompleted`, `4/4` `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
