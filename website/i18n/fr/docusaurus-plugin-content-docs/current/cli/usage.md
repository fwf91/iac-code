---
title: Aperçu CLI
description: Démarrer IaC Code depuis le terminal et choisir le bon flux de travail.
---

# Aperçu CLI

Exécutez `iac-code` depuis le terminal :

```bash
iac-code
```

Le CLI prend en charge deux flux de travail :

| Flux de travail | Quand l'utiliser |
|---|---|
| [Mode interactif](./interactive-mode.md) | Vous souhaitez affiner les exigences d'infrastructure sur plusieurs échanges dans un REPL. |
| [Mode non interactif](../automation/non-interactive-mode.md) | Vous souhaitez exécuter une seule requête et renvoyer la sortie à un appelant. |

Commandes de démarrage courantes :

```bash
iac-code
iac-code --prompt "Create an OSS Bucket"
echo "Create a VPC" | iac-code --prompt -
iac-code --debug
```

Utilisez les [Options de ligne de commande](./command-line-options.md) pour les indicateurs de démarrage et les [Commandes slash](./commands.md) pour les commandes disponibles dans une session interactive.
