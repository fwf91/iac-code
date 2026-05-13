---
title: Configuration
description: Ordre de configuration d'exécution et fichiers locaux.
---

# Configuration

IaC Code lit la configuration depuis les arguments CLI, les variables d'environnement et les fichiers dans le répertoire de configuration d'exécution.

Priorité de la configuration :

```text
CLI arguments > environment variables > configuration files
```

Le répertoire d'exécution est :

```text
~/.iac-code/
```

Fichiers courants :

| Fichier | Description |
|---|---|
| `.credentials.yml` | Identifiants LLM |
| `.cloud-credentials.yml` | Identifiants du fournisseur cloud |
| `settings.yml` | Fournisseur sélectionné, modèle et paramètres associés |
| history files | Historique de saisie pour les flux de travail interactifs |

Évitez de valider ou de partager les fichiers de ce répertoire car ils peuvent contenir des secrets ou des préférences locales.
