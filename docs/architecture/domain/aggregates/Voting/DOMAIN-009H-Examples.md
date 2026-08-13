# DOMAIN-009H — Voting Examples

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
- DOMAIN-009J-Consistency-Boundary.md
- DOMAIN-009K-Integration-Events.md
- DOMAIN-009L-Read-Model.md

---

# Objetivo

Proporcionar ejemplos conceptuales del comportamiento del Aggregate
**Voting** utilizando exclusivamente las reglas definidas por su
modelo de dominio.

Los ejemplos permiten observar conjuntamente:

- identidad;
- OrganizationId;
- contexto;
- Lifecycle;
- State Machine;
- Commands;
- Domain Events;
- Invariants;
- Permissions;
- Repository Contract;
- Versioning;
- Consistency Boundary.

Los ejemplos de este documento no agregan:

- nuevos estados;
- nuevas transiciones;
- nuevos Commands;
- nuevos Domain Events;
- nuevas Permissions;
- nuevas Invariants;
- nuevas responsabilidades.

Toda regla normativa permanece definida por los documentos
especializados del Aggregate.

---

# Principios

Los ejemplos deben interpretarse bajo los siguientes principios:

- Voting es la única Aggregate Root;
- VotingId es único e inmutable;
- OrganizationId es obligatorio e inmutable;
- los Aggregates externos se representan mediante identificadores;
- todo Voting comienza en Draft;
- VotingStatus solamente cambia mediante la State Machine;
- toda modificación válida preserva las Invariants;
- toda modificación válida incrementa Version;
- toda modificación relevante produce el Domain Event
  correspondiente;
- una operación rechazada no modifica estado ni Version;
- una operación rechazada no genera el Domain Event de éxito;
- Archived es terminal;
- Voting no modifica directamente otros Aggregates.

---

# Convenciones

Los ejemplos utilizan identificadores conceptuales como:

```text
VotingId = VOT-001

OrganizationId = ORG-001

AssemblyId = ASM-001

ProposalId = PRO-001
```

Estos valores tienen propósito exclusivamente ilustrativo.

Los tipos concretos de identificadores permanecen definidos por los
contratos correspondientes de AURA.

---

# Ejemplo 1 — Creación de Voting

Estado inicial:

```text
No Voting
```

Intención:

```text
CreateVoting
```

Datos conceptuales:

```text
VotingId = VOT-001

OrganizationId = ORG-001

VotingType = ValidVotingType

Title = ValidTitle

Rules = ValidRules
```

Debe cumplirse:

```text
VotingId valid

OrganizationId valid

VotingType valid

Title valid

Rules valid

Creation Invariants valid
```

Resultado:

```text
VotingId = VOT-001

OrganizationId = ORG-001

VotingStatus = Draft

Version = 1
```

Domain Event:

```text
VotingCreated
```

Flujo:

```text
No Voting

↓

CreateVoting

↓

Validate Creation Invariants

↓

VotingStatus = Draft

Version = 1

↓

VotingCreated
```

---

# Ejemplo 2 — Creación con Assembly

Un Voting puede crearse dentro del contexto de una Assembly cuando
dicho contexto corresponda al proceso.

Datos conceptuales:

```text
VotingId = VOT-002

OrganizationId = ORG-001

AssemblyId = ASM-001

VotingType = ValidVotingType

Title = ValidTitle

Rules = ValidRules
```

La relación debe interpretarse como:

```text
Voting

↓

AssemblyId
```

No como:

```text
Voting

↓

Assembly Aggregate
```

Resultado conceptual:

```text
VotingId = VOT-002

OrganizationId = ORG-001

AssemblyId = ASM-001

VotingStatus = Draft
```

Voting no modifica Assembly durante su creación.

---

# Ejemplo 3 — Creación relacionada con Proposal

Cuando una Proposal constituye la materia relacionada con el
proceso de Voting puede utilizarse:

```text
ProposalId
```

Ejemplo:

```text
VotingId = VOT-003

OrganizationId = ORG-001

ProposalId = PRO-001
```

La relación significa:

```text
Voting

references

ProposalId = PRO-001
```

No significa:

```text
Voting

owns

Proposal
```

Proposal conserva:

- identidad;
- Lifecycle;
- State Machine;
- Invariants;
- Version;
- Repository.

---

# Ejemplo 4 — Creación con Assembly y Proposal

Un Voting puede mantener simultáneamente referencias contextuales
cuando las reglas del dominio así lo permitan.

Ejemplo:

```text
VotingId = VOT-004

OrganizationId = ORG-001

AssemblyId = ASM-001

ProposalId = PRO-001
```

Conceptualmente:

```text
Assembly
    │
    │ AssemblyId
    ▼
 Voting
    ▲
    │ ProposalId
    │
Proposal
```

Voting continúa siendo un Consistency Boundary independiente.

---

# Ejemplo 5 — Apertura Válida

Estado inicial:

```text
VotingStatus = Draft

Version = 1
```

Permission:

```text
Voting.Open
```

Command:

```text
OpenVoting
```

Debe cumplirse:

```text
VotingStatus = Draft

Valid VotingType

Valid Rules

Valid Options when applicable

Opening Invariants satisfied
```

Resultado:

```text
VotingStatus = Open

OpenedAt = T1

Version = 2
```

Domain Event:

```text
VotingOpened
```

Flujo:

```text
Draft

↓

Voting.Open

↓

OpenVoting

↓

Validate State

Validate Rules

Validate Invariants

↓

Open

Version + 1

↓

VotingOpened
```

---

# Ejemplo 6 — Apertura Rechazada desde Open

Estado:

```text
VotingStatus = Open
```

Command:

```text
OpenVoting
```

La State Machine no define:

```text
Open → Open
```

como transición de Lifecycle.

Resultado:

```text
Rejected
```

Debe conservarse:

```text
VotingStatus = Open

Version = Previous Version
```

No se produce:

```text
VotingOpened
```

---

# Ejemplo 7 — Apertura Rechazada desde Closed

Estado:

```text
VotingStatus = Closed
```

Permission:

```text
Voting.Open = Granted
```

Command:

```text
OpenVoting
```

La Permission no modifica la State Machine.

No existe:

```text
Closed → Open
```

Resultado:

```text
Rejected
```

Debe mantenerse:

```text
VotingStatus = Closed

Version = Previous Version
```

No se produce:

```text
VotingOpened
```

---

# Ejemplo 8 — Permission Concedida con Invariant Inválida

Permission:

```text
Voting.Open = Granted
```

Estado:

```text
VotingStatus = Draft
```

Pero las condiciones requeridas para abrir el Voting no son
válidas.

Debe mantenerse:

```text
Permission Granted

+

Invalid Opening Invariant

=

Rejected
```

No se produce:

```text
Draft → Open
```

No se produce:

```text
VotingOpened
```

Version permanece sin cambios.

---

# Ejemplo 9 — Permission Denegada

Estado:

```text
VotingStatus = Draft
```

Permission:

```text
Voting.Open = Denied
```

Intención:

```text
OpenVoting
```

Resultado:

```text
Authorization Denied
```

El Aggregate permanece:

```text
VotingStatus = Draft

Version = Previous Version
```

No se produce:

```text
VotingOpened
```

---

# Ejemplo 10 — Cierre Válido

Estado inicial:

```text
VotingStatus = Open

OpenedAt = T1

Version = 2
```

Permission:

```text
Voting.Close
```

Command:

```text
CloseVoting
```

Debe cumplirse:

```text
VotingStatus = Open

Valid Rules

Valid Closing Conditions

Valid Result when applicable

Closing Invariants satisfied
```

Resultado:

```text
VotingStatus = Closed

OpenedAt = T1

ClosedAt = T2

Version = 3
```

Debe mantenerse:

```text
T2 >= T1
```

Domain Event:

```text
VotingClosed
```

---

# Ejemplo 11 — Cierre Rechazado desde Draft

Estado:

```text
VotingStatus = Draft
```

Command:

```text
CloseVoting
```

La State Machine no permite:

```text
Draft → Closed
```

Resultado:

```text
Rejected
```

Debe conservarse:

```text
VotingStatus = Draft

Version = Previous Version
```

No se produce:

```text
VotingClosed
```

---

# Ejemplo 12 — Cierre Rechazado desde Closed

Estado:

```text
VotingStatus = Closed
```

Command:

```text
CloseVoting
```

No existe una transición:

```text
Closed → Closed
```

Resultado:

```text
Rejected
```

No se genera un nuevo:

```text
VotingClosed
```

Version permanece sin cambios.

---

# Ejemplo 13 — Cancelación Válida

Estado inicial:

```text
VotingStatus = Draft

Version = 1
```

Permission:

```text
Voting.Cancel
```

Command:

```text
CancelVoting
```

Resultado:

```text
VotingStatus = Cancelled

CancelledAt = T1

Version = 2
```

Domain Event:

```text
VotingCancelled
```

Flujo:

```text
Draft

↓

CancelVoting

↓

Validate State

Validate Invariants

↓

Cancelled

Version + 1

↓

VotingCancelled
```

---

# Ejemplo 14 — Cancelación Rechazada desde Open

Estado:

```text
VotingStatus = Open
```

Command:

```text
CancelVoting
```

La versión 1.0 no define:

```text
Open → Cancelled
```

Resultado:

```text
Rejected
```

Debe mantenerse:

```text
VotingStatus = Open

Version = Previous Version
```

No se produce:

```text
VotingCancelled
```

---

# Ejemplo 15 — Cancelación Rechazada desde Closed

Estado:

```text
VotingStatus = Closed
```

Command:

```text
CancelVoting
```

No existe:

```text
Closed → Cancelled
```

Resultado:

```text
Rejected
```

No se modifica el Aggregate.

---

# Ejemplo 16 — Archivado desde Closed

Estado inicial:

```text
VotingStatus = Closed

Version = 3
```

Permission:

```text
Voting.Archive
```

Command:

```text
ArchiveVoting
```

Resultado:

```text
VotingStatus = Archived

ArchivedAt = T3

Version = 4
```

Domain Event:

```text
VotingArchived
```

Flujo:

```text
Closed

↓

ArchiveVoting

↓

Archived
```

---

# Ejemplo 17 — Archivado desde Cancelled

Estado inicial:

```text
VotingStatus = Cancelled

Version = 2
```

Command:

```text
ArchiveVoting
```

Resultado:

```text
VotingStatus = Archived

ArchivedAt = T2

Version = 3
```

Domain Event:

```text
VotingArchived
```

---

# Ejemplo 18 — Archivado Rechazado desde Draft

Estado:

```text
VotingStatus = Draft
```

Command:

```text
ArchiveVoting
```

La State Machine no define:

```text
Draft → Archived
```

Resultado:

```text
Rejected
```

No se produce:

```text
VotingArchived
```

---

# Ejemplo 19 — Archivado Rechazado desde Open

Estado:

```text
VotingStatus = Open
```

Command:

```text
ArchiveVoting
```

La transición:

```text
Open → Archived
```

no pertenece a la State Machine versión 1.0.

Resultado:

```text
Rejected
```

---

# Ejemplo 20 — Modificación de VotingType

Estado conceptual:

```text
VotingStatus = Draft

VotingType = VotingTypeA

Version = 2
```

Permission:

```text
Voting.ChangeType
```

Command:

```text
ChangeVotingType(
    NewVotingType = VotingTypeB
)
```

Cuando la operación cumple todas las reglas aplicables:

```text
VotingTypeA

↓

VotingTypeB
```

Debe mantenerse:

```text
VotingStatus = Draft
```

Version:

```text
2 → 3
```

Domain Event:

```text
VotingTypeChanged
```

El evento puede representar conceptualmente:

```text
PreviousVotingType = VotingTypeA

NewVotingType = VotingTypeB
```

---

# Ejemplo 21 — VotingType Inválido

Command:

```text
ChangeVotingType(
    NewVotingType = InvalidVotingType
)
```

Si el nuevo valor no satisface las reglas del dominio:

```text
Rejected
```

Debe conservarse:

```text
VotingType = PreviousVotingType

VotingStatus = PreviousVotingStatus

Version = PreviousVersion
```

No se produce:

```text
VotingTypeChanged
```

---

# Ejemplo 22 — Cambio de Title

Estado:

```text
VotingStatus = Draft

Title = Title A

Version = 2
```

Permission:

```text
Voting.ChangeTitle
```

Command:

```text
ChangeVotingTitle(
    NewTitle = Title B
)
```

Resultado:

```text
Title = Title B

VotingStatus = Draft

Version = 3
```

Domain Event:

```text
VotingTitleChanged
```

Conceptualmente:

```text
PreviousTitle = Title A

NewTitle = Title B
```

VotingId permanece inmutable.

OrganizationId permanece inmutable.

---

# Ejemplo 23 — Cambio de Description

Estado:

```text
Description = Description A

Version = N
```

Command:

```text
ChangeVotingDescription(
    NewDescription = Description B
)
```

Cuando la operación es válida:

```text
Description = Description B

Version = N + 1
```

Domain Event:

```text
VotingDescriptionChanged
```

VotingStatus permanece sin transición de Lifecycle.

---

# Ejemplo 24 — Cambio de Rules

Estado conceptual:

```text
VotingStatus = Draft

Rules = Rules A

Version = N
```

Permission:

```text
Voting.ChangeRules
```

Command:

```text
ChangeVotingRules(
    NewRules = Rules B
)
```

Antes de confirmar debe mantenerse:

```text
Valid Rules B

+

Compatible VotingType

+

Compatible Options when applicable

+

Valid Invariants
```

Resultado:

```text
Rules = Rules B

VotingStatus = Draft

Version = N + 1
```

Domain Event:

```text
VotingRulesChanged
```

---

# Ejemplo 25 — Cambio de Rules Rechazado

Estado:

```text
Rules = Rules A

Version = N
```

Command:

```text
ChangeVotingRules(
    NewRules = InvalidRules
)
```

Resultado:

```text
Rejected
```

Debe mantenerse:

```text
Rules = Rules A

Version = N
```

No se produce:

```text
VotingRulesChanged
```

---

# Ejemplo 26 — Agregar VotingOption

Estado conceptual:

```text
VotingStatus = Draft

Options = [
    OptionA,
    OptionB
]

Version = N
```

Permission:

```text
Voting.AddOption
```

Command:

```text
AddVotingOption(
    VotingOption = OptionC
)
```

Cuando OptionC es válida y compatible con VotingType y Rules:

```text
Options = [
    OptionA,
    OptionB,
    OptionC
]
```

VotingStatus permanece:

```text
Draft
```

Version:

```text
N + 1
```

Domain Event:

```text
VotingOptionAdded
```

---

# Ejemplo 27 — Agregar VotingOption Inválida

Estado:

```text
Options = CurrentOptions

Version = N
```

Command:

```text
AddVotingOption(
    VotingOption = InvalidOption
)
```

Si la Option viola VotingType, Rules o Invariants:

```text
Rejected
```

Debe mantenerse:

```text
Options = CurrentOptions

Version = N
```

No se produce:

```text
VotingOptionAdded
```

---

# Ejemplo 28 — Eliminar VotingOption

Estado conceptual:

```text
Options = [
    OptionA,
    OptionB,
    OptionC
]

Version = N
```

Permission:

```text
Voting.RemoveOption
```

Command:

```text
RemoveVotingOption(
    VotingOption = OptionC
)
```

Cuando el conjunto resultante continúa siendo válido:

```text
Options = [
    OptionA,
    OptionB
]
```

Version:

```text
N + 1
```

Domain Event:

```text
VotingOptionRemoved
```

---

# Ejemplo 29 — Eliminación de Option que Rompe Invariants

Estado:

```text
Options = CurrentOptions

Version = N
```

Command:

```text
RemoveVotingOption(
    VotingOption = ExistingOption
)
```

Si la eliminación produciría:

```text
Invalid Options
```

según VotingType o Rules:

```text
Rejected
```

Debe preservarse:

```text
Options = CurrentOptions

Version = N
```

No se produce:

```text
VotingOptionRemoved
```

---

# Ejemplo 30 — Modificación sin Cambio de Lifecycle

Estado:

```text
VotingStatus = Draft

Title = Title A

Version = 3
```

Command:

```text
ChangeVotingTitle(
    NewTitle = Title B
)
```

Resultado:

```text
VotingStatus = Draft

Title = Title B

Version = 4
```

Debe observarse:

```text
Draft

↓

Domain Modification

↓

Draft
```

Una modificación válida puede incrementar Version sin producir una
transición de Lifecycle.

---

# Ejemplo 31 — Flujo Normal Completo

Creación:

```text
No Voting

↓

CreateVoting

↓

Draft
Version = 1

↓

VotingCreated
```

Apertura:

```text
Draft

↓

OpenVoting

↓

Open
Version = 2

↓

VotingOpened
```

Cierre:

```text
Open

↓

CloseVoting

↓

Closed
Version = 3

↓

VotingClosed
```

Archivado:

```text
Closed

↓

ArchiveVoting

↓

Archived
Version = 4

↓

VotingArchived
```

Lifecycle resultante:

```text
Draft

↓

Open

↓

Closed

↓

Archived
```

---

# Ejemplo 32 — Flujo Cancelado Completo

Creación:

```text
No Voting

↓

CreateVoting

↓

Draft
Version = 1

↓

VotingCreated
```

Cancelación:

```text
Draft

↓

CancelVoting

↓

Cancelled
Version = 2

↓

VotingCancelled
```

Archivado:

```text
Cancelled

↓

ArchiveVoting

↓

Archived
Version = 3

↓

VotingArchived
```

Lifecycle resultante:

```text
Draft

↓

Cancelled

↓

Archived
```

---

# Ejemplo 33 — Preservación Temporal del Flujo Normal

Supóngase:

```text
CreatedAt = T1
```

Después de abrir:

```text
OpenedAt = T2
```

Después de cerrar:

```text
ClosedAt = T3
```

Después de archivar:

```text
ArchivedAt = T4
```

Debe mantenerse:

```text
T1 <= T2 <= T3 <= T4
```

El archivado conserva:

```text
CreatedAt = T1

OpenedAt = T2

ClosedAt = T3

ArchivedAt = T4
```

Los timestamps anteriores no se reescriben.

---

# Ejemplo 34 — Preservación Temporal del Flujo Cancelado

Creación:

```text
CreatedAt = T1
```

Cancelación:

```text
CancelledAt = T2
```

Archivado:

```text
ArchivedAt = T3
```

Debe mantenerse:

```text
T1 <= T2 <= T3
```

---

# Ejemplo 35 — Reapertura Rechazada

Estado:

```text
VotingStatus = Closed
```

Command:

```text
OpenVoting
```

La versión 1.0 no define:

```text
Closed → Open
```

Resultado:

```text
Rejected
```

No existe:

```text
VotingOpened
```

Version permanece sin cambios.

---

# Ejemplo 36 — Reactivación Rechazada

Estado:

```text
VotingStatus = Cancelled
```

Una intención equivalente a volver a:

```text
Draft
```

o:

```text
Open
```

no forma parte del modelo versión 1.0.

No existe un Command oficial de reactivación.

El Aggregate permanece:

```text
Cancelled
```

---

# Ejemplo 37 — Desarchivado Rechazado

Estado:

```text
VotingStatus = Archived
```

Archived es terminal.

No existe:

```text
Archived → Previous State
```

No existe un Command oficial de desarchivado.

El Aggregate permanece:

```text
Archived
```

---

# Ejemplo 38 — Modificación Ordinaria sobre Archived

Estado:

```text
VotingStatus = Archived
```

Command:

```text
ChangeVotingTitle
```

Aunque el actor posea:

```text
Voting.ChangeTitle
```

debe mantenerse:

```text
Permission Granted

+

Archived

=

Rejected
```

No se modifica:

```text
Title

VotingStatus

Version
```

No se produce:

```text
VotingTitleChanged
```

---

# Ejemplo 39 — Result no es VotingStatus

Supóngase un Voting cerrado con un Result válido.

Debe mantenerse conceptualmente:

```text
VotingStatus = Closed

Result = ValidResult
```

No debe transformarse VotingStatus en un estado derivado del
resultado.

Debe mantenerse:

```text
Result

≠

VotingStatus
```

Los estados oficiales continúan siendo:

```text
Draft

Open

Closed

Cancelled

Archived
```

---

# Ejemplo 40 — Result no se Establece Directamente

No forma parte del modelo oficial:

```text
SetVotingResult
```

Result permanece protegido por el comportamiento definido del
Aggregate.

Conceptualmente:

```text
CloseVoting

↓

Validate Closing Conditions

Validate Result when applicable

↓

Closed

↓

VotingClosed
```

No:

```text
External Actor

↓

Direct Result Mutation
```

---

# Ejemplo 41 — Voting no Modifica Proposal

Contexto:

```text
VotingId = VOT-001

ProposalId = PRO-001
```

Voting alcanza:

```text
Closed
```

y produce:

```text
VotingClosed
```

Debe mantenerse:

```text
VotingClosed

≠

Direct Proposal State Mutation
```

Proposal conserva la autoridad sobre su propio estado.

---

# Ejemplo 42 — Voting no Modifica Assembly

Contexto:

```text
VotingId = VOT-001

AssemblyId = ASM-001
```

Voting ejecuta:

```text
OpenVoting
```

y alcanza:

```text
Open
```

Esto no implica:

```text
Assembly State Change
```

Debe mantenerse:

```text
Voting State Machine

≠

Assembly State Machine
```

---

# Ejemplo 43 — Voting y Participation

Voting representa:

```text
Formal Voting Process
```

Participation representa:

```text
Individual Participation
```

Por ejemplo:

```text
VotingId = VOT-001
```

puede ser utilizado como contexto por procesos de Participation.

Esto no significa:

```text
Voting
    │
    └── Participation Aggregate
```

Debe mantenerse:

```text
Voting

≠

Participation
```

Cada Aggregate conserva:

- identidad;
- Lifecycle;
- State Machine;
- Invariants;
- Version;
- Repository;
- Consistency Boundary.

---

# Ejemplo 44 — Domain Event de Creación

Después de una creación válida puede producirse conceptualmente:

```text
VotingCreated

EventId = EVT-001

EventType = VotingCreated

VotingId = VOT-001

OrganizationId = ORG-001

AggregateVersion = 1

OccurredAt = T1

CorrelationId = COR-001

CausationId = CMD-001
```

El evento representa un hecho ocurrido.

No constituye una solicitud de creación.

---

# Ejemplo 45 — Domain Event de Apertura

Una apertura válida puede producir conceptualmente:

```text
VotingOpened

EventId = EVT-002

EventType = VotingOpened

VotingId = VOT-001

OrganizationId = ORG-001

PreviousStatus = Draft

OpenedAt = T2

AggregateVersion = 2

OccurredAt = T2

CorrelationId = COR-001

CausationId = CMD-002
```

El Event representa:

```text
Voting was opened
```

No:

```text
Please open Voting
```

---

# Ejemplo 46 — Domain Event de Cierre

Un cierre válido puede producir:

```text
VotingClosed

EventId = EVT-003

VotingId = VOT-001

OrganizationId = ORG-001

PreviousStatus = Open

OpenedAt = T2

ClosedAt = T3

AggregateVersion = 3
```

Cuando corresponda puede preservar el Result necesario para
representar formalmente el hecho.

---

# Ejemplo 47 — Evento no Generado ante Rechazo

Estado:

```text
VotingStatus = Draft

Version = 1
```

Command:

```text
CloseVoting
```

Resultado:

```text
Rejected
```

Debe mantenerse:

```text
Version = 1
```

No se produce:

```text
VotingClosed
```

Debe mantenerse:

```text
Rejected Command

↓

No Success Domain Event
```

---

# Ejemplo 48 — Versioning

Estado inicial:

```text
VotingStatus = Draft

Version = 1
```

Cambio válido:

```text
ChangeVotingTitle
```

Resultado:

```text
Version = 2
```

Posteriormente:

```text
OpenVoting
```

Resultado:

```text
Version = 3
```

Secuencia conceptual:

```text
VotingCreated
AggregateVersion = 1

VotingTitleChanged
AggregateVersion = 2

VotingOpened
AggregateVersion = 3
```

AggregateVersion representa el orden lógico de evolución del mismo
Voting.

---

# Ejemplo 49 — Lectura no Incrementa Version

Estado persistido:

```text
VotingId = VOT-001

Version = 5
```

Repository:

```text
getById(VOT-001)
```

Resultado:

```text
VotingId = VOT-001

Version = 5
```

Debe mantenerse:

```text
Read

↓

No Version Increment
```

---

# Ejemplo 50 — exists() no Modifica Voting

Operación:

```text
exists(VOT-001)
```

Resultado conceptual:

```text
true
```

o:

```text
false
```

La operación no modifica:

```text
VotingStatus

Version

Lifecycle Timestamps
```

---

# Ejemplo 51 — Persistencia Válida

Estado recuperado:

```text
VotingId = VOT-001

Version = 4
```

Se ejecuta un Command válido.

Resultado en memoria del dominio:

```text
Version = 5
```

Persistencia:

```text
save(Voting)
```

con:

```text
ExpectedVersion = 4
```

Si:

```text
PersistedVersion = 4
```

la escritura puede confirmarse como:

```text
PersistedVersion = 5
```

---

# Ejemplo 52 — Conflicto de Concurrencia

Estado persistido inicial:

```text
VotingId = VOT-001

Version = 7
```

Dos operaciones recuperan:

```text
Version = 7
```

Operation A modifica válidamente Voting y persiste:

```text
Version = 8
```

Operation B intenta persistir utilizando:

```text
ExpectedVersion = 7
```

pero el Repository encuentra:

```text
PersistedVersion = 8
```

Debe producirse:

```text
ConcurrencyConflict
```

La modificación B no puede sobrescribir silenciosamente la
modificación A.

---

# Ejemplo 53 — No Last Write Wins

Estado persistido:

```text
Version = 8
```

Una operación intenta guardar una modificación calculada desde:

```text
ExpectedVersion = 7
```

No debe ocurrir:

```text
Overwrite Version 8
```

Debe ocurrir:

```text
ConcurrencyConflict
```

El estado confirmado previamente permanece protegido.

---

# Ejemplo 54 — Rehidratación

Estado persistido:

```text
VotingId = VOT-001

OrganizationId = ORG-001

VotingStatus = Closed

OpenedAt = T1

ClosedAt = T2

Version = 6
```

getById() debe reconstruir conceptualmente:

```text
VotingId = VOT-001

OrganizationId = ORG-001

VotingStatus = Closed

OpenedAt = T1

ClosedAt = T2

Version = 6
```

La rehidratación no produce:

```text
VotingCreated

VotingOpened

VotingClosed
```

como nuevos Domain Events.

Tampoco incrementa Version.

---

# Ejemplo 55 — Identidad Duplicada

Supóngase:

```text
exists(VOT-001) = true
```

Se intenta crear otro Voting con:

```text
VotingId = VOT-001
```

Debe mantenerse:

```text
Existing VotingId

+

New Voting with Same VotingId

=

Rejected
```

VotingId no puede reutilizarse.

---

# Ejemplo 56 — OrganizationId Inmutable

Estado:

```text
VotingId = VOT-001

OrganizationId = ORG-001
```

No existe un Command oficial para transformar:

```text
OrganizationId = ORG-001
```

en:

```text
OrganizationId = ORG-002
```

Debe mantenerse durante toda la vida del Aggregate:

```text
OrganizationId = ORG-001
```

---

# Ejemplo 57 — Modificación Directa de Estado Prohibida

No debe utilizarse:

```text
VotingStatus = Closed
```

como operación directa.

Debe utilizarse el comportamiento del dominio:

```text
CloseVoting

↓

Voting

↓

Validate State

Validate Invariants

↓

Open → Closed
```

cuando la transición sea válida.

---

# Ejemplo 58 — Modificación Directa de Version Prohibida

No debe utilizarse:

```text
Version = Version + 1
```

como una operación independiente del dominio.

Version cambia como consecuencia de:

```text
Valid Domain Modification

↓

Version + 1
```

---

# Ejemplo 59 — Permission no Sustituye State Machine

Actor autorizado:

```text
Voting.Archive = Granted
```

Voting:

```text
VotingStatus = Open
```

Command:

```text
ArchiveVoting
```

Resultado:

```text
Rejected
```

porque no existe:

```text
Open → Archived
```

Debe mantenerse:

```text
Permission Granted

≠

State Transition Guaranteed
```

---

# Ejemplo 60 — Permission no Sustituye Invariants

Actor autorizado:

```text
Voting.ChangeRules = Granted
```

Command:

```text
ChangeVotingRules(
    NewRules = InvalidRules
)
```

Resultado:

```text
Rejected
```

Debe mantenerse:

```text
Permission Granted

+

Invariant Violation

=

Rejected
```

---

# Ejemplo 61 — Voting.Read

Permission:

```text
Voting.Read
```

permite realizar una consulta autorizada según el modelo de
autorización correspondiente.

Debe mantenerse:

```text
Voting.Read

↓

Read
```

No:

```text
Voting.Read

↓

Change Voting
```

La lectura no modifica:

```text
VotingStatus

Version

Rules

Options

Result
```

---

# Ejemplo 62 — Voting Permission no Modifica Assembly

Un actor posee:

```text
Voting.Open
```

Eso no significa que posea una capacidad sobre:

```text
Assembly
```

Debe mantenerse:

```text
Voting.Open

≠

Assembly Permission
```

La autorización permanece limitada a la capacidad correspondiente
sobre Voting.

---

# Ejemplo 63 — Voting Permission no Modifica Proposal

Un actor posee:

```text
Voting.Close
```

y ejecuta válidamente:

```text
CloseVoting
```

Voting produce:

```text
VotingClosed
```

Esto no concede autoridad para ejecutar una modificación directa
sobre Proposal.

---

# Ejemplo 64 — Voting Permission no Modifica Participation

Una Permission:

```text
Voting.ChangeRules
```

no constituye:

```text
Participation Permission
```

Los modelos permanecen separados.

---

# Ejemplo 65 — Read Model no Modifica Voting

Una proyección puede representar:

```text
VotingId

VotingStatus

Version
```

pero no puede ejecutar:

```text
VotingStatus = Open
```

sobre el Aggregate.

Debe mantenerse:

```text
Read Model

↓

Read
```

y:

```text
Command

↓

Voting Aggregate

↓

Write
```

---

# Ejemplo 66 — Flujo Command / Event

Ejemplo de apertura:

```text
Voting.Open
    │
    ▼
OpenVoting
    │
    ▼
Voting
    │
    ├── Validate VotingStatus
    ├── Validate Rules
    ├── Validate Invariants
    └── Apply Transition
             │
             ▼
       VotingOpened
```

La Permission representa capacidad.

El Command representa intención.

Voting determina la validez.

El Event representa el hecho consumado.

---

# Ejemplo 67 — Flujo de Persistencia

Conceptualmente:

```text
getById(VotingId)

↓

Voting
Version = N

↓

Authorized Command

↓

Validate Domain Rules

↓

Valid Modification

↓

Version = N + 1

↓

Domain Event

↓

save(Voting)
ExpectedVersion = N
```

El Repository no ejecuta el comportamiento de dominio.

---

# Ejemplo 68 — Consistency Boundary

Durante:

```text
CloseVoting
```

el límite de modificación es:

```text
Voting
```

Puede modificarse coherentemente dentro de Voting:

```text
VotingStatus

ClosedAt

Result when applicable

Version
```

No forman parte de la misma modificación interna:

```text
ProposalStatus

AssemblyStatus

ParticipationStatus

Organization State
```

Debe mantenerse:

```text
One Voting

=

One Consistency Boundary
```

---

# Ejemplo 69 — Referencia no es Ownership

Voting contiene:

```text
ProposalId = PRO-001
```

Esto representa:

```text
Reference
```

No:

```text
Ownership
```

VotingRepository puede persistir:

```text
ProposalId
```

pero no debe convertir:

```text
Proposal Aggregate
```

en parte interna de Voting.

---

# Ejemplo 70 — Flujo Histórico

Una secuencia conceptual válida puede ser:

```text
VotingCreated
AggregateVersion = 1

VotingTitleChanged
AggregateVersion = 2

VotingRulesChanged
AggregateVersion = 3

VotingOpened
AggregateVersion = 4

VotingClosed
AggregateVersion = 5

VotingArchived
AggregateVersion = 6
```

Cada evento representa un hecho diferente.

Los hechos anteriores permanecen verdaderos después de eventos
posteriores.

---

# Ejemplo 71 — Flujo Histórico Cancelado

Una secuencia conceptual válida puede ser:

```text
VotingCreated
AggregateVersion = 1

VotingTitleChanged
AggregateVersion = 2

VotingCancelled
AggregateVersion = 3

VotingArchived
AggregateVersion = 4
```

No existe en esta secuencia:

```text
VotingOpened
```

ni:

```text
VotingClosed
```

porque el Lifecycle siguió la ruta de cancelación.

---

# Ejemplo 72 — Evento Inmutable

Supóngase:

```text
VotingTitleChanged

PreviousTitle = Title A

NewTitle = Title B

AggregateVersion = 2
```

Posteriormente ocurre otro cambio:

```text
VotingTitleChanged

PreviousTitle = Title B

NewTitle = Title C

AggregateVersion = 3
```

El primer evento no se modifica.

Debe mantenerse:

```text
Event Version 2

≠

Event Version 3
```

Ambos representan hechos históricos diferentes.

---

# Ejemplo 73 — EventId Único

Dos cambios diferentes pueden producir:

```text
EventId = EVT-001
```

y:

```text
EventId = EVT-002
```

aunque ambos sean:

```text
VotingTitleChanged
```

Debe mantenerse:

```text
One Domain Fact

↓

One EventId
```

El mismo EventId no representa dos hechos diferentes.

---

# Ejemplo 74 — Archived como Registro Histórico

Estado:

```text
VotingStatus = Archived
```

Voting continúa conservando:

```text
VotingId

OrganizationId

Context

VotingType

Rules

Options

Result when applicable

Lifecycle Timestamps

Version
```

Archived significa:

```text
Historical Preservation
```

No:

```text
Physical Deletion
```

---

# Ejemplo 75 — Operación Rechazada Mantiene Estado Completo

Estado antes:

```text
VotingId = VOT-001

OrganizationId = ORG-001

VotingStatus = Closed

Version = 5
```

Command inválido:

```text
OpenVoting
```

Estado después:

```text
VotingId = VOT-001

OrganizationId = ORG-001

VotingStatus = Closed

Version = 5
```

No existe:

```text
VotingOpened
```

Debe mantenerse:

```text
Rejected Operation

=

No Domain Mutation
```

---

# Ejemplo 76 — Separación entre Intent, State y Fact

Debe interpretarse:

```text
OpenVoting
```

como:

```text
Intent
```

La transición:

```text
Draft → Open
```

como:

```text
State Change
```

y:

```text
VotingOpened
```

como:

```text
Fact
```

Los tres conceptos están relacionados, pero no son equivalentes.

---

# Ejemplo 77 — Separación entre Voting y Result

Voting es:

```text
Formal Voting Process
```

Result representa:

```text
Formal Result of Voting when applicable
```

Debe mantenerse:

```text
Voting

≠

Result
```

Result pertenece al estado del Voting cuando corresponde, pero no
reemplaza al Aggregate.

---

# Ejemplo 78 — Separación entre Voting y Options

VotingOption pertenece conceptualmente a Voting cuando forma parte
de la configuración del proceso.

Sin embargo:

```text
VotingOption
```

no posee por ello:

```text
Independent Aggregate Root

Independent Repository

Independent Version

Independent Lifecycle
```

Las modificaciones se realizan mediante:

```text
AddVotingOption

RemoveVotingOption
```

sobre Voting.

---

# Ejemplo 79 — Separación entre Authentication y Permission

Un actor puede encontrarse identificado.

Esto no implica automáticamente:

```text
Voting.Open = Granted
```

Debe mantenerse:

```text
Authentication

≠

Authorization
```

y:

```text
Authorization

≠

Domain Validation
```

---

# Ejemplo 80 — Cadena Conceptual Completa

Un flujo válido de modificación puede expresarse como:

```text
Actor

↓

Permission

↓

Command

↓

Voting Aggregate

↓

Validate VotingStatus

↓

Validate State Machine

↓

Validate Invariants

↓

Apply Domain Behavior

↓

Increment Version

↓

Produce Domain Event

↓

Persist Aggregate
```

Cada elemento mantiene una responsabilidad diferente.

---

# Escenarios Inválidos Consolidados

Los siguientes escenarios deben ser rechazados:

```text
Create Voting directly in Open

Create Voting directly in Closed

Create Voting directly in Cancelled

Create Voting directly in Archived

Draft → Closed

Draft → Archived

Open → Draft

Open → Cancelled

Open → Archived

Closed → Draft

Closed → Open

Closed → Cancelled

Cancelled → Draft

Cancelled → Open

Cancelled → Closed

Archived → Any State
```

También deben rechazarse modificaciones que intenten:

```text
Change VotingId

Change OrganizationId

Set VotingStatus Directly

Set Version Directly

Set Result Directly Outside Defined Behavior

Bypass Invariants

Bypass State Machine

Bypass Permissions

Modify External Aggregates Directly
```

---

# Matriz de Ejemplos de Lifecycle

| Escenario | Estado origen | Command | Estado resultado | Resultado |
| --- | --- | --- | --- | --- |
| Creación | No existe | CreateVoting | Draft | Accepted |
| Apertura | Draft | OpenVoting | Open | Accepted |
| Cierre | Open | CloseVoting | Closed | Accepted |
| Cancelación | Draft | CancelVoting | Cancelled | Accepted |
| Archivado normal | Closed | ArchiveVoting | Archived | Accepted |
| Archivado cancelado | Cancelled | ArchiveVoting | Archived | Accepted |
| Cierre desde Draft | Draft | CloseVoting | Draft | Rejected |
| Cancelación desde Open | Open | CancelVoting | Open | Rejected |
| Reapertura | Closed | OpenVoting | Closed | Rejected |
| Archivado desde Open | Open | ArchiveVoting | Open | Rejected |

---

# Matriz de Ejemplos de Configuración

| Command | Modificación | Cambio de VotingStatus | Domain Event |
| --- | --- | --- | --- |
| ChangeVotingType | VotingType | No | VotingTypeChanged |
| ChangeVotingTitle | Title | No | VotingTitleChanged |
| ChangeVotingDescription | Description | No | VotingDescriptionChanged |
| ChangeVotingRules | Rules | No | VotingRulesChanged |
| AddVotingOption | Options | No | VotingOptionAdded |
| RemoveVotingOption | Options | No | VotingOptionRemoved |

Cada operación continúa sujeta a estado, Permissions e Invariants.

---

# Matriz de Ejemplos de Versioning

| Operación | Resultado | Version |
| --- | --- | --- |
| CreateVoting válido | Accepted | Inicial |
| Command de modificación válido | Accepted | +1 |
| Transición válida | Accepted | +1 |
| Read | No modifica | Igual |
| exists() | No modifica | Igual |
| Command rechazado | Rejected | Igual |
| Permission denegada | Denied | Igual |
| ConcurrencyConflict | Rejected | Persisted Version permanece |

---

# Matriz Permission / Resultado

| Permission | Condición de dominio | Resultado |
| --- | --- | --- |
| Granted | Domain valid | Puede aceptarse |
| Granted | Domain invalid | Rejected |
| Denied | Domain valid o invalid | Denied |

Debe mantenerse:

```text
Permission Granted

≠

Operation Guaranteed
```

---

# Reglas de Interpretación

## REG-001

Los ejemplos no crean nuevas reglas del dominio.

---

## REG-002

Ante cualquier diferencia entre un ejemplo y un documento
normativo del Aggregate, prevalece el documento normativo
correspondiente.

---

## REG-003

Todo ejemplo válido debe preservar VotingId.

---

## REG-004

Todo ejemplo válido debe preservar OrganizationId.

---

## REG-005

Todo cambio de VotingStatus debe corresponder a una transición
oficial.

---

## REG-006

Toda modificación válida debe preservar las Invariants.

---

## REG-007

Toda modificación válida incrementa Version.

---

## REG-008

Toda operación rechazada conserva Version.

---

## REG-009

Toda operación rechazada conserva el estado anterior.

---

## REG-010

Una operación rechazada no produce el Domain Event de éxito.

---

## REG-011

Una Permission concedida no reemplaza la validación de dominio.

---

## REG-012

Voting nunca modifica directamente otro Aggregate.

---

## REG-013

Los identificadores externos representan referencias y no
ownership.

---

## REG-014

Archived continúa siendo terminal en todos los ejemplos.

---

## REG-015

Los ejemplos no pueden utilizarse para inferir estados, Commands,
Events, Permissions o transiciones no definidos explícitamente por
el modelo.

---

# Compatibilidad con Lifecycle

Todos los ejemplos de transición respetan:

```text
DOMAIN-009A-Lifecycle.md
```

y exclusivamente:

```text
No Voting → Draft

Draft → Open

Draft → Cancelled

Open → Closed

Closed → Archived

Cancelled → Archived
```

---

# Compatibilidad con State Machine

Los ejemplos no permiten transiciones fuera de:

```text
DOMAIN-009B-State-Machine.md
```

Toda transición no reconocida resulta:

```text
Rejected
```

---

# Compatibilidad con Commands

Los ejemplos utilizan exclusivamente los Commands definidos en:

```text
DOMAIN-009C-Commands.md
```

```text
CreateVoting

OpenVoting

CloseVoting

CancelVoting

ArchiveVoting

ChangeVotingType

ChangeVotingTitle

ChangeVotingDescription

ChangeVotingRules

AddVotingOption

RemoveVotingOption
```

---

# Compatibilidad con Domain Events

Los ejemplos utilizan exclusivamente los Domain Events definidos
en:

```text
DOMAIN-009D-Domain-Events.md
```

```text
VotingCreated

VotingOpened

VotingClosed

VotingCancelled

VotingArchived

VotingTypeChanged

VotingTitleChanged

VotingDescriptionChanged

VotingRulesChanged

VotingOptionAdded

VotingOptionRemoved
```

---

# Compatibilidad con Invariants

Todo escenario aceptado debe mantener:

```text
Invariant Before = true

↓

Valid Operation

↓

Invariant After = true
```

Los escenarios que producirían:

```text
Invariant After = false
```

son rechazados.

---

# Compatibilidad con Permissions

Los ejemplos utilizan exclusivamente las Permissions definidas en:

```text
DOMAIN-009F-Permissions.md
```

```text
Voting.Create

Voting.Open

Voting.Close

Voting.Cancel

Voting.Archive

Voting.ChangeType

Voting.ChangeTitle

Voting.ChangeDescription

Voting.ChangeRules

Voting.AddOption

Voting.RemoveOption

Voting.Read
```

---

# Compatibilidad con Repository Contract

Los ejemplos de persistencia utilizan exclusivamente:

```text
getById()

save()

exists()
```

según:

```text
DOMAIN-009G-Repository-Contract.md
```

---

# Compatibilidad con Versioning

Todos los ejemplos deben mantener:

```text
Valid Modification

↓

Version + 1
```

y:

```text
Rejected Operation

↓

Version unchanged
```

La especificación normativa pertenece a:

```text
DOMAIN-009I-Versioning.md
```

---

# Compatibilidad con Consistency Boundary

Todos los ejemplos mantienen:

```text
Voting

=

Independent Consistency Boundary
```

Los Aggregates externos continúan fuera del límite:

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

---

# Definición de Éxito

Los ejemplos del Aggregate **Voting** demuestran de forma
consistente el comportamiento definido por la serie documental
`DOMAIN-009`.

Los escenarios muestran que:

- Voting nace en Draft;
- Draft puede evolucionar hacia Open o Cancelled;
- Open puede evolucionar hacia Closed;
- Closed puede evolucionar hacia Archived;
- Cancelled puede evolucionar hacia Archived;
- Archived permanece terminal;
- los Commands representan intenciones;
- los Domain Events representan hechos;
- las Permissions no sustituyen las reglas del dominio;
- las Invariants permanecen obligatorias;
- las modificaciones de configuración no introducen por sí mismas
  transiciones de Lifecycle;
- VotingId permanece inmutable;
- OrganizationId permanece inmutable;
- Version aumenta únicamente ante modificaciones válidas;
- las operaciones rechazadas preservan estado y Version;
- el Repository trabaja con Voting como unidad;
- la concurrencia optimista protege modificaciones confirmadas;
- las referencias externas utilizan identificadores;
- Voting no absorbe ni modifica directamente otros Aggregates;
- Result, Options y contexto permanecen bajo las reglas propias del
  Aggregate;
- Archived representa preservación histórica y no eliminación.

De esta forma, `DOMAIN-009H-Examples.md` proporciona ejemplos
conceptuales coherentes con el Aggregate **Voting** sin ampliar,
reinterpretar ni modificar las decisiones de dominio ya
consolidadas por AURA Core.