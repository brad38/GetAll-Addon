# Validação experimental — dnzhrecomp 0.0.3

Jogo: duke-nukem-zero-hour
Projeto oficial: dnzhrecomp
Repositório: https://github.com/sonicdcer/DNZHRecomp
Release: https://github.com/sonicdcer/DNZHRecomp/releases/tag/0.0.3
ZIP oficial: DNZHRecompiled-0.0.3-Windows-RelWithDebInfo.zip
Tamanho do ZIP baixado: 24044294 bytes
SHA-256 ZIP: ece88320327ffc58ec73e084c23aca274a016e45dd3558a684d59c37f88bdbc3
Executável: DNZHRecompiled.exe
Required files: DNZHRecompiled.exe, SDL2.dll, dxcompiler.dll, dxil.dll
Caminho da receita: recipes/duke-nukem-zero-hour/dnzhrecomp/0.0.3.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros.
Não testado: instalação ponta a ponta no AllFix.exe com ROM original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial de Duke Nukem: Zero Hour (0.0.3) foi extraido. Execute DNZHRecompiled.exe na pasta instalada e Forneca sua ROM original de Duke Nukem: Zero Hour (US) no menu inicial. Nenhuma ROM e fornecida pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:17:05Z`
- **Pacote baixado e conferido:** `DNZHRecompiled-0.0.3-Windows-RelWithDebInfo.zip` (`24044294` bytes, SHA-256 `ece88320327ffc58ec73e084c23aca274a016e45dd3558a684d59c37f88bdbc3`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 4/4 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
