# DOMAIN-006H — Assembly Examples

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Assembly Management

Aggregate:
Assembly

Autor:
ARADA

Documentos relacionados:

* DOMAIN-006-Aggregate.md
* DOMAIN-006A-Lifecycle.md
* DOMAIN-006B-State-Machine.md
* DOMAIN-006C-Commands.md
* DOMAIN-006D-Domain-Events.md
* DOMAIN-006E-Invariants.md
* DOMAIN-006F-Permissions.md
* DOMAIN-006G-Repository-Contract.md
* DOMAIN-006I-Versioning.md
* DOMAIN-006J-Consistency-Boundary.md
* DOMAIN-006K-Integration-Events.md
* DOMAIN-006L-Read-Model.md
* DOMAIN-006M-Test-Scenarios.md
* DOMAIN-006N-Performance-Rules.md
* DOMAIN-006O-Security-Model.md
* DOMAIN-006P-Extension-Points.md
* DOMAIN-001-Aggregate.md
* DOMAIN-002-Aggregate.md
* DOMAIN-003-Aggregate.md
* DOMAIN-004-Aggregate.md
* DOMAIN-005-Aggregate.md
* CORE-003-Shared-Kernel.md
* CORE-004-Ubiquitous-Language.md
* CORE-006-Domain-Invariants.md
* CORE-008-Aggregate-Design-Rules.md
* CORE-011-Repository-Contracts.md

---

# Objetivo

Proporcionar ejemplos conceptuales completos del Aggregate
**Assembly** que permitan comprender cómo deben aplicarse en
conjunto:

* identidad;
* Lifecycle;
* State Machine;
* Commands;
* Domain Events;
* invariantes;
* Permissions;
* Repository Contract;
* Versioning;
* Consistency Boundary;
* relaciones con otros Aggregates;
* Integration Events;
* Read Models.

Los ejemplos definidos en este documento forman parte de la
documentación conceptual del Aggregate.

No constituyen código de implementación.

No reemplazan las reglas normativas definidas en los demás
documentos del Aggregate.

Su propósito es mostrar cómo dichas reglas deben interpretarse de
manera coherente cuando aparecen combinadas dentro de casos reales.

---

# Propósito

El modelo conceptual de Assembly contiene múltiples reglas que
deben actuar conjuntamente.

Un ejemplo válido nunca debe analizar únicamente:

```text
Command
```

sin considerar:

```text
Permission

Current State

Guards

Invariants

Version

Domain Events

Consistency Boundary
```

De igual forma, una transición válida no puede analizarse
ignorando:

* OrganizationId;
* programación;
* convocatoria;
* modalidad;
* condiciones de realización;
* concurrencia;
* trazabilidad.

Este documento permite observar el comportamiento del Aggregate
como una unidad coherente.

---

# Principio Fundamental

Todo ejemplo debe respetar la secuencia conceptual:

```text
Intent
    │
    ▼
Command
    │
    ▼
Authorization
    │
    ▼
Load Aggregate
    │
    ▼
Version Validation
    │
    ▼
State Machine
    │
    ▼
Guards
    │
    ▼
Invariants
    │
    ▼
Domain Behavior
    │
    ▼
New Valid State
    │
    ▼
Domain Event
    │
    ▼
Repository Persistence
```

Cuando corresponda:

```text
Domain Event
    │
    ▼
Application / Integration Handler
    │
    ▼
Integration Event
    │
    ▼
External System
```

Las responsabilidades no deben mezclarse.

---

# Naturaleza de los Ejemplos

Los ejemplos de este documento son:

```text
conceptual examples
```

No son:

```text
API contracts

database schemas

DTO definitions

framework code

HTTP payloads

ORM entities
```

La sintaxis utilizada busca representar conceptos del dominio.

No prescribe detalles técnicos de implementación.

---

# Convenciones Utilizadas

Los ejemplos utilizan identificadores conceptuales como:

```text
AssemblyId = ASM-001

OrganizationId = ORG-001

TerritoryId = TERR-001

ActorId = ACT-001
```

Estos valores existen únicamente para facilitar comprensión.

No representan una estrategia obligatoria para generar
identificadores.

---

# Aggregate de Referencia Inicial

Muchos ejemplos utilizarán una Assembly conceptual:

```text
AssemblyId:
ASM-001

OrganizationId:
ORG-001

TerritoryId:
TERR-001

AssemblyName:
Asamblea Ordinaria Agosto 2026

AssemblyType:
Ordinary

AssemblyPurpose:
Revisar materias de gestión comunitaria

AssemblyStatus:
Draft

CreatedAt:
2026-08-01T10:00:00-04:00

Version:
1
```

Este estado representa una Assembly recién creada.

---

# Ejemplo 1 — Creación de una Assembly

## Contexto

Una Organization necesita crear una nueva Asamblea ordinaria.

La Organization es:

```text
OrganizationId = ORG-001
```

El Actor autorizado es:

```text
ActorId = ACT-001
```

El Actor posee:

```text
Assembly.Create
```

---

# Command

```text
CreateAssembly

CommandId:
CMD-001

AssemblyId:
ASM-001

OrganizationId:
ORG-001

ActorId:
ACT-001

AssemblyName:
Asamblea Ordinaria Agosto 2026

AssemblyType:
Ordinary

AssemblyPurpose:
Revisar materias de gestión comunitaria

Timestamp:
2026-08-01T10:00:00-04:00

CorrelationId:
CORR-001

CausationId:
null
```

---

# Validaciones de Autorización

Debe verificarse:

```text
Actor has Assembly.Create
```

dentro de:

```text
OrganizationId = ORG-001
```

La autorización válida permite intentar la creación.

No garantiza todavía que el Aggregate pueda crearse.

---

# Invariantes Iniciales

Debe cumplirse:

```text
AssemblyId valid

OrganizationId valid

AssemblyName valid

AssemblyType valid

CreatedAt valid
```

Debe además verificarse que:

```text
AssemblyId = ASM-001
```

no se encuentre utilizado.

---

# Estado Resultante

```text
AssemblyId:
ASM-001

OrganizationId:
ORG-001

AssemblyName:
Asamblea Ordinaria Agosto 2026

AssemblyType:
Ordinary

AssemblyPurpose:
Revisar materias de gestión comunitaria

AssemblyStatus:
Draft

CreatedAt:
2026-08-01T10:00:00-04:00

Version:
1
```

---

# Domain Event

```text
AssemblyCreated

EventId:
EVT-001

AssemblyId:
ASM-001

OrganizationId:
ORG-001

AggregateVersion:
1

OccurredAt:
2026-08-01T10:00:00-04:00

CorrelationId:
CORR-001

CausationId:
CMD-001
```

---

# Resultado Conceptual

La Assembly existe.

Pero todavía no se encuentra:

```text
Scheduled

Convoked

InProgress
```

Debe mantenerse:

```text
Created
    ≠
Scheduled
```

---

# Ejemplo 2 — Creación Rechazada por Falta de Permission

## Estado Inicial

No existe Assembly.

Actor:

```text
ActorId = ACT-002
```

no posee:

```text
Assembly.Create
```

---

# Intento

```text
CreateAssembly
```

---

# Resultado

```text
PermissionDenied
```

No se crea Assembly.

No existe:

```text
AssemblyCreated
```

No existe Version inicial.

No existe modificación de dominio.

---

# Regla Demostrada

Debe mantenerse:

```text
PermissionDenied
    =>
No Aggregate Change
```

---

# Ejemplo 3 — Creación Rechazada por Identidad Duplicada

## Estado

Ya existe:

```text
AssemblyId = ASM-001
```

---

# Nuevo Command

Otro proceso intenta:

```text
CreateAssembly

AssemblyId:
ASM-001
```

---

# Resultado Esperado

```text
AssemblyAlreadyExists
```

No debe sobrescribirse la Assembly existente.

No se produce:

```text
AssemblyCreated
```

para una nueva entidad con la misma identidad.

---

# Regla Demostrada

Debe mantenerse:

```text
one Assembly
per AssemblyId
```

---

# Ejemplo 4 — Programación de una Assembly

## Estado Inicial

```text
AssemblyStatus:
Draft

Version:
1
```

Actor posee:

```text
Assembly.Schedule
```

---

# Command

```text
ScheduleAssembly

CommandId:
CMD-002

AssemblyId:
ASM-001

OrganizationId:
ORG-001

ActorId:
ACT-001

ScheduledStartAt:
2026-08-20T18:00:00-04:00

ScheduledEndAt:
2026-08-20T20:00:00-04:00

AssemblyModality:
InPerson

AssemblyLocation:
Sede Vecinal Principal

ExpectedVersion:
1

CorrelationId:
CORR-001

CausationId:
CMD-001
```

---

# Validaciones

Debe cumplirse:

```text
Permission = Assembly.Schedule

CurrentStatus = Draft

ExpectedVersion = PersistedVersion

ScheduledStartAt valid

ScheduledEndAt > ScheduledStartAt

AssemblyModality valid

AssemblyLocation valid
```

---

# Transición

```text
Draft
    │
    ▼
Scheduled
```

---

# Estado Resultante

```text
AssemblyStatus:
Scheduled

ScheduledStartAt:
2026-08-20T18:00:00-04:00

ScheduledEndAt:
2026-08-20T20:00:00-04:00

AssemblyModality:
InPerson

AssemblyLocation:
Sede Vecinal Principal

Version:
2
```

---

# Domain Event

```text
AssemblyScheduled

EventId:
EVT-002

AssemblyId:
ASM-001

OrganizationId:
ORG-001

AggregateVersion:
2

OccurredAt:
2026-08-01T12:00:00-04:00

CorrelationId:
CORR-001

CausationId:
CMD-002
```

---

# Regla Demostrada

Programar una Assembly cambia:

```text
Draft
```

a:

```text
Scheduled
```

pero no produce:

```text
Convoked
```

ni:

```text
InProgress
```

---

# Ejemplo 5 — Programación con Horario Inválido

## Estado Inicial

```text
AssemblyStatus:
Draft
```

---

# Command Inválido

```text
ScheduleAssembly

ScheduledStartAt:
2026-08-20T20:00:00-04:00

ScheduledEndAt:
2026-08-20T18:00:00-04:00
```

---

# Violación

Debe cumplirse:

```text
ScheduledEndAt > ScheduledStartAt
```

pero:

```text
20:00 > 18:00
```

no corresponde al orden de los campos introducidos.

La finalización programada precede al inicio.

---

# Resultado

```text
InvalidAssemblySchedule
```

---

# Estado Posterior

Debe mantenerse:

```text
AssemblyStatus = Draft

Version = previous Version
```

No existe:

```text
AssemblyScheduled
```

---

# Ejemplo 6 — Programación con Duración Nula

## Command

```text
ScheduledStartAt:
2026-08-20T18:00:00-04:00

ScheduledEndAt:
2026-08-20T18:00:00-04:00
```

---

# Resultado

Inválido.

Debe mantenerse:

```text
ScheduledEndAt > ScheduledStartAt
```

No:

```text
ScheduledEndAt >= ScheduledStartAt
```

cuando ScheduledEndAt se encuentra definido.

---

# Ejemplo 7 — Modalidad Presencial

Una Assembly se programa como:

```text
AssemblyModality:
InPerson
```

Puede requerir:

```text
AssemblyLocation
```

válida.

Ejemplo:

```text
AssemblyLocation:
Sede Comunitaria Los Robles
```

La Location representa el lugar de realización.

No representa:

```text
Territory
```

---

# Ejemplo 8 — Territory y Location no son Equivalentes

Una Assembly puede poseer:

```text
TerritoryId:
TERR-001
```

y:

```text
AssemblyLocation:
Sede Social Villa Esperanza
```

TerritoryId responde:

```text
¿En qué contexto territorial se desarrolla la Assembly?
```

AssemblyLocation responde:

```text
¿Dónde se realizará físicamente?
```

Debe mantenerse:

```text
TerritoryId
    ≠
AssemblyLocation
```

---

# Ejemplo 9 — Assembly Remota

Una Assembly puede programarse como:

```text
AssemblyModality:
Remote
```

En este caso una ubicación física puede no ser necesaria.

Assembly no almacena:

```text
ZoomPassword

MeetingToken

OAuthCredential

VideoPlatformSession
```

Estos conceptos no pertenecen al Aggregate.

---

# Ejemplo 10 — Assembly Híbrida

Puede existir:

```text
AssemblyModality:
Hybrid
```

con:

```text
AssemblyLocation:
Centro Comunitario Central
```

y condiciones externas para participación remota.

Assembly mantiene la modalidad.

No administra la infraestructura tecnológica utilizada para
conectar participantes remotos.

---

# Ejemplo 11 — Reprogramación desde Scheduled

## Estado Inicial

```text
AssemblyStatus:
Scheduled

ScheduledStartAt:
2026-08-20T18:00:00-04:00

ScheduledEndAt:
2026-08-20T20:00:00-04:00

Version:
2
```

---

# Command

```text
RescheduleAssembly

CommandId:
CMD-003

NewScheduledStartAt:
2026-08-21T18:30:00-04:00

NewScheduledEndAt:
2026-08-21T20:30:00-04:00

ExpectedVersion:
2
```

---

# Resultado

Assembly permanece:

```text
Scheduled
```

pero la programación cambia.

---

# Nuevo Estado

```text
ScheduledStartAt:
2026-08-21T18:30:00-04:00

ScheduledEndAt:
2026-08-21T20:30:00-04:00

Version:
3
```

---

# Domain Event

```text
AssemblyRescheduled

PreviousScheduledStartAt:
2026-08-20T18:00:00-04:00

NewScheduledStartAt:
2026-08-21T18:30:00-04:00

PreviousScheduledEndAt:
2026-08-20T20:00:00-04:00

NewScheduledEndAt:
2026-08-21T20:30:00-04:00

AggregateVersion:
3
```

---

# Regla Demostrada

No todo Domain Event implica cambio de AssemblyStatus.

Debe mantenerse:

```text
Scheduled
    │
    ▼
Scheduled
```

mientras existe un cambio real de dominio.

---

# Ejemplo 12 — No-Op de Reprogramación

## Estado

```text
ScheduledStartAt:
2026-08-21T18:30:00-04:00
```

---

# Command

Solicita exactamente:

```text
ScheduledStartAt:
2026-08-21T18:30:00-04:00
```

sin ningún otro cambio.

---

# Resultado

Puede tratarse como:

```text
No-Op
```

Debe mantenerse:

```text
VersionAfter = VersionBefore
```

y no debe producirse:

```text
AssemblyRescheduled
```

---

# Ejemplo 13 — Convocatoria Válida

## Estado Inicial

```text
AssemblyStatus:
Scheduled

Version:
3
```

Actor posee:

```text
Assembly.Convoke
```

---

# Command

```text
ConvokeAssembly

CommandId:
CMD-004

AssemblyId:
ASM-001

OrganizationId:
ORG-001

ConvokedAt:
2026-08-10T12:00:00-04:00

ConvocationMethod:
OfficialOrganizationChannel

ExpectedVersion:
3
```

---

# Guards

Debe verificarse:

```text
CurrentStatus = Scheduled

ScheduleValid = true

ConvocationValid = true

ConvocationRulesSatisfied = true
```

---

# Transición

```text
Scheduled
    │
    ▼
Convoked
```

---

# Estado Resultante

```text
AssemblyStatus:
Convoked

ConvokedAt:
2026-08-10T12:00:00-04:00

Version:
4
```

---

# Domain Event

```text
AssemblyConvoked

EventId:
EVT-004

AssemblyId:
ASM-001

AggregateVersion:
4
```

---

# Ejemplo 14 — Convocatoria no es Notification

Después de:

```text
AssemblyConvoked
```

un handler puede iniciar:

```text
CreateNotification
```

en otro contexto.

Conceptualmente:

```text
AssemblyConvoked
      │
      ▼
Notification Handler
      │
      ▼
Notification Command
      │
      ▼
Notification Aggregate
```

Assembly no contiene:

```text
Notification
```

y no envía mensajes directamente.

---

# Regla Demostrada

Debe mantenerse:

```text
AssemblyConvoked
    ≠
NotificationDelivered
```

---

# Ejemplo 15 — Convocatoria desde Draft

## Estado

```text
AssemblyStatus:
Draft
```

Actor posee:

```text
Assembly.Convoke
```

---

# Command

```text
ConvokeAssembly
```

---

# Resultado

Debe ser rechazado.

Aunque:

```text
PermissionGranted = true
```

la transición:

```text
Draft -> Convoked
```

no se encuentra permitida.

---

# Regla Demostrada

```text
Permission Granted
    ≠
Operation Valid
```

---

# Ejemplo 16 — Cambio de Nombre

## Estado

```text
AssemblyStatus:
Scheduled

AssemblyName:
Asamblea Ordinaria Agosto 2026

Version:
4
```

---

# Command

```text
RenameAssembly

NewName:
Asamblea General Ordinaria Agosto 2026

ExpectedVersion:
4
```

---

# Resultado

```text
AssemblyName:
Asamblea General Ordinaria Agosto 2026

Version:
5
```

---

# Domain Event

```text
AssemblyRenamed

PreviousName:
Asamblea Ordinaria Agosto 2026

NewName:
Asamblea General Ordinaria Agosto 2026

AggregateVersion:
5
```

AssemblyId permanece:

```text
ASM-001
```

---

# Ejemplo 17 — Rename no Cambia Identidad

Antes:

```text
AssemblyId:
ASM-001

AssemblyName:
Asamblea Ordinaria Agosto 2026
```

Después:

```text
AssemblyId:
ASM-001

AssemblyName:
Asamblea General Ordinaria Agosto 2026
```

Debe mantenerse:

```text
AssemblyId before
=
AssemblyId after
```

---

# Ejemplo 18 — Rename No-Op

Si:

```text
CurrentName:
Asamblea General Ordinaria Agosto 2026
```

y se solicita:

```text
NewName:
Asamblea General Ordinaria Agosto 2026
```

no existe cambio semántico.

No debe generarse necesariamente:

```text
AssemblyRenamed
```

ni incrementarse Version.

---

# Ejemplo 19 — Cambio de Tipo

## Estado

```text
AssemblyStatus:
Draft

AssemblyType:
Ordinary
```

---

# Command

```text
ChangeAssemblyType

NewAssemblyType:
Extraordinary
```

---

# Resultado

Puede ser válido si las invariantes y reglas permiten el cambio.

Domain Event:

```text
AssemblyTypeChanged
```

---

# Ejemplo 20 — Cambio de Tipo después del Inicio

## Estado

```text
AssemblyStatus:
InProgress
```

---

# Command

```text
ChangeAssemblyType

Ordinary -> Extraordinary
```

---

# Resultado

Debe rechazarse cuando ello reescribiría la naturaleza histórica
de una reunión que ya comenzó.

La mutabilidad disminuye conforme avanza el Lifecycle.

---

# Ejemplo 21 — Cambio de Purpose

Una Assembly Draft posee:

```text
AssemblyPurpose:
Revisión administrativa
```

Puede modificarse válidamente a:

```text
AssemblyPurpose:
Revisión administrativa y aprobación de plan anual
```

si:

* el estado lo permite;
* AssemblyType es compatible;
* las reglas siguen siendo válidas.

Debe producir:

```text
AssemblyPurposeChanged
```

---

# Ejemplo 22 — Purpose no es Proposal

La propiedad:

```text
AssemblyPurpose:
Analizar mejoras de seguridad vecinal
```

no constituye:

```text
Proposal
```

Una Proposal concreta podría posteriormente referenciar:

```text
AssemblyId = ASM-001
```

manteniendo su propio Aggregate.

---

# Ejemplo 23 — AssemblyRules

Una Assembly puede poseer reglas conceptuales:

```text
AssemblyRules:

QuorumRequired:
true

RemoteParticipationAllowed:
false

ProposalSubmissionAllowed:
true

VotingAllowed:
true
```

Estas reglas describen condiciones propias de la reunión.

No convierten:

```text
Proposal
```

ni:

```text
Voting
```

en entidades internas de Assembly.

---

# Ejemplo 24 — AssemblyRule no Puede Anular Invariante

Regla inválida:

```text
AllowStartFromDraft = true
```

No puede utilizarse para permitir:

```text
Draft -> InProgress
```

porque contradice la State Machine.

Debe mantenerse:

```text
Fundamental Invariants
    >
Configurable AssemblyRules
```

---

# Ejemplo 25 — Inicio Válido

## Estado Inicial

```text
AssemblyStatus:
Convoked

ScheduledStartAt:
2026-08-21T18:30:00-04:00

AssemblyModality:
InPerson

AssemblyLocation:
Sede Vecinal Principal

ConvokedAt:
2026-08-10T12:00:00-04:00

Version:
5
```

Actor posee:

```text
Assembly.Start
```

---

# Command

```text
StartAssembly

CommandId:
CMD-005

AssemblyId:
ASM-001

ActorId:
ACT-001

StartedAt:
2026-08-21T18:37:00-04:00

ExpectedVersion:
5
```

---

# Guards

Debe cumplirse:

```text
CurrentStatus = Convoked

ScheduleValid = true

ConvocationValid = true

ModalityValid = true

LocationValid = true

ExecutionConditionsSatisfied = true
```

---

# Transición

```text
Convoked
    │
    ▼
InProgress
```

---

# Estado Resultante

```text
AssemblyStatus:
InProgress

StartedAt:
2026-08-21T18:37:00-04:00

Version:
6
```

---

# Domain Event

```text
AssemblyStarted

EventId:
EVT-006

AssemblyId:
ASM-001

AggregateVersion:
6

StartedAt:
2026-08-21T18:37:00-04:00
```

---

# Ejemplo 26 — Inicio Real Diferente del Programado

La Assembly estaba programada para:

```text
ScheduledStartAt:
18:30
```

Comenzó realmente a:

```text
StartedAt:
18:37
```

Esto es válido.

Debe mantenerse la diferencia semántica:

```text
ScheduledStartAt
=
planned time
```

```text
StartedAt
=
actual start time
```

---

# Ejemplo 27 — Inicio no Automático

A las:

```text
18:30
```

el reloj alcanza ScheduledStartAt.

Esto no produce automáticamente:

```text
AssemblyStarted
```

ni cambia:

```text
Convoked -> InProgress
```

Debe existir comportamiento explícito:

```text
StartAssembly
```

---

# Ejemplo 28 — Inicio desde Scheduled

## Estado

```text
AssemblyStatus:
Scheduled
```

Actor posee:

```text
Assembly.Start
```

---

# Resultado

Debe rechazarse.

Falta la transición:

```text
Scheduled -> Convoked
```

---

# Estado Posterior

```text
AssemblyStatus:
Scheduled

Version:
unchanged
```

No existe:

```text
AssemblyStarted
```

---

# Ejemplo 29 — Inicio sin ExecutionConditions

## Estado

```text
AssemblyStatus:
Convoked
```

Pero:

```text
ExecutionConditionsSatisfied:
false
```

---

# Command

```text
StartAssembly
```

---

# Resultado

Rechazado.

Aunque:

```text
State = Convoked
```

y:

```text
Permission = Assembly.Start
```

exista, las condiciones de realización no están satisfechas.

---

# Ejemplo 30 — Quórum como Condición Externa Validada

Supóngase que las reglas requieren:

```text
QuorumRequired = true
```

El cálculo del quórum puede depender de:

```text
Membership

Participation
```

que son Aggregates independientes.

Assembly no debe cargar estos Aggregates internamente.

Puede recibir conceptualmente una decisión:

```text
QuorumDecision:
Satisfied
```

producida por coordinación externa.

---

# Flujo Conceptual

```text
Membership / Participation Data
        │
        ▼
Application / Domain Policy
        │
        ▼
QuorumDecision
        │
        ▼
StartAssembly
        │
        ▼
Assembly
```

El límite de Assembly permanece intacto.

---

# Ejemplo 31 — Finalización Válida

## Estado

```text
AssemblyStatus:
InProgress

StartedAt:
2026-08-21T18:37:00-04:00

Version:
6
```

Actor posee:

```text
Assembly.Complete
```

---

# Command

```text
CompleteAssembly

CommandId:
CMD-006

CompletedAt:
2026-08-21T20:14:00-04:00

ExpectedVersion:
6
```

---

# Validaciones

Debe cumplirse:

```text
CurrentStatus = InProgress

StartedAt != null

CompletedAt >= StartedAt
```

---

# Transición

```text
InProgress
    │
    ▼
Completed
```

---

# Estado Resultante

```text
AssemblyStatus:
Completed

StartedAt:
2026-08-21T18:37:00-04:00

CompletedAt:
2026-08-21T20:14:00-04:00

Version:
7
```

---

# Domain Event

```text
AssemblyCompleted

AggregateVersion:
7
```

---

# Ejemplo 32 — Completion no Archiva

Después de:

```text
AssemblyCompleted
```

el estado es:

```text
Completed
```

No:

```text
Archived
```

El archivado requiere una operación posterior.

---

# Ejemplo 33 — Finalización desde Convoked

## Estado

```text
AssemblyStatus:
Convoked
```

---

# Command

```text
CompleteAssembly
```

---

# Resultado

Rechazado.

No existe transición:

```text
Convoked -> Completed
```

Debe ocurrir primero:

```text
Convoked -> InProgress
```

---

# Ejemplo 34 — CompletedAt Inválido

## Estado

```text
StartedAt:
20:00
```

Command:

```text
CompletedAt:
19:30
```

---

# Resultado

Debe rechazarse porque:

```text
CompletedAt < StartedAt
```

viola la consistencia temporal.

---

# Ejemplo 35 — Finalización no Automática

Aunque:

```text
CurrentTime > ScheduledEndAt
```

Assembly no cambia automáticamente a:

```text
Completed
```

Debe existir:

```text
CompleteAssembly
```

---

# Ejemplo 36 — Cancelación desde Draft

## Estado

```text
AssemblyStatus:
Draft
```

Actor posee:

```text
Assembly.Cancel
```

---

# Command

```text
CancelAssembly

CancelledAt:
2026-08-05T12:00:00-04:00

CancellationReason:
La reunión dejó de ser necesaria
```

---

# Transición

```text
Draft
    │
    ▼
Cancelled
```

---

# Domain Event

```text
AssemblyCancelled
```

---

# Ejemplo 37 — Cancelación desde Scheduled

## Estado

```text
AssemblyStatus:
Scheduled

ScheduledStartAt:
2026-08-21T18:30:00-04:00
```

---

# Cancelación

Después de:

```text
CancelAssembly
```

el estado es:

```text
Cancelled
```

pero ScheduledStartAt permanece como información histórica.

---

# Regla Demostrada

Debe mantenerse:

```text
Cancellation
    ≠
History Deletion
```

---

# Ejemplo 38 — Cancelación desde Convoked

## Estado Inicial

```text
AssemblyStatus:
Convoked

ConvokedAt:
2026-08-10T12:00:00-04:00
```

---

# Resultado

Puede pasar:

```text
Convoked
    │
    ▼
Cancelled
```

---

# Historia Conservada

Debe preservarse:

```text
ConvokedAt
```

porque la convocatoria ocurrió realmente.

---

# Ejemplo 39 — Cancelación desde InProgress

## Estado

```text
AssemblyStatus:
InProgress
```

---

# Command

```text
CancelAssembly
```

---

# Resultado

En versión 1.0 debe ser rechazado.

No existe:

```text
InProgress -> Cancelled
```

---

# Explicación Conceptual

Una reunión ya iniciada y posteriormente interrumpida posee una
semántica distinta de una reunión cancelada antes del inicio.

Un futuro modelo podría introducir:

```text
Interrupted

Aborted

Suspended
```

pero esos estados no pertenecen a la versión 1.0.

---

# Ejemplo 40 — Archivado de Assembly Completed

## Estado

```text
AssemblyStatus:
Completed

Version:
7
```

Actor posee:

```text
Assembly.Archive
```

---

# Command

```text
ArchiveAssembly

ArchivedAt:
2026-09-01T10:00:00-04:00

ExpectedVersion:
7
```

---

# Transición

```text
Completed
    │
    ▼
Archived
```

---

# Estado Resultante

```text
AssemblyStatus:
Archived

ArchivedAt:
2026-09-01T10:00:00-04:00

Version:
8
```

---

# Domain Event

```text
AssemblyArchived

AggregateVersion:
8
```

---

# Ejemplo 41 — Archivado de Assembly Cancelled

También es válido:

```text
Cancelled
    │
    ▼
Archived
```

si se cumplen las reglas correspondientes.

---

# Ejemplo 42 — Archivado desde Scheduled

## Estado

```text
AssemblyStatus:
Scheduled
```

Actor posee:

```text
Assembly.Archive
```

---

# Resultado

Debe rechazarse.

Permission no crea una transición inexistente.

---

# Ejemplo 43 — Archived no es Deleted

Después de ArchiveAssembly:

```text
AssemblyStatus:
Archived
```

La Assembly continúa poseyendo:

```text
AssemblyId

OrganizationId

Version

CreatedAt

historical timestamps

historical Domain Events
```

Debe mantenerse:

```text
Archived
    ≠
Physical Deletion
```

---

# Ejemplo 44 — Modificación de Assembly Archived

## Estado

```text
AssemblyStatus:
Archived
```

Actor posee:

```text
Assembly.Rename
```

---

# Command

```text
RenameAssembly
```

---

# Resultado

Debe rechazarse.

Archived es inmutable.

---

# Regla Demostrada

Debe mantenerse:

```text
Permission Granted
AND
Archived
=
Operation Rejected
```

---

# Ejemplo 45 — Concurrencia Optimista

## Estado Persistido Inicial

```text
AssemblyId:
ASM-001

Version:
10

AssemblyStatus:
Scheduled
```

Dos procesos cargan la misma versión.

---

# Proceso A

Carga:

```text
Version = 10
```

Ejecuta:

```text
RescheduleAssembly
```

Persistencia:

```text
ExpectedVersion = 10
```

Resultado:

```text
Version = 11
```

Persistencia exitosa.

---

# Proceso B

También había cargado:

```text
Version = 10
```

Ejecuta:

```text
RenameAssembly
```

e intenta persistir con:

```text
ExpectedVersion = 10
```

Pero ahora:

```text
PersistedVersion = 11
```

---

# Resultado

```text
AssemblyConcurrencyConflict
```

No debe sobrescribirse Version 11.

---

# Regla Demostrada

Debe mantenerse:

```text
ExpectedVersion
=
PersistedVersion
```

para aceptar una modificación.

---

# Ejemplo 46 — Reintento después de Concurrency Conflict

Después del conflicto no debe hacerse:

```text
ExpectedVersion = 11
```

y repetir automáticamente la escritura sin reevaluar.

Debe ocurrir:

```text
reload Assembly
    │
    ▼
reevaluate Authorization
    │
    ▼
reevaluate State
    │
    ▼
reevaluate Guards
    │
    ▼
reevaluate Invariants
    │
    ▼
decide whether intent is still valid
```

---

# Ejemplo 47 — Repository get_by_id

Request:

```text
get_by_id(
    ASM-001
)
```

Resultado:

```text
Assembly
```

con:

```text
AssemblyId:
ASM-001

OrganizationId:
ORG-001

AssemblyStatus:
Completed

StartedAt:
...

CompletedAt:
...

Version:
12
```

---

# Regla de Rehidratación

La lectura no produce:

```text
AssemblyCreated
```

ni:

```text
AssemblyCompleted
```

como nuevos eventos.

Recuperar un hecho no significa que vuelva a ocurrir.

---

# Ejemplo 48 — Repository Not Found

```text
get_by_id(
    ASM-999
)
```

si no existe la identidad debe producir:

```text
AssemblyNotFound
```

No:

```text
Assembly(
    empty
)
```

---

# Ejemplo 49 — Rehidratación Inválida

Persistencia contiene:

```text
AssemblyStatus:
Completed

StartedAt:
null

CompletedAt:
2026-08-21T20:00:00-04:00
```

Esto contradice las invariantes.

---

# Resultado

Debe producirse conceptualmente:

```text
AssemblyRehydrationFailure
```

El Repository no debe inventar StartedAt.

---

# Ejemplo 50 — Persistencia del Aggregate Completo

Assembly contiene internamente:

```text
AssemblySchedule

Convocation

AssemblyRules

ExecutionConditions
```

El Repository persiste:

```text
Assembly
```

como unidad conceptual.

No expone:

```text
schedule_repository.save()

convocation_repository.save()

assembly_rule_repository.save()
```

como Repositories de Aggregate independientes.

---

# Ejemplo 51 — Persistencia Física en Varias Tablas

Infrastructure puede almacenar:

```text
assemblies

assembly_schedules

assembly_convocations

assembly_rules
```

en tablas diferentes.

DDD continúa considerando:

```text
Assembly
```

como una sola Aggregate Root.

La estructura física no redefine el dominio.

---

# Ejemplo 52 — Persistencia Documental

MongoDB podría almacenar conceptualmente:

```text
{
    assembly,
    schedule,
    convocation,
    rules
}
```

dentro de un documento.

Esto tampoco convierte el modelo MongoDB en definición del
Aggregate.

---

# Ejemplo 53 — Event Sourcing

Una Assembly puede conceptualmente reconstruirse mediante:

```text
AssemblyCreated
    ↓
AssemblyScheduled
    ↓
AssemblyConvoked
    ↓
AssemblyStarted
    ↓
AssemblyCompleted
```

Resultado:

```text
AssemblyStatus:
Completed
```

---

# Regla de Replay

Durante replay no deben producirse nuevamente:

```text
AssemblyCreated

AssemblyScheduled

AssemblyConvoked

AssemblyStarted

AssemblyCompleted
```

como eventos pendientes.

---

# Ejemplo 54 — Snapshot

Un Event Store puede poseer:

```text
Snapshot

AssemblyId:
ASM-001

Version:
100
```

y posteriormente aplicar eventos:

```text
Version 101

Version 102
```

El Snapshot optimiza reconstrucción.

No cambia la identidad ni el modelo conceptual.

---

# Ejemplo 55 — Domain Event e Integration Event

Hecho interno:

```text
AssemblyCompleted
```

puede originar:

```text
AssemblyCompletedIntegrationEvent
```

para otros Bounded Contexts.

Debe mantenerse:

```text
Domain Event
    ≠
Integration Event
```

---

# Ejemplo 56 — Integración FIWARE

Una Assembly completada puede generar:

```text
AssemblyCompleted
```

Luego:

```text
Integration Handler
```

puede traducir el hecho a un contrato de interoperabilidad.

Conceptualmente:

```text
AssemblyCompleted
      │
      ▼
Integration Handler
      │
      ▼
AssemblyCompletedIntegrationEvent
      │
      ▼
FIWARE Adapter
      │
      ▼
NGSI-LD Entity Update
```

Assembly no conoce FIWARE.

---

# Ejemplo 57 — FIWARE no Cambia Estado Directamente

Un sistema externo reporta:

```text
state = completed
```

Esto no debe ejecutar:

```text
assembly.status = Completed
```

Debe existir una traducción conceptual:

```text
External Event
      │
      ▼
Anti-Corruption Layer
      │
      ▼
CompleteAssembly
      │
      ▼
Assembly
```

y todas las reglas vuelven a evaluarse.

---

# Ejemplo 58 — Sistema Externo Solicita Inicio

Un sistema externo emite:

```text
MEETING_OPENED
```

La Anti-Corruption Layer determina si existe equivalencia con:

```text
StartAssembly
```

Si existe, todavía deben verificarse:

```text
Authorization

ExpectedVersion

State Machine

Guards

Invariants
```

No existe acceso directo al estado interno.

---

# Ejemplo 59 — Role y Permission

Una Organization puede definir:

```text
Role:
President
```

y asociarle:

```text
Assembly.Create

Assembly.Schedule

Assembly.Convoke

Assembly.Start
```

Assembly no contiene esta asociación.

---

# Ejemplo 60 — Otra Organization con Roles Diferentes

Otra Organization puede poseer:

```text
Role:
AssemblyCoordinator
```

con:

```text
Assembly.Schedule

Assembly.Convoke

Assembly.Start
```

El Aggregate Assembly no cambia.

---

# Regla Demostrada

Debe mantenerse:

```text
Role
    ≠
Permission
```

y Assembly depende conceptualmente de capacidades, no de nombres
específicos de cargos.

---

# Ejemplo 61 — Cross-Organization Permission

Assembly:

```text
OrganizationId:
ORG-A
```

Actor posee:

```text
Assembly.Start
```

pero únicamente dentro de:

```text
ORG-B
```

---

# Resultado

```text
AuthorizationDenied
```

El mismo nombre de Permission no elimina Organization scope.

---

# Ejemplo 62 — Administrator no Puede Violar Invariantes

Actor:

```text
PlatformAdministrator
```

posee:

```text
Assembly.Archive
```

Assembly está:

```text
InProgress
```

---

# Intento

```text
ArchiveAssembly
```

---

# Resultado

Debe rechazarse.

No existe:

```text
InProgress -> Archived
```

---

# Regla Demostrada

No debe existir:

```text
if superuser:
    bypass domain
```

---

# Ejemplo 63 — Permission Revocado

Actor poseía:

```text
Assembly.Cancel
```

pero la capacidad fue revocada antes de una nueva solicitud.

---

# Command

```text
CancelAssembly
```

---

# Resultado

```text
PermissionDenied
```

No se modifica Assembly.

Un hecho anteriormente realizado con ese Permission sigue siendo
históricamente válido.

---

# Ejemplo 64 — Audit de una Operación Exitosa

Command:

```text
StartAssembly
```

puede quedar relacionado mediante:

```text
CommandId:
CMD-100

ActorId:
ACT-001

AssemblyId:
ASM-001

CorrelationId:
CORR-100
```

Domain Event:

```text
AssemblyStarted

EventId:
EVT-100

CausationId:
CMD-100

CorrelationId:
CORR-100
```

Audit puede reaccionar posteriormente.

---

# Ejemplo 65 — Audit no Pertenece a Assembly

Debe evitarse:

```text
Assembly
    └── AuditEntries[]
```

cuando Audit representa un Aggregate o contexto independiente.

El flujo correcto puede ser:

```text
AssemblyStarted
    │
    ▼
Audit Handler
    │
    ▼
Audit
```

---

# Ejemplo 66 — Document Relacionado

Una Assembly completada puede asociarse con:

```text
DocumentId:
DOC-100
```

por ejemplo un acta.

Assembly no almacena:

```text
DocumentContent
```

como parte de su Aggregate.

Document conserva:

* identidad;
* contenido;
* Lifecycle;
* Repository.

---

# Ejemplo 67 — Proposal Relacionada

Puede existir:

```text
ProposalId:
PROP-001
```

relacionada con:

```text
AssemblyId:
ASM-001
```

Esto no significa:

```text
Assembly
    └── Proposal Aggregate
```

como entidad interna.

---

# Ejemplo 68 — Voting Relacionada

Una Voting puede ocurrir dentro del contexto de una Assembly.

Conceptualmente:

```text
AssemblyId:
ASM-001

VotingId:
VOTE-001
```

Voting mantiene:

```text
VotingStatus

VotingRules

Votes

Results
```

dentro de su propio Aggregate.

---

# Ejemplo 69 — Participation Relacionada

Participation puede utilizar:

```text
AssemblyId
```

como contexto.

Assembly no administra directamente el ciclo de vida de
Participation.

---

# Ejemplo 70 — Membership Relacionada

Una Membership puede ser necesaria para verificar elegibilidad de
un Actor o participante.

Assembly puede recibir referencias o decisiones validadas.

No modifica:

```text
MembershipStatus
```

---

# Ejemplo 71 — Citizen Relacionado

Assembly puede relacionarse conceptualmente mediante:

```text
CitizenId
```

pero no modifica:

```text
CitizenName

CitizenEmail

CitizenStatus
```

---

# Ejemplo 72 — Organization Relacionada

Cada Assembly posee exactamente un:

```text
OrganizationId
```

Ejemplo:

```text
AssemblyId:
ASM-001

OrganizationId:
ORG-001
```

OrganizationId no puede cambiar posteriormente.

---

# Ejemplo 73 — Transferencia de Organization Prohibida

Estado:

```text
Assembly.OrganizationId:
ORG-001
```

Intento:

```text
OrganizationId:
ORG-002
```

como modificación.

---

# Resultado

Debe rechazarse.

La versión 1.0 no define:

```text
TransferAssemblyToOrganization
```

---

# Ejemplo 74 — Territory Opcional

Una Assembly organizacional sin dimensión territorial específica
puede tener:

```text
TerritoryId:
null
```

si el modelo y AssemblyType lo permiten.

---

# Ejemplo 75 — Territory Obligatorio por Regla

Una Assembly:

```text
AssemblyType:
Territorial
```

podría estar sujeta a una regla que requiera:

```text
TerritoryId
```

antes de avanzar a determinados estados.

La obligatoriedad debe derivarse de reglas explícitas.

---

# Ejemplo 76 — Read Model de Calendario

Una proyección puede contener:

```text
AssemblyId

OrganizationId

AssemblyName

AssemblyType

ScheduledStartAt

ScheduledEndAt

AssemblyModality

AssemblyStatus
```

para mostrar un calendario.

Este modelo no es la Aggregate Root.

---

# Ejemplo 77 — Read Model de Próximas Assemblies

El Read Model puede derivar:

```text
Upcoming = true
```

si:

```text
ScheduledStartAt > CurrentTime
```

y el estado corresponde.

`Upcoming` no se convierte en:

```text
AssemblyStatus
```

---

# Ejemplo 78 — Read Model Eventualmente Consistente

Assembly cambia:

```text
Scheduled -> Convoked
```

y produce:

```text
AssemblyConvoked
```

Puede existir brevemente:

```text
Write Model:
Convoked

Read Model:
Scheduled
```

hasta que la proyección procese el evento.

Esto es consistencia eventual del Read Side.

No inconsistencia interna de Assembly.

---

# Ejemplo 79 — Consistencia Fuerte Dentro de Assembly

Nunca debe existir internamente:

```text
AssemblyStatus:
InProgress

StartedAt:
null
```

como estado aceptado.

La consistencia eventual externa no permite inconsistencia
interna.

---

# Ejemplo 80 — Notification Eventualmente Consistente

Después de:

```text
AssemblyConvoked
```

puede pasar un breve período antes de que Notification sea
creada.

Conceptualmente:

```text
Assembly = Convoked

Notification = Pending creation
```

Esto es válido entre Aggregates.

---

# Ejemplo 81 — Fallo de Notification

Si Notification falla después de:

```text
AssemblyConvoked
```

Assembly permanece:

```text
Convoked
```

El Domain Event sigue siendo verdadero.

El error debe resolverse fuera de Assembly.

---

# Ejemplo 82 — Domain Event Duplicado por Transporte

Un consumidor recibe dos veces:

```text
EventId:
EVT-500
```

Debe reconocer que representa el mismo hecho.

No deben crearse dos cambios de Assembly.

---

# Ejemplo 83 — Dos Eventos del Mismo Tipo

Puede existir:

```text
AssemblyDescriptionChanged

EventId:
EVT-501

AggregateVersion:
8
```

y después:

```text
AssemblyDescriptionChanged

EventId:
EVT-502

AggregateVersion:
9
```

Son dos hechos reales distintos.

No una entrega duplicada.

---

# Ejemplo 84 — Eventos Fuera de Orden

Un consumidor recibe primero:

```text
AssemblyStarted

AggregateVersion:
8
```

y luego:

```text
AssemblyConvoked

AggregateVersion:
7
```

AggregateVersion permite detectar el orden correcto.

---

# Ejemplo 85 — Replay de Read Model

Para reconstruir un Read Model pueden reprocesarse:

```text
AssemblyCreated

AssemblyScheduled

AssemblyConvoked

AssemblyStarted

AssemblyCompleted
```

El replay puede reconstruir una proyección.

No debe volver a enviar comunicaciones externas
indiscriminadamente.

---

# Ejemplo 86 — Side Effect Durante Replay

Reprocesar:

```text
AssemblyConvoked
```

para reconstruir un calendario no debe producir nuevamente una
notificación real a los ciudadanos.

Projection y Side Effect deben permanecer diferenciados.

---

# Ejemplo 87 — Transactional Outbox

Durante:

```text
StartAssembly
```

la transacción puede persistir:

```text
Assembly state:
InProgress

Version:
8
```

y:

```text
Outbox Record:
AssemblyStarted
```

conjuntamente.

Después un dispatcher publica el mensaje.

---

# Regla Demostrada

Debe evitarse:

```text
state committed
event permanently lost
```

sin introducir Outbox dentro del dominio.

---

# Ejemplo 88 — Fallo de Persistencia

Assembly ejecuta internamente una operación válida en memoria.

Antes de commit ocurre:

```text
DatabaseUnavailable
```

---

# Resultado

La operación no debe presentarse externamente como confirmada.

No debe publicarse exitosamente:

```text
AssemblyStarted
```

hacia consumidores externos si el nuevo estado no fue confirmado.

---

# Ejemplo 89 — Error de Dominio versus Error de Infraestructura

Caso A:

```text
StartAssembly from Draft
```

Resultado:

```text
InvalidAssemblyTransition
```

Caso B:

```text
StartAssembly valid
but database unavailable
```

Resultado:

```text
AssemblyPersistenceFailure
```

Son categorías diferentes.

---

# Ejemplo 90 — Permission Failure versus Domain Failure

Caso A:

```text
Actor lacks Assembly.Start
```

Resultado:

```text
PermissionDenied
```

Caso B:

```text
Actor has Assembly.Start

AssemblyStatus = Draft
```

Resultado:

```text
InvalidAssemblyTransition
```

Ambos rechazan la operación.

Las causas son diferentes.

---

# Ejemplo 91 — No Domain Event on Permission Failure

Si:

```text
PermissionDenied
```

no debe producirse:

```text
AssemblyStartDenied
```

como Domain Event del Aggregate simplemente por el rechazo.

Puede existir un registro de Security Audit.

---

# Ejemplo 92 — No Domain Event on Invariant Failure

Command:

```text
CompleteAssembly
```

con:

```text
CompletedAt < StartedAt
```

Resultado:

```text
Invalid temporal invariant
```

No se produce:

```text
AssemblyCompleted
```

---

# Ejemplo 93 — Version no Cambia en Rechazo

Antes:

```text
Version = 10
```

Command inválido.

Después:

```text
Version = 10
```

Debe mantenerse:

```text
Rejected Operation
    =>
Version Unchanged
```

---

# Ejemplo 94 — Version Cambia en Modificación Válida

Antes:

```text
Version = 10
```

Rename válido.

Después:

```text
Version = 11
```

Evento:

```text
AssemblyRenamed

AggregateVersion:
11
```

---

# Ejemplo 95 — Lectura no Cambia Version

```text
get_by_id()
```

antes:

```text
Version = 11
```

después:

```text
Version = 11
```

No existe Domain Event.

---

# Ejemplo 96 — Consulta no es Command

Solicitud:

```text
GetAssemblyDetails
```

no representa intención de modificación.

No produce:

* Version increment;
* Domain Event;
* transición de estado.

---

# Ejemplo 97 — Read Model no Modifica Aggregate

Una vista muestra:

```text
status:
Upcoming
```

como valor derivado.

No debe ejecutar:

```text
AssemblyStatus = Upcoming
```

---

# Ejemplo 98 — No Absorción por Conveniencia

Una implementación necesita mostrar:

* Assembly;
* Proposal;
* Voting;
* Documents.

No debe transformar el Aggregate en:

```text
Assembly
    ├── Proposals[]
    ├── Votings[]
    └── Documents[]
```

si estos conceptos continúan siendo Aggregates independientes.

Puede construirse un Read Model compuesto.

---

# Ejemplo 99 — Read Model Compuesto

Una vista puede presentar:

```text
AssemblySummary

AssemblyId

AssemblyName

AssemblyStatus

ProposalCount

VotingCount

DocumentCount
```

Estos counts pueden provenir de proyecciones.

No forman parte necesariamente del estado transaccional de
Assembly.

---

# Ejemplo 100 — Dashboard Organizacional

Un dashboard puede mostrar:

```text
UpcomingAssemblies

CompletedAssemblies

CancelledAssemblies

AssembliesByTerritory
```

Estas consultas pertenecen al Read Side.

No deben incorporarse como métodos de modificación del Aggregate.

---

# Ejemplo 101 — Repository no es Query Engine

No debe añadirse al Repository de dominio:

```text
search_assemblies(
    text,
    page,
    sort,
    filters
)
```

únicamente para satisfacer una pantalla.

Debe utilizarse el Read Model correspondiente.

---

# Ejemplo 102 — Cache Obsoleta

Cache contiene:

```text
Assembly Version = 15
```

Persistencia oficial contiene:

```text
Version = 16
```

Un proceso modifica la versión en caché.

Al persistir:

```text
ExpectedVersion = 15

PersistedVersion = 16
```

debe ocurrir:

```text
AssemblyConcurrencyConflict
```

---

# Ejemplo 103 — Cache no Anula Versioning

No debe utilizarse:

```text
force save cached Assembly
```

ignorando la Version oficial.

La optimización no puede romper concurrencia.

---

# Ejemplo 104 — Actor Humano

Actor:

```text
ActorId:
CIT-001
```

puede iniciar una operación si la Authorization Layer determina
que posee el Permission requerido.

Assembly no necesita conocer el perfil completo del Citizen.

---

# Ejemplo 105 — System Actor

Proceso automático:

```text
SystemActorId:
SYS-ARCHIVER
```

puede intentar ArchiveAssembly si:

* existe identidad autorizable;
* posee Assembly.Archive;
* AssemblyStatus permite archivado;
* ExpectedVersion es válida.

No es omnipotente por ser System Actor.

---

# Ejemplo 106 — Service Account

Una integración técnica utiliza:

```text
ServiceAccountActorId:
SVC-FIWARE-01
```

y solicita una operación.

La credencial técnica se valida fuera del Aggregate.

Assembly recibe únicamente la intención autorizada.

---

# Ejemplo 107 — JWT no Pertenece a Assembly

Request contiene:

```text
Authorization:
Bearer <JWT>
```

La capa de seguridad obtiene:

```text
ActorId

OrganizationId

Permissions
```

Después ejecuta el Command.

Assembly nunca almacena el JWT.

---

# Ejemplo 108 — OAuth Scope Traducido

Scope externo:

```text
assembly:start
```

puede traducirse a:

```text
Assembly.Start
```

si existe una política explícita.

Assembly conoce la capacidad semántica.

No el mecanismo OAuth.

---

# Ejemplo 109 — PEP Proxy

Un PEP Proxy puede autorizar técnicamente el acceso a:

```text
POST /assemblies/ASM-001/start
```

Esto no sustituye:

* Permission semantic check;
* Version validation;
* State Machine;
* Guards;
* invariantes.

---

# Ejemplo 110 — API no Define el Dominio

Endpoint:

```text
POST /assemblies/{id}/complete
```

puede mapear a:

```text
CompleteAssembly
```

pero el endpoint no define las reglas del comportamiento.

Las reglas viven en el dominio.

---

# Ejemplo 111 — Cambio de API sin Cambio de Dominio

La interfaz puede evolucionar de:

```text
REST
```

a:

```text
GraphQL
```

manteniendo:

```text
CompleteAssembly
```

y:

```text
AssemblyCompleted
```

sin cambios conceptuales.

---

# Ejemplo 112 — Base de Datos no Define Estado

Una columna:

```text
status VARCHAR
```

no autoriza valores arbitrarios como:

```text
OPEN

CLOSED

WAITING
```

AssemblyStatus continúa limitado a:

```text
Draft

Scheduled

Convoked

InProgress

Completed

Cancelled

Archived
```

---

# Ejemplo 113 — Migración Técnica

Una tabla:

```text
assemblies
```

se divide en:

```text
assemblies

assembly_schedule
```

Esto puede ser un cambio exclusivamente técnico.

No crea un nuevo Aggregate.

---

# Ejemplo 114 — Migración Conceptual

Si en el futuro se incorpora:

```text
Interrupted
```

debe revisarse:

* Aggregate;
* Lifecycle;
* State Machine;
* Commands;
* Events;
* Invariants;
* Permissions;
* Repository;
* Integration Events;
* Read Models;
* Tests.

No basta con agregar un valor a una columna.

---

# Ejemplo 115 — Nueva Modalidad

Una futura modalidad:

```text
Distributed
```

solo puede incorporarse mediante:

```text
DOMAIN-006P-Extension-Points.md
```

y revisión de:

* AssemblyModality;
* invariantes;
* Commands;
* Read Models;
* Integration Events;
* tests.

---

# Ejemplo 116 — Nuevo Tipo de Assembly

Puede incorporarse en el futuro:

```text
PublicHearing
```

si existe significado real dentro del dominio.

No requiere una nueva Aggregate Root si continúa representando la
misma naturaleza fundamental de Assembly.

---

# Ejemplo 117 — Concepto que Sí Requiere Otro Aggregate

Supóngase que aparece un proceso con:

* identidad propia;
* Lifecycle propio;
* invariantes propias;
* Repository propio;
* comportamiento independiente.

No debe incorporarse automáticamente como entidad interna de
Assembly.

Debe evaluarse si constituye un Aggregate independiente.

---

# Ejemplo 118 — Proposal como Aggregate Independiente

Aunque Proposal ocurra durante una Assembly:

```text
Assembly
    │
    ▼
Proposal
```

no significa:

```text
Assembly
    └── Proposal as internal entity
```

Proposal conserva su propio Aggregate Boundary.

---

# Ejemplo 119 — Voting como Aggregate Independiente

Aunque una votación sea iniciada durante una Assembly, Voting
puede continuar poseyendo:

* apertura;
* cierre;
* reglas;
* votos;
* resultados;
* auditoría;

independientemente del estado interno de Assembly.

---

# Ejemplo 120 — Completion de Assembly no Cierra Voting Automáticamente

Si Assembly alcanza:

```text
Completed
```

no debe ejecutar directamente:

```text
Voting.close()
```

Puede emitir:

```text
AssemblyCompleted
```

y una política externa decidir qué procesos posteriores deben
ocurrir.

---

# Ejemplo 121 — Cancelación y Voting

Si Assembly es cancelada antes del inicio, una Voting relacionada
puede requerir una reacción.

La coordinación se realiza mediante eventos o políticas.

Assembly no modifica Voting directamente.

---

# Ejemplo 122 — CorrelationId

Un proceso completo puede utilizar:

```text
CorrelationId:
CORR-500
```

en:

```text
CreateAssembly

AssemblyCreated

ScheduleAssembly

AssemblyScheduled

ConvokeAssembly

AssemblyConvoked
```

para permitir trazabilidad transversal.

CorrelationId no constituye identidad del Aggregate.

---

# Ejemplo 123 — CausationId

Command:

```text
CMD-500
```

produce:

```text
EVT-500
```

El evento puede registrar:

```text
CausationId:
CMD-500
```

Esto permite reconstruir la cadena causal.

---

# Ejemplo 124 — EventId versus AssemblyId

```text
AssemblyId:
ASM-001
```

puede producir múltiples eventos:

```text
EVT-001

EVT-002

EVT-003
```

Debe mantenerse:

```text
EventId
    ≠
AssemblyId
```

---

# Ejemplo 125 — Version versus EventSchemaVersion

Evento:

```text
AssemblyStarted
```

puede tener:

```text
AggregateVersion:
15

EventSchemaVersion:
2
```

AggregateVersion representa la evolución de Assembly.

EventSchemaVersion representa la evolución estructural del
contrato del evento.

---

# Ejemplo 126 — Histórico no se Reescribe

Secuencia:

```text
AssemblyScheduled(T1)

AssemblyRescheduled(T2)
```

No debe transformarse en:

```text
AssemblyScheduled(T2)
```

eliminando el hecho original.

---

# Ejemplo 127 — Cancelación no Borra Convocatoria

Secuencia:

```text
AssemblyScheduled

AssemblyConvoked

AssemblyCancelled
```

La historia oficial continúa siendo:

```text
Scheduled
then
Convoked
then
Cancelled
```

---

# Ejemplo 128 — Archived Conserva Historia

Assembly pasa:

```text
Draft

Scheduled

Convoked

InProgress

Completed

Archived
```

Archived no significa que el historial anterior deje de existir.

---

# Ejemplo 129 — Caso Completo Ordinario

## Creación

```text
CreateAssembly
    │
    ▼
AssemblyCreated

Status:
Draft

Version:
1
```

## Programación

```text
ScheduleAssembly
    │
    ▼
AssemblyScheduled

Status:
Scheduled

Version:
2
```

## Convocatoria

```text
ConvokeAssembly
    │
    ▼
AssemblyConvoked

Status:
Convoked

Version:
3
```

## Inicio

```text
StartAssembly
    │
    ▼
AssemblyStarted

Status:
InProgress

Version:
4
```

## Finalización

```text
CompleteAssembly
    │
    ▼
AssemblyCompleted

Status:
Completed

Version:
5
```

## Archivado

```text
ArchiveAssembly
    │
    ▼
AssemblyArchived

Status:
Archived

Version:
6
```

---

# Ejemplo 130 — Caso Completo Cancelado

```text
CreateAssembly
    │
    ▼
Draft

ScheduleAssembly
    │
    ▼
Scheduled

ConvokeAssembly
    │
    ▼
Convoked

CancelAssembly
    │
    ▼
Cancelled

ArchiveAssembly
    │
    ▼
Archived
```

Debe conservarse:

```text
ScheduledStartAt

ConvokedAt

CancelledAt

ArchivedAt
```

---

# Ejemplo 131 — Caso Cancelado antes de Programación

```text
CreateAssembly
    │
    ▼
Draft

CancelAssembly
    │
    ▼
Cancelled

ArchiveAssembly
    │
    ▼
Archived
```

En este caso puede no existir:

```text
ScheduledStartAt

ConvokedAt
```

porque dichos hechos nunca ocurrieron.

---

# Ejemplo 132 — Caso con Reprogramación

```text
Draft
    │
    ▼
Scheduled(T1)
    │
    ▼
Scheduled(T2)
    │
    ▼
Convoked
    │
    ▼
InProgress
    │
    ▼
Completed
```

Eventos:

```text
AssemblyCreated

AssemblyScheduled

AssemblyRescheduled

AssemblyConvoked

AssemblyStarted

AssemblyCompleted
```

---

# Ejemplo 133 — Caso con Cambio de Modalidad

Estado:

```text
Scheduled

AssemblyModality:
InPerson
```

Cambio válido:

```text
ChangeAssemblyModality

NewModality:
Hybrid
```

si todas las reglas permanecen satisfechas.

Debe producir:

```text
AssemblyModalityChanged
```

---

# Ejemplo 134 — Cambio de Modalidad Incompatible

Estado:

```text
Scheduled
```

Se cambia a:

```text
InPerson
```

pero Location requerida es:

```text
null
```

y las reglas exigen ubicación presencial.

---

# Resultado

Rechazado.

No debe quedar un estado parcial:

```text
AssemblyModality = InPerson

AssemblyLocation = null
```

si dicha combinación viola las invariantes.

---

# Ejemplo 135 — Cambio de Location después de Convocatoria

Assembly está:

```text
Convoked
```

La ubicación cambia.

Si la convocatoria formal depende de la ubicación anterior, la
operación puede requerir:

```text
AssemblyLocationChanged
```

y:

```text
AssemblyConvocationUpdated
```

cuando ambos hechos ocurran realmente.

---

# Ejemplo 136 — Evento Derivado no Debe Inventarse

Si cambiar Location no modifica Convocation, no debe producirse
artificialmente:

```text
AssemblyConvocationUpdated
```

Los Domain Events representan hechos reales.

---

# Ejemplo 137 — Multiple Domain Events en una Operación

Una reprogramación puede producir conceptualmente:

```text
AssemblyRescheduled
```

y, si modifica realmente la convocatoria:

```text
AssemblyConvocationUpdated
```

Debe preservarse el orden causal.

---

# Ejemplo 138 — Inmutabilidad de Domain Event

Después de producir:

```text
AssemblyScheduled

ScheduledStartAt:
T1
```

una reprogramación no modifica ese evento.

Produce:

```text
AssemblyRescheduled

Previous:
T1

New:
T2
```

---

# Ejemplo 139 — Read Model reconstruible

Si un Read Model de calendario se pierde, puede reconstruirse
procesando eventos como:

```text
AssemblyScheduled

AssemblyRescheduled

AssemblyCancelled
```

La proyección es reconstruible.

---

# Ejemplo 140 — Read Model no es Fuente de Verdad Transaccional

Read Model indica:

```text
AssemblyStatus:
Scheduled
```

pero el Write Model ya se encuentra:

```text
Convoked
```

Un Command debe cargar el Aggregate oficial.

No confiar exclusivamente en la proyección obsoleta.

---

# Ejemplo 141 — Command basado en Read Model Obsoleto

UI ve:

```text
Scheduled
```

y permite mostrar botón:

```text
Convoke
```

Mientras otro proceso ya convocó Assembly.

Al ejecutar el Command:

```text
ExpectedVersion
```

o la State Machine detecta el cambio.

La UI no constituye autoridad del dominio.

---

# Ejemplo 142 — Doble Start

Dos Actors intentan iniciar simultáneamente.

Ambos cargan:

```text
Status:
Convoked

Version:
10
```

Actor A persiste:

```text
InProgress

Version:
11
```

Actor B intenta persistir:

```text
ExpectedVersion:
10
```

Resultado:

```text
AssemblyConcurrencyConflict
```

Solo un inicio se confirma.

---

# Ejemplo 143 — Segundo Start después de Reload

Actor B recarga y encuentra:

```text
Status:
InProgress
```

Si vuelve a intentar:

```text
StartAssembly
```

la State Machine lo rechaza.

---

# Ejemplo 144 — Doble Completion

El mismo patrón protege:

```text
CompleteAssembly
```

contra doble ejecución concurrente.

---

# Ejemplo 145 — Idempotencia de Command

Una infraestructura puede detectar repetición de:

```text
CommandId:
CMD-900
```

y evitar procesarlo dos veces.

Esta idempotencia ocurre fuera del significado de AssemblyId.

---

# Ejemplo 146 — CommandId no es Aggregate Identity

Debe mantenerse:

```text
CommandId
    ≠
AssemblyId
```

Una misma Assembly recibe múltiples Commands durante su vida.

---

# Ejemplo 147 — Event Delivery at Least Once

Un broker puede entregar:

```text
EVT-1000
```

dos veces.

El consumidor utiliza EventId para reconocer el duplicado.

No se crean dos hechos.

---

# Ejemplo 148 — Seguridad de Datos

Domain Event:

```text
AssemblyStarted
```

puede incluir:

```text
AssemblyId

OrganizationId

StartedAt
```

No debe incluir:

```text
JWT

Password

PrivateKey

OAuthToken
```

---

# Ejemplo 149 — Minimización de Datos

Si un evento solo requiere:

```text
ActorId
```

para trazabilidad, no debe copiar:

```text
FullCitizenProfile
```

---

# Ejemplo 150 — Independence Tecnológica

El mismo comportamiento:

```text
StartAssembly
```

debe mantener idéntica semántica si Infrastructure utiliza:

```text
PostgreSQL
```

o:

```text
MongoDB
```

o:

```text
Event Store
```

---

# Ejemplo 151 — Cambio de Framework

Assembly puede implementarse inicialmente con:

```text
FastAPI
```

y posteriormente con otro framework.

Las reglas:

```text
Convoked -> InProgress
```

y:

```text
Assembly.Start
```

no cambian por esa decisión.

---

# Ejemplo 152 — Cambio de Broker

La infraestructura puede cambiar:

```text
RabbitMQ
```

por:

```text
Kafka
```

sin alterar:

```text
AssemblyStarted
```

como Domain Event conceptual.

---

# Ejemplo 153 — Domain Event no es Kafka Message

Debe mantenerse:

```text
AssemblyStarted
```

como hecho del dominio.

Su representación eventual como mensaje Kafka es una decisión de
Infrastructure.

---

# Ejemplo 154 — Integration Event no es Aggregate State

```text
AssemblyCompletedIntegrationEvent
```

puede transportarse externamente.

No se almacena necesariamente dentro del estado de Assembly.

---

# Ejemplo 155 — Caso Comunitario

Assembly:

```text
AssemblyId:
ASM-COM-001

AssemblyType:
Community

OrganizationId:
ORG-COM-001

TerritoryId:
TERR-BARRIO-01

AssemblyName:
Asamblea Comunitaria de Seguridad

AssemblyPurpose:
Analizar medidas comunitarias de prevención

AssemblyModality:
InPerson
```

El Aggregate representa la reunión formal.

Las propuestas de seguridad surgidas durante la reunión
pertenecerán al Aggregate Proposal.

---

# Ejemplo 156 — Caso de Directorio

```text
AssemblyType:
Board

AssemblyName:
Sesión Ordinaria de Directorio
```

La misma Aggregate Root puede representar este tipo de reunión si
las reglas aplicables lo permiten.

No se requiere crear otro Aggregate simplemente por cambiar la
clasificación.

---

# Ejemplo 157 — Caso Territorial

```text
AssemblyType:
Territorial

TerritoryId:
TERR-UV-10

AssemblyPurpose:
Coordinar prioridades de inversión territorial
```

Territory contextualiza la reunión.

Assembly no administra límites ni geometría territorial.

---

# Ejemplo 158 — Caso de Consulta

```text
AssemblyType:
Consultation

AssemblyPurpose:
Recoger opiniones de la comunidad sobre intervención urbana
```

Participation puede modelar las intervenciones ciudadanas.

Assembly mantiene el contexto formal.

---

# Ejemplo 159 — Caso Remoto

```text
AssemblyType:
Organizational

AssemblyModality:
Remote

AssemblyLocation:
null
```

Puede ser válido si las reglas no requieren Location física.

La infraestructura de videoconferencia permanece externa.

---

# Ejemplo 160 — Caso Híbrido

```text
AssemblyModality:
Hybrid

AssemblyLocation:
Centro Cultural Comunitario
```

Puede relacionarse externamente con servicios digitales.

Estos servicios no forman parte del Aggregate.

---

# Ejemplo 161 — Ejemplo de Límite Correcto

```text
Assembly
    ├── AssemblyId
    ├── OrganizationId
    ├── TerritoryId
    ├── AssemblyName
    ├── AssemblyType
    ├── Schedule
    ├── Modality
    ├── Location
    ├── Convocation
    ├── AssemblyRules
    ├── ExecutionConditions
    ├── Status
    └── Version
```

Los conceptos internos existen para proteger la consistencia de la
reunión.

---

# Ejemplo 162 — Límite Incorrecto

No debe modelarse:

```text
Assembly
    ├── Organization
    ├── Citizens[]
    ├── Memberships[]
    ├── Roles[]
    ├── Proposals[]
    ├── Participations[]
    ├── Votings[]
    ├── Documents[]
    ├── Notifications[]
    └── Audits[]
```

como un único Aggregate.

Este diseño destruiría:

* autonomía;
* límites de consistencia;
* escalabilidad;
* bajo acoplamiento;
* independencia entre procesos.

---

# Ejemplo 163 — Coordinación Correcta entre Aggregates

Debe preferirse:

```text
Assembly
    │
    ▼
AssemblyCompleted
    │
    ├────────► Proposal Policy
    ├────────► Voting Policy
    ├────────► Document Process
    ├────────► Notification Process
    └────────► Audit Process
```

Cada proceso conserva su propio límite.

---

# Ejemplo 164 — Consistencia Eventual

Después de AssemblyCompleted:

```text
Assembly:
Completed
```

puede ocurrir temporalmente:

```text
Document:
not yet generated
```

o:

```text
Notification:
not yet sent
```

Esto no invalida la Assembly.

---

# Ejemplo 165 — Saga Futura

Si un proceso futuro requiere coordinar:

```text
Assembly

Voting

Document

Notification
```

puede utilizarse un:

```text
Process Manager
```

o:

```text
Saga
```

sin incorporar todos los Aggregates dentro de Assembly.

---

# Ejemplo 166 — Rechazo sin Modificación Parcial

Command intenta:

```text
ChangeAssemblyModality
```

y simultáneamente necesita una nueva Location.

La nueva combinación resulta inválida.

Debe ocurrir:

```text
Operation Rejected
```

y mantenerse tanto la modalidad como la ubicación anteriores.

---

# Ejemplo 167 — Atomicidad de Inicio

No debe producirse:

```text
Status:
InProgress

StartedAt:
null
```

ni:

```text
Status:
Convoked

StartedAt:
set
```

después de un inicio aceptado.

La transición modifica el conjunto coherentemente.

---

# Ejemplo 168 — Atomicidad de Completion

Debe confirmarse conjuntamente:

```text
Status:
Completed

CompletedAt:
T

Version:
N+1
```

o ninguno.

---

# Ejemplo 169 — Atomicidad de Archivado

Debe confirmarse:

```text
Status:
Archived

ArchivedAt:
T

Version:
N+1
```

como estado consistente.

---

# Ejemplo 170 — Fallo de Guard

Actor autorizado intenta StartAssembly.

Estado:

```text
Convoked
```

pero:

```text
ExecutionConditionsSatisfied:
false
```

Resultado:

```text
Guard Failed
```

No:

```text
PermissionDenied
```

La causa del rechazo debe mantenerse conceptualmente correcta.

---

# Ejemplo 171 — Fallo de State Machine

Actor autorizado intenta CompleteAssembly desde:

```text
Scheduled
```

La causa principal es:

```text
InvalidAssemblyTransition
```

No debe presentarse como error de Repository.

---

# Ejemplo 172 — Fallo de Repository

Todos los Guards e invariantes se cumplen.

La persistencia falla por indisponibilidad técnica.

La causa es:

```text
AssemblyPersistenceFailure
```

No una violación del dominio.

---

# Ejemplo 173 — Fallo de Concurrencia

Todos los Guards e invariantes eran válidos para la versión
cargada, pero otra modificación se confirmó primero.

Resultado:

```text
AssemblyConcurrencyConflict
```

El Command debe reevaluarse contra la nueva realidad.

---

# Ejemplo 174 — Error Externo no Reescribe Hecho Interno

Assembly fue completada válidamente.

Posteriormente falla FIWARE.

Debe mantenerse:

```text
AssemblyStatus:
Completed
```

El fallo de integración no cambia retroactivamente:

```text
AssemblyCompleted
```

---

# Ejemplo 175 — Retry de Integration Event

Una Outbox puede reintentar:

```text
AssemblyCompletedIntegrationEvent
```

sin volver a ejecutar:

```text
CompleteAssembly
```

---

# Ejemplo 176 — Idempotencia de Integración

El receptor externo puede usar:

```text
IntegrationEventId
```

para evitar procesar dos veces una retransmisión.

Esto no modifica Assembly.Version.

---

# Ejemplo 177 — Extensión Válida

Se agrega un nuevo:

```text
AssemblyType:
PublicHearing
```

sin cambiar la naturaleza fundamental del Aggregate.

Debe actualizarse la documentación relacionada.

---

# Ejemplo 178 — Extensión Inválida

Se intenta agregar como entidad interna:

```text
Voting
```

solo porque ocurre dentro de una Assembly.

Debe rechazarse si Voting conserva identidad y Lifecycle propios.

---

# Ejemplo 179 — Nuevo Estado Requiere Evolución Formal

No debe aparecer espontáneamente:

```text
Paused
```

en código o base de datos.

Debe existir una evolución formal del modelo.

---

# Ejemplo 180 — Nueva Operación Requiere Command y Permission

Si se incorpora algún día:

```text
ReopenAssembly
```

deberán evaluarse al menos:

```text
Command:
ReopenAssembly

Permission:
Assembly.Reopen

Domain Event:
AssemblyReopened

State Machine transition

Invariants

Versioning

Integration impact

Tests
```

No forma parte de la versión 1.0.

---

# Ejemplo de Flujo Integral con Repository

```text
StartAssembly
      │
      ▼
Authorization
      │
      ▼
Assembly.Start granted
      │
      ▼
Repository.get_by_id(ASM-001)
      │
      ▼
Assembly Version 10
Status = Convoked
      │
      ▼
ExpectedVersion = 10
      │
      ▼
State Machine validation
      │
      ▼
Guards validation
      │
      ▼
Invariants validation
      │
      ▼
assembly.start()
      │
      ▼
Status = InProgress
StartedAt = T
Version = 11
      │
      ▼
AssemblyStarted
AggregateVersion = 11
      │
      ▼
Repository.save(
    expected_version = 10
)
      │
      ▼
Persistence Commit
```

---

# Ejemplo de Flujo Integral Rechazado por Permission

```text
StartAssembly
      │
      ▼
Authorization
      │
      ▼
Assembly.Start denied
      │
      ▼
Reject
```

No ocurre:

```text
Repository.save()

Version increment

AssemblyStarted
```

---

# Ejemplo de Flujo Integral Rechazado por Estado

```text
StartAssembly
      │
      ▼
Authorization Granted
      │
      ▼
Repository.get_by_id()
      │
      ▼
Status = Draft
      │
      ▼
State Machine rejects
```

No ocurre modificación.

---

# Ejemplo de Flujo Integral Rechazado por Invariante

```text
CompleteAssembly
      │
      ▼
Authorization Granted
      │
      ▼
Status = InProgress
      │
      ▼
CompletedAt < StartedAt
      │
      ▼
Invariant Violation
      │
      ▼
Reject
```

---

# Ejemplo de Flujo Integral Rechazado por Concurrencia

```text
Command valid
      │
      ▼
Aggregate modified in memory
      │
      ▼
Repository.save(
    ExpectedVersion = 10
)
      │
      ▼
PersistedVersion = 11
      │
      ▼
AssemblyConcurrencyConflict
```

La modificación no se confirma.

---

# Ejemplo de Flujo Integral hacia Integration

```text
CompleteAssembly
      │
      ▼
Assembly
      │
      ▼
AssemblyCompleted
      │
      ▼
Persistence + Outbox
      │
      ▼
Integration Handler
      │
      ▼
AssemblyCompletedIntegrationEvent
      │
      ├────────► FIWARE
      ├────────► Municipal Platform
      └────────► Analytics
```

Assembly no conoce los consumidores.

---

# Ejemplo de Flujo hacia Notification

```text
AssemblyConvoked
      │
      ▼
Notification Policy
      │
      ▼
CreateNotification
      │
      ▼
Notification Aggregate
```

---

# Ejemplo de Flujo hacia Audit

```text
AssemblyStarted
      │
      ▼
Audit Handler
      │
      ▼
Register Audit Fact
      │
      ▼
Audit Aggregate
```

---

# Ejemplo de Flujo hacia Read Model

```text
AssemblyRescheduled
      │
      ▼
Projection Handler
      │
      ▼
AssemblyCalendarReadModel
```

---

# Tabla de Ejemplos de Transición

| Estado inicial | Command            | Resultado                          |
| -------------- | ------------------ | ---------------------------------- |
| Draft          | ScheduleAssembly   | Scheduled                          |
| Draft          | CancelAssembly     | Cancelled                          |
| Scheduled      | ConvokeAssembly    | Convoked                           |
| Scheduled      | RescheduleAssembly | Scheduled                          |
| Scheduled      | CancelAssembly     | Cancelled                          |
| Convoked       | RescheduleAssembly | Convoked cuando reglas lo permitan |
| Convoked       | StartAssembly      | InProgress                         |
| Convoked       | CancelAssembly     | Cancelled                          |
| InProgress     | CompleteAssembly   | Completed                          |
| Completed      | ArchiveAssembly    | Archived                           |
| Cancelled      | ArchiveAssembly    | Archived                           |

---

# Tabla de Transiciones Inválidas

| Estado inicial | Command                          | Resultado        |
| -------------- | -------------------------------- | ---------------- |
| Draft          | StartAssembly                    | Rejected         |
| Draft          | CompleteAssembly                 | Rejected         |
| Draft          | ArchiveAssembly                  | Rejected         |
| Scheduled      | StartAssembly                    | Rejected         |
| Scheduled      | CompleteAssembly                 | Rejected         |
| Convoked       | CompleteAssembly                 | Rejected         |
| InProgress     | ScheduleAssembly                 | Rejected         |
| InProgress     | CancelAssembly                   | Rejected en v1.0 |
| Completed      | StartAssembly                    | Rejected         |
| Completed      | CancelAssembly                   | Rejected         |
| Cancelled      | StartAssembly                    | Rejected         |
| Cancelled      | ScheduleAssembly                 | Rejected         |
| Archived       | cualquier modificación ordinaria | Rejected         |

---

# Tabla Command-Permission-Ejemplo

| Command                           | Permission                         | Ejemplo de estado            |
| --------------------------------- | ---------------------------------- | ---------------------------- |
| CreateAssembly                    | Assembly.Create                    | Aggregate inexistente        |
| ScheduleAssembly                  | Assembly.Schedule                  | Draft                        |
| RescheduleAssembly                | Assembly.Reschedule                | Scheduled                    |
| ConvokeAssembly                   | Assembly.Convoke                   | Scheduled                    |
| RenameAssembly                    | Assembly.Rename                    | Estado modificable           |
| ChangeAssemblyType                | Assembly.ChangeType                | Estado modificable           |
| ChangeAssemblyPurpose             | Assembly.ChangePurpose             | Estado modificable           |
| ChangeAssemblyDescription         | Assembly.ChangeDescription         | Estado modificable           |
| ChangeAssemblyModality            | Assembly.ChangeModality            | Estado modificable           |
| ChangeAssemblyLocation            | Assembly.ChangeLocation            | Estado modificable           |
| UpdateAssemblyConvocation         | Assembly.UpdateConvocation         | Estado permitido             |
| UpdateAssemblyRules               | Assembly.UpdateRules               | Estado permitido             |
| UpdateAssemblyExecutionConditions | Assembly.UpdateExecutionConditions | Estado permitido             |
| StartAssembly                     | Assembly.Start                     | Convoked                     |
| CompleteAssembly                  | Assembly.Complete                  | InProgress                   |
| CancelAssembly                    | Assembly.Cancel                    | Draft / Scheduled / Convoked |
| ArchiveAssembly                   | Assembly.Archive                   | Completed / Cancelled        |

---

# Tabla de Hecho y No Equivalencia

| Concepto           | No equivale a         |
| ------------------ | --------------------- |
| AssemblyCreated    | AssemblyScheduled     |
| AssemblyScheduled  | AssemblyConvoked      |
| AssemblyConvoked   | NotificationDelivered |
| ScheduledStartAt   | StartedAt             |
| ScheduledEndAt     | CompletedAt           |
| Completed          | Archived              |
| Cancelled          | Deleted               |
| TerritoryId        | AssemblyLocation      |
| Role               | Permission            |
| PermissionGranted  | OperationValid        |
| Domain Event       | Integration Event     |
| AssemblyRepository | Read Model            |
| Aggregate          | Persistence Model     |
| Rehydration        | Creation              |

---

# Reglas Demostradas por los Ejemplos

Los ejemplos anteriores confirman las siguientes reglas del
Aggregate:

* Assembly posee una única Aggregate Root;
* AssemblyId es único e inmutable;
* OrganizationId es obligatorio e inmutable;
* una Assembly comienza en Draft;
* una Assembly debe respetar la State Machine;
* los Permissions no anulan las invariantes;
* los Guards no sustituyen las invariantes;
* los estados poseen significado propio;
* Scheduled no equivale a Convoked;
* Convoked no equivale a InProgress;
* Completed no equivale a Archived;
* Cancelled no equivale a Deleted;
* la programación no equivale a ejecución real;
* la convocatoria no equivale a Notification;
* Territory no equivale a Location;
* todo cambio semántico válido incrementa Version;
* una operación rechazada no incrementa Version;
* una operación rechazada no produce Domain Events de éxito;
* la concurrencia se protege mediante ExpectedVersion;
* Repository persiste Assembly como unidad;
* Repository no ejecuta comportamiento de dominio;
* Read Models no modifican Assembly;
* otros Aggregates se referencian mediante identificadores;
* Assembly no absorbe Proposal, Participation, Voting, Document,
  Notification ni Audit;
* las integraciones ocurren fuera del Aggregate;
* los Domain Events preservan historia;
* Archived es terminal e inmutable;
* Infrastructure no define el modelo del dominio.

---

# Uso de estos Ejemplos en Implementación

La implementación futura debe poder mapear cada ejemplo válido a
comportamiento real sin cambiar su significado conceptual.

Por ejemplo:

```text
StartAssembly
```

debe continuar significando:

```text
iniciar formalmente una Assembly previamente Convoked
```

independientemente de si la implementación utiliza:

* Python;
* Java;
* TypeScript;
* PostgreSQL;
* MongoDB;
* Event Store;
* REST;
* GraphQL.

---

# Uso de estos Ejemplos en Tests

Los ejemplos pueden servir como base para:

```text
unit tests

aggregate tests

state machine tests

repository contract tests

authorization tests

integration tests

event tests

event sourcing tests
```

La especificación formal de escenarios de prueba se encuentra en:

```text
DOMAIN-006M-Test-Scenarios.md
```

---

# Uso de estos Ejemplos en Read Models

Los ejemplos de consulta y proyección permiten diseñar Read Models
sin ampliar innecesariamente el Aggregate.

Los Read Models deben permanecer coherentes con:

```text
DOMAIN-006L-Read-Model.md
```

---

# Uso de estos Ejemplos en Integraciones

Los ejemplos de interoperabilidad muestran que todo sistema
externo debe permanecer fuera del Consistency Boundary.

La integración formal se define en:

```text
DOMAIN-006K-Integration-Events.md
```

---

# Uso de estos Ejemplos en Seguridad

Los ejemplos de autorización deben interpretarse conjuntamente
con:

```text
DOMAIN-006F-Permissions.md

DOMAIN-006O-Security-Model.md
```

Authentication, Authorization y Domain Validation continúan siendo
responsabilidades diferentes.

---

# Uso de estos Ejemplos en Persistencia

Los ejemplos de Repository deben interpretarse conforme a:

```text
DOMAIN-006G-Repository-Contract.md

DOMAIN-006I-Versioning.md

DOMAIN-006J-Consistency-Boundary.md
```

La estructura física nunca redefine Assembly.

---

# Ejemplos no Normativos de Tecnología

Cuando este documento menciona:

```text
PostgreSQL

MongoDB

Kafka

FIWARE

NGSI-LD

OAuth

JWT
```

lo hace únicamente para demostrar independencia tecnológica y
límites arquitectónicos.

Estas tecnologías no forman parte del dominio Assembly.

---

# Regla de Coherencia Documental

Todo ejemplo debe permanecer consistente con:

```text
DOMAIN-006-Aggregate.md

DOMAIN-006A-Lifecycle.md

DOMAIN-006B-State-Machine.md

DOMAIN-006C-Commands.md

DOMAIN-006D-Domain-Events.md

DOMAIN-006E-Invariants.md

DOMAIN-006F-Permissions.md

DOMAIN-006G-Repository-Contract.md

DOMAIN-006I-Versioning.md

DOMAIN-006J-Consistency-Boundary.md

DOMAIN-006K-Integration-Events.md

DOMAIN-006L-Read-Model.md
```

Si una evolución futura modifica una regla conceptual, los
ejemplos afectados también deben actualizarse.

---

# Regla de No Invención mediante Ejemplos

Un ejemplo no puede introducir silenciosamente:

* nuevos estados;
* nuevos Commands;
* nuevos Domain Events;
* nuevas invariantes;
* nuevos Permissions;
* nuevas entidades internas;
* nuevos Aggregates;
* nuevas transiciones.

Los ejemplos ilustran el modelo oficial.

No lo modifican por sí mismos.

---

# Evolución de Ejemplos

Cuando Assembly evolucione, deben incorporarse nuevos ejemplos
para cualquier comportamiento relevante añadido.

Una nueva capacidad debe ilustrar como mínimo:

```text
valid case

invalid state case

permission denied case

invariant violation case

version conflict case

domain event result

integration impact when applicable
```

---

# Restricciones

Los ejemplos de Assembly nunca deben:

* modificar AssemblyId;
* modificar OrganizationId;
* permitir estados no oficiales;
* saltar transiciones obligatorias;
* permitir que Permission anule State Machine;
* permitir que Permission anule invariantes;
* permitir que Repository ejecute comportamiento;
* permitir que Read Model modifique Aggregate;
* utilizar Notification como parte interna de Assembly;
* utilizar Proposal como entidad interna;
* utilizar Voting como entidad interna;
* utilizar Document como entidad interna;
* utilizar Audit como entidad interna;
* representar Archived como eliminación física;
* representar Cancelled como interrupción posterior al inicio en
  versión 1.0;
* utilizar infraestructura como fuente de reglas del dominio;
* ignorar Versioning;
* reescribir hechos históricos;
* producir Domain Events después de operaciones rechazadas;
* producir nuevas versiones por simples lecturas;
* introducir nuevos conceptos normativos únicamente mediante un
  ejemplo.

---

# Compatibilidad Arquitectónica

Los ejemplos de Assembly son compatibles con:

* Domain-Driven Design;
* Tactical DDD;
* Aggregate Pattern;
* Repository Pattern;
* Clean Architecture;
* Hexagonal Architecture;
* CQRS;
* Event-Driven Architecture;
* Event Sourcing;
* Optimistic Concurrency;
* Transactional Outbox;
* RBAC;
* ABAC;
* arquitectura distribuida;
* consistencia eventual entre Aggregates;
* consistencia fuerte dentro del Aggregate.

---

# Principios Arquitectónicos

Los ejemplos preservan:

```text
Aggregate
    ≠
Persistence Model
```

```text
Command
    ≠
Domain Event
```

```text
Domain Event
    ≠
Integration Event
```

```text
Role
    ≠
Permission
```

```text
Permission Granted
    ≠
Operation Valid
```

```text
Repository
    ≠
Read Model
```

```text
ScheduledStartAt
    ≠
StartedAt
```

```text
Completed
    ≠
Archived
```

```text
Cancelled
    ≠
Deleted
```

```text
Territory
    ≠
Location
```

Estas separaciones constituyen reglas conceptuales esenciales del
modelo Assembly.

---

# Definición de Éxito

Los ejemplos del Aggregate **Assembly** proporcionan una
representación concreta y coherente de cómo deben aplicarse las
reglas conceptuales definidas por la arquitectura DDD de AURA.

Cada ejemplo demuestra que una operación sobre Assembly debe
considerar conjuntamente:

* identidad;
* Organization scope;
* Permission;
* estado actual;
* State Machine;
* Guards;
* invariantes;
* Version;
* Repository;
* Domain Events;
* Consistency Boundary.

Los casos válidos muestran la evolución controlada de Assembly
desde:

```text
Draft
```

hacia:

```text
Scheduled

Convoked

InProgress

Completed

Archived
```

o mediante el camino alternativo:

```text
Draft / Scheduled / Convoked
    ↓
Cancelled
    ↓
Archived
```

Los casos inválidos demuestran que ninguna autorización, rol,
privilegio administrativo, integración externa, optimización de
persistencia o mecanismo técnico puede evadir las invariantes y la
State Machine del Aggregate.

Los ejemplos preservan la diferencia entre planificación y
ejecución real, entre convocatoria y notificación, entre
finalización y archivado, entre cancelación y eliminación, y entre
las responsabilidades internas de Assembly y las pertenecientes a
otros Aggregates.

Organization, Territory, Membership, Citizen, Role, Proposal,
Participation, Voting, Document, Notification y Audit mantienen
sus propios límites de consistencia y se relacionan con Assembly
mediante identificadores, Domain Events, Integration Events y
coordinación externa.

Repository persiste exclusivamente la Aggregate Root, Read Models
resuelven consultas especializadas, Permissions controlan quién
puede intentar una operación y Assembly conserva la autoridad
final sobre la validez del comportamiento.

De esta forma, **DOMAIN-006H-Examples.md** constituye la referencia
conceptual de ejemplos para interpretar correctamente el
Aggregate Assembly sin introducir decisiones de implementación ni
romper los límites establecidos por Domain-Driven Design dentro de
AURA Core.
