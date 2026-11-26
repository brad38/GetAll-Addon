# Validação experimental — yu-gi-oh-forbidden-memories-recompiled v0.3.0

Jogo: yu-gi-oh-forbidden-memories
Projeto oficial: yu-gi-oh-forbidden-memories-recompiled
Repositório: https://github.com/krystalgamer/Yu-Gi-Oh-Forbidden-Memories-Recompiled
Release: https://github.com/krystalgamer/Yu-Gi-Oh-Forbidden-Memories-Recompiled/releases/tag/v0.3.0
ZIP oficial: yfm-redecomp-v0.3.0-windows.zip
Tamanho do ZIP baixado: 7829947 bytes
SHA-256 ZIP: 40f1fedd363c0db193f8d67dff48c49ebc375f5aa903279fd70d7c622ccb63a6
Executável: yfm-redecomp-v0.3.0/memories-pc.exe
Required files: yfm-redecomp-v0.3.0/memories-pc.exe, yfm-redecomp-v0.3.0/SDL3.dll
Caminho da receita: recipes/yu-gi-oh-forbidden-memories/yu-gi-oh-forbidden-memories-recompiled/v0.3.0.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial de Yu-Gi-Oh! Forbidden Memories (v0.3.0) foi extraido. Para jogar, execute memories-pc.exe em yfm-redecomp-v0.3.0/ e selecione a imagem .bin do seu disco USA na primeira execucao. Nenhum arquivo comercial ou ROM e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:17:43Z`
- **Pacote baixado e conferido:** `yfm-redecomp-v0.3.0-windows.zip` (`7829947` bytes, SHA-256 `40f1fedd363c0db193f8d67dff48c49ebc375f5aa903279fd70d7c622ccb63a6`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `2/2` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 2/2 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.

## Fluxo integral implementado no SDK 1.5.47

O perfil local exige o ZIP oficial e confere o manifesto de 835 arquivos. O seletor compartilhado solicita o BIN MODE2/2352 original dos EUA, SLUS-01411. O motor usa tamanho e SHA-1 do catálogo Redump, importa em staging transacional e passa o BIN instalado ao executável oficial por MEMORIES_DISC. O suporte a esse caminho está em src/pc/platform/game_files.c no commit 663626b1d38355dd11f5532894a2b94169e7f349.

O teste do motor com o pacote oficial conferiu preparo, seleção, cancelamento e rejeição do BIN sintético incompatível. O plano de lançamento e a rejeição de mídia alterada foram exercitados com um registro sintético. A instalação com mídia original e o primeiro boot estão pendentes. A receita permanece experimental.
