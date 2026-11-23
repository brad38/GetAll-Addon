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

Evolução Rodada 1: adicionados inputs verificados (size 33554432, magic_hex 80371240, SHA-1 oficial do README) com import_input para banjo-tooie.us.z64.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:16:32Z`
- **Pacote baixado e conferido:** `BanjoTooieRecompiled-windows-x64.zip` (`20697028` bytes, SHA-256 `cc34db186c61b432505fd2ce38c0686edcc6283a5272a4eb567c85b17cdce53b`)
- **Resultado (`GameInstallationService.Run`):** `extraction_ok_awaiting_media` (`Status=Failed`)
- **Verificação de arquivos:** `5/5` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Execução interrompida na seleção de mídia obrigatória com retorno esperado `Status=Failed` (`A dependência obrigatória não foi selecionada.`) pois não há ROM/ISO comercial local; estrutura do ZIP oficial conferida integralmente (5/5 `required_files` e `launch_file` presentes).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
