# GetAll-Addon — receitas oficiais para AllFix

Repositório público de **receitas declarativas** para o motor nativo do AllFix. Não contém ROMs, arquivos comerciais ou instaladores executáveis.

- `index.json`: índice de receitas (formato independente, versão 1).
- `recipes/`: receitas versionadas por jogo, projeto e release.
- `schemas/`: contratos JSON Schema do índice e das receitas.
- `addons/allfix.install.universal/`: documentos do addon declarativo universal.
- `docs/`: política de confiança, atualização, migração e rollback.

## GetAll-Addon v1.0.0 — instalar e usar

**Download oficial:** [GetAll-Addon.zip (Release v1.0.0)](https://github.com/brad38/GetAll-Addon/releases/tag/v1.0.0)

- **Instalação:** baixe o arquivo original `GetAll-Addon.zip`, abra o AllFix e entre em **Loja de Jogos → Complementos → Adicionar complemento**. Selecione o ZIP e confira o hash apresentado antes de confirmar.
- **Ativação:** abra **Gerenciar** no card do complemento `allfix.install.universal` e ative-o. O host consulta o índice de receitas remotas automaticamente quando necessário.
- **Atualização do complemento:** baixe o ZIP de uma nova Release, mantenha o ID `allfix.install.universal` e importe a versão superior pelo mesmo gerenciador. O AllFix confere a integridade e mantém a ativação, quando aplicável. **Novas receitas** podem ser publicadas no índice sem atualizar o complemento.
- **Reversão:** para suspender as receitas remotas, desative o complemento no gerenciador. Caso também use o addon antigo `allfix.install.sm64coopdx`, reative-o para usar sua receita local; receitas locais válidas têm precedência sobre remotas. Não é necessário remover jogos nem dados do usuário.
- **Integridade do pacote original v1.0.0 (SHA-256):** `3D99BAF35515DE6E2DB6DE16CD6A3D4AF071508F5201DC95DD75BBD7CF6DB0C4`. O ZIP não contém DLLs, executáveis nem ROMs.

As versões de SDK e protocolo são independentes: o addon v1.0.0 utiliza a API declarativa `1.0` e a capacidade `installation.recipe.remote`, disponível desde o SDK `1.1`. O SDK `1.2.0` acrescenta o contrato de receitas v4 sem exigir alteração do ZIP universal.

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

## Cobertura do catálogo — auditoria de novembro de 2026

A análise integral de [87 jogos e 119 projetos](docs/AUDITORIA-CATALOGO-2026-11-22.md) classifica o suporte como **A (compatível estruturalmente), B (parcial), C (fora do SDK atual) ou D (informações insuficientes)**. A classificação A não substitui o teste funcional.

- [Matriz completa dos projetos e Releases](docs/AUDITORIA-CATALOGO-2026-11-22.md)
- [Capacidades genéricas pendentes para o Codex](docs/CAPACIDADES-PENDENTES-2026-11-22.md)
- [GoldenEye 007 PC Port v0.5.0 — validação estática e pendências](docs/GOLDENEYE-V0.5.0-VALIDACAO.md)
- [Rodada SDK 1.2.0: contratos v4, testes integrados e bloqueios concretos](docs/RODADA-SDK-1.2.0-2026-11-23.md)

**Índice atual:** 14 receitas — SM64 Coop Deluxe v1.5.1 segue `validated` e as outras 13 permanecem `experimental` (não descobertas automaticamente pelo host). Com o SDK 1.2.0, a receita experimental GoldenEye v0.5.0 passou a exigir também `libstdc++-6.dll`; ainda não foi homologada com ROM legítima. O ZIP universal v1.0.0 foi preservado.
