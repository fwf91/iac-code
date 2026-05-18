---
title: Mode non interactif
description: Exécuter des prompts uniques depuis des arguments ou stdin.
---

# Mode non interactif

Le mode non interactif exécute un seul prompt et quitte. Utilisez-le quand vous souhaitez qu'IaC Code produise une sortie pour une tâche répétable sans rester dans le REPL.

Utilisez `--prompt` pour passer le prompt directement :

```bash
iac-code --prompt "Create an OSS Bucket"
```

Utilisez `--prompt -` pour lire le prompt depuis l'entrée standard :

```bash
echo "Create a VPC and two ECS instances" | iac-code --prompt -
```

Utilisez `--output-format` quand l'appelant a besoin d'une sortie structurée :

```bash
iac-code --prompt "Create an OSS Bucket" --output-format json
```

Utilisez `--max-turns` pour limiter la durée de travail de l'agent :

```bash
iac-code --prompt "Create a VPC" --max-turns 20
```

Les formats de sortie pris en charge sont :

| Format | Objectif |
|---|---|
| `text` | Sortie lisible par l'homme. C'est la valeur par défaut. |
| `json` | Un seul résultat JSON pour les appelants qui analysent la réponse finale. |
| `stream-json` | Événements JSON en streaming pour les appelants qui traitent la progression incrémentale. |

## Contrôle des permissions en automatisation

Lors de l'exécution en mode non interactif, utilisez `--permission-mode` pour contrôler comment l'agent gère les approbations d'outils :

```bash
iac-code --prompt "Deploy the stack" --permission-mode bypass_permissions
```

Pour restreindre ce que l'agent peut faire, combinez `--allowed-tools` et `--disallowed-tools` :

```bash
iac-code --prompt "Check the stack status" \
  --allowed-tools 'bash(git *),bash(ls:*)' \
  --disallowed-tools 'bash(rm *)' \
  --permission-mode dont_ask
```

Pour tous les paramètres de démarrage, consultez [Options de ligne de commande](../cli/command-line-options.md).
