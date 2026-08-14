# DOMAIN-011J — Notification Consistency Boundary

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Notification Management

Aggregate:
Notification

Documentos relacionados:

- DOMAIN-011-Aggregate.md
- DOMAIN-011A-Lifecycle.md
- DOMAIN-011B-State-Machine.md
- DOMAIN-011C-Commands.md
- DOMAIN-011D-Domain-Events.md
- DOMAIN-011E-Invariants.md
- DOMAIN-011G-Repository-Contract.md
- DOMAIN-011I-Versioning.md

---

# Objetivo

Este documento define el Consistency Boundary oficial del
Aggregate **Notification**.

Su propósito es establecer qué elementos pertenecen a la unidad de
consistencia de Notification y qué elementos permanecen fuera de
ella.

El límite determina qué reglas deben mantenerse de forma inmediata
y atómica durante una modificación del Aggregate.

---

# Definición

Notification constituye una unidad independiente de consistencia.

Toda modificación válida debe preservar de forma inmediata:

- identidad;
- estado;
- Lifecycle;
- State Machine;
- Invariants;
- Version;
- elementos internos oficialmente definidos.

Debe mantenerse:

```text
Notification

=

Independent Consistency Boundary
```

Ningún otro Aggregate forma parte de esta unidad transaccional.

---

# Alcance del Aggregate

El Consistency Boundary comprende conceptualmente:

```text
Notification
    │
    ├── NotificationId
    ├── NotificationStatus
    ├── State
    ├── Version
    ├── CreatedAt
    ├── UpdatedAt
    ├── Value Objects
    └── Internal Entities
```

únicamente cuando dichos Value Objects o Internal Entities hayan
sido definidos explícitamente como parte del Aggregate.

El límite contiene solamente la información necesaria para
mantener consistente una unidad de Notification.

---

# Aggregate Root

La única Aggregate Root es:

```text
Notification
```

Toda modificación dentro del Consistency Boundary debe atravesar
esta raíz.

Ningún elemento interno puede modificarse directamente desde fuera
del Aggregate.

Debe mantenerse:

```text
External Actor

    │
    ▼

Notification

    │
    ▼

Internal State
```

Nunca:

```text
External Actor

    │
    ▼

Internal Entity / State
```

---

# Dentro del Boundary

Pertenecen al Consistency Boundary:

- Notification como Aggregate Root;
- NotificationId;
- NotificationStatus;
- estado confirmado;
- Version;
- CreatedAt;
- UpdatedAt;
- Value Objects propios oficialmente definidos;
- Internal Entities propias oficialmente definidas;
- Invariants que protegen Notification;
- comportamiento necesario para ejecutar sus Commands;
- generación coherente de sus Domain Events.

Todos estos elementos deben quedar consistentes al finalizar una
operación válida.

---

# Fuera del Boundary

No pertenecen al Consistency Boundary:

```text
Organization

Citizen

Membership

Role

Territory

Assembly

Proposal

Participation

Voting

Document

Audit

Integration
```

Tampoco pertenecen:

- Read Models;
- Integration Events;
- proveedores de entrega;
- brokers;
- APIs externas;
- sistemas de mensajería;
- mecanismos de autenticación;
- mecanismos de autorización;
- Infrastructure;
- sistemas municipales;
- FIWARE.

---

# Referencias

Notification puede mantener referencias hacia conceptos externos
únicamente mediante:

```text
AggregateId

Domain Contract
```

cuando corresponda.

No debe mantener una referencia mutable a otro Aggregate.

Debe mantenerse:

```text
External Aggregate Reference

≠

Embedded Aggregate
```

Una referencia no transfiere ownership.

---

# Notification y Organization

Notification puede relacionarse con una Organization cuando el
contexto de dominio correspondiente lo requiera.

Organization permanece fuera del Boundary.

Notification no:

- modifica Organization;
- administra su Lifecycle;
- administra su estructura;
- comparte Version con Organization.

Debe mantenerse:

```text
Notification.Version

≠

Organization.Version
```

---

# Notification y Citizen

Citizen puede aportar identidad de destinatario cuando corresponda.

Citizen permanece fuera del Boundary.

Notification no almacena:

```text
Citizen
```

completo dentro del Aggregate.

Tampoco modifica:

- CitizenStatus;
- identidad cívica;
- Lifecycle de Citizen.

---

# Notification y Membership

Membership puede aportar contexto organizacional para políticas de
comunicación.

Membership permanece fuera del Boundary.

Notification no:

- crea Membership;
- modifica Membership;
- suspende Membership;
- termina Membership.

---

# Notification y Role

Role puede participar en políticas externas de autorización o
determinación de destinatarios.

Role permanece fuera del Boundary.

Notification no administra:

- definición de Roles;
- asignación de Roles;
- jerarquía de Roles.

---

# Notification y Territory

Territory puede aportar contexto cuando exista una regla explícita
de dominio.

Territory permanece fuera del Boundary.

Notification no modifica:

- estructura territorial;
- relaciones territoriales;
- Lifecycle de Territory.

---

# Notification y Assembly

Assembly puede producir hechos que posteriormente generen una
necesidad de Notification.

Assembly permanece fuera del Boundary.

Debe mantenerse:

```text
Assembly

│
▼

Confirmed Domain Fact

│
▼

Notification Management
```

y nunca:

```text
Notification

│
▼

Direct Assembly Mutation
```

Una Notification puede permanecer:

```text
Draft

Pending

Failed
```

mientras el hecho correspondiente de Assembly ya se encuentra
confirmado.

Esto no representa una inconsistencia.

---

# Notification y Proposal

Proposal conserva:

- ProposalId;
- Lifecycle;
- State Machine;
- Invariants;
- Version;
- Repository;
- Consistency Boundary.

Notification puede reaccionar a hechos de Proposal mediante
contratos definidos.

Notification no modifica directamente Proposal.

---

# Notification y Participation

Participation mantiene su propia consistencia.

Notification puede recibir una necesidad de comunicación derivada
de un hecho confirmado de Participation.

Ambos Aggregates permanecen separados.

Debe mantenerse:

```text
Participation Transaction

≠

Notification Transaction
```

---

# Notification y Voting

Voting mantiene su propia identidad, Lifecycle, State Machine,
Invariants y Version.

Notification no:

- abre Voting;
- cierra Voting;
- registra votos;
- modifica resultados;
- cambia VotingStatus.

Un hecho confirmado de Voting puede originar posteriormente una
Notification sin ampliar el Consistency Boundary de ninguno de los
dos Aggregates.

---

# Notification y Document

Document permanece fuera del Consistency Boundary.

Cuando una Notification necesite relacionarse con un Document debe
hacerlo mediante:

```text
DocumentId
```

o contrato equivalente.

Notification no contiene:

```text
Document
```

ni administra:

- Content;
- DocumentType;
- DocumentStatus;
- Document.Version;
- Document Lifecycle.

---

# Notification y Audit

Audit permanece fuera del Consistency Boundary.

Los Domain Events de Notification pueden aportar hechos utilizados
posteriormente por Audit.

Debe mantenerse:

```text
Notification Domain Event

≠

Audit Record
```

La creación de un Audit Record no forma parte de la misma
modificación atómica del Aggregate Notification.

---

# Notification e Integration

Integration permanece fuera del Consistency Boundary.

Notification puede producir Domain Events que posteriormente sean
utilizados para generar Integration Events cuando exista un
contrato explícito.

Debe mantenerse:

```text
Notification Domain Event

≠

Integration Event
```

y:

```text
Notification Commit

≠

External System Commit
```

---

# Reglas de Consistencia

Toda modificación del Aggregate debe garantizar:

- un único NotificationId;
- estado válido;
- transición válida;
- Invariants satisfechas;
- Version coherente;
- CreatedAt preservado;
- UpdatedAt actualizado únicamente en modificación válida;
- Domain Events coherentes;
- ausencia de modificaciones parciales.

Debe mantenerse:

```text
Valid Transaction

↓

Entire Notification Consistent
```

---

# Consistencia Inmediata

Dentro de Notification la consistencia es inmediata.

Una operación válida no puede finalizar con:

- estado parcialmente actualizado;
- Version antigua junto a estado nuevo;
- transición incompleta;
- Invariants violadas;
- Domain Event incompatible con el estado resultante.

Debe cumplirse:

```text
Internal Consistency

=

Immediate
```

---

# Transacción Conceptual

Una modificación de Notification sigue conceptualmente:

```text
Command

    │
    ▼

Load Notification

    │
    ▼

Validate Permissions

    │
    ▼

Validate State

    │
    ▼

Validate Invariants

    │
    ▼

Execute Behavior

    │
    ▼

Transition State

    │
    ▼

Increment Version

    │
    ▼

Produce Domain Events

    │
    ▼

Persist Notification

    │
    ▼

Commit
```

La operación debe ser confirmada como una única modificación
consistente del Aggregate.

---

# Fallo durante la Transacción

Si la modificación no puede completarse:

```text
Operation

↓

Failure

↓

No Confirmed Aggregate Change
```

Una operación rechazada:

- no cambia NotificationStatus;
- no cambia Version;
- no cambia UpdatedAt;
- no confirma Domain Events de éxito.

No puede existir un estado parcialmente confirmado.

---

# Coordinación entre Aggregates

La coordinación con otros Aggregates se realiza mediante:

- Domain Events;
- Integration Events;
- Application Services;
- contratos explícitos;
- procesos de aplicación;
- consistencia eventual.

No se requiere una transacción distribuida que modifique
simultáneamente Notification y otro Aggregate.

Debe mantenerse:

```text
Aggregate A Transaction

≠

Aggregate B Transaction
```

---

# Consistencia Eventual

La consistencia entre Notification y otros Aggregates puede ser
eventual.

Conceptualmente:

```text
Source Aggregate

    │
    ▼

Commit

    │
    ▼

Domain Event / Contract

    │
    ▼

Notification Management

    │
    ▼

Notification
```

Puede existir una ventana temporal entre:

```text
Source Fact Confirmed
```

y:

```text
Notification Created
```

o entre:

```text
Notification Pending
```

y:

```text
Notification Delivered
```

Estas ventanas son compatibles con los límites DDD definidos por
AURA.

---

# Resultado de Entrega y Consistency Boundary

El resultado de entrega pertenece a Notification una vez
incorporado válidamente al dominio.

La ejecución técnica que produce dicho resultado permanece fuera
del Boundary.

Conceptualmente:

```text
Delivery Provider

    │
    ▼

Application / Adapter

    │
    ▼

ConfirmNotificationDelivery
```

o:

```text
Delivery Provider

    │
    ▼

Application / Adapter

    │
    ▼

ReportNotificationDeliveryFailure
```

El proveedor externo nunca modifica directamente:

```text
NotificationStatus
```

---

# Failed y Consistency Boundary

Cuando Notification evoluciona:

```text
Pending → Failed
```

únicamente cambia el Aggregate Notification.

No cambia atómicamente:

- Assembly;
- Document;
- Citizen;
- Organization;
- Voting;
- Proposal;
- Participation.

Por lo tanto:

```text
Notification Failed

≠

External Aggregate Rollback
```

---

# Retry y Consistency Boundary

`RetryNotification` modifica exclusivamente el Aggregate
Notification.

La transición:

```text
Failed → Pending
```

conserva:

- NotificationId;
- historial;
- Consistency Boundary;
- independencia de otros Aggregates.

RetryNotification no requiere modificar de forma atómica el
Aggregate que originó la Notification.

---

# Invariants dentro del Boundary

Las Invariants de Notification pertenecen al mismo Consistency
Boundary.

Entre ellas se encuentran:

- NotificationId obligatorio;
- NotificationId inmutable;
- estado válido;
- transición válida;
- Delivered terminal;
- Failed solamente puede volver a Pending;
- modificación únicamente mediante Aggregate Root;
- toda modificación válida incrementa Version;
- operación rechazada conserva estado y Version;
- referencias externas mediante IDs o contratos;
- no embedding de Aggregates externos.

La definición completa pertenece a:

```text
DOMAIN-011E-Invariants.md
```

---

# Version dentro del Boundary

Version pertenece al Consistency Boundary.

Debe persistirse junto al estado resultante de la modificación.

Debe mantenerse:

```text
Notification State

+

Notification Version

=

Same Atomic Aggregate State
```

No puede confirmarse:

```text
New Status

+

Old Version
```

como resultado válido.

---

# Domain Events dentro del Boundary

Los Domain Events se producen como consecuencia de comportamiento
válido de Notification.

Los eventos oficiales son:

```text
NotificationCreated

NotificationQueued

NotificationDelivered

NotificationDeliveryFailed

NotificationRetried
```

Deben ser coherentes con el estado y Version resultantes.

La publicación externa del evento ocurre después del commit
correspondiente y permanece fuera del Consistency Boundary.

---

# Lo que el Aggregate nunca hace

Notification nunca:

- carga Aggregates externos como parte de su estado interno;
- modifica directamente otro Aggregate;
- ejecuta transacciones distribuidas entre Aggregates;
- espera una modificación externa para alcanzar consistencia
  interna;
- depende de un proveedor de entrega;
- depende de una API externa;
- depende de un broker;
- depende de FIWARE;
- depende de una base de datos;
- depende de HTTP;
- administra Authentication;
- administra Authorization;
- almacena credenciales;
- modifica Read Models directamente;
- crea Audit Records directamente;
- convierte Integration Events en estado interno.

---

# Repository y Boundary

El Repository persiste Notification como una única unidad de
consistencia.

Debe preservar:

```text
Notification

+

Version

+

State
```

de forma coherente.

No persiste otros Aggregates como parte de la misma unidad
Notification.

Debe mantenerse:

```text
NotificationRepository

≠

Multi-Aggregate Repository
```

---

# Read Models y Boundary

Los Read Models permanecen fuera del Consistency Boundary.

Pueden contener información derivada y denormalizada procedente de
múltiples Aggregates.

Sin embargo:

```text
Read Model

≠

Write Consistency Boundary
```

Un Read Model no puede:

- ejecutar transiciones;
- cambiar NotificationStatus;
- cambiar Version;
- validar el Lifecycle como autoridad de escritura.

---

# Relación con CQRS

El Consistency Boundary corresponde al Write Model.

Conceptualmente:

```text
Write Side

    │
    ▼

Notification Aggregate

    │
    ▼

Immediate Consistency
```

Mientras:

```text
Domain Events

    │
    ▼

Read Side

    │
    ▼

Eventually Consistent Projections
```

CQRS no modifica el límite del Aggregate.

---

# Relación con Event Sourcing

En una estrategia Event Sourcing, Notification se reconstruye
únicamente desde los hechos asociados al mismo:

```text
NotificationId
```

Por ejemplo:

```text
NotificationCreated

↓

NotificationQueued

↓

NotificationDeliveryFailed

↓

NotificationRetried

↓

NotificationDelivered
```

No se incorporan dentro de la reconstrucción eventos internos de:

- Assembly;
- Document;
- Voting;
- Proposal;
- Participation;
- Citizen;
- Organization.

Estos pertenecen a otros Consistency Boundaries.

---

# Escenario de Ejemplo

Una Assembly produce un hecho confirmado que requiere una
Notification.

Conceptualmente:

```text
Assembly Transaction

    │
    ▼

Assembly Commit

    │
    ▼

Confirmed Fact

    │
    ▼

Notification Management

    │
    ▼

CreateNotification

    │
    ▼

Notification Commit
```

Existen dos transacciones independientes:

```text
Assembly Transaction
```

y:

```text
Notification Transaction
```

La segunda no forma parte del Consistency Boundary de Assembly.

La primera no forma parte del Consistency Boundary de Notification.

---

# Beneficios

Mantener un Boundary pequeño e independiente permite:

- alta cohesión;
- bajo acoplamiento;
- transacciones cortas;
- reducción de conflictos concurrentes;
- independencia entre Aggregates;
- escalabilidad;
- consistencia eventual controlada;
- integración mediante eventos;
- evolución independiente;
- compatibilidad con CQRS;
- compatibilidad con Event Sourcing.

---

# Principios Arquitectónicos

El Consistency Boundary de Notification cumple:

- Domain-Driven Design;
- Aggregate Pattern;
- una única Aggregate Root;
- consistencia inmediata dentro del Aggregate;
- consistencia eventual entre Aggregates;
- referencias externas mediante identificadores o contratos;
- ausencia de transacciones distribuidas como requisito del
  Aggregate;
- Persistence Ignorance;
- Separation of Concerns;
- High Cohesion;
- Low Coupling.

---

# Definición de Éxito

El Consistency Boundary del Aggregate **Notification** establece de
forma explícita qué información debe permanecer consistente dentro
de una única unidad de dominio.

El Boundary incluye:

```text
Notification

NotificationId

NotificationStatus

State

Version

CreatedAt

UpdatedAt

Value Objects propios

Internal Entities propias
```

cuando dichos elementos hayan sido definidos oficialmente dentro
del Aggregate.

El Boundary excluye:

```text
Organization

Citizen

Membership

Role

Territory

Assembly

Proposal

Participation

Voting

Document

Audit

Integration
```

y garantiza que:

- Notification posee una única Aggregate Root;
- toda modificación interna es atómica;
- las Invariants se mantienen inmediatamente;
- Version y estado se confirman coherentemente;
- no existen modificaciones parciales;
- los Domain Events corresponden al estado resultante;
- los Aggregates externos permanecen independientes;
- las referencias externas utilizan identificadores o contratos;
- Notification no modifica directamente otros Aggregates;
- un fallo de Notification no revierte el Aggregate originador;
- RetryNotification modifica únicamente Notification;
- la ejecución técnica de entrega permanece fuera del Boundary;
- el Repository persiste solamente Notification como unidad;
- Read Models permanecen fuera de la autoridad de escritura;
- Integration Events permanecen fuera del Aggregate;
- Audit permanece separado;
- la consistencia entre Aggregates puede ser eventual;
- CQRS y Event Sourcing respetan el mismo límite.

De esta forma, `DOMAIN-011J-Consistency-Boundary.md` establece el
límite oficial de consistencia del Aggregate **Notification**
conforme al patrón consolidado de AURA Core.