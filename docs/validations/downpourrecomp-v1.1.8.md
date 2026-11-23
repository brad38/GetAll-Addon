# Validação experimental — downpourrecomp v1.1.8

Jogo: silent-hill-downpour
Projeto oficial: downpourrecomp
Repositório: https://github.com/LittleBitUA/DownpourRecomp
Release: https://github.com/LittleBitUA/DownpourRecomp/releases/tag/v1.1.8
ZIP oficial: DownpourRecomp-v1.1.8.zip
Tamanho do ZIP baixado: 41369153 bytes
SHA-256 ZIP: a07d770f34b95f68a2329b279927d329beb067975406fc64eb69478f7703e810
Executável: PlayDownpour.exe
Required files: PlayDownpour.exe, downpour.exe, rexruntimerd.dll, amd_fidelityfx_dx12drel.dll, downpour.toml
Caminho da receita: recipes/silent-hill-downpour/downpourrecomp/v1.1.8.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial DownpourRecomp (v1.1.8) foi extraido. Execute PlayDownpour.exe e aponte sua imagem .iso original de Silent Hill: Downpour (Xbox 360) no assistente de primeira execucao (ou extraia o dump conforme README.txt). Nenhum arquivo comercial e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:18:20Z`
- **Pacote baixado e conferido:** `DownpourRecomp-v1.1.8.zip` (`41369153` bytes, SHA-256 `a07d770f34b95f68a2329b279927d329beb067975406fc64eb69478f7703e810`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `5/5` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 5/5 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
