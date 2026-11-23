# AllFix SDK 1.4.1 — schema v8, Java 25 e classpath restrito

**Rodada 11A — 23/11/2026.** Código local em desenvolvimento, não é release pública.

## Compatibilidade

Protocol.Version permanece 1.0. Protocol.SdkVersion e a versão AllFix.Addons.Sdk.csproj passam a 1.4.1. O aplicativo principal continua versão 3.0.0. Receitas v1–v7 e seus schemas permanecem válidos; não há migração automática. Os campos novos ficam exclusivamente em installation-recipe-v8.schema.json.

## Inspeção do Severed Chains oficial

- Fonte: Legend-of-Dragoon-Modding/Severed-Chains, tag release-3.0.0.
- Windows ZIP oficial: Severed_Chains_Windows.zip, 131.446.655 bytes, SHA-256 164716cba1899cadf834506636de8da56721d695457c3b53c93c533999ef9bb4.
- 769 entradas. JAR principal lod-game-ab5dfe5ba6d4c07464a2f0e67985b9e77e2f7bdb.jar e 95 arquivos JAR adicionais em libs/; updater.jar não é a classe de entrada do jogo.
- Classe principal legend.game.MainWindows, bytecode major 69 (Java 25).
- O launch.bat usa jdk25/bin/java.exe, Amazon Corretto 25.0.0.36.2, na raiz do jogo, com seis opções de JVM, -cp JAR_principal;95_arquivos_libs, classe legend.game.MainWindows e os argumentos finais -Xmx2G -ea.
- Os jogos exigem mídias originais da edição norte-americana de Legend of Dragoon, fornecidas pelo próprio usuário e preparadas em isos/. Nenhuma mídia comercial foi incluída ou executada.
- O script oficial faz download do Java; o All-Fix NÃO reproduz isso. O usuário deve instalar Java 25+ e apontar JAVA_HOME manualmente.

O JAR pode conter Main-Class, mas a existência do manifesto não garante que o modo -jar carregue as 95 dependências. O modo classpath é diferente e não substitui o v7 automaticamente.

## Campos v8: java_launcher

| Campo | Contrato |
|---|---|
| jar | Caminho relativo do JAR contendo a classe principal, incluído em classpath e required_files |
| runtime | java-21 ou java-25, com item correspondente em prerequisites |
| main_class | Classe Java qualificada, ativando modo classpath |
| classpath | Array explícito de 1 a 128 arquivos JAR locais e únicos; todos em required_files |
| jvm_options | Lista sem duplicações de identificadores da whitelist abaixo; não aceita texto arbitrário |
| program_arguments_profile | Exclusivamente severed-chains-3 (opcional), vinculado a identidade de projeto, fonte oficial e Java25 |
| working_directory | Caminho relativo confinado à instalação |

Whitelist de jvm_options:

| Nome no contrato | Opção aplicada |
|---|---|
| joml-fastmath | -Djoml.fastmath |
| joml-sin-lookup | -Djoml.sinLookup |
| joml-fma | -Djoml.useMathFma |
| open-java-util | --add-opens=java.base/java.util=ALL-UNNAMED |
| export-jdk-internal-misc | --add-exports=java.base/jdk.internal.misc=ALL-UNNAMED |
| enable-native-access | --enable-native-access=ALL-UNNAMED |

O perfil local severed-chains-3 adiciona exclusivamente os dois argumentos literais -Xmx2G e -ea APÓS a classe principal, como o launcher oficial. Ele só pode ser solicitado por project_id severed-chains, source_url HTTPS exata do repositório original, runtime java-25, main_class legend.game.MainWindows e conjunto ordenado de seis opções. Nenhuma receita remota fornece parâmetros arbitrários.

## Segurança e instalação

1. O parser valida paths relativos, extensões JAR, ausência de duplicatas, limite de 128 JARs, correspondência com required_files e classe principal válida.
2. Staging, limites de expansão, SHA-256, manifestos e rollback existentes são reutilizados.
3. Antes da publicação, o motor confirma ZIP/JAR válido de cada entrada e a presença da classe principal no JAR declarado, com magic CAFEBABE e versão de bytecode compatível.
4. Ao iniciar, todos os JARs são verificados contra o manifesto persistido de tamanho e SHA-256, inclusive após reinício do aplicativo. A falta de biblioteca ou alteração bloqueia lançamento.
5. O runtime vem de JAVA_HOME, validado pelo arquivo release e bin/java.exe. Java21 continua funcionando em v7; Java25 ou superior é obrigatório quando a receita declara java-25. Não há download automático.
6. O processo é iniciado com UseShellExecute=false e ArgumentList. Não usa cmd.exe, PowerShell, scripts BAT, wildcard de classpath, URLs de JAR ou argumentos de shell.
7. JDK_JAVA_OPTIONS, JAVA_TOOL_OPTIONS, _JAVA_OPTIONS e CLASSPATH são zeradas SOMENTE no processo-filho, sem alterar o sistema do usuário.

## Exemplo e capacidade pendente

installation-recipe-v8.example.json é uma receita sintética com três JARs e classe explicitamente declarada.

O pacote de integração inclui severed-chains-v8.candidate.json, candidato técnico com a lista de 96 JARs comprovada pelo ZIP oficial. Não está integrado nem validado no GetAll. A candidata usa manual_steps para destacar a mídia legítima; a instalação do host permanece PartiallyCompleted. Antes de virar receita funcional, o agente GetAll precisa solucionar o fluxo de comprovação da mídia e registrar um boot real. Não basta preparar o classpath.

O projeto GetAll usa ainda 91 receitas/119 projetos na main após Rodada 10. Não modificar schema v7, nem instalar/promover receitas v8 sem autorização e evidência.

## Testes

Os testes cobrem Java 21/25/26 simulado, JAR sem Main-Class com classe real, múltiplos JARs, hashes, campos remotos indevidos, caminhos maliciosos, dependências faltantes, classes incompatíveis, cancelamento, regressão v3/v5/v6/v7, staging de release oficial e interface WPF/WebView2 sintética isolada.

Limitações: não foi executado jogo comercial; nenhuma DLL instalada, release ou merge foi alterado. Confira o relatório técnico da Rodada 11A e as evidências de validação.
