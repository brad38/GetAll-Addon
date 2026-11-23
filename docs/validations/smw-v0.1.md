# Validação experimental — smw v0.1

Jogo: super-mario-world
Projeto oficial: smw
Repositório: https://github.com/snesrev/smw
Release: https://github.com/snesrev/smw/releases/tag/v0.1
ZIP oficial: smw_0.1.zip
Tamanho do ZIP baixado: 1742607 bytes
SHA-256 ZIP: f2086306d1e93617569ffca4fe010d43578ab41625dab456c3d63b2492b30db3
Executável: smw.exe
Required files: smw.exe, SDL2.dll, smw.ini, smw_assets.bps
Caminho da receita: recipes/super-mario-world/smw/v0.1.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial smw (v0.1) foi extraido. Copie sua ROM USA original de Super Mario World nomeada exatamente como smw.sfc para a pasta raiz instalada (ao lado de smw.exe e smw_assets.bps) e inicie smw.exe. Nenhum arquivo comercial e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:19:09Z`
- **Pacote baixado e conferido:** `smw_0.1.zip` (`1742607` bytes, SHA-256 `f2086306d1e93617569ffca4fe010d43578ab41625dab456c3d63b2492b30db3`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 4/4 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
