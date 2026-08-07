# DOMAIN-005P — Territory Extension Points

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Territorial Management

Aggregate:
Territory

---

# Objetivo

Definir los puntos de extensión permitidos para el Aggregate
**Territory** sin comprometer:

- sus invariantes;
- su máquina de estados;
- su límite de consistencia;
- su encapsulamiento;
- su seguridad;
- su independencia de infraestructura;
- su capacidad de evolución.

Las extensiones deben ampliar las capacidades del sistema sin
convertir Territory en un Aggregate genérico o excesivamente
acoplado.

---

# Principio Fundamental

Territory debe poder evolucionar sin modificar innecesariamente su
núcleo de dominio.

Las extensiones deben respetar:

```text
Aggregate Boundary
+
Domain Invariants
+
State Machine
+
Commands
+
Domain Events
+
Repository Contract