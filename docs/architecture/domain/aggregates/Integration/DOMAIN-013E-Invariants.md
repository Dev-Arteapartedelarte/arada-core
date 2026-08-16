# DOMAIN-013E — Integration Invariants

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
- DOMAIN-013C-Commands.md
- DOMAIN-013D-Domain-Events.md
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

Este documento define formalmente las **Invariants** del Aggregate
**Integration**.

Las Invariants representan reglas que deben permanecer verdaderas
durante toda la existencia válida del Aggregate.

Ningún Command, transición, Repository, Adapter, Integration Event,
Read Model o mecanismo de Infrastructure puede producir un estado que
viole estas reglas.

---

# Principio Fundamental

Debe mantenerse:

```text
Valid Integration

=

All Invariants Hold
```

antes y después de toda modificación válida.

---

# Invariant versus Validation

Una Invariant no representa una validación técnica.

Debe mantenerse:

```text
Domain Invariant

≠

Infrastructure Validation
```

Una validación de:

- formato de transporte;
- protocolo;
- serialización;
- conexión;
- base de datos;
- framework;

no constituye automáticamente una Invariant de Integration.

---

# Invariant versus Permission

Debe mantenerse:

```text
Permission

≠

Invariant
```

Una Permission determina si una intención puede ser intentada.

Una Invariant determina si el estado resultante puede considerarse
válido.

---

# Authorized no Significa Valid

Debe mantenerse:

```text
Authorized

≠

Valid
```

Un Command autorizado debe seguir respetando todas las Invariants.

---

# Alcance

Las Invariants definidas aquí pertenecen exclusivamente al Aggregate:

```text
Integration
```

No gobiernan directamente:

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

External System

FIWARE

Municipal System
```

---

# Invariant de Identidad

Toda Integration debe poseer:

```text
IntegrationId
```

válido.

Debe mantenerse:

```text
IntegrationId != null
```

---

# IntegrationId Inmutable

Una vez creada:

```text
IntegrationId
```

no puede cambiar.

Debe mantenerse:

```text
Original IntegrationId

=

Current IntegrationId
```

durante todo el Lifecycle.

---

# IntegrationId no se Reutiliza

Una identidad no debe reutilizarse para representar una Integration
conceptualmente diferente.

Debe mantenerse:

```text
One IntegrationId

=

One Integration Identity
```

---

# IntegrationId no es Identidad Externa

Debe mantenerse:

```text
IntegrationId

≠

ExternalSystemId
```

cuando exista una identidad externa.

---

# IntegrationId no es EventId

Debe mantenerse:

```text
IntegrationId

≠

DomainEvent.EventId
```

---

# IntegrationId no es CorrelationId

Debe mantenerse:

```text
IntegrationId

≠

CorrelationId
```

---

# IntegrationId no es CausationId

Debe mantenerse:

```text
IntegrationId

≠

CausationId
```

---

# Invariant de Aggregate Root

La única autoridad para modificar el estado interno es:

```text
Integration
```

como Aggregate Root.

Ningún consumidor externo puede modificar directamente sus
propiedades.

---

# No Setters Públicos

No debe existir modificación directa equivalente a:

```text
setIntegrationId()

setState()

setVersion()

setCreatedAt()

setUpdatedAt()
```

para evitar comportamiento de dominio.

---

# Invariant de Lifecycle

Toda Integration persistida debe encontrarse exactamente en uno de los
estados oficiales:

```text
Draft

Active

Suspended

Archived
```

---

# Estados Exclusivos

Una Integration no puede encontrarse simultáneamente en más de un
State.

Debe mantenerse:

```text
exactly one current State
```

---

# No Integration no es State

Debe mantenerse:

```text
No Integration

≠

Persisted State
```

---

# Estado Inicial

Toda Integration creada válidamente debe comenzar en:

```text
Draft
```

No puede comenzar en:

```text
Active

Suspended

Archived
```

---

# Estado Terminal

Debe mantenerse:

```text
Archived

=

Terminal State
```

---

# Archived no se Reactiva

Desde:

```text
Archived
```

ninguna transición posterior es válida en versión 1.0.

---

# Draft no se Recupera

Una Integration que abandonó:

```text
Draft
```

no puede volver a Draft.

---

# Invariant de Transiciones

Solamente están permitidas:

```text
No Integration → Draft

Draft          → Active

Draft          → Archived

Active         → Suspended

Active         → Archived

Suspended      → Active

Suspended      → Archived
```

---

# Lista Cerrada de Transiciones

Debe mantenerse:

```text
Not Explicitly Allowed

=

Rejected
```

---

# Active → Draft Prohibido

Debe mantenerse:

```text
Active → Draft

=

Invalid
```

---

# Suspended → Draft Prohibido

Debe mantenerse:

```text
Suspended → Draft

=

Invalid
```

---

# Archived → Active Prohibido

Debe mantenerse:

```text
Archived → Active

=

Invalid
```

---

# Archived → Suspended Prohibido

Debe mantenerse:

```text
Archived → Suspended

=

Invalid
```

---

# Archived → Draft Prohibido

Debe mantenerse:

```text
Archived → Draft

=

Invalid
```

---

# Archived → Archived no es Transición

Debe mantenerse:

```text
Archived → Archived

≠

Valid Lifecycle Transition
```

---

# Invariant de Commands

La versión 1.0 define exactamente:

```text
CreateIntegration

ActivateIntegration

SuspendIntegration

ReactivateIntegration

ArchiveIntegration
```

Ningún Command adicional forma parte del modelo oficial.

---

# CreateIntegration

`CreateIntegration` solamente es válido cuando:

```text
No Integration
```

existe conceptualmente para el IntegrationId objetivo.

---

# CreateIntegration Result

Un CreateIntegration válido debe producir:

```text
State = Draft
```

---

# CreateIntegration no Sobrescribe

Si una Integration con el mismo IntegrationId ya existe:

```text
CreateIntegration

=

Rejected
```

---

# ActivateIntegration

`ActivateIntegration` solamente es válido desde:

```text
Draft
```

---

# ActivateIntegration Result

Debe producir:

```text
Draft → Active
```

---

# SuspendIntegration

`SuspendIntegration` solamente es válido desde:

```text
Active
```

---

# SuspendIntegration Result

Debe producir:

```text
Active → Suspended
```

---

# ReactivateIntegration

`ReactivateIntegration` solamente es válido desde:

```text
Suspended
```

---

# ReactivateIntegration Result

Debe producir:

```text
Suspended → Active
```

---

# ArchiveIntegration

`ArchiveIntegration` solamente es válido desde:

```text
Draft

Active

Suspended
```

---

# ArchiveIntegration Result

Debe producir:

```text
State = Archived
```

---

# No Commands Técnicos

No forman parte del dominio Commands como:

```text
ConnectIntegration

DisconnectIntegration

RetryIntegration

FailIntegration

DeleteIntegration

SyncFIWARE

PublishMessage

SendHttpRequest

RefreshToken
```

---

# Invariant de Domain Events

La versión 1.0 define exactamente:

```text
IntegrationCreated

IntegrationActivated

IntegrationSuspended

IntegrationReactivated

IntegrationArchived
```

---

# Command y Event Coherentes

Debe mantenerse:

```text
CreateIntegration
    →
IntegrationCreated
```

```text
ActivateIntegration
    →
IntegrationActivated
```

```text
SuspendIntegration
    →
IntegrationSuspended
```

```text
ReactivateIntegration
    →
IntegrationReactivated
```

```text
ArchiveIntegration
    →
IntegrationArchived
```

solamente cuando la operación fue válida.

---

# No Event on Rejection

Una operación rechazada no produce un Domain Event de éxito.

Debe mantenerse:

```text
Rejected Command

→

No Success Domain Event
```

---

# IntegrationCreated

`IntegrationCreated` solamente puede existir como consecuencia de:

```text
No Integration → Draft
```

---

# IntegrationActivated

`IntegrationActivated` solamente puede representar:

```text
Draft → Active
```

---

# IntegrationSuspended

`IntegrationSuspended` solamente puede representar:

```text
Active → Suspended
```

---

# IntegrationReactivated

`IntegrationReactivated` solamente puede representar:

```text
Suspended → Active
```

---

# IntegrationArchived

`IntegrationArchived` solamente puede representar:

```text
Draft → Archived

Active → Archived

Suspended → Archived
```

---

# No Eventos Técnicos

No deben producirse como Domain Events:

```text
IntegrationConnected

IntegrationDisconnected

IntegrationFailed

IntegrationRetried

IntegrationSaved

IntegrationPublished

IntegrationFIWARESynced

IntegrationBrokerConnected
```

---

# Invariant de EventId

Todo Domain Event debe poseer:

```text
EventId
```

único e inmutable.

---

# EventId Identifica un Hecho

Debe mantenerse:

```text
One EventId

=

One Domain Fact
```

---

# No Reutilización de EventId

Dos hechos distintos no deben compartir el mismo EventId.

---

# EventType

Todo Domain Event debe poseer un EventType coherente con el hecho
representado.

---

# AggregateVersion

Todo Domain Event debe relacionarse con:

```text
AggregateVersion
```

correspondiente a la Version resultante del Aggregate.

---

# Version Coherente con Evento

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

# Version del Aggregate

Integration debe poseer:

```text
Version
```

válida.

---

# Version no se Modifica Directamente

Debe mantenerse:

```text
Version changes

only through

Valid Aggregate Modification
```

---

# Modificación Válida

Toda modificación válida sobre una Integration existente debe producir:

```text
Version N → Version N + 1
```

conforme al contrato de Versioning.

---

# Operación Rechazada

Una operación rechazada debe mantener:

```text
Version N → Version N
```

---

# Lectura

Una lectura no incrementa Version.

---

# Rehydration

Rehydration no incrementa Version.

---

# Replay

Replay no incrementa Version artificialmente.

---

# Retry Técnico

Un retry técnico no incrementa Version por sí mismo.

---

# Projection

Una Projection no incrementa Version.

---

# Publicación Externa

Una publicación externa no incrementa Version.

---

# Invariant de Concurrencia

Cuando una operación sobre Integration existente utiliza
ExpectedVersion:

```text
ExpectedVersion

=

PersistedVersion
```

debe cumplirse para confirmar la modificación.

---

# ConcurrencyConflict

Si:

```text
ExpectedVersion

≠

PersistedVersion
```

la operación debe rechazarse.

---

# No Last-Write-Wins Implícito

Debe mantenerse:

```text
ConcurrencyConflict

≠

Permission to Overwrite
```

---

# Concurrency no se Evita por Permission

Un actor autorizado no puede evitar Versioning o concurrencia.

---

# CreatedAt

Toda Integration debe poseer:

```text
CreatedAt
```

establecido durante su creación.

---

# CreatedAt Inmutable

Después de la creación:

```text
CreatedAt
```

no cambia.

---

# UpdatedAt

UpdatedAt solamente cambia como consecuencia de una modificación
válida del Aggregate.

---

# UpdatedAt no Cambia en Rechazo

Una operación rechazada debe mantener:

```text
UpdatedAt unchanged
```

---

# UpdatedAt no Cambia en Lectura

Una Query no modifica UpdatedAt.

---

# Invariant de Ownership

Integration solamente posee su propio estado.

No posee:

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

External System
```

---

# Referencia no Transfiere Ownership

Debe mantenerse:

```text
External Reference

≠

Ownership Transfer
```

---

# No Aggregates Embebidos

Integration no debe contener otros Aggregate Roots como entidades
internas.

---

# No External Systems Embebidos

Un sistema externo tampoco debe modelarse como una parte mutable
embebida dentro de Integration.

---

# Source Aggregate no se Modifica

Un Command válido sobre Integration no modifica directamente el
Aggregate que originó un hecho o contrato.

---

# Invariant de Consistency Boundary

Una operación de Integration modifica solamente:

```text
Integration
```

dentro de su propio Consistency Boundary.

---

# No Cross-Aggregate Transaction

Debe mantenerse:

```text
Integration Transaction

≠

Other Aggregate Transaction
```

---

# No External Distributed Aggregate

Debe mantenerse:

```text
Integration

+

External System

≠

One Aggregate
```

---

# Consistencia Interna

Todas las Invariants de Integration deben cumplirse inmediatamente
antes de confirmar una modificación.

---

# Consistencia Externa

La relación con otros Aggregates o sistemas permanece bajo
consistencia eventual.

---

# External Failure no Revierte Aggregate

Un fallo posterior en otro sistema no modifica automáticamente una
transición de Integration ya confirmada.

---

# Source Transaction no es Integration Transaction

Debe mantenerse:

```text
Source Aggregate Commit

≠

Integration Commit
```

---

# External System Transaction

Debe mantenerse:

```text
Integration Commit

≠

External System Commit
```

---

# Invariant de Independencia Tecnológica

El estado válido de Integration no depende de una tecnología concreta.

---

# Protocol Independence

Integration no depende conceptualmente de:

```text
HTTP

REST

GraphQL

MQTT

AMQP

WebSocket
```

para satisfacer sus Invariants.

---

# Broker Independence

Integration no depende conceptualmente de:

```text
Kafka

RabbitMQ

NATS
```

para ser válida.

---

# Database Independence

Integration no depende conceptualmente de:

```text
PostgreSQL

MongoDB

Redis

SQL

ORM
```

para definir sus reglas.

---

# FIWARE Independence

Debe mantenerse:

```text
Valid Integration

≠

FIWARE Availability
```

---

# Municipal System Independence

Debe mantenerse:

```text
Valid Integration

≠

Municipal System Availability
```

---

# External Availability no Determina State

Debe mantenerse:

```text
External System Availability

≠

Integration State
```

---

# Technical Health no Determina State

Debe mantenerse:

```text
Technical Health

≠

Lifecycle State
```

---

# Connected no es State

La conectividad técnica no puede introducir:

```text
Connected
```

como State de Integration versión 1.0.

---

# Disconnected no es State

Tampoco:

```text
Disconnected
```

forma parte del State.

---

# Failed no es State

Debe mantenerse:

```text
Failed

∉

Integration Lifecycle
```

---

# Pending no es State

Debe mantenerse:

```text
Pending

∉

Integration Lifecycle
```

---

# Deleted no es State

Debe mantenerse:

```text
Deleted

∉

Integration Lifecycle
```

---

# Cancelled no es State

Debe mantenerse:

```text
Cancelled

∉

Integration Lifecycle
```

---

# Estados Técnicos no son States

No forman parte del Lifecycle:

```text
Connecting

Reconnecting

Retrying

Processing

Queued

Published

DeliveryFailed

DeadLettered

Healthy

Unhealthy

Degraded
```

---

# Technical Failure no es Domain Transition

Un fallo de:

- network;
- broker;
- endpoint;
- provider;
- FIWARE;
- sistema municipal;

no produce automáticamente una transición de State.

---

# Timeout no Suspende

Debe mantenerse:

```text
Timeout

≠

SuspendIntegration
```

---

# Broker Failure no Suspende

Debe mantenerse:

```text
BrokerFailure

≠

SuspendIntegration
```

---

# FIWARE Failure no Suspende

Debe mantenerse:

```text
FIWAREUnavailable

≠

SuspendIntegration
```

---

# Municipal Failure no Suspende

Debe mantenerse:

```text
MunicipalSystemUnavailable

≠

SuspendIntegration
```

---

# Technical Recovery no Reactiva

Debe mantenerse:

```text
TechnicalRecovery

≠

ReactivateIntegration
```

---

# Invariant de Contratos

La interoperabilidad debe basarse en contratos explícitos.

Debe mantenerse:

```text
Integration

requires

Explicit Contract
```

cuando exista intercambio entre contextos o sistemas.

---

# Contrato no es Aggregate

Debe mantenerse:

```text
Integration Contract

≠

Integration Aggregate
```

---

# Contract Version no es Aggregate Version

Debe mantenerse:

```text
Contract Version

≠

Integration.Version
```

---

# API Version no es Aggregate Version

Debe mantenerse:

```text
API Version

≠

Integration.Version
```

---

# Schema Version no es Aggregate Version

Debe mantenerse:

```text
Schema Version

≠

Integration.Version
```

---

# External State no es Integration State

Ningún estado externo se incorpora automáticamente como State interno.

---

# External Model no es AURA Model

Debe mantenerse:

```text
External Model

≠

AURA Domain Model
```

---

# Domain Event no es Integration Event

Debe mantenerse:

```text
Domain Event

≠

Integration Event
```

---

# Domain Event no Obliga Publicación

Debe mantenerse:

```text
Domain Event

≠

Mandatory External Publication
```

---

# Source Domain Event Ownership

Un Domain Event originado en otro Aggregate continúa perteneciendo a
su productor.

Integration no adquiere ownership sobre él.

---

# External Message no es Domain Fact

Debe mantenerse:

```text
External Message

≠

AURA Domain Fact
```

sin una interpretación contractual válida.

---

# External Message no es Command

Debe mantenerse:

```text
External Message

≠

Automatic Integration Command
```

---

# Integration Event Entrante

Recibir un Integration Event no permite modificar directamente el
Aggregate.

---

# No Direct State Mutation from Integration Event

Debe mantenerse:

```text
Integration Event

≠

setState()
```

---

# CorrelationId

CorrelationId puede preservarse cuando corresponda.

No determina:

- identidad del Aggregate;
- Permission;
- State;
- ownership.

---

# CausationId

CausationId puede preservarse cuando corresponda.

No determina:

- Permission;
- State;
- ownership;
- Version.

---

# Invariant de Datos

Integration debe conservar solamente información necesaria para su
propósito de dominio.

Debe mantenerse:

```text
Minimum Necessary Domain Data
```

---

# External Payload no se Copia Automáticamente

Debe mantenerse:

```text
External Payload

≠

Automatic Aggregate State
```

---

# Source Payload no se Copia Automáticamente

Debe mantenerse:

```text
Source Aggregate Payload

≠

Automatic Integration State
```

---

# Información Ausente

No debe fabricarse información que el contrato no proporciona.

Debe mantenerse:

```text
Missing Information

≠

Fabricated Information
```

---

# Invariant de Credenciales

Integration no debe almacenar:

```text
Password

AccessToken

RefreshToken

ApiKey

PrivateKey

ClientSecret

Secret

Session
```

como estado del dominio.

---

# Credencial no es Atributo de Dominio

Debe mantenerse:

```text
Credential

∉

Integration Aggregate
```

---

# Token Expiration no Cambia State

La expiración de una credencial no produce automáticamente una
transición.

---

# Credential Rotation no Cambia Version

Una rotación técnica de credenciales no modifica Integration.Version
por sí misma.

---

# Invariant de Security

Authentication permanece fuera del Aggregate.

---

# Authorization permanece Separada

Authorization decide si una intención puede ser intentada.

El Aggregate decide si el comportamiento es válido.

---

# Security no Puede Evitar Invariants

Debe mantenerse:

```text
Security Privilege

≠

Invariant Override
```

---

# Security no Puede Evitar State Machine

Debe mantenerse:

```text
Security Privilege

≠

State Machine Override
```

---

# Security no Puede Evitar Versioning

Debe mantenerse:

```text
Security Privilege

≠

Version Override
```

---

# Repository Invariants

El Repository debe preservar el Aggregate como una unidad.

No debe permitir persistir un estado que viole Invariants.

---

# Repository no Corrige Aggregate

El Repository no debe:

- inventar datos faltantes;
- cambiar State;
- incrementar Version por decisión propia;
- crear Domain Events;
- corregir Invariants.

---

# Repository no Decide Lifecycle

Debe mantenerse:

```text
Repository

≠

Lifecycle Authority
```

---

# Repository no Decide Permission

Debe mantenerse:

```text
Repository

≠

Authorization Authority
```

---

# Persistencia Atómica

Una modificación válida debe persistir Integration de forma que no
quede parcialmente actualizada.

---

# No Partial Commit

No debe existir:

```text
State updated

but

Version not updated
```

cuando la operación válida requiera ambos cambios.

---

# No Partial Event Result

Tampoco:

```text
Domain Event confirmed

but

Aggregate modification rejected
```

---

# Read Model Invariants

Los Read Models no constituyen autoridad de escritura.

---

# Read Model no Modifica Aggregate

Debe mantenerse:

```text
Read Model

≠

Aggregate Mutation Authority
```

---

# Projection Lag no Viola Aggregate

Un Read Model temporalmente desactualizado no modifica el estado
autoritativo de Integration.

---

# Projection Failure no Revierte Aggregate

Un fallo de Projection no revierte una modificación confirmada.

---

# Audit no Modifica Integration

Audit puede preservar hechos relacionados.

No puede cambiar:

```text
IntegrationId

State

Version
```

---

# Notification no Modifica Integration

Notification puede comunicar hechos.

No controla Lifecycle.

---

# Organization no Modifica Integration Directamente

Organization mantiene su propio Consistency Boundary.

---

# Citizen no Modifica Integration Directamente

Citizen permanece fuera del Boundary.

---

# Membership no Modifica Integration Directamente

Membership permanece fuera del Boundary.

---

# Role no Modifica Integration Directamente

Role permanece fuera del Boundary.

---

# Territory no Modifica Integration Directamente

Territory permanece fuera del Boundary.

---

# Assembly no Modifica Integration Directamente

Assembly puede producir hechos consumibles.

No posee autoridad directa sobre Integration.

---

# Proposal no Modifica Integration Directamente

Proposal permanece independiente.

---

# Participation no Modifica Integration Directamente

Participation mantiene transacción propia.

---

# Voting no Modifica Integration Directamente

Voting mantiene Lifecycle propio.

---

# Document no Modifica Integration Directamente

Document mantiene ownership propio.

---

# External System no Modifica Integration Directamente

Ningún sistema externo posee autoridad directa para cambiar el
Aggregate.

---

# FIWARE no Modifica Aggregate Directamente

Debe mantenerse:

```text
FIWARE

≠

Integration Mutation Authority
```

---

# Municipal System no Modifica Aggregate Directamente

Debe mantenerse:

```text
Municipal System

≠

Integration Mutation Authority
```

---

# Infrastructure no Modifica Domain Rules

Infrastructure puede implementar mecanismos técnicos.

No puede redefinir:

- State;
- Commands;
- Domain Events;
- Invariants;
- Versioning;
- Lifecycle.

---

# Invariant de Active

Cuando:

```text
State = Active
```

significa únicamente que la Integration está formalmente habilitada.

No garantiza éxito técnico.

---

# Active no Requiere Conectividad Persistente

Debe mantenerse:

```text
Active

≠

Connected
```

---

# Invariant de Suspended

Cuando:

```text
State = Suspended
```

la Integration permanece existente pero formalmente suspendida.

---

# Suspended Conserva Identidad

Debe mantenerse:

```text
IntegrationId before suspension

=

IntegrationId after suspension
```

---

# Suspended no es Deleted

Debe mantenerse:

```text
Suspended

≠

Deleted
```

---

# Invariant de Archived

Cuando:

```text
State = Archived
```

la Integration permanece históricamente identificable pero fuera del
flujo operativo.

---

# Archived Conserva Identidad

Debe mantenerse:

```text
IntegrationId before archive

=

IntegrationId after archive
```

---

# Archived no es Physical Deletion

Debe mantenerse:

```text
Archived

≠

Physical Deletion
```

---

# Retención no es Invariant Actual

La versión 1.0 no define:

- retention period;
- expiry;
- purge;
- automatic deletion.

No deben inferirse como Invariants.

---

# Anonymization no es Invariant Actual

La versión 1.0 no define reglas de:

```text
Anonymization
```

dentro de Integration.

---

# Redaction no es Invariant Actual

La versión 1.0 no define reglas de:

```text
Redaction
```

dentro de Integration.

---

# Deletion no es Comportamiento de Dominio

La versión 1.0 no define:

```text
DeleteIntegration
```

---

# Invariant de Trazabilidad

Las modificaciones válidas deben preservar:

- IntegrationId;
- Version;
- timestamps;
- Domain Events correspondientes.

---

# Trazabilidad no es Observability

Debe mantenerse:

```text
Domain Traceability

≠

Technical Observability
```

---

# Logs no son Estado

Logs técnicos no forman parte del Aggregate.

---

# Metrics no son Estado

Metrics técnicas no forman parte del Aggregate.

---

# Health Status no es State

Health information no constituye Lifecycle State.

---

# Invariant de Domain Event Payload

Un Domain Event no debe contener el Aggregate completo como Payload.

---

# Domain Event Payload no Contiene Secretos

Debe mantenerse:

```text
Secret

∉

Domain Event Payload
```

---

# Domain Event Payload no Contiene Credenciales

Debe mantenerse:

```text
Credentials

∉

Domain Event Payload
```

---

# Domain Event Inmutable

Una vez confirmado:

```text
Domain Event

=

Immutable Fact
```

---

# Historical Meaning

Un evento histórico no debe reinterpretarse retrospectivamente como un
hecho distinto.

---

# Integration Event no Reemplaza Domain Event

Debe mantenerse:

```text
Integration Event

≠

Domain Event Replacement
```

---

# External Publication no Cambia Hecho Interno

Un fallo o éxito de publicación externa no modifica retroactivamente
un Domain Event confirmado.

---

# Retry de Publicación

Retry técnico no constituye una nueva modificación del Aggregate.

---

# Outbox State no es Aggregate State

Estados técnicos de Outbox no forman parte de Integration.

---

# Queue State no es Aggregate State

Estados técnicos de Queue no forman parte de Integration.

---

# Broker ACK no es Domain Fact

Un acknowledgement técnico no modifica el Aggregate.

---

# Delivery Failure no es Domain Transition

Una falla de entrega no produce automáticamente:

```text
Active → Suspended
```

---

# Event Sourcing

Las Invariants deben mantenerse independientemente de si se utiliza o
no Event Sourcing.

---

# Event Sourcing no Cambia Invariants

Debe mantenerse:

```text
Persistence Strategy

≠

Invariant Semantics
```

---

# Rehydration Preserva Invariants

Toda Integration rehidratada debe satisfacer las mismas Invariants que
una Integration en memoria.

---

# Replay no Crea Nuevas Reglas

Replay reconstruye el Aggregate.

No redefine Invariants.

---

# CQRS

Separar Command Side y Query Side no modifica las Invariants del Write
Model.

---

# Read Side no Valida Estado para Escritura

La validez del Aggregate no depende de la representación de un Read
Model.

---

# Performance

Una optimización no puede evitar ninguna Invariant.

Debe mantenerse:

```text
Performance Optimization

≠

Invariant Bypass
```

---

# Cache no Puede Ser Autoridad

Una Cache no puede utilizarse para ignorar la Version real del
Aggregate.

---

# Replica no Puede Redefinir State

Una réplica técnica no redefine el State autoritativo.

---

# Bulk Processing

Procesar varias Integration no fusiona sus Consistency Boundaries.

Debe mantenerse:

```text
One IntegrationId

=

One Aggregate Boundary
```

---

# No Global Integration Aggregate

No debe existir una única Integration que contenga el estado de todas
las integraciones de AURA.

---

# Different IntegrationId

Integration con identidades distintas deben mantener estado y Version
independientes.

---

# Same IntegrationId

Operaciones concurrentes sobre la misma identidad deben respetar
Versioning.

---

# Invariant de Idempotencia

La repetición técnica de un mensaje no debe interpretarse
automáticamente como una nueva intención real.

Debe mantenerse:

```text
Technical Redelivery

≠

New Domain Intent
```

---

# Estrategia de Idempotencia

La estrategia concreta de idempotencia no se define como Invariant del
Aggregate en versión 1.0.

---

# Deduplicación

Deduplicación técnica no crea automáticamente una regla de cardinalidad
de dominio.

---

# No One-to-One Implícito

Este documento no establece reglas adicionales de cardinalidad entre:

```text
External Message

Integration

Domain Event

Integration Event
```

más allá de las identidades ya definidas.

---

# Invariant de Orden

Para una misma Integration, Version representa orden lógico de
evolución.

---

# No Orden Global

No existe una Invariant que exija orden global entre diferentes
IntegrationId.

---

# Timestamp no Sustituye Version

Debe mantenerse:

```text
Timestamp

≠

Aggregate Version
```

---

# State no Sustituye Version

Debe mantenerse:

```text
State

≠

Version
```

---

# Version no Sustituye State

Debe mantenerse:

```text
Version

≠

State
```

---

# Contract no Sustituye State

Debe mantenerse:

```text
Contract Status

≠

Integration State
```

salvo definición formal futura.

---

# External Status no Sustituye State

Estados externos como:

```text
ENABLED

DISABLED

ERROR

ONLINE

OFFLINE
```

no se convierten automáticamente en:

```text
Draft

Active

Suspended

Archived
```

---

# Invariant de Independencia de FIWARE

Ninguna Invariant requiere que Integration conozca internamente:

```text
NGSI-LD

Context Broker

Orion

FIWARE Entity
```

---

# FIWARE Entity no es Internal Entity

Debe mantenerse:

```text
FIWARE Entity

≠

Integration Internal Entity
```

---

# Municipal Model no es Internal Model

Debe mantenerse:

```text
Municipal Model

≠

Integration Internal Model
```

---

# External API no es Domain Model

Debe mantenerse:

```text
External API Schema

≠

Integration Domain Model
```

---

# Invariant de Internal Entities

La versión 1.0 no establece entidades internas concretas.

Ninguna implementación debe inventarlas como requisito de dominio sin
definición formal.

---

# Invariant de Value Objects

La versión 1.0 no establece Value Objects específicos obligatorios de
Integration.

No deben introducirse por conveniencia técnica.

---

# Source of Truth

Integration es fuente de verdad solamente para su propio estado.

Debe mantenerse:

```text
Integration

=

Source of Truth for Integration
```

---

# No Source of Truth Externo

Integration no es fuente de verdad para:

```text
FIWARE

Municipal System

External Platform

Other Aggregate
```

---

# External System no es Source of Truth de Integration

Del mismo modo:

```text
External System

≠

Source of Truth for Integration State
```

---

# Regla de Validación Previa

Antes de toda modificación deben ser válidos:

```text
Identity

Current State

Permission

Guards

Invariants

ExpectedVersion
```

cuando corresponda.

---

# Regla de Validación Posterior

Después de toda modificación válida deben seguir siendo válidos:

```text
Identity

Resulting State

Invariants

Version

Timestamps

Domain Event consistency
```

---

# Invariant Failure

Si cualquier Invariant falla:

```text
Operation = Rejected
```

---

# Resultado de Invariant Failure

Debe mantenerse:

```text
State unchanged

Version unchanged

UpdatedAt unchanged

No success Domain Event
```

---

# No Partial Mutation

Una Invariant fallida no debe dejar modificaciones parciales.

---

# No Recovery by Mutation

El Repository o Infrastructure no puede modificar silenciosamente el
Aggregate para convertir un estado inválido en válido.

---

# Regla de Rechazo

La seguridad del Aggregate debe favorecer:

```text
Reject Invalid Operation

rather than

Persist Invalid State
```

---

# Evolución Futura

Toda nueva Invariant requiere una necesidad explícita del dominio.

No debe inferirse desde Infrastructure.

---

# Nueva Invariant

Una nueva Invariant debe:

- pertenecer a Integration;
- proteger una regla real;
- ser compatible con Lifecycle;
- ser compatible con State Machine;
- ser compatible con Commands;
- ser compatible con Domain Events;
- ser compatible con Versioning;
- respetar Consistency Boundary;
- ser verificable mediante Test Scenarios.

---

# Impacto de una Nueva Invariant

Toda nueva Invariant debe revisar cuando corresponda:

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

---

# Regla de No Inferencia

Debe mantenerse:

```text
Technical Constraint

≠

Domain Invariant
```

y:

```text
External Requirement

≠

Automatic Domain Invariant
```

---

# Reglas Fundamentales

Las Invariants del Aggregate Integration deben cumplir:

1. IntegrationId es obligatorio.
2. IntegrationId es único.
3. IntegrationId es inmutable.
4. IntegrationId no se reutiliza para otra identidad.
5. IntegrationId no es ExternalSystemId.
6. IntegrationId no es EventId.
7. IntegrationId no es CorrelationId.
8. IntegrationId no es CausationId.
9. La Aggregate Root es la única autoridad de modificación.
10. No existen setters públicos para evitar comportamiento de dominio.
11. Todo Aggregate persistido posee exactamente un State oficial.
12. Los únicos States oficiales son Draft, Active, Suspended y
    Archived.
13. No Integration representa inexistencia.
14. No Integration no es State persistido.
15. Toda Integration comienza en Draft.
16. Archived es terminal.
17. Archived no puede reactivarse.
18. Una Integration que abandona Draft no vuelve a Draft.
19. Solamente las transiciones oficiales son válidas.
20. Toda transición no declarada es rechazada.
21. Active → Draft es inválida.
22. Suspended → Draft es inválida.
23. Archived → Draft es inválida.
24. Archived → Active es inválida.
25. Archived → Suspended es inválida.
26. Archived → Archived no es transición.
27. Los únicos Commands oficiales son CreateIntegration,
    ActivateIntegration, SuspendIntegration, ReactivateIntegration y
    ArchiveIntegration.
28. CreateIntegration solamente opera desde inexistencia.
29. CreateIntegration produce Draft.
30. CreateIntegration no sobrescribe una Integration existente.
31. ActivateIntegration solamente opera desde Draft.
32. ActivateIntegration produce Active.
33. SuspendIntegration solamente opera desde Active.
34. SuspendIntegration produce Suspended.
35. ReactivateIntegration solamente opera desde Suspended.
36. ReactivateIntegration produce Active.
37. ArchiveIntegration solamente opera desde Draft, Active o
    Suspended.
38. ArchiveIntegration produce Archived.
39. Commands técnicos no forman parte del dominio.
40. Los únicos Domain Events oficiales son IntegrationCreated,
    IntegrationActivated, IntegrationSuspended,
    IntegrationReactivated e IntegrationArchived.
41. Cada Domain Event debe corresponder a comportamiento válido.
42. Una operación rechazada no produce Domain Event de éxito.
43. IntegrationCreated solamente corresponde a creación válida.
44. IntegrationActivated solamente corresponde a Draft → Active.
45. IntegrationSuspended solamente corresponde a Active → Suspended.
46. IntegrationReactivated solamente corresponde a Suspended →
    Active.
47. IntegrationArchived solamente corresponde a rutas válidas hacia
    Archived.
48. EventId es único e inmutable.
49. Un EventId representa un único hecho.
50. AggregateVersion coincide con la Version resultante.
51. AggregateVersion no es Contract Version.
52. Una modificación válida incrementa Version conforme al contrato.
53. Una operación rechazada no incrementa Version.
54. Lecturas no incrementan Version.
55. Rehydration no incrementa Version.
56. Replay no incrementa Version artificialmente.
57. Retry técnico no incrementa Version.
58. Projection no incrementa Version.
59. Publicación externa no incrementa Version.
60. ExpectedVersion debe coincidir con PersistedVersion cuando
    corresponda.
61. ConcurrencyConflict rechaza la modificación.
62. Permission no permite evitar concurrencia.
63. CreatedAt se establece en creación.
64. CreatedAt es inmutable.
65. UpdatedAt cambia solamente por modificación válida.
66. Rechazo no modifica UpdatedAt.
67. Integration solamente posee su propio estado.
68. Referencias externas no transfieren ownership.
69. Otros Aggregates no se embeben dentro de Integration.
70. Sistemas externos no se embeben dentro de Integration.
71. Una operación modifica solamente un Integration Aggregate.
72. Consistencia interna es inmediata.
73. Consistencia externa es eventual.
74. Source Aggregate Transaction no es Integration Transaction.
75. External System Transaction no es Integration Transaction.
76. La validez del Aggregate no depende de protocolo.
77. La validez del Aggregate no depende de broker.
78. La validez del Aggregate no depende de base de datos.
79. La validez del Aggregate no depende de FIWARE availability.
80. La validez del Aggregate no depende de Municipal System
    availability.
81. Technical Health no determina Lifecycle State.
82. Connected no es State.
83. Disconnected no es State.
84. Failed no es State.
85. Pending no es State.
86. Deleted no es State.
87. Cancelled no es State.
88. Technical Failure no produce transición automática.
89. Technical Recovery no produce reactivación automática.
90. Integration requiere contratos explícitos para interoperabilidad.
91. Integration Contract no es Integration Aggregate.
92. Contract Version no es Integration.Version.
93. External Model no es AURA Domain Model.
94. Domain Event no es Integration Event.
95. Domain Event no obliga publicación externa.
96. External Message no es automáticamente Domain Fact ni Command.
97. CorrelationId y CausationId no conceden autoridad.
98. External Payload no se convierte automáticamente en Aggregate
    State.
99. Credenciales y secretos permanecen fuera del Aggregate.
100. Toda nueva Invariant requiere definición formal de dominio.

---

# Restricciones

No está permitido:

- crear Integration sin IntegrationId;
- modificar IntegrationId;
- reutilizar IntegrationId para otra Integration;
- usar EventId como IntegrationId;
- modificar State directamente;
- modificar Version directamente;
- modificar CreatedAt;
- persistir más de un State actual;
- crear Integration fuera de Draft;
- regresar a Draft después de abandonar Draft;
- reactivar Archived;
- ejecutar transiciones no definidas;
- ejecutar ActivateIntegration fuera de Draft;
- ejecutar SuspendIntegration fuera de Active;
- ejecutar ReactivateIntegration fuera de Suspended;
- ejecutar ArchiveIntegration desde Archived;
- introducir Commands técnicos como comportamiento del Aggregate;
- producir Domain Events sin un hecho confirmado;
- producir Domain Events de éxito después de rechazo;
- producir Domain Events de éxito después de ConcurrencyConflict;
- incrementar Version ante una operación rechazada;
- modificar UpdatedAt ante una operación rechazada;
- ignorar ExpectedVersion cuando corresponda;
- embebir otros Aggregates;
- embebir sistemas externos completos;
- modificar otros Aggregates desde Integration;
- modificar sistemas externos dentro de la misma transacción del
  Aggregate;
- utilizar estado técnico como Lifecycle State;
- utilizar Connected;
- utilizar Disconnected;
- utilizar Failed;
- utilizar Pending;
- utilizar Deleted;
- utilizar Cancelled;
- suspender automáticamente por timeout;
- suspender automáticamente por Broker Failure;
- suspender automáticamente por FIWARE Failure;
- suspender automáticamente por Municipal System Failure;
- reactivar automáticamente por Technical Recovery;
- convertir modelos externos directamente en modelo interno;
- confundir Contract Version con Integration.Version;
- confundir Domain Event con Integration Event;
- publicar automáticamente todo Domain Event;
- utilizar un External Message directamente como modificación del
  Aggregate;
- copiar automáticamente External Payload completo;
- fabricar información faltante;
- almacenar Password;
- almacenar AccessToken;
- almacenar RefreshToken;
- almacenar ApiKey;
- almacenar PrivateKey;
- almacenar ClientSecret;
- almacenar Secret;
- permitir que Repository decida State;
- permitir que Repository decida Permissions;
- permitir que Repository invente Domain Events;
- permitir que Read Model modifique Integration;
- permitir que Projection modifique Integration;
- utilizar Performance para evitar Invariants;
- utilizar Cache como autoridad sobre State o Version;
- fusionar múltiples IntegrationId en un único Consistency Boundary;
- convertir Technical Redelivery en nueva intención automáticamente;
- imponer cardinalidades no definidas;
- introducir orden global no definido;
- introducir una nueva Invariant por conveniencia técnica;
- introducir una nueva Invariant sin revisar los contratos afectados.

---

# Compatibilidad Arquitectónica

Las Invariants de Integration son compatibles con:

- Domain-Driven Design;
- Aggregate Pattern;
- State Machine Pattern;
- Command Pattern;
- Domain Event Pattern;
- Repository Pattern;
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

Estas compatibilidades no modifican las Invariants ni imponen una
tecnología concreta.

---

# Definición de Éxito

Las Invariants del Aggregate **Integration** garantizan que toda
Integration permanezca conceptualmente válida durante su Lifecycle.

El núcleo protegido queda expresado por:

```text
IntegrationId
    │
    ▼
Valid Identity
    │
    ▼
Valid State
    │
    ▼
Valid Command
    │
    ▼
Valid Transition
    │
    ▼
Valid Version
    │
    ▼
Confirmed Domain Event
```

El modelo garantiza que:

- IntegrationId sea único e inmutable;
- cada Aggregate tenga exactamente un State válido;
- solamente existan Draft, Active, Suspended y Archived;
- toda Integration comience en Draft;
- Archived permanezca terminal;
- solamente las transiciones oficiales puedan ocurrir;
- Commands respeten Lifecycle y State Machine;
- Domain Events representen únicamente hechos confirmados;
- EventId identifique un único hecho;
- AggregateVersion corresponda a la Version resultante;
- Version evolucione solamente mediante modificaciones válidas;
- ConcurrencyConflict impida sobrescrituras incompatibles;
- CreatedAt permanezca inmutable;
- UpdatedAt cambie solamente ante modificaciones válidas;
- Integration mantenga ownership exclusivamente sobre su propio
  estado;
- otros Aggregates permanezcan fuera del Consistency Boundary;
- sistemas externos permanezcan fuera del Consistency Boundary;
- consistencia externa permanezca eventual;
- protocolos, brokers, bases de datos y frameworks no definan reglas
  del dominio;
- FIWARE no determine State ni validez;
- sistemas municipales no determinen State ni validez;
- fallos técnicos no se conviertan en transiciones;
- recuperación técnica no se convierta en reactivación;
- Domain Events e Integration Events permanezcan conceptualmente
  separados;
- contratos externos no sustituyan el Domain Model;
- External Payloads no se conviertan automáticamente en estado;
- información ausente no sea fabricada;
- credenciales y secretos permanezcan fuera del Aggregate;
- Repository preserve pero no decida las reglas;
- Read Models y Projections permanezcan sin autoridad de escritura;
- optimizaciones no puedan evitar Invariants;
- cada IntegrationId conserve su propio Consistency Boundary;
- cualquier nueva Invariant requiera definición explícita y evolución
  coordinada del dominio.

De esta forma, `DOMAIN-013E-Invariants.md` establece formalmente las
Invariants oficiales del Aggregate **Integration** conforme al patrón
consolidado de AURA Core.