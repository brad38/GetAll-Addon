# GoldenEye 007 PC Port v0.5.0 — receita experimental

- **Jogo:** `goldeneye-007`; **projeto:** `goldeneye-007-pc-port`; repositório: [jkdansereau/goldeneye-pc-port](https://github.com/jkdansereau/goldeneye-pc-port).
- **Release:** `v0.5.0`; pacote Windows `goldeneye-pc-port-0.5.0-win64.zip`, 17.178.242 bytes pela API do GitHub.
- **ZIP inspecionado diretamente:** exe `goldeneye-pc-port-0.5.0-win64/ge007.x86_64.exe` e cinco dependências listadas em `required_files` (a DLL libstdc++-6.dll está no ZIP, mas não é um caminho válido na gramática do schema); SHA-256 do ZIP baixado `b49bfb826566367a4d1af16466530f0fadd85e522b33859521d849c143a005ef`.
- **ROM oficial exigida:** USA NTSC-U, `.z64`, 12.582.912 bytes, magic `80371240`, SHA-1 `abe01e4aeb033b6c0836819f549c791b26cfde83`, conforme README do projeto. **A ROM não está incluída.**
- **Importação declarativa:** `import_input` com `scope=installation`, target `goldeneye-pc-port-0.5.0-win64/data/ge007.ntsc-final.z64`. A pasta interna corresponde ao layout real do ZIP. O usuário escolhe a ROM legítima e o host valida o arquivo antes de copiar.
- **Execução:** `launch_file=goldeneye-pc-port-0.5.0-win64/ge007.x86_64.exe`, somente após o motor registrar uma instalação completa verificada.
- **SHA-256 do JSON da candidata:** `9f7a669c9dca4bf19246ac281192132832ad6d5fc2db5f53a0687b3dea47c1b9`.
- **Testes:** schema v3 exato do SDK 1.1, sintaxe JSON, IDs, arquivo/tag oficial, lista de required_files presente no ZIP, caminhos relativos, critério SHA-1 e rejeição sintética de ROM adulterada por digest: **aprovados**. Teste da execução completa com ROM original legítima e botão Jogar agora: **não executado**.
- **Status:** `experimental` (não recomendada nem instalada pelo host). Só passar para `validated` após teste positivo integrado de importação e inicialização.

**Referências:** [README original](https://github.com/jkdansereau/goldeneye-pc-port/blob/main/README.md) · [Release v0.5.0](https://github.com/jkdansereau/goldeneye-pc-port/releases/tag/v0.5.0).

O pacote, os scripts e as DLLs da Release não são publicados no GetAll-Addon; a receita contém apenas JSON.
