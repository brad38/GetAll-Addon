# Cobertura de instalação e elegibilidade — 28/11/2026

A revisão preserva **108 jogos e 137 projetos elegíveis**. Os **11 IDs arquivados**
ficam em AllFix-Repo/excluded-projects.json, com metadados, motivo e condição de
reavaliação. O catálogo, a elegibilidade e as exclusões usam o mesmo commit
**b816345f811547cc04f6150faf16548c26b7409b** na prévia de StrikersRecomp.

## Receitas e projetos

O índice contém **146 receitas: 134 experimentais, uma validada histórica e
11 desativadas**. Há **135 receitas ativas para 135 projetos**. Os outros
**dois projetos elegíveis** permanecem disponíveis pelo procedimento oficial
registrado no catálogo, com automação suspensa por um impedimento concreto.

As 11 receitas desativadas se dividem em **cinco IDs arquivados** (GGA64,
Burnout 3, o agregado Sonic 1 Forever/Sonic 2 Absolute, Dr. Mario 64 base e
Metaforce), **quatro variantes antigas com outra receita ativa no mesmo projeto**
(SM64Plus, SSX, CTR e MKW) e **dois projetos elegíveis bloqueados**
(VandalHearts-PcPort e REDRIVER2). Dr. Mario 64 Plus é um projeto
distinto; sua presença não reativa o ID base. Burnout 3 e Metaforce não têm
uma rota ativa nem permanecem no catálogo atual.

A retomada restaurou treze projetos anteriormente suspensos por caminhos oficiais,
completou SM64Plus/CTR e eliminou a etapa manual restante de Shadow of Rome.
A prévia seguinte acrescenta StrikersRecomp pelo RecompCore com ISO própria.
Novos perfis têm hashes exatos aprovados; os perfis antigos adulterados continuam
bloqueados. Os bytes anteriores permanecem em retired-recipes. Veja
[a revisão dos contratos](OFFICIAL-CONTRACT-RESTORATION-20261128.md).

## Seis dimensões independentes

| Dimensão | Resultado registrado | Alcance da evidência |
|---|---:|---|
| Upstream funcional | 137 com evidência específica | Evidência externa do catálogo, independente de testes locais GetAll. |
| Automação implementada | 135 implementadas; 0 parciais; 2 bloqueadas | Código, dispatch, perfil e operação oficial revisados; não é uma instalação comercial concluída. |
| Validação sintética | 52 atuais passaram; 13 históricos; 1 falhou; 71 desconhecidos | Somente as operações descritas em cada recibo: pacotes, negativos, configuração, ferramentas ou builds sem mídia. |
| Instalação com mídia original | 1 relato histórico; 136 desconhecidas | SM64 Coop Deluxe v1.5.1, sem nova reprodução nesta rodada. |
| Primeiro boot pelo GetAll | 1 relato histórico; 136 desconhecidos | O mesmo relato anterior de importação e execução. |
| Gameplay pelo GetAll | 137 desconhecidos | Nenhuma sessão específica GetAll atribuível foi acrescentada. |

Nesta retomada houve **zero instalação completa com mídia original, zero
primeiro boot e zero sessão de gameplay com mídia original**. A única receita
validated continua SM64 Coop Deluxe v1.5.1, SHA-256
54fb8ac09863fc500b532244070e9cbe5bc4a81aaff66530b4e711b97fb2a2f3.
Sua evidência é o relato histórico na
[auditoria de 22/11](AUDITORIA-CATALOGO-2026-11-22.md), SHA-256
5a3747fbc2ba1f57d28ddb26851dfc93f71f3fa1d761ccc6e69f92d9e52cef78.
Não foi criada uma nova homologação.

Entre os resultados anteriores estão SSX, FH1, GOW Daniel, Pinyon,
SoH, SM64Plus, sm64ex, Render96ex, SM64RT, SM, SM Rewrite, GT5, GOW KIexster,
MKDD e Shadow of Rome. Seus escopos variam: FH1 prova integridade do kit;
SM/SM Rewrite também têm compilação nativa intacta sem ROM; MKDD prova
runtime_check sem link do jogo; Mario prova ferramentas e recusas de ROM;
SoR prova defaults, kit e plano de lançamento sintético. Uma aprovação não
substitui as demais dimensões. A nova prova de StrikersRecomp verifica o
seletor único, cancelamento, recusa de ISO incompatível, compilação do módulo
a partir de mídia autoral e staging do host. [Recibo do SDK 1.5.71](validations/official-scope/strikers-getall-result-20261128.json).

A única falha sintética atual é a configuração CMake nativa intacta de
VandalHearts neste ambiente: links simbólicos obrigatórios e OpenAL impediram
a configuração. Esse resultado não é uma avaliação de gameplay nem uma
declaração de incompatibilidade universal. Os demais detalhes estão nos
[recibos dos bloqueios](validations/official-scope/remaining-official-blockers.json).

## Impedimentos concretos e reentrada

| Projeto | Impedimento da automação atual | Condição de reentrada |
|---|---|---|
| VandalHearts-PcPort | Binários incorporam dados declarados no NOTICE; a alternativa de fonte/mídia/BIOS próprios ainda carece de ambiente oficial integrado e validado. | Validar build oficial com os arquivos próprios e recursos preservados; não reutilizar a distribuição binária como substituto dessa geração. |
| REDRIVER2 | O pacote copia dados extras rastreados cuja procedência/extração integral não foi esclarecida; os conversores examinados cobrem áudio/vídeo. | Documentar origem/licença dos extras ou extração oficial reprodutível dos CDs próprios. |

Essas são suspensões da integração, não remoções da elegibilidade funcional.
A investigação e os commits exatos constam em
[OFFICIAL-CONTRACT-RESTORATION-20261128.md](OFFICIAL-CONTRACT-RESTORATION-20261128.md).

## Registros e semântica

O [ledger](installation-evidence.json) registra cada projeto e dimensão. Uma
alegação positiva exige tag e SHA-256 exatos da receita, fonte atribuível e
observação. Arquivos locais têm SHA-256 conferido. Se a receita mudar ou for
desativada, uma prova positiva deixa de contar como atual. Provas sintéticas
não são aceitas como mídia original, boot ou gameplay; evidência upstream
alimenta somente a primeira dimensão.

A [matriz JSON](validations/official-scope/catalog-coverage.json) é gerada sem
consultar ou mudar a instalação pública. Os campos legados main_covered e
development_covered contam contratos, não execução. preparation_only é um
alias descontinuado de uses_closed_preparation_profiles: schema 9 pode
implementar a preparação oficial completa no SDK e não significa somente
manual. Existem 32 projetos com esses perfis fechados. O estado de automação
vem da dimensão apropriada. main_comparison: not_requested indica ausência
de comparação com a branch pública.

unknown significa falta de prova atribuível; historical preserva prova anterior
sem reaprová-la; failed descreve a operação nomeada que falhou. Não se converte
uma fixture, tela inicial ou build em gameplay.

## Testes e reprodução

Os kits oficiais e casos sintéticos foram executados para 29 projetos ativos
N64 e sete Xbox. A conversão de vídeo do REDRIVER2 e a configuração Windows
cruzada de Vandal Hearts receberam provas dirigidas. Esses dois projetos
continuam com instalação manual. Consulte os recibos de
[N64](validations/official-scope/n64-portable-batch-20261128.json),
[Xbox](validations/official-scope/xbox-portable-batch-20261128.log),
[REDRIVER2](validations/official-scope/redriver2-official-alternatives-20261128.md) e
[Vandal Hearts](validations/official-scope/vandal-cross-build-result-20261128.json).

**81 testes Python passaram** na prévia de StrikersRecomp. O validador
local conferiu as **146 receitas** com LF estrito, JSON Schema, blobs Git
e o checkout do catálogo fixado. A matriz conferiu os hashes de evidência.
Os resultados anteriores do Desktop estão nos
[recibos de validação](validations/official-scope/README.md).

~~~sh
python scripts/validate_recipes.py --strict-lf --require-jsonschema --check-git-blobs --check-catalog ../catalog-scope-20261127/catalog.json
python scripts/catalog_coverage.py --catalog ../catalog-scope-20261127/catalog.json --output docs/validations/official-scope/catalog-coverage.json
python -m unittest discover -s tests -v
python scripts/validate_ci.py
~~~

CI e monitor da prévia fixam o catálogo em b816345f811547cc04f6150faf16548c26b7409b.
O monitor consulta fontes oficiais, preserva datas e não reativa receita
desativada nem atribui validated automaticamente. Candidatos/excluídos geram
revisão, não instalação automática. A prévia não pode ter main como destino.

A prévia StrikersRecomp é **1.5.77**, com SDK mínimo **1.5.71**. Seu recibo posterior
ao commit contém o SHA GetAll definitivo, o SHA do catálogo, o hash/tamanho
do ZIP e os dois membros JSON. Commit local, publicação e CI hospedado são
verificados separadamente; a geração do ZIP não presume acesso remoto.
