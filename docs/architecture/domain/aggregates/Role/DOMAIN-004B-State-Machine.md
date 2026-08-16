# DOMAIN-004B — Role State Machine

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
- DOMAIN-004A-Lifecycle.md
- DOMAIN-004C-Commands.md
- DOMAIN-004D-Domain-Events.md
- DOMAIN-004E-Invariants.md
- DOMAIN-004J-Consistency-Boundary.md

---

# Objetivo

Este documento define la máquina de estados oficial del
Aggregate **Role**.

La máquina de estados controla todas las transiciones válidas de
un Role durante su existencia, garantizando que la estructura de
cargos de una **Organization** permanezca consistente y que toda
evolución sea explícita, verificable y auditable.

---

# Principios

La máquina de estados sigue los siguientes principios:

- estados finitos;
- transiciones determinísticas;
- una única transición por Command;
- preservación de invariantes;
- generación de Domain Events;
- consistencia transaccional.

---

# Estados

El Aggregate **Role** posee cuatro estados oficiales.

```text
Draft

Active

Inactive

Archived
```

Cada Role debe encontrarse exactamente en uno de ellos.

---

# Diagrama General

```text
                CreateRole
                     │
                     ▼
                 +---------+
                 |  Draft  |
                 +---------+
                     │
          ActivateRole │
                     ▼
                +----------+
                |  Active  |
                +----------+
                     │
        DeactivateRole │
                     ▼
               +-----------+
               | Inactive  |
               +-----------+
                     │
          ActivateRole │
                     └──────────────┐
                                    │
                                    ▼
                               +----------+
                               |  Active  |
                               +----------+

Draft ───────────────┐
Active ──────────────┼── ArchiveRole ───► Archived
Inactive ────────────┘
```

---

# Estado: Draft

Representa un Role recién creado.

Características:

- aún no está disponible como referencia activa del catálogo;
- puede modificarse;
- puede activarse;
- puede archivarse.

Commands permitidos:

```text
RenameRole

ChangeDescription

ActivateRole

ArchiveRole
```

---

# Estado: Active

Representa un Role operativo.

Características:

- disponible para asignaciones;
- visible para la organización;
- puede utilizarse por Memberships.

Commands permitidos:

```text
RenameRole

ChangeDescription

DeactivateRole

ArchiveRole
```

---

# Estado: Inactive

Representa un Role temporalmente fuera de uso.

Características:

- no admite nuevas asignaciones;
- conserva historial;
- puede volver a activarse.

Commands permitidos:

```text
ActivateRole

RenameRole

ChangeDescription

ArchiveRole
```

---

# Estado: Archived

Estado final.

Características:

- sólo lectura;
- histórico;
- irreversible.

Commands permitidos:

Ninguno.

---

# Tabla Oficial de Transiciones

| Estado Actual | Command | Estado Resultante |
|---------------|---------|-------------------|
| Draft | ActivateRole | Active |
| Draft | ArchiveRole | Archived |
| Active | DeactivateRole | Inactive |
| Active | ArchiveRole | Archived |
| Inactive | ActivateRole | Active |
| Inactive | ArchiveRole | Archived |

---

# Transiciones Internas

Las siguientes operaciones no modifican el estado:

```text
RenameRole

ChangeDescription
```

Diagrama:

```text
Draft
   │
RenameRole
   │
Draft
```

```text
Active
   │
ChangeDescription
   │
Active
```

---

# Transiciones Inválidas

Las siguientes operaciones deben rechazarse.

```text
Draft

↓

DeactivateRole
```

```text
Active

↓

ActivateRole
```

```text
Inactive

↓

DeactivateRole
```

```text
Archived

↓

ActivateRole
```

```text
Archived

↓

RenameRole
```

```text
Archived

↓

ChangeDescription
```

```text
Archived

↓

ArchiveRole
```

Resultado:

```text
InvalidStateTransition
```

---

# Eventos Asociados

Cada transición válida genera un Domain Event.

| Command | Domain Event |
|----------|--------------|
| CreateRole | RoleCreated |
| ActivateRole | RoleActivated |
| DeactivateRole | RoleDeactivated |
| ArchiveRole | RoleArchived |
| RenameRole | RoleRenamed |
| ChangeDescription | RoleDescriptionChanged |

---

# Reglas Especiales para System Roles

Cuando:

```text
IsSystemRole = true
```

se aplican restricciones adicionales.

Ejemplos:

- no pueden eliminarse;
- el archivado puede estar restringido;
- el nombre puede ser inmutable;
- el código puede ser inmutable.

Las reglas específicas se documentan en:

```text
DOMAIN-004E-Invariants.md
```

---

# Concurrencia

Antes de aplicar una transición se valida:

```text
Version
```

Proceso:

```text
Load Aggregate

↓

Validate Version

↓

Execute Command

↓

Persist

↓

Publish Events
```

Si la versión no coincide:

```text
ConcurrencyConflict
```

---

# Consistencia

Cada transición:

- modifica un único Aggregate;
- ejecuta una sola transacción;
- preserva todas las invariantes;
- incrementa la versión;
- genera los eventos correspondientes.

---

# Compatibilidad con Event Sourcing

La máquina de estados puede reconstruirse mediante la secuencia
de Domain Events.

Ejemplo:

```text
RoleCreated

↓

RoleActivated

↓

RoleRenamed

↓

RoleDeactivated

↓

RoleActivated

↓

RoleArchived
```

La reproducción ordenada de los eventos reconstruye exactamente
el estado del Aggregate.

---

# Compatibilidad Arquitectónica

Este modelo es compatible con:

- Domain-Driven Design (DDD);
- Clean Architecture;
- CQRS;
- Event Sourcing;
- Event-Driven Architecture.

---

# Definición de Éxito

La máquina de estados del Aggregate **Role** garantiza que toda
función organizacional evolucione mediante transiciones
explícitas, válidas y auditables. Ningún cambio puede realizarse
fuera del flujo definido por el dominio, asegurando la
consistencia de la estructura organizacional y proporcionando
una base sólida para la asignación de responsabilidades dentro
del ecosistema AURA.