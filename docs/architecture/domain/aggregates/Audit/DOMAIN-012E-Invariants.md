# DOMAIN-012E — Audit Invariants

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
- DOMAIN-012F-Permissions.md
- DOMAIN-012G-Repository-Contract.md
- DOMAIN-012I-Versioning.md
- DOMAIN-012J-Consistency-Boundary.md
- DOMAIN-012K-Integration-Events.md
- DOMAIN-012L-Read-Model.md
- DOMAIN-012M-Test-Scenarios.md

---

# Objetivo

Este documento define formalmente las **Invariants** del Aggregate
**Audit**.

Una Invariant representa una regla que debe permanecer verdadera
durante toda la existencia válida del Aggregate.

Las Invariants protegen:

- identidad;
- Lifecycle;
- State Machine;
- trazabilidad;
- significado histórico;
- Versioning;
- Consistency Boundary;
- relación con hechos externos;
- Domain Events;
- integridad del Aggregate.

Toda operación válida debe preservar las Invariants antes y después
de modificar Audit.

---

# Principio Fundamental

Debe mantenerse:

```text
Invariants Before Operation

=

Valid
```

y:

```text
Invariants After Operation

=

Valid
```

Si una operación no puede preservar todas las Invariants
aplicables:

```text
Operation

↓

Rejected
```

---

# Alcance

Las Invariants pertenecen exclusivamente al Consistency Boundary:

```text
Audit
```

No otorgan a Audit autoridad para validar o modificar el estado
interno de otros Aggregates.

Debe mantenerse:

```text
Audit Invariant

≠

External Aggregate Invariant
```

---

# INV-001 — AuditId es obligatorio

Toda instancia válida de Audit debe poseer:

```text
AuditId
```

No puede existir un Audit persistido sin identidad.

---

# INV-002 — AuditId es inmutable

Una vez creado:

```text
AuditId
```

nunca puede cambiar.

Debe mantenerse:

```text
AuditId at Creation

=

AuditId for Entire Aggregate Existence
```

---

# INV-003 — AuditId es identidad propia

AuditId identifica exclusivamente al Aggregate Audit.

No debe confundirse con:

```text
SourceAggregateId

SourceEventId

DomainEvent.EventId

CorrelationId

CausationId
```

---

# INV-004 — AuditId no se reutiliza

Dos unidades Audit distintas no deben compartir intencionalmente el
mismo AuditId.

Debe mantenerse:

```text
One AuditId

=

One Audit Aggregate Identity
```

---

# INV-005 — El único estado oficial es Recorded

La versión 1.0 reconoce exclusivamente:

```text
Recorded
```

como estado persistido válido.

---

# INV-006 — No Audit no es estado persistido

```text
No Audit
```

representa inexistencia conceptual del Aggregate.

No constituye un valor válido de AuditStatus.

---

# INV-007 — Toda unidad Audit comienza en Recorded

Una nueva unidad Audit válida debe resultar directamente en:

```text
Recorded
```

mediante:

```text
No Audit → Recorded
```

---

# INV-008 — Recorded es terminal

Una vez alcanzado:

```text
Recorded
```

no existe otra transición oficial en la versión 1.0.

---

# INV-009 — No existen estados adicionales

No forman parte del modelo oficial:

```text
Draft

Pending

Active

Failed

Cancelled

Archived

Deleted
```

ni otros estados no definidos explícitamente.

---

# INV-010 — Toda transición debe pertenecer a la State Machine

La única transición válida es:

```text
No Audit → Recorded
```

Ninguna operación puede establecer un estado fuera de esta regla.

---

# INV-011 — No existe modificación directa de State

No debe permitirse:

```text
setStatus(...)
```

ni mecanismo equivalente que evite el comportamiento del
Aggregate.

---

# INV-012 — Toda modificación ocurre mediante la Aggregate Root

Toda modificación válida de Audit debe ocurrir mediante:

```text
Audit
```

como única Aggregate Root.

Ninguna estructura interna puede ser modificada directamente desde
fuera del Aggregate.

---

# INV-013 — Existe un único Command oficial

La versión 1.0 define exclusivamente:

```text
RecordAudit
```

---

# INV-014 — RecordAudit solamente crea Recorded

Debe mantenerse:

```text
RecordAudit

=

No Audit → Recorded
```

RecordAudit no puede producir otro estado.

---

# INV-015 — Audit solamente registra hechos ya confirmados

Antes de aceptar:

```text
RecordAudit
```

debe existir un hecho auditable ya ocurrido.

Debe mantenerse:

```text
Confirmed Auditable Fact

before

Recorded Audit
```

---

# INV-016 — Audit no registra intenciones futuras como hechos

Una intención todavía no consumada no puede considerarse un hecho
auditable confirmado.

Debe mantenerse:

```text
Intent

≠

Confirmed Fact
```

---

# INV-017 — Command externo no equivale automáticamente a hecho auditable

Un Command perteneciente a otro Aggregate representa intención.

No debe tratarse automáticamente como hecho consumado.

Debe mantenerse:

```text
Source Command

≠

Source Domain Fact
```

---

# INV-018 — Audit no crea el hecho originador

Audit registra una representación propia de un hecho ya ocurrido.

Nunca debe cumplirse:

```text
Audit

↓

Creates Source Fact
```

---

# INV-019 — Audit no modifica el hecho originador

Una unidad Audit no puede modificar retrospectivamente el hecho que
originó su creación.

Debe mantenerse:

```text
Source Fact

=

Independent Confirmed Fact
```

---

# INV-020 — Audit no modifica el Source Aggregate

Audit no puede modificar directamente:

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

---

# INV-021 — Audit no realiza rollback del Source Aggregate

Un fallo de Audit no revierte un hecho ya confirmado por otro
Aggregate.

Debe mantenerse:

```text
Audit Failure

≠

Source Aggregate Rollback
```

---

# INV-022 — Source Aggregate y Audit poseen transacciones independientes

Debe mantenerse:

```text
Source Aggregate Transaction

≠

Audit Transaction
```

No existe una transacción multi-Aggregate obligatoria por regla del
dominio.

---

# INV-023 — Las referencias externas no incorporan Aggregates completos

Audit solamente puede conservar referencias e información necesaria
conforme al contrato recibido.

Debe mantenerse:

```text
External Reference

≠

Embedded External Aggregate
```

---

# INV-024 — SourceAggregateId no es AuditId

Cuando exista:

```text
SourceAggregateId
```

debe mantenerse conceptualmente distinto de:

```text
AuditId
```

---

# INV-025 — SourceEventId no es AuditId

Cuando exista:

```text
SourceEventId
```

debe mantenerse:

```text
SourceEventId

≠

AuditId
```

---

# INV-026 — Source Domain Event permanece propiedad del Source Aggregate

Cuando Audit se origine desde un Domain Event:

```text
Source Domain Event
```

continúa perteneciendo al Aggregate que lo produjo.

Audit no adquiere ownership sobre ese evento.

---

# INV-027 — Source Domain Event no es Audit

Debe mantenerse:

```text
Source Domain Event

≠

Audit
```

Un evento externo puede aportar información auditable, pero no
constituye el Aggregate Audit.

---

# INV-028 — Source Domain Event no es Audit Domain Event

Debe mantenerse:

```text
Source Domain Event

≠

AuditRecorded
```

Cada evento pertenece al Aggregate que lo produce.

---

# INV-029 — Audit y AuditRecorded son conceptos distintos

Debe mantenerse:

```text
Audit

≠

AuditRecorded
```

Audit representa estado.

AuditRecorded representa un hecho consumado del Aggregate Audit.

---

# INV-030 — Existe un único Domain Event oficial

La versión 1.0 define exclusivamente:

```text
AuditRecorded
```

como Domain Event de Audit.

---

# INV-031 — AuditRecorded solamente ocurre después de RecordAudit válido

Debe mantenerse:

```text
Valid RecordAudit

↓

AuditRecorded
```

Una operación inválida no produce este evento.

---

# INV-032 — AuditRecorded representa un hecho consumado

AuditRecorded nunca representa:

- una intención;
- una solicitud;
- una operación futura;
- un mensaje técnico pendiente.

Debe mantenerse:

```text
AuditRecorded

=

Confirmed Domain Fact
```

---

# INV-033 — EventId es obligatorio para AuditRecorded

Todo Domain Event válido debe poseer:

```text
EventId
```

conforme al contrato oficial de Domain Events.

---

# INV-034 — EventId es inmutable

Una vez producido:

```text
EventId
```

no puede cambiar ni reutilizarse para representar otro hecho.

---

# INV-035 — EventId no es AuditId

Debe mantenerse:

```text
AuditRecorded.EventId

≠

AuditId
```

porque representan identidades conceptualmente diferentes.

---

# INV-036 — AggregateVersion del evento representa la Version resultante

Todo Domain Event de Audit debe mantener:

```text
Event.AggregateVersion

=

Resulting Audit.Version
```

---

# INV-037 — SourceAggregateVersion no es Audit.Version

Cuando exista:

```text
SourceAggregateVersion
```

debe mantenerse:

```text
SourceAggregateVersion

≠

Audit.Version
```

como concepto.

Una eventual coincidencia numérica no transforma ambas Versions en
la misma identidad lógica.

---

# INV-038 — SourceAggregateVersion no es AuditRecorded.AggregateVersion

Debe mantenerse:

```text
SourceAggregateVersion

≠

AuditRecorded.AggregateVersion
```

semánticamente.

Cada valor pertenece a un Aggregate diferente.

---

# INV-039 — La creación válida establece Version 1

Después de:

```text
No Audit → Recorded
```

debe resultar:

```text
Audit.Version = 1
```

---

# INV-040 — Toda modificación válida incrementa Version

Si en una evolución futura existe una modificación válida:

```text
Version = N

↓

Valid Modification

↓

Version = N + 1
```

conforme al patrón consolidado de AURA.

---

# INV-041 — Una operación rechazada no incrementa Version

Debe mantenerse:

```text
Rejected Operation

↓

Version Unchanged
```

En creación rechazada no existe una nueva Version persistida.

---

# INV-042 — La lectura no incrementa Version

Consultar o recuperar Audit no constituye una modificación del
Aggregate.

Debe mantenerse:

```text
Read

≠

Version Increment
```

---

# INV-043 — La rehidratación no incrementa Version

Reconstruir un Aggregate desde persistencia o eventos históricos no
constituye una nueva modificación.

Debe mantenerse:

```text
Rehydration

≠

Version Increment
```

---

# INV-044 — CreatedAt es obligatorio después de la creación

Una unidad Audit Recorded debe poseer:

```text
CreatedAt
```

---

# INV-045 — CreatedAt es inmutable

Después de la creación:

```text
CreatedAt
```

no cambia.

---

# INV-046 — CreatedAt no es SourceOccurredAt

Debe mantenerse:

```text
Audit.CreatedAt

≠

SourceOccurredAt
```

semánticamente.

CreatedAt pertenece a Audit.

SourceOccurredAt pertenece al hecho de origen.

---

# INV-047 — AuditRecorded.OccurredAt no es SourceOccurredAt

Debe mantenerse:

```text
AuditRecorded.OccurredAt

≠

SourceOccurredAt
```

semánticamente.

Cada valor representa la ocurrencia de un hecho diferente.

---

# INV-048 — UpdatedAt solamente cambia por modificación válida

Cuando UpdatedAt exista:

```text
UpdatedAt
```

solamente puede cambiar como consecuencia de una modificación
válida del Aggregate.

---

# INV-049 — Operación rechazada no modifica UpdatedAt

Debe mantenerse:

```text
Rejected Operation

↓

UpdatedAt Unchanged
```

---

# INV-050 — Información ausente no se inventa

Si el contrato de origen no proporciona:

```text
ActorId

CorrelationId

CausationId

SourceEventId

SourceAggregateVersion
```

u otra información opcional, Audit no debe fabricar valores.

---

# INV-051 — ActorId no es obligatorio por definición general

ActorId solamente puede conservarse cuando:

- esté disponible;
- sea aplicable;
- pertenezca al contrato auditable.

Su ausencia no invalida automáticamente un hecho auditable salvo que
una regla explícita del dominio establezca lo contrario.

---

# INV-052 — ActorId no concede ownership

La presencia de:

```text
ActorId
```

no convierte Citizen, Membership o Role en entidades internas de
Audit.

---

# INV-053 — Audit no autentica ActorId

Audit no valida credenciales ni identidad técnica asociada al actor.

Authentication permanece fuera del Aggregate.

---

# INV-054 — CorrelationId no es identidad del Aggregate

Debe mantenerse:

```text
CorrelationId

≠

AuditId
```

como concepto.

---

# INV-055 — CausationId no es identidad del Aggregate

Debe mantenerse:

```text
CausationId

≠

AuditId
```

como concepto.

---

# INV-056 — CorrelationId no crea un Consistency Boundary compartido

Dos Aggregates relacionados por:

```text
CorrelationId
```

no pasan a compartir automáticamente la misma transacción.

Debe mantenerse:

```text
Correlated

≠

Atomically Consistent
```

---

# INV-057 — CausationId no permite modificar otro Aggregate

La relación causal no concede autoridad de escritura.

Debe mantenerse:

```text
Causation

≠

Mutation Authority
```

---

# INV-058 — La información auditada debe preservar su significado

Audit no puede transformar retrospectivamente una representación
confirmada para hacerla significar un hecho diferente.

Debe mantenerse:

```text
Recorded Meaning

=

Stable Historical Meaning
```

---

# INV-059 — Un nuevo Source Fact no reescribe un Audit anterior

Si posteriormente ocurre un nuevo hecho:

```text
Source Fact B
```

no debe utilizarse para modificar la representación histórica de:

```text
Source Fact A
```

dentro de una unidad Audit ya confirmada.

---

# INV-060 — Corrección del Source Aggregate es un nuevo hecho

Cuando el Source Aggregate emite posteriormente un hecho correctivo
o complementario:

```text
New Source Fact

≠

Rewrite Existing Audit
```

Audit preserva la trazabilidad histórica de cada hecho conforme a
su contrato.

---

# INV-061 — Diferentes hechos pueden producir diferentes AuditId

Hechos auditables independientes pueden generar unidades Audit
independientes.

Debe mantenerse:

```text
Source Fact A → Audit A

Source Fact B → Audit B
```

sin fusionar ambas identidades.

---

# INV-062 — Audit no hereda Source Status

El estado del Aggregate originador no determina AuditStatus.

Debe mantenerse:

```text
Source Status

≠

Audit Status
```

---

# INV-063 — Failed externo no produce Audit Failed

Un hecho originado desde:

```text
NotificationStatus = Failed
```

no produce:

```text
AuditStatus = Failed
```

Audit permanece Recorded.

---

# INV-064 — Archived externo no produce Audit Archived

Un hecho originado desde un Aggregate en:

```text
Archived
```

no produce:

```text
AuditStatus = Archived
```

porque Archived no pertenece al Lifecycle de Audit versión 1.0.

---

# INV-065 — Fallos técnicos no son estados de Audit

Fallos de:

```text
Persistence

Messaging

Network

Broker

Integration

Infrastructure
```

no producen un AuditStatus.

---

# INV-066 — PersistenceFailure no equivale a estado de dominio

Debe mantenerse:

```text
PersistenceFailure

≠

AuditStatus
```

---

# INV-067 — ConcurrencyConflict no equivale a estado de dominio

Debe mantenerse:

```text
ConcurrencyConflict

≠

AuditStatus
```

---

# INV-068 — Retry técnico no es transición

Un retry técnico no produce:

```text
Recorded → Recorded
```

ni ningún otro cambio de Lifecycle.

---

# INV-069 — Duplicate Delivery no es nuevo hecho

La entrega técnica repetida del mismo mensaje no representa un nuevo
hecho del dominio.

Debe mantenerse:

```text
Duplicate Technical Delivery

≠

New Domain Fact
```

---

# INV-070 — Duplicate Delivery no produce automáticamente nuevo Audit

Una duplicación técnica no debe crear automáticamente otra unidad
Audit para el mismo hecho por el solo hecho de repetirse el
transporte.

La estrategia concreta de idempotencia pertenece a las capas
correspondientes.

---

# INV-071 — Repository no decide Invariants

El Repository no define ni modifica las reglas del Aggregate.

Debe mantenerse:

```text
Repository

≠

Domain Rule Authority
```

---

# INV-072 — Repository no corrige estado inválido

El Repository no debe modificar un Audit inválido para hacerlo
persistible.

El Aggregate debe llegar al Repository ya consistente.

---

# INV-073 — Repository no inventa AuditRecorded

El Repository no produce:

```text
AuditRecorded
```

por decisión propia.

El Domain Event pertenece al comportamiento válido del Aggregate.

---

# INV-074 — Repository persiste una unidad Audit

Audit constituye la unidad de consistencia para persistencia.

No debe persistirse parcialmente de forma que sus Invariants puedan
quedar incumplidas.

---

# INV-075 — Optimistic Concurrency protege Version

Cuando exista una modificación sobre un Audit persistido:

```text
ExpectedVersion

=

PersistedVersion
```

debe cumplirse antes de confirmar la escritura.

---

# INV-076 — Escritura obsoleta no sobrescribe estado confirmado

Cuando:

```text
ExpectedVersion

≠

PersistedVersion
```

la operación debe ser rechazada como conflicto de concurrencia.

---

# INV-077 — Permission no reemplaza Invariant

Debe mantenerse:

```text
Permission

≠

Domain Rule
```

Una operación autorizada todavía debe preservar todas las
Invariants.

---

# INV-078 — Authorized no significa automáticamente válido

Debe mantenerse:

```text
Authorized

≠

Automatically Valid
```

---

# INV-079 — Authorization no permite transición inexistente

Ningún permiso puede crear:

```text
Recorded → Another State
```

cuando dicha transición no pertenece a la State Machine.

---

# INV-080 — Authentication permanece fuera del Aggregate

Audit no:

- valida passwords;
- valida tokens;
- administra sesiones;
- administra OAuth;
- administra JWT;
- administra proveedores de identidad.

---

# INV-081 — Audit no almacena credenciales

No deben formar parte del Aggregate:

```text
Password

AccessToken

RefreshToken

ApiKey

PrivateKey

Secret
```

---

# INV-082 — Domain Event Payload utiliza información mínima

AuditRecorded debe contener únicamente información necesaria para
representar el hecho.

Debe mantenerse:

```text
Domain Event Payload

≠

Aggregate Snapshot
```

---

# INV-083 — Domain Event Payload no incorpora Source Aggregate completo

No está permitido transportar un Aggregate externo completo dentro
de AuditRecorded.

---

# INV-084 — Source Event Payload no se copia automáticamente

Debe mantenerse:

```text
Source Event Payload

≠

Automatic AuditRecorded Payload
```

Solo se conserva información necesaria y permitida.

---

# INV-085 — Domain Events no contienen secretos

AuditRecorded no debe incluir:

- contraseñas;
- tokens;
- claves privadas;
- secretos;
- credenciales técnicas.

---

# INV-086 — Domain Event histórico es inmutable

Una vez producido:

```text
AuditRecorded
```

no debe modificarse retrospectivamente.

---

# INV-087 — Operación rechazada no produce Domain Event de éxito

Debe mantenerse:

```text
Rejected RecordAudit

↓

No AuditRecorded
```

---

# INV-088 — Domain Event no es Integration Event

Debe mantenerse:

```text
AuditRecorded

≠

Integration Event
```

---

# INV-089 — Domain Event no implica Integration Event obligatorio

La existencia de:

```text
AuditRecorded
```

no exige automáticamente publicación externa.

Debe existir un contrato explícito de integración cuando
corresponda.

---

# INV-090 — Integration Event no modifica Audit directamente

Un Integration Event recibido o publicado no puede mutar
directamente el estado interno del Aggregate.

---

# INV-091 — Publicación de Integration Event no incrementa Version

Publicar información derivada de un hecho ya confirmado no
constituye modificación de Audit.

Debe mantenerse:

```text
Integration Publication

≠

Audit Version Increment
```

---

# INV-092 — Retry de publicación no es modificación de Audit

Un retry técnico de publicación no produce:

```text
Audit.Version + 1
```

---

# INV-093 — Read Model no es autoridad de escritura

Debe mantenerse:

```text
Read Model

≠

Write Authority
```

---

# INV-094 — Read Model no modifica Audit

Una proyección no puede:

- ejecutar RecordAudit;
- cambiar AuditStatus;
- cambiar AuditId;
- incrementar Audit.Version;
- producir AuditRecorded como comportamiento del Aggregate.

---

# INV-095 — Read Model puede estar eventualmente desactualizado

Puede existir:

```text
Audit.Version = N

ReadModel.Version < N
```

durante una ventana válida de propagación.

Esto no viola las Invariants internas del Aggregate.

---

# INV-096 — Audit no es Read Model

Debe mantenerse:

```text
Audit Aggregate

≠

Audit Read Model
```

---

# INV-097 — Audit no es Log

Debe mantenerse:

```text
Audit

≠

Application Log
```

y:

```text
Audit

≠

Infrastructure Log
```

---

# INV-098 — Log técnico no es hecho auditable automáticamente

La existencia de una entrada de log no obliga a crear Audit.

Debe mantenerse:

```text
Log Entry

≠

Automatic Auditable Fact
```

---

# INV-099 — Audit no es Observability

Audit no reemplaza:

- logs;
- metrics;
- traces;
- monitoring;
- alerting.

---

# INV-100 — Métrica técnica no es estado de Audit

Debe mantenerse:

```text
Operational Metric

≠

Audit Domain State
```

---

# INV-101 — Audit no es Document

Debe mantenerse:

```text
Audit

≠

Document
```

Audit no se convierte en almacenamiento documental por conservar
información histórica.

---

# INV-102 — Audit no es Notification

Debe mantenerse:

```text
Audit

≠

Notification
```

Audit preserva trazabilidad.

Notification gestiona comunicación.

---

# INV-103 — Audit no es Integration

Debe mantenerse:

```text
Audit

≠

Integration
```

Audit pertenece al dominio de trazabilidad.

Integration mantiene responsabilidades de interoperabilidad.

---

# INV-104 — Audit no es Source of Truth de otros Aggregates

Audit solamente es autoridad sobre su propio estado.

Debe mantenerse:

```text
Audit

≠

Source of Truth for Source Aggregate
```

---

# INV-105 — Source Aggregate permanece autoridad sobre su estado

Cuando Audit registra un hecho externo, el Source Aggregate
mantiene ownership sobre su propio:

- estado;
- Lifecycle;
- Version;
- Invariants;
- Domain Events.

---

# INV-106 — Audit no reconstruye autoritativamente otros Aggregates

La información histórica almacenada por Audit no convierte al
Aggregate Audit en mecanismo autoritativo para reconstruir el Write
Model de otro Aggregate.

---

# INV-107 — Consistencia interna es inmediata

Dentro del Consistency Boundary de Audit, una operación válida debe
producir un resultado internamente consistente.

No puede confirmarse un estado parcial.

---

# INV-108 — Consistencia externa es independiente

La relación entre Audit y otros Aggregates puede mantener:

```text
Eventual Consistency
```

sin exigir una transacción distribuida.

---

# INV-109 — Ventana temporal sin Audit es válida

Puede existir:

```text
Source Fact Confirmed

+

Audit Not Yet Recorded
```

durante una ventana temporal válida.

---

# INV-110 — Fallo posterior de Audit no invalida Source Fact

Un fallo posterior de procesamiento no cambia la validez del hecho
ya confirmado por el Source Aggregate.

---

# INV-111 — No existe eliminación física como transición

Debe mantenerse:

```text
Physical Deletion

≠

Audit State Transition
```

---

# INV-112 — Deleted no es estado

La versión 1.0 no define:

```text
Deleted
```

como AuditStatus.

---

# INV-113 — Archived no es estado

La versión 1.0 no define:

```text
Archived
```

como AuditStatus.

---

# INV-114 — No existe política de retención implícita

La existencia de Audit no permite inferir:

- plazo mínimo;
- plazo máximo;
- expiración;
- archivado automático;
- eliminación automática.

---

# INV-115 — No existe política de anonimización implícita

La versión 1.0 no define automáticamente:

```text
AuditAnonymized
```

ni un estado equivalente.

---

# INV-116 — No existe política de redacción implícita

La versión 1.0 no define:

```text
AuditRedacted
```

ni comportamiento equivalente.

---

# INV-117 — No existe CorrectAudit

La versión 1.0 no define:

```text
CorrectAudit
```

como Command oficial.

---

# INV-118 — No existe AuditCorrected

La versión 1.0 no define:

```text
AuditCorrected
```

como Domain Event.

---

# INV-119 — No existe RetryAudit

La versión 1.0 no define:

```text
RetryAudit
```

como Command.

---

# INV-120 — No existe AuditRetried

La versión 1.0 no define:

```text
AuditRetried
```

como Domain Event.

---

# INV-121 — No existe ArchiveAudit

La versión 1.0 no define:

```text
ArchiveAudit
```

porque Archived no forma parte del Lifecycle.

---

# INV-122 — No existe DeleteAudit

La versión 1.0 no define:

```text
DeleteAudit
```

como Command de dominio.

---

# INV-123 — No existen Commands técnicos

No pertenecen al Aggregate Commands como:

```text
SaveAudit

LoadAudit

PersistAudit

SerializeAudit

PublishAuditMessage

SyncAuditToFIWARE
```

---

# INV-124 — No existen Domain Events técnicos

No pertenecen al Aggregate eventos como:

```text
AuditSaved

AuditLoaded

AuditPersisted

AuditDatabaseUpdated

AuditMessagePublished

AuditFIWARESynced
```

---

# INV-125 — FIWARE permanece fuera del Aggregate

Audit no depende directamente de:

```text
FIWARE

NGSI-LD

Context Broker

Orion
```

---

# INV-126 — Sistemas municipales permanecen fuera del Aggregate

Los contratos o mecanismos municipales no forman parte de la
consistencia interna de Audit.

La traducción pertenece a la frontera de Integration.

---

# INV-127 — Infrastructure no determina las Invariants

Bases de datos, frameworks, brokers, protocolos y proveedores no
pueden modificar las reglas conceptuales del Aggregate.

Debe mantenerse:

```text
Infrastructure Constraint

≠

Domain Invariant
```

salvo que una regla real del dominio sea definida explícitamente.

---

# INV-128 — CQRS no altera las Invariants

La separación Write Side / Read Side no modifica las reglas del
Aggregate.

El Write Model continúa siendo responsable de proteger las
Invariants.

---

# INV-129 — Event Sourcing no altera las Invariants

Si Audit utiliza Event Sourcing:

- AuditId permanece inmutable;
- los eventos históricos permanecen inmutables;
- el replay no ejecuta Commands;
- el replay no produce nuevos Domain Events;
- Version reconstruida debe ser coherente;
- Recorded continúa siendo el único estado oficial.

---

# INV-130 — Rehidratación preserva identidad

Una unidad Audit rehidratada debe conservar exactamente su:

```text
AuditId
```

---

# INV-131 — Rehidratación preserva estado

Una unidad Audit válida rehidratada debe resultar:

```text
Recorded
```

conforme a su historial confirmado.

---

# INV-132 — Rehidratación no genera AuditRecorded

Aplicar un evento histórico no debe producir un nuevo:

```text
AuditRecorded
```

---

# INV-133 — Replay no constituye nuevo hecho

Debe mantenerse:

```text
Event Replay

≠

New Audit Fact
```

---

# INV-134 — EventId preserva identidad del evento

Una entrega duplicada con el mismo:

```text
EventId
```

representa el mismo Domain Event, no un nuevo hecho.

---

# INV-135 — No existe orden global obligatorio

El dominio no requiere un orden total entre todos los Aggregates
Audit.

Debe mantenerse:

```text
Per Aggregate Versioning

≠

Global Audit Ordering
```

---

# INV-136 — AuditRecorded pertenece a Version 1 en creación

Para el modelo versión 1.0:

```text
AuditRecorded.AggregateVersion = 1
```

cuando representa la creación válida de una nueva unidad Audit.

---

# INV-137 — AuditRecorded no se produce antes del estado válido

No puede considerarse confirmado:

```text
AuditRecorded
```

sin que el Aggregate resultante sea válido en:

```text
Recorded
```

---

# INV-138 — Estado y Version se confirman coherentemente

La creación válida debe confirmar coherentemente:

```text
State = Recorded

Version = 1
```

No debe existir un estado parcial confirmado con valores
incompatibles.

---

# INV-139 — Estado y CreatedAt se confirman coherentemente

Una unidad:

```text
Recorded
```

debe poseer CreatedAt válido conforme al contrato temporal del
Aggregate.

---

# INV-140 — State Machine no puede ser evitada

Ningún Command, Repository, Permission, Integration Event,
Read Model o mecanismo técnico puede crear un estado fuera de:

```text
Recorded
```

para Audit versión 1.0.

---

# Validación Previa

Antes de aceptar `RecordAudit` deben validarse todas las Invariants
aplicables.

Conceptualmente:

```text
RecordAudit
    │
    ▼
Validate State Machine
    │
    ▼
Validate Invariants
    │
    ├── Invalid
    │      │
    │      ▼
    │   Reject
    │
    └── Valid
           │
           ▼
        Record
```

---

# Validación Posterior

Después de una operación válida, el Aggregate debe continuar
satisfaciendo todas las Invariants.

Debe mantenerse:

```text
Valid Before

+

Valid Operation

=

Valid After
```

---

# Atomicidad

Todas las Invariants internas del Aggregate deben preservarse dentro
de la misma unidad de consistencia.

No puede confirmarse parcialmente:

```text
AuditId

State

Version

CreatedAt

Audit Traceability Information
```

cuando su combinación deje el Aggregate inválido.

---

# Operaciones Rechazadas

Una operación rechazada debe garantizar:

```text
No New Audit State

No Version Increment

No UpdatedAt Change

No Success Domain Event
```

y no debe modificar ningún Source Aggregate.

---

# Persistencia

El Repository solamente puede persistir un Aggregate que ya cumpla
las Invariants.

Debe mantenerse:

```text
Domain Validity

before

Persistence
```

La persistencia no reemplaza la validación del dominio.

---

# Consistencia con Lifecycle

Las Invariants deben permanecer coherentes con:

```text
No Audit → Recorded
```

y no pueden introducir indirectamente estados adicionales.

---

# Consistencia con State Machine

Las Invariants no pueden permitir una transición que:

```text
DOMAIN-012B-State-Machine.md
```

prohíba.

---

# Consistencia con Commands

Las Invariants deben aplicarse al único Command oficial:

```text
RecordAudit
```

conforme a:

```text
DOMAIN-012C-Commands.md
```

---

# Consistencia con Domain Events

Las Invariants deben garantizar que:

```text
AuditRecorded
```

solamente represente una operación válida y confirmada.

---

# Consistencia con Permissions

Permissions determinan si una intención puede intentar ejecutarse.

Invariants determinan si la operación puede producir un estado
válido.

Debe mantenerse:

```text
Authorized

+

Invalid Domain Operation

=

Rejected
```

---

# Consistencia con Repository

El Repository:

- no redefine Invariants;
- no elimina Invariants;
- no modifica Invariants;
- no inventa estado;
- no inventa Domain Events.

---

# Consistencia con Read Models

Read Models pueden representar información derivada de Audit.

Nunca pueden utilizarse para evitar las Invariants del Write Model.

---

# Consistencia con Integration

Integration puede transportar información hacia o desde otros
límites.

Ningún mensaje externo puede modificar directamente Audit evitando
sus Invariants.

---

# Consistencia con Security

El Security Model debe proteger las Invariants sin reemplazarlas.

Debe mantenerse:

```text
Security

supports

Domain Integrity
```

pero:

```text
Security

≠

Domain Invariant Definition
```

---

# Consistencia con Performance

Ninguna optimización puede eliminar:

- validación de Invariants;
- control de Version;
- protección de identidad;
- State Machine;
- Consistency Boundary.

Debe mantenerse:

```text
Performance Optimization

≠

Invariant Bypass
```

---

# Reglas Fundamentales

Las Invariants de Audit establecen que:

1. Audit posee AuditId obligatorio.
2. AuditId es inmutable.
3. AuditId identifica exclusivamente a Audit.
4. AuditId no se reutiliza.
5. Recorded es el único estado persistido.
6. No Audit representa inexistencia.
7. Toda unidad Audit comienza en Recorded.
8. Recorded es terminal.
9. No existen estados adicionales en versión 1.0.
10. La única transición es No Audit → Recorded.
11. El estado no puede modificarse directamente.
12. Toda modificación pasa por la Aggregate Root.
13. RecordAudit es el único Command oficial.
14. RecordAudit solamente produce Recorded.
15. El hecho auditable debe estar confirmado previamente.
16. Audit no registra intenciones futuras como hechos.
17. Audit no crea el Source Fact.
18. Audit no modifica el Source Fact.
19. Audit no modifica el Source Aggregate.
20. Un fallo de Audit no revierte el Source Aggregate.
21. Source Aggregate y Audit poseen transacciones independientes.
22. Las referencias externas no incorporan Aggregates completos.
23. SourceAggregateId permanece distinto de AuditId.
24. SourceEventId permanece distinto de AuditId.
25. Source Domain Event conserva ownership externo.
26. Source Domain Event permanece distinto de Audit.
27. Source Domain Event permanece distinto de AuditRecorded.
28. Audit permanece distinto de AuditRecorded.
29. AuditRecorded es el único Domain Event oficial.
30. AuditRecorded solamente ocurre después de RecordAudit válido.
31. AuditRecorded representa un hecho consumado.
32. EventId es único e inmutable.
33. EventId permanece distinto de AuditId.
34. Event.AggregateVersion coincide con Audit.Version resultante.
35. SourceAggregateVersion permanece independiente.
36. La creación válida establece Version = 1.
37. Operaciones rechazadas no incrementan Version.
38. Lecturas no incrementan Version.
39. Rehidratación no incrementa Version.
40. CreatedAt existe y permanece inmutable.
41. CreatedAt no equivale a SourceOccurredAt.
42. UpdatedAt cambia únicamente por modificación válida.
43. Información ausente no se inventa.
44. ActorId es opcional cuando el contrato así lo permita.
45. ActorId no concede ownership.
46. CorrelationId no es identidad del Aggregate.
47. CausationId no es identidad del Aggregate.
48. Correlación no fusiona Consistency Boundaries.
49. Causalidad no concede autoridad de modificación.
50. El significado histórico permanece estable.
51. Nuevos Source Facts no reescriben Audits anteriores.
52. Audit no hereda Source Status.
53. Fallos técnicos no son estados de Audit.
54. Retries técnicos no son transiciones.
55. Duplicados técnicos no son nuevos hechos.
56. Repository no decide reglas de dominio.
57. Repository no corrige estados inválidos.
58. Repository no inventa Domain Events.
59. Repository persiste Audit como unidad.
60. Optimistic Concurrency protege Version.
61. Permissions no reemplazan Invariants.
62. Authentication permanece fuera del Aggregate.
63. Audit no almacena credenciales.
64. Event Payload utiliza información mínima.
65. Source Payload no se copia automáticamente.
66. Domain Events no contienen secretos.
67. Eventos históricos permanecen inmutables.
68. Operaciones rechazadas no producen Domain Event de éxito.
69. Domain Event permanece distinto de Integration Event.
70. Domain Event no implica Integration Event obligatorio.
71. Integration no modifica Audit directamente.
72. Publicación externa no incrementa Audit.Version.
73. Read Models no poseen autoridad de escritura.
74. Audit no es Log.
75. Audit no es Observability.
76. Audit no es Document.
77. Audit no es Notification.
78. Audit no es Integration.
79. Audit no es Source of Truth de otros Aggregates.
80. Consistencia interna es inmediata.
81. Consistencia externa puede ser eventual.
82. Puede existir una ventana con Source Fact confirmado y Audit aún
    no registrado.
83. Eliminación física no constituye transición.
84. Archived y Deleted no son estados oficiales.
85. No existen políticas de retención implícitas.
86. No existen políticas de anonimización o redacción implícitas.
87. No existen Commands o Domain Events de corrección, retry,
    archivado o eliminación.
88. Operaciones técnicas no son Commands.
89. Hechos técnicos no son Domain Events.
90. FIWARE e Infrastructure permanecen fuera del Aggregate.
91. CQRS no altera Invariants.
92. Event Sourcing no altera Invariants.
93. Rehidratación preserva identidad, estado y Version.
94. No existe orden global obligatorio entre Audits.
95. AuditRecorded corresponde a AggregateVersion = 1 en la creación.
96. State, Version y CreatedAt se confirman coherentemente.
97. Ningún mecanismo puede evitar la State Machine.
98. Toda operación válida debe preservar todas las Invariants
    aplicables.

---

# Restricciones

No está permitido:

- crear Audit sin AuditId;
- modificar AuditId;
- reutilizar AuditId para otra identidad;
- utilizar SourceAggregateId como AuditId;
- utilizar SourceEventId como AuditId;
- crear estados distintos de Recorded;
- modificar State directamente;
- registrar hechos futuros como consumados;
- tratar un Command externo como Domain Event confirmado;
- modificar el Source Fact;
- modificar el Source Aggregate;
- realizar rollback del Source Aggregate desde Audit;
- almacenar Aggregates externos completos;
- fabricar información ausente;
- confundir SourceAggregateVersion con Audit.Version;
- incrementar Version ante rechazo;
- modificar CreatedAt;
- producir AuditRecorded ante operación rechazada;
- modificar Domain Events históricos;
- copiar automáticamente Payloads externos completos;
- incluir secretos o credenciales;
- utilizar Repository para corregir Invariants;
- utilizar Permissions para evitar la State Machine;
- utilizar Read Models como Write Model;
- utilizar Integration Events para mutar Audit directamente;
- convertir fallos técnicos en estados;
- convertir retries técnicos en Commands;
- convertir logs o métricas en estado de Audit;
- introducir políticas de retención sin definición explícita;
- introducir estados, Commands o Events no consolidados.

---

# Compatibilidad Arquitectónica

Las Invariants de Audit son compatibles con:

- Domain-Driven Design;
- Aggregate Pattern;
- Tactical DDD;
- Clean Architecture;
- Hexagonal Architecture;
- SOLID;
- CQRS;
- Event-Driven Architecture;
- Event Sourcing Compatible;
- Optimistic Concurrency Control;
- Transactional Outbox;
- consistencia eventual;
- High Cohesion;
- Low Coupling.

Estas compatibilidades no modifican ninguna Invariant ni introducen
dependencias tecnológicas.

---

# Definición de Éxito

Las Invariants del Aggregate **Audit** garantizan que toda unidad de
trazabilidad permanezca conceptualmente válida durante toda su
existencia.

El modelo protege:

```text
AuditId

Recorded State

Source References

Traceability Information

Version

CreatedAt

UpdatedAt

AuditRecorded
```

y garantiza que:

- AuditId existe y permanece inmutable;
- Recorded es el único estado oficial;
- No Audit representa únicamente inexistencia;
- la única transición válida es No Audit → Recorded;
- RecordAudit es el único Command oficial;
- el hecho auditado debe haber ocurrido antes de Audit;
- Audit no crea, modifica ni revierte el Source Fact;
- Audit no modifica el Source Aggregate;
- los límites transaccionales permanecen separados;
- SourceAggregateId y SourceEventId no sustituyen AuditId;
- Source Domain Event permanece distinto de Audit y AuditRecorded;
- AuditRecorded es el único Domain Event oficial;
- EventId permanece único e independiente;
- AggregateVersion corresponde a la Version resultante de Audit;
- SourceAggregateVersion permanece independiente;
- Version evoluciona únicamente mediante modificaciones válidas;
- CreatedAt permanece inmutable;
- UpdatedAt cambia únicamente cuando existe modificación válida;
- información ausente no se inventa;
- ActorId, CorrelationId y CausationId conservan únicamente su
  significado de trazabilidad;
- el significado histórico no se reescribe;
- nuevos hechos de origen no modifican Audits anteriores;
- Audit no hereda estados externos;
- fallos, retries y duplicados técnicos permanecen fuera del
  Lifecycle;
- Repository no altera reglas del dominio;
- Optimistic Concurrency protege escrituras;
- Permissions no sustituyen Invariants;
- Authentication permanece fuera del Aggregate;
- Payloads permanecen mínimos y sin secretos;
- Domain Events e Integration Events permanecen separados;
- Read Models no poseen autoridad de escritura;
- Audit permanece separado de Logs, Observability, Document,
  Notification e Integration;
- consistencia interna permanece inmediata;
- consistencia con otros Aggregates puede ser eventual;
- no se introducen reglas de retención, eliminación, corrección,
  anonimización o archivado sin definición explícita;
- CQRS, Event Sourcing e Infrastructure no alteran las reglas
  conceptuales del Aggregate.

De esta forma, `DOMAIN-012E-Invariants.md` establece las Invariants
oficiales del Aggregate **Audit** conforme al patrón consolidado de
AURA Core.