# DOMAIN-001B — Organization State Machine

Versión: 2.0

Estado: Official

Proyecto: AURA Core

Bounded Context: Organization Management

Aggregate: Organization

## Máquina oficial

```text
                       Reject
                ┌─────────────────┐
                ▼                 │
None -> Draft -> PendingValidation -> Active -> Suspended
         │                           │  ▲         │
         │                           │  └─────────┘
         │                           ▼
         └------> Deleted         Archived -> Deleted
                                     ▲
                                     └── Suspended
```

## Guards

- Submit requiere Draft y datos obligatorios válidos.
- Approve y Reject requieren PendingValidation.
- Suspend requiere Active.
- Reactivate requiere Suspended.
- Archive requiere Active o Suspended.
- Delete requiere Draft o Archived.

No existe transición implícita por eventos externos, persistencia,
autorización, lectura o adapters. Sólo la Aggregate Root cambia el estado.
