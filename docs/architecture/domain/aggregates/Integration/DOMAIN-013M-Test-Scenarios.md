# DOMAIN-013M — Integration Test Scenarios

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Integration Management

Aggregate:
Integration

Autor:
ARADA

Documentos Relacionados:

- DOMAIN-013-Aggregate.md
- DOMAIN-013A-Lifecycle.md
- DOMAIN-013B-State-Machine.md
- DOMAIN-013C-Commands.md
- DOMAIN-013D-Domain-Events.md
- DOMAIN-013E-Invariants.md
- DOMAIN-013F-Permissions.md
- DOMAIN-013G-Repository-Contract.md
- DOMAIN-013H-Examples.md
- DOMAIN-013I-Versioning.md
- DOMAIN-013J-Consistency-Boundary.md
- DOMAIN-013K-Integration-Events.md
- DOMAIN-013L-Read-Model.md
- DOMAIN-013N-Performance-Rules.md
- DOMAIN-013O-Security-Model.md
- DOMAIN-013P-Extension-Points.md

---

# Objetivo

Este documento define formalmente los **Test Scenarios** conceptuales
del Aggregate **Integration**.

Los escenarios permiten verificar que las reglas definidas por el
dominio permanezcan consistentes durante creación, evolución,
persistencia, concurrencia, interoperabilidad y lectura.

Los Test Scenarios no introducen comportamiento nuevo.

---

# Principio Fundamental

Debe mantenerse:

```text
Test Scenario

=

Verification of Existing Domain Rule
```

y:

```text
Test Scenario

≠

New Domain Rule
```

---

# Alcance

Los escenarios verifican:

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
- Read Model.

---

# No Arquitectura Nueva

Los Test Scenarios no determinan:

- framework de testing;
- lenguaje;
- runner;
- mocking library;
- base de datos;
- broker;
- protocolo;
- mecanismo de persistencia;
- mecanismo de mensajería;
- FIWARE;
- infraestructura municipal;
- estrategia de Event Sourcing;
- estrategia física de CQRS.

---

# Formato Conceptual

Los escenarios utilizan:

```text
Given

When

Then
```

como forma conceptual de expresar:

```text
Preconditions

Intent or Fact

Expected Domain Result
```

---

# Estados Oficiales

Los únicos States utilizados son:

```text
Draft

Active

Suspended

Archived
```

`No Integration` representa inexistencia.

---

# Commands Oficiales

Los únicos Commands utilizados son:

```text
CreateIntegration

ActivateIntegration

SuspendIntegration

ReactivateIntegration

ArchiveIntegration
```

---

# Domain Events Oficiales

Los únicos Domain Events utilizados son:

```text
IntegrationCreated

IntegrationActivated

IntegrationSuspended

IntegrationReactivated

IntegrationArchived
```

---

# Permissions Oficiales

Las Permissions oficiales utilizadas son:

```text
Integration.Create

Integration.Activate

Integration.Suspend

Integration.Reactivate

Integration.Archive
```

---

# Escenario 1 — Crear Integration

```text
Given

No Integration with IntegrationId = X

And

Integration.Create is allowed

When

CreateIntegration succeeds

Then

Integration exists

And

IntegrationId = X

And

State = Draft

And

Version = 1

And

IntegrationCreated is produced

And

IntegrationCreated.AggregateVersion = 1
```

---

# Escenario 2 — Creación sin Permission

```text
Given

No Integration with IntegrationId = X

And

Integration.Create is denied

When

CreateIntegration is attempted

Then

operation is rejected

And

No Integration remains

And

no IntegrationCreated is produced
```

---

# Escenario 3 — Creación Duplicada

```text
Given

IntegrationId = X already exists

When

CreateIntegration with IntegrationId = X is attempted

Then

operation is rejected

And

no second Integration with IntegrationId = X exists

And

no new IntegrationCreated is confirmed
```

---

# Escenario 4 — Estado Inicial Obligatorio

```text
Given

No Integration

When

CreateIntegration succeeds

Then

State = Draft
```

No debe resultar:

```text
Active

Suspended

Archived
```

---

# Escenario 5 — Version Inicial

```text
Given

No Integration

When

CreateIntegration succeeds

Then

Version = 1
```

---

# Escenario 6 — No Version 0 Persistida

```text
Given

No Integration

Then

no persisted Aggregate with Version = 0 exists
```

---

# Escenario 7 — Activar Draft

```text
Given

State = Draft

Version = N

And

Integration.Activate is allowed

When

ActivateIntegration succeeds

Then

State = Active

And

Version = N + 1

And

IntegrationActivated is produced

And

IntegrationActivated.AggregateVersion = N + 1
```

---

# Escenario 8 — Activar Active

```text
Given

State = Active

Version = N

When

ActivateIntegration is attempted

Then

operation is rejected

And

State = Active

And

Version = N

And

UpdatedAt remains unchanged

And

no new IntegrationActivated is produced
```

---

# Escenario 9 — Activar Suspended

```text
Given

State = Suspended

When

ActivateIntegration is attempted

Then

operation is rejected

And

State = Suspended
```

---

# Escenario 10 — Activar Archived

```text
Given

State = Archived

When

ActivateIntegration is attempted

Then

operation is rejected

And

State = Archived

And

no IntegrationActivated is produced
```

---

# Escenario 11 — Suspender Active

```text
Given

State = Active

Version = N

And

Integration.Suspend is allowed

When

SuspendIntegration succeeds

Then

State = Suspended

And

Version = N + 1

And

IntegrationSuspended is produced

And

IntegrationSuspended.AggregateVersion = N + 1
```

---

# Escenario 12 — Suspender Draft

```text
Given

State = Draft

When

SuspendIntegration is attempted

Then

operation is rejected

And

State = Draft

And

no IntegrationSuspended is produced
```

---

# Escenario 13 — Suspender Suspended

```text
Given

State = Suspended

When

SuspendIntegration is attempted

Then

operation is rejected

And

State = Suspended
```

---

# Escenario 14 — Suspender Archived

```text
Given

State = Archived

When

SuspendIntegration is attempted

Then

operation is rejected

And

State = Archived
```

---

# Escenario 15 — Reactivar Suspended

```text
Given

State = Suspended

Version = N

And

Integration.Reactivate is allowed

When

ReactivateIntegration succeeds

Then

State = Active

And

Version = N + 1

And

IntegrationReactivated is produced

And

IntegrationReactivated.AggregateVersion = N + 1
```

---

# Escenario 16 — Reactivar Draft

```text
Given

State = Draft

When

ReactivateIntegration is attempted

Then

operation is rejected

And

State = Draft
```

---

# Escenario 17 — Reactivar Active

```text
Given

State = Active

When

ReactivateIntegration is attempted

Then

operation is rejected

And

State = Active
```

---

# Escenario 18 — Reactivar Archived

```text
Given

State = Archived

Version = N

When

ReactivateIntegration is attempted

Then

operation is rejected

And

State = Archived

And

Version = N

And

UpdatedAt remains unchanged

And

no IntegrationReactivated is produced
```

---

# Escenario 19 — Archivar Draft

```text
Given

State = Draft

Version = N

And

Integration.Archive is allowed

When

ArchiveIntegration succeeds

Then

State = Archived

And

Version = N + 1

And

IntegrationArchived is produced

And

IntegrationArchived.AggregateVersion = N + 1
```

---

# Escenario 20 — Archivar Active

```text
Given

State = Active

Version = N

When

ArchiveIntegration succeeds

Then

State = Archived

And

Version = N + 1

And

IntegrationArchived is produced
```

---

# Escenario 21 — Archivar Suspended

```text
Given

State = Suspended

Version = N

When

ArchiveIntegration succeeds

Then

State = Archived

And

Version = N + 1

And

IntegrationArchived is produced
```

---

# Escenario 22 — Archivar Archived

```text
Given

State = Archived

Version = N

When

ArchiveIntegration is attempted

Then

operation is rejected

And

State = Archived

And

Version = N

And

no new IntegrationArchived is produced
```

---

# Escenario 23 — Archived es Terminal

```text
Given

State = Archived

When

any Lifecycle Command is attempted

Then

no valid State transition occurs
```

---

# Escenario 24 — No Regreso a Draft

```text
Given

Integration has already left Draft

When

any Command is attempted

Then

no transition back to Draft is allowed
```

---

# Escenario 25 — Active a Draft Prohibido

```text
Given

State = Active

Then

Active → Draft is invalid
```

---

# Escenario 26 — Suspended a Draft Prohibido

```text
Given

State = Suspended

Then

Suspended → Draft is invalid
```

---

# Escenario 27 — Archived a Active Prohibido

```text
Given

State = Archived

Then

Archived → Active is invalid
```

---

# Escenario 28 — Archived a Suspended Prohibido

```text
Given

State = Archived

Then

Archived → Suspended is invalid
```

---

# Escenario 29 — Archived a Archived no es Transición

```text
Given

State = Archived

When

ArchiveIntegration is attempted

Then

Archived → Archived is not accepted as a Lifecycle transition
```

---

# Escenario 30 — Lista Cerrada de Transiciones

```text
Given

a transition is not explicitly defined in DOMAIN-013B-State-Machine.md

When

the transition is attempted

Then

it is rejected
```

---

# Escenario 31 — IntegrationId Inmutable

```text
Given

IntegrationId = X

When

any valid Lifecycle modification occurs

Then

IntegrationId remains X
```

---

# Escenario 32 — CreatedAt Inmutable

```text
Given

CreatedAt = T1

When

ActivateIntegration

And

SuspendIntegration

And

ReactivateIntegration

And

ArchiveIntegration

occur validly

Then

CreatedAt remains T1
```

---

# Escenario 33 — UpdatedAt Cambia por Modificación Válida

```text
Given

UpdatedAt = T1

When

a valid Aggregate modification succeeds

Then

UpdatedAt represents the new valid modification time
```

---

# Escenario 34 — UpdatedAt no Cambia por Rechazo

```text
Given

UpdatedAt = T1

When

a Command is rejected

Then

UpdatedAt remains T1
```

---

# Escenario 35 — Version Incrementa una Vez

```text
Given

Version = N

When

one valid Aggregate modification succeeds

Then

Version = N + 1
```

---

# Escenario 36 — Version no Salta

```text
Given

Version = N

When

one valid Aggregate modification succeeds

Then

Version ≠ N + 2
```

---

# Escenario 37 — Version no Retrocede

```text
Given

Version = N

When

valid domain behavior occurs

Then

resulting Version > N

And

Version never becomes N - 1
```

---

# Escenario 38 — Version no Cambia ante Rechazo

```text
Given

Version = N

When

a Command is rejected

Then

Version = N
```

---

# Escenario 39 — Domain Event AggregateVersion

```text
Given

Version = N

When

a valid modification produces Version = N + 1

Then

DomainEvent.AggregateVersion = N + 1
```

---

# Escenario 40 — EventId Diferente de IntegrationId

```text
Given

IntegrationId = X

And

EventId = Y

Then

EventId identifies the Domain Event

And

IntegrationId identifies the Aggregate

And

both concepts remain distinct
```

---

# Escenario 41 — Un EventId por Hecho

```text
Given

EventId = E1 represents one confirmed Domain Fact

Then

E1 is not reused for another distinct Domain Fact
```

---

# Escenario 42 — Command Rechazado no Produce Evento de Éxito

```text
Given

a Command fails State Machine validation

When

the Command is rejected

Then

no corresponding success Domain Event is produced
```

---

# Escenario 43 — Invariant Failure

```text
Given

a Command is otherwise applicable

But

an Invariant fails

When

the operation is evaluated

Then

operation is rejected

And

State remains unchanged

And

Version remains unchanged

And

UpdatedAt remains unchanged

And

no success Domain Event is produced
```

---

# Escenario 44 — Guard Failure

```text
Given

a required Guard is not satisfied

When

a Command is attempted

Then

operation is rejected

And

no partial Aggregate modification exists
```

---

# Escenario 45 — Permission Denied

```text
Given

State permits the requested transition

But

required Permission is denied

When

the Command is attempted

Then

operation is rejected

And

State remains unchanged

And

Version remains unchanged

And

UpdatedAt remains unchanged

And

no success Domain Event is produced
```

---

# Escenario 46 — Permission no Sustituye State Machine

```text
Given

Permission is allowed

But

current State does not permit the Command

When

the Command is attempted

Then

operation is rejected
```

---

# Escenario 47 — Permission no Sustituye Invariant

```text
Given

Permission is allowed

But

an Invariant is violated

When

the Command is attempted

Then

operation is rejected
```

---

# Escenario 48 — Permission no Sustituye Versioning

```text
Given

Permission is allowed

And

ExpectedVersion does not match PersistedVersion

When

a modification is attempted

Then

ConcurrencyConflict occurs
```

---

# Escenario 49 — ActorId no es Permission

```text
Given

ActorId = X

When

a protected Command is attempted

Then

ActorId alone does not imply Authorization
```

---

# Escenario 50 — CorrelationId no es Permission

```text
Given

CorrelationId = C

When

a protected Command is attempted

Then

CorrelationId does not grant Permission
```

---

# Escenario 51 — CausationId no es Permission

```text
Given

CausationId = C

When

a protected Command is attempted

Then

CausationId does not grant Permission
```

---

# Escenario 52 — Optimistic Concurrency Válida

```text
Given

PersistedVersion = 5

And

ExpectedVersion = 5

And

the Command is valid

When

the modification is confirmed

Then

Integration.Version = 6
```

---

# Escenario 53 — ConcurrencyConflict

```text
Given

PersistedVersion = 5

And

ExpectedVersion = 4

When

a modification is attempted

Then

ConcurrencyConflict occurs

And

PersistedVersion remains 5

And

persisted State remains unchanged

And

persisted UpdatedAt remains unchanged

And

no new success Domain Event is confirmed
```

---

# Escenario 54 — No Silent Overwrite

```text
Given

a concurrent modification already produced Version = N + 1

When

another operation attempts to persist using ExpectedVersion = N

Then

existing revision is not silently overwritten
```

---

# Escenario 55 — Different IntegrationId Concurrency

```text
Given

Integration A has Version = 5

And

Integration B has Version = 3

Then

each Aggregate maintains an independent Version sequence
```

---

# Escenario 56 — No Version Global

```text
Given

multiple Integration Aggregates exist

Then

no shared global Integration Version is required
```

---

# Escenario 57 — Repository save()

```text
Given

a valid Integration Aggregate

When

IntegrationRepository.save() succeeds

Then

Aggregate identity, State, Version and domain information are persisted
```

---

# Escenario 58 — Repository no Ejecuta Command

```text
Given

State = Draft

When

IntegrationRepository.save() is called

Then

State does not become Active merely because of save()
```

---

# Escenario 59 — Repository Round-Trip

```text
Given

IntegrationId = X

State = Suspended

Version = 5

When

save()

And

findById(X)

Then

IntegrationId = X

State = Suspended

Version = 5
```

---

# Escenario 60 — findById() no Modifica Aggregate

```text
Given

Integration Version = N

When

findById() retrieves the Aggregate

Then

Version remains N

And

UpdatedAt remains unchanged

And

no new Domain Event is produced
```

---

# Escenario 61 — IntegrationNotFound

```text
Given

IntegrationId = X does not exist

When

findById(X)

Then

IntegrationNotFound is represented

And

no Failed State is created
```

---

# Escenario 62 — exists()

```text
Given

IntegrationId = X exists

When

exists(X)

Then

true is returned

And

Aggregate remains unchanged
```

---

# Escenario 63 — exists() para Inexistencia

```text
Given

IntegrationId = X does not exist

When

exists(X)

Then

false is returned
```

---

# Escenario 64 — nextIdentity()

```text
Given

a new Integration identity is required

When

nextIdentity() is invoked

Then

a valid IntegrationId is provided

And

no Integration Aggregate is created
```

---

# Escenario 65 — delete() no es Archive

```text
Given

Repository.delete() exists in the Repository Contract

Then

Repository.delete()

≠

ArchiveIntegration
```

---

# Escenario 66 — Archived no Ejecuta delete()

```text
Given

ArchiveIntegration succeeds

And

State = Archived

Then

Repository.delete() is not automatically implied
```

---

# Escenario 67 — Sin Política de Retención Inferida

```text
Given

State = Archived

Then

no retention period

And

no purge schedule

And

no automatic deletion

is inferred
```

---

# Escenario 68 — Consistency Boundary por IntegrationId

```text
Given

IntegrationId = X

When

a valid modification occurs

Then

only Integration X is modified inside its Aggregate Boundary
```

---

# Escenario 69 — No Cross-Aggregate Mutation

```text
Given

Integration X executes a valid Command

Then

Organization remains outside the transaction

And

Citizen remains outside the transaction

And

Assembly remains outside the transaction

And

Notification remains outside the transaction

And

Audit remains outside the transaction
```

---

# Escenario 70 — No External System Transaction

```text
Given

Integration X confirms a valid State transition

Then

no external system commit is required to belong to the same Aggregate transaction
```

---

# Escenario 71 — FIWARE Fuera del Boundary

```text
Given

Integration interoperates with FIWARE

When

Integration is modified

Then

FIWARE does not become part of the Aggregate Consistency Boundary
```

---

# Escenario 72 — Sistema Municipal Fuera del Boundary

```text
Given

Integration interoperates with a Municipal System

When

Integration is modified

Then

Municipal System does not become part of the Aggregate Consistency Boundary
```

---

# Escenario 73 — Source Aggregate Fuera del Boundary

```text
Given

a fact originated in another Aggregate

When

Integration later processes a related valid intention

Then

Source Aggregate remains outside Integration Boundary
```

---

# Escenario 74 — Source Commit Independiente

```text
Given

another Aggregate confirms a Domain Fact

Then

Source Aggregate Commit

≠

Integration Commit
```

---

# Escenario 75 — External Failure no Revierte Integration

```text
Given

Integration State = Active

And

Version = N

And

the Aggregate modification is already confirmed

When

an external system later fails

Then

State remains Active

And

Version remains N
```

---

# Escenario 76 — External Recovery no Reactiva

```text
Given

Integration State = Suspended

When

an external system becomes available

Then

State remains Suspended

And

no IntegrationReactivated is produced
```

---

# Escenario 77 — Timeout no Suspende

```text
Given

State = Active

When

a technical timeout occurs

Then

State remains Active

And

no IntegrationSuspended is produced
```

---

# Escenario 78 — Broker Failure no Suspende

```text
Given

State = Active

When

broker becomes unavailable

Then

State remains Active
```

---

# Escenario 79 — FIWARE Failure no Suspende

```text
Given

State = Active

When

FIWARE becomes unavailable

Then

State remains Active
```

---

# Escenario 80 — Municipal Failure no Suspende

```text
Given

State = Active

When

Municipal System becomes unavailable

Then

State remains Active
```

---

# Escenario 81 — Credential Expiration no Cambia State

```text
Given

State = Active

When

an external technical credential expires

Then

Integration State remains Active
```

---

# Escenario 82 — Credential Rotation no Incrementa Version

```text
Given

Integration.Version = N

When

Infrastructure rotates a credential outside the Aggregate

Then

Integration.Version remains N
```

---

# Escenario 83 — Authentication Failure no Cambia Aggregate

```text
Given

Integration State = Active

Version = N

When

Authentication fails before a protected operation

Then

Integration State remains Active

And

Version remains N
```

---

# Escenario 84 — Authorization Failure no Cambia Aggregate

```text
Given

Integration State = Active

Version = N

When

Authorization denies SuspendIntegration

Then

State remains Active

And

Version remains N

And

no IntegrationSuspended is produced
```

---

# Escenario 85 — Permission Change no Modifica Aggregate

```text
Given

Integration State = Active

Version = N

When

an external Authorization Policy changes

Then

State remains Active

And

Version remains N

And

UpdatedAt remains unchanged
```

---

# Escenario 86 — External Message no es Command

```text
Given

an external message contains an "activate" instruction

When

it reaches AURA

Then

it is not treated automatically as ActivateIntegration
```

---

# Escenario 87 — Integration Event Entrante no Modifica Directamente

```text
Given

an incoming Integration Event

When

it is received

Then

it does not execute direct State mutation

And

it must be interpreted through its explicit contract
```

---

# Escenario 88 — External State no Mapea Automáticamente

```text
Given

external status = OFFLINE

And

Integration State = Active

When

the external status is observed

Then

Integration State remains Active unless an explicit domain rule produces a valid Command
```

---

# Escenario 89 — External ENABLED no Activa

```text
Given

Integration State = Draft

And

external status = ENABLED

Then

Integration remains Draft
```

---

# Escenario 90 — External DISABLED no Suspende

```text
Given

Integration State = Active

And

external status = DISABLED

Then

Integration remains Active
```

---

# Escenario 91 — Domain Event no es Integration Event

```text
Given

IntegrationActivated is confirmed

Then

IntegrationActivated remains a Domain Event

And

no Integration Event is inferred automatically
```

---

# Escenario 92 — Sin Contrato no hay Integration Event Obligatorio

```text
Given

a confirmed Integration Domain Event

And

no explicit Integration Contract requires external publication

Then

no mandatory Integration Event exists
```

---

# Escenario 93 — Contrato Explícito

```text
Given

a confirmed Domain Fact

And

an explicit external contract requires that fact to cross a boundary

When

the interoperability contract is applied

Then

an Integration Event may be produced according to that contract
```

---

# Escenario 94 — Payload Mínimo de Integration Event

```text
Given

an explicit Integration Event contract

When

an Integration Event is produced

Then

only contractually necessary information is included
```

---

# Escenario 95 — No Snapshot Completo en Integration Event

```text
Given

an Integration Event is produced

Then

full Integration Aggregate state is not exposed by default
```

---

# Escenario 96 — Sin Credenciales en Integration Event

```text
Given

Infrastructure has external credentials

When

an Integration Event is produced

Then

Password is absent

And

AccessToken is absent

And

RefreshToken is absent

And

ApiKey is absent

And

PrivateKey is absent

And

ClientSecret is absent

And

Secret is absent
```

---

# Escenario 97 — Publication Failure no Revierte Aggregate

```text
Given

IntegrationActivated is already confirmed

And

Integration State = Active

Version = N

When

publication toward an external consumer fails

Then

State remains Active

And

Version remains N
```

---

# Escenario 98 — Retry de Publicación no Crea Hecho Nuevo

```text
Given

the same Integration Event publication is retried

When

technical retry occurs

Then

no new Integration Domain Event is created

And

Integration.Version remains unchanged
```

---

# Escenario 99 — Redelivery no Crea Hecho Nuevo

```text
Given

the same technical Integration Event is delivered more than once

Then

repeated delivery is not interpreted automatically as multiple Domain Facts
```

---

# Escenario 100 — No Exactly Once Inferido

```text
Given

Integration Events are used

Then

Exactly Once is not inferred as a universal domain guarantee
```

---

# Escenario 101 — No At Least Once Inferido

```text
Given

Integration Events are used

Then

At Least Once is not inferred as a universal domain guarantee
```

---

# Escenario 102 — No At Most Once Inferido

```text
Given

Integration Events are used

Then

At Most Once is not inferred as a universal domain guarantee
```

---

# Escenario 103 — No Global Ordering

```text
Given

Integration INT-001 has AggregateVersion = 7

And

Integration INT-002 has AggregateVersion = 4

Then

no global event order between both Aggregates is inferred
```

---

# Escenario 104 — Read Model Query

```text
Given

a projected Integration Read Model

When

it is queried

Then

Integration Aggregate remains unchanged
```

---

# Escenario 105 — Query no Incrementa Version

```text
Given

Integration.Version = N

When

a Query is executed

Then

Integration.Version remains N
```

---

# Escenario 106 — Query no Modifica UpdatedAt

```text
Given

Integration.UpdatedAt = T1

When

a Query is executed

Then

Integration.UpdatedAt remains T1
```

---

# Escenario 107 — Query no Produce Domain Event

```text
Given

a Read Model exists

When

Search, Filter, Sort or Pagination is performed

Then

no Integration Domain Event is produced
```

---

# Escenario 108 — Projection Lag

```text
Given

Aggregate State = Suspended

Aggregate Version = 5

And

Read Model State = Active

Read Model projected Version = 4

Then

Aggregate State and Version remain authoritative for writes
```

---

# Escenario 109 — Projection Failure

```text
Given

IntegrationSuspended is confirmed

When

Projection processing fails

Then

Integration remains Suspended

And

Integration.Version remains unchanged by the Projection failure
```

---

# Escenario 110 — Projection Retry

```text
Given

Projection processing is retried

Then

no new IntegrationSuspended Domain Event is produced

And

Integration.Version remains unchanged
```

---

# Escenario 111 — Projection Rebuild

```text
Given

a Read Model must be rebuilt

When

confirmed information is replayed for Projection purposes

Then

no Integration Command is re-executed

And

no new Integration Domain Fact is created
```

---

# Escenario 112 — Read Model no es Write Authority

```text
Given

Read Model State = Draft

And

Aggregate State = Active

When

a write operation is evaluated

Then

Aggregate State is authoritative
```

---

# Escenario 113 — Stale Read no Evita Concurrencia

```text
Given

Read Model projected Version = 4

And

Aggregate PersistedVersion = 5

When

a write attempt uses ExpectedVersion = 4

Then

ConcurrencyConflict occurs
```

---

# Escenario 114 — Joined Read Model no Fusiona Aggregates

```text
Given

a Read Model combines Integration and Organization information

Then

Integration and Organization remain separate Aggregate Boundaries
```

---

# Escenario 115 — Read Aggregation no Fusiona Boundaries

```text
Given

a Query aggregates multiple Integration records

Then

their individual Consistency Boundaries remain independent
```

---

# Escenario 116 — Archived Sigue Siendo Consultable Conceptualmente

```text
Given

Integration State = Archived

When

a permitted Query is executed

Then

Archived information may remain represented

And

no Lifecycle transition occurs
```

---

# Escenario 117 — Read Model Failure no Suspende

```text
Given

Integration State = Active

When

Read Model becomes unavailable

Then

Integration State remains Active
```

---

# Escenario 118 — Read Model Recovery no Reactiva

```text
Given

Integration State = Suspended

When

Read Model becomes available again

Then

Integration remains Suspended
```

---

# Escenario 119 — Replay no Reejecuta Commands

```text
Given

historical Integration Domain Events exist

When

Replay is performed

Then

CreateIntegration

ActivateIntegration

SuspendIntegration

ReactivateIntegration

ArchiveIntegration

are not re-executed as new Commands
```

---

# Escenario 120 — Replay no Produce Hechos Nuevos

```text
Given

existing Domain Events are replayed

Then

no new IntegrationCreated

And

no new IntegrationActivated

And

no new IntegrationSuspended

And

no new IntegrationReactivated

And

no new IntegrationArchived

are produced as new facts
```

---

# Escenario 121 — Rehydration Preserva State

```text
Given

persisted State = Active

When

Integration is rehydrated

Then

State = Active
```

---

# Escenario 122 — Rehydration Preserva Version

```text
Given

persisted Version = N

When

Integration is rehydrated

Then

Version = N
```

---

# Escenario 123 — Rehydration no Produce Domain Event

```text
Given

an existing Integration is rehydrated

Then

no new Domain Event is produced
```

---

# Escenario 124 — Event Sourcing no Obligatorio

```text
Given

Integration follows all domain contracts

Then

Event Sourcing is not required for domain validity
```

---

# Escenario 125 — CQRS no Obligatorio

```text
Given

Integration follows all domain contracts

Then

a physical CQRS implementation is not required for domain validity
```

---

# Escenario 126 — External Payload no es Aggregate State

```text
Given

an external payload contains technical and business information

When

it is received

Then

its entire content is not automatically persisted as Integration state
```

---

# Escenario 127 — Información Ausente no se Fabrica

```text
Given

an external contract does not provide ActorId

When

the information is interpreted

Then

ActorId is not fabricated as a historical fact
```

---

# Escenario 128 — Secrets Fuera del Aggregate

```text
Given

Infrastructure stores credentials

When

Integration is persisted

Then

Password is absent from Aggregate state

And

AccessToken is absent

And

RefreshToken is absent

And

ApiKey is absent

And

PrivateKey is absent

And

ClientSecret is absent

And

Secret is absent
```

---

# Escenario 129 — Secrets Fuera de Domain Events

```text
Given

a valid Integration Domain Event is produced

Then

credentials and secrets are absent from the Domain Event payload
```

---

# Escenario 130 — Secrets Fuera de Read Models

```text
Given

Infrastructure credentials exist

When

Integration information is projected

Then

credentials are absent from the Domain Read Model
```

---

# Escenario 131 — Active no Significa Connected

```text
Given

Integration State = Active

Then

technical connectivity is not implied
```

---

# Escenario 132 — Suspended no Significa Disconnected

```text
Given

Integration State = Suspended

Then

technical disconnection is not implied
```

---

# Escenario 133 — Archived no Significa Deleted

```text
Given

Integration State = Archived

Then

physical deletion is not implied
```

---

# Escenario 134 — Failed no es State

```text
Given

a technical failure occurs

Then

Integration State does not become Failed
```

---

# Escenario 135 — Pending no es State

```text
Given

a technical process is pending

Then

Integration State does not become Pending
```

---

# Escenario 136 — Processing no es State

```text
Given

Infrastructure is processing a message

Then

Integration State does not become Processing
```

---

# Escenario 137 — Retrying no es State

```text
Given

Infrastructure retries an operation

Then

Integration State does not become Retrying
```

---

# Escenario 138 — Healthy no es State

```text
Given

technical health = Healthy

Then

Integration Lifecycle State remains independently defined
```

---

# Escenario 139 — Unhealthy no es State

```text
Given

technical health = Unhealthy

Then

Integration State is not changed automatically
```

---

# Escenario 140 — Deployment no Modifica Aggregate

```text
Given

Integration State = Active

Version = N

When

Infrastructure is deployed

Then

State remains Active

And

Version remains N
```

---

# Escenario 141 — Restart no Modifica Aggregate

```text
Given

Integration State = Active

Version = N

When

a service restarts

Then

State remains Active

And

Version remains N
```

---

# Escenario 142 — Cache no Modifica Aggregate

```text
Given

Integration.Version = N

When

a cache hit, miss or invalidation occurs

Then

Integration.Version remains N
```

---

# Escenario 143 — Queue no Modifica Aggregate

```text
Given

Integration State = Active

When

Queue State changes

Then

Integration State remains Active
```

---

# Escenario 144 — Outbox no Modifica Aggregate

```text
Given

Integration.Version = N

When

an external publication mechanism changes its technical state

Then

Integration.Version remains N
```

---

# Escenario 145 — Broker ACK no Modifica Aggregate

```text
Given

Integration.Version = N

When

a broker acknowledgement occurs

Then

Integration.Version remains N
```

---

# Escenario 146 — Monitoring no Modifica Aggregate

```text
Given

Integration State = Active

When

monitoring reports latency or errors

Then

Integration State remains unchanged
```

---

# Escenario 147 — Metrics no Modifican Version

```text
Given

Integration.Version = N

When

latency, throughput or error metrics change

Then

Integration.Version remains N
```

---

# Escenario 148 — Contract Version Independiente

```text
Given

Integration.Version = 5

And

Integration Contract Version = 2

Then

both versions remain semantically distinct
```

---

# Escenario 149 — API Version Independiente

```text
Given

Integration.Version = 7

And

API Version = 3

Then

API Version does not determine Integration.Version
```

---

# Escenario 150 — Schema Version Independiente

```text
Given

Integration.Version = N

When

an external schema version changes

Then

Integration.Version remains N unless a valid Aggregate modification occurs
```

---

# Escenario 151 — External Version Independiente

```text
Given

Integration.Version = 4

And

External System Version = 18

Then

both versions remain independent
```

---

# Escenario 152 — Audit Version Independiente

```text
Given

Integration.Version = 5

And

Audit.Version = 3

Then

both Aggregate versions remain independent
```

---

# Escenario 153 — Notification Version Independiente

```text
Given

Integration.Version = 5

And

Notification.Version = 2

Then

both Aggregate versions remain independent
```

---

# Escenario 154 — Audit Failure no Revierte Integration

```text
Given

IntegrationArchived is confirmed

And

State = Archived

When

Audit processing later fails

Then

Integration remains Archived
```

---

# Escenario 155 — Notification Failure no Revierte Integration

```text
Given

IntegrationSuspended is confirmed

When

a related Notification later fails

Then

Integration remains Suspended
```

---

# Escenario 156 — Consumer Failure no Revierte Integration

```text
Given

IntegrationActivated is confirmed

When

an external consumer fails

Then

Integration remains Active
```

---

# Escenario 157 — No Domain Event desde Repository Error

```text
Given

RepositoryUnavailable occurs

Then

IntegrationFailed is not produced

And

no new Lifecycle State is introduced
```

---

# Escenario 158 — PersistenceFailure no Crea Failed

```text
Given

PersistenceFailure occurs

Then

Failed is not introduced as Integration State
```

---

# Escenario 159 — DuplicateIntegrationId no Crea State

```text
Given

DuplicateIntegrationId occurs

Then

no Failed

And

no Pending

And

no Deleted

State is introduced
```

---

# Escenario 160 — ConcurrencyConflict no Crea State

```text
Given

ConcurrencyConflict occurs

Then

Integration State remains its last confirmed State
```

---

# Escenario 161 — No setState()

```text
Given

an attempt is made to change State directly

Then

the operation is not considered valid domain behavior
```

---

# Escenario 162 — No setVersion()

```text
Given

an attempt is made to set Version directly

Then

the operation is not considered valid domain behavior
```

---

# Escenario 163 — No UpdateIntegration Genérico

```text
Given

UpdateIntegration is requested

Then

it is not recognized as an official version 1.0 Command
```

---

# Escenario 164 — No ModifyIntegration Genérico

```text
Given

ModifyIntegration is requested

Then

it is not recognized as an official version 1.0 Command
```

---

# Escenario 165 — No ConnectIntegration

```text
Given

ConnectIntegration is requested

Then

it is not recognized as an official version 1.0 Command
```

---

# Escenario 166 — No DisconnectIntegration

```text
Given

DisconnectIntegration is requested

Then

it is not recognized as an official version 1.0 Command
```

---

# Escenario 167 — No RetryIntegration

```text
Given

RetryIntegration is requested

Then

it is not recognized as an official version 1.0 Command
```

---

# Escenario 168 — No DeleteIntegration

```text
Given

DeleteIntegration is requested

Then

it is not recognized as an official version 1.0 Command
```

---

# Escenario 169 — No IntegrationConnected

```text
Given

a technical connection succeeds

Then

IntegrationConnected is not inferred as an official Domain Event
```

---

# Escenario 170 — No IntegrationDisconnected

```text
Given

a technical connection is lost

Then

IntegrationDisconnected is not inferred as an official Domain Event
```

---

# Escenario 171 — No IntegrationFailed

```text
Given

a technical operation fails

Then

IntegrationFailed is not inferred as an official Domain Event
```

---

# Escenario 172 — No IntegrationRetried

```text
Given

a technical retry occurs

Then

IntegrationRetried is not inferred as an official Domain Event
```

---

# Escenario 173 — No IntegrationDeleted

```text
Given

Integration is Archived

Then

IntegrationDeleted is not inferred as an official Domain Event
```

---

# Escenario 174 — No IntegrationUpdated Genérico

```text
Given

ActivateIntegration succeeds

Then

IntegrationActivated is the semantic Domain Event

And

IntegrationUpdated is not substituted for it
```

---

# Escenario 175 — No Permission Técnica Inferida

```text
Given

a technical endpoint exists

Then

no new domain Permission is inferred from that endpoint
```

---

# Escenario 176 — FIWARE Authorization no es AURA Permission

```text
Given

a requester is authorized in FIWARE

Then

Integration.Activate is not automatically granted
```

---

# Escenario 177 — Municipal Authorization no es AURA Permission

```text
Given

a requester is authorized in a Municipal System

Then

Integration permissions are not automatically granted
```

---

# Escenario 178 — Infrastructure Access no es Permission

```text
Given

a requester has technical database access

Then

no Integration domain Permission is inferred
```

---

# Escenario 179 — Read Permission no es Write Permission

```text
Given

a requester can read an Integration Read Model

Then

Integration.Activate

And

Integration.Suspend

And

Integration.Reactivate

And

Integration.Archive

are not automatically granted
```

---

# Escenario 180 — Write Permission no es Autoridad Universal

```text
Given

Integration.Activate is allowed

Then

Integration.Suspend

And

Integration.Archive

are not automatically inferred as allowed
```

---

# Escenario 181 — No Internal Entity Inferida

```text
Given

Infrastructure uses multiple persistence records

Then

no new Integration Internal Entity is inferred from that structure
```

---

# Escenario 182 — No Value Object Inferido

```text
Given

Infrastructure uses a technical URL value

Then

no Integration-specific Value Object is inferred automatically
```

---

# Escenario 183 — No Cardinalidad Inferida

```text
Given

one external message exists

Then

no one-to-one cardinality with Integration is inferred automatically
```

---

# Escenario 184 — No Auto-Archive por Tiempo

```text
Given

Integration remains Active over time

When

time passes without an explicit valid Command

Then

State remains Active
```

---

# Escenario 185 — No Expired State

```text
Given

an external date expires

Then

Expired is not introduced as Integration State
```

---

# Escenario 186 — No Scheduled Suspension

```text
Given

a technical schedule reaches a configured time

Then

SuspendIntegration is not inferred automatically as domain behavior
```

---

# Escenario 187 — No Scheduled Archive

```text
Given

a technical schedule reaches a configured time

Then

ArchiveIntegration is not inferred automatically as domain behavior
```

---

# Escenario 188 — Protocol Independence

```text
Given

external transport changes from one protocol to another

Then

IntegrationId remains unchanged

And

Lifecycle rules remain unchanged

And

State Machine remains unchanged
```

---

# Escenario 189 — Broker Independence

```text
Given

Infrastructure replaces one broker with another

Then

Integration domain behavior remains unchanged
```

---

# Escenario 190 — Persistence Independence

```text
Given

Infrastructure replaces the persistence technology

Then

IntegrationId

State

Version

CreatedAt

UpdatedAt

and domain semantics

remain preserved
```

---

# Escenario 191 — No FIWARE Internal Model

```text
Given

AURA interoperates with FIWARE

Then

FIWARE Entity is not treated as an Integration Internal Entity
```

---

# Escenario 192 — No Municipal Internal Model

```text
Given

AURA interoperates with a Municipal System

Then

the Municipal System model is not absorbed into Integration
```

---

# Escenario 193 — No NGSI-LD Requirement

```text
Given

Integration Events are conceptually defined

Then

NGSI-LD is not required universally by the domain
```

---

# Escenario 194 — No Broker Requirement

```text
Given

Domain Events or Integration Events exist

Then

no broker technology is required by the domain definition
```

---

# Escenario 195 — No Outbox Requirement

```text
Given

external publication may occur

Then

Transactional Outbox is not inferred as a mandatory domain mechanism
```

---

# Escenario 196 — No Inbox Requirement

```text
Given

Integration Events may be consumed

Then

Inbox Pattern is not inferred as mandatory
```

---

# Escenario 197 — No Dead Letter Requirement

```text
Given

technical delivery may fail

Then

Dead Letter Queue is not inferred as a mandatory domain mechanism
```

---

# Escenario 198 — No Retry Policy Inferida

```text
Given

a technical delivery fails

Then

retry count

retry delay

backoff

and retry schedule

are not defined by this Aggregate
```

---

# Escenario 199 — No Saga Requirement

```text
Given

multiple Boundaries participate in a larger process

Then

Saga is not inferred as a mandatory domain mechanism
```

---

# Escenario 200 — No Process Manager Requirement

```text
Given

multiple Boundaries participate in a larger process

Then

Process Manager is not inferred as a mandatory domain mechanism
```

---

# Escenario 201 — No Two-Phase Commit Requirement

```text
Given

Integration collaborates with an external system

Then

Two-Phase Commit is not inferred as a mandatory domain mechanism
```

---

# Escenario 202 — No Distributed Aggregate

```text
Given

Integration interoperates with an external platform

Then

Integration plus external platform do not become one Aggregate
```

---

# Escenario 203 — Batch no Fusiona Boundaries

```text
Given

INT-001

INT-002

INT-003

are processed in one technical batch

Then

each retains its own State

Version

Invariants

and Consistency Boundary
```

---

# Escenario 204 — Performance no Rompe Invariants

```text
Given

an optimization is introduced

Then

State Machine

Invariants

Versioning

and Consistency Boundary

remain unchanged
```

---

# Escenario 205 — Performance no Fusiona Aggregates

```text
Given

a high-throughput optimization is introduced

Then

multiple Integration Aggregates remain separate Consistency Boundaries
```

---

# Escenario 206 — Event Sourcing Replay Preserva Version

```text
Given

confirmed historical Domain Events end at AggregateVersion = N

When

the Aggregate is replayed

Then

Integration.Version = N
```

---

# Escenario 207 — Event Sourcing Replay no Incrementa Version

```text
Given

historical Domain Events are replayed

Then

Version does not increment merely because replay occurs
```

---

# Escenario 208 — SourceAggregateVersion Independiente

```text
Given

a source fact contains SourceAggregateVersion = S

And

Integration.Version = I

Then

S and I remain separate concepts unless the source fact explicitly represents Integration itself
```

---

# Escenario 209 — CorrelationId no Fusiona Boundaries

```text
Given

Integration and another Aggregate share CorrelationId = C

Then

both Aggregates remain separate Consistency Boundaries
```

---

# Escenario 210 — CausationId no Fusiona Boundaries

```text
Given

a Domain Fact references CausationId = C

Then

causal relation does not transfer ownership or merge Aggregate Boundaries
```

---

# Escenario 211 — Read Composition no Transfiere Ownership

```text
Given

a Read Model combines Integration and Audit information

Then

Integration ownership remains with Integration

And

Audit ownership remains with Audit
```

---

# Escenario 212 — Read Aggregation no Crea Aggregate Global

```text
Given

a Query returns all Active Integration records

Then

no GlobalIntegrationAggregate is created
```

---

# Escenario 213 — Technical Redelivery no es Nueva Intención

```text
Given

the same technical representation of an intention is delivered twice

Then

two separate Domain Intentions are not inferred automatically
```

---

# Escenario 214 — Idempotencia no se Decide

```text
Given

technical redelivery is possible

Then

no specific idempotency mechanism is inferred by the domain
```

---

# Escenario 215 — Deduplicación no se Decide

```text
Given

duplicated technical messages are possible

Then

no specific deduplication technology or algorithm is inferred
```

---

# Escenario 216 — Domain Event Histórico Inmutable

```text
Given

IntegrationSuspended was confirmed at AggregateVersion = 3

When

Integration later becomes Active again

Then

the historical IntegrationSuspended event remains unchanged
```

---

# Escenario 217 — Historical State no es Current State

```text
Given

IntegrationSuspended exists historically

And

IntegrationReactivated later occurs

Then

historical State = Suspended does not mean current State remains Suspended
```

---

# Escenario 218 — Archived no Reinicia Version

```text
Given

State = Active

Version = 7

When

ArchiveIntegration succeeds

Then

State = Archived

And

Version = 8
```

---

# Escenario 219 — Reactivation no Reinicia Version

```text
Given

State = Suspended

Version = 6

When

ReactivateIntegration succeeds

Then

State = Active

And

Version = 7
```

---

# Escenario 220 — Same State, Different Version

```text
Given

Integration was Active at Version = 2

Then

Suspended at Version = 3

Then

Reactivated to Active at Version = 4

Then

State may be Active again

And

Version remains monotonic
```

---

# Escenario 221 — No Version Reset

```text
Given

Integration.Version = N

Then

no ResetIntegrationVersion behavior exists
```

---

# Escenario 222 — No Technical Version Mapping

```text
Given

Database Revision = D

And

Integration.Version = I

Then

D does not automatically define I
```

---

# Escenario 223 — Timestamp no es Version

```text
Given

UpdatedAt = T

And

Integration.Version = N

Then

T and N remain separate concepts
```

---

# Escenario 224 — Event Contract Version no es AggregateVersion

```text
Given

Integration Event Contract Version = C

And

SourceAggregateVersion = S

Then

C and S remain semantically distinct
```

---

# Escenario 225 — Read Model Field no Crea Aggregate Attribute

```text
Given

a Read Model introduces a derived field for query purposes

Then

the derived field is not automatically added to Integration Aggregate state
```

---

# Escenario 226 — Read Model Technical Status no Crea Lifecycle State

```text
Given

a Read Model displays Technical Health = Degraded

Then

Degraded is not introduced into Integration Lifecycle
```

---

# Escenario 227 — Query Histórica no Obliga Historial Interno

```text
Given

users need a historical query

Then

Integration Aggregate is not required to embed a query-oriented history collection
```

---

# Escenario 228 — Reporting no Amplía Repository

```text
Given

reporting is required

Then

reporting operations are not automatically added to IntegrationRepository
```

---

# Escenario 229 — Analytics no Amplía Aggregate

```text
Given

analytics are required

Then

no new Integration domain behavior is inferred
```

---

# Escenario 230 — Search no Crea Invariant

```text
Given

a search capability is required

Then

no new Aggregate Invariant is inferred
```

---

# Escenario 231 — No Auto-Mapping de Domain Event a Integration Event

```text
Given

IntegrationArchived is confirmed

Then

IntegrationArchivedIntegrationEvent is not inferred automatically
```

---

# Escenario 232 — Consumer Authorization no Concede Write Permission

```text
Given

an external consumer is authorized to receive an Integration Event

Then

that consumer is not automatically granted Integration.Archive or any other write Permission
```

---

# Escenario 233 — Integration Event no Cambia UpdatedAt

```text
Given

Integration.UpdatedAt = T1

When

an Integration Event is published

Then

Integration.UpdatedAt remains T1
```

---

# Escenario 234 — Integration Event no Cambia CreatedAt

```text
Given

Integration.CreatedAt = T1

When

an Integration Event is published

Then

Integration.CreatedAt remains T1
```

---

# Escenario 235 — Integration Event no Cambia State

```text
Given

Integration State = Active

When

an external publication occurs

Then

Integration State remains Active
```

---

# Escenario 236 — Read Model no es FIWARE Entity

```text
Given

a Read Model exposes Integration information related to FIWARE

Then

the Read Model is not treated as an Integration Aggregate or FIWARE Entity by domain definition
```

---

# Escenario 237 — External Model no Sustituye AURA Model

```text
Given

an external system exposes its own schema

Then

the schema does not automatically redefine Integration attributes, States, Commands or Invariants
```

---

# Escenario 238 — New Endpoint no Crea Command

```text
Given

Infrastructure adds a new endpoint

Then

no new Integration Command is inferred automatically
```

---

# Escenario 239 — New Broker Operation no Crea Domain Event

```text
Given

a broker introduces a new technical operation

Then

no new Integration Domain Event is inferred automatically
```

---

# Escenario 240 — New External Status no Crea State

```text
Given

an external provider introduces status = PAUSED

Then

Paused is not introduced automatically into Integration Lifecycle
```

---

# Escenario 241 — Nuevo Consumer no Expande Boundary

```text
Given

a new external consumer is added

Then

Integration Consistency Boundary remains unchanged unless a formal domain decision changes it
```

---

# Escenario 242 — Nuevo Read Model no Expande Boundary

```text
Given

a new Read Model is introduced

Then

Integration Consistency Boundary remains unchanged
```

---

# Escenario 243 — Nueva Tecnología no Modifica Dominio

```text
Given

Infrastructure technology changes

Then

Lifecycle

State Machine

Commands

Domain Events

Invariants

Permissions

Versioning

and Consistency Boundary

remain conceptually unchanged
```

---

# Escenario 244 — Nuevo Integration Event Requiere Contrato

```text
Given

a new external communication need appears

When

no explicit Integration Contract has been defined

Then

no new official Integration Event is inferred
```

---

# Escenario 245 — Nuevo State Requiere Definición Formal

```text
Given

a technical requirement suggests a new State

Then

the State is not part of Integration until formally defined across the affected domain contracts
```

---

# Escenario 246 — Nuevo Command Requiere Definición Formal

```text
Given

a new technical action is required

Then

no new Integration Command exists until a real domain intent is formally defined
```

---

# Escenario 247 — Nuevo Domain Event Requiere Hecho Real

```text
Given

a new technical occurrence exists

Then

no new Integration Domain Event exists unless it represents a real confirmed domain fact
```

---

# Escenario 248 — Nueva Permission Requiere Capability

```text
Given

a new technical operation exists

Then

no new Integration Permission is introduced unless a real domain capability exists
```

---

# Escenario 249 — Nuevo Campo de Projection no Crea Dominio

```text
Given

a new Read Model field is useful for reporting

Then

no new Integration Aggregate attribute is inferred
```

---

# Escenario 250 — Test de Regla de No Inferencia

```text
Given

a requirement belongs to Infrastructure or an external system

When

it is evaluated against Integration

Then

no new State

Command

Domain Event

Permission

Invariant

Aggregate member

Repository operation

Integration Event

or architectural mechanism

is inferred without explicit domain definition
```

---

# Matriz de Transiciones Válidas

```text
Current State      Command                  Resulting State

No Integration     CreateIntegration        Draft

Draft              ActivateIntegration      Active

Draft              ArchiveIntegration       Archived

Active             SuspendIntegration       Suspended

Active             ArchiveIntegration       Archived

Suspended          ReactivateIntegration    Active

Suspended          ArchiveIntegration       Archived
```

---

# Matriz de Transiciones Inválidas

```text
Current State      Command                  Result

Draft              SuspendIntegration       Rejected

Draft              ReactivateIntegration    Rejected

Active             ActivateIntegration      Rejected

Active             ReactivateIntegration    Rejected

Suspended          ActivateIntegration      Rejected

Suspended          SuspendIntegration       Rejected

Archived           ActivateIntegration      Rejected

Archived           SuspendIntegration       Rejected

Archived           ReactivateIntegration    Rejected

Archived           ArchiveIntegration       Rejected
```

---

# Matriz Command / Domain Event

```text
Command                  Domain Event

CreateIntegration        IntegrationCreated

ActivateIntegration      IntegrationActivated

SuspendIntegration       IntegrationSuspended

ReactivateIntegration    IntegrationReactivated

ArchiveIntegration       IntegrationArchived
```

solamente cuando el Command es aceptado.

---

# Matriz Command / Permission

```text
Command                  Permission

CreateIntegration        Integration.Create

ActivateIntegration      Integration.Activate

SuspendIntegration       Integration.Suspend

ReactivateIntegration    Integration.Reactivate

ArchiveIntegration       Integration.Archive
```

---

# Matriz de Resultado Válido

```text
Valid Command
    │
    ▼
Permission Allowed
    │
    ▼
State Valid
    │
    ▼
Guards Valid
    │
    ▼
Invariants Valid
    │
    ▼
Version Valid
    │
    ▼
Aggregate Modification
    │
    ▼
Version Increment
    │
    ▼
UpdatedAt Updated
    │
    ▼
Domain Event
```

---

# Matriz de Resultado Rechazado

```text
Rejected Operation
    │
    ├── State unchanged
    ├── Version unchanged
    ├── UpdatedAt unchanged
    └── no success Domain Event
```

---

# Cobertura de Lifecycle

Los Test Scenarios deben cubrir:

```text
Creation

Activation

Suspension

Reactivation

Archive

Terminal State behavior

Invalid transitions
```

---

# Cobertura de Commands

Deben cubrirse:

```text
successful Command

unauthorized Command

invalid-State Command

Guard failure

Invariant failure

Version conflict
```

---

# Cobertura de Domain Events

Debe verificarse:

```text
correct EventType

correct IntegrationId

correct EventId semantics

correct AggregateVersion

correct resulting State

correct OccurredAt semantics

CorrelationId when applicable

CausationId when applicable

minimum necessary Payload

no credentials

no success event on rejection
```

---

# Cobertura de Versioning

Debe verificarse:

```text
initial Version = 1

valid modification increments Version once

rejected operation does not increment Version

ExpectedVersion comparison

ConcurrencyConflict

no silent overwrite

no global Version

Version monotonicity

AggregateVersion correspondence
```

---

# Cobertura de Repository

Debe verificarse:

```text
save()

findById()

exists()

nextIdentity()

delete() semantic separation

Aggregate round-trip

duplicate identity rejection

concurrency preservation

no Repository-driven domain behavior
```

---

# Cobertura de Consistency Boundary

Debe verificarse:

```text
one IntegrationId

one Aggregate Boundary

no cross-Aggregate mutation

no external system inside Aggregate

no FIWARE inside Aggregate

no Municipal System inside Aggregate

eventual external consistency

no mandatory distributed transaction
```

---

# Cobertura de Integration Events

Debe verificarse:

```text
Domain Event ≠ Integration Event

no automatic external publication

explicit contract required

no direct incoming-event mutation

minimal payload

no secrets

publication failure does not rollback Aggregate

retry does not create new Domain Fact

no delivery guarantee inferred
```

---

# Cobertura de Read Model

Debe verificarse:

```text
Query does not mutate Aggregate

Projection has no Write Authority

Projection Lag is allowed

Projection Failure does not rollback Aggregate

Projection Replay creates no new Domain Facts

Read composition does not merge Aggregate Boundaries

Read fields do not create Aggregate attributes
```

---

# Cobertura de Security

Debe verificarse:

```text
Authentication outside Aggregate

Permission before protected behavior

Permission does not bypass State Machine

Permission does not bypass Invariants

Permission does not bypass Versioning

no credentials in Aggregate

no credentials in Domain Events

no credentials in Integration Events

no credentials in Domain Read Model
```

---

# Cobertura de Independencia Tecnológica

Debe verificarse conceptualmente que un cambio de:

```text
protocol

broker

persistence technology

framework

external provider

FIWARE availability

municipal system availability
```

no redefina las reglas internas del Aggregate.

---

# Test de Regresión Conceptual

Toda evolución futura debe mantener escenarios que demuestren que las
reglas previamente válidas continúan siendo válidas salvo cambio formal
del dominio.

---

# Nueva Regla Requiere Nuevo Test

Debe mantenerse:

```text
New Domain Rule

requires

Corresponding Test Scenario
```

cuando dicha regla requiera comportamiento verificable.

---

# Nuevo State

La incorporación futura de un State requiere escenarios para:

- entrada;
- salida;
- transiciones válidas;
- transiciones inválidas;
- Commands;
- Domain Events;
- Invariants;
- Versioning;
- terminalidad cuando corresponda.

---

# Nuevo Command

Todo nuevo Command debe incluir escenarios para:

```text
valid execution

invalid State

missing Permission

Guard failure

Invariant failure

ConcurrencyConflict

Domain Event result
```

---

# Nuevo Domain Event

Todo nuevo Domain Event debe verificar:

```text
correct source behavior

correct AggregateVersion

correct EventType

correct identity

minimum Payload

historical immutability
```

---

# Nueva Permission

Toda nueva Permission debe verificar:

```text
allowed intent

denied intent

inability to bypass State Machine

inability to bypass Invariants

inability to bypass Versioning
```

---

# Nueva Repository Operation

Toda nueva operación futura del Repository debe verificar que:

```text
it remains persistence behavior

it does not become Aggregate behavior

it preserves Consistency Boundary

it preserves Versioning

it does not become Read-side analytics
```

---

# Nuevo Integration Event

Todo nuevo Integration Event concreto deberá verificar:

```text
explicit contract exists

source fact exists

Payload is minimal

no secrets are exposed

ownership is preserved

publication does not modify Aggregate

consumer failure does not rollback Aggregate
```

---

# Nuevo Read Model

Todo nuevo Read Model deberá verificar:

```text
Query purpose exists

no Write Authority

no Aggregate mutation

no Boundary merge

no ownership transfer

no secret exposure
```

---

# Impacto de Evolución

La evolución de los Test Scenarios debe mantener coherencia con:

```text
DOMAIN-013-Aggregate.md

DOMAIN-013A-Lifecycle.md

DOMAIN-013B-State-Machine.md

DOMAIN-013C-Commands.md

DOMAIN-013D-Domain-Events.md

DOMAIN-013E-Invariants.md

DOMAIN-013F-Permissions.md

DOMAIN-013G-Repository-Contract.md

DOMAIN-013H-Examples.md

DOMAIN-013I-Versioning.md

DOMAIN-013J-Consistency-Boundary.md

DOMAIN-013K-Integration-Events.md

DOMAIN-013L-Read-Model.md

DOMAIN-013N-Performance-Rules.md

DOMAIN-013O-Security-Model.md

DOMAIN-013P-Extension-Points.md
```

---

# Regla de No Inferencia

Debe mantenerse:

```text
Test Convenience

≠

Domain Rule
```

y:

```text
Test Framework Capability

≠

Domain Requirement
```

y:

```text
Mocked Infrastructure Behavior

≠

Integration Lifecycle Rule
```

y:

```text
Technical Failure Scenario

≠

New Domain State
```

---

# Reglas Fundamentales

Los Test Scenarios de Integration deben cumplir:

1. Los tests verifican reglas existentes.
2. Los tests no crean reglas de dominio.
3. Los tests no introducen arquitectura.
4. Toda creación válida termina en Draft.
5. Toda creación válida comienza en Version 1.
6. IntegrationId permanece inmutable.
7. CreatedAt permanece inmutable.
8. UpdatedAt cambia solamente por modificación válida.
9. ActivateIntegration solamente funciona desde Draft.
10. SuspendIntegration solamente funciona desde Active.
11. ReactivateIntegration solamente funciona desde Suspended.
12. ArchiveIntegration funciona desde Draft, Active o Suspended.
13. Archived es terminal.
14. No existe retorno a Draft.
15. Transiciones no definidas son rechazadas.
16. Commands rechazados no modifican State.
17. Commands rechazados no modifican Version.
18. Commands rechazados no modifican UpdatedAt.
19. Commands rechazados no producen Domain Event de éxito.
20. Permission no sustituye State Machine.
21. Permission no sustituye Invariants.
22. Permission no sustituye Versioning.
23. Permission Failure no modifica el Aggregate.
24. ActorId no es Permission.
25. CorrelationId no es Permission.
26. CausationId no es Permission.
27. Toda modificación válida incrementa Version una vez.
28. Version es monotónica.
29. Version no retrocede.
30. Version no se reinicia.
31. Event AggregateVersion coincide con Version resultante.
32. EventId identifica un hecho distinto de IntegrationId.
33. ConcurrencyConflict rechaza escrituras incompatibles.
34. Silent Overwrite está prohibido.
35. Different IntegrationId mantienen Version independiente.
36. No existe Version global.
37. Repository persiste sin ejecutar Commands.
38. Repository round-trip preserva identidad, State y Version.
39. findById() no modifica el Aggregate.
40. exists() no modifica el Aggregate.
41. nextIdentity() no crea Integration.
42. Repository.delete() no es ArchiveIntegration.
43. Archived no implica delete().
44. No existe política de retención inferida.
45. Un IntegrationId representa un Consistency Boundary.
46. Otros Aggregates permanecen fuera del Boundary.
47. Sistemas externos permanecen fuera del Boundary.
48. FIWARE permanece fuera del Boundary.
49. Sistemas municipales permanecen fuera del Boundary.
50. Source Aggregate Commit no es Integration Commit.
51. External System Commit no es Integration Commit.
52. Consistencia externa permanece eventual.
53. External Failure no revierte Integration automáticamente.
54. External Recovery no reactiva Integration automáticamente.
55. Timeout no suspende Integration.
56. Broker Failure no suspende Integration.
57. FIWARE Failure no suspende Integration.
58. Municipal System Failure no suspende Integration.
59. Credential Expiration no cambia State.
60. Credential Rotation no incrementa Version por sí misma.
61. Authentication Failure no cambia Aggregate.
62. Authorization Failure no cambia Aggregate.
63. Permission Policy Change no cambia Aggregate.
64. External Message no es Command automático.
65. Incoming Integration Event no modifica directamente Integration.
66. External State no se mapea automáticamente al Lifecycle.
67. Domain Event no es Integration Event.
68. No existe publicación externa automática.
69. Integration Event concreto requiere contrato explícito.
70. Integration Event Payload debe ser mínimo.
71. Integration Events no contienen credenciales.
72. Publication Failure no revierte Aggregate.
73. Retry de publicación no crea Domain Fact.
74. Redelivery no crea Domain Fact automáticamente.
75. No se infiere Exactly Once.
76. No se infiere At Least Once.
77. No se infiere At Most Once.
78. No existe orden global obligatorio.
79. Queries no modifican Aggregate.
80. Queries no incrementan Version.
81. Queries no modifican UpdatedAt.
82. Queries no producen Domain Events.
83. Projection Lag es permitido bajo consistencia eventual.
84. Projection Failure no revierte Aggregate.
85. Projection Retry no crea Domain Facts.
86. Projection Rebuild no reejecuta Commands.
87. Read Model no es Write Authority.
88. Stale Read no evita ConcurrencyConflict.
89. Joined Read Model no fusiona Aggregates.
90. Read Aggregation no crea Global Aggregate.
91. Replay no reejecuta Commands.
92. Replay no crea nuevos hechos.
93. Rehydration preserva State y Version.
94. Event Sourcing no es obligatorio.
95. CQRS físico no es obligatorio.
96. External Payload no se copia automáticamente al Aggregate.
97. Información ausente no se fabrica.
98. Secrets permanecen fuera de Aggregate, Events y Read Models.
99. Ningún Test Scenario introduce una decisión arquitectónica nueva.
100. Toda evolución futura debe mantener cobertura coherente con los
     contratos oficiales de Integration.

---

# Restricciones

No está permitido utilizar Test Scenarios para:

- introducir nuevos States;
- introducir nuevas transiciones;
- introducir nuevos Commands;
- introducir nuevos Domain Events;
- introducir nuevas Permissions;
- introducir nuevas Invariants;
- introducir nuevos Repository methods;
- introducir Internal Entities;
- introducir Value Objects;
- introducir Integration Events concretos sin contrato;
- introducir mecanismos técnicos de publicación;
- introducir estrategias de retry;
- introducir estrategias de idempotencia;
- introducir estrategias de deduplicación;
- imponer Exactly Once;
- imponer At Least Once;
- imponer At Most Once;
- imponer Global Ordering;
- imponer Event Sourcing;
- imponer CQRS físico;
- imponer Transactional Outbox;
- imponer Inbox Pattern;
- imponer Dead Letter Queue;
- imponer Saga;
- imponer Process Manager;
- imponer Two-Phase Commit;
- imponer broker;
- imponer protocolo;
- imponer base de datos;
- imponer framework;
- imponer FIWARE;
- imponer NGSI-LD;
- imponer arquitectura municipal;
- convertir errores técnicos en States;
- convertir fallos de publicación en Lifecycle transitions;
- convertir eventos externos directamente en Commands;
- fusionar Aggregate Boundaries;
- ignorar Versioning por conveniencia de testing;
- ignorar Permissions por conveniencia de testing;
- ignorar Invariants por conveniencia de testing;
- ignorar State Machine por conveniencia de testing;
- considerar mocks como reglas del dominio;
- convertir resultados técnicos de tests en decisiones arquitectónicas.

---

# Compatibilidad Arquitectónica

Los Test Scenarios son compatibles conceptualmente con:

- Domain-Driven Design;
- Aggregate Pattern;
- State Machine Pattern;
- Command Pattern;
- Domain Event Pattern;
- Repository Pattern;
- Clean Architecture;
- Hexagonal Architecture;
- SOLID;
- CQRS;
- Event-Driven Architecture;
- Event Sourcing Compatible;
- Optimistic Concurrency Control;
- consistencia eventual;
- High Cohesion;
- Low Coupling.

Estas compatibilidades no imponen ninguna tecnología o herramienta de
testing.

---

# Definición de Éxito

Los Test Scenarios del Aggregate **Integration** permiten verificar de
forma consistente que las reglas oficiales del dominio permanecen
protegidas frente a operaciones válidas, inválidas, concurrentes,
externas y derivadas.

El modelo de verificación fundamental queda expresado como:

```text
Given

Valid or Invalid Preconditions
    │
    ▼
When

Domain Intent or External Condition
    │
    ▼
Then

Expected Integration Domain Result
```

donde una modificación válida debe satisfacer:

```text
Valid Permission

Valid State

Valid Guards

Valid Invariants

Valid Version

    │
    ▼

Aggregate Modification

    │
    ▼

Version Increment

    │
    ▼

Domain Event
```

mientras una operación rechazada debe satisfacer:

```text
State unchanged

Version unchanged

UpdatedAt unchanged

No success Domain Event
```

El conjunto de escenarios garantiza que:

- Lifecycle permanezca cerrado y explícito;
- State Machine rechace transiciones no definidas;
- Commands expresen únicamente intenciones oficiales;
- Domain Events representen únicamente hechos confirmados;
- Invariants no puedan evitarse;
- Permissions no garanticen éxito;
- Versioning proteja concurrencia;
- IntegrationId permanezca inmutable;
- Repository preserve el Aggregate sin ejecutar comportamiento;
- Consistency Boundary permanezca limitado a una Integration;
- sistemas externos permanezcan fuera del Aggregate;
- FIWARE permanezca fuera del Aggregate;
- sistemas municipales permanezcan fuera del Aggregate;
- External Failure no se convierta en State;
- Domain Event e Integration Event permanezcan separados;
- contratos explícitos sean necesarios para interoperabilidad externa;
- Integration Events no introduzcan write authority;
- Read Models permanezcan derivados y sin autoridad de escritura;
- Projection Lag y Projection Failure no modifiquen el Aggregate;
- Replay y Rehydration no produzcan hechos nuevos;
- Event Sourcing permanezca compatible pero no obligatorio;
- CQRS permanezca compatible pero no obligatorio;
- credenciales y secretos permanezcan fuera del dominio;
- tecnología externa no redefina Lifecycle, Version o Consistency
  Boundary;
- ningún escenario sea utilizado para introducir arquitectura no
  definida.

De esta forma, `DOMAIN-013M-Test-Scenarios.md` establece formalmente
los Test Scenarios oficiales del Aggregate **Integration** conforme al
patrón consolidado de AURA Core.