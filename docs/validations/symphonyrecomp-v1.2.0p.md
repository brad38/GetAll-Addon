# Validação experimental — symphonyrecomp v1.2.0p

Jogo: castlevania-symphony-of-the-night
Projeto oficial: symphonyrecomp
Repositório: https://github.com/BlackLabelHQ/SymphonyRecomp
Release: https://github.com/BlackLabelHQ/SymphonyRecomp/releases/tag/v1.2.0p
ZIP oficial: SymphonyRecomp-v1.2.0p-windows-x64.zip
Tamanho do ZIP baixado: 63884901 bytes
SHA-256 ZIP: 3d3e5f0a46896737a6a0a3bcddbc9b1b0c58e0d5f91e0de16bd44f64451ef662
Schema da receita: v5 (`schema_version: 5`)
Executável (`launch_file`): sotn.exe
Pré-requisitos declarados: dotnet-desktop-10-x64, openal-x64
Required files: sotn.exe, sotn.dll, sotn.runtimeconfig.json, SDL2.dll, soft_oal.dll
Caminho da receita: recipes/castlevania-symphony-of-the-night/symphonyrecomp/v1.2.0p.json

Testado estaticamente: JSON Schema v5 (`installation-recipe-v5.schema.json`), `scripts/validate_recipes.py --require-jsonschema --check-git-blobs --check-catalog`, IDs/tag exatos, presença dos `required_files` no ZIP oficial e regras de caminhos v5.
Não testado: instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário nem inicialização real do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial SymphonyRecomp (v1.2.0p) foi extraido e a pasta disc/ foi criada. Certifique-se de ter o .NET 10 Desktop Runtime x64 e o OpenAL instalados e copie para disc/ as faixas norte-americanas PS1 'Castlevania - Symphony of the Night (USA) (Track 1).bin', 'Castlevania - Symphony of the Night (USA) (Track 2).bin' e 'Castlevania - Symphony of the Night (USA).cue' (ou arquivo .chd compativel) antes de iniciar sotn.exe. Nenhum ativo comercial e fornecido.

## Teste de instalação no motor `AllFix.dll` 1.3.0

- **Data (UTC):** `2026-11-23T16:13:58Z`
- **Pacote baixado e conferido:** `SymphonyRecomp-v1.2.0p-windows-x64.zip` (`63884901` bytes, SHA-256 `3d3e5f0a46896737a6a0a3bcddbc9b1b0c58e0d5f91e0de16bd44f64451ef662`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `5/5` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e operações declaradas concluídas pelo motor oficial `AllFix.dll` 1.3.0 (`Status=PartiallyCompleted`, `5/5` `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
