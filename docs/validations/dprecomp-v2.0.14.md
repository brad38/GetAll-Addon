# Validação experimental — dprecomp v2.0.14

Jogo: deadly-premonition
Projeto oficial: dprecomp
Repositório: https://github.com/LittleBitUA/DPRecomp
Release: https://github.com/LittleBitUA/DPRecomp/releases/tag/v2.0.14
ZIP oficial: DPRecomp-2.0.14-win64.zip
Tamanho do ZIP baixado: 46811589 bytes
SHA-256 ZIP: 3d26da25ff910cc2c41b4d2f7d5a8d6c17f6a3e4e2a9a29d2e4afee5e38b75fe
Executável: DPRecomp-2.0.14-win64/PlayDeadlyPremonition.exe
Required files: DPRecomp-2.0.14-win64/PlayDeadlyPremonition.exe, DPRecomp-2.0.14-win64/deadlyprem.exe, DPRecomp-2.0.14-win64/deadlyprem_usa.exe, DPRecomp-2.0.14-win64/rexruntimerd.dll, DPRecomp-2.0.14-win64/deadlyprem.toml
Caminho da receita: recipes/deadly-premonition/dprecomp/v2.0.14.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial Deadly Premonition Recompilation (v2.0.14) foi extraido. Execute PlayDeadlyPremonition.exe em DPRecomp-2.0.14-win64/ e selecione sua imagem .iso original (PAL ou USA Xbox 360) no instalador inicial (ou copie seu dump com default.xex para assets/). Nenhum arquivo comercial e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:18:22Z`
- **Pacote baixado e conferido:** `DPRecomp-2.0.14-win64.zip` (`46811589` bytes, SHA-256 `3d26da25ff910cc2c41b4d2f7d5a8d6c17f6a3e4e2a9a29d2e4afee5e38b75fe`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `5/5` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 5/5 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
