# Complemento de prévia — SDK 1.5.70 / addon 1.5.76

O complemento é declarativo e fixa um commit de receitas e um commit de
catálogo revisado. Seus dois arquivos JSON não contêm binários nem mídia.

| Campo | Valor fixado |
|---|---|
| ID do complemento | `allfix.install.universal.preview` |
| Versão do complemento | `1.5.76` |
| SDK mínimo | `1.5.70` |
| Commit GetAll | SHA completo do commit final desta branch, registrado no recibo do pacote |
| Commit do catálogo | `e4fdde9d7c128f79eb19cf99ea07e2e9b628127a` |
| Entrada | `responses.json` |
| Capacidade | `installation.recipe.remote` |

A versão de teste foi incrementada de 1.5.75 para **1.5.76** porque os
contratos e pins mudaram. Assim, o registry não confunde os dois payloads
com a mesma identidade de versão; não se presume que o arquivo anterior nunca
tenha sido importado. A versão pública permanece inalterada.

## Gerar o ZIP

Execute na raiz do checkout GetAll que contém o commit informado. O caminho de
saída deve ainda não existir; o empacotador não sobrescreve uma prévia anterior.

```bash
getall_preview_revision=$(git rev-parse HEAD)
python scripts/package_preview.py "$getall_preview_revision" e4fdde9d7c128f79eb19cf99ea07e2e9b628127a 1.5.76 GetAll-Addon-preview-1.5.76.zip --min-sdk 1.5.70
```

Em PowerShell, atribua `$getallPreviewRevision = git rev-parse HEAD` e passe
`$getallPreviewRevision` como primeiro argumento do mesmo comando Python. A geração é
local e não publica release. Antes de distribuir uma prévia utilizável, confirme
que **ambos** os commits foram enviados ao GitHub e que o Desktop usa SDK
1.5.70 ou superior. Um ZIP local válido não comprova que os commits já estão
acessíveis remotamente, nem que o build Windows passou.

## Recibo local e pin final

O pacote final deve ser gerado depois do commit de código/documentação, para
incluir a revisão mais recente. Preserve ao lado do ZIP o SHA-256, tamanho,
nomes dos dois membros, manifesto e referências lidos de dentro do arquivo.
O recibo preliminar da versão anterior 1.5.75 está em
[preview-addon-1.5.75-preliminary.json](validations/official-scope/preview-addon-1.5.75-preliminary.json).
A versão 1.5.75 registra a primeira prova do empacotador e não substitui o pin do pacote
final. O SHA final é entregue com o pacote, evitando uma referência circular
entre o commit e um arquivo que precisaria conter o próprio SHA desse commit.
Nenhum recibo de empacotamento declara push, CI hospedado ou build Windows.

## Conferir os bytes e as referências

```bash
python -m zipfile -l GetAll-Addon-preview-1.5.76.zip
```

A lista deve conter somente `addon.json` e `responses.json`. Em `addon.json`,
confira versão `1.5.76` e `min_sdk_version: 1.5.70`. Em `responses.json`, confira
`repository: brad38/GetAll-Addon`, `ref` e `catalog_ref` iguais aos SHAs da tabela.
No PowerShell, calcule o hash do ZIP com:

```powershell
Get-FileHash .\GetAll-Addon-preview-1.5.76.zip -Algorithm SHA256
```

O esquema do manifesto e a imutabilidade dos dois pins são cobertos por
`tests/test_preview_package.py`. O índice e o catálogo precisam passar nos
validadores e o parser Desktop precisa aplicar as regras de fidelidade. O
complemento só seleciona a origem; não comprova a execução de nenhum jogo.

## Importar para revisão

Abra a instalação de teste do Desktop, entre em Loja de Jogos → Complementos
→ Adicionar complemento, selecione o ZIP e confira a identidade e a versão.
Ative o complemento de desenvolvimento em Gerenciar quando quiser usar o
catálogo revisado. O pacote não ativa o canal sozinho. Esta etapa é separada
da instalação corrente do usuário e não altera a versão pública.
