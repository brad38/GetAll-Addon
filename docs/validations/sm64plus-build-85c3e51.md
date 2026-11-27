# SM64Plus — build-85c3e51

Status: experimental, fluxo integral implementado aguardando ROM original e primeiro boot.
SDK minimo: 1.5.64. Fonte oficial fixada em 85c3e5198f051b990da98ec0bcb7fc9f3197df65.
Arquivo: 11258099 bytes; SHA-256 c993a13a96e99ae6fac8534ff00f96bfdbeb3adfca3754f25500011bfcaaa9d6.
A receita LauncherMirror anterior permanece disponivel; nao foi promovida a validated.

O motor prepara o ZIP verificado, solicita a ROM original americana de 8 MiB em .z64 e verifica SHA-1 antes do consentimento.
Provisiona 55 pacotes MSYS2/UCRT64 fixados por SHA-256, sem instalar o MSYS2 globalmente, e executa o Makefile em staging.
Aplica ajustes locais ao diretorio de trabalho do jogo e a arquitetura x86-64; prepara PE AMD64, SDL2 e recursos gfx e registra o resultado.
Jogar usa o executavel local e revalida os recursos registrados.

Evidencias locais: evidence-r18/sm64plus-handoff.
- 55 pacotes processados pelo motor C#; preflight oficial chegou a rejeicao esperada por ROM ausente.
- ZIP oficial passou pela preparacao do motor, seletor, cancelamento, recusa de ROM de tamanho correto mas hash invalido antes do consentimento.
- 10 verificacoes especificas C#; 1315 verificacoes de regressao aprovadas.
- Parser: 142 receitas; Python: 46 testes; JavaScript: 3 testes.
- Nao houve compilacao integral positiva com ROM original, nem primeiro boot. Nenhum arquivo de jogo foi distribuido.
