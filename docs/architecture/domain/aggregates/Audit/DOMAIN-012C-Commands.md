# DOMAIN-012C — Audit Commands

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
- DOMAIN-012D-Domain-Events.md
- DOMAIN-012E-Invariants.md
- DOMAIN-012F-Permissions.md
- DOMAIN-012I-Versioning.md
- DOMAIN-012J-Consistency-Boundary.md

---

# Objetivo

Este documento define formalmente los **Commands** del Aggregate
**Audit**.

Los Commands representan intenciones explícitas de modificar el
Aggregate conforme a:

- Lifecycle;
- State Machine;
- Invariants;
- Permissions;
- Versioning;
- Consistency Boundary.

Un Command expresa una intención.

No representa un hecho ya ocurrido.

Debe mantenerse:

```text
Command

≠

Domain Event
```

---

# Principio Fundamental

Audit posee un Lifecycle mínimo:

```text
No Audit → Recorded
```

Por lo tanto, la versión 1.0 requiere una única intención de dominio
capaz de producir la creación válida del Aggregate.

El Command oficial es:

```text
RecordAudit
```

---

# Commands Oficiales

La versión 1.0 define exclusivamente:

```text
RecordAudit
```

No existen otros Commands oficiales.

---

# RecordAudit

`RecordAudit` expresa la intención de crear una unidad Audit a partir
de un hecho auditable ya confirmado.

Conceptualmente:

```text
Confirmed Auditable Fact

    │
    ▼

RecordAudit

    │
    ▼

Audit

    │
    ▼

Recorded
```

---

# Intención

`RecordAudit` significa:

```text
Record a confirmed auditable fact
```

dentro de Audit Management.

No significa:

```text
Create Source Fact
```

ni:

```text
Modify Source Aggregate
```

ni:

```text
Replay Source Event
```

---

# Estado Requerido

`RecordAudit` solamente puede ejecutarse cuando:

```text
No Audit
```

representa la inexistencia previa de la unidad Audit.

La transición correspondiente es:

```text
No Audit → Recorded
```

---

# Estado Resultante

Después de una ejecución válida:

```text
AuditStatus = Recorded
```

conforme al Lifecycle y State Machine oficiales.

---

# Precondición Fundamental

Antes de ejecutar:

```text
RecordAudit
```

debe existir un hecho auditable ya confirmado.

Debe mantenerse:

```text
Confirmed Source Fact

before

RecordAudit
```

Audit no registra hechos futuros ni intenciones todavía no
consumadas.

---

# Información Conceptual del Command

`RecordAudit` puede transportar conceptualmente la información
necesaria para representar el hecho auditable conforme al contrato
recibido.

Puede incluir:

```text
AuditId

SourceAggregateId

SourceAggregateType

SourceEventId

SourceEventType

SourceAggregateVersion

ActorId

OccurredAt

CorrelationId

CausationId
```

únicamente cuando cada elemento sea aplicable y esté disponible en
el contrato de origen.

---

# AuditId

`RecordAudit` debe permitir establecer:

```text
AuditId
```

para la nueva unidad Audit.

AuditId:

- identifica exclusivamente a Audit;
- es único;
- permanece inmutable;
- no equivale a SourceAggregateId;
- no equivale a SourceEventId.

---

# SourceAggregateId

Cuando el hecho auditable provenga de un Aggregate identificable,
el Command puede proporcionar:

```text
SourceAggregateId
```

conforme al contrato recibido.

Esta referencia no incorpora el Aggregate externo dentro de Audit.

---

# SourceAggregateType

Cuando esté disponible:

```text
SourceAggregateType
```

permite conservar la naturaleza conceptual del Aggregate de origen.

No concede a Audit autoridad sobre dicho Aggregate.

---

# SourceEventId

Cuando el hecho auditable provenga de un Domain Event y exista:

```text
EventId
```

el Command puede proporcionar dicha identidad como:

```text
SourceEventId
```

Debe mantenerse:

```text
SourceEventId

≠

AuditId
```

---

# SourceEventType

Cuando el hecho auditable provenga de un Domain Event:

```text
SourceEventType
```

puede preservar el tipo del hecho recibido.

Audit no redefine el significado del Source Event.

---

# SourceAggregateVersion

Cuando el contrato recibido la proporcione:

```text
SourceAggregateVersion
```

puede conservarse como información auditable.

Debe mantenerse:

```text
SourceAggregateVersion

≠

Audit.Version
```

---

# ActorId

`ActorId` puede formar parte del Command cuando el hecho auditable
identifica al actor correspondiente.

La ausencia de ActorId no autoriza a inventar un actor.

Debe mantenerse:

```text
Missing ActorId

≠

Fabricated ActorId
```

---

# OccurredAt

Cuando el hecho de origen proporciona:

```text
OccurredAt
```

el Command puede preservarlo como parte de la información auditable.

OccurredAt representa el momento del hecho de origen.

No representa automáticamente:

```text
Audit.CreatedAt
```

---

# CorrelationId

Cuando exista:

```text
CorrelationId
```

puede preservarse para mantener trazabilidad entre hechos
relacionados.

No constituye identidad del Aggregate.

---

# CausationId

Cuando exista:

```text
CausationId
```

puede preservarse para mantener trazabilidad causal.

No constituye identidad del Aggregate.

---

# Información Mínima

`RecordAudit` debe contener únicamente la información necesaria para
que Audit pueda validar y representar el hecho auditable.

No debe transportar Aggregates completos.

Debe mantenerse:

```text
Command Payload

=

Minimum Required Domain Information
```

---

# Información No Disponible

`RecordAudit` no debe inventar información ausente en el contrato de
origen.

Si no existen:

```text
ActorId

CorrelationId

CausationId
```

u otros valores opcionales, el Command no debe fabricarlos.

---

# Validación

Antes de aceptar `RecordAudit`, el Aggregate debe validar:

- AuditId;
- inexistencia previa de la unidad Audit correspondiente;
- existencia de un hecho auditable válido;
- referencias de origen aplicables;
- coherencia de la información recibida;
- Invariants;
- State Machine;
- Consistency Boundary.

---

# Resultado Válido

Una ejecución válida produce:

```text
No Audit

    │
    ▼

RecordAudit

    │
    ▼

Recorded
```

y establece:

```text
Version = 1
```

conforme al patrón consolidado de AURA.

---

# Domain Event Resultante

El Domain Event correspondiente a una ejecución válida se define
formalmente en:

```text
DOMAIN-012D-Domain-Events.md
```

Este documento establece únicamente que:

```text
Valid RecordAudit

↓

Audit Domain Event
```

debe representar un hecho consumado.

---

# Command Rechazado

Si `RecordAudit` no puede preservar las Invariants:

```text
RecordAudit

↓

Rejected
```

No debe producirse:

- Aggregate parcial;
- estado Recorded inválido;
- incremento de Version;
- actualización de timestamps;
- Domain Event de éxito.

---

# Registro sin Hecho Confirmado

Si se intenta:

```text
RecordAudit
```

sin un hecho auditable confirmado:

```text
Operation

↓

Rejected
```

Debe mantenerse:

```text
Intent

≠

Auditable Fact
```

---

# Registro de Hecho Futuro

No está permitido utilizar `RecordAudit` para registrar una acción
que todavía no ocurrió.

Debe mantenerse:

```text
Future Intent

≠

Audit Record
```

---

# Registro de Command Externo

Un Command perteneciente a otro Aggregate no constituye por sí mismo
un hecho auditable consumado.

Por ejemplo:

```text
StartAssembly
```

representa una intención.

Mientras:

```text
AssemblyStarted
```

representa un hecho confirmado.

Audit debe basarse en hechos auditables conforme a sus contratos.

---

# Source Domain Event

Cuando un Domain Event confirmado constituye el origen:

```text
Source Domain Event

    │
    ▼

Application / Audit Coordination

    │
    ▼

RecordAudit

    │
    ▼

Audit
```

El Source Domain Event no se ejecuta como Command de Audit.

---

# Separación de Propiedad

Debe mantenerse:

```text
Source Domain Event

belongs to

Source Aggregate
```

mientras:

```text
RecordAudit

belongs to

Audit Management
```

y:

```text
Audit

belongs to

Audit Management
```

---

# No Modificación del Source Aggregate

`RecordAudit` nunca modifica directamente:

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

Debe mantenerse:

```text
RecordAudit

≠

Source Aggregate Command
```

---

# No Rollback del Source Fact

Si `RecordAudit` es rechazado o falla su procesamiento técnico:

```text
Confirmed Source Fact
```

permanece confirmado.

Debe mantenerse:

```text
Audit Failure

≠

Source Fact Rollback
```

---

# Permissions

`RecordAudit` debe ejecutarse únicamente desde un actor o proceso
autorizado por la política aplicable.

La autorización se resuelve antes de ejecutar comportamiento del
Aggregate.

Debe mantenerse:

```text
Authorized

≠

Automatically Valid
```

Una autorización válida no permite evitar:

- State Machine;
- Invariants;
- Consistency Boundary.

---

# Authentication

Audit no autentica al actor que origina el Command.

Authentication permanece fuera del Aggregate.

Debe mantenerse:

```text
Authentication

∉

Audit Aggregate
```

---

# Command Inmutable

`RecordAudit` representa una intención inmutable.

Una vez creado para procesamiento, sus datos no deben modificarse
arbitrariamente para representar otra intención.

Debe mantenerse:

```text
Command

=

Immutable Intent
```

---

# Un Command, Un Propósito

`RecordAudit` posee un único propósito:

```text
Record an Auditable Fact
```

No debe utilizarse simultáneamente para:

- modificar el Aggregate originador;
- enviar Notifications;
- publicar Integration Events;
- generar Documents;
- actualizar Read Models;
- cambiar permisos;
- ejecutar tareas de Infrastructure.

---

# Command no es Query

`RecordAudit` modifica el Write Model.

No debe utilizarse para consultar Audit.

Debe mantenerse:

```text
Command

≠

Query
```

Las consultas pertenecen al Read Side.

---

# Ausencia de Setters

No existen Commands equivalentes a:

```text
SetAuditId

SetSourceAggregateId

SetSourceEventId

SetActorId

SetOccurredAt

SetVersion

SetCreatedAt

SetUpdatedAt
```

como mecanismo de modificación directa.

Los valores protegidos se establecen únicamente mediante
comportamiento válido del Aggregate.

---

# Commands No Oficiales

La versión 1.0 no define:

```text
CreateAudit

UpdateAudit

ModifyAudit

ArchiveAudit

DeleteAudit

CancelAudit

RetryAudit

PublishAudit

ApproveAudit

RejectAudit

CorrectAudit

InvalidateAudit
```

Ninguno debe utilizarse como Command de dominio sin una evolución
explícita del modelo.

---

# CreateAudit

La versión 1.0 utiliza:

```text
RecordAudit
```

como intención oficial asociada a:

```text
No Audit → Recorded
```

No se define adicionalmente:

```text
CreateAudit
```

porque constituiría una intención redundante dentro del modelo
actual.

---

# UpdateAudit

No existe:

```text
UpdateAudit
```

como Command genérico.

Los Commands deben expresar lenguaje ubicuo y comportamiento
específico.

Debe mantenerse:

```text
Generic Update

≠

Domain Command
```

---

# CorrectAudit

La versión 1.0 no define:

```text
CorrectAudit
```

Una corrección posterior del Aggregate originador debe representarse
mediante un nuevo hecho del contexto responsable cuando corresponda.

Audit no reescribe el hecho histórico anterior mediante un Command
genérico de corrección.

---

# ArchiveAudit

La versión 1.0 no define:

```text
ArchiveAudit
```

porque:

```text
Archived
```

no pertenece al Lifecycle oficial.

---

# DeleteAudit

La versión 1.0 no define:

```text
DeleteAudit
```

como Command de Lifecycle.

La eliminación física no constituye una transición oficial.

---

# RetryAudit

La versión 1.0 no define:

```text
RetryAudit
```

Los retries técnicos previos a la creación de Audit pertenecen a
Application o Infrastructure.

Debe mantenerse:

```text
Technical Retry

≠

Domain Command
```

---

# PublishAudit

La publicación de información hacia Integration no constituye un
Command del Aggregate Audit.

Debe mantenerse:

```text
PublishIntegrationMessage

≠

Audit Domain Command
```

---

# Commands Técnicos

No forman parte del dominio Commands como:

```text
SaveAudit

LoadAudit

PersistAudit

SerializeAudit

CacheAudit

PublishAuditMessage

SendAuditToBroker

SyncAuditToFIWARE

WriteAuditToDatabase
```

Estas son operaciones técnicas.

---

# Repository

El Repository no ejecuta `RecordAudit` por decisión propia.

El flujo conceptual es:

```text
RecordAudit

    │
    ▼

Audit

    │
    ├── Validate
    ├── Preserve Invariants
    └── Produce Valid State
            │
            ▼
        Repository
```

El Repository persiste el resultado válido.

---

# Repository no es Command Handler de Dominio

El Repository:

- no decide si el hecho es auditable;
- no crea Audit por sí mismo;
- no genera AuditId por comportamiento de negocio;
- no modifica el Source Aggregate;
- no inventa Domain Events;
- no evita Invariants.

---

# Versioning

`RecordAudit` produce la creación válida del Aggregate.

El resultado:

```text
Version = 1
```

pertenece a Audit.

Una operación rechazada conserva:

```text
No Audit
```

y no existe Version persistida para una unidad no creada.

---

# Optimistic Concurrency

Como `RecordAudit` crea una nueva unidad Audit, la persistencia debe
proteger la identidad frente a creación incompatible o duplicada
conforme al Repository Contract y Versioning.

La estrategia técnica concreta permanece fuera del Aggregate.

---

# Duplicados

Una entrega duplicada del mismo mensaje técnico no debe provocar
automáticamente un nuevo hecho de dominio.

Debe mantenerse:

```text
Duplicate Technical Message

≠

New RecordAudit Intent
```

La coordinación de idempotencia pertenece a las capas
correspondientes.

---

# Identidad del Hecho

Cuando el contrato de origen proporciona:

```text
SourceEventId
```

dicha identidad puede contribuir a reconocer conceptualmente el
hecho original.

Esto no convierte SourceEventId en AuditId.

---

# Technical Retry

Si el procesamiento de `RecordAudit` falla antes de confirmar el
Aggregate:

```text
No Audit
```

permanece como condición conceptual.

Un nuevo intento técnico del mismo procesamiento no constituye un
nuevo Command semántico por el solo hecho de repetirse.

---

# Consistency Boundary

`RecordAudit` solamente modifica:

```text
Audit
```

dentro de su Consistency Boundary.

No existe una transacción obligatoria:

```text
Source Aggregate

+

Audit
```

Debe mantenerse:

```text
Source Transaction

≠

Audit Transaction
```

---

# Consistencia Eventual

Puede existir:

```text
Source Fact Confirmed

↓

Audit Not Yet Recorded
```

y posteriormente:

```text
RecordAudit

↓

Recorded
```

sin violar consistencia del dominio.

---

# Read Models

Los Read Models no ejecutan:

```text
RecordAudit
```

y no pueden crear Audit.

Debe mantenerse:

```text
Read Model

≠

Command Handler
```

---

# CQRS

En el Write Side:

```text
RecordAudit

    │
    ▼

Audit Aggregate

    │
    ├── State Machine
    ├── Invariants
    ├── Version
    └── Domain Event
```

En el Read Side:

```text
Audit Facts

    │
    ▼

Projection

    │
    ▼

Read Model
```

Los Queries no se incorporan a `RecordAudit`.

---

# Event Sourcing

Si Audit utiliza Event Sourcing:

```text
RecordAudit
```

representa comportamiento nuevo.

La rehidratación de hechos históricos no vuelve a ejecutar:

```text
RecordAudit
```

Debe mantenerse:

```text
Replay

≠

Command Execution
```

---

# Rehidratación

Rehidratar un Audit ya Recorded:

- no ejecuta RecordAudit;
- no crea un nuevo AuditId;
- no incrementa Version;
- no produce un nuevo Domain Event;
- no modifica CreatedAt.

---

# Domain Events e Integration Events

`RecordAudit` puede producir un Domain Event propio después de una
operación válida.

La eventual transformación de ese Domain Event en un Integration
Event pertenece a la frontera correspondiente.

Debe mantenerse:

```text
RecordAudit

↓

Audit Domain Event
```

separado de:

```text
Audit Domain Event

↓

Integration Event
```

---

# Integration

`RecordAudit` no publica directamente:

- mensajes de broker;
- contratos FIWARE;
- payloads NGSI-LD;
- APIs municipales;
- eventos externos.

La publicación pertenece a Application e Integration.

---

# FIWARE

No existe:

```text
RecordAuditInFIWARE
```

como Command del Aggregate.

Debe mantenerse:

```text
FIWARE Operation

≠

Audit Domain Command
```

---

# Audit de Organization

Un hecho confirmado de Organization puede producir:

```text
RecordAudit
```

cuando exista el contrato correspondiente.

Audit no ejecuta Commands sobre Organization.

---

# Audit de Citizen

Un hecho confirmado relacionado con Citizen puede ser registrado
mediante Audit cuando corresponda.

`RecordAudit` no modifica Citizen.

---

# Audit de Membership

Un hecho confirmado de Membership puede originar `RecordAudit`.

Audit no modifica:

```text
MembershipStatus

Membership.Version

Membership Lifecycle
```

---

# Audit de Role

Un hecho confirmado relacionado con Role puede originar
trazabilidad.

`RecordAudit` no asigna ni revoca Roles.

---

# Audit de Territory

Un hecho confirmado de Territory puede originar Audit.

`RecordAudit` no modifica Territory.

---

# Audit de Assembly

Conceptualmente:

```text
Assembly Domain Event

    │
    ▼

Audit Coordination

    │
    ▼

RecordAudit

    │
    ▼

Audit Recorded
```

Assembly permanece fuera del Consistency Boundary.

---

# Audit de Proposal

Un hecho confirmado de Proposal puede originar `RecordAudit`.

Audit no modifica Proposal.

---

# Audit de Participation

Un hecho confirmado de Participation puede originar `RecordAudit`.

Audit no modifica Participation.

---

# Audit de Voting

Un hecho confirmado de Voting puede originar `RecordAudit`.

El Command no:

- registra votos;
- modifica votos;
- abre Voting;
- cierra Voting;
- calcula resultados;
- modifica VotingStatus.

---

# Audit de Document

Un hecho confirmado de Document puede originar `RecordAudit`.

El Command no modifica:

```text
DocumentStatus

Document.Version

Document Content

Document Lifecycle
```

---

# Audit de Notification

Un hecho confirmado de Notification puede originar `RecordAudit`.

El Command no modifica:

```text
NotificationStatus

Notification.Version

Notification Lifecycle
```

---

# Audit e Integration

Integration puede proporcionar contratos desde los cuales Audit
reciba información auditable cuando exista equivalencia conceptual
explícita.

`RecordAudit` no adquiere conocimiento del protocolo o tecnología
utilizada para transportar dicha información.

---

# Seguridad

`RecordAudit` no debe contener:

- passwords;
- access tokens;
- refresh tokens;
- API keys;
- private keys;
- secretos técnicos;
- credenciales de infraestructura;
- información no necesaria para el hecho auditable.

---

# Minimización

Debe mantenerse:

```text
Source Payload

≠

Automatic RecordAudit Payload
```

El Command transporta únicamente la información necesaria para el
dominio Audit.

---

# Logs

Un log técnico no se transforma automáticamente en:

```text
RecordAudit
```

Debe existir un hecho reconocido como auditable conforme al dominio.

Debe mantenerse:

```text
Log Entry

≠

Domain Command
```

---

# Observability

Metrics, traces y logs no generan por sí mismos `RecordAudit`.

Audit Management debe recibir un hecho conforme a un contrato
reconocido por el dominio.

---

# Extensión de Commands

Cualquier nuevo Command debe representar una intención de dominio
explícita.

Para incorporar un nuevo Command deberá definirse:

- propósito;
- estado requerido;
- transición cuando corresponda;
- precondiciones;
- Invariants;
- Permissions;
- impacto sobre Version;
- Domain Event resultante;
- Test Scenarios.

---

# Impacto de un Nuevo Command

Incorporar un nuevo Command requiere revisar, cuando corresponda:

```text
DOMAIN-012-Aggregate.md

DOMAIN-012A-Lifecycle.md

DOMAIN-012B-State-Machine.md

DOMAIN-012C-Commands.md

DOMAIN-012D-Domain-Events.md

DOMAIN-012E-Invariants.md

DOMAIN-012F-Permissions.md

DOMAIN-012H-Examples.md

DOMAIN-012I-Versioning.md

DOMAIN-012M-Test-Scenarios.md
```

No debe añadirse un Command aisladamente rompiendo coherencia
documental.

---

# Relación Oficial Command / State Machine

La relación versión 1.0 es:

| Command | Estado previo | Estado resultante |
|---|---|---|
| RecordAudit | No Audit | Recorded |

No existen otras combinaciones válidas.

---

# Reglas Fundamentales

Los Commands de Audit deben cumplir:

1. Existe un único Command oficial: RecordAudit.
2. RecordAudit representa una intención.
3. RecordAudit solamente puede producir No Audit → Recorded.
4. El hecho auditable debe estar confirmado previamente.
5. Audit no registra hechos futuros.
6. Audit no utiliza Commands externos como hechos consumados.
7. AuditId se establece durante la creación y permanece inmutable.
8. SourceAggregateId no equivale a AuditId.
9. SourceEventId no equivale a AuditId.
10. SourceAggregateVersion no equivale a Audit.Version.
11. Información ausente no debe inventarse.
12. El Command debe utilizar información mínima necesaria.
13. El Command no contiene Aggregates externos completos.
14. Un Command rechazado no crea Aggregate parcial.
15. Un Command rechazado no produce Domain Event de éxito.
16. RecordAudit no modifica el Source Aggregate.
17. Un fallo de Audit no revierte el Source Fact.
18. Authorization no evita Invariants.
19. Authentication permanece fuera del Aggregate.
20. Los Commands son intenciones inmutables.
21. Un Command posee un propósito específico.
22. Command no equivale a Query.
23. No existen setters como Commands.
24. No existen Commands genéricos UpdateAudit o ModifyAudit.
25. CreateAudit no es Command adicional en versión 1.0.
26. CorrectAudit no está definido.
27. ArchiveAudit no está definido.
28. DeleteAudit no está definido.
29. RetryAudit no está definido.
30. PublishAudit no está definido.
31. Operaciones técnicas no son Domain Commands.
32. Repository no decide comportamiento de dominio.
33. Read Models no ejecutan Commands.
34. Technical Retry no constituye nuevo Command semántico.
35. Duplicate Delivery no constituye automáticamente nueva intención.
36. RecordAudit modifica exclusivamente el Consistency Boundary de
    Audit.
37. CQRS mantiene Commands en el Write Side.
38. Event Sourcing replay no ejecuta Commands.
39. Integration Events no son publicados directamente por el
    Aggregate.
40. Cualquier nuevo Command requiere evolución explícita y
    coordinada.

---

# Definición de Éxito

Los Commands del Aggregate **Audit** expresan las intenciones
permitidas para modificar su Write Model conforme al Lifecycle
mínimo definido para la versión 1.0.

El modelo define exclusivamente:

```text
RecordAudit
```

asociado a:

```text
No Audit → Recorded
```

y garantiza que:

- RecordAudit solamente registra hechos ya confirmados;
- un Command representa intención y no hecho;
- Audit no anticipa acontecimientos futuros;
- AuditId permanece propio e inmutable;
- las referencias al origen no transfieren ownership;
- SourceEventId permanece distinto de AuditId;
- SourceAggregateVersion permanece distinto de Audit.Version;
- la información faltante no se inventa;
- el Command utiliza solamente información necesaria;
- las Invariants deben cumplirse antes de aceptar la operación;
- una operación rechazada no produce estado parcial;
- una operación rechazada no produce Domain Event de éxito;
- el Source Aggregate no es modificado;
- un fallo posterior de Audit no revierte el hecho original;
- Permissions permanecen separadas de Domain Validation;
- Authentication permanece fuera del Aggregate;
- no existen setters públicos disfrazados de Commands;
- no existen Commands genéricos de actualización;
- no existen ArchiveAudit, DeleteAudit, RetryAudit o PublishAudit en
  la versión 1.0;
- operaciones de persistencia, mensajería, FIWARE y Infrastructure
  no son Commands de dominio;
- Repository, Read Models e Integration permanecen separados;
- CQRS mantiene el Command en el Write Side;
- Event Sourcing permanece compatible sin reutilizar Commands
  durante replay;
- cualquier nuevo Command requerirá una evolución explícita del
  dominio.

De esta forma, `DOMAIN-012C-Commands.md` establece los Commands
oficiales del Aggregate **Audit** conforme al patrón consolidado de
AURA Core.