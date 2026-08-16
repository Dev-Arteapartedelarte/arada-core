# DOMAIN-012L — Audit Read Model

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
- DOMAIN-012M-Test-Scenarios.md
- DOMAIN-012N-Performance-Rules.md
- DOMAIN-012O-Security-Model.md

---

# Objetivo

Este documento define formalmente el **Read Model** asociado al
Aggregate **Audit**.

El Read Model representa información derivada y optimizada para
consulta.

Su propósito es permitir explorar la trazabilidad preservada por
Audit sin utilizar el Aggregate de escritura como motor de:

- búsqueda;
- filtrado;
- ordenamiento;
- paginación;
- historial;
- reporting;
- análisis.

Debe mantenerse:

```text
Audit Aggregate

≠

Audit Read Model
```

---

# Principio Fundamental

Audit constituye la autoridad de escritura sobre su propio estado.

El Read Model constituye una representación derivada para consulta.

Debe mantenerse:

```text
Write Model

=

Domain Authority
```

mientras:

```text
Read Model

=

Query Projection
```

---

# CQRS

El modelo de Audit es compatible con:

```text
CQRS
```

Conceptualmente:

```text
Write Side

RecordAudit
    │
    ▼
Audit
    │
    ▼
AuditRecorded
```

separado de:

```text
Read Side

AuditRecorded
    │
    ▼
Projection
    │
    ▼
Audit Read Model
```

---

# Separación Write Side / Read Side

Debe mantenerse:

```text
Audit Write Model

≠

Audit Read Model
```

El Write Model protege:

- State Machine;
- Invariants;
- Version;
- Consistency Boundary;
- Domain Behavior.

El Read Model optimiza:

- consultas;
- filtros;
- navegación histórica;
- presentación;
- análisis de trazabilidad.

---

# Autoridad

El Read Model no constituye fuente autoritativa para modificar Audit.

Debe mantenerse:

```text
Read Model

≠

Write Authority
```

y:

```text
Projection

≠

Aggregate Root
```

---

# Fuente de Verdad

La fuente de verdad de Audit permanece en:

```text
Audit Aggregate
```

y, cuando la estrategia de persistencia corresponda:

```text
Audit Domain Event History
```

El Read Model es derivado.

---

# Reconstrucción

Un Read Model puede reconstruirse desde hechos confirmados.

Debe mantenerse:

```text
Read Model

=

Rebuildable Projection
```

La reconstrucción no modifica Audit.

---

# Fuente de Proyección

La versión 1.0 define:

```text
AuditRecorded
```

como único Domain Event oficial.

Por lo tanto, una proyección puede reaccionar a:

```text
AuditRecorded
```

para incorporar una unidad Audit al Read Side.

---

# Proyección de AuditRecorded

Conceptualmente:

```text
AuditRecorded
    │
    ▼
Audit Projection
    │
    ▼
Audit Read Model
```

La proyección no ejecuta:

```text
RecordAudit
```

ni modifica el Aggregate.

---

# Información Conceptual

Un Audit Read Model puede representar conceptualmente información
como:

```text
AuditId

AuditStatus

SourceAggregateId

SourceAggregateType

SourceEventId

SourceEventType

SourceAggregateVersion

ActorId

SourceOccurredAt

CreatedAt

UpdatedAt

Version

CorrelationId

CausationId
```

únicamente cuando dichos elementos:

- existan en Audit;
- sean necesarios para la consulta;
- sean permitidos por Security;
- respeten minimización.

---

# AuditId

AuditId puede utilizarse en el Read Model para identificar la unidad
Audit representada.

Debe mantenerse:

```text
ReadModel.AuditId

=

Audit.AuditId
```

para la unidad proyectada.

---

# AuditStatus

La versión 1.0 solamente puede proyectar como estado de Audit:

```text
Recorded
```

El Read Model no puede introducir estados como:

```text
Draft

Pending

Active

Failed

Cancelled

Archived

Deleted
```

como estados del Aggregate.

---

# SourceAggregateId

Cuando exista:

```text
SourceAggregateId
```

puede utilizarse para localizar Audits relacionados con un Aggregate
originador.

Esto no convierte al Read Model en propietario del Source Aggregate.

---

# SourceAggregateType

Puede utilizarse:

```text
SourceAggregateType
```

para clasificar o filtrar trazabilidad según el tipo conceptual del
Aggregate originador.

---

# SourceEventId

Cuando exista:

```text
SourceEventId
```

puede utilizarse para localizar la representación Audit asociada a
un hecho de origen.

Debe mantenerse:

```text
SourceEventId

≠

AuditId
```

---

# SourceEventType

Cuando corresponda:

```text
SourceEventType
```

puede utilizarse para consultas por tipo de hecho auditado.

---

# SourceAggregateVersion

Puede proyectarse:

```text
SourceAggregateVersion
```

cuando sea útil para trazabilidad.

Debe mantenerse:

```text
SourceAggregateVersion

≠

Audit.Version
```

---

# ActorId

Cuando esté disponible y permitido:

```text
ActorId
```

puede utilizarse para consultas relacionadas con el actor del hecho
auditado.

ActorId no implica que el Read Model incorpore Citizen completo.

---

# SourceOccurredAt

Cuando Audit preserve:

```text
SourceOccurredAt
```

el Read Model puede utilizarlo para ordenar o filtrar hechos según el
momento de ocurrencia del Source Fact.

---

# CreatedAt

CreatedAt puede utilizarse para representar el momento de creación de
la unidad Audit.

Debe mantenerse:

```text
CreatedAt

≠

SourceOccurredAt
```

semánticamente.

---

# UpdatedAt

Cuando exista:

```text
UpdatedAt
```

puede proyectarse.

Su presencia no introduce una nueva transición del Lifecycle.

---

# Version

El Read Model puede conservar:

```text
Audit.Version
```

para:

- trazabilidad;
- control de orden de proyección;
- detección de lag;
- reconstrucción coherente.

---

# ReadModel.Version

Cuando una proyección represente la Version procesada:

```text
ReadModel.Version
```

debe corresponder conceptualmente a la última AggregateVersion
aplicada para esa identidad.

No constituye autoridad sobre:

```text
Audit.Version
```

---

# CorrelationId

Cuando esté disponible:

```text
CorrelationId
```

puede permitir consultar hechos pertenecientes a un mismo flujo
lógico.

Debe mantenerse:

```text
Shared CorrelationId

≠

Shared Aggregate
```

---

# CausationId

Cuando esté disponible:

```text
CausationId
```

puede utilizarse para reconstruir relaciones causales entre hechos.

No constituye ownership ni autoridad de escritura.

---

# Consultas por AuditId

El Read Side puede soportar conceptualmente:

```text
Find Audit by AuditId
```

Esta consulta devuelve una representación de lectura.

No ejecuta:

```text
RecordAudit
```

ni modifica Version.

---

# Consultas por SourceAggregateId

Puede soportarse:

```text
Find Audits by SourceAggregateId
```

para obtener trazabilidad asociada a un Aggregate originador.

---

# Consultas por SourceAggregateType

Puede soportarse:

```text
Find Audits by SourceAggregateType
```

para agrupar o filtrar hechos según su origen conceptual.

---

# Consultas por SourceEventId

Puede soportarse:

```text
Find Audits by SourceEventId
```

cuando dicha identidad esté disponible.

La existencia de esta consulta no establece una regla de unicidad
adicional no definida por el dominio.

---

# Consultas por SourceEventType

Puede soportarse:

```text
Find Audits by SourceEventType
```

para navegación histórica.

---

# Consultas por ActorId

Puede soportarse:

```text
Find Audits by ActorId
```

cuando la política de acceso permita dicha consulta.

---

# Consultas por CorrelationId

Puede soportarse:

```text
Find Audits by CorrelationId
```

para reconstruir un flujo distribuido.

---

# Consultas por CausationId

Puede soportarse:

```text
Find Audits by CausationId
```

para reconstruir relaciones causales.

---

# Consultas Temporales

El Read Side puede permitir filtros temporales basados en información
disponible como:

```text
SourceOccurredAt

CreatedAt
```

sin confundir el significado de ambos timestamps.

---

# Ordenamiento

El Read Model puede ordenar resultados según necesidades de consulta.

Ejemplos conceptuales:

```text
SourceOccurredAt

CreatedAt

AuditId
```

cuando correspondan.

El criterio concreto de presentación pertenece al Read Side.

---

# Orden Lógico

Dentro de una misma identidad Audit, la evolución lógica se preserva
mediante:

```text
Version
```

No debe inferirse un orden global obligatorio entre todos los Audits.

---

# No Orden Global

Debe mantenerse:

```text
Per Aggregate Version

≠

Global Audit Sequence
```

Las vistas que requieran una línea temporal global pueden construir
una representación derivada.

---

# Historial

El Read Side puede proporcionar:

```text
Audit History
```

para facilitar navegación y análisis.

Este historial es una representación derivada.

No constituye un Aggregate global.

---

# Timeline

Puede existir un Read Model orientado a:

```text
Cross-Aggregate Timeline
```

utilizando referencias de trazabilidad.

Debe mantenerse:

```text
Timeline View

≠

Shared Consistency Boundary
```

---

# Correlation View

Puede existir una proyección que agrupe hechos mediante:

```text
CorrelationId
```

para visualizar un flujo.

La agrupación no fusiona los Aggregates involucrados.

---

# Causation View

Puede existir una representación derivada de relaciones:

```text
Cause

↓

Effect
```

utilizando CausationId cuando la información disponible lo permita.

---

# Source Aggregate History View

Puede existir una vista que reúna Audit relacionados con:

```text
SourceAggregateId
```

Conceptualmente:

```text
SourceAggregateId = X

    │
    ├── Audit A
    ├── Audit B
    └── Audit C
```

Cada Audit continúa siendo un Aggregate independiente.

---

# Actor History View

Cuando esté permitido, puede existir una vista derivada que reúna
hechos asociados a:

```text
ActorId
```

Esta vista no convierte Actor en una entidad interna de Audit.

---

# Read Models Conceptuales

La versión 1.0 puede soportar conceptualmente vistas como:

```text
AuditDetailView

AuditHistoryView

AuditSourceHistoryView

AuditCorrelationView
```

como proyecciones de lectura.

Estas denominaciones representan capacidades conceptuales de
consulta y no nuevos Aggregates.

---

# AuditDetailView

Puede representar una unidad Audit específica.

Puede contener, según corresponda:

```text
AuditId

AuditStatus

Source References

Traceability Information

Version

CreatedAt
```

conforme a Security y minimización.

---

# AuditHistoryView

Puede representar un conjunto de unidades Audit ordenadas conforme a
criterios de consulta.

No constituye una única unidad transaccional.

---

# AuditSourceHistoryView

Puede agrupar hechos asociados a:

```text
SourceAggregateId
```

sin cargar ni modificar el Source Aggregate.

---

# AuditCorrelationView

Puede representar hechos relacionados mediante:

```text
CorrelationId
```

sin alterar ninguna identidad Audit.

---

# No AuditGlobalAggregate

La existencia de:

```text
AuditHistoryView
```

no justifica crear:

```text
AuditGlobalAggregate
```

Debe mantenerse:

```text
Global Query Need

≠

Global Consistency Boundary
```

---

# Paginación

Los resultados históricos pueden requerir paginación.

La paginación pertenece al Read Side.

Debe mantenerse:

```text
Pagination

≠

Aggregate Behavior
```

---

# Filtrado

Los filtros pertenecen al Read Side.

Pueden utilizar información proyectada como:

```text
SourceAggregateType

SourceEventType

ActorId

CorrelationId

CausationId

SourceOccurredAt

CreatedAt
```

cuando corresponda.

---

# Búsqueda

Las capacidades de búsqueda no forman parte del Aggregate de
escritura.

Debe mantenerse:

```text
Audit Aggregate

≠

Audit Search Engine
```

---

# Full-Text Search

Si una futura proyección requiere búsqueda textual, dicha capacidad
permanece en el Read Side.

No introduce comportamiento nuevo en Audit.

---

# Reporting

Los reportes históricos deben construirse desde Read Models o
proyecciones apropiadas.

Debe mantenerse:

```text
Reporting

≠

Aggregate Behavior
```

---

# Analytics

Audit Aggregate no constituye un motor analítico.

Debe mantenerse:

```text
Audit Aggregate

≠

Historical Analytics Engine
```

Analytics puede consumir Read Models o hechos publicados según el
contrato correspondiente.

---

# Agregaciones

Contadores, agrupaciones y estadísticas pertenecen al Read Side.

Ejemplos conceptuales:

```text
count by SourceAggregateType

count by SourceEventType

count by period
```

no modifican Audit.

---

# Projection Lag

Puede existir una ventana temporal donde:

```text
Audit committed

+

Read Model not yet updated
```

Debe mantenerse:

```text
Projection Lag

≠

Audit Inconsistency
```

---

# Consistencia Eventual

El Read Model puede mantener:

```text
Eventual Consistency
```

respecto del Write Model.

Una proyección temporalmente desactualizada no modifica el estado
real del Aggregate.

---

# Version y Projection Lag

Cuando el Read Model proyecte Version, puede utilizarla para detectar:

```text
ReadModel.Version < Audit.Version
```

cuando exista una evolución con más de una Version.

La versión 1.0 mantiene actualmente:

```text
Audit.Version = 1
```

después de la creación válida.

---

# Actualización de Proyección

Una proyección procesa un hecho confirmado.

Conceptualmente:

```text
AuditRecorded
    │
    ▼
Apply Projection
    │
    ▼
Read Model Updated
```

Esta actualización:

- no ejecuta RecordAudit;
- no modifica AuditStatus;
- no incrementa Audit.Version;
- no modifica CreatedAt;
- no produce AuditRecorded.

---

# Idempotencia de Proyección

Un mismo Domain Event puede ser entregado más de una vez a una
proyección.

El Read Side debe poder evitar que una entrega duplicada represente
un nuevo hecho.

Debe mantenerse:

```text
Same EventId

=

Same Domain Event
```

---

# Duplicate Delivery

Una entrega duplicada de:

```text
AuditRecorded
```

no debe producir una segunda unidad lógica en la proyección por el
solo hecho de repetirse el transporte.

---

# Orden de Proyección

Cuando existan múltiples eventos para una identidad Audit en una
evolución futura, la proyección debe respetar:

```text
AggregateVersion
```

para mantener orden lógico por Aggregate.

---

# Evento Fuera de Orden

Si una proyección recibe eventos fuera de orden, no debe reinterpretar
arbitrariamente la evolución del Aggregate.

La estrategia técnica concreta permanece fuera del dominio.

---

# Rebuild

Un Read Model puede reconstruirse desde:

```text
Audit Domain Events
```

o desde una fuente de estado autoritativa compatible, según la
arquitectura de persistencia.

Debe mantenerse:

```text
Rebuild

≠

New Domain Behavior
```

---

# Rebuild no Incrementa Version

Reconstruir una proyección no incrementa:

```text
Audit.Version
```

---

# Rebuild no Produce Domain Events

Reconstruir Read Models no produce:

```text
AuditRecorded
```

nuevamente.

---

# Repository del Aggregate

`AuditRepository` pertenece al Write Side.

Su propósito es persistir y recuperar el Aggregate.

Debe mantenerse:

```text
AuditRepository

≠

Audit Read Query Repository
```

---

# Query Repository

El Read Side puede utilizar un mecanismo de consulta especializado.

Su existencia no modifica el contrato:

```text
AuditRepository
```

definido para el Aggregate.

---

# Repository Contract

Consultas históricas complejas no deben añadirse al Repository del
Aggregate solamente para satisfacer necesidades de presentación.

Debe mantenerse:

```text
Write Repository

=

Aggregate Persistence
```

mientras:

```text
Read Query Mechanism

=

Optimized Retrieval
```

---

# Read Model no Ejecuta Commands

Ningún Read Model puede ejecutar directamente:

```text
RecordAudit
```

como consecuencia de una consulta.

Debe mantenerse:

```text
Query

≠

Command
```

---

# Read Model no Modifica State

Una vista no puede modificar:

```text
AuditStatus
```

ni introducir estados nuevos.

---

# Read Model no Modifica Version

Una consulta o actualización de proyección no puede incrementar:

```text
Audit.Version
```

---

# Read Model no Modifica AuditId

El Read Model no puede reasignar:

```text
AuditId
```

dentro del Write Model.

---

# Read Model no Modifica Source Fact

Una proyección no posee autoridad para modificar:

```text
Source Aggregate

Source Domain Event

Source Fact
```

---

# Read Model no Produce AuditRecorded

AuditRecorded solamente es producido por comportamiento válido del
Aggregate.

La proyección no puede generar dicho evento como hecho de Audit.

---

# Read Model e Integration Events

Los Read Models internos pueden consumir:

```text
AuditRecorded
```

directamente dentro del Bounded Context.

No existe obligación de utilizar:

```text
AuditRecordedIntegrationEvent
```

para una proyección interna.

---

# Read Models Externos

Un sistema externo puede construir una proyección desde:

```text
AuditRecordedIntegrationEvent
```

cuando exista un contrato explícito.

Dicha proyección no constituye el Read Model interno autoritativo de
AURA.

---

# Domain Event versus Integration Event

Debe mantenerse:

```text
Internal Read Projection

may consume

Domain Event
```

mientras:

```text
External Projection

may consume

Integration Event
```

según el contrato aplicable.

---

# Event Sourcing

Si Audit utiliza Event Sourcing:

```text
AuditRecorded
```

puede servir tanto para reconstruir el Aggregate como para construir
proyecciones.

Estas responsabilidades permanecen conceptualmente separadas.

---

# Event Stream versus Read Model

Debe mantenerse:

```text
Domain Event Stream

≠

Read Model
```

El primero preserva hechos.

El segundo representa una vista derivada.

---

# Snapshot

Un snapshot del Aggregate no es un Read Model por definición.

Debe mantenerse:

```text
Aggregate Snapshot

≠

Query Projection
```

aunque una implementación pueda utilizar estructuras técnicas
similares.

---

# Cache

Una cache de consultas puede utilizarse como optimización.

Debe mantenerse:

```text
Cache

≠

Read Model Authority
```

y:

```text
Cache

≠

Aggregate Authority
```

---

# Index

Índices técnicos pueden optimizar consultas.

No forman parte del Domain Model.

Debe mantenerse:

```text
Search Index

≠

Audit Aggregate
```

---

# Denormalización

Los Read Models pueden utilizar información denormalizada para
facilitar consultas.

Debe mantenerse:

```text
Read Model Denormalization

≠

Aggregate Embedding
```

La denormalización de lectura no cambia el Consistency Boundary de
Audit.

---

# Datos de Otros Aggregates

Una proyección puede combinar información derivada de múltiples
contextos cuando exista una necesidad de consulta.

Esto no convierte dichos Aggregates en entidades internas de Audit.

---

# Cross-Aggregate Read Model

Puede existir una vista que combine hechos de:

```text
Assembly

Voting

Document

Notification

Audit
```

para una necesidad de lectura.

Debe mantenerse:

```text
Cross-Aggregate Read Model

≠

Cross-Aggregate Transaction
```

---

# Organization

Un Read Model puede mostrar información relacionada con Organization
si el contrato de lectura dispone de ella.

Audit no adquiere ownership sobre Organization.

---

# Citizen

Un Read Model puede mostrar una representación relacionada con
ActorId.

La proyección no convierte Citizen en parte del Aggregate Audit.

---

# Membership

La información de Membership puede combinarse en una vista externa o
compuesta cuando corresponda.

Esto no modifica Membership ni Audit.

---

# Role

Una vista puede resolver información relacionada con Role mediante
mecanismos externos.

El Read Model de Audit no administra Role.

---

# Territory

Una proyección puede incorporar contexto territorial cuando exista
una necesidad de lectura explícita.

Territory permanece fuera del Consistency Boundary.

---

# Assembly

Puede construirse una vista histórica de hechos Audit relacionados
con:

```text
AssemblyId
```

mediante SourceAggregateId cuando corresponda.

Assembly no se carga ni modifica desde Audit.

---

# Proposal

Puede consultarse trazabilidad de Proposal desde Read Models sin
modificar Proposal.

---

# Participation

Puede consultarse trazabilidad de Participation sin compartir
transacción con Audit.

---

# Voting

Un Read Model puede exponer hechos auditables relacionados con
Voting.

No puede:

- registrar votos;
- modificar votos;
- alterar resultados;
- cambiar VotingStatus.

---

# Document

Una proyección puede exponer referencias documentales cuando sean
necesarias.

No se convierte en:

```text
Document Archive
```

---

# Notification

Una vista puede mostrar hechos relacionados con Notification.

No puede cambiar:

```text
NotificationStatus

Notification.Version
```

---

# Integration

Read Models no administran Integration.

Pueden ser consumidores o fuentes de consulta para procesos externos
según contratos separados.

---

# Security

Todo Read Model debe respetar:

```text
DOMAIN-012O-Security-Model.md
```

La capacidad de proyectar información no implica derecho universal
de lectura.

---

# Read Permission

Debe mantenerse:

```text
Read Permission

≠

Write Permission
```

Un actor autorizado para:

```text
RecordAudit
```

no obtiene automáticamente acceso a todos los Read Models.

---

# Write Permission

Del mismo modo, poseer permiso de lectura no concede:

```text
RecordAudit Permission
```

---

# Visibilidad

Diferentes consumidores pueden disponer de diferentes vistas según
las políticas de acceso aplicables.

El Aggregate no modifica su estado para representar diferencias de
visibilidad.

---

# Public Read Model

La versión 1.0 no establece que exista un Read Model público
universal de Audit.

La exposición pública requiere definición explícita.

---

# Internal Read Model

La existencia de un Read Model interno tampoco implica acceso
irrestricto.

Las políticas de Authorization permanecen aplicables.

---

# Minimización

Debe mantenerse:

```text
Aggregate Data

≠

Automatic Read Model Data
```

Cada vista debe contener únicamente la información necesaria para su
propósito.

---

# ActorId y Minimización

ActorId no debe proyectarse en todas las vistas por defecto.

Su inclusión depende de:

- finalidad;
- necesidad;
- Permission;
- Security;
- minimización.

---

# Datos Sensibles

Un Read Model no debe contener automáticamente información sensible
solamente porque esté disponible en fuentes internas.

---

# Credenciales

No deben proyectarse:

```text
Password

AccessToken

RefreshToken

ApiKey

PrivateKey

Secret
```

como datos de Audit Read Models.

---

# Source Payload

Un Read Model no debe exponer automáticamente:

```text
Entire Source Payload
```

La proyección debe respetar minimización y contratos de lectura.

---

# Domain Event Payload

La existencia de información en:

```text
AuditRecorded
```

no obliga a exponer todo su Payload en una vista.

---

# Integration Event Payload

Del mismo modo:

```text
AuditRecordedIntegrationEvent
```

no determina automáticamente el contenido del Read Model interno.

---

# Logs

Audit Read Models no son:

```text
Log Viewer
```

por definición.

Debe mantenerse:

```text
Audit Read Model

≠

Application Log
```

---

# Observability

Metrics, traces y logs técnicos permanecen fuera del Read Model de
dominio Audit salvo que un producto de lectura separado los combine
explícitamente sin cambiar ownership.

---

# FIWARE

Un Read Model de Audit no es una entidad FIWARE por definición.

Debe mantenerse:

```text
Audit Read Model

≠

NGSI-LD Entity
```

---

# FIWARE Projection

Cuando exista una necesidad de interoperabilidad:

```text
Audit / Audit Event
    │
    ▼
Integration
    │
    ▼
FIWARE Representation
```

la representación FIWARE permanece separada del Read Model interno.

---

# Sistemas Municipales

Una plataforma municipal puede consumir una vista o contrato de
integración cuando corresponda.

Su modelo de consulta no determina el modelo interno de Audit.

---

# Anti-Corruption Layer

Cuando un consumidor externo requiera una estructura diferente, debe
realizarse una traducción fuera del Aggregate.

Debe mantenerse:

```text
External Read Contract

≠

Audit Internal Read Model
```

salvo equivalencia explícitamente definida.

---

# Persistencia del Read Model

La persistencia física de proyecciones pertenece a Infrastructure.

El dominio no depende de:

```text
SQL

PostgreSQL

MongoDB

Elasticsearch

OpenSearch

Redis

Graph Database

Search Engine
```

ni tecnologías equivalentes.

---

# Read Store

Un Read Store puede ser diferente del almacenamiento del Write Model.

Debe mantenerse:

```text
Write Store

≠

Read Store
```

como posibilidad compatible con CQRS.

No constituye una obligación tecnológica.

---

# Consistencia del Read Store

El Read Store puede actualizarse de forma eventual.

No participa necesariamente en la misma transacción que:

```text
AuditRepository.save()
```

---

# Fallo de Proyección

Si una proyección falla después de que Audit fue confirmado:

```text
Audit
```

permanece válido.

Debe mantenerse:

```text
Projection Failure

≠

Audit Rollback
```

---

# Projection Failure no es AuditStatus

Debe mantenerse:

```text
ProjectionFailure

≠

AuditStatus
```

No produce:

```text
Failed
```

dentro del Aggregate.

---

# Retry de Proyección

Un retry técnico de proyección no modifica Audit.

Debe mantenerse:

```text
Projection Retry

≠

Audit Modification
```

---

# Retry no Incrementa Version

Un retry de proyección no incrementa:

```text
Audit.Version
```

---

# Read Model y Delete

La eliminación o reconstrucción física de una proyección no implica:

```text
DeleteAudit
```

ni:

```text
AuditStatus = Deleted
```

---

# Rebuild Completo

Una proyección puede eliminarse técnicamente y reconstruirse desde
sus fuentes.

Debe mantenerse:

```text
Delete Read Projection

≠

Delete Aggregate
```

---

# Retención de Read Models

La política de retención física de una proyección no define la
política de retención del Aggregate.

Debe mantenerse:

```text
Read Model Retention

≠

Audit Retention
```

---

# Archivado de Read Model

Un Read Model puede aplicar estrategias técnicas de almacenamiento
histórico.

Esto no crea:

```text
AuditStatus = Archived
```

---

# Performance

El Read Model permite optimizar consultas sin ampliar el Aggregate.

Debe mantenerse:

```text
Query Optimization

≠

Aggregate Expansion
```

---

# Aggregate Pequeño

Audit no debe cargar colecciones históricas completas para responder
consultas.

Las necesidades de:

```text
history

filtering

sorting

aggregation
```

pertenecen al Read Side.

---

# Índices de Consulta

Pueden crearse índices sobre:

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

cuando sea necesario.

La estrategia de indexación pertenece a Infrastructure.

---

# Grandes Volúmenes

El crecimiento histórico de Audit debe resolverse en el Read Side
mediante mecanismos apropiados de consulta.

No debe provocar que una única Aggregate Root cargue todo el
historial.

---

# Batch Queries

Las consultas masivas pueden operar sobre Read Models.

No requieren cargar múltiples Audit Aggregates dentro de una
transacción.

---

# Bulk Export

Una exportación masiva de información Audit pertenece al Read Side o
a Application.

No constituye un Command del Aggregate.

---

# Reporting Histórico

Un reporte puede combinar múltiples unidades Audit.

Debe mantenerse:

```text
Report

≠

Aggregate
```

---

# Dashboard

Un dashboard de trazabilidad puede utilizar Read Models.

No constituye parte del Aggregate Audit.

---

# Read Model e Historial Inmutable

Una proyección debe preservar el significado histórico de los hechos
confirmados.

No debe reinterpretar:

```text
AuditRecorded
```

como un hecho diferente.

---

# Nuevo Source Fact

Cuando se registra una nueva unidad Audit correspondiente a otro
Source Fact:

```text
Audit A

Audit B
```

el Read Model puede mostrarlas juntas.

Esto no implica que Audit B modifique Audit A.

---

# Corrección del Source Aggregate

Si el Source Aggregate produce un hecho correctivo posterior, el Read
Model puede mostrar ambos hechos.

Conceptualmente:

```text
Fact A

Fact B
```

permanecen como hechos históricos distintos.

---

# Vista de Correcciones

Una proyección puede mostrar relaciones entre un hecho original y un
hecho posterior cuando exista información suficiente.

No debe reescribir el registro histórico anterior.

---

# No CorrectAudit desde Read Side

Una vista no puede producir:

```text
CorrectAudit
```

porque dicho Command no existe en la versión 1.0.

---

# No ArchiveAudit desde Read Side

Una vista histórica no puede ejecutar:

```text
ArchiveAudit
```

porque Archived no forma parte del Lifecycle.

---

# No DeleteAudit desde Read Side

Una vista no puede ejecutar:

```text
DeleteAudit
```

porque dicho Command no forma parte del modelo oficial.

---

# No RetryAudit desde Read Side

Una proyección no ejecuta:

```text
RetryAudit
```

porque los retries técnicos permanecen fuera del dominio.

---

# Query no Produce Domain Event

Una consulta no produce:

```text
AuditRecorded
```

ni ningún otro Domain Event de Audit.

---

# Read Access no Incrementa Version

Debe mantenerse:

```text
Read Access

≠

Audit Version Increment
```

---

# Read Access no Modifica UpdatedAt

Una consulta no constituye modificación válida del Aggregate.

Por lo tanto:

```text
Read

≠

Audit.UpdatedAt Change
```

---

# Queries Conceptuales

El Read Side puede soportar conceptualmente consultas como:

```text
Get Audit by AuditId

List Audits by SourceAggregateId

List Audits by SourceAggregateType

List Audits by SourceEventId

List Audits by SourceEventType

List Audits by ActorId

List Audits by CorrelationId

List Audits by CausationId

List Audits by SourceOccurredAt range

List Audits by CreatedAt range
```

La forma técnica de implementación pertenece a Application e
Infrastructure.

---

# Composición de Filtros

Los filtros pueden combinarse según las necesidades de lectura.

Por ejemplo:

```text
SourceAggregateType

+

SourceEventType

+

Time Range
```

como criterio de consulta.

Esta combinación no introduce nuevas Invariants en el Aggregate.

---

# Query Result

El resultado de una consulta puede contener uno o múltiples registros
proyectados.

Debe mantenerse:

```text
Query Result

≠

Aggregate Collection Ownership
```

---

# Empty Result

Una consulta sin resultados no implica error del Aggregate.

Debe mantenerse:

```text
No Read Result

≠

Invalid Audit State
```

---

# AuditNotFound en Read Side

Una consulta por AuditId puede no encontrar una proyección.

Esto no modifica el Aggregate ni produce Domain Events.

---

# Projection Missing

Puede existir un Audit confirmado cuya proyección aún no esté
disponible debido a lag.

Debe mantenerse:

```text
Missing Projection

≠

Missing Aggregate
```

necesariamente.

---

# Reconciliación

La reconstrucción o reconciliación de proyecciones debe ocurrir fuera
del Aggregate.

No debe utilizarse para modificar silenciosamente Audit.

---

# Independencia Tecnológica

El Read Model no depende conceptualmente de:

```text
PostgreSQL

MongoDB

Elasticsearch

OpenSearch

Redis

GraphQL

REST

HTTP

FastAPI

Django

React

Next.js

FIWARE

NGSI-LD
```

Estas tecnologías pueden implementar consultas o presentación.

No definen el significado del Read Model.

---

# API

La existencia de una API de consulta no modifica el Read Model
conceptual.

Debe mantenerse:

```text
API Contract

≠

Audit Aggregate
```

---

# UI

Una interfaz de usuario puede presentar Read Models.

La UI no adquiere autoridad sobre el Write Model.

---

# Export

Una representación exportada:

```text
CSV

JSON

PDF

Report
```

no constituye el Aggregate Audit.

---

# Auditoría de Consultas

La versión 1.0 no establece automáticamente que toda lectura de Audit
deba producir otra unidad Audit.

Debe mantenerse:

```text
Read Audit

≠

Automatic RecordAudit
```

Cualquier necesidad de auditar accesos deberá definirse mediante un
hecho y contrato explícitos.

---

# Recursividad

Consultar Audit no debe crear automáticamente:

```text
Audit of Audit Read
```

evitando ciclos recursivos no definidos.

---

# Read Model y Domain Ownership

Ninguna vista derivada adquiere ownership sobre:

- Audit;
- Source Aggregate;
- Source Domain Event;
- Actor;
- Organization;
- Citizen;
- Membership;
- Role;
- Territory;
- Assembly;
- Proposal;
- Participation;
- Voting;
- Document;
- Notification;
- Integration.

---

# Consistency Boundary

El Read Model permanece fuera del Consistency Boundary:

```text
Audit
```

Debe mantenerse:

```text
Read Model Update

≠

Audit Transaction
```

---

# Fallo del Read Model

Una proyección fallida no puede provocar:

```text
Audit Rollback
```

ni:

```text
Source Aggregate Rollback
```

---

# Flujo Oficial

```text
Confirmed Source Fact
        │
        ▼
   RecordAudit
        │
        ▼
      Audit
        │
        ▼
   AuditRecorded
        │
        ▼
   Audit Commit
        │
        ▼
    Projection
        │
        ▼
  Audit Read Model
        │
        ▼
      Query
```

---

# Flujo de Consulta

```text
User / Process
      │
      ▼
Read Authorization
      │
      ▼
   Query
      │
      ▼
Audit Read Model
      │
      ▼
   Result
```

Esta secuencia no modifica el Aggregate.

---

# Flujo de Projection Lag

```text
T1

Audit committed
```

luego:

```text
T2

Read Model still old
```

posteriormente:

```text
T3

Projection applied
```

Esta secuencia es compatible con consistencia eventual.

---

# Flujo de Rebuild

```text
Confirmed Audit Facts
    │
    ▼
Rebuild Projection
    │
    ▼
Read Model
```

sin:

```text
RecordAudit

Version Increment

New Domain Event
```

---

# Flujo con Integration

Para consumidores externos:

```text
AuditRecorded
    │
    ▼
Integration Boundary
    │
    ▼
AuditRecordedIntegrationEvent
    │
    ▼
External Projection
```

Esta proyección permanece fuera del dominio Audit.

---

# Reglas Fundamentales

El Read Model de Audit debe cumplir:

1. Audit Aggregate y Audit Read Model son conceptos distintos.
2. El Aggregate es autoridad sobre el Write Model.
3. El Read Model es una proyección derivada.
4. El Read Model no modifica Audit.
5. El Read Model no ejecuta Commands.
6. El Read Model no produce Domain Events de Audit.
7. AuditRecorded puede alimentar proyecciones internas.
8. AuditId puede proyectarse como identidad de lectura.
9. Recorded es el único AuditStatus válido versión 1.0.
10. SourceAggregateId puede utilizarse para búsqueda.
11. SourceAggregateType puede utilizarse para clasificación.
12. SourceEventId puede utilizarse para trazabilidad.
13. SourceEventType puede utilizarse para filtros.
14. SourceAggregateVersion permanece distinta de Audit.Version.
15. ActorId puede proyectarse únicamente cuando corresponda.
16. CorrelationId puede utilizarse para reconstruir flujos.
17. CausationId puede utilizarse para reconstruir causalidad.
18. SourceOccurredAt y CreatedAt mantienen significado distinto.
19. Version puede proyectarse para trazabilidad.
20. ReadModel.Version no posee autoridad sobre Audit.Version.
21. Consultas por AuditId pertenecen al Read Side.
22. Consultas por SourceAggregateId pertenecen al Read Side.
23. Consultas por SourceEventId pertenecen al Read Side.
24. Consultas por ActorId pertenecen al Read Side.
25. Consultas por CorrelationId pertenecen al Read Side.
26. Consultas por CausationId pertenecen al Read Side.
27. Filtros temporales pertenecen al Read Side.
28. Ordenamiento pertenece al Read Side.
29. No existe orden global obligatorio de Audit.
30. Timeline y vistas históricas no crean un Aggregate global.
31. Paginación no es comportamiento del Aggregate.
32. Búsqueda no es comportamiento del Aggregate.
33. Reporting no es comportamiento del Aggregate.
34. Analytics no es comportamiento del Aggregate.
35. Agregaciones pertenecen al Read Side.
36. El Read Model puede mantener consistencia eventual.
37. Projection Lag no constituye inconsistencia de Audit.
38. Una actualización de proyección no incrementa Audit.Version.
39. Las proyecciones deben soportar procesamiento idempotente.
40. Duplicate Delivery no crea un nuevo hecho.
41. AggregateVersion puede preservar orden por identidad.
42. Rebuild no ejecuta Commands.
43. Rebuild no produce Domain Events.
44. Rebuild no incrementa Audit.Version.
45. AuditRepository pertenece al Write Side.
46. Query Repository permanece separado del Aggregate Repository.
47. Consultas complejas no deben agregarse al Aggregate Repository
    por conveniencia.
48. Read Model no modifica State.
49. Read Model no modifica AuditId.
50. Read Model no modifica Source Fact.
51. Read Models internos pueden consumir Domain Events.
52. Read Models externos pueden consumir Integration Events.
53. Domain Event Stream y Read Model son conceptos distintos.
54. Snapshot no es Read Model por definición.
55. Cache no es autoridad.
56. Índices técnicos no son parte del dominio.
57. Denormalización de lectura no amplía el Aggregate.
58. Cross-Aggregate Read Models no crean transacciones
    Cross-Aggregate.
59. Otros Aggregates permanecen fuera del ownership de Audit.
60. Read Permission permanece separada de Write Permission.
61. La existencia de un Read Model no implica acceso público.
62. Cada vista debe respetar minimización.
63. ActorId no se expone automáticamente.
64. Credenciales no deben formar parte de Read Models.
65. Source Payload no se expone automáticamente.
66. Domain Event Payload no determina automáticamente una vista.
67. Audit Read Model no es Log Viewer.
68. Audit Read Model no es Observability.
69. Audit Read Model no es entidad FIWARE.
70. Sistemas municipales utilizan contratos separados.
71. La persistencia del Read Model pertenece a Infrastructure.
72. Write Store y Read Store pueden ser distintos.
73. Fallos de proyección no provocan rollback de Audit.
74. ProjectionFailure no es AuditStatus.
75. Retry de proyección no modifica Audit.
76. Eliminar una proyección no elimina Audit.
77. Retención del Read Model no define retención del Aggregate.
78. Optimización de consulta no amplía el Aggregate.
79. Grandes volúmenes históricos deben resolverse mediante el Read
    Side.
80. Bulk Queries y Bulk Export no son Commands del Aggregate.
81. Un reporte no es un Aggregate.
82. Nuevos Source Facts no reescriben Audits previos.
83. Una vista puede mostrar hechos correctivos sin alterar historia.
84. Read Side no introduce CorrectAudit, ArchiveAudit, DeleteAudit o
    RetryAudit.
85. Queries no producen Domain Events.
86. Read Access no incrementa Version.
87. Read Access no modifica UpdatedAt.
88. Empty Result no constituye estado inválido.
89. Missing Projection no implica necesariamente Missing Aggregate.
90. Reconciliación de proyecciones permanece fuera del Aggregate.

---

# Restricciones

No está permitido:

- utilizar Read Model como fuente autoritativa de escritura;
- modificar Audit desde una proyección;
- ejecutar RecordAudit desde una Query;
- incrementar Audit.Version al consultar;
- modificar Audit.UpdatedAt al consultar;
- producir AuditRecorded desde una proyección;
- introducir nuevos AuditStatus desde el Read Side;
- utilizar ReadModel.Version como Version autoritativa;
- cargar historia global dentro de una única Aggregate Root;
- convertir una necesidad de búsqueda en comportamiento del
  Aggregate;
- agregar filtros analíticos al Repository del Write Model por
  conveniencia;
- utilizar una proyección para evitar State Machine;
- utilizar una proyección para evitar Invariants;
- exponer automáticamente todos los datos del Aggregate;
- exponer automáticamente ActorId;
- exponer secretos o credenciales;
- copiar automáticamente Source Payload completo;
- convertir logs, metrics o traces en Read Model de Audit;
- convertir una entidad FIWARE en modelo interno de Audit;
- utilizar ProjectionFailure como AuditStatus;
- realizar rollback de Audit porque una proyección falla;
- tratar Duplicate Delivery como nuevo hecho;
- tratar Rebuild como nueva modificación;
- eliminar el Aggregate al eliminar una proyección;
- convertir Cross-Aggregate Read Models en Cross-Aggregate
  transactions;
- introducir Commands inexistentes desde la capa de lectura.

---

# Compatibilidad Arquitectónica

El Read Model de Audit es compatible con:

- Domain-Driven Design;
- CQRS;
- Event-Driven Architecture;
- Aggregate Pattern;
- Clean Architecture;
- Hexagonal Architecture;
- SOLID;
- Event Sourcing Compatible;
- Optimistic Concurrency Control;
- consistencia eventual;
- Projection Pattern;
- Materialized Views;
- Persistence Ignorance;
- High Cohesion;
- Low Coupling.

Estas compatibilidades no introducen tecnologías concretas ni
modifican el Consistency Boundary del Aggregate.

---

# Definición de Éxito

El Read Model del Aggregate **Audit** proporciona una representación
derivada, reconstruible y optimizada para consultar la trazabilidad
preservada por AURA sin ampliar ni debilitar el Write Model.

El modelo garantiza que:

```text
Audit Aggregate

≠

Audit Read Model
```

y que:

- Audit permanece como autoridad de escritura;
- el Read Model permanece como proyección derivada;
- AuditRecorded puede alimentar vistas internas;
- las proyecciones no ejecutan Commands;
- las proyecciones no producen Domain Events de Audit;
- AuditId, Source References, Version y Traceability Information
  pueden proyectarse cuando corresponda;
- Recorded permanece como único estado oficial;
- SourceAggregateVersion y Audit.Version conservan significado
  independiente;
- ActorId, CorrelationId y CausationId solo se exponen cuando
  corresponde;
- consultas históricas permanecen en el Read Side;
- búsqueda, filtrado, ordenamiento, paginación, reporting y
  Analytics no forman parte del Aggregate;
- vistas globales no crean un Aggregate global;
- múltiples Audits pueden combinarse en consultas sin compartir
  Consistency Boundary;
- consistencia eventual entre Write Model y Read Model es válida;
- Projection Lag no representa inconsistencia del Aggregate;
- Duplicate Delivery no crea nuevos hechos en la proyección;
- Rebuild no modifica Audit;
- AuditRepository y mecanismos de consulta permanecen separados;
- Read Permissions y Write Permissions permanecen independientes;
- minimización y Security gobiernan qué información puede exponerse;
- datos sensibles y credenciales permanecen fuera de las vistas;
- Domain Event Payload y Source Payload no se exponen
  automáticamente;
- Read Models internos y externos pueden utilizar fuentes diferentes
  conforme a sus contratos;
- Event Sourcing permanece compatible sin convertir el Event Stream
  en Read Model;
- Cache, índices, denormalización y stores físicos permanecen fuera
  del dominio;
- fallos o retries de proyección no modifican Audit;
- eliminar o reconstruir una proyección no modifica el Aggregate;
- FIWARE, sistemas municipales, APIs y UI permanecen desacoplados del
  modelo conceptual;
- cualquier evolución futura del Read Side debe preservar la
  autoridad, identidad, Invariants y Consistency Boundary del
  Aggregate Audit.

De esta forma, `DOMAIN-012L-Read-Model.md` establece formalmente el
Read Model del Aggregate **Audit** conforme al patrón consolidado de
AURA Core.