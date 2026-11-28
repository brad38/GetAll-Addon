# Cobertura de instalação e elegibilidade — 28/11/2026

A revisão preserva **108 jogos e 137 projetos elegíveis**.
Os **11 IDs arquivados** continuam em AllFix-Repo/excluded-projects.json, com
metadados, motivo e condições de reavaliação. Somente VandalHearts-PcPort e
REDRIVER2 tiveram suas entradas de automação atualizadas nesta continuação.

Esta é a preparação da **prévia TESTE 1.5.78 / SDK mínimo 1.5.72**.
O catálogo está fixado em **6407730f9708de995175cd757ec41e871c3ebc62**, com catalog.json,
eligibility.json e excluded-projects.json conferidos por GET público no mesmo
commit. O CI Catalog [46115153161](https://github.com/brad38/AllFix-Repo/actions/runs/46115153161) passou.
O pin PREVIEW_CATALOG foi atualizado depois dessa verificação. GetAll ainda
aguarda seu commit; nenhuma instalação pública foi alterada.

## Receitas e projetos

O índice contém **147 receitas: 136 experimentais,
uma validada histórica e 10 desativadas**.
São **137 receitas ativas para 137 projetos elegíveis**.
Isso mede disponibilidade de contratos de instalação; não significa
137 jogos testados ou 137 primeiros boots.

As dez receitas desativadas correspondem a **cinco IDs arquivados**
(GGA64, Burnout 3, o agregado Sonic 1 Forever/Sonic 2 Absolute, Dr. Mario 64 base
e Metaforce) e **cinco variantes antigas com outra receita ativa no mesmo
projeto** (SM64Plus, SSX, CTR, MKW e VandalHearts v2.1.0).
Nenhum ID arquivado foi reincluído. O contrato REDRIVER2 anterior foi preservado
byte a byte em retired-recipes antes da substituição por um novo perfil exato.

## Novas rotas experimentais

| Projeto | Contrato e entradas | Limites materiais |
|---|---|---|
| VandalHearts-PcPort | build-14552ff, perfil vandal-14552fff-official-wsl; discos originais US SLUS-00447 e JP SLPM-86007 em BIN MODE2/2352; BIOS/KROM compatível. | Ubuntu x64 no WSL2, Python 3.12+, glibc 2.38+, CMake, Ninja, Make, GCC, dpkg-deb, Bash e libzstd. Dependências de compilação Windows privadas; fonte upstream intacta; WebP/HD video ligados. |
| REDRIVER2 | 7.4-rc2, perfil redriver2-7.4-rc2-official-media; dois discos originais PAL ou NTSC-U da mesma região/revisão; Java 21 privado preparado pelo SDK. | Download direto do publisher fixado por hash; preserva 93 arquivos do kit e todos os 76 extras. A revisão documenta origens mistas sem declarar licença MIT integral dos componentes de terceiros. |

VandalHearts é compilado localmente a partir da fonte oficial com os dados
do usuário. O binário precompilado v2.1.0 continua desativado.
REDRIVER2 usa o pacote oficial integral e seus conversores, com os dados dos
dois discos do usuário. O addon não hospeda, espelha nem reempacota os recursos
do jogo ou do publisher. Ambos os perfis antigos permanecem aposentados.

A [revisão desta ativação](validations/official-scope/vandal-redriver2-sdk172-review-20261128.json)
fixa as receitas e preserva os registros anteriores. A procedência específica
do REDRIVER2 está [documentada por grupo e commit](validations/official-scope/redriver2-provenance-20261128.md).
O silêncio na issue 234 não foi interpretado como ilegalidade nem como uma
licença; as conclusões descrevem a origem e o uso direto do pacote oficial.

## Seis dimensões independentes

| Dimensão | Resultado registrado | Alcance da evidência |
|---|---:|---|
| Upstream funcional | 137 com evidência específica | Evidência externa do catálogo; não é teste local GetAll. |
| Automação implementada | 137 implementadas; 0 parciais; 0 bloqueadas | Perfis, preparação, publicação e lançamento revisados; não atesta conclusão com mídia original. |
| Validação sintética | 54 atuais passaram; 13 históricos; 0 falhas atuais; 70 desconhecidos | Somente as operações atribuídas nos recibos: kits, recusas, ferramentas, configuração ou builds sem mídia original. |
| Instalação com mídia original | 1 relato histórico; 136 desconhecidas | SM64 Coop Deluxe v1.5.1; sem nova reprodução nesta rodada. |
| Primeiro boot pelo GetAll | 1 relato histórico; 136 desconhecidos | O mesmo relato anterior de importação e execução. |
| Gameplay pelo GetAll | 137 desconhecidos | Nenhuma sessão específica GetAll atribuível foi acrescentada. |

Nesta continuação houve **zero instalação completa com mídia original, zero
primeiro boot e zero sessão de gameplay com mídia original**.
A única receita validated permanece SM64 Coop Deluxe v1.5.1, SHA-256
54fb8ac09863fc500b532244070e9cbe5bc4a81aaff66530b4e711b97fb2a2f3.
O relato anterior consta na [auditoria de 22/11](AUDITORIA-CATALOGO-2026-11-22.md);
ele não foi reaprovado nem reproduzido por esta ativação.

A falha anterior de configuração nativa Windows do VandalHearts continua
registrada no histórico. Ela não é transferida como resultado da nova rota
WSL. Os recibos anteriores de conversão REDRIVER2 também não provam uma
instalação completa com ambos os discos. Os resultados atuais só entram no
eixo sintético quando há evidência atribuível vinculada à receita corrente.

## Ledger e reprodução

O [ledger](installation-evidence.json) vincula cada alegação positiva à tag
e ao SHA-256 exatos da receita. Os hashes dos arquivos de evidência são
conferidos pelo gerador da [matriz JSON](validations/official-scope/catalog-coverage.json).
Mudar a receita sem renovar essa vinculação torna a evidência positiva histórica.
Fixtures, builds e testes de ferramenta nunca contam como mídia original,
primeiro boot ou gameplay.

Existem **34 projetos com perfis fechados schema 9**.
O alias legado preparation_only significa uses_closed_preparation_profiles;
ele não implica automação manual ou incompleta. main_comparison:
not_requested indica que a matriz não consultou nem alterou a branch pública.

A regressão Desktop SDK 1.5.72 passou com 2372 checks; o build do harness
terminou sem erros/avisos. O kit oficial Vandal passou 12 checks e o preflight
Windows/WSL passou. Os recibos WSL e REDRIVER2 delimitam seus testes atuais.
Os 82 testes Python passaram; o validador conferiu as 147 receitas com JSON
Schema, LF estrito e os três documentos de catálogo. O parser Desktop aceitou
147 receitas, com zero falhas. Esses checks não são somados como sessões de jogo. Resultados anteriores permanecem no
[histórico de validação](validations/official-scope/README.md); eles não são
apresentados como execução desta revisão.

~~~sh
python -B scripts/validate_recipes.py --strict-lf --require-jsonschema --check-catalog ../catalog-scope-20261127/catalog.json
python -B scripts/catalog_coverage.py --catalog ../catalog-scope-20261127/catalog.json --output docs/validations/official-scope/catalog-coverage.json
python -B -m unittest discover -s tests -v
~~~

Com o catálogo já fixado, executar também python -B scripts/validate_ci.py. O monitor continua limitado às fontes
oficiais e não promove contratos para validated automaticamente.
Nenhum merge em main, release pública, version.json ou instalação corrente
é modificado por esta ativação experimental.
