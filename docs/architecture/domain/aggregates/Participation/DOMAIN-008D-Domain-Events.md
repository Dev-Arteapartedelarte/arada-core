# DOMAIN-008D — Participation Domain Events

Versión: 1.1

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
- DOMAIN-008E-Invariants.md
- DOMAIN-008F-Permissions.md
- DOMAIN-008G-Repository-Contract.md
- DOMAIN-008H-Examples.md
- DOMAIN-008I-Versioning.md
- DOMAIN-008J-Consistency-Boundary.md
- DOMAIN-008K-Integration-Events.md
- DOMAIN-008L-Read-Model.md
- DOMAIN-008M-Test-Scenarios.md
- DOMAIN-008N-Performance-Rules.md
- DOMAIN-008O-Security-Model.md
- DOMAIN-008P-Extension-Points.md
- CORE-003-Shared-Kernel.md
- CORE-004-Ubiquitous-Language.md
- CORE-005-Domain-Events.md
- CORE-006-Domain-Invariants.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Definir los Domain Events oficiales generados y registrados por el Aggregate
**Participation** cuando ocurre un hecho relevante dentro de su
límite de consistencia.

Un Domain Event representa un hecho que ya ocurrió.

No representa una intención.

No representa una solicitud.

No representa una operación futura.

No representa directamente un Integration Event.

Los Domain Events permiten registrar de manera explícita la
evolución significativa de una Participation y constituyen el
mecanismo conceptual mediante el cual el Aggregate comunica que
su estado interno ha cambiado válidamente.

---

# Propósito

El modelo de Domain Events permite representar hechos consumados
del Aggregate Participation.

Debe mantenerse:

```text
Command

↓

Participation Aggregate

↓

State Validation

↓

Permission Validation

↓

Invariant Validation

↓

Domain Behavior

↓

State Change

↓

Version Increment

↓

Domain Event
```

El Command expresa intención.

El Aggregate toma la decisión.

El Domain Event representa el resultado ocurrido.

---

# Principios

Todos los Domain Events de Participation deben cumplir los
siguientes principios:

- representan hechos consumados;
- se expresan en tiempo pasado;
- son inmutables;
- poseen identidad propia;
- pertenecen conceptualmente al Aggregate Participation;
- identifican la Participation que produjo el hecho;
- preservan información suficiente para trazabilidad;
- pueden incluir información de correlación y causalidad;
- representan únicamente cambios válidos del dominio;
- se producen después de proteger las Invariants;
- reflejan transiciones o modificaciones realmente ejecutadas;
- no contienen comportamiento mutable;
- no ejecutan Commands;
- no modifican otros Aggregates;
- no contienen lógica de Infrastructure;
- pueden utilizarse para construir Read Models;
- pueden originar Integration Events;
- pueden utilizarse para auditoría;
- son compatibles con reconstrucción cuando la arquitectura lo
  requiera.

---

# Domain Event y Aggregate Root

Los Domain Events de Participation son producidos como consecuencia
del comportamiento ejecutado mediante:

```text
Participation
```

como Aggregate Root.

Debe existir:

```text
Command

↓

Participation Aggregate Root

↓

Domain Behavior

↓

Domain Event
```

No debe existir:

```text
External Component

↓

Direct Participation Mutation

↓

Synthetic Domain Event
```

Un Domain Event debe corresponder a un hecho que haya sido
aceptado por las reglas del Aggregate.

---

# Estructura General

Todo Domain Event debe contener, como mínimo, información
conceptual suficiente para establecer:

```text
EventId

EventType

ParticipationId

OrganizationId

OccurredAt

AggregateVersion

CorrelationId

CausationId
```

Cuando corresponda, puede contener además:

```text
ActorId
```

y los datos específicos necesarios para representar el hecho
ocurrido.

---

# EventId

`EventId` identifica de forma única una instancia de Domain Event.

Debe ser:

- único;
- inmutable;
- independiente de ParticipationId;
- independiente de AggregateVersion;
- utilizable para trazabilidad;
- utilizable para detección de procesamiento duplicado cuando
  corresponda.

Debe mantenerse:

```text
EventId

≠

ParticipationId
```

Dos eventos distintos nunca deben compartir identidad aunque
pertenezcan a la misma Participation.

---

# EventType

`EventType` identifica el tipo conceptual del hecho ocurrido.

Ejemplos:

```text
ParticipationRegistered

ParticipationActivated

ParticipationCompleted

ParticipationWithdrawn

ParticipationInvalidated

ParticipationArchived
```

El tipo debe corresponder a un Domain Event definido oficialmente.

No debe utilizarse un tipo genérico como:

```text
ParticipationChanged
```

para ocultar hechos de dominio que poseen significado propio.

---

# ParticipationId

`ParticipationId` identifica el Aggregate que produjo el Domain
Event.

Debe corresponder exactamente a la identidad del Aggregate.

Un Domain Event de Participation no puede representar
simultáneamente modificaciones sobre múltiples Participation.

---

# OrganizationId

`OrganizationId` identifica el contexto organizacional de la
Participation que produjo el evento.

Debe corresponder al OrganizationId inmutable del Aggregate.

Debe mantenerse:

```text
DomainEvent.OrganizationId

=

Participation.OrganizationId
```

El evento no puede utilizarse para modificar Organization.

---

# ActorId

Cuando el hecho requiera mantener referencia al actor responsable
de la operación, el Domain Event puede incluir:

```text
ActorId
```

ActorId permite apoyar:

- trazabilidad;
- auditoría;
- responsabilidad;
- causalidad;
- análisis posterior.

ActorId no sustituye:

```text
CitizenId

MembershipId
```

ni otras identidades propias del contexto de Participation.

---

# OccurredAt

`OccurredAt` representa el momento en que el hecho de dominio
ocurrió.

Debe representar el hecho consumado.

No debe confundirse con:

```text
Command.Timestamp
```

ni necesariamente con:

```text
PublishedAt
```

de un Integration Event.

Debe mantenerse:

```text
Command Timestamp

↓

Domain Decision

↓

OccurredAt
```

El momento de recepción de una intención y el momento conceptual
del hecho pueden representar responsabilidades diferentes.

---

# AggregateVersion

`AggregateVersion` identifica la versión de Participation resultante
del cambio que produjo el Domain Event.

Conceptualmente:

```text
PreviousVersion = N

↓

Valid Domain Change

↓

CurrentVersion = N + 1

↓

Domain Event

AggregateVersion = N + 1
```

La versión del evento debe corresponder a la versión resultante del
Aggregate.

---

# CorrelationId

`CorrelationId` permite asociar el Domain Event con un flujo lógico
más amplio.

Ejemplo:

```text
Application Process

↓

Command

↓

Participation Domain Event

↓

Integration Event
```

Todos pueden conservar un mismo:

```text
CorrelationId
```

sin compartir identidad.

---

# CausationId

`CausationId` identifica conceptualmente la causa inmediata que
originó el hecho.

Cuando un Domain Event deriva de un Command:

```text
DomainEvent.CausationId

=

Command.CommandId
```

cuando el modelo de causalidad así lo requiera.

La causalidad permite reconstruir relaciones entre intenciones y
hechos sin convertir el Command en parte del Domain Event.

---

# Datos Específicos

Además de los campos comunes, cada Domain Event puede contener los
datos específicos necesarios para describir el hecho.

Debe mantenerse el principio:

```text
Event Payload

=

Minimum Domain Information Required
```

No debe incluirse el Aggregate completo por conveniencia.

---

# Domain Events Oficiales

El Aggregate Participation reconoce los siguientes Domain Events
principales:

```text
ParticipationRegistered

ParticipationActivated

ParticipationCompleted

ParticipationWithdrawn

ParticipationInvalidated

ParticipationArchived

ParticipationTypeChanged

ParticipationContextChanged

ParticipationMetadataUpdated
```

Estos eventos representan los hechos definidos por el modelo
actual del Aggregate.

---

# ParticipationRegistered

## Objetivo

Representar el hecho de que una nueva Participation fue registrada
válidamente.

---

## Hecho representado

```text
Participation Registered
```

La Participation ya existe cuando este evento es producido.

---

## Estado anterior

```text
None
```

---

## Estado resultante

```text
Registered
```

---

## Datos conceptuales

Como mínimo:

```text
EventId

ParticipationId

OrganizationId

ParticipationType

OccurredAt

AggregateVersion

CorrelationId

CausationId
```

Cuando corresponda al contexto pueden existir referencias como:

```text
CitizenId

MembershipId

AssemblyId

ProposalId

TerritoryId

ActorId
```

Estas referencias no incorporan los Aggregates externos dentro del
evento ni dentro de Participation.

---

## Command relacionado

```text
RegisterParticipation
```

---

## Significado

Este evento confirma que:

- la identidad fue aceptada;
- el contexto organizacional fue establecido;
- el tipo de Participation es válido;
- las referencias requeridas fueron aceptadas;
- las Invariants de creación fueron satisfechas;
- la Participation ingresó formalmente al Lifecycle.

---

## Regla

No debe emitirse:

```text
ParticipationRegistered
```

si la creación fue rechazada.

---

# ParticipationActivated

## Objetivo

Representar el hecho de que una Participation registrada comenzó
formalmente su ejecución.

---

## Estado anterior

```text
Registered
```

---

## Estado resultante

```text
Active
```

---

## Datos conceptuales

```text
EventId

ParticipationId

OrganizationId

StartedAt

OccurredAt

ActorId

AggregateVersion

CorrelationId

CausationId
```

---

## Command relacionado

```text
ActivateParticipation
```

---

## Significado

El evento confirma que:

```text
Registered

↓

Active
```

ocurrió válidamente.

Debe existir:

```text
StartedAt
```

como parte del estado resultante.

---

## Regla

No puede emitirse desde:

```text
Active

Completed

Withdrawn

Invalidated

Archived
```

---

# ParticipationCompleted

## Objetivo

Representar el hecho de que una Participation activa finalizó
normalmente.

---

## Estado anterior

```text
Active
```

---

## Estado resultante

```text
Completed
```

---

## Datos conceptuales

```text
EventId

ParticipationId

OrganizationId

StartedAt

CompletedAt

OccurredAt

ActorId

AggregateVersion

CorrelationId

CausationId
```

---

## Command relacionado

```text
CompleteParticipation
```

---

## Significado

El evento representa una finalización normal del proceso
participativo.

Debe mantenerse:

```text
StartedAt <= CompletedAt
```

conforme a las reglas temporales del Aggregate.

---

## Regla

No debe utilizarse este evento para representar:

```text
Withdrawal

Invalidation

Archive
```

Cada uno posee semántica propia.

---

# ParticipationWithdrawn

## Objetivo

Representar el hecho de que una Participation fue retirada antes
de completar normalmente su Lifecycle.

---

## Estados anteriores permitidos

```text
Registered

Active
```

---

## Estado resultante

```text
Withdrawn
```

---

## Datos conceptuales

```text
EventId

ParticipationId

OrganizationId

WithdrawnAt

OccurredAt

ActorId

AggregateVersion

CorrelationId

CausationId
```

Cuando corresponda:

```text
WithdrawalReason
```

---

## Command relacionado

```text
WithdrawParticipation
```

---

## Significado desde Registered

```text
Registered

↓

Withdrawn
```

indica que la Participation fue retirada sin haber comenzado
formalmente.

En este caso:

```text
StartedAt = None
```

cuando nunca existió una activación previa.

---

## Significado desde Active

```text
Active

↓

Withdrawn
```

indica que una Participation ya iniciada fue retirada antes de su
finalización normal.

Debe preservarse:

```text
StartedAt
```

---

## Regla

Withdrawal no significa:

```text
Completion

Invalidation

Deletion

Archive
```

---

# ParticipationInvalidated

## Objetivo

Representar el hecho de que una Participation perdió formalmente
su validez conforme a una regla del dominio.

---

## Estados anteriores permitidos

```text
Registered

Active

Completed
```

---

## Estado resultante

```text
Invalidated
```

---

## Datos conceptuales

```text
EventId

ParticipationId

OrganizationId

InvalidationReason

InvalidatedAt

OccurredAt

ActorId

AggregateVersion

CorrelationId

CausationId
```

---

## Command relacionado

```text
InvalidateParticipation
```

---

## Significado

Invalidation representa una decisión explícita del dominio.

Debe conservar la historia previa de la Participation.

Ejemplo:

```text
Registered

↓

Active

↓

Completed

↓

Invalidated
```

El evento no elimina:

```text
StartedAt

CompletedAt
```

ni los hechos históricos anteriores.

---

## Regla

No debe emitirse desde:

```text
Withdrawn

Invalidated

Archived
```

conforme a la State Machine actual.

---

# ParticipationArchived

## Objetivo

Representar el hecho de que una Participation terminó su vida
operacional y fue archivada lógicamente.

---

## Estados anteriores permitidos

```text
Completed

Withdrawn

Invalidated
```

---

## Estado resultante

```text
Archived
```

---

## Datos conceptuales

```text
EventId

ParticipationId

OrganizationId

ArchivedAt

OccurredAt

ActorId

AggregateVersion

CorrelationId

CausationId
```

---

## Command relacionado

```text
ArchiveParticipation
```

---

## Significado

El evento confirma que el Aggregate ingresó al estado terminal:

```text
Archived
```

Archive no representa eliminación física.

La identidad y la historia permanecen preservadas.

---

## Regla

No puede emitirse directamente desde:

```text
Registered

Active
```

---

# ParticipationTypeChanged

## Objetivo

Representar el hecho de que la clasificación conceptual de una
Participation fue modificada válidamente.

---

## Datos conceptuales

```text
EventId

ParticipationId

OrganizationId

PreviousParticipationType

NewParticipationType

OccurredAt

ActorId

AggregateVersion

CorrelationId

CausationId
```

---

## Command relacionado

```text
ChangeParticipationType
```

---

## Estado

Este evento no representa por sí mismo una transición del
Lifecycle.

Debe mantenerse:

```text
PreviousStatus

=

CurrentStatus
```

antes y después del cambio de tipo.

---

## Significado

El evento permite conocer:

```text
PreviousParticipationType

↓

NewParticipationType
```

sin reconstruir el cambio a partir de un estado genérico.

---

## Regla

No debe emitirse cuando:

```text
PreviousParticipationType

=

NewParticipationType
```

si no existe una modificación real del dominio.

---

# ParticipationContextChanged

## Objetivo

Representar el hecho de que el contexto mutable permitido de una
Participation fue modificado válidamente.

---

## Datos conceptuales

```text
EventId

ParticipationId

OrganizationId

PreviousContext

NewContext

OccurredAt

ActorId

AggregateVersion

CorrelationId

CausationId
```

La información concreta puede representar cambios sobre referencias
como:

```text
TerritoryId

AssemblyId

ProposalId
```

cuando dichas referencias formen parte del contexto mutable
permitido.

---

## Command relacionado

```text
ChangeParticipationContext
```

---

## Regla de Referencias

El evento mantiene identidades.

No contiene Aggregates completos.

Debe mantenerse:

```text
AggregateId Reference
```

y nunca:

```text
Mutable External Aggregate
```

---

## Regla de Identidad

Este evento nunca puede representar modificación de:

```text
ParticipationId

OrganizationId
```

---

# ParticipationMetadataUpdated

## Objetivo

Representar el hecho de que metadata no estructural de una
Participation fue modificada válidamente.

---

## Datos conceptuales

```text
EventId

ParticipationId

OrganizationId

ChangedMetadata

OccurredAt

ActorId

AggregateVersion

CorrelationId

CausationId
```

---

## Command relacionado

```text
UpdateParticipationMetadata
```

---

## Regla

Este evento no puede utilizarse para ocultar cambios estructurales
que poseen semántica propia.

No debe representar indirectamente modificaciones de:

```text
ParticipationId

OrganizationId

ParticipationStatus

ParticipationType

Version

CreatedAt

StartedAt

CompletedAt

WithdrawnAt

InvalidatedAt

ArchivedAt
```

cuando dichos conceptos se encuentran protegidos por
comportamientos específicos.

---

# Eventos Transicionales

Los Domain Events que representan cambios de
`ParticipationStatus` son:

```text
ParticipationRegistered

ParticipationActivated

ParticipationCompleted

ParticipationWithdrawn

ParticipationInvalidated

ParticipationArchived
```

Su relación con el Lifecycle es:

```text
Domain Event                  Origin         Destination

ParticipationRegistered      None           Registered

ParticipationActivated       Registered     Active

ParticipationCompleted       Active         Completed

ParticipationWithdrawn       Registered     Withdrawn

ParticipationWithdrawn       Active         Withdrawn

ParticipationInvalidated     Registered     Invalidated

ParticipationInvalidated     Active         Invalidated

ParticipationInvalidated     Completed      Invalidated

ParticipationArchived        Completed      Archived

ParticipationArchived        Withdrawn      Archived

ParticipationArchived        Invalidated    Archived
```

No deben inferirse transiciones adicionales.

---

# Eventos No Transicionales

Los Domain Events no transicionales representan modificaciones
válidas sin cambiar `ParticipationStatus`.

Incluyen:

```text
ParticipationTypeChanged

ParticipationContextChanged

ParticipationMetadataUpdated
```

Debe mantenerse:

```text
Valid Domain Change

↓

Same ParticipationStatus

↓

Version Increment

↓

Domain Event
```

---

# Matriz Command / Domain Event

```text
Command                      Domain Event

RegisterParticipation        ParticipationRegistered

ActivateParticipation        ParticipationActivated

CompleteParticipation        ParticipationCompleted

WithdrawParticipation        ParticipationWithdrawn

InvalidateParticipation      ParticipationInvalidated

ArchiveParticipation         ParticipationArchived

ChangeParticipationType      ParticipationTypeChanged

ChangeParticipationContext   ParticipationContextChanged

UpdateParticipationMetadata  ParticipationMetadataUpdated
```

La existencia de un Command no garantiza la existencia del evento.

El evento solo existe cuando la intención fue aceptada y ejecutada.

---

# Regla Command / Event

Debe mantenerse:

```text
Command

=

Intent
```

```text
Domain Event

=

Occurred Fact
```

Por lo tanto:

```text
ActivateParticipation

≠

ParticipationActivated
```

hasta que la transición haya sido validada y ejecutada.

---

# Regla de Emisión

Un Domain Event debe registrarse únicamente después de que el
Aggregate determine que la operación es válida.

Conceptualmente:

```text
Command

↓

Permission Validation

↓

State Validation

↓

Invariant Validation

↓

Version Validation

↓

Domain Behavior

↓

State Modification

↓

Version Increment

↓

Domain Event
```

---

# Evento y Estado Resultante

Todo evento transicional debe corresponder exactamente al estado
resultante del Aggregate.

Ejemplo:

```text
ParticipationCompleted
```

requiere:

```text
ParticipationStatus = Completed
```

No puede existir:

```text
ParticipationCompleted

+

ParticipationStatus = Active
```

como resultado confirmado de la misma operación.

---

# Evento y Version

Toda modificación válida incrementa Version.

El Domain Event correspondiente debe representar la versión
resultante.

Ejemplo:

```text
Version = 7

↓

CompleteParticipation

↓

Version = 8

↓

ParticipationCompleted

AggregateVersion = 8
```

---

# Evento y Timestamps

Los eventos que representan cambios del Lifecycle deben mantener
coherencia con los timestamps correspondientes.

Debe existir coherencia conceptual entre:

```text
ParticipationActivated

↓

StartedAt
```

```text
ParticipationCompleted

↓

CompletedAt
```

```text
ParticipationWithdrawn

↓

WithdrawnAt
```

```text
ParticipationInvalidated

↓

InvalidatedAt
```

```text
ParticipationArchived

↓

ArchivedAt
```

---

# Inmutabilidad

Una vez creado, un Domain Event no puede modificarse.

No debe existir:

```text
DomainEvent.setParticipationId()

DomainEvent.setOccurredAt()

DomainEvent.setAggregateVersion()
```

Si un hecho posterior modifica el dominio, debe producirse un nuevo
Domain Event.

---

# Eventos Históricos

Los Domain Events representan hechos históricos.

Un hecho posterior no reescribe un hecho anterior.

Ejemplo:

```text
ParticipationCompleted
```

seguido por:

```text
ParticipationInvalidated
```

no elimina ni modifica:

```text
ParticipationCompleted
```

Ambos hechos forman parte de la historia.

---

# Orden de Eventos

Los eventos de una misma Participation deben mantener un orden
compatible con:

```text
AggregateVersion
```

Ejemplo:

```text
ParticipationRegistered     Version 1

ParticipationActivated      Version 2

ParticipationCompleted      Version 3

ParticipationArchived       Version 4
```

No debe existir para la misma evolución confirmada:

```text
Version 3

↓

Version 2
```

---

# Eventos Concurrentes

Cuando dos Commands compiten sobre la misma Version, solo la
modificación confirmada puede producir el Domain Event de éxito
correspondiente.

Ejemplo:

```text
Participation

Status = Active

Version = 5
```

Command A:

```text
CompleteParticipation
ExpectedVersion = 5
```

Command B:

```text
WithdrawParticipation
ExpectedVersion = 5
```

Si A se confirma:

```text
ParticipationCompleted
AggregateVersion = 6
```

B no puede producir posteriormente:

```text
ParticipationWithdrawn
AggregateVersion = 6
```

sobre la misma versión previa sin reevaluar el nuevo estado.

---

# Eventos Duplicados

Cada instancia de evento posee:

```text
EventId
```

único.

La infraestructura puede utilizar EventId para detectar
procesamiento duplicado.

Sin embargo:

```text
Duplicate Delivery

≠

New Domain Fact
```

El reprocesamiento técnico de un mismo evento no crea un nuevo
hecho del dominio.

---

# Domain Events y Consistencia

Los Domain Events pertenecen conceptualmente al cambio consistente
del Aggregate.

Debe mantenerse:

```text
Aggregate Change

+

Version Increment

+

Domain Event Registration
```

como una unidad lógica.

No debe confirmarse un cambio válido del Aggregate dejando
inconsistente el hecho que lo representa.

---

# Atomicidad Conceptual

Dentro del límite de consistencia de Participation:

```text
Validate

↓

Modify Aggregate

↓

Increment Version

↓

Register Domain Event
```

representa una única modificación lógica.

No debe existir:

```text
State Changed

but

Event Missing
```

cuando el modelo exige el evento correspondiente.

Tampoco:

```text
Event Registered

but

State Change Rejected
```

---

# Commands Rechazados

Un Command rechazado no produce el Domain Event de éxito
correspondiente.

Ejemplo:

```text
Status = Completed

Command = ActivateParticipation
```

Resultado:

```text
Rejected
```

No debe existir:

```text
ParticipationActivated
```

---

# Invariant Violation

Cuando una operación viola una Invariant:

```text
Command

↓

Invariant Violation

↓

Rejected
```

No se modifica:

```text
ParticipationStatus

Version

Lifecycle Timestamps
```

y no se registra el Domain Event de éxito.

---

# Permission Denied

Cuando el actor no posee Permission:

```text
Command

↓

Permission Denied

↓

No Domain Change
```

No debe producirse el evento de éxito correspondiente.

La denegación de autorización y el Domain Event representan
responsabilidades diferentes.

---

# Version Conflict

Cuando:

```text
ExpectedVersion

≠

CurrentVersion
```

la operación no puede confirmarse sobre la versión esperada.

No debe producirse el Domain Event de éxito como si la modificación
hubiese sido aceptada.

---

# Domain Events y Organization

Los eventos de Participation pueden contener:

```text
OrganizationId
```

como contexto.

No modifican Organization.

Debe mantenerse:

```text
Participation Domain Event

≠

Organization Domain Event
```

---

# Domain Events y Citizen

Cuando Participation referencia un Citizen, un Domain Event puede
contener:

```text
CitizenId
```

como identidad contextual.

No contiene:

```text
Citizen Aggregate
```

No modifica Citizen.

---

# Domain Events y Membership

Cuando Participation se encuentra asociada a una Membership, el
evento puede conservar:

```text
MembershipId
```

como referencia.

No puede representar modificaciones del Lifecycle de Membership.

---

# Domain Events y Role

Role puede participar indirectamente en la autorización de un
Command.

El Domain Event resultante no convierte Role en parte de
Participation.

Debe mantenerse:

```text
RoleId Reference when required

≠

Role Aggregate Ownership
```

---

# Domain Events y Territory

Cuando el contexto participativo sea territorial, el evento puede
incluir:

```text
TerritoryId
```

No modifica:

- geometría;
- jerarquía;
- estado;
- clasificación;
- límites territoriales.

Estas responsabilidades corresponden a Territory.

---

# Domain Events y Assembly

Cuando Participation ocurre dentro del contexto de una Assembly,
el evento puede mantener:

```text
AssemblyId
```

como referencia.

No modifica:

- programación de Assembly;
- convocatoria;
- estado;
- modalidad;
- ubicación.

---

# Domain Events y Proposal

Cuando Participation se encuentra relacionada con una Proposal,
puede mantener:

```text
ProposalId
```

como referencia.

El evento de Participation no representa una transición de
Proposal.

Debe mantenerse:

```text
Participation Domain Event

≠

Proposal Domain Event
```

---

# Domain Events y Voting

Participation y Voting conservan límites independientes.

Un Domain Event de Participation no representa:

- apertura de votación;
- emisión de voto;
- cierre de votación;
- resultado de votación.

Debe mantenerse:

```text
Participation Domain Event

≠

Voting Domain Event
```

---

# Domain Events y Document

Un Domain Event de Participation puede originar posteriormente
procesos documentales.

No contiene ni modifica el Aggregate Document.

La coordinación se realiza fuera del Aggregate.

---

# Domain Events y Notification

Un Domain Event puede originar handlers internos de
Notification.

Ejemplo conceptual:

```text
ParticipationActivated

↓

Application / Event Handler

↓

Notification Process
```

Participation no envía directamente la Notification.

---

# Domain Events y Audit

Los Domain Events constituyen una fuente relevante de trazabilidad
para Audit.

Información como:

```text
EventId

EventType

ParticipationId

OrganizationId

ActorId

OccurredAt

AggregateVersion

CorrelationId

CausationId
```

puede ser utilizada por el contexto de Audit.

Audit no forma parte del Aggregate Participation.

---

# Domain Events e Integration

Un Domain Event puede originar un Integration Event cuando el hecho
deba ser comunicado fuera del Bounded Context.

Debe mantenerse:

```text
Participation Domain Event

↓

Integration Mapping

↓

Integration Event
```

No debe publicarse necesariamente el Domain Event interno de forma
directa hacia consumidores externos.

---

# Domain Event e Integration Event

Debe mantenerse la separación:

```text
Domain Event

=

Internal Domain Fact
```

```text
Integration Event

=

External Contract
```

Un Domain Event puede contener conceptos internos que no deban
formar parte del contrato de interoperabilidad.

Los Integration Events se definen en:

```text
DOMAIN-008K-Integration-Events.md
```

---

# Domain Events y Read Models

Los Read Models pueden proyectarse desde Domain Events.

Conceptualmente:

```text
ParticipationRegistered

↓

Projection

↓

ParticipationSummary
```

```text
ParticipationActivated

↓

Projection

↓

ParticipationStatus
```

```text
ParticipationCompleted

↓

Projection

↓

ParticipationHistory
```

Los Read Models no modifican los Domain Events.

---

# Reconstrucción de Read Models

Las proyecciones pueden reconstruirse utilizando la secuencia de
Domain Events disponible cuando la arquitectura lo permita.

Debe mantenerse:

```text
Domain Events

↓

Projection Engine

↓

Read Models
```

La pérdida de un Read Model no modifica la historia del Aggregate.

---

# Domain Events y CQRS

Los Domain Events conectan conceptualmente el lado de escritura con
las proyecciones del lado de lectura.

```text
Write Side

Command

↓

Participation Aggregate

↓

Domain Events

↓

Projection

↓

Read Side
```

Los Read Models no sustituyen la autoridad del Aggregate.

---

# Domain Events y Event Sourcing

El modelo es compatible con Event Sourcing.

En una implementación Event Sourced:

```text
Domain Events

↓

Replay

↓

Participation State
```

Los eventos utilizados para reconstrucción deben representar
hechos históricos válidos.

La compatibilidad con Event Sourcing no obliga por sí sola a que
toda implementación utilice Event Sourcing.

---

# Rehidratación

La aplicación de eventos históricos durante rehidratación no
representa nuevos hechos.

Debe mantenerse:

```text
Historical Event Application

≠

New Domain Event Emission
```

La rehidratación:

- no crea nuevos EventId;
- no incrementa Version adicionalmente;
- no modifica OccurredAt;
- no vuelve a ejecutar Commands;
- no vuelve a publicar hechos como nuevos Domain Events.

---

# Replay

El replay reproduce hechos existentes.

No debe transformar:

```text
ParticipationCompleted
```

histórico en un nuevo:

```text
ParticipationCompleted
```

con nueva identidad.

Debe preservarse la identidad histórica del evento cuando
corresponda.

---

# Domain Events y Event-Driven Architecture

Los Domain Events permiten que componentes internos reaccionen a
hechos sin acoplar el Aggregate a sus consumidores.

Debe mantenerse:

```text
Participation

↓

Domain Event

↓

Independent Reaction
```

Participation no necesita conocer quién consumirá el evento.

---

# Productores

El productor conceptual de los Domain Events definidos en este
documento es:

```text
Participation Aggregate
```

La infraestructura puede encargarse posteriormente de:

- persistencia;
- serialización;
- publicación;
- transporte;
- reintentos;
- distribución.

Estas responsabilidades no cambian la propiedad conceptual del
evento.

---

# Consumidores

Dentro de Participation Management, los Domain Events pueden ser
consumidos por:

- Application Services;
- Projection Handlers;
- Audit;
- Integration Mapping;
- procesos de Notification;
- coordinadores de procesos;
- componentes analíticos internos.

La existencia de consumidores no modifica el Aggregate.

---

# Desacoplamiento

Participation no debe conocer consumidores concretos.

No debe existir dentro del dominio:

```text
Participation

↓

Call Notification Service

↓

Call Audit Service

↓

Call FIWARE
```

Debe existir:

```text
Participation

↓

Domain Event
```

y la reacción ocurre fuera del Aggregate.

---

# Persistencia de Eventos

La forma concreta de persistir Domain Events pertenece a
Infrastructure.

Puede existir:

- Event Store;
- almacenamiento transaccional;
- Outbox;
- almacenamiento relacional;
- almacenamiento documental;
- otro mecanismo compatible.

El dominio no depende de la tecnología seleccionada.

---

# Regla de No Dependencia Tecnológica

Los Domain Events no deben depender de:

```text
PostgreSQL

MongoDB

Redis

Kafka

RabbitMQ

HTTP

REST

GraphQL

FastAPI

Django

FIWARE

NGSI-LD
```

Estos mecanismos pueden transportar o persistir información.

No definen la semántica del evento.

---

# Serialización

La serialización técnica de un Domain Event no forma parte de su
significado de dominio.

Debe mantenerse:

```text
Domain Event

≠

JSON
```

```text
Domain Event

≠

Database Row
```

```text
Domain Event

≠

Kafka Message
```

Estas son representaciones técnicas posibles.

---

# Esquema de Evento

Conceptualmente un Domain Event puede representarse como:

```text
ParticipationDomainEvent

EventId

EventType

ParticipationId

OrganizationId

ActorId

OccurredAt

AggregateVersion

CorrelationId

CausationId

EventSpecificData
```

La representación concreta pertenece a etapas posteriores de
diseño e implementación.

---

# Payload

El payload debe contener únicamente información necesaria para
representar el hecho.

No debe contener por conveniencia:

- el Aggregate completo;
- credenciales;
- tokens;
- JWT;
- secretos;
- sesiones;
- objetos de Infrastructure;
- conexiones;
- clientes externos;
- modelos ORM.

---

# Datos Sensibles

Los Domain Events deben aplicar minimización de datos.

Cuando una referencia mediante identidad sea suficiente debe
preferirse:

```text
CitizenId
```

sobre copiar información completa del Citizen.

Debe evitarse propagar información personal que no sea necesaria
para representar el hecho de Participation.

---

# Seguridad

Los Domain Events no deben contener:

- contraseñas;
- tokens de acceso;
- refresh tokens;
- JWT;
- claves privadas;
- secretos criptográficos;
- credenciales de infraestructura;
- sesiones autenticadas.

El modelo completo se desarrolla en:

```text
DOMAIN-008O-Security-Model.md
```

---

# Integridad

Un Domain Event debe ser coherente con:

- ParticipationId;
- OrganizationId;
- estado resultante;
- AggregateVersion;
- timestamps;
- datos específicos;
- transición realizada.

Un evento inconsistente no debe considerarse representación válida
del hecho.

---

# Trazabilidad

La secuencia de eventos debe permitir observar conceptualmente la
evolución significativa de Participation.

Ejemplo:

```text
ParticipationRegistered

↓

ParticipationActivated

↓

ParticipationCompleted

↓

ParticipationArchived
```

o:

```text
ParticipationRegistered

↓

ParticipationWithdrawn

↓

ParticipationArchived
```

o:

```text
ParticipationRegistered

↓

ParticipationActivated

↓

ParticipationCompleted

↓

ParticipationInvalidated

↓

ParticipationArchived
```

---

# Historia

La historia de eventos no debe confundirse con el estado actual.

Ejemplo:

```text
ParticipationRegistered

ParticipationActivated

ParticipationCompleted

ParticipationInvalidated
```

Estado actual:

```text
Invalidated
```

pero la historia demuestra que anteriormente existieron estados
válidos diferentes.

---

# Estado Actual

El estado actual puede derivarse conceptualmente de la evolución
confirmada.

Sin embargo:

```text
Current State

≠

Complete History
```

Un Read Model que solo exponga:

```text
Status = Invalidated
```

no sustituye la secuencia histórica de hechos.

---

# Event Ordering

Para una misma Participation debe existir una secuencia coherente.

La Version permite establecer orden lógico:

```text
Version 1

↓

Version 2

↓

Version 3
```

Los mecanismos técnicos de transporte pueden entregar mensajes de
forma diferente.

La infraestructura debe preservar o recuperar la semántica de
orden cuando sea necesaria.

---

# Entrega Fuera de Orden

La entrega técnica fuera de orden no modifica el orden lógico de
los hechos.

Debe mantenerse:

```text
Transport Order

≠

Domain Order
```

El orden del dominio se determina mediante información como:

```text
ParticipationId

AggregateVersion

OccurredAt
```

según las reglas establecidas.

---

# Entrega al Menos Una Vez

Una infraestructura puede entregar un mismo evento más de una vez.

Los consumidores deben poder utilizar:

```text
EventId
```

para controlar duplicados cuando corresponda.

La repetición de entrega no modifica el hecho original.

---

# Eventual Consistency

Los Domain Events pueden originar actualizaciones fuera del
Aggregate mediante consistencia eventual.

Ejemplo:

```text
ParticipationCompleted

↓

Commit

↓

Projection Update

↓

Integration Publication
```

Puede existir un retraso entre estas etapas.

Ese retraso no modifica el estado confirmado de Participation.

---

# Consistency Boundary

El Domain Event representa un hecho ocurrido dentro del límite de
consistencia de Participation.

No amplía ese límite.

Debe mantenerse:

```text
Participation Domain Event

↓

External Reaction
```

No:

```text
Participation Transaction

↓

Participation + Assembly + Proposal + Voting
```

La definición formal del límite se encuentra en:

```text
DOMAIN-008J-Consistency-Boundary.md
```

---

# No Distributed Transaction

La reacción de otros Aggregates ante un Domain Event no requiere
que todos sean modificados dentro de la misma transacción.

Debe utilizarse coordinación externa y consistencia eventual cuando
corresponda.

---

# Domain Event y Repository

El Repository persiste Participation conforme a su contrato.

Los eventos producidos por el Aggregate pueden formar parte del
proceso de persistencia según la arquitectura adoptada.

Debe mantenerse:

```text
Participation Aggregate

↓

Repository
```

sin convertir el Repository en productor semántico de Domain
Events.

---

# Regla del Repository

El Repository no debe inventar eventos para representar cambios que
no fueron ejecutados por el Aggregate.

No debe existir:

```text
Repository

↓

Direct Database Update

↓

Synthetic ParticipationCompleted
```

Debe existir:

```text
Participation.complete()

↓

ParticipationCompleted

↓

Repository Persistence
```

o el comportamiento conceptual equivalente.

---

# Domain Events y Versioning

Todo evento asociado a una modificación válida debe respetar el
modelo de Versioning.

La relación conceptual es:

```text
CurrentVersion = N

↓

Valid Modification

↓

Version = N + 1

↓

DomainEvent.AggregateVersion = N + 1
```

La definición formal se encuentra en:

```text
DOMAIN-008I-Versioning.md
```

---

# Domain Events y Permissions

Permissions se evalúan antes de ejecutar el comportamiento que
produce el evento.

Debe mantenerse:

```text
Permission Denied

↓

No Domain Modification

↓

No Success Domain Event
```

La definición formal corresponde a:

```text
DOMAIN-008F-Permissions.md
```

---

# Domain Events e Invariants

Las Invariants deben cumplirse antes y después de toda modificación
válida.

Debe mantenerse:

```text
Invariant Violation

↓

No Valid Domain Change

↓

No Success Domain Event
```

La definición formal corresponde a:

```text
DOMAIN-008E-Invariants.md
```

---

# Domain Events y State Machine

Los eventos transicionales deben corresponder exactamente a las
transiciones oficiales.

Debe mantenerse:

```text
State Machine Transition

↓

Domain Event
```

No puede existir un Domain Event que implique una transición no
reconocida por:

```text
DOMAIN-008B-State-Machine.md
```

---

# Matriz Evento / Estado Resultante

```text
Domain Event                  Resulting State

ParticipationRegistered      Registered

ParticipationActivated       Active

ParticipationCompleted       Completed

ParticipationWithdrawn       Withdrawn

ParticipationInvalidated     Invalidated

ParticipationArchived        Archived
```

Los eventos no transicionales conservan el estado actual.

---

# Matriz Evento / Timestamp

```text
Domain Event                  Lifecycle Timestamp

ParticipationRegistered      CreatedAt

ParticipationActivated       StartedAt

ParticipationCompleted       CompletedAt

ParticipationWithdrawn       WithdrawnAt

ParticipationInvalidated     InvalidatedAt

ParticipationArchived        ArchivedAt
```

Los timestamps deben respetar las Invariants temporales del
Aggregate.

---

# Secuencia Normal

La secuencia normal de Participation puede representarse como:

```text
ParticipationRegistered

↓

ParticipationActivated

↓

ParticipationCompleted

↓

ParticipationArchived
```

---

# Secuencia con Withdrawal antes de Activación

```text
ParticipationRegistered

↓

ParticipationWithdrawn

↓

ParticipationArchived
```

---

# Secuencia con Withdrawal durante Participación

```text
ParticipationRegistered

↓

ParticipationActivated

↓

ParticipationWithdrawn

↓

ParticipationArchived
```

---

# Secuencia con Invalidation previa a Activación

```text
ParticipationRegistered

↓

ParticipationInvalidated

↓

ParticipationArchived
```

---

# Secuencia con Invalidation durante Participación

```text
ParticipationRegistered

↓

ParticipationActivated

↓

ParticipationInvalidated

↓

ParticipationArchived
```

---

# Secuencia con Invalidation posterior a Completion

```text
ParticipationRegistered

↓

ParticipationActivated

↓

ParticipationCompleted

↓

ParticipationInvalidated

↓

ParticipationArchived
```

---

# Secuencias Inválidas

No son válidas secuencias como:

```text
ParticipationRegistered

↓

ParticipationCompleted
```

sin:

```text
ParticipationActivated
```

Tampoco:

```text
ParticipationArchived

↓

ParticipationActivated
```

ni:

```text
ParticipationWithdrawn

↓

ParticipationCompleted
```

ni:

```text
ParticipationInvalidated

↓

ParticipationActivated
```

---

# Eventos No Transicionales dentro del Lifecycle

Los eventos no transicionales pueden aparecer entre hechos del
Lifecycle cuando el estado y las Invariants permitan la
modificación.

Ejemplo conceptual:

```text
ParticipationRegistered

↓

ParticipationTypeChanged

↓

ParticipationActivated
```

La existencia del evento intermedio no altera por sí misma el
estado del Lifecycle.

---

# Múltiples Eventos por Operación

Una operación de dominio puede producir más de un Domain Event
únicamente cuando existan múltiples hechos conceptualmente
diferentes que deban representarse.

No deben generarse eventos redundantes para duplicar la misma
semántica.

El modelo debe preservar:

```text
One Fact

↓

One Explicit Meaning
```

---

# Granularidad

Los Domain Events deben poseer granularidad suficiente para
representar hechos significativos.

No deben ser excesivamente genéricos.

Debe preferirse:

```text
ParticipationActivated
```

sobre:

```text
ParticipationUpdated
```

cuando el hecho real sea una activación.

---

# No Event per Attribute by Default

La existencia de un atributo no obliga a crear un evento
independiente para cada modificación.

Debe existir un hecho de dominio significativo.

Los eventos se definen por lenguaje ubicuo y comportamiento, no por
la estructura de una tabla.

---

# No CRUD Events

No deben utilizarse eventos técnicos como:

```text
ParticipationRowInserted

ParticipationRowUpdated

ParticipationRowDeleted

ParticipationSaved
```

Estos nombres representan persistencia.

No hechos del dominio.

---

# No Generic Changed Event

No debe utilizarse:

```text
ParticipationChanged
```

como sustituto universal de hechos explícitos.

Esto eliminaría semántica del dominio y dificultaría:

- auditoría;
- proyecciones;
- integración;
- análisis;
- evolución.

---

# No Event for Rejected Command

No deben existir eventos de éxito para Commands rechazados.

Ejemplo:

```text
CompleteParticipation

↓

Rejected
```

no produce:

```text
ParticipationCompleted
```

La observabilidad de rechazos puede resolverse fuera de la
semántica de éxito del Aggregate cuando corresponda.

---

# No Event for Read

Consultar una Participation no produce Domain Events.

Debe mantenerse:

```text
Query

↓

Read

↓

No Domain Mutation

↓

No Domain Event
```

---

# No Event for Rehydration

Rehidratar Participation no produce nuevos Domain Events.

Debe mantenerse:

```text
Load Aggregate

↓

Apply Historical State

↓

No New Domain Fact
```

---

# No Event for Serialization

Serializar Participation no produce Domain Events.

Debe mantenerse:

```text
Serialization

≠

Domain Behavior
```

---

# No Event for Persistence

Persistir un Aggregate sin un nuevo cambio de dominio no produce un
nuevo Domain Event.

Debe mantenerse:

```text
Repository Save

≠

New Domain Fact
```

---

# No Event for Projection

Actualizar un Read Model no produce por sí mismo un Domain Event de
Participation.

Debe mantenerse:

```text
Domain Event

↓

Projection
```

No:

```text
Projection

↓

Participation Domain Event
```

---

# No Event for Integration Delivery

La publicación o entrega de un Integration Event no constituye un
nuevo Domain Event de Participation.

Debe mantenerse:

```text
Domain Fact

↓

Integration Event

↓

External Delivery
```

El transporte externo no reescribe el hecho interno.

---

# Naming

Los Domain Events deben utilizar nombres en pasado.

Ejemplos válidos:

```text
ParticipationRegistered

ParticipationActivated

ParticipationCompleted

ParticipationWithdrawn

ParticipationInvalidated

ParticipationArchived
```

Ejemplos no válidos como Domain Events:

```text
RegisterParticipation

ActivateParticipation

CompleteParticipation
```

Estos corresponden a Commands.

---

# Lenguaje Ubicuo

Los nombres de eventos deben utilizar conceptos reconocidos por el
dominio Participation.

Debe existir correspondencia entre:

```text
Lifecycle

State Machine

Commands

Domain Events

Invariants
```

No deben introducirse sinónimos técnicos que fragmenten el lenguaje
ubicuo.

---

# Evolución de Eventos

Los Domain Events pueden evolucionar cuando el dominio requiera
representar nuevos hechos.

La evolución debe preservar:

- significado histórico;
- identidad del evento;
- compatibilidad conceptual;
- trazabilidad;
- coherencia con Lifecycle;
- coherencia con State Machine;
- coherencia con Commands;
- coherencia con Invariants;
- coherencia con Read Models;
- coherencia con Integration Events.

---

# Eventos Históricos y Evolución

Un evento histórico conserva el significado que tenía cuando fue
producido.

Una nueva versión del modelo no debe reinterpretar silenciosamente
un hecho histórico con una semántica incompatible.

---

# Compatibilidad

Cuando la estructura técnica de un evento evolucione, la estrategia
de compatibilidad pertenece al diseño de serialización e
Infrastructure.

El dominio debe preservar el significado conceptual del hecho.

---

# Extension Points

El modelo puede incorporar nuevos Domain Events cuando aparezcan
nuevos hechos reales del dominio.

Ejemplos de extensión pueden surgir por:

- nuevos tipos de Participation;
- nuevas reglas de Lifecycle;
- nuevas modificaciones contextuales;
- nuevas capacidades del Aggregate;
- nuevas transiciones formalmente aprobadas.

Una extensión no puede introducir por sí sola una transición que no
exista en la State Machine.

---

# Regla de Extensión

Para incorporar un nuevo evento debe existir una pregunta clara:

```text
What Domain Fact Occurred?
```

Si no existe un hecho de dominio identificable, no debe añadirse un
Domain Event únicamente por razones técnicas.

---

# Domain Events y Extension Points

Toda extensión debe revisarse contra:

```text
DOMAIN-008-Aggregate.md

DOMAIN-008A-Lifecycle.md

DOMAIN-008B-State-Machine.md

DOMAIN-008C-Commands.md

DOMAIN-008E-Invariants.md

DOMAIN-008F-Permissions.md

DOMAIN-008I-Versioning.md

DOMAIN-008J-Consistency-Boundary.md

DOMAIN-008K-Integration-Events.md

DOMAIN-008L-Read-Model.md

DOMAIN-008M-Test-Scenarios.md

DOMAIN-008O-Security-Model.md

DOMAIN-008P-Extension-Points.md
```

---

# Testabilidad

Cada Domain Event debe poder verificarse mediante escenarios
deterministas.

Como mínimo deben comprobarse:

- EventType correcto;
- ParticipationId correcto;
- OrganizationId correcto;
- estado origen correcto;
- estado resultante correcto;
- AggregateVersion correcta;
- OccurredAt válido;
- timestamps del Lifecycle coherentes;
- CorrelationId preservado;
- CausationId correcto;
- datos específicos correctos;
- ausencia del evento cuando el Command es rechazado;
- ausencia de eventos duplicados por una misma modificación;
- preservación de hechos históricos.

Los escenarios formales se documentan en:

```text
DOMAIN-008M-Test-Scenarios.md
```

---

# Performance

Las optimizaciones técnicas relacionadas con Domain Events no
pueden modificar su semántica.

No está permitido eliminar eventos requeridos por el dominio para
reducir:

- escrituras;
- almacenamiento;
- tráfico;
- latencia;
- procesamiento.

Las reglas de rendimiento se desarrollan en:

```text
DOMAIN-008N-Performance-Rules.md
```

---

# Security Model

La información contenida en Domain Events debe respetar el modelo
de seguridad de Participation.

Especialmente:

- minimización de datos;
- separación organizacional;
- protección de identidades;
- ausencia de credenciales;
- control de consumidores;
- trazabilidad;
- integridad.

La definición completa corresponde a:

```text
DOMAIN-008O-Security-Model.md
```

---

# Matriz de Responsabilidades

```text
Responsibility                    Authority

Express Intent                    Command

Validate Business Rules           Participation Aggregate

Protect Invariants                Participation Aggregate

Control State Transition          State Machine

Represent Occurred Fact           Domain Event

Represent Aggregate Version       AggregateVersion

Preserve Causality                CorrelationId / CausationId

Persist Aggregate                 Repository

Build Query Views                 Read Model

Expose External Contract          Integration Event

Consume Audit Information         Audit

Transport Event                   Infrastructure
```

---

# Regla de Separación de Responsabilidades

El Domain Event no debe asumir responsabilidades pertenecientes a:

```text
Command

Aggregate

Repository

Read Model

Integration Event

Audit

Notification

Infrastructure
```

Su responsabilidad es representar un hecho ocurrido dentro del
dominio Participation.

---

# Restricciones

No está permitido:

- modificar un Domain Event después de su creación;
- emitir eventos de éxito para Commands rechazados;
- emitir eventos que representen transiciones inexistentes;
- modificar Participation desde un Event Handler interno al mismo
  Aggregate sin una intención válida;
- utilizar Domain Events como Commands;
- utilizar Domain Events como setters;
- utilizar eventos CRUD como sustituto del lenguaje de dominio;
- utilizar un evento genérico para ocultar hechos significativos;
- incluir Aggregates externos completos;
- modificar otros Aggregates directamente;
- incluir credenciales;
- incluir tokens;
- incluir secretos;
- incluir sesiones;
- depender de Infrastructure;
- depender de protocolos de transporte;
- depender de bases de datos;
- depender de frameworks;
- confundir OccurredAt con tiempos técnicos de publicación;
- confundir EventId con ParticipationId;
- reutilizar EventId para hechos distintos;
- reescribir eventos históricos;
- producir nuevos eventos durante rehidratación;
- producir nuevos eventos durante replay;
- producir nuevos eventos por una simple consulta;
- producir nuevos eventos por serialización;
- producir nuevos eventos por persistencia sin cambio de dominio;
- incrementar Version por procesar nuevamente un evento histórico;
- representar cambios de otros Aggregates como eventos propios de
  Participation;
- exponer automáticamente un Domain Event interno como contrato
  externo;
- introducir eventos sin significado dentro del lenguaje ubicuo.

---

# Compatibilidad con DDD

Los Domain Events de Participation cumplen los principios de
Domain-Driven Design mediante:

- representación explícita de hechos;
- lenguaje ubicuo;
- propiedad del Aggregate;
- independencia entre Aggregates;
- protección de Invariants;
- separación entre intención y hecho;
- separación entre dominio e Infrastructure.

---

# Compatibilidad con CQRS

Los eventos permiten conectar:

```text
Write Side

↓

Participation Aggregate

↓

Domain Events

↓

Read Side
```

sin permitir que el Read Side controle las decisiones del
Aggregate.

---

# Compatibilidad con Event Sourcing

Los eventos poseen semántica suficiente para formar parte de una
historia reconstruible cuando Event Sourcing sea utilizado.

Debe preservarse:

```text
Ordered Domain Facts

↓

Aggregate Reconstruction
```

sin convertir Event Sourcing en una dependencia obligatoria del
modelo conceptual.

---

# Compatibilidad con Event-Driven Architecture

Los Domain Events permiten reaccionar a hechos sin acoplar
Participation con consumidores concretos.

Debe mantenerse:

```text
Producer

↓

Domain Event

↓

Independent Consumers
```

---

# Compatibilidad con Clean Architecture

Los Domain Events permanecen dentro de las capas internas del
modelo.

No conocen:

- adaptadores;
- controladores;
- bases de datos;
- brokers;
- endpoints;
- frameworks.

---

# Compatibilidad con Hexagonal Architecture

Los Domain Events pueden atravesar Ports definidos por la
arquitectura sin depender de Adapters concretos.

La infraestructura adapta su representación.

El dominio mantiene su semántica.

---

# Compatibilidad con Arquitectura Distribuida

Los Domain Events permiten coordinar procesos entre límites
independientes sin ampliar la transacción del Aggregate.

Debe mantenerse:

```text
Participation Transaction

↓

Domain Event

↓

Eventual External Coordination
```

---

# Principios Arquitectónicos

El modelo oficial mantiene:

```text
Command

=

Intent
```

```text
Domain Event

=

Occurred Domain Fact
```

```text
Integration Event

=

External Contract
```

```text
Read Model

=

Derived Query Representation
```

```text
Domain Event

≠

Command
```

```text
Domain Event

≠

Integration Event
```

```text
Domain Event

≠

Read Model
```

```text
Domain Event

≠

Database Record
```

```text
Domain Event

≠

Transport Message
```

```text
Domain Event

≠

Audit Aggregate
```

```text
Domain Event

≠

External Aggregate Mutation
```

---

# Documentación Complementaria

Los Domain Events deben interpretarse conjuntamente con:

```text
DOMAIN-008-Aggregate.md

DOMAIN-008A-Lifecycle.md

DOMAIN-008B-State-Machine.md

DOMAIN-008C-Commands.md

DOMAIN-008E-Invariants.md

DOMAIN-008F-Permissions.md

DOMAIN-008G-Repository-Contract.md

DOMAIN-008H-Examples.md

DOMAIN-008I-Versioning.md

DOMAIN-008J-Consistency-Boundary.md

DOMAIN-008K-Integration-Events.md

DOMAIN-008L-Read-Model.md

DOMAIN-008M-Test-Scenarios.md

DOMAIN-008N-Performance-Rules.md

DOMAIN-008O-Security-Model.md

DOMAIN-008P-Extension-Points.md
```

Cada documento desarrolla una responsabilidad específica sin
alterar la definición de Domain Event establecida en este
documento.

---

# Definición de Éxito

Los Domain Events del Aggregate **Participation** constituyen la
representación oficial de los hechos relevantes que han ocurrido
dentro de su límite de consistencia.

Los eventos transicionales:

```text
ParticipationRegistered

ParticipationActivated

ParticipationCompleted

ParticipationWithdrawn

ParticipationInvalidated

ParticipationArchived
```

representan la evolución oficial del Lifecycle.

Los eventos no transicionales:

```text
ParticipationTypeChanged

ParticipationContextChanged

ParticipationMetadataUpdated
```

representan modificaciones válidas que no alteran implícitamente
el estado del Lifecycle.

Cada Domain Event:

- representa un hecho consumado;
- posee identidad propia;
- identifica la Participation;
- mantiene contexto organizacional;
- conserva trazabilidad;
- conserva correlación y causalidad cuando corresponda;
- representa la AggregateVersion resultante;
- es inmutable;
- corresponde a una modificación válida;
- respeta Lifecycle;
- respeta State Machine;
- respeta Invariants;
- respeta Permissions;
- respeta Versioning;
- puede alimentar Read Models;
- puede originar Integration Events;
- puede apoyar Audit;
- no modifica otros Aggregates;
- no depende de Infrastructure.

Debe mantenerse como regla fundamental:

```text
Command Rejected

↓

No Domain Change

↓

No Version Increment

↓

No Success Domain Event
```

y:

```text
Valid Domain Change

↓

Version Increment

↓

Domain Event
```

De esta forma,
`DOMAIN-008D-Domain-Events.md` constituye la definición normativa
oficial de los hechos de dominio del Aggregate **Participation**,
preservando la trazabilidad, la semántica del lenguaje ubicuo, la
separación entre intención y hecho, la independencia entre
Aggregates, la consistencia del dominio y el patrón DDD consolidado
de AURA Core.