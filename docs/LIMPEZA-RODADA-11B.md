# Relatório de limpeza — GetAll-Addon Rodada 11B (2026-11-23)

## Escopo e prevenção de perdas

A execução utilizou **um único diretório temporário dedicado** no Bradsson:

C:\Users\bradg\AppData\Local\Temp\GetAll-Rodada11B-20261123\

O checkout de código foi criado separadamente em:

C:\Users\bradg\Downloads\GetAll-Rodada11B\

**Regra:** eliminar somente arquivos e diretórios auxiliares comprovadamente criados na Rodada 11B e não usados como código de produção. Não tocar em arquivos ou diretórios pertencentes a outras rodadas, projetos, SDK, DLL instalada, backups ou cópias comerciais do usuário.

## Arquivos e pastas descartáveis removidos após a bateria local de testes

1. Diretório temporário dedicado GetAll-Rodada11B-20261123 inteiro, incluindo scripts descartáveis de inspeção, geração, patches e auditorias: inspect.py, verify_official.py, import_contract.py, patch_validator.py, patch_root.py, make_recipe.py, fix_test.py, make_harness.py, fix_harness.py, update_matrices.py, write_report.py, update_context.py, finaltests.py, stage.py e quaisquer outros scripts de teste gerados exclusivamente nesse diretório.
2. Subdiretório temporário ParserHarness, com Program.cs adaptado exclusivamente para este teste, cópia do .csproj, bin/ e obj/. O harness foi executado, mas não é componente do GetAll.
3. Cópia **temporária**, extraída do ZIP de integração, de GETALL-RODADA11A-SDK141-CONTRATOS/ dentro da mesma pasta. Os schemas, documentação e exemplos necessários já estão versionados no repositório.
4. Subdiretórios Python __pycache__/ e arquivos *.pyc gerados exclusivamente pelo validador em scripts/ e tests/ do novo checkout, sem afetar arquivos de código.
5. Pasta de extração temporária dos 96 JARs oficiais, criada pelo harness em %TEMP%\getall-round11b-official-<ID>: removida pelo próprio teste após validações positivas e negativas.

A exclusão será conferida por verificação de existência. Não é necessário manter executáveis de teste ou downloads duplicados na pasta Downloads.

## Arquivos preservados expressamente

- C:\Users\bradg\Downloads\GetAll-Rodada11B\: **checkout Git versionado** desta rodada, contendo código, 92 receitas, testes permanentes, schemas v1-v8, docs, histórico e configurações do repositório, para revisão posterior.
- GitHub brad38/GetAll-Addon: branch e Pull Request da Rodada 11B com histórico, hash SHA-256 e CI; **fonte de verdade após publicação**.
- Pacote original GetAll-Rodada11A-SDK141-Integration.zip e demais arquivos da pasta AllFixDesktop-sdk141-work, pertencentes ao desenvolvimento SDK do Codex.
- C:\Users\bradg\Downloads\GetAll-Round10-evidence\Severed_Chains_Windows.zip, **ZIP oficial anterior reutilizado como fixture**, SHA-256 164716cba1899cadf834506636de8da56721d695457c3b53c93c533999ef9bb4; não baixado novamente e não removido, pois pertence à Rodada 10.
- Diretórios GetAll das rodadas anteriores, AllFixDesktop, SDK, DLL instalada, arquivos de usuário, catálogos, mídia legítima e backups: não foram modificados, nem excluídos.
- Relatórios permanentes dentro de docs/, especialmente CHECKPOINT.md, RODADA-11B-SDK141-2026-11-23.md, HOMOLOGACAO-MIDIA-NECESSARIA.md, COBERTURA-CATALOGO.md, ESPECIFICACAO-CODEX-SDK.md e validations/severed-chains-release-3.0.0.md.

## Verificação final

Após os testes locais, foi feita a limpeza dos arquivos temporários listados, limitada exclusivamente aos caminhos criados na Rodada 11B. O diretório temporário dedicado e caches Python do novo checkout foram removidos; o checkout e seu histórico Git foram preservados. Os dados finais deverão ser conferidos no commit e PR. O teste de CI ocorre remotamente no GitHub, sem exigir temporários locais. **Nenhuma exclusão ampla em Downloads nem em AppData deve ocorrer.**


## Observação de compatibilidade Git/Windows

A main continha o schema v4 com bytes CRLF históricos (6426 bytes), apesar da política atual de LF em .gitattributes. O checkout novo no Windows inicialmente o sinalizou como modificado apenas por normalização de linhas. Para preservar **exatamente** o blob original (sem alterar ou publicar o v4), foi adicionado um override **local e específico** em GetAll-Rodada11B/.git/info/attributes desativando a conversão EOL somente para schemas/installation-recipe-v4.schema.json. Esse override não entra no commit ou PR; nenhum schema v1-v7 foi alterado semanticamente ou em bytes no repositório.
