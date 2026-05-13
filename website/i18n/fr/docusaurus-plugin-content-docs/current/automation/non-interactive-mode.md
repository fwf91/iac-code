---
title: Mode non interactif
description: Exécuter des requêtes ponctuelles depuis les arguments ou stdin.
---

# Mode non interactif

Le mode non interactif exécute une seule requête puis se termine. Utilisez-le lorsque vous souhaitez qu'IaC Code produise une sortie pour une tâche reproductible sans rester dans le REPL.

Utilisez `--prompt` pour passer la requête directement :

```bash
iac-code --prompt "Create an OSS Bucket"
```

Utilisez `--prompt -` pour lire la requête depuis l'entrée standard :

```bash
echo "Create a VPC and two ECS instances" | iac-code --prompt -
```

Utilisez `--output-format` lorsque l'appelant a besoin d'une sortie structurée :

```bash
iac-code --prompt "Create an OSS Bucket" --output-format json
```

Utilisez `--max-turns` pour limiter la durée de travail de l'agent :

```bash
iac-code --prompt "Create a VPC" --max-turns 20
```

Les formats de sortie pris en charge sont :

| Format | Fonction |
|---|---|
| `text` | Sortie lisible par l'homme. C'est le format par défaut. |
| `json` | Un seul résultat JSON pour les appelants qui analysent la réponse finale. |
| `stream-json` | Événements JSON en streaming pour les appelants qui traitent la progression incrémentale. |

Pour tous les indicateurs de démarrage, consultez les [Options de ligne de commande](../cli/command-line-options.md).
