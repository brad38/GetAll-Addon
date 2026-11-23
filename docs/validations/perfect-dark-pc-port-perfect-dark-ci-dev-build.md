# Validação experimental — perfect-dark-pc-port-perfect-dark ci-dev-build

Jogo: perfect-dark
Projeto oficial: perfect-dark-pc-port-perfect-dark
Repositório: https://github.com/perfect-dark-pc-port/perfect_dark
Release: https://github.com/perfect-dark-pc-port/perfect_dark/releases/tag/ci-dev-build
ZIP oficial: pd-x86_64-windows.zip
Tamanho do ZIP baixado: 25739820 bytes
SHA-256 ZIP: 56e6a2f8bad36bd90f0d396c1d525b953adcc1a20157f594b90a7530d58258d3
Executável: pd-x86_64-windows/pd.x86_64.exe
Required files: pd-x86_64-windows/pd.x86_64.exe, pd-x86_64-windows/pd.pal.x86_64.exe, pd-x86_64-windows/pd.jpn.x86_64.exe, pd-x86_64-windows/SDL2.dll, pd-x86_64-windows/libgcc_s_seh-1.dll, pd-x86_64-windows/libwinpthread-1.dll, pd-x86_64-windows/zlib1.dll
Caminho da receita: recipes/perfect-dark/perfect-dark-pc-port-perfect-dark/ci-dev-build.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. port/src/romdata.c confirma ROMDATA_ROM_SIZE=33554432 e caminho data/pd.ntsc-final.z64 (Classe A estrutural sem etapas manuais).
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Correção pós-teste no AllFix.dll: o motor C# rejeitou import_input sem sha1/sha256 ('Operação incompatível'); como o projeto oficial publica apenas MD5, ajustado para manual_steps e registrado pedido de suporte a md5 em inputs para o Codex.
