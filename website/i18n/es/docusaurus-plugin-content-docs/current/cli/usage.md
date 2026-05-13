---
title: Vision general del CLI
description: Iniciar IaC Code desde la terminal y elegir el flujo de trabajo adecuado.
---

# Vision general del CLI

Ejecuta `iac-code` desde la terminal:

```bash
iac-code
```

El CLI admite dos flujos de trabajo:

| Flujo de trabajo | Cuando usarlo |
|---|---|
| [Modo interactivo](./interactive-mode.md) | Quieres refinar los requisitos de infraestructura en multiples turnos en un REPL. |
| [Modo no interactivo](../automation/non-interactive-mode.md) | Quieres ejecutar un solo prompt y devolver la salida a un proceso llamador. |

Comandos de inicio comunes:

```bash
iac-code
iac-code --prompt "Create an OSS Bucket"
echo "Create a VPC" | iac-code --prompt -
iac-code --debug
```

Usa [Opciones de linea de comandos](./command-line-options.md) para los indicadores de inicio y [Comandos slash](./commands.md) para los comandos disponibles dentro de una sesion interactiva.
