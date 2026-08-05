# DOMAIN-002B — Citizen State Machine

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Citizen Management

Aggregate:
Citizen

Documentos relacionados:

- DOMAIN-002-Aggregate.md
- DOMAIN-002A-Lifecycle.md
- DOMAIN-002C-Commands.md
- DOMAIN-002D-Domain-Events.md
- DOMAIN-002E-Invariants.md

---

# Objetivo

Este documento define la Máquina de Estados oficial del
Aggregate **Citizen**.

La State Machine establece las transiciones válidas entre los
distintos estados del ciudadano dentro del ecosistema AURA.

Toda modificación del Aggregate debe respetar este modelo.

---

# Principios

La máquina de estados garantiza:

- consistencia del Aggregate;
- transiciones explícitas;
- trazabilidad completa;
- ausencia de estados ambiguos;
- compatibilidad con Event Sourcing;
- compatibilidad con CQRS.

---

# Estados Oficiales

El Aggregate Citizen reconoce exclusivamente los siguientes
estados:

```text
Draft

PendingVerification

Verified

Active

Suspended

Inactive

Archived
```

No existen estados adicionales.

---

# Estado Inicial

Todo Citizen comienza en:

```text
Draft
```

---

# Estado Final

El estado terminal es:

```text
Archived
```

Un Aggregate archivado no participa nuevamente del dominio
mediante transiciones normales.

---

# Diagrama de Estados

```text
                   +----------------------+
                   |        Draft         |
                   +----------+-----------+
                              |
                              v
               +-------------------------------+
               | PendingVerification           |
               +---------------+---------------+
                               |
                               v
                     +------------------+
                     |     Verified     |
                     +--------+---------+
                              |
                              v
                     +------------------+
                     |      Active      |
                     +---+----------+---+
                         |          |
             Suspend     |          | Deactivate
                         |          |
                         v          v
                  +-------------+ +-------------+
                  | Suspended   | | Inactive    |
                  +------+------+ +------+------+
                         |                |
            Reactivate   |                |
                         v                |
                     +------------------+ |
                     |      Active      | |
                     +------------------+ |
                                          |
                                          v
                                 +------------------+
                                 |    Archived      |
                                 +------------------+
```

---

# Transiciones Permitidas

## Draft

Puede transicionar a:

- PendingVerification

No puede:

- Active
- Suspended
- Archived

---

## PendingVerification

Puede transicionar a:

- Verified
- Archived

No puede:

- Active
- Suspended

---

## Verified

Puede transicionar a:

- Active
- Archived

No puede:

- Suspended
- Inactive

---

## Active

Puede transicionar a:

- Suspended
- Inactive
- Archived

---

## Suspended

Puede transicionar a:

- Active
- Archived

No puede:

- Draft
- PendingVerification

---

## Inactive

Puede transicionar a:

- Archived

Opcionalmente, una política de negocio podría permitir el
retorno a **Active** mediante un proceso formal de
reactivación. Esa decisión pertenece a las reglas del dominio
y no a la máquina de estados base.

---

## Archived

No posee transiciones salientes.

Es un estado terminal.

---

# Tabla de Transiciones

| Estado Actual | Estado Destino | Permitida |
|---------------|----------------|-----------|
| Draft | PendingVerification | Sí |
| PendingVerification | Verified | Sí |
| PendingVerification | Archived | Sí |
| Verified | Active | Sí |
| Verified | Archived | Sí |
| Active | Suspended | Sí |
| Active | Inactive | Sí |
| Active | Archived | Sí |
| Suspended | Active | Sí |
| Suspended | Archived | Sí |
| Inactive | Archived | Sí |

Toda transición no incluida en esta tabla se considera
inválida.

---

# Reglas de Validación

Antes de ejecutar una transición se debe verificar:

- cumplimiento de invariantes;
- autorización correspondiente;
- consistencia del Aggregate;
- versión vigente;
- integridad de los Value Objects.

Si alguna validación falla, la transición debe rechazarse.

---

# Eventos Asociados

Cada transición válida genera al menos un Domain Event.

Ejemplos:

```text
Draft
    └── CitizenDraftCreated

PendingVerification
    └── CitizenVerificationRequested

Verified
    └── CitizenVerified

Active
    └── CitizenActivated

Suspended
    └── CitizenSuspended

Inactive
    └── CitizenDeactivated

Archived
    └── CitizenArchived
```

Los eventos se documentan en:

```text
DOMAIN-002D-Domain-Events.md
```

---

# Commands Asociados

Cada transición se inicia mediante un Command.

Ejemplos:

```text
SubmitCitizenVerification

ApproveCitizen

ActivateCitizen

SuspendCitizen

DeactivateCitizen

ArchiveCitizen
```

Los Commands se especifican en:

```text
DOMAIN-002C-Commands.md
```

---

# Restricciones

Las siguientes operaciones nunca están permitidas:

- Active → Draft
- Suspended → Draft
- Archived → Active
- Archived → Verified
- Archived → PendingVerification
- Archived → Draft

Estas restricciones preservan la trazabilidad histórica del
Aggregate.

---

# Compatibilidad con Event Sourcing

La máquina de estados puede reconstruirse completamente a
partir de la secuencia ordenada de Domain Events.

El estado almacenado es una proyección del historial de
eventos.

---

# Compatibilidad con CQRS

Las consultas pueden proyectar el estado actual del Citizen
sin acceder directamente al Aggregate.

Ejemplos de proyecciones:

- ciudadanos activos;
- ciudadanos suspendidos;
- ciudadanos pendientes de verificación;
- ciudadanos archivados.

---

# Principios Arquitectónicos

La State Machine cumple con:

- Domain-Driven Design (DDD);
- Clean Architecture;
- Event-Driven Architecture;
- Open/Closed Principle;
- Single Responsibility Principle.

---

# Definición de Éxito

La Máquina de Estados del Aggregate **Citizen** garantiza que
toda evolución de una identidad cívica siga un flujo explícito,
consistente y auditable, evitando transiciones inválidas y
proporcionando una base sólida para los procesos de
participación ciudadana e interoperabilidad del ecosistema
AURA.