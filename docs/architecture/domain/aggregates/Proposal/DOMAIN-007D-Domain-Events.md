# DOMAIN-007D — Proposal Domain Events

Versión: 1.1

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Proposal Management

Aggregate:
Proposal

Autor:
ARADA

Documentos relacionados:

- DOMAIN-007-Aggregate.md
- DOMAIN-007A-Lifecycle.md
- DOMAIN-007B-State-Machine.md
- DOMAIN-007C-Commands.md
- DOMAIN-007E-Invariants.md
- DOMAIN-007F-Permissions.md
- DOMAIN-007I-Versioning.md
- DOMAIN-007J-Consistency-Boundary.md
- DOMAIN-007K-Integration-Events.md
- CORE-003-Shared-Kernel.md
- CORE-004-Ubiquitous-Language.md
- CORE-005-Domain-Events.md
- CORE-006-Domain-Invariants.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Definir los Domain Events oficiales generados y registrados por el Aggregate
**Proposal** cuando ocurre un hecho relevante dentro de su ciclo
de vida.

Un Domain Event representa un hecho que ya ocurrió dentro del
dominio.

Los Domain Events permiten registrar de forma explícita las
modificaciones relevantes de Proposal y comunicar dichos hechos
sin acoplar el Aggregate a consumidores externos.

Este documento establece:

- significado conceptual de cada evento;
- condiciones que permiten su emisión;
- relación entre Commands y Domain Events;
- información conceptual mínima de los eventos;
- relación con el Lifecycle;
- relación con la State Machine;
- relación con Versioning;
- reglas de consistencia;
- reglas de publicación;
- restricciones;
- trazabilidad;
- relación con Integration Events.

---

# Propósito

Los Domain Events de Proposal representan hechos consumados que
han ocurrido como consecuencia de comportamiento válido del
Aggregate.

Conceptualmente:

```text
Command

↓

Proposal Aggregate

↓

State Machine

↓

Invariants

↓

Valid State Change

↓

Domain Event
```

Un Domain Event solo puede existir después de que Proposal haya
aceptado y aplicado válidamente una operación.

El evento describe lo ocurrido.

No solicita que ocurra.

---

# Definición

Un Domain Event es una representación inmutable de un hecho
significativo ocurrido dentro del Aggregate Proposal.

Ejemplos:

```text
ProposalCreated

ProposalSubmitted

ProposalReviewStarted

ProposalAccepted

ProposalRejected

ProposalWithdrawn

ProposalArchived
```

Cada nombre utiliza tiempo pasado porque representa un hecho ya
consumado.

Debe mantenerse:

```text
Domain Event
    =
Fact
```

No:

```text
Domain Event
    =
Intent
```

---

# Principios

Todos los Domain Events de Proposal deben cumplir los siguientes
principios:

- representan hechos consumados;
- utilizan lenguaje ubicuo;
- son inmutables;
- poseen identidad propia;
- identifican el Aggregate que produjo el hecho;
- corresponden a una modificación válida;
- son emitidos exclusivamente después de proteger invariantes;
- no ejecutan comportamiento del Aggregate;
- no contienen lógica de negocio;
- no modifican directamente otros Aggregates;
- permiten trazabilidad;
- pueden alimentar Read Models;
- pueden originar Integration Events;
- pueden participar en auditoría;
- pueden utilizarse para reconstrucción cuando la arquitectura lo
  requiera.

---

# Domain Event y Command

Command y Domain Event representan conceptos diferentes.

```text
Command
    =
Intent
```

```text
Domain Event
    =
Fact
```

Ejemplo:

```text
SubmitProposal
```

representa:

```text
Intent to submit
```

Después de una operación válida:

```text
ProposalSubmitted
```

representa:

```text
Proposal was submitted
```

Debe mantenerse:

```text
SubmitProposal
    ≠
ProposalSubmitted
```

El primero puede ser rechazado.

El segundo representa un hecho que ya ocurrió.

---

# Domain Event y Estado

Un Domain Event puede representar una transición de estado.

Ejemplo:

```text
ProposalStatus = Draft
```

Command:

```text
SubmitProposal
```

Transición válida:

```text
Draft

↓

Submitted
```

Domain Event:

```text
ProposalSubmitted
```

El evento no realiza la transición.

El Aggregate realiza la transición y posteriormente registra el
hecho correspondiente.

---

# Domain Event y Aggregate Root

Los Domain Events son producidos por:

```text
Proposal
```

como Aggregate Root.

No son producidos directamente por:

- Repository;
- Controller;
- endpoint HTTP;
- base de datos;
- Read Model;
- infraestructura;
- consumidor externo.

El Aggregate determina qué hecho de dominio ocurrió como
consecuencia de su comportamiento.

---

# Estructura General

Todo Domain Event debe contener, como mínimo, información
conceptual suficiente para identificar:

```text
EventId

EventType

ProposalId

OrganizationId

OccurredAt

AggregateVersion

CorrelationId

CausationId
```

Cada evento puede incorporar información adicional cuando sea
necesaria para representar correctamente el hecho ocurrido.

---

# EventId

Identifica de forma única una instancia del Domain Event.

```text
EventId
```

EventId:

- es único;
- es inmutable;
- no constituye ProposalId;
- permite trazabilidad;
- permite distinguir eventos diferentes;
- puede utilizarse para evitar procesamiento duplicado.

Dos eventos del mismo tipo producidos por la misma Proposal deben
poseer EventId diferentes.

---

# EventType

Identifica semánticamente el tipo de hecho ocurrido.

Ejemplos:

```text
ProposalCreated

ProposalSubmitted

ProposalAccepted
```

EventType debe corresponder al lenguaje ubicuo del dominio.

No debe representar nombres técnicos de infraestructura.

---

# ProposalId

Identifica el Aggregate que produjo el evento.

```text
ProposalId
```

ProposalId permite relacionar el evento con la historia de una
Proposal específica.

ProposalId es inmutable dentro del evento.

---

# OrganizationId

Identifica el contexto organizacional de Proposal.

```text
OrganizationId
```

OrganizationId permite conservar el contexto de pertenencia del
Aggregate sin incorporar Organization dentro del evento como un
Aggregate completo.

---

# OccurredAt

Representa el instante en que ocurrió el hecho de dominio.

```text
OccurredAt
```

OccurredAt corresponde al hecho consumado.

No debe confundirse con el momento técnico en que un consumidor
procesa posteriormente el evento.

---

# AggregateVersion

Representa la versión de Proposal asociada al hecho ocurrido.

```text
AggregateVersion
```

Permite:

- ordenar modificaciones;
- mantener trazabilidad;
- detectar secuencias inconsistentes;
- relacionar el evento con el estado producido;
- soportar reconstrucción cuando corresponda.

El modelo formal de Versioning se desarrolla en:

```text
DOMAIN-007I-Versioning.md
```

---

# CorrelationId

Permite relacionar el evento con un flujo lógico mayor.

```text
CorrelationId
```

Puede conservarse a través de:

```text
Command

↓

Domain Event

↓

Integration Event
```

CorrelationId no modifica el significado del hecho.

---

# CausationId

Identifica conceptualmente la causa inmediata del evento.

```text
CausationId
```

Cuando un Domain Event es consecuencia de un Command,
CausationId puede referenciar:

```text
CommandId
```

Esto permite mantener la relación:

```text
Command

↓

Domain Event
```

sin convertir ambos conceptos en la misma entidad.

---

# Inmutabilidad

Una vez producido un Domain Event no puede ser modificado.

Debe mantenerse:

```text
Domain Event

↓

Immutable
```

No está permitido:

```text
UpdateDomainEvent
```

ni:

```text
EditDomainEvent
```

Si posteriormente ocurre otro hecho relevante, debe producirse
otro Domain Event.

---

# Eventos Oficiales

Los Domain Events oficiales del Aggregate Proposal son:

```text
ProposalCreated

ProposalRenamed

ProposalPurposeChanged

ProposalDescriptionChanged

ProposalTypeChanged

ProposalContentUpdated

ProposalTerritoryChanged

ProposalAssemblyAssociated

ProposalSubmitted

ProposalReviewStarted

ProposalAccepted

ProposalRejected

ProposalWithdrawn

ProposalArchived
```

Cada evento corresponde a un hecho reconocido por el modelo
conceptual de Proposal.

---

# ProposalCreated

## Significado

Indica que una nueva Proposal ha sido creada válidamente.

## Command asociado

```text
CreateProposal
```

## Estado resultante

```text
Draft
```

## Información conceptual

```text
EventId

ProposalId

OrganizationId

ActorId

ProposalName

ProposalType

ProposalPurpose

ProposalStatus

OccurredAt

AggregateVersion

CorrelationId

CausationId
```

## Condiciones

ProposalCreated solo puede producirse cuando:

- ProposalId es válido;
- ProposalId no representa una Proposal existente;
- OrganizationId es válido;
- los datos iniciales satisfacen las reglas del dominio;
- las invariantes iniciales están satisfechas;
- CreateProposal ha sido aceptado.

## Semántica

```text
Proposal did not exist

↓

Proposal created

↓

Draft
```

ProposalCreated constituye el primer hecho formal del ciclo de
vida de Proposal.

---

# ProposalRenamed

## Significado

Indica que el nombre de una Proposal fue modificado válidamente.

## Command asociado

```text
RenameProposal
```

## Estado permitido

```text
Draft
```

## Información conceptual

```text
EventId

ProposalId

OrganizationId

PreviousProposalName

ProposalName

ActorId

OccurredAt

AggregateVersion

CorrelationId

CausationId
```

## Condiciones

ProposalRenamed solo puede producirse cuando:

- Proposal existe;
- ProposalStatus permite edición;
- el nuevo nombre es válido;
- las invariantes permanecen satisfechas;
- RenameProposal ha sido aceptado.

## Semántica

El evento representa el cambio de nombre.

No modifica ProposalId.

No representa una nueva Proposal.

---

# ProposalPurposeChanged

## Significado

Indica que el propósito formal de Proposal fue modificado
válidamente.

## Command asociado

```text
ChangeProposalPurpose
```

## Estado permitido

```text
Draft
```

## Información conceptual

```text
EventId

ProposalId

OrganizationId

PreviousProposalPurpose

ProposalPurpose

ActorId

OccurredAt

AggregateVersion

CorrelationId

CausationId
```

## Condiciones

ProposalPurposeChanged solo puede producirse después de una
modificación válida del propósito.

La operación no modifica:

```text
ProposalId

OrganizationId

ProposalStatus
```

---

# ProposalDescriptionChanged

## Significado

Indica que la descripción de Proposal fue modificada válidamente.

## Command asociado

```text
ChangeProposalDescription
```

## Estado permitido

```text
Draft
```

## Información conceptual

```text
EventId

ProposalId

OrganizationId

PreviousProposalDescription

ProposalDescription

ActorId

OccurredAt

AggregateVersion

CorrelationId

CausationId
```

## Condiciones

El evento solo puede producirse cuando la descripción resultante
satisface las reglas aplicables del Aggregate.

---

# ProposalTypeChanged

## Significado

Indica que la clasificación conceptual de Proposal fue modificada
válidamente.

## Command asociado

```text
ChangeProposalType
```

## Estado permitido

```text
Draft
```

## Información conceptual

```text
EventId

ProposalId

OrganizationId

PreviousProposalType

ProposalType

ActorId

OccurredAt

AggregateVersion

CorrelationId

CausationId
```

## Restricciones

ProposalTypeChanged no modifica la identidad de Proposal.

Debe mantenerse:

```text
ProposalId
    =
same ProposalId
```

antes y después del cambio.

---

# ProposalContentUpdated

## Significado

Indica que el contenido propio de Proposal fue actualizado
válidamente.

## Command asociado

```text
UpdateProposalContent
```

## Estado permitido

```text
Draft
```

## Información conceptual

```text
EventId

ProposalId

OrganizationId

ContentChangeReference

ActorId

OccurredAt

AggregateVersion

CorrelationId

CausationId
```

## Condiciones

ProposalContentUpdated solo puede producirse cuando:

- Proposal se encuentra en un estado editable;
- el contenido pertenece al límite del Aggregate;
- la actualización es válida;
- las invariantes permanecen satisfechas.

## Restricciones

El evento no debe utilizarse para incorporar otros Aggregates
completos dentro de Proposal.

---

# ProposalTerritoryChanged

## Significado

Indica que la referencia territorial de Proposal fue modificada
válidamente.

## Command asociado

```text
ChangeProposalTerritory
```

## Estado permitido

```text
Draft
```

## Información conceptual

```text
EventId

ProposalId

OrganizationId

PreviousTerritoryId

TerritoryId

ActorId

OccurredAt

AggregateVersion

CorrelationId

CausationId
```

## Restricciones

ProposalTerritoryChanged representa exclusivamente el cambio de
referencia:

```text
TerritoryId
```

No representa una modificación del Aggregate Territory.

---

# ProposalAssemblyAssociated

## Significado

Indica que Proposal fue asociada válidamente con una Assembly.

## Command asociado

```text
AssociateProposalAssembly
```

## Estado permitido

```text
Draft
```

## Información conceptual

```text
EventId

ProposalId

OrganizationId

AssemblyId

ActorId

OccurredAt

AggregateVersion

CorrelationId

CausationId
```

## Restricciones

El evento:

- no modifica Assembly;
- no modifica AssemblyStatus;
- no convierte Assembly en parte del Aggregate Proposal;
- no modifica el ciclo de vida de Assembly.

La relación se mantiene mediante:

```text
AssemblyId
```

---

# ProposalSubmitted

## Significado

Indica que Proposal fue presentada formalmente.

## Command asociado

```text
SubmitProposal
```

## Estado origen

```text
Draft
```

## Estado destino

```text
Submitted
```

## Información conceptual

```text
EventId

ProposalId

OrganizationId

ActorId

SubmittedAt

OccurredAt

AggregateVersion

CorrelationId

CausationId
```

## Condiciones

ProposalSubmitted solo puede producirse cuando:

- ProposalStatus era Draft;
- la Proposal cumple las condiciones de presentación;
- los datos obligatorios están completos;
- las invariantes están satisfechas;
- SubmitProposal fue aceptado.

## Semántica

```text
Draft

↓

Submitted

↓

ProposalSubmitted
```

La emisión del evento significa que la presentación ya ocurrió.

---

# ProposalReviewStarted

## Significado

Indica que comenzó formalmente la revisión de Proposal.

## Command asociado

```text
StartProposalReview
```

## Estado origen

```text
Submitted
```

## Estado destino

```text
UnderReview
```

## Información conceptual

```text
EventId

ProposalId

OrganizationId

ActorId

ReviewStartedAt

OccurredAt

AggregateVersion

CorrelationId

CausationId
```

## Condiciones

ProposalReviewStarted solo puede producirse cuando:

- ProposalStatus era Submitted;
- las condiciones de revisión están satisfechas;
- StartProposalReview fue aceptado;
- la transición es válida;
- las invariantes permanecen satisfechas.

## Semántica

```text
Submitted

↓

UnderReview

↓

ProposalReviewStarted
```

---

# ProposalAccepted

## Significado

Indica que Proposal fue aceptada formalmente.

## Command asociado

```text
AcceptProposal
```

## Estado origen

```text
UnderReview
```

## Estado destino

```text
Accepted
```

## Información conceptual

```text
EventId

ProposalId

OrganizationId

ActorId

AcceptedAt

DecisionReference

OccurredAt

AggregateVersion

CorrelationId

CausationId
```

## Condiciones

ProposalAccepted solo puede producirse cuando:

- ProposalStatus era UnderReview;
- las condiciones de aceptación están satisfechas;
- las reglas de decisión aplicables fueron respetadas;
- AcceptProposal fue aceptado;
- las invariantes permanecen satisfechas.

## Semántica

```text
UnderReview

↓

Accepted

↓

ProposalAccepted
```

## Restricciones

ProposalAccepted no significa automáticamente:

- ejecución de Proposal;
- creación de Voting;
- modificación de Assembly;
- modificación de Participation;
- creación de Document;
- envío de Notification.

Representa exclusivamente el hecho de que Proposal fue aceptada.

---

# ProposalRejected

## Significado

Indica que Proposal fue rechazada formalmente.

## Command asociado

```text
RejectProposal
```

## Estado origen

```text
UnderReview
```

## Estado destino

```text
Rejected
```

## Información conceptual

```text
EventId

ProposalId

OrganizationId

ActorId

RejectionReason

RejectedAt

DecisionReference

OccurredAt

AggregateVersion

CorrelationId

CausationId
```

## Condiciones

ProposalRejected solo puede producirse cuando:

- ProposalStatus era UnderReview;
- las condiciones de rechazo están satisfechas;
- RejectionReason es válido cuando sea requerido;
- RejectProposal fue aceptado;
- las invariantes permanecen satisfechas.

## Semántica

```text
UnderReview

↓

Rejected

↓

ProposalRejected
```

Rejected no elimina Proposal.

La identidad y trazabilidad permanecen conservadas.

---

# ProposalWithdrawn

## Significado

Indica que Proposal fue retirada formalmente del flujo normal.

## Command asociado

```text
WithdrawProposal
```

## Estados origen permitidos

```text
Draft

Submitted
```

## Estado destino

```text
Withdrawn
```

## Información conceptual

```text
EventId

ProposalId

OrganizationId

ActorId

WithdrawalReason

WithdrawnAt

OccurredAt

AggregateVersion

CorrelationId

CausationId
```

## Condiciones

ProposalWithdrawn solo puede producirse cuando:

- ProposalStatus era Draft o Submitted;
- el Lifecycle permite retiro;
- las reglas de retiro están satisfechas;
- WithdrawProposal fue aceptado;
- las invariantes permanecen satisfechas.

## Semántica

```text
Draft

↓

Withdrawn

↓

ProposalWithdrawn
```

o:

```text
Submitted

↓

Withdrawn

↓

ProposalWithdrawn
```

## Restricciones

ProposalWithdrawn no equivale a:

```text
ProposalRejected
```

El retiro y el rechazo representan hechos diferentes del dominio.

---

# ProposalArchived

## Significado

Indica que Proposal fue archivada formalmente.

## Command asociado

```text
ArchiveProposal
```

## Estados origen permitidos

```text
Accepted

Rejected

Withdrawn
```

## Estado destino

```text
Archived
```

## Información conceptual

```text
EventId

ProposalId

OrganizationId

ActorId

ArchivedAt

OccurredAt

AggregateVersion

CorrelationId

CausationId
```

## Condiciones

ProposalArchived solo puede producirse cuando:

- ProposalStatus pertenece a un estado archivable;
- las condiciones de archivado están satisfechas;
- ArchiveProposal fue aceptado;
- la transición es válida;
- las invariantes permanecen satisfechas.

## Semántica

```text
Accepted

↓

Archived
```

o:

```text
Rejected

↓

Archived
```

o:

```text
Withdrawn

↓

Archived
```

seguido de:

```text
ProposalArchived
```

Archived constituye un estado terminal.

---

# Eventos de Transición

Los Domain Events que representan transiciones de
ProposalStatus son:

```text
ProposalCreated

ProposalSubmitted

ProposalReviewStarted

ProposalAccepted

ProposalRejected

ProposalWithdrawn

ProposalArchived
```

Su relación con la State Machine es:

```text
Domain Event                 From           To

ProposalCreated              Nonexistent    Draft

ProposalSubmitted            Draft          Submitted

ProposalReviewStarted        Submitted      UnderReview

ProposalAccepted             UnderReview    Accepted

ProposalRejected             UnderReview    Rejected

ProposalWithdrawn            Draft          Withdrawn

ProposalWithdrawn            Submitted      Withdrawn

ProposalArchived             Accepted       Archived

ProposalArchived             Rejected       Archived

ProposalArchived             Withdrawn      Archived
```

---

# Eventos sin Transición de Estado

Los siguientes eventos representan modificaciones válidas que no
cambian ProposalStatus:

```text
ProposalRenamed

ProposalPurposeChanged

ProposalDescriptionChanged

ProposalTypeChanged

ProposalContentUpdated

ProposalTerritoryChanged

ProposalAssemblyAssociated
```

Aunque no exista transición de estado, cada hecho representa una
modificación del Aggregate y debe corresponder a una Version
posterior válida.

---

# Relación Command — Domain Event

La relación oficial entre Commands y Domain Events es:

```text
Command                      Domain Event
────────────────────────────────────────────────────────────
CreateProposal               ProposalCreated

RenameProposal               ProposalRenamed

ChangeProposalPurpose        ProposalPurposeChanged

ChangeProposalDescription    ProposalDescriptionChanged

ChangeProposalType           ProposalTypeChanged

UpdateProposalContent        ProposalContentUpdated

ChangeProposalTerritory      ProposalTerritoryChanged

AssociateProposalAssembly    ProposalAssemblyAssociated

SubmitProposal               ProposalSubmitted

StartProposalReview          ProposalReviewStarted

AcceptProposal               ProposalAccepted

RejectProposal               ProposalRejected

WithdrawProposal             ProposalWithdrawn

ArchiveProposal              ProposalArchived
```

Esta relación representa correspondencia conceptual.

No significa que recibir un Command garantice la producción del
evento.

Debe mantenerse:

```text
Command Accepted

↓

Valid Domain Change

↓

Domain Event
```

---

# Evento y Version

Todo Domain Event modificador debe corresponder a una versión
válida del Aggregate.

Conceptualmente:

```text
CurrentVersion = N

↓

Valid Change

↓

Version = N + 1

↓

Domain Event
AggregateVersion = N + 1
```

Un Domain Event no debe representar una modificación que no haya
sido confirmada por Proposal.

---

# Orden de Eventos

Los eventos producidos por una misma Proposal deben mantener un
orden coherente con:

```text
AggregateVersion
```

Ejemplo:

```text
ProposalCreated
Version 1

↓

ProposalRenamed
Version 2

↓

ProposalSubmitted
Version 3

↓

ProposalReviewStarted
Version 4

↓

ProposalAccepted
Version 5

↓

ProposalArchived
Version 6
```

No debe existir una secuencia como:

```text
ProposalAccepted
Version 4

↓

ProposalReviewStarted
Version 5
```

porque contradice la State Machine.

---

# Consistencia

Un Domain Event solo puede registrarse como consecuencia de una
modificación válida dentro del Consistency Boundary de Proposal.

Debe mantenerse:

```text
Validate Command

↓

Validate State

↓

Validate Permissions

↓

Validate Invariants

↓

Validate Version

↓

Apply Proposal Behavior

↓

Update Aggregate

↓

Increment Version

↓

Record Domain Event
```

El evento y el cambio que representa pertenecen a la misma unidad
lógica de consistencia del Aggregate.

---

# Atomicidad

No debe existir un Domain Event de éxito sin la modificación
válida que representa.

Ejemplo inválido:

```text
ProposalSubmitted emitted

but

ProposalStatus = Draft
```

También es inválido:

```text
ProposalStatus = Submitted

but

ProposalSubmitted not recorded
```

cuando el modelo exige registrar el hecho correspondiente.

La operación válida debe mantener coherencia entre:

```text
Aggregate State

+

Version

+

Domain Event
```

---

# Evento después de Rechazo

Cuando un Command es rechazado:

```text
Aggregate State
    =
Unchanged
```

```text
Version
    =
Unchanged
```

y:

```text
Success Domain Event
    =
Not Produced
```

Un Command inválido nunca debe generar el Domain Event que
representaría su supuesto éxito.

---

# Domain Events y Permissions

Permissions determinan si un actor puede intentar una operación.

Domain Events representan hechos ocurridos después de que la
operación haya sido aceptada.

Debe mantenerse:

```text
Permission Granted

↓

Command Evaluation

↓

Domain Validation

↓

Domain Event
```

No:

```text
Permission Granted

↓

Domain Event
```

La autorización por sí sola no produce hechos de dominio.

---

# Domain Events e Invariantes

Ningún Domain Event de éxito puede representar una modificación
que viole una invariante.

Debe mantenerse:

```text
Invariant Violation

↓

Operation Rejected

↓

No Success Domain Event
```

Las invariantes oficiales se desarrollan en:

```text
DOMAIN-007E-Invariants.md
```

---

# Domain Events y Lifecycle

Los eventos de transición deben respetar el Lifecycle definido en:

```text
DOMAIN-007A-Lifecycle.md
```

El evento describe una transición ya realizada.

No puede introducir una transición que no exista en el Lifecycle.

---

# Domain Events y State Machine

Los eventos de transición deben corresponder a transiciones
válidas de:

```text
DOMAIN-007B-State-Machine.md
```

La existencia de un evento no puede utilizarse para crear una
transición alternativa fuera de la State Machine.

---

# Domain Events y Repository

El Repository persiste Proposal conforme al contrato establecido
para el Aggregate.

No es responsabilidad del Repository decidir qué Domain Event
corresponde a una operación.

Debe mantenerse:

```text
Proposal Behavior

↓

Domain Event Recorded

↓

Repository Persistence
```

El Repository no sustituye el comportamiento de Proposal.

---

# Domain Events y Read Models

Los Domain Events pueden alimentar proyecciones de lectura.

Conceptualmente:

```text
Proposal Aggregate

↓

Domain Events

↓

Projection Engine

↓

Proposal Read Models
```

Ejemplos:

```text
ProposalCreated

↓

ProposalSummary
```

```text
ProposalSubmitted

↓

ProposalStatus View
```

```text
ProposalAccepted

↓

ProposalDecision View
```

Los Read Models no modifican Proposal.

La definición formal se desarrollará en:

```text
DOMAIN-007L-Read-Model.md
```

---

# Domain Events e Integration Events

Domain Events e Integration Events no representan el mismo
contrato.

Debe mantenerse:

```text
Domain Event

↓

Domain Boundary

↓

Integration Mapping

↓

Integration Event
```

Un Domain Event puede contener semántica interna que no debe ser
expuesta directamente fuera del Bounded Context.

Los Integration Events deben construirse mediante contratos
específicos de interoperabilidad.

La definición formal se desarrolla en:

```text
DOMAIN-007K-Integration-Events.md
```

---

# Domain Events y Notification

Un Domain Event puede originar posteriormente procesos de
Notification.

Ejemplo:

```text
ProposalSubmitted

↓

Notification Process
```

o:

```text
ProposalAccepted

↓

Notification Process
```

Proposal no envía Notification directamente como parte de la
emisión del Domain Event.

Notification conserva su propio límite de consistencia.

---

# Domain Events y Audit

Los Domain Events constituyen una fuente relevante de
trazabilidad.

Audit Management no consume estos Domain Events. Si existe contrato en
DOMAIN-007K, puede recibir Integration Events equivalentes a:

```text
ProposalCreated

ProposalSubmitted

ProposalReviewStarted

ProposalAccepted

ProposalRejected

ProposalWithdrawn

ProposalArchived
```

Proposal no incorpora Audit como entidad interna.

La relación se mantiene mediante:

- EventId;
- ProposalId;
- OrganizationId;
- ActorId;
- OccurredAt;
- AggregateVersion;
- CorrelationId;
- CausationId.

---

# Domain Events y Assembly

ProposalAssemblyAssociated puede representar el hecho de que una
Proposal adquirió una referencia válida hacia:

```text
AssemblyId
```

El evento no modifica Assembly.

Debe mantenerse:

```text
ProposalAssemblyAssociated

↓

Proposal changed
```

No:

```text
ProposalAssemblyAssociated

↓

Assembly changed
```

---

# Domain Events y Territory

ProposalTerritoryChanged representa una modificación de:

```text
TerritoryId
```

dentro del contexto permitido de Proposal.

No representa una modificación del Aggregate Territory.

---

# Domain Events y Participation

Participation puede reaccionar a determinados hechos de Proposal
cuando las reglas del dominio así lo requieran.

La relación conceptual es:

```text
Proposal

↓

Domain Event

↓

Coordination

↓

Participation
```

Proposal no modifica Participation directamente durante la
producción de su evento.

---

# Domain Events y Voting

Voting puede utilizar hechos de Proposal como contexto para
procesos posteriores.

De igual forma, un resultado de Voting puede originar una
intención posterior sobre Proposal.

Esto no transforma:

```text
Voting Event
```

en:

```text
Proposal Domain Event
```

Cada Aggregate conserva sus propios eventos.

---

# Domain Events y Document

Los Domain Events de Proposal pueden originar procesos
documentales posteriores.

Ejemplo:

```text
ProposalAccepted

↓

Document Process
```

Proposal no crea ni modifica directamente Document como parte de
la emisión del evento.

---

# Domain Events y Organization

Todos los eventos de Proposal conservan el contexto de:

```text
OrganizationId
```

Esto no significa que Organization forme parte de Proposal ni que
el evento modifique Organization.

---

# Domain Events y Event Sourcing

Cuando la arquitectura utilice Event Sourcing Compatible, los
Domain Events pueden participar en la reconstrucción histórica
del Aggregate.

Conceptualmente:

```text
ProposalCreated

↓

ProposalRenamed

↓

ProposalSubmitted

↓

ProposalReviewStarted

↓

ProposalAccepted

↓

ProposalArchived
```

puede reconstruir la evolución de una Proposal.

La reconstrucción aplica hechos históricos.

No vuelve a ejecutar Commands.

Debe mantenerse:

```text
Replay Domain Events
```

No:

```text
Replay Commands
```

---

# Replay

Durante Event Replay:

- no se vuelven a evaluar Permissions;
- no se vuelven a ejecutar Commands;
- no se producen nuevamente efectos externos;
- no se publican nuevamente Integration Events como consecuencia
  automática del replay;
- se reconstruye el estado mediante hechos ya ocurridos.

Replay representa reconstrucción.

No representa nueva actividad del dominio.

---

# Idempotencia de Consumo

Los handlers internos de Domain Events deben poder distinguir eventos
mediante:

```text
EventId
```

Un mismo evento procesado más de una vez no debe interpretarse
como múltiples hechos diferentes.

Conceptualmente:

```text
Same EventId

↓

Same Domain Fact
```

No:

```text
Same EventId

↓

New Domain Fact
```

---

# Ordenamiento

Para eventos de un mismo Aggregate, el orden lógico se determina
mediante:

```text
ProposalId

+

AggregateVersion
```

OccurredAt proporciona contexto temporal, pero no sustituye el
orden de Version cuando se reconstruye la secuencia del
Aggregate.

---

# Concurrencia

Los Domain Events deben reflejar únicamente la modificación que
logró confirmarse válidamente.

Ejemplo:

```text
ProposalStatus = UnderReview

Version = 12
```

Dos Commands compiten:

```text
AcceptProposal
ExpectedVersion = 12
```

y:

```text
RejectProposal
ExpectedVersion = 12
```

Si AcceptProposal confirma primero:

```text
ProposalStatus = Accepted

Version = 13

ProposalAccepted
AggregateVersion = 13
```

RejectProposal debe fallar por conflicto de concurrencia.

No debe producirse:

```text
ProposalRejected
AggregateVersion = 13
```

para la misma versión confirmada.

---

# Publicación

Los Domain Events deben considerarse publicables únicamente
después de que el cambio correspondiente haya sido confirmado
dentro de la unidad de consistencia.

Conceptualmente:

```text
Apply Change

↓

Persist Valid Aggregate

↓

Confirm Change

↓

Publish Domain Event
```

La estrategia técnica concreta de publicación pertenece a la
arquitectura de implementación.

El dominio únicamente establece que no debe comunicarse como
consumado un hecho que todavía no ha sido confirmado.

---

# Fallo de Publicación

Un fallo técnico posterior a la confirmación del Aggregate no
debe reinterpretar el hecho de dominio como si nunca hubiese
ocurrido.

La infraestructura debe preservar la capacidad de publicar los
hechos confirmados conforme a los mecanismos definidos por la
arquitectura.

El Domain Event continúa representando un hecho ocurrido.

---

# Domain Events y Efectos Externos

Un Domain Event no ejecuta directamente:

- envío de correo;
- envío de SMS;
- notificaciones push;
- llamadas HTTP;
- actualización de sistemas municipales;
- publicación FIWARE;
- escritura en sistemas externos;
- modificación de otros Aggregates.

Los efectos externos son responsabilidad de consumidores,
Application Services o mecanismos de integración.

---

# Independencia Tecnológica

Los Domain Events de Proposal no dependen de:

```text
HTTP

REST

GraphQL

JSON

Kafka

RabbitMQ

MQTT

PostgreSQL

MongoDB

Redis

OAuth

JWT

FastAPI

Django

React

Next.js

FIWARE
```

Estas tecnologías pueden transportar, persistir o consumir
representaciones de eventos.

No definen su significado de dominio.

---

# Serialización

La forma técnica utilizada para serializar un Domain Event no
forma parte de su significado conceptual.

Un evento puede representarse técnicamente mediante diferentes
formatos sin alterar el hecho que representa.

Debe mantenerse:

```text
Domain Event Semantics

≠

Serialization Format
```

---

# Seguridad

Los Domain Events no deben contener:

- contraseñas;
- tokens de acceso;
- JWT;
- claves privadas;
- secretos;
- credenciales;
- información técnica de sesión.

La información incluida debe limitarse a aquella necesaria para
representar el hecho de dominio.

---

# Privacidad

La existencia de un Domain Event no autoriza automáticamente la
exposición de todos sus datos a cualquier consumidor.

La publicación y proyección deben respetar las políticas de
seguridad y privacidad correspondientes.

Los Integration Events pueden requerir una representación
reducida o transformada del Domain Event.

---

# Trazabilidad

Cada Domain Event debe permitir relacionar:

```text
Event

↓

Proposal

↓

Organization

↓

Actor

↓

Time

↓

Aggregate Version

↓

Correlation

↓

Cause
```

Esto permite mantener una historia coherente de los hechos
relevantes sin introducir Audit dentro del Aggregate.

---

# Matriz Event — Lifecycle

```text
Domain Event                 Lifecycle Meaning
────────────────────────────────────────────────────────────
ProposalCreated              Proposal enters Draft

ProposalRenamed              Draft data changed

ProposalPurposeChanged       Draft data changed

ProposalDescriptionChanged   Draft data changed

ProposalTypeChanged          Draft data changed

ProposalContentUpdated       Draft data changed

ProposalTerritoryChanged     Draft context changed

ProposalAssemblyAssociated   Draft context changed

ProposalSubmitted            Draft → Submitted

ProposalReviewStarted        Submitted → UnderReview

ProposalAccepted             UnderReview → Accepted

ProposalRejected             UnderReview → Rejected

ProposalWithdrawn            Draft → Withdrawn
                             Submitted → Withdrawn

ProposalArchived             Accepted → Archived
                             Rejected → Archived
                             Withdrawn → Archived
```

---

# Secuencia Válida — Proposal Aceptada

```text
ProposalCreated

↓

ProposalRenamed

↓

ProposalContentUpdated

↓

ProposalSubmitted

↓

ProposalReviewStarted

↓

ProposalAccepted

↓

ProposalArchived
```

Esta secuencia representa una evolución válida conforme al
Lifecycle.

---

# Secuencia Válida — Proposal Rechazada

```text
ProposalCreated

↓

ProposalSubmitted

↓

ProposalReviewStarted

↓

ProposalRejected

↓

ProposalArchived
```

---

# Secuencia Válida — Proposal Retirada desde Draft

```text
ProposalCreated

↓

ProposalWithdrawn

↓

ProposalArchived
```

---

# Secuencia Válida — Proposal Retirada desde Submitted

```text
ProposalCreated

↓

ProposalSubmitted

↓

ProposalWithdrawn

↓

ProposalArchived
```

---

# Secuencias Inválidas

No son válidas secuencias como:

```text
ProposalCreated

↓

ProposalAccepted
```

porque falta:

```text
Submitted

↓

UnderReview
```

Tampoco:

```text
ProposalSubmitted

↓

ProposalRenamed
```

porque los Commands editoriales definidos en la versión 1.0 solo
se permiten en Draft.

Tampoco:

```text
ProposalArchived

↓

ProposalSubmitted
```

porque Archived constituye un estado terminal.

---

# Escenario — ProposalCreated

```text
Given

Proposal no existe

And

CreateProposal es válido

When

Proposal es creada

Then

ProposalStatus = Draft

And

Version incrementa conforme al modelo inicial

And

ProposalCreated es registrado
```

---

# Escenario — ProposalSubmitted

```text
Given

ProposalStatus = Draft

And

SubmitProposal es válido

When

Proposal cambia a Submitted

Then

Version incrementa

And

ProposalSubmitted es registrado
```

---

# Escenario — ProposalAccepted

```text
Given

ProposalStatus = UnderReview

And

AcceptProposal es válido

When

Proposal cambia a Accepted

Then

Version incrementa

And

ProposalAccepted es registrado
```

---

# Escenario — ProposalRejected

```text
Given

ProposalStatus = UnderReview

And

RejectProposal es válido

When

Proposal cambia a Rejected

Then

Version incrementa

And

ProposalRejected es registrado
```

---

# Escenario — ProposalWithdrawn

```text
Given

ProposalStatus = Submitted

And

WithdrawProposal es válido

When

Proposal cambia a Withdrawn

Then

Version incrementa

And

ProposalWithdrawn es registrado
```

---

# Escenario — ProposalArchived

```text
Given

ProposalStatus = Accepted

And

ArchiveProposal es válido

When

Proposal cambia a Archived

Then

Version incrementa

And

ProposalArchived es registrado
```

---

# Escenario — Command Rechazado

```text
Given

ProposalStatus = Submitted

When

AcceptProposal es solicitado

Then

el Command es rechazado

And

Proposal permanece Submitted

And

Version permanece sin cambios

And

ProposalAccepted no es producido
```

---

# Escenario — Concurrencia

```text
Given

ProposalStatus = UnderReview

And

Version = 12

When

AcceptProposal confirma primero

Then

ProposalStatus = Accepted

And

Version = 13

And

ProposalAccepted
AggregateVersion = 13

And

un RejectProposal concurrente basado en Version 12 es rechazado

And

ProposalRejected no es producido
```

---

# Reconstrucción Conceptual

Una historia válida puede representarse como:

```text
ProposalCreated
Version 1

↓

ProposalPurposeChanged
Version 2

↓

ProposalContentUpdated
Version 3

↓

ProposalSubmitted
Version 4

↓

ProposalReviewStarted
Version 5

↓

ProposalAccepted
Version 6

↓

ProposalArchived
Version 7
```

El estado resultante es:

```text
ProposalStatus = Archived

Version = 7
```

La identidad permanece:

```text
ProposalId
```

durante toda la secuencia.

---

# Reglas de Evolución

Un nuevo Domain Event puede incorporarse cuando exista un nuevo
hecho relevante reconocido por el dominio.

La incorporación debe evaluar su coherencia con:

```text
DOMAIN-007-Aggregate.md

DOMAIN-007A-Lifecycle.md

DOMAIN-007B-State-Machine.md

DOMAIN-007C-Commands.md

DOMAIN-007D-Domain-Events.md

DOMAIN-007E-Invariants.md

DOMAIN-007F-Permissions.md

DOMAIN-007I-Versioning.md

DOMAIN-007J-Consistency-Boundary.md

DOMAIN-007K-Integration-Events.md

DOMAIN-007L-Read-Model.md

DOMAIN-007M-Test-Scenarios.md

DOMAIN-007O-Security-Model.md

DOMAIN-007P-Extension-Points.md
```

No debe incorporarse un Domain Event únicamente porque una
tecnología, API o interfaz requiera una notificación técnica.

---

# Versionado de Contratos

La evolución de la representación técnica de un Domain Event no
debe alterar silenciosamente su significado conceptual.

Cuando una evolución cambie la semántica del hecho, debe
evaluarse como una modificación del contrato de dominio.

La compatibilidad técnica pertenece a los mecanismos de
implementación correspondientes.

---

# Regla de Coherencia Documental

Todo Domain Event oficial de Proposal debe encontrarse
documentado en este archivo.

Los documentos posteriores pueden profundizar:

- invariantes;
- Permissions;
- Versioning;
- consistencia;
- Integration Events;
- Read Models;
- seguridad;
- escenarios.

No deben introducir silenciosamente Domain Events que contradigan
el modelo establecido aquí.

---

# Restricciones

No está permitido:

- producir un Domain Event antes de que ocurra el hecho;
- utilizar nombres imperativos para representar Domain Events;
- utilizar Domain Events como Commands;
- utilizar Domain Events como Queries;
- modificar un Domain Event después de su creación;
- producir eventos de éxito para Commands rechazados;
- producir eventos que representen transiciones inválidas;
- producir eventos que violen invariantes;
- producir eventos con AggregateVersion inconsistente;
- utilizar un evento de Proposal para modificar directamente otro
  Aggregate;
- utilizar ProposalAccepted como sustitución de comportamiento de
  Voting;
- utilizar ProposalAssemblyAssociated para modificar Assembly;
- utilizar ProposalTerritoryChanged para modificar Territory;
- publicar como consumado un hecho no confirmado;
- incluir credenciales o secretos;
- acoplar el significado del evento a una tecnología específica;
- confundir Domain Events con Integration Events;
- alterar la historia de eventos ya ocurridos.

---

# Principios Arquitectónicos

Los Domain Events de Proposal preservan las siguientes
separaciones:

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
Domain Event
    ≠
Query
```

```text
Domain Event
    ≠
Notification
```

```text
Domain Event
    ≠
Audit Record
```

```text
Domain Event
    ≠
Persistence Model
```

```text
Domain Event
    ≠
Transport Message
```

```text
Domain Event
    ≠
External Side Effect
```

```text
Proposal Domain Event
    ≠
Event of another Aggregate
```

Estas separaciones preservan el límite del Aggregate y evitan que
responsabilidades externas sean absorbidas por Proposal.

---

# Compatibilidad Arquitectónica

El modelo de Domain Events de Proposal es compatible con:

- Domain-Driven Design;
- Aggregate Pattern;
- CQRS;
- Clean Architecture;
- Hexagonal Architecture;
- Event-Driven Architecture;
- Event Sourcing Compatible;
- Optimistic Concurrency;
- arquitectura distribuida;
- interoperabilidad basada en contratos.

---

# Documentación Complementaria

El modelo de Domain Events debe interpretarse conjuntamente con:

```text
DOMAIN-007-Aggregate.md

DOMAIN-007A-Lifecycle.md

DOMAIN-007B-State-Machine.md

DOMAIN-007C-Commands.md

DOMAIN-007E-Invariants.md

DOMAIN-007F-Permissions.md

DOMAIN-007G-Repository-Contract.md

DOMAIN-007I-Versioning.md

DOMAIN-007J-Consistency-Boundary.md

DOMAIN-007K-Integration-Events.md

DOMAIN-007L-Read-Model.md

DOMAIN-007M-Test-Scenarios.md

DOMAIN-007O-Security-Model.md

DOMAIN-007P-Extension-Points.md
```

Cada documento profundiza una responsabilidad específica sin
reemplazar el significado conceptual de los Domain Events
establecido en este archivo.

---

# Definición de Éxito

Los Domain Events del Aggregate **Proposal** constituyen el
registro conceptual oficial de los hechos relevantes ocurridos
durante la evolución de una iniciativa dentro de AURA Core.

Cada evento representa exclusivamente un hecho consumado después
de que Proposal haya validado:

```text
Current State

↓

Permissions

↓

Preconditions

↓

Invariants

↓

ExpectedVersion

↓

Proposal Behavior
```

Los eventos de transición reflejan estrictamente el Lifecycle:

```text
ProposalCreated

↓

Draft

↓

ProposalSubmitted

↓

Submitted

↓

ProposalReviewStarted

↓

UnderReview

├────────► ProposalAccepted
│
│          Accepted
│
└────────► ProposalRejected
           Rejected
```

junto con los caminos de retiro:

```text
Draft

↓

ProposalWithdrawn

↓

Withdrawn
```

y:

```text
Submitted

↓

ProposalWithdrawn

↓

Withdrawn
```

y los caminos de archivado:

```text
Accepted

↓

ProposalArchived

↓

Archived
```

```text
Rejected

↓

ProposalArchived

↓

Archived
```

```text
Withdrawn

↓

ProposalArchived

↓

Archived
```

Los eventos editoriales representan modificaciones válidas
realizadas mientras Proposal permanece en Draft:

```text
ProposalRenamed

ProposalPurposeChanged

ProposalDescriptionChanged

ProposalTypeChanged

ProposalContentUpdated

ProposalTerritoryChanged

ProposalAssemblyAssociated
```

Cada Domain Event mantiene identidad propia, ProposalId,
OrganizationId, información temporal, AggregateVersion y
trazabilidad suficiente para relacionar el hecho con su contexto.

Los Domain Events no modifican otros Aggregates, no ejecutan
efectos externos, no contienen lógica de negocio y no sustituyen
Commands, Integration Events, Read Models, Notifications ni
Audit.

Un Command rechazado no produce el Domain Event de éxito.

Un hecho confirmado no puede ser modificado retroactivamente.

De esta forma, **DOMAIN-007D-Domain-Events.md** establece el
contrato conceptual oficial de hechos del Aggregate Proposal,
preservando su identidad, Lifecycle, State Machine, invariantes,
consistencia, versionado, trazabilidad, independencia tecnológica
y los principios Domain-Driven Design establecidos para
AURA Core.