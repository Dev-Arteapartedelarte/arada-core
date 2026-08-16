# DOMAIN-013F — Integration Permissions

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
- DOMAIN-013G-Repository-Contract.md
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

Este documento define formalmente las **Permissions** conceptuales
aplicables a las operaciones del Aggregate **Integration**.

Las Permissions determinan quién o qué contexto autorizado puede
intentar ejecutar un Command sobre una Integration.

Las Permissions no reemplazan:

- Authentication;
- State Machine;
- Lifecycle;
- Guards;
- Invariants;
- Versioning;
- Consistency Boundary.

---

# Principio Fundamental

Debe mantenerse:

```text
Permission

=

Authority to Attempt a Domain Capability
```

y no:

```text
Permission

=

Guarantee of Domain Success
```

---

# Authorized no Significa Valid

Debe mantenerse:

```text
Authorized

≠

Domain Valid
```

Una operación autorizada todavía puede ser rechazada porque:

- State no permite la transición;
- Guard no se cumple;
- Invariant no se cumple;
- ExpectedVersion no coincide;
- el Aggregate no existe;
- el Aggregate ya existe cuando la operación requiere inexistencia.

---

# Permission versus Invariant

Debe mantenerse:

```text
Permission

≠

Invariant
```

Permissions determinan capacidad de intento.

Invariants determinan validez del estado del dominio.

---

# Permission versus State Machine

Debe mantenerse:

```text
Permission

≠

State Transition
```

Poseer Permission no crea una transición que no exista en:

```text
DOMAIN-013B-State-Machine.md
```

---

# Permission versus Command

Un Command expresa una intención.

Permission determina si esa intención puede ser intentada por el
requester correspondiente.

Debe mantenerse:

```text
Command

≠

Permission
```

---

# Authentication

Authentication permanece fuera del Aggregate.

Integration no:

- autentica usuarios;
- autentica servicios;
- valida passwords;
- valida tokens;
- administra sesiones;
- administra certificados;
- administra credenciales.

---

# Authentication versus Authorization

Debe mantenerse:

```text
Authentication

≠

Authorization
```

Authentication determina identidad autenticada.

Authorization determina si esa identidad puede intentar una capacidad.

---

# Authorization versus Domain Rules

Debe mantenerse:

```text
Authorization

≠

Domain Validation
```

El sistema de autorización puede permitir una intención.

La Aggregate Root todavía debe proteger sus propias reglas.

---

# Orden Conceptual

Conceptualmente:

```text
Authenticated Requester
        │
        ▼
  Authorization
        │
        ▼
    Permission
        │
        ▼
     Command
        │
        ▼
Integration Aggregate
        │
        ├── State Machine
        ├── Guards
        ├── Invariants
        └── Versioning
```

Esta representación es conceptual y no define mecanismo técnico de
implementación.

---

# Principio de Deny by Default

Cuando una capacidad requiera Permission y dicha Permission no esté
reconocida:

```text
Request

=

Rejected
```

---

# Least Privilege

Las Permissions deben expresar solamente las capacidades necesarias.

Debe mantenerse:

```text
Permission Scope

=

Minimum Required Domain Capability
```

---

# Roles

Este documento no define una taxonomía interna obligatoria de Roles
para Integration.

Debe mantenerse:

```text
Permission

≠

Role Definition
```

La relación entre Roles y Permissions pertenece al contexto
correspondiente.

---

# Role no es Permission

Debe mantenerse:

```text
Role

≠

Permission
```

Un Role puede eventualmente asociarse a capacidades mediante reglas
externas al Aggregate.

Integration no administra dicha asociación.

---

# Membership no es Permission

Debe mantenerse:

```text
Membership

≠

Permission
```

La existencia de Membership no concede automáticamente autoridad sobre
Integration.

---

# Citizen no es Permission

Debe mantenerse:

```text
Citizen

≠

Permission
```

---

# ActorId no es Permission

Cuando exista ActorId para trazabilidad:

```text
ActorId

≠

Permission
```

---

# ActorId no es Authorization

Debe mantenerse:

```text
ActorId

≠

Authorization Decision
```

ActorId puede representar a un actor relacionado con la intención o
el hecho.

No demuestra por sí mismo que la operación haya sido autorizada.

---

# Requester versus Actor

El requester que intenta un Command y el actor referenciado por un
hecho no deben suponerse necesariamente idénticos.

Debe mantenerse:

```text
Requester

≠

ActorId
```

salvo que el contexto correspondiente determine explícitamente que
representan la misma entidad.

---

# Permissions Oficiales

La versión 1.0 define conceptualmente las siguientes capacidades:

```text
Integration.Create

Integration.Activate

Integration.Suspend

Integration.Reactivate

Integration.Archive
```

Estas Permissions corresponden exclusivamente a los Commands oficiales
definidos en:

```text
DOMAIN-013C-Commands.md
```

---

# Integration.Create

`Integration.Create` representa autorización para intentar:

```text
CreateIntegration
```

No garantiza que la creación sea válida.

---

# Integration.Create y Existencia

Aunque exista:

```text
Permission = Integration.Create
```

si el IntegrationId ya corresponde a una Integration existente:

```text
CreateIntegration

=

Rejected
```

---

# Integration.Create no Permite Estado Arbitrario

`Integration.Create` no autoriza crear directamente:

```text
Active

Suspended

Archived
```

Toda nueva Integration comienza en Draft.

---

# Integration.Activate

`Integration.Activate` representa autorización para intentar:

```text
ActivateIntegration
```

---

# Integration.Activate no Evita State Machine

Aunque exista:

```text
Permission = Integration.Activate
```

el Command solamente puede ejecutarse válidamente desde:

```text
Draft
```

---

# Integration.Activate desde Active

Debe mantenerse:

```text
State = Active

Permission = Integration.Activate

Result = Rejected
```

---

# Integration.Activate desde Suspended

Debe mantenerse:

```text
State = Suspended

Permission = Integration.Activate

Result = Rejected
```

La operación correcta del Lifecycle desde Suspended corresponde a la
capacidad de reactivación.

---

# Integration.Activate desde Archived

Debe mantenerse:

```text
State = Archived

Permission = Integration.Activate

Result = Rejected
```

Archived es terminal.

---

# Integration.Suspend

`Integration.Suspend` representa autorización para intentar:

```text
SuspendIntegration
```

---

# Integration.Suspend no Evita State Machine

Aunque exista:

```text
Permission = Integration.Suspend
```

el Command solamente es válido desde:

```text
Active
```

---

# Integration.Suspend desde Draft

Debe mantenerse:

```text
State = Draft

Permission = Integration.Suspend

Result = Rejected
```

---

# Integration.Suspend desde Suspended

Debe mantenerse:

```text
State = Suspended

Permission = Integration.Suspend

Result = Rejected
```

---

# Integration.Suspend desde Archived

Debe mantenerse:

```text
State = Archived

Permission = Integration.Suspend

Result = Rejected
```

---

# Integration.Reactivate

`Integration.Reactivate` representa autorización para intentar:

```text
ReactivateIntegration
```

---

# Integration.Reactivate no Evita State Machine

Aunque exista:

```text
Permission = Integration.Reactivate
```

el Command solamente es válido desde:

```text
Suspended
```

---

# Integration.Reactivate desde Draft

Debe mantenerse:

```text
State = Draft

Permission = Integration.Reactivate

Result = Rejected
```

---

# Integration.Reactivate desde Active

Debe mantenerse:

```text
State = Active

Permission = Integration.Reactivate

Result = Rejected
```

---

# Integration.Reactivate desde Archived

Debe mantenerse:

```text
State = Archived

Permission = Integration.Reactivate

Result = Rejected
```

---

# Integration.Archive

`Integration.Archive` representa autorización para intentar:

```text
ArchiveIntegration
```

---

# Estados Permitidos para Integration.Archive

La Permission puede aplicarse a una intención sobre una Integration en:

```text
Draft

Active

Suspended
```

siempre que las demás reglas sean válidas.

---

# Integration.Archive desde Archived

Debe mantenerse:

```text
State = Archived

Permission = Integration.Archive

Result = Rejected
```

La Permission no elimina la terminalidad del State.

---

# Matriz Permission / Command

```text
Permission              Command

Integration.Create      CreateIntegration

Integration.Activate    ActivateIntegration

Integration.Suspend     SuspendIntegration

Integration.Reactivate  ReactivateIntegration

Integration.Archive     ArchiveIntegration
```

---

# Matriz Permission / Capability

```text
Permission              Domain Capability

Integration.Create      Create a new Integration

Integration.Activate    Activate a Draft Integration

Integration.Suspend     Suspend an Active Integration

Integration.Reactivate  Reactivate a Suspended Integration

Integration.Archive     Archive a non-Archived Integration
```

---

# Permission no Crea Command

Una Permission no introduce un Command inexistente.

Debe mantenerse:

```text
Permission Exists

≠

New Command Exists
```

---

# No Permissions para Commands Inexistentes

La versión 1.0 no define Permissions para:

```text
ConnectIntegration

DisconnectIntegration

RetryIntegration

FailIntegration

DeleteIntegration

CancelIntegration

ResetIntegration

UpdateIntegration

ModifyIntegration

SetIntegrationState
```

porque dichos Commands no forman parte del dominio oficial.

---

# No Permission de Retry Técnico

La versión 1.0 no define una Permission de dominio:

```text
Integration.Retry
```

asociada a retry técnico.

---

# No Permission de Connect

No se define:

```text
Integration.Connect
```

porque conectividad técnica no pertenece al Lifecycle.

---

# No Permission de Disconnect

No se define:

```text
Integration.Disconnect
```

---

# No Permission de Fail

No se define:

```text
Integration.Fail
```

porque Failed no es un State oficial.

---

# No Permission de Delete

No se define:

```text
Integration.Delete
```

porque DeleteIntegration no pertenece al Lifecycle versión 1.0.

---

# No Permission de Direct State Change

Nunca debe existir una Permission que habilite:

```text
setState()
```

directamente.

---

# No Permission de Direct Version Change

Nunca debe existir una Permission que habilite:

```text
setVersion()
```

---

# Permission no Modifica IntegrationId

Ninguna Permission permite modificar:

```text
IntegrationId
```

---

# Permission no Modifica CreatedAt

Ninguna Permission permite modificar:

```text
CreatedAt
```

---

# Permission no Modifica Version Arbitrariamente

Version evoluciona únicamente como consecuencia de comportamiento de
dominio válido.

---

# Permission no Evita Guards

Debe mantenerse:

```text
Permission Granted

+

Guard Failed

=

Rejected
```

---

# Permission no Evita Invariants

Debe mantenerse:

```text
Permission Granted

+

Invariant Failed

=

Rejected
```

---

# Permission no Evita Versioning

Debe mantenerse:

```text
Permission Granted

+

ConcurrencyConflict

=

Rejected
```

---

# Permission no Evita Lifecycle

Debe mantenerse:

```text
Permission Granted

+

Invalid Lifecycle Transition

=

Rejected
```

---

# Permission no Evita Terminalidad

Ninguna Permission permite reactivar:

```text
Archived
```

en versión 1.0.

---

# Permission no Autoriza Modificación Parcial

Poseer una Permission no autoriza persistir un Aggregate parcialmente
modificado.

---

# Permission no Cambia Consistency Boundary

Debe mantenerse:

```text
Permission

≠

Consistency Boundary Expansion
```

---

# Scope del Command

Una Permission de Integration autoriza una capacidad sobre el
Aggregate Integration correspondiente.

No autoriza modificar otros Aggregates.

---

# No Cross-Aggregate Authority

Una Permission de Integration no concede autoridad sobre:

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

---

# Integration.Create no Crea otros Aggregates

`Integration.Create` no permite crear:

- Organization;
- Citizen;
- Membership;
- Assembly;
- Notification;
- Audit.

---

# Integration.Activate no Activa otros Aggregates

`Integration.Activate` no modifica Lifecycle externo.

---

# Integration.Suspend no Suspende otros Aggregates

`Integration.Suspend` modifica únicamente Integration.

---

# Integration.Reactivate no Reactiva otros Aggregates

La reactivación pertenece exclusivamente a la Integration objetivo.

---

# Integration.Archive no Archiva otros Aggregates

El archivado no se propaga como transición atómica a otros
Aggregates.

---

# External Systems

Una Permission del dominio Integration no concede por sí misma
autoridad técnica o funcional sobre:

```text
FIWARE

Municipal Systems

External Platforms
```

---

# External Authorization

Las reglas de acceso de un sistema externo pertenecen al sistema o
contrato correspondiente.

Debe mantenerse:

```text
AURA Permission

≠

External System Permission
```

---

# External Permission no es AURA Permission

Del mismo modo:

```text
External Permission

≠

Integration Permission
```

---

# FIWARE Authorization

Una autorización existente en FIWARE no se convierte automáticamente
en:

```text
Integration.Create

Integration.Activate

Integration.Suspend

Integration.Reactivate

Integration.Archive
```

---

# Municipal Authorization

Una autorización existente en un sistema municipal tampoco se
convierte automáticamente en una Permission del Aggregate.

---

# Permission Mapping

Cualquier relación entre autorizaciones externas y capacidades de AURA
debe respetar contratos explícitos.

Este documento no define un mecanismo técnico de mapping.

---

# RBAC

Integration es compatible conceptualmente con modelos de autorización
basados en Roles.

Esto no significa que RBAC forme parte del Aggregate.

Debe mantenerse:

```text
RBAC Compatible

≠

RBAC Required by Domain
```

---

# ABAC

Integration también puede permanecer compatible conceptualmente con
autorización basada en atributos.

Debe mantenerse:

```text
ABAC Compatible

≠

ABAC Required by Domain
```

---

# No Modelo de Autorización Impuesto

Este documento no decide:

- RBAC;
- ABAC;
- ACL;
- policy engine;
- provider de identidad;
- protocolo de autenticación.

Solamente define capacidades conceptuales del dominio.

---

# Permission Evaluation

La evaluación de Authorization debe ocurrir antes de permitir que una
intención alcance comportamiento protegido del Aggregate.

La Aggregate Root no necesita conocer el mecanismo técnico utilizado
para obtener dicha decisión.

---

# Aggregate no Consulta Credenciales

Integration no debe recibir o interpretar:

```text
Password

AccessToken

RefreshToken

ApiKey

ClientSecret

PrivateKey
```

para decidir sus Invariants.

---

# Aggregate no Interpreta Token

Un token no forma parte de:

```text
Integration State
```

ni de:

```text
Permission Semantics
```

del Aggregate.

---

# Permission Result

Conceptualmente una evaluación de Permission permite distinguir:

```text
Allowed

Denied
```

como resultado de autorización.

Estos resultados no son Lifecycle States de Integration.

---

# Denied no es State

Debe mantenerse:

```text
Authorization Denied

≠

Integration State
```

---

# Permission Failure no Genera State

Una operación denegada no produce:

```text
Failed

Suspended

Archived
```

automáticamente.

---

# Permission Failure no Cambia Aggregate

Ante Permission insuficiente:

```text
State unchanged

Version unchanged

UpdatedAt unchanged

No success Domain Event
```

---

# Domain Event

Domain Events no contienen lógica de autorización.

Representan hechos posteriores a una intención válida y autorizada.

---

# Domain Event no Concede Permission

Debe mantenerse:

```text
Domain Event

≠

Permission Grant
```

---

# Integration Event no Concede Permission

Debe mantenerse:

```text
Integration Event

≠

Permission Grant
```

---

# External Message no Concede Permission

Debe mantenerse:

```text
External Message

≠

Authorization
```

---

# CorrelationId no Concede Permission

Debe mantenerse:

```text
CorrelationId

≠

Permission
```

---

# CausationId no Concede Permission

Debe mantenerse:

```text
CausationId

≠

Permission
```

---

# IntegrationId no Concede Permission

Conocer:

```text
IntegrationId
```

no concede autoridad para modificar el Aggregate.

---

# ExternalSystemId no Concede Permission

Conocer una identidad externa tampoco concede Permission de dominio.

---

# Permission y Version

Una Permission no permite establecer:

```text
ExpectedVersion
```

arbitrariamente como si fuera la Version real.

---

# Permission y Concurrency

Ninguna Permission permite ignorar:

```text
ConcurrencyConflict
```

---

# Permission y Repository

El Repository no decide Permissions.

Debe mantenerse:

```text
Repository

≠

Authorization Policy
```

---

# Repository no Concede Permission

Poder ejecutar:

```text
save()
```

técnicamente no significa poseer una Permission de dominio.

---

# Repository no Revoca Permission

El Repository tampoco administra revocaciones de autorización.

---

# Infrastructure Access

Poseer acceso técnico a:

- base de datos;
- broker;
- servidor;
- runtime;

no equivale a Permission de dominio.

Debe mantenerse:

```text
Infrastructure Access

≠

Integration Permission
```

---

# Database Privilege

Un privilegio de base de datos no autoriza modificar Integration
evitando la Aggregate Root.

---

# API Access

Tener acceso a una API no implica automáticamente autoridad para todas
las capacidades del Aggregate.

---

# Adapter Access

Un Adapter no adquiere Permissions por pertenecer a Infrastructure.

---

# Service Identity

Una identidad de servicio puede eventualmente ser autorizada por el
contexto correspondiente.

Integration no define cómo dicha identidad es representada o
autenticada.

---

# Human Identity

Una identidad humana también puede ser autorizada por el contexto
correspondiente.

Integration no administra su perfil.

---

# Permission Subject

Este documento no establece una única categoría obligatoria de sujeto
de autorización.

Una Permission puede ser evaluada para un requester reconocido por el
contexto de seguridad correspondiente.

---

# Permission Assignment

La asignación de Permissions no pertenece al Aggregate Integration.

---

# Permission Revocation

La revocación de Permissions tampoco modifica directamente el
Aggregate.

---

# Authorization Policy Change

Cambiar una política de autorización:

```text
≠

Integration State Change
```

---

# Permission History

Este documento no incorpora historial de Permissions dentro del
Aggregate Integration.

---

# Permission Snapshot

Integration no almacena una copia completa de las reglas de
autorización.

---

# Permission y Audit

Audit puede registrar hechos relevantes relacionados con operaciones
autorizadas o rechazadas cuando exista el contrato correspondiente.

Audit permanece fuera del Aggregate Integration.

---

# Audit no Decide Permission

Debe mantenerse:

```text
Audit

≠

Authorization Authority
```

---

# Notification no Decide Permission

Notification no concede ni revoca Permissions.

---

# Organization y Permission

Organization puede participar en contextos de autorización.

Sin embargo, Integration no administra las reglas internas de
Organization.

---

# Membership y Permission

Membership puede aportar contexto externo para una decisión de
autorización.

Integration no interpreta ni modifica Membership directamente.

---

# Role y Permission

Role puede aportar contexto para Authorization.

Integration no administra:

- Role assignment;
- Role hierarchy;
- Role lifecycle;
- Role permissions.

---

# Permission y Read Model

Read Models no conceden Permissions.

---

# Read Model no es Authorization Authority

Debe mantenerse:

```text
Read Model

≠

Authorization Authority
```

---

# Query Permissions

Las capacidades de lectura pueden requerir Authorization.

Sin embargo, este documento define las Permissions asociadas a los
Commands oficiales del Aggregate.

Las políticas específicas de acceso a Read Models se desarrollan
conforme al Security Model y a los contratos de lectura
correspondientes.

---

# Read versus Write

Debe mantenerse:

```text
Read Permission

≠

Write Permission
```

Poseer capacidad de lectura no concede:

```text
Integration.Create

Integration.Activate

Integration.Suspend

Integration.Reactivate

Integration.Archive
```

---

# Write no Implica Read Universal

Del mismo modo, una capacidad de escritura concreta no debe
interpretarse automáticamente como acceso universal a cualquier Read
Model.

---

# CQRS

En un modelo CQRS:

```text
Write Permissions

protect

Commands
```

mientras las políticas de lectura protegen los Read Models
correspondientes.

CQRS no modifica la semántica de las Permissions.

---

# Event Sourcing

Event Sourcing no modifica las Permissions.

---

# Replay

Replay no requiere reinterpretar cada evento histórico como un nuevo
Command autorizado.

Debe mantenerse:

```text
Replay

≠

New Authorization Decision
```

---

# Rehydration

Rehydration tampoco constituye una nueva intención protegida por una
Permission de Command.

---

# Projection

Projection no ejecuta Commands del Aggregate.

Por lo tanto no utiliza las Permissions de escritura para modificar
Integration.

---

# Integration Events

Publicar o consumir Integration Events no concede autoridad directa
sobre el Aggregate.

---

# Consumer Authorization

El acceso de consumidores a contratos de integración pertenece a las
reglas de seguridad de la frontera correspondiente.

No modifica las Permissions de los Commands de Integration.

---

# Publication Authorization

Una eventual autorización para publicar hacia un sistema externo no
equivale a:

```text
Integration.Activate
```

ni a otra Permission del Lifecycle.

---

# Technical Retry

Retry técnico no requiere una nueva Permission de dominio de Lifecycle
porque no constituye un nuevo Command por sí mismo.

---

# Technical Redelivery

La retransmisión técnica de una intención no crea automáticamente una
nueva Permission ni una nueva autorización.

---

# Idempotencia

La estrategia técnica de idempotencia permanece fuera de este
documento.

No modifica la semántica de las Permissions.

---

# FIWARE

Las Permissions de Integration no dependen conceptualmente de:

```text
FIWARE

NGSI-LD

Context Broker

Orion
```

---

# Sistemas Municipales

Las Permissions tampoco dependen conceptualmente de un mecanismo
específico de autorización municipal.

---

# Protocolos

Las Permissions son independientes de:

```text
HTTP

REST

GraphQL

MQTT

AMQP
```

---

# Brokers

Las Permissions no dependen de:

```text
Kafka

RabbitMQ

NATS
```

---

# Frameworks

Las Permissions no dependen de:

- FastAPI;
- Django;
- React;
- Next.js;
- otro framework concreto.

---

# Tokens

Una Permission no se define como:

```text
JWT Claim

Access Token

API Key
```

Estos pueden participar en mecanismos externos de Authentication o
Authorization.

No definen por sí mismos la semántica del dominio.

---

# Security Model

Las reglas complementarias se definen en:

```text
DOMAIN-013O-Security-Model.md
```

Permissions y Security Model deben permanecer coherentes.

---

# Data Minimization

La decisión de Authorization no requiere introducir dentro del
Aggregate información adicional innecesaria sobre el requester.

---

# No Credential Persistence

Integration no persiste credenciales para recordar por qué una
operación fue autorizada.

---

# No Authorization State

La versión 1.0 no define estados como:

```text
Authorized

Unauthorized

AccessDenied

PermissionPending
```

dentro del Lifecycle de Integration.

---

# Permission Denied no es Domain Event de Lifecycle

Una denegación no produce automáticamente:

```text
IntegrationSuspended

IntegrationArchived

IntegrationFailed
```

---

# Permission Granted no es Domain Event de Lifecycle

Conceder una Permission tampoco produce automáticamente:

```text
IntegrationActivated
```

---

# Permission Changes no Incrementan Integration.Version

Cambiar una política o asignación externa de autorización no modifica:

```text
Integration.Version
```

por sí mismo.

---

# Permission Changes no Modifican UpdatedAt

Una modificación externa de autorización no actualiza:

```text
Integration.UpdatedAt
```

por sí misma.

---

# Permission Changes no Modifican State

Debe mantenerse:

```text
Authorization Policy Change

≠

Integration State Transition
```

---

# Security Failure

Un fallo técnico de Authentication o Authorization no cambia el State
del Aggregate.

---

# No Auto-Suspension por Authorization Failure

Debe mantenerse:

```text
Authorization Failure

≠

SuspendIntegration
```

---

# No Auto-Archive por Authorization Failure

Debe mantenerse:

```text
Authorization Failure

≠

ArchiveIntegration
```

---

# Permission Evaluation Failure

Si el sistema no puede determinar una autorización requerida, la
operación protegida no debe considerarse autorizada.

Esto no cambia el State del Aggregate.

---

# Permission y Consistency Boundary

La decisión de Permission permanece conceptualmente fuera del estado
interno de Integration.

El Aggregate recibe una intención autorizada y protege su propio
Consistency Boundary.

---

# No Cross-Context Permission Mutation

Integration no modifica:

- usuarios;
- roles;
- memberships;
- credenciales;
- políticas externas;

como consecuencia de ejecutar sus Commands.

---

# Permission Scope no se Propaga

Poseer:

```text
Integration.Archive
```

sobre una Integration no implica poseerla sobre todas las Integration.

La determinación concreta del alcance de autorización pertenece al
contexto correspondiente.

---

# No Global Permission Inference

Este documento no establece que una Permission concedida para una
instancia sea automáticamente global.

---

# No Instance Scope Architecture

Este documento tampoco define el mecanismo técnico utilizado para
representar scope.

---

# Performance

La optimización de Authorization no puede permitir evitar Permissions.

Debe mantenerse:

```text
Performance Optimization

≠

Permission Bypass
```

---

# Cache de Authorization

La existencia técnica de cache de decisiones no forma parte del
dominio Integration.

No debe alterar la semántica de las Permissions.

---

# Availability

La indisponibilidad de un mecanismo técnico de Authorization no crea
un nuevo State del Aggregate.

---

# Evolución Futura

Toda nueva Permission debe corresponder a una capacidad real del
dominio.

No debe introducirse una Permission sin que exista comportamiento
formalmente definido que la justifique.

---

# Regla para Incorporar una Nueva Permission

Una nueva Permission debe responder conceptualmente:

```text
What domain capability is being protected?

Which Command or explicit behavior requires it?

Does the capability belong to Integration?

Does it preserve Lifecycle?

Does it preserve State Machine?

Does it preserve Invariants?

Does it preserve Consistency Boundary?
```

---

# No Permission sin Capability

Debe mantenerse:

```text
No Domain Capability

=

No Domain Permission
```

---

# No Permission desde Infrastructure

No debe crearse una Permission de dominio solamente porque exista:

- endpoint;
- método HTTP;
- broker operation;
- database operation;
- SDK method;
- FIWARE operation;
- municipal API operation.

---

# Impacto de una Nueva Permission

Toda nueva Permission debe revisar cuando corresponda:

```text
DOMAIN-013-Aggregate.md

DOMAIN-013A-Lifecycle.md

DOMAIN-013B-State-Machine.md

DOMAIN-013C-Commands.md

DOMAIN-013D-Domain-Events.md

DOMAIN-013E-Invariants.md

DOMAIN-013F-Permissions.md

DOMAIN-013I-Versioning.md

DOMAIN-013J-Consistency-Boundary.md

DOMAIN-013M-Test-Scenarios.md

DOMAIN-013O-Security-Model.md

DOMAIN-013P-Extension-Points.md
```

---

# Regla de No Inferencia

Debe mantenerse:

```text
Technical Privilege

≠

Domain Permission
```

y:

```text
External Authorization

≠

Automatic AURA Permission
```

y:

```text
New Infrastructure Operation

≠

New Domain Permission
```

---

# Reglas Fundamentales

Las Permissions de Integration deben cumplir:

1. Permission representa autoridad para intentar una capacidad del
   dominio.
2. Permission no garantiza éxito.
3. Authorized no significa Domain Valid.
4. Permission no es Invariant.
5. Permission no es State Machine.
6. Permission no es Command.
7. Authentication permanece fuera del Aggregate.
8. Authentication no es Authorization.
9. Authorization no es Domain Validation.
10. Deny by Default aplica cuando una capacidad requiere Permission.
11. Least Privilege limita la autorización a la capacidad necesaria.
12. Integration no define una taxonomía obligatoria de Roles.
13. Role no es Permission.
14. Membership no es Permission.
15. Citizen no es Permission.
16. ActorId no es Permission.
17. ActorId no es Authorization.
18. Requester y ActorId no se suponen idénticos automáticamente.
19. La versión 1.0 define Integration.Create.
20. La versión 1.0 define Integration.Activate.
21. La versión 1.0 define Integration.Suspend.
22. La versión 1.0 define Integration.Reactivate.
23. La versión 1.0 define Integration.Archive.
24. Integration.Create protege CreateIntegration.
25. Integration.Activate protege ActivateIntegration.
26. Integration.Suspend protege SuspendIntegration.
27. Integration.Reactivate protege ReactivateIntegration.
28. Integration.Archive protege ArchiveIntegration.
29. Integration.Create no permite crear un State distinto de Draft.
30. Integration.Activate no permite evitar Draft → Active.
31. Integration.Suspend no permite evitar Active → Suspended.
32. Integration.Reactivate no permite evitar Suspended → Active.
33. Integration.Archive no permite archivar nuevamente Archived.
34. Permission no crea Commands.
35. No existen Permissions para Commands inexistentes.
36. No existe Integration.Connect.
37. No existe Integration.Disconnect.
38. No existe Integration.Fail.
39. No existe Integration.Retry como Permission de Lifecycle.
40. No existe Integration.Delete en versión 1.0.
41. Ninguna Permission permite setState().
42. Ninguna Permission permite setVersion().
43. Ninguna Permission permite modificar IntegrationId.
44. Ninguna Permission permite modificar CreatedAt.
45. Permission no evita Guards.
46. Permission no evita Invariants.
47. Permission no evita State Machine.
48. Permission no evita Lifecycle.
49. Permission no evita Versioning.
50. Permission no evita ConcurrencyConflict.
51. Permission no permite reactivar Archived.
52. Permission no expande Consistency Boundary.
53. Una Permission de Integration no concede autoridad sobre otros
    Aggregates.
54. Integration.Create no crea otros Aggregates.
55. Integration.Activate no activa otros Aggregates.
56. Integration.Suspend no suspende otros Aggregates.
57. Integration.Reactivate no reactiva otros Aggregates.
58. Integration.Archive no archiva otros Aggregates.
59. AURA Permission no es External System Permission.
60. External Permission no es Integration Permission.
61. FIWARE Authorization no se convierte automáticamente en una
    Permission de Integration.
62. Municipal Authorization no se convierte automáticamente en una
    Permission de Integration.
63. Mapping de autorizaciones requiere contratos explícitos.
64. RBAC es compatible pero no obligatorio.
65. ABAC es compatible pero no obligatorio.
66. Este documento no decide mecanismo técnico de Authorization.
67. Integration no interpreta credenciales.
68. Allowed y Denied no son Lifecycle States.
69. Permission Failure no cambia State.
70. Permission Failure no incrementa Version.
71. Permission Failure no modifica UpdatedAt.
72. Permission Failure no produce Domain Event de éxito.
73. Domain Event no concede Permission.
74. Integration Event no concede Permission.
75. External Message no concede Permission.
76. CorrelationId no concede Permission.
77. CausationId no concede Permission.
78. IntegrationId no concede Permission.
79. ExternalSystemId no concede Permission.
80. Repository no decide Permissions.
81. Repository access no equivale a Permission.
82. Infrastructure access no equivale a Permission.
83. Database privilege no equivale a Permission.
84. API access no equivale a autoridad total.
85. Adapter no adquiere Permission automáticamente.
86. La asignación de Permissions permanece fuera del Aggregate.
87. La revocación de Permissions permanece fuera del Aggregate.
88. Cambiar una Authorization Policy no modifica State.
89. Cambiar una Authorization Policy no modifica Version.
90. Cambiar una Authorization Policy no modifica UpdatedAt.
91. Read Permission no es Write Permission.
92. Read Model no concede Permission.
93. CQRS no modifica semántica de Permissions.
94. Event Sourcing no modifica semántica de Permissions.
95. Replay no representa nueva Authorization.
96. Rehydration no representa nueva Authorization.
97. Technical Retry no crea una nueva Permission.
98. Protocolos, brokers y frameworks no definen Permissions del
    dominio.
99. Technical Privilege no es Domain Permission.
100. Toda nueva Permission requiere una capacidad explícita del
     dominio.

---

# Restricciones

No está permitido:

- interpretar Authentication como Authorization;
- interpretar Authorization como Domain Validation;
- considerar una Permission como garantía de éxito;
- utilizar Permission para evitar State Machine;
- utilizar Permission para evitar Lifecycle;
- utilizar Permission para evitar Guards;
- utilizar Permission para evitar Invariants;
- utilizar Permission para evitar Versioning;
- utilizar Permission para ignorar ConcurrencyConflict;
- utilizar Permission para modificar IntegrationId;
- utilizar Permission para modificar State directamente;
- utilizar Permission para modificar Version directamente;
- utilizar Permission para modificar CreatedAt;
- utilizar Permission para reactivar Archived;
- utilizar Permission para crear una transición inexistente;
- utilizar Integration.Create para crear Active, Suspended o Archived;
- utilizar Integration.Activate fuera de Draft;
- utilizar Integration.Suspend fuera de Active;
- utilizar Integration.Reactivate fuera de Suspended;
- utilizar Integration.Archive desde Archived;
- introducir Integration.Connect;
- introducir Integration.Disconnect;
- introducir Integration.Fail;
- introducir Integration.Retry como Permission de Lifecycle;
- introducir Integration.Delete;
- introducir Permissions para Commands inexistentes;
- interpretar Role como Permission automáticamente;
- interpretar Membership como Permission automáticamente;
- interpretar Citizen como Permission;
- interpretar ActorId como Permission;
- interpretar CorrelationId como Permission;
- interpretar CausationId como Permission;
- interpretar IntegrationId como Permission;
- interpretar una autorización FIWARE como Permission interna
  automáticamente;
- interpretar una autorización municipal como Permission interna
  automáticamente;
- utilizar acceso técnico a Infrastructure como Domain Permission;
- utilizar acceso a base de datos como Domain Permission;
- utilizar acceso a API como autorización universal;
- permitir que Repository decida Permissions;
- permitir que Read Model conceda Permissions;
- almacenar credenciales dentro del Aggregate para resolver
  Permissions;
- convertir Allowed o Denied en Lifecycle States;
- suspender automáticamente una Integration por Permission Failure;
- archivar automáticamente una Integration por Permission Failure;
- incrementar Version por cambio de Authorization Policy;
- modificar UpdatedAt por cambio de Authorization Policy;
- considerar Replay como nueva autorización;
- considerar Rehydration como nueva autorización;
- crear Permissions por conveniencia de Infrastructure;
- crear Permissions por nombres de endpoints;
- crear Permissions por operaciones de broker;
- crear Permissions por acciones de FIWARE;
- crear Permissions por operaciones municipales;
- introducir una nueva Permission sin una capacidad real del dominio.

---

# Compatibilidad Arquitectónica

Las Permissions de Integration son compatibles conceptualmente con:

- Domain-Driven Design;
- Aggregate Pattern;
- Command Pattern;
- Clean Architecture;
- Hexagonal Architecture;
- SOLID;
- CQRS;
- Event-Driven Architecture;
- Event Sourcing Compatible;
- modelos externos de Authorization;
- Least Privilege;
- Deny by Default.

Estas compatibilidades no imponen:

- RBAC;
- ABAC;
- ACL;
- Identity Provider;
- protocolo;
- token;
- framework;
- broker;
- base de datos;
- FIWARE;
- sistema municipal.

---

# Definición de Éxito

Las Permissions del Aggregate **Integration** protegen las capacidades
oficiales de modificación sin confundirse con Authentication,
Lifecycle o reglas internas del dominio.

La relación oficial versión 1.0 queda definida como:

```text
Integration.Create
        │
        ▼
CreateIntegration

Integration.Activate
        │
        ▼
ActivateIntegration

Integration.Suspend
        │
        ▼
SuspendIntegration

Integration.Reactivate
        │
        ▼
ReactivateIntegration

Integration.Archive
        │
        ▼
ArchiveIntegration
```

El modelo garantiza que:

- una Permission solamente autorice intentar una capacidad;
- Authentication permanezca separada de Authorization;
- Authorization permanezca separada de Domain Validation;
- State Machine continúe siendo autoridad sobre transiciones;
- Invariants continúen siendo obligatorias;
- Versioning continúe siendo obligatorio;
- ConcurrencyConflict no pueda evitarse mediante privilegios;
- Archived permanezca terminal;
- IntegrationId permanezca inmutable;
- Commands inexistentes no generen Permissions;
- Roles no se conviertan automáticamente en Permissions;
- Membership no conceda autoridad automáticamente;
- ActorId no represente Authorization;
- sistemas externos no concedan autoridad directa sobre Integration;
- FIWARE no determine las Permissions del dominio;
- sistemas municipales no determinen las Permissions del dominio;
- Repository no decida Authorization;
- Read Models no concedan autoridad de escritura;
- acceso técnico no equivalga a autoridad de dominio;
- cambios de Authorization Policy no modifiquen el Aggregate;
- fallos de Authorization no produzcan transiciones del Lifecycle;
- RBAC y ABAC permanezcan como compatibilidades y no como decisiones
  impuestas por el dominio;
- cada nueva Permission requiera una capacidad real y explícitamente
  definida.

De esta forma, `DOMAIN-013F-Permissions.md` establece formalmente las
Permissions oficiales del Aggregate **Integration** conforme al patrón
consolidado de AURA Core.