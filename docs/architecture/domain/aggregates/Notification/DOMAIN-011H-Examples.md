# DOMAIN-011H — Notification Examples

Versión: 1.1

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
- DOMAIN-011D-Domain-Events.md
- DOMAIN-011E-Invariants.md
- DOMAIN-011F-Permissions.md
- DOMAIN-011G-Repository-Contract.md

---

# Objetivo

Este documento presenta escenarios completos de negocio para
el Aggregate **Notification**.

Los ejemplos muestran cómo interactúan Commands, reglas de
negocio, transiciones de estado y Domain Events durante el
ciclo de vida de una Notification dentro de AURA.

Los ejemplos son conceptuales y no representan una
implementación tecnológica.

---

# Ejemplo 1 — Creación de una Notification

## Escenario

Un hecho confirmado dentro del ecosistema AURA genera una
necesidad de comunicación y Notification Management crea la
correspondiente Notification.

### Estado inicial

```text
No existe Aggregate.
```

### Command

```text
CreateNotification
```

### Resultado

```text
Notification

↓

State = Draft
```

### Domain Event

```text
NotificationCreated
```

La creación de la Notification no modifica el Aggregate que
originó la necesidad de comunicación.

---

# Ejemplo 2 — Incorporación al proceso de entrega

## Escenario

Una Notification existente en Draft cumple las condiciones
necesarias para incorporarse al proceso de entrega.

### Estado inicial

```text
Draft
```

### Command

```text
QueueNotification
```

### Estado final

```text
Pending
```

### Domain Event

```text
NotificationQueued
```

`Pending` representa que el resultado de entrega todavía no ha
sido confirmado.

---

# Ejemplo 3 — Entrega confirmada

## Escenario

Una Notification Pending obtiene una confirmación válida de
entrega.

### Estado inicial

```text
Pending
```

### Command

```text
ConfirmNotificationDelivery
```

### Estado final

```text
Delivered
```

### Domain Event

```text
NotificationDelivered
```

Delivered representa una entrega confirmada.

No representa:

```text
Read

Opened

Acknowledged
```

---

# Ejemplo 4 — Fallo de entrega

## Escenario

Una Notification Pending no puede completar satisfactoriamente
su intento de entrega.

### Estado inicial

```text
Pending
```

### Command

```text
ReportNotificationDeliveryFailure
```

### Estado final

```text
Failed
```

### Domain Event

```text
NotificationDeliveryFailed
```

La Notification conserva:

- NotificationId;
- Version;
- trazabilidad;
- hechos históricos.

El fallo no elimina el Aggregate.

---

# Ejemplo 5 — Reintento de una Notification

## Escenario

Una Notification cuyo último intento de entrega terminó en
Failed vuelve a incorporarse al proceso de entrega.

### Estado inicial

```text
Failed
```

### Command

```text
RetryNotification
```

### Estado final

```text
Pending
```

### Domain Event

```text
NotificationRetried
```

El reintento utiliza el mismo:

```text
NotificationId
```

y conserva el evento:

```text
NotificationDeliveryFailed
```

como hecho histórico.

---

# Ejemplo 6 — Reintento seguido de entrega exitosa

## Escenario

Una Notification falla durante su primer intento, es reintentada
y posteriormente obtiene una confirmación válida de entrega.

### Estado inicial

```text
Pending
```

### Primera operación

```text
ReportNotificationDeliveryFailure
```

### Resultado

```text
Failed
```

### Domain Event

```text
NotificationDeliveryFailed
```

### Segunda operación

```text
RetryNotification
```

### Resultado

```text
Pending
```

### Domain Event

```text
NotificationRetried
```

### Tercera operación

```text
ConfirmNotificationDelivery
```

### Resultado final

```text
Delivered
```

### Domain Event

```text
NotificationDelivered
```

La secuencia conserva todos los hechos anteriores.

---

# Ejemplo 7 — Reintento seguido de nuevo fallo

## Escenario

Una Notification Failed vuelve a Pending mediante un reintento,
pero el nuevo intento tampoco puede completarse.

### Estado inicial

```text
Failed
```

### Command

```text
RetryNotification
```

### Estado intermedio

```text
Pending
```

### Domain Event

```text
NotificationRetried
```

### Command posterior

```text
ReportNotificationDeliveryFailure
```

### Estado final

```text
Failed
```

### Domain Event

```text
NotificationDeliveryFailed
```

Ambos fallos permanecen como hechos históricos de la misma
Notification.

---

# Ejemplo 8 — Intento inválido de entrega desde Draft

## Escenario

Se intenta confirmar la entrega de una Notification que todavía
permanece en Draft.

### Estado inicial

```text
Draft
```

### Command

```text
ConfirmNotificationDelivery
```

### Resultado

```text
Rejected
```

### Motivo

La transición:

```text
Draft → Delivered
```

no está definida en el Lifecycle ni en la State Machine.

### Estado final

```text
Draft
```

### Domain Event

```text
Ninguno
```

Version permanece sin modificación.

---

# Ejemplo 9 — Intento inválido de fallo desde Draft

## Escenario

Se intenta registrar un fallo de entrega para una Notification
que todavía no se encuentra Pending.

### Estado inicial

```text
Draft
```

### Command

```text
ReportNotificationDeliveryFailure
```

### Resultado

```text
Rejected
```

### Motivo

La transición:

```text
Draft → Failed
```

no pertenece al Lifecycle oficial.

### Estado final

```text
Draft
```

### Domain Event

```text
Ninguno
```

---

# Ejemplo 10 — Intento de reintento desde Delivered

## Escenario

Se intenta reintentar una Notification cuya entrega ya fue
confirmada.

### Estado inicial

```text
Delivered
```

### Command

```text
RetryNotification
```

### Resultado

```text
Rejected
```

### Motivo

Delivered constituye un estado terminal en la versión 1.0.

### Estado final

```text
Delivered
```

### Domain Event

```text
Ninguno
```

---

# Ejemplo 11 — Intento de entrega directa desde Failed

## Escenario

Se intenta confirmar directamente como Delivered una
Notification cuyo estado actual es Failed.

### Estado inicial

```text
Failed
```

### Command

```text
ConfirmNotificationDelivery
```

### Resultado

```text
Rejected
```

### Motivo

La transición:

```text
Failed → Delivered
```

no existe.

El Lifecycle exige:

```text
Failed

↓

Pending

↓

Delivered
```

### Domain Event

```text
Ninguno
```

---

# Ejemplo 12 — Command autorizado pero inválido por estado

## Escenario

Un actor o proceso autorizado intenta ejecutar
RetryNotification sobre una Notification Pending.

### Autorización

```text
Authorized
```

### Estado inicial

```text
Pending
```

### Command

```text
RetryNotification
```

### Resultado

```text
Rejected
```

### Motivo

La autorización no reemplaza las reglas del dominio.

RetryNotification requiere:

```text
Failed
```

como estado de origen.

### Domain Event

```text
Ninguno
```

Debe mantenerse:

```text
Authorized

≠

Automatically Valid
```

---

# Ejemplo 13 — Hecho de Assembly que origina una Notification

## Escenario

Una Assembly produce un hecho confirmado que requiere una
comunicación posterior.

Conceptualmente:

```text
Assembly

    │
    ▼

Confirmed Domain Fact

    │
    ▼

Notification Management

    │
    ▼

CreateNotification
```

Notification Management crea:

```text
NotificationId
```

como identidad independiente.

### Resultado

```text
NotificationStatus = Draft
```

### Domain Event

```text
NotificationCreated
```

La Notification no modifica directamente Assembly.

Assembly conserva su propio:

- AssemblyId;
- Lifecycle;
- State Machine;
- Version;
- Consistency Boundary.

---

# Ejemplo 14 — Convocatoria de Assembly y entrega pendiente

## Escenario

Una Assembly ya confirmó su hecho de convocatoria y posteriormente
se creó una Notification para comunicarlo.

La Notification fue incorporada al proceso de entrega.

Conceptualmente:

```text
Assembly

Confirmed Fact
    │
    ▼

NotificationCreated
    │
    ▼

Draft
    │
    ▼

NotificationQueued
    │
    ▼

Pending
```

En este momento:

```text
Assembly Fact = Confirmed

NotificationStatus = Pending
```

Esta situación es válida.

La consistencia entre ambos Aggregates es independiente y puede
ser eventual.

---

# Ejemplo 15 — Fallo de Notification no revierte Assembly

## Escenario

Una Notification creada como consecuencia de un hecho de Assembly
falla durante su entrega.

### Notification

```text
Pending

↓

ReportNotificationDeliveryFailure

↓

Failed
```

### Domain Event

```text
NotificationDeliveryFailed
```

El hecho de Assembly que originó la comunicación permanece
confirmado.

Debe mantenerse:

```text
Notification Failed

≠

Assembly Rollback
```

Notification no modifica directamente Assembly.

---

# Ejemplo 16 — Notification asociada a Document

## Escenario

Una comunicación necesita hacer referencia a un Document ya
existente.

La relación utiliza:

```text
DocumentId
```

Notification no incorpora:

```text
Document
```

completo dentro de su Consistency Boundary.

Notification tampoco modifica:

- DocumentStatus;
- DocumentType;
- Content;
- Document.Version.

La existencia de una Notification asociada al Document no altera
el Lifecycle de Document.

---

# Ejemplo 17 — Delivered no significa Read

## Escenario

Una Notification alcanza Delivered después de una confirmación
válida de entrega.

### Estado final

```text
Delivered
```

Esto permite afirmar:

```text
Delivery Confirmed
```

pero no permite afirmar:

```text
Read

Opened

Acknowledged
```

La versión 1.0 no incorpora esos estados al Lifecycle.

---

# Ejemplo 18 — Fallo técnico de persistencia

## Escenario

Notification acepta una operación válida, pero el mecanismo de
persistencia no puede confirmar la escritura.

Conceptualmente:

```text
Repository

↓

PersistenceFailure
```

Esto no significa:

```text
NotificationStatus = Failed
```

Failed representa un resultado de entrega del dominio.

`PersistenceFailure` representa un fallo de persistencia.

Debe mantenerse:

```text
PersistenceFailure

≠

NotificationDeliveryFailed
```

---

# Ejemplo 19 — Conflicto de concurrencia

## Escenario

Dos operaciones intentan modificar la misma Notification utilizando
la misma Version inicial.

Conceptualmente:

```text
PersistedVersion = 4

Operation A
ExpectedVersion = 4

Operation B
ExpectedVersion = 4
```

Operation A se confirma primero:

```text
Version = 5
```

Cuando Operation B intenta persistirse:

```text
PersistedVersion = 5

ExpectedVersion = 4
```

### Resultado

```text
ConcurrencyConflict
```

La escritura obsoleta no sobrescribe el estado confirmado.

No se confirma un nuevo Domain Event de éxito para la operación
rechazada.

---

# Ejemplo 20 — Flujo completo exitoso

```text
CreateNotification
        │
        ▼
NotificationCreated
        │
        ▼
      Draft
        │
        ▼
QueueNotification
        │
        ▼
NotificationQueued
        │
        ▼
     Pending
        │
        ▼
ConfirmNotificationDelivery
        │
        ▼
NotificationDelivered
        │
        ▼
    Delivered
```

Delivered finaliza el Lifecycle operativo exitoso de la
Notification versión 1.0.

---

# Ejemplo 21 — Flujo completo con fallo y reintento

```text
CreateNotification
        │
        ▼
NotificationCreated
        │
        ▼
      Draft
        │
        ▼
QueueNotification
        │
        ▼
NotificationQueued
        │
        ▼
     Pending
        │
        ▼
ReportNotificationDeliveryFailure
        │
        ▼
NotificationDeliveryFailed
        │
        ▼
      Failed
        │
        ▼
RetryNotification
        │
        ▼
NotificationRetried
        │
        ▼
     Pending
        │
        ▼
ConfirmNotificationDelivery
        │
        ▼
NotificationDelivered
        │
        ▼
    Delivered
```

Todos los hechos pertenecen al mismo:

```text
NotificationId
```

y permanecen históricamente trazables.

---

# Ejemplo 22 — Reconstrucción mediante Event Sourcing

## Escenario

Se reconstruye una Notification a partir de:

```text
NotificationCreated

NotificationQueued

NotificationDeliveryFailed

NotificationRetried

NotificationDelivered
```

La aplicación cronológica de los hechos produce:

```text
Draft

↓

Pending

↓

Failed

↓

Pending

↓

Delivered
```

La identidad reconstruida permanece:

```text
NotificationId
```

y los eventos históricos no son modificados durante la
reconstrucción.

---

# Ejemplo 23 — Proyección CQRS

## Escenario

Los Domain Events confirmados alimentan un Read Model.

Conceptualmente:

```text
NotificationCreated

↓

NotificationQueued

↓

NotificationDelivered

↓

Projection

↓

Read Model
```

El Read Model puede representar:

```text
NotificationStatus = Delivered
```

sin adquirir autoridad para modificar el Aggregate.

Debe mantenerse:

```text
Read Model

≠

Aggregate Authority
```

---

# Ejemplo 24 — Ausencia de Integration Event automático

## Escenario

Una Notification alcanza válidamente:

```text
Delivered
```

y produce:

```text
NotificationDelivered
```

como Domain Event.

Este hecho no obliga automáticamente a producir un Integration
Event.

Debe mantenerse:

```text
NotificationDelivered

≠

Mandatory Integration Event
```

Un Integration Event solamente existe cuando haya un contrato
explícito definido para comunicación entre contextos o sistemas
externos.

---

# Relación con CQRS

Los Commands de estos ejemplos pertenecen al lado de escritura.

Los Domain Events generados pueden alimentar posteriormente los
Read Models utilizados para consultas.

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

Los Read Models no modifican Notification.

---

# Relación con Event Sourcing

Cada escenario puede reconstruirse reproduciendo en orden lógico
los Domain Events generados y registrados por el Aggregate.

Para un mismo:

```text
NotificationId
```

`AggregateVersion` permite preservar la secuencia lógica de
evolución.

Los hechos históricos permanecen inmutables.

La reconstrucción no ejecuta nuevos Commands ni genera nuevos
Domain Events.

---

# Definición de Éxito

Los ejemplos presentados demuestran el comportamiento esperado del
Aggregate **Notification** frente a situaciones habituales,
fallidas y excepcionales del dominio.

Los escenarios confirman que:

- toda Notification comienza en Draft;
- QueueNotification produce Draft → Pending;
- ConfirmNotificationDelivery produce Pending → Delivered;
- ReportNotificationDeliveryFailure produce Pending → Failed;
- RetryNotification produce Failed → Pending;
- Delivered permanece terminal;
- Failed permite reintento;
- un reintento conserva NotificationId;
- los fallos anteriores permanecen como hechos históricos;
- Delivered no significa Read;
- una transición inválida es rechazada;
- una operación rechazada no produce Domain Event de éxito;
- autorización no permite evitar State Machine o Invariants;
- Notification no modifica directamente el Aggregate de origen;
- un fallo de Notification no revierte el hecho originador;
- las referencias a otros Aggregates utilizan identificadores o
  contratos;
- PersistenceFailure no equivale a Notification Failed;
- los conflictos de concurrencia no sobrescriben silenciosamente
  el estado confirmado;
- los Read Models permanecen fuera de la autoridad de escritura;
- los Domain Events no generan automáticamente Integration Events;
- CQRS y Event Sourcing permanecen compatibles.

De esta forma, `DOMAIN-011H-Examples.md` sirve como referencia
conceptual para validar que Lifecycle, State Machine, Commands,
Domain Events, Invariants, Permissions y Repository Contract del
Aggregate **Notification** permanezcan coherentes dentro del
ecosistema AURA.