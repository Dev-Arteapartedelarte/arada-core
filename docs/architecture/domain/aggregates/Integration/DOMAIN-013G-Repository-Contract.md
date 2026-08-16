# DOMAIN-013G — Integration Repository Contract

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
- DOMAIN-013H-Examples.md
- DOMAIN-013I-Versioning.md
- DOMAIN-013J-Consistency-Boundary.md
- DOMAIN-013K-Integration-Events.md
- DOMAIN-013L-Read-Model.md
- DOMAIN-013M-Test-Scenarios.md
- DOMAIN-013N-Performance-Rules.md
- DOMAIN-013O-Security-Model.md
- DOMAIN-013P-Extension-Points.md

---

# Objetivo

Este documento define formalmente el **Repository Contract** del
Aggregate **Integration**.

El Repository proporciona la abstracción de dominio necesaria para:

- persistir Integration;
- recuperar Integration;
- verificar existencia;
- administrar identidad conforme al contrato;
- proteger Optimistic Concurrency;
- preservar el Aggregate como unidad de consistencia.

La implementación física del Repository pertenece a Infrastructure.

---

# Principio Fundamental

Debe mantenerse:

```text
Repository

=

Domain Persistence Contract
```

y no:

```text
Repository

=

Domain Behavior
```

---

# Nombre Conceptual

El contrato del Aggregate es:

```text
IntegrationRepository
```

---

# Contrato Oficial

La versión 1.0 define conceptualmente:

```text
IntegrationRepository

    save()

    findById()

    exists()

    delete()

    nextIdentity()
```

Estas operaciones representan el contrato del Repository.

No representan Commands del Aggregate.

---

# Responsabilidad

IntegrationRepository es responsable de:

- persistir un Integration válido;
- recuperar un Integration previamente persistido;
- verificar existencia por identidad;
- preservar IntegrationId;
- preservar State;
- preservar Version;
- preservar CreatedAt;
- preservar UpdatedAt;
- preservar la información formal del Aggregate;
- proteger el control de concurrencia definido;
- mantener el Aggregate como unidad de persistencia.

---

# Responsabilidades Fuera del Repository

IntegrationRepository no es responsable de:

- ejecutar Commands;
- decidir Lifecycle;
- decidir State Machine;
- decidir Guards;
- decidir Invariants;
- decidir Permissions;
- autenticar requesters;
- autorizar operaciones;
- modificar otros Aggregates;
- publicar Integration Events;
- transportar mensajes;
- ejecutar llamadas externas;
- administrar FIWARE;
- administrar sistemas municipales;
- administrar brokers;
- administrar credenciales;
- construir Read Models;
- decidir políticas de retención.

---

# Repository versus Aggregate

Debe mantenerse:

```text
Integration

owns

Domain Behavior
```

mientras:

```text
IntegrationRepository

owns

Persistence Contract
```

---

# Repository no es Aggregate

Debe mantenerse:

```text
IntegrationRepository

≠

Integration
```

---

# Repository no Ejecuta Commands

Debe mantenerse:

```text
Repository

≠

Command Handler
```

El Repository no ejecuta:

```text
CreateIntegration

ActivateIntegration

SuspendIntegration

ReactivateIntegration

ArchiveIntegration
```

---

# Repository no Decide State

El Repository no decide:

```text
Draft

Active

Suspended

Archived
```

El State es consecuencia del comportamiento válido del Aggregate.

---

# Repository no Ejecuta Transiciones

El Repository no puede producir directamente:

```text
Draft → Active

Active → Suspended

Suspended → Active

Draft → Archived

Active → Archived

Suspended → Archived
```

---

# Repository no Corrige State

Si recibe un Aggregate inválido, el Repository no debe modificarlo
silenciosamente para convertirlo en válido.

Debe mantenerse:

```text
Invalid Aggregate

≠

Repository Repair
```

---

# Repository no Corrige Invariants

Debe mantenerse:

```text
Repository

≠

Invariant Repair Mechanism
```

Las Invariants pertenecen al Aggregate.

---

# Repository no Decide Permissions

Debe mantenerse:

```text
Repository

≠

Authorization Policy
```

---

# Repository no Produce Domain Behavior

Persistir un Aggregate no representa comportamiento de negocio.

Debe mantenerse:

```text
save()

≠

Domain Command
```

---

# save()

`save()` persiste una instancia válida de Integration como una unidad
de consistencia.

Conceptualmente:

```text
save(Integration)
```

---

# Precondición de save()

Antes de persistir:

- Integration debe existir como Aggregate válido;
- IntegrationId debe ser válido;
- State debe ser válido;
- Invariants deben cumplirse;
- Version debe ser coherente;
- la modificación debe haber sido producida por comportamiento válido.

---

# save() no Valida Comportamiento en Lugar del Aggregate

El Repository puede rechazar persistencia incompatible.

No sustituye la responsabilidad del Aggregate de validar:

- State Machine;
- Guards;
- Invariants;
- Commands.

---

# save() y Creación

Para una nueva Integration:

```text
CreateIntegration
    │
    ▼
Integration
    │
    ▼
State = Draft
    │
    ▼
save()
```

`save()` persiste el resultado.

No crea por sí mismo la transición:

```text
No Integration → Draft
```

---

# save() y Modificación

Para una Integration existente:

```text
Command
    │
    ▼
Integration Aggregate
    │
    ▼
Valid Modification
    │
    ▼
save()
```

---

# save() no Incrementa Version

El Repository no decide incrementar Version.

Debe mantenerse:

```text
Aggregate Behavior

determines

New Version
```

mientras:

```text
Repository

verifies and persists

Version
```

---

# save() no Cambia UpdatedAt

UpdatedAt debe haber sido establecido como consecuencia de una
modificación válida del Aggregate.

El Repository no debe reemplazar arbitrariamente ese valor.

---

# save() no Cambia CreatedAt

CreatedAt permanece inmutable.

El Repository no debe sustituirlo por un timestamp técnico de
persistencia.

---

# Persistencia del Aggregate Completo

Integration debe persistirse como una unidad.

Conceptualmente:

```text
Integration
    │
    ├── IntegrationId
    ├── State
    ├── Version
    ├── CreatedAt
    ├── UpdatedAt
    └── Domain Information
```

---

# No Persistencia Parcial

No está permitido persistir partes de Integration mediante operaciones
que permitan dejar el Aggregate en estado inconsistente.

Debe mantenerse:

```text
Partial Aggregate Persistence

≠

Valid Repository Save
```

---

# Atomicidad de save()

La persistencia debe preservar conceptualmente la atomicidad de la
unidad de consistencia.

No debe confirmarse:

```text
State = NewState
```

mientras:

```text
Version = OldVersion
```

cuando ambos pertenecen a la misma modificación válida.

---

# findById()

`findById()` recupera una Integration mediante:

```text
IntegrationId
```

Conceptualmente:

```text
findById(IntegrationId)
```

---

# Resultado de findById()

Cuando existe el Aggregate, la recuperación debe preservar:

```text
IntegrationId

State

Version

CreatedAt

UpdatedAt

Domain Information
```

conforme al estado persistido.

---

# Aggregate no Encontrado

Cuando no existe una Integration con el IntegrationId solicitado,
`findById()` debe representar conceptualmente:

```text
IntegrationNotFound
```

conforme al contrato de dominio.

---

# findById() no Crea Aggregate

Debe mantenerse:

```text
findById()

≠

CreateIntegration
```

---

# findById() no Modifica Aggregate

Una lectura:

- no cambia State;
- no incrementa Version;
- no modifica UpdatedAt;
- no genera Domain Events;
- no ejecuta Commands.

---

# Rehidratación

`findById()` puede requerir reconstruir conceptualmente el Aggregate.

Debe mantenerse:

```text
Rehydration

≠

Domain Modification
```

---

# Rehydration y Lifecycle

Recuperar:

```text
State = Active
```

no ejecuta:

```text
ActivateIntegration
```

---

# Rehydration y Domain Events

Rehidratar una Integration no produce nuevos:

```text
IntegrationCreated

IntegrationActivated

IntegrationSuspended

IntegrationReactivated

IntegrationArchived
```

---

# Rehydration y Version

Debe recuperarse la Version persistida.

No debe incrementarse Version por el acto de recuperar.

---

# Rehydration y Invariants

El Aggregate rehidratado debe respetar las mismas Invariants definidas
en:

```text
DOMAIN-013E-Invariants.md
```

---

# exists()

`exists()` verifica conceptualmente si existe una Integration para un:

```text
IntegrationId
```

---

# Resultado de exists()

Conceptualmente:

```text
exists(IntegrationId)

→

true | false
```

---

# exists() no Recupera Autoridad de Escritura

`exists()` es una operación de consulta.

No modifica:

- State;
- Version;
- UpdatedAt;
- Domain Events.

---

# exists() y CreateIntegration

La existencia de una Integration puede ser relevante para impedir que
una misma identidad sea creada nuevamente.

Sin embargo:

```text
exists()

≠

CreateIntegration Validation Authority
```

La regla de identidad continúa perteneciendo al dominio.

---

# nextIdentity()

`nextIdentity()` proporciona conceptualmente una nueva identidad válida
para Integration.

Conceptualmente:

```text
nextIdentity()

→

IntegrationId
```

---

# nextIdentity() no Crea Integration

Debe mantenerse:

```text
nextIdentity()

≠

CreateIntegration
```

Obtener una identidad no crea un Aggregate.

---

# nextIdentity() y Unicidad

La identidad proporcionada debe ser adecuada para preservar:

```text
IntegrationId uniqueness
```

---

# nextIdentity() no Deriva Identidad Externa

La identidad de Integration no debe requerir que sea idéntica a:

```text
ExternalSystemId

FIWARE Entity Id

Municipal System Id

External Message Id

Domain Event Id

Integration Event Id
```

---

# nextIdentity() no Decide Formato

Este documento no define:

- UUID;
- ULID;
- sequence;
- database identity;
- numeric identifier;
- string identifier.

La representación concreta de IntegrationId no se decide aquí.

---

# delete()

El contrato consolidado del Repository contempla conceptualmente:

```text
delete()
```

como operación de persistencia.

Debe mantenerse:

```text
Repository.delete()

≠

DeleteIntegration
```

---

# delete() no es Lifecycle

La operación de Repository:

```text
delete()
```

no representa una transición de:

```text
DOMAIN-013A-Lifecycle.md
```

---

# delete() no Crea Deleted

La existencia de `delete()` no introduce:

```text
Deleted
```

como State.

---

# delete() no Sustituye ArchiveIntegration

Debe mantenerse:

```text
ArchiveIntegration

≠

Repository.delete()
```

`ArchiveIntegration` representa comportamiento del dominio.

`delete()` pertenece al contrato de persistencia.

---

# Política de Eliminación

El Repository no decide cuándo una eliminación física está permitida.

La versión 1.0 no define:

- retention period;
- automatic purge;
- expiration;
- physical deletion policy.

Estas reglas no deben inferirse desde la existencia de `delete()`.

---

# delete() y Reglas Externas

`delete()` solamente puede ser utilizado cuando una regla aplicable,
explícitamente definida fuera de este contrato de persistencia, permita
la eliminación correspondiente.

El Repository no crea dicha regla.

---

# Archived no Implica delete()

Debe mantenerse:

```text
State = Archived

≠

Repository.delete()
```

Archivar no significa eliminar físicamente.

---

# Repository y Lifecycle

El Repository persiste el resultado del Lifecycle.

No controla el Lifecycle.

Debe mantenerse:

```text
Lifecycle Authority

=

Integration Aggregate
```

y:

```text
Persistence Authority

=

Repository Contract
```

---

# Repository y State Machine

El Repository no puede aceptar una modificación como mecanismo para
evitar:

```text
DOMAIN-013B-State-Machine.md
```

---

# Repository y Commands

Los Commands se ejecutan antes de la persistencia del resultado.

El Repository no interpreta un:

```text
ActivateIntegration
```

ni cualquier otro Command.

---

# Repository y Domain Events

El Repository no inventa Domain Events.

Debe mantenerse:

```text
Repository

≠

Domain Event Producer
```

---

# Domain Event Ownership

Los Domain Events:

```text
IntegrationCreated

IntegrationActivated

IntegrationSuspended

IntegrationReactivated

IntegrationArchived
```

son producidos por comportamiento válido de Integration.

---

# save() no Produce IntegrationCreated

Debe mantenerse:

```text
save(new Integration)

≠

create IntegrationCreated
```

El evento existe porque el Aggregate fue creado válidamente.

---

# save() no Produce IntegrationActivated

Persistir:

```text
State = Active
```

no es la causa semántica de:

```text
IntegrationActivated
```

La causa es la transición válida del dominio.

---

# Domain Events y Commit

Un Domain Event de modificación debe corresponder a un cambio
confirmado del Aggregate.

Conceptualmente:

```text
Domain Behavior
    │
    ▼
Domain Event
    │
    ▼
Repository save()
    │
    ▼
Commit
```

La persistencia confirma la modificación como unidad.

---

# No Success Event after Persistence Failure

Si la persistencia de la modificación no puede confirmarse, el hecho
no debe tratarse externamente como un nuevo evento de éxito confirmado.

---

# Publicación Externa

La publicación de Integration Events permanece fuera del Repository.

Debe mantenerse:

```text
Repository save()

≠

Publish Integration Event
```

---

# Domain Event versus Integration Event

El Repository no transforma:

```text
Domain Event

→

Integration Event
```

como responsabilidad de dominio del contrato.

---

# Optimistic Concurrency

IntegrationRepository debe preservar el modelo de Optimistic
Concurrency definido en:

```text
DOMAIN-013I-Versioning.md
```

---

# ExpectedVersion

Para una modificación de una Integration existente:

```text
ExpectedVersion

=

PersistedVersion
```

debe cumplirse antes de aceptar la escritura.

---

# PersistedVersion

PersistedVersion representa la Version confirmada actualmente para el
IntegrationId correspondiente.

---

# NewVersion

La nueva Version debe haber sido producida por comportamiento válido
del Aggregate.

Conceptualmente:

```text
PersistedVersion = N

ExpectedVersion = N

Integration.Version = N + 1
```

permite confirmar la modificación cuando las demás reglas son válidas.

---

# ConcurrencyConflict

Si:

```text
ExpectedVersion

≠

PersistedVersion
```

el Repository debe rechazar la escritura mediante:

```text
ConcurrencyConflict
```

---

# No Silent Overwrite

Debe mantenerse:

```text
ConcurrencyConflict

≠

Silent Overwrite
```

---

# No Last-Write-Wins Implícito

La versión 1.0 no permite inferir:

```text
Last Write Wins
```

como estrategia que ignore Versioning.

---

# Concurrency por IntegrationId

El control de concurrencia se aplica al Aggregate identificado por:

```text
IntegrationId
```

---

# Different IntegrationId

Diferentes IntegrationId mantienen Version independiente.

Debe mantenerse:

```text
Integration A Version

≠

Integration B Version
```

como secuencias independientes.

---

# Source Version

Si un contrato externo posee una versión propia:

```text
External Version

≠

Integration.Version
```

---

# Contract Version

Debe mantenerse:

```text
Integration Contract Version

≠

Integration.Version
```

---

# Repository Error Model

El contrato puede representar conceptualmente errores como:

```text
IntegrationNotFound

DuplicateIntegrationId

ConcurrencyConflict

PersistenceFailure

RepositoryUnavailable
```

Estos errores no son Lifecycle States.

---

# IntegrationNotFound

`IntegrationNotFound` representa ausencia de un Aggregate solicitado.

No crea:

```text
Failed
```

como State.

---

# DuplicateIntegrationId

`DuplicateIntegrationId` representa un conflicto de identidad durante
persistencia de una nueva Integration.

No debe producir una segunda Integration con la misma identidad.

---

# ConcurrencyConflict no es Domain State

Debe mantenerse:

```text
ConcurrencyConflict

≠

Integration State
```

---

# PersistenceFailure

`PersistenceFailure` representa imposibilidad de confirmar la
persistencia.

No transforma automáticamente:

```text
Active

→

Suspended
```

ni cualquier otra transición.

---

# RepositoryUnavailable

La indisponibilidad técnica del Repository no modifica el Lifecycle.

---

# Error Técnico no Modifica Aggregate

Debe mantenerse:

```text
Repository Error

≠

Domain Transition
```

---

# Error Técnico no Incrementa Version

Una operación que no logra confirmarse no debe incrementar
artificialmente la Version persistida.

---

# Error Técnico no Modifica UpdatedAt Persistido

Si el cambio no se confirma, el estado persistido anterior permanece
autoritativo.

---

# Repository e Invariants

El Repository debe preservar las Invariants definidas en:

```text
DOMAIN-013E-Invariants.md
```

No debe aceptar persistencia parcial que las rompa.

---

# Aggregate Válido Antes de Persistir

Debe mantenerse:

```text
Valid Aggregate

before

Repository Commit
```

---

# Repository no Fabrica Datos

El Repository no puede completar arbitrariamente información de
dominio ausente.

Debe mantenerse:

```text
Missing Domain Information

≠

Repository Generated Domain Information
```

---

# Repository no Traduce Modelos Externos

El Repository no convierte:

```text
FIWARE Model

Municipal Model

External API Model
```

en el Domain Model de Integration.

---

# Repository no es Integration Boundary Externo

Debe mantenerse:

```text
Repository

≠

External Integration Contract
```

---

# Repository no es Adapter Externo

Debe mantenerse:

```text
IntegrationRepository

≠

FIWARE Adapter

≠

Municipal Adapter

≠

HTTP Client
```

---

# Independencia Tecnológica

El contrato no depende de:

```text
PostgreSQL

MongoDB

MySQL

SQLite

Redis

EventStoreDB

SQL

ORM

Filesystem

HTTP

REST

GraphQL

Kafka

RabbitMQ

NATS

FIWARE

NGSI-LD

Context Broker
```

---

# Persistencia Relacional

El contrato no exige una base de datos relacional.

---

# Persistencia Documental

El contrato tampoco exige una base de datos documental.

---

# Event Store

El contrato no exige un Event Store.

---

# Event Sourcing

IntegrationRepository permanece compatible con Event Sourcing.

Debe mantenerse:

```text
Event Sourcing Compatible

≠

Event Sourcing Required
```

---

# Repository y Event Sourcing

Si Event Sourcing fuese utilizado, la implementación del Repository
deberá preservar:

- IntegrationId;
- State reconstruible;
- Version;
- Invariants;
- historial necesario conforme al modelo adoptado.

Esto no cambia el contrato conceptual del dominio.

---

# Event Stream no es Integration Event Stream

Debe mantenerse:

```text
Aggregate Event Stream

≠

Integration Event Stream
```

---

# Replay

El Repository puede participar técnicamente en una rehidratación
mediante replay si la estrategia de persistencia lo requiere.

Sin embargo:

```text
Replay

≠

Execute Commands
```

---

# Replay no Produce Nuevos Domain Events

Debe mantenerse:

```text
Replay

≠

New Domain Fact
```

---

# Snapshot

Este contrato no exige:

```text
Snapshot
```

como mecanismo de persistencia.

---

# CQRS

IntegrationRepository pertenece conceptualmente al Write Side del
Aggregate.

Debe mantenerse:

```text
Repository

≠

Read Model
```

---

# Repository versus Read Model

El Repository recupera Aggregates para comportamiento de dominio.

Los Read Models resuelven necesidades de consulta.

---

# Consultas Complejas

El Repository no debe convertirse en un motor general de:

- reporting;
- analytics;
- búsqueda histórica;
- dashboards;
- agregaciones globales.

Estas necesidades pertenecen al Read Side.

---

# findById() versus Query Model

`findById()` recupera un Aggregate por identidad.

No reemplaza los Read Models definidos en:

```text
DOMAIN-013L-Read-Model.md
```

---

# exists() versus Read Model

`exists()` responde exclusivamente a existencia conceptual por
identidad.

No representa una consulta analítica.

---

# No Repository Global

IntegrationRepository no representa una Aggregate Root global.

Debe mantenerse:

```text
Repository manages many Aggregates

≠

One Global Integration Aggregate
```

---

# Unidad de Consistencia

Cada operación de persistencia de escritura afecta a una única
Integration como unidad.

Debe mantenerse:

```text
One IntegrationId

=

One Aggregate Consistency Boundary
```

---

# No Cross-Aggregate Save

Una operación `save()` de Integration no debe persistir atómicamente
cambios de:

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

Audit
```

como parte del mismo Aggregate.

---

# No External System Commit

`save()` tampoco significa:

```text
FIWARE Commit

Municipal System Commit

External Platform Commit
```

---

# Consistencia Externa

Debe mantenerse:

```text
Integration Commit

≠

External System Commit
```

La consistencia externa permanece eventual.

---

# No Distributed Transaction Requirement

El Repository Contract no exige una transacción distribuida entre:

```text
Integration

+

External System
```

---

# Source Aggregate Commit

Un commit de otro Aggregate no equivale a un commit de Integration.

Debe mantenerse:

```text
Source Aggregate Transaction

≠

Integration Repository Transaction
```

---

# Domain Event Commit

La persistencia debe conservar coherencia entre el cambio del Aggregate
y los Domain Events producidos por dicho comportamiento conforme al
modelo de persistencia adoptado.

Este documento no decide un mecanismo técnico concreto para lograrlo.

---

# No Decisión de Outbox

Este contrato no establece obligatoriamente:

```text
Transactional Outbox
```

ni otro mecanismo específico de publicación.

---

# Outbox no es Repository Domain State

Si una implementación utiliza un mecanismo externo de publicación, su
estado técnico no forma parte de Integration.

---

# Repository y Security

IntegrationRepository no administra Authentication.

---

# Repository y Permissions

El Repository no evalúa:

```text
Integration.Create

Integration.Activate

Integration.Suspend

Integration.Reactivate

Integration.Archive
```

como política de Authorization.

---

# Technical Access no es Permission

Poder acceder técnicamente al Repository no concede una Permission de
dominio.

---

# Repository no Almacena Credenciales como Dominio

El Aggregate persistido no debe incorporar:

```text
Password

AccessToken

RefreshToken

ApiKey

PrivateKey

ClientSecret

Secret
```

como estado de Integration.

---

# Data Minimization

El Repository debe persistir la información perteneciente al Aggregate
sin ampliar arbitrariamente su estado con información externa.

---

# External Payload

El Repository no almacena automáticamente:

```text
Full External Payload
```

como parte de Integration.

Solamente persiste información reconocida por el Domain Model.

---

# FIWARE

IntegrationRepository no conoce conceptualmente FIWARE como requisito
del dominio.

---

# NGSI-LD

El Repository Contract no se expresa mediante NGSI-LD.

Debe mantenerse:

```text
Repository Domain Contract

≠

NGSI-LD Persistence Contract
```

---

# Sistemas Municipales

El Repository no persiste directamente modelos municipales como si
fueran el Aggregate Integration.

---

# External IDs

Si una referencia externa forma parte legítima del dominio, el
Repository debe preservarla exactamente conforme al Aggregate.

No debe convertirla en IntegrationId.

---

# Identidad Round-Trip

Debe cumplirse conceptualmente:

```text
Integration X
    │
    ▼
save(X)
    │
    ▼
findById(X.IntegrationId)
    │
    ▼
Integration X
```

preservando identidad y estado de dominio.

---

# Round-Trip de State

Si:

```text
State = Active
```

al persistir, una recuperación posterior debe reconstruir:

```text
State = Active
```

mientras no exista una modificación posterior válida.

---

# Round-Trip de Version

Si:

```text
Version = N
```

al persistir, una recuperación debe preservar:

```text
Version = N
```

mientras no exista una modificación posterior.

---

# Round-Trip de CreatedAt

CreatedAt debe conservarse sin ser reemplazado por timestamps técnicos
de lectura o escritura.

---

# Round-Trip de UpdatedAt

UpdatedAt debe preservar el valor correspondiente a la última
modificación válida del Aggregate.

---

# Round-Trip de Información de Dominio

Toda información formal que pertenezca al Aggregate debe conservar su
significado después de persistir y recuperar.

---

# Orden de Persistencia

Version establece el orden lógico de modificaciones de una misma
Integration.

Un timestamp de almacenamiento no sustituye esta semántica.

---

# No Global Version

El Repository no establece una Version global para todas las
Integration.

---

# No Global Ordering

El Repository Contract no exige orden global entre diferentes
IntegrationId.

---

# Idempotencia

El Repository debe ser compatible con las reglas de identidad y
concurrencia del Aggregate.

La estrategia técnica concreta de idempotencia no se define aquí.

---

# Technical Redelivery

Una retransmisión técnica no debe provocar por sí misma una nueva
modificación válida del Aggregate.

---

# Duplicate Creation

Dos intentos incompatibles de creación para el mismo IntegrationId no
pueden producir dos Aggregate Roots válidas con la misma identidad.

---

# DuplicateIntegrationId

Debe rechazarse la persistencia incompatible de una segunda identidad
equivalente mediante:

```text
DuplicateIntegrationId
```

---

# Repository y Performance

El Repository debe operar sobre la unidad Aggregate necesaria para la
escritura.

No debe requerir cargar todas las Integration para modificar una.

---

# No Historical Query Engine

El Repository no debe cargar toda la historia global para responder
consultas que pertenecen al Read Side.

---

# No Reporting Repository

El Repository Contract no incorpora operaciones de reporting como
responsabilidad del Write Model.

---

# No Analytics Repository

Analytics permanece fuera del contrato del Aggregate Repository.

---

# No Technology-Specific Methods

No forman parte del contrato métodos como:

```text
insertRow()

updateDocument()

executeSql()

mongoFind()

publishKafka()

sendHttp()

syncFIWARE()
```

---

# Lenguaje del Repository

Las operaciones del contrato deben conservar semántica del dominio y
no exponer detalles de Infrastructure.

---

# Repository Implementation

La implementación concreta pertenece a Infrastructure.

Debe respetar completamente este contrato.

---

# Infrastructure Freedom

Infrastructure puede implementar el contrato mediante tecnologías
compatibles con las necesidades de AURA.

Este documento no selecciona ninguna.

---

# Substituibilidad

Dos implementaciones diferentes de IntegrationRepository deben
preservar la misma semántica observable del contrato de dominio.

---

# Persistencia no Redefine Dominio

Debe mantenerse:

```text
Persistence Model

≠

Domain Model
```

---

# Schema no Redefine Aggregate

Una tabla, colección, documento o schema físico no determina por sí
mismo:

- entidades;
- Value Objects;
- State;
- Commands;
- Invariants.

---

# Internal Entities

La versión 1.0 del Aggregate no establece Internal Entities concretas.

El Repository Contract no debe inventarlas por conveniencia de
persistencia.

---

# Value Objects

La versión 1.0 no establece Value Objects específicos obligatorios de
Integration.

El Repository tampoco debe introducirlos como reglas de dominio por
conveniencia técnica.

---

# Mapping de Persistencia

Cualquier transformación entre representación física y Aggregate debe
preservar exactamente la semántica del dominio.

La estrategia concreta de mapping pertenece a Infrastructure.

---

# Test de Contrato

Una implementación de IntegrationRepository debe permitir verificar
conceptualmente:

```text
save valid Integration

find existing Integration by IntegrationId

detect missing Integration

verify existence

preserve identity

preserve State

preserve Version

preserve CreatedAt

preserve UpdatedAt

reject duplicate identity

reject incompatible Version

preserve Aggregate round-trip
```

---

# Test de Creación

Conceptualmente:

```text
Given

No Integration with IntegrationId = X

When

a valid Draft Integration X is saved

Then

findById(X) returns the same Aggregate identity and State
```

---

# Test de Recuperación

Conceptualmente:

```text
Given

Integration X exists

When

findById(X)

Then

IntegrationId, State, Version and domain information are preserved
```

---

# Test de Inexistencia

Conceptualmente:

```text
Given

Integration X does not exist

When

findById(X)

Then

IntegrationNotFound
```

---

# Test de exists()

Conceptualmente:

```text
Given

Integration X exists

When

exists(X)

Then

true
```

---

# Test de Identidad Duplicada

Conceptualmente:

```text
Given

IntegrationId = X already exists

When

another new Integration with IntegrationId = X is persisted

Then

DuplicateIntegrationId
```

---

# Test de Concurrencia

Conceptualmente:

```text
Given

PersistedVersion = 5

And

ExpectedVersion = 4

When

save(modified Integration)

Then

ConcurrencyConflict
```

---

# Test de Round-Trip

Conceptualmente:

```text
Given

Integration X

When

save(X)

And

findById(X.IntegrationId)

Then

identity, State, Version and domain meaning are preserved
```

---

# Test de Lectura sin Modificación

Conceptualmente:

```text
Given

Integration Version = N

When

findById()

Then

Version = N

UpdatedAt unchanged

No new Domain Event
```

---

# Test de Repository sin Domain Behavior

Conceptualmente:

```text
Given

State = Draft

When

Repository.save()

Then

Repository does not activate Integration
```

---

# Test de delete() versus Lifecycle

Conceptualmente:

```text
Repository.delete()

≠

ArchiveIntegration
```

La existencia del método no debe alterar la State Machine.

---

# Evolución Futura

Cualquier operación nueva del Repository debe responder a una necesidad
real de persistencia del Aggregate.

No debe introducirse para resolver consultas o comportamientos que
pertenecen a otros contratos.

---

# Regla para Nuevas Operaciones

Una nueva operación del Repository debe:

- pertenecer al contrato de persistencia del Aggregate;
- respetar Consistency Boundary;
- respetar Invariants;
- respetar Versioning;
- preservar independencia tecnológica;
- no ejecutar Commands;
- no sustituir Read Models;
- no incorporar comportamiento de Infrastructure al dominio.

---

# No Repository Growth por Query

Una nueva necesidad de:

- búsqueda;
- filtrado;
- ordenamiento;
- paginación;
- reporting;
- analytics;

no debe ampliar automáticamente el Repository del Write Model.

---

# Impacto de Evolución

Una modificación significativa del Repository Contract debe revisar
cuando corresponda:

```text
DOMAIN-013-Aggregate.md

DOMAIN-013C-Commands.md

DOMAIN-013D-Domain-Events.md

DOMAIN-013E-Invariants.md

DOMAIN-013I-Versioning.md

DOMAIN-013J-Consistency-Boundary.md

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
Persistence Requirement

≠

New Domain Behavior
```

y:

```text
Database Capability

≠

Repository Contract Requirement
```

y:

```text
Infrastructure Feature

≠

Domain Repository Operation
```

---

# Reglas Fundamentales

IntegrationRepository debe cumplir:

1. IntegrationRepository es un contrato del dominio.
2. Su implementación pertenece a Infrastructure.
3. El Repository persiste Integration como unidad.
4. El Repository recupera Integration por IntegrationId.
5. El Repository verifica existencia por IntegrationId.
6. El Repository puede proporcionar una nueva identidad conforme al
   contrato.
7. El contrato oficial define save().
8. El contrato oficial define findById().
9. El contrato oficial define exists().
10. El contrato oficial define delete().
11. El contrato oficial define nextIdentity().
12. Repository no es Aggregate.
13. Repository no ejecuta Commands.
14. Repository no decide Lifecycle.
15. Repository no decide State Machine.
16. Repository no decide Guards.
17. Repository no decide Invariants.
18. Repository no decide Permissions.
19. Repository no autentica.
20. Repository no autoriza.
21. Repository no produce comportamiento de dominio.
22. save() persiste un Aggregate válido.
23. save() no crea el Aggregate por sí mismo.
24. save() no activa Integration.
25. save() no suspende Integration.
26. save() no reactiva Integration.
27. save() no archiva Integration.
28. save() no incrementa Version por decisión propia.
29. save() no reemplaza CreatedAt.
30. save() no decide UpdatedAt.
31. Persistencia debe preservar el Aggregate completo como unidad de
    consistencia.
32. Persistencia parcial incompatible está prohibida.
33. findById() recupera por IntegrationId.
34. findById() no crea Aggregate.
35. findById() no modifica State.
36. findById() no incrementa Version.
37. findById() no modifica UpdatedAt.
38. findById() no genera nuevos Domain Events.
39. Rehydration no es modificación.
40. Rehydration preserva Invariants.
41. exists() no modifica Aggregate.
42. nextIdentity() no crea Aggregate.
43. nextIdentity() debe preservar unicidad.
44. nextIdentity() no requiere derivar IntegrationId desde una
    identidad externa.
45. El formato concreto de IntegrationId no se define aquí.
46. Repository.delete() no es DeleteIntegration.
47. Repository.delete() no es Lifecycle Transition.
48. delete() no introduce Deleted.
49. delete() no sustituye ArchiveIntegration.
50. El Repository no decide política de eliminación.
51. Archived no implica delete().
52. Repository no inventa Domain Events.
53. Domain Events pertenecen al Aggregate.
54. save() no es la causa semántica de un Domain Event.
55. Publicación externa no pertenece al Repository Contract.
56. Repository no transforma Domain Events en Integration Events.
57. Optimistic Concurrency debe preservarse.
58. ExpectedVersion debe coincidir con PersistedVersion cuando
    corresponda.
59. ConcurrencyConflict rechaza escritura incompatible.
60. Silent Overwrite está prohibido.
61. Last-Write-Wins no se infiere como regla.
62. Concurrencia se protege por IntegrationId.
63. Different IntegrationId mantienen Version independiente.
64. External Version no es Integration.Version.
65. Contract Version no es Integration.Version.
66. IntegrationNotFound no es Lifecycle State.
67. DuplicateIntegrationId no es Lifecycle State.
68. ConcurrencyConflict no es Lifecycle State.
69. PersistenceFailure no es Lifecycle State.
70. RepositoryUnavailable no es Lifecycle State.
71. Repository Error no produce transición.
72. Repository no fabrica información de dominio.
73. Repository no traduce modelos externos.
74. Repository no es FIWARE Adapter.
75. Repository no es Municipal Adapter.
76. Repository es independiente de base de datos.
77. Repository es independiente de ORM.
78. Repository es independiente de protocolo.
79. Repository es independiente de broker.
80. Repository es independiente de FIWARE.
81. Repository es compatible con Event Sourcing pero no lo exige.
82. Replay no ejecuta Commands.
83. Replay no produce nuevos Domain Events.
84. Repository pertenece conceptualmente al Write Side.
85. Repository no es Read Model.
86. Consultas complejas pertenecen al Read Side.
87. Repository no es motor de reporting.
88. Repository no es motor de analytics.
89. Cada IntegrationId conserva su propio Consistency Boundary.
90. save() no persiste atómicamente otros Aggregates como parte de
    Integration.
91. Integration Commit no es External System Commit.
92. El contrato no exige Distributed Transaction.
93. El contrato no impone Transactional Outbox.
94. Technical Access al Repository no es Domain Permission.
95. El Repository no incorpora credenciales al estado del Aggregate.
96. External Payload no se persiste automáticamente como estado.
97. Round-trip debe preservar identidad y semántica.
98. Persistencia física no redefine el Domain Model.
99. Nuevas operaciones no deben surgir por conveniencia técnica.
100. Toda evolución del Repository Contract debe preservar el patrón
     consolidado de AURA.

---

# Restricciones

No está permitido:

- ejecutar Commands desde Repository;
- modificar State desde Repository;
- modificar IntegrationId desde Repository;
- incrementar Version arbitrariamente desde Repository;
- modificar CreatedAt desde Repository;
- modificar UpdatedAt por una lectura;
- inventar Domain Events desde Repository;
- corregir Invariants desde Repository;
- decidir Permissions desde Repository;
- autenticar requesters desde Repository;
- persistir un Aggregate inválido;
- persistir parcialmente el Aggregate de forma inconsistente;
- sobrescribir silenciosamente un ConcurrencyConflict;
- ignorar ExpectedVersion cuando corresponda;
- utilizar Last-Write-Wins para evitar Versioning;
- crear Integration mediante findById();
- crear Integration mediante nextIdentity();
- interpretar delete() como DeleteIntegration;
- interpretar delete() como Archived;
- interpretar Archived como orden automática de eliminación;
- introducir Deleted como State por existencia de delete();
- inferir políticas de retención desde el Repository;
- utilizar Repository para publicar Integration Events;
- utilizar Repository como broker;
- utilizar Repository como HTTP Client;
- utilizar Repository como FIWARE Adapter;
- utilizar Repository como Municipal Adapter;
- almacenar otros Aggregates dentro de Integration por conveniencia de
  persistencia;
- persistir un sistema externo como parte embebida del Aggregate;
- convertir automáticamente External Payload en estado del Aggregate;
- fabricar información faltante durante mapping;
- utilizar Read Model como Aggregate recuperado para escritura;
- convertir Repository en motor de búsqueda global;
- convertir Repository en motor de reporting;
- convertir Repository en motor de analytics;
- fusionar Consistency Boundaries por conveniencia de persistencia;
- exigir una base de datos concreta desde el contrato;
- exigir ORM desde el contrato;
- exigir broker desde el contrato;
- exigir FIWARE desde el contrato;
- imponer Event Sourcing desde el contrato;
- imponer Transactional Outbox desde el contrato;
- introducir métodos tecnológicos en el Repository Contract;
- introducir nuevas operaciones sin una necesidad explícita del
  dominio de persistencia.

---

# Compatibilidad Arquitectónica

IntegrationRepository es compatible con:

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
- FIWARE;
- NGSI-LD;
- plataforma municipal;
- mecanismo de publicación.

---

# Definición de Éxito

El Repository Contract del Aggregate **Integration** permite persistir
y recuperar el Aggregate preservando completamente sus reglas de
dominio sin contaminarlo con decisiones de Infrastructure.

El contrato oficial queda definido conceptualmente como:

```text
IntegrationRepository

    save()

    findById()

    exists()

    delete()

    nextIdentity()
```

El modelo garantiza que:

- Integration sea persistida como unidad de consistencia;
- IntegrationId permanezca estable;
- State sea preservado;
- Version sea preservada;
- CreatedAt permanezca inmutable;
- UpdatedAt represente solamente modificaciones válidas;
- el Repository no ejecute Commands;
- el Repository no controle Lifecycle;
- el Repository no controle State Machine;
- el Repository no decida Invariants;
- el Repository no decida Permissions;
- el Repository no produzca Domain Events;
- Optimistic Concurrency proteja modificaciones concurrentes;
- ConcurrencyConflict impida sobrescrituras incompatibles;
- Repository.delete() permanezca separado del Lifecycle;
- Archived permanezca separado de eliminación física;
- las políticas de retención no se infieran;
- Read Models permanezcan separados del Repository del Write Model;
- sistemas externos permanezcan fuera del Consistency Boundary;
- FIWARE permanezca fuera del Repository Contract;
- sistemas municipales permanezcan fuera del Repository Contract;
- la implementación física pueda evolucionar sin modificar la
  semántica del dominio;
- Event Sourcing permanezca compatible pero no obligatorio;
- ninguna tecnología concreta sea impuesta;
- cualquier evolución futura del contrato requiera una necesidad
  explícita y preserve las reglas consolidadas del Aggregate.

De esta forma, `DOMAIN-013G-Repository-Contract.md` establece
formalmente el Repository Contract oficial del Aggregate
**Integration** conforme al patrón consolidado de AURA Core.