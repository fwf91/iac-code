---
title: Visao geral do CLI
description: Inicie o IaC Code a partir do terminal e escolha o fluxo de trabalho adequado.
---

# Visao geral do CLI

Execute `iac-code` a partir do terminal:

```bash
iac-code
```

O CLI suporta dois fluxos de trabalho:

| Fluxo de trabalho | Quando usar |
|---|---|
| [Modo interativo](./interactive-mode.md) | Quando deseja refinar requisitos de infraestrutura ao longo de varias interacoes num REPL. |
| [Modo nao interativo](../automation/non-interactive-mode.md) | Quando deseja executar um unico prompt e retornar a saida para um chamador. |

Comandos de inicializacao comuns:

```bash
iac-code
iac-code --prompt "Create an OSS Bucket"
echo "Create a VPC" | iac-code --prompt -
iac-code --debug
```

Use [Opcoes de linha de comando](./command-line-options.md) para flags de inicializacao e [Comandos slash](./commands.md) para comandos disponiveis dentro de uma sessao interativa.
