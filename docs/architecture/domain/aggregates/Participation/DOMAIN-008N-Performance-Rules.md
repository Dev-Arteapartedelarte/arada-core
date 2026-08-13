````markdown


# DOMAIN-008N — Participation Performance Rules

Versión: 1.0

Estado:
Oficial

Proyecto:
AURA Core

Bounded Context:
Participation Management

Aggregate:
Participation

Autor:
ARADA

Documentos Relacionados:

- DOMAIN-008-Aggregate.md
- DOMAIN-008G-Repository-Contract.md
- DOMAIN-008I-Versioning.md
- DOMAIN-008J-Consistency-Boundary.md
- DOMAIN-008L-Read-Model.md
- DOMAIN-008M-Test-Scenarios.md
- CORE-011-Repository-Contracts.md
- CORE-016-Dependency-Rules.md

---

# Objetivo

Definir las reglas oficiales de rendimiento aplicables al
Aggregate **Participation**.

Estas reglas establecen cómo deben preservarse las
características de rendimiento del sistema sin comprometer:

- las Invariants;
- el Consistency Boundary;
- el Versioning;
- la atomicidad;
- el comportamiento del Aggregate Root;
- la separación entre Write Model y Read Model;
- la independencia entre Aggregates.

Las optimizaciones de rendimiento no pueden modificar las
reglas conceptuales del dominio.

---

# Principios

Las reglas de rendimiento deben cumplir los siguientes
principios.

- el rendimiento no puede justificar la violación de
  Invariants;
- las optimizaciones no pueden evitar el Aggregate Root;
- las optimizaciones no pueden eliminar el control de
  Version;
- las optimizaciones no pueden ampliar el Consistency
  Boundary;
- las consultas masivas deben resolverse mediante Read
  Models cuando corresponda;
- el Repository debe mantenerse orientado al Aggregate;
- las referencias hacia otros Aggregates deben mantenerse
  mediante identificadores;
- la persistencia debe conservar atomicidad;
- las optimizaciones técnicas pertenecen a Infrastructure;
- el dominio permanece independiente de tecnologías
  concretas.

---

# Regla Fundamental

Debe mantenerse:

```text
Performance Optimization

≠

Domain Rule Bypass
```

Toda optimización debe preservar:

```text
Participation Aggregate

↓

Invariants

↓

Versioning

↓

Consistency Boundary

↓

Valid Persistence
```

---

# Aggregate Root

Participation continúa siendo la única puerta de entrada
para modificar el estado del Aggregate.

No está permitido utilizar una optimización que permita:

```text
Direct State Mutation

↓

Persistence
```

evitando:

```text
Participation Aggregate Root
```

El rendimiento no modifica la autoridad del Aggregate.

---

# Consistency Boundary

Participation constituye una única unidad de
consistencia.

Las optimizaciones deben respetar:

```text
One Participation

↓

One Consistency Boundary
```

No debe combinarse el estado de múltiples Aggregates en
una única unidad de consistencia únicamente por razones de
rendimiento.

---

# Atomicidad

Toda modificación válida debe conservar atomicidad.

Conceptualmente:

```text
Load Participation

↓

Execute Domain Behavior

↓

Validate Invariants

↓

Increment Version

↓

Persist
```

No puede dividirse una modificación requerida por el
Aggregate en escrituras independientes que permitan
observar estados parciales inválidos.

---

# Versioning

Las optimizaciones no pueden eliminar el control de
concurrencia basado en Version.

Debe mantenerse:

```text
ExpectedVersion

=

PersistedVersion
```

antes de confirmar una modificación.

No debe utilizarse:

```text
Performance Optimization

↓

Skip Version Check
```

---

# Concurrencia Optimista

El control de concurrencia optimista debe preservarse
incluso cuando Infrastructure utilice mecanismos
especializados para mejorar rendimiento.

Escenario.

```text
Participation

Version 12
```

Proceso A confirma:

```text
Version 13
```

Proceso B intenta persistir utilizando:

```text
ExpectedVersion = 12
```

Resultado.

```text
ConcurrencyConflictError
```

Una optimización no puede convertir este conflicto en una
sobrescritura silenciosa.

---

# Repository

El Repository permanece orientado a la recuperación y
persistencia del Aggregate.

Debe mantenerse:

```text
ParticipationRepository

↓

Participation Aggregate
```

El Repository no debe convertirse en un mecanismo general
de consulta masiva para resolver necesidades de
presentación.

---

# Recuperación del Aggregate

Cuando un caso de uso requiere comportamiento del dominio,
debe recuperarse la Participation correspondiente.

Conceptualmente:

```text
ParticipationId

↓

Repository

↓

Participation
```

No es necesario recuperar Aggregates no involucrados en la
operación.

---

# Recuperación Mínima

Una operación debe recuperar únicamente la información
necesaria para reconstruir correctamente el Aggregate.

La optimización no puede producir una Participation
parcial incapaz de proteger sus Invariants.

Debe mantenerse:

```text
Required Aggregate State

↓

Complete Valid Domain Behavior
```

No:

```text
Incomplete Aggregate State

↓

Assumed Valid Behavior
```

---

# No Partial Aggregate

Una representación parcial utilizada para escritura no
puede sustituir el Aggregate cuando omita estado necesario
para validar sus reglas.

Si una operación requiere:

```text
ParticipationStatus

Version

Context
```

estos elementos deben encontrarse disponibles de forma
coherente para ejecutar el comportamiento correspondiente.

---

# Consultas

Las consultas no deben cargar el Aggregate cuando no
requieren comportamiento de dominio.

Debe mantenerse:

```text
Query

↓

Read Model
```

cuando el propósito sea:

- listado;
- búsqueda;
- filtros;
- paginación;
- estadísticas;
- dashboards;
- análisis;
- visualización.

---

# Read Models

Los Read Models constituyen el mecanismo oficial para
optimizar consultas.

```text
Domain Events

↓

Projection

↓

Participation Read Models
```

Las proyecciones pueden optimizarse para:

- búsquedas;
- filtros;
- ordenamiento;
- agregaciones;
- paginación;
- estadísticas.

Estas optimizaciones no afectan el Write Model.

---

# Separación Write / Read

Debe mantenerse:

```text
Write Side

Participation Aggregate
```

```text
Read Side

Participation Read Models
```

Una necesidad de rendimiento en consultas no justifica
agregar consultas analíticas al Aggregate.

---

# Listados

Los listados de Participations deben resolverse mediante
Read Models cuando su finalidad sea consulta.

Ejemplo:

```text
Participations by Organization
```

debe resolverse desde una proyección optimizada.

No mediante la carga de todos los Aggregates del Write
Side.

---

# Búsquedas

Las búsquedas por:

```text
CitizenId

OrganizationId

AssemblyId

ProposalId

ParticipationType

ParticipationStatus
```

pueden resolverse mediante Read Models especializados.

El Repository del Aggregate no debe transformarse en un
motor de búsqueda.

---

# Paginación

La paginación pertenece principalmente al Read Side.

Conceptualmente:

```text
Query

↓

Participation Read Model

↓

Paginated Result
```

La paginación no modifica el Aggregate.

---

# Ordenamiento

El ordenamiento de resultados pertenece al modelo de
lectura.

Puede realizarse por criterios proyectados como:

```text
CreatedAt

UpdatedAt

ParticipationType

ParticipationStatus
```

cuando dichos datos existan en la proyección
correspondiente.

---

# Filtros

Los filtros de consulta deben resolverse sin incorporar
lógica de negocio al Read Model.

Ejemplo.

```text
Filter by ParticipationStatus
```

es una operación de lectura.

No modifica el Lifecycle ni las Invariants.

---

# Agregaciones

Las agregaciones estadísticas pertenecen al Read Side.

Ejemplos.

```text
Total Participations

Active Participations

Completed Participations

Participations by Organization

Participations by Assembly
```

Estas operaciones no requieren cargar todos los
Aggregates para ejecutar comportamiento de dominio.

---

# Dashboards

Los dashboards deben utilizar proyecciones optimizadas.

No debe emplearse como patrón normal:

```text
Load Many Participation Aggregates

↓

Build Dashboard
```

Debe utilizarse:

```text
Participation Read Models

↓

Dashboard
```

---

# Analytics

Las operaciones analíticas permanecen fuera del
Aggregate.

Conceptualmente:

```text
Read Models

↓

Analytics
```

No:

```text
Participation Aggregate

↓

Analytics Engine
```

---

# Proyecciones Desnormalizadas

Los Read Models pueden utilizar información desnormalizada
cuando sea necesario para optimizar consultas.

Esto no modifica el Consistency Boundary del Write Model.

Debe mantenerse:

```text
Read Model Denormalization

≠

Aggregate Expansion
```

---

# Consistencia Eventual

Las proyecciones pueden actualizarse mediante consistencia
eventual.

```text
Participation

↓

Commit

↓

Domain Event

↓

Projection

↓

Read Model
```

Puede existir un intervalo entre la confirmación del
Aggregate y la actualización de una proyección.

Esta condición no representa una inconsistencia interna de
Participation.

---

# Cache

Infrastructure puede utilizar mecanismos de caché para
mejorar rendimiento.

La caché no modifica el modelo conceptual.

Debe mantenerse:

```text
Cache

≠

Aggregate Source of Truth
```

---

# Cache de Read Models

Los Read Models pueden utilizar caché cuando corresponda.

La caché debe considerarse una representación derivada.

Puede invalidarse o reconstruirse sin modificar el
Aggregate.

---

# Cache del Write Side

Cuando Infrastructure utilice caché para recuperación del
Aggregate, debe preservar:

- ParticipationId;
- estado actual;
- Version;
- coherencia necesaria para operaciones de escritura.

No puede utilizarse un estado obsoleto para evitar el
control de concurrencia.

---

# Datos Obsoletos

Una optimización que utilice información potencialmente
obsoleta no puede reemplazar la validación de Version.

Debe mantenerse:

```text
Cached Version

↓

Repository Version Check

↓

Persist or Conflict
```

---

# Referencias Externas

Participation mantiene referencias mediante
identificadores.

Ejemplos.

```text
OrganizationId

CitizenId

MembershipId

AssemblyId

ProposalId

TerritoryId
```

No debe cargarse automáticamente el Aggregate completo
referenciado si no es necesario para el caso de uso.

---

# No Eager Loading de Aggregates Externos

No debe utilizarse como regla conceptual:

```text
Load Participation

↓

Automatically Load Organization

Citizen

Membership

Assembly

Proposal

Territory
```

La relación mediante identificadores permite evitar
acoplamiento y cargas innecesarias.

---

# No Lazy Loading de Aggregates Mutables

Tampoco debe introducirse:

```text
Participation.Assembly

↓

Lazy Loaded Mutable Assembly
```

como mecanismo para navegar y modificar otro Aggregate.

Debe mantenerse:

```text
Participation.AssemblyId
```

---

# Coordinación entre Aggregates

Cuando un caso de uso requiera información externa, la
Application Layer puede coordinar la obtención del contexto
necesario.

Conceptualmente:

```text
Application

↓

Required External Context

↓

Participation Command
```

Esto no amplía el Aggregate.

---

# Operaciones Masivas

Las operaciones masivas pueden optimizarse técnicamente,
pero cada Participation conserva:

```text
Own Identity

Own Version

Own Invariants

Own Consistency Boundary
```

Una operación masiva no convierte múltiples
Participations en un único Aggregate.

---

# Validación Individual

Cada Participation incluida en una operación masiva debe
mantener sus propias validaciones.

Conceptualmente:

```text
Bulk Operation

↓

PAR-A Validation

PAR-B Validation

PAR-C Validation
```

No debe utilizarse una validación global como sustituto de
las Invariants individuales.

---

# Conflictos Parciales

Una operación masiva puede producir resultados
independientes.

Ejemplo.

```text
PAR-A

Persisted
```

```text
PAR-B

ConcurrencyConflictError
```

```text
PAR-C

Rejected
```

Cada resultado pertenece al Aggregate correspondiente.

---

# Bulk Update

No debe utilizarse un Bulk Update para modificar
directamente estado protegido.

No está permitido conceptualmente:

```text
UPDATE all Participation

SET Status = Archived
```

evitando:

- Commands;
- Lifecycle;
- State Machine;
- Invariants;
- Permissions;
- Versioning.

---

# Persistencia por Lotes

Infrastructure puede optimizar físicamente operaciones de
persistencia por lotes cuando preserve completamente la
semántica individual de cada Aggregate.

Cada Participation continúa manteniendo:

```text
Independent Version

Independent Result

Independent Consistency Boundary
```

---

# Domain Events

Las optimizaciones no pueden eliminar Domain Events
requeridos por modificaciones válidas.

Debe mantenerse:

```text
Valid Domain Modification

↓

Domain Event
```

cuando el modelo correspondiente establezca dicho evento.

---

# Eventos y Rendimiento

La generación de Domain Events no debe sustituirse por
actualizaciones directas únicamente para reducir costo
operacional.

Los eventos representan hechos del dominio.

No son una optimización opcional cuando forman parte del
modelo oficial.

---

# Integration Events

La publicación externa puede realizarse de forma
asíncrona.

Debe mantenerse:

```text
Participation Commit

↓

Integration Process
```

La latencia de publicación externa no debe extender
innecesariamente el Consistency Boundary del Aggregate.

---

# Outbox

Cuando el patrón Outbox consolidado sea utilizado, permite
desacoplar:

```text
Aggregate Commit
```

de:

```text
External Publication
```

La publicación posterior puede optimizarse sin ejecutar
nuevamente el comportamiento del Aggregate.

---

# Reintentos

Los reintentos técnicos pueden utilizarse cuando
corresponda.

No pueden ignorar:

```text
ConcurrencyConflictError
```

Un conflicto de Version requiere reevaluar el estado
actual.

---

# Reintento por Concurrencia

Debe mantenerse:

```text
ConcurrencyConflictError

↓

Reload Participation

↓

Reevaluate Command
```

No:

```text
ConcurrencyConflictError

↓

Force Save
```

---

# Rehidratación

La rehidratación puede optimizarse técnicamente.

Sin embargo:

- no incrementa Version;
- no genera nuevos Domain Events;
- no ejecuta Commands;
- no modifica timestamps;
- no reevalúa Permissions.

---

# Event Sourcing Compatible

Cuando se utilice Event Sourcing, la reconstrucción puede
optimizarse sin cambiar las reglas del Aggregate.

Conceptualmente:

```text
Historical Events

↓

Rehydrate Participation
```

La estrategia técnica pertenece a Infrastructure.

---

# Snapshots

Si una implementación compatible con Event Sourcing
utiliza Snapshots, estos constituyen una optimización de
reconstrucción.

Un Snapshot no modifica:

- ParticipationId;
- Version;
- Lifecycle;
- State Machine;
- Invariants;
- Domain Events.

---

# Snapshot no es Nueva Version

Crear un Snapshot no constituye una nueva modificación del
Aggregate.

Por lo tanto:

```text
Snapshot Creation

↓

No Version Increment
```

---

# Índices

Infrastructure puede utilizar índices para optimizar:

- búsqueda;
- recuperación;
- filtrado;
- ordenamiento;
- acceso por identificadores.

Los índices no forman parte del dominio.

---

# Índices de Write Side

Los índices utilizados para recuperar Participation deben
optimizar acceso sin modificar la semántica del
Repository.

Ejemplo conceptual.

```text
ParticipationId

↓

Efficient Lookup
```

La tecnología concreta pertenece a Infrastructure.

---

# Índices de Read Side

Las proyecciones pueden mantener índices especializados
para consultas.

Ejemplos conceptuales.

```text
OrganizationId

CitizenId

AssemblyId

ProposalId

ParticipationStatus

ParticipationType
```

Esto no modifica el Aggregate.

---

# Persistencia Relacional

Una implementación relacional puede optimizar mediante:

- índices;
- planes de consulta;
- transacciones;
- particionamiento;
- mecanismos propios del motor.

Estas decisiones pertenecen a Infrastructure.

No modifican el modelo conceptual de Participation.

---

# Persistencia Documental

Una implementación documental puede optimizar mediante:

- índices;
- distribución;
- mecanismos de consulta;
- estrategias propias del motor.

La estructura física no redefine el Aggregate Boundary.

---

# Independencia Tecnológica

Las reglas de rendimiento no dependen de:

```text
PostgreSQL

MongoDB

Redis

Elasticsearch

OpenSearch

SQLAlchemy

Django ORM

Kafka

RabbitMQ
```

Estas tecnologías pueden implementar optimizaciones.

No definen las reglas del dominio.

---

# Latencia

La arquitectura puede optimizar la latencia de operaciones.

Sin embargo, reducir latencia no autoriza:

- omitir Invariants;
- omitir Permissions;
- omitir Versioning;
- evitar Domain Events;
- persistir parcialmente el Aggregate;
- modificar otros Aggregates directamente.

---

# Throughput

El sistema puede aumentar el throughput procesando
múltiples Participations de forma independiente.

Debe mantenerse:

```text
Higher Throughput

↓

Independent Aggregate Processing
```

No:

```text
Higher Throughput

↓

Shared Mutable Aggregate State
```

---

# Paralelismo

Participations diferentes pueden procesarse
independientemente.

Ejemplo.

```text
PAR-001

PAR-002

PAR-003
```

pueden evolucionar en paralelo porque poseen:

```text
Independent Identity

Independent Version

Independent Consistency Boundary
```

---

# Paralelismo sobre la misma Participation

Las operaciones concurrentes sobre la misma Participation
están sujetas al control de Version.

No debe suponerse que el paralelismo elimina la necesidad
de coordinación optimista.

---

# Contención

El modelo de Aggregate pequeño y referencias por
identificador permite reducir la necesidad de coordinar
estado mutable externo.

Debe mantenerse la independencia entre Aggregates para
evitar ampliar innecesariamente el área de contención.

---

# Transacciones Distribuidas

No deben introducirse transacciones distribuidas entre
Aggregates como optimización de rendimiento.

Debe mantenerse:

```text
Participation

↓

Own Transaction Boundary
```

La coordinación externa utiliza los mecanismos definidos
por la arquitectura.

---

# Performance y Permissions

Las evaluaciones de autorización no pueden eliminarse para
mejorar rendimiento.

Debe mantenerse:

```text
Authorization Required

↓

Permission Evaluation
```

cuando corresponda.

Una optimización puede mejorar la ejecución técnica, pero
no eliminar la regla.

---

# Performance e Invariants

Todas las Invariants permanecen obligatorias.

No debe utilizarse:

```text
Fast Path

↓

Skip Invariants
```

Toda ruta de modificación debe producir un estado válido.

---

# Performance y State Machine

No puede existir una ruta rápida que evite la State
Machine.

Debe mantenerse:

```text
Command

↓

Valid State Transition

↓

Modification
```

independientemente del origen técnico de la operación.

---

# Performance y Lifecycle

Las optimizaciones no pueden introducir transiciones
abreviadas.

Ejemplo inválido.

```text
Registered

↓

Performance Optimization

↓

Completed
```

si la State Machine no permite esa transición.

---

# Performance y Read Models

Las necesidades de lectura intensiva deben resolverse
mediante proyecciones especializadas.

Debe mantenerse:

```text
High Read Load

↓

Read Models
```

No:

```text
High Read Load

↓

Repeated Aggregate Reconstruction
```

como mecanismo normal de consulta.

---

# Reconstrucción de Read Models

Los Read Models pueden reconstruirse de manera
independiente del Write Side.

La reconstrucción no modifica Participation.

Puede optimizarse técnicamente sin afectar las reglas del
Aggregate.

---

# Proyecciones Especializadas

Pueden existir múltiples proyecciones optimizadas para
distintos patrones de consulta según el modelo ya definido.

La existencia de múltiples vistas no implica múltiples
fuentes de verdad.

Debe mantenerse:

```text
One Write Model

↓

Multiple Read Models
```

---

# Fuente de Verdad

El Write Model permanece como fuente oficial del estado
del Aggregate.

Las optimizaciones de lectura no pueden convertir una
proyección, caché o índice en autoridad de escritura.

---

# Observabilidad

Infrastructure puede medir operaciones relacionadas con
Participation.

Ejemplos.

```text
Repository Load Duration

Repository Save Duration

Projection Lag

Concurrency Conflict Rate
```

Estas métricas no forman parte del Aggregate.

---

# Métricas

Las métricas de rendimiento pueden utilizarse para
detectar:

- latencia elevada;
- consultas costosas;
- retraso de proyecciones;
- contención;
- conflictos concurrentes;
- fallos operacionales.

La observabilidad no modifica el dominio.

---

# Logging

El Logging pertenece a Infrastructure.

Participation no depende de un sistema de logging para
proteger sus Invariants.

---

# Tracing

El Tracing puede utilizarse para observar flujos
distribuidos.

Puede correlacionarse mediante mecanismos ya establecidos
como:

```text
CorrelationId
```

cuando corresponda.

Tracing no forma parte del estado interno de
Participation.

---

# Rendimiento y Seguridad

Las optimizaciones no pueden debilitar las reglas de
seguridad.

No debe existir:

```text
Performance Shortcut

↓

Authorization Bypass
```

ni:

```text
Performance Shortcut

↓

Direct Persistence Mutation
```

---

# Rendimiento y Datos Sensibles

Las optimizaciones de lectura no deben exponer información
adicional únicamente para evitar transformaciones o
consultas.

Las proyecciones deben continuar respetando las reglas de
seguridad y privacidad definidas por AURA.

---

# Importaciones

Las importaciones pueden optimizarse para grandes
volúmenes.

Sin embargo, cada Participation debe continuar respetando:

- identidad;
- OrganizationId;
- Lifecycle;
- Invariants;
- Versioning;
- Consistency Boundary.

---

# Importaciones Masivas

No debe utilizarse una importación masiva para insertar
estados inválidos directamente en persistencia.

Debe mantenerse:

```text
Import

↓

Domain Rules

↓

Valid Participation
```

---

# Migraciones

Las migraciones técnicas pueden optimizarse según
Infrastructure.

No deben modificar silenciosamente:

- ParticipationId;
- OrganizationId;
- ParticipationStatus;
- ParticipationType;
- Version;
- Lifecycle;
- referencias de dominio.

---

# Rendimiento del Repository

El Repository puede ser optimizado siempre que conserve:

```text
getById()

save()

exists()
```

con la semántica definida por:

```text
DOMAIN-008G-Repository-Contract.md
```

Las optimizaciones no pueden modificar su contrato
conceptual.

---

# Rendimiento de Versioning

El control de Version debe mantenerse incluso bajo alta
concurrencia.

La detección de conflictos forma parte de la corrección
del sistema.

No debe considerarse un costo opcional eliminable.

---

# Rendimiento de Domain Events

La creación de Domain Events correspondiente a hechos
válidos debe mantenerse.

Su almacenamiento, distribución o procesamiento puede
optimizarse en Infrastructure sin modificar su semántica.

---

# Rendimiento de Integration Events

La publicación de Integration Events puede desacoplarse
del procesamiento síncrono del Aggregate mediante los
mecanismos consolidados.

La optimización no debe publicar eventos que representen
cambios no confirmados.

---

# Rendimiento de Read Models

Los Read Models pueden optimizarse independientemente.

Pueden utilizar:

- estructuras especializadas;
- índices;
- caché;
- desnormalización;
- persistencias orientadas a lectura.

La elección concreta pertenece a Infrastructure.

---

# Fallo de Optimización

Si una optimización produce un resultado incompatible con
las reglas del dominio, la optimización debe considerarse
inválida.

Debe prevalecer:

```text
Domain Correctness

>

Performance Optimization
```

---

# Testabilidad

Las reglas de rendimiento deben permitir verificar como
mínimo los siguientes escenarios.

```text
Aggregate Load by ParticipationId

Read Query without Aggregate Load

Pagination through Read Model

Filtering through Read Model

Independent Aggregate Processing

Concurrent Modification Detection

No Silent Overwrite

Atomic Persistence

No Partial Aggregate State

No Version Bypass

No Invariant Bypass

No Permission Bypass

No State Machine Bypass

No External Aggregate Loading by Default

No Mutable External Aggregate Reference

Bulk Operations Preserve Individual Boundaries

Read Model Reconstruction

Projection Eventual Consistency

Cache Does Not Replace Version Check

Import Preserves Domain Rules
```

Los escenarios completos se desarrollan en:

```text
DOMAIN-008M-Test-Scenarios.md
```

---

# Matriz de Responsabilidades

```text
Concern                         Responsibility

Write Consistency               Participation Aggregate

Invariant Protection            Participation Aggregate

State Transitions               Participation Aggregate

Version Evolution               Participation Aggregate

Aggregate Persistence           Participation Repository

Concurrency Check               Participation Repository

Read Optimization               Participation Read Models

Search                          Participation Read Models

Filtering                       Participation Read Models

Pagination                      Participation Read Models

Analytics                       Participation Read Models

Caching                         Infrastructure

Indexing                        Infrastructure

Database Optimization           Infrastructure

Projection Processing           Read Side Infrastructure

External Publication            Integration Infrastructure
```

---

# Matriz de Optimización

```text
Optimization                     Allowed

Read Model Projection            Yes

Read Model Denormalization       Yes

Read Side Indexing               Yes

Read Side Cache                  Yes

Repository Lookup Optimization   Yes

Infrastructure Indexing          Yes

Parallel Different Aggregates    Yes

Batch Physical Persistence       Yes, preserving boundaries

Skip Aggregate Root              No

Skip Invariants                  No

Skip Permissions                 No

Skip State Machine               No

Skip Version Check               No

Silent Concurrent Overwrite      No

Direct Status Update             No

Mutable External Aggregate       No

Distributed Aggregate Boundary   No
```

---

# Restricciones

No está permitido:

- optimizar evitando el Aggregate Root;
- optimizar evitando Invariants;
- optimizar evitando Permissions;
- optimizar evitando la State Machine;
- optimizar evitando Lifecycle;
- optimizar eliminando Version;
- optimizar ignorando ExpectedVersion;
- permitir Last Write Wins;
- persistir estados parciales;
- utilizar un Aggregate incompleto para comportamiento que requiera
  estado omitido;
- convertir el Repository en motor analítico;
- cargar masivamente Aggregates para construir dashboards como
  patrón normal;
- incorporar otros Aggregates para evitar consultas adicionales;
- utilizar Eager Loading obligatorio de Aggregates externos;
- utilizar Lazy Loading de Aggregates mutables;
- ampliar el Consistency Boundary;
- compartir Version entre Aggregates;
- utilizar Bulk Update para evitar comportamiento de dominio;
- utilizar una importación para evitar Invariants;
- utilizar una caché como fuente de verdad;
- utilizar datos obsoletos para evitar la comprobación de Version;
- crear Snapshots como nuevas modificaciones del Aggregate;
- ejecutar Commands durante rehidratación;
- generar Domain Events nuevos durante Replay;
- utilizar rendimiento como justificación para introducir
  transacciones distribuidas;
- introducir dependencias tecnológicas dentro del dominio;
- exponer información sensible por conveniencia de rendimiento.

---

# Reglas

## REG-001

Toda optimización debe preservar las Invariants del
Aggregate.

---

## REG-002

Ninguna optimización puede evitar el Aggregate Root.

---

## REG-003

El control de Version debe mantenerse en todas las
modificaciones concurrentes.

---

## REG-004

Las consultas intensivas deben utilizar Read Models cuando
corresponda.

---

## REG-005

El Repository permanece orientado al Aggregate y no a
consultas analíticas.

---

## REG-006

Las referencias externas permanecen expresadas mediante
identificadores.

---

## REG-007

Las optimizaciones no pueden ampliar el Consistency
Boundary.

---

## REG-008

Las modificaciones del Aggregate deben persistirse de
forma atómica.

---

## REG-009

Las operaciones masivas mantienen límites, Version e
Invariants independientes para cada Participation.

---

## REG-010

Las optimizaciones de Infrastructure no modifican el
modelo conceptual del dominio.

---

## REG-011

Los Read Models pueden optimizarse independientemente del
Write Model.

---

## REG-012

Una caché no reemplaza la fuente oficial de verdad ni el
control de concurrencia.

---

## REG-013

Una optimización nunca puede convertir un estado inválido
en un resultado aceptable.

---

# Definición de Éxito

El Aggregate **Participation** mantiene reglas de
rendimiento que permiten optimizar escritura, lectura,
consulta, proyecciones y procesamiento concurrente sin
comprometer el modelo DDD consolidado de AURA Core.

Las reglas garantizan que:

- Participation continúe siendo una unidad independiente de
  consistencia;
- el Aggregate Root permanezca como única autoridad para
  modificaciones;
- las Invariants nunca sean omitidas por razones de rendimiento;
- Lifecycle y State Machine permanezcan protegidos;
- Version continúe controlando modificaciones concurrentes;
- las escrituras se mantengan atómicas;
- el Repository conserve su responsabilidad sobre el Write Model;
- los Read Models absorban las necesidades de consulta intensiva;
- búsquedas, filtros, paginación y agregaciones permanezcan
  separadas del Aggregate;
- las referencias externas continúen utilizando identificadores;
- otros Aggregates no sean cargados o absorbidos por conveniencia;
- las operaciones masivas mantengan límites independientes;
- las cachés permanezcan como optimizaciones derivadas;
- las proyecciones puedan evolucionar independientemente;
- las optimizaciones técnicas permanezcan en Infrastructure;
- ninguna optimización altere las reglas conceptuales establecidas.

La regla fundamental es:

```text
Performance

+

Domain Correctness

=

Valid Optimization
```

mientras:

```text
Performance

-

Domain Correctness

=

Invalid Optimization
```

De esta forma,
`DOMAIN-008N-Performance-Rules.md` establece las reglas oficiales
para que el rendimiento de **Participation** pueda evolucionar sin
romper identidad, Invariants, Versioning, Consistency Boundary,
CQRS ni las demás decisiones ya consolidadas de AURA Core.
````
