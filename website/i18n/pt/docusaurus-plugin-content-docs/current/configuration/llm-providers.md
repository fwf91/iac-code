---
title: Provedores de LLM
description: Provedores de modelos suportados e variaveis de ambiente.
---

# Provedores de LLM

O IaC Code suporta multiplos backends de provedores de modelos.

| Valor do provedor | Finalidade |
|---|---|
| `Anthropic` | Modelos Anthropic |
| `OpenAI` | Modelos OpenAI |
| `DashScope` | Endpoint compativel com DashScope da Alibaba Cloud |
| `DeepSeek` | Modelos DeepSeek |
| `OpenAPICompatible` | Endpoint personalizado compativel com OpenAI |

A selecao do provedor pode vir de opcoes do CLI, variaveis de ambiente ou arquivos de configuracao. A precedencia e:

```text
CLI arguments > environment variables > configuration files
```

Variaveis de ambiente de LLM:

| Variavel | Descricao |
|---|---|
| `IAC_CODE_PROVIDER` | Nome do provedor de modelo, insensivel a maiusculas e minusculas |
| `IAC_CODE_MODEL` | Nome do modelo |
| `IAC_CODE_BASE_URL` | Endpoint de API para `OpenAPICompatible` |
| `IAC_CODE_API_KEY` | Chave de API do provedor |
