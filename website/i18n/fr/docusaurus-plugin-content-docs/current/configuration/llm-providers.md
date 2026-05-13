---
title: Fournisseurs LLM
description: Fournisseurs de modèles pris en charge et variables d'environnement.
---

# Fournisseurs LLM

IaC Code prend en charge plusieurs backends de fournisseurs de modèles.

| Valeur du fournisseur | Fonction |
|---|---|
| `Anthropic` | Modèles Anthropic |
| `OpenAI` | Modèles OpenAI |
| `DashScope` | Point de terminaison compatible Alibaba Cloud DashScope |
| `DeepSeek` | Modèles DeepSeek |
| `OpenAPICompatible` | Point de terminaison personnalisé compatible OpenAI |

La sélection du fournisseur peut provenir des options CLI, des variables d'environnement ou des fichiers de configuration. L'ordre de priorité est :

```text
CLI arguments > environment variables > configuration files
```

Variables d'environnement LLM :

| Variable | Description |
|---|---|
| `IAC_CODE_PROVIDER` | Nom du fournisseur de modèles, insensible à la casse |
| `IAC_CODE_MODEL` | Nom du modèle |
| `IAC_CODE_BASE_URL` | Point de terminaison API pour `OpenAPICompatible` |
| `IAC_CODE_API_KEY` | Clé API du fournisseur |
