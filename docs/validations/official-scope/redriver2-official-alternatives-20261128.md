# REDRIVER2 — revalidação das alternativas oficiais

Status: instalação manual. A receita 7.4-rc2 permanece desativada.

## Verificação

- O HEAD oficial observado é b2d8857426f815007486def9bd23f9a6007a2c64, que coincide com a tag 8.0. A issue upstream nº 234 sobre os recursos adicionais ainda está aberta e não mostra resposta do mantenedor. [Issue 234](https://github.com/OpenDriver2/REDRIVER2/issues/234) · [Release 8.0](https://github.com/OpenDriver2/REDRIVER2/releases/tag/8.0)
- Consultei a árvore Git das 16 tags oficiais em uma cópia bare sem download dos blobs de mídia. Todas as versões de 6.0a-alpha a 8.0 mantêm 25 arquivos de galeria. Em 7.4-rc2 são 76 entradas em data/DRIVER2; em 8.0 são 81, incluindo cinco fontes adicionais.
- 6.0-alpha antecede a inclusão da galeria, mas já empacota oito tabelas de localização e um arquivo de créditos. 5.7-alpha traz um kit Windows oficial e antecede os TIMs da galeria, mas o mantenedor documenta replays quebrados e falhas possíveis nas perseguições. Mantive a versão atual do catálogo para preservar o procedimento e os recursos que o usuário espera. [Release 5.7](https://github.com/OpenDriver2/REDRIVER2/releases/tag/5.7-alpha) · [Commit que introduz a galeria](https://github.com/OpenDriver2/REDRIVER2/commit/87a7d7783c40d4bb319b68b85cd17b8d9ff0c653)
- O layout de CD para a compilação PSX no upstream lista texturas TIM do jogo, mas não inclui o diretório da galeria nem os nomes IMG0–IMG23/INTRO. Esse layout é auxiliar de build e não prova o conteúdo de todas as revisões comerciais. O Launcher e a wiki descrevem conversão de vídeo e áudio, sem uma etapa para produzir a galeria. [Layout de CD fixado](https://github.com/OpenDriver2/REDRIVER2/blob/acca6b139302dd72c1fbff52556f3493aafda2dd/PSXToolchain/CDSrc/redriver2_cd.xml) · [Instruções oficiais](https://github.com/OpenDriver2/REDRIVER2/wiki/Installation-instructions)
- O README do fork ReExtended descreve um processo próprio em que o jogador extrai as pastas dos discos. É um projeto distinto, com outra release e outros recursos. Sua documentação não é um contrato para o REDRIVER2 original. [ReExtended v0.1-beta](https://github.com/E75/Redriver_ReExtended/releases/tag/v0.1-beta)

## Teste do conversor com vídeo

Um CD MODE2/2352 sintético, com ISO9660 mínimo e 96 quadros STR de 16×16,
foi processado pelo jPSXdec 1.05 beta da release 7.4-rc2 usando Java 21.
O índice identificou `DRIVER2/FMV/2/RENDER20.STR[0]` e o próprio conversor
gerou um AVI/MJPEG de 65.988 bytes na estrutura oficial. O motor confirmou
o nome e contêiner do arquivo, encerrou a cópia cancelada com destino vazio
e verificou a cópia byte a byte. A mídia de teste permaneceu intacta.

O script de reprodução valida o SHA-256 dos dois JARs e gera a mídia do zero.
Os três testes foram executados em caminho com espaço e acento.
[Script Desktop](https://github.com/brad38/Allfix/blob/388ea0788279974e5663bebd91418c30f1bdde87/Tests/AddonInfrastructure/redriver_video_probe.py)
· [Recibo com hashes](redriver2-synthetic-video-result-20261128.json)

## Condições para retomar

O motor já tem seleção de dois BIN MODE2/2352, identificação do par, conversão via jPSXdec e staging transacional. Para habilitar uma receita fiel, falta um processo oficial que produza os dados auxiliares a partir da mídia do usuário ou evidência verificável sobre sua origem e distribuição. Ainda é necessário validar o resultado com os dois discos originais da mesma região e revisão. Não houve instalação integral nem primeiro boot.
