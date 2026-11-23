# Validação experimental — the-darkness-recomp v0.1.10

Jogo: the-darkness
Projeto oficial: the-darkness-recomp
Repositório: https://github.com/portingpete/The-Darkness-Recomp
Release: https://github.com/portingpete/The-Darkness-Recomp/releases/tag/v0.1.10
ZIP oficial: The-Darkness-Recomp-v0.1.10-windows-x64.zip
Tamanho do ZIP baixado: 41776055 bytes
SHA-256 ZIP: 46773f866bbbaac51fec5f958d2dc7dcdc8cc7624503fbee771e7e89eb07dec3
Executável: build_native/Release/DarkRecomp.exe
Required files: build_native/Release/DarkRecomp.exe, build_native/Release/DarkRecompPreview.exe, build_native/Release/avcodec-darkxma-62.dll, build_native/Release/avutil-darkxma-60.dll, Launch.cmd
Caminho da receita: recipes/the-darkness/the-darkness-recomp/v0.1.10.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial The Darkness Recomp (v0.1.10) foi extraido. Antes de iniciar, copie todos os arquivos e pastas extraidos do seu dump original de The Darkness (Xbox 360), incluindo default.xex, Content e System, diretamente para a subpasta Darkness/ (nao use um arquivo .iso diretamente). Voce tambem pode usar Launch.cmd ou LaunchWithSettings.cmd na raiz instalada. Nenhum arquivo comercial e distribuido pelo GetAll-Addon.
