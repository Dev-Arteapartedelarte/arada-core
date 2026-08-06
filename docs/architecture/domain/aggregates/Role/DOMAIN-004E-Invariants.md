# DOMAIN-004E — Role Invariants

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
- DOMAIN-004F-Permissions.md
- DOMAIN-004J-Consistency-Boundary.md

---

# Objetivo

Este documento define las **invariantes oficiales** del
Aggregate **Role**.

Las invariantes representan reglas de negocio que deben
cumplirse en todo momento. Ningún Command puede dejar el
Aggregate en un estado que viole cualquiera de estas reglas.

---

# Principios

Las invariantes del Aggregate cumplen los siguientes principios:

- son permanentes;
- son independientes de la infraestructura;
- protegen la consistencia del dominio;
- se validan antes de persistir cambios;
- nunca pueden omitirse.

---

# Invariante 1 — Identidad Inmutable

Todo Role posee un identificador único.

```text
RoleId
```

Una vez creado:

- nunca cambia;
- nunca se reutiliza;
- nunca puede ser reemplazado.

---

# Invariante 2 — Organización Inmutable

Cada Role pertenece exactamente a una Organization.

```text
OrganizationId
```

Después de la creación:

- no puede modificarse;
- no puede reasignarse;
- no puede pertenecer simultáneamente a varias organizaciones.

---

# Invariante 3 — Nombre Único

Dentro de una misma Organization no pueden existir dos Roles
activos con el mismo nombre.

Ejemplo válido:

```text
Organization A

Presidente

Secretario

Tesorero
```

Ejemplo inválido:

```text
Organization A

Presidente

Presidente
```

Resultado:

```text
DuplicateRoleName
```

---

# Invariante 4 — Código Único

El atributo:

```text
Code
```

debe ser único dentro de la Organization.

Ejemplo:

```text
PRESIDENT

SECRETARY

TREASURER
```

No pueden repetirse.

---

# Invariante 5 — Nombre Obligatorio

Todo Role debe poseer un nombre válido.

No se permite:

```text
""
```

```text
NULL
```

```text
"   "
```

---

# Invariante 6 — Código Obligatorio

Todo Role debe poseer un código estable.

No se permiten:

- valores vacíos;
- valores nulos;
- códigos duplicados.

---

# Invariante 7 — Estado Válido

El estado únicamente puede tomar uno de los siguientes valores:

```text
Draft

Active

Inactive

Archived
```

No existen estados adicionales.

---

# Invariante 8 — Transiciones Controladas

Toda transición debe respetar la máquina de estados.

Ejemplos inválidos:

```text
Archived

↓

ActivateRole
```

```text
Active

↓

ActivateRole
```

Resultado:

```text
InvalidStateTransition
```

---

# Invariante 9 — Roles Archivados

Cuando:

```text
Status = Archived
```

el Aggregate pasa a ser de solo lectura.

No puede:

- cambiar nombre;
- cambiar descripción;
- activarse;
- desactivarse;
- recibir nuevas modificaciones.

---

# Invariante 10 — Roles Activos

Solo un Role en estado:

```text
Active
```

puede ser asignado a nuevas Memberships.

Los Roles en estado:

```text
Draft

Inactive

Archived
```

no pueden utilizarse para nuevas asignaciones.

---

# Invariante 11 — Protección de System Roles

Cuando:

```text
IsSystemRole = true
```

se aplican restricciones adicionales.

Dependiendo de la política del dominio:

- no puede archivarse;
- no puede eliminarse;
- el nombre puede ser inmutable;
- el código puede ser inmutable.

Estas restricciones protegen los Roles fundamentales del sistema.

---

# Invariante 12 — Versionado

Toda modificación válida incrementa:

```text
Version
```

La versión:

- nunca disminuye;
- nunca se reinicia;
- nunca se modifica manualmente.

---

# Invariante 13 — Eventos

Toda modificación válida genera los Domain Events
correspondientes.

No pueden existir:

- cambios sin eventos;
- eventos sin cambios efectivos.

---

# Invariante 14 — Consistencia Transaccional

Toda operación debe ejecutarse completamente o no ejecutarse.

Nunca pueden persistirse:

- cambios parciales;
- eventos parciales;
- versiones inconsistentes.

---

# Invariante 15 — Integridad Referencial

Un Role sólo puede existir asociado a una Organization válida.

No pueden existir Roles huérfanos.

---

# Invariante 16 — Independencia del Aggregate

El Aggregate Role no mantiene referencias directas a:

- Citizen;
- Membership;
- Permission;
- Committee;
- Assembly.

La relación con otros Aggregates se realiza mediante sus
identificadores y servicios de aplicación.

---

# Validación de Invariantes

Antes de ejecutar un Command:

```text
Load Aggregate

↓

Validate State

↓

Validate Invariants

↓

Execute Command

↓

Persist

↓

Publish Events
```

Si alguna invariante falla:

```text
Command Rejected
```

---

# Violaciones Típicas

| Situación | Error |
|-----------|-------|
| Nombre duplicado | DuplicateRoleName |
| Código duplicado | DuplicateRoleCode |
| Estado inválido | InvalidStateTransition |
| Organización inexistente | OrganizationNotFound |
| Rol archivado modificado | ArchivedRoleModification |
| Conflicto de versión | ConcurrencyConflict |

---

# Compatibilidad Arquitectónica

Las invariantes son compatibles con:

- Domain-Driven Design (DDD);
- Clean Architecture;
- CQRS;
- Event Sourcing;
- Event-Driven Architecture.

---

# Definición de Éxito

Las invariantes del Aggregate **Role** garantizan que toda
función organizacional mantenga una identidad única, una
pertenencia inequívoca a una **Organization** y un ciclo de vida
consistente. Estas reglas constituyen el mecanismo fundamental
para preservar la integridad del dominio y asegurar que la
gestión de cargos organizacionales evolucione de forma segura,
predecible y auditable dentro del ecosistema AURA.