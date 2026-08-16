# DOMAIN-012K — Audit Integration Events

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
- DOMAIN-012H-Examples.md
- DOMAIN-012I-Versioning.md
- DOMAIN-012J-Consistency-Boundary.md
- DOMAIN-012L-Read-Model.md
- DOMAIN-012M-Test-Scenarios.md
- DOMAIN-012O-Security-Model.md

---

# Objetivo

Este documento define formalmente los **Integration Events**
asociados al Aggregate **Audit**.

Los Integration Events representan contratos públicos utilizados
cuando un hecho confirmado de Audit debe comunicarse fuera de su
Bounded Context.

Debe mantenerse:

```text
Domain Event

≠

Integration Event
```

y:

```text
Integration Event

≠

Aggregate State
```

---

# Principio Fundamental

Audit produce Domain Events dentro de su propio Consistency Boundary.

La versión 1.0 define:

```text
AuditRecorded
```

como único Domain Event oficial.

Cuando exista una necesidad explícita de integración, dicho hecho
puede transformarse en:

```text
AuditRecordedIntegrationEvent
```

Debe mantenerse:

```text
AuditRecorded

≠

AuditRecordedIntegrationEvent
```

---

# Integración no Automática

La existencia de:

```text
AuditRecorded
```

no obliga automáticamente a publicar:

```text
AuditRecordedIntegrationEvent
```

Debe existir una necesidad explícita de comunicación entre Bounded
Contexts o hacia un sistema externo.

Debe mantenerse:

```text
Domain Event

≠

Mandatory Integration Event
```

---

# Integration Event Oficial

La versión 1.0 define conceptualmente:

```text
AuditRecordedIntegrationEvent
```

como contrato de integración asociado al hecho:

```text
AuditRecorded
```

únicamente cuando exista un consumidor o contrato de integración que
requiera dicho hecho.

---

# Relación Oficial

La relación conceptual es:

```text
AuditRecorded

    │
    ▼

Integration Boundary

    │
    ▼

AuditRecordedIntegrationEvent
```

Esta transformación ocurre fuera del Aggregate Audit.

---

# AuditRecordedIntegrationEvent

`AuditRecordedIntegrationEvent` representa públicamente el hecho de
que una unidad Audit fue registrada válidamente.

Puede utilizarse para comunicar dicho hecho hacia:

- otros Bounded Contexts;
- sistemas externos;
- plataformas municipales;
- ecosistemas Smart City;
- FIWARE;
- consumidores analíticos;
- otros sistemas autorizados.

cuando exista un contrato explícito.

---

# Significado

El evento significa:

```text
An Audit unit was recorded
```

dentro de AURA y dicho hecho ha sido seleccionado para comunicación
externa.

No significa:

- que el Source Aggregate haya cambiado nuevamente;
- que el Source Domain Event haya sido modificado;
- que Audit haya cambiado después de Recorded;
- que un consumidor haya procesado exitosamente el mensaje;
- que un Read Model se encuentre actualizado;
- que FIWARE haya confirmado una operación;
- que una plataforma municipal haya aplicado el evento.

---

# Contract Envelope

Todo Integration Event de Audit debe representar conceptualmente:

```text
EventId

EventType

AggregateId

AggregateType

OccurredOn

Version

CorrelationId

CausationId

Payload
```

cuando los elementos correspondientes sean aplicables.

---

# AggregateId

Para Audit:

```text
AggregateId = AuditId
```

`AggregateId` identifica el Aggregate que produjo el hecho original
de dominio.

---

# AggregateType

Para Audit:

```text
AggregateType = Audit
```

---

# EventId

EventId identifica de forma única el Integration Event.

Debe:

- ser único;
- ser inmutable;
- identificar un único mensaje lógico;
- permitir procesamiento idempotente.

Debe mantenerse:

```text
IntegrationEvent.EventId

≠

AuditId
```

---

# EventType

Para la versión 1.0:

```text
EventType = AuditRecordedIntegrationEvent
```

EventType representa semántica pública.

No debe utilizar nombres propios de:

- tablas;
- brokers;
- endpoints;
- bases de datos;
- frameworks;
- proveedores.

---

# OccurredOn

`OccurredOn` representa el momento asociado al hecho que se comunica
mediante el contrato de integración.

Debe mantenerse conceptualmente separado de:

```text
SourceOccurredAt

Audit.CreatedAt

AuditRecorded.OccurredAt
```

cuando dichos valores representen hechos distintos.

---

# Version

`Version` dentro del Integration Event representa la versión del
contrato público correspondiente.

Debe mantenerse:

```text
Integration Contract Version

≠

Audit.Version
```

y:

```text
Integration Contract Version

≠

AuditRecorded.AggregateVersion
```

---

# AggregateVersion

Cuando el contrato requiera conservar la Version del Aggregate que
originó el hecho, dicha información puede incluirse explícitamente
dentro del Payload o contrato correspondiente.

Debe mantenerse:

```text
Audit.AggregateVersion

≠

Integration Contract Version
```

---

# CorrelationId

CorrelationId permite relacionar el Integration Event con el flujo
que originó Audit cuando dicha información esté disponible.

Conceptualmente:

```text
Source Domain Fact
    │
    │ CorrelationId
    ▼
RecordAudit
    │
    │ CorrelationId
    ▼
AuditRecorded
    │
    │ CorrelationId
    ▼
AuditRecordedIntegrationEvent
```

Esta correlación no fusiona Consistency Boundaries.

---

# CausationId

CausationId puede preservar la relación causal inmediata del
Integration Event cuando corresponda.

No constituye:

- AuditId;
- EventId;
- Version;
- Permission.

---

# Payload

El Payload debe contener únicamente la información necesaria para el
contrato público.

Debe mantenerse:

```text
Integration Event Payload

=

Minimum Required Public Information
```

No constituye una copia completa del Aggregate.

---

# Payload Conceptual

`AuditRecordedIntegrationEvent` puede incluir conceptualmente:

```text
AuditId

SourceAggregateId

SourceAggregateType

SourceEventId

SourceEventType

SourceAggregateVersion

ActorId

SourceOccurredAt

AggregateVersion
```

únicamente cuando cada elemento:

- sea necesario para el contrato;
- esté disponible;
- sea permitido;
- tenga significado para el consumidor.

---

# Minimización

Debe mantenerse:

```text
Audit Aggregate State

≠

Automatic Integration Payload
```

y:

```text
AuditRecorded Payload

≠

Automatic Integration Payload
```

El contrato público debe contener únicamente la información necesaria.

---

# Información Ausente

Un Integration Event no debe inventar información inexistente.

Si Audit no posee:

```text
ActorId

SourceEventId

CorrelationId

CausationId
```

u otra referencia opcional, la transformación no debe fabricar dicho
valor.

---

# SourceAggregateId

Cuando se publique:

```text
SourceAggregateId
```

continúa representando la identidad del Aggregate originador.

No representa:

```text
AuditId
```

---

# SourceAggregateType

Cuando se publique:

```text
SourceAggregateType
```

representa el tipo conceptual del Aggregate originador.

No expone obligatoriamente su estructura interna.

---

# SourceEventId

Cuando el Audit proviene de un Source Domain Event:

```text
SourceEventId
```

puede comunicarse si el contrato lo requiere.

Debe mantenerse:

```text
SourceEventId

≠

IntegrationEvent.EventId
```

---

# SourceEventType

`SourceEventType` puede utilizarse para comunicar el tipo del hecho
originador cuando sea relevante para el consumidor.

El Integration Event no redefine su significado histórico.

---

# SourceAggregateVersion

Puede incluirse:

```text
SourceAggregateVersion
```

cuando sea necesaria para trazabilidad externa.

Debe mantenerse:

```text
SourceAggregateVersion

≠

Audit.Version
```

y:

```text
SourceAggregateVersion

≠

Integration Contract Version
```

---

# ActorId

ActorId puede incluirse únicamente cuando:

- exista en Audit;
- sea necesario para el contrato;
- la política de seguridad lo permita;
- la minimización de datos lo permita.

Su existencia no concede Authorization.

---

# Datos Personales

La existencia de información personal dentro de Audit no obliga a
publicarla.

Debe mantenerse:

```text
Data Exists in Audit

≠

Data Must Be Integrated
```

---

# Domain Event versus Integration Event

`AuditRecorded` pertenece al dominio interno.

`AuditRecordedIntegrationEvent` pertenece al contrato de integración.

Debe mantenerse:

```text
AuditRecorded

=

Internal Domain Fact
```

mientras:

```text
AuditRecordedIntegrationEvent

=

Public Integration Contract
```

---

# Ownership

Audit es propietario de:

```text
AuditRecorded
```

El Integration Boundary es responsable de transformar dicho hecho
cuando exista una necesidad externa.

El Aggregate no es responsable de construir directamente contratos
externos.

---

# Aggregate no Publica Contratos Externos

Audit no ejecuta directamente:

```text
publishIntegrationEvent()
```

como comportamiento de dominio.

Debe mantenerse:

```text
Aggregate Behavior

≠

Integration Transport
```

---

# Application e Integration

La transformación conceptual ocurre fuera de Audit.

```text
AuditRecorded
    │
    ▼
Application / Integration
    │
    ▼
AuditRecordedIntegrationEvent
```

Audit permanece independiente del mecanismo utilizado.

---

# Commit Antes de Publicación

Un Integration Event solamente debe publicarse después de que el
hecho de Audit haya sido confirmado.

Debe mantenerse:

```text
Audit Commit

before

Integration Publication
```

---

# Flujo Oficial

Conceptualmente:

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
AuditRepository
    │
    ▼
Commit
    │
    ▼
Integration Boundary
    │
    ▼
AuditRecordedIntegrationEvent
    │
    ▼
Consumer
```

---

# Publicación Antes del Commit

No debe considerarse un flujo válido:

```text
Publish AuditRecordedIntegrationEvent

    │
    ▼

Attempt Audit Commit
```

porque podría comunicarse externamente un hecho que todavía no está
confirmado.

---

# Transactional Outbox

Cuando la arquitectura utilice:

```text
Transactional Outbox
```

puede coordinarse conceptualmente:

```text
Audit Commit

    │
    ▼

Outbox

    │
    ▼

Dispatcher

    │
    ▼

AuditRecordedIntegrationEvent
```

La implementación concreta permanece fuera del dominio.

---

# Outbox no es Audit

Debe mantenerse:

```text
Outbox

≠

Audit Aggregate
```

y:

```text
Outbox State

≠

AuditStatus
```

---

# Estados Técnicos de Outbox

Estados como:

```text
Pending

Published

Failed

Retrying
```

pertenecen a la infraestructura o coordinación de publicación.

No forman parte del Lifecycle de Audit.

---

# Retry de Publicación

Un retry técnico de publicación no modifica Audit.

Debe mantenerse:

```text
Integration Publication Retry

≠

Audit Modification
```

y:

```text
Integration Publication Retry

≠

RecordAudit
```

---

# Retry no Incrementa Version

Si Audit ya se encuentra:

```text
Recorded

Audit.Version = 1
```

un retry de publicación mantiene:

```text
Audit.Version = 1
```

---

# Fallo de Publicación

Si:

```text
AuditRecordedIntegrationEvent
```

no puede publicarse correctamente, Audit permanece:

```text
Recorded
```

y conserva:

```text
Audit.Version
```

sin cambios.

---

# Fallo Externo

Un consumidor puede fallar procesando el Integration Event.

Dicho fallo no modifica retroactivamente:

- AuditId;
- AuditStatus;
- Audit.Version;
- AuditRecorded.

Debe mantenerse:

```text
Consumer Failure

≠

Audit Rollback
```

---

# Consistencia Eventual

La comunicación hacia consumidores externos utiliza consistencia
eventual.

Puede existir:

```text
Audit committed

+

Consumer not yet updated
```

durante una ventana temporal válida.

---

# Garantías Conceptuales

La integración debe preservar:

- publicación posterior al commit;
- independencia entre productor y consumidor;
- consistencia eventual;
- EventId único;
- trazabilidad;
- correlación cuando corresponda;
- causalidad cuando corresponda;
- minimización de datos;
- contratos versionables;
- procesamiento idempotente.

---

# Idempotencia

Un mismo Integration Event puede ser entregado más de una vez por la
infraestructura.

Los consumidores deben poder reconocer duplicados mediante:

```text
EventId
```

Debe mantenerse:

```text
Same EventId

=

Same Integration Event
```

---

# Duplicate Delivery

Una entrega duplicada no representa:

```text
New AuditRecordedIntegrationEvent Fact
```

ni:

```text
New Audit
```

Debe mantenerse:

```text
Duplicate Delivery

≠

New Domain Fact
```

---

# Idempotencia del Consumidor

Un consumidor debe poder procesar de forma segura un evento
previamente recibido.

La estrategia técnica específica permanece fuera del contrato de
dominio.

---

# Orden

Los Integration Events no requieren un orden global entre todos los
Audit Aggregates.

Debe mantenerse:

```text
Per Aggregate Ordering

≠

Global Ordering
```

---

# AggregateVersion y Orden

Cuando sea necesario preservar el orden lógico de hechos de una
identidad Audit, puede utilizarse:

```text
AggregateVersion
```

dentro del contrato correspondiente.

La versión 1.0 define:

```text
AuditRecorded

AggregateVersion = 1
```

para creación válida.

---

# Contract Versioning

Los Integration Events poseen versionado contractual independiente.

Debe mantenerse:

```text
Integration Contract Version

≠

Aggregate Version
```

Cambiar un contrato público no modifica Audit.

---

# Cambio Compatible

Una evolución compatible del contrato puede agregar información
opcional conforme a las reglas de compatibilidad aplicables.

Dicha evolución no modifica:

```text
Audit.Version
```

ni:

```text
AuditStatus
```

---

# Cambio Incompatible

Un cambio incompatible del contrato debe utilizar una evolución
explícita del Integration Contract.

No debe reinterpretar silenciosamente un evento histórico existente.

---

# Evento Histórico

Una instancia ya publicada de:

```text
AuditRecordedIntegrationEvent
```

conserva su significado histórico.

Debe mantenerse:

```text
Historical Integration Event

=

Stable Meaning
```

---

# Integration Event no es Source of Truth

Debe mantenerse:

```text
Integration Event

≠

Audit Source of Truth
```

El Write Model Audit conserva autoridad sobre su propio estado.

---

# Integration Event no es Read Model

Debe mantenerse:

```text
Integration Event

≠

Audit Read Model
```

Un consumidor puede usar el evento para construir una proyección,
pero el mensaje no es la proyección misma.

---

# Read Models Externos

Un consumidor puede utilizar:

```text
AuditRecordedIntegrationEvent
```

para actualizar una proyección externa.

Conceptualmente:

```text
AuditRecordedIntegrationEvent
    │
    ▼
External Projection
    │
    ▼
External Read Model
```

La proyección permanece fuera del Consistency Boundary de Audit.

---

# Read Model Interno

Un Read Model interno de Audit puede proyectarse directamente desde
Domain Events conforme al patrón CQRS.

No se requiere utilizar Integration Events dentro del mismo Bounded
Context por definición de este documento.

---

# CQRS

Conceptualmente:

```text
Write Side

RecordAudit
    │
    ▼
Audit
    │
    ▼
AuditRecorded
```

puede alimentar:

```text
Internal Projection
```

mientras una necesidad externa puede utilizar:

```text
AuditRecorded
    │
    ▼
Integration Boundary
    │
    ▼
AuditRecordedIntegrationEvent
```

---

# Event Sourcing

Audit permanece compatible con Event Sourcing.

Si Event Sourcing se utiliza, el historial autoritativo interno
corresponde a:

```text
Audit Domain Events
```

no a:

```text
Integration Events
```

Debe mantenerse:

```text
Domain Event Stream

≠

Integration Event Stream
```

---

# Rehidratación

Audit no debe reconstruirse autoritativamente desde Integration
Events por definición del Aggregate.

Debe mantenerse:

```text
Audit Rehydration

from

Domain State / Domain Events
```

según la estrategia de persistencia.

---

# Integration Event no Ejecuta Command

La recepción de un:

```text
AuditRecordedIntegrationEvent
```

por un consumidor no ejecuta automáticamente:

```text
RecordAudit
```

sobre el mismo Aggregate.

---

# No Recursividad Automática

Audit no debe consumir su propio:

```text
AuditRecordedIntegrationEvent
```

para producir automáticamente otro:

```text
RecordAudit
```

sin una regla explícita.

Debe mantenerse:

```text
Audit Integration Event

≠

Automatic Recursive Audit
```

---

# Organization como Consumidor

Organization puede reaccionar a información de Audit cuando exista un
contrato explícito.

No puede modificar directamente Audit.

---

# Citizen como Consumidor

Citizen Management puede consumir información pública de Audit cuando
exista una necesidad definida.

Dicho consumo no convierte Citizen en parte del Aggregate Audit.

---

# Membership como Consumidor

Membership puede reaccionar a un Integration Event de Audit cuando
corresponda.

Audit no modifica Membership directamente.

---

# Role como Consumidor

Role Management puede consumir un contrato de Audit cuando exista una
necesidad explícita.

El Integration Event no asigna ni revoca Roles por sí mismo.

---

# Territory como Consumidor

Territory puede utilizar información publicada de Audit sin compartir
Consistency Boundary.

---

# Assembly como Consumidor

Assembly puede reaccionar a hechos publicados por Audit únicamente
mediante contratos explícitos.

Un Audit Integration Event no modifica directamente:

```text
AssemblyStatus

Assembly.Version
```

---

# Proposal como Consumidor

Proposal puede consumir información de Audit cuando corresponda.

No existe modificación directa desde el Integration Event.

---

# Participation como Consumidor

Participation puede reaccionar a información Audit sin que:

```text
Participation Transaction

=

Audit Transaction
```

---

# Voting como Consumidor

Un Integration Event de Audit no:

- registra votos;
- abre Voting;
- cierra Voting;
- modifica resultados;
- modifica VotingStatus.

Cualquier reacción pertenece al dominio Voting.

---

# Document como Consumidor

Un Integration Event de Audit no modifica directamente:

```text
DocumentStatus

Document.Version

Document Content

Document Lifecycle
```

---

# Notification como Consumidor

Notification puede reaccionar a un hecho publicado desde Audit cuando
exista un caso de dominio explícito.

El Integration Event no modifica directamente:

```text
NotificationStatus

Notification.Version
```

---

# Integration como Consumidor

Integration Management puede transformar o enrutar contratos públicos
hacia sistemas externos.

Audit no conoce los mecanismos técnicos utilizados.

---

# Analytics

Analytics puede consumir Integration Events para construir:

- indicadores;
- métricas de negocio;
- reportes;
- proyecciones históricas;
- modelos analíticos.

Analytics permanece fuera del Aggregate.

---

# Sistemas Externos

Los consumidores externos pueden incluir:

```text
Municipal Platforms

Smart City Platforms

FIWARE

Authorized External Systems
```

únicamente mediante contratos de integración explícitos.

---

# FIWARE

La eventual comunicación hacia FIWARE ocurre fuera de Audit.

Conceptualmente:

```text
AuditRecorded
    │
    ▼
AuditRecordedIntegrationEvent
    │
    ▼
Integration
    │
    ▼
FIWARE Representation
```

Audit no conoce:

```text
NGSI-LD

Context Broker

Orion
```

como parte de su Domain Model.

---

# FIWARE Representation

La representación de un hecho Audit como una entidad o actualización
de contexto FIWARE pertenece a Integration.

Debe mantenerse:

```text
AuditRecordedIntegrationEvent

≠

NGSI-LD Entity
```

---

# Sistemas Municipales

La publicación hacia plataformas municipales puede requerir una
traducción específica.

Dicha traducción no modifica el Integration Event interno definido
por AURA.

---

# Anti-Corruption Layer

Cuando un sistema externo utiliza conceptos diferentes, debe
aplicarse una traducción en la frontera correspondiente.

Debe mantenerse:

```text
External Message

≠

AURA Integration Event
```

salvo equivalencia explícitamente definida.

---

# Seguridad

Los Integration Events no deben incluir:

- passwords;
- access tokens;
- refresh tokens;
- API keys;
- private keys;
- secretos;
- credenciales;
- sesiones;
- configuración sensible de Infrastructure.

---

# Minimización de Datos

Un Integration Event debe contener solamente la información necesaria
para su propósito público.

Debe mantenerse:

```text
Minimum Necessary Data
```

como principio.

---

# Información Sensible

Información sensible solamente puede incluirse cuando:

- sea necesaria;
- esté permitida;
- exista una política aplicable;
- el consumidor esté autorizado;
- se respete minimización.

---

# ActorId y Privacidad

La existencia de ActorId dentro de Audit no obliga a publicarlo.

Debe mantenerse:

```text
ActorId in Audit

≠

ActorId in Every Integration Event
```

---

# Authorization

La recepción de un Integration Event no concede automáticamente
Permission sobre Audit.

Debe mantenerse:

```text
Integration Event

≠

Authorization Grant
```

---

# Authentication

Los mecanismos técnicos utilizados para autenticar productor y
consumidor permanecen fuera del Integration Event como concepto de
dominio.

---

# Tokens

Los tokens utilizados para transportar un mensaje no forman parte de
su Payload de dominio.

Debe mantenerse:

```text
Transport Credential

∉

Integration Payload
```

---

# Firmas

Una eventual firma técnica del mensaje pertenece a Infrastructure o
Security.

No modifica la semántica del Integration Event.

---

# Transporte

AuditRecordedIntegrationEvent no depende de:

```text
Kafka

RabbitMQ

NATS

Redis

HTTP

REST

Webhook

AMQP

MQTT
```

ni de otro mecanismo de transporte específico.

---

# Serialización

La representación física puede utilizar:

```text
JSON

Avro

Protobuf

MessagePack
```

u otra tecnología.

La elección pertenece a Integration e Infrastructure.

---

# Broker

El broker no forma parte del Domain Model.

Debe mantenerse:

```text
Broker

≠

Integration Event Semantics
```

---

# Delivery Guarantee

La estrategia técnica concreta de entrega:

- at-most-once;
- at-least-once;
- exactly-once processing;

no se define como regla del Aggregate.

El contrato debe permitir manejo seguro de duplicados mediante
identidad de evento.

---

# EventId e Idempotencia

El principio fundamental es:

```text
EventId

identifies

One Logical Integration Event
```

Un consumidor puede utilizar EventId para reconocer una entrega ya
procesada.

---

# CorrelationId y Trazabilidad

Cuando esté disponible, CorrelationId permite reconstruir
conceptualmente:

```text
Source Fact
    │
    ▼
Audit
    │
    ▼
AuditRecorded
    │
    ▼
AuditRecordedIntegrationEvent
    │
    ▼
External Consumer
```

sin fusionar sus límites de consistencia.

---

# CausationId y Trazabilidad

Cuando esté disponible, CausationId puede expresar la causa inmediata
del Integration Event.

Su utilización no concede autoridad sobre ningún Aggregate.

---

# Observability

Traces, logs y metrics pueden utilizar CorrelationId o EventId para
observabilidad técnica.

Esto no convierte Observability en parte del Integration Event
Domain Model.

---

# Logs

Un log generado durante publicación no es:

```text
AuditRecordedIntegrationEvent
```

Debe mantenerse:

```text
Integration Log

≠

Integration Event
```

---

# Error Técnico

Eventos técnicos como:

```text
AuditIntegrationPublishFailed

AuditIntegrationRetried

AuditBrokerUnavailable

AuditMessageSerialized
```

no forman parte automáticamente de los Integration Events del
dominio.

---

# No Eventos Técnicos Oficiales

La versión 1.0 no define Integration Events como:

```text
AuditSavedIntegrationEvent

AuditPersistedIntegrationEvent

AuditPublishedIntegrationEvent

AuditSyncedIntegrationEvent

AuditFIWARESyncedIntegrationEvent
```

porque representan operaciones técnicas y no hechos públicos del
dominio Audit.

---

# No AuditArchivedIntegrationEvent

La versión 1.0 no define:

```text
AuditArchivedIntegrationEvent
```

porque:

```text
AuditArchived
```

no existe como Domain Event.

---

# No AuditDeletedIntegrationEvent

La versión 1.0 no define:

```text
AuditDeletedIntegrationEvent
```

porque:

```text
AuditDeleted
```

no existe como Domain Event.

---

# No AuditRetriedIntegrationEvent

La versión 1.0 no define:

```text
AuditRetriedIntegrationEvent
```

porque:

```text
AuditRetried
```

no existe como Domain Event.

---

# No AuditCorrectedIntegrationEvent

La versión 1.0 no define:

```text
AuditCorrectedIntegrationEvent
```

porque:

```text
AuditCorrected
```

no existe como Domain Event.

---

# Relación Domain Event / Integration Event

La relación oficial versión 1.0 es:

| Domain Event | Integration Event posible |
|---|---|
| AuditRecorded | AuditRecordedIntegrationEvent |

La transformación ocurre solamente cuando exista una necesidad
explícita de integración.

---

# Relación con Lifecycle

AuditRecordedIntegrationEvent representa un hecho derivado de:

```text
No Audit → Recorded
```

No crea una nueva transición.

---

# Relación con State Machine

El Integration Event no modifica:

```text
Recorded
```

ni introduce nuevos estados.

---

# Relación con Commands

El único Command oficial sigue siendo:

```text
RecordAudit
```

`AuditRecordedIntegrationEvent` no es un Command.

---

# Relación con Invariants

Solamente puede existir un Integration Event válido derivado de un
hecho de dominio que ya haya preservado las Invariants.

Debe mantenerse:

```text
Invalid Audit

↓

No Valid AuditRecorded

↓

No Valid AuditRecordedIntegrationEvent
```

---

# Relación con Permissions

Permissions determinan si una intención puede llegar al Aggregate.

El Integration Event representa un hecho posterior.

No contiene lógica para autorizar `RecordAudit`.

---

# Relación con Repository

El Repository confirma el estado de Audit.

La publicación externa ocurre posteriormente.

Debe mantenerse:

```text
Repository Commit

before

Integration Publication
```

---

# Relación con Versioning

Publicar:

```text
AuditRecordedIntegrationEvent
```

no incrementa:

```text
Audit.Version
```

---

# Relación con Consistency Boundary

El Integration Event permite comunicar un hecho sin expandir:

```text
Audit Consistency Boundary
```

hacia sus consumidores.

Debe mantenerse:

```text
Integration Communication

≠

Shared Transaction
```

---

# Relación con Read Model

Un Integration Event puede alimentar Read Models externos.

El Read Model interno de Audit puede utilizar Domain Events.

No existe obligación de utilizar el mismo mecanismo para ambos.

---

# Relación con Test Scenarios

Los escenarios deben validar:

```text
correct integration event type

correct aggregate id

correct aggregate type

correct contract version

correct correlation

correct causation

minimum payload

no publication before commit

no publication when no integration contract exists

duplicate delivery safety

no aggregate mutation during publication

no aggregate version increment during retry
```

La especificación detallada pertenece a:

```text
DOMAIN-012M-Test-Scenarios.md
```

---

# Relación con Security Model

Los Integration Events deben respetar:

```text
DOMAIN-012O-Security-Model.md
```

incluyendo:

- minimización;
- confidencialidad;
- autorización de consumidores;
- protección de información sensible;
- ausencia de credenciales;
- trazabilidad.

---

# Evolución

Un nuevo Integration Event solamente puede añadirse cuando exista:

- un Domain Fact válido;
- una necesidad explícita de integración;
- un contrato público definido;
- semántica propia;
- consumidores identificables conceptualmente;
- reglas de seguridad aplicables.

---

# Regla de Extensión

Debe mantenerse:

```text
New Domain Event

≠

Automatic New Integration Event
```

Cada nuevo contrato debe justificarse por una necesidad real de
interoperabilidad.

---

# Cambio de Contrato

Cualquier cambio contractual debe preservar:

- significado histórico;
- compatibilidad cuando corresponda;
- identidad del evento;
- independencia del Aggregate;
- minimización de datos;
- separación entre Contract Version y Aggregate Version.

---

# Independencia Tecnológica

AuditRecordedIntegrationEvent no depende conceptualmente de:

```text
Kafka

RabbitMQ

NATS

Redis

HTTP

REST

GraphQL

FastAPI

Django

MongoDB

PostgreSQL

FIWARE

NGSI-LD
```

Estos mecanismos pueden transportar, almacenar o transformar
contratos.

No definen su significado.

---

# Reglas Fundamentales

Los Integration Events de Audit deben cumplir:

1. Domain Event e Integration Event son conceptos distintos.
2. Integration Event no forma parte del estado del Aggregate.
3. AuditRecorded es el único Domain Event oficial versión 1.0.
4. AuditRecordedIntegrationEvent es el único Integration Event
   definido para Audit versión 1.0.
5. AuditRecordedIntegrationEvent solamente se utiliza cuando exista
   una necesidad explícita de integración.
6. La existencia de AuditRecorded no obliga a publicación externa.
7. La transformación ocurre fuera del Aggregate.
8. Audit no publica directamente contratos externos.
9. AggregateId corresponde a AuditId.
10. AggregateType corresponde a Audit.
11. EventId es único e inmutable.
12. EventId permanece distinto de AuditId.
13. Integration Contract Version permanece distinta de
    Audit.Version.
14. Integration Contract Version permanece distinta de
    AggregateVersion.
15. CorrelationId se preserva cuando corresponda.
16. CausationId se preserva cuando corresponda.
17. Payload contiene únicamente información necesaria.
18. El Aggregate completo no se copia al Integration Event.
19. El Domain Event completo no se copia automáticamente al contrato
    público.
20. Información ausente no se inventa.
21. SourceAggregateId permanece distinto de AuditId.
22. SourceEventId permanece distinto del EventId del Integration
    Event.
23. SourceAggregateVersion permanece independiente de Audit.Version.
24. ActorId solamente se publica cuando sea necesario y permitido.
25. Datos personales no se publican automáticamente.
26. Audit commit ocurre antes de publicación externa.
27. Un fallo de publicación no modifica Audit.
28. Un fallo del consumidor no revierte Audit.
29. Retries técnicos no modifican Audit.
30. Retries técnicos no incrementan Audit.Version.
31. Outbox permanece fuera del Aggregate.
32. Estados técnicos de Outbox no son AuditStatus.
33. EventId permite procesamiento idempotente.
34. Duplicate Delivery no representa nuevo Domain Fact.
35. No existe orden global obligatorio entre Audits.
36. AggregateVersion puede preservar orden por Aggregate cuando
    corresponda.
37. Integration Contracts poseen versionado independiente.
38. Cambios contractuales no incrementan Audit.Version.
39. Integration Event no constituye Source of Truth de Audit.
40. Integration Event no constituye Read Model.
41. Read Models externos pueden reaccionar mediante consistencia
    eventual.
42. Read Models internos pueden utilizar Domain Events.
43. Event Sourcing utiliza Domain Events como historial interno, no
    Integration Events.
44. Rehidratación no depende obligatoriamente de Integration Events.
45. Integration Event no ejecuta automáticamente RecordAudit.
46. No existe recursividad automática de Audit.
47. Otros Aggregates permanecen fuera del Consistency Boundary.
48. Consumidores externos no modifican Audit directamente.
49. FIWARE permanece fuera del Aggregate.
50. NGSI-LD no define la semántica de Audit.
51. Sistemas municipales utilizan contratos de integración.
52. Anti-Corruption Layer traduce modelos externos cuando
    corresponda.
53. Integration Events no contienen secretos ni credenciales.
54. Transporte no determina semántica.
55. Serialización no determina semántica.
56. Broker no determina semántica.
57. Logs y métricas técnicas no son Integration Events.
58. No existen Integration Events de Archive, Delete, Retry o
    Correction en versión 1.0.
59. Nuevos Integration Events requieren necesidad explícita.
60. Nuevos Domain Events no generan automáticamente nuevos
    Integration Events.

---

# Restricciones

No está permitido:

- tratar AuditRecorded como Integration Event;
- tratar AuditRecordedIntegrationEvent como Domain Event;
- publicar un Integration Event antes del commit de Audit;
- publicar un Integration Event para una operación rechazada;
- asumir que todo Domain Event debe publicarse;
- modificar Audit desde un consumidor externo;
- incrementar Audit.Version durante publicación;
- incrementar Audit.Version durante retry;
- usar Contract Version como Audit.Version;
- utilizar SourceAggregateVersion como Contract Version;
- reutilizar EventId para hechos diferentes;
- inventar ActorId, CorrelationId o CausationId;
- copiar Aggregates completos al Payload;
- copiar Source Event Payload completo automáticamente;
- incluir passwords;
- incluir tokens;
- incluir private keys;
- incluir secretos;
- convertir estados técnicos de Outbox en AuditStatus;
- convertir errores de broker en Domain Events;
- convertir logs técnicos en Integration Events;
- convertir mensajes FIWARE en Domain Events de Audit;
- utilizar el Integration Event como mecanismo de rehidratación
  autoritativo del Aggregate;
- crear recursividad automática desde Audit hacia Audit;
- introducir contratos Archive, Delete, Retry o Correction no
  soportados por el dominio.

---

# Compatibilidad Arquitectónica

El modelo de Integration Events de Audit es compatible con:

- Domain-Driven Design;
- Event-Driven Architecture;
- Aggregate Pattern;
- Clean Architecture;
- Hexagonal Architecture;
- SOLID;
- CQRS;
- Event Sourcing Compatible;
- Transactional Outbox;
- Optimistic Concurrency Control;
- consistencia eventual;
- Anti-Corruption Layer;
- High Cohesion;
- Low Coupling.

Estas compatibilidades no introducen una tecnología de transporte
obligatoria.

---

# Definición de Éxito

Los Integration Events del Aggregate **Audit** permiten comunicar
hechos confirmados hacia otros Bounded Contexts y sistemas externos
sin ampliar su Consistency Boundary.

La versión 1.0 define:

```text
AuditRecorded
```

como Domain Event interno y:

```text
AuditRecordedIntegrationEvent
```

como contrato público posible cuando existe una necesidad explícita
de integración.

El modelo garantiza que:

- Domain Event e Integration Event permanecen separados;
- AuditRecordedIntegrationEvent no forma parte del estado de Audit;
- la transformación ocurre fuera del Aggregate;
- la existencia de AuditRecorded no obliga a publicar;
- AggregateId representa AuditId;
- AggregateType representa Audit;
- EventId mantiene identidad propia;
- Contract Version permanece independiente de Audit.Version;
- AggregateVersion permanece conceptualmente independiente del
  versionado contractual;
- CorrelationId y CausationId preservan trazabilidad cuando
  corresponda;
- Payload contiene solamente información necesaria;
- información faltante no se inventa;
- datos sensibles no se publican automáticamente;
- Audit commit ocurre antes de la publicación externa;
- fallos y retries de publicación no modifican Audit;
- fallos de consumidores no producen rollback;
- idempotencia puede basarse en EventId;
- duplicados no constituyen nuevos hechos;
- Outbox permanece fuera del Aggregate;
- Read Models internos y externos permanecen separados del Write
  Model;
- Event Sourcing utiliza Domain Events y no Integration Events como
  historial autoritativo;
- consumidores externos no poseen autoridad directa sobre Audit;
- Organization, Citizen, Membership, Role, Territory, Assembly,
  Proposal, Participation, Voting, Document, Notification e
  Integration permanecen fuera del Consistency Boundary;
- FIWARE y sistemas municipales permanecen desacoplados mediante
  contratos;
- transporte, serialización y broker no determinan la semántica;
- no existen Integration Events de archivado, eliminación, retry o
  corrección en la versión 1.0;
- cualquier nuevo Integration Event requiere una necesidad explícita
  y una evolución controlada del contrato.

De esta forma, `DOMAIN-012K-Integration-Events.md` establece los
Integration Events oficiales del Aggregate **Audit** conforme al
patrón consolidado de AURA Core.