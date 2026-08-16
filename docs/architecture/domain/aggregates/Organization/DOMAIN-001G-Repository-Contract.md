# DOMAIN-001G — Organization Repository Contract

Versión: 2.0

Estado: Official

Proyecto: AURA Core

Bounded Context: Organization Management

Aggregate: Organization

## Puerto

`OrganizationRepository` es un output port del núcleo.

```text
findById(OrganizationId) -> Organization | NotFound
exists(OrganizationId) -> bool
save(Organization, ExpectedAggregateVersion) -> SavedVersion
```

## Reglas

- persiste y recupera el Aggregate completo;
- aplica concurrencia optimista;
- no ejecuta Commands ni decide Permissions;
- no publica Domain o Integration Events;
- no carga Membership, Role u otros Aggregates;
- no expone SQL, ORM, sesiones ni transacciones técnicas al dominio.

Deleted es estado lógico; no se define eliminación física en el contrato
1.0. La implementación pertenece a un outbound adapter.
