# DOMAIN-005G — Territory Repository Contract

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
- DOMAIN-005H-Examples.md
- DOMAIN-005I-Versioning.md
- DOMAIN-005J-Consistency-Boundary.md

---

# Objetivo

Definir el contrato de persistencia del Aggregate **Territory**.

El Repository proporciona una abstracción para recuperar y
persistir Aggregates completos sin exponer detalles de
infraestructura al dominio.

El Repository no contiene reglas de negocio.

---

# Principios

El contrato debe garantizar:

- persistencia del Aggregate completo;
- recuperación por identidad;
- consistencia transaccional;
- control de concurrencia;
- aislamiento de infraestructura;
- independencia respecto del motor de persistencia;
- preservación de invariantes;
- ausencia de referencias directas a entidades de otros
  Aggregates.

---

# Responsabilidad

El Repository de Territory es responsable de:

```text
Load Territory
Save Territory
Check existence