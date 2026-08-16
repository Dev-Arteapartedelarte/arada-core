# DOMAIN-003D — Membership Domain Events

Versión: 1.1

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
- DOMAIN-003A-Lifecycle.md
- DOMAIN-003B-State-Machine.md
- DOMAIN-003C-Commands.md
- DOMAIN-003E-Invariants.md
- DOMAIN-003K-Integration-Events.md
- CORE-005-Domain-Events.md

---

# Objetivo

Este documento define los **Domain Events** oficiales del
Aggregate **Membership**.

Un Domain Event representa un hecho de negocio que ya ocurrió y
que modifica el estado del dominio.

Los eventos son inmutables, históricos e internos a Membership
Management. Sólo una decisión futura de Event Sourcing puede convertirlos
en fuente de reconstrucción; no sincronizan directamente otros contextos.

---

# Principios

Todo Domain Event debe cumplir los siguientes principios:

- representar un hecho consumado;
- ser inmutable;
- poseer identidad única;
- contener únicamente información del dominio;
- poder reproducirse cronológicamente;
- preservar el lenguaje ubicuo.

---

# Catálogo Oficial de Domain Events

| Domain Event | Descripción |
|--------------|-------------|
| MembershipCreated | La Membership fue creada |
| MembershipRequested | La Membership fue enviada para evaluación |
| MembershipApproved | La solicitud fue aprobada |
| MembershipRejected | La solicitud fue rechazada |
| MembershipActivated | La Membership quedó activa |
| MembershipSuspended | La Membership fue suspendida |
| MembershipReactivated | La Membership volvió a estar activa |
| MembershipTerminated | La Membership finalizó |
| MembershipArchived | La Membership fue archivada |

---

# Estructura Base

Todo Domain Event deberá contener conceptualmente la siguiente
información:

```text
EventId

AggregateId

AggregateType

AggregateVersion

OccurredOn

CorrelationId

CausationId

ActorId
```

Cada implementación podrá añadir metadatos propios sin alterar
el significado del evento.

---

# MembershipCreated

## Descripción

Indica que una nueva Membership fue creada.

## Generado por

```text
CreateMembership
```

## Estado resultante

```text
Draft
```

---

# MembershipRequested

## Descripción

La Membership fue enviada para aprobación.

## Generado por

```text
RequestMembership
```

## Estado resultante

```text
PendingApproval
```

---

# MembershipApproved

## Descripción

La Organization aprobó la incorporación del Citizen.

## Generado por

```text
ApproveMembership
```

## Estado resultante

```text
Approved
```

---

# MembershipRejected

## Descripción

La solicitud fue rechazada.

## Generado por

```text
RejectMembership
```

## Estado resultante

```text
Rejected
```

---

# MembershipActivated

## Descripción

La Membership comenzó a ejercer plenamente sus derechos.

## Generado por

```text
ActivateMembership
```

## Estado resultante

```text
Active
```

---

# MembershipSuspended

## Descripción

Los derechos de la Membership fueron suspendidos de manera
temporal.

## Generado por

```text
SuspendMembership
```

## Estado resultante

```text
Suspended
```

---

# MembershipReactivated

## Descripción

Una Membership suspendida recuperó sus derechos.

## Generado por

```text
ReactivateMembership
```

## Estado resultante

```text
Active
```

---

# MembershipTerminated

## Descripción

La relación entre el Citizen y la Organization terminó.

## Generado por

```text
TerminateMembership
```

## Estado resultante

```text
Terminated
```

---

# MembershipArchived

## Descripción

La Membership pasó al estado histórico definitivo.

## Generado por

```text
ArchiveMembership
```

## Estado resultante

```text
Archived
```

---

# Orden Cronológico

El historial completo puede representarse de la siguiente forma:

```text
MembershipCreated

↓

MembershipRequested

↓

MembershipApproved

↓

MembershipActivated

↓

MembershipSuspended

↓

MembershipReactivated

↓

MembershipTerminated

↓

MembershipArchived
```

Dependiendo del caso de negocio, algunos eventos pueden no
ocurrir (por ejemplo, una Membership rechazada nunca genera
`MembershipActivated`).

---

# Relación con Commands

| Command | Domain Event |
|----------|--------------|
| CreateMembership | MembershipCreated |
| RequestMembership | MembershipRequested |
| ApproveMembership | MembershipApproved |
| RejectMembership | MembershipRejected |
| ActivateMembership | MembershipActivated |
| SuspendMembership | MembershipSuspended |
| ReactivateMembership | MembershipReactivated |
| TerminateMembership | MembershipTerminated |
| ArchiveMembership | MembershipArchived |

---

# Relación con la Máquina de Estados

Cada transición válida de la State Machine produce exactamente
un Domain Event.

No existen cambios de estado silenciosos.

---

# Consistencia

Los Domain Events:

- se generan dentro de la transacción del Aggregate;
- se almacenan junto al cambio de estado;
- se publican únicamente después del commit mediante el patrón
  **Outbox** o equivalente.

---

# Cruce de Bounded Context

Los Domain Events sólo alimentan handlers y proyecciones internas de
Membership Management. Cuando un hecho deba cruzar el contexto,
Application construye un Integration Event explícito conforme a
DOMAIN-003K; no existe transformación automática ni un contexto Permission.

---

# Compatibilidad con Event Sourcing

En una implementación Event Sourcing:

- los Domain Events constituyen la fuente oficial de verdad;
- el estado del Aggregate se reconstruye aplicando la secuencia
  de eventos;
- los eventos nunca se modifican ni se eliminan.

Las correcciones se realizan generando nuevos eventos.

---

# Compatibilidad con CQRS

Los Read Models se construyen consumiendo estos Domain Events.

Las consultas nunca modifican ni generan eventos.

---

# Versionado

Cada Domain Event incluye la versión del Aggregate en el momento
de su emisión.

Esto permite:

- reconstrucción consistente;
- control de concurrencia;
- evolución del modelo.

---

# Reglas de Evolución

Una vez publicado un Domain Event:

- no cambia su significado;
- no cambia su nombre;
- no se elimina;
- no se reutiliza para otro propósito.

Las nuevas necesidades del dominio se expresan mediante nuevos
Domain Events.

---

# Principios Arquitectónicos

Este modelo sigue:

- Domain-Driven Design (DDD);
- Event-Driven Architecture;
- Event Sourcing;
- CQRS;
- Clean Architecture;
- Immutable Event Pattern.

---

# Definición de Éxito

Los **Domain Events** del Aggregate **Membership** representan
de forma precisa e inmutable todos los hechos relevantes de la
relación entre un **Citizen** y una **Organization**. Constituyen
la base para la trazabilidad interna y, cuando exista un contrato K
explícito, para efectos cross-boundary del
ecosistema AURA mediante una arquitectura orientada a eventos.