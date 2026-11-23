# Validação experimental — zelda3 v0.3

Jogo: the-legend-of-zelda-a-link-to-the-past
Projeto oficial: zelda3
Repositório: https://github.com/snesrev/zelda3
Release: https://github.com/snesrev/zelda3/releases/tag/v0.3
ZIP oficial: zelda3_v0.3.zip
Tamanho do ZIP baixado: 1847661 bytes
SHA-256 ZIP: 0d8709a4a2731920f44f1ea662d665c8c5c223c40f18865692bd6b1602250fb6
Executável: zelda3.exe
Required files: zelda3.exe, SDL2.dll, zelda3.ini, zelda3_assets.bps
Caminho da receita: recipes/the-legend-of-zelda-a-link-to-the-past/zelda3/v0.3.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial Zelda3 (v0.3) foi extraido. Conforme as notas da release oficial, copie sua ROM USA original de The Legend of Zelda: A Link to the Past nomeada exatamente como zelda3.sfc para a pasta raiz instalada (ao lado de zelda3.exe e zelda3_assets.bps) e inicie zelda3.exe. Nenhum arquivo comercial e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:19:09Z`
- **Pacote baixado e conferido:** `zelda3_v0.3.zip` (`1847661` bytes, SHA-256 `0d8709a4a2731920f44f1ea662d665c8c5c223c40f18865692bd6b1602250fb6`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 4/4 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
