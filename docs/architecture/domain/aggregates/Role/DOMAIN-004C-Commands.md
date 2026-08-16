# DOMAIN-004C — Role Commands

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
- DOMAIN-004B-State-Machine.md
- DOMAIN-004D-Domain-Events.md
- DOMAIN-004E-Invariants.md
- DOMAIN-004F-Permissions.md
- DOMAIN-004G-Repository-Contract.md

---

# Objetivo

Este documento define los **Commands** oficiales del Aggregate
**Role**.

Los Commands representan solicitudes explícitas para modificar
el estado de un Role. Todo cambio del Aggregate debe producirse
exclusivamente mediante un Command válido.

Los Commands describen una intención de negocio, no una
implementación técnica.

---

# Principios

Los Commands del Aggregate siguen los siguientes principios:

- expresan una única intención;
- modifican un único Aggregate;
- son ejecutados de forma atómica;
- validan todas las invariantes;
- producen cero o más Domain Events;
- incrementan la versión únicamente cuando el cambio es exitoso.

---

# Lista Oficial de Commands

| Command | Propósito |
|----------|-----------|
| CreateRole | Crear un nuevo Role |
| RenameRole | Cambiar el nombre del Role |
| ChangeDescription | Actualizar la descripción |
| ActivateRole | Activar el Role |
| DeactivateRole | Desactivar el Role |
| ArchiveRole | Archivar definitivamente el Role |

---

# CreateRole

## Objetivo

Crear un nuevo Role dentro de una Organization.

## Precondiciones

- Organization existente.
- Name único.
- Code único.
- Nombre válido.
- Código válido.

## Parámetros

```text
OrganizationId

Name

Code

Description

RoleType

IsSystemRole
```

## Resultado

```text
State = Draft

Version = 1
```

## Domain Event

```text
RoleCreated
```

---

# RenameRole

## Objetivo

Modificar el nombre visible del Role.

## Precondiciones

- Role no archivado.
- Nuevo nombre válido.
- Nombre único dentro de la Organization.

## Parámetros

```text
RoleId

NewName
```

## Resultado

El estado permanece sin cambios.

## Domain Event

```text
RoleRenamed
```

---

# ChangeDescription

## Objetivo

Modificar la descripción funcional del Role.

## Precondiciones

- Role no archivado.

## Parámetros

```text
RoleId

NewDescription
```

## Resultado

Actualización de la descripción.

## Domain Event

```text
RoleDescriptionChanged
```

---

# ActivateRole

## Objetivo

Habilitar el Role dentro del catálogo organizacional.

## Estados permitidos

```text
Draft

Inactive
```

## Parámetros

```text
RoleId
```

## Resultado

```text
State = Active
```

## Domain Event

```text
RoleActivated
```

---

# DeactivateRole

## Objetivo

Suspender temporalmente un Role.

## Estados permitidos

```text
Active
```

## Parámetros

```text
RoleId
```

## Resultado

```text
State = Inactive
```

## Domain Event

```text
RoleDeactivated
```

---

# ArchiveRole

## Objetivo

Cerrar definitivamente el ciclo de vida del Role.

## Estados permitidos

```text
Draft

Active

Inactive
```

## Parámetros

```text
RoleId
```

## Resultado

```text
State = Archived
```

## Domain Event

```text
RoleArchived
```

---

# Validaciones Comunes

Antes de ejecutar cualquier Command se validan:

- existencia del Aggregate;
- versión esperada;
- permisos del actor;
- estado actual;
- invariantes;
- consistencia del Aggregate.

Si alguna validación falla, el Command es rechazado.

---

# Commands Rechazados

Ejemplos:

```text
ActivateRole

↓

Role = Active
```

Resultado:

```text
InvalidStateTransition
```

---

```text
ArchiveRole

↓

Role = Archived
```

Resultado:

```text
InvalidStateTransition
```

---

```text
RenameRole

↓

Nombre duplicado
```

Resultado:

```text
DuplicateRoleName
```

---

```text
CreateRole

↓

Code duplicado
```

Resultado:

```text
DuplicateRoleCode
```

---

# Idempotencia

Los siguientes Commands deben ser idempotentes cuando se
reprocesan con el mismo identificador de solicitud:

- ActivateRole
- DeactivateRole
- ArchiveRole

El sistema no debe generar eventos duplicados.

---

# Concurrencia

Todo Command verifica la propiedad:

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

Persist Aggregate

↓

Persist Events

↓

Commit
```

Si la versión no coincide:

```text
ConcurrencyConflict
```

---

# Domain Events Generados

| Command | Domain Event |
|----------|--------------|
| CreateRole | RoleCreated |
| RenameRole | RoleRenamed |
| ChangeDescription | RoleDescriptionChanged |
| ActivateRole | RoleActivated |
| DeactivateRole | RoleDeactivated |
| ArchiveRole | RoleArchived |

---

# Reglas para System Roles

Cuando:

```text
IsSystemRole = true
```

pueden aplicarse restricciones adicionales.

Ejemplos:

- RenameRole restringido.
- ArchiveRole prohibido.
- DeactivateRole restringido.

Estas reglas se formalizan en:

```text
DOMAIN-004E-Invariants.md
```

---

# Consistencia

Cada Command:

- modifica un único Aggregate;
- ejecuta una única transacción;
- preserva las invariantes;
- incrementa la versión;
- genera los Domain Events correspondientes.

---

# Compatibilidad Arquitectónica

Los Commands son compatibles con:

- Domain-Driven Design (DDD);
- Command Pattern;
- CQRS;
- Clean Architecture;
- Event Sourcing.

---

# Definición de Éxito

Los Commands del Aggregate **Role** constituyen el mecanismo
exclusivo para modificar el estado de una función organizacional
dentro de AURA. Su diseño garantiza operaciones explícitas,
determinísticas y auditables, preservando la consistencia del
Aggregate y proporcionando una base sólida para la gestión de
cargos organizacionales y su posterior integración con el modelo
de autorización y permisos.