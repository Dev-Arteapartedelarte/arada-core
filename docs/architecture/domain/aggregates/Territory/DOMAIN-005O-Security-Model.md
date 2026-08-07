# DOMAIN-005O — Territory Security Model

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

Definir el modelo de seguridad aplicable al Aggregate Territory.

El modelo establece las reglas mediante las cuales Territory debe
proteger:

- su identidad;
- su estado;
- sus invariantes;
- sus operaciones;
- sus relaciones;
- sus eventos;
- su información territorial;
- su límite de consistencia.

La seguridad debe preservar el modelo de dominio sin introducir
dependencias de infraestructura dentro del Aggregate.

---

# Principio Fundamental

La seguridad de Territory se implementa mediante separación de
responsabilidades:

```text
Identity
    ↓
Authentication

Actor
    ↓
Authorization

Command
    ↓
Domain Validation

Territory
    ↓
Invariant Protection

Event
    ↓
Controlled Publication