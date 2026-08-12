# DOMAIN-006G — Assembly Repository Contract

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Assembly Management

Aggregate:
Assembly

Autor:
ARADA

Documentos relacionados:

* DOMAIN-006-Aggregate.md
* DOMAIN-006A-Lifecycle.md
* DOMAIN-006B-State-Machine.md
* DOMAIN-006C-Commands.md
* DOMAIN-006D-Domain-Events.md
* DOMAIN-006E-Invariants.md
* DOMAIN-006F-Permissions.md
* DOMAIN-006I-Versioning.md
* DOMAIN-006J-Consistency-Boundary.md
* DOMAIN-006K-Integration-Events.md
* DOMAIN-006L-Read-Model.md
* DOMAIN-006M-Test-Scenarios.md
* DOMAIN-006N-Performance-Rules.md
* DOMAIN-006O-Security-Model.md
* DOMAIN-006P-Extension-Points.md
* CORE-003-Shared-Kernel.md
* CORE-006-Domain-Invariants.md
* CORE-008-Aggregate-Design-Rules.md
* CORE-011-Repository-Contracts.md

---

# Objetivo

Definir formalmente el contrato conceptual del **Repository** del
Aggregate **Assembly**.

El Repository constituye la abstracción mediante la cual el
dominio puede recuperar y persistir una Assembly sin conocer la
tecnología utilizada para almacenar su estado.

El Repository trabaja con la Aggregate Root completa y respeta el
límite de consistencia definido por Assembly.

No representa:

* una tabla;
* una colección física;
* un ORM;
* un DAO;
* una API;
* un cliente de base de datos;
* un motor general de consultas;
* un servicio de integración;
* un servicio de autorización;
* una capa de aplicación.

Su responsabilidad consiste en proporcionar al dominio la ilusión
conceptual de una colección de Aggregates Assembly identificados
mediante:

```text
AssemblyId
```

---

# Propósito

El Repository permite mantener separadas:

```text
Domain
```

e:

```text
Infrastructure
```

El dominio expresa operaciones conceptuales sobre Assembly.

Infrastructure determina cómo dichas operaciones son
materializadas técnicamente.

Conceptualmente:

```text
Application Layer
      │
      ▼
AssemblyRepository
      │
      ▼
Assembly
```

Mientras que la implementación concreta puede utilizar:

```text
AssemblyRepository
      │
      ▼
Repository Adapter
      │
      ▼
Persistence Technology
```

El dominio conoce el contrato.

El dominio no conoce la implementación concreta.

---

# Principio Fundamental

El Repository existe para administrar la persistencia de la
Aggregate Root:

```text
Assembly
```

Debe mantenerse:

```text
Repository
    │
    ▼
Aggregate Root
```

Nunca:

```text
Repository
    │
    ├── AssemblySchedule
    ├── Convocation
    ├── AssemblyRule
    └── AssemblyLocation
```

como raíces independientes del dominio.

Las entidades internas y Value Objects pertenecientes a Assembly
se recuperan y persisten como parte de una única unidad de
consistencia.

---

# Aggregate Root Administrada

La única Aggregate Root administrada por este Repository es:

```text
Assembly
```

El Repository no administra directamente:

```text
Organization

Territory

Membership

Citizen

Role

Proposal

Participation

Voting

Document

Notification

Audit

Integration
```

Cada uno de estos conceptos mantiene su propio Aggregate,
Repository o Bounded Context cuando corresponda.

---

# Unidad Conceptual de Persistencia

Desde la perspectiva del dominio:

```text
Assembly
```

se persiste como una unidad.

Esto incluye todos los conceptos internos necesarios para
reconstruir su estado consistente.

Ejemplos conceptuales:

```text
AssemblySchedule

Convocation

AssemblyRule

AssemblyLocation

ExecutionConditions
```

Una implementación física puede distribuir estos datos entre
múltiples estructuras de almacenamiento.

Esa decisión no modifica el límite del Aggregate.

---

# Identidad del Repository

La identidad utilizada para recuperar una Assembly es:

```text
AssemblyId
```

AssemblyId constituye la identidad oficial del Aggregate.

El Repository no debe utilizar como identidad conceptual:

```text
AssemblyName

OrganizationId

TerritoryId

ScheduledStartAt

AssemblyStatus

ExternalId
```

Estos valores pueden utilizarse para índices o consultas
auxiliares.

Nunca sustituyen AssemblyId como identidad.

---

# Contrato Conceptual

El Repository expone conceptualmente las siguientes operaciones
mínimas:

```text
get_by_id()

save()

exists()
```

El contrato debe permanecer reducido a las necesidades reales del
dominio.

No debe convertirse en un catálogo general de operaciones de
persistencia.

---

# AssemblyRepository

El contrato conceptual puede representarse como:

```text
AssemblyRepository

    get_by_id(
        assembly_id: AssemblyId
    ) -> Assembly | AssemblyNotFound

    save(
        assembly: Assembly,
        expected_version: Version
    ) -> PersistedAssembly
       | AssemblyAlreadyExists
       | AssemblyConcurrencyConflict
       | AssemblyPersistenceFailure

    exists(
        assembly_id: AssemblyId
    ) -> bool
```

Esta representación es conceptual.

No prescribe una interfaz concreta de programación.

La implementación definitiva dependerá del lenguaje y de la
arquitectura técnica utilizada.

---

# get_by_id

## Objetivo

Recuperar una Assembly mediante su identidad.

Entrada:

```text
AssemblyId
```

Resultado conceptual:

```text
Assembly
```

o:

```text
AssemblyNotFound
```

---

# Reglas de get_by_id

La operación debe:

* utilizar AssemblyId como identidad;
* recuperar el estado necesario del Aggregate;
* reconstruir una Assembly válida;
* preservar AssemblyId;
* preservar OrganizationId;
* preservar Version;
* preservar AssemblyStatus;
* preservar timestamps históricos;
* preservar Value Objects;
* preservar entidades internas;
* no modificar el Aggregate;
* no incrementar Version;
* no producir Domain Events nuevos;
* no ejecutar Commands;
* no cargar otros Aggregates dentro de Assembly.

---

# AssemblyNotFound

Cuando AssemblyId no corresponda a una Assembly existente,
`get_by_id()` debe expresar explícitamente:

```text
AssemblyNotFound
```

La ausencia del Aggregate no debe representarse mediante:

```text
null aggregate
```

ni mediante:

```text
empty Assembly
```

ni mediante una Assembly parcialmente inicializada.

La ausencia de un Aggregate es conceptualmente diferente de una
Assembly existente con propiedades opcionales.

---

# Rehidratación

La recuperación desde persistencia implica reconstruir el
Aggregate desde un estado previamente aceptado.

Este proceso se denomina conceptualmente:

```text
Rehydration
```

La rehidratación no representa creación.

Debe mantenerse:

```text
Create Assembly
        ≠
Rehydrate Assembly
```

---

# Creación

La creación:

* establece una nueva identidad;
* establece OrganizationId;
* valida invariantes iniciales;
* crea el estado Draft;
* inicializa Version;
* establece CreatedAt;
* produce AssemblyCreated.

---

# Rehidratación

La rehidratación:

* recupera una identidad existente;
* recupera OrganizationId existente;
* recupera estado existente;
* recupera Version existente;
* recupera timestamps históricos;
* recupera configuración;
* recupera entidades internas;
* no representa un nuevo hecho de dominio;
* no produce AssemblyCreated.

---

# Rehidratación sin Domain Events Nuevos

El Repository no debe provocar durante la rehidratación:

```text
AssemblyCreated

AssemblyScheduled

AssemblyRescheduled

AssemblyConvoked

AssemblyStarted

AssemblyCompleted

AssemblyCancelled

AssemblyArchived
```

ni ningún otro Domain Event nuevo.

Recuperar un hecho persistido no significa que ese hecho vuelva a
ocurrir.

---

# Estado Rehidratado

El Repository debe reconstruir toda la información necesaria para
que Assembly continúe protegiendo sus invariantes.

Conceptualmente puede incluir:

```text
AssemblyId

OrganizationId

TerritoryId

AssemblyName

AssemblyType

AssemblyPurpose

AssemblyDescription

AssemblySchedule

AssemblyModality

AssemblyLocation

Convocation

AssemblyRules

ExecutionConditions

AssemblyStatus

CreatedAt

UpdatedAt

ConvokedAt

StartedAt

CompletedAt

CancelledAt

ArchivedAt

Version
```

La estructura física de persistencia puede diferir.

El modelo conceptual no depende de dicha representación.

---

# Estado Persistido Válido

El Repository no debe utilizar la persistencia para introducir un
estado imposible dentro del dominio.

Una Assembly rehidratada debe corresponder a un estado válido
según:

```text
DOMAIN-006E-Invariants.md
```

Si la persistencia contiene un estado incompatible con el modelo
vigente, debe producirse un error explícito de reconstrucción o
compatibilidad.

No debe corregirse silenciosamente.

---

# Ejemplo de Estado Persistido Inválido

Ejemplo:

```text
AssemblyStatus = InProgress

StartedAt = null
```

Este estado viola las invariantes.

El Repository no debe fabricar automáticamente un StartedAt.

Debe reportar una inconsistencia de rehidratación.

---

# AssemblyRehydrationFailure

Cuando un estado persistido no pueda reconstruirse de manera
segura como una Assembly válida debe producirse conceptualmente:

```text
AssemblyRehydrationFailure
```

No debe devolverse un Aggregate parcialmente válido.

---

# exists

## Objetivo

Determinar si existe una Assembly con una identidad determinada.

Entrada:

```text
AssemblyId
```

Resultado:

```text
true

false
```

---

# Reglas de exists

La operación:

```text
exists()
```

no debe:

* modificar Assembly;
* incrementar Version;
* generar Domain Events;
* crear una Assembly;
* ejecutar comportamiento de dominio;
* cargar necesariamente el Aggregate completo.

Su implementación puede utilizar mecanismos optimizados siempre
que preserve su semántica.

---

# Uso de exists

`exists()` puede utilizarse durante creación para detectar si:

```text
AssemblyId
```

ya se encuentra utilizado.

Sin embargo, `exists()` por sí solo no constituye una garantía
suficiente frente a concurrencia.

---

# Condición de Carrera en Creación

Puede ocurrir:

```text
Process A
    exists() = false

Process B
    exists() = false
```

antes de que alguno persista.

Por ello la infraestructura debe garantizar finalmente la
unicidad de:

```text
AssemblyId
```

durante la operación de persistencia.

---

# Unicidad Definitiva

Debe existir una garantía final equivalente a:

```text
one Assembly
per AssemblyId
```

La forma técnica puede ser:

* unique constraint;
* primary key;
* unique document identifier;
* stream identity;
* conditional write.

La técnica no forma parte del contrato conceptual.

---

# AssemblyAlreadyExists

Cuando se intente persistir una nueva Assembly con un AssemblyId
ya utilizado debe producirse:

```text
AssemblyAlreadyExists
```

No debe sobrescribirse silenciosamente la Assembly existente.

---

# save

## Objetivo

Persistir el estado válido de una Assembly.

Entrada conceptual:

```text
Assembly

ExpectedVersion
```

Resultado conceptual:

```text
PersistedAssembly
```

o un error explícito.

---

# Reglas de save

`save()` debe:

* recibir una Aggregate Root válida;
* persistir Assembly como unidad;
* preservar AssemblyId;
* preservar OrganizationId;
* validar ExpectedVersion;
* impedir pérdida silenciosa de actualizaciones;
* persistir la nueva Version;
* respetar atomicidad;
* preservar timestamps;
* preservar Value Objects;
* preservar entidades internas;
* no ejecutar comportamiento de dominio;
* no modificar otros Aggregates;
* no corregir invariantes silenciosamente;
* no publicar directamente Integration Events externos.

---

# PersistedAssembly

`PersistedAssembly` representa conceptualmente la confirmación de
que el estado del Aggregate fue persistido correctamente.

Puede contener como mínimo:

```text
AssemblyId

Version
```

y metadatos estrictamente necesarios.

No representa un segundo Aggregate.

No sustituye Assembly.

---

# Repository no Ejecuta Commands

El Repository no debe exponer comportamiento como:

```text
start_assembly()

complete_assembly()

cancel_assembly()

archive_assembly()

convoke_assembly()
```

Estos comportamientos pertenecen a Assembly.

El flujo correcto es:

```text
Repository
    │
    ▼
get_by_id()
    │
    ▼
Assembly
    │
    ▼
assembly.start()
    │
    ▼
Repository.save()
```

Nunca:

```text
Repository.start_assembly()
```

---

# Repository no Modifica Estado Directamente

No deben existir operaciones conceptuales como:

```text
update_status()

update_name()

update_location()

set_started_at()

set_completed_at()

increment_version()
```

para modificar directamente partes del Aggregate.

Estas operaciones evadirían:

* Aggregate Root;
* State Machine;
* Guards;
* invariantes;
* Domain Events;
* Versioning;
* Consistency Boundary.

---

# No Setters mediante Persistencia

No debe utilizarse el Repository como sustituto de setters
públicos.

Ejemplo prohibido:

```text
repository.update_status(
    assembly_id,
    "Completed"
)
```

como implementación de:

```text
CompleteAssembly
```

La transición debe ocurrir dentro de Assembly.

---

# Unidad de Persistencia

Assembly constituye la unidad conceptual de persistencia.

Debe mantenerse:

```text
save(Assembly)
```

No:

```text
save(AssemblySchedule)

save(Convocation)

save(AssemblyRule)

save(ExecutionConditions)
```

como operaciones independientes del Repository del dominio.

---

# Persistencia Física

Una implementación puede almacenar Assembly en:

```text
one table

multiple tables

one document

multiple documents

event stream

distributed persistence structures
```

siempre que preserve:

* identidad;
* atomicidad;
* Version;
* consistencia;
* Aggregate Boundary.

La estructura física no redefine DDD.

---

# Consistency Boundary

El Repository debe respetar:

```text
DOMAIN-006J-Consistency-Boundary.md
```

Assembly constituye un único límite de consistencia.

Todo estado persistido debe representar una Assembly internamente
válida.

---

# Atomicidad

Cuando una modificación afecta múltiples partes internas del
Aggregate, todas deben persistirse como una única modificación
lógica.

Ejemplo:

```text
StartAssembly
```

puede producir:

```text
AssemblyStatus = InProgress

StartedAt = T

UpdatedAt = T

Version = N + 1
```

Estas propiedades deben confirmarse conjuntamente.

---

# Estado Parcial Prohibido

No debe quedar persistido:

```text
AssemblyStatus = InProgress

StartedAt = null
```

después de un inicio exitoso.

Tampoco:

```text
AssemblyStatus = Archived

ArchivedAt = null
```

después de un archivado exitoso.

---

# Transacción Conceptual

La implementación debe proporcionar atomicidad equivalente a:

```text
BEGIN

validate expected version

persist aggregate state

persist required event records

COMMIT
```

o:

```text
ROLLBACK
```

La tecnología concreta no forma parte del contrato.

---

# Todo o Nada

Debe mantenerse:

```text
all Aggregate changes committed
```

o:

```text
no Aggregate changes committed
```

Una persistencia parcial constituye una violación del contrato.

---

# Repository y Versioning

Assembly utiliza:

```text
Version
```

para concurrencia optimista.

El Repository debe respetar:

```text
DOMAIN-006I-Versioning.md
```

---

# ExpectedVersion

Toda persistencia de una Assembly existente debe validar:

```text
ExpectedVersion
```

contra:

```text
PersistedVersion
```

Debe cumplirse:

```text
ExpectedVersion
=
PersistedVersion
```

antes de aceptar una nueva versión.

---

# AssemblyConcurrencyConflict

Si:

```text
ExpectedVersion
≠
PersistedVersion
```

debe producirse:

```text
AssemblyConcurrencyConflict
```

No debe sobrescribirse silenciosamente un estado más reciente.

---

# Lost Update Prevention

El Repository debe impedir el escenario:

```text
Assembly Version = 5

Actor A loads Version 5

Actor B loads Version 5
```

Actor A modifica y persiste:

```text
Version = 6
```

Actor B no puede sobrescribir esa versión utilizando todavía:

```text
ExpectedVersion = 5
```

Debe recibir:

```text
AssemblyConcurrencyConflict
```

---

# Last Write Wins Prohibido

No se permite:

```text
last write wins
```

como estrategia silenciosa para modificaciones del Aggregate.

Una pérdida de actualización rompería:

* consistencia;
* Versioning;
* trazabilidad;
* Domain Events;
* intención del Actor.

---

# Incremento de Version

La modificación válida del Aggregate determina una nueva Version.

El Repository persiste la versión resultante.

No debe inventar arbitrariamente una versión diferente.

---

# Version en Creación

La versión inicial debe seguir la regla oficial definida en:

```text
DOMAIN-006I-Versioning.md
```

El Repository debe aplicar la misma convención para todas las
Assemblies.

---

# No Incremento por Lectura

`get_by_id()` no modifica Version.

`exists()` no modifica Version.

Las consultas no representan evolución del Aggregate.

---

# No Incremento por Persistencia sin Cambio

Guardar una representación sin cambio semántico no debe utilizarse
para crear versiones artificiales.

La política exacta debe mantenerse consistente con
DOMAIN-006I-Versioning.md.

---

# Repository y Domain Events

Assembly produce Domain Events como consecuencia de comportamiento
válido.

El Repository no inventa estos eventos.

Debe mantenerse:

```text
Assembly
    │
    ▼
Domain Behavior
    │
    ▼
Domain Events
```

No:

```text
Repository
    │
    ▼
business event creation
```

---

# Domain Events Pendientes

Assembly puede mantener temporalmente:

```text
PendingDomainEvents
```

después de ejecutar comportamiento válido.

La estrategia de persistencia debe coordinar estos eventos con la
persistencia del Aggregate.

---

# Consistencia Estado-Evento

La arquitectura debe evitar:

```text
Aggregate persisted
Domain Event lost
```

y:

```text
Domain Event externally published
Aggregate persistence failed
```

como estado normal del sistema.

---

# Transactional Outbox

Puede utilizarse:

```text
Transactional Outbox
```

para persistir conjuntamente:

```text
Aggregate State

Outbox Records
```

dentro de una misma transacción.

Después:

```text
Outbox Dispatcher
```

publica los mensajes correspondientes.

Assembly no conoce la Outbox.

---

# Outbox no Pertenece al Dominio

La Outbox:

* no es una entidad de Assembly;
* no es un Value Object;
* no es parte del Lifecycle;
* no forma parte del Repository Contract conceptual.

Es una estrategia de Infrastructure para entrega confiable.

---

# Event Store

Una implementación Event Sourced puede utilizar:

```text
Event Store
```

como mecanismo de persistencia.

En ese caso AssemblyRepository continúa manteniendo la misma
semántica conceptual.

---

# Event Sourcing

Conceptualmente:

```text
get_by_id(AssemblyId)
```

puede:

1. recuperar eventos históricos;
2. ordenarlos;
3. aplicar los eventos;
4. reconstruir Assembly;
5. establecer Version.

---

# Rehidratación desde Event Stream

Aplicar eventos históricos no debe agregar esos eventos como
eventos pendientes nuevos.

Debe mantenerse:

```text
historical event application
        ≠
new domain event generation
```

---

# Event Stream Identity

El stream de una Assembly debe corresponder inequívocamente a:

```text
AssemblyId
```

La representación física del nombre del stream pertenece a
Infrastructure.

---

# Event Stream Version

Cuando se utilice Event Sourcing, la posición del stream debe
mantener coherencia con:

```text
Assembly.Version
```

según la política oficial adoptada.

---

# Snapshot

Una implementación Event Sourced puede utilizar:

```text
Snapshot
```

para optimizar la reconstrucción.

Un Snapshot:

* representa un estado derivado;
* posee una Version;
* puede descartarse;
* puede reconstruirse;
* no reemplaza la identidad del Aggregate;
* no altera Domain Events históricos.

---

# Repository y Domain Event History

En persistencia de estado tradicional, AssemblyRepository no
necesita cargar todo el historial de Domain Events para reconstruir
el Aggregate.

La estrategia depende del modelo de persistencia adoptado.

---

# Repository y Integration Events

El Repository no publica directamente Integration Events de
negocio hacia sistemas externos.

Debe mantenerse:

```text
Assembly
    │
    ▼
Domain Event
    │
    ▼
Application / Integration Layer
    │
    ▼
Integration Event
```

---

# Repository no Integra FIWARE

No debe contener:

```text
sync_fiware()

publish_ngsi_ld()

update_context_broker()
```

Estas operaciones pertenecen a Integration.

---

# Repository no Integra Municipalidad

No debe contener:

```text
send_to_municipality()

call_municipal_api()
```

La persistencia de Assembly y la integración municipal son
responsabilidades distintas.

---

# Repository y Permissions

El Repository no administra autorización.

No debe determinar si un Actor posee:

```text
Assembly.Create

Assembly.Start

Assembly.Complete

Assembly.Cancel

Assembly.Archive
```

Los Permissions se definen en:

```text
DOMAIN-006F-Permissions.md
```

---

# Authorization fuera del Repository

No deben existir métodos conceptuales como:

```text
save_if_admin()

save_if_president()

load_if_authorized()
```

como parte del contrato de dominio.

La autorización debe resolverse antes de ejecutar comportamiento
protegido.

---

# Repository y Authentication

AssemblyRepository no:

* autentica Actors;
* valida passwords;
* valida JWT;
* valida OAuth;
* administra sesiones;
* resuelve Role;
* resuelve Membership;
* valida credenciales externas.

---

# Repository y Organization

Assembly mantiene:

```text
OrganizationId
```

El Repository de Assembly no debe cargar automáticamente:

```text
Organization
```

como parte interna del Aggregate.

---

# Repository y Territory

Assembly puede mantener:

```text
TerritoryId
```

El Repository no debe cargar automáticamente:

```text
Territory
```

como entidad interna de Assembly.

---

# Repository y Membership

Assembly puede relacionarse con:

```text
MembershipId
```

cuando corresponda.

Membership mantiene su propio Aggregate.

AssemblyRepository no debe persistir Membership.

---

# Repository y Citizen

Una referencia:

```text
CitizenId
```

no autoriza a AssemblyRepository a rehidratar Citizen dentro del
Aggregate.

---

# Repository y Role

Role permanece fuera de Assembly.

AssemblyRepository no carga Roles para reconstruir la reunión.

---

# Repository y Proposal

Una relación mediante:

```text
ProposalId
```

no convierte Proposal en parte de AssemblyRepository.

Proposal conserva:

* identidad;
* Repository;
* Lifecycle;
* invariantes.

---

# Repository y Participation

Participation mantiene su propia consistencia.

AssemblyRepository no administra Participation.

---

# Repository y Voting

Voting no forma parte del estado interno de Assembly.

AssemblyRepository no administra votos, resultados ni lifecycle de
Voting.

---

# Repository y Document

Document mantiene su propia identidad y almacenamiento.

AssemblyRepository no debe convertirse en Repository de
Documents.

---

# Repository y Notification

Guardar Assembly no significa enviar Notification.

Notification permanece bajo su propia responsabilidad.

---

# Repository y Audit

Audit conserva su propio límite.

AssemblyRepository puede participar técnicamente en trazabilidad
de persistencia, pero no administra el Aggregate Audit.

---

# Regla de No Absorción

El Repository no puede ampliar el Aggregate por conveniencia de
persistencia.

No debe ocurrir:

```text
AssemblyRepository
    ├── Assembly
    ├── Proposal
    ├── Voting
    ├── Document
    ├── Notification
    └── Audit
```

como una única unidad conceptual.

La facilidad de un JOIN, documento embebido o consulta no redefine
los límites DDD.

---

# Cross-Aggregate Persistence

Una operación sobre Assembly no debe utilizar AssemblyRepository
para persistir simultáneamente:

```text
Organization

Territory

Membership

Citizen

Role

Proposal

Participation

Voting

Document

Notification

Audit
```

como una única transacción de Aggregate.

---

# Transacciones Distribuidas

AssemblyRepository no exige transacciones distribuidas entre
Aggregates.

La coordinación externa debe utilizar cuando corresponda:

```text
Application Services

Domain Events

Integration Events

Process Managers

Sagas

Eventual Consistency
```

---

# Repository versus Read Model

Debe mantenerse:

```text
Repository
    │
    ▼
Aggregate Persistence
```

y:

```text
Read Model
    │
    ▼
Query Optimization
```

No son la misma responsabilidad.

---

# CQRS

En CQRS:

```text
Write Side
    │
    ▼
AssemblyRepository
```

Mientras:

```text
Read Side
    │
    ▼
AssemblyReadModel
```

El Repository protege el Write Model.

El Read Model optimiza consultas.

---

# Consultas Generales

Consultas como:

```text
list all assemblies

search assemblies

filter by status

filter by date

filter by territory

paginate

sort

full text search
```

pertenecen preferentemente al Read Model.

---

# Consultas de Dominio

Una operación adicional en el Repository solo debe incorporarse
cuando sea necesaria para:

* recuperar un Aggregate;
* persistir un Aggregate;
* proteger una invariante;
* resolver una necesidad real del Write Model.

No debe añadirse por conveniencia de UI.

---

# Consulta por Organization

Puede existir una necesidad legítima del dominio de localizar una
Assembly dentro de una Organization.

Sin embargo, la simple necesidad de mostrar todas las Assemblies
de una Organization pertenece normalmente al Read Model.

---

# exists_by...

No deben agregarse operaciones como:

```text
exists_by_name()

exists_by_status()

exists_by_date()
```

salvo que exista una invariante formal que requiera dicha
verificación.

---

# Unicidad de Negocio

Si en el futuro el dominio define una nueva regla como:

```text
one active Assembly
with specific code
per Organization
```

podría requerirse una operación especializada de Repository.

Dicha operación deberá incorporarse formalmente junto con la
invariante correspondiente.

---

# No Repository Genérico como Modelo Conceptual

Debe evitarse reducir el contrato a:

```text
Repository<T>
```

si con ello se pierde semántica importante.

La infraestructura puede compartir abstracciones internas.

El contrato conceptual pertenece específicamente a Assembly.

---

# CRUD no Representa el Dominio

Assembly no debe reducirse a:

```text
Create

Read

Update

Delete
```

El dominio posee comportamiento explícito.

El Repository solo persiste el resultado de dicho comportamiento.

---

# Delete

AssemblyRepository no expone conceptualmente:

```text
delete(assembly_id)
```

como operación ordinaria del dominio.

Assembly posee Lifecycle.

---

# Cancelled

Una Assembly:

```text
Cancelled
```

continúa existiendo.

No debe eliminarse físicamente como consecuencia automática de
CancelAssembly.

---

# Archived

Una Assembly:

```text
Archived
```

continúa existiendo conceptualmente.

Debe mantenerse:

```text
Archived
≠
Deleted
```

---

# Eliminación Física

La eliminación física puede existir únicamente bajo políticas
externas extraordinarias.

Ejemplos:

* obligación legal;
* política de retención;
* protección de datos;
* mantenimiento controlado;
* proceso administrativo excepcional.

No representa comportamiento ordinario de Assembly.

---

# Soft Delete

No debe utilizarse:

```text
deleted = true
```

como sustituto silencioso de:

```text
AssemblyStatus = Archived
```

si ambos conceptos poseen semánticas diferentes.

---

# Repository y Timestamps

El Repository debe preservar timestamps pertenecientes al estado
del Aggregate.

Ejemplos:

```text
CreatedAt

UpdatedAt

ConvokedAt

StartedAt

CompletedAt

CancelledAt

ArchivedAt
```

No debe recalcularlos durante rehidratación.

---

# CreatedAt

CreatedAt representa el momento de creación.

No cambia al recuperar Assembly.

---

# UpdatedAt

UpdatedAt representa una modificación válida cuando forme parte
del modelo oficial.

Leer el Aggregate no debe modificar UpdatedAt.

---

# ConvokedAt

ConvokedAt representa un hecho histórico.

No debe regenerarse al recuperar una Assembly Convoked.

---

# StartedAt

StartedAt representa el momento efectivo en que la reunión
comenzó.

No puede sustituirse por:

```text
load timestamp
```

---

# CompletedAt

CompletedAt representa el momento de finalización real.

No debe reinterpretarse durante una persistencia posterior.

---

# CancelledAt

CancelledAt debe preservarse después de cancelación y archivado.

---

# ArchivedAt

ArchivedAt representa el momento del archivado.

Rehidratar una Assembly Archived no produce un nuevo ArchivedAt.

---

# Serialization

La serialización pertenece a Infrastructure.

El dominio no debe depender de:

```text
JSON

BSON

SQL rows

Protobuf

Avro

MessagePack
```

para expresar Assembly.

---

# Persistence Mapper

Infrastructure puede utilizar:

```text
Assembly
    │
    ▼
Persistence Mapper
    │
    ▼
Persistence Model
```

El Mapper traduce entre:

```text
Domain Model
```

y:

```text
Persistence Model
```

---

# Mapping Bidireccional

Debe existir correspondencia suficiente para:

```text
Assembly
    -> Persistence Model
```

y:

```text
Persistence Model
    -> Assembly
```

sin pérdida de significado relevante.

---

# Persistence Model

El Persistence Model puede contener:

* claves técnicas;
* columnas;
* documentos;
* índices;
* metadata de almacenamiento;
* claves de partición;
* timestamps técnicos.

Estos elementos no forman parte automáticamente del modelo de
dominio.

---

# ORM Entity versus Aggregate

Debe mantenerse:

```text
ORM Entity
≠
Domain Aggregate
```

El modelo de dominio no debe deformarse para satisfacer un ORM.

---

# MongoDB

Una implementación MongoDB puede almacenar Assembly como un
documento.

Eso no significa que Assembly sea conceptualmente un Mongo
Document.

---

# PostgreSQL

Una implementación PostgreSQL puede utilizar múltiples tablas.

Eso no convierte dichas tablas en entidades o Aggregates
independientes.

---

# Event Store

Una implementación Event Sourced puede utilizar un Event Store.

El contrato conceptual sigue siendo AssemblyRepository.

---

# Unit of Work

Infrastructure puede utilizar:

```text
UnitOfWork
```

para coordinar:

* carga;
* tracking;
* persistencia;
* Versioning;
* Outbox;
* commit.

UnitOfWork no pertenece al Aggregate.

---

# Identity Map

Puede utilizarse:

```text
Identity Map
```

para garantizar que dentro de una Unit of Work una AssemblyId
corresponda a una única instancia en memoria.

Esta es una optimización técnica.

---

# Lazy Loading

Debe evitarse Lazy Loading que permita a Assembly obtener
implícitamente otros Aggregates.

Ejemplo conceptualmente incorrecto:

```text
assembly.organization.memberships
```

si provoca carga transparente de Aggregates externos.

---

# Referencias Externas

Las referencias deben permanecer como:

```text
OrganizationId

TerritoryId

MembershipId

CitizenId

ProposalId

ParticipationId

VotingId

DocumentId
```

según corresponda.

No como proxies mutables hacia otros Aggregates.

---

# N+1 Queries

Problemas de N+1 deben resolverse en:

* Infrastructure;
* Query Layer;
* Read Models;
* proyecciones.

No absorbiendo otros Aggregates dentro de Assembly.

---

# Caching

Infrastructure puede utilizar caché para Assembly.

La caché no redefine la fuente de verdad.

---

# Reglas de Cache

La caché debe:

* preservar AssemblyId;
* preservar Version;
* evitar estados corruptos;
* respetar invalidación;
* no permitir pérdida de actualizaciones;
* no reemplazar Optimistic Concurrency.

---

# Cache Staleness

Una Assembly recuperada desde caché con Version obsoleta debe ser
detectada al intentar persistir.

Debe producir:

```text
AssemblyConcurrencyConflict
```

cuando corresponda.

---

# Cache Key

La clave conceptual principal puede basarse en:

```text
AssemblyId
```

La representación concreta pertenece a Infrastructure.

---

# Repository y Performance

Las optimizaciones pueden incluir:

* índices;
* caché;
* connection pooling;
* prepared statements;
* snapshots;
* partitioning;
* batching técnico de lectura;
* compresión;
* replicación.

Ninguna optimización puede violar:

* identidad;
* atomicidad;
* Versioning;
* invariantes;
* Consistency Boundary.

---

# Índices

Pueden existir índices físicos sobre:

```text
AssemblyId

OrganizationId

AssemblyStatus

ScheduledStartAt

TerritoryId
```

según necesidades técnicas.

Un índice no convierte un atributo en identidad del Aggregate.

---

# Partitioning

La persistencia puede particionarse por:

```text
OrganizationId
```

u otra estrategia.

El partition key no sustituye AssemblyId.

---

# Multi-Tenancy

Si Organization actúa como frontera de tenant, el Repository debe
preservar aislamiento entre Organizations.

Una Assembly perteneciente a:

```text
Organization A
```

no debe exponerse accidentalmente dentro del scope de:

```text
Organization B
```

cuando la estrategia de acceso requiera dicho aislamiento.

---

# Organization Scope

El Adapter puede utilizar OrganizationId como parte del contexto
técnico de acceso.

Esto no cambia la identidad de Assembly.

---

# Repository no Decide Permissions

El Repository puede aplicar aislamiento técnico.

No determina si un Actor posee:

```text
Assembly.Read

Assembly.Start

Assembly.Cancel
```

Esa responsabilidad corresponde al modelo de Authorization.

---

# Seguridad de Persistencia

Infrastructure debe proteger la persistencia contra:

* acceso no autorizado;
* modificación directa no controlada;
* corrupción;
* pérdida de datos;
* filtración;
* modificación cross-tenant;
* exposición de secretos.

---

# Repository no es el Único Security Boundary

La seguridad de persistencia no reemplaza:

```text
Authentication

Authorization

Domain Validation
```

Cada responsabilidad mantiene su propio límite.

---

# Error Contract

El Repository debe expresar errores conceptualmente
distinguibles.

Como mínimo:

```text
AssemblyNotFound

AssemblyAlreadyExists

AssemblyConcurrencyConflict

AssemblyPersistenceFailure

AssemblyRehydrationFailure
```

---

# AssemblyPersistenceFailure

Representa un fallo técnico que impide completar la persistencia.

No debe confundirse con:

```text
AssemblyInvariantViolation

InvalidAssemblyTransition

PermissionDenied

AssemblyConcurrencyConflict
```

---

# Domain Failure versus Repository Failure

Debe mantenerse:

```text
Domain Failure
        ≠
Repository Failure
```

Ejemplo de Domain Failure:

```text
StartAssembly from Draft
```

Ejemplo de Repository Failure:

```text
database unavailable
```

---

# Concurrency Failure versus Infrastructure Failure

Debe distinguirse:

```text
AssemblyConcurrencyConflict
```

de:

```text
AssemblyPersistenceFailure
```

El primero representa un conflicto esperado de concurrencia.

El segundo representa incapacidad técnica de persistir.

---

# Retry de Infrastructure Failure

Los fallos técnicos transitorios pueden admitir retries cuando sean
seguros.

La política técnica debe considerar:

* idempotencia;
* transacciones;
* side effects;
* CommandId;
* Domain Events;
* Outbox.

---

# Retry de Concurrency Conflict

Un:

```text
AssemblyConcurrencyConflict
```

no debe resolverse sobrescribiendo automáticamente la nueva
Version.

La Application Layer debe:

1. volver a cargar Assembly;
2. reevaluar la intención;
3. reevaluar Authorization;
4. reevaluar State Machine;
5. reevaluar invariantes;
6. decidir si corresponde un nuevo intento.

---

# Idempotencia

El Repository debe ser compatible con estrategias de idempotencia
de la Application Layer.

Sin embargo:

```text
CommandId
```

no sustituye:

```text
AssemblyId
```

Son identidades conceptualmente diferentes.

---

# Duplicate Save

Una repetición técnica de persistencia debe gestionarse sin crear
hechos de dominio artificiales.

El Repository no inventa Domain Events para cada llamada `save()`.

---

# Repository y Commands

Los Commands definidos en:

```text
DOMAIN-006C-Commands.md
```

no forman parte del estado de Assembly.

AssemblyRepository no es un Command Store.

---

# Flujo General de Command

```text
Command
    │
    ▼
Application Service
    │
    ▼
Authorization
    │
    ▼
Repository.get_by_id()
    │
    ▼
Assembly
    │
    ▼
Domain Behavior
    │
    ▼
Repository.save()
```

---

# CreateAssembly y Repository

Flujo conceptual:

```text
CreateAssembly
      │
      ▼
Authorization
      │
      ▼
Assembly.create()
      │
      ▼
Repository.exists()
      │
      ▼
Repository.save()
```

La garantía final de unicidad debe permanecer en la persistencia.

---

# ScheduleAssembly y Repository

```text
ScheduleAssembly
      │
      ▼
Repository.get_by_id()
      │
      ▼
assembly.schedule()
      │
      ▼
AssemblyScheduled
      │
      ▼
Repository.save(expected_version)
```

---

# ConvokeAssembly y Repository

```text
ConvokeAssembly
      │
      ▼
Repository.get_by_id()
      │
      ▼
assembly.convoke()
      │
      ▼
AssemblyConvoked
      │
      ▼
Repository.save(expected_version)
```

---

# StartAssembly y Repository

```text
StartAssembly
      │
      ▼
Repository.get_by_id()
      │
      ▼
assembly.start()
      │
      ▼
AssemblyStarted
      │
      ▼
Repository.save(expected_version)
```

---

# CompleteAssembly y Repository

```text
CompleteAssembly
      │
      ▼
Repository.get_by_id()
      │
      ▼
assembly.complete()
      │
      ▼
AssemblyCompleted
      │
      ▼
Repository.save(expected_version)
```

---

# CancelAssembly y Repository

```text
CancelAssembly
      │
      ▼
Repository.get_by_id()
      │
      ▼
assembly.cancel()
      │
      ▼
AssemblyCancelled
      │
      ▼
Repository.save(expected_version)
```

---

# ArchiveAssembly y Repository

```text
ArchiveAssembly
      │
      ▼
Repository.get_by_id()
      │
      ▼
assembly.archive()
      │
      ▼
AssemblyArchived
      │
      ▼
Repository.save(expected_version)
```

Archived no representa eliminación física.

---

# Domain Events después de Persistencia

La arquitectura debe garantizar que un Domain Event que represente
una modificación confirmada no sea comunicado externamente como
éxito si la persistencia definitiva falló.

---

# Event Publication Failure

Si la persistencia se confirma pero la publicación externa falla,
debe existir una estrategia de reintento confiable.

Transactional Outbox constituye una opción compatible.

---

# Event Ordering

Cuando una misma modificación produzca múltiples eventos, la
persistencia debe permitir preservar el orden causal cuando sea
necesario.

---

# AggregateVersion del Evento

Todo Domain Event asociado a una modificación debe conservar una
AggregateVersion coherente con Assembly.Version.

---

# Repository y CorrelationId

CorrelationId puede acompañar registros técnicos o de eventos.

No forma parte obligatoria del estado de Assembly salvo definición
explícita.

---

# Repository y CausationId

CausationId puede acompañar la persistencia de eventos.

No modifica identidad ni Version del Aggregate.

---

# Audit Trail

AssemblyRepository no sustituye el Aggregate Audit.

Persistir el estado actual de Assembly no proporciona por sí solo
todo el historial necesario para auditoría.

---

# Migraciones

Infrastructure puede requerir migraciones de persistencia.

Una migración no debe modificar silenciosamente el significado
conceptual de Assembly.

---

# Schema Migration

Cambios como:

```text
column rename

table split

document restructure

index creation
```

pueden ser cambios técnicos sin alterar el dominio.

---

# Domain Migration

Si cambia el significado de los datos persistidos, debe existir una
migración de dominio explícita.

No debe reinterpretarse silenciosamente información histórica.

---

# Backward Compatibility

Durante una transición técnica, el Adapter puede necesitar leer
múltiples versiones del Persistence Model.

Debe traducirlas hacia Assembly solamente cuando exista una
correspondencia semántica válida.

---

# Datos Incompatibles

Si un estado histórico no puede traducirse sin pérdida o
invención de significado, debe producirse un error explícito.

No deben fabricarse valores arbitrarios.

---

# Repository Adapter

Implementaciones concretas pueden denominarse:

```text
PostgreSQLAssemblyRepository

MongoAssemblyRepository

EventStoreAssemblyRepository
```

Estos nombres pertenecen a Infrastructure.

El dominio conoce únicamente:

```text
AssemblyRepository
```

---

# Dependency Inversion

Debe cumplirse:

```text
Domain
    │
    ▼
Repository Contract
```

e:

```text
Infrastructure
    │
    ▼
implements Repository Contract
```

Nunca:

```text
Domain
    │
    ▼
PostgreSQL
```

---

# Dirección de Dependencias

La dependencia apunta hacia el dominio.

Infrastructure implementa las abstracciones requeridas por el
dominio.

El dominio no depende del mecanismo técnico.

---

# Framework Independence

El contrato no depende de:

```text
Django ORM

SQLAlchemy

Prisma

TypeORM

Mongoose

Hibernate

Entity Framework
```

Estas herramientas pueden utilizarse en Infrastructure.

---

# Database Independence

AssemblyRepository no depende de:

```text
PostgreSQL

MongoDB

MySQL

SQLite

Redis

DynamoDB

Cassandra
```

---

# Transport Independence

Repository no depende de:

```text
HTTP

REST

GraphQL

gRPC

WebSocket
```

Repository no es una API de transporte.

---

# Messaging Independence

Repository tampoco depende directamente de:

```text
Kafka

RabbitMQ

NATS

MQTT
```

---

# FIWARE Independence

AssemblyRepository no conoce:

```text
FIWARE

Orion-LD

NGSI-LD

Context Broker
```

La interoperabilidad con FIWARE pertenece a Integration.

---

# Repository Contract Tests

Toda implementación de AssemblyRepository debe superar un conjunto
común de Contract Tests.

Estos tests garantizan que distintos Adapters conserven la misma
semántica.

---

# Contract Test — Save and Load

```text
Given valid Assembly

When repository.save(assembly)

And repository.get_by_id(assembly_id)

Then restored Assembly preserves:
    AssemblyId
    OrganizationId
    State
    Version
    Domain Data
    Historical Timestamps
```

---

# Contract Test — Not Found

```text
Given unknown AssemblyId

When get_by_id()

Then AssemblyNotFound
```

---

# Contract Test — Duplicate Identity

```text
Given existing AssemblyId

When another Assembly with same AssemblyId is persisted

Then AssemblyAlreadyExists
```

---

# Contract Test — Optimistic Concurrency

```text
Given PersistedVersion = 5

When save(
    expected_version = 4
)

Then AssemblyConcurrencyConflict
```

---

# Contract Test — Atomicity

```text
Given modification changes:
    Status
    StartedAt
    Version

When persistence fails

Then none of those changes becomes committed
```

---

# Contract Test — Rehydration

```text
Given persisted valid Assembly

When get_by_id()

Then Assembly is reconstructed

And no new Domain Event is produced
```

---

# Contract Test — Archived

```text
Given AssemblyStatus = Archived

When get_by_id()

Then Assembly is reconstructed as Archived

And ArchivedAt is preserved

And no new AssemblyArchived is produced
```

---

# Contract Test — Version Preservation

```text
Given PersistedVersion = N

When Assembly is loaded

Then Assembly.Version = N
```

---

# Contract Test — Timestamp Preservation

La rehidratación debe preservar:

```text
CreatedAt

ConvokedAt

StartedAt

CompletedAt

CancelledAt

ArchivedAt
```

cuando existan.

---

# Contract Test — Domain Event Silence

```text
Given persisted Assembly

When repository.get_by_id()

Then no new:
    AssemblyCreated
    AssemblyScheduled
    AssemblyConvoked
    AssemblyStarted
    AssemblyCompleted
```

deben producirse.

---

# Contract Test — OrganizationId Preservation

```text
Given OrganizationId = ORG-1

When save/load cycle occurs

Then OrganizationId remains ORG-1
```

---

# Contract Test — AssemblyId Preservation

Después de cualquier secuencia:

```text
save
load
save
load
```

debe cumplirse:

```text
OriginalAssemblyId
=
RehydratedAssemblyId
```

---

# Contract Test — No External Aggregate Loading

Recuperar Assembly no debe convertir:

```text
Organization

Territory

Membership

Citizen

Role

Proposal

Participation

Voting

Document
```

en entidades internas del Aggregate.

---

# Contract Test — Persistence Failure

Cuando Infrastructure no pueda completar la operación debe
producirse:

```text
AssemblyPersistenceFailure
```

sin presentar la operación como confirmada.

---

# Contract Test — Lost Update

Dos modificaciones concurrentes basadas en la misma Version no
pueden confirmarse ambas silenciosamente.

---

# Contract Test — Rehydration Failure

Cuando un estado persistido sea incompatible con las invariantes
de Assembly:

```text
AssemblyRehydrationFailure
```

debe producirse.

---

# Contract Test — Adapter Equivalence

Dos implementaciones diferentes deben ofrecer semántica
equivalente para:

```text
get_by_id()

save()

exists()
```

aunque utilicen tecnologías distintas.

---

# Test Doubles

Los tests pueden utilizar:

```text
InMemoryAssemblyRepository
```

como Test Double.

Debe respetar las mismas reglas conceptuales.

---

# InMemoryAssemblyRepository

Un Repository en memoria no debe omitir:

* identidad;
* protección de duplicados;
* Version;
* Optimistic Concurrency;
* NotFound;
* atomicidad conceptual.

De lo contrario produciría pruebas que no representan el contrato
real.

---

# Mock Repository

Mocks pueden utilizarse para probar coordinación de Application
Services.

Los Contract Tests deben validar implementaciones reales o
equivalentes.

---

# Observabilidad

Infrastructure puede emitir métricas técnicas como:

```text
repository load latency

repository save latency

concurrency conflict rate

persistence failure rate

cache hit rate
```

Estas métricas no forman parte de Assembly.

---

# Logging

El Adapter puede registrar información técnica.

No debe registrar innecesariamente:

* credenciales;
* tokens;
* secretos;
* datos sensibles;
* payloads completos cuando no sean necesarios.

---

# Tracing

Puede utilizarse:

```text
TraceId

CorrelationId
```

para trazabilidad distribuida.

No modifica el Aggregate.

---

# Performance Rules

Las optimizaciones deben respetar:

```text
DOMAIN-006N-Performance-Rules.md
```

Ninguna optimización puede romper:

```text
Identity

Versioning

Atomicity

Consistency

Aggregate Boundary
```

---

# Security Model

La persistencia debe respetar:

```text
DOMAIN-006O-Security-Model.md
```

especialmente en:

* acceso;
* aislamiento;
* cifrado;
* credenciales técnicas;
* logging;
* protección contra manipulación.

---

# Extensibilidad

AssemblyRepository puede evolucionar cuando aparezcan nuevas
necesidades reales del dominio.

No debe ampliarse por conveniencia tecnológica.

---

# Regla para Añadir una Operación

Antes de agregar una nueva operación debe responderse:

```text
¿Es necesaria para recuperar Assembly?

¿Es necesaria para persistir Assembly?

¿Protege una invariante real?

¿Pertenece al Write Model?

¿No corresponde al Read Model?
```

Si la respuesta es negativa, la operación probablemente no
pertenece al Repository del dominio.

---

# Operaciones que no Pertenecen al Repository

No deben incorporarse como responsabilidades del Repository:

```text
find_all()

full_text_search()

paginate()

sort()

export_csv()

generate_report()

send_notification()

sync_fiware()

call_municipality()

assign_role()

grant_permission()

start_assembly()

complete_assembly()
```

---

# Bulk Updates

No debe existir:

```text
update_many_assemblies(...)
```

como mecanismo para modificar múltiples Aggregate Roots evitando
su comportamiento.

Cada Assembly debe proteger sus propias invariantes.

---

# Bulk Reads

Lecturas masivas destinadas exclusivamente a presentación deben
resolverse mediante Read Models.

No requieren cargar Aggregate Roots completos.

---

# Direct Database Updates

Está prohibido utilizar actualizaciones directas de base de datos
como implementación normal de Commands.

Ejemplo:

```text
UPDATE assemblies
SET status = 'Completed'
WHERE assembly_id = ...
```

no representa una implementación válida de:

```text
CompleteAssembly
```

---

# Administrative Database Operations

Pueden existir operaciones técnicas extraordinarias de
mantenimiento.

Deben encontrarse:

* controladas;
* auditadas;
* fuera del comportamiento ordinario;
* separadas del modelo del Aggregate.

---

# Contrato Mínimo Oficial

El contrato mínimo oficial de AssemblyRepository es:

```text
AssemblyRepository

    get_by_id(
        assembly_id: AssemblyId
    ) -> Assembly
       | AssemblyNotFound

    save(
        assembly: Assembly,
        expected_version: Version
    ) -> PersistedAssembly
       | AssemblyAlreadyExists
       | AssemblyConcurrencyConflict
       | AssemblyPersistenceFailure

    exists(
        assembly_id: AssemblyId
    ) -> bool
```

Operaciones adicionales solo podrán incorporarse cuando exista una
necesidad explícita y documentada del dominio.

---

# Invariantes del Repository Contract

El contrato debe preservar permanentemente:

```text
Repository never changes AssemblyId

Repository never changes OrganizationId

Repository never bypasses Versioning

Repository never creates business behavior

Repository never absorbs external Aggregates

Repository never replaces Aggregate invariants

Repository never exposes internal entities as independent roots

Repository never uses persistence technology as domain model

Repository never publishes external integrations as persistence responsibility

Repository never authorizes Actors
```

---

# Relación con DOMAIN-006-Aggregate

`DOMAIN-006-Aggregate.md` define el modelo conceptual oficial de
Assembly.

AssemblyRepository existe únicamente para persistir y recuperar
esa definición.

El Repository no redefine:

* identidad;
* Lifecycle;
* State Machine;
* reglas;
* relaciones;
* límites;
* invariantes.

---

# Relación con Lifecycle

El Repository no ejecuta las transiciones definidas en:

```text
DOMAIN-006A-Lifecycle.md
```

Solo persiste el resultado de transiciones previamente aceptadas
por Assembly.

---

# Relación con State Machine

El Repository no decide si una transición es válida.

La autoridad corresponde a:

```text
DOMAIN-006B-State-Machine.md
```

---

# Relación con Commands

Los Commands definidos en:

```text
DOMAIN-006C-Commands.md
```

son coordinados por Application Services.

El Repository participa cargando y persistiendo Assembly.

No ejecuta Commands.

---

# Relación con Domain Events

Los eventos definidos en:

```text
DOMAIN-006D-Domain-Events.md
```

son producidos por comportamiento del Aggregate.

El Repository ayuda a preservar la consistencia entre estado y
eventos.

No inventa los hechos.

---

# Relación con Invariants

El Repository debe impedir persistencia que viole el contrato de:

```text
DOMAIN-006E-Invariants.md
```

pero no reemplaza a Assembly como autoridad de esas reglas.

---

# Relación con Permissions

Los permisos definidos en:

```text
DOMAIN-006F-Permissions.md
```

se evalúan fuera del Repository.

El Repository no autoriza operaciones funcionales.

---

# Relación con Versioning

Optimistic Concurrency se aplica conforme a:

```text
DOMAIN-006I-Versioning.md
```

ExpectedVersion debe ser respetada por toda implementación.

---

# Relación con Consistency Boundary

La unidad transaccional definida en:

```text
DOMAIN-006J-Consistency-Boundary.md
```

debe preservarse durante persistencia.

---

# Relación con Integration Events

Los Integration Events definidos en:

```text
DOMAIN-006K-Integration-Events.md
```

no forman parte de la responsabilidad directa del Repository.

---

# Relación con Read Model

Las consultas especializadas definidas en:

```text
DOMAIN-006L-Read-Model.md
```

no deben expandir innecesariamente AssemblyRepository.

---

# Relación con Test Scenarios

Los escenarios definidos en:

```text
DOMAIN-006M-Test-Scenarios.md
```

deben validar tanto el Aggregate como el comportamiento contractual
del Repository.

---

# Relación con Performance Rules

Las optimizaciones del Repository deben respetar:

```text
DOMAIN-006N-Performance-Rules.md
```

---

# Relación con Security Model

Los Adapters deben cumplir:

```text
DOMAIN-006O-Security-Model.md
```

sin introducir responsabilidades de seguridad funcional dentro del
contrato del dominio.

---

# Relación con Extension Points

Nuevas estrategias de persistencia pueden incorporarse conforme a:

```text
DOMAIN-006P-Extension-Points.md
```

siempre que el contrato conceptual permanezca estable.

---

# Restricciones

No está permitido:

* persistir entidades internas de Assembly como Aggregate Roots
  independientes;
* modificar atributos internos desde Repository;
* ejecutar Commands desde Repository;
* implementar Lifecycle dentro de Repository;
* implementar State Machine dentro de Repository;
* generar Domain Events de negocio desde Repository;
* cargar otros Aggregates dentro de Assembly;
* modificar otros Aggregates mediante AssemblyRepository;
* ignorar ExpectedVersion;
* sobrescribir modificaciones concurrentes silenciosamente;
* duplicar AssemblyId;
* modificar OrganizationId;
* utilizar delete físico como transición normal;
* sustituir Archived por Deleted;
* utilizar ORM entities como modelo conceptual;
* depender de una base de datos específica desde Domain;
* convertir Repository en motor general de queries;
* implementar autorización dentro del Repository;
* implementar autenticación dentro del Repository;
* implementar integración externa dentro del Repository;
* modificar timestamps históricos durante rehidratación;
* producir Domain Events nuevos durante lectura;
* devolver Aggregates parcialmente reconstruidos;
* corregir silenciosamente datos incompatibles;
* realizar bulk updates evitando comportamiento del Aggregate;
* utilizar consultas directas de base de datos como sustituto de
  Commands;
* permitir que una optimización de caché evada Optimistic
  Concurrency;
* expandir el Consistency Boundary por conveniencia técnica.

---

# Compatibilidad Arquitectónica

AssemblyRepository es compatible con:

* Domain-Driven Design;
* Tactical DDD;
* Repository Pattern;
* Clean Architecture;
* Hexagonal Architecture;
* Ports and Adapters;
* Dependency Inversion;
* CQRS;
* Event-Driven Architecture;
* Event Sourcing;
* Transactional Outbox;
* Unit of Work;
* Optimistic Concurrency;
* arquitectura distribuida;
* persistencia relacional;
* persistencia documental;
* Event Stores.

---

# Principios Arquitectónicos

El Repository mantiene:

```text
Domain
    │
    ▼
Repository Contract
    ▲
    │
Infrastructure Adapter
```

La dirección de dependencia permanece orientada hacia el dominio.

Además:

```text
Aggregate
    ≠
Persistence Model
```

```text
Repository
    ≠
Read Model
```

```text
Repository
    ≠
Application Service
```

```text
Repository
    ≠
Integration Service
```

```text
Repository
    ≠
Authorization Service
```

```text
Repository
    ≠
Database
```

Estas separaciones son obligatorias para preservar el diseño DDD.

---

# Reglas de Diseño

AssemblyRepository debe garantizar:

* persistencia mediante Aggregate Root;
* identidad mediante AssemblyId;
* OrganizationId preservado;
* rehidratación completa;
* atomicidad;
* Optimistic Concurrency;
* preservación de Version;
* protección contra duplicados;
* separación Domain/Infrastructure;
* ausencia de lógica de autorización;
* ausencia de lógica de autenticación;
* ausencia de lógica de integración;
* ausencia de comportamiento de dominio dentro del Repository;
* independencia tecnológica;
* compatibilidad con múltiples estrategias de persistencia;
* coherencia con Domain Events;
* respeto del Consistency Boundary;
* preservación histórica;
* errores explícitos;
* capacidad de Contract Testing.

---

# Definición de Éxito

El **AssemblyRepository** constituye el contrato oficial mediante
el cual el Aggregate **Assembly** puede ser recuperado y persistido
sin introducir dependencias hacia tecnologías de
Infrastructure.

El Repository administra exclusivamente la Aggregate Root
Assembly y preserva su identidad mediante AssemblyId.

Toda rehidratación reconstruye el Aggregate conservando:

* AssemblyId;
* OrganizationId;
* AssemblyStatus;
* Version;
* timestamps históricos;
* Value Objects;
* entidades internas;
* configuración;
* reglas;
* condiciones de realización.

La rehidratación nunca representa una nueva creación y nunca
produce Domain Events nuevos por el solo hecho de recuperar el
Aggregate.

Toda persistencia trata Assembly como una única unidad de
consistencia, respetando atomicidad, invariantes y Optimistic
Concurrency.

ExpectedVersion impide que modificaciones concurrentes
sobrescriban silenciosamente cambios previamente confirmados.

El Repository no ejecuta Commands, no implementa State Machine,
no concede Permissions, no autentica Actors, no modifica otros
Aggregates y no genera comportamiento de dominio.

Organization, Territory, Membership, Citizen, Role, Proposal,
Participation, Voting, Document, Notification, Audit e
Integration conservan sus propios límites de consistencia y nunca
son absorbidos por AssemblyRepository por conveniencia técnica.

Las consultas destinadas a búsqueda, filtrado, paginación,
ordenamiento, reporting o presentación pertenecen al Read Model y
no expanden innecesariamente el contrato del Repository.

La implementación concreta puede utilizar:

```text
PostgreSQL

MongoDB

Event Store

Snapshots

Caching

Unit of Work

Transactional Outbox
```

u otros mecanismos, siempre que preserve exactamente el mismo
contrato conceptual del dominio.

Archived no representa eliminación física.

La persistencia no redefine el Lifecycle.

El ORM no redefine el Aggregate.

La base de datos no redefine la identidad.

La infraestructura no redefine las invariantes.

De esta forma, **AssemblyRepository** establece una frontera
estable entre Domain e Infrastructure, garantiza la persistencia
consistente del Aggregate y preserva la independencia tecnológica,
la concurrencia segura, la atomicidad, el bajo acoplamiento y los
límites definidos por la arquitectura Domain-Driven Design de
AURA.
