# DOMAIN-011E — Notification Invariants

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
- CORE-006-Domain-Invariants.md

---

# Objetivo

Este documento define las Invariants oficiales del Aggregate
**Notification**.

Las Invariants representan condiciones que deben mantenerse
verdaderas antes y después de toda operación válida sobre el
Aggregate.

Ningún Command, transición de estado, mecanismo de persistencia,
integración o decisión de Infrastructure puede violarlas.

---

# Principio Fundamental

El Aggregate Notification solamente puede existir en un estado
válido.

Toda operación debe cumplir:

```text
Valid State Before Operation

          │
          ▼

     Domain Operation

          │
          ▼

Valid State After Operation
```

Si una operación no puede preservar las Invariants:

```text
Operation

    │
    ▼

Rejected
```

El estado confirmado debe permanecer sin modificaciones.

---

# Alcance

Las Invariants protegen exclusivamente el Consistency Boundary de:

```text
Notification
```

No establecen reglas internas para:

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

Cada uno mantiene sus propias Invariants.

---

# INV-001 — NotificationId Obligatorio

Toda Notification debe poseer:

```text
NotificationId
```

válido.

No puede existir una Notification sin identidad.

Debe mantenerse:

```text
NotificationId != null
```

---

# INV-002 — NotificationId Inmutable

Una vez creada la Notification:

```text
NotificationId
```

no puede cambiar.

Debe cumplirse:

```text
NotificationId at Creation

=

NotificationId for Entire Lifecycle
```

Ningún Command puede sustituir la identidad del Aggregate.

---

# INV-003 — Estado Válido

NotificationStatus debe pertenecer exclusivamente al conjunto
oficial:

```text
Draft

Pending

Delivered

Failed
```

Ningún otro estado forma parte del Lifecycle versión 1.0.

---

# INV-004 — Estado Inicial

Toda Notification nueva debe comenzar en:

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
No Notification

↓

CreateNotification

↓

Draft
```

---

# INV-005 — Transiciones Oficiales

Toda transición de NotificationStatus debe pertenecer
exclusivamente al conjunto:

```text
No Notification → Draft

Draft → Pending

Pending → Delivered

Pending → Failed

Failed → Pending
```

Ninguna otra transición es válida en la versión 1.0.

---

# INV-006 — Draft solamente puede avanzar a Pending

Una Notification en:

```text
Draft
```

únicamente puede cambiar su estado hacia:

```text
Pending
```

mediante el comportamiento definido para:

```text
QueueNotification
```

Por lo tanto están prohibidas:

```text
Draft → Delivered

Draft → Failed
```

---

# INV-007 — Pending solamente puede producir un Resultado de Entrega

Una Notification en:

```text
Pending
```

puede evolucionar únicamente hacia:

```text
Delivered
```

o:

```text
Failed
```

según el resultado confirmado de la entrega.

Debe mantenerse:

```text
Pending → Delivered
```

mediante:

```text
ConfirmNotificationDelivery
```

o:

```text
Pending → Failed
```

mediante:

```text
ReportNotificationDeliveryFailure
```

---

# INV-008 — Delivered es Terminal

Una Notification en:

```text
Delivered
```

no puede volver al ciclo operativo ordinario.

Están prohibidas:

```text
Delivered → Draft

Delivered → Pending

Delivered → Failed
```

Una Notification Delivered no puede ser reintentada.

---

# INV-009 — Failed solamente puede volver a Pending

Una Notification en:

```text
Failed
```

solamente puede reingresar al proceso mediante:

```text
RetryNotification
```

produciendo:

```text
Failed → Pending
```

Están prohibidas:

```text
Failed → Draft

Failed → Delivered
```

---

# INV-010 — No Modificación Directa del Estado

NotificationStatus no puede modificarse directamente.

Todo cambio debe producirse mediante comportamiento de la
Aggregate Root.

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

Direct NotificationStatus Mutation
```

---

# INV-011 — Toda Modificación atraviesa la Aggregate Root

Ningún elemento interno de Notification puede ser modificado
directamente desde fuera del Aggregate.

Toda modificación debe ser coordinada por:

```text
Notification
```

como única Aggregate Root.

---

# INV-012 — Commands Oficiales

La versión 1.0 reconoce exclusivamente:

```text
CreateNotification

QueueNotification

ConfirmNotificationDelivery

ReportNotificationDeliveryFailure

RetryNotification
```

No pueden inferirse Commands adicionales a partir de:

- proveedores;
- canales técnicos;
- APIs;
- Infrastructure;
- Read Models;
- Integration Events.

---

# INV-013 — Correspondencia Command → Transición

Cada Command de Lifecycle posee una transición específica:

```text
CreateNotification
    No Notification → Draft

QueueNotification
    Draft → Pending

ConfirmNotificationDelivery
    Pending → Delivered

ReportNotificationDeliveryFailure
    Pending → Failed

RetryNotification
    Failed → Pending
```

Un Command ejecutado desde un estado incompatible debe ser
rechazado.

---

# INV-014 — Correspondencia Command → Domain Event

Toda operación válida de Lifecycle produce el hecho
correspondiente:

```text
CreateNotification
    → NotificationCreated

QueueNotification
    → NotificationQueued

ConfirmNotificationDelivery
    → NotificationDelivered

ReportNotificationDeliveryFailure
    → NotificationDeliveryFailed

RetryNotification
    → NotificationRetried
```

Ningún Domain Event de éxito puede existir cuando la operación
fue rechazada.

---

# INV-015 — Domain Events representan Hechos Consumados

Los Domain Events oficiales:

```text
NotificationCreated

NotificationQueued

NotificationDelivered

NotificationDeliveryFailed

NotificationRetried
```

representan hechos ya ocurridos.

No pueden utilizarse como Commands ni como solicitudes de
modificación futura.

Debe mantenerse:

```text
Domain Event

=

Fact
```

y:

```text
Command

=

Intent
```

---

# INV-016 — Operación Rechazada no Modifica Estado

Cuando una operación es rechazada:

- NotificationStatus permanece igual;
- el estado interno confirmado permanece igual;
- no existe modificación parcial.

Debe mantenerse:

```text
Invalid Operation

↓

Rejected

↓

Confirmed State Preserved
```

---

# INV-017 — Operación Rechazada no Incrementa Version

Una operación rechazada conserva:

```text
Version
```

sin modificaciones.

Debe cumplirse:

```text
Version before rejected operation

=

Version after rejected operation
```

---

# INV-018 — Operación Rechazada no genera Domain Event de Éxito

Ninguna operación rechazada puede producir:

```text
NotificationCreated

NotificationQueued

NotificationDelivered

NotificationDeliveryFailed

NotificationRetried
```

como resultado exitoso de esa operación.

---

# INV-019 — Toda Modificación Válida Incrementa Version

Toda modificación válida del Aggregate incrementa:

```text
Version
```

Conceptualmente:

```text
Notification vN

↓

Valid Modification

↓

Notification vN+1
```

No existen modificaciones válidas del Aggregate que mantengan la
misma Version.

---

# INV-020 — AggregateVersion coherente con Domain Event

Cuando una modificación válida produce un Domain Event:

```text
AggregateVersion
```

del evento debe corresponder a la Version resultante del
Aggregate.

Debe mantenerse:

```text
DomainEvent.AggregateVersion

=

Notification.Version after valid modification
```

---

# INV-021 — CreatedAt Inmutable

Toda Notification posee:

```text
CreatedAt
```

establecido al momento de su creación.

Una vez definido:

```text
CreatedAt
```

permanece inmutable durante todo el Lifecycle.

---

# INV-022 — UpdatedAt solamente cambia con Modificación Válida

`UpdatedAt` representa el momento de la última modificación válida
del Aggregate.

Debe actualizarse únicamente cuando una operación es aceptada.

Una operación rechazada no modifica:

```text
UpdatedAt
```

UpdatedAt no reemplaza Version.

Debe mantenerse:

```text
UpdatedAt

≠

Version
```

---

# INV-023 — Delivered no implica Read

El estado:

```text
Delivered
```

representa exclusivamente una entrega confirmada.

No implica:

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

La versión 1.0 no incorpora estado de lectura.

---

# INV-024 — Failed no implica Eliminación

Una Notification en:

```text
Failed
```

conserva:

- NotificationId;
- estado;
- Version;
- trazabilidad;
- historial de Domain Events.

Debe mantenerse:

```text
Failed

≠

Deleted
```

Un fallo no elimina el Aggregate.

---

# INV-025 — Retry conserva Identidad

`RetryNotification` opera sobre la misma Notification.

Debe mantenerse:

```text
NotificationId before Retry

=

NotificationId after Retry
```

El reintento no crea un nuevo Aggregate.

---

# INV-026 — Retry conserva Historia

Cuando ocurre:

```text
NotificationDeliveryFailed
```

y posteriormente:

```text
NotificationRetried
```

el evento de fallo anterior permanece como hecho histórico.

No puede:

- eliminarse;
- reemplazarse;
- modificarse;
- reinterpretarse retroactivamente.

---

# INV-027 — Retry no produce Delivered directamente

`RetryNotification` solamente puede producir:

```text
Failed → Pending
```

No puede producir:

```text
Failed → Delivered
```

Después de un reintento debe existir un nuevo resultado explícito
de entrega.

---

# INV-028 — Notification no modifica el Aggregate de Origen

Notification nunca modifica directamente el Aggregate que originó
la necesidad de comunicación.

Debe mantenerse:

```text
Notification Lifecycle

≠

Source Aggregate Lifecycle
```

Un cambio en Notification no implica automáticamente un cambio en:

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
```

---

# INV-029 — Fallo de Notification no revierte el Hecho Originador

Si el Aggregate de origen ya confirmó un hecho y posteriormente la
Notification falla:

```text
Source Domain Fact

↓

NotificationDeliveryFailed
```

el hecho original permanece confirmado.

Debe mantenerse:

```text
Notification Failed

≠

Source Aggregate Rollback
```

---

# INV-030 — Referencias Externas por Identidad o Contrato

Toda relación con otro Aggregate debe utilizar:

```text
AggregateId
```

o un contrato explícito.

Notification no almacena instancias completas de otros
Aggregates.

Debe mantenerse:

```text
External Aggregate Reference

≠

Embedded External Aggregate
```

---

# INV-031 — No Ownership sobre Aggregates Externos

Una relación entre Notification y otro Aggregate no establece
ownership.

Notification no posee:

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

Cada uno conserva su propio Consistency Boundary.

---

# INV-032 — Destinatarios no implican Embedding de Citizen

Cuando una Notification se relacione con destinatarios
representados por identidades externas, no debe incorporar el
Aggregate completo correspondiente.

Debe mantenerse:

```text
Recipient

≠

Embedded Citizen Aggregate
```

La representación concreta del destinatario debe respetar los
contratos oficialmente definidos para Notification.

---

# INV-033 — Canal no es Provider

El canal de Notification representa un concepto de dominio.

No debe confundirse con:

- proveedor externo;
- SDK;
- endpoint;
- protocolo;
- implementación concreta.

Debe mantenerse:

```text
Notification Channel

≠

Infrastructure Provider
```

---

# INV-034 — Entrega de Dominio no es Operación Técnica

La semántica de entrega pertenece a Notification.

La ejecución técnica pertenece a Infrastructure.

Debe mantenerse:

```text
Notification Delivery Domain State

≠

Provider Implementation
```

Un proveedor no puede modificar directamente NotificationStatus.

El resultado técnico debe ingresar al dominio mediante el
comportamiento correspondiente.

---

# INV-035 — No Commands Técnicos

No forman parte de los Commands oficiales:

```text
SendEmail

SendSMS

SendPushNotification

CallProvider

PublishToQueue
```

porque representan mecanismos técnicos y no intenciones oficiales
del Aggregate versión 1.0.

---

# INV-036 — No Cancelled en versión 1.0

El estado:

```text
Cancelled
```

no forma parte de NotificationStatus versión 1.0.

Por lo tanto tampoco existe una transición oficial de
cancelación.

---

# INV-037 — No Archived en versión 1.0

El estado:

```text
Archived
```

no forma parte de NotificationStatus versión 1.0.

La conservación histórica no implica una transición automática a
Archived.

---

# INV-038 — No Deleted como Estado

El Lifecycle versión 1.0 no define:

```text
Deleted
```

como NotificationStatus.

La eliminación física no constituye una transición ordinaria del
Aggregate.

---

# INV-039 — Reintentos sin Política Implícita

El dominio versión 1.0 reconoce:

```text
Failed → Pending
```

mediante RetryNotification.

Sin embargo, no establece implícitamente:

- número máximo de reintentos;
- intervalos;
- backoff;
- ventanas temporales;
- scheduler;
- proveedor.

Estas reglas no pueden inferirse sin evolución explícita del
dominio.

---

# INV-040 — Inmutabilidad de Hechos Históricos

Los Domain Events ya producidos son hechos históricos.

No pueden modificarse para reflejar estados posteriores.

Por ejemplo:

```text
NotificationDeliveryFailed
```

continúa siendo verdadero aunque posteriormente existan:

```text
NotificationRetried

NotificationDelivered
```

---

# INV-041 — Read Models no modifican Notification

Ningún Read Model posee autoridad de escritura sobre el Aggregate.

Una proyección puede representar:

```text
Draft

Pending

Delivered

Failed
```

pero no puede producir transiciones.

Debe mantenerse:

```text
Read Model

≠

Aggregate Authority
```

---

# INV-042 — Integration Events no modifican directamente el Aggregate

Un Integration Event puede comunicar información entre contextos,
pero no obtiene autoridad para modificar internamente Notification.

Toda escritura debe atravesar comportamiento válido del Aggregate.

Debe mantenerse:

```text
Integration Event

≠

Direct State Mutation
```

---

# INV-043 — Domain Event no implica Integration Event

La existencia de:

```text
NotificationCreated

NotificationQueued

NotificationDelivered

NotificationDeliveryFailed

NotificationRetried
```

no implica automáticamente un Integration Event correspondiente.

Debe mantenerse:

```text
Domain Event

≠

Mandatory Integration Event
```

Los Integration Events requieren contratos explícitos.

---

# INV-044 — Notification no administra Audit

Notification puede producir hechos utilizados por Audit.

Sin embargo:

```text
Audit
```

permanece fuera del Aggregate.

Notification no incorpora Audit Records como estado interno.

Debe mantenerse:

```text
Domain Event

≠

Audit Record
```

---

# INV-045 — Consistencia Interna Inmediata

Todas las Invariants internas de Notification deben mantenerse
dentro de una única modificación consistente del Aggregate.

No puede existir un estado confirmado donde solamente una parte de
la modificación haya sido aplicada.

Debe mantenerse:

```text
Notification Modification

=

Atomic Aggregate Modification
```

---

# INV-046 — Consistencia Externa Eventual

Notification no comparte una transacción de dominio distribuida
con otros Aggregates.

La consistencia entre Notification y:

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

es independiente y puede ser eventual.

---

# INV-047 — Invariants antes y después de toda Operación

Toda operación debe garantizar:

```text
Invariants valid before operation

AND

Invariants valid after operation
```

Una operación que no pueda cumplir esta condición debe ser
rechazada completamente.

---

# Matriz de Invariants por Command

## CreateNotification

Debe garantizar:

- NotificationId válido;
- NotificationId nuevo;
- estado inicial Draft;
- CreatedAt establecido;
- estado interno consistente;
- Version coherente;
- NotificationCreated solamente después de creación válida.

---

## QueueNotification

Debe garantizar:

- Aggregate existente;
- NotificationStatus = Draft;
- transición Draft → Pending;
- Version incrementada;
- UpdatedAt actualizado;
- NotificationQueued solamente después de transición válida.

---

## ConfirmNotificationDelivery

Debe garantizar:

- Aggregate existente;
- NotificationStatus = Pending;
- confirmación válida del resultado de entrega;
- transición Pending → Delivered;
- Version incrementada;
- UpdatedAt actualizado;
- NotificationDelivered solamente después de transición válida.

---

## ReportNotificationDeliveryFailure

Debe garantizar:

- Aggregate existente;
- NotificationStatus = Pending;
- resultado fallido válido;
- transición Pending → Failed;
- Version incrementada;
- UpdatedAt actualizado;
- NotificationDeliveryFailed solamente después de transición
  válida.

---

## RetryNotification

Debe garantizar:

- Aggregate existente;
- NotificationStatus = Failed;
- transición Failed → Pending;
- preservación de NotificationId;
- preservación de hechos históricos anteriores;
- Version incrementada;
- UpdatedAt actualizado;
- NotificationRetried solamente después de transición válida.

---

# Protección frente a Estados Imposibles

El Aggregate nunca puede terminar una operación válida en un estado
como:

```text
Notification without NotificationId

NotificationStatus = Unknown

Draft after NotificationDelivered

Delivered after NotificationDeliveryFailed without Retry

Failed after NotificationDelivered

Version decreased

NotificationId changed

Confirmed partial transition
```

Tales estados representan violaciones de Invariants y deben ser
imposibles desde la Aggregate Root.

---

# Persistencia

El Repository debe persistir únicamente estados válidos del
Aggregate.

El Repository:

- no corrige Invariants;
- no inventa transiciones;
- no modifica directamente NotificationStatus;
- no crea Domain Events;
- no ejecuta Commands.

Debe persistir el resultado producido por comportamiento válido de
Notification.

---

# Concurrencia

Las Invariants deben mantenerse también frente a modificaciones
concurrentes.

Notification utiliza:

```text
Optimistic Concurrency Control
```

Si:

```text
PersistedVersion

≠

ExpectedVersion
```

la modificación incompatible debe ser rechazada.

Una escritura obsoleta no puede sobrescribir silenciosamente una
modificación confirmada.

---

# Seguridad

Ninguna decisión de autorización puede evitar las Invariants.

Debe mantenerse:

```text
Authorized

≠

Automatically Valid Domain Operation
```

Un actor autorizado para ejecutar un Command puede recibir rechazo
si:

- el estado es incompatible;
- la transición no existe;
- existe conflicto de Version;
- otra Invariant no se cumple.

---

# Compatibilidad con Event Sourcing

En una implementación basada en Event Sourcing, la reconstrucción
debe producir siempre un estado que cumpla las mismas Invariants.

Una secuencia válida puede ser:

```text
NotificationCreated

↓

NotificationQueued

↓

NotificationDelivered
```

o:

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

Una secuencia histórica inválida no debe producir silenciosamente
un estado considerado válido.

---

# Compatibilidad con CQRS

Las Invariants pertenecen al Write Side.

Los Read Models pueden representar el resultado de los hechos, pero
no son responsables de validar ni imponer las Invariants del
Aggregate.

Debe mantenerse:

```text
Write Model

→ Domain Invariants

Read Model

→ Projection
```

---

# Reglas Fundamentales

Las siguientes reglas constituyen el núcleo de consistencia de
Notification:

1. NotificationId siempre existe.
2. NotificationId nunca cambia.
3. Toda Notification comienza en Draft.
4. NotificationStatus solamente puede ser Draft, Pending,
   Delivered o Failed.
5. Toda transición pertenece a la State Machine.
6. Draft solamente puede evolucionar a Pending.
7. Pending solamente puede evolucionar a Delivered o Failed.
8. Failed solamente puede volver a Pending.
9. Delivered es terminal.
10. Ningún estado cambia directamente.
11. Toda modificación atraviesa la Aggregate Root.
12. Los Commands oficiales son los definidos para la versión 1.0.
13. Cada Command de Lifecycle posee una transición definida.
14. Cada transición válida produce su Domain Event correspondiente.
15. Toda modificación válida incrementa Version.
16. Una operación rechazada conserva el estado confirmado.
17. Una operación rechazada conserva Version.
18. Una operación rechazada no genera Domain Event de éxito.
19. CreatedAt permanece inmutable.
20. UpdatedAt cambia únicamente después de una modificación válida.
21. Delivered no significa Read.
22. Failed no significa Deleted.
23. Retry conserva NotificationId.
24. Retry conserva los hechos históricos anteriores.
25. Retry produce Failed → Pending y nunca Failed → Delivered.
26. Notification no modifica directamente otros Aggregates.
27. El fallo de Notification no revierte el hecho originador.
28. Las referencias externas utilizan identificadores o contratos.
29. Notification no posee Aggregates externos.
30. El canal de dominio no equivale a un proveedor técnico.
31. La entrega de dominio no equivale a la implementación del
    proveedor.
32. No existen Commands técnicos de envío en el Aggregate.
33. Cancelled no existe en la versión 1.0.
34. Archived no existe en la versión 1.0.
35. Deleted no existe como estado.
36. Las políticas de reintento no se infieren.
37. Los hechos históricos son inmutables.
38. Los Read Models no modifican Notification.
39. Los Integration Events no modifican directamente Notification.
40. Domain Event no implica Integration Event.
41. Audit permanece fuera del Aggregate.
42. La consistencia interna es inmediata.
43. La consistencia entre Aggregates es independiente y puede ser
    eventual.
44. Las Invariants deben cumplirse antes y después de toda
    operación.

---

# Definición de Éxito

Las Invariants del Aggregate **Notification** garantizan que toda
unidad de notificación permanezca consistente durante su evolución.

El modelo protege:

```text
NotificationId

Lifecycle

State Machine

Commands

Domain Events

Version

CreatedAt

UpdatedAt

Consistency Boundary
```

y garantiza que:

- toda Notification nace en Draft;
- Draft solamente evoluciona a Pending;
- Pending solamente evoluciona a Delivered o Failed;
- Failed solamente vuelve a Pending mediante RetryNotification;
- Delivered permanece terminal;
- ningún estado puede modificarse directamente;
- toda modificación válida incrementa Version;
- una operación rechazada no altera el estado confirmado;
- una operación rechazada no produce eventos de éxito;
- los reintentos preservan identidad e historia;
- los hechos históricos permanecen inmutables;
- Notification no modifica directamente otros Aggregates;
- el Aggregate originador mantiene Lifecycle independiente;
- la ejecución técnica de entrega permanece separada del dominio;
- los Read Models no poseen autoridad de escritura;
- los Integration Events no sustituyen Domain Events;
- Audit permanece fuera del Aggregate;
- Infrastructure no puede violar las reglas conceptuales del
  dominio.

De esta forma, `DOMAIN-011E-Invariants.md` establece las
condiciones obligatorias que deben permanecer verdaderas durante
toda la vida del Aggregate **Notification** conforme al patrón
consolidado de AURA Core.