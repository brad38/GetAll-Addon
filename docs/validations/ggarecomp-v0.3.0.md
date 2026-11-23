# Validação experimental — ggarecomp v0.3.0

Jogo: goemon-s-great-adventure
Projeto oficial: ggarecomp
Repositório: https://github.com/DreaXer/GGARecomp
Release: https://github.com/DreaXer/GGARecomp/releases/tag/v0.3.0
ZIP oficial: GGARecompiled-v0.3.0-windows.zip
Tamanho do ZIP baixado: 40258542 bytes
SHA-256 ZIP: 19c8e7fd7a009e48675742a6af453a8e7e8934adac4a4d7f0fa41bb084241e3c
Executável: GGARecompiled.exe
Required files: GGARecompiled.exe, SDL2.dll, dxcompiler.dll, dxil.dll
Caminho da receita: recipes/goemon-s-great-adventure/ggarecomp/v0.3.0.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros.
Não testado: instalação ponta a ponta no AllFix.exe com ROM original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial de Goemon's Great Adventure (v0.3.0) foi extraido. Execute GGARecompiled.exe na pasta instalada e Forneca sua ROM original de Goemon's Great Adventure (US SHA-1 9f9e860816f9e2a68bb5f4f56086e0c7450c64d7) no launcher. Nenhuma ROM e fornecida pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:17:01Z`
- **Pacote baixado e conferido:** `GGARecompiled-v0.3.0-windows.zip` (`40258542` bytes, SHA-256 `19c8e7fd7a009e48675742a6af453a8e7e8934adac4a4d7f0fa41bb084241e3c`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 4/4 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.

## Rodada 9 — importacao SHA-1 em LocalAppData (v3 para v5)

- **Mudanca:** receita migrada de v3 para v5 com import_input (local_app_data, profile_folders=[GGARecompiled], target=gga.us.z64). A selecao valida o SHA-1 oficial 9f9e860816f9e2a68bb5f4f56086e0c7450c64d7 e assinatura N64 80371240 antes de copiar o arquivo.
- **Destino upstream:** README oficial informa que a ROM US e copiada para LOCALAPPDATA/GGARecompiled durante o primeiro uso; src/game/ga_lang_eu.cpp documenta explicitamente o nome gga.us.z64, ao lado da ROM europeia opcional goemon2.eu.z64. Preservado manual_steps para configurar controles e confirmar ROM no launcher caso ainda seja solicitado. A eliminacao total do prompt depende de boot real.
- **ZIP oficial rebaixado/inspecionado:** GGARecompiled-v0.3.0-windows.zip, 40.258.542 bytes, SHA-256 19c8e7fd7a009e48675742a6af453a8e7e8934adac4a4d7f0fa41bb084241e3c; required_files 4/4 presentes, sem ROM comercial.
- **Teste:** schema v5, index SHA-256, parser real AllFix.dll 1.3.0 com local_app_data aceito, regressao de path traversal em profile_folders, SHA-1 sintetico aceito e adulteracao rejeitada. Nao houve importacao da ROM real ou boot.
- **Estado:** permanece experimental; validar se o launcher detecta gga.us.z64 sem nova selecao e confirmar configuracao inicial e jogo em execucao antes de validated.
- **Fontes:** https://github.com/DreaXer/GGARecomp/blob/main/README.md ; https://github.com/DreaXer/GGARecomp/blob/main/src/game/ga_lang_eu.cpp
