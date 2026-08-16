# DOMAIN-001A — Organization Lifecycle

Versión: 2.0

Estado: Official

Proyecto: AURA Core

Bounded Context: Organization Management

Aggregate: Organization

## Estados oficiales

- `Draft`: estado inicial editable.
- `PendingValidation`: espera una decisión de validación.
- `Active`: organización operativa.
- `Suspended`: operación temporalmente restringida.
- `Archived`: terminal operativo y conservado.
- `Deleted`: terminal lógico para retención.

## Transiciones oficiales

| Origen | Command | Destino | Domain Event |
|---|---|---|---|
| inexistente | CreateOrganization | Draft | OrganizationCreated |
| Draft | SubmitOrganizationForValidation | PendingValidation | OrganizationSubmittedForValidation |
| PendingValidation | ApproveOrganization | Active | OrganizationApproved |
| PendingValidation | RejectOrganization | Draft | OrganizationRejected |
| Active | SuspendOrganization | Suspended | OrganizationSuspended |
| Suspended | ReactivateOrganization | Active | OrganizationReactivated |
| Active, Suspended | ArchiveOrganization | Archived | OrganizationArchived |
| Draft, Archived | DeleteOrganization | Deleted | OrganizationDeleted |

Los Commands descriptivos no cambian OrganizationStatus. Toda transición
rechazada conserva estado, AggregateVersion y eventos pendientes.

Archived y Deleted no regresan al lifecycle operativo. Deleted no implica
eliminación física.
