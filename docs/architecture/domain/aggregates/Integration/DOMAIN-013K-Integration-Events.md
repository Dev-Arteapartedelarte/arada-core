# DOMAIN-013K — Integration Events

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
- DOMAIN-013J-Consistency-Boundary.md
- DOMAIN-013L-Read-Model.md
- DOMAIN-013M-Test-Scenarios.md
- DOMAIN-013N-Performance-Rules.md
- DOMAIN-013O-Security-Model.md
- DOMAIN-013P-Extension-Points.md

---

# Objetivo

Este documento define formalmente las reglas conceptuales de
**Integration Events** asociadas al Aggregate **Integration**.

Los Integration Events permiten representar hechos destinados a cruzar
un Bounded Context o una frontera de sistema cuando existe un contrato
explícito que requiere interoperabilidad.

Este documento no establece que todo Domain Event de Integration deba
transformarse en un Integration Event.

---

# Principio Fundamental

Debe mantenerse:

```text
Domain Event

≠

Integration Event
```

y:

```text
Domain Event

≠

Mandatory External Publication
```

---

# Definición

Un Integration Event representa un hecho expresado mediante un contrato
de interoperabilidad destinado a ser comprendido fuera del Boundary
interno que originó dicho hecho.

Conceptualmente:

```text
Confirmed Domain Fact
    │
    ▼
Explicit Integration Contract
    │
    ▼
Integration Event
    │
    ▼
External Consumer
```

---

# Propósito

Los Integration Events permiten:

- comunicar hechos entre Bounded Contexts;
- comunicar hechos hacia sistemas externos;
- preservar desacoplamiento entre modelos;
- proteger el Domain Model de representaciones externas;
- mantener contratos explícitos;
- permitir consistencia eventual;
- preservar trazabilidad cuando corresponda;
- permitir evolución independiente de productores y consumidores.

---

# Integration Event no es Domain Event

Los Domain Events pertenecen al modelo interno del Aggregate.

Los Integration Events pertenecen al contrato de interoperabilidad
correspondiente.

Debe mantenerse:

```text
Domain Event Ownership

≠

Integration Event Contract
```

---

# Domain Event

Los Domain Events oficiales de Integration versión 1.0 son:

```text
IntegrationCreated

IntegrationActivated

IntegrationSuspended

IntegrationReactivated

IntegrationArchived
```

Estos eventos representan hechos internos confirmados.

---

# No Publicación Automática

Ninguno de los Domain Events oficiales implica automáticamente la
existencia de un Integration Event.

Debe mantenerse:

```text
IntegrationCreated

≠

Mandatory Integration Event
```

```text
IntegrationActivated

≠

Mandatory Integration Event
```

```text
IntegrationSuspended

≠

Mandatory Integration Event
```

```text
IntegrationReactivated

≠

Mandatory Integration Event
```

```text
IntegrationArchived

≠

Mandatory Integration Event
```

---

# Contrato Explícito

Un Integration Event solamente debe existir cuando un contrato explícito
determine que un hecho necesita cruzar una frontera.

Debe mantenerse:

```text
No Explicit Integration Contract

=

No Integration Event Requirement
```

---

# Contrato no se Infiere

La existencia de:

- otro Bounded Context;
- un sistema externo;
- FIWARE;
- una plataforma municipal;
- una API;
- un broker;
- una infraestructura de mensajería;

no crea automáticamente un Integration Event.

---

# Eventos Oficiales versión 1.0

La versión 1.0 no establece nombres concretos obligatorios de
Integration Events para el Aggregate Integration.

Debe mantenerse:

```text
Official Concrete Integration Events

=

Defined only by explicit external contracts
```

---

# No Lista Global Obligatoria

Este documento no define una lista universal de Integration Events
aplicable a todos los consumidores.

Un contrato puede requerir determinados hechos.

Otro contrato puede no requerirlos.

---

# Consumer-Specific Contracts

Diferentes consumidores pueden requerir diferentes contratos de
interoperabilidad.

Debe mantenerse:

```text
Consumer A Contract

≠

Consumer B Contract
```

sin que esto cambie el Domain Event original.

---

# Un Domain Event Puede no Cruzar Fronteras

Puede existir:

```text
IntegrationActivated
```

como hecho confirmado del dominio sin que exista necesidad de
comunicación externa.

En ese caso:

```text
No Integration Event is required
```

---

# Un Domain Event Puede Alimentar un Contrato

Cuando exista un contrato explícito:

```text
Domain Event
    │
    ▼
Contractual Transformation
    │
    ▼
Integration Event
```

La transformación contractual no modifica el hecho original.

---

# No Conversión Uno a Uno Obligatoria

Debe mantenerse:

```text
One Domain Event

≠

Exactly One Integration Event
```

y:

```text
One Integration Event

≠

Automatically One Domain Event
```

salvo definición explícita del contrato correspondiente.

---

# No Cardinalidad Inferida

Este documento no define cardinalidades obligatorias entre:

```text
Domain Event

Integration Event

External Message

External Consumer
```

---

# Semántica

Un Integration Event debe expresar un hecho comprensible para el
consumidor conforme al contrato acordado.

No debe exponer accidentalmente detalles internos del Aggregate.

---

# Protección del Domain Model

Debe mantenerse:

```text
Internal Domain Model

≠

External Contract Model
```

El Integration Event representa únicamente la información necesaria
para la interoperabilidad.

---

# Payload

El Payload de un Integration Event debe contener solamente información
necesaria para el contrato.

Debe mantenerse:

```text
Integration Event Payload

≠

Full Integration Aggregate Snapshot
```

---

# Data Minimization

Debe aplicarse:

```text
Minimum Necessary Contract Data
```

---

# Aggregate Completo no se Publica

No debe exponerse automáticamente:

```text
Integration {
    all internal state
    all internal metadata
    all historical information
}
```

como Payload de un Integration Event.

---

# Domain Event Payload no se Copia Automáticamente

Debe mantenerse:

```text
Domain Event Payload

≠

Automatic Integration Event Payload
```

---

# External Payload no se Copia Automáticamente

Debe mantenerse:

```text
External Payload

≠

Automatic Integration Event Payload
```

---

# Contrato de Datos

La estructura concreta de un Integration Event debe ser definida por
el contrato de interoperabilidad correspondiente.

Este documento no establece un schema universal.

---

# Identidad del Integration Event

Cuando un contrato requiera identificar un Integration Event, la
identidad del mensaje o evento debe ser conceptualmente distinta de:

```text
IntegrationId

DomainEvent.EventId
```

salvo que el contrato explícito determine una relación concreta.

---

# IntegrationId

IntegrationId puede incluirse en un Integration Event cuando sea
necesario para identificar el Aggregate de origen.

Su inclusión no transfiere ownership al consumidor.

---

# Source Aggregate

Cuando corresponda, el contrato puede preservar referencia al Aggregate
que originó el hecho.

Debe mantenerse:

```text
Source Aggregate Reference

≠

Embedded Aggregate
```

---

# Source Domain Event

Cuando un Integration Event se deriva de un Domain Event, la referencia
al hecho fuente puede preservarse cuando el contrato lo requiera.

Esto no convierte el Integration Event en el Domain Event original.

---

# SourceEventId

Si un contrato incluye:

```text
SourceEventId
```

dicho identificador referencia el Domain Event fuente.

Debe mantenerse:

```text
SourceEventId

≠

IntegrationEventId
```

salvo una definición contractual explícita que establezca otra
representación.

---

# SourceAggregateVersion

Cuando el contrato requiera preservar la Version del Aggregate fuente:

```text
SourceAggregateVersion
```

puede representar:

```text
Integration.Version
```

correspondiente al hecho confirmado.

---

# SourceAggregateVersion no es Contract Version

Debe mantenerse:

```text
SourceAggregateVersion

≠

Integration Event Contract Version
```

---

# Contract Version

Un Integration Event puede pertenecer a una versión de contrato.

Debe mantenerse:

```text
Integration Event Contract Version

≠

Integration.Version
```

---

# Domain Event AggregateVersion

Debe mantenerse:

```text
DomainEvent.AggregateVersion

≠

Integration Event Contract Version
```

---

# OccurredAt

Cuando un Integration Event represente un hecho interno ya ocurrido, el
contrato debe preservar correctamente la semántica temporal del hecho.

Debe mantenerse:

```text
Fact OccurredAt

≠

Publication Time
```

---

# Publication Time

El momento técnico en que un Integration Event es publicado no
sustituye el momento del hecho de dominio que representa.

---

# Delivery Time

Debe mantenerse:

```text
Delivery Time

≠

Domain Fact OccurredAt
```

---

# CorrelationId

CorrelationId puede formar parte de un Integration Event cuando el
contrato requiera preservar correlación.

No es obligatorio universalmente.

---

# CorrelationId no Fusiona Boundaries

Debe mantenerse:

```text
Same CorrelationId

≠

Same Consistency Boundary
```

---

# CausationId

CausationId puede formar parte del contrato cuando exista una relación
causal que deba preservarse.

No es obligatorio universalmente.

---

# CausationId no Concede Autoridad

Debe mantenerse:

```text
CausationId

≠

Mutation Authority
```

---

# ActorId

ActorId puede incluirse solamente cuando forme parte necesaria del
contrato.

No debe asumirse como obligatorio.

---

# ActorId no es Authorization

Debe mantenerse:

```text
ActorId

≠

Permission

≠

Authorization
```

---

# Credenciales

Los Integration Events no deben contener:

```text
Password

AccessToken

RefreshToken

ApiKey

PrivateKey

ClientSecret

Secret
```

como información del contrato.

---

# Secrets

Debe mantenerse:

```text
Secret

∉

Integration Event Payload
```

---

# Authentication

Un Integration Event no transporta Authentication como parte del
Domain Model.

---

# Authorization

Un Integration Event no concede por sí mismo una Permission de dominio.

Debe mantenerse:

```text
Integration Event

≠

Authorization Grant
```

---

# Event Entrante

Un Integration Event recibido desde otro contexto o sistema no
modifica directamente Integration.

Debe mantenerse:

```text
Incoming Integration Event

≠

Direct Aggregate Mutation
```

---

# No setState() desde Integration Event

Nunca debe interpretarse:

```text
Incoming Integration Event
    │
    ▼
setState()
```

como comportamiento válido.

---

# Interpretación Contractual

Un Integration Event entrante debe ser interpretado conforme al
contrato correspondiente antes de convertirse, cuando aplique, en una
intención válida del dominio.

Conceptualmente:

```text
Incoming Integration Event
    │
    ▼
Contract Interpretation
    │
    ▼
Valid Domain Intent
    │
    ▼
Integration
```

---

# Integration Event no es Command

Debe mantenerse:

```text
Integration Event

≠

Command
```

---

# Integration Event no es Permission

Debe mantenerse:

```text
Integration Event

≠

Permission
```

---

# Integration Event no es State

Debe mantenerse:

```text
Integration Event

≠

Integration State
```

---

# Integration Event no es Aggregate

Debe mantenerse:

```text
Integration Event

≠

Integration Aggregate
```

---

# Integration Event no es Repository Entity

La existencia de un Integration Event no crea una nueva Internal Entity
del Aggregate.

---

# Consistency Boundary

Los Integration Events cruzan límites de interoperabilidad sin ampliar
el Consistency Boundary del Aggregate.

Debe mantenerse:

```text
Integration Event Publication

≠

Consistency Boundary Expansion
```

---

# Producer Boundary

El productor mantiene su propio Boundary.

---

# Consumer Boundary

El consumidor mantiene su propio Boundary.

---

# Producer y Consumer no Comparten Aggregate

Debe mantenerse:

```text
Producer Boundary

≠

Consumer Boundary
```

---

# Consistencia Eventual

La propagación mediante Integration Events opera conceptualmente bajo:

```text
Eventual Consistency
```

entre Boundaries.

---

# Domain Commit

Un hecho del Aggregate debe estar confirmado antes de ser tratado como
hecho disponible para integración.

---

# External Delivery no Confirma Domain Fact

El éxito de entrega externa no determina si el hecho interno ocurrió.

Debe mantenerse:

```text
External Delivery Success

≠

Domain Fact Confirmation
```

---

# Publication Failure

Un fallo posterior de publicación no revierte automáticamente:

```text
Integration State

Integration.Version

Domain Event
```

ya confirmados.

---

# Delivery Failure

Del mismo modo:

```text
Delivery Failure

≠

Integration State Transition
```

---

# Retry

Un retry técnico de publicación no constituye un nuevo Domain Fact.

Debe mantenerse:

```text
Retry

≠

New Domain Event
```

---

# Retry no Incrementa Version

Debe mantenerse:

```text
Technical Retry

≠

Integration.Version Increment
```

---

# Redelivery

Una retransmisión del mismo Integration Event no representa
automáticamente un nuevo hecho.

---

# Duplicación Técnica

Debe mantenerse:

```text
Technical Duplicate

≠

New Domain Fact
```

---

# Idempotencia

La estrategia concreta de idempotencia para publicación o consumo no se
define en este documento.

---

# Deduplicación

La estrategia concreta de deduplicación tampoco se define como regla
interna del Aggregate.

---

# Exactly Once

La versión 1.0 no establece:

```text
Exactly Once Delivery
```

como garantía del dominio.

---

# At Least Once

La versión 1.0 tampoco establece:

```text
At Least Once
```

como requisito contractual universal.

---

# At Most Once

La versión 1.0 tampoco establece:

```text
At Most Once
```

como requisito contractual universal.

---

# Orden

Este documento no establece un orden global obligatorio entre
Integration Events.

---

# Orden por Aggregate

Cuando un contrato necesite preservar orden relativo de hechos de una
misma Integration, puede utilizar información contractual adecuada.

La estrategia concreta no se define aquí.

---

# AggregateVersion y Orden

Cuando se incluya:

```text
SourceAggregateVersion
```

puede preservar el orden lógico del Aggregate fuente.

Esto no crea orden global entre diferentes IntegrationId.

---

# No Global Ordering

Debe mantenerse:

```text
Per-Aggregate Logical Order

≠

Global Integration Event Order
```

---

# Replay

Replay de Domain Events no debe publicar automáticamente nuevos
Integration Events como si fueran nuevos hechos.

Debe mantenerse:

```text
Replay

≠

New External Fact
```

---

# Rehydration

Rehydration del Aggregate no produce nuevos Integration Events.

---

# Projection Rebuild

Reconstruir un Read Model tampoco produce nuevos Integration Events por
definición.

---

# Event Sourcing

Event Sourcing es compatible con Integration Events.

Debe mantenerse:

```text
Event Sourcing Compatible

≠

Integration Events Required
```

---

# Aggregate Event Stream

Debe mantenerse:

```text
Aggregate Event Stream

≠

Integration Event Stream
```

---

# Integration Event Stream

Una eventual secuencia de Integration Events pertenece a contratos de
interoperabilidad y no constituye automáticamente la fuente de verdad
del Aggregate.

---

# CQRS

CQRS es compatible con la producción y consumo de Integration Events.

No cambia la diferencia entre:

```text
Write Model

Domain Event

Integration Event

Read Model
```

---

# Read Model

Un Integration Event puede alimentar estructuras externas o Read
Models cuando exista un contrato que así lo determine.

No adquiere autoridad de escritura sobre Integration.

---

# Read Model no Produce Integration Events por Defecto

Debe mantenerse:

```text
Read Model Change

≠

Integration Event
```

salvo contrato explícito independiente.

---

# Repository

IntegrationRepository no es responsable conceptualmente de definir
Integration Events.

---

# Repository no Decide Publicación

Debe mantenerse:

```text
Repository

≠

Integration Event Contract Authority
```

---

# save() no es Integration Event

Debe mantenerse:

```text
save()

≠

Integration Event
```

---

# Repository.delete() no Produce Integration Event

La operación:

```text
Repository.delete()
```

no constituye por sí misma un hecho de interoperabilidad.

---

# Persistence Failure

Un PersistenceFailure no produce automáticamente un Integration Event.

---

# Database Event

Hechos como:

```text
RowInserted

DocumentUpdated

RecordDeleted
```

no son Integration Events del dominio por definición.

---

# Infrastructure Event

Eventos de Infrastructure tampoco se convierten automáticamente en
Integration Events.

---

# Broker Event

Un evento técnico como:

```text
BrokerConnected

BrokerDisconnected

MessageAcknowledged

MessageRetried
```

no constituye un Integration Event del dominio.

---

# Monitoring Event

Un hecho de Monitoring no constituye automáticamente un Integration
Event.

---

# Health Event

Estados:

```text
Healthy

Unhealthy

Degraded
```

no se publican como Integration Events del Aggregate por definición de
versión 1.0.

---

# FIWARE

Integration Events pueden participar en contratos que interoperan con
FIWARE.

Sin embargo:

```text
Integration Event

≠

FIWARE Entity
```

---

# NGSI-LD

La versión 1.0 no establece que todo Integration Event deba utilizar
NGSI-LD.

Debe mantenerse:

```text
Integration Event Semantics

≠

NGSI-LD Requirement
```

---

# Context Broker

La existencia de un Context Broker no redefine el significado de un
Integration Event.

---

# FIWARE Contract

Si un contrato concreto con FIWARE fuese definido, dicho contrato debe
preservar:

- semántica de AURA;
- separación de modelos;
- Data Minimization;
- Consistency Boundary;
- independencia del Domain Event interno.

La estructura concreta no se define en este documento.

---

# Sistemas Municipales

Integration Events pueden participar en contratos con sistemas
municipales.

Esto no implica que el modelo municipal se convierta en el modelo de
AURA.

---

# Municipal Contract

Debe mantenerse:

```text
Municipal Data Model

≠

Integration Domain Model
```

---

# Smart City

Los Integration Events pueden utilizarse para interoperabilidad Smart
City cuando exista un contrato explícito.

Ninguna tecnología Smart City concreta forma parte obligatoria de este
documento.

---

# Protocol Independence

La semántica de un Integration Event es independiente de:

```text
HTTP

REST

GraphQL

MQTT

AMQP

WebSocket
```

---

# Broker Independence

La semántica tampoco depende de:

```text
Kafka

RabbitMQ

NATS
```

---

# Serialization Independence

Un Integration Event puede representarse técnicamente mediante un
formato compatible con el contrato.

Debe mantenerse:

```text
Serialization Format

≠

Integration Event Meaning
```

---

# JSON

Este documento no establece JSON como formato obligatorio.

---

# XML

Este documento tampoco establece XML como formato obligatorio.

---

# Schema

Un contrato puede definir un schema.

El schema debe preservar la semántica del Integration Event.

---

# Schema Evolution

La evolución del schema contractual no modifica automáticamente:

```text
Integration.Version
```

---

# Contract Evolution

La evolución de un Integration Event Contract debe preservarse
independientemente del Lifecycle interno del Aggregate.

---

# Contract Version no es Aggregate State

Debe mantenerse:

```text
Integration Event Contract Version

≠

Draft

Active

Suspended

Archived
```

---

# Compatibility

La compatibilidad entre versiones contractuales debe resolverse en el
contrato correspondiente.

Este documento no define una política específica de backward o forward
compatibility.

---

# No Schema Registry Requirement

La versión 1.0 no establece un Schema Registry obligatorio.

---

# No Broker Requirement

La versión 1.0 no establece un broker obligatorio.

---

# No Outbox Requirement

La versión 1.0 no establece:

```text
Transactional Outbox
```

como mecanismo obligatorio.

---

# No Inbox Requirement

La versión 1.0 no establece:

```text
Inbox Pattern
```

como mecanismo obligatorio.

---

# No Dead Letter Requirement

La versión 1.0 no establece:

```text
Dead Letter Queue
```

como requisito del dominio.

---

# No Retry Policy de Dominio

La versión 1.0 no define:

- retry count;
- retry delay;
- exponential backoff;
- retry schedule.

---

# No Delivery Infrastructure Decision

Este documento no decide:

- push;
- pull;
- webhook;
- polling;
- message broker;
- direct request;
- streaming.

---

# No Transport Decision

El Integration Event representa semántica contractual.

No selecciona mecanismo de transporte.

---

# No Middleware Decision

La existencia de Integration Events no obliga a incorporar middleware
específico.

---

# No Event Bus Requirement

La versión 1.0 no establece un Event Bus concreto ni obligatorio.

---

# No Message Broker Requirement

Debe mantenerse:

```text
Integration Event

≠

Broker Requirement
```

---

# No Topic Definition

Este documento no define:

- topic names;
- queue names;
- routing keys;
- exchange names;
- channels.

---

# No Endpoint Definition

Este documento no define endpoints para publicación o consumo.

---

# No Delivery Semantics Definition

La semántica de:

```text
retry

acknowledgement

redelivery

timeout

dead-letter
```

pertenece a contratos o decisiones técnicas posteriores cuando sean
necesarias.

---

# Inbound versus Outbound

Los Integration Events pueden conceptualmente participar en:

```text
Outbound Interoperability

Inbound Interoperability
```

según el contrato correspondiente.

Este documento no define contratos concretos de ambos sentidos.

---

# Outbound

Un Integration Event outbound representa información que cruza desde
AURA hacia otro Boundary.

---

# Inbound

Un Integration Event inbound representa información proveniente desde
otro Boundary que debe ser interpretada contractualmente.

---

# Inbound no es Domain Fact Automático

Debe mantenerse:

```text
Incoming Integration Event

≠

Confirmed AURA Domain Fact
```

---

# Inbound no es Command Automático

Debe mantenerse:

```text
Incoming Integration Event

≠

Automatic Command
```

---

# Outbound no Modifica Consumer

Publicar un Integration Event no confirma que el consumidor haya
modificado su propio estado.

---

# Consumer Acknowledgement

Un acknowledgement del consumidor no se convierte automáticamente en
un Domain Event de Integration.

---

# Consumer Failure

Un fallo del consumidor no suspende automáticamente Integration.

---

# Consumer Recovery

La recuperación del consumidor no reactiva automáticamente Integration.

---

# Integration Lifecycle

Los estados:

```text
Draft

Active

Suspended

Archived
```

pertenecen al Aggregate.

Los Integration Events no forman parte del State.

---

# Active no Significa Published

Debe mantenerse:

```text
Active

≠

Published
```

---

# Suspended no Significa Delivery Failed

Debe mantenerse:

```text
Suspended

≠

Delivery Failed
```

---

# Archived no Significa Integration Event Deleted

Debe mantenerse:

```text
Archived

≠

Integration Event Deletion
```

---

# State Change no Obliga Event Externo

Debe mantenerse:

```text
Integration State Change

≠

Mandatory External Event
```

---

# Domain Fact Independence

Una vez confirmado un Domain Event:

```text
Domain Fact
```

continúa siendo verdadero aunque:

- ningún Integration Event sea necesario;
- la publicación falle;
- el consumidor esté indisponible;
- exista retraso en propagación.

---

# Audit

Audit puede registrar un Domain Event de Integration conforme a su
propio contrato.

Debe mantenerse:

```text
Audit

≠

Integration Event
```

---

# Audit Record no es Integration Event

Debe mantenerse:

```text
Audit Record

≠

Integration Event
```

---

# Notification

Notification puede reaccionar a hechos conforme a sus contratos.

Debe mantenerse:

```text
Notification

≠

Integration Event
```

---

# Notification Delivery no es Integration Event

Una entrega de Notification no representa automáticamente un
Integration Event de Integration Management.

---

# Other Aggregates

Organization, Citizen, Membership, Role, Territory, Assembly, Proposal,
Participation, Voting, Document, Notification y Audit mantienen sus
propios Domain Events e Integration Events cuando corresponda.

---

# No Event Ownership Transfer

Que Integration participe en interoperabilidad no significa que pase a
poseer los eventos de otros Aggregates.

---

# Source Event Ownership

Debe mantenerse:

```text
Source Domain Event

remains owned by

Source Aggregate
```

---

# Integration Event Ownership

Un Integration Event pertenece al contrato mediante el cual se expone
un hecho.

No transforma el Aggregate fuente en parte del consumidor.

---

# Naming

Los nombres concretos de Integration Events deben definirse solamente
cuando exista un contrato explícito.

Este documento no introduce nombres por inferencia.

---

# No Naming by Convention Alone

No debe inferirse automáticamente:

```text
IntegrationCreatedIntegrationEvent

IntegrationActivatedIntegrationEvent

IntegrationSuspendedIntegrationEvent

IntegrationReactivatedIntegrationEvent

IntegrationArchivedIntegrationEvent
```

como eventos oficiales solamente por existir los Domain Events
equivalentes.

---

# Naming Requires Contract

Debe mantenerse:

```text
Concrete Integration Event Name

requires

Explicit Integration Contract
```

---

# No Automatic Suffix Mapping

No se establece una regla:

```text
DomainEventName

+

"IntegrationEvent"

=

Official Integration Event
```

---

# Semantic Independence

El nombre de un Integration Event puede diferir del Domain Event fuente
si el contrato requiere otra semántica explícita.

Esto no autoriza alterar el significado del hecho.

---

# Consumer Language

El contrato debe ser comprensible para el consumidor sin obligarlo a
conocer la estructura interna del Aggregate.

---

# Ubiquitous Language

Cuando corresponda, el contrato debe preservar conceptos de AURA de
manera explícita y estable.

No debe exponer accidentalmente nombres de implementación.

---

# No Infrastructure Naming

Nombres como:

```text
KafkaMessagePublished

HttpPayloadSent

QueueItemCreated

BrokerMessageAcknowledged

WebhookDelivered
```

no constituyen Integration Events del dominio.

---

# No Provider-Specific Event by Default

La existencia de un proveedor no crea automáticamente un evento
específico de proveedor.

---

# No FIWARE-Specific Event by Default

La existencia de FIWARE no crea automáticamente:

```text
FIWAREIntegrationCreated

FIWAREIntegrationActivated
```

como Integration Events oficiales.

---

# No Municipal-Specific Event by Default

La existencia de una integración municipal tampoco crea automáticamente
eventos específicos en este contrato base.

---

# Security

Los Integration Events deben respetar:

```text
DOMAIN-013O-Security-Model.md
```

---

# Data Exposure

La publicación de un Integration Event no autoriza exponer información
que no sea necesaria para el contrato.

---

# Personal Data

La información personal no debe incorporarse por defecto.

Su inclusión requiere necesidad contractual explícita y reglas
aplicables.

---

# Sensitive Data

Datos sensibles o secretos no forman parte del Payload por conveniencia
técnica.

---

# Authorization Context

Un consumidor autorizado para recibir un Integration Event no adquiere
automáticamente Permissions sobre Commands de Integration.

---

# External Consumer no Obtiene Write Authority

Debe mantenerse:

```text
Consume Integration Event

≠

Write Authority over Integration
```

---

# Versioning

La publicación de un Integration Event no incrementa:

```text
Integration.Version
```

---

# Contract Versioning

El contrato de Integration Events puede evolucionar independientemente.

---

# Aggregate Versioning

La evolución contractual no modifica automáticamente:

```text
Integration.Version
```

---

# Event Contract Evolution

Una nueva versión de contrato debe preservar el significado del hecho
conforme a las reglas de compatibilidad que sean definidas para dicho
contrato.

Este documento no decide dichas reglas.

---

# Integration Event no Cambia UpdatedAt

Publicar o entregar un Integration Event no modifica:

```text
Integration.UpdatedAt
```

por sí mismo.

---

# Integration Event no Cambia CreatedAt

Debe mantenerse:

```text
Integration Event Activity

≠

Integration.CreatedAt Change
```

---

# Integration Event no Cambia State

Debe mantenerse:

```text
Publish Integration Event

≠

State Transition
```

---

# Performance

La definición de Integration Events debe evitar trasladar Aggregate
completos innecesariamente.

---

# Small Contract

Debe preferirse:

```text
Contractual Information Required by Consumer
```

sobre:

```text
Entire Internal Model
```

---

# No Global Payload

La versión 1.0 no define un único Payload universal para todos los
consumidores.

---

# No Consumer List

Este documento no establece una lista cerrada de consumidores.

---

# No Broadcast Requirement

Un Integration Event no debe publicarse universalmente por defecto.

---

# Contract Scope

Cada contrato define los consumidores o fronteras para los que resulta
aplicable.

---

# Read Model Relationship

Los Integration Events no sustituyen los Read Models.

Debe mantenerse:

```text
Integration Event

≠

Read Model
```

---

# Integration Event no es Query Result

Un Integration Event representa un hecho contractual.

No es una respuesta genérica de consulta.

---

# API Response no es Integration Event

Una respuesta de API no constituye automáticamente un Integration
Event.

---

# Webhook no es Integration Event

Webhook representa un posible mecanismo técnico.

No define por sí mismo la semántica del evento.

---

# Message no es Integration Event

Debe mantenerse:

```text
Technical Message

≠

Integration Event
```

Un mensaje puede transportar un Integration Event.

No todo mensaje lo representa.

---

# Integration Event no es Transport Envelope

El envelope técnico de transporte permanece separado de la semántica
contractual.

---

# Transport Metadata

Información como:

```text
partition

offset

deliveryCount

routingKey

topic

queue

brokerTimestamp
```

no pertenece automáticamente al Integration Event de dominio.

---

# Contract Metadata

Solamente metadata explícitamente requerida por el contrato forma parte
de la representación conceptual.

---

# Observability Metadata

Metadata técnica de observabilidad permanece fuera del contrato salvo
necesidad explícita.

---

# Correlation Metadata

CorrelationId puede conservarse cuando forma parte del contrato.

Esto no obliga a incorporar toda la metadata de tracing.

---

# Testing

Los Integration Events deben validarse mediante escenarios definidos
en:

```text
DOMAIN-013M-Test-Scenarios.md
```

cuando exista un contrato concreto.

---

# Test Conceptual — Sin Contrato

```text
Given

IntegrationActivated is confirmed

And

no explicit external contract requires publication

When

the fact is processed

Then

no mandatory Integration Event is inferred
```

---

# Test Conceptual — Contrato Explícito

```text
Given

a confirmed Domain Fact

And

an explicit Integration Contract requires external communication

When

the fact crosses the boundary

Then

an Integration Event may be produced according to that contract
```

---

# Test Conceptual — Payload Mínimo

```text
Given

an explicit Integration Event contract

When

the event is produced

Then

only contractually required information is included
```

---

# Test Conceptual — Sin Aggregate Snapshot

```text
Given

an Integration Event is produced

Then

the complete Integration Aggregate is not exposed by default
```

---

# Test Conceptual — Sin Credenciales

```text
Given

Infrastructure credentials exist

When

an Integration Event is produced

Then

credentials are absent from the event payload
```

---

# Test Conceptual — Publication Failure

```text
Given

Integration Domain Fact is already confirmed

When

external publication fails

Then

Integration State remains unchanged

And

Integration.Version remains unchanged
```

---

# Test Conceptual — Redelivery

```text
Given

the same Integration Event is delivered again

When

technical redelivery occurs

Then

no new Integration Domain Fact is inferred
```

---

# Test Conceptual — Incoming Event

```text
Given

an incoming Integration Event

When

it reaches AURA

Then

it must be interpreted through its explicit contract

And

it does not mutate Integration directly
```

---

# Test Conceptual — External State

```text
Given

an incoming contract contains external status = OFFLINE

When

the event is interpreted

Then

Integration State is not automatically changed to Suspended
```

---

# Test Conceptual — Contract Version

```text
Given

Integration.Version = 5

And

Integration Event Contract Version = 2

Then

both versions remain semantically independent
```

---

# Evolución Futura

La incorporación de un Integration Event concreto requiere un contrato
explícito.

---

# Regla para Incorporar un Integration Event

Antes de definir un nuevo Integration Event debe responderse:

```text
Which confirmed fact must cross a boundary?

Which consumer or external boundary requires it?

What semantic contract is required?

What minimum information is necessary?

What source fact does it represent?

Does it preserve domain ownership?

Does it preserve the Consistency Boundary?

Does it avoid exposing credentials or unnecessary data?
```

---

# Nuevo Integration Event no Crea Nuevo Domain Event

Debe mantenerse:

```text
New Integration Event

≠

New Domain Event Automatically
```

---

# Nuevo Integration Event no Crea State

Debe mantenerse:

```text
New Integration Event

≠

New Lifecycle State
```

---

# Nuevo Integration Event no Crea Command

Debe mantenerse:

```text
New Integration Event

≠

New Command
```

---

# Nuevo Integration Event no Crea Permission

Debe mantenerse:

```text
New Integration Event

≠

New Permission
```

---

# Nuevo Contrato no Expande Aggregate

La incorporación de un nuevo consumidor no expande automáticamente el
Consistency Boundary.

---

# Impacto de Evolución

Cuando un nuevo Integration Event concreto sea definido, deberá
revisarse cuando corresponda:

```text
DOMAIN-013-Aggregate.md

DOMAIN-013D-Domain-Events.md

DOMAIN-013E-Invariants.md

DOMAIN-013I-Versioning.md

DOMAIN-013J-Consistency-Boundary.md

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
Domain Event

≠

Automatic Integration Event
```

y:

```text
External System Exists

≠

Integration Event Contract Exists
```

y:

```text
Broker Exists

≠

Integration Event Required
```

y:

```text
Technical Message

≠

Integration Event
```

y:

```text
External State

≠

AURA Domain Fact
```

---

# Reglas Fundamentales

Los Integration Events de Integration deben cumplir:

1. Domain Event e Integration Event son conceptos diferentes.
2. Domain Event representa un hecho interno confirmado.
3. Integration Event representa un hecho expuesto mediante un contrato
   de interoperabilidad.
4. No todo Domain Event produce un Integration Event.
5. No existe publicación externa obligatoria por defecto.
6. Un Integration Event requiere un contrato explícito.
7. La versión 1.0 no define nombres concretos obligatorios de
   Integration Events.
8. Los Domain Events oficiales permanecen IntegrationCreated,
   IntegrationActivated, IntegrationSuspended,
   IntegrationReactivated e IntegrationArchived.
9. Ninguno de esos Domain Events implica automáticamente un evento
   externo homónimo.
10. No existe mapeo uno a uno obligatorio entre Domain Events e
    Integration Events.
11. No se infieren cardinalidades entre eventos.
12. Diferentes consumidores pueden utilizar contratos diferentes.
13. El Integration Event debe expresar semántica contractual.
14. El Integration Event no expone el Aggregate completo.
15. Payload debe aplicar Data Minimization.
16. Domain Event Payload no se copia automáticamente.
17. External Payload no se copia automáticamente.
18. IntegrationId puede incluirse solamente cuando sea necesario.
19. IntegrationId no transfiere ownership.
20. SourceEventId puede preservarse cuando el contrato lo requiera.
21. SourceAggregateVersion puede preservarse cuando corresponda.
22. SourceAggregateVersion no es Contract Version.
23. Contract Version no es Integration.Version.
24. OccurredAt del hecho no es Publication Time.
25. Delivery Time no es OccurredAt del dominio.
26. CorrelationId no es obligatorio universalmente.
27. CausationId no es obligatorio universalmente.
28. ActorId no es obligatorio universalmente.
29. CorrelationId no fusiona Boundaries.
30. CausationId no concede Mutation Authority.
31. ActorId no representa Authorization.
32. Integration Events no contienen credenciales.
33. Integration Events no contienen secretos.
34. Incoming Integration Event no modifica directamente Integration.
35. Incoming Integration Event no es Command automáticamente.
36. Incoming Integration Event no es Permission.
37. Incoming Integration Event no es AURA Domain Fact automáticamente.
38. Integration Event no es State.
39. Integration Event no es Aggregate.
40. Integration Event no crea Internal Entity.
41. Integration Events no amplían el Consistency Boundary.
42. Producer y Consumer mantienen Boundaries separados.
43. Consistencia externa permanece eventual.
44. Domain Fact debe estar confirmado antes de exponerse como hecho
    contractual.
45. External Delivery Success no confirma el Domain Fact.
46. Publication Failure no revierte el Aggregate.
47. Delivery Failure no produce State Transition.
48. Retry técnico no crea un nuevo Domain Fact.
49. Retry técnico no incrementa Integration.Version.
50. Redelivery técnica no representa automáticamente un nuevo hecho.
51. La estrategia de idempotencia no se define aquí.
52. La estrategia de deduplicación no se define aquí.
53. Exactly Once no es requisito universal.
54. At Least Once no es requisito universal.
55. At Most Once no es requisito universal.
56. No existe orden global obligatorio.
57. SourceAggregateVersion puede preservar orden lógico por Aggregate.
58. Replay no produce nuevos Integration Events automáticamente.
59. Rehydration no produce nuevos Integration Events.
60. Projection Rebuild no produce nuevos Integration Events por
    definición.
61. Event Sourcing es compatible pero no obligatorio.
62. Aggregate Event Stream no es Integration Event Stream.
63. Integration Event Stream no es automáticamente Source of Truth del
    Aggregate.
64. CQRS no modifica la semántica de Integration Events.
65. Repository no define Integration Events.
66. save() no es Integration Event.
67. Repository.delete() no es Integration Event.
68. PersistenceFailure no es Integration Event.
69. Database Events no son Integration Events por definición.
70. Infrastructure Events no son Integration Events por definición.
71. Broker Events no son Integration Events del dominio.
72. Monitoring Events no son Integration Events del dominio.
73. FIWARE puede ser consumidor o frontera contractual sin formar parte
    del Aggregate.
74. NGSI-LD no es formato obligatorio del Integration Event.
75. Sistemas municipales pueden interoperar mediante contratos sin
    redefinir el Domain Model.
76. La semántica del evento es independiente del protocolo.
77. La semántica del evento es independiente del broker.
78. Serialization Format no define el significado del evento.
79. Este documento no exige JSON.
80. Este documento no exige XML.
81. Schema Evolution no modifica automáticamente Integration.Version.
82. No se exige Schema Registry.
83. No se exige Transactional Outbox.
84. No se exige Inbox Pattern.
85. No se exige Dead Letter Queue.
86. No se define una Retry Policy universal.
87. No se define mecanismo de transporte.
88. No se define Event Bus obligatorio.
89. No se definen topics, queues ni routing keys.
90. Inbound Integration Event no modifica directamente el Aggregate.
91. Outbound Integration Event no confirma cambio del consumidor.
92. Consumer Failure no suspende automáticamente Integration.
93. Consumer Recovery no reactiva automáticamente Integration.
94. State Change no obliga publicación externa.
95. Audit Record no es Integration Event.
96. Notification Delivery no es Integration Event.
97. Los eventos de otros Aggregates mantienen ownership de sus
    productores.
98. Los nombres concretos de Integration Events requieren contrato
    explícito.
99. No se infieren nombres mediante sufijos automáticos.
100. Toda evolución futura de Integration Events requiere preservar los
     contratos oficiales y el Consistency Boundary de AURA Core.

---

# Restricciones

No está permitido:

- tratar Domain Event e Integration Event como el mismo concepto;
- publicar automáticamente todo Domain Event;
- asumir que IntegrationCreated requiere un Integration Event;
- asumir que IntegrationActivated requiere un Integration Event;
- asumir que IntegrationSuspended requiere un Integration Event;
- asumir que IntegrationReactivated requiere un Integration Event;
- asumir que IntegrationArchived requiere un Integration Event;
- inventar nombres concretos de Integration Events sin contrato;
- crear nombres mediante sufijos automáticos;
- imponer relación uno a uno entre Domain Event e Integration Event;
- imponer cardinalidad no definida;
- exponer el Aggregate completo;
- copiar automáticamente Domain Event Payload completo;
- copiar automáticamente External Payload completo;
- incluir Password;
- incluir AccessToken;
- incluir RefreshToken;
- incluir ApiKey;
- incluir ClientSecret;
- incluir PrivateKey;
- incluir Secret;
- interpretar Integration Event como Command;
- interpretar Integration Event como Permission;
- interpretar Integration Event como Lifecycle State;
- modificar Integration directamente desde un evento entrante;
- utilizar setState() desde un Integration Event;
- convertir un estado externo directamente en State de AURA;
- considerar un Integration Event entrante como Domain Fact confirmado
  automáticamente;
- fusionar Producer y Consumer Boundaries;
- incluir al sistema externo dentro del Aggregate;
- revertir Integration por Publication Failure;
- suspender Integration por Delivery Failure automáticamente;
- incrementar Version por retry técnico;
- generar nuevos Domain Events por redelivery;
- imponer estrategia concreta de idempotencia;
- imponer estrategia concreta de deduplicación;
- imponer Exactly Once;
- imponer At Least Once;
- imponer At Most Once;
- imponer orden global;
- publicar eventos nuevos durante Replay por defecto;
- publicar eventos nuevos durante Rehydration;
- utilizar Repository como productor semántico de Integration Events;
- utilizar eventos de base de datos como Integration Events;
- utilizar eventos de broker como Integration Events de dominio;
- utilizar Health Events como Integration Events del Aggregate;
- imponer NGSI-LD;
- imponer FIWARE como modelo interno;
- imponer modelo municipal como modelo interno;
- imponer protocolo;
- imponer broker;
- imponer JSON;
- imponer XML;
- imponer Schema Registry;
- imponer Transactional Outbox;
- imponer Inbox Pattern;
- imponer Dead Letter Queue;
- imponer Retry Policy;
- imponer Event Bus;
- imponer topic;
- imponer queue;
- imponer routing key;
- imponer webhook;
- imponer polling;
- imponer streaming;
- interpretar Active como Published;
- interpretar Suspended como Delivery Failed;
- interpretar Archived como eliminación de Integration Events;
- conceder Permissions de dominio por consumir un evento;
- crear un nuevo Integration Event sin contrato explícito;
- introducir arquitectura nueva desde este contrato conceptual.

---

# Compatibilidad Arquitectónica

Los Integration Events son compatibles conceptualmente con:

- Domain-Driven Design;
- Aggregate Pattern;
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

Estas compatibilidades no imponen:

- broker;
- protocolo;
- serialización;
- Event Bus;
- Transactional Outbox;
- Inbox;
- Dead Letter Queue;
- Schema Registry;
- FIWARE;
- NGSI-LD;
- plataforma municipal;
- framework;
- estrategia de entrega;
- estrategia de retry;
- estrategia de idempotencia.

---

# Definición de Éxito

Los Integration Events asociados al Aggregate **Integration** permiten
cruzar fronteras de interoperabilidad sin confundir el modelo interno
de AURA con contratos externos ni introducir dependencias técnicas en
el dominio.

El modelo fundamental queda definido como:

```text
Valid Domain Behavior
        │
        ▼
Confirmed Domain Event
        │
        ▼
Explicit Integration Contract
        │
        ▼
Integration Event
        │
        ▼
External Boundary
```

solamente cuando:

```text
Explicit Integration Contract Exists
```

Si no existe dicho contrato:

```text
Confirmed Domain Event

does not imply

Integration Event
```

El modelo garantiza que:

- Domain Events e Integration Events permanezcan separados;
- los hechos internos continúen perteneciendo a Integration;
- ningún Domain Event obligue publicación externa automáticamente;
- los nombres concretos de Integration Events no se inventen;
- cada contrato externo defina únicamente los eventos que necesita;
- Payload permanezca mínimo;
- Aggregate completo no sea expuesto;
- información externa no se copie automáticamente;
- credenciales y secretos permanezcan fuera de los eventos;
- IntegrationId no transfiera ownership;
- SourceEventId y SourceAggregateVersion se utilicen solamente cuando
  el contrato lo requiera;
- Contract Version permanezca separada de Integration.Version;
- OccurredAt permanezca separado de Publication Time y Delivery Time;
- CorrelationId y CausationId no sean obligatorios universalmente;
- Integration Events entrantes no modifiquen directamente el
  Aggregate;
- Integration Event no sea Command ni Permission;
- Producer y Consumer mantengan Consistency Boundaries independientes;
- consistencia externa permanezca eventual;
- Publication Failure no revierta el hecho interno;
- Retry y Redelivery no creen hechos nuevos automáticamente;
- Version no cambie por actividad técnica de publicación;
- Repository permanezca separado del contrato de interoperabilidad;
- FIWARE permanezca como sistema externo;
- NGSI-LD no sea impuesto como formato;
- sistemas municipales permanezcan externos al Domain Model;
- protocolos y brokers no definan la semántica;
- serialización no defina la semántica;
- Event Sourcing permanezca compatible pero no obligatorio;
- CQRS no altere la separación entre hechos internos y externos;
- ninguna estrategia concreta de transporte, publicación, retry,
  deduplicación o idempotencia sea decidida por este documento;
- cualquier nuevo Integration Event requiera una necesidad contractual
  explícita y preserve el patrón consolidado de AURA Core.

De esta forma, `DOMAIN-013K-Integration-Events.md` establece
formalmente las reglas conceptuales oficiales para Integration Events
del Aggregate **Integration** conforme al patrón consolidado de AURA
Core.