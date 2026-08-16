# DOMAIN-004 — Role Aggregate

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

- DOMAIN-003-Aggregate.md
- DOMAIN-003F-Permissions.md
- CORE-004-Ubiquitous-Language.md
- CORE-002-Bounded-Context-Map.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

El Aggregate **Role** representa una función organizacional
dentro de una **Organization**.

Un Role define una función organizacional disponible en el catálogo de
una Organization. No representa personas ni permisos técnicos. La
asignación Membership–Role no forma parte del baseline 1.0.

Ejemplos:

- Presidente
- Vicepresidente
- Secretario
- Tesorero
- Director
- Coordinador
- Moderador
- Socio
- Voluntario

---

# Responsabilidad

El Aggregate Role es responsable de:

- definir Roles organizacionales;
- administrar su ciclo de vida;
- garantizar unicidad dentro de una Organization;
- emitir Domain Events;
- preservar las invariantes del dominio.

No es responsable de:

- autenticar usuarios;
- administrar credenciales;
- asignar permisos técnicos;
- gestionar Memberships;
- controlar sesiones.

---

# Modelo Conceptual

```text
OrganizationId -> Role
```

Una Organization posee un catálogo de Roles. El Aggregate Role no conoce
Memberships y no administra asignaciones.

---

# Identidad

Cada Role posee una identidad única e inmutable:

```text
RoleId
```

Esta identidad permanece constante durante toda su existencia.

---

# Atributos Conceptuales

```text
RoleId

OrganizationId

Name

Code

Description

RoleType

Status

IsSystemRole

CreatedAt

UpdatedAt

ArchivedAt

Version
```

---

# Descripción de Atributos

## RoleId

Identificador único del Aggregate.

---

## OrganizationId

Organización propietaria del Role.

Nunca cambia.

---

## Name

Nombre visible del Role.

Ejemplos:

```text
Presidente

Secretario

Tesorero

Socio
```

Debe ser único dentro de la misma Organization.

---

## Code

Código interno estable.

Ejemplos:

```text
PRESIDENT

SECRETARY

TREASURER

MEMBER
```

Utilizado para integraciones y referencias técnicas.

---

## Description

Descripción funcional del Role.

Opcional.

---

## RoleType

Clasificación conceptual.

Ejemplos:

```text
Governance

Operational

Administrative

Honorary

Technical
```

Permite agrupar Roles sin afectar su identidad.

---

## Status

Estado actual del Role.

Valores posibles:

```text
Draft

Active

Inactive

Archived
```

---

## IsSystemRole

Indica si el Role es provisto por el sistema.

```text
true

false
```

Los System Roles poseen restricciones especiales.

---

## CreatedAt

Fecha de creación.

---

## UpdatedAt

Última modificación.

---

## ArchivedAt

Fecha de archivado.

Puede ser nula.

---

## Version

Número de versión utilizado para concurrencia optimista.

---

# Aggregate Root

El Aggregate Root es:

```text
Role
```

Toda modificación debe realizarse exclusivamente mediante esta
raíz.

No existen modificaciones directas sobre sus atributos.

---

# Invariantes Iniciales

El Aggregate garantiza, como mínimo:

- RoleId único;
- Name único dentro de una Organization;
- Code único dentro de una Organization;
- OrganizationId inmutable;
- Version creciente;
- transición válida de estados;
- imposibilidad de modificar Roles archivados;
- los Roles del sistema no pueden eliminarse.

Las invariantes se desarrollarán formalmente en
**DOMAIN-004E-Invariants.md**.

---

# Relaciones

## Organization

Cada Role pertenece exactamente a una Organization.

La relación se mantiene mediante:

```text
OrganizationId
```

---

## Membership

Role no mantiene MembershipIds. La eventual asignación entre ambos
conceptos requiere un Source of Truth y contratos aún no definidos.

---

## Permission

Permission es una capacidad explícita requerida por un Command. Role no
almacena, agrupa ni concede Permissions.

---

# Consistencia

El Aggregate constituye un único límite de consistencia.

Todas las modificaciones sobre un Role ocurren dentro de una
única transacción.

---

# Persistencia

El Repository persiste el Aggregate completo como una unidad.

Nunca se persisten partes del Aggregate de forma independiente.

---

# Eventos

Ejemplos de Domain Events:

```text
RoleCreated

RoleActivated

RoleRenamed

RoleDescriptionChanged

RoleArchived

SystemRoleProtected
```

La definición formal se documentará en
**DOMAIN-004D-Domain-Events.md**.

---

# Casos de Uso

Ejemplos:

```text
Crear nuevo cargo directivo.

Activar un cargo.

Cambiar la descripción de un cargo.

Archivar un cargo obsoleto.

```

---

# Restricciones

No está permitido:

- duplicar Name en una misma Organization;
- duplicar Code en una misma Organization;
- modificar OrganizationId;
- modificar RoleId;
- eliminar un System Role;
- tratar un Role archivado como referencia activa del catálogo.

---

# Compatibilidad Arquitectónica

El Aggregate es compatible con:

- Domain-Driven Design (DDD);
- Hexagonal Architecture;
- CQRS;
- Event Sourcing;
- Event-Driven Architecture.

---

# Definición de Éxito

El Aggregate **Role** constituye el modelo oficial para
representar funciones organizacionales dentro de AURA. Su diseño
garantiza una definición consistente de los cargos existentes en
cada **Organization**, desacoplándolos de las personas que los
ejercen y proporcionando la base para el modelo de autorización,
la asignación de responsabilidades y la futura gestión de
permisos del ecosistema.