# Validação experimental — ship-of-harkinian-soh 9.3.1

Jogo: the-legend-of-zelda-ocarina-of-time
Projeto oficial: ship-of-harkinian-soh
Repositório: https://github.com/HarbourMasters/Shipwright
Release: https://github.com/HarbourMasters/Shipwright/releases/tag/9.3.1
ZIP oficial: SoH-Dewey-Bravo-Win64.zip
Tamanho do ZIP baixado: 72980600 bytes
SHA-256 ZIP: 429292a0bfbdfcda283b33c1538ecdc49163b9ed53e8702cac80b2489d9fe26c
Executável: soh.exe
Required files: soh.exe, soh.o2r
Caminho da receita: recipes/the-legend-of-zelda-ocarina-of-time/ship-of-harkinian-soh/9.3.1.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP, caminhos relativos. O motor não executou scripts externos.
Não testado: instalação ponta a ponta, importação da ROM/disco original, inicialização do jogo, ação Jogar agora.
Status: experimental (instalação parcial com manual_steps).

Procedimento manual da receita: O pacote oficial Ship of Harkinian foi extraido. Para concluir o primeiro uso, abra soh.exe na pasta instalada e selecione uma ROM legitima e compativel de Zelda Ocarina of Time quando solicitado; consulte ship.equipment para verificar sua ROM. O jogo extrai os recursos localmente; nao ha ROM ou ativos comerciais no pacote.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:15:52Z`
- **Pacote baixado e conferido:** `SoH-Dewey-Bravo-Win64.zip` (`72980600` bytes, SHA-256 `429292a0bfbdfcda283b33c1538ecdc49163b9ed53e8702cac80b2489d9fe26c`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `2/2` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 2/2 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
