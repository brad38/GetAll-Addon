# Metaforce: prova isolada do leitor de mídia

## Resultado

O rascunho `GameInstallationMetaforceMedia.cs` passou 44 verificações dirigidas após corrigir uma rejeição indevida de arquivos vazios na FST. A alteração exige `Size > 0` antes de tratar um intervalo como sobreposição. O leitor compartilhado real `ReadNintendoFst` já aceita arquivos vazios com offset zero; a verificação adicional do rascunho contradizia esse contrato.

A reprodução inicial compilou os Services do Desktop SDK 1.5.68, commit `8ba34eb51ee0ab93accef3da5e1689c68825977d`, e rejeitou uma fixture autoral de 8 KiB com um arquivo vazio. O log `baseline2-empty-member.log` registra a exceção na verificação adicional. Após o patch, a mesma fixture passou, assim como a matriz completa. O build final isolado terminou com zero erros e zero avisos em 8,375 s; a matriz levou 0,203 s.

## Escopo comprovado

- Layout autoral limitado, posição inicial arbitrária do stream, diretórios reais da FST e arquivos vazios.
- Rejeição de região, revisão, número de disco e magic incorretos.
- DOL e FST truncados, limites, sobreposição de seções/áreas, entrada de código inválida, nomes e hierarquia inválidos, traversal e ausência de recursos PAK.
- Cancelamento antes da leitura, durante DOL/FST e entre blocos do SHA.
- Rejeição da fixture pelo hash comercial, tanto por stream quanto por caminho Unicode com extensão GCM.
- Transporte de `--dvd`/`--user-dir` com espaços e Unicode por `ProcessStartInfo.ArgumentList` até um processo real do próprio runner; o teste não executa o jogo.

O SHA1 comercial permaneceu `949c5ed7368aef547e0b0db1c3678f466e2afbff`, conferido nos arquivos oficiais arquivados `config/GM8E01_00/config.yml` e `build.sha1`. A maior fixture contém 147.456 bytes e existe somente em memória; os dois arquivos de teste gravados têm 8.192 bytes cada. Nenhuma mídia original foi usada; não houve boot comercial, build nativo do Metaforce ou integração ao Desktop.

## Reprodução

A prova Windows está em:

`C:\Users\bradg\Downloads\GetAll-R18\evidence-r18\three-upstreams-20261127\metaforce-media-proof`

O projeto isolado `MetaforceMediaProof.csproj` foi derivado do harness real: liga os Services e recursos existentes e referencia os assemblies já compilados do BUILD30. Não copia SDKs/toolchains e não altera o projeto Desktop. O logger de console é o mesmo definido pelo harness oficial; não há substituto do leitor FST.

Com o .NET 8.0.425 existente:

```powershell
& 'C:\Program Files\dotnet\dotnet.exe' build '<prova>\MetaforceMediaProof.csproj' -c Release --nologo --no-restore
& 'C:\Program Files\dotnet\dotnet.exe' '<prova>\bin\Release\net8.0\MetaforceMediaProof.dll' --empty-member
& 'C:\Program Files\dotnet\dotnet.exe' '<prova>\bin\Release\net8.0\MetaforceMediaProof.dll' --all '<nova-pasta-de-fixtures>'
```

`--all` recusa uma pasta existente. Os scripts de execução preservados usam logs exclusivos e não devem ser reaplicados cegamente sobre os recibos existentes. A primeira compilação isolada falhou por faltar o logger do harness; esse erro de montagem ficou registrado em `baseline-build.log`, antes da reprodução válida em `baseline2-*`.

## Artefatos

- `baseline-inputs.json`: commit, referências reais e pin oficial arquivado.
- `baseline2-harness-input.json`: origem e hash do logger/runner.
- `baseline2-result.json` e logs: reprodução da falha com o código original.
- `original-media-source.cs.txt`: bytes originais preservados.
- `final-result1.json`, `final-build1.log`, `final-empty-member1.log`, `final-media1.log`: resultados finais.
- `authored-media-final-1/result.json`: contagem e limites das fixtures.
- `proof-manifest.json`: inventário dos arquivos necessários à reprodução e seus hashes.

SHA256 do Media corrigido: `2190faee02f564d36a8602438054aebc677aa6a6eb553135b93ce901016d7d4e`.
SHA256 do teste: `07d280352814f35212923738466701a82f5d5b8deebffb23027dd9f68eaa4135`.
SHA256 do log final da matriz: `5bf675c7ada048c87938daf1b0abb4abfd7459172e6e3e0a99d98f6a56cc394b`.

O Desktop continuou no commit 8ba34eb, sem alterações, depois da prova. O rascunho Linux está pronto para a integração coordenada pelo responsável pelo provider Metaforce.
