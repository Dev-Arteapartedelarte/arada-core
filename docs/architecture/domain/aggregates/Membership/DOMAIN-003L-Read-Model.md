# DOMAIN-003L — Membership Read Model

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Membership Management

Aggregate:
Membership

Documentos relacionados:

- DOMAIN-003-Aggregate.md
- DOMAIN-003D-Domain-Events.md
- DOMAIN-003G-Repository-Contract.md
- DOMAIN-003J-Consistency-Boundary.md
- DOMAIN-003K-Integration-Events.md
- CORE-013-Application-Services.md
- CORE-015-Package-Architecture.md

---

# Objetivo

Este documento define el **Read Model** oficial del Aggregate
**Membership**.

El Read Model proporciona una representación optimizada para
consultas, separada completamente del modelo de escritura del
Aggregate.

Su propósito es ofrecer lecturas rápidas, agregaciones y
proyecciones del estado de las membresías sin comprometer la
integridad del dominio.

---

# Principios

El Read Model sigue los siguientes principios:

- sólo lectura;
- desacoplado del Aggregate;
- construido a partir de eventos;
- optimizado para consultas;
- eventualmente consistente;
- reconstruible en cualquier momento.

---

# Responsabilidad

El Read Model es responsable de:

- responder consultas;
- facilitar búsquedas;
- generar listados;
- soportar filtros;
- ofrecer proyecciones para interfaces de usuario;
- servir como fuente para reportes operacionales.

No es responsable de:

- validar reglas del dominio;
- ejecutar Commands;
- modificar Memberships;
- generar Domain Events.

---

# Fuente de Datos

El Read Model se alimenta exclusivamente mediante:

```text
MembershipCreated

MembershipRequested

MembershipApproved

MembershipRejected

MembershipActivated

MembershipSuspended

MembershipReactivated

MembershipTerminated

MembershipArchived
```

Cada Domain Event actualiza la proyección correspondiente.

---

# Proyección Conceptual

Cada Membership puede representarse mediante la siguiente
estructura conceptual:

```text
MembershipView

- MembershipId
- CitizenId
- CitizenName
- OrganizationId
- OrganizationName
- MembershipNumber
- Status
- CurrentRole
- AdmissionDate
- ActivationDate
- SuspensionDate
- TerminationDate
- ArchivedDate
- Version
- LastEvent
- LastUpdated
```

Esta estructura es una proyección de lectura y no un Aggregate.

---

# Consultas Principales

## Buscar Membership por Id

```text
find_membership_by_id()
```

---

## Buscar por Citizen

```text
find_memberships_by_citizen()
```

---

## Buscar por Organization

```text
find_memberships_by_organization()
```

---

## Buscar por Estado

```text
find_memberships_by_status()
```

Estados posibles:

```text
Draft

PendingApproval

Approved

Rejected

Active

Suspended

Terminated

Archived
```

---

## Buscar Membresías Activas

```text
find_active_memberships()
```

---

## Buscar Membresías Suspendidas

```text
find_suspended_memberships()
```

---

## Buscar Membresías Terminadas

```text
find_terminated_memberships()
```

---

## Buscar por Período

```text
find_memberships_between_dates()
```

---

## Buscar por Rol Actual

```text
find_memberships_by_role()
```

Esta información puede obtenerse mediante una proyección
compuesta con el Aggregate **Role**.

---

# Consultas de Administración

El Read Model debe soportar consultas como:

```text
Total Members

↓

Active Members

↓

Pending Requests

↓

Rejected Requests

↓

Suspended Members

↓

Archived Members
```

Estas consultas son utilizadas por paneles administrativos.

---

# Consultas para Ciudadanos

Un Citizen puede consultar:

- sus Memberships;
- estado actual;
- historial;
- organización asociada;
- fecha de ingreso;
- estado de solicitudes pendientes.

---

# Consultas para Organizaciones

Una Organization puede consultar:

- miembros activos;
- postulaciones pendientes;
- miembros suspendidos;
- miembros históricos;
- crecimiento de socios;
- distribución por roles.

---

# Proyección para Dashboard

Ejemplo conceptual:

```text
Organization

↓

Members

    Active: 152

    Pending: 7

    Suspended: 2

    Archived: 34
```

---

# Actualización

Cada Domain Event produce una actualización de la proyección.

Ejemplo:

```text
MembershipApproved

↓

Projection Handler

↓

Actualizar Estado

↓

Guardar Read Model
```

---

# Reconstrucción

El Read Model puede reconstruirse completamente mediante:

```text
Replay

↓

Domain Events

↓

Projection

↓

Read Database
```

No depende del estado interno del Aggregate.

---

# Almacenamiento

La implementación puede utilizar:

- PostgreSQL;
- MongoDB;
- Elasticsearch;
- OpenSearch;
- Redis;
- Azure Cosmos DB;
- cualquier motor optimizado para lectura.

El dominio no conoce esta decisión.

---

# Consistencia

El Read Model mantiene:

```text
Eventual Consistency
```

Puede existir un pequeño retraso respecto al Aggregate.

La consistencia inmediata pertenece exclusivamente al modelo
de escritura.

---

# Integración con CQRS

```text
Commands

↓

Aggregate

↓

Domain Events

↓

Projection

↓

Read Model

↓

Queries
```

Los Queries nunca interactúan directamente con el Aggregate.

---

# Integración con Event Sourcing

Cuando Event Sourcing está habilitado:

```text
Replay Events

↓

Projection Handlers

↓

Read Model
```

La pérdida de una proyección nunca implica pérdida de datos.

---

# Indexación

Se recomienda indexar:

```text
MembershipId

CitizenId

OrganizationId

Status

AdmissionDate

ActivationDate

TerminationDate
```

Con el fin de optimizar consultas frecuentes.

---

# Rendimiento

Objetivos recomendados:

- consultas por Id < 50 ms;
- búsquedas filtradas < 150 ms;
- dashboards < 500 ms;
- reconstrucción incremental mediante eventos.

---

# Seguridad

El Read Model no almacena:

- credenciales;
- secretos;
- tokens;
- datos de autenticación.

Las consultas deben respetar las políticas de autorización
definidas por el sistema.

---

# Evolución

Las nuevas proyecciones deben:

- ser independientes;
- no modificar el Aggregate;
- poder reconstruirse;
- mantenerse compatibles con eventos existentes.

---

# Principios Arquitectónicos

Este modelo sigue:

- Domain-Driven Design (DDD);
- CQRS;
- Event Sourcing;
- Projection Pattern;
- Read Model Pattern;
- Clean Architecture.

---

# Definición de Éxito

El **Read Model** del Aggregate **Membership** proporciona una
representación optimizada, reconstruible y desacoplada del
modelo de escritura para consultar la relación entre
**Citizens** y **Organizations**. Su diseño garantiza consultas
eficientes, consistencia eventual y una integración natural con
arquitecturas basadas en **CQRS**, **Event Sourcing** y
**Event-Driven Architecture**, manteniendo intacta la
consistencia del dominio AURA.