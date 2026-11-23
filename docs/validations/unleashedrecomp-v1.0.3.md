# Validação experimental — unleashedrecomp v1.0.3

Jogo: sonic-unleashed
Projeto oficial: unleashedrecomp
Repositório: https://github.com/hedge-dev/UnleashedRecomp
Release: https://github.com/hedge-dev/UnleashedRecomp/releases/tag/v1.0.3
ZIP oficial: UnleashedRecomp-Windows.zip
Tamanho do ZIP baixado: 53386467 bytes
SHA-256 ZIP: 65793fbf3bfa392703275d3a1759bea20bc3d62f3bb39b066b85e5e7fb2d5d32
Executável: UnleashedRecomp.exe
Required files: UnleashedRecomp.exe, D3D12/D3D12Core.dll, dxcompiler.dll, dxil.dll
Caminho da receita: recipes/sonic-unleashed/unleashedrecomp/v1.0.3.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial Unleashed Recompiled (v1.0.3) foi extraido. Execute UnleashedRecomp.exe para abrir o assistente oficial de instalacao e forneca os arquivos ou conteineres da sua copia original de Sonic Unleashed (Xbox 360 US ou EU, com Title Update obrigatorio e DLCs opcionais). Nenhum arquivo comercial e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:18:13Z`
- **Pacote baixado e conferido:** `UnleashedRecomp-Windows.zip` (`53386467` bytes, SHA-256 `65793fbf3bfa392703275d3a1759bea20bc3d62f3bb39b066b85e5e7fb2d5d32`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 4/4 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
