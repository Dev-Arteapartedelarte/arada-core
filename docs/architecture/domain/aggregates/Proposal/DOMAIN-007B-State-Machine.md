# DOMAIN-007B — Proposal State Machine

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
- CORE-003-Shared-Kernel.md
- CORE-004-Ubiquitous-Language.md
- CORE-006-Domain-Invariants.md
- CORE-008-Aggregate-Design-Rules.md
- CORE-011-Repository-Contracts.md

---

# Objetivo

Definir la máquina de estados oficial del Aggregate **Proposal**.

La State Machine establece formalmente:

- los estados válidos de Proposal;
- el estado inicial;
- los estados de resolución;
- el estado terminal;
- las transiciones permitidas;
- las transiciones prohibidas;
- los Commands capaces de solicitar una transición;
- los Guards que deben cumplirse;
- los Domain Events esperados;
- las reglas de rechazo;
- la relación entre estado, invariantes, Permissions y Versioning.

La State Machine constituye la formalización ejecutable del ciclo
de vida conceptual definido en:

```text
DOMAIN-007A-Lifecycle.md
```

No introduce un ciclo de vida alternativo.

No redefine el Aggregate.

No permite que Infrastructure, Application, Read Models,
Integrations u otros Aggregates modifiquen directamente el estado
de Proposal.

---

# Propósito

El propósito de la State Machine es garantizar que una Proposal
solo pueda evolucionar mediante transiciones explícitamente
permitidas por el dominio.

La existencia de un Command no garantiza una transición.

La existencia de Permission tampoco garantiza una transición.

Toda solicitud debe ser evaluada considerando:

```text
Current State

↓

Requested Transition

↓

Permission

↓

Guards

↓

Invariants

↓

Version

↓

State Transition
```

Solo después de satisfacer todas las condiciones puede modificarse
el estado del Aggregate.

---

# Principios

La State Machine de Proposal se rige por los siguientes
principios:

- Proposal posee exactamente un estado actual;
- todo estado pertenece al lenguaje ubicuo;
- toda transición posee un estado origen;
- toda transición posee un estado destino;
- toda transición debe estar explícitamente permitida;
- las transiciones no declaradas están prohibidas;
- ningún estado puede ser asignado directamente;
- toda transición ocurre mediante Proposal como Aggregate Root;
- todo Command representa intención y no hecho consumado;
- toda transición válida preserva las invariantes;
- toda transición válida incrementa Version;
- toda transición válida puede producir Domain Events;
- toda transición rechazada conserva el estado anterior;
- toda transición rechazada conserva Version;
- toda transición rechazada no produce el Domain Event de éxito;
- Archived es terminal;
- los estados de otros Aggregates no forman parte de esta State
  Machine;
- los estados técnicos no forman parte de esta State Machine;
- los estados de UI no forman parte de esta State Machine.

---

# Estado

El estado del Aggregate se representa mediante:

```text
ProposalStatus
```

Los únicos estados oficiales de la versión 1.0 son:

```text
Draft

Submitted

UnderReview

Accepted

Rejected

Withdrawn

Archived
```

Cualquier valor diferente es inválido.

---

# Estado Inicial

El único estado inicial permitido es:

```text
Draft
```

Toda Proposal comienza su existencia formal mediante:

```text
CreateProposal
```

y queda en:

```text
Draft
```

Debe mantenerse:

```text
CreateProposal

↓

Draft
```

No está permitido crear una Proposal directamente en:

```text
Submitted

UnderReview

Accepted

Rejected

Withdrawn

Archived
```

---

# Estados de Elaboración

El estado de elaboración es:

```text
Draft
```

Representa una Proposal existente pero todavía no presentada
formalmente.

Draft permite las operaciones de preparación autorizadas por el
Aggregate.

No representa inexistencia.

Debe mantenerse:

```text
Draft
    ≠
Nonexistent
```

---

# Estado de Presentación

El estado de presentación es:

```text
Submitted
```

Representa una Proposal formalmente presentada y disponible para
ingresar al proceso de revisión.

Debe mantenerse:

```text
Draft
    ↓
Submitted
```

La presentación es una transición explícita.

No ocurre automáticamente por completar información.

---

# Estado de Tratamiento

El estado de tratamiento formal es:

```text
UnderReview
```

Representa una Proposal actualmente sometida al proceso de revisión
correspondiente.

Debe mantenerse:

```text
Submitted
    ↓
UnderReview
```

No puede alcanzarse directamente desde Draft.

---

# Estados de Resolución

Los estados de resolución son:

```text
Accepted

Rejected
```

Accepted representa una Proposal formalmente aceptada.

Rejected representa una Proposal formalmente rechazada.

Ambos estados son semánticamente diferentes.

Debe mantenerse:

```text
Accepted
    ≠
Rejected
```

Una Proposal alcanza uno de estos estados únicamente desde:

```text
UnderReview
```

---

# Estado de Retiro

El estado de retiro es:

```text
Withdrawn
```

Representa una Proposal retirada formalmente del flujo normal.

Withdrawn puede alcanzarse desde los estados definidos por el
Lifecycle oficial:

```text
Draft

Submitted
```

No representa rechazo.

No representa eliminación.

No representa una pausa editable.

Debe mantenerse:

```text
Withdrawn
    ≠
Rejected
```

```text
Withdrawn
    ≠
Deleted
```

```text
Withdrawn
    ≠
Paused
```

---

# Estado Terminal

El estado terminal es:

```text
Archived
```

Archived representa conservación histórica.

No representa eliminación física.

No posee transiciones salientes.

Debe mantenerse:

```text
Archived
    =
Terminal State
```

y:

```text
Archived
    ≠
Deleted
```

---

# Diagrama Oficial de Estados

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

El diagrama representa únicamente transiciones válidas.

La ausencia de una flecha entre dos estados significa que la
transición directa está prohibida.

---

# Flujo Principal

El flujo principal de tratamiento es:

```text
Draft

↓

Submitted

↓

UnderReview

├────────► Accepted

└────────► Rejected
```

Los estados de resolución pueden posteriormente alcanzar:

```text
Archived
```

---

# Flujo de Retiro

El flujo de retiro permitido es:

```text
Draft

↓

Withdrawn

↓

Archived
```

o:

```text
Submitted

↓

Withdrawn

↓

Archived
```

En la versión 1.0 no existe:

```text
UnderReview

↓

Withdrawn
```

Esta transición no debe inferirse.

---

# Tabla Oficial de Transiciones

```text
Current State    Command                Next State      Allowed
───────────────────────────────────────────────────────────────
Draft            SubmitProposal         Submitted       Yes
Draft            WithdrawProposal       Withdrawn       Yes

Submitted        StartProposalReview    UnderReview     Yes
Submitted        WithdrawProposal       Withdrawn       Yes

UnderReview      AcceptProposal         Accepted        Yes
UnderReview      RejectProposal         Rejected        Yes

Accepted         ArchiveProposal        Archived        Yes

Rejected         ArchiveProposal        Archived        Yes

Withdrawn        ArchiveProposal        Archived        Yes
```

Toda combinación no declarada en esta tabla debe considerarse
inválida.

---

# Creación del Aggregate

CreateProposal constituye la operación que origina el Aggregate.

Conceptualmente:

```text
Nonexistent

↓

CreateProposal

↓

Draft
```

`Nonexistent` no constituye un ProposalStatus.

Representa únicamente la ausencia previa del Aggregate.

Por lo tanto no debe incorporarse al conjunto de estados.

---

# Transition — SubmitProposal

## Objetivo

Presentar formalmente una Proposal en Draft.

## Estado origen

```text
Draft
```

## Estado destino

```text
Submitted
```

## Command

```text
SubmitProposal
```

## Domain Event esperado

```text
ProposalSubmitted
```

## Guards conceptuales

La transición requiere, como mínimo:

- Proposal existe;
- ProposalStatus es Draft;
- Proposal posee identidad válida;
- OrganizationId es válido;
- los datos requeridos para presentación están completos;
- el tipo de Proposal es válido;
- el título requerido se encuentra definido;
- el propósito requerido se encuentra definido;
- el contenido requerido satisface las reglas del dominio;
- las referencias obligatorias están presentes;
- el Actor posee Permission cuando corresponda;
- las invariantes de presentación se cumplen;
- la Version esperada coincide.

## Resultado

```text
Draft

↓

Submitted
```

La transición puede establecer:

```text
SubmittedAt
```

cuando corresponda al modelo oficial.

---

# Transition — WithdrawProposal desde Draft

## Objetivo

Retirar una Proposal que todavía se encuentra en elaboración.

## Estado origen

```text
Draft
```

## Estado destino

```text
Withdrawn
```

## Command

```text
WithdrawProposal
```

## Domain Event esperado

```text
ProposalWithdrawn
```

## Guards conceptuales

- Proposal existe;
- ProposalStatus es Draft;
- el Actor posee Permission cuando corresponda;
- las reglas de retiro se cumplen;
- las invariantes permanecen válidas;
- la Version esperada coincide.

## Resultado

```text
Draft

↓

Withdrawn
```

Una Proposal retirada desde Draft no puede volver a Submitted en
la versión 1.0.

---

# Transition — StartProposalReview

## Objetivo

Iniciar formalmente la revisión de una Proposal presentada.

## Estado origen

```text
Submitted
```

## Estado destino

```text
UnderReview
```

## Command

```text
StartProposalReview
```

## Domain Event esperado

```text
ProposalReviewStarted
```

## Guards conceptuales

- Proposal existe;
- ProposalStatus es Submitted;
- la presentación es válida;
- las condiciones necesarias para iniciar Review se cumplen;
- el Actor posee Permission cuando corresponda;
- las invariantes permanecen válidas;
- la Version esperada coincide.

## Resultado

```text
Submitted

↓

UnderReview
```

La transición puede establecer:

```text
ReviewStartedAt
```

cuando corresponda.

---

# Transition — WithdrawProposal desde Submitted

## Objetivo

Retirar una Proposal formalmente presentada antes de que alcance
UnderReview.

## Estado origen

```text
Submitted
```

## Estado destino

```text
Withdrawn
```

## Command

```text
WithdrawProposal
```

## Domain Event esperado

```text
ProposalWithdrawn
```

## Guards conceptuales

- Proposal existe;
- ProposalStatus es Submitted;
- la Proposal todavía puede ser retirada;
- el Actor posee Permission cuando corresponda;
- las invariantes permanecen válidas;
- la Version esperada coincide.

## Resultado

```text
Submitted

↓

Withdrawn
```

Una vez confirmada esta transición la Proposal abandona el flujo
normal de revisión.

---

# Transition — AcceptProposal

## Objetivo

Aceptar formalmente una Proposal que se encuentra UnderReview.

## Estado origen

```text
UnderReview
```

## Estado destino

```text
Accepted
```

## Command

```text
AcceptProposal
```

## Domain Event esperado

```text
ProposalAccepted
```

## Guards conceptuales

- Proposal existe;
- ProposalStatus es UnderReview;
- las condiciones de aceptación están satisfechas;
- el Actor posee Permission cuando corresponda;
- las reglas de decisión aplicables se cumplen;
- las invariantes permanecen válidas;
- la Version esperada coincide.

## Resultado

```text
UnderReview

↓

Accepted
```

La transición puede establecer:

```text
AcceptedAt
```

cuando corresponda.

Accepted representa una decisión sobre Proposal.

No representa automáticamente ejecución de la iniciativa.

---

# Transition — RejectProposal

## Objetivo

Rechazar formalmente una Proposal que se encuentra UnderReview.

## Estado origen

```text
UnderReview
```

## Estado destino

```text
Rejected
```

## Command

```text
RejectProposal
```

## Domain Event esperado

```text
ProposalRejected
```

## Guards conceptuales

- Proposal existe;
- ProposalStatus es UnderReview;
- las condiciones de rechazo están satisfechas;
- el Actor posee Permission cuando corresponda;
- las reglas de decisión aplicables se cumplen;
- las invariantes permanecen válidas;
- la Version esperada coincide.

## Resultado

```text
UnderReview

↓

Rejected
```

La transición puede establecer:

```text
RejectedAt
```

cuando corresponda.

Rejected conserva la identidad y trazabilidad de Proposal.

---

# Transition — ArchiveProposal desde Accepted

## Objetivo

Archivar una Proposal previamente aceptada.

## Estado origen

```text
Accepted
```

## Estado destino

```text
Archived
```

## Command

```text
ArchiveProposal
```

## Domain Event esperado

```text
ProposalArchived
```

## Guards conceptuales

- Proposal existe;
- ProposalStatus es Accepted;
- las condiciones de archivado se cumplen;
- el Actor posee Permission cuando corresponda;
- las invariantes permanecen válidas;
- la Version esperada coincide.

## Resultado

```text
Accepted

↓

Archived
```

---

# Transition — ArchiveProposal desde Rejected

## Objetivo

Archivar una Proposal previamente rechazada.

## Estado origen

```text
Rejected
```

## Estado destino

```text
Archived
```

## Command

```text
ArchiveProposal
```

## Domain Event esperado

```text
ProposalArchived
```

## Guards conceptuales

- Proposal existe;
- ProposalStatus es Rejected;
- las condiciones de archivado se cumplen;
- el Actor posee Permission cuando corresponda;
- las invariantes permanecen válidas;
- la Version esperada coincide.

## Resultado

```text
Rejected

↓

Archived
```

---

# Transition — ArchiveProposal desde Withdrawn

## Objetivo

Archivar una Proposal retirada.

## Estado origen

```text
Withdrawn
```

## Estado destino

```text
Archived
```

## Command

```text
ArchiveProposal
```

## Domain Event esperado

```text
ProposalArchived
```

## Guards conceptuales

- Proposal existe;
- ProposalStatus es Withdrawn;
- las condiciones de archivado se cumplen;
- el Actor posee Permission cuando corresponda;
- las invariantes permanecen válidas;
- la Version esperada coincide.

## Resultado

```text
Withdrawn

↓

Archived
```

---

# Guards

Los Guards representan condiciones que deben satisfacerse antes de
ejecutar una transición.

Conceptualmente:

```text
Command

↓

Current State Validation

↓

Permission Validation

↓

Transition Guards

↓

Invariant Validation

↓

Version Validation

↓

Transition
```

Un Guard no constituye un nuevo estado.

Un Guard tampoco modifica el Aggregate.

Su función es impedir una transición inválida.

---

# Categorías de Guards

Los Guards pueden comprender:

```text
State Guards

Identity Guards

Organization Guards

Content Guards

Reference Guards

Permission Guards

Business Rule Guards

Invariant Guards

Version Guards
```

La existencia concreta de cada Guard depende de la transición.

---

# State Guards

Los State Guards verifican que el estado actual permita la
operación.

Ejemplo:

```text
AcceptProposal

requires

ProposalStatus = UnderReview
```

Si:

```text
ProposalStatus = Draft
```

la transición debe rechazarse.

---

# Identity Guards

Los Identity Guards protegen la identidad del Aggregate.

Una transición no puede modificar:

```text
ProposalId
```

ni transferir la Proposal a otra identidad.

---

# Organization Guards

Los Organization Guards protegen el contexto organizacional.

Una transición no puede modificar arbitrariamente:

```text
OrganizationId
```

OrganizationId permanece bajo las reglas de identidad contextual
definidas por Proposal.

---

# Content Guards

Determinadas transiciones pueden exigir que Proposal posea
contenido suficiente.

Por ejemplo, SubmitProposal puede requerir que la Proposal
satisfaga las condiciones mínimas de presentación.

La State Machine no convierte estos datos en estados.

---

# Reference Guards

Cuando una transición dependa de referencias conceptuales válidas,
estas deben comprobarse mediante los mecanismos definidos por la
arquitectura.

La existencia de una referencia externa no convierte el Aggregate
referenciado en parte de Proposal.

---

# Permission Guards

Los Permission Guards determinan si el Actor puede intentar la
operación.

La definición formal corresponde a:

```text
DOMAIN-007F-Permissions.md
```

Debe mantenerse:

```text
Permission Granted
    ≠
Transition Guaranteed
```

Una operación autorizada puede ser rechazada por estado,
invariantes o Versioning.

---

# Invariant Guards

Toda transición debe preservar las invariantes de Proposal.

La definición formal corresponde a:

```text
DOMAIN-007E-Invariants.md
```

Debe mantenerse:

```text
Transition Allowed by Graph

+

Invariant Violation

↓

Transition Rejected
```

El grafo de estados no sustituye las invariantes.

---

# Version Guards

Toda transición debe respetar el modelo de concurrencia optimista.

Conceptualmente:

```text
ExpectedVersion
    =
CurrentVersion
```

antes de confirmar la modificación.

La definición formal corresponde a:

```text
DOMAIN-007I-Versioning.md
```

---

# Orden Conceptual de Validación

La evaluación de una transición debe preservar conceptualmente:

```text
Proposal Exists

↓

Current State Valid

↓

Actor Authorized

↓

Transition Allowed

↓

Guards Satisfied

↓

Invariants Preserved

↓

Version Valid

↓

State Changed

↓

Version Incremented

↓

Domain Event Produced
```

La implementación puede organizar internamente estas validaciones
sin alterar sus responsabilidades conceptuales.

---

# Regla de Transición Explícita

No existe transición implícita por modificación de atributos.

Ejemplo inválido:

```text
proposal.status = "Accepted"
```

Ejemplo conceptual válido:

```text
proposal.accept(...)
```

El comportamiento del Aggregate debe validar todas las condiciones
antes de modificar ProposalStatus.

---

# Regla de Estado Único

Una Proposal posee exactamente un estado actual.

No puede encontrarse simultáneamente en:

```text
Submitted
```

y:

```text
UnderReview
```

ni simultáneamente en:

```text
Accepted
```

y:

```text
Rejected
```

Los estados son mutuamente excluyentes.

---

# Regla de No Omisión

No pueden omitirse estados obligatorios.

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

Tampoco:

```text
Submitted

↓

Accepted
```

---

# Regla de No Retroceso

La State Machine no permite retrocesos no definidos.

No existe:

```text
UnderReview

↓

Submitted
```

ni:

```text
UnderReview

↓

Draft
```

ni:

```text
Accepted

↓

UnderReview
```

ni:

```text
Rejected

↓

UnderReview
```

---

# Regla de No Reactivación

Los estados:

```text
Accepted

Rejected

Withdrawn

Archived
```

no regresan al flujo principal en la versión 1.0.

No existe:

```text
Withdrawn

↓

Submitted
```

ni:

```text
Archived

↓

Draft
```

Una futura capacidad de reapertura deberá ser modelada
explícitamente.

---

# Regla de Resolución Exclusiva

Una Proposal UnderReview puede resolverse como:

```text
Accepted
```

o:

```text
Rejected
```

pero no como ambos.

Una vez confirmada una resolución, una decisión concurrente basada
en la versión anterior debe ser rechazada.

Debe mantenerse:

```text
Accepted XOR Rejected
```

para una misma evolución válida desde UnderReview.

---

# Regla de Retiro

WithdrawProposal solo puede producir Withdrawn desde:

```text
Draft

Submitted
```

No puede producir Withdrawn desde:

```text
UnderReview

Accepted

Rejected

Archived
```

en la versión 1.0.

---

# Regla de Archivado

ArchiveProposal solo puede ejecutarse desde:

```text
Accepted

Rejected

Withdrawn
```

No puede ejecutarse desde:

```text
Draft

Submitted

UnderReview
```

---

# Regla de Terminalidad

Archived no posee transiciones salientes.

Toda solicitud de transición desde Archived debe ser rechazada.

Conceptualmente:

```text
Archived

↓

No Transition
```

---

# Matriz Completa de Estados

```text
From \ To      Draft  Submitted  UnderReview  Accepted  Rejected  Withdrawn  Archived
──────────────────────────────────────────────────────────────────────────────────────
Draft            —       Yes         No          No        No        Yes         No

Submitted        No       —          Yes         No        No        Yes         No

UnderReview      No       No          —          Yes       Yes       No          No

Accepted         No       No          No          —        No        No          Yes

Rejected         No       No          No          No        —        No          Yes

Withdrawn        No       No          No          No        No         —          Yes

Archived         No       No          No          No        No        No           —
```

Esta matriz constituye la representación normativa de las
transiciones directas permitidas en la versión 1.0.

---

# Transiciones Prohibidas desde Draft

Desde Draft están prohibidas:

```text
Draft → UnderReview

Draft → Accepted

Draft → Rejected

Draft → Archived
```

---

# Transiciones Prohibidas desde Submitted

Desde Submitted están prohibidas:

```text
Submitted → Draft

Submitted → Accepted

Submitted → Rejected

Submitted → Archived
```

---

# Transiciones Prohibidas desde UnderReview

Desde UnderReview están prohibidas:

```text
UnderReview → Draft

UnderReview → Submitted

UnderReview → Withdrawn

UnderReview → Archived
```

---

# Transiciones Prohibidas desde Accepted

Desde Accepted están prohibidas:

```text
Accepted → Draft

Accepted → Submitted

Accepted → UnderReview

Accepted → Rejected

Accepted → Withdrawn
```

---

# Transiciones Prohibidas desde Rejected

Desde Rejected están prohibidas:

```text
Rejected → Draft

Rejected → Submitted

Rejected → UnderReview

Rejected → Accepted

Rejected → Withdrawn
```

---

# Transiciones Prohibidas desde Withdrawn

Desde Withdrawn están prohibidas:

```text
Withdrawn → Draft

Withdrawn → Submitted

Withdrawn → UnderReview

Withdrawn → Accepted

Withdrawn → Rejected
```

---

# Transiciones Prohibidas desde Archived

Desde Archived están prohibidas todas las transiciones.

```text
Archived → Draft

Archived → Submitted

Archived → UnderReview

Archived → Accepted

Archived → Rejected

Archived → Withdrawn
```

---

# Commands de Transición

Los Commands que solicitan cambios de estado son:

```text
SubmitProposal

StartProposalReview

AcceptProposal

RejectProposal

WithdrawProposal

ArchiveProposal
```

CreateProposal origina el Aggregate en Draft.

Los Commands se desarrollarán formalmente en:

```text
DOMAIN-007C-Commands.md
```

---

# Commands que No Cambian Estado

Proposal puede poseer Commands que modifiquen información sin
producir una transición de ProposalStatus.

Conceptualmente pueden existir operaciones como:

```text
RenameProposal

ChangeProposalPurpose

ChangeProposalDescription

ChangeProposalType

UpdateProposalContent

ChangeProposalTerritory

AssociateProposalAssembly
```

cuando estén definidas oficialmente.

Estas operaciones deben respetar el estado actual.

La ausencia de transición no elimina la obligación de:

- validar Permissions;
- validar invariantes;
- validar Version;
- incrementar Version cuando exista una modificación válida;
- producir Domain Events cuando corresponda.

---

# Domain Events de Transición

Las transiciones válidas pueden producir:

```text
ProposalCreated

ProposalSubmitted

ProposalReviewStarted

ProposalAccepted

ProposalRejected

ProposalWithdrawn

ProposalArchived
```

La definición formal corresponde a:

```text
DOMAIN-007D-Domain-Events.md
```

---

# Tabla Command — Transition — Event

```text
Command                 From           To             Domain Event
────────────────────────────────────────────────────────────────────
CreateProposal          Nonexistent    Draft          ProposalCreated

SubmitProposal          Draft          Submitted      ProposalSubmitted

WithdrawProposal        Draft          Withdrawn      ProposalWithdrawn

StartProposalReview     Submitted      UnderReview    ProposalReviewStarted

WithdrawProposal        Submitted      Withdrawn      ProposalWithdrawn

AcceptProposal          UnderReview    Accepted       ProposalAccepted

RejectProposal          UnderReview    Rejected       ProposalRejected

ArchiveProposal         Accepted       Archived       ProposalArchived

ArchiveProposal         Rejected       Archived       ProposalArchived

ArchiveProposal         Withdrawn      Archived       ProposalArchived
```

`Nonexistent` no constituye un estado interno del Aggregate.

---

# Atomicidad de Transición

Toda transición válida debe ser atómica dentro del Aggregate.

Conceptualmente:

```text
Validate

↓

Change State

↓

Update Lifecycle Data

↓

Increment Version

↓

Record Domain Event
```

debe constituir una única modificación consistente del Aggregate.

No puede confirmarse parcialmente.

---

# Modificación de Datos de Lifecycle

Una transición puede actualizar información relacionada con el
hecho ocurrido.

Ejemplos conceptuales:

```text
SubmitProposal
    ↓
ProposalStatus = Submitted
SubmittedAt = Timestamp
```

```text
StartProposalReview
    ↓
ProposalStatus = UnderReview
ReviewStartedAt = Timestamp
```

```text
AcceptProposal
    ↓
ProposalStatus = Accepted
AcceptedAt = Timestamp
```

```text
RejectProposal
    ↓
ProposalStatus = Rejected
RejectedAt = Timestamp
```

```text
WithdrawProposal
    ↓
ProposalStatus = Withdrawn
WithdrawnAt = Timestamp
```

```text
ArchiveProposal
    ↓
ProposalStatus = Archived
ArchivedAt = Timestamp
```

Cuando estos atributos formen parte del modelo oficial, deben
actualizarse dentro de la misma consistencia de la transición.

---

# Coherencia Temporal

Los datos temporales asociados al Lifecycle deben ser coherentes
con la secuencia real de estados.

Ejemplo para una Proposal aceptada:

```text
CreatedAt
    <=
SubmittedAt
    <=
ReviewStartedAt
    <=
AcceptedAt
```

Ejemplo para una Proposal retirada después de presentación:

```text
CreatedAt
    <=
SubmittedAt
    <=
WithdrawnAt
```

Los timestamps no producen por sí mismos una transición.

---

# Rechazo de Transición

Una transición debe rechazarse cuando:

- Proposal no existe;
- el estado origen no corresponde;
- el estado destino no está permitido;
- el Command no corresponde a la transición;
- el Actor no posee Permission;
- un Guard falla;
- una invariante sería violada;
- la Version esperada no coincide;
- Proposal se encuentra Archived;
- la operación intenta omitir un estado obligatorio;
- la operación intenta reactivar un estado no reactivable;
- la operación intenta modificar ProposalStatus directamente.

---

# Resultado del Rechazo

Cuando una transición es rechazada:

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

```text
Partial Mutation
    =
Not Allowed
```

El Aggregate debe permanecer exactamente en un estado válido.

---

# Fallo durante la Transición

Una transición no puede dejar el Aggregate parcialmente
modificado.

Si la operación no puede completarse de forma válida:

```text
State Change
    =
Not Confirmed
```

```text
Version Increment
    =
Not Confirmed
```

```text
Success Domain Event
    =
Not Confirmed
```

La atomicidad pertenece al Consistency Boundary de Proposal.

---

# State Machine e Invariantes

La State Machine determina:

```text
Can this state transition to that state?
```

Las Invariants determinan:

```text
Can the Aggregate remain valid after this operation?
```

Ambas condiciones son necesarias.

Debe mantenerse:

```text
Allowed Transition

+

Valid Invariants

=

Potentially Valid Operation
```

La definición formal de invariantes corresponde a:

```text
DOMAIN-007E-Invariants.md
```

---

# State Machine y Permissions

Permissions determina:

```text
Who may attempt the operation?
```

La State Machine determina:

```text
Is the transition valid from the current state?
```

No deben mezclarse ambas responsabilidades.

Ejemplo:

```text
Actor
    has
AcceptProposal Permission

ProposalStatus
    =
Draft
```

Resultado:

```text
AcceptProposal
    =
Rejected
```

La autorización no convierte una transición inválida en válida.

---

# State Machine y Versioning

Toda transición válida debe respetar Optimistic Concurrency.

Conceptualmente:

```text
ExpectedVersion = 7

CurrentVersion = 7

↓

Transition Allowed to Continue
```

Después de confirmar:

```text
Version = 8
```

Si:

```text
ExpectedVersion = 7

CurrentVersion = 8
```

la transición debe ser rechazada por conflicto de concurrencia.

---

# Resoluciones Concurrentes

Una situación crítica puede ocurrir cuando dos actores intentan
resolver simultáneamente una Proposal UnderReview.

Ejemplo:

```text
Current State:
UnderReview

Version:
12
```

Proceso A solicita:

```text
AcceptProposal
ExpectedVersion = 12
```

Proceso B solicita:

```text
RejectProposal
ExpectedVersion = 12
```

Si AcceptProposal se confirma primero:

```text
ProposalStatus = Accepted

Version = 13
```

RejectProposal debe posteriormente fallar porque:

```text
ExpectedVersion = 12

CurrentVersion = 13
```

No debe aplicarse:

```text
Last Write Wins
```

sobre decisiones de dominio concurrentes.

---

# State Machine y Consistency Boundary

ProposalStatus pertenece exclusivamente al Consistency Boundary de
Proposal.

La State Machine también pertenece a dicho límite.

Otros Aggregates pueden producir información utilizada para decidir
si debe solicitarse una transición.

No pueden ejecutar la mutación directamente.

---

# Relación con Organization

Organization proporciona contexto organizacional a Proposal.

Organization no controla ProposalStatus.

Debe mantenerse:

```text
Organization

↓

Context
```

No:

```text
Organization

↓

Direct Proposal State Mutation
```

---

# Relación con Territory

Territory puede proporcionar contexto territorial.

Un cambio en Territory no produce automáticamente una transición de
Proposal.

Proposal mantiene sus propias reglas.

---

# Relación con Assembly

Assembly puede proporcionar contexto formal para una Proposal.

Los estados de Assembly:

```text
Draft

Scheduled

Convoked

InProgress

Completed

Cancelled

Archived
```

no forman parte de ProposalStatus.

Una transición de Assembly no modifica directamente Proposal.

Debe mantenerse:

```text
Assembly Event

↓

Coordination

↓

Proposal Command

↓

Proposal State Machine
```

cuando una regla explícita del dominio lo requiera.

---

# Relación con Participation

Participation mantiene su propio ciclo de vida.

Un estado de Participation no constituye un estado de Proposal.

Participation puede proporcionar información utilizada por un
proceso de coordinación.

No puede modificar ProposalStatus directamente.

---

# Relación con Voting

Voting mantiene su propio Aggregate y State Machine.

Un resultado de Voting puede ser relevante para la decisión sobre
Proposal.

Sin embargo:

```text
Voting Result
```

no equivale a:

```text
ProposalStatus Mutation
```

La coordinación correcta es:

```text
Voting Result

↓

Application / Domain Coordination

↓

AcceptProposal
```

o:

```text
RejectProposal
```

según corresponda.

Proposal vuelve a validar:

- estado;
- Permission;
- Guards;
- invariantes;
- Version.

---

# Regla de Independencia de Voting

No está permitido:

```text
Voting
    sets
Proposal.Status = Accepted
```

ni:

```text
Voting
    sets
Proposal.Status = Rejected
```

La autoridad sobre ProposalStatus pertenece únicamente a Proposal.

---

# Relación con Document

Document puede aportar antecedentes relacionados con Proposal.

La existencia de un Document puede constituir una precondición
externa cuando el dominio así lo defina.

Document no modifica ProposalStatus.

---

# Relación con Notification

Notification puede reaccionar a los Domain Events producidos por la
State Machine.

Ejemplo:

```text
ProposalSubmitted

↓

Notification
```

Notification no solicita ni confirma por sí misma la transición.

---

# Relación con Audit

Audit puede registrar las transiciones.

La información auditada puede incluir:

```text
ProposalId

PreviousStatus

NewStatus

CommandId

ActorId

Timestamp

Version

CorrelationId

CausationId
```

Audit no controla la State Machine.

---

# Relación con Integration

Integration puede publicar hechos relacionados con cambios de
estado.

Debe mantenerse:

```text
Internal State Transition

↓

Domain Event

↓

Integration Event
```

No:

```text
External Integration

↓

Direct ProposalStatus Mutation
```

---

# Integration Events

Determinados Domain Events pueden originar Integration Events.

Ejemplos conceptuales:

```text
ProposalSubmitted

↓

ProposalSubmittedForIntegration
```

```text
ProposalAccepted

↓

ProposalAcceptedForIntegration
```

```text
ProposalRejected

↓

ProposalRejectedForIntegration
```

```text
ProposalWithdrawn

↓

ProposalWithdrawnForIntegration
```

```text
ProposalArchived

↓

ProposalArchivedForIntegration
```

La definición oficial corresponde a:

```text
DOMAIN-007K-Integration-Events.md
```

---

# Fallo de Integration

Un fallo posterior en Integration no revierte automáticamente una
transición confirmada.

Ejemplo:

```text
UnderReview

↓

Accepted

↓

ProposalAccepted

↓

Integration Failure
```

El estado continúa siendo:

```text
Accepted
```

La recuperación de Integration pertenece a su propia
responsabilidad.

---

# State Machine y Read Model

Los Read Models proyectan el estado.

Conceptualmente:

```text
Proposal State Machine

↓

Domain Event

↓

Projection

↓

ProposalStatus Read Model
```

El Read Model no modifica la State Machine.

---

# Consistencia Eventual del Read Model

Puede existir temporalmente:

```text
Aggregate:
Accepted

Read Model:
UnderReview
```

mientras se actualiza la proyección.

La State Machine no consulta el Read Model para determinar su estado
oficial.

---

# State Machine y Repository

El Repository recupera y persiste el Aggregate.

No define las transiciones.

No debe contener lógica como:

```text
if status == "Draft":
    allow submit
```

como sustitución de la lógica del Aggregate.

La autoridad pertenece a Proposal.

---

# State Machine y Persistencia

La persistencia conserva el estado resultante.

Debe mantenerse:

```text
Domain Decision

↓

ProposalStatus Change

↓

Persistence
```

No:

```text
Database Status Update

↓

Domain Decision
```

---

# State Machine y CQRS

En CQRS:

```text
Write Side
```

posee la State Machine.

El:

```text
Read Side
```

únicamente observa y proyecta el estado.

Debe mantenerse:

```text
Command Side
    owns
State Transition
```

```text
Query Side
    observes
State
```

---

# State Machine y Event Sourcing

Cuando se utilice Event Sourcing Compatible, el estado puede
reconstruirse mediante Domain Events.

Ejemplo:

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

Replay no ejecuta nuevamente Commands.

Replay reconstruye hechos ya confirmados.

---

# State Machine y Seguridad

Authentication determina identidad técnica.

Authorization determina si el Actor puede solicitar una operación.

La State Machine determina si la transición es válida.

Debe mantenerse:

```text
Authentication

↓

Authorization

↓

Command

↓

State Machine

↓

Invariants

↓

Transition
```

---

# No Estados Técnicos

No forman parte de ProposalStatus:

```text
Loading

Saving

Saved

Processing

Queued

Retrying

Synchronizing

Publishing

Published

Failed

DatabaseError

NetworkError

HTTPError
```

Estos estados pertenecen a capas técnicas cuando corresponda.

---

# No Estados de UI

No forman parte de ProposalStatus:

```text
Selected

Expanded

Collapsed

Editing

Viewing

Highlighted

Hidden

Visible
```

La UI no redefine la State Machine.

---

# No Estados de Assembly

No forman parte de ProposalStatus estados propios de Assembly como:

```text
Scheduled

Convoked

InProgress

Completed

Cancelled
```

---

# No Estados de Voting

No forman parte de ProposalStatus estados propios de Voting como:

```text
Open

Closed

Counting

Validated
```

cuando correspondan al modelo de Voting.

---

# No Estados de Participation

No forman parte de ProposalStatus estados propios de Participation.

Cada Aggregate mantiene su State Machine independiente.

---

# Escenario — Crear Proposal

```text
Given

no existe una Proposal con ProposalId

When

CreateProposal es aceptado

Then

Proposal es creada

And

ProposalStatus = Draft

And

Version se establece según el modelo de Versioning

And

ProposalCreated es producido
```

---

# Escenario — Submit válido

```text
Given

ProposalStatus = Draft

And

todos los Guards están satisfechos

When

SubmitProposal es ejecutado

Then

ProposalStatus = Submitted

And

Version incrementa

And

ProposalSubmitted es producido
```

---

# Escenario — Submit desde Submitted

```text
Given

ProposalStatus = Submitted

When

SubmitProposal es ejecutado

Then

la transición es rechazada

And

ProposalStatus permanece Submitted

And

Version permanece sin cambios

And

ProposalSubmitted no es producido
```

---

# Escenario — Start Review válido

```text
Given

ProposalStatus = Submitted

And

todos los Guards están satisfechos

When

StartProposalReview es ejecutado

Then

ProposalStatus = UnderReview

And

Version incrementa

And

ProposalReviewStarted es producido
```

---

# Escenario — Start Review desde Draft

```text
Given

ProposalStatus = Draft

When

StartProposalReview es ejecutado

Then

la transición es rechazada

And

ProposalStatus permanece Draft

And

Version permanece sin cambios
```

---

# Escenario — Accept válido

```text
Given

ProposalStatus = UnderReview

And

todos los Guards están satisfechos

When

AcceptProposal es ejecutado

Then

ProposalStatus = Accepted

And

Version incrementa

And

ProposalAccepted es producido
```

---

# Escenario — Accept desde Draft

```text
Given

ProposalStatus = Draft

When

AcceptProposal es ejecutado

Then

la transición es rechazada

And

ProposalStatus permanece Draft

And

Version permanece sin cambios
```

---

# Escenario — Accept desde Submitted

```text
Given

ProposalStatus = Submitted

When

AcceptProposal es ejecutado

Then

la transición es rechazada

And

ProposalStatus permanece Submitted

And

Version permanece sin cambios
```

---

# Escenario — Reject válido

```text
Given

ProposalStatus = UnderReview

And

todos los Guards están satisfechos

When

RejectProposal es ejecutado

Then

ProposalStatus = Rejected

And

Version incrementa

And

ProposalRejected es producido
```

---

# Escenario — Reject desde Accepted

```text
Given

ProposalStatus = Accepted

When

RejectProposal es ejecutado

Then

la transición es rechazada

And

ProposalStatus permanece Accepted
```

---

# Escenario — Withdraw desde Draft

```text
Given

ProposalStatus = Draft

And

todos los Guards están satisfechos

When

WithdrawProposal es ejecutado

Then

ProposalStatus = Withdrawn

And

Version incrementa

And

ProposalWithdrawn es producido
```

---

# Escenario — Withdraw desde Submitted

```text
Given

ProposalStatus = Submitted

And

todos los Guards están satisfechos

When

WithdrawProposal es ejecutado

Then

ProposalStatus = Withdrawn

And

Version incrementa

And

ProposalWithdrawn es producido
```

---

# Escenario — Withdraw desde UnderReview

```text
Given

ProposalStatus = UnderReview

When

WithdrawProposal es ejecutado

Then

la transición es rechazada

And

ProposalStatus permanece UnderReview

And

Version permanece sin cambios
```

---

# Escenario — Archive Accepted

```text
Given

ProposalStatus = Accepted

And

todos los Guards están satisfechos

When

ArchiveProposal es ejecutado

Then

ProposalStatus = Archived

And

Version incrementa

And

ProposalArchived es producido
```

---

# Escenario — Archive Rejected

```text
Given

ProposalStatus = Rejected

And

todos los Guards están satisfechos

When

ArchiveProposal es ejecutado

Then

ProposalStatus = Archived

And

Version incrementa

And

ProposalArchived es producido
```

---

# Escenario — Archive Withdrawn

```text
Given

ProposalStatus = Withdrawn

And

todos los Guards están satisfechos

When

ArchiveProposal es ejecutado

Then

ProposalStatus = Archived

And

Version incrementa

And

ProposalArchived es producido
```

---

# Escenario — Archive Draft

```text
Given

ProposalStatus = Draft

When

ArchiveProposal es ejecutado

Then

la transición es rechazada

And

ProposalStatus permanece Draft

And

Version permanece sin cambios
```

---

# Escenario — Archived Terminal

```text
Given

ProposalStatus = Archived

When

cualquier Command de transición es ejecutado

Then

la transición es rechazada

And

ProposalStatus permanece Archived

And

Version permanece sin cambios
```

---

# Escenario — Resolución Concurrente

```text
Given

ProposalStatus = UnderReview

And

Version = 15

And

Actor A solicita AcceptProposal con ExpectedVersion = 15

And

Actor B solicita RejectProposal con ExpectedVersion = 15

When

AcceptProposal es confirmado primero

Then

ProposalStatus = Accepted

And

Version = 16

When

RejectProposal intenta confirmar con ExpectedVersion = 15

Then

RejectProposal es rechazado por conflicto de Version

And

ProposalStatus permanece Accepted

And

Version permanece 16
```

---

# Escenario — Permission sin Estado Válido

```text
Given

Actor posee Permission para AcceptProposal

And

ProposalStatus = Draft

When

AcceptProposal es ejecutado

Then

la transición es rechazada

Because

Draft → Accepted no es una transición válida
```

---

# Escenario — Estado Válido sin Permission

```text
Given

ProposalStatus = UnderReview

And

Actor no posee Permission para AcceptProposal

When

AcceptProposal es ejecutado

Then

la operación es rechazada

And

ProposalStatus permanece UnderReview
```

---

# Escenario — Invariante Violada

```text
Given

el estado actual permitiría conceptualmente una transición

And

una invariante obligatoria no se satisface

When

el Command correspondiente es ejecutado

Then

la transición es rechazada

And

Proposal permanece sin cambios
```

---

# Escenario — Version Conflict

```text
Given

ExpectedVersion != CurrentVersion

When

se intenta confirmar una transición

Then

la operación es rechazada

And

ProposalStatus permanece sin cambios

And

no se produce el Domain Event de éxito
```

---

# Regla de Idempotencia Conceptual

La repetición de un Command de transición no implica que la
transición pueda ejecutarse nuevamente.

Ejemplo:

```text
Draft

↓

SubmitProposal

↓

Submitted
```

Una nueva ejecución de:

```text
SubmitProposal
```

sobre:

```text
Submitted
```

no vuelve a producir:

```text
ProposalSubmitted
```

La State Machine evalúa siempre el estado actual.

---

# Regla de Autoridad

La autoridad final sobre ProposalStatus pertenece a:

```text
Proposal Aggregate Root
```

No pertenece a:

```text
Controller

Application Service

Repository

Database

Read Model

Projection

Message Broker

Assembly

Participation

Voting

Document

Notification

Audit

Integration
```

Estos componentes pueden colaborar con el proceso, pero no
reemplazan la decisión del Aggregate.

---

# Regla de No Mutación Externa

Ningún consumidor puede ejecutar:

```text
ProposalStatus = X
```

desde fuera del Aggregate.

Toda modificación debe expresarse mediante comportamiento de
Proposal.

---

# Regla de No Inferencia

No puede agregarse una transición porque resulte conveniente para
una implementación.

No puede inferirse:

```text
Rejected → Draft
```

para permitir correcciones.

No puede inferirse:

```text
Accepted → UnderReview
```

para reconsiderar una decisión.

No puede inferirse:

```text
Withdrawn → Submitted
```

para reutilizar una Proposal retirada.

No puede inferirse:

```text
Archived → Draft
```

para reactivar información histórica.

Toda nueva transición requiere evolución explícita del dominio.

---

# Evolución de la State Machine

La incorporación de un nuevo estado o transición debe evaluarse
contra, como mínimo:

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

No debe existir una transición documentada únicamente en código.

---

# Coherencia con Lifecycle

La State Machine debe permanecer completamente coherente con:

```text
DOMAIN-007A-Lifecycle.md
```

Lifecycle define el ciclo de vida conceptual.

State Machine formaliza las transiciones.

Debe mantenerse:

```text
Lifecycle

↓

State Machine
```

No:

```text
Implementation Convenience

↓

State Machine

↓

Lifecycle
```

---

# Coherencia con Commands

Toda transición debe poseer una intención explícita definida por un
Command.

La State Machine no recibe actualizaciones genéricas de estado.

No debe existir un Command como:

```text
SetProposalStatus
```

que permita seleccionar arbitrariamente el estado destino.

Los Commands deben expresar lenguaje de dominio:

```text
SubmitProposal

StartProposalReview

AcceptProposal

RejectProposal

WithdrawProposal

ArchiveProposal
```

---

# Coherencia con Domain Events

Toda transición confirmada debe producir el hecho correspondiente
cuando el modelo así lo establezca.

No debe existir:

```text
ProposalAccepted
```

si Proposal nunca alcanzó:

```text
Accepted
```

Tampoco debe existir:

```text
ProposalArchived
```

si Proposal no alcanzó:

```text
Archived
```

---

# Coherencia con Invariants

Una transición permitida por la matriz no puede ignorar las
invariantes.

Debe mantenerse:

```text
Transition Matrix
    +
Invariants
    +
Permissions
    +
Versioning
    =
Valid State Change
```

---

# Coherencia con Test Scenarios

Los escenarios definidos en:

```text
DOMAIN-007M-Test-Scenarios.md
```

deben cubrir como mínimo:

- estado inicial;
- todas las transiciones válidas;
- todas las categorías de transición inválida;
- terminalidad de Archived;
- retiro desde Draft;
- retiro desde Submitted;
- rechazo de retiro desde UnderReview;
- aceptación desde UnderReview;
- rechazo desde UnderReview;
- archivado desde estados permitidos;
- conflicto de Version;
- Permission insuficiente;
- invariante violada;
- ausencia de mutación parcial;
- ausencia de eventos de éxito ante rechazo.

---

# Restricciones

No está permitido:

- crear Proposal en un estado distinto de Draft;
- modificar ProposalStatus directamente;
- utilizar un setter público para ProposalStatus;
- utilizar un Command genérico SetProposalStatus;
- omitir Submitted;
- omitir UnderReview;
- aceptar una Proposal fuera de UnderReview;
- rechazar una Proposal fuera de UnderReview;
- retirar una Proposal desde UnderReview en la versión 1.0;
- retirar una Proposal desde Accepted;
- retirar una Proposal desde Rejected;
- retirar una Proposal desde Archived;
- archivar una Proposal desde Draft;
- archivar una Proposal desde Submitted;
- archivar una Proposal desde UnderReview;
- reactivar Accepted;
- reactivar Rejected;
- reactivar Withdrawn;
- reactivar Archived;
- permitir transiciones no declaradas;
- permitir que otro Aggregate modifique ProposalStatus;
- permitir que un Read Model modifique ProposalStatus;
- permitir que Integration modifique ProposalStatus directamente;
- permitir que Persistence decida transiciones;
- permitir que UI introduzca estados;
- utilizar estados técnicos como estados de dominio;
- ignorar Permissions;
- ignorar invariantes;
- ignorar Versioning;
- producir Domain Events de éxito para transiciones rechazadas;
- permitir mutaciones parciales.

---

# Principios Arquitectónicos

La State Machine preserva las siguientes separaciones:

```text
Command
    ≠
State Change
```

```text
Permission
    ≠
Transition Validity
```

```text
Guard
    ≠
State
```

```text
Invariant
    ≠
Permission
```

```text
Domain Event
    ≠
Command
```

```text
Voting Result
    ≠
Proposal State Mutation
```

```text
Read Model
    ≠
State Authority
```

```text
Integration Event
    ≠
State Authority
```

```text
Persistence
    ≠
State Machine
```

```text
Archived
    ≠
Deleted
```

```text
Withdrawn
    ≠
Rejected
```

```text
Accepted
    ≠
Executed
```

Estas separaciones protegen el significado del modelo.

---

# Compatibilidad Arquitectónica

La State Machine de Proposal es compatible con:

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

La compatibilidad no introduce dependencias tecnológicas dentro del
dominio.

---

# Independencia Tecnológica

La State Machine no depende de:

```text
PostgreSQL

MongoDB

MySQL

Redis

Kafka

RabbitMQ

HTTP

REST

GraphQL

OAuth

JWT

FastAPI

Django

React

Next.js

FIWARE
```

Ninguna de estas tecnologías define los estados o transiciones de
Proposal.

---

# Documentación Complementaria

La State Machine debe interpretarse conjuntamente con:

```text
DOMAIN-007-Aggregate.md

DOMAIN-007A-Lifecycle.md

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

Cada documento desarrolla una responsabilidad diferente sin
redefinir unilateralmente la State Machine.

---

# Regla de Coherencia Documental

Ningún documento complementario puede introducir una transición
que contradiga esta State Machine sin actualizar formalmente el
modelo oficial.

No puede existir una transición válida únicamente en:

- código;
- Application Services;
- Infrastructure;
- API;
- base de datos;
- documentación de Integration;
- Read Models;
- UI.

Toda transición del dominio debe existir explícitamente en la
documentación oficial.

---

# Definición de Éxito

La State Machine del Aggregate **Proposal** constituye la
representación normativa oficial de las transiciones de estado de
una iniciativa dentro de AURA Core.

Toda Proposal comienza en:

```text
Draft
```

y únicamente puede evolucionar mediante las transiciones
explícitamente definidas:

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

junto con los flujos de retiro permitidos:

```text
Draft
    ↓
Withdrawn
    ↓
Archived
```

y:

```text
Submitted
    ↓
Withdrawn
    ↓
Archived
```

No existen transiciones implícitas.

No existen retrocesos arbitrarios.

No existe reactivación de estados de resolución o estados
terminales en la versión 1.0.

Archived constituye el estado terminal.

Toda transición debe:

```text
validar el estado actual

↓

validar Permissions

↓

validar Guards

↓

preservar Invariants

↓

validar Version

↓

modificar ProposalStatus

↓

actualizar información de Lifecycle

↓

incrementar Version

↓

producir Domain Events
```

cuando corresponda.

Una transición rechazada mantiene íntegramente el estado anterior,
no incrementa Version y no produce el Domain Event de éxito.

Proposal mantiene autoridad exclusiva sobre ProposalStatus.

Assembly, Participation, Voting, Document, Notification, Audit,
Integration, Read Models, Persistence, Application Services e
Infrastructure no pueden modificar directamente la State Machine.

De esta forma,
**DOMAIN-007B-State-Machine.md** formaliza el comportamiento de
estado del Aggregate Proposal, preservando su ciclo de vida,
identidad, invariantes, consistencia, trazabilidad, concurrencia,
independencia tecnológica y los principios Domain-Driven Design
establecidos para AURA Core.