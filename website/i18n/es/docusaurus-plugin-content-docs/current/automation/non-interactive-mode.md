---
title: Modo no interactivo
description: Ejecutar prompts de un solo uso desde argumentos o stdin.
---

# Modo no interactivo

El modo no interactivo ejecuta un solo prompt y sale. Usalo cuando quieras que IaC Code produzca una salida para una tarea repetible sin permanecer en el REPL.

Usa `--prompt` para pasar el prompt directamente:

```bash
iac-code --prompt "Create an OSS Bucket"
```

Usa `--prompt -` para leer el prompt desde la entrada estandar:

```bash
echo "Create a VPC and two ECS instances" | iac-code --prompt -
```

Usa `--output-format` cuando el proceso llamador necesite una salida estructurada:

```bash
iac-code --prompt "Create an OSS Bucket" --output-format json
```

Usa `--max-turns` para limitar cuanto tiempo puede trabajar el agente:

```bash
iac-code --prompt "Create a VPC" --max-turns 20
```

Los formatos de salida soportados son:

| Formato | Proposito |
|---|---|
| `text` | Salida legible por humanos. Este es el valor predeterminado. |
| `json` | Un unico resultado JSON para los procesos que analizan la respuesta final. |
| `stream-json` | Eventos JSON en streaming para los procesos que procesan el progreso incremental. |

Para todos los indicadores de inicio, consulta [Opciones de linea de comandos](../cli/command-line-options.md).
