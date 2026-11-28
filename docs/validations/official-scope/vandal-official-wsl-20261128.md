# Vandal Hearts — helper oficial via WSL, validação de 28/11/2026

## Resultado e limites

O helper externo de build oficial foi implementado no Desktop e passou **19/19 testes no WSL**, incluindo cancelamento real com filho e neto, heartbeat, timeout, integridade e publicação em staging. A preparação privada de dependências também passou: novo SDK MinGW extraído de pacotes fixados, FFmpeg 7.1 compilado pelo script oficial, um pequeno executável AMD64 de dependências ligado e auditado, e configurações oficiais US/JP com WebP/HDVideo habilitados.

**Não houve build completo do jogo, instalação com mídia original, primeiro boot ou teste de jogabilidade nesta validação.** Os discos US/JP e uma fonte de BIOS/KROM válida não estavam disponíveis. O executável usado no smoke é um programa próprio mínimo que referencia bibliotecas; não contém nem simula o jogo e não foi executado no Windows.

| Dimensão | Resultado observado |
| --- | --- |
| Helper e supervisão Linux | 19 testes aprovados, zero falhas, zero skips, 3,308 s |
| SDK MinGW privado | Extraído novamente de .deb com SHA256 fixado |
| FFmpeg | Script oficial intacto, versão 7.1, bibliotecas estáticas produzidas |
| Probe AMD64 de dependências | Link aprovado; imports e DLLs auditados; execução não realizada |
| CMake US e JP | VH_BLOB=ON, VH_UNIFIED_CORE=ON, VH_WEBP=ON, VH_HDVIDEO=ON |
| Arquivos originais da fonte | Snapshot de arquivos e symlink preservado |
| Processos próprios | Todos os processos dos grupos iniciados foram encerrados e recolhidos por wait |
| Build completo / mídia original / boot / gameplay | Não executados; exigem os originais do usuário |

O estado demonstrado é **preparação e automação prontas para receber a mídia original**, sem promover o resultado sintético a validação de jogo instalado ou jogável.

## Código e fonte fixados

Os arquivos de implementação estão na worktree Desktop:

- `Tools/OfficialBuilders/vandal_wsl.py` — SHA256 `68f409dcb002e3f12c064cafdbfbe4aac76c26bd9e947a1a627964dd9f519911`.
- `Tests/AddonInfrastructure/vandal_wsl_test.py` — SHA256 `66a6f175bc48bc54be33e19a79079b0f066e70b1b0b6e343db91d895b8885abd`.

A fonte é [HalmyLyseas/VandalHearts-PcPort](https://github.com/HalmyLyseas/VandalHearts-PcPort), commit `14552fffa0e0b47e02b57592e274fc6e7a649923`. O [ZIP fixado](https://codeload.github.com/HalmyLyseas/VandalHearts-PcPort/zip/14552fffa0e0b47e02b57592e274fc6e7a649923) tem **21.396.545 bytes** e SHA256 `e7c50aaddf57c05df97eee50c9355473a1a4ea6d8354fe719c9450f89b14160f`.

A validação final confirma 562 entradas no ZIP e um symlink Unix: `jp/tools/maspsx → ../external/maspsx`. O helper extrai no Linux, aceita apenas destinos internos à raiz e preserva o conteúdo do link. Nenhum link precisa ser materializado no Windows.

O ZIP é copiado para o staging Linux com conferência do SHA256 constante durante a cópia, antes de ser extraído ou de qualquer script upstream ser executado. BIOS/KROM também recebe cópia privada verificada. Os discos são projetados em setores ISO9660 para extrair os executáveis originais; os executáveis são validados antes da preparação de dependências. Ao término, o helper verifica novamente os inputs fornecidos e o snapshot dos arquivos originais da fonte.

## Ambiente e dependências

O `--probe` final retornou `ok: true` em Ubuntu 26.04 LTS, kernel `6.18.33.1-microsoft-standard-WSL2`, Python 3.14.4, glibc 2.43 e x86_64.

Os requisitos técnicos checados pelo helper são Linux x86_64, Python ≥3.12, glibc ≥2.38, libzstd e executáveis `/usr/bin/cmake`, `ninja`, `make`, `gcc`, `dpkg-deb` e `bash`. O Desktop seleciona a distribuição `Ubuntu`; WSL2 Ubuntu 26.04 é o ambiente validado. A rotina não instala pacotes no sistema, não usa sudo, não habilita Developer Mode e não desliga WSL.

Os 16 pacotes Ubuntu e os quatro arquivos SDL2/OpenAL/WebP/FFmpeg têm URL e SHA256 literais no helper e na seção `dependency_archives` do [resultado JSON](vandal-official-wsl-20261128-result.json). O SDK é extraído em um diretório Linux próprio por `dpkg-deb --extract`. Arquivos de cache podem ser lidos somente depois de conferir o hash; nenhum SDK compilado anteriormente é requisito.

| Dependência | Versão / origem |
| --- | --- |
| GCC MinGW POSIX | Pacote 13.2.0-6ubuntu1+26.1 |
| MinGW headers | Pacote 13.0.0-2ubuntu1 |
| NASM privado | Pacote 3.01-1 |
| SDL2 | 2.30.11, release oficial MinGW |
| OpenAL Soft | 1.25.2, pacote binário oficial Win64 |
| WebP | 1.6.0-1, pacote MinGW64 MSYS2 |
| FFmpeg | 7.1, tarball oficial e script do port intacto |

A tentativa inicial encontrou uma URL Ubuntu indisponível para uma atualização do zlib. Foi fixada a versão base disponível `1.3.dfsg+really1.3.1-1ubuntu3`, com metadado oficial e SHA256 `c45bbbf9c87457d90b8ba38720c5f01b9388c380d40f303c26f5c4953932da26`; ela foi efetivamente obtida e extraída. A URL integral está no JSON.

O arquivo WebP real usa Zstandard sem informar o tamanho descomprimido. O helper faz descompressão em streaming com limite de expansão; a regressão cobre esse formato, truncamento e limite. A primeira versão do pequeno probe tinha assinatura de `main` incompatível com SDL; foi corrigida somente no arquivo descartável do probe usando `SDL_MAIN_HANDLED`. As fontes upstream não receberam patches.

## Pipeline oficial e revisão final

O procedimento segue [CMakeLists.txt](https://github.com/HalmyLyseas/VandalHearts-PcPort/blob/14552fffa0e0b47e02b57592e274fc6e7a649923/platform/pc/CMakeLists.txt), [build-unified-win.sh](https://github.com/HalmyLyseas/VandalHearts-PcPort/blob/14552fffa0e0b47e02b57592e274fc6e7a649923/platform/pc/packaging/build-unified-win.sh), [build-ffmpeg-static.sh](https://github.com/HalmyLyseas/VandalHearts-PcPort/blob/14552fffa0e0b47e02b57592e274fc6e7a649923/platform/pc/tools/build-ffmpeg-static.sh) e [gen_assets_inc.py](https://github.com/HalmyLyseas/VandalHearts-PcPort/blob/14552fffa0e0b47e02b57592e274fc6e7a649923/jp/tools/gen_assets_inc.py) do commit fixado.

1. O Desktop valida a identidade completa dos discos com OriginalPsxDisc/SHA1 e fornece as cópias privadas e seus SHA256. O helper revalida esses SHA256, extrai `SLUS_004.47` e `SLPM_860.07` dos LBAs oficiais 23 e 15200 e confere os hashes upstream. Não há bypass de identidade.
2. O helper valida os dois prefixos de fonte US/JP no KROM, ou a região a partir de 0x66000 de uma BIOS de 512 KiB. A entrada tem teto de 1 MiB. O arquivo bruto de BIOS/KROM permanece fora do payload.
3. O original US é copiado para `<source>/SLUS_004.47`; o JP, para `<source>/jp/SLPM_860.07`. O gerador JP oficial produz `jp/assets/801009bc.inc`, `80100e9c.inc`, `8010102c.inc` e o link `jp/include/assets`. **Nenhum desses quatro caminhos está presente no ZIP**, portanto a geração não exige modificar arquivos versionados.
4. O script oficial de FFmpeg produz libavformat/libavcodec/libavutil/libswscale estáticas usando o SDK privado, sem alterações no script.
5. CMake configura e compila separadamente US e JP com `VH_UNIFIED_CORE=ON`, `VH_BLOB=ON`, `VH_WEBP=ON` e `VH_HDVIDEO=ON`, além de `VH_PSX_EXE` e `VH_KROM_SOURCE` privados.
6. A terceira etapa liga `VH_UNIFIED_CORES=<core_us.o>;<core_jp.o>`. No CMake fixado, as listas de fontes/objetos e os geradores estão no bloco `if(NOT VH_UNIFIED_CORES)` (linhas 128–454); o ramo unificado liga `pc_region_main.c` mais os dois objetos (488–491). A referência posterior a PSX/KROM para metadados é exclusiva de APPLE (617–640). Assim, a etapa unificada Windows não precisa repetir o override de `VH_PSX_EXE`. A cópia US na raiz também satisfaz o valor default.
7. O helper coleta o EXE/INI, resolve recursivamente DLLs não pertencentes ao sistema, verifica AMD64 e emite manifesto com caminho relativo, tamanho, SHA256 e imports. `LICENSE`, `NOTICE`, `DISCLAIMER` e `CREDITS` foram confirmados no ZIP; seus hashes estão no JSON.
8. O payload é verificado em uma pasta irmã e publicado por rename para um output inexistente ou vazio. `copy_discs` é falso por padrão; o Desktop move os discos privados para `game/vandalhearts-us.bin` e `game/vandalhearts-jp.bin` depois de validar o recibo. BIOS bruta não é publicada.

O smoke de dependências/configuração terminou antes do último fechamento da cópia privada de inputs e da localização de logs. Os bytes finais do helper acima passaram novamente pelos 19 testes. Os pins, opções e comandos oficiais usados para construir as dependências não mudaram; não foi repetido o build de FFmpeg sem um risco restante que justificasse isso.

## Supervisão e diagnóstico

Cada comando é iniciado em sua própria sessão/grupo Linux. O helper mantém o líder aguardável, sinaliza somente seu grupo e usa child-subreaper para recolher os filhos órfãos via wait. Os testes reais confirmam filho/neto resistentes a SIGTERM, timeout, heartbeat expirado, órfão após saída normal e preservação de um grupo não relacionado.

O cancelamento retorna código 4; timeout interno, 5. O timeout padrão é 3.600 s e o heartbeat vence em 60 s. O Desktop fornece `request_id`, sentinel e heartbeat; o recibo ecoa o ID e só atesta `process_groups_reaped: true` depois da supervisão. Falta de confirmação preserva o trabalho da transação no Desktop.

A saída de compilação tem limite agregado de 100 MiB; stdout do helper contém apenas eventos JSONL curtos. Os logs preserváveis ficam em `work/logs/vandal-<token>-*.log`, com cópia do recibo em `vandal-<token>-receipt.log`. Os nomes são exclusivos e não sobrescrevem arquivos existentes.

## Evidências e reprodução

- [Resultado completo e comandos executados](vandal-official-wsl-20261128-result.json).
- [Log integral dos 19 testes](vandal-official-wsl-20261128-tests.log).
- [Trechos pequenos dos logs do smoke](vandal-official-wsl-20261128-smoke.log), com SHA256 e tamanho dos logs integrais.
- Diretório Linux exclusivo da verificação: `/tmp/allfix-vandal-helper-validation-20261128-9a61b4`.
- SDK/FFmpeg recém-preparados: `/tmp/allfix-vandal-helper-validation-20261128-9a61b4/private-provision-jghwqpy_`.

Com caminhos absolutos ajustados ao checkout, a verificação do ambiente é:

```text
wsl.exe --distribution Ubuntu --exec python3 <helper-linux-path> --probe
```

Os testes usam o ZIP oficial existente e não baixam dependências:

```text
wsl.exe --distribution Ubuntu --exec env VANDAL_SOURCE_ZIP=<pinned-source-zip-linux-path> python3 <tests-linux-path>
```

A execução real do helper exige um request JSON com os originais válidos, output vazio e arquivos de controle fora do output:

```text
wsl.exe --distribution Ubuntu --exec python3 <helper-linux-path> --request <request-json-path>
```

A integração Desktop usa o loader fixo que verifica SHA256 do helper antes de executar o recurso e passa o request em base64. O histórico JSON preserva os argv efetivamente usados em extração, FFmpeg, link do probe e configuração US/JP.

Os SHA256 das bibliotecas compiladas e do probe identificam esta execução. O script oficial inclui caminhos/metadados de debug, portanto não se afirma identidade binária entre reconstruções em diretórios diferentes. Os logs e relatórios não contêm mídia comercial, BIOS ou executáveis originais.
