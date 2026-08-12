# DOMAIN-006F — Assembly Permissions

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
* DOMAIN-006G-Repository-Contract.md
* DOMAIN-006I-Versioning.md
* DOMAIN-006J-Consistency-Boundary.md
* DOMAIN-006K-Integration-Events.md
* DOMAIN-006L-Read-Model.md
* DOMAIN-006M-Test-Scenarios.md
* DOMAIN-006N-Performance-Rules.md
* DOMAIN-006O-Security-Model.md
* DOMAIN-006P-Extension-Points.md
* DOMAIN-003-Aggregate.md
* DOMAIN-004-Aggregate.md
* CORE-003-Shared-Kernel.md
* CORE-004-Ubiquitous-Language.md
* CORE-006-Domain-Invariants.md
* CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Definir formalmente el modelo de **Permissions** asociado a las
operaciones del Aggregate **Assembly**.

Los Permissions determinan qué capacidades debe poseer un Actor
para solicitar una operación sobre una Assembly.

Los Permissions no determinan si una operación es válida desde la
perspectiva del dominio.

La autorización responde:

```text
¿Puede este Actor intentar ejecutar esta operación?
```

Assembly responde:

```text
¿Puede esta operación ocurrir sobre este Aggregate
en su estado actual?
```

Esta separación es obligatoria.

Ningún Permission puede anular:

* invariantes;
* State Machine;
* Guards;
* Lifecycle;
* consistencia;
* restricciones del Aggregate;
* Versioning.

---

# Propósito

El modelo de Permissions permite establecer una frontera explícita
entre:

```text
Authorization
```

y:

```text
Domain Behavior
```

El sistema de autorización determina si un Actor puede solicitar
una intención.

La Aggregate Root determina si esa intención puede convertirse en
un hecho válido del dominio.

Conceptualmente:

```text
Actor
    │
    ▼
Authorization
    │
    ├── Permission denied
    │       │
    │       ▼
    │    Rejected
    │
    └── Permission granted
            │
            ▼
         Command
            │
            ▼
         Assembly
            │
            ├── State
            ├── Guards
            ├── Invariants
            └── Domain Rules
                    │
                    ▼
                Domain Event
```

Authorization nunca modifica directamente Assembly.

---

# Principio Fundamental

Debe mantenerse siempre:

```text
Permission Granted
        ≠
Operation Valid
```

Un Actor autorizado puede intentar una operación que el dominio
deba rechazar.

Ejemplo:

```text
Actor has:
Assembly.Start
```

pero:

```text
AssemblyStatus = Draft
```

La operación:

```text
StartAssembly
```

debe ser rechazada porque:

```text
Draft -> InProgress
```

no constituye una transición válida.

El Permission concede capacidad de solicitud.

No concede capacidad para violar el dominio.

---

# Alcance

Los Permissions definidos en este documento protegen las
intenciones de modificación relacionadas con Assembly.

No definen permisos internos de:

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

Cada Aggregate o Bounded Context mantiene su propio modelo de
autorización cuando corresponda.

Assembly no absorbe los permisos de esos dominios.

---

# Permission como Capacidad

Un Permission representa una capacidad autorizable.

Ejemplos:

```text
Assembly.Create

Assembly.Schedule

Assembly.Convoke

Assembly.Start

Assembly.Complete

Assembly.Cancel

Assembly.Archive
```

Un Permission:

* posee significado estable;
* representa una capacidad;
* no representa un Actor;
* no representa una Membership;
* no representa un Role;
* no representa un Command;
* no representa un Domain Event;
* no representa un estado;
* no modifica el Aggregate.

---

# Permission versus Role

Debe mantenerse la separación:

```text
Role
    ≠
Permission
```

Role representa una función organizacional.

Ejemplos:

```text
President

Secretary

Treasurer

Moderator
```

Permission representa una capacidad autorizable.

Ejemplos:

```text
Assembly.Create

Assembly.Convoke

Assembly.Start
```

Un Role puede otorgar uno o más Permissions mediante las políticas
de autorización correspondientes.

Assembly no administra esa asociación.

---

# Permission versus Membership

Membership representa la relación formal entre:

```text
Citizen
```

y:

```text
Organization
```

Un Permission no implica por sí mismo una Membership válida.

Cuando una política requiera pertenencia organizacional, la
Authorization Layer debe considerar la Membership correspondiente.

Assembly no modifica Membership para autorizar una operación.

---

# Permission versus Actor

Actor representa la identidad que intenta ejecutar una operación.

Conceptualmente:

```text
ActorId
```

puede corresponder, según el contexto, a una identidad autorizable.

Un Actor puede obtener capacidades a través de:

* Membership;
* Role;
* políticas organizacionales;
* delegaciones;
* capacidades administrativas;
* mecanismos del contexto de autorización.

Assembly no determina cómo fueron obtenidos los Permissions.

---

# ActorId

Los Commands pueden contener:

```text
ActorId
```

ActorId permite:

* identificar quién solicitó la operación;
* resolver autorización;
* mantener trazabilidad;
* mantener Audit;
* establecer causalidad.

ActorId no contiene:

* Citizen completo;
* Membership completa;
* Role completo;
* credenciales;
* sesión;
* token.

---

# Organización como Frontera de Autorización

Assembly pertenece a una única:

```text
OrganizationId
```

Por lo tanto, los Permissions deben evaluarse dentro del contexto
organizacional correspondiente.

Conceptualmente:

```text
PermissionEvaluation(
    ActorId,
    OrganizationId,
    Permission
)
```

Un Permission concedido dentro de:

```text
Organization A
```

no autoriza automáticamente operaciones sobre una Assembly
perteneciente a:

```text
Organization B
```

---

# Aislamiento Organizacional

Debe mantenerse:

```text
Assembly.OrganizationId
=
AuthorizationContext.OrganizationId
```

para operaciones organizacionalmente restringidas.

Esta regla evita que un Actor utilice capacidades concedidas en
una Organization para modificar Assemblies pertenecientes a otra.

---

# Permission Global versus Organizacional

Una implementación futura puede distinguir capacidades:

```text
OrganizationScopedPermission
```

y:

```text
PlatformScopedPermission
```

Sin embargo, esa distinción debe ser explícita.

No debe asumirse que un Permission es global solo por compartir el
mismo nombre.

La versión 1.0 considera los Permissions de Assembly
principalmente dentro del contexto de Organization.

---

# Modelo Conceptual

```text
Citizen
    │
    ▼
Membership
    │
    ▼
Role
    │
    ▼
Authorization Policy
    │
    ▼
Permission
    │
    ▼
Command
    │
    ▼
Assembly
```

Esta representación describe colaboración conceptual.

No significa que estos Aggregates se encuentren contenidos dentro
de Assembly.

---

# Propiedad del Modelo de Autorización

Assembly no es propietario de:

* Authentication;
* Role assignment;
* Membership validation;
* credential management;
* token validation;
* session management.

Estas responsabilidades pertenecen a otros contextos.

Assembly define qué capacidad es requerida para intentar cada
operación.

---

# Permissions Oficiales

La versión 1.0 define las siguientes capacidades principales:

```text
Assembly.Create

Assembly.Schedule

Assembly.Reschedule

Assembly.Convoke

Assembly.Rename

Assembly.ChangeType

Assembly.ChangePurpose

Assembly.ChangeDescription

Assembly.ChangeModality

Assembly.ChangeLocation

Assembly.UpdateConvocation

Assembly.UpdateRules

Assembly.UpdateExecutionConditions

Assembly.Start

Assembly.Complete

Assembly.Cancel

Assembly.Archive

Assembly.Read

Assembly.List
```

Cuando existan operaciones administrativas adicionales deberán
incorporarse formalmente mediante evolución controlada.

---

# Categorías de Permissions

Los Permissions pueden clasificarse conceptualmente en:

```text
Lifecycle Permissions

Configuration Permissions

Scheduling Permissions

Convocation Permissions

Execution Permissions

Closure Permissions

Read Permissions
```

Esta clasificación facilita su administración.

No crea nuevos límites de dominio.

---

# Lifecycle Permissions

Protegen operaciones principales del Lifecycle.

```text
Assembly.Create

Assembly.Schedule

Assembly.Convoke

Assembly.Start

Assembly.Complete

Assembly.Cancel

Assembly.Archive
```

---

# Configuration Permissions

Protegen cambios configuracionales.

```text
Assembly.Rename

Assembly.ChangeType

Assembly.ChangePurpose

Assembly.ChangeDescription

Assembly.ChangeModality

Assembly.ChangeLocation

Assembly.UpdateRules

Assembly.UpdateExecutionConditions
```

---

# Scheduling Permissions

Protegen modificaciones de programación.

```text
Assembly.Schedule

Assembly.Reschedule
```

---

# Convocation Permissions

Protegen operaciones relacionadas con convocatoria.

```text
Assembly.Convoke

Assembly.UpdateConvocation
```

---

# Execution Permissions

Protegen el comienzo y la finalización efectiva de la reunión.

```text
Assembly.Start

Assembly.Complete
```

---

# Closure Permissions

Protegen operaciones que terminan o retiran Assembly de su flujo
operativo.

```text
Assembly.Complete

Assembly.Cancel

Assembly.Archive
```

---

# Read Permissions

Protegen acceso a información de Assembly cuando las políticas de
visibilidad lo requieran.

```text
Assembly.Read

Assembly.List
```

Los Read Permissions no forman parte del estado interno del
Aggregate.

---

# Convención de Naming

Los Permissions utilizan la estructura:

```text
Aggregate.Action
```

Ejemplos:

```text
Assembly.Create

Assembly.Schedule

Assembly.Start
```

La convención debe:

* utilizar lenguaje ubicuo;
* representar una capacidad;
* ser estable;
* evitar nombres tecnológicos;
* evitar nombres dependientes del transporte.

---

# Permissions Técnicos Prohibidos

No deben existir Permissions de dominio como:

```text
Assembly.HttpPost

Assembly.DatabaseUpdate

Assembly.MongoWrite

Assembly.KafkaPublish

Assembly.RedisInvalidate

Assembly.FIWARESync

Assembly.CallAPI
```

Estas acciones pertenecen a infraestructura.

No representan capacidades funcionales del dominio Assembly.

---

# Assembly.Create

## Objetivo

Autorizar la intención de crear una nueva Assembly dentro de una
Organization.

---

## Command asociado

```text
CreateAssembly
```

---

## Permission requerido

```text
Assembly.Create
```

---

## Condiciones de autorización

La Authorization Layer debe determinar, cuando corresponda:

* Actor autenticado;
* Actor identificado;
* contexto de Organization válido;
* Actor autorizado dentro de Organization;
* Permission Assembly.Create efectivo;
* restricciones organizacionales adicionales.

---

## Validaciones posteriores

Incluso autorizado, CreateAssembly puede ser rechazado por:

* AssemblyId inválido;
* AssemblyId duplicado;
* OrganizationId inválido;
* AssemblyName inválido;
* AssemblyType inválido;
* invariantes iniciales incumplidas.

---

# Assembly.Schedule

## Objetivo

Autorizar la programación formal de una Assembly.

---

## Command asociado

```text
ScheduleAssembly
```

---

## Permission requerido

```text
Assembly.Schedule
```

---

## Estado esperado por dominio

```text
Draft
```

---

## Regla

Poseer:

```text
Assembly.Schedule
```

no permite programar una Assembly en cualquier estado.

Assembly continúa validando:

```text
CurrentStatus == Draft
```

además de programación, modalidad, ubicación e invariantes.

---

# Assembly.Reschedule

## Objetivo

Autorizar la modificación de una programación existente.

---

## Command asociado

```text
RescheduleAssembly
```

---

## Permission requerido

```text
Assembly.Reschedule
```

---

## Estados conceptualmente permitidos

```text
Scheduled

Convoked
```

La operación desde Convoked está sujeta a reglas adicionales.

---

## Restricción

El Permission no autoriza:

* reprogramar una Assembly InProgress;
* reprogramar una Assembly Completed;
* reprogramar una Assembly Cancelled;
* reprogramar una Assembly Archived.

---

# Assembly.Convoke

## Objetivo

Autorizar la formalización de la convocatoria de una Assembly.

---

## Command asociado

```text
ConvokeAssembly
```

---

## Permission requerido

```text
Assembly.Convoke
```

---

## Estado esperado

```text
Scheduled
```

---

## Validaciones de dominio posteriores

Assembly debe comprobar:

* Schedule válido;
* Convocation válida;
* reglas de convocatoria;
* estado;
* invariantes;
* Version.

El Permission no sustituye estas verificaciones.

---

# Assembly.Rename

## Objetivo

Autorizar la modificación del nombre de Assembly.

---

## Command asociado

```text
RenameAssembly
```

---

## Permission requerido

```text
Assembly.Rename
```

---

## Restricción

La existencia del Permission no permite cambiar el nombre en un
estado que el dominio haya declarado inmutable.

Por ejemplo:

```text
Archived
```

continúa siendo inmutable.

---

# Assembly.ChangeType

## Objetivo

Autorizar una modificación de AssemblyType.

---

## Command asociado

```text
ChangeAssemblyType
```

---

## Permission requerido

```text
Assembly.ChangeType
```

---

## Regla

La autorización debe preceder la evaluación de las restricciones
de estado.

Assembly decide finalmente si el tipo puede modificarse sin
alterar:

* significado histórico;
* AssemblyRules;
* ExecutionConditions;
* convocatoria;
* Lifecycle.

---

# Assembly.ChangePurpose

## Objetivo

Autorizar la modificación del propósito formal.

---

## Command asociado

```text
ChangeAssemblyPurpose
```

---

## Permission requerido

```text
Assembly.ChangePurpose
```

---

## Restricción

El Permission no autoriza reescritura retroactiva del propósito de
una Assembly cuando el estado ya no permita dicha modificación.

---

# Assembly.ChangeDescription

## Objetivo

Autorizar la modificación de AssemblyDescription.

---

## Command asociado

```text
ChangeAssemblyDescription
```

---

## Permission requerido

```text
Assembly.ChangeDescription
```

---

## Regla

La modificación debe respetar:

* estados permitidos;
* historicidad;
* invariantes;
* Versioning.

---

# Assembly.ChangeModality

## Objetivo

Autorizar el cambio de modalidad de realización.

---

## Command asociado

```text
ChangeAssemblyModality
```

---

## Permission requerido

```text
Assembly.ChangeModality
```

---

## Validaciones de dominio

Assembly debe comprobar posteriormente:

* nueva modalidad válida;
* compatibilidad con Location;
* compatibilidad con AssemblyRules;
* compatibilidad con ExecutionConditions;
* convocatoria consistente;
* estado permitido.

---

# Assembly.ChangeLocation

## Objetivo

Autorizar el cambio de ubicación formal de Assembly.

---

## Command asociado

```text
ChangeAssemblyLocation
```

---

## Permission requerido

```text
Assembly.ChangeLocation
```

---

## Regla

El Permission permite solicitar el cambio.

No permite:

* modificar Territory;
* saltar restricciones del estado;
* reescribir ubicación histórica sin trazabilidad.

---

# Assembly.UpdateConvocation

## Objetivo

Autorizar la modificación de información formal de convocatoria.

---

## Command asociado

```text
UpdateAssemblyConvocation
```

---

## Permission requerido

```text
Assembly.UpdateConvocation
```

---

## Restricción Histórica

Incluso con Permission válido no puede eliminarse:

```text
ConvokedAt
```

para ocultar una convocatoria ya ocurrida.

La autorización no permite reescribir hechos históricos.

---

# Assembly.UpdateRules

## Objetivo

Autorizar la modificación de AssemblyRules.

---

## Command asociado

```text
UpdateAssemblyRules
```

---

## Permission requerido

```text
Assembly.UpdateRules
```

---

## Regla

El Actor autorizado puede proponer nuevas reglas.

Assembly debe continuar validando que estas:

* sean válidas;
* sean compatibles con AssemblyType;
* sean compatibles con AssemblyModality;
* sean compatibles con ExecutionConditions;
* no violen invariantes;
* no reescriban hechos históricos.

---

# Assembly.UpdateExecutionConditions

## Objetivo

Autorizar la modificación de las condiciones de realización.

---

## Command asociado

```text
UpdateAssemblyExecutionConditions
```

---

## Permission requerido

```text
Assembly.UpdateExecutionConditions
```

---

## Restricción

El Permission no permite modificar condiciones después de que el
estado haya convertido dichas condiciones en hechos históricos no
modificables.

---

# Assembly.Start

## Objetivo

Autorizar la intención de iniciar formalmente una Assembly.

---

## Command asociado

```text
StartAssembly
```

---

## Permission requerido

```text
Assembly.Start
```

---

## Estado requerido por dominio

```text
Convoked
```

---

## Guards posteriores

Después de la autorización Assembly debe validar:

```text
ScheduleValid

ConvocationValid

ModalityValid

LocationValid when required

ExecutionConditionsSatisfied
```

---

## Resultado válido

Únicamente si todas las reglas se cumplen:

```text
Convoked
    ↓
InProgress
```

y se produce:

```text
AssemblyStarted
```

---

# Assembly.Complete

## Objetivo

Autorizar la finalización formal de una Assembly en ejecución.

---

## Command asociado

```text
CompleteAssembly
```

---

## Permission requerido

```text
Assembly.Complete
```

---

## Estado requerido

```text
InProgress
```

---

## Validaciones de dominio

Debe cumplirse:

```text
StartedAt != null

CompletedAt >= StartedAt

CompletionConditionsSatisfied
```

cuando las condiciones de cierre formen parte del modelo.

---

## Resultado

```text
InProgress
    ↓
Completed
```

Evento:

```text
AssemblyCompleted
```

---

# Assembly.Cancel

## Objetivo

Autorizar la cancelación formal de una Assembly.

---

## Command asociado

```text
CancelAssembly
```

---

## Permission requerido

```text
Assembly.Cancel
```

---

## Estados permitidos

```text
Draft

Scheduled

Convoked
```

---

## Estados no autorizables mediante este Permission

```text
InProgress

Completed

Cancelled

Archived
```

La existencia de Assembly.Cancel no amplía la State Machine.

---

# Assembly.Archive

## Objetivo

Autorizar el archivado formal de Assembly.

---

## Command asociado

```text
ArchiveAssembly
```

---

## Permission requerido

```text
Assembly.Archive
```

---

## Estados permitidos

```text
Completed

Cancelled
```

---

## Resultado

```text
Archived
```

Archived permanece terminal e inmutable.

---

# Assembly.Read

## Objetivo

Autorizar la lectura de una Assembly cuando la información no sea
públicamente visible según las políticas del sistema.

---

## Tipo

```text
Read Permission
```

---

## Regla

Assembly.Read protege acceso.

No modifica el Aggregate.

No incrementa Version.

No produce Domain Events.

---

# Assembly.List

## Objetivo

Autorizar la consulta de colecciones o listados de Assemblies
cuando corresponda.

---

## Tipo

```text
Read Permission
```

---

## Regla

Assembly.List pertenece al modelo de autorización de lectura.

No representa un Command de escritura.

No modifica Assembly.

---

# Matriz Command-Permission

| Command                           | Permission requerido               |
| --------------------------------- | ---------------------------------- |
| CreateAssembly                    | Assembly.Create                    |
| ScheduleAssembly                  | Assembly.Schedule                  |
| RescheduleAssembly                | Assembly.Reschedule                |
| ConvokeAssembly                   | Assembly.Convoke                   |
| RenameAssembly                    | Assembly.Rename                    |
| ChangeAssemblyType                | Assembly.ChangeType                |
| ChangeAssemblyPurpose             | Assembly.ChangePurpose             |
| ChangeAssemblyDescription         | Assembly.ChangeDescription         |
| ChangeAssemblyModality            | Assembly.ChangeModality            |
| ChangeAssemblyLocation            | Assembly.ChangeLocation            |
| UpdateAssemblyConvocation         | Assembly.UpdateConvocation         |
| UpdateAssemblyRules               | Assembly.UpdateRules               |
| UpdateAssemblyExecutionConditions | Assembly.UpdateExecutionConditions |
| StartAssembly                     | Assembly.Start                     |
| CompleteAssembly                  | Assembly.Complete                  |
| CancelAssembly                    | Assembly.Cancel                    |
| ArchiveAssembly                   | Assembly.Archive                   |

---

# Matriz Permission-Estado

| Permission                         | Draft |   Scheduled |    Convoked |  InProgress | Completed | Cancelled | Archived |
| ---------------------------------- | ----: | ----------: | ----------: | ----------: | --------: | --------: | -------: |
| Assembly.Schedule                  |    Sí |          No |          No |          No |        No |        No |       No |
| Assembly.Reschedule                |    No |          Sí | Condicional |          No |        No |        No |       No |
| Assembly.Convoke                   |    No |          Sí |          No |          No |        No |        No |       No |
| Assembly.Rename                    |    Sí |          Sí | Condicional |          No |        No |        No |       No |
| Assembly.ChangeType                |    Sí | Condicional |          No |          No |        No |        No |       No |
| Assembly.ChangePurpose             |    Sí |          Sí | Condicional |          No |        No |        No |       No |
| Assembly.ChangeDescription         |    Sí |          Sí |          Sí | Condicional |        No |        No |       No |
| Assembly.ChangeModality            |    Sí |          Sí | Condicional |          No |        No |        No |       No |
| Assembly.ChangeLocation            |    Sí |          Sí | Condicional | Condicional |        No |        No |       No |
| Assembly.UpdateConvocation         |    Sí |          Sí |          Sí |          No |        No |        No |       No |
| Assembly.UpdateRules               |    Sí |          Sí | Condicional | Condicional |        No |        No |       No |
| Assembly.UpdateExecutionConditions |    Sí |          Sí | Condicional |          No |        No |        No |       No |
| Assembly.Start                     |    No |          No |          Sí |          No |        No |        No |       No |
| Assembly.Complete                  |    No |          No |          No |          Sí |        No |        No |       No |
| Assembly.Cancel                    |    Sí |          Sí |          Sí |          No |        No |        No |       No |
| Assembly.Archive                   |    No |          No |          No |          No |        Sí |        Sí |       No |

La matriz expresa compatibilidad conceptual entre autorización y
estado.

No sustituye las invariantes ni los Guards.

`Condicional` significa que además del Permission deben cumplirse
reglas específicas definidas por el modelo.

---

# Permission y State Machine

Debe mantenerse:

```text
Permission
        │
        ▼
Command may be attempted
        │
        ▼
State Machine validation
```

Nunca:

```text
Permission
        │
        ▼
force transition
```

La State Machine definida en:

```text
DOMAIN-006B-State-Machine.md
```

permanece autoritativa respecto de las transiciones.

---

# Permission y Guards

Los Guards continúan evaluándose después de la autorización.

Ejemplo:

```text
Permission = Assembly.Start
```

no evita la evaluación de:

```text
CanStartAssembly
```

El Guard puede rechazar la operación aunque el Permission sea
válido.

---

# Permission e Invariantes

Ningún Permission puede desactivar:

```text
DOMAIN-006E-Invariants.md
```

Debe mantenerse:

```text
PermissionGranted
AND
InvariantViolation
=
OperationRejected
```

---

# Permission y Versioning

La autorización tampoco sustituye:

```text
ExpectedVersion
```

Un Actor autorizado puede ejecutar un Command basado en una
versión obsoleta.

Ejemplo:

```text
Permission = Assembly.Cancel

ExpectedVersion = 4

PersistedVersion = 5
```

Resultado:

```text
ConcurrencyConflict
```

La operación debe rechazarse.

---

# Permission y Optimistic Concurrency

Debe cumplirse:

```text
AuthorizationValid
AND
DomainValid
AND
ExpectedVersionValid
```

antes de aceptar la modificación persistida.

Cada mecanismo protege una dimensión diferente.

---

# Permission y Domain Events

Los Permissions no producen Domain Events por sí mismos.

Ejemplo:

conceder:

```text
Assembly.Start
```

a un Actor no produce:

```text
AssemblyStarted
```

El Domain Event solo se genera cuando:

```text
StartAssembly
```

es ejecutado válidamente por Assembly.

---

# Permission Denied

Cuando el Permission requerido no está presente:

```text
PermissionDenied
```

debe rechazarse la intención antes de ejecutar comportamiento
protegido.

No debe modificarse:

```text
Assembly
```

No debe incrementarse:

```text
Version
```

No debe producirse ningún Domain Event de éxito.

---

# Authorization Failure versus Domain Failure

Debe distinguirse:

```text
Authorization Failure
```

de:

```text
Domain Rule Failure
```

Ejemplo de Authorization Failure:

```text
Actor lacks Assembly.Start
```

Ejemplo de Domain Failure:

```text
Actor has Assembly.Start

AssemblyStatus = Draft
```

Ambos rechazan la operación, pero representan causas
conceptualmente diferentes.

---

# Permission Denied no es Domain Event de Assembly

Un rechazo por autorización no representa necesariamente un hecho
del Aggregate.

Por lo tanto no debe producir automáticamente:

```text
AssemblyPermissionDenied
```

como Domain Event.

Puede registrarse mediante:

* Security Audit;
* Application Audit;
* observabilidad;
* logging seguro.

---

# Auditoría de Authorization

Los intentos de operaciones protegidas pueden registrar
conceptualmente:

```text
ActorId

OrganizationId

Permission

CommandType

AssemblyId

Timestamp

AuthorizationDecision

CorrelationId

CausationId
```

Estos registros pertenecen al mecanismo de seguridad o Audit.

No forman parte obligatoria del estado interno de Assembly.

---

# AuthorizationDecision

Una decisión de autorización puede representarse
conceptualmente como:

```text
Granted

Denied
```

Esta decisión debe ocurrir fuera de la Aggregate Root.

Assembly no consulta directamente un servidor IAM.

---

# Authentication versus Authorization

Debe mantenerse:

```text
Authentication
        ≠
Authorization
```

Authentication responde:

```text
¿Quién es el Actor?
```

Authorization responde:

```text
¿Qué puede hacer este Actor?
```

Assembly responde:

```text
¿Es válida esta operación en el dominio?
```

Las tres responsabilidades permanecen separadas.

---

# Authentication fuera de Assembly

Assembly no:

* valida passwords;
* valida OAuth tokens;
* valida JWT;
* administra sesiones;
* autentica Citizens;
* renueva credenciales.

La autenticación pertenece al contexto correspondiente.

---

# Permission Resolution

La resolución de Permissions puede utilizar conceptualmente:

```text
ActorId

OrganizationId

MembershipId

RoleId

Policies
```

pero Assembly no debe ejecutar directamente la resolución.

La Authorization Layer entrega la decisión correspondiente antes
de invocar comportamiento protegido.

---

# Role-Based Authorization

Una implementación puede utilizar:

```text
RBAC
```

donde:

```text
Role
    │
    ▼
Permissions
```

Ejemplo conceptual:

```text
President
    ├── Assembly.Create
    ├── Assembly.Schedule
    ├── Assembly.Convoke
    ├── Assembly.Start
    ├── Assembly.Complete
    └── Assembly.Cancel
```

Esta relación es política de autorización.

No una invariante del Aggregate Assembly.

---

# No Hardcoding de Role en Assembly

Assembly no debe implementar lógica como:

```text
if actor.role == "PRESIDENT":
    allow_start()
```

Esta decisión acoplaría el Aggregate al modelo de Roles.

Debe evaluarse:

```text
has_permission(
    ActorId,
    OrganizationId,
    Assembly.Start
)
```

fuera del Aggregate.

---

# Evolución Independiente de Roles

La separación permite que una Organization cambie:

* nombres de Roles;
* estructura organizacional;
* asociaciones Role-Permission;

sin modificar Assembly.

Assembly continúa expresando solamente las capacidades requeridas.

---

# Permission-Based Authorization

Debe preferirse semánticamente la capacidad:

```text
Assembly.Start
```

por sobre una dependencia rígida hacia:

```text
President
```

porque distintos modelos organizacionales pueden autorizar
diferentes Roles.

---

# Membership-Based Conditions

Una política puede exigir:

```text
Active Membership
```

para determinadas operaciones.

Esta condición se resuelve fuera de Assembly.

Assembly no mantiene una Membership mutable dentro de su
Consistency Boundary.

---

# Membership y Organization

Cuando la autorización se base en Membership debe verificarse
conceptualmente que:

```text
Membership.OrganizationId
=
Assembly.OrganizationId
```

La validación pertenece al proceso de autorización.

---

# Delegación

Una Organization puede necesitar delegar temporalmente una
capacidad.

Ejemplo:

```text
Assembly.Convoke
```

La delegación no debe modificar Assembly.

Debe implementarse como política del sistema de autorización.

---

# Delegación Temporal

Cuando existan delegaciones temporales deben poder expresar:

```text
Permission

ActorId

OrganizationId

ValidFrom

ValidUntil
```

según el modelo correspondiente.

Una delegación expirada no autoriza nuevas operaciones.

---

# Delegación no Modifica Role

Una delegación de Permission no exige necesariamente modificar el
Role formal del Actor.

Permission y Role permanecen desacoplados.

---

# Permission Expiration

Si una capacidad posee vigencia temporal, la Authorization Layer
debe comprobarla antes de ejecutar el Command.

Assembly no administra:

```text
PermissionExpiration
```

internamente.

---

# Revocación

La revocación de un Permission afecta nuevas decisiones de
autorización.

No revierte automáticamente hechos previamente válidos.

Ejemplo:

un Actor inició válidamente una Assembly y posteriormente perdió:

```text
Assembly.Start
```

El evento:

```text
AssemblyStarted
```

continúa siendo verdadero.

---

# Historicidad de Authorization

La autorización debe evaluarse utilizando la política vigente en
el momento de la operación.

Una modificación posterior de Roles o Permissions no debe
reescribir retroactivamente la validez de un hecho ya aceptado.

---

# Separation of Duties

Una Organization puede establecer políticas de separación de
funciones.

Ejemplo conceptual:

```text
Actor who creates Assembly
    cannot approve specific subsequent operation
```

si esa necesidad existe.

Estas políticas deben modelarse explícitamente en Authorization o
Domain Policies.

No deben introducirse implícitamente.

---

# Self-Authorization

Un Actor no debe poder concederse arbitrariamente un Permission
mediante una operación de Assembly.

Assembly no administra su propio modelo de autorización.

---

# Elevated Privileges

Un Permission administrativo elevado tampoco anula invariantes.

Por ejemplo:

```text
PlatformAdministrator
```

podría poseer:

```text
Assembly.Archive
```

pero no puede archivar una Assembly desde:

```text
InProgress
```

si la State Machine lo prohíbe.

---

# Superuser no Anula el Dominio

No debe existir una regla implícita:

```text
if superuser:
    bypass invariants
```

El dominio continúa siendo obligatorio.

Si una operación excepcional es realmente necesaria debe modelarse
como comportamiento explícito con:

* Command;
* Permission;
* reglas;
* Domain Event;
* Audit;
* tests.

---

# System Actor

Procesos automatizados pueden actuar mediante una identidad
explícita:

```text
SystemActorId
```

cuando la arquitectura lo requiera.

Un System Actor también debe poseer capacidades autorizadas.

No se considera implícitamente omnipotente.

---

# Automated Commands

Un proceso automático que intente ejecutar:

```text
ArchiveAssembly
```

debe pasar por:

```text
Authorization
```

y:

```text
Domain Validation
```

de la misma manera conceptual que un Actor humano.

---

# Service Accounts

Cuando integraciones utilicen identidades técnicas, estas deben
permanecer fuera del Aggregate.

La Authorization Layer puede resolver Permissions para:

```text
ServiceAccountActorId
```

sin almacenar credenciales dentro de Assembly.

---

# Permissions de Sistemas Externos

Un sistema externo no recibe acceso directo al estado interno del
Aggregate.

Debe utilizar:

```text
External Identity
      │
      ▼
Authorization
      │
      ▼
Anti-Corruption Layer
      │
      ▼
Application Layer
      │
      ▼
Command
      │
      ▼
Assembly
```

---

# FIWARE

FIWARE no posee autoridad implícita sobre Assembly.

Una integración FIWARE puede utilizar una identidad técnica
autorizada.

Esa identidad debe poseer el Permission correspondiente si intenta
originar un Command.

---

# NGSI-LD

Una actualización NGSI-LD como:

```text
status = "completed"
```

no constituye autorización ni una transición válida por sí misma.

Debe convertirse, cuando corresponda, en una intención compatible
con:

```text
CompleteAssembly
```

y requerir:

```text
Assembly.Complete
```

además de todas las invariantes.

---

# Anti-Corruption Layer

La Anti-Corruption Layer traduce:

* identidades externas;
* capacidades externas;
* operaciones externas;
* conceptos externos;

al lenguaje autorizado de AURA.

No debe conceder Permissions implícitamente por equivalencia
sintáctica.

---

# Denegación por Defecto

La política de autorización debe seguir conceptualmente:

```text
deny by default
```

Si no existe una concesión válida para el Permission requerido:

```text
Denied
```

La ausencia de una prohibición explícita no significa
autorización.

---

# Least Privilege

Debe aplicarse:

```text
Principle of Least Privilege
```

Un Actor debe recibir únicamente las capacidades necesarias para
sus responsabilidades.

No debe otorgarse:

```text
Assembly.*
```

cuando solo requiere:

```text
Assembly.Read
```

o:

```text
Assembly.Start
```

---

# Wildcard Permissions

Una implementación puede soportar internamente:

```text
Assembly.*
```

como mecanismo de configuración.

Sin embargo, la semántica oficial continúa definida por los
Permissions individuales.

Un wildcard no constituye una nueva capacidad del dominio.

---

# Permission Composition

Una política puede construir capacidades efectivas mediante
múltiples fuentes.

Ejemplo:

```text
Role Permission
+
Delegated Permission
+
Organization Policy
=
Effective Permission Set
```

La resolución ocurre antes del comportamiento del Aggregate.

---

# Deny Rules

Una política de autorización puede incorporar denegaciones
explícitas.

Conceptualmente:

```text
GrantedPermission
+
ExplicitDeny
=
Denied
```

La precedencia exacta pertenece al modelo de Authorization.

Assembly recibe únicamente la decisión final.

---

# Contextual Authorization

La autorización puede depender de contexto.

Ejemplo:

```text
ActorId

OrganizationId

AssemblyId

Permission

CurrentTime
```

cuando existan restricciones temporales o de alcance.

El contexto no debe utilizarse para modificar las invariantes.

---

# Resource-Based Authorization

Puede existir autorización basada en la Assembly específica.

Ejemplo conceptual:

```text
Actor may read Assembly A
but not Assembly B
```

La Authorization Layer puede considerar:

```text
AssemblyId
```

como ResourceId.

---

# Ownership no Equivale a Permission

Que una Assembly pertenezca a una Organization no significa que
todos los miembros de esa Organization posean automáticamente
todas las capacidades.

Las políticas determinan qué Actors obtienen cada Permission.

---

# Creator no Obtiene Permisos Implícitos

El Actor que crea una Assembly no adquiere automáticamente:

```text
Assembly.Convoke

Assembly.Start

Assembly.Complete

Assembly.Cancel
```

salvo que una política explícita así lo determine.

---

# Permission Snapshot

Cuando sea necesario preservar una decisión para trazabilidad
puede registrarse conceptualmente:

```text
AuthorizationDecisionId

ActorId

OrganizationId

Permission

Decision

EvaluatedAt

PolicyVersion
```

Esto no forma parte necesariamente del estado interno de Assembly.

---

# PolicyVersion

Si las políticas de autorización evolucionan puede ser útil
registrar:

```text
PolicyVersion
```

para comprender bajo qué reglas fue autorizada una operación.

PolicyVersion es diferente de:

```text
Assembly.Version
```

---

# Assembly.Version versus PolicyVersion

```text
Assembly.Version
```

representa evolución del Aggregate.

```text
PolicyVersion
```

representa evolución de las reglas de autorización.

No deben confundirse.

---

# Authorization y CorrelationId

Las decisiones de autorización pueden conservar:

```text
CorrelationId
```

para relacionarse con:

```text
Command

Domain Event

Audit
```

sin convertir la decisión de autorización en un Domain Event de
Assembly.

---

# Authorization y CausationId

Cuando corresponda, puede conservarse:

```text
CausationId
```

para identificar la solicitud que produjo la decisión.

Esto permite trazabilidad causal completa.

---

# Permission Evaluation Flow

El flujo recomendado es:

```text
Request
    │
    ▼
Authentication
    │
    ▼
ActorId
    │
    ▼
Resolve Organization Context
    │
    ▼
Resolve Required Permission
    │
    ▼
Authorization Decision
    │
    ├── Denied
    │      │
    │      ▼
    │   Reject
    │
    └── Granted
           │
           ▼
       Load Assembly
           │
           ▼
      Validate Version
           │
           ▼
       Execute Domain Behavior
           │
           ▼
       Validate Invariants
           │
           ▼
       Persist + Events
```

La ubicación exacta de determinados pasos puede variar conforme a
la arquitectura de Application Services, pero sus
responsabilidades deben permanecer separadas.

---

# Authorization antes de Modificación

Ningún comportamiento protegido debe modificar Assembly antes de
resolver autorización.

No debe existir:

```text
mutate Assembly
    ↓
check Permission
```

La evaluación debe ocurrir antes de aceptar la modificación.

---

# Authorization y Carga del Aggregate

En algunos casos puede ser necesario cargar información mínima del
recurso para determinar:

```text
OrganizationId
```

o aplicar Resource-Based Authorization.

Esta necesidad no cambia el principio de que el Aggregate no
resuelve los Permissions internamente.

---

# Filtrado de Existencia

Por razones de seguridad, una Application Layer puede evitar
revelar si una Assembly existe cuando el Actor no posee permisos de
lectura.

Esta política pertenece al Security Model.

No modifica la semántica del Aggregate.

---

# Permissions de Lectura versus Escritura

Debe distinguirse:

```text
Read Permissions
```

de:

```text
Write Permissions
```

Un Actor puede poseer:

```text
Assembly.Read
```

sin poseer:

```text
Assembly.Schedule
```

o:

```text
Assembly.Start
```

La lectura no implica capacidad de modificación.

---

# Read Models

Los Read Models pueden aplicar Permissions diferentes a los del
Write Model.

Ejemplo:

```text
Assembly.List
```

puede controlar acceso a una proyección.

Esta autorización no modifica Assembly.

---

# Public Assemblies

Una política futura puede declarar determinadas Assemblies como
públicamente visibles.

En ese caso:

```text
Assembly.Read
```

podría no ser necesario para ciertos datos públicos.

La política de visibilidad debe ser explícita.

No debe confundirse visibilidad con permiso de modificación.

---

# Field-Level Authorization

Si una futura necesidad exige controlar campos específicos de
lectura, debe modelarse en el Security/Read Model correspondiente.

Assembly no debe introducir setters o estados adicionales para
resolver Field-Level Authorization.

---

# Permission y Consistency Boundary

Authorization se encuentra fuera del límite de consistencia de
Assembly.

Conceptualmente:

```text
Authorization Decision
        │
        ▼
Assembly Command
        │
        ▼
Assembly Consistency Boundary
```

No se requiere una transacción distribuida entre el sistema de
autorización y Assembly.

---

# Cambio de Permission Concurrente

Puede existir una carrera entre:

```text
Permission granted
```

y una posterior:

```text
Permission revoked
```

La política de consistencia de autorización debe establecer en qué
momento se considera válida la decisión.

Esta decisión pertenece al Authorization/Security Model.

No debe resolverse alterando la State Machine de Assembly.

---

# Consistencia de Authorization

La consistencia requerida para decisiones de permisos debe
definirse conforme al riesgo de la operación.

Operaciones como:

```text
Assembly.Start

Assembly.Complete

Assembly.Cancel
```

pueden exigir decisiones más estrictas que operaciones de lectura.

La estrategia concreta pertenece al Security Model.

---

# Permission Caching

Los Permissions pueden almacenarse temporalmente en caché por
razones de rendimiento.

Sin embargo, la caché no debe convertirse en fuente permanente de
verdad.

Debe respetar:

* revocación;
* expiración;
* Organization scope;
* PolicyVersion;
* requerimientos de seguridad.

---

# Cache Staleness

Una decisión obsoleta podría conceder una capacidad revocada.

Por ello las operaciones sensibles deben aplicar una política de
frescura adecuada.

La definición concreta pertenece a:

```text
DOMAIN-006O-Security-Model.md
```

y a los mecanismos generales de Authorization.

---

# No Permission State inside Assembly

Assembly no debe mantener internamente colecciones como:

```text
AllowedUsers

AllowedRoles

Permissions

AccessTokens
```

como parte de su estado principal.

Estas responsabilidades pertenecen al modelo de autorización.

---

# No Role Assignment inside Assembly

Assembly no debe ejecutar:

```text
assignRole()

grantPermission()

revokePermission()
```

Estas operaciones no pertenecen a su comportamiento.

---

# No Credential Storage

Assembly nunca almacena:

```text
Password

OAuthToken

JWT

RefreshToken

APIKey

ClientSecret

PrivateKey

SessionCookie
```

La presencia de estas propiedades dentro del Aggregate violaría su
Consistency Boundary.

---

# Permission Checks no son Invariantes

Una regla:

```text
Actor must have Assembly.Start
```

no constituye una invariante estructural de Assembly.

Es una regla de autorización.

La invariante correspondiente al inicio es:

```text
AssemblyStatus == Convoked
```

junto con los Guards y condiciones requeridas.

---

# Reglas Organizacionales Adicionales

Una Organization puede establecer políticas como:

```text
OnlyBoardMembersMayConvoke

OnlyChairMayStart

SecretaryMayComplete

AdministratorMayArchive
```

Estas políticas deben traducirse a decisiones de autorización
basadas en Permissions.

Assembly no debe codificar nombres concretos de Roles si la
capacidad puede expresarse mediante Permissions.

---

# Ejemplo de Política

Una política podría resolver:

```text
Role = PRESIDENT
```

a:

```text
Assembly.Create

Assembly.Schedule

Assembly.Convoke

Assembly.Start

Assembly.Complete

Assembly.Cancel
```

Mientras:

```text
Role = SECRETARY
```

podría obtener:

```text
Assembly.Read

Assembly.ChangeDescription
```

Esto es un ejemplo de configuración.

No constituye una asociación universal obligatoria para todas las
Organizations.

---

# No Roles Universales Impuestos

El Aggregate no debe asumir que todas las Organizations poseen:

```text
President

Secretary

Treasurer
```

El modelo de Permissions permite que estructuras organizacionales
diferentes utilicen las mismas capacidades.

---

# Policies versus Permissions

Debe mantenerse:

```text
Policy
```

como regla para decidir si:

```text
Permission
```

es efectivo para un Actor.

El Permission representa la capacidad.

La Policy determina su concesión.

---

# Conditional Permissions

Una política puede conceder un Permission bajo condiciones.

Ejemplo:

```text
Assembly.ChangeLocation
```

solo mientras la Assembly se encuentre:

```text
Scheduled
```

Sin embargo, incluso si la política concede el Permission, el
Aggregate debe validar nuevamente el estado.

---

# Domain State en Authorization

La Authorization Layer puede utilizar AssemblyStatus como
información contextual cuando sea necesario.

Pero no debe convertirse en la autoridad del Lifecycle.

La misma regla debe continuar protegida por Assembly.

---

# Defense in Depth

Puede existir validación redundante de determinadas restricciones
en autorización y dominio como mecanismo de seguridad.

Ejemplo:

Authorization puede no conceder:

```text
Assembly.Start
```

para una Assembly Archived.

Assembly igualmente debe rechazar StartAssembly desde Archived.

Esta redundancia no rompe responsabilidades siempre que Assembly
continúe siendo autoridad de sus invariantes.

---

# Reglas de Rechazo

Una operación debe rechazarse por autorización cuando:

* Actor no está identificado cuando la operación lo requiere;
* Organization context no es válido;
* Permission requerido no está concedido;
* Permission se encuentra expirado;
* Permission se encuentra revocado;
* una restricción explícita de autorización lo deniega;
* el Actor intenta operar fuera de su Organization scope;
* una política de seguridad adicional rechaza la intención.

---

# Efectos del Rechazo por Permission

Cuando Authorization devuelve:

```text
Denied
```

debe mantenerse:

```text
Assembly state unchanged

Version unchanged

No success Domain Event

No external success Integration Event
```

La operación no llega a convertirse en comportamiento exitoso del
Aggregate.

---

# Rechazo Atómico

No deben existir modificaciones parciales antes de detectar que el
Actor carece del Permission requerido.

El rechazo debe ocurrir sin alterar Assembly.

---

# Errores de Authorization

Los errores conceptuales pueden incluir:

```text
PermissionDenied

OrganizationScopeViolation

PermissionExpired

PermissionRevoked

AuthorizationContextInvalid
```

Estos errores no deben confundirse con:

```text
InvalidAssemblyState

InvalidAssemblyTransition

AssemblyInvariantViolation

ConcurrencyConflict
```

---

# Error de Authentication

Una identidad no autenticada puede producir:

```text
Unauthenticated
```

antes incluso de la evaluación de Permission.

Esto tampoco constituye un Domain Event de Assembly.

---

# Error Taxonomy

Conceptualmente:

```text
Request
    │
    ├── Authentication Failure
    │
    ├── Authorization Failure
    │
    ├── Concurrency Failure
    │
    ├── Domain Failure
    │
    └── Infrastructure Failure
```

Estas categorías deben permanecer diferenciadas.

---

# Security Audit

Los siguientes intentos pueden requerir auditoría reforzada:

```text
Assembly.Start denied

Assembly.Complete denied

Assembly.Cancel denied

Assembly.Archive denied
```

especialmente cuando la causa sea:

* cross-organization attempt;
* revoked permission;
* privilege escalation;
* invalid service identity.

La política concreta pertenece al Security Model.

---

# Privilege Escalation

Un Actor no debe obtener nuevas capacidades como efecto secundario
de un Command de Assembly.

Ejecutar:

```text
CreateAssembly
```

no concede automáticamente nuevos Permissions.

---

# Confused Deputy Protection

Los Application Services deben preservar:

```text
OriginalActorId
```

cuando ejecuten operaciones en representación de un Actor.

Un servicio privilegiado no debe convertir una solicitud no
autorizada en una operación autorizada simplemente porque el
servicio posee credenciales técnicas elevadas.

---

# Actor versus Service Identity

Cuando un servicio actúa en nombre de un usuario pueden existir:

```text
ActorId

ServiceIdentity
```

con significados diferentes.

La trazabilidad debe conservar quién originó la intención cuando
corresponda.

---

# Impersonation

Si la plataforma soporta impersonation administrativa, esta
capacidad debe:

* estar explícitamente autorizada;
* quedar auditada;
* mantener identidad del impersonador;
* mantener identidad representada;
* no alterar invariantes.

No debe implementarse como sustitución silenciosa de ActorId.

---

# Permissions y Audit

Una operación exitosa puede registrar:

```text
ActorId

PermissionUsed

OrganizationId

AssemblyId

CommandId

DomainEventId

Timestamp

CorrelationId
```

cuando las políticas de Audit lo requieran.

Audit continúa siendo un Aggregate independiente.

---

# PermissionUsed

Registrar:

```text
PermissionUsed
```

puede permitir conocer qué capacidad justificó una operación.

No es obligatorio que forme parte del Domain Event de Assembly.

Puede mantenerse como metadato de seguridad o auditoría.

---

# Dominio no Depende de IAM

Assembly no depende directamente de:

```text
Keyrock

Keycloak

Auth0

Cognito

OAuth Provider

LDAP

Active Directory
```

Estos sistemas pueden implementar Authentication y Authorization.

No definen la semántica de Assembly.

---

# Keyrock

Si AURA utiliza FIWARE Keyrock para Identity Management, Keyrock
puede participar en:

* autenticación;
* usuarios;
* roles técnicos;
* OAuth2;
* autorización externa.

Assembly continúa utilizando conceptos propios:

```text
ActorId

OrganizationId

Permission
```

sin depender directamente de Keyrock.

---

# PEP Proxy

Un PEP Proxy puede impedir el acceso técnico a determinados
endpoints.

Sin embargo:

```text
PEP authorization
```

no sustituye:

```text
Domain authorization
```

ni las invariantes.

La capa de aplicación debe continuar resolviendo la capacidad
semántica requerida.

---

# OAuth Scopes

Los OAuth Scopes pueden mapearse a Permissions cuando exista una
política explícita.

Ejemplo conceptual:

```text
scope:
assembly:start
```

puede mapear a:

```text
Assembly.Start
```

La representación externa no debe reemplazar el concepto interno.

---

# JWT Claims

Claims de JWT pueden proporcionar información para resolver:

```text
ActorId

OrganizationId

Roles

Scopes
```

pero Assembly no analiza JWT directamente.

La transformación ocurre fuera del dominio.

---

# APIs

Un endpoint:

```text
POST /assemblies/{assembly_id}/start
```

puede requerir:

```text
Assembly.Start
```

pero el endpoint no define el Permission.

El Permission pertenece al modelo conceptual.

---

# GraphQL

Una mutation GraphQL como:

```text
startAssembly
```

puede mapear hacia:

```text
StartAssembly
```

y exigir:

```text
Assembly.Start
```

La tecnología de transporte no modifica el modelo.

---

# Application Service

Conceptualmente:

```text
handle(StartAssembly)
```

puede ejecutar:

1. resolver Actor;
2. resolver Organization context;
3. autorizar Assembly.Start;
4. cargar Assembly;
5. verificar ExpectedVersion;
6. ejecutar `assembly.start(...)`;
7. persistir;
8. publicar eventos según estrategia.

La Application Layer coordina.

Assembly mantiene las reglas del dominio.

---

# Command Handler

Un Command Handler no debe asumir:

```text
authenticated = authorized
```

Debe existir una decisión explícita sobre el Permission requerido.

---

# Repository

Repository no concede Permissions.

No deben existir métodos como:

```text
repository.save_if_admin(...)
```

que mezclen persistencia y autorización.

---

# Consistency Boundary

Authorization se encuentra fuera de:

```text
Assembly Consistency Boundary
```

El Aggregate no debe expandirse para incorporar:

```text
Permissions

Roles

Memberships

Sessions
```

como estado mutable interno.

---

# Versioning de Permissions

Agregar, eliminar o cambiar el significado de un Permission puede
afectar:

* Roles;
* políticas;
* APIs;
* Application Services;
* documentación;
* Security Model;
* Audit;
* tests.

Por lo tanto, la evolución debe ser controlada.

---

# Renombrado de Permission

Cambiar:

```text
Assembly.Start
```

a otro nombre no debe realizarse casualmente si existen políticas,
tokens, configuraciones o integraciones que dependen del contrato.

Debe existir una estrategia de compatibilidad.

---

# Eliminación de Permission

Un Permission no debe eliminarse mientras exista un Command
oficial que requiera dicha capacidad sin definir una alternativa.

Command y Permission deben permanecer coherentes.

---

# Nuevo Command

Agregar un nuevo Command requiere analizar si necesita un nuevo
Permission.

Ejemplo:

```text
ReopenAssembly
```

si algún día se incorpora, podría requerir:

```text
Assembly.Reopen
```

pero ninguno de estos conceptos forma parte de la versión 1.0.

---

# Commands Futuros no Autorizados

Actualmente no se definen Permissions para:

```text
Assembly.Suspend

Assembly.Resume

Assembly.Interrupt

Assembly.Abort

Assembly.Reopen

Assembly.Delete
```

porque estos comportamientos no pertenecen al modelo oficial
actual.

No deben implementarse implícitamente.

---

# Regla para Incorporar un Nuevo Permission

Un nuevo Permission debe incorporarse únicamente cuando exista una
capacidad funcional real.

Debe definir:

```text
PermissionName

Objective

ProtectedCommandOrQuery

OrganizationScope

AuthorizationSemantics

AuditRequirements
```

y analizar impacto sobre:

* Commands;
* Roles;
* Membership policies;
* APIs;
* Security Model;
* tests;
* documentación;
* integraciones.

---

# Permissions no Utilizados

No deben crearse Permissions preventivos sin comportamiento real
asociado.

Ejemplo:

```text
Assembly.SuperManage
```

carece de significado suficiente y debe evitarse.

Los Permissions deben expresar capacidades concretas.

---

# Granularidad

Debe evitarse tanto:

```text
Permission demasiado amplio
```

como:

```text
Permission innecesariamente microscópico
```

La granularidad debe seguir acciones significativas del dominio.

---

# Ejemplo de Granularidad Incorrecta

No se recomienda:

```text
Assembly.SetStartDate

Assembly.SetStartHour

Assembly.SetTimezone
```

cuando todas forman parte de una intención semántica:

```text
Assembly.Schedule
```

---

# Ejemplo de Granularidad Correcta

Se mantienen separados:

```text
Assembly.Schedule

Assembly.Convoke

Assembly.Start
```

porque representan capacidades diferentes dentro del Lifecycle.

---

# Permissions y Ubiquitous Language

Los nombres deben utilizar el mismo lenguaje conceptual que:

* Commands;
* Aggregate;
* documentación;
* Application Services.

Debe evitarse terminología técnica no perteneciente al dominio.

---

# Test de Authorization

Cada Command protegido debe poseer como mínimo escenarios de:

```text
permission granted

permission denied

wrong organization scope

expired permission

revoked permission

authorized but invalid domain state

authorized but invariant violation

authorized but concurrency conflict
```

---

# Test de Separación Authorization-Domain

Debe existir una prueba conceptual como:

```text
Actor has Assembly.Start

AssemblyStatus = Draft
```

Resultado esperado:

```text
Domain rejection
```

Esto demuestra que el Permission no anula la State Machine.

---

# Test de Permission Denied

Ejemplo:

```text
Actor lacks Assembly.Start

AssemblyStatus = Convoked
```

Resultado:

```text
PermissionDenied

Status remains Convoked

Version unchanged

AssemblyStarted not generated
```

---

# Test de Organization Scope

Ejemplo:

```text
Assembly.OrganizationId = ORG-A

Permission valid for ORG-B
```

Resultado:

```text
AuthorizationDenied
```

Aunque el nombre del Permission sea:

```text
Assembly.Start
```

---

# Test de Revocación

Un Actor cuyo Permission fue revocado no debe poder iniciar una
nueva operación protegida después de que la revocación sea
efectiva según la política de consistencia.

---

# Test de No Privilege Escalation

Ejecutar:

```text
CreateAssembly
```

no debe alterar los Permissions efectivos del Actor.

---

# Test de Archived

Incluso un Actor con todas las capacidades de Assembly no puede
ejecutar modificaciones ordinarias sobre:

```text
Archived
```

porque la inmutabilidad pertenece al dominio.

---

# Matriz de Escenarios Obligatorios

Como mínimo deben probarse:

```text
CreateAssembly con Assembly.Create;

CreateAssembly sin Assembly.Create;

ScheduleAssembly con Assembly.Schedule;

ScheduleAssembly sin Assembly.Schedule;

RescheduleAssembly con Assembly.Reschedule;

ConvokeAssembly con Assembly.Convoke;

RenameAssembly con Assembly.Rename;

ChangeAssemblyType con Assembly.ChangeType;

ChangeAssemblyPurpose con Assembly.ChangePurpose;

ChangeAssemblyDescription con Assembly.ChangeDescription;

ChangeAssemblyModality con Assembly.ChangeModality;

ChangeAssemblyLocation con Assembly.ChangeLocation;

UpdateAssemblyConvocation con Assembly.UpdateConvocation;

UpdateAssemblyRules con Assembly.UpdateRules;

UpdateAssemblyExecutionConditions con
Assembly.UpdateExecutionConditions;

StartAssembly con Assembly.Start;

StartAssembly sin Assembly.Start;

CompleteAssembly con Assembly.Complete;

CancelAssembly con Assembly.Cancel;

ArchiveAssembly con Assembly.Archive;

Permission correcto en Organization incorrecta;

Permission expirado;

Permission revocado;

Permission válido con estado inválido;

Permission válido con Guard fallido;

Permission válido con invariante violada;

Permission válido con ExpectedVersion obsoleta;

Permission denegado no modifica Version;

Permission denegado no produce Domain Event;

Archived permanece inmutable aunque el Actor tenga Permission.
```

Los escenarios completos se documentan en:

```text
DOMAIN-006M-Test-Scenarios.md
```

---

# Permissions y Performance

La autorización puede necesitar optimizaciones para evitar
latencias innecesarias.

Sin embargo:

* una caché no puede otorgar permisos revocados indefinidamente;
* un permiso obsoleto no puede utilizarse como autoridad
  permanente;
* una optimización no puede saltarse Organization scope;
* una optimización no puede eliminar controles de operaciones
  sensibles.

Las reglas específicas de rendimiento se desarrollan en:

```text
DOMAIN-006N-Performance-Rules.md
```

---

# Permissions y Security Model

Los aspectos relacionados con:

* autenticación;
* identidad;
* sesión;
* tokens;
* revocación;
* threat model;
* privilege escalation;
* audit de seguridad;
* service accounts;

se desarrollan en:

```text
DOMAIN-006O-Security-Model.md
```

Este documento mantiene exclusivamente el contrato conceptual de
capacidades requerido por Assembly.

---

# Permissions y Extension Points

Nuevos Permissions pueden añadirse como consecuencia de nuevas
capacidades oficiales.

Las extensiones deben respetar:

```text
DOMAIN-006P-Extension-Points.md
```

No pueden introducirse Permissions que violen el límite del
Aggregate.

---

# Relación con Commands

Cada Command de escritura debe declarar explícitamente el
Permission requerido.

La relación oficial se encuentra en:

```text
DOMAIN-006C-Commands.md
```

y este documento.

No debe existir un Command protegido cuya política de
autorización sea implícita o desconocida.

---

# Relación con Domain Events

Los Domain Events definidos en:

```text
DOMAIN-006D-Domain-Events.md
```

representan hechos posteriores a:

```text
Authentication

Authorization

Domain Validation
```

Los eventos no realizan autorización retroactiva.

---

# Relación con Invariants

Las reglas definidas en:

```text
DOMAIN-006E-Invariants.md
```

poseen autoridad sobre la validez del estado interno.

Permissions nunca pueden anularlas.

---

# Relación con Repository Contract

El Repository definido en:

```text
DOMAIN-006G-Repository-Contract.md
```

no debe implementar reglas de autorización como parte de su
responsabilidad de persistencia.

Authorization debe resolverse antes de persistir cambios.

---

# Relación con Versioning

El modelo de Versioning definido en:

```text
DOMAIN-006I-Versioning.md
```

continúa aplicándose después de que Authorization concede una
capacidad.

Permission Granted no significa ExpectedVersion válida.

---

# Relación con Consistency Boundary

El límite definido en:

```text
DOMAIN-006J-Consistency-Boundary.md
```

no incluye Roles, Memberships ni Permissions como estado interno
mutable de Assembly.

---

# Relación con Integration Events

Los Integration Events no conceden Permissions.

Una integración que origine una intención debe utilizar una
identidad autorizable y pasar por las mismas reglas de acceso.

---

# Relación con Read Model

Los Read Models definidos en:

```text
DOMAIN-006L-Read-Model.md
```

pueden aplicar:

```text
Assembly.Read

Assembly.List
```

y otras políticas de visibilidad cuando corresponda.

La lectura no modifica el Write Model.

---

# Relación con Test Scenarios

Todos los Permissions deben contar con escenarios positivos y
negativos en:

```text
DOMAIN-006M-Test-Scenarios.md
```

Debe probarse tanto Authorization como su separación del dominio.

---

# Relación con Security Model

Las amenazas y controles técnicos asociados se documentan en:

```text
DOMAIN-006O-Security-Model.md
```

Este documento define qué capacidad se necesita.

El Security Model define cómo proteger de forma segura la
resolución y ejecución de dicha capacidad.

---

# Independencia Tecnológica

El modelo conceptual de Permissions no depende de:

```text
Keyrock

Keycloak

OAuth2

OpenID Connect

JWT

LDAP

Active Directory

Auth0

Cognito

HTTP

REST

GraphQL

FastAPI

Django

React

Next.js

MongoDB

PostgreSQL

Redis

Kafka

FIWARE

NGSI-LD
```

Estas tecnologías pueden implementar mecanismos de autorización.

No definen los Permissions de Assembly.

---

# Implementación Tecnológica

Una futura implementación puede mapear:

```text
Assembly.Start
```

a:

* OAuth Scope;
* IAM Permission;
* RBAC Permission;
* ABAC Policy;
* Keyrock Role;
* API Gateway Policy.

El mapeo pertenece a Infrastructure/Application.

El concepto de dominio permanece estable.

---

# RBAC

El modelo es compatible con:

```text
Role-Based Access Control
```

La relación puede ser:

```text
Role
    │
    ▼
Permission
```

Los Roles permanecen administrados por su propio Aggregate y
contexto.

---

# ABAC

El modelo también puede utilizar:

```text
Attribute-Based Access Control
```

donde una política evalúe atributos como:

```text
Actor

Organization

Permission

Resource

Context
```

ABAC no modifica la semántica del Permission requerido.

---

# Policy-Based Authorization

Una implementación puede utilizar políticas declarativas.

Ejemplo conceptual:

```text
Allow Assembly.Start
when:
    Actor has active organizational authority
    AND Resource.OrganizationId matches
```

La política resuelve Authorization.

Assembly continúa validando el dominio.

---

# Capability-Based Security

El Permission también puede materializarse mediante capacidades
seguras cuando la arquitectura lo requiera.

Sin embargo, la capacidad técnica debe mapear inequívocamente al
Permission conceptual.

---

# Reglas de Diseño

El modelo de Permissions de Assembly debe garantizar:

* separación entre Authentication, Authorization y Domain;
* Permission como capacidad explícita;
* nombres utilizando lenguaje ubicuo;
* Organization scope explícito;
* deny by default;
* least privilege;
* ausencia de Roles hardcoded dentro de Assembly;
* ausencia de Permissions dentro del estado del Aggregate;
* ausencia de credenciales dentro del Aggregate;
* Permission Granted no anula State Machine;
* Permission Granted no anula Guards;
* Permission Granted no anula Invariants;
* Permission Granted no anula Versioning;
* Permission Denied no modifica Assembly;
* Permission Denied no produce Domain Events de éxito;
* soporte para Audit;
* soporte para delegación externa;
* compatibilidad con RBAC;
* compatibilidad con ABAC;
* independencia tecnológica.

---

# Restricciones

No está permitido:

* modificar Assembly sin el Permission requerido cuando la
  operación se encuentre protegida;
* asumir que un Actor autenticado está autorizado;
* asumir que un Role equivale a un Permission;
* hardcodear Roles concretos dentro de Assembly;
* almacenar Permissions como estado mutable interno de Assembly;
* almacenar credenciales dentro de Assembly;
* permitir que un Permission anule invariantes;
* permitir que un Permission cree transiciones no definidas;
* permitir que un Permission omita Guards;
* permitir que un Permission ignore ExpectedVersion;
* permitir que un Permission de una Organization opere
  automáticamente sobre otra;
* considerar que el creador posee todas las capacidades;
* considerar que un System Actor posee todos los Permissions;
* considerar que un administrador puede evadir el dominio;
* producir Domain Events de éxito después de AuthorizationDenied;
* incrementar Version después de AuthorizationDenied;
* conceder Permissions como efecto secundario de Commands de
  Assembly;
* modificar Roles o Memberships desde Assembly;
* depender directamente de un proveedor IAM;
* incorporar OAuth scopes como sustituto del lenguaje ubicuo sin
  traducción;
* permitir que sistemas externos modifiquen el Aggregate
  directamente;
* implementar nuevos Permissions sin comportamiento funcional
  oficial asociado.

---

# Compatibilidad Arquitectónica

El modelo de Permissions de Assembly es compatible con:

* Domain-Driven Design;
* Tactical DDD;
* Clean Architecture;
* Hexagonal Architecture;
* SOLID;
* CQRS;
* Event-Driven Architecture;
* Event Sourcing;
* RBAC;
* ABAC;
* Policy-Based Authorization;
* Principle of Least Privilege;
* Defense in Depth;
* Zero Trust compatible;
* arquitectura distribuida;
* interoperabilidad mediante contratos.

---

# Principios Arquitectónicos

Permissions mantiene los siguientes principios:

```text
Authentication
        ≠
Authorization
        ≠
Domain Validation
```

Además:

```text
Role
        ≠
Permission
```

y:

```text
Permission Granted
        ≠
Operation Valid
```

El modelo utiliza una autorización externa al Aggregate mientras
Assembly mantiene autoridad absoluta sobre sus propias
invariantes y transiciones.

---

# Definición de Éxito

El modelo de Permissions del Aggregate **Assembly** define de
forma oficial las capacidades necesarias para solicitar
operaciones sobre una reunión dentro del ecosistema AURA.

Cada operación protegida posee un Permission semántico y
explícito, asociado al lenguaje ubicuo del dominio y evaluado
dentro del contexto organizacional correspondiente.

Los Permissions determinan quién puede intentar ejecutar un
Command, pero nunca determinan por sí solos que la operación sea
válida.

Assembly conserva autoridad sobre:

* State Machine;
* Guards;
* invariantes;
* Lifecycle;
* consistencia;
* Versioning;
* comportamiento del dominio.

Un Actor que posea un Permission puede solicitar una operación,
pero Assembly debe rechazarla si el estado, Guards, invariantes o
versión no permiten su ejecución.

Un Actor que no posea el Permission requerido no puede provocar
una modificación protegida. El rechazo no modifica el Aggregate,
no incrementa Version y no genera Domain Events de éxito.

El modelo mantiene separación explícita entre Citizen,
Membership, Role, Permission y Assembly. Los Roles pueden conceder
capacidades mediante políticas externas, pero Assembly no
hardcodea cargos organizacionales ni administra asociaciones de
autorización.

La autorización permanece limitada por OrganizationId, evitando
que capacidades concedidas en una Organization otorguen acceso
implícito sobre Assemblies de otra organización.

Authentication, OAuth, JWT, IAM, Keyrock, PEP Proxy, RBAC, ABAC y
otros mecanismos técnicos pueden implementar la seguridad del
sistema, pero no forman parte del estado ni del comportamiento
interno del Aggregate.

De esta forma, Permissions establece una frontera de autorización
explícita, auditable, extensible y tecnológicamente independiente,
preservando el principio de mínimo privilegio, la separación de
responsabilidades y la integridad conceptual del Aggregate
Assembly dentro de la arquitectura Domain-Driven Design de AURA.
