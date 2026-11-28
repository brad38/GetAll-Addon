# Restauração dos procedimentos oficiais — 28/11/2026

## Resultado e critério

A revisão preserva **108 jogos e 137 projetos elegíveis**. O índice contém
**146 receitas: 133 experimentais, uma validated histórica e 12 desativadas**.
Há **134 projetos com contrato ativo**. Os três restantes continuam no catálogo
com o procedimento oficial e o impedimento concreto da integração registrados:
StrikersRecomp, VandalHearts-PcPort e REDRIVER2.

A classificação de implementação depende do código de instalação, dos contratos
fechados e das operações oficiais revisadas. Ela não transforma um teste de
pacote, uma compilação sem ROM ou uma fixture em instalação completa com mídia
original. Nesta retomada houve **zero instalação completa, zero primeiro boot
e zero sessão de gameplay com mídia original**.

Esta é a continuação da auditoria de 27/11. As suspensões dos contratos antigos
continuam válidas. Uma rota legítima pode voltar mediante um **novo perfil e
hash exato**, sem reabilitar o perfil alterado, o estado anterior ou seu cache.
Os bytes substituídos estão em [retired-recipes](retired-recipes/). A política
registra identidade, receita nova, hash novo, perfil, commit upstream e hash da
receita anterior. Uma atualização automática não cria essa exceção.

## Contratos restaurados ou completados

| Projeto / versão preservada | Caminho oficial incorporado | Verificação obtida e limite |
|---|---|---|
| SSX v2.0.1 | Launcher oficial e preparação headless; mídia EA-2413; opções e defaults do autor preservados. | Kit oficial e recusa de mídia inválida/ausência de aceite. Sem compilação completa com disco. A antiga v2.0.0 continua desativada. |
| FH1 ReImagined v0.3.9 | CLI oficial para importar e compilar; GUI oficial para jogar e configurar. | Manifesto integral do kit e CLI. Diretório de dados isolado sem antecipar o JSON que suprimiria os defaults de GPU do primeiro uso. |
| GOW PC Port launcher-v0.4.0 | install.ps1 intacto, registro de instalação/otimização e launcher oficial --play. | Contrato, pacote e layouts revisados. Compilador, fontes e otimização oficiais preservados; sem build completo com ISO/CHD original. |
| Pinyon Shift v0.9.5 | setup-preview.ps1 e launch-preview.ps1 oficiais; fonte embutida na release. | Manifesto e descoberta da raiz revisados. Nenhuma flag própria desativa shaders, atualização de cache ou recursos. Sem build completo com mídia. |
| Ship of Harkinian 9.3.1 | Torch standalone oficial, compilado intacto, com a CLI e os assets da release. | Fontes e probes do extrator verificadas; sucesso exige saída e metadados, não apenas exit 0. Sem ROM/boot. |
| SM64Plus LauncherMirror | build.sh oficial, clone fixado, MSYS2 privado e launcher oficial. | Kit real, ferramentas nativas e recusas de ROM ausente/incorreta. CUSTOM_TEXTURES=1 mantido. Fonte e HEAD conferidos após o script. |
| sm64ex build-d7ca2c0 | Makefile intacto em MSYS2 MINGW64, EXTERNAL_DATA=1. | Ferramentas oficiais compiladas e kit/negativos verificados. Não houve link do jogo com ROM. |
| Render96ex build-48da5c4 | Makefile intacto, EXTERNAL_DATA=1; modelpack e texturas opcionais oficiais preservados. | Ferramentas oficiais compiladas e kit/negativos verificados. Sem habilitar renderer alternativo por imposição do AllFix. |
| SM64RT build-20e618b | Makefile intacto, EXTERNAL_DATA=1 e RENDER_API=RT64, conforme documentação. | Ferramentas e dependências verificadas; RT64 não foi desativado. Sem jogo recompilado ou teste de ray tracing. |
| SM build-578f90b | Solução Visual Studio oficial, MSVC v143 e restore oficial. | sm.exe e SDL2.dll compilados; 124 fontes originais sem mudanças. Sem ROM ou execução. |
| SM Rewrite build-5237873 | Preset Windows CMake e vcpkg oficiais, com baseline upstream fixado. | sm.exe e SDL2.dll compilados; 193 fontes sem mudanças. Baseline 7f9f0e44db287e8e67c0e888141bfa200ab45121; SDL2 2.30.0. Sem ROM. |
| GT5 build-64ca169 | Instalador e launcher oficiais; jogo e firmware próprios; DirectX 12, Vulkan e complementos preservados. | Kit real e recusa de mídia inválida antes das ferramentas. Sem firmware/jogo comercial, link completo ou boot. |
| GOW KIexster build-d1d11ec | Scripts oficiais de extração, compilação e execução com MSVC. | Kit real, extrator intacto sobre ISO criada para teste e rejeição de entrada inválida. Sem instalação comercial. |
| Mario Kart Double Dash build-bd36eb9 | build.ps1 oficial com LLVM/ABI MSVC e gcn-recomp b2193d7c7ce65c40959cf81859beaacafeebfd99. | runtime_check compilou 42 objetos, 165 fontes intactas; GCN_OPENXR=ON e GCN_BENCH_ONLY=OFF. Sem link final do jogo, build do runtime OpenXR ou boot. |

As receitas de preparação usam schema 9 com operações e inputs genéricos vazios,
mídia declarada e perfil fechado no SDK 1.5.70. O perfil identifica uma operação
implementada no Desktop; não é uma autorização para executar um script
arbitrário vindo do JSON. A origem, o tamanho e o hash de cada pacote continuam
fixados. O campo legado preparation_only da matriz é apenas um alias
descontinuado de uses_closed_preparation_profiles: **schema 9 não significa
instalação somente manual nem fluxo parcial**.

O CTR Turbocharged ci-07d0c49 conserva schema 5 e ganhou import_input nativo para
a imagem NTSC-U original no destino oficial assets/ctr-u.bin. Tamanho e SHA-256
vêm dos metadados oficiais de disco. A capacidade genérica e o caminho foram
revisados; aceitação no parser não foi contada como teste sintético de importação.

Shadow of Rome v2.9.5 preserva a importação e as transformações de ELF oficiais.
Na primeira preparação, reproduz os **44 valores** de FirstStartIni e acrescenta
ISO/serial verificados. Um INI existente é preservado byte a byte. Sete verificações
cobrem paridade, PAL/NTSC e preservação das preferências. Jogar abre o launcher
intacto, sem flags próprias ou uma segunda escolha da mesma ISO. Isso elimina
a etapa parcial de seleção sem alterar os defaults do autor.

## Dependências e recursos oficiais

Ferramentas são obtidas sob demanda e não fazem parte do complemento declarativo.
Quando uma instalação exige novos componentes Microsoft, o Desktop apresenta
o termo indicado pelo procedimento e exige aceite explícito. Uma instalação
compatível já existente pode ser reutilizada sem novo download. Para FH1, o
link vem de pins.py do launcher 0.3.9:
https://go.microsoft.com/fwlink/?LinkId=2086102.

Os quatro fluxos Mario usam uma distribuição MSYS2 oficial privada, separada do
MSYS2 do usuário. O bootstrap fixa o instalador, inicializa as chaves oficiais,
atualiza pelos repositórios assinados e registra as revisões instaladas. Não
reduz a política de assinaturas. A coleção de DLLs segue os imports PE reais,
incluindo a dependência SDL3 de SDL2-compat atual, e mantém as licenças. O script
CRLF do Plus roda com a opção igncr do Bash; seus bytes não são reescritos.

As fontes são conferidas antes/depois das etapas que geram arquivos. Nenhum
patch de compilação, renderer, gameplay ou shader foi recolocado. RT64, OpenXR,
HD vídeo e outras opções não podem ser desligados para transformar um erro em
sucesso. O helper legado de SoH continua rejeitado: o substituto tem origem,
licença, comandos de compilação e hashes próprios auditáveis.

## Três impedimentos restantes

### StrikersRecomp

O commit revisado cd88f71f5a836c103484c038454b4143000d883c fixa GXRuntime v0.1.0
no bootstrap. Essa tag exporta alvos DolRuntime, enquanto o projeto espera
GXRuntime e o header gxruntime/gap_report.h. O caminho RecompCore oficial também
gera .so fora do macOS e usa a invocação Metal examinada; não foi demonstrado
um contrato Windows completo intacto nessa revisão. O antigo caminho do Desktop
trocava a dependência e aplicava adaptações próprias, portanto permanece vetado.

A reentrada exige uma revisão upstream compatível e um caminho Windows oficial
verificado, ou autorização específica para o trabalho upstream. Isso não é
uma afirmação de que o port não funciona em outras plataformas.

### VandalHearts-PcPort

O NOTICE oficial distingue código livre dos dados embutidos nas releases:
segmentos estáticos e textos do jogo, glifos derivados da BIOS e tabelas. A
receita binária anterior não os regenerava a partir da mídia do usuário. Não
foi declarada ilegalidade; foi identificada uma procedência insuficiente para
o caminho de redistribuição automatizado.

A fonte atual permite gerar dados do executável PSX e dos glifos da BIOS próprios.
Seu gerador tem fallback direto para o executável PSX: não se exige indevidamente
um ELF ou SDK PsyQ nesse caminho. A tentativa nativa Windows intacta falhou na
criação de links simbólicos exigidos pelo CMake, por falta da capacidade do
ambiente, e na dependência OpenAL. O empacotamento completo oficial documentado
usa cross-build Linux/macOS MinGW e preserva vídeo HD/WebP. Os 505 arquivos
originais examinados permaneceram iguais. Não se contornou o erro com patches,
desativação de recursos ou elevação de privilégios.

A reentrada depende de preparar e validar um desses ambientes oficiais, com
mídia e BIOS próprias. Não há inferência de boot ou de incompatibilidade universal.

### REDRIVER2

A tag 7.4-rc2 rastreia 76 arquivos em data/DRIVER2; o script oficial de pacote
copia esse conteúdo para a distribuição. Os conversores conv.bat/conv.sh
examinados extraem vídeo e áudio com jPSXdec; não demonstram como regenerar todos
os grupos LANG/GFX/GAL/REPLAYS e demais extras a partir dos dois CDs do usuário.
A issue oficial 234 registra a dúvida de procedência sem resposta no momento
inspecionado.

Compilar o executável da fonte não resolve sozinho essa lacuna dos dados
copiados. A reentrada exige uma origem/licença esclarecida ou extração oficial
reprodutível dos componentes necessários a partir da mídia própria. A
funcionalidade upstream e o registro manual do catálogo permanecem.

Os arquivos [remaining-official-blockers.json](validations/official-scope/remaining-official-blockers.json)
e seus recibos vinculados preservam URLs, commits, hashes, resultados e condições
de reavaliação. Não foram feitas novas tentativas de runtime após consolidar
esses impedimentos.

## Evidência, testes e entrega

A [matriz](INSTALLATION-COVERAGE.md) e o
[ledger](installation-evidence.json) separam seis dimensões. Os resultados atuais
de testes estão em [official-scope](validations/official-scope/README.md), com
logs pequenos e hashes das origens. Provas anteriores não foram promovidas a
atuais apenas porque uma receita foi reativada.

A única validated permanece SM64 Coop Deluxe v1.5.1, SHA-256
54fb8ac09863fc500b532244070e9cbe5bc4a81aaff66530b4e711b97fb2a2f3.
O relato histórico de importação/execução está na auditoria de 22/11; não há
uma nova reprodução nesta rodada nem sequência de gameplay atribuível.

A entrega usa uma branch de revisão, catálogo fixado e complemento de TESTE
com SDK mínimo 1.5.70. O ZIP contém somente addon.json e responses.json.
Commit local, geração do pacote, publicação das referências e CI hospedado
são fatos separados. O recibo do ZIP final declara exatamente quais deles
foram verificados. Nenhum merge em main, release pública, alteração de
version.json ou substituição da instalação corrente integra esta entrega.
