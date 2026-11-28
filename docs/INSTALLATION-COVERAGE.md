# Cobertura de instalação e elegibilidade — 27/11/2026

A revisão cobre os 148 IDs anteriores sem exigir que todos permaneçam ativos.
O catálogo revisado tem **108 jogos e 137 projetos elegíveis**. Os outros **11 IDs**
ficam em `AllFix-Repo/excluded-projects.json`, com metadados, motivo e condições
para reconsideração. O registro de elegibilidade e as exclusões pertencem ao
mesmo commit de `catalog.json`.

## Estado do GetAll

O índice preserva **145 receitas**: **122 experimentais**, **uma homologação
histórica (`validated`)** e **22 desativadas (`disabled`)**. Há contrato ativo para
**123 projetos**; **14 projetos elegíveis** ficam sem automação ativa e continuam
com o procedimento oficial registrado no catálogo. Quantidade de receitas não
comprova instalação, boot ou gameplay.

As 22 variantes suspensas compreendem 19 variantes com mudanças próprias
identificadas na auditoria de fontes, Ship of Harkinian 9.3.1 com auxiliar sem
proveniência suficiente, e duas entradas retiradas por elegibilidade/duplicidade
(GGA64 e o agregado Sonic 1 Forever/Sonic 2 Absolute). Dr. Mario base, Metaforce e
Burnout 3 já fazem parte das 19 primeiras. As receitas permanecem versionadas e
com hashes, datas e motivos. A exclusão editorial não proíbe o usuário de jogar
uma instalação existente; a suspensão de um pipeline alterado impede executá-lo
como instalação oficial.

Os aliases oficiais **SM64Plus LauncherMirror**, **CTR ci-07d0c49** e **MKW
v0.1.18** continuam disponíveis. A variante `mkw v0.1.18-allfix-cli` permanece
suspensa. Hookshot agora referencia `ItsNotRexed/Hookshot` e o perfil
`hookshot-3.0.2-official-prepare`. KnowYourRole usa o executável de instalação
fornecido no ZIP oficial com `--cue`/`--out`; a receita não exige duplicar seu
launcher recompilado dentro do Desktop.

## Seis dimensões independentes

| Dimensão | Resultado registrado | O que o resultado permite concluir |
|---|---:|---|
| Upstream funcional | 137 com evidência específica | Gameplay documentado pelas fontes revisadas; limitações e procedimento oficial permanecem no catálogo. |
| Automação implementada | 121 implementadas; 2 parciais; 14 suspensas | Revisão de rotas e corpos de instalação no código. Não é uma execução ponta a ponta. |
| Validação sintética | 13 relatórios históricos; 124 sem resultado individual transferido | Provas limitadas de ferramentas/transações em SDK anterior. Não foram reaprovadas automaticamente para o SDK 1.5.70. |
| Instalação com mídia original | 1 relato histórico; 136 desconhecidas | Relato anterior de SM64 Coop Deluxe, sem novo recibo de reprodução nesta rodada. |
| Primeiro boot pelo GetAll | 1 relato histórico; 136 desconhecidos | O mesmo relato registra importação e execução; não houve nova confirmação. |
| Gameplay pelo GetAll | 137 desconhecidos | Não se transforma o relato genérico de execução nem gameplay upstream em sessão de gameplay comprovada pelo GetAll. |

`unknown` significa ausência de prova atribuível no registro, não falha do port.
`historical` preserva uma prova anterior sem afirmar que a implementação atual
passou novamente. `partial` identifica um trecho documentado que ainda depende
do procedimento manual oficial ou da validação da integração substituída.
Os dois parciais desta revisão são SM64Plus LauncherMirror e CTR ci-07d0c49,
que conservam a preparação manual oficial. MKW v0.1.18, Hookshot e KnowYourRole
têm rotas oficiais implementadas, confirmadas pela leitura dos handlers e do
dispatch do SDK 1.5.70. A falta de uma execução atual não muda essa dimensão
para parcial. As provas de mídia, boot e gameplay continuam independentes;
veja [a revisão dessas rotas](validations/official-scope/installation-route-refresh.json).

O arquivo [installation-evidence.json](installation-evidence.json) registra cada
projeto e dimensão. Cada alegação positiva exige tag e SHA-256 exatos da receita,
fonte atribuível e observação. Os arquivos locais têm SHA-256 conferido. Se a
receita mudar ou ficar desativada, a prova positiva deixa de contar como atual.
Provas sintéticas não são aceitas nos campos de mídia original, boot e gameplay;
provas externas do upstream alimentam somente a dimensão upstream funcional.

A matriz reproduzida está em
[official-scope/catalog-coverage.json](validations/official-scope/catalog-coverage.json).
Ela não consulta nem muda a instalação pública. Os campos antigos de contagem
são preservados para consumidores existentes e explicitamente não significam
cobertura funcional. `main_comparison: not_requested` significa que não houve
comparação com a branch pública nessa execução.

## Monitoramento e reentrada

O monitor consulta somente fontes oficiais. Uma proposta automática de receita
exige projeto ativo com classificação funcional, evidência concreta de gameplay,
procedimento oficial e revisão de proveniência. README, release existente,
compilação, tela inicial e fixture isolada não bastam. Candidatos e excluídos
podem gerar uma nota de revisão, sem download de builds, receita ativa, mudança
de catálogo ou substituição de `added_at`.

Receitas desativadas, suspensões de integridade, contratos estendidos e receitas
homologadas exigem revisão explícita para uma nova versão. Nenhuma atualização
reativa uma receita ou atribui `validated` automaticamente. A branch de
monitoramento da prévia e a base da PR derivam da branch de revisão; a prévia é
recusada quando o destino é `main`. O workflow preserva relatórios textuais
pequenos e usa arquivos temporários para inspeções de ZIP.

O validador admite um ID fora do catálogo somente quando a receita está
`disabled`, sua identidade consta no registro de exclusões e o repositório
preservado confere. IDs órfãos ativos ou sem registro falham. As 20 variantes
suspensas por fidelidade/proveniência também constam em
[official-install-policy.json](official-install-policy.json), independentemente
de o projeto continuar elegível no catálogo.

## Reprodução

```sh
python scripts/validate_recipes.py --strict-lf --require-jsonschema --check-git-blobs --check-catalog ../catalog-scope/catalog.json
python scripts/catalog_coverage.py --catalog ../catalog-scope/catalog.json --output docs/validations/official-scope/catalog-coverage.json
python -m unittest discover -s tests -v
```

O CI usa `scripts/validate_ci.py` com o catálogo fixado em
`91bd560fab30f7411b5350abe0ad7103d370a7ce` e seus registros
companheiros. A seleção do canal é testada separadamente. Os testes cobrem
reativação indevida, candidato/excluído, conservação de datas, igualdade de
identidade, hashes de provas e a separação das seis dimensões.

## Proveniência e limites

A [matriz da auditoria de fontes](audits/source-integrity-20261127/audit-matrix.json)
registra as rotas e os corpos examinados. Os resultados sintéticos transferidos
citados individualmente vêm de [SDK 1.5.67/68](validations/sdk167-flow-completion.md).
O relato histórico de SM64 está na
[auditoria de 22/11](AUDITORIA-CATALOGO-2026-11-22.md).
Nenhum novo teste com mídia comercial foi fabricado para preencher a matriz.
Compilações intermediárias, ZIPs de inspeção e fixtures descartáveis podem ser
removidos depois da verificação; fontes, receitas, scripts, logs, hashes,
resultados, mídias originais e dependências ativas permanecem preservados.
