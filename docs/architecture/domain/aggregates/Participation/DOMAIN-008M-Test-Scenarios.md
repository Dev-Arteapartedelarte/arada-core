# DOMAIN-008M — Participation Test Scenarios

Versión: 1.0

Estado:
Oficial

Proyecto:
AURA Core

Bounded Context:
Participation Management

Aggregate:
Participation

Autor:
ARADA

Documentos Relacionados:

- DOMAIN-008-Aggregate.md
- DOMAIN-008A-Lifecycle.md
- DOMAIN-008B-State-Machine.md
- DOMAIN-008C-Commands.md
- DOMAIN-008D-Domain-Events.md
- DOMAIN-008E-Invariants.md
- DOMAIN-008F-Permissions.md
- DOMAIN-008G-Repository-Contract.md
- DOMAIN-008H-Examples.md
- DOMAIN-008I-Versioning.md
- DOMAIN-008J-Consistency-Boundary.md
- DOMAIN-008K-Integration-Events.md
- DOMAIN-008L-Read-Model.md

---

# Objetivo

Definir los escenarios oficiales de prueba del Aggregate
**Participation**.

Los Test Scenarios permiten verificar que el comportamiento
conceptual definido para Participation preserve:

- identidad;
- pertenencia organizacional;
- Lifecycle;
- State Machine;
- Commands;
- Domain Events;
- Invariants;
- Permissions;
- persistencia;
- Versioning;
- Consistency Boundary;
- Integration Events;
- Read Models.

Los escenarios definidos en este documento verifican reglas del
dominio ya establecidas.

No introducen nuevas reglas, estados, Commands, Events,
Permissions ni decisiones arquitectónicas.

---

# Principios

Los escenarios de prueba deben cumplir las siguientes reglas.

- cada escenario verifica comportamiento del dominio;
- cada escenario parte de un estado conocido;
- cada escenario expresa una intención concreta;
- cada escenario define un resultado esperado;
- los escenarios válidos deben preservar todas las Invariants;
- los escenarios inválidos no deben modificar el Aggregate;
- los escenarios inválidos no deben incrementar Version;
- los escenarios inválidos no deben generar Domain Events de
  éxito;
- la autorización se prueba separadamente de las Invariants;
- la concurrencia se prueba mediante Version;
- los otros Aggregates permanecen fuera del Consistency Boundary;
- los Read Models se verifican como proyecciones derivadas;
- los Integration Events se verifican como contratos posteriores
  a hechos confirmados.

---

# Estructura de un Escenario

Cada escenario puede representarse conceptualmente mediante:

```text
Given

Estado inicial y precondiciones

↓

When

Command o acción

↓

Then

Resultado esperado
```

Cuando corresponda también debe verificarse:

```text
ParticipationStatus

Version

Domain Event

Lifecycle Timestamp

Repository Result
```

---

# Categorías de Prueba

Los escenarios oficiales se organizan en:

```text
Creation Scenarios

Lifecycle Scenarios

State Machine Scenarios

Invariant Scenarios

Permission Scenarios

Versioning Scenarios

Repository Scenarios

Consistency Boundary Scenarios

Domain Event Scenarios

Integration Event Scenarios

Read Model Scenarios

Rehydration Scenarios

Concurrency Scenarios
```

---

# Registro de Participation

## TS-001 — Registro Válido

Given.

```text
Participation does not exist

Valid ParticipationId

Valid OrganizationId

Valid ParticipationType

Valid required context

Authorized Actor
```

When.

```text
RegisterParticipation
```

Then.

```text
ParticipationStatus = Registered

Version = 1

ParticipationRegistered
```

El Aggregate debe quedar creado en un estado válido.

---

## TS-002 — Registro con ParticipationId Inválido

Given.

```text
Invalid ParticipationId
```

When.

```text
RegisterParticipation
```

Then.

```text
Rejected

No Aggregate Created

No Valid Version

No ParticipationRegistered
```

---

## TS-003 — Registro con OrganizationId Ausente

Given.

```text
OrganizationId not defined
```

When.

```text
RegisterParticipation
```

Then.

```text
Rejected

No Aggregate Created

No ParticipationRegistered
```

OrganizationId es obligatorio.

---

## TS-004 — Registro con ParticipationType Inválido

Given.

```text
Invalid ParticipationType
```

When.

```text
RegisterParticipation
```

Then.

```text
Rejected

No Aggregate Created

No ParticipationRegistered
```

---

## TS-005 — Registro con Identidad Duplicada

Given.

```text
ParticipationId = PAR-001

Already exists
```

When.

```text
RegisterParticipation

ParticipationId = PAR-001
```

Then.

```text
Rejected

Duplicate Identity
```

No debe crearse un segundo Aggregate con la misma identidad.

---

# Activation

## TS-006 — Activación Válida

Given.

```text
ParticipationStatus = Registered

Version = 1

Participation.Activate = Granted
```

When.

```text
ActivateParticipation
```

Then.

```text
ParticipationStatus = Active

StartedAt defined

Version = 2

ParticipationActivated
```

---

## TS-007 — Activación desde Active

Given.

```text
ParticipationStatus = Active

Version = N
```

When.

```text
ActivateParticipation
```

Then.

```text
Rejected

ParticipationStatus = Active

Version = N

No ParticipationActivated
```

---

## TS-008 — Activación desde Completed

Given.

```text
ParticipationStatus = Completed

Version = N
```

When.

```text
ActivateParticipation
```

Then.

```text
Rejected

Version = N

No ParticipationActivated
```

---

## TS-009 — Activación desde Withdrawn

Given.

```text
ParticipationStatus = Withdrawn

Version = N
```

When.

```text
ActivateParticipation
```

Then.

```text
Rejected

Version = N
```

---

## TS-010 — Activación desde Invalidated

Given.

```text
ParticipationStatus = Invalidated

Version = N
```

When.

```text
ActivateParticipation
```

Then.

```text
Rejected

Version = N
```

---

## TS-011 — Activación desde Archived

Given.

```text
ParticipationStatus = Archived

Version = N
```

When.

```text
ActivateParticipation
```

Then.

```text
Rejected

ParticipationStatus = Archived

Version = N
```

Archived permanece como estado terminal.

---

# Completion

## TS-012 — Completion Válida

Given.

```text
ParticipationStatus = Active

StartedAt defined

Version = N

Participation.Complete = Granted
```

When.

```text
CompleteParticipation
```

Then.

```text
ParticipationStatus = Completed

CompletedAt defined

Version = N + 1

ParticipationCompleted
```

---

## TS-013 — Completion desde Registered

Given.

```text
ParticipationStatus = Registered

Version = N
```

When.

```text
CompleteParticipation
```

Then.

```text
Rejected

ParticipationStatus = Registered

Version = N

No ParticipationCompleted
```

---

## TS-014 — Completion sin StartedAt

Given.

```text
ParticipationStatus = Active

StartedAt not defined
```

When.

```text
CompleteParticipation
```

Then.

```text
Rejected
```

La operación no puede producir un estado Completed que viole las
Invariants temporales.

---

## TS-015 — Completion desde Archived

Given.

```text
ParticipationStatus = Archived

Version = N
```

When.

```text
CompleteParticipation
```

Then.

```text
Rejected

Version = N
```

---

# Withdrawal

## TS-016 — Withdrawal desde Registered

Given.

```text
ParticipationStatus = Registered

Version = N

Participation.Withdraw = Granted
```

When.

```text
WithdrawParticipation
```

Then.

```text
ParticipationStatus = Withdrawn

WithdrawnAt defined

Version = N + 1

ParticipationWithdrawn
```

---

## TS-017 — Withdrawal desde Active

Given.

```text
ParticipationStatus = Active

StartedAt defined

Version = N
```

When.

```text
WithdrawParticipation
```

Then.

```text
ParticipationStatus = Withdrawn

StartedAt preserved

WithdrawnAt defined

Version = N + 1

ParticipationWithdrawn
```

---

## TS-018 — Withdrawal desde Completed

Given.

```text
ParticipationStatus = Completed

Version = N
```

When.

```text
WithdrawParticipation
```

Then.

```text
Rejected

Version = N
```

---

## TS-019 — Withdrawal desde Invalidated

Given.

```text
ParticipationStatus = Invalidated

Version = N
```

When.

```text
WithdrawParticipation
```

Then.

```text
Rejected

Version = N
```

---

## TS-020 — Withdrawal desde Archived

Given.

```text
ParticipationStatus = Archived

Version = N
```

When.

```text
WithdrawParticipation
```

Then.

```text
Rejected

Version = N
```

---

# Invalidation

## TS-021 — Invalidation desde Registered

Given.

```text
ParticipationStatus = Registered

Version = N

Participation.Invalidate = Granted
```

When.

```text
InvalidateParticipation
```

Then.

```text
ParticipationStatus = Invalidated

InvalidatedAt defined

Version = N + 1

ParticipationInvalidated
```

---

## TS-022 — Invalidation desde Active

Given.

```text
ParticipationStatus = Active

StartedAt defined

Version = N
```

When.

```text
InvalidateParticipation
```

Then.

```text
ParticipationStatus = Invalidated

StartedAt preserved

InvalidatedAt defined

Version = N + 1

ParticipationInvalidated
```

---

## TS-023 — Invalidation desde Completed

Given.

```text
ParticipationStatus = Completed

CompletedAt defined

Version = N
```

When.

```text
InvalidateParticipation
```

Then.

```text
ParticipationStatus = Invalidated

CompletedAt preserved

InvalidatedAt defined

Version = N + 1

ParticipationInvalidated
```

La invalidación no reescribe el hecho histórico de Completion.

---

## TS-024 — Invalidation desde Withdrawn

Given.

```text
ParticipationStatus = Withdrawn

Version = N
```

When.

```text
InvalidateParticipation
```

Then.

```text
Rejected

Version = N
```

---

## TS-025 — Invalidation desde Archived

Given.

```text
ParticipationStatus = Archived

Version = N
```

When.

```text
InvalidateParticipation
```

Then.

```text
Rejected

Version = N
```

---

# Archive

## TS-026 — Archive desde Completed

Given.

```text
ParticipationStatus = Completed

CompletedAt defined

Version = N

Participation.Archive = Granted
```

When.

```text
ArchiveParticipation
```

Then.

```text
ParticipationStatus = Archived

CompletedAt preserved

ArchivedAt defined

Version = N + 1

ParticipationArchived
```

---

## TS-027 — Archive desde Withdrawn

Given.

```text
ParticipationStatus = Withdrawn

WithdrawnAt defined

Version = N
```

When.

```text
ArchiveParticipation
```

Then.

```text
ParticipationStatus = Archived

WithdrawnAt preserved

ArchivedAt defined

Version = N + 1

ParticipationArchived
```

---

## TS-028 — Archive desde Invalidated

Given.

```text
ParticipationStatus = Invalidated

InvalidatedAt defined

Version = N
```

When.

```text
ArchiveParticipation
```

Then.

```text
ParticipationStatus = Archived

InvalidatedAt preserved

ArchivedAt defined

Version = N + 1

ParticipationArchived
```

---

## TS-029 — Archive desde Registered

Given.

```text
ParticipationStatus = Registered

Version = N
```

When.

```text
ArchiveParticipation
```

Then.

```text
Rejected

Version = N
```

---

## TS-030 — Archive desde Active

Given.

```text
ParticipationStatus = Active

Version = N
```

When.

```text
ArchiveParticipation
```

Then.

```text
Rejected

Version = N
```

---

## TS-031 — Modificación después de Archive

Given.

```text
ParticipationStatus = Archived

Version = N
```

When.

```text
ChangeParticipationType
```

Then.

```text
Rejected

Version = N
```

No se permiten modificaciones ordinarias sobre una Participation
Archived.

---

# Identidad

## TS-032 — ParticipationId Inmutable

Given.

```text
ParticipationId = PAR-001

Version = N
```

When.

```text
Attempt to change ParticipationId
```

Then.

```text
Rejected

ParticipationId = PAR-001

Version = N
```

---

## TS-033 — OrganizationId Inmutable

Given.

```text
OrganizationId = ORG-001

Version = N
```

When.

```text
Attempt to change OrganizationId to ORG-002
```

Then.

```text
Rejected

OrganizationId = ORG-001

Version = N
```

---

## TS-034 — Identidad no Reutilizable después de Archive

Given.

```text
ParticipationId = PAR-001

ParticipationStatus = Archived
```

When.

```text
RegisterParticipation

ParticipationId = PAR-001
```

Then.

```text
Rejected
```

La identidad permanece asociada al Aggregate archivado.

---

# ParticipationType

## TS-035 — Cambio de Tipo Válido

Given.

```text
ParticipationType = TypeA

State allows modification

Version = N

Participation.ChangeType = Granted
```

When.

```text
ChangeParticipationType

NewParticipationType = TypeB
```

Then.

```text
ParticipationType = TypeB

Version = N + 1

ParticipationTypeChanged
```

---

## TS-036 — Cambio de Tipo sin Modificación Efectiva

Given.

```text
ParticipationType = TypeA

Version = N
```

When.

```text
ChangeParticipationType

NewParticipationType = TypeA
```

Then.

```text
ParticipationType = TypeA

Version = N

No ParticipationTypeChanged
```

---

## TS-037 — Cambio de Tipo Inválido

Given.

```text
Version = N
```

When.

```text
ChangeParticipationType

Invalid ParticipationType
```

Then.

```text
Rejected

Version = N
```

---

## TS-038 — Cambio de Tipo sobre Archived

Given.

```text
ParticipationStatus = Archived

Version = N
```

When.

```text
ChangeParticipationType
```

Then.

```text
Rejected

Version = N
```

---

# Contexto

## TS-039 — Cambio de Contexto Válido

Given.

```text
State allows modification

Current Context valid

Version = N

Participation.ChangeContext = Granted
```

When.

```text
ChangeParticipationContext
```

Then.

```text
New Context preserved

Version = N + 1

ParticipationContextChanged
```

---

## TS-040 — Cambio de Contexto no Modifica OrganizationId

Given.

```text
OrganizationId = ORG-001

Version = N
```

When.

```text
ChangeParticipationContext
```

Then.

```text
OrganizationId = ORG-001
```

La modificación de contexto no constituye transferencia entre
Organizations.

---

## TS-041 — Cambio de Contexto no Modifica Aggregate Externo

Given.

```text
AssemblyId = ASM-001
```

When.

```text
ChangeParticipationContext

AssemblyId = ASM-002
```

Then.

```text
Participation.AssemblyId = ASM-002
```

y:

```text
Assembly ASM-001

Unchanged
```

```text
Assembly ASM-002

Unchanged
```

Participation modifica exclusivamente su referencia.

---

## TS-042 — Cambio de Contexto sobre Archived

Given.

```text
ParticipationStatus = Archived

Version = N
```

When.

```text
ChangeParticipationContext
```

Then.

```text
Rejected

Version = N
```

---

# Metadata

## TS-043 — Actualización de Metadata Válida

Given.

```text
Metadata = A

State allows modification

Version = N

Participation.UpdateMetadata = Granted
```

When.

```text
UpdateParticipationMetadata

Metadata = B
```

Then.

```text
Metadata = B

Version = N + 1

ParticipationMetadataUpdated
```

---

## TS-044 — Metadata sin Cambio Efectivo

Given.

```text
Metadata = A

Version = N
```

When.

```text
UpdateParticipationMetadata

Metadata = A
```

Then.

```text
Metadata = A

Version = N

No ParticipationMetadataUpdated
```

---

## TS-045 — Metadata no Puede Modificar Status

Given.

```text
ParticipationStatus = Active

Version = N
```

When.

```text
UpdateParticipationMetadata

Metadata contains status = Completed
```

Then.

```text
ParticipationStatus = Active
```

Metadata no sustituye el estado oficial del Aggregate.

---

## TS-046 — Metadata no Puede Modificar Version

Given.

```text
Version = N
```

When.

```text
UpdateParticipationMetadata

Metadata contains version = 100
```

Then.

```text
Version is not set to 100
```

Version evoluciona únicamente según las reglas oficiales.

---

## TS-047 — Metadata no Puede Modificar OrganizationId

Given.

```text
OrganizationId = ORG-001
```

When.

```text
UpdateParticipationMetadata

Metadata contains OrganizationId = ORG-002
```

Then.

```text
OrganizationId = ORG-001
```

---

# Timestamps

## TS-048 — CreatedAt Preservado

Given.

```text
CreatedAt = T1
```

When.

```text
Any valid later modification
```

Then.

```text
CreatedAt = T1
```

---

## TS-049 — StartedAt se Define al Activar

Given.

```text
ParticipationStatus = Registered

StartedAt = None
```

When.

```text
ActivateParticipation
```

Then.

```text
ParticipationStatus = Active

StartedAt defined
```

---

## TS-050 — CompletedAt se Define al Completar

Given.

```text
ParticipationStatus = Active

CompletedAt = None
```

When.

```text
CompleteParticipation
```

Then.

```text
ParticipationStatus = Completed

CompletedAt defined
```

---

## TS-051 — WithdrawnAt se Define al Retirar

Given.

```text
ParticipationStatus = Active

WithdrawnAt = None
```

When.

```text
WithdrawParticipation
```

Then.

```text
ParticipationStatus = Withdrawn

WithdrawnAt defined
```

---

## TS-052 — InvalidatedAt se Define al Invalidar

Given.

```text
ParticipationStatus = Active

InvalidatedAt = None
```

When.

```text
InvalidateParticipation
```

Then.

```text
ParticipationStatus = Invalidated

InvalidatedAt defined
```

---

## TS-053 — ArchivedAt se Define al Archivar

Given.

```text
ParticipationStatus = Completed

ArchivedAt = None
```

When.

```text
ArchiveParticipation
```

Then.

```text
ParticipationStatus = Archived

ArchivedAt defined
```

---

## TS-054 — Preservación de Historia Temporal

Given.

```text
CreatedAt = T1

StartedAt = T2

CompletedAt = T3

ParticipationStatus = Completed
```

When.

```text
InvalidateParticipation at T4
```

Then.

```text
CreatedAt = T1

StartedAt = T2

CompletedAt = T3

InvalidatedAt = T4
```

Los hechos históricos anteriores permanecen preservados.

---

## TS-055 — Orden Temporal de Completion

Given.

```text
CreatedAt = T1

StartedAt = T2
```

When.

```text
CompleteParticipation at T3
```

Then.

Debe cumplirse:

```text
T1 <= T2 <= T3
```

---

# Permissions

## TS-056 — Operación Autorizada

Given.

```text
Participation.Activate = Granted

ParticipationStatus = Registered
```

When.

```text
ActivateParticipation
```

Then.

La operación puede continuar hacia la validación del dominio.

---

## TS-057 — Operación No Autorizada

Given.

```text
Participation.Activate = Denied

ParticipationStatus = Registered

Version = N
```

When.

```text
ActivateParticipation
```

Then.

```text
No Command Execution

ParticipationStatus = Registered

Version = N

No ParticipationActivated
```

---

## TS-058 — Permission Granted no Evita State Machine

Given.

```text
Participation.Complete = Granted

ParticipationStatus = Registered

Version = N
```

When.

```text
CompleteParticipation
```

Then.

```text
Rejected

Version = N
```

Debe mantenerse:

```text
Permission Granted

≠

Operation Guaranteed
```

---

## TS-059 — Permission Administrativo no Evita Invariants

Given.

```text
Administrative Actor

Participation.Invalidate = Granted
```

When.

La operación solicitada viola una Invariant.

Then.

```text
Rejected

No State Change
```

---

## TS-060 — Read Permission no Implica Write Permission

Given.

```text
Participation.Read = Granted

Participation.Invalidate = Denied
```

When.

```text
InvalidateParticipation
```

Then.

```text
Authorization Denied
```

---

# Aislamiento Organizacional

## TS-061 — Actor dentro de la misma Organization

Given.

```text
Actor Organization = ORG-001

Participation.OrganizationId = ORG-001

Required Permission = Granted
```

When.

```text
Authorized Participation Command
```

Then.

La operación puede continuar hacia validación del dominio.

---

## TS-062 — Acceso entre Organizations no Autorizado

Given.

```text
Actor Organization = ORG-A

Participation.OrganizationId = ORG-B

No cross-organization capability
```

When.

```text
Participation Command
```

Then.

```text
Authorization Denied

No State Change

Version Unchanged
```

---

# Versioning

## TS-063 — Version Inicial

Given.

```text
No Participation
```

When.

```text
RegisterParticipation
```

Then.

```text
Version = 1
```

---

## TS-064 — Incremento por Modificación Válida

Given.

```text
Version = N
```

When.

```text
Valid Domain Modification
```

Then.

```text
Version = N + 1
```

---

## TS-065 — No Incremento por Command Rechazado

Given.

```text
Version = N
```

When.

```text
Rejected Command
```

Then.

```text
Version = N
```

---

## TS-066 — No Incremento por Permission Denied

Given.

```text
Version = N
```

When.

```text
Permission Denied
```

Then.

```text
Version = N
```

---

## TS-067 — No Incremento por Invariant Violation

Given.

```text
Version = N
```

When.

```text
Invariant Violation
```

Then.

```text
Version = N
```

---

## TS-068 — No Incremento por No-Op

Given.

```text
Version = N

ParticipationType = TypeA
```

When.

```text
ChangeParticipationType

NewParticipationType = TypeA
```

Then.

```text
Version = N
```

---

## TS-069 — Version Nunca Disminuye

Given.

```text
Version = 8
```

When.

Se intenta producir:

```text
Version = 7
```

Then.

```text
Rejected
```

---

## TS-070 — Version no se Reinicia al Archivar

Given.

```text
ParticipationStatus = Completed

Version = 9
```

When.

```text
ArchiveParticipation
```

Then.

```text
ParticipationStatus = Archived

Version = 10
```

No:

```text
Version = 1
```

---

# Concurrency

## TS-071 — Persistencia con Version Correcta

Given.

```text
PersistedVersion = 5

ExpectedVersion = 5
```

When.

Se persiste una modificación válida.

Then.

```text
PersistedVersion = 6
```

---

## TS-072 — ConcurrencyConflict

Given.

```text
PersistedVersion = 6

ExpectedVersion = 5
```

When.

```text
Repository Save
```

Then.

```text
ConcurrencyConflictError

No Silent Overwrite
```

---

## TS-073 — Dos Procesos Concurrentes

Given.

```text
Process A loads Version 10

Process B loads Version 10
```

When.

Process A persiste:

```text
Version 11
```

y Process B intenta persistir sobre:

```text
ExpectedVersion = 10
```

Then.

```text
Process A = Persisted

Process B = ConcurrencyConflictError
```

---

## TS-074 — Reintento después de Conflicto

Given.

```text
ConcurrencyConflictError
```

When.

El proceso desea intentar nuevamente la operación.

Then.

Debe realizar:

```text
Reload Participation

↓

Obtain Current Version

↓

Reevaluate Command

↓

Persist only if still valid
```

No debe realizar:

```text
Force Save
```

---

# Repository

## TS-075 — Guardar Nueva Participation

Given.

```text
Valid newly registered Participation
```

When.

```text
ParticipationRepository.save()
```

Then.

```text
Persisted
```

---

## TS-076 — Recuperar Participation

Given.

Existe una Participation persistida:

```text
ParticipationId = PAR-001

ParticipationStatus = Active

Version = 5
```

When.

```text
getById(PAR-001)
```

Then.

```text
ParticipationId = PAR-001

ParticipationStatus = Active

Version = 5
```

---

## TS-077 — Recuperación no Incrementa Version

Given.

```text
Persisted Version = 5
```

When.

```text
getById()
```

Then.

```text
Version = 5
```

---

## TS-078 — Participation No Encontrada

Given.

```text
ParticipationId does not exist
```

When.

```text
getById()
```

Then.

```text
NotFound
```

No debe crearse automáticamente una nueva Participation.

---

## TS-079 — exists() no Modifica Aggregate

Given.

```text
ParticipationId = PAR-001
```

When.

```text
exists(PAR-001)
```

Then.

```text
true
```

y:

```text
No State Change

No Version Increment

No Domain Event
```

---

## TS-080 — Persistencia Atómica

Given.

```text
ParticipationStatus = Active

CompletedAt = None

Version = 5
```

When.

```text
CompleteParticipation
```

Then la persistencia confirmada debe contener conjuntamente:

```text
ParticipationStatus = Completed

CompletedAt defined

Version = 6
```

No debe observarse un estado parcial.

---

## TS-081 — PersistenceFailure

Given.

Una modificación válida produce en memoria:

```text
Version = N + 1
```

When.

```text
Repository Save

↓

PersistenceFailure
```

Then.

```text
Confirmed Persisted Version remains N
```

El Repository no debe informar éxito.

---

# Rehidratación

## TS-082 — Rehidratación Correcta

Given.

Persistencia contiene:

```text
ParticipationStatus = Completed

Version = 7
```

When.

```text
Rehydrate Participation
```

Then.

```text
ParticipationStatus = Completed

Version = 7
```

---

## TS-083 — Rehidratación no Genera Eventos Nuevos

Given.

Una Participation persistida.

When.

```text
Rehydrate
```

Then.

```text
No New Domain Events
```

---

## TS-084 — Rehidratación no Incrementa Version

Given.

```text
Persisted Version = 7
```

When.

```text
Rehydrate
```

Then.

```text
Version = 7
```

---

# Event Sourcing Compatible

## TS-085 — Replay Reconstruye Estado

Given.

```text
ParticipationRegistered

ParticipationActivated

ParticipationCompleted
```

When.

```text
Replay
```

Then.

```text
ParticipationStatus = Completed
```

---

## TS-086 — Replay no Ejecuta Commands

Given.

```text
Historical ParticipationActivated
```

When.

```text
Replay
```

Then.

El evento histórico se aplica como hecho ocurrido.

No debe ejecutarse nuevamente:

```text
ActivateParticipation
```

---

## TS-087 — Replay no Genera Nuevos Domain Events

Given.

Un historial persistido de Domain Events.

When.

```text
Replay
```

Then.

```text
No New Domain Events
```

---

# Domain Events

## TS-088 — Evento después de Registration

Given.

Registro válido.

When.

```text
RegisterParticipation
```

Then.

```text
ParticipationRegistered
```

---

## TS-089 — Evento después de Activation

Given.

Activación válida.

When.

```text
ActivateParticipation
```

Then.

```text
ParticipationActivated
```

---

## TS-090 — Evento después de Completion

Given.

Completion válida.

When.

```text
CompleteParticipation
```

Then.

```text
ParticipationCompleted
```

---

## TS-091 — Evento después de Withdrawal

Given.

Withdrawal válido.

When.

```text
WithdrawParticipation
```

Then.

```text
ParticipationWithdrawn
```

---

## TS-092 — Evento después de Invalidation

Given.

Invalidation válida.

When.

```text
InvalidateParticipation
```

Then.

```text
ParticipationInvalidated
```

---

## TS-093 — Evento después de Archive

Given.

Archive válido.

When.

```text
ArchiveParticipation
```

Then.

```text
ParticipationArchived
```

---

## TS-094 — Evento de Operación Rechazada

Given.

Una operación inválida.

When.

El Command es rechazado.

Then.

No debe producirse el Domain Event que represente éxito de la
operación.

---

# AggregateVersion en Eventos

## TS-095 — Domain Event conserva AggregateVersion

Given.

```text
Participation Version = 5
```

When.

Una modificación válida produce:

```text
Version = 6
```

Then.

El Domain Event correspondiente debe mantener:

```text
AggregateVersion = 6
```

---

# Integration Events

## TS-096 — Integration Event después de Hecho Confirmado

Given.

```text
ParticipationCompleted
```

corresponde a una modificación confirmada.

When.

Se genera el contrato de integración correspondiente.

Then.

```text
ParticipationCompletedIntegrationEvent
```

debe representar el hecho confirmado.

---

## TS-097 — No Integration Event antes del Commit

Given.

Existe una modificación todavía no confirmada.

When.

La persistencia no ha sido completada.

Then.

No debe publicarse el hecho como Integration Event confirmado.

---

## TS-098 — Integration Event conserva AggregateVersion

Given.

```text
Participation Version = 9
```

When.

Se produce un Integration Event correspondiente al cambio
confirmado.

Then.

```text
AggregateVersion = 9
```

---

## TS-099 — Integration Event Duplicado no es Nuevo Hecho

Given.

Un Integration Event ya publicado.

When.

La infraestructura entrega nuevamente el mismo evento.

Then.

```text
Same EventId

↓

Duplicate Delivery
```

La segunda entrega no representa una nueva modificación de
Participation.

---

# Consistency Boundary

## TS-100 — Participation Modifica solo su Estado

Given.

Participation mantiene:

```text
AssemblyId = ASM-001
```

When.

Se ejecuta un Command válido sobre Participation.

Then.

```text
Participation may change
```

pero:

```text
Assembly Aggregate

Unchanged
```

---

## TS-101 — Proposal permanece fuera del Boundary

Given.

```text
ProposalId = PRO-001
```

When.

Participation cambia de estado.

Then.

```text
Proposal Aggregate

Unchanged
```

---

## TS-102 — Citizen permanece fuera del Boundary

Given.

```text
CitizenId = CIT-001
```

When.

Participation cambia de estado.

Then.

```text
Citizen Aggregate

Unchanged
```

---

## TS-103 — Membership permanece fuera del Boundary

Given.

```text
MembershipId = MEM-001
```

When.

Participation cambia de estado.

Then.

```text
Membership Aggregate

Unchanged
```

---

## TS-104 — Territory permanece fuera del Boundary

Given.

```text
TerritoryId = TER-001
```

When.

Participation cambia de estado.

Then.

```text
Territory Aggregate

Unchanged
```

---

## TS-105 — Referencias mediante Identificadores

Given.

Participation mantiene referencias hacia otros Aggregates.

Then.

Estas referencias deben expresarse mediante:

```text
AggregateId
```

y no mediante Aggregates externos mutables contenidos dentro de
Participation.

---

# Read Models

## TS-106 — Proyección después de Registration

Given.

```text
ParticipationRegistered
```

When.

El Projection Engine procesa el evento.

Then.

Las proyecciones afectadas deben reflejar la nueva Participation.

---

## TS-107 — Proyección después de Activation

Given.

```text
ParticipationActivated
```

When.

El evento es proyectado.

Then.

El Read Model correspondiente debe reflejar:

```text
ParticipationStatus = Active
```

---

## TS-108 — Proyección después de Completion

Given.

```text
ParticipationCompleted
```

When.

El evento es proyectado.

Then.

El Read Model correspondiente debe reflejar:

```text
ParticipationStatus = Completed
```

---

## TS-109 — Read Model no Modifica Aggregate

Given.

Existe una proyección de Participation.

When.

La proyección es consultada o reconstruida.

Then.

```text
Participation Aggregate

Unchanged
```

---

## TS-110 — Read Model Eventualmente Consistente

Given.

El Write Side confirma:

```text
ParticipationStatus = Completed
```

When.

La proyección todavía no ha procesado:

```text
ParticipationCompleted
```

Then.

Puede existir temporalmente:

```text
Write Side = Completed

Read Side = Previous State
```

hasta que la proyección sea actualizada.

---

# Operaciones Masivas

## TS-111 — Cada Participation conserva su Boundary

Given.

Una operación procesa:

```text
PAR-A

PAR-B

PAR-C
```

When.

Se ejecutan modificaciones sobre las tres Participations.

Then.

Cada una debe mantener:

```text
Own State

Own Version

Own Invariants

Own Persistence Result
```

---

## TS-112 — Conflicto en una Participation no Fusiona Aggregates

Given.

```text
PAR-A = Version valid

PAR-B = Version conflict

PAR-C = Version valid
```

When.

Se procesan las operaciones.

Then.

Cada resultado pertenece a su Aggregate correspondiente.

La operación masiva no convierte las Participations en una única
unidad de consistencia.

---

# Importación

## TS-113 — Importación Respeta Invariants

Given.

Datos externos para registrar una Participation.

When.

Se ejecuta el proceso de incorporación correspondiente.

Then.

La Participation solo puede quedar creada cuando preserve las
mismas Invariants utilizadas por cualquier otro mecanismo de
registro.

---

## TS-114 — Importación no Permite Identidad Duplicada

Given.

```text
ParticipationId already exists
```

When.

Una importación intenta utilizar la misma identidad.

Then.

```text
Rejected
```

---

## TS-115 — Importación no Permite Modificar OrganizationId

Given.

Una Participation existente pertenece a:

```text
OrganizationId = ORG-A
```

When.

Una importación intenta convertirla en:

```text
OrganizationId = ORG-B
```

Then.

```text
Rejected
```

---

# Protección contra Bypass

## TS-116 — Direct State Mutation no Permitida

Given.

```text
ParticipationStatus = Active
```

When.

Se intenta modificar directamente:

```text
ParticipationStatus = Completed
```

sin comportamiento del Aggregate.

Then.

La operación no debe considerarse válida.

---

## TS-117 — Direct Version Mutation no Permitida

Given.

```text
Version = 5
```

When.

Se intenta:

```text
Version = 100
```

directamente.

Then.

```text
Rejected
```

---

## TS-118 — Repository no Ejecuta Lifecycle

Given.

```text
ParticipationStatus = Active
```

When.

Se intenta utilizar el Repository para cambiar directamente:

```text
ParticipationStatus = Completed
```

Then.

La operación no forma parte del contrato válido de modificación del
Aggregate.

---

## TS-119 — Integration no Evita Aggregate Root

Given.

Una Integration desea modificar Participation.

When.

La Integration intenta escribir directamente en persistencia.

Then.

La operación no forma parte del flujo válido del dominio.

Las modificaciones deben respetar los mecanismos establecidos por
AURA Core.

---

# Matriz de Lifecycle

```text
Origin         Command                    Result

None           RegisterParticipation      Registered

Registered     ActivateParticipation      Active

Registered     WithdrawParticipation      Withdrawn

Registered     InvalidateParticipation    Invalidated

Active         CompleteParticipation      Completed

Active         WithdrawParticipation      Withdrawn

Active         InvalidateParticipation    Invalidated

Completed      InvalidateParticipation    Invalidated

Completed      ArchiveParticipation       Archived

Withdrawn      ArchiveParticipation       Archived

Invalidated    ArchiveParticipation       Archived
```

---

# Matriz de Transiciones Rechazadas

```text
Origin         Requested Destination      Result

Registered     Completed                  Rejected

Registered     Archived                   Rejected

Active         Registered                 Rejected

Active         Archived                   Rejected

Completed      Active                     Rejected

Completed      Withdrawn                  Rejected

Withdrawn      Active                     Rejected

Withdrawn      Completed                  Rejected

Invalidated    Active                     Rejected

Invalidated    Completed                  Rejected

Archived       Registered                 Rejected

Archived       Active                     Rejected

Archived       Completed                  Rejected
```

---

# Matriz de Commands

```text
Command                       Primary Expected Result

RegisterParticipation         Registered

ActivateParticipation         Active

CompleteParticipation         Completed

WithdrawParticipation         Withdrawn

InvalidateParticipation       Invalidated

ArchiveParticipation          Archived

ChangeParticipationType       ParticipationType changed

ChangeParticipationContext    Context changed

UpdateParticipationMetadata   Metadata changed
```

---

# Matriz de Eventos

```text
Valid Operation                Expected Domain Event

RegisterParticipation          ParticipationRegistered

ActivateParticipation          ParticipationActivated

CompleteParticipation          ParticipationCompleted

WithdrawParticipation          ParticipationWithdrawn

InvalidateParticipation        ParticipationInvalidated

ArchiveParticipation           ParticipationArchived

ChangeParticipationType        ParticipationTypeChanged

ChangeParticipationContext     ParticipationContextChanged

UpdateParticipationMetadata    ParticipationMetadataUpdated
```

---

# Matriz de Version

```text
Operation                        Version Result

Valid Registration               Initialize

Valid State Transition           Increment

Valid Type Change                Increment

Valid Context Change             Increment

Effective Metadata Change        Increment

Rejected Command                 Unchanged

Permission Denied                Unchanged

Invariant Violation              Unchanged

Invalid State Transition         Unchanged

No-Op                            Unchanged

Repository Read                  Unchanged

Rehydration                      Unchanged

Replay                           No artificial increment

ConcurrencyConflict              No new persisted version
```

---

# Matriz de Consistencia

```text
Concept                         Inside Participation Boundary

ParticipationId                 Yes

OrganizationId                  Yes

ParticipationType               Yes

ParticipationStatus             Yes

Participation Context           Yes

Metadata                        Yes

Lifecycle Timestamps            Yes

Version                         Yes

Organization Aggregate          No

Citizen Aggregate               No

Membership Aggregate            No

Role Aggregate                  No

Territory Aggregate             No

Assembly Aggregate              No

Proposal Aggregate              No

Read Models                     No

Integration Consumers           No
```

---

# Resultado de una Prueba Válida

Un escenario válido debe poder demostrar conceptualmente:

```text
Valid Initial State

↓

Valid Command

↓

Permission Granted

↓

Valid State Machine Rule

↓

Invariants Preserved

↓

Valid State Change

↓

Version Evolution

↓

Expected Domain Event

↓

Consistent Persistence
```

---

# Resultado de una Prueba Inválida

Un escenario inválido debe demostrar:

```text
Invalid Intention or Condition

↓

Rejected
```

manteniendo:

```text
Previous Aggregate State

Version Unchanged

No Success Domain Event
```

---

# Cobertura Mínima

La cobertura conceptual del Aggregate debe incluir como mínimo:

- creación válida;
- creación inválida;
- cada transición válida del Lifecycle;
- cada transición inválida relevante;
- identidad inmutable;
- OrganizationId inmutable;
- cambio válido de ParticipationType;
- cambio inválido de ParticipationType;
- cambio válido de contexto;
- protección de referencias externas;
- actualización válida de Metadata;
- protección de atributos reservados;
- coherencia temporal;
- preservación de timestamps históricos;
- Permissions concedidos;
- Permissions denegados;
- separación entre Permission e Invariant;
- Version inicial;
- incremento de Version;
- no incremento ante rechazo;
- concurrencia optimista;
- ConcurrencyConflict;
- recuperación desde Repository;
- NotFound;
- persistencia atómica;
- PersistenceFailure;
- rehidratación;
- Replay;
- Domain Events;
- AggregateVersion;
- Integration Events;
- consistencia eventual;
- aislamiento entre Aggregates;
- Read Models;
- operaciones masivas;
- protección contra bypass.

---

# Restricciones

Los Test Scenarios no pueden:

- introducir nuevos estados;
- introducir nuevas transiciones;
- introducir nuevos Commands;
- introducir nuevos Domain Events;
- introducir nuevos Integration Events;
- introducir nuevos Permissions;
- modificar Invariants;
- modificar ParticipationId;
- convertir OrganizationId en mutable;
- ampliar el Consistency Boundary;
- convertir otros Aggregates en entidades internas;
- definir Infrastructure como parte del dominio;
- convertir Read Models en fuente de verdad;
- eliminar Versioning;
- permitir Last Write Wins;
- permitir modificaciones parciales;
- permitir Domain Events de éxito ante operaciones rechazadas;
- utilizar escenarios de prueba para redefinir el modelo oficial.

---

# Reglas

## REG-001

Todo Command oficial debe poseer escenarios válidos e inválidos
cuando corresponda.

---

## REG-002

Toda transición válida del Lifecycle debe ser verificable mediante
un escenario.

---

## REG-003

Las transiciones no permitidas deben ser rechazadas sin modificar
el Aggregate.

---

## REG-004

Toda modificación válida debe preservar las Invariants.

---

## REG-005

Una operación rechazada no modifica Version.

---

## REG-006

Una operación rechazada no genera el Domain Event de éxito
correspondiente.

---

## REG-007

ParticipationId debe permanecer inmutable en todos los escenarios.

---

## REG-008

OrganizationId debe permanecer inmutable durante toda la vida del
Aggregate.

---

## REG-009

Archived debe comportarse como estado terminal según el Lifecycle
establecido.

---

## REG-010

El Repository debe recuperar exactamente el estado y Version
persistidos.

---

## REG-011

Las modificaciones concurrentes incompatibles deben producir
ConcurrencyConflictError.

---

## REG-012

La rehidratación no debe generar nuevas modificaciones, Version ni
Domain Events.

---

## REG-013

Los otros Aggregates deben permanecer fuera del Consistency
Boundary de Participation.

---

## REG-014

Los Read Models deben permanecer desacoplados del Write Side.

---

## REG-015

Los Integration Events deben representar únicamente hechos
previamente confirmados.

---

# Definición de Éxito

Los Test Scenarios del Aggregate **Participation** constituyen el
conjunto conceptual oficial de verificaciones necesarias para
demostrar que su comportamiento permanece consistente con el modelo
DDD definido por AURA Core.

Los escenarios garantizan que:

- Participation se crea únicamente en condiciones válidas;
- el Lifecycle respeta sus transiciones oficiales;
- la State Machine rechaza transiciones no permitidas;
- ParticipationId permanece inmutable;
- OrganizationId permanece inmutable;
- las Invariants se preservan después de cada modificación válida;
- los Permissions permanecen separados de las reglas del dominio;
- las operaciones rechazadas no modifican estado ni Version;
- los timestamps representan hechos reales del Lifecycle;
- la historia temporal permanece preservada;
- Version evoluciona únicamente ante modificaciones válidas;
- los conflictos concurrentes son detectados;
- el Repository preserva identidad, estado y Version;
- la persistencia respeta atomicidad;
- la rehidratación no produce nuevas decisiones;
- Replay no ejecuta nuevamente Commands;
- los Domain Events representan hechos consumados;
- los Integration Events representan hechos confirmados;
- los Read Models permanecen derivados y reconstruibles;
- otros Aggregates permanecen fuera del Consistency Boundary;
- ningún mecanismo externo puede evitar el Aggregate Root;
- los escenarios documentan y verifican el modelo existente sin
  introducir nuevas decisiones arquitectónicas.

De esta forma, `DOMAIN-008M-Test-Scenarios.md` permite verificar de
manera sistemática que el Aggregate **Participation** conserva su
identidad, Lifecycle, State Machine, Invariants, Permissions,
Versioning, persistencia, eventos y límites de consistencia conforme
al patrón consolidado de AURA Core.