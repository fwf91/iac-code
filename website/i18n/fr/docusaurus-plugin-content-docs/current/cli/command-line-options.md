---
title: Options de ligne de commande
description: Référence des options de démarrage et des indicateurs d'exécution ponctuelle d'IaC Code.
---

# Options de ligne de commande

Les options de ligne de commande modifient le démarrage d'IaC Code. Utilisez-les avant d'entrer dans le REPL interactif, ou combinez-les avec `--prompt` pour une automatisation ponctuelle.

| Option | Fonction |
|---|---|
| `-h`, `--help` | Afficher l'aide CLI et quitter. Utilisez cette option pour inspecter les options prises en charge par votre version installée. |
| `-v`, `-V`, `--version` | Afficher la version installée d'IaC Code et quitter. |
| `-m <model>`, `--model <model>` | Démarrer avec un modèle LLM spécifique. Cela remplace le modèle enregistré pour l'exécution en cours. |
| `-p <prompt>`, `--prompt <prompt>` | Exécuter une seule requête et quitter. Cela active le mode non interactif. Utilisez `--prompt -` pour lire la requête depuis l'entrée standard. |
| `--output-format <format>` | Définir le format de sortie pour le mode non interactif. Les valeurs prises en charge sont `text`, `json` et `stream-json`. La valeur par défaut est `text`. |
| `--max-turns <number>` | Limiter le nombre maximum de tours de l'agent en mode non interactif. La valeur par défaut est `100`. |
| `-d`, `--debug` | Activer la journalisation de débogage pour l'exécution en cours. En mode interactif, utilisez `/debug` pour inspecter ou modifier la journalisation de débogage après le démarrage. |
| `-r <session-id>`, `--resume <session-id>` | Reprendre une session précédente par son identifiant. Cela permet de revenir à une conversation connue. |
| `-c`, `--continue` | Reprendre la session la plus récente. Cette option ne peut pas être utilisée conjointement avec `--resume`. |

## Commandes de démarrage courantes

Démarrer le REPL interactif avec le modèle enregistré :

```bash
iac-code
```

Démarrer avec un modèle spécifique pour cette exécution :

```bash
iac-code --model qwen3.6-plus
```

Exécuter une requête ponctuelle :

```bash
iac-code --prompt "Create an OSS Bucket"
```

Lire la requête depuis l'entrée standard :

```bash
echo "Create a VPC and two ECS instances" | iac-code --prompt -
```

Reprendre la dernière session :

```bash
iac-code --continue
```
