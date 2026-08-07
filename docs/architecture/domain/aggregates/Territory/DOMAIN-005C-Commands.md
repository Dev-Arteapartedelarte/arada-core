# DOMAIN-005C — Territory Commands

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
- DOMAIN-005D-Domain-Events.md
- DOMAIN-005E-Invariants.md
- DOMAIN-005F-Permissions.md
- DOMAIN-005J-Consistency-Boundary.md

---

# Objetivo

Definir los Commands que representan la intención de modificar
el estado del Aggregate **Territory**.

Un Command expresa una solicitud de cambio. No representa un
hecho consumado y no garantiza su ejecución. Antes de ser
aceptado debe superar todas las validaciones de negocio,
permisos e invariantes del Aggregate.

---

# Principios

Todos los Commands deben cumplir los siguientes principios:

- representan una intención de cambio;
- modifican un único Aggregate;
- son inmutables;
- poseen identidad propia;
- son auditables;
- pueden generar uno o más Domain Events;
- nunca retornan el estado del Aggregate.

---

# Estructura General

Todo Command debe contener, como mínimo:

```text
CommandId

TerritoryId

OrganizationId

ActorId

Timestamp

CorrelationId

CausationId
```

Campos específicos pueden añadirse según la operación.

---

# CreateTerritory

## Objetivo

Crear un nuevo territorio.

## Datos mínimos

```text
OrganizationId

TerritoryName

TerritoryType

AdministrativeCode

ParentTerritoryId (opcional)

GeometryReference (opcional)
```

## Precondiciones

- Organization existe.
- El nombre es válido.
- El tipo es válido.
- El código administrativo no está duplicado.
- El actor posee permisos de creación.

## Estado origen

No aplica.

## Estado destino

```text
Draft
```

## Evento esperado

```text
TerritoryCreated
```

---

# RequestTerritoryValidation

## Objetivo

Solicitar la validación del territorio.

## Estado origen

```text
Draft
```

## Estado destino

```text
PendingValidation
```

## Evento esperado

```text
TerritoryValidationRequested
```

---

# ApproveTerritory

## Objetivo

Aprobar un territorio validado.

## Estado origen

```text
PendingValidation
```

## Estado destino

```text
Active
```

## Evento esperado

```text
TerritoryValidated

TerritoryActivated
```

---

# RejectTerritory

## Objetivo

Rechazar el proceso de validación.

## Estado origen

```text
PendingValidation
```

## Estado destino

```text
Draft
```

## Evento esperado

```text
TerritoryValidationRejected
```

---

# RenameTerritory

## Objetivo

Modificar el nombre del territorio.

## Datos

```text
TerritoryName
```

## Estados permitidos

```text
Draft

Active
```

## Evento esperado

```text
TerritoryRenamed
```

---

# ChangeTerritoryType

## Objetivo

Modificar la clasificación territorial.

## Datos

```text
TerritoryType
```

## Estados permitidos

```text
Draft

Active
```

## Evento esperado

```text
TerritoryTypeChanged
```

---

# ChangeAdministrativeCode

## Objetivo

Actualizar el código administrativo.

## Datos

```text
AdministrativeCode
```

## Estados permitidos

```text
Draft

Active
```

## Evento esperado

```text
AdministrativeCodeChanged
```

---

# ChangeGeometry

## Objetivo

Actualizar la referencia geográfica del territorio.

## Datos

```text
GeometryReference
```

## Estados permitidos

```text
Draft

Active
```

## Evento esperado

```text
TerritoryGeometryChanged
```

---

# ChangeParentTerritory

## Objetivo

Modificar la jerarquía territorial.

## Datos

```text
ParentTerritoryId
```

## Validaciones

- el territorio padre existe;
- no existen ciclos;
- no puede referenciarse a sí mismo.

## Estados permitidos

```text
Draft

Active
```

## Evento esperado

```text
TerritoryParentChanged
```

---

# UpdateTerritoryMetadata

## Objetivo

Actualizar metadatos no estructurales.

## Estados permitidos

```text
Draft

PendingValidation

Active

Inactive
```

## Evento esperado

```text
TerritoryMetadataUpdated
```

---

# DeactivateTerritory

## Objetivo

Suspender temporalmente el territorio.

## Estado origen

```text
Active
```

## Estado destino

```text
Inactive
```

## Evento esperado

```text
TerritoryDeactivated
```

---

# ActivateTerritory

## Objetivo

Reactivar un territorio suspendido.

## Estado origen

```text
Inactive
```

## Estado destino

```text
Active
```

## Evento esperado

```text
TerritoryActivated
```

---

# ArchiveTerritory

## Objetivo

Archivar definitivamente el Aggregate.

## Estados permitidos

```text
Active

Inactive
```

## Estado destino

```text
Archived
```

## Evento esperado

```text
TerritoryArchived
```

---

# Rechazo de Commands

El Aggregate rechazará un Command cuando ocurra cualquiera de
las siguientes situaciones:

- el TerritoryId no existe;
- el estado actual no permite la operación;
- el actor no posee permisos;
- se violan invariantes del dominio;
- existe un código administrativo duplicado;
- la jerarquía territorial produce ciclos;
- el Aggregate se encuentra archivado.

En estos casos no se modifica el estado y no se publica ningún
Domain Event.

---

# Consistencia

Cada Command debe:

- modificar exclusivamente un Aggregate;
- ejecutarse dentro de una única transacción;
- preservar todas las invariantes;
- producir únicamente eventos válidos del dominio.

---

# Auditoría

Todo Command registra:

```text
CommandId

TerritoryId

OrganizationId

ActorId

Timestamp

CorrelationId

CausationId
```

Estos registros forman parte de la trazabilidad completa del
Aggregate.

---

# Compatibilidad

El modelo de Commands es compatible con:

- Domain-Driven Design (DDD);
- CQRS;
- Clean Architecture;
- Event Sourcing;
- Event-Driven Architecture.

---

# Definición de Éxito

Los Commands del Aggregate **Territory** constituyen el único
mecanismo autorizado para solicitar cambios de estado sobre un
territorio. Cada operación expresa una intención explícita,
preserva las invariantes del dominio, mantiene la consistencia
transaccional y permite una trazabilidad completa mediante
eventos y auditoría.