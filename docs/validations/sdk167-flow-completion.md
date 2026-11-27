# Continuidade de implementação — SDK 1.5.67

## Estado confirmado em 27/11/2026

O checkpoint do Bradsson registra **122 de 148 projetos com fluxo integral
implementado**, oito a mais que os 114 do SDK 1.5.66. Há um homologado histórico
e 121 integrais aguardando mídia original; 17 parciais, dois adiados pelo usuário
e sete sem receita. A contagem é calculada sobre as 148 linhas únicas da matriz.

O índice desta branch contém **143 receitas para 141 projetos**: uma entrada
`validated` histórica e 142 experimentais. Dr. Mario recebeu a nova receita e
fechou a preparação automática. Nenhuma das novas receitas foi homologada.

O checkpoint de código Desktop local `7402a99e012aef390a2fc5cb1c1f62e7f555d086`
preserva 68 arquivos da primeira etapa. Correções posteriores seguem em
andamento. A prévia SDK 1.5.66 e os commits-base `c209adc`/`f0942a6` permanecem
preservados. Nova prévia e CI estão pendentes; nenhum merge ou release ocorreu.

## Oito fluxos concluídos tecnicamente

| Projeto | Automação acrescentada | Verificação executada |
|---|---|---|
| `sm64ex` | MSYS2/UCRT64 privado substitui Docker/MXE; ROM, extração, compilação, publicação e Jogar integrados. | Fonte oficial, ferramentas upstream compiladas, loader SDL e rejeição da ROM sintética. |
| `render96ex` | Compilação Windows privada e integração com os packs opcionais existentes. | Fonte oficial e ferramentas reais, loader SDL, políticas de publicação e lançamento. |
| `sm64rt` | Perfil RT64/SDL2 corrigido, SDL2/GLEW fixados e runtime Microsoft app-local. | Ferramentas oficiais, probe SDL/GLEW e dependências PE inspecionadas. |
| `strikers-wiicompiled` | SDK .NET 8.0.425, YamlDotNet 15.1.2 e runtime privados; FST completo e mídia validados. | 38 verificações de fluxo, quatro do tradutor oficial e três do decoder nodtool. |
| `wipeout-rewrite` | UCRT64 privado; composição dos dados PSX e quatro arquivos PC; revalidação no lançamento. | 13 verificações de composição, build nativo e 11 da transação real Run/Resume/registro/Jogar; mídia sintética, sem executar jogo. |
| `drmario64-recomp` | ROM US antes do consentimento; 38 fontes, Python/wheels, LLVM MIPS e LLVM-MinGW privados; 12 adaptações verificadas; geração, build, registro e Jogar. | 52 checks e SourceTools4 de produção: Python, DXC, Clang, sete produtos MIPS e nove avisos. RT64 D3D12/Vulkan, runtime N64 e interface pública compilados e ligados. |
| `mariokartdd-recomp` | LLVM-MinGW UCRT substitui gate MSVC; SDL2/C++ estáticos, ISO GM4E01, build e registro integrados. | Runtime completo e runtime_check da fonte oficial; probe no mesmo CMake executa SDL, threads e exceções C++20 sob PATH Windows, sem compilador global. |
| `burnout3-recomp` | LLVM-MinGW/Ninja privados no ramo Xbox; mídia, geração/build, staging, registro e lançamento integrados. | Oito bibliotecas do runtime e quatro testes D3D8 reais, incluindo DXGI Present. Fluxo de produção e 16 checks de ISO, adaptação, cancelamento e contratos PE aprovados. |

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

| Projeto | Estado conhecido | Próxima verificação |
|---|---|---|
| `mkdd-recomp` (Rust) | Rust 1.100.0 gnullvm e LLVM-MinGW privados, Cargo.lock preservado; gc-core/gc-runtime oficiais testados e Bevy/CPAL/WGPU reais compilados, ligados e executados. | Corrigidos layout duplicado do GameCubeLoader e home Java. Prova Ghidra headless com DOL próprio em preparação. |
| `strikersrecomp` (GameCube) | GXRuntime f83d258 compatível, SDL/Dawn/CRT fixados; 463 objetos e host/renderer ligados na árvore diagnóstica, nove checks de fluxo. | Prova integral pela produção e criação/liberação de instância WebGPU C sob ambiente privado. |
| `doaxvb-re` | Dependências CMake, DXC e CRT privados; RTGI solicitado exige shaders efetivos. Extração cliente miniupnpc preserva licença sem criar links. | Preflight nativo de produção com runtime, D3D11, Vulkan e RTGI. |
| `god-of-war-recomp` | Gerador e runner públicos ligados/executados com LLVM-MinGW; override oficial passa análise sintática. | Integração C# do disco US dual-layer, pipeline interpretado padrão e argumento de lançamento. |

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
- `flow-completion-20261127/regression-10.log`: **1.618 PASS, zero falhas**,
  exit 0 em 12,23 s; build 10 sem erros ou avisos.
- `flow-completion-20261127/work-progress-122.json` e
  `checkpoint-backups-122`: contagem e preservação do checkpoint anterior.
- `flow-completion-20261127/getall-parser.json`: 143 receitas aceitas pelo
  parser do build 4; instruções alteradas depois ainda terão conferência final.

Os arquivos `CONTINUIDADE.md`, `PENDENCIAS.md` e `MATRIZ-FUNCIONAL.md` do workspace
foram atualizados para 122/148. Árvores históricas e mídia permanecem intactas.
A fila continua com contagens novas somente após a prova do fluxo correspondente.
