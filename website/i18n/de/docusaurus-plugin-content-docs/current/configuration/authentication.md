---
title: Authentifizierung
description: Konfigurieren Sie LLM- und Cloud-Anmeldedaten mit dem Authentifizierungsablauf.
---

# Authentifizierung

Verwenden Sie `/auth` im interaktiven Modus, um sowohl den Zugang zum Modellanbieter als auch den Alibaba Cloud-Zugang zu konfigurieren.

```bash
iac-code
```

```text
/auth
```

Der Authentifizierungsablauf fuehrt Sie durch die Anbieterauswahl, API-Schluessel-Eingabe, Modellauswahl und die Einrichtung der Alibaba Cloud-Anmeldedaten.

Die Laufzeitkonfiguration wird im Benutzerkonfigurationsverzeichnis gespeichert:

```text
~/.iac-code/
```

Wichtige Dateien umfassen:

| Datei | Zweck |
|---|---|
| `.credentials.yml` | LLM-Anbieter-Anmeldedaten |
| `.cloud-credentials.yml` | Alibaba Cloud-Anmeldedaten |
| `settings.yml` | Laufzeiteinstellungen |
