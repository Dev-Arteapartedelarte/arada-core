# DOMAIN-001D — Organization Domain Events

Versión: 2.0

Estado: Official

Proyecto: AURA Core

Bounded Context: Organization Management

Aggregate: Organization

## Eventos oficiales

- OrganizationCreated
- OrganizationSubmittedForValidation
- OrganizationApproved
- OrganizationRejected
- OrganizationSuspended
- OrganizationReactivated
- OrganizationArchived
- OrganizationDeleted
- OrganizationRenamed
- OrganizationAddressChanged
- OrganizationPoliciesChanged
- OrganizationSettingsChanged
- OrganizationBrandChanged
- OrganizationTerritoryChanged

## Contrato interno

Cada evento contiene EventId, OrganizationId, AggregateVersion,
OccurredAt, CorrelationId/CausationId cuando correspondan y el payload
mínimo del hecho.

Organization genera y registra estos hechos dentro de su transacción.
Application coordina su publicación interna después del commit.

Los Domain Events no son contratos públicos ni son consumidos por otros
Bounded Contexts. Todo cruce utiliza un Integration Event definido en
DOMAIN-001K o un API Contract explícito.

No existen `MemberRegistered`, `MemberRemoved` ni
`RepresentativeAssigned` en Organization Management.
