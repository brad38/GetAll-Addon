"""Refresh current summary documents from the verified coverage and test receipts."""
from pathlib import Path
import collections, hashlib, json
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/"docs/validations/official-scope"
def load(p):return json.loads(p.read_text(encoding="utf-8"))
def write(p,s):p.write_text(s,encoding="utf-8",newline="\n")
index=load(ROOT/"index.json")
coverage=load(OUT/"catalog-coverage.json")
tests=load(OUT/"final-validation-results.json")
assert len(tests["results"])==2 and all(r["exit_code"]==0 for r in tests["results"])
python_tests=tests["results"][0]["tests"]
desktop=load(OUT/"resumed-evidence/desktop/scope-desktop-final-validation-results.json")
assert all(r["exit"]==0 for r in desktop)
suite=next(r["passes"] for r in desktop if r["test"]=="suite")
counts=collections.Counter(e["status"] for e in index["recipes"])
dimensions=coverage["dimension_counts"]
synth=dimensions["synthetic_validation"]
catalog="e4fdde9d7c128f79eb19cf99ea07e2e9b628127a"
summary=dict(reviewed_at="2026-11-28",catalog_commit=catalog,index_sha256=hashlib.sha256((ROOT/"index.json").read_bytes()).hexdigest(),
    games=coverage["games"],eligible_projects=coverage["projects"],archived_catalog_projects=11,
    recipes=len(index["recipes"]),recipe_statuses=dict(counts),active_recipes=sum(counts.get(k,0) for k in ("experimental","validated")),
    projects_with_active_contract=coverage["development_covered"],manual_only_projects=coverage["missing"],
    dimensions=dimensions,new_original_media_installations=0,new_first_boots=0,new_gameplay_sessions=0,
    historical_validated=dict(project_id="sm64coopdx-super-mario-64-coop-deluxe",tag="v1.5.1",
        recipe_sha256="54fb8ac09863fc500b532244070e9cbe5bc4a81aaff66530b4e711b97fb2a2f3",
        evidence="docs/AUDITORIA-CATALOGO-2026-11-22.md",evidence_sha256="5a3747fbc2ba1f57d28ddb26851dfc93f71f3fa1d761ccc6e69f92d9e52cef78",
        limit="Prior user report of original-ROM import and launch; not reproduced in this resumed work; no specific gameplay sequence."),
    validation=dict(python_tests=python_tests,local_ci_exit=0,desktop_suite_passes=suite,desktop_parser_recipes=146),
    preview=dict(addon_version="1.5.76",min_sdk_version="1.5.70",getall_commit="Exact final local commit recorded with the subsequently generated ZIP."),
    publication=dict(catalog_public_documents_verified=True,getall_publication="Pending exact work-branch push by integration owner at the time of this local summary; no hosted GetAll CI inferred."))
write(OUT/"final-coverage-summary.json",json.dumps(summary,ensure_ascii=False,indent=2)+"\n")
write(ROOT/"docs/INSTALLATION-COVERAGE.md",f"""# Cobertura de instalação e elegibilidade — 28/11/2026

A revisão preserva **108 jogos e 137 projetos elegíveis**. Os **11 IDs arquivados**
ficam em AllFix-Repo/excluded-projects.json, com metadados, motivo e condição de
reavaliação. O catálogo, a elegibilidade e as exclusões usam o mesmo commit
**{catalog}**, confirmado remotamente pelos três documentos.

## Receitas e projetos

O índice contém **146 receitas: 133 experimental, uma validated histórica e
12 disabled**. Há **134 receitas ativas para 134 projetos**. Os outros
**três projetos elegíveis** permanecem disponíveis pelo procedimento oficial
registrado no catálogo, com automação suspensa por um impedimento concreto.

As 12 receitas desativadas se dividem em **cinco IDs arquivados** (GGA64,
Burnout 3, o agregado Sonic 1 Forever/Sonic 2 Absolute, Dr. Mario 64 base e
Metaforce), **quatro variantes antigas com outra receita ativa no mesmo projeto**
(SM64Plus, SSX, CTR e MKW) e **três projetos elegíveis bloqueados**
(StrikersRecomp, VandalHearts-PcPort e REDRIVER2). Dr. Mario 64 Plus é um projeto
distinto; sua presença não reativa o ID base. Burnout 3 e Metaforce não têm
uma rota ativa nem permanecem no catálogo atual.

A retomada restaurou treze projetos anteriormente suspensos por caminhos oficiais,
completou SM64Plus/CTR e eliminou a etapa manual restante de Shadow of Rome.
Novos perfis têm hashes exatos aprovados; os perfis antigos adulterados continuam
bloqueados. Os bytes anteriores permanecem em retired-recipes. Veja
[a revisão dos contratos](OFFICIAL-CONTRACT-RESTORATION-20261128.md).

## Seis dimensões independentes

| Dimensão | Resultado registrado | Alcance da evidência |
|---|---:|---|
| Upstream funcional | 137 com evidência específica | Evidência externa do catálogo, independente de testes locais GetAll. |
| Automação implementada | 134 implementadas; 0 parciais; 3 bloqueadas | Código, dispatch, perfil e operação oficial revisados; não é uma instalação comercial concluída. |
| Validação sintética | {synth.get("passed",0)} atuais passaram; {synth.get("historical",0)} históricos; {synth.get("failed",0)} falhou; {synth.get("unknown",0)} desconhecidos | Somente as operações descritas em cada recibo: pacotes, negativos, configuração, ferramentas ou builds sem mídia. |
| Instalação com mídia original | 1 relato histórico; 136 desconhecidas | SM64 Coop Deluxe v1.5.1, sem nova reprodução nesta rodada. |
| Primeiro boot pelo GetAll | 1 relato histórico; 136 desconhecidos | O mesmo relato anterior de importação e execução. |
| Gameplay pelo GetAll | 137 desconhecidos | Nenhuma sessão específica GetAll atribuível foi acrescentada. |

Nesta retomada houve **zero instalação completa com mídia original, zero
primeiro boot e zero sessão de gameplay com mídia original**. A única receita
validated continua SM64 Coop Deluxe v1.5.1, SHA-256
54fb8ac09863fc500b532244070e9cbe5bc4a81aaff66530b4e711b97fb2a2f3.
Sua evidência é o relato histórico na
[auditoria de 22/11](AUDITORIA-CATALOGO-2026-11-22.md), SHA-256
5a3747fbc2ba1f57d28ddb26851dfc93f71f3fa1d761ccc6e69f92d9e52cef78.
Não foi criada uma nova homologação.

Os 15 resultados atuais positivos correspondem a SSX, FH1, GOW Daniel, Pinyon,
SoH, SM64Plus, sm64ex, Render96ex, SM64RT, SM, SM Rewrite, GT5, GOW KIexster,
MKDD e Shadow of Rome. Seus escopos variam: FH1 prova integridade do kit;
SM/SM Rewrite também têm compilação nativa intacta sem ROM; MKDD prova
runtime_check sem link do jogo; Mario prova ferramentas e recusas de ROM;
SoR prova defaults, kit e plano de lançamento sintético. Uma aprovação não
substitui as demais dimensões.

A única falha sintética atual é a configuração CMake nativa intacta de
VandalHearts neste ambiente: links simbólicos obrigatórios e OpenAL impediram
a configuração. Esse resultado não é uma avaliação de gameplay nem uma
declaração de incompatibilidade universal. Os demais detalhes estão nos
[recibos dos bloqueios](validations/official-scope/remaining-official-blockers.json).

## Impedimentos concretos e reentrada

| Projeto | Impedimento da automação atual | Condição de reentrada |
|---|---|---|
| StrikersRecomp | GXRuntime v0.1.0 fixado pelo bootstrap exporta alvos diferentes dos exigidos; a rota RecompCore examinada não estabelece o contrato Windows completo. | Revisão upstream compatível ou ambiente oficialmente suportado, verificados sem patches próprios de runtime. |
| VandalHearts-PcPort | Binários incorporam dados declarados no NOTICE; a alternativa de fonte/mídia/BIOS próprios ainda carece de ambiente oficial integrado e validado. | Validar build oficial com os arquivos próprios e recursos preservados; não reutilizar a distribuição binária como substituto dessa geração. |
| REDRIVER2 | O pacote copia dados extras rastreados cuja procedência/extração integral não foi esclarecida; os conversores examinados cobrem áudio/vídeo. | Documentar origem/licença dos extras ou extração oficial reprodutível dos CDs próprios. |

Essas são suspensões da integração, não remoções da elegibilidade funcional.
A investigação e os commits exatos constam em
[OFFICIAL-CONTRACT-RESTORATION-20261128.md](OFFICIAL-CONTRACT-RESTORATION-20261128.md).

## Registros e semântica

O [ledger](installation-evidence.json) registra cada projeto e dimensão. Uma
alegação positiva exige tag e SHA-256 exatos da receita, fonte atribuível e
observação. Arquivos locais têm SHA-256 conferido. Se a receita mudar ou for
desativada, uma prova positiva deixa de contar como atual. Provas sintéticas
não são aceitas como mídia original, boot ou gameplay; evidência upstream
alimenta somente a primeira dimensão.

A [matriz JSON](validations/official-scope/catalog-coverage.json) é gerada sem
consultar ou mudar a instalação pública. Os campos legados main_covered e
development_covered contam contratos, não execução. preparation_only é um
alias descontinuado de uses_closed_preparation_profiles: schema 9 pode
implementar a preparação oficial completa no SDK e não significa somente
manual. Existem 31 projetos com esses perfis fechados. O estado de automação
vem da dimensão apropriada. main_comparison: not_requested indica ausência
de comparação com a branch pública.

unknown significa falta de prova atribuível; historical preserva prova anterior
sem reaprová-la; failed descreve a operação nomeada que falhou. Não se converte
uma fixture, tela inicial ou build em gameplay.

## Testes e reprodução

**{python_tests} testes Python passaram**. O ponto de entrada real do CI local
validou as **146 receitas** com LF estrito, JSON Schema, blobs Git e o catálogo
público fixado. A matriz verificou todas as referências locais de evidência.
Desktop registrou **{suite} verificações de regressão**, parser **146/146**,
builds sem avisos/erros e testes específicos dos kits oficiais. Os recibos
[de validação](validations/official-scope/README.md) delimitam cada resultado.

~~~sh
python scripts/validate_recipes.py --strict-lf --require-jsonschema --check-git-blobs --check-catalog ../catalog-scope-20261127/catalog.json
python scripts/catalog_coverage.py --catalog ../catalog-scope-20261127/catalog.json --output docs/validations/official-scope/catalog-coverage.json
python -m unittest discover -s tests -v
python scripts/validate_ci.py
~~~

CI e monitor da prévia fixam o catálogo em {catalog}.
O monitor consulta fontes oficiais, preserva datas e não reativa receita
desativada nem atribui validated automaticamente. Candidatos/excluídos geram
revisão, não instalação automática. A prévia não pode ter main como destino.

O pacote de TESTE é **1.5.76**, com SDK mínimo **1.5.70**. Seu recibo posterior
ao commit contém o SHA GetAll definitivo, o SHA do catálogo, o hash/tamanho
do ZIP e os dois membros JSON. Commit local, publicação e CI hospedado são
verificados separadamente; a geração do ZIP não presume acesso remoto.
""")
readme=ROOT/"README.md"
text=readme.read_text(encoding="utf-8")
begin=text.index("## Escopo revisado")
end=text.index("## GetAll-Addon v1.0.0",begin)
text=text[:begin]+"""## Escopo revisado em 28/11/2026

O GetAll automatiza **procedimentos oficiais** de projetos com gameplay
comprovado. O catálogo de revisão contém **137 projetos em 108 jogos**; 11 IDs
anteriores ficam em registro separado para reavaliação. O índice conserva
**146 receitas: 134 ativas e 12 desativadas**, com 134 projetos de automação
implementada e três impedimentos documentados.

A [cobertura em seis dimensões](docs/INSTALLATION-COVERAGE.md) separa upstream
funcional, implementação, testes sintéticos, instalação com mídia original,
primeiro boot e gameplay. Os [contratos oficiais restaurados](docs/OFFICIAL-CONTRACT-RESTORATION-20261128.md)
preservam as funções dos autores e mantêm os perfis antigos rejeitados.
A revisão não acrescenta homologação nem execução com mídia original.

As métricas de rodadas antigas abaixo são históricas. Não existe meta
obrigatória de manter 148 IDs.

"""+text[end:]
text=text.replace("separado **1.5.75**","separado **1.5.76**")
write(readme,text)
checkpoint=ROOT/"docs/CHECKPOINT.md"
text=checkpoint.read_text(encoding="utf-8")
old_marker="## Revisão de elegibilidade e fidelidade — 27/11/2026"
old=text[text.index(old_marker):]
write(checkpoint,f"""# Checkpoint do GetAll-Addon

## Retomada final dos contratos oficiais — 28/11/2026

Catálogo fixado e publicamente conferido: **{catalog}**,
108 jogos, 137 projetos ativos e 11 arquivados. Índice final SHA-256
**{summary["index_sha256"]}**: 146 receitas, 133 experimental,
uma validated histórica e 12 disabled; **134 contratos/projetos ativos**.

A matriz registra **134 implementadas, zero parciais e três bloqueadas**.
Sintéticos: **{synth.get("passed",0)} atuais positivos, {synth.get("historical",0)} históricos,
{synth.get("failed",0)} falha de configuração e {synth.get("unknown",0)} desconhecidos**.
Mídia e boot: um relato histórico cada; gameplay: 137 desconhecidos.
Nesta retomada, zero instalações completas, zero boots e zero sessões de
gameplay com mídia original. A única validated continua SM64 Coop Deluxe v1.5.1.

Foram restauradas as rotas oficiais de SSX, FH1, GOW Daniel, Pinyon, SoH,
sm64ex, Render96ex, SM64RT, SM, SM Rewrite, GT5, GOW KIexster e MKDD.
SM64Plus/CTR foram completados e Shadow of Rome preserva o preset oficial
integral da primeira inicialização. StrikersRecomp, VandalHearts e REDRIVER2
ficam suspensos pelos impedimentos concretos documentados, mantendo os
procedimentos oficiais e a elegibilidade upstream.

Validação final: **{python_tests} testes Python**, ponto de entrada CI local,
146 receitas e hashes/evidências; Desktop **{suite} checks**, parser **146/146**,
build e testes individuais de kits. Uma asserção antiga de CTR ainda esperava
a cópia manual; foi atualizada para conferir a importação verificada e o teste
completo passou. O log intermediário está preservado.

O complemento final é **TESTE 1.5.76 / SDK mínimo 1.5.70**, em ZIP com somente
addon.json e responses.json. O recibo gerado depois do commit fixa os dois SHAs.
O catálogo já foi confirmado remoto; o envio GetAll e seu CI hospedado são
responsabilidade da integração final, sem inferi-los do pacote local.

Registros: [matriz](INSTALLATION-COVERAGE.md),
[contratos e impedimentos](OFFICIAL-CONTRACT-RESTORATION-20261128.md),
[recibos e reprodução](validations/official-scope/README.md).
Sem merge main, release pública, mudança de version.json ou substituição
da instalação corrente.

As seções seguintes conservam o histórico e os números de cada etapa.

---

"""+old)
scope=ROOT/"docs/SCOPE-CORRECTION-CHECKPOINT.md"
text=scope.read_text(encoding="utf-8")
start=text.index("A pesquisa e os registros de catálogo") if "A pesquisa e os registros de catálogo" in text else text.index("A revisão final registra")
end=text.index("Plano da rodada",start)
text=text[:start]+f"""A revisão final registra 108 jogos, 137 projetos ativos e 11 arquivados.
Catálogo {catalog}, publicado e conferido nos três documentos.
GetAll: 146 receitas, 134 ativas e 12 desativadas; 134 implementações e três
impedimentos concretos, sem fluxos parciais. A matriz separa {synth.get("passed",0)} resultados
sintéticos atuais, {synth.get("historical",0)} históricos, uma falha limitada de configuração e
{synth.get("unknown",0)} desconhecidos. Não houve instalação/boot/gameplay com mídia original nesta retomada.

O complemento final de TESTE 1.5.76 requer SDK 1.5.70 e é gerado com os commits
definitivos, registrados no recibo externo ao commit para evitar referência
circular. O envio GetAll e o CI hospedado são etapas de integração separadas.
Ver [checkpoint](CHECKPOINT.md), [matriz](INSTALLATION-COVERAGE.md) e
[provas finais](validations/official-scope/README.md).

"""+text[end:]
write(scope,text)
preview=ROOT/"docs/PREVIEW-SDK170.md"
text=preview.read_text(encoding="utf-8").replace("O recibo preliminar da versão está em","O recibo preliminar da versão anterior 1.5.75 está em")
write(preview,text)
write(OUT/"README.md",f"""# Provas da revisão de instalações oficiais

## Resultado final local — 28/11/2026

- **146 receitas**, **134 ativas**, **12 desativadas**; 134 projetos com automação.
- **{python_tests} testes Python aprovados**, validador estrito e ponto de entrada CI local aprovado.
- Desktop: **{suite} verificações**, parser **146/146**, build WPF e harness sem avisos/erros.
- Catálogo fixado **{catalog}**, documentos remotos idênticos ao checkout.
- Nenhuma instalação completa, boot ou sessão de gameplay com mídia original nesta retomada.

[final-coverage-summary.json](final-coverage-summary.json) resume cada eixo;
[catalog-coverage.json](catalog-coverage.json) contém os 137 projetos.
O [ledger](../../installation-evidence.json) vincula cada alegação à receita
exata e à prova com hash.

## Índice das provas

| Arquivo / grupo | Conteúdo e limite |
|---|---|
| [final-validation-results.json](final-validation-results.json) | Comandos, exit codes, duração e hashes dos {python_tests} testes e do CI local. |
| [final-python-tests.log](final-python-tests.log) / [final-ci-local.log](final-ci-local.log) | Saída completa UTF-8 LF dos comandos finais. |
| [catalog-pin-verification.json](catalog-pin-verification.json) | HTTP 200, tamanho, SHA-256 e igualdade local dos três documentos públicos fixados. |
| [official-handler-review.json](official-handler-review.json) | Hashes dos arquivos de implementação revistos e os 16 contratos completados/restaurados, incluindo CTR/SoR. |
| [transferred-evidence.json](transferred-evidence.json) | Origens, encodings e hashes dos logs/recibos transferidos; preserva o hash original antes da normalização UTF-8 LF. |
| [resumed-evidence/desktop](resumed-evidence/desktop/) | Logs de kits reais, mídia inválida, consentimento, defaults, regressão, parser e build. |
| [resumed-evidence/native](resumed-evidence/native/) | MSVC SM/SM Rewrite, runtime_check MKDD, extrator KI sobre fixture e bootstrap MSVC. Sem mídia original. |
| [resumed-evidence/torch](resumed-evidence/torch/) | Proveniência, build intacto e probes nativos Torch; a falha do wrapper upstream também foi preservada. |
| [remaining-official-blockers.json](remaining-official-blockers.json) | Três impedimentos, fontes, hashes, alternativas oficiais e condição concreta de restauração. |
| [mario-official-tools-all-result.json](mario-official-tools-all-result.json) | Ferramentas Make oficiais compiladas com MSYS2 privado; não é o jogo completo. |
| [sm64plus-official-script-result.json](sm64plus-official-script-result.json) | Contrato do script oficial, CRLF/igncr, ferramenta e ausência de ROM; fontes intactas. |
| [ctr-ci-import-review.json](ctr-ci-import-review.json) | Caminho/hash/tamanho do BIN oficial; a revisão do contrato não foi contada como execução sintética. |

Os recibos anteriores continuam preservados. intermediate-python-tests-ctr-assertion.log
registra uma execução que falhou porque o teste ainda exigia o hash e a preparação
manual anteriores do CTR. A correção fortaleceu a expectativa do novo import_input;
o recibo final substitui aquela execução para aprovação. Os primeiros probes Mario
que usaram um alvo Make inexistente também permanecem nos logs, com a correção
documentada; não foram atribuídos como defeito upstream.

## Amplitude dos testes atuais

Os 15 positivos atuais são específicos por projeto. GOW/Pinyon/SSX/SoH/Mario/SM/
GT5/KI/MKDD/SoR têm provas de kit, negativas ou componentes conforme cada log;
FH1 verifica o manifesto oficial integral. Não se atribui um teste de jogo a
um pacote que apenas foi extraído. Pinyon teve extensão inválida e ausência de
aceite recusadas antes do setup; isso não certifica a identidade de uma ISO
original. SoR teve paridade dos 44 defaults, preservação INI e plano de launch
sintético; não houve boot.

SM e SM Rewrite produziram executáveis nativos sem ROM, preservando 124/193
arquivos fonte. MKDD produziu 42 objetos runtime_check sem link final de jogo
ou build de runtime OpenXR; OpenXR permaneceu ON. Os quatro Mario compilaram
ferramentas, não a recompilação completa que depende da ROM.

A falha CMake VandalHearts é limitada ao ambiente nativo Windows testado e não
foi ocultada por patches ou desativação de opções. Todos os resultados com
mídia original seguem desconhecidos, salvo o relato histórico já registrado
de SM64 Coop Deluxe.

## Reprodução e materiais externos

Execute os comandos de [INSTALLATION-COVERAGE.md](../../INSTALLATION-COVERAGE.md)
na raiz do repositório, usando Python com jsonschema. run-final-validation.py
executa a suíte e o ponto de entrada real do CI com contexto explícito da branch
de revisão. record-resumed-evidence.py transfere apenas textos da mesma área
de trabalho revisada; não é um downloader nem instalador de jogos.

research-cache, distribuições MSYS2, caches de compilação, kits binários e
fontes upstream expandidas são intermediários externos aos arquivos versionados.
Nenhum deles entra no complemento. O pacote final 1.5.76 contém apenas dois
JSONs e seu recibo é gerado depois do commit. Publicação de referências e
CI hospedado são verificados separadamente pela integração final.
""")
print(json.dumps(summary,ensure_ascii=True))
