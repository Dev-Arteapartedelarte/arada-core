# DOMAIN-001C — Organization Commands

Versión: 2.0

Estado: Official

Proyecto: AURA Core

Bounded Context: Organization Management

Aggregate: Organization

## Catálogo oficial

| Command | Propósito | Estado permitido |
|---|---|---|
| CreateOrganization | crear identidad y estado inicial | inexistente |
| SubmitOrganizationForValidation | solicitar validación | Draft |
| ApproveOrganization | aprobar | PendingValidation |
| RejectOrganization | devolver a edición | PendingValidation |
| SuspendOrganization | suspender operación | Active |
| ReactivateOrganization | reactivar | Suspended |
| ArchiveOrganization | cerrar operación | Active, Suspended |
| DeleteOrganization | eliminar lógicamente | Draft, Archived |
| RenameOrganization | cambiar nombre | Draft, Active, Suspended |
| ChangeOrganizationAddress | cambiar dirección | Draft, Active, Suspended |
| ChangeOrganizationPolicies | cambiar políticas | Draft, Active, Suspended |
| ChangeOrganizationSettings | cambiar configuración | Draft, Active, Suspended |
| ChangeOrganizationBrand | cambiar marca | Draft, Active, Suspended |
| ChangeTerritory | cambiar TerritoryId | Draft, Active, Suspended |

## Reglas

Todo Command identifica una Organization y la AggregateVersion esperada,
salvo creación. La autorización se evalúa en Application mediante la
Permission explícita. Un Command rechazado no cambia estado ni genera un
evento de éxito.

No son Commands de Organization: `RegisterMember`, `RemoveMember`,
`AssignRepresentative` ni cualquier operación de otro Aggregate.
