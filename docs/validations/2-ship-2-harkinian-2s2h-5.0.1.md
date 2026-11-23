# Validação experimental — 2-ship-2-harkinian-2s2h 5.0.1

Jogo: the-legend-of-zelda-majora-s-mask
Projeto oficial: 2-ship-2-harkinian-2s2h
Repositório: https://github.com/2ship2harkinian/2ship2harkinian
Release: https://github.com/2ship2harkinian/2ship2harkinian/releases/tag/5.0.1
ZIP oficial: 2Ship-Battler-Bravo-Win64.zip
Tamanho do ZIP baixado: 44976935 bytes
SHA-256 ZIP: a46664a01623ad5d7cc82d29a9889699f6a98c9501c7a959a089f34380c1f078
Executável: 2ship.exe
Required files: 2ship.exe, 2ship.o2r
Caminho da receita: recipes/the-legend-of-zelda-majora-s-mask/2-ship-2-harkinian-2s2h/5.0.1.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP, caminhos relativos. O motor não executou scripts externos.
Não testado: instalação ponta a ponta, importação da ROM/disco original, inicialização do jogo, ação Jogar agora.
Status: experimental (instalação parcial com manual_steps).

Procedimento manual da receita: O pacote oficial 2 Ship 2 Harkinian foi extraido. Abra 2ship.exe na pasta instalada e forneca sua ROM legitima e compativel de Zelda Majora's Mask quando o aplicativo solicitar. Consulte 2ship.equipment para verificar a compatibilidade. Nenhuma ROM e fornecida.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:16:20Z`
- **Pacote baixado e conferido:** `2Ship-Battler-Bravo-Win64.zip` (`44976935` bytes, SHA-256 `a46664a01623ad5d7cc82d29a9889699f6a98c9501c7a959a089f34380c1f078`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `2/2` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 2/2 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
