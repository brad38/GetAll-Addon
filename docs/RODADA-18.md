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

345 PASS C# (suite), parser C# 129/129, 44 testes Python, jsonschema/paths/SHA256 129/129, JS regressões aprovadas inclusive 9 novos casos SM64; 3 preflights reais SM64, DKB negativo, CoopDX negativo, 39 preparações portáteis. Nenhuma instalação completa, jogo integralmente compilado, boot ou homologação nova. Evidências anteriores permanecem no histórico e matriz. CI público do commit de receitas #53 aprovado; Windows CI aponta exatamente para 028745e1c015428135c3281e58df6de4ef13edc0. Estado atual dos workflows deve ser verificado na retomada (runs do commit de código e do commit final). Publicação Release x64 self-contained a partir de clone remoto limpo.

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
