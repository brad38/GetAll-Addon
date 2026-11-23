# Checkpoint — GetAll-Addon Rodada 10 (2026-11-23)

**Base:** main 6f3c9cb1cd6403b521a9b6c2229272cc6661a6d7 (PR #9 merged).
**Branch:** feat/round-10-sdk14-recipes, derivada da main; nenhum merge automático.
**Repositório modificado:** somente brad38/GetAll-Addon. Nenhuma DLL, AllFix.exe, SDK, catálogo AllFix-Repo nem ZIP universal foi alterado.

## Estado verificável

| Indicador | Main após PR #9 | Proposta Rodada 10 |
|---|---:|---:|
| Jogos / projetos | 87 / 119 | 87 / 119 |
| Receitas indexadas | 90 | 91 |
| v3 / v5 / v6 / v7 | 72 / 18 / 0 / 0 | 70 / 17 / 1 / 3 |
| validated / experimental | 1 / 89 | 1 / 90 |
| Projetos ausentes | 29 | 28 |
| Novos boots reais | 0 | 0 |

**Pacote de integração SDK 1.4.0:** SHA-256 calculado e confirmado 01a5d0aa63969b17319e99b7c40b6b4be90cad2e7eab84b42e8ba8851bb5a5a9. Seus binários são para validação, NÃO são release pública e não foram distribuídos.

## Entregas da Rodada 10

1. **AutoTMC 1.0.2 (novo v6):** EXE portátil PyInstaller --onefile, 25.408.138 B e SHA-256 2abbda2825e8e87ae1787ceda868a2db3ae4a414092d33a6218adcbf3aae3d66. Instala somente o gerenciador, não o jogo TMC. Status experimental.
2. **Cannonball v0.34 (v5 → v7):** import_input_set de 31 ROMs OutRun Revision B por tamanho e CRC32 do loader oficial; 2.064.384 B. Mismatch do upstream roms/roms.txt (epr-10381a.132) versus código que carrega epr-10381b.132. Status experimental.
3. **Zelda3 v0.3 (v3 → v7):** import_input de ROM US .sfc, SHA-256 oficial 66871d66be19ad2c34c927d6b14cd8eb6fc3181965b6e517cb361f7316009cfb. Status experimental.
4. **SMW v0.1 (v3 → v7):** import_input de ROM US .sfc, SHA-1 oficial 6b47bb75d16514b6a476aa0c73a683a2a4c18765. Status experimental.

**Infraestrutura:** schemas 6/7 acrescentados aos anteriores, validador ampliado sem afrouxar v3/v5, 5 exemplos sintéticos e 7 novos testes com casos negativos. Testes da main 18/18 mantidos (total 25/25). Parser real do host SDK 1.4.0: 91/91, harness 70/70, incluindo CRC32 sintético e adulteração rejeitada. Testes com mídias originais e primeiro boot: NENHUM.

## Bloqueios, documentação e próximas tarefas

- Severed Chains exige Java25 (bytecode major 69), classpath com dependências externas e opções JVM; SDK v7 só oferece java-21 e -jar. Não há receita v7 segura equivalente.
- Project Picori exige correção de repositório no catálogo; tar.gz já é suportado no SDK, mas ID de origem está incorreto.
- WipeOut Phantom Edition: validação CUE/BIN exigiria hashes/tamanhos reproduzíveis por faixa indisponíveis.
- Phase Distorter: precisa extrair assets pelo importador oficial; cópia de ROM no perfil não equivale à preparação.
- Instaladores sem perfil aprovado, builds não isolados e releases ausentes continuam bloqueados.

Detalhes: [Rodada 10](RODADA-10-SDK14-2026-11-23.md), [119 projetos](COBERTURA-CATALOGO.md), [Spec Codex](ESPECIFICACAO-CODEX-SDK.md), [Guia de mídias](HOMOLOGACAO-MIDIA-NECESSARIA.md).

**Ações finais:** confirmar hashes/arquivos publicados, executar validações completas e CI, abrir PR para revisão sem merge.
