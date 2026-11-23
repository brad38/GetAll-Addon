# Validação experimental — banjo-recompiled v1.0.2

Jogo: banjo-kazooie
Projeto oficial: banjo-recompiled
Repositório: https://github.com/BanjoRecomp/BanjoRecomp
Release: https://github.com/BanjoRecomp/BanjoRecomp/releases/tag/v1.0.2
ZIP oficial: BanjoRecompiled-v1.0.2-Windows.zip
Tamanho do ZIP baixado: 18669475 bytes
SHA-256 ZIP: fc34aad48e06681878bedd13b88d5332a2f21f6a98cafc931c94d54892a4dd92
Executável: BanjoRecompiled.exe
Required files: BanjoRecompiled.exe, dxil.dll, dxcompiler.dll, SDL2.dll
Caminho da receita: recipes/banjo-kazooie/banjo-recompiled/v1.0.2.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP, caminhos relativos. O motor não executou scripts externos.
Não testado: instalação ponta a ponta, importação da ROM/disco original, inicialização do jogo, ação Jogar agora.
Status: experimental (instalação parcial com manual_steps).

Procedimento manual da receita: O pacote oficial Banjo Recompiled foi extraido. Abra BanjoRecompiled.exe na pasta instalada e forneca sua ROM original de Banjo-Kazooie USA v1.0 no menu inicial. O jogo carrega os recursos dessa copia; a ROM nao esta incluida.
