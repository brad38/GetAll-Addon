# Continuidade de implementação — SDK 1.5.67

## Estado confirmado em 27/11/2026

O checkpoint do Bradsson registra **136 de 148 projetos com fluxo integral
implementado**, vinte e dois a mais que os 114 do SDK 1.5.66. Há um homologado histórico
e 135 integrais aguardando mídia original; 3 parciais, dois adiados pelo usuário
e sete sem receita. A contagem é calculada sobre as 148 linhas únicas da matriz.

O índice desta branch contém **143 receitas para 141 projetos**: uma entrada
`validated` histórica e 142 experimentais. Dr. Mario recebeu a nova receita e
fechou a preparação automática. Nenhuma das novas receitas foi homologada.

O Desktop `6548ce01ed45949effe09c00848317a90f3e53a7` está na PR3 draft,
com CI Windows `46041444134` aprovado (testes, parser, JavaScript, build Release
e publish win-x64). GetAll `9caef66df45682079656ddb6af5421ac1058c344` está na
PR20 draft, CI `46040722683` aprovado. A prévia anterior e as bases permanecem
preservadas. A nova prévia está em fechamento; nenhum merge ou release ocorreu.

## Vinte e dois fluxos concluídos tecnicamente

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

Os três Mario compartilham 57 checks de política/transação/lançamento. Os três
preflights oficiais passaram. Nenhuma ROM ou função comercial foi inventada.

WipEout aceita a faixa BIN 1 original americana ou pasta PSX, mais uma pasta
com os arquivos PC `leeg.cmp`, `leeg.prm`, `msdos.cmp` e `msdos.prm`. A importação
descobre os arquivos sem presumir caminhos em instaladores PC. Uma pasta
combinada ou ISO preparada anteriormente continua aceita.

Dr. Mario ainda exige a ROM original para gerar funções/RSP, ligar o jogo e
comprovar boot. Os testes públicos de runtime/interface e ferramentas não
substituem essa etapa. A mesma distinção vale para todos os fluxos acima.

## Implementações seguintes — fora da soma

SDKs Pinyon/FH1 estão em verificação. Odyssey/LAS já tinham automação; a conclusão acima reflete
o fechamento da prova nativa e a integração dos helpers comuns de produção.
As entradas com estas alterações exigem SDK 1.5.67 no índice; os textos
antigos seguem reconhecidos, e as novas instruções são comparadas exatamente.

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
- `flow-completion-20261127/work-progress-136.json` e
  `checkpoint-backups-136`: contagem e preservação do checkpoint anterior.
- `flow-completion-20261127/getall-parser14.json`: 143 receitas aceitas pelo
  parser do build 14, incluindo as instruções atualizadas DOAX/Burnout.

Os arquivos `CONTINUIDADE.md`, `PENDENCIAS.md` e `MATRIZ-FUNCIONAL.md` do workspace
foram atualizados para 136/148. Árvores históricas e mídia permanecem intactas.
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
