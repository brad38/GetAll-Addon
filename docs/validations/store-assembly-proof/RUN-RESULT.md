# Serviços reais da Loja — SDK 1.5.69

**PASS: 20 verificações**, executadas em 27/11/2026 às 21:49, America/Fortaleza
(28/11/2026 às 00:49 UTC nos recibos). O teste carregou o `AllFix.dll` real do
Desktop `921295de12349e726f7ca21a5edd8a8ecee123d8`, com as dependências produzidas
pelo `dotnet publish`. Nenhum serviço, cache ou transporte HTTP foi substituído.

| Etapa | Resultado | Tempo |
| --- | --- | ---: |
| SDK compartilhado | .NET 8.0.425, exit 0 | 0,093 s |
| Compilação offline do runner | exit 0, sem pacote adicional | 0,985 s |
| Serviços reais por reflexão | 20 PASS, exit 0 | 0,250 s |

O SHA256 do DLL testado é
`3c6ad7c8909888c13452777db37a6ddea940281f533b8588ba0852984ca2c44d`.
Ele coincide com o DLL extraído e auditado do candidato distribuído. O teste
confirmou a identidade do alias local MKW, duas resoluções do pacote fixado,
12 URLs alteradas recusadas, catálogo com e sem refresh, combinação de cache
malformado e **zero requisições HTTP iniciadas**. O marcador final é
`MKW_CLI_STORE_ASSEMBLY_PASS checks=20`.

O Git do Desktop, o DLL testado e o candidato permaneceram idênticos antes e
depois. A execução não abriu a interface do All-Fix, não instalou o addon,
não preparou mídia e não verificou boot comercial.

## Execução e reprodução

O Desktop é self-contained. Por isso a prova usa o runtimeconfig framework-dependent
do próprio runner; `AssemblyDependencyResolver` lê o manifesto real do Desktop
para resolver as dependências adjacentes. Não é necessário recompilar o Desktop.
`NuGet.Config` bloqueia fontes de pacotes e `global.json` seleciona o SDK já
instalado. [run-proof.py](run-proof.py) verifica os pins, compila o runner em
saída nova, executa as 20 verificações e registra os comandos e invariantes.

```powershell
python run-proof.py --task-root 'C:\Users\bradg\Downloads\GetAll-R18' `
  --output 'C:\Users\bradg\Downloads\GetAll-R18\evidence-r18\store-proof-new-run' `
  --desktop-commit 921295de12349e726f7ca21a5edd8a8ecee123d8 `
  --candidate-manifest-sha256 aa85bbe915f2a8d975a8fa0139dea79d145d8c0a0107464941505a7f528a01e3 `
  --candidate-executable-sha256 b558afccf6fa50ec9a3899b66055009f04f8ce71cfc4dbcc6ab3886bd0433fcd
```

## Evidências

[result.json](result.json), [build.log](build.log) e
[store-services.log](store-services.log) preservam o resultado completo.
O recibo original Windows tem 3.868 bytes e SHA256
`22804295925878e3a43bb1173109bd68a5728dc48db63723a1347862abd8c69f`.
A cópia no Git usa UTF-8/LF e tem SHA256
`7400a11b62a76447229478ba2d94f152659ef6a733d23296f07bb81d6cddbbfe`.
[source-transfer.json](../sdk169-preview/source-transfer.json) registra os hashes,
tamanhos e codificações de origem e das cópias normalizadas. Os originais
continuam preservados no diretório de evidências Windows.
