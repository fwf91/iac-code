---
title: Opciones de linea de comandos
description: Referencia de las opciones de inicio de IaC Code y los indicadores de ejecucion de un solo uso.
---

# Opciones de linea de comandos

Las opciones de linea de comandos cambian como se inicia IaC Code. Usalas antes de entrar al REPL interactivo, o combinalas con `--prompt` para automatizacion de un solo uso.

| Opcion | Proposito |
|---|---|
| `-h`, `--help` | Muestra la ayuda del CLI y sale. Usalo para inspeccionar las opciones soportadas por tu version instalada. |
| `-v`, `-V`, `--version` | Imprime la version instalada de IaC Code y sale. |
| `-m <model>`, `--model <model>` | Inicia con un modelo LLM especifico. Esto sobreescribe el modelo guardado para la ejecucion actual. |
| `-p <prompt>`, `--prompt <prompt>` | Ejecuta un solo prompt y sale. Esto habilita el modo no interactivo. Usa `--prompt -` para leer el prompt desde la entrada estandar. |
| `--output-format <format>` | Establece el formato de salida para el modo no interactivo. Los valores soportados son `text`, `json` y `stream-json`. El valor predeterminado es `text`. |
| `--max-turns <number>` | Limita el numero maximo de turnos del agente en modo no interactivo. El valor predeterminado es `100`. |
| `-d`, `--debug` | Habilita el registro de depuracion para la ejecucion actual. En modo interactivo, usa `/debug` para inspeccionar o cambiar el registro de depuracion despues del inicio. |
| `-r <session-id>`, `--resume <session-id>` | Reanuda una sesion anterior por ID. Esto es para volver a una conversacion conocida. |
| `-c`, `--continue` | Reanuda la sesion mas reciente. No se puede usar junto con `--resume`. |

## Comandos de inicio comunes

Iniciar el REPL interactivo con el modelo guardado:

```bash
iac-code
```

Iniciar con un modelo especifico para esta ejecucion:

```bash
iac-code --model qwen3.6-plus
```

Ejecutar un prompt de un solo uso:

```bash
iac-code --prompt "Create an OSS Bucket"
```

Leer el prompt desde la entrada estandar:

```bash
echo "Create a VPC and two ECS instances" | iac-code --prompt -
```

Reanudar la ultima sesion:

```bash
iac-code --continue
```
