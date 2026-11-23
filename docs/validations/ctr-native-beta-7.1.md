# Validação experimental — ctr-native beta-7.1

Jogo: crash-team-racing
Projeto oficial: ctr-native
Repositório: https://github.com/CTR-tools/ctr-native
Release: https://github.com/CTR-tools/ctr-native/releases/tag/beta-7.1
ZIP oficial: ctr-native-beta-7_1-windows-x86.zip
Tamanho do ZIP baixado: 8746455 bytes
SHA-256 ZIP: af0d23c7b41925917b5eaf6fc292bd172368efc1c68918755de527a664049dad
Executável: ctr-native-beta-7_1-windows-x86/ctr_native.exe
Required files: ctr-native-beta-7_1-windows-x86/ctr_native.exe
Caminho da receita: recipes/crash-team-racing/ctr-native/beta-7.1.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial de Crash Team Racing (beta-7.1) foi extraido. Para jogar, copie sua imagem BIN NTSC-U bruta (MODE2/2352) como assets/ctr-u.bin dentro de ctr-native-beta-7_1-windows-x86/ antes de iniciar ctr_native.exe. Nenhum arquivo comercial ou ROM e distribuido pelo GetAll-Addon.
