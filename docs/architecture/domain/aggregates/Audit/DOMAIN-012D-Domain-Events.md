# DOMAIN-012D — Audit Domain Events

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Audit Management

Aggregate:
Audit

Autor:
ARADA

Documentos relacionados:

- DOMAIN-012-Aggregate.md
- DOMAIN-012A-Lifecycle.md
- DOMAIN-012B-State-Machine.md
- DOMAIN-012C-Commands.md
- DOMAIN-012E-Invariants.md
- DOMAIN-012F-Permissions.md
- DOMAIN-012G-Repository-Contract.md
- DOMAIN-012I-Versioning.md
- DOMAIN-012J-Consistency-Boundary.md
- DOMAIN-012K-Integration-Events.md
- DOMAIN-012L-Read-Model.md
- DOMAIN-012M-Test-Scenarios.md
- DOMAIN-012O-Security-Model.md
- CORE-006-Domain-Invariants.md
- CORE-008-Aggregate-Design-Rules.md
- CORE-011-Repository-Contracts.md

---

# Objetivo

Este documento define formalmente los **Domain Events** publicados
por el Aggregate **Audit** cuando ocurren hechos relevantes dentro
de su propio Consistency Boundary.

Un Domain Event representa un hecho consumado.

Describe algo que ocurrió efectivamente dentro del dominio Audit y
que ya fue aceptado por la Aggregate Root después de validar:

- intención recibida;
- State Machine;
- precondiciones;
- Invariants;
- Permissions aplicables;
- consistencia;
- Versioning.

Los Domain Events permiten representar la evolución de Audit sin
acoplarlo directamente a otros Aggregates, Bounded Contexts,
Infrastructure o sistemas externos.

---

# Propósito

Los Domain Events permiten expresar hechos significativos de Audit
mediante el Ubiquitous Language de AURA.

La versión 1.0 posee un Lifecycle mínimo:

```text
No Audit → Recorded
```

y un único Command oficial:

```text
RecordAudit
```

Por lo tanto, el hecho oficial producido por una creación válida es:

```text
AuditRecorded
```

Los Domain Events permiten:

- preservar trazabilidad;
- representar hechos propios del Aggregate;
- desacoplar Audit de otros Aggregates;
- alimentar Read Models;
- iniciar procesos posteriores;
- permitir Integration Events cuando exista un contrato explícito;
- mantener compatibilidad con CQRS;
- mantener compatibilidad con Event Sourcing;
- preservar causalidad;
- preservar evolución mediante AggregateVersion.

---

# Principio Fundamental

Un Domain Event representa:

```text
Fact
```

No representa:

```text
Intent
```

Por lo tanto:

```text
RecordAudit
```

es un Command.

Mientras:

```text
AuditRecorded
```

es un Domain Event.

Conceptualmente:

```text
RecordAudit
    │
    ▼
Audit
    │
    ├── valida State Machine
    ├── valida precondiciones
    ├── valida Invariants
    └── ejecuta comportamiento
            │
            ▼
       AuditRecorded
```

El Domain Event solamente existe cuando el hecho ocurrió
realmente.

---

# Commands versus Domain Events

Los Commands expresan intención en forma imperativa.

La versión 1.0 define:

```text
RecordAudit
```

Los Domain Events expresan hechos consumados en pasado.

La versión 1.0 define:

```text
AuditRecorded
```

Nunca debe utilizarse:

```text
AuditRecorded
```

como solicitud para crear Audit.

Tampoco debe utilizarse:

```text
RecordAudit
```

como representación histórica de un Audit ya registrado.

---

# Propiedad del Evento

El Domain Event:

```text
AuditRecorded
```

pertenece conceptualmente al Aggregate:

```text
Audit
```

La Aggregate Root es responsable de producirlo cuando la operación
válida crea una nueva unidad Audit.

Otros Aggregates, Read Models, procesos de Integration u otros
consumidores pueden reaccionar posteriormente al hecho.

No adquieren ownership sobre el evento original.

---

# Source Domain Event versus Audit Domain Event

Audit puede originarse a partir de un Domain Event perteneciente a
otro Aggregate.

Debe mantenerse una separación explícita entre:

```text
Source Domain Event
```

y:

```text
AuditRecorded
```

Ejemplo conceptual:

```text
AssemblyStarted
    │
    ▼
Audit Coordination
    │
    ▼
RecordAudit
    │
    ▼
AuditRecorded
```

Debe mantenerse:

```text
AssemblyStarted

≠

AuditRecorded
```

El primer evento pertenece a Assembly.

El segundo pertenece a Audit.

---

# Audit Record versus Domain Event

Debe mantenerse:

```text
Audit

≠

AuditRecorded
```

`Audit` representa el estado del Aggregate.

`AuditRecorded` representa el hecho de que dicho Aggregate fue
registrado válidamente.

También debe mantenerse:

```text
Source Domain Event

≠

Audit

≠

AuditRecorded
```

Cada concepto posee responsabilidad y ownership propios.

---

# Alcance

Los Domain Events de Audit describen exclusivamente hechos
pertenecientes al Aggregate Audit.

No representan directamente hechos internos de:

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

Notification

Integration
```

Cuando un hecho pertenece a otro Aggregate debe ser publicado por
el Aggregate responsable.

---

# Evento Oficial

La versión 1.0 define conceptualmente un único Domain Event:

```text
AuditRecorded
```

No existen otros Domain Events oficiales en esta versión.

---

# AuditRecorded

## Definición

`AuditRecorded` representa el hecho de que una nueva unidad Audit
fue registrada válidamente dentro de Audit Management.

Significa que:

```text
No Audit → Recorded
```

ocurrió correctamente.

---

## Command origen

```text
RecordAudit
```

---

## Estado previo

```text
No Audit
```

`No Audit` representa inexistencia conceptual y no un estado
persistido.

---

## Estado resultante

```text
Recorded
```

Recorded constituye:

- el único estado persistido;
- el estado inicial;
- el estado terminal;
- la representación confirmada de una unidad Audit.

---

## AggregateVersion

Después de una creación válida:

```text
AggregateVersion = 1
```

conforme al Versioning oficial del Aggregate.

---

## Significado

El evento significa exclusivamente:

```text
An Audit unit was successfully recorded
```

No significa que:

- el Source Aggregate haya cambiado nuevamente;
- el Source Domain Event haya sido modificado;
- el hecho original haya sido creado por Audit;
- un Integration Event haya sido publicado;
- un Read Model haya sido actualizado;
- un consumidor externo haya procesado el hecho;
- un registro técnico haya sido persistido en una tecnología
  específica;
- una operación FIWARE haya sido ejecutada.

---

# Estructura General

Todo Domain Event de Audit debe contener conceptualmente:

```text
EventId

EventType

AuditId

AggregateVersion

OccurredAt

CorrelationId

CausationId

Payload
```

cuando los elementos correspondientes sean aplicables conforme al
contrato oficial.

---

# EventId

`EventId` identifica de forma única el Domain Event.

Debe:

- ser único;
- ser inmutable;
- no reutilizarse;
- identificar un único hecho;
- ser independiente de AuditId;
- permitir trazabilidad.

Debe mantenerse:

```text
EventId

≠

AuditId
```

---

# EventType

`EventType` representa el nombre semántico del hecho.

Para la versión 1.0:

```text
EventType = AuditRecorded
```

EventType utiliza Ubiquitous Language.

No debe utilizar nombres de:

- tablas;
- endpoints;
- frameworks;
- brokers;
- bases de datos;
- protocolos;
- proveedores;
- tecnologías externas.

---

# AuditId

`AuditId` identifica el Aggregate que produjo el Domain Event.

Debe mantenerse:

```text
Event.AuditId

=

Audit.AuditId
```

para la Version del Aggregate que produjo el hecho.

AuditId permanece inmutable.

---

# AggregateVersion

`AggregateVersion` identifica la Version resultante del Aggregate
que produjo el evento.

Para `AuditRecorded`:

```text
AggregateVersion = 1
```

Debe mantenerse:

```text
Event.AggregateVersion

=

Resulting Audit.Version
```

No debe confundirse con:

```text
SourceAggregateVersion
```

---

# OccurredAt

`OccurredAt` representa el momento en que ocurrió el hecho propio de
Audit:

```text
AuditRecorded
```

No debe confundirse automáticamente con:

```text
SourceOccurredAt
```

ni con el timestamp del Source Domain Event.

Conceptualmente:

```text
Source Fact OccurredAt

≠

AuditRecorded.OccurredAt
```

aunque ambos puedan coincidir temporalmente.

---

# CorrelationId

`CorrelationId` puede permitir relacionar Audit con el flujo que
originó la operación.

Puede preservar una correlación recibida cuando corresponda.

No constituye:

- AuditId;
- EventId;
- SourceAggregateId;
- Permission;
- Version.

---

# CausationId

`CausationId` permite representar conceptualmente la causa inmediata
del evento cuando exista.

Puede relacionar:

```text
RecordAudit

↓

AuditRecorded
```

conforme al contrato aplicado.

No constituye identidad del Aggregate.

---

# Payload

El Payload contiene únicamente información necesaria para expresar
el hecho:

```text
AuditRecorded
```

Debe mantenerse:

```text
Payload

=

Minimum Meaningful Domain Information
```

No constituye una copia completa del Aggregate.

---

# Payload Conceptual de AuditRecorded

`AuditRecorded` puede contener conceptualmente información como:

```text
AuditId

SourceAggregateId

SourceAggregateType

SourceEventId

SourceEventType

SourceAggregateVersion

ActorId

SourceOccurredAt
```

únicamente cuando dichos valores:

- sean aplicables;
- estén disponibles;
- formen parte del contrato auditable;
- sean necesarios para representar el hecho.

No deben inventarse valores faltantes.

---

# SourceAggregateId

Cuando exista:

```text
SourceAggregateId
```

identifica al Aggregate originador del hecho auditado.

No identifica al Aggregate Audit.

Debe mantenerse:

```text
SourceAggregateId

≠

AuditId
```

---

# SourceAggregateType

`SourceAggregateType` puede representar el tipo conceptual del
Aggregate originador cuando corresponda.

No implica dependencia sobre la clase, estructura interna o
implementación del Aggregate externo.

---

# SourceEventId

Cuando el origen sea un Domain Event:

```text
SourceEventId
```

puede identificar el evento auditado.

Debe mantenerse:

```text
SourceEventId

≠

AuditRecorded.EventId
```

El Source Event conserva su propia identidad.

---

# SourceEventType

Cuando corresponda:

```text
SourceEventType
```

preserva el tipo del hecho originador.

Audit no cambia ni redefine su semántica.

---

# SourceAggregateVersion

`SourceAggregateVersion` representa la Version asociada al hecho
originador cuando esté disponible.

Debe mantenerse:

```text
SourceAggregateVersion

≠

AggregateVersion
```

del Domain Event de Audit.

El primer valor pertenece al Source Aggregate.

El segundo pertenece al Aggregate Audit.

---

# ActorId

`ActorId` puede conservarse cuando el hecho de origen identifica
conceptualmente a un actor.

ActorId no implica que Audit administre:

- Citizen;
- Membership;
- Role;
- Authentication;
- Authorization.

---

# SourceOccurredAt

Cuando el hecho originador proporciona:

```text
OccurredAt
```

Audit puede preservar conceptualmente dicho valor como:

```text
SourceOccurredAt
```

dentro de su propia representación.

Debe mantenerse:

```text
SourceOccurredAt

≠

AuditRecorded.OccurredAt
```

porque representan hechos distintos.

---

# Información Ausente

AuditRecorded no debe fabricar información que el dominio no posee.

Si el Source Fact no proporciona:

```text
ActorId

SourceEventId

SourceAggregateVersion

CorrelationId

CausationId
```

u otra información opcional, el Domain Event no debe inventarla.

Debe mantenerse:

```text
Missing Information

≠

Fabricated Event Data
```

---

# Minimización

El Payload debe utilizar únicamente la información requerida para
representar el hecho.

No debe copiar automáticamente:

```text
Entire Source Event Payload
```

ni:

```text
Entire Source Aggregate
```

ni:

```text
Entire Audit Aggregate
```

Debe mantenerse:

```text
Source Payload

≠

Automatic AuditRecorded Payload
```

---

# Inmutabilidad

Una vez producido:

```text
AuditRecorded
```

el evento representa un hecho histórico consumado.

No puede modificarse retrospectivamente.

Debe mantenerse:

```text
Historical Domain Event

=

Immutable
```

---

# Inmutabilidad del Source Fact

AuditRecorded tampoco modifica:

- SourceEventId;
- SourceEventType;
- SourceAggregateId;
- SourceAggregateVersion;
- SourceOccurredAt;
- Payload del Source Domain Event.

Audit conserva una representación propia.

---

# Evento Rechazado

Si:

```text
RecordAudit
```

es rechazado:

```text
AuditRecorded
```

no debe existir.

Conceptualmente:

```text
Invalid RecordAudit

    │
    ▼

Rejected

    │
    ▼

No AuditRecorded
```

---

# Fallo de Persistencia

Un fallo técnico como:

```text
PersistenceFailure
```

no constituye:

```text
AuditRecorded
```

si la creación del Aggregate no quedó confirmada conforme al
contrato de persistencia.

Debe mantenerse:

```text
PersistenceFailure

≠

Domain Event
```

---

# Concurrency Conflict

Un:

```text
ConcurrencyConflict
```

no constituye Domain Event de Audit.

Si la operación no puede confirmarse:

```text
AuditRecorded
```

no se produce como hecho exitoso de dicha operación.

---

# Duplicate Audit

Una entrega técnica duplicada no debe producir automáticamente:

```text
AuditRecorded
```

nuevamente.

Debe mantenerse:

```text
Duplicate Technical Delivery

≠

New Domain Fact
```

---

# Reintento Técnico

Un retry técnico para procesar el mismo hecho no constituye:

```text
AuditRecorded
```

hasta que la operación de dominio sea confirmada.

Tampoco constituye un evento adicional de dominio por el solo hecho
de repetirse.

---

# No Evento de Retry

La versión 1.0 no define:

```text
AuditRetried
```

porque:

```text
RetryAudit
```

no es un Command oficial.

Los reintentos técnicos pertenecen a capas externas.

---

# No Evento de Archive

La versión 1.0 no define:

```text
AuditArchived
```

porque:

```text
Archived
```

no pertenece al Lifecycle.

---

# No Evento de Delete

La versión 1.0 no define:

```text
AuditDeleted
```

porque:

```text
Deleted
```

no pertenece al Lifecycle.

---

# No Evento de Update

La versión 1.0 no define:

```text
AuditUpdated
```

ni:

```text
AuditModified
```

como eventos genéricos.

El dominio no posee Commands genéricos:

```text
UpdateAudit

ModifyAudit
```

---

# No Evento de Correction

La versión 1.0 no define:

```text
AuditCorrected
```

ni:

```text
AuditInvalidated
```

como Domain Events.

Una corrección del Source Aggregate debe expresarse mediante un
nuevo hecho del contexto responsable cuando corresponda.

Audit no reescribe el hecho previo.

---

# Eventos Técnicos No Permitidos

No pertenecen al Aggregate Domain Events como:

```text
AuditSaved

AuditLoaded

AuditSerialized

AuditCached

AuditPersisted

AuditDatabaseUpdated

AuditMessagePublished

AuditBrokerPublished

AuditHttpRequestCompleted

AuditFIWARESynced

AuditProjectionUpdated
```

Estos representan hechos técnicos.

No hechos propios del dominio Audit.

---

# Eventos Futuros

La versión 1.0 no define eventos como:

```text
AuditArchived

AuditDeleted

AuditCorrected

AuditInvalidated

AuditExpired

AuditRedacted

AuditAnonymized

AuditRetried
```

porque los Commands, estados o comportamientos correspondientes no
forman parte del modelo oficial actual.

No deben introducirse aisladamente.

---

# Relación con State Machine

La relación oficial versión 1.0 es:

| Domain Event | Estado previo | Estado resultante |
|---|---|---|
| AuditRecorded | No Audit | Recorded |

No existen otros cambios de estado oficiales.

---

# Relación con Commands

La relación oficial es:

| Command | Domain Event |
|---|---|
| RecordAudit | AuditRecorded |

Una operación rechazada produce:

```text
No Success Domain Event
```

---

# Relación con Version

La secuencia oficial de creación es:

```text
No Audit

    │
    ▼

RecordAudit

    │
    ▼

Audit Version 1

    │
    ▼

AuditRecorded
AggregateVersion = 1
```

Debe mantenerse:

```text
AuditRecorded.AggregateVersion

=

Audit.Version
```

resultante.

---

# Relación con Invariants

AuditRecorded solamente puede producirse después de que las
Invariants permanezcan satisfechas.

Conceptualmente:

```text
RecordAudit
    │
    ▼
Validate Invariants
    │
    ├── Invalid
    │      │
    │      ▼
    │   Rejected
    │
    └── Valid
           │
           ▼
       AuditRecorded
```

---

# Relación con Permissions

Las Permissions aplicables deben evaluarse conforme al modelo
definido en:

```text
DOMAIN-012F-Permissions.md
```

Una operación no autorizada no produce:

```text
AuditRecorded
```

Debe mantenerse:

```text
Unauthorized Operation

↓

No Audit Domain Event
```

---

# AuditRecorded y Source Aggregate

AuditRecorded no modifica directamente:

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

Notification

Integration
```

Estos Aggregates mantienen sus propios Consistency Boundaries.

---

# AuditRecorded y Organization

Un hecho de Organization puede originar Audit.

Conceptualmente:

```text
Organization Domain Event

    │
    ▼

RecordAudit

    │
    ▼

AuditRecorded
```

AuditRecorded no modifica Organization.

---

# AuditRecorded y Citizen

Un hecho relacionado con Citizen puede originar Audit.

AuditRecorded no modifica:

- identidad de Citizen;
- estado de Citizen;
- Lifecycle de Citizen.

---

# AuditRecorded y Membership

Un Domain Event de Membership puede constituir un hecho auditable.

AuditRecorded no modifica:

```text
MembershipStatus

Membership.Version

Membership Lifecycle
```

---

# AuditRecorded y Role

Un hecho de Role puede originar Audit.

AuditRecorded no:

- crea Roles;
- modifica Roles;
- asigna Roles;
- revoca Roles;
- cambia Permissions.

---

# AuditRecorded y Territory

Un Domain Event de Territory puede constituir un hecho auditable.

Territory permanece fuera del Consistency Boundary.

---

# AuditRecorded y Assembly

Ejemplo conceptual:

```text
AssemblyStarted
    │
    ▼
Audit Coordination
    │
    ▼
RecordAudit
    │
    ▼
AuditRecorded
```

AuditRecorded no modifica:

```text
AssemblyStatus

Assembly.Version

Assembly Lifecycle
```

---

# AuditRecorded y Proposal

Un hecho de Proposal puede ser auditado.

AuditRecorded no modifica:

```text
ProposalStatus

Proposal.Version

Proposal Lifecycle
```

---

# AuditRecorded y Participation

Un hecho de Participation puede ser auditado.

AuditRecorded no modifica Participation.

Debe mantenerse:

```text
Participation Transaction

≠

Audit Transaction
```

---

# AuditRecorded y Voting

Los hechos confirmados de Voting pueden ser auditables.

AuditRecorded no:

- registra votos;
- modifica votos;
- abre Voting;
- cierra Voting;
- modifica resultados;
- cambia VotingStatus.

---

# AuditRecorded y Document

Un hecho confirmado de Document puede originar Audit.

AuditRecorded no modifica:

```text
DocumentStatus

Document.Version

Document Content

Document Lifecycle
```

---

# AuditRecorded y Notification

Un hecho confirmado de Notification puede originar Audit.

Por ejemplo:

```text
NotificationDelivered
    │
    ▼
Audit Coordination
    │
    ▼
RecordAudit
    │
    ▼
AuditRecorded
```

AuditRecorded no modifica:

```text
NotificationStatus

Notification.Version

Notification Lifecycle
```

---

# Domain Events y Consistency Boundary

AuditRecorded se produce dentro del Consistency Boundary:

```text
Audit
```

No implica modificación atómica de:

```text
Source Aggregate

Integration

Read Models

External Systems
```

La definición formal del límite pertenece a:

```text
DOMAIN-012J-Consistency-Boundary.md
```

---

# Consistencia Eventual

Puede existir una ventana donde:

```text
Source Domain Event Confirmed
```

y Audit todavía no haya producido:

```text
AuditRecorded
```

Esto es coherente con la separación entre Aggregates.

Debe mantenerse:

```text
Source Aggregate Commit

≠

Audit Commit
```

---

# Fallo de Audit

Si Audit no puede registrarse después de un hecho confirmado:

```text
Source Domain Fact
```

permanece válido.

No se produce rollback automático.

Debe mantenerse:

```text
Audit Failure

≠

Source Aggregate Rollback
```

---

# Domain Events y Read Models

AuditRecorded puede alimentar Read Models.

Conceptualmente:

```text
AuditRecorded
    │
    ▼
Projection
    │
    ▼
Audit Read Model
```

Los Read Models:

- no modifican Audit;
- no producen AuditRecorded;
- no constituyen fuente transaccional de verdad;
- pueden estar eventualmente desactualizados.

---

# Domain Events y CQRS

Dentro de CQRS:

```text
RecordAudit
    │
    ▼
Audit Write Model
    │
    ▼
AuditRecorded
    │
    ▼
Projection
    │
    ▼
Audit Read Model
```

El Read Side permanece separado del Write Side.

---

# Domain Events y Event Sourcing

AuditRecorded es compatible conceptualmente con Event Sourcing.

Una unidad Audit versión 1.0 podría reconstruirse conceptualmente a
partir de:

```text
AuditRecorded
```

produciendo:

```text
State = Recorded

Version = 1
```

La compatibilidad no obliga a utilizar Event Sourcing.

---

# Rehidratación desde Eventos

Si Audit es reconstruido desde:

```text
AuditRecorded
```

el evento debe aplicarse sin producirse nuevamente.

Conceptualmente:

```text
apply(AuditRecorded)

    │
    ▼

AuditStatus = Recorded
```

sin agregar un nuevo:

```text
AuditRecorded
```

---

# Replay

Debe mantenerse:

```text
Event Replay

≠

New Domain Fact
```

y:

```text
Event Replay

≠

RecordAudit Execution
```

La reconstrucción no incrementa Version más allá de la Version
representada por el historial.

---

# Domain Events e Integration Events

Debe existir separación explícita entre:

```text
AuditRecorded
```

y cualquier:

```text
Integration Event
```

Debe mantenerse:

```text
Domain Event

≠

Integration Event
```

La existencia de AuditRecorded no obliga automáticamente a crear un
Integration Event.

---

# Transformación hacia Integration

Cuando exista un contrato explícito:

```text
AuditRecorded
    │
    ▼
Application / Integration Handler
    │
    ▼
Integration Event
    │
    ▼
External Consumer
```

Audit no publica directamente contratos externos.

La especificación formal pertenece a:

```text
DOMAIN-012K-Integration-Events.md
```

---

# Domain Event no implica Integration Event

Debe mantenerse:

```text
AuditRecorded

≠

Mandatory Integration Event
```

La publicación externa requiere una necesidad explícita de
integración.

---

# Publicación

Un hecho externo solamente puede publicarse después de que Audit
haya sido confirmado.

Debe mantenerse:

```text
Audit Commit

    │
    ▼

Integration Publication
```

y nunca:

```text
Integration Publication

    │
    ▼

Try Audit Commit
```

---

# Transactional Outbox

Cuando la arquitectura utilice Transactional Outbox, Audit no
conoce directamente la Outbox.

Conceptualmente:

```text
Audit
    │
    ▼
Domain Event
    │
    ▼
Transaction
    ├── Aggregate State
    └── Outbox Record
            │
            ▼
       Dispatcher
```

La técnica concreta pertenece a Application e Infrastructure.

---

# Outbox no es Domain Event

Estados técnicos como:

```text
Pending

Published

Failed

Retrying
```

pertenecientes a Outbox no son estados ni Domain Events de Audit.

---

# Persistencia de Domain Events

Cuando la arquitectura requiera conservar Domain Events, deben
preservarse conceptualmente:

```text
EventId

EventType

AuditId

AggregateVersion

OccurredAt

CorrelationId

CausationId

Payload
```

La representación física pertenece a Infrastructure.

---

# Domain Event Store

La existencia de un Event Store no es obligatoria para Audit.

El modelo permanece compatible con:

```text
State Persistence + Domain Events
```

y con:

```text
Event Sourcing
```

La estrategia de persistencia se define fuera del Aggregate.

---

# Repository y Domain Events

El Repository persiste Audit como unidad.

Conceptualmente:

```text
RecordAudit
    │
    ▼
Audit Version 1
    +
AuditRecorded
    │
    ▼
Persist Consistently
```

El Repository no inventa:

```text
AuditRecorded
```

por decisión propia.

---

# Optimistic Concurrency

AggregateVersion permite asociar el Domain Event con la evolución
aceptada del Aggregate.

Para la versión 1.0:

```text
Audit.Version = 1

AuditRecorded.AggregateVersion = 1
```

Una operación no confirmada no debe producir un evento exitoso con
una Version inexistente.

---

# Orden

Los Domain Events de una misma identidad deben respetar:

```text
AggregateVersion
```

La versión 1.0 posee una única evolución:

```text
AuditRecorded
AggregateVersion = 1
```

No se exige orden global entre Aggregates Audit distintos.

Debe mantenerse:

```text
Per Aggregate Ordering

≠

Global Ordering
```

---

# Idempotencia

Los consumidores deben poder reconocer que una entrega repetida del
mismo Domain Event no representa un nuevo hecho.

`EventId` permite identificar el hecho.

Debe mantenerse:

```text
Same EventId

=

Same Domain Event
```

La estrategia técnica concreta de idempotencia permanece fuera del
Aggregate.

---

# Correlación entre Source Fact y AuditRecorded

Cuando exista CorrelationId, puede preservarse conceptualmente:

```text
Source Domain Event
    │
    │ CorrelationId
    ▼
RecordAudit
    │
    │ CorrelationId
    ▼
AuditRecorded
```

Esta correlación no fusiona:

```text
Source Aggregate

+

Audit
```

dentro de un único Consistency Boundary.

---

# Causalidad

CausationId puede preservar la relación causal cuando corresponda.

Conceptualmente:

```text
Source Fact

causes

Audit Coordination

causes

RecordAudit

causes

AuditRecorded
```

La representación exacta depende de los contratos aplicables.

---

# Auditoría de Auditoría

AuditRecorded ya es un Domain Event propio de Audit.

Este documento no introduce automáticamente un nuevo Aggregate Audit
para auditar recursivamente cada AuditRecorded.

Debe mantenerse:

```text
AuditRecorded

≠

Automatic Recursive Audit Creation
```

Cualquier necesidad de trazabilidad recursiva requerirá definición
explícita.

---

# Seguridad

Los Domain Events de Audit no deben contener:

- passwords;
- access tokens;
- refresh tokens;
- API keys;
- private keys;
- secretos;
- credenciales;
- configuración sensible de Infrastructure;
- información no necesaria para expresar el hecho.

---

# Datos de Origen

La existencia de información sensible en el Source Domain Event no
obliga a copiarla a AuditRecorded.

Debe mantenerse:

```text
Source Domain Event Payload

≠

AuditRecorded Payload
```

por defecto.

Solo debe conservarse información necesaria conforme al dominio y a
las políticas aplicables.

---

# Logs

Un log técnico no constituye:

```text
AuditRecorded
```

Debe mantenerse:

```text
Log Entry

≠

Audit Domain Event
```

---

# Observability

No pertenecen al Aggregate eventos operacionales como:

```text
AuditMetricCollected

AuditTraceCreated

AuditLogWritten
```

por el solo hecho de ser observados técnicamente.

Observability permanece fuera del dominio Audit.

---

# FIWARE

AuditRecorded no depende de:

```text
FIWARE

NGSI-LD

Context Broker

Orion
```

Una eventual integración debe ocurrir mediante la frontera de
Integration.

Debe mantenerse:

```text
AuditRecorded

≠

FIWARE Message
```

---

# Sistemas Municipales

AuditRecorded no depende de estructuras propietarias de sistemas
municipales.

Cuando exista una necesidad de comunicación externa:

```text
AuditRecorded
    │
    ▼
Integration Boundary
    │
    ▼
External Contract
```

La traducción permanece fuera del Aggregate.

---

# Anti-Corruption Layer

Un evento recibido desde un sistema externo no debe incorporarse
directamente como Domain Event de Audit.

Debe existir una traducción conceptual cuando corresponda.

Debe mantenerse:

```text
External Event

≠

Audit Domain Event
```

salvo que Audit produzca posteriormente su propio hecho mediante
comportamiento válido.

---

# Eventos y Retención

La versión 1.0 no define Domain Events relativos a:

- expiración;
- retención;
- archivado;
- eliminación;
- anonimización;
- redacción.

Ninguna política de retención debe inferirse desde AuditRecorded.

---

# Eventos Históricos

Una vez producido:

```text
AuditRecorded
```

debe preservarse su significado histórico.

Un cambio futuro del dominio no debe reinterpretar retroactivamente
el evento como un hecho diferente.

---

# Regla para Incorporar un Nuevo Domain Event

Un nuevo Domain Event solamente puede incorporarse cuando represente
un hecho relevante propio del Aggregate Audit.

Debe responder afirmativamente:

```text
¿Ocurrió algo relevante dentro de Audit?

¿Puede expresarse en pasado?

¿Posee significado en el Ubiquitous Language?

¿Fue producido por comportamiento válido del Aggregate?

¿No representa solamente una operación técnica?

¿Es coherente con Lifecycle y State Machine?
```

---

# Impacto de un Nuevo Evento

Incorporar un nuevo Domain Event requiere revisar, cuando
corresponda:

```text
DOMAIN-012-Aggregate.md

DOMAIN-012A-Lifecycle.md

DOMAIN-012B-State-Machine.md

DOMAIN-012C-Commands.md

DOMAIN-012D-Domain-Events.md

DOMAIN-012E-Invariants.md

DOMAIN-012F-Permissions.md

DOMAIN-012H-Examples.md

DOMAIN-012I-Versioning.md

DOMAIN-012J-Consistency-Boundary.md

DOMAIN-012K-Integration-Events.md

DOMAIN-012L-Read-Model.md

DOMAIN-012M-Test-Scenarios.md
```

No debe añadirse un evento aisladamente rompiendo coherencia
documental.

---

# Reglas Fundamentales

Los Domain Events de Audit deben cumplir:

1. Representar hechos consumados.
2. Utilizar Ubiquitous Language.
3. Utilizar nombres en pasado.
4. Ser inmutables.
5. Poseer EventId único.
6. Identificar AuditId.
7. Mantener AggregateVersion.
8. Mantener OccurredAt.
9. Mantener CorrelationId cuando corresponda.
10. Mantener CausationId cuando corresponda.
11. Utilizar Payload mínimo significativo.
12. No incluir Aggregates completos.
13. No incluir secretos.
14. No depender de Infrastructure.
15. No reescribir hechos históricos.
16. No producirse ante operaciones rechazadas.
17. Preservar causalidad cuando corresponda.
18. Preservar orden por AggregateVersion.
19. Permitir procesamiento idempotente.
20. Mantener Domain Events separados de Integration Events.
21. Mantener Source Domain Events separados de Audit Domain Events.
22. Mantener SourceAggregateVersion separado de AggregateVersion.
23. No inventar información ausente.
24. No modificar el Source Aggregate.
25. No modificar el Source Domain Event.
26. No utilizar eventos técnicos como Domain Events.
27. No inferir eventos de archivado, eliminación, retry o corrección
    no definidos por el dominio.
28. Mantener coherencia con Lifecycle, State Machine y Commands.

---

# Restricciones

No está permitido:

- modificar AuditRecorded después de ocurrido;
- reutilizar EventId;
- utilizar AuditRecorded como Command;
- publicar AuditRecorded para una operación rechazada;
- producir AuditRecorded antes de validar Invariants;
- utilizar AuditRecorded para modificar directamente otro
  Aggregate;
- copiar un Aggregate externo completo;
- copiar automáticamente el Source Event completo;
- incluir contraseñas;
- incluir tokens;
- incluir claves privadas;
- incluir secretos criptográficos;
- utilizar nombres técnicos como eventos de dominio;
- sobrescribir eventos históricos;
- asumir orden global entre Aggregates Audit;
- acoplar AuditRecorded a FIWARE, brokers o tecnologías específicas;
- convertir silenciosamente AuditRecorded en contrato público;
- reinterpretar Source Domain Event como Audit Domain Event;
- utilizar SourceAggregateVersion como Audit AggregateVersion.

---

# Compatibilidad Arquitectónica

El modelo de Domain Events de Audit es compatible con:

- Domain-Driven Design;
- Tactical DDD;
- Aggregate Pattern;
- Clean Architecture;
- Hexagonal Architecture;
- CQRS;
- Event-Driven Architecture;
- Event Sourcing Compatible;
- Optimistic Concurrency;
- Transactional Outbox;
- consistencia eventual;
- High Cohesion;
- Low Coupling.

Estas compatibilidades no introducen dependencia tecnológica dentro
del Aggregate.

---

# Definición de Éxito

Los Domain Events del Aggregate **Audit** representan oficialmente
los hechos propios de su evolución dentro del ecosistema AURA.

La versión 1.0 define exclusivamente:

```text
AuditRecorded
```

producido por:

```text
RecordAudit
```

mediante:

```text
No Audit → Recorded
```

El modelo garantiza que:

- AuditRecorded representa un hecho consumado;
- RecordAudit representa una intención;
- AuditRecorded pertenece exclusivamente al Aggregate Audit;
- Source Domain Events continúan perteneciendo a sus Aggregates de
  origen;
- Source Domain Event y AuditRecorded no son el mismo evento;
- Audit y AuditRecorded no son el mismo concepto;
- EventId permanece distinto de AuditId;
- AuditId identifica el Aggregate productor;
- AggregateVersion representa la Version resultante de Audit;
- SourceAggregateVersion permanece independiente;
- OccurredAt de AuditRecorded no se confunde con el momento del
  Source Fact;
- CorrelationId y CausationId preservan trazabilidad cuando
  corresponda;
- Payload contiene únicamente información necesaria;
- información faltante no se inventa;
- el Source Event no se modifica;
- el Source Aggregate no se modifica;
- operaciones rechazadas no producen AuditRecorded;
- fallos técnicos no constituyen Domain Events;
- retries técnicos no constituyen Domain Events;
- duplicados técnicos no constituyen nuevos hechos;
- no existen eventos AuditArchived, AuditDeleted, AuditRetried,
  AuditCorrected o equivalentes en la versión 1.0;
- Domain Events permanecen separados de Integration Events;
- la existencia de AuditRecorded no obliga a publicar un
  Integration Event;
- Read Models pueden reaccionar sin adquirir autoridad de escritura;
- Repository persiste el Aggregate pero no inventa eventos;
- Event Sourcing puede reconstruir Audit sin volver a producir
  AuditRecorded;
- CQRS mantiene separación entre Write Side y Read Side;
- FIWARE, sistemas municipales y Infrastructure permanecen fuera
  del dominio;
- cualquier nuevo Domain Event requiere una evolución explícita y
  coordinada.

De esta forma, `DOMAIN-012D-Domain-Events.md` establece los Domain
Events oficiales del Aggregate **Audit** conforme al patrón
consolidado de AURA Core.