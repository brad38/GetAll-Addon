# GetAll-Addon — limitações e capacidades genéricas sugeridas ao Codex

Análise do catálogo oficial: 87 jogos, 119 projetos. Não modificar o motor nesta etapa. O addon universal 1.0.0 e o SM64 Coop Deluxe 1.5.1 permanecem intactos.

## 1. Importação verificável de vários arquivos originais

Projetos: WipeOut Phantom Edition, Cannonball, VandalHearts-PcPort, REDRIVER2, ports de discos PS1/PS2/Xbox 360. Alguns projetos precisam de `BIN+CUE`, vários tracks ou diretórios de arquivos originais e não apenas uma ROM. Proposta: `import_input_set` ou `copy_input_tree` com lista de caminhos e checksums por arquivo, fonte selecionada pelo usuário, rejeição de links, limites de tamanho, escopo confinado ao staging e rollback atômico. Nunca copiar indiscriminadamente diretórios nem executar arquivos fornecidos como código.

## 2. Extração/transformação de recursos sob contrato restrito

Projetos: OpenGOAL, zelda3/smw, projetos de recompilação baseados em ISOs, Tomb Raider, jogos N64 que geram O2R/OTR. Proposta: operações genéricas `extract_verified_archive`, `extract_disc_content` ou provedores de conversão com formatos, saídas e hashes descritos, limites de recursos/tempo, execução sem privilégios administrativos e ferramentas explicitamente confiáveis do host. Não admitir `cmd`, scripts arbitrários, DLLs ou URLs escolhidas pelo JSON.

## 3. Validação do estado pós-primeira execução

Projetos: Ghostship, Ship of Harkinian, Starship, SpaghettiKart, Zelda64Recompiled, BanjoRecompiled, BattleTanxGA, Phase Distorter, Sonic Unleashed Recompiled. Vários binários oficiais abrem um assistente de importação de ROM/ISO. Hoje não existe contrato para o host distinguir 'EXE instalado' de 'jogo efetivamente preparado' quando a própria aplicação transforma os dados. Proposta: pós-condições verificadas sem execução remota, para reconhecer um asset gerado/local validado, e fases explícitas 'aguardando importação pelo jogo' sem disponibilizar Jogar agora como instalação completa prematuramente.

## 4. Instalações/launchers externos

Projetos: AutoTMC, FoxHollow, Silent Hill UWP, God of War launcher, aplicativos dependentes de .NET/JDK. Proposta: instalar pacotes Windows por APIs oficiais quando justificável e com consentimento; execução em conta não elevada/sandbox, manifesto assinado, allowlist de argumentos e confirmação. O AllFix atual pode operar elevado, portanto iniciar binários não confiáveis sob admin não deve ser incorporado como operação simples.

## 5. Origens externas e metadados corretos

Projetos: ExtremeGRecomp (GitLab), Sonic Forever (site externo), Project Picori (catálogo aponta o perfil `999sian`, embora `999sian/tmc` seja o repositório do projeto), Courage Reborn (link de notícia, sem Release confirmada), Wind-Waker-Recomp (README refere BlueWake de outro repositório). Proposta: provedor genérico de fontes de releases verificadas para GitLab e origens HTTPS aprovadas, com correspondência exata entre game_id/project_id/repository/tag; **não alterar o catálogo automaticamente** nem associar projeto de terceiro por aproximação.

## 6. Pipeline de compilação

Projetos: Render96ex, sm64ex/sm64rt, projetos decompilação SNES/N64, mkdd, SymphonyRecomp e outros com build obrigatório. Não permitir código arbitrário em receitas. A capacidade só seria aceitável após definição de fronteira de sandbox real, execução não administrativa, ferramentas auditadas e verificações de dependências/proveniência. Até lá, classe C.

## Bloqueios desta rodada

- Sem ROMs, ISOs ou discos originais dos outros jogos para testes end-to-end; GoldenEye é **candidata experimental**, não uma instalação validada.
- O controle de destino de instalação permanece responsabilidade do AllFix; `import_input` `scope=installation` respeita a pasta selecionada.
- O README e listas de Releases GitHub foram examinados, mas não todos os binários foram inspecionados: oito ZIPs tiveram conteúdo conferido diretamente.
- O addon `allfix.install.universal` versão 1.0.0 não requer atualização, e receitas estáticas não devem receber status `validated` sem teste funcional.
