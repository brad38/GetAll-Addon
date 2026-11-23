# Validação experimental — dinosaur-planet-recompiled-dino-recomp v0.3.0

Jogo: dinosaur-planet
Projeto oficial: dinosaur-planet-recompiled-dino-recomp
Repositório: https://github.com/DinosaurPlanetRecomp/dino-recomp
Release: https://github.com/DinosaurPlanetRecomp/dino-recomp/releases/tag/v0.3.0
ZIP oficial: DinosaurPlanetRecompiled-v0.3.0-Windows-x64.zip
Tamanho do ZIP baixado: 20998063 bytes
SHA-256 ZIP: 4a1ea0a9d41516f33a8d90aaa50a221d3a5be749b1864c8e1225207d663472a8
Executável: DinosaurPlanetRecompiled.exe
Required files: DinosaurPlanetRecompiled.exe, SDL2.dll, dxcompiler.dll, dxil.dll
Caminho da receita: recipes/dinosaur-planet/dinosaur-planet-recompiled-dino-recomp/v0.3.0.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros.
Não testado: instalação ponta a ponta no AllFix.exe com ROM original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial de Dinosaur Planet (v0.3.0) foi extraido. Execute DinosaurPlanetRecompiled.exe na pasta instalada e Forneca sua ROM compativel de Dinosaur Planet no menu inicial. Nenhuma ROM e fornecida pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:16:53Z`
- **Pacote baixado e conferido:** `DinosaurPlanetRecompiled-v0.3.0-Windows-x64.zip` (`20998063` bytes, SHA-256 `4a1ea0a9d41516f33a8d90aaa50a221d3a5be749b1864c8e1225207d663472a8`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `4/4` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 4/4 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
