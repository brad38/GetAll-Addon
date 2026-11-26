# Validação experimental — recharged v1.1.7

Jogo: mario-strikers-charged
Projeto oficial: recharged
Repositório: https://github.com/previouslevelgames/recharged
Release: https://github.com/previouslevelgames/recharged/releases/tag/v1.1.7
ZIP oficial: recharged-1.1.7+g053746ffc142-windows-x86_64.zip
Tamanho do ZIP baixado: 44127662 bytes
SHA-256 ZIP: a23c8ff90e4821550024eb8ca1701ba82191e10d849ff2e9b4a68e88477b63fc
Executável: recharged.exe
Required files: recharged.exe, d3dcompiler_47.dll, dxcompiler.dll, dxil.dll, recharged_game_us.dll
Caminho da receita: recipes/mario-strikers-charged/recharged/v1.1.7.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP, caminhos relativos. O motor não executou scripts externos.
Não testado: instalação ponta a ponta, importação da ROM/disco original, inicialização do jogo, ação Jogar agora.
Status: experimental (instalação parcial com manual_steps).

Procedimento manual da receita: O pacote oficial Recharged foi extraido. Execute recharged.exe na pasta instalada e, no launcher, adicione a pasta que contem a imagem legitima do disco Mario Strikers Charged (ISO, RVZ ou WBFS de regiao suportada). Clique em Play no launcher. A imagem do disco nao e distribuida nem importada pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:16:34Z`
- **Pacote baixado e conferido:** `recharged-1.1.7+g053746ffc142-windows-x86_64.zip` (`44127662` bytes, SHA-256 `a23c8ff90e4821550024eb8ca1701ba82191e10d849ff2e9b4a68e88477b63fc`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `5/5` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 5/5 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.

## Fluxo integral implementado no SDK 1.5.49

O perfil local exige o ZIP oficial e o manifesto dos 275 arquivos. O seletor importa uma ISO Wii integral de 4699979776 bytes. Valida a assinatura Wii, ID, revisão e SHA-1 Redump da mídia inteira. São aceitos EUA R4QE01 rev. 1 (7970), Europa R4QP01 rev. 1 e 2 (9009 e 1400), Japão R4QJ01 rev. 0 (29253) e Coreia R4QK01 rev. 0 (62634). O executável oficial recebe o caminho relativo da ISO instalada por --disc, conforme src/launcher/main.cpp do commit 053746ffc142728ee8d4231eb4e9adbfc11bb30d. RVZ e WBFS podem ser usados pelo launcher upstream.

O teste com o ZIP oficial confirmou preparo, seleção, cancelamento e rejeição de ISO truncada. Cinco cabeçalhos sintéticos e a rejeição de revisão incompatível foram testados. O comando de lançamento foi verificado com registro sintético. A instalação com ISO original e o primeiro boot estão pendentes. A receita permanece experimental.
