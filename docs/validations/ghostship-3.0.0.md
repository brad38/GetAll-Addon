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

Evolução Rodada 1: adicionados inputs verificados (size 8388608, magic_hex 80371240, SHA-1 oficial) com import_input para baserom.us.z64 (detectado automaticamente pelo GameExtractor).

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:15:50Z`
- **Pacote baixado e conferido:** `Nautilus-Alfa-Win64.zip` (`20379303` bytes, SHA-256 `49a0ab6c6624ccb20d29bb433f391d017f638f2b7db0601eae7808574a62aa18`)
- **Resultado (`GameInstallationService.Run`):** `extraction_ok_awaiting_media` (`Status=Failed`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Execução interrompida na seleção de mídia obrigatória com retorno esperado `Status=Failed` (`A dependência obrigatória não foi selecionada.`) pois não há ROM/ISO comercial local; estrutura do ZIP oficial conferida integralmente (4/4 `required_files` e `launch_file` presentes).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
