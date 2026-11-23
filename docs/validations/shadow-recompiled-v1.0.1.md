# Validação experimental — shadow-recompiled v1.0.1

Jogo: shadow-the-hedgehog
Projeto oficial: shadow-recompiled
Repositório: https://github.com/FoxWorkshop/ShadowRecomp
Release: https://github.com/FoxWorkshop/ShadowRecomp/releases/tag/v1.0.1
ZIP oficial: ShadowRecomp-Windows-x64-v1.0.1.zip
Tamanho do ZIP baixado: 30749796 bytes
SHA-256 ZIP: e8cf3cd210e8ba44e10980b0a3587644db715b782ce72dc7c773c07ba81767a3
Executável: ShadowRecomp.exe
Required files: ShadowRecomp.exe, D3D12/D3D12Core.dll, dxcompiler.dll, dxil.dll
Caminho da receita: recipes/shadow-the-hedgehog/shadow-recompiled/v1.0.1.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial Shadow Recompiled (v1.0.1) foi extraido. Execute ShadowRecomp.exe para abrir o instalador integrado e forneca os arquivos da sua copia original de Shadow the Hedgehog (Xbox original). Nenhum arquivo comercial e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:18:16Z`
- **Pacote baixado e conferido:** `ShadowRecomp-Windows-x64-v1.0.1.zip` (`30749796` bytes, SHA-256 `e8cf3cd210e8ba44e10980b0a3587644db715b782ce72dc7c773c07ba81767a3`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 4/4 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
