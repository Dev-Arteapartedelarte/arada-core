# DOMAIN-009D — Voting Domain Events

Versión: 1.1

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
- DOMAIN-009E-Invariants.md
- DOMAIN-009F-Permissions.md
- DOMAIN-009G-Repository-Contract.md
- DOMAIN-009I-Versioning.md
- DOMAIN-009J-Consistency-Boundary.md
- DOMAIN-009K-Integration-Events.md
- DOMAIN-009L-Read-Model.md
- DOMAIN-009M-Test-Scenarios.md
- DOMAIN-009O-Security-Model.md
- CORE-006-Domain-Invariants.md
- CORE-008-Aggregate-Design-Rules.md
- CORE-011-Repository-Contracts.md

---

# Objetivo

Definir formalmente los **Domain Events** generados y registrados por el
Aggregate **Voting** cuando ocurren hechos relevantes dentro de su
ciclo de vida.

Un Domain Event representa un hecho consumado.

Describe algo que ocurrió efectivamente dentro del dominio y que
ya fue aceptado por la Aggregate Root después de validar:

- estado actual;
- Guards;
- precondiciones;
- permisos correspondientes;
- invariantes;
- consistencia;
- concurrencia.

Los Domain Events permiten representar la evolución de Voting sin
acoplarlo directamente a otros Aggregates, Bounded Contexts,
Infrastructure o sistemas externos.

---

# Propósito

Los Domain Events permiten expresar hechos significativos de Voting
mediante el lenguaje ubicuo de AURA.

Ejemplos:

```text
VotingCreated

VotingOpened

VotingClosed

VotingCancelled

VotingArchived
```

Cada evento expresa algo que ya ocurrió.

Los Domain Events permiten:

- preservar trazabilidad;
- comunicar hechos dentro del dominio;
- desacoplar Aggregates;
- alimentar Read Models;
- iniciar procesos posteriores;
- soportar Audit;
- generar Integration Events;
- mantener compatibilidad con CQRS;
- mantener compatibilidad con Event Sourcing.

---

# Principio Fundamental

Un Domain Event representa:

```text
Fact
```

No representa:

```text
Intent
```

Por lo tanto:

```text
OpenVoting
```

es un Command.

Mientras:

```text
VotingOpened
```

es un Domain Event.

La relación conceptual es:

```text
Command
    │
    ▼
Voting
    │
    ├── valida estado
    ├── valida Guards
    ├── valida invariantes
    └── ejecuta comportamiento
            │
            ▼
        Domain Event
```

El Domain Event solamente existe cuando el hecho ocurrió
realmente.

---

# Commands versus Domain Events

Los Commands expresan intención en forma imperativa.

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

Los Domain Events expresan hechos consumados en pasado.

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

Nunca debe utilizarse:

```text
VotingOpened
```

como solicitud de apertura.

Tampoco debe utilizarse:

```text
OpenVoting
```

como registro histórico de una votación abierta.

---

# Propiedad del Evento

Los Domain Events definidos en este documento pertenecen
conceptualmente al Aggregate:

```text
Voting
```

La Aggregate Root es responsable de producirlos cuando sus
operaciones modifican válidamente el estado del dominio.

Otros Aggregates pueden reaccionar posteriormente a estos hechos,
pero no son propietarios del evento original.

---

# Alcance

Los eventos de Voting describen exclusivamente hechos
pertenecientes al Aggregate.

No representan directamente hechos internos de:

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

Cuando un hecho pertenece a otro Aggregate debe ser producido por
el Aggregate responsable.

---

# Eventos Oficiales

La versión 1.0 define los siguientes Domain Events:

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

Estos eventos corresponden exactamente a los hechos definidos por
el Aggregate, Lifecycle, State Machine y Commands de Voting.

No se incorporan eventos adicionales en esta versión.

---

# Categorías de Eventos

Los Domain Events pueden agruparse conceptualmente en:

```text
Lifecycle Events

Configuration Events

Option Events
```

Esta agrupación facilita su comprensión.

No modifica la identidad ni la semántica individual de los
eventos.

---

# Lifecycle Events

Representan cambios significativos en el ciclo de vida de Voting.

```text
VotingCreated

VotingOpened

VotingClosed

VotingCancelled

VotingArchived
```

---

# Configuration Events

Representan modificaciones válidas sobre la configuración de
Voting.

```text
VotingTypeChanged

VotingTitleChanged

VotingDescriptionChanged

VotingRulesChanged
```

---

# Option Events

Representan modificaciones válidas sobre las Options pertenecientes
al Voting.

```text
VotingOptionAdded

VotingOptionRemoved
```

---

# Estructura General

Todo Domain Event de Voting debe contener, como mínimo:

```text
EventId

EventType

VotingId

OrganizationId

AggregateVersion

OccurredAt

CorrelationId

CausationId
```

Puede incorporar campos adicionales según el hecho representado.

Cuando corresponda puede incorporar:

```text
ActorId
```

como referencia al actor relacionado con la intención aceptada.

El evento no contiene el Aggregate completo del Actor.

---

# EventId

Identificador único del Domain Event.

```text
EventId
```

Debe:

- ser único;
- ser inmutable;
- identificar un único hecho;
- no reutilizarse;
- permitir trazabilidad;
- ser independiente de VotingId.

Dos hechos distintos nunca deben compartir EventId.

---

# EventType

Representa el nombre semántico del hecho ocurrido.

Ejemplo:

```text
VotingOpened
```

EventType utiliza el lenguaje ubicuo del dominio.

No debe contener nombres de:

- tablas;
- endpoints;
- frameworks;
- brokers;
- tecnologías;
- acciones técnicas.

---

# VotingId

Identifica el Voting que produjo el hecho.

```text
VotingId
```

VotingId relaciona el evento con la Aggregate Root.

Permanece inmutable.

---

# OrganizationId

Identifica la Organization propietaria de Voting al momento del
evento.

```text
OrganizationId
```

Como OrganizationId es inmutable dentro de Voting, permite
preservar el contexto organizacional del hecho.

El evento no contiene el Aggregate Organization completo.

---

# AggregateVersion

Representa la Version de Voting resultante de la modificación que
produjo el evento.

```text
AggregateVersion
```

Conceptualmente:

```text
BeforeVersion = N

Command accepted

AfterVersion = N + 1

DomainEvent.AggregateVersion = N + 1
```

AggregateVersion permite:

- ordenar hechos del mismo Aggregate;
- detectar inconsistencias;
- reconstruir evolución;
- mantener trazabilidad;
- soportar Event Sourcing cuando corresponda.

---

# OccurredAt

Representa el momento en que el hecho de dominio ocurrió.

```text
OccurredAt
```

Debe diferenciarse conceptualmente del momento en que fue recibida
la intención que originó la operación.

El primero representa el hecho consumado.

El segundo representa la intención.

---

# CorrelationId

Permite relacionar el evento con el flujo al cual pertenece.

```text
CorrelationId
```

Puede mantenerse desde la intención que originó la operación.

Conceptualmente:

```text
Command

↓

Domain Event

↓

Integration Event

↓

External Process
```

CorrelationId no modifica el estado del Aggregate.

---

# CausationId

Identifica la intención o hecho que causó el Domain Event.

```text
CausationId
```

Conceptualmente:

```text
Command

↓

Voting Domain Event
```

CausationId permite mantener trazabilidad causal.

No modifica el comportamiento del Aggregate.

---

# ActorId

Cuando corresponda, un Domain Event puede conservar:

```text
ActorId
```

como referencia al actor relacionado con la operación aceptada.

ActorId:

- representa una referencia;
- no contiene el Aggregate Citizen;
- no contiene Membership;
- no contiene Role;
- no incorpora identidad externa completa dentro de Voting.

---

# Event Payload

Cada Domain Event contiene únicamente la información necesaria
para representar el hecho ocurrido.

No debe transportar automáticamente una copia completa de:

```text
Voting
```

Debe mantenerse:

```text
minimum meaningful payload
```

El Payload debe permitir comprender el hecho sin romper
innecesariamente el encapsulamiento del Aggregate.

---

# Inmutabilidad

Los Domain Events son inmutables.

Una vez producido:

```text
VotingOpened
```

no puede modificarse posteriormente para representar otro hecho.

Si Voting cambia nuevamente debe producirse el evento
correspondiente.

Ejemplo:

```text
VotingTitleChanged

↓

VotingTitleChanged
```

puede representar dos hechos distintos ocurridos en momentos y
Version diferentes.

El primer evento no se modifica retroactivamente.

---

# Historicidad

Los eventos preservan los hechos anteriores.

Si Voting produce:

```text
VotingCreated
```

posteriormente:

```text
VotingOpened
```

luego:

```text
VotingClosed
```

y finalmente:

```text
VotingArchived
```

todos los hechos permanecen verdaderos.

La secuencia representa:

```text
el Voting fue creado,

posteriormente fue abierto,

después fue cerrado,

y finalmente fue archivado.
```

No significa que los estados anteriores nunca hayan existido.

Los Domain Events no reescriben el pasado.

---

# VotingCreated

## Definición

Representa el hecho de que un nuevo Voting fue creado válidamente
dentro del dominio.

---

## Command origen

```text
CreateVoting
```

---

## Estado previo

No existe Aggregate.

---

## Estado resultante

```text
Draft
```

---

## Payload mínimo

```text
VotingId

OrganizationId

VotingType

Title

VotingStatus

CreatedAt
```

Cuando formen parte de la creación inicial puede incorporar:

```text
AssemblyId

ProposalId
```

---

## Invariantes

Antes de producir el evento debe haberse validado:

- VotingId válido;
- VotingId único;
- OrganizationId válido;
- VotingType válido;
- Title válido;
- Rules válidas;
- Options coherentes cuando correspondan;
- referencias contextuales válidas cuando correspondan;
- Invariants iniciales satisfechas.

---

## Significado

```text
VotingCreated
```

significa:

```text
Voting existe formalmente dentro del dominio.
```

No significa:

```text
Voting está abierto.
```

Tampoco significa:

```text
Voting fue cerrado.
```

---

# VotingOpened

## Definición

Representa el hecho de que un Voting Draft fue abierto
formalmente.

---

## Command origen

```text
OpenVoting
```

---

## Estado previo

```text
Draft
```

---

## Estado resultante

```text
Open
```

---

## Payload mínimo

```text
VotingId

OrganizationId

PreviousStatus

OpenedAt
```

Cuando sea necesario para representar el contexto del hecho puede
incorporar referencias ya pertenecientes a Voting.

---

## Invariantes

Antes de producir el evento debe haberse validado:

- VotingStatus = Draft;
- VotingType válido;
- Rules válidas;
- Options coherentes cuando correspondan;
- configuración requerida completa;
- Invariants de apertura satisfechas;
- transición permitida por la State Machine.

---

## Significado

```text
VotingOpened
```

significa:

```text
el proceso formal de Voting comenzó.
```

No significa:

```text
Assembly fue abierta.
```

No significa:

```text
Proposal fue modificada.
```

No significa:

```text
Participation fue activada.
```

---

# VotingClosed

## Definición

Representa el hecho de que un Voting Open finalizó formalmente su
flujo normal.

---

## Command origen

```text
CloseVoting
```

---

## Estado previo

```text
Open
```

---

## Estado resultante

```text
Closed
```

---

## Payload mínimo

```text
VotingId

OrganizationId

PreviousStatus

OpenedAt

ClosedAt
```

Cuando corresponda puede incorporar:

```text
Result
```

si forma parte del hecho formal de cierre definido por Voting.

---

## Invariantes

Antes de producir el evento debe haberse validado:

- VotingStatus = Open;
- OpenedAt existente;
- ClosedAt temporalmente coherente;
- Rules válidas;
- condiciones de cierre satisfechas;
- Result coherente cuando corresponda;
- transición permitida por la State Machine;
- Invariants de cierre satisfechas.

---

## Significado

```text
VotingClosed
```

representa el cierre normal del proceso de Voting.

No implica automáticamente:

- archivado;
- modificación de Assembly;
- modificación de Proposal;
- finalización de Participation;
- creación de Document;
- envío de Notification;
- modificación de otro Aggregate.

Estos procesos permanecen separados.

---

# VotingCancelled

## Definición

Representa el hecho de que un Voting fue cancelado mediante la
ruta de cancelación definida por la versión 1.0.

---

## Command origen

```text
CancelVoting
```

---

## Estado previo

```text
Draft
```

---

## Estado resultante

```text
Cancelled
```

---

## Payload mínimo

```text
VotingId

OrganizationId

PreviousStatus

CancelledAt
```

---

## Invariantes

Antes de producir el evento debe haberse validado:

```text
VotingStatus = Draft
```

y:

- transición permitida por la State Machine;
- Invariants de cancelación satisfechas.

---

## Preservación Histórica

El evento no elimina información anterior del Aggregate.

Voting conserva:

- VotingId;
- OrganizationId;
- VotingType;
- contexto;
- Rules;
- Options;
- CreatedAt;
- Version;
- hechos anteriores.

---

## Significado

```text
VotingCancelled
```

significa:

```text
el Voting terminó mediante la ruta de cancelación.
```

No significa:

```text
Voting fue eliminado.
```

Tampoco significa:

```text
Voting fue archivado.
```

---

## Restricción

La versión 1.0 no utiliza:

```text
VotingCancelled
```

para representar la interrupción de un Voting que ya se encuentra:

```text
Open
```

Dicho escenario no forma parte del Lifecycle ni de la State
Machine actuales.

---

# VotingArchived

## Definición

Representa el hecho de que un Voting fue retirado del ciclo
operativo y pasó a su estado histórico terminal.

---

## Command origen

```text
ArchiveVoting
```

---

## Estados previos permitidos

```text
Closed

Cancelled
```

---

## Estado resultante

```text
Archived
```

---

## Payload mínimo

```text
VotingId

OrganizationId

PreviousStatus

ArchivedAt
```

---

## Preservación Histórica

El evento no elimina los hechos anteriores.

Cuando el estado previo es:

```text
Closed
```

permanecen:

```text
OpenedAt

ClosedAt

Result
```

cuando correspondan.

Cuando el estado previo es:

```text
Cancelled
```

permanece:

```text
CancelledAt
```

---

## Significado

Archived no significa eliminación física.

El Aggregate conserva:

- VotingId;
- OrganizationId;
- contexto;
- historial;
- Rules;
- Options;
- Result cuando exista;
- timestamps;
- Version;
- eventos históricos.

---

# VotingTypeChanged

## Definición

Representa el hecho de que VotingType fue modificado válidamente.

---

## Command origen

```text
ChangeVotingType
```

---

## Estado

La operación no constituye por sí misma una transición del
Lifecycle.

Debe mantenerse:

```text
Previous VotingStatus

=

Resulting VotingStatus
```

---

## Payload mínimo

```text
VotingId

OrganizationId

PreviousVotingType

NewVotingType
```

---

## Invariantes

Antes de producir el evento debe haberse validado:

- NewVotingType válido;
- modificación efectiva;
- estado compatible con la operación;
- Rules compatibles;
- Options compatibles cuando correspondan;
- Invariants satisfechas.

---

## Significado

El evento representa un cambio real de VotingType.

No modifica:

```text
VotingId

OrganizationId

VotingStatus
```

---

# VotingTitleChanged

## Definición

Representa el hecho de que Title fue modificado válidamente.

---

## Command origen

```text
ChangeVotingTitle
```

---

## Estado

VotingStatus permanece sin cambios.

---

## Payload mínimo

```text
VotingId

OrganizationId

PreviousTitle

NewTitle
```

---

## Invariantes

Antes de producir el evento debe haberse validado:

- NewTitle válido;
- modificación efectiva;
- estado compatible con la modificación;
- Invariants satisfechas.

---

## Significado

```text
VotingTitleChanged
```

representa una modificación descriptiva del Voting.

No constituye cambio de identidad.

VotingId permanece inmutable.

---

# VotingDescriptionChanged

## Definición

Representa el hecho de que Description fue modificada válidamente.

---

## Command origen

```text
ChangeVotingDescription
```

---

## Estado

VotingStatus permanece sin cambios.

---

## Payload mínimo

```text
VotingId

OrganizationId

PreviousDescription

NewDescription
```

---

## Invariantes

Antes de producir el evento debe haberse validado:

- NewDescription válida;
- modificación efectiva;
- estado compatible con la operación;
- Invariants satisfechas.

---

## Significado

El evento registra una modificación real de la información
descriptiva del Voting.

No modifica identidad, OrganizationId ni Lifecycle.

---

# VotingRulesChanged

## Definición

Representa el hecho de que las Rules de Voting fueron modificadas
válidamente.

---

## Command origen

```text
ChangeVotingRules
```

---

## Estado

VotingStatus permanece sin cambios.

---

## Payload mínimo

```text
VotingId

OrganizationId

PreviousRules

NewRules
```

---

## Invariantes

Antes de producir el evento debe haberse validado:

- NewRules válidas;
- modificación efectiva;
- estado compatible con la modificación;
- VotingType compatible;
- Options compatibles cuando correspondan;
- Invariants satisfechas.

---

## Significado

```text
VotingRulesChanged
```

representa una modificación formal de las reglas pertenecientes al
Voting.

No modifica directamente:

```text
Assembly

Proposal

Participation
```

---

# VotingOptionAdded

## Definición

Representa el hecho de que una VotingOption fue incorporada
válidamente a Voting.

---

## Command origen

```text
AddVotingOption
```

---

## Estado

VotingStatus permanece sin cambios.

---

## Payload mínimo

```text
VotingId

OrganizationId

VotingOption
```

---

## Invariantes

Antes de producir el evento debe haberse validado:

- VotingOption válida;
- compatibilidad con VotingType;
- compatibilidad con Rules;
- modificación efectiva;
- estado compatible con la operación;
- Invariants satisfechas.

---

## Significado

```text
VotingOptionAdded
```

representa que una alternativa válida pasó a formar parte de las
Options del Voting.

No representa:

```text
Participation
```

ni un hecho interno de otro Aggregate.

---

# VotingOptionRemoved

## Definición

Representa el hecho de que una VotingOption existente fue retirada
válidamente de Voting.

---

## Command origen

```text
RemoveVotingOption
```

---

## Estado

VotingStatus permanece sin cambios.

---

## Payload mínimo

```text
VotingId

OrganizationId

VotingOption
```

---

## Invariantes

Antes de producir el evento debe haberse validado:

- VotingOption existente;
- modificación efectiva;
- estado compatible con la operación;
- Options restantes compatibles con VotingType;
- Options restantes compatibles con Rules;
- Invariants satisfechas.

---

## Significado

```text
VotingOptionRemoved
```

preserva el hecho de que una alternativa previamente perteneciente
al Voting fue posteriormente retirada.

El evento anterior que hubiera representado su incorporación no se
reescribe.

---

# Relación entre Eventos y State Machine

Los eventos de Lifecycle deben ser coherentes con:

```text
DOMAIN-009B-State-Machine.md
```

Relación oficial:

| Evento | Estado previo | Estado resultante |
| --- | --- | --- |
| VotingCreated | No existe | Draft |
| VotingOpened | Draft | Open |
| VotingClosed | Open | Closed |
| VotingCancelled | Draft | Cancelled |
| VotingArchived | Closed | Archived |
| VotingArchived | Cancelled | Archived |

Los eventos de configuración y Options pueden mantener el mismo
VotingStatus cuando la operación correspondiente sea válida.

---

# Evento y Cambio de Estado

No todo Domain Event implica una transición del Lifecycle.

Por ejemplo:

```text
VotingTitleChanged
```

puede ocurrir conceptualmente como:

```text
Draft

↓

Draft
```

cuando el estado permita la modificación.

Igualmente:

```text
VotingRulesChanged
```

puede mantener el mismo VotingStatus.

El evento representa un hecho relevante incluso cuando
VotingStatus permanece sin cambios.

---

# Eventos y Lifecycle

Los eventos de transición deben preservar exactamente la semántica
definida en:

```text
DOMAIN-009A-Lifecycle.md
```

Por ejemplo:

```text
VotingClosed
```

significa que Voting terminó formalmente su flujo normal.

No significa que fue archivado.

```text
VotingArchived
```

representa un hecho posterior diferente.

---

# Eventos y Commands

Cada Domain Event debe mantener correspondencia semántica con el
Command o comportamiento que originó el hecho.

La definición de Commands pertenece a:

```text
DOMAIN-009C-Commands.md
```

Relación oficial:

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

Command y Domain Event deben permanecer semánticamente
coherentes.

---

# Eventos e Invariants

Ningún Domain Event puede representar un estado que viole:

```text
DOMAIN-009E-Invariants.md
```

Por ejemplo:

```text
VotingClosed
```

no puede producirse si:

```text
VotingStatus != Open
```

Tampoco puede producirse:

```text
VotingOpened
```

cuando las condiciones requeridas para apertura no se encuentran
satisfechas.

---

# Eventos y Permissions

Las Permissions determinan quién puede provocar indirectamente un
hecho mediante Commands autorizados.

La definición pertenece a:

```text
DOMAIN-009F-Permissions.md
```

Los Domain Events no constituyen solicitudes de autorización.

Representan hechos posteriores a la autorización y validación
correspondientes.

---

# Eventos y Versioning

Todo Domain Event debe mantener relación coherente con:

```text
DOMAIN-009I-Versioning.md
```

Cada modificación válida incrementa Version.

El evento producido representa la nueva:

```text
AggregateVersion
```

Conceptualmente:

```text
Version N

↓

Valid Command

↓

Version N + 1

↓

Domain Event
AggregateVersion = N + 1
```

---

# Versionado de Eventos

Cada evento debe relacionarse con una Version concreta del
Aggregate.

Ejemplo conceptual:

```text
VotingCreated
AggregateVersion = 1

VotingOpened
AggregateVersion = 2

VotingClosed
AggregateVersion = 3

VotingArchived
AggregateVersion = 4
```

La numeración concreta depende de todas las modificaciones válidas
que hayan ocurrido entre estos hechos.

Dos hechos distintos del mismo Voting no representan la misma
modificación del Aggregate.

---

# Orden de Eventos

Dentro de un mismo Voting:

```text
AggregateVersion
```

representa el orden lógico de evolución del Aggregate.

Conceptualmente:

```text
Version N
Domain Event A

Version N + 1
Domain Event B

Version N + 2
Domain Event C
```

OccurredAt aporta información temporal.

AggregateVersion preserva el orden lógico de evolución del
Aggregate.

---

# Eventos y Concurrencia

Un Domain Event correspondiente a una modificación válida solamente
puede representar una operación confirmable según el modelo de
concurrencia.

Conceptualmente:

```text
PersistedVersion = N + 1

ExpectedVersion = N
```

cuando la operación fue calculada sobre una Version obsoleta,
debe producirse el conflicto correspondiente.

No debe confirmarse un nuevo Domain Event de éxito para una
modificación concurrente rechazada.

---

# Eventos y Consistency Boundary

Los Domain Events comunican hechos únicamente dentro de Voting Management
sin expandir su Consistency Boundary. Todo efecto externo requiere un
Integration Event definido en DOMAIN-009K.

La definición del límite pertenece a:

```text
DOMAIN-009J-Consistency-Boundary.md
```

Debe mantenerse:

```text
Voting

↓

Domain Event
```

sin convertir en parte del Aggregate:

```text
Assembly

Proposal

Participation

Organization
```

---

# Eventos y Integration Events

Los Domain Events que deban cruzar Bounded Contexts pueden dar
origen a Integration Events según:

```text
DOMAIN-009K-Integration-Events.md
```

Domain Event e Integration Event representan contratos diferentes.

Debe mantenerse:

```text
Domain Event

≠

Integration Event
```

Un Domain Event pertenece al modelo interno del dominio.

Un Integration Event pertenece al contrato de comunicación entre
contextos.

No todo Domain Event necesita convertirse en Integration Event.

Solo deben exponerse externamente los hechos requeridos por los
contratos correspondientes.

---

# Eventos y Read Model

Las proyecciones definidas en:

```text
DOMAIN-009L-Read-Model.md
```

pueden consumir Domain Events únicamente para actualizar vistas derivadas
de Voting Management.

Conceptualmente:

```text
Domain Event

↓

Projection

↓

Voting Read Model
```

El Read Model no modifica el evento original.

Tampoco modifica el Aggregate.

---

# Eventos y Test Scenarios

Los escenarios definidos en:

```text
DOMAIN-009M-Test-Scenarios.md
```

deben verificar la producción correcta de Domain Events.

Como mínimo deben comprobar:

- evento correcto para cada Command válido;
- ausencia del evento de éxito para Commands rechazados;
- AggregateVersion correcta;
- estado resultante correcto;
- Payload coherente;
- preservación del historial.

---

# Eventos y Security Model

Las reglas definidas en:

```text
DOMAIN-009O-Security-Model.md
```

deben preservar la integridad de los Domain Events.

Un evento no puede utilizarse para evitar:

- Permissions;
- State Machine;
- Invariants;
- Versioning;
- Consistency Boundary.

---

# Eventos Rechazados

Cuando un Command es rechazado:

```text
Command

↓

Rejected
```

no debe producirse el Domain Event que represente éxito.

Ejemplo:

```text
VotingStatus = Closed

OpenVoting
```

Resultado:

```text
Rejected
```

No debe existir:

```text
VotingOpened
```

Version permanece sin cambios.

---

# Eventos Duplicados

Dos eventos con EventId distintos pueden representar dos hechos
reales del mismo tipo.

Por ejemplo:

```text
VotingTitleChanged
```

puede ocurrir más de una vez durante la vida del Aggregate cuando
las reglas permitan cada modificación.

Cada hecho posee:

```text
EventId
```

propio y:

```text
AggregateVersion
```

propia.

Esto es diferente de procesar nuevamente el mismo evento con el
mismo EventId.

---

# Nombres de Eventos

Los Domain Events utilizan nombres conceptualmente equivalentes a:

```text
Aggregate + PastTenseFact
```

Ejemplos:

```text
VotingCreated

VotingOpened

VotingClosed
```

No deben utilizarse nombres técnicos como:

```text
VotingRowUpdated

VotingSavedToDatabase

VotingHttpProcessed

VotingCacheRefreshed
```

Los nombres deben expresar hechos del dominio.

---

# Granularidad de Eventos

Un Domain Event representa un hecho con significado propio dentro
del lenguaje ubicuo.

Debe evitarse un evento genérico como:

```text
VotingUpdated
```

cuando el modelo conoce específicamente:

```text
VotingTypeChanged

VotingTitleChanged

VotingDescriptionChanged

VotingRulesChanged

VotingOptionAdded

VotingOptionRemoved
```

La granularidad debe permanecer alineada con los Commands
oficiales.

---

# Eventos Técnicos Prohibidos

No pertenecen al Aggregate Domain Events como:

```text
VotingSaved

VotingLoaded

VotingCacheMissed

VotingMessagePublished

VotingDatabaseUpdated

VotingHttpRequestCompleted

VotingFIWARESynced
```

Estos representan hechos técnicos.

No representan hechos propios del dominio Voting.

---

# Eventos no Definidos

La versión 1.0 no define Domain Events como:

```text
VotingReopened

VotingReactivated

VotingSuspended

VotingResumed

VotingInterrupted

VotingDeleted

VotingUnarchived
```

porque dichos comportamientos, estados o Commands no forman parte
del modelo oficial actual.

Tampoco define un evento para cancelar Voting desde Open porque esa
transición no pertenece a la State Machine versión 1.0.

Estos eventos no deben introducirse aisladamente.

---

# Result no es Domain Event

```text
Result
```

es información perteneciente a Voting.

No constituye por sí mismo un nuevo Domain Event dentro del modelo
actual.

El cierre formal continúa representándose mediante:

```text
VotingClosed
```

cuando CloseVoting completa válidamente el proceso.

No debe introducirse un evento adicional de Result sin una
evolución explícita del modelo.

---

# Option no es Aggregate Event Externo

```text
VotingOptionAdded

VotingOptionRemoved
```

representan hechos internos de Voting.

VotingOption no adquiere por ello:

- Aggregate Root independiente;
- Repository independiente;
- Lifecycle independiente;
- Version independiente.

Los eventos pertenecen a Voting.

---

# Relación con Otros Aggregates

Los Domain Events de Voting pueden ser observados por otros
procesos.

Sin embargo, un evento de Voting no modifica directamente:

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

Cada Aggregate conserva su propio Consistency Boundary.

---

# VotingClosed y Proposal

```text
VotingClosed
```

no significa automáticamente:

```text
Proposal Approved
```

ni:

```text
Proposal Rejected
```

Proposal mantiene sus propias reglas y Lifecycle.

Cualquier reacción posterior pertenece al proceso responsable de
coordinar los Aggregates.

---

# VotingClosed y Assembly

```text
VotingClosed
```

no significa:

```text
Assembly Closed
```

Assembly y Voting poseen Lifecycles independientes.

---

# VotingOpened y Participation

```text
VotingOpened
```

no significa automáticamente:

```text
Participation Activated
```

Participation mantiene su propio Lifecycle y sus propias
Invariants.

---

# VotingArchived y Eliminación

```text
VotingArchived
```

no representa eliminación física.

Representa:

```text
Historical Preservation
```

El hecho de archivado permanece como parte del historial del
Aggregate.

---

# Auditoría

Los Domain Events proporcionan hechos utilizables por los procesos
de Audit.

Un evento puede aportar:

```text
EventId

EventType

VotingId

OrganizationId

ActorId

AggregateVersion

OccurredAt

CorrelationId

CausationId
```

según corresponda.

Audit mantiene su propio modelo y no modifica el Domain Event
original.

---

# Trazabilidad Causal

Conceptualmente:

```text
Command

OpenVoting

    │

    ▼

VotingOpened
```

El Domain Event puede mantener:

```text
CausationId
```

relacionado con la intención que produjo el hecho.

Y:

```text
CorrelationId
```

para preservar la relación con el flujo correspondiente.

Esta trazabilidad no incorpora Infrastructure dentro del
Aggregate.

---

# Ejemplo de Flujo Normal

```text
CreateVoting
      │
      ▼
VotingCreated
      │
      ▼
Status = Draft

OpenVoting
      │
      ▼
VotingOpened
      │
      ▼
Status = Open

CloseVoting
      │
      ▼
VotingClosed
      │
      ▼
Status = Closed

ArchiveVoting
      │
      ▼
VotingArchived
      │
      ▼
Status = Archived
```

Cada evento preserva un hecho diferente.

---

# Ejemplo de Flujo Cancelado

```text
CreateVoting
      │
      ▼
VotingCreated
      │
      ▼
Status = Draft

CancelVoting
      │
      ▼
VotingCancelled
      │
      ▼
Status = Cancelled

ArchiveVoting
      │
      ▼
VotingArchived
      │
      ▼
Status = Archived
```

La secuencia preserva todos los hechos ocurridos.

---

# Ejemplo de Cambio de Configuración

Estado inicial:

```text
VotingStatus = Draft

VotingTitle = Title A
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

VotingTitle = Title B
```

Evento:

```text
VotingTitleChanged
```

El estado del Lifecycle permanece Draft.

Version incrementa por existir una modificación válida.

---

# Ejemplo de Option Agregada

Estado inicial:

```text
VotingStatus = Draft

Options = Existing Options
```

Command:

```text
AddVotingOption
```

Resultado:

```text
VotingStatus = Draft

Options = Updated Options
```

Evento:

```text
VotingOptionAdded
```

La operación no crea un nuevo Aggregate.

---

# Ejemplo de Evento Rechazado

Estado:

```text
VotingStatus = Closed
```

Command:

```text
OpenVoting
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

# Ejemplo de Evento con Actor

```text
VotingCancelled
```

puede contener conceptualmente:

```text
EventId

VotingId

OrganizationId

ActorId

PreviousStatus

CancelledAt

AggregateVersion

OccurredAt

CorrelationId

CausationId
```

ActorId referencia al actor relacionado con la intención aceptada.

No contiene su perfil completo.

---

# Regla para Incorporar un Nuevo Domain Event

Un nuevo Domain Event solo puede incorporarse mediante una
evolución explícita del modelo cuando represente un hecho relevante
del dominio Voting.

Debe mantener coherencia con:

```text
DOMAIN-009-Aggregate.md

DOMAIN-009A-Lifecycle.md

DOMAIN-009B-State-Machine.md

DOMAIN-009C-Commands.md

DOMAIN-009D-Domain-Events.md

DOMAIN-009E-Invariants.md
```

y con los documentos posteriores afectados cuando corresponda.

No debe agregarse un evento aisladamente rompiendo la coherencia
del Aggregate.

---

# Restricciones

No está permitido:

- utilizar Domain Events como Commands;
- utilizar Commands como hechos históricos;
- producir un evento para una operación rechazada;
- producir un evento que represente una transición inexistente;
- producir un evento que viole Invariants;
- producir un evento con AggregateVersion incoherente;
- modificar retroactivamente un evento;
- reutilizar EventId;
- modificar VotingId mediante un evento;
- modificar OrganizationId mediante un evento;
- transportar automáticamente el Aggregate completo;
- incorporar Aggregates externos completos en el Payload;
- utilizar eventos técnicos como Domain Events;
- utilizar un Domain Event para modificar directamente otro
  Aggregate;
- utilizar VotingClosed como equivalente a VotingArchived;
- utilizar VotingCancelled como equivalente a eliminación;
- utilizar VotingArchived como eliminación física;
- introducir VotingReopened sin evolución explícita;
- introducir VotingReactivated sin evolución explícita;
- introducir VotingUnarchived sin evolución explícita;
- introducir eventos de estados inexistentes;
- introducir un evento adicional de Result sin evolución explícita
  del modelo.

---

# Reglas

## REG-001

Todo Domain Event representa un hecho consumado.

---

## REG-002

Todo Domain Event pertenece conceptualmente al Aggregate Voting.

---

## REG-003

Todo Domain Event debe poseer un EventId único e inmutable.

---

## REG-004

Todo Domain Event debe identificar el Voting mediante VotingId.

---

## REG-005

Todo Domain Event debe preservar OrganizationId como contexto
organizacional del hecho.

---

## REG-006

Todo Domain Event debe corresponder a una AggregateVersion
concreta.

---

## REG-007

Todo Domain Event debe registrar OccurredAt.

---

## REG-008

Los Domain Events son inmutables.

---

## REG-009

Un Command rechazado no produce el Domain Event de éxito
correspondiente.

---

## REG-010

Un Domain Event de Lifecycle solo puede existir como resultado de
una transición permitida por la State Machine.

---

## REG-011

Ningún Domain Event puede representar un estado que viole las
Invariants.

---

## REG-012

Los Domain Events no modifican directamente otros Aggregates.

---

## REG-013

Los eventos históricos no se reescriben para reflejar cambios
posteriores.

---

## REG-014

El Payload debe contener únicamente información necesaria para
representar el hecho.

---

## REG-015

Los Domain Events no constituyen contratos de integración externa.

---

## REG-016

Los eventos de configuración no modifican VotingStatus cuando el
Command correspondiente no representa una transición de
Lifecycle.

---

## REG-017

VotingArchived representa preservación histórica y no eliminación
física.

---

## REG-018

No pueden incorporarse nuevos Domain Events sin mantener coherencia
con Aggregate, Lifecycle, State Machine, Commands e Invariants.

---

# Definición de Éxito

Los Domain Events del Aggregate **Voting** constituyen la
representación oficial de los hechos relevantes ocurridos dentro
de su Consistency Boundary.

La versión 1.0 define:

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

Cada evento:

- representa un hecho consumado;
- pertenece a Voting;
- utiliza el lenguaje ubicuo;
- mantiene EventId;
- identifica VotingId;
- preserva OrganizationId;
- mantiene AggregateVersion;
- registra OccurredAt;
- puede preservar correlación y causalidad;
- mantiene un Payload mínimo y significativo;
- permanece inmutable;
- respeta Lifecycle;
- respeta State Machine;
- respeta Commands;
- respeta Invariants;
- no modifica directamente otros Aggregates.

Los eventos de Lifecycle mantienen exactamente las transiciones:

```text
No Voting → Draft

Draft → Open

Draft → Cancelled

Open → Closed

Closed → Archived

Cancelled → Archived
```

Los eventos de configuración y Options representan modificaciones
válidas sin introducir nuevas transiciones de Lifecycle.

Los Domain Events preservan la historia de Voting sin reescribir
hechos anteriores y permiten que otros procesos reaccionen
posteriormente sin ampliar el Consistency Boundary del Aggregate.

De esta forma, `DOMAIN-009D-Domain-Events.md` establece el contrato
conceptual oficial de hechos del Aggregate **Voting**, manteniendo
la coherencia con el patrón consolidado de AURA Core.