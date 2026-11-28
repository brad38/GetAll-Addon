# Auditoria de integridade das integrações AllFix / GetAll

**Referência: 27/11/2026, America/Fortaleza.** Objeto: verificar se a integração alterou fontes de terceiros ou implementou partes ausentes para apresentar projetos incompletos como jogos prontos. Este relatório audita a integração existente; não altera produto, receitas ou projetos upstream.

## 1. Resultado

**Houve alteração de código-fonte de terceiros. Há também um caso confirmado de implementação de funcionalidade antes ausente: o compilador de shaders de Mario Kart World.** Portanto, seria incorreto afirmar que o trabalho se limitou a baixar jogos, importar ROMs ou executar launchers oficiais.

O caso MKW não consiste em criar pistas, personagens ou regras do jogo: foram implementadas operações de tradução de shaders que o upstream explicitamente rejeitava. Essa distinção explica o que foi feito; não apaga que houve desenvolvimento de funcionalidade faltante no projeto. Também foram encontradas mudanças semânticas de runtime, novos componentes de ligação gráfica, mudanças de localização de dados e recursos gráficos desabilitados.

**Não foi encontrada implementação própria de fases, missões, personagens ou mecânicas ausentes nos deltas e caminhos de produção examinados. Tampouco foi encontrado uso das fixtures sintéticas examinadas como substituto do jogo instalado.** Essa conclusão está limitada aos fontes, diffs e vínculos de produção efetivamente examinados. Não é uma garantia sobre binários sem reconstrução, patches históricos sem fonte preservado ou todas as funções de cada upstream.

**Os 142 IDs não representam 142 jogos comprovadamente jogáveis.** O índice contém 141 IDs experimentais e um `validated` histórico de SM64 Coop Deluxe. Não houve boot com mídia comercial nesta auditoria. Compilar, reconhecer um executável, carregar uma DLL, gerar código e passar num teste sintético são evidências diferentes de executar o jogo. O estado `Completed`/`Verified` do instalador não realiza essa homologação.

Evidências principais: [inventário do catálogo](catalog-review.json), [rastreamento de rotas](service-routing-review.json), [alterações de fonte por projeto](root-review.json), [MKW/Metaforce/Savage Wind](mkw-metaforce-review.md), [FH1/Pinyon/SSX](rex-review.md) e [matriz consolidada](MATRIZ-148.md).

## 2. Escopo, identidade e método

| Componente | Estado auditado |
|---|---|
| Desktop | `brad38/Allfix@921295de12349e726f7ca21a5edd8a8ecee123d8` |
| GetAll | `brad38/GetAll-Addon@ceaa962fe1a2088a7f3900509b856743ff4b6672` — documentação posterior ao código `37fbc54ee2d137952d8f1ca2b06f3602410870c9` |
| Catálogo | `brad38/AllFix-Repo@3f4603cf42ef43402b4a0a9470232e7d4fcd9eb9` |
| Quantidade | 110 jogos no catálogo, 148 IDs de projeto, 142 IDs com receita, 145 receitas contando três aliases |
| Status das receitas | 144 `experimental`; uma `validated` histórica |

As identidades estão fixadas por commit, não por uma página mutável ou somente pelo nome da release. O snapshot do Desktop foi obtido dos objetos Git do checkout Windows: **538 arquivos rastreados; 521 incluídos e conferidos contra seus blobs Git**. Os 17 excluídos da transferência são binários/recursos; suas identidades permanecem no manifesto. Os cinco ZIPs de suporte com fontes relevantes foram incluídos. A auditoria dos auxiliares consultou também as cópias preservadas no Windows.

A revisão combinou os seguintes procedimentos:

1. Leitura integral das 145 receitas e vinculação de todos os 142 IDs às rotas reais do Desktop. O ledger identifica 68 famílias de fluxo; nenhum ID ficou sem rota. Os 33 IDs/34 receitas de build delegados na primeira leitura são cobertos nominalmente por `root-review.json` e pelos relatórios especializados.
2. Leitura dos handlers, geração de código/texto, aplicação de patches, overlays, scripts e configurações. Uma busca literal serviu para localizar candidatos, mas não foi usada como prova de ausência de alteração.
3. Comparação de preimages e postimages, arquivos originais preservados e árvores Git fixadas. Quando havia patches oficiais, estes foram reaplicados para separar a contribuição upstream da contribuição AllFix.
4. Rastreamento dos produtores e consumidores das fixtures até o fluxo de teste e o fluxo instalado. Um arquivo chamado `dummy`, um `return 0` ou uma flag contendo `stubs` não foi classificado isoladamente como fraude de jogo.
5. Conferência dos 97 estados históricos do índice para identificar promoções a `validated`. Não houve outra promoção além do registro histórico de SM64 Coop Deluxe.

Não foram executados builds ou jogos nesta auditoria. Também não se removeu projeto, alterou patch, modificou receita ou publicou correção. As únicas criações são relatórios, inventários, scripts de reprodução e snapshots pequenos de evidência.

## 3. Achados que mudam a resposta à pergunta do usuário

### A. Mario Kart World: funcionalidade faltante implementada

O upstream `adriadam10/mkw-recomp@006d48de08849495e01e151602690d0ec322af82` contém rejeições explícitas para `ULEA with carry` e para LEA.HI com carry-out. O AllFix acrescenta um backend de `nvdisasm` por CLI, 13 módulos e quatro overlays. Entre eles, `lea_overlay.py` substitui métodos do emissor e implementa essas modalidades; `memory_overlay.py` muda o cálculo da palavra alta de endereços.

Esse é o caso mais direto de desenvolvimento de parte faltante do projeto. Os módulos não completam pistas ou mecânicas, mas alteram uma peça necessária para traduzir shaders do jogo. O alias `v0.1.18-allfix-cli` representa uma variante personalizada e não deve ser apresentado como equivalente à release oficial sem qualificação.

As provas preservadas incluem casos de decode/GLSL, SPIR-V sintético e comparações numéricas. Elas não incluem execução dos shaders comerciais na GPU nem boot do jogo. O pipeline observado falha quando não há shaders ou quando há falhas de tradução; não foi encontrada uma substituição geral de shaders por sucesso vazio.

Fontes: [implementação AllFix](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationMkwCliBackend.cs), [rejeições no emissor oficial](https://github.com/adriadam10/mkw-recomp/blob/006d48de08849495e01e151602690d0ec322af82/sm86/translate/glsl/alu.py) e [comparação detalhada com hashes](mkw-metaforce-review.md).

### B. God of War: alteração funcional do leitor de disco

Os dois IDs de God of War usam `ApplyGowDiscSourceContract`. Essa função muda `ps2xIOP/src/disc_source.cpp` para limitar o lote antes do próximo setor com override, permitindo processá-lo separadamente; ela não aborta a leitura inteira. É uma mudança semântica de I/O no runtime, não apenas uma opção do compilador. O método fixa SHA-256 de entrada `beb18105…23cc0a` e saída `a03fa022…5ae6`, preservados integralmente no JSON.

As outras alterações próprias identificadas incluem a inclusão de `<cstdlib>`. A transformação de IPO/GL/LTCG reproduz o script oficial. Os 55 patches aplicados na variante KIexster já pertencem ao projeto oficial e não foram atribuídos ao AllFix.

Também foi verificado um possível falso positivo: `PS2X_ENABLE_FFMPEG=OFF` não significa remoção das cenas em vídeo. O CMake preservado usa `libmpeg2` por padrão; FFmpeg é backend alternativo. A ausência de recompilação nativa opcional VU1/IOP tem fallback para os intérpretes oficiais, não para funções de jogo inventadas.

Fontes: [patch de leitura](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationGowKiexsterNative.cs#L102), [consumo pelo outro fluxo](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationGowBuild.cs), [script oficial](https://github.com/KIexster/god-of-war-recomp/blob/d1d11ec545c3baf2f3fc17e2df4247ac4b732d5c/scripts/compilar.ps1) e `root-review.json`.

### C. Pinyon, FH1 e SSX: runtimes personalizados e opções reduzidas

Esses três perfis usam SDKs modificados. Foram verificados **86 itens de overlay: 82 textos e quatro binários**. A reaplicação de 22 patches oficiais explica exatamente 32 textos; sobram 54 entradas próprias, mais três alterações de CMake fora dos manifests e as fontes das pontes. A atribuição é importante: os grandes patches oficiais de SSX em gráficos/codegen/memória não foram inventados pela integração.

As mudanças próprias incluem ligação ABI, caminhos, providers DLSS e pontes C/C++ para NVIDIA NGX/ETW. As pontes examinadas chamam as APIs reais; ainda assim, são código de runtime personalizado e sua equivalência não decorre de um link bem-sucedido.

Há duas diferenças funcionais confirmadas:

- **Pinyon:** `REXGLUE_FFX_API_LOADER=OFF` e `REXGLUE_FIDELITYFX_RUNTIME=OFF` desabilitam o caminho de FSR 2/3 temporal e geração de quadros FidelityFX. O cache CMake real confirma a configuração. FSR 1/CAS e os caminhos distintos DLSS/LSFG permanecem; não se afirmou remoção de todo FSR.
- **FH1:** `FORZA_REGPU_PLUGIN=OFF` omite sempre o renderer experimental ReGPU. O launcher oficial Windows tenta habilitá-lo e só o retira após uma falha específica; a integração omite a tentativa. O renderer Xenos continua presente.

Fontes: [relatório e diffs residuais](rex-review.md), [configuração Pinyon](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationPinyonNative.cs), [configuração FH1](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationForzaNativeGame.cs) e [builder FH1 oficial verificado](https://github.com/FH1-ReImagined/ForzaHorizon1-ReImagined/blob/46d5ed62866af68700d15c61748df8c29ad0248d/launcher/forza_launcher/builder.py).

### D. GT5: seleção de renderer e ausência do staging de opcionais

A integração força `PS3RECOMP_RSX_VULKAN=OFF`. O instalador oficial tenta preparar Vulkan, mantém um fallback Direct3D 12 e executa o staging de FSR 3; DLSS depende das condições de licença/hardware previstas por ele. O estágio AllFix copia `gt5.exe` e as três DLLs FFmpeg, sem executar esses instaladores de opcionais. Não preserva todas as opções oferecidas pelo setup oficial.

Os quatro arquivos alterados após o patch oficial envolvem CMake, forceinline, include Windows e um alias `getenv` que encaminha ao cache original. Em contrapartida, as flags `--hle-stubs` e `--allow-partial` já existem no `relift.ps1` oficial fixado. Não são evidência de que o AllFix escreveu stubs para completar gameplay.

Fontes: [configuração e staging AllFix](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationGt5Native.cs), [setup oficial](https://github.com/MormonFTP-hub/gt5-recomp/blob/64ca1697c5f9bb513bfe0414d9a36c10dafd0a37/setup.ps1), [relift oficial](https://github.com/MormonFTP-hub/gt5-recomp/blob/64ca1697c5f9bb513bfe0414d9a36c10dafd0a37/GT5/scripts/relift.ps1).

### E. SM64Plus: dados e saves passam a outro diretório

`PatchSm64PlusSource` altera `src/pc/pc_main.c`. O código original escolhia `%LOCALAPPDATA%/SM64Plus`; a versão da integração usa `GetModuleFileNameW`/`SetCurrentDirectoryW` para escolher a pasta do executável. Isso muda a localização dos recursos e dos dados referenciados por caminho relativo, inclusive configurações/saves conforme o contrato do jogo. Há também mudanças no Makefile. Essa alteração é comportamental, ainda que não crie gameplay.

Fonte: [transformação completa](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationSm64PlusSource.cs).

## 4. Demais alterações de fonte e de comportamento

Os grupos abaixo completam os **19 IDs diretamente associados aos conjuntos documentados de edição de fonte de jogo/runtime/compilação específica**. Essa contagem não inclui importadores auxiliares como se fossem gameplay, nem transforma ausência de patch de fonte em prova de pureza de um binário.

| Projeto(s) | Alteração própria observada | Avaliação |
|---|---|---|
| Metaforce | 12 substituições em oito arquivos; nos dois arquivos de jogo, somente `malloc.h` sob MinGW; COM/WMI, link, headers e descritor de diagnóstico Dawn | Compatibilidade/ABI, sem gameplay faltante implementado nos diffs |
| Dr. Mario 64 Recomp | Headers, conversão JSON, hash, fmt/ImGui, imports e integração dos produtos oficiais de patches | Compatibilidade; `dummy.c` oficial não é um jogo fictício criado pela integração |
| StrikersRecomp GameCube | Guardas POSIX, mkdir Windows, COM/WMI, Dawn/ABI e CMake | Ajustes de plataforma/diagnóstico; probe WebGPU separado do jogo |
| SM64ex, Render96ex, SM64RT | Makefiles, host tools, SDL, headers e flags; Discord RPC desligado | Compilação/configuração, sem mecânicas novas observadas |
| Super Metroid `sm` e `sm-rewrite` | Array/includes, GUIDs/casts e argumento `--allfix-runtime-check` | Acrescenta diagnóstico SDL; caminho normal do jogo preservado no diff |
| CTR Turbocharged, receita build | Argumento `--allfix-validate-disc` chama validador já existente | Adaptação da entrada CLI, sem completar jogo |
| Mario Kart Double Dash C++ | SDL obtido do cache verificado e includes `cstdlib` | Build; não confundir com decompilação base nem com port Rust |
| Burnout 3 | CMake para MinGW, flags de imagem/stack e símbolos/linker | Build; utiliza o recompilador e o código manual oficiais |

As fontes de cada linha e os outros 14 IDs com rotas de build examinadas estão em [root-review.json](root-review.json). O ledger por ID inclui também releases prontas, extração de mídia, launchers e os seis sem receita.

Outras mudanças documentadas incluem DKB com FSR4/DLSS e atualização automática desligados, Savage Wind com opções de DLSS/pré-compilação/atualização alteradas, SotC com cvars de culling e patches opcionais selecionados, TOTK com adaptação do reporter do instalador, Radz com mixer de volume desabilitado no build, GT4 com renderer escolhido, e re:Blue com INI de idioma reconstruído a partir dos discos. Elas não são implementações de fases ou regras, mas precisam aparecer na caracterização do produto. Ver [rotas e configurações](service-routing-review.md) e [Savage Wind](mkw-metaforce-review.md).

## 5. Auxiliares, patches binários e lacunas de proveniência

O importador BlueWake possui fonte modificado: a revisão do auxiliar identifica mudanças de validação/identidade, limites de alocação e nomes REL. Isso é alteração de um extrator, não implementação do motor do jogo. Os wrappers GT4 e King's Field chamam rotinas de importação oficiais; King's Field usa o perfil japonês com tradução inglesa opcional ausente.

As árvores Torch preservadas de Lighthouse, Spaghetti, PaperBoat, Ghostship e Starship foram comparadas com seus respectivos arquivos-fonte originais preservados. Não apareceram diferenças nessas comparações. O arquivo de pesquisa `lighthouse-cli.patch` contém patches upstream; sua existência não demonstra aplicação ao jogo instalado.

**SoH permanece uma lacuna específica:** há registro de correção em `SohTorch::Extract`, mas não foi localizado o par de fontes antes/depois que corresponde ao executável reaproveitado. O hash do binário prova sua identidade, não a natureza de todas as modificações que ele contém. Não se emite um atestado de fonte intacto para esse auxiliar.

No Mega Man Legends Modernization, os patches binários US/JP foram comparados ao manifesto oficial fixado: para cada região, 121 ranges, 247 bytes de alteração e cauda de 512 bytes, com offsets, conteúdos, tamanhos e hashes coincidentes. Eles não foram criados para terminar a decompilação PS1. Fonte: [comparação MML](mml-parity-review.json). A decompilação `mml1-megaman-legends-decomp` é outro ID, sem receita.

O [relatório específico de auxiliares](native-helpers-review.md) registra 13 achados com caminhos, comparações e limites restantes. O mesmo auxiliar Picori também atende AutoTMC. Nenhum auxiliar binário foi recompilado nesta auditoria; a correspondência exata fonte→executável não deve ser inferida apenas de um `ORIGIN` ou SHA-256.

No Sonic Unleashed, foram examinados os 87 arquivos do pacote de fontes do auxiliar. Seis fontes centrais foram comparados novamente com as revisões upstream e coincidem byte a byte; o wrapper chama o patcher original para aplicar o title update e criar um novo XEX. Isso sustenta a atribuição do patch, sem provar reprodução do executável. Ver [evidência Unleashed](unleashed-helper-review.json) e [demais achados dos handlers](handler-findings.md).

## 6. Fixtures sintéticas: o que provam e onde aparecem

Foram encontradas fixtures reais e stubs de teste. Não foram omitidos da análise:

| Caso | Conteúdo sintético | Caminho e limite da prova |
|---|---|---|
| Pinyon | DLLs com nomes das fachadas do jogo e função retornando `0x27` | `PinyonPreflight`/teste; produção gera os três módulos reais. Prova de carga/nomes/ABI |
| LAS | Tabelas vazias de funções para main/sdk | Fixtures chamadas pelos testes; preparação exige módulos originais e codegen real |
| Odyssey | DLL simples de retorno fixo e NSO/RomFS autorais | Provas de infraestrutura; não são a DLL gerada da mídia |
| GT5/Burnout | ELF e callback smoke, probe host | `ConsoleBuildPreflight`; produção usa módulos e geração oficiais |
| PS4/Switch | ELF/SFO/NSO autorais fixados por hash | Testes fechados de geração/runtime; não demonstram boot comercial |
| Mario | ROM sintética de hash incorreto | O teste exige rejeição e não deve produzir executável do jogo |
| Strikers GC | Executável diagnóstico que cria uma instância WebGPU | Também executado durante preparação real; não é o launch_file nem uma implementação do jogo |

Os consumidores estão listados em `root-review.json`; os testes em `Tests/AddonInfrastructure` são excluídos do projeto principal pelo `.csproj`. Métodos auxiliares internos ainda podem existir na assembly; a conclusão de separação depende dos call sites e do fluxo de produção, não apenas da pasta `Tests`.

Um teste desses pode ser válido para seu objetivo e insuficiente para a alegação “o jogo executou”. **O erro é converter evidência limitada em homologação do jogo.** A transação `RunPreparedBuildTransaction` valida o executável/contrato e o manifesto e então grava `Completed`/`Verified`; não executa uma partida. Fonte: [transação de conclusão](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationPreparedBuildTransaction.cs).

## 7. Catálogo, duplicidades e seis IDs sem receita

| ID/projeto sem receita | Problema registrado |
|---|---|
| Courage Reborn | Código/pacote oficial necessário não obtido; launcher não confirmado |
| Project 2099 | Instalador público não basta para provar runtime completo disponível ou fluxo de mídia; não há base para afirmar que é só apertar instalar |
| `doldecomp-mkdd-decompilacao-base` | Decompilação GameCube, distinta dos dois ports MKDD efetivamente integrados |
| `tmc-decompilacao-base` | Decompilação GBA, distinta de Picori |
| `mml1-megaman-legends-decomp` | Decompilação PS1, distinta do Modernization Project |
| `wind-waker-recomp` | Relação de sucessão/duplicidade com BlueWake; não deve criar outra promessa de port Windows |

São seis IDs, não sete. Além dos três aliases de receita que levam 142 IDs a 145 receitas, o catálogo mantém o ID combinado/depreciado Sonic 1 Forever + Sonic 2 Absolute juntamente com os dois separados. AutoTMC utiliza Picori já catalogado. Essas situações precisam de política de catálogo, e não de trabalho para terminar os jogos. Ver [inventário integral](catalog-review.md).

Também há uma inconsistência estática: FH1 tem rota de conclusão, mas seu perfil não entra em `CanCompletePreparation`; `AutomationRank` o classifica de outra forma. Isso não foi extrapolado para uma afirmação de botão quebrado sem seguir a UI completa.

Nenhum item foi removido ou corrigido nesta auditoria.

## 8. Decisões sustentadas pela auditoria

1. **Não tratar a variante MKW personalizada como simples instalação oficial.** Ela contém implementação própria de funcionalidade do compilador e precisa de decisão explícita de escopo antes de continuar como variante AllFix.
2. **Declarar e revisar as mudanças de runtime/configuração.** GOW, FH1/Pinyon/SSX e SM64Plus não são cópias comportamentalmente intactas. Restaurar opções ou delegar ao launcher oficial são trabalhos posteriores, não resultados já feitos aqui.
3. **Manter preparação, compilação, boot e jogabilidade como evidências distintas.** Nenhum número global de receitas substitui prova por jogo. A existência de um launcher tampouco prova que seu runtime privado foi obtido.
4. **Resolver duplicidades e decompilações sem port na política de catálogo.** Não é apropriado implementar partes faltantes para satisfazer uma meta numérica de IDs.
5. **Não emitir garantia sobre o auxiliar SoH sem recuperar seu fonte/diff correspondente.** O limite concreto fica preservado, junto às demais fronteiras fonte→binário.

## 9. Limites e reprodução

Esta é uma auditoria completa do inventário e dos caminhos da integração fixada, com inspeção dos deltas e verificação de proveniência especificadas em cada relatório. **Não é revisão de todas as linhas de todos os repositórios upstream; não é auditoria de todo estado histórico transitório; não é reconstrução de todos os executáveis; não é teste de gameplay.** Os 97 históricos do índice foram usados para status, não como substituto de revisão do histórico inteiro do Desktop.

Os scripts `catalog_inventory.py`, `service_routing_inventory.py`, `snapshot-source.py` e `replay-rex-provenance.py` preservam os procedimentos de inventário/snapshot/comparação. Os JSONs mantêm contratos, commits, árvores, hashes e diffs. O consolidado `audit-matrix.json` e `MATRIZ-148.md` relaciona cada um dos 148 IDs à cobertura e aos achados. `verify-audit.py` confere a consistência dos entregáveis sem compilar jogos.

Foram reutilizados caches e fontes existentes. Nenhuma ROM, ISO, mídia original ou dependência ativa foi apagada. Arquivos base64 de transferência gerados exclusivamente para esta auditoria foram removidos somente após a evidência decodificada ser preservada. Não foram criadas compilações intermediárias ou gigabytes de mídias/provas binárias.
