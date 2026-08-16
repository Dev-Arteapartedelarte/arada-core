# DOMAIN-012F — Audit Permissions

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
- DOMAIN-012G-Repository-Contract.md
- DOMAIN-012I-Versioning.md
- DOMAIN-012J-Consistency-Boundary.md
- DOMAIN-012L-Read-Model.md
- DOMAIN-012O-Security-Model.md

---

# Objetivo

Este documento define formalmente el modelo conceptual de
**Permissions** aplicable al Aggregate **Audit**.

Su propósito es establecer las reglas que determinan cuándo una
intención puede ser presentada al dominio para intentar ejecutar
comportamiento sobre Audit.

Permissions protege el acceso a las capacidades del Aggregate.

No reemplaza:

- Authentication;
- Lifecycle;
- State Machine;
- Commands;
- Invariants;
- Versioning;
- Consistency Boundary.

---

# Principio Fundamental

Debe mantenerse:

```text
Permission

≠

Domain Rule
```

y:

```text
Authorized

≠

Automatically Valid
```

Una operación puede encontrarse autorizada y, aun así, ser
rechazada porque viola:

- State Machine;
- precondiciones;
- Invariants;
- Versioning;
- Consistency Boundary.

---

# Separación de Responsabilidades

Debe mantenerse separación explícita entre:

```text
Authentication

Authorization

Domain Validation
```

Conceptualmente:

```text
Actor / Process
      │
      ▼
Authentication
      │
      ▼
Authorization
      │
      ▼
   Command
      │
      ▼
    Audit
      │
      ├── State Machine
      ├── Invariants
      ├── Versioning
      └── Domain Behavior
```

Cada responsabilidad permanece en su límite correspondiente.

---

# Authentication

Authentication responde conceptualmente:

```text
Who or what is presenting the interaction?
```

Audit no autentica actores ni procesos.

El Aggregate no:

- valida passwords;
- valida tokens;
- crea sesiones;
- mantiene sesiones;
- administra certificados;
- administra proveedores de identidad;
- administra OAuth;
- administra JWT.

Debe mantenerse:

```text
Authentication

∉

Audit Aggregate
```

---

# Authorization

Authorization responde conceptualmente:

```text
Is this actor or process allowed to request this capability?
```

La decisión de autorización debe resolverse antes de ejecutar
comportamiento del Aggregate.

Conceptualmente:

```text
Authorization Decision

    │
    ├── Denied
    │      │
    │      ▼
    │   Reject
    │
    └── Allowed
           │
           ▼
        Audit
```

---

# Domain Validation

Después de una autorización válida, Audit continúa siendo
responsable de proteger su dominio.

Debe validar:

- intención;
- State Machine;
- precondiciones;
- Invariants;
- identidad;
- Version;
- Consistency Boundary.

Debe mantenerse:

```text
Authorization Passed

↓

Domain Validation Required
```

---

# Least Privilege

Las capacidades deben concederse aplicando el principio:

```text
Least Privilege
```

Un actor o proceso debe disponer únicamente de las capacidades
necesarias para cumplir su responsabilidad.

La política concreta que determina dichas capacidades permanece
fuera del Aggregate.

---

# Deny by Default

Debe aplicarse conceptualmente:

```text
No Explicit Authorization

↓

Denied
```

La ausencia de autorización no debe interpretarse como permiso
implícito.

Este principio no introduce nuevos Roles ni Commands.

---

# Command Oficial

La versión 1.0 define un único Command:

```text
RecordAudit
```

Por lo tanto, la única capacidad de escritura del dominio que
requiere autorización explícita en esta versión es la capacidad de
solicitar:

```text
RecordAudit
```

---

# Permission para RecordAudit

`RecordAudit` solamente puede ser presentado al Aggregate por un
actor o proceso autorizado conforme a la política aplicable.

Conceptualmente:

```text
Authorized Actor / Process

    │
    ▼

RecordAudit

    │
    ▼

Audit
```

La Permission no garantiza que el Command sea aceptado.

---

# RecordAudit Autorizado

Incluso cuando:

```text
Permission = Allowed
```

Audit debe validar:

```text
No Audit → Recorded
```

y todas las Invariants aplicables.

Por lo tanto:

```text
Allowed RecordAudit

+

Invalid Domain Conditions

=

Rejected
```

---

# RecordAudit No Autorizado

Si la autorización es rechazada:

```text
RecordAudit

↓

Not Authorized

↓

Rejected
```

El Aggregate no debe ejecutar comportamiento de escritura como
consecuencia de dicha intención.

No debe producirse:

- Audit válido nuevo;
- cambio de estado;
- incremento de Version;
- cambio de timestamps;
- AuditRecorded.

---

# No Taxonomía Interna de Roles

La versión 1.0 no establece dentro de Audit una taxonomía obligatoria
de actores como:

```text
Administrator

Auditor

Operator

Citizen

MunicipalUser

SystemAdministrator
```

ni equivalentes.

Este documento no asigna `RecordAudit` a un Role concreto.

La autorización pertenece a las políticas aplicables del ecosistema
AURA.

---

# Actor Humano y Proceso

La capacidad de originar una operación autorizada puede
corresponder conceptualmente a:

```text
Actor

or

Authorized Process
```

según el flujo aplicable.

Este documento no establece que Audit deba ser registrado
exclusivamente por una persona ni exclusivamente por un proceso
automatizado.

---

# Procesos de Audit

Un proceso que reaccione a un hecho de otro Aggregate puede estar
autorizado para presentar:

```text
RecordAudit
```

conforme a la política aplicable.

Conceptualmente:

```text
Source Domain Fact
      │
      ▼
Authorized Audit Process
      │
      ▼
RecordAudit
      │
      ▼
Audit
```

La autorización del proceso no convierte el Source Domain Event en
un Command de Audit.

---

# Source Aggregate no Autoriza Audit

El hecho de que otro Aggregate produzca un Domain Event no concede
por sí mismo autorización directa para modificar Audit.

Debe mantenerse:

```text
Source Domain Event

≠

Authorization Decision
```

La coordinación correspondiente debe aplicar la política de
autorización definida para Audit Management.

---

# ActorId

Cuando:

```text
ActorId
```

forme parte de la información auditable, su presencia no equivale a
una Permission.

Debe mantenerse:

```text
ActorId

≠

Authorization
```

y:

```text
ActorId

≠

Permission
```

ActorId representa información de trazabilidad cuando corresponda.

---

# Source Actor y Command Actor

El actor asociado al hecho auditado no debe confundirse
automáticamente con el actor o proceso que presenta `RecordAudit`.

Conceptualmente:

```text
Source Actor

≠

Command Requester
```

salvo que el flujo correspondiente establezca que son la misma
identidad.

Audit no debe inferir dicha equivalencia.

---

# Permission no es Ownership

Una Permission para ejecutar:

```text
RecordAudit
```

no concede ownership sobre:

- Audit previamente existentes;
- Source Aggregates;
- Source Domain Events;
- Citizens;
- Organizations;
- Documents;
- Notifications;
- otros Aggregates.

Debe mantenerse:

```text
Permission

≠

Ownership
```

---

# Ownership del Aggregate

Audit mantiene su propio Consistency Boundary.

La capacidad de solicitar una operación no altera el ownership del
Aggregate.

Debe mantenerse:

```text
Authorized Requester

≠

Aggregate Owner
```

como regla conceptual general.

---

# No Ownership Organizacional Implícito

La versión 1.0 no establece que toda unidad Audit pertenezca
obligatoriamente a una:

```text
Organization
```

mediante ownership organizacional.

Por lo tanto, este documento no define permisos basados
automáticamente en OrganizationId.

Cualquier política de ese tipo requerirá definición explícita en el
contexto correspondiente.

---

# Permission no Modifica AuditId

Ningún permiso concede capacidad para modificar:

```text
AuditId
```

Debe mantenerse:

```text
Permission

≠

Identity Mutation Authority
```

AuditId permanece protegido por las Invariants.

---

# Permission no Modifica State Directamente

Ningún actor o proceso, aunque esté autorizado, puede ejecutar:

```text
setStatus(...)
```

o mecanismo equivalente.

Debe mantenerse:

```text
Authorized

≠

Direct State Mutation
```

---

# Permission no Modifica Version Directamente

Ninguna Permission concede autoridad para establecer:

```text
Version
```

arbitrariamente.

Version evoluciona exclusivamente conforme a una modificación válida
del Aggregate.

---

# Permission no Modifica CreatedAt

Ningún permiso permite cambiar:

```text
CreatedAt
```

después de la creación.

CreatedAt permanece protegido por las Invariants.

---

# Permission no Reescribe el Hecho Histórico

Un actor autorizado no puede utilizar su Permission para modificar
retrospectivamente el significado del hecho registrado.

Debe mantenerse:

```text
Authorization

≠

Historical Rewrite Authority
```

---

# Permission no Modifica Source Fact

Una Permission perteneciente a Audit no concede autoridad para
modificar el hecho originador.

Debe mantenerse:

```text
Audit Permission

≠

Source Fact Mutation Permission
```

---

# Permission no Modifica Source Aggregate

Una Permission sobre Audit no concede autoridad sobre:

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

Integration
```

Cada Aggregate o Bounded Context conserva sus propias reglas de
autorización.

---

# Separación de Permissions entre Aggregates

Debe mantenerse:

```text
Permission on Audit

≠

Permission on Assembly
```

```text
Permission on Audit

≠

Permission on Document
```

```text
Permission on Audit

≠

Permission on Notification
```

y de igual forma respecto de cualquier otro Aggregate.

---

# Permission no Permite Transacciones Multi-Aggregate

La autorización para `RecordAudit` no permite modificar
simultáneamente otro Aggregate dentro de la misma operación de
dominio.

Debe mantenerse:

```text
Authorized Audit Operation

≠

Distributed Mutation Authority
```

---

# Permission y Lifecycle

Lifecycle establece:

```text
No Audit → Recorded
```

Permissions no puede añadir nuevas transiciones.

Debe mantenerse:

```text
Permission

≠

Lifecycle Extension
```

---

# Permission y State Machine

La única transición oficial continúa siendo:

```text
No Audit → Recorded
```

Ninguna Permission puede habilitar:

```text
Recorded → Another State
```

porque dicha transición no existe en la versión 1.0.

---

# Permission y Recorded

Recorded permanece terminal independientemente del nivel de
autorización.

Debe mantenerse:

```text
Elevated Permission

≠

Recorded State Override
```

---

# Permission y Invariants

Toda operación autorizada debe cumplir:

```text
DOMAIN-012E-Invariants.md
```

Ninguna Permission puede:

- suspender una Invariant;
- ignorar una Invariant;
- modificar una Invariant durante ejecución;
- corregir automáticamente una violación;
- introducir una excepción no definida.

---

# Permission y Versioning

Una operación autorizada no puede evitar:

```text
Versioning
```

ni:

```text
Optimistic Concurrency
```

cuando corresponda.

Debe mantenerse:

```text
Authorized Write

≠

Concurrency Bypass
```

---

# Permission y ConcurrencyConflict

Si una operación autorizada encuentra:

```text
ConcurrencyConflict
```

debe ser rechazada conforme al contrato correspondiente.

La Permission no transforma un conflicto en una escritura válida.

---

# Permission y Repository

El Repository no decide Permissions.

Debe mantenerse:

```text
Repository

≠

Authorization Policy
```

El Repository persiste y recupera Audit conforme a su contrato.

No concede capacidades de dominio a actores.

---

# Acceso Directo al Repository

El acceso técnico a la implementación del Repository no debe
considerarse una Permission de dominio para evitar la Aggregate
Root.

Debe mantenerse:

```text
Infrastructure Access

≠

Domain Permission
```

---

# Permission y Domain Events

AuditRecorded representa un hecho posterior a una operación válida.

El Domain Event no contiene lógica destinada a decidir si el actor
estaba autorizado.

Conceptualmente:

```text
Authorization

    │
    ▼

RecordAudit

    │
    ▼

Domain Validation

    │
    ▼

AuditRecorded
```

---

# Operación No Autorizada y Domain Events

Una operación no autorizada no produce:

```text
AuditRecorded
```

Debe mantenerse:

```text
Unauthorized Operation

↓

No Success Domain Event
```

---

# Domain Event no Concede Permission

La recepción de:

```text
AuditRecorded
```

no concede automáticamente a ningún consumidor Permission sobre
Audit.

Debe mantenerse:

```text
Domain Event Consumption

≠

Authorization Grant
```

---

# Integration Event no Concede Permission

Un Integration Event tampoco constituye Permission para modificar
Audit.

Debe mantenerse:

```text
Integration Event

≠

Authorization Grant
```

Cualquier operación de escritura debe atravesar la autorización y
comportamiento correspondientes.

---

# Sistemas Externos

Un sistema externo autorizado para integrarse con AURA no obtiene
automáticamente Permission directa sobre el Aggregate Audit.

Debe mantenerse:

```text
Authorized Integration

≠

Direct Aggregate Mutation
```

---

# FIWARE

La autenticación o autorización utilizada por FIWARE permanece fuera
del Aggregate.

Una identidad técnica FIWARE no concede por sí misma Permission de
dominio sobre Audit.

Debe mantenerse:

```text
FIWARE Authorization

≠

Automatic Audit Permission
```

La equivalencia entre una identidad externa y una capacidad del
dominio debe resolverse en la frontera correspondiente.

---

# Sistemas Municipales

Una identidad o permiso perteneciente a una plataforma municipal no
constituye automáticamente una Permission de Audit.

Debe mantenerse:

```text
Municipal Permission

≠

Automatic AURA Audit Permission
```

La traducción de capacidades pertenece a los contratos y políticas
correspondientes.

---

# Delegación

Cuando AURA permita delegación de autoridad, dicha delegación debe
resolverse fuera del Aggregate.

Audit recibe únicamente una intención cuya autorización ya fue
determinada.

La versión 1.0 no define:

- modelo de delegación;
- jerarquía de delegados;
- duración de delegación;
- transferencia de Permissions.

---

# RBAC

El modelo es compatible conceptualmente con:

```text
Role-Based Access Control
```

sin que Audit dependa de una implementación RBAC concreta.

Este documento no define:

- Roles obligatorios;
- jerarquías de Roles;
- tablas Role-Permission;
- asignaciones de usuarios.

---

# ABAC

El modelo también es compatible conceptualmente con:

```text
Attribute-Based Access Control
```

sin incorporar atributos de autorización dentro del Aggregate como
estado obligatorio.

Este documento no define una política ABAC concreta.

---

# RBAC y ABAC

Debe mantenerse:

```text
Authorization Model

outside

Audit Aggregate
```

independientemente de si la implementación utiliza:

- RBAC;
- ABAC;
- combinación de políticas;
- otro mecanismo compatible.

---

# Claims

Claims técnicos de identidad o autorización no forman parte del
estado de Audit por defecto.

Debe mantenerse:

```text
Security Claim

≠

Audit Domain State
```

La capa correspondiente interpreta los claims y produce una decisión
de autorización.

---

# Tokens

Tokens no constituyen Permissions de dominio.

Debe mantenerse:

```text
Token

≠

Domain Permission
```

El Aggregate no recibe ni valida tokens como parte de su
comportamiento.

---

# Credenciales

Audit no almacena:

- passwords;
- access tokens;
- refresh tokens;
- API keys;
- private keys;
- secretos;
- sesiones.

La capacidad autorizada debe llegar al dominio sin introducir
credenciales dentro de su estado.

---

# Permission y CorrelationId

CorrelationId no representa Permission.

Debe mantenerse:

```text
CorrelationId

≠

Authorization
```

Su propósito pertenece a trazabilidad.

---

# Permission y CausationId

CausationId tampoco representa Permission.

Debe mantenerse:

```text
CausationId

≠

Authorization
```

Una relación causal no concede capacidad de escritura.

---

# Permission y SourceEventId

La existencia de:

```text
SourceEventId
```

no concede autorización.

Debe mantenerse:

```text
SourceEventId

≠

Permission
```

SourceEventId identifica un hecho de origen cuando corresponda.

---

# Permission y AuditId

Conocer:

```text
AuditId
```

no concede Permission sobre el Aggregate.

Debe mantenerse:

```text
Knowledge of Identifier

≠

Authorization
```

---

# Read Permissions

La autorización para consultar información Audit pertenece al Read
Side y a las políticas aplicables.

Debe mantenerse:

```text
Read Permission

≠

Write Permission
```

Este documento no establece que quien pueda ejecutar RecordAudit
tenga automáticamente permiso para consultar cualquier Read Model.

---

# Write Permissions

La capacidad de escritura versión 1.0 se limita conceptualmente a:

```text
RecordAudit
```

La autorización para dicha capacidad no implica autorización
ilimitada de lectura.

---

# CQRS

En un modelo CQRS:

```text
Write Authorization

↓

RecordAudit
```

permanece separada de:

```text
Read Authorization

↓

Audit Read Model
```

Cada lado puede aplicar políticas diferentes.

---

# Read Model no Concede Permission

La existencia de un Audit en una proyección no concede Permission
para modificar el Write Model.

Debe mantenerse:

```text
Read Model Visibility

≠

Write Authority
```

---

# Projection no Decide Write Authorization

Un Read Model puede contener información útil para evaluar políticas
en capas externas.

Sin embargo, la proyección no adquiere autoridad para modificar
Audit.

Debe mantenerse:

```text
Projection

≠

Aggregate Authorization Authority
```

---

# Event Sourcing

Si Audit utiliza Event Sourcing, la autorización aplica a nuevos
Commands.

La rehidratación de eventos históricos no constituye una nueva
operación autorizada.

Debe mantenerse:

```text
Event Replay

≠

Authorized Command
```

---

# Rehidratación

Rehidratar un Audit Recorded:

- no requiere reinterpretar el historial como nueva intención;
- no ejecuta RecordAudit;
- no concede Permissions;
- no produce AuditRecorded nuevamente.

La autorización se aplica a nuevas interacciones, no a la
reconstrucción interna del estado ya confirmado.

---

# Retry Técnico

Un retry técnico no crea automáticamente una nueva Permission.

Debe mantenerse:

```text
Technical Retry

≠

New Authorization Decision
```

La estrategia concreta para conservar o reevaluar autorización
pertenece a Application y Security.

Este documento no define dicha estrategia.

---

# Duplicate Delivery

La recepción duplicada de una intención o mensaje no debe utilizarse
para evitar Authorization.

Debe mantenerse:

```text
Duplicate Delivery

≠

Authorization Bypass
```

---

# Automation

La automatización de Audit no elimina la necesidad de que el proceso
que presenta una intención opere bajo una capacidad autorizada.

Debe mantenerse:

```text
Automated

≠

Unrestricted
```

---

# Internal Process

Un proceso interno tampoco posee autorización ilimitada por el solo
hecho de ejecutarse dentro de AURA.

Debe mantenerse:

```text
Internal

≠

Automatically Authorized for Everything
```

---

# Permission y Audit Histórico

La naturaleza histórica de Audit no concede derecho universal de
lectura o escritura.

Debe mantenerse:

```text
Historical Data

≠

Public Data
```

Las políticas de acceso a información histórica pertenecen al
modelo de autorización correspondiente.

---

# Permission y Datos Personales

La presencia de información relacionada con:

```text
ActorId
```

u otras referencias personales no implica derecho general de acceso
a dicha información.

La exposición debe respetar las políticas de lectura y minimización
correspondientes.

---

# Permission y Minimización

Authorization no justifica incorporar información innecesaria al
Aggregate.

Debe mantenerse:

```text
Authorized Access

≠

Unlimited Data Collection
```

La información auditada continúa sujeta a las reglas de
minimización del dominio.

---

# Permission y Retención

La autorización para acceder a Audit no crea políticas de:

- retención;
- eliminación;
- archivado;
- anonimización;
- redacción.

Dichas políticas requieren definición explícita.

---

# Permission y Eliminación

La versión 1.0 no define:

```text
DeleteAudit
```

Por lo tanto, no existe una Permission de dominio asociada a dicho
Command.

Debe mantenerse:

```text
No Command

↓

No Command Permission
```

dentro del modelo actual.

---

# Permission y Archivado

La versión 1.0 no define:

```text
ArchiveAudit
```

ni:

```text
Archived
```

como estado.

Por lo tanto, este documento no define Permission de archivado.

---

# Permission y Corrección

La versión 1.0 no define:

```text
CorrectAudit
```

ni:

```text
AuditCorrected
```

Por lo tanto, tampoco existe una Permission de corrección dentro de
este modelo.

---

# Permission y Retry de Dominio

La versión 1.0 no define:

```text
RetryAudit
```

como Command.

Por lo tanto, no existe una Permission de dominio para RetryAudit.

---

# Commands Técnicos

No deben crearse Permissions de dominio para operaciones técnicas
como:

```text
SaveAudit

LoadAudit

PersistAudit

SerializeAudit

PublishAuditMessage

SyncAuditToFIWARE
```

Estas operaciones pertenecen a otras capas.

---

# Domain Permission versus Infrastructure Permission

Debe mantenerse:

```text
Domain Permission

≠

Infrastructure Permission
```

Por ejemplo, tener acceso técnico a:

- una base de datos;
- un broker;
- una API;
- un filesystem;
- una plataforma FIWARE;

no equivale a autorización de dominio para ejecutar RecordAudit.

---

# Infrastructure Permission no Evita Aggregate Root

Ningún privilegio técnico debe utilizarse como vía válida de dominio
para modificar Audit fuera de:

```text
Audit Aggregate Root
```

Debe mantenerse:

```text
Technical Privilege

≠

Aggregate Bypass
```

---

# Audit Trail de Authorization

Las decisiones de autorización pueden ser objeto de trazabilidad
cuando corresponda.

Sin embargo:

```text
Authorization Decision

≠

Audit Aggregate State
```

por definición automática.

Cualquier hecho auditable relacionado con autorización deberá
ingresar mediante contratos y comportamiento explícitos.

---

# Audit no Audita Automáticamente toda Authorization

La existencia del Aggregate Audit no significa que cada decisión de
autorización deba producir automáticamente:

```text
RecordAudit
```

Debe existir una regla o contrato explícito que determine qué hechos
son auditables.

---

# Permission Denied y Audit

Una operación denegada no crea automáticamente una unidad Audit.

Debe mantenerse:

```text
AuthorizationDenied

≠

Automatic RecordAudit
```

Si una denegación debe ser auditable, dicha necesidad debe
establecerse mediante el contrato correspondiente.

---

# Permission Granted y Audit

Una autorización concedida tampoco constituye por sí sola:

```text
AuditRecorded
```

Primero debe existir una operación válida del Aggregate.

Debe mantenerse:

```text
AuthorizationGranted

≠

AuditRecorded
```

---

# Flujo Conceptual de Escritura

El flujo conceptual completo es:

```text
Actor / Process
      │
      ▼
Authentication
      │
      ▼
Authorization
      │
      ├── Denied
      │      │
      │      ▼
      │   Reject
      │
      └── Allowed
             │
             ▼
        RecordAudit
             │
             ▼
          Audit
             │
             ├── State Machine
             ├── Invariants
             ├── Versioning
             └── Consistency
                     │
                     ▼
                AuditRecorded
```

---

# Flujo Prohibido

No debe existir:

```text
Actor / Process

    │
    ▼

Direct Repository Mutation

    │
    ▼

Audit State Changed
```

como mecanismo válido de dominio.

Tampoco:

```text
Authorized

    │
    ▼

Direct setStatus()
```

---

# Cambios de Permission

Los cambios sobre políticas de autorización no modifican por sí
mismos:

- AuditId;
- AuditStatus;
- Version;
- CreatedAt;
- Source References;
- AuditRecorded histórico.

Debe mantenerse:

```text
Authorization Policy Change

≠

Audit State Change
```

---

# Evolución de Roles

La incorporación futura de nuevos Roles no debe modificar
automáticamente el Aggregate.

Debe mantenerse:

```text
New Role

≠

New Audit Behavior
```

Si un nuevo Role habilita un Command ya existente, dicha asignación
pertenece al modelo de Authorization.

---

# Nuevo Command

Si en una futura versión se incorpora un nuevo Command de Audit,
deberá definirse explícitamente la Permission correspondiente.

Debe revisarse, cuando corresponda:

```text
DOMAIN-012C-Commands.md

DOMAIN-012E-Invariants.md

DOMAIN-012F-Permissions.md

DOMAIN-012M-Test-Scenarios.md

DOMAIN-012O-Security-Model.md
```

No debe inferirse una Permission para un Command inexistente.

---

# Nueva Permission

Incorporar una nueva Permission no crea automáticamente:

- nuevo Command;
- nuevo estado;
- nueva transición;
- nuevo Domain Event;
- nueva Invariant.

Debe mantenerse:

```text
New Permission

≠

New Domain Behavior
```

---

# Reglas Fundamentales

Las Permissions de Audit deben cumplir:

1. Authentication permanece separada de Audit.
2. Authorization se resuelve antes de ejecutar comportamiento del
   Aggregate.
3. Domain Validation ocurre después de una autorización válida.
4. Permission no equivale a Domain Rule.
5. Authorized no significa automáticamente válido.
6. Se aplica Least Privilege.
7. Se aplica Deny by Default.
8. RecordAudit es el único Command oficial de escritura versión 1.0.
9. RecordAudit requiere un actor o proceso autorizado.
10. Una operación no autorizada no crea Audit.
11. Una operación no autorizada no produce AuditRecorded.
12. La versión 1.0 no define una taxonomía interna obligatoria de
    Roles.
13. Este documento no asigna RecordAudit a un Role concreto.
14. Un proceso automatizado no posee autorización ilimitada.
15. Un proceso interno no está automáticamente autorizado para toda
    capacidad.
16. Source Domain Event no constituye decisión de autorización.
17. ActorId no constituye Permission.
18. Source Actor y Command Requester no se consideran idénticos
    automáticamente.
19. Permission no equivale a ownership.
20. No existe ownership organizacional implícito definido por este
    documento.
21. Permission no permite modificar AuditId.
22. Permission no permite modificar State directamente.
23. Permission no permite modificar Version directamente.
24. Permission no permite modificar CreatedAt.
25. Permission no permite reescribir hechos históricos.
26. Audit Permission no concede autoridad sobre Source Aggregate.
27. Permissions de diferentes Aggregates permanecen independientes.
28. Permission no permite crear una transacción multi-Aggregate.
29. Permission no extiende Lifecycle.
30. Permission no extiende State Machine.
31. Recorded permanece terminal independientemente de privilegios.
32. Permission no permite evitar Invariants.
33. Permission no permite evitar Versioning.
34. Permission no permite evitar Optimistic Concurrency.
35. Repository no decide Authorization.
36. Acceso técnico al Repository no equivale a Permission.
37. Domain Events no contienen lógica de autorización.
38. Operaciones no autorizadas no producen Domain Events de éxito.
39. Domain Events no conceden Permissions.
40. Integration Events no conceden Permissions.
41. Sistemas externos no modifican Audit directamente.
42. FIWARE Authorization no equivale automáticamente a Audit
    Permission.
43. Permissions municipales no equivalen automáticamente a
    Permissions AURA.
44. Delegación permanece fuera del Aggregate.
45. RBAC puede utilizarse externamente sin introducir Roles internos
    obligatorios.
46. ABAC puede utilizarse externamente sin introducir atributos de
    autorización como estado obligatorio.
47. Claims no forman parte automáticamente del estado de Audit.
48. Tokens no son Domain Permissions.
49. Audit no almacena credenciales.
50. CorrelationId no representa Permission.
51. CausationId no representa Permission.
52. SourceEventId no representa Permission.
53. Conocer AuditId no concede Permission.
54. Read Permission permanece separada de Write Permission.
55. Read Models no conceden autoridad de escritura.
56. Projection no decide comportamiento del Aggregate.
57. Event Replay no constituye nueva operación autorizada.
58. Technical Retry no evita Authorization.
59. Duplicate Delivery no evita Authorization.
60. Datos históricos no son automáticamente públicos.
61. Authorization no justifica recopilación ilimitada de datos.
62. Permissions no crean políticas de retención.
63. No existe Permission para DeleteAudit porque el Command no
    existe.
64. No existe Permission para ArchiveAudit porque el Command no
    existe.
65. No existe Permission para CorrectAudit porque el Command no
    existe.
66. No existe Permission para RetryAudit porque el Command no
    existe.
67. Operaciones técnicas no requieren Domain Permissions como si
    fueran Commands.
68. Domain Permission y Infrastructure Permission permanecen
    separadas.
69. Privilegios técnicos no pueden evitar la Aggregate Root.
70. Una decisión de Authorization no se convierte automáticamente en
    Audit.
71. AuthorizationDenied no produce automáticamente RecordAudit.
72. AuthorizationGranted no equivale a AuditRecorded.
73. Cambios de Authorization Policy no modifican Audit.
74. Nuevos Roles no crean nuevo comportamiento.
75. Nuevos Commands requieren definición explícita de Permissions.
76. Nuevas Permissions no crean automáticamente comportamiento de
    dominio.

---

# Restricciones

No está permitido:

- ejecutar RecordAudit sin autorización aplicable;
- utilizar Authentication como sustituto de Authorization;
- utilizar Authorization como sustituto de Invariants;
- utilizar una Permission para evitar State Machine;
- utilizar una Permission para evitar Versioning;
- modificar AuditId por privilegio;
- modificar AuditStatus directamente;
- modificar Version directamente;
- modificar CreatedAt;
- reescribir el hecho auditado por privilegio;
- modificar otro Aggregate mediante una Permission de Audit;
- asumir que ActorId representa autorización;
- asumir que SourceEventId representa autorización;
- asumir que CorrelationId representa autorización;
- asumir que CausationId representa autorización;
- asumir que conocer AuditId concede acceso;
- asumir que un sistema interno tiene acceso ilimitado;
- asumir que un sistema externo autorizado puede modificar
  directamente Audit;
- incorporar credenciales dentro del Aggregate;
- crear Roles internos obligatorios sin definición explícita;
- crear Permissions para Commands inexistentes;
- utilizar acceso técnico a Infrastructure para evitar el dominio;
- convertir una denegación de acceso en Audit automáticamente;
- convertir una autorización concedida en AuditRecorded;
- permitir que Read Models modifiquen el Write Model.

---

# Compatibilidad Arquitectónica

El modelo de Permissions de Audit es compatible con:

- Domain-Driven Design;
- Aggregate Pattern;
- Clean Architecture;
- Hexagonal Architecture;
- SOLID;
- CQRS;
- Event-Driven Architecture;
- Event Sourcing Compatible;
- Optimistic Concurrency Control;
- Least Privilege;
- Deny by Default;
- RBAC;
- ABAC;
- Separation of Concerns;
- High Cohesion;
- Low Coupling.

Estas compatibilidades no obligan a utilizar una tecnología,
proveedor o protocolo concreto.

---

# Definición de Éxito

El modelo de Permissions del Aggregate **Audit** establece una
separación explícita entre identidad, autorización y reglas del
dominio.

La versión 1.0 reconoce:

```text
RecordAudit
```

como único Command oficial y establece que su ejecución requiere una
autorización aplicable antes de ingresar al comportamiento del
Aggregate.

El modelo garantiza que:

- Authentication permanece fuera de Audit;
- Authorization se resuelve antes del comportamiento de dominio;
- Permission no reemplaza Domain Validation;
- Authorized no significa automáticamente válido;
- Least Privilege y Deny by Default permanecen aplicables;
- RecordAudit requiere autorización;
- una operación no autorizada no crea Audit ni AuditRecorded;
- no existe una taxonomía interna obligatoria de Roles en versión
  1.0;
- este documento no asigna el Command a un Role concreto;
- actores humanos y procesos pueden participar conforme a políticas
  externas;
- ActorId no equivale a Permission;
- Source Domain Event no equivale a Authorization;
- Permission no concede ownership;
- Audit Permission no concede autoridad sobre otros Aggregates;
- Permissions no modifican Lifecycle ni State Machine;
- Recorded permanece terminal incluso ante capacidades elevadas;
- AuditId, Version y CreatedAt permanecen protegidos;
- Invariants no pueden ser evitadas mediante autorización;
- Optimistic Concurrency permanece obligatoria cuando corresponda;
- Repository no decide Permissions;
- Domain Events e Integration Events no conceden Permissions;
- sistemas externos no acceden directamente al Aggregate;
- FIWARE y sistemas municipales mantienen sus mecanismos de
  autorización fuera del dominio;
- RBAC y ABAC permanecen compatibles sin quedar impuestos;
- claims, tokens y credenciales permanecen fuera del estado de
  Audit;
- Read Permissions y Write Permissions pueden mantenerse separadas;
- Read Models no adquieren autoridad de escritura;
- retries, replay y duplicados técnicos no evitan Authorization;
- la naturaleza histórica de Audit no convierte sus datos en
  información universalmente accesible;
- no existen Permissions para Commands que no forman parte del
  modelo oficial;
- una nueva Permission no introduce automáticamente nuevo
  comportamiento;
- cualquier evolución futura requiere definición explícita y
  coordinada.

De esta forma, `DOMAIN-012F-Permissions.md` establece las
Permissions oficiales del Aggregate **Audit** conforme al patrón
consolidado de AURA Core.