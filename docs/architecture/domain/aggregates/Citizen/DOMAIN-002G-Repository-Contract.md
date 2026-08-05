# DOMAIN-002G — Citizen Repository Contract

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Citizen Management

Aggregate:
Citizen

Documentos relacionados:

- DOMAIN-002-Aggregate.md
- DOMAIN-002C-Commands.md
- DOMAIN-002D-Domain-Events.md
- DOMAIN-002E-Invariants.md
- CORE-011-Repository-Contracts.md

---

# Objetivo

Este documento define el contrato oficial del Repository del
Aggregate **Citizen**.

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
- validar invariantes;
- emitir Domain Events;
- realizar consultas analíticas;
- construir proyecciones CQRS.

---

# Contrato Conceptual

```text
Application Service

        │

        ▼

Citizen Repository

        │

        ▼

Citizen Aggregate

        │

        ▼

Persistence
```

---

# Interfaz Conceptual

```text
CitizenRepository

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

Generar un nuevo identificador para un Aggregate Citizen.

### Entrada

Ninguna.

### Salida

```text
CitizenId
```

### Reglas

Debe garantizar unicidad global.

---

## save()

### Propósito

Persistir el estado actual del Aggregate.

### Entrada

```text
Citizen
```

### Salida

Ninguna.

### Reglas

- persistencia atómica;
- incremento de versión;
- control de concurrencia optimista;
- publicación diferida de eventos (Outbox, si aplica).

---

## findById()

### Propósito

Recuperar un Aggregate existente.

### Entrada

```text
CitizenId
```

### Salida

```text
Citizen
```

o

```text
None
```

si no existe.

---

## exists()

### Propósito

Determinar si un Citizen existe.

### Entrada

```text
CitizenId
```

### Salida

```text
Boolean
```

---

## delete()

### Propósito

Eliminar físicamente un Aggregate cuando exista una política
de retención que lo permita.

### Observación

En AURA, la eliminación física no forma parte del flujo normal
del dominio. Habitualmente se utiliza el estado **Archived**,
por lo que este método debe considerarse excepcional y sujeto
a políticas de cumplimiento normativo.

---

# Consistencia

El Repository debe garantizar que:

- un Aggregate nunca quede parcialmente persistido;
- la versión almacenada sea consistente;
- no existan escrituras concurrentes incompatibles;
- el historial permanezca íntegro.

---

# Concurrencia

El contrato asume **Optimistic Concurrency Control**.

Cada Aggregate posee un número de versión.

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

Si la versión almacenada difiere de la versión enviada por la
capa de aplicación, la operación debe rechazarse.

---

# Gestión de Domain Events

El Repository no publica Domain Events.

Puede colaborar con mecanismos como:

- Outbox Pattern;
- Event Store;
- Unit of Work.

La publicación pertenece a la infraestructura o a la capa de
aplicación.

---

# Errores Esperados

El contrato puede producir errores conceptuales como:

```text
CitizenNotFound

DuplicateCitizenId

ConcurrencyConflict

PersistenceFailure

RepositoryUnavailable
```

Las excepciones concretas dependen de la implementación.

---

# Consultas

El Repository del Aggregate no implementa consultas de negocio
como:

- ciudadanos activos;
- ciudadanos por territorio;
- ciudadanos verificados;
- ciudadanos suspendidos.

Estas consultas pertenecen al lado de lectura (CQRS Read
Models).

---

# Compatibilidad con Event Sourcing

En una implementación basada en Event Sourcing, el Repository
puede reconstruir el Aggregate mediante la reproducción de los
Domain Events asociados al **CitizenId**.

El contrato permanece idéntico; únicamente cambia la forma de
persistencia.

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

---

# Principios Arquitectónicos

El Repository cumple con:

- Domain-Driven Design (DDD);
- Repository Pattern;
- Dependency Inversion Principle (DIP);
- Clean Architecture;
- Persistence Ignorance.

---

# Definición de Éxito

El Repository del Aggregate **Citizen** proporciona una
abstracción estable y desacoplada para la persistencia de las
identidades cívicas del ecosistema AURA. Garantiza consistencia,
control de concurrencia e independencia tecnológica,
permitiendo que el dominio evolucione sin depender de una
tecnología específica de almacenamiento.