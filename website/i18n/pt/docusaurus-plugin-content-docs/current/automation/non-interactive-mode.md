---
title: Modo não interativo
description: Executar prompts únicos a partir de argumentos ou stdin.
---

# Modo não interativo

O modo não interativo executa um único prompt e sai. Use quando quiser que o IaC Code produza uma saída para uma tarefa repetível sem permanecer no REPL.

Use `--prompt` para passar o prompt diretamente:

```bash
iac-code --prompt "Create an OSS Bucket"
```

Use `--prompt -` para ler o prompt da entrada padrão:

```bash
echo "Create a VPC and two ECS instances" | iac-code --prompt -
```

Use `--output-format` quando o chamador precisa de saída estruturada:

```bash
iac-code --prompt "Create an OSS Bucket" --output-format json
```

Use `--max-turns` para limitar quanto tempo o agente pode trabalhar:

```bash
iac-code --prompt "Create a VPC" --max-turns 20
```

Os formatos de saída suportados são:

| Formato | Finalidade |
|---|---|
| `text` | Saída legível para humanos. Este é o padrão. |
| `json` | Um único resultado JSON para chamadores que analisam a resposta final. |
| `stream-json` | Eventos JSON em streaming para chamadores que processam progresso incremental. |

## Controle de permissões na automação

Ao executar em modo não interativo, use `--permission-mode` para controlar como o agente lida com aprovações de ferramentas:

```bash
iac-code --prompt "Deploy the stack" --permission-mode bypass_permissions
```

Para restringir o que o agente pode fazer, combine `--allowed-tools` e `--disallowed-tools`:

```bash
iac-code --prompt "Check the stack status" \
  --allowed-tools 'bash(git *),bash(ls:*)' \
  --disallowed-tools 'bash(rm *)' \
  --permission-mode dont_ask
```

Para todos os parâmetros de inicialização, consulte [Opções de linha de comando](../cli/command-line-options.md).
