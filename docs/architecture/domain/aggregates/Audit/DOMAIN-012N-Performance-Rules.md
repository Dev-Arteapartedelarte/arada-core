# DOMAIN-012N — Audit Performance Rules

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Audit Management

Aggregate:
Audit

Documentos relacionados:

- DOMAIN-012-Aggregate.md
- DOMAIN-012A-Lifecycle.md
- DOMAIN-012B-State-Machine.md
- DOMAIN-012C-Commands.md
- DOMAIN-012D-Domain-Events.md
- DOMAIN-012E-Invariants.md
- DOMAIN-012F-Permissions.md
- DOMAIN-012G-Repository-Contract.md
- DOMAIN-012H-Examples.md
- DOMAIN-012I-Versioning.md
- DOMAIN-012J-Consistency-Boundary.md
- DOMAIN-012K-Integration-Events.md
- DOMAIN-012L-Read-Model.md
- DOMAIN-012M-Test-Scenarios.md
- DOMAIN-012O-Security-Model.md
- DOMAIN-012P-Extension-Points.md

---

# Objetivo

Este documento define formalmente las **Performance Rules**
conceptuales del Aggregate **Audit**.

Las Performance Rules establecen restricciones y principios para
preservar eficiencia operativa sin debilitar:

- Aggregate Boundary;
- Lifecycle;
- State Machine;
- Commands;
- Domain Events;
- Invariants;
- Permissions;
- Versioning;
- Consistency Boundary;
- Security;
- trazabilidad histórica.

Performance no constituye una autorización para modificar reglas del
dominio.

---

# Principio Fundamental

Debe mantenerse:

```text
Performance Optimization

≠

Domain Rule Bypass
```

y:

```text
Faster Execution

≠

Weaker Domain Integrity
```

Toda optimización debe preservar exactamente el significado
conceptual de Audit.

---

# Performance y Dominio

Las reglas de Performance pertenecen al diseño conceptual del
Aggregate únicamente en cuanto protegen:

- tamaño del Consistency Boundary;
- costo del comportamiento de escritura;
- independencia entre Aggregates;
- separación entre Write Side y Read Side;
- crecimiento histórico;
- trazabilidad;
- escalabilidad conceptual.

No definen una tecnología concreta.

---

# Aggregate Pequeño

Audit debe mantener un Consistency Boundary pequeño.

Una unidad Audit representa:

```text
One AuditId

=

One Independent Audit Aggregate
```

No debe incorporar colecciones históricas de otros Audit dentro de
la misma Aggregate Root.

---

# No Aggregate Global

No debe modelarse:

```text
GlobalAudit
    └── All Audit Records
```

como una única unidad de consistencia para responder consultas
históricas.

Debe mantenerse:

```text
Global History Requirement

≠

Global Aggregate
```

---

# Una Unidad Audit por Consistency Boundary

Cada Audit mantiene:

```text
AuditId

State

Version

Traceability Information

CreatedAt

UpdatedAt
```

dentro de su propio Boundary.

El comportamiento sobre una unidad Audit no debe requerir cargar
otros Audits para preservar sus Invariants actuales.

---

# No Carga de Historial Global

`RecordAudit` no debe requerir cargar:

```text
Entire Audit History
```

para crear una nueva unidad.

Debe mantenerse:

```text
RecordAudit

operates on

One Audit Aggregate
```

---

# No Carga del Source Aggregate Completo

Audit no debe cargar el Aggregate originador completo por el solo
hecho de registrar trazabilidad.

Debe mantenerse:

```text
Source Reference

≠

Source Aggregate Load Requirement
```

Audit utiliza únicamente la información necesaria conforme al
contrato recibido.

---

# Source Aggregate fuera del Boundary

No deben incorporarse dentro de Audit:

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

Integration
```

con el objetivo de evitar consultas o reducir llamadas externas.

Performance no justifica expandir el Aggregate.

---

# No Embedding por Performance

Debe mantenerse:

```text
Performance Convenience

≠

Aggregate Ownership
```

No está permitido embebir Aggregates externos completos para evitar
acceso posterior.

---

# Referencias Mínimas

Audit debe conservar únicamente información necesaria del hecho de
origen.

Puede incluir, cuando corresponda:

```text
SourceAggregateId

SourceAggregateType

SourceEventId

SourceEventType

SourceAggregateVersion

ActorId

SourceOccurredAt

CorrelationId

CausationId
```

sin incorporar estructuras externas completas.

---

# Payload Mínimo

Debe mantenerse:

```text
Audit Data

=

Minimum Necessary Traceability Information
```

Un Payload mayor no es automáticamente un Payload mejor.

---

# Source Payload

No debe copiarse automáticamente:

```text
Entire Source Payload
```

dentro de Audit.

Esto protege:

- tamaño del Aggregate;
- minimización;
- Security;
- persistencia;
- procesamiento;
- desacoplamiento.

---

# Domain Event Payload

`AuditRecorded` debe mantener un Payload mínimo y significativo.

Debe mantenerse:

```text
Domain Event Payload

≠

Aggregate Snapshot
```

---

# Integration Event Payload

`AuditRecordedIntegrationEvent` también debe transportar solamente
información necesaria para su contrato.

Debe mantenerse:

```text
Integration Payload

≠

Full Audit Aggregate
```

---

# Write Path

El Write Path debe mantenerse conceptualmente pequeño.

Para versión 1.0:

```text
RecordAudit
    │
    ▼
Validate
    │
    ▼
No Audit → Recorded
    │
    ▼
Version = 1
    │
    ▼
AuditRecorded
    │
    ▼
Persist
```

No debe incluir responsabilidades de consulta masiva, reporting o
analytics.

---

# Write Side no Ejecuta Analytics

Debe mantenerse:

```text
Audit Write Model

≠

Analytics Engine
```

`RecordAudit` no debe calcular:

- estadísticas globales;
- conteos históricos;
- rankings;
- tendencias;
- dashboards;
- agregaciones analíticas.

---

# Write Side no Ejecuta Reporting

Debe mantenerse:

```text
RecordAudit

≠

Generate Historical Report
```

Reporting pertenece al Read Side.

---

# Write Side no Ejecuta Búsquedas Históricas

El Command:

```text
RecordAudit
```

no debe ejecutar búsquedas amplias del historial para construir su
propio estado.

Las reglas actuales de Audit no requieren una consulta global del
historial para validar el Lifecycle:

```text
No Audit → Recorded
```

---

# Repository

`AuditRepository` persiste una unidad Audit.

Debe mantenerse:

```text
Repository Operation

scoped to

Aggregate Boundary
```

El Repository no debe transformarse en motor de:

- analytics;
- reporting;
- búsquedas históricas;
- agregaciones;
- timelines globales.

---

# save()

`save()` debe operar conceptualmente sobre una única unidad Audit.

Debe mantenerse:

```text
save(Audit)

≠

save(All Audits)
```

---

# findById()

`findById()` debe recuperar conceptualmente una unidad por:

```text
AuditId
```

sin requerir reconstruir todo el historial global de Audit.

---

# exists()

`exists()` debe representar una verificación de existencia.

No requiere conceptualmente recuperar toda la representación Audit
cuando únicamente se necesita conocer existencia.

---

# nextIdentity()

`nextIdentity()` no debe requerir cargar Audit Aggregates existentes
dentro del dominio.

La estrategia concreta de generación permanece fuera del Aggregate.

---

# Repository y Consultas

Consultas por:

```text
SourceAggregateId

SourceEventId

ActorId

CorrelationId

CausationId

SourceAggregateType

SourceEventType

Time Range
```

pertenecen al Read Side.

---

# Read Side

El crecimiento histórico de Audit debe resolverse mediante Read
Models apropiados.

Debe mantenerse:

```text
Large Historical Query

→

Read Model
```

y no:

```text
Large Historical Query

→

Load Many Audit Aggregates into One Transaction
```

---

# Read Model Optimizado

El Read Model puede optimizarse para:

- búsqueda;
- filtros;
- ordenamiento;
- paginación;
- timelines;
- correlación;
- causalidad;
- reporting;
- analytics.

Estas optimizaciones no modifican el Aggregate.

---

# Denormalización de Lectura

Los Read Models pueden utilizar denormalización cuando sea útil.

Debe mantenerse:

```text
Read Denormalization

≠

Write Aggregate Expansion
```

---

# Índices

Los mecanismos de lectura pueden utilizar índices sobre información
como:

```text
AuditId

SourceAggregateId

SourceEventId

SourceAggregateType

SourceEventType

ActorId

CorrelationId

CausationId

SourceOccurredAt

CreatedAt
```

La estrategia concreta pertenece a Infrastructure.

---

# Índices no son Invariants

Debe mantenerse:

```text
Search Index

≠

Domain Invariant
```

Un índice puede optimizar lectura.

No redefine el dominio.

---

# Paginación

La navegación sobre grandes volúmenes debe utilizar paginación en el
Read Side cuando corresponda.

Debe mantenerse:

```text
Pagination

∈

Read Side
```

No constituye comportamiento de Audit.

---

# Sorting

El ordenamiento de resultados pertenece al Read Side.

No debe incorporarse a:

```text
RecordAudit
```

ni a las Invariants del Aggregate.

---

# Filtering

Los filtros pertenecen a lectura.

Debe mantenerse:

```text
Filter

≠

Aggregate Behavior
```

---

# Full-Text Search

Si una necesidad futura requiere:

```text
Full-Text Search
```

debe resolverse mediante infraestructura o Read Models apropiados.

No modifica el Aggregate.

---

# Timeline

Una línea temporal global puede construirse como proyección.

Debe mantenerse:

```text
Timeline

≠

Global Transaction
```

---

# Correlation View

Una vista por:

```text
CorrelationId
```

puede agrupar múltiples Audits.

Debe mantenerse:

```text
Shared CorrelationId

≠

Shared Consistency Boundary
```

---

# Causation View

Una vista causal puede recorrer hechos relacionados mediante:

```text
CausationId
```

sin cargar todos los Aggregates dentro de una transacción de
escritura.

---

# Source History View

Una vista histórica por:

```text
SourceAggregateId
```

puede reunir múltiples Audit.

Debe mantenerse:

```text
Source History View

≠

Source Aggregate Embedded in Audit
```

---

# Batch Processing

Múltiples hechos auditables pueden procesarse en batch a nivel
técnico.

Sin embargo:

```text
Batch Processing

≠

One Aggregate Transaction
```

Cada Audit conserva su propio Consistency Boundary.

---

# Bulk Audit

Un flujo que procese:

```text
Fact A

Fact B

Fact C
```

puede producir:

```text
Audit A

Audit B

Audit C
```

como unidades independientes.

No debe crearse:

```text
One Huge Audit Aggregate
```

para reducir operaciones técnicas.

---

# Atomicidad por Aggregate

Cada unidad debe preservar atomicidad interna.

Debe mantenerse:

```text
Performance

≠

Partial Aggregate Commit
```

---

# No Commit Parcial

Una optimización no puede confirmar:

```text
AuditId

without

Valid State
```

ni:

```text
State

without

Valid Version
```

ni cualquier estado parcial incompatible con las Invariants.

---

# Versioning

Ninguna optimización puede omitir:

```text
Audit.Version
```

cuando corresponda al contrato del Aggregate.

---

# Optimistic Concurrency

El control de concurrencia no puede eliminarse por razones de
Performance cuando exista una escritura sobre una unidad persistida
que requiera validar:

```text
ExpectedVersion

=

PersistedVersion
```

---

# Concurrency Check

Debe mantenerse:

```text
Faster Write

≠

Skip Concurrency Validation
```

---

# ConcurrencyConflict

Un:

```text
ConcurrencyConflict
```

debe preservarse como resultado conceptual cuando corresponda.

No debe sobrescribirse silenciosamente estado confirmado para reducir
latencia.

---

# No Last-Write-Wins Implícito

Este documento no autoriza una política:

```text
Last Write Wins
```

que ignore Versioning.

Cualquier estrategia futura distinta requeriría una definición
explícita.

---

# Domain Events

La producción de:

```text
AuditRecorded
```

no debe eliminarse para optimizar escritura cuando dicho evento forme
parte del comportamiento oficial.

---

# Domain Event Mínimo

El evento debe contener información suficiente para representar el
hecho, pero no información innecesaria.

Debe mantenerse:

```text
Small Meaningful Event

preferred over

Full Aggregate Snapshot
```

como principio conceptual.

---

# Event Sourcing

Event Sourcing permanece compatible pero no obligatorio.

Performance no puede utilizarse como justificación para imponer:

```text
Event Sourcing
```

si no existe una decisión arquitectónica explícita.

---

# State Persistence

Persistencia de estado también permanece compatible.

El dominio no selecciona una estrategia física basándose en estas
reglas.

---

# Replay

Si se utiliza Event Sourcing, Replay puede ser costoso en grandes
historiales.

Sin embargo, cualquier optimización técnica debe preservar:

```text
Same AuditId

Same State

Same Version

Same Domain Meaning
```

---

# Snapshot

Snapshots pueden existir como optimización técnica cuando la
arquitectura los utilice.

Debe mantenerse:

```text
Snapshot

≠

New Domain Fact
```

y:

```text
Snapshot

≠

Version Increment
```

---

# Snapshot no Modifica Lifecycle

Crear o utilizar un snapshot no produce:

```text
Recorded → Another State
```

---

# Cache

Cache puede utilizarse como optimización técnica.

Debe mantenerse:

```text
Cache

≠

Domain Authority
```

y:

```text
Cache Miss

≠

Audit Not Found
```

necesariamente.

---

# Cache no Modifica Version

Agregar, refrescar o eliminar una entrada de cache no modifica:

```text
Audit.Version
```

---

# Cache no Modifica State

Debe mantenerse:

```text
Cache Eviction

≠

Audit Deletion
```

y:

```text
Cache Refresh

≠

Audit Modification
```

---

# Replica

Réplicas pueden existir para optimizar disponibilidad o lectura.

La topología física no modifica el modelo.

Debe mantenerse:

```text
Replica Lag

≠

Audit Domain State Change
```

---

# Replica Desactualizada

Una réplica temporalmente desactualizada no redefine:

```text
Audit.Version
```

autoritativa.

---

# Projection Performance

Las proyecciones pueden procesarse de forma asíncrona.

Debe mantenerse:

```text
Audit Commit

≠

Projection Must Complete in Same Transaction
```

---

# Projection Lag

Puede existir:

```text
Audit committed

+

Read Model not yet updated
```

como condición válida.

Esto permite desacoplar rendimiento de escritura de rendimiento de
lectura.

---

# Projection Failure

Un fallo en una proyección no debe ralentizar conceptualmente la
validez del Aggregate ya confirmado mediante rollback.

Debe mantenerse:

```text
Projection Failure

≠

Audit Rollback
```

---

# Projection Retry

Un retry de proyección permanece fuera del Aggregate.

No produce:

```text
Audit.Version + 1
```

---

# Rebuild de Proyecciones

Un Read Model puede reconstruirse sin bloquear conceptualmente el
Write Model como requisito del dominio.

Debe mantenerse:

```text
Read Model Rebuild

≠

Audit Modification
```

---

# Integration Performance

La publicación hacia otros sistemas permanece fuera del Consistency
Boundary.

Debe mantenerse:

```text
External Consumer Latency

≠

Audit Commit Latency Requirement
```

como principio de desacoplamiento conceptual.

---

# Publicación Posterior al Commit

El hecho:

```text
AuditRecordedIntegrationEvent
```

puede publicarse después del commit correspondiente.

Audit no debe esperar conceptualmente la confirmación de todos los
consumidores externos para considerar válido su propio estado.

---

# Consumer Latency

Un consumidor lento no modifica:

```text
AuditStatus

Audit.Version
```

---

# Consumer Failure

Un consumidor fallido no genera:

```text
AuditStatus = Failed
```

---

# Retry de Integration

Retries de publicación pueden ocurrir externamente.

Debe mantenerse:

```text
Integration Retry

≠

Audit Lifecycle Transition
```

---

# Outbox

Cuando se utilice Transactional Outbox, su propósito puede contribuir
a desacoplar persistencia y publicación.

Sin embargo:

```text
Outbox

≠

Audit Aggregate
```

y su utilización no es impuesta por este documento.

---

# Outbox Performance

Estados técnicos de Outbox como:

```text
Pending

Published

Failed

Retrying
```

no deben incorporarse a Audit para optimizar coordinación.

---

# Eventual Consistency

La consistencia eventual permite desacoplar:

```text
Source Aggregate

Audit

Read Models

Integration Consumers
```

sin ampliar el Consistency Boundary.

---

# Source Commit y Audit Commit

Debe mantenerse:

```text
Source Commit

≠

Audit Commit
```

Performance no justifica fusionarlos en una transacción
multi-Aggregate obligatoria.

---

# No Distributed Transaction Obligatoria

El dominio no requiere:

```text
Distributed Transaction
```

para garantizar la validez de Audit.

---

# No Cross-Aggregate Lock

Debe mantenerse:

```text
Audit Operation

≠

Lock Source Aggregate
```

como requisito del dominio.

---

# No Lock Global

Audit no requiere un lock global sobre todo el historial para crear
una nueva unidad.

Debe mantenerse:

```text
RecordAudit

≠

Global Audit Lock
```

---

# Independencia entre AuditId

Diferentes AuditId deben poder procesarse conceptualmente de forma
independiente.

Debe mantenerse:

```text
Audit A

independent from

Audit B
```

dentro de sus respectivos Consistency Boundaries.

---

# Parallelism

El modelo permite que unidades Audit distintas sean procesadas
concurrentemente porque no comparten Consistency Boundary por
definición.

Esto no elimina las reglas de concurrencia aplicables a una misma
identidad.

---

# Same AuditId

Operaciones concurrentes sobre el mismo AuditId deben respetar:

```text
Versioning

+

Optimistic Concurrency
```

cuando corresponda.

---

# Different AuditId

Operaciones sobre:

```text
AUD-A

AUD-B
```

no deben requerir consistencia transaccional compartida solamente
porque pertenezcan al mismo Bounded Context.

---

# CorrelationId y Performance

Agrupar información por:

```text
CorrelationId
```

debe resolverse en lectura.

No debe producir una Aggregate Root que cargue todo el flujo.

---

# CausationId y Performance

Reconstruir una cadena causal debe resolverse mediante Read Models o
mecanismos de consulta.

No debe expandir el Aggregate.

---

# ActorId y Performance

Consultar todos los Audits de un actor pertenece al Read Side.

`RecordAudit` no debe cargar el historial completo de ActorId para
registrar un nuevo hecho salvo futura regla explícita.

La versión 1.0 no introduce dicha regla.

---

# SourceEventId y Performance

Las consultas por SourceEventId pertenecen a lectura o coordinación
correspondiente.

El Aggregate no debe transformarse en un índice global de Source
Events.

---

# SourceAggregateId y Performance

Consultar el historial de un SourceAggregateId pertenece al Read Side.

Debe mantenerse:

```text
SourceAggregate History

≠

Audit Aggregate Collection
```

---

# Historical Growth

Audit puede crecer en cantidad de unidades a lo largo del tiempo.

Debe mantenerse:

```text
More Audit Records

≠

Larger Individual Audit Aggregate
```

---

# Growth by Count

El crecimiento esperado ocurre conceptualmente en:

```text
Number of Audit Aggregates
```

no en:

```text
Size of One Global Audit Aggregate
```

---

# Large History

Grandes historiales deben consultarse mediante proyecciones.

No deben cargarse en la Aggregate Root para:

- filtrar;
- paginar;
- ordenar;
- agrupar;
- reportar.

---

# Historical Integrity versus Performance

Ninguna optimización puede eliminar información necesaria para
preservar el significado histórico de Audit.

Debe mantenerse:

```text
Smaller Storage

≠

Loss of Required Domain Meaning
```

---

# Compresión

Una técnica de compresión física, cuando exista, pertenece a
Infrastructure.

No puede cambiar:

- AuditId;
- State;
- Version;
- referencias;
- significado histórico.

---

# Archiving Técnico

Un mecanismo técnico de almacenamiento histórico no crea:

```text
AuditStatus = Archived
```

---

# Retención

Performance no puede utilizarse para inferir una política de
retención.

Este documento no define:

- expiración;
- retención mínima;
- retención máxima;
- eliminación automática;
- anonimización;
- redacción.

---

# Eliminación por Volumen

El crecimiento de volumen no autoriza automáticamente:

```text
DeleteAudit
```

Debe mantenerse:

```text
Storage Pressure

≠

Domain Deletion Permission
```

---

# Repository.delete()

La existencia de:

```text
Repository.delete()
```

no constituye una estrategia de Performance definida por el dominio.

Su utilización requiere una política aplicable explícita.

---

# Security y Performance

Performance no puede evitar:

- Authentication en la capa correspondiente;
- Authorization;
- minimización;
- protección de información sensible;
- Permissions;
- validación de Invariants.

Debe mantenerse:

```text
Security Check

≠

Optional for Performance
```

---

# Authorization Cache

Si una capa externa utiliza optimizaciones para Authorization, esto
no modifica:

```text
Audit Permission Semantics
```

ni introduce información de seguridad dentro del Aggregate.

---

# Sensitive Data

Evitar copiar información sensible innecesaria contribuye tanto a:

- Security;
- minimización;
- Performance.

Sin embargo, la decisión primaria continúa siendo preservar el
contrato correcto del dominio.

---

# Logging

Logs de alto volumen deben permanecer fuera del Aggregate.

Debe mantenerse:

```text
Audit

≠

Logging System
```

Esto evita convertir Audit en almacenamiento indiscriminado de
actividad técnica.

---

# Metrics

Metrics no deben incorporarse a cada Audit como estado interno por
motivos de observabilidad.

Debe mantenerse:

```text
Metrics

∉

Audit Aggregate
```

---

# Traces

Traces técnicos permanecen fuera de Audit.

CorrelationId puede utilizarse para trazabilidad conceptual cuando
corresponda, pero Audit no almacena automáticamente un trace técnico
completo.

---

# Observability

Observability puede medir:

- latencia;
- throughput;
- errores;
- tamaño de colas;
- tiempo de proyección;

sin convertir dichos valores en atributos del Aggregate.

---

# Performance Metrics no son Domain State

Debe mantenerse:

```text
Latency

Throughput

Queue Depth

CPU Usage

Memory Usage

≠

Audit Domain State
```

---

# Timeouts

Un timeout técnico no produce:

```text
AuditStatus = Failed
```

---

# Retry

Un retry técnico utilizado por razones de resiliencia o Performance
no constituye:

```text
RetryAudit
```

ni:

```text
AuditRetried
```

---

# Queue

Una cola puede utilizarse para desacoplar procesamiento técnico.

Su estado:

```text
Queued

Processing

Retrying

DeadLettered
```

permanece fuera de AuditStatus.

---

# Queue Depth

La profundidad de una cola es una métrica operacional.

No constituye una Invariant del Aggregate.

---

# Backpressure

Los mecanismos técnicos de backpressure pertenecen a Application o
Infrastructure.

No introducen nuevos estados en Audit.

---

# Rate Limiting

Rate Limiting puede proteger sistemas técnicos.

No constituye una transición ni una Invariant de Audit.

Debe mantenerse:

```text
Rate Limit

≠

Audit Domain State
```

---

# Throttling

Throttling pertenece a operación técnica.

No modifica:

```text
AuditStatus

Audit.Version
```

---

# Bulk Read

Bulk Read debe resolverse desde el Read Side cuando corresponda.

No requiere construir un Aggregate que contenga múltiples Audit.

---

# Bulk Export

Bulk Export pertenece al Read Side o Application.

No modifica Audit.

---

# Dashboard

Dashboards deben alimentarse desde Read Models o proyecciones.

No deben consultar cada Aggregate individual como requisito conceptual
del dominio.

---

# Analytics

Analytics puede utilizar:

```text
Read Models

Integration Events

Derived Data
```

según el contrato correspondiente.

No debe transformar el Aggregate Audit en un modelo analítico.

---

# FIWARE

Performance de FIWARE permanece fuera del Aggregate.

Audit no modifica sus reglas para adaptarse a:

```text
NGSI-LD

Context Broker

Orion
```

---

# FIWARE Batch

Si Integration utiliza operaciones batch hacia FIWARE, esto no
fusiona múltiples Audit en una única unidad de dominio.

---

# Sistemas Municipales

Restricciones de latencia, throughput o payload de una plataforma
municipal deben resolverse en Integration.

No deben modificar:

- AuditId;
- State;
- Version;
- Invariants;
- Consistency Boundary.

---

# Anti-Corruption Layer

Una optimización en la traducción de contratos externos no puede
hacer que el modelo externo reemplace el Audit Domain Model.

Debe mantenerse:

```text
Faster Mapping

≠

Domain Model Replacement
```

---

# Serialization

La estrategia de serialización puede optimizar tamaño o velocidad.

Sin embargo:

```text
Serialization Format

≠

Domain Meaning
```

---

# Database

La base de datos puede optimizar:

- índices;
- almacenamiento;
- particionamiento;
- replicación;
- cache;

sin modificar el modelo conceptual de Audit.

---

# Partitioning

Una estrategia de particionamiento físico no modifica:

```text
AuditId

Audit.Version

AuditStatus
```

ni crea nuevos Consistency Boundaries conceptuales.

---

# Sharding

Sharding, cuando exista, pertenece a Infrastructure.

Debe mantenerse:

```text
Physical Shard

≠

Domain Aggregate Boundary
```

---

# Replication

Replication no crea nuevas identidades Audit.

Varias copias físicas continúan representando la misma identidad
lógica cuando corresponda.

---

# Read Replica

Una Read Replica puede utilizarse para consultas.

Su eventual desactualización no modifica el Write Model.

---

# Materialized View

Una Materialized View puede implementar un Read Model.

Debe mantenerse:

```text
Materialized View

≠

Audit Aggregate
```

---

# Search Engine

Un motor de búsqueda puede implementar capacidades del Read Side.

Debe mantenerse:

```text
Search Engine

≠

Source of Truth for Audit
```

---

# Query Cache

Una Query Cache puede optimizar lectura.

Su invalidación no modifica Audit.

---

# Eventual Read Consistency

Las optimizaciones de lectura pueden aceptar:

```text
Eventual Consistency
```

conforme al contrato del Read Model.

No deben utilizarse para redefinir el estado de escritura.

---

# Performance de RecordAudit

`RecordAudit` debe operar solamente con la información necesaria para:

- validar el hecho auditable;
- preservar Invariants;
- establecer AuditId;
- establecer Recorded;
- establecer Version;
- preservar trazabilidad;
- producir AuditRecorded.

No debe adquirir responsabilidades ajenas.

---

# Complejidad Conceptual de RecordAudit

El comportamiento no debe crecer proporcionalmente al número total
de Audits existentes por una necesidad de consulta histórica.

Debe mantenerse:

```text
RecordAudit Complexity

independent from

Total Audit History Query Size
```

como objetivo conceptual.

---

# Historical Query Complexity

Las consultas históricas pueden crecer con el volumen de datos, pero
deben ser responsabilidad de mecanismos de lectura especializados.

---

# Isolation of Write Performance

La latencia de:

- dashboards;
- reportes;
- analytics;
- consumidores externos;
- proyecciones;

no debe formar parte de la validez interna del Command RecordAudit.

---

# No Synchronous External Dependency Obligatoria

La versión 1.0 no define que `RecordAudit` deba esperar
sincrónicamente una respuesta de:

```text
FIWARE

Municipal System

Analytics

Notification

Read Model

External Consumer
```

para considerar válido su propio estado.

---

# Consistencia Interna Prioritaria

Debe mantenerse:

```text
Internal Audit Consistency

before

External Propagation
```

---

# Graceful External Delay

Un retraso externo no cambia:

```text
Recorded
```

una vez que Audit fue confirmado.

---

# Performance y Domain Events Históricos

Un volumen alto de eventos no autoriza a reinterpretar, fusionar o
eliminar hechos históricos desde el dominio.

Cualquier política física requiere una definición independiente.

---

# Event Compaction

Este documento no define:

```text
Event Compaction
```

como regla de dominio.

Si una infraestructura utiliza una técnica similar, debe preservar
el significado histórico requerido por el modelo.

---

# Event Pruning

Este documento no autoriza:

```text
Event Pruning
```

como consecuencia automática de Performance.

---

# Historical Rewrite Prohibido

Debe mantenerse:

```text
Performance Optimization

≠

Historical Rewrite
```

---

# Performance y Corrective Facts

Un nuevo Source Fact correctivo puede generar otra unidad Audit.

No debe modificar un Audit anterior para reducir la cantidad de
registros.

---

# No Consolidación Destructiva

No debe reemplazarse:

```text
Audit A

Audit B
```

por:

```text
Audit C
```

que elimine el significado histórico de A y B por una necesidad de
optimización.

---

# Read Aggregation

Si se necesita una vista consolidada:

```text
Audit A + Audit B → Consolidated Read View
```

dicha consolidación pertenece al Read Side.

---

# Performance y Extensions

Una futura extensión del Aggregate no debe incorporarse dentro de
Audit solamente para evitar una llamada, join o consulta.

Debe evaluarse conforme a:

- identidad propia;
- Lifecycle;
- Invariants;
- necesidad de consistencia;
- ownership.

---

# Extension Point no es Performance Shortcut

Debe mantenerse:

```text
Extension Point

≠

Permission to Expand Aggregate for Convenience
```

---

# Performance y Domain Evolution

Una nueva necesidad de escala no crea automáticamente:

- nuevos estados;
- nuevos Commands;
- nuevos Domain Events;
- nuevas Internal Entities;
- nuevos Value Objects;
- nuevos Consistency Boundaries.

---

# Technology Independence

Las Performance Rules no imponen:

```text
PostgreSQL

MongoDB

Redis

Kafka

RabbitMQ

Elasticsearch

OpenSearch

EventStoreDB

FIWARE

Cloud Provider
```

ni tecnologías equivalentes.

---

# Infrastructure Optimization

Infrastructure puede evolucionar independientemente siempre que
preserve:

```text
AuditId

Lifecycle

State Machine

Commands

Domain Events

Invariants

Versioning

Consistency Boundary

Historical Meaning
```

---

# Performance Tests Conceptuales

Los escenarios deben verificar que grandes volúmenes no requieran
conceptualmente:

```text
loading all Audits

loading complete Source Aggregates

expanding one Audit Aggregate

global transactional lock

cross-Aggregate transaction

synchronous external consumer confirmation
```

para ejecutar comportamiento válido.

---

# Test de Aggregate Size

Debe poder verificarse conceptualmente que un nuevo Audit no aumenta
el tamaño interno de otro Audit existente.

Debe mantenerse:

```text
Create Audit B

≠

Grow Audit A
```

---

# Test de Historical Growth

Un crecimiento:

```text
1 Audit

100 Audits

1,000,000 Audits
```

no cambia conceptualmente el Lifecycle de cada unidad individual.

---

# Test de Projection Lag

Debe verificarse:

```text
Audit Commit

before

Read Model Update
```

sin requerir rollback por demora de proyección.

---

# Test de External Latency

Debe verificarse conceptualmente:

```text
Slow Consumer

≠

Invalid Audit
```

---

# Test de Retry

Debe verificarse:

```text
Technical Retry

does not change

Audit.Version
```

por el solo hecho de reintentar.

---

# Test de Cache

Debe verificarse:

```text
Cache Eviction

does not delete

Audit
```

---

# Test de Read Scaling

Debe verificarse que:

```text
filtering

sorting

pagination

reporting

analytics
```

permanezcan fuera del Write Model.

---

# Test de Batch

Debe verificarse:

```text
Batch of N Source Facts

=

N Independent Audit Boundaries
```

cuando cada hecho produzca una unidad Audit independiente.

---

# Test de Security

Debe verificarse que optimizaciones no:

- eliminen Authorization;
- eviten Invariants;
- expongan secretos;
- copien Payloads completos innecesariamente;
- amplíen el Aggregate.

---

# Test de Technology Replacement

Cambiar infraestructura debe preservar exactamente las reglas del
dominio.

Conceptualmente:

```text
Infrastructure A

    ↓ replace

Infrastructure B
```

debe mantener:

```text
Same Audit Semantics
```

---

# Reglas Fundamentales

Las Performance Rules de Audit deben cumplir:

1. Performance no puede evitar reglas de dominio.
2. Audit debe mantener un Consistency Boundary pequeño.
3. Cada AuditId representa una unidad independiente.
4. No existe un Aggregate global de Audit.
5. RecordAudit no carga el historial global.
6. RecordAudit no requiere cargar el Source Aggregate completo.
7. Referencias externas no justifican embedding.
8. Payloads deben mantenerse mínimos.
9. Source Payload no se copia automáticamente.
10. Domain Event Payload no es Aggregate Snapshot.
11. Integration Event Payload no es Aggregate Snapshot.
12. Write Side no ejecuta Analytics.
13. Write Side no ejecuta Reporting.
14. Write Side no ejecuta búsquedas históricas globales.
15. AuditRepository persiste una unidad Aggregate.
16. findById() recupera una identidad sin cargar historial global.
17. exists() no requiere cargar todo el Aggregate cuando no sea
    necesario conceptualmente.
18. Consultas históricas pertenecen al Read Side.
19. Read Models pueden optimizar búsqueda y navegación.
20. Denormalización de lectura no amplía el Aggregate.
21. Índices pertenecen a Infrastructure.
22. Paginación pertenece al Read Side.
23. Sorting pertenece al Read Side.
24. Filtering pertenece al Read Side.
25. Full-Text Search pertenece al Read Side.
26. Timeline no crea transacción global.
27. Correlation View no crea Consistency Boundary compartido.
28. Causation View no amplía Audit.
29. Batch Processing no fusiona Aggregates.
30. Bulk Processing conserva atomicidad por AuditId.
31. Performance no permite commits parciales.
32. Versioning no puede omitirse por optimización.
33. Optimistic Concurrency no puede evitarse cuando corresponda.
34. ConcurrencyConflict no puede ignorarse para acelerar escrituras.
35. Last-Write-Wins no se infiere como política del dominio.
36. AuditRecorded no puede eliminarse del comportamiento oficial por
    Performance.
37. Domain Events deben utilizar Payload mínimo significativo.
38. Event Sourcing permanece opcional.
39. State Persistence permanece compatible.
40. Replay optimizado debe preservar el mismo estado y Version.
41. Snapshot no es un nuevo hecho.
42. Snapshot no incrementa Version.
43. Cache no es autoridad de dominio.
44. Cache Eviction no elimina Audit.
45. Replica Lag no modifica estado de dominio.
46. Projection puede ser eventual.
47. Projection Lag no invalida Audit.
48. Projection Failure no produce rollback.
49. Projection Retry no incrementa Audit.Version.
50. Read Model Rebuild no modifica Audit.
51. External Consumer Latency no modifica Audit.
52. Consumer Failure no produce AuditStatus Failed.
53. Integration Retry no es transición.
54. Outbox permanece fuera del Aggregate.
55. Eventual Consistency no amplía el Boundary.
56. Source Commit y Audit Commit permanecen independientes.
57. No existe Distributed Transaction obligatoria.
58. No existe Cross-Aggregate Lock obligatorio.
59. No existe Global Audit Lock.
60. Distintos AuditId pueden procesarse independientemente.
61. Same AuditId debe respetar Versioning y Concurrency.
62. Historical Growth aumenta la cantidad de Audits, no el tamaño de
    una única Aggregate Root global.
63. Grandes historiales se consultan mediante Read Models.
64. Performance no puede destruir significado histórico.
65. Compresión física no modifica semántica.
66. Archivado técnico no crea AuditStatus Archived.
67. Performance no define retención.
68. Storage Pressure no autoriza DeleteAudit.
69. Repository.delete() no constituye una regla de Performance del
    dominio.
70. Security no puede evitarse por Performance.
71. Logs permanecen fuera del Aggregate.
72. Metrics permanecen fuera del Aggregate.
73. Traces permanecen fuera del Aggregate.
74. Performance Metrics no son Domain State.
75. Timeout no crea AuditStatus Failed.
76. Retry técnico no crea RetryAudit.
77. Queue State no es AuditStatus.
78. Backpressure permanece fuera del dominio.
79. Rate Limiting permanece fuera del dominio.
80. Bulk Read y Bulk Export pertenecen al Read Side.
81. Dashboards utilizan Read Models.
82. Analytics utiliza proyecciones o contratos externos.
83. FIWARE Performance permanece fuera del Aggregate.
84. Sistemas municipales no alteran el modelo por sus restricciones
    técnicas.
85. Serialización no modifica significado.
86. Partitioning no modifica el Aggregate Boundary.
87. Sharding no crea Domain Boundaries.
88. Replication no crea nuevas identidades.
89. Materialized Views no son Aggregates.
90. Search Engines no son Source of Truth.
91. RecordAudit debe mantener un Write Path pequeño.
92. La complejidad de RecordAudit no debe depender de consultas sobre
    todo el historial.
93. Read workloads permanecen desacoplados del Write Model.
94. No existe dependencia externa sincrónica obligatoria para validar
    Audit.
95. Consistencia interna se confirma antes de propagación externa.
96. Event Compaction no se define como regla de dominio.
97. Event Pruning no se autoriza por Performance.
98. Nuevos Source Facts no consolidan destructivamente Audits previos.
99. Consolidaciones pertenecen al Read Side.
100. Nuevas necesidades de escala no introducen arquitectura de
     dominio automáticamente.

---

# Restricciones

No está permitido:

- expandir Audit para optimizar una consulta;
- crear un Aggregate global para historial;
- cargar todos los Audit para ejecutar RecordAudit;
- cargar Aggregates externos completos por conveniencia;
- copiar Source Payload completo automáticamente;
- utilizar Aggregate Snapshot como Domain Event Payload por defecto;
- utilizar Aggregate Snapshot como Integration Event Payload por
  defecto;
- ejecutar Analytics desde RecordAudit;
- ejecutar Reporting desde RecordAudit;
- ejecutar búsquedas globales desde el Write Model;
- utilizar AuditRepository como Analytics Repository;
- utilizar AuditRepository como Search Engine;
- fusionar múltiples AuditId en una transacción por batch;
- confirmar parcialmente un Aggregate;
- omitir Versioning para acelerar escritura;
- omitir Optimistic Concurrency cuando corresponda;
- ignorar ConcurrencyConflict;
- imponer Last-Write-Wins sin definición explícita;
- eliminar Domain Events oficiales por optimización;
- imponer Event Sourcing;
- convertir Snapshot en Domain Fact;
- convertir Cache en Source of Truth;
- convertir Cache Eviction en eliminación de Audit;
- convertir Projection Lag en inconsistencia del Aggregate;
- realizar rollback de Audit por fallo de proyección;
- esperar consumidores externos como requisito de consistencia
  interna;
- convertir Consumer Failure en AuditStatus Failed;
- convertir Outbox State en AuditStatus;
- crear una Distributed Transaction obligatoria;
- crear Global Lock para Audit;
- utilizar SourceAggregateVersion como Audit Version de concurrencia;
- eliminar hechos históricos por presión de almacenamiento sin una
  regla explícita;
- inferir retención, archivado o eliminación por Performance;
- evitar Authorization o Security checks;
- incorporar logs, metrics o traces al Aggregate por conveniencia;
- convertir estados de queue en estados de Audit;
- convertir timeouts en estados de Audit;
- utilizar FIWARE o restricciones municipales para redefinir el
  Aggregate;
- utilizar una tecnología específica como regla conceptual de
  Performance;
- consolidar destructivamente varios Audits en uno solo;
- introducir nuevos estados, Commands, Events o Boundaries por una
  necesidad técnica de escala.

---

# Compatibilidad Arquitectónica

Las Performance Rules de Audit son compatibles con:

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
- Transactional Outbox;
- consistencia eventual;
- Projection Pattern;
- Materialized Views;
- Persistence Ignorance;
- Horizontal Scaling;
- High Cohesion;
- Low Coupling.

Estas compatibilidades no imponen una tecnología concreta ni
introducen nuevas reglas de arquitectura dentro del dominio.

---

# Definición de Éxito

Las Performance Rules del Aggregate **Audit** garantizan que la
trazabilidad pueda crecer sin ampliar innecesariamente el
Consistency Boundary ni debilitar las reglas del dominio.

El modelo establece que:

```text
One AuditId

=

One Small Independent Aggregate
```

y que el crecimiento histórico ocurre principalmente como:

```text
More Audit Aggregates

+

Specialized Read Models
```

no como:

```text
One Ever-Growing Global Aggregate
```

Las reglas garantizan que:

- Audit permanezca pequeño;
- RecordAudit opere sobre una sola unidad;
- el Source Aggregate completo no sea necesario dentro del Boundary;
- Payloads permanezcan mínimos;
- búsquedas históricas, filtros, sorting, paginación, reporting y
  Analytics permanezcan en el Read Side;
- grandes volúmenes no amplíen el Write Model;
- Batch Processing no fusione Consistency Boundaries;
- Versioning y Optimistic Concurrency no sean sacrificados por
  velocidad;
- Domain Events conserven su significado;
- Event Sourcing continúe siendo compatible pero no obligatorio;
- Snapshot, Cache, Replica y Projection permanezcan optimizaciones
  externas al dominio;
- Projection Lag y Consumer Lag sean compatibles con consistencia
  eventual;
- fallos externos no produzcan rollback del Aggregate;
- Source Commit y Audit Commit permanezcan independientes;
- no exista una transacción distribuida obligatoria;
- diferentes AuditId puedan evolucionar independientemente;
- crecimiento histórico no cambie el Lifecycle de las unidades;
- presión de almacenamiento no introduzca retención o eliminación no
  definidas;
- Security e Invariants no puedan evitarse por Performance;
- logs, metrics, traces, queues y timeouts permanezcan fuera del
  Domain Model;
- FIWARE y sistemas municipales permanezcan desacoplados;
- optimizaciones físicas de almacenamiento o lectura no cambien el
  significado de Audit;
- cualquier futura evolución orientada a escala preserve identidad,
  Invariants, Versioning, Consistency Boundary y significado
  histórico.

De esta forma, `DOMAIN-012N-Performance-Rules.md` establece las
Performance Rules oficiales del Aggregate **Audit** conforme al
patrón consolidado de AURA Core.