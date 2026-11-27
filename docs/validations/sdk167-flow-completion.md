# Continuidade de implementação — SDK 1.5.67

## Estado confirmado em 27/11/2026

O checkpoint do Bradsson registra **128 de 148 projetos com fluxo integral
implementado**, catorze a mais que os 114 do SDK 1.5.66. Há um homologado histórico
e 127 integrais aguardando mídia original; 11 parciais, dois adiados pelo usuário
e sete sem receita. A contagem é calculada sobre as 148 linhas únicas da matriz.

O índice desta branch contém **143 receitas para 141 projetos**: uma entrada
`validated` histórica e 142 experimentais. Dr. Mario recebeu a nova receita e
fechou a preparação automática. Nenhuma das novas receitas foi homologada.

O Desktop `7cbad7d254e4ee9d6f1600a3fbde08101279d3ab` está na PR3 draft,
com CI Windows `46035592163` aprovado (testes, parser, JavaScript, build Release
e publish win-x64). GetAll `ff21fcf06024cc0d998709436b13138074398c9c` está na
PR20 draft, CI `46034996088` aprovado. A prévia anterior e as bases permanecem
preservadas. A nova prévia está em fechamento; nenhum merge ou release ocorreu.

## Catorze fluxos concluídos tecnicamente

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

Outro God of War e GTA Stories, SDKs Pinyon/SSX, GT5 e os geradores de Switch
estão em verificação. Odyssey/LAS já tinham automação; a conclusão acima reflete
o fechamento da prova nativa e a integração dos helpers comuns de produção.
As 14 entradas fechadas nesta rodada exigem SDK 1.5.67 no índice; os textos
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
- `flow-completion-20261127/work-progress-128.json` e
  `checkpoint-backups-128`: contagem e preservação do checkpoint anterior.
- `flow-completion-20261127/getall-parser14.json`: 143 receitas aceitas pelo
  parser do build 14, incluindo as instruções atualizadas DOAX/Burnout.

Os arquivos `CONTINUIDADE.md`, `PENDENCIAS.md` e `MATRIZ-FUNCIONAL.md` do workspace
foram atualizados para 128/148. Árvores históricas e mídia permanecem intactas.
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
