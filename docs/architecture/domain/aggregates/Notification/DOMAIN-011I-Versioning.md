# DOMAIN-011I — Notification Versioning

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
- DOMAIN-011D-Domain-Events.md
- DOMAIN-011E-Invariants.md
- DOMAIN-011G-Repository-Contract.md

---

# Objetivo

Este documento define las reglas oficiales de Versioning del
Aggregate **Notification**.

Version representa la evolución lógica del Aggregate y permite
controlar modificaciones concurrentes sin introducir dependencia
con una tecnología específica de persistencia.

El Versioning protege:

- consistencia;
- orden lógico;
- concurrencia optimista;
- trazabilidad;
- relación entre modificaciones y Domain Events.

---

# Principios

El Versioning de Notification cumple:

- toda modificación válida incrementa Version;
- toda operación rechazada conserva Version;
- toda lectura conserva Version;
- la reconstrucción conserva la Version correspondiente al estado
  reconstruido;
- AggregateVersion de un Domain Event corresponde a la Version
  resultante de la modificación;
- la publicación de Integration Events no incrementa Version;
- la actualización de Read Models no incrementa Version;
- operaciones de Infrastructure no modifican Version por sí mismas.

Debe mantenerse:

```text
Version

=

Logical Aggregate Evolution
```

y no:

```text
Version

=

Technical Operation Counter
```

---

# Concepto

Notification mantiene:

```text
Version
```

como parte de su estado consistente.

Version permite identificar la evolución aceptada del mismo:

```text
NotificationId
```

Conceptualmente:

```text
Notification vN

      │
      ▼

Valid Modification

      │
      ▼

Notification vN+1
```

Version pertenece al Aggregate.

No representa:

- número de intentos técnicos;
- número de llamadas a un proveedor;
- número de lecturas;
- versión de una API;
- versión de un Integration Event;
- versión de un Read Model;
- versión de infraestructura.

---

# Ciclo de Vida

El Lifecycle oficial produce evolución de Version cuando ocurre una
transición válida.

La secuencia básica exitosa es:

```text
CreateNotification

↓

NotificationCreated

↓

Version 1

↓

QueueNotification

↓

NotificationQueued

↓

Version 2

↓

ConfirmNotificationDelivery

↓

NotificationDelivered

↓

Version 3
```

Una secuencia con fallo y reintento puede ser:

```text
CreateNotification

↓

NotificationCreated

↓

Version 1

↓

QueueNotification

↓

NotificationQueued

↓

Version 2

↓

ReportNotificationDeliveryFailure

↓

NotificationDeliveryFailed

↓

Version 3

↓

RetryNotification

↓

NotificationRetried

↓

Version 4

↓

ConfirmNotificationDelivery

↓

NotificationDelivered

↓

Version 5
```

---

# Operaciones que Incrementan la Versión

Toda modificación válida del Aggregate incrementa Version una vez.

Para los Commands oficiales:

```text
CreateNotification

QueueNotification

ConfirmNotificationDelivery

ReportNotificationDeliveryFailure

RetryNotification
```

una ejecución válida produce:

```text
Version N

↓

Valid Command

↓

Version N + 1
```

Debe mantenerse:

```text
One Valid Aggregate Modification

=

One Version Increment
```

---

# Operaciones que No Incrementan la Versión

No incrementan Version:

- operaciones rechazadas;
- consultas;
- carga del Aggregate;
- reconstrucción;
- actualización de Read Models;
- publicación de Domain Events ya producidos;
- publicación de Integration Events;
- reintentos técnicos de publicación externa;
- operaciones de Audit;
- procesamiento realizado por consumidores externos.

Debe mantenerse:

```text
No Aggregate Modification

↓

No Version Increment
```

---

# Operación Rechazada

Una operación rechazada conserva:

```text
Version = N
```

antes y después del intento.

Conceptualmente:

```text
Notification vN

      │
      ▼

Invalid Command

      │
      ▼

   Rejected

      │
      ▼

Notification vN
```

La operación rechazada tampoco produce el Domain Event de éxito.

---

# Concurrencia Optimista

Notification utiliza:

```text
Optimistic Concurrency Control
```

Cada operación de persistencia debe verificar que la Version sobre
la cual se ejecutó el comportamiento corresponda a la Version
actualmente persistida.

Conceptualmente:

```text
ExpectedVersion

=

PersistedVersion
```

permite continuar con la persistencia.

Si:

```text
ExpectedVersion

≠

PersistedVersion
```

debe producirse:

```text
ConcurrencyConflict
```

---

# Conflicto de Concurrencia

Ejemplo:

```text
PersistedVersion = 7

Process A loads Version 7

Process B loads Version 7
```

Process A confirma una modificación:

```text
PersistedVersion = 8
```

Process B intenta posteriormente persistir usando:

```text
ExpectedVersion = 7
```

pero encuentra:

```text
PersistedVersion = 8
```

El resultado debe ser:

```text
ConcurrencyConflict
```

Process B no puede sobrescribir silenciosamente el estado
confirmado por Process A.

---

# Persistencia

El Repository debe preservar coherencia entre:

```text
Notification State

Version

Domain Events
```

El Repository no decide cuándo incrementar Version.

El incremento corresponde a una modificación válida del Aggregate.

El Repository verifica y persiste la Version resultante conforme al
contrato de concurrencia.

Debe mantenerse:

```text
Aggregate Behavior

↓

Version Change

↓

Repository Persistence
```

Nunca:

```text
Repository

↓

Arbitrary Version Change
```

---

# Relación con Domain Events

Todo Domain Event oficial producido por una modificación válida
mantiene:

```text
AggregateVersion
```

correspondiente a la Version resultante del Aggregate.

Debe cumplirse:

```text
DomainEvent.AggregateVersion

=

Notification.Version
```

después de la modificación que produjo el evento.

---

# Secuencia de Domain Events

Para una Notification con entrega exitosa:

```text
Version 1
NotificationCreated

Version 2
NotificationQueued

Version 3
NotificationDelivered
```

Para una Notification con fallo y reintento:

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

AggregateVersion permite preservar el orden lógico para el mismo:

```text
NotificationId
```

---

# Relación con Integration Events

La publicación de un Integration Event no modifica por sí misma el
Aggregate Notification.

Por lo tanto:

```text
Integration Event Publication

≠

Aggregate Modification
```

y:

```text
Integration Event Publication

↓

No Version Increment
```

Un Integration Event puede transportar información relativa a una
Version del Aggregate cuando su contrato explícito así lo requiera,
pero su publicación no genera una nueva Version de Notification.

---

# Version del Aggregate versus Version del Contrato

Deben mantenerse separados:

```text
Notification.Version
```

y:

```text
Integration Contract Version
```

Notification.Version representa:

```text
Aggregate Evolution
```

mientras la versión de un contrato representa:

```text
Contract Evolution
```

Por lo tanto:

```text
Aggregate Version

≠

Integration Contract Version
```

---

# Relación con Outbox

Cuando la arquitectura utilice Outbox para publicación confiable de
eventos, la creación o procesamiento técnico del registro Outbox no
representa una nueva modificación del Aggregate.

Por lo tanto:

```text
Outbox Processing

↓

No Notification Version Increment
```

El Outbox conserva la información necesaria para publicar hechos
previamente confirmados.

No crea nuevos hechos de Notification.

---

# Publicación y Reintentos Técnicos

Un mismo Domain Event o Integration Event puede requerir múltiples
intentos técnicos de publicación.

Estos intentos no modifican:

```text
Notification.Version
```

Debe mantenerse:

```text
Message Publication Retry

≠

RetryNotification
```

`RetryNotification` constituye comportamiento de dominio:

```text
Failed → Pending
```

y sí incrementa Version cuando es válido.

Un reintento técnico de mensajería no constituye comportamiento del
Aggregate.

---

# Reintento de Notification

`RetryNotification` representa una modificación válida del
Aggregate.

Por lo tanto:

```text
Failed
  │
  │ RetryNotification
  ▼
Pending
```

produce:

```text
Version N

↓

Version N + 1
```

junto con:

```text
NotificationRetried
```

cuyo:

```text
AggregateVersion = N + 1
```

---

# Retry no Reinicia Version

Un reintento de Notification no crea un nuevo Aggregate.

Por lo tanto no reinicia Version.

Ejemplo:

```text
NotificationDeliveryFailed
AggregateVersion = 3

↓

RetryNotification

↓

NotificationRetried
AggregateVersion = 4
```

Debe mantenerse:

```text
Retry

≠

Version Reset
```

---

# Delivered y Version

Cuando:

```text
ConfirmNotificationDelivery
```

produce válidamente:

```text
Pending → Delivered
```

Version se incrementa.

El hecho:

```text
NotificationDelivered
```

mantiene la Version resultante.

Debido a que Delivered es terminal en la versión 1.0, no existen
posteriores transiciones ordinarias del Lifecycle que incrementen
Version desde ese estado.

---

# Recuperación

Recuperar una Notification desde el Repository no representa una
modificación.

Por lo tanto:

```text
findById(NotificationId)
```

debe restaurar:

```text
Notification

+

Current Version
```

sin incrementar Version.

Debe mantenerse:

```text
Load Aggregate

≠

Modify Aggregate
```

---

# Rehidratación

La rehidratación reconstruye el estado previamente confirmado del
Aggregate.

No representa comportamiento nuevo.

Por lo tanto no:

- incrementa Version;
- produce nuevos Domain Events;
- ejecuta Commands;
- crea nuevas transiciones.

Debe mantenerse:

```text
Rehydration

=

Restore Confirmed State
```

---

# Integración con Event Store

Cuando Notification utilice Event Sourcing, el Event Store debe
permitir reconstruir la evolución lógica del Aggregate mediante:

```text
NotificationId

+

AggregateVersion
```

Conceptualmente:

```text
NotificationCreated
AggregateVersion = 1

NotificationQueued
AggregateVersion = 2

NotificationDeliveryFailed
AggregateVersion = 3

NotificationRetried
AggregateVersion = 4

NotificationDelivered
AggregateVersion = 5
```

La reconstrucción produce:

```text
Notification.Version = 5
```

sin generar:

```text
Version = 6
```

por el solo acto de reconstruir.

---

# Orden Lógico

AggregateVersion establece el orden lógico de los hechos dentro de
una única Notification.

Debe mantenerse:

```text
Version N

precedes

Version N + 1
```

para el mismo:

```text
NotificationId
```

OccurredAt aporta contexto temporal.

No sustituye AggregateVersion como mecanismo de orden lógico del
Aggregate.

---

# Continuidad de Version

Una Notification debe evolucionar mediante una secuencia coherente:

```text
1

2

3

4

...
```

conforme ocurran modificaciones válidas.

Una operación rechazada no crea una nueva posición en la secuencia.

No debe existir:

```text
Version N

↓

Rejected Operation

↓

Version N + 1
```

---

# Integración con CQRS

El Write Model mantiene la Version autoritativa del Aggregate.

Los Read Models pueden proyectar:

```text
Version
```

cuando sea útil para consultas o trazabilidad.

Sin embargo:

```text
ReadModel.Version

```

no modifica:

```text
Notification.Version
```

Las proyecciones permanecen fuera del Consistency Boundary de
escritura.

---

# Read Model Desactualizado

Debido a consistencia eventual, un Read Model puede representar
temporalmente una Version anterior a la Version actual del
Aggregate.

Conceptualmente:

```text
Notification.Version = N

ReadModel projected Version = N - 1
```

durante una ventana de propagación.

Esto no modifica la Version del Aggregate ni invalida el estado
confirmado de Notification.

---

# Version y Audit

Audit puede utilizar Version como elemento de trazabilidad.

Conceptualmente:

```text
NotificationId

+

Version

+

Domain Event
```

permiten identificar la evolución lógica de Notification.

Audit permanece fuera del Aggregate.

Un Audit Record no incrementa:

```text
Notification.Version
```

---

# Version y Aggregate de Origen

Notification mantiene Version independiente del Aggregate que
originó la necesidad de comunicación.

Por ejemplo:

```text
Assembly.Version

≠

Notification.Version
```

y:

```text
Document.Version

≠

Notification.Version
```

Cada Aggregate mantiene su propia secuencia de evolución.

Una modificación de Notification no incrementa Version de otro
Aggregate.

---

# Consistency Boundary

Version pertenece al Consistency Boundary de Notification.

Debe persistirse coherentemente con el estado resultante de la misma
modificación.

Conceptualmente:

```text
Notification State

+

Notification Version

=

Same Aggregate Consistency Boundary
```

No existe una Version compartida entre Aggregates.

---

# Version y Estado

Version no reemplaza NotificationStatus.

Debe mantenerse:

```text
NotificationStatus

=

Lifecycle Position
```

mientras:

```text
Version

=

Logical Evolution Number
```

Dos Notifications pueden encontrarse en el mismo estado y tener
diferentes Version.

Por ejemplo:

```text
Notification A

Status = Pending

Version = 2
```

y:

```text
Notification B

Status = Pending

Version = 4
```

cuando Notification B haya experimentado fallo y reintento.

---

# Version y UpdatedAt

Version y UpdatedAt representan conceptos diferentes.

Debe mantenerse:

```text
Version

≠

UpdatedAt
```

Version establece la evolución lógica.

UpdatedAt aporta información temporal sobre la última modificación
válida.

Ambos pueden cambiar como consecuencia de una misma modificación
válida sin representar el mismo concepto.

---

# Version y CreatedAt

CreatedAt permanece inmutable durante todo el Lifecycle.

Version puede incrementarse múltiples veces.

Debe mantenerse:

```text
CreatedAt

=

Creation Time
```

y:

```text
Version

=

Aggregate Evolution
```

---

# Versionado del Contrato

La evolución de los contratos de Notification debe mantenerse
separada de Version.

Cambios futuros en:

- Commands;
- Domain Events;
- Integration Events;
- Read Models;
- esquemas de serialización;

pueden requerir versionado de sus propios contratos.

Esto no implica modificar arbitrariamente:

```text
Notification.Version
```

Debe mantenerse:

```text
Domain Contract Version

≠

Aggregate Version
```

---

# Restricciones

No está permitido:

- modificar Version directamente desde fuera del Aggregate;
- disminuir Version;
- reiniciar Version durante un Retry;
- incrementar Version por una consulta;
- incrementar Version por una operación rechazada;
- incrementar Version por reconstrucción;
- incrementar Version por publicación de eventos;
- incrementar Version por actualización de Read Models;
- compartir Version entre diferentes Aggregates;
- utilizar UpdatedAt como sustituto de Version;
- utilizar Version como sustituto de NotificationStatus;
- permitir una escritura obsoleta sin detectar conflicto.

---

# Reglas

## REG-001

Toda Notification nueva comienza su evolución lógica con:

```text
Version = 1
```

después de `CreateNotification` válido.

---

## REG-002

Toda modificación válida incrementa Version exactamente una vez.

---

## REG-003

Toda operación rechazada conserva Version.

---

## REG-004

Toda lectura conserva Version.

---

## REG-005

Todo Domain Event producido por una modificación válida mantiene:

```text
AggregateVersion = resulting Notification.Version
```

---

## REG-006

Una escritura con ExpectedVersion diferente de PersistedVersion
debe producir:

```text
ConcurrencyConflict
```

---

## REG-007

RetryNotification incrementa Version y nunca la reinicia.

---

## REG-008

Publicar Domain Events o Integration Events no incrementa Version.

---

## REG-009

Rehidratar o reconstruir Notification no incrementa Version ni
produce nuevos hechos.

---

## REG-010

Aggregate Version, Integration Contract Version y cualquier versión
técnica permanecen como conceptos independientes.

---

# Compatibilidad con Event Sourcing

El Versioning permite reconstruir de forma determinista la
evolución de Notification.

Los eventos pueden ordenarse lógicamente mediante:

```text
AggregateVersion
```

para el mismo NotificationId.

Una secuencia válida con reintento puede ser:

```text
1 — NotificationCreated

2 — NotificationQueued

3 — NotificationDeliveryFailed

4 — NotificationRetried

5 — NotificationDelivered
```

La reconstrucción produce:

```text
NotificationStatus = Delivered

Notification.Version = 5
```

sin modificar los eventos históricos.

---

# Compatibilidad con CQRS

Version pertenece al Write Model.

Puede proyectarse hacia Read Models para:

- trazabilidad;
- sincronización;
- presentación del estado proyectado;
- detección de proyecciones pendientes.

Sin embargo, los Read Models no son autoridad para modificar la
Version del Aggregate.

Debe mantenerse:

```text
Write Model Version

=

Aggregate Authority
```

y:

```text
Read Model Version

=

Projection Information
```

---

# Definición de Éxito

El Versioning del Aggregate **Notification** permite representar de
forma consistente su evolución lógica y proteger modificaciones
concurrentes dentro del ecosistema AURA.

El modelo garantiza que:

- toda Notification creada válidamente comienza en Version 1;
- toda modificación válida incrementa Version exactamente una vez;
- toda operación rechazada conserva Version;
- las consultas no incrementan Version;
- RetryNotification incrementa Version sin reiniciarla;
- AggregateVersion de cada Domain Event corresponde a la Version
  resultante;
- la secuencia de eventos mantiene orden lógico;
- Optimistic Concurrency detecta escrituras obsoletas;
- una escritura concurrente incompatible produce
  ConcurrencyConflict;
- el Repository no modifica Version arbitrariamente;
- la rehidratación no incrementa Version;
- la reconstrucción por Event Sourcing conserva Version;
- la publicación de Domain Events no incrementa Version;
- la publicación de Integration Events no incrementa Version;
- el procesamiento de Outbox no incrementa Version;
- los reintentos técnicos de mensajería no equivalen a
  RetryNotification;
- los Read Models no modifican Version;
- Audit no modifica Version;
- cada Aggregate mantiene Version independiente;
- Version no reemplaza NotificationStatus;
- Version no reemplaza UpdatedAt;
- Aggregate Version y Contract Version permanecen separados;
- CQRS y Event Sourcing permanecen compatibles.

De esta forma, `DOMAIN-011I-Versioning.md` establece las reglas
oficiales de evolución lógica y concurrencia del Aggregate
**Notification** conforme al patrón consolidado de AURA Core.