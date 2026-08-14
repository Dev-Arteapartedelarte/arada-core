# DOMAIN-011D — Notification Domain Events

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
- DOMAIN-011A-Lifecycle.md
- DOMAIN-011B-State-Machine.md
- DOMAIN-011C-Commands.md
- DOMAIN-011E-Invariants.md
- CORE-005-Domain-Events.md

---

# Objetivo

Este documento define los Domain Events oficiales del Aggregate
**Notification**.

Los Domain Events representan hechos significativos que ya
ocurrieron dentro del Aggregate como consecuencia de una operación
válida.

Cada evento expresa un cambio confirmado del dominio y forma parte
de la trazabilidad de Notification.

---

# Propósito

Los Domain Events permiten:

- representar hechos consumados;
- preservar trazabilidad;
- comunicar cambios dentro del dominio;
- desacoplar Aggregates;
- alimentar Read Models;
- soportar Audit;
- permitir Integration Events cuando exista un contrato explícito;
- mantener compatibilidad con CQRS;
- mantener compatibilidad con Event Sourcing.

Los eventos pertenecen exclusivamente al Aggregate:

```text
Notification
```

---

# Principio Fundamental

Un Domain Event representa:

```text
Fact
```

No representa:

```text
Intent
```

Por lo tanto:

```text
QueueNotification
```

es un Command.

Mientras:

```text
NotificationQueued
```

es un Domain Event.

Debe mantenerse:

```text
Command

    │
    ▼

Notification

    │
    ├── valida estado
    ├── valida transición
    ├── valida Invariants
    └── ejecuta comportamiento
            │
            ▼
       Domain Event
```

El Domain Event existe únicamente cuando el hecho ocurrió
realmente.

---

# Commands versus Domain Events

Los Commands oficiales expresan intención:

```text
CreateNotification

QueueNotification

ConfirmNotificationDelivery

ReportNotificationDeliveryFailure

RetryNotification
```

Los Domain Events oficiales expresan hechos consumados:

```text
NotificationCreated

NotificationQueued

NotificationDelivered

NotificationDeliveryFailed

NotificationRetried
```

Nunca debe utilizarse un Domain Event como solicitud de cambio.

Tampoco debe utilizarse un Command como registro histórico de un
hecho ya ocurrido.

---

# Propiedad del Evento

Los Domain Events definidos en este documento pertenecen
conceptualmente al Aggregate:

```text
Notification
```

Notification es responsable de producirlos cuando sus operaciones
modifican válidamente el estado del dominio.

Otros Aggregates o Bounded Contexts pueden reaccionar
posteriormente a estos hechos, pero no son propietarios del evento
original.

---

# Alcance

Los eventos de Notification describen exclusivamente hechos
pertenecientes al Aggregate Notification.

No representan directamente hechos internos de:

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

Audit

Integration
```

Cuando un hecho pertenece a otro Aggregate debe ser producido por
el Aggregate responsable.

---

# Eventos Oficiales

La versión 1.0 define los siguientes Domain Events:

```text
NotificationCreated

NotificationQueued

NotificationDelivered

NotificationDeliveryFailed

NotificationRetried
```

No existen otros Domain Events oficiales para Notification en la
versión 1.0.

Nuevos eventos requieren evolución explícita del dominio.

---

# NotificationCreated

## Significado

Representa el hecho de que una nueva Notification fue creada
válidamente.

## Command causante

```text
CreateNotification
```

## Transición

```text
No Notification

↓

Draft
```

## Payload conceptual mínimo

```text
NotificationId

NotificationStatus

CreatedAt
```

donde:

```text
NotificationStatus = Draft
```

## Reglas

`NotificationCreated`:

- representa la existencia formal de una nueva Notification;
- no representa entrega;
- no representa procesamiento técnico;
- no representa modificación de otro Aggregate;
- solamente existe después de una creación válida.

---

# NotificationQueued

## Significado

Representa el hecho de que una Notification Draft fue incorporada
válidamente al proceso de entrega.

## Command causante

```text
QueueNotification
```

## Transición

```text
Draft

↓

Pending
```

## Payload conceptual mínimo

```text
NotificationId

PreviousStatus

NotificationStatus
```

donde:

```text
PreviousStatus = Draft

NotificationStatus = Pending
```

## Reglas

`NotificationQueued`:

- representa un cambio confirmado del Lifecycle;
- no representa entrega exitosa;
- no representa fallo;
- no representa una llamada técnica a un proveedor;
- no implica que otro Aggregate haya sido modificado.

Debe mantenerse:

```text
NotificationQueued

≠

NotificationDelivered
```

---

# NotificationDelivered

## Significado

Representa el hecho de que la entrega de una Notification Pending
fue confirmada exitosamente dentro del dominio.

## Command causante

```text
ConfirmNotificationDelivery
```

## Transición

```text
Pending

↓

Delivered
```

## Payload conceptual mínimo

```text
NotificationId

PreviousStatus

NotificationStatus
```

donde:

```text
PreviousStatus = Pending

NotificationStatus = Delivered
```

## Reglas

`NotificationDelivered`:

- representa una entrega confirmada;
- no representa lectura;
- no representa aceptación del contenido;
- no representa una acción posterior del destinatario;
- no modifica directamente el Aggregate que originó la
  Notification.

Debe mantenerse:

```text
NotificationDelivered

≠

NotificationRead
```

y:

```text
NotificationDelivered

≠

External Aggregate Modification
```

Delivered constituye el estado terminal exitoso del Lifecycle
versión 1.0.

---

# NotificationDeliveryFailed

## Significado

Representa el hecho de que un intento de entrega de una
Notification Pending no pudo completarse satisfactoriamente.

## Command causante

```text
ReportNotificationDeliveryFailure
```

## Transición

```text
Pending

↓

Failed
```

## Payload conceptual mínimo

```text
NotificationId

PreviousStatus

NotificationStatus
```

donde:

```text
PreviousStatus = Pending

NotificationStatus = Failed
```

## Reglas

`NotificationDeliveryFailed`:

- representa un hecho confirmado de Notification;
- conserva NotificationId;
- no elimina la Notification;
- no revierte el hecho que originó la necesidad de comunicación;
- no modifica directamente otro Aggregate;
- permanece como hecho histórico incluso si posteriormente existe
  un reintento.

Debe mantenerse:

```text
NotificationDeliveryFailed

≠

Source Aggregate Failure
```

y:

```text
Failed

≠

Deleted
```

---

# NotificationRetried

## Significado

Representa el hecho de que una Notification Failed fue reingresada
válidamente al proceso de entrega.

## Command causante

```text
RetryNotification
```

## Transición

```text
Failed

↓

Pending
```

## Payload conceptual mínimo

```text
NotificationId

PreviousStatus

NotificationStatus
```

donde:

```text
PreviousStatus = Failed

NotificationStatus = Pending
```

## Reglas

`NotificationRetried`:

- no crea una nueva Notification;
- conserva NotificationId;
- conserva el historial previo;
- no elimina NotificationDeliveryFailed;
- no representa entrega exitosa;
- no produce directamente Delivered.

Debe mantenerse:

```text
NotificationRetried

≠

NotificationCreated
```

y:

```text
NotificationRetried

≠

NotificationDelivered
```

---

# Contrato Conceptual del Evento

Todo Domain Event de Notification debe poder representarse mediante
un envelope conceptual que incluya:

```text
EventId

EventType

NotificationId

AggregateVersion

OccurredAt

CorrelationId

CausationId

Payload
```

El envelope representa metadatos del hecho.

Payload representa únicamente la información necesaria para
expresar el significado específico del evento.

---

# EventId

Cada Domain Event posee:

```text
EventId
```

EventId identifica de forma única el hecho registrado.

Debe mantenerse:

```text
EventId

≠

NotificationId
```

Una misma Notification puede producir múltiples Domain Events
durante su Lifecycle.

---

# EventType

EventType identifica el tipo de hecho ocurrido.

En la versión 1.0 sus valores corresponden exclusivamente a:

```text
NotificationCreated

NotificationQueued

NotificationDelivered

NotificationDeliveryFailed

NotificationRetried
```

---

# NotificationId

Todo Domain Event pertenece a una Notification específica.

Por lo tanto debe mantener:

```text
NotificationId
```

NotificationId permite relacionar el hecho con la evolución del
mismo Aggregate.

---

# AggregateVersion

Todo evento debe relacionarse con una versión concreta de
Notification.

Conceptualmente:

```text
Notification vN

↓

Valid Modification

↓

Notification vN+1

+

Domain Event
AggregateVersion = N+1
```

AggregateVersion representa el orden lógico de evolución del
Aggregate.

---

# OccurredAt

Todo evento debe registrar:

```text
OccurredAt
```

OccurredAt representa el momento en que ocurrió el hecho de
dominio.

No debe utilizarse para reemplazar AggregateVersion como mecanismo
de orden lógico del Aggregate.

---

# CorrelationId

CorrelationId permite relacionar hechos que pertenecen a una misma
interacción o proceso distribuido cuando corresponda.

Su presencia no modifica el Consistency Boundary.

CorrelationId no representa identidad del Aggregate.

---

# CausationId

CausationId permite identificar la causa inmediata del evento
cuando el flujo de procesamiento requiera dicha trazabilidad.

Conceptualmente:

```text
Command / Prior Message

↓

CausationId

↓

Domain Event
```

CausationId no reemplaza NotificationId ni EventId.

---

# Payload

El Payload contiene únicamente la información necesaria para
expresar el hecho ocurrido.

No debe utilizarse como snapshot completo del Aggregate.

No debe incluir automáticamente:

- Aggregates externos completos;
- credenciales;
- secretos;
- tokens;
- información técnica de proveedores;
- estructuras internas de Infrastructure.

Debe mantenerse:

```text
Event Payload

≠

Aggregate Snapshot
```

---

# Eventos y Version

Todo Domain Event corresponde a una modificación válida.

Por lo tanto:

```text
Valid Modification

↓

Version + 1

↓

Domain Event
```

Para un mismo NotificationId, AggregateVersion establece la
secuencia lógica de hechos.

Una operación rechazada no puede producir un nuevo Domain Event de
éxito con una versión inexistente.

---

# Orden de Eventos

La evolución de una Notification debe preservar el orden lógico de
sus Domain Events.

Ejemplo:

```text
Version 1
NotificationCreated

Version 2
NotificationQueued

Version 3
NotificationDelivered
```

En un flujo con fallo y reintento:

```text
Version 1
NotificationCreated

Version 2
NotificationQueued

Version 3
NotificationDeliveryFailed

Version 4
NotificationRetried

Version 5
NotificationDelivered
```

El timestamp aporta contexto temporal.

AggregateVersion preserva el orden lógico.

---

# Eventos y State Machine

Cada evento de Lifecycle debe corresponder a una transición válida.

La correspondencia oficial es:

```text
No Notification → Draft
    NotificationCreated

Draft → Pending
    NotificationQueued

Pending → Delivered
    NotificationDelivered

Pending → Failed
    NotificationDeliveryFailed

Failed → Pending
    NotificationRetried
```

No puede existir un evento que implique una transición no permitida
por la State Machine.

---

# No Event on Failure

Una operación rechazada nunca produce un Domain Event de éxito.

Ejemplo:

```text
NotificationStatus = Draft

ConfirmNotificationDelivery
```

debe resultar en:

```text
Rejected
```

y no puede producir:

```text
NotificationDelivered
```

---

# Evento después de Confirmación

Un Domain Event representa un hecho confirmado dentro del
Aggregate.

No debe producirse como anticipación de un resultado futuro.

Debe mantenerse:

```text
Intent

↓

Validation

↓

State Change

↓

Domain Event
```

Nunca:

```text
Intent

↓

Domain Event

↓

Try State Change
```

---

# Inmutabilidad

Los Domain Events representan hechos históricos.

Una vez ocurrido un evento:

- no se modifica;
- no se elimina para representar un estado posterior;
- no se reinterpreta retroactivamente;
- no se reemplaza por otro evento.

Por ejemplo:

```text
NotificationDeliveryFailed
```

permanece como hecho histórico aunque posteriormente ocurra:

```text
NotificationRetried
```

y luego:

```text
NotificationDelivered
```

---

# Eventos y Retry

Cada reintento añade un nuevo hecho a la historia de la misma
Notification.

Conceptualmente:

```text
NotificationDeliveryFailed

↓

NotificationRetried

↓

NotificationDeliveryFailed
```

puede repetirse cuando el Lifecycle y las Invariants lo permitan.

El nuevo intento no elimina ni reemplaza intentos anteriores.

---

# Eventos y Aggregate de Origen

Los eventos de Notification no representan hechos del Aggregate que
originó la necesidad de comunicación.

Por ejemplo:

```text
AssemblyConvoked
```

pertenece a Assembly.

Mientras:

```text
NotificationQueued
```

pertenece a Notification.

Debe mantenerse:

```text
Source Aggregate Event

≠

Notification Event
```

Ambos hechos pueden estar correlacionados sin pertenecer al mismo
Consistency Boundary.

---

# Eventos y Consistency Boundary

El Domain Event se produce como consecuencia de una modificación
dentro del límite:

```text
Notification
```

No implica modificación atómica de:

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

Audit

Integration
```

Cada Aggregate conserva su propio Consistency Boundary.

---

# Eventos e Integration Boundary

Los sistemas externos no deben consumir necesariamente los Domain
Events internos directamente.

Cuando exista una necesidad de comunicación inter-contextual o
externa debe utilizarse un contrato de:

```text
Integration Event
```

cuando corresponda.

Debe mantenerse:

```text
Domain Event

≠

Integration Event
```

y:

```text
Domain Event

≠

Mandatory Integration Event
```

La existencia de un Domain Event no crea automáticamente un
Integration Event.

---

# Eventos y Read Models

Los Domain Events pueden alimentar proyecciones de lectura.

Conceptualmente:

```text
Notification Domain Event

        │
        ▼

   Projection

        │
        ▼

   Read Model
```

Los Read Models:

- no modifican Notification;
- no producen transiciones;
- no sustituyen el historial;
- pueden reconstruirse a partir de hechos disponibles.

---

# Eventos y Audit

Los Domain Events pueden aportar hechos relevantes al contexto de
Audit.

Audit permanece fuera del Aggregate Notification.

Debe mantenerse:

```text
Domain Event

≠

Audit Record
```

Notification no mantiene registros de Audit como estado interno.

---

# Persistencia de Domain Events

Cuando la arquitectura adopte persistencia de Domain Events, debe
preservarse conceptualmente:

```text
EventId

EventType

NotificationId

AggregateVersion

OccurredAt

CorrelationId

CausationId

Payload
```

La representación física pertenece a Infrastructure.

El dominio no depende de:

- Event Store específico;
- base de datos específica;
- formato de serialización;
- broker de mensajería;
- protocolo de transporte.

---

# Event Store

La existencia de un Event Store no constituye una obligación del
Aggregate.

Notification es compatible con:

```text
State Persistence + Domain Events
```

y con:

```text
Event Sourcing
```

La estrategia concreta pertenece a la arquitectura de
persistencia.

---

# Repository y Domain Events

El Repository persiste Notification como unidad.

La estrategia de persistencia debe coordinar:

```text
Notification State

Version

Domain Events
```

sin permitir que el Repository invente hechos de dominio.

El Repository:

- no crea Domain Events;
- no decide transiciones;
- no ejecuta Commands;
- no reemplaza la Aggregate Root.

---

# Eventos y Optimistic Concurrency

Los Domain Events solamente pueden corresponder a una modificación
aceptada dentro de una secuencia válida de Version.

Si existe:

```text
PersistedVersion

≠

ExpectedVersion
```

la modificación debe ser rechazada conforme al Repository
Contract.

No puede generarse un nuevo evento de éxito correspondiente a una
modificación concurrente no confirmada.

---

# Seguridad

Los Domain Events no deben contener:

- contraseñas;
- tokens;
- claves privadas;
- credenciales;
- secretos;
- sesiones;
- información técnica innecesaria de proveedores.

El Payload debe respetar minimización de información.

La existencia de información dentro de Notification no implica su
exposición automática mediante eventos.

---

# Compatibilidad con CQRS

Los Domain Events permiten desacoplar el Write Side del Read Side.

Conceptualmente:

```text
Command

↓

Notification

↓

Domain Event

↓

Projection

↓

Read Model
```

El Read Side no modifica el Aggregate.

---

# Compatibilidad con Event Sourcing

La evolución de Notification puede reconstruirse a partir de sus
Domain Events oficiales.

Flujo exitoso:

```text
NotificationCreated

↓

NotificationQueued

↓

NotificationDelivered
```

Flujo con fallo y reintento:

```text
NotificationCreated

↓

NotificationQueued

↓

NotificationDeliveryFailed

↓

NotificationRetried

↓

NotificationDelivered
```

Los eventos históricos permanecen inmutables.

La reconstrucción aplica únicamente hechos pertenecientes al mismo:

```text
NotificationId
```

---

# Reglas Generales

Todo Domain Event de Notification debe cumplir:

1. Representa un hecho ya ocurrido.
2. Pertenece al Aggregate Notification.
3. Posee EventId.
4. Mantiene NotificationId.
5. Mantiene AggregateVersion coherente.
6. Mantiene OccurredAt.
7. Puede mantener CorrelationId y CausationId conforme al contrato.
8. Posee Payload mínimo necesario.
9. Es inmutable.
10. No representa una intención.
11. No modifica directamente otros Aggregates.
12. No reemplaza un Integration Event.
13. No reemplaza un Audit Record.
14. No puede existir como evento de éxito después de una operación
    rechazada.
15. Debe corresponder a una transición o modificación válida.
16. No contiene secretos ni credenciales.
17. Preserva el orden lógico mediante AggregateVersion.
18. No reescribe hechos históricos anteriores.

---

# Definición de Éxito

Los Domain Events del Aggregate **Notification** representan de
forma oficial los hechos relevantes que ocurren durante la
evolución de una unidad de comunicación dentro del ecosistema
AURA.

La versión 1.0 define:

```text
NotificationCreated

NotificationQueued

NotificationDelivered

NotificationDeliveryFailed

NotificationRetried
```

correspondientes a:

```text
No Notification → Draft

Draft → Pending

Pending → Delivered

Pending → Failed

Failed → Pending
```

El modelo garantiza que:

- cada evento representa un hecho consumado;
- cada evento pertenece a Notification;
- EventId identifica el hecho;
- NotificationId identifica el Aggregate;
- AggregateVersion preserva el orden lógico;
- OccurredAt preserva contexto temporal;
- CorrelationId y CausationId permiten trazabilidad cuando
  corresponda;
- el Payload contiene únicamente información necesaria;
- una operación rechazada no genera eventos de éxito;
- NotificationDelivered no representa lectura;
- NotificationDeliveryFailed no revierte el Aggregate originador;
- NotificationRetried no elimina fallos anteriores;
- los hechos históricos permanecen inmutables;
- otros Aggregates permanecen fuera del Consistency Boundary;
- Domain Events e Integration Events permanecen separados;
- Audit permanece separado;
- Read Models pueden proyectarse sin adquirir autoridad de
  escritura;
- CQRS y Event Sourcing permanecen compatibles;
- Infrastructure no determina la semántica de los eventos.

De esta forma, `DOMAIN-011D-Domain-Events.md` establece los Domain
Events oficiales del Aggregate **Notification** conforme al
Lifecycle y al patrón consolidado de AURA Core.