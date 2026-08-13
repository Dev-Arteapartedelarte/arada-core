# DOMAIN-009J — Voting Consistency Boundary

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
- DOMAIN-009E-Invariants.md
- DOMAIN-009F-Permissions.md
- DOMAIN-009G-Repository-Contract.md
- DOMAIN-009I-Versioning.md
- DOMAIN-009K-Integration-Events.md
- DOMAIN-009L-Read-Model.md
- CORE-006-Domain-Invariants.md
- CORE-008-Aggregate-Design-Rules.md
- CORE-011-Repository-Contracts.md
- CORE-016-Dependency-Rules.md

---

# Objetivo

Definir formalmente el **Consistency Boundary** del Aggregate
**Voting**.

El Consistency Boundary establece qué conceptos deben permanecer
consistentes de forma conjunta cuando Voting ejecuta una
modificación válida.

Voting constituye una unidad independiente de consistencia.

Dentro de este límite:

- existe una única Aggregate Root;
- las Invariants se preservan inmediatamente;
- las modificaciones deben producir un estado completo y válido;
- el Lifecycle permanece coherente;
- la State Machine permanece coherente;
- los Value Objects permanecen válidos;
- las entidades internas, cuando existan, se modifican
  exclusivamente mediante Voting;
- Version se actualiza de forma consistente;
- los Domain Events representan hechos producidos por cambios
  válidos.

Fuera del límite:

- los demás Aggregates conservan su propia consistencia;
- las relaciones utilizan identificadores;
- no existe modificación directa del estado interno de otro
  Aggregate;
- la coordinación ocurre mediante los contratos ya definidos por
  AURA.

---

# Principios

El Consistency Boundary de Voting cumple los siguientes principios:

- Voting constituye una única unidad de consistencia;
- Voting es la única Aggregate Root;
- toda modificación interna pasa por Voting;
- ninguna operación puede dejar Voting parcialmente actualizado;
- las Invariants deben mantenerse antes y después de toda
  modificación válida;
- VotingId permanece inmutable;
- OrganizationId permanece inmutable;
- VotingStatus permanece protegido por la State Machine;
- Rules y Options permanecen coherentes;
- Result permanece coherente cuando corresponda;
- los timestamps del Lifecycle permanecen coherentes;
- Version representa la evolución del Aggregate;
- los Aggregates externos permanecen fuera del límite;
- las referencias externas utilizan identificadores;
- Voting no modifica directamente otro Aggregate;
- la consistencia interna es inmediata;
- la coordinación con otros Aggregates permanece separada del
  cambio interno de Voting.

---

# Aggregate como Consistency Boundary

El límite de consistencia está centrado exclusivamente en:

```text
Voting
```

Conceptualmente:

```text
┌─────────────────────────────────┐
│      Voting Consistency         │
│          Boundary               │
│                                 │
│            Voting               │
│              │                  │
│              ├── Internal State │
│              ├── Value Objects  │
│              ├── Internal       │
│              │   Entities       │
│              └── Version        │
│                                 │
└─────────────────────────────────┘
```

Todo elemento realmente perteneciente a Voting se encuentra
protegido por la Aggregate Root.

---

# Dentro del Boundary

El Consistency Boundary comprende conceptualmente el estado propio
de Voting:

```text
VotingId

OrganizationId

AssemblyId

ProposalId

VotingType

Title

Description

VotingStatus

Rules

Options

Result

OpenedAt

ClosedAt

CancelledAt

ArchivedAt

Version

CreatedAt

UpdatedAt
```

cuando dichos elementos correspondan al estado del Aggregate.

También comprende:

```text
Value Objects

Internal Entities
```

que formen parte legítima de Voting.

Estos conceptos no poseen autoridad independiente para modificar el
Aggregate.

---

# Fuera del Boundary

No forman parte del Consistency Boundary de Voting:

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

Estos conceptos pueden mantener relaciones con Voting.

Sin embargo, conservan:

- identidad propia;
- Lifecycle propio;
- State Machine propia cuando corresponda;
- Invariants propias;
- Version propia;
- Repository propio;
- Consistency Boundary propio.

---

# Regla de No Absorción

La existencia de una relación de dominio no convierte otro
Aggregate en parte de Voting.

No debe interpretarse:

```text
Voting
   │
   ├── Organization
   ├── Assembly
   ├── Proposal
   └── Participation
```

como composición interna.

Debe mantenerse conceptualmente:

```text
Voting
   │
   ├── OrganizationId
   ├── AssemblyId
   └── ProposalId
```

cuando las referencias correspondan.

Participation conserva su propia identidad y puede relacionarse con
Voting mediante VotingId desde el contexto correspondiente.

---

# Aggregate Root

La única Aggregate Root dentro del límite es:

```text
Voting
```

Toda modificación debe pasar por su comportamiento.

No está permitido modificar directamente:

```text
VotingStatus

VotingType

Rules

Options

Result

Lifecycle Timestamps

Version
```

evitando la Aggregate Root.

Debe mantenerse:

```text
Command

↓

Voting

↓

Validate State

Validate Invariants

↓

Valid Internal Modification
```

---

# Consistencia Interna

La consistencia dentro de Voting es inmediata.

Después de una operación válida:

```text
Voting
```

debe encontrarse completamente en un estado válido.

Debe mantenerse:

```text
Valid State Before

↓

Valid Domain Operation

↓

Valid State After
```

No puede existir como resultado confirmado:

```text
Partially Valid Voting
```

---

# Atomicidad Conceptual

Una modificación de Voting constituye una única modificación lógica
del Aggregate.

Por ejemplo, una apertura válida requiere coherencia conjunta entre:

```text
VotingStatus = Open

OpenedAt = T1

Version = N + 1

VotingOpened
```

No debe considerarse válida una modificación que confirme
únicamente una parte de ese cambio lógico.

Igualmente, un cierre válido debe mantener coherencia entre:

```text
VotingStatus = Closed

ClosedAt

Result when applicable

Version

VotingClosed
```

según las reglas definidas por el Aggregate.

---

# Identidad

VotingId pertenece al Consistency Boundary.

Debe mantenerse:

```text
VotingId Before

=

VotingId After
```

para toda operación durante la vida del Aggregate.

Ningún componente interno ni externo puede utilizar una operación
de Voting para sustituir su identidad.

---

# Contexto Organizacional

OrganizationId pertenece al estado de Voting y forma parte de su
consistencia interna.

Debe mantenerse:

```text
OrganizationId Before

=

OrganizationId After
```

La Organization completa permanece fuera del Boundary.

Conceptualmente:

```text
Organization
      │
      │ OrganizationId
      ▼
    Voting
```

Voting conoce la referencia.

No administra el Aggregate Organization.

---

# Contexto de Assembly

Cuando Voting posea:

```text
AssemblyId
```

la referencia forma parte del estado consistente de Voting.

Assembly permanece fuera del Boundary.

Debe mantenerse:

```text
AssemblyId

≠

Assembly Aggregate
```

Una modificación de Voting no incluye una modificación interna de
Assembly.

---

# Contexto de Proposal

Cuando Voting posea:

```text
ProposalId
```

la referencia pertenece al contexto de Voting.

Proposal permanece fuera del Boundary.

Debe mantenerse:

```text
ProposalId

≠

Proposal Aggregate
```

Cerrar Voting no modifica directamente Proposal.

---

# VotingType

VotingType forma parte del estado consistente del Aggregate.

Una modificación válida mediante:

```text
ChangeVotingType
```

debe preservar conjuntamente:

```text
Valid VotingType

Valid Rules

Valid Options when applicable

Valid Invariants

Version
```

VotingStatus no cambia por el solo hecho de modificar VotingType.

---

# Rules

Rules forman parte del Consistency Boundary porque sus valores
pueden determinar la validez del propio Voting.

Toda modificación válida debe asegurar:

```text
Valid Rules
```

y mantener coherencia con:

```text
VotingType

Options
```

cuando corresponda.

No puede confirmarse una modificación de Rules que deje Voting en
un estado inválido.

---

# Options

Las Options pertenecen al Boundary cuando forman parte de la
configuración del Voting.

Las operaciones:

```text
AddVotingOption

RemoveVotingOption
```

deben modificar las Options exclusivamente mediante Voting.

No debe existir:

```text
VotingOption Repository
```

como mecanismo para evitar las Invariants del Aggregate dentro del
modelo versión 1.0.

La Option permanece bajo la consistencia de Voting.

---

# Result

Result pertenece al Consistency Boundary de Voting cuando
corresponda.

Debe mantenerse coherencia entre:

```text
VotingType

Rules

Options

VotingStatus

Result
```

Result no constituye un Aggregate separado.

Tampoco permite ampliar el Boundary hacia Proposal, Assembly o
Participation.

Debe mantenerse:

```text
Voting Result

≠

External Aggregate Mutation
```

---

# Lifecycle

El Lifecycle pertenece al estado interno de Voting.

Los estados oficiales son:

```text
Draft

Open

Closed

Cancelled

Archived
```

Toda transición debe ocurrir completamente dentro del Consistency
Boundary.

Debe mantenerse:

```text
Current VotingStatus

↓

Valid Command

↓

State Machine

↓

Invariant Validation

↓

New VotingStatus
```

La transición no incluye cambios atómicos en otros Aggregates.

---

# State Machine

La State Machine controla exclusivamente:

```text
VotingStatus
```

dentro de Voting.

Las transiciones oficiales permanecen:

```text
No Voting → Draft

Draft → Open

Draft → Cancelled

Open → Closed

Closed → Archived

Cancelled → Archived
```

Una transición de Voting no constituye una transición de:

```text
Assembly

Proposal

Participation

Organization
```

---

# Lifecycle Timestamps

Los timestamps relacionados con transiciones pertenecen al
Consistency Boundary.

Debe preservarse la relación:

```text
VotingCreated
→ CreatedAt
```

```text
VotingOpened
→ OpenedAt
```

```text
VotingClosed
→ ClosedAt
```

```text
VotingCancelled
→ CancelledAt
```

```text
VotingArchived
→ ArchivedAt
```

Cuando una operación afecta estado y timestamp, ambos forman parte
del mismo cambio lógico de Voting.

---

# Invariants

Las Invariants deben ser protegidas íntegramente dentro del
Boundary.

Debe mantenerse:

```text
Voting

↓

Protect Invariants
```

No:

```text
External Component

↓

Responsible for Aggregate Validity
```

El dominio puede recibir información o validaciones externas cuando
corresponda, pero Voting conserva la responsabilidad de no aceptar
un estado interno inválido.

Las reglas completas pertenecen a:

```text
DOMAIN-009E-Invariants.md
```

---

# Commands

Los Commands representan intenciones dirigidas a Voting.

Conceptualmente:

```text
Command

↓

Voting Aggregate

↓

Consistency Boundary
```

Un Command de Voting no puede modificar directamente un Aggregate
externo.

Por ejemplo:

```text
CloseVoting
```

puede modificar dentro de Voting:

```text
VotingStatus

ClosedAt

Result when applicable

Version
```

pero no puede modificar directamente:

```text
ProposalStatus

AssemblyStatus

ParticipationStatus
```

---

# Domain Events

Los Domain Events representan hechos ocurridos como consecuencia de
modificaciones válidas dentro del Boundary.

Conceptualmente:

```text
Voting

↓

Valid Modification

↓

Domain Event
```

Un Domain Event puede comunicar posteriormente un hecho fuera del
Boundary.

La existencia del evento no amplía la modificación interna original
hacia otros Aggregates.

---

# Ejemplo de Apertura

Estado inicial:

```text
VotingStatus = Draft

Version = N
```

Command:

```text
OpenVoting
```

Dentro del Boundary:

```text
Validate State

Validate Rules

Validate Options when applicable

Validate Invariants

↓

VotingStatus = Open

OpenedAt = T1

Version = N + 1

VotingOpened
```

Fuera del Boundary no se modifica directamente:

```text
Assembly

Proposal

Participation

Organization
```

---

# Ejemplo de Cierre

Estado inicial:

```text
VotingStatus = Open

Version = N
```

Command:

```text
CloseVoting
```

Dentro del Boundary:

```text
Validate State

Validate Rules

Validate Result when applicable

Validate Invariants

↓

VotingStatus = Closed

ClosedAt = T2

Result when applicable

Version = N + 1

VotingClosed
```

No forma parte de la misma modificación interna:

```text
Proposal State Change

Assembly State Change

Participation State Change
```

---

# Ejemplo de Cancelación

Estado:

```text
VotingStatus = Draft
```

Command:

```text
CancelVoting
```

Dentro del Boundary:

```text
VotingStatus = Cancelled

CancelledAt = T1

Version = N + 1

VotingCancelled
```

Cancelar Voting no cancela directamente otro Aggregate.

---

# Ejemplo de Archivado

Estado:

```text
VotingStatus = Closed
```

o:

```text
VotingStatus = Cancelled
```

Command:

```text
ArchiveVoting
```

Dentro del Boundary:

```text
VotingStatus = Archived

ArchivedAt

Version = N + 1

VotingArchived
```

Archived mantiene el mismo Consistency Boundary.

Archivar no elimina ni modifica los Aggregates relacionados.

---

# Repository

VotingRepository persiste el Consistency Boundary como una unidad.

Conceptualmente:

```text
Voting

↓

VotingRepository

↓

Persist Voting as one consistency unit
```

No deben existir operaciones de persistencia independientes que
permitan modificar directamente:

```text
VotingStatus

Rules

Options

Result

Version
```

evitando el comportamiento del Aggregate.

La definición formal pertenece a:

```text
DOMAIN-009G-Repository-Contract.md
```

---

# Persistencia Completa

La persistencia debe preservar conjuntamente el estado necesario
para reconstruir un Voting válido.

Conceptualmente:

```text
Voting

   │
   ├── Identity
   ├── Organization Context
   ├── Voting Context
   ├── Configuration
   ├── Lifecycle State
   ├── Rules
   ├── Options
   ├── Result
   ├── Timestamps
   └── Version
```

cuando dichos elementos correspondan.

No se permite una persistencia parcial que viole las Invariants.

---

# Versioning

Version pertenece al Consistency Boundary.

Toda modificación válida debe mantener:

```text
Version N

↓

Valid Aggregate Modification

↓

Version N + 1
```

El nuevo estado interno y su nueva Version deben corresponder a la
misma modificación lógica.

Una operación rechazada mantiene:

```text
Version = Previous Version
```

---

# Concurrencia

El control de concurrencia protege el Consistency Boundary
completo.

Una modificación calculada sobre una Version obsoleta no puede
sobrescribir silenciosamente un estado más reciente.

Debe mantenerse:

```text
ExpectedVersion

=

PersistedVersion
```

para confirmar la escritura correspondiente.

Cuando:

```text
ExpectedVersion

!=

PersistedVersion
```

la modificación debe ser rechazada conforme al modelo de
Versioning.

---

# Consistencia con Organization

Voting pertenece a una Organization mediante:

```text
OrganizationId
```

Organization permanece fuera del Consistency Boundary.

Por lo tanto:

```text
Modify Voting

≠

Modify Organization
```

La consistencia interna de Organization corresponde a su propio
Aggregate.

---

# Consistencia con Assembly

Cuando Voting mantiene:

```text
AssemblyId
```

Assembly permanece fuera del Boundary.

Debe mantenerse:

```text
Voting Transition

≠

Assembly Transition
```

Por ejemplo:

```text
VotingOpened
```

no modifica directamente:

```text
AssemblyStatus
```

---

# Consistencia con Proposal

Cuando Voting mantiene:

```text
ProposalId
```

Proposal permanece fuera del Boundary.

Debe mantenerse:

```text
VotingClosed

≠

Direct Proposal State Change
```

Cualquier reacción posterior debe respetar la autoridad del
Aggregate Proposal.

---

# Consistencia con Participation

Participation representa la participación individual y posee su
propio Consistency Boundary.

Debe mantenerse:

```text
Voting

≠

Participation
```

Una transición:

```text
Voting Open → Closed
```

no implica una modificación interna automática de Participation.

Cada Aggregate preserva sus propias Invariants.

---

# Consistencia con Citizen

Citizen permanece fuera del Consistency Boundary.

Voting no incorpora:

```text
Citizen Aggregate
```

dentro de su estado.

La existencia de participantes no transforma Citizen en entidad
interna de Voting.

---

# Consistencia con Membership

Membership permanece fuera del Consistency Boundary.

Voting no modifica:

```text
MembershipStatus
```

ni administra su Lifecycle.

Las relaciones de pertenencia permanecen bajo el Aggregate
Membership.

---

# Consistencia con Role

Role permanece fuera del Consistency Boundary.

La existencia de Permissions o reglas relacionadas con Roles no
convierte Role en estado interno de Voting.

Debe mantenerse:

```text
Voting Boundary

≠

Role Boundary
```

---

# Consistencia con Territory

Territory permanece fuera del Consistency Boundary.

Voting no administra:

- geometría;
- jerarquía;
- límites;
- clasificación;
- Lifecycle territorial.

Cualquier contexto territorial permanece bajo los contratos de
dominio correspondientes.

---

# Consistencia con Document

Document conserva su propio Consistency Boundary.

Voting puede mantener una relación documental cuando corresponda,
pero no modifica directamente:

```text
Document State

Document Content

Document Version
```

desde su Aggregate.

---

# Consistencia con Notification

Notification permanece fuera del Boundary.

Un hecho como:

```text
VotingOpened
```

puede ser utilizado posteriormente por el contexto correspondiente.

Sin embargo:

```text
VotingOpened

≠

Notification Internal Mutation
```

Voting no envía ni modifica directamente Notifications.

---

# Consistencia con Audit

Audit permanece fuera del Consistency Boundary.

Los hechos de Voting pueden aportar información posteriormente al
contexto de Audit.

La generación de trazabilidad no convierte Audit en una entidad
interna de Voting.

---

# Consistencia con Integration

Integration permanece fuera del Boundary.

Voting produce hechos de dominio.

Los contratos de integración pueden comunicar posteriormente
hechos seleccionados.

Debe mantenerse:

```text
Voting Domain Change

↓

Domain Event

↓

Integration Event when applicable
```

sin incorporar Integration dentro del Aggregate.

---

# Consistencia entre Aggregates

La consistencia inmediata pertenece al interior de Voting.

Conceptualmente:

```text
Inside Voting

=

Immediate Consistency
```

Cuando un hecho de Voting requiera posteriormente coordinación con
otro Aggregate:

```text
Voting

↓

Confirmed Domain Fact

↓

External Coordination
```

el Aggregate externo conserva su propia autoridad sobre cualquier
modificación posterior.

Debe mantenerse:

```text
One Aggregate

=

One Consistency Boundary
```

---

# Domain Events y Consistencia entre Aggregates

Los Domain Events permiten expresar que un hecho ocurrió dentro de
Voting sin ampliar su Consistency Boundary.

Ejemplo:

```text
VotingClosed

↓

External Reaction
```

El evento comunica el hecho.

No otorga a Voting autoridad para modificar directamente el estado
del consumidor.

---

# Integration Events y Boundary

Los Integration Events pertenecen a la comunicación fuera del
modelo interno de Voting.

Debe mantenerse:

```text
Domain Event

≠

Integration Event
```

La transformación hacia un Integration Event no cambia el
Consistency Boundary del Aggregate.

La definición formal pertenece a:

```text
DOMAIN-009K-Integration-Events.md
```

---

# Permissions y Boundary

Las Permissions no forman parte del estado interno de Voting.

Determinan si una operación puede ser solicitada.

No amplían el Boundary.

Debe mantenerse:

```text
Permission Granted

≠

Additional Consistency Boundary
```

Una Permission de Voting tampoco concede capacidad para modificar
otro Aggregate.

---

# Read Models

Los Read Models se encuentran fuera del Consistency Boundary de
escritura.

Conceptualmente:

```text
Voting

↓

Domain Events

↓

Read Model
```

El Read Model:

- es derivado;
- no es Aggregate Root;
- no protege las Invariants de Voting;
- no modifica Voting;
- no forma parte de la unidad de escritura del Aggregate.

La definición formal pertenece a:

```text
DOMAIN-009L-Read-Model.md
```

---

# CQRS

En CQRS, Voting mantiene su Consistency Boundary en el Write Side.

Conceptualmente:

```text
Command

↓

Voting

↓

Consistency Boundary

↓

Domain Event
```

El Read Side permanece separado:

```text
Domain Event

↓

Projection

↓

Read Model
```

La separación de lectura y escritura no modifica las Invariants del
Aggregate.

---

# Event Sourcing

La compatibilidad con Event Sourcing no modifica el Consistency
Boundary.

Cuando Voting sea reconstruido a partir de hechos históricos:

```text
Domain Events

↓

Voting
```

el resultado debe representar el mismo Aggregate y preservar sus
Invariants, Lifecycle y Version.

Replay no amplía el Boundary ni modifica otros Aggregates.

---

# Rehidratación

La rehidratación reconstruye exclusivamente Voting.

Debe mantenerse:

```text
Persisted Voting State

↓

Rehydrate

↓

Voting
```

No debe producir:

```text
Rehydrate Voting

↓

Rehydrate Assembly

Rehydrate Proposal

Rehydrate Participation
```

como parte del mismo Aggregate.

Los otros Aggregates conservan sus propios Repositories y
Boundaries.

---

# Regla de Interacción Externa

Cuando Voting necesite relacionarse con otro Aggregate debe utilizar
los mecanismos ya definidos por AURA sin obtener propiedad sobre su
estado interno.

Conceptualmente:

```text
Voting
   │
   ├── Aggregate Identifiers
   ├── Domain Events
   └── Integration Events
```

según corresponda a la interacción.

La coordinación no transforma varios Aggregates en una única unidad
de consistencia.

---

# Regla de Independencia

Voting debe poder mantener su estado interno válido sin depender de
una modificación simultánea del estado interno de otro Aggregate.

Una modificación válida de Voting debe concluir con:

```text
Valid Voting
```

independientemente de que procesos posteriores relacionados con:

```text
Proposal

Assembly

Participation

Notification

Audit

Integration
```

se ejecuten después.

---

# Fallo de Procesos Externos

Un hecho confirmado dentro de Voting no deja de ser verdadero
porque un proceso externo posterior todavía no haya completado su
propia operación.

Conceptualmente:

```text
VotingClosed

=

Confirmed Voting Fact
```

La evolución posterior de otros Aggregates pertenece a sus propios
Boundaries.

Voting no debe revertir silenciosamente un hecho confirmado para
simular consistencia interna de otro Aggregate.

---

# Restricciones

No está permitido:

- expandir Voting para incorporar Organization como entidad interna;
- incorporar Citizen como entidad interna de Voting;
- incorporar Membership como entidad interna de Voting;
- incorporar Role como entidad interna de Voting;
- incorporar Territory como entidad interna de Voting;
- incorporar Assembly como entidad interna de Voting;
- incorporar Proposal como entidad interna de Voting;
- incorporar Participation como entidad interna de Voting;
- incorporar Document como entidad interna de Voting;
- incorporar Notification como entidad interna de Voting;
- incorporar Audit como entidad interna de Voting;
- incorporar Integration como entidad interna de Voting;
- modificar directamente otro Aggregate desde Voting;
- persistir partes de Voting de manera independiente para evitar
  Invariants;
- modificar VotingStatus fuera de la Aggregate Root;
- modificar Version directamente;
- modificar Result directamente evitando comportamiento del
  Aggregate;
- utilizar Read Models para modificar Voting;
- utilizar Repository para evitar el Consistency Boundary;
- utilizar Permissions para ampliar el Consistency Boundary;
- considerar una referencia externa como ownership;
- considerar un Domain Event como modificación directa de otro
  Aggregate;
- considerar un Integration Event como parte del estado interno de
  Voting;
- permitir una modificación parcial que deje Voting inválido;
- compartir Version con otro Aggregate;
- compartir Lifecycle con otro Aggregate.

---

# Reglas

## REG-001

Voting constituye un Consistency Boundary independiente.

---

## REG-002

La única Aggregate Root del Boundary es:

```text
Voting
```

---

## REG-003

Toda modificación interna debe realizarse mediante Voting.

---

## REG-004

Toda operación válida debe comenzar y terminar con un estado válido
del Aggregate.

---

## REG-005

Las Invariants deben preservarse inmediatamente dentro del
Boundary.

---

## REG-006

Una modificación no puede confirmarse parcialmente cuando ello deje
Voting en un estado inválido.

---

## REG-007

VotingId pertenece al Boundary y permanece inmutable.

---

## REG-008

OrganizationId pertenece al estado de Voting y permanece
inmutable, mientras Organization permanece fuera del Boundary.

---

## REG-009

VotingStatus, Lifecycle y State Machine pertenecen al Consistency
Boundary de Voting.

---

## REG-010

Rules, Options y Result deben permanecer coherentes dentro del
Boundary cuando correspondan.

---

## REG-011

Version pertenece exclusivamente a Voting y debe corresponder al
estado resultante de cada modificación válida.

---

## REG-012

Los Aggregates externos se relacionan mediante identificadores y
contratos sin convertirse en entidades internas de Voting.

---

## REG-013

Voting no modifica directamente otro Aggregate.

---

## REG-014

Un Domain Event comunica un hecho de Voting sin ampliar su
Consistency Boundary.

---

## REG-015

Un Integration Event no forma parte del estado interno de Voting.

---

## REG-016

Los Read Models permanecen fuera del Boundary de escritura y no
pueden modificar Voting.

---

## REG-017

Permissions no amplían el Consistency Boundary ni permiten evitar
sus Invariants.

---

## REG-018

La persistencia debe tratar Voting como una unidad de consistencia.

---

## REG-019

La rehidratación reconstruye exclusivamente el estado del Aggregate
Voting.

---

## REG-020

La coordinación con otros Aggregates debe preservar la
independencia de sus respectivos Consistency Boundaries.

---

# Definición de Éxito

El Aggregate **Voting** mantiene un Consistency Boundary explícito,
cohesivo e independiente.

Dentro del límite permanecen:

```text
Voting

Internal State

Value Objects

Internal Entities when applicable

Lifecycle

State Machine

Rules

Options

Result when applicable

Lifecycle Timestamps

Version
```

Fuera del límite permanecen:

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

Voting mantiene referencias externas mediante identificadores sin
absorber los Aggregates relacionados.

Toda modificación válida:

- ocurre mediante la Aggregate Root;
- preserva identidad;
- preserva OrganizationId;
- mantiene Lifecycle y State Machine;
- protege Invariants;
- mantiene Rules, Options y Result coherentes;
- actualiza Version de forma consistente;
- produce los Domain Events correspondientes;
- persiste Voting como una unidad;
- no modifica directamente otro Aggregate.

Los Domain Events e Integration Events permiten comunicar hechos
fuera del Boundary sin transformar múltiples Aggregates en una sola
unidad de consistencia.

Los Read Models permanecen derivados y no poseen autoridad de
escritura sobre Voting.

De esta forma, `DOMAIN-009J-Consistency-Boundary.md` establece el
límite oficial de consistencia del Aggregate **Voting**, preservando
la independencia entre Aggregates y manteniendo el patrón DDD
consolidado de AURA Core.