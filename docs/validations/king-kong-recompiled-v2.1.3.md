# Validação experimental — king-kong-recompiled v2.1.3

Jogo: peter-jackson-s-king-kong
Projeto oficial: king-kong-recompiled
Repositório: https://github.com/TekRantGaming/king-kong-recompiled
Release: https://github.com/TekRantGaming/king-kong-recompiled/releases/tag/v2.1.3
ZIP oficial: KingKong-v2.1.3-windows-x64.zip
Tamanho do ZIP baixado: 421238902 bytes
SHA-256 ZIP: 0284825e36a0e0252d6250fa585d079b8e4bedaa30c7a72bd11778b7e720fe18
Executável: KingKong/king_kong.exe
Required files: KingKong/king_kong.exe, KingKong/amd_fidelityfx_dx12.dll, KingKong/dxcompiler.dll, KingKong/kk-files.txt
Caminho da receita: recipes/peter-jackson-s-king-kong/king-kong-recompiled/v2.1.3.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial King Kong Recompiled (v2.1.3) foi extraido. Execute king_kong.exe em KingKong/, clique em Select disc image e selecione sua imagem de disco original de Peter Jackson's King Kong (Xbox 360, .iso de 7.834.892.288 bytes / SHA-1 oficial 075f43709e9c9a095e099ab5056cc04b768288d1). Nenhum arquivo comercial e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:18:25Z`
- **Pacote baixado e conferido:** `KingKong-v2.1.3-windows-x64.zip` (`421238902` bytes, SHA-256 `0284825e36a0e0252d6250fa585d079b8e4bedaa30c7a72bd11778b7e720fe18`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 4/4 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
