# DOMAIN-011M — Notification Test Scenarios

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
- DOMAIN-011F-Permissions.md
- DOMAIN-011G-Repository-Contract.md
- DOMAIN-011H-Examples.md
- DOMAIN-011I-Versioning.md
- DOMAIN-011J-Consistency-Boundary.md
- DOMAIN-011K-Integration-Events.md
- DOMAIN-011L-Read-Model.md

---

# Objetivo

Este documento define los escenarios conceptuales de prueba del
Aggregate **Notification**.

Los Test Scenarios verifican que el comportamiento del Aggregate
permanezca coherente con:

- Lifecycle;
- State Machine;
- Commands;
- Domain Events;
- Invariants;
- Permissions;
- Repository Contract;
- Versioning;
- Consistency Boundary;
- Integration Events;
- Read Models.

Estos escenarios representan reglas del dominio.

No establecen:

- framework de testing;
- lenguaje de programación;
- librería de assertions;
- motor de persistencia;
- broker;
- proveedor de entrega;
- tecnología de Infrastructure.

---

# Principios

Todo escenario debe validar conceptualmente:

```text
Given

When

Then
```

donde:

```text
Given
```

representa el estado confirmado previo.

```text
When
```

representa una intención o condición evaluada.

```text
Then
```

representa el resultado esperado del dominio.

---

# Reglas Generales de Prueba

Los escenarios deben comprobar:

- estado inicial válido;
- Command permitido;
- Command rechazado;
- transición válida;
- transición inválida;
- Domain Event esperado;
- ausencia de Domain Event de éxito ante rechazo;
- incremento correcto de Version;
- preservación de Version ante rechazo;
- preservación de NotificationId;
- preservación de CreatedAt;
- actualización de UpdatedAt cuando corresponde;
- Delivered terminal;
- Retry desde Failed;
- separación entre Notification y otros Aggregates;
- separación entre Domain Events e Integration Events;
- separación entre Write Model y Read Model.

---

# TS-001 — Crear Notification

## Given

```text
No Notification
```

## When

```text
CreateNotification
```

con una identidad válida.

## Then

debe existir:

```text
NotificationStatus = Draft
```

y:

```text
Version = 1
```

y debe producirse:

```text
NotificationCreated
```

Debe preservarse:

```text
NotificationId
```

como identidad inmutable del nuevo Aggregate.

---

# TS-002 — Crear Notification directamente en Pending

## Given

```text
No Notification
```

## When

se intenta crear una Notification cuyo estado inicial sea:

```text
Pending
```

## Then

la operación debe ser:

```text
Rejected
```

porque toda nueva Notification comienza exclusivamente en:

```text
Draft
```

No debe existir:

```text
NotificationQueued
```

como consecuencia de la creación inválida.

---

# TS-003 — Crear Notification directamente en Delivered

## Given

```text
No Notification
```

## When

se intenta crear una Notification directamente en:

```text
Delivered
```

## Then

la operación debe ser:

```text
Rejected
```

porque:

```text
No Notification → Delivered
```

no pertenece al Lifecycle.

---

# TS-004 — Queue Notification desde Draft

## Given

```text
NotificationStatus = Draft

Version = N
```

## When

```text
QueueNotification
```

## Then

debe producirse:

```text
Draft → Pending
```

y:

```text
Version = N + 1
```

y:

```text
NotificationQueued
```

---

# TS-005 — Queue Notification desde Pending

## Given

```text
NotificationStatus = Pending

Version = N
```

## When

```text
QueueNotification
```

## Then

la operación debe ser:

```text
Rejected
```

Debe mantenerse:

```text
NotificationStatus = Pending

Version = N
```

y no debe producirse:

```text
NotificationQueued
```

---

# TS-006 — Confirmar entrega desde Pending

## Given

```text
NotificationStatus = Pending

Version = N
```

## When

```text
ConfirmNotificationDelivery
```

con una confirmación válida de entrega.

## Then

debe producirse:

```text
Pending → Delivered
```

y:

```text
Version = N + 1
```

y:

```text
NotificationDelivered
```

---

# TS-007 — Confirmar entrega desde Draft

## Given

```text
NotificationStatus = Draft

Version = N
```

## When

```text
ConfirmNotificationDelivery
```

## Then

debe resultar:

```text
Rejected
```

porque:

```text
Draft → Delivered
```

no pertenece a la State Machine.

Debe conservarse:

```text
NotificationStatus = Draft

Version = N
```

y no debe producirse:

```text
NotificationDelivered
```

---

# TS-008 — Confirmar entrega desde Failed

## Given

```text
NotificationStatus = Failed

Version = N
```

## When

```text
ConfirmNotificationDelivery
```

## Then

debe resultar:

```text
Rejected
```

porque:

```text
Failed → Delivered
```

no es una transición válida.

Debe utilizarse primero:

```text
RetryNotification
```

para alcanzar:

```text
Pending
```

---

# TS-009 — Confirmar entrega desde Delivered

## Given

```text
NotificationStatus = Delivered

Version = N
```

## When

```text
ConfirmNotificationDelivery
```

## Then

debe resultar:

```text
Rejected
```

Delivered permanece terminal.

Debe conservarse:

```text
NotificationStatus = Delivered

Version = N
```

---

# TS-010 — Reportar fallo desde Pending

## Given

```text
NotificationStatus = Pending

Version = N
```

## When

```text
ReportNotificationDeliveryFailure
```

con un resultado fallido válido.

## Then

debe producirse:

```text
Pending → Failed
```

y:

```text
Version = N + 1
```

y:

```text
NotificationDeliveryFailed
```

---

# TS-011 — Reportar fallo desde Draft

## Given

```text
NotificationStatus = Draft

Version = N
```

## When

```text
ReportNotificationDeliveryFailure
```

## Then

debe resultar:

```text
Rejected
```

porque:

```text
Draft → Failed
```

no es válido.

Debe conservarse:

```text
NotificationStatus = Draft

Version = N
```

---

# TS-012 — Reportar fallo desde Delivered

## Given

```text
NotificationStatus = Delivered

Version = N
```

## When

```text
ReportNotificationDeliveryFailure
```

## Then

debe resultar:

```text
Rejected
```

Delivered no puede evolucionar hacia:

```text
Failed
```

---

# TS-013 — Retry desde Failed

## Given

```text
NotificationStatus = Failed

Version = N
```

## When

```text
RetryNotification
```

## Then

debe producirse:

```text
Failed → Pending
```

y:

```text
Version = N + 1
```

y:

```text
NotificationRetried
```

NotificationId debe permanecer inmutable.

---

# TS-014 — Retry desde Pending

## Given

```text
NotificationStatus = Pending

Version = N
```

## When

```text
RetryNotification
```

## Then

debe resultar:

```text
Rejected
```

porque RetryNotification requiere:

```text
NotificationStatus = Failed
```

Debe conservarse:

```text
Version = N
```

---

# TS-015 — Retry desde Delivered

## Given

```text
NotificationStatus = Delivered

Version = N
```

## When

```text
RetryNotification
```

## Then

debe resultar:

```text
Rejected
```

porque Delivered es terminal.

No debe producirse:

```text
NotificationRetried
```

---

# TS-016 — Retry no crea una nueva Notification

## Given

una Notification:

```text
NotificationId = N-001

NotificationStatus = Failed
```

## When

```text
RetryNotification
```

## Then

debe cumplirse:

```text
NotificationId before Retry

=

NotificationId after Retry
```

y no debe producirse:

```text
NotificationCreated
```

---

# TS-017 — Retry conserva el fallo histórico

## Given

existe en la historia:

```text
NotificationDeliveryFailed
```

## When

posteriormente ocurre:

```text
RetryNotification
```

## Then

el hecho:

```text
NotificationDeliveryFailed
```

debe permanecer inmutable en la historia.

Debe añadirse:

```text
NotificationRetried
```

sin reemplazar el evento anterior.

---

# TS-018 — Retry seguido de Delivered

## Given

```text
NotificationStatus = Failed
```

## When

ocurre:

```text
RetryNotification
```

seguido de:

```text
ConfirmNotificationDelivery
```

## Then

la evolución debe ser:

```text
Failed

↓

Pending

↓

Delivered
```

y los hechos:

```text
NotificationRetried

NotificationDelivered
```

deben corresponder a modificaciones distintas y Versions
sucesivas.

---

# TS-019 — Retry seguido de nuevo Failed

## Given

```text
NotificationStatus = Failed
```

## When

ocurre:

```text
RetryNotification

↓

ReportNotificationDeliveryFailure
```

## Then

la evolución debe ser:

```text
Failed

↓

Pending

↓

Failed
```

conservando todos los hechos históricos.

---

# TS-020 — Delivered es Terminal

## Given

```text
NotificationStatus = Delivered
```

## When

se intenta cualquier transición ordinaria del Lifecycle.

## Then

ninguna transición debe ser aceptada.

Debe mantenerse:

```text
NotificationStatus = Delivered
```

---

# TS-021 — Delivered no significa Read

## Given

```text
NotificationStatus = Delivered
```

## When

se consulta el significado de ese estado.

## Then

solamente puede afirmarse:

```text
Delivery Confirmed
```

No puede inferirse:

```text
Read

Opened

Acknowledged
```

---

# TS-022 — Failed no significa Deleted

## Given

```text
NotificationStatus = Failed
```

## When

se evalúa la existencia del Aggregate.

## Then

la Notification debe conservar:

```text
NotificationId

Version

State

History
```

Debe mantenerse:

```text
Failed

≠

Deleted
```

---

# TS-023 — Archived no es Estado Oficial

## Given

una Notification versión 1.0.

## When

se intenta asignar:

```text
Archived
```

como NotificationStatus.

## Then

la operación debe ser rechazada.

El conjunto válido permanece:

```text
Draft

Pending

Delivered

Failed
```

---

# TS-024 — Cancelled no es Estado Oficial

## Given

una Notification versión 1.0.

## When

se intenta asignar:

```text
Cancelled
```

## Then

la operación debe ser rechazada.

No existe:

```text
CancelNotification
```

como Command oficial.

---

# TS-025 — NotificationId es Inmutable

## Given

```text
NotificationId = N-001
```

## When

se ejecuta cualquier modificación válida del Lifecycle.

## Then

debe permanecer:

```text
NotificationId = N-001
```

---

# TS-026 — NotificationId no puede modificarse directamente

## Given

una Notification existente.

## When

un actor intenta modificar directamente:

```text
NotificationId
```

## Then

la operación debe ser imposible desde la interfaz pública del
Aggregate.

---

# TS-027 — Estado no puede modificarse directamente

## Given

```text
NotificationStatus = Draft
```

## When

un actor intenta asignar directamente:

```text
NotificationStatus = Delivered
```

## Then

la modificación debe ser imposible.

Todo cambio de estado debe atravesar comportamiento válido de:

```text
Notification
```

---

# TS-028 — Toda modificación válida incrementa Version

## Given

```text
Version = N
```

## When

un Command válido modifica el Aggregate.

## Then

debe cumplirse:

```text
Version = N + 1
```

---

# TS-029 — Operación rechazada conserva Version

## Given

```text
NotificationStatus = Draft

Version = N
```

## When

se ejecuta:

```text
ConfirmNotificationDelivery
```

## Then

debe resultar:

```text
Rejected
```

y:

```text
Version = N
```

---

# TS-030 — Lectura no incrementa Version

## Given

```text
Notification.Version = N
```

## When

el Repository recupera la Notification.

## Then

debe mantenerse:

```text
Notification.Version = N
```

---

# TS-031 — Rehidratación no incrementa Version

## Given

una secuencia histórica que produce:

```text
Version = N
```

## When

Notification es rehidratada.

## Then

debe resultar:

```text
Version = N
```

y no:

```text
Version = N + 1
```

---

# TS-032 — Domain Event mantiene AggregateVersion

## Given

```text
Notification.Version = N
```

## When

una modificación válida produce:

```text
Notification.Version = N + 1
```

## Then

el Domain Event correspondiente debe mantener:

```text
AggregateVersion = N + 1
```

---

# TS-033 — Operación rechazada no genera Domain Event de Éxito

## Given

```text
NotificationStatus = Draft
```

## When

se ejecuta:

```text
ConfirmNotificationDelivery
```

## Then

no debe existir:

```text
NotificationDelivered
```

---

# TS-034 — Domain Events son Inmutables

## Given

existe:

```text
NotificationDeliveryFailed
```

## When

posteriormente la Notification alcanza:

```text
Delivered
```

## Then

`NotificationDeliveryFailed` debe permanecer como hecho histórico
sin modificación.

---

# TS-035 — Orden de Domain Events

## Given

una secuencia válida:

```text
NotificationCreated
AggregateVersion = 1

NotificationQueued
AggregateVersion = 2

NotificationDelivered
AggregateVersion = 3
```

## When

se reconstruye la evolución lógica.

## Then

el orden debe respetar:

```text
1 < 2 < 3
```

para el mismo NotificationId.

---

# TS-036 — Conflicto de Concurrencia

## Given

```text
PersistedVersion = 5

ExpectedVersion = 4
```

## When

se intenta persistir una modificación.

## Then

debe producirse:

```text
ConcurrencyConflict
```

La escritura obsoleta no debe sobrescribir el estado confirmado.

---

# TS-037 — Concurrencia válida

## Given

```text
PersistedVersion = 5

ExpectedVersion = 5
```

## When

una modificación válida es persistida.

## Then

puede confirmarse:

```text
Version = 6
```

junto con el estado resultante válido.

---

# TS-038 — Repository no modifica Estado

## Given

una Notification válida.

## When

el Repository la persiste.

## Then

el Repository no debe:

- cambiar NotificationStatus;
- ejecutar transiciones;
- modificar NotificationId;
- inventar Domain Events.

---

# TS-039 — Repository no corrige Invariants

## Given

una operación que produciría un estado inválido.

## When

se intenta persistir.

## Then

el Repository no debe corregir el estado.

La operación debe haber sido rechazada por el dominio antes de
confirmar persistencia.

---

# TS-040 — PersistenceFailure no significa Failed

## Given

una operación de persistencia.

## When

ocurre:

```text
PersistenceFailure
```

## Then

no debe inferirse:

```text
NotificationStatus = Failed
```

Debe mantenerse:

```text
PersistenceFailure

≠

NotificationDeliveryFailed
```

---

# TS-041 — Authorization válida no evita Invariants

## Given

```text
Actor = Authorized

NotificationStatus = Draft
```

## When

el actor solicita:

```text
ConfirmNotificationDelivery
```

## Then

la operación debe resultar:

```text
Rejected
```

porque la transición es inválida.

Debe mantenerse:

```text
Authorized

≠

Automatically Valid
```

---

# TS-042 — Command no autorizado no alcanza el Aggregate

## Given

un actor o proceso sin autorización para un Command.

## When

intenta solicitar la operación.

## Then

la Application Layer debe rechazar la intención antes de ejecutar
comportamiento de Notification.

Notification no realiza Authentication.

---

# TS-043 — Permission no permite modificar Estado directamente

## Given

un actor autorizado.

## When

intenta modificar:

```text
NotificationStatus
```

directamente.

## Then

la operación debe permanecer prohibida.

---

# TS-044 — Referencia externa no incorpora Aggregate completo

## Given

una Notification relacionada con un Aggregate externo.

## When

se representa dicha relación.

## Then

debe utilizarse:

```text
AggregateId
```

o contrato explícito.

No debe incorporarse el Aggregate externo completo dentro del
Consistency Boundary.

---

# TS-045 — Citizen permanece fuera del Boundary

## Given

una Notification destinada a un actor representado por Citizen.

## When

Notification evoluciona en su Lifecycle.

## Then

no debe modificarse directamente:

```text
Citizen
```

ni su Lifecycle.

---

# TS-046 — Assembly permanece fuera del Boundary

## Given

un hecho confirmado de Assembly origina una necesidad de
Notification.

## When

se crea la Notification.

## Then

deben existir dos límites independientes:

```text
Assembly Consistency Boundary

Notification Consistency Boundary
```

Notification no modifica directamente Assembly.

---

# TS-047 — Fallo de Notification no revierte Assembly

## Given

un hecho de Assembly ya confirmado.

## When

la Notification asociada evoluciona:

```text
Pending → Failed
```

## Then

el hecho de Assembly debe permanecer confirmado.

Debe mantenerse:

```text
Notification Failed

≠

Assembly Rollback
```

---

# TS-048 — Document permanece fuera del Boundary

## Given

una Notification relacionada con:

```text
DocumentId
```

## When

Notification cambia de estado.

## Then

no debe modificarse:

```text
DocumentStatus

Document.Version

Document Lifecycle
```

---

# TS-049 — Canal no equivale a Provider

## Given

una Notification con un concepto de canal válido.

## When

se selecciona una implementación técnica para ejecutar la entrega.

## Then

debe mantenerse:

```text
Notification Channel

≠

Infrastructure Provider
```

El proveedor no forma parte del Aggregate.

---

# TS-050 — Provider no modifica NotificationStatus directamente

## Given

una Notification Pending.

## When

un proveedor técnico informa un resultado.

## Then

dicho resultado debe ingresar al dominio mediante:

```text
ConfirmNotificationDelivery
```

o:

```text
ReportNotificationDeliveryFailure
```

según corresponda.

Nunca mediante modificación directa de:

```text
NotificationStatus
```

---

# TS-051 — Retry técnico no equivale a RetryNotification

## Given

un mecanismo de publicación o entrega técnica realiza un nuevo
intento.

## When

no existe transición de dominio confirmada.

## Then

no debe inferirse:

```text
NotificationRetried
```

Debe mantenerse:

```text
Technical Retry

≠

RetryNotification
```

---

# TS-052 — Domain Event no implica Integration Event

## Given

ocurre:

```text
NotificationDelivered
```

## When

no existe contrato explícito de integración para comunicar ese
hecho.

## Then

no existe obligación de publicar:

```text
NotificationDeliveredIntegrationEvent
```

Debe mantenerse:

```text
Domain Event

≠

Mandatory Integration Event
```

---

# TS-053 — Integration Event solamente después del Commit

## Given

una modificación válida que puede originar un Integration Event.

## When

el Aggregate todavía no ha sido confirmado.

## Then

el Integration Event no debe publicarse.

Solamente después de:

```text
Confirmed Commit
```

puede ocurrir la publicación correspondiente.

---

# TS-054 — Publicación de Integration Event no incrementa Version

## Given

```text
Notification.Version = N
```

## When

se publica un Integration Event correspondiente a un hecho ya
confirmado.

## Then

debe permanecer:

```text
Notification.Version = N
```

---

# TS-055 — Reintento de publicación no incrementa Version

## Given

un Integration Event ya generado.

## When

Infrastructure realiza múltiples intentos de publicación.

## Then

ninguno de esos intentos incrementa:

```text
Notification.Version
```

---

# TS-056 — Integration Event duplicado

## Given

un Integration Event con:

```text
EventId = E-001
```

## When

un consumidor recibe el mismo EventId más de una vez.

## Then

el procesamiento debe poder tratarlo idempotentemente.

Una recepción duplicada no representa un nuevo hecho del
Aggregate.

---

# TS-057 — Read Model después de NotificationCreated

## Given

ocurre:

```text
NotificationCreated
AggregateVersion = 1
```

## When

la proyección procesa el evento.

## Then

puede representar:

```text
NotificationStatus = Draft

Version = 1
```

---

# TS-058 — Read Model después de NotificationQueued

## Given

un Read Model proyectado en:

```text
Draft
```

## When

procesa:

```text
NotificationQueued
```

## Then

debe representar:

```text
Pending
```

con la AggregateVersion correspondiente.

---

# TS-059 — Read Model después de NotificationDeliveryFailed

## Given

un Read Model proyectado en:

```text
Pending
```

## When

procesa:

```text
NotificationDeliveryFailed
```

## Then

debe representar:

```text
Failed
```

---

# TS-060 — Read Model después de NotificationRetried

## Given

un Read Model proyectado en:

```text
Failed
```

## When

procesa:

```text
NotificationRetried
```

## Then

debe representar:

```text
Pending
```

sin crear una nueva identidad.

---

# TS-061 — Read Model después de NotificationDelivered

## Given

un Read Model proyectado en:

```text
Pending
```

## When

procesa:

```text
NotificationDelivered
```

## Then

debe representar:

```text
Delivered
```

sin modificar el Write Model.

---

# TS-062 — Read Model puede estar desactualizado

## Given

```text
Notification.Version = N

ReadModel.Version = N - 1
```

## When

existe una ventana de propagación.

## Then

la diferencia puede ser válida temporalmente.

Esto representa:

```text
Eventual Consistency
```

y no corrupción del Aggregate.

---

# TS-063 — Read Model no ejecuta Commands

## Given

una proyección de Notification.

## When

se actualiza a partir de un Domain Event.

## Then

no debe ejecutarse nuevamente el Command que originó el hecho.

---

# TS-064 — Read Model no incrementa Aggregate Version

## Given

```text
Notification.Version = N
```

## When

una proyección es creada, actualizada o reconstruida.

## Then

debe mantenerse:

```text
Notification.Version = N
```

---

# TS-065 — Rebuild no modifica Notification

## Given

existe un conjunto de Domain Events disponibles.

## When

se reconstruye el Read Model.

## Then

no debe:

- ejecutar Commands;
- modificar NotificationStatus;
- incrementar Notification.Version;
- producir nuevos Domain Events.

---

# TS-066 — Read Model no reemplaza Audit

## Given

una proyección contiene información de trazabilidad.

## When

se consulta esa información.

## Then

no debe considerarse:

```text
Audit Record
```

por el solo hecho de estar presente en el Read Model.

---

# TS-067 — Domain Event no es Audit Record

## Given

ocurre:

```text
NotificationDelivered
```

## When

Audit procesa el hecho.

## Then

el posible Audit Record resultante debe permanecer conceptualmente
distinto del Domain Event.

---

# TS-068 — Audit no modifica Notification

## Given

existe una Notification confirmada.

## When

Audit registra información derivada de sus hechos.

## Then

no debe modificarse:

```text
NotificationStatus

Notification.Version
```

---

# TS-069 — Event Sourcing reconstruye flujo exitoso

## Given

```text
NotificationCreated

NotificationQueued

NotificationDelivered
```

## When

se reconstruye el Aggregate en orden lógico.

## Then

debe resultar:

```text
NotificationStatus = Delivered

Version = 3
```

---

# TS-070 — Event Sourcing reconstruye flujo con Retry

## Given

```text
NotificationCreated

NotificationQueued

NotificationDeliveryFailed

NotificationRetried

NotificationDelivered
```

## When

se reconstruye el Aggregate.

## Then

debe resultar:

```text
NotificationStatus = Delivered

Version = 5
```

preservando todos los hechos históricos.

---

# TS-071 — Reproducción histórica no genera nuevos Eventos

## Given

una secuencia histórica válida.

## When

se rehidrata Notification mediante replay.

## Then

no deben generarse nuevos:

```text
NotificationCreated

NotificationQueued

NotificationDelivered

NotificationDeliveryFailed

NotificationRetried
```

como consecuencia del replay.

---

# TS-072 — Consistency Boundary permanece pequeño

## Given

una Notification relacionada con múltiples contextos.

## When

se carga el Aggregate.

## Then

no debe ser necesario cargar como parte de su estado interno:

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

---

# TS-073 — Modificación válida es Atómica

## Given

una Notification en estado válido.

## When

una operación válida modifica el Aggregate.

## Then

deben confirmarse coherentemente:

```text
State

Version

UpdatedAt

Domain Event
```

sin estado parcial confirmado.

---

# TS-074 — Fallo durante modificación no confirma estado parcial

## Given

una operación que no puede completarse.

## When

la modificación falla antes del commit.

## Then

no debe existir un estado confirmado donde:

```text
New Status

+

Old Version
```

o cualquier otra combinación parcial sea considerada válida.

---

# TS-075 — CreatedAt permanece Inmutable

## Given

una Notification creada con:

```text
CreatedAt = T1
```

## When

ocurren múltiples modificaciones válidas.

## Then

debe permanecer:

```text
CreatedAt = T1
```

---

# TS-076 — UpdatedAt cambia con modificación válida

## Given

```text
UpdatedAt = T1
```

## When

una modificación válida es confirmada en:

```text
T2
```

## Then

puede establecerse:

```text
UpdatedAt = T2
```

conforme a las reglas temporales del Aggregate.

---

# TS-077 — UpdatedAt no cambia con operación rechazada

## Given

```text
UpdatedAt = T1
```

## When

un Command es rechazado.

## Then

debe permanecer:

```text
UpdatedAt = T1
```

---

# TS-078 — Estado desconocido es inválido

## Given

una Notification.

## When

se intenta establecer:

```text
NotificationStatus = Unknown
```

## Then

el estado debe ser rechazado.

Los únicos estados oficiales son:

```text
Draft

Pending

Delivered

Failed
```

---

# TS-079 — No Command técnico de envío

## Given

el Aggregate Notification.

## When

se intenta expresar una intención mediante:

```text
SendEmail

SendSMS

SendPushNotification
```

## Then

esos nombres no deben considerarse Commands oficiales de
Notification versión 1.0.

Debe mantenerse:

```text
Domain Command

≠

Infrastructure Operation
```

---

# TS-080 — Integración con FIWARE no cambia el Aggregate

## Given

un Integration Event de Notification es consumido por FIWARE.

## When

FIWARE procesa el mensaje.

## Then

no debe modificarse directamente:

```text
NotificationStatus

Notification.Version
```

La integración permanece fuera del Consistency Boundary.

---

# Matriz de Transiciones a Probar

Deben considerarse como válidas:

| Estado origen | Command | Estado destino |
|---|---|---|
| No Notification | CreateNotification | Draft |
| Draft | QueueNotification | Pending |
| Pending | ConfirmNotificationDelivery | Delivered |
| Pending | ReportNotificationDeliveryFailure | Failed |
| Failed | RetryNotification | Pending |

Deben considerarse inválidas todas las demás combinaciones de los
Commands oficiales con estados incompatibles.

---

# Matriz de Eventos Esperados

| Command válido | Domain Event esperado |
|---|---|
| CreateNotification | NotificationCreated |
| QueueNotification | NotificationQueued |
| ConfirmNotificationDelivery | NotificationDelivered |
| ReportNotificationDeliveryFailure | NotificationDeliveryFailed |
| RetryNotification | NotificationRetried |

Una operación rechazada produce:

```text
No Success Domain Event
```

---

# Matriz de Versioning

| Situación | Resultado sobre Version |
|---|---|
| Creación válida | Version = 1 |
| Modificación válida | Version + 1 |
| Command rechazado | Sin cambio |
| Consulta | Sin cambio |
| Rehidratación | Sin cambio |
| Read Model Projection | Sin cambio |
| Integration Event Publication | Sin cambio |
| Audit Processing | Sin cambio |
| RetryNotification válido | Version + 1 |
| Retry técnico de Infrastructure | Sin cambio |

---

# Cobertura Conceptual

La batería de escenarios debe cubrir al menos:

```text
Identity

Lifecycle

State Machine

Commands

Domain Events

Invariants

Permissions

Repository

Versioning

Consistency Boundary

Integration Events

Read Models

Event Sourcing Compatibility

CQRS Compatibility

Concurrency

Failure Paths

Retry Paths
```

---

# Criterios de Aceptación

El Aggregate cumple sus Test Scenarios cuando:

- todas las transiciones válidas producen el estado esperado;
- todas las transiciones inválidas son rechazadas;
- los Commands producen únicamente sus hechos correspondientes;
- ninguna operación rechazada produce Domain Event de éxito;
- Version evoluciona únicamente con modificaciones válidas;
- NotificationId permanece inmutable;
- Delivered permanece terminal;
- Failed solamente reingresa mediante RetryNotification;
- Retry preserva identidad e historia;
- CreatedAt permanece inmutable;
- UpdatedAt cambia únicamente con modificaciones válidas;
- Repository no ejecuta comportamiento de dominio;
- Optimistic Concurrency rechaza escrituras obsoletas;
- Permissions no permiten evitar las Invariants;
- Aggregates externos permanecen fuera del Consistency Boundary;
- los proveedores técnicos no modifican el estado directamente;
- Domain Events e Integration Events permanecen separados;
- Integration Events se publican únicamente después del commit;
- los Read Models permanecen como proyecciones;
- Audit permanece separado;
- CQRS mantiene separación entre escritura y lectura;
- Event Sourcing puede reconstruir un estado consistente.

---

# Definición de Éxito

Los Test Scenarios del Aggregate **Notification** establecen una
batería conceptual de validación capaz de comprobar que todas las
reglas oficiales del dominio permanecen coherentes.

Los escenarios verifican:

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

junto con los Commands:

```text
CreateNotification

QueueNotification

ConfirmNotificationDelivery

ReportNotificationDeliveryFailure

RetryNotification
```

y los Domain Events:

```text
NotificationCreated

NotificationQueued

NotificationDelivered

NotificationDeliveryFailed

NotificationRetried
```

La cobertura garantiza que:

- el Aggregate solamente acepta estados válidos;
- las transiciones siguen la State Machine;
- Delivered es terminal;
- Failed permite Retry;
- los Commands inválidos son rechazados;
- los Domain Events representan únicamente hechos consumados;
- Version protege la evolución lógica;
- Optimistic Concurrency protege escrituras concurrentes;
- las Invariants permanecen verdaderas;
- las Permissions no sustituyen las reglas del dominio;
- Repository permanece separado del comportamiento;
- Consistency Boundary permanece limitado a Notification;
- otros Aggregates no son modificados directamente;
- Integration Events permanecen desacoplados;
- Read Models no poseen autoridad de escritura;
- Audit permanece fuera del Aggregate;
- CQRS y Event Sourcing permanecen compatibles;
- Infrastructure no determina las reglas conceptuales del dominio.

De esta forma, `DOMAIN-011M-Test-Scenarios.md` establece los
escenarios oficiales de validación conceptual del Aggregate
**Notification** conforme al patrón consolidado de AURA Core.