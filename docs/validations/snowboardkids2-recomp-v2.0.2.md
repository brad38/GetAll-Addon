# Validação experimental — snowboardkids2-recomp v2.0.2

Jogo: snowboard-kids-2
Projeto oficial: snowboardkids2-recomp
Repositório: https://github.com/cdlewis/snowboardkids2-recomp
Release: https://github.com/cdlewis/snowboardkids2-recomp/releases/tag/v2.0.2
ZIP oficial: SnowboardKids2Recompiled-Windows.zip
Tamanho do ZIP baixado: 20071009 bytes
SHA-256 ZIP: 51b0c78e758d334eeab2f6aab0eec94daf75d30f7a430375d8bea5f5c26e2414
Executável: SnowboardKids2Recompiled.exe
Required files: SnowboardKids2Recompiled.exe, SDL2.dll, dxcompiler.dll, dxil.dll
Caminho da receita: recipes/snowboard-kids-2/snowboardkids2-recomp/v2.0.2.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros.
Não testado: instalação ponta a ponta no AllFix.exe com ROM original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial de Snowboard Kids 2 (v2.0.2) foi extraido. Execute SnowboardKids2Recompiled.exe na pasta instalada e Forneca sua ROM original de Snowboard Kids 2 (US) no menu inicial. Nenhuma ROM e fornecida pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:17:15Z`
- **Pacote baixado e conferido:** `SnowboardKids2Recompiled-Windows.zip` (`20071009` bytes, SHA-256 `51b0c78e758d334eeab2f6aab0eec94daf75d30f7a430375d8bea5f5c26e2414`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 4/4 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
