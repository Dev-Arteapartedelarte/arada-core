# DOMAIN-013D — Integration Domain Events

Versión: 1.1

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Integration Management

Aggregate:
Integration

Autor:
ARADA

Documentos Relacionados:

- DOMAIN-013-Aggregate.md
- DOMAIN-013A-Lifecycle.md
- DOMAIN-013B-State-Machine.md
- DOMAIN-013C-Commands.md
- DOMAIN-013E-Invariants.md
- DOMAIN-013F-Permissions.md
- DOMAIN-013G-Repository-Contract.md
- DOMAIN-013H-Examples.md
- DOMAIN-013I-Versioning.md
- DOMAIN-013J-Consistency-Boundary.md
- DOMAIN-013K-Integration-Events.md
- DOMAIN-013L-Read-Model.md
- DOMAIN-013M-Test-Scenarios.md
- DOMAIN-013N-Performance-Rules.md
- DOMAIN-013O-Security-Model.md
- DOMAIN-013P-Extension-Points.md

---

# Objetivo

Este documento define formalmente los **Domain Events** del Aggregate
**Integration**.

Los Domain Events representan hechos significativos que ya ocurrieron
dentro del Consistency Boundary de Integration.

Permiten expresar mediante el lenguaje ubicuo de AURA la evolución
confirmada del Aggregate.

---

# Propósito

Los Domain Events permiten:

- representar hechos consumados;
- preservar trazabilidad;
- expresar cambios del Lifecycle;
- relacionar comportamiento con Version;
- alimentar Read Models;
- permitir colaboración desacoplada;
- proporcionar hechos para handlers internos de Integration Management;
- permitir una posterior transformación hacia Integration Events
  cuando exista un contrato explícito;
- mantener compatibilidad con CQRS;
- mantener compatibilidad con Event Sourcing.

---

# Principio Fundamental

Debe mantenerse:

```text
Domain Event

=

Confirmed Domain Fact
```

mientras:

```text
Command

=

Intent
```

Por lo tanto:

```text
ActivateIntegration
```

representa una intención.

Mientras:

```text
IntegrationActivated
```

representa un hecho consumado.

---

# Command versus Domain Event

La relación conceptual es:

```text
Command
    │
    ▼
Integration
    │
    ├── validates State
    ├── validates Guards
    ├── validates Invariants
    ├── validates Version
    └── performs behavior
            │
            ▼
       Domain Event
```

El Domain Event solamente existe cuando el hecho ocurrió realmente.

---

# Propiedad del Evento

Los Domain Events definidos en este documento pertenecen
conceptualmente al Aggregate:

```text
Integration
```

La Aggregate Root es responsable de producirlos como consecuencia de
comportamiento válido.

Otros Aggregates o Bounded Contexts pueden reaccionar a estos hechos.

No adquieren ownership sobre el evento original.

---

# Alcance

Los Domain Events de Integration describen exclusivamente hechos del
Aggregate Integration.

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

Voting

Document

Notification

Audit
```

Tampoco representan directamente hechos internos de:

```text
FIWARE

Municipal Systems

External Platforms

Infrastructure
```

---

# Eventos Oficiales

La versión 1.0 define exactamente los siguientes Domain Events:

```text
IntegrationCreated

IntegrationActivated

IntegrationSuspended

IntegrationReactivated

IntegrationArchived
```

No existen otros Domain Events oficiales en esta versión.

---

# Relación con Commands

Los Commands oficiales definidos en:

```text
DOMAIN-013C-Commands.md
```

se relacionan con los Domain Events de la siguiente forma:

```text
CreateIntegration
    │
    ▼
IntegrationCreated
```

```text
ActivateIntegration
    │
    ▼
IntegrationActivated
```

```text
SuspendIntegration
    │
    ▼
IntegrationSuspended
```

```text
ReactivateIntegration
    │
    ▼
IntegrationReactivated
```

```text
ArchiveIntegration
    │
    ▼
IntegrationArchived
```

---

# Relación con Lifecycle

Los eventos oficiales corresponden a las transiciones definidas en:

```text
DOMAIN-013A-Lifecycle.md
```

Conceptualmente:

```text
IntegrationCreated

No Integration → Draft
```

```text
IntegrationActivated

Draft → Active
```

```text
IntegrationSuspended

Active → Suspended
```

```text
IntegrationReactivated

Suspended → Active
```

```text
IntegrationArchived

Draft     → Archived

Active    → Archived

Suspended → Archived
```

---

# Relación con State Machine

Los Domain Events de cambio de estado solamente pueden producirse como
consecuencia de las transiciones permitidas por:

```text
DOMAIN-013B-State-Machine.md
```

Un Domain Event no puede utilizarse para crear una transición no
permitida.

---

# IntegrationCreated

`IntegrationCreated` representa el hecho de que una nueva Integration
fue creada formalmente.

Corresponde a:

```text
No Integration → Draft
```

---

# Significado de IntegrationCreated

El evento significa exclusivamente:

```text
A new Integration Aggregate was successfully created.
```

No significa:

- que una conexión técnica fue establecida;
- que un sistema externo respondió;
- que FIWARE fue sincronizado;
- que un broker fue conectado;
- que la Integration está Active.

---

# Estado después de IntegrationCreated

Después del hecho:

```text
State = Draft
```

---

# IntegrationCreated y Version

`IntegrationCreated` debe representar la Version inicial del
Aggregate conforme a:

```text
DOMAIN-013I-Versioning.md
```

---

# IntegrationActivated

`IntegrationActivated` representa el hecho de que una Integration
Draft fue formalmente habilitada.

Corresponde a:

```text
Draft → Active
```

---

# Significado de IntegrationActivated

El evento significa:

```text
The Integration was formally activated.
```

No significa:

```text
Infrastructure connected.
```

---

# IntegrationActivated no es Conectividad

Debe mantenerse:

```text
IntegrationActivated

≠

BrokerConnected
```

y:

```text
IntegrationActivated

≠

ExternalSystemAvailable
```

y:

```text
IntegrationActivated

≠

FIWAREConnected
```

---

# Estado después de IntegrationActivated

Después del hecho:

```text
State = Active
```

---

# IntegrationSuspended

`IntegrationSuspended` representa el hecho de que una Integration
Active fue suspendida formalmente.

Corresponde a:

```text
Active → Suspended
```

---

# Significado de IntegrationSuspended

El evento significa:

```text
The Integration was formally suspended.
```

No significa:

- network failure;
- timeout;
- endpoint unavailable;
- broker failure;
- FIWARE failure;
- municipal system failure.

---

# Suspensión Formal

Debe mantenerse:

```text
IntegrationSuspended

=

Confirmed Domain Suspension
```

y no:

```text
IntegrationSuspended

=

Technical Failure Notification
```

---

# Estado después de IntegrationSuspended

Después del hecho:

```text
State = Suspended
```

---

# IntegrationReactivated

`IntegrationReactivated` representa el hecho de que una Integration
Suspended fue habilitada nuevamente.

Corresponde a:

```text
Suspended → Active
```

---

# Significado de IntegrationReactivated

El evento significa:

```text
The Integration was formally reactivated.
```

No significa simplemente que un sistema externo volvió a estar
disponible.

---

# Reactivación Formal

Debe mantenerse:

```text
IntegrationReactivated

≠

TechnicalRecoveryDetected
```

---

# Estado después de IntegrationReactivated

Después del hecho:

```text
State = Active
```

---

# IntegrationArchived

`IntegrationArchived` representa el hecho de que una Integration fue
retirada formalmente del ciclo operativo.

Puede corresponder a:

```text
Draft → Archived
```

```text
Active → Archived
```

```text
Suspended → Archived
```

---

# Significado de IntegrationArchived

El evento significa:

```text
The Integration was formally archived.
```

No significa:

```text
The Integration was physically deleted.
```

---

# Estado después de IntegrationArchived

Después del hecho:

```text
State = Archived
```

Archived permanece terminal.

---

# IntegrationArchived y Estado Previo

Debido a que ArchiveIntegration puede ejecutarse desde diferentes
estados válidos, el hecho debe preservar conceptualmente el estado
previo cuando sea necesario para representar correctamente la
transición.

Conceptualmente:

```text
PreviousState

Archived
```

La estructura exacta del Payload debe preservar únicamente la
información necesaria.

---

# Estructura General

Todo Domain Event de Integration debe contener conceptualmente como
mínimo:

```text
EventId

EventType

IntegrationId

AggregateVersion

OccurredAt

CorrelationId

CausationId

Payload
```

CorrelationId y CausationId solamente estarán presentes cuando
correspondan al flujo y al contrato aplicable.

---

# EventId

EventId identifica un único Domain Event.

Debe:

- ser único;
- ser inmutable;
- identificar un único hecho;
- no reutilizarse;
- ser independiente de IntegrationId.

Debe mantenerse:

```text
EventId

≠

IntegrationId
```

---

# EventType

EventType representa el nombre semántico del hecho.

Los valores oficiales versión 1.0 son:

```text
IntegrationCreated

IntegrationActivated

IntegrationSuspended

IntegrationReactivated

IntegrationArchived
```

---

# Nombres de Eventos

Los Domain Events deben utilizar la forma conceptual:

```text
Aggregate + PastTenseFact
```

Deben expresar hechos consumados.

---

# IntegrationId

IntegrationId identifica el Aggregate que produjo el Domain Event.

Permanece inmutable dentro del evento.

---

# AggregateVersion

AggregateVersion representa la Version resultante del Aggregate
después del hecho.

Debe mantenerse:

```text
DomainEvent.AggregateVersion

=

Resulting Integration.Version
```

---

# AggregateVersion no es Contract Version

Debe mantenerse:

```text
AggregateVersion

≠

Integration Contract Version
```

---

# AggregateVersion no es External Version

También:

```text
AggregateVersion

≠

External System Version
```

---

# OccurredAt

OccurredAt representa el momento en que el hecho de dominio ocurrió.

Debe mantenerse:

```text
Domain Event OccurredAt

≠

Message Delivery Time
```

y:

```text
Domain Event OccurredAt

≠

Projection Processing Time
```

---

# CorrelationId

Cuando corresponda, CorrelationId permite relacionar el hecho con un
flujo de negocio mayor.

Debe mantenerse:

```text
CorrelationId

≠

EventId
```

y:

```text
CorrelationId

≠

IntegrationId
```

---

# CausationId

Cuando corresponda, CausationId identifica el hecho o intención causal
inmediata reconocida por el contrato.

Debe mantenerse:

```text
CausationId

≠

EventId
```

salvo que una relación concreta de causalidad explícita así lo
determine en un flujo posterior.

---

# Payload

Payload contiene exclusivamente la información necesaria para
representar el hecho.

Debe mantenerse:

```text
Domain Event Payload

≠

Full Aggregate Snapshot
```

---

# Payload Mínimo

Todo Payload debe aplicar:

```text
Minimum Necessary Domain Information
```

No debe incorporar información solamente porque esté disponible
técnicamente.

---

# Payload de IntegrationCreated

Puede preservar conceptualmente:

```text
IntegrationId

State = Draft
```

y la información formal de dominio necesaria definida para la creación.

No debe incorporar detalles de Infrastructure.

---

# Payload de IntegrationActivated

Debe representar conceptualmente:

```text
IntegrationId

PreviousState = Draft

NewState = Active
```

cuando dichos valores sean necesarios para expresar el hecho.

---

# Payload de IntegrationSuspended

Debe representar conceptualmente:

```text
IntegrationId

PreviousState = Active

NewState = Suspended
```

y únicamente información adicional formalmente perteneciente al hecho
de suspensión.

---

# Payload de IntegrationReactivated

Debe representar conceptualmente:

```text
IntegrationId

PreviousState = Suspended

NewState = Active
```

---

# Payload de IntegrationArchived

Debe permitir representar:

```text
IntegrationId

PreviousState

NewState = Archived
```

debido a las diferentes rutas válidas de archivado.

---

# PreviousState

PreviousState dentro de un evento de transición representa el estado
confirmado inmediatamente anterior cuando sea necesario para expresar
el hecho.

No constituye un segundo estado activo del Aggregate.

---

# NewState

NewState representa el estado resultante confirmado.

Debe coincidir con la State Machine.

---

# Inmutabilidad del Evento

Una vez producido, un Domain Event es inmutable.

Debe mantenerse:

```text
Confirmed Domain Event

≠

Mutable Operational Object
```

---

# Eventos y Versioning

Cada modificación válida produce una nueva Version conforme a:

```text
DOMAIN-013I-Versioning.md
```

El evento debe relacionarse con la Version resultante.

---

# Ejemplo Conceptual de Versionado

Una evolución válida puede representarse como:

```text
Version 1
IntegrationCreated

Version 2
IntegrationActivated

Version 3
IntegrationSuspended

Version 4
IntegrationReactivated

Version 5
IntegrationArchived
```

Esta secuencia es ilustrativa de una evolución válida.

No obliga a que toda Integration recorra exactamente todos esos
estados.

---

# Orden de Eventos

Dentro de una misma Integration:

```text
AggregateVersion
```

preserva el orden lógico de evolución.

---

# No Orden Global

La versión 1.0 no define un orden global entre eventos pertenecientes
a diferentes IntegrationId.

Debe mantenerse:

```text
Per Aggregate Ordering

≠

Global Ordering
```

---

# Eventos y Concurrencia

Un Domain Event de modificación solamente puede considerarse válido si
la operación correspondiente supera el control de concurrencia.

Si:

```text
ExpectedVersion

≠

PersistedVersion
```

la modificación se rechaza.

No debe producirse un nuevo Domain Event de éxito.

---

# No Event on Rejected Command

Un Command rechazado no genera un Domain Event de éxito.

Conceptualmente:

```text
Command
    │
    ▼
Rejected
    │
    ├── State unchanged
    ├── Version unchanged
    ├── UpdatedAt unchanged
    └── No success Domain Event
```

---

# No Event on Invalid Transition

Una transición no permitida por:

```text
DOMAIN-013B-State-Machine.md
```

no puede producir el correspondiente Domain Event.

---

# No Event on Invariant Failure

Si una Invariant falla:

```text
No success Domain Event
```

---

# No Event on Permission Failure

Si la intención no está autorizada:

```text
No success Domain Event
```

---

# No Event on Concurrency Conflict

Si existe:

```text
ConcurrencyConflict
```

no debe producirse un nuevo Domain Event de éxito.

---

# Persistencia y Confirmación

Un hecho solamente debe tratarse como confirmado cuando la modificación
correspondiente ha sido aceptada dentro del Consistency Boundary y su
persistencia se ha confirmado conforme al Repository Contract.

---

# Persistence Failure

Un fallo de persistencia no constituye:

```text
IntegrationFailed
```

ni otro Domain Event del Lifecycle.

---

# Repository

El Repository no inventa Domain Events.

Debe mantenerse:

```text
Repository

≠

Domain Event Authority
```

---

# Repository Save

`save()` persiste el Aggregate.

No debe producir por sí mismo:

```text
IntegrationCreated

IntegrationActivated

IntegrationSuspended

IntegrationReactivated

IntegrationArchived
```

La producción corresponde al comportamiento del Aggregate.

---

# Domain Events versus Repository Events

Un evento de:

```text
DatabaseInserted

RowUpdated

AggregateSaved
```

no constituye un Domain Event de Integration.

---

# Eventos Técnicos Prohibidos

No pertenecen al Aggregate Domain Events como:

```text
IntegrationSaved

IntegrationLoaded

IntegrationPersisted

IntegrationDatabaseUpdated

IntegrationCacheRefreshed

IntegrationHttpRequestSent

IntegrationHttpRequestCompleted

IntegrationMessagePublished

IntegrationKafkaPublished

IntegrationBrokerConnected

IntegrationBrokerDisconnected

IntegrationFIWARESynced

IntegrationTokenRefreshed

IntegrationRetryScheduled
```

Estos representan hechos técnicos.

No hechos propios del dominio Integration.

---

# No IntegrationConnected

La versión 1.0 no define:

```text
IntegrationConnected
```

porque Connected no pertenece al Lifecycle.

---

# No IntegrationDisconnected

La versión 1.0 no define:

```text
IntegrationDisconnected
```

---

# No IntegrationFailed

La versión 1.0 no define:

```text
IntegrationFailed
```

porque Failed no pertenece al Lifecycle.

---

# No IntegrationRetried

La versión 1.0 no define:

```text
IntegrationRetried
```

porque retry técnico no constituye comportamiento del Aggregate.

---

# No IntegrationDeleted

La versión 1.0 no define:

```text
IntegrationDeleted
```

Physical Deletion no forma parte del Lifecycle.

---

# No IntegrationCancelled

La versión 1.0 no define:

```text
IntegrationCancelled
```

Cancelled no forma parte del Lifecycle.

---

# No IntegrationUpdated

La versión 1.0 no define un evento genérico:

```text
IntegrationUpdated
```

Los hechos deben expresar significado específico del dominio.

---

# Granularidad de Eventos

Los eventos deben ser suficientemente específicos para preservar el
lenguaje ubicuo.

Se prefiere:

```text
IntegrationActivated

IntegrationSuspended

IntegrationReactivated

IntegrationArchived
```

sobre:

```text
IntegrationChanged
```

---

# Technical Failure no es Domain Event

Debe mantenerse:

```text
Timeout

NetworkFailure

BrokerFailure

EndpointUnavailable

FIWAREUnavailable

MunicipalSystemUnavailable

≠

Integration Domain Event
```

por definición de la versión 1.0.

---

# Technical Recovery no es Domain Event

Del mismo modo:

```text
BrokerRecovered

NetworkRecovered

ExternalSystemRecovered

FIWARERecovered
```

no son Domain Events de Integration.

---

# Domain Event versus Integration Event

Debe mantenerse:

```text
Domain Event

≠

Integration Event
```

Los eventos definidos aquí pertenecen al dominio Integration.

---

# No Mapeo Automático

Un Domain Event no genera automáticamente un Integration Event.

Debe mantenerse:

```text
IntegrationCreated

≠

Mandatory External Publication
```

La misma regla se aplica a todos los eventos oficiales.

---

# Publicación Externa

Si un hecho debe cruzar un Bounded Context o sistema, su transformación
se define mediante:

```text
DOMAIN-013K-Integration-Events.md
```

cuando exista un contrato explícito.

---

# Fallo de Publicación

Una vez confirmado el hecho de dominio, un fallo posterior de
publicación externa no modifica retrospectivamente el evento.

Debe mantenerse:

```text
External Publication Failure

≠

Domain Event Rollback
```

---

# Retry de Publicación

Un retry técnico de publicación no produce un nuevo Domain Event.

Debe mantenerse:

```text
Message Retry

≠

New Domain Fact
```

---

# Retransmisión

La retransmisión técnica del mismo evento no constituye un nuevo hecho.

El mismo hecho mantiene su:

```text
EventId
```

conceptual cuando se está representando el mismo Domain Event.

---

# Eventos Duplicados

Dos eventos distintos pueden compartir EventType cuando representan
hechos reales diferentes.

Por ejemplo:

```text
IntegrationActivated
```

puede ocurrir más de una vez durante la vida de una Integration si
existe previamente una suspensión válida y posterior reactivación.

Sin embargo, en ese caso el hecho posterior de retorno a Active está
representado por:

```text
IntegrationReactivated
```

conforme al lenguaje oficial de versión 1.0.

Por lo tanto cada hecho conserva su EventType semánticamente correcto.

---

# Integridad Histórica

Un evento confirmado no debe reescribirse para representar un hecho
posterior.

Debe mantenerse:

```text
Historical Domain Event

≠

Mutable Current State
```

---

# Evento y Estado Actual

Un Domain Event histórico representa el estado resultante en el
momento del hecho.

No debe reinterpretarse utilizando únicamente el State actual.

---

# IntegrationArchived Histórico

Una vez ocurrido:

```text
IntegrationArchived
```

no puede sustituirse retrospectivamente por otro evento para reactivar
la misma Integration.

Archived es terminal en versión 1.0.

---

# Correlation y Eventos

Eventos pertenecientes a diferentes Aggregates pueden compartir:

```text
CorrelationId
```

sin compartir:

- Aggregate;
- Version;
- Consistency Boundary;
- ownership.

---

# Causation y Eventos

CausationId puede relacionar hechos causalmente.

No cambia ownership.

---

# Actor

Cuando la información del actor forme parte del hecho y del contrato
correspondiente, el evento puede preservar una referencia:

```text
ActorId
```

sin incorporar el Aggregate Citizen, Membership o Role.

---

# ActorId no es Obligatorio Universal

Este documento no establece ActorId como campo obligatorio para todos
los eventos.

Solamente debe incluirse cuando:

- esté disponible;
- sea aplicable;
- forme parte del contrato del hecho.

---

# ActorId no es Permission

Debe mantenerse:

```text
ActorId

≠

Authorization
```

---

# Datos Ausentes

Un Domain Event no debe inventar información ausente.

Debe mantenerse:

```text
Missing Domain Information

≠

Fabricated Event Data
```

---

# Credenciales

Los Domain Events de Integration no deben contener:

```text
Password

AccessToken

RefreshToken

ApiKey

ClientSecret

PrivateKey

Secret
```

---

# Security

La información incluida en los Domain Events debe respetar:

```text
DOMAIN-013O-Security-Model.md
```

---

# Data Minimization

Los Domain Events deben contener únicamente información necesaria para
representar el hecho.

Debe mantenerse:

```text
Source Payload

≠

Automatic Domain Event Payload
```

---

# External Payload

Un Payload recibido desde un sistema externo no se copia
automáticamente dentro de un Domain Event.

---

# Domain Model Protection

Los eventos deben utilizar conceptos de AURA.

No deben exponer estructuras internas de sistemas externos como si
fueran conceptos propios de Integration.

---

# FIWARE

Los Domain Events no dependen directamente de:

```text
FIWARE

NGSI-LD

Context Broker

Orion
```

---

# FIWARE Entity

Una FIWARE Entity no forma parte automáticamente del Payload de un
Domain Event.

---

# Sistemas Municipales

Un modelo municipal no determina la estructura de los Domain Events de
Integration.

---

# Protocolos

Los eventos son independientes de:

```text
HTTP

REST

GraphQL

MQTT

AMQP
```

---

# Brokers

Los eventos son independientes de:

```text
Kafka

RabbitMQ

NATS
```

o cualquier tecnología equivalente.

---

# Serialización

La representación serializada de un Domain Event pertenece a capas
externas.

Puede materializarse mediante diferentes formatos sin modificar su
significado conceptual.

Debe mantenerse:

```text
Serialization Format

≠

Domain Event Semantics
```

---

# Read Models

Los Domain Events pueden alimentar Read Models definidos en:

```text
DOMAIN-013L-Read-Model.md
```

---

# Projection

Conceptualmente:

```text
Domain Event
    │
    ▼
Projection
    │
    ▼
Read Model
```

La Projection no modifica el evento original.

---

# Projection Failure

Un fallo de Projection no invalida retrospectivamente un Domain Event
confirmado.

---

# Projection Retry

Un retry de Projection no produce un nuevo Domain Event.

---

# Projection Rebuild

Reconstruir un Read Model no vuelve a producir hechos de dominio.

Debe mantenerse:

```text
Projection Rebuild

≠

Domain Event Re-Creation
```

---

# Audit

Los Domain Events de Integration pueden constituir hechos consumibles
por Audit cuando exista el contrato correspondiente.

Debe mantenerse:

```text
Integration Domain Event

≠

Audit Aggregate
```

---

# Audit no Posee el Evento

Audit puede preservar una representación auditable del hecho.

El Domain Event original continúa perteneciendo a Integration.

---

# Notification

Un Domain Event puede originar una necesidad posterior de Notification
cuando exista una regla o proceso correspondiente.

Notification no forma parte del evento ni del Aggregate Integration.

---

# Consistency Boundary

Un Domain Event representa un hecho confirmado dentro del Consistency
Boundary de:

```text
Integration
```

No confirma simultáneamente cambios en otros Aggregates.

---

# No Cross-Aggregate Event

`IntegrationActivated` no significa que:

```text
Organization changed

Citizen changed

Assembly changed

Audit changed

External System changed
```

---

# External Consistency

Otros contextos sólo pueden observar Integration Events explícitos
posteriormente.

La consistencia externa permanece eventual.

---

# No Distributed Event Commit

La existencia de un Domain Event no requiere que un sistema externo
confirme simultáneamente el mismo hecho.

---

# CQRS

Los Domain Events son compatibles con CQRS.

Conceptualmente:

```text
Command
    │
    ▼
Integration Aggregate
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

---

# Event Sourcing

Los Domain Events son compatibles con Event Sourcing.

Event Sourcing no es obligatorio.

---

# Event Sourcing Compatibility

Si Event Sourcing fuese utilizado, la secuencia de eventos debe poder
reconstruir conceptualmente la evolución válida del Aggregate.

---

# Source of Truth

Este documento no establece que el Event Stream deba ser la estrategia
física obligatoria de Source of Truth.

Esa decisión no pertenece a esta definición conceptual.

---

# Replay

Replay no produce nuevos Domain Events.

Debe mantenerse:

```text
Replay

≠

New Domain Fact
```

---

# Rehydration

Rehidratar una Integration no produce:

```text
IntegrationCreated

IntegrationActivated

IntegrationSuspended

IntegrationReactivated

IntegrationArchived
```

como hechos nuevos.

---

# Snapshot

Un Snapshot técnico no constituye Domain Event.

---

# Cache

Un cambio de Cache no constituye Domain Event.

---

# Outbox

Un cambio de estado de Outbox no constituye Domain Event.

---

# Queue

Un cambio de estado de Queue no constituye Domain Event.

---

# Broker

Un ACK de Broker no constituye Domain Event del Aggregate.

---

# Delivery

Delivery success o delivery failure no constituye por sí mismo un
Domain Event de Integration.

---

# Monitoring

Un resultado de Monitoring no constituye Domain Event.

---

# Health Check

Un resultado:

```text
Healthy

Unhealthy
```

no produce Domain Events del Lifecycle.

---

# Metrics

Cambios en:

```text
latency

throughput

error rate

queue depth
```

no producen Domain Events del Aggregate.

---

# Deployment

Un Deployment no produce Domain Event del Aggregate.

---

# Restart

Un Restart técnico no produce Domain Event.

---

# Credential Rotation

La rotación técnica de una credencial no produce Domain Event de
Integration versión 1.0.

---

# Token Expiration

La expiración de un token no produce:

```text
IntegrationSuspended
```

automáticamente.

---

# Technical Security Event

Un incidente técnico de Security no constituye automáticamente un
Domain Event del Aggregate.

---

# No Recursive Integration Events

Un Domain Event de Integration no debe generar automáticamente otro
Domain Event solamente porque fue publicado o consumido técnicamente.

---

# No Recursive Audit

La auditoría de un Domain Event no produce automáticamente una nueva
modificación de Integration.

---

# Test Scenarios

Los Domain Events deben validarse mediante:

```text
DOMAIN-013M-Test-Scenarios.md
```

---

# Validaciones Mínimas de Eventos

Los escenarios deben comprobar conceptualmente:

```text
correct EventType

correct IntegrationId

correct AggregateVersion

correct resulting State

correct OccurredAt semantics

correct CorrelationId when applicable

correct CausationId when applicable

minimum necessary Payload

event generated after valid Command

event not generated after rejected Command

no credential leakage

historical meaning preserved
```

---

# IntegrationCreated Test Conceptual

Debe verificarse:

```text
Given

No Integration

When

CreateIntegration succeeds

Then

State = Draft

and

IntegrationCreated exists
```

---

# IntegrationActivated Test Conceptual

```text
Given

State = Draft

When

ActivateIntegration succeeds

Then

State = Active

and

IntegrationActivated exists
```

---

# IntegrationSuspended Test Conceptual

```text
Given

State = Active

When

SuspendIntegration succeeds

Then

State = Suspended

and

IntegrationSuspended exists
```

---

# IntegrationReactivated Test Conceptual

```text
Given

State = Suspended

When

ReactivateIntegration succeeds

Then

State = Active

and

IntegrationReactivated exists
```

---

# IntegrationArchived Test Conceptual

```text
Given

State ∈ {Draft, Active, Suspended}

When

ArchiveIntegration succeeds

Then

State = Archived

and

IntegrationArchived exists
```

---

# Invalid Event Scenario

Ejemplo:

```text
Given

State = Archived

When

ActivateIntegration

Then

Rejected
```

No debe producir:

```text
IntegrationActivated
```

---

# Evento y PreviousState

Todo evento que represente transición debe ser coherente con el estado
permitido de origen.

Por ejemplo:

```text
IntegrationSuspended
```

solamente puede representar:

```text
Active → Suspended
```

---

# Evento y Resulting State

Del mismo modo:

```text
IntegrationReactivated
```

debe resultar en:

```text
Active
```

---

# Evento y Terminalidad

Después de:

```text
IntegrationArchived
```

no puede existir posteriormente para la misma Integration una
transición válida de Lifecycle en versión 1.0.

---

# Regla para Incorporar un Nuevo Domain Event

Un nuevo Domain Event solamente puede incorporarse cuando represente
un nuevo hecho real del dominio.

Debe responder:

```text
Did something relevant to Integration actually happen?

Can the fact be expressed in past tense?

Does it belong to Integration?

Was it produced by valid Aggregate behavior?

Does it preserve existing Invariants?

Is its relationship with Version clear?
```

---

# Impacto de un Nuevo Evento

Incorporar un nuevo Domain Event exige revisar cuando corresponda:

```text
DOMAIN-013-Aggregate.md

DOMAIN-013A-Lifecycle.md

DOMAIN-013B-State-Machine.md

DOMAIN-013C-Commands.md

DOMAIN-013D-Domain-Events.md

DOMAIN-013E-Invariants.md

DOMAIN-013F-Permissions.md

DOMAIN-013I-Versioning.md

DOMAIN-013J-Consistency-Boundary.md

DOMAIN-013K-Integration-Events.md

DOMAIN-013L-Read-Model.md

DOMAIN-013M-Test-Scenarios.md

DOMAIN-013O-Security-Model.md

DOMAIN-013P-Extension-Points.md
```

---

# Eventos Futuros no Definidos

La versión 1.0 no define:

```text
IntegrationConnected

IntegrationDisconnected

IntegrationFailed

IntegrationRetried

IntegrationDeleted

IntegrationCancelled

IntegrationExpired

IntegrationReset

IntegrationUpdated

IntegrationSynchronized

IntegrationPublished
```

Estos eventos no deben incorporarse aisladamente.

---

# Regla de No Inferencia

Debe mantenerse:

```text
Technical Activity

≠

Permission to Create Domain Event
```

y:

```text
External Event

≠

Integration Domain Event
```

---

# Reglas Fundamentales

Los Domain Events de Integration deben cumplir:

1. Domain Event representa un hecho consumado.
2. Command representa intención.
3. La versión 1.0 define exactamente IntegrationCreated,
   IntegrationActivated, IntegrationSuspended,
   IntegrationReactivated e IntegrationArchived.
4. IntegrationCreated corresponde a No Integration → Draft.
5. IntegrationActivated corresponde a Draft → Active.
6. IntegrationSuspended corresponde a Active → Suspended.
7. IntegrationReactivated corresponde a Suspended → Active.
8. IntegrationArchived corresponde a Draft → Archived,
   Active → Archived o Suspended → Archived.
9. Un evento pertenece exclusivamente al Aggregate Integration.
10. Otros Aggregates no adquieren ownership del evento.
11. EventId es único.
12. EventId es inmutable.
13. EventId no es IntegrationId.
14. EventType utiliza lenguaje ubicuo.
15. IntegrationId identifica el Aggregate productor.
16. AggregateVersion representa la Version resultante.
17. AggregateVersion no es Contract Version.
18. AggregateVersion no es External System Version.
19. OccurredAt representa el momento del hecho de dominio.
20. OccurredAt no es delivery time.
21. CorrelationId se utiliza solamente cuando corresponda.
22. CorrelationId no crea Consistency Boundary compartido.
23. CausationId se utiliza solamente cuando corresponda.
24. CausationId no concede Mutation Authority.
25. Payload debe contener información mínima necesaria.
26. Payload no es Aggregate Snapshot.
27. External Payload no se copia automáticamente.
28. Información ausente no se fabrica.
29. Los eventos son inmutables.
30. Un evento confirmado preserva significado histórico.
31. AggregateVersion preserva orden lógico por IntegrationId.
32. No existe orden global obligatorio entre diferentes
    IntegrationId.
33. Una operación rechazada no produce Domain Event de éxito.
34. Invalid Transition no produce Domain Event de éxito.
35. Invariant Failure no produce Domain Event de éxito.
36. Permission Failure no produce Domain Event de éxito.
37. ConcurrencyConflict no produce Domain Event de éxito.
38. Repository no inventa Domain Events.
39. Persistence Failure no crea un estado ni evento Failed.
40. Domain Event no es Repository Event.
41. Domain Event no es Infrastructure Event.
42. IntegrationConnected no existe en versión 1.0.
43. IntegrationDisconnected no existe en versión 1.0.
44. IntegrationFailed no existe en versión 1.0.
45. IntegrationRetried no existe en versión 1.0.
46. IntegrationDeleted no existe en versión 1.0.
47. IntegrationCancelled no existe en versión 1.0.
48. IntegrationUpdated genérico no existe en versión 1.0.
49. Technical Failure no produce Domain Event automáticamente.
50. Technical Recovery no produce Domain Event automáticamente.
51. Timeout no produce IntegrationSuspended.
52. Broker Failure no produce IntegrationSuspended.
53. FIWARE Failure no produce IntegrationSuspended.
54. Municipal System Failure no produce IntegrationSuspended.
55. Domain Event no es Integration Event.
56. Domain Event no genera Integration Event automáticamente.
57. External Publication Failure no revierte el Domain Event.
58. Retry de publicación no crea un nuevo Domain Event.
59. Retransmisión del mismo hecho no constituye un nuevo hecho.
60. Confirmed Event no se reescribe.
61. Historical Event no es Current State.
62. ActorId no es obligatorio universalmente.
63. ActorId no representa Authorization.
64. Los eventos no contienen passwords.
65. Los eventos no contienen Access Tokens.
66. Los eventos no contienen Refresh Tokens.
67. Los eventos no contienen API Keys.
68. Los eventos no contienen Private Keys.
69. Los eventos no contienen Client Secrets.
70. Los eventos no dependen de FIWARE.
71. Los eventos no dependen de NGSI-LD.
72. Los eventos no dependen de sistemas municipales.
73. Los eventos no dependen de protocolos.
74. Los eventos no dependen de brokers.
75. Serialization Format no modifica Event Semantics.
76. Read Models pueden consumir eventos.
77. Projection Failure no invalida eventos confirmados.
78. Projection Retry no crea eventos nuevos.
79. Projection Rebuild no crea hechos nuevos.
80. Audit sólo puede recibir Integration Events explícitos sin adquirir ownership.
81. Notification sólo puede reaccionar a Integration Events explícitos mediante
un Command propio.
82. Un evento confirma únicamente el cambio dentro de Integration.
83. Un evento no confirma simultáneamente cambios en otros
    Aggregates.
84. Consistencia externa permanece eventual.
85. No existe Distributed Event Commit obligatorio.
86. CQRS permanece compatible.
87. Event Sourcing permanece compatible pero no obligatorio.
88. Replay no crea nuevos Domain Events.
89. Rehydration no crea nuevos Domain Events.
90. Snapshot no es Domain Event.
91. Cache change no es Domain Event.
92. Outbox state change no es Domain Event.
93. Queue state change no es Domain Event.
94. Broker ACK no es Domain Event.
95. Health Check no es Domain Event.
96. Metrics change no es Domain Event.
97. Deployment no es Domain Event.
98. Credential rotation no es Domain Event de Integration versión
    1.0.
99. Todo nuevo Domain Event requiere un nuevo hecho real del dominio.
100. Ningún Domain Event adicional forma parte de versión 1.0 sin
     definición formal.

---

# Restricciones

No está permitido:

- utilizar Commands como hechos históricos;
- utilizar Domain Events como Commands;
- producir un Domain Event antes de confirmar el comportamiento;
- producir IntegrationCreated sin creación válida;
- producir IntegrationActivated fuera de Draft → Active;
- producir IntegrationSuspended fuera de Active → Suspended;
- producir IntegrationReactivated fuera de Suspended → Active;
- producir IntegrationArchived desde un estado no permitido;
- producir eventos de éxito después de una operación rechazada;
- producir eventos de éxito después de ConcurrencyConflict;
- modificar un Domain Event confirmado;
- reutilizar EventId para hechos diferentes;
- utilizar IntegrationId como EventId;
- utilizar AggregateVersion como Contract Version;
- utilizar estados técnicos como EventType;
- utilizar nombres de infraestructura como Domain Events;
- utilizar IntegrationConnected;
- utilizar IntegrationDisconnected;
- utilizar IntegrationFailed;
- utilizar IntegrationRetried;
- utilizar IntegrationDeleted;
- utilizar IntegrationCancelled;
- utilizar IntegrationUpdated genérico;
- transformar automáticamente cada Domain Event en Integration Event;
- copiar automáticamente Payloads externos completos;
- incluir credenciales;
- incluir secretos;
- incluir Access Tokens;
- incluir API Keys;
- incluir Private Keys;
- incluir Client Secrets;
- convertir timeout en IntegrationSuspended;
- convertir Broker Failure en IntegrationSuspended;
- convertir FIWARE Failure en IntegrationSuspended;
- convertir Technical Recovery en IntegrationReactivated;
- utilizar eventos de Repository como Domain Events;
- utilizar eventos de Projection como Domain Events;
- utilizar eventos de Cache como Domain Events;
- utilizar eventos de Queue como Domain Events;
- utilizar eventos de Outbox como Domain Events;
- utilizar eventos de Monitoring como Domain Events;
- introducir un nuevo Domain Event por conveniencia técnica;
- introducir un nuevo Domain Event sin revisar los contratos de
  dominio afectados.

---

# Compatibilidad Arquitectónica

Los Domain Events de Integration son compatibles con:

- Domain-Driven Design;
- Aggregate Pattern;
- Domain Event Pattern;
- Clean Architecture;
- Hexagonal Architecture;
- SOLID;
- CQRS;
- Event-Driven Architecture;
- Event Sourcing Compatible;
- Optimistic Concurrency Control;
- consistencia eventual;
- High Cohesion;
- Low Coupling.

Estas compatibilidades no imponen:

- broker;
- protocolo;
- serialización;
- framework;
- base de datos;
- proveedor;
- FIWARE;
- sistema municipal.

---

# Definición de Éxito

Los Domain Events del Aggregate **Integration** representan de manera
inequívoca los hechos confirmados de su Lifecycle versión 1.0:

```text
CreateIntegration
    │
    ▼
IntegrationCreated
    │
    ▼
Draft

ActivateIntegration
    │
    ▼
IntegrationActivated
    │
    ▼
Active

SuspendIntegration
    │
    ▼
IntegrationSuspended
    │
    ▼
Suspended

ReactivateIntegration
    │
    ▼
IntegrationReactivated
    │
    ▼
Active

ArchiveIntegration
    │
    ▼
IntegrationArchived
    │
    ▼
Archived
```

El modelo garantiza que:

- los Commands expresen intención;
- los Domain Events expresen hechos consumados;
- cada evento pertenezca a Integration;
- EventId identifique un único hecho;
- IntegrationId identifique al Aggregate productor;
- AggregateVersion represente la Version resultante;
- OccurredAt represente el momento del hecho;
- CorrelationId y CausationId se utilicen únicamente cuando
  correspondan;
- Payload permanezca mínimo;
- información ausente no sea fabricada;
- credenciales permanezcan fuera de los eventos;
- fallos técnicos no se conviertan en hechos del Lifecycle;
- conectividad no se confunda con activación;
- suspensión formal no se confunda con indisponibilidad técnica;
- reactivación formal no se confunda con recuperación técnica;
- archivado no se confunda con eliminación;
- operaciones rechazadas no produzcan eventos de éxito;
- ConcurrencyConflict no produzca eventos de éxito;
- Repository no genere hechos del dominio;
- Domain Event e Integration Event permanezcan diferenciados;
- publicación externa sea independiente del hecho ya confirmado;
- Read Models puedan proyectar hechos sin modificarlos;
- Audit pueda consumir hechos sin adquirir ownership;
- consistencia externa permanezca eventual;
- Event Sourcing permanezca compatible pero no obligatorio;
- Replay y Rehydration no produzcan hechos nuevos;
- Infrastructure no defina la semántica de los eventos;
- cualquier nuevo Domain Event requiera una definición formal y
  coordinada.

De esta forma, `DOMAIN-013D-Domain-Events.md` establece formalmente
los Domain Events oficiales del Aggregate **Integration** conforme al
patrón consolidado de AURA Core.