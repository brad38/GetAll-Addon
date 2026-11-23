# GetAll-Addon — Rodada 13: Crash Team Racing Turbocharged via artefato oficial de CI

Data: 2026-11-23. Branch: `feat/round-13-trusted-ci-turbocharged`, criada a partir da branch do PR #12; nenhum merge nem release foi feito.

## Descoberta

A matriz anterior classificava `crash-team-racing-turbocharged` como apenas codigo-fonte, pois a API de GitHub Releases de `CameronRedmore/Crash-Team-Racing-Turbocharged` estava vazia. Contudo, o [site oficial do proprio desenvolvedor](https://ctr.cmzi.uk/) apresenta download Windows, e o [workflow Build native PC builds](https://github.com/CameronRedmore/Crash-Team-Racing-Turbocharged/actions/workflows/build-native.yml) produz um ZIP para Windows x86 com `actions/upload-artifact` (com `archive: false`), mesmo sem criar uma GitHub Release.

- Repositorio oficial: `CameronRedmore/Crash-Team-Racing-Turbocharged`.
- GitHub Actions run: `37521206289`, commit oficial `07d0c49f01d62dcb9887b455be27ce65728ee893`, sucesso.
- ID do artefato: `11439483665`.
- Nome: `ctr-turbocharged-turbocharged-07d0c49-windows-x86.zip`.
- Download oficial: `https://ctr.cmzi.uk/api/download/11439483665`.
- Tamanho: **6.569.952 bytes**.
- SHA-256 do artefato informado pela API GitHub Actions: `dcba6c0a0c71211a568b8760f0c44fb159724f5f90b87cbbe25328e68786a30f`.
- SHA-256 recalculado do ZIP baixado: **identico**.
- Criado em 2026-10-06; expiracao informada pelo GitHub: **2027-01-04 19:44:11 UTC**. A entrega e transitoria, exigindo renovacao/publicacao de release permanente para uso futuro.

### Evidencias do ZIP real

O ZIP foi inspecionado sem executar seu EXE. Entradas confirmadas incluem:

- `ctr-turbocharged-turbocharged-07d0c49-windows-x86/Crash Team Racing - Turbocharged.exe` (12.714.674 bytes)
- `.../assets/dualshock.png` (1.054.852 bytes)
- `.../assets/fonts/LuckiestGuy-Regular.ttf` (73.320 bytes)
- `.../README.txt` (2.038 bytes)

O jogo **nao inclui o disco comercial**. Seu README orienta fornecer uma copia licita NTSC-U em BIN de setores MODE2/2352; um ISO 2048 nao funciona. O jogo copia dados para `assets/ctr-u.bin` por assistente de primeiro uso. Nenhuma ROM/ISO foi fornecida nem executada.

## Nova candidata GetAll

`recipes/crash-team-racing/crash-team-racing-turbocharged/ci-07d0c49.json`, schema v5, tag `ci-07d0c49`, indice com `status=experimental`; caminho do EXE com espacos, operacoes vazias, `manual_steps` para a imagem comercial. Hash SHA-256 exato dos bytes da receita: `943f43da0758ee982b0f4373d25e3f74a5a8718eb066822f41200543e84b9b18`.

Esta candidata **nao funciona no All-Fix Desktop 3.0.0 publicado sem o provedor CI**. O frontend tradicional filtra URLs que nao sejam `github.com/.../releases/download` e a API antiga busca somente Releases. Para nao incluir uma receita artificial, foi desenvolvida, em copia isolada da arvore local recente do Desktop, uma adaptacao restrita de origem CI, ainda nao substituindo DLL ou executavel instalados.

## Adaptacao restrita do Desktop (sem schema v9)

Arquivos do pacote de integracao local:

- `Services/StoreTrustedCiArtifacts.cs`: whitelist de repositorio, run ID, artefato, tag, nome, tamanho, hash e expiração; origem/URL exatas. Uma origem externa nao definida na whitelist nao pode ser declarada por receitas JSON.
- `Services/StoreCatalogService.cs`: exibe uma release virtual, claramente marcada como CI e temporaria, somente para o repositorio aprovado.
- `Services/StoreDownloadService.cs`: autoriza exclusivamente o download aprovado, confirma tamanho e SHA-256 apos o download, limita redirecionamentos a HTTPS com caminho `/actions-results/` e assinatura de Azure Blob.
- `Web/store.js`: permite a URL aprovada sem permitir domínios arbitrarios.
- `Tests/AddonInfrastructure`: positivos e negativos para URL exata, repositorio/tag, expiracao, protocolo/host/path de redirecionamento e staging oficial.

Nada permite `cmd`, `powershell`, script upstream, instalador desconhecido, comandos arbitrarios ou desvio de hash. A versao do SDK **1.4.1**, schemas v1-v8 e aplicativo **3.0.0** permanecem inalterados porque nao houve mudança do contrato de receita; foi ampliado somente o mecanismo local de distribuicao de pacote oficial.

## Verificacoes executadas

| Verificacao | Resultado |
|---|---|
| SHA-256 do ZIP contra digest da API GitHub Actions | PASS |
| Inspecao estatica do conteudo ZIP | PASS |
| JSON Schema Draft 2020-12, integridade e catalogo proposto | 94/94 PASS |
| Python unit tests | 36/36 PASS |
| Parser C# 1.4.1: todas as receitas | 94/94 PASS |
| Build do Desktop em copia isolada | PASS sem erros/avisos |
| Validacao de URL, expiração e redirect host (harness C#) | PASS |
| Teste de staging no GameInstallationService com ZIP real | **PASS**, status `PartiallyCompleted`, EXE presente, BIN comercial ausente |
| Primeiro boot real / jogo `validated` | NAO executado |

## Estado e dependencia de merge

Main atual: **92/119**. Branch da Rodada 12: **93/119** (Project Picori). Branch da Rodada 13: **94/119 propostas**, 93 `experimental` e uma `validated`. Projetos ainda sem receita: **25**. A nova receita requer incorporacao do provedor CI ao projeto local recente do Desktop antes de ficar instalavel na UI. Depois, ainda exige mídia comercial legítima e homologação do primeiro boot para promocao a `validated`.

Sem autorizacao do usuario, nao fazer merge, instalar DLL, alterar versao 3.0.0 nem publicar release. Nenhuma prova de homologacao comercial foi inventada.

## Limpeza

O workspace dedicado `%TEMP%\AllFix-R13-20261123` contem copia isolada do Desktop, fonte GetAll, ambiente de teste, ZIP oficial baixado e evidencias do parser. O teste de staging remove automaticamente seu proprio diretorio `AllFixCiStaging-*` ao final; nenhum arquivo do usuario ou de outro agente deve ser removido. Preservar o pacote final de integracao e este relatorio; limpar somente residuos desta rodada apos empacotamento.
