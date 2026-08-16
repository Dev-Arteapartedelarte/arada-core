# DOMAIN-001E — Organization Invariants

Versión: 2.0

Estado: Official

Proyecto: AURA Core

Bounded Context: Organization Management

Aggregate: Organization

## Invariantes oficiales

1. OrganizationId es obligatorio, único, inmutable y no reutilizable.
2. OrganizationName, OrganizationType y OrganizationStatus son válidos.
3. OrganizationSettings y OrganizationPolicies siempre existen.
4. TerritoryId es obligatorio cuando OrganizationType lo requiere.
5. Sólo se permiten las transiciones de DOMAIN-001B.
6. AggregateVersion aumenta una vez por modificación válida.
7. Una operación rechazada conserva estado, versión y eventos pendientes.
8. Las referencias externas son IDs; nunca objetos de otro Aggregate.
9. Organization no posee Memberships, Roles ni Representatives.
10. Los Domain Events describen únicamente cambios confirmados propios.

Las reglas que requieren validar el estado actual de otro Aggregate se
orquestan en Application y no amplían esta frontera de consistencia.
