# DOMAIN-001L — Organization Read Model

Versión: 2.0

Estado: Official

Proyecto: AURA Core

Bounded Context: Organization Management

Aggregate: Organization

## Proyecciones propias

- OrganizationSummary
- OrganizationDetail
- OrganizationsByStatus
- OrganizationsByTerritory

Pueden contener OrganizationId, nombre, tipo, estado, TerritoryId,
campos descriptivos y ProjectedAggregateVersion.

Las vistas compuestas con Membership, Role, Citizen u otros contextos son
proyecciones externas eventualmente consistentes. Nunca se usan para
ejecutar Commands ni reparar el Write Model.
