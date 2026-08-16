# DOMAIN-013C — Integration Commands

Versión: 1.0

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
- DOMAIN-013D-Domain-Events.md
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

Este documento define formalmente los **Commands** del Aggregate
**Integration**.

Los Commands representan intenciones explícitas de modificar una
Integration dentro de su propio Consistency Boundary.

Todo Command debe:

- expresar una intención del dominio;
- utilizar el lenguaje ubicuo de Integration;
- dirigirse a una única Aggregate Root;
- respetar Lifecycle;
- respetar State Machine;
- respetar Invariants;
- respetar Permissions;
- respetar Versioning;
- producir cambios solamente cuando la operación sea válida;
- producir Domain Events cuando corresponda.

---

# Principio Fundamental

Debe mantenerse:

```text
Command

=

Intent
```

mientras:

```text
Domain Event

=

Confirmed Fact
```

Por lo tanto, un Command expresa algo que se desea realizar.

Un Domain Event expresa algo que ya ocurrió.

---

# Commands Oficiales

La versión 1.0 define exactamente los siguientes Commands:

```text
CreateIntegration

ActivateIntegration

SuspendIntegration

ReactivateIntegration

ArchiveIntegration
```

No existen otros Commands oficiales en esta versión.

---

# Relación con Lifecycle

Los Commands corresponden a las transiciones oficiales definidas en:

```text
DOMAIN-013A-Lifecycle.md
```

y:

```text
DOMAIN-013B-State-Machine.md
```

Conceptualmente:

```text
CreateIntegration

No Integration → Draft
```

```text
ActivateIntegration

Draft → Active
```

```text
SuspendIntegration

Active → Suspended
```

```text
ReactivateIntegration

Suspended → Active
```

```text
ArchiveIntegration

Draft     → Archived

Active    → Archived

Suspended → Archived
```

---

# Command versus Transition

Un Command no constituye por sí mismo una transición.

Debe mantenerse:

```text
Command Received

≠

State Changed
```

La transición ocurre solamente cuando:

- el Command es autorizado;
- el State actual permite la operación;
- los Guards se cumplen;
- las Invariants se cumplen;
- Versioning es válido;
- la Aggregate Root acepta la intención.

---

# Flujo Conceptual

```text
Command
    │
    ▼
Authorization
    │
    ▼
Integration Aggregate
    │
    ├── validates State
    ├── validates Guards
    ├── validates Invariants
    ├── validates Version
    │
    ▼
Domain Behavior
    │
    ▼
State / Aggregate Change
    │
    ▼
Domain Event
```

---

# CreateIntegration

`CreateIntegration` expresa la intención de crear formalmente una nueva
Integration.

Su transición es:

```text
No Integration → Draft
```

---

# Propósito de CreateIntegration

El Command establece una nueva identidad de Integration y crea una
unidad válida dentro del Bounded Context.

La creación no representa:

- conexión técnica;
- publicación de mensajes;
- comunicación con un sistema externo;
- activación;
- creación de adapters;
- creación de endpoints;
- creación de credenciales.

---

# Precondición de CreateIntegration

Antes de la creación:

```text
No Integration
```

debe ser verdadero para el IntegrationId correspondiente.

No debe existir previamente otra Integration con la misma identidad.

---

# Información Conceptual de CreateIntegration

El Command debe proporcionar la información necesaria para crear una
Integration válida conforme a las Invariants definidas.

Conceptualmente puede incluir:

```text
IntegrationId

CorrelationId

CausationId
```

y la información de dominio adicional que sea definida formalmente
como necesaria para representar la Integration.

Este documento no introduce atributos técnicos adicionales.

---

# IntegrationId en CreateIntegration

IntegrationId representa la identidad que tendrá la nueva Aggregate
Root.

Debe:

- ser válido;
- ser único;
- no representar una identidad externa;
- permanecer inmutable después de la creación.

---

# Resultado Válido de CreateIntegration

Cuando el Command es aceptado:

```text
State = Draft
```

y deben establecerse coherentemente:

```text
IntegrationId

State

Version

CreatedAt

UpdatedAt
```

conforme a las reglas correspondientes.

---

# Resultado Inválido de CreateIntegration

Si el Command es rechazado:

```text
No Integration
```

permanece como inexistencia.

No debe existir:

- Aggregate parcial;
- Version parcial;
- State parcial;
- Domain Event de éxito.

---

# CreateIntegration no Activa

Debe mantenerse:

```text
CreateIntegration

≠

ActivateIntegration
```

La creación finaliza en:

```text
Draft
```

---

# ActivateIntegration

`ActivateIntegration` expresa la intención de habilitar formalmente una
Integration existente.

Su transición es:

```text
Draft → Active
```

---

# Propósito de ActivateIntegration

El Command representa la decisión de dominio de permitir que la
Integration participe como relación activa de interoperabilidad.

Debe mantenerse:

```text
ActivateIntegration

≠

ConnectInfrastructure
```

---

# Precondición de ActivateIntegration

El State actual debe ser:

```text
Draft
```

---

# Guards de ActivateIntegration

Antes de aceptar el Command deben cumplirse:

- Integration existente;
- IntegrationId válido;
- State igual a Draft;
- Permission aplicable;
- Invariants válidas;
- ExpectedVersion válida cuando corresponda;
- condiciones de dominio requeridas para activación.

---

# Resultado Válido de ActivateIntegration

Cuando el Command es aceptado:

```text
Draft → Active
```

debe:

- modificar State;
- incrementar Version conforme al contrato;
- actualizar UpdatedAt;
- preservar IntegrationId;
- preservar CreatedAt;
- producir el Domain Event correspondiente.

---

# Resultado Inválido de ActivateIntegration

Si State es:

```text
Active

Suspended

Archived
```

`ActivateIntegration` debe ser rechazado.

---

# Activación no Implica Conectividad

La aceptación de:

```text
ActivateIntegration
```

no garantiza:

- endpoint disponible;
- broker conectado;
- red disponible;
- sistema externo disponible;
- FIWARE disponible;
- plataforma municipal disponible.

---

# SuspendIntegration

`SuspendIntegration` expresa la intención de suspender formalmente una
Integration activa.

Su transición es:

```text
Active → Suspended
```

---

# Propósito de SuspendIntegration

El Command representa una decisión explícita de dominio.

No representa automáticamente:

- timeout;
- network failure;
- broker failure;
- HTTP failure;
- FIWARE failure;
- endpoint unavailable;
- provider failure.

---

# Precondición de SuspendIntegration

El State actual debe ser:

```text
Active
```

---

# Guards de SuspendIntegration

Deben cumplirse:

- Integration existente;
- State igual a Active;
- Permission aplicable;
- Invariants válidas;
- ExpectedVersion válida cuando corresponda;
- intención formal de suspensión.

---

# Resultado Válido de SuspendIntegration

Cuando es aceptado:

```text
Active → Suspended
```

debe:

- preservar IntegrationId;
- modificar State;
- incrementar Version;
- actualizar UpdatedAt;
- preservar CreatedAt;
- producir el Domain Event correspondiente.

---

# Resultado Inválido de SuspendIntegration

Debe rechazarse desde:

```text
Draft

Suspended

Archived
```

---

# Suspensión no es Fallo

Debe mantenerse:

```text
SuspendIntegration

≠

ReportTechnicalFailure
```

El Command expresa una decisión del dominio.

---

# ReactivateIntegration

`ReactivateIntegration` expresa la intención de regresar formalmente
una Integration Suspended al estado Active.

Su transición es:

```text
Suspended → Active
```

---

# Propósito de ReactivateIntegration

Reactivar significa volver a habilitar formalmente la Integration.

Debe mantenerse:

```text
ReactivateIntegration

≠

TechnicalReconnect
```

---

# Precondición de ReactivateIntegration

El State actual debe ser:

```text
Suspended
```

---

# Guards de ReactivateIntegration

Deben cumplirse:

- Integration existente;
- State igual a Suspended;
- Permission aplicable;
- Invariants válidas;
- ExpectedVersion válida cuando corresponda;
- condiciones formales de reactivación.

---

# Resultado Válido de ReactivateIntegration

Cuando es aceptado:

```text
Suspended → Active
```

debe:

- preservar IntegrationId;
- modificar State;
- incrementar Version;
- actualizar UpdatedAt;
- preservar CreatedAt;
- producir el Domain Event correspondiente.

---

# Resultado Inválido de ReactivateIntegration

Debe rechazarse desde:

```text
Draft

Active

Archived
```

---

# Recuperación Técnica no Reactiva

Debe mantenerse:

```text
External System Recovered

≠

ReactivateIntegration
```

La recuperación técnica no representa una intención formal de dominio.

---

# ArchiveIntegration

`ArchiveIntegration` expresa la intención de retirar formalmente una
Integration del ciclo operativo.

---

# Transiciones de ArchiveIntegration

El Command puede producir:

```text
Draft → Archived
```

o:

```text
Active → Archived
```

o:

```text
Suspended → Archived
```

---

# Propósito de ArchiveIntegration

Archivar significa retirar la Integration de su ciclo operativo
preservando:

- IntegrationId;
- Version;
- historia;
- trazabilidad;
- significado de los hechos previamente confirmados.

---

# ArchiveIntegration no Elimina

Debe mantenerse:

```text
ArchiveIntegration

≠

DeleteIntegration
```

y:

```text
Archived

≠

Physically Deleted
```

---

# Guards de ArchiveIntegration

`ArchiveIntegration` requiere:

- Integration existente;
- State compatible;
- Permission aplicable;
- Invariants válidas;
- ExpectedVersion válida cuando corresponda.

---

# Estados Permitidos para ArchiveIntegration

Puede ejecutarse desde:

```text
Draft

Active

Suspended
```

---

# ArchiveIntegration desde Archived

Si State ya es:

```text
Archived
```

el Command debe ser rechazado.

No existe:

```text
Archived → Archived
```

como transición.

---

# Resultado Válido de ArchiveIntegration

Cuando es aceptado:

```text
State = Archived
```

debe:

- preservar IntegrationId;
- preservar CreatedAt;
- incrementar Version;
- actualizar UpdatedAt;
- producir el Domain Event correspondiente.

---

# Archived es Terminal

Después de:

```text
ArchiveIntegration
```

no pueden ejecutarse:

```text
ActivateIntegration

SuspendIntegration

ReactivateIntegration

ArchiveIntegration
```

como operaciones válidas sobre la misma Integration.

---

# Matriz Command / State

```text
Command                 Current State      Resulting State

CreateIntegration       No Integration     Draft

ActivateIntegration     Draft              Active

SuspendIntegration      Active             Suspended

ReactivateIntegration   Suspended          Active

ArchiveIntegration      Draft              Archived

ArchiveIntegration      Active             Archived

ArchiveIntegration      Suspended          Archived
```

---

# Matriz de Rechazo

```text
Command                 State              Result

CreateIntegration       Existing           Rejected

ActivateIntegration     Active             Rejected

ActivateIntegration     Suspended          Rejected

ActivateIntegration     Archived           Rejected

SuspendIntegration      Draft              Rejected

SuspendIntegration      Suspended          Rejected

SuspendIntegration      Archived           Rejected

ReactivateIntegration   Draft              Rejected

ReactivateIntegration   Active             Rejected

ReactivateIntegration   Archived           Rejected

ArchiveIntegration      Archived           Rejected
```

---

# Commands y State Machine

Los Commands no pueden crear transiciones distintas de:

```text
DOMAIN-013B-State-Machine.md
```

Debe mantenerse:

```text
Command

cannot extend

State Machine
```

---

# Commands y Lifecycle

Los Commands expresan las intenciones que permiten evolucionar el
Lifecycle.

No pueden introducir estados no definidos.

---

# Commands y Invariants

Todo Command debe ser validado contra:

```text
DOMAIN-013E-Invariants.md
```

Una intención autorizada que viole una Invariant debe rechazarse.

---

# Commands y Permissions

Los permisos para ejecutar Commands se definen en:

```text
DOMAIN-013F-Permissions.md
```

Debe mantenerse:

```text
Permission

=

Authority to Attempt
```

y no:

```text
Permission

=

Guarantee of Success
```

---

# Authentication

Authentication permanece fuera del Aggregate.

Un Command no contiene lógica de autenticación.

---

# Authorization

Authorization debe ocurrir antes de ejecutar comportamiento de
dominio.

Sin embargo:

```text
Authorized Command

≠

Automatically Valid Command
```

---

# Actor

Cuando el contexto correspondiente requiera preservar referencia al
actor asociado a una intención, dicha referencia no implica incorporar
Citizen, Membership o Role dentro de Integration.

Debe mantenerse:

```text
Actor Reference

≠

Embedded Actor Aggregate
```

---

# ActorId

Cuando forme parte del contrato aplicable, ActorId representa una
referencia de trazabilidad.

No representa:

- Permission;
- Role;
- Authentication;
- Authorization.

---

# CorrelationId

Cuando corresponda, CorrelationId permite relacionar una intención con
un flujo de negocio.

Debe mantenerse:

```text
CorrelationId

≠

Permission
```

---

# CausationId

Cuando corresponda, CausationId permite identificar el hecho previo
que originó una intención.

Debe mantenerse:

```text
CausationId

≠

Mutation Authority
```

---

# ExpectedVersion

Para Commands sobre una Integration existente debe preservarse la
validación de concurrencia conforme a:

```text
DOMAIN-013I-Versioning.md
```

Conceptualmente:

```text
ExpectedVersion

=

PersistedVersion
```

debe cumplirse cuando corresponda antes de confirmar la modificación.

---

# ExpectedVersion no es Aggregate Version

El Command puede transportar una expectativa de Version.

La Aggregate Root mantiene la Version real.

Debe mantenerse:

```text
ExpectedVersion

≠

Authority to Set Version
```

---

# Version Increment

Un Command aceptado que modifique una Integration existente produce:

```text
Version N

→

Version N + 1
```

conforme al contrato de Versioning.

---

# Creación y Version

`CreateIntegration` establece la Version inicial conforme a:

```text
DOMAIN-013I-Versioning.md
```

`No Integration` no representa una entidad persistida con Version 0.

---

# Rejected Command

Cuando un Command es rechazado:

```text
State      unchanged

Version    unchanged

UpdatedAt  unchanged
```

y no se produce un Domain Event de éxito.

---

# Domain Events

Los Commands aceptados producen los hechos correspondientes conforme
a:

```text
DOMAIN-013D-Domain-Events.md
```

Debe mantenerse:

```text
Command

≠

Domain Event
```

---

# Command no es Hecho Histórico

No debe almacenarse un Command como sustituto conceptual del hecho
confirmado.

Ejemplo:

```text
SuspendIntegration
```

expresa intención.

El hecho confirmado correspondiente se define mediante el Domain Event
oficial.

---

# No Domain Event on Failure

Si un Command no supera:

- Authorization;
- State Machine;
- Guards;
- Invariants;
- Versioning;
- Consistency;

no debe producir un Domain Event de éxito.

---

# Atomicidad

Un Command válido debe modificar el Aggregate de manera atómica.

No debe existir:

```text
State changed

without

Version coherence
```

ni:

```text
Version changed

without

valid Aggregate modification
```

---

# Una Aggregate Root

Cada Command se dirige a una única:

```text
Integration
```

No modifica atómicamente otros Aggregates.

---

# No Cross-Aggregate Command

Los Commands de Integration no pueden modificar:

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

---

# Sistemas Externos

Un Command de Integration no constituye por sí mismo una orden directa
sobre:

```text
FIWARE

Municipal System

External Platform
```

---

# Command versus External Request

Debe mantenerse:

```text
Domain Command

≠

HTTP Request
```

y:

```text
Domain Command

≠

Broker Message
```

---

# No Technical Commands

La versión 1.0 no define Commands como:

```text
SendHttpRequest

RetryHttpRequest

PublishMessage

PublishKafkaMessage

ConnectBroker

ReconnectBroker

OpenSocket

CloseSocket

RefreshAccessToken

RotateApiKey

SerializePayload

DeserializePayload

ExecuteWebhook

SyncFIWARE

RetryFIWARE

PingExternalSystem
```

Estos nombres representan responsabilidades técnicas y no intenciones
propias del Aggregate Integration.

---

# No ConnectIntegration

La versión 1.0 no define:

```text
ConnectIntegration
```

porque Active no representa conectividad técnica.

---

# No DisconnectIntegration

La versión 1.0 no define:

```text
DisconnectIntegration
```

por la misma razón.

---

# No FailIntegration

La versión 1.0 no define:

```text
FailIntegration
```

porque Failed no pertenece al Lifecycle oficial.

---

# No RetryIntegration

La versión 1.0 no define:

```text
RetryIntegration
```

El retry técnico permanece fuera del Aggregate.

---

# No DeleteIntegration

La versión 1.0 no define:

```text
DeleteIntegration
```

La finalización operacional se representa mediante:

```text
ArchiveIntegration
```

---

# No CancelIntegration

La versión 1.0 no define:

```text
CancelIntegration
```

Cancelled no pertenece al Lifecycle oficial.

---

# No ResetIntegration

La versión 1.0 no define:

```text
ResetIntegration
```

No existe transición hacia Draft después de abandonar dicho estado.

---

# No Generic UpdateIntegration

La versión 1.0 no define:

```text
UpdateIntegration
```

como Command genérico.

Una futura modificación de información deberá poseer intención
explícita y semántica de dominio antes de incorporarse.

---

# No ModifyIntegration

La versión 1.0 tampoco define:

```text
ModifyIntegration
```

como mecanismo genérico para alterar atributos.

---

# No setState Command

Nunca debe existir:

```text
SetIntegrationState
```

como Command de dominio.

Las transiciones se representan mediante intenciones semánticas.

---

# No setVersion Command

Nunca debe existir:

```text
SetIntegrationVersion
```

---

# No setCreatedAt Command

No debe existir:

```text
SetIntegrationCreatedAt
```

---

# No setUpdatedAt Command

UpdatedAt es consecuencia de comportamiento válido.

No se modifica mediante:

```text
SetIntegrationUpdatedAt
```

---

# Fallo Técnico

Un fallo técnico no genera automáticamente un Command de dominio.

Debe mantenerse:

```text
Technical Failure

≠

SuspendIntegration
```

---

# Recuperación Técnica

Del mismo modo:

```text
Technical Recovery

≠

ReactivateIntegration
```

---

# Timeout

Un timeout no constituye:

```text
SuspendIntegration
```

---

# Broker Failure

La indisponibilidad de broker no genera automáticamente:

```text
SuspendIntegration
```

---

# FIWARE Failure

Una indisponibilidad FIWARE no equivale a:

```text
SuspendIntegration
```

---

# Municipal System Failure

Una indisponibilidad municipal tampoco equivale a:

```text
SuspendIntegration
```

---

# External Input

Un mensaje externo no constituye automáticamente un Command válido.

Debe mantenerse:

```text
External Message

≠

Domain Command
```

---

# External Integration Event

Un Integration Event recibido puede iniciar un proceso posterior
conforme a contratos explícitos.

No puede utilizarse directamente para evitar:

- Authorization;
- Commands;
- State Machine;
- Invariants;
- Versioning.

---

# Domain Event de Otro Aggregate

Un Domain Event perteneciente a otro Aggregate tampoco constituye
automáticamente un Command de Integration.

---

# Application Coordination

Cuando un hecho externo deba producir una intención sobre Integration,
la coordinación correspondiente debe transformar dicha situación en un
Command válido del dominio.

El Aggregate solamente recibe la intención formal.

---

# Command y Consistency Boundary

Debe mantenerse:

```text
One Command

→

One Integration Aggregate Boundary
```

---

# No Distributed Command

Ningún Command definido aquí implica una transacción distribuida entre:

```text
Integration

+

External System
```

---

# No Cross-Aggregate Atomicity

`ActivateIntegration`, `SuspendIntegration`, `ReactivateIntegration` y
`ArchiveIntegration` modifican exclusivamente Integration.

---

# Repository

El Repository no ejecuta Commands.

Debe mantenerse:

```text
Repository

≠

Command Handler
```

---

# Repository no Decide Commands

El Repository no decide:

- si ActivateIntegration es válido;
- si SuspendIntegration es válido;
- si ReactivateIntegration es válido;
- si ArchiveIntegration es válido.

La decisión pertenece al comportamiento del Aggregate.

---

# Read Model

Un Read Model nunca ejecuta Commands.

Debe mantenerse:

```text
Read Model

≠

Write Authority
```

---

# Projection

Una Projection tampoco modifica Integration.

---

# CQRS

Los Commands pertenecen al Write Side.

Conceptualmente:

```text
Command
    │
    ▼
Integration Aggregate
    │
    ▼
Domain Event
```

Las Queries permanecen separadas.

---

# Event Sourcing

Event Sourcing permanece compatible pero no obligatorio.

Si es utilizado:

```text
Replay

≠

Re-execute Command
```

---

# Rehydration

Rehidratar una Integration no implica ejecutar:

```text
CreateIntegration

ActivateIntegration

SuspendIntegration

ReactivateIntegration

ArchiveIntegration
```

---

# Retry de Command

Un retry técnico de entrega de un Command no constituye
automáticamente una nueva intención de dominio.

La coordinación técnica debe evitar alterar el significado del
Command.

---

# Idempotencia

La estrategia técnica concreta de idempotencia no se define en este
documento.

Debe mantenerse:

```text
Technical Redelivery

≠

New Domain Intent
```

---

# CommandId

La versión 1.0 no establece:

```text
CommandId
```

como atributo obligatorio del Aggregate ni de todos los Commands.

Una eventual estrategia técnica de identificación de mensajes no debe
introducirse como regla de dominio sin definición explícita.

---

# Correlation

Correlation puede preservarse cuando el contrato correspondiente lo
requiera.

No modifica la semántica del Command.

---

# Causation

Causation puede preservarse para trazabilidad.

No concede autoridad para ejecutar la operación.

---

# Timestamp del Command

Un timestamp asociado a la recepción de una intención no debe
confundirse con el tiempo de ocurrencia del Domain Event resultante.

Debe mantenerse:

```text
Command Timestamp

≠

Domain Event OccurredAt
```

---

# Security

Los Commands no deben contener:

```text
Password

AccessToken

RefreshToken

ApiKey

PrivateKey

ClientSecret

Secret
```

como información del dominio.

---

# Credentials

Las credenciales necesarias para comunicación externa permanecen fuera
de Integration.

Por lo tanto no forman parte conceptual de:

```text
CreateIntegration

ActivateIntegration

SuspendIntegration

ReactivateIntegration

ArchiveIntegration
```

---

# FIWARE

Ningún Command depende directamente de:

```text
FIWARE

NGSI-LD

Context Broker

Orion
```

---

# Sistemas Municipales

Los Commands tampoco dependen directamente de modelos, APIs o estados
de una plataforma municipal.

---

# Protocolos

Los Commands son independientes de:

```text
HTTP

REST

GraphQL

MQTT

AMQP
```

---

# Brokers

Los Commands son independientes de:

```text
Kafka

RabbitMQ

NATS
```

o tecnologías equivalentes.

---

# Persistencia

Los Commands no conocen:

- SQL;
- ORM;
- MongoDB;
- PostgreSQL;
- Event Store;
- filesystem.

---

# Command Serialization

La serialización técnica de una intención pertenece a capas externas.

Debe mantenerse:

```text
Command Semantics

≠

Serialization Format
```

---

# Direct Database Mutation

No está permitido sustituir:

```text
ActivateIntegration
```

por una actualización directa:

```text
State = Active
```

en persistencia.

La misma regla aplica a todas las transiciones.

---

# Direct API Mutation

Una API no debe exponer modificación arbitraria de State evitando los
Commands semánticos.

---

# Direct Adapter Mutation

Un Adapter no puede modificar directamente:

```text
State

Version

IntegrationId

CreatedAt

UpdatedAt
```

---

# Command Failure

Un Command puede ser rechazado por:

- Aggregate inexistente cuando se requiere uno existente;
- Aggregate ya existente durante CreateIntegration;
- State incompatible;
- Guard incumplido;
- Invariant incumplida;
- Permission insuficiente;
- ConcurrencyConflict.

Estos rechazos no representan nuevos estados del Aggregate.

---

# Error de Persistencia

Un error de persistencia no constituye un resultado de negocio
equivalente a:

```text
Integration = Failed
```

Failed no pertenece al Lifecycle.

---

# Error de Infrastructure

Un error técnico tampoco genera automáticamente un Domain Event de
éxito.

---

# Command Accepted

Un Command solamente puede considerarse exitoso cuando el cambio del
Aggregate queda confirmado conforme a su Consistency Boundary.

---

# Command Rejected

Debe mantenerse:

```text
Rejected Command
    │
    ├── no state change
    ├── no version change
    ├── no UpdatedAt change
    └── no success Domain Event
```

---

# Archived y Commands

Archived es terminal.

Por lo tanto una Integration Archived no acepta Commands ordinarios de
Lifecycle.

---

# No Command after Archived

Debe mantenerse:

```text
State = Archived

ActivateIntegration     → Rejected

SuspendIntegration      → Rejected

ReactivateIntegration   → Rejected

ArchiveIntegration      → Rejected
```

---

# Evolución Futura

Cualquier Command adicional deberá representar una intención real del
dominio y requerirá revisión coordinada de:

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

DOMAIN-013M-Test-Scenarios.md

DOMAIN-013O-Security-Model.md

DOMAIN-013P-Extension-Points.md
```

cuando corresponda.

---

# Regla para Nuevos Commands

Un nuevo Command debe definir explícitamente:

- intención;
- Aggregate objetivo;
- State permitido;
- Guards;
- Invariants;
- Permission;
- efecto sobre Version;
- efecto sobre UpdatedAt;
- Domain Event resultante;
- escenarios de rechazo.

---

# Commands no se Infieren desde Infrastructure

No debe introducirse un nuevo Command solamente porque exista:

- un endpoint;
- un botón de UI;
- una operación de broker;
- una acción de FIWARE;
- una operación municipal;
- un método de SDK;
- una función de framework.

---

# Commands no se Infieren desde External APIs

Una operación externa denominada:

```text
CONNECT

DISABLE

DELETE

SYNC

RETRY
```

no se convierte automáticamente en un Command de Integration.

---

# Regla de Lenguaje Ubicuo

Todo Command debe expresar una intención propia del lenguaje de AURA.

No debe utilizar nombres técnicos de:

- tablas;
- endpoints;
- métodos HTTP;
- brokers;
- frameworks;
- proveedores.

---

# Reglas Fundamentales

Los Commands de Integration deben cumplir:

1. Los Commands expresan intención.
2. Los Commands no representan hechos consumados.
3. La versión 1.0 define exactamente CreateIntegration,
   ActivateIntegration, SuspendIntegration, ReactivateIntegration y
   ArchiveIntegration.
4. CreateIntegration representa No Integration → Draft.
5. ActivateIntegration representa Draft → Active.
6. SuspendIntegration representa Active → Suspended.
7. ReactivateIntegration representa Suspended → Active.
8. ArchiveIntegration puede representar Draft → Archived.
9. ArchiveIntegration puede representar Active → Archived.
10. ArchiveIntegration puede representar Suspended → Archived.
11. CreateIntegration no activa una Integration.
12. ActivateIntegration no conecta Infrastructure.
13. SuspendIntegration no representa Technical Failure.
14. ReactivateIntegration no representa Technical Recovery.
15. ArchiveIntegration no representa Physical Deletion.
16. Archived no acepta Commands ordinarios de Lifecycle.
17. Ningún Command modifica directamente State.
18. Ningún Command modifica directamente Version.
19. Ningún Command modifica IntegrationId.
20. Ningún Command modifica CreatedAt.
21. UpdatedAt solamente cambia como consecuencia de una operación
    válida.
22. Todo Command debe respetar State Machine.
23. Todo Command debe respetar Invariants.
24. Todo Command debe respetar Permissions.
25. Todo Command debe respetar Versioning.
26. Una Permission no garantiza éxito.
27. Una transición válida no elimina necesidad de Authorization.
28. Una operación rechazada no modifica State.
29. Una operación rechazada no modifica Version.
30. Una operación rechazada no modifica UpdatedAt.
31. Una operación rechazada no produce Domain Event de éxito.
32. ExpectedVersion no permite establecer Version arbitrariamente.
33. ConcurrencyConflict debe rechazar la modificación.
34. Un Command opera sobre una única Integration.
35. Un Command no modifica otros Aggregates atómicamente.
36. Un Command no modifica sistemas externos atómicamente.
37. Un External Message no es automáticamente un Command.
38. Un Integration Event no es automáticamente un Command.
39. Un Domain Event externo no es automáticamente un Command.
40. Technical Failure no crea SuspendIntegration automáticamente.
41. Technical Recovery no crea ReactivateIntegration automáticamente.
42. Timeout no constituye Command de dominio.
43. Broker Failure no constituye Command de dominio.
44. FIWARE Failure no constituye Command de dominio.
45. Municipal System Failure no constituye Command de dominio.
46. No existe ConnectIntegration.
47. No existe DisconnectIntegration.
48. No existe FailIntegration.
49. No existe RetryIntegration.
50. No existe DeleteIntegration.
51. No existe CancelIntegration.
52. No existe ResetIntegration.
53. No existe UpdateIntegration genérico.
54. No existe ModifyIntegration genérico.
55. No existe SetIntegrationState.
56. No existe SetIntegrationVersion.
57. No existe SetIntegrationCreatedAt.
58. No existe SetIntegrationUpdatedAt.
59. Commands técnicos de transporte permanecen fuera del Aggregate.
60. Commands técnicos de credenciales permanecen fuera del Aggregate.
61. Commands técnicos de serialización permanecen fuera del Aggregate.
62. Repository no ejecuta Commands.
63. Repository no decide validez de Commands.
64. Read Model no ejecuta Commands.
65. Projection no ejecuta Commands.
66. Commands pertenecen al Write Side.
67. Replay no reejecuta Commands.
68. Rehydration no reejecuta Commands.
69. Retry técnico de entrega no constituye automáticamente nueva
    intención.
70. Idempotencia técnica no introduce una regla nueva del Aggregate.
71. CommandId no es obligatorio en versión 1.0.
72. CorrelationId no representa Permission.
73. CausationId no representa Mutation Authority.
74. ActorId, cuando corresponda, no representa Authorization.
75. Commands no contienen credenciales.
76. Commands no dependen de FIWARE.
77. Commands no dependen de sistemas municipales.
78. Commands no dependen de protocolos.
79. Commands no dependen de brokers.
80. Commands no dependen de bases de datos.
81. Serialization Format no cambia semántica del Command.
82. Direct Database Mutation no sustituye un Command.
83. Direct API Mutation no sustituye comportamiento de dominio.
84. Adapter no puede modificar el Aggregate directamente.
85. Failed no se introduce como resultado de Lifecycle.
86. Persistence Failure no constituye un nuevo State.
87. Infrastructure Failure no produce Domain Event de éxito.
88. Toda modificación válida debe ser atómica dentro del Aggregate.
89. Domain Event solamente representa un hecho confirmado.
90. Command y Domain Event mantienen semánticas distintas.
91. Un nuevo Command requiere intención real de dominio.
92. Un nuevo Command requiere State permitido.
93. Un nuevo Command requiere Invariants coherentes.
94. Un nuevo Command requiere Permission cuando corresponda.
95. Un nuevo Command requiere definición de Versioning.
96. Un nuevo Command requiere Domain Event cuando corresponda.
97. Un nuevo Command requiere Test Scenarios.
98. Infrastructure no define Commands de dominio.
99. External APIs no definen Commands de dominio automáticamente.
100. Ningún Command adicional forma parte de versión 1.0 sin
     definición formal.

---

# Restricciones

No está permitido:

- crear una Integration fuera de Draft;
- activar una Integration fuera de Draft;
- suspender una Integration fuera de Active;
- reactivar una Integration fuera de Suspended;
- archivar una Integration Archived;
- cambiar State directamente;
- cambiar Version directamente;
- cambiar IntegrationId;
- cambiar CreatedAt;
- utilizar setters como Commands;
- ejecutar un Command evitando State Machine;
- ejecutar un Command evitando Invariants;
- ejecutar un Command evitando Permissions;
- ejecutar un Command evitando Versioning;
- ignorar ConcurrencyConflict;
- producir Domain Event de éxito ante rechazo;
- interpretar timeout como SuspendIntegration;
- interpretar network failure como SuspendIntegration;
- interpretar broker failure como SuspendIntegration;
- interpretar FIWARE failure como SuspendIntegration;
- interpretar external recovery como ReactivateIntegration;
- utilizar ConnectIntegration;
- utilizar DisconnectIntegration;
- utilizar FailIntegration;
- utilizar RetryIntegration;
- utilizar DeleteIntegration;
- utilizar CancelIntegration;
- utilizar ResetIntegration;
- utilizar UpdateIntegration genérico;
- utilizar ModifyIntegration genérico;
- utilizar SetIntegrationState;
- utilizar SetIntegrationVersion;
- utilizar Commands técnicos de transporte como Commands del
  Aggregate;
- utilizar Commands técnicos de Infrastructure como Commands del
  Aggregate;
- almacenar credenciales dentro de Commands de dominio;
- utilizar un External Message directamente como Command;
- permitir que Repository ejecute comportamiento de dominio;
- permitir que Read Model ejecute comportamiento de dominio;
- permitir que Adapter modifique directamente el Aggregate;
- modificar otros Aggregates desde un Command de Integration;
- introducir un nuevo Command por conveniencia técnica;
- introducir un nuevo Command sin actualizar los contratos de dominio
  afectados.

---

# Compatibilidad Arquitectónica

Los Commands de Integration son compatibles con:

- Domain-Driven Design;
- Aggregate Pattern;
- Command Pattern;
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

Estas compatibilidades no imponen tecnologías ni mecanismos de
Infrastructure.

---

# Definición de Éxito

Los Commands del Aggregate **Integration** expresan exclusivamente las
intenciones formales necesarias para ejecutar su Lifecycle versión
1.0:

```text
CreateIntegration
    │
    ▼
No Integration → Draft

ActivateIntegration
    │
    ▼
Draft → Active

SuspendIntegration
    │
    ▼
Active → Suspended

ReactivateIntegration
    │
    ▼
Suspended → Active

ArchiveIntegration
    │
    ├── Draft → Archived
    ├── Active → Archived
    └── Suspended → Archived
```

El modelo garantiza que:

- cada Command exprese una intención real del dominio;
- ningún Command modifique atributos directamente;
- State Machine determine las transiciones posibles;
- Invariants permanezcan protegidas;
- Permissions determinen quién puede intentar cada operación;
- Versioning proteja concurrencia y evolución;
- los rechazos no modifiquen el Aggregate;
- los Domain Events representen solamente hechos confirmados;
- IntegrationId permanezca inmutable;
- Archived permanezca terminal;
- fallos técnicos no generen Commands de Lifecycle automáticamente;
- recuperación técnica no provoque reactivación automática;
- Infrastructure no introduzca Commands de dominio;
- FIWARE no defina los Commands;
- sistemas municipales no definan los Commands;
- Repository no ejecute Commands;
- Read Models no ejecuten Commands;
- cada Command opere solamente dentro del Consistency Boundary de
  Integration;
- nuevos Commands requieran definición explícita y evolución
  coordinada del dominio.

De esta forma, `DOMAIN-013C-Commands.md` establece formalmente los
Commands oficiales del Aggregate **Integration** conforme al patrón
consolidado de AURA Core.