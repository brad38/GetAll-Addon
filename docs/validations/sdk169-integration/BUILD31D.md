# SDK 1.5.69 — gates integrados BUILD31d

Resultado: **PASS** em 27/11/2026, 21:39 no fuso America/Fortaleza. A execução original registra `2026-11-28T00:39:17Z` a `00:39:50Z` em UTC.

| Gate | Resultado | Tempo |
| --- | --- | ---: |
| Toolchain compartilhada | .NET SDK 8.0.425 | 0,219 s |
| Compilação do harness + SDK | zero erros, zero avisos | 10,219 s |
| Regressão padrão | 1.967 PASS, zero FAIL | 11,312 s |
| Parser real do GetAll | 145 receitas aprovadas, zero recusadas | 9,375 s |
| Política/transação Metaforce | 52 PASS, zero FAIL | 0,891 s |

A regressão inclui as 44 verificações do leitor de mídia Metaforce, a política do novo backend MKW e 43 verificações do alias/perfil MKW. O parser executa também checks comuns do harness; esses números não devem ser somados como testes únicos. Nenhuma nova mídia comercial foi aceita e nenhum jogo foi executado. O build C++ nativo Metaforce e Native8 MKW já comprovados não foram repetidos.

O runner conferiu **538 arquivos de fonte** e preservou antes/depois o estado Git, o índice GetAll e o ZIP compartilhado de fontes Metaforce. O índice testado tem SHA256 `2e3ee9a442015c492c84cc28f92f7da75dfffdbbe817d42dc0f3b311cbfac9eb`.

## Tentativas anteriores e correções

BUILD31 detectou ausência de `project.assets.json` antes de compilar. A restauração offline, com fontes NuGet vazias, reutilizou o cache existente e comprovou que os 36 arquivos dos pacotes utilizados não mudaram. BUILD31b detectou apenas uma importação de namespace ausente no teste MKW; foi adicionada `using AllFix.Addons;`.

BUILD31c compilou com zero erros/avisos e expôs uma premissa errada no novo teste de contratos: a receita histórica MKW declara uma mídia original, enquanto a retomada local historicamente exige também o arquivo de shaders. BUILD31d separa esses contratos, conserva a igualdade exata entre receita e retomada do novo CLI e verifica que a receita legada mantém sua mídia/metadados originais. Os negativos agora representam o requisito extra de tabela do fluxo legado e a remoção da mídia original. **Nenhum serviço de produção ou receita foi alterado por essas correções.**

As três tentativas reprovadas permanecem registradas. O resultado final é [build31d-result.json](build31d-result.json), SHA256 `51f98c91d7a0ff2a925ac0a5043217e795ece487fa5478347acfa0f3277229a9`. O manifesto de fontes é [build31d-sources-before.json](build31d-sources-before.json), SHA256 `6bf7cbc0f32ac0c418308b2fc98472cbf067a8c1dc2bf321ec4f522602ce6ede`.

## Reprodução

Use Python 3.12 no Windows e a toolchain .NET 8.0.425 compartilhada. O [runner](run-build31.py) registra sua linha de comando e todos os hashes no [pedido original](build31d-request.json). Ele exige um novo sufixo de execução e recusa sobrepor logs/saídas existentes. Para reproduzir a partir do commit final, informe o seu SHA completo em `--expected-head`; use o mesmo snapshot de 145 receitas e hash de índice. A reprodução não exige baixar a toolchain nem repetir a compilação nativa C++.

O [manifesto de transporte](windows-source-manifest.json) registra tamanhos e hashes originais do Windows e os hashes das cópias locais. Somente os finais de linha dos logs foram convertidos de CRLF para LF; os originais continuam preservados no Windows. Nenhum assembly ou outra evidência binária integra este diretório.

O build do Desktop completo, a prova dos serviços reais de catálogo/download e a publicação/CI são etapas separadas. Este documento não antecipa seus resultados.
