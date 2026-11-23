# Checkpoint de manutenção — GetAll-Addon | Rodada 9 (2026-11-23)

## Estado confirmado do repositório

- **Repositório de escrita:** brad38/GetAll-Addon. Catálogo brad38/AllFix-Repo, AllFix.exe, AllFix.dll e SDK 1.3.0 foram consultados apenas em leitura.
- **Base da branch:** a main contém o merge do PR #8, commit 4960e2a2f375fa8b929cf12f54770d65f183c1c9. PRs #1 a #8 integrados. O PR #8 não deve ser reaberto nem mesclado novamente.
- **Branch exclusiva:** feat/round-9-sdk13-coverage, derivada desse commit. **Integração:** proposta para revisão, sem merge automático.
- **Catálogo oficial:** 87 jogos / 119 projetos. **main após PR #8:** 90 receitas (73 v3, 17 v5), sendo 1 validated e 89 experimental. **Proposta da Rodada 9:** 90 receitas (72 v3, 18 v5), 1 validated, 89 experimental e 29 projetos sem receita.
- **Limite de evidência:** aprovações de schema, parser e testes com arquivos sintéticos não constituem homologação funcional. A única receita validated permanece sm64coopdx v1.5.1.

## Entregas da Rodada 9

| Projeto | Situação anterior | Alteração | Estado de publicação |
|---|---|---|---|
| crash-team-racing-high-octane (v.1.5) | v5 experimental, ROM exigia cópia manual | import_input (installation) de BIN NTSC-U 926, SHA-256 f780bf2331476aabfc00772fa758b12dd95ebfbc907968132cbd3cdd4e2c07c0 e 605698800 bytes; destino assets/ctr-u.bin | experimental, aguarda PR / boot real |
| ggarecomp (v0.3.0) | v3 experimental, seleção manual da ROM | Migração para v5: import_input local_app_data/GGARecompiled/gga.us.z64, SHA-1 9f9e860816f9e2a68bb5f4f56086e0c7450c64d7, magic 80371240; manual_steps de configuração preservado | experimental, aguarda PR / boot real |

Nenhum novo projeto foi adicionado: 29 ausentes permanecem bloqueados após consulta às releases dos 26 repositórios GitHub e reexame das 3 fontes externas. A matriz individual e os critérios estão em [RODADA-9-SDK13-2026-11-23.md](RODADA-9-SDK13-2026-11-23.md).

## Evidências técnicas reproduzíveis

- **High Octane:** ZIP oficial ctr-high-octane-x64.win.zip, 2403121 bytes, SHA-256 005924af516a3cb2bcdc19269422e2de77719600656e5b00df45424fe081693e; apenas o EXE e assets/dualshock.png. README oficial especifica assets/ctr-u.bin; CTR Native (base upstream) publica perfil NTSC-U 926 e SHA-256 do BIN.
- **GGARecomp:** ZIP oficial GGARecompiled-v0.3.0-windows.zip, 40258542 bytes, SHA-256 19c8e7fd7a009e48675742a6af453a8e7e8934adac4a4d7f0fa41bb084241e3c; 4/4 required_files presentes, sem ROM. README oficial informa %LOCALAPPDATA%/GGARecompiled, fonte oficial comenta nome gga.us.z64.
- **Validação JSON/índice:** scripts/validate_recipes.py --strict-lf --require-jsonschema --check-git-blobs --check-catalog passou em 90/90.
- **Regressão Python:** python -m unittest discover -s tests -v, 18/18 testes aprovados (16 anteriores, 2 novos).
- **Parser real SDK 1.3.0:** AllFix.dll compilada: RemoteRecipeCatalog.ParseIndex e StoreAddonProviders.ParseRecipe aceitaram 90/90; harness independente 48/48 assertivas, incluindo SHA-1/SHA-256, cabeçalho, comprimento e rejeição de alterações em arquivos sintéticos.
- **Não realizados:** execução dos jogos com cópias comerciais legítimas, first boot, instalação funcional com ROM real; nenhuma nova promoção a validated.
- **GitHub Actions:** verificar o resultado da execução associada ao commit final do PR da Rodada 9 antes de qualquer decisão de merge.

## Bloqueios e prioridades de próxima rodada

1. **Pacotes instaladores, executáveis avulsos e múltiplos assets:** exigir modelo de artefato explícito, hashes, pós-condições e rollback. Um instalador copiado não é um jogo instalado.
2. **Launchers Java/JAR de Severed Chains:** comando restrito, JRE declarado e boot auditável sem aceitar .bat arbitrário.
3. **Arquivos tar.gz:** extração segura e correção da identidade de Project Picori no catálogo oficial (aqui, apenas documentação).
4. **17 projetos sem binário Windows final:** aguardar release oficial pronta, ou especificar pipeline de compilação estritamente controlado para o Codex; não executar scripts de terceiros via addon.
5. **ROMs arcade Cannonball:** import_input_set atualmente rejeita extensões numéricas oficiais (.88, .76, etc.) e não suporta os CRC32 publicados no código; demanda contrato de arquivos verificáveis e nomes exatos.
6. **Novos destinos de import_input (.sfc/.smc/.gba) e validação de first_run_files em perfis multinível**.

Detalhes de contratos e testes de regressão estão em [ESPECIFICACAO-CODEX-SDK.md](ESPECIFICACAO-CODEX-SDK.md). O guia de seleção de mídias foi atualizado em [HOMOLOGACAO-MIDIA-NECESSARIA.md](HOMOLOGACAO-MIDIA-NECESSARIA.md) (prioridades propostas: 7 + 16 + 66).

**Próxima ação:** revisão do PR da Rodada 9 e homologação posterior com mídias legítimas pelo proprietário; nunca fazer merge automático.
