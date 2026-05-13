---
title: Nicht-interaktiver Modus
description: Einmalige Eingaben ueber Argumente oder stdin ausfuehren.
---

# Nicht-interaktiver Modus

Der nicht-interaktive Modus fuehrt eine einzelne Eingabe aus und beendet sich. Verwenden Sie ihn, wenn IaC Code eine Ausgabe fuer eine wiederholbare Aufgabe erzeugen soll, ohne im REPL zu bleiben.

Verwenden Sie `--prompt`, um die Eingabe direkt zu uebergeben:

```bash
iac-code --prompt "Create an OSS Bucket"
```

Verwenden Sie `--prompt -`, um die Eingabe von der Standardeingabe zu lesen:

```bash
echo "Create a VPC and two ECS instances" | iac-code --prompt -
```

Verwenden Sie `--output-format`, wenn der Aufrufer strukturierte Ausgabe benoetigt:

```bash
iac-code --prompt "Create an OSS Bucket" --output-format json
```

Verwenden Sie `--max-turns`, um die Arbeitsdauer des Agenten zu begrenzen:

```bash
iac-code --prompt "Create a VPC" --max-turns 20
```

Unterstuetzte Ausgabeformate sind:

| Format | Zweck |
|---|---|
| `text` | Menschenlesbare Ausgabe. Dies ist der Standard. |
| `json` | Ein einzelnes JSON-Ergebnis fuer Aufrufer, die die finale Antwort parsen. |
| `stream-json` | Streaming-JSON-Ereignisse fuer Aufrufer, die inkrementellen Fortschritt verarbeiten. |

Fuer alle Startparameter siehe [Kommandozeilenoptionen](../cli/command-line-options.md).
