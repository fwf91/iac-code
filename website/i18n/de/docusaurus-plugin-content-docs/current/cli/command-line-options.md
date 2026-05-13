---
title: Kommandozeilenoptionen
description: Referenz fuer IaC Code-Startoptionen und Einmal-Ausfuehrungsparameter.
---

# Kommandozeilenoptionen

Kommandozeilenoptionen aendern das Startverhalten von IaC Code. Verwenden Sie sie vor dem Starten des interaktiven REPL oder kombinieren Sie sie mit `--prompt` fuer einmalige Automatisierung.

| Option | Zweck |
|---|---|
| `-h`, `--help` | CLI-Hilfe anzeigen und beenden. Verwenden Sie dies, um die von Ihrer installierten Version unterstuetzten Optionen anzuzeigen. |
| `-v`, `-V`, `--version` | Die installierte IaC Code-Version ausgeben und beenden. |
| `-m <model>`, `--model <model>` | Mit einem bestimmten LLM-Modell starten. Dies ueberschreibt das gespeicherte Modell fuer den aktuellen Lauf. |
| `-p <prompt>`, `--prompt <prompt>` | Eine einzelne Eingabe ausfuehren und beenden. Dies aktiviert den nicht-interaktiven Modus. Verwenden Sie `--prompt -`, um die Eingabe von der Standardeingabe zu lesen. |
| `--output-format <format>` | Ausgabeformat fuer den nicht-interaktiven Modus festlegen. Unterstuetzte Werte sind `text`, `json` und `stream-json`. Standard ist `text`. |
| `--max-turns <number>` | Maximale Anzahl der Agenten-Durchgaenge im nicht-interaktiven Modus begrenzen. Standard ist `100`. |
| `-d`, `--debug` | Debug-Protokollierung fuer den aktuellen Lauf aktivieren. Im interaktiven Modus verwenden Sie `/debug`, um die Debug-Protokollierung nach dem Start zu pruefen oder zu aendern. |
| `-r <session-id>`, `--resume <session-id>` | Eine fruehere Sitzung anhand der ID fortsetzen. Dies dient zum Zurueckkehren zu einer bekannten Konversation. |
| `-c`, `--continue` | Die neueste Sitzung fortsetzen. Kann nicht zusammen mit `--resume` verwendet werden. |

## Haeufige Startbefehle

Das interaktive REPL mit dem gespeicherten Modell starten:

```bash
iac-code
```

Mit einem bestimmten Modell fuer diesen Lauf starten:

```bash
iac-code --model qwen3.6-plus
```

Eine einmalige Eingabe ausfuehren:

```bash
iac-code --prompt "Create an OSS Bucket"
```

Die Eingabe von der Standardeingabe lesen:

```bash
echo "Create a VPC and two ECS instances" | iac-code --prompt -
```

Die neueste Sitzung fortsetzen:

```bash
iac-code --continue
```
