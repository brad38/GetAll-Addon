# Prévia completa — Desktop 3.0.0 / SDK 1.5.68 / GetAll 1.5.73

A prévia foi montada em 27/11/2026 às 17:58:44 (America/Fortaleza), reutilizando
o executável do candidato já auditado. Inclui os **140 fluxos integrais
implementados**, inclusive Shadow of the Colossus e Savage Wind. Isso não
altera a contagem de homologação: um histórico, nenhum novo primeiro boot.

## Publicação das fontes

A conferência pela API do GitHub está preservada em [remote-pins.json](remote-pins.json).

| Componente | Commit publicado | CI aprovado |
| --- | --- | --- |
| Desktop | 8ba34eb51ee0ab93accef3da5e1689c68825977d | [46059165665](https://github.com/brad38/Allfix/actions/runs/46059165665) |
| GetAll | 5b7fea8fb8d2b77df5a6cfd7e9efb6b463fba75b | [46059162398](https://github.com/brad38/GetAll-Addon/actions/runs/46059162398) |

As PRs [Desktop #3](https://github.com/brad38/Allfix/pull/3) e
[GetAll #20](https://github.com/brad38/GetAll-Addon/pull/20) continuam em draft,
sem merge. O catálogo é fixado em 3f4603cf42ef43402b4a0a9470232e7d4fcd9eb9.

## Artefatos no Bradsson

Pasta: C:\Users\bradg\Downloads\GetAll-R18\publish-getall-sdk168-20261127

| Arquivo | SHA-256 |
| --- | --- |
| AllFix.exe | 3ce6d4ec0e182a450fa621cc8f7a2288250e1485d6be539513f9b8a705a099da |
| GetAll-Preview.zip | 656fe2fd35cbda71b3e7974f3c8510ee75edf33b53f7a6c2c29d8e8ef3696914 |
| ARTIFACT-MANIFEST.json | 0220e843125b9223435d671fcbb834df1d13ce653fb770e6599989f7efd1c95a |

Foram verificados 74 arquivos, 34 recursos nativos, 66 avisos de licença e
12 propriedades de compilação. O complemento exige SDK 1.5.68 e aponta para
o índice imutável publicado, SHA-256
c82d450f0da6e067c80cc01141b677c950b43fbeac5c9303aededac266bcdee3.

A montagem não executa o aplicativo nem instala o complemento. Para usar a
prévia, abrir o AllFix.exe dessa pasta e adicionar GetAll-Preview.zip pela
Loja de Jogos > Complementos, ativando-o em Gerenciar. A instalação corrente
não foi substituída.

Antes do commit da documentação, o validador estrito confirmou as 143 receitas,
schemas, LF, blobs Git e catálogo. A suíte Python aprovou 60 testes em 2,146 s,
com log preservado. O parser real do harness BUILD30 foi reutilizado e aprovou
143/143 receitas, zero recusas e exit0, sem recompilar ou repetir provas nativas;
ver [parser-result.json](parser-result.json).

## Reprodução e armazenamento

[assemble-preview.py](assemble-preview.py) usa o candidato auditado, o
checkout limpo getall-sdk168-final-20261127 e a confirmação remota acima.
O script verifica os pins, monta em staging próprio, compara o inventário
e publica por renomeação. A execução é registrada em
[preview-result.json](preview-result.json).

No Bradsson, os scripts, logs e recibos ficam em
C:\Users\bradg\Downloads\GetAll-R18\evidence-r18\preview-sdk168-20261127.

Com Python 3.12, executar:

~~~powershell
python assemble-preview.py assemble --task-root 'C:\Users\bradg\Downloads\GetAll-R18' --evidence 'C:\Users\bradg\Downloads\GetAll-R18\evidence-r18\preview-sdk168-20261127'
~~~

A montagem recusa sobrescrever a pasta final. Para verificar a prévia existente,
usar o modo verify com o mesmo task-root. Foram copiados 165.625.170 bytes do
candidato e criado um complemento pequeno; nenhuma recompilação foi feita.
O staging foi removido. O candidato e as prévias entregues anteriormente
foram preservados.
