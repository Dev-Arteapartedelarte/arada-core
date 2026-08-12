# DOMAIN-007A — Proposal Lifecycle

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
- CORE-003-Shared-Kernel.md
- CORE-004-Ubiquitous-Language.md
- CORE-006-Domain-Invariants.md
- CORE-008-Aggregate-Design-Rules.md
- CORE-011-Repository-Contracts.md

---

# Objetivo

Definir el ciclo de vida oficial del Aggregate **Proposal**.

El Lifecycle establece los estados conceptuales que una Proposal
puede adoptar desde su creación hasta su archivado y define las
condiciones generales bajo las cuales puede evolucionar entre
ellos.

El Lifecycle forma parte del modelo de dominio.

No representa:

- estados técnicos;
- estados de interfaz;
- estados de persistencia;
- estados de infraestructura;
- estados de Integration;
- estados de Notification;
- estados de Participation;
- estados de Voting.

El ciclo de vida pertenece exclusivamente al Aggregate Proposal.

---

# Propósito

El propósito del Lifecycle es garantizar que toda Proposal
evolucione de forma explícita, consistente y trazable.

El Lifecycle permite distinguir conceptualmente:

- una Proposal que todavía se encuentra en elaboración;
- una Proposal formalmente presentada;
- una Proposal actualmente bajo revisión;
- una Proposal formalmente aceptada;
- una Proposal formalmente rechazada;
- una Proposal retirada;
- una Proposal archivada.

Cada estado representa una condición real del dominio.

No existen transiciones implícitas.

Toda modificación de estado debe ocurrir mediante comportamiento
del Aggregate Root.

---

# Principios

El Lifecycle de Proposal se rige por los siguientes principios:

- Proposal posee un único estado actual;
- todo estado pertenece al lenguaje ubicuo;
- toda transición debe ser explícita;
- toda transición debe partir desde un estado permitido;
- toda transición debe producir un estado válido;
- toda transición debe preservar las invariantes;
- toda transición válida modifica Version;
- toda transición válida puede producir Domain Events;
- una transición rechazada no modifica el Aggregate;
- una transición rechazada no modifica Version;
- una transición rechazada no produce el Domain Event de éxito;
- otros Aggregates no controlan directamente el estado de
  Proposal;
- ningún sistema externo puede modificar ProposalStatus de forma
  directa;
- los estados terminales conservan la identidad histórica de la
  Proposal;
- Archived no representa eliminación física.

---

# Estado del Aggregate

El estado actual de Proposal se representa mediante:

```text
ProposalStatus
```

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

No existen otros estados oficiales en la versión 1.0 del
Aggregate.

---

# Modelo Conceptual del Lifecycle

El flujo principal de Proposal es:

```text
Draft
    │
    ▼
Submitted
    │
    ▼
UnderReview
    │
    ├──────────────► Accepted
    │
    └──────────────► Rejected
```

El flujo de retiro permitido conceptualmente es:

```text
Draft
    │
    └──────────────► Withdrawn

Submitted
    │
    └──────────────► Withdrawn
```

Los estados que pueden finalizar mediante archivado son:

```text
Accepted
    │
    ▼
Archived
```

```text
Rejected
    │
    ▼
Archived
```

```text
Withdrawn
    │
    ▼
Archived
```

El Lifecycle completo puede representarse como:

```text
                         ┌──────────────► Accepted ───────► Archived
                         │
Draft ─────► Submitted ─────► UnderReview
  │            │            │
  │            │            └──────────────► Rejected ───────► Archived
  │            │
  │            └──────────────► Withdrawn ───────────────────► Archived
  │
  └───────────────────────────► Withdrawn
```

No todas las transiciones son válidas desde todos los estados.

La State Machine formal se especificará en:

```text
DOMAIN-007B-State-Machine.md
```

---

# Estado Inicial

Toda Proposal nueva comienza en:

```text
Draft
```

No puede crearse directamente como:

```text
Submitted

UnderReview

Accepted

Rejected

Withdrawn

Archived
```

La creación y la presentación representan operaciones conceptuales
diferentes.

Debe mantenerse:

```text
CreateProposal
    ≠
SubmitProposal
```

La creación establece la existencia de la Proposal.

La presentación establece su ingreso formal al flujo de
tratamiento.

---

# Draft

## Definición

`Draft` representa una Proposal creada pero todavía no presentada
formalmente.

En este estado la iniciativa se encuentra en elaboración.

La Proposal posee identidad desde el momento de su creación.

Por lo tanto:

```text
Draft
    ≠
Nonexistent Proposal
```

Una Proposal en Draft ya constituye un Aggregate válido.

---

## Responsabilidad Conceptual

Draft permite preparar la iniciativa antes de su presentación.

En este estado pueden realizarse, cuando las invariantes lo
permitan, operaciones como:

```text
changeType()

rename()

changePurpose()

changeDescription()

updateContent()

changeTerritory()

associateAssembly()
```

La existencia conceptual de estas operaciones no implica que todas
deban ser válidas en cualquier circunstancia.

Las reglas completas serán desarrolladas en:

```text
DOMAIN-007C-Commands.md

DOMAIN-007E-Invariants.md
```

---

## Propiedades de Draft

Una Proposal en Draft:

- posee ProposalId;
- posee OrganizationId;
- conserva Version;
- puede mantener proponente;
- puede mantener contexto territorial;
- puede mantener contexto de Assembly;
- todavía no se considera formalmente presentada;
- puede continuar siendo modificada conforme a las reglas del
  dominio;
- puede ser presentada;
- puede ser retirada si el modelo lo permite.

---

## Transiciones Permitidas desde Draft

Las transiciones conceptuales permitidas son:

```text
Draft
    ↓
Submitted
```

y:

```text
Draft
    ↓
Withdrawn
```

No se permite:

```text
Draft
    ✕
    ▼
UnderReview
```

```text
Draft
    ✕
    ▼
Accepted
```

```text
Draft
    ✕
    ▼
Rejected
```

```text
Draft
    ✕
    ▼
Archived
```

salvo que una futura evolución oficial del modelo modifique
explícitamente estas reglas.

---

# Submitted

## Definición

`Submitted` representa una Proposal formalmente presentada dentro
del dominio AURA.

La transición hacia Submitted establece que la iniciativa dejó de
ser únicamente un borrador y adquirió condición formal para ser
tratada.

---

## Significado de Presentación

La presentación representa un hecho de dominio.

Conceptualmente:

```text
Draft

↓

SubmitProposal

↓

Submitted
```

La operación de presentación debe validar que la Proposal
satisfaga las condiciones necesarias para ingresar al flujo formal.

---

## Condiciones Generales

Antes de alcanzar Submitted deben encontrarse satisfechas, como
mínimo, las reglas necesarias respecto de:

- identidad;
- contexto organizacional;
- tipo;
- título;
- propósito;
- contenido requerido;
- proponente cuando corresponda;
- contexto territorial cuando sea obligatorio;
- demás invariantes de presentación.

La definición exacta corresponde a:

```text
DOMAIN-007E-Invariants.md
```

---

## SubmittedAt

Cuando Proposal alcanza Submitted puede registrarse:

```text
SubmittedAt
```

SubmittedAt representa el momento formal de presentación.

Una vez establecido como hecho consumado no debe utilizarse como
simple atributo técnico editable.

Su semántica corresponde al momento en que la Proposal fue
presentada válidamente.

---

## SubmittedBy

Cuando el modelo requiera mantener trazabilidad del proponente o
actor responsable de la presentación puede utilizarse una
referencia conceptual como:

```text
CitizenId

MembershipId

ActorId
```

según el contrato correspondiente.

Estas referencias no convierten a Citizen, Membership o Actor en
entidades internas de Proposal.

---

## Modificaciones Posteriores

Una Proposal presentada no mantiene necesariamente el mismo nivel
de libertad de modificación que una Proposal en Draft.

Debe mantenerse:

```text
Draft Editability
    ≠
Submitted Editability
```

Las operaciones permitidas después de la presentación deben quedar
definidas explícitamente por Commands, State Machine e Invariants.

La presentación no puede perder su significado formal mediante una
edición arbitraria.

---

## Transiciones Permitidas desde Submitted

Conceptualmente:

```text
Submitted
    ↓
UnderReview
```

y:

```text
Submitted
    ↓
Withdrawn
```

No se permite directamente:

```text
Submitted
    ✕
    ▼
Accepted
```

```text
Submitted
    ✕
    ▼
Rejected
```

```text
Submitted
    ✕
    ▼
Archived
```

La Proposal debe atravesar las etapas definidas por el Lifecycle.

---

# UnderReview

## Definición

`UnderReview` representa una Proposal que ha ingresado formalmente
al proceso de evaluación correspondiente a su propio ciclo de vida.

Este estado establece que la Proposal está siendo considerada para
una decisión formal dentro del dominio.

---

## Significado de Review

Review representa la condición de evaluación de Proposal.

No significa que Proposal absorba:

- Participation;
- Assembly;
- Voting;
- Document;
- Audit;
- procesos externos de decisión.

Debe mantenerse:

```text
Proposal Review
    ≠
Voting Aggregate
```

y:

```text
Proposal Review
    ≠
Participation Aggregate
```

La revisión describe el estado de Proposal.

Los procesos externos que puedan aportar antecedentes o decisiones
mantienen sus propios Aggregates.

---

## Inicio de Review

Conceptualmente:

```text
Submitted

↓

StartProposalReview

↓

UnderReview
```

La transición debe validar:

- estado origen;
- Permissions;
- invariantes;
- Version;
- precondiciones aplicables.

---

## Condición durante Review

Una Proposal en UnderReview:

- conserva ProposalId;
- conserva OrganizationId;
- mantiene sus referencias;
- conserva trazabilidad;
- se encuentra sujeta a reglas de modificación más restrictivas
  que Draft;
- puede alcanzar Accepted;
- puede alcanzar Rejected.

El modelo no permite asumir que una Proposal puede volver
arbitrariamente a Draft.

---

## Transiciones Permitidas desde UnderReview

Las transiciones conceptuales son:

```text
UnderReview
    ↓
Accepted
```

o:

```text
UnderReview
    ↓
Rejected
```

No se permite:

```text
UnderReview
    ✕
    ▼
Draft
```

```text
UnderReview
    ✕
    ▼
Submitted
```

```text
UnderReview
    ✕
    ▼
Withdrawn
```

```text
UnderReview
    ✕
    ▼
Archived
```

en la versión 1.0 del modelo.

---

# Accepted

## Definición

`Accepted` representa una Proposal que ha sido formalmente
aceptada dentro de su ciclo de vida.

Accepted es un estado del Aggregate Proposal.

No constituye automáticamente el inicio de otro proceso.

---

## Significado

La aceptación confirma que la Proposal ha superado el tratamiento
correspondiente y alcanzó una condición formal de aceptación.

Debe mantenerse:

```text
Proposal Accepted
    ≠
Proposal Executed
```

```text
Proposal Accepted
    ≠
Project Created
```

```text
Proposal Accepted
    ≠
Budget Approved
```

```text
Proposal Accepted
    ≠
Voting Aggregate Completed
```

```text
Proposal Accepted
    ≠
Automatic External Action
```

Cada proceso posterior mantiene su propia responsabilidad.

---

## Origen de Accepted

En la versión 1.0:

```text
Accepted
```

solo puede alcanzarse desde:

```text
UnderReview
```

Conceptualmente:

```text
UnderReview

↓

AcceptProposal

↓

Accepted
```

---

## Consecuencias Conceptuales

Cuando Proposal alcanza Accepted:

- conserva ProposalId;
- conserva OrganizationId;
- conserva su historia;
- conserva las referencias relacionadas;
- su aceptación constituye un hecho consumado;
- puede producir `ProposalAccepted`;
- puede originar Integration Events;
- puede originar procesos posteriores fuera del Aggregate;
- no modifica directamente otros Aggregates.

---

## Relación con Voting

Una Voting puede proporcionar una decisión relevante para
Proposal.

Sin embargo, Voting no modifica directamente:

```text
ProposalStatus
```

Debe mantenerse:

```text
Voting Result

↓

Coordination

↓

AcceptProposal
```

cuando corresponda.

No:

```text
Voting Aggregate

↓

ProposalStatus = Accepted
```

por modificación directa.

Proposal continúa protegiendo su propio estado.

---

## Transición desde Accepted

La transición conceptual permitida es:

```text
Accepted
    ↓
Archived
```

Accepted no vuelve directamente a:

```text
Draft

Submitted

UnderReview

Rejected

Withdrawn
```

---

# Rejected

## Definición

`Rejected` representa una Proposal formalmente rechazada después
del tratamiento correspondiente.

Rejected conserva la existencia histórica de la iniciativa.

---

## Significado

El rechazo representa un hecho de dominio.

Debe mantenerse:

```text
Rejected
    ≠
Deleted
```

Una Proposal rechazada:

- conserva ProposalId;
- conserva OrganizationId;
- conserva su contenido histórico;
- conserva Version;
- conserva Domain Events;
- puede permanecer disponible para consulta;
- puede ser archivada.

---

## Origen de Rejected

En la versión 1.0:

```text
Rejected
```

solo puede alcanzarse desde:

```text
UnderReview
```

mediante:

```text
RejectProposal
```

Conceptualmente:

```text
UnderReview

↓

RejectProposal

↓

Rejected
```

---

## Rejected no cambia a Accepted directamente

Debe mantenerse:

```text
Rejected
    ✕
    ▼
Accepted
```

La decisión de rechazo constituye un hecho consumado del Lifecycle.

Si en una futura evolución del dominio se requiere reconsideración,
reapertura o nueva presentación, dicho comportamiento deberá ser
modelado explícitamente y no inferido dentro de este Lifecycle.

---

## Transición desde Rejected

La transición permitida es:

```text
Rejected
    ↓
Archived
```

---

# Withdrawn

## Definición

`Withdrawn` representa una Proposal retirada formalmente del flujo
normal de tratamiento.

La Proposal continúa existiendo como hecho histórico.

---

## Significado

Withdrawn no representa eliminación.

Debe mantenerse:

```text
Withdrawn
    ≠
Deleted
```

y:

```text
Withdrawn
    ≠
Rejected
```

Rejected representa una decisión de rechazo.

Withdrawn representa el retiro formal de la iniciativa.

Ambos estados poseen significados diferentes dentro del dominio.

---

## Origen de Withdrawn

En la versión 1.0 puede alcanzarse desde:

```text
Draft
```

o:

```text
Submitted
```

Conceptualmente:

```text
Draft

↓

WithdrawProposal

↓

Withdrawn
```

o:

```text
Submitted

↓

WithdrawProposal

↓

Withdrawn
```

---

## Retiro desde UnderReview

La versión 1.0 no establece:

```text
UnderReview
    ↓
Withdrawn
```

como transición válida.

Si el dominio requiere en el futuro permitir el retiro durante
Review, dicha decisión debe incorporarse explícitamente en:

```text
DOMAIN-007-Aggregate.md

DOMAIN-007A-Lifecycle.md

DOMAIN-007B-State-Machine.md

DOMAIN-007C-Commands.md

DOMAIN-007D-Domain-Events.md

DOMAIN-007E-Invariants.md

DOMAIN-007F-Permissions.md

DOMAIN-007M-Test-Scenarios.md
```

No debe inferirse silenciosamente.

---

## Consecuencias Conceptuales

Una Proposal retirada:

- conserva ProposalId;
- conserva OrganizationId;
- conserva trazabilidad;
- conserva su historial;
- no continúa normalmente hacia UnderReview;
- no puede alcanzar Accepted;
- no puede alcanzar Rejected;
- puede alcanzar Archived.

---

## Transición desde Withdrawn

La transición permitida es:

```text
Withdrawn
    ↓
Archived
```

---

# Archived

## Definición

`Archived` representa el estado final de conservación histórica de
Proposal.

La Proposal deja de admitir modificaciones operativas normales.

---

## Naturaleza de Archived

Archived es un estado del dominio.

No representa:

- eliminación física;
- eliminación del Event History;
- eliminación del Audit;
- eliminación de referencias;
- pérdida de ProposalId.

Debe mantenerse:

```text
Archived
    ≠
Deleted
```

---

## Origen de Archived

En la versión 1.0 Archived puede alcanzarse desde:

```text
Accepted

Rejected

Withdrawn
```

Conceptualmente:

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

---

## Estado Terminal

Archived constituye el estado terminal del Lifecycle.

No existen transiciones salientes desde Archived.

Debe mantenerse:

```text
Archived
    =
Terminal State
```

---

## Inmutabilidad

Una Proposal archivada no admite modificaciones ordinarias.

No pueden ejecutarse sobre ella comportamientos como:

```text
rename()

changePurpose()

changeDescription()

updateContent()

changeType()

changeTerritory()

associateAssembly()

submit()

startReview()

accept()

reject()

withdraw()
```

Una operación incompatible debe ser rechazada.

---

# Clasificación de Estados

Los estados pueden agruparse conceptualmente según su función.

---

# Estado de Elaboración

```text
Draft
```

Representa elaboración previa a la presentación.

---

# Estado de Presentación

```text
Submitted
```

Representa una iniciativa formalmente ingresada al flujo.

---

# Estado de Tratamiento

```text
UnderReview
```

Representa una Proposal actualmente bajo evaluación formal.

---

# Estados de Resolución

```text
Accepted

Rejected
```

Representan resultados formales del proceso propio de Proposal.

---

# Estado de Retiro

```text
Withdrawn
```

Representa la salida voluntaria o formal de la Proposal del flujo
normal permitido por el modelo.

---

# Estado Histórico Terminal

```text
Archived
```

Representa conservación histórica sin operación normal posterior.

---

# Estados Activos

Para efectos conceptuales del Lifecycle se consideran estados en
los que Proposal todavía participa en su flujo operativo:

```text
Draft

Submitted

UnderReview
```

Accepted, Rejected y Withdrawn representan estados de resolución o
terminación operacional previa al archivado.

Archived representa el estado terminal.

Esta clasificación no introduce nuevos valores de ProposalStatus.

---

# Estados de Resolución

Los estados:

```text
Accepted

Rejected

Withdrawn
```

representan resultados diferentes.

No deben considerarse equivalentes.

Conceptualmente:

```text
Accepted
    =
Proposal formally accepted
```

```text
Rejected
    =
Proposal formally rejected
```

```text
Withdrawn
    =
Proposal formally withdrawn
```

Los tres pueden posteriormente alcanzar Archived.

---

# Matriz Conceptual de Transiciones

```text
Origin          Destination       Allowed
─────────────────────────────────────────
Draft           Submitted         Yes
Draft           Withdrawn         Yes

Submitted       UnderReview       Yes
Submitted       Withdrawn         Yes

UnderReview     Accepted          Yes
UnderReview     Rejected          Yes

Accepted        Archived          Yes

Rejected        Archived          Yes

Withdrawn       Archived          Yes
```

Toda combinación no declarada como válida debe considerarse
rechazada por la State Machine.

La especificación formal corresponde a:

```text
DOMAIN-007B-State-Machine.md
```

---

# Transiciones Inválidas

No se permiten, entre otras:

```text
Draft
    → UnderReview
```

```text
Draft
    → Accepted
```

```text
Draft
    → Rejected
```

```text
Draft
    → Archived
```

```text
Submitted
    → Accepted
```

```text
Submitted
    → Rejected
```

```text
Submitted
    → Archived
```

```text
UnderReview
    → Draft
```

```text
UnderReview
    → Submitted
```

```text
UnderReview
    → Withdrawn
```

```text
UnderReview
    → Archived
```

```text
Accepted
    → UnderReview
```

```text
Accepted
    → Rejected
```

```text
Rejected
    → UnderReview
```

```text
Rejected
    → Accepted
```

```text
Withdrawn
    → Submitted
```

```text
Withdrawn
    → UnderReview
```

```text
Withdrawn
    → Accepted
```

```text
Archived
    → any state
```

---

# Regla de No Omisión

No se pueden omitir estados intermedios cuando el Lifecycle los
requiere.

Debe mantenerse:

```text
Draft
    ↓
Submitted
    ↓
UnderReview
    ↓
Accepted
```

No:

```text
Draft
    ↓
Accepted
```

La reducción técnica de pasos no modifica las reglas del dominio.

---

# Regla de No Retroceso

El Lifecycle no permite retrocesos arbitrarios.

No se permite convertir:

```text
UnderReview
```

nuevamente en:

```text
Draft
```

por una simple edición.

Tampoco se permite convertir:

```text
Rejected
```

directamente en:

```text
UnderReview
```

sin que exista una futura regla explícita del dominio.

---

# Regla de No Reactivación

Los estados:

```text
Accepted

Rejected

Withdrawn

Archived
```

no se reactivan hacia el flujo principal en la versión 1.0.

Si el dominio requiere posteriormente:

- reconsideración;
- reapertura;
- nueva presentación;
- revisión extraordinaria;

estas capacidades deberán modelarse explícitamente.

No deben inferirse mediante modificación directa de ProposalStatus.

---

# Lifecycle y Aggregate Root

Toda transición debe ejecutarse mediante:

```text
Proposal
```

como única Aggregate Root.

No está permitido:

```text
proposal.status = Accepted
```

como modificación directa.

La transición debe expresarse mediante comportamiento de dominio.

Ejemplo conceptual:

```text
proposal.accept(...)
```

sujeto a todas las reglas correspondientes.

---

# Lifecycle y Commands

Los Commands relacionados con transiciones conceptuales son:

```text
CreateProposal

SubmitProposal

StartProposalReview

AcceptProposal

RejectProposal

WithdrawProposal

ArchiveProposal
```

Cada Command expresa intención.

No garantiza que la transición ocurra.

---

# Relación Command — Estado

Conceptualmente:

```text
CreateProposal
    ↓
Draft
```

```text
SubmitProposal
    ↓
Submitted
```

```text
StartProposalReview
    ↓
UnderReview
```

```text
AcceptProposal
    ↓
Accepted
```

```text
RejectProposal
    ↓
Rejected
```

```text
WithdrawProposal
    ↓
Withdrawn
```

```text
ArchiveProposal
    ↓
Archived
```

La definición completa de Commands corresponde a:

```text
DOMAIN-007C-Commands.md
```

---

# Lifecycle y Domain Events

Toda transición válida puede producir el Domain Event
correspondiente.

Conceptualmente:

```text
ProposalCreated
```

representa la creación en Draft.

```text
ProposalSubmitted
```

representa la transición a Submitted.

```text
ProposalReviewStarted
```

representa la transición a UnderReview.

```text
ProposalAccepted
```

representa la transición a Accepted.

```text
ProposalRejected
```

representa la transición a Rejected.

```text
ProposalWithdrawn
```

representa la transición a Withdrawn.

```text
ProposalArchived
```

representa la transición a Archived.

La definición completa se documentará en:

```text
DOMAIN-007D-Domain-Events.md
```

---

# Regla de Evento Posterior

Un Domain Event de transición solo puede existir después de que la
transición haya sido válidamente aceptada.

Debe mantenerse:

```text
Valid Transition

↓

State Change

↓

Domain Event
```

No:

```text
Command Received

↓

Domain Event

↓

Validation
```

El evento representa un hecho consumado.

---

# Lifecycle e Invariants

Toda transición debe preservar las invariantes definidas en:

```text
DOMAIN-007E-Invariants.md
```

El Lifecycle no puede producir un estado que viole las reglas del
Aggregate.

---

# Invariantes de Lifecycle

Como mínimo:

- ProposalStatus siempre pertenece al conjunto oficial de estados.
- Toda Proposal comienza en Draft.
- Submitted solo puede alcanzarse desde Draft.
- UnderReview solo puede alcanzarse desde Submitted.
- Accepted solo puede alcanzarse desde UnderReview.
- Rejected solo puede alcanzarse desde UnderReview.
- Withdrawn solo puede alcanzarse desde estados permitidos.
- Archived solo puede alcanzarse desde estados terminales
  permitidos.
- Archived no posee transiciones salientes.
- una transición inválida no modifica ProposalStatus.
- una transición inválida no modifica Version.
- una transición inválida no genera un Domain Event de éxito.
- ningún Aggregate externo modifica ProposalStatus directamente.

---

# Lifecycle y Permissions

Las transiciones pueden requerir Permissions.

Los Permissions se documentarán en:

```text
DOMAIN-007F-Permissions.md
```

Debe mantenerse:

```text
Permission
    ≠
Transition Validity
```

Un Actor puede poseer Permission para intentar una operación y aun
así la transición ser rechazada por el estado actual.

Ejemplo:

```text
Actor has AcceptProposal Permission

ProposalStatus = Draft

↓

AcceptProposal rejected
```

---

# Lifecycle y Versioning

Toda transición válida constituye una modificación del Aggregate.

Por lo tanto debe respetar:

```text
DOMAIN-007I-Versioning.md
```

Conceptualmente:

```text
Version N

↓

Valid Lifecycle Transition

↓

Version N+1
```

Una transición rechazada mantiene:

```text
Version N
```

---

# Lifecycle y Consistency Boundary

ProposalStatus pertenece al límite de consistencia de Proposal.

Ningún Aggregate externo puede modificarlo directamente.

Debe mantenerse:

```text
ProposalStatus
    owned by
Proposal
```

La coordinación con otros Aggregates puede producir una intención
sobre Proposal.

La decisión final de transición pertenece siempre al Aggregate.

---

# Relación con Assembly

Assembly puede proporcionar contexto para Proposal.

Sin embargo:

```text
AssemblyStatus
```

no determina automáticamente:

```text
ProposalStatus
```

Ejemplo:

```text
Assembly Completed
```

no implica automáticamente:

```text
Proposal Accepted
```

o:

```text
Proposal Rejected
```

Debe existir una coordinación explícita conforme al dominio.

---

# Relación con Participation

Participation puede aportar información o resultados relacionados
con Proposal.

Sin embargo:

```text
ParticipationStatus
```

no modifica directamente ProposalStatus.

La consecuencia debe ocurrir mediante coordinación de dominio.

---

# Relación con Voting

Voting puede producir un resultado relevante para una Proposal.

Debe mantenerse:

```text
Voting Result

↓

Application / Domain Coordination

↓

Proposal Command

↓

Proposal State Machine
```

No:

```text
Voting Result

↓

Direct ProposalStatus Mutation
```

---

# Relación con Document

La existencia o modificación de Documents no produce
automáticamente transiciones de Proposal.

Cuando un Document sea necesario como precondición, su existencia o
estado podrá ser validado mediante coordinación externa sin
incorporar Document al Aggregate.

---

# Relación con Notification

Notification puede reaccionar a cambios del Lifecycle.

Ejemplo:

```text
ProposalSubmitted

↓

Notification Process
```

Notification no controla la transición.

Debe mantenerse:

```text
Proposal Lifecycle Event

↓

Notification
```

No:

```text
Notification

↓

Proposal Lifecycle State
```

---

# Relación con Audit

Audit puede registrar las transiciones relevantes del Lifecycle.

Audit no modifica ProposalStatus.

Las transiciones pueden proporcionar información como:

```text
ProposalId

PreviousStatus

NewStatus

ActorId

Timestamp

Version

CorrelationId

CausationId
```

cuando los contratos correspondientes lo definan.

---

# Lifecycle e Integration Events

Las transiciones relevantes pueden originar Integration Events.

Conceptualmente:

```text
ProposalSubmitted

↓

Integration Event
```

```text
ProposalAccepted

↓

Integration Event
```

```text
ProposalRejected

↓

Integration Event
```

```text
ProposalWithdrawn

↓

Integration Event
```

```text
ProposalArchived

↓

Integration Event
```

La publicación externa no forma parte de la transición interna.

---

# Fallo de Integración

Si Proposal ya confirmó válidamente una transición, un fallo
posterior de integración no debe reescribir el Lifecycle.

Debe mantenerse:

```text
Proposal State Change Confirmed

+

External Consumer Failure

↓

Proposal State Remains Confirmed
```

La coordinación técnica pertenece a Integration e Infrastructure.

---

# Lifecycle y Read Model

Los Read Models pueden proyectar:

```text
ProposalStatus
```

La proyección no controla el Lifecycle.

Debe mantenerse:

```text
Read Model
    observes
ProposalStatus
```

No:

```text
Read Model
    modifies
ProposalStatus
```

---

# Lifecycle y Eventual Consistency

Una proyección puede encontrarse temporalmente desactualizada.

Ejemplo:

```text
Proposal Aggregate:
Accepted

Read Model:
UnderReview
```

durante una ventana de consistencia eventual.

Esto no significa que Proposal posea dos estados oficiales.

La fuente transaccional continúa siendo el Aggregate.

---

# Lifecycle y Persistencia

El mecanismo de persistencia debe conservar ProposalStatus como
parte del estado del Aggregate.

La base de datos no decide transiciones.

Debe mantenerse:

```text
Domain Transition

↓

Persisted State
```

No:

```text
Database Update

↓

Domain Transition
```

---

# Lifecycle y Repository

El Repository recupera y persiste Proposal respetando el estado
confirmado.

El Repository no:

- acepta transiciones;
- rechaza transiciones de dominio;
- decide Permissions;
- redefine Lifecycle;
- redefine State Machine.

Estas responsabilidades pertenecen al dominio.

---

# Lifecycle y Seguridad

La seguridad no modifica el conjunto de estados.

Authentication y Authorization determinan el acceso a operaciones.

Proposal determina la validez de la transición.

Debe mantenerse:

```text
Authentication

↓

Authorization

↓

Command

↓

Proposal Lifecycle Rules
```

---

# No Estados Técnicos

No forman parte del Lifecycle:

```text
Saving

Saved

Loading

Loaded

Processing

Publishing

PublishedToBroker

Synchronizing

Retrying

Sending

SendingNotification

WaitingForIntegration

FailedDatabaseWrite

HTTPError
```

Estos conceptos pertenecen a Infrastructure, Application o
Integration.

---

# No Estados de UI

Tampoco forman parte de ProposalStatus estados como:

```text
Selected

Expanded

Visible

Hidden

EditingForm

LoadingScreen

Highlighted
```

La interfaz no redefine el dominio.

---

# No Estados de Voting

No forman parte de ProposalStatus:

```text
VotingOpen

VotingClosed

QuorumReached

VoteApproved

VoteRejected
```

Estos conceptos pertenecen al Aggregate Voting cuando
corresponda.

---

# No Estados de Participation

No forman parte del Lifecycle:

```text
ParticipationOpen

ParticipationClosed

ConsultationOpen

ConsultationCompleted
```

cuando representan estados propios de Participation.

---

# No Estados de Assembly

No forman parte de ProposalStatus:

```text
Scheduled

Convoked

InProgress

Completed

Cancelled
```

cuando representan el Lifecycle de Assembly.

Cada Aggregate mantiene su propio lenguaje de estados.

---

# Modificación de Contenido y Lifecycle

El estado actual puede determinar qué partes de Proposal son
modificables.

Conceptualmente:

```text
Draft
    =
Highest Editability
```

mientras los estados posteriores pueden imponer restricciones
adicionales.

Las reglas exactas de edición se documentarán mediante Commands e
Invariants.

El Lifecycle no autoriza modificaciones directas.

---

# Modificación después de Submitted

Toda modificación posterior a Submitted debe conservar el
significado del hecho de presentación.

No debe permitirse una modificación que transforme materialmente la
Proposal presentada en otra iniciativa diferente sin que el dominio
lo modele explícitamente.

La regla exacta corresponde a Invariants.

---

# Modificación durante UnderReview

Una Proposal bajo revisión debe mantener estabilidad suficiente
para que la evaluación corresponda a la iniciativa realmente
presentada.

Las modificaciones permitidas deben ser explícitas.

No deben inferirse por la existencia de setters o mecanismos
técnicos.

---

# Estados de Resolución e Inmutabilidad

Accepted y Rejected representan decisiones formales.

Su contenido debe estar sujeto a restricciones de modificación
coherentes con el hecho ya consumado.

Una implementación no puede tratar estos estados como simples flags
editables.

---

# Withdrawn e Inmutabilidad Operativa

Withdrawn detiene el flujo normal de la Proposal.

No debe utilizarse como mecanismo temporal para editar y volver a
Submitted en la versión 1.0.

Debe mantenerse:

```text
Withdrawn
    ≠
Editable Pause
```

---

# Archived e Inmutabilidad Total Operativa

Archived constituye el estado de conservación histórica.

Las operaciones ordinarias deben ser rechazadas.

La lectura y la auditoría pueden continuar según las reglas de
acceso correspondientes.

---

# Timestamps del Lifecycle

Las transiciones pueden registrar información temporal
correspondiente.

Conceptualmente pueden existir:

```text
CreatedAt

SubmittedAt

ReviewStartedAt

AcceptedAt

RejectedAt

WithdrawnAt

ArchivedAt
```

cuando sean establecidos en los contratos correspondientes.

Estos timestamps representan hechos temporales del Lifecycle.

No son estados independientes.

---

# Regla de Coherencia Temporal

Cuando existan timestamps de Lifecycle deben preservar un orden
coherente con las transiciones efectivamente ocurridas.

Ejemplo conceptual:

```text
CreatedAt
    <=
SubmittedAt
    <=
ReviewStartedAt
    <=
AcceptedAt
```

cuando el flujo haya terminado en Accepted.

La definición exacta se establecerá en Invariants.

---

# Estado y Timestamp

Debe mantenerse:

```text
Timestamp
    ≠
State
```

La existencia de una fecha no produce por sí sola una transición.

Ejemplo:

```text
CurrentTime > SomeDate
```

no cambia automáticamente ProposalStatus salvo que una regla
explícita del dominio defina dicho comportamiento mediante una
operación correspondiente.

---

# Escenario — Creación

```text
Given

datos válidos para crear una Proposal

When

CreateProposal es aceptado

Then

ProposalStatus = Draft

And

se produce ProposalCreated
```

---

# Escenario — Presentación

```text
Given

ProposalStatus = Draft

And

las condiciones de presentación están satisfechas

When

SubmitProposal es aceptado

Then

ProposalStatus = Submitted

And

se registra SubmittedAt cuando corresponda

And

se produce ProposalSubmitted
```

---

# Escenario — Presentación Inválida

```text
Given

ProposalStatus diferente de Draft

When

SubmitProposal es ejecutado

Then

la transición es rechazada

And

ProposalStatus permanece sin cambios

And

Version permanece sin cambios

And

no se produce ProposalSubmitted
```

---

# Escenario — Inicio de Review

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

se produce ProposalReviewStarted
```

---

# Escenario — Inicio de Review desde Draft

```text
Given

ProposalStatus = Draft

When

StartProposalReview es ejecutado

Then

la operación es rechazada

And

ProposalStatus permanece Draft
```

---

# Escenario — Aceptación

```text
Given

ProposalStatus = UnderReview

And

las condiciones de aceptación están satisfechas

When

AcceptProposal es aceptado

Then

ProposalStatus = Accepted

And

se produce ProposalAccepted
```

---

# Escenario — Aceptación desde Submitted

```text
Given

ProposalStatus = Submitted

When

AcceptProposal es ejecutado

Then

la operación es rechazada

And

ProposalStatus permanece Submitted
```

---

# Escenario — Rechazo

```text
Given

ProposalStatus = UnderReview

And

las condiciones de rechazo están satisfechas

When

RejectProposal es aceptado

Then

ProposalStatus = Rejected

And

se produce ProposalRejected
```

---

# Escenario — Rechazo desde Draft

```text
Given

ProposalStatus = Draft

When

RejectProposal es ejecutado

Then

la operación es rechazada

And

ProposalStatus permanece Draft
```

---

# Escenario — Retiro desde Draft

```text
Given

ProposalStatus = Draft

And

las condiciones de retiro están satisfechas

When

WithdrawProposal es aceptado

Then

ProposalStatus = Withdrawn

And

se produce ProposalWithdrawn
```

---

# Escenario — Retiro desde Submitted

```text
Given

ProposalStatus = Submitted

And

las condiciones de retiro están satisfechas

When

WithdrawProposal es aceptado

Then

ProposalStatus = Withdrawn

And

se produce ProposalWithdrawn
```

---

# Escenario — Retiro desde UnderReview

```text
Given

ProposalStatus = UnderReview

When

WithdrawProposal es ejecutado

Then

la transición es rechazada

And

ProposalStatus permanece UnderReview
```

---

# Escenario — Archivado de Accepted

```text
Given

ProposalStatus = Accepted

When

ArchiveProposal es aceptado

Then

ProposalStatus = Archived

And

se produce ProposalArchived
```

---

# Escenario — Archivado de Rejected

```text
Given

ProposalStatus = Rejected

When

ArchiveProposal es aceptado

Then

ProposalStatus = Archived

And

se produce ProposalArchived
```

---

# Escenario — Archivado de Withdrawn

```text
Given

ProposalStatus = Withdrawn

When

ArchiveProposal es aceptado

Then

ProposalStatus = Archived

And

se produce ProposalArchived
```

---

# Escenario — Archivado desde Draft

```text
Given

ProposalStatus = Draft

When

ArchiveProposal es ejecutado

Then

la transición es rechazada

And

ProposalStatus permanece Draft
```

---

# Escenario — Modificación de Archived

```text
Given

ProposalStatus = Archived

When

se intenta ejecutar una operación ordinaria de modificación

Then

la operación es rechazada

And

Proposal permanece sin cambios

And

Version permanece sin cambios
```

---

# Escenario — Rejected a Accepted

```text
Given

ProposalStatus = Rejected

When

AcceptProposal es ejecutado

Then

la operación es rechazada

And

ProposalStatus permanece Rejected
```

---

# Escenario — Accepted a Rejected

```text
Given

ProposalStatus = Accepted

When

RejectProposal es ejecutado

Then

la operación es rechazada

And

ProposalStatus permanece Accepted
```

---

# Escenario — Withdrawn a Submitted

```text
Given

ProposalStatus = Withdrawn

When

SubmitProposal es ejecutado

Then

la operación es rechazada

And

ProposalStatus permanece Withdrawn
```

---

# Escenario — Archived es Terminal

```text
Given

ProposalStatus = Archived

When

se intenta ejecutar cualquier transición del Lifecycle

Then

la transición es rechazada

And

ProposalStatus permanece Archived
```

---

# Reglas de Rechazo

Una transición debe rechazarse cuando:

- el estado origen no corresponde;
- el estado destino no está permitido;
- las invariantes no se satisfacen;
- el Permission requerido no se encuentra satisfecho;
- existe conflicto de Version;
- faltan precondiciones obligatorias;
- Proposal se encuentra Archived;
- la operación intenta omitir un estado obligatorio.

---

# Resultado de una Transición Rechazada

Toda transición rechazada debe mantener:

```text
ProposalStatus
    =
PreviousStatus
```

```text
Version
    =
PreviousVersion
```

```text
Success Domain Event
    =
Not Produced
```

No existen actualizaciones parciales.

---

# Atomicidad

Una transición válida puede modificar conjuntamente información
relacionada con el nuevo estado.

Por ejemplo, una presentación puede modificar:

```text
ProposalStatus

SubmittedAt

Version
```

como una única modificación consistente.

No puede confirmarse:

```text
SubmittedAt
```

sin que la transición correspondiente haya sido confirmada cuando
ambos conceptos formen parte de la misma operación.

---

# Consistencia

Toda transición ocurre dentro del Consistency Boundary de Proposal.

La modificación del estado debe ser atómica respecto de las
invariantes internas del Aggregate.

La coordinación con otros Aggregates ocurre fuera de esta
transacción.

---

# Concurrencia

Dos procesos pueden intentar transiciones concurrentes sobre la
misma Proposal.

Versioning debe impedir que una transición basada en un estado
obsoleto sobrescriba silenciosamente otra transición ya confirmada.

Ejemplo:

```text
Process A:
UnderReview → Accepted

Process B:
UnderReview → Rejected
```

Si Process A confirma primero su modificación, Process B debe
detectar el conflicto de Version antes de persistir su decisión
basada en el estado anterior.

Debe mantenerse:

```text
Concurrent Decision
    ≠
Last Write Wins
```

---

# Trazabilidad

Cada transición relevante debe permitir mantener información
suficiente para reconstruir conceptualmente:

```text
ProposalId

PreviousStatus

NewStatus

ActorId

Timestamp

Version

CorrelationId

CausationId
```

cuando corresponda a los contratos definidos.

La trazabilidad no sustituye el Domain Event.

---

# Reconstrucción

Cuando la arquitectura utilice Event Sourcing Compatible, el
Lifecycle debe poder reconstruirse a partir de los hechos
confirmados.

Ejemplo conceptual:

```text
ProposalCreated
    ↓
Draft

ProposalSubmitted
    ↓
Submitted

ProposalReviewStarted
    ↓
UnderReview

ProposalAccepted
    ↓
Accepted

ProposalArchived
    ↓
Archived
```

El Replay no constituye una nueva transición.

Representa reconstrucción del estado histórico.

---

# Compatibilidad con CQRS

El Write Model administra el Lifecycle.

Los Read Models únicamente proyectan ProposalStatus.

Debe mantenerse:

```text
Write Side
    owns
Lifecycle
```

```text
Read Side
    observes
Lifecycle
```

---

# Compatibilidad con Event-Driven Architecture

Cada cambio relevante del Lifecycle puede originar Domain Events.

Los consumidores pueden reaccionar a dichos hechos sin modificar
directamente Proposal.

Esto permite mantener:

- desacoplamiento;
- consistencia eventual entre Aggregates;
- integración;
- trazabilidad;
- independencia de consumidores.

---

# Compatibilidad con Event Sourcing

El Lifecycle es compatible con reconstrucción desde eventos.

Los estados representan el resultado acumulado de hechos válidos.

No significa que Event Sourcing sea una dependencia obligatoria de
la implementación.

---

# Independencia Tecnológica

El Lifecycle no depende de:

```text
PostgreSQL

MongoDB

MySQL

SQLite

Redis

Kafka

RabbitMQ

HTTP

REST

GraphQL

OAuth

JWT

Django

FastAPI

React

Next.js

FIWARE
```

Estas tecnologías no definen los estados ni las transiciones.

---

# Regla de No Inferencia

No debe introducirse un nuevo estado o transición únicamente porque:

- una interfaz lo requiera;
- una base de datos lo facilite;
- una API externa lo utilice;
- un sistema municipal posea un estado equivalente;
- FIWARE utilice otra representación;
- una integración necesite sincronización;
- una optimización técnica lo sugiera.

Todo nuevo estado debe representar un concepto real del dominio.

---

# Regla de Evolución

El Lifecycle puede evolucionar únicamente mediante una decisión
explícita del modelo de dominio.

La incorporación de un nuevo estado debe evaluar coherencia con:

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

cuando dichos documentos existan y resulten afectados.

No deben existir estados incorporados silenciosamente.

---

# Restricciones

No está permitido:

- crear Proposal directamente en un estado distinto de Draft;
- modificar ProposalStatus mediante setters públicos;
- omitir Submitted antes de UnderReview;
- omitir UnderReview antes de Accepted;
- omitir UnderReview antes de Rejected;
- aceptar una Proposal en Draft;
- rechazar una Proposal en Draft;
- aceptar directamente una Proposal Submitted;
- rechazar directamente una Proposal Submitted;
- volver una Proposal UnderReview a Draft;
- convertir Rejected directamente en Accepted;
- convertir Accepted directamente en Rejected;
- reactivar Withdrawn;
- reactivar Archived;
- modificar normalmente una Proposal Archived;
- permitir que Assembly modifique ProposalStatus directamente;
- permitir que Participation modifique ProposalStatus
  directamente;
- permitir que Voting modifique ProposalStatus directamente;
- utilizar Integration Events para modificar directamente el
  estado;
- utilizar Read Models como fuente de transición;
- utilizar estados técnicos como ProposalStatus;
- utilizar estados de UI como ProposalStatus;
- utilizar estados de otros Aggregates como ProposalStatus;
- ignorar Versioning durante una transición;
- producir Domain Events de éxito después de una transición
  rechazada.

---

# Principios Arquitectónicos

El Lifecycle mantiene:

```text
Create
    ≠
Submit
```

```text
Submit
    ≠
Review
```

```text
Review
    ≠
Voting
```

```text
Accepted
    ≠
Executed
```

```text
Rejected
    ≠
Deleted
```

```text
Withdrawn
    ≠
Rejected
```

```text
Withdrawn
    ≠
Paused
```

```text
Archived
    ≠
Deleted
```

```text
Permission
    ≠
Valid Transition
```

```text
External Result
    ≠
Direct State Mutation
```

```text
Read Model
    ≠
Lifecycle Authority
```

```text
Integration Event
    ≠
Lifecycle Command
```

```text
Technical State
    ≠
Domain State
```

```text
Valid Transition

↓

Valid Aggregate State
```

Estas separaciones preservan la semántica del Aggregate Proposal.

---

# Compatibilidad Arquitectónica

El Lifecycle de Proposal es compatible con:

- Domain-Driven Design;
- Aggregate Pattern;
- Clean Architecture;
- Hexagonal Architecture;
- CQRS;
- Event-Driven Architecture;
- Event Sourcing Compatible;
- Optimistic Concurrency;
- arquitectura distribuida;
- consistencia eventual entre Aggregates.

La compatibilidad no introduce tecnologías concretas dentro del
dominio.

---

# Relación con DOMAIN-007-Aggregate

`DOMAIN-007-Aggregate.md` constituye la fuente conceptual oficial de
Proposal.

Este documento desarrolla exclusivamente el Lifecycle allí
establecido.

No redefine la identidad, relaciones o Consistency Boundary del
Aggregate.

---

# Relación con State Machine

`DOMAIN-007B-State-Machine.md` desarrollará formalmente:

- transiciones;
- estados origen;
- estados destino;
- Guards;
- operaciones permitidas;
- transiciones rechazadas.

Este documento define el ciclo de vida conceptual.

La State Machine formaliza su ejecución.

---

# Relación con Commands

`DOMAIN-007C-Commands.md` definirá las intenciones capaces de
solicitar las transiciones establecidas.

Un Command no modifica Proposal automáticamente.

El Aggregate decide si la transición es válida.

---

# Relación con Domain Events

`DOMAIN-007D-Domain-Events.md` definirá los hechos producidos después
de las transiciones válidas.

Los eventos no sustituyen el Lifecycle.

Representan su evolución consumada.

---

# Relación con Invariants

`DOMAIN-007E-Invariants.md` definirá las reglas que deben
permanecer verdaderas antes y después de cada transición.

Una transición permitida por el grafo puede igualmente ser
rechazada si viola una invariante aplicable.

---

# Relación con Permissions

`DOMAIN-007F-Permissions.md` definirá quién puede intentar cada
operación protegida.

Los Permissions no cambian las transiciones válidas.

---

# Relación con Versioning

`DOMAIN-007I-Versioning.md` definirá la protección frente a
modificaciones concurrentes.

Toda transición confirmada debe integrarse al modelo de Version.

---

# Relación con Consistency Boundary

`DOMAIN-007J-Consistency-Boundary.md` definirá formalmente la
frontera de consistencia.

ProposalStatus permanece dentro de dicho Boundary.

Otros Aggregates permanecen fuera.

---

# Relación con Integration Events

`DOMAIN-007K-Integration-Events.md` permitirá comunicar cambios
relevantes del Lifecycle a consumidores externos.

Los consumidores no modifican ProposalStatus directamente.

---

# Relación con Read Model

`DOMAIN-007L-Read-Model.md` proyectará los estados del Lifecycle
para consulta.

Las proyecciones no ejecutan transiciones.

---

# Relación con Test Scenarios

`DOMAIN-007M-Test-Scenarios.md` deberá verificar:

- cada transición permitida;
- cada transición rechazada;
- estado inicial;
- estados terminales;
- Versioning;
- Domain Events;
- invariantes;
- Permissions;
- ausencia de mutación ante errores.

---

# Relación con Security Model

`DOMAIN-007O-Security-Model.md` deberá mantener la separación entre:

```text
Authorization
```

y:

```text
Lifecycle Validity
```

Un Actor autorizado no puede producir una transición inválida.

---

# Relación con Extension Points

`DOMAIN-007P-Extension-Points.md` deberá establecer las reglas para
evolucionar el Lifecycle sin introducir estados o transiciones de
forma implícita.

---

# Regla de Coherencia Documental

El Lifecycle debe permanecer coherente con la documentación oficial
de Proposal.

Ningún documento complementario puede introducir por sí solo:

- nuevos ProposalStatus;
- nuevas transiciones;
- nuevos estados terminales;
- nuevas rutas de reactivación;
- nuevas reglas de archivado;

sin que la modificación forme parte de una evolución explícita del
modelo oficial.

---

# Definición de Éxito

El Lifecycle del Aggregate **Proposal** establece el ciclo de vida
oficial mediante el cual una iniciativa evoluciona dentro del
ecosistema AURA desde su creación hasta su conservación histórica.

Toda Proposal comienza en:

```text
Draft
```

Puede posteriormente alcanzar:

```text
Submitted
```

cuando es formalmente presentada.

Una Proposal presentada puede alcanzar:

```text
UnderReview
```

cuando ingresa al proceso formal de evaluación.

Una Proposal bajo revisión puede finalizar como:

```text
Accepted
```

o:

```text
Rejected
```

según la decisión válida del dominio.

Una Proposal puede alcanzar:

```text
Withdrawn
```

desde los estados explícitamente permitidos cuando se ejecute un
retiro válido.

Los estados de resolución:

```text
Accepted

Rejected

Withdrawn
```

pueden alcanzar:

```text
Archived
```

como estado terminal de conservación histórica.

El Lifecycle no incorpora estados técnicos, estados de UI, estados
de Voting, estados de Participation ni estados de Assembly.

Cada transición es controlada exclusivamente por Proposal como
Aggregate Root.

Los Permissions determinan quién puede intentar una transición.

La State Machine determina si la transición corresponde al estado
actual.

Las invariantes determinan si el resultado mantiene un Aggregate
válido.

Versioning protege la transición frente a modificaciones
concurrentes incompatibles.

Los Domain Events representan las transiciones válidamente
consumadas.

Los Integration Events permiten comunicar dichos hechos fuera del
Bounded Context sin transferir autoridad sobre el Aggregate.

Assembly, Participation, Voting, Document, Notification, Audit y
cualquier otro Aggregate relacionado permanecen fuera del
Consistency Boundary y no pueden modificar ProposalStatus
directamente.

Debe mantenerse permanentemente:

```text
Draft
    ↓
Submitted
    ↓
UnderReview
    ├────────► Accepted
    │             ↓
    │          Archived
    │
    └────────► Rejected
                  ↓
               Archived
```

junto con el flujo de retiro oficialmente permitido:

```text
Draft
    └────────► Withdrawn
                   ↓
                Archived
```

```text
Submitted
    └────────► Withdrawn
                   ↓
                Archived
```

De esta forma,
**DOMAIN-007A-Lifecycle.md** establece el modelo conceptual y
normativo oficial del ciclo de vida de Proposal, preservando su
identidad, trazabilidad, invariantes, autoridad sobre su propio
estado, límite de consistencia y los principios Domain-Driven
Design establecidos para AURA Core.