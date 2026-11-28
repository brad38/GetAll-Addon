# Correção integral de escopo — 27/11/2026

## Estado de partida preservado

- Desktop: 921295de12349e726f7ca21a5edd8a8ecee123d8, work/complete-install-flows-20261127.
- GetAll: ceaa962fe1a2088a7f3900509b856743ff4b6672, mesma branch de desenvolvimento.
- Catálogo: 44bdb508842407d501e420457274eb4064f5d935 (inclui datas; não usar o snapshot anterior sem datas).
- Contagem de partida: 110 jogos, 148 IDs; 145 receitas/142 IDs, um validated histórico.
- Auditoria anterior e pedido integral preservados nesta branch.
- Bradsson acessível. Worktree Windows Desktop nova: GetAll-R18/desktop-scope-20261127.
- Branch Desktop/GetAll: work/official-install-scope-20261127.
- Branch catálogo: work/catalog-eligibility-20261127.
- Espelho editável do Desktop em scratch/desktop-scope; commit e build serão feitos no worktree Windows autenticado. Clone privado via CLI local não possui credencial; acesso Windows funciona.

## Etapas e estado de integração

A revisão final registra 108 jogos, 137 projetos ativos e 11 arquivados.
Catálogo e4fdde9d7c128f79eb19cf99ea07e2e9b628127a, publicado e conferido nos três documentos.
GetAll: 146 receitas, 134 ativas e 12 desativadas; 134 implementações e três
impedimentos concretos, sem fluxos parciais. A matriz separa 15 resultados
sintéticos atuais, 13 históricos, uma falha limitada de configuração e
108 desconhecidos. Não houve instalação/boot/gameplay com mídia original nesta retomada.

O complemento final de TESTE 1.5.76 requer SDK 1.5.70 e é gerado com os commits
definitivos, registrados no recibo externo ao commit para evitar referência
circular. O envio GetAll e o CI hospedado são etapas de integração separadas.
Ver [checkpoint](CHECKPOINT.md), [matriz](INSTALLATION-COVERAGE.md) e
[provas finais](validations/official-scope/README.md).

Plano da rodada, preservado para rastreabilidade:

1. Pesquisa de elegibilidade em três fatias (IDs1–50,51–100,101–148), usando fontes oficiais e evidência além de README/releases existentes.
2. Remoção/substituição dos patches próprios e componentes rejeitados; manutenção das capacidades legítimas.
3. Registro separado dos excluídos, validação de elegibilidade/datas e revisão da descoberta.
4. Índice/receitas, cobertura multidimensional, regressão, build de teste e pacote declarativo.
5. Limpeza de redundâncias comprovadas, commits/push/CI nas branches de revisão.

## Restrições da entrega

Sem merge main, release, mudança do version.json público ou substituição da instalação atual. Sem DownloadAll. A quantidade final vem da evidência; ausência de homologação GetAll não é ausência de funcionalidade upstream.

Não há automação ChatGPT cadastrada nesta conta. A rotina existente identificada é o workflow GitHub `upstream-watch.yml` e a documentação de descoberta do catálogo; serão atualizados sem agendar uma automação duplicada.
