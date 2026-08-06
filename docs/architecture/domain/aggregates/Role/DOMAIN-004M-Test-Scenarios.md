# DOMAIN-004M — Role Test Scenarios

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
- DOMAIN-004C-Commands.md
- DOMAIN-004D-Domain-Events.md
- DOMAIN-004E-Invariants.md
- DOMAIN-004G-Repository-Contract.md
- DOMAIN-004I-Versioning.md
- DOMAIN-004J-Consistency-Boundary.md
- DOMAIN-004L-Read-Model.md
- CORE-015-Test-Strategy.md

---

# Objetivo

Este documento define los escenarios oficiales de prueba para el
Aggregate **Role**.

Su propósito es verificar que el Aggregate implemente
correctamente las reglas de negocio, preserve las invariantes y
genere los Domain Events esperados en cada transición de estado.

---

# Principios

Las pruebas deben garantizar:

- comportamiento determinístico;
- cumplimiento de invariantes;
- consistencia transaccional;
- generación correcta de eventos;
- control de concurrencia;
- independencia de la infraestructura.

Cada escenario describe únicamente el comportamiento esperado
del dominio.

---

# Escenario 1 — Crear un Role

## Dado

- una Organization existente;
- un nombre único;
- un código único.

## Cuando

```text
CreateRole
```

## Entonces

- se crea el Aggregate;
- `State = Draft`;
- `Version = 1`;
- se genera:

```text
RoleCreated
```

---

# Escenario 2 — Activar un Role

## Dado

```text
State = Draft
```

## Cuando

```text
ActivateRole
```

## Entonces

```text
State = Active
```

Evento:

```text
RoleActivated
```

---

# Escenario 3 — Cambiar el Nombre

## Dado

```text
State = Active
```

## Cuando

```text
RenameRole
```

## Entonces

- el nombre cambia;
- la versión aumenta;
- se publica:

```text
RoleRenamed
```

---

# Escenario 4 — Cambiar la Descripción

## Dado

Role activo.

## Cuando

```text
ChangeDescription
```

## Entonces

- la descripción se actualiza;
- la versión aumenta;
- se genera:

```text
RoleDescriptionChanged
```

---

# Escenario 5 — Desactivar un Role

## Dado

```text
State = Active
```

## Cuando

```text
DeactivateRole
```

## Entonces

```text
State = Inactive
```

Evento:

```text
RoleDeactivated
```

---

# Escenario 6 — Reactivar un Role

## Dado

```text
State = Inactive
```

## Cuando

```text
ActivateRole
```

## Entonces

```text
State = Active
```

Evento:

```text
RoleActivated
```

---

# Escenario 7 — Archivar un Role

## Dado

```text
State = Inactive
```

## Cuando

```text
ArchiveRole
```

## Entonces

```text
State = Archived
```

Evento:

```text
RoleArchived
```

---

# Escenario 8 — Nombre Duplicado

## Dado

Existe un Role llamado:

```text
Presidente
```

## Cuando

Se ejecuta:

```text
CreateRole
```

con el mismo nombre.

## Entonces

Resultado:

```text
DuplicateRoleName
```

No se modifica el Aggregate.

No se generan eventos.

---

# Escenario 9 — Código Duplicado

## Dado

Existe:

```text
Code = PRESIDENT
```

## Cuando

Se crea un nuevo Role con el mismo código.

## Entonces

```text
DuplicateRoleCode
```

La operación es rechazada.

---

# Escenario 10 — Modificar un Role Archivado

## Dado

```text
State = Archived
```

## Cuando

```text
RenameRole
```

## Entonces

```text
ArchivedRoleModification
```

No cambia la versión.

No se generan eventos.

---

# Escenario 11 — Activación Inválida

## Dado

```text
State = Active
```

## Cuando

```text
ActivateRole
```

## Entonces

```text
InvalidStateTransition
```

---

# Escenario 12 — Conflicto de Concurrencia

## Dado

Dos usuarios cargan:

```text
Version = 5
```

## Cuando

El primer usuario ejecuta:

```text
RenameRole
```

y persiste correctamente.

El segundo intenta guardar con:

```text
ExpectedVersion = 5
```

## Entonces

```text
ConcurrencyConflict
```

---

# Escenario 13 — Protección de System Role

## Dado

```text
IsSystemRole = true
```

## Cuando

```text
ArchiveRole
```

## Entonces

```text
OperationNotAllowed
```

El Aggregate permanece sin cambios.

---

# Escenario 14 — Búsqueda por Código

## Dado

Existe:

```text
Code = SECRETARY
```

## Cuando

El Repository ejecuta:

```text
FindByCode()
```

## Entonces

Retorna el Aggregate correcto.

---

# Escenario 15 — Búsqueda por Nombre

## Dado

Existe:

```text
Name = Secretario
```

## Cuando

```text
FindByName()
```

## Entonces

Retorna el Role correspondiente.

---

# Escenario 16 — Persistencia Correcta

## Dado

Un Aggregate válido.

## Cuando

```text
Save()
```

## Entonces

- se persiste completamente;
- no existen cambios parciales;
- la versión se incrementa;
- los eventos quedan registrados.

---

# Escenario 17 — Reconstrucción mediante Event Sourcing

## Dado

La secuencia:

```text
RoleCreated

↓

RoleActivated

↓

RoleRenamed

↓

RoleDescriptionChanged

↓

RoleArchived
```

## Cuando

El Repository reconstruye el Aggregate.

## Entonces

El estado obtenido es:

```text
Archived
```

La versión coincide con el número de eventos aplicados.

---

# Escenario 18 — Actualización del Read Model

## Dado

Se publica:

```text
RoleActivated
```

## Cuando

El Projector procesa el evento.

## Entonces

El Read Model refleja:

```text
Status = Active
```

---

# Cobertura Esperada

Las pruebas deben cubrir:

- creación;
- modificaciones;
- transiciones de estado;
- validación de invariantes;
- permisos;
- concurrencia;
- persistencia;
- reconstrucción;
- generación de Domain Events;
- actualización del Read Model.

---

# Criterios de Aceptación

El Aggregate será considerado conforme cuando:

- todos los Commands válidos finalicen correctamente;
- todos los Commands inválidos sean rechazados;
- todas las invariantes permanezcan satisfechas;
- todos los Domain Events sean emitidos correctamente;
- la versión evolucione de forma monotónica;
- el Repository preserve la consistencia del Aggregate;
- el Read Model refleje correctamente los cambios publicados.

---

# Compatibilidad Arquitectónica

Los escenarios son compatibles con:

- Domain-Driven Design (DDD);
- Test-Driven Development (TDD);
- Behavior-Driven Development (BDD);
- CQRS;
- Event Sourcing;
- Clean Architecture.

---

# Definición de Éxito

Los escenarios de prueba del Aggregate **Role** constituyen la especificación verificable del comportamiento esperado del dominio. Su ejecución garantiza que la gestión de cargos organizacionales preserve las invariantes, mantenga la consistencia transaccional y produzca una evolución predecible y auditable del Aggregate dentro de la arquitectura AURA.