# Rodada 18 — checkpoint de desenvolvimento contínuo, 24/11/2026

## Base e resultados efetivamente demonstrados

- GetAll base bfe35f82c6a5d264d3c7b498dc639c98febbdbeb; receita atual 028745e1c015428135c3281e58df6de4ef13edc0.
- Desktop base 272a97821fd693e7ae056f2d700746e64a46426c; atual 930d4be203a25bc703d26f7252ab1f21bdef241f; SDK 1.5.8, Desktop 3.0.0.
- Catálogo oficial atualizado: 110 jogos, 145 projetos, Leonida removido. 125/145 antes; 128/145 após. 129 receitas; 1 validated histórico. Nenhum ID modificado nem receita anterior removida.
- 3 receitas novas (SM64ex, Render96ex, SM64RT), v5 experimentais. Fontes oficiais revisões e SHA-256 fixados no código. 3/3 preflights reais aprovados duas vezes: compilação ferramentas upstream, link de fixture SDL2 em PE x64, verificação de arquitetura, rejeição da ROM falsa pelo extrator oficial. Não são jogos compilados. Fluxos Make, extração, link, saída, registro e recuperação escritos, caminho positivo sem ROM genuína não demonstrado; packs opcionais de Render96 não integrados. Toolchain Docker offline no build, imagem local ID sha256:3d9acbf002a2c662a17fd77cf86346b5a49ab76b17a984064f0587466138b4f8, importação local fixada por hash. Docker Desktop compatível necessário; não foi publicada distribuição da imagem.
- DKB 0.5.1+44ba6b1: pacote oficial, SHA256 7f70832c141e63ff3c3d060140e3d48bc503c51576457ae2ac51ee444886c73d, árvore completa 7128 arquivos/471403139 bytes pin c962e427690517a3cd3fbce765f7b09fd7201c22d4185e73ed7174195973ca38. Integração CLI verificada no NUP falso: saída upstream missing NUP magic, nenhum launch/estado completo, original e kit preservados. CLI fechada, cópia mídia, opções FSR4/DLSS e update desativadas, validação final e registro/reversão codificados; não demonstrados com mídia genuína. Retry reaproveita kit, não reaproveita etapa parcial de compilação; progresso por fase. Não é sandbox de rede nativo. Não contar jogo como instalado.
- 39 preparações reais portáteis novas; 1 pacote adicional SM64CoopDX validado em teste negativo com diretório isolado. 40 pacotes oficiais verificados (não 40 instalações). Evidências: R18-EVIDENCIAS-PORTATEIS.json. Teste de staging simples inicial do CoopDX não se aplica a receita que exige entrada; substituído por teste negativo específico, não alteração da receita homologada histórica.
- Consentimento explícito WPF antes de processamento de perfis de build; restrições de execução anteriores mantidas. Interface visual ainda não homologada: UAC requer ação do usuário.

## Testes

345 PASS C# (suite), parser C# 129/129, 44 testes Python, jsonschema/paths/SHA256 129/129, JS regressões aprovadas inclusive 9 novos casos SM64; 3 preflights reais SM64, DKB negativo, CoopDX negativo, 39 preparações portáteis. Nenhuma instalação completa, jogo integralmente compilado, boot ou homologação nova. Evidências anteriores permanecem no histórico e matriz. CI público do commit de receitas #53 aprovado; Windows CI aponta exatamente para 028745e1c015428135c3281e58df6de4ef13edc0. GetAll CI #54 (45326524918) e Windows CI #4 (45326406164) aprovados nos commits c3500d29d7f146769b92fd16fbf9541e734ef043 e 930d4be203a25bc703d26f7252ab1f21bdef241f; somente documentação posterior não muda o código testado. Publicação Release x64 self-contained a partir de clone remoto limpo.

## Artefatos locais

- C:\Users\bradg\Downloads\GetAll-R18\publish-final\AllFix.exe
- 77537340 bytes; SHA-256 18892d2b0c26809b4a075ddb465d2f7746fc709c367dfff84d5c7d6da6dbeba8
- C:\Users\bradg\Downloads\GetAll-R18\publish-final\Toolchains\allfix-r18-mario.tar
- 278564864 bytes; SHA-256 73d248d9e49b4132aad9d720e956addbf688fcff89ca294541f395a98577080d
- Não publicar imagem nem executável; nenhuma mídia comercial.

## Classificação de pendências

17 IDs sem receita: burnout3-recomp, doldecomp-mkdd-decompilacao-base, drmario64-recomp, god-of-war-recomp, gt5-recomp, hookshot-zelda-oot-port, metaforce, mkdd-recomp, mml1-megaman-legends-decomp, project-2099, sonic-1-forever-sonic-2-absolute, strikers-wiicompiled, strikersrecomp, tmc-decompilacao-base, twilight-princess-courage-reborn, wind-waker-recomp, wipeout-rewrite.

| ID | Próxima decisão / ação |
|---|---|
| gt5-recomp | Implementação de pipeline real PS3Recomp/codegen, dependências fechadas, validação de mídia e build; launcher prévio não é jogo. |
| burnout3-recomp | XboxRecomp, pipeline real, código de saída e runtime; launcher prévio não é jogo. |
| god-of-war-recomp | PS2Recomp, extração SCUS-97399, dependências e compilação real. |
| drmario64-recomp | Autor descreve teste técnico sem intenção de release; não duplicar Plus; decidir classificação com responsável pelo catálogo. |
| strikersrecomp | Build documentado macOS e dependências relacionadas; falta caminho Windows demonstrado. |
| strikers-wiicompiled | Build Windows não testado upstream; fechar LLVM/CMake/Ninja/.NET e validação DOL. |
| mkdd-recomp | Projeto alternativo CISO/Ghidra/Rust, não confundir com MKDD ethannicholas. |
| wipeout-rewrite | Auditoria de autorização dos assets derivados; não redistribuir, se possível criar build sem esses assets. |
| wind-waker-recomp | Migrou para BlueWake, já coberto; solicitar classificação/unificação ao catálogo. |
| doldecomp-mkdd-decompilacao-base | Base de decompilação, não port independente. |
| tmc-decompilacao-base | Base GBA, não port PC independente. |
| mml1-megaman-legends-decomp | Decompilação PS1, não port independente. |
| hookshot-zelda-oot-port | Upstream Forgejo indisponível em verificação anterior; autorização/proveniência de espelho não estabelecida. |
| twilight-princess-courage-reborn | Distribuição Windows oficial verificável não estabelecida. |
| metaforce | Endpoints históricos indisponíveis; nova distribuição oficial não confirmada. |
| sonic-1-forever-sonic-2-absolute | Dois produtos distintos; validar distribuições e classificação sem alterar ID arbitrariamente. |
| project-2099 | Payload não autorizado/verificado quanto à redistribuição; bloqueio externo até comprovação. |

### Kits v9 (15)

MML, Sonic Adventure e Forza: fluxos anteriores preservados, mídia positiva não homologada. Bananza: novo caminho fechado descrito acima. Restantes ainda com trabalho de desenvolvimento, não apenas impedimento externo: God of War (v9), Tears of the Kingdom, Pinyon Shift, DOAX Volleyball, SSX, Link's Awakening, GTA Stories, RyGT GT7, SpartanPort, Odyssey, Mario Kart World. Odyssey CLI inspecionada; não relaxar mitigação de segurança; elaborar solução compatível. TotK: CLI e dependências fixadas, seleção de mídia base/update e arquivos locais necessários. MKW/LAS: caminho de preparação headless ainda não validado. SSX: não aceitar licença VS automaticamente; perfil separado. Não marcar como concluídos.

### Próxima tarefa executável, mesma Rodada 18

1. Consolidar uma família de recompilação Windows com scripts upstream fixados e testes reais: iniciar GT5 pelo fluxo de código-fonte PS3Recomp já identificado no histórico, sem executar instalador BAT arbitrário; alternativamente Burnout XboxRecomp; integrar perfil fechado, dependências, validação e output.
2. Em paralelo, prosseguir kits v9: TotK e SSX, usando a infraestrutura de CLI/manifesto/restrições. Executar fixtures de toolchain e preflight antes da mídia legítima. DKB: completar teste positivo e retomar fases intermediárias, progress reporting e teste de versão ExeFS.
3. Continuar campanha de releases ainda sem evidência em COBERTURA-R18.md; testar caminhos que exigem mídia em diretório isolado, não confundir staging com instalação.
4. Resolver classificação dos não instaláveis com agente do catálogo; manter 17 IDs até decisão externa. Rever as fontes bloqueadas sem usar espelhos não autorizados.
5. Homologar WPF/consentimento/cancelamento/biblioteca e boots quando houver mídia legítima; abrir o novo AllFix.exe e autorizar UAC normalmente, sem substituir a instalação. Verificar CI e preservar este checkpoint antes de qualquer alteração posterior.

Esta é a mesma Rodada 18, desenvolvimento ainda não concluído. Sem merge, release, alteração do version.json público, DownloadAll ou mudança de versão Desktop.

## Insumo já recuperado para continuidade TotK

ZIP oficial TotK-Setup-0.5.0-windows.zip baixado em GetAll-R18/totk, 168127049 bytes, SHA256 201b08348ffb72c70570eba8f92f67d31bc611b5aff4b0de09756259e0c95a7d. Árvore: 6940 arquivos, 646931453 bytes, manifesto canônico SHA256 9b12cf5eb7cd04a57b8cd02f1611f068cf81280a6f8a61d6db4d33c3ef846fa5. VERSION 0.5.0+afae80c9. CLI real possui --base, --update, --keys, --lang, --dest, --root, --temp, --verify; NÃO incluir --dlss. Ferramentas, libs runtime v2/v3, VMA e hactool incluídos. Etapas check, kit, fonts, extract, lift, compile, prepare, pc_prompts, shapes, dlss, cleanup. Estado registra inputs/steps, não conteúdo de chaves. Chaves originais somente via seleção local efêmera, não armazenar ou transmitir chaves/hashes no estado ou telemetria; limpar staging e cópias temporárias de merge em falha. Validar dados finais contra expected-v1.1.0/1.2.1/1.4.3.json e exe_sha256/xlate_sha256, build-kit pinado, sem DLSS nem atualização automática. Ainda não integrado nem executado pelo motor nesta sessão; não repetir download ou auditoria. Esta é tarefa de desenvolvimento, não bloqueio exclusivamente externo.

## Estado atual da missão contínua — 24/11/2026

Este trecho substitui as pendências antigas de TotK, GT5, Burnout e Bananza sem apagar as evidências históricas. SDK 1.5.9; Desktop 3.0.0. Catálogo 110 jogos/145 projetos, 130 cobertos (89,66%), 131 receitas (130 experimentais/1 validada histórica), 15 IDs sem receita, 15 kits v9.

- TotK: commit privado 3fa268b691c5bfa8eb23aec4d3404105bbaaefff. GameInstallationTotkBuild.cs integra CLI oficial 0.5.0, seleção efêmera .keys, cópias verificadas base/update, parâmetros fixos, progresso sanitizado, cancelamento, limpeza, verificação dos hashes oficiais de ExeFS/RomFS e saída PE, registro apenas após verificação. TOTK_OFFICIAL_NEGATIVE_PASS em totk-engine.txt: CLI rejeitou chaves sintéticas, originais preservados, nenhum caminho/conteúdo de chave no estado ou progresso, staging limpo. Caminho positivo não executado. Retomada reaproveita kit, reinicia etapas. Logs transitórios upstream ficam na árvore de trabalho; não afirmar sandbox de rede ou ausência comprovada de qualquer registro interno.
- GT5: receita build-64ca169. GameInstallationConsoleBuild.cs/StoreTrustedConsoleBuild.cs: fonte fixada 64ca1697c5f9bb513bfe0414d9a36c10dafd0a37, toolkit PS3Recomp 4e8f3ca87a3e1d87bb83b8b7e9348fe2685cd514, patch oficial, dependências pinadas, Python/wheels, CMake/LLVM/Ninja, FFmpeg oficial. Seleção PS3_GAME v01.00 BCES00569/BCUS98114, ELF já extraído com SHA-1 oficial, dev_flash legítimo; junção GT.VOL segmentada em staging. Etapas PPU/SPU, CMake, link e PE verificado implementadas. CONSOLE_RUNTIME_PREFLIGHT_PASS no gt5-engine-final.txt: patch, imports, ferramentas e runtime real compilado (ps3recomp_runtime.lib 7507354 bytes). Jogo completo não compilado. Extração de ISO PS3/SELF/PUP não automatizada; não tratar como bloqueio exclusivamente externo.
- Burnout: receita build-3c85ed7. Fonte 3c85ed7777886f4a8f805cb243b123b1b82cf375, XboxRecomp afeb69fe482930f5ccbb5d348740636807fe0784, ISO XDVDFS/pasta, verificação XBE NA (Title ID/certificado/tamanho; SHA oficial não localizado), cinco etapas upstream de geração, CMake/MSVC, link, saída e registro transacional. CONSOLE_RUNTIME_PREFLIGHT_PASS em burnout-engine.txt: XBE fixture oficial processado, ISO falsa rejeitada, xbox_kernel.lib 1540608 bytes compilada. Não é jogo completo.
- Bananza: GameInstallationDkbBuild.cs retém somente fase de dados verificada, com ResumeWorkId, identidade da mídia e manifesto, descarta código/exe/cache de compilação parcial, mantém opções opcionais desativadas, progresso real da CLI. DKB_OFFICIAL_NEGATIVE_PASS em dkb-resume-engine.txt: NUP inválido, ExeFS/RomFS inválido, kit e originais preservados, limpeza. Retomada de checkpoint positivo ainda não comprovada com mídia real.
- Regressões: 363 PASS C#, parser 131/131, JSON Schema/hashes/catálogo 131/131, Python 44/44, JS PASS; build WPF Release x64 0 erros/avisos. Nenhuma nova instalação completa, build integral de jogo, boot ou homologação. Os dois runtimes são bibliotecas, não executáveis de jogo.
- Commit receitas 714cec7f6bfa176ae69986be77c1b8aa23c175f8; privado ec016409f8aebfe45092aecffb0b701045687d4e com CI fixado ao commit exato das receitas. PRs permanecem abertos, sem merge.
- Executável de clone limpo: C:\Users\bradg\Downloads\GetAll-R18\publish-r18-current\AllFix.exe, 77562551 bytes, SHA256 194857b27c23ff2cb9aa9060d27c0a30bcfb3400c795ff69924af7707bc016d0. Toolchains/allfix-r18-mario.tar copiado e hash conferido 73d248d9e49b4132aad9d720e956adbf688fcff89ca294541f395a98577080d; provisionamento em outro Windows ainda não demonstrado.

### Retomada executável — mesma Rodada 18

Workspace C:\Users\bradg\Downloads\GetAll-R18, clones desktop/getall, cache console-cache e console-source, pacotes anteriores GetAll-R16-20261123/range-packages. Não repetir auditorias ou downloads verificados.

1. Próxima implementação: LAS v0.6.1, kit já verificado em range-packages/lasrecomp. A distribuição traz lasgen/lasgen.exe, zig/zig.exe, gamelib-src/gamelib_entry.c e lasrecomp.dll.a. README confirma build local pelo setup, sem CLI de preparação documentada. Identificar no código upstream exato os argumentos do gerador e do linker e o contrato de saída, executar help/fixture do gerador após verificar a árvore, implementar novo perfil fechado em Services (reusar GameInstallationTotkBuild.cs e GameInstallationDkbBuild.cs para staging/registro, GameInstallationPreparationResume.cs para despacho). Adicionar teste em Tests/AddonInfrastructure/Program.cs e integração específica, depois dotnet build Tests/AddonInfrastructure/AddonInfrastructure.csproj -c Release -o ../harness-las. Não executar launcher arbitrário ou aceitar licenças.
2. SSX (launcher minúsculo, dependências externas), Pinyon (fonte embutida, ReXGlue), DOAX (tools/build_game.py e extract_iso.py), God of War (ps2_recomp/ps2-tools), GTA Stories (tools/build.py), RyGT/SpartanPort, Odyssey e MKW: completar pipelines individuais e fixtures, sem desativar proteções. São pendências de desenvolvimento; não classificá-las como externas apenas por falta de mídia.
3. Para GT5/Burnout: com mídia legal, rodar ResumeConsoleSource e BuildConsoleGame em GameInstallationConsoleBuild.cs até codegen/link/registro e corrigir defeitos reais. Regressão --console-source-build com receita/ZIP/cache e diretório isolado já aprovada, não repetir sem mudança. TotK: teste positivo CompleteTotkPreparation e ValidateTotkOutput. Bananza: teste positivo KeepDkbDataPhase, cancelamento após fase de dados e retomada. SM64: validar importação do tar fixado em Docker Windows limpo, packs Render96.
4. Restantes 15 IDs: god-of-war-recomp, strikersrecomp, strikers-wiicompiled, mkdd-recomp, wipeout-rewrite exigem desenvolvimento/proveniência conforme tabela anterior. Cinco IDs de distribuição bloqueada e cinco de classificação ainda pendentes; informar responsável pelo catálogo, sem eliminar IDs.
5. Teste visual WPF: usuário deve abrir publish-r18-current/AllFix.exe e aprovar UAC, sem substituir instalado. Testar controles, operação longa/cancelamento, biblioteca e retomada.
6. Validação após alteração: dotnet build Tests/AddonInfrastructure/AddonInfrastructure.csproj -c Release -o ../harness-next; dotnet ../harness-next/AddonInfrastructure.dll; dotnet ../harness-next/AddonInfrastructure.dll --parse-getall ../getall ../parser-next.json; node --test Tests/StoreSearch/search.test.cjs; validar receitas no GetAll, CI privado fixado ao commit de receitas, publish limpo. Não publicar releases, version.json, merge ou DownloadAll.
