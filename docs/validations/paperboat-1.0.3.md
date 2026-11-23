# Validação experimental — paperboat 1.0.3

Jogo: paper-mario
Projeto oficial: paperboat
Repositório: https://github.com/HarbourMasters/PaperBoat
Release: https://github.com/HarbourMasters/PaperBoat/releases/tag/1.0.3
ZIP oficial: Paperboat-Mulberry-Delta-Win64.zip
Tamanho do ZIP baixado: 27512774 bytes
SHA-256 ZIP: ad7a825befbbad2d925f511fc97cfa26027f825935b413040b9d294d953983f3
Executável: Paperboat.exe
Required files: Paperboat.exe, paperboat.o2r, shaderc_shared.dll
Caminho da receita: recipes/paper-mario/paperboat/1.0.3.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP, caminhos relativos. O motor não executou scripts externos.
Não testado: instalação ponta a ponta, importação da ROM/disco original, inicialização do jogo, ação Jogar agora.
Status: experimental (instalação parcial com manual_steps).

Procedimento manual da receita: O pacote oficial PaperBoat foi extraido. Para concluir a primeira inicializacao, abra Paperboat.exe na pasta do jogo e forneca sua ROM legitima e compativel de Paper Mario USA quando solicitada. O projeto faz a importacao de recursos no proprio aplicativo. Nenhuma ROM e distribuida.

Evolução Rodada 2: tamanho 41943040 bytes (0x2800000) confirmado em pmret/papermario/ver/us/splat.yaml; adicionados inputs verificados + import_input para baserom.us.z64.
