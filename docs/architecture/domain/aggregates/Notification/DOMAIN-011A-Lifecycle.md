# DOMAIN-011A — Notification Lifecycle

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Notification Management

Aggregate:
Notification

Documento relacionado:

- DOMAIN-011-Aggregate.md
- DOMAIN-011B-State-Machine.md
- DOMAIN-011C-Commands.md
- DOMAIN-011D-Domain-Events.md
- DOMAIN-011E-Invariants.md

---

# Objetivo

Este documento define el ciclo de vida oficial del Aggregate
**Notification**.

Describe las etapas por las que transita una Notification desde su
creación hasta la confirmación de su entrega, incluyendo el manejo
explícito de intentos fallidos y reintentos.

El Lifecycle representa únicamente la evolución funcional del
Aggregate.

Las reglas exactas de transición se documentan formalmente en:

```text
DOMAIN-011B-State-Machine.md
```

---

# Principios

El ciclo de vida debe garantizar:

- identidad única;
- evolución controlada;
- trazabilidad completa;
- separación entre dominio e Infrastructure;
- representación explícita del resultado de entrega;
- manejo explícito de fallos;
- reintentos controlados;
- cumplimiento de Invariants;
- Versioning consistente;
- compatibilidad con Event Sourcing;
- preparación para Audit.

El Lifecycle pertenece exclusivamente a Notification.

El Lifecycle del Aggregate que originó la necesidad de comunicación
permanece independiente.

---

# Etapas del ciclo de vida

El Aggregate Notification evoluciona mediante las siguientes
etapas:

```text
No Notification
      │
      ▼
    Draft
      │
      ▼
   Pending
      │
      ├──────────────► Delivered
      │
      ▼
    Failed
      │
      ▼
   Pending
```

Los estados oficiales de Notification versión 1.0 son:

```text
Draft

Pending

Delivered

Failed
```

---

# Draft

Representa una Notification creada dentro del dominio pero que
todavía no ha sido incorporada al proceso de entrega.

En este estado:

- existe NotificationId;
- existe una unidad formal de Notification;
- pueden establecerse las condiciones necesarias para la
  comunicación;
- todavía no existe una entrega confirmada;
- todavía no existe un intento fallido de entrega.

Draft constituye el estado inicial obligatorio de toda nueva
Notification.

Conceptualmente:

```text
No Notification

↓

Draft
```

El hecho de dominio correspondiente es:

```text
NotificationCreated
```

---

# Pending

Representa una Notification preparada para participar del proceso
de entrega y cuyo resultado todavía no ha sido confirmado.

En este estado:

- la Notification continúa existiendo dentro de su propio
  Consistency Boundary;
- la entrega todavía no ha sido confirmada como exitosa;
- la entrega todavía no ha sido confirmada como fallida;
- el mecanismo técnico utilizado para ejecutar la entrega
  permanece fuera del Aggregate.

Conceptualmente:

```text
Draft

↓

Pending
```

El hecho de dominio correspondiente es:

```text
NotificationQueued
```

Pending no significa:

```text
Delivered
```

y tampoco significa:

```text
Failed
```

Representa una Notification cuyo resultado de entrega permanece
pendiente.

---

# Delivered

Representa una Notification cuya entrega fue confirmada
exitosamente conforme al contrato aplicable al canal utilizado.

Conceptualmente:

```text
Pending

↓

Delivered
```

El hecho de dominio correspondiente es:

```text
NotificationDelivered
```

Delivered significa que el proceso de entrega bajo responsabilidad
de Notification Management fue completado satisfactoriamente.

Delivered no implica necesariamente:

- lectura por parte del destinatario;
- comprensión del contenido;
- aceptación del contenido;
- ejecución de una acción posterior;
- modificación de otro Aggregate.

Debe mantenerse:

```text
Delivered

≠

Read
```

y:

```text
NotificationDelivered

≠

External Aggregate Modification
```

Delivered constituye un estado terminal del Lifecycle versión 1.0.

---

# Failed

Representa una Notification cuyo intento de entrega no pudo
completarse satisfactoriamente.

Conceptualmente:

```text
Pending

↓

Failed
```

El hecho de dominio correspondiente es:

```text
NotificationDeliveryFailed
```

Failed:

- conserva NotificationId;
- conserva trazabilidad;
- conserva Version;
- no elimina la Notification;
- no elimina los hechos anteriores;
- puede permitir un reintento explícito.

Un fallo de entrega no modifica el Aggregate que originó la
necesidad de comunicación.

Debe mantenerse:

```text
NotificationDeliveryFailed

≠

Source Domain Fact Failed
```

---

# Retry

Una Notification en estado Failed puede volver a participar del
proceso de entrega mediante un reintento explícito.

Conceptualmente:

```text
Failed

↓

Pending
```

El hecho de dominio correspondiente es:

```text
NotificationRetried
```

El reintento:

- no crea una nueva Notification;
- conserva NotificationId;
- conserva el historial previo;
- incrementa Version como modificación válida;
- representa una nueva evolución del mismo Aggregate.

Debe mantenerse:

```text
Retry

≠

New Notification
```

y:

```text
Failed

↓

Pending

≠

Historical Rewrite
```

El hecho anterior:

```text
NotificationDeliveryFailed
```

permanece inmutable.

---

# Flujo Principal

El flujo principal del Lifecycle es:

```text
No Notification
      │
      ▼
    Draft
      │
      ▼
   Pending
      │
      ▼
  Delivered
```

Representa:

```text
creación

↓

preparación para entrega

↓

entrega confirmada
```

---

# Flujo de Fallo

Cuando el proceso de entrega no puede completarse:

```text
Pending
   │
   ▼
 Failed
```

El Aggregate conserva su identidad e historial.

El fallo no produce eliminación de la Notification.

---

# Flujo de Reintento

Una Notification Failed puede reingresar al proceso de entrega:

```text
Failed
   │
   ▼
Pending
```

y posteriormente puede evolucionar nuevamente hacia:

```text
Pending
   │
   ├────────► Delivered
   │
   ▼
 Failed
```

Cada nuevo resultado pertenece a la evolución del mismo
NotificationId.

---

# Transiciones Oficiales

La versión 1.0 define conceptualmente:

```text
No Notification → Draft

Draft → Pending

Pending → Delivered

Pending → Failed

Failed → Pending
```

No existe otra transición oficial fuera de este conjunto.

Las condiciones exactas, Guards y validaciones pertenecen a:

```text
DOMAIN-011B-State-Machine.md

DOMAIN-011E-Invariants.md
```

---

# Transiciones Prohibidas

No están permitidas:

```text
Draft → Delivered

Draft → Failed

Delivered → Draft

Delivered → Pending

Delivered → Failed

Failed → Draft

Failed → Delivered
```

Una Notification Failed debe pasar primero por:

```text
Pending
```

antes de alcanzar un nuevo resultado de entrega.

Una Notification Delivered no vuelve al ciclo operativo ordinario.

---

# Estado Inicial

Toda Notification nueva comienza exclusivamente en:

```text
Draft
```

No puede crearse directamente en:

```text
Pending

Delivered

Failed
```

Debe mantenerse:

```text
Create Notification

↓

Draft
```

---

# Estado Terminal

En la versión 1.0:

```text
Delivered
```

constituye el estado terminal exitoso del Aggregate.

Una Notification Delivered no puede:

- volver a Draft;
- volver a Pending;
- pasar a Failed;
- ser reintentada mediante una operación ordinaria.

La entrega confirmada constituye un hecho histórico.

---

# Failed no es Terminal

Failed no constituye necesariamente el final del Lifecycle.

El dominio permite:

```text
Failed → Pending
```

mediante un reintento explícito.

Sin embargo, el Lifecycle versión 1.0 no define:

- cantidad máxima de reintentos;
- intervalo entre reintentos;
- estrategia de backoff;
- ventanas temporales;
- proveedor específico;
- scheduler específico.

Estas condiciones no deben inferirse desde el Lifecycle.

---

# Reintentos y Estado

Un reintento nunca modifica directamente:

```text
Failed → Delivered
```

Primero debe existir:

```text
Failed → Pending
```

y posteriormente un nuevo resultado válido:

```text
Pending → Delivered
```

o:

```text
Pending → Failed
```

Esto permite representar explícitamente cada nueva tentativa dentro
de la evolución del Aggregate.

---

# Entrega y Lectura

El Lifecycle de Notification termina funcionalmente con la entrega
confirmada.

La versión 1.0 no incorpora estados:

```text
Read

Opened

Acknowledged
```

como parte del Lifecycle oficial.

Por lo tanto:

```text
Delivered

≠

Read
```

Cualquier necesidad futura de representar lectura, apertura o
confirmación por parte del destinatario requerirá una evolución
explícita del dominio.

---

# Eliminación

El Lifecycle versión 1.0 no utiliza eliminación física como
transición ordinaria del Aggregate.

Un fallo de entrega no implica eliminación.

Una entrega confirmada no implica eliminación.

Debe mantenerse:

```text
Failed

≠

Deleted
```

y:

```text
Delivered

≠

Deleted
```

La eliminación física, cuando fuese requerida por políticas
externas, no constituye una transición ordinaria definida por este
Lifecycle.

---

# Archived

La versión 1.0 no incorpora:

```text
Archived
```

como NotificationStatus.

No debe inferirse un estado Archived por analogía con otros
Aggregates.

La conservación histórica de una Notification se garantiza mediante
su identidad, Version y hechos de dominio sin introducir una
transición adicional no requerida por este Lifecycle.

---

# Cancelación

La versión 1.0 no define:

```text
Cancelled
```

como estado oficial.

Tampoco define una transición de cancelación.

La incorporación futura de una capacidad de cancelación requiere
evolución explícita del modelo y actualización coordinada de:

```text
Lifecycle

State Machine

Commands

Domain Events

Invariants
```

---

# Relación con Commands

Cada transición debe producirse mediante comportamiento explícito
del Aggregate.

Los Commands exactos responsables de expresar las intenciones que
originan estas transiciones se especifican en:

```text
DOMAIN-011C-Commands.md
```

El Lifecycle no permite modificación directa de
NotificationStatus.

Debe mantenerse:

```text
Command

↓

Notification

↓

Validate

↓

State Transition
```

Nunca:

```text
External Actor

↓

Direct Status Mutation
```

---

# Relación con Domain Events

Las transiciones oficiales corresponden conceptualmente a los
siguientes hechos:

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

Estos eventos representan hechos consumados.

No representan intenciones.

La especificación formal pertenece a:

```text
DOMAIN-011D-Domain-Events.md
```

---

# Versioning

Toda transición válida incrementa:

```text
Version
```

Conceptualmente:

```text
Version N

↓

Valid Lifecycle Transition

↓

Version N + 1
```

Una transición rechazada:

- no modifica NotificationStatus;
- no incrementa Version;
- no produce el Domain Event de éxito.

Las reglas formales pertenecen a:

```text
DOMAIN-011I-Versioning.md
```

---

# Relación con el Aggregate de Origen

El Lifecycle de Notification permanece independiente del Lifecycle
del Aggregate que produjo el hecho originador.

Por ejemplo:

```text
Assembly

↓

Domain Fact

↓

Notification
```

Una Assembly puede haber confirmado su propio hecho mientras la
Notification todavía permanece:

```text
Pending
```

o incluso:

```text
Failed
```

Esto no invalida retrospectivamente el hecho de Assembly.

Debe mantenerse:

```text
Source Aggregate Commit

≠

Notification Delivery Result
```

---

# Consistencia Eventual

Notification opera fuera del Consistency Boundary del Aggregate
que originó la necesidad de comunicación.

Conceptualmente:

```text
Source Aggregate

↓

Confirmed Domain Fact

↓

Notification Management

↓

Notification Lifecycle
```

Puede existir una ventana temporal donde el hecho de origen ya está
confirmado y la Notification todavía no se encuentra Delivered.

Esto es consistente con los límites DDD de AURA.

---

# Fallo de Entrega

Un fallo en Notification:

- no revierte el hecho de dominio originador;
- no modifica directamente otro Aggregate;
- no elimina la Notification;
- conserva trazabilidad;
- permite un reintento explícito.

Debe mantenerse:

```text
Notification Failed

≠

Source Transaction Rollback
```

---

# Reglas Generales

Durante todo el Lifecycle se cumplen las siguientes reglas:

- NotificationId nunca cambia.
- Toda Notification nueva comienza en Draft.
- NotificationStatus siempre pertenece al conjunto oficial.
- Toda transición debe estar definida por la State Machine.
- Ninguna transición ocurre mediante modificación directa.
- Toda modificación válida incrementa Version.
- Una transición rechazada conserva el estado confirmado.
- Una transición rechazada conserva Version.
- Una transición rechazada no genera Domain Events de éxito.
- Delivered es terminal en la versión 1.0.
- Failed puede volver únicamente a Pending mediante reintento.
- El historial permanece inmutable.
- Los Aggregates externos conservan Lifecycle independiente.
- La ejecución tecnológica de la entrega permanece fuera del
  Aggregate.

---

# Compatibilidad con Event Sourcing

El Lifecycle puede reconstruirse mediante la secuencia de Domain
Events.

Ejemplo exitoso:

```text
NotificationCreated

↓

NotificationQueued

↓

NotificationDelivered
```

Ejemplo con fallo y reintento:

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

Los hechos históricos no se reescriben.

El reintento agrega nuevos hechos a la historia del mismo
NotificationId.

---

# Compatibilidad con CQRS

Los Read Models pueden representar el estado actual de una
Notification sin consultar directamente el Aggregate.

Conceptualmente pueden distinguir:

```text
Draft

Pending

Delivered

Failed
```

Las proyecciones:

- no modifican Notification;
- no ejecutan transiciones;
- no sustituyen la State Machine;
- pueden reconstruirse desde hechos confirmados.

---

# Objetivos del Lifecycle

El ciclo de vida garantiza:

- creación explícita;
- preparación explícita para entrega;
- diferenciación entre resultado exitoso y fallido;
- reintento explícito;
- estado terminal exitoso;
- trazabilidad completa;
- identidad persistente;
- consistencia interna;
- separación del Aggregate de origen;
- consistencia eventual entre contextos;
- independencia del proveedor tecnológico;
- compatibilidad con CQRS;
- compatibilidad con Event Sourcing;
- evolución futura controlada.

---

# Definición de Éxito

El Lifecycle del Aggregate **Notification** proporciona un modelo
predecible y trazable para administrar la evolución de una
comunicación dentro del ecosistema AURA.

La versión 1.0 establece oficialmente:

```text
Draft

Pending

Delivered

Failed
```

y las transiciones:

```text
No Notification → Draft

Draft → Pending

Pending → Delivered

Pending → Failed

Failed → Pending
```

El modelo garantiza que:

- toda Notification nace en Draft;
- Pending representa una entrega cuyo resultado aún no está
  confirmado;
- Delivered representa una entrega confirmada exitosamente;
- Failed representa un intento de entrega fallido;
- Failed puede volver a Pending mediante un reintento explícito;
- Delivered es terminal;
- Delivered no implica lectura;
- Failed no elimina la Notification;
- no existe Archived en la versión 1.0;
- no existe Cancelled en la versión 1.0;
- no existe eliminación física como transición ordinaria;
- toda transición válida incrementa Version;
- toda transición válida produce el hecho correspondiente;
- una transición rechazada conserva estado y Version;
- el Lifecycle de Notification permanece independiente del
  Lifecycle del Aggregate originador;
- la ejecución técnica de la entrega permanece fuera del dominio.

De esta forma, `DOMAIN-011A-Lifecycle.md` establece el ciclo de
vida oficial de **Notification** conforme al patrón consolidado de
AURA Core.