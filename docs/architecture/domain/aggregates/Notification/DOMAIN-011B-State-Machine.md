# DOMAIN-011B — Notification State Machine

Versión: 1.0

Estado: Official

Proyecto: AURA Core

Bounded Context: Notification Management

Aggregate: Notification

Documentos relacionados:

- DOMAIN-011-Aggregate.md
- DOMAIN-011A-Lifecycle.md
- DOMAIN-011C-Commands.md
- DOMAIN-011D-Domain-Events.md
- DOMAIN-011E-Invariants.md
- DOMAIN-011I-Versioning.md
- DOMAIN-011J-Consistency-Boundary.md

## Objetivo

Formalizar la máquina de estados ya definida por el Lifecycle, Commands,
Invariants y Domain Events de Notification versión 1.0.

## Estados oficiales

```text
Draft
Pending
Delivered
Failed
```

No existen `Archived`, `Cancelled`, `Read`, `Opened`, `Scheduled` ni
estados dependientes de proveedores en esta versión.

## Máquina oficial

```text
None
  │ CreateNotification / NotificationCreated
  ▼
Draft
  │ QueueNotification / NotificationQueued
  ▼
Pending ── ConfirmNotificationDelivery / NotificationDelivered ──► Delivered
  │
  └── ReportNotificationDeliveryFailure
          / NotificationDeliveryFailed
          ▼
        Failed
          │ RetryNotification / NotificationRetried
          └──────────────────────────────────────────────────────► Pending
```

## Tabla de transiciones

| Origen | Command | Destino | Domain Event |
|---|---|---|---|
| inexistente | CreateNotification | Draft | NotificationCreated |
| Draft | QueueNotification | Pending | NotificationQueued |
| Pending | ConfirmNotificationDelivery | Delivered | NotificationDelivered |
| Pending | ReportNotificationDeliveryFailure | Failed | NotificationDeliveryFailed |
| Failed | RetryNotification | Pending | NotificationRetried |

## Guards

- Create requiere un NotificationId nuevo y datos que satisfagan las
  Invariants.
- Queue requiere Draft.
- Confirm delivery y report failure requieren Pending.
- Retry requiere Failed.
- Delivered es terminal.
- Failed sólo puede regresar a Pending mediante RetryNotification.

## Rechazos

Una transición no incluida en la tabla se rechaza. El rechazo:

- conserva NotificationStatus;
- conserva AggregateVersion;
- no genera Domain Events de éxito;
- no ejecuta entrega técnica ni modifica el Aggregate origen.

## Consistencia y adapters

La máquina gobierna únicamente Notification. Confirmaciones o fallos de un
proveedor ingresan por un inbound adapter, Application los traduce al
Command correspondiente y el Aggregate decide la transición.

Notification no consume Domain Events de otros Bounded Contexts. La
creación originada por otro contexto requiere un Integration Event o API
Contract explícito que Application traduzca a CreateNotification.

## Versioning

Cada transición confirmada incrementa AggregateVersion exactamente una
vez. Publicación, entrega técnica, actualización de Read Models y reintento
del adapter no modifican la versión por sí mismos.

## Definición de éxito

Toda Notification ocupa exactamente un estado oficial y sólo cambia por
un Command válido de la tabla, preservando invariantes, versionado y su
frontera de consistencia.
