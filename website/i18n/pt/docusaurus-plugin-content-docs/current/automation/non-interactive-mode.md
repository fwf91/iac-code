---
title: Modo nao interativo
description: Execute prompts unicos a partir de argumentos ou stdin.
---

# Modo nao interativo

O modo nao interativo executa um unico prompt e sai. Use-o quando quiser que o IaC Code produza saida para uma tarefa repetivel sem permanecer no REPL.

Use `--prompt` para passar o prompt diretamente:

```bash
iac-code --prompt "Create an OSS Bucket"
```

Use `--prompt -` para ler o prompt a partir da entrada padrao:

```bash
echo "Create a VPC and two ECS instances" | iac-code --prompt -
```

Use `--output-format` quando o chamador precisar de saida estruturada:

```bash
iac-code --prompt "Create an OSS Bucket" --output-format json
```

Use `--max-turns` para limitar por quanto tempo o agente pode trabalhar:

```bash
iac-code --prompt "Create a VPC" --max-turns 20
```

Os formatos de saida suportados sao:

| Formato | Finalidade |
|---|---|
| `text` | Saida legivel para humanos. Este e o padrao. |
| `json` | Um unico resultado JSON para chamadores que analisam a resposta final. |
| `stream-json` | Eventos JSON em streaming para chamadores que processam progresso incremental. |

Para todas as flags de inicializacao, consulte [Opcoes de linha de comando](../cli/command-line-options.md).
