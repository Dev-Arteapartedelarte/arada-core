# DOMAIN-005I — Territory Versioning

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
- DOMAIN-005J-Consistency-Boundary.md

---

# Objetivo

Definir el modelo de versionado del Aggregate **Territory**.

El versionado permite identificar de forma inequívoca cada
estado persistido del Aggregate y proporciona mecanismos para
controlar modificaciones concurrentes.

El versionado pertenece al Aggregate y forma parte de su
consistencia.

---

# Principios

El versionado de Territory debe cumplir:

- monotonía;
- unicidad dentro de la secuencia del Aggregate;
- incremento controlado;
- inmutabilidad de versiones ya confirmadas;
- compatibilidad con concurrencia optimista;
- trazabilidad;
- consistencia transaccional.

Una versión nunca debe modificarse arbitrariamente.

---

# Aggregate Version

Cada Territory posee una versión:

```text
AggregateVersion