# Validação experimental — body-harvest-recomp v0.1.0

Jogo: body-harvest
Projeto oficial: body-harvest-recomp
Repositório: https://github.com/danielgomesvieira2000/body-harvest-recomp
Release: https://github.com/danielgomesvieira2000/body-harvest-recomp/releases/tag/v0.1.0
ZIP oficial: body-harvest-recomp-0.1.0-windows-x64.zip
Tamanho do ZIP baixado: 17963566 bytes
SHA-256 ZIP: dd1ab059cb729f8657b2efb352e535b60fad0881eb93e11c1f7a1775c94e693b
Executável: body-harvest-recomp.exe
Required files: body-harvest-recomp.exe, SDL2.dll, dxcompiler.dll, dxil.dll
Caminho da receita: recipes/body-harvest/body-harvest-recomp/v0.1.0.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial, caminhos relativos seguros. include/bh/rom.h confirma 12582912 bytes (12 MiB) e SHA-1 bbb6666f5014a473747ee4145f036d9fb25d7348.
Não testado: instalação ponta a ponta no AllFix.exe com ROM original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima antes de promoção para validated).

Procedimento manual da receita: O pacote oficial Body Harvest Recompiled e sua ROM verificada body-harvest.us.z64 foram instalados. Execute body-harvest-recomp.exe e aponte para body-harvest.us.z64 no launcher.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:16:41Z`
- **Pacote baixado e conferido:** `body-harvest-recomp-0.1.0-windows-x64.zip` (`17963566` bytes, SHA-256 `dd1ab059cb729f8657b2efb352e535b60fad0881eb93e11c1f7a1775c94e693b`)
- **Resultado (`GameInstallationService.Run`):** `extraction_ok_awaiting_media` (`Status=Failed`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Execução interrompida na seleção de mídia obrigatória com retorno esperado `Status=Failed` (`A dependência obrigatória não foi selecionada.`) pois não há ROM/ISO comercial local; estrutura do ZIP oficial conferida integralmente (4/4 `required_files` e `launch_file` presentes).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
