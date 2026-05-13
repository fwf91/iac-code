---
title: Konfiguration
description: Reihenfolge der Laufzeitkonfiguration und lokale Dateien.
---

# Konfiguration

IaC Code liest die Konfiguration aus CLI-Argumenten, Umgebungsvariablen und Dateien im Laufzeitkonfigurationsverzeichnis.

Konfigurationsrangfolge:

```text
CLI-Argumente > Umgebungsvariablen > Konfigurationsdateien
```

Das Laufzeitverzeichnis ist:

```text
~/.iac-code/
```

Gaengige Dateien:

| Datei | Beschreibung |
|---|---|
| `.credentials.yml` | LLM-Anmeldedaten |
| `.cloud-credentials.yml` | Cloud-Anbieter-Anmeldedaten |
| `settings.yml` | Ausgewaehlter Anbieter, Modell und zugehoerige Einstellungen |
| History-Dateien | Eingabeverlauf fuer interaktive Workflows |

Vermeiden Sie es, Dateien aus diesem Verzeichnis zu committen oder zu teilen, da sie Geheimnisse oder lokale Einstellungen enthalten koennen.
