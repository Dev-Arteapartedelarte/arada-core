# DOMAIN-013I — Integration Versioning

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
- DOMAIN-013J-Consistency-Boundary.md
- DOMAIN-013K-Integration-Events.md
- DOMAIN-013L-Read-Model.md
- DOMAIN-013M-Test-Scenarios.md
- DOMAIN-013N-Performance-Rules.md
- DOMAIN-013O-Security-Model.md
- DOMAIN-013P-Extension-Points.md

---

# Objetivo

Este documento define formalmente las reglas de **Versioning** del
Aggregate **Integration**.

Version representa la evolución lógica confirmada de una única
Integration.

Su propósito es:

- identificar la evolución lógica del Aggregate;
- preservar coherencia entre modificaciones sucesivas;
- proteger modificaciones concurrentes;
- relacionar Domain Events con el estado resultante;
- distinguir la evolución de Integration de versiones externas;
- permitir reconstrucción y trazabilidad;
- preservar el Consistency Boundary.

---

# Principio Fundamental

Debe mantenerse:

```text
Integration.Version

=

Logical Aggregate Evolution
```

Version pertenece exclusivamente al Aggregate Integration.

---

# Version no es Estado

Debe mantenerse:

```text
Version

≠

State
```

State representa la condición actual del Lifecycle.

Version representa la evolución lógica del Aggregate.

---

# State no es Version

Debe mantenerse:

```text
Draft

Active

Suspended

Archived

≠

Version
```

Diferentes Integration pueden encontrarse en el mismo State con
Version diferentes.

---

# Version Inicial

Una Integration recién creada comienza con:

```text
Version = 1
```

La transición:

```text
No Integration → Draft
```

crea el Aggregate directamente en:

```text
State = Draft

Version = 1
```

---

# No Version 0 Persistida

`No Integration` representa inexistencia.

Por lo tanto:

```text
No Integration

≠

Integration Version = 0
```

Version 0 no representa una Integration persistida previa a la
creación.

---

# Creación

Un:

```text
CreateIntegration
```

válido produce:

```text
IntegrationCreated
```

con:

```text
Integration.Version = 1

IntegrationCreated.AggregateVersion = 1
```

---

# Regla de Incremento

Toda modificación válida de una Integration existente incrementa
Version exactamente una vez.

Debe mantenerse:

```text
Version N

→

Version N + 1
```

---

# Incremento Unitario

Una modificación válida no debe producir:

```text
Version N → Version N + 2
```

ni:

```text
Version N → Version N + X
```

para representar una sola modificación del Aggregate.

---

# Una Modificación, Una Nueva Version

Debe mantenerse:

```text
One Valid Aggregate Modification

=

One Version Increment
```

---

# ActivateIntegration

Si:

```text
State = Draft

Version = N
```

y:

```text
ActivateIntegration
```

es válido, el resultado es:

```text
State = Active

Version = N + 1
```

---

# SuspendIntegration

Si:

```text
State = Active

Version = N
```

y:

```text
SuspendIntegration
```

es válido, el resultado es:

```text
State = Suspended

Version = N + 1
```

---

# ReactivateIntegration

Si:

```text
State = Suspended

Version = N
```

y:

```text
ReactivateIntegration
```

es válido, el resultado es:

```text
State = Active

Version = N + 1
```

---

# ArchiveIntegration

Si:

```text
State ∈ {Draft, Active, Suspended}

Version = N
```

y:

```text
ArchiveIntegration
```

es válido, el resultado es:

```text
State = Archived

Version = N + 1
```

---

# Ejemplo de Evolución

Una secuencia válida puede producir:

```text
No Integration
    │
    │ CreateIntegration
    ▼
Draft
Version = 1
    │
    │ ActivateIntegration
    ▼
Active
Version = 2
    │
    │ SuspendIntegration
    ▼
Suspended
Version = 3
    │
    │ ReactivateIntegration
    ▼
Active
Version = 4
    │
    │ ArchiveIntegration
    ▼
Archived
Version = 5
```

Esta secuencia es ilustrativa.

No obliga a que toda Integration recorra todos esos estados.

---

# Flujo Corto

También es válido:

```text
No Integration
    │
    ▼
Draft
Version = 1
    │
    ▼
Archived
Version = 2
```

cuando:

```text
ArchiveIntegration
```

se ejecuta válidamente desde Draft.

---

# Version y Domain Events

Todo Domain Event producido por una modificación válida debe contener:

```text
AggregateVersion
```

correspondiente a la Version resultante.

Debe mantenerse:

```text
DomainEvent.AggregateVersion

=

Resulting Integration.Version
```

---

# IntegrationCreated y AggregateVersion

Debe mantenerse:

```text
IntegrationCreated.AggregateVersion = 1
```

---

# IntegrationActivated y AggregateVersion

Si ActivateIntegration modifica:

```text
Version N

→

Version N + 1
```

entonces:

```text
IntegrationActivated.AggregateVersion

=

N + 1
```

---

# IntegrationSuspended y AggregateVersion

Debe mantenerse:

```text
IntegrationSuspended.AggregateVersion

=

Resulting Integration.Version
```

---

# IntegrationReactivated y AggregateVersion

Debe mantenerse:

```text
IntegrationReactivated.AggregateVersion

=

Resulting Integration.Version
```

---

# IntegrationArchived y AggregateVersion

Debe mantenerse:

```text
IntegrationArchived.AggregateVersion

=

Resulting Integration.Version
```

---

# EventId no es Version

Debe mantenerse:

```text
EventId

≠

AggregateVersion
```

EventId identifica un hecho.

AggregateVersion identifica la posición lógica resultante de dicho
hecho dentro de la evolución de una Integration.

---

# IntegrationId no es Version

Debe mantenerse:

```text
IntegrationId

≠

Version
```

IntegrationId permanece estable.

Version evoluciona.

---

# Version por Aggregate

Cada Integration posee su propia secuencia de Version.

Conceptualmente:

```text
Integration INT-001

Version 1
Version 2
Version 3
```

y:

```text
Integration INT-002

Version 1
Version 2
```

son evoluciones independientes.

---

# No Version Global

La versión 1.0 no define:

```text
Global Integration Version
```

compartida por todas las Integration.

---

# No Orden Global

Debe mantenerse:

```text
Per-Aggregate Version Order

≠

Global Domain Order
```

Version permite ordenar modificaciones dentro de una misma
Integration.

No establece un orden total entre Aggregate Roots diferentes.

---

# Different IntegrationId

Supóngase:

```text
INT-001 Version = 7

INT-002 Version = 3
```

No puede concluirse que INT-001 sea globalmente posterior a INT-002.

---

# Same IntegrationId

Para una misma Integration:

```text
Version 3

precedes

Version 4
```

dentro de su evolución lógica.

---

# Version y Optimistic Concurrency

Version participa en Optimistic Concurrency.

Para modificar una Integration existente debe preservarse
conceptualmente:

```text
ExpectedVersion

=

PersistedVersion
```

antes de confirmar la modificación.

---

# ExpectedVersion

ExpectedVersion representa la Version sobre la cual una intención
espera operar.

No constituye la autoridad para establecer la nueva Version.

---

# ExpectedVersion no es Setter

Debe mantenerse:

```text
ExpectedVersion

≠

setVersion()
```

---

# PersistedVersion

PersistedVersion representa la Version actualmente confirmada para la
Integration correspondiente.

---

# Concurrencia Válida

Si:

```text
PersistedVersion = 4

ExpectedVersion = 4
```

y el Command es válido:

```text
Integration.Version = 5
```

puede ser confirmado conforme al Repository Contract.

---

# ConcurrencyConflict

Si:

```text
PersistedVersion = 5

ExpectedVersion = 4
```

debe producirse:

```text
ConcurrencyConflict
```

---

# Efecto de ConcurrencyConflict

Ante:

```text
ConcurrencyConflict
```

debe mantenerse:

```text
Persisted State unchanged

Persisted Version unchanged

Persisted UpdatedAt unchanged

No new confirmed success Domain Event
```

---

# No Silent Overwrite

Debe mantenerse:

```text
ConcurrencyConflict

≠

Permission to Overwrite
```

---

# No Last-Write-Wins Implícito

Versioning no debe ignorarse mediante una regla implícita:

```text
Last Write Wins
```

que sobrescriba silenciosamente una modificación concurrente
incompatible.

---

# Ejemplo de Concurrencia

Estado inicial:

```text
IntegrationId = INT-001

State = Active

Version = 4
```

Dos intenciones leen:

```text
ExpectedVersion = 4
```

Primera modificación:

```text
SuspendIntegration
```

se confirma:

```text
State = Suspended

Version = 5
```

La segunda operación todavía intenta persistir usando:

```text
ExpectedVersion = 4
```

Resultado:

```text
ConcurrencyConflict
```

---

# Permission no Evita Concurrencia

Aunque la segunda operación posea Permission válida:

```text
Authorized

+

ExpectedVersion mismatch

=

ConcurrencyConflict
```

---

# State Machine no Evita Concurrencia

Una transición semánticamente permitida también debe respetar
Versioning.

Debe mantenerse:

```text
Valid Transition

≠

Concurrency Automatically Valid
```

---

# Invariants no Evitan Concurrencia

Del mismo modo:

```text
Invariants Valid

≠

ExpectedVersion Valid
```

Ambas condiciones deben cumplirse cuando corresponda.

---

# Rejected Command

Un Command rechazado no incrementa Version.

Debe mantenerse:

```text
Version N

→

Version N
```

---

# Rechazo por State

Si:

```text
State = Active

Version = 4
```

y se intenta:

```text
ActivateIntegration
```

resultado:

```text
Rejected

Version = 4
```

---

# Rechazo por Permission

Si una Permission requerida es denegada:

```text
Version unchanged
```

---

# Rechazo por Invariant

Si una Invariant falla:

```text
Version unchanged
```

---

# Rechazo por Guard

Si un Guard falla:

```text
Version unchanged
```

---

# Rechazo por Concurrencia

Ante ConcurrencyConflict:

```text
Persisted Version unchanged
```

---

# Lecturas no Incrementan Version

Operaciones como:

```text
findById()

exists()
```

no modifican Version.

---

# Query no Incrementa Version

Debe mantenerse:

```text
Query

≠

Aggregate Modification
```

---

# Rehydration no Incrementa Version

Recuperar una Integration:

```text
Version = N
```

debe producir una Integration rehidratada con:

```text
Version = N
```

---

# Replay no Incrementa Version Artificialmente

Si Event Sourcing fuese utilizado, Replay reconstruye la Version
histórica.

No debe generar incrementos adicionales por el hecho de reconstruir.

---

# Projection no Incrementa Version

Procesar un Domain Event en una Projection no modifica:

```text
Integration.Version
```

---

# Projection Rebuild no Incrementa Version

Reconstruir un Read Model tampoco modifica Version.

---

# Integration Event no Incrementa Version

Publicar un Integration Event después de un Domain Event confirmado no
constituye una nueva modificación del Aggregate.

Por lo tanto:

```text
Integration Event Publication

≠

Version Increment
```

---

# External Publication Failure

Un fallo posterior de publicación no modifica:

```text
Integration.Version
```

ya confirmada.

---

# Retry de Publicación

Retry técnico no incrementa Version.

---

# Technical Redelivery

Una retransmisión técnica no incrementa Version por sí misma.

---

# Broker ACK

Un acknowledgement técnico no incrementa Version.

---

# Queue State

Cambios técnicos de Queue no incrementan Version.

---

# Outbox State

Cambios técnicos de Outbox no incrementan Version.

---

# Health Check

Un Health Check no incrementa Version.

---

# Monitoring

Monitoring no incrementa Version.

---

# Metrics

Cambios en:

```text
latency

throughput

error rate

availability
```

no incrementan Integration.Version.

---

# Deployment

Deployment no incrementa Version.

---

# Restart

Restart no incrementa Version.

---

# Scaling

Scaling de Infrastructure no incrementa Version.

---

# Cache

Cache hit, miss o invalidation no incrementan Integration.Version.

---

# Credential Rotation

Rotar:

```text
AccessToken

ApiKey

Certificate

Secret
```

fuera del Aggregate no incrementa Integration.Version.

---

# Credential Expiration

La expiración técnica de una credencial no modifica Version por sí
misma.

---

# Authentication

Authentication success o failure no modifica Integration.Version.

---

# Authorization Policy

Cambiar una política externa de Authorization no modifica
Integration.Version por sí mismo.

---

# Permission Assignment

Asignar o revocar una Permission fuera del Aggregate no incrementa
Version.

---

# External System Availability

Un cambio de disponibilidad de un sistema externo no incrementa
Version.

---

# FIWARE Availability

La disponibilidad o indisponibilidad de FIWARE no modifica Version.

---

# Municipal System Availability

La disponibilidad de un sistema municipal no incrementa Version.

---

# Protocol Change

Un cambio técnico de:

```text
HTTP

→

MQTT
```

no modifica automáticamente Integration.Version.

---

# Broker Change

Un cambio técnico de broker no incrementa Version por sí mismo.

---

# Persistence Technology Change

Cambiar la tecnología utilizada por Infrastructure para persistir el
Aggregate no modifica:

```text
Integration.Version
```

---

# Contract Version

Integration Contract puede poseer versionado propio.

Debe mantenerse:

```text
Integration Contract Version

≠

Integration.Version
```

---

# Contract Version no Incrementa Aggregate Version Automáticamente

Una evolución:

```text
Contract Version 1

→

Contract Version 2
```

no implica automáticamente:

```text
Integration.Version N

→

Integration.Version N + 1
```

salvo que exista además una modificación explícita del Aggregate
definida por el dominio.

---

# API Version

Debe mantenerse:

```text
API Version

≠

Integration.Version
```

---

# Schema Version

Debe mantenerse:

```text
Schema Version

≠

Integration.Version
```

---

# Domain Contract Version

La versión del documento o contrato conceptual del dominio tampoco es:

```text
Integration.Version
```

---

# Document Version

Debe mantenerse:

```text
DOMAIN-013I Document Version

≠

Integration.Version
```

---

# Application Version

Debe mantenerse:

```text
Application Version

≠

Integration.Version
```

---

# Deployment Version

Debe mantenerse:

```text
Deployment Version

≠

Integration.Version
```

---

# Database Revision

Una revisión interna de persistencia no sustituye
Integration.Version.

---

# External System Version

Debe mantenerse:

```text
External System Version

≠

Integration.Version
```

---

# FIWARE Entity Version

Si una representación externa posee algún concepto propio de
versionado:

```text
External FIWARE Version

≠

Integration.Version
```

---

# Municipal Version

Una versión propia de un sistema municipal no determina
Integration.Version.

---

# Domain Event Version

Debe distinguirse:

```text
DomainEvent.AggregateVersion
```

de cualquier versión del schema o contrato utilizado para representar
el evento.

---

# AggregateVersion versus Event Contract Version

Debe mantenerse:

```text
DomainEvent.AggregateVersion

≠

Event Contract Version
```

---

# Integration Event Contract Version

Debe mantenerse:

```text
Integration Event Contract Version

≠

Integration.Version
```

---

# Timestamps no son Version

Debe mantenerse:

```text
CreatedAt

UpdatedAt

OccurredAt

≠

Version
```

---

# CreatedAt

CreatedAt no determina Version.

La creación establece simultáneamente:

```text
Version = 1
```

y:

```text
CreatedAt
```

como conceptos diferentes.

---

# UpdatedAt

UpdatedAt acompaña una modificación válida.

No sustituye la secuencia lógica de Version.

---

# OccurredAt

DomainEvent.OccurredAt representa tiempo del hecho.

DomainEvent.AggregateVersion representa posición lógica dentro de la
evolución de la Integration.

---

# Igual Timestamp, Diferente Version

La semántica de Version no depende de que dos timestamps posean
precisión suficiente para establecer orden.

Version continúa siendo la referencia lógica por Aggregate.

---

# Repository

IntegrationRepository debe preservar Version.

---

# Repository no Decide Version

Debe mantenerse:

```text
Repository

≠

Version Authority
```

---

# Repository no Incrementa Arbitrariamente

El Repository:

- verifica Version;
- protege concurrencia;
- persiste Version;
- recupera Version.

No decide por sí mismo cuándo ocurrió una modificación válida.

---

# save()

Para una Integration existente:

```text
PersistedVersion = N

ExpectedVersion = N

Aggregate.Version = N + 1
```

representa la relación conceptual esperada para una modificación
válida.

---

# findById()

Debe recuperar exactamente:

```text
Persisted Integration.Version
```

sin incrementarla.

---

# exists()

`exists()` no modifica Version.

---

# nextIdentity()

`nextIdentity()` no crea una Version porque todavía no crea una
Integration.

---

# delete()

La existencia conceptual de:

```text
Repository.delete()
```

no introduce una nueva Version de Lifecycle.

`delete()` no constituye:

```text
DeleteIntegration
```

y no introduce:

```text
Deleted
```

como State.

---

# ArchiveIntegration y Version

ArchiveIntegration sí representa una modificación de dominio.

Por lo tanto:

```text
Version N

→

Version N + 1
```

cuando el archivado es válido.

---

# Archived Conserva Version

Después de archivarse:

```text
State = Archived

Version = N
```

donde N representa la última Version confirmada.

---

# Archived es Terminal

Debido a que Archived es terminal en versión 1.0, no existen
modificaciones ordinarias posteriores del Lifecycle que incrementen
Version.

---

# Physical Deletion no es Version Transition

Una eventual eliminación física permitida por una política externa
explícita no debe reinterpretarse como una transición de Version del
Lifecycle.

---

# Retención

Este documento no define una Version asociada a:

- retention;
- expiry;
- purge;
- deletion.

---

# Read Models

Un Read Model puede proyectar:

```text
Integration.Version
```

para consulta.

No constituye autoridad sobre ella.

---

# Projection Version no es Aggregate Version

Si una Projection utiliza internamente un mecanismo propio de
versionado:

```text
Projection Version

≠

Integration.Version
```

---

# Read Model Lag

Puede existir:

```text
Aggregate Version = 5

Read Model projected Version = 4
```

temporalmente.

Bajo consistencia eventual esto no altera:

```text
Integration.Version = 5
```

como valor autoritativo del Write Model.

---

# Read Model no Incrementa Version

Actualizar una Projection no modifica la Version del Aggregate.

---

# Audit

Audit puede preservar:

```text
SourceAggregateVersion
```

cuando el hecho fuente la proporciona.

En ese caso:

```text
Audit.SourceAggregateVersion

=

Integration.Version represented by the source fact
```

sin transferir ownership.

---

# Audit Version no es Integration Version

Debe mantenerse:

```text
Audit.Version

≠

Integration.Version
```

Ambos Aggregates mantienen evolución independiente.

---

# Notification Version

Debe mantenerse:

```text
Notification.Version

≠

Integration.Version
```

---

# Other Aggregate Version

Ningún otro Aggregate comparte automáticamente la misma Version de
Integration.

---

# Source Aggregate Version

Si Integration procesa información originada por otro Aggregate:

```text
SourceAggregateVersion

≠

Integration.Version
```

---

# CorrelationId

CorrelationId no determina Version.

---

# CausationId

CausationId no determina Version.

---

# ActorId

ActorId no determina Version.

---

# External Message Id

External Message Id no determina Version.

---

# EventId

EventId no determina Version mediante su formato o secuencia.

---

# No Derivación de Version

Integration.Version no debe derivarse automáticamente de:

```text
Timestamp

EventId

External Message Id

External Version

Contract Version

API Version

Database Revision
```

---

# Source of Truth

El Aggregate Integration es autoridad sobre su propia Version.

Debe mantenerse:

```text
Integration

=

Source of Truth for Integration.Version
```

---

# External System no es Version Authority

Debe mantenerse:

```text
External System

≠

Authority for Integration.Version
```

---

# FIWARE no es Version Authority

Debe mantenerse:

```text
FIWARE

≠

Authority for Integration.Version
```

---

# Municipal System no es Version Authority

Debe mantenerse:

```text
Municipal System

≠

Authority for Integration.Version
```

---

# Infrastructure no es Version Authority

Infrastructure implementa persistencia y concurrencia.

No redefine la semántica de Version.

---

# Database Sequence no es Version

Una secuencia de base de datos no constituye automáticamente
Integration.Version.

---

# ORM Revision no es Version

Un mecanismo interno de ORM no redefine Version.

---

# Cache Version no es Aggregate Version

Una Cache puede utilizar metadata propia.

Debe mantenerse:

```text
Cache Version

≠

Integration.Version
```

---

# Replica Version no es Aggregate Version

Una réplica técnica puede poseer metadata interna independiente.

No reemplaza Integration.Version.

---

# Snapshot Version

Si una estrategia futura utiliza Snapshots:

```text
Snapshot Version
```

debe distinguirse conceptualmente de Integration.Version salvo que
represente explícitamente la Version del Aggregate en el punto del
Snapshot.

La existencia de Snapshots no se establece como requisito.

---

# Event Sourcing

Versioning es compatible con Event Sourcing.

Debe mantenerse:

```text
Event Sourcing Compatible

≠

Event Sourcing Required
```

---

# Rehydration mediante Eventos

Si Event Sourcing fuese utilizado, la rehidratación debe reconstruir
la misma Version lógica confirmada.

---

# Event Stream

Una secuencia conceptual válida puede ser:

```text
IntegrationCreated
AggregateVersion = 1

IntegrationActivated
AggregateVersion = 2

IntegrationSuspended
AggregateVersion = 3

IntegrationReactivated
AggregateVersion = 4

IntegrationArchived
AggregateVersion = 5
```

---

# No Gaps por Replay

Replay no debe producir:

```text
AggregateVersion = 6
```

solamente porque se reconstruyeron cinco eventos existentes.

El resultado continúa siendo:

```text
Version = 5
```

---

# CQRS

En CQRS:

```text
Write Model

owns

Integration.Version
```

mientras:

```text
Read Model

may project

Integration.Version
```

---

# Consistency Boundary

Version pertenece al Consistency Boundary de una única Integration.

Debe mantenerse:

```text
One IntegrationId

=

One Independent Version Sequence
```

---

# No Shared Aggregate Version

Dos Aggregates no comparten una sola Version solamente porque
participen en la misma integración de negocio.

---

# External Consistency

La consistencia eventual con otros sistemas no exige igualar sus
versiones.

---

# Integration Commit

Debe mantenerse:

```text
Integration Commit Version

≠

External System Commit Version
```

---

# No Distributed Version

La versión 1.0 no define una Version distribuida que abarque:

```text
Integration

+

External System
```

---

# No Cross-Aggregate Version

Tampoco existe una Version común que abarque:

```text
Integration

+

Audit

+

Notification

+

Assembly
```

---

# Domain Event Ordering

Para una misma Integration:

```text
AggregateVersion
```

proporciona orden lógico entre sus Domain Events confirmados.

---

# No Global Event Ordering

No se establece:

```text
Global Event Order
```

mediante Integration.Version.

---

# Version y Idempotencia

Versioning no define por sí mismo la estrategia técnica de
idempotencia.

Debe mantenerse:

```text
Aggregate Versioning

≠

Complete Idempotency Strategy
```

---

# Technical Redelivery y Version

Recibir nuevamente el mismo mensaje técnico no debe interpretarse
automáticamente como:

```text
Version N → Version N + 1
```

---

# Nueva Intención Real

Solamente una nueva modificación válida del Aggregate incrementa
Version.

---

# Duplicate Command Delivery

La entrega duplicada de una misma representación técnica de Command no
define automáticamente dos modificaciones de dominio.

La estrategia concreta para resolver deduplicación permanece fuera de
este documento.

---

# Version y Data Minimization

Version no requiere almacenar Snapshots externos completos.

---

# Version y Security

Ninguna Permission permite modificar Version directamente.

---

# Permission no es Version Authority

Debe mantenerse:

```text
Integration.Create

Integration.Activate

Integration.Suspend

Integration.Reactivate

Integration.Archive

≠

Authority to set arbitrary Version
```

---

# Authentication no Modifica Version

Authentication no incrementa Version.

---

# Authorization Failure no Modifica Version

Una operación rechazada antes de llegar al comportamiento válido del
Aggregate mantiene:

```text
Version unchanged
```

---

# Security Incident no Modifica Version Automáticamente

Un hecho técnico de seguridad no modifica Integration.Version salvo que
posteriormente exista un Command válido del dominio que modifique el
Aggregate.

---

# Version y Performance

Ninguna optimización puede evitar las reglas de Versioning.

Debe mantenerse:

```text
Performance Optimization

≠

Versioning Bypass
```

---

# Batch Processing

Un proceso técnico puede manejar varias Integration.

Cada una mantiene:

```text
own IntegrationId

own Version

own ExpectedVersion

own Consistency Boundary
```

---

# Bulk Update

Una operación técnica sobre múltiples Integration no transforma sus
Version independientes en una única Version compartida.

---

# No Version por Lote

La versión 1.0 no define:

```text
BatchVersion
```

como Version del dominio Integration.

---

# Archived y Version Histórica

Una Integration Archived conserva su última Version confirmada.

Ejemplo:

```text
IntegrationId = INT-001

State = Archived

Version = 8
```

Version 8 continúa representando la última evolución lógica de esa
Integration.

---

# Historial no se Reescribe

Una modificación posterior en otro sistema no cambia retroactivamente:

```text
Integration.Version
```

histórica.

---

# Historical Domain Event

Un Domain Event histórico conserva su:

```text
AggregateVersion
```

original.

---

# No Renumbering

Los Domain Events históricos no deben renumerarse para adaptarse a
cambios posteriores.

---

# No Version Reset

La versión 1.0 no define:

```text
ResetIntegrationVersion
```

---

# Archived no Vuelve a Version 1

Archivar una Integration no reinicia Version.

---

# Reactivation no Reinicia Version

La transición:

```text
Suspended → Active
```

continúa la secuencia existente.

Ejemplo:

```text
Suspended Version = 6

ReactivateIntegration

Active Version = 7
```

---

# Suspension no Reinicia Version

La transición:

```text
Active → Suspended
```

continúa la secuencia.

---

# Estado Repetido, Nueva Version

Una Integration puede estar:

```text
Active Version = 2
```

luego:

```text
Suspended Version = 3
```

luego:

```text
Active Version = 4
```

El State puede volver a Active mediante ReactivateIntegration.

Version nunca retrocede.

---

# Monotonicidad

Para una misma Integration:

```text
Version
```

es monotónicamente creciente ante modificaciones válidas.

---

# Version no Retrocede

No está permitido:

```text
Version 5 → Version 4
```

mediante comportamiento ordinario.

---

# Version no se Reutiliza

Una misma Integration no debe confirmar dos estados diferentes como:

```text
Version = N
```

dentro de su evolución lógica.

---

# One Version, One Confirmed Aggregate Revision

Debe mantenerse:

```text
One IntegrationId + One Version

=

One Confirmed Logical Aggregate Revision
```

---

# Version y Domain Event Correspondence

Cuando una modificación válida produce un Domain Event, la Version
resultante y AggregateVersion deben identificar la misma revisión
lógica.

---

# No Event Version Ahead

No debe existir un Domain Event confirmado con:

```text
AggregateVersion > Integration.Version
```

para el mismo estado confirmado.

---

# No Event Version Behind

El Domain Event correspondiente a una modificación no debe representar
la Version anterior.

Ejemplo:

```text
Before = Version 4

After = Version 5

DomainEvent.AggregateVersion = 5
```

---

# Version y CreatedAt

La creación establece:

```text
Version = 1

CreatedAt = creation time
```

Ambos permanecen semánticamente distintos.

---

# Version y UpdatedAt

Para una modificación válida:

```text
Version N → N + 1

UpdatedAt → modification time
```

conforme a las reglas temporales del Aggregate.

---

# Rechazo y UpdatedAt

Si Version no cambia por rechazo:

```text
UpdatedAt
```

tampoco cambia.

---

# Version y Repository Round-Trip

Debe cumplirse:

```text
Integration Version = N
    │
    ▼
save()
    │
    ▼
findById()
    │
    ▼
Integration Version = N
```

cuando no exista una modificación posterior.

---

# Persistencia no Incrementa Version

Persistir nuevamente una representación sin una nueva modificación de
dominio no debe inventar una nueva Version.

---

# Rehydration Round-Trip

Debe preservarse exactamente la Version confirmada.

---

# Version y Integration Events

Un futuro Integration Event puede transportar información de Version
cuando su contrato explícito lo requiera.

Esto no convierte:

```text
Integration Event Contract Version
```

en:

```text
Integration.Version
```

---

# No Integration Event Obligatorio

La existencia de una nueva Integration.Version no obliga a publicar un
Integration Event.

Debe mantenerse:

```text
Version Increment

≠

Mandatory Integration Event
```

---

# Version y Audit

Un Domain Event de Integration puede permitir a Audit preservar la
SourceAggregateVersion correspondiente.

Audit no controla ni incrementa Integration.Version.

---

# Audit Failure

Un fallo posterior de Audit no revierte:

```text
Integration.Version
```

confirmada.

---

# Notification Failure

Un fallo posterior de Notification tampoco revierte Version.

---

# External Consumer Failure

Un consumidor externo que no procese un hecho no cambia la Version
confirmada del Aggregate.

---

# Version y Consistencia Eventual

Puede existir:

```text
Integration.Version = 6

External Consumer knows Version = 5
```

temporalmente.

Esto no crea dos Version autoritativas.

---

# Write Model Authority

La Version autoritativa pertenece al Write Model de Integration.

---

# Read Side Lag

El retraso del Read Side no obliga a reducir o repetir la Version del
Aggregate.

---

# Evolución Futura

Cualquier nueva modificación de dominio que altere Integration debe
definir explícitamente su efecto sobre Version.

---

# Nuevo Command

Un nuevo Command futuro deberá establecer si:

```text
it modifies Integration

or

it does not modify Integration
```

Si modifica válidamente el Aggregate:

```text
Version N → N + 1
```

---

# Nueva Transición

Toda nueva transición válida de Lifecycle implica una modificación del
Aggregate y debe respetar Versioning.

---

# Nuevo Domain Event

Un nuevo Domain Event asociado a una modificación deberá preservar:

```text
AggregateVersion

=

Resulting Integration.Version
```

---

# Nuevo Atributo

Incorporar un atributo futuro al Aggregate no autoriza modificar
Version fuera de comportamiento de dominio explícito.

---

# Evolución de Repository

Cambiar la implementación de Repository no modifica la semántica de
Version.

---

# Evolución de Infrastructure

Cambiar:

- database;
- broker;
- framework;
- protocol;
- provider;

no redefine Integration.Version.

---

# Impacto de una Evolución de Versioning

Toda modificación de estas reglas debe revisar coherencia con:

```text
DOMAIN-013-Aggregate.md

DOMAIN-013A-Lifecycle.md

DOMAIN-013B-State-Machine.md

DOMAIN-013C-Commands.md

DOMAIN-013D-Domain-Events.md

DOMAIN-013E-Invariants.md

DOMAIN-013G-Repository-Contract.md

DOMAIN-013H-Examples.md

DOMAIN-013J-Consistency-Boundary.md

DOMAIN-013L-Read-Model.md

DOMAIN-013M-Test-Scenarios.md

DOMAIN-013P-Extension-Points.md
```

---

# Regla de No Inferencia

Debe mantenerse:

```text
Technical Version

≠

Domain Aggregate Version
```

y:

```text
External Version Change

≠

Automatic Integration Version Change
```

y:

```text
Technical Activity

≠

Automatic Version Increment
```

---

# Reglas Fundamentales

Versioning de Integration debe cumplir:

1. Version pertenece exclusivamente a Integration.
2. Version representa evolución lógica del Aggregate.
3. Version no es State.
4. State no es Version.
5. Toda Integration nueva comienza en Version 1.
6. No Integration no representa Version 0 persistida.
7. CreateIntegration válido establece Version 1.
8. IntegrationCreated.AggregateVersion es 1.
9. Toda modificación válida posterior incrementa Version exactamente
   una vez.
10. Version evoluciona N → N + 1.
11. Una sola modificación no salta arbitrariamente múltiples
    Version.
12. ActivateIntegration válido incrementa Version.
13. SuspendIntegration válido incrementa Version.
14. ReactivateIntegration válido incrementa Version.
15. ArchiveIntegration válido incrementa Version.
16. DomainEvent.AggregateVersion coincide con la Version resultante.
17. EventId no es Version.
18. IntegrationId no es Version.
19. Cada Integration mantiene una secuencia de Version independiente.
20. No existe Version global de todas las Integration.
21. Version establece orden lógico solamente dentro de una misma
    Integration.
22. Version no establece orden global.
23. ExpectedVersion representa la Version esperada para una
    modificación.
24. ExpectedVersion no permite establecer Version directamente.
25. ExpectedVersion debe coincidir con PersistedVersion cuando
    corresponda.
26. Una diferencia entre ExpectedVersion y PersistedVersion produce
    ConcurrencyConflict.
27. ConcurrencyConflict no permite Silent Overwrite.
28. Last-Write-Wins no se infiere como mecanismo para ignorar
    Versioning.
29. Permission no evita ConcurrencyConflict.
30. State Machine válida no evita control de concurrencia.
31. Invariants válidas no eliminan control de concurrencia.
32. Un Command rechazado no incrementa Version.
33. Un Permission Failure no incrementa Version.
34. Un Guard Failure no incrementa Version.
35. Un Invariant Failure no incrementa Version.
36. Una lectura no incrementa Version.
37. findById() no incrementa Version.
38. exists() no incrementa Version.
39. Rehydration no incrementa Version.
40. Replay no incrementa Version artificialmente.
41. Projection no incrementa Version.
42. Projection Rebuild no incrementa Version.
43. Publicar Integration Events no incrementa Version.
44. Publication Failure no modifica Version.
45. Technical Retry no incrementa Version.
46. Technical Redelivery no incrementa Version automáticamente.
47. Broker ACK no incrementa Version.
48. Queue State no incrementa Version.
49. Outbox State no incrementa Version.
50. Health Check no incrementa Version.
51. Monitoring no incrementa Version.
52. Metrics no incrementan Version.
53. Deployment no incrementa Version.
54. Restart no incrementa Version.
55. Scaling no incrementa Version.
56. Cache no incrementa Version.
57. Credential Rotation no incrementa Version por sí misma.
58. Credential Expiration no incrementa Version.
59. Authentication no incrementa Version.
60. Authorization Policy Change no incrementa Version por sí mismo.
61. Permission Assignment o Revocation no incrementan Version.
62. External System Availability no incrementa Version.
63. FIWARE Availability no incrementa Version.
64. Municipal System Availability no incrementa Version.
65. Protocol Change no incrementa Version automáticamente.
66. Broker Change no incrementa Version automáticamente.
67. Persistence Technology Change no incrementa Version.
68. Integration Contract Version no es Integration.Version.
69. API Version no es Integration.Version.
70. Schema Version no es Integration.Version.
71. Document Version no es Integration.Version.
72. Application Version no es Integration.Version.
73. Deployment Version no es Integration.Version.
74. Database Revision no es Integration.Version.
75. External System Version no es Integration.Version.
76. Event Contract Version no es AggregateVersion.
77. Integration Event Contract Version no es Integration.Version.
78. Timestamp no es Version.
79. CreatedAt no es Version.
80. UpdatedAt no es Version.
81. OccurredAt no es Version.
82. Repository preserva Version pero no decide cuándo incrementarla.
83. Repository no incrementa Version arbitrariamente.
84. findById() recupera la Version persistida.
85. nextIdentity() no crea Version.
86. Repository.delete() no constituye una transición de Version.
87. Archived conserva su última Version confirmada.
88. Archived no reinicia Version.
89. Reactivation no reinicia Version.
90. Version es monotónicamente creciente para una misma Integration.
91. Version nunca retrocede mediante comportamiento ordinario.
92. Una Version no se reutiliza para dos revisiones lógicas
    diferentes de la misma Integration.
93. Event Sourcing es compatible pero no obligatorio.
94. Replay reconstruye la Version histórica.
95. CQRS no cambia la semántica de Version.
96. Read Models pueden proyectar Version pero no controlarla.
97. Audit.Version no es Integration.Version.
98. SourceAggregateVersion no es Integration.Version salvo que
    represente explícitamente la Version de Integration en el hecho
    fuente correspondiente.
99. Una nueva modificación futura debe declarar su impacto sobre
    Version.
100. Toda evolución de Versioning debe preservar el Consistency
     Boundary y los contratos oficiales del Aggregate.

---

# Restricciones

No está permitido:

- crear una Integration persistida con Version 0;
- crear una Integration nueva con una Version distinta de 1;
- modificar Version directamente;
- exponer setVersion();
- reducir Version;
- reiniciar Version después de una transición;
- reutilizar una Version para dos revisiones distintas;
- saltar Version arbitrariamente para una sola modificación;
- incrementar Version después de un Command rechazado;
- incrementar Version después de Permission Failure;
- incrementar Version después de Guard Failure;
- incrementar Version después de Invariant Failure;
- incrementar Version después de ConcurrencyConflict;
- incrementar Version por una lectura;
- incrementar Version por Rehydration;
- incrementar Version por Replay;
- incrementar Version por Projection;
- incrementar Version por Projection Rebuild;
- incrementar Version por publicación externa;
- incrementar Version por retry técnico;
- incrementar Version por broker ACK;
- incrementar Version por Queue State;
- incrementar Version por Outbox State;
- incrementar Version por Health Check;
- incrementar Version por Monitoring;
- incrementar Version por Metrics;
- incrementar Version por Deployment;
- incrementar Version por Restart;
- incrementar Version por Scaling;
- incrementar Version por Cache;
- incrementar Version por rotación de credenciales;
- incrementar Version por disponibilidad externa;
- utilizar Timestamp como Version;
- utilizar EventId como Version;
- utilizar IntegrationId como Version;
- utilizar Contract Version como Integration.Version;
- utilizar API Version como Integration.Version;
- utilizar Schema Version como Integration.Version;
- utilizar External System Version como Integration.Version;
- utilizar Database Revision como Integration.Version;
- permitir que Repository decida incrementos arbitrariamente;
- permitir Silent Overwrite ante ConcurrencyConflict;
- utilizar Last-Write-Wins para evitar el control de concurrencia;
- permitir que Permission evite Versioning;
- permitir que Infrastructure redefina Version;
- utilizar Read Model como autoridad de Version;
- compartir una Version entre diferentes IntegrationId;
- inferir una Version global;
- inferir orden global mediante AggregateVersion;
- interpretar Archived como reinicio de Version;
- interpretar Repository.delete() como nueva revisión del Lifecycle;
- crear Version por Technical Redelivery;
- modificar Version por External Publication Failure;
- modificar Version de Integration porque Audit o Notification
  evolucionen;
- introducir una nueva semántica de Version sin revisar los contratos
  de dominio afectados.

---

# Compatibilidad Arquitectónica

El Versioning de Integration es compatible con:

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

- base de datos;
- ORM;
- Event Store;
- broker;
- protocolo;
- framework;
- mecanismo de locking físico;
- mecanismo de serialización;
- FIWARE;
- plataforma municipal.

---

# Definición de Éxito

El Versioning del Aggregate **Integration** permite representar de
manera inequívoca su evolución lógica y proteger modificaciones
concurrentes sin acoplar el dominio a mecanismos físicos de
persistencia.

El comportamiento fundamental queda definido como:

```text
No Integration
    │
    │ CreateIntegration
    ▼
Draft
Version = 1
    │
    │ Valid Modification
    ▼
Version = 2
    │
    │ Valid Modification
    ▼
Version = 3
    │
    ▼
   ...
```

y:

```text
Valid Modification

Version N

→

Version N + 1
```

mientras:

```text
Rejected Operation

Version N

→

Version N
```

El modelo garantiza que:

- toda Integration comience en Version 1;
- No Integration no represente una Version persistida;
- Version evolucione únicamente mediante modificaciones válidas;
- cada modificación válida incremente Version exactamente una vez;
- Version sea monotónicamente creciente;
- Version nunca retroceda;
- AggregateVersion de cada Domain Event corresponda a la Version
  resultante;
- cada IntegrationId mantenga su propia secuencia de Version;
- no exista Version global implícita;
- ExpectedVersion proteja modificaciones concurrentes;
- ConcurrencyConflict impida sobrescrituras incompatibles;
- Permission no permita evitar Versioning;
- Repository preserve Version sin decidir arbitrariamente su
  evolución;
- Read Models proyecten Version sin poseer autoridad de escritura;
- Replay y Rehydration preserven Version sin generar incrementos;
- publicaciones externas no alteren Version;
- fallos técnicos no alteren Version;
- credenciales, protocolos, brokers y disponibilidad externa no
  alteren Version;
- Contract Version permanezca separada;
- API Version permanezca separada;
- Schema Version permanezca separada;
- External System Version permanezca separada;
- timestamps permanezcan separados de Version;
- Audit y otros Aggregates mantengan sus propias versiones;
- Event Sourcing permanezca compatible pero no obligatorio;
- CQRS no cambie la semántica del Aggregate;
- cualquier evolución futura preserve la relación entre identidad,
  modificación válida, Version, Domain Event y Consistency Boundary.

De esta forma, `DOMAIN-013I-Versioning.md` establece formalmente las
reglas oficiales de Versioning del Aggregate **Integration** conforme
al patrón consolidado de AURA Core.