---
title: Credenciales de Alibaba Cloud
description: Configurar credenciales de AccessKey o STS de Alibaba Cloud.
---

# Credenciales de Alibaba Cloud

Las credenciales de Alibaba Cloud son necesarias para las operaciones que inspeccionan o gestionan recursos en la nube.

Variables de entorno soportadas:

| Variable | Descripcion |
|---|---|
| `ALIBABA_CLOUD_ACCESS_KEY_ID` | AccessKey ID |
| `ALIBABA_CLOUD_ACCESS_KEY_SECRET` | AccessKey Secret |
| `ALIBABA_CLOUD_SECURITY_TOKEN` | Token STS; cambia el modo de credenciales a STS cuando se establece |
| `ALIBABA_CLOUD_REGION_ID` | Region predeterminada |

Usa credenciales de prueba o temporales cuando experimentes. No pegues secretos de produccion en el historial del shell, capturas de pantalla, registros o reportes de problemas.
