# Validação experimental — kf1-enhanced v0.1.0-pre.3

Jogo: king-s-field-jp-1994
Projeto oficial: kf1-enhanced
Repositório: https://github.com/Acranon/kf1-enhanced
Release: https://github.com/Acranon/kf1-enhanced/releases/tag/v0.1.0-pre.3
ZIP oficial: KingsFieldEnhanced-v0.1.0-pre.3-windows.zip
Tamanho do ZIP baixado: 3511950 bytes
SHA-256 ZIP: 400bffc15e2f95d0f5770c9f898c0bbe23e2fdcfeeb98942b8b1d1c8844249ff
Executável: KingsFieldEnhanced-v0.1.0-pre.3-windows/kings-field.exe
Required files: KingsFieldEnhanced-v0.1.0-pre.3-windows/kings-field.exe, KingsFieldEnhanced-v0.1.0-pre.3-windows/SDL3.dll
Caminho da receita: recipes/king-s-field-jp-1994/kf1-enhanced/v0.1.0-pre.3.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial de King's Field (JP, 1994) (v0.1.0-pre.3) foi extraido. Para jogar, execute kings-field.exe e selecione sua imagem .cue+.bin ou .iso japonesa original para gerar a pasta data/. Nenhum arquivo comercial ou ROM e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:17:42Z`
- **Pacote baixado e conferido:** `KingsFieldEnhanced-v0.1.0-pre.3-windows.zip` (`3511950` bytes, SHA-256 `400bffc15e2f95d0f5770c9f898c0bbe23e2fdcfeeb98942b8b1d1c8844249ff`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `2/2` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 2/2 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.

## Fluxo integral implementado no SDK 1.5.48

O motor confere o manifesto do ZIP oficial e aceita o BIN MODE2/2352 japonês SLPS-00017 de 30378432 bytes com SHA-1 00BFD94CE99BF214B03BDAA07DE99B9CA1466550 (Redump). O importador e o verificador usam o código upstream ac147450249c95b8d7683300292a2761796cb611 em modo japonês. O motor exige 428 arquivos nos recursos extraídos e verifica a árvore com o código oficial antes de registrar a instalação. O executável oficial recebe --data data/ja --language ja, com o manifesto dos arquivos conferido antes de iniciar.

O teste com o pacote oficial confirmou preparo, seletor, cancelamento e rejeição de mídia incompatível. O importador e o verificador foram executados pelo motor em pasta com acentos e rejeitaram dados sintéticos. O plano de lançamento e a rejeição de recurso alterado foram exercitados com registro sintético. Extração com disco original e primeiro boot pendentes. A receita permanece experimental.
