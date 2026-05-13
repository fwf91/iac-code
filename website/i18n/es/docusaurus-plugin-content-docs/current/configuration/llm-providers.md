---
title: Proveedores de LLM
description: Proveedores de modelos soportados y variables de entorno.
---

# Proveedores de LLM

IaC Code admite multiples backends de proveedores de modelos.

| Valor del proveedor | Proposito |
|---|---|
| `Anthropic` | Modelos de Anthropic |
| `OpenAI` | Modelos de OpenAI |
| `DashScope` | Endpoint compatible con DashScope de Alibaba Cloud |
| `DeepSeek` | Modelos de DeepSeek |
| `OpenAPICompatible` | Endpoint personalizado compatible con OpenAI |

La seleccion del proveedor puede provenir de las opciones del CLI, variables de entorno o archivos de configuracion. La precedencia es:

```text
CLI arguments > environment variables > configuration files
```

Variables de entorno de LLM:

| Variable | Descripcion |
|---|---|
| `IAC_CODE_PROVIDER` | Nombre del proveedor de modelos, sin distincion de mayusculas/minusculas |
| `IAC_CODE_MODEL` | Nombre del modelo |
| `IAC_CODE_BASE_URL` | Endpoint de API para `OpenAPICompatible` |
| `IAC_CODE_API_KEY` | Clave API del proveedor |
