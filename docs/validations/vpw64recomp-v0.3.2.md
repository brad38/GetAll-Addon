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
