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

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:16:26Z`
- **Pacote baixado e conferido:** `Paperboat-Mulberry-Delta-Win64.zip` (`27512774` bytes, SHA-256 `ad7a825befbbad2d925f511fc97cfa26027f825935b413040b9d294d953983f3`)
- **Resultado (`GameInstallationService.Run`):** `extraction_ok_awaiting_media` (`Status=Failed`)
- **Verificação de arquivos:** `3/3` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Execução interrompida na seleção de mídia obrigatória com retorno esperado `Status=Failed` (`A dependência obrigatória não foi selecionada.`) pois não há ROM/ISO comercial local; estrutura do ZIP oficial conferida integralmente (3/3 `required_files` e `launch_file` presentes).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
