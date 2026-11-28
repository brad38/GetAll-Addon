# SDK 1.5.69 — Metaforce e preparação automática de MKW

O SDK integra os perfis `metaforce-source-de8fc69` e
`mkw-0.1.18-cli-prepare`. O Desktop permanece 3.0.0 e o protocolo permanece
1.0. As duas receitas novas exigem SDK mínimo 1.5.69 e continuam
`experimental`. O índice tem **145 receitas para 142 projetos**: 144 entradas
experimentais e uma homologação histórica. Nenhum teste desta rodada comprova
um novo primeiro boot comercial.

As fontes do Desktop estão no commit
[`921295de12349e726f7ca21a5edd8a8ecee123d8`](https://github.com/brad38/Allfix/commit/921295de12349e726f7ca21a5edd8a8ecee123d8),
branch `work/complete-install-flows-20261127`. O envio foi confirmado no
GitHub. A [prévia completa SDK169](../sdk169-preview/README.md) foi montada e
verificada. A [prova dos serviços Store](../store-assembly-proof/RUN-RESULT.md)
passou em 20 verificações no mesmo assembly distribuído no executável final.

## Resultados integrados

| Gate | Resultado |
| --- | --- |
| Compilação BUILD31d, .NET 8.0.425 | 0 erros, 0 avisos; 10,219 s |
| Regressão do harness real | 1.967 verificações aprovadas, zero falhas; 11,312 s |
| Leitor de mídia Metaforce, incluído na regressão | 44 verificações aprovadas |
| Perfil, alias local e compatibilidade MKW, incluídos na regressão | 43 verificações aprovadas |
| Parser C# sobre o índice final | 145/145 receitas, zero falhas; 9,375 s |
| Preparação, transação e recuperação Metaforce | 52 verificações aprovadas; 0,891 s |
| Fontes e entradas antes/depois | 538 arquivos, estado Git, índice e ZIP compartilhado idênticos |

[BUILD31D.md](BUILD31D.md) conserva os comandos, tempos e correções das
tentativas anteriores. [build31d-result.json](build31d-result.json) identifica
os assemblies executados e os hashes dos logs. O índice tem SHA256
`2e3ee9a442015c492c84cc28f92f7da75dfffdbbe817d42dc0f3b311cbfac9eb`.
O manifesto [windows-source-manifest.json](windows-source-manifest.json)
distingue os hashes dos originais Windows e das cópias textuais em LF.

O BUILD31 preserva a falha por ausência de `project.assets.json`; o restore
offline reutilizou os pacotes existentes sem alterá-los. O BUILD31b preserva
a importação de namespace faltante no teste novo. O BUILD31c preserva a
asserção indevida que igualava a receita histórica MKW à seleção local de
mídias. O BUILD31d passou após corrigir somente esses testes. As correções
não alteraram código produtivo nem receitas para satisfazer os testes.

## Metaforce

A revisão `de8fc69bd7f345d6cf5f0c8fc2798295e22522d3` e sua árvore oficial
foram recuperadas e verificadas. O perfil prepara fontes, dependências e
toolchains fixadas, compila o runtime Windows, publica suas bibliotecas e
avisos, registra a instalação e configura o lançamento com a mídia original.
A recuperação conserva a instalação anterior e os saves. A mídia é validada
antes do consentimento e novamente durante a preparação; a ISO não é copiada
para o produto publicado.

A prova nativa compilou o C++ real e verificou o runtime e seus imports.
A prova posterior atravessou o staging C# real em **19 verificações**, sem
recompilar novamente o C++. O leitor exige o disco e DOL da edição suportada;
fixtures autorais não são aceitas como mídia comercial. A execução de
`--help` e as provas de ABI não equivalem a boot com ISO ou execução de jogo
na GPU. Evidência e reprodução:
[Metaforce](../metaforce-de8fc69/README.md),
[preparação/transação](../metaforce-de8fc69/BUILD-PROOF.md) e
[leitor de mídia](../metaforce-de8fc69/MEDIA-PROOF.md).

## Mario Kart World

A variante local `v0.1.18-allfix-cli` usa o pacote oficial **v0.1.18** sem
inventar uma release upstream. Seu perfil exige somente a pasta original
com ExeFS/RomFS. A CLI oficial nvdisasm é obtida com tamanho e hash fixados;
um parser textual e adaptadores abertos alimentam o tradutor original.
Descritores, fontes modificadas e ferramenta instalada são verificados
novamente no lançamento. Falhas de tradução ou contêineres truncados são
propagadas, sem gerar um estado de sucesso incompleto.

A receita e o perfil antigos `v0.1.18` permanecem disponíveis. Seu contrato
de receita declara uma mídia, e a retomada histórica acrescenta a seleção
local de `shader-spec`. O perfil novo mantém uma mídia tanto na receita
quanto na retomada. O teste integrado verifica essa diferença explicitamente.

O Native8 passou em **77 verificações** pela cadeia real de extração,
decodificação, tradução, compilação SPIR-V e empacotamento. Foram validados
14 programas autorais em cinco estágios; o pacote tem 15 programas incluindo
o vertex auxiliar oficial. Provas adicionais verificaram emissão de texturas,
carry LEA e endereços de 64 bits com deslocamento negativo. Os 99 nomes
consumidos têm evidência positiva documentada; isso não comprova todas as
variantes SM86 nem todos os shaders comerciais. Não houve execução GPU ou
boot de MKW. Fontes, limites e reprodução:
[MKW CLI](../mkw-sm86-cli/README.md).

## Preservação e reprodução

O recurso `MkwSm86.cli-support.zip` tem 63.227 bytes e SHA256
`1c79d30594951495f210a349da05aabe0e240f0189dba87c95a78da73a4500ce`.
As fontes e o repacker determinístico estão em `Tools/MkwSm86` no Desktop;
uma reconstrução independente produziu bytes idênticos. O ZIP contém fontes,
adaptações e avisos, sem executável NVIDIA, tabela privada ou dados de jogo.

Os scripts deste diretório repetem os gates em uma saída nova e recusam
sobrescrever os resultados antigos. A reprodução nativa reutiliza caches e
toolchains compartilhados. [STORAGE.md](STORAGE.md) e os recibos associados
registram a remoção de objetos, cópias redundantes e fixtures descartáveis,
com verificação dos arquivos preservados. Código, receitas, logs relevantes,
scripts, resultados, mídia original, dados pessoais e dependências em uso
ficam preservados.

## Projetos ainda dependentes de outra fonte ou implementação

Courage Reborn precisa de uma árvore de fonte acessível; Project 2099 precisa
do runtime e de um contrato completo de preparação. As bases de decompilação
de MKDD, TMC e MML1 produzem saídas para seus consoles, sem um port Windows
correspondente. Wind Waker Recomp remete ao sucessor BlueWake, já contado.
Os seis IDs permanecem no catálogo de 148 projetos, sem duplicar sucessores
ou converter kits/fixtures em instalações concluídas.

As fontes e condições específicas estão em
[contratos restantes](../remaining-projects-20261127/README.md) e
[contrato do sucessor Wind Waker](wind-waker-successor-contract.json).
