# DOMAIN-001F — Organization Permissions

Versión: 2.0

Estado: Official

Proyecto: AURA Core

Bounded Context: Organization Management

Aggregate: Organization

## Modelo

Permission es una capacidad explícita evaluada antes de ejecutar un
Command. Role, Membership y Citizen pueden aportar contexto, pero no
conceden autorización implícita.

## Matriz Command–Permission

| Commands | Permission |
|---|---|
| CreateOrganization | organization.create |
| SubmitOrganizationForValidation | organization.submit |
| ApproveOrganization, RejectOrganization | organization.validate |
| SuspendOrganization, ReactivateOrganization | organization.change-status |
| ArchiveOrganization | organization.archive |
| DeleteOrganization | organization.delete |
| RenameOrganization | organization.rename |
| ChangeOrganizationAddress | organization.change-address |
| ChangeOrganizationPolicies | organization.change-policies |
| ChangeOrganizationSettings | organization.change-settings |
| ChangeOrganizationBrand | organization.change-brand |
| ChangeTerritory | organization.change-territory |

Application verifica autenticación, tenant/OrganizationId y Permission.
El Aggregate vuelve a verificar estado e invariantes, pero no consulta
Identity Providers ni Repositories externos.
