# MKW: tradutor privado por CLI normal

O perfil `mkw-0.1.18-cli-prepare` usa o kit oficial `v0.1.18` e solicita uma única pasta original do usuário. O alias local `v0.1.18-allfix-cli` identifica esse contrato no catálogo; ele não representa uma tag upstream. O perfil anterior `mkw-0.1.18-prepare` permanece separado, com suas duas entradas originais. Estados antigos não são promovidos automaticamente.

Este pacote contém fontes Python, quatro adaptações de arquivos oficiais, um descritor fechado, avisos e a receita da prova autoral. O executável NVIDIA é obtido separadamente pela URL oficial fixada. O arquivo instalado `sm86/instructions.json` é um descritor interno com versão e hashes; não contém uma tabela de codificação NVIDIA.

## Pins

| Item | Identidade verificada |
| --- | --- |
| Fonte MKW | `adriadam10/mkw-recomp`, commit `006d48de08849495e01e151602690d0ec322af82` |
| Kit oficial Windows | 221.949.886 bytes; SHA256 `ff655d6dc566d315c9f33f96b9b94b7dc7e9c1b383091ed36c7f35921b6444c8` |
| Suporte incorporado | `mkw-sm86-cli-support-v1.zip`, 63.227 bytes; SHA256 `1c79d30594951495f210a349da05aabe0e240f0189dba87c95a78da73a4500ce` |
| Recurso .NET | `MkwSm86.cli-support.zip` |
| NVIDIA nvdisasm | Redistribuível Windows x86_64 12.8.90, ZIP 5.368.805 bytes; SHA256 `a348209c803fa67b7bc216a5b4d7a6f9a117ccc60a8c567eb94cf25ba737ec47` |
| Executável privado | 5.947.392 bytes; SHA256 `f0ab98df225b9f2568e8f56c24a919a4e1362425fb7c02101afbf85022324add` |
| Licença NVIDIA | 63.021 bytes; SHA256 `e2c71babfd18a8e69542dd7e9ca018f9caa438094001a58e6bc4d8c999bf0d07` |

URL fechada do redistribuível:

`https://developer.download.nvidia.com/compute/cuda/redist/cuda_nvdisasm/windows-x86_64/cuda_nvdisasm-windows-x86_64-12.8.90-archive.zip`

O manifesto no ZIP relaciona os 26 membros, seus tamanhos e hashes, os 13 módulos instalados e as quatro preimagens/resultados oficiais. Todas as preimagens são verificadas antes de escrever qualquer adaptação na cópia privada. `ValidateMkwCliInstalled` confere fontes, descritor, avisos, executável AMD64, licença e presença dos módulos na identidade de retomada `FILES`.

## Caminho executado

`shaderstep.shaders` chama o extrator BNSH oficial adaptado, `pipeline_pairs.py` e `translate.py`. Este último carrega o modelo original `Insn`/`Sph` e o novo `Decoder.program`. Cada programa é enviado ao executável NVIDIA fixado com `--binary SM86 --no-dataflow`. O adaptador converte a saída textual aos campos que o consumidor original lê; o emissor original produz GLSL. O compilador e o validador SPIR-V privados do kit são usados por caminhos explícitos. O empacotador original produz `shaders.pack`.

Não há chamada a `sm86/spec/spec.py`, inspeção de memória de processo nem fallback para captura. Não há tabelas globais, shaders de jogo, ROM ou mídia comercial no suporte. A importação dos pequenos overlays de emissão é adiada até a inicialização do decoder para preservar a ordem real de imports do tradutor.

## Cobertura e limites

A análise do consumidor fixado identificou 99 nomes de instrução, 98 campos literais e 31 expressões de campos dinâmicos. Os adaptadores têm quatro grupos: 58 famílias escalares, 16 de controle, 16 de memória/atributos e nove de textura/imagem. LEA/ULEA passam pelo overlay específico antes do grupo escalar. A relação exata de nomes e provas está em `support/coverage-completion.json`.

O corpus público foi submetido à CLI normal: 2.917 palavras em 90 mnemonics, sem divergência de nome; cinco palavras com combinação de scheduling/reuse rejeitada pela CLI permanecem negativas. O corpus isolado fornece prova positiva para 81 nomes, sem associação de campo quebrada. Os programas contextuais autorais e a prova de texturas completam os 99 nomes consumidos. Isso não demonstra todas as variantes da ISA SM86 nem todos os shaders comerciais do jogo.

Formas desconhecidas falham explicitamente. Entre os limites deliberados estão endereços descritores, ponteiros globais de 32 bits sem lowering comprovado, bases uniformes não rastreadas no fallback, modos de coerência/ordenação não representados pelo consumidor, handles de textura bindless e variantes já recusadas pelo emissor original. Nenhuma dessas formas vira EOF, instrução vazia ou GLSL presumido correto.

As classes de compatibilidade e as unidades de deslocamento preservam o contrato original: LDC/ULDC usam bytes, operandos ALU de constant bank usam palavras, IPA usa palavras e ALD/AST usam bytes. O fallback de endereço de 64 bits preserva a extensão de sinal do deslocamento; a base uniforme não pode ser descartada. O overlay LEA preserva deslocamento/concatenação, complementação posterior, carry e aliases de registradores.

Cada programa fica limitado a 1 MiB de instruções, 30 segundos por chamada de nvdisasm, 16 MiB de stdout e 64 KiB de stderr. Os dois pipes são drenados em paralelo e o processo é encerrado ao ultrapassar os limites. O runner do Desktop mantém seu token restrito, cancelamento e árvore de processos. Arquivos temporários de entrada são removidos em `finally`.

O extrator valida os limites declarados de contêineres, controles, código e constantes. Uma cauda não zero após terminador zero ou um segundo cabeçalho ambíguo é recusado. Um BNSH inválido faz a etapa falhar mesmo após um contêiner anterior válido. `translate.py` termina com código diferente de zero se houver erro de lowering/compilação ou nenhuma tarefa. O cache de sucesso exige SPIR-V, reflexão e resultado; os módulos novos entram em `FILES` e na chave do tradutor.

## Evidência executada em 2026-11-27

| Prova | Resultado observado |
| --- | --- |
| Caminho normal completo, pacote final | `backend-native-8`: exit 0, `MKW_NORMAL_CLI_NATIVE_PASS`, 77 verificações |
| Programas autorais BNSH | 14 extraídos e 14 SPIR-V válidos; estágios cs, vs, ps, task e mesh |
| Empacotamento | 15 programas no pack, incluindo o vertex auxiliar oficial; pares de pipeline no formato oficial |
| Retomada | Remoção de `.res.json` forçou reconstrução pelo caminho real de cache |
| Falhas reais | Contêiner válido seguido de truncado e cauda não zero recusados no extractor; lowering não suportado retornou exit 1 e manteve `failed.tsv` |
| Texturas/imagens | 482 casos: 293 decodificados, 285 GLSLs, 189 recusas do adaptador e oito recusas do consumidor; nove famílias positivas e três negativos de fronteira |
| SPIR-V de texturas | Nove fontes representativas passaram glslc e spirv-val no kit privado |
| LEA | 216 variantes autorais e 257 registros públicos aceitos; 49.248 comparações numéricas executadas contra o folding Mesa |
| Endereço signed64 | 11 deslocamentos confirmados pela CLI; 22.132 comparações numéricas executadas |
| SPIR-V complementar | Quatro variantes LEA e composição com 75 instruções passaram compilação e validação |

A prova usou somente programas autorais e registros públicos. Ela não executou shaders em GPU, não usou a mídia de Mario Kart World e não comprova boot do jogo. Os testes .NET do provedor e a integração do SDK são gates separados; os resultados devem ser registrados após o harness central, sem reaproveitar o status desta prova para antecipá-los.

Os recibos completos de comandos, hashes e saídas estão em `proof/windows-receipts.json` na área de desenvolvimento e nos logs Windows `evidence-r18/mkw-independent-20261127`. As fixtures binárias/SPIR-V da prova final foram removidas depois de registrar tamanho e hash. Fontes, scripts, logs e manifestos foram preservados.

## Proveniência e reprodução

O consumidor e as quatro preimagens vêm exclusivamente do ZIP oficial fixado. O parser textual MIT é `kuterd/nv_isa_solver` no commit `3640363b7d7f3ddd4a65b67502687d2d5f147d92`, arquivo `parser.py` SHA256 `4db3ec6bcfab76f0480250183148b8c0b2357187a7bb6684dd92d99f9b00068e`. O solver não é executado nem distribuído; o parser recebe somente texto produzido pela CLI normal.

As referências abertas de codificação são Mesa 26.3.0 `src/nouveau/compiler/nak/sm70_encode.rs` e `ir.rs` (MIT), e os registros de CuAssembler no commit `96a9f72baf00f40b9b299653fcef8d3e2b4a3d49` (MIT). A licença Mesa completa acompanha seu cabeçalho de copyright. As fontes consultadas e seus hashes estão em `sources.json` e `references/mesa-lea-sources.json`. Nenhum trecho de ScarletNX integra o pacote.

`build_support.py` reconstrói o ZIP de forma determinística, com timestamps fixos e sem binários. `prove_backend.py` mais `proof/backend-fixtures.json` reproduzem a cadeia autoral com o ZIP, Python/glslc oficiais já existentes e o nvdisasm pinado. As rotas do harness são `--mkw-cli-policy` e `--mkw-cli-native <official.zip> <kit-existente> <cache> <work-novo>`.
