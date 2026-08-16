# DOMAIN-012J — Audit Consistency Boundary

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
- DOMAIN-012K-Integration-Events.md
- DOMAIN-012L-Read-Model.md
- DOMAIN-012M-Test-Scenarios.md
- DOMAIN-012O-Security-Model.md

---

# Objetivo

Este documento define formalmente el **Consistency Boundary** del
Aggregate **Audit**.

El Consistency Boundary determina qué información y reglas deben
permanecer internamente consistentes dentro de una única unidad
Audit y qué conceptos permanecen fuera de su límite transaccional.

El Aggregate:

```text
Audit
```

constituye una unidad independiente de consistencia.

---

# Principio Fundamental

Debe mantenerse:

```text
Audit Transaction

≠

Source Aggregate Transaction
```

Audit protege exclusivamente su propio estado.

La existencia de una relación causal, temporal o de trazabilidad con
otro Aggregate no fusiona sus Consistency Boundaries.

---

# Aggregate Root

La única Aggregate Root del Consistency Boundary es:

```text
Audit
```

Toda modificación perteneciente al Aggregate debe realizarse
exclusivamente mediante dicha Aggregate Root.

Ninguna estructura interna puede ser modificada directamente desde
fuera del límite.

---

# Unidad de Consistencia

Una unidad Audit representa:

```text
One AuditId

=

One Consistency Boundary
```

Cada AuditId mantiene:

- identidad propia;
- estado propio;
- Version propia;
- CreatedAt propio;
- UpdatedAt cuando corresponda;
- referencias propias al hecho auditado;
- información de trazabilidad propia;
- Domain Events propios;
- Invariants propias.

---

# Elementos Dentro del Boundary

El Consistency Boundary de Audit incluye conceptualmente:

```text
Audit

AuditId

AuditStatus

Source References

Traceability Information

Version

CreatedAt

UpdatedAt

Value Objects propios

Internal Entities propias
```

únicamente cuando cada concepto haya sido definido oficialmente por
el dominio.

---

# Elementos Fuera del Boundary

Permanecen fuera:

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

También permanecen fuera:

- Authentication;
- Authorization;
- Read Models;
- Integration Events;
- Infrastructure;
- brokers;
- APIs;
- FIWARE;
- sistemas municipales;
- logs;
- metrics;
- traces;
- Observability.

---

# Identidad

AuditId define la identidad del Aggregate dentro de su límite.

Debe mantenerse:

```text
AuditId

≠

SourceAggregateId
```

y:

```text
AuditId

≠

SourceEventId
```

y:

```text
AuditId

≠

DomainEvent.EventId
```

Las identidades externas no amplían el Boundary.

---

# Estado

La versión 1.0 define exclusivamente:

```text
Recorded
```

como estado persistido del Aggregate.

El Boundary debe garantizar atómicamente que una unidad válida no
pueda quedar confirmada con:

```text
AuditId valid

+

State invalid
```

ni:

```text
State = Recorded

+

Version invalid
```

ni cualquier combinación que viole las Invariants.

---

# Lifecycle

La única evolución oficial es:

```text
No Audit → Recorded
```

Esta transición pertenece exclusivamente al Consistency Boundary de
Audit.

No implica una transición simultánea en ningún Aggregate externo.

---

# State Machine

La State Machine solamente gobierna:

```text
Audit
```

No gobierna:

```text
Source Aggregate State
```

Debe mantenerse:

```text
Source Status

≠

Audit Status
```

---

# Command Boundary

El único Command oficial:

```text
RecordAudit
```

modifica exclusivamente el Aggregate Audit.

No puede utilizarse para modificar:

- Source Aggregate;
- Source Domain Event;
- Read Models;
- Integration;
- otros Aggregates.

---

# Comportamiento Atómico

Una ejecución válida de:

```text
RecordAudit
```

debe mantener coherentemente dentro del mismo Boundary:

```text
AuditId

State = Recorded

Version = 1

CreatedAt

Traceability Information

AuditRecorded
```

conforme a las reglas aplicables.

---

# Invariants

Todas las Invariants internas de Audit deben cumplirse dentro del
mismo Consistency Boundary.

Debe mantenerse:

```text
Valid Before

+

Valid Operation

=

Valid After
```

Ninguna modificación puede confirmarse dejando el Aggregate en un
estado parcialmente válido.

---

# Versioning

Version pertenece exclusivamente a Audit.

Debe mantenerse:

```text
Audit.Version

≠

SourceAggregateVersion
```

El control de concurrencia de Audit solamente protege la evolución
de dicha identidad Audit.

---

# Atomicidad de State y Version

Cuando una modificación válida cambia el estado interno del
Aggregate, State y Version deben quedar confirmados coherentemente.

Para la creación:

```text
State = Recorded

Version = 1
```

pertenecen al mismo resultado válido.

---

# Atomicidad de Domain Event

`AuditRecorded` representa el hecho correspondiente a una creación
válida del Aggregate.

Debe mantenerse coherencia entre:

```text
Audit State

Audit.Version

AuditRecorded.AggregateVersion
```

Para la versión 1.0:

```text
Audit.Version = 1

AuditRecorded.AggregateVersion = 1
```

---

# Source Aggregate

El Source Aggregate permanece fuera del Consistency Boundary.

Audit puede conservar:

```text
SourceAggregateId

SourceAggregateType

SourceAggregateVersion
```

cuando corresponda.

Estas referencias no convierten al Source Aggregate en parte de
Audit.

---

# Source Domain Event

Un Source Domain Event también permanece fuera del Boundary.

Audit puede conservar información como:

```text
SourceEventId

SourceEventType

SourceOccurredAt
```

cuando el contrato lo permita.

Debe mantenerse:

```text
Source Domain Event

≠

Audit Internal Entity
```

---

# No Ownership Externo

Audit no adquiere ownership sobre:

- Source Aggregate;
- Source Domain Event;
- Actor externo;
- Organization;
- Citizen;
- Document;
- Notification;
- Integration.

Debe mantenerse:

```text
External Reference

≠

Aggregate Ownership
```

---

# Referencias Externas

Las relaciones externas deben representarse mediante:

- identificadores;
- hechos;
- contratos;
- referencias conceptuales.

No mediante composición de Aggregates completos.

Debe mantenerse:

```text
Reference

≠

Embedded Aggregate
```

---

# Source Aggregate Commit

El hecho originador debe estar confirmado antes de que Audit pueda
registrarlo.

Conceptualmente:

```text
Source Aggregate
    │
    ▼
Source Commit
    │
    ▼
Confirmed Source Fact
```

posteriormente:

```text
Audit Processing
```

puede ocurrir de forma independiente.

---

# Audit Commit

La confirmación de Audit ocurre dentro de su propia transacción.

Conceptualmente:

```text
RecordAudit
    │
    ▼
Audit
    │
    ▼
AuditRepository.save()
    │
    ▼
Audit Commit
```

---

# Separación de Commits

Debe mantenerse:

```text
Source Commit

≠

Audit Commit
```

La confirmación de uno no constituye automáticamente la confirmación
del otro.

---

# Consistencia Eventual

La relación entre Source Aggregate y Audit puede utilizar:

```text
Eventual Consistency
```

Puede existir legítimamente:

```text
Source Fact Confirmed

+

Audit Not Yet Recorded
```

durante una ventana temporal.

---

# Ventana Temporal Válida

Conceptualmente:

```text
T1

Source Fact committed
```

luego:

```text
T2

No Audit yet
```

posteriormente:

```text
T3

Audit Recorded
```

Esta secuencia no viola la consistencia interna de ninguno de los
Aggregates.

---

# No Transacción Distribuida Obligatoria

La versión 1.0 no requiere:

```text
Distributed Transaction
```

entre Audit y el Source Aggregate.

Debe mantenerse:

```text
Audit Consistency

≠

Distributed Atomicity Requirement
```

---

# No Two-Phase Commit de Dominio

El dominio no exige:

```text
Source Aggregate
    +
Audit
    │
    ▼
Two-Phase Commit
```

como condición para la validez del hecho auditado.

La coordinación técnica futura no debe confundirse con el
Consistency Boundary del dominio.

---

# Fallo de Audit

Si Audit falla después de que el Source Fact ya fue confirmado:

```text
Audit Failure
```

no produce:

```text
Source Aggregate Rollback
```

Debe mantenerse:

```text
Audit Failure

≠

Source Fact Invalid
```

---

# Fallo del Source Aggregate

Si el Source Aggregate no confirma el hecho:

```text
No Confirmed Source Fact
```

entonces Audit no debe registrar ese hecho como consumado.

Debe mantenerse:

```text
No Source Commit

↓

No Valid Audit for that Fact
```

---

# PersistenceFailure

Un:

```text
PersistenceFailure
```

durante Audit no crea:

```text
AuditStatus = Failed
```

ni expande la transacción hacia el Source Aggregate.

---

# RepositoryUnavailable

Un:

```text
RepositoryUnavailable
```

no modifica el Consistency Boundary.

El Aggregate continúa sujeto a las mismas reglas conceptuales.

---

# ConcurrencyConflict

Un:

```text
ConcurrencyConflict
```

solamente afecta la escritura de la unidad Audit correspondiente.

No implica conflicto de concurrencia en el Source Aggregate.

Debe mantenerse:

```text
Audit Concurrency Conflict

≠

Source Aggregate Concurrency Conflict
```

---

# Optimistic Concurrency

Optimistic Concurrency protege:

```text
AuditId

+

Audit.Version
```

dentro del propio Aggregate.

No utiliza:

```text
SourceAggregateVersion
```

como Version de concurrencia de Audit.

---

# SourceAggregateVersion

SourceAggregateVersion puede conservarse para trazabilidad.

No debe utilizarse como:

```text
Audit ExpectedVersion
```

ni como:

```text
Audit PersistedVersion
```

---

# Múltiples Audit Aggregates

Diferentes unidades Audit poseen Consistency Boundaries
independientes.

Debe mantenerse:

```text
Audit A

≠

Audit B
```

como unidades transaccionales distintas.

---

# No Aggregate Global

Las necesidades de consulta histórica global no justifican crear una
única unidad de consistencia que contenga todos los Audit.

Debe mantenerse:

```text
Global Audit History Query

≠

Global Audit Aggregate
```

Las consultas globales pertenecen al Read Side.

---

# Múltiples Hechos del Mismo Source Aggregate

Un mismo Source Aggregate puede producir:

```text
Source Fact A

Source Fact B

Source Fact C
```

y Audit puede representar:

```text
Audit A

Audit B

Audit C
```

Cada unidad mantiene:

- AuditId independiente;
- Version independiente;
- Consistency Boundary independiente.

---

# Corrección del Source Aggregate

Si posteriormente el Source Aggregate produce un hecho correctivo:

```text
Source Fact B
```

este hecho no entra en el Consistency Boundary de:

```text
Audit A
```

ya existente.

Debe mantenerse:

```text
New Source Fact

≠

Rewrite Existing Audit
```

---

# ActorId

Cuando Audit conserve:

```text
ActorId
```

Actor permanece fuera del Boundary.

AuditId y ActorId no definen una composición interna.

---

# Citizen

Si ActorId referencia a Citizen:

```text
Citizen
```

continúa siendo un Aggregate externo.

Audit no carga ni modifica Citizen como parte de su transacción.

---

# Membership

Membership permanece fuera del Consistency Boundary.

Audit no modifica:

```text
MembershipStatus

Membership.Version

Membership Lifecycle
```

dentro de RecordAudit.

---

# Role

Role permanece fuera del Boundary.

Registrar información de trazabilidad relacionada con un Role no
permite:

- asignar Role;
- revocar Role;
- modificar Role;
- modificar Permissions.

---

# Territory

Territory permanece fuera del Boundary.

Una referencia territorial no convierte Territory en una Internal
Entity de Audit.

---

# Organization

Organization permanece fuera del Boundary.

Audit no requiere cargar Organization para proteger sus propias
Invariants salvo que un contrato futuro explícito establezca una
regla distinta.

La versión 1.0 no introduce dicha dependencia.

---

# Assembly

Conceptualmente:

```text
Assembly
    │
    ▼
Assembly Domain Event
    │
    ▼
Eventual Propagation
    │
    ▼
Audit
```

Assembly y Audit mantienen transacciones separadas.

---

# Proposal

Proposal permanece fuera del Boundary.

Audit no modifica:

```text
ProposalStatus

Proposal.Version

Proposal Lifecycle
```

---

# Participation

Participation permanece fuera del Boundary.

Debe mantenerse:

```text
Participation Transaction

≠

Audit Transaction
```

---

# Voting

Voting permanece fuera del Boundary.

Audit no:

- registra votos;
- modifica votos;
- abre Voting;
- cierra Voting;
- cambia resultados;
- cambia VotingStatus.

---

# Document

Document permanece fuera del Boundary.

Una referencia documental no convierte Document en parte del
Aggregate Audit.

Audit no modifica:

```text
DocumentStatus

Document.Version

Document Content

Document Lifecycle
```

---

# Notification

Notification permanece fuera del Boundary.

Conceptualmente:

```text
Notification Domain Event
    │
    ▼
Audit Coordination
    │
    ▼
RecordAudit
```

pero:

```text
Notification Transaction

≠

Audit Transaction
```

---

# Integration

Integration permanece fuera del Consistency Boundary.

Audit puede producir Domain Events.

La eventual transformación hacia Integration Events ocurre fuera del
Aggregate.

---

# Domain Events

El Domain Event oficial:

```text
AuditRecorded
```

pertenece al Consistency Boundary lógico de Audit como hecho
producido por una modificación válida.

Debe representar la Version resultante del Aggregate.

---

# Source Domain Event versus AuditRecorded

Debe mantenerse:

```text
Source Domain Event

≠

AuditRecorded
```

El Source Domain Event pertenece al Source Aggregate.

AuditRecorded pertenece a Audit.

No comparten ownership.

---

# Domain Event y Commit

Un Domain Event producido por comportamiento válido debe permanecer
coherente con el resultado que será confirmado.

La publicación externa del hecho debe ocurrir después del commit
correspondiente.

Debe mantenerse:

```text
Audit Commit

before

External Publication
```

---

# Integration Events

Los Integration Events permanecen fuera del Boundary.

Debe mantenerse:

```text
AuditRecorded

≠

Integration Event
```

y:

```text
Integration Event

≠

Audit State
```

---

# Publicación Externa

Publicar un Integration Event no modifica:

```text
AuditStatus

Audit.Version

AuditId
```

porque la publicación ocurre fuera del Write Model.

---

# Fallo de Publicación

Si Audit ya fue confirmado:

```text
AuditStatus = Recorded

Version = 1
```

y posteriormente falla una publicación externa:

```text
IntegrationFailure
```

Audit permanece:

```text
Recorded

Version = 1
```

---

# Retry de Publicación

Un retry técnico de publicación tampoco modifica el Consistency
Boundary.

Debe mantenerse:

```text
Integration Retry

≠

Audit Modification
```

---

# Transactional Outbox

Cuando la arquitectura utilice Transactional Outbox, su utilización
no amplía el Aggregate Audit.

Conceptualmente:

```text
Audit Transaction
    │
    ├── Audit State
    └── Publication Coordination
```

puede coordinarse desde las capas correspondientes sin que:

```text
Outbox
```

se convierta en Internal Entity del Aggregate por definición de este
documento.

---

# Outbox State

Estados técnicos como:

```text
Pending

Published

Failed

Retrying
```

pertenecientes a Outbox permanecen fuera de AuditStatus.

---

# Read Models

Los Read Models permanecen fuera del Consistency Boundary.

Debe mantenerse:

```text
Audit Write Model

≠

Audit Read Model
```

---

# Proyección

Conceptualmente:

```text
AuditRecorded
    │
    ▼
Projection
    │
    ▼
Audit Read Model
```

La proyección ocurre después del hecho confirmado.

No forma parte de la transacción interna obligatoria del Aggregate.

---

# Projection Lag

Puede existir:

```text
Audit committed

+

Read Model not yet updated
```

durante una ventana temporal válida.

Debe mantenerse:

```text
Projection Lag

≠

Audit Inconsistency
```

---

# ReadModel.Version

Cuando un Read Model proyecte Version:

```text
ReadModel.Version
```

representa la última Version procesada por dicha proyección.

No gobierna:

```text
Audit.Version
```

---

# CQRS

El Consistency Boundary permanece en el Write Model.

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

   Projection
        │
        ▼
   Read Models
```

---

# Read Queries

Consultas por:

- AuditId;
- SourceAggregateId;
- SourceEventId;
- ActorId;
- CorrelationId;
- CausationId;
- período temporal;
- tipo de hecho;

no amplían el Consistency Boundary del Aggregate.

Pertenecen al Read Side.

---

# Repository

AuditRepository persiste:

```text
One Audit Aggregate
```

como una unidad.

Debe mantenerse:

```text
AuditRepository

≠

Multi-Aggregate Repository
```

---

# Repository Transaction

El Repository confirma la persistencia de Audit sin requerir
persistir simultáneamente:

```text
Source Aggregate
```

dentro del mismo Repository Contract.

---

# No Persistencia Parcial

El Repository no debe confirmar solamente una parte del estado
requerido para que Audit sea válido.

Debe mantenerse:

```text
Aggregate Persistence

=

Consistent Unit Persistence
```

---

# Repository no Amplía el Boundary

La implementación del Repository no puede decidir que:

```text
Source Aggregate
```

pase a formar parte de Audit por conveniencia técnica.

Persistencia y Aggregate Boundary son conceptos distintos.

---

# Authentication

Authentication permanece fuera del Consistency Boundary.

El Aggregate no almacena:

- passwords;
- tokens;
- sesiones;
- claves privadas;
- credenciales.

---

# Authorization

Authorization también permanece fuera del Boundary.

Conceptualmente:

```text
Authorization
    │
    ▼
RecordAudit
    │
    ▼
Audit
```

La decisión de autorización ocurre antes del comportamiento del
Aggregate.

---

# Authorized no Amplía el Boundary

Debe mantenerse:

```text
Authorized

≠

Expanded Consistency Boundary
```

Una Permission no permite modificar otro Aggregate dentro de la
misma operación Audit.

---

# Permission no es Internal State

Las políticas de Authorization no forman parte del estado de Audit
por definición de este documento.

La Aggregate Root recibe una intención ya autorizada y continúa
validando sus propias reglas.

---

# Actor de Seguridad versus Actor Auditado

El actor o proceso que solicita RecordAudit puede ser distinto del:

```text
ActorId
```

preservado como información del Source Fact.

Ninguno de ellos amplía automáticamente el Consistency Boundary.

---

# Security Claims

Claims técnicos no forman parte del estado interno de Audit por
defecto.

Debe mantenerse:

```text
Security Claim

≠

Audit State
```

---

# Logs

Logs permanecen fuera del Consistency Boundary.

Debe mantenerse:

```text
Audit

≠

Application Log
```

y:

```text
Audit

≠

Infrastructure Log
```

---

# Observability

Metrics, traces y monitoring permanecen fuera del Aggregate.

Debe mantenerse:

```text
Observability

≠

Audit Consistency Boundary
```

---

# FIWARE

FIWARE permanece fuera del Consistency Boundary.

Audit no requiere:

```text
FIWARE

NGSI-LD

Context Broker

Orion
```

para preservar sus Invariants.

---

# Integración FIWARE

Una eventual integración puede ocurrir conceptualmente:

```text
AuditRecorded
    │
    ▼
Integration Boundary
    │
    ▼
FIWARE
```

sin incorporar FIWARE al Aggregate.

---

# Sistemas Municipales

Los sistemas municipales permanecen fuera del Boundary.

Sus:

- APIs;
- protocolos;
- permisos;
- modelos de datos;
- reglas técnicas;

no forman parte de Audit.

---

# External Consumer

Un consumidor externo puede reaccionar a información publicada desde
Audit.

No puede modificar directamente:

```text
AuditId

AuditStatus

Audit.Version
```

---

# Anti-Corruption Layer

Cuando la semántica externa difiera de AURA, la traducción ocurre en
la frontera correspondiente.

Debe mantenerse:

```text
External Model

≠

Audit Internal Model
```

salvo equivalencia explícitamente definida.

---

# Event Sourcing

Event Sourcing no modifica el Consistency Boundary.

Si se utiliza:

```text
AuditId
```

continúa identificando una única unidad Aggregate.

Su Event Stream contiene únicamente eventos pertenecientes a dicha
identidad Audit.

---

# Event Stream

Conceptualmente:

```text
Stream AUD-001

    AuditRecorded v1
```

pertenece solamente a:

```text
AUD-001
```

No incorpora eventos internos de Assembly, Notification, Document u
otros Aggregates como si fueran eventos propios.

---

# Source Event no es Audit Event Stream

Debe mantenerse:

```text
Source Aggregate Event Stream

≠

Audit Event Stream
```

Audit puede preservar referencias a Source Events sin convertirlos
en eventos propios.

---

# Rehidratación

La rehidratación reconstruye únicamente:

```text
Audit
```

No reconstruye automáticamente el Source Aggregate.

Debe mantenerse:

```text
Audit Rehydration

≠

Source Aggregate Rehydration
```

---

# Replay

Replay no amplía el Boundary.

Aplicar:

```text
AuditRecorded
```

reconstruye Audit.

No ejecuta el Source Domain Event ni modifica otros Aggregates.

---

# Snapshot

Un snapshot técnico, cuando exista, representa una optimización de
persistencia.

No amplía el Boundary ni introduce nuevos conceptos del dominio.

---

# Cache

Cache permanece fuera del Consistency Boundary.

Debe mantenerse:

```text
Cache

≠

Aggregate Boundary
```

Una representación cacheada no adquiere autoridad de escritura.

---

# Replica

Réplicas técnicas permanecen fuera del modelo de consistencia del
dominio.

La consistencia interna de Audit sigue definida por el Aggregate y
no por la topología física de almacenamiento.

---

# Performance

Ninguna optimización puede ampliar el Consistency Boundary para
incorporar otros Aggregates por conveniencia.

Debe mantenerse:

```text
Performance Optimization

≠

Aggregate Boundary Expansion
```

---

# Batch Processing

Procesar múltiples hechos en un mismo proceso técnico no convierte
múltiples Audits en una sola unidad Aggregate.

Debe mantenerse:

```text
Batch

=

Multiple Independent Audit Operations
```

cuando represente múltiples identidades Audit.

---

# Bulk Audit

Una operación coordinadora puede procesar múltiples hechos
auditables.

Sin embargo:

```text
Audit A

Audit B

Audit C
```

continúan manteniendo Consistency Boundaries independientes.

---

# Analytics

Analytics permanece fuera del Boundary.

Consultar todos los Audit para producir métricas, indicadores o
informes no convierte Analytics en parte del Aggregate.

---

# Trazabilidad Global

Una necesidad de reconstruir:

```text
Cross-Aggregate Timeline
```

puede resolverse mediante Read Models o proyecciones.

No requiere compartir una transacción global entre los Aggregates.

---

# CorrelationId

CorrelationId puede permitir trazabilidad entre múltiples hechos.

Debe mantenerse:

```text
Shared CorrelationId

≠

Shared Consistency Boundary
```

---

# CausationId

CausationId puede preservar relaciones causales.

Debe mantenerse:

```text
Causal Relationship

≠

Transactional Ownership
```

---

# SourceEventId

Dos estructuras pueden referenciar el mismo SourceEventId sin
compartir un Aggregate Boundary.

La referencia no crea atomicidad distribuida.

---

# Temporalidad

Una diferencia temporal entre:

```text
SourceOccurredAt

Audit.CreatedAt

AuditRecorded.OccurredAt
```

no constituye inconsistencia.

Cada timestamp representa un hecho diferente.

---

# Atomicidad Conceptual de Creación

El flujo de creación válido es:

```text
RecordAudit
    │
    ▼
Validate Permission
    │
    ▼
Validate State Machine
    │
    ▼
Validate Invariants
    │
    ▼
Establish Audit State
    │
    ▼
Increment Version
    │
    ▼
Produce AuditRecorded
    │
    ▼
Persist Audit
    │
    ▼
Commit
```

La decisión de Authorization pertenece a Application o al contexto
correspondiente y no constituye una Invariant interna del Aggregate.

---

# Resultado de una Operación Rechazada

Si la operación no puede confirmarse:

```text
Rejected
```

debe resultar en:

```text
No New Confirmed Audit State

No Version Increment

No UpdatedAt Change

No Success Domain Event
```

---

# Operación No Autorizada

Si Authorization rechaza la intención:

```text
RecordAudit
```

el comportamiento del Aggregate no debe producir una nueva unidad
Audit.

---

# Operación Inválida

Si Audit rechaza RecordAudit por Invariants:

```text
Source Fact
```

permanece fuera del Boundary y conserva su estado previo confirmado.

---

# No Compensación Automática

El Consistency Boundary de Audit no define una compensación
automática sobre otros Aggregates cuando una operación Audit falla.

Debe mantenerse:

```text
Audit Failure

≠

Automatic External Compensation
```

---

# No Cascading Rollback

No debe producirse:

```text
Audit Failure
    │
    ▼
Rollback Assembly
    │
    ▼
Rollback Notification
    │
    ▼
Rollback Document
```

por definición del Consistency Boundary.

---

# No Cascading Mutation

Una operación válida de Audit tampoco debe producir modificaciones
directas en otros Aggregates dentro de la misma Aggregate Root.

---

# No Cross-Aggregate Setter

No pueden existir comportamientos como:

```text
audit.setAssemblyStatus(...)

audit.setNotificationStatus(...)

audit.setDocumentStatus(...)
```

como parte del Aggregate Audit.

---

# No Embedded Source Aggregate

No debe modelarse:

```text
Audit
    └── SourceAggregate
            └── Complete External State
```

dentro del Consistency Boundary.

Audit conserva únicamente la representación necesaria conforme al
contrato de trazabilidad.

---

# No Embedded Domain Event Object como Ownership

Audit puede conservar datos provenientes de un Source Domain Event.

Sin embargo, no adquiere ownership sobre el objeto evento original.

Debe mantenerse:

```text
Event Reference

≠

Event Ownership Transfer
```

---

# Consistencia Histórica

El Boundary protege el significado histórico de la unidad Audit.

Una vez:

```text
Recorded
```

no debe reinterpretarse el registro para representar otro hecho.

---

# Nuevo Hecho

Un hecho posterior:

```text
Source Fact B
```

puede originar otra unidad Audit.

No modifica el Consistency Boundary de:

```text
Audit A
```

ya existente.

---

# Retención

Las reglas de retención no forman parte de este Consistency Boundary
en versión 1.0.

Este documento no introduce:

- expiración;
- archivado;
- eliminación automática;
- anonimización;
- redacción.

---

# delete()

La capacidad conceptual:

```text
Repository.delete()
```

no modifica el Lifecycle ni el Consistency Boundary definido por el
dominio.

No existe:

```text
Recorded → Deleted
```

como transición.

---

# Escenario de Éxito

```text
Source Aggregate
    │
    ▼
Source Fact committed
    │
    ▼
Eventual propagation
    │
    ▼
Authorization
    │
    ▼
RecordAudit
    │
    ▼
Audit
    │
    ├── AuditId
    ├── Recorded
    ├── Version = 1
    ├── CreatedAt
    └── AuditRecorded
            │
            ▼
     AuditRepository
            │
            ▼
          Commit
```

El Source Aggregate permanece fuera de la transacción Audit.

---

# Escenario de Fallo

```text
Source Fact committed
    │
    ▼
RecordAudit
    │
    ▼
PersistenceFailure
```

Resultado:

```text
Source Fact remains committed

No confirmed Audit commit
```

No existe rollback del Source Aggregate.

---

# Escenario con Read Model

```text
Audit Commit
    │
    ▼
AuditRecorded
    │
    ▼
Projection
    │
    ▼
Read Model
```

El Read Model puede actualizarse posteriormente.

---

# Escenario con Integration

```text
Audit Commit
    │
    ▼
AuditRecorded
    │
    ▼
Integration Boundary
    │
    ▼
Integration Event
    │
    ▼
External Consumer
```

El consumidor externo permanece fuera del Aggregate.

---

# Escenario con Fallo de Integration

```text
Audit committed

+

Integration publication failed
```

produce:

```text
Audit remains Recorded

Audit.Version unchanged
```

---

# Escenario con Múltiples Audits

```text
Source Fact A → Audit A

Source Fact B → Audit B

Source Fact C → Audit C
```

Cada Audit posee:

```text
Independent Transaction

Independent AuditId

Independent Version

Independent Consistency Boundary
```

---

# Reglas Fundamentales

El Consistency Boundary de Audit debe cumplir:

1. Audit es una unidad independiente de consistencia.
2. Audit es la única Aggregate Root.
3. Un AuditId representa un Consistency Boundary.
4. State, Version e Invariants pertenecen al Boundary.
5. La única transición oficial es No Audit → Recorded.
6. RecordAudit modifica exclusivamente Audit.
7. AuditRecorded pertenece al Aggregate Audit.
8. Source Domain Events permanecen fuera del Boundary.
9. Source Aggregates permanecen fuera del Boundary.
10. Referenciar un Aggregate no lo incorpora al Boundary.
11. Audit no adquiere ownership sobre Source Aggregate.
12. Audit no adquiere ownership sobre Source Domain Event.
13. AuditId permanece independiente de identidades externas.
14. Audit.Version permanece independiente de SourceAggregateVersion.
15. State y Version deben confirmarse coherentemente.
16. La modificación interna es atómica.
17. No se permite persistencia parcial que viole Invariants.
18. Source Commit y Audit Commit son independientes.
19. Puede existir consistencia eventual entre Source y Audit.
20. Puede existir una ventana con Source Fact confirmado y Audit aún
    inexistente.
21. No existe transacción distribuida obligatoria.
22. Un fallo de Audit no revierte el Source Aggregate.
23. Un Source Fact no confirmado no produce Audit válido.
24. PersistenceFailure no crea estado de dominio.
25. ConcurrencyConflict solamente afecta al Audit correspondiente.
26. Optimistic Concurrency protege Audit.Version.
27. SourceAggregateVersion no se usa como Audit ExpectedVersion.
28. Diferentes Audits tienen Boundaries independientes.
29. No existe un Aggregate global para toda la auditoría.
30. Consultas globales pertenecen al Read Side.
31. Un mismo Source Aggregate puede originar múltiples Audits.
32. Un nuevo Source Fact no reescribe un Audit anterior.
33. ActorId no incorpora Citizen al Boundary.
34. Organization permanece fuera del Boundary.
35. Membership permanece fuera del Boundary.
36. Role permanece fuera del Boundary.
37. Territory permanece fuera del Boundary.
38. Assembly permanece fuera del Boundary.
39. Proposal permanece fuera del Boundary.
40. Participation permanece fuera del Boundary.
41. Voting permanece fuera del Boundary.
42. Document permanece fuera del Boundary.
43. Notification permanece fuera del Boundary.
44. Integration permanece fuera del Boundary.
45. Domain Event permanece distinto de Integration Event.
46. External publication ocurre después del commit correspondiente.
47. Fallos de publicación no modifican Audit.
48. Retries de publicación no modifican Audit.
49. Outbox permanece fuera del Aggregate.
50. Read Models permanecen fuera del Write Boundary.
51. Projection Lag no constituye inconsistencia interna.
52. ReadModel.Version no gobierna Audit.Version.
53. Repository persiste una unidad Audit.
54. Repository no crea un Multi-Aggregate Boundary.
55. Authentication permanece fuera del Boundary.
56. Authorization permanece fuera del Boundary.
57. Permissions no amplían el Boundary.
58. Security Claims no forman parte automáticamente del estado.
59. Logs permanecen fuera del Boundary.
60. Observability permanece fuera del Boundary.
61. FIWARE permanece fuera del Boundary.
62. Sistemas municipales permanecen fuera del Boundary.
63. External Consumers no modifican Audit directamente.
64. Event Sourcing no cambia el Boundary.
65. Source Event Stream y Audit Event Stream permanecen separados.
66. Rehidratación solamente reconstruye Audit.
67. Replay no modifica otros Aggregates.
68. Cache, Replica y Snapshot no amplían el Boundary.
69. Performance no permite fusionar Aggregates.
70. Batch Processing conserva Audits independientes.
71. CorrelationId no crea consistencia compartida.
72. CausationId no crea ownership transaccional.
73. Timestamps distintos no constituyen inconsistencia por sí
    mismos.
74. Operaciones rechazadas no confirman estado parcial.
75. No existe compensación automática sobre otros Aggregates.
76. No existe Cascading Rollback desde Audit.
77. Audit no utiliza setters sobre otros Aggregates.
78. El Source Aggregate completo no se embebe en Audit.
79. El significado histórico permanece protegido.
80. Retención y eliminación no amplían ni redefinen el Boundary en
    versión 1.0.

---

# Restricciones

No está permitido:

- modificar otro Aggregate dentro de RecordAudit;
- incluir otro Aggregate como Internal Entity de Audit;
- utilizar SourceAggregateVersion como Audit.Version;
- utilizar SourceAggregateVersion como ExpectedVersion de Audit;
- compartir Version entre Aggregates;
- crear una transacción distribuida obligatoria por decisión del
  Aggregate;
- realizar rollback del Source Aggregate si Audit falla;
- tratar un Source Domain Event como estado interno de Audit;
- tratar un Integration Event como estado de Audit;
- modificar Audit directamente desde un External Consumer;
- permitir que Read Models modifiquen el Write Model;
- permitir que Repository amplíe el Aggregate Boundary;
- crear un Multi-Aggregate Repository para Audit;
- utilizar CorrelationId para justificar atomicidad distribuida;
- utilizar CausationId para justificar ownership;
- introducir FIWARE dentro del Aggregate;
- introducir sistemas municipales dentro del Aggregate;
- introducir logs, metrics o traces dentro del Boundary como
  conceptos de Audit por conveniencia;
- fusionar múltiples AuditId en una única unidad de consistencia para
  consultas;
- modificar un Audit previo cuando aparece un nuevo Source Fact;
- utilizar optimizaciones técnicas para evitar Invariants;
- convertir Outbox en estado de Audit;
- convertir estados técnicos de procesamiento en AuditStatus.

---

# Compatibilidad Arquitectónica

El Consistency Boundary de Audit es compatible con:

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

Estas compatibilidades no amplían el Consistency Boundary ni
introducen dependencias tecnológicas.

---

# Definición de Éxito

El Consistency Boundary del Aggregate **Audit** establece una unidad
de consistencia pequeña, explícita e independiente para cada hecho
auditable representado por AURA.

El modelo garantiza que:

- Audit constituye su propia Aggregate Root;
- cada AuditId define una unidad de consistencia independiente;
- State, Version, timestamps, referencias e Invariants pertenecen a
  Audit;
- la creación No Audit → Recorded ocurre dentro del propio Boundary;
- RecordAudit modifica exclusivamente Audit;
- AuditRecorded pertenece exclusivamente a Audit;
- Source Aggregate y Source Domain Event permanecen fuera;
- referencias externas no transfieren ownership;
- Audit.Version y SourceAggregateVersion permanecen independientes;
- Source Commit y Audit Commit son transacciones diferentes;
- consistencia eventual entre Source Aggregate y Audit es válida;
- puede existir una ventana temporal sin Audit después del Source
  Commit;
- un fallo de Audit no revierte el hecho original;
- no existe una transacción distribuida obligatoria;
- Optimistic Concurrency protege únicamente la identidad Audit;
- diferentes unidades Audit permanecen transaccionalmente
  independientes;
- nuevos Source Facts producen nueva trazabilidad sin reescribir
  Audits anteriores;
- otros Aggregates no son incorporados dentro del Boundary;
- Read Models permanecen fuera del Write Model;
- Integration Events permanecen fuera del estado;
- publicación externa y sus retries no modifican Audit;
- Repository persiste Audit como una sola unidad;
- Authentication y Authorization permanecen fuera del Aggregate;
- Permissions no amplían el Boundary;
- FIWARE, sistemas municipales, Infrastructure, logs y Observability
  permanecen fuera;
- CQRS mantiene separación entre escritura y lectura;
- Event Sourcing permanece compatible sin fusionar Event Streams de
  otros Aggregates;
- CorrelationId y CausationId permiten trazabilidad sin introducir
  atomicidad distribuida;
- ninguna optimización técnica puede modificar los límites
  conceptuales del Aggregate.

De esta forma, `DOMAIN-012J-Consistency-Boundary.md` establece
formalmente el Consistency Boundary del Aggregate **Audit** conforme
al patrón consolidado de AURA Core.