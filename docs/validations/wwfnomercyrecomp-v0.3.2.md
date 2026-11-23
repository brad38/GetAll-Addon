# Validação experimental — wwfnomercyrecomp v0.3.2

Jogo: wwf-no-mercy
Projeto oficial: wwfnomercyrecomp
Repositório: https://github.com/jessetbh/WWFNoMercyRecomp
Release: https://github.com/jessetbh/WWFNoMercyRecomp/releases/tag/v0.3.2
ZIP oficial: NoMercyRecompiled-v0.3.2-Windows.zip
Tamanho do ZIP baixado: 29234117 bytes
SHA-256 ZIP: 8cefdcca49c582dc2a7e10ea925c16d761e1b0bb6249f49e8e80eb220ccf23bd
Executável: NoMercyRecompiled.exe
Required files: NoMercyRecompiled.exe, SDL2.dll, dxcompiler.dll, dxil.dll, librashader.dll, msvcp140.dll, msvcp140_atomic_wait.dll, vcruntime140.dll, vcruntime140_1.dll
Caminho da receita: recipes/wwf-no-mercy/wwfnomercyrecomp/v0.3.2.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial, caminhos relativos seguros. disasm/nomercy.yaml confirma 33554432 bytes (0x2000000) e SHA-1 91cee3d096f4a76644d8b35b9aead6448909abd1.
Não testado: instalação ponta a ponta no AllFix.exe com ROM original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima antes de promoção para validated).

Procedimento manual da receita: O pacote oficial e sua ROM verificada nomercy.z64 foram instalados. Abra NoMercyRecompiled.exe na pasta do jogo e escolha nomercy.z64 no botao Load ROM na primeira execucao.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:16:49Z`
- **Pacote baixado e conferido:** `NoMercyRecompiled-v0.3.2-Windows.zip` (`29234117` bytes, SHA-256 `8cefdcca49c582dc2a7e10ea925c16d761e1b0bb6249f49e8e80eb220ccf23bd`)
- **Resultado (`GameInstallationService.Run`):** `extraction_ok_awaiting_media` (`Status=Failed`)
- **Verificação de arquivos:** `9/9` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Execução interrompida na seleção de mídia obrigatória com retorno esperado `Status=Failed` (`A dependência obrigatória não foi selecionada.`) pois não há ROM/ISO comercial local; estrutura do ZIP oficial conferida integralmente (9/9 `required_files` e `launch_file` presentes).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
