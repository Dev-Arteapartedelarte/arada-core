# DOMAIN-008H — Participation Examples

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Participation Management

Aggregate:
Participation

Autor:
ARADA

Documentos relacionados:

- DOMAIN-008-Aggregate.md
- DOMAIN-008A-Lifecycle.md
- DOMAIN-008B-State-Machine.md
- DOMAIN-008C-Commands.md
- DOMAIN-008D-Domain-Events.md
- DOMAIN-008E-Invariants.md
- DOMAIN-008F-Permissions.md
- DOMAIN-008G-Repository-Contract.md
- DOMAIN-008I-Versioning.md
- DOMAIN-008J-Consistency-Boundary.md
- DOMAIN-008K-Integration-Events.md
- DOMAIN-008L-Read-Model.md
- DOMAIN-008M-Test-Scenarios.md
- DOMAIN-008N-Performance-Rules.md
- DOMAIN-008O-Security-Model.md
- DOMAIN-008P-Extension-Points.md
- DOMAIN-001-Aggregate.md
- DOMAIN-002-Aggregate.md
- DOMAIN-003-Aggregate.md
- DOMAIN-005-Aggregate.md
- DOMAIN-006-Aggregate.md
- DOMAIN-007-Aggregate.md
- CORE-004-Ubiquitous-Language.md
- CORE-005-Domain-Events.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Definir ejemplos conceptuales oficiales que permitan comprender el
comportamiento esperado del Aggregate **Participation** dentro de
AURA Core.

Los ejemplos documentados en este archivo ilustran cómo se aplican
conjuntamente:

- identidad;
- pertenencia organizacional;
- tipos de participación;
- referencias hacia otros Aggregates;
- Lifecycle;
- State Machine;
- Commands;
- Domain Events;
- Invariants;
- Permissions;
- Repository Contract;
- Versioning;
- Consistency Boundary.

Los ejemplos no sustituyen las definiciones normativas contenidas
en los documentos especializados del Aggregate.

Cuando exista diferencia entre un ejemplo y una regla normativa,
prevalece siempre la regla normativa oficial.

---

# Propósito

El propósito de este documento es proporcionar escenarios
comprensibles que permitan observar el modelo de Participation en
funcionamiento sin introducir nuevas reglas de dominio.

Debe mantenerse:

```text
Domain Rules

↓

Examples

↓

Understanding
```

No:

```text
Examples

↓

New Domain Rules
```

Los ejemplos representan aplicaciones concretas del modelo ya
establecido.

---

# Principios

Los ejemplos de Participation siguen los siguientes principios:

- utilizan exclusivamente conceptos definidos por el Aggregate;
- no introducen estados adicionales;
- no introducen transiciones adicionales;
- no introducen Commands adicionales;
- no introducen Domain Events adicionales;
- no modifican Invariants;
- no amplían Permissions;
- no modifican el límite de consistencia;
- no convierten referencias externas en entidades internas;
- mantienen OrganizationId inmutable;
- mantienen ParticipationId inmutable;
- respetan Version;
- respetan Lifecycle;
- respetan State Machine;
- respetan Repository Contract;
- distinguen operaciones válidas de operaciones rechazadas.

---

# Modelo General de Ejemplo

Una Participation puede representarse conceptualmente como:

```text
Participation

ParticipationId

OrganizationId

ParticipationType

ParticipationStatus

CitizenId

MembershipId

AssemblyId

ProposalId

TerritoryId

Metadata

CreatedAt

StartedAt

CompletedAt

WithdrawnAt

InvalidatedAt

ArchivedAt

Version
```

No todos los contextos requieren necesariamente todas las
referencias.

Las referencias utilizadas dependen del tipo y contexto de la
Participation definido por el dominio.

---

# Estados Utilizados

Los ejemplos utilizan exclusivamente los estados oficiales:

```text
Registered

Active

Completed

Withdrawn

Invalidated

Archived
```

No deben inferirse estados adicionales a partir de los escenarios.

---

# Flujo General

El flujo conceptual normal puede representarse como:

```text
RegisterParticipation

↓

Registered

↓

ActivateParticipation

↓

Active

↓

CompleteParticipation

↓

Completed

↓

ArchiveParticipation

↓

Archived
```

También pueden existir terminaciones alternativas según las reglas
oficiales:

```text
Registered / Active

↓

WithdrawParticipation

↓

Withdrawn

↓

ArchiveParticipation

↓

Archived
```

o:

```text
Registered / Active / Completed

↓

InvalidateParticipation

↓

Invalidated

↓

ArchiveParticipation

↓

Archived
```

Las transiciones exactas permanecen definidas por:

```text
DOMAIN-008A-Lifecycle.md

DOMAIN-008B-State-Machine.md
```

---

# Ejemplo 1 — Registro de Participation

## Contexto

Una Organization registra una nueva Participation asociada a un
Citizen dentro de un contexto reconocido por el dominio.

Datos conceptuales:

```text
OrganizationId = ORG-001

CitizenId = CIT-001

ParticipationType = AssemblyParticipation

AssemblyId = ASM-001
```

El actor posee:

```text
Participation.Register
```

---

## Command

```text
RegisterParticipation

CommandId = CMD-001

ParticipationId = PAR-001

OrganizationId = ORG-001

CitizenId = CIT-001

ParticipationType = AssemblyParticipation

AssemblyId = ASM-001

ActorId = ACT-001

Timestamp = T1

CorrelationId = COR-001
```

---

## Validaciones

Antes de aceptar el registro deben preservarse las reglas definidas
por el Aggregate.

Conceptualmente:

```text
Valid ParticipationId

Valid OrganizationId

Valid ParticipationType

Valid Required Context

Valid References

Valid Initial State

Permission Granted

Invariants Preserved
```

---

## Resultado

```text
ParticipationId = PAR-001

OrganizationId = ORG-001

ParticipationType = AssemblyParticipation

ParticipationStatus = Registered

CitizenId = CIT-001

AssemblyId = ASM-001

CreatedAt = T1

Version = 1
```

---

## Domain Event

```text
ParticipationRegistered
```

---

## Persistencia

```text
Participation

↓

ParticipationRepository.save()

↓

Persisted
```

El Repository persiste el Aggregate válido.

No decide crear la Participation.

---

# Ejemplo 2 — Activación de Participation

## Estado inicial

```text
ParticipationId = PAR-001

ParticipationStatus = Registered

Version = 1
```

El actor posee:

```text
Participation.Activate
```

---

## Command

```text
ActivateParticipation

ParticipationId = PAR-001

ActorId = ACT-001

ExpectedVersion = 1

Timestamp = T2

CorrelationId = COR-002
```

---

## Evaluación

```text
Permission Granted

+

CurrentStatus = Registered

+

Activation Invariants Preserved
```

---

## Transición

```text
Registered

↓

Active
```

---

## Resultado

```text
ParticipationStatus = Active

StartedAt = T2

Version = 2
```

---

## Domain Event

```text
ParticipationActivated
```

---

# Ejemplo 3 — Completion de Participation

## Estado inicial

```text
ParticipationId = PAR-001

ParticipationStatus = Active

Version = 2
```

El actor posee:

```text
Participation.Complete
```

---

## Command

```text
CompleteParticipation

ParticipationId = PAR-001

ActorId = ACT-001

ExpectedVersion = 2

Timestamp = T3

CorrelationId = COR-003
```

---

## Evaluación

```text
Permission Granted

+

CurrentStatus = Active

+

Completion Invariants Preserved
```

---

## Transición

```text
Active

↓

Completed
```

---

## Resultado

```text
ParticipationStatus = Completed

CompletedAt = T3

Version = 3
```

---

## Domain Event

```text
ParticipationCompleted
```

---

# Ejemplo 4 — Archivado de Participation completada

## Estado inicial

```text
ParticipationId = PAR-001

ParticipationStatus = Completed

CompletedAt = T3

Version = 3
```

El actor posee:

```text
Participation.Archive
```

---

## Command

```text
ArchiveParticipation

ParticipationId = PAR-001

ActorId = ACT-001

ExpectedVersion = 3

Timestamp = T4

CorrelationId = COR-004
```

---

## Transición

```text
Completed

↓

Archived
```

---

## Resultado

```text
ParticipationStatus = Archived

CompletedAt = T3

ArchivedAt = T4

Version = 4
```

CompletedAt permanece preservado.

Archive no elimina la historia anterior.

---

## Domain Event

```text
ParticipationArchived
```

---

# Ejemplo 5 — Withdrawal de Participation

## Contexto

Un participante solicita retirarse de una Participation cuando el
estado permite dicha operación.

Estado inicial:

```text
ParticipationId = PAR-002

ParticipationStatus = Active

Version = 2
```

El actor posee:

```text
Participation.Withdraw
```

---

## Command

```text
WithdrawParticipation

ParticipationId = PAR-002

ActorId = ACT-002

ExpectedVersion = 2

Timestamp = T5

CorrelationId = COR-005
```

---

## Transición

```text
Active

↓

Withdrawn
```

---

## Resultado

```text
ParticipationStatus = Withdrawn

WithdrawnAt = T5

Version = 3
```

---

## Domain Event

```text
ParticipationWithdrawn
```

---

# Ejemplo 6 — Archive después de Withdrawal

## Estado inicial

```text
ParticipationId = PAR-002

ParticipationStatus = Withdrawn

WithdrawnAt = T5

Version = 3
```

---

## Command

```text
ArchiveParticipation

ParticipationId = PAR-002

ActorId = ACT-001

ExpectedVersion = 3

Timestamp = T6
```

---

## Resultado

```text
ParticipationStatus = Archived

WithdrawnAt = T5

ArchivedAt = T6

Version = 4
```

Debe mantenerse:

```text
WithdrawnAt = T5
```

Archive no reemplaza el hecho histórico de Withdrawal.

---

# Ejemplo 7 — Invalidation de Participation

## Contexto

Una Participation debe ser invalidada mediante una operación
autorizada reconocida por el dominio.

Estado inicial:

```text
ParticipationId = PAR-003

ParticipationStatus = Active

Version = 2
```

El actor posee:

```text
Participation.Invalidate
```

---

## Command

```text
InvalidateParticipation

ParticipationId = PAR-003

ActorId = ACT-003

ExpectedVersion = 2

Timestamp = T7

CorrelationId = COR-007
```

---

## Evaluación

```text
Permission Granted

+

State Allows Invalidation

+

Invalidation Invariants Preserved
```

---

## Resultado

```text
ParticipationStatus = Invalidated

InvalidatedAt = T7

Version = 3
```

---

## Domain Event

```text
ParticipationInvalidated
```

---

# Ejemplo 8 — Archive después de Invalidation

## Estado inicial

```text
ParticipationId = PAR-003

ParticipationStatus = Invalidated

InvalidatedAt = T7

Version = 3
```

---

## Command

```text
ArchiveParticipation

ParticipationId = PAR-003

ActorId = ACT-003

ExpectedVersion = 3

Timestamp = T8
```

---

## Resultado

```text
ParticipationStatus = Archived

InvalidatedAt = T7

ArchivedAt = T8

Version = 4
```

InvalidatedAt permanece preservado.

---

# Ejemplo 9 — Participation asociada a Assembly

## Contexto

Una Participation representa participación ciudadana dentro de una
Assembly.

Referencias:

```text
ParticipationId = PAR-010

OrganizationId = ORG-001

CitizenId = CIT-010

MembershipId = MEM-010

AssemblyId = ASM-010
```

La relación conceptual es:

```text
Participation

↓

AssemblyId
```

No:

```text
Participation

↓

Assembly Aggregate
```

---

## Límite

Participation no incorpora dentro de su estado:

```text
Assembly Title

Assembly Lifecycle

Assembly Agenda

Assembly Participants Collection
```

Estos conceptos pertenecen al Aggregate Assembly.

---

# Ejemplo 10 — Participation asociada a Proposal

## Contexto

Una Participation puede referenciar una Proposal cuando el contexto
del dominio así lo requiera.

```text
ParticipationId = PAR-011

OrganizationId = ORG-001

CitizenId = CIT-011

ProposalId = PRO-011
```

La relación se expresa mediante:

```text
ProposalId
```

---

## Separación

Participation no modifica:

```text
ProposalStatus

ProposalContent

ProposalLifecycle

ProposalVersion
```

Debe mantenerse:

```text
Participation Aggregate

≠

Proposal Aggregate
```

---

# Ejemplo 11 — Participation con contexto territorial

## Contexto

Una Participation puede encontrarse asociada a un Territory cuando
el contexto de participación requiera una referencia territorial.

```text
ParticipationId = PAR-012

OrganizationId = ORG-001

CitizenId = CIT-012

TerritoryId = TER-001
```

La referencia:

```text
TerritoryId
```

no convierte Territory en parte interna de Participation.

---

# Ejemplo 12 — Cambio de ParticipationType

## Estado inicial

```text
ParticipationId = PAR-020

ParticipationType = TypeA

ParticipationStatus = Registered

Version = 1
```

El actor posee:

```text
Participation.ChangeType
```

---

## Command

```text
ChangeParticipationType

ParticipationId = PAR-020

ParticipationType = TypeB

ActorId = ACT-001

ExpectedVersion = 1

Timestamp = T20
```

---

## Evaluación

La operación solo puede ejecutarse cuando:

```text
Permission Granted

+

Current State Allows Change

+

New ParticipationType Valid

+

Invariants Preserved
```

---

## Resultado

```text
ParticipationType = TypeB

Version = 2
```

El cambio no modifica:

```text
ParticipationId

OrganizationId
```

---

# Ejemplo 13 — Cambio de contexto

## Estado inicial

```text
ParticipationId = PAR-021

AssemblyId = ASM-020

ParticipationStatus = Registered

Version = 1
```

El actor posee:

```text
Participation.ChangeContext
```

---

## Command

```text
ChangeParticipationContext

ParticipationId = PAR-021

AssemblyId = ASM-021

ActorId = ACT-001

ExpectedVersion = 1

Timestamp = T21
```

---

## Resultado conceptual

Cuando la operación es válida:

```text
AssemblyId = ASM-021

Version = 2
```

No se modifica el Aggregate Assembly.

Solo cambia la referencia mantenida por Participation.

---

# Ejemplo 14 — Actualización de Metadata

## Estado inicial

```text
ParticipationId = PAR-022

ParticipationStatus = Active

Version = 4
```

El actor posee:

```text
Participation.UpdateMetadata
```

---

## Command

```text
UpdateParticipationMetadata

ParticipationId = PAR-022

Metadata = UpdatedMetadata

ActorId = ACT-001

ExpectedVersion = 4

Timestamp = T22
```

---

## Resultado

```text
Metadata = UpdatedMetadata

Version = 5
```

Metadata no puede utilizarse para modificar indirectamente:

```text
ParticipationId

OrganizationId

ParticipationStatus

Version

CreatedAt

StartedAt

CompletedAt

WithdrawnAt

InvalidatedAt

ArchivedAt
```

---

# Ejemplo 15 — Intento de modificar OrganizationId

## Estado inicial

```text
ParticipationId = PAR-030

OrganizationId = ORG-001
```

Se intenta transformar:

```text
OrganizationId = ORG-002
```

---

## Resultado

```text
Rejected
```

La regla es:

```text
OrganizationId

=

Immutable
```

No se genera una nueva versión válida.

No se produce un Domain Event de modificación exitosa.

---

# Ejemplo 16 — Intento de modificar ParticipationId

## Estado inicial

```text
ParticipationId = PAR-031
```

Se intenta modificar:

```text
PAR-031

↓

PAR-999
```

---

## Resultado

```text
Rejected
```

ParticipationId es identidad inmutable.

---

# Ejemplo 17 — Completion desde estado Registered

## Estado inicial

```text
ParticipationStatus = Registered
```

El actor posee:

```text
Participation.Complete
```

---

## Command

```text
CompleteParticipation
```

---

## Evaluación

```text
Permission Granted
```

pero:

```text
Registered → Completed
```

no constituye la transición válida requerida para Completion.

---

## Resultado

```text
Rejected
```

Debe mantenerse:

```text
Permission Granted

≠

Operation Guaranteed
```

---

# Ejemplo 18 — Activación desde estado Completed

## Estado inicial

```text
ParticipationStatus = Completed
```

---

## Command

```text
ActivateParticipation
```

---

## Resultado

```text
Rejected
```

No existe una transición válida:

```text
Completed → Active
```

La State Machine prevalece independientemente de los Permissions
del actor.

---

# Ejemplo 19 — Modificación después de Archive

## Estado inicial

```text
ParticipationStatus = Archived
```

Se intenta:

```text
ChangeParticipationType
```

---

## Resultado

```text
Rejected
```

Archive representa el estado terminal establecido.

No debe utilizarse un Permission administrativo para evitar esta
restricción.

---

# Ejemplo 20 — Permission Denied

## Contexto

Estado:

```text
ParticipationStatus = Registered

Version = 1
```

El actor intenta:

```text
ActivateParticipation
```

pero:

```text
Participation.Activate = Denied
```

---

## Resultado

```text
No Command Execution

No State Change

No Version Increment

No ParticipationActivated
```

El estado permanece:

```text
ParticipationStatus = Registered

Version = 1
```

---

# Ejemplo 21 — Permission Granted pero Invariant violada

## Contexto

El actor posee:

```text
Participation.ChangeContext
```

pero el cambio solicitado produciría un estado incompatible con las
Invariants vigentes.

---

## Flujo

```text
Permission Granted

↓

ChangeParticipationContext

↓

Invariant Validation

↓

Invariant Violation

↓

Rejected
```

---

## Resultado

```text
No Valid State Change

No Version Increment

No Success Domain Event
```

---

# Ejemplo 22 — Acceso entre Organizations

## Contexto

El actor se encuentra autorizado dentro de:

```text
OrganizationId = ORG-A
```

La Participation pertenece a:

```text
OrganizationId = ORG-B
```

No existe capacidad explícita de acceso transversal.

---

## Resultado

```text
Authorization Denied
```

Debe mantenerse:

```text
Permission in Organization A

≠

Permission in Organization B
```

---

# Ejemplo 23 — Membership como contexto

## Contexto

```text
CitizenId = CIT-100

MembershipId = MEM-100

OrganizationId = ORG-100
```

Membership puede participar en la evaluación externa de
Authorization.

Conceptualmente:

```text
Citizen

↓

Membership

↓

Role

↓

Permission

↓

Participation Command
```

Participation conserva únicamente las referencias que formen parte
de su modelo.

No incorpora:

```text
Membership Aggregate

Role Aggregate
```

dentro de su límite.

---

# Ejemplo 24 — Role no forma parte de Participation

## Contexto

Un actor posee un Role que le concede:

```text
Participation.Invalidate
```

La autorización puede permitir:

```text
InvalidateParticipation
```

Sin embargo, Participation no almacena:

```text
Role = "President"
```

como regla interna de comportamiento.

Debe mantenerse:

```text
Role

↓

Authorization
```

y:

```text
Authorized Command

↓

Participation
```

---

# Ejemplo 25 — Repository Load

## Estado persistido

```text
ParticipationId = PAR-100

OrganizationId = ORG-001

ParticipationStatus = Active

StartedAt = T10

Version = 5
```

---

## Operación

```text
ParticipationRepository.getById(PAR-100)
```

---

## Resultado

```text
ParticipationId = PAR-100

OrganizationId = ORG-001

ParticipationStatus = Active

StartedAt = T10

Version = 5
```

La recuperación no produce:

```text
Version = 6
```

ni genera nuevos Domain Events.

---

# Ejemplo 26 — Repository NotFound

## Operación

```text
ParticipationRepository.getById(PAR-UNKNOWN)
```

---

## Resultado

```text
NotFound
```

No debe generarse automáticamente:

```text
New Participation
```

---

# Ejemplo 27 — Persistencia después de modificación

## Estado inicial persistido

```text
ParticipationId = PAR-101

ParticipationStatus = Registered

Version = 1
```

---

## Flujo

```text
getById(PAR-101)

↓

ActivateParticipation

↓

ParticipationStatus = Active

Version = 2

↓

save(ExpectedVersion = 1)
```

---

## Resultado

```text
Persisted
```

El estado persistido queda:

```text
ParticipationStatus = Active

Version = 2
```

---

# Ejemplo 28 — Conflicto de concurrencia

## Estado inicial

```text
Persisted Version = 5
```

Dos procesos recuperan simultáneamente:

```text
Process A → Version 5

Process B → Version 5
```

Process A modifica y persiste:

```text
Version 6
```

Process B intenta posteriormente:

```text
save(ExpectedVersion = 5)
```

---

## Evaluación

```text
PersistedVersion = 6

ExpectedVersion = 5
```

---

## Resultado

```text
ConcurrencyConflict
```

Process B no sobrescribe silenciosamente el cambio confirmado por
Process A.

---

# Ejemplo 29 — Retry después de ConcurrencyConflict

## Contexto

Process B recibió:

```text
ConcurrencyConflict
```

No debe realizar simplemente:

```text
Force Save
```

---

## Flujo correcto

Conceptualmente:

```text
Reload Participation

↓

Current Version = 6

↓

Reevaluate Requested Intention

↓

Validate Current State

↓

Execute if Still Valid

↓

Save with Current ExpectedVersion
```

La intención debe reevaluarse porque el estado actual puede haber
cambiado.

---

# Ejemplo 30 — Rehidratación

## Estado persistido

```text
ParticipationId = PAR-110

ParticipationStatus = Completed

CreatedAt = T1

StartedAt = T2

CompletedAt = T3

Version = 7
```

---

## Rehidratación

```text
Persisted State

↓

ParticipationRepository

↓

Participation
```

---

## Resultado

```text
ParticipationStatus = Completed

CreatedAt = T1

StartedAt = T2

CompletedAt = T3

Version = 7
```

No ocurre:

```text
CompleteParticipation

ParticipationCompleted

Version = 8
```

La rehidratación no reproduce Commands.

---

# Ejemplo 31 — Archive no es Delete

## Estado inicial

```text
ParticipationId = PAR-120

ParticipationStatus = Completed

Version = 3
```

---

## Operación

```text
ArchiveParticipation
```

---

## Resultado

```text
ParticipationStatus = Archived

Version = 4
```

Posteriormente:

```text
ParticipationRepository.getById(PAR-120)
```

puede recuperar:

```text
ParticipationStatus = Archived
```

Archive no significa conceptualmente:

```text
Participation Does Not Exist
```

---

# Ejemplo 32 — Identidad no reutilizable después de Archive

## Contexto

Existe:

```text
ParticipationId = PAR-120

ParticipationStatus = Archived
```

Se intenta registrar una nueva Participation utilizando:

```text
ParticipationId = PAR-120
```

---

## Resultado

```text
Rejected
```

La identidad permanece asociada al Aggregate archivado.

---

# Ejemplo 33 — Cambio atómico de estado

## Estado inicial

```text
ParticipationStatus = Active

CompletedAt = None

Version = 8
```

---

## Operación

```text
CompleteParticipation
```

---

## Resultado válido

```text
ParticipationStatus = Completed

CompletedAt = T30

Version = 9
```

Estos cambios constituyen una única modificación coherente del
Aggregate.

No debe persistirse:

```text
ParticipationStatus = Completed

CompletedAt = None
```

si la Invariant exige CompletedAt.

---

# Ejemplo 34 — Timestamp histórico preservado

## Historia

```text
CreatedAt = T1

StartedAt = T2

CompletedAt = T3

ArchivedAt = T4
```

---

## Estado final

```text
ParticipationStatus = Archived
```

Los timestamps permanecen:

```text
CreatedAt = T1

StartedAt = T2

CompletedAt = T3

ArchivedAt = T4
```

Archive no reemplaza los timestamps anteriores.

---

# Ejemplo 35 — Withdrawal no es Invalidation

Dos Participations pueden finalizar por razones conceptualmente
diferentes.

Participation A:

```text
Active

↓

WithdrawParticipation

↓

Withdrawn
```

Participation B:

```text
Active

↓

InvalidateParticipation

↓

Invalidated
```

Debe mantenerse:

```text
Withdrawn

≠

Invalidated
```

Los estados representan hechos diferentes.

---

# Ejemplo 36 — Completion no es Withdrawal

Debe mantenerse:

```text
Completed

≠

Withdrawn
```

Completion expresa que la Participation alcanzó su terminación
normal definida por el dominio.

Withdrawal expresa retiro.

No deben utilizarse indistintamente.

---

# Ejemplo 37 — Invalidation posterior a Completion

Cuando la State Machine oficial permita invalidar una
Participation previamente completada, el escenario conceptual es:

```text
Completed

↓

InvalidateParticipation

↓

Invalidated
```

Los hechos históricos previos permanecen preservados.

Conceptualmente:

```text
CompletedAt = T1

InvalidatedAt = T2
```

La invalidación posterior no reescribe el hecho de que Completion
ocurrió anteriormente.

---

# Ejemplo 38 — Contexto no absorbido

Una Participation mantiene:

```text
AssemblyId = ASM-500

ProposalId = PRO-500

TerritoryId = TER-500
```

Esto no significa que contenga:

```text
Assembly Aggregate

Proposal Aggregate

Territory Aggregate
```

Debe mantenerse:

```text
Cross-Aggregate Reference

=

Identity Reference
```

---

# Ejemplo 39 — Modificación externa de Assembly

## Contexto

Participation referencia:

```text
AssemblyId = ASM-600
```

Assembly cambia su propio estado.

---

## Resultado sobre Participation

Participation no modifica automáticamente su estado interno por
acceso directo al Aggregate Assembly.

La coordinación, cuando corresponda, debe realizarse mediante los
mecanismos establecidos por la arquitectura.

No debe existir:

```text
Participation.Assembly.status
```

como referencia mutable compartida.

---

# Ejemplo 40 — Modificación externa de Proposal

Participation mantiene:

```text
ProposalId = PRO-600
```

Proposal evoluciona de forma independiente.

Debe mantenerse:

```text
Proposal Aggregate

↓

Own Lifecycle
```

y:

```text
Participation Aggregate

↓

Own Lifecycle
```

La relación no fusiona ambos Aggregates.

---

# Ejemplo 41 — Command rechazado no incrementa Version

## Estado inicial

```text
ParticipationStatus = Completed

Version = 9
```

Se intenta:

```text
ActivateParticipation
```

---

## Resultado

```text
Rejected
```

El estado permanece:

```text
ParticipationStatus = Completed

Version = 9
```

No existe:

```text
Version = 10
```

porque no se produjo una modificación válida.

---

# Ejemplo 42 — Command rechazado no genera evento de éxito

## Contexto

```text
ParticipationStatus = Archived
```

Se intenta:

```text
ChangeParticipationType
```

---

## Resultado

```text
Rejected
```

No debe emitirse un evento que represente falsamente un cambio
exitoso.

---

# Ejemplo 43 — Permission Denied no modifica timestamps

## Estado inicial

```text
ParticipationStatus = Registered

StartedAt = None

Version = 1
```

Se intenta:

```text
ActivateParticipation
```

pero:

```text
Participation.Activate = Denied
```

---

## Resultado

```text
ParticipationStatus = Registered

StartedAt = None

Version = 1
```

---

# Ejemplo 44 — Read Model

Una interfaz necesita mostrar:

```text
ParticipationId

CitizenId

ParticipationType

ParticipationStatus

AssemblyId

CreatedAt
```

La consulta debe resolverse mediante una proyección apropiada del
Read Side.

Conceptualmente:

```text
Query

↓

Participation Read Model
```

No es necesario cargar el Aggregate únicamente para presentar
información.

---

# Ejemplo 45 — Dashboard

Una Organization necesita conocer:

```text
Total Participations

Active Participations

Completed Participations

Withdrawn Participations

Invalidated Participations
```

El escenario corresponde a:

```text
Participation Read Model
```

No al Repository del Write Side.

---

# Ejemplo 46 — Consulta por Citizen

Una interfaz necesita listar todas las Participations asociadas a:

```text
CitizenId = CIT-700
```

Debe utilizarse una proyección optimizada.

No debe asumirse que:

```text
ParticipationRepository
```

es un motor general de búsqueda.

---

# Ejemplo 47 — Consulta por Assembly

Una pantalla necesita mostrar las Participations relacionadas con:

```text
AssemblyId = ASM-700
```

Conceptualmente:

```text
Query

↓

Participation Read Model

↓

Participations for ASM-700
```

El Aggregate no necesita cargarse para cada fila del listado.

---

# Ejemplo 48 — Domain Event y Read Model

Después de:

```text
ParticipationActivated
```

una proyección puede actualizar:

```text
ParticipationStatusView
```

Conceptualmente:

```text
ParticipationActivated

↓

Projection

↓

Read Model Updated
```

El Read Model no modifica el Aggregate.

---

# Ejemplo 49 — Eventual Consistency

Después de confirmar una modificación:

```text
Participation

↓

Domain Event

↓

Projection
```

puede existir un intervalo en el cual:

```text
Write Side = New State

Read Side = Previous Projection
```

hasta que la proyección sea actualizada.

Esta diferencia temporal no modifica la consistencia interna del
Aggregate.

---

# Ejemplo 50 — System Actor

Un proceso automático necesita ejecutar una operación protegida.

No debe asumirse:

```text
System Actor

=

Unlimited Permission
```

Debe existir conceptualmente:

```text
System Actor

↓

Authorization

↓

Permission Granted

↓

Command

↓

Participation
```

---

# Ejemplo 51 — Integration Actor

Una integración externa solicita registrar una Participation.

El flujo conceptual es:

```text
External Integration

↓

Authenticated Identity

↓

Authorization

↓

Participation.Register

↓

RegisterParticipation

↓

Participation Aggregate
```

La integración no recibe autoridad implícita por ser externa.

---

# Ejemplo 52 — Evento externo no modifica directamente el Aggregate

Una integración recibe información externa relacionada con
Participation.

No debe ejecutarse:

```text
External Event

↓

Direct Database Update
```

El flujo debe respetar las fronteras establecidas:

```text
External Input

↓

Application

↓

Authorized Command

↓

Participation
```

cuando corresponda una modificación del dominio.

---

# Ejemplo 53 — Domain Event

Después de una activación válida:

```text
Registered

↓

ActivateParticipation

↓

Active
```

se produce:

```text
ParticipationActivated
```

El evento representa un hecho consumado.

No representa:

```text
Request to Activate
```

---

# Ejemplo 54 — Integration Event

Un Domain Event relevante puede posteriormente originar un
Integration Event según las reglas establecidas en:

```text
DOMAIN-008K-Integration-Events.md
```

Conceptualmente:

```text
ParticipationActivated

↓

Integration Mapping

↓

Integration Event
```

El Integration Event no redefine el hecho del dominio.

---

# Ejemplo 55 — Replay

Cuando una implementación utiliza Event Sourcing, una Participation
puede reconstruirse conceptualmente mediante:

```text
ParticipationRegistered

↓

ParticipationActivated

↓

ParticipationCompleted
```

Resultado:

```text
ParticipationStatus = Completed
```

Durante Replay no se ejecutan nuevamente:

```text
RegisterParticipation

ActivateParticipation

CompleteParticipation
```

---

# Ejemplo 56 — Replay no genera eventos nuevos

Historia persistida:

```text
Event 1 → ParticipationRegistered

Event 2 → ParticipationActivated

Event 3 → ParticipationCompleted
```

Durante la rehidratación:

```text
Apply Event 1

Apply Event 2

Apply Event 3
```

No debe producirse:

```text
Event 4 → ParticipationRegistered

Event 5 → ParticipationActivated

Event 6 → ParticipationCompleted
```

---

# Ejemplo 57 — Snapshot

Una implementación puede disponer de:

```text
Snapshot at Version 50
```

y posteriormente:

```text
Event 51

Event 52

Event 53
```

La reconstrucción conceptual puede ser:

```text
Snapshot Version 50

↓

Apply Events 51..53

↓

Participation Version 53
```

El Snapshot no reinicia Version.

---

# Ejemplo 58 — Persistencia relacional

Infrastructure puede representar Participation mediante tablas.

Conceptualmente:

```text
Participation Aggregate

↓

Mapper

↓

Relational Persistence
```

El dominio continúa trabajando con:

```text
Participation
```

y no con filas SQL.

---

# Ejemplo 59 — Persistencia documental

Infrastructure puede almacenar Participation como documento.

Conceptualmente:

```text
Participation

↓

Mapper

↓

Document Persistence
```

La estructura documental no redefine el Aggregate Boundary.

---

# Ejemplo 60 — Cambio de tecnología de persistencia

Una implementación puede evolucionar desde:

```text
Relational Persistence
```

hacia:

```text
Document Persistence
```

sin modificar conceptualmente:

```text
ParticipationId

OrganizationId

Lifecycle

State Machine

Invariants

Commands

Domain Events
```

La persistencia no define el dominio.

---

# Ejemplo 61 — Caso de participación en una Assembly comunitaria

## Contexto

Una Organization realiza una Assembly.

Un Citizen posee una Membership válida dentro de la Organization.

Se registra su Participation en la Assembly.

Referencias conceptuales:

```text
OrganizationId = ORG-800

CitizenId = CIT-800

MembershipId = MEM-800

AssemblyId = ASM-800
```

---

## Registro

```text
RegisterParticipation
```

produce:

```text
ParticipationStatus = Registered
```

---

## Activación

Cuando corresponda según el proceso:

```text
ActivateParticipation
```

produce:

```text
ParticipationStatus = Active
```

---

## Completion

Una vez finalizada la participación:

```text
CompleteParticipation
```

produce:

```text
ParticipationStatus = Completed
```

---

## Separación de Aggregates

Durante todo el proceso:

```text
Assembly
```

continúa siendo un Aggregate independiente.

Participation no modifica directamente:

```text
AssemblyStatus
```

---

# Ejemplo 62 — Participación vinculada a una Proposal

## Contexto

Un Citizen participa en un proceso relacionado con una Proposal.

```text
OrganizationId = ORG-810

CitizenId = CIT-810

MembershipId = MEM-810

ProposalId = PRO-810
```

Participation mantiene:

```text
ProposalId
```

como referencia.

---

## Límite

El proceso no convierte:

```text
Proposal
```

en una entidad interna de Participation.

La Proposal mantiene:

```text
Own Identity

Own Lifecycle

Own Version

Own Repository

Own Invariants
```

---

# Ejemplo 63 — Participación retirada por el participante

## Contexto

Una Participation se encuentra:

```text
Active
```

El participante dispone de la capacidad correspondiente para
solicitar Withdrawal.

---

## Flujo

```text
Actor

↓

Participation.Withdraw

↓

WithdrawParticipation

↓

State Validation

↓

Invariant Validation

↓

Withdrawn
```

---

## Resultado

```text
WithdrawnAt = Timestamp

Version = PreviousVersion + 1

ParticipationWithdrawn
```

---

# Ejemplo 64 — Invalidation administrativa

## Contexto

Una Participation se encuentra en un estado que permite
Invalidation.

Un actor administrativo posee:

```text
Participation.Invalidate
```

---

## Flujo

```text
Administrative Actor

↓

Authorization

↓

InvalidateParticipation

↓

Participation

↓

Invariant Validation

↓

Invalidated
```

---

## Regla

La autoridad administrativa no permite:

```text
Bypass Invariants
```

---

# Ejemplo 65 — Operación administrativa inválida

## Contexto

Un actor administrativo posee:

```text
Participation.Activate
```

pero intenta activar una Participation:

```text
ParticipationStatus = Archived
```

---

## Resultado

```text
Rejected
```

Debe mantenerse:

```text
Administrative Permission

≠

State Machine Bypass
```

---

# Ejemplo 66 — Cambio de contexto sin modificar Aggregate externo

## Contexto

Participation referencia:

```text
AssemblyId = ASM-A
```

Se autoriza cambiar el contexto a:

```text
AssemblyId = ASM-B
```

cuando el dominio lo permita.

---

## Resultado

Participation modifica únicamente:

```text
AssemblyId
```

No ejecuta ninguna modificación sobre:

```text
ASM-A

ASM-B
```

---

# Ejemplo 67 — Referencia inexistente

Cuando una operación requiera una referencia externa válida y la
precondición correspondiente no se encuentre satisfecha, la
operación no debe producir una Participation válida.

Debe mantenerse la regla definida por los documentos normativos
correspondientes.

El ejemplo no establece el mecanismo técnico mediante el cual se
verifica la existencia externa.

---

# Ejemplo 68 — Validación externa no amplía el Aggregate

Cuando Application necesita confirmar información relacionada con:

```text
Citizen

Membership

Assembly

Proposal

Territory
```

puede obtener el contexto requerido antes de ejecutar el Command.

Esto no convierte esos Aggregates en parte del límite de
Participation.

Debe mantenerse:

```text
Application Coordination

≠

Aggregate Expansion
```

---

# Ejemplo 69 — Una Participation por identidad

Dos registros no pueden compartir:

```text
ParticipationId = PAR-900
```

como si representaran Aggregates diferentes.

Debe mantenerse:

```text
One ParticipationId

↓

One Aggregate Identity
```

---

# Ejemplo 70 — Dos Participations independientes

Puede existir:

```text
ParticipationId = PAR-901

CitizenId = CIT-900

AssemblyId = ASM-900
```

y:

```text
ParticipationId = PAR-902

CitizenId = CIT-900

AssemblyId = ASM-901
```

Ambas son Aggregates Participation independientes.

Cada una mantiene:

```text
Own Lifecycle

Own Status

Own Version

Own Consistency Boundary
```

---

# Ejemplo 71 — Misma Assembly, Participations independientes

Puede existir:

```text
PAR-A → AssemblyId = ASM-1000

PAR-B → AssemblyId = ASM-1000

PAR-C → AssemblyId = ASM-1000
```

Cada Participation mantiene identidad independiente.

Una modificación sobre:

```text
PAR-A
```

no incrementa automáticamente:

```text
PAR-B.Version

PAR-C.Version
```

---

# Ejemplo 72 — Misma Proposal, Participations independientes

Puede existir:

```text
PAR-D → ProposalId = PRO-1000

PAR-E → ProposalId = PRO-1000
```

Ambas Participations pueden evolucionar independientemente dentro
de las reglas del dominio.

La referencia común no fusiona sus límites de consistencia.

---

# Ejemplo 73 — Atomicidad entre Status, Timestamp y Version

Estado:

```text
ParticipationStatus = Active

Version = 10
```

Completion válida:

```text
CompleteParticipation
```

debe producir coherentemente:

```text
ParticipationStatus = Completed

CompletedAt = T100

Version = 11
```

La persistencia debe preservar el conjunto como una unidad lógica.

---

# Ejemplo 74 — Fallo de persistencia

## Contexto

El Aggregate acepta válidamente:

```text
CompleteParticipation
```

pero Infrastructure no puede confirmar la persistencia.

---

## Resultado de persistencia

```text
PersistenceFailure
```

No debe informarse:

```text
Persisted
```

si el commit no ocurrió.

Debe distinguirse:

```text
Domain Acceptance

≠

Persistence Confirmation
```

---

# Ejemplo 75 — Domain Rejection antes de persistencia

## Contexto

Una Participation se encuentra:

```text
Archived
```

Se intenta:

```text
ActivateParticipation
```

---

## Resultado

```text
Domain Rejection
```

No es necesario ejecutar:

```text
Repository.save()
```

porque no existe una modificación válida que persistir.

---

# Ejemplo 76 — ConcurrencyConflict no es Domain Rejection

## Contexto

El Command produjo un estado válido respecto de la copia cargada,
pero al persistir:

```text
ExpectedVersion = 7

PersistedVersion = 8
```

---

## Resultado

```text
ConcurrencyConflict
```

Debe distinguirse de:

```text
Invalid State Transition
```

El conflicto corresponde a concurrencia de persistencia.

---

# Ejemplo 77 — Read Permission sin Write Permission

Un actor posee:

```text
Participation.Read
```

pero no:

```text
Participation.Invalidate
```

Puede acceder a una vista autorizada.

No puede ejecutar:

```text
InvalidateParticipation
```

Debe mantenerse:

```text
Read Permission

≠

Write Permission
```

---

# Ejemplo 78 — Write Permission no implica acceso irrestricto de lectura

La existencia de una capacidad de modificación específica no debe
interpretarse automáticamente como acceso a cualquier proyección o
dato sensible.

Las políticas del Read Side permanecen separadas.

---

# Ejemplo 79 — Metadata no sustituye atributos oficiales

No debe utilizarse:

```text
Metadata = {
    "status": "Completed"
}
```

como mecanismo para reemplazar:

```text
ParticipationStatus
```

El estado oficial solo evoluciona mediante comportamiento de
dominio reconocido.

---

# Ejemplo 80 — Metadata no sustituye OrganizationId

No debe utilizarse:

```text
Metadata = {
    "organization_id": "ORG-B"
}
```

para reinterpretar una Participation cuyo:

```text
OrganizationId = ORG-A
```

OrganizationId permanece inmutable.

---

# Ejemplo 81 — Metadata no sustituye Version

No debe utilizarse:

```text
Metadata = {
    "version": 100
}
```

para alterar:

```text
Version
```

Version posee semántica propia.

---

# Ejemplo 82 — Evento no modifica otro Aggregate directamente

Después de:

```text
ParticipationCompleted
```

otros componentes pueden reaccionar.

Sin embargo, el evento no significa que Participation pueda
modificar directamente:

```text
Assembly

Proposal

Voting

Document
```

Cada Aggregate conserva su propio límite.

---

# Ejemplo 83 — Coordinación mediante Application

Un caso de uso necesita consultar Assembly antes de registrar una
Participation.

Conceptualmente:

```text
Application

↓

Obtain Required Assembly Context

↓

Authorize Operation

↓

RegisterParticipation

↓

Participation Aggregate
```

Assembly no se incorpora dentro de Participation.

---

# Ejemplo 84 — Coordinación mediante eventos

Una modificación de Participation puede producir:

```text
ParticipationCompleted
```

Otro proceso puede reaccionar posteriormente.

Conceptualmente:

```text
ParticipationCompleted

↓

Event Consumer

↓

New Process
```

El nuevo proceso constituye una operación independiente.

---

# Ejemplo 85 — Integration Event no otorga Permission

Una integración recibe:

```text
ParticipationCompletedIntegrationEvent
```

cuando corresponda según el contrato de integración.

Esto no significa:

```text
Integration has Participation.Archive
```

Debe mantenerse:

```text
Event Visibility

≠

Mutation Authorization
```

---

# Ejemplo 86 — Direct Database Update prohibido

No debe utilizarse:

```text
UPDATE participation
SET status = 'Completed'
WHERE participation_id = 'PAR-001'
```

como sustituto conceptual de:

```text
CompleteParticipation
```

El comportamiento debe pasar por el Aggregate.

---

# Ejemplo 87 — Patch prohibido

No debe utilizarse:

```text
PATCH {
    "status": "Archived"
}
```

como mecanismo para evitar:

```text
ArchiveParticipation
```

La API externa puede utilizar HTTP, pero debe traducir la intención
al Command reconocido por el dominio.

---

# Ejemplo 88 — ORM no define el dominio

Una implementación puede mapear:

```text
Participation
```

a una entidad ORM.

La entidad ORM no determina:

- Lifecycle;
- State Machine;
- Invariants;
- Permissions;
- Commands;
- Domain Events.

Estas reglas permanecen en el modelo de dominio.

---

# Ejemplo 89 — FIWARE no redefine Participation

Una integración futura puede proyectar información de
Participation hacia un ecosistema FIWARE.

Conceptualmente:

```text
Participation

↓

Integration Event

↓

Adapter

↓

External Representation
```

La representación externa no modifica:

```text
Participation Aggregate
```

---

# Ejemplo 90 — Representación externa diferente

Una plataforma externa puede representar una Participation mediante
un esquema distinto.

Debe mantenerse:

```text
External Schema

≠

Domain Model
```

El Adapter realiza la traducción correspondiente.

---

# Ejemplo 91 — CorrelationId

Una operación puede transportar:

```text
CorrelationId = COR-900
```

Posteriormente, Domain Events e Integration Events pueden mantener
la correlación cuando corresponda.

CorrelationId no sustituye:

```text
ParticipationId
```

---

# Ejemplo 92 — CausationId

Una operación originada por otro hecho puede transportar:

```text
CausationId
```

para establecer trazabilidad causal.

CausationId no determina:

- identidad;
- autorización;
- estado;
- Version.

---

# Ejemplo 93 — ActorId

Un Command puede registrar:

```text
ActorId = ACT-900
```

ActorId permite trazabilidad.

No convierte al actor en entidad interna del Aggregate.

---

# Ejemplo 94 — Actor distinto del participante

El actor que ejecuta una operación puede ser diferente del Citizen
referenciado por Participation.

Ejemplo:

```text
ActorId = ADMIN-001

CitizenId = CIT-001
```

Esto puede ocurrir en una operación administrativa autorizada.

Debe mantenerse:

```text
ActorId

≠

CitizenId
```

cuando representen responsabilidades distintas.

---

# Ejemplo 95 — Participante como actor

En una operación de autoservicio puede existir:

```text
ActorId = CIT-001

CitizenId = CIT-001
```

La coincidencia de identidad no elimina la evaluación de
Authorization ni las Invariants.

---

# Ejemplo 96 — System Actor y Version

Un proceso automático autorizado carga:

```text
Version = 12
```

Antes de persistir otro proceso confirma:

```text
Version = 13
```

El System Actor recibe:

```text
ConcurrencyConflict
```

No posee excepción por ser un proceso del sistema.

---

# Ejemplo 97 — Archive preserva identidad

Antes:

```text
ParticipationId = PAR-1000
```

Después:

```text
ParticipationStatus = Archived
```

continúa:

```text
ParticipationId = PAR-1000
```

Archive no crea una nueva identidad.

---

# Ejemplo 98 — Invalidation preserva identidad

Antes:

```text
ParticipationId = PAR-1001
```

Después:

```text
ParticipationStatus = Invalidated
```

continúa:

```text
ParticipationId = PAR-1001
```

---

# Ejemplo 99 — Withdrawal preserva identidad

Antes:

```text
ParticipationId = PAR-1002
```

Después:

```text
ParticipationStatus = Withdrawn
```

continúa:

```text
ParticipationId = PAR-1002
```

---

# Ejemplo 100 — Lifecycle completo

Un recorrido conceptual válido puede ser:

```text
ParticipationRegistered

↓

Registered

↓

ParticipationActivated

↓

Active

↓

ParticipationCompleted

↓

Completed

↓

ParticipationArchived

↓

Archived
```

El historial conserva:

```text
CreatedAt

StartedAt

CompletedAt

ArchivedAt
```

y la evolución correspondiente de:

```text
Version
```

---

# Ejemplo 101 — Lifecycle con Withdrawal

Otro recorrido conceptual puede ser:

```text
ParticipationRegistered

↓

Registered

↓

ParticipationActivated

↓

Active

↓

ParticipationWithdrawn

↓

Withdrawn

↓

ParticipationArchived

↓

Archived
```

El historial conserva:

```text
CreatedAt

StartedAt

WithdrawnAt

ArchivedAt
```

---

# Ejemplo 102 — Lifecycle con Invalidation

Otro recorrido conceptual puede ser:

```text
ParticipationRegistered

↓

Registered

↓

ParticipationActivated

↓

Active

↓

ParticipationInvalidated

↓

Invalidated

↓

ParticipationArchived

↓

Archived
```

El historial conserva:

```text
CreatedAt

StartedAt

InvalidatedAt

ArchivedAt
```

---

# Ejemplo 103 — Invalidation posterior a Completion

Cuando la State Machine oficial contemple la transición:

```text
Completed

↓

Invalidated
```

el historial puede ser:

```text
CreatedAt = T1

StartedAt = T2

CompletedAt = T3

InvalidatedAt = T4
```

Debe mantenerse:

```text
CompletedAt < InvalidatedAt
```

según la secuencia real de hechos.

Invalidation no elimina Completion del historial.

---

# Ejemplo 104 — Archive posterior a Invalidation

Después del ejemplo anterior:

```text
Invalidated

↓

ArchiveParticipation

↓

Archived
```

puede mantenerse:

```text
CreatedAt = T1

StartedAt = T2

CompletedAt = T3

InvalidatedAt = T4

ArchivedAt = T5
```

La historia permanece acumulativa.

---

# Ejemplo 105 — Estado actual versus historia

Una Participation puede encontrarse actualmente:

```text
ParticipationStatus = Archived
```

y al mismo tiempo conservar:

```text
CompletedAt

InvalidatedAt

ArchivedAt
```

El estado actual no reemplaza la historia.

---

# Ejemplo 106 — Read Model reconstruible

Si una proyección de Participation se elimina, puede reconstruirse
desde las fuentes oficiales definidas por la arquitectura.

Conceptualmente:

```text
Domain Events

↓

Projection

↓

Participation Read Model
```

La pérdida de una proyección no modifica el Aggregate.

---

# Ejemplo 107 — Read Model desactualizado temporalmente

Después de una modificación confirmada:

```text
ParticipationStatus = Completed
```

una proyección puede mostrar temporalmente:

```text
ParticipationStatus = Active
```

hasta procesar:

```text
ParticipationCompleted
```

Esta situación corresponde a consistencia eventual del Read Side.

No significa que el Aggregate haya regresado a Active.

---

# Ejemplo 108 — Reconstrucción no modifica dominio

Reconstruir:

```text
ParticipationSummary

ParticipationStatusView

ParticipationStatistics
```

no ejecuta Commands sobre Participation.

Las proyecciones son derivadas.

---

# Ejemplo 109 — Analytics no modifica Participation

Un indicador puede calcular:

```text
Participation Completion Rate
```

a partir de Read Models.

El resultado analítico no cambia:

```text
ParticipationStatus
```

---

# Ejemplo 110 — Una operación, un Aggregate

Un Command dirigido a:

```text
ParticipationId = PAR-2000
```

modifica exclusivamente esa Participation.

No debe modificar simultáneamente dentro de la misma consistencia:

```text
PAR-2001

PAR-2002

Assembly

Proposal
```

---

# Ejemplo 111 — Operación masiva

Una operación administrativa desea archivar múltiples
Participations.

Conceptualmente:

```text
PAR-A

PAR-B

PAR-C
```

continúan siendo Aggregates independientes.

Cada uno debe preservar:

```text
Own Authorization Context

Own State Validation

Own Invariants

Own Version

Own Persistence Result
```

La operación masiva no fusiona los Aggregates.

---

# Ejemplo 112 — Fallo parcial en operación masiva

Si:

```text
PAR-A → Archived

PAR-B → Rejected

PAR-C → Archived
```

no debe reinterpretarse el conjunto como un único Aggregate.

Cada resultado pertenece a su Participation correspondiente.

---

# Ejemplo 113 — Importación

Una importación de Participations no debe escribir directamente el
estado interno.

Debe respetar conceptualmente:

```text
Import Input

↓

Validation

↓

Authorization

↓

RegisterParticipation

↓

Participation Aggregate
```

cuando corresponda registrar nuevas Participations.

---

# Ejemplo 114 — Importación con identidad duplicada

Una importación intenta registrar:

```text
ParticipationId = PAR-3000
```

pero esa identidad ya existe.

---

## Resultado

```text
Rejected / DuplicateIdentity
```

La importación no constituye una excepción a la identidad única.

---

# Ejemplo 115 — Importación con Organization incorrecta

Una importación intenta alterar:

```text
OrganizationId
```

de una Participation existente.

---

## Resultado

```text
Rejected
```

OrganizationId permanece inmutable independientemente del canal de
entrada.

---

# Ejemplo 116 — API

Una API recibe una intención equivalente a:

```text
Complete Participation
```

El Adapter puede traducirla a:

```text
CompleteParticipation
```

El protocolo externo no modifica la semántica del dominio.

---

# Ejemplo 117 — UI

Una interfaz muestra:

```text
Complete
```

solo cuando el usuario posee la capacidad correspondiente.

Sin embargo, aunque el botón esté visible:

```text
Participation Aggregate
```

continúa validando su estado e Invariants.

---

# Ejemplo 118 — UI desactualizada

Una interfaz cree que:

```text
Version = 5
```

pero el Aggregate ya se encuentra en:

```text
Version = 6
```

Una modificación basada en Version 5 puede producir:

```text
ConcurrencyConflict
```

La interfaz no determina el estado oficial.

---

# Ejemplo 119 — No confianza en cliente

Un cliente envía:

```text
ParticipationStatus = Completed
```

como parte de una solicitud.

El dominio no debe aceptar el estado únicamente porque el cliente
lo proporcionó.

La intención debe expresarse mediante:

```text
CompleteParticipation
```

y validarse según las reglas oficiales.

---

# Ejemplo 120 — No confianza en Metadata externa

Un sistema externo envía Metadata indicando:

```text
"archived": true
```

Esto no equivale a:

```text
ArchiveParticipation
```

El estado solo cambia mediante comportamiento reconocido por el
Aggregate.

---

# Escenarios Válidos Resumidos

Ejemplos de operaciones válidas cuando todas sus precondiciones se
cumplen:

```text
RegisterParticipation

Registered → Active

Active → Completed

Registered / Active → Withdrawn

Allowed State → Invalidated

Completed / Withdrawn / Invalidated → Archived

Allowed ParticipationType Change

Allowed ParticipationContext Change

Allowed Metadata Update
```

Las transiciones exactas permanecen gobernadas por la State
Machine oficial.

---

# Escenarios Inválidos Resumidos

Ejemplos de operaciones que deben rechazarse cuando violen las
reglas establecidas:

```text
Modify ParticipationId

Modify OrganizationId

Activate Archived Participation

Complete Registered Participation

Modify Archived Participation

Bypass Permission

Bypass State Machine

Bypass Invariants

Direct Database State Change

Silent Concurrent Overwrite

Reuse Archived ParticipationId

Embed Mutable External Aggregate

Increment Version on Load

Generate New Domain Events on Rehydration
```

---

# Matriz de Ejemplos de Estado

```text
Initial State     Operation                    Expected Result

Registered        ActivateParticipation        Active

Active            CompleteParticipation        Completed

Active            WithdrawParticipation        Withdrawn

Completed         ArchiveParticipation         Archived

Withdrawn         ArchiveParticipation         Archived

Invalidated       ArchiveParticipation         Archived

Completed         ActivateParticipation        Rejected

Archived          ActivateParticipation        Rejected

Archived          ChangeParticipationType      Rejected
```

La matriz ilustra reglas documentadas formalmente en Lifecycle y
State Machine.

---

# Matriz de Ejemplos de Authorization

```text
Permission                         Operation                      Result

Participation.Register             RegisterParticipation          May Attempt

Participation.Activate             ActivateParticipation          May Attempt

Participation.Complete             CompleteParticipation          May Attempt

Participation.Withdraw             WithdrawParticipation          May Attempt

Participation.Invalidate           InvalidateParticipation        May Attempt

Participation.Archive              ArchiveParticipation           May Attempt

Participation.ChangeType           ChangeParticipationType        May Attempt

Participation.ChangeContext        ChangeParticipationContext     May Attempt

Participation.UpdateMetadata       UpdateParticipationMetadata    May Attempt
```

`May Attempt` no significa éxito garantizado.

---

# Matriz de Ejemplos de Version

```text
Situation                          Version Result

Successful Registration            Increment according to model

Successful Activation              Increment

Successful Completion              Increment

Successful Withdrawal              Increment

Successful Invalidation            Increment

Successful Archive                 Increment

Rejected Command                   Unchanged

Permission Denied                  Unchanged

Load                               Unchanged

Rehydration                        Unchanged

Concurrency Conflict               No new persisted version
```

La definición normativa completa pertenece a:

```text
DOMAIN-008I-Versioning.md
```

---

# Matriz de Referencias

```text
Reference         Represents                    Embedded Aggregate

OrganizationId    Owning Organization           No

CitizenId         Citizen Reference             No

MembershipId      Membership Reference          No

AssemblyId        Assembly Reference            No

ProposalId        Proposal Reference            No

TerritoryId       Territory Reference           No
```

---

# Matriz de Responsabilidades

```text
Concern                         Responsible Component

Participation Identity          Participation

Participation Lifecycle         Participation

State Transitions               Participation

Invariants                      Participation

Authorization                   Authorization Capability

Persistence                     ParticipationRepository

Concurrency Persistence         ParticipationRepository

Read Queries                    Participation Read Models

Assembly Lifecycle              Assembly Aggregate

Proposal Lifecycle              Proposal Aggregate

Citizen Lifecycle               Citizen Aggregate

Membership Lifecycle            Membership Aggregate

Territory Lifecycle             Territory Aggregate

External Integration            Integration Layer

Audit                           Audit Context
```

---

# Anti-Ejemplo 1 — Estado modificado directamente

Incorrecto:

```text
participation.status = Completed
```

Correcto conceptualmente:

```text
CompleteParticipation

↓

Participation.complete()

↓

Invariant Validation

↓

Completed
```

---

# Anti-Ejemplo 2 — OrganizationId mutable

Incorrecto:

```text
participation.organization_id = another_organization
```

OrganizationId permanece inmutable.

---

# Anti-Ejemplo 3 — Aggregate externo embebido

Incorrecto:

```text
Participation {
    Assembly mutable_assembly
}
```

Correcto:

```text
Participation {
    AssemblyId
}
```

---

# Anti-Ejemplo 4 — Repository con lógica de dominio

Incorrecto:

```text
ParticipationRepository.complete(participation_id)
```

cuando esta operación implementa la transición de dominio dentro
del Repository.

Correcto:

```text
Repository.getById()

↓

Participation.complete()

↓

Repository.save()
```

---

# Anti-Ejemplo 5 — Permission como Invariant

Incorrecto:

```text
Actor is Administrator

↓

Any Transition Allowed
```

Correcto:

```text
Permission Granted

↓

State Machine

↓

Invariant Validation

↓

Accept or Reject
```

---

# Anti-Ejemplo 6 — Read Model como fuente de escritura

Incorrecto:

```text
Update Participation Read Model

↓

Assume Aggregate Updated
```

Correcto:

```text
Command

↓

Participation Aggregate

↓

Domain Event

↓

Projection

↓

Read Model
```

---

# Anti-Ejemplo 7 — Evento como Command

Incorrecto:

```text
ParticipationCompleted
```

utilizado como solicitud para completar.

Correcto:

```text
CompleteParticipation

↓

ParticipationCompleted
```

---

# Anti-Ejemplo 8 — Replay ejecutando Commands

Incorrecto:

```text
Replay ParticipationActivated

↓

Execute ActivateParticipation
```

Correcto:

```text
Replay ParticipationActivated

↓

Apply Historical Event
```

---

# Anti-Ejemplo 9 — Archive como Delete

Incorrecto:

```text
ArchiveParticipation

↓

Delete Aggregate Identity
```

Correcto:

```text
ArchiveParticipation

↓

ParticipationStatus = Archived

↓

Identity Preserved
```

---

# Anti-Ejemplo 10 — Last Write Wins

Incorrecto:

```text
Version Conflict

↓

Overwrite Latest State
```

Correcto:

```text
Version Conflict

↓

ConcurrencyConflict
```

---

# Anti-Ejemplo 11 — Metadata como bypass

Incorrecto:

```text
UpdateMetadata({
    "status": "Completed"
})
```

para evitar `CompleteParticipation`.

Correcto:

```text
CompleteParticipation
```

para modificar el estado.

---

# Anti-Ejemplo 12 — Integración privilegiada

Incorrecto:

```text
External Integration

↓

Unlimited Participation Access
```

Correcto:

```text
External Integration

↓

Authentication

↓

Authorization

↓

Command

↓

Participation
```

---

# Anti-Ejemplo 13 — Transacción distribuida innecesaria

Incorrecto:

```text
Participation

+

Assembly

+

Proposal

+

Membership

↓

Single Aggregate Transaction
```

Correcto:

```text
Participation

↓

Own Consistency Boundary
```

con coordinación externa cuando corresponda.

---

# Anti-Ejemplo 14 — Consulta masiva mediante Aggregates

Incorrecto como patrón normal de lectura:

```text
Load 100000 Participation Aggregates

↓

Build Dashboard
```

Correcto:

```text
Participation Read Model

↓

Dashboard Query
```

---

# Anti-Ejemplo 15 — Cliente determina Version

Incorrecto:

```text
Client sends:

Version = 999
```

y el sistema acepta ese valor como nueva versión oficial.

Version debe evolucionar conforme al modelo de dominio y
concurrencia establecido.

---

# Reglas de Interpretación

Los ejemplos contenidos en este documento deben interpretarse
siempre dentro de los límites definidos por los documentos
normativos.

No deben utilizarse para:

- crear nuevos estados;
- crear nuevas transiciones;
- crear nuevos Commands;
- crear nuevos eventos;
- crear nuevos Permissions;
- modificar Invariants;
- ampliar el Aggregate Boundary;
- cambiar la semántica de Version;
- introducir dependencias tecnológicas;
- convertir Infrastructure en dominio.

---

# Relación con Lifecycle

Los ejemplos de transición ilustran:

```text
DOMAIN-008A-Lifecycle.md
```

Lifecycle continúa siendo la fuente normativa para la evolución
temporal de Participation.

---

# Relación con State Machine

La validez de las transiciones ilustradas debe verificarse contra:

```text
DOMAIN-008B-State-Machine.md
```

Los ejemplos no crean transiciones implícitas.

---

# Relación con Commands

Las intenciones ilustradas utilizan Commands definidos en:

```text
DOMAIN-008C-Commands.md
```

Un ejemplo no constituye autorización para introducir un Command
no documentado.

---

# Relación con Domain Events

Los hechos ilustrados corresponden a eventos definidos en:

```text
DOMAIN-008D-Domain-Events.md
```

Los ejemplos no redefinen sus contratos.

---

# Relación con Invariants

Todos los escenarios válidos presuponen el cumplimiento de:

```text
DOMAIN-008E-Invariants.md
```

Un ejemplo abreviado no elimina una Invariant por no mostrarla
explícitamente.

---

# Relación con Permissions

La autorización ilustrada corresponde a:

```text
DOMAIN-008F-Permissions.md
```

Los ejemplos mantienen:

```text
Permission Granted

≠

Operation Guaranteed
```

---

# Relación con Repository Contract

Los ejemplos de persistencia corresponden a:

```text
DOMAIN-008G-Repository-Contract.md
```

El Repository no introduce comportamiento de dominio.

---

# Relación con Versioning

La evolución de Version ilustrada corresponde a:

```text
DOMAIN-008I-Versioning.md
```

Los números utilizados en ejemplos son demostrativos del orden
conceptual y no sustituyen las reglas normativas de Versioning.

---

# Relación con Consistency Boundary

Las referencias entre Aggregates ilustran:

```text
DOMAIN-008J-Consistency-Boundary.md
```

Los ejemplos preservan Participation como unidad independiente de
consistencia.

---

# Relación con Integration Events

Los escenarios de integración deben interpretarse según:

```text
DOMAIN-008K-Integration-Events.md
```

Un Domain Event no se convierte automáticamente en contrato
externo.

---

# Relación con Read Model

Las consultas ilustradas corresponden a:

```text
DOMAIN-008L-Read-Model.md
```

Los Read Models permanecen separados del Aggregate de escritura.

---

# Relación con Test Scenarios

Los escenarios documentados aquí proporcionan ejemplos
conceptuales.

Las verificaciones formales y sistemáticas se desarrollan en:

```text
DOMAIN-008M-Test-Scenarios.md
```

---

# Relación con Performance Rules

Los ejemplos no autorizan optimizaciones que violen:

```text
DOMAIN-008N-Performance-Rules.md
```

Performance no puede utilizarse para evitar las reglas del
Aggregate.

---

# Relación con Security Model

Los ejemplos de actores, Permissions e integraciones deben
interpretarse conjuntamente con:

```text
DOMAIN-008O-Security-Model.md
```

---

# Relación con Extension Points

Ningún ejemplo constituye por sí mismo un Extension Point.

Las extensiones permitidas se documentan exclusivamente en:

```text
DOMAIN-008P-Extension-Points.md
```

---

# Restricciones

No está permitido interpretar estos ejemplos como autorización
para:

- introducir nuevos atributos en Participation;
- introducir nuevos estados;
- introducir nuevas transiciones;
- introducir nuevos Commands;
- introducir nuevos Domain Events;
- introducir nuevos Integration Events;
- introducir nuevas Invariants;
- introducir nuevos Permissions;
- modificar ParticipationId;
- modificar OrganizationId;
- reutilizar identidades archivadas;
- modificar Aggregates externos dentro de Participation;
- utilizar Metadata para evitar reglas;
- utilizar Repository para ejecutar comportamiento;
- utilizar Read Models como fuente de escritura;
- utilizar Infrastructure como definición del dominio;
- evitar Versioning;
- permitir sobrescrituras concurrentes silenciosas;
- evitar Authorization;
- evitar State Machine;
- evitar Lifecycle;
- evitar Invariants;
- convertir Archive en Delete;
- convertir Domain Events en Commands;
- ejecutar Commands durante Replay;
- generar nuevos eventos durante Rehydration;
- asumir que un actor administrativo puede producir estados
  inválidos;
- asumir que una integración externa posee autoridad ilimitada.

---

# Principios Arquitectónicos

Los ejemplos oficiales mantienen el flujo:

```text
Actor

↓

Authorization

↓

Command

↓

Participation Aggregate

↓

State Machine

↓

Invariant Validation

↓

Valid State Change

↓

Version Evolution

↓

Domain Event

↓

Repository Persistence
```

Cuando corresponda comunicación externa:

```text
Domain Event

↓

Integration Mapping

↓

Integration Event
```

Cuando corresponda lectura:

```text
Domain Event

↓

Projection

↓

Participation Read Model
```

Cuando una operación es inválida:

```text
Command

↓

Participation Aggregate

↓

Rule Violation

↓

Rejected

↓

No Valid State Change

↓

No Version Increment

↓

No Success Domain Event
```

Cuando la autorización falla:

```text
Actor

↓

Permission Denied

↓

No Command Execution

↓

No Aggregate Modification
```

---

# Definición de Éxito

Los Examples del Aggregate **Participation** constituyen la
referencia conceptual oficial para observar cómo las reglas
definidas en los documentos normativos del Aggregate se combinan en
escenarios concretos de AURA Core.

Los ejemplos garantizan que:

- Registration se comprenda como creación controlada de una
  Participation;
- Activation represente el inicio válido de su actividad;
- Completion represente una terminación válida;
- Withdrawal permanezca diferenciado de Completion e Invalidation;
- Invalidation mantenga su significado propio;
- Archive preserve identidad e historia;
- ParticipationId permanezca inmutable;
- OrganizationId permanezca inmutable;
- las referencias hacia Citizen, Membership, Assembly, Proposal y
  Territory permanezcan expresadas mediante identidad;
- los Aggregates externos no sean absorbidos;
- Permissions permitan intentar operaciones sin reemplazar las
  reglas del dominio;
- State Machine continúe gobernando las transiciones;
- Invariants permanezcan obligatorias;
- Version evolucione únicamente ante modificaciones válidas;
- los conflictos concurrentes sean explícitos;
- Repository preserve el Aggregate sin introducir comportamiento;
- Read Models permanezcan separados del Write Side;
- Domain Events representen hechos consumados;
- Integration Events permanezcan separados del modelo interno;
- rehidratación y Replay no generen nuevas decisiones;
- los timestamps históricos permanezcan preservados;
- las integraciones externas respeten las mismas fronteras del
  dominio;
- los ejemplos no introduzcan nuevas decisiones arquitectónicas.

La regla fundamental de interpretación es:

```text
Example

=

Application of Existing Domain Rules
```

y nunca:

```text
Example

=

New Domain Rule
```

Por lo tanto:

```text
DOMAIN-008H-Examples.md
```

documenta escenarios concretos exclusivamente para explicar,
verificar y comunicar el comportamiento ya establecido del
Aggregate **Participation**, manteniendo íntegramente el patrón DDD
consolidado de AURA Core y sin alterar las decisiones conceptuales
definidas por sus documentos normativos oficiales.