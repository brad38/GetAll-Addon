# Validação experimental — battletanx-global-assault-pc-port v0.2.5

Jogo: battletanx-global-assault
Projeto oficial: battletanx-global-assault-pc-port
Repositório: https://github.com/TheGh0stShip/BattleTanx-Global-Assault-PC-Port
Release: https://github.com/TheGh0stShip/BattleTanx-Global-Assault-PC-Port/releases/tag/v0.2.5
ZIP oficial: BattleTanxGA-0.2.5-windows-x64-portable.zip
Tamanho do ZIP baixado: 13559683 bytes
SHA-256 ZIP: 1e4cebcdf9e38e5f24917148c25a2181b4e7df3f8c236f54734d706a3a91c8fc
Executável: BattleTanxGA-0.2.5-windows-x64-portable/BattleTanxGA.exe
Required files: BattleTanxGA-0.2.5-windows-x64-portable/BattleTanxGA.exe, BattleTanxGA-0.2.5-windows-x64-portable/SDL2.dll, BattleTanxGA-0.2.5-windows-x64-portable/dxcompiler.dll, BattleTanxGA-0.2.5-windows-x64-portable/dxil.dll
Caminho da receita: recipes/battletanx-global-assault/battletanx-global-assault-pc-port/v0.2.5.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP, caminhos relativos. O motor não executou scripts externos.
Não testado: instalação ponta a ponta, importação da ROM/disco original, inicialização do jogo, ação Jogar agora.
Status: experimental (instalação parcial com manual_steps).

Procedimento manual da receita: O pacote oficial BattleTanx Global Assault PC Port foi extraido. Abra BattleTanxGA.exe a partir da subpasta original da Release, selecione sua ROM legitima BattleTanx Global Assault USA Rev 0 .z64 no primeiro uso e conclua a verificacao realizada pelo proprio jogo. O programa usa diretamente o caminho da ROM. Nenhuma ROM e incluida.

Evolução Rodada 1: adicionados inputs verificados (size 8388608, magic_hex 80371240, SHA-1 e SHA-256 oficiais do README) com import_input para BattleTanxGA-0.2.5-windows-x64-portable/BattleTanxGA.z64.
