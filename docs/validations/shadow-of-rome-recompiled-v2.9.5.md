# Validação experimental — shadow-of-rome-recompiled v2.9.5

Jogo: shadow-of-rome
Projeto oficial: shadow-of-rome-recompiled
Repositório: https://github.com/Korvonordico/shadow-of-rome-recompiled
Release: https://github.com/Korvonordico/shadow-of-rome-recompiled/releases/tag/v2.9.5
ZIP oficial: ShadowOfRome-2.9.5-windows.zip
Tamanho do ZIP baixado: 58027163 bytes
SHA-256 ZIP: a416fcf346bba3be23a4b9753d9f1ab32925a65d5baa3f8b70d6752527aac508
Executável: ShadowOfRome-2.9.5-windows/ShadowOfRome.exe
Required files: ShadowOfRome-2.9.5-windows/ShadowOfRome.exe, ShadowOfRome-2.9.5-windows/sor.exe, ShadowOfRome-2.9.5-windows/sor-usa.exe, ShadowOfRome-2.9.5-windows/dxcompiler.dll, ShadowOfRome-2.9.5-windows/lz4.dll
Caminho da receita: recipes/shadow-of-rome/shadow-of-rome-recompiled/v2.9.5.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial Shadow of Rome Recompiled (v2.9.5) foi extraido. Execute ShadowOfRome.exe em ShadowOfRome-2.9.5-windows/, clique em Play e selecione sua imagem .iso original de Shadow of Rome (PAL SLES-52950 ou NTSC-U SLUS-20902). Nenhum arquivo comercial e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:19:06Z`
- **Pacote baixado e conferido:** `ShadowOfRome-2.9.5-windows.zip` (`58027163` bytes, SHA-256 `a416fcf346bba3be23a4b9753d9f1ab32925a65d5baa3f8b70d6752527aac508`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `5/5` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 5/5 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
