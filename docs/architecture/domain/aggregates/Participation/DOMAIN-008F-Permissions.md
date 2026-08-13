# DOMAIN-008F — Participation Permissions

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
- DOMAIN-008G-Repository-Contract.md
- DOMAIN-008H-Examples.md
- DOMAIN-008I-Versioning.md
- DOMAIN-008J-Consistency-Boundary.md
- DOMAIN-008K-Integration-Events.md
- DOMAIN-008L-Read-Model.md
- DOMAIN-008M-Test-Scenarios.md
- DOMAIN-008N-Performance-Rules.md
- DOMAIN-008O-Security-Model.md
- DOMAIN-008P-Extension-Points.md
- DOMAIN-003-Aggregate.md
- DOMAIN-004-Aggregate.md
- CORE-004-Ubiquitous-Language.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Definir el modelo conceptual oficial de Permissions aplicable al
Aggregate **Participation**.

Este documento establece las reglas que determinan quién puede
intentar ejecutar operaciones sobre una Participation y cómo debe
mantenerse la separación entre:

```text
Authorization

Domain Behavior

Domain Invariants
```

Los Permissions determinan si un actor se encuentra autorizado
para solicitar una operación.

El Aggregate determina posteriormente si dicha operación es válida
de acuerdo con:

- su estado actual;
- su Lifecycle;
- su State Machine;
- sus Invariants;
- sus reglas de consistencia;
- las condiciones propias del dominio.

Por lo tanto:

```text
Permission Granted

≠

Operation Guaranteed
```

Un actor autorizado puede intentar ejecutar un Command que sea
rechazado posteriormente por el Aggregate.

---

# Propósito

El modelo de Permissions protege las operaciones sobre
Participation sin incorporar mecanismos técnicos de autorización
dentro del Aggregate.

Debe mantenerse:

```text
Actor

↓

Authorization Evaluation

↓

Permission Granted

↓

Command

↓

Participation Aggregate

↓

Domain Validation

↓

State Change
```

Cuando el actor no posee autorización:

```text
Actor

↓

Authorization Evaluation

↓

Permission Denied

↓

Command Not Executed
```

Cuando posee autorización pero la operación viola el dominio:

```text
Actor

↓

Authorization Evaluation

↓

Permission Granted

↓

Command

↓

Participation Aggregate

↓

Invariant or State Violation

↓

Rejected
```

---

# Principios

Los Permissions de Participation siguen los siguientes principios:

- autorización y dominio permanecen separados;
- los Permissions determinan quién puede intentar una operación;
- las Invariants determinan si la operación produce un estado
  válido;
- los Permissions no forman parte de la identidad de
  Participation;
- los Permissions no forman parte del Lifecycle;
- los Permissions no modifican ParticipationStatus;
- los Permissions no sustituyen la State Machine;
- los Permissions no sustituyen las Invariants;
- los Permissions no dependen de mecanismos específicos de
  autenticación;
- el Aggregate no almacena credenciales;
- el Aggregate no almacena tokens;
- el Aggregate no administra sesiones;
- las decisiones de autorización deben ser auditables cuando
  corresponda;
- una autorización válida no permite evitar las reglas del
  dominio;
- una operación administrativa continúa sometida a las
  Invariants.

---

# Separación Fundamental

Debe mantenerse estrictamente:

```text
Authentication

≠

Authorization

≠

Domain Validation
```

Authentication determina:

```text
Who is the actor?
```

Authorization determina:

```text
May this actor attempt this operation?
```

Participation determina:

```text
Is this operation valid for the current domain state?
```

Estas responsabilidades no deben mezclarse.

---

# Authentication

Participation no autentica actores.

El Aggregate no conoce:

```text
Password

Token

JWT

OAuth

Session

API Key

Private Key

Authentication Provider
```

La autenticación ocurre fuera del Aggregate.

Participation recibe una intención cuya identidad de actor ya ha
sido establecida por las capas correspondientes.

---

# Authorization

Authorization determina si un actor puede intentar ejecutar un
Command sobre Participation.

Conceptualmente:

```text
Actor

+

Organization Context

+

Membership Context

+

Role Context

+

Requested Action

↓

Authorization Decision
```

La forma técnica mediante la cual se resuelve esta decisión no
forma parte del Aggregate Participation.

---

# Domain Validation

Una vez autorizada la intención, Participation protege sus propias
reglas.

Conceptualmente:

```text
Authorized Command

↓

Participation

↓

Current State

+

Lifecycle

+

State Machine

+

Invariants

↓

Accept or Reject
```

Authorization no puede modificar estas reglas.

---

# Actor

Toda operación protegida debe asociarse conceptualmente a un actor
identificable.

La referencia conceptual puede expresarse mediante:

```text
ActorId
```

ActorId representa la identidad del actor que intenta ejecutar la
operación.

ActorId:

- permite trazabilidad;
- permite evaluación de autorización;
- no forma parte de ParticipationId;
- no modifica OrganizationId;
- no convierte al actor en entidad interna de Participation;
- no representa una credencial;
- no representa una sesión.

---

# Actor y Citizen

Cuando el actor corresponda a un Citizen, la relación se mantiene
mediante identidad.

Conceptualmente:

```text
ActorId

↓

CitizenId
```

Participation no incorpora Citizen dentro de su límite de
consistencia.

La existencia de CitizenId no implica automáticamente autorización.

---

# Actor y Membership

La autorización organizacional puede utilizar Membership como
contexto.

Conceptualmente:

```text
Actor

↓

MembershipId

↓

Organization Context
```

Membership representa la pertenencia del actor a una
Organization.

Participation no modifica Membership.

Participation no determina el Lifecycle de Membership.

Participation no activa ni suspende Memberships.

---

# Actor y Role

Los Roles organizacionales pueden participar en la evaluación de
Permissions.

Conceptualmente:

```text
Membership

↓

RoleId

↓

Authorization Rule
```

Role representa una función organizacional.

Participation no incorpora Role como entidad interna.

Participation no modifica Role.

Participation no asigna Roles.

Participation no elimina Roles.

---

# Contexto Organizacional

Toda autorización sobre Participation debe respetar su:

```text
OrganizationId
```

La autorización debe impedir que un actor utilice permisos
pertenecientes a una Organization para operar sobre una
Participation perteneciente a otra Organization cuando las reglas
del sistema no lo permitan.

Debe mantenerse conceptualmente:

```text
Actor Organization Context

↓

Authorization Evaluation

↓

Participation.OrganizationId
```

---

# Aislamiento Organizacional

El modelo debe proteger el aislamiento entre Organizations.

No debe permitirse:

```text
Actor authorized in Organization A

↓

Modify Participation in Organization B
```

salvo que exista una capacidad explícita del sistema que autorice
dicha operación.

La existencia de una capacidad administrativa superior no modifica
OrganizationId de Participation ni elimina sus Invariants.

---

# Permission

Un Permission representa conceptualmente la autorización para
intentar una acción determinada.

Los Permissions no representan comportamiento del Aggregate.

Ejemplos conceptuales:

```text
Participation.Register

Participation.Activate

Participation.Complete

Participation.Withdraw

Participation.Invalidate

Participation.Archive

Participation.ChangeType

Participation.ChangeContext

Participation.UpdateMetadata

Participation.Read
```

Estos nombres expresan capacidades conceptuales.

La representación técnica concreta pertenece al modelo de
autorización correspondiente.

---

# Granularidad

Los Permissions deben mantener granularidad suficiente para evitar
autorizaciones excesivamente amplias.

No debe asumirse:

```text
CanManageParticipation

=

CanPerformEveryParticipationOperation
```

cuando el dominio o la autorización requieran distinguir
operaciones.

Debe poder diferenciarse conceptualmente entre:

```text
Register

Activate

Complete

Withdraw

Invalidate

Archive

ChangeType

ChangeContext

UpdateMetadata

Read
```

---

# Permission para RegisterParticipation

El Command:

```text
RegisterParticipation
```

requiere autorización para registrar una Participation dentro del
contexto organizacional correspondiente.

Permission conceptual:

```text
Participation.Register
```

La autorización no garantiza la creación.

Después de autorizarse deben validarse:

- identidad;
- OrganizationId;
- ParticipationType;
- contexto requerido;
- referencias requeridas;
- estado inicial;
- Invariants de creación.

---

# Permission para ActivateParticipation

El Command:

```text
ActivateParticipation
```

requiere:

```text
Participation.Activate
```

La autorización permite intentar la activación.

Participation continúa exigiendo:

```text
CurrentStatus = Registered
```

y todas las demás condiciones definidas por el dominio.

---

# Permission para CompleteParticipation

El Command:

```text
CompleteParticipation
```

requiere:

```text
Participation.Complete
```

La autorización no permite completar una Participation desde un
estado inválido.

Debe mantenerse:

```text
Permission Granted

+

CurrentStatus = Active

+

Completion Invariants

=

Valid Completion
```

---

# Permission para WithdrawParticipation

El Command:

```text
WithdrawParticipation
```

requiere:

```text
Participation.Withdraw
```

La autorización debe evaluarse según el actor y el contexto de la
Participation.

El Aggregate determina posteriormente si Withdrawal es válido
desde el estado actual.

---

# Retiro por el Participante

Cuando las reglas de autorización permitan que el propio
participante solicite su retiro, debe poder distinguirse
conceptualmente esta capacidad de una operación administrativa.

Debe mantenerse:

```text
Self Withdrawal

≠

Administrative Invalidation
```

Withdrawal expresa retiro de la Participation según las reglas
establecidas.

Invalidation representa un concepto diferente del Lifecycle.

---

# Permission para InvalidateParticipation

El Command:

```text
InvalidateParticipation
```

requiere:

```text
Participation.Invalidate
```

Invalidation constituye una operación distinta de Withdrawal.

La autorización para retirar una Participation no implica
automáticamente autorización para invalidarla.

Debe mantenerse:

```text
Participation.Withdraw

≠

Participation.Invalidate
```

---

# Permission para ArchiveParticipation

El Command:

```text
ArchiveParticipation
```

requiere:

```text
Participation.Archive
```

La autorización no permite archivar desde cualquier estado.

El Aggregate continúa exigiendo que el estado actual pertenezca al
conjunto permitido:

```text
Completed

Withdrawn

Invalidated
```

---

# Permission para ChangeParticipationType

El Command:

```text
ChangeParticipationType
```

requiere:

```text
Participation.ChangeType
```

La autorización permite intentar modificar la clasificación.

No permite:

- modificar ParticipationId;
- modificar OrganizationId;
- modificar Status directamente;
- modificar Version directamente;
- evitar las reglas de estado;
- utilizar un ParticipationType inválido.

---

# Permission para ChangeParticipationContext

El Command:

```text
ChangeParticipationContext
```

requiere:

```text
Participation.ChangeContext
```

Esta capacidad puede permitir modificar referencias contextuales
cuando el estado y las Invariants lo permitan.

No autoriza modificar:

```text
OrganizationId
```

ni permite modificar los Aggregates referenciados.

---

# Permission para UpdateParticipationMetadata

El Command:

```text
UpdateParticipationMetadata
```

requiere:

```text
Participation.UpdateMetadata
```

La autorización no permite utilizar Metadata como mecanismo para
evitar las restricciones sobre atributos protegidos.

No puede utilizarse para modificar directamente:

```text
ParticipationId

OrganizationId

ParticipationStatus

Version

Lifecycle Timestamps
```

---

# Permission de Lectura

Las consultas pueden requerir:

```text
Participation.Read
```

La autorización de lectura pertenece al lado correspondiente de la
aplicación y de los Read Models.

El Aggregate no modifica su estado para autorizar una consulta.

Debe mantenerse:

```text
Read Permission

↓

Read Model / Query
```

y no:

```text
Read Permission

↓

Aggregate Mutation
```

---

# Permissions y Commands

Cada Command protegido debe asociarse con una capacidad de
autorización correspondiente.

Matriz conceptual:

```text
Command                         Permission

RegisterParticipation           Participation.Register

ActivateParticipation           Participation.Activate

CompleteParticipation           Participation.Complete

WithdrawParticipation           Participation.Withdraw

InvalidateParticipation         Participation.Invalidate

ArchiveParticipation            Participation.Archive

ChangeParticipationType         Participation.ChangeType

ChangeParticipationContext      Participation.ChangeContext

UpdateParticipationMetadata     Participation.UpdateMetadata
```

La matriz establece correspondencia conceptual.

No reemplaza las validaciones del Aggregate.

---

# Permissions y Lifecycle

Los Permissions no modifican las transiciones oficiales.

Debe mantenerse:

```text
Permission

↓

May Attempt Transition
```

y:

```text
State Machine

↓

Determines Whether Transition Exists
```

Ejemplo:

```text
Actor has Participation.Complete

CurrentStatus = Registered
```

Resultado:

```text
CompleteParticipation

↓

Rejected
```

porque:

```text
Registered → Completed
```

no constituye una transición válida.

---

# Permissions y State Machine

La State Machine mantiene autoridad sobre las transiciones.

Authorization no puede crear transiciones adicionales.

No debe existir:

```text
Administrative Permission

↓

Bypass State Machine
```

Una operación administrativa sigue siendo una operación de
dominio.

---

# Permissions e Invariants

Las Invariants permanecen obligatorias para todos los actores.

Debe mantenerse:

```text
Permission Granted

↓

Invariant Validation Required
```

No existe un actor que pueda producir válidamente un estado
internamente inconsistente.

---

# Permisos Administrativos

Los actores administrativos pueden poseer capacidades diferentes
de los participantes ordinarios.

Sin embargo:

```text
Administrative Capability

≠

Invariant Bypass
```

Un administrador autorizado puede ejecutar determinadas
operaciones adicionales, pero siempre mediante Commands y
comportamientos reconocidos por el dominio.

---

# Operaciones Privilegiadas

Operaciones como:

```text
InvalidateParticipation

ArchiveParticipation

ChangeParticipationContext
```

pueden requerir capacidades de autorización más restrictivas que
operaciones ordinarias.

La política concreta debe mantenerse fuera del Aggregate.

Participation únicamente recibe una intención autorizada y protege
sus propias reglas.

---

# Roles Organizacionales

Los Roles pueden utilizarse para otorgar capacidades.

Ejemplos de Roles organizacionales existentes en AURA pueden
incluir:

```text
President

Secretary

Coordinator

Moderator

Member
```

La asociación concreta:

```text
Role

↓

Permission
```

pertenece al modelo de autorización.

Participation no mantiene internamente una tabla de Roles
autorizados.

---

# No Acoplamiento Role-Permission dentro de Participation

No debe existir dentro del Aggregate una regla técnica como:

```text
if role == "President":
    allow()
```

Participation no conoce la representación técnica de Roles ni
Permissions.

La autorización debe resolverse antes de ejecutar el comportamiento
del Aggregate.

---

# Membership como Contexto de Autorización

Membership puede proporcionar el contexto organizacional necesario
para evaluar la capacidad del actor.

Conceptualmente:

```text
Citizen

↓

Membership

↓

Role

↓

Permission

↓

Participation Command
```

Esta secuencia no significa que Participation contenga:

```text
Citizen

Membership

Role
```

como entidades internas.

---

# Estado de Membership

Cuando la política de autorización requiera una Membership válida,
la evaluación correspondiente debe realizarse fuera del Aggregate
Participation.

Participation no carga Membership para modificarla.

Debe mantenerse:

```text
Authorization Context

↓

Membership Information

↓

Permission Decision
```

No:

```text
Participation

↓

Mutable Membership
```

---

# Participation Ownership

Cuando el modelo de autorización reconozca una relación entre el
actor y la Participation, dicha relación puede utilizarse para
evaluar capacidades específicas.

Ejemplo conceptual:

```text
Actor

=

Participation Participant
```

puede ser relevante para determinar si el actor puede solicitar:

```text
WithdrawParticipation
```

La evaluación de autorización no modifica la identidad ni el
Lifecycle del Aggregate.

---

# Self-Service Permissions

Las operaciones de autoservicio deben limitarse a las capacidades
explícitamente autorizadas.

Conceptualmente puede existir:

```text
Participant

↓

Own Participation

↓

Allowed Self-Service Operation
```

No debe inferirse que ser el participante autoriza automáticamente:

```text
CompleteParticipation

InvalidateParticipation

ArchiveParticipation
```

La autorización debe mantenerse explícita.

---

# Cross-Organization Permissions

Las operaciones entre Organizations deben considerarse
privilegiadas cuando el modelo de autorización las permita.

Debe mantenerse:

```text
Default

=

Organization Boundary Preserved
```

Una capacidad transversal debe ser explícita.

No debe derivarse automáticamente de un Role organizacional local.

---

# System Actors

Procesos internos del sistema pueden actuar como actores cuando
ejecutan operaciones sobre Participation.

Conceptualmente:

```text
System Actor

↓

Authorization

↓

Command
```

Un proceso automático no queda exento de:

- Permissions;
- State Machine;
- Invariants;
- Versioning;
- Consistency Boundary.

---

# Integration Actors

Una integración externa no recibe autoridad implícita sobre
Participation.

Debe mantenerse:

```text
External Integration

↓

Authenticated Identity

↓

Authorized Capability

↓

Command
```

cuando la integración solicite modificaciones.

La existencia de una Integration no implica:

```text
Full Participation Access
```

---

# Event Consumers

Un consumidor de eventos que posteriormente origine un Command
debe encontrarse sujeto al modelo de autorización definido para
dicha operación.

El hecho de reaccionar a un Domain Event no autoriza
automáticamente cualquier modificación posterior.

---

# Permissions y Domain Events

Los Domain Events representan hechos consumados.

No requieren Permission para existir después de una modificación
válida.

Debe mantenerse:

```text
Authorized Command

↓

Valid Domain Change

↓

Domain Event
```

No:

```text
Domain Event

↓

Authorization Decision
```

El evento describe lo que ocurrió.

---

# Permissions e Integration Events

Los Integration Events no constituyen mecanismos de autorización.

Un consumidor externo no obtiene Permission sobre Participation
por haber recibido un Integration Event.

Debe mantenerse:

```text
Integration Event Visibility

≠

Mutation Authorization
```

---

# Permissions y Repository

El Repository no decide Permissions.

Debe mantenerse:

```text
Authorization

↓

Application / Authorization Capability
```

```text
Repository

↓

Persistence Contract
```

El Repository no debe convertirse en un mecanismo para evitar la
autorización mediante operaciones directas de actualización.

---

# Protección contra Modificación Directa

Una operación no debe evitar Permissions mediante acceso directo a
persistencia.

No debe existir como flujo autorizado:

```text
Actor

↓

Database Update

↓

Participation Modified
```

Debe mantenerse:

```text
Actor

↓

Authorization

↓

Command

↓

Participation Aggregate

↓

Repository
```

---

# Permissions y Read Models

Los Read Models pueden aplicar políticas de acceso diferentes según
el consumidor.

Conceptualmente pueden existir vistas:

```text
Public Participation View

Member Participation View

Administrative Participation View
```

La existencia concreta de estas vistas se define en el modelo de
lectura correspondiente.

El acceso a un Read Model no concede autorización para modificar el
Aggregate.

---

# Separación Read / Write

Debe mantenerse:

```text
Read Authorization

≠

Write Authorization
```

Poseer:

```text
Participation.Read
```

no implica poseer:

```text
Participation.ChangeContext
```

ni cualquier otro Permission de modificación.

---

# Datos Sensibles

La autorización de lectura debe considerar la naturaleza de los
datos proyectados.

No todos los consumidores deben recibir necesariamente la misma
información.

La protección de datos en Read Models puede requerir:

- filtrado;
- minimización;
- anonimización;
- exclusión de atributos;
- proyecciones especializadas.

Estas medidas no modifican el Aggregate.

---

# Permission Evaluation

Una evaluación conceptual puede considerar:

```text
ActorId

OrganizationId

MembershipId

RoleId

RequestedPermission

ResourceId

ResourceOrganizationId
```

La información concreta requerida depende de la política de
autorización.

No todos estos elementos deben formar parte del estado interno de
Participation.

---

# Resultado de Authorization

La evaluación debe producir conceptualmente:

```text
Granted
```

o:

```text
Denied
```

La decisión no modifica por sí misma Participation.

---

# Permission Denied

Cuando la autorización es rechazada:

```text
Permission = Denied
```

el Command no debe ejecutarse sobre el Aggregate.

Debe mantenerse:

```text
No Domain State Change

No Version Increment

No Success Domain Event
```

---

# Permission Granted

Cuando:

```text
Permission = Granted
```

el actor puede intentar la operación.

Debe continuar:

```text
Command

↓

Participation

↓

State Validation

↓

Invariant Validation

↓

Accept or Reject
```

---

# Permission Denial y Domain Event

Una denegación de autorización ocurre antes de ejecutar el
comportamiento protegido del Aggregate.

Por lo tanto, una denegación no debe producir un Domain Event que
represente falsamente la operación solicitada.

Ejemplo:

```text
Participation.Complete = Denied
```

no produce:

```text
ParticipationCompleted
```

---

# Permission Denial y Version

Una operación que no supera autorización no modifica:

```text
Version
```

Debe mantenerse:

```text
Version Before = N

↓

Permission Denied

↓

Version After = N
```

---

# Permission Denial y Timestamps

Una operación denegada tampoco modifica timestamps del Lifecycle.

Ejemplo:

```text
ActivateParticipation

↓

Permission Denied
```

no establece:

```text
StartedAt
```

---

# Auditoría de Autorización

Las decisiones de autorización pueden formar parte de la
trazabilidad operacional.

Conceptualmente pueden registrarse:

```text
ActorId

RequestedPermission

ResourceId

OrganizationId

Decision

Timestamp

CorrelationId
```

Esta información no forma parte necesariamente del estado interno
de Participation.

Audit mantiene su propio límite de consistencia.

---

# ActorId en Commands

Los Commands pueden transportar:

```text
ActorId
```

para permitir trazabilidad y contexto de ejecución.

ActorId no representa que Participation sea responsable de
autorizar al actor.

Debe mantenerse:

```text
Command Actor Context

≠

Aggregate Authorization Engine
```

---

# CorrelationId

Las operaciones autorizadas pueden transportar:

```text
CorrelationId
```

para correlacionar una intención con eventos y procesos
posteriores.

CorrelationId no determina autorización.

---

# CausationId

Cuando corresponda, una operación puede transportar:

```text
CausationId
```

para establecer causalidad.

CausationId tampoco representa un Permission.

---

# Least Privilege

El modelo de autorización debe seguir conceptualmente el principio:

```text
Least Privilege
```

Un actor debe disponer únicamente de las capacidades necesarias
para ejecutar sus responsabilidades.

No debe otorgarse acceso total a Participation cuando solo se
requiere una operación específica.

---

# Deny by Default

Cuando no exista una autorización reconocida para una operación
protegida, debe aplicarse conceptualmente:

```text
Deny by Default
```

La ausencia de una prohibición explícita no equivale a permiso.

---

# Explicit Permission

Una operación protegida requiere una capacidad explícitamente
reconocida.

Debe mantenerse:

```text
No Permission

↓

No Protected Command Execution
```

---

# Separation of Duties

El modelo puede aplicar separación de responsabilidades cuando las
políticas organizacionales así lo requieran.

Conceptualmente:

```text
Actor A

↓

Register Participation
```

```text
Actor B

↓

Invalidate Participation
```

cuando una política establezca que ambas capacidades no deben
concentrarse.

La política concreta pertenece al modelo de autorización y no al
estado interno de Participation.

---

# Permission Escalation

No está permitido que una operación sobre Participation otorgue al
actor nuevas capacidades de autorización como efecto implícito.

Debe mantenerse:

```text
Participation State Change

≠

Permission Grant
```

La gestión de Permissions pertenece al contexto de autorización.

---

# Role Escalation

Participation tampoco puede modificar Role para obtener una
capacidad superior.

No debe existir:

```text
Participation Command

↓

Change Actor Role

↓

Retry Participation Command
```

como comportamiento interno del Aggregate.

---

# Permission Revocation

La revocación de una capacidad pertenece al modelo de
autorización.

Participation no mantiene una copia mutable de Permissions que
deba sincronizarse con Role o Membership.

Esto evita que el Aggregate posea autorizaciones obsoletas como
parte de su estado.

---

# Temporalidad de Authorization

La autorización debe evaluarse para la intención correspondiente.

Una autorización obtenida en un momento anterior no debe asumirse
indefinidamente válida si las condiciones de autorización han
cambiado.

Esta regla pertenece al proceso de autorización.

No implica almacenar sesiones o permisos temporales dentro de
Participation.

---

# Optimistic Concurrency y Permissions

La autorización no elimina las reglas de concurrencia.

Un actor autorizado puede intentar modificar una versión obsoleta.

Debe mantenerse:

```text
Permission Granted

↓

ExpectedVersion Validation

↓

Accept or Concurrency Conflict
```

La especificación de Versioning corresponde a:

```text
DOMAIN-008I-Versioning.md
```

---

# Permissions y Consistency Boundary

Authorization no amplía el límite de consistencia.

Aunque una operación requiera información de:

```text
Citizen

Membership

Role

Organization
```

Participation continúa siendo un Aggregate independiente.

Debe mantenerse:

```text
Authorization Context

≠

Aggregate Ownership
```

---

# No Transacciones Distribuidas por Authorization

La evaluación de Permissions no convierte múltiples Aggregates en
una única transacción de dominio.

No debe utilizarse:

```text
Participation

+

Membership

+

Role

+

Organization
```

como un Aggregate artificial únicamente para resolver
autorización.

---

# Permissions y Event Sourcing

Cuando Event Sourcing sea utilizado, la autorización se evalúa
sobre nuevas intenciones.

Los eventos históricos no vuelven a solicitar autorización durante
la rehidratación.

Debe mantenerse:

```text
Historical Event Replay

≠

New Authorized Command
```

---

# Rehidratación

Durante la rehidratación:

- no se evalúan Permissions nuevamente;
- no se autentican actores históricos;
- no se ejecutan Commands;
- no se generan nuevos eventos;
- no se modifican versiones;
- no se alteran decisiones históricas.

Los eventos representan hechos ya aceptados.

---

# Permissions y CQRS

En CQRS pueden existir políticas diferentes para:

```text
Command Side

Query Side
```

Debe mantenerse:

```text
Write Permission

↓

Command
```

y:

```text
Read Permission

↓

Query
```

La autorización de una consulta no implica autorización de
escritura.

---

# Permissions y Clean Architecture

El Aggregate no depende de una implementación concreta de
Authorization.

Participation no conoce:

```text
Keyrock

OAuth2

JWT

HTTP Headers

Framework Middleware

Database ACL

Identity Provider
```

Las capas externas resuelven autenticación y autorización antes de
invocar el comportamiento correspondiente.

---

# Permissions y Hexagonal Architecture

La autorización puede implementarse mediante capacidades externas
conectadas a través de Ports y Adapters.

El dominio permanece independiente de dichas implementaciones.

Conceptualmente:

```text
External Authorization Mechanism

↓

Application Boundary

↓

Authorized Command

↓

Participation
```

---

# Permissions y FIWARE

La eventual integración de AURA con mecanismos de identidad o
autorización del ecosistema FIWARE no modifica el modelo conceptual
de Participation.

Participation no depende directamente de:

```text
Keyrock

Wilma PEP Proxy

OAuth2

JWT
```

Estos componentes pueden implementar capacidades de seguridad en
Infrastructure.

No forman parte del Aggregate.

---

# Permissions y APIs

Una API puede verificar autorización antes de ejecutar un Command.

Sin embargo:

```text
API Authorization

≠

Domain Validation
```

El Aggregate continúa protegiendo Lifecycle, State Machine e
Invariants.

---

# Permissions y UI

La interfaz puede ocultar acciones que el actor no posee.

Ejemplo:

```text
Participation.Invalidate = Denied
```

puede provocar que la UI no muestre la acción correspondiente.

Sin embargo:

```text
Hidden Button

≠

Authorization Enforcement
```

La autorización debe aplicarse independientemente de la interfaz.

---

# Protección contra Bypass

Todos los puntos de entrada capaces de originar modificaciones
deben respetar el modelo de autorización.

Esto incluye:

- APIs;
- interfaces administrativas;
- procesos internos;
- workers;
- jobs;
- integraciones;
- consumidores de eventos;
- importaciones;
- operaciones masivas.

No debe existir un canal técnico alternativo que permita modificar
Participation evitando Permissions.

---

# Bulk Operations

Las operaciones masivas deben evaluar autorización de acuerdo con
los recursos afectados.

Una autorización sobre una Participation no debe inferirse
automáticamente para todas las demás.

Conceptualmente:

```text
Bulk Command

↓

Participation A Authorization

Participation B Authorization

Participation C Authorization
```

según la política correspondiente.

Cada Participation mantiene su propio límite de consistencia.

---

# Importaciones

Una importación no constituye una excepción automática al modelo
de Permissions.

Debe mantenerse:

```text
Import

↓

Authorized Operation

↓

Domain Validation
```

No:

```text
Import

↓

Bypass Authorization

↓

Direct Persistence
```

---

# Procesos Automáticos

Los procesos automáticos deben operar bajo una identidad y
capacidad reconocibles cuando ejecuten Commands protegidos.

No debe asumirse:

```text
System Process

=

Unlimited Permission
```

---

# Superuser

La existencia técnica de una capacidad administrativa global, si
la arquitectura de autorización la contempla, no elimina las
Invariants.

Debe mantenerse:

```text
Global Authorization

≠

Domain Rule Bypass
```

Un actor con autoridad amplia continúa sujeto a:

- State Machine;
- Lifecycle;
- Invariants;
- Versioning;
- Consistency Boundary.

---

# Emergency Access

Si en el futuro se define una capacidad excepcional de acceso, esta
debe permanecer explícita, trazable y separada de las reglas
ordinarias.

No debe implementarse como modificación silenciosa del Aggregate.

La existencia de una capacidad excepcional no autoriza estados
inválidos.

---

# Permission Matrix

Matriz conceptual de capacidades:

```text
Operation                       Required Permission

Register Participation          Participation.Register

Activate Participation          Participation.Activate

Complete Participation          Participation.Complete

Withdraw Participation          Participation.Withdraw

Invalidate Participation        Participation.Invalidate

Archive Participation           Participation.Archive

Change Participation Type       Participation.ChangeType

Change Participation Context    Participation.ChangeContext

Update Participation Metadata   Participation.UpdateMetadata

Read Participation              Participation.Read
```

---

# Matriz Permission / Dominio

```text
Permission                      Domain Validation Still Required

Participation.Register          Yes

Participation.Activate          Yes

Participation.Complete          Yes

Participation.Withdraw          Yes

Participation.Invalidate        Yes

Participation.Archive           Yes

Participation.ChangeType        Yes

Participation.ChangeContext     Yes

Participation.UpdateMetadata    Yes
```

No existe un Permission de modificación que permita omitir la
validación del Aggregate.

---

# Matriz de Responsabilidades

```text
Responsibility                  Authority

Actor Authentication            Authentication Layer

Permission Evaluation           Authorization Capability

Organization Access             Authorization Capability

Membership Evaluation           Authorization Capability

Role Evaluation                 Authorization Capability

Command Dispatch                Application Layer

Lifecycle Validation            Participation Aggregate

State Transition Validation     Participation Aggregate

Invariant Protection            Participation Aggregate

Version Evolution               Participation Aggregate

Concurrency Persistence         Repository Contract

Read Authorization              Application / Read Side

Audit Persistence               Audit Context
```

---

# Matriz de Separación

```text
Concept                         Belongs to Participation State

ParticipationId                 Yes

OrganizationId                  Yes

ParticipationType               Yes

ParticipationStatus             Yes

Lifecycle Timestamps            Yes

Version                         Yes

Password                        No

JWT                             No

OAuth Token                     No

Session                         No

Role Definition                 No

Membership Aggregate            No

Permission Assignment           No

Authentication Provider         No

Authorization Policy Engine     No
```

---

# Escenarios de Autorización

## Registro autorizado

```text
Actor

↓

Participation.Register = Granted

↓

RegisterParticipation

↓

Domain Validation

↓

ParticipationRegistered
```

---

## Registro no autorizado

```text
Actor

↓

Participation.Register = Denied

↓

No Command Execution

↓

No State Change
```

---

## Activación autorizada y válida

```text
Actor

↓

Participation.Activate = Granted

↓

Status = Registered

↓

ActivateParticipation

↓

ParticipationActivated
```

---

## Activación autorizada pero inválida

```text
Actor

↓

Participation.Activate = Granted

↓

Status = Completed

↓

ActivateParticipation

↓

Rejected
```

La autorización no crea:

```text
Completed → Active
```

---

## Completion no autorizada

```text
Actor

↓

Participation.Complete = Denied

↓

No Aggregate Mutation

↓

No ParticipationCompleted
```

---

## Invalidation autorizada

```text
Authorized Administrative Actor

↓

Participation.Invalidate = Granted

↓

InvalidateParticipation

↓

Domain Validation

↓

ParticipationInvalidated
```

---

## Invalidation no autorizada

```text
Actor

↓

Participation.Invalidate = Denied

↓

No Command Execution
```

---

## Acceso entre Organizations denegado

```text
Actor Context = Organization A

Participation.OrganizationId = Organization B

No Cross-Organization Capability

↓

Denied
```

---

## Operación con versión obsoleta

```text
Permission Granted

↓

ExpectedVersion = 5

CurrentVersion = 6

↓

Concurrency Conflict
```

El Permission válido no evita el conflicto de concurrencia.

---

# Rechazo de Authorization

Una operación debe ser rechazada antes de ejecutar el
comportamiento protegido cuando:

- el actor no se encuentra autenticado cuando la operación lo
  requiere;
- el actor no posee el Permission correspondiente;
- el actor no pertenece al contexto organizacional requerido;
- la Membership requerida no satisface la política de
  autorización;
- el Role no concede la capacidad requerida;
- la operación intenta acceder a otra Organization sin capacidad
  explícita;
- la política de autorización aplicable produce Denied.

---

# Resultado de Rechazo

Cuando Authorization rechaza una operación:

```text
Participation State

=

Unchanged
```

También debe mantenerse:

```text
Version

=

Unchanged
```

y no debe emitirse el Domain Event de éxito correspondiente.

---

# Reglas No Negociables

Las siguientes reglas son fundamentales:

```text
Authentication

≠

Authorization
```

```text
Authorization

≠

Domain Validation
```

```text
Permission Granted

≠

Command Success
```

```text
Administrative Permission

≠

Invariant Bypass
```

```text
Read Permission

≠

Write Permission
```

```text
Organization Permission

≠

Cross-Organization Permission
```

```text
Role

≠

Participation State
```

```text
Membership

≠

Participation State
```

```text
Authorization Context

≠

Aggregate Boundary
```

```text
System Actor

≠

Unlimited Authority
```

---

# Restricciones

No está permitido:

- autenticar actores dentro de Participation;
- almacenar contraseñas en Participation;
- almacenar JWT en Participation;
- almacenar OAuth tokens en Participation;
- almacenar sesiones en Participation;
- almacenar credenciales en Participation;
- incorporar Membership como entidad interna;
- incorporar Role como entidad interna;
- modificar Membership desde Participation;
- modificar Role desde Participation;
- modificar Permissions desde Participation;
- utilizar un Role como sustituto directo de una Invariant;
- utilizar Authorization para evitar la State Machine;
- utilizar Authorization para evitar el Lifecycle;
- utilizar Authorization para evitar Invariants;
- considerar una capacidad administrativa como acceso ilimitado al
  estado interno;
- permitir modificaciones directas de persistencia para evitar
  Permissions;
- considerar acceso de lectura como autorización de escritura;
- considerar pertenencia organizacional como autorización
  automática para cualquier operación;
- conceder acceso entre Organizations por inferencia;
- considerar una Integration como actor automáticamente
  privilegiado;
- considerar un proceso automático como actor ilimitado;
- utilizar eventos como mecanismos de autorización;
- utilizar Read Models para conceder permisos de modificación;
- modificar Version ante una denegación;
- modificar timestamps ante una denegación;
- emitir eventos de éxito ante una denegación;
- ampliar el límite de consistencia para resolver Authorization.

---

# Testabilidad

El modelo de Permissions debe permitir verificar escenarios
deterministas como:

```text
Authorized Registration

Unauthorized Registration

Authorized Activation

Unauthorized Activation

Authorized but Invalid Activation

Authorized Completion

Unauthorized Completion

Authorized Withdrawal

Unauthorized Withdrawal

Authorized Invalidation

Unauthorized Invalidation

Authorized Archive

Unauthorized Archive

Authorized Type Change

Unauthorized Type Change

Authorized Context Change

Unauthorized Context Change

Authorized Metadata Update

Unauthorized Metadata Update

Authorized Read

Unauthorized Read

Same Organization Access

Cross-Organization Access Denied

Explicit Cross-Organization Access

Permission Granted but Invariant Violated

Permission Granted but Version Conflict

Permission Denied without Version Change

Permission Denied without Domain Event

Permission Denied without Timestamp Change

System Actor Authorization

Integration Actor Authorization
```

Los escenarios completos se desarrollan en:

```text
DOMAIN-008M-Test-Scenarios.md
```

---

# Auditoría

Las decisiones relevantes de autorización deben poder
correlacionarse con la operación solicitada cuando la arquitectura
de Audit lo requiera.

Conceptualmente puede utilizarse:

```text
ActorId

ParticipationId

OrganizationId

RequestedPermission

AuthorizationDecision

Timestamp

CorrelationId

CausationId
```

Audit permanece fuera del Aggregate Participation.

---

# Seguridad

Permissions constituye una parte del modelo conceptual de
seguridad, pero no representa el Security Model completo.

La definición complementaria corresponde a:

```text
DOMAIN-008O-Security-Model.md
```

Este documento se concentra exclusivamente en las capacidades de
autorización asociadas a operaciones sobre Participation.

---

# Persistencia

Participation no necesita persistir una colección interna de
Permissions para proteger su estado.

Las asignaciones entre:

```text
Actor

Membership

Role

Permission
```

pertenecen a los modelos responsables de autorización.

El Repository de Participation persiste el Aggregate, no el modelo
global de autorización.

---

# Interoperabilidad

Las integraciones que soliciten modificaciones deben respetar las
mismas reglas conceptuales de autorización.

No existe un modelo alternativo de dominio para:

```text
Internal API

Municipal API

Smart City Integration

FIWARE Integration
```

La procedencia de la solicitud no elimina los Permissions ni las
Invariants aplicables.

---

# Independencia Tecnológica

El modelo conceptual de Permissions no depende de:

```text
Keyrock

Wilma

OAuth2

JWT

OpenID Connect

HTTP

REST

GraphQL

FastAPI

Django

React

Database ACL

Cloud IAM
```

Estas tecnologías pueden implementar mecanismos relacionados con
Authentication o Authorization.

No definen el modelo conceptual del Aggregate.

---

# Compatibilidad con DDD

El modelo mantiene Domain-Driven Design porque:

- mantiene Authorization fuera del estado interno del Aggregate;
- protege el límite de consistencia;
- mantiene responsabilidades explícitas;
- evita acoplar Role y Membership a Participation;
- preserva las Invariants dentro del Aggregate;
- utiliza referencias entre Aggregates mediante identidad.

---

# Compatibilidad con Clean Architecture

El dominio permanece independiente de mecanismos técnicos de
seguridad.

Conceptualmente:

```text
Infrastructure Authorization

↓

Application

↓

Authorized Domain Intention

↓

Participation
```

Participation no depende de Infrastructure.

---

# Compatibilidad con Hexagonal Architecture

Los mecanismos concretos de autorización pueden conectarse mediante
Ports y Adapters.

El núcleo del dominio no depende de dichos Adapters.

---

# Compatibilidad con CQRS

Los Permissions pueden diferenciarse entre:

```text
Command Permissions

Query Permissions
```

El Write Side protege Commands.

El Read Side protege Queries y proyecciones.

Ambos permanecen conceptualmente separados.

---

# Compatibilidad con Event Sourcing

La autorización se evalúa sobre nuevas intenciones.

La reproducción de eventos históricos no requiere volver a
autorizar cada hecho.

Debe mantenerse:

```text
Command Authorization

≠

Event Replay Authorization
```

---

# Compatibilidad con Event-Driven Architecture

Un evento puede originar procesos posteriores, pero no concede por
sí mismo Permissions sobre Participation.

Todo nuevo Command protegido continúa sujeto a la autorización
correspondiente.

---

# Compatibilidad con Arquitectura Distribuida

Los Permissions pueden resolverse mediante capacidades distribuidas
sin modificar el límite de consistencia de Participation.

La arquitectura distribuida no convierte Authorization en una
responsabilidad interna del Aggregate.

---

# Evolución

El modelo puede incorporar nuevas capacidades cuando se agreguen
nuevos comportamientos oficiales a Participation.

Una nueva capacidad debe corresponder a una intención real del
dominio.

Ejemplo conceptual:

```text
NewParticipationCommand

↓

New Explicit Permission
```

La incorporación debe mantener coherencia con:

```text
DOMAIN-008-Aggregate.md

DOMAIN-008A-Lifecycle.md

DOMAIN-008B-State-Machine.md

DOMAIN-008C-Commands.md

DOMAIN-008D-Domain-Events.md

DOMAIN-008E-Invariants.md
```

---

# Extension Points

Las futuras extensiones de Permissions deben respetar:

- separación entre Authentication y Authorization;
- separación entre Authorization e Invariants;
- aislamiento organizacional;
- Least Privilege;
- Deny by Default;
- granularidad explícita;
- independencia tecnológica;
- límites entre Aggregates;
- trazabilidad;
- compatibilidad con Commands;
- compatibilidad con Lifecycle;
- compatibilidad con State Machine.

Las extensiones formales se documentarán en:

```text
DOMAIN-008P-Extension-Points.md
```

---

# Documentación Complementaria

El modelo de Permissions debe interpretarse conjuntamente con:

```text
DOMAIN-008-Aggregate.md

DOMAIN-008A-Lifecycle.md

DOMAIN-008B-State-Machine.md

DOMAIN-008C-Commands.md

DOMAIN-008D-Domain-Events.md

DOMAIN-008E-Invariants.md

DOMAIN-008G-Repository-Contract.md

DOMAIN-008I-Versioning.md

DOMAIN-008J-Consistency-Boundary.md

DOMAIN-008O-Security-Model.md
```

Cada documento desarrolla una responsabilidad específica sin
alterar la separación establecida en este documento.

---

# Principios Arquitectónicos

El modelo oficial de Permissions de Participation mantiene:

```text
Authentication

↓

Actor Identity
```

```text
Authorization

↓

Permission Decision
```

```text
Permission Granted

↓

Command
```

```text
Command

↓

Participation Aggregate
```

```text
Participation Aggregate

↓

State Machine

+

Invariants
```

```text
Valid Domain Change

↓

Version Increment

↓

Domain Event
```

y:

```text
Permission Denied

↓

No Command Execution

↓

No Aggregate Change

↓

No Version Increment

↓

No Success Domain Event
```

---

# Definición de Éxito

El modelo de Permissions del Aggregate **Participation** constituye
la definición conceptual oficial de las capacidades necesarias para
intentar operaciones sobre una Participation dentro de AURA Core.

El modelo garantiza que:

- Authentication permanezca separada de Authorization;
- Authorization permanezca separada de Domain Validation;
- los actores sean evaluados dentro de su contexto organizacional;
- Membership y Role puedan participar en Authorization sin formar
  parte del Aggregate;
- cada operación protegida pueda asociarse a una capacidad
  explícita;
- las capacidades mantengan granularidad suficiente;
- el acceso entre Organizations no sea concedido implícitamente;
- los actores administrativos continúen sujetos a las Invariants;
- los procesos automáticos no posean autoridad implícita;
- las integraciones externas no obtengan privilegios automáticos;
- los Read Permissions permanezcan separados de los Write
  Permissions;
- ninguna denegación modifique el estado, Version o timestamps;
- ninguna autorización permita evitar Lifecycle, State Machine o
  Invariants;
- Participation permanezca independiente de mecanismos técnicos de
  identidad y autorización.

La regla fundamental es:

```text
Authorized Domain Operation

=

Authenticated Actor

+

Granted Permission

+

Valid Organization Context

+

Valid Command

+

Valid Aggregate State

+

Preserved Invariants
```

La ausencia de cualquiera de las condiciones necesarias impide que
la operación produzca una modificación válida.

De esta forma,
`DOMAIN-008F-Permissions.md` establece el modelo oficial de
autorización conceptual para el Aggregate **Participation**,
manteniendo la separación de responsabilidades, el aislamiento
organizacional, la protección del dominio y la independencia
tecnológica conforme al patrón DDD consolidado de AURA Core.