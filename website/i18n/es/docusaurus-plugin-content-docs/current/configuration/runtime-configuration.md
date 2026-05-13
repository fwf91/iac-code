---
title: Configuracion
description: Orden de configuracion en tiempo de ejecucion y archivos locales.
---

# Configuracion

IaC Code lee la configuracion desde los argumentos del CLI, las variables de entorno y los archivos en el directorio de configuracion en tiempo de ejecucion.

Precedencia de configuracion:

```text
CLI arguments > environment variables > configuration files
```

El directorio de tiempo de ejecucion es:

```text
~/.iac-code/
```

Archivos comunes:

| Archivo | Descripcion |
|---|---|
| `.credentials.yml` | Credenciales de LLM |
| `.cloud-credentials.yml` | Credenciales del proveedor de nube |
| `settings.yml` | Proveedor seleccionado, modelo y configuraciones relacionadas |
| archivos de historial | Historial de entrada para flujos de trabajo interactivos |

Evita hacer commit o compartir archivos de este directorio porque pueden contener secretos o preferencias locales.
