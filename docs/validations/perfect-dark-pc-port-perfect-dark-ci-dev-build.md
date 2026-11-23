# Validação experimental — perfect-dark-pc-port-perfect-dark ci-dev-build

Jogo: perfect-dark
Projeto oficial: perfect-dark-pc-port-perfect-dark
Repositório: https://github.com/perfect-dark-pc-port/perfect_dark
Release: https://github.com/perfect-dark-pc-port/perfect_dark/releases/tag/ci-dev-build
ZIP oficial: pd-x86_64-windows.zip
Tamanho do ZIP baixado: 25739820 bytes
SHA-256 ZIP: 56e6a2f8bad36bd90f0d396c1d525b953adcc1a20157f594b90a7530d58258d3
Executável: pd-x86_64-windows/pd.x86_64.exe
Required files: pd-x86_64-windows/pd.x86_64.exe, pd-x86_64-windows/pd.pal.x86_64.exe, pd-x86_64-windows/pd.jpn.x86_64.exe, pd-x86_64-windows/SDL2.dll, pd-x86_64-windows/libgcc_s_seh-1.dll, pd-x86_64-windows/libwinpthread-1.dll, pd-x86_64-windows/zlib1.dll
Caminho da receita: recipes/perfect-dark/perfect-dark-pc-port-perfect-dark/ci-dev-build.json

Testado estaticamente: JSON, schema v3, IDs e tag exatos, presença dos required_files no ZIP oficial e caminhos relativos seguros. port/src/romdata.c confirma ROMDATA_ROM_SIZE=33554432 e caminho data/pd.ntsc-final.z64 (Classe A estrutural sem etapas manuais).
Não testado: instalação ponta a ponta no AllFix.exe com mídia original legítima nem inicialização do jogo.
Status: experimental (aguarda homologação funcional com mídia legítima).

Correção pós-teste no AllFix.dll: o motor C# rejeitou import_input sem sha1/sha256 ('Operação incompatível'); como o projeto oficial publica apenas MD5, ajustado para manual_steps e registrado pedido de suporte a md5 em inputs para o Codex.

## Teste de instalação no motor `AllFix.dll`

- **Data (UTC):** `2026-11-23T05:17:21Z`
- **Pacote baixado e conferido:** `pd-x86_64-windows.zip` (`25739820` bytes, SHA-256 `56e6a2f8bad36bd90f0d396c1d525b953adcc1a20157f594b90a7530d58258d3`)
- **Resultado (`GameInstallationService.Run`):** `extracted_awaiting_manual_media` (`Status=PartiallyCompleted`)
- **Verificação de arquivos:** `7/7` `required_files` presentes; `launch_file_exists=True`
- **Observação:** Extração e validação concluídas em pasta temporária pelo motor real (`Status=PartiallyCompleted`, 7/7 `required_files` e `launch_file` presentes em `Destination`).
- **Homologação final:** Permanece `experimental` até instalação ponta a ponta no `AllFix.exe` com mídia legítima do usuário e boot real comprovado do jogo.


## Rodada 8 — upgrade experimental SDK 1.3.0

- **Receita atualizada:** schema_version 3 para **5**; o indice permanece experimental. A receita anterior exigia copia manual da midia original; agora usa import_input no escopo installation e validacao nativa antes da escrita.
- **ROM original:** MD5 e03b088b6ac9e0080440efed07c1e40f; destino exato pd-x86_64-windows/data/pd.ntsc-final.z64. A imagem USA v1.1 possui 33554432 bytes e cabecalho 80371240. O caminho automatico e confirmado pelo README e por port/src/romdata.c do projeto.
- **Pacote oficial:** ZIP baixado novamente, SHA-256 56e6a2f8bad36bd90f0d396c1d525b953adcc1a20157f594b90a7530d58258d3; executavel e DLLs obrigatorias conferidos; nenhuma ROM/ISO no pacote.
- **Contrato/ambiente:** parser de receitas da AllFix.dll compilada com SDK 1.3.0, incluindo as 90 receitas; criterios cumulativos de hash, tamanho e assinatura conferidos estaticamente e por testes com dados sinteticos.
- **Teste funcional pendente:** nao havia ROM legitima para executar a importacao real e o boot do jogo. Nenhum teste de jogo real foi realizado e nenhum status validated foi concedido.
- **Referencia oficial:** https://github.com/perfect-dark-pc-port/perfect_dark/blob/port/README.md
