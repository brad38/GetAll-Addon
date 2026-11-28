# Auditoria de integridade — FH1, Pinyon e SSX

## Resultado

**Houve alteração de código-fonte de terceiros e substituição de componentes de runtime.** Os três fluxos usam cópias modificadas dos SDKs; FH1 e Pinyon também dependem de pontes C/C++ próprias para NVIDIA NGX, e Pinyon de uma ponte ETW. Portanto, não são apenas receitas que baixam e executam o launcher oficial.

**Foram encontradas duas reduções concretas de recursos:** Pinyon desabilita o caminho FidelityFX de FSR 2/3 temporal e de geração de quadros; FH1 omite sempre o renderer experimental ReGPU que o launcher oficial tenta compilar no Windows. Esses pontos não podem ser descritos somente como ajustes de compilador.

Nos diffs examinados destes três projetos, **não foi encontrada implementação própria de gameplay faltante nem substituição de funções comerciais por stubs no caminho de produção**. Há uma fachada sintética em um teste de Pinyon, explicitada abaixo. Compilação, carregamento de DLLs e testes de imagem sintética não comprovam que os jogos iniciam ou estão completos.

## Escopo e método verificável

- Desktop: commit `921295de12349e726f7ca21a5edd8a8ecee123d8`.
- GetAll: commit `ceaa962fe1a2088a7f3900509b856743ff4b6672`.
- Projetos: `fh1-reimagined`, `pinyon-shift`, `ssx-recomp`.
- Foram examinadas todas as **86 entradas dos três manifests de overlay: 82 textos e quatro binários DLL/LIB**, mais as alterações C# em dois CMake do jogo FH1 e no CMake de geração do SSX, fora desses manifests. As fontes das pontes e os consumidores de teste também foram lidos.
- Todos os hashes de preimage e replacement dessas 86 entradas foram confrontados com os bytes reais dos arquivos/arquivos ZIP preservados. Os caminhos declarados como novos estavam ausentes dos originais. Não se usou a justificativa de `ORIGIN.json` como prova da natureza da alteração.
- Foram reaplicados **22 patches oficiais em memória**, obtidos diretamente dos ZIPs originais: dois do SDK FH1 e vinte do repositório SSX. Não houve erro de aplicação. O resultado de **32 textos de overlay** coincide com esses patches oficiais: quatro em FH1 e 28 em SSX. Para essa comparação textual foi normalizado apenas CRLF para LF; a verificação SHA-256 de entrada e saída usa os bytes sem normalização.
- O cache CMake real da qualificação final do Pinyon foi lido para verificar se as flags desabilitadas chegaram à configuração usada.

O inventário completo, os hashes por entrada, os diffs residuais das nossas alterações e as evidências estão em [rex-review.json](rex-review.json). O script [replay-rex-provenance.py](replay-rex-provenance.py) reproduz a comparação usando os arquivos já existentes no Windows; lê arquivos, aplica patches somente em memória e imprime JSON. Esta auditoria não recompilou SDKs, não executou jogos e não alterou fontes, receitas ou dados do Windows.

| Fluxo | Origem efetivamente comparada | Entradas do overlay | Coincidem com patches oficiais | Alterações locais adicionais |
|---|---|---:|---:|---|
| FH1 | `FH1-ReImagined/ReIGlue@18fa1cc468d4d8b3a2ee5aa8f0480bae68e734b9`, ZIP SHA-256 `e0d27948ac36bdd1499182d1f75910e3e8805e2c984f0a8042b27bad6ed3826d` | 20 textos | 4 | 16 textos do overlay; dois CMake do jogo; ponte NGX fornecida no suporte |
| Pinyon | `arcanite24/shiftglue-sdk@0c2187cbdc1857029550f510f4d3d5bee36a57a6`, ZIP SHA-256 `aa1d44cb4110953d53e7693021949dcbcc69429b09f15e78bd753169e2169f96`; source ZIP oficial do kit SHA-256 `0d0ef7fc980366c2564128f619aee2ecc859bd4fd2723c0dc32ab55769df3f81` | 19 textos + 4 binários | 0 | 14 textos existentes do SDK, oito entradas novas de suporte e um CMake do jogo |
| SSX | `rexglue/rexglue-sdk@bd833a2ab69d305f99ddf57418fc38ffec8af93d`, ZIP SHA-256 `e9678e260713a11d716f7870547f53c6e7fcae8eb979f6ab78c1c96dcdcaecfe`; jogo `717a7a93e1ca652b046f4f76ec46ab8758c5d80f`, ZIP SHA-256 `1b48d42db48d3eff77ed0dbabac4ecb7e572421afa536c0611190748ec6e7327` | 43 textos | 28 | 13 textos do SDK, dois do jogo e um CMake de geração fora do overlay |

## REX-01 — Pinyon perde FSR 2/3 temporal e geração de quadros FidelityFX

**Constatação de configuração funcional, prioridade alta para revisão do produto.** `GameInstallationPinyonNative.cs`, linha 159, e `GameInstallationPinyonBuild.cs`, linha 116, fixam `REXGLUE_FFX_API_LOADER=OFF` e `REXGLUE_FIDELITYFX_RUNTIME=OFF`.

No SDK original, `cmake/rexglue_ffx_api_headers.cmake`, linhas 16–27, habilita o loader por padrão e retorna cedo quando ele está desabilitado. `cmake/rexglue_helpers.cmake`, linhas 11–13, habilita o staging do runtime por padrão. `src/ui/CMakeLists.txt`, linhas 168–170, somente define `REX_HAS_FFX_API` quando os headers desse caminho existem. O código original `src/ui/vulkan/vulkan_ffx_upscaler.cpp`, linhas 765–777, só registra os provedores FSR 2 e FSR 3 com essa macro; a criação do gerador de quadros retorna `nullptr` sem ela.

O arquivo real `pinyon-production27/preflight/native-sdk-build/CMakeCache.txt`, SHA-256 `9cf5a23bde5633945efdd2574adbfcf79f4f9839fc392077d7e9870f75fd0697`, confirma `REXGLUE_ENABLE_FIDELITYFX`, `REXGLUE_FFX_API_LOADER` e `REXGLUE_FIDELITYFX_RUNTIME` em `OFF`. D3D11, D3D12, Vulkan e o provider DLSS estão em `ON` nesse mesmo cache.

O alcance é específico: **FSR 1 e CAS continuam em outro caminho de shaders; DLSS e LSFG também são implementações distintas**. Não é correto dizer que todo FidelityFX/FSR foi removido, mas é igualmente incorreto apresentar essa configuração como preservação integral das opções do upstream.

Fontes: [configuração AllFix do SDK](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationPinyonNative.cs), [configuração AllFix do jogo](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationPinyonBuild.cs), [loader oficial](https://github.com/arcanite24/shiftglue-sdk/blob/0c2187cbdc1857029550f510f4d3d5bee36a57a6/cmake/rexglue_ffx_api_headers.cmake), [provider oficial](https://github.com/arcanite24/shiftglue-sdk/blob/0c2187cbdc1857029550f510f4d3d5bee36a57a6/src/ui/vulkan/vulkan_ffx_upscaler.cpp).

## REX-02 — FH1 omite ReGPU sem tentar a compilação oficial

**Constatação de redução de opção gráfica.** `GameInstallationForzaNativeGame.cs`, linha 95, força `FORZA_REGPU_PLUGIN=OFF`. A lista fechada de publicação `ForzaNativeDllNames` não inclui `rexgpu-regpu.dll`.

A comparação foi além do comentário do CMake: o arquivo oficial `launcher/forza_launcher/builder.py`, revision `46d5ed62866af68700d15c61748df8c29ad0248d`, foi obtido pelo GitHub e conferido contra o blob Git `94f132bf0d142d52f37b788ad316764da2e2cd61`. Na linha 1298 ele habilita ReGPU no Windows; na linha 1316 passa a opção correspondente; nas linhas 1324–1327 só desabilita após uma falha identificada como exclusiva do plugin.

O CMake isolado tem default `OFF`, mas **o fluxo do launcher Windows usa `ON` primeiro**. AllFix omite a tentativa e o recurso. O renderer Xenos permanece, portanto este achado não equivale a afirmar que FH1 não pode renderizar; demonstra uma diferença efetiva em relação ao caminho oficial.

Fontes: [configuração AllFix](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationForzaNativeGame.cs), [builder oficial verificado](https://github.com/FH1-ReImagined/ForzaHorizon1-ReImagined/blob/46d5ed62866af68700d15c61748df8c29ad0248d/launcher/forza_launcher/builder.py).

## REX-03 — Modificações próprias no runtime e na compilação

### FH1

As diferenças próprias incluem adaptação dos exports e nomes de DLLs; Win10/COM/DXC/XInput; correção do caminho executável com `GetModuleFileNameW`; remoção do registro global de pacote CMake; guarda de header UCRT do FFmpeg; substituição da compilação FidelityFX por uma DLL C ABI fixada; e uma ponte NGX própria. O arquivo de renderer `src/graphics/vulkan/fh1_dlss.cpp` é alterado para chamar essa ponte em criação, avaliação, parâmetros, encerramento e configurações ótimas de DLSS. O acesso à API anterior já existia: não foi criado um renderer DLSS do zero, mas a ligação e o gerenciamento de handles foram modificados.

O bridge encaminha para as funções NVIDIA reais, valida handles e layout e devolve falha em exceções; o catch silencioso encontrado é de logging/destruição, não um retorno genérico de sucesso de gameplay. Isso ainda é código de runtime que precisa de qualificação no uso real.

No fonte específico do jogo, os dois CMake modificados ajustam nomes de módulos, `-municode` e recursos Windows. As funções comerciais continuam vindo dos três módulos XEX originais e da geração oficial. Não apareceu alteração própria de fases, regras, carros, missão ou física nesses diffs.

### Pinyon

Foram alterados CMake, exports, aliases CRT, includes e GUIDs COM/DXC, XInput, o contador ETW e o provider Vulkan DLSS. Foram acrescentadas pontes NGX e ETW. O diff do header `allfix_d3d11sdklayers.h` foi comparado com o header real da toolchain preservada: a mudança é acrescentar `D3D11_RLDO_IGNORE_INTERNAL = 4` ao enum, não implementar funções Direct3D substitutas.

A ponte ETW preserva o GUID e os nomes/campos dos dois eventos existentes; usa as chamadas TraceLogging reais. A ponte NGX encaminha SR e FG para a biblioteca real. O teste histórico de SR com imagem sintética não testa geração real de quadros nem o jogo.

O único arquivo do fonte do jogo no overlay é `cmake/PinyonShiftRexGlue.cmake`: troca `/Brepro` por `--no-insert-timestamp` sob MinGW. A exclusão de seis unidades dependentes do guest ocorre no modo de prova pública **já existente no upstream**. `CompletePinyonPreparation` passa `hostOnly=false`, exige a geração dos três módulos e copia os produtos do build real.

Tracy desligado coincide com o próprio CMake do jogo original. DLSS desligado por padrão é uma escolha exposta ao usuário em `MainWindow.StoreGameInstallation.cs`, linhas 335–344. Esses dois casos não têm o mesmo problema do FidelityFX desabilitado incondicionalmente descrito em REX-01.

### SSX

Depois de remover as diferenças explicadas pelos vinte patches oficiais, restam adaptações de ABI/build, caminho executável, CMake privado, conversão de relógios libc++ já existente para Apple, constante WIC `HighQualityCubic = 4`, link explícito de `windowscodecs` e suporte FidelityFX C ABI. O trecho `generated/rexglue.cmake` alterado por `AdaptSsxCodegenCmake` acrescenta um modo de cache: só pula a geração quando `TryRestoreSsxCodegenCache` validou a identidade da mídia, atualização, gerador e arquivos do cache. Se não há cache válido, o codegen real continua obrigatório. Esse no-op é do alvo de regeneração, não uma função do jogo.

Fontes: [FH1 source overlays](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationForzaNativeSources.cs), [Pinyon source overlays](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationPinyonNativeSources.cs), [SSX cache](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationSsxCache.cs). Os diffs completos das alterações residuais existentes estão no JSON desta auditoria; headers novos extensos continuam no pacote fixado, com identidade registrada no JSON.

## REX-04 — A prova de fachadas Pinyon usa DLLs sintéticas

O arquivo `Tools/PinyonNative/source-support.zip!probe/facade.cpp` contém uma função exportada que retorna `0x27`. `probe/entry-CMakeLists.txt` compila essa função em duas DLLs **com os nomes das fachadas do jogo**, para conferir o carregamento por nome e o entrypoint Unicode.

Não se ocultou esse fato na auditoria. Os call sites mostram que esses arquivos são escritos apenas por `CheckPinyonNativePublicSources`, em uma pasta de prova. `PinyonPreflight`, que chega a essa função, só é chamado pelo teste `R18PinyonIntegration` no snapshot auditado. O caminho `CompletePinyonPreparation` não chama a prova: compila os módulos gerados e copia as DLLs do diretório de build correspondente. **Não foi encontrado uso dessas DLLs sintéticas na publicação do jogo.**

O marcador `PINYON_NATIVE_ENTRY_FACADES_PATH_PASS` demonstra somente o contrato de carregamento testado. Não é prova de execução das verdadeiras fachadas comerciais. Da mesma forma, os 78 objetos públicos de Pinyon, os sete módulos SSX compilados em duas variantes e os 128 objetos públicos FH1 são evidências limitadas a host/build; não comprovam primeiro boot.

Fontes: [prova Pinyon](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationPinyonNativeProof.cs), [preparação de produção](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Services/GameInstallationPinyonBuild.cs), [teste que chama o preflight](https://github.com/brad38/Allfix/blob/921295de12349e726f7ca21a5edd8a8ecee123d8/Tests/AddonInfrastructure/R18PinyonIntegration.cs).

## REX-05 — Patches oficiais não devem ser atribuídos ao AllFix

O replay comprova que as alterações SDL/FFmpeg dos dois patches FH1 e os grandes patches de GPU, shaders, codegen, memória e title update do SSX já constam dos arquivos originais fixados. Em SSX, por exemplo, os arquivos alterados de `src/graphics`, `src/codegen/builders/vector.cpp`, `src/core/memory_posix.cpp`, `src/core/threading_posix.cpp` e `src/system/user_module.cpp` resultam exatamente da sequência oficial, sem delta próprio adicional nesses arquivos após normalizar as quebras de linha.

Seria incorreto usá-los como prova de que AllFix implementou o que faltava no jogo. A conclusão correta separa esses 32 textos dos ajustes e componentes próprios, sem esconder as duas desativações funcionais encontradas.

## Limites e encaminhamento

Esta fatia da auditoria cobre integralmente os mecanismos de alteração identificados nos três perfis e seus pacotes fixados. Não é uma revisão de todas as funções dos três projetos upstream nem um teste comercial com mídia original. As pontes binárias não foram reconstruídas durante a auditoria; foram verificados hashes, fontes, proveniência preservada e uso no código de produção.

Os três fluxos devem ser tratados como **builds personalizados experimentais**, com alterações de runtime declaradas. Recomenda-se retirar qualquer promessa de equivalência integral ao launcher oficial; revisar FSR/FidelityFX em Pinyon e ReGPU em FH1; e manter as provas de host, ABI e imagem sintética separadas de comprovação de boot/jogabilidade. Nenhuma dessas correções foi aplicada durante a auditoria.
