# Validação experimental — vandalhearts-pcport v2.1.0

Jogo: vandal-hearts
Projeto oficial: vandalhearts-pcport
Repositório: https://github.com/HalmyLyseas/VandalHearts-PcPort
Release: https://github.com/HalmyLyseas/VandalHearts-PcPort/releases/tag/v2.1.0
ZIP oficial: VandalHearts-v2.1.0-windows-x64.zip
Tamanho do ZIP baixado: 5771542 bytes
SHA-256 ZIP: 365c7515e59f705ccb5942ab77270f0f9b98dbd3716e492d95266c226355868d
Schema da receita: v5 (`schema_version: 5`)
Executável (`launch_file`): vandalhearts_pc.exe
Pré-requisitos declarados: nenhum
Required files: vandalhearts_pc.exe, SDL2.dll, OpenAL32.dll, vandalhearts.ini
Caminho da receita: recipes/vandal-hearts/vandalhearts-pcport/v2.1.0.json

Testado estaticamente: JSON Schema v5 (`installation-recipe-v5.schema.json`), `scripts/validate_recipes.py --require-jsonschema --check-git-blobs --check-catalog`, IDs/tag exatos, presença dos `required_files` no ZIP oficial e regras de caminhos v5.
Não testado: instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário nem inicialização real do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial de Vandal Hearts PC Port (v2.1.0) e sua imagem .bin foram preparados em game/vandalhearts.bin (compativel apenas com USA SLUS-00447, Asia SCPS-45183 ou Japan SLPM-86007; Europe SLES-00204 nao e suportada). Inicie vandalhearts_pc.exe para verificar o disco e jogar.

## Teste de instalação no motor `AllFix.dll` 1.3.0

- **Data (UTC):** `2026-11-23T16:13:57Z`
- **Pacote baixado e conferido:** `VandalHearts-v2.1.0-windows-x64.zip` (`5771542` bytes, SHA-256 `365c7515e59f705ccb5942ab77270f0f9b98dbd3716e492d95266c226355868d`)
- **Resultado (`GameInstallationService.Run`):** `extraction_ok_awaiting_media` (`Status=Failed`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Execução avançou até a etapa de dependência obrigatória com retorno esperado `Status=Failed` (`A dependência obrigatória não foi selecionada.`), pois não há imagem PS1 comercial local; `4/4` `required_files` e `launch_file` conferidos no ZIP oficial.
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
