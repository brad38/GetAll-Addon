# GetAll-Addon — rodada SDK 1.2.0 / contrato de instalação v4 (2026-11-23)

## Escopo e controle de versão

- SDK adotado: arquivo original AllFix-Addon-SDK-1.2.0.zip, versão contratual 1.2.0, API 1.0; índice remoto no formato 1.
- SDK localizado em AllFix-SDK-1.2\AllFix-Addon-SDK-1.2.0.zip. SHA-256 do ZIP do SDK: b33bfda93682a005b8851d2eba7b178210f1ef38e77aac4892be7ecfb22a3709.
- Executável disponibilizado: AllFix.exe da mesma pasta, FileVersion 3.0.0.0, SHA-256 6ea9cdf98b4d43a4ca52e1d307c8a0f80810a197978a1520bdb66d2d83390937.
- Código do AllFix, binário de testes, catálogo, pacote GetAll-Addon v1.0.0 e receita funcional do SM64 Coop Deluxe: **sem alterações**.
- Auditorias anteriores preservadas: [119 projetos](AUDITORIA-CATALOGO-2026-11-22.md), [85 projetos B](RODADA-B-2026-11-23.md), [pendências](CAPACIDADES-PENDENTES-2026-11-22.md). Nesta rodada não se refez o catálogo.

## Contrato v4 efetivamente conferido

O documento INSTALACAO-V4.md, o arquivo Contracts.cs, o schema v4 e o exemplo do SDK 1.2.0 foram examinados diretamente no ZIP oficial. Receitas v1/v2/v3 continuam no contrato. O novo import_input_set exige entrada kind=directory e files com caminhos relativos, size e SHA-256 individuais, até 64 arquivos e 64 GiB totais, scope=installation. A importação ocorre por preparação temporária; arquivos faltantes e alterados são rejeitados. first_run_files exige paths, sizes e hashes reproduzíveis de saídas de dados dentro da pasta instalada, além de manual_steps e launch_file presente em required_files; a verificação posterior libera Jogar agora apenas quando o host confirma os dados e o executável instalado.

O schema v1 do SDK 1.2.0 admite + no interior de nomes de arquivo, mas ainda rejeita espaços. Foi alinhado apenas esse padrão no schema compartilhado do repositório e publicada a cópia exata do schema v4 do SDK, com referências aos schemas v1 e v3. O manifesto do addon universal não foi modificado.

**Experimentos:** o código do host aceita entradas experimentais no índice, mas FindAsync somente oferece status validated, com schema de 1 a 4. Nenhuma receita experimental foi promovida apenas para descoberta.

## Prioridade 1 — cinco projetos sem receita

| Jogo / ID oficial | Release e pacote Windows inspecionado | Diagnóstico | Estado |
|---|---|---|---|
| OutRun / cannonball | djyt/cannonball v0.34, cannonball-v034-w64.zip; pacote já inspecionado na auditoria anterior | Precisa do romset OutRun Revision B em roms/ e da configuração correspondente. Não há lista confiável de tamanhos e SHA-256 de todos os originais no material auditado; não se pode preencher files artificialmente. | Bloqueado para v4 verificável |
| WipeOut / wipeout-phantom-edition | v1.2.256, wipeout-x64-release.zip (3.619.822 bytes), executável wipeout/wipeout.exe | São necessárias 9 trilhas BIN e uma CUE do disco PS1 USA, ou 517 arquivos extraídos. Nomes oficiais das trilhas incluem espaços e parênteses e o schema v4 rejeita esses caminhos. Também faltam SHA-256 reprodutíveis das trilhas; o port realiza extração de recursos no primeiro uso. | Bloqueado |
| Driver 2 / redriver2 | 7.4-rc2, REDRIVER2_Win32_Release.zip (9.772.801 bytes), executáveis Launcher.exe e REDRIVER2.exe | Instruções oficiais exigem os dois discos originais e um instalador/launcher com assistente; o fluxo recomenda Java e processamento específico dos dados. A operação v4 não executa o assistente nem extrai/converte conteúdo de imagens ISO/BIN/CUE. | Bloqueado para automatização nativa |
| Vandal Hearts / vandalhearts-pcport | v2.1.0, VandalHearts-v2.1.0-windows-x64.zip (5.771.542 bytes), vandalhearts_pc.exe + 8 DLLs | Exige pelo menos um disco PS1 legítimo em imagem BIN bruta dentro de game/. O projeto confirma regiões e MD5 do executável PS1, não os SHA-256 dos BIN completos, que são necessários à importação v4. A instalação manual do disco pelo próprio jogo não substitui uma lista verificável. | Bloqueado para import_input_set |
| EarthBound / phase-distorter | 0.5, Phase-Distorter-0.5-windows-x86_64.zip, executável Phase-Distorter-0.5-windows-x86_64/Phase Distorter.exe | Mesmo com hashes SHA-256 oficiais das ROMs, o nome real do EXE contém espaço. O schema v1 referenciado pela receita v4 não aceita espaços em required_files e launch_file. Os recursos gerados ficam no diretório externo de dados do usuário, que first_run_files não pode verificar. | Bloqueado |

As três releases Windows de WipeOut, REDRIVER2 e Vandal Hearts foram baixadas e seus ZIPs abertos nesta rodada sem executar código. Os pacotes Cannonball e Phase Distorter já haviam sido inspecionados na auditoria anterior; as releases e os métodos oficiais foram revisitados apenas para conferir a compatibilidade v4. Nenhum arquivo de jogo comercial foi adquirido, distribuído ou inferido. Não foram publicadas receitas com hashes inventados.

Fontes principais: [Cannonball](https://github.com/djyt/cannonball), [WipeOut Phantom Edition](https://github.com/wipeout-phantom-edition/wipeout-phantom-edition), [REDRIVER2](https://github.com/OpenDriver2/REDRIVER2/wiki/Installation-instructions), [Vandal Hearts / manual](https://github.com/HalmyLyseas/VandalHearts-PcPort/blob/master/docs/manual/manual.md), [Phase Distorter](https://github.com/TheRunaway5/Phase-Distorter).

## Prioridade 2 — 12 receitas v3 reavaliadas, sem migração artificial

| Projeto | Motivo para preservar v3 |
|---|---|
| Ghostship | Recursos do primeiro uso derivados da ROM, suportando US/JP; não há tamanho e SHA-256 reproduzíveis das saídas declaradas dentro da instalação |
| Ship of Harkinian | Suporta diferentes ROMs; recursos O2R/OTR variam; hashes de saída e local final não foram homologados |
| Zelda64 Recompiled | Lê a ROM na própria interface e armazena dados fora do destino de instalação; nenhuma saída estática aprovada em first_run_files |
| 2Ship2Harkinian | Primeiro uso depende da ROM e de recursos específicos; saídas exatas não verificadas |
| Starship | US 1.0 ou 1.1 e O2R gerado pelo jogo; não existe um único hash de saída autorizado |
| SpaghettiKart | Geração local de MK64 O2R; tamanho e SHA-256 da saída pós-importação ainda não homologados |
| PaperBoat | Importação pelo jogo, sem conjunto completo de arquivos gerados e hashes demonstrados |
| Banjo Recompiled | Seleção de ROM no próprio launcher, sem artefato determinístico sob a pasta instalada |
| Lighthouse | ROMs US/JP/PAL suportadas; conteúdo resultante varia, sem hashes oficiais por versão |
| Banjo-Tooie Recompiled | O programa lê a ROM diretamente, sem etapa de extração local que first_run_files possa confirmar |
| BattleTanx Global Assault PC Port | Seleção da ROM durante execução; nenhum arquivo gerado determinístico, identificado e verificável |
| Recharged | Launcher aponta para imagem legítima ISO/RVZ/WBFS em pasta externa; não há saída estática sob a instalação |

Não converter para schema_version 4 apenas para trocar o número de versão. Todas as 12 receitas permanecem experimentais v3, com as limitações de primeira execução descritas anteriormente.

## Prioridade 3 — GoldenEye PC Port v0.5.0

O pacote oficial goldeneye-pc-port-0.5.0-win64.zip foi baixado novamente (17.178.242 bytes; SHA-256 b49bfb826566367a4d1af16466530f0fadd85e522b33859521d849c143a005ef) e inspecionado. Contém 534 arquivos. A DLL necessária está exatamente em goldeneye-pc-port-0.5.0-win64/libstdc++-6.dll.

A receita existente schema_version 3 recebeu somente essa entrada adicional em required_files. Executável, outras DLLs exigidas, operação import_input, hash SHA-1 da ROM americana, project_id e tag não mudaram. O SDK v3 herdou a gramática de caminhos ampliada no SDK 1.2, portanto migrar a receita para v4 não traz benefício. O status permanece experimental. Não foi testada a execução com ROM original legítima.

## Testes executados no motor e suas limitações

Um harness de testes separado, criado em GetAll-SDK12-round\HostContractHarness, foi compilado com .NET 8 e carregou a DLL Release do AllFix já compilada, sem alterar o projeto-fonte nem executar o EXE do jogo. **27/27 verificações foram aprovadas.** Casos cobertos:

1. Parser v3 do GoldenEye com o + em nome de DLL; parser v4 para import_input_set e first_run_files.
2. Rejeição de SHA-256 inválido, caminho duplicado, extensão proibida, traversal, scope incorreto, espaço no caminho e first_run_files sem manual_steps.
3. Índice v4 com status experimental aceito sintaticamente e filtrado da descoberta; validated descoberto com dados sintéticos.
4. Arquivos sintéticos originais de 11 bytes verificados por tamanho e SHA-256, com rejeição de adulteração sem mudança de tamanho.
5. Importação sintética do conjunto para a pasta de instalação; etapa manual preservada como pendente.
6. Cancelamento anterior à operação rejeitado sem gravar importações.
7. Estado de preparação pendente mantido até os dados gerados serem verificados; transição para Completed; PlayInstalled bloqueado depois da alteração do arquivo gerado ou do executável.

As verificações foram feitas pelos métodos reais do motor compilado, mas **não equivalem a uma instalação completa pela interface do AllFix.exe**, nem a teste funcional de qualquer jogo. Cancelamento no meio de um volume grande e rollback pós-falha não foram demonstrados. O executável fornecido foi inspecionado quanto a hash e metadados, porém não foi aberto nesta rodada. A verificação do código e da DLL confirma suporte estrutural; o fluxo visual completo continua pendente de teste.

A validação estática adicional aceitou todas as 14 receitas já publicadas no SDK 1.2.0 e o exemplo oficial de contrato v4. Após publicar a alteração, repetir os hashes dos bytes remotos.

## Solicitações concretas ao Codex

1. **Caminhos Windows com espaços:** ampliar a gramática de segmentos relativos seguros, mantendo proibição de traversal, nomes reservados, caminhos absolutos e links. Desbloqueia Phase Distorter e nomes de trilhas WipeOut.
2. **Leitores e extratores restritos de formatos de disco:** capazes de validar e extrair BIN/CUE multi-track e ISO/RVZ/WBFS, com formatos e destinos controlados pelo host, sem scripts arbitrários; necessário para WipeOut e REDRIVER2, e potencialmente outros projetos.
3. **Verificadores declarativos confiáveis de saídas variáveis/externas:** além de first_run_files exatos, um verificador aprovado pelo host para formatos e diretórios de dados do usuário, sem aceitar checagem trivial de arquivo. Útil para ports que geram O2R/OTR, Zelda64 e Phase Distorter.
4. **Perfis legítimos de integridade de originais:** ferramenta/processo de publicação para identificar coleções de ROMs/discos por SHA-256 conhecido, tamanho, região e layout, evitando hashes inventados. Não deve ser um modo de ignorar a integridade.

## Resultado e política de publicação

- Projetos prioritários reavaliados: 5. Receitas v3 existentes reavaliadas: 12. GoldenEye revisado: 1. Total 18 projetos examinados nesta rodada, sem refazer a auditoria dos 119.
- Novas receitas v4 seguras para jogos reais: 0. Migrações v3→v4: 0. Novas receitas v3 para outros jogos: 0. Atualizações relevantes de receitas: 1 (GoldenEye v3, dependência DLL).
- Receitas funcionalmente validadas nesta rodada: 0. Status validated anterior do SM64 Coop Deluxe preservado.
- Índice remoto esperado: 14 entradas (1 validated; 13 experimental). As experimentais não aparecem na descoberta normal.
- Não atualizar o ZIP v1.0.0, o host ou o catálogo. As mudanças desta rodada ficam restritas ao GitHub GetAll-Addon.
