# Validação experimental — starship v2.0.0

Jogo: star-fox-64
Projeto oficial: starship
Repositório: https://github.com/HarbourMasters/Starship
Release: https://github.com/HarbourMasters/Starship/releases/tag/v2.0.0
ZIP oficial: Starship-Barnard-Alfa-Windows.zip
Tamanho do ZIP baixado: 4218590 bytes
SHA-256 ZIP: 42444eeccda0406cb40826ebce0b6f7a46338a9dc25c8e9d9a536807d504ae6a
Executável: Starship.exe
Required files: Starship.exe, starship.o2r
Caminho da receita: recipes/star-fox-64/starship/v2.0.0.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP, caminhos relativos. O motor não executou scripts externos.
Não testado: instalação ponta a ponta, importação da ROM/disco original, inicialização do jogo, ação Jogar agora.
Status: experimental (instalação parcial com manual_steps).

Procedimento manual da receita: O pacote oficial Starship foi extraido. Para jogar, abra Starship.exe na pasta instalada e selecione sua ROM original de Star Fox 64 USA v1.0 ou v1.1 em formato .z64; o projeto cria os recursos localmente. ROMs JP/EU nao sao aceitas como base. Nenhuma ROM e fornecida.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:16:25Z`
- **Pacote baixado e conferido:** `Starship-Barnard-Alfa-Windows.zip` (`4218590` bytes, SHA-256 `42444eeccda0406cb40826ebce0b6f7a46338a9dc25c8e9d9a536807d504ae6a`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `2/2` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 2/2 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
