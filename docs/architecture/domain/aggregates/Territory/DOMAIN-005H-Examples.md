# DOMAIN-005H — Territory Examples

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
- DOMAIN-005I-Versioning.md
- DOMAIN-005J-Consistency-Boundary.md

---

# Objetivo

Documentar ejemplos representativos del comportamiento del
Aggregate **Territory**.

Los ejemplos tienen carácter normativo respecto del flujo
descrito en los documentos del Aggregate, pero no constituyen
implementaciones de código.

Su objetivo es mostrar:

- creación;
- validación;
- activación;
- modificación;
- desactivación;
- reactivación;
- archivado;
- cambios jerárquicos;
- rechazo de operaciones inválidas;
- control de permisos;
- control de invariantes;
- concurrencia.

---

# Ejemplo 01 — Creación de Territory

## Contexto

Un actor autorizado solicita crear un nuevo territorio.

Command:

```text
CreateTerritory