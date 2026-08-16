# DOMAIN-012G — Audit Repository Contract

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Audit Management

Aggregate:
Audit

Documentos relacionados:

- DOMAIN-012-Aggregate.md
- DOMAIN-012A-Lifecycle.md
- DOMAIN-012B-State-Machine.md
- DOMAIN-012C-Commands.md
- DOMAIN-012D-Domain-Events.md
- DOMAIN-012E-Invariants.md
- DOMAIN-012F-Permissions.md
- DOMAIN-012I-Versioning.md
- DOMAIN-012J-Consistency-Boundary.md
- DOMAIN-012L-Read-Model.md

---

# Objetivo

Este documento define formalmente el contrato conceptual del
**Repository** correspondiente al Aggregate **Audit**.

El Repository proporciona la abstracción mediante la cual el dominio
puede:

- persistir Audit;
- recuperar Audit;
- verificar existencia;
- obtener una nueva identidad;
- proteger la consistencia de persistencia;
- preservar Versioning;
- detectar conflictos de concurrencia.

El Repository pertenece conceptualmente al dominio como contrato.

Su implementación pertenece a Infrastructure.

Debe mantenerse:

```text
Repository Contract

∈

Domain
```

mientras:

```text
Repository Implementation

∈

Infrastructure
```

---

# Principio Fundamental

Audit constituye una unidad de consistencia.

Por lo tanto:

```text
AuditRepository

persists

Audit Aggregate
```

como una unidad.

El Repository no gobierna el comportamiento del Aggregate.

Debe mantenerse:

```text
Repository

≠

Domain Behavior Authority
```

---

# Responsabilidad

`AuditRepository` es responsable conceptualmente de:

- persistir una unidad Audit válida;
- recuperar una unidad Audit existente;
- verificar la existencia de una identidad;
- proporcionar una nueva identidad cuando corresponda;
- preservar AuditId;
- preservar Version;
- preservar el estado confirmado;
- detectar conflictos de concurrencia;
- abstraer el mecanismo técnico de persistencia.

---

# Responsabilidades Excluidas

El Repository no es responsable de:

- decidir si un hecho es auditable;
- ejecutar RecordAudit;
- decidir Permissions;
- autenticar actores;
- autorizar actores o procesos;
- validar reglas pertenecientes a otros Aggregates;
- crear transiciones de Lifecycle;
- definir State Machine;
- definir Invariants;
- modificar AuditId;
- inventar información de trazabilidad;
- inventar Domain Events;
- publicar Integration Events;
- construir Read Models;
- ejecutar consultas analíticas;
- administrar FIWARE;
- administrar sistemas municipales.

---

# Contrato Conceptual

El contrato conceptual es:

```text
AuditRepository

    save()

    findById()

    exists()

    delete()

    nextIdentity()
```

Estas operaciones representan capacidades conceptuales del
Repository.

No definen:

- lenguaje de programación;
- firma técnica;
- protocolo;
- ORM;
- base de datos;
- estrategia física de almacenamiento.

---

# save()

`save()` persiste una unidad Audit válida.

Conceptualmente:

```text
save(Audit)
```

debe preservar:

- AuditId;
- estado;
- Version;
- CreatedAt;
- UpdatedAt cuando corresponda;
- referencias de origen;
- información de trazabilidad;
- consistencia del Aggregate.

---

# Precondición de save()

El Aggregate entregado a `save()` debe ser válido antes de llegar al
Repository.

Debe mantenerse:

```text
Valid Audit

before

Repository.save()
```

El Repository no corrige un Aggregate inválido.

---

# save() no Ejecuta RecordAudit

El Repository no ejecuta:

```text
RecordAudit
```

por decisión propia.

Conceptualmente:

```text
RecordAudit

    │
    ▼

Audit

    │
    ├── valida State Machine
    ├── valida Invariants
    ├── establece estado válido
    ├── incrementa Version
    └── produce Domain Event
            │
            ▼
         save()
```

---

# save() no Incrementa Version

El Repository no decide el incremento de:

```text
Version
```

La Version resultante pertenece al comportamiento válido del
Aggregate.

Debe mantenerse:

```text
Aggregate Valid Modification

↓

Version Increment

↓

Repository Persists Resulting Version
```

y nunca:

```text
Repository.save()

↓

Decide Domain Version Increment
```

---

# Creación

Para una nueva unidad Audit válida:

```text
No Audit
    │
    ▼
RecordAudit
    │
    ▼
Recorded
Version = 1
    │
    ▼
save()
```

El Repository persiste el resultado ya validado.

---

# Persistencia Atómica

`save()` debe preservar Audit como una única unidad de consistencia.

No debe existir como resultado confirmado:

```text
AuditId persisted

+

State missing
```

ni:

```text
State persisted

+

Invalid Version
```

ni cualquier otra combinación parcial que viole las Invariants.

---

# Estado Persistido

La versión 1.0 solamente permite persistir:

```text
Recorded
```

como estado válido.

El Repository no puede persistir estados inexistentes como:

```text
Draft

Pending

Active

Failed

Cancelled

Archived

Deleted
```

como estados de Audit.

---

# findById()

`findById()` recupera una unidad Audit mediante:

```text
AuditId
```

Conceptualmente:

```text
findById(AuditId)
```

puede producir:

```text
Audit
```

o ausencia de resultado conforme al contrato aplicado.

---

# Recuperación

Una unidad recuperada debe preservar exactamente el estado de
dominio persistido.

La recuperación debe preservar:

- AuditId;
- Recorded;
- Version;
- CreatedAt;
- UpdatedAt cuando corresponda;
- referencias de origen;
- información auditable confirmada.

---

# findById() no Modifica Audit

Recuperar Audit no constituye una modificación.

Debe mantenerse:

```text
findById()

≠

Domain Modification
```

Por lo tanto:

```text
Version
```

no cambia.

---

# findById() no Produce Domain Events

La recuperación no produce:

```text
AuditRecorded
```

ni ningún otro Domain Event.

Debe mantenerse:

```text
Load

≠

New Domain Fact
```

---

# Rehidratación

`findById()` puede requerir reconstruir conceptualmente Audit desde
su representación persistida.

La rehidratación:

- no ejecuta RecordAudit;
- no cambia AuditId;
- no incrementa Version;
- no modifica CreatedAt;
- no genera AuditRecorded;
- no crea nueva intención de dominio.

Debe mantenerse:

```text
Rehydration

≠

Domain Behavior Execution
```

---

# exists()

`exists()` permite verificar conceptualmente si una identidad Audit
ya existe.

Conceptualmente:

```text
exists(AuditId)
```

produce una respuesta de existencia.

No recupera necesariamente todo el Aggregate.

---

# exists() no Modifica Estado

`exists()` es una operación de verificación.

No puede:

- cambiar Recorded;
- incrementar Version;
- modificar timestamps;
- producir Domain Events.

---

# nextIdentity()

`nextIdentity()` proporciona conceptualmente una nueva:

```text
AuditId
```

válida para identificar una unidad Audit nueva.

Debe garantizar:

```text
New AuditId

≠

Existing AuditId
```

dentro del espacio de identidad correspondiente.

---

# nextIdentity() no Crea Audit

Obtener una identidad no equivale a crear un Aggregate.

Debe mantenerse:

```text
nextIdentity()

≠

RecordAudit
```

y:

```text
New AuditId

≠

Existing Audit
```

hasta que el comportamiento válido del dominio cree la unidad
correspondiente.

---

# Identidad

El Repository debe preservar:

```text
AuditId
```

exactamente.

No puede:

- sustituirlo;
- reasignarlo;
- derivarlo de SourceAggregateId;
- derivarlo de SourceEventId como equivalencia obligatoria;
- reutilizarlo para otra unidad Audit.

---

# SourceAggregateId

Cuando Audit conserve:

```text
SourceAggregateId
```

el Repository debe persistir dicha referencia como parte del estado
de Audit.

No puede utilizarla como sustituto de:

```text
AuditId
```

---

# SourceEventId

Cuando exista:

```text
SourceEventId
```

el Repository puede preservarlo como parte de la representación
Audit.

Debe mantenerse:

```text
SourceEventId

≠

AuditId
```

---

# SourceAggregateVersion

Cuando Audit preserve:

```text
SourceAggregateVersion
```

el Repository debe mantenerla separada de:

```text
Audit.Version
```

Debe mantenerse:

```text
SourceAggregateVersion

≠

Audit.Version
```

semánticamente.

---

# Version

El Repository debe persistir la Version producida por el Aggregate.

Conceptualmente:

```text
Audit.Version = N
```

debe recuperarse posteriormente como:

```text
Audit.Version = N
```

salvo que exista una nueva modificación válida confirmada.

---

# Optimistic Concurrency

Audit utiliza el patrón consolidado de:

```text
Optimistic Concurrency Control
```

Antes de confirmar una escritura sobre una unidad existente debe
cumplirse:

```text
ExpectedVersion

=

PersistedVersion
```

---

# ConcurrencyConflict

Cuando:

```text
ExpectedVersion

≠

PersistedVersion
```

debe producirse:

```text
ConcurrencyConflict
```

La escritura obsoleta no debe sobrescribir una modificación ya
confirmada.

---

# ConcurrencyConflict no Modifica Audit

Un conflicto de concurrencia no constituye una modificación válida
del Aggregate.

No debe producir:

- nueva Version confirmada;
- nuevo estado;
- cambio de UpdatedAt;
- Domain Event de éxito.

---

# Creación Concurrente

Dos intentos incompatibles de persistir la misma:

```text
AuditId
```

como una nueva identidad no deben producir dos Aggregates distintos
bajo la misma identidad.

Debe mantenerse:

```text
One AuditId

=

One Audit Aggregate Identity
```

---

# DuplicateAuditId

Cuando una nueva unidad intenta utilizar una identidad ya existente:

```text
AuditId
```

el Repository debe impedir la duplicación incompatible.

Conceptualmente puede representar:

```text
DuplicateAuditId
```

como error del contrato.

---

# Idempotencia y Repository

El Repository no redefine la semántica de idempotencia del proceso
que origina RecordAudit.

Una entrega técnica duplicada:

```text
Duplicate Technical Delivery
```

no se convierte automáticamente en:

```text
New Audit
```

por decisión del Repository.

---

# SourceEventId e Idempotencia

Cuando SourceEventId esté disponible puede formar parte de la
información utilizada por capas externas para reconocer un hecho
previamente procesado.

Este documento no convierte:

```text
SourceEventId
```

en AuditId ni establece una estrategia técnica concreta de
deduplicación.

---

# delete()

El contrato conceptual conserva:

```text
delete()
```

como capacidad de persistencia conforme al patrón consolidado de
Repository Contracts de AURA.

Su existencia no implica que exista un Command de dominio:

```text
DeleteAudit
```

ni un estado:

```text
Deleted
```

---

# delete() no es Lifecycle

Debe mantenerse:

```text
Repository.delete()

≠

Audit Lifecycle Transition
```

La versión 1.0 no define:

```text
Recorded → Deleted
```

---

# Uso de delete()

La eliminación física solamente puede utilizarse cuando una regla
externa de persistencia, retención o cumplimiento explícitamente
aplicable lo permita.

El Repository no decide esa política.

Debe mantenerse:

```text
Repository Capability

≠

Domain Permission to Delete
```

---

# Retención

El Repository no define:

- período de retención;
- expiración;
- archivado;
- eliminación automática;
- anonimización;
- redacción.

Estas reglas requieren definición explícita fuera del Repository
Contract cuando correspondan.

---

# Historial

El Repository debe preservar el significado del estado histórico
confirmado de Audit.

No puede modificar una representación persistida para reinterpretar
retrospectivamente el hecho auditado.

Debe mantenerse:

```text
Persistence

≠

Historical Rewrite Authority
```

---

# Repository y Source Fact

El Repository de Audit no persiste el Source Aggregate como parte de
la misma unidad.

Debe mantenerse:

```text
AuditRepository

≠

SourceAggregateRepository
```

---

# Repository y Source Domain Event

Cuando Audit preserve referencias provenientes de un Source Domain
Event, el Repository no adquiere ownership sobre el evento original.

Debe mantenerse:

```text
Persisted Audit Representation

≠

Source Domain Event Ownership
```

---

# Aggregate Boundary

`AuditRepository` opera sobre:

```text
Audit
```

No sobre:

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

como parte de una misma operación de Repository.

---

# No Multi-Aggregate Repository

No debe existir dentro del contrato:

```text
saveAuditAndAssembly()

saveAuditAndNotification()

saveAuditAndDocument()

saveAuditAndVoting()
```

como operaciones pertenecientes al Repository del Aggregate Audit.

Debe mantenerse:

```text
One Repository Contract

per

Aggregate Boundary
```

---

# No Transacción Distribuida Obligatoria

El Repository de Audit no requiere una transacción atómica con el
Repository de otro Aggregate.

Debe mantenerse:

```text
Audit Persistence Transaction

≠

Source Aggregate Persistence Transaction
```

---

# Consistencia Eventual

Puede existir una ventana temporal donde:

```text
Source Fact Confirmed

+

Audit Not Yet Persisted
```

sin violar el Consistency Boundary.

Audit será persistido posteriormente mediante su propia transacción.

---

# Fallo de Persistencia

Un error técnico durante persistencia puede representarse
conceptualmente como:

```text
PersistenceFailure
```

Este error:

- no es AuditStatus;
- no crea Failed;
- no cambia el Source Aggregate;
- no revierte el Source Fact;
- no constituye AuditRecorded confirmado si el commit no ocurrió.

---

# RepositoryUnavailable

Si la implementación del Repository no está disponible, puede
producirse conceptualmente:

```text
RepositoryUnavailable
```

Este error pertenece al contrato de persistencia.

No representa un estado del Aggregate.

---

# AuditNotFound

Cuando:

```text
findById(AuditId)
```

no encuentra una unidad existente, el contrato puede representar:

```text
AuditNotFound
```

conforme al contexto de uso.

La ausencia no crea ni modifica Audit.

---

# Errores Conceptuales

El Repository Contract reconoce conceptualmente errores como:

```text
AuditNotFound

DuplicateAuditId

ConcurrencyConflict

PersistenceFailure

RepositoryUnavailable
```

Estos errores no son Domain Events del Aggregate.

---

# Error no es Estado

Debe mantenerse:

```text
Repository Error

≠

AuditStatus
```

Por lo tanto:

```text
PersistenceFailure

≠

Recorded → Failed
```

porque Failed no pertenece al Lifecycle.

---

# Error no es Domain Event

Errores como:

```text
AuditNotFound

DuplicateAuditId

ConcurrencyConflict

PersistenceFailure

RepositoryUnavailable
```

no constituyen automáticamente Domain Events de Audit.

---

# AuditRecorded

El Repository no inventa:

```text
AuditRecorded
```

El evento solamente puede originarse como consecuencia del
comportamiento válido:

```text
RecordAudit
```

dentro del Aggregate.

---

# Persistencia y Domain Event

Conceptualmente:

```text
RecordAudit
    │
    ▼
Audit Recorded
Version = 1
    +
AuditRecorded
    │
    ▼
Repository.save()
    │
    ▼
Commit
```

El Repository participa en la persistencia del resultado.

No define el significado del Domain Event.

---

# Confirmación

Un Domain Event asociado a una modificación solamente puede
considerarse externamente publicable después de una persistencia
confirmada conforme al flujo correspondiente.

Debe mantenerse:

```text
Aggregate Commit

before

External Publication
```

---

# Domain Event no es Registro de Repository

Debe mantenerse:

```text
AuditRecorded

≠

Repository Record
```

El Domain Event representa un hecho del dominio.

La representación física de persistencia pertenece a
Infrastructure.

---

# Transactional Outbox

Cuando la arquitectura utilice:

```text
Transactional Outbox
```

el Aggregate y su Repository no conocen la implementación concreta
de la Outbox.

Debe mantenerse:

```text
AuditRepository Contract

≠

Outbox Implementation
```

La coordinación técnica pertenece a Application e Infrastructure.

---

# Event Sourcing

El Repository Contract es compatible conceptualmente con:

```text
Event Sourcing
```

sin imponerlo.

Una implementación Event Sourced puede reconstruir Audit desde sus
Domain Events oficialmente definidos.

---

# State Persistence

El Repository Contract también es compatible con:

```text
State Persistence + Domain Events
```

La elección entre estrategias de persistencia no pertenece al
Aggregate.

---

# Event Store

La versión 1.0 no exige:

```text
Event Store
```

como tecnología obligatoria.

Debe mantenerse:

```text
Event Sourcing Compatible

≠

Event Sourcing Mandatory
```

---

# Rehidratación con Event Sourcing

Si el Repository reconstruye Audit mediante:

```text
AuditRecorded
```

debe obtener:

```text
State = Recorded

Version = 1
```

conforme al historial.

La reconstrucción no produce un nuevo Domain Event.

---

# Replay

El Repository no debe utilizar replay como una nueva modificación de
dominio.

Debe mantenerse:

```text
Replay

≠

RecordAudit
```

y:

```text
Replay

≠

Version Increment
```

---

# CQRS

En CQRS, `AuditRepository` pertenece conceptualmente al Write Side.

Debe mantenerse:

```text
Write Repository

≠

Read Query Model
```

---

# Consultas de Negocio

Consultas como:

- buscar Audits por SourceAggregateId;
- buscar por SourceEventId;
- buscar por ActorId;
- buscar por CorrelationId;
- buscar por CausationId;
- filtrar por fecha;
- obtener historial;
- realizar reporting;
- realizar analytics;

pertenecen al Read Side.

No deben incorporarse al Repository del Aggregate solamente por
conveniencia de consulta.

---

# Aggregate Repository versus Read Query Repository

Debe mantenerse:

```text
AuditRepository

≠

Audit Read Query Repository
```

El primero soporta persistencia del Aggregate.

El segundo, cuando exista, soporta necesidades de lectura.

---

# Read Models

Los Read Models se definen en:

```text
DOMAIN-012L-Read-Model.md
```

El Repository del Aggregate no debe convertirse en el mecanismo
principal para consultas históricas o analíticas.

---

# Listados

La versión 1.0 no requiere que:

```text
AuditRepository
```

exponga operaciones de listado masivo como responsabilidad del
Aggregate.

Los listados pertenecen al Read Side.

---

# Filtros

Filtros por:

```text
SourceAggregateType

SourceEventType

ActorId

OccurredAt

CorrelationId

CausationId
```

son necesidades de consulta.

No constituyen comportamiento de escritura del Aggregate.

---

# Analytics

El Repository del Aggregate no es:

```text
Analytics Repository
```

ni:

```text
Reporting Engine
```

Las necesidades analíticas pueden utilizar Read Models y
proyecciones especializadas.

---

# Repository y Permissions

El Repository no decide:

```text
Permission
```

ni:

```text
Authorization
```

Debe mantenerse:

```text
Repository

≠

Authorization Authority
```

---

# Repository y Authentication

El Repository no autentica actores.

No valida:

- passwords;
- tokens;
- sesiones;
- OAuth;
- JWT.

Authentication permanece fuera del Repository Contract de dominio.

---

# Repository y Security

La implementación debe respetar el Security Model aplicable.

Sin embargo, el Repository Contract no incorpora:

- claves;
- credenciales;
- tokens;
- secretos;
- certificados privados.

---

# Repository y AuditId

Conocer AuditId no permite evitar el Aggregate.

El Repository no debe exponerse conceptualmente como una vía para
realizar modificaciones directas del estado interno.

Debe mantenerse:

```text
Repository Access

≠

Aggregate Mutation Authority
```

---

# Repository y Infrastructure

La implementación concreta puede utilizar diferentes tecnologías.

El dominio no conoce:

```text
SQL

PostgreSQL

MongoDB

EventStoreDB

ORM

Filesystem

HTTP

REST

GraphQL

Redis

Cloud Storage
```

ni tecnologías equivalentes.

---

# Repository y Serialización

La forma de serializar Audit pertenece a Infrastructure.

El contrato no define:

```text
JSON

BSON

Avro

Protobuf

Binary Format
```

como parte del dominio.

---

# Repository y FIWARE

`AuditRepository` no es un:

```text
FIWARE Repository
```

ni depende de:

```text
NGSI-LD

Context Broker

Orion
```

La persistencia del Aggregate y la integración FIWARE son
responsabilidades distintas.

---

# Repository y Sistemas Municipales

AuditRepository no persiste directamente el Aggregate mediante
contratos municipales como parte de su definición de dominio.

La interacción con sistemas externos pertenece a Integration.

---

# Anti-Corruption Layer

Una representación externa de Audit no debe utilizarse directamente
como modelo de persistencia del dominio si su semántica no coincide
con AURA.

Debe mantenerse:

```text
External Persistence Model

≠

Audit Domain Model
```

La traducción pertenece a las capas correspondientes.

---

# Independencia Tecnológica

AuditRepository no depende conceptualmente de:

```text
Django ORM

SQLAlchemy

Hibernate

Entity Framework

Prisma

MongoDB Driver

PostgreSQL Driver

FIWARE SDK
```

ni frameworks equivalentes.

---

# Persistencia de Value Objects

Si Audit incorpora Value Objects oficialmente definidos, el
Repository debe preservar sus valores como parte del estado del
Aggregate.

No puede modificar su semántica.

---

# Persistencia de Internal Entities

Si en una evolución futura Audit incorpora Internal Entities, estas
deben persistirse dentro del mismo Consistency Boundary.

No deben convertirse en Aggregates independientes por decisión del
Repository.

---

# Persistencia Parcial

No está permitido persistir una parte de Audit de forma que otra
parte necesaria para sus Invariants quede inconsistente.

Debe mantenerse:

```text
Aggregate Persistence

=

Consistent Unit Persistence
```

---

# Repository no Repara Aggregate

Si Audit llega al Repository en un estado inválido:

```text
Repository

≠

Domain Repair Service
```

El Repository no debe:

- completar campos faltantes;
- inventar Source References;
- cambiar State;
- cambiar Version;
- modificar timestamps;
- sustituir AuditId.

---

# Repository no Infiere Información

El Repository no puede inventar:

```text
ActorId

CorrelationId

CausationId

SourceEventId

SourceAggregateVersion
```

cuando el dominio no los posee.

---

# Repository y Historical Meaning

La serialización o reconstrucción debe preservar el significado de
la información auditada.

Debe mantenerse:

```text
Persist

+

Recover

=

Same Domain Meaning
```

---

# Round Trip Conceptual

Conceptualmente:

```text
Audit A
    │
    ▼
  save()
    │
    ▼
Persistence
    │
    ▼
findById(AuditId)
    │
    ▼
Audit A
```

debe preservar:

```text
Identity

State

Version

Traceability Meaning
```

---

# Repository y UpdatedAt

El Repository persiste:

```text
UpdatedAt
```

cuando forme parte del estado válido.

No decide cambiarlo.

Debe mantenerse:

```text
Repository.save()

≠

Domain UpdatedAt Mutation
```

---

# Repository y CreatedAt

El Repository debe preservar:

```text
CreatedAt
```

exactamente como parte del estado del Aggregate.

No debe reemplazarlo por el momento técnico de escritura.

Debe mantenerse:

```text
Audit.CreatedAt

≠

Database Write Timestamp
```

semánticamente.

---

# Repository y OccurredAt

Cuando Audit preserve información relativa al momento del Source
Fact:

```text
SourceOccurredAt
```

el Repository debe conservar su significado.

No debe sustituirlo por:

```text
CreatedAt
```

ni por un timestamp técnico de persistencia.

---

# Timestamps Técnicos

Timestamps propios de Infrastructure como:

```text
InsertedAt

ReplicatedAt

IndexedAt

BackedUpAt
```

no deben convertirse automáticamente en atributos del Aggregate.

---

# Cache

Una cache puede existir como optimización técnica.

No constituye fuente de verdad del Aggregate por definición de
dominio.

Debe mantenerse:

```text
Cache

≠

Audit Domain Authority
```

---

# Replica

La utilización técnica de réplicas no cambia:

- AuditId;
- State;
- Version;
- Invariants;
- Consistency Boundary.

La estrategia pertenece a Infrastructure.

---

# Backup

Backup y restore son responsabilidades operacionales.

No constituyen:

- Commands;
- Domain Events;
- estados;
- transiciones.

---

# Migration

Migraciones físicas de almacenamiento no constituyen comportamiento
del Aggregate.

Debe mantenerse:

```text
Persistence Migration

≠

Domain State Transition
```

---

# Repository y Performance

Optimizar persistencia no puede:

- evitar Invariants;
- evitar Versioning;
- modificar identidad;
- ampliar Consistency Boundary;
- fusionar Aggregates.

Debe mantenerse:

```text
Persistence Optimization

≠

Domain Rule Bypass
```

---

# Repository y Testabilidad

El contrato permite verificar conceptualmente:

- persistencia de Audit válido;
- recuperación por AuditId;
- preservación de Version;
- preservación de State;
- preservación de timestamps;
- preservación de Source References;
- inexistencia;
- identidad duplicada;
- conflictos de concurrencia;
- fallo de persistencia;
- indisponibilidad del Repository.

Los escenarios completos se definen en:

```text
DOMAIN-012M-Test-Scenarios.md
```

---

# Flujo de Creación

```text
RecordAudit
    │
    ▼
Audit
    │
    ├── AuditId
    ├── State = Recorded
    ├── Version = 1
    ├── CreatedAt
    └── AuditRecorded
            │
            ▼
    AuditRepository.save()
            │
            ▼
          Commit
```

---

# Flujo de Recuperación

```text
AuditId
    │
    ▼
AuditRepository.findById()
    │
    ▼
Rehydrate Audit
    │
    ▼
Recorded
Same Version
Same Identity
```

---

# Flujo de Concurrencia

Conceptualmente:

```text
PersistedVersion = N

ExpectedVersion = N
        │
        ▼
   Write Allowed
```

mientras:

```text
PersistedVersion = N

ExpectedVersion = N - 1
        │
        ▼
ConcurrencyConflict
```

---

# Flujo de Error

```text
Valid Audit
    │
    ▼
Repository.save()
    │
    ▼
PersistenceFailure
```

no debe producir:

```text
AuditStatus = Failed
```

ni modificar el Source Aggregate.

---

# Reglas Fundamentales

El Repository Contract de Audit debe cumplir:

1. AuditRepository pertenece conceptualmente al dominio como
   abstracción.
2. Su implementación pertenece a Infrastructure.
3. El Repository persiste Audit como unidad.
4. El Repository no define comportamiento del Aggregate.
5. El contrato oficial contiene save(), findById(), exists(),
   delete() y nextIdentity().
6. save() recibe un Aggregate ya válido.
7. save() no ejecuta RecordAudit.
8. save() no decide el incremento de Version.
9. El Aggregate incrementa Version mediante comportamiento válido.
10. El Repository persiste la Version resultante.
11. Recorded es el único estado persistido válido en versión 1.0.
12. findById() recupera por AuditId.
13. findById() no modifica Audit.
14. findById() no incrementa Version.
15. findById() no produce Domain Events.
16. Rehidratación no ejecuta comportamiento nuevo.
17. exists() no modifica el Aggregate.
18. nextIdentity() proporciona una nueva identidad.
19. nextIdentity() no crea Audit.
20. AuditId debe preservarse exactamente.
21. SourceAggregateId no sustituye AuditId.
22. SourceEventId no sustituye AuditId.
23. SourceAggregateVersion permanece separado de Audit.Version.
24. Version persistida debe recuperarse sin alteración.
25. Optimistic Concurrency protege escrituras.
26. ExpectedVersion debe coincidir con PersistedVersion.
27. Una versión obsoleta produce ConcurrencyConflict.
28. Una escritura obsoleta no sobrescribe estado confirmado.
29. Una identidad duplicada produce conflicto de identidad.
30. DuplicateAuditId no es estado del Aggregate.
31. delete() no constituye transición del Lifecycle.
32. DeleteAudit no existe como Command versión 1.0.
33. Deleted no existe como estado versión 1.0.
34. Repository no decide políticas de retención.
35. Repository no reescribe el significado histórico.
36. AuditRepository no persiste otros Aggregates en la misma unidad.
37. No existe Multi-Aggregate Repository.
38. No existe transacción distribuida obligatoria.
39. Puede existir consistencia eventual con el Source Aggregate.
40. PersistenceFailure no equivale a AuditStatus.
41. RepositoryUnavailable no equivale a AuditStatus.
42. AuditNotFound no modifica el Aggregate.
43. Errores de Repository no son Domain Events.
44. Repository no inventa AuditRecorded.
45. Domain Event se origina en comportamiento del Aggregate.
46. Publicación externa ocurre después del commit correspondiente.
47. Transactional Outbox permanece fuera del contrato del Aggregate.
48. Event Sourcing es compatible pero no obligatorio.
49. State Persistence también es compatible.
50. Event Store no es obligatorio.
51. Replay no ejecuta RecordAudit.
52. Replay no incrementa Version.
53. AuditRepository pertenece al Write Side.
54. Consultas históricas y analíticas pertenecen al Read Side.
55. AuditRepository no es Query Repository.
56. Listados y filtros no son comportamiento del Aggregate.
57. Repository no decide Permissions.
58. Repository no autentica actores.
59. Repository no almacena credenciales como parte del dominio.
60. Acceso técnico al Repository no concede autoridad de dominio.
61. La implementación permanece independiente de tecnologías
    concretas.
62. FIWARE no forma parte del Repository Contract.
63. Sistemas municipales permanecen fuera del Repository Contract.
64. Value Objects se preservan dentro del Aggregate cuando existan.
65. Internal Entities permanecen dentro del mismo Consistency
    Boundary cuando existan.
66. Persistencia parcial no puede violar Invariants.
67. Repository no repara Aggregates inválidos.
68. Repository no inventa información faltante.
69. Persistir y recuperar debe preservar significado de dominio.
70. CreatedAt no se sustituye por timestamp técnico.
71. UpdatedAt no es decidido por el Repository.
72. SourceOccurredAt no se sustituye por timestamps técnicos.
73. Cache no es autoridad de dominio.
74. Replica, Backup y Migration no son comportamiento del Aggregate.
75. Optimizaciones de persistencia no pueden evitar reglas de
    dominio.

---

# Restricciones

No está permitido:

- utilizar Repository como servicio de negocio;
- ejecutar RecordAudit desde el Repository;
- decidir Permissions desde el Repository;
- modificar AuditId;
- sustituir AuditId por SourceAggregateId;
- sustituir AuditId por SourceEventId;
- incrementar Version desde save();
- cambiar State desde Repository;
- persistir estados no definidos;
- inventar ActorId;
- inventar CorrelationId;
- inventar CausationId;
- inventar SourceEventId;
- corregir Invariants;
- producir AuditRecorded desde Repository;
- utilizar errores técnicos como AuditStatus;
- sobrescribir una escritura confirmada con una Version obsoleta;
- fusionar Audit con otro Aggregate;
- crear un Multi-Aggregate Repository;
- exigir transacción distribuida con el Source Aggregate;
- utilizar delete() como transición de Lifecycle;
- inferir políticas de retención desde delete();
- utilizar Aggregate Repository para Analytics;
- utilizar Aggregate Repository como motor de búsqueda;
- permitir que Infrastructure determine reglas de dominio;
- convertir timestamps técnicos en atributos de Audit
  automáticamente;
- convertir una cache en fuente autoritativa del dominio;
- acoplar el Repository Contract a FIWARE, ORM, base de datos o
  framework concreto.

---

# Compatibilidad Arquitectónica

El Repository Contract de Audit es compatible con:

- Domain-Driven Design;
- Aggregate Pattern;
- Repository Pattern;
- Clean Architecture;
- Hexagonal Architecture;
- SOLID;
- Dependency Inversion Principle;
- CQRS;
- Event-Driven Architecture;
- Event Sourcing Compatible;
- Optimistic Concurrency Control;
- Transactional Outbox;
- Persistence Ignorance;
- consistencia eventual;
- High Cohesion;
- Low Coupling.

Estas compatibilidades no introducen dependencias tecnológicas en el
dominio.

---

# Definición de Éxito

El Repository Contract del Aggregate **Audit** proporciona una
abstracción de persistencia coherente con el patrón consolidado de
AURA.

El contrato oficial define:

```text
AuditRepository

    save()

    findById()

    exists()

    delete()

    nextIdentity()
```

y garantiza que:

- Audit se persiste como una unidad de consistencia;
- el Repository no gobierna comportamiento de dominio;
- RecordAudit se ejecuta antes de persistir el resultado;
- AuditId permanece único e inmutable;
- SourceAggregateId y SourceEventId permanecen referencias
  independientes;
- SourceAggregateVersion permanece distinta de Audit.Version;
- Recorded es el único estado persistido oficial;
- Version es incrementada por el Aggregate y no por el Repository;
- la Version resultante se preserva durante persistencia;
- findById() recupera sin modificar el Aggregate;
- exists() no altera estado;
- nextIdentity() no crea Audit;
- Optimistic Concurrency protege escrituras;
- conflictos de Version producen ConcurrencyConflict;
- identidades duplicadas no pueden sobrescribir una unidad
  existente;
- errores de persistencia no se convierten en estados de Audit;
- Repository no inventa AuditRecorded;
- Repository no corrige Invariants;
- Repository no inventa información auditable;
- Source Aggregate y Audit permanecen transaccionalmente separados;
- consistencia externa puede ser eventual;
- delete() no constituye un Command ni una transición de Lifecycle;
- políticas de retención permanecen fuera del Repository Contract;
- Event Sourcing permanece compatible sin quedar impuesto;
- Read Models y consultas históricas permanecen separados del
  Repository del Write Model;
- Authentication y Authorization permanecen fuera del Repository;
- FIWARE y sistemas municipales permanecen fuera del contrato;
- persistir y recuperar preserva identidad, estado, Version y
  significado histórico;
- Infrastructure puede cambiar sin modificar las reglas
  conceptuales del dominio.

De esta forma, `DOMAIN-012G-Repository-Contract.md` establece el
Repository Contract oficial del Aggregate **Audit** conforme al
patrón consolidado de AURA Core.