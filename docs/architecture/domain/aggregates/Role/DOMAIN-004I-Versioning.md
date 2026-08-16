# DOMAIN-004I — Role Versioning

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
- DOMAIN-004G-Repository-Contract.md
- DOMAIN-004J-Consistency-Boundary.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Este documento define el modelo oficial de versionado del
Aggregate **Role**.

El versionado garantiza el control de concurrencia optimista,
permite detectar modificaciones simultáneas y asegura la
consistencia del Aggregate durante todo su ciclo de vida.

---

# Principios

El modelo de versionado sigue los siguientes principios:

- una única versión por Aggregate;
- incremento monotónico;
- control de concurrencia optimista;
- independencia de la tecnología de persistencia;
- trazabilidad completa;
- compatibilidad con Event Sourcing.

---

# Atributo Version

Todo Aggregate Role posee el atributo:

```text
Version
```

Características:

- entero positivo;
- obligatorio;
- administrado exclusivamente por el dominio;
- nunca editable por usuarios;
- nunca disminuye.

---

# Inicialización

Al crear un Role:

```text
CreateRole
```

Resultado:

```text
Version = 1
```

Evento generado:

```text
RoleCreated
```

---

# Incremento de Versión

Cada modificación válida incrementa exactamente una unidad.

Ejemplo:

```text
Version = 3

↓

RenameRole

↓

Version = 4
```

---

# Commands que Incrementan la Versión

| Command | Incrementa Version |
|----------|:------------------:|
| CreateRole | ✓ |
| RenameRole | ✓ |
| ChangeDescription | ✓ |
| ActivateRole | ✓ |
| DeactivateRole | ✓ |
| ArchiveRole | ✓ |

---

# Commands Rechazados

Cuando un Command es rechazado:

- la versión permanece inalterada;
- no se generan Domain Events;
- el Aggregate conserva su estado.

Ejemplo:

```text
Version = 5

↓

RenameRole

↓

DuplicateRoleName

↓

Version = 5
```

---

# Concurrencia Optimista

Antes de persistir cambios se compara:

```text
ExpectedVersion

↓

CurrentVersion
```

Si ambas coinciden:

```text
Persist Aggregate

↓

Version + 1
```

Si no coinciden:

```text
ConcurrencyConflict
```

---

# Flujo de Persistencia

```text
Load Aggregate

↓

Read Version

↓

Validate Version

↓

Execute Command

↓

Increment Version

↓

Persist Aggregate

↓

Publish Domain Events
```

Todo el proceso debe ejecutarse dentro de una única transacción.

---

# Ejemplo de Concurrencia

Estado inicial:

```text
Role

Version = 8
```

Usuario A:

```text
RenameRole
```

Resultado:

```text
Version = 9
```

Usuario B intenta guardar utilizando:

```text
ExpectedVersion = 8
```

Resultado:

```text
ConcurrencyConflict
```

El segundo cambio es rechazado.

---

# Relación con Domain Events

Cada Domain Event registra la versión resultante del Aggregate.

Ejemplo:

```text
RoleActivated

Version = 4
```

Esto permite reconstruir la evolución exacta del Aggregate.

---

# Relación con Event Sourcing

Cuando Event Sourcing está habilitado:

```text
Version
```

corresponde al número de eventos aplicados sobre el Aggregate.

Ejemplo:

```text
RoleCreated

Version = 1

↓

RoleActivated

Version = 2

↓

RoleRenamed

Version = 3

↓

RoleArchived

Version = 4
```

---

# Recuperación

Al recuperar un Aggregate desde el Repository:

```text
FindById()

↓

Role

↓

Version
```

La versión debe reflejar el último cambio persistido.

---

# Auditoría

Cada modificación registra conceptualmente:

```text
AggregateId

Version

OccurredOn

ActorId

CorrelationId

CausationId
```

Esta información permite reconstruir cualquier estado histórico.

---

# Reglas

Las siguientes reglas son obligatorias:

- la versión nunca puede ser negativa;
- la versión nunca puede disminuir;
- la versión nunca puede reiniciarse;
- sólo aumenta después de una modificación exitosa;
- no puede modificarse manualmente.

---

# Errores Asociados

| Situación | Resultado |
|-----------|-----------|
| Versión desactualizada | ConcurrencyConflict |
| Aggregate inexistente | RoleNotFound |
| Persistencia parcial | TransactionRollback |

---

# Compatibilidad Arquitectónica

El modelo de versionado es compatible con:

- Domain-Driven Design (DDD);
- Optimistic Concurrency Control;
- Repository Pattern;
- CQRS;
- Event Sourcing;
- Clean Architecture.

---

# Definición de Éxito

El modelo de versionado del Aggregate **Role** garantiza que toda modificación sea consistente, auditable y segura frente a accesos concurrentes. La utilización de concurrencia optimista, junto con el incremento monotónico de la versión y su integración con los Domain Events, proporciona una base sólida para preservar la integridad del dominio y la evolución controlada de los Roles dentro del ecosistema AURA.