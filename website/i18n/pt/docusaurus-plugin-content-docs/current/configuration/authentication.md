---
title: Autenticacao
description: Configure as credenciais de LLM e nuvem com o fluxo de autenticacao.
---

# Autenticacao

Use `/auth` no modo interativo para configurar tanto o acesso ao provedor de modelos quanto o acesso a Alibaba Cloud.

```bash
iac-code
```

```text
/auth
```

O fluxo de autenticacao guia-o pela selecao do provedor, entrada da chave de API, selecao do modelo e configuracao das credenciais da Alibaba Cloud.

A configuracao em tempo de execucao e armazenada no diretorio de configuracao do utilizador:

```text
~/.iac-code/
```

Os arquivos importantes incluem:

| Arquivo | Finalidade |
|---|---|
| `.credentials.yml` | Credenciais do provedor de LLM |
| `.cloud-credentials.yml` | Credenciais da Alibaba Cloud |
| `settings.yml` | Configuracoes em tempo de execucao |
