# DOMAIN-013L — Integration Read Model

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
- DOMAIN-013M-Test-Scenarios.md
- DOMAIN-013N-Performance-Rules.md
- DOMAIN-013O-Security-Model.md
- DOMAIN-013P-Extension-Points.md

---

# Objetivo

Este documento define formalmente las reglas conceptuales del
**Read Model** asociado al Aggregate **Integration**.

El Read Model representa información derivada y optimizada para
consultas.

Su propósito es permitir lectura eficiente sin otorgar autoridad de
escritura ni modificar el Consistency Boundary del Aggregate.

---

# Principio Fundamental

Debe mantenerse:

```text
Read Model

=

Query Representation
```

y:

```text
Read Model

≠

Aggregate
```

---

# Write Authority

La autoridad de escritura pertenece exclusivamente a:

```text
Integration Aggregate
```

Debe mantenerse:

```text
Read Model

≠

Write Authority
```

---

# Read Model versus Aggregate

Integration protege:

- identidad;
- Lifecycle;
- State Machine;
- Commands;
- Invariants;
- Versioning;
- comportamiento;
- Consistency Boundary.

El Read Model representa información para consulta.

---

# Source of Truth

Para modificaciones:

```text
Integration Aggregate

=

Source of Truth
```

El Read Model no sustituye al Aggregate como autoridad de escritura.

---

# Read Side

El Read Model pertenece conceptualmente al:

```text
Read Side
```

y permanece separado del:

```text
Write Side
```

---

# CQRS

Integration es compatible con CQRS.

Conceptualmente:

```text
Write Side
    │
    ▼
Integration Aggregate
    │
    ▼
Domain Events
    │
    ▼
Projection
    │
    ▼
Read Model
```

Esta compatibilidad no impone una implementación técnica concreta.

---

# CQRS no es Obligatorio

Debe mantenerse:

```text
CQRS Compatible

≠

CQRS Required
```

El documento define separación conceptual de responsabilidades sin
imponer una topología técnica determinada.

---

# Read Model no Protege Invariants de Escritura

Las Invariants pertenecen al Aggregate.

Debe mantenerse:

```text
Read Model

≠

Invariant Authority
```

---

# Read Model no Ejecuta Commands

No está permitido que el Read Model ejecute:

```text
CreateIntegration

ActivateIntegration

SuspendIntegration

ReactivateIntegration

ArchiveIntegration
```

---

# Read Model no Ejecuta Transiciones

El Read Model no puede producir directamente:

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

# Read Model no Modifica State

Debe mantenerse:

```text
Read Model State

≠

Integration State Mutation Authority
```

---

# Read Model no Modifica Version

El Read Model puede representar:

```text
Integration.Version
```

pero no puede incrementarla ni establecerla.

---

# Read Model no Modifica IntegrationId

IntegrationId puede proyectarse para consulta.

No puede modificarse desde el Read Side.

---

# Read Model no Modifica CreatedAt

CreatedAt puede proyectarse.

No puede alterarse desde una Query.

---

# Read Model no Modifica UpdatedAt

UpdatedAt puede proyectarse.

Consultar el Read Model no modifica UpdatedAt del Aggregate.

---

# Naturaleza Derivada

El Read Model contiene información derivada desde hechos o estado
confirmado del dominio.

Debe mantenerse:

```text
Read Model

=

Derived Representation
```

---

# Proyección

Una Projection puede construir o actualizar el Read Model a partir de
información confirmada.

Conceptualmente:

```text
Confirmed Domain Fact
    │
    ▼
Projection
    │
    ▼
Read Model
```

---

# Projection no es Aggregate

Debe mantenerse:

```text
Projection

≠

Integration Aggregate
```

---

# Projection no es Command Handler de Dominio

Una Projection no debe ejecutar Commands para reproducir cambios ya
ocurridos.

---

# Domain Events

Los Domain Events oficiales:

```text
IntegrationCreated

IntegrationActivated

IntegrationSuspended

IntegrationReactivated

IntegrationArchived
```

pueden alimentar representaciones de lectura.

---

# Domain Event no es Read Model

Debe mantenerse:

```text
Domain Event

≠

Read Model
```

---

# Domain Event no es Query Result

Un Domain Event representa un hecho.

Una Query representa una necesidad de lectura.

---

# Read Model no Produce Domain Events

Consultar o actualizar una Projection no produce nuevos Domain Events
del Aggregate.

Debe mantenerse:

```text
Read Model Update

≠

New Domain Fact
```

---

# Integration Events

Los Integration Events permanecen conceptualmente separados de los
Read Models.

Debe mantenerse:

```text
Integration Event

≠

Read Model
```

---

# Integration Event no es Query Result

Un Integration Event representa un contrato de interoperabilidad.

No constituye una respuesta genérica de lectura.

---

# Read Model no Define Integration Events

Una necesidad de consulta no crea automáticamente:

```text
Integration Event
```

---

# Contenido Conceptual

El Read Model puede proyectar información perteneciente al dominio de
Integration cuando sea necesaria para consulta.

Conceptualmente puede incluir:

```text
IntegrationId

State

Version

CreatedAt

UpdatedAt
```

y otra información formalmente definida en el Aggregate o derivada de
hechos confirmados.

---

# No Nuevos Atributos de Dominio

La existencia de un campo en un Read Model no introduce automáticamente
un nuevo atributo al Aggregate.

Debe mantenerse:

```text
Read Model Field

≠

Aggregate Attribute
```

---

# Información Derivada

El Read Model puede contener información derivada para facilitar
consultas.

Esa información derivada no adquiere automáticamente semántica de
estado interno del Aggregate.

---

# Derived Field

Debe mantenerse:

```text
Derived Field

≠

New Domain State
```

---

# State

El Read Model puede representar:

```text
Draft

Active

Suspended

Archived
```

como proyección del State confirmado.

---

# No Nuevos States

El Read Model no puede introducir como Lifecycle States:

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
```

---

# Estado Técnico en Read Model

Una eventual representación técnica de disponibilidad puede existir
fuera del Aggregate para propósitos operacionales.

Debe mantenerse:

```text
Technical Status

≠

Integration Lifecycle State
```

---

# Technical Health

Si una vista presenta información como:

```text
Healthy

Unhealthy

Degraded
```

dicha información no redefine:

```text
Integration.State
```

---

# Projection Lag

Debido a consistencia eventual, puede existir temporalmente:

```text
Aggregate State = Active

Read Model State = Draft
```

---

# Read Model Lag no es Inconsistencia Interna

Debe mantenerse:

```text
Projection Lag

≠

Aggregate Invariant Violation
```

El Aggregate sigue siendo autoritativo para escritura.

---

# Version Lag

Puede existir temporalmente:

```text
Integration.Version = 8

Read Model projected Version = 7
```

---

# Read Model Version

Cuando el Read Model proyecta:

```text
Integration.Version
```

representa la Version conocida por la Projection.

No puede utilizarse como autoridad final de escritura sin recuperar el
Aggregate conforme a sus reglas.

---

# Projection Version

Una Projection puede poseer metadata técnica propia.

Debe mantenerse:

```text
Projection Version

≠

Integration.Version
```

salvo que un campo represente explícitamente la Version proyectada del
Aggregate.

---

# Read Model y ExpectedVersion

Una Query puede mostrar Version.

Sin embargo, la validación de ExpectedVersion para una modificación
pertenece al Write Side y al Repository Contract.

---

# Stale Read

Una lectura desactualizada no autoriza sobrescribir una revisión más
reciente.

Debe mantenerse:

```text
Stale Read Model

≠

Permission to Ignore Concurrency
```

---

# Concurrency

Optimistic Concurrency continúa protegiendo al Aggregate aunque una
intención se haya originado desde información proyectada.

---

# Query

Una Query expresa una necesidad de lectura.

Debe mantenerse:

```text
Query

≠

Command
```

---

# Query no Modifica Aggregate

Toda Query debe ser conceptualmente libre de efectos sobre el estado
del Aggregate.

---

# Query no Incrementa Version

Debe mantenerse:

```text
Query

→

Integration.Version unchanged
```

---

# Query no Modifica UpdatedAt

Debe mantenerse:

```text
Query

→

Integration.UpdatedAt unchanged
```

---

# Query no Produce Domain Event

Debe mantenerse:

```text
Query

→

No new Integration Domain Event
```

---

# Query no Produce Integration Event

Una consulta tampoco produce automáticamente un Integration Event.

---

# Capacidades de Consulta

El Read Side puede soportar conceptualmente necesidades como:

```text
Search

Filter

Sort

Pagination

Reporting

Analytics
```

cuando corresponda.

---

# Search

Búsqueda pertenece al Read Side.

No debe ampliar IntegrationRepository del Write Model por conveniencia.

---

# Filter

Filtrar Integrations por información proyectada no modifica sus
Aggregates.

---

# Sort

Ordenar resultados es una responsabilidad de lectura.

---

# Pagination

Paginar resultados no modifica el dominio.

---

# Reporting

Reporting pertenece al Read Side.

No constituye comportamiento de Integration.

---

# Analytics

Analytics pertenece al Read Side.

No crea nuevas Invariants.

---

# Ejemplos de Consultas Conceptuales

Pueden existir necesidades conceptuales como:

```text
find Integration by IntegrationId

list Integration by State

list Active Integration

list Suspended Integration

list Archived Integration

inspect projected Version

inspect creation time

inspect last domain modification time
```

sin convertir dichas necesidades en Commands.

---

# Query by IntegrationId

Una vista puede recuperar información de:

```text
IntegrationId = X
```

sin rehidratar el Aggregate cuando solamente se requiere lectura.

---

# Query by State

Una consulta puede seleccionar:

```text
State = Active
```

para lectura.

No ejecuta:

```text
ActivateIntegration
```

---

# Query by Version

Puede consultarse:

```text
Version = N
```

como dato proyectado.

No modifica la secuencia de Version.

---

# Query Histórica

Si existe información histórica proyectada, puede utilizarse para
lectura.

Esto no obliga al Aggregate a almacenar una colección de historial para
consultas.

---

# Historial

Debe mantenerse:

```text
Query History Requirement

≠

Aggregate History Collection Requirement
```

---

# Repository versus Read Model

IntegrationRepository pertenece conceptualmente al Write Side.

El Read Model pertenece al Read Side.

Debe mantenerse:

```text
IntegrationRepository

≠

Read Model
```

---

# Repository findById()

`findById()` recupera el Aggregate cuando se requiere comportamiento de
dominio.

---

# Read Model Lookup

Una consulta de lectura puede utilizar una representación proyectada
cuando no se requiere comportamiento del Aggregate.

---

# Repository no es Motor Analítico

Debe mantenerse:

```text
Repository

≠

Reporting Engine
```

y:

```text
Repository

≠

Analytics Engine
```

---

# Read Model no es Repository

El Read Model tampoco adquiere las responsabilidades de persistencia
del Aggregate.

---

# Repository save()

`save()` no pertenece al Read Model.

---

# Read Model no Tiene save() de Aggregate

Una operación de persistencia técnica de una Projection no debe
interpretarse como:

```text
IntegrationRepository.save()
```

---

# Consistency Boundary

El Read Model permanece fuera del Write Consistency Boundary.

Debe mantenerse:

```text
Read Model

∉

Integration Aggregate Consistency Boundary
```

---

# Projection no Expande Boundary

Crear nuevas vistas no amplía:

```text
Integration Consistency Boundary
```

---

# Multiple Read Models

Pueden existir múltiples representaciones de lectura para diferentes
necesidades.

Debe mantenerse:

```text
Multiple Read Models

≠

Multiple Aggregate Sources of Truth
```

---

# No Read Model Único Obligatorio

La versión 1.0 no establece una única estructura física obligatoria de
Read Model.

---

# No Nombre Concreto Obligatorio

Este documento no establece nombres concretos obligatorios como:

```text
IntegrationView

IntegrationSummary

IntegrationDashboardView

IntegrationProjection
```

como contratos universales del dominio.

---

# No Estructura Física Obligatoria

Este documento no define:

- tablas;
- colecciones;
- índices;
- documentos;
- vistas SQL;
- materialized views;
- caches;
- search indexes.

---

# Persistencia del Read Model

La estrategia física utilizada para almacenar una Projection pertenece
a Infrastructure.

---

# Database Independence

El Read Model conceptual no exige:

```text
PostgreSQL

MongoDB

Redis

Elasticsearch

OpenSearch
```

ni otra tecnología concreta.

---

# Indexing

La necesidad de índices pertenece a Infrastructure.

No introduce reglas del Aggregate.

---

# Cache

Un Read Model puede eventualmente utilizar cache.

Debe mantenerse:

```text
Cache

≠

Integration Source of Truth
```

---

# Cache Lag

Un cache desactualizado no modifica el Aggregate.

---

# Cache Invalidation

Cache invalidation no produce Domain Events.

---

# Rebuild

Un Read Model puede ser reconstruido desde información confirmada cuando
la estrategia adoptada lo permita.

---

# Projection Rebuild

Debe mantenerse:

```text
Projection Rebuild

≠

Re-execute Commands
```

---

# Projection Rebuild no Cambia Version

Reconstruir una vista no modifica:

```text
Integration.Version
```

---

# Projection Rebuild no Cambia State

Tampoco modifica:

```text
Integration.State
```

---

# Projection Rebuild no Produce Domain Events

Debe mantenerse:

```text
Projection Rebuild

≠

New Domain Fact
```

---

# Projection Replay

Reprocesar hechos para reconstruir una vista no constituye comportamiento
nuevo del Aggregate.

---

# Event Sourcing

Event Sourcing permanece compatible.

No es obligatorio para construir Read Models.

---

# Event Sourcing no es Requisito

Debe mantenerse:

```text
Read Model

≠

Event Sourcing Requirement
```

---

# Source Data

Un Read Model puede derivarse de información confirmada del dominio.

Este documento no impone una única fuente técnica de proyección.

---

# Domain Event Projection

Los Domain Events pueden constituir una fuente conceptual válida para
actualizar vistas.

---

# Current State Projection

Una estrategia también puede representar el estado confirmado según la
solución adoptada.

Este documento no decide la estrategia física.

---

# No Architecture Decision

La definición del Read Model no decide:

- Event Sourcing;
- polling;
- broker;
- database;
- synchronous projection;
- asynchronous projection;
- cache;
- search engine;
- materialized view;
- streaming.

---

# Consistencia Eventual

Entre Write Side y Read Side puede existir:

```text
Eventual Consistency
```

---

# No Immediate Projection Requirement

Este documento no exige:

```text
Write Commit

=

Read Model Updated at same instant
```

---

# Aggregate Commit Independiente

Debe mantenerse:

```text
Integration Commit

≠

Read Model Commit
```

---

# Projection Failure

Una falla al actualizar una Projection no revierte automáticamente:

```text
Integration State

Integration.Version

Domain Event
```

ya confirmados.

---

# Projection Retry

Un retry técnico de Projection no representa una nueva modificación del
Aggregate.

---

# Projection Retry no Incrementa Version

Debe mantenerse:

```text
Projection Retry

≠

Integration.Version Increment
```

---

# Projection Failure no Suspende

Debe mantenerse:

```text
Projection Failure

≠

SuspendIntegration
```

---

# Projection Recovery no Reactiva

Debe mantenerse:

```text
Projection Recovery

≠

ReactivateIntegration
```

---

# Freshness

Un Read Model puede tener un grado temporal de retraso respecto del
Write Model.

---

# Freshness no es State

Debe mantenerse:

```text
Projection Freshness

≠

Integration State
```

---

# Stale no es State

La condición técnica:

```text
Stale
```

no pertenece al Lifecycle de Integration.

---

# Rebuilding no es State

La condición:

```text
Rebuilding
```

tampoco pertenece al Lifecycle.

---

# Synchronizing no es State

La condición:

```text
Synchronizing
```

no pertenece al Lifecycle.

---

# Projection Status

Un estado técnico de Projection permanece separado del estado del
Aggregate.

---

# Read Model y Permissions

Las Permissions de escritura definidas en:

```text
DOMAIN-013F-Permissions.md
```

protegen Commands.

No deben confundirse con políticas de lectura.

---

# Read Permission versus Write Permission

Debe mantenerse:

```text
Read Permission

≠

Integration.Create

≠

Integration.Activate

≠

Integration.Suspend

≠

Integration.Reactivate

≠

Integration.Archive
```

---

# Query Authorization

Una Query puede requerir Authorization.

La política concreta de acceso a la información pertenece al Security
Model y al contrato de lectura correspondiente.

---

# Read Model no Decide Authorization

Debe mantenerse:

```text
Read Model

≠

Authorization Authority
```

---

# Read Data no Concede Permission

Conocer:

```text
IntegrationId

State

Version
```

no concede autoridad para modificar Integration.

---

# Read Access no es Write Access

Debe mantenerse:

```text
Can Read Integration

≠

Can Modify Integration
```

---

# Security

El Read Model debe respetar las reglas definidas en:

```text
DOMAIN-013O-Security-Model.md
```

sin incorporar Authentication dentro del Aggregate.

---

# Credentials

El Read Model no debe utilizarse para exponer:

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

# Secret no es Read Field de Dominio

Debe mantenerse:

```text
Secret

∉

Integration Domain Read Model
```

---

# Data Minimization

Los Read Models deben representar únicamente la información necesaria
para el propósito de consulta correspondiente.

---

# No Full External Payload by Default

Debe mantenerse:

```text
Full External Payload

≠

Automatic Read Model Content
```

---

# External Model

Un Read Model de Integration no debe convertirse automáticamente en una
copia del modelo de un sistema externo.

---

# External State

Si una vista muestra datos externos, deben mantenerse semánticamente
separados de:

```text
Integration.State
```

---

# FIWARE

Un Read Model puede participar en consultas relacionadas con
interoperabilidad FIWARE cuando exista información contractual
disponible.

Esto no convierte el Read Model en una FIWARE Entity.

---

# FIWARE Entity

Debe mantenerse:

```text
Integration Read Model

≠

FIWARE Entity
```

---

# NGSI-LD

Este documento no exige NGSI-LD para representar Read Models.

---

# Municipal Systems

Una vista puede mostrar información asociada a interoperabilidad
municipal.

No incorpora automáticamente el modelo municipal como modelo interno de
Integration.

---

# External Identifiers

Referencias externas pueden proyectarse cuando formen parte del contrato
de dominio correspondiente.

No sustituyen IntegrationId.

---

# IntegrationId

Debe mantenerse:

```text
IntegrationId

=

Aggregate Identity
```

aunque el Read Model contenga otras referencias.

---

# CorrelationId

CorrelationId puede aparecer en vistas de trazabilidad cuando esté
disponible y sea necesario.

No constituye identidad del Aggregate.

---

# CausationId

CausationId puede aparecer en vistas de trazabilidad.

No constituye State ni Permission.

---

# ActorId

ActorId puede proyectarse cuando forme parte de los hechos disponibles.

No embebe Citizen.

---

# ActorId no es Citizen Aggregate

Debe mantenerse:

```text
ActorId

≠

Embedded Citizen
```

---

# Other Aggregates

Información referencial sobre otros Aggregates puede proyectarse cuando
exista un contrato válido.

Esto no transfiere ownership.

---

# No Aggregate Embedding

Un Read Model puede combinar información para consulta.

Esto no significa que los Aggregates combinados formen parte de un
único Consistency Boundary.

---

# Joined Read Model

Puede existir conceptualmente una vista que combine información
derivada de múltiples fuentes.

Debe mantenerse:

```text
Joined Read Model

≠

Joined Aggregate
```

---

# Read Composition

La composición para lectura no cambia ownership.

---

# Organization

Una vista puede mostrar una referencia organizacional cuando el
contrato lo permita.

Organization continúa siendo un Aggregate independiente.

---

# Citizen

Una vista puede mostrar una referencia de actor cuando corresponda.

Citizen continúa siendo independiente.

---

# Membership

Una Projection puede combinar información de Membership para una
necesidad concreta de lectura.

Esto no incorpora Membership dentro de Integration.

---

# Role

Una vista puede proyectar información contextual de Role.

Role permanece fuera del Aggregate.

---

# Territory

Una vista puede relacionar información territorial si existe el
contrato correspondiente.

Territory mantiene su propio Boundary.

---

# Assembly

Una vista puede presentar relaciones derivadas con Assembly.

Assembly permanece independiente.

---

# Proposal

Proposal no se convierte en una Internal Entity de Integration por
aparecer en una consulta.

---

# Participation

Participation mantiene su propio estado y Version.

---

# Voting

Voting mantiene su propio Lifecycle.

---

# Document

Document mantiene su propio ownership.

---

# Notification

Un Read Model puede eventualmente mostrar información derivada sobre
Notifications relacionadas.

Notification continúa siendo un Aggregate independiente.

---

# Audit

Audit puede proporcionar información para trazabilidad.

Debe mantenerse:

```text
Audit Read Information

≠

Integration Aggregate State
```

---

# Audit Version

Si una vista presenta:

```text
Audit.Version
```

debe distinguirse de:

```text
Integration.Version
```

---

# SourceAggregateVersion

Una vista de trazabilidad puede mostrar:

```text
SourceAggregateVersion
```

cuando esté disponible.

No debe confundirse con la Version actual de Integration si representa
otro hecho o Aggregate.

---

# Historical Projection

Una vista histórica puede representar sucesivas revisiones o hechos.

Eso no convierte al historial en parte mutable del Aggregate actual.

---

# Current View

Una vista puede representar el estado actual conocido de Integration.

---

# Historical View

Otra vista puede representar hechos históricos.

---

# No View Type Obligatorio

Este documento no establece como obligatorios:

```text
CurrentIntegrationView

IntegrationHistoryView

IntegrationSummaryView
```

ni otros nombres concretos.

---

# Multiple Purposes

Diferentes Read Models pueden atender:

- operación;
- consulta;
- reporting;
- trazabilidad;
- analytics;

sin modificar el Aggregate.

---

# Operational Read Model

Una necesidad operacional de consulta no convierte el Read Model en
mecanismo de escritura.

---

# Reporting Read Model

Una vista de reporting puede agregar información.

No crea nuevas Invariants.

---

# Analytics Read Model

Una vista analítica puede calcular métricas.

No modifica Integration.

---

# Aggregation

Agregar datos de múltiples Integration es una operación de lectura.

Debe mantenerse:

```text
Read Aggregation

≠

Aggregate Boundary Merge
```

---

# Count

Una consulta:

```text
count Active Integration
```

pertenece al Read Side.

---

# Grouping

Una consulta agrupada pertenece al Read Side.

---

# Sorting

Una consulta ordenada pertenece al Read Side.

---

# Filtering

Una consulta filtrada pertenece al Read Side.

---

# Pagination

Una consulta paginada pertenece al Read Side.

---

# Search

Una búsqueda textual o estructurada pertenece al Read Side.

---

# Full-Text Search

La necesidad de Full-Text Search no modifica el Aggregate.

---

# Indexing Strategy

La estrategia de indexación pertenece a Infrastructure.

---

# Query Performance

El Read Model puede optimizarse para patrones de consulta.

---

# Performance no Cambia Dominio

Debe mantenerse:

```text
Read Optimization

≠

Domain Rule
```

---

# Denormalization

Un Read Model puede utilizar información derivada o desnormalizada para
consulta.

Debe mantenerse:

```text
Read Denormalization

≠

Aggregate Denormalization Requirement
```

---

# Denormalized Data no Transfiere Ownership

Copiar información para lectura no transfiere ownership del dato
fuente.

---

# Staleness

Una copia proyectada puede estar temporalmente desactualizada.

---

# Staleness no Permite Escritura Directa

Un consumidor no debe editar la Projection para corregir el Aggregate.

---

# Read Model Correction

Corregir una Projection debe reconstruir o actualizar la representación
derivada.

No modificar silenciosamente el Aggregate.

---

# Aggregate Correction

Si el dominio requiere una modificación real, debe ejecutarse un
Command válido sobre Integration.

---

# Read Model y Archive

Una Integration Archived puede permanecer disponible para consulta.

Debe mantenerse:

```text
Archived

≠

Unreadable
```

salvo política externa explícita de acceso.

---

# Archived no es Deleted

Una vista puede continuar representando:

```text
State = Archived
```

porque Archived no equivale a eliminación física.

---

# Repository.delete()

La existencia de:

```text
Repository.delete()
```

no implica que una Projection deba eliminarse automáticamente por una
regla del Lifecycle.

---

# Retention

Este documento no define:

- retention period;
- purge;
- expiration;
- automatic deletion;
- read model retention.

---

# Historical Retention

La existencia de una vista histórica no establece una política de
conservación.

---

# Read Model Deletion

Eliminar físicamente una Projection es una operación técnica.

No representa:

```text
ArchiveIntegration
```

ni:

```text
IntegrationArchived
```

---

# Read Model Rebuild after Deletion

Si una estrategia permite reconstrucción, eliminar y reconstruir una
Projection no modifica el Aggregate.

---

# Query Result

Una respuesta de lectura representa una instantánea de información
disponible para consulta.

No constituye una nueva revisión del Aggregate.

---

# Query Result no es Domain Event

Debe mantenerse:

```text
Query Result

≠

Domain Event
```

---

# Query Result no es Integration Event

Debe mantenerse:

```text
Query Result

≠

Integration Event
```

---

# API Response

Una API Response puede materializar un Query Result.

No redefine el Read Model conceptual ni el Aggregate.

---

# Serialization

La serialización de un Read Model pertenece a capas externas.

---

# JSON

Este documento no establece JSON como formato obligatorio.

---

# XML

Este documento no establece XML como formato obligatorio.

---

# GraphQL

La existencia de GraphQL no redefine el Read Model de dominio.

---

# REST

La existencia de REST tampoco redefine su semántica.

---

# Protocol Independence

Debe mantenerse:

```text
Read Model Semantics

≠

Transport Protocol
```

---

# Broker

Un broker no es obligatorio para actualizar Read Models.

---

# Polling

Este documento no impone polling.

---

# Push

Este documento no impone push.

---

# Streaming

Este documento no impone streaming.

---

# Synchronous Projection

Este documento no exige Projection síncrona.

---

# Asynchronous Projection

Este documento tampoco exige Projection asíncrona.

---

# Projection Timing

El mecanismo temporal de actualización pertenece a decisiones
posteriores de Infrastructure.

---

# Projection Ordering

Una Projection debe preservar la semántica de los hechos que procesa.

Este documento no establece una estrategia técnica universal de
ordering.

---

# Duplicate Delivery

La infraestructura puede entregar repetidamente un mismo hecho a una
Projection.

Debe mantenerse:

```text
Technical Redelivery

≠

New Domain Fact
```

---

# Idempotencia de Projection

La estrategia técnica concreta de idempotencia no se define en este
documento.

---

# Deduplicación de Projection

Tampoco se define un mecanismo técnico obligatorio de deduplicación.

---

# Exactly Once

No se exige:

```text
Exactly Once
```

para Projections.

---

# Replay de Projection

Un replay técnico puede reprocesar hechos ya existentes.

Esto no genera nuevas modificaciones de Integration.

---

# Projection Error

Un error de Projection pertenece al Read Side.

No crea:

```text
Failed
```

como State de Integration.

---

# Read Model Availability

Una indisponibilidad del Read Model no modifica Integration.

---

# Query Failure

Un Query Failure no produce:

```text
IntegrationSuspended
```

ni:

```text
IntegrationArchived
```

---

# Read Model Recovery

Recuperar disponibilidad del Read Side no produce:

```text
IntegrationReactivated
```

---

# Read Model y FIWARE

Una Projection puede servir necesidades de interoperabilidad o consulta
relacionadas con FIWARE.

Sin embargo:

```text
Read Model

≠

FIWARE Contract
```

---

# Read Model y Integration Event

Un contrato externo puede consumir información derivada.

Esto no convierte la Projection en un Integration Event.

---

# Read Model y External API

Un endpoint de consulta puede exponer un Read Model.

El endpoint no se convierte en parte del dominio.

---

# No Query Endpoint en Dominio

Este documento no define:

- URLs;
- HTTP methods;
- route names;
- GraphQL queries;
- broker topics.

---

# No Concrete Query API

La semántica conceptual del Read Model no selecciona una API concreta.

---

# No Query Repository Concreto

Este documento no introduce un Repository adicional concreto para
consultas.

Las necesidades de lectura se expresan mediante Read Models y Queries
sin imponer un contrato de Infrastructure adicional.

---

# No Query Service Concreto

Tampoco se establece una clase o servicio concreto obligatorio de
consulta.

---

# No Read Store Concreto

La versión 1.0 no establece:

```text
IntegrationReadStore
```

ni otro almacenamiento conceptual obligatorio.

---

# No Projection Class Concreta

La versión 1.0 no define clases concretas de Projection.

---

# No Schema Concreto

No se define un schema físico de Read Model.

---

# No Index Concreto

No se definen índices específicos.

---

# No Cache Policy

No se define política de cache.

---

# No TTL

No se define:

```text
TTL
```

para Read Models.

---

# No Retention Policy

No se establece política de retención del Read Side.

---

# No Search Engine Requirement

No se exige un motor de búsqueda.

---

# No Analytics Engine Requirement

No se exige una plataforma analítica.

---

# No Reporting Engine Requirement

No se exige una herramienta específica de reporting.

---

# Data Ownership

El Read Model no adquiere ownership sobre información proveniente de
otros Aggregates.

---

# Source Ownership

Debe mantenerse:

```text
Projected Data

≠

Ownership Transfer
```

---

# Joined Projection

Una Projection puede presentar información derivada desde diferentes
Boundaries.

Esto no crea un nuevo Aggregate compuesto.

---

# Query Consistency

Un Query Result representa información disponible en el momento de
consulta.

No garantiza por sí mismo que sea la revisión más reciente del Write
Model.

---

# Strong Read Consistency no es Regla del Aggregate

Este documento no exige una política concreta de consistencia de
lectura.

---

# Eventual Read Consistency

El patrón consolidado permite consistencia eventual entre Write Side y
Read Side.

---

# Write Validation

Para modificar Integration debe utilizarse el Aggregate y sus reglas,
independientemente del estado observado en una Projection.

---

# Example — Current Projection

Supóngase:

```text
IntegrationId = INT-001

State = Active

Version = 4
```

Un Read Model puede mostrar:

```text
IntegrationId = INT-001

State = Active

Version = 4
```

---

# Example — Projection Lag

Aggregate:

```text
IntegrationId = INT-001

State = Suspended

Version = 5
```

Projection temporal:

```text
IntegrationId = INT-001

State = Active

Version = 4
```

La Projection no redefine el Aggregate.

---

# Example — Query no Mutation

```text
Given

Integration Version = 5

When

Integration Read Model is queried

Then

Integration Version remains 5

And

UpdatedAt remains unchanged

And

no new Domain Event exists
```

---

# Example — Query by State

```text
Given

multiple Integration projections

When

State = Active is queried

Then

matching projected records may be returned

And

no Integration Aggregate is modified
```

---

# Example — Analytics

Una consulta:

```text
count Integration by State
```

puede resolverse en el Read Side.

No introduce un Command.

---

# Example — Historical Query

Una consulta:

```text
show known Integration lifecycle history
```

puede resolverse mediante información proyectada disponible.

No modifica el Aggregate actual.

---

# Example — Projection Failure

```text
Given

IntegrationActivated is confirmed

When

Projection update fails

Then

Integration remains Active

And

Integration.Version remains unchanged by the projection failure
```

---

# Example — Projection Retry

```text
Given

Projection update failed

When

the projection is retried

Then

no new IntegrationActivated Domain Event is produced
```

---

# Example — Archived Query

```text
Given

Integration State = Archived

When

a permitted Read Query is executed

Then

archived information may remain queryable

And

no Lifecycle transition occurs
```

---

# Example — Joined Read

Una vista puede mostrar conceptualmente:

```text
IntegrationId

State

Organization Reference

Audit-related derived information
```

cuando exista información contractual válida.

Esto no significa:

```text
Integration
+
Organization
+
Audit

=

One Aggregate
```

---

# Example — External Status

Una vista puede mostrar:

```text
Integration State = Active

External Technical Status = OFFLINE
```

sin contradicción.

---

# Example — FIWARE Information

Una vista puede presentar información derivada relacionada con un
contrato FIWARE.

No convierte:

```text
Integration Read Model

into

FIWARE Domain Model
```

---

# Example — Version Independence

Read Model:

```text
Projected Integration.Version = 5
```

External System:

```text
External Version = 18
```

Ambos conceptos permanecen independientes.

---

# Example — Authorization

Un requester puede tener acceso de lectura a una Projection.

Esto no implica:

```text
Integration.Activate

Integration.Suspend

Integration.Reactivate

Integration.Archive
```

---

# Example — Credentials Excluded

Si Infrastructure posee:

```text
AccessToken

ClientSecret
```

estos no deben aparecer como información del dominio en el Read Model.

---

# Example — Rebuild

```text
Given

a Read Model is unavailable or lost

When

the chosen infrastructure rebuilds the projection from confirmed information

Then

Integration State and Version remain unchanged
```

---

# Test Conceptual — No Write Authority

```text
Given

a Read Model with State = Draft

When

an attempt is made to mutate it to Active

Then

no Integration transition is considered valid
```

---

# Test Conceptual — Projection Lag

```text
Given

Aggregate Version = 6

And

Projected Version = 5

Then

Aggregate Version remains authoritative for writes
```

---

# Test Conceptual — Query Safety

```text
Given

an Integration Read Model

When

Search, Filter, Sort or Pagination is executed

Then

Integration Aggregate remains unchanged
```

---

# Test Conceptual — Read Composition

```text
Given

a projection combines information from multiple sources

When

the result is queried

Then

source Aggregate ownership remains unchanged
```

---

# Test Conceptual — No Secret Exposure

```text
Given

Infrastructure credentials exist

When

Integration information is projected

Then

credentials are not included as domain read data
```

---

# Test Conceptual — Projection Failure

```text
Given

a confirmed Integration Domain Event

When

projection processing fails

Then

no Integration rollback occurs
```

---

# Test Conceptual — Projection Replay

```text
Given

confirmed historical facts

When

they are replayed only to rebuild a projection

Then

no new Integration Domain Facts are created
```

---

# Evolución Futura

Nuevos Read Models pueden incorporarse para necesidades concretas de
consulta.

Deben mantenerse separados del Write Model.

---

# Regla para Incorporar un Nuevo Read Model

Un nuevo Read Model debe responder:

```text
What query need does it solve?

What confirmed information does it represent?

What minimum data is required?

Does it preserve source ownership?

Does it remain outside the Aggregate Consistency Boundary?

Does it avoid introducing write authority?

Does it avoid exposing unnecessary or secret data?
```

---

# Nuevo Read Model no Crea Attribute

Debe mantenerse:

```text
New Read Field

≠

New Aggregate Attribute
```

---

# Nuevo Read Model no Crea State

Debe mantenerse:

```text
New Read Representation

≠

New Lifecycle State
```

---

# Nuevo Read Model no Crea Command

Debe mantenerse:

```text
New Read Model

≠

New Command
```

---

# Nuevo Read Model no Crea Domain Event

Debe mantenerse:

```text
New Read Model

≠

New Domain Event
```

---

# Nuevo Read Model no Crea Permission de Escritura

Debe mantenerse:

```text
New Read Model

≠

New Write Permission
```

---

# Nuevo Read Model no Expande Boundary

Debe mantenerse:

```text
New Read Model

≠

Consistency Boundary Expansion
```

---

# Nueva Query

Una nueva Query no debe modificar el Aggregate.

---

# Nueva Necesidad Analítica

Una necesidad analítica no debe convertirse automáticamente en
comportamiento del Write Model.

---

# Nueva Necesidad de Reporting

Reporting no amplía IntegrationRepository por defecto.

---

# Nueva Necesidad de Search

Search no introduce nuevas Invariants.

---

# Nueva Tecnología de Lectura

Incorporar una tecnología de búsqueda, cache o analytics no modifica
el modelo conceptual.

---

# Impacto de Evolución

Cuando un nuevo Read Model implique nuevas representaciones
conceptuales deberá revisarse cuando corresponda:

```text
DOMAIN-013-Aggregate.md

DOMAIN-013D-Domain-Events.md

DOMAIN-013E-Invariants.md

DOMAIN-013F-Permissions.md

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
Query Need

≠

New Domain Behavior
```

y:

```text
Read Optimization

≠

Aggregate Redesign
```

y:

```text
Projection Field

≠

Aggregate Attribute
```

y:

```text
Joined Read Model

≠

Shared Consistency Boundary
```

y:

```text
Read Technology

≠

Domain Architecture Decision
```

---

# Reglas Fundamentales

El Read Model de Integration debe cumplir:

1. Read Model representa información para consulta.
2. Read Model no es Aggregate.
3. Read Model no posee Write Authority.
4. Integration Aggregate continúa siendo Source of Truth para
   escritura.
5. Read Side permanece separado del Write Side.
6. CQRS es compatible pero no obligatorio.
7. Read Model no protege Invariants en lugar del Aggregate.
8. Read Model no ejecuta Commands.
9. Read Model no ejecuta transiciones.
10. Read Model no modifica State.
11. Read Model no modifica Version.
12. Read Model no modifica IntegrationId.
13. Read Model no modifica CreatedAt.
14. Read Model no modifica UpdatedAt.
15. Read Model es una representación derivada.
16. Projection no es Aggregate.
17. Projection no reejecuta Commands para representar hechos ya
    confirmados.
18. Domain Events pueden alimentar Projections.
19. Domain Event no es Read Model.
20. Domain Event no es Query Result.
21. Read Model Update no produce Domain Event.
22. Integration Event no es Read Model.
23. Integration Event no es Query Result.
24. Una necesidad de Query no crea Integration Event.
25. Read Model puede proyectar IntegrationId.
26. Read Model puede proyectar State.
27. Read Model puede proyectar Version.
28. Read Model puede proyectar CreatedAt.
29. Read Model puede proyectar UpdatedAt.
30. Read Model Field no crea Aggregate Attribute.
31. Derived Field no crea Domain State.
32. Los únicos Lifecycle States continúan siendo Draft, Active,
    Suspended y Archived.
33. Technical Status no redefine Integration.State.
34. Projection Lag es compatible con consistencia eventual.
35. Projection Lag no viola Invariants internas.
36. Read Model Version puede estar temporalmente retrasada.
37. Projection Version no es Integration.Version.
38. Read Model no es autoridad de ExpectedVersion.
39. Stale Read no permite ignorar Concurrency.
40. Query no es Command.
41. Query no modifica Aggregate.
42. Query no incrementa Version.
43. Query no modifica UpdatedAt.
44. Query no produce Domain Event.
45. Query no produce Integration Event automáticamente.
46. Search pertenece al Read Side.
47. Filter pertenece al Read Side.
48. Sort pertenece al Read Side.
49. Pagination pertenece al Read Side.
50. Reporting pertenece al Read Side.
51. Analytics pertenece al Read Side.
52. Query History Requirement no obliga Aggregate History Collection.
53. IntegrationRepository no es Read Model.
54. Repository no debe convertirse en Reporting Engine.
55. Repository no debe convertirse en Analytics Engine.
56. Read Model permanece fuera del Write Consistency Boundary.
57. Projection no expande el Aggregate Boundary.
58. Pueden existir múltiples Read Models.
59. Múltiples Read Models no crean múltiples Sources of Truth de
    escritura.
60. No existe una estructura física obligatoria de Read Model.
61. No existe un nombre concreto obligatorio de Read Model.
62. La persistencia de Projections pertenece a Infrastructure.
63. No se exige una base de datos concreta.
64. Cache no es Source of Truth.
65. Projection Rebuild no ejecuta Commands.
66. Projection Rebuild no modifica Version.
67. Projection Rebuild no modifica State.
68. Projection Rebuild no crea nuevos Domain Facts.
69. Event Sourcing no es requisito para Read Models.
70. No se impone una fuente técnica única de Projection.
71. Write Side y Read Side pueden mantener consistencia eventual.
72. Integration Commit no es Read Model Commit.
73. Projection Failure no revierte Integration.
74. Projection Retry no incrementa Integration.Version.
75. Projection Failure no suspende Integration.
76. Projection Recovery no reactiva Integration.
77. Projection Freshness no es Lifecycle State.
78. Stale no es Lifecycle State.
79. Rebuilding no es Lifecycle State.
80. Synchronizing no es Lifecycle State.
81. Read Permission no es Write Permission.
82. Read Model no decide Authorization.
83. Read Data no concede Write Permission.
84. Credentials no forman parte del Domain Read Model.
85. Data Minimization aplica al Read Side.
86. External Payload no se copia automáticamente al Read Model.
87. External Model no reemplaza el Domain Model.
88. FIWARE Entity no es Integration Read Model.
89. Joined Read Model no es Joined Aggregate.
90. Read Composition no transfiere ownership.
91. Read Aggregation no fusiona Aggregate Boundaries.
92. Denormalization de lectura no redefine el Aggregate.
93. Archived puede continuar representándose para consulta.
94. Archived no es Deleted.
95. Este documento no define política de retención del Read Side.
96. Query Result no es Domain Event.
97. Query Result no es Integration Event.
98. Read Model Semantics no depende del protocolo.
99. Ninguna tecnología de lectura concreta es obligatoria.
100. Toda evolución futura del Read Model debe preservar separación
     entre lectura, escritura, ownership y Consistency Boundary.

---

# Restricciones

No está permitido:

- utilizar Read Model como Aggregate;
- utilizar Read Model como autoridad de escritura;
- ejecutar Commands desde Read Model;
- ejecutar State Transitions desde Read Model;
- modificar State directamente desde una Projection;
- modificar Version desde una Query;
- modificar IntegrationId desde Read Side;
- modificar CreatedAt desde Read Side;
- modificar UpdatedAt por una consulta;
- producir Domain Events desde una Query;
- producir Domain Events nuevos durante Projection Rebuild;
- producir Integration Events automáticamente desde una Query;
- utilizar Projection como Command Handler del Aggregate;
- utilizar Projection Lag como motivo para modificar el Aggregate;
- utilizar una Version desactualizada de Read Model para ignorar
  ConcurrencyConflict;
- interpretar Read Model Field como Aggregate Attribute automático;
- introducir nuevos Lifecycle States desde vistas;
- utilizar Connected como State del Aggregate;
- utilizar Failed como State del Aggregate;
- utilizar Pending como State del Aggregate;
- utilizar Stale como State del Aggregate;
- utilizar Rebuilding como State del Aggregate;
- utilizar Synchronizing como State del Aggregate;
- convertir IntegrationRepository en motor de reporting;
- convertir IntegrationRepository en motor de analytics;
- convertir IntegrationRepository en motor global de search por
  conveniencia;
- incluir Read Model dentro del Write Consistency Boundary;
- fusionar Boundaries mediante una vista combinada;
- transferir ownership mediante Projection;
- imponer una única estructura física de Read Model;
- imponer un único nombre de Projection;
- imponer base de datos;
- imponer search engine;
- imponer cache;
- imponer índices concretos;
- imponer TTL;
- imponer política de retención;
- imponer Event Sourcing;
- imponer Projection síncrona;
- imponer Projection asíncrona;
- imponer broker;
- imponer polling;
- imponer push;
- imponer streaming;
- imponer mecanismo técnico de idempotencia;
- imponer Exactly Once;
- revertir el Aggregate por Projection Failure;
- suspender Integration por Read Model Failure;
- reactivar Integration por Read Model Recovery;
- exponer secretos;
- exponer credenciales como datos del dominio;
- copiar automáticamente External Payload completo;
- sustituir IntegrationId por una identidad externa;
- convertir FIWARE Entity en Integration Read Model obligatorio;
- convertir un modelo municipal en el Domain Model;
- interpretar Read Access como Write Permission;
- introducir una nueva arquitectura de lectura sin necesidad explícita
  y decisión correspondiente.

---

# Compatibilidad Arquitectónica

El Read Model de Integration es compatible conceptualmente con:

- Domain-Driven Design;
- Aggregate Pattern;
- Repository Pattern;
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

- CQRS físico;
- Event Sourcing;
- base de datos;
- cache;
- search engine;
- broker;
- protocolo;
- framework;
- synchronous projection;
- asynchronous projection;
- polling;
- streaming;
- FIWARE;
- NGSI-LD;
- plataforma municipal.

---

# Definición de Éxito

El Read Model asociado al Aggregate **Integration** permite representar
información optimizada para consulta sin debilitar las reglas del Write
Model ni ampliar el Consistency Boundary.

El modelo fundamental queda expresado como:

```text
Integration Aggregate
        │
        │ confirmed domain information
        ▼
   Projection
        │
        ▼
   Read Model
        │
        ▼
      Query
```

mientras:

```text
Query
    │
    ▼
Read Model
    │
    └── no Aggregate mutation
```

y:

```text
Command
    │
    ▼
Integration Aggregate
    │
    └── domain behavior
```

El modelo garantiza que:

- Integration permanezca como autoridad de escritura;
- Read Models permanezcan como representaciones derivadas;
- Queries no modifiquen el Aggregate;
- Projections no ejecuten Commands;
- Domain Events puedan alimentar vistas sin perder ownership;
- Read Model Fields no creen atributos del Aggregate;
- State proyectado no tenga autoridad sobre Lifecycle;
- Version proyectada no tenga autoridad sobre concurrencia;
- Projection Lag sea compatible con consistencia eventual;
- Projection Failure no revierta el Aggregate;
- Projection Retry no produzca nuevos hechos;
- Rebuild no modifique State ni Version;
- Search, Filter, Sort, Pagination, Reporting y Analytics permanezcan
  en el Read Side;
- IntegrationRepository permanezca enfocado en el Write Model;
- múltiples Read Models no creen múltiples Sources of Truth;
- composición de lectura no fusione Consistency Boundaries;
- datos derivados no transfieran ownership;
- Archived pueda continuar siendo consultable sin convertirse en
  Deleted;
- credenciales y secretos permanezcan fuera del Domain Read Model;
- FIWARE permanezca separado del Domain Model;
- sistemas municipales permanezcan separados del Domain Model;
- ninguna tecnología específica sea impuesta;
- CQRS permanezca compatible pero no obligatorio;
- Event Sourcing permanezca compatible pero no obligatorio;
- cualquier nueva vista preserve la separación entre Query, Command,
  Projection, Aggregate y Consistency Boundary.

De esta forma, `DOMAIN-013L-Read-Model.md` establece formalmente las
reglas conceptuales oficiales del Read Model asociado al Aggregate
**Integration** conforme al patrón consolidado de AURA Core.