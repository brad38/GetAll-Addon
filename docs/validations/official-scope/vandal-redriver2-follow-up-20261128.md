# Validação de Vandal Hearts e REDRIVER2 em 28/11/2026

`vandalhearts-pcport` e `redriver2` permanecem com procedimentos manuais. Esta revisão verificou pré-requisitos da compilação e a origem dos arquivos nos procedimentos oficiais. A matriz deve preservar o estado de instalação, primeiro boot e gameplay como desconhecido para ambos.

## Vandal Hearts v2.1.0

A tag `v2.1.0` aponta para `7450a2462c0d437740da2ec438a7d8d55c27fadf`. A revisão fixada `14552fffa0e0b47e02b57592e274fc6e7a649923` está um commit à frente. A comparação upstream mostra somente mudanças no changelog e no empacotamento de releases, incluindo seu teste. Os geradores e o script unificado usados aqui são os mesmos. [Comparação upstream](https://github.com/HalmyLyseas/VandalHearts-PcPort/compare/7450a2462c0d437740da2ec438a7d8d55c27fadf...14552fffa0e0b47e02b57592e274fc6e7a649923)

- O CMake Windows nativo anterior parava no privilégio para criar symlinks e na localização do OpenAL. Em Ubuntu 26.04 sobre WSL2, a configuração do CMake com o compilador GNU 15.2.0 criou os symlinks originais em `datagen/include_stage`, inclusive o de `PsyQ`. A configuração chegou ao `find_package(SDL2)` e parou por falta de `SDL2Config.cmake`.
- A rota oficial do executável Windows usa `build-unified-win.sh`. Sua verificação de ferramentas parou porque não há `x86_64-w64-mingw32-gcc` nesse Ubuntu. Além do MinGW-w64, a compilação requer as dependências Windows de SDL2, OpenAL e WebP e o prefixo estático de libav. Nenhuma configuração global de privilégios foi alterada.
- O script oficial recompila os núcleos US e JP e os liga na versão unificada. Ele depende, portanto, dos dois executáveis originais `SLUS_004.47` e `SLPM_860.07`, além de KROMDAT ou BIOS compatível. O gerador verifica o MD5 esperado por região e o SHA-256 do trecho de fonte do BIOS. O lançamento do executável pronto com um disco suportado e a produção local do executável unificado possuem requisitos diferentes.
- Os geradores intactos do commit fixado recusaram executáveis ausentes, inválidos, truncados e com hash incorreto, além de KROM truncado e BIOS de tamanho correto com conteúdo inválido. As 12 verificações negativas passaram, sem gerar dados. A paridade de 54 unidades de compilação e 11 headers também passou. O caminho das fixtures contém espaços. Resultado em [vandal-source-inputs-result.json](vandal-source-inputs-result.json).
- O aviso de licenciamento e a release documentam conteúdo de jogo e BIOS embutido no binário publicado. Para o GetAll, fica pendente o teste da compilação local com as entradas originais. Essa rota evita redistribuir o binário com dados derivados e não depende de alterar a fonte do jogo.

Fontes upstream: [procedimento de build](https://github.com/HalmyLyseas/VandalHearts-PcPort/blob/14552fffa0e0b47e02b57592e274fc6e7a649923/docs/building.md), [script de build unificado](https://github.com/HalmyLyseas/VandalHearts-PcPort/blob/14552fffa0e0b47e02b57592e274fc6e7a649923/platform/pc/packaging/build-unified-win.sh), [aviso de licenciamento](https://github.com/HalmyLyseas/VandalHearts-PcPort/blob/14552fffa0e0b47e02b57592e274fc6e7a649923/NOTICE) e [release v2.1.0](https://github.com/HalmyLyseas/VandalHearts-PcPort/releases/tag/v2.1.0).

### Reproduzir as verificações

Aponte `$source` para a extração intacta em `research-cache/vandal-source/source`.

```powershell
python -B ./test-vandal-source-inputs.py $source
```

Com `$linuxSource` apontando para a mesma árvore no WSL e uma pasta de saída nova:

```powershell
wsl -d Ubuntu -- cmake -S "$linuxSource/platform/pc" -B /tmp/getall-vandal-20261128-linux-config -G Ninja
wsl -d Ubuntu -- ls -l /tmp/getall-vandal-20261128-linux-config/datagen/include_stage/PsyQ
```

O script abaixo verifica MinGW-w64 e libav antes de limpar os diretórios de build relativos à fonte e iniciar a compilação. Quando os pré-requisitos estiverem disponíveis, execute-o em uma extração exclusiva de teste.

```powershell
wsl -d Ubuntu -- bash "$linuxSource/platform/pc/packaging/build-unified-win.sh"
```

### Cross-build Windows x64 reproduzido até as entradas originais

A preparação privada no WSL superou o bloqueio de ferramentas encontrado acima. O GCC MinGW-w64 e o NASM vieram dos pacotes oficiais Ubuntu, extraídos com `dpkg-deb -x` para um prefixo privado. SDL2 2.30.11, OpenAL Soft 1.25.2 e WebP 1.6.0 foram preparados em outro prefixo com headers, bibliotecas de importação, DLLs x64 e licenças. A cópia Win64 de `soft_oal.dll` foi nomeada `OpenAL32.dll` de acordo com a biblioteca de importação oficial. A distribuição MSYS2 de WebP preserva exatamente `libwebp-7.dll` e `libsharpyuv-0.dll`, os nomes esperados pelo empacotador upstream.

O script intacto `tools/build-ffmpeg-static.sh` produziu as quatro bibliotecas estáticas Windows x64 com NASM habilitado. Foi usada a versão 7.1 padrão desse script e a assinatura PGP do tarball da FFmpeg foi verificada pelo fingerprint publicado. O probe de ligação compilou um PE32+ x64 com referências reais às bibliotecas Windows e aos decodificadores estáticos. A tabela de importação confirmou SDL2, OpenAL, WebP, OpenGL, BCrypt e winpthreads. Esse probe só foi inspecionado. [Chave oficial FFmpeg](https://ffmpeg.org/download.html#releases) · [Pacote WebP MSYS2](https://packages.msys2.org/packages/mingw-w64-x86_64-libwebp).

Os quatro planos CMake intactos (núcleos US/JP do unificado e executáveis US/JP de desenvolvimento) configuraram e geraram arquivos Ninja com WebP e HD Video habilitados. Ao iniciar o build dos núcleos, o Ninja bloqueou no insumo `SLUS_004.47` para `pc_evt_entities.c` e no insumo `jp/SLPM_860.07` para `pc_battle_data.c`. Nenhum núcleo ou executável do jogo foi produzido. A fonte BIOS/KROM é outro insumo obrigatório em ambos os núcleos, registrada no grafo CMake. Está tudo registrado no [recibo de cross-build](vandal-cross-build-result-20261128.json).

Para reproduzir, use a revisão upstream fixada e um Linux x64 com CMake/Ninja/Python e GCC de host. Mantenha três prefixos separados no diretório de staging. O recibo registra as fontes exatas, versões e hashes. Extraia os pacotes Ubuntu no primeiro prefixo (`sdk`), exponha `gcc-posix` como `x86_64-w64-mingw32-gcc` dentro de `sdk/usr/bin`, e mantenha `sdk/usr/x86_64-w64-mingw32` como sysroot de busca. No segundo prefixo (`deps-final`), use a distribuição MinGW x64 oficial do SDL2, as entradas Win64 e os headers OpenAL e o pacote MinGW64 WebP da MSYS2. O terceiro prefixo recebe `libav` por meio do script upstream. Com `stage` e `source` apontando para caminhos privados, sem modificar a árvore upstream:

```bash
export PATH="$stage/sdk/usr/bin:$PATH"
SRC="$stage/ffmpeg-7.1" PREFIX="$stage/libav" \
  bash "$source/platform/pc/tools/build-ffmpeg-static.sh"
cmake -G Ninja -S "$source/platform/pc" -B "$stage/core-$region" \
  -DCMAKE_TOOLCHAIN_FILE="$source/platform/pc/cmake/toolchain-mingw-w64.cmake" \
  -DVH_MINGW_ROOT="$stage/sdk/usr/x86_64-w64-mingw32" \
  -DVH_MINGW_PREFIX="$stage/deps-final" -DVH_MINGW_FFMPEG="$stage/libav" \
  -DCMAKE_C_FLAGS=-O2 -DVH_REGION="$region" -DVH_UNIFIED_CORE=ON -DVH_BLOB=ON
cmake --build "$stage/core-$region" --parallel 6
```

Repita para `us` e `jp`. Quando a mídia original estiver disponível, use `-DVH_PSX_EXE` com o arquivo extraído da mídia e `-DVH_KROM_SOURCE` com a fonte local compatível. Os geradores originais continuam verificando o conteúdo. O terceiro estágio usa o mesmo toolchain, prefixos e otimização, com `-DVH_UNIFIED_CORES="$stage/core-us/core_us.o;$stage/core-jp/core_jp.o"` e sem as opções de núcleo individual. A ligação final e a execução permanecem pendentes dos dados legítimos.


## Extração da mídia e escopo regional

O procedimento de extração mantido pelo upstream usa `bchunk` na faixa MODE2/2352 para projetar os setores Form 1 de 2.048 bytes. Em seguida, usa `7z e` no ISO9660 para extrair `SLUS_004.47`. O mesmo procedimento foi exercitado para ambos os nomes, `SLUS_004.47` e `SLPM_860.07`, usando discos sintéticos produzidos localmente. O ISO reconstruído e o executável extraído conferiram byte a byte com suas fixtures. Os dois executáveis sintéticos tiveram SHA-256 `53ff184eab9631f73b3fcecc8946ba4cafac9527315b137d9104c9f81e0d94c6` e foram recusados pelos geradores oficiais. Nenhum executável PS-X legítimo foi testado. Um integrador pode derivar o arquivo diretamente do BIN já selecionado, sem solicitar o mesmo conteúdo novamente. [Procedimento upstream](https://github.com/HalmyLyseas/VandalHearts-PcPort/blob/14552fffa0e0b47e02b57592e274fc6e7a649923/.claude/skills/decomp-build/SKILL.md#the-base-game-files).

- Para o núcleo US, o executável extraído de SLUS-00447 precisa de MD5 `596bb082a2de5f1fe977dd3d7e160b03` e SHA-256 `351daaf337cdfd4c00e8abde694f6d0dcbc8b3dcd5e69a411f6d30b8446dfbb4`, conforme o verificador US upstream.
- Para o núcleo JP, o executável extraído de SLPM-86007 precisa de MD5 `53849277b08184863bd45f10925995a6`, conforme o gerador oficial. O disco Asia SCPS-45183 roda no núcleo US, mas traz uma identificação de save diferente no executável PS-X. A rota de build só reconhece o SHA-256 do executável US exato e não há variante Asia documentada para esse fim.
- Uma fonte adicional de caracteres do BIOS continua obrigatória. O gerador aceita KROMDAT compatível ou um BIOS de 524.288 bytes, lê a região de caracteres a partir de `0x66000` no BIOS e confere os hashes `19b1dd839020e62a8a0f6dfc673c320da36105d9bc9bbce876aa151b7bd927a7` (6.270 bytes, US) e `014313b691fa9caf95239400653ff61ca90fae8d481e79fa8fc571c7cdf13a86` (104.670 bytes, JP) para o binário unificado. Não foi fornecida mídia que satisfaça esses requisitos.
- O executável de desenvolvimento `VH_REGION=us` cobre Estados Unidos e Ásia no runtime, e `VH_REGION=jp` cobre Japão. Cada variante oficial usa os geradores da sua região com dados do seu próprio executável PS-X. Como substituto para o release, cada binário perderia o núcleo da outra região, a seleção unificada e a troca de disco entre regiões. Preserve o build unificado e solicite os dois BINs e uma fonte compatível de caracteres uma vez, caso essa rota avance. [Desenho do binário unificado](https://github.com/HalmyLyseas/VandalHearts-PcPort/blob/14552fffa0e0b47e02b57592e274fc6e7a649923/docs/building.md#the-unified-binary).


## REDRIVER2 7.4-rc2 e 8.0

- O ZIP Windows arquivado de 7.4-rc2 teve o SHA-256 conferido. As 76 entradas em `DRIVER2` coincidem por nome com as 76 entradas da árvore oficial revisionada.
- A árvore da pré-release 8.0 contém 81 entradas nesse diretório. As cinco adicionais são de `GFX/HQ`. Os 25 TIMs de `GFX/GAL` têm os mesmos nomes, tamanhos e IDs de blob nas duas revisões. O recibo [redriver2-8.0-data-tree-result.json](redriver2-8.0-data-tree-result.json) registra as revisões, a lista de blobs e o digest do ZIP Windows 8.0 divulgado pela API. O ZIP 8.0 não foi baixado nem executado.
- As contribuições upstream identificáveis incluem créditos, traduções alteradas pelo port, replays regravados e legendas. A inclusão da galeria foi feita em um commit separado, cujo histórico identifica 25 arquivos TIM adicionados, sem instruções para gerá-los com a mídia original ou declaração específica da origem e dos direitos. O código usa esses arquivos no menu de galeria. Retirá-los do kit alteraria a funcionalidade do procedimento oficial.
- O Launcher oficial e o roteiro manual convertem áudio e vídeo via jPSXdec a partir dos dois discos. As ferramentas OpenDriver2 documentam extração de texturas, conversão de imagens de interface e criação de cutscenes. Nenhuma dessas rotas documenta a reconstrução integral dos 25 TIMs da galeria. O suporte do runtime aos discos do usuário não resolve a procedência dos arquivos adicionais.
- O próximo passo verificável é encontrar a etapa oficial que reconstrói a galeria, ou confirmar a procedência e a licença desse subconjunto incluído no pacote. O teste completo com os dois discos também continua pendente.

A conversão de áudio XA foi repetida com Temurin 21.0.13.1+2 e os JARs do kit Windows 7.4-rc2, conferidos byte a byte por SHA-256 contra as entradas do ZIP. A mídia era a fixture sintética já registrada em `evidence-r18/after-1.5.31/redriver2-jar-evidence/fixture/synthetic.bin`, copiada para um caminho com espaços e acentos. A indexação e a conversão terminaram com código 0, a fixture permaneceu íntegra e o único WAV gerado tinha o mesmo hash do teste anterior com Java 17. Esta execução verifica o conversor de áudio e a compatibilidade de caminhos. Conversão de vídeo, instalação, galeria, primeiro boot e gameplay continuam sem validação nesta revisão.

```powershell
& $java -jar $jar -f $syntheticFixture -x $index
& $java -jar $jar -x $index -a audio -quality psx -af wav
```


Fontes upstream: [instalação oficial](https://github.com/OpenDriver2/REDRIVER2/wiki/Installation-instructions), [conversão do Launcher](https://github.com/OpenDriver2/Launcher/blob/e55540646e87a9de47d58ec9bae9a09271cb7d4b/setupwin.cpp), [introdução da galeria](https://github.com/OpenDriver2/REDRIVER2/commit/87a7d7783c40d4bb319b68b85cd17b8d9ff0c653), [carregamento dos TIMs](https://github.com/OpenDriver2/REDRIVER2/blob/acca6b139302dd72c1fbff52556f3493aafda2dd/src_rebuild/Game/C/E3stuff.c), [ferramentas upstream](https://github.com/OpenDriver2/OpenDriver2Tools/blob/master/README.md) e [pré-release 8.0](https://github.com/OpenDriver2/REDRIVER2/releases/tag/8.0).

Para reproduzir a comparação de metadados, consulte os endpoints GitHub `/repos/OpenDriver2/REDRIVER2/git/trees/{revision}?recursive=1` para as duas revisões do recibo, conte os blobs sob `data/DRIVER2/` e compare os itens sob `data/DRIVER2/GFX/GAL/` pelos campos `path`, `size` e `sha`. O ZIP local pode ser conferido com `Get-FileHash -Algorithm SHA256` e `tar -tf`, comparando as entradas de arquivos sob `DRIVER2/` com as da árvore versionada.
