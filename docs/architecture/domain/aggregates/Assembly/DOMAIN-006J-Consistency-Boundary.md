# DOMAIN-006J — Assembly Consistency Boundary

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
* DOMAIN-006G-Repository-Contract.md
* DOMAIN-006H-Examples.md
* DOMAIN-006I-Versioning.md
* DOMAIN-006K-Integration-Events.md
* DOMAIN-006L-Read-Model.md
* DOMAIN-006M-Test-Scenarios.md
* CORE-003-Shared-Kernel.md
* CORE-006-Domain-Invariants.md
* CORE-008-Aggregate-Design-Rules.md
* CORE-011-Repository-Contracts.md

---

# Objetivo

Definir formalmente el **Consistency Boundary** del Aggregate
**Assembly**.

El Consistency Boundary establece qué conceptos deben permanecer
fuertemente consistentes dentro de una única Assembly y qué
conceptos deben permanecer fuera del Aggregate aun cuando
participen en el mismo proceso organizacional.

Assembly constituye una unidad de consistencia.

Toda operación que modifique su estado debe preservar
simultáneamente:

* identidad;
* estado;
* programación;
* convocatoria;
* modalidad;
* ubicación cuando corresponda;
* reglas internas;
* condiciones de realización;
* información temporal propia;
* Version;
* invariantes.

Los conceptos pertenecientes a otros Aggregates no deben
incorporarse dentro de esta misma frontera únicamente porque
participen en una reunión.

---

# Propósito

El propósito del Consistency Boundary es impedir que Assembly
crezca hasta convertirse en un Aggregate encargado de coordinar
directamente todos los procesos relacionados con una reunión.

Assembly representa:

```text
la reunión formal
```

No representa:

```text
todo lo que ocurre alrededor de la reunión
```

Esta separación permite preservar:

* alta cohesión;
* bajo acoplamiento;
* autonomía entre Aggregates;
* consistencia transaccional local;
* escalabilidad;
* evolución independiente;
* interoperabilidad mediante contratos;
* separación explícita de responsabilidades.

---

# Principio Fundamental

Debe mantenerse:

```text
Assembly
    =
Consistency Boundary de la reunión formal
```

No:

```text
Assembly
    =
Consistency Boundary de todos los procesos
relacionados con una reunión
```

La existencia de una relación funcional o temporal con Assembly no
convierte automáticamente un concepto en parte del Aggregate.

---

# Aggregate Root

La única Aggregate Root dentro del Consistency Boundary es:

```text
Assembly
```

Toda modificación del estado interno debe ocurrir exclusivamente a
través de esta raíz.

No puede existir una segunda Aggregate Root dentro del mismo
límite.

---

# Unidad de Consistencia

Assembly constituye una única unidad lógica de consistencia.

Conceptualmente:

```text
Assembly
    │
    ├── Identity
    ├── Organization Context
    ├── Territorial Context
    ├── Name
    ├── Type
    ├── Purpose
    ├── Description
    ├── Schedule
    ├── Modality
    ├── Location
    ├── Convocation
    ├── Assembly Rules
    ├── Execution Conditions
    ├── Status
    ├── Lifecycle Timestamps
    └── Version
```

Toda modificación válida debe dejar este conjunto en un estado
coherente.

---

# Conceptos Dentro del Boundary

El Consistency Boundary de Assembly comprende exclusivamente los
conceptos necesarios para representar y proteger la consistencia
formal de la reunión.

Incluye conceptualmente:

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

La presencia concreta de cada propiedad debe permanecer coherente
con el modelo definido en `DOMAIN-006-Aggregate.md`.

---

# Conceptos Fuera del Boundary

No forman parte del Consistency Boundary de Assembly:

```text
Organization

Citizen

Membership

Role

Territory

Proposal

Participation

Voting

Document

Notification

Audit

Integration
```

Estos conceptos mantienen sus propios límites de consistencia.

Assembly puede relacionarse con ellos.

No los contiene.

---

# Regla de Pertenencia

Un concepto pertenece al Consistency Boundary de Assembly cuando
su consistencia debe protegerse necesariamente dentro de la misma
modificación transaccional de la reunión.

Un concepto no pertenece al Boundary cuando:

* posee identidad propia fuera de Assembly;
* posee Lifecycle propio;
* posee invariantes propias;
* puede evolucionar independientemente;
* posee Repository propio;
* pertenece a otro Aggregate;
* pertenece a otro Bounded Context.

---

# Identidad dentro del Boundary

La identidad principal es:

```text
AssemblyId
```

AssemblyId identifica toda la unidad de consistencia.

Las partes internas de Assembly no pueden convertirse en raíces
independientes únicamente por razones de persistencia.

---

# OrganizationId dentro del Boundary

Assembly mantiene:

```text
OrganizationId
```

dentro de su estado porque toda Assembly pertenece a una
Organization determinada.

Sin embargo:

```text
OrganizationId
```

no significa que:

```text
Organization
```

forme parte del Aggregate Assembly.

Debe mantenerse:

```text
OrganizationId inside Assembly
```

pero:

```text
Organization Aggregate outside Assembly
```

---

# Organization fuera del Boundary

Organization mantiene su propia:

* identidad;
* configuración;
* políticas;
* Lifecycle;
* invariantes;
* Version;
* Repository.

Assembly no puede modificar esas propiedades directamente.

---

# Inmutabilidad de OrganizationId

OrganizationId forma parte de la consistencia estructural de
Assembly.

Una Assembly no cambia de Organization durante su Lifecycle
oficial.

Modificar OrganizationId implicaría alterar el contexto
organizacional fundamental del Aggregate.

Esa operación no pertenece al comportamiento definido actualmente
para Assembly.

---

# TerritoryId dentro del Boundary

Assembly puede mantener:

```text
TerritoryId
```

cuando la reunión requiere contexto territorial.

TerritoryId pertenece al estado de Assembly como referencia.

El Aggregate Territory permanece fuera.

Debe mantenerse:

```text
TerritoryId
    ≠
Territory Aggregate
```

---

# Territory fuera del Boundary

Assembly no administra:

* TerritoryName;
* TerritoryType;
* TerritoryStatus;
* ParentTerritoryId;
* AdministrativeCode;
* GeometryReference;
* TerritoryMetadata.

Estas responsabilidades corresponden a Territory.

---

# AssemblyLocation dentro del Boundary

AssemblyLocation puede pertenecer al Consistency Boundary cuando
forma parte de las condiciones formales de realización de la
reunión.

Location representa:

```text
lugar de realización
```

Territory representa:

```text
contexto territorial
```

Debe mantenerse:

```text
AssemblyLocation
    ≠
Territory
```

---

# AssemblySchedule dentro del Boundary

La programación pertenece al Boundary porque Assembly no puede
mantener un estado válido si su información temporal interna es
inconsistente.

Conceptualmente comprende:

```text
ScheduledStart

ScheduledEnd
```

o los nombres establecidos por el modelo oficial.

La programación debe mantenerse coherente con:

* AssemblyStatus;
* AssemblyModality;
* AssemblyLocation;
* Convocation;
* invariantes temporales.

---

# Coherencia Temporal

Dentro de una misma Assembly no debe persistirse un estado que
viole sus relaciones temporales.

Ejemplo conceptualmente inválido:

```text
ScheduledEnd
<
ScheduledStart
```

cuando ambos valores se encuentran definidos.

La programación y el estado deben permanecer consistentes dentro
de la misma unidad lógica.

---

# Convocation dentro del Boundary

La condición formal de convocatoria pertenece al Consistency
Boundary de Assembly.

Conceptualmente puede comprender:

```text
ConvocationStatus

ConvokedAt

ConvocationDeadline

ConvocationRules
```

según el modelo oficial.

Assembly debe garantizar que estos conceptos sean coherentes con
su estado.

---

# Convocation no es Notification

Debe mantenerse:

```text
Convocation
    ≠
Notification
```

Convocation representa la condición formal de la reunión.

Notification representa comunicación.

La primera pertenece a Assembly cuando forma parte de su estado.

La segunda permanece fuera.

---

# Notification fuera del Boundary

Assembly no necesita que una Notification haya sido físicamente
enviada, procesada o entregada dentro de la misma transacción que
modifica el Aggregate.

Conceptualmente:

```text
AssemblyConvoked
```

puede ser un hecho válido aun cuando:

```text
Notification
```

sea procesada posteriormente.

---

# AssemblyRules dentro del Boundary

Las reglas propias de la reunión pertenecen al Boundary cuando
determinan condiciones internas necesarias para preservar un
estado válido de Assembly.

Ejemplos conceptuales:

```text
AssemblyRules
```

pueden controlar condiciones propias de:

* convocatoria;
* modalidad;
* realización;
* inicio;
* cierre.

Estas reglas no absorben procesos externos.

---

# ExecutionConditions dentro del Boundary

Las condiciones de realización pertenecen al Boundary cuando deben
quedar establecidas y protegidas como parte del estado formal de
Assembly.

Conceptualmente:

```text
ExecutionConditions
```

pueden participar en Guards para operaciones como:

```text
StartAssembly
```

Las decisiones o datos externos utilizados para determinar dichas
condiciones pueden provenir de otros Aggregates.

Eso no convierte dichos Aggregates en partes internas de Assembly.

---

# Información Externa Validada

Assembly puede recibir información previamente resuelta por la
Application Layer o por Domain Policies.

Ejemplo conceptual:

```text
External Domain Information
        │
        ▼
Application / Domain Policy
        │
        ▼
Validated Decision
        │
        ▼
Assembly
```

Assembly utiliza la decisión necesaria para proteger su
comportamiento.

No necesita absorber el Aggregate que originó la información.

---

# Quórum como Ejemplo Conceptual

Una regla de Assembly puede requerir que determinada condición de
quórum se encuentre satisfecha.

La información necesaria para calcular dicho quórum puede depender
de conceptos como:

```text
Membership

Participation
```

Estos permanecen fuera de Assembly.

Debe mantenerse:

```text
Quorum Requirement
    may belong to AssemblyRules
```

pero:

```text
Membership Aggregate
    does not belong to Assembly
```

---

# Membership fuera del Boundary

Membership representa el vínculo formal entre Citizen y
Organization.

Assembly no modifica:

* MembershipStatus;
* AdmissionDate;
* ActivationDate;
* TerminationDate;
* MembershipVersion.

La existencia de Memberships válidas puede ser necesaria para
determinadas decisiones externas.

Eso no convierte Membership en parte de Assembly.

---

# MembershipId

Cuando Assembly necesita una referencia hacia una Membership debe
utilizar:

```text
MembershipId
```

La referencia por identidad no expande el Consistency Boundary.

---

# Citizen fuera del Boundary

Citizen representa identidad cívica.

Assembly no administra:

* FullName;
* Email;
* NationalIdentifier;
* CitizenStatus;
* CitizenProfile;
* CitizenVersion.

Citizen permanece fuera del Aggregate.

---

# CitizenId

Una relación con un ciudadano se mantiene, cuando corresponda,
mediante:

```text
CitizenId
```

No mediante una referencia mutable al Aggregate Citizen.

---

# Role fuera del Boundary

Role representa una función organizacional.

Assembly no administra:

* RoleName;
* RoleCode;
* RoleStatus;
* asignación de Roles;
* Lifecycle de Role.

Role permanece fuera del Consistency Boundary.

---

# Permissions fuera del Estado Interno

Los Permissions necesarios para intentar Commands sobre Assembly
no forman parte del estado interno del Aggregate.

Debe mantenerse:

```text
Authorization
    outside Assembly Consistency Boundary
```

y:

```text
Domain Validation
    inside Assembly behavior
```

---

# Permission versus Boundary

Assembly puede requerir una capacidad como:

```text
Assembly.Start
```

pero no mantiene:

```text
AllowedRoles

AllowedUsers

PermissionAssignments
```

como parte de su estado interno.

---

# Proposal fuera del Boundary

Proposal posee su propia:

* identidad;
* Lifecycle;
* State Machine;
* invariantes;
* Version;
* Repository;
* Domain Events.

Aunque una Proposal pueda originarse o discutirse dentro de una
Assembly, permanece como Aggregate independiente.

---

# ProposalId

Assembly puede relacionarse mediante:

```text
ProposalId
```

cuando corresponda.

La existencia de la referencia no significa que Proposal deba
persistirse conjuntamente con Assembly.

---

# Participation fuera del Boundary

Participation representa procesos de participación ciudadana.

Puede utilizar AssemblyId como contexto.

Assembly no administra directamente:

* estado de Participation;
* reglas de Participation;
* Version de Participation;
* Lifecycle de Participation.

---

# Voting fuera del Boundary

Voting posee un modelo independiente.

Assembly puede proporcionar contexto para una votación.

No administra:

* VotingStatus;
* apertura de Voting;
* cierre de Voting;
* votos;
* resultados;
* reglas internas de Voting.

---

# VotingId

La relación se mantiene conceptualmente mediante:

```text
VotingId
```

sin incorporar Voting dentro del Aggregate.

---

# Document fuera del Boundary

Document posee su propia identidad y Lifecycle.

Assembly puede relacionarse con documentos como:

* convocatoria;
* actas;
* antecedentes;
* documentos de apoyo.

Pero no almacena el Aggregate Document dentro de su frontera.

---

# DocumentId

Assembly puede mantener una referencia:

```text
DocumentId
```

cuando el modelo correspondiente lo requiera.

Document continúa siendo persistido y modificado de forma
independiente.

---

# Audit fuera del Boundary

Audit no forma parte del estado interno de Assembly.

Assembly puede producir Domain Events utilizados posteriormente
para auditoría.

Debe mantenerse:

```text
Assembly
    │
    ▼
Domain Event
    │
    ▼
Audit Process
```

No:

```text
Assembly
    └── Audit Aggregate
```

---

# Integration fuera del Boundary

Las integraciones externas no forman parte del Consistency
Boundary.

Assembly no contiene:

* endpoints;
* webhooks;
* contratos HTTP;
* credenciales;
* FIWARE entities;
* NGSI-LD payloads;
* municipal API clients.

Estas responsabilidades pertenecen a Integration e
Infrastructure.

---

# Domain Events en el Boundary

Los Domain Events son producidos por cambios válidos del
Aggregate.

Representan hechos ocurridos dentro de Assembly.

Ejemplos:

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

El hecho se origina dentro del Aggregate.

Su consumo ocurre fuera.

---

# Domain Event no Amplía el Boundary

Que otro Aggregate reaccione a:

```text
AssemblyCompleted
```

no convierte ese Aggregate en parte de Assembly.

Conceptualmente:

```text
Assembly
    │
    ▼
AssemblyCompleted
    │
    ├────────► Document
    ├────────► Notification
    ├────────► Audit
    └────────► Integration
```

Cada consumidor mantiene su propia frontera.

---

# Integration Events fuera del Boundary

Los Integration Events definidos en:

```text
DOMAIN-006K-Integration-Events.md
```

son contratos utilizados para comunicar hechos hacia otros
Bounded Contexts o sistemas.

No forman parte del estado interno de Assembly.

---

# Consistencia Interna

Dentro de Assembly se requiere consistencia inmediata.

Después de una operación válida:

```text
Assembly
```

debe encontrarse completamente consistente.

No existe un período aceptable durante el cual sus invariantes
internas puedan permanecer rotas esperando que otro proceso las
corrija.

---

# Consistencia Externa

Entre Assembly y otros Aggregates se utiliza consistencia eventual
cuando la coordinación depende de eventos.

Debe mantenerse:

```text
Strong Consistency
    inside Assembly
```

y:

```text
Eventual Consistency
    between Aggregates
```

---

# Ejemplo de Consistencia Interna

Después de un inicio válido:

```text
AssemblyStatus:
InProgress
```

debe mantenerse coherencia con:

```text
StartedAt
```

y demás condiciones internas definidas por las invariantes.

No debe quedar Assembly parcialmente iniciada.

---

# Ejemplo de Consistencia Externa

Después de:

```text
AssemblyStatus:
Convoked
```

puede ocurrir temporalmente:

```text
Notification:
not yet processed
```

sin invalidar el Aggregate Assembly.

Notification pertenece a otra frontera de consistencia.

---

# Otro Ejemplo de Consistencia Externa

Después de:

```text
AssemblyStatus:
Completed
```

puede ocurrir:

```text
Document:
acta not yet created
```

sin que Assembly deje de estar Completed.

La creación documental puede producirse posteriormente mediante
coordinación externa.

---

# No Transacciones Distribuidas entre Aggregates

Assembly no debe exigir una única transacción que modifique
simultáneamente:

```text
Assembly

Proposal

Participation

Voting

Document

Notification

Audit
```

La necesidad de sincronización entre ellos debe resolverse fuera
del Aggregate.

---

# Regla de Una Transacción por Aggregate

Una modificación de Assembly debe afectar exclusivamente una
Assembly como unidad transaccional de dominio.

Conceptualmente:

```text
Command
    │
    ▼
Assembly
    │
    ▼
Single Aggregate Transaction
```

No:

```text
Command
    │
    ├── modify Assembly
    ├── modify Voting
    ├── modify Document
    └── modify Notification
```

dentro de la misma modificación del Aggregate.

---

# Atomicidad

Toda modificación interna de Assembly debe ser atómica.

Conceptualmente:

```text
all internal changes succeed
```

o:

```text
no internal change succeeds
```

No se permiten estados parcialmente confirmados.

---

# Atomicidad de ScheduleAssembly

Una programación válida puede modificar conjuntamente:

```text
Schedule

Modality

Location

Status

Version
```

según el comportamiento definido.

Estos cambios deben representar una única modificación consistente.

---

# Atomicidad de ConvokeAssembly

Una convocatoria válida puede modificar conjuntamente:

```text
Convocation

ConvokedAt

Status

Version
```

cuando dichos conceptos formen parte de la operación.

No debe confirmarse una parte sin la otra si ello produce un estado
inválido.

---

# Atomicidad de StartAssembly

Una operación válida:

```text
StartAssembly
```

debe dejar coherentemente establecidos los elementos internos
correspondientes al inicio.

No debe persistirse una Assembly que se encuentre conceptualmente
en InProgress sin satisfacer las invariantes de dicho estado.

---

# Atomicidad de CompleteAssembly

Una operación válida:

```text
CompleteAssembly
```

debe dejar Assembly en un estado completamente consistente con
Completed.

No debe existir una finalización parcial.

---

# Atomicidad de CancelAssembly

CancelAssembly debe dejar conjuntamente coherentes:

```text
AssemblyStatus

Cancellation information

Version
```

según las reglas definidas.

---

# Atomicidad de ArchiveAssembly

ArchiveAssembly debe dejar coherentes:

```text
AssemblyStatus

ArchivedAt

Version
```

cuando estos conceptos correspondan al modelo oficial.

---

# Version dentro del Boundary

Version forma parte de la consistencia interna de Assembly.

Una modificación válida debe mantener coherencia entre:

```text
Aggregate State
```

y:

```text
Version
```

Debe evitarse:

```text
new state
+
old Version
```

o:

```text
old state
+
new Version
```

como resultado confirmado.

---

# Optimistic Concurrency

El control de concurrencia definido en:

```text
DOMAIN-006I-Versioning.md
```

protege precisamente el Consistency Boundary de Assembly.

Debe mantenerse:

```text
ExpectedVersion
=
PersistedVersion
```

antes de confirmar una nueva modificación.

---

# Concurrencia sobre Partes Internas

No debe existir concurrencia independiente sobre:

```text
AssemblySchedule

Convocation

AssemblyRules

ExecutionConditions
```

si estos conceptos pertenecen al mismo Aggregate.

Todos se protegen mediante:

```text
Assembly.Version
```

---

# Persistencia

El Repository definido en:

```text
DOMAIN-006G-Repository-Contract.md
```

debe persistir Assembly respetando su Consistency Boundary.

Aunque Infrastructure utilice múltiples estructuras físicas, desde
el dominio debe mantenerse una única unidad lógica.

---

# Estructura Física no Redefine el Boundary

Puede existir:

```text
assemblies

assembly_schedule

assembly_convocation

assembly_rules
```

como estructuras físicas distintas.

Esto no crea cuatro Aggregates.

Debe mantenerse:

```text
Persistence Structure
    ≠
Aggregate Boundary
```

---

# Documento Persistente no Redefine el Boundary

Del mismo modo, una implementación documental puede guardar varios
datos juntos.

Esto no permite incorporar otros Aggregates por conveniencia.

Ejemplo incorrecto conceptualmente:

```text
Assembly Document
    ├── Assembly
    ├── Organization
    ├── Voting
    └── Documents
```

si esos conceptos continúan siendo Aggregates independientes.

---

# Repository por Aggregate

AssemblyRepository administra:

```text
Assembly
```

No administra:

```text
Organization

Membership

Proposal

Voting

Document
```

como parte de su contrato.

---

# Repository no Amplía la Consistencia

El Repository no puede utilizar una operación técnica conjunta para
convertir múltiples Aggregates en una unidad de consistencia.

Las decisiones de infraestructura deben respetar el modelo.

No definirlo.

---

# Application Layer

La Application Layer puede coordinar operaciones entre múltiples
Aggregates.

Conceptualmente:

```text
Application Service
    │
    ├── Assembly
    ├── Proposal
    └── Notification
```

puede existir como coordinación.

Esto no significa que exista un único Aggregate.

---

# Coordinación Externa

Cuando una operación de aplicación involucre múltiples Aggregates,
debe mantenerse la autonomía de cada uno.

Ejemplo:

```text
AssemblyCompleted
      │
      ▼
Application Process
      │
      ├── request Document process
      ├── request Notification process
      └── request Audit process
```

Cada proceso mantiene su consistencia propia.

---

# Process Manager

Cuando una coordinación requiera múltiples pasos y estados
intermedios puede utilizarse un mecanismo externo apropiado.

El mecanismo de coordinación no debe convertirse en una entidad
interna de Assembly únicamente por coordinar su Lifecycle con
otros procesos.

---

# Regla de No Absorción

Assembly no absorbe un concepto únicamente porque:

* ocurra durante una reunión;
* dependa temporalmente de una reunión;
* necesite AssemblyId;
* sea mostrado en la misma interfaz;
* se persista en la misma base de datos;
* sea necesario para un reporte;
* participe en el mismo caso de uso.

Estas condiciones no determinan pertenencia al Aggregate.

---

# Ejemplo de No Absorción — Proposal

Una Proposal puede presentarse dentro de una Assembly.

Debe mantenerse:

```text
Assembly
    │
    ▼
ProposalId
```

No:

```text
Assembly
    └── Proposal Aggregate
```

como entidad interna.

---

# Ejemplo de No Absorción — Voting

Una Voting puede realizarse durante una Assembly.

Debe mantenerse:

```text
Assembly
    │
    ▼
VotingId
```

No:

```text
Assembly
    └── Voting
        └── Votes
```

como parte de la consistencia interna de la reunión.

---

# Ejemplo de No Absorción — Document

Un acta puede pertenecer conceptualmente a la documentación de una
Assembly.

Debe mantenerse:

```text
Assembly
    │
    ▼
DocumentId
```

No:

```text
Assembly
    └── Document Content
```

como parte obligatoria del Aggregate.

---

# Ejemplo de No Absorción — Notification

Convocar una Assembly puede requerir notificar ciudadanos.

Debe mantenerse:

```text
AssemblyConvoked
      │
      ▼
Notification Process
```

No:

```text
assembly.send_notifications()
```

como responsabilidad interna del Aggregate.

---

# Ejemplo de No Absorción — Audit

Un cambio de Assembly puede requerir trazabilidad.

Debe mantenerse:

```text
Assembly Domain Event
      │
      ▼
Audit Process
```

No:

```text
Assembly
    └── AuditEntries[]
```

como agregado interno de auditoría externa.

---

# Regla de Referencias por Identidad

Las relaciones hacia otros Aggregates deben mantenerse mediante
identificadores.

Ejemplos:

```text
OrganizationId

TerritoryId

MembershipId

CitizenId

RoleId

ProposalId

ParticipationId

VotingId

DocumentId

NotificationId

AuditId
```

cuando correspondan al modelo.

---

# Referencias no Implican Propiedad

Debe mantenerse:

```text
Reference by AggregateId
    ≠
Aggregate Ownership
```

Una referencia permite identificar un concepto externo.

No otorga a Assembly autoridad sobre su estado.

---

# Referencias no Implican Consistencia Fuerte

El hecho de que Assembly mantenga:

```text
ProposalId
```

no exige que Proposal y Assembly se modifiquen dentro de una misma
transacción.

La relación puede mantenerse mediante consistencia eventual.

---

# Lecturas de Otros Aggregates

Assembly no debe cargar automáticamente el estado mutable de otros
Aggregates para convertirlos en dependencias internas.

Cuando una operación necesite información externa, la coordinación
debe realizarse fuera del Aggregate.

---

# Datos Externos versus Estado Interno

Debe distinguirse:

```text
external information required to make a decision
```

de:

```text
internal Aggregate state
```

No toda información necesaria para un caso de uso pertenece a
Assembly.

---

# Domain Policy

Cuando una regla necesite combinar información perteneciente a
diferentes Aggregates, puede existir una política de dominio o
coordinación externa.

Assembly recibe el resultado necesario para proteger sus propias
invariantes.

---

# Ejemplo de Política Externa

Conceptualmente:

```text
Membership
      │
      ┐
      │
Participation
      │
      ┘
      ▼
Participation Eligibility Policy
      │
      ▼
Eligibility Decision
      │
      ▼
Assembly-related Command
```

La decisión puede utilizarse en una operación.

Membership y Participation continúan fuera.

---

# Commands

Los Commands definidos en:

```text
DOMAIN-006C-Commands.md
```

modifican exclusivamente una Assembly.

Un Command de Assembly no debe modificar directamente otro
Aggregate.

---

# Regla de Un Command — Un Aggregate

Para el Write Model debe mantenerse:

```text
Assembly Command
    │
    ▼
Assembly
```

La coordinación posterior con otros Aggregates se realiza mediante
eventos o Application Services.

---

# Domain Events

Los Domain Events definidos en:

```text
DOMAIN-006D-Domain-Events.md
```

constituyen el principal mecanismo para comunicar cambios ocurridos
dentro del Boundary.

Conceptualmente:

```text
Assembly State Change
      │
      ▼
Domain Event
      │
      ▼
External Reaction
```

---

# Domain Event como Salida del Boundary

Un Domain Event permite que otros procesos conozcan un hecho sin
necesidad de acceder directamente al estado interno de Assembly.

Ejemplo:

```text
AssemblyCompleted
```

expresa que el Aggregate alcanzó válidamente Completed.

Los consumidores deciden cómo reaccionar.

---

# Integration Events

Los Integration Events permiten propagar hechos más allá del
Bounded Context cuando corresponde.

La transformación:

```text
Domain Event
      │
      ▼
Integration Event
```

ocurre fuera de la Aggregate Root.

---

# Read Model fuera del Boundary

Los Read Models definidos en:

```text
DOMAIN-006L-Read-Model.md
```

no forman parte del Consistency Boundary del Write Model.

Pueden combinar información de múltiples fuentes para facilitar
consultas.

---

# Read Model Compuesto

Un Read Model puede presentar:

```text
AssemblyName

AssemblyStatus

ProposalCount

VotingStatus

DocumentCount
```

en una misma vista.

Esto no implica que:

```text
Proposal

Voting

Document
```

formen parte de Assembly.

---

# CQRS

Debe mantenerse:

```text
Write Model
    │
    ▼
Assembly Consistency Boundary
```

y:

```text
Read Model
    │
    ▼
Projection optimized for queries
```

Una proyección puede desnormalizar información.

El Aggregate no debe hacerlo por conveniencia de lectura.

---

# Consistencia Eventual del Read Side

Después de una modificación válida de Assembly puede existir un
breve período en el cual el Read Model aún represente el estado
anterior.

Ejemplo:

```text
Write Model:
Convoked
```

mientras:

```text
Read Model:
Scheduled
```

hasta procesar el evento correspondiente.

Esto no viola el Consistency Boundary de Assembly.

---

# Write Model como Autoridad

Los Commands deben evaluarse contra Assembly.

No contra un Read Model eventualmente consistente.

La proyección puede ayudar a interfaces y consultas.

No reemplaza la autoridad del Aggregate.

---

# Boundary y Seguridad

Authentication y Authorization se encuentran fuera del estado
interno del Aggregate.

Assembly no almacena:

* contraseñas;
* tokens;
* JWT;
* sesiones;
* OAuth credentials;
* Permissions;
* Role assignments.

---

# Autorización y Boundary

La autorización determina si un Actor puede intentar un Command.

Después de la autorización, Assembly protege:

* estado;
* Guards;
* invariantes;
* Lifecycle;
* consistencia.

Debe mantenerse:

```text
Authorization
    outside Aggregate state
```

y:

```text
Domain rules
    enforced by Aggregate
```

---

# Boundary y Authentication

La identidad autenticada de un Actor puede llegar a Application
como:

```text
ActorId
```

Assembly no valida la credencial que produjo esa identidad.

---

# Boundary y Infrastructure

Assembly no depende de:

```text
HTTP

REST

GraphQL

Database

ORM

Kafka

RabbitMQ

FIWARE

NGSI-LD

OAuth

JWT
```

Estas tecnologías permanecen fuera del Consistency Boundary.

---

# Base de Datos

La base de datos utilizada no define el límite del Aggregate.

Debe mantenerse:

```text
Database Transaction Capability
    ≠
DDD Consistency Boundary
```

El hecho de que una base de datos permita transacciones amplias no
significa que deban utilizarse para unir múltiples Aggregates.

---

# Microservicios

La eventual distribución de Bounded Contexts o servicios tampoco
redefine automáticamente los límites.

El Consistency Boundary pertenece al modelo del dominio.

No a la topología de despliegue.

---

# Boundary y FIWARE

FIWARE puede consumir o recibir representaciones derivadas de
Assembly.

No forma parte de su Boundary.

Conceptualmente:

```text
Assembly
    │
    ▼
Domain Event
    │
    ▼
Integration Layer
    │
    ▼
FIWARE
```

---

# Boundary y Municipalidad

Una plataforma municipal puede consumir Integration Events o
interactuar mediante contratos de aplicación.

No accede directamente al estado interno de Assembly.

---

# Boundary y Smart City

Sistemas Smart City pueden utilizar información derivada de
Assembly.

La interoperabilidad no convierte dichos sistemas en componentes
del Aggregate.

---

# Estados

Los estados definidos para Assembly son:

```text
Draft

Scheduled

Convoked

InProgress

Completed

Cancelled

Archived
```

La coherencia entre AssemblyStatus y el resto del estado interno
debe garantizarse dentro del Boundary.

---

# Draft

Una Assembly Draft debe mantener únicamente combinaciones de
estado permitidas por las invariantes aplicables.

Otros Aggregates no necesitan formar parte de su transacción de
creación.

---

# Scheduled

Al alcanzar Scheduled, Assembly debe mantener internamente la
información necesaria para que su programación sea válida.

La actualización de calendarios externos ocurre posteriormente.

---

# Convoked

Al alcanzar Convoked, el estado formal de convocatoria debe ser
coherente dentro de Assembly.

El envío de Notifications permanece fuera.

---

# InProgress

Al alcanzar InProgress, las condiciones internas necesarias para
representar el inicio deben encontrarse consistentes.

Procesos como Voting o Participation continúan siendo externos.

---

# Completed

Completed representa que la reunión ha finalizado conforme al
modelo de Assembly.

No significa automáticamente que:

* todos los Documents estén creados;
* todas las Notifications estén enviadas;
* todas las Votings estén cerradas;
* todos los procesos externos estén completos.

Esos conceptos pertenecen a otros Aggregates.

---

# Cancelled

Cancelled representa el estado propio de Assembly.

Las reacciones externas a la cancelación pueden ocurrir
posteriormente mediante eventos.

---

# Archived

Archived representa un estado terminal e inmutable de Assembly.

Archivar Assembly no implica eliminar otros Aggregates
relacionados.

---

# Completed no Significa Ecosistema Completado

Debe mantenerse:

```text
Assembly Completed
    ≠
All Related Processes Completed
```

Una Assembly puede estar Completed mientras otro Aggregate aún
procesa una reacción derivada.

---

# Cancelled no Significa Eliminación Externa

Debe mantenerse:

```text
Assembly Cancelled
    ≠
Delete Proposal

Delete Document

Delete Notification

Delete Audit
```

Cada Aggregate responde a sus propias reglas.

---

# Archived no Significa Cascada

Debe evitarse una semántica implícita:

```text
Archive Assembly
    │
    ├── archive Proposal
    ├── archive Voting
    ├── archive Document
    └── archive Notification
```

si dichas operaciones no están definidas explícitamente por sus
respectivos dominios.

---

# No Cascading Domain Behavior

Los cambios de estado de Assembly no producen modificaciones
directas sobre otros Aggregates por cascada ORM o mecanismo
similar.

Las reacciones deben ser explícitas.

---

# Integridad Referencial versus Consistencia de Dominio

Una base de datos puede implementar integridad referencial.

Esto no significa que múltiples Aggregates compartan un único
Consistency Boundary.

Debe mantenerse:

```text
Referential Integrity
    ≠
Aggregate Consistency Boundary
```

---

# Eliminación Física

Una operación técnica de eliminación física no forma parte del
Consistency Boundary ordinario de Assembly.

El Lifecycle oficial utiliza estados de dominio.

Archived permanece conceptualmente diferente de Deleted.

---

# Rollback

Cuando una modificación interna de Assembly falla antes de
confirmarse, debe producirse conceptualmente:

```text
Rollback
```

de toda la modificación del Aggregate.

No debe quedar una parte aceptada y otra rechazada.

---

# Fallo de Domain Rule

Ejemplo:

```text
StartAssembly
```

falla porque una condición interna no se satisface.

Resultado:

```text
Assembly unchanged
```

La Version permanece sin cambios.

Otros Aggregates tampoco deben modificarse como consecuencia de
una operación de Assembly que nunca fue confirmada.

---

# Fallo de Persistencia

Si Assembly produce un estado válido en memoria pero la
persistencia falla, la operación no debe presentarse como
confirmada.

La garantía concreta corresponde al Repository y a Infrastructure.

El Consistency Boundary exige que el estado oficial no quede
parcialmente actualizado.

---

# Domain Event y Commit

Los Domain Events representan hechos consumados del Aggregate.

La arquitectura debe preservar coherencia entre la confirmación de
la modificación y la publicación posterior de sus eventos.

La estrategia técnica no redefine el Boundary.

---

# Reintentos

Un retry técnico no amplía el Consistency Boundary.

La nueva ejecución debe continuar respetando:

* Version;
* State Machine;
* Guards;
* invariantes;
* Permissions cuando correspondan.

---

# Idempotencia

Los mecanismos de idempotencia pueden evitar procesar dos veces una
misma intención.

No forman parte del estado interno de Assembly salvo que el modelo
lo establezca expresamente.

Idempotencia y Consistency Boundary son responsabilidades
diferentes.

---

# Boundary y Event Sourcing

Si Assembly utiliza Event Sourcing, el Event Stream correspondiente
continúa representando una única Aggregate Root.

Debe mantenerse:

```text
one Assembly
    │
    ▼
one logical Aggregate history
```

La estrategia de almacenamiento de eventos no expande el Boundary.

---

# Replay

Rehidratar Assembly desde eventos históricos reconstruye el mismo
Consistency Boundary.

No incorpora Aggregates externos durante el replay.

---

# Snapshot

Un Snapshot puede representar el estado de Assembly para optimizar
rehidratación.

No constituye un Aggregate distinto.

No modifica el Boundary.

---

# Boundary y Cache

Una caché puede almacenar representaciones del Aggregate.

No redefine:

* identidad;
* Version;
* consistencia;
* relaciones;
* responsabilidades.

La caché pertenece a Infrastructure.

---

# Boundary y Performance

Las optimizaciones de rendimiento no pueden ampliar o romper el
Consistency Boundary.

No debe incorporarse otro Aggregate dentro de Assembly para evitar
una consulta adicional.

---

# Regla contra Optimización Arquitectónicamente Incorrecta

Debe evitarse:

```text
Embed external Aggregate
because it is faster
```

si ello rompe los límites definidos.

Performance debe optimizarse respetando DDD.

---

# Boundary y Reporting

Los reportes que combinan:

```text
Assembly

Proposal

Voting

Participation

Documents
```

deben utilizar Read Models o mecanismos de consulta apropiados.

No deben ampliar Assembly para facilitar reporting.

---

# Boundary y UI

La interfaz puede mostrar múltiples Aggregates en una sola vista.

La composición visual no redefine el dominio.

Debe mantenerse:

```text
UI Composition
    ≠
Aggregate Boundary
```

---

# Boundary y API

Una API puede devolver una respuesta compuesta.

Esto tampoco significa que los recursos retornados formen un único
Aggregate.

---

# Boundary y Organización de Código

La ubicación de clases dentro de una carpeta o módulo no define por
sí sola el Consistency Boundary.

El límite es conceptual.

La implementación debe reflejarlo.

No inventarlo.

---

# Boundary y Bounded Context

Assembly pertenece a:

```text
Assembly Management
```

como Bounded Context.

El Aggregate constituye una frontera táctica dentro de dicho
contexto.

Debe mantenerse:

```text
Bounded Context
    ≠
Aggregate
```

El Bounded Context puede contener más conceptos que un único
Aggregate.

---

# Boundary y Aggregate

Debe mantenerse:

```text
Aggregate Boundary
    =
Transactional consistency boundary
for Assembly
```

No debe confundirse con:

* módulo;
* microservicio;
* base de datos;
* API;
* frontend;
* proceso de negocio completo.

---

# Reglas de Consistency Boundary

Siempre deben cumplirse las siguientes reglas:

* Assembly posee una única Aggregate Root;
* Assembly constituye una única unidad de consistencia;
* toda modificación interna deja el Aggregate completamente
  consistente;
* las invariantes se preservan dentro de la misma modificación;
* Version pertenece al mismo Boundary;
* las entidades internas no se modifican directamente desde fuera;
* otros Aggregates se mantienen fuera;
* las relaciones externas se expresan mediante identificadores;
* Assembly no modifica directamente otros Aggregates;
* la coordinación entre Aggregates utiliza mecanismos externos;
* la consistencia interna es inmediata;
* la consistencia entre Aggregates puede ser eventual;
* Repository persiste Assembly como unidad;
* Read Models permanecen fuera del Write Model;
* Infrastructure no redefine el Aggregate;
* Authentication permanece fuera del estado interno;
* Authorization permanece fuera del estado interno;
* Integration permanece fuera del Aggregate.

---

# Invariantes del Boundary

El Consistency Boundary debe preservar como mínimo:

```text
One Aggregate Root

One AssemblyId

One OrganizationId

One AssemblyStatus

One Version
```

por Aggregate.

Además:

* OrganizationId no puede modificarse durante la vida oficial de
  Assembly;
* el estado interno debe respetar la State Machine;
* los datos temporales deben respetar sus invariantes;
* Archived debe permanecer inmutable;
* las referencias externas no deben transformarse en Aggregates
  internos;
* una operación no puede dejar una modificación parcial.

---

# Restricciones

No está permitido:

* incorporar Organization como entidad interna de Assembly;
* incorporar Territory como entidad interna de Assembly;
* incorporar Citizen como entidad interna de Assembly;
* incorporar Membership como entidad interna de Assembly;
* incorporar Role como entidad interna de Assembly;
* incorporar Proposal como entidad interna de Assembly;
* incorporar Participation como entidad interna de Assembly;
* incorporar Voting como entidad interna de Assembly;
* incorporar Document como entidad interna de Assembly;
* incorporar Notification como entidad interna de Assembly;
* incorporar Audit como entidad interna de Assembly;
* modificar otros Aggregates mediante AssemblyRepository;
* utilizar transacciones distribuidas como mecanismo ordinario para
  mantener múltiples Aggregates dentro de una misma frontera;
* almacenar credenciales dentro de Assembly;
* almacenar Permissions como estado interno de Assembly;
* almacenar Roles completos dentro de Assembly;
* permitir referencias mutables hacia otros Aggregates;
* permitir Lazy Loading que convierta otros Aggregates en partes
  implícitas del modelo;
* utilizar un Read Model como fuente transaccional de verdad;
* utilizar estructura de base de datos para redefinir el Boundary;
* expandir el Aggregate por conveniencia de UI;
* expandir el Aggregate por conveniencia de reporting;
* expandir el Aggregate por conveniencia de performance;
* realizar cascadas de dominio implícitas sobre otros Aggregates;
* modificar entidades internas fuera de la Aggregate Root;
* persistir parcialmente una modificación interna;
* dejar invariantes temporalmente rotas dentro de una operación
  confirmada.

---

# Casos de Uso Conceptuales

El Consistency Boundary permite que operaciones como:

```text
Crear una Assembly.

Programar una Assembly.

Reprogramar una Assembly.

Convocar una Assembly.

Modificar su nombre.

Modificar su tipo.

Modificar su propósito.

Modificar su descripción.

Modificar su modalidad.

Modificar su ubicación.

Actualizar su convocatoria.

Actualizar sus reglas.

Actualizar sus condiciones de realización.

Iniciar una Assembly.

Completar una Assembly.

Cancelar una Assembly.

Archivar una Assembly.
```

sean resueltas dentro de una única unidad de consistencia.

Estas operaciones no deben modificar directamente Aggregates
externos.

---

# Ejemplo — ScheduleAssembly

Estado inicial:

```text
AssemblyStatus:
Draft
```

La operación modifica únicamente información interna de Assembly.

Puede producir:

```text
AssemblyStatus:
Scheduled

Schedule:
valid

Modality:
defined

Location:
valid when required

Version:
updated
```

Todo debe quedar consistente dentro de una misma modificación.

---

# Ejemplo — ConvokeAssembly

Una convocatoria válida modifica la condición formal de Assembly.

Puede producir:

```text
AssemblyStatus:
Convoked

Convocation:
valid

ConvokedAt:
defined

Version:
updated
```

El envío posterior de Notifications permanece fuera.

---

# Ejemplo — StartAssembly

StartAssembly modifica exclusivamente Assembly.

No abre directamente:

```text
Voting
```

ni registra directamente:

```text
Participation
```

ni genera:

```text
Document
```

como modificaciones dentro del mismo Boundary.

---

# Ejemplo — CompleteAssembly

CompleteAssembly deja Assembly:

```text
Completed
```

de forma consistente.

Procesos externos pueden reaccionar posteriormente.

---

# Ejemplo — CancelAssembly

CancelAssembly cambia únicamente la consistencia propia de la
reunión.

Las reacciones externas a la cancelación se coordinan mediante
eventos.

---

# Ejemplo — ArchiveAssembly

ArchiveAssembly transforma Assembly en:

```text
Archived
```

sin archivar automáticamente otros Aggregates relacionados.

---

# Ejemplo — Proposal durante Assembly

Una Proposal puede ser creada mientras Assembly se encuentra:

```text
InProgress
```

pero la creación de Proposal pertenece al Aggregate Proposal.

Debe mantenerse:

```text
Assembly InProgress
```

y:

```text
Proposal Created
```

como hechos de Aggregates diferentes.

---

# Ejemplo — Voting durante Assembly

Una Voting puede iniciarse durante una Assembly.

Assembly proporciona el contexto.

Voting mantiene su propia consistencia.

---

# Ejemplo — Document después de Completion

Una acta puede ser creada después de:

```text
AssemblyCompleted
```

La ausencia temporal del Document no revierte Assembly a
InProgress.

---

# Ejemplo — Notification después de Convocation

Una Notification puede generarse después de:

```text
AssemblyConvoked
```

Si el proceso de Notification se retrasa, Assembly continúa siendo
Convoked.

---

# Ejemplo — Audit

Audit puede registrar posteriormente el hecho:

```text
AssemblyStarted
```

Sin embargo la ausencia momentánea de dicha proyección de Audit no
invalida InProgress.

---

# Test de Boundary

Debe probarse que una modificación de Assembly no modifique
directamente otro Aggregate.

Ejemplo:

```text
Given Assembly

When StartAssembly

Then Assembly changes

And Voting remains untouched

And Document remains untouched

And Notification remains untouched
```

---

# Test de Atomicidad

Debe probarse:

```text
Given valid Assembly

When operation changes multiple internal values

Then all changes are committed

Or none are committed
```

---

# Test de Invariante Interna

No debe poder persistirse:

```text
AssemblyStatus:
InProgress
```

con un estado interno incompatible con las invariantes definidas
para InProgress.

---

# Test de Referencia Externa

Una Assembly puede mantener:

```text
TerritoryId
```

sin cargar:

```text
Territory
```

dentro de la Aggregate Root.

---

# Test de No Absorción

Debe verificarse que:

```text
Proposal

Voting

Document

Notification

Audit
```

no formen parte del estado transaccional de Assembly.

---

# Test de Version

Toda modificación válida dentro del Boundary debe respetar:

```text
DOMAIN-006I-Versioning.md
```

Una modificación concurrente basada en una Version obsoleta debe
ser rechazada.

---

# Test de Read Model

La actualización o retraso de un Read Model no debe afectar la
consistencia interna del Aggregate.

---

# Test de Integration Failure

Un fallo posterior de integración no debe revertir un Domain Event
válidamente confirmado dentro del Boundary.

---

# Relación con DOMAIN-006-Aggregate

`DOMAIN-006-Aggregate.md` define conceptualmente qué representa
Assembly y cuáles son sus límites fundamentales.

Este documento formaliza específicamente su frontera de
consistencia.

No redefine el Aggregate.

Desarrolla la regla establecida en su fuente conceptual oficial.

---

# Relación con Lifecycle

`DOMAIN-006A-Lifecycle.md` define la evolución de Assembly.

Cada transición válida debe ocurrir íntegramente dentro del
Consistency Boundary.

---

# Relación con State Machine

`DOMAIN-006B-State-Machine.md` define las transiciones permitidas.

El Boundary garantiza que una transición nunca deje el Aggregate
en un estado parcial.

---

# Relación con Commands

`DOMAIN-006C-Commands.md` define las intenciones de modificación.

Cada Command de Assembly modifica exclusivamente una instancia del
Aggregate Assembly.

---

# Relación con Domain Events

`DOMAIN-006D-Domain-Events.md` define los hechos producidos por
Assembly.

Los eventos constituyen el mecanismo principal para comunicar
cambios fuera del Boundary sin permitir acceso directo a su estado
interno.

---

# Relación con Invariants

`DOMAIN-006E-Invariants.md` define las reglas que deben cumplirse en
todo estado válido.

El Consistency Boundary determina dónde dichas reglas deben
protegerse de manera inmediata.

---

# Relación con Permissions

`DOMAIN-006F-Permissions.md` define las capacidades requeridas para
intentar operaciones.

Permissions permanecen fuera del estado interno de Assembly y no
amplían el Boundary.

---

# Relación con Repository Contract

`DOMAIN-006G-Repository-Contract.md` define la persistencia del
Aggregate.

Repository debe persistir exactamente el Consistency Boundary de
Assembly como una unidad conceptual.

---

# Relación con Examples

`DOMAIN-006H-Examples.md` ilustra cómo Assembly interactúa con otros
Aggregates sin absorberlos.

Todos los ejemplos deben respetar esta frontera.

---

# Relación con Versioning

`DOMAIN-006I-Versioning.md` protege el Consistency Boundary frente
a modificaciones concurrentes.

Assembly.Version corresponde a toda la unidad de consistencia.

---

# Relación con Integration Events

`DOMAIN-006K-Integration-Events.md` define la comunicación hacia
otros Bounded Contexts y sistemas.

Los Integration Events se producen fuera de la Aggregate Root y no
expanden el Boundary.

---

# Relación con Read Model

`DOMAIN-006L-Read-Model.md` define proyecciones de consulta.

Los Read Models pueden combinar datos externos sin incorporarlos al
Write Model.

---

# Relación con Test Scenarios

`DOMAIN-006M-Test-Scenarios.md` debe verificar que todos los
Commands y transiciones preserven el Consistency Boundary definido
en este documento.

---

# Compatibilidad Arquitectónica

El Consistency Boundary de Assembly es compatible con:

* Domain-Driven Design;
* Tactical DDD;
* Aggregate Pattern;
* Repository Pattern;
* Clean Architecture;
* Hexagonal Architecture;
* CQRS;
* Event-Driven Architecture;
* Event Sourcing Compatible;
* Optimistic Concurrency;
* arquitectura distribuida;
* consistencia eventual entre Aggregates.

---

# Principios Arquitectónicos

El modelo mantiene:

```text
Aggregate
    =
Consistency Boundary
```

```text
Aggregate
    ≠
Entire Business Process
```

```text
Aggregate
    ≠
Bounded Context
```

```text
Aggregate
    ≠
Database
```

```text
Aggregate
    ≠
API
```

```text
Reference
    ≠
Ownership
```

```text
Relationship
    ≠
Same Transaction
```

```text
Strong Consistency
    inside Aggregate
```

```text
Eventual Consistency
    between Aggregates
```

```text
Read Model
    ≠
Write Model
```

```text
Persistence Structure
    ≠
Aggregate Structure
```

Estas separaciones constituyen principios esenciales para
preservar el diseño DDD de Assembly.

---

# Reglas de Diseño

El Consistency Boundary debe garantizar:

* una única Aggregate Root;
* una única unidad lógica de modificación;
* atomicidad interna;
* invariantes siempre válidas;
* Version común para toda la unidad;
* ausencia de modificaciones parciales;
* referencias externas mediante identificadores;
* autonomía de otros Aggregates;
* ausencia de transacciones distribuidas como mecanismo normal de
  consistencia;
* comunicación mediante Domain Events;
* Integration Events fuera de la Aggregate Root;
* Read Models fuera del Write Model;
* infraestructura fuera del dominio;
* autorización fuera del estado interno;
* alta cohesión;
* bajo acoplamiento.

---

# Definición de Éxito

El **Consistency Boundary** del Aggregate **Assembly** establece de
forma oficial qué conceptos deben permanecer unidos dentro de una
única unidad de consistencia y cuáles deben conservar su autonomía
fuera del Aggregate.

Assembly mantiene dentro de su frontera exclusivamente la
información necesaria para representar y proteger de manera
consistente la reunión formal:

* identidad;
* contexto organizacional;
* contexto territorial cuando corresponda;
* nombre;
* tipo;
* propósito;
* descripción;
* programación;
* modalidad;
* ubicación;
* convocatoria;
* reglas;
* condiciones de realización;
* estado;
* información temporal propia;
* Version.

Toda modificación válida de estos conceptos debe ocurrir como una
única operación consistente, preservando State Machine, Guards,
invariantes y Versioning.

Organization, Citizen, Membership, Role, Territory, Proposal,
Participation, Voting, Document, Notification, Audit e Integration
permanecen fuera del Consistency Boundary.

La relación con estos conceptos se realiza mediante
identificadores, Domain Events, Integration Events, Application
Services y mecanismos de coordinación externos, sin permitir que
Assembly modifique directamente sus estados.

La coexistencia de múltiples procesos dentro de una reunión no
implica que dichos procesos pertenezcan al mismo Aggregate.

La necesidad de mostrar información conjunta en una interfaz,
persistirla en una misma base de datos, utilizarla en un reporte o
coordinarla dentro de un mismo caso de uso tampoco modifica la
frontera conceptual.

Dentro de Assembly se mantiene consistencia inmediata.

Entre Assembly y otros Aggregates se permite consistencia eventual
cuando corresponda.

El Repository persiste exclusivamente la unidad conceptual de
Assembly, Version protege esa unidad frente a concurrencia y los
Domain Events permiten comunicar cambios fuera de la frontera sin
introducir acoplamiento directo.

De esta forma, **DOMAIN-006J-Consistency-Boundary.md** constituye
la definición normativa oficial del límite transaccional y de
consistencia del Aggregate Assembly, preservando su cohesión,
autonomía, escalabilidad y separación de responsabilidades dentro
de la arquitectura Domain-Driven Design de AURA Core.
