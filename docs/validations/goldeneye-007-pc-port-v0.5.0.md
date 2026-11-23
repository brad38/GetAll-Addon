# Validação experimental — goldeneye-007-pc-port v0.5.0

Jogo: goldeneye-007
Projeto oficial: goldeneye-007-pc-port
Repositório: https://github.com/jkdansereau/goldeneye-pc-port
Release: https://github.com/jkdansereau/goldeneye-pc-port/releases/tag/v0.5.0
ZIP oficial: goldeneye-pc-port-0.5.0-win64.zip
Tamanho do ZIP baixado: 17178242 bytes
SHA-256 ZIP: b49bfb826566367a4d1af16466530f0fadd85e522b33859521d849c143a005ef
Caminho da receita: recipes/goldeneye-007/goldeneye-007-pc-port/v0.5.0.json

Status: experimental (aguarda homologação funcional com mídia legítima).

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:20:43Z`
- **Pacote baixado e conferido:** `goldeneye-pc-port-0.5.0-win64.zip` (`17178242` bytes, SHA-256 `b49bfb826566367a4d1af16466530f0fadd85e522b33859521d849c143a005ef`)
- **Resultado (`GameInstallationService.Run`):** `extraction_ok_awaiting_media` (`Status=Failed`)
- **Verificação de arquivos:** `7/7` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Execução interrompida na seleção de mídia obrigatória com retorno esperado `Status=Failed` (`A dependência obrigatória não foi selecionada.`) pois não há ROM/ISO comercial local; estrutura do ZIP oficial conferida integralmente (7/7 `required_files` e `launch_file` presentes). Subdiretórios de destino criados automaticamente pelo motor na importação: goldeneye-pc-port-0.5.0-win64/data/.
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
