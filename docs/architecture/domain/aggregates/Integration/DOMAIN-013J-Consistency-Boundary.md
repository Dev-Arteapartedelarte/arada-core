# DOMAIN-013J — Integration Consistency Boundary

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
- DOMAIN-013E-Invariants.md
- DOMAIN-013F-Permissions.md
- DOMAIN-013G-Repository-Contract.md
- DOMAIN-013H-Examples.md
- DOMAIN-013I-Versioning.md
- DOMAIN-013K-Integration-Events.md
- DOMAIN-013L-Read-Model.md
- DOMAIN-013M-Test-Scenarios.md
- DOMAIN-013N-Performance-Rules.md
- DOMAIN-013O-Security-Model.md
- DOMAIN-013P-Extension-Points.md

---

# Objetivo

Este documento define formalmente el **Consistency Boundary** del
Aggregate **Integration**.

El Consistency Boundary establece qué información, reglas y
modificaciones deben mantenerse consistentes de manera inmediata
dentro de una única transacción lógica del Aggregate.

También establece qué conceptos permanecen fuera de ese límite y se
coordinan mediante consistencia eventual.

---

# Principio Fundamental

Debe mantenerse:

```text
One IntegrationId

=

One Aggregate Consistency Boundary
```

Una Integration protege exclusivamente su propio estado y sus propias
Invariants.

---

# Aggregate Boundary

El límite de consistencia está centrado en:

```text
Integration
```

como única Aggregate Root.

Toda modificación válida debe preservar inmediatamente la consistencia
interna de esa única Integration.

---

# Identidad del Boundary

El Boundary está determinado por:

```text
IntegrationId
```

Dos Integration con IntegrationId diferentes representan dos
Consistency Boundaries independientes.

---

# Una Integration por Boundary

Debe mantenerse:

```text
IntegrationId = X

→

Boundary X
```

y:

```text
IntegrationId = Y

→

Boundary Y
```

donde:

```text
X ≠ Y
```

implica límites de consistencia independientes.

---

# No Global Integration Aggregate

El conjunto de todas las Integration no constituye un único Aggregate.

Debe mantenerse:

```text
Many Integration Aggregates

≠

One Global Integration Aggregate
```

---

# Contenido del Consistency Boundary

El Boundary de Integration contiene conceptualmente:

```text
IntegrationId

State

Version

CreatedAt

UpdatedAt

Domain Information formally defined for Integration

Internal Entities formally defined for Integration

Value Objects formally defined for Integration

Domain Events produced by valid Integration behavior
```

solamente cuando cada concepto esté formalmente definido por el
dominio.

---

# Internal Entities

La versión 1.0 no establece Internal Entities concretas.

Por lo tanto, el Consistency Boundary no debe ampliarse mediante
entidades internas inventadas por conveniencia técnica.

---

# Value Objects

La versión 1.0 no establece Value Objects específicos obligatorios de
Integration.

Cualquier Value Object futuro deberá pertenecer conceptualmente al
Boundary solamente cuando sea definido formalmente.

---

# Concepts Outside the Boundary

Permanecen fuera del Consistency Boundary:

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

External Systems

FIWARE

Municipal Systems

Smart City Platforms

Read Models

Authentication

Authorization

Infrastructure

Transport

Brokers

Databases

External APIs

External Contracts
```

salvo referencias conceptuales explícitamente necesarias.

---

# Referencia no Expande Boundary

Debe mantenerse:

```text
External Reference

≠

Consistency Boundary Membership
```

Una referencia a otro Aggregate o sistema no lo convierte en parte
interna de Integration.

---

# Ownership

Integration mantiene ownership únicamente sobre:

```text
Integration
```

y los conceptos internos que sean formalmente definidos como parte del
Aggregate.

No adquiere ownership sobre otros Aggregates por referenciarlos.

---

# No Aggregate Embedding

No está permitido incorporar como parte mutable interna:

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

# Source Aggregate no Pertenece al Boundary

Cuando Integration participa en un flujo originado por otro Aggregate:

```text
Source Aggregate

∉

Integration Consistency Boundary
```

---

# Source Domain Event no Expande Boundary

Un Domain Event producido por otro Aggregate puede ser observado o
procesado mediante contratos explícitos.

Esto no incorpora:

```text
Source Aggregate

or

Source Domain Event ownership
```

dentro de Integration.

---

# External System no Pertenece al Boundary

Debe mantenerse:

```text
External System

∉

Integration Aggregate
```

---

# FIWARE no Pertenece al Boundary

Debe mantenerse:

```text
FIWARE

∉

Integration Consistency Boundary
```

---

# Municipal System no Pertenece al Boundary

Debe mantenerse:

```text
Municipal System

∉

Integration Consistency Boundary
```

---

# Smart City Platform no Pertenece al Boundary

Debe mantenerse:

```text
Smart City Platform

∉

Integration Consistency Boundary
```

---

# External Contract no es Internal Aggregate State

Un Integration Contract puede definir una relación semántica con un
sistema o contexto externo.

Debe mantenerse:

```text
Integration Contract

≠

Integration Aggregate
```

La existencia del contrato no fusiona los respectivos Boundaries.

---

# Consistencia Interna

Dentro de Integration, la consistencia debe ser inmediata.

Toda operación válida debe finalizar con:

```text
Valid Identity

Valid State

Valid Version

Valid Timestamps

Valid Invariants

Valid Domain Event relationship
```

conforme a las reglas del Aggregate.

---

# Consistencia Externa

La relación entre Integration y otros Aggregates o sistemas externos
permanece bajo:

```text
Eventual Consistency
```

---

# Internal Consistency versus External Consistency

Debe mantenerse:

```text
Integration Internal Consistency

=

Immediate
```

mientras:

```text
Cross-Boundary Consistency

=

Eventual
```

---

# Integration Transaction

Una transacción de dominio de Integration modifica:

```text
One Integration Aggregate
```

---

# No Cross-Aggregate Transaction

Debe mantenerse:

```text
Integration Transaction

≠

Organization Transaction

≠

Citizen Transaction

≠

Assembly Transaction

≠

Notification Transaction

≠

Audit Transaction
```

---

# No Shared Aggregate Transaction

Una operación de Integration no debe modificar atómicamente otro
Aggregate como parte del mismo Consistency Boundary.

---

# Source Aggregate Transaction

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

# FIWARE Transaction

Debe mantenerse:

```text
Integration Commit

≠

FIWARE Commit
```

---

# Municipal Transaction

Debe mantenerse:

```text
Integration Commit

≠

Municipal System Commit
```

---

# No Distributed Aggregate

Debe mantenerse:

```text
Integration

+

External System

≠

One Distributed Aggregate
```

---

# No Distributed Transaction Requirement

La versión 1.0 no establece como regla del dominio:

```text
Distributed Transaction
```

entre Integration y otros sistemas.

---

# No Two-Phase Commit Requirement

Este documento no exige:

```text
Two-Phase Commit
```

para coordinar Integration con sistemas externos.

---

# Atomicidad Interna

Una modificación válida de Integration debe ser atómica dentro de su
propio Boundary.

No debe confirmarse parcialmente:

```text
State changed

but

Version unchanged
```

cuando la modificación válida requiera ambos cambios.

---

# No Partial Aggregate Commit

Debe mantenerse:

```text
Partial Aggregate Commit

=

Invalid
```

---

# Creation Boundary

CreateIntegration modifica exclusivamente la nueva Integration.

Conceptualmente:

```text
No Integration
    │
    ▼
CreateIntegration
    │
    ▼
Integration Boundary
    │
    ▼
Draft
```

---

# CreateIntegration no Crea otros Aggregates

`CreateIntegration` no crea atómicamente:

```text
Organization

Citizen

Audit

Notification
```

ni ningún otro Aggregate.

---

# ActivateIntegration Boundary

`ActivateIntegration` produce:

```text
Draft → Active
```

únicamente dentro de Integration.

---

# ActivateIntegration no Activa Sistema Externo

Debe mantenerse:

```text
ActivateIntegration

≠

External System Activation
```

---

# SuspendIntegration Boundary

`SuspendIntegration` modifica únicamente:

```text
Integration
```

---

# SuspendIntegration no Suspende Sistemas Externos

Debe mantenerse:

```text
Integration Suspension

≠

External System Suspension
```

---

# ReactivateIntegration Boundary

`ReactivateIntegration` modifica exclusivamente la Integration
Suspended correspondiente.

---

# ReactivateIntegration no Reactiva Sistema Externo

Debe mantenerse:

```text
Integration Reactivation

≠

External System Reactivation
```

---

# ArchiveIntegration Boundary

`ArchiveIntegration` modifica únicamente Integration.

---

# ArchiveIntegration no Archiva otros Aggregates

Debe mantenerse:

```text
Integration Archived

≠

Other Aggregate Archived
```

---

# Lifecycle Boundary

Los estados:

```text
Draft

Active

Suspended

Archived
```

pertenecen únicamente a Integration.

---

# External State no Cruza Boundary

Debe mantenerse:

```text
External State

≠

Integration State
```

---

# Source Aggregate State no Cruza Boundary

Debe mantenerse:

```text
Source Aggregate State

≠

Integration State
```

---

# FIWARE State no Cruza Boundary

Debe mantenerse:

```text
FIWARE State

≠

Integration State
```

---

# Municipal State no Cruza Boundary

Debe mantenerse:

```text
Municipal System State

≠

Integration State
```

---

# Technical State no Cruza Boundary

Conceptos como:

```text
Connected

Disconnected

Queued

Processing

Retrying

Failed

Healthy

Unhealthy
```

permanecen fuera del Lifecycle oficial.

---

# Technical Health Outside Boundary

Debe mantenerse:

```text
Technical Health

∉

Integration Domain State
```

---

# Infrastructure Failure

Un fallo de Infrastructure no constituye automáticamente una
modificación interna del Aggregate.

---

# External Failure

Debe mantenerse:

```text
External Failure

≠

Integration State Transition
```

---

# External Recovery

Debe mantenerse:

```text
External Recovery

≠

Integration State Transition
```

---

# Timeout

Un timeout ocurre fuera del Boundary del Lifecycle.

No produce automáticamente:

```text
Active → Suspended
```

---

# Broker Failure

Un fallo de broker no cruza automáticamente la frontera como una
transición de dominio.

---

# FIWARE Failure

Una indisponibilidad FIWARE no modifica automáticamente Integration.

---

# Municipal System Failure

Una indisponibilidad municipal tampoco modifica automáticamente el
Aggregate.

---

# Domain Event Boundary

Los Domain Events:

```text
IntegrationCreated

IntegrationActivated

IntegrationSuspended

IntegrationReactivated

IntegrationArchived
```

expresan hechos confirmados dentro del Consistency Boundary de
Integration.

---

# Domain Event no Confirma otros Boundaries

`IntegrationActivated` confirma:

```text
Integration = Active
```

No confirma:

```text
External System = Active

FIWARE = Available

Municipal System = Updated

Audit = Recorded

Notification = Delivered
```

---

# Domain Event Ownership

Debe mantenerse:

```text
Integration Domain Event

owned by

Integration
```

---

# Domain Event no Fusiona Boundaries

El hecho de que otro contexto consuma un Domain Event no fusiona sus
Consistency Boundaries.

---

# Integration Event Boundary

Un Integration Event, cuando exista por contrato explícito, cruza una
frontera de interoperabilidad.

Debe mantenerse:

```text
Integration Event

≠

Shared Aggregate State
```

---

# Domain Event versus Integration Event

Debe mantenerse:

```text
Domain Event

≠

Integration Event
```

---

# No Mandatory Integration Event

Una modificación confirmada dentro de Integration no obliga
automáticamente a publicar un Integration Event.

---

# Publication Outside Boundary

La publicación hacia otros sistemas ocurre fuera de la modificación
interna del Aggregate.

---

# External Publication Failure

Una vez confirmado:

```text
Integration State Change
```

un fallo posterior de publicación externa no revierte automáticamente
el Aggregate.

---

# Retry Outside Boundary

El retry técnico de una publicación pertenece fuera del Consistency
Boundary de Integration.

No constituye:

```text
New Integration Modification
```

---

# Redelivery Outside Boundary

Una retransmisión técnica tampoco constituye automáticamente una nueva
modificación.

---

# Repository Boundary

IntegrationRepository persiste:

```text
One Integration Aggregate
```

como unidad.

---

# Repository no Expande Boundary

El Repository no puede incorporar otro Aggregate dentro de la misma
unidad de consistencia solamente por conveniencia de persistencia.

---

# save()

`save()` debe preservar el Boundary de una única Integration.

---

# findById()

`findById()` recupera:

```text
One Integration
```

por IntegrationId.

---

# Repository no Ejecuta Cross-Boundary Behavior

El Repository no:

- publica hacia FIWARE;
- modifica sistemas municipales;
- modifica Notification;
- modifica Audit;
- ejecuta Commands de otros Aggregates.

---

# Repository Transaction

Debe mantenerse:

```text
IntegrationRepository Transaction

=

Integration Persistence Boundary
```

dentro de la semántica del Aggregate.

---

# Repository.delete()

La existencia de:

```text
Repository.delete()
```

no modifica el Consistency Boundary ni introduce:

```text
Deleted
```

como State.

---

# Archive versus Delete

Debe mantenerse:

```text
ArchiveIntegration

≠

Repository.delete()
```

---

# Read Model Outside Boundary

Los Read Models permanecen fuera del Consistency Boundary de escritura.

Debe mantenerse:

```text
Read Model

∉

Integration Write Boundary
```

---

# Read Model no es Aggregate State

Una Projection representa información derivada.

No forma parte del estado autoritativo requerido para mantener
Invariants de Integration.

---

# Projection Lag

Puede existir:

```text
Aggregate State = Active

Read Model State = Draft
```

temporalmente.

Esto no viola la consistencia interna de Integration.

---

# Projection Failure

Un fallo de Projection no revierte la transacción ya confirmada del
Aggregate.

---

# Projection Rebuild

Reconstruir un Read Model no modifica el Consistency Boundary de
Integration.

---

# Query Outside Write Boundary

Búsqueda, filtrado, ordenamiento, paginación, reporting y analytics
permanecen fuera del Boundary de escritura.

---

# CQRS

En CQRS:

```text
Write Side

owns

Integration Consistency Boundary
```

mientras:

```text
Read Side

projects

Integration Information
```

---

# Event Sourcing

Event Sourcing no altera el Consistency Boundary.

Debe mantenerse:

```text
Persistence Strategy

≠

Aggregate Boundary
```

---

# Event Sourcing Compatible

Si Event Sourcing fuese utilizado, el Event Stream correspondiente a
una Integration debe preservar:

```text
one IntegrationId

one logical Aggregate history
```

---

# External Event Stream

Debe mantenerse:

```text
External Event Stream

≠

Integration Aggregate Event Stream
```

---

# Replay

Replay reconstruye el mismo Boundary.

No fusiona Integration con otros Aggregates.

---

# Rehydration

Rehydration reconstruye:

```text
One Integration Aggregate
```

preservando su identidad, State, Version e Invariants.

---

# Version Boundary

Integration.Version pertenece exclusivamente a una Integration.

Debe mantenerse:

```text
One IntegrationId

=

One Version Sequence
```

---

# No Shared Version

No existe:

```text
Shared Version
```

entre Integration y otro Aggregate.

---

# External Version

Debe mantenerse:

```text
External System Version

≠

Integration.Version
```

---

# Contract Version

Debe mantenerse:

```text
Integration Contract Version

≠

Integration.Version
```

---

# Domain Event AggregateVersion

`DomainEvent.AggregateVersion` pertenece a la evolución lógica de la
Integration productora.

No constituye una Version compartida con consumidores.

---

# Optimistic Concurrency

Optimistic Concurrency protege modificaciones concurrentes sobre:

```text
Same IntegrationId
```

---

# ExpectedVersion Scope

ExpectedVersion se compara con:

```text
PersistedVersion
```

de la misma Integration.

---

# ExpectedVersion no Cruza Aggregates

No debe compararse:

```text
Integration.ExpectedVersion

with

OtherAggregate.Version
```

como regla de consistencia interna.

---

# Different IntegrationId Concurrency

Dos Integration distintas poseen control de concurrencia independiente.

---

# No Global Lock de Dominio

La versión 1.0 no establece como requisito conceptual un lock global
sobre todas las Integration.

---

# Permission Outside Aggregate State

Las Permissions protegen Commands.

No forman parte del estado interno del Aggregate.

---

# Authorization Outside Boundary

Debe mantenerse:

```text
Authorization

∉

Integration Domain State
```

---

# Authentication Outside Boundary

Debe mantenerse:

```text
Authentication

∉

Integration Aggregate
```

---

# Credentials Outside Boundary

No pertenecen al Consistency Boundary:

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

---

# Authorization Decision no Modifica Boundary

Una decisión:

```text
Allowed

Denied
```

no constituye un State del Aggregate.

---

# Permission Change

Cambiar una Authorization Policy externa no modifica:

```text
Integration.State

Integration.Version

Integration.UpdatedAt
```

por sí mismo.

---

# Role Outside Boundary

Role permanece bajo ownership de su propio dominio.

Una referencia a Role no incorpora el Role Aggregate dentro de
Integration.

---

# Membership Outside Boundary

Membership permanece fuera del Boundary.

---

# Citizen Outside Boundary

Citizen permanece fuera del Boundary.

---

# ActorId no Expande Boundary

Cuando ActorId forme parte de una intención o hecho:

```text
ActorId

≠

Embedded Citizen
```

---

# Organization Outside Boundary

Organization permanece fuera del Boundary.

---

# Territory Outside Boundary

Territory permanece fuera del Boundary.

---

# Assembly Outside Boundary

Assembly mantiene su propia unidad de consistencia.

---

# Proposal Outside Boundary

Proposal mantiene su propia unidad de consistencia.

---

# Participation Outside Boundary

Participation mantiene su propia transacción.

---

# Voting Outside Boundary

Voting mantiene Lifecycle y Version independientes.

---

# Document Outside Boundary

Document mantiene ownership independiente.

---

# Notification Outside Boundary

Notification permanece fuera de Integration.

Debe mantenerse:

```text
Integration State Transition

≠

Notification State Transition
```

---

# Audit Outside Boundary

Audit permanece fuera de Integration.

Debe mantenerse:

```text
Integration Domain Fact

≠

Audit State
```

---

# Audit Failure

Si Audit no procesa inmediatamente un hecho:

```text
Integration remains confirmed
```

conforme al estado ya persistido.

---

# Notification Failure

Una falla de Notification no revierte Integration.

---

# External Consumer Failure

El fallo de un consumidor externo no revierte el Aggregate ya
confirmado.

---

# Integration Boundary versus Integration Contract

Debe mantenerse:

```text
Aggregate Consistency Boundary

≠

Integration Contract Boundary
```

Un contrato describe interoperabilidad.

El Aggregate protege consistencia interna.

---

# Integration Boundary versus Network Boundary

Debe mantenerse:

```text
Domain Consistency Boundary

≠

Network Boundary
```

---

# Integration Boundary versus Deployment Boundary

Debe mantenerse:

```text
Aggregate Boundary

≠

Deployment Unit
```

---

# Integration Boundary versus Database Boundary

Debe mantenerse:

```text
Aggregate Boundary

≠

Database Schema
```

---

# Integration Boundary versus Table

Una tabla o colección física no define el Boundary.

---

# Integration Boundary versus Service

Una unidad técnica de servicio no redefine automáticamente el
Aggregate Boundary.

---

# Integration Boundary versus API

Una API puede exponer múltiples capacidades.

Esto no cambia:

```text
One IntegrationId

=

One Aggregate Boundary
```

---

# Integration Boundary versus Broker

Un broker puede transportar información sobre múltiples Integration.

Esto no crea un Consistency Boundary compartido.

---

# Batch Processing

Un proceso técnico puede procesar:

```text
INT-001

INT-002

INT-003
```

pero cada uno mantiene:

```text
own State

own Version

own Invariants

own Boundary
```

---

# Bulk Operation

Una operación externa sobre múltiples Integration no fusiona sus
Boundaries.

---

# No Mass Aggregate Mutation

La versión 1.0 no define una única modificación atómica de dominio que
convierta múltiples Integration en una sola unidad de consistencia.

---

# Performance

Una necesidad de rendimiento no autoriza ampliar o fusionar el
Consistency Boundary.

Debe mantenerse:

```text
Performance Optimization

≠

Consistency Boundary Expansion
```

---

# Caching

Cache permanece fuera del Boundary autoritativo.

---

# Replication

Replicación técnica no crea una segunda autoridad de dominio.

---

# Source of Truth

Integration es Source of Truth solamente para:

```text
its own Integration state
```

---

# External Source of Truth

Integration no es Source of Truth para:

```text
Organization

Citizen

Assembly

Audit

Notification

FIWARE

Municipal System

External Platform
```

---

# External System no es Source of Truth para Integration State

Debe mantenerse:

```text
External System

≠

Source of Truth for Integration State
```

---

# Read Model no es Source of Truth de Escritura

Debe mantenerse:

```text
Read Model

≠

Write Model Authority
```

---

# Integration Contract no es Source of Truth del Aggregate

Un contrato externo no sustituye el estado autoritativo de Integration.

---

# Domain Event no es Aggregate

Debe mantenerse:

```text
Domain Event

≠

Aggregate
```

Un evento representa un hecho del Boundary.

No reemplaza la Aggregate Root.

---

# Integration Event no es Aggregate

Debe mantenerse:

```text
Integration Event

≠

Integration Aggregate
```

---

# External Message no es Aggregate State

Debe mantenerse:

```text
External Message

≠

Integration State
```

---

# External Payload no Expande Boundary

Un External Payload completo no entra automáticamente al Aggregate.

Solamente información formalmente reconocida por el dominio puede
pertenecer a Integration.

---

# Data Minimization

El Consistency Boundary debe contener solamente información necesaria
para preservar las reglas del Aggregate.

---

# No Technical Metadata by Default

Metadata técnica no debe incorporarse automáticamente al Boundary.

---

# CorrelationId

CorrelationId puede relacionar hechos entre Boundaries.

Debe mantenerse:

```text
Same CorrelationId

≠

Same Consistency Boundary
```

---

# CausationId

CausationId puede representar causalidad.

No fusiona Boundaries.

---

# EventId

EventId identifica un Domain Event.

No identifica el Consistency Boundary.

---

# External Identifier

Un identificador externo no determina el Boundary.

IntegrationId sigue siendo la identidad del Aggregate.

---

# Lifecycle Consistency

Una transición válida debe quedar completamente reflejada dentro del
Boundary.

Ejemplo:

```text
Before

State = Active

Version = 4

After valid SuspendIntegration

State = Suspended

Version = 5
```

---

# Invalid Lifecycle Consistency

No debe existir una confirmación:

```text
State = Suspended

Version = 4
```

si la misma modificación válida requería:

```text
Version = 5
```

---

# Domain Event Consistency

Para la modificación anterior:

```text
IntegrationSuspended.AggregateVersion = 5
```

debe corresponder a:

```text
Integration.Version = 5
```

---

# Rejected Operation Consistency

Ante una operación rechazada:

```text
State unchanged

Version unchanged

UpdatedAt unchanged

No success Domain Event
```

---

# Permission Failure

Permission Failure ocurre fuera de la modificación del Aggregate.

No produce cambios parciales internos.

---

# Guard Failure

Guard Failure no modifica el Boundary.

---

# Invariant Failure

Invariant Failure no modifica el Boundary.

---

# ConcurrencyConflict

ConcurrencyConflict impide confirmar una modificación incompatible.

---

# ConcurrencyConflict no Expande Transaction

Resolver un conflicto no permite incluir otros Aggregates dentro de la
misma transacción.

---

# PersistenceFailure

Si Repository no confirma la persistencia:

```text
No new persisted Integration revision
```

debe considerarse confirmada.

---

# RepositoryUnavailable

RepositoryUnavailable no produce un nuevo State.

---

# Transaction Result

Una modificación válida debe terminar conceptualmente en uno de dos
resultados:

```text
Confirmed Aggregate Revision
```

o:

```text
Rejected / Not Confirmed
```

No debe existir una revisión parcialmente autoritativa.

---

# No External Compensation Rule

La versión 1.0 no define una compensación automática de Integration
por fallo de un sistema externo.

---

# No Automatic Rollback from External Failure

Debe mantenerse:

```text
External Failure

≠

Automatic Integration Rollback
```

---

# No Automatic Rollback from Audit Failure

Debe mantenerse:

```text
Audit Failure

≠

Integration Rollback
```

---

# No Automatic Rollback from Notification Failure

Debe mantenerse:

```text
Notification Failure

≠

Integration Rollback
```

---

# No Automatic Rollback from Read Model Failure

Debe mantenerse:

```text
Projection Failure

≠

Integration Rollback
```

---

# No Automatic Rollback from Publication Failure

Debe mantenerse:

```text
Publication Failure

≠

Integration Rollback
```

---

# External Coordination

Los procesos que involucren múltiples Boundaries deben coordinarse sin
convertirlos en una única unidad de consistencia.

Este documento no define el mecanismo técnico de coordinación.

---

# No Coordination Technology Decision

La necesidad de coordinación externa no determina:

```text
Broker

Saga

Process Manager

Outbox

Workflow Engine

Two-Phase Commit
```

como mecanismo obligatorio.

---

# No Outbox Requirement

La versión 1.0 no establece:

```text
Transactional Outbox
```

como requisito del Consistency Boundary.

---

# No Saga Requirement

La versión 1.0 no establece:

```text
Saga
```

como requisito del dominio.

---

# No Process Manager Requirement

La versión 1.0 no establece:

```text
Process Manager
```

como requisito del Aggregate.

---

# No Broker Requirement

El Consistency Boundary no depende de un broker concreto.

---

# No Protocol Requirement

El Consistency Boundary no depende de:

```text
HTTP

REST

MQTT

AMQP

GraphQL
```

---

# No Database Requirement

El Boundary no depende de:

```text
PostgreSQL

MongoDB

EventStoreDB

Redis
```

---

# No FIWARE Requirement

Integration puede interoperar con FIWARE.

Sin embargo, FIWARE no define el Boundary.

---

# No Municipal Architecture Requirement

La interacción con sistemas municipales no determina la estructura
interna del Aggregate.

---

# Security Boundary

Authentication y Authorization permanecen fuera del estado interno.

---

# Security no Expande Aggregate

La necesidad de autorización no autoriza incorporar:

```text
User

Role

Membership

Identity Provider

Access Token

Credential
```

dentro de Integration.

---

# Authorization Outcome

Una intención autorizada entra al comportamiento del Aggregate.

El Aggregate todavía debe proteger:

```text
State Machine

Guards

Invariants

Versioning
```

---

# Security Failure no Modifica Boundary

Un Authentication Failure o Authorization Failure no crea una nueva
revisión del Aggregate.

---

# Permission Change no es Aggregate Transaction

Cambiar una Permission no constituye una transacción de Integration.

---

# Audit Boundary

Audit conserva un Boundary independiente.

Conceptualmente:

```text
Integration Domain Event
    │
    ▼
eventual observation
    │
    ▼
Audit Boundary
```

sin compartir transacción.

---

# Notification Boundary

Notification conserva su Boundary independiente.

Conceptualmente:

```text
Integration Domain Fact
    │
    ▼
eventual coordination
    │
    ▼
Notification Boundary
```

---

# Read Model Boundary

El Read Side conserva sus propias estructuras derivadas.

No forma parte del Boundary de escritura.

---

# Integration Event Consumer Boundary

Un consumidor externo mantiene su propio Boundary.

Debe mantenerse:

```text
Producer Boundary

≠

Consumer Boundary
```

---

# Integration Event Producer Boundary

Un Integration Event no extiende el Consistency Boundary de
Integration hasta el consumidor.

---

# Consumer Failure

Un consumidor puede fallar después del commit de Integration.

Esto es compatible con consistencia eventual.

---

# Consumer Lag

Puede existir:

```text
Integration Version = 8

Consumer observed Version = 7
```

temporalmente.

Esto no crea una inconsistencia interna del Aggregate.

---

# Consumer State

El State del consumidor no sustituye el State de Integration.

---

# No Consumer Write Authority

Un consumidor no modifica directamente Integration mediante su propio
modelo interno.

---

# External Input Boundary

Una entrada externa debe cruzar una frontera conceptual antes de
convertirse en una intención válida.

Conceptualmente:

```text
External Input
    │
    ▼
External Contract
    │
    ▼
Valid Domain Intent
    │
    ▼
Integration Boundary
```

---

# External Input no Cruza Directamente

No debe ocurrir:

```text
External Payload
    │
    ▼
Direct State Mutation
```

---

# External State Mapping

Un estado externo solamente puede influir en comportamiento de dominio
mediante una regla explícitamente definida.

No se incorpora automáticamente.

---

# Contract Translation

Cualquier traducción necesaria entre modelos externos y AURA debe
preservar el Boundary.

Este documento no define el mecanismo técnico de traducción.

---

# External Model Separation

Debe mantenerse:

```text
External Model

≠

Integration Internal Model
```

---

# Boundary and Data Minimization

Incluir información externa dentro de Integration requiere una razón
explícita de dominio.

La disponibilidad técnica de información no constituye razón
suficiente.

---

# Boundary and Privacy

El Boundary no debe ampliarse con datos personales, credenciales o
metadata externa innecesaria solamente porque estén disponibles.

---

# Boundary and Secrets

Debe mantenerse:

```text
Secrets

∉

Integration Consistency Boundary
```

---

# Boundary and Infrastructure Configuration

Configuraciones técnicas de:

- endpoints;
- brokers;
- credentials;
- retries;
- connection pools;

no pertenecen automáticamente al Aggregate.

---

# Boundary and Technical Retry

Retry técnico ocurre fuera del Boundary del dominio.

---

# Boundary and Queue

Queue state ocurre fuera del Boundary.

---

# Boundary and Outbox

Outbox state, cuando exista técnicamente, ocurre fuera del Aggregate.

---

# Boundary and Monitoring

Monitoring ocurre fuera del Boundary.

---

# Boundary and Logs

Logs no forman parte del Consistency Boundary.

---

# Boundary and Metrics

Metrics no forman parte del Consistency Boundary.

---

# Boundary and Tracing Infrastructure

La infraestructura de tracing permanece fuera del Aggregate.

CorrelationId y CausationId pueden formar parte de contratos cuando
corresponda sin incorporar la infraestructura de tracing.

---

# Boundary Stability

El Consistency Boundary no debe ampliarse por conveniencia.

Toda ampliación futura requiere una necesidad explícita de consistencia
del dominio.

---

# Regla para Expandir el Boundary

Un concepto solamente puede incorporarse dentro de Integration cuando
necesite participar en las mismas Invariants y en la misma unidad de
consistencia.

---

# No Expansion by Query Convenience

Una necesidad de consulta no amplía el Boundary.

---

# No Expansion by Persistence Convenience

Una necesidad de persistencia no amplía el Boundary.

---

# No Expansion by API Convenience

Una necesidad de API no amplía el Boundary.

---

# No Expansion by External System Model

Un sistema externo con una estructura compleja no amplía el Boundary.

---

# No Expansion by Performance

Performance no amplía el Boundary.

---

# No Expansion by Security

Security no amplía el Boundary con Roles, Users o Credentials.

---

# No Expansion by Integration Technology

FIWARE, NGSI-LD, brokers o APIs no expanden el Aggregate.

---

# Boundary Evolution

Cualquier cambio futuro del Boundary debe revisar:

```text
Identity

Ownership

Lifecycle

State Machine

Commands

Domain Events

Invariants

Permissions

Repository Contract

Versioning

Read Models

Integration Events

Security

Performance

Test Scenarios
```

---

# Impacto de una Evolución

Una modificación del Consistency Boundary debe revisar cuando
corresponda:

```text
DOMAIN-013-Aggregate.md

DOMAIN-013A-Lifecycle.md

DOMAIN-013B-State-Machine.md

DOMAIN-013C-Commands.md

DOMAIN-013D-Domain-Events.md

DOMAIN-013E-Invariants.md

DOMAIN-013F-Permissions.md

DOMAIN-013G-Repository-Contract.md

DOMAIN-013H-Examples.md

DOMAIN-013I-Versioning.md

DOMAIN-013K-Integration-Events.md

DOMAIN-013L-Read-Model.md

DOMAIN-013M-Test-Scenarios.md

DOMAIN-013N-Performance-Rules.md

DOMAIN-013O-Security-Model.md

DOMAIN-013P-Extension-Points.md
```

---

# Regla de No Inferencia

Debe mantenerse:

```text
External Relationship

≠

Shared Consistency Boundary
```

y:

```text
Technical Dependency

≠

Aggregate Membership
```

y:

```text
Integration Contract

≠

Distributed Aggregate
```

y:

```text
Cross-System Communication

≠

Cross-System Transaction
```

---

# Reglas Fundamentales

El Consistency Boundary de Integration debe cumplir:

1. Un IntegrationId representa un Aggregate Boundary.
2. Cada Integration mantiene un Boundary independiente.
3. No existe Global Integration Aggregate.
4. Integration es la única Aggregate Root del Boundary.
5. Internal Entities solamente pertenecen al Boundary si son
   formalmente definidas.
6. Value Objects solamente pertenecen al Boundary si son formalmente
   definidos.
7. Otros Aggregates permanecen fuera del Boundary.
8. Sistemas externos permanecen fuera del Boundary.
9. FIWARE permanece fuera del Boundary.
10. Sistemas municipales permanecen fuera del Boundary.
11. Smart City Platforms permanecen fuera del Boundary.
12. Read Models permanecen fuera del Write Boundary.
13. Authentication permanece fuera del Aggregate.
14. Authorization permanece fuera del Aggregate State.
15. Infrastructure permanece fuera del Aggregate.
16. Referencias externas no transfieren ownership.
17. Referencias externas no expanden el Boundary.
18. No se embeben otros Aggregate Roots.
19. Source Aggregate permanece fuera de Integration.
20. Source Domain Event no transfiere ownership.
21. Consistencia interna es inmediata.
22. Consistencia externa es eventual.
23. Integration Transaction modifica una Integration.
24. Integration Transaction no es otra Aggregate Transaction.
25. Source Aggregate Commit no es Integration Commit.
26. Integration Commit no es External System Commit.
27. Integration Commit no es FIWARE Commit.
28. Integration Commit no es Municipal System Commit.
29. No existe Distributed Aggregate entre Integration y sistemas
    externos.
30. Distributed Transaction no es requisito del dominio.
31. Two-Phase Commit no es requisito del dominio.
32. La modificación interna debe ser atómica.
33. No se permite Partial Aggregate Commit.
34. CreateIntegration solamente crea Integration.
35. ActivateIntegration solamente modifica Integration.
36. SuspendIntegration solamente modifica Integration.
37. ReactivateIntegration solamente modifica Integration.
38. ArchiveIntegration solamente modifica Integration.
39. Los States pertenecen únicamente a Integration.
40. External State no es Integration State.
41. Source Aggregate State no es Integration State.
42. FIWARE State no es Integration State.
43. Municipal State no es Integration State.
44. Technical State no es Integration State.
45. External Failure no produce transición automática.
46. External Recovery no produce transición automática.
47. Domain Events expresan hechos del Boundary de Integration.
48. Domain Event no confirma cambios en otros Boundaries.
49. Otros consumidores no adquieren ownership del Domain Event.
50. Domain Event no es Integration Event.
51. Integration Event no constituye Shared Aggregate State.
52. Domain Event no exige Integration Event obligatorio.
53. Publicación externa ocurre fuera de la modificación interna.
54. Publication Failure no revierte automáticamente el Aggregate.
55. Retry técnico permanece fuera del Boundary.
56. Redelivery técnico no crea automáticamente nueva modificación.
57. IntegrationRepository persiste una Integration como unidad.
58. Repository no expande el Boundary.
59. Repository no ejecuta comportamiento cross-boundary.
60. Repository.delete() no es Lifecycle Transition.
61. Read Model no pertenece al Write Boundary.
62. Projection Lag no altera consistencia interna.
63. Projection Failure no revierte el Aggregate.
64. Query concerns permanecen fuera del Write Boundary.
65. CQRS no altera el Consistency Boundary.
66. Event Sourcing no altera el Consistency Boundary.
67. Rehydration reconstruye una Integration.
68. Replay no fusiona Boundaries.
69. Version pertenece a una única Integration.
70. No existe Shared Aggregate Version.
71. ExpectedVersion se evalúa dentro de la misma Integration.
72. Different IntegrationId poseen concurrencia independiente.
73. No se define Global Lock de dominio.
74. Permissions no forman parte del Aggregate State.
75. Credentials permanecen fuera del Boundary.
76. Authorization Policy Change no modifica Integration por sí mismo.
77. ActorId no embebe Citizen.
78. Audit permanece fuera del Boundary.
79. Notification permanece fuera del Boundary.
80. Audit Failure no revierte Integration.
81. Notification Failure no revierte Integration.
82. Consumer Failure no revierte Integration.
83. Integration Contract no es Aggregate Boundary.
84. Network Boundary no es Aggregate Boundary.
85. Deployment Boundary no es Aggregate Boundary.
86. Database Schema no es Aggregate Boundary.
87. Broker no crea Shared Consistency Boundary.
88. Batch Processing no fusiona Boundaries.
89. Performance no permite ampliar el Boundary.
90. Cache no constituye autoridad del Aggregate.
91. External System no es Source of Truth para Integration State.
92. Read Model no es Source of Truth de escritura.
93. External Message no es Aggregate State.
94. External Payload no se incorpora automáticamente al Boundary.
95. Same CorrelationId no significa Same Boundary.
96. CausationId no fusiona Boundaries.
97. No se define compensación automática por fallo externo.
98. No se impone Outbox, Saga, Process Manager ni 2PC.
99. Toda expansión del Boundary requiere una necesidad explícita de
    consistencia del dominio.
100. Toda evolución del Boundary debe preservar el patrón consolidado
     del Aggregate Integration.

---

# Restricciones

No está permitido:

- fusionar múltiples Integration en un solo Aggregate;
- utilizar un Global Integration Aggregate;
- embebir Organization dentro de Integration;
- embebir Citizen dentro de Integration;
- embebir Membership dentro de Integration;
- embebir Role dentro de Integration;
- embebir Territory dentro de Integration;
- embebir Assembly dentro de Integration;
- embebir Proposal dentro de Integration;
- embebir Participation dentro de Integration;
- embebir Voting dentro de Integration;
- embebir Document dentro de Integration;
- embebir Notification dentro de Integration;
- embebir Audit dentro de Integration;
- embebir sistemas externos completos;
- incorporar FIWARE dentro del Aggregate;
- incorporar un sistema municipal dentro del Aggregate;
- utilizar una referencia externa como transferencia de ownership;
- modificar otro Aggregate dentro de Integration Transaction;
- exigir External System Commit dentro del mismo Boundary;
- exigir FIWARE Commit dentro del mismo Boundary;
- exigir Municipal System Commit dentro del mismo Boundary;
- convertir Integration en Distributed Aggregate;
- imponer Two-Phase Commit como regla del dominio;
- confirmar una modificación parcial del Aggregate;
- modificar State sin coherencia de Version;
- convertir External State en Integration State automáticamente;
- convertir Technical State en Integration State;
- suspender automáticamente por fallo externo;
- reactivar automáticamente por recuperación externa;
- utilizar Domain Event para afirmar cambios en otros Aggregates;
- convertir Domain Event en Integration Event automáticamente;
- incluir publicación externa dentro de la autoridad del Aggregate;
- revertir automáticamente el Aggregate por Publication Failure;
- incrementar Version por Retry técnico;
- permitir que Repository expanda el Boundary;
- utilizar Repository como mecanismo de integración externa;
- utilizar Read Model como parte autoritativa del Write Boundary;
- revertir el Aggregate por Projection Failure;
- compartir Version entre Aggregates;
- comparar ExpectedVersion con Version de otro Aggregate;
- utilizar una Authorization Policy como Aggregate State;
- almacenar credenciales dentro del Boundary;
- interpretar ActorId como Citizen embebido;
- revertir Integration por Audit Failure;
- revertir Integration por Notification Failure;
- revertir Integration por Consumer Failure;
- utilizar Integration Contract como Aggregate State;
- utilizar Network Boundary como Aggregate Boundary;
- utilizar Deployment Unit como Aggregate Boundary;
- utilizar Database Schema como Aggregate Boundary;
- utilizar Broker como Aggregate Boundary;
- fusionar Boundaries mediante Batch Processing;
- ampliar Boundary por performance;
- ampliar Boundary por conveniencia de persistencia;
- ampliar Boundary por conveniencia de API;
- ampliar Boundary por modelo externo;
- ampliar Boundary por seguridad técnica;
- utilizar External Payload completo como estado del Aggregate por
  defecto;
- imponer Outbox;
- imponer Saga;
- imponer Process Manager;
- imponer broker;
- imponer protocolo;
- imponer base de datos;
- imponer FIWARE como tecnología interna;
- introducir un nuevo miembro del Boundary sin necesidad explícita de
  consistencia del dominio.

---

# Compatibilidad Arquitectónica

El Consistency Boundary de Integration es compatible con:

- Domain-Driven Design;
- Aggregate Pattern;
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

Estas compatibilidades no imponen:

- Distributed Transaction;
- Two-Phase Commit;
- Transactional Outbox;
- Saga;
- Process Manager;
- broker;
- protocolo;
- base de datos;
- framework;
- FIWARE;
- NGSI-LD;
- plataforma municipal.

---

# Definición de Éxito

El Consistency Boundary del Aggregate **Integration** establece una
frontera clara entre el estado que debe permanecer inmediatamente
consistente dentro de AURA y toda colaboración externa que debe
preservar independencia entre contextos.

El modelo central queda expresado como:

```text
             Integration
                  │
                  │
    ┌─────────────┴─────────────┐
    │                           │
    ▼                           ▼
Internal                    External
Consistency                 Coordination
    │                           │
    ▼                           ▼
Immediate                   Eventual
    │                           │
    ▼                           ▼
IntegrationId              Other Aggregates
State                      External Systems
Version                    FIWARE
Invariants                 Municipal Systems
Domain Behavior            Read Models
```

y:

```text
One IntegrationId

=

One Consistency Boundary
```

El modelo garantiza que:

- cada Integration mantenga identidad propia;
- cada Integration mantenga su propio State;
- cada Integration mantenga su propia Version;
- cada Integration proteja sus propias Invariants;
- modificaciones internas sean atómicas;
- otros Aggregates permanezcan fuera del Boundary;
- sistemas externos permanezcan fuera del Boundary;
- FIWARE permanezca fuera del Boundary;
- sistemas municipales permanezcan fuera del Boundary;
- referencias no transfieran ownership;
- Source Aggregate y Integration mantengan transacciones separadas;
- Integration Commit y External System Commit permanezcan separados;
- consistencia interna sea inmediata;
- consistencia externa sea eventual;
- Domain Events confirmen solamente hechos de Integration;
- Integration Events no fusionen Boundaries;
- publicación externa permanezca separada de la modificación interna;
- fallos externos no reviertan automáticamente el Aggregate;
- Retry técnico permanezca fuera del Boundary;
- Repository preserve una única unidad de consistencia;
- Read Models permanezcan fuera del Write Boundary;
- Version y concurrencia se evalúen por IntegrationId;
- Authentication, Authorization y Credentials permanezcan fuera del
  Aggregate;
- Audit y Notification mantengan Boundaries independientes;
- contratos externos no sustituyan el Aggregate;
- Network, Deployment y Persistence Boundaries no redefinan el
  Aggregate Boundary;
- Batch Processing no fusione Aggregates;
- performance no permita violar el Boundary;
- ninguna coordinación técnica específica sea impuesta por este
  documento;
- cualquier ampliación futura del Boundary requiera una necesidad
  explícita de consistencia del dominio.

De esta forma, `DOMAIN-013J-Consistency-Boundary.md` establece
formalmente el Consistency Boundary oficial del Aggregate
**Integration** conforme al patrón consolidado de AURA Core.