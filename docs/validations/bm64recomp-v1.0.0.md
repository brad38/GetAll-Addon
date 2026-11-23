# Validação experimental — bm64recomp v1.0.0

Jogo: bomberman-64
Projeto oficial: bm64recomp
Repositório: https://github.com/RevoSucks/BM64Recomp
Release: https://github.com/RevoSucks/BM64Recomp/releases/tag/v1.0.0
ZIP oficial: BM64Recompiled-Windows-RelWithDebInfo.zip
Tamanho do ZIP baixado: 25227040 bytes
SHA-256 ZIP: c47a260901c45550b69380fa6dc9e9a0e3cbc8c0d6149be4a96fedf3283a1e96
Executável: BM64Recompiled.exe
Required files: BM64Recompiled.exe, SDL2.dll, dxcompiler.dll, dxil.dll
Caminho da receita: recipes/bomberman-64/bm64recomp/v1.0.0.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros.
Não testado: instalação ponta a ponta no AllFix.exe com ROM original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial de Bomberman 64 (v1.0.0) foi extraido. Execute BM64Recompiled.exe na pasta instalada e Forneca sua ROM original de Bomberman 64 (US) no menu inicial. Nenhuma ROM e fornecida pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:16:54Z`
- **Pacote baixado e conferido:** `BM64Recompiled-Windows-RelWithDebInfo.zip` (`25227040` bytes, SHA-256 `c47a260901c45550b69380fa6dc9e9a0e3cbc8c0d6149be4a96fedf3283a1e96`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 4/4 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
