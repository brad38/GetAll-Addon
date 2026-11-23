# SDK 1.4.0 - etapa A (schema v6)
Receitas v3/v5 permanecem aceitas; protocolo 1.0 permanece inalterado.
assets: opcional e exclusivo de v6; 1-16 itens e limite agregado de 64 GiB.
Campos: name, target, size, sha256, kind (portable_executable ou payload).
portable_executable exige target .exe igual ao launch_file e presente em required_files.
Assets adicionais são fornecidos por IInstallationAssetProvider como arquivos locais; o motor verifica SHA-256 e tamanho antes de aplicar a receita. VerifiedAssetBundle.DownloadAsync baixa assets de releases GitHub oficiais com hash obrigatório e limpeza em falhas. O serviço já foi integrado ao fluxo da interface e oferece progresso e cancelamento. GitLab multi-asset ainda não é suportado.
payload é copiado como dado, sem execução ou extração automática.
Instaladores EXE/MSI nunca são executados nesta etapa.
O executável é validado pelo formato PE e por SHA-256. Mesmo um PE válido não prova que seja um jogo ou que seja confiável. A execução depende de ação do usuário.
