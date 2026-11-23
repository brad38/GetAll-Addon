# Validação experimental — spaghettikart 1.0.0

Jogo: mario-kart-64
Projeto oficial: spaghettikart
Repositório: https://github.com/HarbourMasters/SpaghettiKart
Release: https://github.com/HarbourMasters/SpaghettiKart/releases/tag/1.0.0
ZIP oficial: spaghetti-windows.zip
Tamanho do ZIP baixado: 7806456 bytes
SHA-256 ZIP: bf7bd7cdb5f412c7b370af92949b9431ce7503968631f8cacd607933fb32aff3
Executável: Spaghettify.exe
Required files: Spaghettify.exe, spaghetti.o2r
Caminho da receita: recipes/mario-kart-64/spaghettikart/1.0.0.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP, caminhos relativos. O motor não executou scripts externos.
Não testado: instalação ponta a ponta, importação da ROM/disco original, inicialização do jogo, ação Jogar agora.
Status: experimental (instalação parcial com manual_steps).

Procedimento manual da receita: O pacote oficial SpaghettiKart foi extraido. Execute Spaghettify.exe na pasta instalada e selecione sua ROM original de Mario Kart 64 USA no formato .z64. O jogo valida a copia e gera seus recursos em disco; nenhuma ROM e distribuida.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:16:26Z`
- **Pacote baixado e conferido:** `spaghetti-windows.zip` (`7806456` bytes, SHA-256 `bf7bd7cdb5f412c7b370af92949b9431ce7503968631f8cacd607933fb32aff3`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `2/2` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 2/2 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
