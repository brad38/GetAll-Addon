# Validação experimental — automobililamborghini-recomp v0.11.1

Jogo: automobili-lamborghini
Projeto oficial: automobililamborghini-recomp
Repositório: https://github.com/alondero/automobililamborghini-recomp
Release: https://github.com/alondero/automobililamborghini-recomp/releases/tag/v0.11.1
ZIP oficial: lamborghini-recomp-windows-x64.zip
Tamanho do ZIP baixado: 37895031 bytes
SHA-256 ZIP: 296d24961c1b763de25ee2edee934cc5cfa66c63379db204f6f377670c6046db
Executável: lamborghini_modern.exe
Required files: lamborghini_modern.exe, SDL2.dll, dxcompiler.dll, dxil.dll, freetype.dll
Caminho da receita: recipes/automobili-lamborghini/automobililamborghini-recomp/v0.11.1.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros.
Não testado: instalação ponta a ponta no AllFix.exe com ROM original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial de Automobili Lamborghini (v0.11.1) foi extraido. Execute lamborghini_modern.exe na pasta instalada e Forneca sua ROM original de Automobili Lamborghini (USA) pelo seletor ou renomeada na pasta do executavel. Nenhuma ROM e fornecida pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:17:18Z`
- **Pacote baixado e conferido:** `lamborghini-recomp-windows-x64.zip` (`37895031` bytes, SHA-256 `296d24961c1b763de25ee2edee934cc5cfa66c63379db204f6f377670c6046db`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `5/5` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 5/5 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
