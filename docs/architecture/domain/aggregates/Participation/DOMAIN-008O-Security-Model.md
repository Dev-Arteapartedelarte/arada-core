# DOMAIN-008O — Participation Security Model

Versión: 1.0

Estado:
Oficial

Proyecto:
AURA Core

Bounded Context:
Participation Management

Aggregate:
Participation

Autor:
ARADA

Documentos Relacionados:

- DOMAIN-008-Aggregate.md
- DOMAIN-008C-Commands.md
- DOMAIN-008D-Domain-Events.md
- DOMAIN-008E-Invariants.md
- DOMAIN-008F-Permissions.md
- DOMAIN-008G-Repository-Contract.md
- DOMAIN-008I-Versioning.md
- DOMAIN-008J-Consistency-Boundary.md
- DOMAIN-008K-Integration-Events.md
- DOMAIN-008L-Read-Model.md
- DOMAIN-008M-Test-Scenarios.md
- DOMAIN-008N-Performance-Rules.md
- CORE-016-Dependency-Rules.md

---

# Objetivo

Definir el modelo oficial de seguridad del Aggregate
**Participation**.

El Security Model establece las reglas conceptuales que
protegen:

- identidad;
- estado;
- Lifecycle;
- State Machine;
- Invariants;
- Commands;
- Permissions;
- Version;
- Consistency Boundary;
- persistencia;
- Domain Events;
- Integration Events;
- Read Models;
- información asociada a Participation.

La seguridad debe preservar las reglas ya definidas por el
Aggregate sin introducir comportamiento de dominio adicional.

---

# Principios

El Security Model debe cumplir los siguientes principios.

- toda modificación requiere autorización cuando corresponda;
- la autorización no sustituye las Invariants;
- las Invariants no sustituyen la autorización;
- todo cambio debe ingresar mediante comportamiento válido del
  Aggregate;
- el Aggregate Root protege su estado interno;
- ParticipationId permanece inmutable;
- OrganizationId permanece inmutable;
- Version no puede modificarse directamente;
- el Consistency Boundary no puede evitarse;
- el Repository no constituye un mecanismo para evitar las reglas
  del dominio;
- los Read Models son de solo lectura;
- los Integration Events exponen únicamente información necesaria;
- otros Aggregates permanecen fuera del Consistency Boundary;
- las optimizaciones no pueden debilitar las reglas de seguridad.

---

# Principio Fundamental

Debe mantenerse:

```text
Authorization

+

Domain Validation

+

Consistency Protection

=

Valid Modification
```

No debe asumirse:

```text
Authorization

=

Valid Domain Operation
```

Un actor autorizado puede solicitar una operación que el dominio
deba rechazar.

---

# Capas de Protección

Una modificación de Participation debe atravesar las protecciones
correspondientes.

```text
Actor

↓

Permission

↓

Command

↓

Participation Aggregate

↓

State Machine

↓

Invariants

↓

Version Check

↓

Persistence
```

Cada nivel conserva una responsabilidad distinta.

---

# Aggregate Root

Participation es la autoridad sobre su estado interno.

Debe mantenerse:

```text
External Actor

↓

Command

↓

Participation Aggregate Root

↓

State Change
```

No:

```text
External Actor

↓

Direct State Mutation
```

---

# Encapsulamiento

El estado interno del Aggregate no puede modificarse directamente
desde componentes externos.

Esto protege:

- ParticipationStatus;
- ParticipationType;
- Context;
- Metadata;
- Lifecycle timestamps;
- Version;
- referencias del Aggregate.

Toda modificación debe respetar los comportamientos definidos por
Participation.

---

# Identidad

ParticipationId identifica de forma única al Aggregate.

Una vez creado:

```text
ParticipationId

=

Immutable
```

No puede:

- modificarse;
- sustituirse;
- reutilizarse para representar otra Participation;
- alterarse mediante Metadata;
- alterarse mediante persistencia directa.

---

# OrganizationId

OrganizationId establece la pertenencia organizacional de
Participation.

Una vez establecida:

```text
OrganizationId

=

Immutable
```

No puede utilizarse una operación ordinaria para transferir una
Participation entre Organizations.

No puede modificarse mediante:

- Metadata;
- cambios de Context;
- operaciones de Repository;
- proyecciones;
- Integration Events.

---

# Permissions

Las Permissions oficiales están definidas en:

```text
DOMAIN-008F-Permissions.md
```

El Security Model debe respetar esas Permissions sin crear
permisos alternativos.

Debe mantenerse:

```text
Requested Operation

↓

Required Permission

↓

Granted or Denied
```

---

# Permission Granted

Una Permission concedida permite que la intención continúe hacia
las reglas del dominio.

```text
Permission Granted

↓

Command

↓

Domain Validation
```

No garantiza que la operación sea válida.

---

# Permission Denied

Cuando la Permission requerida es denegada:

```text
Permission Denied

↓

No Domain Modification
```

Debe mantenerse:

```text
State Unchanged

Version Unchanged

No Success Domain Event
```

---

# Separación entre Permission e Invariant

Permission responde conceptualmente:

```text
May this actor request this operation?
```

Invariant responde:

```text
May the Aggregate exist in the resulting state?
```

Son responsabilidades diferentes.

Debe mantenerse:

```text
Permission Granted

+

Invariant Violation

=

Rejected
```

---

# Separación entre Permission y State Machine

Una Permission concedida no permite ejecutar una transición
prohibida.

Ejemplo conceptual.

```text
Participation.Complete = Granted

ParticipationStatus = Registered
```

Si la State Machine no permite la transición solicitada:

```text
Rejected
```

La Permission no modifica la State Machine.

---

# Separación entre Permission y Lifecycle

El Lifecycle continúa determinando la evolución válida de
Participation.

La autorización no puede crear transiciones alternativas.

Debe mantenerse:

```text
Authorized Actor

↓

Existing Lifecycle Rules
```

No:

```text
Authorized Actor

↓

Bypass Lifecycle
```

---

# Commands

Los Commands representan intenciones de modificación.

Un Command no constituye autorización por sí mismo.

Debe mantenerse:

```text
Command

≠

Permission
```

y:

```text
Command

≠

Successful Modification
```

El Command debe atravesar las reglas correspondientes antes de
producir un cambio válido.

---

# RegisterParticipation

El registro de una Participation debe respetar:

- Permission correspondiente;
- identidad válida;
- OrganizationId válido;
- ParticipationType válido;
- Context válido;
- Invariants de creación.

Si alguna condición requerida falla:

```text
No Participation Created
```

---

# ActivateParticipation

La activación debe respetar:

```text
Participation.Activate

+

Valid Lifecycle Transition

+

Invariants
```

Solo entonces puede producirse:

```text
ParticipationActivated
```

---

# CompleteParticipation

La finalización debe respetar:

```text
Participation.Complete

+

Valid Lifecycle Transition

+

Invariants
```

La autorización no permite completar una Participation desde un
estado no permitido.

---

# WithdrawParticipation

El retiro debe respetar:

```text
Participation.Withdraw

+

Valid Lifecycle Transition

+

Invariants
```

Una operación no autorizada o inválida no modifica el Aggregate.

---

# InvalidateParticipation

La invalidación debe respetar:

```text
Participation.Invalidate

+

Valid Lifecycle Transition

+

Invariants
```

La capacidad de invalidar no elimina las restricciones del
Aggregate.

---

# ArchiveParticipation

El archivado debe respetar:

```text
Participation.Archive

+

Valid Lifecycle Transition

+

Invariants
```

Una vez alcanzado Archived, deben preservarse las reglas
establecidas para dicho estado.

---

# ChangeParticipationType

La modificación de ParticipationType requiere la Permission
correspondiente y debe respetar las reglas del Aggregate.

No puede utilizarse para:

- modificar ParticipationId;
- modificar OrganizationId;
- modificar Version;
- evitar el Lifecycle;
- modificar otros Aggregates.

---

# ChangeParticipationContext

La modificación del Context requiere la Permission correspondiente.

El cambio de Context no permite:

- transferir la Participation a otra Organization;
- modificar directamente un Assembly;
- modificar directamente una Proposal;
- modificar directamente un Citizen;
- ampliar el Consistency Boundary.

---

# UpdateParticipationMetadata

La Metadata no constituye un canal alternativo para modificar
atributos protegidos.

No puede utilizarse para modificar:

```text
ParticipationId

OrganizationId

ParticipationStatus

Version
```

ni para evitar reglas del Lifecycle, State Machine o Invariants.

---

# Invariants

Las Invariants definidas en:

```text
DOMAIN-008E-Invariants.md
```

constituyen reglas obligatorias del Aggregate.

No existe actor autorizado para producir deliberadamente un estado
que viole una Invariant.

Debe mantenerse:

```text
Any Actor

↓

Invariant Validation
```

---

# Estado

ParticipationStatus solo puede cambiar mediante las transiciones
oficiales.

No puede modificarse mediante:

- escritura directa;
- Metadata;
- Repository;
- Read Model;
- Integration Event;
- importación que evite el comportamiento del dominio.

---

# Archived

Cuando Participation alcanza:

```text
Archived
```

deben respetarse las restricciones definidas por el Lifecycle y la
State Machine.

Una Permission no convierte Archived en un estado libremente
mutable.

---

# Lifecycle Timestamps

Los timestamps del Lifecycle representan hechos del dominio.

Ejemplos:

```text
CreatedAt

StartedAt

CompletedAt

WithdrawnAt

InvalidatedAt

ArchivedAt
```

No pueden modificarse arbitrariamente para alterar la historia del
Aggregate.

---

# Historia Temporal

Los hechos temporales ya ocurridos deben preservarse.

Ejemplo:

```text
CreatedAt = T1

StartedAt = T2

CompletedAt = T3
```

Una operación posterior no debe reescribir esos valores para
representar una historia diferente.

---

# Version

Version protege la evolución concurrente del Aggregate.

Debe mantenerse:

```text
Version

=

Controlled by Aggregate Evolution
```

No puede ser:

- establecida por un actor;
- modificada mediante Metadata;
- alterada directamente por una integración;
- sobrescrita para evitar un conflicto;
- reiniciada;
- disminuida.

---

# Concurrencia

La seguridad contra modificaciones concurrentes depende del
Versioning definido para Participation.

Debe mantenerse:

```text
ExpectedVersion

=

PersistedVersion
```

antes de confirmar una actualización.

Si no coinciden:

```text
ConcurrencyConflictError
```

---

# Protección contra Lost Update

No debe permitirse:

```text
Process A

Version 8

↓

Save Version 9
```

seguido por:

```text
Process B

Stale Version 8

↓

Overwrite Version 9
```

El segundo proceso debe ser rechazado mediante el mecanismo de
concurrencia definido.

---

# Repository

El Repository debe respetar el contrato definido en:

```text
DOMAIN-008G-Repository-Contract.md
```

No puede utilizarse como mecanismo para evitar:

- Commands;
- Permissions;
- State Machine;
- Invariants;
- Versioning;
- Consistency Boundary.

---

# Escritura Directa

No forma parte del modelo válido:

```text
Repository

↓

Direct Protected State Mutation
```

El Repository persiste el resultado del comportamiento del
Aggregate.

No define comportamiento alternativo.

---

# Recuperación

La recuperación de Participation debe preservar exactamente:

- identidad;
- estado;
- Version;
- información requerida por el Aggregate.

La recuperación no debe generar una modificación.

Debe mantenerse:

```text
Repository Read

↓

Version Unchanged

No New Domain Event
```

---

# Rehidratación

La rehidratación reconstruye un estado previamente persistido.

No debe:

- ejecutar Commands;
- reevaluar Permissions como una nueva operación;
- incrementar Version;
- generar nuevos Domain Events;
- modificar timestamps históricos.

---

# Consistency Boundary

El límite de consistencia definido en:

```text
DOMAIN-008J-Consistency-Boundary.md
```

constituye también un límite de protección.

Debe mantenerse:

```text
Participation

↓

Own Consistency Boundary
```

Otros Aggregates no pueden incorporarse al Boundary para permitir
modificaciones indirectas.

---

# Referencias Externas

Participation puede mantener referencias mediante identificadores.

Ejemplos:

```text
OrganizationId

CitizenId

MembershipId

TerritoryId

AssemblyId

ProposalId
```

Estas referencias no otorgan autoridad sobre el Aggregate
referenciado.

---

# Protección de Otros Aggregates

Una operación sobre Participation no puede modificar directamente:

```text
Organization

Citizen

Membership

Role

Territory

Assembly

Proposal
```

Cada Aggregate mantiene su propio:

- Aggregate Root;
- Permissions;
- Invariants;
- Version;
- Consistency Boundary.

---

# Aislamiento Organizacional

Participation pertenece a una Organization determinada por:

```text
OrganizationId
```

Las operaciones deben respetar las reglas de autorización y
aislamiento organizacional definidas por AURA.

Una Participation perteneciente a una Organization no debe quedar
expuesta a modificaciones provenientes de otra Organization sin la
capacidad correspondiente definida por el modelo de Permissions.

---

# Domain Events

Los Domain Events representan hechos válidos ya producidos por el
Aggregate.

No deben utilizarse como mecanismo para ejecutar modificaciones
externas sobre Participation.

Debe mantenerse:

```text
Valid Domain Change

↓

Domain Event
```

No:

```text
Forged Domain Event

↓

Direct Aggregate Mutation
```

---

# Integridad de Domain Events

Un Domain Event debe corresponder a una modificación válida.

No debe existir un evento de éxito cuando:

- la Permission fue denegada;
- la State Machine rechazó la transición;
- una Invariant fue violada;
- ocurrió un conflicto de Version;
- la modificación no fue válida.

---

# Integration Events

Los Integration Events definidos en:

```text
DOMAIN-008K-Integration-Events.md
```

constituyen contratos de comunicación externa.

No otorgan a los consumidores autoridad directa sobre
Participation.

Debe mantenerse:

```text
Integration Event

↓

External Information
```

No:

```text
Integration Event

↓

Direct Participation Mutation
```

---

# Exposición Mínima

Los Integration Events deben contener únicamente la información
necesaria para representar el hecho publicado.

No deben exponer automáticamente:

```text
Complete Aggregate Internal State
```

Esto preserva:

- encapsulamiento;
- privacidad;
- estabilidad contractual;
- independencia entre Bounded Contexts.

---

# EventId

EventId permite identificar de forma única un Integration Event.

Esto permite soportar:

- trazabilidad;
- idempotencia;
- detección de duplicados.

La recepción repetida del mismo EventId no representa un nuevo
hecho del dominio.

---

# CorrelationId

Cuando exista dentro del contrato correspondiente,
CorrelationId puede utilizarse para relacionar operaciones
distribuidas.

No debe utilizarse como sustituto de:

```text
ParticipationId
```

ni de:

```text
EventId
```

---

# CausationId

Cuando exista dentro del contrato correspondiente,
CausationId permite preservar la relación causal entre eventos u
operaciones.

No modifica el estado del Aggregate.

---

# Outbox

Cuando se utilice el mecanismo Outbox consolidado, la seguridad del
flujo debe preservar:

```text
Confirmed Aggregate Change

↓

Outbox Record

↓

Integration Event
```

No debe publicarse como hecho confirmado una modificación que no
haya sido confirmada correctamente.

---

# Reintentos de Publicación

Un reintento de publicación no debe ejecutar nuevamente el
comportamiento de Participation.

Debe mantenerse:

```text
Existing Outbox Record

↓

Retry Publication
```

No:

```text
Retry Publication

↓

Execute Command Again
```

---

# Read Models

Los Read Models definidos en:

```text
DOMAIN-008L-Read-Model.md
```

son de solo lectura.

No pueden utilizarse para modificar Participation.

Debe mantenerse:

```text
Participation Read Model

↓

Query
```

No:

```text
Participation Read Model

↓

Write Aggregate State
```

---

# Fuente de Verdad

Los Read Models no son fuente de verdad para operaciones de
escritura.

Una proyección puede encontrarse temporalmente desactualizada debido
a consistencia eventual.

Por ello no debe sustituir las reglas del Write Model.

---

# Exposición de Read Models

Cada Read Model debe exponer únicamente la información autorizada
para su consumidor.

Cuando corresponda, una proyección puede:

- excluir información;
- ocultar atributos;
- anonimizar información;
- limitar información sensible.

Estas medidas no modifican el Aggregate.

---

# Datos Personales

La información asociada a ciudadanos debe exponerse únicamente
cuando sea necesaria y autorizada.

La existencia de una referencia:

```text
CitizenId
```

no implica que Participation deba contener o exponer el perfil
completo del Citizen.

---

# Datos Sensibles

Los datos sensibles no deben incorporarse innecesariamente en:

- Metadata;
- Integration Events;
- Read Models;
- logs;
- mensajes externos.

El modelo debe preservar el principio de exposición mínima.

---

# Metadata

Metadata debe tratarse como información perteneciente al contexto
definido por Participation.

No puede convertirse en un contenedor libre utilizado para evitar
las restricciones del Aggregate.

No debe utilizarse para duplicar o sobrescribir atributos
protegidos.

---

# Entrada de Datos

Toda información utilizada para construir o modificar Participation
debe respetar las validaciones correspondientes antes de producir
un estado válido.

Debe mantenerse:

```text
Input

↓

Validation

↓

Domain Behavior
```

No:

```text
Input

↓

Trusted Automatically

↓

Direct Persistence
```

---

# Datos Externos

Los datos provenientes de integraciones externas no poseen
autoridad especial sobre el Aggregate.

Deben atravesar las mismas reglas conceptuales que cualquier otra
intención de modificación.

---

# Importaciones

Las importaciones no constituyen una excepción de seguridad.

Cada Participation incorporada debe respetar:

- identidad;
- OrganizationId;
- Permissions cuando correspondan;
- Invariants;
- Lifecycle;
- Versioning;
- Consistency Boundary.

---

# Operaciones Masivas

Una operación masiva no elimina la evaluación individual de
seguridad.

Debe mantenerse:

```text
Bulk Operation

↓

Participation A

Own Authorization
Own Invariants
Own Version
```

```text
Participation B

Own Authorization
Own Invariants
Own Version
```

Cada Aggregate conserva sus propias reglas.

---

# Bulk Update

No debe utilizarse una operación masiva para modificar directamente
estado protegido.

No forma parte del modelo válido:

```text
Bulk Update

↓

Set ParticipationStatus
```

evitando el comportamiento del Aggregate.

---

# Seguridad y Performance

Las reglas definidas en:

```text
DOMAIN-008N-Performance-Rules.md
```

no pueden utilizarse para reducir controles de seguridad.

Debe mantenerse:

```text
Performance Optimization

≠

Security Bypass
```

---

# Cache

Una caché no constituye una fuente de autoridad para modificar
Participation.

Los datos almacenados en caché no pueden utilizarse para evitar:

- Version Check;
- Permissions;
- Invariants;
- State Machine.

---

# Logs

Los mecanismos de Logging pertenecen a Infrastructure.

Los logs no deben utilizarse como fuente de verdad del Aggregate.

La información registrada debe evitar exposición innecesaria de
datos protegidos.

---

# Trazabilidad

Las operaciones relevantes deben poder relacionarse conceptualmente
con:

```text
ParticipationId

↓

Command

↓

Domain Event

↓

AggregateVersion
```

y, cuando exista integración externa:

```text
Domain Event

↓

Integration Event

↓

EventId
```

Esto permite preservar trazabilidad sin incorporar comportamiento
de auditoría dentro del Aggregate.

---

# Auditoría

El Aggregate Participation no debe asumir responsabilidades
pertenecientes al Aggregate Audit.

Participation produce hechos del dominio.

Audit mantiene su propio modelo y Consistency Boundary.

Debe mantenerse:

```text
Participation

↓

Domain / Integration Events

↓

Audit
```

sin incorporar Audit dentro del Aggregate Participation.

---

# Protección contra Bypass

Ningún mecanismo externo puede considerar válida una modificación
que evite las reglas oficiales.

No están permitidos conceptualmente:

```text
Direct Database Update
```

```text
Direct Status Mutation
```

```text
Direct Version Mutation
```

```text
Read Model Writeback
```

```text
Integration Event Writeback
```

```text
Metadata Protected Field Override
```

```text
Repository Lifecycle Bypass
```

---

# Protección contra Escalamiento de Permisos

Una Permission específica no concede automáticamente otras
Permissions.

Debe mantenerse:

```text
Participation.Read

≠

Participation.Update
```

```text
Participation.Update

≠

Participation.Invalidate
```

```text
Participation.Invalidate

≠

Participation.Archive
```

Cada capacidad conserva el significado definido en
`DOMAIN-008F-Permissions.md`.

---

# Protección de Estados Terminales

Los estados terminales definidos por el Lifecycle deben permanecer
protegidos.

Una Permission administrativa no implica capacidad para crear una
transición inexistente.

Debe mantenerse:

```text
Terminal State

↓

Lifecycle Rules
```

---

# Protección de Version

No debe permitirse:

```text
Force Version
```

```text
Reset Version
```

```text
Decrease Version
```

```text
Reuse Version
```

```text
Ignore Version Conflict
```

Version representa la evolución monotónica del Aggregate.

---

# Protección de Persistencia

La persistencia debe mantener coherentemente:

```text
ParticipationId

State

Version

Lifecycle Information
```

Una escritura parcial que deje el Aggregate en estado inválido no
puede considerarse una persistencia válida.

---

# Fallo de Persistencia

Cuando la persistencia falla:

```text
PersistenceFailure
```

no debe informarse la modificación como confirmada.

No debe publicarse como hecho confirmado un cambio cuya
persistencia no haya sido completada.

---

# Protección contra Replay Incorrecto

Replay no debe tratar eventos históricos como nuevas solicitudes.

Debe mantenerse:

```text
Historical Event

↓

Rehydrate
```

No:

```text
Historical Event

↓

New Command

↓

New Domain Event
```

---

# Seguridad de Proyecciones

Las proyecciones deben derivarse de hechos válidos.

No pueden crear nuevos hechos del dominio.

Debe mantenerse:

```text
Domain Event

↓

Projection

↓

Read Model
```

No:

```text
Read Model

↓

Domain State Mutation
```

---

# Seguridad entre Bounded Contexts

Los consumidores externos deben permanecer desacoplados del estado
interno de Participation.

La comunicación entre Bounded Contexts no permite compartir estado
mutable del Aggregate.

Debe mantenerse:

```text
Participation

↓

Integration Contract

↓

Consumer
```

---

# Independencia Tecnológica

El Security Model no depende de una tecnología específica.

No define como parte del dominio:

```text
OAuth2

JWT

Keyrock

PEP Proxy

PostgreSQL

MongoDB

Redis

Kafka

RabbitMQ
```

Las tecnologías concretas pertenecen a capas externas y deben
implementar las reglas conceptuales establecidas por AURA.

---

# Autenticación

La autenticación determina la identidad del actor que interactúa
con el sistema.

No constituye por sí misma autorización.

Debe mantenerse:

```text
Authenticated

≠

Authorized
```

La autorización continúa determinada por las Permissions
correspondientes.

---

# Autorización

La autorización determina si el actor posee la Permission requerida
para solicitar una operación.

Debe mantenerse:

```text
Actor

↓

Permission Evaluation

↓

Granted / Denied
```

La autorización no modifica el dominio para hacer válida una
operación inválida.

---

# Integridad

La integridad de Participation requiere que todo estado confirmado
sea resultado de una operación válida.

Debe preservarse:

```text
Valid Identity

+

Valid State

+

Valid Lifecycle

+

Valid Invariants

+

Valid Version

=

Consistent Participation
```

---

# Confidencialidad

La información expuesta por Participation y sus representaciones
derivadas debe limitarse a consumidores autorizados.

La existencia de información en el Aggregate no implica que deba
exponerse íntegramente en:

- APIs;
- Read Models;
- Integration Events;
- logs;
- interfaces externas.

---

# Disponibilidad

Las medidas destinadas a mejorar disponibilidad no pueden
sacrificar integridad.

Debe mantenerse:

```text
Availability

+

Domain Integrity
```

No:

```text
Availability

↓

Skip Domain Rules
```

---

# Testabilidad

El Security Model debe permitir verificar como mínimo:

```text
Authorized Command

Unauthorized Command

Permission Granted + Valid Domain Operation

Permission Granted + Invalid State Transition

Permission Granted + Invariant Violation

Cross Organization Access Denied

Immutable ParticipationId

Immutable OrganizationId

Protected ParticipationStatus

Protected Version

Protected Lifecycle Timestamps

Metadata Cannot Override Protected Fields

Repository Cannot Bypass Aggregate

Read Model Cannot Modify Aggregate

Integration Event Cannot Modify Aggregate

ConcurrencyConflict Protection

No Silent Overwrite

No Domain Event on Rejected Operation

No Integration Event before Confirmed Change

External Aggregate Remains Unchanged

Archived State Protection

Import Preserves Security Rules

Bulk Operation Preserves Individual Security

Rehydration Does Not Execute New Behavior

Replay Does Not Generate New Commands

Performance Optimization Does Not Bypass Security
```

Los escenarios correspondientes se verifican mediante:

```text
DOMAIN-008M-Test-Scenarios.md
```

---

# Matriz de Protección

```text
Element                     Protection

ParticipationId             Immutable

OrganizationId              Immutable

ParticipationStatus         State Machine

ParticipationType           Aggregate Rules

Context                     Aggregate Rules

Metadata                    Aggregate Rules

Lifecycle Timestamps        Lifecycle

Version                     Versioning

Commands                    Permissions + Domain Rules

Domain Events               Valid Domain Changes

Integration Events          Confirmed Domain Facts

Read Models                 Read Only

External Aggregates         Separate Boundaries

Repository                  Aggregate Persistence Contract
```

---

# Matriz de Autoridad

```text
Concern                     Authority

State Mutation              Participation Aggregate

State Transition            Participation State Machine

Invariant Validation        Participation Aggregate

Permission Evaluation       Authorization Model

Version Evolution           Participation Aggregate

Concurrency Detection       Repository Contract

Persistence                 Participation Repository

Read Projection             Read Model

External Communication      Integration Events

External Aggregate State    External Aggregate
```

---

# Matriz de Acceso

```text
Operation                    Security Requirement

RegisterParticipation        Corresponding Permission

ActivateParticipation        Participation.Activate

CompleteParticipation        Participation.Complete

WithdrawParticipation        Participation.Withdraw

InvalidateParticipation      Participation.Invalidate

ArchiveParticipation         Participation.Archive

ChangeParticipationType      Corresponding Permission

ChangeParticipationContext   Corresponding Permission

UpdateParticipationMetadata  Corresponding Permission

Read Participation           Participation.Read
```

Las denominaciones exactas de Permissions permanecen definidas por:

```text
DOMAIN-008F-Permissions.md
```

Este documento no crea Permissions adicionales.

---

# Amenazas Conceptuales

El modelo debe impedir conceptualmente:

- modificación directa del estado;
- modificación directa de Version;
- modificación de ParticipationId;
- modificación de OrganizationId;
- transición inválida de estado;
- evasión de Permissions;
- evasión de Invariants;
- evasión de State Machine;
- evasión del Lifecycle;
- sobrescritura concurrente silenciosa;
- persistencia parcial;
- uso de Metadata para modificar atributos protegidos;
- modificación indirecta de otros Aggregates;
- uso de Read Models como Write Model;
- uso de Integration Events como comandos;
- publicación de hechos no confirmados;
- exposición innecesaria de información;
- utilización de importaciones como bypass;
- utilización de operaciones masivas como bypass;
- utilización de optimizaciones como bypass.

---

# Restricciones

No está permitido:

- modificar Participation sin pasar por el Aggregate Root;
- ejecutar una operación sin la Permission requerida;
- interpretar Permission Granted como garantía de éxito;
- omitir Invariants por privilegios del actor;
- omitir la State Machine;
- omitir reglas del Lifecycle;
- modificar ParticipationId;
- modificar OrganizationId;
- modificar Version manualmente;
- ignorar ConcurrencyConflictError;
- permitir Last Write Wins;
- modificar timestamps históricos arbitrariamente;
- utilizar Metadata para sobrescribir estado protegido;
- utilizar Repository para ejecutar comportamiento del dominio;
- utilizar Read Models para escribir en el Aggregate;
- utilizar Integration Events para modificar directamente el
  Aggregate;
- incorporar otros Aggregates dentro del Consistency Boundary;
- modificar otros Aggregates desde Participation;
- publicar Integration Events correspondientes a cambios no
  confirmados;
- considerar reintentos de publicación como nuevas operaciones del
  dominio;
- ejecutar Commands durante rehidratación;
- generar nuevos Domain Events durante Replay;
- exponer información innecesaria;
- debilitar seguridad por razones de rendimiento;
- introducir tecnologías concretas como reglas del dominio.

---

# Reglas

## REG-001

Toda modificación de Participation debe realizarse mediante
comportamiento válido del Aggregate Root.

---

## REG-002

Toda operación protegida requiere la Permission correspondiente.

---

## REG-003

Una Permission concedida no puede evitar State Machine, Lifecycle
ni Invariants.

---

## REG-004

ParticipationId es inmutable.

---

## REG-005

OrganizationId es inmutable durante toda la vida del Aggregate.

---

## REG-006

Version no puede modificarse directamente.

---

## REG-007

Todo conflicto de concurrencia debe impedir la sobrescritura
silenciosa del estado persistido.

---

## REG-008

El Repository no puede utilizarse para evitar comportamiento del
Aggregate.

---

## REG-009

Los Read Models son de solo lectura y no pueden modificar
Participation.

---

## REG-010

Los Integration Events no otorgan autoridad de escritura sobre
Participation.

---

## REG-011

Otros Aggregates permanecen fuera del Consistency Boundary de
Participation.

---

## REG-012

Metadata no puede modificar atributos protegidos del Aggregate.

---

## REG-013

Una operación rechazada no modifica estado ni Version y no genera
el Domain Event de éxito correspondiente.

---

## REG-014

Los Integration Events solo pueden representar hechos previamente
confirmados.

---

## REG-015

Las optimizaciones de rendimiento no pueden reducir las
protecciones del dominio.

---

# Definición de Éxito

El Security Model del Aggregate **Participation** protege su
identidad, pertenencia organizacional, estado, Lifecycle, State
Machine, Invariants, Permissions, Version, persistencia,
Consistency Boundary, Domain Events, Integration Events y Read
Models sin introducir comportamiento alternativo ni ampliar las
responsabilidades del Aggregate.

El modelo garantiza que:

- ParticipationId permanezca inmutable;
- OrganizationId permanezca inmutable;
- toda modificación protegida requiera la Permission
  correspondiente;
- las Permissions no sustituyan las reglas del dominio;
- State Machine y Lifecycle permanezcan obligatorios;
- las Invariants no puedan evitarse;
- Version permanezca protegida contra modificación directa;
- los conflictos concurrentes no produzcan sobrescrituras
  silenciosas;
- el Repository no permita evitar el Aggregate Root;
- Metadata no permita sobrescribir atributos protegidos;
- los timestamps preserven la historia del Lifecycle;
- otros Aggregates permanezcan fuera del Consistency Boundary;
- los Domain Events correspondan únicamente a hechos válidos;
- los Integration Events representen únicamente cambios
  confirmados;
- los Read Models permanezcan de solo lectura;
- las importaciones y operaciones masivas respeten las mismas
  reglas;
- las optimizaciones de rendimiento no debiliten las protecciones;
- las tecnologías concretas permanezcan fuera del modelo
  conceptual.

De esta forma,
`DOMAIN-008O-Security-Model.md` establece las reglas oficiales de
seguridad para proteger el Aggregate **Participation** manteniendo
íntegramente el patrón consolidado de AURA Core.