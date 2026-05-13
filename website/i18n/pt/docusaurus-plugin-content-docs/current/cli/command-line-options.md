---
title: Opcoes de linha de comando
description: Referencia das opcoes de inicializacao do IaC Code e flags de execucao unica.
---

# Opcoes de linha de comando

As opcoes de linha de comando alteram como o IaC Code inicia. Use-as antes de entrar no REPL interativo, ou combine-as com `--prompt` para automacao de execucao unica.

| Opcao | Finalidade |
|---|---|
| `-h`, `--help` | Mostra a ajuda do CLI e sai. Use para inspecionar as opcoes suportadas pela sua versao instalada. |
| `-v`, `-V`, `--version` | Imprime a versao do IaC Code instalada e sai. |
| `-m <model>`, `--model <model>` | Inicia com um modelo LLM especifico. Substitui o modelo salvo para a execucao atual. |
| `-p <prompt>`, `--prompt <prompt>` | Executa um unico prompt e sai. Habilita o modo nao interativo. Use `--prompt -` para ler o prompt a partir da entrada padrao. |
| `--output-format <format>` | Define o formato de saida para o modo nao interativo. Os valores suportados sao `text`, `json` e `stream-json`. O padrao e `text`. |
| `--max-turns <number>` | Limita o numero maximo de turnos do agente no modo nao interativo. O padrao e `100`. |
| `-d`, `--debug` | Habilita o log de depuracao para a execucao atual. No modo interativo, use `/debug` para inspecionar ou alterar o log de depuracao apos a inicializacao. |
| `-r <session-id>`, `--resume <session-id>` | Retoma uma sessao anterior pelo ID. Serve para retornar a uma conversa conhecida. |
| `-c`, `--continue` | Retoma a sessao mais recente. Nao pode ser usada junto com `--resume`. |

## Comandos de inicializacao comuns

Inicie o REPL interativo com o modelo salvo:

```bash
iac-code
```

Inicie com um modelo especifico para esta execucao:

```bash
iac-code --model qwen3.6-plus
```

Execute um prompt unico:

```bash
iac-code --prompt "Create an OSS Bucket"
```

Leia o prompt a partir da entrada padrao:

```bash
echo "Create a VPC and two ECS instances" | iac-code --prompt -
```

Retome a ultima sessao:

```bash
iac-code --continue
```
