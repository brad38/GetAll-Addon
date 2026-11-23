# AllFix SDK 1.4.0 — contratos v6/v7 e suporte

Revisão local de desenvolvimento de 23/11/2026. Não é uma release. O aplicativo permanece 3.0.0 e o protocolo público permanece 1.0. Receitas v1–v5 e schemas anteriores não foram reescritos.

## Matriz técnica

| Etapa | Código implementado | Restrições |
|---|---|---|
| A | v6, portáteis PE, múltiplos assets, downloads oficiais GitHub, progresso global/individual, SHA-256, cancelamento, staging, recuperação de atualização falha, UI | GitLab multi-asset ainda não habilitado; sem execução de instaladores |
| B | v7 java_launcher, runtime Java 21+, validação de JAR, working_directory relativo, inicialização usando ArgumentList (exatamente -jar e caminho verificado) | Sem BAT/CMD/PowerShell, parâmetros livres ou elevação |
| C | .tar.gz com GZipStream + TarReader, máximo 100.000 entradas e 64 GiB expandidos, sem links, travessia ou duplicatas | Rejeita outros tipos TAR não regulares e dispositivos |
| D | v7 arcade_romset, CRC32+tamanho por membro, SHA-256 opcional, extensão numérica exclusivamente para romset | Ainda precisa das ROMs/dados originais e hashes oficiais |
| E | v7 .sfc/.smc/.gba, BIN/CUE multitrack, destinos de perfil multinível com autorização, validação de primeiro uso | Exige edição/dados originais corretos e homologação |
| F | Contratos installer_profile/build_profile reconhecidos e política de aprovação local estrita | Nenhum perfil aprovado nem isolamento de builds auditado: execução expressamente BLOQUEADA |

## Etapa A — receitas v6 e multi-asset

Campo assets (opcional, exclusivo de v6+): até 16 objetos {name,target,size,sha256,kind}, tamanho agregado até 64 GiB. kind pode ser portable_executable ou payload. Para executável portátil, target deve terminar em .exe, coincidir com launch_file e estar em required_files. O motor verifica tamanho, SHA-256 e cabeçalho PE Windows. Cabeçalho PE NÃO comprova confiança; executável só inicia por ação do usuário.

O recibo principal pode representar o próprio EXE portátil ou um ZIP/RAR/7z. Assets adicionais são resolvidos pela release oficial GitHub do mesmo repositório/tag, conferindo metadados e SHA-256 da receita. O payload é verificado novamente no staging. Links de script, comandos e caminhos externos não são aceitos como operações de instalação. A interface mostra progresso agregado, arquivo atual, cancelamento e erros. O estado da instalação anterior é preservado em registro separado até o commit final; uma falha ou cancelamento não apaga a instalação antiga.

VerifiedAssetBundle fornece arquivos temporários ao motor. Não aceita URLs diretas em JSON remoto. GitLab multi-asset requer implementação de origem equivalente.

## Etapa B — exemplo sintético de launcher Java v7

~~~json
{
  "schema_version": 7,
  "project_id": "synthetic-jar-test",
  "tag": "v1",
  "source_url": "https://github.com/example/demo",
  "operations": [],
  "required_files": ["launcher.jar"],
  "inputs": [],
  "prerequisites": ["java-21"],
  "java_launcher": {"jar": "launcher.jar", "runtime": "java-21"}
}
~~~

java_launcher admite working_directory opcional, relativo à pasta do jogo. Não declare launch_file simultaneamente. O host verifica ZIP/JAR, META-INF/MANIFEST.MF e Main-Class, compara integridade com o manifesto de instalação, valida JAVA_HOME e release Java 21+ e monta ProcessStartInfo sem shell. Argumentos remotos adicionais são rejeitados. O código não executa o jogo durante os testes sintéticos.

## Etapa C — TAR/GZIP

Pacotes .tar.gz são extraídos para staging com limites de quantidade e tamanho expandido, validação por segmento, rejeição de symlink/hardlink/dispositivo, detecção de caminhos duplicados e rollback. O download oficial reconhece .tar.gz e a biblioteca local também pode identificar esse formato. Não alterar catálogo para Project Picori sem autorização.

## Etapa D — romset arcade

Input kind arcade_romset é um diretório selecionado pelo usuário. Cada arquivo deve ter path e size e ser identificado por CRC32 de 8 dígitos, SHA-256, SHA-1 ou outro critério seguro compatível. Nomes com extensões numéricas de 1 a 3 dígitos são aceitos somente nessa modalidade. Use import_input_set com scope installation. Exemplo puramente sintético:

~~~json
{
  "id": "synthetic-romset",
  "name": "Dados originais",
  "kind": "arcade_romset",
  "files": [{"path": "epr-example.133", "size": 9, "crc32": "CBF43926"}]
}
~~~

O conteúdo desse exemplo é a sequência ASCII 123456789, não uma ROM de OutRun. Para Cannonball, fornecer os arquivos e CRC32/tamanhos reais publicados pela fonte oficial.

## Etapa E — mídia, CUE e perfis

V7 aceita .sfc, .smc e .gba em operações e conjuntos de mídia declarados. Entradas directory com validate_cue_references=true verificam linhas FILE dos CUE contra a relação exata de BINs informados, sem permitir caminhos externos ou faixas não declaradas. Profile_folders/profile_folder permitem até quatro segmentos relativos, sempre com validação por segmento; destinos LocalAppData/RoamingAppData exigem confirmação do usuário e rejeitam sobrescrever conteúdos distintos. Verificação first_run_files é passiva: o usuário prepara e solicita verificação.

## Etapa F — instaladores e builds

installer_profile e build_profile são identificadores de contratos locais, não comandos, argumentos, scripts nem URLs. ApprovedExecutionProfiles contém uma lista de aprovação vazia e rejeita esses campos por padrão. Não há sandbox confiável nem perfis auditados prontos; não implementamos um executor que poderia iniciar processos arbitrários. Para liberar um perfil no futuro é obrigatório auditar origem, hashes de ferramentas, consentimento, isolamento, limites de tempo/recursos, saídas verificáveis e rollback. Não considerar source-only desbloqueado.

## Compatibilidade e integração

- Protocol.Version permanece 1.0; Protocol.SdkVersion é 1.4.0.
- AllFix.Addons.Sdk.csproj é 1.4.0; AllFix.Desktop.csproj permanece 3.0.0.
- Receitas v3/v5/v6 e estados instalados anteriormente continuam aceitos. V7 acrescenta campos opcionais versionados.
- RemoteRecipeCatalog agora reconhece v6/v7 somente para entradas validated; experimental não é promovida automaticamente.
- A UI WPF existente integra downloads multi-asset, seleção de arquivos originais, progresso, cancelamento, mensagens e abertura EXE/Java sem redesign.
- Durante atualizações, registros de trabalho ficam separados dos registros instalados. Na falha, a instalação anterior permanece acessível.

## Instruções para o agente GetAll

1. Portáteis: confirmar release/tag/asset oficiais, formato executável realmente portátil, SHA-256 e tamanho de cada membro; escrever receita v6.
2. Severed Chains: verificar origem de JAR executável, Java 21+, diretório de trabalho, edição e dados necessários; adaptar para v7.
3. Project Picori: confirmar origem e versão Windows oficial tar.gz antes de propor nova receita.
4. Cannonball: obter lista exata do romset OutRun rev. B, tamanhos/CRC32 oficiais e destinos; nunca usar os dados sintéticos deste documento.
5. BIN/CUE: enumerar todas as faixas e suas relações, critérios de integridade e edição suportada, habilitar validação de referências.
6. Projetos source-only: preferir binários oficiais; onde não houver isolamento aprovado, manter status bloqueado e não inserir comandos em JSON remoto.

Esta rodada NÃO publicou receitas no GetAll nem homologou projetos reais. Testes sintéticos não equivalem à execução e verificação de jogos ou mídias comerciais.

## Testes e distribuição

Os testes locais cobrem regressões antigas, SHA-256, CRC32, CUE, JAR, TAR/GZIP, rejeição de links/travessia, arquivos duplicados, perfil sem consentimento, rollback e atualização com falha. São necessários testes de interface em Windows com arquivos oficiais e jogos reais para homologação.

Não mover as DLLs compiladas de validação para a instalação em produção, publicar releases ou fazer merge sem autorização.
