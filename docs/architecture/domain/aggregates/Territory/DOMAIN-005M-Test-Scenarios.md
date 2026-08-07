# DOMAIN-005M — Territory Test Scenarios

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
- DOMAIN-005L-Read-Model.md
- DOMAIN-005N-Performance-Rules.md
- DOMAIN-005O-Security-Model.md
- DOMAIN-005P-Extension-Points.md

---

# Objetivo

Definir los escenarios de prueba que permiten verificar que el
Aggregate **Territory** cumple su contrato de dominio.

Los escenarios validan:

- identidad;
- creación;
- ciclo de vida;
- máquina de estados;
- Commands;
- Domain Events;
- invariantes;
- permisos;
- consistencia;
- versionado;
- Integration Events;
- Read Model;
- comportamiento ante errores;
- extensibilidad.

Las pruebas deben verificar comportamiento observable y no detalles
internos de implementación.

---

# Principio Fundamental

Las pruebas del Aggregate deben comprobar que:

```text
Command
    ↓
Territory
    ↓
Validación
    ↓
Nuevo estado
    ↓
Domain Event