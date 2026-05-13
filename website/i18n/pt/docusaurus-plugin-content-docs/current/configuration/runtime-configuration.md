---
title: Configuracao
description: Ordem de configuracao em tempo de execucao e arquivos locais.
---

# Configuracao

O IaC Code le a configuracao a partir de argumentos do CLI, variaveis de ambiente e arquivos no diretorio de configuracao em tempo de execucao.

Precedencia de configuracao:

```text
CLI arguments > environment variables > configuration files
```

O diretorio de execucao e:

```text
~/.iac-code/
```

Arquivos comuns:

| Arquivo | Descricao |
|---|---|
| `.credentials.yml` | Credenciais de LLM |
| `.cloud-credentials.yml` | Credenciais do provedor de nuvem |
| `settings.yml` | Provedor selecionado, modelo e configuracoes relacionadas |
| Arquivos de historico | Historico de entrada para fluxos de trabalho interativos |

Evite fazer commit ou compartilhar arquivos deste diretorio, pois eles podem conter segredos ou preferencias locais.
