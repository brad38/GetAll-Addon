# Validação experimental — bloodyroar2recomp v0.7.1

Jogo: bloody-roar-ii
Projeto oficial: bloodyroar2recomp
Repositório: https://github.com/novapowers0/BloodyRoar2Recomp
Release: https://github.com/novapowers0/BloodyRoar2Recomp/releases/tag/v0.7.1
ZIP oficial: BloodyRoar2-v0.7.1.zip
Tamanho do ZIP baixado: 20650840 bytes
SHA-256 ZIP: 745c2ae512a37b6a02087b418710ba92833c900393b133293fde54269aefd779
Executável: BloodyRoar2/BloodyRoar2_Recompiled.exe
Required files: BloodyRoar2/BloodyRoar2_Recompiled.exe
Caminho da receita: recipes/bloody-roar-ii/bloodyroar2recomp/v0.7.1.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial de Bloody Roar II (v0.7.1) foi extraido. Para jogar, abra BloodyRoar2_Recompiled.exe na pasta BloodyRoar2/ e indique sua imagem .bin/.cue ou .iso/.chd original no assistente inicial. Nenhum arquivo comercial ou ROM e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:17:34Z`
- **Pacote baixado e conferido:** `BloodyRoar2-v0.7.1.zip` (`20650840` bytes, SHA-256 `745c2ae512a37b6a02087b418710ba92833c900393b133293fde54269aefd779`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `1/1` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 1/1 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
