# DOMAIN-007E — Proposal Invariants

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
- DOMAIN-007D-Domain-Events.md
- DOMAIN-007F-Permissions.md
- DOMAIN-007G-Repository-Contract.md
- DOMAIN-007I-Versioning.md
- DOMAIN-007J-Consistency-Boundary.md
- CORE-003-Shared-Kernel.md
- CORE-004-Ubiquitous-Language.md
- CORE-006-Domain-Invariants.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Definir las invariantes oficiales del Aggregate **Proposal**.

Las invariantes representan condiciones que deben permanecer
verdaderas durante toda la existencia válida de una Proposal.

Toda operación que pretenda modificar el Aggregate debe preservar
estas condiciones.

Una Proposal nunca puede encontrarse legítimamente en un estado
que viole alguna de sus invariantes.

Este documento establece:

- invariantes de identidad;
- invariantes organizacionales;
- invariantes territoriales;
- invariantes de Assembly;
- invariantes de contenido;
- invariantes de estado;
- invariantes de transición;
- invariantes de presentación;
- invariantes de revisión;
- invariantes de aceptación;
- invariantes de rechazo;
- invariantes de retiro;
- invariantes de archivado;
- invariantes de modificación;
- invariantes de relaciones externas;
- invariantes de consistencia;
- invariantes de versionado;
- invariantes de eventos;
- restricciones estructurales del Aggregate.

---

# Propósito

Las invariantes protegen la consistencia interna de Proposal
independientemente del origen de una operación.

No importa si una modificación fue solicitada desde:

- una interfaz web;
- una aplicación móvil;
- una API;
- un proceso administrativo;
- una integración;
- un Application Service;
- un proceso automatizado.

Toda modificación debe atravesar el comportamiento del Aggregate
y producir un estado válido.

Conceptualmente:

```text
Command

↓

Proposal Aggregate

↓

Validate Current State

↓

Validate Preconditions

↓

Validate Invariants

↓

Apply Behavior

↓

Valid Proposal State
```

Si una invariante no puede preservarse:

```text
Operation Rejected
```

El Aggregate permanece sin modificaciones.

---

# Definición

Una invariante es una condición del dominio que debe permanecer
verdadera antes y después de toda modificación válida del
Aggregate.

Formalmente:

```text
Valid Proposal
    =
All Invariants Satisfied
```

Por lo tanto:

```text
Any Invariant Violated
    =
Invalid Proposal
```

Una operación válida debe satisfacer:

```text
Valid State Before

↓

Domain Operation

↓

Valid State After
```

Nunca:

```text
Valid State

↓

Domain Operation

↓

Invalid State
```

---

# Autoridad de las Invariantes

Las invariantes pertenecen al modelo de dominio.

No pertenecen exclusivamente a:

- Controller;
- API;
- UI;
- base de datos;
- ORM;
- Repository;
- infraestructura;
- cliente externo.

Las capas externas pueden realizar validaciones anticipadas, pero
estas validaciones no sustituyen la protección del Aggregate.

La autoridad final sobre la consistencia de Proposal corresponde
al Aggregate Root:

```text
Proposal
```

---

# Aggregate Root

La única Aggregate Root es:

```text
Proposal
```

Proposal es responsable de proteger todas las invariantes que
pertenecen a su límite de consistencia.

Ninguna propiedad interna puede modificarse evitando el
comportamiento definido por Proposal.

Debe mantenerse:

```text
External Actor

↓

Command

↓

Proposal

↓

Invariant Validation

↓

State Change
```

No:

```text
External Actor

↓

Direct Property Mutation
```

---

# Clasificación de Invariantes

Las invariantes de Proposal se clasifican conceptualmente en:

```text
Identity Invariants

Organizational Invariants

Territorial Invariants

Assembly Reference Invariants

Content Invariants

Lifecycle Invariants

State Invariants

Transition Invariants

Submission Invariants

Review Invariants

Decision Invariants

Withdrawal Invariants

Archival Invariants

Modification Invariants

Relationship Invariants

Consistency Invariants

Version Invariants

Domain Event Invariants
```

Todas forman parte del mismo modelo de consistencia de Proposal.

---

# Invariantes de Identidad

Cada Proposal posee exactamente una identidad:

```text
ProposalId
```

ProposalId:

- es obligatorio;
- es único;
- es inmutable;
- permanece constante durante toda la existencia del Aggregate;
- no depende del nombre;
- no depende del estado;
- no depende de OrganizationId;
- no depende de TerritoryId;
- no depende de AssemblyId;
- no depende de la persistencia;
- no se reutiliza después del archivado.

Debe mantenerse:

```text
ProposalId at Creation
    =
ProposalId at Archive
```

No existe ninguna operación válida que permita:

```text
ChangeProposalId
```

---

# Unicidad de Identidad

Dos Proposal diferentes nunca pueden compartir el mismo:

```text
ProposalId
```

Debe mantenerse:

```text
Proposal A
ProposalId = X
```

y:

```text
Proposal B
ProposalId = Y
```

donde:

```text
X ≠ Y
```

La igualdad de:

- nombre;
- propósito;
- descripción;
- tipo;
- Organization;
- Territory;
- Assembly;

no convierte dos Proposal en el mismo Aggregate.

---

# Invariantes de Organization

Toda Proposal pertenece exactamente a una:

```text
Organization
```

La relación se representa mediante:

```text
OrganizationId
```

OrganizationId:

- es obligatorio;
- debe existir desde la creación;
- identifica el contexto organizacional propietario;
- permanece inmutable durante la vida de Proposal;
- no puede sustituirse por otro OrganizationId;
- no incorpora Organization dentro del Aggregate.

Debe mantenerse:

```text
OrganizationId at Creation
    =
OrganizationId throughout Lifecycle
```

---

# Inmutabilidad de OrganizationId

No está permitido:

```text
ChangeOrganization
```

ni:

```text
TransferProposalToOrganization
```

dentro del modelo establecido para Proposal.

Si una iniciativa debe existir bajo otra Organization, ello no
modifica retroactivamente la propiedad organizacional de la
Proposal existente.

La identidad organizacional forma parte del contexto estructural
del Aggregate.

---

# Existencia Organizacional

Una Proposal no puede crearse sin un contexto organizacional
válido.

Debe cumplirse:

```text
ProposalCreated

⇒

OrganizationId exists
```

La comprobación de existencia de Organization puede requerir
coordinación fuera del Aggregate.

Sin embargo, Proposal nunca contiene:

```text
Organization Aggregate
```

dentro de su límite de consistencia.

---

# Invariantes Territoriales

Proposal puede mantener una referencia territorial mediante:

```text
TerritoryId
```

cuando el contexto de la iniciativa lo requiera.

TerritoryId:

- representa exclusivamente una referencia;
- no incorpora Territory dentro de Proposal;
- no permite modificar Territory;
- debe ser válido cuando se encuentre presente;
- solo puede modificarse mientras el estado permita modificar el
  contexto de Proposal.

Debe mantenerse:

```text
Proposal.TerritoryId

≠

Territory Aggregate ownership
```

---

# Modificación Territorial

En el modelo 1.0 establecido para Proposal, la referencia
territorial puede modificarse únicamente mientras:

```text
ProposalStatus = Draft
```

Debe cumplirse:

```text
ChangeProposalTerritory

requires

ProposalStatus = Draft
```

Después de la presentación formal:

```text
ProposalStatus ≠ Draft
```

la referencia territorial no puede modificarse mediante el
Command editorial definido.

---

# Independencia de Territory

Proposal nunca modifica:

```text
TerritoryName

TerritoryType

TerritoryStatus

ParentTerritoryId

AdministrativeCode

GeometryReference
```

Estas propiedades pertenecen al Aggregate Territory.

La modificación de:

```text
Proposal.TerritoryId
```

representa exclusivamente un cambio dentro de Proposal.

---

# Invariantes de Assembly

Proposal puede mantener una referencia hacia una Assembly
mediante:

```text
AssemblyId
```

AssemblyId:

- representa una referencia externa;
- no incorpora Assembly dentro de Proposal;
- no otorga a Proposal autoridad sobre Assembly;
- debe corresponder a una referencia válida cuando esté presente;
- no modifica el Lifecycle de Assembly;
- no modifica AssemblyStatus.

Debe mantenerse:

```text
Proposal references Assembly

≠

Proposal owns Assembly
```

---

# Asociación con Assembly

En el modelo 1.0, la asociación de Proposal con Assembly se
realiza mientras:

```text
ProposalStatus = Draft
```

Debe cumplirse:

```text
AssociateProposalAssembly

requires

ProposalStatus = Draft
```

Una asociación válida modifica únicamente el contexto de
Proposal.

No modifica:

```text
Assembly
```

---

# Independencia de Assembly

Proposal no puede:

- crear Assembly;
- programar Assembly;
- convocar Assembly;
- iniciar Assembly;
- finalizar Assembly;
- cancelar Assembly;
- archivar Assembly.

Estas responsabilidades pertenecen exclusivamente al Aggregate
Assembly.

---

# Invariantes de Nombre

Proposal mantiene un nombre conceptual:

```text
ProposalName
```

ProposalName debe:

- representar de forma válida la iniciativa;
- cumplir las reglas de valor definidas por el dominio;
- encontrarse presente cuando sea requerido;
- no determinar ProposalId.

La modificación del nombre se realiza mediante:

```text
RenameProposal
```

y únicamente cuando:

```text
ProposalStatus = Draft
```

---

# Invariantes de Propósito

Proposal mantiene:

```text
ProposalPurpose
```

como representación de la finalidad formal de la iniciativa.

ProposalPurpose:

- pertenece al Aggregate;
- debe ser válido;
- no representa ProposalId;
- no representa una Voting;
- no representa una Assembly;
- no representa Participation;
- puede modificarse únicamente mientras el estado permita
  edición.

En el modelo 1.0:

```text
ChangeProposalPurpose

requires

ProposalStatus = Draft
```

---

# Invariantes de Descripción

Proposal puede mantener:

```text
ProposalDescription
```

como información descriptiva de la iniciativa.

La descripción:

- no sustituye ProposalPurpose;
- no constituye identidad;
- no puede utilizarse para incorporar otros Aggregates;
- debe satisfacer las reglas de valor aplicables.

Su modificación mediante:

```text
ChangeProposalDescription
```

requiere:

```text
ProposalStatus = Draft
```

---

# Invariantes de Tipo

Toda Proposal debe poseer una clasificación conceptual válida
cuando el modelo así lo requiera.

La clasificación se representa mediante:

```text
ProposalType
```

ProposalType:

- pertenece al Aggregate;
- no determina ProposalId;
- no altera OrganizationId;
- debe corresponder a un tipo reconocido por el dominio.

En el modelo 1.0:

```text
ChangeProposalType

requires

ProposalStatus = Draft
```

---

# Invariantes de Contenido

El contenido propio de Proposal debe mantenerse dentro del límite
conceptual del Aggregate.

El contenido:

- representa la iniciativa;
- puede contener información necesaria para describirla;
- debe permanecer válido;
- no puede utilizarse para absorber otros Aggregates;
- debe ser modificable únicamente en estados editoriales.

En el modelo 1.0:

```text
UpdateProposalContent

requires

ProposalStatus = Draft
```

---

# Regla de Contenido Completo para Presentación

Una Proposal no puede pasar a:

```text
Submitted
```

si no satisface las condiciones mínimas definidas para una
presentación formal.

Debe mantenerse:

```text
SubmitProposal

requires

Valid Proposal Content
```

Esto incluye los conceptos obligatorios establecidos por el
Aggregate.

Una Proposal incompleta no puede ser considerada formalmente
presentada.

---

# Invariantes de Estado

Toda Proposal posee exactamente un:

```text
ProposalStatus
```

válido.

Los estados oficiales son:

```text
Draft

Submitted

UnderReview

Accepted

Rejected

Withdrawn

Archived
```

No puede existir una Proposal con:

```text
ProposalStatus = null
```

ni con un estado no reconocido por la State Machine.

---

# Estado Inicial

Toda Proposal creada válidamente comienza en:

```text
Draft
```

Debe mantenerse:

```text
ProposalCreated

↓

ProposalStatus = Draft
```

No está permitido crear directamente una Proposal en:

```text
Submitted

UnderReview

Accepted

Rejected

Withdrawn

Archived
```

---

# Modificación Directa del Estado

ProposalStatus nunca puede modificarse mediante asignación
directa.

No está permitido:

```text
proposal.status = Accepted
```

La modificación debe ocurrir mediante comportamiento del
Aggregate.

Ejemplo:

```text
AcceptProposal

↓

Proposal validates operation

↓

UnderReview → Accepted
```

---

# Invariantes de State Machine

Toda transición debe pertenecer a la State Machine oficial.

Las transiciones permitidas son:

```text
Nonexistent
    ↓
Draft
```

```text
Draft
    ↓
Submitted
```

```text
Submitted
    ↓
UnderReview
```

```text
UnderReview
    ├────────► Accepted
    │
    └────────► Rejected
```

```text
Draft
    ↓
Withdrawn
```

```text
Submitted
    ↓
Withdrawn
```

```text
Accepted
    ↓
Archived
```

```text
Rejected
    ↓
Archived
```

```text
Withdrawn
    ↓
Archived
```

Toda transición no representada en este modelo es inválida para
la versión 1.0.

---

# Regla de No Omisión de Estados

No pueden omitirse estados intermedios requeridos por el
Lifecycle.

No está permitido:

```text
Draft

↓

Accepted
```

Debe ocurrir:

```text
Draft

↓

Submitted

↓

UnderReview

↓

Accepted
```

Tampoco está permitido:

```text
Submitted

↓

Accepted
```

Debe ocurrir:

```text
Submitted

↓

UnderReview

↓

Accepted
```

---

# Regla de No Retroceso

El modelo 1.0 no permite retroceder arbitrariamente en el
Lifecycle.

No están permitidas transiciones como:

```text
Submitted → Draft

UnderReview → Submitted

Accepted → UnderReview

Rejected → UnderReview

Withdrawn → Draft

Archived → Accepted
```

La ausencia de una transición en la State Machine significa que
la transición no pertenece al modelo oficial.

---

# Invariantes de Draft

Mientras:

```text
ProposalStatus = Draft
```

Proposal se encuentra en su fase editorial.

En este estado pueden ejecutarse, conforme a Commands y
Permissions:

```text
RenameProposal

ChangeProposalPurpose

ChangeProposalDescription

ChangeProposalType

UpdateProposalContent

ChangeProposalTerritory

AssociateProposalAssembly

SubmitProposal

WithdrawProposal
```

Toda modificación debe preservar las invariantes generales del
Aggregate.

---

# Invariantes de Submitted

Cuando:

```text
ProposalStatus = Submitted
```

la Proposal ha sido presentada formalmente.

Debe mantenerse:

- la presentación ya ocurrió;
- Proposal no continúa comportándose como borrador;
- las operaciones editoriales de Draft dejan de estar
  disponibles;
- puede iniciarse la revisión;
- puede retirarse conforme al Lifecycle establecido.

Operaciones conceptuales permitidas:

```text
StartProposalReview

WithdrawProposal
```

---

# Invariantes de UnderReview

Cuando:

```text
ProposalStatus = UnderReview
```

la Proposal se encuentra formalmente en revisión.

Desde este estado puede producirse exclusivamente una decisión
válida conforme al modelo:

```text
AcceptProposal
```

o:

```text
RejectProposal
```

No puede retirarse mediante el flujo definido para Draft o
Submitted.

No puede volver a Draft.

No puede volver a Submitted.

---

# Invariantes de Accepted

Cuando:

```text
ProposalStatus = Accepted
```

la Proposal ha sido aceptada formalmente.

Accepted:

- representa una decisión consumada;
- no significa que la Proposal haya sido ejecutada;
- no significa que exista automáticamente una Voting;
- no modifica Assembly;
- no modifica Participation;
- no crea Document;
- no envía Notification.

Desde Accepted, el modelo 1.0 permite:

```text
ArchiveProposal
```

No permite regresar al flujo editorial o de revisión.

---

# Invariantes de Rejected

Cuando:

```text
ProposalStatus = Rejected
```

la Proposal ha sido rechazada formalmente.

Rejected:

- conserva ProposalId;
- conserva OrganizationId;
- conserva la trazabilidad;
- no elimina el Aggregate;
- no equivale a Withdrawn.

Desde Rejected, el modelo 1.0 permite:

```text
ArchiveProposal
```

No permite retornar a UnderReview.

---

# Invariantes de Withdrawn

Cuando:

```text
ProposalStatus = Withdrawn
```

la Proposal fue retirada formalmente.

Withdrawn puede alcanzarse desde:

```text
Draft
```

o:

```text
Submitted
```

No puede alcanzarse desde:

```text
UnderReview

Accepted

Rejected

Archived
```

en el Lifecycle establecido.

Withdrawn no equivale a Rejected.

---

# Invariantes de Archived

Cuando:

```text
ProposalStatus = Archived
```

el Aggregate se encuentra en un estado terminal.

Una Proposal archivada:

- conserva ProposalId;
- conserva OrganizationId;
- conserva su historia;
- conserva Version;
- conserva la trazabilidad;
- no admite modificaciones ordinarias;
- no puede volver al flujo activo.

Debe mantenerse:

```text
Archived

↓

No Domain Mutation
```

---

# Invariantes de Presentación

Para ejecutar:

```text
SubmitProposal
```

deben cumplirse simultáneamente las condiciones establecidas por
el dominio.

Como mínimo:

- Proposal existe;
- ProposalStatus es Draft;
- ProposalName es válido;
- ProposalType es válido;
- ProposalPurpose es válido;
- el contenido requerido es válido;
- OrganizationId es válido;
- las referencias obligatorias son válidas;
- las invariantes generales están satisfechas.

Si cualquiera falla:

```text
SubmitProposal

↓

Rejected
```

y:

```text
ProposalStatus remains Draft
```

---

# Invariantes de Inicio de Revisión

Para ejecutar:

```text
StartProposalReview
```

debe cumplirse:

```text
ProposalStatus = Submitted
```

Además:

- Proposal debe haber sido presentada válidamente;
- las precondiciones de revisión deben encontrarse satisfechas;
- el actor debe poseer Permission cuando corresponda;
- ExpectedVersion debe ser válida;
- las invariantes deben permanecer satisfechas.

La operación produce:

```text
Submitted

↓

UnderReview
```

---

# Invariantes de Decisión

Una Proposal solo puede ser aceptada o rechazada desde:

```text
UnderReview
```

Debe mantenerse:

```text
AcceptProposal

requires

ProposalStatus = UnderReview
```

y:

```text
RejectProposal

requires

ProposalStatus = UnderReview
```

No existe aceptación o rechazo directo desde Draft o Submitted.

---

# Exclusividad de Decisión

Una Proposal no puede ser simultáneamente:

```text
Accepted
```

y:

```text
Rejected
```

Debe existir una única transición válida desde UnderReview.

Conceptualmente:

```text
UnderReview

├────────► Accepted
│
└────────► Rejected
```

Una vez confirmada una de las decisiones, la otra deja de ser
válida.

---

# Invariantes de Aceptación

AcceptProposal debe rechazarse cuando:

- Proposal no existe;
- ProposalStatus no es UnderReview;
- el actor no posee Permission;
- la decisión viola una regla del dominio;
- ExpectedVersion no coincide;
- existe una violación de invariantes.

Cuando la operación es válida:

```text
ProposalStatus = Accepted
```

y se produce:

```text
ProposalAccepted
```

---

# Invariantes de Rechazo

RejectProposal debe rechazarse cuando:

- Proposal no existe;
- ProposalStatus no es UnderReview;
- el actor no posee Permission;
- las condiciones de rechazo no están satisfechas;
- RejectionReason es requerido y no es válido;
- ExpectedVersion no coincide;
- existe una violación de invariantes.

Cuando la operación es válida:

```text
ProposalStatus = Rejected
```

y se produce:

```text
ProposalRejected
```

---

# Invariantes de Retiro

WithdrawProposal solo puede ejecutarse cuando:

```text
ProposalStatus = Draft
```

o:

```text
ProposalStatus = Submitted
```

Debe rechazarse cuando:

```text
ProposalStatus = UnderReview
```

```text
ProposalStatus = Accepted
```

```text
ProposalStatus = Rejected
```

```text
ProposalStatus = Withdrawn
```

```text
ProposalStatus = Archived
```

Cuando la operación es válida:

```text
ProposalStatus = Withdrawn
```

---

# Diferencia entre Retiro y Rechazo

Debe mantenerse la distinción:

```text
Withdrawn
    ≠
Rejected
```

Withdrawn representa que Proposal fue retirada del flujo conforme
a las reglas correspondientes.

Rejected representa una decisión formal tomada durante revisión.

No deben utilizarse indistintamente.

---

# Invariantes de Archivado

ArchiveProposal solo puede ejecutarse desde:

```text
Accepted

Rejected

Withdrawn
```

No está permitido archivar directamente desde:

```text
Draft

Submitted

UnderReview
```

Cuando el archivado es válido:

```text
ProposalStatus = Archived
```

y:

```text
ProposalArchived
```

es producido.

---

# Archivado no Equivale a Eliminación

Archived representa cierre lógico del ciclo de vida.

No significa:

```text
Delete Proposal
```

La Proposal conserva:

```text
ProposalId

OrganizationId

Domain History

Version

Traceability
```

La persistencia física pertenece a Infrastructure y no modifica
el significado de Archived.

---

# Invariantes de Modificación

Toda modificación debe realizarse mediante comportamiento
explícito.

No se permiten setters públicos para alterar directamente:

```text
ProposalId

OrganizationId

ProposalStatus

Version
```

Las demás propiedades deben modificarse únicamente mediante los
Commands definidos por el dominio.

---

# Regla de Edición

En el modelo 1.0, las operaciones editoriales están restringidas
a:

```text
ProposalStatus = Draft
```

Estas operaciones incluyen:

```text
RenameProposal

ChangeProposalPurpose

ChangeProposalDescription

ChangeProposalType

UpdateProposalContent

ChangeProposalTerritory

AssociateProposalAssembly
```

Una vez ejecutado:

```text
SubmitProposal
```

la Proposal deja de ser editable mediante estos Commands.

---

# Invariantes de Relaciones Externas

Proposal mantiene relaciones con otros Aggregates exclusivamente
mediante identificadores.

Ejemplos:

```text
OrganizationId

TerritoryId

AssemblyId

CitizenId

MembershipId

ParticipationId

VotingId

DocumentId

NotificationId

AuditId
```

La existencia de una referencia no convierte al Aggregate
referenciado en parte de Proposal.

---

# Regla de No Absorción

Proposal no absorbe:

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

Debe mantenerse:

```text
Proposal
    │
    ├── OrganizationId
    ├── TerritoryId
    └── AssemblyId
```

No:

```text
Proposal
    │
    ├── Organization Aggregate
    ├── Territory Aggregate
    └── Assembly Aggregate
```

Cada Aggregate mantiene su propio límite de consistencia.

---

# Invariantes de Citizen

Cuando Proposal mantenga una referencia contextual a un Citizen,
esta se representa mediante:

```text
CitizenId
```

Proposal no administra:

- identidad cívica;
- datos personales;
- estado del Citizen;
- autenticación;
- verificación del Citizen.

Estas responsabilidades pertenecen al Aggregate Citizen.

---

# Invariantes de Membership

Cuando Proposal requiera contexto de Membership, la relación se
mantiene mediante:

```text
MembershipId
```

Proposal no:

- crea Membership;
- activa Membership;
- suspende Membership;
- asigna Roles;
- modifica Membership.

---

# Invariantes de Participation

Participation mantiene identidad y ciclo de vida propios.

Proposal no incorpora procesos de Participation como entidades
internas.

Debe mantenerse:

```text
Proposal

≠

Participation
```

La existencia de participación asociada a una iniciativa no
modifica el límite del Aggregate Proposal.

---

# Invariantes de Voting

Voting constituye un Aggregate independiente.

Proposal no:

- abre una votación;
- registra votos;
- contabiliza votos;
- cierra una votación;
- calcula resultados de Voting.

Una Proposal puede proporcionar contexto a Voting sin absorber su
comportamiento.

Debe mantenerse:

```text
Proposal Accepted

≠

Voting Completed
```

---

# Invariantes de Document

Document posee identidad y ciclo de vida propios.

Proposal puede mantener referencias documentales cuando el
modelo lo requiera, pero no incorpora el Aggregate Document
completo.

Proposal no administra directamente:

- contenido documental externo;
- versionado documental;
- almacenamiento documental;
- ciclo de vida de Document.

---

# Invariantes de Notification

Proposal no envía Notifications directamente.

Un hecho como:

```text
ProposalSubmitted
```

puede originar posteriormente:

```text
Notification Process
```

pero:

```text
Proposal

≠

Notification
```

La emisión de un Domain Event no incorpora Notification dentro
del Aggregate.

---

# Invariantes de Audit

Proposal no mantiene Audit como entidad interna.

La trazabilidad se conserva mediante:

```text
ProposalId

OrganizationId

ActorId

Version

Domain Events

OccurredAt

CorrelationId

CausationId
```

Audit puede consumir esta información desde su propio contexto.

---

# Invariantes de Integration

Proposal no contiene lógica específica de sistemas externos.

No puede depender conceptualmente de:

```text
Municipal API

FIWARE Broker

HTTP Endpoint

OAuth Provider

External Database
```

Las integraciones se realizan fuera del Aggregate mediante
contratos e Integration Events.

---

# Invariantes de Consistencia

Proposal constituye un único límite de consistencia.

Toda modificación válida debe producir un estado completamente
consistente.

No se permiten actualizaciones parciales.

Debe mantenerse:

```text
Before Operation

Proposal = Valid
```

y:

```text
After Successful Operation

Proposal = Valid
```

Si una operación falla:

```text
Proposal = Previous Valid State
```

---

# Atomicidad Conceptual

Una modificación de Proposal debe tratarse como una única
operación lógica.

Debe mantenerse coherencia entre:

```text
State

+

Version

+

Domain Events
```

No es válido confirmar parcialmente alguno de estos elementos
dejando los demás inconsistentes.

---

# Invariantes de Version

Proposal mantiene:

```text
Version
```

para control de concurrencia optimista.

Version:

- pertenece al Aggregate;
- no puede modificarse directamente;
- es creciente;
- cambia únicamente después de una modificación válida;
- no cambia cuando un Command es rechazado.

Debe mantenerse:

```text
Valid Modification

↓

Version N → Version N + 1
```

---

# ExpectedVersion

Cuando una operación requiera control de concurrencia, la versión
esperada debe coincidir con la versión actual.

Debe cumplirse:

```text
ExpectedVersion
    =
CurrentVersion
```

antes de confirmar la modificación.

Si:

```text
ExpectedVersion
    ≠
CurrentVersion
```

la operación debe ser rechazada como conflicto de concurrencia.

---

# Invariante de Concurrencia

Dos modificaciones concurrentes no pueden confirmar cambios
incompatibles sobre la misma versión del Aggregate.

Ejemplo:

```text
ProposalStatus = UnderReview

Version = 12
```

Dos operaciones compiten:

```text
AcceptProposal
ExpectedVersion = 12
```

```text
RejectProposal
ExpectedVersion = 12
```

Si AcceptProposal confirma:

```text
ProposalStatus = Accepted

Version = 13
```

entonces RejectProposal basado en:

```text
ExpectedVersion = 12
```

debe ser rechazado.

No puede existir simultáneamente:

```text
ProposalAccepted
Version = 13
```

y:

```text
ProposalRejected
Version = 13
```

para la misma Proposal.

---

# Invariantes de Domain Events

Todo cambio relevante definido por el modelo debe producir el
Domain Event correspondiente.

Debe mantenerse:

```text
Valid Domain Change

↓

Version Increment

↓

Corresponding Domain Event
```

Los Domain Events oficiales se encuentran definidos en:

```text
DOMAIN-007D-Domain-Events.md
```

---

# Correspondencia entre Estado y Evento

Las transiciones deben producir eventos coherentes.

```text
Draft → Submitted

requires

ProposalSubmitted
```

```text
Submitted → UnderReview

requires

ProposalReviewStarted
```

```text
UnderReview → Accepted

requires

ProposalAccepted
```

```text
UnderReview → Rejected

requires

ProposalRejected
```

```text
Draft → Withdrawn

requires

ProposalWithdrawn
```

```text
Submitted → Withdrawn

requires

ProposalWithdrawn
```

```text
Accepted → Archived

requires

ProposalArchived
```

```text
Rejected → Archived

requires

ProposalArchived
```

```text
Withdrawn → Archived

requires

ProposalArchived
```

---

# Prohibición de Evento de Éxito ante Rechazo

Cuando una operación es rechazada:

```text
State = Unchanged

Version = Unchanged
```

y no se produce el Domain Event de éxito.

Ejemplo:

```text
ProposalStatus = Submitted

↓

AcceptProposal

↓

Rejected
```

Debe mantenerse:

```text
ProposalStatus = Submitted

Version = Unchanged

ProposalAccepted = Not Produced
```

---

# Invariantes entre Command y Domain Event

Un Command representa intención.

Un Domain Event representa un hecho consumado.

Debe mantenerse:

```text
Command
    ≠
Domain Event
```

Ejemplo:

```text
SubmitProposal
    ≠
ProposalSubmitted
```

La existencia de un Command no garantiza la existencia del
Domain Event correspondiente.

---

# Invariantes de Permissions

Permissions y Domain Invariants son conceptos diferentes.

Permissions responden:

```text
Who may attempt the operation?
```

Las invariantes responden:

```text
Can Proposal remain valid if the operation occurs?
```

Debe mantenerse:

```text
Permission Granted
```

no implica:

```text
Operation Valid
```

Un actor autorizado puede solicitar una operación que el estado
actual del Aggregate no permite.

---

# Orden Conceptual de Validación

Una operación modificadora debe respetar conceptualmente:

```text
Command Received

↓

Application Identity Port

↓

Authorization / Permission

↓

Current State

↓

Preconditions

↓

Domain Invariants

↓

ExpectedVersion

↓

Apply Behavior

↓

Increment Version

↓

Record Domain Event
```

La implementación concreta puede organizar estas
responsabilidades entre las capas correspondientes sin alterar
las reglas conceptuales del dominio.

---

# Invariantes de Repository

Repository no puede utilizarse para evitar las invariantes.

No está permitido conceptualmente:

```text
Repository.updateStatus(
    ProposalId,
    Accepted
)
```

como sustitución de:

```text
AcceptProposal
```

El Repository persiste el estado producido por el Aggregate.

No define por sí mismo la validez de las transiciones.

---

# Invariantes de Persistencia

La tecnología de persistencia no modifica las reglas del
Aggregate.

Las invariantes deben mantenerse independientemente de si
Proposal se persiste utilizando:

- PostgreSQL;
- MongoDB;
- Event Store;
- almacenamiento en memoria;
- otra tecnología.

Debe mantenerse:

```text
Domain Invariants

≠

Database Constraints Only
```

Las restricciones de base de datos pueden reforzar determinadas
reglas técnicas, pero no sustituyen las invariantes del dominio.

---

# Invariantes de Read Model

Los Read Models no constituyen fuente de autoridad para modificar
Proposal.

No está permitido:

```text
Read Model

↓

Modify Proposal
```

Las proyecciones pueden reflejar:

```text
ProposalStatus

ProposalName

ProposalType

OrganizationId

TerritoryId

AssemblyId

Version
```

pero no gobiernan las invariantes del Aggregate.

---

# Invariantes de Integration Events

Integration Events pueden derivarse de hechos confirmados del
dominio.

No pueden utilizarse para declarar internamente una modificación
que Proposal no haya aceptado.

Debe mantenerse:

```text
Valid Proposal Change

↓

Domain Event

↓

Integration Mapping

↓

Integration Event
```

No:

```text
Integration Event

↓

Bypass Proposal Invariants
```

---

# Invariantes de Seguridad

Proposal nunca almacena:

- contraseñas;
- tokens;
- JWT;
- claves privadas;
- secretos criptográficos;
- credenciales;
- sesiones.

Estos conceptos no forman parte del estado válido de Proposal.

La seguridad técnica pertenece a los contextos y capas
correspondientes.

---

# Invariantes de Independencia Tecnológica

La validez de Proposal no puede depender de una tecnología
específica.

Las invariantes no deben expresarse en términos de:

```text
HTTP Status Code

Database Row

MongoDB Document

Kafka Topic

REST Endpoint

JWT Claim

React Component

FastAPI Route

FIWARE Entity
```

Las tecnologías pueden representar o transportar información del
dominio, pero no definen sus reglas conceptuales.

---

# Regla de Estado Siempre Válido

No existe un período legítimo durante el cual Proposal pueda
permanecer parcialmente inválida esperando que otra operación la
corrija.

No debe existir:

```text
Operation A

↓

Invalid Proposal

↓

Operation B

↓

Valid Proposal
```

Cada operación confirmada debe finalizar con:

```text
Valid Proposal
```

---

# Regla de Consistencia entre Documentos

Las invariantes de este documento deben mantenerse coherentes con:

```text
DOMAIN-007-Aggregate.md

DOMAIN-007A-Lifecycle.md

DOMAIN-007B-State-Machine.md

DOMAIN-007C-Commands.md

DOMAIN-007D-Domain-Events.md
```

Ningún documento posterior puede introducir una operación que
viole silenciosamente las invariantes establecidas aquí.

---

# Matriz de Invariantes por Estado

```text
Rule / State                 Draft  Submitted  UnderReview  Accepted  Rejected  Withdrawn  Archived
──────────────────────────────────────────────────────────────────────────────────────────────────
Identity immutable            ✓        ✓           ✓           ✓         ✓          ✓         ✓

Organization immutable        ✓        ✓           ✓           ✓         ✓          ✓         ✓

Rename                         ✓        ✗           ✗           ✗         ✗          ✗         ✗

Change purpose                 ✓        ✗           ✗           ✗         ✗          ✗         ✗

Change description             ✓        ✗           ✗           ✗         ✗          ✗         ✗

Change type                    ✓        ✗           ✗           ✗         ✗          ✗         ✗

Update content                 ✓        ✗           ✗           ✗         ✗          ✗         ✗

Change Territory               ✓        ✗           ✗           ✗         ✗          ✗         ✗

Associate Assembly             ✓        ✗           ✗           ✗         ✗          ✗         ✗

Submit                         ✓        ✗           ✗           ✗         ✗          ✗         ✗

Start review                   ✗        ✓           ✗           ✗         ✗          ✗         ✗

Accept                         ✗        ✗           ✓           ✗         ✗          ✗         ✗

Reject                         ✗        ✗           ✓           ✗         ✗          ✗         ✗

Withdraw                       ✓        ✓           ✗           ✗         ✗          ✗         ✗

Archive                        ✗        ✗           ✗           ✓         ✓          ✓         ✗

Ordinary modification          ✓        Limited     Limited     No        No         No        No
```

La matriz resume las restricciones establecidas por el modelo
1.0.

Las reglas específicas de cada Command prevalecen sobre cualquier
interpretación simplificada de esta representación.

---

# Matriz de Transiciones

```text
Current State    Command                 Result State
─────────────────────────────────────────────────────────
Nonexistent      CreateProposal          Draft

Draft            SubmitProposal          Submitted

Draft            WithdrawProposal        Withdrawn

Submitted        StartProposalReview     UnderReview

Submitted        WithdrawProposal        Withdrawn

UnderReview      AcceptProposal          Accepted

UnderReview      RejectProposal          Rejected

Accepted         ArchiveProposal         Archived

Rejected         ArchiveProposal         Archived

Withdrawn        ArchiveProposal         Archived
```

Cualquier combinación no incluida debe considerarse inválida para
el modelo 1.0, salvo una extensión formal posterior del dominio.

---

# Escenario — Creación Válida

```text
Given

Proposal no existe

And

OrganizationId es válido

And

los datos iniciales son válidos

When

CreateProposal es aceptado

Then

ProposalId es creado

And

ProposalStatus = Draft

And

OrganizationId queda establecido

And

ProposalCreated es producido
```

---

# Escenario — Presentación Inválida

```text
Given

ProposalStatus = Draft

And

ProposalPurpose no satisface las reglas requeridas

When

SubmitProposal es solicitado

Then

el Command es rechazado

And

ProposalStatus permanece Draft

And

Version permanece sin cambios

And

ProposalSubmitted no es producido
```

---

# Escenario — Edición después de Presentación

```text
Given

ProposalStatus = Submitted

When

RenameProposal es solicitado

Then

el Command es rechazado

And

ProposalName permanece sin cambios

And

Version permanece sin cambios

And

ProposalRenamed no es producido
```

---

# Escenario — Revisión Válida

```text
Given

ProposalStatus = Submitted

And

las precondiciones de revisión están satisfechas

When

StartProposalReview es aceptado

Then

ProposalStatus = UnderReview

And

Version incrementa

And

ProposalReviewStarted es producido
```

---

# Escenario — Aceptación Inválida desde Draft

```text
Given

ProposalStatus = Draft

When

AcceptProposal es solicitado

Then

el Command es rechazado

And

ProposalStatus permanece Draft

And

Version permanece sin cambios

And

ProposalAccepted no es producido
```

---

# Escenario — Decisión Exclusiva

```text
Given

ProposalStatus = UnderReview

And

Version = 8

When

AcceptProposal es confirmado

Then

ProposalStatus = Accepted

And

Version = 9

And

ProposalAccepted es producido

When

RejectProposal basado en Version 8 intenta confirmarse

Then

el Command es rechazado

And

ProposalStatus permanece Accepted

And

ProposalRejected no es producido
```

---

# Escenario — Retiro Válido

```text
Given

ProposalStatus = Submitted

When

WithdrawProposal es aceptado

Then

ProposalStatus = Withdrawn

And

Version incrementa

And

ProposalWithdrawn es producido
```

---

# Escenario — Retiro Inválido durante Revisión

```text
Given

ProposalStatus = UnderReview

When

WithdrawProposal es solicitado

Then

el Command es rechazado

And

ProposalStatus permanece UnderReview

And

Version permanece sin cambios

And

ProposalWithdrawn no es producido
```

---

# Escenario — Archivado Válido

```text
Given

ProposalStatus = Rejected

When

ArchiveProposal es aceptado

Then

ProposalStatus = Archived

And

Version incrementa

And

ProposalArchived es producido
```

---

# Escenario — Modificación de Proposal Archivada

```text
Given

ProposalStatus = Archived

When

cualquier Command modificador ordinario es solicitado

Then

el Command es rechazado

And

Proposal permanece sin cambios

And

Version permanece sin cambios

And

ningún Domain Event de éxito es producido
```

---

# Escenario — Intento de Cambiar Organization

```text
Given

Proposal.OrganizationId = Organization-A

When

se intenta establecer:

Proposal.OrganizationId = Organization-B

Then

la operación es inválida

And

OrganizationId permanece Organization-A

And

Version permanece sin cambios
```

---

# Escenario — Referencia Territorial

```text
Given

ProposalStatus = Draft

And

TerritoryId es válido

When

ChangeProposalTerritory es aceptado

Then

Proposal.TerritoryId cambia

And

Territory permanece sin modificaciones

And

Version incrementa

And

ProposalTerritoryChanged es producido
```

---

# Escenario — Asociación con Assembly

```text
Given

ProposalStatus = Draft

And

AssemblyId es válido

When

AssociateProposalAssembly es aceptado

Then

Proposal.AssemblyId queda asociado

And

Assembly permanece sin modificaciones

And

Version incrementa

And

ProposalAssemblyAssociated es producido
```

---

# Escenario — Conflicto de Concurrencia

```text
Given

ProposalStatus = UnderReview

And

Version = 12

And

AcceptProposal.ExpectedVersion = 12

And

RejectProposal.ExpectedVersion = 12

When

AcceptProposal confirma primero

Then

ProposalStatus = Accepted

And

Version = 13

And

ProposalAccepted
AggregateVersion = 13

When

RejectProposal intenta confirmar

Then

ExpectedVersion 12 ≠ CurrentVersion 13

And

RejectProposal es rechazado

And

ProposalStatus permanece Accepted

And

Version permanece 13

And

ProposalRejected no es producido
```

---

# Violación de Invariantes

Cuando una operación viola cualquier invariante:

```text
Operation

↓

Invariant Violation

↓

Reject Operation
```

El resultado obligatorio es:

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

```text
Success Domain Event
    =
Not Produced
```

La operación inválida nunca debe dejar una modificación parcial.

---

# Prioridad de Consistencia

La preservación de las invariantes tiene prioridad sobre la
intención expresada por un Command.

Debe mantenerse:

```text
Command Intent

<

Domain Consistency
```

La existencia de:

- Permission;
- Command válido estructuralmente;
- actor autenticado;
- solicitud técnicamente correcta;

no obliga al Aggregate a aceptar una modificación que viole el
dominio.

---

# Reglas de Evolución

Las invariantes pueden evolucionar cuando evolucione formalmente
el dominio.

Una nueva regla debe evaluarse contra:

```text
Aggregate Definition

Lifecycle

State Machine

Commands

Domain Events

Permissions

Repository Contract

Versioning

Consistency Boundary

Integration Events

Read Models

Test Scenarios

Security Model

Extension Points
```

Una modificación no debe introducir contradicciones silenciosas
entre documentos.

---

# Extensión de Estados

La incorporación futura de un nuevo ProposalStatus requiere
actualizar coherentemente:

```text
DOMAIN-007-Aggregate.md

DOMAIN-007A-Lifecycle.md

DOMAIN-007B-State-Machine.md

DOMAIN-007C-Commands.md

DOMAIN-007D-Domain-Events.md

DOMAIN-007E-Invariants.md
```

y los documentos dependientes correspondientes.

No debe introducirse un nuevo estado únicamente desde
Infrastructure, UI o API.

---

# Extensión de Commands

Un nuevo Command modificador debe definir:

- estado o estados desde los cuales puede ejecutarse;
- precondiciones;
- invariantes afectadas;
- Permission correspondiente;
- modificación esperada;
- Version esperada cuando corresponda;
- Domain Event resultante.

Ningún Command nuevo puede evitar el Aggregate Root.

---

# Extensión de Relaciones

Una nueva relación con otro Aggregate debe mantenerse mediante
identidad cuando corresponda.

La incorporación de una relación no autoriza automáticamente a
Proposal a modificar el Aggregate relacionado.

Debe preservarse:

```text
Reference

≠

Ownership
```

y:

```text
Contextual Relationship

≠

Consistency Boundary Expansion
```

---

# Restricciones

No está permitido:

- modificar ProposalId;
- reutilizar ProposalId;
- crear una Proposal sin OrganizationId;
- modificar OrganizationId;
- modificar ProposalStatus directamente;
- modificar Version directamente;
- omitir estados intermedios del Lifecycle;
- realizar transiciones no definidas;
- editar una Proposal fuera de Draft mediante Commands
  editoriales;
- aceptar una Proposal fuera de UnderReview;
- rechazar una Proposal fuera de UnderReview;
- retirar una Proposal fuera de Draft o Submitted;
- archivar una Proposal fuera de Accepted, Rejected o Withdrawn;
- modificar una Proposal archivada;
- aceptar y rechazar simultáneamente una misma Proposal;
- absorber Organization dentro de Proposal;
- absorber Territory dentro de Proposal;
- absorber Assembly dentro de Proposal;
- absorber Participation dentro de Proposal;
- absorber Voting dentro de Proposal;
- absorber Document dentro de Proposal;
- modificar otro Aggregate desde Proposal;
- utilizar Repository para evitar comportamiento del Aggregate;
- utilizar Read Models para modificar Proposal;
- utilizar Integration Events para evitar invariantes;
- confirmar cambios incompatibles sobre una misma Version;
- incrementar Version ante una operación rechazada;
- producir Domain Events de éxito ante una operación rechazada;
- mantener un estado parcialmente inválido;
- depender de Infrastructure para definir la validez del dominio.

---

# Principios Arquitectónicos

Las invariantes de Proposal preservan:

```text
Aggregate Root
    =
Proposal
```

```text
Identity
    =
Immutable
```

```text
Organization Context
    =
Immutable
```

```text
State Change
    =
Controlled
```

```text
Domain Mutation
    =
Behavior Driven
```

```text
External Aggregate
    =
Referenced by Identity
```

```text
Valid Modification
    =
Invariant Preserving
```

```text
Invalid Modification
    =
No State Change
```

```text
Successful Modification
    =
Version Increment
```

```text
Successful Domain Fact
    =
Domain Event
```

```text
Cross-Aggregate Coordination
    =
Outside Proposal Consistency Boundary
```

Estas reglas mantienen alta cohesión y bajo acoplamiento dentro
del modelo de dominio.

---

# Compatibilidad Arquitectónica

El modelo de invariantes de Proposal es compatible con:

- Domain-Driven Design;
- Aggregate Pattern;
- Clean Architecture;
- Hexagonal Architecture;
- SOLID;
- CQRS;
- Event-Driven Architecture;
- Event Sourcing Compatible;
- Optimistic Concurrency;
- arquitectura distribuida;
- interoperabilidad basada en contratos.

---

# Documentación Complementaria

Las invariantes deben interpretarse conjuntamente con:

```text
DOMAIN-007-Aggregate.md

DOMAIN-007A-Lifecycle.md

DOMAIN-007B-State-Machine.md

DOMAIN-007C-Commands.md

DOMAIN-007D-Domain-Events.md

DOMAIN-007F-Permissions.md

DOMAIN-007G-Repository-Contract.md

DOMAIN-007I-Versioning.md

DOMAIN-007J-Consistency-Boundary.md

DOMAIN-007K-Integration-Events.md

DOMAIN-007L-Read-Model.md

DOMAIN-007M-Test-Scenarios.md

DOMAIN-007N-Performance-Rules.md

DOMAIN-007O-Security-Model.md

DOMAIN-007P-Extension-Points.md
```

Estos documentos profundizan responsabilidades específicas sin
reemplazar las reglas de consistencia establecidas en este
archivo.

---

# Definición de Éxito

Las invariantes del Aggregate **Proposal** constituyen las reglas
obligatorias que determinan cuándo una iniciativa puede
considerarse válida dentro del dominio AURA.

Durante toda su existencia debe mantenerse:

```text
ProposalId
    =
Immutable
```

```text
OrganizationId
    =
Required + Immutable
```

```text
ProposalStatus
    =
Valid State
```

```text
State Transition
    =
Defined by State Machine
```

```text
External Aggregates
    =
Referenced, Not Owned
```

```text
Successful Mutation
    =
Valid State
    +
Version Increment
    +
Domain Event
```

```text
Rejected Mutation
    =
State Unchanged
    +
Version Unchanged
    +
No Success Domain Event
```

El Lifecycle permanece protegido por las transiciones:

```text
Nonexistent

↓

Draft

├──────────────► Submitted
│                   │
│                   ├──────────────► UnderReview
│                   │                    │
│                   │                    ├────► Accepted
│                   │                    │
│                   │                    └────► Rejected
│                   │
│                   └──────────────► Withdrawn
│
└──────────────────► Withdrawn
```

y por los cierres:

```text
Accepted

↓

Archived
```

```text
Rejected

↓

Archived
```

```text
Withdrawn

↓

Archived
```

Las operaciones editoriales permanecen limitadas a:

```text
Draft
```

La decisión permanece limitada a:

```text
UnderReview
```

El retiro permanece limitado a:

```text
Draft

or

Submitted
```

El archivado permanece limitado a:

```text
Accepted

Rejected

Withdrawn
```

y:

```text
Archived
```

permanece terminal.

Proposal nunca absorbe las responsabilidades de Organization,
Citizen, Membership, Role, Territory, Assembly, Participation,
Voting, Document, Notification, Audit o Integration.

De esta forma, **DOMAIN-007E-Invariants.md** establece la
protección conceptual oficial del límite de consistencia del
Aggregate Proposal y garantiza que ninguna operación, Command,
integración, mecanismo de persistencia o decisión tecnológica
pueda dejar al Aggregate en un estado incompatible con su
identidad, Lifecycle, State Machine, reglas de negocio,
versionado y principios Domain-Driven Design establecidos para
AURA Core.