# Extrator oficial para Ship of Harkinian 9.3.1

## Artefato e alcance

O helper usa a CLI **standalone do Torch upstream**, no mesmo commit que o
Shipwright 9.3.1 referencia: 2ab12fe9660aec04e02ee89fe81baed304a1a1d6.
Não contém alterações próprias no Torch, no jogo, em renderers ou em shaders.

O build verificado em 28/11/2026 produziu torch.exe, Windows x64, com
2.226.688 bytes e SHA-256:

~~~text
947b5714668072c121166abcf3bfeee72c77495c52a3cbf4a1b2b7e0e284a15c
~~~

Foram comparados os hashes dos **764 arquivos de fonte do Torch** antes e
depois do build; todos permaneceram iguais. As dependências foram exportadas
dos commits oficiais em caches Git existentes. O CMake oficial do zlib
renomeia zconf.h para zconf.h.included durante a configuração; essa
transformação é registrada separadamente e não é um patch AllFix.

Esta comprovação cobre a origem, compilação e testes sintéticos do extrator.
Não comprova extração de uma ROM original, primeiro boot ou gameplay via GetAll.

## Fontes e parâmetros

- [Shipwright 9.3.1, CMakeLists.txt](https://github.com/HarbourMasters/Shipwright/blob/f0599f96f8d442f26d0fa1c5cedafddacd56633f/CMakeLists.txt)
  define PORT_VERSION_ENDIANNESS=ON, ROM_CRC_BSWAP=OFF, BUILD_OOT=ON,
  UI/StormLib/NAudio e demais jogos desativados.
- [Torch, CLI oficial](https://github.com/HarbourMasters/Torch/blob/2ab12fe9660aec04e02ee89fe81baed304a1a1d6/src/main.cpp)
  fornece os comandos o2r e pack, com diretórios de entrada/saída e versão.
- [Torch, opções oficiais de build](https://github.com/HarbourMasters/Torch/blob/2ab12fe9660aec04e02ee89fe81baed304a1a1d6/CMakeLists.txt)
  fornece USE_STANDALONE=ON. Essa opção habilita sua própria CLI.
- [TorchExtract.cpp do Shipwright](https://github.com/HarbourMasters/Shipwright/blob/f0599f96f8d442f26d0fa1c5cedafddacd56633f/soh/soh/Extractor/TorchExtract.cpp)
  usa o mesmo Companion, formato O2R, versão e metadados.
- upstream.json fixa os commits, URLs e SHA-256 dos seis arquivos de fonte
  usados na reprodução. source-files.sha256.json registra os 764 arquivos.

## Reprodução

Requisitos: Windows x64, Python 3.10+, Visual Studio 2022 com ferramentas C++,
CMake e Ninja. O build inicial validado usou MSVC 14.44.35207 e dois jobs.
Nenhum programa é instalado por estes scripts.

~~~powershell
python Tools/NativeExtractors/SoH/build.py --work-dir C:\AllFix-Tools\SoH
python Tools/NativeExtractors/SoH/verify.py --binary C:\AllFix-Tools\SoH\build\torch.exe --work-dir C:\AllFix-Tools\SoH\probe
~~~

A opção --archive-cache de build.py reutiliza os arquivos ZIP identificados
em upstream.json. Se necessário, --cmake, --ninja e --vcvars informam
os caminhos das ferramentas. O script verifica os arquivos baixados antes de
extrair, usa os CMake oficiais e compara as fontes após compilar. Ele grava
build.cmd, build.log e build-result.json no diretório escolhido.

A opção --config de verify.py usa uma cópia local do config oficial, com
hash obrigatório. --expected-sha256 confere um helper já produzido.
O probe exige um diretório vazio, evitando confundir arquivos antigos com saída
do teste. A reprodução pode gerar outro hash do executável por diferenças de
toolchain e caminhos; o hash acima identifica o artefato efetivamente auditado.

## Contrato de extração

Perfil novo: **ship-of-harkinian-9.3.1-official-extractor**.

~~~text
torch.exe o2r <ROM.z64> -s <assets-oficiais-9.3.1> -d <diretorio-saida> -u 9.3.1
~~~

O diretório assets deve conter config.yml e as definições oficiais
correspondentes ao pacote Shipwright 9.3.1. O arquivo de entrada deve ser a ROM
legítima do usuário, de uma revisão aceita pelos hashes oficiais e em ordem
big endian .z64. O config escolhe oot.o2r ou oot-mq.o2r; o integrador
não deve presumir o nome sem verificar a revisão selecionada.

**Não basta aceitar exit code 0.** O Torch upstream retorna zero mesmo quando
um hash de ROM não consta no config. Antes de concluir a instalação, exigir
o archive esperado, recursos necessários e os metadados do jogo e da versão.
O metadado portVersion para 9.3.1 tem sete bytes:
01 00 09 00 03 00 01. O primeiro byte marca big endian; os demais são três
inteiros de 16 bits. O arquivo version identifica a ROM e também precisa ser
validado pelo contrato de instalação. Os probes sintéticos não geram esse archive de jogo.

Preservar os dados pessoais e as preferências do usuário. Usar diretório de
saída temporário novo para não aceitar recursos remanescentes de outra tentativa.
O helper não deve ser distribuído junto de ROMs nem de arquivos extraídos delas.

## Wrapper antigo e alternativa verificada

O alvo SOH_TOOLS_ONLY / soh-torch do próprio Shipwright 9.3.1 contém uma
incompatibilidade: main.cpp passa o caminho como std::string, enquanto
TorchExtract.h declara a entrada como std::vector<uint8_t>. Uma compilação
isolada das fontes oficiais intactas reproduziu MSVC C2664, exit code 2.
A mudança upstream ocorreu em
[94be08c / PR 7301](https://github.com/HarbourMasters/Shipwright/commit/94be08c27ec349efa87a3f8ab6ebc7abffc531c3).

Essa falha não significa ausência de um extrator oficial. A CLI standalone do
mesmo Torch foi compilada e verificada com sucesso. Não se reaproveita o helper
antigo soh-torch.exe, cujo histórico de construção declarava uma correção
particular da chamada. O perfil histórico continua separado do perfil novo.

## Evidências incluídas

- build-evidence.json: commit, opções, dependências e hash do artefato auditado.
- native-probe-evidence.json: ajuda CLI, arquivo ausente, ROM sintética inválida
  e empacotamento sintético com formato correto de portVersion.
- wrapper-compile-evidence.json: erro real e hashes das fontes intactas.
- source-files.sha256.json: inventário das fontes antes/depois.
- LICENSE-Torch.txt: licença preservada do upstream. As licenças das
  dependências permanecem nos respectivos arquivos de fonte identificados.

Todos os sete checks nativos passaram. O arquivo ausente retornou 105; a ROM
sintética de 64 bytes teve o hash recusado, sem archive, apesar de retornar zero;
o teste de pack preservou o texto sintético e gerou portVersion correto.
Nenhum desses resultados é registrado como mídia original, boot ou gameplay.
