---
title: LLM-Anbieter
description: Unterstuetzte Modellanbieter und Umgebungsvariablen.
---

# LLM-Anbieter

IaC Code unterstuetzt mehrere Modellanbieter-Backends.

| Anbieterwert | Zweck |
|---|---|
| `Anthropic` | Anthropic-Modelle |
| `OpenAI` | OpenAI-Modelle |
| `DashScope` | Alibaba Cloud DashScope-kompatibler Endpunkt |
| `DeepSeek` | DeepSeek-Modelle |
| `OpenAPICompatible` | Benutzerdefinierter OpenAI-kompatibler Endpunkt |

Die Anbieterauswahl kann ueber CLI-Optionen, Umgebungsvariablen oder Konfigurationsdateien erfolgen. Die Rangfolge ist:

```text
CLI-Argumente > Umgebungsvariablen > Konfigurationsdateien
```

LLM-Umgebungsvariablen:

| Variable | Beschreibung |
|---|---|
| `IAC_CODE_PROVIDER` | Name des Modellanbieters, Gross-/Kleinschreibung wird nicht beachtet |
| `IAC_CODE_MODEL` | Modellname |
| `IAC_CODE_BASE_URL` | API-Endpunkt fuer `OpenAPICompatible` |
| `IAC_CODE_API_KEY` | API-Schluessel des Anbieters |
