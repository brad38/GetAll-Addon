# Validação experimental — re-blue nightly-v1.4.0-d187173d8-s44b7fdc5

Jogo: blue-dragon
Projeto oficial: re-blue
Repositório: https://github.com/zolaware/reblue
Release: https://github.com/zolaware/reblue/releases/tag/nightly-v1.4.0-d187173d8-s44b7fdc5
ZIP oficial: reblue-1.4.0-dev-187173d8-44b7fdc5-win-amd64.zip
Tamanho do ZIP baixado: 40199273 bytes
SHA-256 ZIP: 57f9c40edf30c6b83462eb0004f64e8a1f0f7e31c59a898175a281d34825cb47
Executável: reblue.exe
Required files: reblue.exe, reblue_vk.exe, SDL3.dll, rexapp.dll, D3D12/D3D12Core.dll
Caminho da receita: recipes/blue-dragon/re-blue/nightly-v1.4.0-d187173d8-s44b7fdc5.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial re:Blue (nightly-v1.4.0-d187173d8-s44b7fdc5) foi extraido. Execute reblue.exe (ou reblue_vk.exe para Vulkan) e selecione as 3 imagens .iso originais de Blue Dragon (Xbox 360) no assistente inicial. Nenhum arquivo comercial e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:18:17Z`
- **Pacote baixado e conferido:** `reblue-1.4.0-dev-187173d8-44b7fdc5-win-amd64.zip` (`40199273` bytes, SHA-256 `57f9c40edf30c6b83462eb0004f64e8a1f0f7e31c59a898175a281d34825cb47`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `5/5` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 5/5 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
