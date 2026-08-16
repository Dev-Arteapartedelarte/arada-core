# DOMAIN-004N — Role Performance Rules

Versión: 1.1

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Authorization Management

Aggregate:
Role

Documentos relacionados:

- DOMAIN-004-Aggregate.md
- DOMAIN-004G-Repository-Contract.md
- DOMAIN-004I-Versioning.md
- DOMAIN-004J-Consistency-Boundary.md
- DOMAIN-004K-Integration-Events.md
- DOMAIN-004L-Read-Model.md
- CORE-011-Repository-Contracts.md

---

# Objetivo

Este documento establece las reglas oficiales de rendimiento
para el Aggregate **Role**.

El propósito es asegurar que la administración de Roles sea
escalable, eficiente y predecible, incluso en organizaciones con
miles de miembros, múltiples sedes y una alta frecuencia de
consultas y asignaciones.

Las reglas aquí definidas son independientes de la tecnología de
persistencia y representan requisitos arquitectónicos del
dominio.

---

# Principios

El Aggregate Role debe cumplir los siguientes principios:

- operaciones determinísticas;
- complejidad acotada;
- mínima carga transaccional;
- lectura desacoplada;
- escalabilidad horizontal;
- consistencia fuerte únicamente dentro del Aggregate.

---

# Responsabilidades de Rendimiento

El Aggregate únicamente administra:

- identidad del Role;
- ciclo de vida;
- nombre;
- código;
- descripción;
- estado;
- metadatos.

No administra:

- Memberships;
- Permissions;
- Citizens;
- Organizations;
- consultas complejas.

---

# Tiempo Esperado de Ejecución

Los Commands deberían ejecutarse con la siguiente complejidad
conceptual:

| Command | Complejidad esperada |
|----------|----------------------|
| CreateRole | O(1) |
| RenameRole | O(1) |
| ChangeDescription | O(1) |
| ActivateRole | O(1) |
| DeactivateRole | O(1) |
| ArchiveRole | O(1) |

Las verificaciones de unicidad podrán depender de índices del
almacenamiento utilizado.

---

# Consultas

Las consultas deben resolverse mediante el Read Model.

Nunca mediante el Aggregate.

Ejemplos:

```text
Roles por Organization

Roles Activos

Roles Archivados

System Roles

Búsqueda por Código

Búsqueda por Nombre
```

---

# Índices Recomendados

Toda implementación debería indexar como mínimo:

```text
RoleId
```

```text
OrganizationId
```

```text
Code
```

```text
Name
```

```text
Status
```

```text
IsSystemRole
```

Estos índices permiten consultas eficientes sin afectar el modelo
transaccional.

---

# Escalabilidad

El Aggregate debe escalar de manera independiente.

Ejemplo conceptual:

```text
Organization

↓

500 Roles

↓

20.000 Memberships
```

La cantidad de Memberships no debe afectar el rendimiento del
Aggregate Role.

---

# Tamaño del Aggregate

El Aggregate debe permanecer pequeño.

Debe contener únicamente atributos propios del Role.

No debe incorporar:

- listas de miembros;
- listas de permisos;
- historial completo;
- documentos;
- archivos.

---

# Lecturas

Las operaciones de lectura deben utilizar:

```text
Role Read Model
```

Nunca deben reconstruir el Aggregate para consultas masivas.

---

# Escrituras

Cada Command debe modificar únicamente un Aggregate.

Nunca debe actualizar:

- Membership;
- Permission;
- Citizen;
- Organization.

Los cambios sobre otros Aggregates se propagan mediante
Integration Events.

---

# Publicación de Eventos

El costo de publicación de eventos debe mantenerse constante.

Proceso:

```text
Execute Command

↓

Persist Aggregate

↓

Commit

↓

Publish Integration Event
```

La publicación nunca debe bloquear la transacción principal.

---

# Event Sourcing

Cuando Event Sourcing esté habilitado:

- la reconstrucción debe realizarse únicamente con eventos del
  Aggregate;
- snapshots podrán utilizarse para reducir tiempos de carga;
- los snapshots nunca reemplazan la secuencia oficial de eventos.

---

# Snapshots

Se recomienda considerar snapshots cuando un Aggregate acumule un
número elevado de eventos.

Ejemplo:

```text
Role

↓

100 Events

↓

Snapshot

↓

Continue Event Stream
```

La frecuencia de snapshots depende de la infraestructura.

---

# Caché

Puede utilizarse caché para:

- consultas frecuentes;
- catálogos de Roles;
- System Roles.

El caché:

- nunca reemplaza el Repository;
- nunca modifica el dominio;
- debe invalidarse después de cambios exitosos.

---

# Concurrencia

El Aggregate utiliza concurrencia optimista basada en:

```text
Version
```

La validación de versión debe realizarse antes de persistir.

Los conflictos deben resolverse mediante:

```text
ConcurrencyConflict
```

---

# Operaciones Prohibidas

No se permite:

- recorrer Memberships desde Role;
- consultar otros Repositories;
- cargar Permissions durante un Command;
- ejecutar consultas analíticas;
- realizar agregaciones complejas dentro del Aggregate.

---

# Consistencia

La consistencia fuerte aplica únicamente al Aggregate.

Las proyecciones externas utilizan:

```text
Eventually Consistent
```

mediante Integration Events.

---

# Métricas Recomendadas

La plataforma debería monitorear:

- tiempo promedio de ejecución de Commands;
- conflictos de concurrencia;
- latencia del Repository;
- latencia de publicación de eventos;
- tiempo de actualización del Read Model;
- cantidad de Roles por Organization;
- frecuencia de activaciones y desactivaciones.

---

# Escenarios de Alta Carga

El Aggregate debe mantener un comportamiento estable cuando:

- múltiples administradores crean Roles simultáneamente;
- varias Organizations operan en paralelo;
- existen miles de consultas concurrentes al Read Model;
- se publican eventos hacia múltiples consumidores.

---

# Compatibilidad Arquitectónica

Estas reglas son compatibles con:

- Domain-Driven Design (DDD);
- CQRS;
- Event Sourcing;
- Clean Architecture;
- Event-Driven Architecture;
- Escalabilidad Horizontal.

---

# Definición de Éxito

El Aggregate **Role** cumple los requisitos de rendimiento cuando
mantiene operaciones de escritura pequeñas, determinísticas y
atómicas, delega las consultas al Read Model, publica eventos sin
acoplamiento y conserva un comportamiento estable y escalable
independientemente del número de miembros, organizaciones o
consumidores del ecosistema AURA.