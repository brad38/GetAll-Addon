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

## Fluxo integral implementado na prévia do SDK 1.5.50

O motor fixa o pacote oficial e seu manifesto de 278 arquivos. Seleciona o BIN MODE2/2352 NTSC-U SLUS-01234 de 746266080 bytes pelo SHA-1 Redump 893F354EA412068CCFB4E64BBF144FCF770AD6A6. Gera o CUE no staging e compila com o launcher de código-fonte fixado, em modo CLI, sem iniciar o jogo. O registro do upstream deve confirmar a versão e os hashes de SLUS_012.34 e EXE.PAC. São conferidas as 16 bibliotecas esperadas. Antes da mudança de pasta, o motor grava CdPath no destino final e preserva os demais campos das configurações.

Dois builds do helper a partir dos commits eca626b79ffeab146b84e8de260e43713fb9a649 e d54b944fd3a7e3eaaac4cd7e62ea460440c3f9e7 produziram o mesmo SHA-256. O motor exercitou preparo do ZIP oficial, cancelamento, rejeição de mídia truncada, execução do compilador local contra um disco sintético e plano de lançamento com itens simulados. Compilação do jogo com disco original e primeiro boot aguardam homologação. A receita permanece experimental.
