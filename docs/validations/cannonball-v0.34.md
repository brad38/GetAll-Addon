# Validação experimental — cannonball v0.34

Jogo: outrun
Projeto oficial: cannonball
Repositório: https://github.com/djyt/cannonball
Release: https://github.com/djyt/cannonball/releases/tag/v0.34
ZIP oficial: cannonball-v034-w64.zip
Tamanho do ZIP baixado: 790148 bytes
SHA-256 ZIP: 2545d9b10cb10ed66bc5dc07aa5290577aa911370e79f06fafa5b561a846e303
Schema da receita: v5 (`schema_version: 5`)
Executável (`launch_file`): cannonball.exe
Pré-requisitos declarados: nenhum
Required files: cannonball.exe, SDL2.dll, config.xml, roms/roms.txt
Caminho da receita: recipes/outrun/cannonball/v0.34.json

Testado estaticamente: JSON Schema v5 (`installation-recipe-v5.schema.json`), `scripts/validate_recipes.py --require-jsonschema --check-git-blobs --check-catalog`, IDs/tag exatos, presença dos `required_files` no ZIP oficial e regras de caminhos v5.
Não testado: instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário nem inicialização real do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial Cannonball (v0.34) foi extraido. Copie os 31 arquivos originais do romset OutRun Revision B listados em roms/roms.txt (epr-10187.88 a opr-10268.99 e, opcionalmente, os arquivos alternativos da versao japonesa) para a pasta roms/ antes de iniciar cannonball.exe. Nenhuma ROM e fornecida pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll` 1.3.0

- **Data (UTC):** `2026-11-23T16:13:58Z`
- **Pacote baixado e conferido:** `cannonball-v034-w64.zip` (`790148` bytes, SHA-256 `2545d9b10cb10ed66bc5dc07aa5290577aa911370e79f06fafa5b561a846e303`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e operações declaradas concluídas pelo motor oficial `AllFix.dll` 1.3.0 (`Status=PartiallyCompleted`, `4/4` `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.

## Rodada 10 — importação v7 do romset OutRun Revision B

- v5 para v7, import_input_set arcade_romset com 31 arquivos obrigatórios, 2.064.384 bytes totais, CRC32/tamanho oficiais de src/main/roms.cpp tag v0.34, destino roms/.
- Divergência upstream: roms/roms.txt lista epr-10381a.132, mas o código de carga da mesma tag requer epr-10381b.132 (65.536 bytes, CRC32 BE8C412B). A receita usa o nome e checksum do loader; não presume versões intercambiáveis.
- ZIP oficial cannonball-v034-w64.zip: 790.148 B, SHA-256 2545d9b10cb10ed66bc5dc07aa5290577aa911370e79f06fafa5b561a846e303, 4/4 arquivos obrigatórios anteriores presentes e sem ROMs originais.
- Testes: schema v7/índice, parser SDK 1.4.0 e validador de ROM arcade sintético com conteúdo ASCII 123456789 (CRC32 CBF43926), adulteração e falta de arquivo rejeitadas.
- Não testado: romset comercial legítimo, instalação completa e primeiro boot; permanece experimental.
- Fonte: https://github.com/djyt/cannonball/blob/v0.34/src/main/roms.cpp
