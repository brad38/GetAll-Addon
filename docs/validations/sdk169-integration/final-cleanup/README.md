# Limpeza final após publicação do SDK 1.5.69

**PASS**. Foram removidos **93 arquivos, 181.478.855 bytes**, exclusivamente de quatro diretórios próprios:

| Diretório | Arquivos | Bytes |
| --- | ---: | ---: |
| `publish-desktop-final-sdk169-20261127` | 80 | 165.754.040 |
| `evidence-r18/flow-completion-20261127/harness-build31` | 0 | 0 |
| `evidence-r18/flow-completion-20261127/harness-build31b` | 3 | 116.109 |
| `evidence-r18/flow-completion-20261127/harness-build31c` | 10 | 15.608.706 |

Os **78 arquivos de payload do candidato** foram comparados byte/hash com a prévia completa antes da remoção. `ARTIFACT-MANIFEST.json`, `SHA256SUMS.txt` e `RESOURCE-AUDIT.json` do candidato foram arquivados e verificados em `candidate-receipts/` antes de apagar a cópia intermediária.

As prévias completas SDK167, SDK168 e SDK169, além dos harnesses30 e31d, totalizam **253 arquivos em cinco raízes**. Todos permaneceram com os mesmos nomes, tamanhos e SHA256. Os recibos dos três builds falhos também ficaram intactos. Os diretórios do repositório `bin`/`obj`, fontes, caches, toolchains, mídias originais e dados pessoais ficaram fora de todas as raízes de remoção.

A prévia completa169 continua com manifesto SHA256 `18cbb75144560fbacbe20708b0b3a63a95577d85490a814cc4dece4d770d9590`. O espaço livre observado passou de 102.123.524.096 para 102.305.079.296 bytes; a soma de tamanhos removidos acima é lógica, distinta da variação de blocos do volume.

## Evidência e execução

- [Resultado](result.json): SHA256 `fa2215792b510614036a44b1297d11b23b908d7d806215b1145b58e8fcae4ef3`.
- [Plano fechado](final-cleanup-plan.json): SHA256 `7e9298276b3c2fdfdda238e5e33f3862c24c2e36079691cbb95ab62bfa3ecfcb`.
- [Script de aplicação](apply-final-cleanup.py): SHA256 `ae62a7c0fa2cc0f027262b0cfd0573a49c6293fcf7774b237ac186109188f72b`.
- [Planejador somente leitura](plan-final-cleanup.py): inventaria e valida os payloads sem remover arquivos.

O coordenador liberou a execução depois de terminar a cópia dos recibos de publicação. O script exigiu `--execute`, o hash exato do plano, raízes fixas, recusa de links/reparse points, validação completa antes de remover e uma segunda verificação de cada arquivo imediatamente antes da exclusão. A remoção de diretórios utilizou `rmdir`, que recusa conteúdo inesperado. As verificações dos itens preservados foram repetidas no fechamento.

Não há executáveis ou outras evidências binárias nesta pasta. O caminho original Windows da evidência é `evidence-r18/flow-completion-20261127/cleanup-final-sdk169` dentro da raiz GetAll-R18.
