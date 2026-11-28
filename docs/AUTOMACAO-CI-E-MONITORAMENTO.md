# CI e monitoramento de instalações oficiais

Esta rotina valida a elegibilidade, a fidelidade do procedimento e as evidências
sem usar uma meta numérica de projetos. O relatório vigente é
[INSTALLATION-COVERAGE.md](INSTALLATION-COVERAGE.md).

## Validação em PR, push e execução manual

O workflow `.github/workflows/validate-recipes.yml` usa
`scripts/validate_ci.py`, `scripts/validate_recipes.py` e
`scripts/catalog_coverage.py`. Executa a suíte de `tests/` e preserva o relatório
textual de cobertura como artifact por 14 dias. As permissões são somente de
leitura. Os gatilhos incluem PR, execução manual e push em main e nas branches
de desenvolvimento declaradas, incluindo `work/official-install-scope-20261127`.

O canal `preview` usa o catálogo fixado em
`3d86836676e9c7fa7359c32987c13fefc0a2ff8b`, com `eligibility.json` e
`excluded-projects.json` desse mesmo commit. O canal público/legado mantém a
origem pública. Índice preview é recusado em push, execução manual ou PR com
destino main, antes de executar os validadores.

A validação verifica UTF-8/LF, schemas, hashes das receitas, identidade, caminhos,
operações, mídia e contratos fechados do SDK. Todo ID ativo do catálogo deve
ter avaliação funcional concreta, procedimento oficial e revisão de
proveniência. Uma receita de um projeto excluído só é aceita como histórico
`disabled` com a identidade/repositório arquivados. Órfãos ativos falham.
Receitas desativadas exigem motivo, data e referência. A política de integridade
impede reativar os contratos retirados apenas apagando seus motivos.

O relatório separa upstream funcional, implementação da automação, teste
sintético, instalação com mídia original, primeiro boot e gameplay. Evidência
local exige arquivo e SHA-256; alegações positivas exigem tag e SHA-256 exatos
da receita. Mudança de receita deixa a evidência anterior como histórica.
Teste sintético e gameplay upstream não preenchem mídia/boot/gameplay GetAll.
O status legado `validated` não se transforma sozinho em prova de execução.

```bash
python scripts/validate_ci.py
python -m unittest discover -s tests -v
```

Para conferir o checkout local do catálogo revisado:

```bash
python scripts/validate_recipes.py --strict-lf --require-jsonschema --check-git-blobs --check-catalog ../catalog-scope/catalog.json
python scripts/catalog_coverage.py --catalog ../catalog-scope/catalog.json --output catalog-coverage-report.json
```

## Monitoramento diário e descobertas

O workflow `.github/workflows/upstream-watch.yml` usa
`scripts/upstream_watch.py`. O agendamento existente é diário às 09:00 UTC;
`workflow_dispatch` permite uma revisão manual. Não foi criada uma segunda
rotina de agendamento. GitHub executa o agendamento da branch padrão; a nova
prévia pode ser verificada por dispatch na sua branch até ser aprovada a
integração posterior. Este trabalho não faz merge em main.

A consulta lê o catálogo e seus registros do mesmo commit selecionado pelo
canal. A matriz de 22/11 é usada apenas como histórico de tags, nunca como
lista fixa de 119 projetos nem como critério de elegibilidade.

Projetos ativos elegíveis podem receber uma proposta de versão. Para geração
automática, todas as receitas existentes desse projeto devem ser v3,
experimentais, com etapas manuais explícitas e sem operações/inputs. Contratos
estendidos, suspensões de integridade, versões disabled/draft e receitas
homologadas exigem revisão. A rotina jamais reativa variantes retiradas ou
promove automaticamente uma receita a validated.

Candidatos sem evidência e projetos do registro de exclusões podem gerar notas
de reavaliação quando aparece uma release nova. Esse caminho não baixa builds,
não cria receita ativa, não muda classificação, não altera o catálogo e não
substitui `added_at` pela data da pesquisa. Uma release sozinha não prova jogo
funcional. A reentrada exige análise de gameplay e procedimento oficial.

A inspeção de ZIP para uma proposta elegível usa pasta temporária, limite de
250 MiB, SHA-256 calculado e leitura da lista de membros. Não extrai nem executa
binários. O pacote temporário é descartado; o relatório mantém tamanho, hash,
URLs e observações. As receitas e evidências antigas são preservadas.

A branch de automação e a base da PR derivam da branch em que o workflow foi
iniciado. Revisões diferentes usam branches separadas. A prévia nunca tem main
como base. Atualizações na branch de automação usam push normal, sem force;
validação e testes precedem a publicação da proposta. Fingerprints suprimem
relatórios repetidos. Não existe merge automático.

O workflow mantém `contents: write` e `pull-requests: write` para propostas.
A criação de PR depende da permissão do repositório para o GitHub Actions.
O código do workflow foi revisado; a existência dessa permissão e uma execução
hospedada bem-sucedida precisam ser verificadas separadamente na integração.

## Pacote da prévia

[PREVIEW-SDK170.md](PREVIEW-SDK170.md) contém o comando com commits fixos para
addon **1.5.75** e SDK **1.5.70**. O empacotador aceita somente SHAs completos,
índice preview e versões canônicas `x.y.z`. Índices com a política
`official_upstream_only` exigem no mínimo SDK 1.5.70. O padrão legado do
empacotador não é suficiente para esta revisão.

O ZIP contém apenas `addon.json` e `responses.json`. Não incorpora runtime,
launcher, ROM, ISO, fonte do jogo ou ferramenta binária. O pacote universal
público continua preservado; instalar a prévia não muda automaticamente a
ativação do canal nem constitui uma release pública.
