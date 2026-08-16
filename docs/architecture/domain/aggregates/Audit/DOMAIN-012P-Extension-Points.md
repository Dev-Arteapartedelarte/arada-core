# DOMAIN-012P — Audit Extension Points

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
- DOMAIN-012N-Performance-Rules.md
- DOMAIN-012O-Security-Model.md

---

# Objetivo

Este documento define formalmente los **Extension Points**
conceptuales del Aggregate **Audit**.

Los Extension Points establecen dónde el dominio puede evolucionar
en versiones futuras sin romper:

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
- Performance Rules;
- Security Model;
- significado histórico.

Los Extension Points no representan comportamiento ya existente.

---

# Principio Fundamental

Debe mantenerse:

```text
Extension Point

≠

Existing Domain Behavior
```

y:

```text
Extension Point

≠

Permission to Invent Architecture
```

Un Extension Point solamente identifica una zona de evolución
potencial.

Toda evolución requiere una decisión explícita de dominio.

---

# Regla de No Inferencia

La existencia de este documento no autoriza introducir:

- nuevos estados;
- nuevos Commands;
- nuevos Domain Events;
- nuevas Permissions;
- nuevas Internal Entities;
- nuevos Value Objects;
- nuevas relaciones obligatorias;
- nuevas políticas de retención;
- nuevas políticas de eliminación;
- nuevas políticas de anonimización;
- nuevas estrategias de persistencia;
- nuevas tecnologías.

sin definición formal.

---

# Modelo Actual Cerrado

La versión 1.0 permanece definida por:

```text
Lifecycle:

No Audit → Recorded
```

```text
Command:

RecordAudit
```

```text
Domain Event:

AuditRecorded
```

```text
Persisted State:

Recorded
```

```text
Initial Version:

1
```

Cualquier extensión futura debe partir de este modelo consolidado.

---

# Recorded Permanece Terminal

En versión 1.0:

```text
Recorded
```

permanece terminal.

Este documento no modifica dicha regla.

No se introduce:

```text
Recorded → Another State
```

como consecuencia de declarar Extension Points.

---

# Extension Point — Nuevos Commands

Audit puede evolucionar en el futuro mediante nuevos Commands
únicamente si aparece una nueva intención legítima del dominio.

Debe mantenerse:

```text
New Command

requires

New Explicit Domain Intent
```

---

# Regla para Nuevos Commands

Todo nuevo Command deberá definir explícitamente:

- intención;
- precondiciones;
- estado permitido;
- Invariants aplicables;
- Permissions;
- Versioning;
- Domain Event resultante;
- Consistency Boundary;
- efecto sobre timestamps;
- escenarios de rechazo.

---

# Nuevos Commands no se Infieren

No deben inferirse automáticamente Commands como:

```text
UpdateAudit

ModifyAudit

ArchiveAudit

DeleteAudit

RetryAudit

CorrectAudit

RedactAudit

AnonymizeAudit

InvalidateAudit
```

Su existencia futura requeriría definición explícita.

---

# Extension Point — Nuevos Estados

El Lifecycle puede evolucionar solamente cuando aparezca una necesidad
real de dominio que requiera un nuevo estado persistido.

Debe mantenerse:

```text
New State

requires

Explicit Lifecycle Meaning
```

---

# Nuevos Estados no se Infieren

No deben añadirse automáticamente:

```text
Draft

Pending

Active

Failed

Cancelled

Archived

Deleted

Expired

Redacted

Anonymized

Invalidated
```

como estados futuros por conveniencia técnica.

---

# Regla para Nuevos Estados

Todo nuevo estado deberá definir explícitamente:

- significado;
- entrada;
- salida;
- terminalidad;
- Commands que pueden alcanzarlo;
- Domain Events asociados;
- Invariants;
- Versioning;
- Permissions;
- Test Scenarios.

---

# Extension Point — Nuevas Transiciones

Una nueva transición solamente puede existir si ambos estados están
definidos formalmente.

Debe mantenerse:

```text
New Transition

requires

Defined Source State

+

Defined Target State
```

---

# No Transición Técnica

Estados técnicos de:

```text
Queue

Outbox

Broker

Repository

Projection

Integration
```

no deben convertirse en transiciones de Audit.

---

# Extension Point — Nuevos Domain Events

Audit puede incorporar nuevos Domain Events únicamente cuando exista
un nuevo hecho de dominio confirmado.

Debe mantenerse:

```text
New Domain Event

=

New Confirmed Audit Fact
```

---

# Regla para Nuevos Domain Events

Todo nuevo Domain Event deberá definir:

- nombre semántico;
- hecho representado;
- Command o comportamiento que lo produce;
- AggregateVersion resultante;
- EventId;
- OccurredAt;
- CorrelationId cuando corresponda;
- CausationId cuando corresponda;
- Payload mínimo;
- relación con Integration Events.

---

# No Domain Events Técnicos

No deben añadirse como Domain Events:

```text
AuditPersisted

AuditPublished

AuditProjectionUpdated

AuditRetryScheduled

AuditBrokerDelivered

AuditCached

AuditReplicated
```

cuando representen únicamente hechos técnicos.

---

# Extension Point — Nuevas Invariants

Una futura evolución puede requerir nuevas Invariants.

Toda nueva Invariant debe proteger una regla real del Aggregate.

Debe mantenerse:

```text
New Invariant

≠

Infrastructure Constraint
```

---

# Regla para Nuevas Invariants

Toda nueva Invariant deberá:

- pertenecer al Aggregate Audit;
- poder evaluarse dentro del Boundary correspondiente;
- preservar identidad;
- preservar estado válido;
- preservar coherencia con Commands;
- preservar coherencia con Domain Events;
- ser verificable mediante Test Scenarios.

---

# Invariants no se Crean por Persistencia

Una restricción de:

- base de datos;
- índice;
- formato;
- API;
- broker;
- serialización;

no se convierte automáticamente en Domain Invariant.

---

# Extension Point — Nuevas Permissions

Si aparece un nuevo Command, deberá definirse su Permission
correspondiente.

Debe mantenerse:

```text
New Command

requires

Permission Review
```

---

# Permissions no se Infieren

La existencia de un nuevo actor técnico, consumidor o integración no
crea automáticamente una Permission de dominio.

---

# Nuevos Actores

Si el dominio requiere distinguir nuevos tipos de actores,
deberá definirse explícitamente su relación con:

- Authentication;
- Authorization;
- Commands;
- Read Permissions;
- Integration Permissions.

Audit no debe incorporar Roles internos por defecto.

---

# Extension Point — Información de Trazabilidad

Audit puede evolucionar para preservar nueva información de
trazabilidad solamente cuando exista una necesidad explícita.

Debe mantenerse:

```text
New Traceability Attribute

requires

Defined Domain Meaning
```

---

# Nuevos Atributos no se Infieren

No debe añadirse información solamente porque:

- exista en el Source Payload;
- esté disponible técnicamente;
- facilite debugging;
- facilite reporting;
- facilite integración.

---

# Regla para Nuevos Atributos

Todo nuevo atributo deberá definir:

- significado;
- ownership;
- obligatoriedad;
- origen;
- inmutabilidad o mutabilidad;
- relación con Security;
- relación con Read Models;
- relación con Integration Events;
- impacto en Invariants.

---

# Extension Point — Value Objects

La versión 1.0 no define Value Objects específicos obligatorios para
Audit.

Una futura versión puede introducirlos únicamente cuando exista una
semántica propia que justifique:

```text
Value Object
```

---

# Regla para Nuevos Value Objects

Un nuevo Value Object deberá:

- representar un concepto del dominio;
- proteger sus propias reglas;
- ser coherente con Audit;
- no introducir dependencia tecnológica;
- no sustituir un Aggregate externo.

---

# Extension Point — Internal Entities

La versión 1.0 no establece Internal Entities concretas.

Una futura versión puede incorporarlas únicamente cuando exista:

- identidad interna;
- comportamiento propio;
- Lifecycle interno;
- necesidad de consistencia dentro de Audit.

---

# Internal Entity no es Aggregate Externo

No debe utilizarse una Internal Entity para absorber:

```text
Citizen

Organization

Assembly

Document

Notification

Integration
```

u otro Aggregate externo.

---

# Extension Point — Repository Contract

El Repository Contract puede evolucionar únicamente cuando una nueva
necesidad del Write Model lo requiera.

Debe mantenerse:

```text
Repository Evolution

follows

Aggregate Behavior
```

y no:

```text
Repository Convenience

creates

Aggregate Behavior
```

---

# Repository no Crece por Queries

Nuevas necesidades de:

- búsqueda;
- filtros;
- reporting;
- analytics;
- timeline;
- export;

no justifican ampliar AuditRepository.

Pertenecen al Read Side.

---

# Extension Point — Versioning

Versioning puede evolucionar solamente conforme aparezcan nuevas
modificaciones válidas del Aggregate.

Debe mantenerse:

```text
Valid Future Modification

N → N + 1
```

salvo que una futura definición explícita modifique formalmente la
regla.

---

# No Version Global

Ninguna extensión debe introducir automáticamente:

```text
GlobalAuditVersion
```

para ordenar todos los Audits.

---

# Extension Point — Concurrency

Nuevas operaciones de escritura deberán revisar:

```text
ExpectedVersion

PersistedVersion

Optimistic Concurrency
```

conforme al modelo consolidado.

---

# Concurrency no se Relaja Implícitamente

Una futura necesidad de Performance no autoriza:

```text
Last Write Wins
```

ni otra política distinta sin definición explícita.

---

# Extension Point — Consistency Boundary

El Boundary solamente puede ampliarse si una nueva regla de dominio
requiere consistencia atómica con nuevos elementos internos.

Debe mantenerse:

```text
Boundary Expansion

requires

Explicit Consistency Requirement
```

---

# No Boundary Expansion por Conveniencia

No debe ampliarse Audit para:

- evitar joins;
- evitar llamadas;
- reducir latencia;
- simplificar persistencia;
- simplificar UI;
- simplificar reporting.

---

# Cross-Aggregate Boundary

Ninguna extensión debe incorporar otro Aggregate dentro de Audit por
defecto.

Debe mantenerse:

```text
Audit

≠

Multi-Aggregate Consistency Boundary
```

---

# Extension Point — Integration Events

Nuevos Integration Events pueden existir solamente cuando:

- exista un Domain Fact válido;
- exista una necesidad explícita de interoperabilidad;
- exista un contrato público necesario.

---

# Regla para Nuevos Integration Events

Todo nuevo Integration Event deberá definir:

- hecho de origen;
- EventType;
- EventId;
- AggregateId;
- AggregateType;
- Contract Version;
- Payload mínimo;
- CorrelationId cuando corresponda;
- CausationId cuando corresponda;
- reglas de Security;
- consumidores conceptuales.

---

# Domain Event no Obliga Integration Event

Debe mantenerse:

```text
New Domain Event

≠

Automatic New Integration Event
```

---

# Extension Point — Read Models

Nuevas necesidades de consulta pueden generar nuevos Read Models sin
modificar el Write Model.

Este es uno de los principales Extension Points de Audit.

Debe mantenerse:

```text
New Query Requirement

→

Read Model Evolution
```

antes que:

```text
New Query Requirement

→

Aggregate Expansion
```

---

# Nuevas Vistas

Pueden definirse futuras vistas para:

- historial;
- timeline;
- correlación;
- causalidad;
- reporting;
- analytics;
- integración de lectura;

sin modificar Audit.

---

# Read Model no Cambia Ownership

Una nueva proyección no modifica:

- AuditId;
- Audit.Version;
- AuditStatus;
- Consistency Boundary;
- ownership.

---

# Extension Point — Cross-Aggregate Read Models

Pueden existir vistas combinadas con otros dominios.

Debe mantenerse:

```text
Cross-Aggregate Read Model

≠

Cross-Aggregate Write Model
```

---

# Extension Point — Performance

Nuevas necesidades de escala pueden resolverse mediante:

- Read Models;
- proyecciones;
- índices;
- caches;
- particionamiento;
- replicación;
- estrategias de persistencia;

en las capas correspondientes.

Estas posibilidades no modifican el Domain Model por sí mismas.

---

# Performance no Crea Dominio

Debe mantenerse:

```text
Scaling Need

≠

New Domain Concept
```

salvo que exista una nueva necesidad real de negocio.

---

# Extension Point — Security

El Security Model puede evolucionar cuando aparezcan nuevas:

- capacidades;
- clases de información;
- reglas de visibilidad;
- necesidades de exposición;
- contratos externos.

---

# Security no Crea Estados

Una nueva necesidad de seguridad no debe crear automáticamente:

```text
Locked

Hidden

Redacted

Anonymized
```

como AuditStatus.

---

# Security no Crea Commands Automáticamente

Necesidades de:

- redacción;
- anonimización;
- ocultamiento;
- retención;

no deben convertirse en Commands sin definición explícita de dominio.

---

# Extension Point — Retención

La versión 1.0 no define políticas de retención.

Una futura versión puede hacerlo únicamente mediante definición
explícita.

---

# Regla para Retención Futura

Una política futura deberá especificar:

- propósito;
- alcance;
- duración;
- autoridad;
- efectos sobre Audit;
- impacto en Read Models;
- impacto en Integration;
- impacto en Security;
- relación con significado histórico.

---

# Retención no se Infere

Debe mantenerse:

```text
Historical Data

≠

Automatic Infinite Retention
```

y:

```text
Storage Pressure

≠

Automatic Deletion Policy
```

---

# Extension Point — Deletion

La versión 1.0 no define:

```text
DeleteAudit
```

como Command.

Una futura política de eliminación requeriría una decisión explícita
y coordinada.

---

# Repository.delete() no Define Deletion Domain Rule

Debe mantenerse:

```text
Repository.delete()

≠

Existing DeleteAudit Behavior
```

---

# Extension Point — Redaction

La versión 1.0 no define:

```text
RedactAudit

AuditRedacted
```

Una futura necesidad deberá definir formalmente:

- qué se redacta;
- por qué;
- autoridad;
- efecto histórico;
- Versioning;
- eventos;
- Read Models;
- Integration Events.

---

# Extension Point — Anonymization

La versión 1.0 no define:

```text
AnonymizeAudit

AuditAnonymized
```

Una futura introducción deberá preservar coherencia con:

- identidad;
- trazabilidad;
- significado histórico;
- Security;
- Versioning.

---

# Extension Point — Historical Correction

Audit no se corrige mediante reescritura en versión 1.0.

Debe mantenerse:

```text
Later Source Fact

≠

Rewrite Previous Audit
```

---

# Corrección Futura

Si en el futuro el dominio requiere representar explícitamente una
relación entre un hecho original y otro correctivo, deberá definirse
mediante nuevos conceptos formales.

No debe reinterpretarse silenciosamente un Audit histórico.

---

# Extension Point — Provenance

Puede existir una evolución futura que requiera mayor información de
procedencia.

Cualquier nuevo dato de provenance deberá:

- tener significado de dominio;
- provenir de un contrato válido;
- respetar minimización;
- respetar Security;
- no transferir ownership.

---

# Extension Point — Correlation

El modelo puede evolucionar para enriquecer trazabilidad de flujos.

Sin embargo:

```text
Correlation

≠

Shared Consistency Boundary
```

debe preservarse.

---

# Extension Point — Causation

Una evolución puede enriquecer relaciones causales.

Debe mantenerse:

```text
Causation

≠

Mutation Authority
```

---

# Extension Point — Source Types

Audit puede recibir hechos de nuevos Aggregates o Bounded Contexts.

La incorporación de una nueva fuente no modifica automáticamente el
Aggregate Audit.

Debe mantenerse:

```text
New Source Type

≠

New Audit Lifecycle
```

---

# Nueva Fuente

Una nueva fuente deberá proporcionar un contrato reconocido que
permita identificar el hecho auditable.

Audit no debe inferir información que la fuente no proporciona.

---

# Source-Specific Rules

Si una fuente futura requiere reglas específicas, deberá evaluarse si
esas reglas pertenecen realmente a Audit o al Bounded Context
originador.

Debe mantenerse:

```text
Source Rule

belongs to

Source Context
```

salvo que exista una Invariant propia de Audit.

---

# Extension Point — Integration Management

Audit puede integrarse con nuevos sistemas mediante Integration.

No debe incorporar directamente:

- adaptadores;
- protocolos;
- SDKs;
- APIs externas;
- brokers;
- modelos externos.

---

# FIWARE

Una evolución de integración con:

```text
FIWARE

NGSI-LD

Context Broker
```

debe permanecer fuera del Aggregate Audit.

---

# Municipal Systems

Nuevos contratos con sistemas municipales deben evolucionar dentro de
Integration.

No modifican automáticamente Audit.

---


# Extension Point — Anti-Corruption Layer

Nuevos sistemas externos pueden requerir nuevas traducciones.

Debe mantenerse:

```text
External Model Evolution

≠

Audit Domain Model Evolution
```

salvo que exista una necesidad real del dominio Audit.

---

# Extension Point — Event Sourcing

Audit permanece:

```text
Event Sourcing Compatible
```

pero no obligatorio.

Una futura decisión de utilizar Event Sourcing no modifica por sí
misma:

- Commands;
- State Machine;
- Invariants;
- Domain Event semantics;
- Consistency Boundary.

---

# Event Sourcing no es Domain Extension

Debe mantenerse:

```text
Persistence Strategy Change

≠

Domain Behavior Change
```

---

# Extension Point — Snapshots

Snapshots pueden existir como optimización de Infrastructure.

No requieren:

- nuevo Command;
- nuevo Domain Event;
- nuevo estado;
- nueva Version de dominio.

---


# Extension Point — Cache

Nuevas estrategias de cache no modifican el Aggregate.

Debe mantenerse:

```text
Cache Strategy

≠

Domain Evolution
```

---

# Extension Point — Projection

Nuevas proyecciones pueden añadirse libremente mientras:

- consuman hechos válidos;
- no modifiquen Audit;
- no redefinan ownership;
- respeten Security;
- respeten minimización.

---

# Extension Point — Analytics

Nuevas capacidades analíticas deben evolucionar fuera del Write Model.

Debe mantenerse:

```text
Analytics Requirement

≠

Audit Aggregate Behavior
```

---


# Extension Point — Reporting

Reporting puede evolucionar mediante Read Models y Application.

No debe introducir Commands en Audit por conveniencia.

---


# Extension Point — Export

Nuevos formatos de exportación pertenecen al Read Side o Application.

Debe mantenerse:

```text
Export Format

≠

Domain Model
```

---


# Extension Point — Observability

Nuevas capacidades de:

- logs;
- metrics;
- traces;
- monitoring;

permanecen fuera del Aggregate.

---


# Observability no es Audit Extension

Debe mantenerse:

```text
Observability Evolution

≠

Audit Domain Evolution
```

---


# Extension Point — Cryptographic Protection

Una futura arquitectura puede introducir mecanismos de:

- encryption;
- hashing;
- signatures;
- tamper resistance.

Este documento no selecciona ninguno.

---


# Cryptography no se Convierte Automáticamente en Dominio

Debe mantenerse:

```text
Cryptographic Mechanism

≠

Audit Value Object
```

salvo definición explícita de dominio.

---


# Extension Point — Tamper Resistance

Si en el futuro se requiere una garantía de dominio adicional sobre
integridad histórica, deberá definirse explícitamente antes de
introducir:

```text
Hash Chain

Signature Chain

WORM

Blockchain

Append-Only Constraint
```

como parte de una decisión arquitectónica o de dominio.

---


# Extension Point — Legal or Regulatory Rules

Nuevos requerimientos legales o regulatorios pueden afectar Audit.

No deben incorporarse mediante suposición.

Toda nueva regla deberá identificar explícitamente:

- fuente normativa;
- alcance;
- comportamiento requerido;
- impacto en retención;
- impacto en exposición;
- impacto en eliminación;
- impacto en Security;
- impacto en histórico.

---


# Regulation no se Infiere

Debe mantenerse:

```text
Audit Domain

≠

Assumed Regulatory Policy
```

---


# Extension Point — Multi-Tenancy

La versión 1.0 no define reglas adicionales de Multi-Tenancy dentro
de Audit.

Si una futura necesidad requiere aislamiento adicional, deberá
definirse explícitamente su impacto en:

- identidad;
- Permissions;
- Read Models;
- Integration;
- Consistency Boundary.

---


# Extension Point — Organization Scope

La relación de Audit con Organization no debe ampliarse
automáticamente para resolver aislamiento o consulta.

Cualquier nuevo scope requiere una regla formal.

---


# Extension Point — Territory Scope

Del mismo modo, una futura necesidad territorial deberá preservar:

```text
Territory Reference

≠

Territory Ownership
```

---


# Extension Point — Actor Context

Una futura necesidad de enriquecer Actor Context no debe incorporar
Citizen, Membership o Role completos dentro de Audit.

---


# Extension Point — Event Metadata

Si una futura versión requiere metadata adicional en Domain Events,
deberá diferenciarse entre:

```text
Domain Meaning

and

Technical Metadata
```

Solamente la primera pertenece al contrato conceptual del dominio.

---


# Extension Point — Integration Metadata

Metadata técnica de transporte no debe convertirse automáticamente en
información del Integration Event conceptual.

---


# Extension Point — Version de Contratos

Domain Event Contracts, Integration Event Contracts, APIs y documentos
pueden evolucionar independientemente de:

```text
Audit.Version
```

---


# Independencia de Versiones

Debe mantenerse:

```text
Audit.Version

≠

Domain Contract Version

≠

Integration Contract Version

≠

API Version

≠

Documentation Version
```

---


# Extension Point — API

Una evolución de API no modifica automáticamente Audit.

Debe mantenerse:

```text
API Evolution

≠

Aggregate Evolution
```

---


# Extension Point — UI

Nuevas interfaces de usuario pueden requerir nuevas vistas.

La UI no debe inducir nuevas reglas de escritura por conveniencia.

---


# UI Requirement

Debe preferirse:

```text
UI Need

→

Read Model
```

cuando la necesidad sea exclusivamente de visualización.

---


# Extension Point — Search

Nuevas capacidades de búsqueda deben evolucionar en Read Models o
Infrastructure.

No deben modificar AuditRepository por defecto.

---


# Extension Point — Bulk Operations

Una futura necesidad de bulk processing debe preservar:

```text
One AuditId

=

One Consistency Boundary
```

---


# Bulk no Fusiona Identidades

Debe mantenerse:

```text
Bulk Operation

≠

One Giant Aggregate
```

---


# Extension Point — Parallel Processing

Nuevas estrategias de procesamiento paralelo pueden utilizar la
independencia entre AuditId.

No modifican reglas de concurrencia sobre una misma identidad.

---


# Extension Point — Idempotency

La estrategia técnica concreta de idempotencia permanece fuera del
Aggregate.

Una futura necesidad de formalizar idempotencia como regla de dominio
requerirá definición explícita.

---


# SourceEventId no se Convierte Automáticamente en Idempotency Key

Debe mantenerse:

```text
SourceEventId

≠

Mandatory Audit Idempotency Key
```

salvo definición futura explícita.

---


# Extension Point — Deduplication

Deduplicación técnica no debe crear una regla de cardinalidad de
dominio no definida.

Debe mantenerse:

```text
Technical Deduplication

≠

One-to-One Domain Cardinality
```

---


# Extension Point — Cardinality

La versión 1.0 no establece:

```text
One SourceEventId

=

Exactly One Audit
```

como regla universal.

Cualquier cardinalidad futura requiere definición explícita.

---


# Extension Point — Ordering

La versión 1.0 no establece orden global entre Audit Aggregates.

Una futura necesidad de orden global requeriría una decisión formal.

---


# Per-Aggregate Ordering

Debe preservarse:

```text
AggregateVersion

=

Ordering within AuditId
```

cuando existan múltiples Versions futuras.

---


# Global Ordering no se Infiere

Debe mantenerse:

```text
Per Aggregate Version

≠

Global Audit Sequence
```

---


# Extension Point — Historical Views

Nuevas vistas históricas pueden evolucionar libremente en Read Side.

No deben reescribir hechos confirmados.

---


# Extension Point — Correction Views

Una vista puede relacionar:

```text
Original Fact

Corrective Fact
```

sin modificar ninguno de los Audits correspondientes.

---


# Extension Point — Retrospective Interpretation

Nuevas capacidades analíticas pueden reinterpretar datos para
reporting.

No deben modificar el significado histórico del Aggregate.

Debe mantenerse:

```text
New Interpretation

≠

Historical Rewrite
```

---


# Extension Point — New Bounded Context Consumers

Nuevos Bounded Contexts pueden consumir Audit mediante contratos
explícitos.

Su incorporación no modifica automáticamente Audit.

---


# Consumer-specific Models

Un consumidor puede requerir una representación propia.

Debe utilizar:

```text
Integration Contract

or

Read Model
```

en lugar de expandir Audit para satisfacer una necesidad externa.

---


# Extension Point — New External Systems

Nuevos sistemas externos deben integrarse mediante:

```text
Integration
```

y no mediante dependencia directa del Aggregate.

---


# Technology Replacement

Cambiar:

- database;
- ORM;
- broker;
- cache;
- transport;
- framework;
- provider;

no constituye una extensión del dominio.

---


# Infrastructure Evolution

Debe mantenerse:

```text
Infrastructure Evolution

≠

Domain Evolution
```

salvo que surja una necesidad real del dominio.

---


# Extension Governance

Toda extensión futura debe revisar coherencia con:

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

Test Scenarios

Performance Rules

Security Model
```

---


# Impact Analysis

Antes de incorporar una extensión deberá determinarse:

- qué problema de dominio resuelve;
- qué conceptos existentes afecta;
- qué documentos requieren cambio;
- qué nuevas Invariants aparecen;
- qué Commands cambian;
- qué Domain Events cambian;
- qué Permissions cambian;
- qué Read Models cambian;
- qué Integration Events cambian;
- qué Test Scenarios deben añadirse;
- si cambia el Consistency Boundary.

---


# No Cambio Parcial de Contrato

No debe modificarse solamente un documento cuando una nueva regla
afecta múltiples contratos conceptuales.

Debe mantenerse:

```text
Domain Evolution

=

Coherent Contract Evolution
```

---


# Backward Compatibility Conceptual

Una evolución futura debe preservar el significado de hechos
históricos ya confirmados.

Debe mantenerse:

```text
New Domain Version

≠

Reinterpret Old Audit Facts
```

---


# Historical Event Compatibility

`AuditRecorded` histórico debe conservar su significado original.

Una evolución futura no debe convertirlo retrospectivamente en un
hecho diferente.

---


# Integration Contract Compatibility

Las evoluciones de Integration Events deben respetar versionado
contractual independiente.

No deben reutilizar silenciosamente un contrato incompatible con
significado distinto.

---


# Read Model Compatibility

Los Read Models pueden reconstruirse conforme a nuevas necesidades,
pero no deben inventar hechos inexistentes.

---


# Test Requirement

Toda extensión deberá incorporar Test Scenarios para:

```text
success

rejection

invariants

permissions

versioning

domain events

consistency boundary

security

read models

integration
```

cuando correspondan.

---


# Performance Review

Toda extensión deberá revisar que:

- el Aggregate permanezca pequeño;
- no se cargue historial global;
- no se embeban Aggregates externos;
- nuevas consultas permanezcan en Read Side;
- no se introduzcan bloqueos globales innecesarios.

---


# Security Review

Toda extensión deberá revisar:

- minimización;
- exposición;
- Permissions;
- información sensible;
- Read Model visibility;
- Integration Event payloads;
- ausencia de credenciales.

---


# Boundary Review

Toda nueva información o comportamiento deberá responder:

```text
Does this require atomic consistency with Audit?
```

Si la respuesta es no, no debe incorporarse automáticamente al
Aggregate.

---


# Ownership Review

Toda extensión debe identificar:

```text
Who owns this concept?
```

Si otro Bounded Context posee el concepto, Audit debe mantener una
referencia o contrato, no absorber ownership.

---


# Source of Truth Review

Toda nueva capacidad deberá mantener:

```text
Audit

=

Source of Truth only for Audit
```

y no convertirse en autoridad sobre otros dominios.

---


# Extension Point — Documentation

La evolución de Audit debe actualizar la documentación de dominio
correspondiente.

Ninguna nueva regla se considera parte del contrato consolidado hasta
ser formalmente definida.

---


# Extension Point — ADR

Una decisión que modifique arquitectura, persistencia, integración,
seguridad o estrategia técnica puede requerir documentación
arquitectónica separada.

Dicha decisión no debe introducirse implícitamente mediante este
documento.

---


# Domain Rule versus Architecture Decision

Debe mantenerse:

```text
Domain Rule

≠

Architecture Decision
```

aunque ambas puedan relacionarse.

---


# Extensión Válida

Una extensión es válida cuando:

```text
Explicit Domain Need
    │
    ▼
Defined Concept
    │
    ▼
Defined Rules
    │
    ▼
Updated Contracts
    │
    ▼
Updated Tests
    │
    ▼
Preserved Historical Meaning
```

---


# Extensión Inválida

Una extensión es inválida cuando surge solamente de:

```text
Technical Convenience

Framework Limitation

Database Shape

UI Convenience

Broker Feature

Integration Shortcut
```

sin una necesidad real de dominio.

---


# Reglas Fundamentales

Los Extension Points de Audit deben cumplir:

1. Extension Point no representa comportamiento existente.
2. Extension Point no autoriza inventar arquitectura.
3. El modelo actual No Audit → Recorded permanece vigente.
4. Recorded permanece terminal en versión 1.0.
5. RecordAudit permanece como único Command oficial.
6. AuditRecorded permanece como único Domain Event oficial.
7. Nuevos Commands requieren intención explícita.
8. Nuevos Commands requieren revisión de Invariants.
9. Nuevos Commands requieren revisión de Permissions.
10. Nuevos Commands requieren Domain Events cuando corresponda.
11. Nuevos estados requieren significado explícito.
12. Nuevos estados requieren Lifecycle formal.
13. Nuevas transiciones requieren estados definidos.
14. Estados técnicos no se convierten en estados de Audit.
15. Nuevos Domain Events requieren nuevos hechos confirmados.
16. Eventos técnicos no se convierten automáticamente en Domain
    Events.
17. Nuevas Invariants deben proteger reglas reales del Aggregate.
18. Constraints de Infrastructure no son automáticamente Invariants.
19. Nuevas Permissions siguen a nuevas capacidades.
20. Nuevos actores técnicos no crean Permissions automáticamente.
21. Nuevos atributos requieren significado de dominio.
22. Source Payload no determina atributos nuevos.
23. Nuevos Value Objects requieren semántica propia.
24. Nuevas Internal Entities requieren identidad o comportamiento
    interno real.
25. Internal Entities no absorben Aggregates externos.
26. Repository evoluciona siguiendo al Aggregate.
27. Queries no hacen crecer AuditRepository.
28. Nuevas modificaciones válidas preservan Versioning.
29. No se introduce GlobalAuditVersion automáticamente.
30. Nuevas escrituras revisan Optimistic Concurrency.
31. Performance no relaja Concurrency implícitamente.
32. Consistency Boundary solamente cambia por necesidad explícita de
    consistencia.
33. Convenience no amplía el Boundary.
34. Audit no se convierte en Multi-Aggregate Boundary.
35. Nuevos Integration Events requieren necesidad explícita.
36. Nuevos Domain Events no generan Integration Events
    automáticamente.
37. Nuevos Query Requirements deben preferir evolución del Read Side.
38. Nuevas vistas no modifican ownership.
39. Cross-Aggregate Read Models no crean Cross-Aggregate Write Models.
40. Scaling Needs no crean conceptos de dominio automáticamente.
41. Security Needs no crean estados automáticamente.
42. Retention no está definida en versión 1.0.
43. Deletion no está definida como Command en versión 1.0.
44. Redaction no está definida en versión 1.0.
45. Anonymization no está definida en versión 1.0.
46. Historical Correction no reescribe Audits previos.
47. Provenance futura requiere significado explícito.
48. Correlation no crea consistencia compartida.
49. Causation no crea mutation authority.
50. Nuevas Source Types no cambian automáticamente Audit Lifecycle.
51. Source-specific rules permanecen en Source Context salvo
    Invariant propia.
52. Integration Management permanece fuera del Aggregate.
53. FIWARE permanece fuera del Aggregate.
54. Municipal Systems permanecen fuera del Aggregate.
55. Anti-Corruption Layer puede evolucionar sin modificar Audit.
56. Event Sourcing sigue siendo compatible pero no obligatorio.
57. Persistence Strategy no equivale a Domain Evolution.
58. Snapshots no constituyen Domain Facts.
59. Cache Strategy no constituye Domain Evolution.
60. Nuevas Projections no modifican Audit.
61. Analytics permanece fuera del Write Model.
62. Reporting permanece fuera del Write Model.
63. Export permanece fuera del Domain Model.
64. Observability permanece fuera del Domain Model.
65. Cryptographic Protection no se impone desde este documento.
66. Tamper Resistance no selecciona tecnología automáticamente.
67. Regulatory Rules no se incorporan por suposición.
68. Multi-Tenancy no está ampliado por este documento.
69. Actor Context no incorpora Citizen, Membership o Role completos.
70. Event Metadata debe diferenciar dominio de metadata técnica.
71. Contract Versions permanecen independientes de Audit.Version.
72. API Evolution no equivale a Aggregate Evolution.
73. UI Needs deben preferir Read Models cuando sean de presentación.
74. Search evoluciona fuera del Write Model.
75. Bulk Operations preservan un Boundary por AuditId.
76. Parallel Processing no elimina concurrencia por identidad.
77. Idempotency técnica permanece fuera del Aggregate.
78. SourceEventId no es Idempotency Key obligatoria.
79. Deduplicación técnica no crea cardinalidad de dominio.
80. No existe cardinalidad universal uno-a-uno SourceEventId/Audit.
81. No existe orden global obligatorio.
82. AggregateVersion preserva orden por AuditId cuando corresponda.
83. Historical Views no reescriben hechos.
84. New Interpretation no equivale a Historical Rewrite.
85. Nuevos consumidores utilizan contratos explícitos.
86. Consumer-specific models no hacen crecer el Aggregate.
87. Nuevos sistemas externos se integran fuera del Aggregate.
88. Technology Replacement no constituye Domain Evolution.
89. Toda extensión requiere Impact Analysis.
90. Domain Evolution debe actualizar contratos afectados
    coherentemente.
91. Backward Compatibility preserva significado histórico.
92. AuditRecorded histórico conserva su significado.
93. Integration Contracts evolucionan independientemente.
94. Read Models pueden evolucionar sin inventar hechos.
95. Toda extensión requiere nuevos Test Scenarios cuando corresponda.
96. Toda extensión requiere Performance Review.
97. Toda extensión requiere Security Review.
98. Toda extensión requiere Boundary Review.
99. Toda extensión requiere Ownership Review.
100. Ninguna extensión se incorpora al modelo consolidado sin
     definición formal.

---

# Restricciones

No está permitido:

- utilizar Extension Points como comportamiento ya aprobado;
- introducir arquitectura nueva desde este documento;
- añadir Commands sin intención explícita;
- añadir estados por conveniencia técnica;
- añadir Domain Events para representar acciones de Infrastructure;
- añadir Invariants a partir de restricciones de base de datos;
- añadir Permissions por existencia de actores técnicos;
- añadir atributos porque estén disponibles en Source Payload;
- añadir Value Objects sin semántica propia;
- añadir Internal Entities para absorber Aggregates externos;
- ampliar Repository por necesidades de query;
- crear GlobalAuditVersion;
- relajar Concurrency sin definición explícita;
- ampliar Consistency Boundary por Performance;
- crear Integration Events automáticamente por cada Domain Event;
- ampliar Audit para resolver nuevas consultas;
- introducir Retention sin definición formal;
- introducir DeleteAudit sin definición formal;
- introducir RedactAudit sin definición formal;
- introducir AnonymizeAudit sin definición formal;
- reescribir Audit histórico para representar un nuevo Source Fact;
- incorporar reglas propias del Source Context dentro de Audit sin
  justificación;
- incorporar FIWARE dentro del Aggregate;
- incorporar sistemas municipales dentro del Aggregate;
- imponer Event Sourcing;
- convertir Snapshot, Cache o Projection en conceptos de dominio sin
  justificación;
- imponer hashing, firmas, blockchain o WORM;
- inferir políticas regulatorias;
- convertir metadata técnica en información de dominio
  automáticamente;
- confundir Contract Version con Audit.Version;
- utilizar UI o API como autoridad del Domain Model;
- fusionar Audits durante Bulk Operations;
- convertir SourceEventId en Idempotency Key obligatoria sin decisión
  explícita;
- introducir cardinalidad uno-a-uno no definida;
- introducir orden global por conveniencia;
- reinterpretar hechos históricos;
- utilizar limitaciones tecnológicas para crear comportamiento de
  dominio;
- modificar solamente un contrato cuando la evolución afecta varios;
- incorporar una extensión sin actualizar Test Scenarios cuando
  corresponda.

---

# Compatibilidad Arquitectónica

Los Extension Points de Audit son compatibles con:

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
- Anti-Corruption Layer;
- Persistence Ignorance;
- Open/Closed Principle;
- High Cohesion;
- Low Coupling.

Estas compatibilidades no constituyen decisiones tecnológicas ni
autorizan modificaciones al modelo consolidado sin definición
explícita.

---

# Definición de Éxito

Los Extension Points del Aggregate **Audit** permiten evolucionar el
dominio de manera controlada sin convertir posibilidades futuras en
comportamiento presente.

El modelo conserva como base:

```text
Confirmed Source Fact

    │
    ▼

RecordAudit

    │
    ▼

No Audit → Recorded

    │
    ▼

Audit.Version = 1

    │
    ▼

AuditRecorded
```

y garantiza que:

- Recorded permanezca terminal mientras no exista una evolución
  explícita;
- RecordAudit continúe siendo el único Command oficial de versión
  1.0;
- AuditRecorded continúe siendo el único Domain Event oficial de
  versión 1.0;
- nuevos Commands requieran definición formal;
- nuevos estados requieran Lifecycle formal;
- nuevos Domain Events representen hechos reales;
- nuevas Invariants protejan reglas reales del Aggregate;
- nuevas Permissions acompañen nuevas capacidades;
- nuevos atributos tengan significado, ownership y reglas claras;
- Value Objects e Internal Entities no se introduzcan por
  conveniencia;
- Repository evolucione siguiendo comportamiento y no necesidades de
  consulta;
- Versioning y Concurrency permanezcan coherentes;
- Consistency Boundary solamente cambie por necesidad explícita;
- nuevos Integration Events requieran contratos públicos reales;
- nuevas consultas evolucionen preferentemente mediante Read Models;
- Performance no cree conceptos de dominio;
- Security no cree estados ni Commands implícitos;
- Retention, Deletion, Redaction y Anonymization permanezcan sin
  definir hasta una decisión explícita;
- hechos correctivos futuros no reescriban Audits anteriores;
- nuevas fuentes permanezcan desacopladas;
- FIWARE, sistemas municipales e Infrastructure permanezcan fuera del
  Aggregate;
- Event Sourcing permanezca compatible pero no impuesto;
- Analytics, Reporting, Search, Export y Observability permanezcan
  fuera del Write Model;
- mecanismos criptográficos no se conviertan en dominio sin
  definición explícita;
- Contract Versions permanezcan independientes de Audit.Version;
- Bulk, Parallel Processing, Idempotency y Deduplication no
  introduzcan reglas de cardinalidad o Boundary no definidas;
- no exista orden global obligatorio;
- el significado histórico permanezca estable;
- toda evolución futura incluya Impact Analysis, actualización
  coherente de contratos y Test Scenarios;
- ninguna necesidad técnica se convierta silenciosamente en una nueva
  regla del dominio.

De esta forma, `DOMAIN-012P-Extension-Points.md` establece los
Extension Points oficiales del Aggregate **Audit** conforme al patrón
consolidado de AURA Core.