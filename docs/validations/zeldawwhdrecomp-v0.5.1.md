# Validação experimental — zeldawwhdrecomp v0.5.1

Jogo: the-legend-of-zelda-the-wind-waker-hd
Projeto oficial: zeldawwhdrecomp
Repositório: https://github.com/ZeldaWWHDRecomp/ZeldaWWHDRecomp
Release: https://github.com/ZeldaWWHDRecomp/ZeldaWWHDRecomp/releases/tag/v0.5.1
ZIP oficial: WindWakerHD-v0.5.1-windows-x86_64.zip
Tamanho do ZIP baixado: 41201612 bytes
SHA-256 ZIP: 2e8a8b29ed1b35e6d3cae370a7c9b6878a05d6269b28420dd492415da72f48c4
Schema da receita: v5 (`schema_version: 5`)
Executável (`launch_file`): WindWakerHD-v0.5.1-windows-x86_64/Wind Waker HD.exe
Pré-requisitos declarados: nenhum
Required files: WindWakerHD-v0.5.1-windows-x86_64/Wind Waker HD.exe, WindWakerHD-v0.5.1-windows-x86_64/sdk/runtime/SDL3.dll, WindWakerHD-v0.5.1-windows-x86_64/tools/bin/wwhd-extract.exe, WindWakerHD-v0.5.1-windows-x86_64/portable.txt
Caminho da receita: recipes/the-legend-of-zelda-the-wind-waker-hd/zeldawwhdrecomp/v0.5.1.json

Testado estaticamente: JSON Schema v5 (`installation-recipe-v5.schema.json`), `scripts/validate_recipes.py --require-jsonschema --check-git-blobs --check-catalog`, IDs/tag exatos, presença dos `required_files` no ZIP oficial e regras de caminhos v5.
Não testado: instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário nem inicialização real do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial Wind Waker HD Recompiled (v0.5.1) foi extraido em WindWakerHD-v0.5.1-windows-x86_64/. Na primeira preparacao, extraia os ativos da sua copia legitima de Wii U (USA ou EUR) usando o assistente ou tools/bin/wwhd-extract.exe antes de iniciar 'Wind Waker HD.exe'. Nenhum ativo comercial e fornecido.

## Teste de instalação no motor `AllFix.dll` 1.3.0

- **Data (UTC):** `2026-11-23T16:13:51Z`
- **Pacote baixado e conferido:** `WindWakerHD-v0.5.1-windows-x86_64.zip` (`41201612` bytes, SHA-256 `2e8a8b29ed1b35e6d3cae370a7c9b6878a05d6269b28420dd492415da72f48c4`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e operações declaradas concluídas pelo motor oficial `AllFix.dll` 1.3.0 (`Status=PartiallyCompleted`, `4/4` `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
