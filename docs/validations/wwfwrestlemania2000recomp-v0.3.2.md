# Validação experimental — wwfwrestlemania2000recomp v0.3.2

Jogo: wwf-wrestlemania-2000
Projeto oficial: wwfwrestlemania2000recomp
Repositório: https://github.com/jessetbh/WWFWrestleMania2000Recomp
Release: https://github.com/jessetbh/WWFWrestleMania2000Recomp/releases/tag/v0.3.2
ZIP oficial: Wm2kRecompiled-v0.3.2-Windows.zip
Tamanho do ZIP baixado: 23562293 bytes
SHA-256 ZIP: eed70bc4c57fcbc0f3331414850f549f50be0b0dae0ff98b89cc58497dc8ffe5
Executável: Wm2kRecompiled.exe
Required files: Wm2kRecompiled.exe, SDL2.dll, dxcompiler.dll, dxil.dll, librashader.dll, msvcp140.dll, msvcp140_atomic_wait.dll, vcruntime140.dll, vcruntime140_1.dll
Caminho da receita: recipes/wwf-wrestlemania-2000/wwfwrestlemania2000recomp/v0.3.2.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial, caminhos relativos seguros. disasm/wm2k.yaml confirma 33554432 bytes (0x2000000) e SHA-1 442d417a52ed672ca1a47e7261a5414debb1e27a.
Não testado: instalação ponta a ponta no AllFix.exe com ROM original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima antes de promoção para validated).

Procedimento manual da receita: O pacote oficial e sua ROM verificada wm2k.z64 foram instalados. Abra Wm2kRecompiled.exe na pasta do jogo e escolha wm2k.z64 no botao Load ROM na primeira execucao.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:16:46Z`
- **Pacote baixado e conferido:** `Wm2kRecompiled-v0.3.2-Windows.zip` (`23562293` bytes, SHA-256 `eed70bc4c57fcbc0f3331414850f549f50be0b0dae0ff98b89cc58497dc8ffe5`)
- **Resultado (`GameInstallationService.Run`):** `extraction_ok_awaiting_media` (`Status=Failed`)
- **Verificação de arquivos:** `9/9` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Execução interrompida na seleção de mídia obrigatória com retorno esperado `Status=Failed` (`A dependência obrigatória não foi selecionada.`) pois não há ROM/ISO comercial local; estrutura do ZIP oficial conferida integralmente (9/9 `required_files` e `launch_file` presentes).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
