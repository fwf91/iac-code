---
title: Alibaba Cloud-Anmeldedaten
description: Konfigurieren Sie Alibaba Cloud AccessKey- oder STS-Anmeldedaten.
---

# Alibaba Cloud-Anmeldedaten

Alibaba Cloud-Anmeldedaten werden fuer Operationen benoetigt, die Cloud-Ressourcen ueberpruefen oder verwalten.

Unterstuetzte Umgebungsvariablen:

| Variable | Beschreibung |
|---|---|
| `ALIBABA_CLOUD_ACCESS_KEY_ID` | AccessKey-ID |
| `ALIBABA_CLOUD_ACCESS_KEY_SECRET` | AccessKey-Secret |
| `ALIBABA_CLOUD_SECURITY_TOKEN` | STS-Token; wechselt den Anmeldedatenmodus zu STS, wenn gesetzt |
| `ALIBABA_CLOUD_REGION_ID` | Standardregion |

Verwenden Sie Test- oder temporaere Anmeldedaten beim Experimentieren. Fuegen Sie keine Produktionsgeheimnisse in Shell-Verlaeufe, Screenshots, Protokolle oder Fehlerberichte ein.
