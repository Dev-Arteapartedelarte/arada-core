# DOMAIN-009G — Voting Repository Contract

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Voting Management

Aggregate:
Voting

Autor:
ARADA

Documentos relacionados:

- DOMAIN-009-Aggregate.md
- DOMAIN-009A-Lifecycle.md
- DOMAIN-009B-State-Machine.md
- DOMAIN-009C-Commands.md
- DOMAIN-009D-Domain-Events.md
- DOMAIN-009E-Invariants.md
- DOMAIN-009F-Permissions.md
- DOMAIN-009I-Versioning.md
- DOMAIN-009J-Consistency-Boundary.md
- CORE-008-Aggregate-Design-Rules.md
- CORE-011-Repository-Contracts.md
- CORE-016-Dependency-Rules.md

---

# Objetivo

Definir formalmente el **Repository Contract** utilizado para
persistir y recuperar el Aggregate **Voting**.

El Repository representa el contrato mediante el cual el dominio
puede recuperar y persistir Voting sin conocer el mecanismo
concreto de almacenamiento.

El Repository debe preservar:

- identidad del Aggregate;
- estado completo;
- Value Objects;
- entidades internas cuando existan;
- Lifecycle;
- State Machine;
- Invariants;
- Version;
- Consistency Boundary.

El Repository no define comportamiento de negocio.

Tampoco reemplaza a la Aggregate Root.

Debe mantenerse:

```text
Voting Aggregate

↓

Repository Contract

↓

Persistence Implementation
```

La implementación concreta de persistencia permanece fuera del
dominio.

---

# Principios

El Repository de Voting debe cumplir los siguientes principios:

- trabaja con la Aggregate Root completa;
- persiste Voting como una unidad de consistencia;
- recupera Voting como una unidad de consistencia;
- no modifica directamente atributos internos;
- no evita las Invariants;
- no evita Lifecycle;
- no evita State Machine;
- preserva VotingId;
- preserva OrganizationId;
- preserva Version;
- protege la concurrencia optimista;
- no expone detalles de Infrastructure al dominio;
- no constituye un Read Model;
- no modifica otros Aggregates;
- no utiliza consultas de lectura para evitar el Aggregate.

---

# Contrato

El Repository oficial del Aggregate es conceptualmente:

```text
VotingRepository
```

El contrato debe permitir:

```text
getById()

save()

exists()
```

Estas operaciones representan las capacidades mínimas necesarias
para recuperar, persistir y comprobar la existencia de Voting.

La versión 1.0 no introduce operaciones adicionales.

---

# getById()

## Objetivo

Recuperar un Voting existente mediante:

```text
VotingId
```

Conceptualmente:

```text
VotingRepository

↓

getById(VotingId)

↓

Voting
```

---

## Resultado

Cuando Voting existe, getById() debe recuperar el Aggregate
completo necesario para preservar su comportamiento.

Conceptualmente:

```text
Voting

VotingId

OrganizationId

AssemblyId

ProposalId

VotingType

Title

Description

VotingStatus

Rules

Options

Result

Lifecycle Timestamps

Version
```

cuando dichos elementos correspondan al estado persistido del
Aggregate.

---

## Regla

getById() no debe devolver únicamente una representación parcial
cuando esa representación impida ejecutar correctamente el
comportamiento del Aggregate.

Debe mantenerse:

```text
Repository Retrieval

↓

Complete Voting Aggregate
```

---

# exists()

## Objetivo

Determinar si existe un Voting identificado mediante:

```text
VotingId
```

Conceptualmente:

```text
exists(VotingId)
```

produce una respuesta equivalente a:

```text
true

or

false
```

sin modificar el Aggregate.

---

## Uso Conceptual

exists() puede utilizarse cuando el dominio necesite determinar si
una identidad ya se encuentra persistida.

Por ejemplo, durante la creación debe preservarse:

```text
VotingId

↓

Unique Voting
```

La comprobación de existencia no modifica Voting.

---

## Regla

Debe mantenerse:

```text
exists()

↓

Read Only
```

Por lo tanto:

```text
Version Before

=

Version After
```

---

# save()

## Objetivo

Persistir una instancia válida de Voting como una única unidad de
consistencia.

Conceptualmente:

```text
Voting

↓

save()

↓

Persisted Voting
```

---

## Precondición

El Repository recibe un Aggregate cuyo comportamiento de dominio
ya produjo un estado válido.

Debe mantenerse:

```text
Valid Voting

↓

Repository

↓

Persisted Valid Voting
```

El Repository no debe transformar un estado inválido en válido.

---

# Persistencia del Aggregate Completo

Voting debe persistirse como una unidad.

Conceptualmente:

```text
Voting
   │
   ├── Identity
   ├── Organization Context
   ├── Voting Context
   ├── Configuration
   ├── Rules
   ├── Options
   ├── Result
   ├── Lifecycle State
   ├── Timestamps
   └── Version
```

cuando estos elementos pertenezcan al estado actual del
Aggregate.

No deben persistirse partes independientes de forma que puedan
violarse las Invariants.

---

# Unidad de Consistencia

El Repository debe respetar el Consistency Boundary definido por
Voting.

La unidad lógica de persistencia es:

```text
Voting
```

No:

```text
VotingStatus
```

ni:

```text
VotingRules
```

ni:

```text
VotingOptions
```

ni:

```text
VotingResult
```

como unidades de modificación independientes capaces de evitar la
Aggregate Root.

---

# Aggregate Root

El Repository persiste:

```text
Voting
```

como Aggregate Root.

No proporciona mecanismos para modificar directamente elementos
internos evitando comportamiento de dominio.

No debe existir conceptualmente una operación equivalente a:

```text
setVotingStatus()

setVotingVersion()

setVotingResult()

setVotingOrganizationId()
```

dentro del Repository Contract.

---

# Identidad

VotingId debe preservarse durante persistencia y recuperación.

Debe mantenerse:

```text
Persisted VotingId

=

Recovered VotingId
```

El Repository no genera una nueva identidad al recuperar un
Aggregate existente.

---

# OrganizationId

OrganizationId es obligatorio e inmutable dentro de Voting.

Debe mantenerse:

```text
Persisted OrganizationId

=

Recovered OrganizationId
```

El Repository no puede utilizar persistencia para transferir
Voting hacia otra Organization.

---

# Estado

VotingStatus recuperado debe corresponder exactamente al estado
persistido del Aggregate.

Conceptualmente:

```text
Persisted VotingStatus = Open

↓

getById()

↓

VotingStatus = Open
```

La recuperación no ejecuta una transición de State Machine.

---

# Lifecycle

La persistencia debe conservar la información necesaria para
reconstruir correctamente el Lifecycle de Voting.

Los estados oficiales permanecen:

```text
Draft

Open

Closed

Cancelled

Archived
```

El Repository no puede convertir un estado en otro durante la
recuperación.

---

# State Machine

El Repository no ejecuta transiciones de estado.

Debe mantenerse:

```text
Repository

≠

State Machine
```

Las transiciones pertenecen al comportamiento de Voting.

Por tanto, save() no puede utilizarse para introducir una
transición que no haya sido aceptada previamente por la Aggregate
Root.

---

# Invariants

El Repository debe preservar las Invariants definidas en:

```text
DOMAIN-009E-Invariants.md
```

No puede existir una estrategia de persistencia que permita evitar
reglas como:

```text
VotingId immutable

OrganizationId immutable

Valid VotingStatus

Valid Lifecycle

Valid Rules

Valid Options

Valid Result

Valid Version
```

cuando correspondan.

---

# Version

Voting mantiene:

```text
Version
```

como parte de su estado.

El Repository debe preservar la Version exacta del Aggregate.

Conceptualmente:

```text
Voting

Version = N

↓

save()

↓

Persisted Version = N
```

y:

```text
Persisted Version = N

↓

getById()

↓

Voting Version = N
```

---

# Concurrencia Optimista

Voting utiliza control de concurrencia optimista.

Antes de aceptar una escritura sobre un Aggregate previamente
persistido, el Repository debe comprobar que la versión utilizada
para realizar la modificación corresponde con la versión
actualmente persistida.

Conceptualmente:

```text
ExpectedVersion

=

PersistedVersion
```

permite continuar con la persistencia.

Mientras:

```text
ExpectedVersion

!=

PersistedVersion
```

representa un conflicto de concurrencia.

---

# ExpectedVersion

ExpectedVersion representa la versión sobre la cual se produjo la
modificación que intenta persistirse.

Conceptualmente:

```text
Load Voting

Version = N

↓

Execute Valid Command

↓

Voting Version = N + 1

↓

save()

ExpectedVersion = N
```

El Repository compara ExpectedVersion con la versión actualmente
persistida.

---

# Persistencia sin Conflicto

Cuando:

```text
PersistedVersion = N

ExpectedVersion = N
```

la escritura puede continuar.

Después de una modificación válida:

```text
PersistedVersion = N + 1
```

según las reglas definidas en:

```text
DOMAIN-009I-Versioning.md
```

---

# Conflicto de Concurrencia

Cuando:

```text
PersistedVersion != ExpectedVersion
```

la modificación no debe sobrescribir silenciosamente el estado
actual.

Conceptualmente:

```text
PersistedVersion = 7

ExpectedVersion = 6

↓

ConcurrencyConflict
```

La escritura debe ser rechazada.

---

# Ejemplo de Concurrencia

Estado inicial:

```text
Voting

Version = 4
```

Dos operaciones recuperan la misma Version:

```text
Operation A

Version = 4
```

```text
Operation B

Version = 4
```

Operation A completa una modificación válida:

```text
Version = 5
```

y la persiste.

El estado persistido pasa a:

```text
Version = 5
```

Operation B intenta posteriormente persistir una modificación
calculada sobre:

```text
ExpectedVersion = 4
```

Debe obtener:

```text
ConcurrencyConflict
```

Operation B no puede sobrescribir silenciosamente Version 5.

---

# No Last Write Wins

El Repository no puede resolver un conflicto de concurrencia
mediante sobrescritura silenciosa.

No debe mantenerse:

```text
Last Write Wins
```

cuando ello elimine una modificación válida ya persistida.

Debe preservarse el control de Version definido por Voting.

---

# Creación

Cuando un Voting se persiste por primera vez debe preservarse su
identidad única.

Conceptualmente:

```text
VotingId

↓

exists(VotingId)

↓

false

↓

Create Voting

↓

save()
```

Una identidad que ya representa otro Voting no puede reutilizarse
para crear uno nuevo.

---

# Voting Existente

Para una modificación de un Voting existente:

```text
getById(VotingId)

↓

Voting

↓

Domain Command

↓

Valid Modification

↓

save()
```

El Repository no ejecuta el Command.

El Command pertenece al flujo de comportamiento del Aggregate.

---

# Repository y Commands

El Repository no contiene Commands de dominio.

Debe mantenerse:

```text
Command

↓

Voting

↓

Repository
```

No:

```text
Command

↓

Repository

↓

Direct State Modification
```

Commands y Repository poseen responsabilidades distintas.

---

# Repository y Domain Events

Los Domain Events son producidos por Voting como consecuencia de
comportamiento válido.

El Repository no inventa Domain Events para representar
operaciones de persistencia.

Debe mantenerse:

```text
Voting

↓

Domain Event
```

No:

```text
Repository Save

↓

VotingSaved Domain Event
```

La persistencia no constituye por sí misma un hecho del dominio
Voting.

---

# Persistencia y Domain Events

Cuando una modificación válida de Voting produce Domain Events,
estos deben mantener coherencia con la Version resultante del
Aggregate.

Conceptualmente:

```text
Valid Command

↓

Voting Version = N + 1

↓

Domain Event
AggregateVersion = N + 1

↓

Persistence
```

El Repository no modifica el significado del Domain Event.

---

# Repository y Permissions

El Repository no evalúa el modelo conceptual de Permissions de
Voting.

Debe mantenerse:

```text
Permission

↓

Command

↓

Voting

↓

Repository
```

No:

```text
Repository Access

=

Voting Permission
```

La capacidad técnica para acceder a persistencia no constituye una
Permission del dominio.

---

# Repository y Consistency Boundary

El Repository respeta el Consistency Boundary de Voting.

Debe persistir únicamente el Aggregate Voting como la unidad de
consistencia correspondiente.

No debe incorporar dentro de la misma unidad de persistencia de
dominio los Aggregates:

```text
Organization

Citizen

Membership

Role

Territory

Assembly

Proposal

Participation

Document

Notification

Audit

Integration
```

Estos mantienen sus propios límites.

---

# Referencias Externas

Voting puede mantener referencias mediante identificadores como:

```text
OrganizationId

AssemblyId

ProposalId
```

cuando correspondan.

El Repository persiste dichas referencias como parte del estado de
Voting.

No persiste los Aggregates externos como entidades internas de
Voting.

Debe mantenerse:

```text
AssemblyId

≠

Assembly Aggregate
```

y:

```text
ProposalId

≠

Proposal Aggregate
```

---

# Repository y Otros Aggregates

VotingRepository administra exclusivamente:

```text
Voting
```

No administra:

```text
Organization

Citizen

Membership

Role

Territory

Assembly

Proposal

Participation

Document

Notification

Audit

Integration
```

Un Repository no constituye una vía para modificar múltiples
Aggregates desde Voting.

---

# Fuente de Verdad

El Repository recupera la representación persistida necesaria para
reconstruir la fuente de verdad del Write Model de Voting.

Los Read Models no reemplazan esta responsabilidad.

Debe mantenerse:

```text
Voting Aggregate

≠

Voting Read Model
```

---

# Repository y Read Model

El Repository Contract definido en este documento pertenece al
Aggregate Voting.

Los Read Models poseen responsabilidades de consulta y permanecen
separados.

No debe utilizarse:

```text
VotingRepository
```

como mecanismo para convertir una proyección en autoridad de
escritura.

Igualmente, un Read Model no puede modificar Voting.

---

# Consultas

El Repository Contract versión 1.0 mantiene exclusivamente:

```text
getById()

save()

exists()
```

Las necesidades de consulta especializadas pertenecen a:

```text
DOMAIN-009L-Read-Model.md
```

cuando correspondan.

El Repository del Aggregate no debe expandirse con operaciones de
consulta únicamente para resolver necesidades propias del Read
Side.

---

# Rehidratación

getById() debe permitir reconstruir Voting manteniendo su estado
persistido.

La rehidratación:

- no representa un Command;
- no representa una modificación;
- no cambia VotingStatus;
- no incrementa Version;
- no genera nuevos Domain Events;
- no ejecuta nuevamente transiciones del Lifecycle.

Debe mantenerse:

```text
Persisted State

↓

Rehydrate

↓

Equivalent Domain State
```

---

# Rehidratación de Version

Si el estado persistido contiene:

```text
Version = N
```

la instancia recuperada debe mantener:

```text
Version = N
```

No:

```text
Version = N + 1
```

La recuperación no es una modificación del dominio.

---

# Rehidratación de Timestamps

Los timestamps históricos deben conservar exactamente el
significado persistido.

Por ejemplo:

```text
OpenedAt

ClosedAt

CancelledAt

ArchivedAt
```

no deben cambiar como consecuencia de getById().

---

# Atomicidad Conceptual

save() debe representar la persistencia de una modificación lógica
completa del Aggregate.

Conceptualmente:

```text
Voting State

+

Lifecycle Data

+

Version
```

deben persistirse de manera coherente respecto de la misma
modificación válida.

No puede confirmarse una parte dejando el Aggregate persistido en
un estado incompatible con sus Invariants.

---

# Operación Fallida

Una operación de persistencia que no puede completarse no debe
considerarse una persistencia válida.

Debe mantenerse:

```text
save()

↓

Success
```

o:

```text
save()

↓

Failure
```

sin considerar exitoso un estado parcialmente persistido que viole
el Consistency Boundary.

---

# Duplicate Identity

La creación de un nuevo Voting no puede reemplazar silenciosamente
un Aggregate existente con el mismo VotingId.

Debe mantenerse:

```text
Existing VotingId

+

Create New Voting with Same VotingId

=

Rejected
```

La identidad pertenece al dominio y no puede reutilizarse.

---

# PersistenceFailure

Cuando la persistencia no puede completarse, el resultado no debe
interpretarse como una escritura confirmada.

Conceptualmente:

```text
PersistenceFailure

↓

No Confirmed Persistence
```

Una falla de persistencia no crea por sí misma un nuevo estado de
Lifecycle.

---

# ConcurrencyConflict

ConcurrencyConflict representa una escritura incompatible con la
Version actualmente persistida.

Debe mantenerse:

```text
ExpectedVersion != PersistedVersion

↓

ConcurrencyConflict
```

El conflicto no modifica silenciosamente el estado persistido.

---

# Independencia Tecnológica

VotingRepository representa un contrato del dominio.

Voting no conoce si el contrato es implementado mediante:

```text
Database

Document Store

Event Store

File Storage

Memory
```

ni mediante otra tecnología de persistencia.

La tecnología concreta no modifica la semántica del contrato.

---

# Dependencias Prohibidas

El contrato del dominio no debe depender directamente de:

```text
SQL

ORM

MongoDB

PostgreSQL

HTTP

REST

GraphQL

Frameworks
```

Estas tecnologías pueden participar en implementaciones externas.

No forman parte de la semántica de VotingRepository.

---

# Repository como Contrato

Debe mantenerse:

```text
Domain

↓

Repository Contract
```

mientras:

```text
Infrastructure

↓

Repository Implementation
```

La implementación satisface el contrato.

El dominio no depende de la implementación concreta.

---

# Compatibilidad con Versioning

El Repository Contract debe mantener coherencia con:

```text
DOMAIN-009I-Versioning.md
```

Debe preservar:

- Version actual;
- ExpectedVersion;
- control de concurrencia optimista;
- rechazo de escrituras obsoletas;
- ausencia de sobrescritura silenciosa.

---

# Compatibilidad con Consistency Boundary

El Repository Contract debe mantener coherencia con:

```text
DOMAIN-009J-Consistency-Boundary.md
```

Debe persistir Voting como una única unidad de consistencia y no
expandir su límite hacia otros Aggregates.

---

# Compatibilidad con CQRS

VotingRepository pertenece conceptualmente al Write Model del
Aggregate.

Debe mantenerse:

```text
Write Side

Voting Aggregate

↓

VotingRepository
```

Las necesidades especializadas del Read Side pertenecen a los Read
Models.

---

# Compatibilidad con Event Sourcing

El contrato no impide que una implementación futura compatible con
AURA pueda reconstruir Voting a partir de su historial de Domain
Events.

Sin embargo, la semántica del Repository continúa siendo:

```text
Recover Voting Aggregate

Persist Voting Aggregate
```

La estrategia concreta de persistencia no modifica las reglas del
dominio.

---

# Restricciones

No está permitido:

- persistir VotingId diferente al de la Aggregate Root;
- modificar VotingId durante persistencia;
- modificar OrganizationId durante persistencia;
- modificar VotingStatus desde el Repository;
- modificar Version arbitrariamente;
- evitar ExpectedVersion;
- sobrescribir silenciosamente una modificación concurrente;
- persistir un cambio parcial que viole Invariants;
- utilizar Repository para evitar Lifecycle;
- utilizar Repository para evitar State Machine;
- utilizar Repository para evitar Commands;
- utilizar Repository para evitar Permissions;
- utilizar Repository para modificar otros Aggregates;
- incorporar Aggregates externos completos dentro de Voting;
- ejecutar comportamiento de negocio dentro de getById();
- ejecutar comportamiento de negocio dentro de exists();
- utilizar getById() como una transición de Lifecycle;
- incrementar Version durante una lectura;
- generar Domain Events nuevos durante rehidratación;
- utilizar Read Models como fuente de escritura;
- agregar operaciones de consulta especializadas al Repository para
  reemplazar el Read Model;
- exponer detalles concretos de Infrastructure dentro del contrato
  del dominio;
- considerar una persistencia parcial como una escritura válida;
- reutilizar VotingId para representar otro Voting.

---

# Reglas

## REG-001

VotingRepository administra exclusivamente el Aggregate Voting.

---

## REG-002

El Repository debe trabajar con Voting como una unidad de
consistencia.

---

## REG-003

Las operaciones oficiales de la versión 1.0 son:

```text
getById()

save()

exists()
```

---

## REG-004

getById() debe recuperar el Aggregate necesario para preservar
correctamente su comportamiento e Invariants.

---

## REG-005

exists() no modifica el Aggregate ni Version.

---

## REG-006

save() persiste únicamente estados válidos producidos por el
Aggregate.

---

## REG-007

VotingId debe preservarse durante persistencia y recuperación.

---

## REG-008

OrganizationId debe preservarse durante persistencia y recuperación.

---

## REG-009

Version debe preservarse durante persistencia y recuperación.

---

## REG-010

Toda escritura sobre un Voting existente debe respetar el control
de concurrencia optimista.

---

## REG-011

Cuando ExpectedVersion no coincide con PersistedVersion debe
producirse:

```text
ConcurrencyConflict
```

---

## REG-012

El Repository no puede sobrescribir silenciosamente una
modificación concurrente confirmada.

---

## REG-013

La rehidratación no incrementa Version ni genera nuevos Domain
Events.

---

## REG-014

El Repository no puede modificar directamente VotingStatus.

---

## REG-015

El Repository no puede utilizarse para evitar Lifecycle, State
Machine o Invariants.

---

## REG-016

El Repository no modifica directamente otros Aggregates.

---

## REG-017

VotingRepository no constituye un Read Model.

---

## REG-018

Las necesidades de consulta especializadas deben permanecer
separadas del Repository del Aggregate.

---

## REG-019

La implementación concreta de persistencia permanece fuera del
dominio.

---

## REG-020

La persistencia debe conservar el Consistency Boundary completo de
Voting.

---

# Definición de Éxito

El Repository Contract del Aggregate **Voting** permite recuperar y
persistir Voting sin introducir dependencias de Infrastructure
dentro del dominio.

El contrato oficial mantiene:

```text
VotingRepository

getById()

save()

exists()
```

y garantiza que:

- Voting se persiste como una unidad de consistencia;
- Voting se recupera como un Aggregate coherente;
- VotingId permanece estable;
- OrganizationId permanece inmutable;
- VotingStatus conserva su semántica;
- Lifecycle permanece intacto;
- State Machine no puede evitarse mediante persistencia;
- Invariants permanecen protegidas;
- Version se conserva correctamente;
- ExpectedVersion protege la concurrencia optimista;
- los conflictos concurrentes no producen sobrescrituras
  silenciosas;
- la rehidratación no constituye una modificación;
- los Domain Events no son inventados por el Repository;
- los Read Models permanecen separados;
- otros Aggregates permanecen fuera del Consistency Boundary;
- la tecnología concreta de persistencia permanece fuera del
  dominio.

De esta forma, `DOMAIN-009G-Repository-Contract.md` establece el
contrato conceptual oficial de persistencia del Aggregate
**Voting**, manteniendo la independencia tecnológica, el control de
concurrencia y el patrón consolidado de AURA Core.