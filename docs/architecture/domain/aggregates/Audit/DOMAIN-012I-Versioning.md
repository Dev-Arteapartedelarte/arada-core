# DOMAIN-012I — Audit Versioning

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
- DOMAIN-012J-Consistency-Boundary.md
- DOMAIN-012K-Integration-Events.md
- DOMAIN-012L-Read-Model.md
- DOMAIN-012M-Test-Scenarios.md

---

# Objetivo

Este documento define formalmente las reglas conceptuales de
**Versioning** del Aggregate **Audit**.

Version permite representar la evolución lógica de una unidad Audit
y proteger su consistencia frente a modificaciones concurrentes.

Version pertenece exclusivamente al Aggregate:

```text
Audit
```

y debe permanecer independiente de cualquier Version perteneciente
al hecho o Aggregate originador.

---

# Principio Fundamental

Debe mantenerse:

```text
Audit.Version

=

Logical Evolution of Audit
```

y:

```text
Audit.Version

≠

SourceAggregateVersion
```

Cada Aggregate mantiene su propia evolución lógica.

---

# Propósito de Version

Version permite:

- identificar la evolución lógica del Aggregate;
- relacionar modificaciones válidas con Domain Events;
- detectar escrituras concurrentes incompatibles;
- proteger contra sobrescritura de estado confirmado;
- preservar orden dentro de una identidad Audit;
- soportar Optimistic Concurrency Control;
- mantener compatibilidad con CQRS;
- mantener compatibilidad con Event Sourcing.

---

# Propiedad de Version

Version pertenece a:

```text
Audit
```

No pertenece a:

- Repository;
- Source Aggregate;
- Source Domain Event;
- Integration Event;
- Read Model;
- Infrastructure;
- base de datos;
- broker;
- sistema externo.

---

# Version Inicial

La creación válida del Aggregate mediante:

```text
RecordAudit
```

produce:

```text
No Audit → Recorded
```

y establece:

```text
Audit.Version = 1
```

---

# Creación

El flujo oficial es:

```text
No Audit
    │
    ▼
RecordAudit
    │
    ▼
Recorded
    │
    ▼
Version = 1
    │
    ▼
AuditRecorded
AggregateVersion = 1
```

La Version inicial solamente existe después de una creación válida.

---

# No Audit y Version

Mientras:

```text
No Audit
```

represente inexistencia del Aggregate:

```text
Audit.Version
```

no existe como Version persistida del dominio.

Debe mantenerse:

```text
No Audit

≠

Version = 0
```

como regla obligatoria del dominio.

La inexistencia del Aggregate no requiere un estado lógico
Version 0 persistido.

---

# Incremento de Version

Toda modificación válida del Aggregate debe incrementar:

```text
Version
```

exactamente una vez.

Conceptualmente:

```text
Version = N

    │
    ▼

Valid Aggregate Modification

    │
    ▼

Version = N + 1
```

---

# Una Modificación, Un Incremento

Debe mantenerse:

```text
One Valid Aggregate Modification

=

One Version Increment
```

Una misma modificación válida no puede producir múltiples
incrementos arbitrarios de Version.

---

# Version 1.0 del Lifecycle

La versión 1.0 del dominio define únicamente:

```text
No Audit → Recorded
```

mediante:

```text
RecordAudit
```

Por lo tanto, dentro del comportamiento actualmente definido:

```text
Recorded Audit

Version = 1
```

después de su creación válida.

No existe un Command posterior que modifique el Aggregate en esta
versión.

---

# Recorded es Terminal

`Recorded` es terminal en:

```text
DOMAIN-012A-Lifecycle.md
```

Por lo tanto, la versión 1.0 no define transiciones posteriores que
incrementen Version.

Esto no convierte Version en un atributo innecesario.

Version continúa formando parte del contrato consolidado del
Aggregate y permite evolución futura controlada.

---

# Version no es Estado

Debe mantenerse:

```text
Version

≠

AuditStatus
```

Para la versión 1.0:

```text
AuditStatus = Recorded

Audit.Version = 1
```

son conceptos diferentes.

---

# Version no Determina State Machine

Un valor de Version no autoriza una transición.

Debe mantenerse:

```text
Version

≠

Transition Permission
```

State Machine continúa siendo definida por:

```text
DOMAIN-012B-State-Machine.md
```

---

# Modificación Rechazada

Una operación rechazada no incrementa Version.

Debe mantenerse:

```text
Version = N

    │
    ▼

Rejected Operation

    │
    ▼

Version = N
```

---

# Creación Rechazada

Si:

```text
RecordAudit
```

es rechazado antes de crear válidamente el Aggregate:

```text
No Audit
```

permanece como inexistencia.

No debe producirse:

```text
Version = 1
```

persistida para dicha unidad.

---

# Rechazo y Domain Events

Una operación rechazada no produce un Domain Event de éxito.

Por lo tanto:

```text
Rejected RecordAudit

↓

No AuditRecorded

No Version Increment
```

---

# Lectura

Leer Audit no modifica Version.

Debe mantenerse:

```text
findById()

≠

Version Increment
```

y:

```text
Query

≠

Version Increment
```

---

# exists()

Verificar existencia mediante:

```text
exists()
```

no modifica Version.

---

# nextIdentity()

Solicitar una identidad mediante:

```text
nextIdentity()
```

no crea el Aggregate y no establece Version.

Debe mantenerse:

```text
New AuditId

≠

Audit Version Created
```

hasta que exista una creación válida.

---

# Rehidratación

Rehidratar un Audit no incrementa Version.

Debe mantenerse:

```text
Rehydration

≠

Aggregate Modification
```

y:

```text
Rehydration

≠

Version Increment
```

---

# Replay

Reproducir eventos históricos para reconstruir estado no incrementa
Version como una nueva modificación.

Debe mantenerse:

```text
Replay

≠

New Domain Behavior
```

La Version reconstruida debe corresponder al historial ya
confirmado.

---

# Domain Event y AggregateVersion

Todo Domain Event producido por Audit debe reflejar la Version
resultante del Aggregate.

Debe mantenerse:

```text
DomainEvent.AggregateVersion

=

Resulting Audit.Version
```

---

# AuditRecorded

Para la creación oficial:

```text
RecordAudit

↓

Audit.Version = 1

↓

AuditRecorded.AggregateVersion = 1
```

---

# AggregateVersion no es EventId

Debe mantenerse:

```text
AggregateVersion

≠

EventId
```

EventId identifica el hecho.

AggregateVersion identifica la evolución lógica del Aggregate que
produjo ese hecho.

---

# EventId no Determina Version

Un EventId no establece ni reemplaza:

```text
AggregateVersion
```

Ambos conceptos permanecen independientes.

---

# SourceAggregateVersion

Cuando Audit preserve:

```text
SourceAggregateVersion
```

este valor representa la Version del Aggregate que originó el hecho
auditable.

Debe mantenerse:

```text
SourceAggregateVersion

≠

Audit.Version
```

---

# Independencia Semántica de Versions

Ejemplo:

```text
SourceAggregateVersion = 8

Audit.Version = 1
```

significa:

- el Source Aggregate produjo el hecho en su Version 8;
- Audit se encuentra en su propia Version 1.

No existe relación aritmética obligatoria entre ambos valores.

---

# Coincidencia Numérica

Puede existir:

```text
SourceAggregateVersion = 1

Audit.Version = 1
```

sin que ambas Versions sean el mismo concepto.

Debe mantenerse:

```text
Numeric Equality

≠

Semantic Identity
```

---

# Cambio Posterior del Source Aggregate

Después de registrar Audit:

```text
Audit.Version = 1
```

el Source Aggregate puede evolucionar:

```text
SourceAggregateVersion = N

↓

SourceAggregateVersion = N + 1
```

sin modificar automáticamente:

```text
Audit.Version
```

---

# Nuevo Source Fact

Un nuevo hecho del mismo Source Aggregate puede producir otra unidad
Audit.

Conceptualmente:

```text
Source Fact A
    │
    ▼
Audit A
Version = 1

Source Fact B
    │
    ▼
Audit B
Version = 1
```

Cada identidad Audit mantiene Version independiente.

---

# AuditId y Version

Version evoluciona dentro de una única identidad:

```text
AuditId
```

Debe mantenerse:

```text
Version

belongs to

AuditId
```

Una Version no debe transferirse entre Audits distintos.

---

# Independencia entre Audits

Debe mantenerse:

```text
Audit A.Version

≠

Audit B.Version
```

como evoluciones lógicas independientes.

Aunque ambos valores puedan ser:

```text
1
```

pertenecen a identidades distintas.

---

# No Version Global

El dominio no define:

```text
GlobalAuditVersion
```

para ordenar todos los Audit Aggregates.

Debe mantenerse:

```text
Per Aggregate Versioning

≠

Global Audit Ordering
```

---

# Orden por Aggregate

Cuando exista más de un Domain Event para una identidad en una
evolución futura, el orden debe preservarse mediante:

```text
AggregateVersion
```

dentro de:

```text
AuditId
```

No se exige orden global entre identidades distintas.

---

# Optimistic Concurrency Control

Audit utiliza conceptualmente:

```text
Optimistic Concurrency Control
```

El principio consiste en comparar:

```text
ExpectedVersion
```

con:

```text
PersistedVersion
```

antes de confirmar una escritura sobre una unidad existente.

---

# Regla de Concurrencia

Debe cumplirse:

```text
ExpectedVersion

=

PersistedVersion
```

antes de confirmar una modificación válida sobre un Audit ya
existente.

---

# ConcurrencyConflict

Cuando:

```text
ExpectedVersion

≠

PersistedVersion
```

la escritura debe ser rechazada mediante:

```text
ConcurrencyConflict
```

---

# Escritura Obsoleta

Una escritura basada en una Version anterior no debe sobrescribir
silenciosamente un estado más reciente.

Conceptualmente:

```text
PersistedVersion = 5

ExpectedVersion = 4

    │
    ▼

ConcurrencyConflict
```

---

# ConcurrencyConflict no Incrementa Version

Un conflicto de concurrencia no constituye modificación válida.

Debe mantenerse:

```text
ConcurrencyConflict

≠

Version Increment
```

---

# ConcurrencyConflict no es AuditStatus

Debe mantenerse:

```text
ConcurrencyConflict

≠

AuditStatus
```

No produce:

```text
Failed
```

ni ningún otro estado inexistente.

---

# Repository

El Repository debe verificar y persistir Version conforme al
contrato definido en:

```text
DOMAIN-012G-Repository-Contract.md
```

El Repository no decide la Version de dominio.

---

# Repository no Incrementa Version

Debe mantenerse:

```text
Repository.save()

≠

Version Increment Authority
```

La secuencia correcta es:

```text
Valid Aggregate Modification
    │
    ▼
Aggregate increments Version
    │
    ▼
Repository verifies persistence conditions
    │
    ▼
Repository persists resulting Version
```

---

# Persistencia de Version

Si:

```text
Audit.Version = N
```

es persistido correctamente, una recuperación posterior debe
reconstruir:

```text
Audit.Version = N
```

salvo que haya ocurrido posteriormente una modificación válida.

---

# Version no es Timestamp

Debe mantenerse:

```text
Version

≠

CreatedAt
```

y:

```text
Version

≠

UpdatedAt
```

Version representa evolución lógica.

Los timestamps representan información temporal.

---

# UpdatedAt

Una modificación válida que en una evolución futura incremente
Version puede actualizar:

```text
UpdatedAt
```

conforme a las reglas del Aggregate.

Sin embargo:

```text
Version

≠

UpdatedAt
```

y no existe una equivalencia automática entre ambos valores.

---

# CreatedAt

La creación válida establece:

```text
Version = 1
```

y:

```text
CreatedAt
```

como conceptos distintos confirmados dentro de la misma modificación
válida.

CreatedAt no determina Version.

---

# SourceOccurredAt

El momento del Source Fact tampoco determina Audit.Version.

Debe mantenerse:

```text
SourceOccurredAt

≠

Audit.Version
```

---

# AuditRecorded.OccurredAt

El timestamp:

```text
AuditRecorded.OccurredAt
```

no sustituye:

```text
AggregateVersion
```

El orden lógico dentro del Aggregate se expresa mediante Version.

---

# Version y Permissions

Permissions no pueden modificar Version directamente.

Debe mantenerse:

```text
Authorized

≠

Version Mutation Authority
```

---

# Privilegio Elevado

Ningún actor o proceso, independientemente de sus permisos, puede
ejecutar:

```text
setVersion(...)
```

como comportamiento válido del dominio.

---

# Version y Invariants

Version forma parte de las reglas protegidas por:

```text
DOMAIN-012E-Invariants.md
```

Toda modificación válida debe preservar coherencia entre:

```text
State

Version

Domain Event

UpdatedAt
```

cuando corresponda.

---

# Atomicidad

Una modificación válida debe confirmar de forma coherente:

```text
Domain State

+

Version

+

UpdatedAt

+

Domain Event
```

cuando cada uno corresponda al comportamiento ejecutado.

No debe confirmarse solamente una parte dejando al Aggregate
inconsistente.

---

# Creación Atómica

Para:

```text
RecordAudit
```

debe confirmarse coherentemente:

```text
AuditId

State = Recorded

Version = 1

CreatedAt

AuditRecorded
AggregateVersion = 1
```

conforme al contrato de persistencia.

---

# Fallo de Persistencia

Si la persistencia no puede confirmarse:

```text
PersistenceFailure
```

no debe utilizarse para incrementar una Version persistida
inexistente.

Debe mantenerse:

```text
PersistenceFailure

≠

Valid Version Increment
```

---

# RepositoryUnavailable

La indisponibilidad del Repository:

```text
RepositoryUnavailable
```

no constituye una modificación válida del Aggregate.

No incrementa Version.

---

# DuplicateAuditId

Un intento incompatible de crear una identidad ya existente:

```text
DuplicateAuditId
```

no produce una nueva Version del Audit existente.

---

# Retry Técnico

Un retry técnico de persistencia o procesamiento no incrementa
Audit.Version por el solo hecho de repetirse.

Debe mantenerse:

```text
Technical Retry

≠

Domain Modification
```

y:

```text
Technical Retry

≠

Version Increment
```

---

# Duplicate Technical Delivery

La recepción repetida del mismo mensaje técnico no incrementa
automáticamente Version.

Debe mantenerse:

```text
Duplicate Technical Delivery

≠

Audit Version Increment
```

---

# Integration Event Publication

Publicar un Integration Event derivado de Audit no modifica el
Aggregate.

Debe mantenerse:

```text
Integration Event Publication

≠

Audit Version Increment
```

---

# Retry de Integration Event

Un retry técnico de publicación externa tampoco modifica Version.

Debe mantenerse:

```text
Integration Publication Retry

≠

Audit Version Increment
```

---

# Outbox

Cuando se utilice Outbox, su procesamiento no modifica:

```text
Audit.Version
```

Estados técnicos como:

```text
Pending

Published

Failed

Retrying
```

pertenecientes a Outbox no representan evolución del Aggregate.

---

# Version de Integration Event

Un contrato de Integration Event puede poseer su propio versionado.

Debe mantenerse:

```text
Integration Contract Version

≠

Audit.Version
```

---

# AggregateVersion e Integration Contract Version

Conceptualmente pueden coexistir:

```text
Audit.Version = 1

Integration Contract Version = 2
```

sin contradicción.

El primer valor representa evolución del Aggregate.

El segundo representa evolución del contrato público.

---

# Domain Event Version y Integration Event Version

Una eventual transformación:

```text
AuditRecorded
    │
    ▼
Integration Event
```

no transfiere automáticamente:

```text
AggregateVersion
```

como versión del contrato.

Ambos conceptos deben permanecer separados.

---

# Read Model

Un Read Model puede proyectar:

```text
Version
```

del Aggregate para facilitar trazabilidad y detección de lag.

Sin embargo:

```text
ReadModel.Version

≠

Aggregate Version Authority
```

---

# Read Model Desactualizado

Puede existir:

```text
Audit.Version = N

ReadModel.Version = N - 1
```

durante una ventana de consistencia eventual.

Esto no modifica la Version real del Aggregate.

---

# Read Model no Incrementa Version

Actualizar una proyección no incrementa:

```text
Audit.Version
```

Debe mantenerse:

```text
Projection Update

≠

Aggregate Modification
```

---

# Rebuild de Read Model

Reconstruir un Read Model desde eventos históricos:

- no ejecuta Commands;
- no modifica Audit;
- no incrementa Audit.Version;
- no produce nuevos Domain Events.

---

# CQRS

En CQRS:

```text
Write Model

owns

Audit.Version
```

mientras:

```text
Read Model

projects

Audit.Version
```

cuando dicha información forme parte de la proyección.

---

# Event Sourcing

Audit es compatible con Event Sourcing.

En esta estrategia, AggregateVersion puede representar el orden de
los hechos dentro del stream de una identidad Audit.

Para la versión 1.0:

```text
Stream AUD-001

    AuditRecorded
    AggregateVersion = 1
```

reconstruye:

```text
Audit.Version = 1
```

---

# Event Stream por AuditId

Cuando se utilice Event Sourcing:

```text
AuditId
```

identifica conceptualmente el stream del Aggregate.

Los eventos de diferentes AuditId no comparten una única Version.

---

# Replay de Event Stream

Aplicar:

```text
AuditRecorded
AggregateVersion = 1
```

durante replay debe reconstruir:

```text
Audit.Version = 1
```

sin producir:

```text
Version = 2
```

como consecuencia del replay.

---

# Snapshot

Si una implementación utiliza snapshots, estos no cambian el
significado de Version.

Debe mantenerse:

```text
Snapshot

≠

New Aggregate Modification
```

La estrategia técnica pertenece a Infrastructure.

---

# Cache

Una representación cacheada puede contener Version.

Sin embargo:

```text
Cached Version

≠

Domain Authority
```

La autoridad permanece en el Write Model conforme al Repository
Contract.

---

# Replica

Una réplica técnica puede encontrarse temporalmente en una Version
anterior.

Esto no modifica la Version confirmada del Aggregate.

La replicación pertenece a Infrastructure.

---

# Version de Base de Datos

Una base de datos puede utilizar números de revisión internos.

Debe mantenerse:

```text
Database Revision

≠

Audit.Version
```

salvo que la implementación los utilice expresamente para
representar el mismo concepto sin alterar su semántica.

---

# Version de Esquema

Debe mantenerse:

```text
Database Schema Version

≠

Audit.Version
```

Una migración de esquema no incrementa Version del Aggregate.

---

# Version de Aplicación

Debe mantenerse:

```text
Application Version

≠

Audit.Version
```

Desplegar una nueva versión de AURA no modifica automáticamente los
Aggregates persistidos.

---

# Version de API

Debe mantenerse:

```text
API Version

≠

Audit.Version
```

El versionado de una API pertenece a contratos externos.

---

# Domain Contract Version

Debe mantenerse:

```text
Domain Contract Version

≠

Audit.Version
```

El documento:

```text
Versión: 1.0
```

tampoco representa:

```text
Audit.Version
```

de una instancia concreta.

---

# Versión del Documento y Version del Aggregate

Debe mantenerse:

```text
DOMAIN-012I Version 1.0

≠

Audit.Version
```

La primera representa versión documental del contrato.

La segunda representa evolución lógica de una instancia Audit.

---

# AuditRecorded y Contract Version

El evento:

```text
AuditRecorded
```

puede evolucionar contractualmente en el futuro.

La versión del contrato del evento no debe confundirse con:

```text
AuditRecorded.AggregateVersion
```

---

# Version y Retención

Una política futura de retención no debe reinterpretar Version.

Debe mantenerse:

```text
Retention Policy

≠

Aggregate Version
```

---

# Version y Eliminación

Una eventual eliminación física permitida por política externa no
representa automáticamente:

```text
Version = N + 1
```

como transición de dominio.

La versión 1.0 no define:

```text
DeleteAudit
```

ni:

```text
AuditDeleted
```

---

# Version y Archived

La versión 1.0 no define:

```text
Archived
```

como estado.

Por lo tanto, no existe un incremento oficial de Version asociado a:

```text
Recorded → Archived
```

---

# Version y CorrectAudit

La versión 1.0 no define:

```text
CorrectAudit
```

Por lo tanto, no existe una modificación oficial de Version
asociada a dicho Command.

---

# Version y RetryAudit

La versión 1.0 no define:

```text
RetryAudit
```

Por lo tanto:

```text
Technical Retry

≠

Audit Version Increment
```

---

# Version y Source Correction

Si el Source Aggregate produce un hecho correctivo posterior:

```text
Source Fact B
```

este hecho no incrementa automáticamente:

```text
Audit A.Version
```

de una unidad Audit previa.

Puede originar otra unidad Audit cuando corresponda.

---

# Independencia Temporal

Version no se calcula desde el tiempo.

Debe mantenerse:

```text
Later Timestamp

≠

Automatically Higher Aggregate Version
```

La Version evoluciona por modificaciones válidas del Aggregate.

---

# Independencia de CorrelationId

CorrelationId no determina Version.

Debe mantenerse:

```text
CorrelationId

≠

Aggregate Version
```

---

# Independencia de CausationId

CausationId no determina Version.

Debe mantenerse:

```text
CausationId

≠

Aggregate Version
```

---

# Independencia de ActorId

ActorId no determina Version.

Debe mantenerse:

```text
ActorId

≠

Aggregate Version
```

---

# Independencia de SourceEventId

SourceEventId no determina:

```text
Audit.Version
```

Debe mantenerse:

```text
SourceEventId

≠

Aggregate Version
```

---

# Independencia de EventId

AuditRecorded.EventId tampoco determina Version.

El orden conceptual pertenece a AggregateVersion.

---

# Consistency Boundary

Version protege únicamente la evolución de:

```text
Audit
```

No protege directamente la concurrencia de:

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

Cada Aggregate mantiene su propio mecanismo de Versioning.

---

# No Version Compartida

No debe existir una regla obligatoria:

```text
Audit.Version

=

SourceAggregate.Version
```

ni:

```text
Audit.Version

=

Notification.Version
```

ni equivalentes.

---

# No Bloqueo Multi-Aggregate

Optimistic Concurrency sobre Audit no requiere bloquear el Source
Aggregate.

Debe mantenerse:

```text
Audit Concurrency Control

≠

Cross-Aggregate Lock
```

---

# Consistencia Eventual

Puede existir:

```text
SourceAggregateVersion = N

Source Fact committed
```

mientras:

```text
Audit does not yet exist
```

y posteriormente:

```text
Audit.Version = 1
```

al registrarse la unidad Audit.

Esto es consistente con límites independientes.

---

# Version y Audit Failure

Si Audit no logra crearse:

```text
SourceAggregateVersion
```

no cambia como consecuencia de dicho fallo.

Debe mantenerse:

```text
Audit Failure

≠

Source Version Rollback
```

---

# Version y Source Aggregate Rollback

Audit no posee autoridad para reducir, modificar o restaurar la
Version del Source Aggregate.

Debe mantenerse:

```text
Audit

≠

Source Version Authority
```

---

# Version y Domain Event Ordering

Dentro de una identidad Audit, los Domain Events futuros deberán
mantener un orden compatible con:

```text
1, 2, 3, ..., N
```

conforme a modificaciones válidas.

No se permiten saltos arbitrarios producidos por decisiones de
Infrastructure.

---

# No Incremento por Publicación

Producir un Domain Event como consecuencia de una modificación
válida y posteriormente publicarlo son momentos conceptualmente
distintos.

El incremento ocurre por la modificación del Aggregate.

La publicación no incrementa nuevamente Version.

---

# No Incremento por Consumo

Que otro componente consuma:

```text
AuditRecorded
```

no modifica:

```text
Audit.Version
```

---

# No Incremento por Proyección

Que un Read Model procese:

```text
AuditRecorded
```

no incrementa:

```text
Audit.Version
```

---

# No Incremento por Audit Externo

Que otro contexto genere su propia trazabilidad sobre un hecho de
Audit no modifica automáticamente:

```text
Audit.Version
```

---

# Flujo Oficial de Version

Para versión 1.0:

```text
Confirmed Source Fact
        │
        ▼
   RecordAudit
        │
        ▼
  Validate Audit
        │
        ▼
No Audit → Recorded
        │
        ▼
   Version = 1
        │
        ▼
  AuditRecorded
AggregateVersion = 1
        │
        ▼
Repository.save()
        │
        ▼
      Commit
```

---

# Flujo de Rechazo

```text
RecordAudit
    │
    ▼
Validation
    │
    ▼
  Invalid
    │
    ▼
 Rejected
```

Resultado:

```text
No Audit

No persisted Version

No AuditRecorded
```

---

# Flujo de Lectura

```text
Audit.Version = 1
    │
    ▼
findById()
    │
    ▼
Audit.Version = 1
```

---

# Flujo de Rehidratación

```text
Persisted Audit
Version = 1
    │
    ▼
Rehydration
    │
    ▼
Audit
Version = 1
```

---

# Flujo Event Sourced

```text
AuditRecorded
AggregateVersion = 1
    │
    ▼
apply()
    │
    ▼
Audit
State = Recorded
Version = 1
```

---

# Flujo de Publicación

```text
Audit
Version = 1
    │
    ▼
Commit
    │
    ▼
Integration Publication
    │
    ▼
Audit
Version = 1
```

---

# Flujo de Retry Técnico

```text
Technical Processing
    │
    ▼
   Failure
    │
    ▼
Technical Retry
```

no implica:

```text
Audit.Version + 1
```

---

# Reglas Fundamentales

Versioning de Audit debe cumplir:

1. Audit posee Version propia.
2. Version representa evolución lógica del Aggregate.
3. Version pertenece exclusivamente a Audit.
4. No Audit no requiere una Version 0 persistida.
5. La creación válida establece Version = 1.
6. RecordAudit produce Version = 1.
7. Toda modificación válida futura incrementa Version exactamente
   una vez.
8. Una misma modificación no incrementa Version múltiples veces.
9. Una operación rechazada no incrementa Version.
10. Una creación rechazada no produce Version persistida.
11. Una lectura no incrementa Version.
12. exists() no incrementa Version.
13. nextIdentity() no establece Version.
14. Rehidratación no incrementa Version.
15. Replay no incrementa Version como nueva modificación.
16. DomainEvent.AggregateVersion coincide con Audit.Version
    resultante.
17. AuditRecorded posee AggregateVersion = 1 en la creación.
18. EventId no equivale a AggregateVersion.
19. SourceAggregateVersion permanece independiente de Audit.Version.
20. Coincidencia numérica de Versions no implica identidad
    semántica.
21. Cambios posteriores del Source Aggregate no modifican
    Audit.Version.
22. Cada AuditId mantiene Version independiente.
23. No existe GlobalAuditVersion en el dominio.
24. No existe orden global obligatorio entre Audit Aggregates.
25. Optimistic Concurrency protege escrituras.
26. ExpectedVersion debe coincidir con PersistedVersion.
27. Una Version obsoleta produce ConcurrencyConflict.
28. ConcurrencyConflict no incrementa Version.
29. ConcurrencyConflict no es AuditStatus.
30. Repository no decide Version.
31. Repository persiste la Version producida por el Aggregate.
32. Persistir no incrementa Version nuevamente.
33. Recuperar preserva Version.
34. Version no es timestamp.
35. Version no equivale a CreatedAt.
36. Version no equivale a UpdatedAt.
37. State, Version y Domain Event deben permanecer coherentes.
38. La creación confirma coherentemente State = Recorded y Version
    = 1.
39. PersistenceFailure no representa incremento válido.
40. RepositoryUnavailable no incrementa Version.
41. DuplicateAuditId no incrementa Version del Aggregate existente.
42. Retry técnico no incrementa Version.
43. Duplicate Technical Delivery no incrementa Version.
44. Publicar Integration Events no incrementa Version.
45. Retries de publicación no incrementan Version.
46. Outbox no modifica Version.
47. Integration Contract Version no equivale a Audit.Version.
48. ReadModel.Version no posee autoridad sobre Audit.Version.
49. Proyecciones no incrementan Version.
50. Rebuild de Read Models no incrementa Version.
51. CQRS mantiene Version en el Write Model.
52. Event Sourcing preserva Version conforme al stream.
53. Snapshot no constituye modificación del Aggregate.
54. Cache no es autoridad sobre Version.
55. Réplicas técnicas no determinan Version.
56. Database Revision no equivale automáticamente a Audit.Version.
57. Database Schema Version no equivale a Audit.Version.
58. Application Version no equivale a Audit.Version.
59. API Version no equivale a Audit.Version.
60. Domain Contract Version no equivale a Audit.Version.
61. La versión documental 1.0 no equivale a Audit.Version.
62. Contract Version de AuditRecorded no equivale a
    AggregateVersion.
63. No existe incremento oficial por archivado.
64. No existe incremento oficial por DeleteAudit.
65. No existe incremento oficial por CorrectAudit.
66. No existe incremento oficial por RetryAudit.
67. Nuevos Source Facts no incrementan Audit previos.
68. Timestamps posteriores no determinan automáticamente Version.
69. ActorId no determina Version.
70. CorrelationId no determina Version.
71. CausationId no determina Version.
72. SourceEventId no determina Version.
73. Version protege únicamente el Consistency Boundary de Audit.
74. Versions de distintos Aggregates permanecen independientes.
75. Audit Concurrency Control no requiere cross-Aggregate locking.
76. La consistencia eventual no altera Versioning interno.
77. Audit no posee autoridad sobre SourceAggregateVersion.
78. Publicar, consumir o proyectar un evento no modifica Version.
79. Cualquier evolución futura debe preservar estas reglas salvo
    modificación explícita del contrato de dominio.

---

# Restricciones

No está permitido:

- establecer Version arbitrariamente;
- utilizar setters públicos para Version;
- iniciar una unidad Audit válida con una Version distinta de la
  definida por el dominio;
- utilizar Version 0 persistida como requisito no definido;
- incrementar Version ante una operación rechazada;
- incrementar Version al leer;
- incrementar Version al rehidratar;
- incrementar Version durante replay;
- incrementar Version al publicar Integration Events;
- incrementar Version por retry técnico;
- incrementar Version por Duplicate Delivery;
- permitir que Repository decida Version;
- confundir Audit.Version con SourceAggregateVersion;
- confundir AggregateVersion con Contract Version;
- confundir Version con timestamps;
- utilizar Version de otro Aggregate como ExpectedVersion de Audit;
- utilizar una Permission para modificar Version directamente;
- sobrescribir estado confirmado usando una Version obsoleta;
- utilizar Infrastructure para generar saltos arbitrarios de
  Version;
- imponer orden global entre identidades Audit distintas;
- utilizar ReadModel.Version como autoridad de escritura;
- modificar SourceAggregateVersion desde Audit.

---

# Compatibilidad Arquitectónica

El modelo de Versioning de Audit es compatible con:

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
- Persistence Ignorance;
- High Cohesion;
- Low Coupling.

Estas compatibilidades no introducen tecnologías concretas ni
modifican las reglas conceptuales de Version.

---

# Definición de Éxito

El Versioning del Aggregate **Audit** proporciona una evolución
lógica independiente, coherente y protegida para cada unidad Audit.

La versión 1.0 establece:

```text
No Audit
    │
    ▼
RecordAudit
    │
    ▼
Recorded
    │
    ▼
Audit.Version = 1
    │
    ▼
AuditRecorded.AggregateVersion = 1
```

y garantiza que:

- Audit mantiene Version propia;
- la creación válida establece Version = 1;
- No Audit no exige una Version 0 persistida;
- toda modificación válida futura incrementará Version una sola vez;
- operaciones rechazadas no incrementan Version;
- lecturas no incrementan Version;
- rehidratación y replay no incrementan Version como nuevos hechos;
- AuditRecorded representa la Version resultante del Aggregate;
- SourceAggregateVersion permanece semánticamente independiente;
- cambios del Source Aggregate no cambian Audit.Version;
- cada AuditId mantiene evolución independiente;
- no existe Version global obligatoria;
- Optimistic Concurrency protege las escrituras;
- escrituras obsoletas producen ConcurrencyConflict;
- Repository verifica y persiste Version pero no la decide;
- Version permanece distinta de CreatedAt y UpdatedAt;
- fallos de persistencia no producen incrementos confirmados;
- Technical Retry y Duplicate Delivery no cambian Version;
- publicación y retry de Integration Events no cambian Version;
- Outbox permanece fuera de la evolución del Aggregate;
- Integration Contract Version permanece distinta de Audit.Version;
- Read Models pueden proyectar Version pero no controlarla;
- CQRS mantiene Version en el Write Model;
- Event Sourcing puede reconstruir Version sin producir nuevas
  modificaciones;
- snapshots, caches, réplicas y revisiones técnicas no determinan
  Version;
- API Version, Application Version, Schema Version y Domain Contract
  Version permanecen conceptos distintos;
- Versions de otros Aggregates no se comparten con Audit;
- ninguna optimización técnica puede evitar las reglas de
  concurrencia o Versioning;
- cualquier evolución futura deberá mantener coherencia entre
  estado, Version, Domain Events e Invariants.

De esta forma, `DOMAIN-012I-Versioning.md` establece las reglas
oficiales de Versioning del Aggregate **Audit** conforme al patrón
consolidado de AURA Core.