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


## Rodada 8 — upgrade experimental SDK 1.3.0

- **Receita atualizada:** schema_version 3 para **5**; o indice permanece experimental. A receita anterior exigia copia manual da midia original; agora usa import_input no escopo installation e validacao nativa antes da escrita.
- **ROM original:** SHA-256 cab2467684a58bc19c787423d704a961aa497629763367d9fe691172de58591c; destino exato Automobili Lamborghini (USA).z64. O script oficial scripts/race_field_patches.py fixa SHA-256 da ROM USA, e scripts/gen_syms_toml.py fixa ROM_SIZE=0x400000 e ROM_FILE. O README descreve a procura automatica desse nome ao lado do EXE.
- **Pacote oficial:** ZIP baixado novamente, SHA-256 296d24961c1b763de25ee2edee934cc5cfa66c63379db204f6f377670c6046db; executavel e DLLs obrigatorias conferidos; nenhuma ROM/ISO no pacote.
- **Contrato/ambiente:** parser de receitas da AllFix.dll compilada com SDK 1.3.0, incluindo as 90 receitas; criterios cumulativos de hash, tamanho e assinatura conferidos estaticamente e por testes com dados sinteticos.
- **Teste funcional pendente:** nao havia ROM legitima para executar a importacao real e o boot do jogo. Nenhum teste de jogo real foi realizado e nenhum status validated foi concedido.
- **Referencia oficial:** https://github.com/alondero/automobililamborghini-recomp/blob/main/README.md
