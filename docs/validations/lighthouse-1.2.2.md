# Validação experimental — lighthouse 1.2.2

Jogo: banjo-kazooie
Projeto oficial: lighthouse
Repositório: https://github.com/HarbourMasters/Lighthouse
Release: https://github.com/HarbourMasters/Lighthouse/releases/tag/1.2.2
ZIP oficial: Lighthouse-Montauk-Charlie-Win64.zip
Tamanho do ZIP baixado: 36631216 bytes
SHA-256 ZIP: 27c0066b0aa0a75de95974ca21bc86e2eadc3215ffa6a8e8b67e2c572107ae07
Executável: Lighthouse.exe
Required files: Lighthouse.exe, lighthouse.o2r
Caminho da receita: recipes/banjo-kazooie/lighthouse/1.2.2.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP, caminhos relativos. O motor não executou scripts externos.
Não testado: instalação ponta a ponta, importação da ROM/disco original, inicialização do jogo, ação Jogar agora.
Status: experimental (instalação parcial com manual_steps).

Procedimento manual da receita: O pacote oficial Lighthouse foi extraido. Abra Lighthouse.exe na pasta instalada e selecione sua ROM legitima e compativel de Banjo-Kazooie no formato .z64 (US v1.0/v1.1, JP ou PAL, segundo o README). O jogo gera os recursos localmente. Nenhuma ROM e fornecida.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:16:30Z`
- **Pacote baixado e conferido:** `Lighthouse-Montauk-Charlie-Win64.zip` (`36631216` bytes, SHA-256 `27c0066b0aa0a75de95974ca21bc86e2eadc3215ffa6a8e8b67e2c572107ae07`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `2/2` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 2/2 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
