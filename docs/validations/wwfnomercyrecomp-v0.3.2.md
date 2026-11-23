# Validação experimental — wwfnomercyrecomp v0.3.2

Jogo: wwf-no-mercy
Projeto oficial: wwfnomercyrecomp
Repositório: https://github.com/jessetbh/WWFNoMercyRecomp
Release: https://github.com/jessetbh/WWFNoMercyRecomp/releases/tag/v0.3.2
ZIP oficial: NoMercyRecompiled-v0.3.2-Windows.zip
Tamanho do ZIP baixado: 29234117 bytes
SHA-256 ZIP: 8cefdcca49c582dc2a7e10ea925c16d761e1b0bb6249f49e8e80eb220ccf23bd
Executável: NoMercyRecompiled.exe
Required files: NoMercyRecompiled.exe, SDL2.dll, dxcompiler.dll, dxil.dll, librashader.dll, msvcp140.dll, msvcp140_atomic_wait.dll, vcruntime140.dll, vcruntime140_1.dll
Caminho da receita: recipes/wwf-no-mercy/wwfnomercyrecomp/v0.3.2.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial, caminhos relativos seguros. disasm/nomercy.yaml confirma 33554432 bytes (0x2000000) e SHA-1 91cee3d096f4a76644d8b35b9aead6448909abd1.
Não testado: instalação ponta a ponta no AllFix.exe com ROM original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima antes de promoção para validated).

Procedimento manual da receita: O pacote oficial e sua ROM verificada nomercy.z64 foram instalados. Abra NoMercyRecompiled.exe na pasta do jogo e escolha nomercy.z64 no botao Load ROM na primeira execucao.
