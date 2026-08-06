# DOMAIN-004A — Role Lifecycle

Versión: 1.0

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
- DOMAIN-004B-State-Machine.md
- DOMAIN-004C-Commands.md
- DOMAIN-004D-Domain-Events.md
- DOMAIN-004E-Invariants.md
- DOMAIN-004K-Integration-Events.md

---

# Objetivo

Este documento define el ciclo de vida oficial del Aggregate
**Role**.

El ciclo de vida establece cómo evoluciona un Role desde su
creación hasta su archivado, garantizando que cada transición
respete las reglas del dominio y preserve la consistencia de la
estructura organizacional.

---

# Principios

El ciclo de vida del Aggregate sigue los siguientes principios:

- evolución controlada;
- transiciones explícitas;
- estados finitos;
- invariantes preservadas;
- historial auditable;
- consistencia transaccional.

---

# Estados del Ciclo de Vida

```text
Draft

↓

Active

↓

Inactive

↓

Archived
```

Cada estado representa una condición válida del Role dentro del
dominio.

---

# Estado: Draft

Representa un Role recién creado.

Características:

- aún no puede asignarse a Memberships;
- puede modificarse libremente;
- aún no participa en procesos organizacionales.

Operaciones permitidas:

- RenameRole
- ChangeDescription
- ActivateRole
- ArchiveRole

---

# Estado: Active

El Role se encuentra operativo.

Características:

- puede asignarse a Memberships;
- puede utilizarse en procesos de autorización;
- forma parte de la estructura organizacional.

Operaciones permitidas:

- RenameRole
- ChangeDescription
- DeactivateRole
- ArchiveRole

---

# Estado: Inactive

El Role deja de estar disponible para nuevas asignaciones.

Características:

- conserva su historial;
- las asignaciones existentes permanecen válidas hasta que el
  dominio determine lo contrario;
- no puede asignarse a nuevas Memberships.

Operaciones permitidas:

- ActivateRole
- RenameRole
- ChangeDescription
- ArchiveRole

---

# Estado: Archived

Estado final del ciclo de vida.

Características:

- el Role permanece únicamente con fines históricos;
- no admite modificaciones;
- no puede reactivarse;
- conserva toda su trazabilidad.

Operaciones permitidas:

Ninguna.

---

# Flujo Completo

```text
CreateRole

↓

Draft

↓

ActivateRole

↓

Active

↓

DeactivateRole

↓

Inactive

↓

ActivateRole

↓

Active

↓

ArchiveRole

↓

Archived
```

---

# Creación

El ciclo comienza mediante:

```text
CreateRole
```

Resultado:

```text
State = Draft

Version = 1
```

Evento generado:

```text
RoleCreated
```

---

# Activación

Un Role en estado Draft o Inactive puede activarse.

```text
Draft

↓

ActivateRole

↓

Active
```

o

```text
Inactive

↓

ActivateRole

↓

Active
```

Evento:

```text
RoleActivated
```

---

# Desactivación

Sólo un Role activo puede desactivarse.

```text
Active

↓

DeactivateRole

↓

Inactive
```

Evento:

```text
RoleDeactivated
```

---

# Archivado

El archivado representa el cierre definitivo del Role.

```text
Draft

↓

ArchiveRole

↓

Archived
```

o

```text
Active

↓

ArchiveRole

↓

Archived
```

o

```text
Inactive

↓

ArchiveRole

↓

Archived
```

Evento:

```text
RoleArchived
```

---

# Estados Terminales

El único estado terminal es:

```text
Archived
```

Desde este estado no existen transiciones válidas.

---

# Transiciones Inválidas

No están permitidas las siguientes operaciones:

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

DeactivateRole
```

Todas deben generar:

```text
InvalidStateTransition
```

---

# Roles del Sistema

Cuando:

```text
IsSystemRole = true
```

el ciclo de vida incorpora restricciones adicionales.

Ejemplos:

- no puede eliminarse;
- el archivado puede estar prohibido;
- determinadas modificaciones requieren privilegios elevados.

Estas reglas se formalizan en:

```text
DOMAIN-004E-Invariants.md
```

---

# Versionado

Cada transición válida incrementa:

```text
Version
```

Ejemplo:

```text
Draft

Version = 1

↓

ActivateRole

↓

Version = 2
```

Las transiciones rechazadas no modifican la versión.

---

# Eventos del Ciclo de Vida

| Transición | Domain Event |
|------------|--------------|
| Create | RoleCreated |
| Activate | RoleActivated |
| Deactivate | RoleDeactivated |
| Archive | RoleArchived |
| Rename | RoleRenamed |
| Change Description | RoleDescriptionChanged |

---

# Consistencia

Todas las transiciones:

- ocurren dentro del Aggregate;
- son atómicas;
- generan cero o más Domain Events;
- preservan las invariantes;
- incrementan la versión únicamente cuando el cambio es exitoso.

---

# Reconstrucción

Cuando se emplea Event Sourcing, el ciclo de vida se reconstruye
mediante:

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

El estado final se obtiene aplicando secuencialmente los eventos.

---

# Compatibilidad Arquitectónica

El ciclo de vida es compatible con:

- Domain-Driven Design (DDD);
- Clean Architecture;
- CQRS;
- Event Sourcing;
- Event-Driven Architecture.

---

# Definición de Éxito

El ciclo de vida del Aggregate **Role** garantiza que toda
función organizacional evolucione de forma controlada, auditable
y consistente. Cada transición preserva las invariantes del
dominio, protege la estructura organizacional y proporciona una
base estable para la asignación de responsabilidades dentro del
ecosistema AURA.