# Metaforce: instalação, recuperação e staging nativo

## Resultado fechado

O harness isolado compilou os Services do Desktop `8ba34eb51ee0ab93accef3da5e1689c68825977d`, os rascunhos Metaforce completos e as duas alterações de catálogo/provedor. Usou o SDK 1.5.68 já compilado no BUILD30 e .NET 8.0.425 existente. O build corrigido terminou com **zero erros e zero avisos**, em **8,719 s**. Nenhum arquivo do checkout Desktop foi modificado.

| Prova | Resultado | Tempo |
|---|---:|---:|
| Leitor de mídia, rodada anterior | 44 verificações aprovadas | 0,203 s |
| Política, transação, recuperação e ferramentas compartilhadas | 52 verificações aprovadas | 0,875 s |
| Configuração CMake e staging reais por C# | 19 verificações aprovadas | 18,828 s |

Não houve aceitação de mídia sintética como disco comercial, nem boot do jogo. A prova do staging consumiu o executável público previamente compilado pelo outro agente; não repetiu a compilação C++ completa. O primeiro build da nova prova apontou duas referências minhas a `Id`; o SDK usa `MediaId`. A correção ficou restrita ao novo serviço e ao teste. Os logs dessa tentativa também foram preservados.

## Implementação

`GameInstallationMetaforceBuild.cs` adiciona a conclusão e o lançamento ao perfil fixado. A conclusão revalida o recibo, o ZIP de fonte e o README interno. Exige uma referência ISO/GCM externa com SHA256 do arquivo completo e valida o DOL comercial com a identidade oficial. Um handle `FileAccess.Read`/`FileShare.Read` permanece aberto até a publicação terminar; a mídia é revalidada após o build. Nenhuma ISO é copiada para a instalação.

A publicação usa `RunPreparedBuildTransaction`: conserva o kit anterior, move a saída atomicamente e só então salva o registro final. A prova atravessou os caminhos reais de falha do build, cancelamento tardio e erro de gravação do registro após o move. Todos removeram somente a área de trabalho própria. O caminho de sucesso usou um produto autoral não executado; não foi apresentado como jogo construído.

`ConfigureMetaforceLaunch` verifica o snapshot imutável inteiro, o runtime e a mídia original antes de montar `ProcessStartInfo.ArgumentList` com `--dvd` e `--user-dir`. A pasta `AllFix-UserData/metaforce/<state.Id>` fica fora do manifesto dos binários e é preservada nas recuperações. O transporte de espaços e Unicode foi conferido com um processo real do runner. O cache de preferência do SDL pode continuar no perfil pessoal; esta implementação não o classifica como descartável.

`RollbackMetaforce` restaura somente o registro do kit de fonte fixado. A prova recusou recibo alterado, kit adulterado, destinos incorretos, cancelamento e falha de persistência. A recuperação bem-sucedida funcionou mesmo com a ISO temporariamente ausente e preservou o produto anterior, os saves e a mídia.

O `finally` do callback conserva somente os arquivos `.log` da pasta própria `work/metaforce-logs` antes da limpeza transacional. O limite é 64 arquivos e 512 KiB finais por arquivo, total máximo de 32 MiB. O manifesto informa cortes e omissões. SDKs, objetos, binários e pastas aninhadas não são copiados. O teste confirmou limites, integridade dos bytes de origem e recusa de uma área sem proprietário.

## Ferramentas e descoberta

A prova chamou `PrepareMetaforceSharedTool` real por reflexão com um ZIP autoral previamente validado no cache, sem rede. Conferiu primeira extração, reuso sem nova cópia, alteração de mesmo tamanho, arquivo adicional e cancelamento. O helper recusou árvores alteradas sem apagá-las ou substituí-las.

O caminho `Describe` realmente usado por `Discover` atribuiu rank 2 à tag fixa `build-de8fc69`; não houve flexibilização genérica da autorização experimental.

## Staging nativo C#

A prova usou `MetaforceConfigureArguments` e o ambiente privado de produção para uma configuração CMake em uma pasta nova. Não executou o alvo de compilação do jogo. `StageMetaforceNativeOutput` e `ValidateMetaforceOutput` reais produziram **89 arquivos**: executável + 9 DLLs, 19 recursos e 60 avisos. O método completo `BuildMetaforceNative` acrescenta seu recibo `allfix-build.json` depois desse estágio.

O executável e todas as DLLs/recursos foram comparados por tamanho e SHA256 com o inventário independente da compilação pública. Todos os conteúdos não vazios dos avisos também foram preservados, incluindo a normalização LF explicitamente validada para SQLite. A saída preparada carregou `--help` com PATH limitado às pastas Windows, sem toolchain no caminho. Os snapshots completos de fonte e dependências, o executável original, o CMakeCache anterior e a prova portátil anterior permaneceram inalterados.

A comparação independente é `metaforce-runtime-proof.json`, SHA256 `e84d98f3a0200d4fac2ba3b0ead3784667d4937df8f389414525b135cef5dd2c`. A revisão da fonte é `de8fc69bd7f345d6cf5f0c8fc2798295e22522d3`; o driver público final tem SHA256 `178ce9b95c1cdadffd77b47d8e1231d3a2b218864d6782b884177771e9953f29`.

## Evidências e reprodução

Raiz Windows:

`C:\Users\bradg\Downloads\GetAll-R18\evidence-r18\three-upstreams-20261127\metaforce-build-policy-proof`

- `inputs1.json` / `inputs2.json`: fontes, referências e hashes das duas compilações.
- `result2.json`: recibo final do build, da política e do staging.
- `build2.log`: compilação 0/0.
- `policy2.log`: marcador `METAFORCE_BUILD_POLICY_PASS checks=52`.
- `native-stage1.log`: marcador `METAFORCE_CSHARP_NATIVE_STAGE_PASS checks=19 files=89`.
- `authored-policy-1/result.json`: limites e escopo das fixtures.
- `csharp-native-stage-1/stage-result.json`: manifesto da saída real por C#.
- `csharp-native-stage-1/configure.log`, `configure-arguments.json` e `staged-help.log`: configurações e execução restrita.
- `proof-manifest.json`: hashes dos arquivos de continuidade.

O ZIP público foi verificado e mantido em `C:\Users\bradg\Downloads\GetAll-R18\console-cache\metaforce-de8fc69-source.zip` (21.536.851 bytes, SHA256 `e130131a1a41e8599541d8ab3dd2f31c6d8abaa9af03411f8bba25c3f5b63f21`). Não houve nova cópia de toolchain. A única imagem autoral gravada pela prova de política tem 8.192 bytes.

Rotas do runner isolado:

```text
MetaforceBuildProof.dll --build-policy <source.zip> <fresh-work>
MetaforceBuildProof.dll --native-stage <settings.json>
```

Os runners `BuildProofProgram.cs` e `MediaProofProgram.cs` são exclusivos da evidência e não devem entrar no glob do projeto Desktop. Os testes reutilizáveis são `MetaforceMediaIntegration.cs`, `MetaforceBuildIntegration.cs` e `MetaforceNativeStageIntegration.cs`; o teste de argumentos depende da rota autoral `--echo-args` do runner.

Dispatch compartilhado necessário na recuperação, antes de `FindLocal`:

```csharp
if (state.PreparationProfile == MetaforceProfile) return RollbackMetaforce(state, token);
```

Nenhum commit, push, mudança de SDK ou publicação foi executado por esta prova. A integração central e o SDK 1.5.69 permanecem sob coordenação do responsável pelo projeto.

## Hashes principais

- Serviço de instalação: `bc3b4418aa9081be01946ebc39be86c756dadc78214ec1155a038460ccd6dec5`.
- Serviço de mídia corrigido: `2190faee02f564d36a8602438054aebc677aa6a6eb553135b93ce901016d7d4e`.
- Log de política: `c86b78a6768a349152141a439f4a35ca0bbcda43005d3f06dcf71cb4fb3fb49d`.
- Log do staging: `3d5a5836f21eefa705b87842cf8f9d6727bf566067b8ee6764e1b01c1bd995b9`.
- Assembly isolado: `0ffc100a2f0864da26fa5a1fcf2fc3d4f049c58b368d6a5ae24db01a9a792b18`.
