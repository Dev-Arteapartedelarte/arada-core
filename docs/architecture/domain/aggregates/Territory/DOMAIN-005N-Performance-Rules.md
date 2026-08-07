# DOMAIN-005N — Territory Performance Rules

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

Definir las reglas de rendimiento que deben respetarse en la
implementación del Aggregate **Territory**.

Estas reglas buscan garantizar que Territory pueda operar de forma
predecible a medida que aumente:

- el número de territorios;
- la cantidad de relaciones territoriales;
- la frecuencia de cambios;
- el volumen de eventos;
- el número de consumidores;
- la cantidad de consultas sobre información territorial.

Las reglas de rendimiento no deben alterar las invariantes ni
romper el límite de consistencia del Aggregate.

---

# Principio Fundamental

El rendimiento de Territory debe obtenerse mediante:

```text
Aggregate pequeño
+
Operaciones acotadas
+
Persistencia eficiente
+
Read Models
+
Event-Driven Integration