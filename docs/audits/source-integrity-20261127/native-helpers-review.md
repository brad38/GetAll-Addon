# Auditoria dos auxiliares nativos — integridade e limites

**Snapshot Desktop:** `921295de12349e726f7ca21a5edd8a8ecee123d8`. Inspeção somente leitura; data de referência 27/11/2026, America/Fortaleza. O relatório estruturado é [native-helpers-review.json](native-helpers-review.json), com 13 achados H01–H13 associados aos IDs dos projetos. Horários UTC originais permanecem nos dados brutos quando registrados.

**Conclusão desta fatia:** foram encontradas alterações próprias em importadores, entradas de CLI e receitas de compilação. BlueWake tem três alterações reais de fonte do importador; King’s Field tem um ajuste de macro e um importador deliberadamente japonês com tabela inglesa opcional vazia; SoH admite uma correção de CLI cuja fonte alterada não foi recuperada. Isso impede afirmar que todos os auxiliares são cópias inalteradas do upstream. Nas árvores comparadas e wrappers lidos, não foi encontrada implementação AllFix de fases, personagens, regras, IA ou outras partes faltantes de gameplay. Essa conclusão se limita aos componentes efetivamente examinados e não demonstra boot ou completude dos jogos.

## Método e fronteira da prova

Foram lidos os wrappers e scripts próprios, comparados os bytes de cada membro dos arquivos-fonte preservados com as árvores extraídas e calculados hashes dos binários realmente disponíveis no Windows. BlueWake e os cinco arquivos Pikmin1 usados pelo build Nectar também tiveram identidade conferida em blobs Git obtidos do upstream durante esta auditoria.

A igualdade de uma árvore com seu ZIP/tar preservado demonstra a ausência de alterações nessa árvore em relação àquele arquivo. Ela **não comprova**, por si, que um EXE foi produzido exatamente daquela árvore, que todas as dependências são iguais, nem que o jogo funciona. Nenhum build foi repetido e nenhuma mídia comercial foi utilizada. A auditoria não usa README como substituto para a comparação: quando só há declaração documental, isso está explicitado.

Os recursos opcionais `SoHTorchPath`, `TwoShipZapdPath`, `PaperboatTorchPath`, `GhostshipTorchPath`, `StarshipTorchPath`, `SpaghettiTorchPath`, `LighthouseTorchPath`, `PicoriExtractorPath`, `NectarExtractorPath`, `KnowYourRoleBuilderPath` e `Gt4DiscHelperPath` são caminhos MSBuild externos, declarados em `AllFix.Desktop.csproj:119–155`. Estar no build do aplicativo não significa ter a origem completa versionada no repositório.

### Comparações efetivamente realizadas

| Componente | Arquivos originais comparados | Resultado nos bytes da árvore |
|---|---:|---|
| PaperBoat Torch | 770 | Nenhuma alteração ou ausência |
| Ghostship Torch | 768 | Nenhuma alteração ou ausência |
| Starship Torch | 598 | Nenhuma alteração ou ausência |
| Lighthouse Torch | 776 | Nenhuma alteração ou ausência |
| Spaghetti Torch | 638 | Nenhuma alteração ou ausência |
| King’s Field Enhanced, fonte do helper A | 346 | Somente guarda de `NOMINMAX` |
| Know Your Role, fonte preservada do projeto | 51 | Nenhuma alteração ou ausência |
| Picori | 2.397 | Nenhuma alteração ou ausência |
| GT4, apenas crate `gt4l-disc` | 16 | Nenhum arquivo original alterado; wrapper próprio adicionado |
| TwoShip, ZAPDTR | 232 | Nenhuma alteração ou ausência |
| TwoShip, OTRExporter | 176 | Nenhuma alteração ou ausência |
| TwoShip, libultraship | 430 | Somente `common.cmake`: CRLF e download STB trocado por cópia local |
| Nectar, leitores e suporte preservados | 13 | Blobs iguais ao manifesto Git preservado; cinco entradas do build conferidas também no upstream ao vivo |

As cinco árvores Torch não tinham fontes C/C++ extras na varredura. Para as outras árvores, a varredura de extras omitiu diretórios gerados/dependências/`bin`/`obj`; a comparação de membros originais não os omitiu. O wrapper GT4 em `src/bin` foi verificado separadamente. Os números não são uma afirmação de auditoria semântica linha a linha de toda dependência.

Fontes: [comparações Torch](native-torch-tree-comparisons.json), [outros projetos](native-other-source-comparisons.json), [TwoShip e tabela de tradução](native-twoship-comparisons.json), [hashes dos binários](native-helper-actual-hashes.json).

## H01 — BlueWake: importador modificado, runtime separado

O ZIP `Tools/NativeExtractors/bluewake-import-windows-x64.zip` inclui fonte, compatibilidade POSIX/Windows, licença e build script. Seu SHA-256 observado é `5dd29c5f689f55135a9b1591525cfb9ff917c1b5ee699c71629fcc671400a6df`.

O `disc_import.c` original foi obtido de [BlueWake v0.12.0](https://github.com/chrissotraidis/bluewake/blob/v0.12.0/apple/ios/src/disc_import.c), blob `d76654f46af92041371528c61fff6360ac2c5d46`, e comparado com a cópia realmente embarcada. As diferenças são:

- `read_at`, linha original 128: rejeição de alocação maior que 64 MiB.
- `write_rel`, linha original 317: rejeição de tamanho menor que 0x44, nomes maiores que 100 caracteres e caracteres fora do conjunto ASCII permitido.
- Linha original 637: `getenv("BLUEWAKE_ACCEPT_DOL_SHA1")` vira `NULL`, removendo a aceitação de um executável alternativo fornecida por variável de ambiente.

O próprio upstream já reescrevia o alinhamento dos RELs para 4; essa operação não foi criada pelo AllFix. Os dez arquivos de cabeçalho, compatibilidade e licença copiados conferem com os blobs upstream.

O `main.c` próprio verifica disco GZLE01 revisão 0 de tamanho completo, chama `bluewake_disc_prepare` e exige `main.dol` e 415 RELs com alinhamento correto. O motor Desktop acrescenta validação do SHA-1 do DOL. É uma adaptação e restrição do importador, não implementação de gameplay. Não foi comprovada extração com ISO genuína. Evidência completa: [fonte embarcada](bluewake-helper-source.json), [original e blobs oficiais](bluewake-original-importer.json) e `Services/GameInstallationBlueWake.cs`.

## H02 — Open Nectar: wrapper próprio sobre leitor oficial

O build usa o leitor GameCube de Pikmin1 e SHA-256 do commit `c0ceb05eb8cebfc7d25ee0834c8ebc1a6b20226c`, também para os discos Pikmin2. Os cinco arquivos de compilação/suporte conferem com a [consulta upstream preservada](nectar-live-source-pins.json).

O wrapper próprio de 57 linhas trata argumentos, tamanho do disco, diretório vazio, quatro identidades admitidas, progresso e erro. O último argumento `true` de `extractGameCubeImage` é `verifyWrites`: conserva a releitura e comparação dos arquivos extraídos. A checagem do hash completo da mídia está no Desktop, em `SelectNectarDiscs`; não foi substituída por uma checagem de cabeçalho.

O motor escreve marcadores de edição/build e copia o executável oficial apropriado de Pikmin2 para o layout esperado. Não compila o jogo nem cria lógica faltante. Usar o leitor Pikmin1 para Pikmin2 é uma decisão própria de integração; fonte inalterada não prova a execução correta dessa combinação com discos reais. Ver `extract.cpp` e `Build-NectarExtractor.ps1` em [inputs preservados](native-helper-build-inputs.json) e `Services/GameInstallationNectar.cs:22–154`.

## H03 — King’s Field: importação japonesa e tradução opcional vazia

A árvore de compilação `kingsfield-helper-a/source/kf1-enhanced-ac147450249c95b8d7683300292a2761796cb611` difere do ZIP original em um único arquivo: `src/platform/translation_ppf.cpp`, onde `#define NOMINMAX` recebe guarda `#ifndef`.

Há também código próprio: `kingsfield-import.cpp` invoca `kf::disc_extract` e `kf::disc_verify_directory` com `Language::Japanese`. O build executa o script original com `embed --input generated/absent.kfdelta --optional`. O arquivo gerado foi lido: ele contém `std::array<unsigned char, 0> english_patch_data`.

Portanto, **o helper não contém a tradução inglesa opcional** e atende ao perfil japonês. Isso não demonstra remoção do inglês do executável oficial do jogo: o componente compilado aqui é o importador. Tampouco permite prometer preparação em inglês. Fontes: `Tools/NativeExtractors/build-kingsfield-import.ps1:29–42`, `kingsfield-import.cpp` e comparações JSON acima.

## H04 — Know Your Role: republicação do launcher/builder oficial

O script fixado valida hashes dos ZIPs, copia RecompOne para a árvore do projeto, insere três locks NuGet, restaura em modo locked e publica o projeto Launcher. Não há substituição de C# de gameplay no script. Os 51 arquivos da fonte preservada `eca626b79ffeab146b84e8de260e43713fb9a649` correspondem ao ZIP.

O binário de 76.668.714 bytes foi identificado por hash. Porém, a comparação de 51 arquivos não cobre todos os fontes/dependências RecompOne e não é uma recompilação independente do EXE. A conclusão correta é “não houve reescrita de fonte no build recipe examinado e na árvore do projeto comparada”, não “todo o runtime foi provado idêntico”. Fonte: `Tools/NativeExtractors/build-know-your-role.ps1` e [comparações](native-other-source-comparisons.json).

## H05 — Ship of Harkinian: lacuna concreta de fonte

`AddonSdk/INSTALACAO-V9.md:40` registra explicitamente uma correção da entrada CLI para chamar `SohTorch::Extract` com os bytes da ROM, usando Shipwright `f0599f96f8d442f26d0fa1c5cedafddacd56633f` e Torch `2ab12fe9660aec04e02ee89fe81baed304a1a1d6`.

O EXE observado corresponde ao hash esperado `e1d221f2a58ad56581b85da752e0bc236e577a26a2e145404764ca836779be02`. Os scripts `recover-soh-resource.py` e `verify-soh-resource.py`, lidos sem executá-los, recuperam esse recurso de um AllFix.exe anterior. Eles não reconstroem a fonte alterada.

As buscas delimitadas não localizaram o before/after dessa correção. **A integridade de fonte deste helper permanece inconclusiva.** Identidade binária não preenche essa lacuna. Não se pode incluir SoH em “todos os fontes inalterados”. Localização da admissão, hash, busca e seus limites estão em [native-soh-provenance-gap.json](native-soh-provenance-gap.json).

## H06 — TwoShip: build próprio, extratores originais

ZAPDTR `ee3397a365c5f350a60538c88f0643f155944836` e OTRExporter `32e088e28c8cdd055d4bb8f3f219d33ad37963f3` estão byte a byte iguais aos ZIPs. Em libultraship `7cb10226e7875ec48ceec2f841d00afd84eef964`, a única alteração observada é CRLF e a troca de download de `stb_image.h` por cópia de uma entrada local fixada.

O `prepare-deps.py` próprio substitui o CMake de topo para compilar o extrator, seleciona MM e desativa scripting/auto-vcpkg nessa compilação. Os patches ImGui/StormLib são os arquivos do libultraship upstream comparado. Desativar scripting no helper não equivale a remover scripts do jogo oficial distribuído. Não se demonstrou equivalência de todos os outputs das dependências. Ver [inputs](native-helper-build-inputs.json) e [comparações](native-twoship-comparisons.json).

## H07–H11 — Starship, PaperBoat, Ghostship, Spaghetti e Lighthouse

Todas as árvores Torch comparadas são iguais aos arquivos-fonte preservados nos pins registrados no JSON. Os builds selecionam formatos dos jogos correspondentes e podem excluir UI e formatos de outros jogos. Isso afeta o executável de extração; os jogos usam seus pacotes oficiais.

O caso Lighthouse exige uma distinção: `lighthouse-cli.patch` é uma série de cinco commits upstream de Jeod, começando em `ee95c850...` e terminando em `339b695b...`. O arquivo contém inclusive mudanças de threads/menu/estado do jogo. **Sua presença nos materiais de pesquisa não demonstra aplicação pelo AllFix.** A árvore Torch realmente compilada não tem essas mudanças e o handler `GameInstallationLighthouse.cs:64–79` usa o kit oficial fixado com Torch separado. Não foi identificado um passo de build/patch do runtime Lighthouse nesse fluxo.

Para Starship, o histórico registra CLI oficial retornando zero sem produzir resultado para entrada inválida; saída do processo isoladamente não é prova de sucesso. Para Spaghetti, esta fatia não revalidou independentemente a proveniência de todo input gerado, inclusive `defines.h`. Para todos os cinco, faltam prova de reprodução binária completa e teste com ROM genuína.

## H12 — Picori: alvo de extração existente

Os 2.397 arquivos preservados de `999sian/tmc@d377558d973c648e8d0dc491bf99af9aaa0d8067` correspondem ao tar original. O script próprio compila sete entradas originais: API/main do extrator, sons embutidos, índice/pipeline/log/pak dos assets. Gera `sounds.json.h` a partir do JSON original e escolhe `PC_PORT`, `NON_MATCHING`, `USA`, `ENGLISH`, `REVISION=0`.

São definições do helper de extração e não implementação de jogo faltante. Não confundir este port Picori com outra base de decompilação Minish Cap sem port nativo. A equivalência de todas as dependências e o funcionamento com ROM real não foram demonstrados. Fonte: [Build-PicoriExtractor.ps1 preservado](native-helper-build-inputs.json).

## H13 — GT4: wrapper sobre biblioteca oficial

A biblioteca `gt4l-disc` do commit `7e069b4b9a9939cda48942994aa2e509c95a00ff` conserva seus 16 arquivos originais na árvore usada em `helper-production-4`. O build acrescenta `src/bin/getall-gt4-disc.rs`; o wrapper real tem o mesmo SHA-256 `4d37840b5a096a790356cbe06c585697d71b7717972eaab55fdfafb7119823bb` da fonte publicada.

As 84 linhas carregam pins oficiais, identificam o disco, chamam `setup::run` ou `spec2::run`, depois exigem `check_installed == Installed::Ready`. Tratam caminhos, staging, progresso e códigos de erro. Não contêm reimplementação de CPU/GPU ou gameplay. O build usa Cargo locked e não reescreve a biblioteca original. Essa comparação se limita à crate e não atesta todo GT4 ou todas as dependências Cargo. Fontes: `Tools/Gt4Disc/getall-gt4-disc.rs:19–83`, `build-gt4-disc.ps1` e [hashes observados](native-helper-actual-hashes.json).

## O que pode ser afirmado ao usuário

Houve alteração de código auxiliar e decisões próprias de preparação. Não é correto apresentar tudo como “apenas baixar o launcher” ou “todos os fontes intocados”. Dentro desta fatia, o resultado observado não é uma tentativa identificada de completar gameplay ausente. **SoH permanece sem verificação completa do patch**, e nenhum dos resultados deve ser chamado de jogo homologado por boot somente porque compilou, extraiu um fixture ou passou um teste negativo.

Somente relatórios e evidências textuais pequenos foram acrescentados. Não foram alterados produto, receitas, fontes originais, binários, dependências ativas ou mídias.

