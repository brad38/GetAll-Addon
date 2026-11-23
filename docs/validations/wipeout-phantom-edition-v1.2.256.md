# Validação experimental — wipeout-phantom-edition v1.2.256

Jogo: wipeout
Projeto oficial: wipeout-phantom-edition
Repositório: https://github.com/wipeout-phantom-edition/wipeout-phantom-edition
Release: https://github.com/wipeout-phantom-edition/wipeout-phantom-edition/releases/tag/v1.2.256
ZIP oficial: wipeout-x64-release.zip
Tamanho do ZIP baixado: 3619822 bytes
SHA-256 ZIP: f63eca6d14ca4995083b2127fb8912d94a58437791da843e0899522c8664fb23
Schema da receita: v5 (`schema_version: 5`)
Executável (`launch_file`): wipeout/wipeout.exe
Pré-requisitos declarados: nenhum
Required files: wipeout/wipeout.exe, wipeout/sdl2.dll, wipeout/OpenAL32.dll, wipeout/lua51.dll, wipeout/sndfile.dll, wipeout/defaultinput.cfg, wipeout/phantom/gamedatamanifest
Caminho da receita: recipes/wipeout/wipeout-phantom-edition/v1.2.256.json

Testado estaticamente: JSON Schema v5 (`installation-recipe-v5.schema.json`), `scripts/validate_recipes.py --require-jsonschema --check-git-blobs --check-catalog`, IDs/tag exatos, presença dos `required_files` no ZIP oficial e regras de caminhos v5.
Não testado: instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário nem inicialização real do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial WipeOut Phantom Edition (v1.2.256) foi extraido e a pasta wipeout/diskimages foi criada. Copie sua imagem multi-faixa PS1 da regiao USA composta por 9 arquivos .bin (faixa 1 em MODE2/2352 e faixas 2 a 9 em AUDIO) mais o arquivo .cue para wipeout/diskimages/ antes de iniciar wipeout/wipeout.exe. Na primeira execucao o port extrai os dados e faixas musicais automaticamente. Nenhuma midia e fornecida.

## Teste de instalação no motor `AllFix.dll` 1.3.0

- **Data (UTC):** `2026-11-23T16:13:57Z`
- **Pacote baixado e conferido:** `wipeout-x64-release.zip` (`3619822` bytes, SHA-256 `f63eca6d14ca4995083b2127fb8912d94a58437791da843e0899522c8664fb23`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `7/7` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e operações declaradas concluídas pelo motor oficial `AllFix.dll` 1.3.0 (`Status=PartiallyCompleted`, `7/7` `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
