# Revisão dos handlers de mídia, release e launcher

Fonte: snapshot textual verificado do Desktop `921295de12349e726f7ca21a5edd8a8ecee123d8`. GetAll `ceaa962fe1a2088a7f3900509b856743ff4b6672`. Esta revisão não executou jogos, compiladores ou instaladores. Os únicos arquivos criados estão na pasta desta auditoria.

## Cobertura que esta fatia sustenta

O inventário leu as 145 receitas completas, conferiu seus hashes contra o índice e reconciliou 142 IDs implementados com os 148 IDs do catálogo. A matriz `service-routing-review.json` tem uma entrada por receita e uma entrada por cada um dos 148 IDs, inclusive os seis sem receita. Cada entrada aponta método, arquivo, linha e commit. Os dois aliases de launcher/release que não seguem o build principal são tratados separadamente; os dois perfis MKW também permanecem distintos.

Os corpos de preparação/lançamento dos handlers simples e os dispatchers compartilhados foram lidos. Isso cobre 111 rotas de receita nesta fatia. As 34 rotas de receita de build têm despacho e contrato identificados, mas revisão de corpo atribuída explicitamente aos outros revisores. A ausência de arquivo `.patch` não foi usada para concluir ausência de alterações.

Não foi identificada, nos corpos dos handlers simples lidos, uma implementação local destinada a inventar partes ausentes de gameplay. Essa observação é limitada aos métodos de integração lidos. Há transformações reais de código/binário, adapters próprios e escolhas de recursos; elas estão discriminadas abaixo. Nenhum release fica certificado como completo ou jogável por essa observação.

## `Completed` não certifica primeiro boot

`GameInstallationPreparedBuildTransaction.cs:24-49` executa o callback de preparação, valida formato/contrato do executável ou Java, registra manifesto e publica os arquivos com `Verified=true` e `Completed`. Não há teste de gameplay nesse caminho. O texto padrão do método inclusive declara que o primeiro boot não foi homologado.

No caminho genérico, `GameInstallationService.cs:646-810` aplica operações de entrada/cópia/diretório, confere arquivos requeridos e só retorna conclusão quando `manual_steps` está vazio. Isso prova atendimento ao contrato de arquivos, não que o runtime esteja completo. Os aliases **SM64Plus `LauncherMirror`** e **CTR Turbocharged `ci-07d0c49`** têm `manual_steps`; o caminho genérico não os transforma automaticamente em jogo homologado. As instruções de usar o launcher são apenas instruções da receita, não um boot observado nesta auditoria.

`GameInstallationPreparationResume.cs:183-188` rejeita kits desconhecidos ou inelegíveis. O último fallback em `260-302` preserva a preparação parcial e registra seleção de mídia; não promove um projeto desconhecido para `Completed`. Os caminhos reconhecidos podem concluir após validação estrutural, sem executar a partida.

Há uma inconsistência de classificação: `ForzaInnoProfile` tem retomada em `256-298`, que chama `StageForzaCompilerInputs` e então `BuildForzaGame` (`GameInstallationForzaXex.cs:144-204`), mas não aparece em `CanCompletePreparation` (`18-38`). `StoreAddonProviders.cs:137-143` calcula rank 1 para esse perfil. Isso contraria uma interpretação uniforme dos 142 como rank 2; não foi demonstrado que bloqueie o botão na UI.

## Alterações próprias e transformações que precisam ser declaradas

| Projeto/fluxo | Operação observada | O que essa evidência permite concluir |
| --- | --- | --- |
| Zelda 3 Launcher e Super Metroid Launcher | `CompileRadzLauncher`, `GameInstallationRadzLauncher.cs:117-141`, compila as fontes oficiais fixadas com TCC e passa `STBI_NO_SIMD=1` e `SYSTEM_VOLUME_MIXER_AVAILABLE=0`. | Há escolha local de configuração de build, incluindo desativação do caminho de integração do mixer do sistema. Não é uma simples extração de launcher. Não se observou reescrita de lógica de gameplay nesse método. |
| Severed Chains | `GameInstallationSevered.cs` gera uma pequena classe Java `AllFixSeveredUnpack`, que registra listener e chama `legend.game.unpacker.Unpacker.unpack()` do JAR oficial. | Adapter próprio para chamar o extrator existente; não reescrita do JAR/gameplay. |
| King's Field | `Tools/NativeExtractors/build-kingsfield-import.ps1` coloca guarda em `NOMINMAX` de `translation_ppf.cpp` e usa `english_patch.py embed --optional` para gerar include vazio de tradução; `kingsfield-import.cpp` chama `kf::disc_extract` em japonês. | Há edição de fonte de helper e escolha de idioma. Não cabe chamá-lo de absolutamente intocado. Não implementa gameplay faltante. |
| re:Blue | `BuildReBlueBootIni`, `GameInstallationReBlue.cs:90-116`, une os idiomas originais e reescreve `[Language]`, `[Voice]`, `[MovieVoice]`; `176` grava o INI derivado. | Mudança explícita de configuração do conteúdo importado, baseada nos três discos. Não é alteração do runtime Windows. |
| GT4 | `GameInstallationGt4.cs:84-87` normaliza caminho no recibo; `153-162` limpa variáveis herdadas e seleciona renderer `hw`, CoreGS `2` e cache. | Configuração local de execução. O helper externo foi inspecionado em auditoria complementar; o seu hash sozinho não provaria ausência de alteração. |
| Unleashed | Wrapper `unleashed-xex-patch.cpp` no ZIP de fontes recebe base e atualização originais, verifica hashes aceitos e chama `XexPatcher::apply`; cria `patched/default.xex`. | Adapter próprio e aplicação real do Title Update original. Os seis arquivos-chave de implementação/patcher comparados são idênticos às revisões oficiais fixadas; o binário não foi recompilado nesta auditoria. |

As opções de DKB, Pinyon, MKDD e os patches dos demais builds são cobertas nos relatórios de source-build. Esta tabela não substitui sua revisão.

## Geração ou patch oficial não é sinônimo de jogo criado pelo AllFix

**Mega Man Legends Modernization.** O plano incorporado `Tools/VerifiedPatches/mml-v0.9.6-beta.json` foi comparado integralmente ao `src/patch_manifest.py` oficial em `09b8dd326e009e895635e6516ac73e5709db0aec`. Os dois perfis US/JP têm 121 ranges, 247 bytes alterados e 512 bytes de cauda cada; todos os campos, offsets, bytes, tamanhos e hashes de entrada/saída coincidem. O blob original foi verificado como `b300621c88e1573371f9c91c128981be7e36c55e`. O código aplica o patch a uma cópia em staging. Isso é uma modificação binária real de origem upstream, não preenchimento local de partes faltantes do jogo. Reprodução: `verify_mml_parity.py`; evidência: `mml-parity-review.json`.

**Sonic Adventure.** `GameInstallationSonicContent.cs` prepara a imagem de RAM esperada usando o delta oficial `bootstrap.xor.z`; não é cópia simples. O fluxo verifica manifesto e hashes finais. A presença desse delta oficial não comprova gameplay nem que o AllFix tenha escrito o conteúdo transformado.

**The Last Guardian e inFAMOUS Second Son.** `GameInstallationLinkedPs4Ports.cs` usa cinco scripts upstream por título, fixados por hash, incluindo `tlg_patches.py`/`infamous_patches.py` e `isa_rewrite.py --red-zone`. São procedimentos reais de patch/reescrita derivada do port oficial. O C# não contém substitutos de gameplay; a fonte oficial executada precisa continuar identificada como origem dessas transformações.

**Golden Sun.** O handler invoca o `gsr_builder.exe` oficial com ROM e diretório de trabalho, exige marcador de conclusão e confere o registro da engine/biblioteca. **OpenGOAL** invoca o extrator oficial com `--extract --validate --decompile --compile` e verifica os arquivos CGO. **KnowYourRole** usa a CLI construída das fontes oficiais para gerar assemblies gerenciadas. São exemplos em que o launcher/gerador oficial faz mais que extrair arquivos.

**Wind Waker HD.** A integração chama `tools/installer/setup.py` do pacote oficial, com `--no-decomp --code-mods 0 --skip-shader-prebuild` e demais opções locais. Ela rejeita `placeholder_code:true` no recibo e exige o executável Windows e dependências. Isso evita aceitar o placeholder declarado por esse instalador, mas não prova primeiro boot nem completude do upstream.

**Outros Xbox.** NG2, Downpour, PGR4 e Edge of Time importam atualizações originais verificadas. Dead Rising Case Zero/West chama comandos do executável oficial para extração, geração de shader cache e overlays, em vez de gerar essas implementações no C#. Os nomes dos comandos e validações constam nos métodos da matriz.

## Unleashed: proveniência de fonte verificada, sem reproduzir o binário

O ZIP de fontes versionado tem 248.867 bytes e inclui wrapper, build, provisionamento, testes e dependências. Foram lidos integralmente `BUILD.md`, `CMakeLists.txt`, `provision.py`, `unleashed-xex-patch.cpp`, `msvc-byteswap.h` e o teste de carregamento de DLL. O shim MSVC é injetado por `/FI`; não reescreve o arquivo do patcher.

Foram obtidas novamente das revisões oficiais e comparadas byte a byte seis entradas: `XenonUtils/xex_patcher.cpp`, `xex_patcher.h`, `memory_mapped_file.cpp`, `libmspack/mspack/lzxd.c`, `aes.c` e `xxhash.c`. **Todas coincidem.** As URLs, hashes, tamanhos e o manifesto de todo o ZIP estão em `unleashed-helper-review.json`; a verificação offline e a opção de repetir downloads estão em `verify_unleashed_source_manifest.py`.

Essa comparação cobre as implementações-chave explicitadas e não é comparação binária de uma compilação reproduzida. A afirmação de reprodução no `BUILD.md` é evidência histórica, não uma execução desta auditoria. Não foi processado XEX/TU de um jogo para este resultado.

## Fronteira de helpers e origem de release

Os handlers de Torch, ZAPD, Nectar, BlueWake, Picori e GT4 chamam binários fixados por hash. O hash prova que se usa o artefato escolhido, não que esse artefato corresponda sem alterações a todo seu upstream. A matriz marca esses fluxos separadamente como **release + helper não recompilado nesta fatia**; fontes e transformações disponíveis são assunto da auditoria complementar de NativeExtractors. O mesmo limite vale para ferramentas oficiais pré-compiladas como `jpsxdec.jar`, `PT.PkgExtract.exe` e os geradores de launcher.

Para os releases que apenas importam/copiam mídia, a categoria é precisamente **“nenhuma edição de source/runtime observada nas instruções do instalador lidas”**. Ela não afirma que o upstream é completo, que seus binários foram todos reconstituídos ou que o jogo abriu de fato.

## Os seis sem receita e as alegações de launcher

São `doldecomp-mkdd-decompilacao-base`, `mml1-megaman-legends-decomp`, `project-2099`, `tmc-decompilacao-base`, `twilight-princess-courage-reborn` e `wind-waker-recomp`. Não existe rota de receita para esses IDs no índice auditado. As três bases de decompilação para console não foram convertidas em ports Windows por uma receita. Wind Waker antigo tem relação de sucessão com BlueWake, já contado. A presença de um instalador público de Project 2099 não confirma que ele obtenha runtime ou solicite ROM; Courage Reborn também não teve funcionamento do launcher confirmado. A auditoria não deve repetir essas expectativas como fatos.

O número inicial de 114 era um estado herdado de implementação. O índice preserva somente uma homologação histórica, SM64CoopDX, baseada em relato do usuário. Não há evidência para reinterpretar 114 ou 142 como número de jogos testados em gameplay.
