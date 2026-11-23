# Validação experimental — marathon-recompiled v1.0.0

Jogo: sonic-the-hedgehog-2006
Projeto oficial: marathon-recompiled
Repositório: https://github.com/sonicnext-dev/MarathonRecomp
Release: https://github.com/sonicnext-dev/MarathonRecomp/releases/tag/v1.0.0
ZIP oficial: MarathonRecomp-Windows-x64.zip
Tamanho do ZIP baixado: 37884609 bytes
SHA-256 ZIP: e6ec48456fc9708af90bb9a227bcb7e28d0923c77633751381178a8340ceaa4d
Executável: MarathonRecomp.exe
Required files: MarathonRecomp.exe, D3D12/D3D12Core.dll, dxcompiler.dll, dxil.dll
Caminho da receita: recipes/sonic-the-hedgehog-2006/marathon-recompiled/v1.0.0.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial Marathon Recompiled (v1.0.0) foi extraido. Execute MarathonRecomp.exe e siga o assistente integrado para selecionar seus arquivos ou imagem original de Sonic the Hedgehog (2006) para Xbox 360. Nenhum arquivo comercial e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:18:15Z`
- **Pacote baixado e conferido:** `MarathonRecomp-Windows-x64.zip` (`37884609` bytes, SHA-256 `e6ec48456fc9708af90bb9a227bcb7e28d0923c77633751381178a8340ceaa4d`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 4/4 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
