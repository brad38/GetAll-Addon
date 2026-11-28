# Regras de manutenção — instalações oficiais e catálogo funcional

Estas regras incorporam a instrução do usuário de 27/11/2026, preservada em
docs/INSTALLATION-SCOPE-REQUEST-20261127.md. Substituem metas numéricas antigas e
restrições antigas de escrita que conflitem com a autorização desta rodada.

## Objetivo e elegibilidade

- All-Fix oferece projetos funcionalmente comprovados; GetAll automatiza seus
  procedimentos oficiais. Não implementar jogos em nome dos autores.
- Não manter uma meta artificial de 119/148 IDs.
- Não confundir upstream funcional, receita, preparação sintética, instalação com
  mídia original, primeiro boot e jogabilidade. Registrar cada dimensão.
- README, percentual de decompilação, release existente e build isolado não
  comprovam jogabilidade. Preservar evidência específica e verificável de execução.
- Projetos sem comprovação após investigação ficam fora do catálogo ativo, em
  registro reavaliável. Projetos funcionais podem permanecer com automação
  temporariamente indisponível.

## Fidelidade da instalação

- Usar launcher oficial ou reproduzir fielmente suas operações documentadas.
- Permitir importadores, extratores, formatos de mídia, verificadores, dependências,
  toolchains, geradores/build oficiais, patches oficiais, staging e rollback.
- Não aplicar patches próprios a fontes upstream; não implementar shaders,
  gameplay, renderers ou runtimes faltantes; não desativar recursos para compilar.
- Uma mudança upstream indispensável exige autorização específica. Até lá,
  documentar e suspender a automação afetada.
- Não relaxar identidade/integridade da mídia. Não distribuir ROMs, ISOs ou assets.
- Preservar automações legítimas. Não reverter indiscriminadamente o desenvolvimento.
- Não distribuir nem executar componentes rejeitados; o histórico Git preserva
  as versões anteriores para auditoria.

## Repositórios e entrega

- Esta rodada pode alterar Allfix, GetAll-Addon e AllFix-Repo em branches dedicadas.
- Conferir status, commits, branches e worktrees; preservar alterações não versionadas.
- Fazer commits e pushes das alterações verificadas, sem force push.
- Não fazer merge em main, publicar releases, alterar version.json público,
  substituir instalação atual nem desenvolver DownloadAll.
- Addon leve/declarativo; ferramentas específicas obtidas sob demanda quando
  tecnicamente adequado. Justificar componentes incorporados ao Desktop.
- Preservar IDs e datas dos mantidos. Data do jogo e data do port são conceitos
  separados; nunca substituir added_at por data da última pesquisa.

## Verificação e armazenamento

- Executar validadores, regressões relevantes, parser/SDK e build de teste Desktop.
- Nunca promover receita a validated com schema, build ou fixture sintética.
- Não inventar hashes, tamanhos, evidências, resultados ou CI.
- Usar UTF-8 sem BOM e LF para arquivos de texto.
- Preservar fontes, receitas, scripts, manifests, hashes, logs e resultados.
- Reutilizar toolchains/caches. Remover somente intermediários e duplicatas
  comprovadamente descartáveis, após validação, sem pedir autorização repetida.
- Nunca remover mídia original, fonte não versionado necessário, dependência
  ativa ou dado pessoal.
- Registrar progresso real, pendências e comandos de reprodução no checkpoint.
