# DOMAIN-006D — Assembly Domain Events

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Assembly Management

Aggregate:
Assembly

Autor:
ARADA

Documentos relacionados:

* DOMAIN-006-Aggregate.md
* DOMAIN-006A-Lifecycle.md
* DOMAIN-006B-State-Machine.md
* DOMAIN-006C-Commands.md
* DOMAIN-006E-Invariants.md
* DOMAIN-006F-Permissions.md
* DOMAIN-006G-Repository-Contract.md
* DOMAIN-006I-Versioning.md
* DOMAIN-006J-Consistency-Boundary.md
* DOMAIN-006K-Integration-Events.md
* DOMAIN-006L-Read-Model.md
* DOMAIN-006M-Test-Scenarios.md
* DOMAIN-006O-Security-Model.md
* CORE-006-Domain-Invariants.md
* CORE-008-Aggregate-Design-Rules.md
* CORE-011-Repository-Contracts.md

---

# Objetivo

Definir formalmente los **Domain Events** publicados por el
Aggregate **Assembly** cuando ocurren hechos relevantes dentro de
su ciclo de vida.

Un Domain Event representa un hecho consumado.

Describe algo que ocurrió efectivamente dentro del dominio y que
ya fue aceptado por la Aggregate Root después de validar:

* estado actual;
* Guards;
* precondiciones;
* permisos correspondientes;
* invariantes;
* consistencia;
* concurrencia.

Los Domain Events permiten representar la evolución de Assembly
sin acoplarla directamente a otros Aggregates, Bounded Contexts,
infraestructura o sistemas externos.

---

# Propósito

Los Domain Events permiten expresar hechos significativos de
Assembly mediante el lenguaje ubicuo de AURA.

Ejemplos:

```text
AssemblyCreated

AssemblyScheduled

AssemblyConvoked

AssemblyStarted

AssemblyCompleted
```

Cada evento expresa algo que ya ocurrió.

Los Domain Events permiten:

* preservar trazabilidad;
* comunicar hechos dentro del dominio;
* desacoplar Aggregates;
* alimentar Read Models;
* iniciar procesos posteriores;
* soportar Audit;
* generar Integration Events;
* habilitar arquitecturas Event-Driven;
* mantener compatibilidad con CQRS;
* mantener compatibilidad con Event Sourcing.

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
StartAssembly
```

es un Command.

Mientras:

```text
AssemblyStarted
```

es un Domain Event.

La relación conceptual es:

```text
Command
    │
    ▼
Assembly
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

Ejemplos:

```text
CreateAssembly

ScheduleAssembly

ConvokeAssembly

StartAssembly

CompleteAssembly

CancelAssembly

ArchiveAssembly
```

Los Domain Events expresan hechos consumados en pasado.

Ejemplos:

```text
AssemblyCreated

AssemblyScheduled

AssemblyConvoked

AssemblyStarted

AssemblyCompleted

AssemblyCancelled

AssemblyArchived
```

Nunca debe utilizarse:

```text
AssemblyStarted
```

como solicitud de inicio.

Tampoco debe utilizarse:

```text
StartAssembly
```

como registro histórico de una reunión iniciada.

---

# Propiedad del Evento

Los Domain Events definidos en este documento pertenecen
conceptualmente al Aggregate:

```text
Assembly
```

La Aggregate Root es responsable de producirlos cuando sus
operaciones cambian el estado del dominio.

Otros Aggregates pueden reaccionar posteriormente a estos hechos,
pero no son propietarios del evento original.

---

# Alcance

Los eventos de Assembly describen exclusivamente hechos
pertenecientes al Aggregate.

No representan directamente hechos internos de:

```text
Organization

Territory

Citizen

Membership

Role

Proposal

Participation

Voting

Document

Notification

Audit

Integration
```

Cuando un hecho pertenece a otro Aggregate debe ser publicado por
el Aggregate responsable.

---

# Eventos Oficiales

La versión 1.0 define conceptualmente los siguientes Domain
Events:

```text
AssemblyCreated

AssemblyScheduled

AssemblyRescheduled

AssemblyConvoked

AssemblyRenamed

AssemblyTypeChanged

AssemblyPurposeChanged

AssemblyDescriptionChanged

AssemblyModalityChanged

AssemblyLocationChanged

AssemblyConvocationUpdated

AssemblyRulesUpdated

AssemblyExecutionConditionsUpdated

AssemblyStarted

AssemblyCompleted

AssemblyCancelled

AssemblyArchived
```

Estos eventos representan los hechos principales definidos por el
modelo conceptual, Lifecycle, State Machine y Commands de
Assembly.

---

# Categorías de Eventos

Los Domain Events pueden agruparse conceptualmente en:

```text
Lifecycle Events

Configuration Events

Scheduling Events

Convocation Events

Execution Events

Closure Events
```

Esta agrupación facilita comprensión y documentación.

No modifica la identidad individual de los eventos.

---

# Lifecycle Events

Representan cambios significativos en el ciclo de vida.

```text
AssemblyCreated

AssemblyScheduled

AssemblyConvoked

AssemblyStarted

AssemblyCompleted

AssemblyCancelled

AssemblyArchived
```

---

# Configuration Events

Representan modificaciones conceptuales sobre propiedades de la
reunión.

```text
AssemblyRenamed

AssemblyTypeChanged

AssemblyPurposeChanged

AssemblyDescriptionChanged

AssemblyModalityChanged

AssemblyLocationChanged

AssemblyRulesUpdated

AssemblyExecutionConditionsUpdated
```

---

# Scheduling Events

Representan cambios en la planificación temporal.

```text
AssemblyScheduled

AssemblyRescheduled
```

---

# Convocation Events

Representan hechos relacionados con la convocatoria formal.

```text
AssemblyConvoked

AssemblyConvocationUpdated
```

---

# Execution Events

Representan hechos de ejecución real.

```text
AssemblyStarted

AssemblyCompleted
```

---

# Closure Events

Representan hechos que sacan a la reunión de su flujo normal o
activo.

```text
AssemblyCompleted

AssemblyCancelled

AssemblyArchived
```

---

# Estructura General

Todo Domain Event de Assembly debe contener, como mínimo:

```text
EventId

EventType

AssemblyId

OrganizationId

AggregateVersion

OccurredAt

CorrelationId

CausationId
```

Puede incorporar campos adicionales según el hecho representado.

---

# EventId

Identificador único del Domain Event.

```text
EventId
```

Debe:

* ser único;
* ser inmutable;
* identificar un único hecho;
* no reutilizarse;
* permitir trazabilidad;
* ser independiente de AssemblyId.

Dos hechos distintos nunca deben compartir EventId.

---

# EventType

Representa el nombre semántico del hecho ocurrido.

Ejemplo:

```text
AssemblyStarted
```

EventType debe utilizar el lenguaje ubicuo del dominio.

No debe contener nombres de:

* tablas;
* endpoints;
* frameworks;
* brokers;
* tecnologías;
* acciones técnicas.

---

# AssemblyId

Identifica la Assembly que produjo el hecho.

```text
AssemblyId
```

AssemblyId permite relacionar el evento con la Aggregate Root.

Permanece inmutable.

---

# OrganizationId

Identifica la Organization propietaria de la Assembly al momento
del evento.

```text
OrganizationId
```

Como OrganizationId es inmutable en Assembly, permite mantener el
contexto organizacional del hecho.

El evento no contiene el Aggregate Organization completo.

---

# AggregateVersion

Representa la versión de Assembly resultante del cambio que
produjo el evento.

```text
AggregateVersion
```

Ejemplo:

```text
BeforeVersion = 4

Command accepted

AfterVersion = 5

DomainEvent.AggregateVersion = 5
```

AggregateVersion permite:

* ordenar eventos del mismo Aggregate;
* detectar inconsistencias;
* reconstruir evolución;
* mantener trazabilidad;
* soportar Event Sourcing cuando corresponda.

---

# OccurredAt

Representa el momento en que el hecho de dominio ocurrió.

```text
OccurredAt
```

Debe diferenciarse de:

```text
Command.Timestamp
```

El primero representa el hecho consumado.

El segundo representa la intención recibida.

Ambos pueden coincidir temporalmente, pero poseen significados
conceptuales distintos.

---

# CorrelationId

Permite correlacionar el evento con el flujo de negocio al cual
pertenece.

```text
CorrelationId
```

Puede mantenerse desde el Command que originó la operación.

Ejemplo:

```text
CorrelationId = Process-123
```

permite seguir un proceso a través de:

```text
Command
    ↓
Domain Event
    ↓
Integration Event
    ↓
External Process
```

---

# CausationId

Identifica el Command o Domain Event que causó el hecho.

```text
CausationId
```

Ejemplo:

```text
CommandId = CMD-100

AssemblyStarted.CausationId = CMD-100
```

Permite mantener una cadena causal explícita.

---

# Event Payload

Cada Domain Event contiene únicamente los datos necesarios para
representar el hecho.

No debe transportar automáticamente una copia completa de
Assembly.

Debe aplicarse:

```text
minimum meaningful payload
```

El Payload debe ser suficiente para comprender el hecho sin
romper encapsulamiento innecesariamente.

---

# Inmutabilidad

Los Domain Events son inmutables.

Una vez producido:

```text
AssemblyStarted
```

no puede modificarse posteriormente para representar otro hecho.

Si el dominio cambia nuevamente debe producirse un nuevo evento.

Ejemplo:

```text
AssemblyScheduled
    ↓
AssemblyRescheduled
```

No se modifica retroactivamente AssemblyScheduled.

Se agrega un nuevo hecho:

```text
AssemblyRescheduled
```

---

# Historicidad

Los eventos preservan hechos anteriores.

Si una Assembly produce:

```text
AssemblyScheduled
```

posteriormente:

```text
AssemblyConvoked
```

y finalmente:

```text
AssemblyCancelled
```

todos los hechos permanecen verdaderos.

La secuencia significa:

```text
la reunión fue programada,
luego convocada,
y posteriormente cancelada.
```

No significa:

```text
la reunión nunca fue programada
ni convocada.
```

Los Domain Events no reescriben el pasado.

---

# AssemblyCreated

## Definición

Representa el hecho de que una nueva Assembly fue creada
válidamente dentro del dominio.

---

## Command origen

```text
CreateAssembly
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
AssemblyId

OrganizationId

AssemblyName

AssemblyType

AssemblyStatus

CreatedAt
```

Puede incluir:

```text
TerritoryId

AssemblyPurpose
```

cuando formen parte de la creación inicial.

---

## Invariantes

Antes de producir el evento debe haberse validado:

* AssemblyId válido;
* AssemblyId único;
* OrganizationId válido;
* AssemblyName válido;
* AssemblyType válido;
* invariantes iniciales satisfechas.

---

## Significado

```text
AssemblyCreated
```

significa:

```text
la Assembly existe formalmente dentro del dominio.
```

No significa:

```text
la Assembly fue programada.
```

Tampoco:

```text
la Assembly fue convocada.
```

---

# AssemblyScheduled

## Definición

Representa el hecho de que una Assembly Draft fue programada
formalmente.

---

## Command origen

```text
ScheduleAssembly
```

---

## Estado previo

```text
Draft
```

---

## Estado resultante

```text
Scheduled
```

---

## Payload mínimo

```text
AssemblyId

OrganizationId

ScheduledStartAt

ScheduledEndAt

TimeZone

AssemblyModality
```

Puede incluir:

```text
AssemblyLocation
```

cuando corresponda.

---

## Significado

El evento confirma que existe una programación aceptada por el
dominio.

No confirma que la reunión haya comenzado.

Por lo tanto:

```text
AssemblyScheduled
```

no equivale a:

```text
AssemblyStarted
```

---

# AssemblyRescheduled

## Definición

Representa el hecho de que la programación previamente existente
de una Assembly fue modificada válidamente.

---

## Command origen

```text
RescheduleAssembly
```

---

## Estados permitidos

Conceptualmente puede ocurrir desde:

```text
Scheduled

Convoked
```

según las reglas oficiales.

---

## Estado resultante

Puede mantenerse:

```text
Scheduled
```

o:

```text
Convoked
```

según el estado previo y las reglas aplicables.

---

## Payload mínimo

```text
AssemblyId

OrganizationId

PreviousScheduledStartAt

NewScheduledStartAt

PreviousScheduledEndAt

NewScheduledEndAt

TimeZone
```

Los valores opcionales se incluyen únicamente cuando existan.

---

## Significado

El evento preserva explícitamente que existió una programación
anterior y que posteriormente fue modificada.

No se modifica retroactivamente:

```text
AssemblyScheduled
```

---

# AssemblyConvoked

## Definición

Representa el hecho de que una Assembly fue formalmente
convocada.

---

## Command origen

```text
ConvokeAssembly
```

---

## Estado previo

```text
Scheduled
```

---

## Estado resultante

```text
Convoked
```

---

## Payload mínimo

```text
AssemblyId

OrganizationId

ConvokedAt

ConvocationMethod
```

Puede incluir:

```text
ConvocationDate

ConvocationDeadline

ConvocationReference
```

según el modelo vigente.

---

## Significado

```text
AssemblyConvoked
```

representa que la condición formal de convocatoria quedó
satisfecha.

No representa que Notifications hayan sido entregadas.

La notificación pertenece a otro contexto.

---

# AssemblyRenamed

## Definición

Representa el hecho de que el nombre formal de una Assembly fue
modificado.

---

## Command origen

```text
RenameAssembly
```

---

## Payload mínimo

```text
AssemblyId

OrganizationId

PreviousName

NewName
```

---

## Estado

No exige cambio de AssemblyStatus.

---

## Significado

Permite preservar trazabilidad del cambio de nombre sin alterar
la identidad de la reunión.

AssemblyId permanece igual.

---

# AssemblyTypeChanged

## Definición

Representa el hecho de que la clasificación conceptual de una
Assembly fue modificada válidamente.

---

## Command origen

```text
ChangeAssemblyType
```

---

## Payload mínimo

```text
AssemblyId

OrganizationId

PreviousAssemblyType

NewAssemblyType
```

---

## Estado

No modifica necesariamente AssemblyStatus.

---

## Restricción

El evento solo puede existir si el cambio era válido para el
estado actual.

No debe publicarse después de un intento rechazado.

---

# AssemblyPurposeChanged

## Definición

Representa el hecho de que el propósito formal de una Assembly
fue modificado.

---

## Command origen

```text
ChangeAssemblyPurpose
```

---

## Payload mínimo

```text
AssemblyId

OrganizationId

PreviousAssemblyPurpose

NewAssemblyPurpose
```

---

## Significado

La modificación del propósito no crea una nueva Assembly.

AssemblyId permanece inmutable.

---

# AssemblyDescriptionChanged

## Definición

Representa el hecho de que la descripción complementaria de la
Assembly fue modificada.

---

## Command origen

```text
ChangeAssemblyDescription
```

---

## Payload mínimo

```text
AssemblyId

OrganizationId

PreviousDescription

NewDescription
```

---

## Estado

Puede ocurrir únicamente en estados donde la modificación sea
válida.

---

# AssemblyModalityChanged

## Definición

Representa el hecho de que la modalidad de realización de una
Assembly fue modificada.

---

## Command origen

```text
ChangeAssemblyModality
```

---

## Payload mínimo

```text
AssemblyId

OrganizationId

PreviousModality

NewModality
```

Puede incorporar cambios derivados de Location cuando la
operación los incluya explícitamente.

---

## Validaciones Previas

Antes de producir el evento debe haberse validado:

* nueva modalidad válida;
* compatibilidad con Location;
* compatibilidad con reglas;
* estado modificable;
* invariantes preservadas.

---

# AssemblyLocationChanged

## Definición

Representa el hecho de que la ubicación formal asociada a una
Assembly cambió.

---

## Command origen

```text
ChangeAssemblyLocation
```

---

## Payload mínimo

```text
AssemblyId

OrganizationId

PreviousLocation

NewLocation
```

---

## Significado

El evento describe un cambio en el contexto físico o referencial
de realización.

No representa un cambio de Territory.

TerritoryId posee significado independiente.

---

# AssemblyConvocationUpdated

## Definición

Representa el hecho de que información formal de Convocation fue
modificada.

---

## Command origen

```text
UpdateAssemblyConvocation
```

Puede generarse también como consecuencia complementaria de una
reprogramación cuando el modelo determine que la convocatoria
debe actualizarse.

---

## Payload mínimo

```text
AssemblyId

OrganizationId

PreviousConvocation

NewConvocation
```

---

## Restricción Histórica

Si la Assembly ya fue convocada:

```text
ConvokedAt
```

no debe ser eliminado ni sobrescrito como si la convocatoria
original nunca hubiera ocurrido.

El evento representa una actualización posterior.

---

# AssemblyRulesUpdated

## Definición

Representa el hecho de que las reglas propias de la Assembly
fueron modificadas válidamente.

---

## Command origen

```text
UpdateAssemblyRules
```

---

## Payload mínimo

```text
AssemblyId

OrganizationId

PreviousAssemblyRules

NewAssemblyRules
```

---

## Restricción

El evento solo puede generarse cuando las reglas modificadas:

* son válidas;
* son compatibles con AssemblyType;
* son compatibles con AssemblyModality;
* no violan invariantes;
* pueden modificarse en el estado vigente.

---

# AssemblyExecutionConditionsUpdated

## Definición

Representa el hecho de que las condiciones de realización de la
Assembly fueron modificadas.

---

## Command origen

```text
UpdateAssemblyExecutionConditions
```

---

## Payload mínimo

```text
AssemblyId

OrganizationId

PreviousExecutionConditions

NewExecutionConditions
```

---

## Significado

Permite preservar que los requisitos necesarios para realizar la
reunión cambiaron antes de su ejecución.

No modifica directamente otros Aggregates utilizados para
evaluar esas condiciones.

---

# AssemblyStarted

## Definición

Representa el hecho de que la Assembly comenzó formalmente.

---

## Command origen

```text
StartAssembly
```

---

## Estado previo

```text
Convoked
```

---

## Estado resultante

```text
InProgress
```

---

## Payload mínimo

```text
AssemblyId

OrganizationId

StartedAt
```

Puede incorporar:

```text
AssemblyModality

AssemblyLocation
```

cuando sean necesarios para representar el contexto efectivo de
inicio.

---

## Invariantes

Debe cumplirse:

```text
StartedAt != null
```

El estado resultante debe ser:

```text
InProgress
```

---

## Significado

```text
AssemblyStarted
```

representa un hecho real.

No debe producirse automáticamente porque:

```text
CurrentTime >= ScheduledStartAt
```

La programación y el inicio efectivo permanecen separados.

---

# AssemblyCompleted

## Definición

Representa el hecho de que una Assembly InProgress finalizó
formalmente.

---

## Command origen

```text
CompleteAssembly
```

---

## Estado previo

```text
InProgress
```

---

## Estado resultante

```text
Completed
```

---

## Payload mínimo

```text
AssemblyId

OrganizationId

StartedAt

CompletedAt
```

---

## Invariantes

Debe cumplirse:

```text
CompletedAt >= StartedAt
```

---

## Significado

El evento representa el cierre normal de la reunión.

No implica automáticamente:

* archivado;
* cierre de Voting;
* cierre de Proposal;
* cierre de Participation;
* creación de Document;
* envío de Notification.

Estos procesos permanecen separados.

---

# AssemblyCancelled

## Definición

Representa el hecho de que una Assembly fue cancelada antes de
completar su flujo normal.

---

## Command origen

```text
CancelAssembly
```

---

## Estados previos permitidos

```text
Draft

Scheduled

Convoked
```

---

## Estado resultante

```text
Cancelled
```

---

## Payload mínimo

```text
AssemblyId

OrganizationId

PreviousStatus

CancelledAt
```

Cuando corresponda también:

```text
CancellationReason
```

---

## Preservación Histórica

El evento no elimina información anterior.

Si la Assembly estaba Scheduled:

```text
ScheduledStartAt
```

permanece como información histórica.

Si estaba Convoked:

```text
ConvokedAt
```

también permanece.

---

## Restricción

La versión 1.0 no utiliza:

```text
AssemblyCancelled
```

para representar una interrupción de una reunión que ya estaba
InProgress.

Dicho escenario requiere una evolución explícita del modelo.

---

# AssemblyArchived

## Definición

Representa el hecho de que una Assembly fue retirada del ciclo
operativo y pasó a estado histórico terminal.

---

## Command origen

```text
ArchiveAssembly
```

---

## Estados previos permitidos

```text
Completed

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
AssemblyId

OrganizationId

PreviousStatus

ArchivedAt
```

Puede incorporar:

```text
ArchiveReason
```

cuando las reglas lo requieran.

---

## Significado

Archived no significa eliminación física.

El Aggregate conserva:

* AssemblyId;
* OrganizationId;
* historial;
* timestamps;
* Version;
* eventos históricos.

---

# Relación entre Eventos y State Machine

Los eventos principales deben ser coherentes con:

```text
DOMAIN-006B-State-Machine.md
```

Relación oficial:

| Evento              | Estado previo | Estado resultante |
| ------------------- | ------------- | ----------------- |
| AssemblyCreated     | No existe     | Draft             |
| AssemblyScheduled   | Draft         | Scheduled         |
| AssemblyRescheduled | Scheduled     | Scheduled         |
| AssemblyRescheduled | Convoked      | Convoked          |
| AssemblyConvoked    | Scheduled     | Convoked          |
| AssemblyStarted     | Convoked      | InProgress        |
| AssemblyCompleted   | InProgress    | Completed         |
| AssemblyCancelled   | Draft         | Cancelled         |
| AssemblyCancelled   | Scheduled     | Cancelled         |
| AssemblyCancelled   | Convoked      | Cancelled         |
| AssemblyArchived    | Completed     | Archived          |
| AssemblyArchived    | Cancelled     | Archived          |

Los eventos de modificación pueden mantener el mismo estado.

---

# Evento y Cambio de Estado

No todo Domain Event implica una transición del Lifecycle.

Por ejemplo:

```text
AssemblyRenamed
```

puede ocurrir:

```text
Draft
    │
    ▼
Draft
```

y:

```text
AssemblyRescheduled
```

puede ocurrir:

```text
Scheduled
    │
    ▼
Scheduled
```

El evento representa un cambio de dominio incluso cuando
AssemblyStatus permanece igual.

---

# Versionado de Eventos

Todo evento debe relacionarse con una versión concreta del
Aggregate.

Ejemplo:

```text
AssemblyCreated
AggregateVersion = 1

AssemblyScheduled
AggregateVersion = 2

AssemblyConvoked
AggregateVersion = 3

AssemblyStarted
AggregateVersion = 4
```

Para un mismo AssemblyId no deben existir dos eventos válidos
aplicados al mismo orden de versión.

---

# Orden de Eventos

Dentro de una única Assembly:

```text
AggregateVersion
```

establece el orden lógico de evolución.

Conceptualmente:

```text
Version 1
AssemblyCreated

Version 2
AssemblyScheduled

Version 3
AssemblyConvoked

Version 4
AssemblyStarted
```

El timestamp puede aportar información temporal.

La versión protege el orden lógico del Aggregate.

---

# Eventos y Concurrencia

Los Domain Events solo pueden existir después de una
modificación que superó control de concurrencia.

Ejemplo:

```text
PersistedVersion = 5

ExpectedVersion = 4
```

El Command debe fallar.

Por lo tanto no puede producirse un nuevo:

```text
AssemblyStarted
```

con una versión inválida.

---

# Eventos de una Transacción

Un Command válido puede producir uno o más Domain Events.

Cuando existan múltiples eventos dentro de una misma modificación,
debe preservarse su orden causal.

Ejemplo conceptual:

```text
RescheduleAssembly
        │
        ▼
AssemblyRescheduled
        │
        ▼
AssemblyConvocationUpdated
```

cuando ambos hechos ocurran dentro de la misma operación válida.

La estrategia concreta de numeración interna pertenece al modelo
de eventos adoptado por AURA, pero el orden causal debe
preservarse.

---

# Evento Principal

Cuando una operación produzca varios eventos, debe distinguirse
el hecho principal de hechos derivados internos.

Ejemplo:

```text
RescheduleAssembly
```

puede tener como hecho principal:

```text
AssemblyRescheduled
```

y, si corresponde:

```text
AssemblyConvocationUpdated
```

El segundo evento no debe inventarse si la convocatoria no cambió
realmente.

---

# No Event on Failure

Una operación rechazada nunca publica un Domain Event de éxito.

Ejemplo:

```text
AssemblyStatus = Draft

StartAssembly
```

Debe resultar en:

```text
Rejected
```

No debe producir:

```text
AssemblyStarted
```

---

# No-Op y Eventos

Cuando un Command no representa un cambio real puede considerarse
un No-Op.

Ejemplo:

```text
CurrentName = "Asamblea General"

RenameAssembly(
    NewName = "Asamblea General"
)
```

No debería producir:

```text
AssemblyRenamed
```

si no ocurrió un cambio semántico.

Esto evita eventos artificiales y Versiones sin significado.

---

# Eventos Pendientes

La Aggregate Root puede mantener conceptualmente una colección
temporal de:

```text
PendingDomainEvents
```

Estos eventos representan hechos ocurridos durante la ejecución
actual del Aggregate que todavía deben ser despachados mediante la
estrategia arquitectónica correspondiente.

La colección no representa el historial completo del Aggregate.

---

# Propiedad de PendingDomainEvents

Los eventos pendientes pertenecen temporalmente a la Aggregate
Root hasta que la capa correspondiente complete su procesamiento.

Conceptualmente:

```text
Assembly
    │
    ├── State
    └── PendingDomainEvents
```

No deben utilizarse como mecanismo para incorporar dependencias de
infraestructura dentro del dominio.

---

# Persistencia y Eventos

La consistencia entre:

```text
Aggregate State
```

y:

```text
Domain Events
```

debe protegerse mediante la estrategia de persistencia adoptada.

No debe ocurrir:

```text
state persisted
event lost
```

ni:

```text
event published
state rollback
```

como comportamiento normal.

La implementación puede utilizar estrategias como:

```text
Transactional Outbox
```

cuando corresponda.

La técnica concreta pertenece a Infrastructure.

---

# Transactional Outbox

El patrón Transactional Outbox puede utilizarse para garantizar
entrega confiable después de persistir el Aggregate.

Conceptualmente:

```text
Assembly
    │
    │ Domain Event
    ▼
Transaction
    ├── Aggregate State
    └── Outbox Record
            │
            ▼
       Event Dispatcher
```

Assembly no conoce la Outbox.

El patrón pertenece a Infrastructure/Application.

---

# Domain Events e Integration Events

Debe existir una separación explícita entre:

```text
Domain Event
```

e:

```text
Integration Event
```

Un Domain Event pertenece al dominio interno.

Un Integration Event pertenece a una frontera de integración.

Ejemplo:

```text
AssemblyStarted
```

puede originar:

```text
AssemblyStartedIntegrationEvent
```

pero no son el mismo contrato.

---

# Razón de la Separación

Los Domain Events pueden evolucionar conforme al modelo interno.

Los Integration Events deben proteger contratos externos.

La separación evita que:

* cambios internos rompan consumidores;
* infraestructura determine el modelo de dominio;
* modelos externos contaminen el lenguaje ubicuo;
* el Aggregate publique directamente contratos externos.

---

# Flujo de Integración

```text
Assembly
    │
    ▼
Domain Event
    │
    ▼
Application / Integration Handler
    │
    ▼
Integration Event
    │
    ▼
External Consumer
```

La definición formal de Integration Events pertenece a:

```text
DOMAIN-006K-Integration-Events.md
```

---

# Domain Events y Notification

Eventos como:

```text
AssemblyConvoked

AssemblyRescheduled

AssemblyCancelled
```

pueden ser consumidos por procesos de Notification.

Ejemplo:

```text
AssemblyConvoked
      │
      ▼
Notification Handler
      │
      ▼
Notification Command
```

Assembly no crea ni envía directamente Notification dentro de su
transacción.

---

# Domain Events y Audit

Audit puede consumir eventos de Assembly.

Ejemplos:

```text
AssemblyCreated

AssemblyScheduled

AssemblyConvoked

AssemblyStarted

AssemblyCompleted

AssemblyCancelled

AssemblyArchived
```

El evento proporciona hechos relevantes para trazabilidad.

Audit mantiene su propio Aggregate.

---

# Domain Events y Read Models

Los eventos pueden alimentar proyecciones de lectura.

Ejemplo:

```text
AssemblyScheduled
       │
       ▼
AssemblyCalendarProjection
```

Otro ejemplo:

```text
AssemblyCompleted
       │
       ▼
AssemblyTimelineProjection
```

Los Read Models son reconstruibles a partir de hechos y otras
fuentes autorizadas.

No constituyen la fuente transaccional de verdad.

---

# Domain Events y CQRS

Dentro de CQRS:

```text
Command
    │
    ▼
Assembly Write Model
    │
    ▼
Domain Event
    │
    ▼
Projection
    │
    ▼
Read Model
```

La lectura permanece desacoplada de la modificación del
Aggregate.

---

# Domain Events y Event Sourcing

Los eventos definidos son compatibles conceptualmente con Event
Sourcing.

Una Assembly podría reconstruirse mediante:

```text
AssemblyCreated

AssemblyScheduled

AssemblyConvoked

AssemblyStarted

AssemblyCompleted

AssemblyArchived
```

generando la evolución:

```text
Draft
    ↓
Scheduled
    ↓
Convoked
    ↓
InProgress
    ↓
Completed
    ↓
Archived
```

La compatibilidad no obliga a utilizar Event Sourcing.

---

# Rehidratación desde Eventos

Cuando se reconstruye una Assembly desde eventos históricos,
estos eventos deben aplicarse sin producirlos nuevamente.

Conceptualmente:

```text
apply(AssemblyCreated)

apply(AssemblyScheduled)

apply(AssemblyConvoked)
```

reconstruye:

```text
AssemblyStatus = Convoked
```

pero no agrega nuevos:

```text
PendingDomainEvents
```

La rehidratación restaura hechos.

No genera hechos nuevos.

---

# Eventos Históricos

Los Domain Events persistidos deben considerarse inmutables.

No deben editarse retrospectivamente para reflejar el estado
actual.

Si una información cambia se agrega un nuevo evento.

Ejemplo:

```text
AssemblyScheduled(T1)

AssemblyRescheduled(T2)
```

No debe convertirse el primer evento en:

```text
AssemblyScheduled(T2)
```

---

# Evolución de Esquema

La estructura de un Domain Event puede evolucionar.

Cuando exista persistencia histórica o consumidores internos
dependientes, los cambios deben ser controlados.

Puede utilizarse:

```text
EventSchemaVersion
```

cuando la arquitectura lo requiera.

Ejemplo conceptual:

```text
EventSchemaVersion = 1
```

Este valor es distinto de:

```text
AggregateVersion
```

---

# AggregateVersion versus EventSchemaVersion

```text
AggregateVersion
```

representa la posición evolutiva del Aggregate.

```text
EventSchemaVersion
```

representa la versión del contrato estructural del evento.

No deben confundirse.

Ejemplo:

```text
AssemblyStarted

AggregateVersion = 15

EventSchemaVersion = 2
```

Esto significa que el evento corresponde a la versión 15 de la
Assembly, utilizando la versión 2 del esquema del evento.

---

# Compatibilidad hacia Atrás

Cuando un esquema de evento cambie debe evaluarse:

* consumidores existentes;
* eventos históricos;
* proyecciones;
* Event Sourcing;
* auditoría;
* integraciones;
* migraciones;
* replay.

No deben eliminarse campos con significado histórico sin una
estrategia explícita.

---

# Upcasting

Cuando eventos históricos deban ser interpretados mediante un
modelo más reciente puede utilizarse conceptualmente:

```text
Event Upcaster
```

El Upcaster transforma una representación histórica hacia una
forma compatible para consumo interno.

No modifica físicamente el hecho histórico original por defecto.

La necesidad concreta debe documentarse mediante arquitectura
explícita.

---

# Identidad del Actor

Los Domain Events pueden incluir:

```text
ActorId
```

cuando conocer quién provocó el hecho forme parte necesaria de la
trazabilidad del dominio.

Sin embargo, debe distinguirse:

```text
ActorId
```

de:

```text
Citizen Aggregate
```

El evento contiene una referencia.

No contiene el Aggregate Citizen.

---

# ActorId como Metadato

Cuando ActorId no modifica el significado del hecho puede
mantenerse como metadato del evento.

Ejemplo:

```text
AssemblyCancelled
```

puede registrar quién provocó la cancelación.

La decisión de ubicar ActorId en Payload o Metadata debe ser
consistente en la arquitectura de eventos de AURA.

---

# Privacidad

Los eventos deben contener exclusivamente información necesaria.

No deben transportar indiscriminadamente:

* perfiles completos;
* datos personales innecesarios;
* credenciales;
* información privada de Citizen;
* secretos;
* tokens.

Los identificadores deben utilizarse cuando sea suficiente.

---

# Datos Sensibles

Domain Events nunca deben contener:

* contraseñas;
* claves privadas;
* secretos criptográficos;
* tokens OAuth;
* JWT de sesión;
* credenciales de proveedores;
* cookies;
* secretos de infraestructura.

Estas propiedades no pertenecen al dominio Assembly.

---

# Seguridad de Eventos

Los Domain Events pueden contener información de negocio
sensible.

La infraestructura responsable de:

* almacenamiento;
* transporte;
* autorización;
* cifrado;
* retención;
* acceso;

debe aplicar las políticas definidas por el Security Model.

Assembly no implementa mecanismos criptográficos directamente.

---

# Orden entre Aggregates

No existe un orden global obligatorio entre eventos de Aggregates
distintos.

Ejemplo:

```text
AssemblyStarted
```

y:

```text
ParticipationCreated
```

pertenecen a límites distintos.

La coordinación distribuida debe usar:

* CorrelationId;
* CausationId;
* AggregateVersion;
* identificadores;
* políticas de consistencia eventual.

No debe suponerse una transacción global.

---

# Entrega al Menos Una Vez

Una infraestructura de mensajería puede operar con semántica:

```text
at-least-once delivery
```

Esto significa que un consumidor podría recibir un mismo evento
más de una vez.

Los consumidores deben utilizar mecanismos apropiados de
idempotencia.

Esta necesidad no altera la semántica del Domain Event.

---

# Idempotencia de Consumidores

Un consumidor puede utilizar:

```text
EventId
```

para detectar procesamiento repetido.

Conceptualmente:

```text
if EventId already processed:
    ignore duplicate delivery
```

La lógica concreta pertenece al consumidor.

Assembly no debe generar un nuevo EventId para representar la
misma entrega retransmitida.

---

# Eventos Fuera de Orden

En sistemas distribuidos algunos consumidores pueden observar
eventos fuera de orden.

AggregateVersion permite identificar el orden correcto dentro de
una Assembly.

Ejemplo:

```text
AssemblyStarted
AggregateVersion = 8
```

no debe proyectarse como anterior a:

```text
AssemblyConvoked
AggregateVersion = 7
```

aunque la infraestructura los entregue en orden inverso.

---

# Replay

Los eventos pueden ser reprocesados para reconstruir:

* Read Models;
* Analytics;
* proyecciones;
* auditoría derivada;
* estado cuando se utilice Event Sourcing.

El replay no debe causar efectos externos irreversibles de forma
indiscriminada.

Por ejemplo, reprocesar:

```text
AssemblyConvoked
```

no debe necesariamente volver a enviar una Notification real.

---

# Proyecciones versus Side Effects

Los consumidores deben distinguir:

```text
Projection
```

de:

```text
External Side Effect
```

Una proyección puede reprocesarse.

Un Side Effect como enviar una comunicación externa puede requerir
protecciones adicionales de idempotencia.

---

# Domain Event Handlers

Los Domain Event Handlers reaccionan a eventos después de que el
hecho ocurrió.

Ejemplo conceptual:

```text
AssemblyCompleted
       │
       ├────────► UpdateReadModel
       ├────────► RegisterAudit
       └────────► PrepareIntegrationEvent
```

Un Handler no modifica retroactivamente el hecho original.

---

# Handler Failure

El fallo de un consumidor no significa que el Domain Event deje
de ser verdadero.

Ejemplo:

```text
AssemblyConvoked
```

ocurrió.

Si el Notification Handler falla, la Assembly continúa siendo:

```text
Convoked
```

El error debe resolverse mediante retry, compensación o políticas
de infraestructura.

No mediante reversión silenciosa del Domain Event.

---

# Eventos y Consistencia Eventual

Los efectos externos derivados de Domain Events utilizan
consistencia eventual.

Ejemplo:

```text
AssemblyConvoked
        │
        ▼
Assembly persisted
        │
        ▼
Notification eventually created
```

Puede existir una ventana temporal donde Assembly ya está
Convoked y Notification aún no fue procesada.

Esto es coherente con el límite DDD.

---

# Eventos y Consistency Boundary

El evento se produce como consecuencia de una modificación dentro
del límite:

```text
Assembly
```

No implica modificación atómica de:

```text
Notification

Audit

Participation

Proposal

Voting

Document
```

La definición formal pertenece a:

```text
DOMAIN-006J-Consistency-Boundary.md
```

---

# Eventos e Integration Boundary

Los sistemas externos no deben consumir necesariamente los Domain
Events internos directamente.

Cuando exista un contrato público o inter-contextual debe
utilizarse:

```text
Integration Event
```

La transformación protege el dominio interno.

---

# FIWARE

Los Domain Events pueden originar proyecciones hacia FIWARE.

Ejemplo:

```text
AssemblyStarted
      │
      ▼
Integration Handler
      │
      ▼
AssemblyStartedIntegrationEvent
      │
      ▼
FIWARE Adapter
      │
      ▼
NGSI-LD
```

FIWARE no constituye el propietario del Domain Event.

---

# Anti-Corruption Layer

Cuando un sistema externo utiliza una semántica diferente, la
transformación debe realizarse mediante una Anti-Corruption
Layer.

Un evento externo:

```text
MEETING_OPENED
```

no debe incorporarse automáticamente como Domain Event de AURA.

Debe traducirse solamente cuando exista equivalencia real con:

```text
AssemblyStarted
```

---

# Persistencia de Domain Events

Cuando la arquitectura requiera conservar Domain Events, la
persistencia debe preservar:

```text
EventId

EventType

AssemblyId

OrganizationId

AggregateVersion

OccurredAt

CorrelationId

CausationId

Payload
```

y, cuando corresponda:

```text
EventSchemaVersion
```

La representación física pertenece a Infrastructure.

---

# Domain Event Store

La existencia de un Event Store no forma parte obligatoria del
Aggregate.

El modelo de dominio es compatible con:

```text
State Persistence + Domain Events
```

y con:

```text
Event Sourcing
```

La estrategia debe definirse explícitamente a nivel
arquitectónico.

---

# Repository y Domain Events

El Repository persiste Assembly como unidad.

La estrategia de persistencia debe coordinar la versión del
Aggregate con los eventos generados.

Conceptualmente:

```text
load Assembly vN
      │
      ▼
execute Command
      │
      ▼
Assembly vN+1
      +
Domain Events
      │
      ▼
persist consistently
```

---

# Eventos y Optimistic Concurrency

AggregateVersion permite verificar que el evento corresponde a la
secuencia aceptada del Aggregate.

No debe existir:

```text
AssemblyVersion = 9
```

con un nuevo evento aceptado como:

```text
AggregateVersion = 8
```

después de que la versión 9 ya fue persistida.

---

# Eventos Duplicados

Dos eventos con EventId distinto pueden representar dos hechos
reales del mismo tipo.

Ejemplo:

```text
AssemblyDescriptionChanged
```

puede ocurrir varias veces durante la vida del Aggregate cuando el
estado permita modificaciones.

Cada hecho posee:

```text
EventId
```

propio y:

```text
AggregateVersion
```

propia.

Esto es diferente de una retransmisión duplicada del mismo
evento.

---

# Nombres de Eventos

Los Domain Events deben utilizar nombres:

```text
Aggregate + PastTenseFact
```

Ejemplos válidos:

```text
AssemblyCreated

AssemblyStarted

AssemblyCompleted
```

No deben utilizarse nombres técnicos como:

```text
AssemblyRowUpdated

AssemblyInsertedIntoMongo

AssemblyHttpRequestProcessed

AssemblyCacheRefreshed
```

---

# Granularidad de Eventos

Un evento debe representar un hecho con significado de negocio.

No debe ser excesivamente genérico.

Evitar:

```text
AssemblyUpdated
```

cuando el dominio conoce específicamente:

```text
AssemblyRenamed

AssemblyRescheduled

AssemblyLocationChanged
```

La granularidad explícita mejora:

* trazabilidad;
* lenguaje ubicuo;
* proyecciones;
* auditoría;
* evolución.

---

# Eventos Técnicos Prohibidos

No pertenecen al Aggregate Domain Events como:

```text
AssemblySaved

AssemblyLoaded

AssemblyCacheMissed

AssemblyMessagePublished

AssemblyDatabaseUpdated

AssemblyHttpRequestCompleted

AssemblyFIWARESynced
```

Estos representan hechos técnicos.

No hechos propios del dominio Assembly.

---

# Eventos Futuros

La versión 1.0 no define eventos como:

```text
AssemblySuspended

AssemblyResumed

AssemblyInterrupted

AssemblyAborted

AssemblyReopened

AssemblyDeleted
```

porque dichos estados y Commands no forman parte del modelo
oficial actual.

No deben introducirse aisladamente.

---

# Regla para Incorporar un Nuevo Domain Event

Un nuevo Domain Event debe incorporarse únicamente cuando
represente un hecho relevante del dominio.

Debe responder afirmativamente:

```text
¿Ocurrió algo relevante para el negocio?

¿Puede expresarse en pasado?

¿Posee significado dentro del lenguaje ubicuo?

¿Fue producido por comportamiento válido del Aggregate?

¿Debe poder ser observado por otras partes del dominio?
```

---

# Impacto de un Nuevo Evento

Agregar un nuevo evento exige revisar al menos:

```text
DOMAIN-006-Aggregate.md

DOMAIN-006A-Lifecycle.md

DOMAIN-006B-State-Machine.md

DOMAIN-006C-Commands.md

DOMAIN-006D-Domain-Events.md

DOMAIN-006E-Invariants.md

DOMAIN-006K-Integration-Events.md

DOMAIN-006L-Read-Model.md

DOMAIN-006M-Test-Scenarios.md
```

cuando corresponda.

No debe agregarse un evento aisladamente rompiendo coherencia
documental.

---

# Auditoría

Los Domain Events proporcionan una fuente natural de hechos
auditables.

Todo evento puede aportar:

```text
EventId

EventType

AssemblyId

OrganizationId

ActorId

AggregateVersion

OccurredAt

CorrelationId

CausationId
```

según el contrato oficial.

Audit puede almacenar su propia representación.

No debe modificar el Domain Event original.

---

# Trazabilidad Causal

Ejemplo:

```text
CommandId:
CMD-001

StartAssembly
    │
    ▼
AssemblyStarted
EventId:
EVT-010
```

El evento puede mantener:

```text
CausationId = CMD-001
```

y:

```text
CorrelationId = FLOW-100
```

Esto permite seguir un flujo sin acoplar el Aggregate a
infraestructura específica.

---

# Ejemplo de Flujo Completo

```text
CreateAssembly
      │
      ▼
AssemblyCreated
      │
      ▼
Status = Draft

ScheduleAssembly
      │
      ▼
AssemblyScheduled
      │
      ▼
Status = Scheduled

ConvokeAssembly
      │
      ▼
AssemblyConvoked
      │
      ▼
Status = Convoked

StartAssembly
      │
      ▼
AssemblyStarted
      │
      ▼
Status = InProgress

CompleteAssembly
      │
      ▼
AssemblyCompleted
      │
      ▼
Status = Completed

ArchiveAssembly
      │
      ▼
AssemblyArchived
      │
      ▼
Status = Archived
```

---

# Ejemplo de Flujo Cancelado

```text
AssemblyCreated
      │
      ▼
Draft

AssemblyScheduled
      │
      ▼
Scheduled

AssemblyConvoked
      │
      ▼
Convoked

AssemblyCancelled
      │
      ▼
Cancelled

AssemblyArchived
      │
      ▼
Archived
```

La secuencia mantiene todos los hechos ocurridos.

---

# Ejemplo de Reprogramación

Estado inicial:

```text
ScheduledStartAt = T1

AssemblyStatus = Scheduled
```

Command:

```text
RescheduleAssembly(
    ScheduledStartAt = T2
)
```

Resultado:

```text
ScheduledStartAt = T2

AssemblyStatus = Scheduled
```

Evento:

```text
AssemblyRescheduled
```

Payload conceptual:

```text
PreviousScheduledStartAt = T1

NewScheduledStartAt = T2
```

---

# Ejemplo de Evento Rechazado

Estado:

```text
AssemblyStatus = Completed
```

Command:

```text
StartAssembly
```

Resultado:

```text
Rejected
```

No existe:

```text
AssemblyStarted
```

Version permanece sin cambios.

---

# Ejemplo de Evento con Actor

```text
AssemblyCancelled
```

puede contener conceptualmente:

```text
EventId

AssemblyId

OrganizationId

ActorId

PreviousStatus

CancellationReason

CancelledAt

AggregateVersion

OccurredAt

CorrelationId

CausationId
```

El ActorId referencia al responsable de la intención aceptada.

No contiene el perfil completo del Actor.

---

# Relación con Lifecycle

Los eventos de transición deben preservar la semántica definida
en:

```text
DOMAIN-006A-Lifecycle.md
```

Por ejemplo:

```text
AssemblyCompleted
```

significa que la reunión terminó.

No significa que fue archivada.

```text
AssemblyArchived
```

representa un hecho posterior distinto.

---

# Relación con State Machine

Los eventos de cambio de estado solo pueden producirse como
resultado de transiciones permitidas por:

```text
DOMAIN-006B-State-Machine.md
```

Un evento no puede utilizarse para crear una transición no
permitida.

---

# Relación con Commands

Cada evento debe estar relacionado con una intención válida o con
comportamiento interno explícito del dominio.

La definición de Commands se encuentra en:

```text
DOMAIN-006C-Commands.md
```

Command y Event deben permanecer semánticamente coherentes.

---

# Relación con Invariants

Ningún evento puede representar un estado que viole:

```text
DOMAIN-006E-Invariants.md
```

Ejemplo:

```text
AssemblyCompleted
```

no puede existir si:

```text
StartedAt = null
```

porque el estado Completed requiere que la reunión haya iniciado.

---

# Relación con Permissions

Los permisos determinan quién puede provocar indirectamente un
hecho mediante Commands autorizados.

La definición pertenece a:

```text
DOMAIN-006F-Permissions.md
```

Los Domain Events no contienen lógica de autorización.

Representan hechos posteriores a la autorización y validación.

---

# Relación con Versioning

Todo Domain Event debe mantener una relación coherente con:

```text
DOMAIN-006I-Versioning.md
```

Cada modificación válida incrementa Version.

El evento producido representa la nueva AggregateVersion.

---

# Relación con Consistency Boundary

Los eventos permiten comunicar hechos fuera del límite sin
expandir la transacción de Assembly.

La definición del límite pertenece a:

```text
DOMAIN-006J-Consistency-Boundary.md
```

---

# Relación con Integration Events

Los eventos que deban cruzar Bounded Contexts pueden ser
traducidos según:

```text
DOMAIN-006K-Integration-Events.md
```

No todos los Domain Events necesitan transformarse en Integration
Events.

Solo deben publicarse externamente los hechos necesarios.

---

# Relación con Read Model

Las proyecciones definidas en:

```text
DOMAIN-006L-Read-Model.md
```

pueden consumir Domain Events para actualizar vistas.

El orden debe respetar AggregateVersion.

---

# Relación con Test Scenarios

Cada Domain Event debe contar con pruebas que aseguren:

```text
correct event type

correct payload

correct aggregate id

correct aggregate version

correct causation

correct correlation

event generated after valid command

event not generated after rejected command

historical values preserved

consumer idempotency assumptions
```

Los escenarios formales se encuentran en:

```text
DOMAIN-006M-Test-Scenarios.md
```

---

# Relación con Security Model

La información incluida en los eventos debe cumplir:

```text
DOMAIN-006O-Security-Model.md
```

Los Payloads deben respetar:

* minimización de datos;
* confidencialidad;
* clasificación de información;
* control de acceso;
* trazabilidad;
* políticas de retención.

---

# Independencia Tecnológica

Los Domain Events no dependen de:

```text
Kafka

RabbitMQ

NATS

Redis

MongoDB

PostgreSQL

HTTP

REST

GraphQL

FastAPI

Django

React

Next.js

OAuth

JWT

FIWARE

NGSI-LD
```

Estos mecanismos pueden transportar o persistir eventos.

No definen su semántica.

---

# Serialización

La representación serializada de un Domain Event pertenece a las
capas externas.

Conceptualmente el dominio puede representar:

```text
AssemblyStarted
```

sin conocer si posteriormente se serializa como:

```text
JSON

Avro

Protobuf

MessagePack
```

La elección tecnológica no debe contaminar el modelo.

---

# Reglas de Diseño

Los Domain Events de Assembly deben cumplir:

* representar hechos consumados;
* utilizar lenguaje ubicuo;
* utilizar nombres en pasado;
* ser inmutables;
* poseer EventId único;
* identificar AssemblyId;
* identificar OrganizationId;
* mantener AggregateVersion;
* mantener OccurredAt;
* mantener CorrelationId;
* mantener CausationId;
* utilizar Payload mínimo significativo;
* no incluir Aggregates completos;
* no incluir secretos;
* no depender de infraestructura;
* no reescribir eventos históricos;
* no publicarse cuando una operación falla;
* preservar causalidad;
* preservar orden por AggregateVersion;
* permitir consumidores idempotentes;
* separar Domain Events de Integration Events.

---

# Restricciones

No está permitido:

* modificar un Domain Event después de ocurrido;
* reutilizar EventId;
* utilizar Domain Events como Commands;
* publicar eventos de operaciones rechazadas;
* publicar eventos antes de validar invariantes;
* utilizar un evento para modificar directamente otro Aggregate;
* transportar Aggregate completo sin necesidad;
* incluir contraseñas;
* incluir tokens;
* incluir claves privadas;
* incluir secretos criptográficos;
* utilizar nombres técnicos como eventos de dominio;
* sobrescribir eventos históricos;
* asumir orden global entre distintos Aggregates;
* acoplar un Domain Event a Kafka, FIWARE o cualquier tecnología;
* transformar silenciosamente un Domain Event interno en contrato
  público permanente.

---

# Compatibilidad Arquitectónica

El modelo de Domain Events es compatible con:

* Domain-Driven Design;
* Tactical DDD;
* Clean Architecture;
* Hexagonal Architecture;
* CQRS;
* Event-Driven Architecture;
* Event Sourcing;
* Optimistic Concurrency;
* Transactional Outbox;
* arquitectura distribuida;
* consistencia eventual.

---

# Definición de Éxito

Los Domain Events del Aggregate **Assembly** representan de forma
oficial los hechos relevantes que ocurren durante la evolución de
una reunión dentro del ecosistema AURA.

Cada evento expresa un hecho consumado utilizando el lenguaje
ubicuo del dominio, posee identidad propia, referencia la
Assembly y Organization correspondientes, mantiene la versión del
Aggregate, timestamp del hecho, correlación y causalidad, y
transporta únicamente la información necesaria para representar
su significado.

Los eventos preservan el historial de Assembly sin reescribir
hechos anteriores, mantienen una secuencia coherente mediante
AggregateVersion y solamente se generan después de que la
Aggregate Root acepta una operación, valida Guards e invariantes y
produce un nuevo estado consistente.

Assembly utiliza Domain Events para comunicar hechos sin modificar
directamente otros Aggregates. Notification, Audit, Read Models,
Integration y otros procesos reaccionan posteriormente mediante
consistencia eventual y conservan sus propios límites de
consistencia.

Los Domain Events permanecen separados de Commands, Integration
Events y mecanismos técnicos de mensajería, permitiendo que el
modelo de dominio continúe independiente de infraestructura.

De esta forma, los Domain Events de Assembly proporcionan una
base inmutable, trazable, auditable, desacoplada y compatible con
Domain-Driven Design, CQRS, Event-Driven Architecture, Event
Sourcing y una arquitectura distribuida.
