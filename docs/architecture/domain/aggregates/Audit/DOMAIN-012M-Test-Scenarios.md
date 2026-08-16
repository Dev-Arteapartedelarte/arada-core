# DOMAIN-012M — Audit Test Scenarios

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
- DOMAIN-012G-Repository-Contract.md
- DOMAIN-012H-Examples.md
- DOMAIN-012I-Versioning.md
- DOMAIN-012J-Consistency-Boundary.md
- DOMAIN-012K-Integration-Events.md
- DOMAIN-012L-Read-Model.md
- DOMAIN-012N-Performance-Rules.md
- DOMAIN-012O-Security-Model.md
- DOMAIN-012P-Extension-Points.md

---

# Objetivo

Este documento define formalmente los **Test Scenarios**
conceptuales del Aggregate **Audit**.

Los escenarios verifican que el comportamiento del dominio preserve:

- Lifecycle;
- State Machine;
- Commands;
- Domain Events;
- Invariants;
- Permissions;
- Repository Contract;
- Versioning;
- Consistency Boundary;
- Integration Events;
- Read Models;
- Security.

Los escenarios representan reglas conceptuales del dominio.

No definen:

- framework de testing;
- lenguaje de programación;
- librería;
- runner;
- infraestructura;
- base de datos;
- broker;
- API.

---

# Principio Fundamental

Todo escenario debe preservar:

```text
Given

When

Then
```

donde:

```text
Given

=

Valid Initial Domain Context
```

```text
When

=

Domain Intent or Relevant Interaction
```

```text
Then

=

Expected Domain Result
```

---

# Alcance

Los Test Scenarios deben validar exclusivamente reglas oficialmente
definidas para Audit versión 1.0.

No deben introducir:

- nuevos estados;
- nuevos Commands;
- nuevos Domain Events;
- nuevas Permissions;
- nuevas políticas de retención;
- nuevas reglas de eliminación;
- nuevas reglas de anonimización;
- nuevas estrategias técnicas.

---

# Estado Oficial

La versión 1.0 define:

```text
Recorded
```

como único estado persistido.

Debe verificarse:

```text
No Audit → Recorded
```

como única transición oficial.

---

# Command Oficial

La versión 1.0 define:

```text
RecordAudit
```

como único Command oficial.

---

# Domain Event Oficial

La versión 1.0 define:

```text
AuditRecorded
```

como único Domain Event oficial.

---

# Escenario TS-001 — RecordAudit válido

Given:

```text
No Audit

Confirmed Auditable Fact

Valid AuditId

Authorized Request
```

When:

```text
RecordAudit
```

Then:

```text
Audit exists

AuditStatus = Recorded

Version = 1

AuditRecorded produced
```

---

# Escenario TS-002 — Creación establece AuditId

Given:

```text
AuditId = AUD-001
```

When:

```text
RecordAudit
```

succeeds.

Then:

```text
Audit.AuditId = AUD-001
```

---

# Escenario TS-003 — AuditId permanece inmutable

Given:

```text
AuditId = AUD-001

AuditStatus = Recorded
```

When:

```text
Change AuditId to AUD-002
```

is attempted.

Then:

```text
Rejected

AuditId = AUD-001
```

---

# Escenario TS-004 — AuditId no puede ser nulo

Given:

```text
No Audit
```

When:

```text
RecordAudit(
    AuditId = null
)
```

Then:

```text
Rejected

No Audit

No AuditRecorded
```

---

# Escenario TS-005 — AuditId y SourceAggregateId son distintos

Given:

```text
AuditId = AUD-010

SourceAggregateId = ASM-010
```

When:

```text
RecordAudit
```

succeeds.

Then:

```text
AuditId = AUD-010

SourceAggregateId = ASM-010
```

and conceptually:

```text
AuditId

≠

SourceAggregateId
```

---

# Escenario TS-006 — AuditId y SourceEventId son distintos

Given:

```text
AuditId = AUD-011

SourceEventId = EVT-100
```

When:

```text
RecordAudit
```

succeeds.

Then:

```text
AuditId = AUD-011

SourceEventId = EVT-100
```

and:

```text
AuditId

≠

SourceEventId
```

---

# Escenario TS-007 — AuditId y Domain Event EventId son distintos

Given:

```text
AuditId = AUD-012
```

When:

```text
RecordAudit
```

succeeds and produces:

```text
AuditRecorded
```

Then:

```text
AuditRecorded.EventId

≠

AuditId
```

---

# Escenario TS-008 — Hecho no confirmado

Given:

```text
No confirmed source fact
```

When:

```text
RecordAudit
```

Then:

```text
Rejected

No Audit

No Version

No AuditRecorded
```

---

# Escenario TS-009 — Intento futuro no es hecho

Given:

```text
Future Intent
```

When:

```text
RecordAudit
```

attempts to represent it as already occurred.

Then:

```text
Rejected
```

because:

```text
Future Intent

≠

Confirmed Auditable Fact
```

---

# Escenario TS-010 — Source Command no es automáticamente auditable

Given:

```text
StartAssembly
```

as an external Command.

When:

```text
RecordAudit
```

is attempted before the corresponding fact exists.

Then:

```text
Rejected
```

because:

```text
Source Command

≠

Confirmed Source Fact
```

---

# Escenario TS-011 — Source Domain Event confirmado

Given:

```text
AssemblyStarted
```

confirmed by Assembly.

When:

```text
RecordAudit
```

is validly executed.

Then:

```text
AuditStatus = Recorded

AuditRecorded produced
```

while:

```text
AssemblyStarted

≠

AuditRecorded
```

---

# Escenario TS-012 — Source Aggregate no se modifica

Given:

```text
AssemblyStatus = InProgress

Assembly.Version = 8
```

When:

```text
RecordAudit
```

succeeds.

Then:

```text
AssemblyStatus = InProgress

Assembly.Version = 8
```

remains unchanged by Audit.

---

# Escenario TS-013 — Fallo de Audit no revierte Source Aggregate

Given:

```text
Source Fact committed
```

When:

```text
Audit processing fails
```

Then:

```text
Source Fact remains committed
```

and:

```text
No Source Aggregate rollback
```

---

# Escenario TS-014 — SourceAggregateVersion preservada

Given:

```text
SourceAggregateVersion = 8
```

When:

```text
RecordAudit
```

succeeds.

Then:

```text
SourceAggregateVersion = 8

Audit.Version = 1
```

---

# Escenario TS-015 — SourceAggregateVersion no es Audit.Version

Given:

```text
SourceAggregateVersion = 8

Audit.Version = 1
```

Then:

```text
SourceAggregateVersion

≠

Audit.Version
```

semantically.

---

# Escenario TS-016 — Coincidencia numérica no implica identidad

Given:

```text
SourceAggregateVersion = 1

Audit.Version = 1
```

Then:

```text
Numeric Equality

≠

Semantic Identity
```

---

# Escenario TS-017 — ActorId disponible

Given:

```text
ActorId = CIT-100
```

is present in the source contract.

When:

```text
RecordAudit
```

succeeds.

Then:

```text
ActorId = CIT-100
```

may be preserved.

---

# Escenario TS-018 — ActorId ausente

Given:

```text
ActorId not provided
```

When:

```text
RecordAudit
```

succeeds under a contract where ActorId is optional.

Then:

```text
No fabricated ActorId
```

---

# Escenario TS-019 — ActorId inventado

Given:

```text
Source contract has no ActorId
```

When:

```text
ActorId = SYSTEM
```

is fabricated as source information.

Then:

```text
Rejected
```

---

# Escenario TS-020 — CorrelationId disponible

Given:

```text
CorrelationId = FLOW-100
```

When:

```text
RecordAudit
```

succeeds.

Then:

```text
CorrelationId = FLOW-100
```

may be preserved without sharing Consistency Boundary.

---

# Escenario TS-021 — CorrelationId ausente

Given:

```text
CorrelationId not provided
```

When:

```text
RecordAudit
```

succeeds.

Then:

```text
No fabricated CorrelationId
```

---

# Escenario TS-022 — CausationId disponible

Given:

```text
CausationId = EVT-200
```

When:

```text
RecordAudit
```

succeeds.

Then:

```text
CausationId = EVT-200
```

may be preserved.

---

# Escenario TS-023 — CausationId ausente

Given:

```text
CausationId not provided
```

When:

```text
RecordAudit
```

succeeds.

Then:

```text
No fabricated CausationId
```

---

# Escenario TS-024 — SourceEventId ausente

Given:

```text
SourceEventId not available
```

under a valid source contract.

When:

```text
RecordAudit
```

succeeds.

Then:

```text
No fabricated SourceEventId
```

---

# Escenario TS-025 — SourceOccurredAt preservado

Given:

```text
SourceOccurredAt = T1
```

When:

```text
RecordAudit
```

succeeds at:

```text
CreatedAt = T2
```

Then:

```text
SourceOccurredAt = T1

CreatedAt = T2
```

remain conceptually distinct.

---

# Escenario TS-026 — AuditRecorded.OccurredAt es distinto del Source Fact

Given:

```text
SourceOccurredAt = T1
```

When:

```text
AuditRecorded
```

occurs at:

```text
T2
```

Then:

```text
AuditRecorded.OccurredAt = T2
```

and:

```text
SourceOccurredAt

≠

AuditRecorded.OccurredAt
```

semantically.

---

# Escenario TS-027 — CreatedAt es obligatorio

Given:

```text
Valid RecordAudit
```

When:

```text
Audit becomes Recorded
```

Then:

```text
CreatedAt exists
```

---

# Escenario TS-028 — CreatedAt permanece inmutable

Given:

```text
Audit.CreatedAt = T1
```

When:

```text
Change CreatedAt to T2
```

is attempted.

Then:

```text
Rejected

CreatedAt = T1
```

---

# Escenario TS-029 — UpdatedAt no cambia por lectura

Given:

```text
UpdatedAt = T1
```

When:

```text
Audit is read
```

Then:

```text
UpdatedAt = T1
```

---

# Escenario TS-030 — Versión inicial

Given:

```text
No Audit
```

When:

```text
RecordAudit
```

succeeds.

Then:

```text
Audit.Version = 1
```

---

# Escenario TS-031 — No existe Version 0 persistida obligatoria

Given:

```text
No Audit
```

Then:

```text
No persisted Audit.Version
```

is required.

---

# Escenario TS-032 — Operación rechazada no incrementa Version

Given:

```text
Audit.Version = N
```

When:

```text
Invalid Operation
```

is rejected.

Then:

```text
Audit.Version = N
```

---

# Escenario TS-033 — Lectura no incrementa Version

Given:

```text
Audit.Version = 1
```

When:

```text
findById()
```

Then:

```text
Audit.Version = 1
```

---

# Escenario TS-034 — Rehidratación no incrementa Version

Given:

```text
Persisted Audit.Version = 1
```

When:

```text
Audit is rehydrated
```

Then:

```text
Audit.Version = 1
```

---

# Escenario TS-035 — Replay no incrementa Version como nuevo hecho

Given:

```text
AuditRecorded
AggregateVersion = 1
```

When:

```text
Event replay
```

reconstructs Audit.

Then:

```text
Audit.Version = 1
```

and not:

```text
Audit.Version = 2
```

---

# Escenario TS-036 — AuditRecorded representa AggregateVersion resultante

Given:

```text
RecordAudit succeeds
```

Then:

```text
Audit.Version = 1

AuditRecorded.AggregateVersion = 1
```

---

# Escenario TS-037 — EventId único

Given:

```text
AuditRecorded Event A
```

Then:

```text
EventId exists
```

and identifies only that Domain Event.

---

# Escenario TS-038 — EventId permanece inmutable

Given:

```text
AuditRecorded.EventId = EVT-AUD-001
```

When:

```text
Change EventId
```

is attempted.

Then:

```text
Rejected
```

conceptually.

---

# Escenario TS-039 — Operación inválida no produce AuditRecorded

Given:

```text
Invalid RecordAudit
```

When:

```text
Domain Validation
```

rejects it.

Then:

```text
No AuditRecorded
```

---

# Escenario TS-040 — Operación no autorizada no produce AuditRecorded

Given:

```text
RecordAudit not authorized
```

When:

```text
Authorization denies request
```

Then:

```text
No Audit

No AuditRecorded
```

---

# Escenario TS-041 — Autorización no reemplaza Invariants

Given:

```text
Authorized RecordAudit
```

and:

```text
Invalid Domain Conditions
```

When:

```text
Audit validates the Command
```

Then:

```text
Rejected
```

---

# Escenario TS-042 — Deny by Default

Given:

```text
No explicit authorization
```

When:

```text
RecordAudit
```

is requested.

Then:

```text
Denied
```

---

# Escenario TS-043 — Permission no modifica State Machine

Given:

```text
Elevated Permission
```

and:

```text
AuditStatus = Recorded
```

When:

```text
Transition to Archived
```

is attempted.

Then:

```text
Rejected
```

because Archived is not an official state.

---

# Escenario TS-044 — Permission no modifica AuditId

Given:

```text
Authorized Actor

AuditId = AUD-100
```

When:

```text
Change AuditId
```

is attempted.

Then:

```text
Rejected
```

---

# Escenario TS-045 — Permission no modifica Version directamente

Given:

```text
Authorized Actor

Audit.Version = 1
```

When:

```text
setVersion(10)
```

is attempted.

Then:

```text
Rejected
```

---

# Escenario TS-046 — Authentication permanece fuera del Aggregate

Given:

```text
Authentication process
```

When:

```text
credentials are validated
```

Then:

```text
Audit Aggregate does not validate credentials
```

---

# Escenario TS-047 — Token no forma parte del estado

Given:

```text
AccessToken
```

is present in technical context.

When:

```text
RecordAudit
```

is constructed.

Then:

```text
AccessToken

∉

Audit Domain State
```

---

# Escenario TS-048 — Password no forma parte de Audit

Given:

```text
Password
```

exists in a technical source.

Then:

```text
Password

∉

Audit
```

---

# Escenario TS-049 — Source Payload completo no se copia

Given:

```text
Large Source Payload
```

When:

```text
RecordAudit
```

requires only selected traceability information.

Then:

```text
Only necessary information preserved
```

---

# Escenario TS-050 — Información sensible no necesaria

Given:

```text
Sensitive information exists in Source Payload
```

and:

```text
it is not required for Audit
```

Then:

```text
it is not incorporated
```

---

# Escenario TS-051 — Estado inicial válido

Given:

```text
No Audit
```

When:

```text
RecordAudit
```

succeeds.

Then:

```text
AuditStatus = Recorded
```

---

# Escenario TS-052 — Recorded es terminal

Given:

```text
AuditStatus = Recorded
```

When:

```text
any lifecycle transition
```

not officially defined is attempted.

Then:

```text
Rejected
```

---

# Escenario TS-053 — Draft no existe

Given:

```text
No Audit
```

When:

```text
Create Audit with Draft
```

is attempted.

Then:

```text
Rejected
```

---

# Escenario TS-054 — Pending no existe

Given:

```text
Technical processing is pending
```

When:

```text
AuditStatus = Pending
```

is attempted.

Then:

```text
Invalid State
```

---

# Escenario TS-055 — Active no existe

When:

```text
AuditStatus = Active
```

is attempted.

Then:

```text
Invalid State
```

---

# Escenario TS-056 — Failed no existe

Given:

```text
PersistenceFailure
```

When:

```text
AuditStatus = Failed
```

is inferred.

Then:

```text
Invalid State
```

---

# Escenario TS-057 — Cancelled no existe

Given:

```text
AuditStatus = Recorded
```

When:

```text
Recorded → Cancelled
```

is attempted.

Then:

```text
Rejected
```

---

# Escenario TS-058 — Archived no existe

Given:

```text
AuditStatus = Recorded
```

When:

```text
Recorded → Archived
```

is attempted.

Then:

```text
Rejected
```

---

# Escenario TS-059 — Deleted no existe

Given:

```text
AuditStatus = Recorded
```

When:

```text
Recorded → Deleted
```

is attempted.

Then:

```text
Rejected
```

---

# Escenario TS-060 — Source Status no se hereda

Given:

```text
Source Status = Failed
```

When:

```text
corresponding fact is audited
```

Then:

```text
AuditStatus = Recorded
```

and not:

```text
AuditStatus = Failed
```

---

# Escenario TS-061 — Source Archived no produce Audit Archived

Given:

```text
Source Status = Archived
```

When:

```text
corresponding fact is audited
```

Then:

```text
AuditStatus = Recorded
```

---

# Escenario TS-062 — Source Cancelled no produce Audit Cancelled

Given:

```text
Source Status = Cancelled
```

When:

```text
corresponding fact is audited
```

Then:

```text
AuditStatus = Recorded
```

---

# Escenario TS-063 — Repository save() persiste Aggregate válido

Given:

```text
Valid Audit

AuditStatus = Recorded

Version = 1
```

When:

```text
AuditRepository.save()
```

succeeds.

Then:

```text
persisted Audit preserves identity, state and Version
```

---

# Escenario TS-064 — Repository no corrige Aggregate inválido

Given:

```text
Invalid Audit
```

When:

```text
AuditRepository.save()
```

is attempted.

Then:

```text
Repository does not repair domain state
```

---

# Escenario TS-065 — Repository no incrementa Version

Given:

```text
Audit.Version = 1
```

When:

```text
save()
```

succeeds.

Then:

```text
PersistedVersion = 1
```

---

# Escenario TS-066 — findById preserva identidad

Given:

```text
AuditId = AUD-200
```

persisted.

When:

```text
findById(AUD-200)
```

Then:

```text
AuditId = AUD-200
```

---

# Escenario TS-067 — findById preserva Version

Given:

```text
Audit.Version = 1
```

persisted.

When:

```text
findById()
```

Then:

```text
Audit.Version = 1
```

---

# Escenario TS-068 — findById no produce AuditRecorded

Given:

```text
Existing Audit
```

When:

```text
findById()
```

Then:

```text
No new AuditRecorded
```

---

# Escenario TS-069 — exists() no modifica Audit

Given:

```text
Audit exists
```

When:

```text
exists(AuditId)
```

Then:

```text
no state change

no Version change

no Domain Event
```

---

# Escenario TS-070 — nextIdentity() no crea Aggregate

Given:

```text
AuditRepository
```

When:

```text
nextIdentity()
```

returns:

```text
AUD-300
```

Then:

```text
Audit AUD-300 does not yet exist
```

---

# Escenario TS-071 — DuplicateAuditId

Given:

```text
AuditId = AUD-300
```

already exists.

When:

```text
another incompatible Audit with AUD-300
```

is persisted.

Then:

```text
DuplicateAuditId
```

and existing Audit remains unchanged.

---

# Escenario TS-072 — AuditNotFound

Given:

```text
AuditId = AUD-404
```

does not exist.

When:

```text
findById(AUD-404)
```

Then:

```text
AuditNotFound
```

according to the Repository Contract.

No Aggregate is created.

---

# Escenario TS-073 — PersistenceFailure no cambia estado

Given:

```text
Valid Audit candidate
```

When:

```text
PersistenceFailure
```

occurs before commit.

Then:

```text
No confirmed Audit commit
```

and no:

```text
AuditStatus = Failed
```

---

# Escenario TS-074 — RepositoryUnavailable no cambia Source Fact

Given:

```text
Source Fact committed
```

When:

```text
RepositoryUnavailable
```

prevents Audit persistence.

Then:

```text
Source Fact remains committed
```

---

# Escenario TS-075 — Concurrency válida

Given:

```text
ExpectedVersion = N

PersistedVersion = N
```

When:

```text
a future valid modification
```

is persisted.

Then:

```text
write may proceed
```

subject to domain validity.

---

# Escenario TS-076 — ConcurrencyConflict

Given:

```text
ExpectedVersion = N - 1

PersistedVersion = N
```

When:

```text
write is attempted
```

Then:

```text
ConcurrencyConflict
```

---

# Escenario TS-077 — ConcurrencyConflict no incrementa Version

Given:

```text
PersistedVersion = N
```

When:

```text
ConcurrencyConflict
```

occurs.

Then:

```text
PersistedVersion = N
```

---

# Escenario TS-078 — SourceAggregateVersion no se usa como ExpectedVersion

Given:

```text
SourceAggregateVersion = 8

Audit.Version = 1
```

Then:

```text
SourceAggregateVersion
```

must not be treated as:

```text
Audit ExpectedVersion
```

---

# Escenario TS-079 — Repository.delete() no es DeleteAudit

Given:

```text
Repository.delete()
```

exists conceptually.

Then:

```text
DeleteAudit
```

is not inferred.

---

# Escenario TS-080 — delete() no crea Deleted

Given:

```text
Repository.delete()
```

Then:

```text
AuditStatus = Deleted
```

is not inferred.

---

# Escenario TS-081 — No ArchiveAudit

When:

```text
ArchiveAudit
```

is requested.

Then:

```text
Undefined Domain Command
```

---

# Escenario TS-082 — No DeleteAudit

When:

```text
DeleteAudit
```

is requested.

Then:

```text
Undefined Domain Command
```

---

# Escenario TS-083 — No CorrectAudit

When:

```text
CorrectAudit
```

is requested.

Then:

```text
Undefined Domain Command
```

---

# Escenario TS-084 — No RetryAudit

When:

```text
RetryAudit
```

is requested.

Then:

```text
Undefined Domain Command
```

---

# Escenario TS-085 — No AuditArchived

When:

```text
AuditArchived
```

is expected after an unsupported archive operation.

Then:

```text
No such Domain Event
```

---

# Escenario TS-086 — No AuditDeleted

When:

```text
AuditDeleted
```

is expected.

Then:

```text
No such Domain Event
```

---

# Escenario TS-087 — No AuditCorrected

When:

```text
AuditCorrected
```

is expected.

Then:

```text
No such Domain Event
```

---

# Escenario TS-088 — No AuditRetried

When:

```text
AuditRetried
```

is expected after technical retry.

Then:

```text
No such Domain Event
```

---

# Escenario TS-089 — Retry técnico no modifica Audit

Given:

```text
Audit processing failed technically
```

When:

```text
technical retry
```

occurs.

Then:

```text
no lifecycle transition
```

occurs because of the retry itself.

---

# Escenario TS-090 — Duplicate Technical Delivery

Given:

```text
Same technical message delivered twice
```

Then:

```text
Duplicate Delivery

≠

Two Source Facts
```

---

# Escenario TS-091 — Duplicate Technical Delivery no crea segundo Audit automáticamente

Given:

```text
Same source fact is delivered twice technically
```

Then:

```text
no automatic second Audit
```

is created solely because of transport duplication.

---

# Escenario TS-092 — AuditRecorded duplicado mantiene identidad

Given:

```text
AuditRecorded.EventId = EVT-AUD-100
```

delivered twice to a consumer.

Then:

```text
Same EventId

=

Same Domain Event
```

---

# Escenario TS-093 — Read Model recibe AuditRecorded

Given:

```text
AuditRecorded
```

When:

```text
Projection applies event
```

Then:

```text
Audit Read Model updated
```

without modifying Audit.

---

# Escenario TS-094 — Projection no ejecuta Command

Given:

```text
AuditRecorded
```

When:

```text
Projection processes event
```

Then:

```text
RecordAudit not executed
```

---

# Escenario TS-095 — Projection no incrementa Version

Given:

```text
Audit.Version = 1
```

When:

```text
Read Model is updated
```

Then:

```text
Audit.Version = 1
```

---

# Escenario TS-096 — Projection no produce AuditRecorded

Given:

```text
Read Model projection
```

When:

```text
projection update succeeds
```

Then:

```text
No new AuditRecorded
```

---

# Escenario TS-097 — Projection Lag

Given:

```text
Audit committed
```

and:

```text
Read Model not yet updated
```

Then:

```text
Projection Lag

≠

Audit Inconsistency
```

---

# Escenario TS-098 — Projection Failure no revierte Audit

Given:

```text
Audit committed
```

When:

```text
ProjectionFailure
```

occurs.

Then:

```text
Audit remains committed
```

---

# Escenario TS-099 — Projection Failure no es AuditStatus

Given:

```text
ProjectionFailure
```

Then:

```text
AuditStatus remains Recorded
```

---

# Escenario TS-100 — Projection Retry no modifica Version

Given:

```text
Audit.Version = 1
```

When:

```text
projection retry
```

occurs.

Then:

```text
Audit.Version = 1
```

---

# Escenario TS-101 — Rebuild de Read Model

Given:

```text
confirmed Audit facts
```

When:

```text
Read Model is rebuilt
```

Then:

```text
no RecordAudit

no Audit Version increment

no new AuditRecorded
```

---

# Escenario TS-102 — Eliminación de proyección no elimina Aggregate

Given:

```text
Audit exists
```

When:

```text
Read projection is physically deleted
```

Then:

```text
Audit remains unchanged
```

---

# Escenario TS-103 — Read Access no incrementa Version

Given:

```text
Audit.Version = 1
```

When:

```text
query is executed
```

Then:

```text
Audit.Version = 1
```

---

# Escenario TS-104 — Read Access no modifica UpdatedAt

Given:

```text
UpdatedAt = T1
```

When:

```text
query is executed
```

Then:

```text
UpdatedAt = T1
```

---

# Escenario TS-105 — Query no produce Domain Event

When:

```text
Find Audit by AuditId
```

is executed.

Then:

```text
No AuditRecorded
```

---

# Escenario TS-106 — Consulta por SourceAggregateId

Given:

```text
multiple Audits related to SourceAggregateId = ASM-500
```

When:

```text
Find Audits by SourceAggregateId
```

Then:

```text
matching Read Models may be returned
```

without loading them into one Aggregate.

---

# Escenario TS-107 — Consulta por SourceEventId

Given:

```text
SourceEventId available
```

When:

```text
Find Audits by SourceEventId
```

Then:

```text
Read Side may return matching projections
```

without introducing a new domain uniqueness rule.

---

# Escenario TS-108 — Consulta por ActorId

Given:

```text
ActorId available and read permission granted
```

When:

```text
Find Audits by ActorId
```

Then:

```text
permitted Read Models may be returned
```

---

# Escenario TS-109 — Consulta por CorrelationId

Given:

```text
multiple facts share CorrelationId = FLOW-100
```

When:

```text
Find Audits by CorrelationId
```

Then:

```text
a correlated view may be returned
```

without creating a shared Consistency Boundary.

---

# Escenario TS-110 — Consulta por CausationId

Given:

```text
CausationId available
```

When:

```text
Find Audits by CausationId
```

Then:

```text
causal relations may be queried
```

without granting mutation authority.

---

# Escenario TS-111 — Timeline no es Aggregate global

Given:

```text
multiple Audit projections
```

When:

```text
a global timeline is requested
```

Then:

```text
Read Model may combine records
```

while:

```text
no Global Audit Aggregate
```

is introduced.

---

# Escenario TS-112 — Cross-Aggregate Read Model

Given:

```text
Assembly

Voting

Document

Notification

Audit
```

information is available for reading.

When:

```text
combined projection is built
```

Then:

```text
Cross-Aggregate Read Model

≠

Cross-Aggregate Transaction
```

---

# Escenario TS-113 — Domain Event no implica Integration Event

Given:

```text
AuditRecorded
```

and:

```text
no explicit integration need
```

Then:

```text
no AuditRecordedIntegrationEvent required
```

---

# Escenario TS-114 — Integration Event cuando existe contrato explícito

Given:

```text
AuditRecorded

Explicit Integration Need
```

When:

```text
Integration Boundary transforms the fact
```

Then:

```text
AuditRecordedIntegrationEvent
```

may be produced.

---

# Escenario TS-115 — Integration Event no modifica Audit

Given:

```text
AuditStatus = Recorded

Audit.Version = 1
```

When:

```text
AuditRecordedIntegrationEvent is published
```

Then:

```text
AuditStatus = Recorded

Audit.Version = 1
```

---

# Escenario TS-116 — Publicación antes del commit no es válida

Given:

```text
Audit not committed
```

When:

```text
external publication is attempted
```

Then:

```text
publication must not represent a confirmed Audit fact
```

---

# Escenario TS-117 — Fallo de publicación no revierte Audit

Given:

```text
Audit committed
```

When:

```text
Integration publication fails
```

Then:

```text
Audit remains Recorded

Audit.Version unchanged
```

---

# Escenario TS-118 — Retry de Integration no modifica Version

Given:

```text
Audit.Version = 1
```

When:

```text
Integration publication retry
```

occurs.

Then:

```text
Audit.Version = 1
```

---

# Escenario TS-119 — Fallo del consumidor no revierte Audit

Given:

```text
AuditRecordedIntegrationEvent published
```

When:

```text
external consumer fails
```

Then:

```text
Audit remains unchanged
```

---

# Escenario TS-120 — Duplicate Integration Delivery

Given:

```text
Same Integration Event EventId
```

delivered twice.

Then:

```text
Same EventId

=

Same Integration Event
```

---

# Escenario TS-121 — Integration Event EventId no es AuditId

Given:

```text
IntegrationEvent.EventId = INT-001

AuditId = AUD-001
```

Then:

```text
INT-001

≠

AUD-001
```

conceptually.

---

# Escenario TS-122 — Integration Contract Version no es Audit.Version

Given:

```text
Integration Contract Version = 2

Audit.Version = 1
```

Then:

```text
both values remain conceptually independent
```

---

# Escenario TS-123 — Outbox State no es AuditStatus

Given:

```text
OutboxStatus = Failed
```

Then:

```text
AuditStatus = Recorded
```

remains unchanged.

---

# Escenario TS-124 — Outbox Retry no ejecuta RecordAudit

Given:

```text
Audit already committed
```

When:

```text
Outbox retry
```

occurs.

Then:

```text
RecordAudit not executed
```

---

# Escenario TS-125 — FIWARE permanece fuera del Aggregate

Given:

```text
AuditRecordedIntegrationEvent
```

When:

```text
Integration maps it to FIWARE
```

Then:

```text
Audit does not acquire NGSI-LD or Context Broker behavior
```

---

# Escenario TS-126 — NGSI-LD no es Audit Domain Model

Given:

```text
NGSI-LD representation
```

Then:

```text
NGSI-LD Entity

≠

Audit Aggregate
```

---

# Escenario TS-127 — Sistema municipal no modifica Audit directamente

Given:

```text
Municipal System
```

When:

```text
it consumes Audit information
```

Then:

```text
no direct Audit state mutation
```

occurs.

---

# Escenario TS-128 — Permiso municipal no equivale a Audit Permission

Given:

```text
Municipal Authorization
```

Then:

```text
Municipal Authorization

≠

Automatic RecordAudit Permission
```

---

# Escenario TS-129 — FIWARE Authentication no equivale a Domain Permission

Given:

```text
authenticated FIWARE identity
```

Then:

```text
authenticated

≠

automatically authorized for RecordAudit
```

---

# Escenario TS-130 — Log técnico no es Audit

Given:

```text
Application Log Entry
```

When:

```text
it is generated
```

Then:

```text
no automatic RecordAudit
```

---

# Escenario TS-131 — Metric no es Audit

Given:

```text
Operational Metric
```

Then:

```text
no automatic Audit Aggregate
```

---

# Escenario TS-132 — Trace técnico no es Audit

Given:

```text
Technical Trace
```

Then:

```text
Technical Trace

≠

Audit
```

---

# Escenario TS-133 — Audit no es Document Archive

Given:

```text
Source Document
```

When:

```text
a Document fact is audited
```

Then:

```text
Document reference may be preserved
```

but:

```text
Entire Document Content
```

is not automatically embedded.

---

# Escenario TS-134 — Audit no envía Notification

Given:

```text
AuditRecorded
```

Then:

```text
no Notification delivery occurs automatically
```

as behavior of Audit.

---

# Escenario TS-135 — Notification fact auditado

Given:

```text
NotificationDelivered
```

confirmed.

When:

```text
RecordAudit
```

succeeds.

Then:

```text
AuditStatus = Recorded
```

and Notification remains unchanged.

---

# Escenario TS-136 — NotificationDeliveryFailed no crea Audit Failed

Given:

```text
NotificationDeliveryFailed
```

When:

```text
its fact is audited
```

Then:

```text
AuditStatus = Recorded
```

---

# Escenario TS-137 — AssemblyCancelled no crea Audit Cancelled

Given:

```text
AssemblyCancelled
```

When:

```text
its fact is audited
```

Then:

```text
AuditStatus = Recorded
```

---

# Escenario TS-138 — Document Archived no crea Audit Archived

Given:

```text
DocumentStatus = Archived
```

and a confirmed auditable fact.

When:

```text
RecordAudit
```

succeeds.

Then:

```text
AuditStatus = Recorded
```

---

# Escenario TS-139 — Voting permanece independiente

Given:

```text
confirmed Voting fact
```

When:

```text
RecordAudit
```

succeeds.

Then Audit does not:

```text
register vote

modify vote

open Voting

close Voting

alter result
```

---

# Escenario TS-140 — Membership permanece independiente

Given:

```text
confirmed Membership fact
```

When:

```text
RecordAudit
```

succeeds.

Then:

```text
MembershipStatus unchanged

Membership.Version unchanged by Audit
```

---

# Escenario TS-141 — Role permanece independiente

Given:

```text
confirmed Role fact
```

When:

```text
RecordAudit
```

succeeds.

Then Audit does not:

```text
assign Role

revoke Role

modify Role
```

---

# Escenario TS-142 — Territory permanece independiente

Given:

```text
confirmed Territory fact
```

When:

```text
RecordAudit
```

succeeds.

Then:

```text
Territory remains outside Audit Consistency Boundary
```

---

# Escenario TS-143 — Organization permanece independiente

Given:

```text
confirmed Organization fact
```

When:

```text
RecordAudit
```

succeeds.

Then:

```text
Organization remains unchanged by Audit
```

---

# Escenario TS-144 — Proposal permanece independiente

Given:

```text
confirmed Proposal fact
```

When:

```text
RecordAudit
```

succeeds.

Then:

```text
ProposalStatus unchanged

Proposal.Version unchanged by Audit
```

---

# Escenario TS-145 — Participation permanece independiente

Given:

```text
confirmed Participation fact
```

When:

```text
RecordAudit
```

succeeds.

Then:

```text
Participation Transaction

≠

Audit Transaction
```

---

# Escenario TS-146 — Nuevo Source Fact no reescribe Audit anterior

Given:

```text
Source Fact A

Audit A = Recorded
```

When:

```text
Source Fact B
```

occurs later.

Then:

```text
Audit A remains unchanged
```

---

# Escenario TS-147 — Hecho correctivo produce trazabilidad independiente

Given:

```text
Source Fact A

Audit A
```

and later:

```text
Corrective Source Fact B
```

Then:

```text
Audit A remains historical
```

and Fact B may produce:

```text
Audit B
```

when the applicable contract exists.

---

# Escenario TS-148 — Múltiples hechos producen Audits independientes

Given:

```text
Source Fact A

Source Fact B

Source Fact C
```

When each valid fact is audited.

Then:

```text
Audit A

Audit B

Audit C
```

maintain independent:

```text
AuditId

Version

Consistency Boundary
```

---

# Escenario TS-149 — No Aggregate global

Given:

```text
many Audit instances
```

When:

```text
global historical query
```

is required.

Then:

```text
Read Model
```

is used conceptually.

No:

```text
GlobalAudit Aggregate
```

is inferred.

---

# Escenario TS-150 — Batch no fusiona Aggregates

Given:

```text
multiple auditable facts
```

When:

```text
batch processing
```

occurs.

Then:

```text
multiple independent Audit operations
```

remain conceptually distinct.

---

# Escenario TS-151 — CorrelationId compartido no fusiona transacciones

Given:

```text
Audit A.CorrelationId = FLOW-1

Audit B.CorrelationId = FLOW-1
```

Then:

```text
Shared CorrelationId

≠

Shared Consistency Boundary
```

---

# Escenario TS-152 — CausationId no concede ownership

Given:

```text
CausationId references external fact
```

Then:

```text
Causation

≠

Mutation Authority
```

---

# Escenario TS-153 — Event Sourcing reconstruye Recorded

Given:

```text
AuditRecorded
AggregateVersion = 1
```

When:

```text
event is applied during rehydration
```

Then:

```text
AuditStatus = Recorded

Audit.Version = 1
```

---

# Escenario TS-154 — Replay no vuelve a producir evento

Given:

```text
historical AuditRecorded
```

When:

```text
replay
```

occurs.

Then:

```text
no new AuditRecorded
```

is emitted.

---

# Escenario TS-155 — Event Stream de Audit no incorpora Source Events como propios

Given:

```text
AssemblyStarted
```

is the Source Domain Event.

When:

```text
Audit event stream
```

is reconstructed.

Then:

```text
AuditRecorded
```

belongs to Audit.

```text
AssemblyStarted
```

remains owned by Assembly.

---

# Escenario TS-156 — Source Event Stream y Audit Event Stream son distintos

Then:

```text
Source Aggregate Event Stream

≠

Audit Event Stream
```

---

# Escenario TS-157 — Snapshot no modifica Audit

Given:

```text
Audit snapshot
```

is created technically.

Then:

```text
no Version increment

no State change

no Domain Event
```

---

# Escenario TS-158 — Cache no es autoridad

Given:

```text
cached Audit representation
```

Then:

```text
Cache

≠

Write Authority
```

---

# Escenario TS-159 — Replica desactualizada no cambia autoridad

Given:

```text
technical replica has stale data
```

Then:

```text
stale replica

≠

change of Audit domain state
```

---

# Escenario TS-160 — Schema migration no incrementa Audit.Version

Given:

```text
persistence schema migration
```

When:

```text
migration executes
```

Then:

```text
Audit.Version unchanged
```

unless a valid domain modification separately occurs.

---

# Escenario TS-161 — API Version no es Audit.Version

Given:

```text
API Version = 2

Audit.Version = 1
```

Then:

```text
API Version

≠

Audit.Version
```

---

# Escenario TS-162 — Document Version no es Audit.Version

Given:

```text
DOMAIN-012 documentation version = 1.0

Audit.Version = 1
```

Then:

```text
Documentation Version

≠

Aggregate Version
```

---

# Escenario TS-163 — Integration Contract Version no modifica Aggregate

Given:

```text
Integration Contract Version changes
```

Then:

```text
Audit.Version unchanged
```

---

# Escenario TS-164 — Read Permission no implica Write Permission

Given:

```text
Read Permission granted
```

Then:

```text
RecordAudit Permission
```

is not inferred.

---

# Escenario TS-165 — Write Permission no implica acceso universal de lectura

Given:

```text
RecordAudit Permission granted
```

Then:

```text
unrestricted Read Permission
```

is not inferred.

---

# Escenario TS-166 — ActorId no implica Permission

Given:

```text
ActorId = CIT-500
```

Then:

```text
ActorId

≠

Authorization
```

---

# Escenario TS-167 — SourceEventId no implica Permission

Given:

```text
SourceEventId = EVT-500
```

Then:

```text
SourceEventId

≠

Authorization
```

---

# Escenario TS-168 — Conocer AuditId no concede acceso

Given:

```text
Actor knows AuditId
```

Then:

```text
Knowledge of AuditId

≠

Authorization
```

---

# Escenario TS-169 — Internal Process no está autorizado automáticamente

Given:

```text
internal process
```

Then:

```text
Internal

≠

Automatically Authorized
```

---

# Escenario TS-170 — External System no obtiene mutación directa

Given:

```text
authorized external integration
```

Then:

```text
no direct Aggregate mutation authority
```

is inferred.

---

# Escenario TS-171 — Datos históricos no son públicos automáticamente

Given:

```text
Audit historical data
```

Then:

```text
Historical

≠

Public
```

---

# Escenario TS-172 — Read Model respeta minimización

Given:

```text
Audit contains several traceability fields
```

When:

```text
a specific Read Model is built
```

Then:

```text
only necessary and permitted data
```

is exposed.

---

# Escenario TS-173 — ActorId no se expone automáticamente

Given:

```text
Audit.ActorId exists
```

When:

```text
a Read Model does not require ActorId
```

Then:

```text
ActorId is not required in the projection
```

---

# Escenario TS-174 — Integration Event respeta minimización

Given:

```text
AuditRecorded
```

When:

```text
AuditRecordedIntegrationEvent
```

is built.

Then:

```text
only necessary public information
```

is included.

---

# Escenario TS-175 — Integration Event no contiene credenciales

Given:

```text
technical context contains tokens or secrets
```

When:

```text
AuditRecordedIntegrationEvent
```

is created.

Then:

```text
no password

no access token

no refresh token

no API key

no private key

no secret
```

is included.

---

# Escenario TS-176 — Read Model no contiene credenciales

Given:

```text
technical credentials exist elsewhere
```

When:

```text
Audit Read Model
```

is projected.

Then:

```text
credentials not projected
```

---

# Escenario TS-177 — Source Payload no determina Integration Payload

Given:

```text
Source Payload contains fields A, B, C, D
```

and Integration Contract requires only:

```text
A, C
```

Then:

```text
Integration Payload contains only required information
```

according to the contract.

---

# Escenario TS-178 — Source Payload no determina Read Model

Given:

```text
Source Payload contains many fields
```

When:

```text
Read Model is projected
```

Then:

```text
only read-purpose information is exposed
```

---

# Escenario TS-179 — Audit no se audita recursivamente por defecto

Given:

```text
AuditRecorded
```

When:

```text
event is produced
```

Then:

```text
no automatic RecordAudit(AuditRecorded)
```

is triggered by the Aggregate definition.

---

# Escenario TS-180 — Consulta Audit no crea otro Audit

Given:

```text
Audit read query
```

When:

```text
query executes
```

Then:

```text
no automatic RecordAudit
```

---

# Escenario TS-181 — AuthorizationDenied no crea Audit automáticamente

Given:

```text
AuthorizationDenied
```

Then:

```text
no automatic RecordAudit
```

unless a separate explicit auditable contract exists.

---

# Escenario TS-182 — AuthorizationGranted no equivale a AuditRecorded

Given:

```text
AuthorizationGranted
```

Then:

```text
AuthorizationGranted

≠

AuditRecorded
```

---

# Escenario TS-183 — Technical Processing State no es AuditStatus

Given:

```text
WorkerState = Processing
```

Then:

```text
AuditStatus

≠

Processing
```

---

# Escenario TS-184 — Queued no es AuditStatus

Given:

```text
MessageState = Queued
```

Then:

```text
AuditStatus

≠

Queued
```

---

# Escenario TS-185 — DeadLettered no es AuditStatus

Given:

```text
MessageState = DeadLettered
```

Then:

```text
AuditStatus

≠

DeadLettered
```

---

# Escenario TS-186 — Technical Publish Event no es Domain Event

Given:

```text
AuditMessagePublished
```

as a technical fact.

Then:

```text
AuditMessagePublished

≠

Audit Domain Event
```

---

# Escenario TS-187 — Technical Persist Event no es Domain Event

Given:

```text
AuditPersisted
```

as a technical persistence notification.

Then:

```text
it is not an official Audit Domain Event
```

---

# Escenario TS-188 — Integration log no es Integration Event

Given:

```text
integration log entry
```

Then:

```text
Integration Log

≠

AuditRecordedIntegrationEvent
```

---

# Escenario TS-189 — Broker failure no es Audit Domain Event

Given:

```text
BrokerUnavailable
```

Then:

```text
BrokerUnavailable

≠

Audit Domain Event
```

---

# Escenario TS-190 — Broker failure no modifica Audit

Given:

```text
Audit committed

Audit.Version = 1
```

When:

```text
broker failure
```

occurs during publication.

Then:

```text
Audit remains Recorded

Audit.Version = 1
```

---

# Escenario TS-191 — No orden global obligatorio

Given:

```text
Audit A.Version = 1

Audit B.Version = 1
```

Then:

```text
no global ordering between A and B
```

is inferred from those Versions.

---

# Escenario TS-192 — AggregateVersion preserva orden por identidad

Given:

```text
future Audit history with multiple versions
```

Then:

```text
AggregateVersion
```

must preserve logical order for the same AuditId.

---

# Escenario TS-193 — No salto arbitrario de Version

Given:

```text
Audit.Version = N
```

When:

```text
one valid future modification
```

occurs.

Then:

```text
Audit.Version = N + 1
```

not:

```text
N + 5
```

by arbitrary Infrastructure decision.

---

# Escenario TS-194 — Un incremento por modificación

Given:

```text
Audit.Version = N
```

When:

```text
one valid modification
```

occurs.

Then:

```text
exactly one Version increment
```

occurs.

---

# Escenario TS-195 — Persistencia y recuperación preservan significado

Given:

```text
Audit A
```

When:

```text
save(Audit A)

findById(Audit A.AuditId)
```

Then:

```text
Same Identity

Same State

Same Version

Same Traceability Meaning
```

are preserved.

---

# Escenario TS-196 — Repository no inventa ActorId

Given:

```text
Audit.ActorId absent
```

When:

```text
save()
```

occurs.

Then:

```text
Repository does not add ActorId
```

---

# Escenario TS-197 — Repository no inventa SourceEventId

Given:

```text
SourceEventId absent
```

When:

```text
save()
```

occurs.

Then:

```text
Repository does not fabricate SourceEventId
```

---

# Escenario TS-198 — Repository no inventa AuditRecorded

Given:

```text
Repository.save()
```

Then:

```text
Repository does not decide to create AuditRecorded
```

---

# Escenario TS-199 — Repository no autentica

Given:

```text
AuditRepository
```

Then:

```text
it does not validate passwords or tokens
```

as domain responsibility.

---

# Escenario TS-200 — Repository no autoriza

Given:

```text
AuditRepository
```

Then:

```text
it does not decide RecordAudit Permission
```

---

# Escenario TS-201 — Repository no realiza Analytics

Given:

```text
need to count Audits by SourceEventType
```

Then:

```text
Read Side
```

handles the query conceptually.

AuditRepository does not become an Analytics engine.

---

# Escenario TS-202 — Repository no crea Multi-Aggregate Transaction

Given:

```text
Audit

Assembly
```

When:

```text
AuditRepository.save()
```

executes.

Then:

```text
Assembly is not persisted as part of AuditRepository
```

---

# Escenario TS-203 — Source Aggregate completo no se embebe

Given:

```text
Source Aggregate
```

When:

```text
Audit is created
```

Then:

```text
necessary references only
```

may be retained.

No:

```text
complete embedded Source Aggregate
```

is required.

---

# Escenario TS-204 — Citizen completo no se embebe por ActorId

Given:

```text
ActorId references Citizen
```

Then:

```text
Citizen Aggregate

∉

Audit Consistency Boundary
```

---

# Escenario TS-205 — Document completo no se embebe por referencia

Given:

```text
Document reference
```

Then:

```text
Document Aggregate

∉

Audit Consistency Boundary
```

---

# Escenario TS-206 — Source Event Object no transfiere ownership

Given:

```text
Source Domain Event
```

When:

```text
Audit preserves information from it
```

Then:

```text
Source Event Ownership

remains with

Source Aggregate
```

---

# Escenario TS-207 — Consistencia eventual entre Source y Audit

Given:

```text
Source Fact committed at T1
```

and:

```text
Audit committed at T3
```

with:

```text
T1 < T3
```

Then:

```text
eventual consistency is valid
```

---

# Escenario TS-208 — Ausencia temporal de Audit es válida

Given:

```text
Source Fact committed
```

and:

```text
Audit not yet recorded
```

Then:

```text
Source Aggregate remains valid
```

---

# Escenario TS-209 — No Two-Phase Commit obligatorio

Given:

```text
Source Aggregate

Audit
```

Then:

```text
no mandatory two-phase commit
```

is required by the domain model.

---

# Escenario TS-210 — No Cascading Rollback

Given:

```text
Audit failure
```

Then:

```text
no automatic rollback of Assembly

no automatic rollback of Notification

no automatic rollback of Document
```

---

# Escenario TS-211 — No Cascading Mutation

Given:

```text
successful RecordAudit
```

Then:

```text
no direct mutation of Source Aggregate
```

occurs.

---

# Escenario TS-212 — No Cross-Aggregate Setter

When:

```text
audit.setAssemblyStatus(...)
```

is attempted.

Then:

```text
Not Allowed
```

---

# Escenario TS-213 — No setNotificationStatus

When:

```text
audit.setNotificationStatus(...)
```

is attempted.

Then:

```text
Not Allowed
```

---

# Escenario TS-214 — No setDocumentStatus

When:

```text
audit.setDocumentStatus(...)
```

is attempted.

Then:

```text
Not Allowed
```

---

# Escenario TS-215 — Read Model no crea Permission

Given:

```text
Audit visible in Read Model
```

Then:

```text
Write Permission

is not inferred
```

---

# Escenario TS-216 — Integration Event no concede Permission

Given:

```text
consumer receives AuditRecordedIntegrationEvent
```

Then:

```text
RecordAudit Permission

is not granted automatically
```

---

# Escenario TS-217 — Domain Event no concede Permission

Given:

```text
consumer receives AuditRecorded
```

Then:

```text
no mutation authority over Audit
```

is granted.

---

# Escenario TS-218 — CorrelationId no concede Permission

Given:

```text
CorrelationId known by requester
```

Then:

```text
Authorization

is not implied
```

---

# Escenario TS-219 — CausationId no concede Permission

Given:

```text
CausationId known
```

Then:

```text
mutation authority

is not implied
```

---

# Escenario TS-220 — Security Claim no es estado

Given:

```text
Security Claim
```

Then:

```text
Security Claim

≠

AuditStatus
```

---

# Escenario TS-221 — RBAC no introduce Roles internos en Audit

Given:

```text
external RBAC implementation
```

Then:

```text
Audit Aggregate

does not require internal Role entities
```

---

# Escenario TS-222 — ABAC no introduce atributos obligatorios de dominio

Given:

```text
external ABAC implementation
```

Then:

```text
authorization attributes

are not automatically Audit domain state
```

---

# Escenario TS-223 — Retención no se infiere

Given:

```text
AuditStatus = Recorded
```

Then:

```text
no retention period
```

is inferred automatically.

---

# Escenario TS-224 — Expiración no se infiere

Given:

```text
Audit exists
```

Then:

```text
Expired
```

is not inferred as an Audit state.

---

# Escenario TS-225 — Anonimización no se infiere

Given:

```text
Audit exists
```

Then:

```text
AuditAnonymized
```

is not inferred as a Domain Event.

---

# Escenario TS-226 — Redacción no se infiere

Given:

```text
Audit exists
```

Then:

```text
AuditRedacted
```

is not inferred as a Domain Event.

---

# Escenario TS-227 — Política de retención del Read Model no modifica Aggregate

Given:

```text
Read Model retention policy
```

When:

```text
projection data expires
```

Then:

```text
Audit Aggregate remains unchanged
```

---

# Escenario TS-228 — Archivado técnico de Read Model no crea Archived

Given:

```text
Read Model archived technically
```

Then:

```text
AuditStatus remains Recorded
```

---

# Escenario TS-229 — Cache eviction no elimina Audit

Given:

```text
Audit cached
```

When:

```text
cache entry is evicted
```

Then:

```text
Audit remains persisted
```

---

# Escenario TS-230 — Backup no es Domain Event

Given:

```text
Infrastructure backup
```

Then:

```text
no Audit Domain Event
```

is produced solely because of backup.

---

# Escenario TS-231 — Restore no ejecuta RecordAudit

Given:

```text
Infrastructure restore
```

Then:

```text
RecordAudit
```

is not executed as a new business intent.

---

# Escenario TS-232 — Migración no cambia State

Given:

```text
persistence migration
```

Then:

```text
AuditStatus remains Recorded
```

if the domain state itself has not changed.

---

# Escenario TS-233 — Query Engine no es Aggregate

Given:

```text
advanced search requirement
```

Then:

```text
Audit Aggregate

≠

Query Engine
```

---

# Escenario TS-234 — Reporting no modifica Aggregate

Given:

```text
historical report
```

When:

```text
report is generated
```

Then:

```text
Audit state and Version remain unchanged
```

---

# Escenario TS-235 — Analytics no incrementa Version

Given:

```text
analytics process reads Audit data
```

Then:

```text
Audit.Version unchanged
```

---

# Escenario TS-236 — Bulk Export no es Command

Given:

```text
export of multiple Audit records
```

Then:

```text
Bulk Export

≠

Audit Domain Command
```

---

# Escenario TS-237 — Paginación no es comportamiento de Aggregate

Given:

```text
paginated Audit history query
```

Then:

```text
Pagination

∈

Read Side
```

---

# Escenario TS-238 — Filtrado no es comportamiento de Aggregate

Given:

```text
filter by SourceEventType
```

Then:

```text
Filter

∈

Read Side
```

---

# Escenario TS-239 — Ordenamiento no es comportamiento de Aggregate

Given:

```text
sort by SourceOccurredAt
```

Then:

```text
Sorting

∈

Read Side
```

---

# Escenario TS-240 — Full-Text Search no modifica Aggregate

Given:

```text
full-text search over projected information
```

Then:

```text
Audit Aggregate remains unchanged
```

---

# Escenario TS-241 — External Read Contract no es modelo interno

Given:

```text
external system requires a different read representation
```

Then:

```text
External Read Contract

≠

Audit Internal Read Model
```

unless explicitly defined as equivalent.

---

# Escenario TS-242 — Anti-Corruption Layer preserva semántica

Given:

```text
external model differs from AURA
```

When:

```text
translation occurs
```

Then:

```text
Audit internal semantics remain unchanged
```

---

# Escenario TS-243 — External message no es Audit Domain Event

Given:

```text
external message received
```

Then:

```text
External Message

≠

AuditRecorded
```

unless Audit itself produces its Domain Event through valid
behavior.

---

# Escenario TS-244 — Event serialization no cambia semántica

Given:

```text
AuditRecordedIntegrationEvent
```

serialized as a technical format.

Then:

```text
serialization format

does not change

event semantics
```

---

# Escenario TS-245 — Transporte no cambia semántica

Given:

```text
integration event transported through a broker or protocol
```

Then:

```text
transport

≠

domain meaning
```

---

# Escenario TS-246 — Broker no define EventType

Given:

```text
broker topic name
```

Then:

```text
broker topic name

≠

Audit Domain Event semantic authority
```

---

# Escenario TS-247 — Base de datos no define State

Given:

```text
persistence technology
```

Then:

```text
database representation

does not define

AuditStatus
```

---

# Escenario TS-248 — ORM no define Invariants

Given:

```text
ORM constraints
```

Then:

```text
ORM

≠

Domain Invariant Authority
```

---

# Escenario TS-249 — Performance Optimization no evita Invariants

Given:

```text
optimization proposal
```

When:

```text
it attempts to bypass validation
```

Then:

```text
Not Allowed
```

---

# Escenario TS-250 — Performance Optimization no amplía Boundary

Given:

```text
query or persistence optimization
```

Then:

```text
no Source Aggregate embedding
```

is introduced solely for performance.

---

# Matriz de State Machine

| Estado previo | Operación | Estado resultante | Resultado |
|---|---|---|---|
| No Audit | RecordAudit válido | Recorded | Permitido |
| No Audit | RecordAudit inválido | No Audit | Rechazado |
| Recorded | transición a Draft | Recorded | Rechazado |
| Recorded | transición a Pending | Recorded | Rechazado |
| Recorded | transición a Active | Recorded | Rechazado |
| Recorded | transición a Failed | Recorded | Rechazado |
| Recorded | transición a Cancelled | Recorded | Rechazado |
| Recorded | transición a Archived | Recorded | Rechazado |
| Recorded | transición a Deleted | Recorded | Rechazado |

---

# Matriz Command / Domain Event

| Command | Resultado | Domain Event |
|---|---|---|
| RecordAudit válido | Recorded | AuditRecorded |
| RecordAudit inválido | Rejected | Ninguno de éxito |
| RecordAudit no autorizado | Rejected | Ninguno de éxito |

---

# Matriz de Versioning

| Operación | Version previa | Version resultante |
|---|---:|---:|
| Creación válida | No existe | 1 |
| Creación rechazada | No existe | No existe |
| Lectura | N | N |
| Rehidratación | N | N |
| Replay | N | N |
| Retry técnico | N | N |
| Publicación de Integration Event | N | N |
| Projection Update | N | N |
| Operación rechazada | N | N |

---

# Matriz de Ownership

| Concepto | Ownership |
|---|---|
| Audit | Audit Management |
| AuditRecorded | Audit |
| Source Aggregate | Bounded Context originador |
| Source Domain Event | Aggregate originador |
| AuditRecordedIntegrationEvent | Integration Contract |
| Audit Read Model | Read Side |

---

# Matriz de Identidades

| Identidad | Significado |
|---|---|
| AuditId | identidad del Aggregate Audit |
| SourceAggregateId | identidad del Aggregate originador |
| SourceEventId | identidad del evento originador |
| AuditRecorded.EventId | identidad del Domain Event AuditRecorded |
| IntegrationEvent.EventId | identidad del Integration Event |
| CorrelationId | correlación |
| CausationId | causalidad |

Ninguna debe sustituirse automáticamente por otra.

---

# Matriz de Consistencia

| Relación | Consistencia |
|---|---|
| Estado interno de Audit | inmediata dentro del Aggregate |
| Audit / Source Aggregate | eventual |
| Audit / Read Model | eventual |
| Audit / Integration Consumer | eventual |
| Audits diferentes | límites independientes |

---

# Matriz de Rechazos

Debe rechazarse:

```text
RecordAudit without confirmed fact

RecordAudit without required identity

unauthorized RecordAudit

direct AuditId mutation

direct State mutation

direct Version mutation

unsupported lifecycle transition

fabricated source information

stale concurrent write

attempt to embed external Aggregate

attempt to rewrite historical meaning
```

---

# Matriz de No Efectos

Las siguientes operaciones no modifican Audit:

```text
Query

findById

exists

nextIdentity

Rehydration

Replay

Projection Update

Projection Retry

Integration Publication

Integration Retry

Consumer Processing

Cache Operation

Backup

Restore

Persistence Migration
```

salvo que una futura regla explícita del dominio establezca
comportamiento diferente.

---

# Escenarios de Seguridad

Deben verificarse como mínimo:

```text
unauthorized command rejected

credentials not stored

tokens not stored

secrets not stored

read permission separated from write permission

actor id not treated as authorization

external identity not treated as automatic domain permission

minimum data exposed in read models

minimum data exposed in integration events
```

---

# Escenarios de Repository

Deben verificarse:

```text
valid save

identity preservation

state preservation

version preservation

created at preservation

source references preservation

find by id

exists

next identity

audit not found

duplicate audit id

concurrency conflict

persistence failure

repository unavailable

no repository generated domain events

no repository domain repair
```

---

# Escenarios de Domain Events

Deben verificarse:

```text
correct event type

correct EventId

correct AuditId

correct AggregateVersion

correct OccurredAt

correct CorrelationId when available

correct CausationId when available

minimum payload

no fabricated source information

event generated after valid command

event not generated after rejected command

historical values preserved
```

---

# Escenarios de Integration Events

Deben verificarse:

```text
integration event only when explicit contract exists

no integration publication before commit

correct integration event type

correct aggregate id

correct aggregate type

correct contract version

minimum public payload

no credentials

no aggregate mutation on publish

no aggregate version increment on retry

duplicate delivery safety

consumer failure does not rollback Audit
```

---

# Escenarios de Read Model

Deben verificarse:

```text
projection from confirmed Audit fact

no Command execution during projection

no Domain Event creation during projection

no Audit Version increment

projection idempotency

projection lag allowed

projection failure does not rollback Audit

rebuild without domain mutation

read permission separated from write permission

query filtering

query ordering

query pagination

global view does not create global Aggregate
```

---

# Escenarios de Consistency Boundary

Deben verificarse:

```text
Audit modifies only itself

Source Aggregate remains unchanged

Source Event remains unchanged

Source Commit independent from Audit Commit

no mandatory distributed transaction

no cascading rollback

no embedded external Aggregate

separate Version per Aggregate

separate Consistency Boundary per AuditId
```

---

# Escenarios de Historical Integrity

Deben verificarse:

```text
Audit meaning remains stable

new Source Fact does not rewrite previous Audit

corrective Source Fact remains a different fact

Source Status is not inherited

Domain Event remains immutable

Integration Event keeps historical meaning

projection does not reinterpret historical fact
```

---

# Escenarios de Tecnología

Debe verificarse conceptualmente que cambiar:

```text
database

ORM

broker

transport

serialization

cache

read store

FIWARE adapter

municipal adapter
```

no cambie:

```text
AuditId

Lifecycle

State Machine

Commands

Domain Events

Invariants

Versioning

Consistency Boundary
```

---

# Property-Based Rules

Cualquier conjunto amplio de casos debe preservar propiedades como:

```text
AuditId never changes

Recorded is always terminal

valid Audit always has Version >= 1

rejected operation never increments Version

read never mutates Write Model

source references never transfer Aggregate ownership

source status never becomes Audit status

duplicate technical delivery never means new domain fact by itself

source aggregate failure and Audit failure remain independent

domain event identity remains stable
```

---

# Invariant Tests

Cada Invariant definida en:

```text
DOMAIN-012E-Invariants.md
```

debe disponer conceptualmente de al menos:

```text
valid scenario

invalid scenario

boundary scenario when applicable
```

---

# Command Tests

`RecordAudit` debe probar:

```text
valid execution

missing required identity

unconfirmed source fact

unauthorized request

missing optional source information

valid source references

invariant violation

resulting Recorded state

resulting Version

resulting AuditRecorded
```

---

# State Machine Tests

Deben verificarse:

```text
No Audit → Recorded allowed

Recorded → Draft rejected

Recorded → Pending rejected

Recorded → Active rejected

Recorded → Failed rejected

Recorded → Cancelled rejected

Recorded → Archived rejected

Recorded → Deleted rejected
```

---

# Version Tests

Deben verificarse:

```text
creation gives Version 1

rejection keeps Version

query keeps Version

rehydration keeps Version

replay keeps Version

repository save does not increment Version

projection does not increment Version

integration publication does not increment Version

technical retry does not increment Version

concurrency conflict does not increment Version
```

---

# Permission Tests

Deben verificarse:

```text
authorized RecordAudit may reach domain validation

unauthorized RecordAudit rejected

authorization does not bypass invariants

authorization does not bypass state machine

authorization does not mutate AuditId

read permission does not imply write permission

write permission does not imply unrestricted read permission
```

---

# Repository Contract Tests

Deben verificarse:

```text
save valid Aggregate

preserve AuditId

preserve Recorded state

preserve Version

preserve timestamps

preserve source references

find existing Aggregate

handle absence

detect duplicate identity

detect stale expected Version

no Domain Event creation

no invariant repair

no external Aggregate persistence
```

---

# Read Model Tests

Deben verificarse:

```text
AuditRecorded creates or updates projection correctly

duplicate AuditRecorded does not duplicate logical record

projection can be rebuilt

rebuild does not affect Aggregate

queries do not affect Aggregate

filters do not affect Aggregate

sorting does not affect Aggregate

pagination does not affect Aggregate

projection failure does not affect Aggregate
```

---

# Integration Tests Conceptuales

Deben verificarse:

```text
AuditRecorded may map to AuditRecordedIntegrationEvent

mapping requires explicit integration contract

commit precedes external publication

publication failure leaves Audit unchanged

publication retry leaves Version unchanged

duplicate Integration Event can be identified

external consumer does not acquire Audit mutation authority
```

---

# Negative Tests

Deben existir escenarios que rechacen explícitamente:

```text
CreateAudit

UpdateAudit

ModifyAudit

ArchiveAudit

DeleteAudit

CorrectAudit

RetryAudit

PublishAudit

setAuditId

setStatus

setVersion

AuditStatus = Draft

AuditStatus = Pending

AuditStatus = Failed

AuditStatus = Archived

AuditStatus = Deleted
```

en la versión 1.0.

---

# Regresión

Toda evolución futura debe mantener pruebas de regresión sobre las
reglas consolidadas que continúen vigentes.

Un nuevo comportamiento no debe romper silenciosamente:

- identidad;
- trazabilidad;
- Versioning;
- separación de Aggregates;
- significado histórico;
- Domain Event contracts;
- Integration contracts;
- Read Models.

---

# Evolución de Test Scenarios

Cuando se incorpore oficialmente un nuevo:

- estado;
- Command;
- Domain Event;
- Invariant;
- Permission;
- Integration Event;
- Read Model behavior;

deben añadirse sus Test Scenarios correspondientes.

---

# Regla de Cobertura Conceptual

Todo nuevo comportamiento debe poseer escenarios para:

```text
success

rejection

invariants

permissions

versioning

domain events

consistency boundary
```

cuando correspondan.

---

# Regla de No Inferencia

Los Test Scenarios no pueden utilizarse para introducir una regla de
dominio todavía no definida.

Debe mantenerse:

```text
Test Scenario

verifies

Domain Rule
```

y no:

```text
Test Scenario

creates

New Domain Rule
```

---

# Reglas Fundamentales

Los Test Scenarios de Audit deben cumplir:

1. Validar exclusivamente reglas de dominio oficiales.
2. Utilizar Given / When / Then como estructura conceptual.
3. Verificar No Audit → Recorded.
4. Verificar que Recorded es terminal.
5. Verificar RecordAudit como único Command oficial.
6. Verificar AuditRecorded como único Domain Event oficial.
7. Verificar AuditId obligatorio e inmutable.
8. Verificar separación entre AuditId y SourceAggregateId.
9. Verificar separación entre AuditId y SourceEventId.
10. Verificar separación entre AuditId y EventId.
11. Verificar que el Source Fact debe estar confirmado.
12. Verificar que intenciones futuras no son hechos.
13. Verificar que Source Commands no son hechos automáticamente.
14. Verificar que Source Aggregate no se modifica.
15. Verificar que fallos de Audit no revierten Source Fact.
16. Verificar independencia entre SourceAggregateVersion y
    Audit.Version.
17. Verificar que información ausente no se fabrica.
18. Verificar tratamiento opcional de ActorId.
19. Verificar tratamiento opcional de CorrelationId.
20. Verificar tratamiento opcional de CausationId.
21. Verificar separación temporal entre SourceOccurredAt,
    CreatedAt y AuditRecorded.OccurredAt.
22. Verificar Version inicial igual a 1.
23. Verificar que No Audit no exige Version 0 persistida.
24. Verificar que operaciones rechazadas no incrementan Version.
25. Verificar que lecturas no incrementan Version.
26. Verificar que rehidratación no incrementa Version.
27. Verificar que replay no incrementa Version como nuevo hecho.
28. Verificar AggregateVersion de AuditRecorded.
29. Verificar EventId único e inmutable.
30. Verificar ausencia de AuditRecorded ante rechazo.
31. Verificar separación entre Authorization e Invariants.
32. Verificar Deny by Default.
33. Verificar que Permissions no alteran State Machine.
34. Verificar que Permissions no modifican identidad ni Version.
35. Verificar que Authentication permanece fuera del Aggregate.
36. Verificar que credenciales no forman parte de Audit.
37. Verificar minimización de Source Payload.
38. Verificar ausencia de estados Draft, Pending, Active, Failed,
    Cancelled, Archived y Deleted.
39. Verificar que Source Status no se hereda.
40. Verificar persistencia válida mediante Repository.
41. Verificar que Repository no corrige Aggregates inválidos.
42. Verificar que Repository no incrementa Version.
43. Verificar findById(), exists() y nextIdentity().
44. Verificar DuplicateAuditId.
45. Verificar AuditNotFound.
46. Verificar PersistenceFailure y RepositoryUnavailable.
47. Verificar Optimistic Concurrency.
48. Verificar ConcurrencyConflict.
49. Verificar que delete() no introduce DeleteAudit.
50. Verificar ausencia de Commands no oficiales.
51. Verificar ausencia de Domain Events no oficiales.
52. Verificar que retries técnicos no son comportamiento de dominio.
53. Verificar que Duplicate Delivery no crea nuevos hechos.
54. Verificar proyecciones desde AuditRecorded.
55. Verificar que Read Models no ejecutan Commands.
56. Verificar que Read Models no incrementan Version.
57. Verificar Projection Lag.
58. Verificar Projection Failure y Retry.
59. Verificar rebuild sin modificación del Aggregate.
60. Verificar consultas sin efectos sobre Write Model.
61. Verificar que Timeline y vistas globales no crean Aggregate
    global.
62. Verificar separación Domain Event / Integration Event.
63. Verificar publicación solamente después del commit.
64. Verificar fallos y retries de Integration sin modificación de
    Audit.
65. Verificar idempotencia mediante EventId.
66. Verificar Contract Version independiente de Audit.Version.
67. Verificar que Outbox no forma parte de AuditStatus.
68. Verificar desacoplamiento de FIWARE.
69. Verificar desacoplamiento de sistemas municipales.
70. Verificar que logs, metrics y traces no son Audit.
71. Verificar independencia de Organization, Citizen, Membership,
    Role, Territory, Assembly, Proposal, Participation, Voting,
    Document y Notification.
72. Verificar que nuevos Source Facts no reescriben Audits previos.
73. Verificar múltiples Audits como Consistency Boundaries
    independientes.
74. Verificar ausencia de Aggregate global.
75. Verificar que Batch Processing no fusiona identidades.
76. Verificar que CorrelationId no fusiona transacciones.
77. Verificar que CausationId no concede mutation authority.
78. Verificar Event Sourcing sin reproducción de nuevos hechos.
79. Verificar separación entre Source Event Stream y Audit Event
    Stream.
80. Verificar que Cache, Replica, Snapshot y Migration no modifican
    reglas de dominio.
81. Verificar independencia entre versiones técnicas y Audit.Version.
82. Verificar separación entre Read y Write Permissions.
83. Verificar que datos históricos no son públicos automáticamente.
84. Verificar minimización en Read Models.
85. Verificar minimización en Integration Events.
86. Verificar ausencia de recursividad automática.
87. Verificar que retención, expiración, anonimización y redacción no
    se infieren.
88. Verificar que optimizaciones no evitan Invariants ni amplían el
    Consistency Boundary.
89. Verificar que Test Scenarios no introducen nuevas reglas de
    dominio.

---

# Restricciones

No está permitido utilizar los Test Scenarios para:

- inventar estados;
- inventar Commands;
- inventar Domain Events;
- inventar Permissions;
- inventar Integration Events;
- introducir reglas de retención;
- introducir reglas de eliminación;
- introducir reglas de anonimización;
- introducir reglas de redacción;
- imponer Event Sourcing;
- imponer una base de datos;
- imponer un broker;
- imponer FIWARE;
- imponer una estrategia de idempotencia concreta;
- imponer una estrategia de retry concreta;
- introducir un Aggregate global;
- expandir el Consistency Boundary;
- reinterpretar Source Status como AuditStatus;
- utilizar expectativas técnicas como reglas del dominio.

---

# Compatibilidad Arquitectónica

Los Test Scenarios de Audit son compatibles con:

- Domain-Driven Design;
- Aggregate Pattern;
- Test-Driven Development;
- Behavior-Driven Development;
- Clean Architecture;
- Hexagonal Architecture;
- CQRS;
- Event-Driven Architecture;
- Event Sourcing Compatible;
- Optimistic Concurrency Control;
- Transactional Outbox;
- consistencia eventual;
- Property-Based Testing;
- Contract Testing;
- High Cohesion;
- Low Coupling.

Estas compatibilidades no introducen una herramienta de testing
obligatoria.

---

# Definición de Éxito

Los Test Scenarios del Aggregate **Audit** proporcionan una
especificación conceptual verificable de las reglas oficiales de la
versión 1.0.

Los escenarios garantizan que:

```text
Confirmed Source Fact

    │
    ▼

Authorized RecordAudit

    │
    ▼

Validate State Machine

    │
    ▼

Validate Invariants

    │
    ▼

No Audit → Recorded

    │
    ▼

Version = 1

    │
    ▼

AuditRecorded
```

permanezca como comportamiento central del Aggregate.

La cobertura conceptual verifica que:

- AuditId existe y permanece inmutable;
- Recorded es el único estado persistido;
- Recorded permanece terminal;
- RecordAudit es el único Command oficial;
- AuditRecorded es el único Domain Event oficial;
- el hecho auditable debe estar previamente confirmado;
- Source Commands no se confunden con hechos consumados;
- Audit no modifica ni revierte Source Aggregates;
- identidades y Versions externas permanecen separadas;
- información ausente no se fabrica;
- Version inicial es 1;
- operaciones rechazadas, lecturas, retries, replay y proyecciones no
  incrementan Version;
- Repository preserva el Aggregate sin gobernar su comportamiento;
- Optimistic Concurrency evita escrituras obsoletas;
- Authentication, Authorization y Domain Validation permanecen
  separadas;
- Permissions no permiten evitar Invariants ni State Machine;
- Read Models no adquieren autoridad de escritura;
- Domain Events e Integration Events permanecen separados;
- publicación externa ocurre después del commit;
- fallos de integración no provocan rollback;
- EventId permite reconocer hechos duplicados;
- Outbox y estados técnicos permanecen fuera del dominio;
- FIWARE y sistemas municipales permanecen desacoplados;
- Logs, Metrics y Traces permanecen fuera de Audit;
- otros Aggregates mantienen sus propios Consistency Boundaries;
- nuevos hechos no reescriben trazabilidad previa;
- múltiples Audits permanecen independientes;
- Event Sourcing es compatible sin quedar impuesto;
- retención, eliminación, anonimización y redacción no se infieren;
- optimizaciones técnicas no alteran las reglas conceptuales;
- los propios Test Scenarios verifican el dominio sin crear
  arquitectura nueva.

De esta forma, `DOMAIN-012M-Test-Scenarios.md` establece los Test
Scenarios oficiales del Aggregate **Audit** conforme al patrón
consolidado de AURA Core.