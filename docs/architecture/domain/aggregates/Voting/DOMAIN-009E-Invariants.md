# DOMAIN-009E — Voting Invariants

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Voting Management

Aggregate:
Voting

Autor:
ARADA

Documentos relacionados:

- DOMAIN-009-Aggregate.md
- DOMAIN-009A-Lifecycle.md
- DOMAIN-009B-State-Machine.md
- DOMAIN-009C-Commands.md
- DOMAIN-009D-Domain-Events.md
- DOMAIN-009F-Permissions.md
- DOMAIN-009G-Repository-Contract.md
- DOMAIN-009I-Versioning.md
- DOMAIN-009J-Consistency-Boundary.md
- CORE-006-Domain-Invariants.md
- CORE-008-Aggregate-Design-Rules.md
- CORE-011-Repository-Contracts.md

---

# Objetivo

Definir formalmente las **Invariants** que deben mantenerse
verdaderas durante toda la vida del Aggregate **Voting**.

Una Invariant representa una condición del dominio que nunca puede
ser violada por una modificación válida del Aggregate.

Toda operación sobre Voting debe garantizar:

```text
Valid State Before Operation

↓

Domain Behavior

↓

Valid State After Operation
```

Una operación que produciría un estado inválido debe ser
rechazada.

Las Invariants protegen:

- identidad;
- propiedad organizacional;
- contexto;
- VotingType;
- VotingStatus;
- Rules;
- Options;
- Result;
- Lifecycle;
- coherencia temporal;
- Version;
- Consistency Boundary.

Este documento desarrolla exclusivamente las reglas ya establecidas
por el modelo conceptual, Lifecycle, State Machine, Commands y
Domain Events de Voting.

No introduce nuevos estados, transiciones, Commands, Events ni
capacidades del Aggregate.

---

# Principio Fundamental

Debe mantenerse siempre:

```text
Invariant Before Operation = true

↓

Operation

↓

Invariant After Operation = true
```

No existe una modificación válida cuando:

```text
Invariant After Operation = false
```

En dicho caso:

```text
Operation

↓

Rejected
```

---

# Responsabilidad

La Aggregate Root:

```text
Voting
```

es responsable de proteger sus Invariants.

La protección no puede delegarse exclusivamente a:

- Application;
- Repository;
- base de datos;
- UI;
- API;
- integración externa;
- Read Model.

Los componentes externos pueden realizar validaciones adicionales,
pero el Aggregate debe impedir por sí mismo alcanzar un estado
inválido.

---

# Alcance

Las Invariants de este documento protegen exclusivamente el
Aggregate:

```text
Voting
```

No definen las Invariants internas de:

```text
Organization

Citizen

Membership

Role

Territory

Assembly

Proposal

Participation

Document

Notification

Audit

Integration
```

Cada Aggregate mantiene sus propias reglas.

---

# Invariants Oficiales

La versión 1.0 establece como mínimo las siguientes Invariants:

- VotingId siempre existe;
- VotingId es único;
- VotingId nunca cambia;
- VotingId nunca se reutiliza para representar otro Voting;
- OrganizationId siempre existe;
- OrganizationId nunca cambia;
- VotingType siempre es válido;
- VotingStatus siempre pertenece al conjunto oficial de estados;
- Title debe ser válido;
- Rules deben ser válidas;
- Options deben ser coherentes con VotingType y Rules cuando
  correspondan;
- Voting comienza en Draft;
- toda transición debe pertenecer a la State Machine;
- Voting no puede abrirse si su configuración requerida es inválida;
- OpenedAt solamente puede establecerse mediante una apertura
  válida;
- Voting no puede cerrarse si no se encuentra Open;
- ClosedAt solamente puede establecerse mediante un cierre válido;
- ClosedAt no puede preceder a OpenedAt;
- CancelledAt solamente puede establecerse mediante una
  cancelación válida;
- ArchivedAt solamente puede establecerse mediante un archivado
  válido;
- Result debe corresponder a las Rules y condiciones válidas del
  proceso cuando exista;
- un Voting Closed no vuelve a Open mediante una operación
  ordinaria;
- un Voting Cancelled no vuelve a Draft ni Open;
- un Voting Archived no puede modificarse mediante Commands
  ordinarios;
- Archived es terminal;
- toda modificación válida incrementa Version;
- una operación rechazada no modifica Version;
- una operación rechazada no produce el Domain Event de éxito;
- ninguna operación modifica directamente otro Aggregate;
- las Invariants deben mantenerse antes y después de toda operación.

---

# Categorías

Las Invariants pueden comprenderse conceptualmente mediante las
siguientes categorías:

```text
Identity Invariants

Organization Invariants

Context Invariants

Configuration Invariants

Lifecycle Invariants

State Invariants

Temporal Invariants

Result Invariants

Version Invariants

Consistency Invariants
```

Esta clasificación organiza las reglas ya definidas.

No introduce responsabilidades adicionales.

---

# Invariants de Identidad

## VotingId Obligatorio

Todo Voting debe poseer:

```text
VotingId
```

No puede existir un Aggregate válido sin identidad.

Debe mantenerse:

```text
VotingId != null
```

---

# VotingId Único

VotingId debe identificar una única instancia conceptual de Voting.

No puede utilizarse el mismo VotingId para representar dos
procesos de Voting diferentes.

Conceptualmente:

```text
VotingId

↓

One Voting
```

---

# VotingId Inmutable

Una vez creado el Aggregate:

```text
VotingId = VOT-001
```

debe mantenerse durante toda su existencia:

```text
Draft

↓

Open

↓

Closed

↓

Archived
```

sin cambiar VotingId.

Igualmente en la ruta cancelada:

```text
Draft

↓

Cancelled

↓

Archived
```

VotingId permanece inmutable.

---

# No Reutilización de VotingId

Un Voting archivado conserva su identidad.

Por lo tanto, su VotingId no puede reutilizarse posteriormente para
representar otro proceso.

Debe mantenerse:

```text
Archived VotingId

≠

Reusable Identity
```

---

# Invariants Organizacionales

## OrganizationId Obligatorio

Todo Voting pertenece a una Organization.

Debe existir:

```text
OrganizationId
```

durante toda la vida del Aggregate.

No puede existir:

```text
Voting

without

OrganizationId
```

---

# OrganizationId Inmutable

OrganizationId queda establecido en la creación.

Debe mantenerse:

```text
OrganizationId Before

=

OrganizationId After
```

para toda modificación válida.

Voting no puede transferirse a otra Organization mediante una
operación ordinaria.

---

# Organization no Forma Parte del Aggregate

Voting mantiene:

```text
OrganizationId
```

No mantiene:

```text
Organization Aggregate
```

como estado interno.

La referencia organizacional no amplía el Consistency Boundary.

---

# Invariants de Contexto

Voting puede mantener:

```text
AssemblyId

ProposalId
```

cuando correspondan a su contexto.

Estas referencias:

- representan identidades externas;
- no convierten Assembly o Proposal en entidades internas;
- no permiten modificar esos Aggregates desde Voting;
- deben permanecer coherentes con el contexto definido por Voting.

La obligatoriedad de dichas referencias depende del contexto ya
establecido por el modelo.

---

# AssemblyId

Cuando Voting posea:

```text
AssemblyId
```

este valor representa exclusivamente la referencia a la Assembly
correspondiente.

No implica:

```text
Voting owns Assembly
```

ni permite:

```text
Voting

↓

Modify Assembly
```

---

# ProposalId

Cuando Voting posea:

```text
ProposalId
```

este valor representa exclusivamente la referencia a la Proposal
correspondiente.

No implica:

```text
Voting owns Proposal
```

ni permite modificar su estado interno.

---

# Invariants de VotingType

Todo Voting debe mantener un:

```text
VotingType
```

válido.

Debe cumplirse:

```text
VotingType ∈ Valid Voting Types
```

El conjunto formal de tipos pertenece al lenguaje ubicuo de Voting
Management.

Este documento no agrega nuevos VotingTypes.

---

# Cambio de VotingType

Cuando:

```text
ChangeVotingType
```

sea válido, debe mantenerse:

- NewVotingType válido;
- coherencia con Rules;
- coherencia con Options cuando correspondan;
- todas las demás Invariants;
- VotingStatus sin transición implícita.

No puede utilizarse ChangeVotingType para alterar:

```text
VotingId

OrganizationId

VotingStatus

Version
```

directamente.

---

# Invariants de Title

Todo Title debe cumplir las reglas descriptivas definidas por el
modelo.

Debe mantenerse:

```text
Valid Title
```

La modificación mediante:

```text
ChangeVotingTitle
```

solo puede producir un nuevo estado cuando NewTitle sea válido.

Title no constituye la identidad del Aggregate.

---

# Invariants de Description

Cuando Description exista o sea modificada mediante:

```text
ChangeVotingDescription
```

debe permanecer válida conforme a las reglas del Aggregate.

Description no puede utilizarse para alterar indirectamente:

```text
VotingId

OrganizationId

VotingStatus

Rules

Version
```

---

# Invariants de Rules

Voting debe mantener Rules válidas.

Debe cumplirse:

```text
Valid Voting Rules
```

durante toda operación que dependa de ellas.

Las Rules deben mantenerse coherentes con:

```text
VotingType

Options
```

cuando corresponda.

---

# Cambio de Rules

Una modificación mediante:

```text
ChangeVotingRules
```

solo puede aceptarse si el estado resultante conserva:

```text
Valid Rules

+

Valid VotingType

+

Valid Options
```

cuando estos conceptos correspondan al Voting.

Una modificación de Rules no produce por sí misma una transición
de Lifecycle.

---

# Rules no son Configuración Técnica

Rules representan reglas del proceso de Voting.

No deben utilizarse para almacenar:

```text
HTTP Configuration

Database Configuration

OAuth Tokens

JWT

Infrastructure Credentials

UI Configuration
```

Estos elementos permanecen fuera del dominio.

---

# Invariants de Options

Cuando Voting requiera Options, estas deben permanecer coherentes
con:

```text
VotingType

Rules
```

Debe mantenerse:

```text
Valid Options
```

antes y después de toda modificación.

---

# AddVotingOption

Una operación:

```text
AddVotingOption
```

solo puede aceptarse cuando:

- VotingOption es válida;
- VotingOption es compatible con VotingType;
- VotingOption es compatible con Rules;
- el estado permite la modificación;
- el conjunto resultante de Options permanece válido.

Si alguna condición falla:

```text
Rejected
```

---

# RemoveVotingOption

Una operación:

```text
RemoveVotingOption
```

solo puede aceptarse cuando:

- la VotingOption corresponde a una Option existente;
- el estado permite la modificación;
- las Options restantes permanecen válidas;
- VotingType permanece coherente;
- Rules permanecen coherentes.

No puede aceptarse una eliminación que deje Voting en un estado
inválido.

---

# Options no son Aggregates

Una VotingOption pertenece al Aggregate Voting cuando forma parte
de su configuración.

No adquiere por ello:

```text
Independent Aggregate Root

Independent Repository

Independent Version

Independent Consistency Boundary
```

---

# VotingStatus

VotingStatus debe contener exclusivamente uno de los estados
oficiales:

```text
Draft

Open

Closed

Cancelled

Archived
```

Debe cumplirse:

```text
VotingStatus ∈ {
    Draft,
    Open,
    Closed,
    Cancelled,
    Archived
}
```

No existe otro estado en la versión 1.0.

---

# Estado Inicial

Todo Voting recién creado debe comenzar en:

```text
Draft
```

No puede crearse directamente en:

```text
Open

Closed

Cancelled

Archived
```

---

# Protección de VotingStatus

VotingStatus no puede modificarse directamente.

Debe mantenerse:

```text
Command

↓

Voting Aggregate

↓

State Machine

↓

Valid Transition

↓

New VotingStatus
```

No:

```text
SetVotingStatus
```

como mecanismo de modificación directa.

---

# Invariants de State Machine

Toda transición debe pertenecer exactamente a:

```text
DOMAIN-009B-State-Machine.md
```

Las transiciones oficiales son:

```text
No Voting → Draft

Draft → Open

Draft → Cancelled

Open → Closed

Closed → Archived

Cancelled → Archived
```

Toda transición diferente debe ser rechazada.

---

# Draft

Cuando:

```text
VotingStatus = Draft
```

Voting existe formalmente pero todavía no se encuentra Open.

Desde Draft las únicas transiciones de Lifecycle permitidas son:

```text
Draft → Open

Draft → Cancelled
```

No puede producirse directamente:

```text
Draft → Closed

Draft → Archived
```

---

# Invariants de Apertura

Un Voting solamente puede abrirse desde:

```text
Draft
```

Debe mantenerse:

```text
VotingStatus = Draft
```

antes de ejecutar válidamente:

```text
OpenVoting
```

Además deben permanecer válidos los elementos requeridos por el
modelo:

```text
VotingType

Rules

Options
```

cuando correspondan.

Una apertura inválida debe ser rechazada.

---

# Apertura Válida

Una apertura válida produce:

```text
Draft

↓

OpenVoting

↓

Open
```

y debe establecer:

```text
OpenedAt
```

además de producir:

```text
VotingOpened
```

e incrementar Version.

---

# OpenedAt

OpenedAt solamente puede establecerse como consecuencia de una
apertura válida.

Debe mantenerse:

```text
VotingStatus = Draft

OpenedAt = null

↓

OpenVoting

↓

VotingStatus = Open

OpenedAt = T1
```

No puede modificarse arbitrariamente mediante otro Command.

---

# Open

Cuando:

```text
VotingStatus = Open
```

Voting representa un proceso formalmente abierto.

Desde Open la única transición definida por la versión 1.0 es:

```text
Open → Closed
```

No existen:

```text
Open → Draft

Open → Cancelled

Open → Archived
```

---

# Invariants de Cierre

Un Voting solamente puede cerrarse desde:

```text
Open
```

Debe mantenerse:

```text
VotingStatus = Open
```

antes de ejecutar válidamente:

```text
CloseVoting
```

Además:

- OpenedAt debe corresponder a una apertura válida;
- Rules deben permanecer válidas;
- las condiciones de cierre deben cumplirse;
- Result debe ser coherente cuando corresponda.

---

# Cierre Válido

Un cierre válido produce:

```text
Open

↓

CloseVoting

↓

Closed
```

y establece:

```text
ClosedAt
```

además de producir:

```text
VotingClosed
```

e incrementar Version.

---

# ClosedAt

ClosedAt solo puede establecerse mediante un cierre válido.

Cuando existan:

```text
OpenedAt

ClosedAt
```

debe cumplirse:

```text
ClosedAt >= OpenedAt
```

No puede existir un cierre temporalmente anterior a la apertura.

---

# Closed

Cuando:

```text
VotingStatus = Closed
```

Voting ha finalizado formalmente su flujo normal.

Desde Closed la única transición definida es:

```text
Closed → Archived
```

No existen:

```text
Closed → Draft

Closed → Open

Closed → Cancelled
```

---

# No Reapertura

La versión 1.0 no permite:

```text
Closed → Open
```

Por tanto:

```text
OpenVoting
```

sobre un Voting Closed debe ser rechazado.

No existe una operación ordinaria de reapertura.

---

# Invariants de Cancelación

La ruta de cancelación definida por la versión 1.0 es:

```text
Draft

↓

CancelVoting

↓

Cancelled
```

Debe cumplirse:

```text
VotingStatus = Draft
```

antes de una cancelación válida.

La versión 1.0 no permite:

```text
Open → Cancelled
```

---

# CancelledAt

CancelledAt solo puede establecerse como consecuencia de:

```text
CancelVoting
```

aceptado desde Draft.

Conceptualmente:

```text
VotingStatus = Draft

CancelledAt = null

↓

CancelVoting

↓

VotingStatus = Cancelled

CancelledAt = T1
```

---

# Cancelled

Cuando:

```text
VotingStatus = Cancelled
```

Voting terminó mediante la ruta alternativa de cancelación.

Desde Cancelled únicamente puede producirse:

```text
Cancelled → Archived
```

No puede regresar a:

```text
Draft

Open

Closed
```

---

# No Reactivación

La versión 1.0 no permite:

```text
Cancelled → Draft

Cancelled → Open
```

No existe una operación ordinaria para reactivar un Voting
Cancelled.

---

# Invariants de Archivado

ArchiveVoting solamente puede ejecutarse desde:

```text
Closed
```

o:

```text
Cancelled
```

Debe mantenerse:

```text
Closed → Archived
```

o:

```text
Cancelled → Archived
```

No puede archivarse directamente desde:

```text
Draft

Open
```

---

# ArchivedAt

ArchivedAt solo puede establecerse mediante una transición válida
hacia:

```text
Archived
```

Conceptualmente:

```text
Closed | Cancelled

↓

ArchiveVoting

↓

Archived

ArchivedAt = Tn
```

---

# Archived

Archived representa el estado histórico terminal.

Debe mantenerse:

```text
Archived

↓

No Lifecycle Transition
```

No existen:

```text
Archived → Draft

Archived → Open

Archived → Closed

Archived → Cancelled
```

---

# Inmutabilidad Operativa de Archived

Un Voting Archived no puede modificarse mediante Commands
ordinarios.

Debe preservar:

- VotingId;
- OrganizationId;
- contexto;
- VotingType;
- configuración histórica;
- Rules;
- Options;
- Result cuando exista;
- timestamps;
- Version.

Archivar no significa eliminar físicamente el Aggregate.

---

# No Desarchivado

La versión 1.0 no permite:

```text
Archived → Previous State
```

No existe un Command ordinario de desarchivado.

---

# Invariants Temporales

Los timestamps deben representar hechos reales del Lifecycle.

Debe mantenerse:

```text
CreatedAt
```

desde la creación.

Cuando ocurra apertura:

```text
OpenedAt
```

Cuando ocurra cierre:

```text
ClosedAt
```

Cuando ocurra cancelación:

```text
CancelledAt
```

Cuando ocurra archivado:

```text
ArchivedAt
```

Cada timestamp corresponde exclusivamente al hecho que representa.

---

# CreatedAt

CreatedAt queda establecido cuando Voting es creado.

Debe permanecer inmutable durante toda la vida del Aggregate.

---

# Coherencia Temporal del Flujo Normal

Cuando Voting siga:

```text
Draft

↓

Open

↓

Closed

↓

Archived
```

debe mantenerse:

```text
CreatedAt <= OpenedAt <= ClosedAt <= ArchivedAt
```

para los timestamps existentes.

---

# Coherencia Temporal del Flujo Cancelado

Cuando Voting siga:

```text
Draft

↓

Cancelled

↓

Archived
```

debe mantenerse:

```text
CreatedAt <= CancelledAt <= ArchivedAt
```

---

# Preservación Histórica de Timestamps

Una transición posterior no elimina timestamps de hechos
anteriores.

Ejemplo:

```text
OpenedAt = T1

ClosedAt = T2
```

después de archivar debe mantenerse:

```text
OpenedAt = T1

ClosedAt = T2

ArchivedAt = T3
```

---

# Invariants de Result

Result representa el resultado formal del proceso cuando
corresponda.

Debe mantenerse coherencia entre:

```text
VotingType

Rules

Options

VotingStatus

Result
```

Result no puede contradecir las Rules vigentes del proceso que lo
produce.

---

# Result y Cierre

Cuando el cierre requiera Result, este debe encontrarse en una
condición válida antes de confirmar:

```text
VotingClosed
```

Debe mantenerse:

```text
Valid Close Conditions

+

Valid Result when applicable

=

Valid CloseVoting
```

Si Result no es coherente con las Rules:

```text
CloseVoting

↓

Rejected
```

---

# Result no Modifica Otros Aggregates

El resultado de Voting no modifica directamente:

```text
Proposal

Assembly

Participation

Organization
```

Debe mantenerse:

```text
Voting Result

≠

External Aggregate Mutation
```

---

# Result no es VotingStatus

Result y VotingStatus representan conceptos diferentes.

Debe mantenerse:

```text
Result

≠

VotingStatus
```

La versión 1.0 no agrega estados derivados del resultado.

VotingStatus continúa limitado a:

```text
Draft

Open

Closed

Cancelled

Archived
```

---

# Invariants de Commands

Todo Command debe mantener las Invariants antes y después de su
ejecución.

Debe cumplirse:

```text
Command

↓

Validate Current State

Validate Command Data

Validate Invariants

↓

Execute or Reject
```

La existencia de un Command no garantiza que la operación sea
válida.

---

# Commands de Lifecycle

Los Commands de Lifecycle son:

```text
CreateVoting

OpenVoting

CloseVoting

CancelVoting

ArchiveVoting
```

Cada uno debe respetar exactamente las transiciones establecidas
por Lifecycle y State Machine.

---

# Commands de Configuración

Los Commands:

```text
ChangeVotingType

ChangeVotingTitle

ChangeVotingDescription

ChangeVotingRules

AddVotingOption

RemoveVotingOption
```

no producen por sí mismos una transición de Lifecycle.

Cuando sean válidos debe mantenerse:

```text
VotingStatus Before

=

VotingStatus After
```

---

# Command Rechazado

Cuando un Command viola una Invariant:

```text
Command

↓

Rejected
```

Debe preservarse:

```text
State = Previous State

Version = Previous Version
```

y no debe producirse el Domain Event de éxito correspondiente.

---

# Invariants de Domain Events

Todo Domain Event debe representar una modificación válida ya
aceptada por Voting.

Debe mantenerse:

```text
Valid Domain Change

↓

Domain Event
```

No:

```text
Rejected Change

↓

Success Domain Event
```

---

# Correspondencia Command / Event

Debe mantenerse:

```text
CreateVoting
→ VotingCreated

OpenVoting
→ VotingOpened

CloseVoting
→ VotingClosed

CancelVoting
→ VotingCancelled

ArchiveVoting
→ VotingArchived

ChangeVotingType
→ VotingTypeChanged

ChangeVotingTitle
→ VotingTitleChanged

ChangeVotingDescription
→ VotingDescriptionChanged

ChangeVotingRules
→ VotingRulesChanged

AddVotingOption
→ VotingOptionAdded

RemoveVotingOption
→ VotingOptionRemoved
```

Un Event no puede representar una operación que fue rechazada.

---

# Invariants de Version

Voting mantiene:

```text
Version
```

como parte de su estado.

Toda modificación válida debe producir:

```text
Version N

↓

Valid Modification

↓

Version N + 1
```

Version no puede:

- disminuir;
- reutilizarse para otra modificación;
- modificarse directamente mediante Commands;
- cambiar como consecuencia de una lectura.

---

# Command Rechazado y Version

Cuando una operación es rechazada:

```text
Version Before

=

Version After
```

No existe incremento de Version.

---

# Domain Event y Version

Todo Domain Event producido por una modificación válida debe
corresponder a la nueva:

```text
AggregateVersion
```

Conceptualmente:

```text
Version = N

↓

Valid Command

↓

Version = N + 1

↓

DomainEvent.AggregateVersion = N + 1
```

---

# Concurrencia

Las Invariants deben evaluarse sobre el estado actual de Voting.

Una modificación basada en una Version obsoleta no puede
sobrescribir silenciosamente una modificación ya confirmada.

El control detallado pertenece a:

```text
DOMAIN-009I-Versioning.md

DOMAIN-009G-Repository-Contract.md
```

---

# Invariants de Consistencia

Voting constituye un Consistency Boundary independiente.

Toda operación válida debe finalizar con:

```text
One Voting

+

Valid Internal State

+

Valid Version
```

No debe existir una actualización parcial que deje el Aggregate en
un estado inválido.

---

# Atomicidad Conceptual

Una modificación válida debe preservar conjuntamente los elementos
afectados.

Ejemplo de apertura:

```text
VotingStatus = Open

OpenedAt = T1

Version = N + 1

VotingOpened
```

Estos elementos representan una misma modificación lógica.

No debe confirmarse únicamente una parte dejando un estado
incoherente.

---

# Aggregate Root

Toda modificación debe realizarse mediante:

```text
Voting
```

como Aggregate Root.

No está permitido:

```text
Direct Property Mutation
```

ni:

```text
Direct VotingStatus Mutation
```

ni:

```text
Direct Version Mutation
```

---

# No Setters Públicos

No se permite modificar directamente:

```text
VotingId

OrganizationId

VotingStatus

Version

OpenedAt

ClosedAt

CancelledAt

ArchivedAt

Result
```

Estos valores se encuentran protegidos por comportamiento del
Aggregate.

---

# Invariants entre Aggregates

Voting no puede modificar directamente:

```text
Organization

Citizen

Membership

Role

Territory

Assembly

Proposal

Participation

Document

Notification

Audit

Integration
```

Las Invariants externas permanecen bajo sus respectivos
Aggregates.

---

# Voting y Assembly

Voting puede mantener:

```text
AssemblyId
```

pero no controla:

```text
AssemblyStatus
```

Una transición de Voting no puede utilizarse para producir
directamente una transición de Assembly.

---

# Voting y Proposal

Voting puede mantener:

```text
ProposalId
```

pero no controla:

```text
ProposalStatus
```

El resultado o cierre de Voting no modifica directamente Proposal.

---

# Voting y Participation

Voting representa el proceso formal.

Participation representa la participación individual.

Debe mantenerse:

```text
Voting

≠

Participation
```

Voting no incorpora Participations como entidades internas para
expandir su Consistency Boundary.

---

# Voting y Citizen

Voting no mantiene Citizens completos como parte de su estado.

Debe mantenerse la separación entre:

```text
Citizen Identity

Voting Process
```

La participación individual permanece fuera del Aggregate Voting.

---

# Voting y Membership

Voting no modifica Membership.

Las condiciones externas relacionadas con pertenencia no convierten
Membership en estado interno de Voting.

---

# Voting y Role

Voting no modifica Role.

Las condiciones de autorización no convierten Role en parte del
Consistency Boundary.

---

# Voting y Document

Voting no administra el contenido ni Lifecycle de Document.

Cuando exista una relación documental, Document mantiene su propio
Aggregate.

---

# Voting y Notification

Voting no envía Notifications directamente.

Un Domain Event puede ser observado posteriormente por el contexto
correspondiente.

Esto no modifica las Invariants internas de Voting.

---

# Voting y Audit

Voting no mantiene Audit como entidad interna.

Los Domain Events pueden aportar hechos al contexto de Audit.

Audit no modifica las Invariants de Voting.

---

# Voting e Integration

Voting no ejecuta directamente integraciones externas.

Los procesos de Integration permanecen fuera del Aggregate.

Las Invariants de Voting no dependen de que una integración externa
se encuentre disponible.

---

# Permissions e Invariants

La autorización determina quién puede intentar una operación.

Las Invariants determinan si el estado resultante es válido.

Debe mantenerse:

```text
Permission Granted

≠

Invariant Bypass
```

Un actor autorizado puede recibir:

```text
Rejected
```

cuando la operación violaría una Invariant.

---

# Repository e Invariants

El Repository persiste el Aggregate.

No redefine las Invariants.

Debe mantenerse:

```text
Voting

↓

Valid Domain State

↓

Repository
```

No:

```text
Repository

↓

Bypass Aggregate Rules
```

---

# Rehidratación

La recuperación de Voting desde persistencia debe reconstruir un
estado que respete las Invariants correspondientes al estado
persistido.

La rehidratación no constituye una nueva operación del dominio.

Por lo tanto no debe:

- cambiar VotingStatus;
- incrementar Version;
- modificar timestamps;
- generar nuevos Domain Events.

---

# Read Models

Los Read Models no modifican Voting.

Una proyección no puede utilizarse para evitar las Invariants del
Write Model.

Debe mantenerse:

```text
Read Model

=

Derived Representation
```

y no:

```text
Read Model

=

Aggregate Mutation Authority
```

---

# Persistencia Parcial

No debe persistirse una modificación parcial que deje incoherencia
entre:

```text
VotingStatus

Lifecycle Timestamps

Rules

Options

Result

Version
```

cuando estos elementos sean afectados por la misma operación
válida.

---

# Estado Siempre Válido

Al finalizar cualquier operación aceptada debe cumplirse:

```text
VotingId valid

OrganizationId valid

VotingType valid

VotingStatus valid

Rules valid

Options valid when applicable

Result valid when applicable

Temporal State coherent

Version coherent
```

El Aggregate no puede permanecer temporalmente persistido en un
estado inválido.

---

# Matriz de Invariants por Estado

| Estado | Condición fundamental |
| --- | --- |
| Draft | Voting existe y aún no está Open |
| Open | apertura válida y OpenedAt existente |
| Closed | cierre válido y ClosedAt coherente con OpenedAt |
| Cancelled | cancelación válida y CancelledAt existente |
| Archived | archivado válido, ArchivedAt existente y estado terminal |

---

# Matriz de Transiciones

| Origen | Destino | Invariant |
| --- | --- | --- |
| No existe | Draft | creación válida |
| Draft | Open | configuración e Invariants de apertura válidas |
| Draft | Cancelled | cancelación válida |
| Open | Closed | Invariants de cierre válidas |
| Closed | Archived | archivado válido |
| Cancelled | Archived | archivado válido |

Toda transición no incluida debe ser rechazada.

---

# Matriz de Timestamps

| Hecho | Timestamp |
| --- | --- |
| VotingCreated | CreatedAt |
| VotingOpened | OpenedAt |
| VotingClosed | ClosedAt |
| VotingCancelled | CancelledAt |
| VotingArchived | ArchivedAt |

Un timestamp de Lifecycle solamente puede establecerse mediante el
hecho correspondiente.

---

# Matriz de Modificaciones de Configuración

| Command | Elemento protegido | VotingStatus |
| --- | --- | --- |
| ChangeVotingType | VotingType | permanece |
| ChangeVotingTitle | Title | permanece |
| ChangeVotingDescription | Description | permanece |
| ChangeVotingRules | Rules | permanece |
| AddVotingOption | Options | permanece |
| RemoveVotingOption | Options | permanece |

La operación solamente es válida cuando todas las Invariants
correspondientes permanecen verdaderas.

---

# Violación de Invariant

Cuando una Invariant sería violada:

```text
Operation

↓

Invariant Violation

↓

Rejected
```

Debe preservarse:

```text
Previous State

Previous Version
```

No se produce el Domain Event de éxito.

---

# Restricciones

No está permitido:

- crear Voting sin VotingId;
- reutilizar VotingId;
- modificar VotingId;
- crear Voting sin OrganizationId;
- modificar OrganizationId;
- mantener un VotingType inválido;
- mantener un VotingStatus fuera del conjunto oficial;
- modificar VotingStatus directamente;
- crear Voting directamente en Open;
- crear Voting directamente en Closed;
- crear Voting directamente en Cancelled;
- crear Voting directamente en Archived;
- abrir Voting desde un estado distinto de Draft;
- abrir Voting con configuración inválida;
- cerrar Voting desde un estado distinto de Open;
- establecer ClosedAt antes de OpenedAt;
- cancelar Voting desde un estado distinto de Draft en la versión
  1.0;
- archivar Voting desde Draft;
- archivar Voting desde Open;
- reabrir un Voting Closed;
- reactivar un Voting Cancelled;
- desarchivar un Voting Archived;
- modificar un Voting Archived mediante Commands ordinarios;
- mantener Rules inválidas;
- mantener Options incompatibles con VotingType o Rules cuando
  correspondan;
- aceptar Result incompatible con las Rules;
- utilizar Result como VotingStatus;
- modificar Version directamente;
- incrementar Version ante una operación rechazada;
- generar Domain Events de éxito ante una operación rechazada;
- modificar directamente otro Aggregate;
- incorporar Aggregates externos completos dentro de Voting;
- utilizar Repository para evitar las Invariants;
- utilizar Permissions para evitar las Invariants;
- utilizar Read Models para modificar el Aggregate;
- persistir parcialmente una modificación dejando Voting en estado
  inválido.

---

# Reglas

## REG-001

VotingId siempre debe existir.

---

## REG-002

VotingId es único, inmutable y no reutilizable.

---

## REG-003

OrganizationId siempre debe existir y permanecer inmutable.

---

## REG-004

VotingType siempre debe ser válido.

---

## REG-005

VotingStatus solamente puede contener:

```text
Draft

Open

Closed

Cancelled

Archived
```

---

## REG-006

Todo Voting comienza en Draft.

---

## REG-007

VotingStatus solamente puede cambiar mediante una transición
definida por la State Machine.

---

## REG-008

Draft solamente puede evolucionar hacia Open o Cancelled dentro del
Lifecycle versión 1.0.

---

## REG-009

Open solamente puede evolucionar hacia Closed.

---

## REG-010

Closed solamente puede evolucionar hacia Archived.

---

## REG-011

Cancelled solamente puede evolucionar hacia Archived.

---

## REG-012

Archived es terminal y no admite Commands ordinarios de
modificación.

---

## REG-013

OpenedAt solamente puede establecerse mediante una apertura válida.

---

## REG-014

ClosedAt solamente puede establecerse mediante un cierre válido y
no puede preceder a OpenedAt.

---

## REG-015

CancelledAt solamente puede establecerse mediante una cancelación
válida.

---

## REG-016

ArchivedAt solamente puede establecerse mediante un archivado
válido.

---

## REG-017

Rules deben permanecer válidas durante toda operación aceptada.

---

## REG-018

Options deben permanecer coherentes con VotingType y Rules cuando
correspondan.

---

## REG-019

Result debe permanecer coherente con las Rules y condiciones
válidas del Voting cuando exista.

---

## REG-020

Toda modificación válida incrementa Version.

---

## REG-021

Una operación rechazada no modifica estado ni Version.

---

## REG-022

Una operación rechazada no produce el Domain Event de éxito
correspondiente.

---

## REG-023

Ninguna operación de Voting puede modificar directamente otro
Aggregate.

---

## REG-024

Toda Invariant debe ser verdadera antes y después de cada operación
válida del Aggregate.

---

# Compatibilidad con Lifecycle

Las Invariants deben mantener coherencia permanente con:

```text
DOMAIN-009A-Lifecycle.md
```

No pueden permitir una transición inexistente en dicho Lifecycle.

---

# Compatibilidad con State Machine

Las Invariants deben mantener coherencia permanente con:

```text
DOMAIN-009B-State-Machine.md
```

Debe mantenerse:

```text
Valid State Machine Transition

+

Valid Invariants

=

Valid State Change
```

Una transición permitida por estructura continúa siendo rechazada
si una Invariant aplicable no se cumple.

---

# Compatibilidad con Commands

Los Commands definidos en:

```text
DOMAIN-009C-Commands.md
```

deben respetar todas las Invariants aplicables.

Ningún Command constituye una excepción.

---

# Compatibilidad con Domain Events

Los Domain Events definidos en:

```text
DOMAIN-009D-Domain-Events.md
```

solo pueden producirse después de una modificación válida.

Todo evento debe representar un estado que respete las Invariants.

---

# Compatibilidad con Versioning

Las Invariants de modificación deben preservar:

```text
Valid Change

↓

Version + 1
```

El comportamiento completo se desarrolla en:

```text
DOMAIN-009I-Versioning.md
```

---

# Compatibilidad con Consistency Boundary

Todas las Invariants internas deben protegerse dentro del límite:

```text
Voting
```

sin incorporar otros Aggregates.

La definición formal se desarrolla en:

```text
DOMAIN-009J-Consistency-Boundary.md
```

---

# Definición de Éxito

Las Invariants del Aggregate **Voting** garantizan que toda
instancia permanezca conceptualmente válida durante toda su
existencia.

El modelo protege:

- VotingId único e inmutable;
- OrganizationId obligatorio e inmutable;
- referencias externas sin absorción de Aggregates;
- VotingType válido;
- VotingStatus válido;
- Title válido;
- Rules válidas;
- Options coherentes;
- Result coherente cuando corresponda;
- Lifecycle oficial;
- State Machine oficial;
- timestamps coherentes;
- Archived como estado terminal;
- Version monotónica ante modificaciones válidas;
- ausencia de cambios ante operaciones rechazadas;
- Domain Events coherentes;
- independencia de otros Aggregates;
- Consistency Boundary propio.

Toda modificación debe comenzar y terminar con:

```text
Valid Voting
```

Si una operación produciría:

```text
Invalid Voting
```

debe ser rechazada sin modificar estado, Version ni generar el
Domain Event de éxito.

De esta forma, `DOMAIN-009E-Invariants.md` establece las reglas
conceptuales que deben permanecer siempre verdaderas dentro del
Aggregate **Voting**, manteniendo íntegramente el patrón consolidado
de AURA Core.