# Segurança e migração

- A origem remota é fixada no host em `brad38/GetAll-Addon`, branch `main`, por HTTPS sem redirects. O addon não escolhe URLs livres.
- O SHA-256 indexado detecta conteúdo divergente, mas não prova autenticidade contra o comprometimento da conta/branch. Recomenda-se MFA, proteção de branch e revisão por pull request.
- O índice é armazenado atomicamente, com fallback a último índice válido. Receitas são cacheadas por hash e só são aceitas após validação de metadata, schema e operações pelo motor.
- A rede é consultada antes da instalação, nunca durante execução de operações. Versões sem receita não são anunciadas como compatíveis.
- A precedência das receitas locais existentes é maior que a do repositório. Para usar SM64 via GetAll, desative (sem excluir) `allfix.install.sm64coopdx` e ative `allfix.install.universal`. Reverter essa escolha restaura o comportamento anterior.
- Nunca enviar ROMs, arquivos protegidos ou instaladores ao repositório. Uma nova receita requer teste por release, hash sobre bytes finais e atualização conjunta de índice/receita.
