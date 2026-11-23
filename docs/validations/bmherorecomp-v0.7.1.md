# Validação experimental — bmherorecomp v0.7.1

Jogo: bomberman-hero
Projeto oficial: bmherorecomp
Repositório: https://github.com/RevoSucks/BMHeroRecomp
Release: https://github.com/RevoSucks/BMHeroRecomp/releases/tag/v0.7.1
ZIP oficial: BMHeroRecompiled-Windows-RelWithDebInfo.zip
Tamanho do ZIP baixado: 18577511 bytes
SHA-256 ZIP: d6a865b4e1adb17860ccc6faf15306ce4a7c885b4dc16b0989e01e1c7bbcb58d
Executável: BMHeroRecompiled.exe
Required files: BMHeroRecompiled.exe, SDL2.dll, dxcompiler.dll, dxil.dll
Caminho da receita: recipes/bomberman-hero/bmherorecomp/v0.7.1.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros.
Não testado: instalação ponta a ponta no AllFix.exe com ROM original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial de Bomberman Hero (v0.7.1) foi extraido. Execute BMHeroRecompiled.exe na pasta instalada e Forneca sua ROM original de Bomberman Hero (US) no menu inicial. Nenhuma ROM e fornecida pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:16:56Z`
- **Pacote baixado e conferido:** `BMHeroRecompiled-Windows-RelWithDebInfo.zip` (`18577511` bytes, SHA-256 `d6a865b4e1adb17860ccc6faf15306ce4a7c885b4dc16b0989e01e1c7bbcb58d`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 4/4 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
