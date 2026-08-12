# DOMAIN-007N — Proposal Performance Rules

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Proposal Management

Aggregate:
Proposal

Autor:
ARADA

Documentos relacionados:

- DOMAIN-007-Aggregate.md
- DOMAIN-007A-Lifecycle.md
- DOMAIN-007B-State-Machine.md
- DOMAIN-007C-Commands.md
- DOMAIN-007D-Domain-Events.md
- DOMAIN-007E-Invariants.md
- DOMAIN-007F-Permissions.md
- DOMAIN-007G-Repository-Contract.md
- DOMAIN-007H-Examples.md
- DOMAIN-007I-Versioning.md
- DOMAIN-007J-Consistency-Boundary.md
- DOMAIN-007K-Integration-Events.md
- DOMAIN-007L-Read-Model.md
- DOMAIN-007M-Test-Scenarios.md
- CORE-003-Shared-Kernel.md
- CORE-004-Ubiquitous-Language.md
- CORE-005-Domain-Events.md
- CORE-006-Domain-Invariants.md
- CORE-007-Strategic-Design.md
- CORE-008-Aggregate-Design-Rules.md
- CORE-011-Repository-Contracts.md

---

# Objetivo

Definir las reglas conceptuales de rendimiento del Aggregate
**Proposal**.

Estas reglas establecen los principios que deben preservar la
eficiencia operativa, escalabilidad y capacidad de evolución del
Aggregate sin comprometer:

- identidad;
- invariantes;
- ciclo de vida;
- State Machine;
- consistencia;
- versionado;
- Domain Events;
- límites del Aggregate;
- independencia tecnológica;
- comportamiento del dominio.

Las Performance Rules no constituyen optimizaciones específicas de
Infrastructure.

Su propósito es establecer restricciones arquitectónicas que
permitan optimizar la implementación de Proposal sin alterar su
modelo conceptual.

---

# Propósito

El rendimiento de Proposal debe obtenerse mediante una correcta
separación de responsabilidades y no mediante la eliminación de
reglas del dominio.

Una implementación puede optimizar:

- almacenamiento;
- recuperación;
- serialización;
- consultas;
- índices;
- cachés;
- proyecciones;
- transporte;
- procesamiento de eventos;
- concurrencia;
- escalamiento.

Estas optimizaciones no pueden modificar el significado
conceptual de Proposal.

Debe mantenerse:

```text
Performance Optimization

≠

Domain Simplification
```

Una optimización válida mejora la ejecución sin alterar el
comportamiento oficial del Aggregate.

---

# Principios

Las reglas de rendimiento de Proposal siguen los siguientes
principios:

- el dominio conserva prioridad sobre la optimización técnica;
- las invariantes nunca se omiten por rendimiento;
- el Aggregate mantiene un límite de consistencia acotado;
- las consultas complejas se separan del Write Model;
- los Read Models pueden optimizarse independientemente;
- la persistencia debe respetar el Aggregate completo;
- las referencias externas utilizan identificadores;
- no se cargan otros Aggregates como parte interna de Proposal;
- la concurrencia utiliza Version;
- los eventos permiten desacoplar procesos secundarios;
- las integraciones externas no forman parte de la transacción
  interna;
- las operaciones de lectura no modifican Proposal;
- las optimizaciones de Infrastructure permanecen fuera del
  dominio;
- ninguna optimización puede modificar el lenguaje ubicuo.

---

# Regla Fundamental

La regla fundamental de rendimiento es:

```text
Optimize Infrastructure

Preserve Domain
```

Nunca:

```text
Optimize by Breaking Domain Rules
```

El rendimiento no constituye una excepción a las invariantes.

---

# Prioridad de Correctitud

La correctitud del dominio posee prioridad sobre cualquier
optimización.

Debe mantenerse:

```text
Domain Correctness

>

Performance Shortcut
```

No está permitido mejorar tiempos de ejecución mediante:

- omisión de invariantes;
- omisión de validaciones obligatorias;
- modificación directa de estado;
- modificación directa de Version;
- eliminación de controles de concurrencia;
- bypass del Aggregate Root;
- escritura directa sobre Read Models;
- modificación simultánea de otros Aggregates;
- publicación prematura de Integration Events.

---

# Aggregate Pequeño y Cohesivo

Proposal debe mantener dentro de su límite únicamente los
conceptos necesarios para proteger su consistencia.

El Aggregate no debe crecer mediante incorporación de otros
Aggregates.

No deben formar parte interna de Proposal:

```text
Organization

Citizen

Membership

Role

Territory

Assembly

Participation

Voting

Document

Notification

Audit

Integration
```

Mantener el Aggregate acotado reduce:

- volumen de carga;
- superficie transaccional;
- conflictos de concurrencia;
- complejidad de persistencia;
- acoplamiento;
- tiempo de reconstrucción;
- riesgo de bloqueos conceptuales.

Esta regla de rendimiento coincide con el límite DDD definido en:

```text
DOMAIN-007J-Consistency-Boundary.md
```

---

# Referencias por Identidad

Proposal se relaciona con otros Aggregates mediante
identificadores.

Ejemplos:

```text
OrganizationId

CitizenId

MembershipId

TerritoryId

AssemblyId

ParticipationId

VotingId

DocumentId
```

Estas referencias permiten mantener el Aggregate independiente y
evitan cargar grafos completos de objetos externos para ejecutar
comportamiento propio de Proposal.

Debe mantenerse:

```text
External Aggregate Reference

=

AggregateId
```

y no:

```text
External Aggregate Reference

=

Complete Mutable Aggregate
```

---

# Regla de Carga

Una operación de escritura sobre Proposal debe cargar únicamente
la información necesaria para proteger las invariantes del
Aggregate.

No debe requerirse cargar automáticamente:

```text
Organization Aggregate

Citizen Aggregate

Membership Aggregate

Territory Aggregate

Assembly Aggregate

Participation Aggregate

Voting Aggregate

Document Aggregate
```

como parte del estado interno de Proposal.

Cuando una regla requiera información externa, dicha coordinación
debe respetar los límites definidos por la arquitectura.

---

# Regla de No Sobrelectura

El Write Model no debe utilizarse como mecanismo general para
resolver consultas que no requieren comportamiento de dominio.

Debe evitarse:

```text
Load Proposal Aggregate

↓

Read Data Only

↓

Discard Aggregate
```

cuando exista una proyección adecuada para la consulta.

Las consultas deben utilizar los Read Models definidos en:

```text
DOMAIN-007L-Read-Model.md
```

cuando corresponda.

---

# Separación Write / Read

Proposal mantiene separación conceptual entre:

```text
Write Side

Proposal Aggregate
```

y:

```text
Read Side

Proposal Read Models
```

El Write Side está optimizado para:

- comportamiento;
- invariantes;
- transiciones;
- consistencia;
- Domain Events;
- versionado.

El Read Side puede estar optimizado para:

- búsqueda;
- filtrado;
- ordenamiento;
- paginación;
- estadísticas;
- dashboards;
- agregaciones;
- visualización.

Debe mantenerse:

```text
Write Model

≠

Read Model
```

---

# Read Models Especializados

Las necesidades de lectura no deben provocar crecimiento
innecesario del Aggregate.

Las proyecciones oficiales pueden proporcionar vistas como:

```text
ProposalSummary

ProposalDetail

ProposalDirectory

ProposalStatus

ProposalOrganization

ProposalTerritory

ProposalAssembly

ProposalProposer

ProposalReview

ProposalActivity

ProposalStatistics
```

Cada proyección puede optimizarse según su propósito.

Una necesidad de consulta nueva puede producir una nueva
proyección sin modificar Proposal.

---

# Desnormalización de Lectura

Los Read Models pueden desnormalizar información cuando esto
mejore las consultas.

Ejemplo conceptual:

```text
ProposalSummary

ProposalId

Title

ProposalType

ProposalStatus

OrganizationName

TerritoryName

UpdatedAt
```

La presencia de información desnormalizada no modifica los
límites del dominio.

Debe mantenerse:

```text
Read Model Denormalization

≠

Aggregate Composition
```

---

# Paginación

Las colecciones de lectura potencialmente grandes deben admitir
paginación.

Ejemplos:

```text
ProposalDirectory

ProposalActivity

ProposalStatistics
```

La paginación pertenece al modelo de consulta y no al
comportamiento interno del Aggregate.

Proposal no debe cargar colecciones ilimitadas para resolver una
consulta de listado.

---

# Filtrado

Las operaciones de filtrado deben ejecutarse preferentemente sobre
Read Models cuando no representen comportamiento de dominio.

Ejemplos:

```text
Proposals by Organization

Proposals by Territory

Proposals by Assembly

Proposals by Status

Proposals by Type

Proposals by Proposer
```

Estas consultas no requieren modificar Proposal.

---

# Ordenamiento

El ordenamiento de resultados pertenece al lado de lectura.

Ejemplos:

```text
CreatedAt

UpdatedAt

SubmittedAt

AcceptedAt

RejectedAt

Title
```

El Aggregate no debe incorporar comportamiento artificial
únicamente para satisfacer necesidades de ordenamiento de
interfaces o reportes.

---

# Búsqueda

Las búsquedas de Proposal deben resolverse mediante modelos
especializados de lectura.

Ejemplos:

```text
Search by Title

Search by Status

Search by Organization

Search by Territory

Search by Assembly

Search by Proposer
```

La tecnología utilizada para búsqueda pertenece a
Infrastructure.

---

# Índices

Los índices utilizados para acelerar consultas pertenecen a
Infrastructure.

Pueden existir índices conceptualmente sobre campos como:

```text
ProposalId

OrganizationId

TerritoryId

AssemblyId

ProposalStatus

ProposalType

CreatedAt

UpdatedAt
```

La existencia física de índices no forma parte del Aggregate.

Cambiar un índice no modifica el dominio.

---

# Regla de Índices

Los índices pueden optimizar:

- búsqueda;
- filtrado;
- ordenamiento;
- paginación;
- recuperación por identidad.

No pueden definir:

- invariantes;
- State Machine;
- permisos;
- comportamiento;
- identidad conceptual.

Debe mantenerse:

```text
Database Index

≠

Domain Rule
```

---

# Recuperación por Identidad

La operación principal de recuperación del Write Model debe
utilizar:

```text
ProposalId
```

El Repository debe permitir recuperar la unidad de consistencia
correspondiente sin requerir búsquedas ambiguas.

Debe mantenerse:

```text
ProposalId

↓

Proposal Aggregate
```

La identidad constituye el mecanismo conceptual principal para
localizar el Aggregate.

---

# Persistencia como Unidad

Proposal debe persistirse respetando su límite de consistencia.

Una optimización no puede convertir la persistencia en una serie
de modificaciones parciales que permitan estados intermedios
inválidos.

Debe mantenerse:

```text
Valid Aggregate State

↓

Persistence

↓

Valid Persisted Aggregate State
```

Nunca:

```text
Partial Update

↓

Temporarily Invalid Domain State
```

cuando dicha actualización rompa las invariantes del Aggregate.

---

# Regla de Escritura

Toda escritura debe originarse en comportamiento válido del
Aggregate.

No debe optimizarse mediante:

```text
Direct Database Update

↓

ProposalStatus Changed
```

sin ejecutar las reglas correspondientes del dominio.

La optimización técnica de persistencia puede existir siempre que
el resultado preserve exactamente el comportamiento y las
invariantes del Aggregate.

---

# Versionado Optimista

Proposal utiliza:

```text
Version
```

para controlar concurrencia optimista.

El versionado permite evitar bloqueos pesados como requisito
conceptual permanente y detectar modificaciones concurrentes
incompatibles.

Debe mantenerse:

```text
ExpectedVersion

=

PersistedVersion
```

antes de confirmar una modificación.

Si las versiones no coinciden:

```text
Concurrency Conflict
```

La especificación completa se encuentra en:

```text
DOMAIN-007I-Versioning.md
```

---

# Regla de Conflictos

Una optimización no puede desactivar la verificación de Version
para aumentar throughput.

Debe mantenerse:

```text
Higher Throughput

≠

Lost Update Acceptance
```

Los conflictos concurrentes deben detectarse.

No deben resolverse mediante sobrescritura silenciosa.

---

# Contención del Aggregate

Mantener Proposal como Aggregate independiente reduce la
contención entre operaciones no relacionadas.

Una modificación sobre:

```text
Proposal A
```

no debe requerir bloquear conceptualmente:

```text
Proposal B
```

cuando ambas poseen identidades diferentes y no comparten el mismo
límite de consistencia.

Debe mantenerse:

```text
ProposalId A

≠

ProposalId B
```

como unidades independientes de modificación.

---

# Operaciones de Escritura

Los Commands definidos para Proposal deben afectar únicamente la
instancia correspondiente del Aggregate.

Ejemplos:

```text
CreateProposal

SubmitProposal

StartProposalReview

AcceptProposal

RejectProposal

WithdrawProposal

ArchiveProposal
```

Una operación no debe cargar ni modificar múltiples Proposal
cuando el Command representa una intención sobre una sola
identidad.

---

# Commands y Rendimiento

Los Commands deben contener únicamente la información necesaria
para expresar la intención y proporcionar la trazabilidad definida
por el modelo.

No deben utilizarse como transporte arbitrario de:

- Aggregates completos;
- Read Models completos;
- grandes colecciones no relacionadas;
- infraestructura;
- conexiones;
- sesiones técnicas.

Debe mantenerse:

```text
Command

=

Intent
```

No:

```text
Command

=

Application State Container
```

---

# Domain Events y Rendimiento

Los Domain Events permiten desacoplar procesos derivados del
comportamiento principal de Proposal.

Una operación válida puede producir:

```text
ProposalAccepted
```

sin ejecutar dentro de la misma responsabilidad interna todos los
procesos secundarios que puedan depender de ese hecho.

Esto permite mantener separado:

```text
Proposal Transaction
```

de:

```text
External Reactions
```

Los Domain Events no deben utilizarse para evitar invariantes
internas que deban protegerse antes del Commit.

---

# Procesamiento Asíncrono

Los procesos que no forman parte de la consistencia inmediata de
Proposal pueden ejecutarse de forma desacoplada cuando la
arquitectura correspondiente lo permita.

Ejemplos conceptuales:

```text
Notification

Read Model Projection

Audit Projection

External Integration

Analytics
```

Debe mantenerse:

```text
Proposal Commit

↓

Confirmed Domain Fact

↓

Secondary Processing
```

El procesamiento secundario no debe incorporarse al Aggregate
únicamente para obtener consistencia inmediata donde no es
necesaria.

---

# Regla de Trabajo Secundario

Proposal debe ejecutar sincrónicamente únicamente el
comportamiento necesario para preservar su estado válido.

Procesos externos no pertenecientes al límite del Aggregate deben
mantenerse fuera de su transacción.

No debe ocurrir:

```text
AcceptProposal

↓

Update Proposal

↓

Update Voting

↓

Send Notification

↓

Update Audit

↓

Call Municipality

↓

Commit Everything
```

como una única transacción del Aggregate.

Debe mantenerse el límite definido en:

```text
DOMAIN-007J-Consistency-Boundary.md
```

---

# Integration Events y Rendimiento

Los Integration Events permiten comunicar hechos confirmados a
otros Bounded Contexts y sistemas sin ampliar la transacción de
Proposal.

Debe mantenerse:

```text
Proposal Commit

↓

Domain Event

↓

Integration Mapping

↓

Integration Event
```

Los consumidores externos pueden procesar la información de forma
independiente.

La especificación correspondiente se encuentra en:

```text
DOMAIN-007K-Integration-Events.md
```

---

# Regla de Integraciones Externas

Proposal no debe esperar dentro de su comportamiento interno por
operaciones pertenecientes a:

```text
Municipal Systems

FIWARE

Notification Providers

Document Systems

Analytics Platforms

External APIs
```

como condición técnica de persistencia de su estado, salvo que una
regla de dominio explícita ya establecida determine una
precondición conceptual que deba resolverse antes de ejecutar el
Command.

La dependencia técnica del proveedor nunca forma parte del
Aggregate.

---

# Consistencia Eventual

Las vistas y consumidores externos pueden utilizar consistencia
eventual.

Puede existir:

```text
Proposal Commit

↓

Short Delay

↓

Read Model Updated
```

o:

```text
Proposal Commit

↓

Short Delay

↓

External Consumer Updated
```

Este retraso no modifica la consistencia interna del Aggregate.

---

# Regla de Fuente de Verdad

Una optimización de lectura no puede convertir una proyección en
fuente autoritativa del Write Model.

Debe mantenerse:

```text
Proposal Aggregate

=

Source of Domain Truth
```

y:

```text
Read Model

=

Derived View
```

Nunca:

```text
Read Model

=

Aggregate Replacement
```

---

# Caché

La infraestructura puede utilizar caché para optimizar lecturas.

Conceptualmente puede aplicarse sobre:

```text
ProposalSummary

ProposalDetail

ProposalDirectory

ProposalStatistics
```

La caché:

- no constituye fuente de verdad;
- puede invalidarse;
- puede reconstruirse;
- puede contener información temporalmente anterior;
- no modifica Proposal;
- no controla invariantes.

---

# Regla de Caché

No debe utilizarse una copia potencialmente obsoleta para
sobrescribir silenciosamente una revisión más reciente del
Aggregate.

Debe mantenerse:

```text
Cached Version

≠

Authoritative Write Version
```

El control de escritura permanece sujeto a Version.

---

# Invalidación de Caché

La estrategia concreta de invalidación pertenece a
Infrastructure.

Puede utilizar:

- expiración;
- eventos;
- invalidación explícita;
- reconstrucción;
- actualización de proyecciones.

La elección técnica no modifica el modelo de Proposal.

---

# Serialización

La serialización debe limitarse a la información necesaria para
cada contrato.

No debe serializarse automáticamente el Aggregate completo para:

- Commands;
- Domain Events;
- Integration Events;
- Read Models;
- APIs;
- mensajes externos.

Cada representación debe contener únicamente los datos necesarios
para su responsabilidad.

---

# Regla de Payload

Los contratos externos deben evitar Payloads innecesariamente
grandes.

Debe mantenerse:

```text
Required Contract Data

⊂

Complete Aggregate State
```

cuando el consumidor no necesite todo el estado.

Esta regla reduce:

- acoplamiento;
- volumen de transporte;
- exposición de datos;
- costo de serialización;
- dependencia contractual.

---

# Domain Events Compactos

Los Domain Events deben representar hechos del dominio con la
información necesaria para expresar dichos hechos.

No deben convertirse en copias completas del Aggregate por
conveniencia técnica.

Ejemplo:

```text
ProposalAccepted

ProposalId

OrganizationId

AcceptedAt

Version
```

puede expresar el hecho correspondiente sin transportar
información no relacionada.

La estructura exacta permanece definida por el contrato oficial de
eventos.

---

# Integration Events Compactos

Los Integration Events deben transportar únicamente la información
necesaria para el contrato externo.

No deben utilizarse como:

```text
Complete Proposal Snapshot
```

salvo que un contrato explícitamente definido requiera una
representación específica compatible con las reglas de
integración.

Debe preservarse el principio:

```text
Minimum Necessary Contract
```

---

# Read Models y Payload

Las vistas de lectura deben estar especializadas según la
necesidad del consumidor.

Una vista de listado no necesita necesariamente la misma
información que una vista detallada.

Ejemplo:

```text
ProposalSummary
```

puede ser menor que:

```text
ProposalDetail
```

Esto permite reducir transferencia y procesamiento innecesarios.

---

# Reconstrucción de Read Models

Las proyecciones deben poder reconstruirse desde sus fuentes
definidas.

La reconstrucción puede ejecutarse fuera del flujo normal de
Commands.

Debe mantenerse:

```text
Projection Rebuild

≠

Proposal Modification
```

Una reconstrucción intensiva no debe requerir modificar cada
Aggregate como parte del proceso de lectura.

---

# Reproyección

La reproyección puede procesar grandes cantidades de eventos o
información derivada.

Debe ejecutarse de manera que:

- no genere nuevos Domain Events de negocio;
- no incremente ProposalVersion;
- no ejecute Commands;
- no modifique el Aggregate;
- no produzca falsos hechos externos.

La optimización de la reproyección pertenece a Infrastructure.

---

# Event Replay

Cuando se utilice Event Sourcing, la reconstrucción del Aggregate
mediante replay debe aplicar únicamente la información necesaria
para restaurar su estado.

Durante replay no deben ejecutarse nuevamente efectos externos.

Debe mantenerse:

```text
Event Replay

≠

New Business Operation
```

---

# Regla de Replay

El replay debe evitar:

- enviar Notifications;
- publicar nuevamente Integration Events como hechos nuevos;
- ejecutar llamadas externas;
- modificar otros Aggregates;
- generar Commands nuevos por efecto automático del replay.

Su responsabilidad es reconstruir estado.

---

# Historial

Cuando exista historial de eventos, su tamaño no debe provocar la
incorporación de reglas técnicas dentro del Aggregate.

Las estrategias de optimización del historial pertenecen a la
arquitectura de persistencia.

El dominio únicamente requiere que la reconstrucción preserve:

- identidad;
- orden lógico;
- estado;
- invariantes aplicables;
- Version;
- semántica de eventos.

---

# Snapshots

Cuando una implementación compatible con Event Sourcing utilice
snapshots para reducir costos de reconstrucción, estos constituyen
una optimización de Infrastructure.

Un snapshot:

- no reemplaza la identidad;
- no redefine Version;
- no modifica la State Machine;
- no modifica eventos históricos;
- no constituye un nuevo hecho del dominio;
- no debe alterar el comportamiento reconstruido.

Debe mantenerse:

```text
Snapshot

=

Performance Optimization
```

y no:

```text
Snapshot

=

Domain Event
```

---

# Regla de Equivalencia de Reconstrucción

Si una implementación utiliza una optimización de reconstrucción,
el resultado debe ser conceptualmente equivalente al estado que se
obtendría aplicando la historia válida correspondiente.

Debe mantenerse:

```text
Optimized Reconstruction

=

Conceptually Equivalent Domain State
```

---

# Operaciones Idempotentes de Infraestructura

Los mecanismos externos que procesen eventos pueden implementar
idempotencia para evitar efectos duplicados.

La entrega repetida de:

```text
Same EventId
```

no representa un nuevo hecho del dominio.

La idempotencia del consumidor no debe requerir modificar el
Aggregate Proposal.

---

# Reintentos

Los reintentos técnicos pertenecen a Infrastructure o Application
cuando corresponda.

Un reintento de:

```text
Integration Delivery
```

no debe incrementar:

```text
ProposalVersion
```

si no existe una nueva modificación del Aggregate.

Debe mantenerse:

```text
Retry

≠

New Proposal Change
```

---

# Backpressure

Cuando consumidores externos procesen información más lentamente
que la producción de eventos, la infraestructura puede aplicar
mecanismos de control de carga.

Estos mecanismos no forman parte de Proposal.

Proposal no debe modificar sus invariantes para adaptarse a la
velocidad de consumidores externos.

Debe mantenerse:

```text
Consumer Throughput

≠

Domain Rule
```

---

# Batch Processing

Las operaciones de lectura, análisis, proyección o integración
pueden utilizar procesamiento por lotes cuando corresponda.

El procesamiento por lotes no debe convertir múltiples Proposal en
un único Aggregate.

Debe mantenerse:

```text
Batch of Proposals

≠

Proposal Aggregate
```

Cada Proposal conserva:

```text
ProposalId

Version

Lifecycle

Invariants

Consistency Boundary
```

propios.

---

# Bulk Commands

Una solicitud externa puede expresar una operación sobre múltiples
Proposal a nivel de Application.

Sin embargo, conceptualmente cada Aggregate debe proteger sus
propias reglas.

No debe asumirse:

```text
Bulk Operation

=

Single Proposal Transaction
```

Cada Proposal debe preservar:

- invariantes;
- estado;
- Version;
- Domain Events;
- resultado individual.

La coordinación masiva pertenece fuera del Aggregate.

---

# Regla de Fallo Parcial en Procesamiento Masivo

Cuando una operación de Application procese múltiples Proposal, el
fallo de una instancia no debe implicar que todas compartan
automáticamente un único límite de consistencia.

Debe mantenerse:

```text
Proposal A Result

Independent from

Proposal B Aggregate Consistency
```

salvo que una regla conceptual explícita de otro contexto defina
una coordinación superior.

---

# Estadísticas

Las estadísticas sobre Proposal deben obtenerse mediante Read
Models o proyecciones especializadas.

Ejemplos:

```text
Total Proposals

Draft Proposals

Submitted Proposals

Accepted Proposals

Rejected Proposals

Withdrawn Proposals

Proposals by Organization

Proposals by Territory

Proposals by Type
```

Estas estadísticas no deben calcularse cargando todos los
Aggregates de escritura cuando exista una proyección adecuada.

---

# Dashboards

Los dashboards deben consumir Read Models.

No deben consultar directamente múltiples Aggregate Roots para
construir vistas analíticas.

Debe mantenerse:

```text
Dashboard

↓

Read Models
```

y no:

```text
Dashboard

↓

Mass Aggregate Loading
```

---

# Analytics

Los procesos analíticos pertenecen al lado de lectura o a
sistemas especializados.

Analytics puede utilizar:

- proyecciones;
- datos agregados;
- Integration Events;
- información histórica autorizada.

No debe ejecutar comportamiento interno de Proposal para producir
métricas.

---

# Regla de Métricas

Las métricas técnicas de rendimiento no forman parte del estado de
Proposal.

Ejemplos:

```text
Request Latency

Database Latency

Cache Hit Rate

Queue Depth

CPU Usage

Memory Usage

Throughput
```

Estas métricas pertenecen a observabilidad e Infrastructure.

No deben agregarse al Aggregate como atributos del dominio.

---

# Métricas de Dominio

Una métrica que represente un concepto real del dominio puede
existir en una proyección o modelo correspondiente si ha sido
definida conceptualmente.

Debe distinguirse:

```text
Domain Metric
```

de:

```text
Technical Performance Metric
```

La similitud de representación numérica no convierte una métrica
técnica en concepto del dominio.

---

# Observabilidad

La observabilidad técnica puede medir el comportamiento de la
implementación sin modificar Proposal.

Puede registrar:

- latencia;
- errores;
- conflictos de concurrencia;
- tiempo de persistencia;
- tiempo de proyección;
- retraso de consumidores;
- volumen de Commands;
- volumen de eventos.

Estos datos no forman parte del estado interno del Aggregate.

---

# CorrelationId

CorrelationId puede utilizarse para seguir un flujo distribuido
sin introducir dependencias entre Aggregates.

Conceptualmente:

```text
Command

↓

Domain Event

↓

Integration Event

↓

External Consumer
```

puede mantener una correlación común.

La trazabilidad no exige mantener una transacción distribuida.

---

# CausationId

CausationId permite identificar la causa inmediata de un hecho
cuando corresponda.

Su utilización facilita observabilidad y trazabilidad sin
convertir la cadena causal completa en parte del Aggregate.

Debe mantenerse:

```text
CorrelationId

≠

CausationId
```

---

# Regla de Timestamps

Los timestamps de dominio deben representar hechos relevantes del
Lifecycle.

No deben incorporarse timestamps técnicos arbitrarios al
Aggregate únicamente para medir rendimiento.

Ejemplos de información temporal de dominio pueden incluir:

```text
CreatedAt

SubmittedAt

AcceptedAt

RejectedAt

WithdrawnAt

ArchivedAt
```

según las reglas oficiales del Aggregate.

Ejemplos técnicos como:

```text
DatabaseQueryStartedAt

CacheLookupFinishedAt

HTTPResponseSentAt
```

no pertenecen a Proposal.

---

# Operaciones Largas

Una operación que requiera trabajo externo prolongado no debe
mantener artificialmente abierto el límite transaccional de
Proposal.

Debe separarse:

```text
Domain Decision

↓

Commit

↓

External Processing
```

cuando el procesamiento externo no forme parte de una invariante
inmediata.

---

# Timeouts

Los timeouts técnicos pertenecen a Infrastructure.

Un timeout de:

```text
HTTP

Database

Queue

External API
```

no constituye por sí mismo un estado de Proposal.

Si una falla técnica impide confirmar una modificación, no debe
representarse falsamente como una transición completada.

---

# Disponibilidad de Sistemas Externos

La disponibilidad de sistemas externos no debe definir
directamente la validez interna de Proposal salvo que exista una
regla conceptual explícita ya establecida.

Ejemplo:

```text
FIWARE unavailable
```

no debe modificar automáticamente:

```text
ProposalStatus
```

La integración puede recuperarse independientemente.

---

# Escalabilidad Horizontal

Las implementaciones pueden escalar horizontalmente mientras
preserven:

- identidad;
- Version;
- consistencia;
- orden lógico requerido;
- Domain Events;
- idempotencia externa cuando corresponda.

El número de instancias de aplicación no forma parte del dominio.

---

# Stateless Application Services

Los Application Services pueden diseñarse sin estado técnico local
persistente cuando esto facilite escalabilidad.

Esta decisión no modifica Proposal.

El estado autoritativo del dominio permanece asociado al
Aggregate y a su mecanismo de persistencia correspondiente.

---

# Afinidad de Instancia

Proposal no debe depender conceptualmente de que todos sus
Commands sean procesados por una misma instancia física de
aplicación.

Debe mantenerse:

```text
Proposal Identity

≠

Application Instance Identity
```

La coordinación técnica necesaria pertenece a Infrastructure.

---

# Particionamiento

La infraestructura puede particionar almacenamiento o
procesamiento utilizando claves apropiadas.

Conceptualmente:

```text
ProposalId
```

puede actuar como una identidad útil para distribuir unidades de
trabajo.

La estrategia concreta de particionamiento no forma parte del
Aggregate.

---

# Regla de Particionamiento

El particionamiento no puede alterar:

- identidad;
- orden requerido de modificaciones;
- Version;
- consistencia;
- disponibilidad de invariantes internas.

Debe mantenerse:

```text
Partition Strategy

≠

Domain Boundary
```

Un shard, partición o nodo técnico no constituye un Bounded
Context ni un Aggregate.

---

# Consistencia y Rendimiento

La optimización de consistencia debe respetar la distinción entre:

```text
Strong Consistency

Inside Proposal
```

y:

```text
Eventual Consistency

Between Aggregates
```

No debe relajarse la consistencia interna de Proposal para obtener
mayor rendimiento.

No debe imponerse consistencia fuerte distribuida entre Aggregates
cuando el modelo no la requiere.

---

# Regla de Consistencia Interna

Dentro del Aggregate debe mantenerse:

```text
Atomic Domain Change
```

Una operación válida debe dejar Proposal completamente consistente.

No existe un estado conceptual permitido de:

```text
Half Submitted Proposal

Half Accepted Proposal

Half Archived Proposal
```

---

# Regla de Consistencia Externa

Las reacciones de otros Aggregates pueden ocurrir posteriormente.

Ejemplo:

```text
ProposalAccepted

↓

Commit Proposal

↓

Integration Event

↓

Voting Context reacts
```

Esto no convierte Voting en parte de Proposal.

---

# Hot Aggregates

Si una Proposal recibe un volumen elevado de modificaciones
concurrentes, no debe resolverse el problema ampliando su límite
de consistencia.

Las optimizaciones deben preservar:

```text
Single Proposal Identity

Single Proposal Version

Proposal Invariants
```

La infraestructura puede mejorar coordinación, procesamiento o
persistencia sin modificar el significado del Aggregate.

---

# Regla de No Fragmentación

El rendimiento no justifica dividir artificialmente Proposal en
múltiples Aggregates cuando los datos separados sean necesarios
para proteger una misma invariante inmediata ya definida.

Debe mantenerse el límite conceptual oficial.

La fragmentación solo puede producirse mediante una decisión de
dominio explícita y documentada, no como optimización técnica
accidental.

---

# Regla de No Fusión

El rendimiento tampoco justifica fusionar Proposal con otros
Aggregates para evitar llamadas o coordinación.

No debe ocurrir:

```text
Proposal + Assembly + Voting

↓

Single Aggregate
```

por razones exclusivamente técnicas.

Cada Aggregate mantiene su límite oficial.

---

# Evitar N+1 Conceptual

Las consultas que necesiten información de múltiples Proposals y
sus referencias externas deben resolverse mediante proyecciones
adecuadas.

No debe requerirse cargar repetidamente:

```text
Proposal

↓

Organization

↓

Territory

↓

Assembly
```

para cada fila de una vista de listado cuando el Read Model pueda
mantener la información necesaria.

Esta optimización pertenece al lado de lectura y no modifica los
límites DDD.

---

# Consultas Compuestas

Una vista puede combinar información derivada de múltiples
Bounded Contexts para lectura.

Ejemplo:

```text
ProposalId

ProposalTitle

OrganizationName

TerritoryName

AssemblyName

ProposalStatus
```

Esta composición pertenece a una proyección.

No representa un nuevo Aggregate.

---

# Límites de Datos

Proposal debe mantener únicamente datos necesarios para su
comportamiento e invariantes.

No debe almacenar copias completas de información externa para
evitar consultas.

Debe evitarse duplicar dentro del Aggregate:

- perfil completo del Citizen;
- información completa de Membership;
- estructura completa de Organization;
- geometría completa de Territory;
- estado completo de Assembly;
- información completa de Voting;
- contenido completo de Documents.

Las proyecciones pueden mantener datos derivados cuando sea útil
para lectura.

---

# Documentos

Si Proposal se relaciona con Documents, debe hacerlo mediante la
referencia establecida por el dominio.

El contenido documental potencialmente pesado no debe incorporarse
al estado interno de Proposal únicamente para evitar una consulta
externa.

Debe mantenerse:

```text
Proposal

↓

DocumentId
```

cuando corresponda al modelo.

No:

```text
Proposal

↓

Complete Binary Document
```

---

# Notificaciones

El envío de Notifications no forma parte de la transacción interna
de Proposal.

Un hecho como:

```text
ProposalSubmitted
```

puede originar posteriormente una Notification.

Proposal no debe esperar a que todos los canales de comunicación
confirmen entrega antes de considerar válido su propio cambio de
estado.

---

# Auditoría

La auditoría derivada no debe ampliar el Aggregate.

Proposal proporciona información de trazabilidad mediante:

```text
ProposalId

Version

Domain Events

Actor references

CorrelationId

CausationId

timestamps
```

cuando corresponda.

El almacenamiento y consulta de grandes historiales de auditoría
pertenecen al contexto correspondiente.

---

# Seguridad y Rendimiento

Una optimización de rendimiento no puede omitir controles de
seguridad requeridos.

Debe mantenerse:

```text
Performance

≠

Authorization Bypass
```

y:

```text
Performance

≠

Sensitive Data Exposure
```

La especificación completa de seguridad se documentará en:

```text
DOMAIN-007O-Security-Model.md
```

---

# Permisos y Rendimiento

La evaluación de permisos pertenece a la responsabilidad definida
en:

```text
DOMAIN-007F-Permissions.md
```

Una optimización puede mejorar técnicamente la evaluación de
autorización, pero no puede modificar quién posee una capacidad
según el modelo oficial.

Debe mantenerse:

```text
Permission Cache

≠

Permission Definition
```

---

# Invariantes y Rendimiento

Las invariantes definidas en:

```text
DOMAIN-007E-Invariants.md
```

son obligatorias independientemente del costo computacional.

No puede utilizarse una ruta rápida que omita una invariante.

Debe mantenerse:

```text
Fast Path

↓

Same Domain Validation
```

---

# State Machine y Rendimiento

Las transiciones definidas en:

```text
DOMAIN-007B-State-Machine.md
```

no pueden omitirse para reducir operaciones.

No está permitido convertir:

```text
Draft

↓

Submitted

↓

UnderReview

↓

Accepted
```

en una transición directa no definida únicamente para reducir
procesamiento.

La optimización no redefine el Lifecycle.

---

# Commands y Atajos Técnicos

No debe existir un Command técnico cuyo único propósito sea eludir
las reglas oficiales.

Ejemplo inválido:

```text
ForceProposalStatus
```

si permite establecer directamente cualquier estado.

Los Commands deben expresar intenciones válidas del dominio.

---

# Eventos y Atajos Técnicos

No debe generarse directamente un Domain Event para evitar
ejecutar el comportamiento del Aggregate.

No debe ocurrir:

```text
Publish ProposalAccepted

without

Valid AcceptProposal behavior
```

Los eventos representan hechos ocurridos.

No crean por sí mismos la validez de una operación.

---

# Performance Budget Conceptual

El dominio no establece valores físicos obligatorios de latencia,
CPU, memoria o throughput.

Estos valores dependen de:

- infraestructura;
- escala;
- carga;
- despliegue;
- hardware;
- base de datos;
- topología;
- requisitos operacionales.

Por lo tanto, este documento define reglas conceptuales de
rendimiento y no objetivos numéricos arbitrarios.

---

# Regla de Métricas Cuantitativas

Valores como:

```text
Response < 100 ms

1000 Commands per second

Cache Hit Rate > 90%

CPU < 70%
```

no deben incorporarse al modelo oficial de Proposal sin una
decisión arquitectónica u operacional explícita que los defina.

Este documento no introduce dichos valores por iniciativa propia.

---

# Performance Testing

Las pruebas de rendimiento deben verificar la implementación sin
alterar las reglas del dominio.

Pueden medir:

- carga de Aggregate;
- ejecución de Commands;
- persistencia;
- conflictos de Version;
- procesamiento de eventos;
- actualización de Read Models;
- consultas;
- reproyección;
- integración.

Los escenarios técnicos concretos pueden variar según
Infrastructure.

---

# Regla de Pruebas de Rendimiento

Una prueba de rendimiento no se considera válida si obtiene
mejores resultados mediante:

- desactivar invariantes;
- desactivar permisos;
- ignorar Version;
- evitar Domain Events obligatorios;
- utilizar estados inválidos;
- omitir persistencia requerida;
- reemplazar el Aggregate por un Read Model;
- eliminar controles definidos por el dominio.

La prueba debe medir una implementación conceptualmente correcta.

---

# Escenario de Rendimiento — Lectura Masiva

## Objetivo

Verificar que las consultas masivas no requieran cargar Aggregates
individuales cuando existen Read Models adecuados.

## Flujo conceptual

```text
Query

↓

Proposal Read Model

↓

Paginated Result
```

No:

```text
Query

↓

Load N Proposal Aggregates

↓

Build Listing
```

cuando no existe necesidad de comportamiento de dominio.

---

# Escenario de Rendimiento — Escritura Individual

## Objetivo

Verificar que un Command dirigido a una Proposal modifique
únicamente dicha unidad de consistencia.

## Flujo conceptual

```text
Command

↓

Load Proposal

↓

Validate

↓

Apply Behavior

↓

Increment Version

↓

Persist

↓

Domain Event
```

No debe requerirse cargar todos los Proposals de una Organization.

---

# Escenario de Rendimiento — Proyección

## Objetivo

Verificar que la actualización del Read Model permanezca separada
del comportamiento interno de Proposal.

## Flujo conceptual

```text
Proposal Domain Event

↓

Projection

↓

Read Model Update
```

La proyección no debe bloquear conceptualmente el Aggregate como
parte de su consistencia interna.

---

# Escenario de Rendimiento — Integración

## Objetivo

Verificar que una integración lenta no amplíe la transacción de
Proposal.

## Flujo conceptual

```text
Proposal Change

↓

Commit

↓

Integration Event

↓

External Consumer
```

Una falla o lentitud del consumidor no debe convertir la
integración en parte del Aggregate.

---

# Escenario de Rendimiento — Concurrencia

## Objetivo

Verificar que múltiples intentos concurrentes sobre una misma
Proposal respeten Version.

## Given

```text
ProposalVersion = N
```

Dos operaciones utilizan:

```text
ExpectedVersion = N
```

## When

Una operación confirma primero la nueva revisión.

## Then

La segunda debe detectar el conflicto correspondiente.

No debe obtenerse rendimiento mediante:

```text
Last Write Wins
```

si ello produce pérdida silenciosa de modificaciones.

---

# Escenario de Rendimiento — Reproyección

## Objetivo

Verificar que una reconstrucción de Read Models no modifique el
Write Model.

## Flujo conceptual

```text
Historical Events

↓

Projection Engine

↓

Read Models
```

Debe mantenerse:

```text
ProposalVersion unchanged
```

---

# Escenario de Rendimiento — Consumidor Lento

## Objetivo

Verificar que la velocidad de un consumidor externo no determine
la velocidad transaccional interna del Aggregate cuando no existe
una dependencia de dominio inmediata.

## Given

Un Integration Event confirmado.

## When

El consumidor procesa lentamente.

## Then

Proposal permanece en su estado confirmado.

No se extiende su transacción.

---

# Escenario de Rendimiento — Caché Obsoleta

## Objetivo

Verificar que una optimización de lectura no provoque pérdida de
actualizaciones.

## Given

```text
Cached ProposalVersion = 5

Persisted ProposalVersion = 6
```

## When

Una operación intenta utilizar la revisión antigua para escribir.

## Then

Debe aplicarse el control de concurrencia correspondiente.

La caché no puede sobrescribir silenciosamente la revisión 6.

---

# Escenario de Rendimiento — Procesamiento Masivo

## Objetivo

Verificar que procesar múltiples Proposal no fusione sus límites
de consistencia.

## Given

```text
Proposal A

Proposal B

Proposal C
```

## When

Una operación de Application procesa las tres.

## Then

Cada una conserva:

```text
ProposalId

Version

State

Invariants

Domain Events
```

propios.

---

# Escenario de Rendimiento — Integración FIWARE

## Objetivo

Verificar que la interoperabilidad con sistemas Smart City no
introduzca dependencias técnicas dentro del Aggregate.

## Given

Un hecho de Proposal requiere interoperabilidad externa.

## When

Se publica la información correspondiente.

## Then

Debe mantenerse:

```text
Proposal

↓

Domain Event

↓

Integration Event

↓

Adapter

↓

External Platform
```

Proposal no debe conocer los detalles técnicos del consumidor.

---

# Reglas de Optimización Permitidas

La implementación puede optimizar mediante:

- índices;
- cachés;
- paginación;
- proyecciones;
- procesamiento asíncrono;
- procesamiento por lotes;
- particionamiento;
- escalamiento horizontal;
- serialización eficiente;
- reducción de Payload;
- almacenamiento especializado de lectura;
- reconstrucción optimizada;
- snapshots cuando corresponda;
- idempotencia de consumidores;
- reintentos técnicos;
- mecanismos de backpressure.

Estas optimizaciones son válidas únicamente si preservan el modelo
conceptual.

---

# Optimizaciones No Permitidas

No está permitido optimizar mediante:

- eliminar invariantes;
- modificar State Machine;
- modificar Lifecycle;
- eliminar Version;
- aceptar lost updates;
- modificar estado directamente;
- modificar Repository evitando Aggregate Root;
- almacenar otros Aggregates dentro de Proposal;
- crear transacciones distribuidas por conveniencia;
- convertir Read Models en fuente de escritura;
- publicar Integration Events antes del Commit;
- omitir Domain Events requeridos;
- mezclar autenticación con dominio;
- exponer información innecesaria;
- depender directamente de infraestructura externa;
- introducir estados técnicos dentro de Proposal;
- fusionar Aggregates por rendimiento;
- fragmentar el Aggregate rompiendo invariantes.

---

# Evolución

Las optimizaciones futuras deben poder incorporarse sin modificar
el significado del Aggregate.

Una nueva técnica puede reemplazar:

```text
Database

Cache

Message Broker

Projection Store

Search Engine

Deployment Model
```

sin alterar:

```text
ProposalId

ProposalStatus

ProposalType

Lifecycle

State Machine

Commands

Domain Events

Invariants

Version

Consistency Boundary
```

---

# Regla de Evolución

Toda optimización futura debe responder conceptualmente a:

```text
Does this change domain behavior?
```

Si la respuesta es:

```text
No
```

puede pertenecer a Infrastructure o Application.

Si la respuesta es:

```text
Yes
```

no constituye una simple optimización y requiere una decisión de
dominio explícita y documentada.

---

# Extension Points de Rendimiento

Las futuras implementaciones pueden incorporar nuevas estrategias
de rendimiento sin modificar Proposal.

Ejemplos:

```text
New Cache Strategy

New Search Engine

New Projection Store

New Partition Strategy

New Event Transport

New Persistence Engine

New Scaling Strategy
```

Estas extensiones deben respetar:

```text
DOMAIN-007P-Extension-Points.md
```

cuando corresponda.

---

# Validación mediante Test Scenarios

Las Performance Rules deben poder verificarse mediante escenarios
conceptuales definidos en:

```text
DOMAIN-007M-Test-Scenarios.md
```

Los escenarios deben comprobar especialmente:

- ausencia de modificaciones parciales;
- preservación de Version;
- independencia entre Aggregates;
- separación Write/Read;
- separación entre Commit e integración;
- comportamiento correcto ante concurrencia;
- independencia de Infrastructure;
- ausencia de efectos externos durante replay;
- preservación de invariantes durante optimizaciones.

---

# Compatibilidad con CQRS

Las reglas de rendimiento aprovechan la separación:

```text
Write Side

Proposal Aggregate
```

y:

```text
Read Side

Proposal Read Models
```

Cada lado puede optimizarse según su responsabilidad sin modificar
el otro.

---

# Compatibilidad con Event Sourcing

Cuando Proposal utilice Event Sourcing, las optimizaciones pueden
incluir:

- replay eficiente;
- snapshots;
- proyecciones especializadas;
- procesamiento incremental;
- particionamiento de streams;
- consumidores independientes.

Estas técnicas no modifican la semántica de los Domain Events ni
las invariantes del Aggregate.

---

# Compatibilidad con Event-Driven Architecture

Los eventos permiten separar la transacción de Proposal de
procesos secundarios.

Conceptualmente:

```text
Proposal

↓

Domain Event

↓

Commit

↓

Integration / Projection / Audit / Notification
```

Esta separación reduce acoplamiento y evita ampliar
innecesariamente el límite transaccional.

---

# Compatibilidad con Clean Architecture

Las decisiones de rendimiento dependientes de tecnología deben
permanecer en capas externas.

El dominio no depende de:

```text
Database Engine

Cache Engine

Message Broker

Search Engine

HTTP Server

Cloud Provider
```

Las dependencias apuntan hacia el dominio y no desde el dominio
hacia Infrastructure.

---

# Compatibilidad con Arquitectura Hexagonal

Los mecanismos técnicos utilizados para optimizar Proposal se
conectan mediante Ports y Adapters cuando corresponda.

Ejemplos:

```text
Repository Port

↓

Persistence Adapter
```

```text
Integration Port

↓

Messaging Adapter
```

```text
Query Port

↓

Read Model Adapter
```

Los Adapters pueden cambiar sin redefinir Proposal.

---

# Principios Arquitectónicos

Las Performance Rules mantienen:

```text
Performance

≠

Domain Correctness
```

```text
Optimization

≠

Invariant Bypass
```

```text
Optimization

≠

State Machine Bypass
```

```text
Optimization

≠

Authorization Bypass
```

```text
Write Model

≠

Read Model
```

```text
Read Model

≠

Source of Truth
```

```text
Cache

≠

Source of Truth
```

```text
Database Index

≠

Domain Rule
```

```text
Snapshot

≠

Domain Event
```

```text
Retry

≠

New Domain Change
```

```text
Replay

≠

New Business Operation
```

```text
Batch

≠

Aggregate
```

```text
Partition

≠

Domain Boundary
```

```text
External Consumer

≠

Aggregate Dependency
```

```text
External Aggregate Reference

≠

Aggregate Membership
```

```text
Infrastructure Scaling

≠

Domain Evolution
```

```text
Technical Metric

≠

Domain State
```

---

# Restricciones

No está permitido:

- sacrificar invariantes para reducir latencia;
- omitir Version para aumentar throughput;
- utilizar Read Models para escribir Proposal;
- cargar Aggregates externos como parte de Proposal por
  conveniencia;
- fusionar Aggregates por razones de rendimiento;
- fragmentar Proposal rompiendo su consistencia;
- publicar hechos externos antes de confirmar el estado;
- ejecutar efectos externos durante replay;
- utilizar caché como autoridad de escritura;
- permitir lost updates;
- introducir dependencias de infraestructura dentro del dominio;
- incorporar métricas técnicas al estado de Proposal;
- convertir índices en reglas de negocio;
- convertir snapshots en hechos del dominio;
- utilizar procesamiento masivo como una única transacción de
  múltiples Aggregates;
- modificar el Lifecycle para reducir operaciones;
- crear Commands técnicos que permitan saltarse comportamiento de
  dominio.

---

# Documentación Complementaria

Las Performance Rules deben interpretarse conjuntamente con:

```text
DOMAIN-007-Aggregate.md

DOMAIN-007A-Lifecycle.md

DOMAIN-007B-State-Machine.md

DOMAIN-007C-Commands.md

DOMAIN-007D-Domain-Events.md

DOMAIN-007E-Invariants.md

DOMAIN-007F-Permissions.md

DOMAIN-007G-Repository-Contract.md

DOMAIN-007H-Examples.md

DOMAIN-007I-Versioning.md

DOMAIN-007J-Consistency-Boundary.md

DOMAIN-007K-Integration-Events.md

DOMAIN-007L-Read-Model.md

DOMAIN-007M-Test-Scenarios.md

DOMAIN-007O-Security-Model.md

DOMAIN-007P-Extension-Points.md
```

Estos documentos constituyen conjuntamente la definición
conceptual del Aggregate Proposal.

Las Performance Rules no sustituyen ninguna regla del Aggregate.

Definen cómo preservar su eficiencia y capacidad de escalamiento
sin alterar las decisiones conceptuales ya establecidas.

---

# Definición de Éxito

Las Performance Rules del Aggregate **Proposal** garantizan que
las implementaciones puedan evolucionar hacia mayores niveles de
carga, concurrencia, volumen de consultas e interoperabilidad sin
sacrificar las reglas fundamentales del dominio.

El modelo de rendimiento preserva:

```text
Proposal Identity

Lifecycle

State Machine

Commands

Domain Events

Invariants

Permissions

Versioning

Consistency Boundary

Integration Contracts

Read Models

Aggregate Independence
```

El rendimiento se obtiene mediante:

- Aggregates acotados;
- referencias por identidad;
- separación Write/Read;
- Read Models especializados;
- consistencia eventual entre Aggregates;
- versionado optimista;
- procesamiento desacoplado;
- Integration Events;
- cachés de lectura;
- índices;
- paginación;
- proyecciones;
- procesamiento por lotes fuera del Aggregate;
- escalamiento de Infrastructure;
- optimización de serialización;
- reconstrucción eficiente cuando corresponda.

Ninguna optimización puede redefinir las invariantes, alterar el
Lifecycle, modificar la State Machine, ampliar el Consistency
Boundary o convertir decisiones de Infrastructure en reglas del
dominio.

De esta forma, `DOMAIN-007N-Performance-Rules.md` establece el
modelo conceptual oficial para preservar el rendimiento del
Aggregate **Proposal**, manteniendo simultáneamente consistencia,
escalabilidad, independencia tecnológica, trazabilidad y fidelidad
al diseño DDD consolidado de AURA Core.