# Prévia completa — SDK 1.5.69

A prévia Windows de desenvolvimento está pronta em:

`C:\Users\bradg\Downloads\GetAll-R18\publish-getall-sdk169-20261127`

Ela reúne Desktop **3.0.0**, SDK **1.5.69** e addon **1.5.74**, com os fluxos
Metaforce e MKW CLI. O fechamento registra **142/148 fluxos implementados**:
um homologado histórico e 141 aguardando mídia original. As duas receitas
novas permanecem experimentais. Não houve novo boot comercial comprovado.

## Identidade publicada

| Componente | Revisão ou resultado |
| --- | --- |
| Desktop | [`921295de12349e726f7ca21a5edd8a8ecee123d8`](https://github.com/brad38/Allfix/commit/921295de12349e726f7ca21a5edd8a8ecee123d8) |
| Receitas GetAll fixadas no addon | [`37fbc54ee2d137952d8f1ca2b06f3602410870c9`](https://github.com/brad38/GetAll-Addon/commit/37fbc54ee2d137952d8f1ca2b06f3602410870c9) |
| Catálogo | `3f4603cf42ef43402b4a0a9470232e7d4fcd9eb9`, com os mesmos 148 IDs |
| Índice | 145 receitas para 142 projetos; 144 experimentais e uma homologação histórica |
| Conteúdo final | 79 arquivos listados, mais `ARTIFACT-MANIFEST.json` e `SHA256SUMS.txt` |
| Auditoria | 35 recursos embutidos, 71 avisos e 12 propriedades nativas |
| CI Desktop | [46089235002 — aprovado](https://github.com/brad38/Allfix/actions/runs/46089235002) |
| CI GetAll das receitas | [46089870630 — aprovado](https://github.com/brad38/GetAll-Addon/actions/runs/46089870630) |

As duas PRs permanecem draft, na branch
`work/complete-install-flows-20261127`. A atualização documental posterior
registra os recibos deste pacote; o addon mantém o commit imutável das
receitas mostrado acima. Não houve merge, release pública, alteração de
`version.json` ou substituição da instalação corrente.

| Arquivo | SHA256 |
| --- | --- |
| `AllFix.exe` | `b558afccf6fa50ec9a3899b66055009f04f8ce71cfc4dbcc6ab3886bd0433fcd` |
| `GetAll-Preview.zip` | `dbc36433b462070682949fc211ce8ce2c51b8477141d55251ce440fbc57d9a2e` |
| Manifesto final | `18cbb75144560fbacbe20708b0b3a63a95577d85490a814cc4dece4d770d9590` |

[preview-result.json](preview-result.json) conserva o resultado da montagem.
O manifesto completo está em [full-preview](full-preview), e
[remote-pins.json](remote-pins.json) registra a confirmação no GitHub.

## Compilação, integração e serviços reais

O BUILD31d compilou sem erros ou avisos e passou em **1.967 verificações**.
O parser C# aceitou **145/145 receitas**, e a prova Metaforce Policy passou
em **52 verificações**. O índice também passou no validador estrito com
JSON Schema, SHA256, blobs Git, LF e catálogo fixado; os **60 testes Python**
passaram. Os resultados e limites estão em
[integração SDK169](../sdk169-integration/README.md).

O publisher compilou o aplicativo e extraiu estaticamente seu bundle para
auditoria. O assembly real tem SHA256
`3c6ad7c8909888c13452777db37a6ddea940281f533b8588ba0852984ca2c44d`,
idêntico no output normal e dentro do executável distribuído.
[StoreAssemblyProof](../store-assembly-proof/RUN-RESULT.md) carregou esse
assembly e passou em **20 verificações**, incluindo duas resoluções positivas,
12 URLs alteradas recusadas, catálogo, cache e zero requisições HTTP.

A montagem da prévia reutilizou esse executável auditado, sem nova compilação.
Comparou todos os arquivos copiados com o candidato e fixou o addon aos commits
publicados. As prévias SDK167 e SDK168 foram conferidas e preservadas.

## Reutilização de avisos e ferramentas

O preflight encontrou oito origens antigas em `publish-getall-media-100` que
já não existiam. Todos os arquivos tinham cópias idênticas na prévia SDK168.
[notice-relocations.json](notice-relocations.json) registra a troca das
origens, mantendo destinos, tamanhos e hashes. Nenhum recurso nativo ou
toolchain precisou ser reconstruído por esse motivo.

O auditor foi reutilizado após verificar seus cinco arquivos fixados em
[audit-reuse.json](audit-reuse.json). Os scripts e entradas efetivas estão
neste diretório; os manifestos de transporte distinguem os hashes originais
Windows dos textos normalizados em LF. Não há cópias de executáveis ou
toolchains na documentação Git.

## Reprodução e armazenamento

`publish-desktop-candidate.ps1` constrói e audita o candidato a partir do
checkout limpo, das propriedades fixadas e dos caches compartilhados.
`assemble-preview.py` exige os commits, o hash do manifesto do candidato e
o hash do executável. Seu modo `verify` confere esses pins, os 79 arquivos,
o addon e os checksums. O modo de montagem recusa uma saída já existente.

Depois da validação, o candidato intermediário redundante e os outputs
falhos foram removidos após comparação e recibo, liberando 181.478.855 bytes
lógicos neste lote. Os três recibos do candidato foram arquivados. A prévia completa,
as fontes, os scripts, os logs, os resultados e os manifestos permanecem
preservados. [Armazenamento SDK169](../sdk169-integration/STORAGE.md) registra
a limpeza efetivamente executada e distingue tamanhos lógicos de espaço livre.

## Limites restantes

Restam **seis projetos sem fluxo Windows implementável a partir das fontes
disponíveis**: Courage Reborn, Project 2099, as bases de decompilação MKDD,
TMC e MML1, e o ID antigo Wind Waker Recomp cujo sucessor já está coberto.
As condições concretas estão em
[contratos restantes](../remaining-projects-20261127/README.md) e
[sucessor Wind Waker](../sdk169-integration/wind-waker-successor-contract.json).
O denominador de 148 projetos foi preservado; sucessores não foram contados
duas vezes.
