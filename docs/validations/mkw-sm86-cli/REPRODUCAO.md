# Reprodução e limites do registro

Esta pasta preserva a disposição de caminhos usada pelos scripts. Ela contém fontes e recibos; não incorpora o corpus CuAssembler bruto de 1,55 MB, ferramentas executáveis, a mídia do jogo ou shaders comerciais. Os bytes de fontes originais foram preservados. Os recibos Windows com CRLF aparecem como strings JSON escapadas em `proof/windows-receipts.json`; o próprio arquivo versionado usa UTF-8 sem BOM e LF.

## Reconstruir somente o suporte distribuído

Com Python 3.12 ou posterior, a partir desta pasta:

```text
python build_support.py
```

O resultado deve ter 63.227 bytes e SHA256 `1c79d30594951495f210a349da05aabe0e240f0189dba87c95a78da73a4500ce`. Essa reconstrução usa somente as fontes presentes, sem rede nem execução de ferramenta NVIDIA. `support/package.json` registra o resultado e `support/manifest.json` relaciona cada membro. No Desktop o mesmo ZIP entra como `MkwSm86.cli-support.zip`; a cópia legível e o empacotador alternativo desse recurso ficam em `Tools/MkwSm86`.

As quatro preimagens oficiais estão em `upstream/`: `sm86/translate/frontend/program.py`, `tools/prepare/shaderstep.py`, `tools/shaders/extract.py` e `translate.py` (esta última corresponde a `tools/shaders/translate.py` no kit). `build_support.py` exige seus hashes exatos antes de aplicar as mudanças.

## Reproduzir a cadeia autoral Windows

Reutilize o ZIP oficial `mkw-recomp-0.1.18-windows-x64.zip`, 221.949.886 bytes, SHA256 `ff655d6dc566d315c9f33f96b9b94b7dc7e9c1b383091ed36c7f35921b6444c8`, publicado em:

`https://github.com/adriadam10/mkw-recomp/releases/download/v0.1.18/mkw-recomp-0.1.18-windows-x64.zip`

Use Python, glslc e spirv-val da árvore verificada desse kit e o redistribuível NVIDIA identificado no manifesto. A prova copia somente `mkw-recomp/setup/src/` para uma área nova; ferramentas existentes são reutilizadas. Execute pelo `RunNativeBuildStep` do motor, preservando suas mitigações e cancelamento. A rota de integração do harness faz isso:

```text
dotnet AddonInfrastructure.dll --mkw-cli-native <ZIP-oficial> <kit-existente> <cache> <work-novo>
```

Ela valida os arquivos Python/glslc reutilizados contra os membros do ZIP, chama o provedor C# real e executa `prove_backend.py` sobre a árvore adaptada. A rota `--mkw-cli-policy` é um gate separado de contrato, seleção de mídia, corrupção e cancelamento.

O script Python também aceita execução pela receita do runner diagnóstico registrada em `run_windows_proof.ps1`. Seus argumentos explícitos são `--kit`, `--support`, `--support-sha256`, `--nvdisasm`, `--fixtures`, `--work` e `--official-archive`. `--staged-game` é reservado à prova que já chamou o provedor C#. Nenhum argumento é mídia de jogo.

`backend-native-8` é a prova Python final do pacote, com 77 verificações e 14 programas. Ela não substitui os gates C# do BUILD31, a validação do SDK, o parser das receitas ou o CI remoto. Os resultados dessas outras camadas devem ser registrados separadamente após sua execução.

## Reproduzir as provas numéricas e de corpus

Os scripts `probe_*.py` e os logs correspondentes foram preservados. Para restaurar os dois textos públicos omitidos, prefira o cache existente:

```text
python restore_probe_sources.py --cache <pasta-original-mkw-independent-draft>
```

Se esse cache não existir, `--download` busca apenas as URLs oficiais fixadas em `probe-source-pins.json` e exige tamanho/SHA256 antes de escrever. Esses dois textos são os registros públicos CuAssembler SM86 e `ir.rs` Mesa 26.3.0. A restauração não executa código baixado. O corpus é lido com `ast.literal_eval` sobre os registros numéricos, sem `eval` ou import do módulo de dados.

Os probes Linux esperam o executável `tools/nvdisasm` fixado em `tools/ORIGIN.json`; copie a ferramenta verificada do cache em vez de baixar novamente. Ela usa somente `--binary SM86 --no-dataflow`. As provas numéricas compilam pequenos corpos autorais com o compilador C++ local e removem o executável e o C++ temporário ao terminar. Os scripts LEA e memória importam `Builder` diretamente de `glsl.core`, portanto o adiamento dos imports nos overlays não altera sua reprodução.

O registro `sources.json` também lista fontes consultadas durante a pesquisa. Os arquivos ScarletNX, o solver completo de nv_isa_solver e as classes CuAssembler não são necessários ao suporte nem copiados nesta pasta. A origem consultada não é uma indicação de que código dessas fontes integra a implementação.

## Evidência preservada

- `proof/consumer-contract.json`: levantamento original dos 99 nomes e campos; seus marcadores estáticos históricos não foram reescritos como resultados de execução.
- `support/coverage-completion.json`: ligação de cada nome às provas positivas posteriores, com as limitações explícitas de variantes.
- `proof/adapter-corpus-result.json`, `cli-corpus-result.json`, `texture-adapter-result.json`: provas da CLI, campos, GLSL e recusas.
- `proof/lea-overlay-result.json`, `memory-address-result.json` e logs numéricos: comparação executada contra os modelos Mesa/adicional64.
- `proof/backend-fixtures.json`, programas GLSL e scripts: entradas autorais reproduzíveis, incluindo constantes, branch/retorno, memória, atributos e task/mesh.
- `proof/windows-receipts.json`: resultado final, log real, validações SPIR-V complementares e import scan; cada entrada registra também o hash/tamanho do arquivo Windows original.

As provas confirmam componentes e fronteiras do fluxo. Não houve execução GPU desses shaders, instalação com mídia de Mario Kart World nem primeiro boot do jogo. A receita continua experimental.
