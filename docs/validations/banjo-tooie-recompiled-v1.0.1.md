# Validação experimental — banjo-tooie-recompiled v1.0.1

Jogo: banjo-tooie
Projeto oficial: banjo-tooie-recompiled
Repositório: https://github.com/Vidanox/BanjoTooieRecompiled
Release: https://github.com/Vidanox/BanjoTooieRecompiled/releases/tag/v1.0.1
ZIP oficial: BanjoTooieRecompiled-windows-x64.zip
Tamanho do ZIP baixado: 20697028 bytes
SHA-256 ZIP: cc34db186c61b432505fd2ce38c0686edcc6283a5272a4eb567c85b17cdce53b
Executável: BanjoTooieRecompiled.exe
Required files: BanjoTooieRecompiled.exe, dxcompiler.dll, dxil.dll, SDL2.dll, assets/LatoLatin-Regular.ttf
Caminho da receita: recipes/banjo-tooie/banjo-tooie-recompiled/v1.0.1.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP, caminhos relativos. O motor não executou scripts externos.
Não testado: instalação ponta a ponta, importação da ROM/disco original, inicialização do jogo, ação Jogar agora.
Status: experimental (instalação parcial com manual_steps).

Procedimento manual da receita: O pacote oficial Banjo-Tooie Recompiled foi extraido. Execute BanjoTooieRecompiled.exe a partir da pasta instalada, que contem assets/, e escolha Select ROM no primeiro uso. Use sua ROM original USA .z64 de 33554432 bytes (SHA-1 AF1A89E12B638B8D82CC4C085C8E01D4CBA03FB3). O jogo le a ROM sem copia-la; nenhuma ROM e distribuida.
