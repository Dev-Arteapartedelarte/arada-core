# DOMAIN-009C — Voting Commands

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
- DOMAIN-009D-Domain-Events.md
- DOMAIN-009E-Invariants.md
- DOMAIN-009F-Permissions.md
- DOMAIN-009J-Consistency-Boundary.md

---

# Objetivo

Definir los Commands que representan la intención de modificar
el estado del Aggregate **Voting**.

Los Commands constituyen solicitudes explícitas de comportamiento
del dominio.

Un Command:

- expresa intención;
- utiliza lenguaje imperativo;
- se dirige a una Aggregate Root;
- no representa un hecho consumado;
- no modifica directamente propiedades;
- debe respetar Permissions;
- debe respetar Lifecycle;
- debe respetar State Machine;
- debe respetar Invariants;
- puede producir uno o más Domain Events cuando la operación es
  válida.

Este documento desarrolla exclusivamente los Commands ya definidos
por el modelo conceptual de Voting.

No introduce nuevos estados, transiciones, Events ni capacidades
del Aggregate.

---

# Principios

Los Commands de Voting deben cumplir las siguientes reglas.

- toda modificación comienza mediante una intención explícita;
- Voting es la única Aggregate Root capaz de aceptar la intención;
- ningún Command modifica directamente otro Aggregate;
- ningún Command permite modificar VotingId;
- ningún Command permite modificar OrganizationId;
- ningún Command permite modificar Version directamente;
- ningún Command permite modificar VotingStatus directamente;
- toda operación válida preserva las Invariants;
- toda transición de estado debe pertenecer a la State Machine;
- toda modificación válida incrementa Version;
- toda modificación relevante genera el Domain Event
  correspondiente;
- un Command rechazado no modifica el Aggregate;
- un Command rechazado no incrementa Version;
- un Command rechazado no produce el Domain Event de éxito
  correspondiente.

---

# Estructura General

Conceptualmente, un Command contiene la información necesaria para
expresar una intención sobre un Voting.

```text
Command

VotingId

Required Domain Data
```

Cuando corresponde a creación:

```text
CreateVoting

VotingId

OrganizationId

VotingType

Title

Rules

Context
```

Los datos concretos deben utilizar los Value Objects definidos por
el dominio.

Los Commands no transportan Aggregates externos completos.

---

# Commands Oficiales

La versión 1.0 define los siguientes Commands:

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

Estos Commands corresponden al comportamiento definido en:

```text
DOMAIN-009-Aggregate.md
```

---

# Categorías de Commands

Los Commands pueden agruparse conceptualmente en:

```text
Lifecycle Commands

Configuration Commands
```

Lifecycle Commands:

```text
CreateVoting

OpenVoting

CloseVoting

CancelVoting

ArchiveVoting
```

Configuration Commands:

```text
ChangeVotingType

ChangeVotingTitle

ChangeVotingDescription

ChangeVotingRules

AddVotingOption

RemoveVotingOption
```

Esta agrupación facilita la comprensión del modelo.

No modifica la identidad ni la semántica individual de cada
Command.

---

# CreateVoting

## Objetivo

Crear una nueva instancia válida del Aggregate Voting.

---

## Datos mínimos

```text
VotingId

OrganizationId

VotingType

Title

Rules
```

Cuando el contexto del Voting lo requiera también puede incorporar:

```text
AssemblyId

ProposalId

Description

Options
```

La obligatoriedad de las referencias y datos contextuales depende
de las reglas ya establecidas por el Aggregate.

---

## Precondiciones

Debe cumplirse:

- VotingId es válido;
- VotingId no identifica un Voting existente;
- OrganizationId es válido;
- VotingType es válido;
- Title es válido;
- Rules son válidas;
- Options son coherentes con VotingType y Rules cuando
  correspondan;
- AssemblyId cumple las reglas del contexto cuando corresponda;
- ProposalId cumple las reglas del contexto cuando corresponda;
- todas las Invariants de creación son satisfechas.

---

## Estado origen

```text
No Voting
```

---

## Estado destino

```text
Draft
```

---

## Evento esperado

```text
VotingCreated
```

---

## Resultado

Una creación válida produce conceptualmente:

```text
Voting

VotingId = provided VotingId

OrganizationId = provided OrganizationId

VotingStatus = Draft

Version = 1
```

VotingId y OrganizationId quedan establecidos como identidades
inmutables dentro del Aggregate.

---

# OpenVoting

## Objetivo

Abrir formalmente un Voting que se encuentra preparado para
comenzar su proceso.

---

## Datos mínimos

```text
VotingId
```

---

## Precondiciones

Debe cumplirse:

```text
VotingStatus = Draft
```

Además:

- VotingType debe ser válido;
- Rules deben ser válidas;
- Options deben ser coherentes cuando correspondan;
- la configuración requerida debe encontrarse completa;
- todas las Invariants de apertura deben cumplirse;
- la State Machine debe permitir la transición.

---

## Estado origen

```text
Draft
```

---

## Estado destino

```text
Open
```

---

## Evento esperado

```text
VotingOpened
```

---

## Resultado

Una apertura válida:

- cambia VotingStatus a Open;
- establece OpenedAt;
- incrementa Version;
- actualiza UpdatedAt;
- genera VotingOpened.

Conceptualmente:

```text
Draft

↓

OpenVoting

↓

Open
```

---

# CloseVoting

## Objetivo

Cerrar formalmente un Voting que se encuentra Open.

---

## Datos mínimos

```text
VotingId
```

---

## Precondiciones

Debe cumplirse:

```text
VotingStatus = Open
```

Además:

- las Rules deben permanecer válidas;
- las condiciones requeridas para el cierre deben cumplirse;
- Result debe ser coherente con las reglas del proceso cuando
  corresponda;
- las Invariants de cierre deben cumplirse;
- la State Machine debe permitir la transición.

---

## Estado origen

```text
Open
```

---

## Estado destino

```text
Closed
```

---

## Evento esperado

```text
VotingClosed
```

---

## Resultado

Un cierre válido:

- cambia VotingStatus a Closed;
- establece ClosedAt;
- preserva Result cuando corresponda;
- incrementa Version;
- actualiza UpdatedAt;
- genera VotingClosed.

Conceptualmente:

```text
Open

↓

CloseVoting

↓

Closed
```

---

# CancelVoting

## Objetivo

Cancelar formalmente un Voting cuando el Lifecycle permite
terminar el proceso mediante la ruta de cancelación.

---

## Datos mínimos

```text
VotingId
```

---

## Precondiciones

La versión 1.0 requiere:

```text
VotingStatus = Draft
```

Además:

- la State Machine debe permitir la transición;
- las Invariants correspondientes deben cumplirse.

La versión 1.0 no utiliza CancelVoting para cancelar un Voting que
ya se encuentra Open.

---

## Estado origen

```text
Draft
```

---

## Estado destino

```text
Cancelled
```

---

## Evento esperado

```text
VotingCancelled
```

---

## Resultado

Una cancelación válida:

- cambia VotingStatus a Cancelled;
- establece CancelledAt;
- conserva VotingId;
- conserva OrganizationId;
- conserva la información histórica previa;
- incrementa Version;
- actualiza UpdatedAt;
- genera VotingCancelled.

Cancelar no equivale a eliminar el Aggregate.

---

# ArchiveVoting

## Objetivo

Retirar un Voting finalizado del ciclo operativo y conservarlo
como referencia histórica.

---

## Datos mínimos

```text
VotingId
```

---

## Precondiciones

VotingStatus debe ser:

```text
Closed
```

o:

```text
Cancelled
```

Además:

- la State Machine debe permitir la transición;
- las Invariants correspondientes deben cumplirse.

---

## Estados origen

```text
Closed

Cancelled
```

---

## Estado destino

```text
Archived
```

---

## Evento esperado

```text
VotingArchived
```

---

## Resultado

Un archivado válido:

- cambia VotingStatus a Archived;
- establece ArchivedAt;
- conserva VotingId;
- conserva OrganizationId;
- conserva Rules;
- conserva Options;
- conserva Result cuando exista;
- conserva los timestamps históricos;
- incrementa Version;
- actualiza UpdatedAt;
- genera VotingArchived.

Archived es terminal.

Archivar no equivale a eliminar físicamente el Aggregate.

---

# ChangeVotingType

## Objetivo

Modificar VotingType cuando las reglas vigentes del Aggregate
permitan cambiar la naturaleza formal del Voting.

---

## Datos

```text
VotingId

NewVotingType
```

---

## Precondiciones

Debe cumplirse:

- NewVotingType es válido;
- NewVotingType es diferente del VotingType actual;
- el estado actual permite modificar VotingType;
- Rules permanecen válidas;
- Options permanecen coherentes cuando correspondan;
- todas las Invariants aplicables se mantienen.

La operación no puede utilizarse para modificar VotingStatus.

---

## Estado origen

VotingStatus debe corresponder a un estado en el cual el modelo de
Voting permita modificar su configuración.

La operación no introduce una nueva transición de Lifecycle.

---

## Estado destino

```text
Same VotingStatus
```

---

## Evento esperado

```text
VotingTypeChanged
```

---

## Resultado

Una modificación válida:

```text
Previous VotingType

↓

ChangeVotingType

↓

New VotingType
```

manteniendo:

```text
VotingStatus = Previous VotingStatus
```

y produciendo una nueva Version.

---

# ChangeVotingTitle

## Objetivo

Modificar el Title descriptivo de Voting cuando las reglas del
Aggregate permitan hacerlo.

---

## Datos

```text
VotingId

NewTitle
```

---

## Precondiciones

Debe cumplirse:

- NewTitle es válido;
- NewTitle representa una modificación efectiva;
- el estado actual permite modificar Title;
- todas las Invariants aplicables se mantienen.

---

## Estado origen

VotingStatus debe corresponder a un estado en el cual el modelo
permita modificar la configuración del Voting.

---

## Estado destino

```text
Same VotingStatus
```

---

## Evento esperado

```text
VotingTitleChanged
```

---

## Resultado

```text
Previous Title

↓

ChangeVotingTitle

↓

New Title
```

VotingId permanece inmutable.

OrganizationId permanece inmutable.

VotingStatus no cambia como consecuencia directa de este Command.

---

# ChangeVotingDescription

## Objetivo

Modificar Description cuando el estado y las reglas del Aggregate
permitan actualizar la información descriptiva del Voting.

---

## Datos

```text
VotingId

NewDescription
```

---

## Precondiciones

Debe cumplirse:

- NewDescription cumple las reglas del dominio;
- existe una modificación efectiva;
- el estado actual permite modificar Description;
- las Invariants permanecen válidas.

---

## Estado origen

VotingStatus debe corresponder a un estado en el cual la
modificación se encuentre permitida por el modelo.

---

## Estado destino

```text
Same VotingStatus
```

---

## Evento esperado

```text
VotingDescriptionChanged
```

---

## Resultado

```text
Previous Description

↓

ChangeVotingDescription

↓

New Description
```

La operación no modifica el Lifecycle.

---

# ChangeVotingRules

## Objetivo

Modificar las Rules formales del proceso cuando el estado del
Voting permita realizar dicha modificación.

---

## Datos

```text
VotingId

NewRules
```

---

## Precondiciones

Debe cumplirse:

- NewRules son válidas;
- existe una modificación efectiva;
- VotingStatus permite modificar Rules;
- VotingType permanece compatible con NewRules;
- Options permanecen compatibles con NewRules cuando
  correspondan;
- las Invariants permanecen válidas.

---

## Estado origen

VotingStatus debe corresponder a un estado en el cual el modelo
permita modificar Rules.

---

## Estado destino

```text
Same VotingStatus
```

---

## Evento esperado

```text
VotingRulesChanged
```

---

## Resultado

```text
Previous Rules

↓

ChangeVotingRules

↓

New Rules
```

VotingStatus permanece sin cambios.

Toda modificación válida incrementa Version.

---

# AddVotingOption

## Objetivo

Agregar una VotingOption al proceso cuando VotingType, Rules,
Lifecycle e Invariants permitan incorporar una nueva alternativa.

---

## Datos

```text
VotingId

VotingOption
```

---

## Precondiciones

Debe cumplirse:

- VotingOption es válida;
- VotingOption es compatible con VotingType;
- VotingOption es compatible con Rules;
- la incorporación representa una modificación efectiva;
- el estado actual permite modificar Options;
- las Invariants permanecen válidas.

---

## Estado origen

VotingStatus debe corresponder a un estado en el cual el modelo
permita modificar Options.

---

## Estado destino

```text
Same VotingStatus
```

---

## Evento esperado

```text
VotingOptionAdded
```

---

## Resultado

Conceptualmente:

```text
Current Options

↓

AddVotingOption

↓

Updated Options
```

VotingStatus permanece sin cambios.

La operación modifica exclusivamente el estado interno de Voting.

---

# RemoveVotingOption

## Objetivo

Eliminar una VotingOption existente cuando las reglas del
Aggregate permitan retirar dicha alternativa.

---

## Datos

```text
VotingId

VotingOption
```

---

## Precondiciones

Debe cumplirse:

- VotingOption corresponde a una Option existente;
- la eliminación representa una modificación efectiva;
- VotingStatus permite modificar Options;
- las Options restantes continúan siendo compatibles con
  VotingType;
- las Options restantes continúan siendo compatibles con Rules;
- las Invariants permanecen válidas.

---

## Estado origen

VotingStatus debe corresponder a un estado en el cual el modelo
permita modificar Options.

---

## Estado destino

```text
Same VotingStatus
```

---

## Evento esperado

```text
VotingOptionRemoved
```

---

## Resultado

Conceptualmente:

```text
Current Options

↓

RemoveVotingOption

↓

Updated Options
```

VotingStatus permanece sin cambios.

La operación no modifica ningún Aggregate externo.

---

# Commands y Lifecycle

Los Commands de Lifecycle mantienen la correspondencia oficial:

| Command | Estado origen | Estado destino |
| --- | --- | --- |
| CreateVoting | No existe | Draft |
| OpenVoting | Draft | Open |
| CancelVoting | Draft | Cancelled |
| CloseVoting | Open | Closed |
| ArchiveVoting | Closed | Archived |
| ArchiveVoting | Cancelled | Archived |

Estas transiciones corresponden exactamente a:

```text
DOMAIN-009A-Lifecycle.md
```

---

# Commands y State Machine

Los Commands que producen cambios de VotingStatus deben respetar:

```text
DOMAIN-009B-State-Machine.md
```

Debe mantenerse:

```text
Command

↓

Current VotingStatus

↓

State Machine Validation

↓

Allowed Transition
```

Un Command no puede crear una transición inexistente.

---

# Commands de Configuración

Los Commands:

```text
ChangeVotingType

ChangeVotingTitle

ChangeVotingDescription

ChangeVotingRules

AddVotingOption

RemoveVotingOption
```

representan modificaciones del estado interno que no constituyen
por sí mismas una transición del Lifecycle.

Debe mantenerse:

```text
VotingStatus Before

=

VotingStatus After
```

cuando dichas operaciones son válidas.

La validez de cada modificación depende del estado, Rules e
Invariants correspondientes.

---

# Commands y Domain Events

Cada modificación válida debe mantener correspondencia con el
hecho producido.

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

La definición formal de los eventos pertenece a:

```text
DOMAIN-009D-Domain-Events.md
```

---

# Intención versus Hecho

Debe mantenerse la diferencia:

```text
Command

=

Intent
```

y:

```text
Domain Event

=

Fact
```

Por ejemplo:

```text
OpenVoting
```

representa una solicitud.

Mientras:

```text
VotingOpened
```

representa un hecho ya ocurrido.

Nunca debe utilizarse un Event como sustituto del Command.

---

# Validación

Todo Command debe evaluarse antes de modificar el Aggregate.

Conceptualmente:

```text
Command

↓

Validate Permission

↓

Load Voting

↓

Validate Current State

↓

Validate Command Data

↓

Validate Invariants

↓

Execute Domain Behavior
```

Si alguna condición no se cumple:

```text
Rejected
```

---

# Rechazo de Commands

Un Command debe ser rechazado cuando:

- no posee la información requerida;
- la información proporcionada es inválida;
- el estado actual no permite la operación;
- la State Machine no permite la transición;
- una Invariant sería violada;
- la Permission requerida no se encuentra disponible;
- la operación intenta modificar identidad;
- la operación intenta modificar OrganizationId;
- la operación intenta modificar Version;
- la operación intenta modificar directamente otro Aggregate.

---

# Efecto del Rechazo

Un Command rechazado debe mantener:

```text
Aggregate State = Previous State

Version = Previous Version
```

y no debe producir el Domain Event que represente éxito.

Conceptualmente:

```text
Command

↓

Rejected

↓

No State Change

No Version Increment

No Success Domain Event
```

---

# Commands e Invariants

Ningún Command puede evitar:

```text
DOMAIN-009E-Invariants.md
```

Debe mantenerse:

```text
Permission Granted

+

Valid Command

+

Invariant Violation

=

Rejected
```

Las Invariants permanecen obligatorias independientemente del actor
que solicita la operación.

---

# Commands y Permissions

Los Commands no contienen la decisión de autorización.

Las Permissions determinan quién puede solicitar determinadas
operaciones.

La definición formal pertenece a:

```text
DOMAIN-009F-Permissions.md
```

Debe mantenerse:

```text
Permission Granted

≠

Command Guaranteed
```

La autorización permite continuar hacia la validación del dominio.

No sustituye State Machine ni Invariants.

---

# Commands y Versioning

Una modificación válida incrementa Version.

Conceptualmente:

```text
Version = N

↓

Valid Command

↓

Version = N + 1
```

Un Command rechazado mantiene:

```text
Version = N
```

La definición formal pertenece a:

```text
DOMAIN-009I-Versioning.md
```

---

# Commands y Concurrencia

Un Command debe ejecutarse sobre el estado actual del Aggregate.

Una modificación calculada sobre una versión obsoleta no debe
sobrescribir silenciosamente una modificación confirmada.

Conceptualmente:

```text
Load Voting

Version = N

↓

Execute Command

↓

Persist

↓

Validate Version
```

El control formal de concurrencia pertenece al Repository Contract
y al modelo de Versioning.

---

# Commands y Consistency Boundary

Todo Command modifica únicamente:

```text
Voting
```

dentro de su propio Consistency Boundary.

Un Command de Voting no puede modificar directamente:

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

La definición formal del límite pertenece a:

```text
DOMAIN-009J-Consistency-Boundary.md
```

---

# Referencias Externas

Los Commands pueden utilizar identificadores externos cuando el
comportamiento ya definido por Voting requiera contexto.

Ejemplos:

```text
OrganizationId

AssemblyId

ProposalId
```

Estos identificadores representan referencias.

No transportan ni incorporan Aggregates externos completos dentro
de Voting.

---

# Commands y Assembly

Cuando un Voting posee:

```text
AssemblyId
```

los Commands de Voting continúan modificando exclusivamente Voting.

No pueden:

- abrir Assembly;
- cerrar Assembly;
- cancelar Assembly;
- archivar Assembly;
- modificar su Lifecycle.

---

# Commands y Proposal

Cuando Voting posee:

```text
ProposalId
```

ningún Command de Voting modifica directamente Proposal.

Debe mantenerse:

```text
Voting Command

↓

Voting
```

y no:

```text
Voting Command

↓

Proposal State Mutation
```

---

# Commands y Participation

Los Commands de Voting no representan la participación individual
de Citizens.

Debe mantenerse:

```text
Voting Commands

=

Voting Process Intentions
```

mientras:

```text
Participation Commands

=

Participation Aggregate Intentions
```

Ambos modelos permanecen separados.

---

# Commands y Result

Result pertenece al Aggregate Voting.

Sin embargo, Result no constituye un Command.

Debe mantenerse:

```text
CloseVoting

↓

Valid Domain Behavior

↓

Result when applicable

↓

VotingClosed
```

No debe utilizarse:

```text
SetVotingResult
```

como modificación directa del estado mientras dicho Command no
forme parte del modelo oficial definido para Voting.

Result permanece protegido por el comportamiento e Invariants del
Aggregate.

---

# Commands y Timestamps

Los timestamps del Lifecycle no son modificados directamente por
Commands especializados.

Debe mantenerse:

```text
OpenVoting

↓

OpenedAt
```

```text
CloseVoting

↓

ClosedAt
```

```text
CancelVoting

↓

CancelledAt
```

```text
ArchiveVoting

↓

ArchivedAt
```

No existen Commands para establecer directamente esos timestamps.

---

# Commands y Archived

Cuando:

```text
VotingStatus = Archived
```

los Commands ordinarios de modificación deben ser rechazados.

Archived permanece como estado histórico terminal.

No existe en la versión 1.0:

```text
ReactivateVoting
```

ni:

```text
UnarchiveVoting
```

---

# Commands y Closed

La versión 1.0 no define:

```text
ReopenVoting
```

Por lo tanto un Voting Closed no vuelve a Open mediante un Command
ordinario.

---

# Commands y Cancelled

La versión 1.0 no define:

```text
ReactivateVoting
```

para regresar desde Cancelled hacia Draft u Open.

La incorporación de una capacidad de este tipo requeriría una
evolución explícita del modelo.

---

# Atomicidad

La ejecución válida de un Command debe representar una única
modificación lógica del Aggregate.

Conceptualmente:

```text
Previous Voting

↓

Command

↓

Validate

↓

New Voting

+

New Version

+

Domain Event
```

No puede confirmarse únicamente una parte del cambio.

---

# Consistencia

Al finalizar un Command válido:

```text
Voting
```

debe encontrarse en un estado válido.

Debe preservarse conjuntamente:

- identidad;
- OrganizationId;
- VotingStatus;
- VotingType;
- Rules;
- Options;
- Result cuando corresponda;
- Lifecycle timestamps;
- Version;
- Invariants.

Los Commands no pueden dejar un estado parcialmente válido.

---

# Auditoría

Los Commands no implementan directamente el Aggregate Audit.

La trazabilidad se preserva mediante los hechos producidos por el
dominio.

Conceptualmente:

```text
Command

↓

Voting

↓

Domain Event

↓

Audit Process
```

Audit permanece fuera del Consistency Boundary de Voting.

---

# Integración

Los Commands pertenecen al modelo interno de escritura de Voting.

No constituyen contratos de Integration Events.

Debe mantenerse:

```text
Command

↓

Voting

↓

Domain Event

↓

Integration Event
```

cuando un hecho deba comunicarse fuera del Bounded Context.

Los consumidores externos no ejecutan modificaciones mediante
Domain Events.

---

# Compatibilidad con CQRS

Los Commands pertenecen al Write Side.

Conceptualmente:

```text
Command

↓

Voting Aggregate

↓

Domain Behavior

↓

Domain Event
```

Las consultas pertenecen al Read Side.

No deben representarse mediante Commands.

---

# Compatibilidad con Event Sourcing

Los Commands no forman parte del historial permanente de hechos.

Debe mantenerse:

```text
Command

↓

Decision

↓

Domain Event
```

Los Domain Events representan los hechos históricos.

Replay aplica Events.

No vuelve a ejecutar Commands.

---

# Matriz de Commands

| Command | Tipo | Cambio de VotingStatus |
| --- | --- | --- |
| CreateVoting | Lifecycle | No existe → Draft |
| OpenVoting | Lifecycle | Draft → Open |
| CloseVoting | Lifecycle | Open → Closed |
| CancelVoting | Lifecycle | Draft → Cancelled |
| ArchiveVoting | Lifecycle | Closed → Archived |
| ArchiveVoting | Lifecycle | Cancelled → Archived |
| ChangeVotingType | Configuration | No |
| ChangeVotingTitle | Configuration | No |
| ChangeVotingDescription | Configuration | No |
| ChangeVotingRules | Configuration | No |
| AddVotingOption | Configuration | No |
| RemoveVotingOption | Configuration | No |

---

# Matriz Command / Event

| Command | Event |
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

# Restricciones

No está permitido utilizar Commands para:

- modificar VotingId;
- modificar OrganizationId;
- modificar Version directamente;
- modificar VotingStatus directamente;
- establecer OpenedAt directamente;
- establecer ClosedAt directamente;
- establecer CancelledAt directamente;
- establecer ArchivedAt directamente;
- ejecutar una transición inexistente;
- ejecutar Draft → Closed;
- ejecutar Draft → Archived;
- ejecutar Open → Cancelled;
- ejecutar Open → Archived;
- ejecutar Closed → Open;
- ejecutar Cancelled → Open;
- ejecutar cualquier transición desde Archived;
- modificar otro Aggregate;
- incorporar Aggregates externos completos;
- utilizar Domain Events como Commands;
- utilizar Commands como registro histórico;
- evitar Permissions;
- evitar State Machine;
- evitar Invariants;
- evitar Versioning;
- utilizar el Repository como sustituto del comportamiento del
  Aggregate;
- establecer Result directamente mediante un Command no definido;
- introducir reapertura sin evolución explícita;
- introducir reactivación sin evolución explícita;
- introducir desarchivado sin evolución explícita.

---

# Reglas

## REG-001

Todo Command representa una intención de modificar Voting.

---

## REG-002

Todo Command de modificación se dirige a la Aggregate Root
Voting.

---

## REG-003

Ningún Command puede modificar VotingId.

---

## REG-004

Ningún Command puede modificar OrganizationId.

---

## REG-005

Ningún Command puede modificar Version directamente.

---

## REG-006

VotingStatus solo puede cambiar mediante Commands de Lifecycle
definidos oficialmente.

---

## REG-007

Toda transición solicitada por un Command debe existir en la State
Machine.

---

## REG-008

Todo Command debe preservar las Invariants del Aggregate.

---

## REG-009

Toda modificación válida incrementa Version.

---

## REG-010

Toda modificación relevante genera el Domain Event
correspondiente.

---

## REG-011

Un Command rechazado no modifica el estado del Aggregate.

---

## REG-012

Un Command rechazado no incrementa Version.

---

## REG-013

Un Command rechazado no genera el Domain Event de éxito
correspondiente.

---

## REG-014

Los Commands de configuración no modifican VotingStatus por sí
mismos.

---

## REG-015

Los Commands no pueden modificar directamente otro Aggregate.

---

## REG-016

Los Commands no pueden utilizarse para evitar Permissions,
Lifecycle, State Machine o Invariants.

---

## REG-017

Archived no acepta Commands ordinarios de modificación.

---

## REG-018

La versión 1.0 no define Commands de reapertura, reactivación o
desarchivado.

---

# Definición de Éxito

El Aggregate **Voting** dispone de un conjunto explícito y
coherente de Commands que representan todas las intenciones de
modificación definidas por su modelo conceptual versión 1.0.

Los Commands oficiales son:

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

Los Commands de Lifecycle respetan exactamente las transiciones
establecidas por `DOMAIN-009A-Lifecycle.md` y
`DOMAIN-009B-State-Machine.md`.

Los Commands de configuración modifican únicamente elementos
pertenecientes al Aggregate y no crean por sí mismos nuevas
transiciones de Lifecycle.

Toda operación válida:

- pasa por Voting como Aggregate Root;
- respeta Permissions;
- valida el estado actual;
- preserva las Invariants;
- mantiene VotingId inmutable;
- mantiene OrganizationId inmutable;
- protege VotingStatus;
- protege Version;
- incrementa Version ante modificaciones válidas;
- genera el Domain Event correspondiente;
- permanece dentro del Consistency Boundary de Voting;
- no modifica directamente otros Aggregates.

Toda operación inválida es rechazada sin modificar estado, Version
ni producir el Domain Event de éxito.

De esta forma, `DOMAIN-009C-Commands.md` define el contrato
conceptual de intenciones de escritura del Aggregate **Voting**
manteniendo íntegramente el Lifecycle, State Machine, límites de
consistencia y reglas consolidadas de AURA Core.