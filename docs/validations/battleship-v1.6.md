# Validação experimental — battleship v1.6

Jogo: super-smash-bros
Projeto oficial: battleship
Repositório: https://github.com/JRickey/BattleShip
Release: https://github.com/JRickey/BattleShip/releases/tag/v1.6
ZIP oficial: BattleShip-windows.zip
Tamanho do ZIP baixado: 8818427 bytes
SHA-256 ZIP: a0c2ef997e7f561dc02da19b0e1134ecb9bfaac1d577d65ff04db3c7e27eadb4
Executável: BattleShip.exe
Required files: BattleShip.exe, torch.exe, f3d.o2r
Caminho da receita: recipes/super-smash-bros/battleship/v1.6.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial, caminhos relativos seguros. ZIP contem BattleShip.exe, torch.exe e f3d.o2r; README confirma SHA-1 US e JP sem tamanho numerico de ROM documentado.
Não testado: instalação ponta a ponta no AllFix.exe com ROM original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima antes de promoção para validated).

Procedimento manual da receita: O pacote oficial BattleShip (US) foi extraido. Execute BattleShip.exe na pasta instalada e forneca sua ROM legitima de Super Smash Bros. NTSC-U v1.0 (SHA-1 e2929e10fccc0aa84e5776227e798abc07cedabf) no assistente inicial para gerar BattleShip.o2r localmente.

Evolução Rodada 2: tamanho 16777216 bytes (0x1000000) confirmado em VetriTheRetri/ssb-decomp-re/smashbrothers.us.yaml; adicionados inputs verificados + import_input para baserom.us.z64.
