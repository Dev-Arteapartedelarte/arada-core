# DOMAIN-009M — Voting Test Scenarios

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

Documentos Relacionados:

- DOMAIN-009-Aggregate.md
- DOMAIN-009A-Lifecycle.md
- DOMAIN-009B-State-Machine.md
- DOMAIN-009C-Commands.md
- DOMAIN-009D-Domain-Events.md
- DOMAIN-009E-Invariants.md
- DOMAIN-009F-Permissions.md
- DOMAIN-009G-Repository-Contract.md
- DOMAIN-009H-Examples.md
- DOMAIN-009I-Versioning.md
- DOMAIN-009J-Consistency-Boundary.md
- DOMAIN-009K-Integration-Events.md
- DOMAIN-009L-Read-Model.md
- DOMAIN-009N-Performance-Rules.md
- DOMAIN-009O-Security-Model.md
- CORE-006-Domain-Invariants.md
- CORE-008-Aggregate-Design-Rules.md
- CORE-011-Repository-Contracts.md

---

# Objetivo

Definir los escenarios conceptuales de prueba necesarios para
verificar que el Aggregate **Voting** cumple las reglas establecidas
por la serie documental `DOMAIN-009`.

Los escenarios deben verificar conjuntamente:

- identidad;
- contexto organizacional;
- Lifecycle;
- State Machine;
- Commands;
- Domain Events;
- Invariants;
- Permissions;
- Repository Contract;
- Versioning;
- Consistency Boundary;
- Integration Events;
- Read Models.

Los Test Scenarios no agregan comportamiento al dominio.

No definen:

- nuevos estados;
- nuevas transiciones;
- nuevos Commands;
- nuevos Domain Events;
- nuevas Permissions;
- nuevas Invariants;
- nuevos Integration Events;
- nuevos Read Models.

Su responsabilidad es comprobar el comportamiento ya definido.

---

# Principios

Todo escenario debe verificar exclusivamente reglas existentes del
Aggregate.

Debe mantenerse:

```text
Domain Specification

↓

Test Scenario

↓

Expected Domain Behavior
```

No:

```text
Test Scenario

↓

New Domain Rule
```

Los escenarios deben comprobar:

- estado inicial;
- intención ejecutada;
- condiciones aplicables;
- resultado esperado;
- estado resultante;
- Version resultante;
- Domain Event esperado cuando corresponda;
- ausencia de modificación cuando la operación sea rechazada.

---

# Escenarios de Creación

## TS-001 — Crear Voting Válido

Estado inicial:

```text
Voting does not exist
```

Command:

```text
CreateVoting
```

Precondiciones:

```text
Valid VotingId

Valid OrganizationId

Valid VotingType

Valid Title

Valid Rules

Valid Creation Invariants
```

Resultado esperado:

```text
Voting exists

VotingStatus = Draft

Version = 1
```

Domain Event esperado:

```text
VotingCreated
```

Debe verificarse:

```text
VotingCreated.AggregateVersion = 1
```

---

## TS-002 — VotingId Duplicado

Precondición:

```text
exists(VotingId) = true
```

Command:

```text
CreateVoting
```

utilizando el mismo VotingId.

Resultado esperado:

```text
Rejected
```

No debe producirse:

```text
VotingCreated
```

No debe reemplazarse el Voting existente.

---

## TS-003 — OrganizationId Obligatorio

Command:

```text
CreateVoting
```

sin un OrganizationId válido.

Resultado esperado:

```text
Rejected
```

No debe existir un nuevo Voting válido.

No debe producirse:

```text
VotingCreated
```

---

## TS-004 — Estado Inicial

Después de una creación válida debe verificarse:

```text
VotingStatus = Draft
```

No puede resultar directamente:

```text
Open

Closed

Cancelled

Archived
```

---

# Escenarios de Identidad

## TS-005 — VotingId Inmutable

Estado inicial:

```text
VotingId = VOT-001
```

Después de cualquier modificación válida debe mantenerse:

```text
VotingId = VOT-001
```

---

## TS-006 — OrganizationId Inmutable

Estado inicial:

```text
OrganizationId = ORG-001
```

Después de cualquier modificación válida debe mantenerse:

```text
OrganizationId = ORG-001
```

No debe existir una operación ordinaria que produzca:

```text
OrganizationId = ORG-002
```

sobre el mismo Voting.

---

# Escenarios de Apertura

## TS-007 — Abrir Voting desde Draft

Estado inicial:

```text
VotingStatus = Draft

Version = N
```

Command:

```text
OpenVoting
```

con todas las Invariants de apertura satisfechas.

Resultado esperado:

```text
VotingStatus = Open

OpenedAt exists

Version = N + 1
```

Domain Event esperado:

```text
VotingOpened
```

Debe verificarse:

```text
VotingOpened.AggregateVersion = N + 1
```

---

## TS-008 — Abrir Voting desde Open

Estado inicial:

```text
VotingStatus = Open

Version = N
```

Command:

```text
OpenVoting
```

Resultado esperado:

```text
Rejected
```

Debe mantenerse:

```text
VotingStatus = Open

Version = N
```

No debe producirse:

```text
VotingOpened
```

---

## TS-009 — Abrir Voting desde Closed

Estado inicial:

```text
VotingStatus = Closed

Version = N
```

Command:

```text
OpenVoting
```

Resultado esperado:

```text
Rejected
```

No debe existir:

```text
Closed → Open
```

Version permanece:

```text
N
```

---

## TS-010 — Abrir Voting desde Cancelled

Estado inicial:

```text
VotingStatus = Cancelled
```

Command:

```text
OpenVoting
```

Resultado esperado:

```text
Rejected
```

No debe existir:

```text
Cancelled → Open
```

---

## TS-011 — Abrir Voting desde Archived

Estado inicial:

```text
VotingStatus = Archived
```

Command:

```text
OpenVoting
```

Resultado esperado:

```text
Rejected
```

Archived permanece terminal.

---

## TS-012 — Apertura con Invariant Inválida

Estado inicial:

```text
VotingStatus = Draft

Version = N
```

Command:

```text
OpenVoting
```

cuando una Invariant necesaria para la apertura no se cumple.

Resultado esperado:

```text
Rejected
```

Debe mantenerse:

```text
VotingStatus = Draft

Version = N
```

No debe producirse:

```text
VotingOpened
```

---

# Escenarios de Cierre

## TS-013 — Cerrar Voting desde Open

Estado inicial:

```text
VotingStatus = Open

OpenedAt = T1

Version = N
```

Command:

```text
CloseVoting
```

con las condiciones de cierre válidas.

Resultado esperado:

```text
VotingStatus = Closed

ClosedAt = T2

Version = N + 1
```

Debe cumplirse:

```text
T2 >= T1
```

Domain Event esperado:

```text
VotingClosed
```

---

## TS-014 — Cerrar Voting desde Draft

Estado inicial:

```text
VotingStatus = Draft

Version = N
```

Command:

```text
CloseVoting
```

Resultado esperado:

```text
Rejected
```

No debe existir:

```text
Draft → Closed
```

Version permanece:

```text
N
```

No debe producirse:

```text
VotingClosed
```

---

## TS-015 — Cerrar Voting desde Closed

Estado inicial:

```text
VotingStatus = Closed
```

Command:

```text
CloseVoting
```

Resultado esperado:

```text
Rejected
```

No debe producirse un nuevo:

```text
VotingClosed
```

---

## TS-016 — Cerrar Voting desde Cancelled

Estado inicial:

```text
VotingStatus = Cancelled
```

Command:

```text
CloseVoting
```

Resultado esperado:

```text
Rejected
```

No existe:

```text
Cancelled → Closed
```

---

## TS-017 — Cerrar Voting desde Archived

Estado inicial:

```text
VotingStatus = Archived
```

Command:

```text
CloseVoting
```

Resultado esperado:

```text
Rejected
```

Archived permanece terminal.

---

## TS-018 — Cierre con Result Inválido

Estado inicial:

```text
VotingStatus = Open

Version = N
```

Cuando el cierre requiera Result y este no sea coherente con las
Rules correspondientes:

```text
CloseVoting
```

debe producir:

```text
Rejected
```

Debe mantenerse:

```text
VotingStatus = Open

Version = N
```

No debe producirse:

```text
VotingClosed
```

---

# Escenarios de Cancelación

## TS-019 — Cancelar Voting desde Draft

Estado inicial:

```text
VotingStatus = Draft

Version = N
```

Command:

```text
CancelVoting
```

Resultado esperado:

```text
VotingStatus = Cancelled

CancelledAt exists

Version = N + 1
```

Domain Event esperado:

```text
VotingCancelled
```

---

## TS-020 — Cancelar Voting desde Open

Estado inicial:

```text
VotingStatus = Open

Version = N
```

Command:

```text
CancelVoting
```

Resultado esperado:

```text
Rejected
```

La versión 1.0 no permite:

```text
Open → Cancelled
```

Debe mantenerse:

```text
VotingStatus = Open

Version = N
```

No debe producirse:

```text
VotingCancelled
```

---

## TS-021 — Cancelar Voting desde Closed

Estado inicial:

```text
VotingStatus = Closed
```

Command:

```text
CancelVoting
```

Resultado esperado:

```text
Rejected
```

---

## TS-022 — Cancelar Voting desde Cancelled

Estado inicial:

```text
VotingStatus = Cancelled
```

Command:

```text
CancelVoting
```

Resultado esperado:

```text
Rejected
```

No debe producirse un nuevo:

```text
VotingCancelled
```

---

## TS-023 — Cancelar Voting desde Archived

Estado inicial:

```text
VotingStatus = Archived
```

Command:

```text
CancelVoting
```

Resultado esperado:

```text
Rejected
```

---

# Escenarios de Archivado

## TS-024 — Archivar Voting Closed

Estado inicial:

```text
VotingStatus = Closed

Version = N
```

Command:

```text
ArchiveVoting
```

Resultado esperado:

```text
VotingStatus = Archived

ArchivedAt exists

Version = N + 1
```

Domain Event esperado:

```text
VotingArchived
```

---

## TS-025 — Archivar Voting Cancelled

Estado inicial:

```text
VotingStatus = Cancelled

Version = N
```

Command:

```text
ArchiveVoting
```

Resultado esperado:

```text
VotingStatus = Archived

ArchivedAt exists

Version = N + 1
```

Domain Event esperado:

```text
VotingArchived
```

---

## TS-026 — Archivar Voting Draft

Estado inicial:

```text
VotingStatus = Draft

Version = N
```

Command:

```text
ArchiveVoting
```

Resultado esperado:

```text
Rejected
```

No debe existir:

```text
Draft → Archived
```

Version permanece:

```text
N
```

---

## TS-027 — Archivar Voting Open

Estado inicial:

```text
VotingStatus = Open
```

Command:

```text
ArchiveVoting
```

Resultado esperado:

```text
Rejected
```

No debe existir:

```text
Open → Archived
```

---

## TS-028 — Archived es Terminal

Estado inicial:

```text
VotingStatus = Archived
```

Debe verificarse que ninguna transición ordinaria produzca:

```text
Archived → Draft

Archived → Open

Archived → Closed

Archived → Cancelled
```

Voting permanece:

```text
Archived
```

---

# Escenarios de VotingType

## TS-029 — Cambiar VotingType Válidamente

Estado inicial:

```text
VotingType = VotingTypeA

Version = N
```

Command:

```text
ChangeVotingType(
    NewVotingType = VotingTypeB
)
```

cuando la operación sea válida conforme al estado e Invariants.

Resultado esperado:

```text
VotingType = VotingTypeB

VotingStatus = Previous VotingStatus

Version = N + 1
```

Domain Event esperado:

```text
VotingTypeChanged
```

---

## TS-030 — VotingType Inválido

Command:

```text
ChangeVotingType(
    NewVotingType = InvalidVotingType
)
```

Resultado esperado:

```text
Rejected
```

Debe mantenerse:

```text
VotingType = PreviousVotingType

VotingStatus = PreviousVotingStatus

Version = PreviousVersion
```

No debe producirse:

```text
VotingTypeChanged
```

---

# Escenarios de Title

## TS-031 — Cambiar Title Válidamente

Estado inicial:

```text
Title = Title A

Version = N
```

Command:

```text
ChangeVotingTitle(
    NewTitle = Title B
)
```

cuando el cambio se encuentre permitido.

Resultado esperado:

```text
Title = Title B

VotingStatus = Previous VotingStatus

Version = N + 1
```

Domain Event esperado:

```text
VotingTitleChanged
```

---

## TS-032 — Title Inválido

Command:

```text
ChangeVotingTitle(
    NewTitle = InvalidTitle
)
```

Resultado esperado:

```text
Rejected
```

Debe mantenerse:

```text
Title = PreviousTitle

Version = PreviousVersion
```

No debe producirse:

```text
VotingTitleChanged
```

---

# Escenarios de Description

## TS-033 — Cambiar Description Válidamente

Estado inicial:

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

cuando la operación sea válida.

Resultado esperado:

```text
Description = Description B

VotingStatus = Previous VotingStatus

Version = N + 1
```

Domain Event esperado:

```text
VotingDescriptionChanged
```

---

## TS-034 — Description Inválida

Cuando NewDescription no cumpla las reglas correspondientes:

```text
ChangeVotingDescription
```

debe resultar:

```text
Rejected
```

Debe preservarse:

```text
Description = PreviousDescription

Version = PreviousVersion
```

No debe producirse:

```text
VotingDescriptionChanged
```

---

# Escenarios de Rules

## TS-035 — Cambiar Rules Válidamente

Estado inicial:

```text
Rules = Rules A

Version = N
```

Command:

```text
ChangeVotingRules(
    NewRules = Rules B
)
```

cuando:

```text
NewRules are valid

VotingType remains compatible

Options remain compatible when applicable

All Invariants remain valid
```

Resultado esperado:

```text
Rules = Rules B

VotingStatus = Previous VotingStatus

Version = N + 1
```

Domain Event esperado:

```text
VotingRulesChanged
```

---

## TS-036 — Rules Inválidas

Command:

```text
ChangeVotingRules(
    NewRules = InvalidRules
)
```

Resultado esperado:

```text
Rejected
```

Debe mantenerse:

```text
Rules = PreviousRules

Version = PreviousVersion
```

No debe producirse:

```text
VotingRulesChanged
```

---

## TS-037 — Rules Incompatibles con Options

Cuando una modificación de Rules produciría Options inválidas o
incompatibles:

```text
ChangeVotingRules
```

debe resultar:

```text
Rejected
```

El Aggregate debe conservar su estado anterior completo.

---

# Escenarios de Options

## TS-038 — Agregar VotingOption Válida

Estado inicial:

```text
Options = CurrentOptions

Version = N
```

Command:

```text
AddVotingOption
```

con una VotingOption válida y compatible.

Resultado esperado:

```text
Options = UpdatedOptions

VotingStatus = Previous VotingStatus

Version = N + 1
```

Domain Event esperado:

```text
VotingOptionAdded
```

---

## TS-039 — Agregar VotingOption Inválida

Command:

```text
AddVotingOption
```

con una Option que viola VotingType, Rules o Invariants.

Resultado esperado:

```text
Rejected
```

Debe mantenerse:

```text
Options = PreviousOptions

Version = PreviousVersion
```

No debe producirse:

```text
VotingOptionAdded
```

---

## TS-040 — Eliminar VotingOption Válidamente

Estado inicial:

```text
Options = CurrentOptions

Version = N
```

Command:

```text
RemoveVotingOption
```

sobre una Option existente cuando el conjunto resultante permanece
válido.

Resultado esperado:

```text
Options = UpdatedOptions

VotingStatus = Previous VotingStatus

Version = N + 1
```

Domain Event esperado:

```text
VotingOptionRemoved
```

---

## TS-041 — Eliminar VotingOption Inexistente

Command:

```text
RemoveVotingOption
```

sobre una Option que no pertenece a Voting.

Resultado esperado:

```text
Rejected
```

No se modifica:

```text
Options

Version
```

No debe producirse:

```text
VotingOptionRemoved
```

---

## TS-042 — Eliminar VotingOption y Romper Invariants

Cuando la eliminación de una Option dejaría un conjunto inválido
según VotingType o Rules:

```text
RemoveVotingOption
```

debe resultar:

```text
Rejected
```

El Aggregate conserva las Options anteriores.

---

# Escenarios de Permissions

## TS-043 — Permission Concedida y Dominio Válido

Cuando:

```text
Required Permission = Granted
```

y todas las condiciones del dominio son válidas:

```text
Command
```

puede ser aceptado.

Debe verificarse que la Permission no sustituye las validaciones del
Aggregate.

---

## TS-044 — Permission Denegada

Cuando:

```text
Required Permission = Denied
```

la operación protegida debe resultar:

```text
Denied
```

Debe mantenerse:

```text
Aggregate State = Previous State

Version = Previous Version
```

No debe producirse el Domain Event de éxito.

---

## TS-045 — Permission Concedida con Transición Inválida

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

Resultado esperado:

```text
Rejected
```

Debe verificarse:

```text
Permission Granted

≠

State Transition Guaranteed
```

---

## TS-046 — Permission Concedida con Invariant Inválida

Permission:

```text
Voting.ChangeRules = Granted
```

Command:

```text
ChangeVotingRules
```

con Rules inválidas.

Resultado esperado:

```text
Rejected
```

Debe verificarse:

```text
Permission Granted

≠

Invariant Bypass
```

---

## TS-047 — Voting.Read no Modifica Voting

Permission:

```text
Voting.Read
```

Operación:

```text
Read Voting
```

Debe mantenerse:

```text
VotingStatus = Previous VotingStatus

Version = Previous Version
```

La lectura no produce Domain Events de modificación.

---

# Escenarios de Versioning

## TS-048 — Modificación Válida Incrementa Version

Estado inicial:

```text
Version = N
```

Después de cualquier modificación válida:

```text
Version = N + 1
```

---

## TS-049 — Command Rechazado no Incrementa Version

Estado inicial:

```text
Version = N
```

Command inválido:

```text
Rejected Command
```

Resultado:

```text
Version = N
```

---

## TS-050 — Lectura no Incrementa Version

Estado inicial:

```text
Version = N
```

Operaciones:

```text
getById()

exists()

Read Voting
```

Resultado esperado:

```text
Version = N
```

---

## TS-051 — Version Monotónica

Para modificaciones válidas consecutivas debe verificarse:

```text
Version N

↓

Version N + 1

↓

Version N + 2
```

No debe ocurrir:

```text
Version N + 1

↓

Version N
```

---

# Escenarios de Concurrencia

## TS-052 — Persistencia con ExpectedVersion Correcta

Estado persistido:

```text
PersistedVersion = N
```

Una modificación válida fue calculada desde:

```text
ExpectedVersion = N
```

Resultado esperado:

```text
Persistence Accepted
```

y el nuevo estado corresponde a:

```text
Version = N + 1
```

---

## TS-053 — Conflicto de Concurrencia

Estado persistido:

```text
PersistedVersion = N + 1
```

Una operación intenta persistir una modificación calculada desde:

```text
ExpectedVersion = N
```

Resultado esperado:

```text
ConcurrencyConflict
```

No debe sobrescribirse el estado persistido.

---

## TS-054 — Conflicto no Produce Domain Event de Éxito

Ante:

```text
ConcurrencyConflict
```

debe verificarse que no se confirma un nuevo Domain Event de éxito
para la modificación rechazada.

---

# Escenarios de Repository Contract

## TS-055 — getById Recupera Voting

Para un Voting persistido:

```text
getById(VotingId)
```

debe recuperar el Aggregate con su estado necesario para preservar
correctamente:

```text
VotingId

OrganizationId

VotingStatus

Rules

Options

Result when applicable

Lifecycle Timestamps

Version
```

según corresponda al Voting persistido.

---

## TS-056 — getById no Modifica Version

Estado persistido:

```text
Version = N
```

Después de:

```text
getById(VotingId)
```

debe mantenerse:

```text
Version = N
```

---

## TS-057 — exists no Modifica Estado

Operación:

```text
exists(VotingId)
```

debe producir exclusivamente:

```text
true
```

o:

```text
false
```

sin modificar Voting.

---

## TS-058 — save Preserva Identidad

Después de:

```text
save(Voting)
```

debe mantenerse:

```text
Persisted VotingId = Voting.VotingId

Persisted OrganizationId = Voting.OrganizationId
```

---

## TS-059 — Rehidratación

Un Voting persistido con:

```text
VotingStatus = Closed

Version = N
```

debe reconstruirse como:

```text
VotingStatus = Closed

Version = N
```

La rehidratación no debe producir nuevos Domain Events.

---

# Escenarios de Domain Events

## TS-060 — Event Type Correcto

Para cada Command válido debe verificarse la correspondencia:

| Command | Domain Event |
| --- | --- |
| CreateVoting | VotingCreated |
| OpenVoting | VotingOpened |
| CloseVoting | VotingClosed |
| CancelVoting | VotingCancelled |
| ArchiveVoting | VotingArchived |
| ChangeVotingType | VotingTypeChanged |
| ChangeVotingTitle | VotingTitleChanged |
| ChangeVotingDescription | VotingDescriptionChanged |
| ChangeVotingRules | VotingRulesChanged |
| AddVotingOption | VotingOptionAdded |
| RemoveVotingOption | VotingOptionRemoved |

---

## TS-061 — AggregateId Correcto

Todo Domain Event debe mantener:

```text
DomainEvent.VotingId

=

Voting.VotingId
```

---

## TS-062 — OrganizationId Correcto

Todo Domain Event que preserve el contexto organizacional debe
mantener:

```text
DomainEvent.OrganizationId

=

Voting.OrganizationId
```

---

## TS-063 — AggregateVersion Correcta

Después de una modificación válida:

```text
Voting.Version = N
```

el Domain Event correspondiente debe mantener:

```text
AggregateVersion = N
```

---

## TS-064 — No Event on Failure

Cuando una operación resulta:

```text
Rejected
```

no debe producirse el Domain Event de éxito correspondiente.

Debe verificarse para todos los Commands oficiales.

---

## TS-065 — Evento Histórico Inmutable

Un Domain Event previamente producido debe conservar sus valores
históricos aunque Voting cambie posteriormente.

Ejemplo:

```text
VotingTitleChanged
PreviousTitle = Title A
NewTitle = Title B
```

no debe modificarse cuando posteriormente ocurra otro:

```text
VotingTitleChanged
PreviousTitle = Title B
NewTitle = Title C
```

---

# Escenarios de Lifecycle

## TS-066 — Flujo Normal Completo

Debe aceptarse la secuencia:

```text
No Voting

↓

CreateVoting

↓

Draft

↓

OpenVoting

↓

Open

↓

CloseVoting

↓

Closed

↓

ArchiveVoting

↓

Archived
```

Los Domain Events correspondientes deben ser:

```text
VotingCreated

VotingOpened

VotingClosed

VotingArchived
```

en el orden lógico definido por AggregateVersion.

---

## TS-067 — Flujo Cancelado Completo

Debe aceptarse:

```text
No Voting

↓

CreateVoting

↓

Draft

↓

CancelVoting

↓

Cancelled

↓

ArchiveVoting

↓

Archived
```

Los Domain Events correspondientes son:

```text
VotingCreated

VotingCancelled

VotingArchived
```

---

## TS-068 — Transiciones No Permitidas

Debe verificarse el rechazo de:

```text
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

Ninguna operación rechazada debe modificar Version.

---

# Escenarios Temporales

## TS-069 — Flujo Temporal Normal

Cuando Voting siga:

```text
Draft → Open → Closed → Archived
```

debe verificarse:

```text
CreatedAt <= OpenedAt <= ClosedAt <= ArchivedAt
```

---

## TS-070 — Flujo Temporal Cancelado

Cuando Voting siga:

```text
Draft → Cancelled → Archived
```

debe verificarse:

```text
CreatedAt <= CancelledAt <= ArchivedAt
```

---

## TS-071 — Preservación de Timestamps

Después de archivar un Voting cerrado deben preservarse:

```text
CreatedAt

OpenedAt

ClosedAt

ArchivedAt
```

con sus valores históricos correspondientes.

---

# Escenarios de Consistency Boundary

## TS-072 — Command modifica únicamente Voting

Cuando:

```text
CloseVoting
```

sea aceptado, puede modificar el estado interno correspondiente de
Voting.

No debe modificar directamente:

```text
Organization

Assembly

Proposal

Participation
```

---

## TS-073 — AssemblyId es Referencia

Cuando Voting mantenga:

```text
AssemblyId
```

debe verificarse que la relación representa:

```text
Reference
```

y no:

```text
Ownership
```

Un Command de Voting no modifica directamente Assembly.

---

## TS-074 — ProposalId es Referencia

Cuando Voting mantenga:

```text
ProposalId
```

un cierre de Voting no debe modificar directamente Proposal.

Debe mantenerse:

```text
VotingClosed

≠

Direct Proposal Mutation
```

---

## TS-075 — Participation Permanece Separada

Debe verificarse:

```text
Voting

≠

Participation
```

Una transición de Voting no debe modificar directamente el estado
interno de Participation.

---

# Escenarios de Integration Events

## TS-076 — VotingCreatedIntegrationEvent

Cuando se confirma:

```text
VotingCreated
```

y corresponde producir su Integration Event, este debe representar:

```text
VotingCreatedIntegrationEvent
```

preservando la identidad y AggregateVersion correspondientes.

---

## TS-077 — VotingOpenedIntegrationEvent

Cuando se confirma:

```text
VotingOpened
```

el Integration Event correspondiente es:

```text
VotingOpenedIntegrationEvent
```

cuando aplique el contrato de integración.

---

## TS-078 — VotingClosedIntegrationEvent

Cuando se confirma:

```text
VotingClosed
```

el Integration Event correspondiente es:

```text
VotingClosedIntegrationEvent
```

cuando aplique el contrato de integración.

El Integration Event no modifica directamente Proposal, Assembly ni
Participation.

---

## TS-079 — VotingCancelledIntegrationEvent

Cuando se confirma:

```text
VotingCancelled
```

el Integration Event correspondiente es:

```text
VotingCancelledIntegrationEvent
```

cuando aplique el contrato de integración.

Cancelled no debe interpretarse como Deleted.

---

## TS-080 — VotingArchivedIntegrationEvent

Cuando se confirma:

```text
VotingArchived
```

el Integration Event correspondiente es:

```text
VotingArchivedIntegrationEvent
```

cuando aplique el contrato de integración.

Archived no debe interpretarse como eliminación física.

---

## TS-081 — Command Rechazado no Produce Integration Event

Cuando:

```text
Command

↓

Rejected
```

no debe producirse:

```text
Success Domain Event
```

ni:

```text
Success Integration Event
```

---

## TS-082 — Integration Event no Incrementa Version

Si:

```text
Voting.Version = N
```

la generación o publicación del Integration Event correspondiente
debe mantener:

```text
Voting.Version = N
```

---

# Escenarios de Read Model

## TS-083 — VotingSummary es Solo Lectura

Una instancia de:

```text
VotingSummary
```

puede representar información derivada del Voting.

No debe permitir:

```text
Domain Mutation
```

---

## TS-084 — VotingDetailView no es Aggregate

Debe verificarse:

```text
VotingDetailView

≠

Voting Aggregate
```

La proyección no puede ejecutar Commands ni modificar Voting.

---

## TS-085 — VotingHistoryView Preserva Orden

Cuando existan hechos:

```text
AggregateVersion = 1

AggregateVersion = 2

AggregateVersion = 3
```

VotingHistoryView debe preservar su orden lógico.

---

## TS-086 — VotingResultView no Crea Result

Cuando no exista un Result confirmado por el dominio:

```text
VotingResultView
```

no debe inventar un Result.

Debe mantenerse:

```text
No Confirmed Result

↓

No Invented Result
```

---

## TS-087 — Actualización de Proyección no Modifica Voting

Cuando un Domain Event actualiza un Read Model:

```text
Domain Event

↓

Projection
```

debe mantenerse:

```text
Voting.Version = Previous Voting.Version
```

La actualización del Read Model no constituye una nueva modificación
del Aggregate.

---

## TS-088 — Reconstrucción de Read Model

El Replay utilizado para reconstruir una proyección no debe:

- ejecutar Commands sobre Voting;
- incrementar Voting.Version;
- producir nuevos Domain Events;
- modificar los hechos históricos originales.

---

# Escenarios de Archived

## TS-089 — Archived Conserva Identidad

Después de archivar debe mantenerse:

```text
VotingId = Previous VotingId

OrganizationId = Previous OrganizationId
```

---

## TS-090 — Archived Conserva Historia

Un Voting Archived debe conservar los hechos y timestamps anteriores
que correspondan a su Lifecycle.

Archived no significa:

```text
Delete History
```

---

## TS-091 — Archived Rechaza Modificación Ordinaria

Estado:

```text
VotingStatus = Archived

Version = N
```

Command ordinario de modificación:

```text
ChangeVotingTitle
```

Resultado esperado:

```text
Rejected
```

Debe mantenerse:

```text
VotingStatus = Archived

Version = N
```

No debe producirse:

```text
VotingTitleChanged
```

---

# Escenarios de Result

## TS-092 — Result no es VotingStatus

Cuando Result exista debe verificarse:

```text
Result

≠

VotingStatus
```

Los estados continúan limitados a:

```text
Draft

Open

Closed

Cancelled

Archived
```

---

## TS-093 — Result no Modifica Proposal Directamente

Cuando Voting posea:

```text
ProposalId
```

y alcance un Result válido, debe mantenerse:

```text
Voting Result

≠

Direct Proposal State Mutation
```

---

# Escenarios de No-Op

## TS-094 — Operación sin Modificación Efectiva

Cuando una operación no represente una modificación efectiva según
las reglas del Command correspondiente, no debe considerarse una
nueva modificación válida.

Debe mantenerse:

```text
State = Previous State

Version = Previous Version
```

y no debe producirse el Domain Event de modificación
correspondiente.

---

# Matriz de Cobertura de Commands

| Command | Éxito | Rechazo | Version | Domain Event |
| --- | --- | --- | --- | --- |
| CreateVoting | Sí | Sí | Verificada | VotingCreated |
| OpenVoting | Sí | Sí | Verificada | VotingOpened |
| CloseVoting | Sí | Sí | Verificada | VotingClosed |
| CancelVoting | Sí | Sí | Verificada | VotingCancelled |
| ArchiveVoting | Sí | Sí | Verificada | VotingArchived |
| ChangeVotingType | Sí | Sí | Verificada | VotingTypeChanged |
| ChangeVotingTitle | Sí | Sí | Verificada | VotingTitleChanged |
| ChangeVotingDescription | Sí | Sí | Verificada | VotingDescriptionChanged |
| ChangeVotingRules | Sí | Sí | Verificada | VotingRulesChanged |
| AddVotingOption | Sí | Sí | Verificada | VotingOptionAdded |
| RemoveVotingOption | Sí | Sí | Verificada | VotingOptionRemoved |

---

# Matriz de Cobertura de Estados

| Estado | Entrada válida | Salida válida |
| --- | --- | --- |
| Draft | CreateVoting | OpenVoting, CancelVoting |
| Open | OpenVoting | CloseVoting |
| Closed | CloseVoting | ArchiveVoting |
| Cancelled | CancelVoting | ArchiveVoting |
| Archived | ArchiveVoting | Ninguna |

La columna de entrada representa el Command que produce el estado
desde una transición válida del Lifecycle.

---

# Matriz de Cobertura de Domain Events

| Domain Event | Event Type | VotingId | OrganizationId | AggregateVersion | No Event on Failure |
| --- | --- | --- | --- | --- | --- |
| VotingCreated | Verificar | Verificar | Verificar | Verificar | Verificar |
| VotingOpened | Verificar | Verificar | Verificar | Verificar | Verificar |
| VotingClosed | Verificar | Verificar | Verificar | Verificar | Verificar |
| VotingCancelled | Verificar | Verificar | Verificar | Verificar | Verificar |
| VotingArchived | Verificar | Verificar | Verificar | Verificar | Verificar |
| VotingTypeChanged | Verificar | Verificar | Verificar | Verificar | Verificar |
| VotingTitleChanged | Verificar | Verificar | Verificar | Verificar | Verificar |
| VotingDescriptionChanged | Verificar | Verificar | Verificar | Verificar | Verificar |
| VotingRulesChanged | Verificar | Verificar | Verificar | Verificar | Verificar |
| VotingOptionAdded | Verificar | Verificar | Verificar | Verificar | Verificar |
| VotingOptionRemoved | Verificar | Verificar | Verificar | Verificar | Verificar |

---

# Reglas

## REG-001

Todo Command válido debe contar con al menos un escenario que
verifique su comportamiento esperado.

---

## REG-002

Todo Command debe contar con escenarios de rechazo cuando el estado
o las Invariants no permitan la operación.

---

## REG-003

Toda transición oficial del Lifecycle debe ser verificada.

---

## REG-004

Toda transición no permitida relevante debe resultar rechazada.

---

## REG-005

Todo Domain Event debe verificarse únicamente después de una
modificación válida.

---

## REG-006

Una operación rechazada no debe producir el Domain Event de éxito.

---

## REG-007

Toda modificación válida debe verificar el incremento de Version.

---

## REG-008

Toda operación rechazada debe verificar que Version permanece sin
cambios.

---

## REG-009

Las operaciones de lectura no deben modificar Version.

---

## REG-010

Los escenarios de concurrencia deben verificar que una
ExpectedVersion obsoleta no sobrescriba una PersistedVersion más
reciente.

---

## REG-011

Los escenarios deben verificar la inmutabilidad de VotingId y
OrganizationId.

---

## REG-012

Los escenarios deben verificar que Voting no modifica directamente
otros Aggregates.

---

## REG-013

Los escenarios de Integration Events deben partir siempre de hechos
de dominio confirmados.

---

## REG-014

Los escenarios de Read Models deben verificar que las proyecciones
no poseen autoridad para modificar Voting.

---

## REG-015

Los Test Scenarios no pueden introducir comportamiento que no esté
definido por los documentos normativos del Aggregate.

---

# Definición de Éxito

El conjunto de Test Scenarios de **Voting** permite verificar de
forma sistemática que el Aggregate cumple las reglas establecidas
por la serie documental `DOMAIN-009`.

La cobertura debe demostrar que:

- Voting se crea únicamente en Draft;
- VotingId permanece único e inmutable;
- OrganizationId permanece obligatorio e inmutable;
- las transiciones válidas corresponden exactamente a la State
  Machine;
- las transiciones inválidas son rechazadas;
- Archived permanece terminal;
- los Commands válidos producen los cambios esperados;
- los Commands inválidos no modifican el Aggregate;
- las Invariants permanecen verdaderas antes y después de cada
  modificación válida;
- las Permissions no sustituyen las reglas del dominio;
- toda modificación válida incrementa Version;
- toda operación rechazada conserva Version;
- las lecturas no modifican Version;
- la concurrencia optimista impide sobrescrituras incompatibles;
- el Repository preserva identidad, estado y Version;
- la rehidratación no constituye una nueva modificación;
- cada Domain Event posee correspondencia con el hecho producido;
- un Command rechazado no genera el Domain Event de éxito;
- los eventos históricos permanecen inmutables;
- los Integration Events solo representan hechos confirmados;
- los Integration Events no modifican Voting;
- los Read Models permanecen derivados y sin autoridad de
  escritura;
- Voting mantiene su propio Consistency Boundary;
- los Aggregates externos permanecen fuera de dicho límite.

Los escenarios definidos en este documento validan las reglas
conceptuales ya establecidas y no agregan nuevas decisiones de
dominio ni arquitectura.

De esta forma, `DOMAIN-009M-Test-Scenarios.md` establece la
especificación conceptual oficial de pruebas del Aggregate
**Voting**, manteniendo el patrón consolidado de AURA Core.