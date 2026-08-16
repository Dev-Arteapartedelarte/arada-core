# DOMAIN-013N — Integration Performance Rules

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
- DOMAIN-013O-Security-Model.md
- DOMAIN-013P-Extension-Points.md

---

# Objetivo

Este documento define formalmente las **Performance Rules**
conceptuales del Aggregate **Integration**.

Estas reglas buscan preservar:

- un Aggregate pequeño;
- un Consistency Boundary acotado;
- comportamiento determinista;
- modificaciones independientes por IntegrationId;
- separación entre Write Side y Read Side;
- independencia respecto de sistemas externos;
- evolución escalable del dominio;
- eficiencia sin sacrificar Invariants.

Las Performance Rules no introducen tecnología concreta ni modifican
las reglas funcionales del Aggregate.

---

# Principio Fundamental

Debe mantenerse:

```text
Performance Optimization

≠

Domain Rule Bypass
```

Ninguna necesidad de rendimiento puede utilizarse para evitar:

- Lifecycle;
- State Machine;
- Commands;
- Invariants;
- Permissions;
- Versioning;
- Consistency Boundary.

---

# Performance versus Correctness

Debe mantenerse:

```text
Correct Domain State

>

Performance Convenience
```

Una optimización nunca debe producir un Aggregate inválido.

---

# Performance versus Architecture

Las reglas de este documento son conceptuales.

No determinan:

- base de datos;
- broker;
- cache;
- framework;
- protocolo;
- lenguaje;
- ORM;
- Event Store;
- search engine;
- infraestructura FIWARE;
- infraestructura municipal.

---

# Aggregate Pequeño

Integration debe permanecer conceptualmente pequeño.

Debe contener solamente información necesaria para proteger sus propias
reglas.

Debe mantenerse:

```text
Integration Aggregate

=

Minimum State Required for Domain Consistency
```

---

# No Aggregate Inflado

No debe incorporarse información solamente porque esté disponible desde:

- sistemas externos;
- FIWARE;
- plataformas municipales;
- mensajes;
- APIs;
- Read Models;
- Audit;
- Notification;
- otros Aggregates.

---

# External Payload no Pertenece por Defecto

Debe mantenerse:

```text
Full External Payload

≠

Integration Aggregate State
```

---

# Source Aggregate no se Carga Dentro de Integration

Para modificar Integration no debe ser necesario incorporar como parte
interna del Aggregate:

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

# One Aggregate per Modification

Una modificación de Integration opera conceptualmente sobre:

```text
One IntegrationId
```

---

# No Global Aggregate Load

Para modificar:

```text
Integration INT-001
```

no debe ser necesario cargar:

```text
all Integration Aggregates
```

---

# No Global Consistency Requirement

Debe mantenerse:

```text
One Integration Modification

≠

Global Integration Consistency Check
```

salvo una futura regla explícita del dominio que requiera otra cosa.

---

# Independent Aggregate Boundaries

Integration con diferentes identidades deben poder evolucionar
independientemente.

Debe mantenerse:

```text
INT-001

≠

INT-002

Consistency Boundary
```

---

# No Shared Version

Diferentes IntegrationId mantienen:

```text
independent Version sequences
```

evitando una dependencia global de Versioning.

---

# Performance y Versioning

Optimizar concurrencia no permite omitir:

```text
ExpectedVersion

PersistedVersion
```

cuando corresponda.

---

# No Concurrency Bypass

Debe mantenerse:

```text
High Throughput Requirement

≠

Permission to Ignore ConcurrencyConflict
```

---

# No Silent Overwrite por Rendimiento

No puede utilizarse:

```text
Last Write Wins
```

como atajo para evitar las reglas oficiales de Versioning.

---

# Performance y Repository

IntegrationRepository debe operar sobre el Aggregate necesario para el
comportamiento solicitado.

---

# Repository no Requiere Cargar Todos los Aggregates

Debe mantenerse:

```text
findById(IntegrationId)

≠

loadAllIntegrations()
```

como necesidad conceptual.

---

# Repository Focus

El Repository del Write Model debe permanecer enfocado en:

```text
Aggregate Persistence
```

y no convertirse en:

```text
Reporting Engine

Analytics Engine

Global Search Engine
```

---

# Queries Complejas Fuera del Write Model

Necesidades de:

```text
Search

Filter

Sort

Pagination

Reporting

Analytics

Aggregation
```

pertenecen conceptualmente al Read Side.

---

# Read Model para Consultas

Debe mantenerse:

```text
Query Optimization

belongs to

Read Model
```

sin expandir el Aggregate.

---

# No Aggregate Expansion por Query

Una necesidad de consulta no autoriza añadir al Aggregate:

- colecciones de historial;
- índices conceptuales;
- agregaciones globales;
- estadísticas;
- métricas;
- información duplicada de otros Aggregates.

---

# Historial

Una necesidad de consultar historia no obliga a Integration a mantener
una colección interna completa de eventos para lectura.

Debe mantenerse:

```text
Historical Query Need

≠

Aggregate History Collection Requirement
```

---

# Reporting

Reporting no forma parte del comportamiento del Aggregate.

---

# Analytics

Analytics no forma parte del comportamiento del Aggregate.

---

# Metrics

Métricas técnicas o analíticas no forman parte del estado interno.

Debe mantenerse:

```text
Metrics

∉

Integration Aggregate
```

---

# Logs

Logs técnicos permanecen fuera del Aggregate.

---

# Monitoring

Monitoring permanece fuera del Aggregate.

---

# Observability

Observability no amplía el Consistency Boundary.

---

# Technical Health

Información como:

```text
latency

throughput

availability

error rate

health
```

no forma parte del Lifecycle de Integration.

---

# Performance Metrics no son Domain State

Debe mantenerse:

```text
Slow

Fast

Overloaded

Degraded

≠

Integration State
```

---

# No Performance State

No se introducen States como:

```text
Slow

Busy

Saturated

Throttled

Degraded
```

en el Lifecycle versión 1.0.

---

# Timeout no es State

Debe mantenerse:

```text
Timeout

≠

Integration State
```

---

# Performance Failure no Suspende Automáticamente

Debe mantenerse:

```text
Slow External Response

≠

SuspendIntegration
```

---

# Performance Recovery no Reactiva Automáticamente

Debe mantenerse:

```text
External Performance Recovery

≠

ReactivateIntegration
```

---

# External Availability

La disponibilidad de un sistema externo no forma parte de las
Invariants internas.

---

# External Latency

Debe mantenerse:

```text
External Latency

≠

Integration Lifecycle
```

---

# External Throughput

Debe mantenerse:

```text
External Throughput

≠

Integration State
```

---

# FIWARE Performance

La latencia o disponibilidad de FIWARE no redefine:

```text
Draft

Active

Suspended

Archived
```

---

# Municipal System Performance

El rendimiento de un sistema municipal tampoco redefine el Lifecycle.

---

# Performance y Commands

Los Commands oficiales permanecen:

```text
CreateIntegration

ActivateIntegration

SuspendIntegration

ReactivateIntegration

ArchiveIntegration
```

Una necesidad de rendimiento no crea Commands adicionales.

---

# No Performance Commands

No deben inferirse Commands como:

```text
OptimizeIntegration

ScaleIntegration

RefreshIntegration

WarmIntegration

PreloadIntegration

CacheIntegration

ThrottleIntegration
```

---

# No RetryIntegration por Performance

Una necesidad técnica de retry no crea:

```text
RetryIntegration
```

---

# No HealthCheckIntegration

Una necesidad de observabilidad no crea:

```text
HealthCheckIntegration
```

como Command del dominio.

---

# Performance y Domain Events

Los únicos Domain Events oficiales permanecen:

```text
IntegrationCreated

IntegrationActivated

IntegrationSuspended

IntegrationReactivated

IntegrationArchived
```

---

# No Performance Domain Events

No deben inferirse:

```text
IntegrationSlowed

IntegrationThrottled

IntegrationOverloaded

IntegrationRecovered

IntegrationScaled

IntegrationCached
```

como Domain Events.

---

# Technical Event no es Domain Event

Debe mantenerse:

```text
Technical Performance Event

≠

Integration Domain Event
```

---

# Performance y Integration Events

Un problema técnico de rendimiento no crea automáticamente un
Integration Event del dominio.

---

# No Mandatory Performance Integration Event

No se define como contrato universal:

```text
IntegrationPerformanceDegraded
```

ni equivalente.

---

# Contractual Need

Si en el futuro un contrato externo requiere información de rendimiento,
dicha necesidad debe definirse explícitamente sin modificar por
inferencia el Aggregate.

---

# Performance y Consistency Boundary

Debe mantenerse:

```text
Performance Need

≠

Consistency Boundary Expansion
```

---

# No Boundary Merge

Procesar muchas Integration no permite fusionarlas en una única unidad
de consistencia.

---

# Batch Processing

Un proceso técnico puede manejar múltiples Integration.

Cada una conserva:

```text
own IntegrationId

own State

own Version

own Invariants

own Consistency Boundary
```

---

# Batch no es Aggregate

Debe mantenerse:

```text
Technical Batch

≠

Aggregate
```

---

# Bulk Processing

Bulk Processing no crea:

```text
Global Integration Aggregate
```

---

# Bulk Mutation

Una operación técnica que recorra varias Integration debe preservar las
reglas individuales de cada Aggregate.

---

# No Shared Transaction Requirement

El dominio no exige que múltiples Integration se modifiquen dentro de
una única transacción compartida.

---

# No Global Lock Requirement

La versión 1.0 no define:

```text
Global Integration Lock
```

como requisito del dominio.

---

# No Global Version Requirement

La versión 1.0 tampoco define:

```text
Global Integration Version
```

---

# Performance y External Systems

Integration no debe incorporar dentro de su Boundary sistemas externos
para reducir llamadas o accesos técnicos.

---

# No External Snapshot por Performance

No debe almacenarse automáticamente:

```text
Full External System Snapshot
```

dentro del Aggregate con fines de optimización.

---

# No Source Aggregate Snapshot

Tampoco debe incluirse:

```text
Full Source Aggregate Snapshot
```

como estado interno por conveniencia de lectura.

---

# Reference over Embedding

Cuando exista una referencia formalmente definida, debe preservarse la
separación de ownership.

Debe mantenerse:

```text
Reference

≠

Embedded Aggregate
```

---

# Data Minimization

Mantener el Aggregate pequeño exige conservar únicamente datos
necesarios para su consistencia.

---

# No Derived Analytics State

No deben persistirse dentro del Aggregate campos como:

```text
totalRequests

averageLatency

successRate

failureRate

throughput

lastHealthCheck
```

como parte del dominio solamente por razones de performance o
observability.

---

# Derived Data

Información derivada para lectura pertenece al Read Side cuando
corresponda.

---

# Duplication for Read

Una eventual duplicación de datos para optimizar lectura no transfiere
ownership al Read Model.

---

# Read Denormalization

La desnormalización de lectura no obliga a desnormalizar el Aggregate.

Debe mantenerse:

```text
Read Denormalization

≠

Write Model Expansion
```

---

# Indexes

Este documento no define índices concretos.

---

# Search Index

La necesidad de un Search Index no modifica el Aggregate.

---

# Cache

Este documento no exige cache.

---

# Cache no es Source of Truth

Si Infrastructure utiliza cache:

```text
Cache

≠

Integration Source of Truth
```

---

# Cache Hit

Un cache hit no modifica:

```text
Integration.Version
```

---

# Cache Miss

Un cache miss tampoco modifica:

```text
Integration.Version
```

---

# Cache Invalidation

Cache invalidation no constituye Domain Command ni Domain Event.

---

# Cache Staleness

Una cache desactualizada no autoriza sobrescribir la Version
autoritativa.

---

# Read Model Cache

Un mecanismo de cache puede formar parte de Infrastructure del Read
Side.

No se establece como requisito.

---

# No Cache Policy

La versión 1.0 no define:

- TTL;
- eviction;
- refresh interval;
- prewarming;
- invalidation strategy.

---

# No Throughput Threshold

Este documento no define un umbral obligatorio de:

```text
requests per second
```

---

# No Latency Threshold

Este documento no define un límite obligatorio de:

```text
milliseconds
```

para Commands o Queries.

---

# No Storage Threshold

Este documento no define tamaños máximos físicos de:

- tablas;
- documentos;
- mensajes;
- bases de datos;
- caches.

---

# No Payload Byte Limit

Este documento no establece un tamaño técnico concreto en bytes para
Domain Events o Integration Events.

La regla conceptual permanece:

```text
Minimum Necessary Information
```

---

# Domain Event Payload

Domain Events deben mantener Payload suficiente para representar el
hecho sin convertirse en snapshots innecesarios del Aggregate.

---

# Integration Event Payload

Cuando exista un Integration Event concreto:

```text
Contractual Minimum Payload
```

debe prevalecer sobre una copia completa del Domain Model.

---

# No Full Aggregate Publication

Debe mantenerse:

```text
Integration Event Payload

≠

Full Aggregate Snapshot by Default
```

---

# Read Model Payload

Una Query debe devolver únicamente la información necesaria para su
propósito.

---

# Pagination

Grandes colecciones de resultados pueden requerir una estrategia de
paginación en el Read Side.

La estrategia concreta no se define aquí.

---

# Pagination no es Aggregate Behavior

Debe mantenerse:

```text
Pagination

≠

Integration Domain Behavior
```

---

# Sorting

Sorting pertenece al Read Side.

---

# Filtering

Filtering pertenece al Read Side.

---

# Search

Search pertenece al Read Side.

---

# Aggregation

Aggregation pertenece al Read Side.

---

# Count

Count de múltiples Integration pertenece al Read Side.

---

# Grouping

Grouping pertenece al Read Side.

---

# No Repository Analytics

No debe incorporarse al Repository del Write Model comportamiento como:

```text
countByState()

averageLatency()

groupByProvider()

calculateSuccessRate()
```

como responsabilidad del Aggregate Repository por necesidad de
reporting.

---

# No Query Optimization in Aggregate

Integration no debe mantener datos adicionales solamente para evitar
operaciones de lectura.

---

# Performance y Projection

Projection puede optimizar lectura sin modificar el Aggregate.

---

# Projection Lag

Debe aceptarse conceptualmente que Read Side pueda encontrarse
temporalmente retrasado bajo consistencia eventual.

---

# Projection Lag no Afecta Write Validity

Debe mantenerse:

```text
Projection Lag

≠

Aggregate Invalidity
```

---

# Projection Failure

Un fallo de Projection no revierte una modificación ya confirmada.

---

# Projection Retry

Un retry técnico de Projection no incrementa:

```text
Integration.Version
```

---

# Projection Rebuild

Rebuild de un Read Model no ejecuta Commands del Aggregate.

---

# Projection Rebuild no Produce Hechos Nuevos

Debe mantenerse:

```text
Projection Rebuild

≠

New Domain Fact
```

---

# Performance y Event Sourcing

Event Sourcing puede ser compatible con Integration.

No se exige por razones de performance.

---

# Event Sourcing no es Performance Requirement

Debe mantenerse:

```text
Performance Need

≠

Event Sourcing Requirement
```

---

# Snapshot

La versión 1.0 no establece Snapshot como requisito.

---

# Snapshot no Cambia Domain Rules

Si una estrategia futura utiliza snapshots:

```text
Snapshot

≠

New Aggregate State
```

---

# Replay

Una optimización de Replay no debe producir:

- nuevos Commands;
- nuevos Domain Events;
- nuevos Integration Events;
- nuevos incrementos artificiales de Version.

---

# Performance y CQRS

CQRS es compatible con la separación entre Write Side y Read Side.

No se impone por rendimiento.

---

# CQRS no es Performance Requirement

Debe mantenerse:

```text
Performance Need

≠

CQRS Requirement
```

---

# Write Side

Write Side prioriza:

```text
Domain Correctness

Aggregate Consistency

Versioning
```

---

# Read Side

Read Side puede priorizar:

```text
Query Efficiency
```

sin adquirir autoridad de escritura.

---

# Performance y Integration Events

El Aggregate no espera confirmación de consumidores externos como parte
de sus Invariants.

---

# External Consumer Lag

Puede existir:

```text
Integration.Version = N

Consumer observed Version = N - 1
```

temporalmente.

---

# Consumer Lag no es Aggregate Failure

Debe mantenerse:

```text
Consumer Lag

≠

Integration Failed State
```

---

# Consumer Failure

Consumer Failure no revierte Integration.

---

# Consumer Recovery

Consumer Recovery no reactiva Integration.

---

# Publication Latency

La latencia de publicación externa no modifica el State del Aggregate.

---

# Publication Retry

Retry de publicación no incrementa Version.

---

# Delivery Throughput

Throughput de transporte no forma parte del estado del Aggregate.

---

# Message Queue Depth

Debe mantenerse:

```text
Queue Depth

≠

Integration State
```

---

# Broker Lag

Broker Lag no suspende Integration automáticamente.

---

# External Backpressure

Una condición técnica de backpressure no introduce:

```text
Throttled
```

como Lifecycle State.

---

# No Delivery Architecture Decision

Este documento no decide:

- synchronous delivery;
- asynchronous delivery;
- push;
- pull;
- polling;
- streaming;
- webhook;
- broker.

---

# No Queue Architecture Decision

Este documento no exige Queue.

---

# No Broker Architecture Decision

Este documento no exige broker.

---

# No Outbox Architecture Decision

Este documento no exige:

```text
Transactional Outbox
```

---

# No Inbox Architecture Decision

Este documento no exige:

```text
Inbox Pattern
```

---

# No Saga Architecture Decision

Este documento no exige:

```text
Saga
```

---

# No Process Manager Architecture Decision

Este documento no exige:

```text
Process Manager
```

---

# No Load Balancer Decision

La versión 1.0 no establece un mecanismo concreto de distribución de
carga.

---

# No Horizontal Scaling Decision

Este documento no obliga una estrategia específica de escalamiento
horizontal.

---

# No Vertical Scaling Decision

Tampoco obliga escalamiento vertical.

---

# No Partitioning Decision

Este documento no define particionamiento físico.

---

# No Sharding Decision

Este documento no define sharding.

---

# No Replication Decision

Este documento no define estrategia de replicación.

---

# No Caching Decision

Este documento no define cache como requisito.

---

# No CDN Decision

Este documento no define CDN.

---

# No Search Engine Decision

Este documento no define motor de búsqueda.

---

# No Materialized View Decision

La versión 1.0 no obliga materialized views.

---

# No Database Decision

El dominio no selecciona:

```text
PostgreSQL

MongoDB

MySQL

Redis

EventStoreDB

Elasticsearch
```

---

# Repository Substitutability

Una implementación de Repository puede optimizarse siempre que preserve:

```text
IntegrationId

State

Version

CreatedAt

UpdatedAt

Invariants

Consistency Boundary
```

---

# Performance Optimization no Cambia Semántica

Dos implementaciones con diferentes características de rendimiento
deben mantener el mismo resultado conceptual para las mismas
precondiciones de dominio.

---

# Determinismo del Dominio

El resultado de un Command válido o inválido no debe depender de:

- latencia de red;
- capacidad de broker;
- tamaño de cache;
- velocidad de base de datos;
- cantidad de réplicas;
- número de workers.

---

# Domain Decision no Depende de Infraestructura

Debe mantenerse:

```text
Domain Decision

≠

Infrastructure Performance Condition
```

salvo que una futura regla explícita del dominio establezca un concepto
distinto.

---

# Performance y Security

Una optimización no puede omitir:

```text
Authentication

Authorization

Permission Evaluation
```

cuando corresponda.

---

# No Security Bypass

Debe mantenerse:

```text
Lower Latency Goal

≠

Authorization Bypass
```

---

# Performance y Secrets

Optimizar acceso no autoriza incorporar credenciales al Aggregate.

---

# No Credential Cache dentro del Aggregate

Integration no debe almacenar:

```text
AccessToken

RefreshToken

ApiKey

ClientSecret

PrivateKey

Secret
```

como estado para acelerar integraciones.

---

# Performance y Audit

Audit mantiene su propio Boundary.

Una necesidad de rendimiento no permite incorporar Audit dentro de
Integration.

---

# Performance y Notification

Notification mantiene su propio Boundary.

Una necesidad de rendimiento no permite incorporar Notification dentro
de Integration.

---

# Performance y Organization

Organization no se embebe dentro de Integration para evitar consultas.

---

# Performance y Citizen

Citizen no se embebe dentro de Integration para evitar accesos externos
al Boundary.

---

# Performance y Membership

Membership permanece independiente.

---

# Performance y Role

Role permanece independiente.

---

# Performance y Territory

Territory permanece independiente.

---

# Performance y Assembly

Assembly permanece independiente.

---

# Performance y Proposal

Proposal permanece independiente.

---

# Performance y Participation

Participation permanece independiente.

---

# Performance y Voting

Voting permanece independiente.

---

# Performance y Document

Document permanece independiente.

---

# No Cross-Aggregate Denormalization in Write Model

No deben copiarse Aggregates completos dentro de Integration para
reducir lecturas.

---

# Read Composition

Si una consulta requiere información combinada:

```text
Integration

+

Other Aggregate Information
```

dicha composición pertenece conceptualmente al Read Side cuando sea
apropiado.

---

# Joined Read Model no es Joined Aggregate

Debe mantenerse:

```text
Joined Read Model

≠

Joined Aggregate
```

---

# Performance y External Models

No se debe copiar un modelo externo completo dentro de Integration para
evitar transformación o consulta.

---

# FIWARE Entity no es Cache del Aggregate

Debe mantenerse:

```text
FIWARE Entity

≠

Integration Aggregate Cache
```

---

# External System Cache no es Source of Truth

Un cache externo no reemplaza el estado autoritativo del Aggregate.

---

# Read Side Freshness

Una necesidad de mayor frescura de lectura no autoriza:

- modificar el Aggregate desde una Projection;
- compartir el Consistency Boundary;
- omitir Versioning;
- fusionar Write Side y Read Side conceptualmente.

---

# Strong Read Requirement

Si en el futuro una Query requiere una garantía específica de
consistencia de lectura, dicha necesidad debe definirse explícitamente.

Este documento no impone una estrategia técnica.

---

# Performance Thresholds

Los objetivos cuantitativos de:

- latencia;
- throughput;
- memoria;
- CPU;
- almacenamiento;
- concurrencia;

pertenecen a requisitos no funcionales o decisiones posteriores.

No forman parte de las Invariants conceptuales de Integration en
versión 1.0.

---

# No SLO de Dominio

Este documento no establece:

```text
SLO

SLA

SLI
```

como reglas internas del Aggregate.

---

# Availability Target

La disponibilidad técnica del servicio no es un atributo del Aggregate.

---

# Capacity Target

La capacidad física tampoco pertenece al estado del dominio.

---

# Scaling Target

Un objetivo de escalamiento no modifica Lifecycle.

---

# Performance Testing

Las pruebas técnicas de rendimiento pueden validar requisitos no
funcionales.

Debe mantenerse:

```text
Performance Test

≠

Domain Test Scenario
```

aunque ambos puedan coexistir.

---

# Domain Test Scenarios

Los Test Scenarios del dominio continúan definidos en:

```text
DOMAIN-013M-Test-Scenarios.md
```

---

# Performance Test Failure

Un fallo en una prueba técnica de performance no produce:

```text
IntegrationSuspended

IntegrationArchived

IntegrationFailed
```

automáticamente.

---

# Load Test

Un Load Test no modifica el Lifecycle conceptual.

---

# Stress Test

Un Stress Test tampoco modifica State por sí mismo.

---

# Benchmark

Un benchmark no produce Domain Events.

---

# Performance Regression

Una regresión técnica puede requerir acciones de ingeniería.

No crea automáticamente nuevas reglas del Aggregate.

---

# Evolution

Las Performance Rules pueden evolucionar cuando aparezcan necesidades
reales que afecten la forma de preservar eficiencia sin romper el
dominio.

---

# Nueva Performance Rule

Una nueva regla debe responder:

```text
Does this preserve Aggregate correctness?

Does this preserve IntegrationId boundary?

Does this preserve Versioning?

Does this preserve Invariants?

Does this preserve ownership?

Does this avoid introducing Infrastructure into the Domain Model?
```

---

# Nueva Optimización

Toda optimización debe preservar:

```text
Lifecycle

State Machine

Commands

Domain Events

Invariants

Permissions

Repository Contract

Versioning

Consistency Boundary
```

---

# Nueva Query Requirement

Una nueva necesidad de consulta debe evaluarse primero como concern del
Read Side antes de ampliar el Write Model.

---

# Nuevo Payload Requirement

Una nueva necesidad de Payload debe respetar:

```text
Minimum Necessary Data
```

---

# Nueva Necesidad de Cache

Una necesidad de cache no modifica por sí misma:

- Aggregate;
- Repository Contract;
- Lifecycle;
- Domain Events;
- Versioning.

---

# Nueva Necesidad de Broker

Una necesidad de broker no crea:

- Command;
- State;
- Domain Event;
- Integration Event concreto;
- Aggregate member.

---

# Nueva Necesidad de Scaling

Una necesidad de scaling no cambia el Consistency Boundary.

---

# Nueva Necesidad de Partitioning

Una necesidad de particionamiento no crea nuevas identidades de dominio
por sí misma.

---

# Nueva Necesidad de Replication

Replication no crea una segunda Source of Truth del Aggregate.

---

# Impacto de Evolución

Toda modificación de las Performance Rules debe revisar cuando
corresponda:

```text
DOMAIN-013-Aggregate.md

DOMAIN-013E-Invariants.md

DOMAIN-013G-Repository-Contract.md

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
Performance Requirement

≠

New Domain Rule
```

y:

```text
Performance Optimization

≠

New Aggregate State
```

y:

```text
Scaling Requirement

≠

Consistency Boundary Expansion
```

y:

```text
Query Performance Requirement

≠

Write Model Expansion
```

y:

```text
Infrastructure Optimization

≠

Architectural Decision inside Domain
```

---

# Reglas Fundamentales

Las Performance Rules de Integration deben cumplir:

1. Performance no puede evitar reglas del dominio.
2. Correctness tiene prioridad sobre conveniencia de optimización.
3. Integration debe permanecer conceptualmente pequeño.
4. El Aggregate contiene solamente información necesaria para su
   consistencia.
5. External Payload no se incorpora completo por defecto.
6. Otros Aggregates no se embeben por razones de rendimiento.
7. Una modificación opera sobre un IntegrationId.
8. Modificar una Integration no requiere cargar todas las Integration.
9. Different IntegrationId mantienen Boundaries independientes.
10. Different IntegrationId mantienen Version independiente.
11. Performance no permite evitar ExpectedVersion.
12. Performance no permite evitar ConcurrencyConflict.
13. Silent Overwrite no es una optimización válida.
14. Repository permanece enfocado en persistencia del Aggregate.
15. Repository no se convierte en Reporting Engine.
16. Repository no se convierte en Analytics Engine.
17. Search pertenece al Read Side.
18. Filter pertenece al Read Side.
19. Sort pertenece al Read Side.
20. Pagination pertenece al Read Side.
21. Reporting pertenece al Read Side.
22. Analytics pertenece al Read Side.
23. Query Requirement no expande el Aggregate automáticamente.
24. Historical Query no obliga historial interno orientado a lectura.
25. Metrics no forman parte del Aggregate.
26. Logs no forman parte del Aggregate.
27. Monitoring no forma parte del Aggregate.
28. Technical Health no es Lifecycle State.
29. Latency no es Lifecycle State.
30. Throughput no es Lifecycle State.
31. Timeout no es Lifecycle State.
32. Slow External Response no suspende Integration automáticamente.
33. Performance Recovery no reactiva Integration automáticamente.
34. FIWARE Performance no redefine State.
35. Municipal System Performance no redefine State.
36. Performance Need no crea Commands.
37. Performance Need no crea Domain Events.
38. Performance Need no crea Integration Events concretos.
39. Performance Need no expande Consistency Boundary.
40. Batch Processing no fusiona Aggregates.
41. Bulk Processing no crea Global Integration Aggregate.
42. No se requiere Global Lock de dominio.
43. No se requiere Global Version.
44. External Snapshot no se incorpora por performance.
45. Source Aggregate Snapshot no se incorpora por performance.
46. Data Minimization protege el tamaño del Aggregate.
47. Derived Analytics Data pertenece al Read Side.
48. Read Denormalization no expande el Write Model.
49. Este documento no define índices concretos.
50. Este documento no exige Search Index.
51. Este documento no exige Cache.
52. Cache no es Source of Truth.
53. Cache Hit no incrementa Version.
54. Cache Miss no incrementa Version.
55. Cache Invalidation no produce Domain Event.
56. No se define Cache Policy.
57. No se define Throughput Threshold.
58. No se define Latency Threshold.
59. No se define Storage Threshold.
60. No se define Payload Byte Limit.
61. Domain Event Payload debe evitar snapshots innecesarios.
62. Integration Event Payload debe ser contractual y mínimo.
63. Query Payload debe ajustarse a la necesidad de lectura.
64. Pagination no es Aggregate Behavior.
65. Read Side puede optimizar consultas.
66. Projection Lag no invalida Integration.
67. Projection Failure no revierte Integration.
68. Projection Retry no incrementa Version.
69. Projection Rebuild no crea Domain Facts.
70. Event Sourcing no se exige por performance.
71. CQRS no se exige por performance.
72. Snapshot no se exige por performance.
73. Consumer Lag no crea Failed State.
74. Consumer Failure no revierte Integration.
75. Consumer Recovery no reactiva Integration.
76. Publication Latency no modifica State.
77. Publication Retry no incrementa Version.
78. Queue Depth no es Integration State.
79. Broker Lag no suspende Integration automáticamente.
80. Backpressure no introduce Throttled como State.
81. No se decide mecanismo de delivery.
82. No se exige Queue.
83. No se exige Broker.
84. No se exige Transactional Outbox.
85. No se exige Inbox Pattern.
86. No se exige Saga.
87. No se exige Process Manager.
88. No se exige Load Balancer concreto.
89. No se define Horizontal Scaling.
90. No se define Vertical Scaling.
91. No se define Partitioning.
92. No se define Sharding.
93. No se define Replication.
94. No se selecciona Database.
95. Repository implementations deben preservar semántica del dominio.
96. Domain Decision no depende de condiciones técnicas de performance.
97. Security no puede evitarse para reducir latencia.
98. Credentials no se incorporan al Aggregate para optimización.
99. Toda nueva optimización debe preservar el Consistency Boundary.
100. Toda evolución de Performance debe preservar el patrón consolidado
     de AURA Core.

---

# Restricciones

No está permitido:

- sacrificar Invariants por rendimiento;
- evitar State Machine por rendimiento;
- evitar Permissions por rendimiento;
- evitar Versioning por rendimiento;
- ignorar ConcurrencyConflict;
- utilizar Silent Overwrite;
- fusionar múltiples Integration en un Aggregate global;
- cargar todas las Integration como requisito conceptual para modificar
  una;
- embebir otros Aggregates por conveniencia;
- copiar External Payload completo;
- copiar Source Aggregate Snapshot completo;
- almacenar métricas dentro del Aggregate por conveniencia técnica;
- utilizar latency como Lifecycle State;
- utilizar throughput como Lifecycle State;
- utilizar Degraded como Lifecycle State;
- utilizar Throttled como Lifecycle State;
- suspender automáticamente por lentitud externa;
- reactivar automáticamente por recuperación de performance;
- crear OptimizeIntegration;
- crear ScaleIntegration;
- crear CacheIntegration;
- crear RetryIntegration;
- crear HealthCheckIntegration;
- crear Domain Events de performance no definidos;
- crear Integration Events concretos de performance sin contrato;
- ampliar el Consistency Boundary por optimización;
- fusionar Aggregates mediante Batch Processing;
- introducir Global Lock como regla del dominio;
- introducir Global Version;
- convertir Repository en Reporting Engine;
- convertir Repository en Analytics Engine;
- convertir Repository en Search Engine;
- ampliar Write Model por una necesidad de Query;
- incorporar historia completa para reporting;
- considerar Cache como Source of Truth;
- modificar Version por Cache Hit;
- modificar Version por Cache Miss;
- producir Domain Events por Cache Invalidation;
- imponer Cache;
- imponer TTL;
- imponer Search Index;
- imponer índice concreto;
- imponer threshold de latencia;
- imponer threshold de throughput;
- imponer tamaño físico de almacenamiento;
- imponer límite técnico de Payload desde el dominio;
- imponer Event Sourcing por performance;
- imponer CQRS por performance;
- imponer Snapshot;
- imponer Broker;
- imponer Queue;
- imponer Transactional Outbox;
- imponer Inbox Pattern;
- imponer Saga;
- imponer Process Manager;
- imponer Load Balancer;
- imponer sharding;
- imponer partitioning;
- imponer replication;
- imponer database;
- imponer protocolo;
- incorporar credenciales al Aggregate para acelerar operaciones;
- utilizar acceso técnico como sustituto de Authorization;
- convertir información FIWARE en estado interno por optimización;
- convertir información municipal en estado interno por optimización;
- introducir una decisión arquitectónica nueva desde una regla de
  performance.

---

# Compatibilidad Arquitectónica

Las Performance Rules de Integration son compatibles conceptualmente
con:

- Domain-Driven Design;
- Aggregate Pattern;
- Repository Pattern;
- Clean Architecture;
- Hexagonal Architecture;
- SOLID;
- CQRS Compatible;
- Event-Driven Architecture;
- Event Sourcing Compatible;
- Optimistic Concurrency Control;
- consistencia eventual;
- High Cohesion;
- Low Coupling.

Estas compatibilidades no imponen:

- CQRS físico;
- Event Sourcing;
- cache;
- broker;
- queue;
- Transactional Outbox;
- Inbox;
- Saga;
- Process Manager;
- database;
- search engine;
- sharding;
- partitioning;
- replication;
- load balancer;
- protocolo;
- framework;
- FIWARE;
- NGSI-LD;
- plataforma municipal.

---

# Definición de Éxito

Las Performance Rules del Aggregate **Integration** garantizan que las
necesidades de eficiencia puedan resolverse sin debilitar el modelo de
dominio ni ampliar artificialmente su Consistency Boundary.

El principio central queda expresado como:

```text
One IntegrationId
        │
        ▼
Small Aggregate
        │
        ▼
Local Invariants
        │
        ▼
Independent Version
        │
        ▼
Independent Consistency Boundary
```

mientras:

```text
Complex Query Need
        │
        ▼
    Read Side
```

y:

```text
External Performance Concern
        │
        ▼
  Infrastructure
        │
        └── no automatic Domain mutation
```

El modelo garantiza que:

- Integration permanezca pequeño;
- cada IntegrationId mantenga un Boundary independiente;
- cada Integration mantenga su propia Version;
- modificaciones no requieran cargar el conjunto global;
- Optimistic Concurrency no pueda omitirse;
- Repository permanezca orientado a persistencia del Write Model;
- Search, Filter, Sort, Pagination, Reporting y Analytics permanezcan
  en el Read Side;
- necesidades de consulta no amplíen el Aggregate;
- métricas, logs y monitoring permanezcan fuera del dominio;
- latencia y throughput no se conviertan en States;
- fallos de rendimiento externos no suspendan automáticamente
  Integration;
- recuperación técnica no reactive automáticamente Integration;
- Batch Processing no fusione Consistency Boundaries;
- External Payloads no inflen el Aggregate;
- Read Models puedan optimizar consultas sin adquirir Write Authority;
- Projection Lag y Projection Failure no modifiquen el Aggregate;
- Integration Events permanezcan contractuales y mínimos;
- retries técnicos no creen nuevos hechos ni incrementen Version;
- Cache no sea Source of Truth;
- Event Sourcing permanezca compatible pero no obligatorio;
- CQRS permanezca compatible pero no obligatorio;
- ninguna tecnología de scaling, cache, broker, persistencia o
  distribución sea impuesta;
- Security y Versioning no puedan evitarse para reducir latencia;
- cualquier optimización futura preserve Lifecycle, Invariants,
  ownership, Versioning y Consistency Boundary.

De esta forma, `DOMAIN-013N-Performance-Rules.md` establece
formalmente las Performance Rules oficiales del Aggregate
**Integration** conforme al patrón consolidado de AURA Core.