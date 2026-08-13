# DOMAIN-009A — Voting Lifecycle

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
- DOMAIN-009B-State-Machine.md
- DOMAIN-009C-Commands.md
- DOMAIN-009D-Domain-Events.md
- DOMAIN-009E-Invariants.md
- DOMAIN-009F-Permissions.md
- DOMAIN-009I-Versioning.md
- DOMAIN-009J-Consistency-Boundary.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Definir el Lifecycle oficial del Aggregate **Voting**.

El Lifecycle establece los estados válidos que puede
alcanzar un proceso de Voting durante su existencia y las
transiciones conceptuales permitidas entre dichos estados.

El Lifecycle protege la evolución temporal del Aggregate y
garantiza que Voting no pueda modificar arbitrariamente su
estado.

Toda transición debe:

- partir de un estado válido;
- alcanzar un estado válido;
- ser ejecutada por comportamiento del Aggregate;
- respetar las Invariants;
- respetar la State Machine;
- respetar las Permissions correspondientes;
- incrementar Version cuando produce una modificación
  válida;
- generar el Domain Event correspondiente.

El Lifecycle definido en este documento desarrolla
exclusivamente los estados y transiciones establecidos por
`DOMAIN-009-Aggregate.md`.

No introduce estados ni rutas adicionales.

---

# Principios

El Lifecycle de Voting cumple los siguientes principios:

- Voting posee un único estado actual;
- todo Voting comienza en Draft;
- el estado solo cambia mediante comportamiento explícito
  del Aggregate;
- las transiciones no pueden ejecutarse directamente;
- toda transición debe encontrarse definida por el modelo;
- una transición inválida debe rechazarse;
- una transición rechazada no modifica el estado;
- una transición rechazada no incrementa Version;
- una transición rechazada no genera un Domain Event de
  éxito;
- Closed representa la finalización formal del flujo normal;
- Cancelled representa una terminación alternativa;
- Archived representa conservación histórica;
- Archived es terminal;
- el Lifecycle de Voting es independiente de los
  Lifecycles de otros Aggregates.

---

# Estado del Aggregate

El estado del Lifecycle se representa conceptualmente
mediante:

```text
VotingStatus
```

Los estados oficiales de la versión 1.0 son:

```text
Draft

Open

Closed

Cancelled

Archived
```

No existen otros estados dentro de esta versión del modelo.

---

# Estado Inicial

Todo Voting válido comienza en:

```text
Draft
```

Conceptualmente:

```text
No Voting

    │

    │ CreateVoting

    ▼

  Draft
```

La creación produce:

```text
VotingCreated
```

y establece la primera versión válida del Aggregate.

---

# Flujo Principal

El flujo principal del Lifecycle es:

```text
Draft
  │
  │ OpenVoting
  ▼
Open
  │
  │ CloseVoting
  ▼
Closed
  │
  │ ArchiveVoting
  ▼
Archived
```

Este flujo representa:

```text
Configuration

↓

Execution

↓

Formal Closure

↓

Historical Preservation
```

---

# Ruta de Cancelación

La versión 1.0 mantiene la ruta de cancelación establecida
por el modelo:

```text
Draft
  │
  │ CancelVoting
  ▼
Cancelled
  │
  │ ArchiveVoting
  ▼
Archived
```

La cancelación representa una terminación alternativa del
proceso antes de su apertura.

No constituye eliminación del Aggregate.

---

# Modelo Conceptual Completo

El Lifecycle completo de la versión 1.0 es:

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

# Draft

## Definición

Draft representa un Voting creado formalmente que todavía
no ha sido abierto.

Conceptualmente:

```text
Voting exists

+

VotingStatus = Draft
```

En Draft el proceso existe dentro del dominio, pero todavía
no se encuentra activo para su ejecución.

---

## Entrada a Draft

Draft se alcanza únicamente mediante:

```text
CreateVoting
```

desde:

```text
No Voting
```

Resultado:

```text
VotingStatus = Draft
```

Evento:

```text
VotingCreated
```

---

## Responsabilidad de Draft

Draft representa la fase en la cual Voting mantiene la
configuración necesaria antes de su apertura.

El Aggregate puede proteger durante esta fase los
elementos ya establecidos por su modelo:

```text
VotingType

Title

Description

Rules

Options

AssemblyId

ProposalId
```

cuando correspondan.

Las modificaciones concretas permitidas permanecen
definidas mediante Commands, State Machine e Invariants.

---

## Salidas Permitidas

Desde Draft existen únicamente las siguientes transiciones
de Lifecycle:

```text
Draft

↓

Open
```

y:

```text
Draft

↓

Cancelled
```

---

## Permanencia en Draft

No toda modificación válida implica una transición de
Lifecycle.

Por ejemplo, cuando el estado y las reglas correspondientes
lo permitan:

```text
Draft

↓

Configuration Change

↓

Draft
```

El Voting permanece en Draft aunque su estado interno haya
cambiado válidamente.

Una modificación de configuración válida:

- puede incrementar Version;
- puede actualizar UpdatedAt;
- puede generar un Domain Event;
- no cambia necesariamente VotingStatus.

---

# Open

## Definición

Open representa un Voting formalmente abierto.

Conceptualmente:

```text
VotingStatus = Open
```

significa que el proceso de Voting ha comenzado
formalmente.

---

## Entrada a Open

Open se alcanza mediante:

```text
OpenVoting
```

desde:

```text
Draft
```

La transición conceptual es:

```text
Draft

↓

OpenVoting

↓

Open
```

Evento:

```text
VotingOpened
```

---

## Condiciones de Entrada

La transición hacia Open debe validar las condiciones
definidas por el Aggregate.

Conceptualmente:

```text
Draft

↓

OpenVoting

↓

Validate VotingStatus

Validate VotingType

Validate Rules

Validate Options

Validate Invariants

↓

Open
```

Las condiciones exhaustivas pertenecen a:

```text
DOMAIN-009E-Invariants.md
```

---

## Efectos de Entrada

Una apertura válida:

- establece VotingStatus en Open;
- establece OpenedAt;
- incrementa Version;
- actualiza UpdatedAt;
- genera VotingOpened.

Conceptualmente:

```text
VotingStatus = Draft

OpenedAt = null

Version = N
```

después de una apertura válida:

```text
VotingStatus = Open

OpenedAt = T1

Version = N + 1
```

---

## Significado

Open significa:

```text
Formal Voting Process Active
```

No significa:

```text
Assembly Open
```

ni:

```text
Proposal Approved
```

ni:

```text
Participation Completed
```

Cada Aggregate mantiene su propio Lifecycle.

---

## Salida Permitida

Desde Open la transición de Lifecycle definida para la
versión 1.0 es:

```text
Open

↓

Closed
```

mediante:

```text
CloseVoting
```

---

# Closed

## Definición

Closed representa la finalización formal del proceso normal
de Voting.

Conceptualmente:

```text
VotingStatus = Closed
```

indica que el proceso ya no se encuentra abierto.

---

## Entrada a Closed

Closed se alcanza mediante:

```text
CloseVoting
```

desde:

```text
Open
```

La transición es:

```text
Open

↓

CloseVoting

↓

Closed
```

Evento:

```text
VotingClosed
```

---

## Condiciones de Entrada

El cierre debe respetar las Invariants correspondientes.

Conceptualmente:

```text
Open

↓

CloseVoting

↓

Validate VotingStatus

Validate Rules

Validate Result Conditions

Validate Invariants

↓

Closed
```

La definición exhaustiva pertenece a:

```text
DOMAIN-009E-Invariants.md
```

---

## Efectos de Entrada

Un cierre válido:

- establece VotingStatus en Closed;
- establece ClosedAt;
- preserva el resultado formal cuando corresponda;
- incrementa Version;
- actualiza UpdatedAt;
- genera VotingClosed.

Conceptualmente:

```text
VotingStatus = Open

OpenedAt = T1

ClosedAt = null

Version = N
```

después del cierre:

```text
VotingStatus = Closed

OpenedAt = T1

ClosedAt = T2

Version = N + 1
```

Debe mantenerse:

```text
T2 >= T1
```

---

## Naturaleza de Closed

Closed representa un hecho del dominio.

Un Voting Closed:

- conserva VotingId;
- conserva OrganizationId;
- conserva su contexto;
- conserva su configuración histórica;
- conserva OpenedAt;
- conserva ClosedAt;
- conserva Result cuando corresponda;
- conserva Version;
- conserva Domain Events históricos.

Cerrar no significa archivar.

Debe mantenerse:

```text
Closed

≠

Archived
```

---

## Salida Permitida

Desde Closed la transición definida es:

```text
Closed

↓

Archived
```

mediante:

```text
ArchiveVoting
```

---

## Restricción

La versión 1.0 no define:

```text
Closed

↓

Open
```

Un Voting formalmente cerrado no vuelve al estado Open
mediante una operación ordinaria.

---

# Cancelled

## Definición

Cancelled representa la terminación alternativa de un
Voting antes de su apertura.

Conceptualmente:

```text
VotingStatus = Cancelled
```

indica que el proceso fue cancelado sin recorrer el flujo
normal:

```text
Draft

↓

Open

↓

Closed
```

---

## Entrada a Cancelled

La versión 1.0 define:

```text
Draft

↓

CancelVoting

↓

Cancelled
```

Evento:

```text
VotingCancelled
```

---

## Efectos de Entrada

Una cancelación válida:

- establece VotingStatus en Cancelled;
- establece CancelledAt;
- conserva VotingId;
- conserva OrganizationId;
- conserva la configuración histórica;
- incrementa Version;
- actualiza UpdatedAt;
- genera VotingCancelled.

Conceptualmente:

```text
VotingStatus = Draft

CancelledAt = null

Version = N
```

después de cancelar:

```text
VotingStatus = Cancelled

CancelledAt = T1

Version = N + 1
```

---

## Significado

Cancelled no significa:

```text
Deleted
```

Tampoco significa:

```text
Archived
```

La identidad del proceso permanece.

Su historial también permanece.

---

## Salida Permitida

Desde Cancelled la transición definida es:

```text
Cancelled

↓

Archived
```

mediante:

```text
ArchiveVoting
```

---

## Restricción

La versión 1.0 no define:

```text
Cancelled

↓

Draft
```

ni:

```text
Cancelled

↓

Open
```

La reanudación de un Voting cancelado no forma parte del
Lifecycle establecido.

Una capacidad de ese tipo requeriría una evolución
explícita del modelo de dominio.

---

# Archived

## Definición

Archived representa el estado histórico terminal de
Voting.

Conceptualmente:

```text
VotingStatus = Archived
```

significa que el Aggregate ha sido retirado del ciclo
operativo y se conserva como parte del historial del
dominio.

---

## Entradas Permitidas

Archived puede alcanzarse desde:

```text
Closed
```

o:

```text
Cancelled
```

mediante:

```text
ArchiveVoting
```

Conceptualmente:

```text
Closed

↓

ArchiveVoting

↓

Archived
```

y:

```text
Cancelled

↓

ArchiveVoting

↓

Archived
```

Evento:

```text
VotingArchived
```

---

## Efectos de Entrada

Un archivado válido:

- establece VotingStatus en Archived;
- establece ArchivedAt;
- conserva VotingId;
- conserva OrganizationId;
- conserva el contexto histórico;
- conserva Rules;
- conserva Options;
- conserva Result cuando exista;
- conserva timestamps anteriores;
- incrementa Version;
- actualiza UpdatedAt;
- genera VotingArchived.

---

## Estado Terminal

Archived es terminal.

Debe mantenerse:

```text
Archived

↓

No Lifecycle Transition
```

No existe en la versión 1.0:

```text
Archived → Draft

Archived → Open

Archived → Closed

Archived → Cancelled
```

---

## Archivado no es Eliminación

Debe mantenerse:

```text
ArchiveVoting

≠

DeleteVoting
```

El Aggregate conserva su identidad y trazabilidad.

Voting puede continuar siendo referenciado históricamente
y consultado mediante Read Models.

---

# Transiciones Oficiales

Las transiciones oficiales del Lifecycle versión 1.0 son:

| Estado origen | Command | Estado destino | Domain Event |
| --- | --- | --- | --- |
| No existe | CreateVoting | Draft | VotingCreated |
| Draft | OpenVoting | Open | VotingOpened |
| Draft | CancelVoting | Cancelled | VotingCancelled |
| Open | CloseVoting | Closed | VotingClosed |
| Closed | ArchiveVoting | Archived | VotingArchived |
| Cancelled | ArchiveVoting | Archived | VotingArchived |

No existen otras transiciones oficiales en esta versión.

---

# Flujo de Creación

Conceptualmente:

```text
CreateVoting

↓

Validate Creation Invariants

↓

Voting

Status = Draft

Version = 1

↓

VotingCreated
```

La creación válida establece el inicio del Lifecycle.

---

# Flujo de Apertura

Conceptualmente:

```text
Voting

Status = Draft

↓

OpenVoting

↓

Validate State

Validate Rules

Validate Invariants

↓

Status = Open

OpenedAt = T1

Version = N + 1

↓

VotingOpened
```

---

# Flujo de Cierre

Conceptualmente:

```text
Voting

Status = Open

↓

CloseVoting

↓

Validate State

Validate Rules

Validate Invariants

↓

Status = Closed

ClosedAt = T2

Version = N + 1

↓

VotingClosed
```

---

# Flujo de Cancelación

Conceptualmente:

```text
Voting

Status = Draft

↓

CancelVoting

↓

Validate State

Validate Invariants

↓

Status = Cancelled

CancelledAt = T1

Version = N + 1

↓

VotingCancelled
```

---

# Flujo de Archivado desde Closed

Conceptualmente:

```text
Voting

Status = Closed

↓

ArchiveVoting

↓

Validate State

Validate Invariants

↓

Status = Archived

ArchivedAt = T3

Version = N + 1

↓

VotingArchived
```

---

# Flujo de Archivado desde Cancelled

Conceptualmente:

```text
Voting

Status = Cancelled

↓

ArchiveVoting

↓

Validate State

Validate Invariants

↓

Status = Archived

ArchivedAt = T2

Version = N + 1

↓

VotingArchived
```

---

# Transiciones No Permitidas

Toda transición que no aparezca en la tabla oficial debe
ser rechazada.

Entre otras:

```text
Draft → Closed

Draft → Archived

Open → Draft

Open → Archived

Closed → Draft

Closed → Open

Closed → Cancelled

Cancelled → Draft

Cancelled → Open

Cancelled → Closed

Archived → Draft

Archived → Open

Archived → Closed

Archived → Cancelled
```

Estas rutas no forman parte del Lifecycle versión 1.0.

---

# Regla de Transición

Debe cumplirse:

```text
Current State

+

Valid Command

+

Permission

+

State Machine

+

Invariants

=

Valid Transition
```

La existencia del Command no garantiza por sí sola la
transición.

---

# Transición Inválida

Cuando una transición no está permitida:

```text
Command

↓

Rejected
```

El Aggregate debe conservar:

```text
Previous VotingStatus

Previous Version

Previous Lifecycle Timestamps
```

No debe generarse el Domain Event que represente éxito.

---

# Modificaciones sin Cambio de Estado

No toda modificación válida produce una transición de
Lifecycle.

Conceptualmente puede existir:

```text
Draft

↓

ChangeVotingTitle

↓

Draft
```

o:

```text
Draft

↓

ChangeVotingRules

↓

Draft
```

cuando las reglas correspondientes permitan la operación.

En estos casos:

```text
VotingStatus
```

permanece sin cambios.

Sin embargo, una modificación válida puede:

- cambiar estado interno;
- incrementar Version;
- actualizar UpdatedAt;
- generar el Domain Event correspondiente.

Lifecycle y Versioning son conceptos relacionados pero no
equivalentes.

---

# Lifecycle y Commands

Los Commands que producen transiciones del Lifecycle son:

```text
CreateVoting

OpenVoting

CloseVoting

CancelVoting

ArchiveVoting
```

La especificación completa de Commands pertenece a:

```text
DOMAIN-009C-Commands.md
```

Los Commands de configuración no modifican el Lifecycle
salvo que una regla explícita del dominio lo establezca.

---

# Lifecycle y Domain Events

Cada transición válida genera el Domain Event
correspondiente.

La relación oficial es:

```text
CreateVoting

↓

VotingCreated

↓

Draft
```

```text
OpenVoting

↓

VotingOpened

↓

Open
```

```text
CloseVoting

↓

VotingClosed

↓

Closed
```

```text
CancelVoting

↓

VotingCancelled

↓

Cancelled
```

```text
ArchiveVoting

↓

VotingArchived

↓

Archived
```

Los Domain Events completos se especifican en:

```text
DOMAIN-009D-Domain-Events.md
```

---

# Lifecycle y State Machine

El Lifecycle define los estados y evolución conceptual.

La State Machine formaliza las transiciones permitidas.

Debe mantenerse:

```text
Lifecycle

↓

DOMAIN-009A-Lifecycle.md
```

y:

```text
State Transition Rules

↓

DOMAIN-009B-State-Machine.md
```

Ambos documentos deben permanecer consistentes.

La State Machine no puede introducir un estado inexistente
en el Lifecycle.

---

# Lifecycle e Invariants

Toda transición debe preservar las Invariants del
Aggregate.

Conceptualmente:

```text
Current State

↓

Command

↓

Validate Invariants

↓

Transition

↓

New Valid State
```

No puede existir:

```text
Transition

↓

Invalid Aggregate
```

Las reglas exhaustivas pertenecen a:

```text
DOMAIN-009E-Invariants.md
```

---

# Lifecycle y Permissions

Las Permissions determinan quién puede solicitar una
transición.

No determinan si la transición es válida para el estado
actual.

Debe mantenerse:

```text
Permission Granted

≠

Lifecycle Transition Guaranteed
```

Ejemplo:

```text
Permission to Close Voting

+

VotingStatus = Draft

=

Rejected
```

porque el Lifecycle no permite:

```text
Draft → Closed
```

La definición formal de Permissions pertenece a:

```text
DOMAIN-009F-Permissions.md
```

---

# Lifecycle y Versioning

Toda transición válida modifica el estado observable del
Aggregate.

Por lo tanto:

```text
Valid Lifecycle Transition

↓

Version + 1
```

Ejemplo:

```text
Draft

Version = 3

↓

OpenVoting

↓

Open

Version = 4
```

Una transición rechazada mantiene:

```text
Version = 3
```

Las reglas completas pertenecen a:

```text
DOMAIN-009I-Versioning.md
```

---

# Lifecycle y Timestamps

Los timestamps representan hechos ocurridos dentro del
Lifecycle.

Debe mantenerse la relación:

```text
VotingCreated

↓

CreatedAt
```

```text
VotingOpened

↓

OpenedAt
```

```text
VotingClosed

↓

ClosedAt
```

```text
VotingCancelled

↓

CancelledAt
```

```text
VotingArchived

↓

ArchivedAt
```

Los timestamps históricos no deben eliminarse por
transiciones posteriores.

---

# Preservación Temporal

Una transición posterior conserva los timestamps
anteriores que representen hechos válidos.

Ejemplo:

```text
CreatedAt = T1

OpenedAt = T2

ClosedAt = T3
```

al archivar:

```text
CreatedAt = T1

OpenedAt = T2

ClosedAt = T3

ArchivedAt = T4
```

Debe preservarse la secuencia histórica.

---

# Coherencia Temporal

Cuando existan los timestamps correspondientes, debe
mantenerse coherencia temporal.

Para el flujo normal:

```text
CreatedAt <= OpenedAt <= ClosedAt <= ArchivedAt
```

Para el flujo cancelado:

```text
CreatedAt <= CancelledAt <= ArchivedAt
```

Las reglas temporales exhaustivas pertenecen a las
Invariants.

---

# Lifecycle y Result

Result pertenece al proceso formal de Voting.

El Lifecycle determina cuándo puede existir un resultado
formal válido.

Debe mantenerse:

```text
VotingStatus

+

Rules

+

Result Conditions

↓

Valid Result
```

El Lifecycle no convierte Result en una autoridad sobre
otros Aggregates.

El resultado de Voting no modifica directamente:

```text
Proposal

Assembly

Participation

Organization
```

---

# Lifecycle y Otros Aggregates

El Lifecycle de Voting es independiente de:

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

Una transición de Voting no implica automáticamente una
transición en otro Aggregate.

Ejemplo:

```text
Voting

Open → Closed
```

no implica:

```text
Proposal

Automatic State Change
```

ni:

```text
Assembly

Automatic State Change
```

ni:

```text
Participation

Automatic State Change
```

Cada Aggregate mantiene su propia autoridad.

---

# Lifecycle y Consistency Boundary

Todas las transiciones de Voting ocurren dentro de su
propio Consistency Boundary.

Conceptualmente:

```text
Voting

↓

Validate Transition

↓

Validate Invariants

↓

Change State

↓

Increment Version

↓

Generate Domain Event
```

No debe incluirse dentro de la misma modificación interna:

```text
Modify Assembly

Modify Proposal

Modify Participation
```

La definición formal del límite pertenece a:

```text
DOMAIN-009J-Consistency-Boundary.md
```

---

# Estado Terminal

El único estado terminal del Lifecycle versión 1.0 es:

```text
Archived
```

Una vez alcanzado:

```text
Archived
```

no existe transición posterior.

Debe mantenerse:

```text
Archived

↓

Historical State
```

---

# Closed no es Terminal Histórico

Closed representa el término formal del flujo normal, pero
puede evolucionar hacia:

```text
Archived
```

Por lo tanto:

```text
Closed

≠

Terminal Historical State
```

---

# Cancelled no es Terminal Histórico

Cancelled representa una terminación alternativa, pero
puede evolucionar hacia:

```text
Archived
```

Por lo tanto:

```text
Cancelled

≠

Archived
```

---

# Eliminación

El Lifecycle versión 1.0 no utiliza eliminación física
como transición de dominio.

No existe:

```text
Archived

↓

Deleted
```

dentro del Lifecycle definido.

La preservación histórica se representa mediante:

```text
Archived
```

---

# Reapertura

La versión 1.0 no contempla reapertura de un Voting
Closed.

No existe:

```text
Closed

↓

Open
```

La incorporación futura de una capacidad de reapertura
requeriría una evolución explícita del modelo y no puede
inferirse desde este Lifecycle.

---

# Reactivación

La versión 1.0 no contempla reactivación de un Voting
Cancelled.

No existe:

```text
Cancelled

↓

Draft
```

ni:

```text
Cancelled

↓

Open
```

Una capacidad de reactivación requeriría una evolución
explícita del dominio.

---

# Desarchivado

La versión 1.0 no contempla desarchivado.

No existe:

```text
Archived

↓

Previous State
```

Archived permanece terminal.

---

# Matriz de Estados

| Estado | Operativo | Puede recibir transición de Lifecycle | Histórico terminal |
| --- | --- | --- | --- |
| Draft | Sí | Sí | No |
| Open | Sí | Sí | No |
| Closed | No | Sí, hacia Archived | No |
| Cancelled | No | Sí, hacia Archived | No |
| Archived | No | No | Sí |

---

# Matriz de Transiciones

| Origen | Destino | Permitida |
| --- | --- | --- |
| No existe | Draft | Sí |
| Draft | Open | Sí |
| Draft | Cancelled | Sí |
| Open | Closed | Sí |
| Closed | Archived | Sí |
| Cancelled | Archived | Sí |
| Draft | Closed | No |
| Draft | Archived | No |
| Open | Draft | No |
| Open | Archived | No |
| Closed | Draft | No |
| Closed | Open | No |
| Closed | Cancelled | No |
| Cancelled | Draft | No |
| Cancelled | Open | No |
| Cancelled | Closed | No |
| Archived | Draft | No |
| Archived | Open | No |
| Archived | Closed | No |
| Archived | Cancelled | No |

---

# Matriz de Commands de Lifecycle

| Command | Estado origen | Estado destino |
| --- | --- | --- |
| CreateVoting | No existe | Draft |
| OpenVoting | Draft | Open |
| CloseVoting | Open | Closed |
| CancelVoting | Draft | Cancelled |
| ArchiveVoting | Closed | Archived |
| ArchiveVoting | Cancelled | Archived |

---

# Matriz de Domain Events de Lifecycle

| Domain Event | Estado previo | Estado resultante |
| --- | --- | --- |
| VotingCreated | No existe | Draft |
| VotingOpened | Draft | Open |
| VotingClosed | Open | Closed |
| VotingCancelled | Draft | Cancelled |
| VotingArchived | Closed | Archived |
| VotingArchived | Cancelled | Archived |

---

# Reglas

## REG-001

Todo Voting válido comienza en estado:

```text
Draft
```

---

## REG-002

VotingStatus solo puede cambiar mediante una transición
oficial del Lifecycle.

---

## REG-003

La transición:

```text
Draft → Open
```

solo puede producirse mediante:

```text
OpenVoting
```

---

## REG-004

La transición:

```text
Open → Closed
```

solo puede producirse mediante:

```text
CloseVoting
```

---

## REG-005

La transición de cancelación definida para la versión 1.0
es:

```text
Draft → Cancelled
```

mediante:

```text
CancelVoting
```

---

## REG-006

Closed puede evolucionar únicamente hacia:

```text
Archived
```

dentro del Lifecycle versión 1.0.

---

## REG-007

Cancelled puede evolucionar únicamente hacia:

```text
Archived
```

dentro del Lifecycle versión 1.0.

---

## REG-008

Archived es un estado terminal.

---

## REG-009

Toda transición válida debe preservar las Invariants del
Aggregate.

---

## REG-010

Toda transición válida debe incrementar Version.

---

## REG-011

Toda transición válida debe producir el Domain Event
correspondiente.

---

## REG-012

Una transición inválida no modifica VotingStatus.

---

## REG-013

Una transición inválida no incrementa Version.

---

## REG-014

Una transición inválida no genera el Domain Event de éxito
correspondiente.

---

## REG-015

Los timestamps históricos del Lifecycle no pueden
reescribirse arbitrariamente.

---

## REG-016

El Lifecycle de Voting no modifica directamente el
Lifecycle de ningún otro Aggregate.

---

## REG-017

Cerrar un Voting no equivale a archivarlo.

---

## REG-018

Cancelar un Voting no equivale a eliminarlo.

---

## REG-019

Archivar un Voting no equivale a eliminar físicamente el
Aggregate.

---

## REG-020

Ninguna transición adicional puede incorporarse sin una
evolución explícita del modelo de dominio.

---

# Restricciones

No está permitido:

- modificar VotingStatus directamente;
- crear estados adicionales de forma implícita;
- saltar estados mediante operaciones no definidas;
- ejecutar Draft → Closed;
- ejecutar Draft → Archived;
- ejecutar Open → Draft;
- ejecutar Open → Archived;
- ejecutar Closed → Open;
- ejecutar Closed → Cancelled;
- ejecutar Cancelled → Draft;
- ejecutar Cancelled → Open;
- ejecutar Archived → cualquier otro estado;
- utilizar Permissions para evitar el Lifecycle;
- utilizar Metadata o configuración para modificar
  VotingStatus;
- utilizar Repository para evitar la State Machine;
- modificar Version directamente durante una transición;
- reescribir timestamps históricos;
- modificar otro Aggregate como efecto interno de una
  transición;
- interpretar Closed como Archived;
- interpretar Cancelled como eliminación;
- interpretar Archived como eliminación física;
- introducir reapertura sin evolución explícita;
- introducir reactivación sin evolución explícita;
- introducir desarchivado sin evolución explícita.

---

# Compatibilidad con State Machine

La State Machine debe implementar exactamente las
transiciones definidas por este Lifecycle.

Debe mantenerse:

```text
Lifecycle States

=

State Machine States
```

y:

```text
Lifecycle Transitions

=

Allowed State Machine Transitions
```

La especificación formal se desarrolla en:

```text
DOMAIN-009B-State-Machine.md
```

---

# Compatibilidad con Domain Events

Cada transición debe mantener correspondencia semántica
con el hecho producido.

Conceptualmente:

```text
Intent

↓

Valid Transition

↓

Fact
```

Ejemplo:

```text
OpenVoting

↓

Draft → Open

↓

VotingOpened
```

Command, transición y Domain Event deben permanecer
semánticamente alineados.

---

# Compatibilidad con Event Sourcing

El Lifecycle puede reconstruirse conceptualmente mediante
la secuencia histórica de Domain Events.

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

Replay no ejecuta nuevamente las transiciones como nuevas
intenciones.

Los eventos históricos representan hechos ya ocurridos.

---

# Compatibilidad con CQRS

El Write Side mantiene el Lifecycle oficial:

```text
Command

↓

Voting Aggregate

↓

Lifecycle Transition

↓

Domain Event
```

El Read Side puede proyectar el estado resultante:

```text
Domain Event

↓

Projection

↓

VotingStatus View
```

El Read Model no modifica el Lifecycle.

---

# Trazabilidad

El Lifecycle debe permitir reconstruir:

- cuándo nació Voting;
- cuándo fue abierto;
- cuándo fue cerrado;
- cuándo fue cancelado;
- cuándo fue archivado;
- qué estado existía antes de cada transición;
- qué Domain Event representó cada cambio;
- qué Version correspondió a cada modificación.

Conceptualmente:

```text
VotingId

↓

Lifecycle State

↓

Domain Event

↓

AggregateVersion
```

---

# Definición de Éxito

El Lifecycle del Aggregate **Voting** define una evolución
explícita, finita y protegida del proceso formal de
votación.

La versión 1.0 mantiene exclusivamente los estados:

```text
Draft

Open

Closed

Cancelled

Archived
```

y las transiciones:

```text
No Voting → Draft

Draft → Open

Draft → Cancelled

Open → Closed

Closed → Archived

Cancelled → Archived
```

Cada transición:

- ocurre mediante comportamiento explícito del Aggregate;
- respeta la State Machine;
- preserva las Invariants;
- respeta las Permissions correspondientes;
- mantiene coherencia temporal;
- incrementa Version;
- genera el Domain Event correspondiente;
- permanece dentro del Consistency Boundary de Voting.

El modelo impide transiciones arbitrarias, reaperturas,
reactivaciones o desarchivados no definidos y mantiene
separados los Lifecycles de Organization, Citizen,
Membership, Role, Territory, Assembly, Proposal,
Participation, Document, Notification, Audit e
Integration.

De esta forma, `DOMAIN-009A-Lifecycle.md` establece el
ciclo de vida oficial de **Voting** sin ampliar ni alterar
las decisiones conceptuales definidas por el Aggregate
`DOMAIN-009`.
````
