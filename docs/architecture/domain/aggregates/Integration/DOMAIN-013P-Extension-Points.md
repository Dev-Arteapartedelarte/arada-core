# DOMAIN-013P — Integration Extension Points

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
- DOMAIN-013K-Integration-Events.md
- DOMAIN-013L-Read-Model.md
- DOMAIN-013M-Test-Scenarios.md
- DOMAIN-013N-Performance-Rules.md
- DOMAIN-013O-Security-Model.md

---

# Objetivo

Este documento define formalmente los **Extension Points**
conceptuales del Aggregate **Integration**.

Su propósito es establecer las reglas mediante las cuales el dominio
puede evolucionar en versiones futuras sin romper:

- identidad;
- Lifecycle;
- State Machine;
- Commands;
- Domain Events;
- Invariants;
- Permissions;
- Repository Contract;
- Versioning;
- Consistency Boundary;
- Integration Events;
- Read Models;
- Security Model;
- Performance Rules.

Los Extension Points no representan funcionalidades ya existentes.

---

# Principio Fundamental

Debe mantenerse:

```text
Extension Point

=

Explicitly Controlled Domain Evolution Possibility
```

y:

```text
Extension Point

≠

Existing Domain Behavior
```

---

# Regla de No Inferencia

La existencia de un Extension Point no autoriza implementar o asumir
comportamiento futuro.

Debe mantenerse:

```text
Extension Point Exists

≠

Future Feature Already Defined
```

---

# Evolución Explícita

Toda extensión futura requiere una definición explícita.

No puede derivarse automáticamente desde:

- Infrastructure;
- APIs externas;
- FIWARE;
- sistemas municipales;
- brokers;
- protocolos;
- frameworks;
- bases de datos;
- necesidades de UI;
- necesidades de reporting;
- necesidades de observabilidad.

---

# Protección del Patrón Consolidado

Toda extensión debe preservar el patrón consolidado de AURA Core.

Debe mantenerse:

```text
New Requirement

≠

Automatic Domain Redesign
```

---

# Extension Point — Lifecycle

El Lifecycle puede evolucionar solamente mediante decisión formal.

Cualquier nuevo State requiere revisar:

```text
DOMAIN-013A-Lifecycle.md

DOMAIN-013B-State-Machine.md

DOMAIN-013C-Commands.md

DOMAIN-013D-Domain-Events.md

DOMAIN-013E-Invariants.md

DOMAIN-013F-Permissions.md

DOMAIN-013I-Versioning.md

DOMAIN-013J-Consistency-Boundary.md

DOMAIN-013M-Test-Scenarios.md
```

---

# Estados Oficiales Actuales

La versión 1.0 mantiene exclusivamente:

```text
Draft

Active

Suspended

Archived
```

---

# No Nuevos States Implícitos

No deben inferirse como States:

```text
Connected

Disconnected

Failed

Pending

Processing

Retrying

Healthy

Unhealthy

Degraded

Deleted

Cancelled

Expired

Locked

Blocked

Compromised
```

---

# Nuevo State

Un nuevo State solamente puede incorporarse cuando represente una
condición real del dominio y no una condición técnica.

Debe definir explícitamente:

- significado;
- precondiciones;
- transiciones de entrada;
- transiciones de salida;
- Commands relacionados;
- Domain Events relacionados;
- Invariants;
- Permissions;
- efecto sobre Versioning;
- terminalidad cuando corresponda.

---

# Extension Point — State Machine

Nuevas transiciones pueden incorporarse únicamente mediante definición
formal.

---

# Lista Cerrada Actual

Las transiciones oficiales permanecen:

```text
No Integration → Draft

Draft → Active

Draft → Archived

Active → Suspended

Active → Archived

Suspended → Active

Suspended → Archived
```

---

# Nueva Transición

Una nueva transición requiere:

```text
Explicit Source State

Explicit Target State

Explicit Domain Intent

Explicit Permission

Explicit Guards

Explicit Invariants

Explicit Versioning Effect

Explicit Domain Event
```

cuando corresponda.

---

# No Transición por Infraestructura

Un cambio técnico no crea una transición.

Debe mantenerse:

```text
Infrastructure State Change

≠

Integration State Transition
```

---

# Extension Point — Commands

Nuevos Commands pueden incorporarse cuando exista una nueva intención
real del dominio.

---

# Commands Oficiales Actuales

La versión 1.0 mantiene:

```text
CreateIntegration

ActivateIntegration

SuspendIntegration

ReactivateIntegration

ArchiveIntegration
```

---

# Nuevo Command

Un nuevo Command debe representar:

```text
Explicit Domain Intent
```

y no una acción técnica.

---

# No Command Técnico

No se incorporan por inferencia:

```text
ConnectIntegration

DisconnectIntegration

RetryIntegration

FailIntegration

RefreshIntegration

HealthCheckIntegration

SyncIntegration

PublishIntegration

DeleteIntegration

UpdateIntegration

ModifyIntegration
```

---

# Nuevo Command y State Machine

Todo nuevo Command que modifique Lifecycle debe declarar explícitamente
la transición correspondiente.

---

# Nuevo Command y Permission

Todo nuevo Command protegido debe declarar la Permission asociada.

---

# Nuevo Command y Versioning

Si un nuevo Command modifica válidamente el Aggregate:

```text
Version N

→

Version N + 1
```

conforme al patrón oficial.

---

# Nuevo Command y Domain Event

Una modificación confirmada debe definir su hecho correspondiente
cuando represente un nuevo hecho de dominio.

---

# Extension Point — Domain Events

Nuevos Domain Events pueden incorporarse solamente cuando exista un
nuevo hecho real del dominio.

---

# Domain Events Oficiales Actuales

La versión 1.0 mantiene:

```text
IntegrationCreated

IntegrationActivated

IntegrationSuspended

IntegrationReactivated

IntegrationArchived
```

---

# Nuevo Domain Event

Un nuevo Domain Event debe definir:

- hecho representado;
- Aggregate productor;
- relación con Command o comportamiento;
- AggregateVersion;
- identidad del hecho;
- semántica temporal;
- Payload mínimo necesario;
- relación con CorrelationId cuando corresponda;
- relación con CausationId cuando corresponda.

---

# No Domain Event Técnico

No deben incorporarse por conveniencia:

```text
IntegrationConnected

IntegrationDisconnected

IntegrationFailed

IntegrationRetried

IntegrationCached

IntegrationScaled

IntegrationPublished

IntegrationSynchronized

IntegrationUpdated
```

---

# Event Naming

Un nuevo Domain Event debe expresar un hecho de dominio concreto.

Debe evitar nombres genéricos que oculten significado.

---

# Event Immutability

Todo nuevo Domain Event confirmado debe preservar inmutabilidad
histórica.

---

# Extension Point — Invariants

Nuevas Invariants solamente pueden introducirse cuando representen una
condición necesaria para mantener válido el Aggregate.

---

# Nueva Invariant

Una nueva Invariant debe:

- pertenecer a Integration;
- proteger validez interna;
- ser evaluable dentro del Boundary correspondiente;
- no depender de condiciones técnicas transitorias;
- no depender de disponibilidad externa como condición implícita;
- no sustituir Permissions;
- no sustituir Authentication;
- no sustituir Authorization.

---

# No Invariant Técnica

No se convierte automáticamente en Invariant:

```text
External system available

Broker available

FIWARE available

Latency below threshold

Retry count below threshold

Cache warm

Network connected
```

---

# Extension Point — Permissions

Nuevas Permissions pueden incorporarse solamente cuando exista una
nueva capacidad real del dominio.

---

# Permissions Oficiales Actuales

La versión 1.0 mantiene:

```text
Integration.Create

Integration.Activate

Integration.Suspend

Integration.Reactivate

Integration.Archive
```

---

# Nueva Permission

Una nueva Permission debe:

- proteger una capacidad explícita;
- mantener Least Privilege;
- no sustituir State Machine;
- no sustituir Invariants;
- no sustituir Versioning;
- no transferir ownership;
- no concederse por inferencia desde autorizaciones externas.

---

# No Permission Técnica

La existencia de una operación técnica no crea automáticamente:

```text
Integration.Connect

Integration.Disconnect

Integration.Retry

Integration.HealthCheck

Integration.Sync

Integration.Publish

Integration.Delete
```

---

# Extension Point — Repository Contract

IntegrationRepository puede evolucionar solamente por necesidades reales
de persistencia del Aggregate.

---

# Repository Contract Actual

La versión 1.0 mantiene:

```text
save()

findById()

exists()

delete()

nextIdentity()
```

---

# Nueva Repository Operation

Una nueva operación debe demostrar que:

```text
it belongs to Aggregate persistence
```

y no a:

```text
reporting

analytics

search

external communication

transport

domain behavior
```

---

# No Repository Growth por Query

Una nueva necesidad de lectura no amplía automáticamente
IntegrationRepository.

---

# No Repository Growth por Integration

Una nueva necesidad de interoperabilidad no convierte Repository en:

- HTTP Client;
- FIWARE Adapter;
- broker publisher;
- municipal connector;
- message producer.

---

# Repository Compatibility

Toda extensión del contrato debe preservar:

```text
Aggregate Persistence

Consistency Boundary

Versioning

Technology Independence
```

---

# Extension Point — Versioning

Versioning puede evolucionar solamente mediante decisión formal.

---

# Versioning Actual

La versión 1.0 mantiene:

```text
New Integration

=

Version 1
```

y:

```text
Valid Modification

Version N

→

Version N + 1
```

---

# Nueva Regla de Versioning

Cualquier cambio debe preservar:

- evolución lógica;
- monotonicidad;
- relación con AggregateVersion;
- protección de concurrencia;
- independencia por IntegrationId.

---

# No Version Técnica

No debe reemplazarse Integration.Version por:

```text
Database Revision

External Version

Contract Version

API Version

Schema Version

Timestamp

EventId
```

---

# Extension Point — Consistency Boundary

El Boundary solamente puede ampliarse mediante una necesidad real de
consistencia inmediata.

---

# Boundary Actual

Debe mantenerse:

```text
One IntegrationId

=

One Integration Consistency Boundary
```

---

# Nueva Información Dentro del Boundary

Para incorporar un nuevo concepto debe demostrarse que:

```text
it must participate in the same invariants

and

it must be consistent in the same Aggregate transaction
```

---

# No Boundary Expansion por Conveniencia

No amplían automáticamente el Boundary:

- Query requirements;
- reporting;
- analytics;
- performance;
- security infrastructure;
- external APIs;
- FIWARE;
- municipal systems;
- transport;
- broker;
- caching.

---

# No Aggregate Merge

Una nueva integración funcional no permite fusionar:

```text
Integration

+

Organization

+

Audit

+

Notification
```

en un Aggregate único por inferencia.

---

# Extension Point — Internal Entities

La versión 1.0 no establece Internal Entities concretas.

---

# Nueva Internal Entity

Una futura Internal Entity solamente puede incorporarse cuando:

- tenga identidad local dentro del Aggregate;
- pertenezca al Lifecycle interno de Integration;
- necesite consistencia inmediata con la Aggregate Root;
- no pueda ser modelada simplemente como referencia externa;
- no sea otro Aggregate Root.

---

# No Entity por Persistencia

Una tabla, colección o documento técnico no crea una Internal Entity.

---

# No Entity por External Model

Una entidad FIWARE o municipal no se convierte automáticamente en
Internal Entity.

---

# Extension Point — Value Objects

La versión 1.0 no establece Value Objects específicos obligatorios.

---

# Nuevo Value Object

Un futuro Value Object debe:

- representar un concepto real del dominio;
- poseer semántica propia;
- ser definido explícitamente;
- no surgir únicamente por conveniencia de serialización o tecnología.

---

# No Value Object Técnico

Un tipo técnico no crea automáticamente un Value Object de Integration.

---

# Extension Point — Integration Events

Integration Events concretos pueden incorporarse cuando exista un
contrato explícito que requiera cruzar una frontera.

---

# Regla Actual

La versión 1.0 mantiene:

```text
Domain Event

≠

Automatic Integration Event
```

---

# Nuevo Integration Event

Un nuevo Integration Event requiere:

- hecho fuente confirmado;
- consumidor o frontera identificada;
- contrato explícito;
- semántica explícita;
- Payload mínimo;
- preservación de ownership;
- separación respecto del Domain Event;
- separación respecto del Aggregate.

---

# No Integration Event Automático

No se crea un Integration Event solamente porque:

- exista un Domain Event;
- exista FIWARE;
- exista un broker;
- exista una API;
- exista un consumidor potencial.

---

# No Naming Automático

No debe inferirse:

```text
DomainEventName

+

"IntegrationEvent"
```

como nombre contractual oficial.

---

# Contract Evolution

Los Integration Event Contracts pueden evolucionar de forma
independiente.

---

# Contract Version Independence

Debe mantenerse:

```text
Integration Event Contract Version

≠

Integration.Version
```

---

# Extension Point — Read Models

Nuevos Read Models pueden incorporarse para nuevas necesidades de
consulta.

---

# Nuevo Read Model

Un nuevo Read Model debe definir:

- propósito de consulta;
- información necesaria;
- fuentes conceptuales;
- separación respecto del Write Model;
- ausencia de Write Authority;
- Data Minimization.

---

# No Read Model as Aggregate

Debe mantenerse:

```text
Read Model

≠

Aggregate
```

---

# Nuevo Read Field

Un nuevo campo de lectura no crea automáticamente un nuevo atributo del
Aggregate.

---

# Joined Read Model

Una composición de lectura puede combinar información de múltiples
contextos.

Debe mantenerse:

```text
Joined Read Model

≠

Joined Aggregate
```

---

# Read Model Technology

La incorporación de una nueva tecnología de lectura no modifica el
Domain Model.

---

# Extension Point — Security

Nuevas necesidades de seguridad pueden incorporarse sin convertir
mecanismos técnicos en estado del Aggregate.

---

# Nueva Security Capability

Una nueva capacidad protegida puede requerir:

```text
New Permission
```

solamente si existe una nueva capacidad real del dominio.

---

# Nuevo Security Mechanism

Un nuevo mecanismo técnico de:

- Authentication;
- Authorization;
- encryption;
- secret management;
- key management;

no crea automáticamente:

- State;
- Command;
- Domain Event;
- Permission;
- Aggregate attribute.

---

# No Credentials in Aggregate

Toda extensión debe preservar:

```text
Credentials

∉

Integration Aggregate
```

---

# No Secrets in Events

Toda extensión debe preservar:

```text
Secrets

∉

Domain Events

Integration Events
```

---

# Security Technology Independence

Nuevos mecanismos de seguridad no redefinen las reglas conceptuales de
Integration.

---

# Extension Point — Performance

Nuevas optimizaciones pueden incorporarse siempre que no modifiquen el
significado del dominio.

---

# Nueva Performance Optimization

Una optimización debe preservar:

```text
Correctness

Invariants

Versioning

Boundary

Permissions

Ownership
```

---

# No Performance State

Una optimización o degradación técnica no crea nuevo Lifecycle State.

---

# No Performance Command

Una acción técnica de scaling, caching o tuning no crea Command del
dominio.

---

# No Performance Event

Una métrica técnica no crea Domain Event.

---

# Extension Point — External Systems

Nuevos sistemas externos pueden integrarse mediante contratos explícitos.

---

# Nuevo Sistema Externo

Incorporar un nuevo sistema externo no modifica automáticamente:

- IntegrationId;
- State;
- Version;
- Lifecycle;
- Commands;
- Domain Events;
- Permissions;
- Consistency Boundary.

---

# External System Remains External

Debe mantenerse:

```text
External System

∉

Integration Aggregate
```

---

# External Model Remains External

Debe mantenerse:

```text
External Data Model

≠

Integration Domain Model
```

---

# Extension Point — FIWARE

Nuevos contratos con FIWARE pueden definirse.

FIWARE permanece externo al Domain Model.

---

# FIWARE Contract

Un futuro contrato FIWARE deberá preservar:

- separación de modelos;
- ownership;
- Consistency Boundary;
- Data Minimization;
- Domain Event versus Integration Event;
- Security Model.

---

# No FIWARE Internalization

Debe mantenerse:

```text
FIWARE Entity

≠

Integration Internal Entity
```

---

# NGSI-LD

El uso futuro de NGSI-LD no redefine automáticamente Integration.

---

# Extension Point — Sistemas Municipales

Nuevos contratos municipales pueden incorporarse.

---

# Municipal Contract

Un contrato municipal futuro debe preservar:

```text
Municipal Model

≠

AURA Domain Model
```

---

# Municipal Identity

Identidades municipales no se convierten automáticamente en:

```text
Citizen

Role

Membership

Permission
```

---

# Municipal Authorization

Autorizaciones municipales no conceden automáticamente Permissions de
Integration.

---

# Extension Point — Smart City

Nuevas plataformas Smart City pueden participar mediante contratos
explícitos.

---

# Smart City Technology

Una tecnología Smart City no se incorpora al Aggregate por existir una
nueva integración.

---

# Extension Point — Protocols

Nuevos protocolos pueden utilizarse en Infrastructure sin modificar el
dominio.

---

# Protocol Independence

Debe mantenerse:

```text
Protocol Change

≠

Domain Change
```

---

# Extension Point — Brokers

Nuevos brokers pueden utilizarse sin modificar Integration.

---

# Broker Independence

Debe mantenerse:

```text
Broker Change

≠

Aggregate Change
```

---

# Extension Point — Persistence

Una nueva tecnología de persistencia puede reemplazar a otra siempre
que preserve el Repository Contract.

---

# Persistence Independence

Debe mantenerse:

```text
Persistence Technology Change

≠

Domain Model Change
```

---

# Extension Point — Event Sourcing

Event Sourcing permanece compatible.

Puede adoptarse solamente mediante decisión arquitectónica explícita.

---

# Event Sourcing no es Extensión Implícita

Debe mantenerse:

```text
Domain Events Exist

≠

Event Sourcing Required
```

---

# Event Sourcing Adoption

Si se adopta en el futuro, debe preservar:

- Aggregate identity;
- Lifecycle;
- Invariants;
- Versioning;
- historical event meaning;
- Replay semantics;
- Consistency Boundary.

---

# Extension Point — CQRS

CQRS permanece compatible.

Una implementación física separada de Write Side y Read Side requiere
una decisión arquitectónica explícita.

---

# CQRS no es Extensión Implícita

Debe mantenerse:

```text
Read Model Exists

≠

Physical CQRS Required
```

---

# Extension Point — Idempotency

La versión 1.0 no define un mecanismo técnico concreto de idempotencia.

---

# Future Idempotency Strategy

Una estrategia futura puede incorporarse mediante decisión explícita.

No debe modificar:

- Commands;
- Domain Events;
- Lifecycle;
- Versioning;
- Aggregate identity;

salvo que exista una razón real del dominio para ello.

---

# Extension Point — Deduplication

La versión 1.0 no define un mecanismo técnico concreto de deduplicación.

---

# Deduplication no es Domain State

Debe mantenerse:

```text
Duplicate Technical Message

≠

Integration State
```

---

# Extension Point — Delivery Semantics

La versión 1.0 no define garantías universales de:

```text
Exactly Once

At Least Once

At Most Once
```

---

# Future Delivery Contract

Una garantía concreta puede establecerse en un contrato técnico o de
interoperabilidad futuro.

No se convierte automáticamente en Invariant del Aggregate.

---

# Extension Point — Ordering

La versión 1.0 no define Global Ordering.

---

# Future Ordering Need

Una necesidad de orden futuro debe distinguir:

```text
Per-Aggregate Logical Order

from

Cross-Aggregate Global Order
```

---

# No Global Ordering by Default

Debe mantenerse:

```text
AggregateVersion

≠

Global Event Sequence
```

---

# Extension Point — Retention

La versión 1.0 no define:

- retention period;
- purge;
- expiration;
- automatic deletion.

---

# Future Retention Rule

Una futura política de retención requiere definición explícita.

No debe alterar silenciosamente Lifecycle.

---

# Retention no Crea State

Una política futura no crea automáticamente:

```text
Expired

Deleted
```

como Lifecycle States.

---

# Extension Point — Physical Deletion

Repository.delete() existe como operación conceptual de persistencia.

La posibilidad de eliminación física continúa separada del Lifecycle.

---

# Future Physical Deletion Rule

Una futura regla debe especificar claramente cuándo una eliminación
física está permitida.

---

# Physical Deletion no es Archive

Debe mantenerse:

```text
ArchiveIntegration

≠

Physical Deletion
```

---

# Extension Point — Audit

Nuevos contratos con Audit pueden definirse.

---

# Audit Remains Separate

Debe mantenerse:

```text
Audit

≠

Integration
```

---

# Audit Contract

Una futura extensión puede permitir mayor trazabilidad sin incorporar
Audit dentro del Consistency Boundary.

---

# Extension Point — Notification

Nuevos contratos con Notification pueden definirse.

---

# Notification Remains Separate

Debe mantenerse:

```text
Notification

≠

Integration
```

---

# Notification Contract

Una futura extensión puede producir necesidades de Notification sin
hacer que el Delivery State pertenezca a Integration.

---

# Extension Point — Other Aggregates

Nuevas relaciones con otros Aggregates pueden definirse mediante
referencias y contratos explícitos.

---

# Ownership Preservation

Toda nueva relación debe preservar:

```text
Reference

≠

Ownership Transfer
```

---

# No Aggregate Embedding

Ninguna relación futura debe embebir otro Aggregate Root solamente por
conveniencia.

---

# Extension Point — Correlation

CorrelationId puede utilizarse cuando un contrato requiera trazabilidad.

---

# Correlation no Crea Shared Boundary

Debe mantenerse:

```text
Same CorrelationId

≠

Same Consistency Boundary
```

---

# Extension Point — Causation

CausationId puede utilizarse cuando deba preservarse causalidad.

---

# Causation no Concede Authority

Debe mantenerse:

```text
CausationId

≠

Authorization
```

---

# Extension Point — Actor Traceability

ActorId puede incorporarse en hechos o contratos cuando corresponda.

---

# ActorId no es Aggregate Member Obligatorio

Debe mantenerse:

```text
ActorId

≠

Mandatory Integration Aggregate Attribute
```

---

# Extension Point — External Identity

Nuevas identidades externas pueden referenciarse cuando exista un
contrato explícito.

---

# External Identity no Reemplaza IntegrationId

Debe mantenerse:

```text
External Identifier

≠

IntegrationId
```

---

# Extension Point — Data Model

El Domain Model puede evolucionar mediante nuevos atributos cuando
exista necesidad explícita.

---

# Nuevo Aggregate Attribute

Un nuevo atributo debe:

- pertenecer realmente a Integration;
- ser necesario para comportamiento o consistencia;
- no duplicar información externa innecesariamente;
- preservar ownership;
- preservar Data Minimization;
- definir su efecto sobre Commands, Events, Invariants y Read Models
  cuando corresponda.

---

# No Attribute por API

Un campo de una API externa no crea automáticamente un Aggregate
Attribute.

---

# No Attribute por Read Model

Un campo útil para reporting tampoco crea automáticamente un atributo de
escritura.

---

# No Attribute por Infrastructure

Metadata técnica no crea atributos del dominio por sí misma.

---

# Extension Point — Timestamps

Nuevos timestamps solamente deben incorporarse cuando tengan semántica
real de dominio.

---

# No Technical Timestamp as Domain Attribute

Un timestamp técnico de:

- delivery;
- retry;
- broker;
- cache;
- monitoring;

no se convierte automáticamente en atributo del Aggregate.

---

# Extension Point — Read-side Analytics

Nuevas necesidades analíticas deben resolverse sin expandir
automáticamente el Write Model.

---

# Analytics Remains Read Concern

Debe mantenerse:

```text
Analytics Requirement

≠

Aggregate Behavior Requirement
```

---

# Extension Point — Reporting

Nuevos reportes pueden generar nuevas vistas de lectura.

No nuevos Commands por defecto.

---

# Extension Point — Search

Nuevas necesidades de búsqueda pueden generar estructuras de lectura.

No nuevas Invariants por defecto.

---

# Extension Point — Performance Thresholds

Futuros SLO, SLA o SLI pueden definirse fuera del Aggregate.

---

# Threshold no Crea Domain State

Debe mantenerse:

```text
Latency Threshold Exceeded

≠

Integration State Transition
```

---

# Extension Point — Security Policies

Nuevas políticas de seguridad pueden evolucionar sin modificar
Integration.Version por sí mismas.

---

# Security Policy Change

Debe mantenerse:

```text
Security Policy Change

≠

Aggregate Modification
```

salvo que exista una modificación explícita del dominio.

---

# Extension Point — External Authorization Mapping

Una futura equivalencia entre autorizaciones externas y AURA puede
definirse mediante contrato explícito.

---

# Mapping no Transfiere Ownership

Debe mantenerse:

```text
External Permission

≠

Internal Permission by Default
```

---

# Extension Point — Multi-Context Interoperability

Nuevos Bounded Contexts pueden interoperar con Integration.

Esto no crea un Consistency Boundary compartido.

---

# Cross-Context Contracts

Toda nueva relación cross-context debe preservar autonomía de ambos
contextos.

---

# Extension Point — Compatibility

Toda evolución debe considerar compatibilidad semántica con hechos,
estados y contratos históricos.

---

# Historical Meaning

Debe mantenerse:

```text
Existing Historical Fact

retains

Existing Meaning
```

---

# No Historical Reinterpretation

Una extensión futura no debe reinterpretar silenciosamente:

```text
IntegrationCreated

IntegrationActivated

IntegrationSuspended

IntegrationReactivated

IntegrationArchived
```

---

# No Historical State Rewrite

Cambiar el modelo futuro no modifica los States que fueron válidos
históricamente.

---

# Extension Point — Backward Compatibility

Cuando una evolución requiera compatibilidad con consumidores
existentes, dicha compatibilidad debe definirse explícitamente en el
contrato afectado.

---

# No Compatibility Policy Assumed

Este documento no impone una estrategia concreta de:

```text
backward compatibility

forward compatibility
```

---

# Extension Point — Contract Versioning

Nuevos contratos pueden poseer su propio versionado.

---

# Contract Version Independence

Debe mantenerse:

```text
Contract Version

≠

Integration.Version
```

---

# Extension Point — Migration

Una evolución futura puede requerir migraciones técnicas.

---

# Migration no es Domain Behavior

Debe mantenerse:

```text
Technical Migration

≠

Integration Command
```

---

# Migration no Produce Domain Event por Defecto

Una migración técnica no debe producir nuevos hechos de dominio salvo
que realmente exista una nueva modificación válida definida por el
dominio.

---

# Extension Point — Rehydration

Cualquier evolución debe preservar que Rehydration no constituye una
nueva modificación.

---

# Extension Point — Replay

Cualquier evolución debe preservar:

```text
Replay

≠

New Domain Fact
```

---

# Extension Point — Projection Rebuild

Nuevas vistas deben preservar:

```text
Projection Rebuild

≠

New Aggregate Modification
```

---

# Extension Point — Testing

Toda nueva regla de dominio debe estar acompañada por escenarios de
prueba conceptuales coherentes.

---

# Nueva Regla

Debe mantenerse:

```text
New Domain Rule

requires

Corresponding Test Coverage
```

---

# Extension Point — Documentation

Toda evolución relevante debe reflejarse en los documentos del
Aggregate afectados.

---

# Coordinated Evolution

Una modificación no debe aplicarse a un único documento cuando afecta
contratos relacionados.

---

# Impact Analysis

Antes de incorporar una extensión debe revisarse su impacto sobre:

```text
Aggregate

Lifecycle

State Machine

Commands

Domain Events

Invariants

Permissions

Repository Contract

Examples

Versioning

Consistency Boundary

Integration Events

Read Model

Test Scenarios

Performance Rules

Security Model
```

---

# Extension Review

Una extensión válida debe responder:

```text
Is this a real domain concept?

Which Aggregate owns it?

Does it belong inside Integration?

Does it change Lifecycle?

Does it require a Command?

Does it produce a Domain Event?

Does it require a Permission?

Does it create or modify an Invariant?

Does it affect Versioning?

Does it affect the Consistency Boundary?

Does it require an Integration Event contract?

Does it belong only to a Read Model?

Does it expose sensitive information?

Does it depend on Infrastructure?
```

---

# Rejection Criteria

Una propuesta de extensión debe rechazarse como cambio de dominio cuando
solamente exista por:

- conveniencia técnica;
- limitación de framework;
- decisión de base de datos;
- decisión de broker;
- necesidad de logging;
- necesidad de monitoring;
- necesidad de caching;
- necesidad de retries;
- necesidad de scaling;
- estructura de API externa;
- estructura de FIWARE;
- estructura de sistema municipal.

---

# Architecture Decision Boundary

Una extensión que requiera una nueva decisión arquitectónica debe
separarse de la definición del dominio y ser evaluada explícitamente.

---

# No Architecture by Implication

Debe mantenerse:

```text
New Domain Requirement

≠

Automatic Architecture Choice
```

---

# No Infrastructure by Implication

Debe mantenerse:

```text
New Domain Requirement

≠

Automatic Infrastructure Component
```

---

# No Pattern by Implication

La aparición de una necesidad no establece automáticamente:

```text
Saga

Process Manager

Outbox

Inbox

Event Sourcing

CQRS

Broker

Cache

Schema Registry
```

---

# No Technology by Implication

Tampoco establece automáticamente:

```text
PostgreSQL

MongoDB

Kafka

RabbitMQ

NATS

FIWARE

NGSI-LD

HTTP

MQTT
```

---

# Domain First

Debe mantenerse:

```text
Domain Meaning

before

Technical Mechanism
```

---

# Extension Sequencing

Una nueva extensión debe definirse primero conceptualmente.

Solamente después puede evaluarse su materialización técnica.

---

# No Premature Implementation Detail

Los Extension Points no deben especificar detalles de implementación
antes de que exista una decisión explícita.

---

# Extension Point Stability

Los Extension Points deben mantener flexibilidad sin debilitar las
garantías actuales.

---

# Current Rules Remain Authoritative

Hasta que una extensión sea formalmente aprobada:

```text
Current Version 1.0 Rules

remain

Authoritative
```

---

# No Provisional Domain Behavior

Un comportamiento futuro no debe considerarse válido solamente porque
haya sido mencionado como posibilidad.

---

# Formal Adoption

Una extensión pasa a formar parte del dominio únicamente cuando:

- su significado ha sido definido;
- sus reglas han sido definidas;
- sus impactos han sido revisados;
- los contratos afectados han sido actualizados;
- sus Test Scenarios han sido definidos;
- no contradice Invariants vigentes sin una evolución explícita.

---

# Extension and Version 1.0

Mientras no exista una evolución formal, permanecen vigentes:

```text
States:

Draft
Active
Suspended
Archived
```

```text
Commands:

CreateIntegration
ActivateIntegration
SuspendIntegration
ReactivateIntegration
ArchiveIntegration
```

```text
Domain Events:

IntegrationCreated
IntegrationActivated
IntegrationSuspended
IntegrationReactivated
IntegrationArchived
```

```text
Permissions:

Integration.Create
Integration.Activate
Integration.Suspend
Integration.Reactivate
Integration.Archive
```

---

# Version 1.0 Repository Contract

Mientras no exista una evolución formal:

```text
IntegrationRepository

    save()

    findById()

    exists()

    delete()

    nextIdentity()
```

permanece como contrato conceptual oficial.

---

# Version 1.0 Identity

IntegrationId permanece:

```text
unique

immutable
```

dentro de las reglas vigentes.

---

# Version 1.0 Versioning

Permanece:

```text
Create

→

Version = 1
```

y:

```text
Valid Modification

→

Version N + 1
```

---

# Version 1.0 Boundary

Permanece:

```text
One IntegrationId

=

One Consistency Boundary
```

---

# Version 1.0 Integration Events

No existen nombres concretos obligatorios de Integration Events sin un
contrato explícito.

---

# Version 1.0 Read Model

Read Models permanecen derivados y sin Write Authority.

---

# Version 1.0 Security

Authentication permanece fuera del Aggregate.

Permissions protegen Commands.

Credentials y Secrets permanecen fuera del Domain Model.

---

# Version 1.0 Performance

Performance no puede modificar reglas de dominio ni ampliar el
Consistency Boundary.

---

# Future Extension Governance

Toda futura extensión debe preservar la distinción:

```text
Domain Decision

Architecture Decision

Infrastructure Decision
```

---

# Domain Decision

Una Domain Decision define:

- significado;
- ownership;
- reglas;
- comportamiento;
- consistencia.

---

# Architecture Decision

Una Architecture Decision define mecanismos estructurales para
materializar necesidades ya comprendidas.

No se decide dentro de este documento.

---

# Infrastructure Decision

Una Infrastructure Decision selecciona tecnologías concretas.

No forma parte de los Extension Points del dominio.

---

# Extension Point and ADR

Si una futura extensión requiere una decisión arquitectónica, dicha
decisión debe documentarse mediante el mecanismo de arquitectura
correspondiente.

Este documento no crea ni selecciona ADR concretos.

---

# Extension Point and Technical Debt

Una implementación provisional no debe convertirse silenciosamente en
regla del dominio.

---

# Technical Debt no Redefine Domain

Debe mantenerse:

```text
Technical Debt

≠

Domain Rule
```

---

# Compatibility with Existing Integrations

Toda extensión futura debe evaluar el impacto sobre Integration ya
existentes.

---

# Existing Integration Identity

Una extensión no debe modificar IntegrationId histórico.

---

# Existing Event Meaning

Una extensión no debe cambiar retroactivamente el significado de
Domain Events confirmados.

---

# Existing Version Meaning

Una extensión no debe reutilizar o renumerar Version históricas.

---

# Existing Archived Integrations

Archived continúa siendo terminal mientras no exista una evolución
formal del Lifecycle.

---

# No Reactivation by Extension Mention

Mencionar una posibilidad futura de reactivación de Archived no hace
válida:

```text
Archived → Active
```

---

# No New Command by Extension Mention

Mencionar una operación futura no la convierte en Command oficial.

---

# No New Event by Extension Mention

Mencionar un posible evento futuro no lo convierte en Domain Event
oficial.

---

# No New Permission by Extension Mention

Mencionar una capacidad futura no crea una Permission.

---

# No New Repository Method by Extension Mention

Mencionar una necesidad técnica futura no amplía IntegrationRepository.

---

# No New Attribute by Extension Mention

Mencionar información potencial no la convierte en Aggregate Attribute.

---

# No New Entity by Extension Mention

Mencionar una estructura futura no crea Internal Entity.

---

# No New Value Object by Extension Mention

Mencionar un tipo conceptual posible no crea Value Object.

---

# No New Integration Event by Extension Mention

Mencionar un consumidor futuro no crea Integration Event.

---

# No New Read Model by Extension Mention

Mencionar una consulta futura no define una vista contractual obligatoria.

---

# Extension Test Principle

Toda extensión aprobada debe agregar cobertura sin eliminar silenciosamente
escenarios que continúan siendo válidos.

---

# Regression Protection

Debe mantenerse:

```text
Existing Rule

+

New Extension

=

Existing Rule Preserved

unless explicitly evolved
```

---

# Extension Conflict

Si una extensión contradice una regla actual, debe tratarse como una
evolución explícita del dominio y no como una simple ampliación.

---

# Explicit Breaking Change

Un cambio incompatible debe identificarse explícitamente como cambio de
contrato.

---

# No Silent Breaking Change

Debe mantenerse:

```text
Breaking Domain Change

≠

Silent Extension
```

---

# Extension Documentation

Toda extensión aprobada debe actualizar los documentos afectados de
manera coordinada.

---

# Extension Consistency

Una extensión no puede dejar documentos oficiales describiendo reglas
incompatibles entre sí.

---

# Canonical Consistency

Debe mantenerse:

```text
Aggregate

Lifecycle

State Machine

Commands

Domain Events

Invariants

Permissions

Repository Contract

Versioning

Consistency Boundary

Integration Events

Read Model

Tests

Performance

Security

Extension Points

=

One Coherent Domain Contract
```

---

# Regla de Evaluación

Antes de aprobar cualquier extensión debe comprobarse:

```text
Does it belong to Integration?

Is it domain or infrastructure?

Is ownership clear?

Is consistency ownership clear?

Are existing invariants preserved?

Are commands explicit?

Are events explicit?

Are permissions explicit?

Is versioning impact explicit?

Is boundary impact explicit?

Are external contracts explicit?

Are security implications explicit?

Are tests defined?
```

---

# Regla de Rechazo

Si no puede justificarse como concepto real del dominio:

```text
Extension

=

Not part of Integration Domain
```

---

# Reglas Fundamentales

Los Extension Points de Integration deben cumplir:

1. Un Extension Point representa una posibilidad controlada de
   evolución.
2. Un Extension Point no representa comportamiento ya existente.
3. Ninguna extensión se infiere automáticamente.
4. Toda extensión requiere definición explícita.
5. Toda extensión debe preservar el patrón consolidado de AURA Core.
6. Los States oficiales permanecen Draft, Active, Suspended y
   Archived hasta evolución formal.
7. Nuevos States requieren definición completa de Lifecycle.
8. Nuevas transiciones requieren Source State y Target State explícitos.
9. Nuevas transiciones requieren intención explícita.
10. Los Commands oficiales actuales permanecen cerrados mientras no
    exista evolución formal.
11. Nuevos Commands requieren una intención real del dominio.
12. Acciones técnicas no crean Commands.
13. Los Domain Events actuales permanecen oficiales mientras no exista
    evolución formal.
14. Nuevos Domain Events requieren hechos reales confirmados.
15. Eventos técnicos no crean Domain Events.
16. Nuevas Invariants requieren una necesidad real de validez interna.
17. Condiciones técnicas no crean Invariants automáticamente.
18. Las Permissions actuales permanecen oficiales mientras no exista
    evolución formal.
19. Nuevas Permissions requieren nuevas capacidades reales.
20. Operaciones técnicas no crean Permissions.
21. IntegrationRepository evoluciona solamente por necesidades de
    persistencia del Aggregate.
22. Query requirements no amplían Repository automáticamente.
23. Interoperabilidad no convierte Repository en Adapter.
24. Versioning permanece independiente por IntegrationId.
25. External Version no reemplaza Integration.Version.
26. Contract Version no reemplaza Integration.Version.
27. El Consistency Boundary solamente se amplía por necesidad explícita
    de consistencia inmediata.
28. Query, performance y infrastructure no amplían el Boundary.
29. Otros Aggregates no se fusionan con Integration por conveniencia.
30. La versión 1.0 no define Internal Entities concretas.
31. Nuevas Internal Entities requieren identidad local y pertenencia al
    Aggregate.
32. Persistencia física no crea Internal Entities.
33. La versión 1.0 no define Value Objects específicos obligatorios.
34. Nuevos Value Objects requieren semántica real de dominio.
35. Tipos técnicos no crean Value Objects.
36. Integration Events concretos requieren contratos explícitos.
37. Domain Events no crean Integration Events automáticamente.
38. Los nombres de Integration Events no se infieren por convención.
39. Integration Event Contract Version permanece independiente.
40. Nuevos Read Models requieren necesidades reales de consulta.
41. Read Models no adquieren Write Authority.
42. Read Fields no crean Aggregate Attributes automáticamente.
43. Joined Read Models no fusionan Aggregate Boundaries.
44. Nuevos mecanismos de Security no crean Domain State.
45. Credentials permanecen fuera del Aggregate.
46. Secrets permanecen fuera de Domain Events e Integration Events.
47. Nuevas optimizaciones no pueden evitar reglas del dominio.
48. Performance no crea States.
49. Performance no crea Commands.
50. Performance no crea Domain Events.
51. Nuevos sistemas externos permanecen fuera del Aggregate.
52. External Models no redefinen Integration.
53. FIWARE permanece externo al Domain Model.
54. NGSI-LD no redefine automáticamente el Aggregate.
55. Sistemas municipales permanecen externos.
56. Municipal Authorization no crea Permissions automáticamente.
57. Smart City Platforms permanecen externas.
58. Protocol Changes no son Domain Changes.
59. Broker Changes no son Domain Changes.
60. Persistence Technology Changes no son Domain Changes.
61. Event Sourcing permanece compatible pero no obligatorio.
62. Adoptar Event Sourcing requiere decisión explícita.
63. CQRS permanece compatible pero no obligatorio.
64. Adoptar CQRS físico requiere decisión explícita.
65. Idempotency mechanism no está definido en versión 1.0.
66. Deduplication mechanism no está definido en versión 1.0.
67. Delivery semantics universales no están definidas en versión 1.0.
68. Global Ordering no está definido.
69. AggregateVersion no es Global Sequence.
70. Retention Policy no está definida.
71. Physical Deletion permanece separada del Lifecycle.
72. Audit permanece separado.
73. Notification permanece separado.
74. Nuevas relaciones con otros Aggregates preservan ownership.
75. CorrelationId no fusiona Boundaries.
76. CausationId no concede Authorization.
77. ActorId no es atributo obligatorio del Aggregate.
78. External Identifier no reemplaza IntegrationId.
79. Nuevos Aggregate Attributes requieren necesidad explícita.
80. API Fields no crean Aggregate Attributes automáticamente.
81. Read Fields no crean Aggregate Attributes automáticamente.
82. Technical Metadata no crea Aggregate Attributes automáticamente.
83. Nuevos timestamps requieren semántica real del dominio.
84. Analytics permanece en el Read Side.
85. Reporting permanece en el Read Side.
86. Search permanece en el Read Side.
87. Performance Thresholds no crean States.
88. Security Policy Changes no modifican Aggregate automáticamente.
89. External Authorization Mapping requiere contrato explícito.
90. Nuevos Bounded Contexts no crean Shared Consistency Boundary.
91. Historical Domain Events conservan significado.
92. Historical Versions no se renumeran.
93. Breaking Changes deben identificarse explícitamente.
94. Technical Migration no es Command.
95. Replay no crea hechos nuevos.
96. Rehydration no crea hechos nuevos.
97. Projection Rebuild no modifica Aggregate.
98. Toda nueva regla requiere Test Coverage correspondiente.
99. Toda extensión debe distinguir Domain, Architecture e
    Infrastructure.
100. Hasta aprobación formal, las reglas versión 1.0 permanecen
     autoritativas.

---

# Restricciones

No está permitido utilizar Extension Points para:

- introducir States implícitos;
- introducir transiciones implícitas;
- introducir Commands implícitos;
- introducir Domain Events implícitos;
- introducir Permissions implícitas;
- introducir Invariants implícitas;
- introducir Repository methods implícitos;
- introducir Internal Entities implícitas;
- introducir Value Objects implícitos;
- introducir Aggregate Attributes implícitos;
- introducir Integration Events sin contrato;
- introducir Read Models obligatorios sin necesidad de consulta;
- modificar Versioning por conveniencia técnica;
- ampliar Consistency Boundary por conveniencia;
- fusionar Aggregates;
- incorporar sistemas externos dentro de Integration;
- incorporar FIWARE dentro de Integration;
- incorporar modelos municipales dentro de Integration;
- convertir estados técnicos en States de dominio;
- convertir acciones técnicas en Commands;
- convertir eventos técnicos en Domain Events;
- convertir operaciones técnicas en Permissions;
- convertir estructuras de persistencia en Entities;
- convertir tipos técnicos en Value Objects;
- convertir campos de Read Model en atributos del Aggregate;
- interpretar CorrelationId como Shared Boundary;
- interpretar CausationId como Authorization;
- interpretar ActorId como Permission;
- interpretar External Identifier como IntegrationId;
- interpretar Domain Event como Integration Event automático;
- interpretar Integration Event como Command;
- interpretar External Authorization como AURA Permission automática;
- imponer Event Sourcing;
- imponer CQRS;
- imponer Saga;
- imponer Process Manager;
- imponer Transactional Outbox;
- imponer Inbox Pattern;
- imponer Dead Letter Queue;
- imponer Exactly Once;
- imponer At Least Once;
- imponer At Most Once;
- imponer Global Ordering;
- imponer broker;
- imponer protocolo;
- imponer base de datos;
- imponer cache;
- imponer Schema Registry;
- imponer framework;
- imponer FIWARE;
- imponer NGSI-LD;
- imponer arquitectura municipal;
- imponer mecanismo de Authentication;
- imponer mecanismo de Authorization;
- imponer mecanismo criptográfico;
- imponer Secret Manager;
- imponer Key Management;
- reinterpretar hechos históricos silenciosamente;
- renumerar Version históricas;
- reactivar Archived sin evolución formal;
- introducir breaking changes como simples extensiones;
- convertir deuda técnica en regla de dominio;
- tomar una decisión arquitectónica desde una posibilidad de extensión.

---

# Compatibilidad Arquitectónica

Los Extension Points de Integration son compatibles conceptualmente con:

- Domain-Driven Design;
- Aggregate Pattern;
- State Machine Pattern;
- Command Pattern;
- Domain Event Pattern;
- Repository Pattern;
- Clean Architecture;
- Hexagonal Architecture;
- SOLID;
- CQRS Compatible;
- Event-Driven Architecture;
- Event Sourcing Compatible;
- Optimistic Concurrency Control;
- consistencia eventual;
- Least Privilege;
- Data Minimization;
- High Cohesion;
- Low Coupling.

Estas compatibilidades no imponen ninguna arquitectura, patrón técnico,
framework, protocolo o tecnología concreta adicional.

---

# Definición de Éxito

Los Extension Points del Aggregate **Integration** permiten evolucionar
el dominio de manera controlada sin convertir posibilidades futuras en
reglas presentes ni introducir decisiones arquitectónicas por
inferencia.

El modelo fundamental queda expresado como:

```text
New Requirement
    │
    ▼
Domain Evaluation
    │
    ├── Does it belong to Integration?
    ├── Who owns it?
    ├── Does it change consistency?
    ├── Does it change behavior?
    ├── Does it change lifecycle?
    └── Does it require a contract?
    │
    ▼
Explicit Domain Decision
    │
    ▼
Coordinated Contract Evolution
```

mientras:

```text
Technical Requirement
    │
    ▼
Architecture / Infrastructure Evaluation
    │
    └── no automatic Domain change
```

Hasta que una extensión sea formalmente definida:

```text
Version 1.0

remains

Authoritative
```

El modelo garantiza que:

- Lifecycle no evolucione por inferencia;
- State Machine no evolucione por conveniencia técnica;
- Commands permanezcan intenciones reales del dominio;
- Domain Events permanezcan hechos reales confirmados;
- Invariants permanezcan condiciones de validez interna;
- Permissions permanezcan capacidades explícitas;
- Repository permanezca contrato de persistencia;
- Versioning permanezca lógico e independiente por Aggregate;
- Consistency Boundary permanezca acotado;
- nuevos sistemas externos no sean absorbidos por el Aggregate;
- FIWARE permanezca externo;
- sistemas municipales permanezcan externos;
- Integration Events requieran contratos explícitos;
- Read Models permanezcan sin Write Authority;
- Security permanezca separada del estado interno;
- Credentials y Secrets permanezcan fuera del Domain Model;
- Performance no debilite reglas del dominio;
- Event Sourcing permanezca opcional;
- CQRS permanezca opcional;
- idempotencia, deduplicación y delivery semantics no se definan por
  inferencia;
- Retention y Physical Deletion no se incorporen silenciosamente al
  Lifecycle;
- Audit y Notification mantengan Boundaries independientes;
- ownership se preserve en toda nueva relación;
- hechos históricos conserven su significado;
- Version históricas no se reescriban;
- cambios incompatibles sean tratados como evolución explícita;
- Test Scenarios acompañen nuevas reglas;
- Domain Decisions permanezcan separadas de Architecture Decisions;
- Architecture Decisions permanezcan separadas de Infrastructure
  Decisions;
- ninguna extensión sea considerada parte del dominio antes de su
  aprobación formal.

De esta forma, `DOMAIN-013P-Extension-Points.md` establece formalmente
los Extension Points oficiales del Aggregate **Integration** conforme
al patrón consolidado de AURA Core.