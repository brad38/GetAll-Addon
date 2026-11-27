# Contratos restantes reavaliados — 27/11/2026

A contagem continua em **140/148 fluxos integrais implementados**. Este registro
preserva as verificações das fontes e o que cada projeto ainda exige. Não
representa nova receita, instalação ou homologação. Metaforce e MKW estão em
frentes de implementação separadas; seus resultados serão incorporados quando
o fluxo completo estiver provado.

## Quatro projetos cuja fonte não fornece o fluxo Windows pedido

| ID preservado | Evidência atual | Condição necessária |
| --- | --- | --- |
| project-2099 | Windows beta5 continua sendo instalador + payload de 1.361.209.156 bytes. O próprio repositório distingue a licença do instalador do runtime e dos dados separados, declara que EOTP pode incluir recursos substitutos completos e não certifica o payload como livre de ativos do jogo. O código publicado não contém a implementação completa do runtime. | Distribuição independente com proveniência de seus componentes e contrato completo de preparação a partir da mídia original, ou fonte verificável do runtime e das alterações específicas. |
| doldecomp-mkdd-decompilacao-base | A revisão 0c3baef1ba96867f4ebbcdde02f7a43624224a85 é uma decompilação 1:1 de GameCube, atualmente da edição debug MarioClub_us. Ter ferramentas de build que executam no Windows não torna a saída um port Windows. | Um port nativo correspondente a este ID, com compilação e contrato de execução verificáveis. |
| tmc-decompilacao-base | A revisão beaf1ade00984b666fd625ba0c76686eae75cc69 reconstrói ROMs GBA. O README exige a ROM de origem para extrair os ativos. | Um port nativo correspondente a este ID. Project Picori é outro projeto já coberto e não foi contado novamente. |
| mml1-megaman-legends-decomp | A revisão 964bad3096a2d7a4a3d6cc65678d8440b2ea9cb1 usa ferramentas MIPS, extrai o disco PS1 e reconstrói uma imagem de disco; o código ainda não é relocável. | Um port nativo correspondente a este ID. MML Modernization é outro projeto já coberto. |

O catálogo consultado já identifica as três bases como
classification=base_decompilation, status=console_decompilation e instalação
Windows desabilitada. Nenhum ID foi removido, duplicado ou renomeado para
alterar o denominador.

### Project 2099: verificação além das notas da release

Foram lidos NO_GAME_DATA.md, THIRD_PARTY_LICENSES.md, prepare_payload.ps1 e
src/InstallerCore.cs no commit
1830cb5ed02c13290ddd8f53d2adc103decc2514. O gerador requer ReleaseRoot,
árvores de mídia e manifestos de correção verificados. O instalador exige o
payload completo e índice de correções schema4. Portanto, compilar apenas o
instalador público não resolve a preparação do jogo.

A lista de releases também contém um conjunto de arquivos de atualização beta3
e um APK Android mais novo. Eles não demonstram um pacote completo Windows
independente com todos os componentes necessários. Não foi baixado o payload,
o remaster de 4K nem uma imagem comercial. O bloqueio documentado é a ausência
do contrato/distribuição exigidos pelo projeto GetAll; não é uma conclusão
jurídica sobre todos os arquivos upstream.

Fontes primárias: [release beta5](https://github.com/GenryTheFox0/Project-2099/releases/tag/v2.0.0-beta.5),
[escopo dos dados](https://github.com/GenryTheFox0/Project-2099/blob/1830cb5ed02c13290ddd8f53d2adc103decc2514/NO_GAME_DATA.md),
[licenças e limites do payload](https://github.com/GenryTheFox0/Project-2099/blob/1830cb5ed02c13290ddd8f53d2adc103decc2514/THIRD_PARTY_LICENSES.md),
[gerador](https://github.com/GenryTheFox0/Project-2099/blob/1830cb5ed02c13290ddd8f53d2adc103decc2514/prepare_payload.ps1).

## Courage Reborn: recuperação pública adicional tentada

A [documentação oficial de build](https://docs.couragereborn.com/building/build/)
continua apontando para Linifadomra/Courage-Reborn, branch0.8. A documentação
[Docker](https://docs.couragereborn.com/building/docker/) descreve uma saída
tp_pc.exe por LLVM-MinGW, portanto a linguagem/toolchain não é o impedimento
atual. Falta acesso à árvore exata de fontes e dependências.

Além dos 404 do GitHub, a consulta de visitas mais recentes no Software Heritage
foi feita com as quatro grafias de origem documentada (com/sem .git e variação de
capitalização), todas sem snapshot encontrado. A pesquisa de origem por
Courage-Reborn retornou lista vazia. Isso descreve as consultas realizadas;
não prova que nenhum arquivo possa existir em outro endereço.

A busca pública no GitHub encontrou ferramentas de mods relacionadas, sem
identificar a árvore completa de Courage Reborn. Petrichor/Augment e documentação
de build, isoladamente, não permitem recompilar o jogo. Não houve acesso privado,
solicitação de credenciais ou alteração da identidade do projeto.

## Evidência e reprodução

[source-manifest.json](source-manifest.json) conserva os URLs imutáveis, commits,
tamanhos UTF-8 e SHA-256 dos sete contratos fonte. [recheck-sources.py](recheck-sources.py)
repete a leitura desses arquivos pequenos, com limite de tamanho e validação de
hash, e grava source-recheck-result.json. Não baixa pacotes binários.

[probe-courage-archive.py](probe-courage-archive.py) reproduz a consulta às origens
e preserva [courage-archive-origins.json](courage-archive-origins.json).
A resposta de pesquisa adicional está em
[courage-archive-search.json](courage-archive-search.json).

Os textos completos usados na análise foram transitórios; o manifesto, os
scripts e os resultados bastam para reproduzir esta verificação.
