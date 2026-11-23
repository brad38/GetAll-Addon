# Validação experimental — earthworm-jim-hd-recompiled v0.9.6

Jogo: earthworm-jim-hd
Projeto oficial: earthworm-jim-hd-recompiled
Repositório: https://github.com/TekRantGaming/earthworm-jim-hd-recompiled
Release: https://github.com/TekRantGaming/earthworm-jim-hd-recompiled/releases/tag/v0.9.6
ZIP oficial: EarthwormJimHD-v0.9.6-windows-x64.zip
Tamanho do ZIP baixado: 32436439 bytes
SHA-256 ZIP: 2c940956830f735b9c9ff31e2e590eb955ad4776ba20606ba1aa3beec8383bc7
Executável: EarthwormJimHD/earthworm_jim_hd.exe
Required files: EarthwormJimHD/earthworm_jim_hd.exe, EarthwormJimHD/rexgpu-xenos.dll, EarthwormJimHD/rexruntime.dll, EarthwormJimHD/README.txt
Caminho da receita: recipes/earthworm-jim-hd/earthworm-jim-hd-recompiled/v0.9.6.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial Earthworm Jim HD Recompiled (v0.9.6) foi extraido. Execute earthworm_jim_hd.exe em EarthwormJimHD/, clique em Install from package... e aponte seu pacote XBLA legitimo (Title ID 584109E2/000D0000/, com default.xex SHA-1 62d9d28a3bce42843607c26ab4b200e91cb31203). Nenhum arquivo comercial e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:18:38Z`
- **Pacote baixado e conferido:** `EarthwormJimHD-v0.9.6-windows-x64.zip` (`32436439` bytes, SHA-256 `2c940956830f735b9c9ff31e2e590eb955ad4776ba20606ba1aa3beec8383bc7`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 4/4 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
