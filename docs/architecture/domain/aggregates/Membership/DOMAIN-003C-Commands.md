# DOMAIN-003C — Membership Commands

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
- DOMAIN-003A-Lifecycle.md
- DOMAIN-003B-State-Machine.md
- DOMAIN-003D-Domain-Events.md
- DOMAIN-003E-Invariants.md
- DOMAIN-003F-Permissions.md

---

# Objetivo

Este documento define los Commands oficiales del Aggregate
**Membership**.

Un Command representa la intención explícita de modificar el
estado de una Membership. Todo Command expresa una acción del
negocio, nunca una operación técnica.

Los Commands son procesados por la capa de aplicación y
ejecutados exclusivamente por el Aggregate Root.

---

# Principios

Todo Command debe:

- representar una intención de negocio;
- modificar un único Aggregate;
- ejecutarse dentro de una única transacción;
- respetar las invariantes;
- generar Domain Events cuando corresponda;
- incrementar la versión del Aggregate tras una ejecución
  exitosa.

---

# Catálogo Oficial de Commands

| Command | Propósito |
|----------|-----------|
| CreateMembership | Crear una nueva Membership |
| RequestMembership | Solicitar formalmente el ingreso |
| ApproveMembership | Aprobar la solicitud |
| RejectMembership | Rechazar la solicitud |
| ActivateMembership | Activar la Membership |
| SuspendMembership | Suspender temporalmente la Membership |
| ReactivateMembership | Reactivar una Membership suspendida |
| TerminateMembership | Finalizar la Membership |
| ArchiveMembership | Archivar definitivamente la Membership |

---

# CreateMembership

## Objetivo

Crear una nueva Membership en estado inicial.

## Estado requerido

No existe previamente una Membership con el mismo
**MembershipId**.

## Estado resultante

```text
Draft
```

## Domain Event

```text
MembershipCreated
```

---

# RequestMembership

## Objetivo

Enviar la Membership para evaluación.

## Estado requerido

```text
Draft
```

## Estado resultante

```text
PendingApproval
```

## Domain Event

```text
MembershipRequested
```

---

# ApproveMembership

## Objetivo

Aceptar la solicitud de incorporación.

## Estado requerido

```text
PendingApproval
```

## Estado resultante

```text
Approved
```

## Domain Event

```text
MembershipApproved
```

---

# RejectMembership

## Objetivo

Rechazar la solicitud de incorporación.

## Estado requerido

```text
PendingApproval
```

## Estado resultante

```text
Rejected
```

## Domain Event

```text
MembershipRejected
```

---

# ActivateMembership

## Objetivo

Habilitar la Membership para participar plenamente en la
organización.

## Estado requerido

```text
Approved
```

## Estado resultante

```text
Active
```

## Domain Event

```text
MembershipActivated
```

---

# SuspendMembership

## Objetivo

Suspender temporalmente los derechos asociados a la Membership.

## Estado requerido

```text
Active
```

## Estado resultante

```text
Suspended
```

## Domain Event

```text
MembershipSuspended
```

---

# ReactivateMembership

## Objetivo

Restablecer una Membership suspendida.

## Estado requerido

```text
Suspended
```

## Estado resultante

```text
Active
```

## Domain Event

```text
MembershipReactivated
```

---

# TerminateMembership

## Objetivo

Finalizar definitivamente la relación entre el Citizen y la
Organization.

## Estado requerido

Puede ejecutarse desde:

```text
Active
```

o

```text
Suspended
```

## Estado resultante

```text
Terminated
```

## Domain Event

```text
MembershipTerminated
```

---

# ArchiveMembership

## Objetivo

Mover la Membership a estado histórico e inmutable.

## Estados permitidos

```text
Draft

Rejected

Terminated
```

## Estado resultante

```text
Archived
```

## Domain Event

```text
MembershipArchived
```

---

# Validaciones Previas

Antes de ejecutar cualquier Command deben verificarse:

- existencia del Aggregate cuando corresponda;
- estado actual válido;
- permisos del actor;
- invariantes del dominio;
- versión del Aggregate;
- consistencia de los datos de entrada.

Si alguna validación falla, el Command debe rechazarse sin
modificar el estado.

---

# Reglas de Ejecución

Todo Command exitoso debe:

1. validar las precondiciones;
2. aplicar las reglas del dominio;
3. modificar el estado del Aggregate;
4. incrementar la versión;
5. registrar los Domain Events generados;
6. finalizar la transacción.

---

# Reglas de Idempotencia

Los Commands deben diseñarse para evitar efectos duplicados
cuando una misma solicitud sea recibida más de una vez.

La estrategia de idempotencia será implementada en la capa de
aplicación y/o infraestructura, sin alterar el comportamiento
del Aggregate.

---

# Reglas de Concurrencia

La ejecución utiliza:

```text
Optimistic Concurrency Control
```

Si la versión recibida no coincide con la versión persistida,
el Command debe rechazarse mediante un conflicto de
concurrencia.

---

# Relación con Domain Events

Todo Command exitoso genera uno o más Domain Events.

La relación oficial es:

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

# Compatibilidad con CQRS

Los Commands pertenecen exclusivamente al lado de escritura.

No realizan consultas complejas ni devuelven proyecciones.

Las consultas deben resolverse mediante Read Models.

---

# Compatibilidad con Event Sourcing

En implementaciones basadas en Event Sourcing, el estado del
Aggregate se reconstruye aplicando los Domain Events
producidos por estos Commands.

Los Commands nunca modifican directamente el historial.

---

# Principios Arquitectónicos

Este catálogo sigue los principios de:

- Domain-Driven Design (DDD);
- Command Pattern;
- CQRS;
- Event Sourcing;
- Clean Architecture;
- Command Query Separation (CQS).

---

# Definición de Éxito

Los Commands del Aggregate **Membership** representan todas las
acciones de negocio necesarias para gestionar la pertenencia de
un **Citizen** a una **Organization**. Cada Command expresa una
intención clara, respeta las invariantes del dominio y produce
los eventos necesarios para mantener la consistencia,
trazabilidad y evolución del ecosistema AURA.