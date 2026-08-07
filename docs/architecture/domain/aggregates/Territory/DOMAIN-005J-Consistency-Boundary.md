# DOMAIN-005J — Territory Consistency Boundary

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
- DOMAIN-005K-Integration-Events.md

---

# Objetivo

Definir el límite de consistencia del Aggregate **Territory**.

El Consistency Boundary establece qué información debe
mantenerse consistente dentro del Aggregate y qué
colaboraciones deben resolverse fuera de él.

Territory constituye una unidad de consistencia.

Toda modificación que afecte directamente al estado interno del
Aggregate debe resolverse dentro de este límite antes de que la
operación sea confirmada.

---

# Principio Fundamental

El Aggregate **Territory** protege su propio estado.

```text
Territory
    │
    ├── Identity
    ├── State
    ├── Type
    ├── Administrative Data
    ├── Hierarchy Constraints
    └── Domain Invariants