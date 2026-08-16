# DOMAIN-001P — Organization Extension Points

Versión: 2.0

Estado: Official

Proyecto: AURA Core

Bounded Context: Organization Management

Aggregate: Organization

## Extensiones permitidas

- nuevos OrganizationType mediante política explícita;
- nuevas reglas de validación propias;
- nuevos campos de Address, Brand, Settings o Policies como Value Objects;
- nuevos Integration Events y Read Models versionados;
- nuevos adapters municipales, FIWARE o NGSI-LD protegidos por ACL.

## Restricciones

Una extensión no puede:

- incorporar Membership, Role, Citizen o Representative al boundary;
- crear referencias directas a otros Aggregates;
- introducir una transacción distribuida;
- convertir Domain Events en contratos públicos automáticamente;
- hacer obligatorios CQRS físico o Event Sourcing;
- introducir frameworks o modelos externos en Domain.

Una capacidad con identidad, lifecycle o consistencia propios requiere una
decisión de Bounded Context, no una ampliación implícita de Organization.
