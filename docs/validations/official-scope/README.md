# Provas da revisão de instalações oficiais

## Resultado final local — 28/11/2026

- **146 receitas**, **134 ativas**, **12 desativadas**; 134 projetos com automação.
- **79 testes Python aprovados**, validador estrito e ponto de entrada CI local aprovado.
- Desktop: **2312 verificações**, parser **146/146**, build WPF e harness sem avisos/erros.
- Catálogo fixado **e4fdde9d7c128f79eb19cf99ea07e2e9b628127a**, documentos remotos idênticos ao checkout.
- Nenhuma instalação completa, boot ou sessão de gameplay com mídia original nesta retomada.

[final-coverage-summary.json](final-coverage-summary.json) resume cada eixo;
[catalog-coverage.json](catalog-coverage.json) contém os 137 projetos.
O [ledger](../../installation-evidence.json) vincula cada alegação à receita
exata e à prova com hash.

## Índice das provas

| Arquivo / grupo | Conteúdo e limite |
|---|---|
| [final-validation-results.json](final-validation-results.json) | Comandos, exit codes, duração e hashes dos 79 testes e do CI local. |
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
