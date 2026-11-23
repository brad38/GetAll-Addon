# GoldenEye 007 PC Port v0.5.0 — receita experimental

- **Jogo:** `goldeneye-007`; **projeto:** `goldeneye-007-pc-port`; repositório: [jkdansereau/goldeneye-pc-port](https://github.com/jkdansereau/goldeneye-pc-port).
- **Release:** `v0.5.0`; pacote Windows `goldeneye-pc-port-0.5.0-win64.zip`, 17.178.242 bytes pela API do GitHub.
- **ZIP inspecionado novamente com SDK 1.2:** executáveis `ge007.x86_64.exe` e `prepare-assets/ge007-convert.exe`, e DLLs `libgcc_s_seh-1.dll`, `libstdc++-6.dll`, `libwinpthread-1.dll`, `SDL2.dll`, `zlib1.dll`, todos sob `goldeneye-pc-port-0.5.0-win64/` (no caso do conversor, sob `prepare-assets/`). SHA-256 do ZIP oficial: `b49bfb826566367a4d1af16466530f0fadd85e522b33859521d849c143a005ef`.
- **ROM oficial exigida:** USA NTSC-U, `.z64`, 12.582.912 bytes, magic `80371240`, SHA-1 `abe01e4aeb033b6c0836819f549c791b26cfde83`, conforme README do projeto. **A ROM não está incluída.**
- **Importação declarativa:** `import_input` com `scope=installation`, target `goldeneye-pc-port-0.5.0-win64/data/ge007.ntsc-final.z64`. A pasta interna corresponde ao layout real do ZIP. O usuário escolhe a ROM legítima e o host valida o arquivo antes de copiar.
- **Execução:** `launch_file=goldeneye-pc-port-0.5.0-win64/ge007.x86_64.exe`, somente após o motor registrar uma instalação completa verificada.
- **SHA-256 do JSON publicado com a DLL adicional:** `9e0adef9cb292cf915f244cdf8d030b8b537b7aa68d0cb2ecbfe548d1eb91d05`. A receita continua no schema v3; `required_files` foi ampliado usando o padrão de caminhos do SDK 1.2.
- **Testes:** schema v3 herdado pelo SDK 1.2, lista de arquivos no ZIP, paths, IDs, tag, verificações da ROM por SHA-1 e tamanho; parser real da DLL Release do host 1.2 aceitou a entrada `libstdc++-6.dll`. O harness externo do SDK 1.2 passou em 27/27 testes sintéticos de importação, integridade, primeira preparação e rejeições. **Não houve teste funcional com ROM legítima**, nem execução da interface gráfica.
- **Status:** `experimental` (não recomendada nem instalada pelo host). Só passar para `validated` após teste positivo integrado de importação e inicialização.

**Referências:** [README original](https://github.com/jkdansereau/goldeneye-pc-port/blob/main/README.md) · [Release v0.5.0](https://github.com/jkdansereau/goldeneye-pc-port/releases/tag/v0.5.0).

O pacote, os scripts e as DLLs da Release não são publicados no GetAll-Addon; a receita contém apenas JSON.
