# DOMAIN-004H — Role Examples

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
- DOMAIN-004A-Lifecycle.md
- DOMAIN-004B-State-Machine.md
- DOMAIN-004C-Commands.md
- DOMAIN-004D-Domain-Events.md
- DOMAIN-004E-Invariants.md
- DOMAIN-004F-Permissions.md
- DOMAIN-003-Aggregate.md

---

# Objetivo

Este documento presenta ejemplos conceptuales del Aggregate
**Role**.

Los ejemplos ilustran el comportamiento esperado del dominio y
sirven como referencia para analistas, desarrolladores,
arquitectos y responsables de pruebas.

Todos los ejemplos son independientes de cualquier tecnología de
implementación.

---

# Ejemplo 1 — Crear un Role

Una junta de vecinos necesita incorporar el cargo de
**Encargado de Comunicaciones**.

Command

```text
CreateRole
```

Parámetros

```text
OrganizationId = ORG-001

Name = Encargado de Comunicaciones

Code = COMMUNICATION_MANAGER

Description = Responsable de las comunicaciones oficiales.

RoleType = Operational

IsSystemRole = false
```

Resultado

```text
State = Draft

Version = 1
```

Evento generado

```text
RoleCreated
```

---

# Ejemplo 2 — Activar un Role

Una vez revisado por la directiva, el nuevo cargo queda
disponible para ser utilizado.

Estado inicial

```text
Draft
```

Command

```text
ActivateRole
```

Resultado

```text
State = Active
```

Evento

```text
RoleActivated
```

---

# Ejemplo 3 — Cambiar el nombre

La organización decide utilizar una denominación más adecuada.

Estado inicial

```text
Active
```

Command

```text
RenameRole
```

Parámetros

```text
NewName = Coordinador de Comunicaciones
```

Resultado

```text
Name actualizado

State = Active
```

Evento

```text
RoleRenamed
```

---

# Ejemplo 4 — Modificar la descripción

Se amplían las responsabilidades del cargo.

Command

```text
ChangeDescription
```

Nueva descripción

```text
Responsable de la comunicación institucional,
redes sociales y relación con medios.
```

Resultado

```text
Descripción actualizada
```

Evento

```text
RoleDescriptionChanged
```

---

# Ejemplo 5 — Desactivar un Role

La organización decide dejar de utilizar temporalmente el cargo.

Estado inicial

```text
Active
```

Command

```text
DeactivateRole
```

Resultado

```text
State = Inactive
```

Evento

```text
RoleDeactivated
```

---

# Ejemplo 6 — Reactivar un Role

Meses después el cargo vuelve a ser necesario.

Estado inicial

```text
Inactive
```

Command

```text
ActivateRole
```

Resultado

```text
State = Active
```

Evento

```text
RoleActivated
```

---

# Ejemplo 7 — Archivar un Role

El cargo deja de existir en la estructura organizacional.

Estado inicial

```text
Inactive
```

Command

```text
ArchiveRole
```

Resultado

```text
State = Archived
```

Evento

```text
RoleArchived
```

---

# Ejemplo 8 — Nombre duplicado

Ya existe:

```text
Presidente
```

Se intenta crear nuevamente:

```text
Presidente
```

Resultado

```text
DuplicateRoleName
```

No se genera ningún Domain Event.

---

# Ejemplo 9 — Código duplicado

Ya existe:

```text
PRESIDENT
```

Nuevo intento

```text
Code = PRESIDENT
```

Resultado

```text
DuplicateRoleCode
```

El Aggregate permanece sin cambios.

---

# Ejemplo 10 — Modificar un Role archivado

Estado actual

```text
Archived
```

Command

```text
RenameRole
```

Resultado

```text
ArchivedRoleModification
```

No existe transición válida.

---

# Ejemplo 11 — Asignación a Membership

Existe el Role:

```text
Secretario
```

Existe la Membership:

```text
Juan Pérez

Miembro Activo
```

Resultado conceptual

```text
Membership

↓

RoleId

↓

Secretary
```

La asignación pertenece al Aggregate
**Membership**.

El Aggregate **Role** permanece inalterado.

---

# Ejemplo 12 — Protección de un System Role

Role

```text
Platform Administrator
```

Propiedad

```text
IsSystemRole = true
```

Command

```text
ArchiveRole
```

Resultado

```text
OperationNotAllowed
```

El Role continúa activo.

---

# Ejemplo 13 — Conflicto de concurrencia

Usuario A

```text
Version = 5
```

Usuario B

```text
Version = 5
```

Usuario A ejecuta:

```text
RenameRole
```

La versión pasa a:

```text
Version = 6
```

Usuario B intenta guardar utilizando:

```text
Version = 5
```

Resultado

```text
ConcurrencyConflict
```

El segundo cambio es rechazado.

---

# Ejemplo 14 — Ciclo de vida completo

```text
CreateRole

↓

Draft

↓

ActivateRole

↓

Active

↓

RenameRole

↓

ChangeDescription

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

Eventos generados

```text
RoleCreated

↓

RoleActivated

↓

RoleRenamed

↓

RoleDescriptionChanged

↓

RoleDeactivated

↓

RoleActivated

↓

RoleArchived
```

---

# Ejemplo 15 — Organización con múltiples Roles

```text
Organization
│
├── Presidente
├── Vicepresidente
├── Secretario
├── Tesorero
├── Director
├── Coordinador de Proyectos
├── Encargado de Comunicaciones
└── Voluntario
```

Cada Role:

- posee un `RoleId` único;
- pertenece a la misma `Organization`;
- mantiene su propio ciclo de vida;
- puede ser asignado a múltiples Memberships según las reglas del dominio.

---

# Compatibilidad Arquitectónica

Los ejemplos son compatibles con:

- Domain-Driven Design (DDD);
- Clean Architecture;
- CQRS;
- Event Sourcing;
- Event-Driven Architecture.

---

# Definición de Éxito

Los ejemplos del Aggregate **Role** ilustran escenarios representativos de creación, administración y evolución de los cargos organizacionales dentro de AURA. Sirven como referencia común para el diseño, implementación, pruebas y validación del dominio, asegurando una comprensión uniforme del comportamiento esperado del Aggregate.