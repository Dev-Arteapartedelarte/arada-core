# DOMAIN-012H — Audit Examples

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
- DOMAIN-012F-Permissions.md
- DOMAIN-012G-Repository-Contract.md
- DOMAIN-012I-Versioning.md
- DOMAIN-012J-Consistency-Boundary.md
- DOMAIN-012K-Integration-Events.md
- DOMAIN-012L-Read-Model.md
- DOMAIN-012M-Test-Scenarios.md

---

# Objetivo

Este documento presenta ejemplos conceptuales del Aggregate
**Audit** conforme al modelo oficial definido para la versión 1.0.

Los ejemplos permiten observar la aplicación conjunta de:

- Aggregate;
- Lifecycle;
- State Machine;
- Commands;
- Domain Events;
- Invariants;
- Permissions;
- Repository Contract;
- Versioning;
- Consistency Boundary.

Los ejemplos no introducen nuevos:

- estados;
- Commands;
- Domain Events;
- Invariants;
- Permissions;
- políticas de retención;
- mecanismos técnicos.

---

# Principio Fundamental

Todos los ejemplos deben respetar:

```text
Confirmed Source Fact

    │
    ▼

RecordAudit

    │
    ▼

Audit

    │
    ▼

Recorded

    │
    ▼

AuditRecorded
```

y:

```text
Source Domain Fact

≠

Audit

≠

AuditRecorded
```

---

# Ejemplo 1 — Registro Básico

Existe un hecho auditable ya confirmado.

Conceptualmente:

```text
Confirmed Source Fact
```

Se presenta:

```text
RecordAudit
```

Estado previo:

```text
No Audit
```

Resultado:

```text
AuditStatus = Recorded

Version = 1
```

Domain Event:

```text
AuditRecorded
```

---

# Ejemplo 2 — Creación con AuditId

Command:

```text
RecordAudit(
    AuditId = AUD-001
)
```

Resultado válido:

```text
AuditId = AUD-001

AuditStatus = Recorded

Version = 1
```

Debe mantenerse:

```text
AuditId

=

AUD-001
```

durante toda la existencia del Aggregate.

---

# Ejemplo 3 — AuditId distinto del SourceAggregateId

Hecho de origen:

```text
SourceAggregateId = ASM-100
```

Audit:

```text
AuditId = AUD-002
```

Debe mantenerse:

```text
AUD-002

≠

ASM-100
```

Ambos identificadores representan identidades diferentes.

---

# Ejemplo 4 — AuditId distinto de SourceEventId

Source Domain Event:

```text
EventId = EVT-500
```

Audit:

```text
AuditId = AUD-003
```

representación:

```text
SourceEventId = EVT-500
```

Debe mantenerse:

```text
AuditId

≠

SourceEventId
```

---

# Ejemplo 5 — Source Domain Event de Assembly

Assembly produce:

```text
AssemblyStarted
```

como hecho confirmado.

Posteriormente:

```text
AssemblyStarted
    │
    ▼
Audit Coordination
    │
    ▼
RecordAudit
    │
    ▼
Audit
    │
    ▼
Recorded
    │
    ▼
AuditRecorded
```

AssemblyStarted continúa perteneciendo a Assembly.

AuditRecorded pertenece a Audit.

---

# Ejemplo 6 — Assembly no se Modifica

Estado de Assembly:

```text
AssemblyStatus = InProgress

Assembly.Version = 8
```

Se registra Audit:

```text
RecordAudit
```

Resultado en Audit:

```text
AuditStatus = Recorded

Audit.Version = 1
```

Assembly permanece:

```text
AssemblyStatus = InProgress

Assembly.Version = 8
```

Debe mantenerse:

```text
Audit Transaction

≠

Assembly Transaction
```

---

# Ejemplo 7 — SourceAggregateVersion

Source Aggregate:

```text
Assembly.Version = 8
```

Audit conserva:

```text
SourceAggregateVersion = 8
```

mientras:

```text
Audit.Version = 1
```

Debe mantenerse:

```text
SourceAggregateVersion

≠

Audit.Version
```

semánticamente.

---

# Ejemplo 8 — Coincidencia Numérica de Version

Source Aggregate:

```text
SourceAggregateVersion = 1
```

Audit recién creado:

```text
Audit.Version = 1
```

Aunque los valores numéricos coincidan:

```text
1 = 1
```

conceptualmente:

```text
SourceAggregateVersion

≠

Audit.Version
```

Cada Version pertenece a un Aggregate distinto.

---

# Ejemplo 9 — ActorId Disponible

El hecho original contiene:

```text
ActorId = CIT-050
```

RecordAudit puede preservar:

```text
ActorId = CIT-050
```

Resultado:

```text
AuditStatus = Recorded
```

Audit no administra Citizen.

Debe mantenerse:

```text
ActorId

≠

Citizen Aggregate Ownership
```

---

# Ejemplo 10 — ActorId Ausente

El hecho original no contiene ActorId.

Entonces Audit puede registrar:

```text
AuditStatus = Recorded
```

sin inventar:

```text
ActorId
```

Debe mantenerse:

```text
Missing ActorId

≠

Fabricated ActorId
```

---

# Ejemplo 11 — CorrelationId

Source Domain Event:

```text
CorrelationId = FLOW-100
```

Audit puede preservar:

```text
CorrelationId = FLOW-100
```

Esto permite relacionar ambos hechos sin fusionar sus Consistency
Boundaries.

---

# Ejemplo 12 — CausationId

Si el flujo proporciona:

```text
CausationId = EVT-700
```

Audit puede preservar dicho valor conforme al contrato recibido.

Debe mantenerse:

```text
CausationId

≠

AuditId
```

---

# Ejemplo 13 — CorrelationId no es Permission

Existe:

```text
CorrelationId = FLOW-200
```

Esto no significa:

```text
Permission = Allowed
```

CorrelationId representa trazabilidad.

Authorization continúa siendo una responsabilidad separada.

---

# Ejemplo 14 — Actor Autorizado

Un actor o proceso autorizado presenta:

```text
RecordAudit
```

La autorización es válida.

Audit todavía debe validar:

- State Machine;
- Invariants;
- identidad;
- información de origen.

Debe mantenerse:

```text
Authorized

≠

Automatically Valid
```

---

# Ejemplo 15 — Operación No Autorizada

Se intenta:

```text
RecordAudit
```

sin autorización aplicable.

Resultado:

```text
Rejected
```

No existe:

```text
AuditRecorded
```

No existe nueva unidad Audit.

---

# Ejemplo 16 — Autorizado pero Inválido

El actor está autorizado.

Sin embargo, el Command intenta registrar información que no
representa un hecho confirmado.

Resultado:

```text
Rejected
```

No se produce:

```text
AuditRecorded
```

Debe mantenerse:

```text
Authorized

+

Invalid Domain Conditions

=

Rejected
```

---

# Ejemplo 17 — Intento de Registrar un Command Externo

Se recibe:

```text
StartAssembly
```

Este concepto representa una intención.

No debe tratarse automáticamente como hecho consumado.

Debe mantenerse:

```text
StartAssembly

≠

Confirmed Auditable Fact
```

---

# Ejemplo 18 — Registro Posterior al Domain Event

Assembly acepta:

```text
StartAssembly
```

y produce:

```text
AssemblyStarted
```

Ahora existe un hecho consumado.

Posteriormente puede existir:

```text
RecordAudit
```

conforme al contrato correspondiente.

---

# Ejemplo 19 — Hecho Futuro Rechazado

Se intenta registrar:

```text
"Assembly will start tomorrow"
```

como si fuera un hecho ya ocurrido.

Resultado:

```text
Rejected
```

Debe mantenerse:

```text
Future Intent

≠

Audit Fact
```

---

# Ejemplo 20 — SourceOccurredAt y CreatedAt

Source Domain Event:

```text
SourceOccurredAt = T1
```

Audit es creado posteriormente:

```text
Audit.CreatedAt = T2
```

donde:

```text
T2 >= T1
```

cuando corresponda temporalmente.

Debe mantenerse:

```text
SourceOccurredAt

≠

Audit.CreatedAt
```

semánticamente.

---

# Ejemplo 21 — AuditRecorded.OccurredAt

El hecho de origen ocurre en:

```text
SourceOccurredAt = T1
```

Audit es registrado en:

```text
AuditRecorded.OccurredAt = T2
```

Debe mantenerse:

```text
SourceOccurredAt

≠

AuditRecorded.OccurredAt
```

porque representan hechos distintos.

---

# Ejemplo 22 — NotificationDelivered

Notification produce:

```text
NotificationDelivered
```

Posteriormente:

```text
NotificationDelivered
    │
    ▼
RecordAudit
    │
    ▼
AuditRecorded
```

El Audit resultante:

```text
AuditStatus = Recorded
```

No:

```text
AuditStatus = Delivered
```

---

# Ejemplo 23 — NotificationDeliveryFailed

Notification produce:

```text
NotificationDeliveryFailed
```

como hecho confirmado.

Audit puede registrar dicho hecho.

Resultado:

```text
AuditStatus = Recorded
```

No:

```text
AuditStatus = Failed
```

Debe mantenerse:

```text
NotificationStatus

≠

AuditStatus
```

---

# Ejemplo 24 — Document Archived

Document se encuentra:

```text
DocumentStatus = Archived
```

y produce un hecho auditable conforme a su dominio.

Audit resultante:

```text
AuditStatus = Recorded
```

No:

```text
AuditStatus = Archived
```

porque Archived no forma parte del Lifecycle de Audit versión 1.0.

---

# Ejemplo 25 — Assembly Cancelled

Assembly produce:

```text
AssemblyCancelled
```

Audit registra el hecho.

Resultado:

```text
AuditStatus = Recorded
```

No:

```text
AuditStatus = Cancelled
```

---

# Ejemplo 26 — Voting

Voting produce un hecho confirmado.

Audit puede registrar su representación.

Audit no:

- registra el voto;
- cambia el voto;
- abre Voting;
- cierra Voting;
- modifica resultados;
- cambia VotingStatus.

---

# Ejemplo 27 — Membership

Membership produce un hecho confirmado.

Audit conserva la trazabilidad aplicable.

Audit no modifica:

```text
MembershipStatus

Membership.Version

Membership Lifecycle
```

---

# Ejemplo 28 — Proposal

Proposal produce un hecho auditable.

Resultado:

```text
AuditStatus = Recorded
```

Proposal mantiene:

```text
ProposalStatus

Proposal.Version

Proposal Lifecycle
```

independientes.

---

# Ejemplo 29 — Participation

Participation produce un hecho confirmado.

Audit registra una representación propia.

Debe mantenerse:

```text
Participation Transaction

≠

Audit Transaction
```

---

# Ejemplo 30 — Organization

Organization produce un hecho auditable.

Audit registra:

```text
SourceAggregateId

SourceAggregateType
```

cuando corresponda.

Organization permanece fuera del Aggregate Audit.

---

# Ejemplo 31 — Citizen

Un hecho relacionado con Citizen incluye:

```text
ActorId = CIT-900
```

Audit puede preservar ActorId.

No almacena el Aggregate Citizen completo.

Debe mantenerse:

```text
ActorId Reference

≠

Embedded Citizen
```

---

# Ejemplo 32 — Territory

Territory produce un Domain Event auditable.

Audit registra la referencia aplicable.

Territory conserva:

- identidad;
- Lifecycle;
- Version;
- Invariants;
- Consistency Boundary.

---

# Ejemplo 33 — Role

Un hecho relacionado con Role puede ser auditable.

Audit no:

- crea Role;
- asigna Role;
- revoca Role;
- cambia Permissions.

---

# Ejemplo 34 — Source Event Completo no se Copia

El Source Domain Event contiene:

```text
Large Payload
```

Audit solamente necesita:

```text
SourceEventId

SourceEventType

SourceAggregateId

SourceAggregateVersion

OccurredAt
```

conforme al contrato aplicable.

No debe copiar automáticamente:

```text
Entire Source Payload
```

---

# Ejemplo 35 — Información Sensible

El Source Event contiene información que no es necesaria para Audit.

Audit no la incorpora solamente porque exista.

Debe mantenerse:

```text
Source Data Exists

≠

Audit Must Store It
```

---

# Ejemplo 36 — Token en Source Payload

Un mensaje técnico incluye:

```text
AccessToken
```

El token no debe formar parte del Aggregate Audit.

Audit conserva únicamente información de dominio necesaria.

---

# Ejemplo 37 — Password

Si una fuente técnica contiene:

```text
Password
```

Audit no lo incorpora.

Debe mantenerse:

```text
Credential

∉

Audit Aggregate
```

---

# Ejemplo 38 — Source Fact Confirmado y Audit Pendiente

En tiempo:

```text
T1:

Source Fact Confirmed
```

posteriormente:

```text
T2:

Audit Not Yet Recorded
```

y finalmente:

```text
T3:

Audit Recorded
```

Esta ventana es válida conforme a consistencia eventual.

---

# Ejemplo 39 — Fallo Antes de Registrar Audit

Source Aggregate confirma:

```text
Source Fact
```

Audit intenta procesarlo.

Ocurre:

```text
PersistenceFailure
```

antes del commit de Audit.

Resultado:

```text
Source Fact remains confirmed
```

y:

```text
No confirmed AuditRecorded
```

---

# Ejemplo 40 — PersistenceFailure no es Failed

Ocurre:

```text
PersistenceFailure
```

No debe crearse:

```text
AuditStatus = Failed
```

porque Failed no existe en el Lifecycle.

---

# Ejemplo 41 — RepositoryUnavailable

`AuditRepository` no está disponible.

Resultado conceptual:

```text
RepositoryUnavailable
```

Esto no produce:

```text
AuditStatus = Failed
```

ni:

```text
AuditRecorded
```

confirmado.

---

# Ejemplo 42 — AuditNotFound

Consulta:

```text
findById(AUD-404)
```

Resultado:

```text
AuditNotFound
```

La operación no:

- crea Audit;
- cambia Version;
- produce AuditRecorded.

---

# Ejemplo 43 — nextIdentity()

Repository proporciona:

```text
nextIdentity()

↓

AUD-010
```

Esto no significa todavía:

```text
Audit AUD-010 exists
```

Solo después de una creación válida:

```text
RecordAudit

↓

Audit AUD-010 Recorded
```

existe el Aggregate.

---

# Ejemplo 44 — DuplicateAuditId

Ya existe:

```text
AuditId = AUD-010
```

Otro intento incompatible intenta crear una nueva unidad con:

```text
AuditId = AUD-010
```

Resultado:

```text
DuplicateAuditId
```

La unidad existente no se sobrescribe.

---

# Ejemplo 45 — save() no Incrementa Version

Aggregate válido:

```text
Audit.Version = 1
```

Repository ejecuta:

```text
save(Audit)
```

Resultado:

```text
Persisted Version = 1
```

No:

```text
Persisted Version = 2
```

porque Repository no decide Version.

---

# Ejemplo 46 — findById() no Incrementa Version

Persistido:

```text
Audit.Version = 1
```

Operación:

```text
findById(AUD-001)
```

Resultado:

```text
Audit.Version = 1
```

---

# Ejemplo 47 — Rehidratación

Repository recupera:

```text
AuditId = AUD-001

AuditStatus = Recorded

Version = 1
```

La rehidratación no genera:

```text
AuditRecorded
```

nuevamente.

---

# Ejemplo 48 — Rehidratación con Event Sourcing

Historial:

```text
AuditRecorded
AggregateVersion = 1
```

Aplicación:

```text
apply(AuditRecorded)
```

Resultado:

```text
AuditStatus = Recorded

Version = 1
```

No se ejecuta:

```text
RecordAudit
```

---

# Ejemplo 49 — Replay no es Nuevo Hecho

Se vuelve a aplicar:

```text
AuditRecorded
```

para reconstruir estado.

Debe mantenerse:

```text
Replay

≠

New AuditRecorded
```

---

# Ejemplo 50 — EventId

Domain Event:

```text
EventId = EVT-AUD-001

EventType = AuditRecorded

AuditId = AUD-001

AggregateVersion = 1
```

Debe mantenerse:

```text
EventId

≠

AuditId
```

---

# Ejemplo 51 — Domain Event Duplicado

Un consumidor recibe dos veces:

```text
EventId = EVT-AUD-001
```

Conceptualmente:

```text
Same EventId

=

Same Domain Event
```

La segunda entrega no representa un nuevo hecho del Aggregate.

---

# Ejemplo 52 — Duplicate Technical Delivery

Un mensaje técnico que origina Audit se entrega dos veces.

Debe mantenerse:

```text
Duplicate Technical Delivery

≠

Two Source Facts
```

y:

```text
Duplicate Technical Delivery

≠

Automatic Second Audit
```

---

# Ejemplo 53 — Retry Técnico

Primer intento:

```text
RecordAudit processing
    │
    ▼
PersistenceFailure
```

Segundo intento técnico:

```text
Retry processing
```

Debe mantenerse:

```text
Technical Retry

≠

RetryAudit
```

porque RetryAudit no existe como Command.

---

# Ejemplo 54 — No AuditRetried

Después de un retry técnico exitoso:

```text
AuditRecorded
```

puede representar la creación finalmente confirmada.

No se produce:

```text
AuditRetried
```

porque dicho Domain Event no existe en versión 1.0.

---

# Ejemplo 55 — No Draft

Intento conceptual:

```text
No Audit → Draft
```

Resultado:

```text
Rejected
```

Draft no pertenece al Lifecycle.

---

# Ejemplo 56 — No Pending

Intento:

```text
AuditStatus = Pending
```

Resultado:

```text
Invalid State
```

Pending técnico no es estado de Audit.

---

# Ejemplo 57 — No Active

Intento:

```text
AuditStatus = Active
```

Resultado:

```text
Invalid State
```

---

# Ejemplo 58 — No Failed

Intento:

```text
AuditStatus = Failed
```

Resultado:

```text
Invalid State
```

---

# Ejemplo 59 — No Cancelled

Intento:

```text
Recorded → Cancelled
```

Resultado:

```text
Rejected
```

Cancelled no existe en Audit versión 1.0.

---

# Ejemplo 60 — No Archived

Intento:

```text
Recorded → Archived
```

Resultado:

```text
Rejected
```

La naturaleza histórica de Audit no introduce automáticamente
Archived.

---

# Ejemplo 61 — No Deleted

Intento:

```text
Recorded → Deleted
```

Resultado:

```text
Rejected
```

Deleted no pertenece al Lifecycle.

---

# Ejemplo 62 — Repository.delete() no es DeleteAudit

Repository Contract contiene conceptualmente:

```text
delete()
```

Esto no crea:

```text
DeleteAudit
```

ni:

```text
AuditDeleted
```

ni:

```text
AuditStatus = Deleted
```

---

# Ejemplo 63 — No ArchiveAudit

Se intenta:

```text
ArchiveAudit
```

Resultado:

```text
Undefined Domain Command
```

ArchiveAudit no forma parte de la versión 1.0.

---

# Ejemplo 64 — No CorrectAudit

Se intenta modificar un Audit histórico mediante:

```text
CorrectAudit
```

Resultado:

```text
Undefined Domain Command
```

Una corrección del Source Aggregate debe expresarse mediante un nuevo
hecho del contexto responsable cuando corresponda.

---

# Ejemplo 65 — Nuevo Hecho Correctivo

Source Aggregate produce inicialmente:

```text
Source Fact A
```

Audit:

```text
Audit A = Recorded
```

posteriormente ocurre:

```text
Source Fact B
```

que corrige o complementa el estado del Source Aggregate.

Resultado:

```text
Audit A remains unchanged
```

y puede existir:

```text
Audit B = Recorded
```

conforme al contrato correspondiente.

---

# Ejemplo 66 — Múltiples Hechos del Mismo Aggregate

Source Aggregate:

```text
AggregateId = ASM-100
```

produce:

```text
Fact A

Fact B

Fact C
```

Audit puede representar:

```text
AUD-101 → Fact A

AUD-102 → Fact B

AUD-103 → Fact C
```

Cada Audit mantiene identidad independiente.

---

# Ejemplo 67 — Recorded es Terminal

Audit:

```text
AuditStatus = Recorded
```

Se intenta una transición posterior.

Resultado:

```text
Rejected
```

Recorded permanece terminal en versión 1.0.

---

# Ejemplo 68 — setStatus()

Intento:

```text
audit.setStatus(Archived)
```

Resultado:

```text
Not Allowed
```

El estado no puede modificarse mediante setter directo.

---

# Ejemplo 69 — setAuditId()

Audit existente:

```text
AuditId = AUD-200
```

Intento:

```text
setAuditId(AUD-201)
```

Resultado:

```text
Rejected
```

AuditId permanece inmutable.

---

# Ejemplo 70 — setVersion()

Audit:

```text
Version = 1
```

Intento:

```text
setVersion(99)
```

Resultado:

```text
Rejected
```

Version no posee setter público.

---

# Ejemplo 71 — SourceEventId no Sustituye AuditId

Source:

```text
SourceEventId = EVT-900
```

No debe asumirse:

```text
AuditId = EVT-900
```

como regla obligatoria.

Audit mantiene identidad propia.

---

# Ejemplo 72 — Falta de CorrelationId

Source Fact no proporciona:

```text
CorrelationId
```

Audit puede continuar siendo válido cuando el contrato lo permita.

No debe inventarse:

```text
CorrelationId = RANDOM
```

para completar artificialmente la información.

---

# Ejemplo 73 — Falta de CausationId

Source Fact no proporciona:

```text
CausationId
```

Audit no fabrica dicho valor.

---

# Ejemplo 74 — Falta de SourceEventId

Un hecho auditable no proviene necesariamente de un Domain Event
identificable.

Si el contrato válido no contiene:

```text
SourceEventId
```

Audit no inventa uno.

---

# Ejemplo 75 — Read Model

Audit confirmado:

```text
AuditId = AUD-300

AuditStatus = Recorded

Version = 1
```

puede proyectarse hacia:

```text
Audit Read Model
```

La proyección no modifica el Aggregate.

---

# Ejemplo 76 — Read Model Desactualizado

Si en una futura evolución existiera:

```text
Audit.Version = N
```

mientras una proyección mantiene temporalmente:

```text
ReadModel.Version = N - 1
```

la ventana puede ser válida conforme a consistencia eventual.

El Read Model no constituye autoridad de escritura.

---

# Ejemplo 77 — Query no es Command

Una consulta:

```text
Find Audit by AuditId
```

no ejecuta:

```text
RecordAudit
```

ni incrementa Version.

---

# Ejemplo 78 — Buscar por ActorId

Una necesidad:

```text
Find Audits by ActorId
```

pertenece al Read Side.

No requiere añadir:

```text
findByActorId()
```

al Aggregate como comportamiento de dominio.

---

# Ejemplo 79 — Buscar por CorrelationId

Consulta:

```text
Find Audits by CorrelationId
```

pertenece a Read Models o mecanismos de consulta.

No modifica Audit.

---

# Ejemplo 80 — Analytics

Analytics necesita contar hechos auditables por período.

Debe utilizar:

```text
Read Models

or

Projections
```

No debe utilizar Audit Aggregate como motor analítico.

---

# Ejemplo 81 — Audit no es Log

Aplicación escribe:

```text
"HTTP request completed in 120 ms"
```

Esto representa un log técnico.

No se transforma automáticamente en:

```text
RecordAudit
```

---

# Ejemplo 82 — Audit no es Metric

Observability registra:

```text
request_count = 100
```

Esto no constituye automáticamente un hecho del Aggregate Audit.

---

# Ejemplo 83 — Audit no es Trace Técnico

Un trace técnico identifica:

```text
span-123
```

Esto no convierte el trace en:

```text
Audit
```

Audit y Observability permanecen separados.

---

# Ejemplo 84 — Integration Event

Audit produce:

```text
AuditRecorded
```

Si existe un contrato explícito de integración, posteriormente puede
ocurrir:

```text
AuditRecorded
    │
    ▼
Integration Boundary
    │
    ▼
Integration Event
```

El Integration Event no es el Domain Event original.

---

# Ejemplo 85 — Sin Necesidad de Integration Event

Audit produce:

```text
AuditRecorded
```

pero no existe consumidor externo que requiera un contrato público.

Entonces:

```text
No Integration Event Required
```

Debe mantenerse:

```text
Domain Event

≠

Mandatory Integration Event
```

---

# Ejemplo 86 — Publicación Después del Commit

Flujo válido:

```text
RecordAudit
    │
    ▼
Audit
    │
    ▼
Repository.save()
    │
    ▼
Commit
    │
    ▼
External Publication
```

No debe utilizarse:

```text
Publish Externally
    │
    ▼
Attempt Commit
```

como comportamiento normal.

---

# Ejemplo 87 — Retry de Publicación

Audit ya está:

```text
Recorded

Version = 1
```

La publicación externa falla y se reintenta.

Resultado:

```text
AuditStatus = Recorded

Audit.Version = 1
```

Debe mantenerse:

```text
Integration Retry

≠

Audit Modification
```

---

# Ejemplo 88 — Outbox

Cuando la arquitectura utilice Outbox:

```text
Audit Commit
    │
    ▼
Outbox Processing
    │
    ▼
External Publication
```

estados de Outbox como:

```text
Pending

Published

Failed
```

no se convierten en AuditStatus.

---

# Ejemplo 89 — FIWARE

AuditRecorded puede originar posteriormente una integración hacia
FIWARE cuando exista contrato explícito.

Audit no conoce:

```text
NGSI-LD

Context Broker

Orion
```

como parte de su comportamiento.

---

# Ejemplo 90 — SyncAuditToFIWARE

Intento de introducir:

```text
SyncAuditToFIWARE
```

como Domain Command.

Resultado:

```text
Not a Domain Command
```

La operación pertenece a Integration o Infrastructure.

---

# Ejemplo 91 — Sistema Municipal

Una plataforma municipal necesita información Audit.

La comunicación debe ocurrir mediante un contrato de integración.

La plataforma no modifica directamente:

```text
AuditStatus

Audit.Version

AuditId
```

---

# Ejemplo 92 — Permiso Municipal

Un sistema municipal posee su propia autorización.

Esto no significa automáticamente:

```text
Audit Permission = Allowed
```

Debe existir la traducción o política correspondiente en la frontera
adecuada.

---

# Ejemplo 93 — FIWARE Authorization

Una identidad técnica FIWARE está autenticada.

Esto no implica:

```text
RecordAudit Authorized
```

automáticamente.

Authentication externa y Permission de dominio permanecen
separadas.

---

# Ejemplo 94 — Read Permission

Un actor puede tener permiso para consultar un Read Model.

Esto no significa:

```text
RecordAudit Permission
```

Debe mantenerse:

```text
Read Permission

≠

Write Permission
```

---

# Ejemplo 95 — Write Permission

Un proceso tiene permiso para:

```text
RecordAudit
```

Esto no le concede automáticamente acceso a todos los Audit Read
Models.

---

# Ejemplo 96 — ConcurrencyConflict Conceptual

En una futura modificación válida de un Audit existente:

```text
PersistedVersion = 5

ExpectedVersion = 4
```

Resultado:

```text
ConcurrencyConflict
```

La escritura no debe sobrescribir el estado confirmado.

---

# Ejemplo 97 — ConcurrencyConflict no es Estado

Después de:

```text
ConcurrencyConflict
```

no debe existir:

```text
AuditStatus = Failed
```

ni ningún otro estado nuevo.

---

# Ejemplo 98 — Repository no Corrige Aggregate

Audit inválido:

```text
AuditId = null
```

llega hipotéticamente al Repository.

El Repository no debe:

```text
generate AuditId silently
```

para reparar el Aggregate.

El estado debe ser válido antes de persistencia.

---

# Ejemplo 99 — Repository no Inventa ActorId

Audit no contiene:

```text
ActorId
```

porque el Source Fact no lo proporcionó.

Repository no debe completar:

```text
ActorId = SYSTEM
```

automáticamente.

---

# Ejemplo 100 — Repository no Inventa AuditRecorded

Repository ejecuta:

```text
save()
```

sobre una unidad válida.

Repository no crea por decisión propia:

```text
AuditRecorded
```

El Domain Event pertenece al comportamiento del Aggregate.

---

# Ejemplo 101 — Múltiples Audits Independientes

Existen:

```text
Audit A

Audit B

Audit C
```

Cada uno posee:

```text
Independent AuditId

Independent Version

Independent Consistency Boundary
```

Persistir Audit A no requiere modificar Audit B o Audit C.

---

# Ejemplo 102 — No Aggregate Global de Auditoría

No debe modelarse conceptualmente:

```text
GlobalAudit
    ├── Audit A
    ├── Audit B
    ├── Audit C
    └── All Audit History
```

como una única unidad de consistencia por el solo hecho de requerir
consultas históricas.

Las consultas globales pertenecen al Read Side.

---

# Ejemplo 103 — Event Sourcing Compatible

Si se utiliza Event Sourcing:

```text
Stream AUD-001

    AuditRecorded v1
```

puede reconstruir:

```text
AuditId = AUD-001

AuditStatus = Recorded

Version = 1
```

La compatibilidad no obliga a utilizar Event Sourcing.

---

# Ejemplo 104 — State Persistence Compatible

Si se utiliza persistencia de estado:

```text
Audit
    │
    ├── AuditId = AUD-001
    ├── Status = Recorded
    └── Version = 1
```

puede persistirse como unidad.

El dominio no decide la tecnología concreta.

---

# Ejemplo 105 — Cache

Infrastructure utiliza una cache para acelerar lecturas.

La cache contiene:

```text
AUD-001
```

Esto no convierte la cache en autoridad del Aggregate.

Debe mantenerse:

```text
Cache

≠

Domain Source of Truth
```

---

# Ejemplo 106 — Timestamp Técnico

Base de datos registra:

```text
InsertedAt = T3
```

Esto no sustituye:

```text
SourceOccurredAt

Audit.CreatedAt

AuditRecorded.OccurredAt
```

que poseen significados propios.

---

# Ejemplo 107 — Estado Técnico Processing

Un worker se encuentra:

```text
Processing
```

Esto no significa:

```text
AuditStatus = Processing
```

Processing no pertenece al Lifecycle.

---

# Ejemplo 108 — Estado Técnico Queued

Un mensaje se encuentra:

```text
Queued
```

Esto no significa:

```text
AuditStatus = Queued
```

---

# Ejemplo 109 — Dead Letter

Un mensaje termina técnicamente en:

```text
DeadLettered
```

Esto no crea:

```text
AuditStatus = DeadLettered
```

ni un Domain Event de Audit por sí mismo.

---

# Ejemplo 110 — Nuevo Source Fact no Cambia Audit Anterior

Audit existente:

```text
AUD-500

SourceEventId = EVT-A
```

posteriormente el Source Aggregate produce:

```text
EVT-B
```

Audit AUD-500 continúa representando:

```text
EVT-A
```

No se reescribe para representar EVT-B.

---

# Ejemplo 111 — Audit no es Document Archive

Un hecho histórico contiene referencia:

```text
DocumentId = DOC-100
```

Audit puede conservar la referencia aplicable.

No almacena automáticamente todo el contenido del Document.

Debe mantenerse:

```text
Audit

≠

Document Archive
```

---

# Ejemplo 112 — Audit no Envía Notification

Audit registra:

```text
AuditRecorded
```

Esto no significa:

```text
Send Notification
```

Notification pertenece a su propio Bounded Context.

---

# Ejemplo 113 — Audit no Modifica Integration

Audit produce un hecho.

Integration puede reaccionar posteriormente.

Audit no administra directamente:

- adapters;
- brokers;
- schemas externos;
- APIs;
- FIWARE;
- municipal systems.

---

# Ejemplo 114 — No Auditoría Recursiva Automática

Audit produce:

```text
AuditRecorded
```

Esto no debe generar automáticamente:

```text
RecordAudit(AuditRecorded)
```

de manera recursiva indefinida.

Debe mantenerse:

```text
AuditRecorded

≠

Automatic Recursive Audit
```

---

# Ejemplo 115 — Operación Completa Exitosa

Source Aggregate:

```text
AggregateId = NOT-100

Version = 3
```

produce:

```text
NotificationDelivered

EventId = EVT-NOT-300

AggregateVersion = 3

OccurredAt = T1

CorrelationId = FLOW-500
```

Audit recibe conceptualmente:

```text
RecordAudit(
    AuditId = AUD-900,
    SourceAggregateId = NOT-100,
    SourceAggregateType = Notification,
    SourceEventId = EVT-NOT-300,
    SourceEventType = NotificationDelivered,
    SourceAggregateVersion = 3,
    OccurredAt = T1,
    CorrelationId = FLOW-500
)
```

Audit valida la operación.

Resultado:

```text
AuditId = AUD-900

AuditStatus = Recorded

SourceAggregateId = NOT-100

SourceEventId = EVT-NOT-300

SourceAggregateVersion = 3

Version = 1
```

Domain Event:

```text
AuditRecorded
```

con:

```text
AggregateVersion = 1
```

Notification permanece independiente.

---

# Ejemplo 116 — Operación Completa Rechazada

Se presenta:

```text
RecordAudit(
    AuditId = null
)
```

Resultado:

```text
Rejected
```

No existe:

```text
Audit
```

confirmado.

No existe:

```text
AuditRecorded
```

No existe:

```text
Version = 1
```

persistida para dicha unidad.

---

# Ejemplo 117 — Operación con Información Inventada

Source Fact no contiene:

```text
ActorId
```

Se intenta completar:

```text
ActorId = CIT-UNKNOWN
```

sin respaldo contractual.

Resultado:

```text
Invalid Audit Information
```

Audit no debe fabricar información.

---

# Ejemplo 118 — Auditoría y Consistencia Eventual

Flujo:

```text
T1

AssemblyStarted committed
```

luego:

```text
T2

Audit does not yet exist
```

posteriormente:

```text
T3

RecordAudit accepted
```

y:

```text
T4

AuditRecorded committed
```

Esta secuencia mantiene:

```text
Assembly Consistency Boundary

≠

Audit Consistency Boundary
```

---

# Ejemplo 119 — Fallo de Audit no Revierte Assembly

Assembly:

```text
AssemblyStarted
```

ya fue confirmado.

Audit falla antes del commit.

Assembly permanece:

```text
InProgress
```

conforme a su propio estado.

No ocurre:

```text
Assembly rollback
```

---

# Ejemplo 120 — Read Model no Modifica Audit

Read Model contiene:

```text
AuditId = AUD-900

AuditStatus = Recorded
```

Un consumidor intenta modificar:

```text
AuditStatus
```

desde la proyección.

Resultado:

```text
Not Allowed
```

El Read Model no posee Write Authority.

---

# Matriz de Ejemplos de Estado

| Situación | Resultado de Audit |
|---|---|
| Hecho válido registrado | Recorded |
| Source Aggregate está Failed | Recorded |
| Source Aggregate está Archived | Recorded |
| Source Aggregate está Cancelled | Recorded |
| Persistencia falla antes del commit | No Audit confirmado |
| Mensaje está Queued | No nuevo AuditStatus |
| Worker está Processing | No nuevo AuditStatus |
| Retry técnico | No transición |
| Duplicate Delivery | No transición automática |

---

# Matriz Command / Resultado

| Command | Condición | Resultado |
|---|---|---|
| RecordAudit | válido y autorizado | Recorded |
| RecordAudit | no autorizado | Rejected |
| RecordAudit | hecho no confirmado | Rejected |
| RecordAudit | identidad inválida | Rejected |
| RecordAudit | viola Invariants | Rejected |

---

# Matriz Command / Event

| Command | Resultado válido | Domain Event |
|---|---|---|
| RecordAudit | Recorded | AuditRecorded |

Una operación rechazada produce:

```text
No Success Domain Event
```

---

# Matriz de Identidades

| Concepto | Significado |
|---|---|
| AuditId | identidad de Audit |
| SourceAggregateId | identidad del Aggregate originador |
| SourceEventId | identidad del evento originador |
| EventId | identidad del Domain Event de Audit |
| CorrelationId | correlación del flujo |
| CausationId | relación causal |

Ninguno debe sustituir automáticamente a otro.

---

# Matriz de Versiones

| Concepto | Significado |
|---|---|
| Audit.Version | evolución del Aggregate Audit |
| SourceAggregateVersion | versión del Aggregate originador |
| AuditRecorded.AggregateVersion | Version resultante de Audit |

Para creación válida:

```text
Audit.Version = 1

AuditRecorded.AggregateVersion = 1
```

mientras SourceAggregateVersion conserva su valor independiente.

---

# Flujo General

```text
Source Aggregate
      │
      ▼
Confirmed Source Fact
      │
      ▼
Eventual Propagation
      │
      ▼
Authorization
      │
      ▼
RecordAudit
      │
      ▼
Audit
      │
      ├── Validate State Machine
      ├── Validate Invariants
      ├── Establish AuditId
      ├── State = Recorded
      └── Version = 1
              │
              ▼
         AuditRecorded
              │
              ▼
     AuditRepository.save()
              │
              ▼
            Commit
```

---

# Flujo con Read Model

```text
RecordAudit
    │
    ▼
Audit
    │
    ▼
AuditRecorded
    │
    ▼
Projection
    │
    ▼
Audit Read Model
```

La proyección no posee autoridad de escritura.

---

# Flujo con Integration

Cuando exista una necesidad explícita:

```text
AuditRecorded
    │
    ▼
Integration Boundary
    │
    ▼
Integration Event
    │
    ▼
External Consumer
```

El Integration Event no modifica retroactivamente Audit.

---

# Flujo con Fallo de Integración

Audit ya está:

```text
Recorded

Version = 1
```

La publicación externa falla:

```text
IntegrationFailure
```

Audit continúa:

```text
Recorded

Version = 1
```

---

# Flujo con Event Sourcing

```text
RecordAudit
    │
    ▼
AuditRecorded v1
    │
    ▼
Event Stream
    │
    ▼
Rehydration
    │
    ▼
Recorded v1
```

Rehydration no produce nuevos eventos.

---

# Reglas Fundamentales

Los ejemplos de Audit confirman que:

1. Audit solamente registra hechos ya confirmados.
2. RecordAudit es el único Command oficial.
3. La única transición es No Audit → Recorded.
4. Recorded es el único estado persistido.
5. Recorded es terminal.
6. AuditRecorded es el único Domain Event oficial.
7. AuditId permanece inmutable.
8. AuditId es distinto de SourceAggregateId.
9. AuditId es distinto de SourceEventId.
10. EventId es distinto de AuditId.
11. SourceAggregateVersion es independiente de Audit.Version.
12. AuditRecorded.AggregateVersion coincide con Audit.Version
    resultante.
13. ActorId solamente se conserva cuando existe conforme al
    contrato.
14. CorrelationId solamente se conserva cuando corresponde.
15. CausationId solamente se conserva cuando corresponde.
16. Información ausente no se inventa.
17. El Source Domain Event permanece separado de AuditRecorded.
18. Audit no modifica el Source Aggregate.
19. Un fallo de Audit no revierte el Source Fact.
20. Source Aggregate y Audit mantienen transacciones independientes.
21. La consistencia entre Aggregates puede ser eventual.
22. Authorization no reemplaza Domain Validation.
23. Una operación no autorizada no produce AuditRecorded.
24. Un Command externo no es automáticamente un hecho auditable.
25. Un hecho futuro no puede registrarse como consumado.
26. Source Status no determina AuditStatus.
27. Fallos técnicos no crean estado Failed.
28. Estados técnicos no pertenecen al Lifecycle.
29. Retries técnicos no son Commands de dominio.
30. Duplicados técnicos no son nuevos hechos.
31. Repository no incrementa Version.
32. Repository no inventa Domain Events.
33. Repository no corrige Aggregates inválidos.
34. Rehidratación no ejecuta Commands.
35. Replay no crea nuevos Domain Events.
36. Read Models no poseen autoridad de escritura.
37. Domain Event no implica Integration Event obligatorio.
38. Publicación externa no cambia Audit.Version.
39. Audit no es Log.
40. Audit no es Observability.
41. Audit no es Document Archive.
42. Audit no es Notification.
43. Audit no es Integration.
44. FIWARE permanece fuera del Aggregate.
45. Sistemas municipales permanecen fuera del Aggregate.
46. No existen Draft, Pending, Active, Failed, Cancelled, Archived o
    Deleted como estados de Audit.
47. No existen ArchiveAudit, DeleteAudit, RetryAudit o CorrectAudit
    como Commands.
48. No existen AuditArchived, AuditDeleted, AuditRetried o
    AuditCorrected como Domain Events.
49. Nuevos hechos del Source Aggregate no reescriben Audits
    anteriores.
50. Cada unidad Audit mantiene identidad y consistencia propias.

---

# Definición de Éxito

Los ejemplos del Aggregate **Audit** demuestran el comportamiento
conceptual de la versión 1.0 sin introducir reglas adicionales al
modelo consolidado.

El flujo principal permanece:

```text
Confirmed Source Fact

    │
    ▼

RecordAudit

    │
    ▼

No Audit → Recorded

    │
    ▼

Version = 1

    │
    ▼

AuditRecorded
```

Los ejemplos demuestran que:

- Audit representa su propia unidad de trazabilidad;
- el hecho originador ya debe estar confirmado;
- Source Domain Event y AuditRecorded permanecen separados;
- Audit no modifica el Aggregate originador;
- AuditId, SourceAggregateId, SourceEventId y EventId mantienen
  significados distintos;
- SourceAggregateVersion y Audit.Version permanecen independientes;
- información de actor, correlación y causalidad solamente se
  conserva cuando está disponible;
- ninguna información faltante se inventa;
- Recorded es el único estado oficial y permanece terminal;
- operaciones no autorizadas o inválidas no producen estado ni
  Domain Event de éxito;
- fallos de Repository no se convierten en estados del dominio;
- Technical Retry y Duplicate Delivery permanecen fuera del
  Lifecycle;
- Repository persiste el resultado válido pero no decide
  comportamiento;
- rehidratación y replay no representan nuevos hechos;
- Read Models permanecen fuera del Write Model;
- Integration Events permanecen separados de Domain Events;
- publicación externa no cambia el Aggregate;
- FIWARE, sistemas municipales, logs y Observability permanecen
  fuera del Consistency Boundary;
- cualquier corrección del Source Aggregate produce nuevos hechos sin
  reescribir la trazabilidad anterior;
- cada unidad Audit conserva identidad, Version y Consistency
  Boundary independientes.

De esta forma, `DOMAIN-012H-Examples.md` consolida ejemplos
conceptuales coherentes con el Aggregate **Audit** y con el patrón
oficial de AURA Core.