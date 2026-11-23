# Validação experimental — donkey-kong-64-recompiled-dk64-rekongpiled v1.0.3

Jogo: donkey-kong-64
Projeto oficial: donkey-kong-64-recompiled-dk64-rekongpiled
Repositório: https://github.com/Rainchus/Donkey-Kong-64-Recompiled
Release: https://github.com/Rainchus/Donkey-Kong-64-Recompiled/releases/tag/v1.0.3
ZIP oficial: DK64Recompiled-Windows-Release-1-0-3.zip
Tamanho do ZIP baixado: 19986113 bytes
SHA-256 ZIP: bfde3985365247f083ee47568b496eaf8a4a0845155a95802bc8f4a4871c60d5
Executável: DK64Recompiled.exe
Required files: DK64Recompiled.exe, SDL2.dll, dxcompiler.dll, dxil.dll, libcurl.dll, zlib1.dll
Caminho da receita: recipes/donkey-kong-64/donkey-kong-64-recompiled-dk64-rekongpiled/v1.0.3.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros.
Não testado: instalação ponta a ponta no AllFix.exe com ROM original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial de Donkey Kong 64 (v1.0.3) foi extraido. Execute DK64Recompiled.exe na pasta instalada e Escolha sua ROM original de Donkey Kong 64 (US) no menu inicial. Nenhuma ROM e fornecida pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:16:52Z`
- **Pacote baixado e conferido:** `DK64Recompiled-Windows-Release-1-0-3.zip` (`19986113` bytes, SHA-256 `bfde3985365247f083ee47568b496eaf8a4a0845155a95802bc8f4a4871c60d5`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `6/6` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 6/6 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
