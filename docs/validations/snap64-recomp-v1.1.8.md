# Validação experimental — snap64-recomp v1.1.8

Jogo: pokemon-snap
Projeto oficial: snap64-recomp
Repositório: https://github.com/JackandBeans/Snap64Recomp
Release: https://github.com/JackandBeans/Snap64Recomp/releases/tag/v1.1.8
ZIP oficial: Snap64Recomp-1.1.8-win64.zip
Tamanho do ZIP baixado: 18856540 bytes
SHA-256 ZIP: 7045e8c056a933c28d2311a9255e3011e88ceba81360d62a13a5a0d50d7e8fc4
Executável: Snap64Recomp-1.1.8-win64/Snap64Recomp.exe
Required files: Snap64Recomp-1.1.8-win64/Snap64Recomp.exe, Snap64Recomp-1.1.8-win64/SDL2.dll, Snap64Recomp-1.1.8-win64/dxcompiler.dll, Snap64Recomp-1.1.8-win64/dxil.dll
Caminho da receita: recipes/pokemon-snap/snap64-recomp/v1.1.8.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial, caminhos relativos seguros. Caminho do executavel e DLLs verificados no ZIP oficial; README e src/paths.cpp confirmam carga automatica de pokemonsnap.z64 na pasta instalada (sem tamanho em bytes publicado para o schema v3).
Não testado: instalação ponta a ponta no AllFix.exe com ROM original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima antes de promoção para validated).

Procedimento manual da receita: O pacote oficial Snap64 Recomp foi extraido em Snap64Recomp-1.1.8-win64/. Copie sua ROM legitima de Pokemon Snap (US, SHA-1 edc7c49cc568c045fe48be0d18011c30f393cbaf) como pokemonsnap.z64 ao lado de Snap64Recomp.exe, ou abra o executavel para seleciona-la uma unica vez.
