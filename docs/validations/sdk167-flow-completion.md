# Continuidade de implementação — SDK 1.5.67 → 1.5.68

## Estado confirmado em 27/11/2026

O checkpoint do Bradsson registra **140 de 148 projetos com fluxo integral
implementado**, vinte e seis a mais que os 114 do SDK 1.5.66. Há um homologado histórico
e 139 integrais aguardando mídia original; um parcial e sete sem receita.
As duas retomadas anteriormente adiadas foram concluídas. A contagem é calculada sobre as 148 linhas únicas da matriz.

O índice desta branch contém **143 receitas para 141 projetos**: uma entrada
`validated` histórica e 142 experimentais. Dr. Mario recebeu a nova receita e
fechou a preparação automática. Nenhuma das novas receitas foi homologada.

O Desktop `6548ce01ed45949effe09c00848317a90f3e53a7` está na PR3 draft,
com CI Windows `46041444134` aprovado (testes, parser, JavaScript, build Release
e publish win-x64). GetAll `9caef66df45682079656ddb6af5421ac1058c344` está na
PR20 draft, CI `46040722683` aprovado. A prévia anterior e as bases permanecem
preservadas. A prévia de 138 projetos está pronta; nenhum merge ou release ocorreu.

O fechamento de 138 está local: Desktop `02d7c4b` e GetAll `c1ee000`,
seguidos do SotC no Desktop `c39ac77787893c2fb77e9dda48593ec266b11503` e
do fechamento Savage Wind comprovado no BUILD29b. A revisão automática recusou o envio
seguinte ao GitHub e exige autorização direta para os destinos e conteúdo
exatos. As verificações abaixo são locais; os CIs citados acima pertencem
aos commits publicados anteriores.

BUILD30 SDK 1.5.68 terminou com **zero erros e zero avisos em 12,25 s**.
A regressão completa aprovou **1.866 verificações, sem falhas, em 13,515 s**.
O parser30 aceitou **143/143 receitas** do snapshot final em 11,547 s.
Os 60 testes Python passaram em 2,141 s; a validação estrita também
conferiu os 143 documentos, JSON Schema, hashes, LF e catálogo fixado.
O BUILD28 anterior havia aprovado 1.820 verificações e ambos os índices,
publicado e atualizado, com 143/0; esse histórico permanece preservado.

A prévia de 138 usa a compilação anterior: BUILD27b terminou com **zero erros e zero avisos em 9,32 s**. A regressão
teve **1.787 PASS, zero falhas em 13,531 s**. O parser C# aprovou **143/143**
receitas tanto no commit publicado `9caef66` quanto no snapshot atualizado.
Assim, a prévia SDK 1.5.67 pode usar o índice já publicado sem depender de
um SHA ainda indisponível no GitHub. Os novos textos e hashes permanecem
prontos para o envio posterior. A nova receita SotC v9 também está local e
dependerá da publicação do GetAll para ser obtida pelo catálogo remoto.

O candidato final usa SDK **1.5.68**, e o índice exige esse mínimo para
SotC e Savage Wind. A prévia138/SDK 1.5.67 já existente não contém o perfil
SotC, portanto anunciar o mesmo mínimo permitiria uma combinação de
catálogo e Desktop incompatível. As provas nativas28/29b continuam válidas
para o código de preparação; a compilação final30 confirmou a identidade
1.5.68 e o catálogo atualizado. Nenhum pacote histórico foi sobrescrito.

### Prévia Windows verificada de 138 projetos

`C:\Users\bradg\Downloads\GetAll-R18\publish-getall-complete-flows-20261127`
contém Desktop 3.0.0, SDK 1.5.67 e GetAll 1.5.72. O addon aponta para
`9caef66df45682079656ddb6af5421ac1058c344`, já publicado. A auditoria verificou
34 recursos incorporados, 66 avisos de licença e 74 arquivos. O verificador
final aprovou o commit, as versões, os hashes e a separação da prévia antiga.

| Artefato | Bytes | SHA-256 |
|---|---:|---|
| `AllFix.exe` | 157.358.350 | `0e37aae27082f5eda7aa76f43985d5be52c5e0c63f03b084ce4812eaddc022e1` |
| `GetAll-Preview.zip` | 879 | `7d22572b5736391b52c0cf5ba424bf3ea6c9a63a46c4cdc25c78ddd414aaa36b` |
| `ARTIFACT-MANIFEST.json` | 14.073 | `0f2db05e027d27732451a4d1f29fffb0fb7b868f82c1c9fd23c00c9b329c8e96` |

Os recibos estão em `evidence-r18/complete-flows-publish-20261127`, incluindo
`local-preview-final-result.json` e
`run-20261127T190214Z-0467ae01/publication-checkpoint.json`. A prévia anterior
SDK 1.5.66 foi mantida. SotC e Savage Wind ainda não fazem parte dessa prévia.

## Vinte e seis fluxos concluídos tecnicamente

| Projeto | Fluxo implementado ou reforçado | Verificação executada |
|---|---|---|
| `sm64ex` | MSYS2/UCRT64 privado substitui Docker/MXE; ROM, extração, compilação, publicação e Jogar integrados. | Fonte oficial, ferramentas upstream compiladas, loader SDL e rejeição da ROM sintética. |
| `render96ex` | Compilação Windows privada e integração com os packs opcionais existentes. | Fonte oficial e ferramentas reais, loader SDL, políticas de publicação e lançamento. |
| `sm64rt` | Perfil RT64/SDL2 corrigido, SDL2/GLEW fixados e runtime Microsoft app-local. | Ferramentas oficiais, probe SDL/GLEW e dependências PE inspecionadas. |
| `strikers-wiicompiled` | SDK .NET 8.0.425, YamlDotNet 15.1.2 e runtime privados; FST completo e mídia validados. | 38 verificações de fluxo, quatro do tradutor oficial e três do decoder nodtool. |
| `wipeout-rewrite` | UCRT64 privado; composição dos dados PSX e quatro arquivos PC; revalidação no lançamento. | 13 verificações de composição, build nativo e 11 da transação real Run/Resume/registro/Jogar; mídia sintética, sem executar jogo. |
| `drmario64-recomp` | ROM US antes do consentimento; 38 fontes, Python/wheels, LLVM MIPS e LLVM-MinGW privados; 12 adaptações verificadas; geração, build, registro e Jogar. | 52 checks e SourceTools4 de produção: Python, DXC, Clang, sete produtos MIPS e nove avisos. RT64 D3D12/Vulkan, runtime N64 e interface pública compilados e ligados. |
| `mariokartdd-recomp` | LLVM-MinGW UCRT substitui gate MSVC; SDL2/C++ estáticos, ISO GM4E01, build e registro integrados. | Runtime completo e runtime_check da fonte oficial; probe no mesmo CMake executa SDL, threads e exceções C++20 sob PATH Windows, sem compilador global. |
| `burnout3-recomp` | LLVM-MinGW/Ninja privados no ramo Xbox; mídia, geração/build, staging, registro e lançamento integrados. | Oito bibliotecas do runtime e quatro testes D3D8 reais, incluindo DXGI Present. Fluxo de produção e 16 checks de ISO, adaptação, cancelamento e contratos PE aprovados. |
| `strikersrecomp` | ISO G4QE01 Rev0 completa; DolRecomp, GXRuntime compatível, SDL3/Dawn/CRT privados; mídia/launch revalidados. | Prova de produção: 463 etapas de host/renderer, EXE + oito DLLs + 37 avisos. WebGPU C cria/libera Dawn com TimedWaitAny; host executa bloco PowerPC próprio, retorna ao sentinel, gap-report 0/0. |
| `mkdd-recomp` (Rust) | Rust gnullvm, LLVM-MinGW, JDK/Ghidra e GameCubeLoader privados, sem diálogo de mapa no modo headless; geração/build/registro/launch. | Dependências oficiais Bevy/CPAL/WGPU compiladas/linkadas/executadas, Cargo.lock preservado. Ghidra real: 15 checks, loader oficial, decompilação nativa, p-code/tabelas, caminho com espaços e home privado. |
| `doaxvb-re` | Dependências CMake e DXC/CRT privados; RTGI solicitado exige shaders presentes; notices e import closure publicados. | Produção: 189 etapas, quatro executáveis de runtime/D3D11/Vulkan/RTGI ligados; seis arquivos de shaders verificados e runtime público executado, exit 0 em 106,92 s. |
| `god-of-war-recomp` | ISO US validada antes do consentimento, duas camadas preservadas, compiladores/dependências privados, pipeline interpretado upstream e ELF no lançamento. | BUILD15: 44 checks e Native com 55 patches, recompiler/host públicos ligados e executados; consumidor C++ leu todos os 608 setores da fixture, inclusive camada2/padding. Exit 0 em 216,18 s. |
| `super-odyssey-pc-recomp` | Automação existente refatorada para que a preparação real e a prova usem o mesmo helper de compilação. Instruções de Retomar alinhadas. | BUILD16: sete checks; geradores oficiais main/sdk/subsdk0 com NSO próprio, jump table real, seis unidades + gamelib_entry.c oficiais compilados e DLL/ABI verificados. MovieData preservada. Gate comercial rejeita a identidade própria. |
| `lasrecomp` | Automação existente refatorada em BuildLasLibrary comum; instruções de Retomar alinhadas. | BUILD17: quatro checks; gerador SDK oficial e jump table própria, quatro objetos/DLL/ABI ligados. O gerador main rejeitou corretamente o build ID próprio; patches e main comercial aguardam original. |
| `god-of-war-native-pc-port-gow-pc-port` | ISO/CHD US validada antes das ferramentas; extração preserva as duas camadas e padding; intérpretes upstream quando os manifestos não se aplicam; compilador/CRT privados e ELF no lançamento. | BUILD18: 21 checks de política + 12 engine/native; runtime/UI compilados, host público sem mídia encerrou como esperado e DiscSource C++ leu todos os setores. BUILD19: oito checks de helpers, três DLLs Microsoft por hash e duas licenças; PATH apenas System32. |
| `totk-pc-recomp` | Automação existente usa runner Python privado comum; extração/patches/cache/build/registro/Jogar preservados. | BUILD19: sete checks, 22,65 s; geradores oficiais main/sdk com NSO próprio, libtotkrt.a fixada, selftest de memória/dispatch, RomFS próprio, DLLs isoladas e shader Maxwell → SPIR-V. |
| `dkb-pc-recomp` | Automação existente usa o mesmo runner privado; mantém NUP ou ExeFS/RomFS, extração/patches/build/registro/Jogar. | BUILD19: oito checks, 69,58 s; 151 objetos de runtime + código próprio, selftest, probe NVN2 oficial com seis checks e tradução de shader próprio para SPIR-V. |
| `gt5-recomp` | Compilador LLVM-MinGW, CMake/Ninja/MinGit/Python privados; mantém disco/ELF/SELF/PUP, PPU/SPU, D3D12/ImGui, FFmpeg, transação e Jogar. | BUILD20 compilou 200 etapas do alvo real com programa público próprio. BUILD21 verificou imports, três ABI FFmpeg, 11 marcadores e três presents D3D12; loader/finder/lifter geraram e compilaram dois C++ de PowerPC próprio. Gate comercial rejeitou a fixture. BigObj 65.545 seções e CodeView/PDB/delay-load preservados. |
| `rygt-gt7` | Conversor PS4 oficial com dois módulos originais, nomes `.guest.prx` corrigidos, validação, publicação e Jogar. | BUILD22: seis checks em 1,74 s; pin/cópia do kit, recusa de fixture alterada, conversão com `--verify`, PE e dois PRXs próprios. Execução pelo worker real chamou dois exports próprios (37/42) e saiu 0; sem identidade comercial. |
| `spartanport` | Preparação PS4 pelo CLI oficial, saída validada, publicação, registro e Jogar; instruções corrigidas para a automação existente. | BUILD23: nove checks em 2,73 s; kit459/pin, três layouts G3PROBE/content próprios, trailer recusado, host real chama exports37/42 e sai por libc exit(0); Vulkan submission/readback de4.096B. SFO sem ID comercial. |
| `ssx-recomp` | ISO/pasta EA-2413 e TU STFS opcional; SDK e compilador privados, D3D12/Vulkan/FidelityFX, geração/build, cache verificado, registro e Jogar. | BUILD22: rota real prepara SDK do zero, configura fonte oficial, compila 14 objetos públicos disco/TU, verifica nove DLLs + EXE e executa consumidor D3D12/WIC com ambiente isolado. 70 checks de política/cache/extração/transação. |
| `gta-stories-recompiled` | ISOs LCS/VCS validadas antes do consentimento; ferramentas privadas, codegen/build individual ou combinado, host/DLLs oneproc na ordem e caminhos corretos, packs e Jogar. | 42 checks de política + 72 nativos BUILD22: runtime/app LTO, 29 imports, DLL LCS real/export, host e Python privado. BUILD24: cinco contratos de dispatcher e launcher até Popen em 0,383 s. Sem entrada de jogo executada. |
| `fh1-reimagined` | ISO, Games on Demand ou pasta Xbox 360; ReIGlue e LLVM-MinGW privados, três módulos, recursos Windows e entry points Unicode, build, runtime, registro e Jogar. | BUILD27b: Policy9 e Native22 aprovados; SDK completo compilado do zero pelo provider em 503,188 s, 20 adaptações/16 links fixados, 11 DLLs, avisos, recibos, rejeição de corrupção/cancelamento e consumidor C++/D3D12 em caminho Unicode. DLSS real e 128 fontes públicas do host comprovados separadamente. |
| `pinyon-shift` | ISO/pasta USA MS-2505, TU v4 opcional, SDK/compilador privados, geração e cache verificados, build, registro e Jogar; preserva renderers e DLSS. | BUILD27b: Policy19 e provider completo em pasta nova aprovados; 1.021 etapas de SDK, 78 objetos públicos do host, nove DLLs, extrator, D3D11/D3D12/Vulkan, DLSS real com leitura de imagem e wrapper oficial wWinMain com fachadas, Unicode e cleanup. |
| `shadow-of-the-colossus-pc` | Pasta PS4 EU 1.01/US 1.00 validada, cinco scripts oficiais no kit fixado, transação privada, recibo e Jogar com revalidação; preserva mídia e configuração anterior. | BUILD28: Policy33 e Native23 aprovados em 0,187 s e 22,86 s. Run v5→v9, cancelamento, Resume real, cinco CLIs, bb-probe negativo e wrapper oficial até fronteira interceptada; ELF/SELF/SFO autorais, sem boot comercial. |
| `savagewindrecomp` | Perfil interno ligado ao recibo/ZIP exatos; valida ExeFS/RomFS 1.9.0, copia dados, gera main/subsdk0/sdk, compila com Zig privado, verifica ABI, publica, registra, recupera o kit e permite Jogar. | BUILD29b: Policy46 e Native26 aprovados em 0,156 s e 13,219 s. Pacote136, URLs oficiais, migração por novo destino, rollback/falha de registro, swgen real com três jump tables autorais e biblioteca AMD64 ligada. Sem boot comercial. |

Os três Mario compartilham 57 checks de política/transação/lançamento. Os três
preflights oficiais passaram. Nenhuma ROM ou função comercial foi inventada.

WipEout aceita a faixa BIN 1 original americana ou pasta PSX, mais uma pasta
com os arquivos PC `leeg.cmp`, `leeg.prm`, `msdos.cmp` e `msdos.prm`. A importação
descobre os arquivos sem presumir caminhos em instaladores PC. Uma pasta
combinada ou ISO preparada anteriormente continua aceita.

Dr. Mario ainda exige a ROM original para gerar funções/RSP, ligar o jogo e
comprovar boot. Os testes públicos de runtime/interface e ferramentas não
substituem essa etapa. A mesma distinção vale para todos os fluxos acima.

## Conclusão das duas retomadas

SotC fechou o checkpoint139 e Savage Wind fechou o checkpoint140, ambos após
provas nativas. O histórico de adiamento foi preservado; não é tratado como
exclusão permanente. Os oito projetos fora da soma estão discriminados no
final deste relatório. Odyssey/LAS já tinham automação; sua conclusão nesta
rodada reflete a prova nativa e a integração dos helpers comuns de produção.
As entradas anteriores desta rodada exigem SDK 1.5.67; SotC/Savage exigem
1.5.68 para separar suas capacidades da prévia138 existente.

## Evidências no Bradsson

Raiz: `C:\Users\bradg\Downloads\GetAll-R18\evidence-r18`.

- `flow-completion-20261127/mario-native-tests/round3`: três preflights Mario.
- `complete-install-flows-20261127/wii-policy-38.log`, `wii-translator2.log`
  e `wii-decoder.log`: fluxo Wii, tradutor e decoder.
- `flow-completion-20261127/wipeout-installed-7.log`: transação real com
  compilação oficial e mídia sintética, 11 checks, exit 0 em 70,09 s.
- `drmario-desktop-flow-20261127/drmario-source-tools-4.log` e
  `production-evidence-inventory.json`: SourceTools4, exit 0 em 72,06 s;
  inventário de dez fontes/testes, 14 recursos e nove avisos.
- `complete-install-flows-20261127/mkdd-official-final.log`: runtime e
  integração C++/SDL, exit 0 em 130,52 s.
- `flow-completion-20261127/burnout-native/engine-round1.log`: fluxo nativo
  de produção e 16 checks, exit 0 em 54,60 s.
- `flow-completion-20261127/regression-14.log`: **1.661 PASS, zero falhas**;
  build 14 sem erros ou avisos e parser 14 com 143/0.
- `flow-completion-20261127/work-progress-140.json` e
  `checkpoint-backups-140`: contagem e preservação do checkpoint anterior.
- `flow-completion-20261127/getall-parser14.json`: 143 receitas aceitas pelo
  parser do build 14, incluindo as instruções atualizadas DOAX/Burnout.

Os arquivos `CONTINUIDADE.md`, `PENDENCIAS.md` e `MATRIZ-FUNCIONAL.md` do workspace
foram atualizados para 140/148. Árvores históricas e mídia permanecem intactas.
A fila continua com contagens novas somente após a prova do fluxo correspondente.

Provas seguintes: `complete-install-flows-20261127/strikers-gc-official-final.log`
(exit 0, 221,19 s), `flow-completion-20261127/mkdd-ghidra/round2-final.log`
(exit 0, 35,13 s) e `flow-completion-20261127/doax-official-12b.log`
(exit 0, 106,92 s). Os testes usam código público e fixtures próprias; não houve
primeiro boot comercial. No GC, a extensão diagnóstica C++ opcional do Dawn e
Tracy não são usados no MinGW; renderer, callbacks de device e toggles seguem
ativos. O GetAll `31cfa7c` foi enviado na PR20 draft e passou no CI `46032725114`.

GOW KI: `gow-kiexster-mingw-20261127/policy-build15.log`, `native-build15.log`
e `production-evidence-inventory.json`: 44 checks, 37 avisos e 19 evidências.
Rust crates: `flow-completion-20261127/rust-game-source/round1/crate-notices-build15.log`,
12 checks e 364 crates verificadas contra Cargo.lock antes da publicação dos avisos.

Switch: `complete-install-flows-20261127/odyssey-generator-final.log` (BUILD16,
sete PASS, 5,66 s) e `las-generator-final.log` (BUILD17, quatro PASS, 2,58 s).
Os dois builds C# encerraram sem erros ou avisos. As fixtures usam identidade
própria; não há mídia comercial, boot de jogo ou promoção para `validated`.

GOW 0.4.0: `gow-native-completion-20261127/policy-build18.log`,
`native-build18.log` (173,25 s) e `runtime-build19.log` (0,87 s).
DKB/TotK: `flow-completion-20261127/dkb-native-final.log` e
`totk-native-final.log`. Os dois passam pela DLL19 de produção; compilação e
boot comerciais continuam pendentes. A regressão conjunta19 teve **1.689 PASS**;
parser18 aprovou 143/143 receitas do GetAll `b759f69`, cujo CI `46038014110` passou.

GT5: `gt5-native-20261127/production run2/preflight/compile-link.log`
comprova o build público integral de runtime/host/interface; `products-build21b.log`
e `production run2/preflight/native-proof.json` registram a etapa final aprovada.
O executável tem 4.841.984 bytes e o staging inclui três FFmpeg e oito avisos
(mais os avisos de projeto/toolkit copiados pelo caminho de instalação).
A fixture de D3D12 deriva da pública upstream e espera cada apresentação antes
de enviar o quadro seguinte; mantém todas as 11 asserções e a exigência de três
presents. A alteração é restrita ao teste. Não houve primeiro boot comercial.
As falhas anteriores de lista de DLLs Windows e log já existente estão preservadas;
a validação final usa os mesmos objetos nativos compilados, sem os recompilar.
Parser21: 143/143 no GetAll `9caef66`, CI `46040722683` aprovado.

RyGT: `flow-completion-20261127/rygt-native-final.log` e `rygt-native-final`. A prova chama o mesmo helper de conversão da instalação. A regressão22 completa passou com **1.745 PASS**, build C# sem erros ou avisos. GT5 também tem `README.md` e inventário com quatro fontes, 27 evidências, cinco binários e oito avisos em `gt5-native-20261127`.

Spartan: `flow-completion-20261127/spartan-native-final.log` e `spartan-native-final`. BUILD23 sem erros ou avisos. O fluxo já estava automatizado; a nova evidência fecha a preparação e execução públicas pelo helper real, sem fornecimento de jogo, ID comercial ou promoção da receita.

SSX: `flow-completion-20261127/rex-native-source/ssx-production-build22.log` termina em `SSX_PREFLIGHT_PASS`; a árvore `engine22` guarda a preparação real. GTA: `gta-stories-completion-20261127/native-build22.log`, `launch-contracts-build24.log`, README e inventário com sete fontes, 32 evidências, 31 produtos públicos e 38 avisos/documentos. A fixture Python corrigiu apenas `quick=False`; os objetos C++ não foram recompilados. BUILD24: zero erros/avisos. Nenhum dos dois casos comprovou boot comercial.

## Refinamentos de fluxos já incluídos na contagem

CTR Turbocharged, SM e SM Rewrite agora usam o compilador privado também na
preparação nativa. A exigência de Visual Studio global foi removida dos três
caminhos, preservando a arquitetura i686 do CTR e x64 dos dois SM, SDL2 2.26.3
fixada, os GUIDs oficiais e as chamadas COM. BUILD26 terminou com zero erros e
avisos. A política teve **14 PASS**; os três builds pelo motor real tiveram
**46 PASS em 249,469 s**, incluindo loader, dependências, avisos, entradas
inválidas e a transação de CTR com dados autorais. Isso melhora três projetos
já contados, sem aumentar artificialmente a cobertura.

Evidência: `ctr-sm-private-toolchains-20261127/README.md`,
`production-results.json` e `production-evidence-inventory.json`: sete fontes,
35 evidências, cinco produtos PE e 38 avisos.

O SDK SSX recebeu a correção do caminho real do executável para MinGW. O
getter usa `GetModuleFileNameW` e foi recompilado na árvore de produção
`engine22`. `ssx-executable-path-loader2.log` comprova o caminho com espaços e
acento, além de WIC, D3D12 e carregamento do plugin. O suporte incorporado
atual tem **601.221 bytes**, SHA-256
`054ae3be11679a61050033ccae491883c10b223c40fdd4a96512859b4e23715a`.
As provas e o recurso anteriores permanecem no histórico.

## Provas públicas FH1 anteriores à integração final

`fh1-native-20261127/README.md` e `prototype-evidence-inventory.json` registram
125 arquivos de fontes, produtos, pedidos e logs. O SDK ReIGlue fixado foi
compilado com LLVM-MinGW privado, preservando D3D12, Vulkan, FidelityFX, FSR3,
DLSS e Tracy. Foram compiladas 128 unidades públicas do host; o consumidor
C++ exercitou FILE*/FileHandle, caminho Unicode, carregamento do renderer e
D3D12. Os testes upstream de `forza-texcompress` passaram.

`ngx-probe-loader1.log` comprova 64 ciclos de parâmetros opacos e capacidade
SR na GPU. `ngx-dispatch-loader1.log` comprova OptimalSettings, criação EXT1,
avaliação, submissão e leitura de imagem autoral: 640 × 360 para 1280 × 720,
RGBA 0.200073, 0.399902, 0.595215, 1.000000. O wrapper Windows `wWinMain` e os
recursos oficiais de ícone/DPI também foram ligados e executados. Nenhuma
dessas provas gerou funções comerciais ou comprovou primeiro boot do jogo.

O inventário tem SHA-256
`41fdc9f2f8c1f64ddaa0dc5c88de7523f4ae5dc3f4f55afb6c129f292e27ec5e`.
A ponte NGX é específica do SDK FH1 e tem SHA-256
`548976161a6793bdd847f51d3b151902cfe667fa83213bb5c04af34515c7dd58`.

## MKW: entrada externa ainda necessária

O projeto `mkw-recomp` permanece parcial. A especificação global SM86
`instructions.json` é independente da mídia do jogo. O produtor de `v0.1.18`
e do `main` consultado exige captura de dados internos do `nvdisasm`, fora
do escopo autorizado. A saída pública `nvdisasm -json` descreve funções
disassembladas e não fornece as classes, opcodes e tabelas de bits exigidas
pelo decoder atual.

Para pedir somente a mídia original, falta uma especificação compatível com
procedência e distribuição verificáveis, ou um produtor/decoder público que
dispense essa captura. O fluxo atual continua aceitando uma especificação
local legítima como entrada adicional; essa dependência mantém sua
classificação parcial.

Evidência: `mkw-sm86-contract-20261127/README.md`, `source-provenance.json`,
`review-result.json`, `checkpoint-list-extract.txt` e inventário de 23 arquivos.
O inventário tem SHA-256
`c60d36901bced30a13bbdfe4214f37a315637ee494e9b0e1be811b83e95774cb`.
A revisão não alterou o motor MKW nem as contagens.

FH1: `fh1-native-20261127/production-policy27.log` (9 PASS, 0,125 s) e
`production-native27.log` (22 PASS, 503,188 s) encerraram com exit 0 e
`FH1_PRIVATE_SDK_PRODUCTION_PASS`. A árvore `fh1-production-27` foi criada
do zero pelo provider C# de produção. Os dois CMake do jogo reproduziram os
hashes esperados; o SDK compilado, a publicação das 11 DLLs e o consumidor
nativo passaram sem usar o runtime C++ MSVC anterior. Apenas OpenXR de ABI C
foi reaproveitado por hash. O checkpoint137 preserva 148 IDs e a matriz
anterior; nenhum primeiro boot comercial foi acrescentado.

Pinyon: `flow-completion-20261127/rex-native-source/pinyon-production27.log`
e `.exit` registram exit 0 e `PINYON_PREFLIGHT_PASS`. A pasta nova
`pinyon-production27/preflight` contém os logs de SDK, instalação, imports,
versão, host, renderer e entry point. `renderer-loader.log` executa os três
renderizadores e DLSS; `entry-loader.log` verifica o wrapper Windows oficial
e as fachadas. A política teve 19/19 PASS e a preparação rejeitou mídia
inválida com rollback. O suporte incorporado tem 175.161 bytes e SHA-256
`cc77d46b575da64c3c66e50d5306cd4e12c9cd45f2dc42738b09e614367bcfc6`.
O checkpoint138 acrescenta apenas Pinyon após o checkpoint137 de FH1.

## Shadow of the Colossus — fechamento139

O perfil `sotc-0.77-prepare` fixa o pacote oficial v0.77 de
`AjncSystem/ShadowOfTheColossus-PC`: 155.228.419 bytes, SHA-256
`79f6f4be4a6829b7141c8f1e8047863114c105603d5ed167d4c5e87bd520e7c1`.
O manifesto inclui 1.194 arquivos, 329.006.019 bytes, SHA-256
`622f35ae1964b01da1bb1d4ff92ce3cd74a9a2bf502318a181cf1f5374531d5c`.
A receita v9 contém 14 arquivos obrigatórios, um único diretório original
e exige SDK 1.5.68 no índice final. Seu SHA-256 é
`dd6491c1b3afe360cbeb37ff890af5a18398f100b1896b43c651bda771187854`.

O instalador confere ELF/SELF, módulos descriptografados, SFO e as verificações
públicas de versão antes do consentimento. Executa `prepare.py`,
`link_modules.py`, `content_profile.py`, `sotc_cpu.py` e `sotc_modes.py`
com o Python incluído no kit. Confere os produtos, a correspondência com a
mídia, a configuração privada, o recibo e o destino antes da publicação
transacional. A mídia fica no local original e é revalidada ao usar Jogar.

BUILD28 compilou sem erros ou avisos. Em `sotc-automatic-20261127`,
`production-policy28.json` registra 33 PASS em 0,187 s, e
`production-native28.json` registra 23 PASS em 22,86 s, ambos exit0.
O log nativo tem SHA-256
`d4df38692a66623994e0219459dedd4a9a093df02c4220a9a6ae63543f29797a`;
o de política,
`01b3df68f89847fc617dfe007ef3112a29d664a395c1bf8317f7df69664857a5`.
A execução ficou em `production-native-1`, preservada para revisão.

A prova fez a transação de um kit v5 anterior para uma instalação v9 nova,
com cancelamento e preservação da configuração antiga; executou os cinco
scripts oficiais e conferiu registro/Jogar e o wrapper original até a
fronteira de execução interceptada. O `bb-probe.exe` oficial rejeitou uma
assinatura de boot inválida. As fixtures ELF/SELF/SFO contêm dados e código
autorais e verificações de formato públicas; não contêm funções comerciais
e não representam primeiro boot do jogo.

O checkpoint139 foi aplicado preservando os 148 IDs na mesma ordem, com
uma única transição: `shadow-of-the-colossus-pc`. O arquivo
`work-progress-139.json` e o `work-progress-latest.json` têm SHA-256
`6aa99e4936f0b13740bfa7a29a7f2b8704b20d138327e369f1e03d5b414f0bfb`.
A variante `advance-checkpoint-retomadas.py` exige logs positivos, deriva
a contagem de retomadas da matriz e mantém backups; o updater e o
checkpoint138 originais permanecem intactos. A evidência detalhada e o
inventário estão em `sotc-implementation-20261127/README.md` e
`inventory-final.json`, sem duplicar os logs e produtos existentes.

## Savage Wind — fechamento140

O adaptador interno mantém a receita v5 e reconhece somente o recibo completo
de `revivedx/savagewindrecomp` v0.6.0-alpha.6: 125.936.779 bytes, SHA-256
`9bfc05217ed7e69001e02dee7ae9a6070a23b68cfbf946f23727f0767d4c28f8`.
O manifesto fixa 136 arquivos, 325.732.158 bytes e SHA-256
`96ed35491da81e791e9646e0894088d5b9d991b72d059f5c8927794c8f0d2c84`.
O asset oficial 752877473 usa `Revivedx/SavageWindRecomp` na URL. O motor
aceita essa grafia e a forma minúscula já observada no GetAll, mantendo
host, tag, nome do asset e ausência de query fechados. A fonte exata e os
18 blobs que determinam a ABI estão em `Tools/SavageWind/ORIGIN.json`.

A mídia é validada antes do consentimento e copiada para o novo destino.
A geração de `main`, `subsdk0` e `sdk`, as flags da CPU, a entrada ABI e o
link usam as ferramentas e os contratos do próprio kit. A execução direta
dos geradores pelo runner do All-Fix mantém as proteções normais de processo;
não usa a cadeia do launcher que desativa CFG para `swgen.exe`. Produtos,
layout, manifesto, dados copiados, imports/exports e ABI são conferidos
antes da publicação. Jogar usa os dados privados e ignora flags externas
salvas. Recuperar o kit altera somente o registro ativo, preservando o
produto anterior e os saves.

BUILD29b compilou sem erros ou avisos em 10,68 s. Em
`savagewind-automatic-20261127`, `production-policy29b.json` registra
46 PASS em 0,156 s e `production-native29b.json` registra 26 PASS em
13,219 s, ambos exit0. O log de política tem SHA-256
`e94f7e97571062c9ca716cde56a22222aaa55b1114212e25b5432000764728d3`;
o nativo,
`6f147d35ff70ba04b6171817f4a0389e06bcc553263589b97b18939fd312a28a`.
O BUILD29 anterior compilou corretamente, mas o helper de rejeição do teste
não capturava `InvalidDataException`; a correção29b foi restrita a esse catch.
Nenhuma validação de produção foi relaxada.

A prova usa uma NSO autoral fixada por tamanho e hash. Os três geradores
oficiais resolveram suas jump tables, e Zig vinculou a biblioteca AMD64
com a entrada ABI oficial. A opção de teste upstream `--no-sites` é
inacessível na rota de produção. O teste também percorreu Run v5, novo
destino, rejeição de estado legado/mídia incompleta, falha/cancelamento,
falha de registro após o move e recuperação do kit. O kit permaneceu
parcial nos testes: não houve fabricação de mídia, registro de jogo
comercial como pronto nem primeiro boot. A receita continua experimental.

## Oito dependências externas restantes

| Projeto | Classificação | Dependência concreta |
|---|---|---|
| `mkw-recomp` | Parcial | Modelo ISA SM86 `instructions.json` compatível, com procedência/distribuição verificáveis, ou um produtor público que dispense a captura de memória descrita na seção MKW. |
| `wind-waker-recomp` | Sem receita | Distribuição própria verificável desse ID ou decisão sobre sua identidade sucedida. BlueWake já tem cobertura independente. |
| `twilight-princess-courage-reborn` | Sem receita | Fonte/pacote oficial acessível e fixável. A documentação de build existe, mas o repositório indicado retornou 404 na auditoria registrada. |
| `metaforce` | Sem receita | Distribuição Windows oficial verificável ou fonte oficial acessível. Os endpoints de distribuição consultados estavam indisponíveis. |
| `doldecomp-mkdd-decompilacao-base` | Sem receita | Implementação Windows independente; a base auditada reconstrói o programa de console. |
| `tmc-decompilacao-base` | Sem receita | Implementação Windows independente; a base auditada é de decompilação para GBA. |
| `mml1-megaman-legends-decomp` | Sem receita | Implementação Windows independente; a base auditada é de decompilação para PS1. |
| `project-2099` | Sem receita | Pacote/contrato verificável para preparação da mídia própria e procedência dos conteúdos incluídos, especialmente Title Update. O payload não foi baixado nessa auditoria. |

As condições dos sete projetos sem receita vêm dos registros individuais em
[COBERTURA-R18](../COBERTURA-R18.md) e das fontes já consultadas na seção
histórica de [CHECKPOINT](../CHECKPOINT.md). O item histórico Dr. Mario dessa
lista foi resolvido nesta continuidade e não está entre os sete atuais.
Os 148 IDs foram preservados, assim como o bloqueio MKW; nenhuma indisponibilidade
de fonte ou ausência de port Windows foi convertida em fluxo concluído.

## Registro final de cobertura e validação

`work-progress-140.json` e `work-progress-latest.json` têm SHA-256
`cb254ea6a9da175851557fc98a0754164b05afd70dbb0137b49443325880ab14`.
O checkpoint140 mudou somente `savagewindrecomp`, preservando os 148 IDs
na mesma ordem, o checkpoint139 e os backups anteriores. Há 140 integrais,
um parcial, zero retomadas pendentes e sete sem receita. O novo updater
`advance-checkpoint-final.py` tem SHA-256
`07729737de4b2d74056301096570200c477eb1e3944da9db607bc5e9752caabf`;
os scripts anteriores foram preservados.

A etapa final30 não mudou geradores, mídia ou bibliotecas nativas. Ela
atualizou somente a identidade do SDK e o teste dessa identidade, seguida
pela regressão completa e pelo parser do snapshot com mínimo 1.5.68. Os logs
estão em `flow-completion-20261127/regression30.log` e
`parser30-next.log`, com os recibos de resultado correspondentes. O índice
final conferido tem SHA-256
`c82d450f0da6e067c80cc01141b677c950b43fbeac5c9303aededac266bcdee3`.
A compilação candidata do Desktop será registrada separadamente, depois
do commit final; seus hashes não são confundidos com os da prévia138.
