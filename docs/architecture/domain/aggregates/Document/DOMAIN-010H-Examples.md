# DOMAIN-010H — Document Examples

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Document Management

Aggregate:
Document

Documentos relacionados:

- DOMAIN-010-Aggregate.md
- DOMAIN-010A-Lifecycle.md
- DOMAIN-010B-State-Machine.md
- DOMAIN-010C-Commands.md
- DOMAIN-010D-Domain-Events.md
- DOMAIN-010E-Invariants.md
- DOMAIN-010F-Permissions.md
- DOMAIN-010G-Repository-Contract.md

---

# Objetivo

Este documento presenta escenarios completos de negocio para
el Aggregate **Document**.

Los ejemplos muestran cómo interactúan Commands, reglas de
negocio, transiciones de estado y Domain Events durante el
ciclo de vida de una unidad documental dentro de AURA.

Los ejemplos son conceptuales y no representan una
implementación tecnológica.

---

# Ejemplo 1 — Creación de un nuevo Document

## Escenario

Se crea una nueva unidad documental dentro del dominio AURA.

### Estado inicial

```text
No existe Aggregate.
```

### Command

```text
CreateDocument
```

### Resultado

```text
Document

↓

Status = Draft
```

### Domain Event

```text
DocumentCreated
```

---

# Ejemplo 2 — Publicación de un Document

## Escenario

Un Document que se encuentra en preparación alcanza formalmente
la condición de publicación definida por el dominio.

### Estado inicial

```text
Draft
```

### Command

```text
PublishDocument
```

### Estado final

```text
Published
```

### Domain Event

```text
DocumentPublished
```

---

# Ejemplo 3 — Archivado de un Document

## Escenario

Un Document Published es retirado de su ciclo operativo y
conservado como parte del historial del dominio.

### Estado inicial

```text
Published
```

### Command

```text
ArchiveDocument
```

### Estado final

```text
Archived
```

### Domain Event

```text
DocumentArchived
```

---

# Ejemplo 4 — Publicación inválida de un Document ya Published

## Escenario

Se intenta publicar nuevamente un Document que ya alcanzó el
estado Published.

### Estado inicial

```text
Published
```

### Command

```text
PublishDocument
```

### Resultado

```text
Rejected
```

### Motivo

La transición:

```text
Published → Published
```

no está definida para `PublishDocument` en la State Machine.

### Domain Event

```text
Ninguno
```

---

# Ejemplo 5 — Intento de archivado desde Draft

## Escenario

Se intenta archivar un Document que todavía se encuentra en
estado Draft.

### Estado inicial

```text
Draft
```

### Command

```text
ArchiveDocument
```

### Resultado

```text
Rejected
```

### Motivo

La transición:

```text
Draft → Archived
```

no está definida en la State Machine y viola las Invariants
del Aggregate.

### Domain Event

```text
Ninguno
```

---

# Ejemplo 6 — Intento de publicación sobre un Document archivado

## Escenario

Se intenta publicar un Document que ya alcanzó el estado
terminal Archived.

### Estado inicial

```text
Archived
```

### Command

```text
PublishDocument
```

### Resultado

```text
Rejected
```

### Motivo

Archived es el estado terminal del Lifecycle versión 1.0.

La transición:

```text
Archived → Published
```

no forma parte de la State Machine.

### Domain Event

```text
Ninguno
```

---

# Ejemplo 7 — Intento de archivado sobre un Document archivado

## Escenario

Se intenta ejecutar nuevamente el archivado sobre un Document
cuyo Lifecycle ya terminó.

### Estado inicial

```text
Archived
```

### Command

```text
ArchiveDocument
```

### Resultado

```text
Rejected
```

### Motivo

`ArchiveDocument` requiere:

```text
Published
```

como estado origen.

Archived no posee transiciones ordinarias dentro del Lifecycle
versión 1.0.

### Domain Event

```text
Ninguno
```

---

# Ejemplo 8 — Documento de convocatoria asociado a una Assembly

## Escenario

Se crea un Document destinado a representar una convocatoria
utilizada por una Assembly.

Assembly mantiene únicamente la referencia:

```text
DocumentId
```

y no administra el contenido ni el Lifecycle del Document.

### Estado inicial

```text
No existe Document.
```

### Command

```text
CreateDocument
```

### Estado final

```text
Draft
```

### Domain Event

```text
DocumentCreated
```

Posteriormente:

```text
PublishDocument
```

produce:

```text
DocumentPublished
```

y:

```text
DocumentStatus = Published
```

La publicación del Document no modifica automáticamente el
estado de Assembly.

---

# Ejemplo 9 — Acta como Document independiente

## Escenario

Un acta utilizada por una Assembly se representa mediante un
Document con identidad y Lifecycle propios.

La relación se mantiene mediante:

```text
DocumentId
```

El Aggregate Assembly no contiene el Aggregate Document.

### Estado inicial

```text
No existe Document.
```

### Command

```text
CreateDocument
```

### Estado final

```text
Draft
```

### Domain Event

```text
DocumentCreated
```

Cuando el Document alcanza las condiciones correspondientes:

```text
PublishDocument
```

produce:

```text
DocumentPublished
```

sin modificar directamente el Lifecycle de Assembly.

---

# Ejemplo 10 — Flujo completo del ciclo de vida

```text
CreateDocument
      │
      ▼
DocumentCreated
      │
      ▼
    Draft
      │
      ▼
PublishDocument
      │
      ▼
DocumentPublished
      │
      ▼
  Published
      │
      ▼
ArchiveDocument
      │
      ▼
DocumentArchived
      │
      ▼
   Archived
```

Archived representa el estado terminal del Lifecycle versión
1.0.

No existe una transición ordinaria posterior.

---

# Relación con CQRS

Los Commands de estos ejemplos pertenecen al lado de escritura.

Los Domain Events generados alimentan posteriormente los Read
Models utilizados para consultas y representaciones derivadas
de Document.

Los Read Models no modifican el Aggregate y no sustituyen la
autoridad de escritura de Document.

---

# Relación con Event Sourcing

Cada escenario puede reconstruirse conceptualmente reproduciendo
la secuencia cronológica de Domain Events emitidos por el
Aggregate cuando la arquitectura adoptada utilice Event Sourcing.

Por ejemplo:

```text
DocumentCreated

↓

DocumentPublished

↓

DocumentArchived
```

representa la evolución histórica del mismo Document.

Los hechos históricos permanecen inmutables y no se reescriben
para reflejar estados posteriores.

---

# Definición de Éxito

Los ejemplos presentados demuestran el comportamiento esperado
del Aggregate **Document** frente a situaciones habituales y
excepcionales del negocio.

Sirven como referencia para el diseño, implementación y
validación del dominio, asegurando que:

- CreateDocument produzca un Document en Draft;
- PublishDocument solamente permita Draft → Published;
- ArchiveDocument solamente permita Published → Archived;
- Archived permanezca como estado terminal;
- las operaciones inválidas sean rechazadas;
- una operación rechazada no produzca Domain Events de éxito;
- Document conserve identidad y Lifecycle propios;
- Assembly utilice Document mediante DocumentId sin absorberlo;
- las reglas de negocio, la State Machine y los Domain Events
  permanezcan coherentes en todo el ecosistema AURA.