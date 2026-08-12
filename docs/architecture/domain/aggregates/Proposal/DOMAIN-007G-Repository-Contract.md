# DOMAIN-007G — Proposal Repository Contract

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
- DOMAIN-007I-Versioning.md
- DOMAIN-007J-Consistency-Boundary.md
- CORE-003-Shared-Kernel.md
- CORE-004-Ubiquitous-Language.md
- CORE-006-Domain-Invariants.md
- CORE-008-Aggregate-Design-Rules.md
- CORE-011-Repository-Contracts.md

---

# Objetivo

Definir el contrato conceptual oficial del Repository del
Aggregate **Proposal**.

El Repository proporciona la abstracción mediante la cual el
dominio puede recuperar y persistir una Proposal sin conocer el
mecanismo tecnológico utilizado para almacenar su estado.

El Repository protege la separación entre:

```text
Domain

and

Infrastructure
```

Su responsabilidad consiste exclusivamente en trabajar con el
Aggregate completo como unidad de persistencia.

Este documento establece:

- responsabilidad del Repository;
- límites del contrato;
- operaciones conceptuales permitidas;
- reglas de recuperación;
- reglas de persistencia;
- reglas de existencia;
- reglas de identidad;
- reglas de versionado;
- reglas de concurrencia;
- relación con Domain Events;
- relación con Unit of Work;
- comportamiento ante errores;
- independencia tecnológica;
- restricciones arquitectónicas.

El Repository no contiene lógica de negocio.

Las reglas del dominio permanecen exclusivamente bajo la
responsabilidad del Aggregate Proposal.

---

# Propósito

El propósito de ProposalRepository es proporcionar una
abstracción de persistencia coherente con el modelo DDD de AURA.

Conceptualmente:

```text
Application Service

↓

ProposalRepository

↓

Proposal Aggregate

↓

Infrastructure Persistence
```

El dominio conoce:

```text
ProposalRepository
```

pero no conoce:

```text
Database

ORM

Driver

Collection

Table

Document Store

External API
```

La implementación concreta pertenece a Infrastructure.

---

# Principios

El Repository de Proposal cumple los siguientes principios:

- existe un Repository por Aggregate Root;
- trabaja exclusivamente con Proposal como Aggregate Root;
- recupera Aggregates completos;
- persiste Aggregates completos;
- utiliza identidad de dominio;
- respeta el límite de consistencia;
- preserva Version;
- participa en el control de concurrencia optimista;
- no expone detalles de persistencia;
- no contiene lógica de negocio;
- no ejecuta Commands;
- no decide transiciones de estado;
- no valida permisos;
- no publica Integration Events;
- no implementa reglas de autorización;
- no modifica otros Aggregates;
- permanece independiente de frameworks;
- permanece independiente de motores de persistencia.

---

# Repository

El contrato conceptual es:

```text
ProposalRepository
```

ProposalRepository representa una abstracción del dominio.

No representa:

```text
ProposalTable

ProposalCollection

ProposalDocumentStore

ProposalORM

ProposalDAO
```

El Repository opera utilizando conceptos del lenguaje ubicuo.

---

# Aggregate Administrado

ProposalRepository administra exclusivamente:

```text
Proposal
```

Proposal constituye:

```text
Aggregate Root
```

Por lo tanto:

```text
ProposalRepository

↓

Proposal
```

No debe existir acceso de persistencia externo hacia partes
internas del Aggregate que permita evitar su raíz.

---

# Regla Fundamental

Toda persistencia modificadora debe operar sobre:

```text
Proposal Aggregate
```

como unidad completa de consistencia.

No está permitido conceptualmente:

```text
update proposal_status directly
```

ni:

```text
update proposal_content directly
```

ni:

```text
increment version directly
```

desde fuera del Aggregate.

El flujo correcto es:

```text
Load Proposal

↓

Execute Domain Behavior

↓

Validate Invariants

↓

Produce Domain Events

↓

Save Proposal
```

---

# Contrato Conceptual

ProposalRepository expone conceptualmente las siguientes
operaciones:

```text
getById()

exists()

save()
```

Estas operaciones constituyen el contrato mínimo necesario para
trabajar con Proposal como Aggregate Root.

Las implementaciones pueden proporcionar mecanismos internos
adicionales siempre que estos no sean expuestos como capacidades
que permitan violar el modelo del dominio.

---

# getById

## Objetivo

Recuperar una Proposal mediante su identidad.

Firma conceptual:

```text
getById(
    ProposalId
) → Proposal | NotFound
```

La operación recibe:

```text
ProposalId
```

y devuelve:

```text
Proposal
```

cuando existe.

---

# Reglas de getById

`getById()` debe:

- utilizar ProposalId como identidad de dominio;
- recuperar el Aggregate correspondiente;
- reconstruir un estado válido de Proposal;
- preservar su identidad;
- preservar su estado;
- preservar su Version;
- devolver el Aggregate completo;
- mantener ocultos los detalles de persistencia.

`getById()` no debe:

- modificar Proposal;
- incrementar Version;
- ejecutar Commands;
- producir Domain Events de modificación;
- aplicar transiciones de estado;
- retornar una representación parcial como sustituto del
  Aggregate;
- exponer entidades de persistencia;
- exponer modelos ORM;
- exponer documentos de base de datos.

---

# Proposal No Encontrada

Cuando ProposalId no corresponda a una Proposal existente, el
Repository debe expresar conceptualmente:

```text
ProposalNotFound
```

La ausencia de Proposal no debe representarse mediante una
Proposal artificial o parcialmente inicializada.

No debe utilizarse:

```text
Proposal(
    invalid_state
)
```

para representar inexistencia.

La inexistencia constituye una condición explícita del contrato.

---

# Reconstrucción del Aggregate

Al recuperar una Proposal, el Repository debe reconstruir un
Aggregate coherente con el estado persistido.

Conceptualmente:

```text
Persistence Representation

↓

Repository Mapping

↓

Proposal Aggregate
```

La reconstrucción debe preservar:

```text
ProposalId

OrganizationId

AuthorId

TerritoryId

AssemblyId

ProposalType

ProposalName

ProposalPurpose

ProposalDescription

ProposalContent

ProposalStatus

CreatedAt

UpdatedAt

SubmittedAt

ReviewStartedAt

DecidedAt

WithdrawnAt

ArchivedAt

Version
```

cuando dichos conceptos formen parte del estado oficial definido
por el Aggregate.

---

# Regla de Reconstrucción

La reconstrucción desde persistencia no representa la creación de
una nueva Proposal desde la perspectiva del dominio.

Por lo tanto:

```text
Repository Reconstruction
```

no debe producir:

```text
ProposalCreated
```

ni ejecutar nuevamente:

```text
CreateProposal
```

El Repository reconstruye un Aggregate existente.

No recrea el hecho de dominio que originalmente produjo su
existencia.

---

# Estado Válido después de Recuperación

Una Proposal recuperada debe encontrarse en un estado compatible
con:

```text
DOMAIN-007-Aggregate.md

DOMAIN-007A-Lifecycle.md

DOMAIN-007B-State-Machine.md

DOMAIN-007E-Invariants.md
```

El Repository no debe entregar al dominio una Proposal
estructuralmente inválida.

La representación persistida debe poder reconstruirse sin
romper las invariantes estructurales del Aggregate.

---

# exists

## Objetivo

Determinar si existe una Proposal con una identidad determinada.

Firma conceptual:

```text
exists(
    ProposalId
) → Boolean
```

Resultado:

```text
true
```

cuando la identidad existe.

Resultado:

```text
false
```

cuando la identidad no existe.

---

# Reglas de exists

`exists()`:

- consulta existencia mediante ProposalId;
- no recupera necesariamente el Aggregate completo;
- no modifica estado;
- no incrementa Version;
- no produce Domain Events;
- no ejecuta lógica de negocio;
- no sustituye getById cuando el Aggregate necesita ser
  modificado.

Debe mantenerse:

```text
exists()

≠

Load Aggregate For Modification
```

---

# save

## Objetivo

Persistir el estado completo y válido de Proposal.

Firma conceptual:

```text
save(
    Proposal,
    ExpectedVersion
) → Persisted
```

El Repository recibe una instancia válida de:

```text
Proposal
```

y la persiste como una única unidad lógica.

---

# Reglas de save

`save()` debe:

- persistir Proposal como Aggregate completo;
- preservar ProposalId;
- preservar OrganizationId;
- persistir el estado resultante del comportamiento de dominio;
- respetar Version;
- validar ExpectedVersion;
- detectar conflictos de concurrencia;
- mantener atomicidad sobre el límite del Aggregate;
- persistir únicamente estados válidos;
- evitar actualizaciones parciales observables;
- mantener la consistencia del Aggregate.

`save()` no debe:

- decidir reglas de negocio;
- ejecutar Commands;
- cambiar ProposalStatus por iniciativa propia;
- modificar ProposalContent;
- corregir automáticamente valores;
- modificar OrganizationId;
- modificar ProposalId;
- generar nuevas decisiones de dominio;
- evitar las invariantes;
- modificar otros Aggregates.

---

# Aggregate Completo

El Repository persiste:

```text
Proposal
```

como una unidad.

No debe ofrecer operaciones públicas como:

```text
updateStatus()

updateContent()

updateAssemblyId()

updateTerritoryId()

incrementVersion()

updateDecision()
```

Estas operaciones permitirían modificar partes del Aggregate sin
pasar por el comportamiento de Proposal.

La única modificación válida sigue el flujo:

```text
Proposal Behavior

↓

Valid Aggregate State

↓

Repository.save()
```

---

# Persistencia Atómica

La persistencia de Proposal debe ser atómica respecto de su
límite de consistencia.

Conceptualmente:

```text
Save Proposal
```

debe producir:

```text
All Aggregate State Persisted
```

o:

```text
No Aggregate State Persisted
```

No debe existir un resultado observable como:

```text
ProposalStatus persisted

but

Version not persisted
```

o:

```text
ProposalContent persisted

but

ProposalStatus not persisted
```

---

# Unidad de Persistencia

La unidad lógica de persistencia es:

```text
Proposal Aggregate
```

No:

```text
Proposal Attribute
```

No:

```text
Proposal Value Object
```

No:

```text
Proposal Internal Component
```

El límite de persistencia debe respetar el límite de consistencia
establecido en:

```text
DOMAIN-007J-Consistency-Boundary.md
```

---

# Identidad

ProposalRepository utiliza:

```text
ProposalId
```

como identidad oficial del Aggregate.

ProposalId:

- pertenece al dominio;
- es único;
- es inmutable;
- no depende de la tecnología de persistencia;
- no debe ser sustituido por una identidad técnica de
  infraestructura.

Una implementación puede mantener identificadores internos de
almacenamiento cuando sean necesarios, pero estos no sustituyen:

```text
ProposalId
```

como identidad del dominio.

---

# OrganizationId

ProposalRepository debe preservar:

```text
OrganizationId
```

como parte del estado del Aggregate.

OrganizationId es inmutable durante la vida de Proposal.

El Repository no puede utilizar una operación de persistencia
para cambiar la Organization propietaria.

Debe mantenerse:

```text
Persisted.OrganizationId
    =
Aggregate.OrganizationId
```

y cualquier intento de alterar esa identidad fuera del dominio
debe ser rechazado.

---

# Referencias Externas

Proposal puede mantener referencias mediante identificadores
como:

```text
OrganizationId

AuthorId

TerritoryId

AssemblyId
```

El Repository persiste estas referencias como parte del estado de
Proposal.

No recupera automáticamente los Aggregates externos.

Debe mantenerse:

```text
ProposalRepository

↓

Proposal
```

No:

```text
ProposalRepository

↓

Proposal
+
Organization
+
Citizen
+
Territory
+
Assembly
```

Los límites de Aggregate permanecen independientes.

---

# No Carga de Aggregates Externos

La recuperación de Proposal no debe convertir las referencias
externas en Aggregates cargados dentro de Proposal.

Por ejemplo:

```text
TerritoryId
```

permanece una referencia.

No debe convertirse automáticamente en:

```text
Territory Aggregate
```

dentro de Proposal.

Lo mismo aplica a:

```text
OrganizationId

AuthorId

AssemblyId
```

Esta regla protege el límite de consistencia.

---

# Version

ProposalRepository debe preservar:

```text
Version
```

Version representa la versión lógica del Aggregate utilizada para
control de concurrencia optimista.

La versión persistida debe corresponder al estado persistido de
Proposal.

No puede modificarse arbitrariamente desde Infrastructure.

---

# ExpectedVersion

Toda persistencia modificadora debe comprobar conceptualmente:

```text
ExpectedVersion
```

contra:

```text
PersistedVersion
```

Antes de aceptar una escritura:

```text
ExpectedVersion
    =
PersistedVersion
```

debe cumplirse.

Cuando la condición es válida:

```text
Save Accepted
```

Cuando no se cumple:

```text
Save Rejected
```

---

# Concurrencia Optimista

ProposalRepository participa en el mecanismo de concurrencia
optimista definido para Proposal.

Flujo conceptual:

```text
Load Proposal

↓

CurrentVersion = 12

↓

Execute Command

↓

Proposal Version = 13

↓

save(
    Proposal,
    ExpectedVersion = 12
)

↓

Repository checks persisted version
```

Si:

```text
PersistedVersion = 12
```

entonces:

```text
Persist Proposal Version 13
```

Si:

```text
PersistedVersion ≠ 12
```

entonces:

```text
Concurrency Conflict
```

---

# Conflicto de Concurrencia

Cuando ExpectedVersion no coincide con la versión persistida, el
Repository debe expresar conceptualmente:

```text
ProposalConcurrencyConflict
```

En ese caso:

```text
Proposal Persistence
    =
Rejected
```

El Repository no debe:

- sobrescribir silenciosamente el estado más reciente;
- ignorar la diferencia de Version;
- reducir Version;
- forzar la escritura;
- fusionar automáticamente decisiones de dominio.

---

# Regla de No Last-Write-Wins

No está permitido utilizar:

```text
Last Write Wins
```

como comportamiento que permita sobrescribir silenciosamente una
modificación concurrente del Aggregate.

Debe mantenerse:

```text
ExpectedVersion
    ≠
PersistedVersion

↓

Conflict
```

No:

```text
ExpectedVersion
    ≠
PersistedVersion

↓

Overwrite
```

Esta regla protege decisiones concurrentes sobre Proposal.

---

# Ejemplo de Conflicto

Estado inicial:

```text
ProposalStatus = UnderReview

Version = 20
```

Proceso A carga:

```text
Version = 20
```

Proceso B carga:

```text
Version = 20
```

Proceso A ejecuta:

```text
AcceptProposal
```

Resultado:

```text
ProposalStatus = Accepted

Version = 21
```

Proceso A persiste:

```text
ExpectedVersion = 20
```

La escritura es aceptada.

Posteriormente Proceso B intenta:

```text
RejectProposal
```

sobre la copia que había cargado con:

```text
Version = 20
```

Aunque localmente produzca:

```text
ProposalStatus = Rejected

Version = 21
```

al intentar persistir:

```text
ExpectedVersion = 20
```

el Repository encuentra:

```text
PersistedVersion = 21
```

Resultado:

```text
ProposalConcurrencyConflict
```

La Proposal persistida permanece:

```text
Accepted

Version = 21
```

---

# Versionado

Las reglas completas de versionado se desarrollan en:

```text
DOMAIN-007I-Versioning.md
```

ProposalRepository debe respetar ese modelo.

El Repository participa en la persistencia y comparación de
Version, pero no redefine las reglas conceptuales de versionado.

---

# Creación y Persistencia Inicial

Una Proposal recién creada mediante:

```text
CreateProposal
```

puede ser persistida mediante:

```text
save()
```

La persistencia inicial debe garantizar que:

```text
ProposalId
```

no corresponda a otra Proposal existente.

Una identidad duplicada debe producir un conflicto explícito.

---

# Identidad Duplicada

Cuando se intenta persistir una nueva Proposal utilizando un
ProposalId ya existente:

```text
ProposalId

Already Exists
```

la operación debe ser rechazada.

Conceptualmente:

```text
ProposalIdentityConflict
```

No debe sobrescribirse una Proposal existente como consecuencia
de una creación con identidad duplicada.

---

# Unicidad

Las reglas de unicidad pertenecientes al dominio deben
preservarse durante la persistencia.

El Repository puede participar técnicamente en la protección de
restricciones que requieran garantías de almacenamiento.

Sin embargo, la existencia de una restricción técnica no
transforma al Repository en propietario de la regla de negocio.

Debe mantenerse:

```text
Domain Rule

↓

Domain Model
```

mientras:

```text
Persistence Constraint

↓

Infrastructure Enforcement
```

puede actuar como protección complementaria.

---

# Domain Events

Proposal puede producir Domain Events durante la ejecución de su
comportamiento.

Ejemplo:

```text
Proposal

↓

AcceptProposal

↓

ProposalAccepted
```

El Repository no inventa Domain Events.

El Repository no decide qué evento corresponde a una
modificación.

Los eventos son consecuencia del comportamiento del Aggregate.

---

# Eventos Pendientes

Cuando Proposal mantiene Domain Events pendientes de publicación,
la persistencia debe preservar la coherencia entre:

```text
Aggregate State
```

y:

```text
Domain Events Produced
```

El Repository no puede sustituir los eventos producidos por
Proposal por eventos inferidos desde diferencias de persistencia.

Debe mantenerse:

```text
Aggregate Behavior

↓

Domain Event
```

No:

```text
Database Difference

↓

Invent Domain Event
```

---

# Persistencia y Publicación de Eventos

El Repository persiste el Aggregate.

La publicación efectiva de eventos puede ser coordinada por los
mecanismos establecidos por la arquitectura.

Conceptualmente:

```text
Command

↓

Proposal

↓

Domain Event

↓

Repository.save()

↓

Commit

↓

Event Publication
```

La persistencia del Aggregate y la entrega de eventos deben
mantener la consistencia definida por la arquitectura.

El Repository no convierte Integration Events en parte interna
del Aggregate.

---

# Eventos ante Fallo de Persistencia

Si la persistencia falla:

```text
save()

↓

Failure
```

no debe considerarse confirmada una modificación persistida del
Aggregate.

Los eventos asociados a esa modificación no deben interpretarse
como hechos confirmados externamente antes de que el cambio haya
sido aceptado por la unidad de persistencia correspondiente.

Debe mantenerse:

```text
Persistence Failure

↓

No Confirmed External Publication
```

---

# Unit of Work

ProposalRepository puede participar conceptualmente en una:

```text
Unit of Work
```

cuando la arquitectura de persistencia lo requiera.

La Unit of Work coordina:

```text
Load

↓

Domain Execution

↓

Save

↓

Commit
```

El uso de Unit of Work no modifica las responsabilidades del
Aggregate ni del Repository.

---

# Responsabilidad de Unit of Work

Cuando exista una Unit of Work, esta puede coordinar:

- inicio de unidad transaccional;
- seguimiento de Aggregate cargado;
- persistencia;
- commit;
- rollback;
- coordinación de eventos pendientes.

La Unit of Work no debe:

- contener reglas de Proposal;
- decidir transiciones;
- modificar ProposalStatus;
- ignorar Version;
- alterar invariantes.

---

# Regla de Una Transacción por Aggregate

Una modificación de Proposal debe persistirse dentro de una única
unidad transaccional correspondiente a su límite de consistencia.

Conceptualmente:

```text
One Proposal Modification

↓

One Aggregate Transaction
```

No debe requerirse una transacción distribuida que modifique
simultáneamente:

```text
Proposal

+

Assembly

+

Territory

+

Voting
```

Cada Aggregate mantiene su propio límite de consistencia.

---

# No Transacciones Distribuidas entre Aggregates

ProposalRepository no debe asumir atomicidad conjunta con
Repositories de otros Aggregates.

No debe diseñarse:

```text
ProposalRepository.save()

and

AssemblyRepository.save()

and

VotingRepository.save()

as one Aggregate transaction
```

La coordinación entre Aggregates debe respetar el modelo de
consistencia establecido por AURA.

---

# Consistencia Eventual entre Aggregates

Cuando una modificación de Proposal requiera producir efectos en
otros Aggregates o Bounded Contexts, la coordinación puede
utilizar:

```text
Domain Events

Integration Events

Application Services
```

según corresponda.

ProposalRepository continúa persistiendo exclusivamente:

```text
Proposal
```

---

# Relación con Commands

Los Commands definidos en:

```text
DOMAIN-007C-Commands.md
```

no son ejecutados por el Repository.

Flujo correcto:

```text
Command

↓

Application Service

↓

ProposalRepository.getById()

↓

Proposal Behavior

↓

ProposalRepository.save()
```

El Repository no contiene métodos como:

```text
acceptProposal()

rejectProposal()

submitProposal()

withdrawProposal()
```

Estas operaciones representan comportamiento del dominio, no
persistencia.

---

# Relación con Permissions

Los permisos definidos en:

```text
DOMAIN-007F-Permissions.md
```

no son responsabilidad del Repository.

El Repository no decide:

```text
Who may save?
```

en términos de autorización del dominio.

La autorización ocurre antes de ejecutar el comportamiento
protegido.

El Repository protege exclusivamente las reglas de persistencia
que forman parte de su contrato.

---

# Relación con Invariantes

Las invariantes definidas en:

```text
DOMAIN-007E-Invariants.md
```

son responsabilidad del Aggregate.

ProposalRepository no debe duplicar la lógica completa de esas
invariantes.

Sin embargo, nunca debe persistir deliberadamente un estado que
viole el contrato estructural del Aggregate.

Debe mantenerse:

```text
Proposal

↓

Valid Domain State

↓

Repository.save()
```

---

# Relación con State Machine

ProposalRepository no conoce decisiones de transición.

No debe contener reglas como:

```text
if status == Submitted:
    allow UnderReview
```

Estas reglas pertenecen a:

```text
DOMAIN-007B-State-Machine.md
```

El Repository persiste el estado resultante después de que
Proposal haya validado la transición.

---

# Relación con Lifecycle

ProposalRepository no controla el Lifecycle.

Estados como:

```text
Draft

Submitted

UnderReview

Accepted

Rejected

Withdrawn

Archived
```

son conceptos del Aggregate.

El Repository los persiste.

No decide cuándo deben producirse.

---

# Consulta y Modificación

Cuando una Proposal necesita ser modificada, debe recuperarse
como Aggregate mediante:

```text
getById()
```

La modificación se realiza sobre:

```text
Proposal
```

y posteriormente:

```text
save()
```

No debe utilizarse un Read Model como sustituto del Aggregate
para ejecutar comportamiento de escritura.

---

# Repository y Read Models

ProposalRepository pertenece al lado de escritura del modelo.

Los Read Models poseen responsabilidades diferentes.

Debe mantenerse:

```text
Write Side

ProposalRepository

↓

Proposal Aggregate
```

y:

```text
Read Side

Proposal Read Models
```

Las consultas optimizadas no deben obligar a expandir el contrato
del Repository de escritura.

---

# Consultas Complejas

Consultas como:

```text
Proposals by Territory

Proposals by Assembly

Proposals by Status

Proposals by Author

Proposal Statistics

Proposal Dashboard
```

no deben incorporarse automáticamente a ProposalRepository si su
propósito corresponde al modelo de lectura.

Estas consultas deben resolverse mediante:

```text
Read Models
```

cuando así lo establezca la arquitectura CQRS.

---

# Separación CQRS

Debe mantenerse:

```text
ProposalRepository

=

Aggregate Persistence
```

No:

```text
ProposalRepository

=

Aggregate Persistence
+
Reporting
+
Analytics
+
Search Engine
+
Dashboard Queries
```

Esta separación mantiene el Repository enfocado en el Aggregate
Root.

---

# Búsqueda por Identidad

La operación principal de recuperación para modificación es:

```text
getById(ProposalId)
```

La identidad del Aggregate constituye el mecanismo oficial para
recuperar una Proposal que será modificada.

Las búsquedas por criterios secundarios pertenecen
preferentemente a modelos de consulta cuando no sean necesarias
para proteger una regla del dominio.

---

# Dependencias del Contrato

ProposalRepository puede depender conceptualmente de:

```text
Proposal

ProposalId

Version

Domain Repository Contracts
```

No debe depender conceptualmente de:

```text
SQL

Mongo Query

ORM Session

HTTP Client

Redis Client

Elasticsearch Client

Framework Repository
```

---

# Dirección de Dependencias

La dirección arquitectónica debe ser:

```text
Infrastructure

↓

implements

↓

ProposalRepository
```

No:

```text
ProposalRepository

↓

depends on Infrastructure
```

El contrato pertenece a una capa interior.

La implementación pertenece a una capa exterior.

---

# Implementación

Una implementación concreta puede utilizar:

- PostgreSQL;
- MongoDB;
- MySQL;
- SQLite;
- Event Store;
- almacenamiento documental;
- almacenamiento distribuido;
- otros mecanismos compatibles.

La elección tecnológica pertenece a Infrastructure.

El contrato conceptual no cambia por utilizar un motor de
persistencia diferente.

---

# Independencia de ORM

ProposalRepository no depende conceptualmente de un ORM.

Una implementación puede utilizar un ORM internamente.

Sin embargo, el dominio no debe recibir:

```text
ORM Entity

ORM Session

ORM Query

ORM Model
```

El Repository transforma las representaciones necesarias hacia:

```text
Proposal
```

---

# Independencia de Base de Datos

Proposal no debe conocer si se encuentra almacenada en:

```text
PostgreSQL

MongoDB

MySQL

SQLite

Event Store
```

El Repository abstrae esta decisión.

Cambiar el mecanismo de almacenamiento no debe exigir modificar
las reglas internas del Aggregate.

---

# Independencia de HTTP

ProposalRepository no representa una API HTTP.

No define:

```text
GET

POST

PUT

PATCH

DELETE
```

No conoce:

```text
Routes

Controllers

Status Codes

Headers
```

La exposición mediante HTTP pertenece a capas externas.

---

# Independencia de FIWARE

ProposalRepository no depende directamente de:

```text
FIWARE

Orion-LD

NGSI-LD

Keyrock

PEP Proxy
```

Si Proposal debe interoperar con FIWARE, esa responsabilidad
pertenece a los mecanismos de Integration correspondientes.

La persistencia del Aggregate y su interoperabilidad son
responsabilidades separadas.

---

# Independencia de Integraciones Municipales

El Repository no conoce:

- APIs municipales;
- endpoints externos;
- formatos de interoperabilidad;
- sistemas de gestión municipal;
- credenciales municipales;
- protocolos externos.

Estas responsabilidades no forman parte del contrato de
persistencia.

---

# Fallos del Repository

El contrato debe distinguir conceptualmente fallos como:

```text
ProposalNotFound

ProposalIdentityConflict

ProposalConcurrencyConflict

ProposalPersistenceFailure
```

Estos fallos representan condiciones relevantes para la
persistencia.

No deben confundirse con errores del dominio como:

```text
InvalidProposalTransition

ProposalInvariantViolation

UnauthorizedProposalOperation
```

Cada responsabilidad permanece separada.

---

# ProposalNotFound

Representa la ausencia de una Proposal solicitada mediante:

```text
ProposalId
```

No modifica estado.

No produce Domain Events.

No crea una Proposal implícitamente.

---

# ProposalIdentityConflict

Representa un intento de persistir una nueva Proposal utilizando
una identidad ya existente.

Debe mantenerse:

```text
Existing Proposal

+

Duplicate ProposalId

↓

Persistence Rejected
```

---

# ProposalConcurrencyConflict

Representa una incompatibilidad entre:

```text
ExpectedVersion
```

y:

```text
PersistedVersion
```

Debe producir rechazo de la escritura.

No debe resolverse mediante sobrescritura silenciosa.

---

# ProposalPersistenceFailure

Representa la imposibilidad de completar la persistencia del
Aggregate por una condición perteneciente al mecanismo de
almacenamiento.

Conceptualmente:

```text
Persistence Attempt

↓

Failure

↓

No Successful Commit
```

El Aggregate persistido debe permanecer en su último estado
confirmado.

---

# Reintentos

Un fallo técnico de persistencia puede permitir reintentos desde
la capa responsable.

Sin embargo, un reintento no debe:

- ignorar ExpectedVersion;
- convertir un conflicto de concurrencia en una escritura
  forzada;
- ejecutar nuevamente comportamiento de dominio de forma
  indiscriminada;
- duplicar efectos;
- producir eventos duplicados como hechos independientes.

La estrategia técnica de reintentos pertenece a Infrastructure o
Application.

---

# Idempotencia de Persistencia

La persistencia debe evitar que un reintento técnico convierta una
misma modificación lógica en múltiples modificaciones del
Aggregate.

Conceptualmente:

```text
Same Logical Save

↓

Must Not Create Multiple Domain Changes
```

El Repository no debe interpretar un reintento de persistencia
como un nuevo Command de dominio.

---

# Eliminación

ProposalRepository no expone conceptualmente:

```text
delete()
```

como mecanismo ordinario del ciclo de vida.

Proposal utiliza:

```text
Archived
```

como estado terminal definido por el dominio.

Por lo tanto:

```text
ArchiveProposal

↓

ProposalArchived

↓

ProposalStatus = Archived
```

representa el mecanismo de retiro lógico establecido.

---

# Regla de No Eliminación Física como Comportamiento de Dominio

La eliminación física de persistencia no forma parte del
Lifecycle ordinario de Proposal.

No debe confundirse:

```text
Archive
```

con:

```text
Physical Delete
```

El archivado constituye una transición del dominio.

La eliminación física, cuando existan necesidades técnicas,
legales o de operación, pertenece a políticas externas y no debe
ser utilizada para representar una transición del Aggregate.

---

# Proposal Archivada

Una Proposal archivada puede continuar siendo recuperada cuando
la arquitectura requiera:

- trazabilidad;
- auditoría;
- reconstrucción;
- consulta histórica;
- interoperabilidad histórica.

El Repository debe preservar:

```text
ProposalStatus = Archived
```

sin interpretar ese estado como inexistencia.

Debe mantenerse:

```text
Archived Proposal

≠

ProposalNotFound
```

---

# Timestamps

El Repository persiste los timestamps que formen parte del estado
oficial de Proposal.

Puede incluir:

```text
CreatedAt

UpdatedAt

SubmittedAt

ReviewStartedAt

DecidedAt

WithdrawnAt

ArchivedAt
```

cuando correspondan al Lifecycle y estado del Aggregate.

El Repository no debe inventar hechos temporales del dominio que
no hayan sido producidos por Proposal.

---

# UpdatedAt

Cuando:

```text
UpdatedAt
```

forme parte del estado del Aggregate, su valor debe provenir del
comportamiento válido del dominio o del mecanismo temporal
establecido por la arquitectura.

El Repository no debe utilizar un timestamp técnico para alterar
silenciosamente el significado temporal del dominio.

---

# Mapeo de Persistencia

La implementación concreta debe realizar el mapeo entre:

```text
Domain Model
```

y:

```text
Persistence Model
```

Conceptualmente:

```text
Proposal

↓

Mapper

↓

Persistence Representation
```

y:

```text
Persistence Representation

↓

Mapper

↓

Proposal
```

El mapeo no modifica las reglas del dominio.

---

# Regla de Mapeo

El mapeo debe preservar semánticamente:

- identidad;
- referencias;
- Value Objects;
- estado;
- timestamps;
- Version;
- información necesaria para reconstruir Proposal.

La representación física puede ser diferente.

La semántica del Aggregate no puede cambiar.

---

# Serialización

Cuando la infraestructura requiera serialización, esta pertenece
a la implementación del Repository o a componentes de
Infrastructure.

Proposal no debe conocer:

```text
JSON

BSON

SQL Rows

ORM Records

Protocol Buffers
```

La serialización no forma parte del lenguaje interno del
Aggregate.

---

# Event Sourcing

La arquitectura de Proposal es compatible con Event Sourcing.

Cuando una implementación utilice Event Sourcing, el Repository
puede reconstruir Proposal mediante:

```text
Domain Events

↓

Replay

↓

Proposal
```

y persistir nuevos eventos correspondientes a modificaciones
válidas.

Esta posibilidad no modifica el contrato conceptual fundamental:

```text
Repository

↓

Load Aggregate

Save Aggregate
```

---

# Reconstrucción mediante Eventos

Cuando se utilice Event Sourcing:

```text
getById(ProposalId)
```

puede conceptualmente:

```text
Load Event Stream

↓

Replay Events

↓

Rehydrate Proposal
```

La reconstrucción no debe volver a publicar los eventos
históricos como nuevos hechos.

Debe mantenerse:

```text
Historical Event Replay

≠

New Domain Event Publication
```

---

# Version en Event Sourcing

Cuando se utilice Event Sourcing, Version puede corresponder a la
posición lógica del Aggregate dentro de su stream.

La implementación debe continuar respetando:

```text
ExpectedVersion
```

para detectar concurrencia.

El mecanismo físico puede variar.

La semántica conceptual permanece igual.

---

# Snapshot

Una implementación basada en Event Sourcing puede utilizar
snapshots como optimización técnica.

Un snapshot:

- no reemplaza los Domain Events;
- no redefine la identidad;
- no cambia Version semánticamente;
- no introduce reglas de negocio;
- no constituye una nueva fuente conceptual del dominio.

El uso o ausencia de snapshots pertenece a Infrastructure.

---

# Seguridad del Repository

ProposalRepository no autentica actores.

ProposalRepository no administra permisos.

ProposalRepository no almacena dentro del Aggregate:

- contraseñas;
- tokens;
- JWT;
- secretos;
- claves privadas;
- credenciales de infraestructura.

Las credenciales necesarias para acceder a la persistencia
pertenecen a Infrastructure.

---

# Auditoría

El Repository puede proporcionar información técnica necesaria
para trazabilidad de persistencia.

Sin embargo, el Repository no sustituye:

```text
Audit
```

como responsabilidad independiente del dominio.

Los hechos relevantes de Proposal permanecen representados
mediante sus Domain Events.

---

# Observabilidad

La implementación del Repository puede registrar información
operacional como:

- duración de consultas;
- duración de persistencia;
- conflictos de concurrencia;
- errores de almacenamiento;
- disponibilidad del mecanismo de persistencia.

Esta observabilidad pertenece a Infrastructure.

No debe modificar el comportamiento conceptual de Proposal.

---

# Performance

El Repository debe permitir recuperar y persistir Proposal de
forma compatible con los requisitos operacionales del sistema.

Las optimizaciones técnicas pueden incluir:

- índices;
- caché;
- particionamiento;
- réplicas;
- batching técnico;
- snapshots;
- conexiones persistentes.

Estas decisiones pertenecen a Infrastructure.

No deben alterar:

```text
ProposalId

ProposalStatus

Version

Invariants

Consistency Boundary
```

---

# Caché

Una implementación puede utilizar caché.

Sin embargo, la caché no puede:

- sustituir la fuente persistida sin garantías de consistencia;
- ignorar Version;
- devolver una versión incompatible para modificación;
- permitir sobrescrituras concurrentes;
- alterar el Aggregate.

La utilización de caché debe preservar el contrato del
Repository.

---

# Repository y Consistencia

El Repository debe respetar el límite definido en:

```text
DOMAIN-007J-Consistency-Boundary.md
```

Debe persistir exclusivamente el estado perteneciente a Proposal.

No debe expandir el límite transaccional para incluir otros
Aggregates.

---

# Restricciones

No está permitido:

- persistir partes de Proposal como sustituto de la persistencia
  del Aggregate;
- exponer setters de persistencia para atributos internos;
- modificar ProposalStatus directamente desde el Repository;
- modificar ProposalContent directamente desde el Repository;
- modificar ProposalId;
- modificar OrganizationId;
- modificar Version arbitrariamente;
- ignorar ExpectedVersion;
- utilizar Last Write Wins para ocultar conflictos;
- sobrescribir modificaciones concurrentes;
- reconstruir Proposal ejecutando CreateProposal;
- producir ProposalCreated durante una reconstrucción;
- inventar Domain Events desde diferencias de base de datos;
- ejecutar Commands dentro del Repository;
- validar permisos dentro del Repository;
- implementar la State Machine dentro del Repository;
- implementar el Lifecycle dentro del Repository;
- cargar otros Aggregates como partes internas de Proposal;
- modificar otros Aggregates;
- utilizar Read Models para modificar Proposal;
- exponer entidades ORM al dominio;
- exponer sesiones de base de datos al dominio;
- acoplar el contrato a SQL;
- acoplar el contrato a MongoDB;
- acoplar el contrato a HTTP;
- acoplar el contrato a FIWARE;
- acoplar el contrato a proveedores externos;
- interpretar Archived como inexistencia;
- utilizar eliminación física para representar Archive;
- publicar externamente eventos de una modificación cuya
  persistencia no haya sido confirmada.

---

# Escenario — Recuperación Exitosa

```text
Given

ProposalId = proposal-001

And

la Proposal existe

When

getById(proposal-001) es ejecutado

Then

ProposalRepository reconstruye Proposal

And

ProposalId permanece proposal-001

And

ProposalStatus corresponde al estado persistido

And

Version corresponde a la versión persistida

And

ningún Domain Event de modificación es producido
```

---

# Escenario — Proposal No Encontrada

```text
Given

ProposalId = proposal-999

And

la Proposal no existe

When

getById(proposal-999) es ejecutado

Then

ProposalNotFound es expresado

And

ninguna Proposal artificial es creada

And

ningún Domain Event es producido
```

---

# Escenario — Persistencia Exitosa

```text
Given

Proposal fue recuperada con Version = 7

And

un Command válido modifica Proposal

And

Proposal.Version = 8

When

save(
    Proposal,
    ExpectedVersion = 7
) es ejecutado

And

PersistedVersion = 7

Then

la persistencia es aceptada

And

el estado completo de Proposal es persistido

And

PersistedVersion = 8
```

---

# Escenario — Conflicto de Concurrencia

```text
Given

Proposal fue recuperada con Version = 7

And

otra modificación ya persistió Version = 8

When

save(
    Proposal,
    ExpectedVersion = 7
) es ejecutado

Then

ProposalConcurrencyConflict es expresado

And

la escritura es rechazada

And

Version 8 permanece persistida

And

el estado más reciente no es sobrescrito
```

---

# Escenario — Proposal Archivada

```text
Given

ProposalStatus = Archived

And

Version = 15

When

getById(ProposalId) es ejecutado

Then

Proposal es recuperada

And

ProposalStatus permanece Archived

And

Version permanece 15

And

Archived no es interpretado como ProposalNotFound
```

---

# Escenario — Reconstrucción sin Evento de Creación

```text
Given

Proposal existe en persistencia

When

ProposalRepository reconstruye el Aggregate

Then

Proposal es rehidratada

And

ProposalCreated no es producido

And

Version no incrementa

And

el Lifecycle no reinicia
```

---

# Escenario — Referencia a Assembly

```text
Given

Proposal contiene:

AssemblyId = assembly-001

When

ProposalRepository recupera Proposal

Then

AssemblyId es reconstruido como referencia

And

Assembly Aggregate no es cargado como parte de Proposal

And

Assembly no pasa a formar parte del límite de consistencia
```

---

# Escenario — Referencia a Territory

```text
Given

Proposal contiene:

TerritoryId = territory-001

When

ProposalRepository recupera Proposal

Then

TerritoryId es reconstruido

And

Territory Aggregate no es cargado como entidad interna

And

Proposal mantiene su límite de consistencia
```

---

# Escenario — Fallo de Persistencia

```text
Given

Proposal contiene una modificación válida

And

save() intenta persistirla

When

el mecanismo de persistencia falla antes del commit

Then

ProposalPersistenceFailure es expresado

And

la modificación no se considera persistida

And

los eventos asociados no se consideran confirmados para
publicación externa
```

---

# Escenario — Identidad Duplicada

```text
Given

ProposalId = proposal-001 ya existe

When

una nueva Proposal intenta persistirse con:

ProposalId = proposal-001

Then

ProposalIdentityConflict es expresado

And

la Proposal existente no es sobrescrita

And

la nueva Proposal no reemplaza el Aggregate existente
```

---

# Escenario — Consulta de Existencia

```text
Given

ProposalId = proposal-001

When

exists(proposal-001) es ejecutado

Then

el Repository retorna true o false según corresponda

And

Proposal no es modificada

And

Version no cambia

And

ningún Domain Event es producido
```

---

# Escenario — Read Model No Utilizado para Escritura

```text
Given

ProposalSummary representa una proyección de lectura

When

una operación intenta modificar Proposal

Then

ProposalSummary no es utilizado como Aggregate

And

ProposalRepository recupera Proposal

And

el comportamiento se ejecuta sobre Proposal Aggregate

And

el estado válido resultante puede ser persistido mediante save()
```

---

# Compatibilidad Arquitectónica

ProposalRepository es compatible con:

- Domain-Driven Design;
- Repository Pattern;
- Clean Architecture;
- Hexagonal Architecture;
- Dependency Inversion Principle;
- CQRS;
- Event-Driven Architecture;
- Event Sourcing;
- Unit of Work;
- Optimistic Concurrency Control;
- arquitectura distribuida.

La compatibilidad con estos patrones no obliga a una
implementación tecnológica específica.

---

# Principios Arquitectónicos

ProposalRepository mantiene:

```text
Repository

=

Persistence Abstraction
```

```text
Repository

≠

Domain Service
```

```text
Repository

≠

Application Service
```

```text
Repository

≠

Authorization Service
```

```text
Repository

≠

Read Model
```

```text
Repository

≠

Integration Adapter
```

```text
Repository

≠

Database Model
```

```text
Aggregate Root

=

Persistence Unit
```

```text
ProposalId

=

Domain Identity
```

```text
ExpectedVersion
    =
PersistedVersion

↓

Save Allowed
```

```text
ExpectedVersion
    ≠
PersistedVersion

↓

Concurrency Conflict
```

```text
Archived

≠

Deleted
```

```text
Infrastructure

↓

implements

↓

Domain Repository Contract
```

Estos principios protegen la independencia del dominio y el
límite de consistencia del Aggregate Proposal.

---

# Documentación Complementaria

El contrato del Repository debe interpretarse conjuntamente con:

```text
DOMAIN-007-Aggregate.md

DOMAIN-007A-Lifecycle.md

DOMAIN-007B-State-Machine.md

DOMAIN-007C-Commands.md

DOMAIN-007D-Domain-Events.md

DOMAIN-007E-Invariants.md

DOMAIN-007F-Permissions.md

DOMAIN-007I-Versioning.md

DOMAIN-007J-Consistency-Boundary.md

DOMAIN-007K-Integration-Events.md

DOMAIN-007L-Read-Model.md

DOMAIN-007M-Test-Scenarios.md

DOMAIN-007N-Performance-Rules.md

DOMAIN-007O-Security-Model.md

DOMAIN-007P-Extension-Points.md
```

Estos documentos desarrollan responsabilidades complementarias
sin modificar el contrato conceptual establecido en este
archivo.

---

# Definición de Éxito

El Repository Contract del Aggregate **Proposal** constituye la
abstracción oficial mediante la cual AURA recupera y persiste una
Proposal sin acoplar el dominio a mecanismos tecnológicos de
almacenamiento.

El contrato garantiza que:

```text
Application Service

↓

ProposalRepository.getById()

↓

Proposal Aggregate

↓

Domain Behavior

↓

Invariant Validation

↓

Version Change

↓

Domain Events

↓

ProposalRepository.save()

↓

Persistence Commit
```

mantenga la separación entre dominio e infraestructura.

ProposalRepository trabaja exclusivamente con:

```text
Proposal
```

como Aggregate Root y unidad de consistencia.

El Repository preserva:

```text
ProposalId

OrganizationId

Aggregate State

Lifecycle State

Version

External References

Domain Consistency
```

sin modificar las decisiones tomadas por el Aggregate.

El contrato garantiza que:

```text
ExpectedVersion
    =
PersistedVersion
```

sea condición necesaria para aceptar una modificación
concurrente y que:

```text
ExpectedVersion
    ≠
PersistedVersion
```

produzca:

```text
ProposalConcurrencyConflict
```

sin sobrescritura silenciosa.

El Repository no administra:

- Commands;
- permisos;
- Lifecycle;
- State Machine;
- invariantes;
- otros Aggregates;
- Read Models;
- Integration Events;
- autenticación;
- infraestructura externa.

Asimismo:

```text
Archived Proposal

≠

Deleted Proposal
```

y:

```text
Repository Reconstruction

≠

Domain Creation
```

por lo que la recuperación de una Proposal existente preserva su
identidad, estado, historia lógica y Version sin reiniciar su
ciclo de vida ni producir nuevos hechos de dominio.

De esta forma,
**DOMAIN-007G-Repository-Contract.md** establece el contrato
conceptual oficial de persistencia del Aggregate Proposal,
manteniendo independencia tecnológica, consistencia
transaccional, concurrencia optimista, trazabilidad y separación
estricta entre el modelo de dominio y la infraestructura dentro
de la arquitectura DDD de AURA Core.