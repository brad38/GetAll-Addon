# SDK 1.5.69 — consolidação do armazenamento

Os sete lotes de limpeza registrados removem **11.797 arquivos e 5.389.561.073 bytes lógicos**: aproximadamente **5,39 GB** (5,02 GiB). Este documento consolida remoções já executadas; sua criação e atualização não executaram novas exclusões.

| Parcela | Arquivos removidos | Bytes lógicos removidos |
| --- | ---: | ---: |
| Cinco lotes anteriores, incluindo Metaforce | 11.727 | 5.332.203.105 |
| Último lote MKW: cópias verificadas de nvdisasm | 6 | 35.684.352 |
| Último lote MKW: fixtures autorais | 62 | 14.933 |
| Lote posterior à validação integrada 31d: ZIP duplicado e transporte base64 | 2 | 21.658.683 |
| **Total dos sete lotes** | **11.797** | **5.389.561.073** |

As duas parcelas MKW pertencem à mesma execução. Bytes lógicos são os tamanhos dos arquivos removidos, não uma medição atual do espaço livre. O recibo MKW não registra espaço livre antes/depois; atividades concorrentes impedem inferir esse valor pela soma dos lotes.

## Lote MKW

A [cópia integral do recibo](cleanup-native-attempts-20261127.receipt.json) tem **27.752 bytes**, SHA256 `dff865fecdd027c2483bf173583b331d01b5e06892ca93257254c0542d4be980`. Seu resultado é `PASS`, com execução de `2026-11-27T22:03:04.3774770Z` a `2026-11-27T22:03:06.1184116Z`.

O recibo lista individualmente os 68 caminhos, tamanhos, hashes e classes de artefato. Todos pertencem às tentativas próprias `backend-native-2` a `backend-native-7`. As seis cópias de `nvdisasm.exe` tinham 5.947.392 bytes cada e SHA256 `f0ab98df225b9f2568e8f56c24a919a4e1362425fb7c02101afbf85022324add`. As outras 62 entradas são fixtures sintéticas autorais, totalizando 14.933 bytes.

Esta consolidação conferiu o hash do recibo, a unicidade e o escopo dos caminhos, as contagens, as somas por classe e a igualdade dos registros de preservação antes/depois. Os registros preservados são:

| Conjunto preservado | Arquivos | Bytes | SHA256 do inventário |
| --- | ---: | ---: | --- |
| Fontes, logs e avisos das tentativas antigas | 829 | 10.518.851 | `97574e6b2524d4bec0994dd5cd9dc8a6f85f047d302f2756ef4be7783f42443c` |
| Prova final Native8 | 220 | 8.296.116 | `23ed715c3d63962e0eb3fb464a0b6c48791e070ad932d1d1898c86db3135b603` |
| Scripts, logs e recibos externos às tentativas | 44 | 298.704 | `6107ba05d11a96582dc2c9ef7385aa6b906a6fde9b551839bb5ce27dd0efcda4` |

O ZIP de nvdisasm no cache compartilhado permaneceu com SHA256 `a348209c803fa67b7bc216a5b4d7a6f9a117ccc60a8c567eb94cf25ba737ec47`. A prova Native8, o checkout Desktop, a documentação Git, os caches compartilhados e as mídias originais estavam expressamente fora do escopo de exclusão.

Recibo original no Bradsson:

`C:\Users\bradg\Downloads\GetAll-R18\evidence-r18\mkw-independent-20261127\cleanup-native-attempts-20261127.receipt.json`

O plano tem SHA256 `6a2827055f01fd200f30295fb812c6e3d28ca6715f371152431896e8397fdddc`. Plano, script e recibos originais permanecem na área de evidências MKW.

## Lote posterior à validação integrada 31d

O [recibo Policy31d](cleanup-policy31d-result.json) tem **1.861 bytes**, SHA256 `ca41a8380b6e2966c5498b6420944d27cc7150188ae9f948fe18bfd694bb5509`, com resultado `PASS` e término em `2026-11-28T00:42:27.956012+00:00` (27/11/2026, 21:42:27, em Fortaleza).

Foram removidos somente dois arquivos próprios da tarefa, totalizando **21.658.683 bytes**:

- A cópia de `source.zip` no kit autoral `metaforce-policy-build31d`: 21.536.851 bytes, SHA256 `e130131a1a41e8599541d8ab3dd2f31c6d8abaa9af03411f8bba25c3f5b63f21`.
- O transporte `evidence-transfer31d.zip.b64`: 121.832 bytes, SHA256 `3bd29638620fc9b048c321a99c9d455a28ca30aeb72d26458780e5e06983d768`.

O recibo registra a preservação de **145 outros arquivos da Policy, totalizando 1.605.553 bytes**, do ZIP oficial no cache compartilhado e do resultado da validação integrada `build31d-result.json` (6.687 bytes, SHA256 `51f98c91d7a0ff2a925ac0a5043217e795ece487fa5478347acfa0f3277229a9`). O manifesto anterior à limpeza tem 47.987 bytes e SHA256 `c70a7bb0408e44b3f4ffb1dac0946fdfb7ae818b54483d11b63203443b4c1dc1`.

O espaço livre observado nesse lote passou de **103.018.151.936 para 103.039.766.528 bytes**, uma variação de **+21.614.592 bytes**. Essa variação é distinta da soma dos tamanhos lógicos removidos e não constitui uma medição atual do disco.

O kit autoral histórico ficou intencionalmente incompleto após retirar sua cópia de fonte; a reprodução deve usar uma pasta nova e o cache compartilhado preservado. O recibo declara que mídia original, dados pessoais, build ativo, harness, toolchains e dependências compartilhadas ficaram fora do escopo de remoção.

## Base dos cinco lotes anteriores

O subtotal de 11.727 arquivos e 5.332.203.105 bytes vem do [relatório de limpeza Metaforce](../metaforce-de8fc69/CLEANUP-OBJECTS.md), com 3.497 bytes e SHA256 `fcbb49b881b18bbb3f718a54e1c5ea19fec222908f26e44f576319afd33cd959` nesta consolidação. Esse relatório registra os cinco lotes e identifica os dois recibos Metaforce:

| Lote incluído no subtotal | Arquivos | Bytes lógicos | SHA256 do recibo |
| --- | ---: | ---: | --- |
| Objetos compilados `.obj`, `.o` e `.res` | 1.293 | 34.448.295 | `f5058db262118f26a6db82b68ca4ff823a9bed9bba9250c157f331123b604adc` |
| Cópia redundante de `source.zip` no kit autoral Policy52 | 1 | 21.536.851 | `c2d046385107afe903474e03d304ab6da7223d8e89dcee80cb6e5d7a52eeeb48` |

Esses dois lotes **já fazem parte** do subtotal; não foram somados novamente. Seus recibos originais estão sob:

`C:\Users\bradg\Downloads\GetAll-R18\evidence-r18\three-upstreams-20261127`

respectivamente em `cleanup-objects-20261127T214812Z-cf5340d4/result.json` e `cleanup-policy-source-20261127T215117Z-bd512aae/result.json`. O relatório registra conferência dos demais arquivos, dos 128 arquivos de provas/produtos e dos 145 outros arquivos da fixture, além da preservação do ZIP oficial no cache compartilhado.

O hash de `LIMPEZA-ARMAZENAMENTO.md` registrado após esses cinco lotes é `74ba0ff7de8a3bebeb9dd7e95f494bb5c46d8dca0863390b2c47718efe70df29`; ele corresponde à versão anterior à consolidação do último lote MKW.

## Alcance desta verificação

O [resumo estruturado](storage-summary.json) conserva a origem dos números e os hashes. Os recibos MKW e Policy31d foram verificados diretamente a partir das cópias locais integrais. O subtotal anterior foi conferido contra o relatório local já existente; os recibos Windows dos cinco lotes anteriores não foram reabertos nesta tarefa. Portanto, este registro não declara uma nova inspeção do disco Windows nem uma nova medição de espaço disponível.

Fontes, receitas, scripts de reprodução, logs relevantes, resultados, manifestos e hashes continuam preservados. Caches e toolchains compartilhados permanecem reutilizáveis. A consolidação não duplica executáveis, toolchains, mídia ou extrações temporárias.
