# DOMAIN-005K — Territory Integration Events

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
- DOMAIN-005L-Read-Model.md

---

# Objetivo

Definir los Integration Events asociados al Aggregate
**Territory** y establecer las reglas mediante las cuales los
cambios relevantes del Aggregate pueden ser comunicados hacia
otros Bounded Contexts, servicios o sistemas externos.

Los Integration Events constituyen una frontera de integración.

No forman parte del estado interno del Aggregate.

---

# Principio Fundamental

Territory produce cambios dentro de su propio límite de
consistencia.

Cuando un cambio debe ser conocido fuera de ese límite, puede
publicarse un Integration Event.

```text
Territory
    ↓
Domain Event
    ↓
Integration Event
    ↓
External Boundary