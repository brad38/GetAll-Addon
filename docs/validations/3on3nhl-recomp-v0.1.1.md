# Validação experimental — 3on3nhl-recomp v0.1.1

Jogo: 3-on-3-nhl-arcade
Projeto oficial: 3on3nhl-recomp
Repositório: https://github.com/Wndwsqrrl/3on3NHL-recomp
Release: https://github.com/Wndwsqrrl/3on3NHL-recomp/releases/tag/v0.1.1
ZIP oficial: 3on3NHL-recomp-v0.1.1-win64.zip
Tamanho do ZIP baixado: 91897254 bytes
SHA-256 ZIP: e6231d538a88dea1d67a6a612498d01dce6a1a0a986d53eeb85c7ed8fd6186ab
Executável: nhl3on3/nhl3on3.exe
Required files: nhl3on3/nhl3on3.exe, nhl3on3/rexgpu-xenos.dll, nhl3on3/rexruntime.dll, nhl3on3/nhl3on3.toml
Caminho da receita: recipes/3-on-3-nhl-arcade/3on3nhl-recomp/v0.1.1.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial 3 on 3 NHL Arcade PC Port (v0.1.1) foi extraido. Na configuracao inicial, abra 'NHL 3on3 Launcher.exe' dentro da pasta nhl3on3/, informe seu pacote XBLA legitimo (58410975/000D0000/) e clique em Set up game. Apos a extracao, o jogo inicia diretamente por nhl3on3/nhl3on3.exe. Nenhum arquivo comercial e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:19:03Z`
- **Pacote baixado e conferido:** `3on3NHL-recomp-v0.1.1-win64.zip` (`91897254` bytes, SHA-256 `e6231d538a88dea1d67a6a612498d01dce6a1a0a986d53eeb85c7ed8fd6186ab`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 4/4 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
