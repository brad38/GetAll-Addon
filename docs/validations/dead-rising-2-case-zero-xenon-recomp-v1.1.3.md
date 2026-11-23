# Validação experimental — dead-rising-2-case-zero-xenon-recomp v1.1.3

Jogo: dead-rising-2-case-zero-case-west
Projeto oficial: dead-rising-2-case-zero-xenon-recomp
Repositório: https://github.com/wivi514/Dead_Rising_2_Case_Zero_Xenon_Recomp
Release: https://github.com/wivi514/Dead_Rising_2_Case_Zero_Xenon_Recomp/releases/tag/v1.1.3
ZIP oficial: CaseZeroRecomp-windows-x86_64.zip
Tamanho do ZIP baixado: 24956419 bytes
SHA-256 ZIP: f821dd717c08baa83b06ae11ece1963835bbe07816b43a52792f3040cfd99a28
Executável: CaseZeroRecomp/cz_runtime.exe
Required files: CaseZeroRecomp/cz_runtime.exe, CaseZeroRecomp/SDL2.dll, CaseZeroRecomp/dxcompiler.dll, CaseZeroRecomp/cz_defaults.env
Caminho da receita: recipes/dead-rising-2-case-zero-case-west/dead-rising-2-case-zero-xenon-recomp/v1.1.3.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial Dead Rising 2: Case Zero (v1.1.3) foi extraido. Copie seu pacote XBLA legitimo (Content/0000000000000000/58410A8D/000D0000/) para CaseZeroRecomp/assets/package/ (ou arraste-o para a janela inicial) e execute CaseZeroRecomp/cz_runtime.exe. Nenhum arquivo comercial e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:19:01Z`
- **Pacote baixado e conferido:** `CaseZeroRecomp-windows-x86_64.zip` (`24956419` bytes, SHA-256 `f821dd717c08baa83b06ae11ece1963835bbe07816b43a52792f3040cfd99a28`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 4/4 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
