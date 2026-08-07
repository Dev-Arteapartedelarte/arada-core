# DOMAIN-005L — Territory Read Model

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Territorial Management

Aggregate:
Territory

Documentos relacionados:

- DOMAIN-005-Aggregate.md
- DOMAIN-005A-Lifecycle.md
- DOMAIN-005B-State-Machine.md
- DOMAIN-005C-Commands.md
- DOMAIN-005D-Domain-Events.md
- DOMAIN-005E-Invariants.md
- DOMAIN-005F-Permissions.md
- DOMAIN-005G-Repository-Contract.md
- DOMAIN-005H-Examples.md
- DOMAIN-005I-Versioning.md
- DOMAIN-005J-Consistency-Boundary.md
- DOMAIN-005K-Integration-Events.md
- DOMAIN-005M-Test-Scenarios.md

---

# Objetivo

Definir el Read Model asociado al Aggregate **Territory**.

El Read Model proporciona una representación optimizada para
consulta del estado territorial sin exponer ni modificar
directamente el Aggregate.

El Read Model existe para satisfacer necesidades de lectura,
consulta, búsqueda, navegación, visualización e integración sin
convertir dichas necesidades en dependencias sobre el modelo
transaccional del dominio.

---

# Principio Fundamental

El Read Model es una representación de lectura.

No constituye el Aggregate.

```text
Territory Aggregate
        │
        ▼
Domain Event
        │
        ▼
Integration / Projection
        │
        ▼
Territory Read Model