# REDRIVER2 7.4-rc2 — procedência e rota oficial

Revisão: 2026-11-28. Novo perfil: `redriver2-7.4-rc2-official-media`. O perfil `redriver2-7.4-rc2-native` permanece aposentado.

## Decisão e escopo

O pacote original da release 7.4-rc2 tem procedência específica documentada por grupo. GetAll fornece a receita de download direto e instalação com os dois discos do usuário; não espelha, reempacota ou incorpora os recursos do jogo. A investigação não usa a ausência de resposta à issue 234 como prova de impossibilidade.

Esta decisão documenta origem e fidelidade técnica. A licença MIT raiz não é apresentada como transferência dos direitos de terceiros sobre gráficos representados em capturas, falas, textos e notices do jogo original. Preserve os avisos existentes. Não há autorização geral de redistribuição dos recursos neste recibo.

## Identidade fixada

- [Release 7.4-rc2](https://github.com/OpenDriver2/REDRIVER2/releases/tag/7.4-rc2), commit [acca6b139302dd72c1fbff52556f3493aafda2dd](https://github.com/OpenDriver2/REDRIVER2/commit/acca6b139302dd72c1fbff52556f3493aafda2dd).
- [ZIP Windows original](https://github.com/OpenDriver2/REDRIVER2/releases/download/7.4-rc2/REDRIVER2_Win32_Release.zip): 9772801 bytes, SHA256 `92c20bf6194af715a84c058783fa3095ed09d3aeeb4c41485b11c984d14d276c`.
- Baseline instalado: 93 arquivos, 24.350.736 bytes; manifesto SHA256 `5dbcdaf29e72ba3d3ec20a0804385dde88a42e71540cdff4527319a86872ca55`.
- `data/DRIVER2`: 76 blobs; árvore Git `5fcf52804a893436476ccdaf92a4deecf1b43386`.
- [LICENSE da mesma revisão](https://github.com/OpenDriver2/REDRIVER2/blob/acca6b139302dd72c1fbff52556f3493aafda2dd/LICENSE): MIT, copyright SoapyMan; 1.065 bytes, SHA256 `db3b97ec54bd96f5219e94039156ed1f05e2c9f1c7284db9c12fc70e1c7a63eb`.
- 8.0 e seus cinco recursos HQ adicionais ficam fora deste contrato.

## Origem dos extras

| Grupo | Arquivos | Evidência | Limite da conclusão |
| --- | ---: | --- | --- |
| gallery | 25 | Project development-history gallery, March–September 2020. INTRO and sampled slides identify REDRIVER2 progress; screenshots include original-game graphics. [Histórico](https://github.com/OpenDriver2/REDRIVER2/commit/87a7d7783c40d4bb319b68b85cd17b8d9ff0c653) | Upstream project documentation; no independent relicensing claim over third-party graphics visible in screenshots. |
| localization | 10 | Game/source strings externalized to locale files, with maintained translations. The German addition expressly credits @Jordem. [Histórico](https://github.com/OpenDriver2/REDRIVER2/commit/6e895f5877c145ff14283271de605d30cd75eca7) | Attributed project contributions with source-game strings; not described as entirely original dialogue or independently relicensed commercial text. |
| replays | 14 | Replacement chase recordings maintained by upstream. The Mission 10 update expressly records a new chase recording; official Driver2CutsceneTool assembles REDRIVER2 replay inputs. [Histórico](https://github.com/OpenDriver2/REDRIVER2/commit/726e94d3877320c221d7719a73ab392e270b5ef4) | Identified project recordings/fixes. Do not substitute original-disc replays or silently omit the replacements. |
| subtitles | 26 | SBN text/timing metadata added by SoapyMan for the official subtitle implementation/exporter. 7384 bytes total; 24 nonempty files and two empty files. The 56-byte record format accounts for 130 subtitle entries; inspected samples contain timed game dialogue, not audio. [Histórico](https://github.com/OpenDriver2/REDRIVER2/commit/a3f81aed0e1178afc103d5bbc9af2c24ab71810c) | Project formatting/timing contributions reproduce game dialogue. The exporter needs WAV cue/LIST annotations; ordinary PCM conversion alone does not reconstruct these exact subtitles. |
| credits | 1 | Original-game credits/notices adapted for the port, with a project-specific final line discussed publicly by a collaborator and subsequently edited. [Histórico](https://github.com/OpenDriver2/REDRIVER2/commit/a0d9368220c39df9b7b614091dbe755e30fdbcda) | Preserve original Infogrames/Reflections and music attribution notices. This text file does not contain the credited music recordings. |

A galeria foi inspecionada pela decodificação de INTRO, IMG0 e IMG23: a abertura descreve o progresso de REDRIVER2 em 2020. Os replays possuem commits de regravação. LANG foi externalizado do código e corrigido/traduzido pelo projeto; não é um novo conjunto de diálogos integralmente autorais. XA contém metadados de texto/tempo, não áudio. CREDITS preserva avisos do jogo original e inclui edição própria documentada pelo projeto. O JSON acompanhante lista os commits e seus URLs completos.

## Procedimento completo

1. Baixar apenas o ZIP oficial fixado e verificar tamanho/SHA256, recibo e manifesto integral do kit antes da seleção de mídia.
2. Preservar todos os 93 arquivos originais, incluindo galeria, idiomas, replays, legendas e créditos. Os dois jars jPSXdec mantêm seus hashes fixados.
3. Receber os dois BIN MODE2/2352 locais do usuário; conferir tamanho e SHA1 da edição, SHA256 do arquivo selecionado e par da mesma região/revisão. Recusar troca de discos, mistura de revisão/região, duplicação de caminho ou mídia alterada.
4. Preparar Java 21 privado a partir do pacote Temurin fixado e verificado, reutilizando o cache de ferramentas. Não alterar JAVA_HOME global ou instalar Java no sistema. Reproduzir [conv.bat](https://github.com/OpenDriver2/REDRIVER2/blob/acca6b139302dd72c1fbff52556f3493aafda2dd/data/install/conv.bat) com jPSXdec: indexação, vídeo AVI/MJPEG (quality psx, Lanczos3) e áudio WAV. O runtime usa a primeira imagem validada por `-cdimage`, conforme suporte CDFS oficial. No commit fixado, DiscSwapped em system.c retorna CDTYPE_CORRECTDISC e a CLI aceita o caminho de -cdimage sem impor nome; não há troca da imagem para o disco 2 no runtime PC. Os FMVs e XA dos dois discos já estão locais.
5. Mesclar somente saídas AVI/WAV nos caminhos esperados; validar RIFF, tamanho e duplicatas. Revalidar o baseline sem alteração antes da publicação transacional.
6. Acrescentar a licença e este recibo em `installation-logs/`, fora do baseline. Registrar esses arquivos no manifesto final e verificá-los no lançamento. Os discos originais permanecem necessários no local selecionado.

[Instruções oficiais](https://github.com/OpenDriver2/REDRIVER2/wiki/Installation-instructions). [OpenDriver2Tools](https://github.com/OpenDriver2/OpenDriver2Tools/tree/89009f7f4f48f37a886b376292432cdffab4a136) converte formatos específicos e monta cutscenes a partir de replays gravados; não é um gerador de todos os extras do pacote. O exportador de SBN precisa de WAVs com anotações cue/LIST já existentes. Não afirmar que converter PCM sozinho reconstrói essas legendas ou a galeria histórica.

## Integridade e regressões

Depois da publicação, o usuário pode editar as preferências em config.ini; o arquivo deve continuar presente e ser um arquivo comum. Os outros 92 arquivos do baseline, incluindo os 76 extras, e os notices acrescentados continuam verificados no lançamento. O manifesto histórico de 93 arquivos conserva seu hash fixado. O teste do contrato de payload é separado da validação de discos e não afirma execução do jogo.

O perfil novo deve validar recibo, URL, tamanho e SHA256 do ZIP, o manifesto inteiro do kit, os 76 extras e ambos os jars. O fluxo antigo continua recusado. Testes focados abrangem contrato de receita, cancelamento, mídia inválida, pares incompatíveis, kit/extra adulterado, notices e perfil aposentado. A fixture STR sintética já existente pode validar conversão e merge sem mídia comercial.

O resultado anterior `redriver2-synthetic-video-result-20261128.json` contém a evidência de conversão sintética; não representa uma instalação com discos originais, primeiro boot ou jogabilidade. Esta revisão não registra execução desses três testes. Resultados da nova integração devem ser registrados separadamente após a execução, sem promover a receita a `validated` por schema, build ou fixture.

## Arquivos complementares e reprodução

O JSON acompanhante contém o contrato legível por máquina e fontes primárias por grupo. A cópia `Tools/OfficialBuilders/REDRIVER2-provenance.json` é idêntica ao recibo JSON de GetAll; o Desktop incorpora apenas esse texto e a licença, não assets, replays, legendas ou diálogos. Verifique o SHA256 do ZIP e use `RedriverOfficialIntegration.Policy()`, `Source(recipePath)` e `Official(recipePath, zipPath, evidenceDirectory)` no harness compilado pelo coordenador. A conversão sintética pode reutilizar `redriver_video_probe.py` com uma pasta nova e os jars oficiais fixados.
