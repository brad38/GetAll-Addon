# All-Fix + GetAll — Revisão integral do catálogo e correção do escopo de instalação

## Contexto

Durante o desenvolvimento do GetAll, foram identificadas implementações que ultrapassaram a responsabilidade de um instalador, incluindo modificações em código-fonte de terceiros, runtimes, renderizadores, compiladores de shaders e desativação de funcionalidades para viabilizar determinados projetos.

Essa abordagem está incorreta.

**O All-Fix deve disponibilizar ports e recompilações funcionais. O GetAll deve automatizar suas instalações, e não assumir o desenvolvimento dos próprios jogos.**

A meta anterior de cobrir os 148 projetos não deve ser mantida artificialmente.

## 1. Ambiente de trabalho

Workspace:

`C:\Users\bradg\Downloads\GetAll-R18`

Repositórios:

- Desktop: https://github.com/brad38/Allfix
- GetAll: https://github.com/brad38/GetAll-Addon
- Catálogo: https://github.com/brad38/AllFix-Repo

Utilize o arquivo `Auditoria-AllFix-GetAll-20261127.zip` como referência inicial.

Leia também os checkpoints, a matriz funcional, os relatórios de validação e as pendências existentes.

Verifique os commits, branches, worktrees e alterações locais antes de modificar qualquer arquivo. Não descarte trabalho ainda não versionado.

Caso não tenha acesso aos repositórios ou ao computador Bradsson, solicite o acesso necessário.

## 2. Critérios definitivos de inclusão no catálogo

O All-Fix é uma loja de projetos funcionais, não um catálogo de projetos promissores.

Um projeto pode ser incluído quando:

- Possui implementação funcional e evidências verificáveis de execução do jogo.
- Possui distribuição oficial ou procedimento reproduzível de compilação.
- Pode ser instalado utilizando os componentes oficiais e a mídia original necessária.
- Ainda apresenta bugs ou limitações, mas já permite jogar efetivamente.

Um projeto não deve permanecer no catálogo ativo quando:

- É apenas uma base de decompilação sem port funcional independente.
- Ainda não possui implementação jogável.
- Possui somente demonstrações técnicas, telas iniciais ou testes de renderização.
- Depende da implementação de funcionalidades ausentes no código upstream.
- Precisa que o All-Fix modifique o motor do jogo para torná-lo funcional.
- Não possui distribuição legítima ou fonte verificável suficiente para sua utilização.

A ausência de um executável pronto para download não é motivo suficiente para excluir um projeto. Se a compilação oficial produzir um jogo funcional, ele pode permanecer.

Da mesma forma, a ausência de homologação pelo GetAll não significa que o projeto upstream não seja funcional.

Não utilize somente o README, o percentual de decompilação, a existência de releases ou o sucesso de uma compilação como prova de jogabilidade.

## 3. Revisão completa do catálogo existente

Audite todos os jogos e projetos atualmente catalogados.

Consulte as fontes oficiais, releases, documentação, demonstrações e evidências de funcionamento de cada projeto.

Classifique cada projeto como:

- Funcional e elegível.
- Funcional com limitações documentadas.
- Funcional, mas temporariamente sem instalação automatizada.
- Funcionalidade não comprovada.
- Não funcional ou inelegível.

Remova do catálogo ativo os projetos inelegíveis ou cuja funcionalidade não possa ser comprovada após investigação adequada.

Quando um jogo possuir múltiplos projetos, remova somente aqueles que não atendem aos critérios. Remova o jogo inteiro apenas quando não restar nenhum projeto elegível.

Preserve os IDs, datas de inclusão, datas de lançamento e demais informações dos projetos mantidos.

Crie um registro separado dos projetos removidos, contendo:

- Nome e ID.
- Repositório oficial.
- Motivo da exclusão.
- Evidências utilizadas.
- Data da última verificação.
- Condições necessárias para sua futura reinclusão.

Esse registro deve permitir que a rotina de descoberta reavalie esses projetos futuramente, sem exibi-los na loja enquanto não forem funcionais.

## 4. Responsabilidade exclusiva do GetAll

O GetAll deve transformar os procedimentos oficiais de instalação em uma experiência automatizada.

### Projetos com launcher ou instalador oficial

Utilize o launcher ou instalador oficial, automatizando suas operações quando possível.

É permitido dispensar o launcher quando suas operações puderem ser reproduzidas fielmente pelo GetAll, incluindo:

- Solicitação da ROM, ISO ou demais arquivos originais.
- Verificação de integridade e compatibilidade.
- Extração de recursos.
- Aplicação de patches oficiais.
- Preparação de configurações.
- Instalação de dependências.
- Registro do executável e integração com o botão Jogar.

Não é necessário obrigar o usuário a utilizar um launcher intermediário quando o GetAll puder executar corretamente as mesmas operações.

### Projetos sem launcher ou instalador oficial

Automatize o procedimento oficial documentado pelo desenvolvedor.

O fluxo deve solicitar a mídia original necessária, preparar os recursos, provisionar dependências, executar os geradores oficiais e compilar o projeto quando necessário.

A compilação deve utilizar uma versão ou commit verificável do código upstream, respeitando suas instruções e requisitos.

O resultado deve ser equivalente ao que o usuário obteria seguindo manualmente o procedimento oficial.

## 5. Modificações proibidas

O GetAll não deve:

- Implementar funcionalidades ausentes nos jogos.
- Corrigir mecânicas, missões, fases ou comportamento do gameplay.
- Implementar operações ausentes em compiladores de shaders.
- Desenvolver ou substituir componentes gráficos do jogo.
- Modificar o runtime para contornar limitações funcionais do port.
- Desativar funcionalidades existentes apenas para conseguir compilar.
- Criar versões próprias dos jogos para torná-los jogáveis.
- Aplicar patches não oficiais ao código-fonte de terceiros.
- Alterar verificações de integridade ou identidade da mídia para forçar a instalação.
- Apresentar um projeto como funcional somente porque foi possível gerar um executável.

Se o projeto oficial não funciona, o GetAll não deve tentar fazê-lo funcionar.

Se o projeto oficial funciona, mas seu procedimento não pode ser automatizado sem alterações indevidas, mantenha a instalação automatizada indisponível até que exista uma solução legítima.

## 6. Implementações permitidas

São permitidos:

- Importadores e extratores próprios destinados exclusivamente à instalação.
- Adaptadores de formatos de mídia.
- Verificadores de hashes e integridade.
- Provisionamento de toolchains e dependências.
- Automação dos sistemas oficiais de compilação.
- Configurações documentadas e argumentos oficiais de execução.
- Patches publicados oficialmente pelo projeto upstream.
- Reprodução fiel das operações realizadas pelo launcher oficial.
- Gerenciamento de staging, cache, cancelamento, recuperação e rollback.
- Registro dos jogos e integração com o botão Jogar.

A criação de uma ferramenta auxiliar não deve modificar o comportamento funcional do jogo instalado.

Quando uma alteração no código-fonte upstream parecer indispensável, documente o problema e não aplique a alteração sem autorização específica.

## 7. Revisão das implementações existentes

Audite integralmente o Desktop e o GetAll, utilizando o histórico Git, os arquivos modificados, as ferramentas incorporadas, os patches, os overlays e os procedimentos de compilação.

Não limite a revisão aos projetos mencionados no relatório de auditoria.

Identifique todas as intervenções em código de terceiros e classifique-as conforme sua finalidade.

Para cada intervenção, determine:

- Qual arquivo ou componente foi modificado.
- Qual problema a modificação pretendia resolver.
- Se o projeto oficial já era funcional antes dela.
- Se a modificação é necessária exclusivamente à instalação.
- Se altera o funcionamento ou as funcionalidades do jogo.
- Se existe uma alternativa oficial.
- Se deve ser preservada, substituída ou removida.

Remova dos fluxos ativos as alterações indevidas.

Restaure os procedimentos oficiais e as funcionalidades que tenham sido omitidas ou desativadas.

Preserve todas as automações legítimas já implementadas. Não reverta indiscriminadamente o desenvolvimento do GetAll.

Mantenha o histórico Git das implementações anteriores para auditoria e recuperação, mas não distribua nem execute código que tenha sido considerado inadequado.

## 8. Arquitetura e tamanho do complemento

O GetAll deve continuar sendo um complemento leve e declarativo.

Seu pacote deve conter apenas os manifestos, configurações e informações necessárias para acessar as receitas remotas.

Os jogos, toolchains, dependências e componentes específicos devem ser obtidos sob demanda, quando o usuário selecionar a instalação correspondente.

Não incorpore ao complemento:

- Jogos completos.
- ROMs, ISOs ou recursos proprietários.
- Toolchains completas.
- Ambientes de compilação.
- Artefatos de testes.
- Caches de desenvolvimento.

Audite também o crescimento do executável AllFix.exe e os recursos incorporados ao SDK.

Sempre que tecnicamente adequado, substitua componentes específicos de determinados jogos por ferramentas verificadas, obtidas sob demanda.

Preserve no motor do All-Fix somente as capacidades compartilhadas e os componentes cuja incorporação seja tecnicamente justificada.

## 9. Gerenciamento contínuo do armazenamento

Durante todo o desenvolvimento, mantenha o workspace organizado.

Após validar uma implementação:

- Preserve o código, as receitas, os scripts de reprodução, os manifestos, os hashes e os logs relevantes.
- Faça commit das alterações necessárias.
- Exclua compilações intermediárias e artefatos comprovadamente descartáveis.
- Remova mídias sintéticas e extrações temporárias que não serão reutilizadas.
- Reutilize caches e toolchains compartilhadas.
- Evite acumular múltiplas publicações antigas do Desktop.

Não mantenha gigabytes de evidências binárias quando relatórios, hashes e scripts de reprodução forem suficientes.

Audite a pasta `evidence-r18` e elimine redundâncias comprovadas sem perder informações necessárias à reprodução dos testes.

Não exclua mídias originais, código não versionado necessário, dependências ativas ou dados pessoais.

Essa limpeza deve acontecer continuamente, sem interromper o desenvolvimento.

## 10. Atualização da rotina de descoberta

Atualize as instruções, a documentação e os validadores da rotina responsável por procurar novos projetos para o catálogo.

A partir de agora, a rotina deverá:

- Pesquisar novos ports, decompilações e recompilações.
- Verificar se existe implementação efetivamente funcional.
- Confirmar a procedência do código e dos componentes distribuídos.
- Investigar o procedimento oficial de instalação.
- Adicionar somente projetos elegíveis.
- Registrar as datas de lançamento e inclusão corretamente.
- Preservar as datas existentes durante atualizações.
- Reavaliar periodicamente os projetos anteriormente excluídos.
- Nunca incluir projetos somente porque parecem promissores.

Não confunda a data de lançamento do jogo com a data de criação ou lançamento do projeto de recompilação.

Preserve a integração com o carrossel Adicionados recentemente e as opções de ordenação da loja.

## 11. Nova matriz de cobertura

Recalcule a cobertura funcional do GetAll com base no catálogo revisado.

Diferencie claramente:

- Projeto upstream funcional.
- Instalação automatizada implementada.
- Instalação automatizada validada com dados sintéticos.
- Instalação validada com mídia original.
- Primeiro boot comprovado.
- Jogabilidade comprovada.

Não utilize testes sintéticos, compilação bem-sucedida ou preparação de componentes como comprovação de jogabilidade.

A quantidade final de projetos pode ser inferior aos 148 anteriores. Isso não representa uma regressão se os projetos removidos nunca deveriam ter sido incluídos.

**A nova meta é automatizar corretamente 100% dos projetos elegíveis, sem desenvolver os jogos em nome dos autores originais.**

## 12. Execução e entrega

Execute a revisão e todas as correções necessárias de forma contínua e autônoma.

Não encerre a tarefa após apresentar apenas uma auditoria, um planejamento ou a correção de alguns projetos.

Revise o conjunto completo, reutilize capacidades compartilhadas e paralelize investigações e testes independentes quando possível.

Atualize os três repositórios, os schemas, as receitas, os testes, a documentação, a matriz funcional e os checkpoints.

Execute os testes de regressão, valide as receitas e compile uma nova versão de teste do Desktop.

Faça os commits e pushes necessários nas branches apropriadas.

Ao finalizar, apresente:

- Quantidade de jogos e projetos antes e depois da revisão.
- Projetos removidos e respectivos motivos.
- Projetos que receberam modificações indevidas.
- Alterações indevidas removidas ou substituídas.
- Automações legítimas preservadas.
- Nova cobertura funcional do GetAll.
- Resultados dos testes e da compilação.
- Tamanho final do complemento e do Desktop.
- Espaço em disco recuperado.
- Commits, branches e resultados de CI.
- Caminho do executável e do complemento de teste.

Não faça merge na main, não publique releases, não altere o version.json público e não substitua a instalação atual sem autorização.

Não desenvolva o DownloadAll nesta tarefa.

**Priorize a fidelidade aos projetos oficiais, a funcionalidade real e a simplicidade da instalação. Não tente aumentar artificialmente a quantidade de jogos suportados.**