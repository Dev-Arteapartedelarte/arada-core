# DOMAIN-001H — Organization Examples

Versión: 2.0

Estado: Official

Proyecto: AURA Core

Bounded Context: Organization Management

Aggregate: Organization

## Creación y validación

```text
CreateOrganization -> Draft -> OrganizationCreated
SubmitOrganizationForValidation -> PendingValidation
ApproveOrganization -> Active -> OrganizationApproved
```

Si la validación es rechazada:

```text
PendingValidation -> RejectOrganization -> Draft
```

## Suspensión y reactivación

```text
Active -> SuspendOrganization -> Suspended
Suspended -> ReactivateOrganization -> Active
```

## Archivo y eliminación lógica

```text
Active|Suspended -> ArchiveOrganization -> Archived
Archived -> DeleteOrganization -> Deleted
```

## Cambio descriptivo

`RenameOrganization` sobre Active conserva el estado, incrementa una vez
AggregateVersion y genera `OrganizationRenamed`.

## Rechazos

- Approve sobre Draft se rechaza sin cambios.
- Reactivate sobre Archived se rechaza.
- ChangeTerritory sin Permission se rechaza en Application.
- save con ExpectedAggregateVersion obsoleta produce conflicto y no
  confirma eventos.

## Límites

Registrar una Membership o asignar un Representative no es un ejemplo de
Organization: requiere el contrato del contexto que posea ese proceso.
