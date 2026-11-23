# Validação experimental — ghostship 3.0.0

Jogo: super-mario-64
Projeto oficial: ghostship
Repositório: https://github.com/HarbourMasters/Ghostship
Release: https://github.com/HarbourMasters/Ghostship/releases/tag/3.0.0
ZIP oficial: Nautilus-Alfa-Win64.zip
Tamanho do ZIP baixado: 20379303 bytes
SHA-256 ZIP: 49a0ab6c6624ccb20d29bb433f391d017f638f2b7db0601eae7808574a62aa18
Executável: Ghostship.exe
Required files: Ghostship.exe, ghostship.o2r, shaderc_shared.dll, tcc.dll
Caminho da receita: recipes/super-mario-64/ghostship/3.0.0.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP, caminhos relativos. O motor não executou scripts externos.
Não testado: instalação ponta a ponta, importação da ROM/disco original, inicialização do jogo, ação Jogar agora.
Status: experimental (instalação parcial com manual_steps).

Procedimento manual da receita: O pacote oficial do Ghostship foi extraido. Para jogar, abra Ghostship.exe a partir da pasta do jogo e selecione sua propria ROM legitima de Super Mario 64 US ou JP, formato .z64. O jogo valida a ROM e gera os recursos localmente. Nenhuma ROM e fornecida pelo GetAll-Addon.
