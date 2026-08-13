# DOMAIN-009B — Voting State Machine

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
- DOMAIN-009C-Commands.md
- DOMAIN-009D-Domain-Events.md
- DOMAIN-009E-Invariants.md
- DOMAIN-009F-Permissions.md
- DOMAIN-009I-Versioning.md
- DOMAIN-009J-Consistency-Boundary.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Definir la State Machine oficial del Aggregate
**Voting**.

La State Machine formaliza las transiciones de estado
permitidas durante el Lifecycle de Voting.

Su propósito es garantizar que:

- Voting siempre mantenga un estado válido;
- las transiciones ocurran únicamente desde estados
  permitidos;
- cada transición sea provocada por un Command válido;
- cada transición preserve las Invariants;
- cada transición produzca el Domain Event
  correspondiente;
- las transiciones inválidas sean rechazadas;
- ninguna operación externa pueda modificar directamente
  VotingStatus.

La State Machine implementa conceptualmente el Lifecycle
definido en:

```text
DOMAIN-009A-Lifecycle.md
```

No introduce nuevos estados ni nuevas transiciones.

---

# Principios

La State Machine debe cumplir las siguientes reglas:

- Voting posee exactamente un VotingStatus;
- todo Voting nuevo comienza en Draft;
- VotingStatus nunca se modifica directamente;
- toda transición requiere un Command explícito;
- toda transición debe estar declarada en esta State
  Machine;
- toda transición debe validar su estado origen;
- toda transición debe preservar las Invariants;
- toda transición válida incrementa Version;
- toda transición válida genera el Domain Event
  correspondiente;
- una transición rechazada conserva el estado anterior;
- una transición rechazada conserva Version;
- una transición rechazada no genera un Domain Event de
  éxito;
- Archived es terminal;
- la State Machine de Voting no modifica estados de otros
  Aggregates.

---

# Estado

El estado del Aggregate se representa mediante:

```text
VotingStatus
```

Los estados oficiales son:

```text
Draft

Open

Closed

Cancelled

Archived
```

Estos estados corresponden exactamente al Lifecycle
definido para Voting.

---

# Estado Inicial

La creación de un Voting produce:

```text
No Voting

↓

CreateVoting

↓

Draft
```

El estado inicial oficial es:

```text
Draft
```

No puede crearse directamente un Voting en:

```text
Open

Closed

Cancelled

Archived
```

---

# Diagrama General

La State Machine oficial es:

```text
                 ┌───────────────┐
                 │     Draft     │
                 └───────┬───────┘
                         │
               ┌─────────┴─────────┐
               │                   │
          OpenVoting          CancelVoting
               │                   │
               ▼                   ▼
        ┌─────────────┐     ┌─────────────┐
        │    Open     │     │  Cancelled  │
        └──────┬──────┘     └──────┬──────┘
               │                   │
          CloseVoting         ArchiveVoting
               │                   │
               ▼                   │
        ┌─────────────┐             │
        │   Closed    │             │
        └──────┬──────┘             │
               │                   │
          ArchiveVoting            │
               │                   │
               └─────────┬─────────┘
                         ▼
                 ┌─────────────┐
                 │  Archived   │
                 └─────────────┘
```

---

# Transiciones Oficiales

La versión 1.0 define exclusivamente las siguientes
transiciones:

```text
No Voting → Draft

Draft → Open

Draft → Cancelled

Open → Closed

Closed → Archived

Cancelled → Archived
```

No existen otras transiciones de estado dentro de esta
versión.

---

# Tabla Oficial de Transiciones

| Estado origen | Command | Estado destino | Domain Event |
| --- | --- | --- | --- |
| No existe | CreateVoting | Draft | VotingCreated |
| Draft | OpenVoting | Open | VotingOpened |
| Draft | CancelVoting | Cancelled | VotingCancelled |
| Open | CloseVoting | Closed | VotingClosed |
| Closed | ArchiveVoting | Archived | VotingArchived |
| Cancelled | ArchiveVoting | Archived | VotingArchived |

---

# Regla General de Transición

Toda transición debe seguir conceptualmente:

```text
Current VotingStatus

↓

Command

↓

Validate State

↓

Validate Invariants

↓

Apply Transition

↓

Update Lifecycle Information

↓

Increment Version

↓

Generate Domain Event
```

Una transición solamente puede confirmarse cuando todas
las reglas aplicables se cumplen.

---

# Guard

Cada transición debe validar como mínimo que el estado
actual corresponda al estado origen permitido.

Conceptualmente:

```text
Current State

=

Expected Origin State
```

Si no coincide:

```text
Transition Rejected
```

Las condiciones adicionales pertenecientes al dominio se
definen formalmente en:

```text
DOMAIN-009E-Invariants.md
```

---

# CreateVoting

## Estado Origen

```text
No Voting
```

---

## Command

```text
CreateVoting
```

---

## Estado Destino

```text
Draft
```

---

## Evento

```text
VotingCreated
```

---

## Regla

Un Voting solamente puede comenzar su State Machine
mediante su creación válida.

Conceptualmente:

```text
No Voting

↓

CreateVoting

↓

Validate Creation Invariants

↓

Draft
```

---

## Resultado

Una creación válida produce:

```text
VotingStatus = Draft

Version = 1
```

y:

```text
VotingCreated
```

---

# Draft

Draft constituye el estado inicial operativo del
Aggregate.

Desde Draft existen exactamente dos transiciones de
Lifecycle:

```text
Draft → Open
```

y:

```text
Draft → Cancelled
```

No existe transición directa desde Draft hacia:

```text
Closed

Archived
```

---

# Draft → Open

## Estado Origen

```text
Draft
```

---

## Command

```text
OpenVoting
```

---

## Estado Destino

```text
Open
```

---

## Evento

```text
VotingOpened
```

---

## Validación Conceptual

```text
VotingStatus = Draft

↓

OpenVoting

↓

Validate State

Validate Rules

Validate Options

Validate Invariants

↓

VotingStatus = Open
```

La definición exhaustiva de las condiciones de apertura
pertenece a:

```text
DOMAIN-009E-Invariants.md
```

---

## Efectos

Una transición válida:

```text
Draft → Open
```

debe:

- establecer VotingStatus en Open;
- establecer OpenedAt;
- incrementar Version;
- actualizar UpdatedAt;
- generar VotingOpened.

---

# Draft → Cancelled

## Estado Origen

```text
Draft
```

---

## Command

```text
CancelVoting
```

---

## Estado Destino

```text
Cancelled
```

---

## Evento

```text
VotingCancelled
```

---

## Validación Conceptual

```text
VotingStatus = Draft

↓

CancelVoting

↓

Validate State

Validate Invariants

↓

VotingStatus = Cancelled
```

---

## Efectos

Una cancelación válida debe:

- establecer VotingStatus en Cancelled;
- establecer CancelledAt;
- incrementar Version;
- actualizar UpdatedAt;
- generar VotingCancelled.

Cancelar no elimina el Aggregate.

---

# Open

Open representa un proceso de Voting formalmente activo.

Desde Open existe exclusivamente la transición:

```text
Open → Closed
```

La versión 1.0 no define desde Open:

```text
Open → Draft

Open → Cancelled

Open → Archived
```

---

# Open → Closed

## Estado Origen

```text
Open
```

---

## Command

```text
CloseVoting
```

---

## Estado Destino

```text
Closed
```

---

## Evento

```text
VotingClosed
```

---

## Validación Conceptual

```text
VotingStatus = Open

↓

CloseVoting

↓

Validate State

Validate Rules

Validate Result Conditions

Validate Invariants

↓

VotingStatus = Closed
```

Las condiciones completas de cierre se desarrollan en:

```text
DOMAIN-009E-Invariants.md
```

---

## Efectos

Una transición válida:

```text
Open → Closed
```

debe:

- establecer VotingStatus en Closed;
- establecer ClosedAt;
- preservar Result cuando corresponda;
- incrementar Version;
- actualizar UpdatedAt;
- generar VotingClosed.

---

# Closed

Closed representa la finalización formal del flujo normal
de Voting.

Desde Closed existe únicamente:

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

# Closed → Archived

## Estado Origen

```text
Closed
```

---

## Command

```text
ArchiveVoting
```

---

## Estado Destino

```text
Archived
```

---

## Evento

```text
VotingArchived
```

---

## Validación Conceptual

```text
VotingStatus = Closed

↓

ArchiveVoting

↓

Validate State

Validate Invariants

↓

VotingStatus = Archived
```

---

## Efectos

Una transición válida debe:

- establecer VotingStatus en Archived;
- establecer ArchivedAt;
- conservar OpenedAt;
- conservar ClosedAt;
- conservar Result cuando exista;
- incrementar Version;
- actualizar UpdatedAt;
- generar VotingArchived.

---

# Cancelled

Cancelled representa una terminación alternativa del
proceso.

Desde Cancelled existe únicamente:

```text
Cancelled → Archived
```

No existen:

```text
Cancelled → Draft

Cancelled → Open

Cancelled → Closed
```

---

# Cancelled → Archived

## Estado Origen

```text
Cancelled
```

---

## Command

```text
ArchiveVoting
```

---

## Estado Destino

```text
Archived
```

---

## Evento

```text
VotingArchived
```

---

## Validación Conceptual

```text
VotingStatus = Cancelled

↓

ArchiveVoting

↓

Validate State

Validate Invariants

↓

VotingStatus = Archived
```

---

## Efectos

Una transición válida debe:

- establecer VotingStatus en Archived;
- establecer ArchivedAt;
- conservar CancelledAt;
- incrementar Version;
- actualizar UpdatedAt;
- generar VotingArchived.

---

# Archived

Archived representa el estado histórico terminal.

No posee transiciones salientes.

Debe mantenerse:

```text
Archived

↓

No State Transition
```

Cualquier Command que intente producir una transición
desde Archived debe ser rechazado.

---

# Estado Terminal

El único estado terminal es:

```text
Archived
```

No puede evolucionar hacia:

```text
Draft

Open

Closed

Cancelled
```

---

# Matriz de Transiciones Permitidas

| Origen | Destino | Permitida |
| --- | --- | --- |
| No existe | Draft | Sí |
| Draft | Open | Sí |
| Draft | Cancelled | Sí |
| Open | Closed | Sí |
| Closed | Archived | Sí |
| Cancelled | Archived | Sí |

---

# Matriz de Transiciones Rechazadas

| Origen | Destino | Resultado |
| --- | --- | --- |
| Draft | Closed | Rejected |
| Draft | Archived | Rejected |
| Open | Draft | Rejected |
| Open | Cancelled | Rejected |
| Open | Archived | Rejected |
| Closed | Draft | Rejected |
| Closed | Open | Rejected |
| Closed | Cancelled | Rejected |
| Cancelled | Draft | Rejected |
| Cancelled | Open | Rejected |
| Cancelled | Closed | Rejected |
| Archived | Draft | Rejected |
| Archived | Open | Rejected |
| Archived | Closed | Rejected |
| Archived | Cancelled | Rejected |

---

# Representación Matricial

```text
FROM \ TO     Draft     Open     Closed     Cancelled     Archived

No Voting      YES       NO        NO           NO            NO

Draft           -        YES       NO           YES           NO

Open            NO        -        YES          NO            NO

Closed          NO       NO         -           NO            YES

Cancelled       NO       NO        NO            -            YES

Archived        NO       NO        NO           NO             -
```

---

# Commands de Transición

Los Commands que modifican VotingStatus son:

```text
CreateVoting

OpenVoting

CloseVoting

CancelVoting

ArchiveVoting
```

Estos Commands son los únicos Commands de Lifecycle
definidos por la versión 1.0.

La especificación completa pertenece a:

```text
DOMAIN-009C-Commands.md
```

---

# Commands sin Transición

El Aggregate también puede recibir Commands que produzcan
modificaciones válidas sin cambiar VotingStatus.

Entre los Commands conceptualmente definidos por el
Aggregate se encuentran:

```text
ChangeVotingType

ChangeVotingTitle

ChangeVotingDescription

ChangeVotingRules

AddVotingOption

RemoveVotingOption
```

Estos Commands no constituyen por sí mismos transiciones
de State Machine.

Debe mantenerse:

```text
State Before

=

State After
```

cuando la operación sea válida y no exista una transición
de Lifecycle asociada.

La State Machine no determina en este documento en qué
estados puede ejecutarse cada modificación de
configuración.

Esa definición corresponde a:

```text
DOMAIN-009C-Commands.md

DOMAIN-009E-Invariants.md
```

---

# Modificación con Estado Invariable

Conceptualmente:

```text
Draft

↓

ChangeVotingTitle

↓

Draft
```

puede representar una modificación válida sin transición
de Lifecycle cuando las reglas correspondientes lo
permitan.

En ese caso:

```text
VotingStatus
```

permanece igual, mientras:

```text
Version
```

puede incrementarse por existir una modificación válida.

---

# State Machine y Lifecycle

Lifecycle y State Machine representan responsabilidades
complementarias.

Lifecycle define:

```text
Valid Domain States

+

Conceptual Evolution
```

State Machine define:

```text
Allowed State Transitions
```

Debe mantenerse:

```text
DOMAIN-009A-Lifecycle.md

=

DOMAIN-009B-State-Machine.md
```

respecto de estados y transiciones.

---

# State Machine y Commands

Toda transición es provocada por un Command.

Debe mantenerse:

```text
Command

↓

State Machine Validation

↓

Transition
```

No puede existir:

```text
Direct VotingStatus Mutation
```

---

# State Machine y Domain Events

Toda transición válida produce un hecho correspondiente.

Debe mantenerse:

```text
CreateVoting

↓

VotingCreated
```

```text
OpenVoting

↓

VotingOpened
```

```text
CloseVoting

↓

VotingClosed
```

```text
CancelVoting

↓

VotingCancelled
```

```text
ArchiveVoting

↓

VotingArchived
```

Los eventos representan el resultado de una transición ya
ejecutada.

No pueden utilizarse para solicitarla.

---

# Command versus Event

Debe mantenerse:

```text
OpenVoting
```

como intención.

Y:

```text
VotingOpened
```

como hecho.

Igualmente:

```text
CloseVoting
```

es una intención.

Mientras:

```text
VotingClosed
```

es un hecho consumado.

---

# State Machine e Invariants

La existencia de una transición en la State Machine no
significa que pueda ejecutarse sin validar las Invariants.

Debe mantenerse:

```text
Allowed Transition

+

Valid Invariants

=

Executable Transition
```

Por ejemplo:

```text
Draft → Open
```

es una transición reconocida.

Sin embargo, OpenVoting debe rechazarse cuando las
condiciones requeridas para apertura no sean válidas.

---

# State Machine y Permissions

Las Permissions determinan si un actor puede solicitar un
Command.

La State Machine determina si el Command puede provocar la
transición desde el estado actual.

Debe mantenerse:

```text
Permission

≠

State Transition
```

Ejemplo:

```text
Permission to Close

+

VotingStatus = Draft
```

no permite:

```text
Draft → Closed
```

---

# State Machine y Versioning

Cada transición válida modifica el estado observable del
Aggregate.

Por tanto:

```text
Valid State Transition

↓

Version + 1
```

Una transición rechazada mantiene:

```text
Version
```

sin cambios.

---

# State Machine y Timestamps

Los timestamps de Lifecycle deben corresponder a
transiciones concretas.

Debe mantenerse:

```text
Draft → Open

↓

OpenedAt
```

```text
Open → Closed

↓

ClosedAt
```

```text
Draft → Cancelled

↓

CancelledAt
```

```text
Closed → Archived

↓

ArchivedAt
```

```text
Cancelled → Archived

↓

ArchivedAt
```

No pueden establecerse mediante una transición diferente.

---

# Preservación Histórica

Una transición posterior no elimina hechos anteriores.

Ejemplo:

```text
Draft

↓

Open

OpenedAt = T1

↓

Closed

ClosedAt = T2

↓

Archived

ArchivedAt = T3
```

En Archived deben conservarse:

```text
OpenedAt = T1

ClosedAt = T2

ArchivedAt = T3
```

---

# Rechazo de Transición

Cuando una transición sea inválida:

```text
Current State

↓

Invalid Command for State

↓

Rejected
```

El resultado debe preservar:

```text
VotingStatus = Previous VotingStatus

Version = Previous Version

Lifecycle Timestamps = Previous Values
```

No debe producirse el Domain Event correspondiente al
éxito.

---

# Intento de Cierre desde Draft

Estado:

```text
Draft
```

Command:

```text
CloseVoting
```

Resultado:

```text
Rejected
```

Debe permanecer:

```text
VotingStatus = Draft
```

No debe existir:

```text
VotingClosed
```

---

# Intento de Apertura desde Closed

Estado:

```text
Closed
```

Command:

```text
OpenVoting
```

Resultado:

```text
Rejected
```

Debe permanecer:

```text
VotingStatus = Closed
```

No debe existir:

```text
VotingOpened
```

---

# Intento de Reapertura

La versión 1.0 no define:

```text
Closed → Open
```

Por tanto:

```text
OpenVoting
```

sobre un Voting Closed debe ser rechazado.

No existe Command de reapertura dentro del modelo actual.

---

# Intento de Reactivación

La versión 1.0 no define:

```text
Cancelled → Draft
```

ni:

```text
Cancelled → Open
```

No existe Command de reactivación dentro del modelo
actual.

---

# Intento de Desarchivado

La versión 1.0 no define transición desde Archived.

No existe:

```text
Archived → Previous State
```

No existe Command de desarchivado dentro del modelo
actual.

---

# Cancelación desde Open

La versión 1.0 no define:

```text
Open → Cancelled
```

Por tanto:

```text
CancelVoting
```

sobre un Voting Open debe ser rechazado.

La incorporación futura de una interrupción o cancelación
de un Voting ya abierto requeriría una evolución explícita
del modelo.

---

# Archivado desde Draft

La versión 1.0 no define:

```text
Draft → Archived
```

Por tanto:

```text
ArchiveVoting
```

sobre Draft debe ser rechazado.

---

# Archivado desde Open

La versión 1.0 no define:

```text
Open → Archived
```

Por tanto:

```text
ArchiveVoting
```

sobre Open debe ser rechazado.

---

# Repetición de Transición

Una transición ya consumada no puede repetirse como si el
estado anterior todavía existiera.

Ejemplo:

```text
Draft

↓

OpenVoting

↓

Open
```

Un segundo:

```text
OpenVoting
```

no encuentra:

```text
VotingStatus = Draft
```

por lo tanto debe ser rechazado.

---

# Idempotencia Conceptual del Estado

La repetición de un Command de transición no debe crear
una transición inexistente.

Ejemplo:

```text
VotingStatus = Closed
```

seguido de:

```text
CloseVoting
```

no produce:

```text
Closed → Closed
```

como transición válida de Lifecycle.

Debe ser rechazado.

---

# State Machine y Result

Result no constituye un estado adicional.

Debe mantenerse:

```text
Result

≠

VotingStatus
```

La existencia de Result no crea estados como:

```text
Approved

Rejected

Passed

Failed
```

dentro de VotingStatus en la versión 1.0.

El resultado permanece como concepto propio del Voting,
mientras el estado del proceso continúa representado por:

```text
Draft

Open

Closed

Cancelled

Archived
```

---

# State Machine y Otros Aggregates

La State Machine controla exclusivamente:

```text
VotingStatus
```

No controla:

```text
Organization Status

Assembly Status

Proposal Status

Participation Status

Document Status

Notification Status

Audit Status
```

Una transición de Voting no genera una transición directa
en otro Aggregate.

---

# Assembly y State Machine

Assembly puede proporcionar contexto mediante:

```text
AssemblyId
```

Sin embargo:

```text
Assembly State Machine

≠

Voting State Machine
```

Voting no modifica el estado de Assembly durante sus
transiciones.

---

# Proposal y State Machine

Proposal puede estar relacionada mediante:

```text
ProposalId
```

Sin embargo:

```text
VotingClosed
```

no implica dentro de este Aggregate:

```text
Proposal State Transition
```

Proposal conserva su propia State Machine.

---

# Participation y State Machine

Participation puede relacionarse con Voting dentro del
modelo de participación.

Sin embargo:

```text
Voting Open

≠

Participation Active
```

y:

```text
Voting Closed

≠

Participation Completed
```

Las State Machines permanecen independientes.

---

# Consistency Boundary

Toda transición pertenece exclusivamente al Consistency
Boundary de Voting.

Conceptualmente:

```text
Voting

↓

Validate Current State

↓

Validate Invariants

↓

Change VotingStatus

↓

Update Lifecycle Timestamp

↓

Increment Version

↓

Generate Domain Event
```

No forma parte de la transición:

```text
Modify Assembly

Modify Proposal

Modify Participation

Modify Organization
```

---

# Persistencia

Una transición válida debe persistirse como una
modificación coherente del Aggregate.

Conceptualmente:

```text
Previous State

+

New State

+

Lifecycle Timestamp

+

Version

+

Domain Event
```

deben corresponder al mismo cambio lógico.

No debe persistirse únicamente VotingStatus ignorando el
resto de las reglas del Aggregate.

---

# Concurrencia

La State Machine debe evaluarse sobre la versión actual
del Aggregate.

Conceptualmente:

```text
Load Voting

↓

Version N

↓

Validate Transition

↓

Persist Version N + 1
```

Si el Aggregate cambió concurrentemente, el mecanismo de
Versioning debe impedir que una transición calculada sobre
un estado obsoleto sobrescriba el estado actual.

---

# Rehidratación

La rehidratación debe restaurar exactamente el estado
persistido.

Ejemplo:

```text
Persisted VotingStatus = Closed

↓

Rehydrate

↓

VotingStatus = Closed
```

La rehidratación:

- no ejecuta Commands;
- no ejecuta nuevas transiciones;
- no incrementa Version;
- no genera nuevos Domain Events.

---

# Replay

Cuando el Aggregate sea reconstruido desde hechos
históricos, Replay aplica estados ya ocurridos.

Conceptualmente:

```text
VotingCreated

↓

Draft

VotingOpened

↓

Open

VotingClosed

↓

Closed
```

Replay no vuelve a ejecutar:

```text
CreateVoting

OpenVoting

CloseVoting
```

como nuevas intenciones.

---

# Matriz Command / Estado

La matriz de Commands de Lifecycle es:

| Command | Draft | Open | Closed | Cancelled | Archived |
| --- | --- | --- | --- | --- | --- |
| OpenVoting | Permitido | Rechazado | Rechazado | Rechazado | Rechazado |
| CloseVoting | Rechazado | Permitido | Rechazado | Rechazado | Rechazado |
| CancelVoting | Permitido | Rechazado | Rechazado | Rechazado | Rechazado |
| ArchiveVoting | Rechazado | Rechazado | Permitido | Permitido | Rechazado |

`CreateVoting` aplica únicamente cuando el Aggregate todavía no
existe.

---

# Matriz Evento / Transición

| Domain Event | Origen | Destino |
| --- | --- | --- |
| VotingCreated | No existe | Draft |
| VotingOpened | Draft | Open |
| VotingClosed | Open | Closed |
| VotingCancelled | Draft | Cancelled |
| VotingArchived | Closed | Archived |
| VotingArchived | Cancelled | Archived |

---

# Matriz Estado / Timestamp

| Estado alcanzado | Timestamp asociado |
| --- | --- |
| Draft | CreatedAt |
| Open | OpenedAt |
| Closed | ClosedAt |
| Cancelled | CancelledAt |
| Archived | ArchivedAt |

Los timestamps históricos anteriores permanecen
preservados.

---

# Reglas

## REG-001

VotingStatus solo puede contener uno de los estados
oficiales:

```text
Draft

Open

Closed

Cancelled

Archived
```

---

## REG-002

Todo Voting comienza en:

```text
Draft
```

---

## REG-003

VotingStatus no puede modificarse directamente.

---

## REG-004

Toda transición requiere un Command de Lifecycle válido.

---

## REG-005

La transición:

```text
Draft → Open
```

requiere:

```text
OpenVoting
```

---

## REG-006

La transición:

```text
Draft → Cancelled
```

requiere:

```text
CancelVoting
```

---

## REG-007

La transición:

```text
Open → Closed
```

requiere:

```text
CloseVoting
```

---

## REG-008

La transición:

```text
Closed → Archived
```

requiere:

```text
ArchiveVoting
```

---

## REG-009

La transición:

```text
Cancelled → Archived
```

requiere:

```text
ArchiveVoting
```

---

## REG-010

Toda transición no declarada explícitamente debe ser
rechazada.

---

## REG-011

Toda transición válida debe preservar las Invariants.

---

## REG-012

Toda transición válida incrementa Version.

---

## REG-013

Toda transición válida genera el Domain Event
correspondiente.

---

## REG-014

Una transición rechazada no modifica VotingStatus.

---

## REG-015

Una transición rechazada no incrementa Version.

---

## REG-016

Una transición rechazada no genera el Domain Event de
éxito correspondiente.

---

## REG-017

Archived no posee transiciones salientes.

---

## REG-018

Closed no puede volver a Open dentro de la versión 1.0.

---

## REG-019

Cancelled no puede volver a Draft ni Open dentro de la
versión 1.0.

---

## REG-020

Open no puede transicionar a Cancelled dentro de la
versión 1.0.

---

## REG-021

Los Commands que modifican configuración no introducen por
sí mismos nuevas transiciones de Lifecycle.

---

## REG-022

Result no constituye un VotingStatus.

---

## REG-023

La State Machine de Voting no puede modificar directamente
el estado de otro Aggregate.

---

## REG-024

Ninguna transición adicional puede incorporarse sin una
evolución explícita del modelo de dominio.

---

# Restricciones

No está permitido:

- asignar VotingStatus directamente;
- crear Voting directamente en Open;
- crear Voting directamente en Closed;
- crear Voting directamente en Cancelled;
- crear Voting directamente en Archived;
- ejecutar Draft → Closed;
- ejecutar Draft → Archived;
- ejecutar Open → Draft;
- ejecutar Open → Cancelled;
- ejecutar Open → Archived;
- ejecutar Closed → Draft;
- ejecutar Closed → Open;
- ejecutar Closed → Cancelled;
- ejecutar Cancelled → Draft;
- ejecutar Cancelled → Open;
- ejecutar Cancelled → Closed;
- ejecutar cualquier transición desde Archived;
- utilizar un Command de configuración para cambiar
  VotingStatus;
- utilizar Permissions para evitar la State Machine;
- utilizar Repository para modificar VotingStatus;
- utilizar Metadata para modificar VotingStatus;
- interpretar Result como un estado;
- crear estados derivados del resultado dentro de
  VotingStatus;
- modificar timestamps históricos arbitrariamente;
- ejecutar una transición sobre una versión obsoleta como
  si fuera actual;
- modificar otro Aggregate durante una transición interna;
- introducir reapertura sin evolución explícita;
- introducir reactivación sin evolución explícita;
- introducir desarchivado sin evolución explícita;
- introducir cancelación desde Open sin evolución
  explícita.

---

# Compatibilidad con Lifecycle

La State Machine implementa exactamente:

```text
DOMAIN-009A-Lifecycle.md
```

Debe mantenerse permanentemente:

```text
Lifecycle State Set

=

State Machine State Set
```

y:

```text
Lifecycle Transition Set

=

State Machine Transition Set
```

Una modificación futura de estados o transiciones requiere
actualizar ambos documentos de forma coherente.

---

# Compatibilidad con Commands

La State Machine recibe las intenciones definidas en:

```text
DOMAIN-009C-Commands.md
```

Un Command de Lifecycle solo puede cambiar estado si la
transición correspondiente está permitida.

---

# Compatibilidad con Domain Events

Una transición confirmada produce el Domain Event definido
en:

```text
DOMAIN-009D-Domain-Events.md
```

Debe mantenerse la correspondencia:

```text
Command

↓

Transition

↓

Domain Event
```

---

# Compatibilidad con Invariants

La State Machine no reemplaza las Invariants.

Debe mantenerse:

```text
Valid Transition

+

Valid Invariants

=

Valid State Change
```

Las reglas exhaustivas pertenecen a:

```text
DOMAIN-009E-Invariants.md
```

---

# Compatibilidad con Versioning

Toda transición confirmada representa una modificación
válida.

Por tanto:

```text
State N

Version X

↓

Valid Transition

↓

State N+1

Version X+1
```

El modelo de Versioning se define en:

```text
DOMAIN-009I-Versioning.md
```

---

# Compatibilidad con Event Sourcing

La State Machine puede reconstruirse mediante la secuencia
de Domain Events.

Flujo normal:

```text
VotingCreated

↓

Draft

VotingOpened

↓

Open

VotingClosed

↓

Closed

VotingArchived

↓

Archived
```

Flujo cancelado:

```text
VotingCreated

↓

Draft

VotingCancelled

↓

Cancelled

VotingArchived

↓

Archived
```

Los eventos históricos no crean transiciones adicionales.

---

# Compatibilidad con CQRS

La State Machine pertenece al Write Side.

Conceptualmente:

```text
Command

↓

Voting Aggregate

↓

State Machine

↓

Domain Event
```

El Read Side puede observar:

```text
VotingStatus
```

mediante proyecciones.

No puede modificarlo.

---

# Definición de Éxito

La State Machine del Aggregate **Voting** formaliza
exactamente la evolución definida por
`DOMAIN-009A-Lifecycle.md`.

La versión 1.0 reconoce los estados:

```text
Draft

Open

Closed

Cancelled

Archived
```

y exclusivamente las transiciones:

```text
No Voting → Draft

Draft → Open

Draft → Cancelled

Open → Closed

Closed → Archived

Cancelled → Archived
```

Cada transición:

- es iniciada mediante un Command explícito;
- valida el estado origen;
- preserva las Invariants;
- mantiene coherencia temporal;
- incrementa Version;
- genera el Domain Event correspondiente;
- permanece dentro del Consistency Boundary de Voting.

Las transiciones no declaradas son rechazadas.

La State Machine impide reaperturas, reactivaciones,
desarchivados, cancelación desde Open y cualquier otro
cambio de estado no definido por el modelo actual.

VotingStatus permanece protegido exclusivamente por la
Aggregate Root y nunca puede ser utilizado para modificar
directamente los estados de Organization, Citizen,
Membership, Role, Territory, Assembly, Proposal,
Participation, Document, Notification, Audit o
Integration.

De esta forma, `DOMAIN-009B-State-Machine.md` establece el
modelo oficial y determinista de transiciones de estado del
Aggregate **Voting**, manteniendo íntegramente las reglas
conceptuales consolidadas de AURA Core.