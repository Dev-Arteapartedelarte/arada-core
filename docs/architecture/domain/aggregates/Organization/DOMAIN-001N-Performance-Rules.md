# DOMAIN-001N — Organization Performance Rules

Versión: 2.0

Estado: Official

Proyecto: AURA Core

Bounded Context: Organization Management

Aggregate: Organization

## Reglas

- cargar una Organization no carga otros Aggregates ni Read Models;
- los Commands operan sobre tamaño acotado por la Organization;
- listados y filtros pertenecen a Read Models;
- la concurrencia se protege con AggregateVersion;
- publicación e integraciones ocurren después del commit;
- cachés e índices son detalles de outbound adapters;
- no se amplía la transacción para optimizar procesos cross-context.

Ninguna regla de rendimiento puede debilitar invariantes, ownership o
consistencia.
