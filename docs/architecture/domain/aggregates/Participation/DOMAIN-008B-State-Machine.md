# DOMAIN-008B — Participation State Machine

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Participation Management

Aggregate:
Participation

Autor:
ARADA

Documentos relacionados:

- DOMAIN-008-Aggregate.md
- DOMAIN-008A-Lifecycle.md
- DOMAIN-008C-Commands.md
- DOMAIN-008D-Domain-Events.md
- DOMAIN-008E-Invariants.md
- DOMAIN-008F-Permissions.md
- DOMAIN-008G-Repository-Contract.md
- DOMAIN-008H-Examples.md
- DOMAIN-008I-Versioning.md
- DOMAIN-008J-Consistency-Boundary.md
- DOMAIN-008K-Integration-Events.md
- DOMAIN-008L-Read-Model.md
- DOMAIN-008M-Test-Scenarios.md
- DOMAIN-008N-Performance-Rules.md
- DOMAIN-008O-Security-Model.md
- DOMAIN-008P-Extension-Points.md
- CORE-003-Shared-Kernel.md
- CORE-004-Ubiquitous-Language.md
- CORE-006-Domain-Invariants.md
- CORE-007-Strategic-Design.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Definir la máquina de estados oficial del Aggregate
**Participation**.

La State Machine establece formalmente:

- estados reconocidos por el dominio;
- estado inicial;
- estados operacionales;
- estados de finalización;
- estado terminal;
- transiciones permitidas;
- transiciones prohibidas;
- Commands responsables de solicitar cada transición;
- Domain Events producidos por transiciones válidas;
- precondiciones conceptuales;
- postcondiciones;
- efectos temporales;
- efectos sobre Version;
- comportamiento ante operaciones inválidas.

La State Machine constituye la autoridad formal para determinar si
una transición de estado puede ejecutarse.

El significado conceptual de cada etapa del ciclo de vida se
encuentra definido en:

```text
DOMAIN-008A-Lifecycle.md
```

---

# Propósito

La State Machine protege la evolución del Aggregate evitando que
`ParticipationStatus` pueda modificarse arbitrariamente.

Toda modificación de estado debe representar un comportamiento
explícito del dominio.

Debe mantenerse:

```text
Current State

+

Command

+

Permissions

+

Invariants

+

Expected Version

↓

Transition Validation

↓

New State

+

Domain Event

+

Version Increment
```

Cuando cualquiera de las condiciones requeridas no se cumple:

```text
Transition Rejected
```

y el Aggregate permanece sin modificaciones.

---

# Principios

La State Machine de Participation sigue los siguientes
principios:

- existe un conjunto explícito y finito de estados;
- toda Participation comienza en Registered;
- ningún estado se asigna directamente;
- cada transición posee un estado origen definido;
- cada transición posee un estado destino definido;
- una transición puede poseer múltiples estados origen únicamente
  cuando el dominio lo establece explícitamente;
- cada transición es solicitada mediante un Command;
- cada transición válida produce el Domain Event correspondiente;
- una transición inválida no modifica el Aggregate;
- una transición inválida no incrementa Version;
- una transición inválida no produce eventos de éxito;
- las transiciones deben preservar invariantes;
- las transiciones deben respetar Permissions;
- Archived no posee transiciones operacionales de salida;
- la State Machine controla exclusivamente Participation;
- ningún estado externo sustituye `ParticipationStatus`;
- Infrastructure no puede alterar las reglas de transición.

---

# Estados Oficiales

Los estados oficiales son:

```text
Registered

Active

Completed

Withdrawn

Invalidated

Archived
```

No existen estados implícitos adicionales.

No deben introducirse estados técnicos dentro de la State Machine
por necesidades de persistencia, transporte, sincronización,
mensajería o interfaz de usuario.

---

# ParticipationStatus

El estado actual se representa conceptualmente mediante:

```text
ParticipationStatus
```

Sus valores válidos son:

```text
Registered

Active

Completed

Withdrawn

Invalidated

Archived
```

`ParticipationStatus` forma parte del estado interno protegido del
Aggregate.

No puede ser modificado directamente desde Application,
Infrastructure, Repository, UI o Integrations.

---

# Estado Inicial

El único estado inicial es:

```text
Registered
```

La creación válida sigue:

```text
No Participation

↓

RegisterParticipation

↓

ParticipationRegistered

↓

Registered
```

Una Participation no puede crearse directamente en otro estado.

---

# Estados Operacionales

Los estados operacionales son:

```text
Registered

Active
```

Registered representa una Participation formalmente registrada que
todavía no ha comenzado.

Active representa una Participation cuyo ejercicio participativo
se encuentra en curso.

---

# Estados de Finalización

Los estados que representan finalización del flujo operacional
normal son:

```text
Completed

Withdrawn

Invalidated
```

Estos estados poseen significados diferentes.

Debe mantenerse:

```text
Completed

≠

Withdrawn

≠

Invalidated
```

---

# Estado Terminal

El estado terminal de conservación lógica es:

```text
Archived
```

Archived no representa eliminación física.

Debe mantenerse:

```text
Archived

≠

Deleted
```

Desde Archived no existen transiciones operacionales normales.

---

# Diagrama Oficial

```text
                         RegisterParticipation
                                  │
                                  ▼
                         ┌─────────────────┐
                         │   Registered    │
                         └───────┬─────────┘
                                 │
                                 │ ActivateParticipation
                                 ▼
                         ┌─────────────────┐
                         │     Active      │
                         └───────┬─────────┘
                                 │
                                 │ CompleteParticipation
                                 ▼
                         ┌─────────────────┐
                         │    Completed    │
                         └───────┬─────────┘
                                 │
                                 │ ArchiveParticipation
                                 ▼
                         ┌─────────────────┐
                         │    Archived     │
                         └─────────────────┘


Registered ── WithdrawParticipation ─────────► Withdrawn

Registered ── InvalidateParticipation ───────► Invalidated

Active ────── WithdrawParticipation ─────────► Withdrawn

Active ────── InvalidateParticipation ───────► Invalidated

Completed ─── InvalidateParticipation ───────► Invalidated

Withdrawn ─── ArchiveParticipation ──────────► Archived

Invalidated ─ ArchiveParticipation ──────────► Archived
```

---

# Tabla Oficial de Transiciones

```text
Origin         Command                      Destination     Domain Event

None           RegisterParticipation        Registered      ParticipationRegistered

Registered     ActivateParticipation        Active          ParticipationActivated

Active         CompleteParticipation        Completed       ParticipationCompleted

Registered     WithdrawParticipation        Withdrawn       ParticipationWithdrawn

Active         WithdrawParticipation        Withdrawn       ParticipationWithdrawn

Registered     InvalidateParticipation      Invalidated     ParticipationInvalidated

Active         InvalidateParticipation      Invalidated     ParticipationInvalidated

Completed      InvalidateParticipation      Invalidated     ParticipationInvalidated

Completed      ArchiveParticipation         Archived        ParticipationArchived

Withdrawn      ArchiveParticipation         Archived        ParticipationArchived

Invalidated    ArchiveParticipation         Archived        ParticipationArchived
```

Esta tabla constituye la definición conceptual de las
transiciones reconocidas por la State Machine.

Una transición no incluida en esta tabla no debe asumirse válida.

---

# Regla de Transición

Toda transición debe satisfacer:

```text
CurrentState ∈ AllowedSourceStates
```

y:

```text
RequestedTransition ∈ DefinedTransitions
```

además de:

```text
Permissions = Valid
```

```text
Invariants = Valid
```

```text
ExpectedVersion = CurrentVersion
```

cuando corresponda.

Solo entonces puede producirse:

```text
State Change
```

---

# Regla de Atomicidad

Una transición constituye una modificación atómica del Aggregate.

Debe confirmarse conjuntamente:

```text
New Status

Lifecycle Timestamp

Version

Domain Event
```

cuando dichos elementos formen parte de la transición.

No debe persistirse un estado parcialmente modificado.

---

# Creación

La creación constituye la entrada inicial a la State Machine.

Command:

```text
RegisterParticipation
```

Estado origen:

```text
None
```

Estado destino:

```text
Registered
```

Evento esperado:

```text
ParticipationRegistered
```

---

# Precondiciones de RegisterParticipation

La creación requiere como mínimo:

- ParticipationId válido;
- OrganizationId válido;
- actor participante identificado;
- ParticipationType válido;
- contexto participativo válido;
- referencias externas válidas según corresponda;
- actor autorizado;
- invariantes de creación satisfechas.

La creación no constituye una transición desde otro estado del
Aggregate porque la Participation todavía no existe.

---

# Postcondiciones de RegisterParticipation

Después de una creación válida:

```text
Status = Registered
```

Debe existir:

```text
CreatedAt
```

Debe existir una versión inicial válida:

```text
Version
```

Debe producirse:

```text
ParticipationRegistered
```

---

# Creación Inválida

Si RegisterParticipation viola una regla del dominio:

```text
No Aggregate Created
```

No debe existir:

```text
ParticipationRegistered
```

No debe persistirse una Participation parcial.

---

# Registered → Active

Command:

```text
ActivateParticipation
```

Estado origen:

```text
Registered
```

Estado destino:

```text
Active
```

Evento esperado:

```text
ParticipationActivated
```

---

# Significado de Registered → Active

Esta transición representa el comienzo formal del ejercicio
participativo.

No representa simplemente un cambio técnico de estado.

Debe mantenerse:

```text
Registered

↓

Valid Activation

↓

Active
```

---

# Precondiciones de ActivateParticipation

Como mínimo:

- Participation existe;
- CurrentStatus es Registered;
- OrganizationId permanece válido;
- identidad del participante permanece válida;
- contexto participativo requerido permanece definido;
- condiciones de activación están satisfechas;
- actor posee Permission;
- invariantes permanecen satisfechas;
- Version esperada coincide con Version actual.

---

# Postcondiciones de ActivateParticipation

Una transición válida produce:

```text
Status = Active
```

Debe establecer:

```text
StartedAt
```

Debe incrementar:

```text
Version
```

Debe producir:

```text
ParticipationActivated
```

---

# Activación Inválida

ActivateParticipation debe rechazarse desde:

```text
Active

Completed

Withdrawn

Invalidated

Archived
```

No debe existir activación idempotente implícita.

Si la operación requiere comportamiento idempotente en una capa
externa, dicha política no modifica la semántica de la State
Machine.

---

# Active → Completed

Command:

```text
CompleteParticipation
```

Estado origen:

```text
Active
```

Estado destino:

```text
Completed
```

Evento esperado:

```text
ParticipationCompleted
```

---

# Significado de Active → Completed

La transición representa la finalización válida de la instancia
participativa.

Completed pertenece exclusivamente al Lifecycle de Participation.

No debe interpretarse como estado de otro Aggregate.

Debe mantenerse:

```text
ParticipationCompleted

≠

AssemblyCompleted
```

```text
ParticipationCompleted

≠

ProposalAccepted
```

```text
ParticipationCompleted

≠

VotingCompleted
```

---

# Precondiciones de CompleteParticipation

Como mínimo:

- Participation existe;
- CurrentStatus es Active;
- StartedAt existe;
- condiciones de finalización están satisfechas;
- invariantes permanecen válidas;
- actor posee Permission;
- Version esperada coincide con Version actual.

---

# Postcondiciones de CompleteParticipation

Una transición válida produce:

```text
Status = Completed
```

Debe establecer:

```text
CompletedAt
```

Debe mantener:

```text
StartedAt
```

Debe incrementar:

```text
Version
```

Debe producir:

```text
ParticipationCompleted
```

---

# Completion Inválido

CompleteParticipation debe rechazarse desde:

```text
Registered

Completed

Withdrawn

Invalidated

Archived
```

La State Machine no permite:

```text
Registered → Completed
```

como transición directa.

---

# Registered → Withdrawn

Command:

```text
WithdrawParticipation
```

Estado origen:

```text
Registered
```

Estado destino:

```text
Withdrawn
```

Evento esperado:

```text
ParticipationWithdrawn
```

---

# Significado de Registered → Withdrawn

Esta transición representa una Participation retirada antes de
haber comenzado formalmente.

Debe mantenerse:

```text
StartedAt = absent
```

cuando nunca existió una activación previa.

---

# Precondiciones de Withdrawal desde Registered

Como mínimo:

- Participation existe;
- CurrentStatus es Registered;
- retiro permitido por las reglas del dominio;
- actor autorizado;
- invariantes satisfechas;
- Version compatible.

---

# Postcondiciones de Withdrawal desde Registered

Debe producir:

```text
Status = Withdrawn
```

Debe establecer:

```text
WithdrawnAt
```

Debe incrementar:

```text
Version
```

Debe producir:

```text
ParticipationWithdrawn
```

No debe inventarse:

```text
StartedAt
```

---

# Active → Withdrawn

Command:

```text
WithdrawParticipation
```

Estado origen:

```text
Active
```

Estado destino:

```text
Withdrawn
```

Evento esperado:

```text
ParticipationWithdrawn
```

---

# Significado de Active → Withdrawn

Representa el retiro de una Participation que ya había comenzado.

La historia debe conservar:

```text
StartedAt
```

porque la Participation estuvo efectivamente Active.

---

# Precondiciones de Withdrawal desde Active

Como mínimo:

- Participation existe;
- CurrentStatus es Active;
- StartedAt existe;
- retiro permitido;
- actor autorizado;
- invariantes satisfechas;
- Version compatible.

---

# Postcondiciones de Withdrawal desde Active

Debe producir:

```text
Status = Withdrawn
```

Debe establecer:

```text
WithdrawnAt
```

Debe preservar:

```text
StartedAt
```

Debe incrementar:

```text
Version
```

Debe producir:

```text
ParticipationWithdrawn
```

---

# Estados desde los cuales Withdrawal está Prohibido

WithdrawParticipation debe rechazarse desde:

```text
Completed

Withdrawn

Invalidated

Archived
```

No debe utilizarse Withdrawal para sustituir:

```text
Invalidation

Archive
```

---

# Registered → Invalidated

Command:

```text
InvalidateParticipation
```

Estado origen:

```text
Registered
```

Estado destino:

```text
Invalidated
```

Evento esperado:

```text
ParticipationInvalidated
```

---

# Significado de Registered → Invalidated

Representa una Participation que pierde su validez antes de
iniciar formalmente.

La invalidación no elimina el Aggregate.

---

# Active → Invalidated

Command:

```text
InvalidateParticipation
```

Estado origen:

```text
Active
```

Estado destino:

```text
Invalidated
```

Evento esperado:

```text
ParticipationInvalidated
```

---

# Significado de Active → Invalidated

Representa una Participation previamente activa cuya validez
cesa conforme a una regla explícita del dominio.

La transición debe conservar:

```text
StartedAt
```

---

# Completed → Invalidated

Command:

```text
InvalidateParticipation
```

Estado origen:

```text
Completed
```

Estado destino:

```text
Invalidated
```

Evento esperado:

```text
ParticipationInvalidated
```

---

# Significado de Completed → Invalidated

Esta transición representa una invalidación posterior a una
finalización previamente válida.

La State Machine preserva la historia.

Por lo tanto:

```text
CompletedAt
```

no debe eliminarse.

Debe mantenerse la secuencia causal:

```text
ParticipationActivated

↓

ParticipationCompleted

↓

ParticipationInvalidated
```

cuando ese haya sido el recorrido real.

---

# Precondiciones de InvalidateParticipation

Como mínimo:

- Participation existe;
- CurrentStatus pertenece a los estados permitidos;
- existe una causa de invalidación reconocida por el dominio;
- actor posee Permission;
- invariantes aplicables están satisfechas;
- Version esperada coincide con Version actual.

Los estados origen permitidos son:

```text
Registered

Active

Completed
```

---

# Postcondiciones de InvalidateParticipation

Una invalidación válida produce:

```text
Status = Invalidated
```

Debe establecer:

```text
InvalidatedAt
```

Debe preservar timestamps históricos anteriores.

Debe incrementar:

```text
Version
```

Debe producir:

```text
ParticipationInvalidated
```

---

# Estados desde los cuales Invalidation está Prohibida

InvalidateParticipation debe rechazarse desde:

```text
Withdrawn

Invalidated

Archived
```

No existe invalidación repetida implícita.

---

# Completed → Archived

Command:

```text
ArchiveParticipation
```

Estado origen:

```text
Completed
```

Estado destino:

```text
Archived
```

Evento esperado:

```text
ParticipationArchived
```

---

# Withdrawn → Archived

Command:

```text
ArchiveParticipation
```

Estado origen:

```text
Withdrawn
```

Estado destino:

```text
Archived
```

Evento esperado:

```text
ParticipationArchived
```

---

# Invalidated → Archived

Command:

```text
ArchiveParticipation
```

Estado origen:

```text
Invalidated
```

Estado destino:

```text
Archived
```

Evento esperado:

```text
ParticipationArchived
```

---

# Significado de ArchiveParticipation

ArchiveParticipation representa el cierre lógico de una
Participation cuyo flujo operacional ya terminó.

Archived conserva:

- identidad;
- OrganizationId;
- actor;
- contexto;
- timestamps históricos;
- Version;
- historia de eventos;
- referencias necesarias para trazabilidad.

No representa eliminación física.

---

# Precondiciones de ArchiveParticipation

Como mínimo:

- Participation existe;
- CurrentStatus pertenece a los estados archivables;
- actor posee Permission;
- invariantes están satisfechas;
- Version es compatible.

Los estados archivables son:

```text
Completed

Withdrawn

Invalidated
```

---

# Postcondiciones de ArchiveParticipation

Una transición válida produce:

```text
Status = Archived
```

Debe preservar la información histórica previa.

Debe incrementar:

```text
Version
```

Debe producir:

```text
ParticipationArchived
```

---

# Estados desde los cuales Archive está Prohibido

ArchiveParticipation debe rechazarse desde:

```text
Registered

Active

Archived
```

No se permite archivar una Participation que todavía se encuentra
en su flujo operacional normal.

---

# Matriz Completa de Transiciones

```text
Current State   Register   Activate   Complete   Withdraw   Invalidate   Archive

None            YES        NO         NO         NO         NO           NO

Registered      NO         YES        NO         YES        YES          NO

Active          NO         NO         YES        YES        YES          NO

Completed       NO         NO         NO         NO         YES          YES

Withdrawn       NO         NO         NO         NO         NO           YES

Invalidated     NO         NO         NO         NO         NO           YES

Archived        NO         NO         NO         NO         NO           NO
```

`YES` significa que la transición existe conceptualmente.

No significa que deba ejecutarse automáticamente.

Toda transición continúa sujeta a:

```text
Permissions

Invariants

Version

Domain Rules
```

---

# Matriz Estado / Command / Evento

```text
Current        Command                    Next          Event

None           RegisterParticipation      Registered    ParticipationRegistered

Registered     ActivateParticipation      Active        ParticipationActivated

Registered     WithdrawParticipation      Withdrawn     ParticipationWithdrawn

Registered     InvalidateParticipation    Invalidated   ParticipationInvalidated

Active         CompleteParticipation      Completed     ParticipationCompleted

Active         WithdrawParticipation      Withdrawn     ParticipationWithdrawn

Active         InvalidateParticipation    Invalidated   ParticipationInvalidated

Completed      InvalidateParticipation    Invalidated   ParticipationInvalidated

Completed      ArchiveParticipation       Archived      ParticipationArchived

Withdrawn      ArchiveParticipation       Archived      ParticipationArchived

Invalidated    ArchiveParticipation       Archived      ParticipationArchived
```

---

# Matriz de Estados Prohibidos

```text
Origin         Forbidden Destinations

Registered     Completed
               Archived

Active         Registered
               Archived

Completed      Registered
               Active
               Withdrawn

Withdrawn      Registered
               Active
               Completed
               Invalidated

Invalidated    Registered
               Active
               Completed
               Withdrawn

Archived       Registered
               Active
               Completed
               Withdrawn
               Invalidated
```

La ausencia de una transición en la tabla oficial implica que no
existe dentro del modelo actual.

---

# Transiciones Prohibidas desde Registered

No están permitidas:

```text
Registered → Completed

Registered → Archived
```

Registered tampoco puede transicionar hacia sí mismo como una
operación de estado.

---

# Transiciones Prohibidas desde Active

No están permitidas:

```text
Active → Registered

Active → Archived
```

Active no puede volver al estado previo mediante rollback de
dominio.

---

# Transiciones Prohibidas desde Completed

No están permitidas:

```text
Completed → Registered

Completed → Active

Completed → Withdrawn
```

Completed puede únicamente evolucionar según las transiciones
explícitamente reconocidas:

```text
Completed → Invalidated

Completed → Archived
```

---

# Transiciones Prohibidas desde Withdrawn

No están permitidas:

```text
Withdrawn → Registered

Withdrawn → Active

Withdrawn → Completed

Withdrawn → Invalidated
```

La única transición operacional posterior reconocida es:

```text
Withdrawn → Archived
```

---

# Transiciones Prohibidas desde Invalidated

No están permitidas:

```text
Invalidated → Registered

Invalidated → Active

Invalidated → Completed

Invalidated → Withdrawn
```

La única transición posterior reconocida es:

```text
Invalidated → Archived
```

---

# Transiciones Prohibidas desde Archived

No existe transición normal desde:

```text
Archived
```

hacia ningún otro estado.

Debe mantenerse:

```text
Archived

↓

No Operational Transition
```

---

# No Reactivación

La State Machine actual no define:

```text
Completed → Active
```

```text
Withdrawn → Active
```

```text
Invalidated → Active
```

```text
Archived → Active
```

Por lo tanto, no existe conceptualmente:

```text
ReactivateParticipation
```

dentro del modelo actual.

Una futura necesidad de reactivación requiere una evolución
explícita del dominio.

---

# No Restauración

La State Machine actual tampoco define:

```text
Archived → Previous State
```

No existe:

```text
RestoreParticipation
```

como transición oficial.

Archived constituye el estado terminal del modelo actual.

---

# No Eliminación

La State Machine no contiene:

```text
Deleted
```

como estado.

Debe mantenerse:

```text
Withdrawn ≠ Deleted

Invalidated ≠ Deleted

Archived ≠ Deleted
```

La eliminación física pertenece a políticas de persistencia,
retención o infraestructura cuando corresponda y no sustituye el
estado conceptual del Aggregate.

---

# Estados y Timestamps

La State Machine debe mantener coherencia entre estado y
timestamps.

```text
Registered
    │
    └── CreatedAt
```

```text
Active
    │
    ├── CreatedAt
    └── StartedAt
```

```text
Completed
    │
    ├── CreatedAt
    ├── StartedAt
    └── CompletedAt
```

```text
Withdrawn
    │
    ├── CreatedAt
    └── WithdrawnAt
```

Cuando Withdrawal ocurre desde Active también debe conservar:

```text
StartedAt
```

---

# Invalidated y Timestamps

Invalidated debe conservar toda información temporal válida
anterior.

Ejemplo desde Registered:

```text
CreatedAt

InvalidatedAt
```

Ejemplo desde Active:

```text
CreatedAt

StartedAt

InvalidatedAt
```

Ejemplo desde Completed:

```text
CreatedAt

StartedAt

CompletedAt

InvalidatedAt
```

La invalidación no reescribe la historia.

---

# Archived y Timestamps

Archived conserva los timestamps acumulados durante el Lifecycle.

Ejemplo:

```text
Registered

↓

Active

↓

Completed

↓

Archived
```

conserva:

```text
CreatedAt

StartedAt

CompletedAt
```

El archivado no elimina información temporal previa.

---

# Coherencia Temporal

Debe mantenerse:

```text
CreatedAt <= StartedAt
```

cuando StartedAt exista.

Debe mantenerse:

```text
StartedAt <= CompletedAt
```

cuando CompletedAt exista.

Debe mantenerse:

```text
CreatedAt <= WithdrawnAt
```

cuando WithdrawnAt exista.

Debe mantenerse:

```text
CreatedAt <= InvalidatedAt
```

cuando InvalidatedAt exista.

Las invariantes temporales completas se especifican en:

```text
DOMAIN-008E-Invariants.md
```

---

# Estado y Version

Toda transición válida incrementa Version.

Conceptualmente:

```text
Registered
Version 1

↓

ActivateParticipation

↓

Active
Version 2
```

Luego:

```text
Active
Version 2

↓

CompleteParticipation

↓

Completed
Version 3
```

La numeración exacta de la versión inicial se encuentra gobernada
por:

```text
DOMAIN-008I-Versioning.md
```

---

# Transición Rechazada y Version

Una transición rechazada no incrementa Version.

Ejemplo:

```text
Status = Registered
Version = 3
```

Command:

```text
CompleteParticipation
```

Resultado:

```text
Rejected
```

Debe mantenerse:

```text
Status = Registered

Version = 3
```

No debe existir:

```text
ParticipationCompleted
```

---

# Concurrencia Optimista

Las transiciones deben respetar el mecanismo de Version definido
para Participation.

Conceptualmente:

```text
ExpectedVersion

=

CurrentVersion
```

debe cumplirse antes de confirmar una modificación.

---

# Conflicto de Concurrencia

Ejemplo:

```text
Participation
Status = Active
Version = 7
```

Proceso A solicita:

```text
CompleteParticipation
ExpectedVersion = 7
```

Proceso B solicita:

```text
WithdrawParticipation
ExpectedVersion = 7
```

Si A se confirma primero:

```text
Status = Completed
Version = 8
```

B ya no puede confirmar silenciosamente la modificación basada en:

```text
Version = 7
```

Debe detectarse el conflicto y reevaluarse el estado actual.

---

# Concurrencia no Redefine Transiciones

Un conflicto de Version no constituye un nuevo estado.

No deben agregarse estados como:

```text
Conflict

Retry

Stale
```

a `ParticipationStatus`.

Estos conceptos pertenecen al control de concurrencia y no al
Lifecycle del Aggregate.

---

# State Machine e Invariantes

La existencia de una transición en la State Machine no garantiza
su ejecución.

Debe mantenerse:

```text
Transition Defined

+

Invariant Violation

=

Rejected
```

Las invariantes se definen formalmente en:

```text
DOMAIN-008E-Invariants.md
```

---

# State Machine y Permissions

Una transición definida tampoco puede ser ejecutada por cualquier
actor.

Debe mantenerse:

```text
Transition Defined

+

Unauthorized Actor

=

Rejected
```

Las Permissions se definen en:

```text
DOMAIN-008F-Permissions.md
```

---

# Permission no Crea Transiciones

Un actor con privilegios administrativos no puede crear
transiciones inexistentes.

Debe mantenerse:

```text
Authorized Actor

+

Undefined Transition

=

Rejected
```

Ejemplo:

```text
Administrator

+

Archived → Active

=

Rejected
```

mientras dicha transición no exista en el dominio.

---

# Invariant no Crea Transiciones

El cumplimiento de invariantes tampoco permite una transición no
definida.

Debe mantenerse:

```text
All Invariants Valid

+

Undefined Transition

=

Rejected
```

La State Machine continúa siendo autoridad sobre la existencia de
la transición.

---

# Estado e Identidad

Ninguna transición puede modificar:

```text
ParticipationId
```

Debe mantenerse:

```text
ParticipationId before transition

=

ParticipationId after transition
```

durante todo el Lifecycle.

---

# Estado y Organization

Ninguna transición puede modificar:

```text
OrganizationId
```

Debe mantenerse:

```text
OrganizationId at Registered

=

OrganizationId at Active

=

OrganizationId at Completed

=

OrganizationId at Withdrawn

=

OrganizationId at Invalidated

=

OrganizationId at Archived
```

---

# Estado y Actor

Las transiciones de estado no convierten la Participation en la
participación de otro actor.

La identidad contextual del participante debe preservarse según
las referencias definidas en el Aggregate.

No debe utilizarse una transición para sustituir:

```text
CitizenId
```

o:

```text
MembershipId
```

cuando dichas referencias formen parte de la identidad contextual
de Participation.

---

# State Machine y Organization

El estado de Organization no sustituye el estado de
Participation.

Debe mantenerse:

```text
OrganizationStatus

≠

ParticipationStatus
```

Un cambio en Organization puede provocar una coordinación de
dominio externa cuando corresponda, pero no constituye una
asignación automática del estado interno de Participation.

---

# State Machine y Citizen

Citizen mantiene su propio Lifecycle.

Debe mantenerse:

```text
CitizenStatus

≠

ParticipationStatus
```

Una transición de Citizen no modifica directamente
Participation.

---

# State Machine y Membership

Membership mantiene una State Machine independiente.

Debe mantenerse:

```text
MembershipStatus

≠

ParticipationStatus
```

Por ejemplo:

```text
Membership = Active
```

no implica:

```text
Participation = Active
```

---

# State Machine y Role

Role no controla `ParticipationStatus`.

Una modificación de Role puede afectar autorización para futuros
Commands cuando corresponda.

No modifica retroactivamente el estado confirmado de
Participation.

---

# State Machine y Territory

Territory puede proporcionar contexto territorial.

Debe mantenerse:

```text
TerritoryStatus

≠

ParticipationStatus
```

La State Machine de Participation permanece independiente.

---

# State Machine y Assembly

Assembly y Participation poseen Lifecycles independientes.

Debe mantenerse:

```text
AssemblyStatus

≠

ParticipationStatus
```

No debe asumirse:

```text
Assembly InProgress

↓

Participation Active
```

sin un Command válido sobre Participation.

Tampoco:

```text
Assembly Completed

↓

Participation Completed
```

como modificación automática.

---

# State Machine y Proposal

Proposal mantiene su propia State Machine.

Debe mantenerse:

```text
ProposalStatus

≠

ParticipationStatus
```

No debe asumirse:

```text
Proposal Accepted

↓

Participation Completed
```

ni:

```text
Proposal Rejected

↓

Participation Invalidated
```

sin comportamiento explícito sobre Participation.

---

# State Machine y Voting

Voting mantiene su propia State Machine.

Debe mantenerse:

```text
VotingStatus

≠

ParticipationStatus
```

Una votación puede existir dentro del mismo contexto participativo
sin convertirse en parte del estado interno de Participation.

---

# State Machine y Document

Document mantiene su propio Lifecycle.

Debe mantenerse:

```text
DocumentStatus

≠

ParticipationStatus
```

Crear, publicar o archivar un Document no constituye una
transición automática de Participation.

---

# State Machine y Notification

Notification puede reaccionar a Domain Events.

Ejemplo:

```text
ParticipationActivated

↓

Notification
```

El resultado de Notification no modifica directamente
`ParticipationStatus`.

---

# State Machine y Audit

Audit puede registrar las transiciones ocurridas.

Conceptualmente:

```text
ParticipationRegistered

ParticipationActivated

ParticipationCompleted

ParticipationWithdrawn

ParticipationInvalidated

ParticipationArchived
```

constituyen hechos relevantes para trazabilidad.

Audit no determina qué transiciones son válidas.

---

# State Machine e Integration

Integration puede publicar representaciones externas de los hechos
producidos por la State Machine.

Debe mantenerse:

```text
Internal Transition

↓

Domain Event

↓

Integration Mapping

↓

Integration Event
```

Integration no modifica directamente `ParticipationStatus`.

---

# Fallos Externos

Un fallo posterior en:

```text
Notification

Audit Projection

Integration

Read Model

External API
```

no debe revertir automáticamente una transición ya confirmada.

Ejemplo:

```text
Active

↓

CompleteParticipation

↓

Completed

↓

ParticipationCompleted

↓

Integration Failure
```

no significa:

```text
Completed → Active
```

---

# Transacción del Aggregate

La transición interna debe completarse dentro del límite de
consistencia de Participation.

Conceptualmente:

```text
Load Participation

↓

Validate Command

↓

Validate State

↓

Validate Permissions

↓

Validate Invariants

↓

Validate Version

↓

Apply Transition

↓

Create Domain Event

↓

Persist Aggregate
```

La coordinación con otros Aggregates ocurre fuera de esta
transacción cuando corresponda.

---

# State Machine y Repository

El Repository persiste el estado resultante.

No decide transiciones.

Debe mantenerse:

```text
Aggregate

↓

Valid Transition

↓

Repository Persistence
```

No:

```text
Repository

↓

Direct Status Mutation

↓

Aggregate
```

El contrato formal se define en:

```text
DOMAIN-008G-Repository-Contract.md
```

---

# Persistencia Directa Prohibida

No debe utilizarse una operación de infraestructura equivalente a:

```text
UPDATE participation
SET status = 'Completed'
WHERE participation_id = ...
```

como sustituto de:

```text
CompleteParticipation
```

La persistencia debe reflejar una transición ya validada por el
Aggregate.

---

# State Machine y Rehidratación

La rehidratación recupera el estado existente.

No constituye una transición.

Debe mantenerse:

```text
Persisted Participation

↓

Rehydrate

↓

Same Participation State
```

Sin:

```text
Version Increment
```

y sin nuevos eventos de negocio.

---

# State Machine y Event Sourcing

Cuando Participation utilice Event Sourcing, la State Machine
puede reconstruirse aplicando eventos históricos.

Ejemplo:

```text
ParticipationRegistered

↓

Registered

↓

ParticipationActivated

↓

Active

↓

ParticipationCompleted

↓

Completed
```

La secuencia histórica debe respetar las transiciones oficiales.

---

# Aplicación de Eventos Históricos

Aplicar un evento durante replay no equivale a ejecutar el Command
que originalmente lo produjo.

Debe mantenerse:

```text
Apply Historical Event

≠

Execute Command
```

Durante replay no se vuelven a validar Permissions como si se
tratara de una nueva intención.

La reconstrucción representa hechos ya ocurridos.

---

# Historia Inválida

Una secuencia histórica incompatible con la State Machine no debe
normalizarse silenciosamente.

Ejemplo:

```text
ParticipationRegistered

↓

ParticipationCompleted
```

sin:

```text
ParticipationActivated
```

es incompatible con el modelo actual.

La implementación debe tratar dicha inconsistencia conforme a las
reglas de reconstrucción y consistencia establecidas para el
dominio.

---

# State Machine y CQRS

En CQRS:

```text
Command

↓

Write Side

↓

Participation Aggregate

↓

State Machine

↓

Domain Event

↓

Read Side
```

El Read Side refleja el estado.

No controla las transiciones.

---

# Proyección de Estados

Los Domain Events pueden proyectar:

```text
ParticipationRegistered
    ↓
Registered
```

```text
ParticipationActivated
    ↓
Active
```

```text
ParticipationCompleted
    ↓
Completed
```

```text
ParticipationWithdrawn
    ↓
Withdrawn
```

```text
ParticipationInvalidated
    ↓
Invalidated
```

```text
ParticipationArchived
    ↓
Archived
```

---

# Consistencia Eventual del Read Model

Una proyección puede encontrarse temporalmente retrasada.

Ejemplo:

```text
Write Model

Status = Completed
```

mientras:

```text
Read Model

Status = Active
```

hasta procesar:

```text
ParticipationCompleted
```

Esta diferencia temporal no modifica la autoridad de la State
Machine.

---

# Estado Autoritativo

La autoridad para decidir una transición pertenece al Aggregate
de escritura.

Debe mantenerse:

```text
Participation Aggregate State

=

Authoritative Domain State
```

El Read Model no debe utilizarse para bypass de la validación del
Aggregate.

---

# Idempotencia

La State Machine no interpreta automáticamente la repetición de un
Command como una transición válida.

Ejemplo:

```text
Registered

↓

ActivateParticipation

↓

Active
```

Un segundo:

```text
ActivateParticipation
```

sobre Active no representa otra transición válida.

Debe ser rechazado por estado salvo que una política externa de
idempotencia evite que el Command duplicado llegue nuevamente al
Aggregate.

---

# Idempotencia y Eventos

Un Command duplicado no debe generar eventos duplicados de éxito
si no produce una nueva transición válida.

Debe evitarse:

```text
ParticipationActivated

ParticipationActivated
```

para una única transición real.

---

# Commands Fuera de Orden

La State Machine debe rechazar Commands recibidos fuera del orden
permitido.

Ejemplo:

```text
CompleteParticipation
```

recibido antes de:

```text
ActivateParticipation
```

no puede completar una Participation Registered.

---

# Eventos Fuera de Orden

Las proyecciones e integraciones deben preservar la capacidad de
detectar o manejar eventos fuera de orden conforme a sus propios
contratos.

Sin embargo, un evento externo fuera de orden no redefine la State
Machine interna.

---

# Razón de Transición

Cuando el modelo definido para una transición requiera una razón,
causa o contexto, dicha información debe formar parte del Command
o del comportamiento correspondiente.

Especialmente:

```text
WithdrawParticipation

InvalidateParticipation
```

pueden requerir información contextual según las reglas
establecidas en Commands e Invariants.

La State Machine no inventa causas.

---

# Invalidation no es Correction

Invalidar una Participation no significa modificar retroactivamente
su historia.

Debe mantenerse:

```text
Historical Facts

+

ParticipationInvalidated

=

New Domain History
```

No:

```text
Historical Facts Deleted
```

---

# Withdrawal no es Rollback

WithdrawParticipation tampoco revierte los hechos anteriores.

Si la Participation estuvo Active:

```text
ParticipationActivated
```

continúa formando parte de su historia después de:

```text
ParticipationWithdrawn
```

---

# Archive no es Reset

ArchiveParticipation no reinicia atributos ni elimina el recorrido
del Aggregate.

Debe mantenerse:

```text
Archived Participation

=

Participation with preserved history
```

No:

```text
Archived Participation

=

Empty Participation
```

---

# Reglas de Modificación durante Registered

Mientras el estado sea Registered, pueden existir comportamientos
no transicionales definidos por el Aggregate y sus Commands.

Estos comportamientos:

- no deben cambiar Status salvo que correspondan a una transición
  oficial;
- deben respetar invariantes;
- deben respetar Permissions;
- deben incrementar Version cuando constituyan modificaciones
  válidas;
- pueden producir Domain Events específicos.

La existencia de operaciones no transicionales no altera la State
Machine.

---

# Reglas de Modificación durante Active

Mientras Participation se encuentre Active, solo pueden ejecutarse
comportamientos compatibles con dicho estado.

Una modificación no transicional no puede:

- cambiar ParticipationId;
- cambiar OrganizationId;
- sustituir arbitrariamente al participante;
- eliminar StartedAt;
- modificar Status directamente;
- crear una transición implícita.

---

# Reglas de Modificación durante Completed

Completed restringe las modificaciones ordinarias.

Solo deben permitirse comportamientos expresamente definidos por el
dominio para este estado.

Las transiciones reconocidas son:

```text
Completed → Invalidated

Completed → Archived
```

No debe utilizarse una modificación de atributos para simular una
reactivación.

---

# Reglas de Modificación durante Withdrawn

Withdrawn representa cierre por retiro.

La transición reconocida es:

```text
Withdrawn → Archived
```

No deben permitirse modificaciones que reabran implícitamente la
Participation.

---

# Reglas de Modificación durante Invalidated

Invalidated representa cierre por pérdida de validez.

La transición reconocida es:

```text
Invalidated → Archived
```

No deben permitirse modificaciones que restauren implícitamente la
validez.

---

# Reglas de Modificación durante Archived

Archived es inmutable para comportamiento operacional normal.

No se permiten:

- cambios de estado;
- cambios de contexto;
- cambios de actor;
- cambios de OrganizationId;
- cambios ordinarios de atributos;
- Commands operacionales.

Las necesidades técnicas de migración o mantenimiento no
constituyen comportamiento del Aggregate.

---

# Separación entre Estado y Autorización

La State Machine responde:

```text
Can this state transition exist?
```

Permissions responde:

```text
Can this actor request this operation?
```

Ambas condiciones deben cumplirse.

No deben mezclarse.

---

# Separación entre Estado e Invariantes

La State Machine define la relación estructural entre estados.

Las Invariants determinan condiciones que siempre deben
preservarse.

Ejemplo:

```text
Registered → Active
```

puede existir como transición, pero debe rechazarse si una
invariante requerida para activación no se cumple.

---

# Separación entre Estado y Application Workflow

La capa Application puede coordinar pasos como:

```text
Load

Authorize

Execute

Persist

Publish
```

pero no puede inventar transiciones.

La State Machine pertenece al dominio.

---

# Separación entre Estado e Infrastructure

Infrastructure puede:

- persistir;
- serializar;
- transportar;
- publicar mensajes;
- recuperar datos.

Infrastructure no puede:

- agregar estados;
- eliminar estados;
- permitir transiciones prohibidas;
- modificar Status directamente;
- reinterpretar estados del dominio.

---

# Separación entre Estado e Integración

Los sistemas externos pueden utilizar estados diferentes.

La capa de integración debe traducirlos.

Ejemplo conceptual:

```text
External Status

↓

Integration Mapping

↓

Participation Concept
```

No debe incorporarse automáticamente un valor externo a:

```text
ParticipationStatus
```

---

# Separación entre Estado y UI

La interfaz puede representar:

```text
Registered
```

como:

```text
Registrada
```

o utilizar indicadores visuales.

La representación visual no redefine la State Machine.

---

# Estado Desconocido

Un valor que no pertenezca a:

```text
Registered

Active

Completed

Withdrawn

Invalidated

Archived
```

no constituye un estado válido de Participation.

Debe ser rechazado por el modelo.

---

# Validación de Estado al Rehidratar

El Repository no debe rehidratar silenciosamente un estado
desconocido como si fuese válido.

Debe preservarse la integridad del modelo.

Un estado persistido incompatible debe tratarse como una
inconsistencia y no como una nueva extensión automática del
dominio.

---

# Reglas de Dominio ante Transición Inválida

Ante una transición inválida:

```text
State remains unchanged
```

```text
Version remains unchanged
```

```text
No success Domain Event
```

```text
No lifecycle timestamp mutation
```

```text
No partial persistence
```

---

# Regla de Evento

Un Domain Event de transición solo puede representar una
transición efectivamente confirmada.

No debe publicarse:

```text
ParticipationCompleted
```

si el Aggregate continúa:

```text
Active
```

debido a que `CompleteParticipation` fue rechazado.

---

# Regla de Evento y Commit

El evento representa un hecho del dominio asociado a una
modificación válida.

La persistencia del Aggregate y el tratamiento confiable de los
eventos deben respetar los contratos arquitectónicos definidos
para AURA.

La State Machine no depende del mecanismo técnico utilizado para
publicarlos.

---

# Matriz de Eventos por Estado Destino

```text
Destination     Domain Event

Registered      ParticipationRegistered

Active          ParticipationActivated

Completed       ParticipationCompleted

Withdrawn       ParticipationWithdrawn

Invalidated     ParticipationInvalidated

Archived        ParticipationArchived
```

---

# Matriz de Timestamps por Transición

```text
Transition                Timestamp Effect

None → Registered         CreatedAt

Registered → Active       StartedAt

Active → Completed        CompletedAt

Registered → Withdrawn    WithdrawnAt

Active → Withdrawn        WithdrawnAt

Registered → Invalidated  InvalidatedAt

Active → Invalidated      InvalidatedAt

Completed → Invalidated   InvalidatedAt

Completed → Archived      Preserve history

Withdrawn → Archived      Preserve history

Invalidated → Archived    Preserve history
```

---

# Matriz de Versionado

```text
Operation                  Version

Valid creation             Initial Version

Valid transition           Increment

Rejected transition        Unchanged

Rehydration                Unchanged

Replay                     Reconstructed from history

Read projection            Does not modify Aggregate Version
```

La definición normativa completa corresponde a:

```text
DOMAIN-008I-Versioning.md
```

---

# Matriz de Responsabilidad

```text
Concern                     Authority

State existence             State Machine

Transition existence        State Machine

Business validity           Invariants

Actor authorization         Permissions

Intent                      Command

Occurred fact               Domain Event

Persistence                 Repository

Concurrency                 Versioning

External publication        Integration

Query representation        Read Model

Audit consumption           Audit
```

---

# Casos de Transición Válida

## Caso 1 — Activación

Given:

```text
Status = Registered
```

When:

```text
ActivateParticipation
```

And:

```text
Permissions valid

Invariants valid

Version valid
```

Then:

```text
Status = Active
```

And:

```text
ParticipationActivated
```

---

# Caso 2 — Completion

Given:

```text
Status = Active
```

When:

```text
CompleteParticipation
```

Then:

```text
Status = Completed
```

And:

```text
ParticipationCompleted
```

---

# Caso 3 — Withdrawal antes de Active

Given:

```text
Status = Registered
```

When:

```text
WithdrawParticipation
```

Then:

```text
Status = Withdrawn
```

And:

```text
ParticipationWithdrawn
```

---

# Caso 4 — Withdrawal durante Active

Given:

```text
Status = Active
```

When:

```text
WithdrawParticipation
```

Then:

```text
Status = Withdrawn
```

And:

```text
ParticipationWithdrawn
```

---

# Caso 5 — Invalidation después de Completion

Given:

```text
Status = Completed
```

When:

```text
InvalidateParticipation
```

Then:

```text
Status = Invalidated
```

And:

```text
ParticipationInvalidated
```

CompletedAt permanece como hecho histórico.

---

# Caso 6 — Archive de Withdrawn

Given:

```text
Status = Withdrawn
```

When:

```text
ArchiveParticipation
```

Then:

```text
Status = Archived
```

And:

```text
ParticipationArchived
```

---

# Casos de Transición Inválida

## Caso 1 — Complete desde Registered

Given:

```text
Status = Registered
```

When:

```text
CompleteParticipation
```

Then:

```text
Rejected
```

State:

```text
Registered
```

permanece sin cambios.

---

# Caso 2 — Activate desde Completed

Given:

```text
Status = Completed
```

When:

```text
ActivateParticipation
```

Then:

```text
Rejected
```

No existe:

```text
Completed → Active
```

---

# Caso 3 — Complete desde Withdrawn

Given:

```text
Status = Withdrawn
```

When:

```text
CompleteParticipation
```

Then:

```text
Rejected
```

Withdrawal terminó el flujo operacional normal.

---

# Caso 4 — Withdraw desde Invalidated

Given:

```text
Status = Invalidated
```

When:

```text
WithdrawParticipation
```

Then:

```text
Rejected
```

Invalidated y Withdrawn poseen semánticas diferentes.

---

# Caso 5 — Archive desde Active

Given:

```text
Status = Active
```

When:

```text
ArchiveParticipation
```

Then:

```text
Rejected
```

Active no es un estado archivable.

---

# Caso 6 — Cualquier transición desde Archived

Given:

```text
Status = Archived
```

When:

Se solicita cualquier transición operacional.

Then:

```text
Rejected
```

Archived permanece:

```text
Archived
```

---

# Caso 7 — Version Conflict

Given:

```text
CurrentVersion = 12
```

When:

```text
Command.ExpectedVersion = 11
```

Then:

La transición no puede confirmarse sobre la revisión obsoleta.

Debe mantenerse el estado actual hasta que la operación sea
reevaluada conforme a las reglas de Versioning.

---

# Caso 8 — Actor no Autorizado

Given:

```text
Status = Registered
```

When:

```text
ActivateParticipation
```

And:

```text
Permission = Denied
```

Then:

```text
Rejected
```

Aunque:

```text
Registered → Active
```

sea una transición definida.

---

# Caso 9 — Invariante Violada

Given:

```text
Status = Active
```

When:

```text
CompleteParticipation
```

And:

```text
Invariant = Violated
```

Then:

```text
Rejected
```

No se produce:

```text
ParticipationCompleted
```

---

# Testabilidad de la State Machine

La State Machine debe poder verificarse de forma determinista.

Los escenarios deben cubrir:

- cada transición válida;
- cada transición prohibida;
- cada estado origen;
- cada estado destino;
- rechazo por estado;
- rechazo por Permission;
- rechazo por Invariant;
- rechazo por Version;
- timestamps;
- Domain Events;
- conservación histórica;
- inmutabilidad de Archived;
- independencia respecto de otros Aggregates.

La especificación detallada corresponde a:

```text
DOMAIN-008M-Test-Scenarios.md
```

---

# Reglas de Performance

Las optimizaciones no pueden omitir validaciones de la State
Machine.

No debe utilizarse:

```text
Direct Database State Update
```

para evitar cargar o validar el Aggregate.

Las reglas específicas se desarrollan en:

```text
DOMAIN-008N-Performance-Rules.md
```

---

# Reglas de Seguridad

La State Machine debe estar protegida contra:

- modificación directa de Status;
- Commands no autorizados;
- bypass del Aggregate Root;
- manipulación de Version;
- modificación cruzada de Organizations;
- sustitución del participante;
- estados desconocidos;
- transiciones inexistentes;
- persistencia parcial.

El modelo completo se desarrolla en:

```text
DOMAIN-008O-Security-Model.md
```

---

# Extension Points

La State Machine puede evolucionar cuando el dominio requiera
nuevos estados o transiciones.

Toda extensión debe:

- representar una necesidad real del dominio;
- utilizar lenguaje ubicuo;
- preservar invariantes existentes o evolucionarlas
  explícitamente;
- actualizar Lifecycle;
- actualizar State Machine;
- actualizar Commands;
- actualizar Domain Events;
- actualizar Permissions;
- actualizar Test Scenarios;
- actualizar Read Models cuando corresponda;
- mantener compatibilidad de Versioning e Integration Events.

Las extensiones se documentan en:

```text
DOMAIN-008P-Extension-Points.md
```

---

# Prohibición de Extensiones Implícitas

No se considera una extensión válida agregar directamente un nuevo
valor a:

```text
ParticipationStatus
```

sin actualizar el modelo conceptual.

No debe introducirse por conveniencia técnica:

```text
Pending

Processing

Failed

Retrying

Syncing

Deleted
```

como estado de dominio sin una decisión explícita de evolución.

---

# Compatibilidad con DDD

La State Machine cumple los principios de Domain-Driven Design al
mantener:

- comportamiento dentro del Aggregate;
- estado encapsulado;
- invariantes protegidas;
- transiciones explícitas;
- identidad estable;
- consistencia interna;
- separación entre Aggregates.

---

# Compatibilidad con Clean Architecture

La State Machine pertenece al Domain Layer.

No depende de:

```text
Database

ORM

HTTP

REST

GraphQL

Framework

Message Broker

External API
```

Las tecnologías implementan los mecanismos necesarios.

No definen las reglas de estado.

---

# Compatibilidad con CQRS

Los Commands solicitan transiciones.

Los Domain Events representan transiciones confirmadas.

Los Read Models proyectan sus resultados.

```text
Command

↓

State Machine

↓

Domain Event

↓

Projection
```

---

# Compatibilidad con Event Sourcing

La State Machine puede reconstruirse mediante la secuencia de
Domain Events.

La historia debe producir un recorrido compatible con las
transiciones definidas.

---

# Compatibilidad con Event-Driven Architecture

Cada transición relevante puede originar reacciones externas
mediante eventos.

Las reacciones permanecen fuera del límite de consistencia de
Participation.

---

# Compatibilidad con Arquitectura Distribuida

La State Machine no requiere transacciones distribuidas con otros
Aggregates.

Debe mantenerse:

```text
Participation Transaction

=

Participation Consistency Boundary
```

La coordinación externa utiliza los mecanismos establecidos por la
arquitectura de AURA.

---

# Principios Arquitectónicos

La State Machine mantiene:

```text
State

≠

Public Mutable Attribute
```

```text
Command

≠

State
```

```text
Command

≠

Domain Event
```

```text
Domain Event

=

Occurred Domain Fact
```

```text
Defined Transition

≠

Automatically Valid Transition
```

```text
Permission

≠

Transition Definition
```

```text
Invariant

≠

Transition Definition
```

```text
Archived

≠

Deleted
```

```text
Withdrawal

≠

Invalidation
```

```text
Completion

≠

External Process Completion
```

```text
Repository

≠

State Machine
```

```text
Read Model

≠

State Authority
```

```text
Integration

≠

State Authority
```

```text
Infrastructure

≠

Domain Transition Authority
```

---

# Restricciones

No está permitido:

- modificar ParticipationStatus directamente;
- crear Participation en un estado diferente de Registered;
- completar una Participation Registered;
- activar una Participation Completed;
- activar una Participation Withdrawn;
- activar una Participation Invalidated;
- activar una Participation Archived;
- retirar una Participation Completed;
- retirar una Participation Invalidated;
- retirar una Participation Archived;
- invalidar una Participation Withdrawn;
- invalidar una Participation Archived;
- archivar una Participation Registered;
- archivar una Participation Active;
- salir de Archived mediante comportamiento normal;
- inventar transiciones no documentadas;
- utilizar Permissions para bypass de la State Machine;
- utilizar Infrastructure para bypass del Aggregate Root;
- utilizar el Repository para modificar Status directamente;
- utilizar estados de otros Aggregates como ParticipationStatus;
- utilizar estados técnicos como estados del dominio;
- eliminar timestamps históricos válidos durante una transición;
- modificar ParticipationId;
- modificar OrganizationId;
- sustituir arbitrariamente al participante;
- incrementar Version ante una transición rechazada;
- producir Domain Events de éxito ante una transición rechazada;
- persistir parcialmente una transición.

---

# Documentación Complementaria

La State Machine debe interpretarse conjuntamente con:

```text
DOMAIN-008-Aggregate.md

DOMAIN-008A-Lifecycle.md

DOMAIN-008C-Commands.md

DOMAIN-008D-Domain-Events.md

DOMAIN-008E-Invariants.md

DOMAIN-008F-Permissions.md

DOMAIN-008G-Repository-Contract.md

DOMAIN-008H-Examples.md

DOMAIN-008I-Versioning.md

DOMAIN-008J-Consistency-Boundary.md

DOMAIN-008K-Integration-Events.md

DOMAIN-008L-Read-Model.md

DOMAIN-008M-Test-Scenarios.md

DOMAIN-008N-Performance-Rules.md

DOMAIN-008O-Security-Model.md

DOMAIN-008P-Extension-Points.md
```

Cada documento desarrolla una dimensión específica del Aggregate
sin sustituir la autoridad conceptual de esta State Machine sobre
las transiciones de `ParticipationStatus`.

---

# Definición de Éxito

La State Machine del Aggregate **Participation** define
oficialmente todas las transiciones reconocidas entre los estados:

```text
Registered

Active

Completed

Withdrawn

Invalidated

Archived
```

Toda Participation comienza en:

```text
Registered
```

El camino principal es:

```text
Registered

↓

Active

↓

Completed

↓

Archived
```

Los caminos alternativos permiten representar:

```text
Withdrawal

Invalidation
```

sin eliminar ni reescribir la historia del Aggregate.

Toda transición:

- se solicita mediante un Command;
- parte de un estado origen permitido;
- termina en un estado destino definido;
- requiere Permissions válidas;
- preserva Invariants;
- respeta Version;
- mantiene coherencia temporal;
- produce el Domain Event correspondiente cuando se confirma;
- modifica exclusivamente el Aggregate Participation;
- preserva ParticipationId;
- preserva OrganizationId;
- preserva la identidad contextual del participante;
- mantiene la historia de estados anteriores.

Una transición inválida:

```text
Does Not Change State

Does Not Increment Version

Does Not Produce Success Domain Event

Does Not Modify Lifecycle Timestamps
```

Archived constituye el estado terminal de conservación lógica y no
admite transiciones operacionales normales.

De esta forma,
`DOMAIN-008B-State-Machine.md` constituye la definición normativa
oficial de la máquina de estados de **Participation** y proporciona
la base conceptual para Commands, Domain Events, Invariants,
Permissions, Repository Contract, Versioning, Consistency Boundary,
Integration Events, Read Models, Test Scenarios, Performance Rules,
Security Model y Extension Points del Aggregate, manteniendo la
coherencia de la arquitectura DDD consolidada de AURA Core.