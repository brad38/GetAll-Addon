# Validação experimental — zelda-64-recompiled v1.2.2

Jogo: the-legend-of-zelda-majora-s-mask
Projeto oficial: zelda-64-recompiled
Repositório: https://github.com/Zelda64Recomp/Zelda64Recomp
Release: https://github.com/Zelda64Recomp/Zelda64Recomp/releases/tag/v1.2.2
ZIP oficial: Zelda64Recompiled-v1.2.2-Windows.zip
Tamanho do ZIP baixado: 28940501 bytes
SHA-256 ZIP: d02b95f1cf5e4d44d6587fa6136c6db521f61aa41ba8700c05f91bea8b0a26d0
Executável: Zelda64Recompiled.exe
Required files: Zelda64Recompiled.exe, dxcompiler.dll, dxil.dll, SDL2.dll
Caminho da receita: recipes/the-legend-of-zelda-majora-s-mask/zelda-64-recompiled/v1.2.2.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP, caminhos relativos. O motor não executou scripts externos.
Não testado: instalação ponta a ponta, importação da ROM/disco original, inicialização do jogo, ação Jogar agora.
Status: experimental (instalação parcial com manual_steps).

Procedimento manual da receita: O pacote oficial Zelda64 Recompiled foi extraido. No primeiro uso, abra Zelda64Recompiled.exe na pasta instalada e forneca sua copia legitima norte-americana de Zelda Majora's Mask no menu do jogo. O projeto carrega os recursos da ROM selecionada e nao fornece o jogo original.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:16:17Z`
- **Pacote baixado e conferido:** `Zelda64Recompiled-v1.2.2-Windows.zip` (`28940501` bytes, SHA-256 `d02b95f1cf5e4d44d6587fa6136c6db521f61aa41ba8700c05f91bea8b0a26d0`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 4/4 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
