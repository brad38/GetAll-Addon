# Validação experimental — nookery-ex-acgc-pc-port v1.0.0

Jogo: animal-crossing
Projeto oficial: nookery-ex-acgc-pc-port
Repositório: https://github.com/flyngmt/Nookery
Release: https://github.com/flyngmt/Nookery/releases/tag/v1.0.0
ZIP oficial: Nookery-v1.0.0-windows-x86_64.zip
Tamanho do ZIP baixado: 32404132 bytes
SHA-256 ZIP: 542fe6fc9a216b209fea5a75314d7bc453ce9d91d32a098ebab06a52455d9d68
Executável: Nookery.exe
Required files: Nookery.exe, SDL3.dll, dxcompiler.dll, dxil.dll, nod.dll
Caminho da receita: recipes/animal-crossing/nookery-ex-acgc-pc-port/v1.0.0.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial Nookery (v1.0.0) foi extraido. Execute Nookery.exe e selecione sua imagem de disco legitima de Animal Crossing (GameCube USA GAFE01 rev 0 em .rvz, .iso, .ciso ou .gcm). Nenhum arquivo comercial e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:18:09Z`
- **Pacote baixado e conferido:** `Nookery-v1.0.0-windows-x86_64.zip` (`32404132` bytes, SHA-256 `542fe6fc9a216b209fea5a75314d7bc453ce9d91d32a098ebab06a52455d9d68`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `5/5` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 5/5 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
