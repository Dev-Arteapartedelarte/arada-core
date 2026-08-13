# DOMAIN-008G — Participation Repository Contract

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Participation Management

Aggregate:
Participation

Autor:
ARADA

Documentos relacionados:

- DOMAIN-008-Aggregate.md
- DOMAIN-008A-Lifecycle.md
- DOMAIN-008B-State-Machine.md
- DOMAIN-008C-Commands.md
- DOMAIN-008D-Domain-Events.md
- DOMAIN-008E-Invariants.md
- DOMAIN-008F-Permissions.md
- DOMAIN-008H-Examples.md
- DOMAIN-008I-Versioning.md
- DOMAIN-008J-Consistency-Boundary.md
- DOMAIN-008K-Integration-Events.md
- DOMAIN-008L-Read-Model.md
- DOMAIN-008M-Test-Scenarios.md
- DOMAIN-008N-Performance-Rules.md
- DOMAIN-008O-Security-Model.md
- DOMAIN-008P-Extension-Points.md
- CORE-003-Shared-Kernel.md
- CORE-004-Ubiquitous-Language.md
- CORE-005-Domain-Events.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Definir el contrato conceptual oficial del Repository del
Aggregate **Participation**.

El Repository representa la abstracción mediante la cual el dominio
puede recuperar y persistir una Participation como una unidad
completa de consistencia.

El Repository no constituye una base de datos.

El Repository no constituye un ORM.

El Repository no constituye un servicio HTTP.

El Repository no constituye un Read Model.

El Repository define exclusivamente el contrato necesario para
preservar y recuperar el Aggregate sin introducir dependencias de
Infrastructure dentro del dominio.

---

# Propósito

El Repository permite mantener la separación:

```text
Domain

↓

Repository Contract

↓

Infrastructure Adapter

↓

Persistence Technology
```

El dominio conoce:

```text
ParticipationRepository
```

El dominio no conoce:

```text
PostgreSQL

MongoDB

MySQL

SQLite

ORM

Redis

Elasticsearch

Filesystem

HTTP API
```

La implementación concreta pertenece a Infrastructure.

---

# Principios

El Repository de Participation sigue los siguientes principios:

- trabaja con el Aggregate completo;
- utiliza ParticipationId como identidad principal del Aggregate;
- preserva el límite de consistencia;
- no modifica atributos internos directamente;
- no contiene lógica de negocio;
- no decide transiciones de estado;
- no decide Permissions;
- no decide Invariants;
- no ejecuta Commands;
- no produce cambios de dominio por iniciativa propia;
- protege la persistencia frente a modificaciones concurrentes;
- preserva Version;
- permite reconstruir el estado persistido;
- mantiene independencia tecnológica;
- no expone detalles del almacenamiento al dominio;
- no convierte consultas analíticas en responsabilidades del
  Aggregate Repository.

---

# Repository

El contrato conceptual es:

```text
ParticipationRepository
```

Su responsabilidad fundamental es:

```text
Participation Aggregate

↕

Persistence
```

El Repository opera exclusivamente sobre Aggregates
Participation.

---

# Aggregate Root

La unidad persistida por el Repository es:

```text
Participation
```

No deben persistirse mediante contratos independientes partes
internas del Aggregate como si poseyeran autonomía propia.

Debe mantenerse:

```text
ParticipationRepository

↓

Participation
```

No:

```text
ParticipationRepository

↓

ParticipationStatusRepository

ParticipationMetadataRepository

ParticipationContextRepository

ParticipationTimestampRepository
```

cuando estos elementos formen parte del mismo límite de
consistencia.

---

# Unidad de Persistencia

Participation constituye la unidad lógica de persistencia.

Debe mantenerse:

```text
Load Participation

↓

Execute Domain Behavior

↓

Validate Invariants

↓

Save Participation
```

La persistencia debe representar el estado completo y válido
resultante del Aggregate.

---

# Identidad de Persistencia

El Repository identifica Participation mediante:

```text
ParticipationId
```

ParticipationId:

- pertenece al dominio;
- es único;
- es inmutable;
- no depende del identificador físico de la base de datos;
- no debe ser sustituido por una clave técnica de Infrastructure.

Una implementación puede utilizar identificadores internos
adicionales.

Esos identificadores no reemplazan:

```text
ParticipationId
```

como identidad oficial del Aggregate.

---

# OrganizationId

El Repository debe preservar:

```text
OrganizationId
```

como parte del estado del Aggregate.

OrganizationId no constituye la identidad primaria de
Participation.

Por lo tanto:

```text
ParticipationId

≠

OrganizationId
```

Una Organization puede mantener múltiples Participation.

El Repository no debe inferir identidad de Participation mediante
OrganizationId.

---

# Contrato Conceptual

El Repository debe proporcionar conceptualmente operaciones
equivalentes a:

```text
getById()

save()

exists()
```

Pueden existir operaciones adicionales estrictamente necesarias
para preservar reglas del dominio o resolver la recuperación del
Aggregate.

Estas operaciones no deben transformar el Repository en un
servicio general de consultas.

---

# getById()

## Objetivo

Recuperar una Participation mediante:

```text
ParticipationId
```

## Entrada

```text
ParticipationId
```

## Resultado

Conceptualmente:

```text
Participation
```

o:

```text
NotFound
```

## Reglas

`getById()` debe:

- recuperar exactamente un Aggregate cuando exista;
- reconstruir su estado persistido;
- preservar ParticipationId;
- preservar OrganizationId;
- preservar ParticipationType;
- preservar ParticipationStatus;
- preservar referencias de dominio;
- preservar timestamps del Lifecycle;
- preservar Version;
- no incrementar Version;
- no generar nuevos Domain Events;
- no ejecutar Commands;
- no modificar el estado durante la recuperación.

---

# save()

## Objetivo

Persistir una modificación válida de Participation.

## Entrada

```text
Participation
```

y, cuando corresponda al control de concurrencia:

```text
ExpectedVersion
```

## Resultado

Conceptualmente:

```text
Persisted
```

o una condición explícita de fallo como:

```text
ConcurrencyConflict

PersistenceFailure
```

## Reglas

`save()` debe:

- persistir el Aggregate como unidad;
- preservar su identidad;
- preservar sus Invariants;
- comprobar la versión esperada cuando corresponda;
- impedir sobrescrituras concurrentes incompatibles;
- no modificar comportamiento del dominio;
- no decidir nuevas transiciones;
- no alterar arbitrariamente Version;
- no corregir silenciosamente estados inválidos;
- no modificar Aggregates externos.

---

# exists()

## Objetivo

Determinar si existe una Participation identificada mediante:

```text
ParticipationId
```

## Entrada

```text
ParticipationId
```

## Resultado

```text
true
```

o:

```text
false
```

## Reglas

`exists()`:

- no modifica el Aggregate;
- no incrementa Version;
- no genera Domain Events;
- no constituye una consulta analítica;
- no sustituye `getById()` cuando se requiere comportamiento del
  Aggregate.

---

# Recuperación del Aggregate

La recuperación debe reconstruir una Participation conceptualmente
equivalente a la persistida.

Debe mantenerse:

```text
Persisted Participation

↓

Repository

↓

Rehydrated Participation
```

con:

```text
Same ParticipationId

Same OrganizationId

Same Domain State

Same Lifecycle State

Same Historical Timestamps

Same Version
```

---

# Rehidratación

La rehidratación no representa una modificación del dominio.

Durante la rehidratación:

- no se ejecutan Commands;
- no se aplican Permissions;
- no se toman nuevas decisiones de negocio;
- no se incrementa Version;
- no se generan nuevos Domain Events;
- no se reemplazan timestamps históricos;
- no se modifica ParticipationId;
- no se modifica OrganizationId.

Debe mantenerse:

```text
Rehydrate

≠

Create
```

y:

```text
Rehydrate

≠

Modify
```

---

# Estado Rehidratado

El Aggregate recuperado debe representar el último estado válido
persistido.

Ejemplo:

```text
ParticipationId = P-001

OrganizationId = O-001

ParticipationStatus = Active

Version = 4
```

Después de la recuperación debe mantenerse:

```text
ParticipationId = P-001

OrganizationId = O-001

ParticipationStatus = Active

Version = 4
```

No:

```text
Version = 5
```

por el simple hecho de cargar el Aggregate.

---

# Persistencia de Estado

El Repository persiste el estado necesario para reconstruir el
Aggregate.

Conceptualmente puede incluir:

```text
ParticipationId

OrganizationId

ParticipationType

ParticipationStatus

Domain References

Metadata

CreatedAt

StartedAt

CompletedAt

WithdrawnAt

InvalidatedAt

ArchivedAt

Version
```

La representación física concreta no forma parte de este
documento.

---

# Referencias de Dominio

Cuando Participation mantenga referencias hacia otros Aggregates,
el Repository debe preservar sus identificadores.

Conceptualmente:

```text
CitizenId

MembershipId

AssemblyId

ProposalId

TerritoryId
```

cuando correspondan al estado de Participation.

El Repository no debe convertir estas referencias en Aggregates
embebidos.

---

# Regla de No Absorción

Debe mantenerse:

```text
Participation

↓

CitizenId
```

No:

```text
Participation

↓

Citizen Aggregate
```

Debe mantenerse:

```text
Participation

↓

AssemblyId
```

No:

```text
Participation

↓

Assembly Aggregate
```

Debe mantenerse:

```text
Participation

↓

ProposalId
```

No:

```text
Participation

↓

Proposal Aggregate
```

La estrategia física de almacenamiento no puede redefinir el
límite conceptual del Aggregate.

---

# Persistencia y Aggregate Boundary

La forma en que Infrastructure almacene información no determina
el Aggregate Boundary.

Una base de datos documental podría almacenar información
físicamente cercana.

Una base de datos relacional podría distribuirla entre múltiples
tablas.

Ninguna de estas decisiones modifica:

```text
Participation Aggregate Boundary
```

El límite es definido por el dominio.

---

# Persistencia Completa

Una modificación válida debe persistirse de forma que el Aggregate
no pueda quedar parcialmente actualizado.

Ejemplo de modificación conceptual:

```text
Active

↓

CompleteParticipation

↓

Completed
```

El resultado puede requerir preservar conjuntamente:

```text
ParticipationStatus = Completed

CompletedAt

Version
```

No debe observarse un estado persistido como:

```text
ParticipationStatus = Completed

CompletedAt = None
```

si Completion exige ambos valores.

---

# Atomicidad

La persistencia de una modificación del Aggregate debe respetar su
unidad lógica de consistencia.

Debe mantenerse:

```text
Valid Aggregate State

↓

Atomic Persistence

↓

Persisted Valid Aggregate State
```

No:

```text
Partial State A

↓

Partial State B

↓

Temporarily Invalid Aggregate
```

como resultado visible de una única modificación de dominio.

---

# Consistencia

El Repository participa en la preservación técnica de la
consistencia, pero no define las Invariants.

Debe mantenerse:

```text
Participation Aggregate

↓

Defines Valid State
```

```text
Repository

↓

Persists Valid State
```

El Repository no sustituye al Aggregate como autoridad del
dominio.

---

# Invariants

Las Invariants oficiales se definen en:

```text
DOMAIN-008E-Invariants.md
```

El Repository debe respetarlas.

No debe:

- inventar nuevas Invariants;
- eliminar Invariants;
- reinterpretar Invariants;
- corregir silenciosamente violaciones;
- persistir deliberadamente estados que el Aggregate considera
  inválidos.

---

# Estado Inválido

Si Infrastructure detecta que un estado no puede persistirse de
forma coherente, debe fallar explícitamente.

No debe existir:

```text
Invalid Aggregate

↓

Repository Auto-Correction

↓

Persisted Aggregate
```

como sustituto de comportamiento del dominio.

---

# Version

Participation utiliza:

```text
Version
```

para representar su evolución confirmada.

El Repository debe preservar Version durante:

```text
Load

Save

Concurrency Validation
```

La definición normativa completa se encuentra en:

```text
DOMAIN-008I-Versioning.md
```

---

# Optimistic Concurrency

El Repository debe soportar el modelo de concurrencia optimista
establecido para Participation.

Conceptualmente:

```text
Load Participation

Version = N

↓

Domain Modification

Version = N + 1

↓

Save

Expected Persisted Version = N
```

La persistencia solo puede confirmarse si la versión persistida
continúa siendo la esperada.

---

# ExpectedVersion

Para una modificación puede utilizarse conceptualmente:

```text
ExpectedVersion
```

Debe cumplirse:

```text
PersistedVersion

=

ExpectedVersion
```

antes de confirmar el nuevo estado.

Si no se cumple:

```text
ConcurrencyConflict
```

---

# ConcurrencyConflict

Debe producirse un conflicto cuando:

```text
ExpectedVersion

≠

PersistedVersion
```

Ejemplo:

```text
Process A loads Version 5

Process B loads Version 5

Process A saves Version 6

Process B attempts save
```

Para Process B:

```text
ExpectedVersion = 5

PersistedVersion = 6
```

Resultado:

```text
ConcurrencyConflict
```

Process B no puede sobrescribir silenciosamente Version 6.

---

# No Last-Write-Wins Silencioso

No debe utilizarse como comportamiento conceptual:

```text
Last Write Wins
```

cuando ello permita perder una modificación confirmada.

Debe mantenerse:

```text
Version Conflict

↓

Explicit Conflict
```

No:

```text
Version Conflict

↓

Silent Overwrite
```

---

# Version durante getById()

La recuperación no modifica Version.

Debe mantenerse:

```text
Persisted Version = N

↓

getById()

↓

Aggregate Version = N
```

---

# Version durante save()

`save()` no inventa una nueva Version arbitrariamente.

La evolución de Version debe corresponder al modelo establecido por
el Aggregate y por:

```text
DOMAIN-008I-Versioning.md
```

El Repository valida y preserva esa evolución.

---

# Version durante exists()

`exists()` no modifica Version.

Debe mantenerse:

```text
exists()

↓

Read Only
```

---

# Version y Fallo de Persistencia

Si la persistencia no se confirma, el estado persistido no debe
considerarse actualizado.

Conceptualmente:

```text
Save Attempt

↓

PersistenceFailure

↓

No Confirmed Persistence
```

La gestión del estado en memoria después del fallo pertenece al
flujo de aplicación correspondiente.

El Repository no debe reportar éxito cuando el commit no ocurrió.

---

# Version y ConcurrencyConflict

Cuando existe conflicto:

```text
ConcurrencyConflict
```

el Repository no confirma la nueva versión solicitada.

Debe mantenerse el estado persistido previamente confirmado.

---

# Insert de Nueva Participation

La primera persistencia de una Participation debe garantizar que su
identidad no exista previamente.

Conceptualmente:

```text
New Participation

↓

ParticipationId = P
```

debe comprobarse contra la persistencia de manera que no puedan
confirmarse dos Aggregates diferentes con la misma identidad.

---

# Duplicate Identity

Cuando ParticipationId ya exista, no debe confirmarse una nueva
Participation con la misma identidad.

Debe producirse una condición explícita equivalente a:

```text
DuplicateIdentity
```

o al mecanismo de error definido por el contrato de aplicación.

La implementación técnica concreta no forma parte de este
documento.

---

# Unicidad

La unicidad de ParticipationId debe preservarse incluso ante
solicitudes concurrentes.

No basta con una validación previa no atómica como:

```text
exists(P) = false

↓

create P
```

si dos procesos pueden confirmar simultáneamente la misma
identidad.

Infrastructure debe proporcionar las garantías técnicas necesarias
para preservar la regla.

---

# No Reutilización

Una Participation archivada continúa existiendo conceptualmente
con su identidad.

El Repository no debe considerar:

```text
Archived
```

como equivalente a:

```text
Nonexistent
```

para permitir reutilización de ParticipationId.

---

# Archive

El archivado representa una transición del Lifecycle.

No representa eliminación física obligatoria.

Debe mantenerse:

```text
Participation

↓

Archived
```

como estado recuperable cuando las reglas de retención y
persistencia lo permitan.

---

# Archive no es Delete

El Repository no debe traducir automáticamente:

```text
ArchiveParticipation
```

en:

```text
DELETE FROM participation
```

como definición conceptual.

La implementación física puede aplicar estrategias específicas,
pero debe preservar la identidad, trazabilidad e historia exigidas
por el dominio.

---

# Eliminación Física

La eliminación física no forma parte de las operaciones ordinarias
del Repository conceptual de Participation.

No se define como operación de dominio:

```text
deleteParticipation()
```

para representar el Lifecycle normal.

El estado terminal oficial es:

```text
Archived
```

---

# Hard Delete

Una eventual eliminación física por razones operacionales,
regulatorias o de retención no constituye una transición del
Aggregate.

Debe permanecer separada de:

```text
Participation Lifecycle
```

y no puede utilizarse para reinterpretar Archive.

---

# Queries de Dominio

El Repository puede incorporar consultas estrictamente necesarias
para recuperar Aggregates o proteger reglas del dominio.

No debe convertirse en un catálogo general de consultas de
presentación.

Debe mantenerse:

```text
Repository

=

Aggregate Persistence
```

No:

```text
Repository

=

Reporting Engine
```

---

# Consultas Analíticas

Consultas como:

```text
Participation Count by Territory

Participation Statistics

Participation Dashboard

Participation Trends

Participation by Date Range

Participation Ranking

Participation Analytics
```

no constituyen responsabilidades primarias del Repository del
Aggregate.

Estas consultas corresponden a:

```text
Read Models
```

definidos en:

```text
DOMAIN-008L-Read-Model.md
```

---

# Consultas por Estado

Una consulta masiva como:

```text
findAllActiveParticipations()
```

puede pertenecer al Read Side cuando su propósito sea listado,
visualización o análisis.

No debe añadirse automáticamente al Repository del Aggregate por
conveniencia de interfaz.

---

# Consultas por Organization

Una consulta como:

```text
listParticipationsByOrganization()
```

debe evaluarse según su propósito.

Si corresponde a:

- listado;
- dashboard;
- búsqueda;
- paginación;
- reporte;

debe resolverse preferentemente mediante el Read Model.

El Repository del Aggregate no debe transformarse en una API de
consulta general.

---

# Consultas por Citizen

Una consulta como:

```text
findParticipationsByCitizen()
```

no debe incorporarse al contrato del Repository únicamente porque
una pantalla la necesite.

Cuando la finalidad sea lectura, corresponde al modelo CQRS de
consulta.

---

# Consultas por Assembly

De igual forma:

```text
findParticipationsByAssembly()
```

pertenece conceptualmente al Read Side cuando su objetivo sea
obtener listados o proyecciones.

El Repository mantiene su foco en recuperar Aggregates para
comportamiento de dominio.

---

# Consultas por Proposal

La relación:

```text
ProposalId
```

no convierte al Repository de Participation en un servicio de
consulta de Proposal.

Cada Aggregate mantiene su propio Repository.

---

# Paginación

La paginación pertenece principalmente a modelos de lectura.

No constituye una responsabilidad fundamental del Repository del
Aggregate.

Debe mantenerse:

```text
Pagination

↓

Read Model
```

cuando el objetivo sea presentar colecciones.

---

# Sorting

El ordenamiento de colecciones para interfaces o reportes tampoco
forma parte del contrato fundamental del Repository.

Conceptualmente:

```text
Sorting

↓

Read Side
```

---

# Filtering

Filtros complejos como:

```text
Status

Type

Territory

Citizen

Assembly

Proposal

Date Range
```

pertenecen a proyecciones de lectura cuando se utilizan para
exploración o análisis.

---

# Full Text Search

El Repository del Aggregate no debe asumir responsabilidades de:

```text
Full Text Search
```

La búsqueda especializada pertenece a Read Models o servicios de
consulta.

---

# Reporting

El Repository no genera reportes.

No debe conocer:

```text
PDF

CSV

Dashboard

Chart

BI
```

Estas responsabilidades pertenecen fuera del dominio del
Repository.

---

# Domain Events

Participation puede producir Domain Events como resultado de
modificaciones válidas.

El Repository no inventa Domain Events.

Debe mantenerse:

```text
Participation Aggregate

↓

Domain Behavior

↓

Domain Events
```

No:

```text
Repository

↓

Invent Domain Event
```

---

# Persistencia y Domain Events

El Repository debe permitir que el flujo de aplicación preserve la
coherencia entre:

```text
Aggregate State

Version

Domain Events
```

La estrategia técnica de almacenamiento o publicación no forma
parte de este contrato conceptual.

---

# Eventos Pendientes

Cuando el modelo de implementación mantenga Domain Events
pendientes dentro del Aggregate, el Repository no debe
reinterpretarlos ni alterar su significado.

Los eventos pertenecen al dominio.

El Repository participa únicamente en la persistencia según el
contrato establecido.

---

# Evento no es Estado de Persistencia Externo

La publicación hacia sistemas externos no forma parte de la
responsabilidad conceptual fundamental del Repository.

Debe mantenerse:

```text
Repository

↓

Aggregate Persistence
```

y:

```text
Integration Publication

↓

Integration Mechanism
```

---

# Integration Events

Los Integration Events se definen en:

```text
DOMAIN-008K-Integration-Events.md
```

El Repository no transforma automáticamente cualquier Domain Event
en Integration Event como responsabilidad del dominio.

---

# Event Sourcing Compatible

El contrato de Repository debe ser compatible con una eventual
estrategia de Event Sourcing sin exigirla.

Debe mantenerse la posibilidad conceptual de:

```text
ParticipationId

↓

Event Stream

↓

Rehydrated Participation
```

si la arquitectura de persistencia adopta dicho modelo.

---

# Event Sourcing no Obligatorio

La compatibilidad con Event Sourcing no significa que el
Repository deba utilizarlo obligatoriamente.

Puede existir una implementación basada en:

```text
Current State Persistence
```

o una estrategia compatible con:

```text
Event Stream Persistence
```

sin alterar el modelo conceptual de Participation.

---

# Snapshot

Una eventual estrategia de snapshots pertenece a Infrastructure.

No modifica:

- ParticipationId;
- Lifecycle;
- State Machine;
- Invariants;
- Domain Events;
- Version.

Un Snapshot no constituye un nuevo hecho del dominio.

---

# Repository y Commands

El Repository no ejecuta Commands.

Debe mantenerse:

```text
Command

↓

Application Service

↓

Participation Aggregate
```

y posteriormente:

```text
Participation Aggregate

↓

Repository.save()
```

No:

```text
Repository.executeCommand()
```

---

# Repository y Permissions

El Repository no decide si un actor posee:

```text
Participation.Register

Participation.Activate

Participation.Complete

Participation.Withdraw

Participation.Invalidate

Participation.Archive
```

La autorización se define en:

```text
DOMAIN-008F-Permissions.md
```

---

# Repository y Lifecycle

El Repository no decide:

```text
Registered → Active
```

ni:

```text
Active → Completed
```

ni ninguna otra transición.

Estas reglas pertenecen a:

```text
DOMAIN-008A-Lifecycle.md

DOMAIN-008B-State-Machine.md
```

---

# Repository y Invariants

El Repository no reemplaza:

```text
DOMAIN-008E-Invariants.md
```

Puede aplicar restricciones técnicas complementarias.

Sin embargo:

```text
Database Constraint

≠

Domain Invariant Definition
```

---

# Repository y Metadata

El Repository persiste Metadata cuando forme parte del estado del
Aggregate.

No interpreta Metadata para decidir comportamiento.

No debe utilizar Metadata como mecanismo para modificar
silenciosamente atributos protegidos.

---

# Repository y Timestamps

El Repository preserva los timestamps definidos por el Lifecycle.

Conceptualmente:

```text
CreatedAt

StartedAt

CompletedAt

WithdrawnAt

InvalidatedAt

ArchivedAt
```

El Repository no debe reemplazarlos durante cada lectura o
persistencia por el tiempo actual.

---

# CreatedAt

Debe preservarse exactamente como hecho histórico de creación.

No debe recalcularse durante:

```text
getById()

save()

rehydrate()
```

---

# StartedAt

Debe preservarse cuando la Participation haya sido activada.

El Repository no determina cuándo comienza una Participation.

Solo persiste el hecho producido por el Aggregate.

---

# CompletedAt

Debe preservarse después de Completion.

No debe eliminarse si posteriormente la Participation es
Invalidated o Archived.

---

# WithdrawnAt

Debe preservarse después de Withdrawal.

Archive no reemplaza WithdrawnAt.

---

# InvalidatedAt

Debe preservarse después de Invalidation.

Archive no reemplaza InvalidatedAt.

---

# ArchivedAt

Debe preservarse cuando la Participation alcanza:

```text
Archived
```

No sustituye los timestamps históricos anteriores.

---

# Repository y Audit

El Repository no constituye el Aggregate Audit.

No debe incorporar dentro de Participation una colección completa
de registros de auditoría externos.

La trazabilidad del dominio puede utilizar:

```text
ParticipationId

Version

Domain Events

Timestamps

ActorId

CorrelationId

CausationId
```

cuando corresponda.

Audit mantiene su propio límite de consistencia.

---

# Repository y Security

El Repository no almacena como parte de Participation:

```text
Passwords

JWT

OAuth Tokens

Private Keys

API Keys

Sessions

Authentication Secrets
```

La persistencia de credenciales no forma parte del Aggregate.

---

# Repository y Authorization

El Repository no debe exponer operaciones de modificación directa
que permitan evitar el modelo de autorización.

No debe convertirse en una puerta alternativa como:

```text
updateStatus(participationId, status)
```

utilizada desde Application para evitar el comportamiento del
Aggregate.

---

# No Partial Updates de Dominio

No deben exponerse como contrato conceptual operaciones como:

```text
updateStatus()

updateVersion()

updateOrganizationId()

updateStartedAt()

updateCompletedAt()

updateArchivedAt()
```

para modificar partes del Aggregate desde fuera.

Debe mantenerse:

```text
Load Aggregate

↓

Domain Behavior

↓

Save Aggregate
```

---

# Patch Directo

El Repository no define:

```text
patchParticipation(fields)
```

como mecanismo para modificar el dominio evitando sus
comportamientos.

La optimización técnica de persistencia no debe filtrarse como
semántica del contrato del dominio.

---

# Bulk Update

No debe exponerse:

```text
updateAllParticipations(...)
```

como mecanismo para modificar directamente múltiples Aggregates
evitando:

- Commands;
- Permissions;
- Lifecycle;
- State Machine;
- Invariants;
- Versioning.

---

# Bulk Persistence

Infrastructure puede optimizar operaciones físicas cuando ello no
modifique la semántica del dominio.

Cada Participation continúa siendo:

```text
Independent Aggregate

Independent Version

Independent Consistency Boundary
```

---

# Transacciones

Una modificación de Participation debe persistirse dentro de una
unidad transaccional compatible con su límite de consistencia.

Debe mantenerse:

```text
One Participation Modification

↓

One Logical Transaction
```

No debe requerirse una transacción distribuida con otros
Aggregates.

---

# No Distributed Transaction

El Repository no debe ampliar una transacción para modificar
simultáneamente:

```text
Participation

Assembly

Proposal

Voting

Document

Notification

Audit
```

como requisito normal para preservar Participation.

La coordinación entre Aggregates utiliza los mecanismos definidos
por la arquitectura.

---

# Aggregate Isolation

Cada Aggregate posee su propio límite.

Conceptualmente:

```text
ParticipationRepository

↓

Participation
```

```text
AssemblyRepository

↓

Assembly
```

```text
ProposalRepository

↓

Proposal
```

No debe existir un Repository que mezcle sus estados internos como
si constituyeran un único Aggregate.

---

# Cross-Aggregate Coordination

Cuando un caso de uso necesite coordinar múltiples Aggregates, la
coordinación corresponde a:

```text
Application Services

Domain Events

Integration Events
```

según corresponda.

El Repository de Participation no asume esa responsabilidad.

---

# Unit of Work

Una implementación puede utilizar un patrón técnico equivalente a:

```text
Unit of Work
```

cuando sea necesario para administrar la persistencia.

Esta decisión pertenece a Infrastructure/Application.

No modifica el contrato conceptual ni el límite de Participation.

---

# Transaction Manager

El dominio no depende de un Transaction Manager concreto.

No debe conocer:

```text
SQL Transaction

Mongo Session

ORM Session

Distributed Transaction Coordinator
```

El Adapter de persistencia proporciona las garantías necesarias.

---

# Repository Interface

El contrato debe ubicarse conceptualmente en una capa accesible al
dominio o a la aplicación sin introducir dependencia hacia
Infrastructure.

La dirección de dependencia debe mantenerse:

```text
Infrastructure

↓

implements

↓

ParticipationRepository Contract
```

No:

```text
Domain

↓

depends on PostgreSQLRepository
```

---

# Dependency Inversion

Debe cumplirse:

```text
Domain Abstraction

↑

Infrastructure Implementation
```

La implementación depende del contrato.

El contrato no depende de la implementación.

---

# Implementaciones

Pueden existir múltiples implementaciones del mismo contrato.

Ejemplos conceptuales:

```text
InMemoryParticipationRepository

RelationalParticipationRepository

DocumentParticipationRepository

EventSourcedParticipationRepository
```

Estos nombres representan posibilidades de Infrastructure.

No forman parte del modelo obligatorio del dominio.

---

# InMemory Repository

Una implementación en memoria puede utilizarse para:

- pruebas;
- desarrollo;
- simulaciones;
- ejecución local.

Debe respetar exactamente las mismas reglas contractuales
relevantes que una implementación persistente.

No puede ignorar Versioning únicamente por tratarse de memoria.

---

# Tecnología Relacional

Una implementación relacional puede utilizar:

```text
Tables

Rows

Indexes

Constraints

Transactions
```

Estas estructuras no deben filtrarse hacia el dominio.

---

# Tecnología Documental

Una implementación documental puede almacenar el estado del
Aggregate como documento.

La estructura física del documento no redefine las entidades,
Value Objects ni referencias del dominio.

---

# Tecnología Event Sourced

Una implementación Event Sourced puede reconstruir Participation
desde eventos.

Debe respetar:

- orden de eventos;
- identidad;
- Version;
- rehidratación;
- invariantes para nuevas decisiones;
- separación entre Domain Events e Integration Events.

---

# Independencia Tecnológica

ParticipationRepository no depende conceptualmente de:

```text
PostgreSQL

MongoDB

MySQL

MariaDB

SQLite

Redis

DynamoDB

Cassandra

Elasticsearch

OpenSearch

SQLAlchemy

Django ORM

Prisma

TypeORM

Entity Framework

Hibernate
```

La elección tecnológica pertenece a Infrastructure.

---

# Serialización

La serialización del Aggregate para persistencia pertenece al
Adapter.

El dominio no debe incorporar detalles como:

```text
BSON

SQL Row

JSON Database Document

ORM Entity
```

como parte de su modelo conceptual.

---

# Mapping

Puede existir un Mapper entre:

```text
Domain Model

↕

Persistence Model
```

cuando la implementación lo requiera.

El Mapper no modifica el significado del dominio.

---

# Persistence Model

Una implementación puede mantener un modelo físico diferente del
modelo de dominio.

Debe mantenerse:

```text
Domain Model

≠

Persistence Model
```

cuando la separación sea necesaria.

La persistencia no define el dominio.

---

# Schema Evolution

Los cambios del esquema físico deben preservar la capacidad de
reconstruir correctamente Participation.

Una migración técnica no debe modificar silenciosamente:

- ParticipationId;
- OrganizationId;
- ParticipationType;
- ParticipationStatus;
- Lifecycle;
- timestamps;
- Version;
- referencias de dominio.

---

# Migraciones

Las migraciones de Infrastructure deben respetar el modelo
conceptual vigente.

Una migración no puede utilizarse para introducir una nueva regla
de dominio sin documentarla en los artefactos correspondientes.

---

# Data Corruption

Si la persistencia contiene información incompatible con las reglas
del Aggregate, la recuperación no debe corregir silenciosamente la
historia.

La situación debe tratarse explícitamente como una condición de
inconsistencia o corrupción según la capa responsable.

No debe inventarse un estado de dominio para ocultar el problema.

---

# NotFound

Cuando `getById()` no encuentre ParticipationId debe producir una
condición explícita equivalente a:

```text
NotFound
```

No debe retornar una Participation ficticia.

No debe crear automáticamente un Aggregate nuevo.

---

# PersistenceFailure

Cuando Infrastructure no pueda confirmar una operación de
persistencia debe producir una condición explícita equivalente a:

```text
PersistenceFailure
```

No debe reportarse:

```text
Persisted
```

si el estado no fue confirmado.

---

# Error de Infraestructura

Errores como:

```text
Connection Failure

Timeout

Storage Unavailable

Serialization Failure
```

pertenecen a Infrastructure.

El contrato debe permitir que Application distinga un fallo de
persistencia de un rechazo del dominio.

---

# Domain Rejection vs Persistence Failure

Debe mantenerse:

```text
Domain Rejection

≠

Persistence Failure
```

Un Command puede ser rechazado antes de intentar persistencia.

Una persistencia puede fallar después de una modificación válida
en memoria.

Ambas condiciones tienen semánticas diferentes.

---

# Concurrency Conflict vs Persistence Failure

También debe mantenerse:

```text
ConcurrencyConflict

≠

Generic PersistenceFailure
```

El conflicto de versión posee significado propio para el control de
concurrencia.

---

# Retry

Una política técnica de Retry puede aplicarse a determinados fallos
de Infrastructure.

No debe aplicarse ciegamente a:

```text
ConcurrencyConflict
```

como si la operación pudiera sobrescribirse sin volver a evaluar el
estado actual.

---

# Retry y Commands

Cuando una operación deba reintentarse después de un conflicto de
concurrencia, debe considerarse el nuevo estado del Aggregate.

No debe asumirse que una decisión válida para:

```text
Version = N
```

continúa siendo automáticamente válida para:

```text
Version = N + 1
```

---

# Idempotencia de Persistencia

El Repository debe evitar que un reintento técnico produzca
duplicaciones incompatibles con la identidad y Version del
Aggregate.

La estrategia concreta depende de Infrastructure.

La semántica del dominio debe permanecer estable.

---

# Repository y Cache

Una implementación puede utilizar Cache.

Cache pertenece a Infrastructure.

Debe preservar:

- identidad;
- Version;
- coherencia suficiente para operaciones de escritura;
- protección contra datos obsoletos utilizados como estado actual.

---

# Cache no es Fuente de Verdad Conceptual

Una Cache no redefine la identidad ni el estado del Aggregate.

La implementación debe garantizar que el uso de Cache no permita
evitar el control de concurrencia.

---

# Repository y Read Model

Debe mantenerse una separación clara:

```text
ParticipationRepository

=

Write Model Persistence
```

```text
Participation Read Models

=

Optimized Queries
```

El Repository no debe asumir responsabilidades propias de las
proyecciones.

---

# CQRS

En una arquitectura CQRS:

```text
Command Side

↓

Participation Aggregate

↓

ParticipationRepository
```

Mientras:

```text
Query Side

↓

Participation Read Models
```

Ambos modelos pueden utilizar persistencias diferentes.

---

# Read Model Persistence

La persistencia de Read Models no forma parte del contrato de:

```text
ParticipationRepository
```

Puede existir infraestructura específica para proyecciones.

---

# Repository y Domain Events Replay

Cuando una implementación utilice Event Sourcing, el Repository
puede reconstruir el Aggregate mediante replay.

Debe mantenerse:

```text
Load Event Stream

↓

Apply Historical Events

↓

Rehydrated Participation
```

El replay:

- no ejecuta Commands;
- no evalúa Permissions;
- no genera eventos nuevos;
- no incrementa Version adicionalmente;
- no modifica hechos históricos.

---

# Orden de Eventos

Cuando el estado se reconstruya mediante eventos, estos deben
aplicarse en el orden definido por su secuencia histórica.

No debe reconstruirse el Aggregate aplicando eventos en un orden
arbitrario.

---

# Stream Identity

En Event Sourcing, el stream debe corresponder conceptualmente a:

```text
ParticipationId
```

La implementación puede utilizar una representación técnica
adicional.

Esta representación no sustituye la identidad del dominio.

---

# Event Version

La secuencia histórica debe mantener coherencia con Version.

No debe aceptarse silenciosamente una secuencia que produzca
versiones incompatibles con la historia persistida.

---

# Snapshot y Version

Cuando se utilicen snapshots, estos deben registrar información
suficiente para continuar la reconstrucción desde una Version
conocida.

Un snapshot no reinicia Version.

---

# Repository y Integration

El Repository no conoce:

```text
Municipal API

FIWARE

NGSI-LD

External Participation Platform

Notification Provider
```

Las integraciones se coordinan fuera del Repository.

---

# Repository y HTTP

El contrato no utiliza semántica HTTP como parte del dominio.

No debe definir sus resultados conceptualmente mediante:

```text
200

404

409

500
```

Estas traducciones pertenecen a Adapters externos.

El dominio utiliza conceptos como:

```text
NotFound

ConcurrencyConflict

PersistenceFailure
```

---

# Repository y ORM

Un ORM puede ser utilizado por Infrastructure.

El Aggregate no debe convertirse obligatoriamente en una entidad
ORM.

Debe mantenerse:

```text
Domain Aggregate

≠

ORM Entity
```

cuando el acoplamiento comprometa la independencia del dominio.

---

# Lazy Loading

El Repository no debe introducir referencias mutables a otros
Aggregates mediante Lazy Loading.

No debe ocurrir:

```text
Participation.Assembly

↓

Lazy Loaded Mutable Assembly Aggregate
```

Debe mantenerse la referencia mediante:

```text
AssemblyId
```

---

# Proxies de Persistencia

Los proxies técnicos no deben alterar el comportamiento observable
del Aggregate ni introducir dependencias del framework en el
dominio.

---

# Repository y Serialization Boundaries

La representación serializada puede evolucionar.

La semántica reconstruida debe continuar correspondiendo al
Aggregate oficial.

Debe mantenerse:

```text
Serialized Representation

↓

Mapper

↓

Participation Domain State
```

---

# Contract Testing

Toda implementación de ParticipationRepository debe poder
verificarse contra el mismo contrato conceptual.

Como mínimo deben comprobarse escenarios como:

```text
Save New Participation

Load Existing Participation

Participation Not Found

Preserve ParticipationId

Preserve OrganizationId

Preserve ParticipationType

Preserve ParticipationStatus

Preserve Domain References

Preserve Lifecycle Timestamps

Preserve Version

No Version Increment on Load

No Domain Event on Load

Save Modified Participation

Reject Duplicate Identity

Detect Concurrency Conflict

Prevent Silent Overwrite

Preserve Archived Participation

No Identity Reuse after Archive

Atomic Aggregate Persistence

Persistence Failure

Rehydrate Equivalent Aggregate

No External Aggregate Embedding

No Direct Partial Domain Update
```

---

# Test de Nueva Participation

Escenario:

```text
Participation Created

↓

save()

↓

Persisted
```

Posteriormente:

```text
getById(ParticipationId)

↓

Equivalent Participation
```

Debe preservarse todo el estado relevante.

---

# Test de NotFound

Escenario:

```text
Unknown ParticipationId

↓

getById()

↓

NotFound
```

No debe crearse una Participation automáticamente.

---

# Test de Version

Escenario:

```text
Persisted Version = 5

↓

getById()

↓

Version = 5
```

La lectura no produce:

```text
Version = 6
```

---

# Test de Concurrency

Escenario:

```text
Process A → Load Version 3

Process B → Load Version 3

Process A → Save Version 4

Process B → Save using ExpectedVersion 3
```

Resultado:

```text
ConcurrencyConflict
```

---

# Test de Archive

Escenario:

```text
ParticipationStatus = Archived

↓

save()

↓

getById()
```

Resultado:

```text
ParticipationStatus = Archived
```

con identidad e historia preservadas.

---

# Test de Atomicidad

Una modificación válida que altere:

```text
Status

Timestamp

Version
```

debe persistir esos cambios como una única unidad lógica.

No debe observarse una combinación parcial incompatible.

---

# Test de Referencias

Una Participation con:

```text
AssemblyId

ProposalId

CitizenId
```

debe recuperar esas mismas identidades sin convertirlas en
Aggregates embebidos.

---

# Test de Rehidratación

La rehidratación debe producir:

```text
Equivalent Domain State
```

sin:

```text
New Domain Events

New Version Increment

New Lifecycle Timestamps
```

---

# Test de Implementaciones

Las implementaciones:

```text
InMemory

Relational

Document

EventSourced
```

cuando existan, deben mantener la misma semántica contractual.

Una diferencia tecnológica no puede cambiar el comportamiento
conceptual del Repository.

---

# Performance

El Repository puede ser optimizado por Infrastructure.

Las optimizaciones no deben comprometer:

- consistencia;
- Versioning;
- identidad;
- atomicidad;
- aislamiento del Aggregate;
- reconstrucción correcta;
- detección de conflictos.

Las reglas específicas se desarrollan en:

```text
DOMAIN-008N-Performance-Rules.md
```

---

# Security

La implementación debe proteger el acceso a persistencia según la
arquitectura de seguridad.

Sin embargo, el Repository Contract no incorpora credenciales ni
mecanismos concretos de autenticación.

La definición complementaria corresponde a:

```text
DOMAIN-008O-Security-Model.md
```

---

# Observabilidad

Infrastructure puede registrar:

```text
Repository Operation

Duration

Result

Concurrency Conflict

Persistence Failure

CorrelationId
```

La observabilidad no debe modificar el comportamiento del
Aggregate.

---

# Logging

Los logs pertenecen a Infrastructure.

El Repository Contract no exige que Participation conozca:

```text
Logger

Log Level

Tracing SDK

Metrics Provider
```

---

# Métricas

Pueden medirse:

```text
Load Latency

Save Latency

Conflict Rate

Failure Rate
```

Estas métricas no forman parte del estado del Aggregate.

---

# Trazabilidad

Cuando corresponda, las operaciones pueden correlacionarse mediante:

```text
CorrelationId

CausationId
```

sin convertir dichos mecanismos en identidad de Participation.

---

# Restricciones

No está permitido:

- modificar ParticipationId desde el Repository;
- modificar OrganizationId desde el Repository;
- modificar ParticipationStatus directamente desde el Repository;
- modificar Version arbitrariamente;
- modificar timestamps del Lifecycle arbitrariamente;
- crear Domain Events desde el Repository por iniciativa propia;
- ejecutar Commands desde el Repository;
- evaluar Permissions dentro del Repository;
- definir Invariants dentro del Repository;
- crear transiciones de Lifecycle dentro del Repository;
- corregir silenciosamente estados inválidos;
- persistir parcialmente una modificación del Aggregate;
- permitir sobrescrituras concurrentes silenciosas;
- reutilizar ParticipationId después de Archive;
- considerar Archive como inexistencia;
- convertir otros Aggregates en estado interno de Participation;
- utilizar Lazy Loading para introducir Aggregates mutables;
- exponer setters de persistencia para atributos protegidos;
- exponer `updateStatus()` como sustituto del comportamiento;
- exponer `updateVersion()` como operación externa;
- exponer `patchParticipation()` para evitar el Aggregate Root;
- utilizar Bulk Update para evitar Invariants;
- utilizar consultas analíticas como responsabilidad primaria del
  Repository;
- incorporar lógica de UI;
- incorporar lógica HTTP;
- incorporar lógica de reportes;
- depender de un ORM concreto desde el dominio;
- depender de una base de datos concreta desde el dominio;
- depender de FIWARE desde el Repository Contract;
- ampliar el límite transaccional a otros Aggregates;
- utilizar transacciones distribuidas como requisito normal;
- ocultar ConcurrencyConflict como éxito;
- reportar persistencia exitosa cuando el commit no ocurrió;
- generar modificaciones durante `getById()`;
- incrementar Version durante rehidratación;
- volver a ejecutar Commands durante replay;
- volver a evaluar Permissions durante replay.

---

# Matriz de Operaciones

```text
Operation      Modifies Aggregate   Changes Version   Emits Domain Event

getById()      No                   No                No

exists()       No                   No                No

save()         Persists State       No New Domain     No New Domain
                                    Decision          Decision
```

`save()` persiste una modificación ya producida válidamente por el
Aggregate.

No constituye por sí mismo una nueva modificación de dominio.

---

# Matriz de Responsabilidades

```text
Responsibility                     Authority

Participation Identity             Participation Aggregate

Organization Ownership             Participation Aggregate

Lifecycle                          Participation Aggregate

State Transitions                  Participation Aggregate

Invariants                         Participation Aggregate

Permissions                        Authorization Capability

Command Orchestration              Application Layer

Aggregate Persistence              ParticipationRepository

Concurrency Persistence Check      ParticipationRepository

Version Domain Evolution           Participation Aggregate

Read Projections                   Read Side

Analytics                          Read Side

External Integration               Integration Layer

Audit                              Audit Context
```

---

# Matriz de Persistencia

```text
Concept                            Repository Responsibility

ParticipationId                    Preserve

OrganizationId                     Preserve

ParticipationType                  Preserve

ParticipationStatus                Preserve

Domain References                  Preserve

Metadata                           Preserve when part of Aggregate

Lifecycle Timestamps               Preserve

Version                            Preserve and validate

Domain Behavior                    No

Permissions                        No

State Machine Definition           No

Read Model                         No

External Aggregates                No

Authentication Credentials         No
```

---

# Flujo de Creación

```text
RegisterParticipation

↓

Authorization

↓

Participation.create()

↓

Invariant Validation

↓

ParticipationRegistered

↓

ParticipationRepository.save()

↓

Persisted
```

El Repository no crea la decisión de registrar.

Persiste el resultado válido.

---

# Flujo de Modificación

```text
ParticipationRepository.getById()

↓

Participation

↓

Command

↓

Domain Behavior

↓

Invariant Validation

↓

State Change

↓

Version Increment

↓

Domain Event

↓

ParticipationRepository.save()

↓

Persisted
```

---

# Flujo de Conflicto

```text
Load Version N

↓

Domain Change

↓

New Version N + 1

↓

save(ExpectedVersion = N)

↓

PersistedVersion ≠ N

↓

ConcurrencyConflict
```

---

# Flujo de Lectura CQRS

```text
Query

↓

Participation Read Model
```

No:

```text
Query

↓

Load Thousands of Participation Aggregates

↓

Build Dashboard
```

como patrón normal de lectura.

---

# Flujo de Rehidratación

```text
Persisted State / Event Stream

↓

ParticipationRepository

↓

Rehydrate

↓

Participation
```

sin:

```text
Permission Evaluation

Command Execution

New Domain Event

New Version Increment
```

---

# Reglas No Negociables

Las siguientes reglas constituyen principios fundamentales del
Repository Contract:

```text
Repository

=

Aggregate Persistence Abstraction
```

```text
Repository

≠

Database
```

```text
Repository

≠

ORM
```

```text
Repository

≠

Read Model
```

```text
Repository

≠

Domain Service
```

```text
Repository

≠

Authorization Engine
```

```text
Repository

≠

State Machine
```

```text
Repository

≠

Reporting Engine
```

```text
Load

≠

Domain Modification
```

```text
Save

≠

New Domain Decision
```

```text
Archive

≠

Delete
```

```text
Persistence Model

≠

Domain Model
```

```text
Concurrency Conflict

≠

Silent Overwrite
```

```text
Participation Reference

=

AggregateId
```

```text
External Aggregate

≠

Embedded Mutable State
```

---

# Compatibilidad con DDD

El Repository Contract cumple Domain-Driven Design porque:

- trabaja con Aggregate Roots;
- preserva el límite de consistencia;
- utiliza identidad de dominio;
- abstrae persistencia;
- mantiene Infrastructure fuera del dominio;
- evita operaciones parciales sobre estado interno;
- respeta independencia entre Aggregates.

---

# Compatibilidad con Clean Architecture

La dependencia apunta hacia la abstracción.

Debe mantenerse:

```text
Domain / Application

↓

Repository Contract
```

mientras:

```text
Infrastructure

↓

Implements Repository Contract
```

El dominio no depende de Infrastructure.

---

# Compatibilidad con Hexagonal Architecture

ParticipationRepository constituye conceptualmente un Port de
persistencia.

Las implementaciones concretas constituyen Adapters.

Debe mantenerse:

```text
Participation Domain

↓

Repository Port

←

Persistence Adapter
```

---

# Compatibilidad con CQRS

El Repository pertenece al Write Side.

Las consultas especializadas pertenecen al Read Side.

Debe mantenerse:

```text
Write

↓

Aggregate Repository
```

```text
Read

↓

Read Models
```

---

# Compatibilidad con Event Sourcing

El contrato puede implementarse mediante persistencia de eventos
cuando corresponda.

Debe preservar:

- ParticipationId;
- orden histórico;
- Version;
- reconstrucción;
- ausencia de nuevos eventos durante replay.

---

# Compatibilidad con Event-Driven Architecture

El Repository persiste el estado asociado a decisiones válidas del
dominio.

La publicación y distribución de eventos se coordina mediante los
mecanismos establecidos por la arquitectura sin convertir al
Repository en propietario conceptual de los eventos.

---

# Compatibilidad con Arquitectura Distribuida

Cada Participation mantiene su propio límite de consistencia.

El Repository no requiere transacciones distribuidas entre
Aggregates.

La coordinación externa puede utilizar consistencia eventual.

---

# Evolución

El Repository Contract puede evolucionar cuando aparezca una nueva
necesidad real de persistencia del Aggregate.

Una nueva operación debe evaluarse contra las siguientes preguntas:

```text
Does it operate on Participation Aggregate?

Is it required for domain behavior?

Does it preserve Aggregate Boundary?

Does it avoid Read Model responsibilities?

Does it avoid Infrastructure leakage?

Does it preserve Versioning?

Does it preserve Invariants?
```

Si la operación corresponde principalmente a:

```text
Search

Filtering

Pagination

Reporting

Analytics

Dashboard
```

debe evaluarse primero como responsabilidad del Read Side.

---

# Extension Points

Las futuras extensiones del Repository Contract deben respetar:

- Aggregate Root;
- ParticipationId;
- OrganizationId;
- Lifecycle;
- State Machine;
- Invariants;
- Versioning;
- Consistency Boundary;
- independencia tecnológica;
- separación CQRS;
- separación entre Aggregates.

Las extensiones formales se documentan en:

```text
DOMAIN-008P-Extension-Points.md
```

---

# Documentación Complementaria

El Repository Contract debe interpretarse conjuntamente con:

```text
DOMAIN-008-Aggregate.md

DOMAIN-008A-Lifecycle.md

DOMAIN-008B-State-Machine.md

DOMAIN-008C-Commands.md

DOMAIN-008D-Domain-Events.md

DOMAIN-008E-Invariants.md

DOMAIN-008F-Permissions.md

DOMAIN-008I-Versioning.md

DOMAIN-008J-Consistency-Boundary.md

DOMAIN-008K-Integration-Events.md

DOMAIN-008L-Read-Model.md

DOMAIN-008M-Test-Scenarios.md

DOMAIN-008N-Performance-Rules.md

DOMAIN-008O-Security-Model.md

DOMAIN-008P-Extension-Points.md
```

Cada documento desarrolla una responsabilidad específica sin
redefinir el contrato establecido en este archivo.

---

# Principios Arquitectónicos

El modelo oficial del Repository de Participation mantiene:

```text
Application

↓

ParticipationRepository.getById()

↓

Participation Aggregate

↓

Domain Behavior

↓

Invariant Protection

↓

Version Increment

↓

Domain Event

↓

ParticipationRepository.save()
```

El Repository preserva:

```text
Identity

State

References

Lifecycle Timestamps

Version

Consistency Boundary
```

El Repository no decide:

```text
Authorization

Lifecycle

State Transitions

Invariants

Domain Behavior

Integration Behavior

Read Projections
```

---

# Definición de Éxito

El `ParticipationRepository` constituye el contrato oficial de
persistencia del Aggregate **Participation** dentro de AURA Core.

El contrato garantiza que:

- Participation se recupera y persiste como Aggregate completo;
- ParticipationId permanece como identidad oficial;
- OrganizationId permanece preservado e inmutable;
- las referencias hacia otros Aggregates permanecen expresadas
  mediante identificadores;
- el Repository no absorbe Aggregates externos;
- las modificaciones se persisten como unidades lógicas de
  consistencia;
- la recuperación no constituye una nueva modificación;
- la rehidratación no incrementa Version;
- la rehidratación no genera nuevos Domain Events;
- Version se preserva y participa en el control de concurrencia;
- los conflictos concurrentes no producen sobrescrituras
  silenciosas;
- Archive permanece diferenciado de Delete;
- las consultas analíticas permanecen separadas mediante CQRS;
- Infrastructure puede evolucionar sin modificar el modelo de
  dominio;
- el contrato permanece compatible con persistencia tradicional y
  Event Sourcing;
- el Repository no asume responsabilidades de Authorization,
  Lifecycle, State Machine, Invariants, Audit o Integration;
- el límite de consistencia de Participation permanece protegido.

La regla fundamental es:

```text
ParticipationRepository

=

Load Aggregate

+

Persist Valid Aggregate

+

Preserve Identity

+

Preserve Version

+

Protect Persistence Concurrency

+

Respect Consistency Boundary
```

y nunca:

```text
ParticipationRepository

=

Domain Behavior

+

Authorization

+

State Machine

+

Read Model

+

External Aggregate Coordination
```

De esta forma,
`DOMAIN-008G-Repository-Contract.md` constituye la definición
conceptual y normativa oficial del contrato de persistencia del
Aggregate **Participation**, manteniendo independencia tecnológica,
consistencia transaccional, control de concurrencia, separación
CQRS y respeto estricto por los límites DDD consolidados de
AURA Core.