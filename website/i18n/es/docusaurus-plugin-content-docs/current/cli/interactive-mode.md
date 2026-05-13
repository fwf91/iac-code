---
title: Modo interactivo
description: Usar el REPL para trabajo iterativo de infraestructura.
---

# Modo interactivo

Ejecuta sin argumentos para entrar al REPL interactivo:

```bash
iac-code
```

El modo interactivo es util cuando quieres refinar los requisitos de infraestructura en multiples turnos.

Comienza con la autenticacion:

```text
/auth
```

Luego describe lo que quieres construir:

```text
Create a VPC, two ECS instances, and a security group that allows SSH from my office IP.
```
