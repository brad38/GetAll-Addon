# Validação experimental — recharged v1.1.7

Jogo: mario-strikers-charged
Projeto oficial: recharged
Repositório: https://github.com/previouslevelgames/recharged
Release: https://github.com/previouslevelgames/recharged/releases/tag/v1.1.7
ZIP oficial: recharged-1.1.7+g053746ffc142-windows-x86_64.zip
Tamanho do ZIP baixado: 44127662 bytes
SHA-256 ZIP: a23c8ff90e4821550024eb8ca1701ba82191e10d849ff2e9b4a68e88477b63fc
Executável: recharged.exe
Required files: recharged.exe, d3dcompiler_47.dll, dxcompiler.dll, dxil.dll, recharged_game_us.dll
Caminho da receita: recipes/mario-strikers-charged/recharged/v1.1.7.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP, caminhos relativos. O motor não executou scripts externos.
Não testado: instalação ponta a ponta, importação da ROM/disco original, inicialização do jogo, ação Jogar agora.
Status: experimental (instalação parcial com manual_steps).

Procedimento manual da receita: O pacote oficial Recharged foi extraido. Execute recharged.exe na pasta instalada e, no launcher, adicione a pasta que contem a imagem legitima do disco Mario Strikers Charged (ISO, RVZ ou WBFS de regiao suportada). Clique em Play no launcher. A imagem do disco nao e distribuida nem importada pelo GetAll-Addon.
