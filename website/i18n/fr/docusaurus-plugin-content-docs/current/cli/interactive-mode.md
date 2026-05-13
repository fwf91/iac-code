---
title: Mode interactif
description: Utiliser le REPL pour un travail itératif sur l'infrastructure.
---

# Mode interactif

Lancez sans arguments pour entrer dans le REPL interactif :

```bash
iac-code
```

Le mode interactif est utile lorsque vous souhaitez affiner les exigences d'infrastructure sur plusieurs échanges.

Commencez par l'authentification :

```text
/auth
```

Puis décrivez ce que vous souhaitez construire :

```text
Create a VPC, two ECS instances, and a security group that allows SSH from my office IP.
```
