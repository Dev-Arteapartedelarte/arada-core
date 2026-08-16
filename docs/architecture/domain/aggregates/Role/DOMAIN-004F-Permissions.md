# DOMAIN-004F — Role Permissions

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
- DOMAIN-004C-Commands.md
- DOMAIN-004D-Domain-Events.md
- DOMAIN-004E-Invariants.md
- DOMAIN-005-Aggregate.md
- DOMAIN-005F-Permissions.md

---

# Objetivo

Este documento define las autorizaciones necesarias para
ejecutar los Commands del Aggregate **Role**.

Los permisos determinan quién puede administrar la estructura de
Roles de una Organization.

Este documento **no define permisos funcionales del sistema**;
define únicamente quién está autorizado para modificar el
Aggregate Role.

Role no contiene Permissions. Cada Permission es una capacidad explícita
asociada al Command y evaluada por Application.

---

# Principios

El modelo de autorización sigue los siguientes principios:

- mínimo privilegio;
- separación de responsabilidades;
- autorización explícita;
- auditoría obligatoria;
- independencia del modelo de autenticación;
- control por Organization.

---

# Actores del Dominio

El Aggregate reconoce los siguientes actores conceptuales:

```text
Platform Administrator

Organization Administrator

Organization Owner

Committee Manager

Auditor

System Process
```

Todos los actores se representan mediante una Membership válida.

---

# Matriz de Permisos

| Command | Platform Admin | Org Owner | Org Admin | Committee Manager | Auditor | System |
|----------|:--------------:|:---------:|:---------:|:-----------------:|:--------:|:------:|
| CreateRole | ✓ | ✓ | ✓ | ✗ | ✗ | ✓ |
| RenameRole | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| ChangeDescription | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| ActivateRole | ✓ | ✓ | ✓ | ✗ | ✗ | ✓ |
| DeactivateRole | ✓ | ✓ | ✓ | ✗ | ✗ | ✓ |
| ArchiveRole | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |

---

# CreateRole

Permite registrar un nuevo Role dentro de una Organization.

Autorizados:

- Platform Administrator
- Organization Owner
- Organization Administrator
- procesos automáticos autorizados

Requiere:

- Organization existente;
- permisos administrativos vigentes.

---

# RenameRole

Permite modificar el nombre visible del Role.

Autorizados:

- Platform Administrator
- Organization Owner
- Organization Administrator

No está permitido para:

- Committee Manager
- Auditor

---

# ChangeDescription

Permite actualizar la descripción funcional.

Autorizados:

- Platform Administrator
- Organization Owner
- Organization Administrator

---

# ActivateRole

Permite habilitar nuevamente un Role.

Autorizados:

- Platform Administrator
- Organization Owner
- Organization Administrator
- procesos automáticos autorizados

---

# DeactivateRole

Permite suspender temporalmente un Role.

Autorizados:

- Platform Administrator
- Organization Owner
- Organization Administrator
- procesos automáticos autorizados

---

# ArchiveRole

Finaliza definitivamente el ciclo de vida del Role.

Autorizados:

- Platform Administrator
- Organization Owner
- Organization Administrator

El archivado debe quedar registrado en auditoría.

---

# Restricciones para System Roles

Cuando:

```text
IsSystemRole = true
```

se aplican restricciones adicionales.

Dependiendo de la política de la plataforma:

- sólo Platform Administrator puede modificarlos;
- puede prohibirse su archivado;
- puede prohibirse cambiar Name;
- puede prohibirse cambiar Code.

Estas restricciones protegen la integridad del sistema.

---

# Validación de Autorización

Antes de ejecutar cualquier Command se valida:

```text
Identity

↓

Authentication

↓

Membership

↓

Authorization

↓

Execute Command
```

Si la autorización falla:

```text
PermissionDenied
```

---

# Auditoría

Toda operación autorizada registra conceptualmente:

```text
ActorId

MembershipId

RoleId

OrganizationId

Command

OccurredOn

CorrelationId
```

La información permite reconstruir quién realizó cada cambio.

---

# Delegación

Una Organization puede delegar la administración de Roles
mediante mecanismos definidos por el dominio.

La delegación:

- debe ser explícita;
- debe ser revocable;
- debe quedar auditada.

La implementación pertenece a servicios de aplicación y no al
Aggregate.

---

# Permissions y Aggregate

Role no almacena, agrupa ni concede Permissions. Application exige la
Permission explícita asociada al Command y puede utilizar el contexto del
actor sin inferir autorización desde Role, Membership o Citizen.

El Aggregate valida exclusivamente estado e invariantes propias.

---

# Compatibilidad Arquitectónica

El modelo de permisos es compatible con:

- Domain-Driven Design (DDD);
- Role-Based Access Control (RBAC);
- Hexagonal Architecture;
- CQRS;
- Event-Driven Architecture.

---

# Definición de Éxito

El modelo de permisos del Aggregate **Role** garantiza que la
administración de los cargos organizacionales sólo pueda ser
realizada por actores autorizados. La separación entre **Role**
(como función organizacional) y **Permission** (como capacidad
de autorización) proporciona un diseño desacoplado, extensible y
coherente con la arquitectura de AURA y con las prácticas de
RBAC utilizadas en sistemas empresariales.