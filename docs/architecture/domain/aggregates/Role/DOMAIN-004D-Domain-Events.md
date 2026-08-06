# DOMAIN-004D — Role Domain Events

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
- DOMAIN-004E-Invariants.md
- DOMAIN-004K-Integration-Events.md
- CORE-009-Domain-Events.md

---

# Objetivo

Este documento define los **Domain Events** oficiales del
Aggregate **Role**.

Los Domain Events representan hechos de negocio que ya han
ocurrido dentro del dominio. Son inmutables, forman parte del
lenguaje ubicuo y permiten que otros componentes reaccionen ante
cambios relevantes sin acoplarse al Aggregate.

---

# Principios

Los Domain Events cumplen los siguientes principios:

- representan hechos consumados;
- son inmutables;
- describen eventos del dominio, no acciones técnicas;
- se publican únicamente después de una transacción exitosa;
- preservan la independencia entre Aggregates.

---

# Eventos Oficiales

| Domain Event | Descripción |
|--------------|-------------|
| RoleCreated | Se creó un nuevo Role |
| RoleRenamed | Se modificó el nombre del Role |
| RoleDescriptionChanged | Se modificó la descripción |
| RoleActivated | El Role fue activado |
| RoleDeactivated | El Role fue desactivado |
| RoleArchived | El Role fue archivado |

---

# Evento: RoleCreated

## Descripción

Indica que un nuevo Role fue creado correctamente.

## Originado por

```text
CreateRole
```

## Payload conceptual

```text
RoleId

OrganizationId

Name

Code

RoleType

IsSystemRole

OccurredOn

Version
```

---

# Evento: RoleRenamed

## Descripción

Indica que el nombre visible del Role fue modificado.

## Originado por

```text
RenameRole
```

## Payload conceptual

```text
RoleId

OldName

NewName

OccurredOn

Version
```

---

# Evento: RoleDescriptionChanged

## Descripción

Indica que la descripción funcional fue actualizada.

## Originado por

```text
ChangeDescription
```

## Payload conceptual

```text
RoleId

OccurredOn

Version
```

La descripción anterior y la nueva pueden mantenerse en la
auditoría si así lo requiere la implementación.

---

# Evento: RoleActivated

## Descripción

El Role quedó disponible para ser utilizado dentro de la
Organization.

## Originado por

```text
ActivateRole
```

## Payload conceptual

```text
RoleId

OrganizationId

OccurredOn

Version
```

---

# Evento: RoleDeactivated

## Descripción

El Role dejó de estar disponible para nuevas asignaciones.

## Originado por

```text
DeactivateRole
```

## Payload conceptual

```text
RoleId

OccurredOn

Version
```

---

# Evento: RoleArchived

## Descripción

El ciclo de vida del Role finalizó.

## Originado por

```text
ArchiveRole
```

## Payload conceptual

```text
RoleId

OccurredOn

Version
```

---

# Secuencia de Eventos

Un ciclo de vida típico genera la siguiente secuencia:

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

Cada evento representa un hecho irreversible del dominio.

---

# Reglas de Publicación

Los Domain Events se publican únicamente cuando:

- el Command finaliza correctamente;
- la transacción es confirmada;
- el Aggregate queda en un estado consistente.

No deben emitirse eventos durante validaciones fallidas.

---

# Inmutabilidad

Una vez publicado, un Domain Event:

- no puede modificarse;
- no puede eliminarse;
- no puede reutilizarse;
- conserva su identidad para auditoría y reconstrucción.

---

# Relación con Event Sourcing

Cuando Event Sourcing está habilitado, los Domain Events
constituyen la fuente oficial para reconstruir el Aggregate.

Ejemplo:

```text
RoleCreated

↓

RoleActivated

↓

RoleRenamed

↓

RoleArchived
```

Aplicando los eventos en orden cronológico se reconstruye el
estado exacto del Aggregate.

---

# Relación con Integration Events

Los Domain Events permanecen dentro del Bounded Context.

Cuando un evento debe ser compartido con otros Contextos se
transforma en un **Integration Event**, definido en:

```text
DOMAIN-004K-Integration-Events.md
```

Ejemplo:

```text
RoleActivated

↓

RoleActivatedIntegrationEvent
```

---

# Auditoría

Todo Domain Event debe registrar conceptualmente:

```text
EventId

AggregateId

AggregateType

AggregateVersion

OccurredOn

CorrelationId

CausationId
```

Estos datos permiten reconstrucción histórica y trazabilidad.

---

# Compatibilidad Arquitectónica

El modelo es compatible con:

- Domain-Driven Design (DDD);
- Event-Driven Architecture (EDA);
- CQRS;
- Event Sourcing;
- Clean Architecture.

---

# Definición de Éxito

Los Domain Events del Aggregate **Role** representan de manera
precisa y auditable la evolución de las funciones
organizacionales dentro de AURA. Su diseño desacoplado permite
la integración con otros Bounded Contexts, facilita la
reconstrucción del estado mediante Event Sourcing y constituye
la base para mecanismos de auditoría, analítica e integración
sin comprometer la pureza del dominio.