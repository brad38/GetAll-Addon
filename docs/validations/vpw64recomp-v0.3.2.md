# Validação experimental — vpw64recomp v0.3.2

Jogo: virtual-pro-wrestling-64
Projeto oficial: vpw64recomp
Repositório: https://github.com/jessetbh/VPW64Recomp
Release: https://github.com/jessetbh/VPW64Recomp/releases/tag/v0.3.2
ZIP oficial: Vpw64Recompiled-v0.3.2-Windows.zip
Tamanho do ZIP baixado: 23100157 bytes
SHA-256 ZIP: 71bad5632916c5725f1d143207aeba36cd6889cf6c9072f1429a8e20e0492e82
Executável: Vpw64Recompiled.exe
Required files: Vpw64Recompiled.exe, SDL2.dll, dxcompiler.dll, dxil.dll, librashader.dll, msvcp140.dll, msvcp140_atomic_wait.dll, vcruntime140.dll, vcruntime140_1.dll
Caminho da receita: recipes/virtual-pro-wrestling-64/vpw64recomp/v0.3.2.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial, caminhos relativos seguros. disasm/vpw64.yaml confirma 16777216 bytes (0x1000000) e SHA-1 f9e9fa2ed819c3a39db5cb6afeca186f021db5ed.
Não testado: instalação ponta a ponta no AllFix.exe com ROM original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima antes de promoção para validated).

Procedimento manual da receita: O pacote oficial e sua ROM verificada vpw64.z64 foram instalados. Abra Vpw64Recompiled.exe na pasta do jogo e escolha vpw64.z64 no botao Load ROM na primeira execucao.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:16:48Z`
- **Pacote baixado e conferido:** `Vpw64Recompiled-v0.3.2-Windows.zip` (`23100157` bytes, SHA-256 `71bad5632916c5725f1d143207aeba36cd6889cf6c9072f1429a8e20e0492e82`)
- **Resultado (`GameInstallationService.Run`):** `extraction_ok_awaiting_media` (`Status=Failed`)
- **Verificação de arquivos:** `9/9` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Execução interrompida na seleção de mídia obrigatória com retorno esperado `Status=Failed` (`A dependência obrigatória não foi selecionada.`) pois não há ROM/ISO comercial local; estrutura do ZIP oficial conferida integralmente (9/9 `required_files` e `launch_file` presentes).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
