# Validação experimental — btgarecomp v0.1.13

Jogo: battletanx-global-assault
Projeto oficial: btgarecomp
Repositório: https://github.com/wootbeer/btgarecomp
Release: https://github.com/wootbeer/btgarecomp/releases/tag/v0.1.13
ZIP oficial: BattleTanxGARecompiled-0.1.13-windows.zip
Tamanho do ZIP baixado: 16783239 bytes
SHA-256 ZIP: fa64ebd1407543754fc55f7a69c335953cb02cfaeef9f93b897e3cb1be3c877e
Executável: BattleTanxGARecompiled.exe
Required files: BattleTanxGARecompiled.exe, SDL2.dll, dxcompiler.dll, dxil.dll
Caminho da receita: recipes/battletanx-global-assault/btgarecomp/v0.1.13.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial, caminhos relativos seguros. syms/rom_info.md confirma 8388608 bytes (8 MiB) e README confirma SHA-1 08a9037488c47d1e26ce6f709955639e9f0f0bb8.
Não testado: instalação ponta a ponta no AllFix.exe com ROM original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima antes de promoção para validated).

Procedimento manual da receita: O pacote oficial BattleTanxGA Recompiled e sua ROM verificada BattleTanxGA.us.z64 foram instalados. Abra BattleTanxGARecompiled.exe e selecione BattleTanxGA.us.z64 na primeira execucao.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:16:39Z`
- **Pacote baixado e conferido:** `BattleTanxGARecompiled-0.1.13-windows.zip` (`16783239` bytes, SHA-256 `fa64ebd1407543754fc55f7a69c335953cb02cfaeef9f93b897e3cb1be3c877e`)
- **Resultado (`GameInstallationService.Run`):** `extraction_ok_awaiting_media` (`Status=Failed`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Execução interrompida na seleção de mídia obrigatória com retorno esperado `Status=Failed` (`A dependência obrigatória não foi selecionada.`) pois não há ROM/ISO comercial local; estrutura do ZIP oficial conferida integralmente (4/4 `required_files` e `launch_file` presentes).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
