---
title: Credenciais da Alibaba Cloud
description: Configure credenciais AccessKey ou STS da Alibaba Cloud.
---

# Credenciais da Alibaba Cloud

As credenciais da Alibaba Cloud sao necessarias para operacoes que inspecionam ou gerenciam recursos na nuvem.

Variaveis de ambiente suportadas:

| Variavel | Descricao |
|---|---|
| `ALIBABA_CLOUD_ACCESS_KEY_ID` | AccessKey ID |
| `ALIBABA_CLOUD_ACCESS_KEY_SECRET` | AccessKey Secret |
| `ALIBABA_CLOUD_SECURITY_TOKEN` | Token STS; muda o modo de credencial para STS quando definido |
| `ALIBABA_CLOUD_REGION_ID` | Regiao padrao |

Use credenciais de teste ou temporarias ao experimentar. Nao cole segredos de producao no historico do shell, capturas de tela, logs ou relatorios de problemas.
