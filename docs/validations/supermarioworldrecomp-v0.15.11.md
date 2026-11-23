# Validação experimental — supermarioworldrecomp v0.15.11

Jogo: super-mario-world
Projeto oficial: supermarioworldrecomp
Repositório: https://github.com/mstan/SuperMarioWorldRecomp
Release: https://github.com/mstan/SuperMarioWorldRecomp/releases/tag/v0.15.11
ZIP oficial: SuperMarioWorldRecomp-windows-x64-v0.15.11.zip
Tamanho do ZIP baixado: 25787143 bytes
SHA-256 ZIP: c4c0933bcbbf575ce1d74389b7ce89c9e34960aed395c18764683c483ecdc5cd
Executável: SuperMarioWorldSNESRecomp.exe
Required files: SuperMarioWorldSNESRecomp.exe, SDL3.dll, libiconv-2.dll
Caminho da receita: recipes/super-mario-world/supermarioworldrecomp/v0.15.11.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial de Super Mario World (v0.15.11) foi extraido. Para jogar, selecione sua ROM original de Super Mario World (USA, .sfc/.smc) no assistente inicial. Nenhum arquivo comercial ou ROM e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:17:23Z`
- **Pacote baixado e conferido:** `SuperMarioWorldRecomp-windows-x64-v0.15.11.zip` (`25787143` bytes, SHA-256 `c4c0933bcbbf575ce1d74389b7ce89c9e34960aed395c18764683c483ecdc5cd`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `3/3` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 3/3 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
