---
title: Identifiants Alibaba Cloud
description: Configurer les identifiants AccessKey ou STS d'Alibaba Cloud.
---

# Identifiants Alibaba Cloud

Les identifiants Alibaba Cloud sont requis pour les opérations qui inspectent ou gèrent des ressources cloud.

Variables d'environnement prises en charge :

| Variable | Description |
|---|---|
| `ALIBABA_CLOUD_ACCESS_KEY_ID` | AccessKey ID |
| `ALIBABA_CLOUD_ACCESS_KEY_SECRET` | AccessKey Secret |
| `ALIBABA_CLOUD_SECURITY_TOKEN` | Jeton STS ; bascule le mode d'identification vers STS lorsqu'il est défini |
| `ALIBABA_CLOUD_REGION_ID` | Région par défaut |

Utilisez des identifiants de test ou temporaires lors de vos expérimentations. Ne collez pas de secrets de production dans l'historique du shell, les captures d'écran, les journaux ou les rapports de problèmes.
