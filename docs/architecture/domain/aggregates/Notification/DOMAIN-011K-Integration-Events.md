# DOMAIN-011K — Notification Integration Events

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Notification Management

Aggregate:
Notification

Documentos relacionados:

- DOMAIN-011-Aggregate.md
- DOMAIN-011D-Domain-Events.md
- DOMAIN-011I-Versioning.md
- DOMAIN-011J-Consistency-Boundary.md
- CORE-005-Domain-Events.md

---

# Objetivo

Este documento define los **Integration Events** publicados por
el Aggregate **Notification** para permitir la comunicación con
otros Bounded Contexts y sistemas externos.

A diferencia de los Domain Events, los Integration Events
constituyen contratos públicos y estables orientados a la
integración.

Su publicación ocurre únicamente después de que la transacción
del Aggregate haya sido confirmada exitosamente.

---

# Principios

Los Integration Events cumplen los siguientes principios:

- representan hechos ya confirmados;
- son inmutables;
- poseen contratos públicos versionados;
- son independientes del dominio interno;
- son consumidos por otros Bounded Contexts;
- pueden ser enviados a sistemas externos;
- no modifican directamente el Aggregate;
- no sustituyen los Domain Events.

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

# Flujo General

```text
Notification Aggregate

        │

        ▼

Domain Event

        │

        ▼

Outbox Pattern

        │

        ▼

Integration Event

        │

        ▼

Message Broker

        │

        ├──────── Organization
        ├──────── Citizen
        ├──────── Membership
        ├──────── Assembly
        ├──────── Proposal
        ├──────── Participation
        ├──────── Voting
        ├──────── Document
        ├──────── Audit
        ├──────── Analytics
        └──────── Sistemas Externos
```

---

# Relación Domain Event → Integration Event

La existencia de un Domain Event no implica automáticamente la
existencia de un Integration Event.

Un Integration Event solamente debe publicarse cuando exista un
contrato explícito de integración y un consumidor necesite conocer
el hecho correspondiente.

Cuando dicho contrato exista, la relación conceptual puede ser:

```text
NotificationCreated
        │
        ▼
NotificationCreatedIntegrationEvent
```

```text
NotificationQueued
        │
        ▼
NotificationQueuedIntegrationEvent
```

```text
NotificationDelivered
        │
        ▼
NotificationDeliveredIntegrationEvent
```

```text
NotificationDeliveryFailed
        │
        ▼
NotificationDeliveryFailedIntegrationEvent
```

```text
NotificationRetried
        │
        ▼
NotificationRetriedIntegrationEvent
```

La transformación entre ambos contratos ocurre fuera del
Aggregate.

---

# Eventos Oficiales

El Aggregate Notification puede publicar los siguientes contratos
de integración cuando exista una necesidad explícita de
comunicación fuera de su Consistency Boundary:

```text
NotificationCreatedIntegrationEvent

NotificationQueuedIntegrationEvent

NotificationDeliveredIntegrationEvent

NotificationDeliveryFailedIntegrationEvent

NotificationRetriedIntegrationEvent
```

Estos contratos representan hechos públicos de integración
derivados de hechos ya confirmados por Notification.

Su existencia no altera el Lifecycle ni la State Machine del
Aggregate.

---

# NotificationCreatedIntegrationEvent

Representa públicamente que una nueva Notification fue creada
válidamente.

Se deriva conceptualmente de:

```text
NotificationCreated
```

Puede ser utilizado por consumidores que necesiten conocer la
existencia de una nueva unidad de Notification.

No representa:

```text
Notification Delivered
```

ni:

```text
Notification Queued
```

---

# NotificationQueuedIntegrationEvent

Representa públicamente que una Notification fue incorporada
válidamente al proceso de entrega.

Se deriva conceptualmente de:

```text
NotificationQueued
```

El hecho comunicado corresponde al estado:

```text
Pending
```

No representa una entrega confirmada.

Debe mantenerse:

```text
NotificationQueuedIntegrationEvent

≠

NotificationDeliveredIntegrationEvent
```

---

# NotificationDeliveredIntegrationEvent

Representa públicamente que la entrega de una Notification fue
confirmada válidamente por el dominio.

Se deriva conceptualmente de:

```text
NotificationDelivered
```

El estado correspondiente es:

```text
Delivered
```

Este Integration Event no significa:

```text
Read

Opened

Acknowledged
```

Debe mantenerse:

```text
Delivered

≠

Read
```

---

# NotificationDeliveryFailedIntegrationEvent

Representa públicamente que un intento de entrega de una
Notification terminó en fallo.

Se deriva conceptualmente de:

```text
NotificationDeliveryFailed
```

El estado correspondiente es:

```text
Failed
```

Este evento:

- no elimina la Notification;
- no revierte el hecho que originó la Notification;
- no modifica directamente otro Aggregate;
- conserva la identidad de la Notification.

Debe mantenerse:

```text
NotificationDeliveryFailedIntegrationEvent

≠

Source Aggregate Failure
```

---

# NotificationRetriedIntegrationEvent

Representa públicamente que una Notification previamente Failed
fue reingresada válidamente al proceso de entrega.

Se deriva conceptualmente de:

```text
NotificationRetried
```

La transición correspondiente es:

```text
Failed → Pending
```

Este evento no representa una nueva Notification.

Debe mantenerse:

```text
NotificationRetriedIntegrationEvent

≠

NotificationCreatedIntegrationEvent
```

---

# Contrato Conceptual

Todo Integration Event contiene conceptualmente:

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

Para Notification:

```text
AggregateId = NotificationId

AggregateType = Notification
```

El formato físico:

```text
JSON

Avro

Protobuf
```

o equivalente pertenece a Infrastructure.

---

# EventId

Cada Integration Event posee:

```text
EventId
```

como identidad única del mensaje de integración.

Debe mantenerse:

```text
EventId

≠

NotificationId
```

Un mismo NotificationId puede originar múltiples Integration
Events durante su evolución.

---

# EventType

EventType identifica el contrato público del hecho comunicado.

Ejemplos:

```text
NotificationCreatedIntegrationEvent

NotificationQueuedIntegrationEvent

NotificationDeliveredIntegrationEvent

NotificationDeliveryFailedIntegrationEvent

NotificationRetriedIntegrationEvent
```

---

# AggregateId

Todo Integration Event de Notification referencia:

```text
NotificationId
```

mediante:

```text
AggregateId
```

Este identificador permite relacionar el mensaje con el Aggregate
originador sin transportar el Aggregate completo.

---

# AggregateType

Para los Integration Events definidos en este documento:

```text
AggregateType = Notification
```

AggregateType identifica conceptualmente el tipo de Aggregate que
originó el hecho.

---

# OccurredOn

Todo Integration Event debe conservar información temporal del hecho
comunicado mediante:

```text
OccurredOn
```

Este valor representa el momento asociado al hecho confirmado.

No reemplaza la Version como referencia lógica de evolución.

---

# Version

Todo contrato posee:

```text
Version
```

Ejemplo:

```text
NotificationDeliveredIntegrationEvent

Version 1
```

Version del contrato de integración y Version del Aggregate son
conceptos independientes.

Debe mantenerse:

```text
Integration Contract Version

≠

Notification.Version
```

---

# CorrelationId

CorrelationId permite mantener trazabilidad a través de procesos
distribuidos.

Puede relacionar:

```text
Source Domain Fact

↓

Notification

↓

Notification Integration Event
```

sin fusionar sus respectivos Consistency Boundaries.

---

# CausationId

CausationId permite mantener la relación causal con el mensaje o
hecho que produjo el Integration Event cuando corresponda.

No reemplaza:

```text
EventId

NotificationId

CorrelationId
```

---

# Payload

El Payload debe contener únicamente la información necesaria para
que otros contextos puedan reaccionar al hecho.

Debe evitar:

- lógica de negocio;
- Aggregates completos;
- referencias circulares;
- información redundante;
- credenciales;
- secretos;
- detalles internos de Infrastructure.

Ejemplo conceptual:

```text
NotificationDeliveredIntegrationEvent

NotificationId

OccurredOn

Version
```

El Payload no constituye un snapshot completo de Notification.

Debe mantenerse:

```text
Integration Event Payload

≠

Aggregate Snapshot
```

---

# Consumidores

Los Integration Events de Notification pueden ser consumidos por
otros Bounded Contexts o sistemas externos cuando exista una
necesidad explícita de integración.

---

# Organization Context

Puede reaccionar a hechos de Notification cuando una política
organizacional requiera conocer el estado de una comunicación.

Organization no modifica Notification directamente.

---

# Citizen Context

Puede consumir información de integración cuando exista una
necesidad explícita relacionada con comunicaciones destinadas a un
Citizen.

Citizen permanece fuera del Consistency Boundary de Notification.

---

# Membership Context

Puede reaccionar a hechos de Notification cuando las reglas de
integración requieran relacionar comunicaciones con Memberships.

Notification no modifica Membership directamente.

---

# Assembly Context

Assembly puede haber producido el hecho que originó una necesidad
de comunicación.

Posteriormente puede existir interés de integración respecto al
resultado de Notification.

Debe mantenerse:

```text
Assembly Domain Fact

≠

Notification Integration Event
```

Ambos hechos pertenecen a contextos independientes.

---

# Proposal Context

Proposal puede consumir hechos públicos de Notification cuando
exista un contrato explícito.

Notification no modifica directamente Proposal.

---

# Participation Context

Participation puede reaccionar a hechos públicos de Notification
cuando la comunicación forme parte de un proceso de participación.

La reacción ocurre fuera del Consistency Boundary de Notification.

---

# Voting Context

Voting puede consumir eventos de integración de Notification cuando
una regla explícita de integración lo requiera.

Notification no:

- abre Voting;
- cierra Voting;
- registra votos;
- modifica resultados.

---

# Document Context

Document puede relacionarse con una Notification mediante contratos
explícitos.

Un Integration Event de Notification no modifica:

```text
DocumentStatus

Document.Version

Document Lifecycle
```

---

# Audit Context

Audit puede consumir hechos públicos para construir trazabilidad
cuando corresponda.

Sin embargo:

```text
Integration Event

≠

Audit Record
```

Audit conserva su propio modelo.

---

# Analytics Context

Los Integration Events pueden alimentar:

- indicadores;
- métricas;
- estadísticas;
- tableros;
- modelos analíticos.

Analytics no modifica Notification mediante dichas proyecciones.

---

# Sistemas Externos

Los Integration Events pueden utilizarse para interoperar con:

- FIWARE;
- plataformas municipales;
- sistemas de participación;
- sistemas comunitarios;
- motores de integración;
- plataformas analíticas;
- otros sistemas externos autorizados.

La existencia de estos consumidores no introduce dependencias
tecnológicas dentro del Aggregate.

---

# Publicación

Los Integration Events se publican únicamente después del commit
exitoso del Aggregate.

```text
Command

↓

Notification

↓

Repository

↓

Commit

↓

Outbox

↓

Integration Event

↓

Broker

↓

Consumers
```

Nunca antes.

Debe mantenerse:

```text
Integration Event Publication

after

Confirmed Aggregate Commit
```

---

# Outbox Pattern

El Outbox Pattern permite coordinar la persistencia confirmada del
Aggregate con la publicación posterior de mensajes de integración.

Conceptualmente:

```text
Notification Modification

+

Pending Integration Message

↓

Atomic Persistence

↓

Later Publication
```

El procesamiento técnico del Outbox:

- no modifica NotificationStatus;
- no incrementa Notification.Version;
- no genera nuevos Domain Events;
- no constituye una nueva transición del Lifecycle.

---

# Garantías

El modelo garantiza:

- publicación posterior al commit;
- consistencia transaccional del origen;
- entrega eventual;
- independencia entre productores y consumidores;
- reintentos seguros;
- idempotencia;
- contratos públicos versionados;
- trazabilidad.

La entrega de un Integration Event a un consumidor no forma parte
del Consistency Boundary de Notification.

---

# Idempotencia

Todo consumidor debe asumir que un mismo Integration Event puede
recibirse más de una vez.

La identidad del evento está determinada por:

```text
EventId
```

Los consumidores deben poder reconocer duplicados.

Una entrega duplicada del Integration Event no implica una nueva
modificación de Notification.

---

# Reintentos de Publicación

Un Integration Event puede requerir múltiples intentos técnicos de
publicación.

Debe mantenerse:

```text
Integration Event Publication Retry

≠

RetryNotification
```

`RetryNotification` pertenece al Lifecycle del Aggregate.

Un reintento de publicación pertenece a Infrastructure.

Los reintentos técnicos no incrementan:

```text
Notification.Version
```

---

# Versionado

Cada contrato de integración posee una Version propia.

Ejemplo:

```text
NotificationDeliveredIntegrationEvent

Version 1
```

Los cambios compatibles pueden evolucionar preservando el contrato.

Los cambios incompatibles requieren una nueva versión del contrato.

El versionado del Integration Event no modifica:

```text
Notification.Version
```

---

# Compatibilidad

La evolución de Integration Events debe preservar:

- estabilidad semántica;
- trazabilidad histórica;
- compatibilidad hacia atrás cuando sea posible;
- independencia entre productor y consumidor;
- estabilidad de identificadores;
- significado del hecho comunicado.

Los consumidores no deben depender de detalles internos del
Aggregate.

---

# Relación con Domain Events

Los Domain Events oficiales de Notification son:

```text
NotificationCreated

NotificationQueued

NotificationDelivered

NotificationDeliveryFailed

NotificationRetried
```

Permanecen como hechos internos del dominio.

Los Integration Events constituyen contratos públicos derivados
cuando exista una necesidad de integración.

Debe mantenerse:

```text
Domain Event

=

Internal Domain Fact
```

mientras:

```text
Integration Event

=

Public Integration Contract
```

---

# No Correspondencia Automática

No existe una obligación de publicar un Integration Event por cada
Domain Event.

Debe mantenerse:

```text
Domain Event

≠

Mandatory Integration Event
```

La publicación depende de la existencia de un contrato de
integración explícito y de una necesidad de comunicación fuera del
Bounded Context.

---

# Relación con Event Sourcing

Los Integration Events no forman parte del historial autoritativo
del Aggregate.

El historial de Notification continúa representándose mediante:

```text
Domain Events
```

asociados al mismo:

```text
NotificationId
```

Por lo tanto:

```text
Integration Event

≠

Event Sourcing Aggregate History
```

---

# Relación con CQRS

Los Integration Events pueden alimentar:

- Read Models distribuidos;
- Data Warehouse;
- motores de búsqueda;
- sistemas analíticos;
- proyecciones externas;
- sistemas municipales.

Estas proyecciones permanecen fuera del Write Model de
Notification.

---

# Seguridad

Los Integration Events nunca deben exponer:

- credenciales;
- secretos;
- tokens;
- claves privadas;
- sesiones;
- información sensible innecesaria;
- datos personales no autorizados.

Deben aplicarse:

- minimización;
- autorización;
- anonimización cuando corresponda;
- protección de información conforme a las políticas aplicables.

La existencia de información dentro del Aggregate no implica su
publicación automática.

---

# Consistency Boundary

Los Integration Events existen fuera del Consistency Boundary de
Notification.

Conceptualmente:

```text
Notification

│
│ Immediate Consistency
▼

Commit

│
▼

Integration Event

│
│ Eventual Consistency
▼

External Consumer
```

El éxito o fallo posterior de un consumidor no modifica
retroactivamente el estado confirmado de Notification.

---

# Principios Arquitectónicos

Los Integration Events siguen:

- Domain-Driven Design (DDD);
- Event-Driven Architecture;
- Outbox Pattern;
- CQRS;
- Event Sourcing Compatible;
- Clean Architecture;
- Open/Closed Principle;
- High Cohesion;
- Low Coupling.

La compatibilidad con estas arquitecturas no introduce dependencias
tecnológicas dentro del Aggregate.

---

# Definición de Éxito

Los **Integration Events** del Aggregate **Notification**
constituyen la interfaz pública de comunicación entre Notification
Management y el resto del ecosistema AURA cuando existe una
necesidad explícita de integración.

La versión 1.0 define los contratos:

```text
NotificationCreatedIntegrationEvent

NotificationQueuedIntegrationEvent

NotificationDeliveredIntegrationEvent

NotificationDeliveryFailedIntegrationEvent

NotificationRetriedIntegrationEvent
```

derivados, cuando corresponda, de los Domain Events:

```text
NotificationCreated

NotificationQueued

NotificationDelivered

NotificationDeliveryFailed

NotificationRetried
```

El modelo garantiza que:

- los Integration Events representan hechos ya confirmados;
- su publicación ocurre después del commit;
- Domain Events e Integration Events permanecen separados;
- no existe obligación de correspondencia uno a uno;
- los contratos públicos son versionados;
- EventId permite idempotencia;
- el Payload contiene únicamente información necesaria;
- NotificationId identifica el Aggregate originador;
- CorrelationId y CausationId permiten trazabilidad cuando
  corresponda;
- los consumidores permanecen desacoplados;
- el Outbox no modifica el Lifecycle;
- los reintentos técnicos de publicación no equivalen a
  RetryNotification;
- la publicación no incrementa Notification.Version;
- otros Aggregates mantienen sus propios Consistency Boundaries;
- los Integration Events no forman parte del historial autoritativo
  del Aggregate;
- CQRS puede utilizarlos para proyecciones distribuidas;
- Event Sourcing continúa basado en Domain Events;
- FIWARE, plataformas municipales y otros sistemas externos pueden
  integrarse sin introducir dependencias dentro de Notification;
- la información sensible no se publica automáticamente.

De esta forma, `DOMAIN-011K-Integration-Events.md` establece los
contratos oficiales de integración del Aggregate **Notification**
conforme al patrón consolidado de AURA Core.