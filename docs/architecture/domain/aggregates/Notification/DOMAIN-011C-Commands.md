# DOMAIN-011C — Notification Commands

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
- DOMAIN-011D-Domain-Events.md
- DOMAIN-011E-Invariants.md
- CORE-005-Domain-Events.md

---

# Objetivo

Este documento define los Commands oficiales que pueden
modificar el estado del Aggregate Notification.

Los Commands representan solicitudes explícitas de cambio
de estado. No contienen lógica de negocio ni describen el
resultado esperado; únicamente expresan una intención.

Toda modificación del Aggregate debe originarse mediante un
Command válido.

---

# Principios

Los Commands cumplen los siguientes principios:

- representan intención;
- son inmutables;
- poseen un único propósito;
- son validados antes de ejecutarse;
- pueden rechazarse;
- nunca representan consultas.

Un Command autorizado no garantiza que la operación pueda
ejecutarse.

Notification continúa siendo responsable de validar:

- estado actual;
- State Machine;
- Invariants;
- Version;
- consistencia del Aggregate.

---

# Flujo General

```text
Actor / Process

      │

      ▼

Application Service

      │

      ▼

Command

      │

      ▼

Notification Aggregate

      │

      ▼

Domain Validation

      │

      ▼

Domain Events
```

---

# Commands Oficiales

El Aggregate Notification reconoce los siguientes Commands.

```text
CreateNotification

QueueNotification

ConfirmNotificationDelivery

ReportNotificationDeliveryFailure

RetryNotification
```

Estos Commands corresponden exclusivamente al Lifecycle
oficial definido para Notification versión 1.0.

No deben inferirse Commands adicionales desde:

- canales;
- proveedores;
- APIs;
- mecanismos técnicos de entrega;
- Read Models;
- Integration Events.

---

# CreateNotification

## Propósito

Crear una nueva unidad formal de Notification dentro del
Bounded Context Notification Management.

## Estado requerido

No existe Aggregate previo para el NotificationId.

## Estado resultante

```text
Draft
```

## Datos conceptuales mínimos

El Command debe proporcionar la información necesaria para
establecer válidamente la nueva Notification conforme a las
Invariants del Aggregate.

Debe existir:

```text
NotificationId
```

Los demás datos requeridos deberán corresponder únicamente a
conceptos oficialmente definidos por Notification.

El Command no contiene Aggregates externos completos.

## Eventos esperados

```text
NotificationCreated
```

## Reglas

`CreateNotification`:

- crea una nueva identidad Notification;
- establece Draft como estado inicial;
- no permite seleccionar arbitrariamente otro estado inicial;
- no ejecuta técnicamente la entrega;
- no modifica el Aggregate que originó la necesidad de
  comunicación;
- debe dejar el nuevo Aggregate en estado válido.

---

# QueueNotification

## Propósito

Incorporar una Notification Draft al proceso de entrega.

## Estado requerido

```text
Draft
```

## Estado resultante

```text
Pending
```

## Eventos

```text
NotificationQueued
```

## Reglas

`QueueNotification` representa la intención de dejar la
Notification preparada para que su entrega pueda ser procesada.

No significa:

```text
Delivered
```

ni:

```text
Failed
```

Tampoco representa la ejecución técnica del proveedor utilizado
para entregar la comunicación.

Debe mantenerse:

```text
QueueNotification

≠

Technical Delivery
```

---

# ConfirmNotificationDelivery

## Propósito

Confirmar dentro del dominio que la entrega de una Notification
Pending fue completada satisfactoriamente.

## Estado requerido

```text
Pending
```

## Estado resultante

```text
Delivered
```

## Eventos

```text
NotificationDelivered
```

## Reglas

`ConfirmNotificationDelivery` solamente puede ejecutarse cuando
existe una confirmación válida del resultado de entrega conforme
al contrato correspondiente.

El Command:

- confirma el resultado de entrega;
- no representa lectura del mensaje;
- no representa comprensión del contenido;
- no representa aceptación del contenido;
- no modifica al destinatario;
- no modifica el Aggregate originador.

Debe mantenerse:

```text
ConfirmNotificationDelivery

≠

ConfirmNotificationRead
```

y:

```text
Delivered

≠

Read
```

Delivered constituye un estado terminal en el Lifecycle
versión 1.0.

---

# ReportNotificationDeliveryFailure

## Propósito

Registrar que un intento de entrega de una Notification Pending
no pudo completarse satisfactoriamente.

## Estado requerido

```text
Pending
```

## Estado resultante

```text
Failed
```

## Eventos

```text
NotificationDeliveryFailed
```

## Reglas

`ReportNotificationDeliveryFailure` representa la incorporación
al dominio del resultado fallido de un intento de entrega.

El Command:

- conserva NotificationId;
- no elimina la Notification;
- no revierte el hecho de dominio que originó la Notification;
- no modifica directamente otro Aggregate;
- permite que la Notification pueda ser posteriormente
  reintentada conforme al Lifecycle.

Debe mantenerse:

```text
NotificationDeliveryFailure

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

# RetryNotification

## Propósito

Solicitar un nuevo intento de entrega para una Notification cuyo
último resultado fue Failed.

## Estado requerido

```text
Failed
```

## Estado resultante

```text
Pending
```

## Eventos

```text
NotificationRetried
```

## Reglas

`RetryNotification`:

- conserva NotificationId;
- no crea un nuevo Aggregate;
- conserva los hechos históricos anteriores;
- vuelve a situar la Notification en Pending;
- no produce directamente Delivered;
- no elimina el hecho NotificationDeliveryFailed anterior.

Debe mantenerse:

```text
RetryNotification

≠

CreateNotification
```

y:

```text
RetryNotification

≠

ConfirmNotificationDelivery
```

Después del reintento:

```text
Failed

    │
    ▼

Pending
```

será necesario un nuevo resultado explícito para alcanzar:

```text
Delivered
```

o nuevamente:

```text
Failed
```

---

# Matriz Command → Estado → Evento

```text
No Notification
      │
      │ CreateNotification
      ▼
    Draft
      │
      │ NotificationCreated
      │
      │ QueueNotification
      ▼
   Pending
      │
      ├──── ConfirmNotificationDelivery
      │              │
      │              ▼
      │          Delivered
      │              │
      │              └── NotificationDelivered
      │
      └──── ReportNotificationDeliveryFailure
                     │
                     ▼
                   Failed
                     │
                     ├── NotificationDeliveryFailed
                     │
                     │ RetryNotification
                     ▼
                   Pending
                     │
                     └── NotificationRetried
```

La representación anterior no sustituye la State Machine formal.

Las transiciones exactas pertenecen a:

```text
DOMAIN-011B-State-Machine.md
```

---

# Commands y Estados

La versión 1.0 mantiene la siguiente correspondencia:

| Command | Estado requerido | Estado resultante |
|---|---|---|
| CreateNotification | No Notification | Draft |
| QueueNotification | Draft | Pending |
| ConfirmNotificationDelivery | Pending | Delivered |
| ReportNotificationDeliveryFailure | Pending | Failed |
| RetryNotification | Failed | Pending |

Ningún Command puede utilizarse desde un estado distinto al
establecido por su contrato.

---

# Commands y Domain Events

La correspondencia oficial es:

| Command | Domain Event |
|---|---|
| CreateNotification | NotificationCreated |
| QueueNotification | NotificationQueued |
| ConfirmNotificationDelivery | NotificationDelivered |
| ReportNotificationDeliveryFailure | NotificationDeliveryFailed |
| RetryNotification | NotificationRetried |

Un Domain Event solamente existe cuando el Command fue aceptado y
el hecho ocurrió realmente.

---

# Commands sin Cambio Directo de Propiedades

Ningún Command representa un setter.

Por lo tanto, no existen Commands como:

```text
SetNotificationStatus

SetNotificationVersion

SetNotificationId
```

El cambio de estado es consecuencia del comportamiento del
Aggregate.

Conceptualmente:

```text
Command

      │
      ▼

Domain Behavior

      │
      ▼

State Transition
```

Nunca:

```text
Command

      │
      ▼

Direct Property Assignment
```

---

# Commands de Entrega

La ejecución técnica de una entrega no constituye un Command del
Aggregate.

Por lo tanto, el dominio no define Commands específicos para:

```text
SendEmail

SendSMS

SendPushNotification

CallProvider

PublishToQueue
```

Estos nombres describen mecanismos tecnológicos o acciones de
Infrastructure.

El dominio expresa intenciones y resultados mediante los Commands
oficiales de Notification.

Debe mantenerse:

```text
Domain Command

≠

Infrastructure Operation
```

---

# Commands de Canal

La versión 1.0 no introduce Commands adicionales para modificar
canales.

La existencia conceptual de canales dentro de Notification
Management no permite inferir automáticamente:

```text
ChangeNotificationChannel

AddNotificationChannel

RemoveNotificationChannel
```

La incorporación de cualquiera de estas capacidades requerirá una
evolución explícita del dominio.

---

# Commands de Destinatarios

La versión 1.0 no incorpora Commands separados para alterar
destinatarios después de la creación.

No deben inferirse:

```text
AddRecipient

RemoveRecipient

ChangeRecipient
```

sin una decisión explícita de evolución del Aggregate.

La definición de destinatarios necesaria para crear una
Notification debe respetar las Invariants oficiales que se definan
para el Aggregate.

---

# Commands de Plantillas

La existencia conceptual de plantillas dentro de Notification
Management no implica Commands de modificación de plantillas dentro
del Aggregate Notification.

La versión 1.0 no define:

```text
ChangeTemplate

UpdateTemplate

CreateTemplate
```

como Commands de Notification.

La evolución futura de este concepto deberá respetar el
Consistency Boundary y el Ubiquitous Language.

---

# Commands de Cancelación

El Lifecycle versión 1.0 no define:

```text
Cancelled
```

Por lo tanto no existe:

```text
CancelNotification
```

como Command oficial.

Su incorporación futura requeriría una evolución explícita de:

```text
Lifecycle

State Machine

Commands

Domain Events

Invariants
```

---

# Commands de Archivado

El Lifecycle versión 1.0 no define:

```text
Archived
```

como NotificationStatus.

Por lo tanto no existe:

```text
ArchiveNotification
```

como Command oficial.

La conservación histórica no requiere inferir un estado adicional.

---

# Commands de Lectura

Los Commands nunca representan consultas.

No son Commands:

```text
GetNotification

FindNotification

ListNotifications

SearchNotifications

GetNotificationHistory
```

Estas operaciones pertenecen al lado de lectura.

Debe mantenerse:

```text
Command Side

≠

Query Side
```

---

# Reglas Generales

Todo Command debe cumplir:

- NotificationId válido cuando corresponda;
- Version válida cuando la operación actúe sobre un Aggregate
  existente;
- autorización previa;
- estado compatible;
- transición válida;
- Invariants satisfechas;
- Value Objects válidos cuando correspondan;
- consistencia del Aggregate.

Una intención autorizada puede ser rechazada por Notification si
cualquiera de estas condiciones no se cumple.

---

# Commands Rechazados

El Aggregate debe rechazar Commands cuando:

- el estado actual no permite la transición;
- existe conflicto de Version;
- faltan condiciones requeridas;
- existen datos inválidos;
- se incumplen Invariants.

Una operación rechazada:

- no modifica NotificationStatus;
- no modifica el estado confirmado;
- no incrementa Version;
- no modifica UpdatedAt;
- no genera el Domain Event de éxito.

Conceptualmente:

```text
Command

      │
      ▼

Validation Failure

      │
      ▼

   Rejected
```

---

# Ejemplos de Commands Rechazados

Si:

```text
NotificationStatus = Draft
```

no puede ejecutarse:

```text
ConfirmNotificationDelivery
```

porque:

```text
Draft → Delivered
```

no forma parte del Lifecycle.

---

Si:

```text
NotificationStatus = Delivered
```

no puede ejecutarse:

```text
RetryNotification
```

porque Delivered es terminal.

---

Si:

```text
NotificationStatus = Failed
```

no puede ejecutarse directamente:

```text
ConfirmNotificationDelivery
```

porque el Lifecycle exige:

```text
Failed → Pending → Delivered
```

---

# Idempotencia

Los Application Services deben garantizar que un mismo Command no
produzca efectos duplicados cuando sea recibido más de una vez.

La estrategia concreta de identificación y deduplicación pertenece
a las capas responsables y no forma parte del Aggregate.

La idempotencia técnica no permite considerar válida una transición
que el dominio rechaza.

---

# Relación con Domain Events

Todo Command exitoso genera el Domain Event correspondiente al hecho
ocurrido.

```text
Command

        │

        ▼

Notification

        │

        ▼

Domain Event
```

Un Command nunca publica eventos directamente.

Notification produce el hecho después de:

- validar el estado;
- validar la transición;
- validar las Invariants;
- ejecutar el comportamiento;
- producir un nuevo estado consistente.

La definición formal de eventos pertenece a:

```text
DOMAIN-011D-Domain-Events.md
```

---

# Relación con Versioning

Todo Command que produzca una modificación válida incrementa:

```text
Version
```

Conceptualmente:

```text
Notification vN

      │
      ▼

Valid Command

      │
      ▼

Notification vN+1
```

Un Command rechazado conserva:

```text
Version = N
```

Las reglas formales pertenecen a:

```text
DOMAIN-011I-Versioning.md
```

---

# Relación con Permissions

La autorización se evalúa antes de ejecutar el Command sobre
Notification.

Sin embargo:

```text
Authorized Command

≠

Guaranteed State Transition
```

El Aggregate continúa protegiendo:

- Lifecycle;
- State Machine;
- Invariants;
- Versioning.

La definición completa pertenece a:

```text
DOMAIN-011F-Permissions.md
```

---

# Relación con Aggregate de Origen

Los Commands de Notification no modifican directamente el
Aggregate que originó la necesidad de comunicación.

Conceptualmente:

```text
Source Aggregate

      │
      ▼

Confirmed Fact

      │
      ▼

Notification Management

      │
      ▼

Notification Command
```

Cada Aggregate mantiene su propio Consistency Boundary.

Un fallo o reintento de Notification no revierte automáticamente el
hecho del Aggregate de origen.

---

# Relación con CQRS

Los Commands pertenecen exclusivamente al lado de escritura:

```text
Command Side
```

No pueden utilizarse para:

- consultas;
- listados;
- búsqueda;
- construcción de Read Models;
- proyecciones.

Las necesidades de consulta pertenecen a:

```text
DOMAIN-011L-Read-Model.md
```

---

# Compatibilidad con Event Sourcing

Cada Command válido puede originar un nuevo Domain Event que
represente la evolución histórica de Notification.

Una secuencia exitosa puede representar:

```text
CreateNotification

↓

NotificationCreated

↓

QueueNotification

↓

NotificationQueued

↓

ConfirmNotificationDelivery

↓

NotificationDelivered
```

Una secuencia con fallo y reintento puede representar:

```text
CreateNotification

↓

NotificationCreated

↓

QueueNotification

↓

NotificationQueued

↓

ReportNotificationDeliveryFailure

↓

NotificationDeliveryFailed

↓

RetryNotification

↓

NotificationRetried
```

Los Commands no forman parte del historial de hechos.

Los Domain Events representan los hechos consumados.

---

# Evolución

Nuevos Commands podrán incorporarse sin modificar los ya
existentes siempre que:

- representen una nueva intención real del dominio;
- respeten el Ubiquitous Language;
- respeten el Lifecycle;
- respeten la State Machine;
- no violen las Invariants;
- mantengan el Consistency Boundary;
- preserven NotificationId;
- mantengan la compatibilidad de contratos existentes;
- no introduzcan dependencias con Infrastructure.

Un nuevo proveedor tecnológico no constituye por sí mismo una
razón para crear un nuevo Command.

---

# Definición de Éxito

Los Commands del Aggregate **Notification** constituyen la única
interfaz válida para solicitar modificaciones sobre una unidad de
Notification dentro del ecosistema AURA.

La versión 1.0 define:

```text
CreateNotification

QueueNotification

ConfirmNotificationDelivery

ReportNotificationDeliveryFailure

RetryNotification
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

- los Commands expresan intención;
- los Commands no son setters;
- los Commands no son consultas;
- toda modificación atraviesa la Aggregate Root;
- CreateNotification crea exclusivamente en Draft;
- QueueNotification produce Draft → Pending;
- ConfirmNotificationDelivery produce Pending → Delivered;
- ReportNotificationDeliveryFailure produce Pending → Failed;
- RetryNotification produce Failed → Pending;
- Delivered permanece terminal;
- no existen Commands implícitos de cancelación o archivado;
- no existen Commands derivados de proveedores tecnológicos;
- una operación rechazada conserva estado y Version;
- solamente operaciones válidas generan Domain Events de éxito;
- los Commands no modifican directamente otros Aggregates;
- CQRS mantiene Commands exclusivamente en el Write Side;
- Event Sourcing utiliza los hechos resultantes y no los Commands
  como historia del Aggregate.

De esta forma, `DOMAIN-011C-Commands.md` define oficialmente las
intenciones de escritura del Aggregate **Notification** conforme al
Lifecycle y al patrón consolidado de AURA Core.