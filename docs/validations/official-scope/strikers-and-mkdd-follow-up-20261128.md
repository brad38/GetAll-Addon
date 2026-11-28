# Validação técnica de StrikersRecomp e Double Dash C++ em 28/11/2026

## StrikersRecomp

Foram exercitados o gerador oficial, a tabela de símbolos e o CMake dos
projetos sem alterar as fontes. A entrada de teste tem três instruções PPC
autorais de retorno. A build usou MSVC 19.44.35230.0 com Ninja e o renderer
Aurora habilitado. Foram conferidos 3.867 arquivos originais por SHA-256.

| Revisão StrikersRecomp | Dependência em teste | Resultado Windows |
| --- | --- | --- |
| `67047ed` (v0.1.0) | `b4c85bb` (tag DolRuntime v0.1.0 no repositório hoje chamado GXRuntime) | Geração e configuração concluídas. A compilação falhou em `src/dvd.c` pelo uso de `off_t` e `fseeko`, sem alternativa Win32 na fonte. |
| `cd88f71` | `b4c85bb`, tag que o bootstrap atual exige | O CMake interrompeu a geração por faltar `GXRuntime::runtime` e `GXRuntime::aurora`. A tag oferece os targets `DolRuntime::*`. |
| `cd88f71` | `8a47b0e`, head oficial do GXRuntime | A configuração aceitou a API nova. A compilação MSVC falhou no mesmo acesso de disco. |
| `cd88f71` | `f83d258`, commit oficial anterior com API compatível | A configuração passou. A compilação MSVC falhou no mesmo ponto. |
| `cd88f71` | `8a47b0e`, LLVM-MinGW 23.1.4 com Dawn e SDL3 publicados | A configuração passou. A compilação isolada de `runtime/host/main.c` falhou nos sinais POSIX `SIGUSR1` e `SIGUSR2`. |

O módulo RecompCore continua sem binário Windows publicado. Sua rotina
oficial de empacotamento seleciona `.dylib` no macOS e `.so` nos demais hosts.
O CI do jogo só executa lint. Os CIs de GXRuntime e RecompCore verificam
macOS e Linux. O upstream apresenta Windows como trabalho futuro.

O projeto continua manual. O executável standalone segue bloqueado no
Windows. A prova do host alternativo está descrita abaixo. Os testes e hashes
estão em [strikers-native-probe-result-20261128.json](strikers-native-probe-result-20261128.json).

Fontes oficiais.
[StrikersRecomp cd88f71](https://github.com/aharonahdoot/StrikersRecomp/tree/cd88f71f5a836c103484c038454b4143000d883c)
[GXRuntime 8a47b0e](https://github.com/aharonahdoot/GXRuntime/tree/8a47b0e8ea7dfc39014a4cff4f7895d88494a611)
[RecompCore](https://github.com/aharonahdoot/RecompCore)

### Rota alternativa RecompCore

A chamada direta ao CMake do módulo, com LLVM-MinGW e ABI do RecompCore
`283baee`, gerou um PE x64 `gG4QE01_recomp.dll` com o símbolo
`staticrecomp_get_module`. Uma segunda mídia de teste, com instruções
PPC autorais de invalidação de cache, fez o DolRecomp emitir o próprio
relatório de nove intervalos SMC. O carregador do Windows abriu a DLL e
leu ABI 2, ABI da CPU 2, tamanho de CPU 7592, três intervalos de código
e três hashes de chunks. A prova só leu o descritor da fixture.

O projeto Visual Studio de `DolphinLib` omite as fontes StaticRecomp.
O projeto CMake inclui essas fontes e o frontend `PlatformWin32`. O
teste do módulo não comprova que esse host consiga iniciar o jogo.

### Rota Linux em WSL

As tags oficiais de StrikersRecomp e DolRuntime v0.1.0 passaram pelas 726
etapas de compilação e link em Linux x86-64 com Clang 21.1.8 e Aurora
habilitado. As dependências da distribuição foram extraídas em uma pasta
privada do teste. A tentativa anterior com GCC parou em uma inicialização
designada fora da ordem do padrão C++ em `gxcore.cpp`. O Clang aceitou
o código upstream, mantendo o aviso.

O modo oficial `--call` executou um bloco PPC sintético e retornou ao
sentinela `0x0BADF00C`, com código de saída 0 e sem abrir janela. Essa
rota confirma o ambiente Linux. A instalação automatizada Windows do
GetAll e a execução da mídia original seguem sem homologação.

## Mario Kart: Double Dash!! C++

A compilação oficial sem disco parava no `runtime_check`. Um projeto CMake
externo reutilizou `gcn_add_game` do submódulo original com duas funções PPC
autorais, ID sintético `AFTEST`, o hash real desse DOL e as quatro fontes
Windows do projeto. Foram conferidos 165 arquivos originais por SHA-256.
O Clang 23.1.3 e o MSVC compilaram `xr_desktop.cpp`, `xr_frontend.cpp`,
o loader estático Khronos OpenXR 1.1.63 e vincularam o executável de teste.

Com `--vr` e mídia sintética, o executável chegou ao loader, que retornou
`XR_ERROR_RUNTIME_UNAVAILABLE` (-51) por ausência de um runtime OpenXR ativo.
A mensagem de erro oficial foi exibida. Um caminho de disco ausente com
espaços também foi rejeitado antes de inicializar o jogo.

Este teste verifica a compilação e o link do frontend Windows de ponta a
ponta com dados autorais. O alvo de jogo do upstream exige um disco legítimo
GM4E01 com o `main.dol` SHA-1 `e389e50357d4a5076ab3d38672204658f411123d`
para gerar e compilar o código final. A instalação com essa mídia, o
primeiro boot, uma sessão de gameplay e a execução em um headset seguem
pendentes.

[Resultado](mkdd-openxr-synthetic-result-20261128.json)
[Script](mkdd-openxr-synthetic-probe.py)
[Código do jogo fixado](https://github.com/ethannicholas/mariokartdd-recomp/tree/bd36eb982ea58c6651584cc48264876d1aba9546)
[Submódulo fixado](https://github.com/ethannicholas/gcn-recomp/tree/b2193d7c7ce65c40959cf81859beaacafeebfd99)

### Host Windows RecompCore compilado

O host oficial `283baee` gerou `DolphinNoGUI.exe`. A primeira compilação
MSVC interrompeu no aviso C5048 sobre `__DATE__` e `__TIME__` sob
`/WX`. A retomada usou `_CL_=/wd5048`, restrito a esse aviso de
compilação. As fontes ficaram intactas e os renderizadores permaneceram
compilados. O executável identificou a revisão oficial em `--version`.

Em duas execuções Windows com o DOL sintético QA01, o núcleo 6 rejeitou a
DLL com ID G4QE01 e carregou a DLL gerada com o template oficial para
ID-QA01. O teste sem janela usou a saída de vídeo Null somente na
execução de diagnóstico. Ambos os processos foram encerrados no limite
do teste. O registro confirma carregamento e rejeição por identidade.
A criação do módulo com a ISO original, o empacotamento licenciado do
host e a integração de instalação e lançamento no GetAll continuam
pendentes.

- [Recibo Windows com hashes](strikers-recompcore-headless-result-20261128.json)
- [Script de reprodução](strikers-recompcore-headless-probe.py)
- [Procedimento oficial RecompCore](https://github.com/aharonahdoot/RecompCore/blob/283baee01e54b6c3f71e441bb78fc77b260512fa/CHASSIS.md)

### Empacotamento local do host

O pacote de teste reúne o executável do build anterior, a árvore oficial
Sys, COPYING e LICENSES. O script verifica que o checkout corresponde
ao commit fixado e que a árvore rastreada está intacta. O manifesto local
verifica os 2.635 arquivos por caminho, tamanho e SHA-256. As duas provas
headless passaram novamente usando o executável da pasta empacotada.

O pacote é local. Para distribuí-lo, ainda é necessário preparar a oferta
de fontes correspondentes com os submódulos fixados e instruções de build.
O GetAll ainda precisa de uma rota fechada para gerar o módulo G4QE01
a partir da ISO verificada, fornecer a pasta de usuário isolada ao host
e registrar o lançamento após validação da mídia original.

- [Script de empacotamento local](strikers-stage-recompcore-host.py)
- [Recibo do pacote de teste](strikers-staged-host-result-20261128.json)

### Ensaio da rota ISO oficial

Uma imagem GameCube criada para teste, ID QATX01, exercitou o fluxo
`generate.py --iso` em um caminho com espaços. O DolRecomp extraiu o DOL
autoral com SHA-256 idêntico e o CMake upstream produziu a DLL Windows
`gG4QE01_recomp.dll`. A imagem sintética permaneceu idêntica e o teste
ficou em uma pasta isolada. Essa prova cobre a extração, geração e link,
sem tentar instalar ou iniciar o jogo comercial.

- [Script da prova](strikers-iso-module-probe.py)
- [Recibo e hashes](strikers-iso-module-result-20261128.json)

### Contrato GetAll de prévia

A substituição experimental mantém o jogo fixado em cd88f71 e usa a
rota RecompCore, separada do standalone GXRuntime. O índice requer SDK 1.5.71
e autoriza somente a receita v9 de hash fixado. A receita v5 anterior
permanece arquivada e bloqueada para execução. O SDK recebe uma única
ISO G4QE01 Rev 0 fornecida pelo usuário.

A validação de schema, identidade, política e hash do contrato passou.
Os ensaios de host e de geração acima usaram mídias autorais. Instalação
com mídia original e primeiro boot são evidências ainda pendentes.

O SDK 1.5.71 executou 15 verificações do kit e testou compilação, staging
e lançamento com mídia autoral. O host encontrou a DLL pelo ID, sem
variável de ambiente de substituição. A verificação de lançamento
recusou a DLL alterada. [Recibo](strikers-getall-result-20261128.json).
