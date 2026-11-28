# Metaforce — limpeza após as provas

As provas isoladas encerraram antes da limpeza: 44 checks de mídia, 52 de instalação/recuperação/ferramentas e 19 de configuração/staging C# real. O checkout Desktop permaneceu no commit `8ba34eb51ee0ab93accef3da5e1689c68825977d`, sem alteração de fontes por esta tarefa.

## Objetos compilados

O plano `native-1/cleanup-plan-objects.json`, SHA256 `6d71de1a371607cdebae1e2639d07e44ddc559f82167520606b213c080d4ad12`, autorizava exatamente 1.293 arquivos `.obj`, `.o` e `.res`. Todos foram reconferidos por caminho ordinário, contenção, tamanho, SHA256 e identidade NTFS com `nlink=1`. Não havia processo de build/staging/probe ativo. Nenhuma pasta foi removida.

- Bytes lógicos removidos: **34.448.295**.
- Espaço livre antes/depois: **99.744.067.584 → 99.784.273.920** bytes.
- Variação observada: **+40.206.336** bytes.
- A árvore `native-1` ficou com **713.345.872** bytes lógicos.
- Toda a metadata dos demais arquivos da árvore ficou igual; **128 arquivos de provas/produtos** tiveram tamanho e SHA256 novamente comparados.
- O primeiro preflight interrompeu antes de excluir: a comparação de hashes precisava aceitar a caixa hexadecimal emitida pelo manifesto C#. O plano permaneceu intacto, a comparação foi normalizada e a verificação completa passou antes da exclusão.

Recibo no Bradsson:

`C:\Users\bradg\Downloads\GetAll-R18\evidence-r18\three-upstreams-20261127\cleanup-objects-20261127T214812Z-cf5340d4\result.json`

SHA256: `f5058db262118f26a6db82b68ca4ff823a9bed9bba9250c157f331123b604adc`. A mesma pasta contém o script, o plano original, os inventários antes/depois, os hashes de provas preservadas e um journal com cada exclusão.

## Cópia do ZIP no kit autoral

A fixture da Policy52 tinha apenas um arquivo maior que 10 MiB: sua cópia de `source.zip`, criada pelo `Run` real no kit de teste. A cópia e o arquivo oficial preservado em `console-cache/metaforce-de8fc69-source.zip` tinham **21.536.851 bytes** e SHA256 `e130131a1a41e8599541d8ab3dd2f31c6d8abaa9af03411f8bba25c3f5b63f21`.

Somente a cópia do kit autoral foi removida. Os **145 outros arquivos** da fixture permaneceram com os mesmos hashes, tamanhos e identidades, incluindo a mídia autoral de 8 KiB, saves de teste, produto autoral não executado, logs e resultados. O kit histórico fica incompleto após a limpeza; uma nova execução usa o teste em uma pasta nova e o ZIP compartilhado preservado.

- Espaço livre antes/depois: **99.771.523.072 → 99.793.063.936** bytes.
- Variação observada nesse lote: **+21.540.864** bytes.

Recibo:

`C:\Users\bradg\Downloads\GetAll-R18\evidence-r18\three-upstreams-20261127\cleanup-policy-source-20261127T215117Z-bd512aae\result.json`

SHA256: `c2d046385107afe903474e03d304ab6da7223d8e89dcee80cb6e5d7a52eeeb48`.

## Continuidade

Os cinco lotes de limpeza desta rodada somam **11.727 arquivos e 5.332.203.105 bytes lógicos** removidos. Variações de espaço entre lotes incluem outras atividades e não são atribuídas à limpeza. `LIMPEZA-ARMAZENAMENTO.md` foi atualizado com backup de cada versão anterior; SHA256 final `74ba0ff7de8a3bebeb9dd7e95f494bb5c46d8dca0863390b2c47718efe70df29`.

Fontes, bibliotecas linkadas, executáveis/DLLs finais, dependências, recursos, avisos, relatórios, mídia pessoal, saves, caches/toolchains compartilhados, prévias e todos os trabalhos MKW foram preservados. Não houve nova compilação nativa, commit, push ou publicação nesta limpeza.
