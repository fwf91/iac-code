---
title: Modo interativo
description: Use o REPL para trabalho iterativo de infraestrutura.
---

# Modo interativo

Execute sem argumentos para entrar no REPL interativo:

```bash
iac-code
```

O modo interativo e util quando deseja refinar requisitos de infraestrutura ao longo de varias interacoes.

Comece com a autenticacao:

```text
/auth
```

Em seguida, descreva o que deseja construir:

```text
Create a VPC, two ECS instances, and a security group that allows SSH from my office IP.
```
