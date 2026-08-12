# DOMAIN-007J — Proposal Consistency Boundary

Versión: 1.0

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
- DOMAIN-007D-Domain-Events.md
- DOMAIN-007E-Invariants.md
- DOMAIN-007F-Permissions.md
- DOMAIN-007G-Repository-Contract.md
- DOMAIN-007H-Examples.md
- DOMAIN-007I-Versioning.md
- CORE-003-Shared-Kernel.md
- CORE-004-Ubiquitous-Language.md
- CORE-006-Domain-Invariants.md
- CORE-008-Aggregate-Design-Rules.md
- CORE-011-Repository-Contracts.md

---

# Objetivo

Definir el límite oficial de consistencia del Aggregate
**Proposal**.

El Consistency Boundary establece qué conceptos, estado,
comportamientos e invariantes deben mantenerse consistentes de
forma inmediata dentro de una única operación sobre Proposal.

Este límite determina qué pertenece al Aggregate y qué debe
permanecer fuera de él.

Su propósito es garantizar que Proposal conserve una frontera
transaccional explícita, evitando que procesos relacionados con
Organization, Citizen, Membership, Role, Territory, Assembly,
Participation, Voting, Document, Notification, Audit o
Integration sean absorbidos dentro de su modelo interno.

Proposal constituye una única unidad de consistencia.

---

# Propósito

El Consistency Boundary de Proposal permite:

- definir la frontera transaccional del Aggregate;
- determinar qué estado pertenece a Proposal;
- proteger las invariantes internas;
- mantener una única Aggregate Root;
- impedir modificaciones parciales del Aggregate;
- evitar transacciones distribuidas entre Aggregates;
- impedir referencias mutables hacia otros Aggregates;
- mantener independencia entre ciclos de vida;
- controlar la persistencia como una unidad;
- establecer las reglas de interacción con otros Aggregates;
- mantener consistencia fuerte dentro de Proposal;
- utilizar consistencia eventual fuera de Proposal;
- preservar alta cohesión y bajo acoplamiento;
- proteger la autonomía del Aggregate dentro de una arquitectura
  distribuida.

---

# Principio Fundamental

El Aggregate **Proposal** constituye un único límite de
consistencia.

Conceptualmente:

```text
Proposal Aggregate
        │
        │
        ▼
Consistency Boundary
```

Todo estado que pertenezca a Proposal debe permanecer válido al
finalizar cualquier modificación aceptada.

Ninguna operación válida puede dejar parcialmente actualizado el
estado interno del Aggregate.

---

# Regla Principal

La regla fundamental del límite es:

```text
One Aggregate

=

One Consistency Boundary
```

Para Proposal:

```text
Proposal

=

Proposal Consistency Boundary
```

Esto significa que una operación sobre Proposal garantiza
consistencia inmediata exclusivamente sobre el estado que
pertenece al Aggregate Proposal.

No garantiza consistencia transaccional inmediata sobre otros
Aggregates.

---

# Aggregate Root

La única Aggregate Root dentro del límite es:

```text
Proposal
```

Toda modificación del estado interno debe realizarse mediante
Proposal.

No existen múltiples Aggregate Roots dentro del mismo límite.

No está permitido modificar directamente componentes internos
evitando la Aggregate Root.

Conceptualmente:

```text
Command

↓

Proposal

↓

Internal State
```

No:

```text
Command

↓

Internal Component
```

---

# Estado Dentro del Límite

El Consistency Boundary protege el estado conceptual propio de
Proposal.

Este estado comprende, según la definición oficial del
Aggregate:

```text
ProposalId

OrganizationId

Proposer references

TerritoryId

AssemblyId

ProposalType

ProposalName

ProposalPurpose

ProposalDescription

ProposalContent

ProposalStatus

CreatedAt

UpdatedAt

SubmittedAt

ReviewedAt

AcceptedAt

RejectedAt

WithdrawnAt

ArchivedAt

Version
```

Cuando alguno de estos conceptos forme parte del estado de una
Proposal concreta, debe mantenerse consistente con las
invariantes del Aggregate.

---

# Identidad Dentro del Límite

La identidad protegida por el Consistency Boundary es:

```text
ProposalId
```

ProposalId:

- pertenece exclusivamente a Proposal;
- es único;
- es inmutable;
- permanece constante durante todo el ciclo de vida;
- no depende de la persistencia;
- no depende del estado de otros Aggregates.

El límite de consistencia garantiza que ninguna operación válida
pueda reemplazar o modificar ProposalId.

---

# Propiedad Organizacional

Proposal mantiene la referencia hacia la Organization
correspondiente mediante:

```text
OrganizationId
```

OrganizationId forma parte del estado referencial de Proposal.

La Organization completa no forma parte del Aggregate.

Conceptualmente:

```text
Proposal
    │
    └── OrganizationId
```

No:

```text
Proposal
    │
    └── Organization
            │
            └── Internal Organization State
```

Proposal protege la integridad de su referencia.

No protege ni modifica el estado interno de Organization.

---

# Proponente

Proposal puede mantener las referencias necesarias para
identificar al proponente conforme al modelo definido para el
Aggregate.

Estas referencias pueden relacionarse con:

```text
CitizenId

MembershipId
```

según corresponda al contexto de la Proposal.

Las referencias pertenecen al estado de Proposal cuando forman
parte de su identidad contextual.

Los Aggregates Citizen y Membership no forman parte del límite de
consistencia.

Conceptualmente:

```text
Proposal
    │
    ├── CitizenId
    │
    └── MembershipId
```

No:

```text
Proposal
    │
    ├── Citizen Aggregate
    │
    └── Membership Aggregate
```

---

# Contexto Territorial

Cuando una Proposal posee contexto territorial, mantiene:

```text
TerritoryId
```

TerritoryId forma parte de la referencia contextual de Proposal.

Territory permanece fuera del límite.

Proposal no contiene:

- geometría territorial;
- jerarquía territorial;
- límites territoriales;
- estado interno de Territory;
- reglas internas del Aggregate Territory.

Conceptualmente:

```text
Proposal

↓

TerritoryId
```

La existencia de esta referencia no convierte Territory en una
entidad interna de Proposal.

---

# Contexto de Assembly

Una Proposal puede estar relacionada con una Assembly mediante:

```text
AssemblyId
```

cuando corresponda.

AssemblyId permite contextualizar la Proposal dentro de una
instancia formal de reunión.

Assembly permanece como Aggregate independiente.

Proposal no absorbe:

- programación de Assembly;
- convocatoria;
- modalidad;
- ubicación;
- estado interno de Assembly;
- reglas de realización;
- ciclo de vida de Assembly.

Debe mantenerse:

```text
Proposal
    │
    └── AssemblyId
```

No:

```text
Proposal
    │
    └── Assembly Aggregate
```

---

# Estado de Proposal

ProposalStatus pertenece al Consistency Boundary.

Conceptualmente:

```text
ProposalStatus
```

representa el estado actual del Aggregate dentro de su Lifecycle.

Las transiciones de estado deben respetar:

```text
DOMAIN-007A-Lifecycle.md

DOMAIN-007B-State-Machine.md
```

Una operación válida no puede dejar Proposal en un estado que
viole su State Machine.

---

# Contenido de Proposal

El contenido conceptual propio de Proposal forma parte de su
límite cuando corresponde a la definición formal del Aggregate.

Esto incluye conceptos como:

```text
ProposalName

ProposalPurpose

ProposalDescription

ProposalContent

ProposalType
```

Estos valores pertenecen a Proposal.

Su modificación debe realizarse mediante comportamiento del
Aggregate Root y respetar:

- estado actual;
- Commands permitidos;
- Permissions;
- invariantes;
- reglas de modificación;
- Version.

---

# Información Temporal

Las marcas temporales que representan hechos propios del ciclo de
vida de Proposal pertenecen al Aggregate cuando así se encuentran
definidas.

Conceptualmente:

```text
CreatedAt

UpdatedAt

SubmittedAt

ReviewedAt

AcceptedAt

RejectedAt

WithdrawnAt

ArchivedAt
```

Estas marcas representan información temporal asociada a hechos
del propio Aggregate.

No representan registros de Audit externos.

---

# Version Dentro del Límite

Proposal mantiene:

```text
Version
```

Version pertenece al Consistency Boundary.

Toda modificación válida debe mantener coherencia entre:

```text
Proposal State

+

ProposalStatus

+

Version
```

No puede confirmarse parcialmente una modificación en la que el
estado cambie pero Version permanezca representando una revisión
anterior.

Las reglas completas se encuentran en:

```text
DOMAIN-007I-Versioning.md
```

---

# Componentes Internos

Los conceptos internos que formen parte de Proposal no poseen
autonomía fuera del Aggregate.

Cuando el modelo utilice Value Objects u otros componentes
internos, estos:

- pertenecen al Consistency Boundary;
- son controlados por Proposal;
- no poseen Repository independiente;
- no pueden modificarse directamente desde el exterior;
- no poseen Lifecycle independiente del Aggregate;
- no constituyen nuevos Aggregates.

Conceptualmente:

```text
Proposal
    │
    ├── ProposalName
    ├── ProposalPurpose
    ├── ProposalDescription
    ├── ProposalContent
    ├── ProposalType
    └── ProposalStatus
```

---

# Value Objects

Los Value Objects pertenecientes al modelo interno de Proposal
forman parte del límite de consistencia cuando representan
atributos propios del Aggregate.

Estos Value Objects:

- son inmutables;
- validan sus propias reglas de valor;
- no poseen identidad independiente;
- no poseen Repository;
- no se modifican fuera de Proposal;
- no amplían el Consistency Boundary hacia otros Aggregates.

La utilización de identificadores externos como Value Objects no
convierte al Aggregate referenciado en parte de Proposal.

Por ejemplo:

```text
TerritoryId
```

puede pertenecer al estado de Proposal.

Pero:

```text
Territory
```

permanece fuera del Aggregate.

---

# Invariantes Dentro del Límite

Todas las invariantes propias de Proposal deben cumplirse antes de
confirmar una modificación.

El límite protege, entre otras, reglas relacionadas con:

- identidad;
- propiedad organizacional;
- proponente;
- contenido;
- tipo;
- estado;
- transición;
- contexto territorial;
- contexto de Assembly;
- información temporal;
- Version;
- archivado;
- referencias externas.

Las invariantes completas se encuentran definidas en:

```text
DOMAIN-007E-Invariants.md
```

---

# Atomicidad

Una modificación válida de Proposal constituye una única
operación lógica.

Conceptualmente:

```text
Previous Proposal State

↓

Command

↓

Domain Validation

↓

Valid Modification

↓

New Proposal State
```

El resultado debe ser:

```text
Complete Valid State
```

o:

```text
No State Change
```

No existe un estado intermedio parcialmente confirmado.

---

# Regla All-or-Nothing

Las modificaciones internas siguen:

```text
All

or

Nothing
```

Si una operación requiere modificar varios atributos internos de
Proposal, todos deben quedar consistentes como una única
modificación lógica.

Ejemplo:

```text
SubmitProposal
```

puede implicar conceptualmente:

```text
ProposalStatus

SubmittedAt

UpdatedAt

Version
```

Estos valores deben representar conjuntamente la misma revisión
válida.

No está permitido confirmar solo una parte.

---

# Ejemplo de Modificación Atómica

Estado inicial:

```text
ProposalStatus = Draft

SubmittedAt = null

Version = 4
```

Se ejecuta:

```text
SubmitProposal
```

Si la operación es válida:

```text
ProposalStatus = Submitted

SubmittedAt = Timestamp

Version = 5
```

Todo el nuevo estado pertenece a la misma modificación lógica.

No debe producirse:

```text
ProposalStatus = Submitted

SubmittedAt = null

Version = 4
```

como resultado persistido de una operación parcialmente aplicada.

---

# Fallo de Invariante

Si una operación viola una invariante:

```text
Command

↓

Invariant Violation

↓

Reject
```

El estado debe permanecer:

```text
Previous Proposal State
```

No puede existir una modificación parcial.

---

# Fallo de State Machine

Si una transición no está permitida:

```text
Current State

↓

Requested Transition

↓

Invalid
```

el Aggregate mantiene:

```text
Current State
```

sin modificar el resto de su estado interno.

---

# Fallo de Permission

Si la autorización necesaria no se encuentra satisfecha, la
operación no debe modificar Proposal.

Conceptualmente:

```text
Permission Denied

↓

No Aggregate Modification
```

Permissions se define formalmente en:

```text
DOMAIN-007F-Permissions.md
```

La autorización determina quién puede intentar una operación.

El Consistency Boundary determina qué estado debe permanecer
consistente cuando la operación es ejecutada.

---

# Fallo de Concurrencia

Cuando:

```text
ExpectedVersion

≠

PersistedVersion
```

la nueva revisión no puede ser confirmada.

Debe mantenerse:

```text
Persisted Proposal State

=

Unchanged
```

El conflicto de concurrencia no permite persistencia parcial.

Las reglas completas se encuentran en:

```text
DOMAIN-007I-Versioning.md
```

---

# Persistencia como Unidad

Proposal se persiste como una unidad de consistencia.

Conceptualmente:

```text
ProposalRepository

↓

Proposal Aggregate
```

No:

```text
ProposalRepository

↓

Independent Attribute Updates
```

El Repository no expone mecanismos que permitan modificar partes
del Aggregate evitando las reglas de Proposal.

---

# Repository Boundary

El Repository opera sobre:

```text
Proposal
```

como Aggregate completo.

No deben existir contratos de dominio equivalentes a:

```text
updateProposalStatusDirectly()

updateProposalVersionDirectly()

updateProposalContentDirectly()
```

que permitan alterar el estado persistido evitando el
comportamiento del Aggregate Root.

El contrato oficial se encuentra en:

```text
DOMAIN-007G-Repository-Contract.md
```

---

# Consistencia Fuerte

Dentro del límite de Proposal se aplica:

```text
Strong Consistency
```

Esto significa que al finalizar correctamente una modificación,
el estado interno del Aggregate debe satisfacer inmediatamente
todas sus invariantes.

Conceptualmente:

```text
Command

↓

Proposal

↓

Validate

↓

Modify

↓

Consistent Aggregate State
```

---

# Consistencia Eventual

Entre Proposal y otros Aggregates se utiliza:

```text
Eventually Consistent
```

cuando la coordinación requiera propagación de cambios entre
límites independientes.

Conceptualmente:

```text
Proposal

↓

Domain Event

↓

Application / Integration Coordination

↓

Other Aggregate or Bounded Context
```

Proposal no mantiene una transacción distribuida para garantizar
que todos los Aggregates relacionados cambien simultáneamente.

---

# Límite Externo

Permanecen fuera del Consistency Boundary de Proposal:

```text
Organization

Citizen

Membership

Role

Territory

Assembly

Participation

Voting

Document

Notification

Audit

Integration
```

Cada uno conserva, cuando corresponda:

- identidad propia;
- Aggregate Root propia;
- Lifecycle propio;
- State Machine propia;
- invariantes propias;
- Repository propio;
- Version propia;
- Domain Events propios;
- Consistency Boundary propio.

---

# Regla de No Absorción

La relación funcional entre Proposal y otro Aggregate no convierte
al segundo Aggregate en parte de Proposal.

Debe mantenerse:

```text
Relationship

≠

Aggregate Membership
```

y:

```text
Contextual Association

≠

Consistency Ownership
```

Por lo tanto, una Proposal puede relacionarse con:

```text
Assembly

Participation

Voting

Document
```

sin absorber ninguno de ellos.

---

# Proposal y Organization

La relación conceptual es:

```text
Organization
      │
      │ 1
      ▼
   Proposal
      │
      │ N
```

Una Organization puede mantener múltiples Proposals.

Cada Proposal pertenece al contexto de una Organization según las
reglas establecidas por el dominio.

Proposal mantiene:

```text
OrganizationId
```

pero no contiene:

```text
Organization Aggregate
```

---

# Proposal y Citizen

Citizen puede relacionarse con Proposal como actor o proponente
según las reglas del dominio.

Proposal puede mantener:

```text
CitizenId
```

cuando corresponda.

Citizen permanece fuera del límite.

Proposal no modifica:

- identidad de Citizen;
- perfil;
- contacto;
- estado;
- verificación;
- consentimiento;
- Lifecycle de Citizen.

---

# Proposal y Membership

Membership puede proporcionar contexto organizacional al
proponente.

Proposal puede mantener:

```text
MembershipId
```

cuando corresponda.

Membership permanece fuera del límite.

Proposal no modifica:

- estado de Membership;
- OrganizationId de Membership;
- CitizenId de Membership;
- Roles asociados;
- Lifecycle de Membership.

---

# Proposal y Role

Role puede participar en reglas de autorización o responsabilidad
organizacional.

Role no forma parte de Proposal.

Proposal no mantiene una copia mutable del Role ni modifica:

- Name;
- Code;
- RoleType;
- Status;
- IsSystemRole.

La autorización correspondiente se resuelve fuera del estado
interno del Aggregate.

---

# Proposal y Territory

Proposal puede referenciar:

```text
TerritoryId
```

Territory conserva su propio límite.

Proposal no modifica:

```text
Territory
```

ni requiere una transacción compartida con Territory para
modificar su propio estado.

---

# Proposal y Assembly

Proposal puede mantener:

```text
AssemblyId
```

cuando la Proposal se encuentra contextualizada dentro de una
Assembly.

Assembly conserva su propia consistencia.

Proposal no puede modificar directamente:

```text
AssemblyStatus

AssemblySchedule

AssemblyConvocation

AssemblyMode

AssemblyLocation

AssemblyVersion
```

---

# Proposal y Participation

Participation representa procesos de participación relacionados
con el dominio.

Participation no forma parte de Proposal.

Debe mantenerse:

```text
Proposal

≠

Participation
```

Una relación entre ambos no permite que Proposal modifique
directamente el estado de Participation.

---

# Proposal y Voting

Una Proposal puede convertirse en materia de un proceso de
Voting.

Esto no convierte Voting en parte de Proposal.

Conceptualmente:

```text
Proposal
      │
      │ contextual relation
      ▼
Voting
```

No:

```text
Proposal
    └── Voting Internal Entity
```

Voting mantiene:

- identidad propia;
- Lifecycle propio;
- State Machine propia;
- reglas propias;
- resultados propios;
- Repository propio;
- Version propia.

Proposal no ejecuta internamente el proceso de votación.

---

# Proposal y Document

Una Proposal puede relacionarse con Documents.

La relación puede establecerse mediante:

```text
DocumentId
```

cuando corresponda.

Proposal no almacena el Aggregate Document dentro de su límite.

Document mantiene:

- identidad propia;
- contenido documental;
- metadatos documentales;
- Lifecycle propio;
- Repository propio.

---

# Proposal y Notification

Los hechos producidos por Proposal pueden originar procesos de
Notification.

Ejemplo:

```text
ProposalSubmitted

↓

Notification Process
```

Notification permanece fuera del límite.

Proposal no:

- envía mensajes;
- administra canales;
- administra destinatarios técnicos;
- controla reintentos;
- mantiene estado de entrega.

---

# Proposal y Audit

Los cambios relevantes de Proposal pueden ser observados por
Audit.

Audit permanece fuera del Aggregate.

Proposal no contiene:

```text
Audit Aggregate
```

ni mantiene registros externos de auditoría como entidades
internas.

La trazabilidad puede utilizar:

```text
ProposalId

Version

Domain Events

ActorId

Timestamp

CorrelationId

CausationId
```

sin convertir Audit en parte del Consistency Boundary.

---

# Proposal e Integration

Integration permanece fuera del límite de Proposal.

Proposal no conoce:

- endpoints;
- protocolos externos;
- OAuth;
- JWT;
- FIWARE;
- NGSI-LD;
- APIs municipales;
- SDKs externos;
- sistemas Smart City;
- credenciales;
- proveedores.

La interoperabilidad se establece mediante contratos y eventos.

---

# Referencias Externas

Las relaciones hacia otros Aggregates deben mantenerse mediante
identificadores.

Conceptualmente:

```text
OrganizationId

CitizenId

MembershipId

TerritoryId

AssemblyId

DocumentId
```

cuando correspondan al modelo de Proposal.

Estos identificadores pueden formar parte del estado del
Aggregate.

Los Aggregates completos referenciados no forman parte de
Proposal.

---

# Regla de Referencia por Identidad

Debe mantenerse:

```text
Aggregate A

↓

AggregateBId
```

No:

```text
Aggregate A

↓

Mutable Aggregate B
```

Para Proposal:

```text
Proposal

↓

TerritoryId
```

es válido.

```text
Proposal

↓

Mutable Territory Aggregate
```

no pertenece al modelo.

---

# Prohibición de Referencias Mutables

Proposal nunca mantiene una referencia mutable que permita
alterar directamente otro Aggregate.

No está permitido conceptualmente:

```text
Proposal.changeTerritoryName()
```

si esa operación modifica Territory.

Tampoco:

```text
Proposal.completeAssembly()
```

si modifica Assembly.

Ni:

```text
Proposal.openVoting()
```

si modifica Voting.

Cada operación debe dirigirse al Aggregate propietario del estado
correspondiente.

---

# Propiedad del Comportamiento

Cada comportamiento pertenece al Aggregate propietario de las
invariantes que modifica.

Por ejemplo:

```text
SubmitProposal
```

pertenece a Proposal.

```text
StartAssembly
```

pertenece a Assembly.

```text
CastVote
```

pertenece a Voting.

```text
UpdateCitizenProfile
```

pertenece a Citizen.

La coordinación entre comportamientos no fusiona sus límites.

---

# Regla de Transacción

Una transacción de dominio sobre Proposal modifica únicamente:

```text
One Proposal Aggregate
```

No debe requerir una transacción ACID distribuida que modifique
simultáneamente:

```text
Proposal

+

Assembly

+

Voting

+

Document
```

Cada Aggregate confirma su propio estado de manera independiente.

---

# Prohibición de Transacciones Distribuidas

No debe diseñarse Proposal bajo la condición de que una operación
solo sea válida si múltiples Aggregates se persisten dentro de la
misma transacción técnica.

No:

```text
BEGIN DISTRIBUTED TRANSACTION

Update Proposal

Update Assembly

Update Voting

Update Document

COMMIT ALL
```

El modelo debe preservar límites independientes.

---

# Coordinación entre Aggregates

Cuando un proceso de negocio requiere intervenir en múltiples
Aggregates, la coordinación ocurre fuera del Consistency Boundary
de Proposal.

Conceptualmente:

```text
Application Service

or

Domain Coordination

or

Event-Driven Coordination
```

puede coordinar operaciones independientes.

Proposal continúa siendo responsable exclusivamente de su propio
estado.

---

# Domain Events

Proposal publica Domain Events después de hechos relevantes del
dominio.

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

Los eventos permiten comunicar hechos sin ampliar el límite
transaccional del Aggregate.

La definición oficial se encuentra en:

```text
DOMAIN-007D-Domain-Events.md
```

---

# Domain Events y Boundary

Un Domain Event producido por Proposal representa un hecho
ocurrido dentro de su Consistency Boundary.

Conceptualmente:

```text
Proposal

↓

Valid State Change

↓

Domain Event
```

El evento puede ser observado fuera del Aggregate.

El consumidor del evento no pasa a formar parte de Proposal.

---

# Integration Events

Cuando un hecho debe cruzar el Bounded Context o comunicarse con
sistemas externos, puede originar un Integration Event.

Conceptualmente:

```text
Proposal Domain Event

↓

Integration Mapping

↓

Integration Event

↓

External Consumer
```

La publicación de Integration Events no amplía el Consistency
Boundary de Proposal.

La definición correspondiente se desarrolla en:

```text
DOMAIN-007K-Integration-Events.md
```

---

# Commands y Boundary

Un Command dirigido a Proposal debe modificar exclusivamente una
Proposal.

Debe mantenerse:

```text
Command

↓

Proposal Aggregate
```

No:

```text
Command

↓

Proposal + Assembly + Voting
```

Si un caso de uso requiere cambios sobre varios Aggregates, cada
Aggregate recibe la intención correspondiente mediante la
coordinación de aplicación definida para el proceso.

---

# Command Rechazado

Cuando Proposal rechaza un Command:

```text
Rejected Command
```

el Consistency Boundary garantiza:

```text
No Partial Proposal Modification
```

y:

```text
No Valid New Proposal Revision
```

El estado interno permanece en la última revisión válida.

---

# Version y Boundary

Version protege la revisión del Consistency Boundary.

Conceptualmente:

```text
ProposalId

+

Proposal State

+

Version
```

representan conjuntamente una revisión lógica del Aggregate.

Version no protege directamente el estado de otros Aggregates.

---

# Concurrencia Dentro del Boundary

Dos modificaciones concurrentes sobre la misma Proposal deben
validar:

```text
ExpectedVersion

=

PersistedVersion
```

antes de confirmar una nueva revisión.

Esto evita que una modificación basada en un estado obsoleto
sobrescriba otra modificación válida.

---

# Concurrencia entre Aggregates

Las versiones de distintos Aggregates son independientes.

Ejemplo:

```text
Proposal.Version = 8

Assembly.Version = 14

Voting.Version = 3
```

No existe una regla que requiera:

```text
Proposal.Version

=

Assembly.Version

=

Voting.Version
```

Cada Aggregate protege su propia evolución.

---

# Independencia del Lifecycle

Proposal posee su propio Lifecycle.

El estado de otro Aggregate no modifica automáticamente
ProposalStatus.

Ejemplo:

```text
Assembly = Completed
```

no implica automáticamente:

```text
Proposal = Accepted
```

Cualquier cambio en Proposal debe producirse mediante un
comportamiento válido del propio Aggregate.

---

# Independencia de State Machine

La State Machine de Proposal es independiente de las State
Machines de otros Aggregates.

Una transición válida en Assembly no constituye automáticamente
una transición válida en Proposal.

Debe mantenerse:

```text
Assembly Transition

≠

Proposal Transition
```

---

# Independencia de Invariantes

Cada Aggregate protege sus propias invariantes.

Proposal no debe intentar proteger internamente todas las
invariantes de:

```text
Organization

Citizen

Membership

Territory

Assembly

Participation

Voting

Document
```

Debe proteger únicamente las invariantes que pertenecen a su
propio límite.

---

# Validación de Referencias Externas

Cuando una operación requiere verificar información perteneciente
a otro Aggregate, dicha verificación no convierte al Aggregate
externo en parte de Proposal.

Ejemplo conceptual:

```text
CreateProposal

↓

Verify Organization Context

↓

Create Proposal
```

La validación externa puede ocurrir antes de invocar el
comportamiento correspondiente.

Proposal recibe únicamente la información necesaria para proteger
sus propias reglas.

---

# Snapshot Externo

Proposal no debe almacenar una copia mutable completa de otro
Aggregate con el propósito de mantener consistencia compartida.

No:

```text
Proposal
    │
    └── OrganizationSnapshot
            │
            ├── Roles
            ├── Memberships
            └── Internal State
```

si dicho snapshot pretende convertirse en una copia autoritativa
de Organization.

Las representaciones necesarias para lectura o integración
pertenecen a otros modelos.

---

# Read Models

Los Read Models se encuentran fuera del Consistency Boundary de
Proposal.

Conceptualmente:

```text
Proposal Aggregate

↓

Domain Events

↓

Projection

↓

Proposal Read Model
```

Las proyecciones:

- no modifican Proposal;
- no protegen invariantes;
- no forman parte de la transacción del Aggregate;
- pueden ser eventualmente consistentes;
- pueden reconstruirse.

La definición correspondiente se encuentra en:

```text
DOMAIN-007L-Read-Model.md
```

---

# Read Model Desnormalizado

Un Read Model puede combinar información procedente de múltiples
Aggregates.

Ejemplo conceptual:

```text
ProposalId

ProposalName

OrganizationName

TerritoryName

AssemblyName
```

Esto no significa que esos datos formen parte del Aggregate
Proposal.

Debe mantenerse:

```text
Read Composition

≠

Write Consistency Boundary
```

---

# Performance

Las optimizaciones de lectura o persistencia no pueden ampliar ni
romper el Consistency Boundary.

Una optimización técnica no puede justificar:

- modificar atributos internos fuera del Aggregate;
- compartir tablas como modelo de dominio;
- introducir setters directos;
- omitir invariantes;
- fusionar Aggregates;
- utilizar Read Models como Write Models.

Las reglas específicas de rendimiento se desarrollarán en:

```text
DOMAIN-007N-Performance-Rules.md
```

---

# Seguridad

El Consistency Boundary no contiene infraestructura de
autenticación.

Proposal no almacena:

- contraseñas;
- JWT;
- tokens OAuth;
- sesiones;
- secretos;
- claves privadas;
- credenciales de sistemas externos.

La seguridad técnica permanece fuera del Aggregate.

Las reglas específicas se desarrollarán en:

```text
DOMAIN-007O-Security-Model.md
```

---

# Permissions

Permissions determina quién puede solicitar determinadas
modificaciones.

El Consistency Boundary determina qué estado pertenece a Proposal
y qué debe permanecer consistente.

Debe mantenerse:

```text
Permission

≠

Consistency Boundary
```

pero ambos cooperan para proteger el dominio.

---

# Auditoría

La auditoría de operaciones no amplía el límite.

Puede existir trazabilidad basada en:

```text
ProposalId

Version

CommandId

ActorId

Timestamp

CorrelationId

CausationId

Domain Events
```

pero Audit conserva su propio modelo.

---

# Interoperabilidad

Proposal puede participar en procesos de interoperabilidad con:

- sistemas municipales;
- plataformas de participación ciudadana;
- ecosistemas Smart City;
- sistemas FIWARE;
- servicios territoriales;
- plataformas documentales;
- sistemas analíticos.

Estas integraciones permanecen fuera del Consistency Boundary.

---

# FIWARE

Una representación NGSI-LD de Proposal constituye una
representación de integración.

No constituye el Aggregate.

Debe mantenerse:

```text
Proposal Aggregate

↓

Integration Mapping

↓

NGSI-LD Representation
```

No:

```text
NGSI-LD Entity

=

Proposal Aggregate
```

La representación externa no define el Consistency Boundary del
dominio.

---

# Infraestructura

El límite de consistencia es independiente de:

- base de datos;
- ORM;
- framework;
- lenguaje;
- protocolo;
- API;
- sistema de mensajería;
- proveedor cloud;
- FIWARE;
- NGSI-LD.

La infraestructura implementa el modelo.

No lo redefine.

---

# Persistencia Relacional

Si Proposal se persiste utilizando una base de datos relacional,
la existencia de múltiples tablas técnicas no significa que
existan múltiples Aggregates.

Conceptualmente:

```text
Multiple Persistence Structures

≠

Multiple Consistency Boundaries
```

La persistencia debe respetar el límite definido por el dominio.

---

# Persistencia Documental

Si Proposal se persiste como un documento:

```text
Proposal Document
```

esto tampoco significa que la estructura física determine el
Aggregate.

Debe mantenerse:

```text
Persistence Model

≠

Domain Model
```

---

# Event Sourcing

Cuando se utilice Event Sourcing, el Event Stream correspondiente
a Proposal representa la evolución de una única instancia del
Aggregate.

Conceptualmente:

```text
ProposalId

↓

Proposal Event Stream

↓

Proposal State
```

Los eventos pertenecientes a otros Aggregates no se convierten en
parte del Event Stream de Proposal por el solo hecho de estar
relacionados funcionalmente.

---

# CQRS

En CQRS:

```text
Write Side
    │
    ▼
Proposal Aggregate
    │
    ▼
Consistency Boundary
```

mientras:

```text
Read Side
    │
    ▼
Proposal Projections
```

Las proyecciones no amplían el límite de escritura.

---

# Event-Driven Architecture

La arquitectura dirigida por eventos permite coordinar
Aggregates independientes sin fusionar sus límites.

Conceptualmente:

```text
Proposal
    │
    ▼
Domain Event
    │
    ▼
Event-Driven Coordination
    │
    ▼
Another Aggregate / Context
```

Cada participante mantiene su propia consistencia.

---

# Clean Architecture

El Consistency Boundary pertenece al dominio.

No depende de Infrastructure.

Conceptualmente:

```text
Domain

Proposal Consistency Rules
```

permanece independiente de:

```text
Infrastructure

Database

Framework

Transport

External Systems
```

---

# Hexagonal Architecture

Proposal permanece en el núcleo del dominio.

Las interacciones externas ocurren mediante puertos y contratos.

Conceptualmente:

```text
External Adapter

↓

Application Port

↓

Proposal Aggregate

↓

Repository Port

↓

Persistence Adapter
```

Los adaptadores no forman parte del Consistency Boundary.

---

# Regla de Alta Cohesión

Todo concepto incluido dentro de Proposal debe existir porque es
necesario para proteger las invariantes y comportamiento propios
de Proposal.

No debe incluirse un concepto únicamente porque:

- aparece en la misma interfaz;
- participa en el mismo caso de uso;
- comparte una pantalla;
- utiliza la misma base de datos;
- pertenece a la misma Organization;
- ocurre durante la misma Assembly.

La pertenencia al Aggregate se determina por consistencia de
dominio.

---

# Regla de Bajo Acoplamiento

Proposal mantiene bajo acoplamiento con otros Aggregates mediante:

```text
Identifiers

Domain Events

Integration Events

Application Coordination

Repository Contracts
```

No mediante referencias mutables compartidas.

---

# Regla de Tamaño del Aggregate

Proposal debe contener únicamente el estado necesario para
proteger sus invariantes.

No debe crecer mediante incorporación indiscriminada de
conceptos relacionados.

Debe mantenerse:

```text
Small Consistency Boundary

+

Explicit Relationships

=

Controlled Aggregate
```

---

# Regla de Autonomía

Proposal debe poder validar una modificación de su propio estado
sin requerir acceso mutable directo a otros Aggregates.

Cuando se necesite información externa, esta debe obtenerse o
validarse mediante los mecanismos arquitectónicos
correspondientes antes o alrededor de la operación de dominio.

La autonomía evita convertir Proposal en un Aggregate
distribuido.

---

# Regla de Propiedad

Un dato mutable debe poseer un único propietario de consistencia.

Si un dato pertenece a Proposal:

```text
Proposal
```

es responsable de modificarlo.

Si pertenece a Assembly:

```text
Assembly
```

es responsable.

Si pertenece a Voting:

```text
Voting
```

es responsable.

No deben existir múltiples Aggregates modificando directamente el
mismo estado autoritativo.

---

# Regla de Consistencia entre Referencias

Proposal protege la validez estructural de las referencias que
mantiene según sus propias invariantes.

Sin embargo, no asume propiedad sobre el estado completo de las
entidades referenciadas.

Debe mantenerse:

```text
Reference Ownership

≠

Referenced Aggregate Ownership
```

---

# Escenario — Creación

```text
CreateProposal

↓

Validate Required Context

↓

Proposal.create()

↓

ProposalCreated

↓

Proposal State Consistent

↓

Persist Proposal
```

La operación crea únicamente Proposal.

No crea automáticamente:

```text
Organization

Citizen

Membership

Territory

Assembly
```

---

# Escenario — Submission

```text
Proposal Draft

↓

SubmitProposal

↓

Validate Proposal Invariants

↓

Proposal Submitted

↓

ProposalSubmitted

↓

Persist Proposal
```

La modificación afecta exclusivamente el Consistency Boundary de
Proposal.

---

# Escenario — Review

```text
Proposal Submitted

↓

StartProposalReview

↓

Validate State

↓

Proposal UnderReview

↓

ProposalReviewStarted
```

El proceso no modifica directamente otros Aggregates.

---

# Escenario — Acceptance

```text
Proposal UnderReview

↓

AcceptProposal

↓

Validate Permission

↓

Validate State

↓

Validate Invariants

↓

Proposal Accepted

↓

ProposalAccepted
```

Cualquier reacción externa al evento ocurre fuera del límite.

---

# Escenario — Voting Relacionado

Una Proposal puede encontrarse asociada a un proceso de Voting.

Conceptualmente:

```text
Proposal

↓

ProposalAccepted or other valid domain condition

↓

Domain / Application Coordination

↓

Voting
```

Proposal no crea internamente una entidad Voting como parte de su
estado.

---

# Escenario — Assembly Relacionada

Una Proposal puede estar asociada a:

```text
AssemblyId
```

La finalización de Assembly no modifica automáticamente Proposal.

Cualquier consecuencia sobre Proposal debe ser expresada mediante
una operación válida del propio Aggregate.

---

# Escenario — Document Relacionado

Una Proposal puede referenciar documentación.

La creación o modificación del Document ocurre en su propio
límite.

Conceptualmente:

```text
Proposal

↓

DocumentId
```

No:

```text
Proposal

↓

Mutable Document Aggregate
```

---

# Escenario — Notification

Después de:

```text
ProposalSubmitted
```

un proceso externo puede decidir producir una Notification.

Esto ocurre fuera de Proposal.

El fallo de Notification no revierte automáticamente la
modificación válida de Proposal.

---

# Escenario — Audit

Después de una modificación:

```text
ProposalAccepted
```

Audit puede registrar el hecho.

El registro de Audit no forma parte de la misma consistencia
interna de Proposal.

---

# Escenario — Integration

Después de un hecho relevante:

```text
ProposalAccepted
```

puede producirse:

```text
ProposalAcceptedForIntegration
```

La comunicación externa no amplía la transacción interna del
Aggregate.

---

# Escenario — Fallo Externo

Supóngase:

```text
ProposalSubmitted

↓

Commit Successful

↓

Notification Attempt

↓

Notification Failure
```

El fallo de Notification no significa que Proposal vuelva
automáticamente a Draft.

La Proposal permanece en su estado válido confirmado.

El sistema externo o proceso correspondiente administra su propia
recuperación.

---

# Escenario — Consistencia Eventual

```text
Proposal Accepted

↓

ProposalAccepted

↓

Integration Processing

↓

External Projection Updated
```

Puede existir un intervalo temporal entre:

```text
Proposal Commit
```

y:

```text
External Update
```

Ese intervalo es compatible con consistencia eventual.

---

# Escenario — Concurrencia

```text
Proposal Version 10

        │
        ├──────────────┐
        │              │
        ▼              ▼
    Process A       Process B
        │              │
        ▼              ▼
   Modification    Modification
        │              │
        ▼              ▼
   Save Version    Save Version
```

Solo una modificación basada en la versión persistida válida
puede ser confirmada.

El límite de consistencia permanece protegido mediante el modelo
definido en:

```text
DOMAIN-007I-Versioning.md
```

---

# Escenario — Operación Parcial

No está permitido:

```text
ProposalStatus Updated

↓

Version Update Failed

↓

Partial Commit
```

Debe ocurrir:

```text
All Changes Committed
```

o:

```text
No Changes Committed
```

---

# Escenario — Otro Aggregate Falla

Supóngase un proceso coordinado:

```text
Proposal Updated Successfully

↓

Another Aggregate Operation

↓

Failure
```

El sistema no debe asumir que existe una única transacción
distribuida que revierte automáticamente Proposal.

La coordinación debe respetar la autonomía de cada Aggregate.

---

# Restricciones

No está permitido:

- incluir otros Aggregates completos dentro de Proposal;
- mantener referencias mutables hacia otros Aggregates;
- modificar directamente Organization desde Proposal;
- modificar directamente Citizen desde Proposal;
- modificar directamente Membership desde Proposal;
- modificar directamente Role desde Proposal;
- modificar directamente Territory desde Proposal;
- modificar directamente Assembly desde Proposal;
- modificar directamente Participation desde Proposal;
- modificar directamente Voting desde Proposal;
- modificar directamente Document desde Proposal;
- modificar directamente Notification desde Proposal;
- modificar directamente Audit desde Proposal;
- utilizar una única transacción distribuida como requisito del
  Aggregate;
- persistir parcialmente el estado interno;
- modificar atributos internos evitando la Aggregate Root;
- utilizar Read Models como modelo de escritura;
- permitir que Infrastructure redefina el Consistency Boundary;
- utilizar una estructura de base de datos para determinar los
  límites del dominio;
- utilizar Version de otro Aggregate como Version de Proposal;
- compartir invariantes internas entre múltiples Aggregate Roots;
- convertir una relación contextual en pertenencia estructural.

---

# Invariantes del Consistency Boundary

El Consistency Boundary mantiene como mínimo:

- Proposal constituye una única unidad de consistencia;
- Proposal es la única Aggregate Root;
- ProposalId permanece dentro del límite y es inmutable;
- el estado interno se modifica exclusivamente mediante Proposal;
- una operación válida deja todo el Aggregate consistente;
- una operación rechazada no deja modificaciones parciales;
- Version corresponde a la revisión completa del estado;
- otros Aggregates permanecen fuera del límite;
- las relaciones externas utilizan identificadores;
- Proposal no mantiene referencias mutables hacia otros
  Aggregates;
- Proposal no modifica directamente otros Aggregates;
- cada Aggregate mantiene su propio Lifecycle;
- cada Aggregate mantiene su propia State Machine;
- cada Aggregate mantiene sus propias invariantes;
- cada Aggregate mantiene su propia Version;
- cada Aggregate mantiene su propio Repository;
- la consistencia fuerte se aplica dentro de Proposal;
- la coordinación externa utiliza consistencia eventual cuando
  corresponda;
- Read Models permanecen fuera del límite de escritura;
- Integration permanece fuera del Aggregate;
- Infrastructure no redefine la frontera conceptual.

---

# Matriz de Pertenencia

```text
Concept                         Dentro de Proposal

ProposalId                      Sí

OrganizationId                  Sí, como referencia

CitizenId                       Sí, cuando corresponda como
                                referencia

MembershipId                    Sí, cuando corresponda como
                                referencia

TerritoryId                     Sí, cuando corresponda como
                                referencia

AssemblyId                      Sí, cuando corresponda como
                                referencia

ProposalType                    Sí

ProposalName                    Sí

ProposalPurpose                 Sí

ProposalDescription             Sí

ProposalContent                 Sí

ProposalStatus                  Sí

Lifecycle timestamps            Sí

Version                         Sí

Organization Aggregate          No

Citizen Aggregate               No

Membership Aggregate            No

Role Aggregate                  No

Territory Aggregate             No

Assembly Aggregate              No

Participation Aggregate         No

Voting Aggregate                No

Document Aggregate              No

Notification Aggregate          No

Audit Aggregate                 No

Integration Aggregate           No

Read Models                     No

Infrastructure                  No
```

---

# Diagrama del Boundary

```text
┌─────────────────────────────────────────────────────┐
│                                                     │
│              PROPOSAL CONSISTENCY BOUNDARY          │
│                                                     │
│   ┌─────────────────────────────────────────────┐   │
│   │                                             │   │
│   │              Proposal Root                  │   │
│   │                                             │   │
│   │  ProposalId                                 │   │
│   │  OrganizationId                             │   │
│   │  Proposer References                        │   │
│   │  TerritoryId                                │   │
│   │  AssemblyId                                 │   │
│   │  ProposalType                               │   │
│   │  ProposalName                               │   │
│   │  ProposalPurpose                            │   │
│   │  ProposalDescription                        │   │
│   │  ProposalContent                            │   │
│   │  ProposalStatus                             │   │
│   │  Lifecycle Timestamps                       │   │
│   │  Version                                    │   │
│   │                                             │   │
│   └─────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘

              │
              │ identifiers / events
              ▼

┌─────────────────────────────────────────────────────┐
│               OUTSIDE THE BOUNDARY                  │
│                                                     │
│ Organization                                        │
│ Citizen                                             │
│ Membership                                          │
│ Role                                                │
│ Territory                                           │
│ Assembly                                            │
│ Participation                                       │
│ Voting                                              │
│ Document                                            │
│ Notification                                        │
│ Audit                                               │
│ Integration                                         │
│ Read Models                                         │
│ Infrastructure                                      │
└─────────────────────────────────────────────────────┘
```

---

# Flujo de Consistencia

```text
Command
    │
    ▼
Application Authorization
    │
    ▼
Proposal Aggregate
    │
    ├── Validate Current State
    │
    ├── Validate Invariants
    │
    ├── Execute Behavior
    │
    ├── Update Internal State
    │
    ├── Increment Version
    │
    └── Produce Domain Events
    │
    ▼
Repository
    │
    ├── Validate ExpectedVersion
    │
    └── Persist Aggregate
    │
    ▼
Commit
    │
    ▼
Consistent Proposal Revision
```

---

# Flujo entre Aggregates

```text
Proposal
    │
    ▼
Domain Event
    │
    ▼
Application / Event Coordination
    │
    ├────────► Assembly
    │
    ├────────► Participation
    │
    ├────────► Voting
    │
    ├────────► Document
    │
    ├────────► Notification
    │
    └────────► Audit
```

Cada destino mantiene su propio Consistency Boundary.

---

# Compatibilidad Arquitectónica

El Consistency Boundary de Proposal es compatible con:

- Domain-Driven Design;
- Clean Architecture;
- Hexagonal Architecture;
- CQRS;
- Event Sourcing;
- Event-Driven Architecture;
- SOLID;
- concurrencia optimista;
- consistencia eventual entre Aggregates;
- arquitectura distribuida;
- interoperabilidad basada en contratos.

---

# Principios Arquitectónicos

El Consistency Boundary mantiene:

```text
One Aggregate

=

One Consistency Boundary
```

```text
Proposal

=

Single Aggregate Root
```

```text
Internal State

=

Strong Consistency
```

```text
External Aggregates

=

Independent Consistency Boundaries
```

```text
Aggregate Relationship

≠

Aggregate Ownership
```

```text
Identifier Reference

≠

Mutable Aggregate Reference
```

```text
Contextual Association

≠

Structural Membership
```

```text
Valid Modification

=

Complete Consistent Revision
```

```text
Rejected Modification

=

No Partial State Change
```

```text
Proposal Version

=

Proposal Revision
```

```text
Proposal Version

≠

Other Aggregate Version
```

```text
Read Composition

≠

Write Consistency Boundary
```

```text
Persistence Model

≠

Domain Model
```

```text
External Integration

≠

Aggregate Membership
```

```text
Infrastructure

≠

Domain Boundary
```

---

# Documentación Complementaria

El Consistency Boundary debe interpretarse conjuntamente con:

```text
DOMAIN-007-Aggregate.md

DOMAIN-007A-Lifecycle.md

DOMAIN-007B-State-Machine.md

DOMAIN-007C-Commands.md

DOMAIN-007D-Domain-Events.md

DOMAIN-007E-Invariants.md

DOMAIN-007F-Permissions.md

DOMAIN-007G-Repository-Contract.md

DOMAIN-007H-Examples.md

DOMAIN-007I-Versioning.md

DOMAIN-007K-Integration-Events.md

DOMAIN-007L-Read-Model.md

DOMAIN-007M-Test-Scenarios.md

DOMAIN-007N-Performance-Rules.md

DOMAIN-007O-Security-Model.md

DOMAIN-007P-Extension-Points.md
```

Estos documentos desarrollan responsabilidades específicas sin
alterar el límite fundamental definido en este documento.

---

# Definición de Éxito

El Consistency Boundary del Aggregate **Proposal** establece de
forma explícita que Proposal constituye una única unidad de
consistencia dentro de AURA Core.

Dentro de este límite se protegen conjuntamente:

```text
Identity

Organizational Context

Proposer References

Territorial Context

Assembly Context

Proposal Classification

Proposal Content

Proposal State

Lifecycle Information

Version

Domain Invariants
```

Toda modificación válida debe producir una revisión completa y
consistente del Aggregate.

Una operación inválida debe mantener:

```text
Previous State

Previous Version
```

sin modificaciones parciales.

Los Aggregates:

```text
Organization

Citizen

Membership

Role

Territory

Assembly

Participation

Voting

Document

Notification

Audit

Integration
```

permanecen fuera del Consistency Boundary de Proposal y conservan
sus propias identidades, ciclos de vida, invariantes, versiones,
Repositories y límites de consistencia.

Las relaciones entre estos conceptos se mantienen mediante:

```text
Identifiers

Domain Events

Integration Events

Application Coordination

Repository Contracts
```

sin introducir referencias mutables compartidas ni transacciones
distribuidas como parte del modelo del Aggregate.

De esta forma, Proposal mantiene consistencia fuerte dentro de su
propia frontera y permite consistencia eventual en las
interacciones externas, preservando autonomía, alta cohesión,
bajo acoplamiento, trazabilidad y capacidad de evolución dentro
de la arquitectura DDD distribuida de AURA Core.