# Validação experimental — dusklight-ex-dusk v2.0.3

Jogo: the-legend-of-zelda-twilight-princess
Projeto oficial: dusklight-ex-dusk
Repositório: https://github.com/TwilitRealm/dusklight
Release: https://github.com/TwilitRealm/dusklight/releases/tag/v2.0.3
ZIP oficial: Dusklight-v2.0.3-win32-x86_64.zip
Tamanho do ZIP baixado: 56037777 bytes
SHA-256 ZIP: ac63514eeb13cd4e9bd22be02dabee4952d1331a78f0496326bba2b577b12caf
Executável: dusklight.exe
Required files: dusklight.exe, SDL3.dll, dxcompiler.dll, dxil.dll, nod.dll
Caminho da receita: recipes/the-legend-of-zelda-twilight-princess/dusklight-ex-dusk/v2.0.3.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial Dusklight (v2.0.3) foi extraido. Execute dusklight.exe e informe sua imagem de disco original de The Legend of Zelda: Twilight Princess (.iso ou .rvz) no assistente inicial. Nenhum arquivo comercial e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:18:07Z`
- **Pacote baixado e conferido:** `Dusklight-v2.0.3-win32-x86_64.zip` (`56037777` bytes, SHA-256 `ac63514eeb13cd4e9bd22be02dabee4952d1331a78f0496326bba2b577b12caf`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `5/5` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 5/5 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
