# Validação experimental — knowyourrolerecomp v0.2.0

Jogo: wwf-smackdown-2-know-your-role
Projeto oficial: knowyourrolerecomp
Repositório: https://github.com/Comfubar/KnowYourRoleRecomp
Release: https://github.com/Comfubar/KnowYourRoleRecomp/releases/tag/v0.2.0
ZIP oficial: KnowYourRole-win-x64.zip
Tamanho do ZIP baixado: 127898385 bytes
SHA-256 ZIP: 5771e291f13c621537301922bb63fbb8e3b9645ec30a7c3bc8359fe978da4e2a
Executável: KnowYourRole-v0.2.0-win-x64/KnowYourRole.exe
Required files: KnowYourRole-v0.2.0-win-x64/KnowYourRole.exe, KnowYourRole-v0.2.0-win-x64/KnowYourRole-files/runtime/KnowYourRole.Game.exe
Caminho da receita: recipes/wwf-smackdown-2-know-your-role/knowyourrolerecomp/v0.2.0.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. Layout e caminhos relativos conferidos no ZIP oficial.
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Procedimento manual da receita: O pacote oficial de WWF SmackDown! 2: Know Your Role (v0.2.0) foi extraido. Para jogar, abra KnowYourRole.exe em KnowYourRole-v0.2.0-win-x64/ e selecione o arquivo .cue/.bin da sua copia NTSC-U SLUS-01234. Nenhum arquivo comercial ou ROM e distribuido pelo GetAll-Addon.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:17:35Z`
- **Pacote baixado e conferido:** `KnowYourRole-win-x64.zip` (`127898385` bytes, SHA-256 `5771e291f13c621537301922bb63fbb8e3b9645ec30a7c3bc8359fe978da4e2a`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `2/2` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 2/2 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.
