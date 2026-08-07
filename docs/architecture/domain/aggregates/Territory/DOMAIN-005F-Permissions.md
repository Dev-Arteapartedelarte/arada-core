# DOMAIN-005F — Territory Permissions

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Territorial Management

Aggregate:
Territory

Documentos relacionados:

- DOMAIN-005-Aggregate.md
- DOMAIN-005A-Lifecycle.md
- DOMAIN-005B-State-Machine.md
- DOMAIN-005C-Commands.md
- DOMAIN-005D-Domain-Events.md
- DOMAIN-005E-Invariants.md
- DOMAIN-005G-Repository-Contract.md
- DOMAIN-005O-Security-Model.md

---

# Objetivo

Definir las reglas de autorización que determinan qué actores
pueden ejecutar Commands sobre el Aggregate **Territory**.

Este documento establece la relación entre:

```text
Actor
    ↓
Permission
    ↓
Command
    ↓
Territory
```

Las permissions no modifican el Aggregate.

Su función es determinar si una determinada operación puede ser
intentada por un actor dentro del contexto correspondiente.

---

# Principios

Las autorizaciones de Territory deben cumplir:

- mínimo privilegio;
- separación de responsabilidades;
- trazabilidad;
- pertenencia al contexto organizacional;
- respeto por el estado del Aggregate;
- independencia entre autorización y persistencia;
- prohibición de bypass del Aggregate Root.

Una autorización válida nunca permite modificar directamente
los atributos internos del Aggregate.

---

# Actor

Un actor representa la identidad que intenta ejecutar una
operación.

Puede corresponder a:

```text
Citizen

Representative

OrganizationMember

OrganizationAdministrator

TerritorialAdministrator

MunicipalAuthority

SystemActor
```

La identidad concreta del actor pertenece al modelo de
seguridad y aplicación.

Territory sólo recibe el contexto de autorización necesario
para aceptar o rechazar la operación.

---

# Contexto Organizacional

Cuando una operación se realiza dentro de una Organization,
el actor debe poseer una relación válida con dicha
Organization.

La autorización debe considerar:

```text
ActorId

OrganizationId

TerritoryId

Permission

Command
```

Una membership inválida o inexistente no puede utilizarse para
obtener permisos organizacionales.

---

# Permission Model

Las permissions principales de Territory son:

```text
territory.create

territory.read

territory.validate

territory.update

territory.activate

territory.deactivate

territory.archive

territory.change_parent

territory.change_geometry

territory.change_administrative_code
```

Las permissions representan capacidades.

No representan estados.

---

# territory.create

Permite solicitar la creación de un Territory.

Puede utilizarse para:

```text
CreateTerritory
```

Condiciones:

- actor autenticado;
- actor autorizado en el contexto correspondiente;
- datos mínimos válidos.

Resultado esperado:

```text
Territory → Draft
```

---

# territory.read

Permite consultar información de Territory.

Puede utilizarse para:

- obtener información territorial;
- consultar estado;
- consultar jerarquía;
- consultar metadatos.

La lectura no modifica el Aggregate.

---

# territory.validate

Permite ejecutar operaciones relacionadas con la validación
territorial.

Commands asociados:

```text
RequestTerritoryValidation

ApproveTerritory

RejectTerritory
```

El actor debe poseer una capacidad de validación compatible con
su rol dentro del contexto territorial.

---

# territory.update

Permite modificar información editable del Territory.

Puede cubrir:

```text
RenameTerritory

ChangeTerritoryType

UpdateTerritoryMetadata
```

No incluye automáticamente operaciones administrativas
especiales.

---

# territory.activate

Permite activar un Territory cuando las condiciones del
dominio han sido satisfechas.

Command:

```text
ActivateTerritory
```

La permission no reemplaza las invariantes.

Aunque el actor posea:

```text
territory.activate
```

la operación debe ser rechazada si el estado actual no permite
la transición.

---

# territory.deactivate

Permite desactivar temporalmente un Territory.

Command:

```text
DeactivateTerritory
```

Estado requerido:

```text
Active
```

Resultado:

```text
Inactive
```

---

# territory.archive

Permite solicitar el archivado de un Territory.

Command:

```text
ArchiveTerritory
```

Estados desde los cuales puede ejecutarse:

```text
Active

Inactive
```

El archivado es una operación administrativa de alto impacto y
debe estar restringido a actores autorizados.

---

# territory.change_parent

Permite modificar la relación jerárquica del Territory.

Command:

```text
ChangeParentTerritory
```

La autorización no elimina las validaciones de:

- existencia del padre;
- autorreferencia;
- ciclos;
- compatibilidad jerárquica.

---

# territory.change_geometry

Permite modificar la referencia geográfica.

Command:

```text
ChangeGeometry
```

El actor debe poseer autorización territorial suficiente.

La operación debe además cumplir las reglas geográficas del
dominio.

---

# territory.change_administrative_code

Permite modificar el código administrativo.

Command:

```text
ChangeAdministrativeCode
```

Esta permission debe considerarse de carácter administrativo.

La operación requiere además:

- código válido;
- unicidad;
- compatibilidad con el tipo territorial;
- autorización correspondiente.

---

# Matriz Permission → Command

| Permission | Command |
|---|---|
| `territory.create` | CreateTerritory |
| `territory.read` | consulta |
| `territory.validate` | RequestTerritoryValidation |
| `territory.validate` | ApproveTerritory |
| `territory.validate` | RejectTerritory |
| `territory.update` | RenameTerritory |
| `territory.update` | ChangeTerritoryType |
| `territory.update` | UpdateTerritoryMetadata |
| `territory.activate` | ActivateTerritory |
| `territory.deactivate` | DeactivateTerritory |
| `territory.archive` | ArchiveTerritory |
| `territory.change_parent` | ChangeParentTerritory |
| `territory.change_geometry` | ChangeGeometry |
| `territory.change_administrative_code` | ChangeAdministrativeCode |

---

# Permission ≠ Invariant

Una permission responde:

```text
¿Este actor puede intentar esta operación?
```

Una invariant responde:

```text
¿Esta operación puede mantener el Aggregate consistente?
```

Ambas condiciones deben cumplirse.

```text
Authorization
      │
      ▼
Permission Check
      │
      ▼
Invariant Check
      │
      ▼
State Transition
```

Poseer una permission nunca permite violar una invariant.

---

# Permission ≠ State Transition

Una permission tampoco concede automáticamente una transición.

Por ejemplo:

```text
territory.archive
```

no significa que cualquier Territory pueda ser archivado.

Debe cumplirse simultáneamente:

```text
Permission válida
        +
Estado permitido
        +
Invariantes satisfechas
        =
Operación válida
```

---

# Estado y Permissions

## Draft

Puede permitir:

```text
read
update
change_parent
change_geometry
change_administrative_code
```

y, según el contexto:

```text
validate
```

---

## PendingValidation

Puede permitir:

```text
read
validate
```

Las modificaciones estructurales deben permanecer restringidas
mientras el territorio se encuentra en validación.

---

## Active

Puede permitir:

```text
read
update
change_parent
change_geometry
change_administrative_code
deactivate
archive
```

---

## Inactive

Puede permitir:

```text
read
activate
archive
update
```

Las modificaciones estructurales deben evaluarse según las
reglas específicas del dominio.

---

## Archived

Sólo:

```text
read
```

No se permiten Commands de modificación.

---

# Separación de Responsabilidades

Las siguientes capacidades deben poder separarse:

```text
TerritoryEditor

TerritoryValidator

TerritoryAdministrator

TerritoryArchivist
```

No es obligatorio que una persona posea todas ellas.

La asignación concreta de estas capacidades corresponde al
modelo de autorización de AURA.

---

# Principio de Mínimo Privilegio

Un actor debe recibir únicamente las permissions necesarias
para cumplir su función.

Ejemplo:

```text
TerritoryReader
    → territory.read
```

```text
TerritoryEditor
    → territory.read
    → territory.update
```

```text
TerritoryValidator
    → territory.read
    → territory.validate
```

```text
TerritoryAdministrator
    → permissions territoriales administrativas
```

Los conjuntos anteriores son ejemplos conceptuales y no
constituyen roles obligatorios del dominio.

---

# Cross-Organization Access

Una permission obtenida dentro de una Organization no concede
automáticamente acceso sobre cualquier Territory.

Debe verificarse el contexto de acceso:

```text
Actor
  +
Organization
  +
Territory
  +
Permission
```

El alcance territorial debe ser compatible con la autoridad
del actor.

---

# System Actors

Los procesos automatizados pueden actuar mediante:

```text
SystemActor
```

Un SystemActor debe poseer permissions explícitas.

No se permite asumir:

```text
SystemActor = Administrator
```

por defecto.

---

# Denegación

Una operación debe ser rechazada cuando:

- el actor no está autenticado;
- no posee la permission requerida;
- la permission no corresponde al Command;
- el actor no tiene alcance sobre el Territory;
- la Organization asociada no es válida;
- el estado del Territory no permite la operación;
- una invariant es violada.

La denegación no modifica el Aggregate.

---

# Auditoría de Autorización

Toda operación administrativa debe permitir registrar:

```text
ActorId

OrganizationId

TerritoryId

Permission

Command

AuthorizationResult

OccurredOn

CorrelationId

CausationId
```

Ejemplo:

```text
Actor:
actor-123

Permission:
territory.archive

Command:
ArchiveTerritory

AuthorizationResult:
Denied
```

---

# Seguridad y Dominio

La capa de autorización puede utilizar mecanismos externos,
pero el Aggregate debe permanecer protegido contra operaciones
inválidas.

La arquitectura debe mantener:

```text
Authentication
       ↓
Authorization
       ↓
Application
       ↓
Domain
       ↓
Aggregate
```

El dominio no debe depender de un framework concreto de
autenticación.

---

# Regla Fundamental

La autorización nunca sustituye las reglas del dominio.

La operación sólo puede ejecutarse cuando:

```text
Actor autenticado
        +
Permission válida
        +
Contexto válido
        +
Estado permitido
        +
Invariantes satisfechas
        =
Command aceptado
```

---

# Compatibilidad

El modelo de Permissions es compatible con:

- Domain-Driven Design (DDD);
- Role-Based Access Control (RBAC);
- Attribute-Based Access Control (ABAC);
- Clean Architecture;
- CQRS;
- Event-Driven Architecture.

La implementación concreta del mecanismo de autorización queda
fuera del Aggregate.

---

# Definición de Éxito

El modelo de Permissions del Aggregate **Territory** garantiza
que cada operación sea ejecutada únicamente por actores con la
capacidad y el alcance adecuados, manteniendo separadas las
responsabilidades de autenticación, autorización y reglas de
dominio.

Ninguna permission puede modificar directamente el Aggregate ni
puede utilizarse para eludir sus invariantes, transiciones de
estado o límites de consistencia.