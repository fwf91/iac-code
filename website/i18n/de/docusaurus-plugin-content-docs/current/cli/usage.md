---
title: CLI-Uebersicht
description: Starten Sie IaC Code vom Terminal und waehlen Sie den richtigen Workflow.
---

# CLI-Uebersicht

Fuehren Sie `iac-code` vom Terminal aus:

```bash
iac-code
```

Die CLI unterstuetzt zwei Workflows:

| Workflow | Verwendung |
|---|---|
| [Interaktiver Modus](./interactive-mode.md) | Wenn Sie Infrastrukturanforderungen ueber mehrere Durchgaenge in einem REPL verfeinern moechten. |
| [Nicht-interaktiver Modus](../automation/non-interactive-mode.md) | Wenn Sie eine einzelne Eingabe ausfuehren und die Ausgabe an einen Aufrufer zurueckgeben moechten. |

Haeufige Startbefehle:

```bash
iac-code
iac-code --prompt "Create an OSS Bucket"
echo "Create a VPC" | iac-code --prompt -
iac-code --debug
```

Verwenden Sie [Kommandozeilenoptionen](./command-line-options.md) fuer Startparameter und [Slash-Befehle](./commands.md) fuer Befehle, die innerhalb einer interaktiven Sitzung verfuegbar sind.
