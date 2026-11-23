# Severed Chains release-3.0.0 — validação experimental v8 (Rodada 11B)

**Projeto:** Legend-of-Dragoon-Modding/Severed-Chains.
**Jogo:** the-legend-of-dragoon.
**Tag:** release-3.0.0.
**Status index:** experimental. **Nenhum boot com mídia comercial foi realizado.**

## Evidência oficial da distribuição

- Origem HTTPS: https://github.com/Legend-of-Dragoon-Modding/Severed-Chains/releases/tag/release-3.0.0
- ZIP Severed_Chains_Windows.zip, 131446655 bytes e SHA-256 164716cba1899cadf834506636de8da56721d695457c3b53c93c533999ef9bb4, conferidos diretamente nos bytes oficiais.
- 769 itens no ZIP; todos os **96 JARs** declarados constam no ZIP e possuem estrutura JAR válida. Ordem de classpath confrontada com launch.bat oficial: correspondência 96/96, incluindo 95 libs externas.
- JAR principal lod-game-ab5dfe5ba6d4c07464a2f0e67985b9e77e2f7bdb.jar. Classe real legend/game/MainWindows.class encontrada, prefixo CAFEBABE, bytecode 69 (Java25).
- Opts oficiais: joml-fastmath, joml-sin-lookup, joml-fma, open-java-util, export-jdk-internal-misc, enable-native-access (lista restrita e ordenada). Perfil fechado severed-chains-3.

## Validação nativa

- AllFix.dll 1.4.1 em desktop-release foi apenas lida por harness .NET em diretório temporário dedicado; SDK instalado não foi modificado.
- ParseIndex (92 entradas) e ParseRecipe de todas as 92 receitas: PASS; a v8 continha 96 libs, Java25, profile e manual_steps.
- JavaJarLauncher.ValidateClasspath aplicado aos 96 JARs **oficiais extraídos isoladamente**, sem executar jogo: PASS.
- Negativos nativos: classe inexistente, bytecode 69 com runtime Java21 e JAR ausente rejeitados. Mutacoes de origem, classe, runtime, traversal, opção arbitrária e downgrade a v7 rejeitadas.
- Resultado global do harness: 92 asserts aprovados. Testes Python 34/34.
- Evidência SDK 11A anterior: GameInstallationService.Run com a candidata técnica sobre ZIP oficial retornou **PartiallyCompleted** (preparo Java, mas sem mídias originais). Esta Rodada 11B não reivindica nova execução de ponta a ponta do motor.
- Nenhuma mídia comercial incluída. Imagens de discos NTSC-U de The Legend of Dragoon e preparo em isos/ seguem **manuais e não verificados**. O primeiro boot permanece pendente.

## Critérios para promoção a validated

Somente após ambiente Java25+ legítimo, seleção dos discos originais do usuário, preparo das imagens e verificação da saída gerada, execução com primeiro boot real bem-sucedido, registro de data/hashes/versões e ausência de execução de scripts inseguros. Sem isso, manter experimental.

**Limitação:** suporte ao classpath 96/96 comprova estrutura do aplicativo, não disponibilidade de dados de jogo nem jogabilidade.
