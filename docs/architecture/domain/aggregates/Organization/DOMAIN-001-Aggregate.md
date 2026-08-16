# DOMAIN-001 — Organization Aggregate

Versión: 2.0

Estado: Official

Proyecto: AURA Core

Bounded Context: Organization Management

Aggregate: Organization

## Objetivo

Organization representa una entidad colectiva y posee exclusivamente su
identidad, lifecycle, configuración, políticas, marca, dirección y
territorio asociado.

## Aggregate Root e identidad

`Organization` es la única Aggregate Root. `OrganizationId` es único,
inmutable y nunca reutilizable.

## Estado

- OrganizationId
- OrganizationName y OrganizationType
- OrganizationStatus
- OrganizationAddress y OrganizationBrand
- OrganizationSettings y OrganizationPolicies
- TerritoryId cuando el tipo lo requiere
- CreatedAt, UpdatedAt y AggregateVersion
- Pending Domain Events

## Lifecycle

```text
Draft -> PendingValidation -> Active -> Suspended -> Active
  ^             |              |           |
  |-------------|              └-----> Archived -> Deleted
  └-- rejection                  Suspended -> Archived
Draft -> Deleted
```

## Commands oficiales

- CreateOrganization
- SubmitOrganizationForValidation
- ApproveOrganization
- RejectOrganization
- SuspendOrganization
- ReactivateOrganization
- ArchiveOrganization
- DeleteOrganization
- RenameOrganization
- ChangeOrganizationAddress
- ChangeOrganizationPolicies
- ChangeOrganizationSettings
- ChangeOrganizationBrand
- ChangeTerritory

## Ownership externo

Organization no administra Citizen, Membership, Role, Representative,
Assembly, Proposal, Participation, Voting, Document, Notification, Audit
ni Integration. Mantiene sólo IDs requeridos por sus propias invariantes.

En particular, no existen `RegisterMember`, `RemoveMember` ni
`AssignRepresentative` en este Aggregate.

## Consistencia

Cada Command modifica una sola Organization y se persiste mediante
OrganizationRepository. La colaboración cross-context utiliza
Integration Events explícitos y consistencia eventual.

## Arquitectura

El Aggregate genera y registra Domain Events internos. Application
coordina persistencia, autorización y publicación posterior al commit.
Infrastructure implementa puertos sin ingresar al modelo.
