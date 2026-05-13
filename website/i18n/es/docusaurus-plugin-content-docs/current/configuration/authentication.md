---
title: Autenticacion
description: Configurar credenciales de LLM y de la nube con el flujo de autenticacion.
---

# Autenticacion

Usa `/auth` en modo interactivo para configurar tanto el acceso al proveedor de modelos como el acceso a Alibaba Cloud.

```bash
iac-code
```

```text
/auth
```

El flujo de autenticacion te guia a traves de la seleccion de proveedor, la entrada de clave API, la seleccion de modelo y la configuracion de credenciales de Alibaba Cloud.

La configuracion en tiempo de ejecucion se almacena en el directorio de configuracion del usuario:

```text
~/.iac-code/
```

Los archivos importantes incluyen:

| Archivo | Proposito |
|---|---|
| `.credentials.yml` | Credenciales del proveedor de LLM |
| `.cloud-credentials.yml` | Credenciales de Alibaba Cloud |
| `settings.yml` | Configuracion en tiempo de ejecucion |
