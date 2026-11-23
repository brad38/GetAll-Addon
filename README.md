# GetAll-Addon — receitas oficiais para AllFix

Repositório público de **receitas declarativas** para o motor nativo do AllFix. Não contém ROMs, arquivos comerciais ou instaladores executáveis.

- `index.json`: índice de receitas (formato independente, versão 1).
- `recipes/`: receitas versionadas por jogo, projeto e release.
- `schemas/`: contratos JSON Schema do índice e das receitas.
- `addons/allfix.install.universal/`: documentos do addon declarativo universal.
- `docs/`: política de confiança, atualização, migração e rollback.

## Adicionar uma nova receita

1. Confirme `game_id`, `project_id` e `repository` no catálogo oficial [AllFix-Repo](https://github.com/brad38/AllFix-Repo/blob/main/catalog.json).
2. Consulte as instruções oficiais de uma tag específica; crie a receita conforme o schema suportado pelo SDK, sem scripts ou execução arbitrária.
3. Valide o JSON, as operações, os caminhos e o resultado da instalação. Publique com status `validated` apenas após validação efetiva.
4. Grave a receita em `recipes/<jogo>/<projeto>/<tag>.json`; compute SHA-256 sobre os **bytes UTF-8 publicados**.
5. Acrescente a entrada ao `index.json` no **mesmo commit** da receita e revise o hash. Nenhuma recompilação do aplicativo é necessária para receitas compatíveis.
6. Reverter o commit ou marcar a entrada como `disabled` permite rollback.

Versões independentes: `index_format_version` (índice), `schema_version` (receita) e `manifest.version` (addon).

## Segurança

A versão inicial do host aceita somente a origem fixa `https://raw.githubusercontent.com/brad38/GetAll-Addon/main/`, acessada por HTTPS e sem redirecionamentos. O índice não pode definir URLs arbitrárias; caminhos de receitas são relativos a `recipes/` e seguem um formato restrito. O host valida o SHA-256, os metadados, o schema, o conjunto de operações e a segurança de caminhos **antes** de executar a receita, e mantém cache local seguro.

**Limitação do modelo de confiança:** um SHA-256 armazenado no mesmo índice comprova consistência, não é uma assinatura independente. A autoridade vem da propriedade e do controle do repositório GitHub fixado; o comprometimento da conta ou da branch pode publicar dados maliciosos. Exija MFA, revisão por pull requests, proteção de branch e privilégios mínimos. Assinaturas digitais independentes ficam para uma evolução posterior.

## Compatibilidade e migração

Addons locais existentes mantêm precedência sobre receitas remotas para a mesma release. Para testar a fonte remota do SM64 Coop Deluxe v1.5.1, desative temporariamente `allfix.install.sm64coopdx` e ative `allfix.install.universal`. Para voltar, reative o addon local e desative o universal. Nenhum arquivo do addon antigo precisa ser removido.

O addon universal é declarativo, sem DLL, executável ou runtime.
