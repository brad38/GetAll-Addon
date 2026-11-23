# Validação experimental — adam-s-ant-farm v0.11.14

Jogo: body-harvest
Projeto oficial: adam-s-ant-farm
Repositório: https://github.com/LunarLaurus/adams-ant-farm-recomp
Release: https://github.com/LunarLaurus/adams-ant-farm-recomp/releases/tag/v0.11.14
ZIP oficial: adams-ant-farm-windows-x86_64-v0.11.14.zip
Tamanho do ZIP baixado: 17084695 bytes
SHA-256 ZIP: 8202b51929a3721aaf16649f9dd30f95fedb000537d5690b2709f3f21e74097e
Executável: adams-ant-farm-windows-x86_64-v0.11.14/bh-launcher.exe
Required files: adams-ant-farm-windows-x86_64-v0.11.14/bh-launcher.exe, adams-ant-farm-windows-x86_64-v0.11.14/adams-ant-farm.exe, adams-ant-farm-windows-x86_64-v0.11.14/adams-ant-farm-eu.exe
Caminho da receita: recipes/body-harvest/adam-s-ant-farm/v0.11.14.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros.
Não testado: instalação ponta a ponta no AllFix.exe com ROM original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial Adam's Ant Farm e sua ROM verificada body-harvest.us.z64 foram instalados em adams-ant-farm-windows-x86_64-v0.11.14/. Execute bh-launcher.exe e selecione essa ROM no primeiro uso.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:17:07Z`
- **Pacote baixado e conferido:** `adams-ant-farm-windows-x86_64-v0.11.14.zip` (`17084695` bytes, SHA-256 `8202b51929a3721aaf16649f9dd30f95fedb000537d5690b2709f3f21e74097e`)
- **Resultado (`GameInstallationService.Run`):** `extraction_ok_awaiting_media` (`Status=Failed`)
- **Verificação de arquivos:** `3/3` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Execução interrompida na seleção de mídia obrigatória com retorno esperado `Status=Failed` (`A dependência obrigatória não foi selecionada.`) pois não há ROM/ISO comercial local; estrutura do ZIP oficial conferida integralmente (3/3 `required_files` e `launch_file` presentes).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
