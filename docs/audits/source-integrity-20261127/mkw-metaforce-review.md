# Auditoria de fonte: MKW, Metaforce e Savage Wind

Data de referência: 27/11/2026, America/Fortaleza. Auditoria estática, com consultas de proveniência e comparações de bytes; nenhuma compilação ou alteração de produto foi executada nesta auditoria.

## Conclusão

**MKW recebeu código novo do AllFix que implementa funcionalidade antes ausente no compilador de shaders.** O decoder oficial foi substituído e o emissor ganhou suporte a modalidades de LEA/ULEA que o código original rejeitava. Isso ultrapassa instalar ou chamar o launcher oficial. Não encontrei implementação de pistas, personagens, regras ou outras mecânicas de jogo nos acréscimos examinados; tampouco existe prova de que essa variante execute Mario Kart World com a mídia comercial. Seria incorreto transformar essa ausência de gameplay novo em uma afirmação de que o código de terceiros ficou intacto.

**Metaforce recebeu 12 substituições em oito arquivos**, incluindo dois arquivos do jogo. Nesses dois, a mudança é exatamente habilitar `malloc.h` também sob MinGW. As demais mudanças envolvem COM/WMI, link e imports, cabeçalhos Windows e a retirada do descritor C++ de diagnóstico de Dawn no caminho MinGW. Não foram encontradas implementações de funções de gameplay ausentes nos diffs desta integração.

**Savage Wind usa as ferramentas e o runtime oficiais sem escrever seus fontes.** A integração replica a preparação do launcher com comandos próprios, gera o código a partir da mídia, compila a DLL e escreve configurações que desligam download de DLSS, pré-compilação inicial de shaders e verificação de atualizações. Também ignora opções de lançamento salvas. São mudanças observáveis no fluxo/configuração; não são implementação de gameplay.

Nenhum dos três pode ser descrito como jogo homologado por esta auditoria. Os registros examinados não contêm primeiro boot comercial.

## Escopo e identidades verificadas

- Desktop: `brad38/Allfix@921295de12349e726f7ca21a5edd8a8ecee123d8`.
- MKW upstream: `adriadam10/mkw-recomp@006d48de08849495e01e151602690d0ec322af82`, release `v0.1.18`.
- Metaforce: `de8fc69bd7f345d6cf5f0c8fc2798295e22522d3`, árvore `9d693e8894c031e5d1d220f39a44999d4010dc9f`, recuperada no espelho `Antidote/metaforce`.
- Aurora: `40cf48fce6ce85366608596bae018c6188f2b2e7`; Borealis: `d4d7ff146ff4097d64bb24e52459152f1b5e597a`.
- Savage Wind: `Revivedx/SavageWindRecomp`, tag `v0.6.0-alpha.6`; árvore retornada na consulta: `02041fdf3f5ee0a1496c4fcc9898162fc362d1df`.

Foram conferidos 45 arquivos locais contra os blobs publicados do Desktop, incluindo os 15 serviços C# desta fatia e o conteúdo de `Tools/MkwSm86`. Todos coincidem. Foram conferidos 32 blobs de fontes originais contra árvores consultadas novamente no GitHub: seis de MKW, quatro de Aurora e 22 de Savage Wind. Todos coincidem. O ZIP Metaforce tem SHA-256 `e130131a1a41e8599541d8ab3dd2f31c6d8abaa9af03411f8bba25c3f5b63f21`; os seus 2.070 arquivos coincidem com a árvore Git, considerando a conversão de final de linha declarada pelo checkout. A árvore Git preservada tem 2.271 entradas e não divergiu da consulta atual.

No Windows, a cópia original dos 2.070 arquivos Metaforce foi comparada com a cópia usada na compilação: somente `src/MetroidPrime/CActorLights.cpp` e `src/Kyoto/Particles/CElementGen.cpp` mudaram; não há arquivo faltante nem arquivo adicional fora de `extern`. Os oito arquivos finais dos patches foram relidos por hash e coincidem com os resultados calculados das 12 substituições. Isso é verificação de bytes, não aceitação automática de justificativas de `ORIGIN.json`.

## Achado MKW-01 — implementação de funcionalidade do compilador

Classificação: alteração semântica e componente novo; impacto alto para a definição de escopo do AllFix.

`Services/GameInstallationMkwCliBackend.cs:92-150` grava quatro overlays e 13 módulos em uma cópia do pacote. O arquivo `FILES` também recebe os módulos novos. O pacote de suporte tem 63.227 bytes e SHA-256 `1c79d30594951495f210a349da05aabe0e240f0189dba87c95a78da73a4500ce`. Seus 25 membros declarados e o manifesto foram confrontados com os arquivos literais publicados. As quatro preimages e postimages também foram comparadas.

| Arquivo ou componente | Mudança observada nos bytes |
|---|---|
| `sm86/translate/frontend/program.py` | Remove a classe `Decoder` original e importa o backend AllFix. O novo backend usa a CLI de `nvdisasm` e reconstrói o modelo de operandos consumido pelo tradutor. |
| `lea_overlay.py` | Substitui `Builder.lea` e `Builder.ulea` em execução. Implementa carry-in `.X`, carry-out, formas `.HI` e `.SX32`, tratamento de negação/inversão e emissão GLSL correspondente. |
| `memory_overlay.py` | Substitui `Builder.global_search` e corrige a palavra alta do endereço para deslocamentos negativos, acrescentando `- 1u` na expressão emitida. |
| Adaptadores scalar/control/memory/texture | Implementam a tradução de texto do desassemblador para campos do consumidor, com validações e rejeições de formas não cobertas. O parser vendorizado é uma cópia sem modificação de seu blob upstream; os adaptadores são código AllFix. |
| `tools/prepare/shaderstep.py` | Substitui geração/captura da especificação original pelo descritor da CLI. Retira `--no-validate`, ativando a validação SPIR-V nesse caminho. |
| `tools/shaders/extract.py` | Reescreve delimitação/recorte dos shaders e verificações de BNSH/BAHS/NDSR; passa a propagar erros de BNSH antes ignorados. |
| `tools/shaders/translate.py` | Muda identidade do cache e requisitos de reflexão, invoca `spirv-val` ao lado de `glslc` e falha quando há shaders inválidos ou nenhum trabalho. |

A evidência direta de funcionalidade antes ausente está no original `sm86/translate/glsl/alu.py:135-138`, que lança `Unsupported("ULEA with carry")`, e em `:358-364`, que rejeita LEA.HI com carry-out. O overlay AllFix implementa ambos. Os arquivos `alu.py`/`mem.py` permanecem em disco com bytes originais, mas seus métodos são substituídos em memória. Uma auditoria que procurasse somente arquivos regravados perderia essa alteração.

Fontes primárias:

- [Emissor oficial original](https://github.com/adriadam10/mkw-recomp/blob/006d48de08849495e01e151602690d0ec322af82/sm86/translate/glsl/alu.py).
- [LEA AllFix publicado](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Tools/MkwSm86/support-src/files/sm86/translate/frontend/allfix_sm86/lea_overlay.py).
- [Memória AllFix publicada](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Tools/MkwSm86/support-src/files/sm86/translate/frontend/allfix_sm86/memory_overlay.py).
- [Aplicação dos overlays](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationMkwCliBackend.cs).

## Achado MKW-02 — rejeições e limites da prova

Nos módulos AllFix examinados, um opcode desconhecido não vira fim de programa, uma forma sem suporte não vira valor constante e um shader inválido não é promovido a sucesso. `cli_decoder.py:58-73,89-136` verifica sintaxe, tamanho, endereços contíguos, código de saída e número de instruções; erros lançam exceção. `Fields.finish` rejeita modificadores não consumidos. As restrições de memória e textura rejeitam casos com semântica não comprovada, por exemplo acessos ordenados/voláteis, certos endereços uniformes e predicados de fault de textura. O emissor original contém no-ops próprios para algumas instruções de controle; esses trechos já constavam no blob original e não foram escritos pelo AllFix.

O caminho antigo `mkw-0.1.18-prepare` também tem um patch: `RestrictMkwShaderStep` substitui a extração automática da especificação por erro, exigindo o arquivo externo. O caminho novo é `mkw-0.1.18-cli-prepare`. `v0.1.18-allfix-cli` é explicitamente definido como identificador local, não uma release publicada pelo upstream. A presença desse rótulo correto não transforma a implementação em código oficial.

As provas anteriores incluem 49.248 comparações de aritmética LEA e 22.132 de endereço, executando expressões emitidas como C++ no CPU; o teste LEA compara com uma transcrição do folding de Mesa. Isso sustenta os casos testados, não todos os shaders do jogo. A cobertura de 99 mnemônicos representa pelo menos formas positivas de cada família, não cobertura de toda a ISA, nem garantia de equivalência. O próprio corpus de textura contém formas rejeitadas. Não há execução de shaders comerciais na GPU nem boot do jogo nos resultados examinados. Não refiz esses testes nesta auditoria.

## Achado META-01 — portabilidade com redução de diagnóstico

As 12 substituições de `Services/GameInstallationMetaforcePatches.cs` foram aplicadas em memória a preimages recuperadas, com unicidade de âncora verificada. Todos os hashes de resultado coincidem com os registros nativos preservados e com os oito arquivos atuais no Windows.

| Arquivo | Resultado da comparação |
|---|---|
| `extern/aurora/lib/system_info.cpp` | Três substituições trocam `_bstr_t` por `SysAllocString`/`SysFreeString` com RAII e preservam as consultas WMI. Acrescentam retorno `Unknown` quando alocação falha. |
| `extern/aurora/cmake/aurora_core.cmake` | Remove dependência MSVC `comsuppw` e usa libs COM/Windows de MinGW. |
| `extern/aurora/lib/webgpu/gpu.cpp` | Duas substituições desviam a cadeia diretamente para `DawnTogglesDescriptor` sob MinGW. Com isso o callback `wgpu_log` e o descritor C++ de plataforma de profiling deixam de ser configurados por esse trecho. O original já definia backend validation como `Disabled`; não se deve apresentar esta mudança como desativação nova desse controle. |
| `nodConfig.cmake` | Duas substituições fixam `nod.dll` e `nod.lib` nos imports. |
| `extern/borealis/CMakeLists.txt` | Acrescenta alvos Windows 10 para APIs já usadas. |
| `DolphinCardPath.cpp` | Usa `shlobj.h`/`knownfolders.h` no MinGW. |
| `CActorLights.cpp`, `CElementGen.cpp` | Somente amplia o condicional de inclusão de `malloc.h` para MinGW. |

A configuração também desliga Sentry, Tracy, exemplos/testes e suporte BZIP2 do FreeType (`GameInstallationMetaforceNative.cs:212-215`). São opções explícitas, não remoção observada de gameplay. O build continua usando o alvo oficial `metaforce`, as fontes reais e os runtimes Dawn, SDL3 e nod. Não foi encontrada substituição de unidade de jogo por stub nesta fatia. O arquivo de mídia continua externo e é aberto em leitura. A prova preservada executou `--help`, verificações de staging e ABI; não comprova gameplay.

Fontes primárias: [patches publicados](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationMetaforcePatches.cs), [configuração nativa](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationMetaforceNative.cs), [GPU original de Aurora](https://github.com/encounter/aurora/blob/40cf48fce6ce85366608596bae018c6188f2b2e7/lib/webgpu/gpu.cpp).

## Achado SW-01 — preparação oficial reorquestrada e opções alteradas

Não há substituição de fonte do jogo no serviço Savage Wind examinado. O kit exige um manifesto de 136 arquivos, é copiado e conferido novamente depois da geração e link. Os comandos de `SavageWindCompilerArguments` coincidem com as flags do Makefile original; inclusive `-Wno-return-type` e desativação de vetorização já eram opções oficiais, não atalhos introduzidos para ocultar uma implementação incompleta. O HLE para módulos não-main também está no gerador oficial.

Há diferenças de experiência: `GameInstallationSavageWindBuild.cs:21,92` escreve `dlss_download=0`, `precompile_shaders=0`, `check_updates=0`, `start_in_config=0`. As definições upstream em `runtime/settings.h:142-147` confirmam que essas opções controlam download, preparo inicial, atualizações e entrada pela configuração; não demonstram remoção do renderer. `GameInstallationSavageWindOutput.cs:15,162` passa `--no-launch-flags`, que o código oficial `launch_flags_boot.c` usa para ignorar opções salvas. O lançamento vai direto para `--play`.

O teste autoral com NSO de 658 bytes usa `--no-sites`. Ele está em uma função separada, exige o hash exato da fixture e uma pasta nova. A produção chama o gerador sem `authoredFixture=true`, conservando verificação de versão/sites. Não encontrei caminho de publicação que substitua a mídia por essa fixture. Os testes compilaram oito unidades sintéticas e a DLL de teste; não demonstram boot de Breath of the Wild.

Fontes primárias: [preparação publicada](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationSavageWindBuild.cs), [compilação/fixture](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationSavageWindNative.cs), [Makefile original](https://github.com/Revivedx/SavageWindRecomp/blob/v0.6.0-alpha.6/Makefile), [opções originais](https://github.com/Revivedx/SavageWindRecomp/blob/v0.6.0-alpha.6/runtime/settings.h).

## Evidências e limite da conclusão

`mkw-metaforce-byte-verification.json` contém as quatro diferenças integrais de MKW, os 12 pares antes/depois de Metaforce e os resultados de integridade. `mkw-metaforce-local-pin-check.json` liga os arquivos lidos aos blobs publicados. Os recibos `metaforce-current-game-tree-diff.json` e `metaforce-current-patched-hashes.json` registram a comparação atual no Windows. As árvores upstream consultadas ficam em `mkw-metaforce-upstream-trees.json` e `metaforce-source-tree-recheck.json`.

Esta fatia permite afirmar quais alterações foram introduzidas nesses três fluxos. Não estabelece que todo o código upstream seja completo, que todos os caminhos originais funcionem ou que jogos comerciais iniciem. O ponto de decisão é concreto: MKW contém desenvolvimento novo do compilador; Metaforce contém portabilidade e perda de diagnóstico; Savage Wind contém orquestração e configurações diferentes. Nada disso autoriza contar os três como jogos com boot comprovado.
