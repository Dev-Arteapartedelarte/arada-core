# DOMAIN-011G — Notification Repository Contract

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Notification Management

Aggregate:
Notification

Documentos relacionados:

- DOMAIN-011-Aggregate.md
- DOMAIN-011C-Commands.md
- DOMAIN-011D-Domain-Events.md
- DOMAIN-011E-Invariants.md
- CORE-011-Repository-Contracts.md

---

# Objetivo

Este documento define el contrato oficial del Repository del
Aggregate **Notification**.

El Repository constituye el único mecanismo autorizado para
persistir y recuperar Aggregates desde el dominio. Su propósito
es abstraer completamente la tecnología de almacenamiento,
permitiendo que el dominio permanezca independiente de bases
de datos, ORM, APIs o cualquier infraestructura externa.

El Repository nunca implementa reglas de negocio; únicamente
proporciona acceso consistente a los Aggregates.

---

# Responsabilidades

El Repository es responsable de:

- recuperar un Aggregate por su identidad;
- persistir cambios del Aggregate;
- garantizar consistencia transaccional;
- aplicar control de concurrencia;
- abstraer el mecanismo de almacenamiento.

No es responsable de:

- ejecutar Commands;
- validar Invariants;
- emitir Domain Events;
- realizar consultas analíticas;
- construir proyecciones CQRS.

---

# Contrato Conceptual

```text
Application Service

        │

        ▼

Notification Repository

        │

        ▼

Notification Aggregate

        │

        ▼

Persistence
```

---

# Interfaz Conceptual

```text
NotificationRepository

    save()

    findById()

    exists()

    delete()

    nextIdentity()
```

La implementación concreta dependerá de la infraestructura.

---

# Operaciones

## nextIdentity()

### Propósito

Generar un nuevo identificador para un Aggregate Notification.

### Entrada

Ninguna.

### Salida

```text
NotificationId
```

### Reglas

Debe garantizar unicidad global.

---

## save()

### Propósito

Persistir el estado actual del Aggregate.

### Entrada

```text
Notification
```

### Salida

Ninguna.

### Reglas

- persistencia atómica;
- incremento de Version;
- control de concurrencia optimista;
- publicación diferida de eventos mediante Outbox cuando aplique.

El Repository persiste únicamente el resultado de una operación
previamente aceptada por Notification.

No puede:

- modificar NotificationStatus;
- ejecutar transiciones;
- corregir Invariants;
- crear Domain Events;
- decidir si una operación de dominio es válida.

---

## findById()

### Propósito

Recuperar un Aggregate existente.

### Entrada

```text
NotificationId
```

### Salida

```text
Notification
```

o

```text
None
```

si no existe.

La recuperación debe preservar el estado válido del Aggregate,
incluyendo su Version.

---

## exists()

### Propósito

Determinar si una Notification existe.

### Entrada

```text
NotificationId
```

### Salida

```text
Boolean
```

La operación no modifica el Aggregate.

---

## delete()

### Propósito

Eliminar físicamente un Aggregate cuando exista una política de
retención que lo permita.

### Observación

En AURA, la eliminación física no forma parte del flujo normal del
dominio.

El Lifecycle versión 1.0 de Notification no define:

```text
Deleted
```

ni:

```text
Archived
```

como NotificationStatus.

Por lo tanto, `delete()` debe considerarse una operación
excepcional de persistencia, sujeta a políticas externas de
retención o cumplimiento normativo.

`delete()` no constituye un Command del Aggregate y no crea una
transición de Lifecycle.

---

# Consistencia

El Repository debe garantizar que:

- un Aggregate nunca quede parcialmente persistido;
- la Version almacenada sea consistente;
- no existan escrituras concurrentes incompatibles;
- el historial permanezca íntegro;
- NotificationId permanezca asociado al mismo Aggregate;
- el estado persistido corresponda a una modificación válida.

Debe mantenerse:

```text
Notification

=

Single Persistence Unit
```

No deben existir escrituras parciales que permitan confirmar
únicamente una parte del nuevo estado.

---

# Concurrencia

El contrato asume **Optimistic Concurrency Control**.

Cada Notification posee:

```text
Version
```

Conceptualmente:

```text
Version

↓

Read

↓

Modify

↓

Save

↓

Version + 1
```

Si la Version almacenada difiere de la Version esperada por la
operación:

```text
PersistedVersion

≠

ExpectedVersion
```

la persistencia debe rechazarse.

El resultado conceptual es:

```text
ConcurrencyConflict
```

Una escritura obsoleta nunca debe sobrescribir silenciosamente una
modificación previamente confirmada.

---

# Gestión de Domain Events

El Repository no publica Domain Events.

Puede colaborar con mecanismos como:

- Outbox Pattern;
- Event Store;
- Unit of Work.

La publicación pertenece a Infrastructure o a la capa de
Application.

Los Domain Events oficiales de Notification son:

```text
NotificationCreated

NotificationQueued

NotificationDelivered

NotificationDeliveryFailed

NotificationRetried
```

El Repository no los inventa ni determina cuándo deben existir.

Notification los produce como consecuencia de comportamiento
válido.

---

# Errores Esperados

El contrato puede producir errores conceptuales como:

```text
NotificationNotFound

DuplicateNotificationId

ConcurrencyConflict

PersistenceFailure

RepositoryUnavailable
```

Las excepciones concretas dependen de la implementación.

Estos errores no introducen nuevos estados dentro del Lifecycle.

Por ejemplo:

```text
PersistenceFailure

≠

NotificationStatus = Failed
```

`Failed` pertenece al resultado de entrega definido por el dominio
y no a un fallo técnico de persistencia.

---

# Consultas

El Repository del Aggregate no implementa consultas de negocio
como:

- Notifications en Draft;
- Notifications Pending;
- Notifications Delivered;
- Notifications Failed;
- Notifications por destinatario;
- Notifications por canal;
- Notifications que fueron reintentadas;
- historial de Notifications.

Estas consultas pertenecen al lado de lectura:

```text
CQRS Read Models
```

La definición formal se encuentra en:

```text
DOMAIN-011L-Read-Model.md
```

---

# Compatibilidad con Event Sourcing

En una implementación basada en Event Sourcing, el Repository
puede reconstruir el Aggregate mediante la reproducción de los
Domain Events asociados al:

```text
NotificationId
```

Por ejemplo:

```text
NotificationCreated

↓

NotificationQueued

↓

NotificationDelivered
```

o:

```text
NotificationCreated

↓

NotificationQueued

↓

NotificationDeliveryFailed

↓

NotificationRetried

↓

NotificationDelivered
```

El contrato del Repository permanece idéntico.

Únicamente cambia la estrategia de persistencia.

La reconstrucción:

- no ejecuta nuevos Commands;
- no crea nuevas transiciones;
- no incrementa Version por sí misma;
- no genera nuevos Domain Events;
- no modifica hechos históricos.

---

# Compatibilidad con Bases de Datos

El contrato es independiente de la tecnología utilizada.

Puede implementarse sobre:

- PostgreSQL;
- MongoDB;
- EventStoreDB;
- DynamoDB;
- Cosmos DB;
- almacenamiento documental;
- cualquier mecanismo equivalente.

Ninguna de estas tecnologías forma parte del modelo de dominio.

Debe mantenerse:

```text
Repository Contract

≠

Persistence Technology
```

---

# Principios Arquitectónicos

El Repository cumple con:

- Domain-Driven Design (DDD);
- Repository Pattern;
- Dependency Inversion Principle (DIP);
- Clean Architecture;
- Persistence Ignorance.

El contrato mantiene:

- independencia tecnológica;
- encapsulamiento del Aggregate;
- consistencia transaccional;
- Optimistic Concurrency Control;
- separación entre persistencia y reglas de negocio;
- separación entre Repository y Read Models;
- separación entre persistencia y publicación de eventos.

---

# Definición de Éxito

El Repository del Aggregate **Notification** proporciona una
abstracción estable y desacoplada para persistir y recuperar las
unidades de notificación del ecosistema AURA.

El contrato garantiza que:

- Notification se persiste como una unidad;
- NotificationId mantiene identidad estable;
- Version protege modificaciones concurrentes;
- no existen escrituras parciales confirmadas;
- el Repository no ejecuta Commands;
- el Repository no valida Invariants;
- el Repository no modifica NotificationStatus;
- el Repository no crea Domain Events;
- la publicación de eventos permanece fuera del Repository;
- `delete()` permanece excepcional y no constituye una transición
  del Lifecycle;
- `PersistenceFailure` no se confunde con Notification Failed;
- las consultas de negocio pertenecen a Read Models;
- Event Sourcing puede utilizarse sin alterar el contrato;
- la tecnología de persistencia permanece fuera del dominio.

De esta forma, `DOMAIN-011G-Repository-Contract.md` establece el
contrato oficial de persistencia del Aggregate **Notification**
conforme al patrón consolidado de AURA Core.