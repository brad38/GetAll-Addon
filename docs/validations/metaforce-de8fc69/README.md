# Metaforce de8fc69 — fonte recuperada e compilação nativa

## Origem e identidade

O perfil mantém o projeto `metaforce` do catálogo, repositório
`AxioDL/metaforce`, e fixa o commit
`de8fc69bd7f345d6cf5f0c8fc2798295e22522d3`, árvore Git
`9d693e8894c031e5d1d220f39a44999d4010dc9f`.
O arquivo público do espelho [Antidote/metaforce](https://github.com/Antidote/metaforce/tree/de8fc69bd7f345d6cf5f0c8fc2798295e22522d3)
contém esse mesmo commit e a mesma árvore. Foram conferidas 199 árvores e
2.070 entradas de arquivo, com tratamento explícito dos dois arquivos `.bat`
cuja forma de checkout usa CRLF. Nenhuma identidade nova foi criada no catálogo.

O ZIP usado pelo SDK tem 21.536.851 bytes e SHA-256
`e130131a1a41e8599541d8ab3dd2f31c6d8abaa9af03411f8bba25c3f5b63f21`.
A exceção de URL está restrita a esse perfil compilado no SDK. A receita
continua usando a origem histórica do projeto e não altera a verificação
genérica de origem experimental.

## Prova nativa concluída

A compilação C++ real terminou com sucesso no Windows usando LLVM-MinGW,
CMake e Ninja compartilhados. Foram compilados o jogo, o renderizador,
a interface, o áudio e o suporte ao cartão de memória. Os 19 pacotes de
dependências e os três submódulos estão fixados por tamanho, hash e revisão.
As 12 alterações de portabilidade estão registradas integralmente no
script de reprodução e no manifesto de patches.

O executável produzido tem 18.186.752 bytes e SHA-256
`dfb79798a507ac553d29fb2dda51939861d38f085c82dd77d8ec7534f112a249`.
O produto inclui nove DLLs locais e 19 recursos da interface. O manifesto
de runtime inclui também um executável de teste separado, que não faz
parte da instalação do jogo.

As provas executadas verificaram:

- Importações PE AMD64 do produto e fechamento das DLLs locais.
- Interfaces públicas C de Dawn, SDL e nod, incluindo recusa de dados
  autorais inválidos pelo nod.
- Substituição atômica de arquivo pelo Borealis, com caminho Unicode e
  preservação de origem e destino no caso negativo.
- Carregamento de `metaforce.exe --help` e análise dos argumentos
  `--dvd` e `--user-dir` sem abrir imagem comercial.

O código do SDK acrescenta os avisos de licença de Metaforce, dependências,
LLVM-MinGW, CRT, Dawn, DXC, nod, FreeType e fontes da interface. O aviso
SQLite é extraído do primeiro comentário do cabeçalho pinado e verificado
após normalização LF: 1.485 bytes, SHA-256
`85806d613cfda5901f848b3b5b4b04396c8c64e89c97c0af3706c42b0c44bb47`.

## Fluxo do SDK

A receita `build-de8fc69` é experimental e requer SDK 1.5.69. O backend
passou 44 verificações de mídia, 52 de fluxo/transação/cache e 19 de
staging nativo pelo C# real: 115 verificações dirigidas, com compilação
isolada sem erros ou avisos. A montagem produziu 89 arquivos e
60.415.785 bytes, incluindo dez PE, 19 recursos e 60 avisos. A publicação
conjunta ainda depende dos gates do SDK central; a receita isolada não
altera a contagem de fluxos concluídos.

O perfil solicita a ISO/GCM original americana `GM8E01`, disco 0,
revisão 0. Confere cabeçalho, DOL, FST e o SHA-1 oficial do DOL
`949c5ed7368aef547e0b0db1c3678f466e2afbff` antes de compilar. A imagem
é usada no local selecionado, com leitura exclusiva de escrita durante a
compilação, e é conferida novamente para Jogar. Nenhuma cópia adicional
do disco é criada.

A montagem usa uma transação que publica somente o produto completo,
registra os arquivos, preserva o kit para retomada e mantém os saves fora
do manifesto imutável da instalação. O rollback recupera o registro do
kit e preserva o produto anterior, a mídia e os dados do usuário.

As ferramentas expandidas ficam em cache compartilhado por hash. Cada
reutilização confere o conteúdo contra o ZIP oficial verificado. A área
de trabalho da tentativa é removida ao terminar; os logs necessários são
retidos com limites por arquivo e por tentativa. O backend não remove
diretórios pessoais de cache do SDL/Borealis.

## Evidências e limites

Os arquivos desta pasta preservam código de reprodução, manifestos de
fontes e pacotes, patches e resultados da prova nativa. O manifesto
`evidence-source-manifest.json` registra o hash original e o hash salvo
de cada arquivo; qualquer normalização CRLF/LF é explícita. Compilações
intermediárias, ZIPs de ferramentas e binários de teste não são versionados.

Os resultados dirigidos estão em [mídia](MEDIA-PROOF.md),
[fluxo e staging C#](BUILD-PROOF.md) e [limpeza](CLEANUP-OBJECTS.md).
Após os gates, foram removidos 1.293 objetos de compilação (34.448.295
bytes) e uma duplicata do ZIP público da fixture (21.536.851 bytes).
O arquivo oficial do cache, as fontes, os produtos e todos os relatórios
foram preservados. A reprodução usa uma nova área de trabalho.

Os testes de mídia usam somente pequenas fixtures autorais. Elas não
passam pelo hash comercial exigido em produção. O carregamento com
`--help` e as provas de interface não comprovam boot ou funcionamento de
Metroid Prime com mídia original. Nenhuma promoção a `validated` é feita.
