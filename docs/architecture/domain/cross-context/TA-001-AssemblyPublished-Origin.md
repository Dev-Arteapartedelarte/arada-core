# TA-001 — AssemblyPublished Origin

Versión: 1.0

Estado:
Resolved

Proyecto:
AURA Core

Baseline de referencia:
domain-model-v1.0.0

Alcance:
Transversal

Aggregate:
Assembly

Bounded Context:
Assembly Management

---

# Objetivo

Resolver de forma normativa el origen semántico del Integration
Event:

```text
AssemblyPublished
```

preservando el modelo de dominio existente de Assembly y sin
introducir nuevos:

* estados;
* Commands;
* Domain Events;
* Integration Events;
* Aggregates;
* Consistency Boundaries.

---

# Hallazgo

La documentación transversal mantenía ambigüedad respecto del
Domain Event que debía considerarse origen semántico de:

```text
AssemblyPublished
```

Las alternativas documentales existentes permitían relacionarlo
con:

```text
AssemblyCreated
```

o:

```text
AssemblyScheduled
```

Esta ambigüedad impedía establecer un mapping transversal
determinista.

---

# Decisión

El único Domain Event origen semántico de:

```text
AssemblyPublished
```

es:

```text
AssemblyScheduled
```

La relación normativa queda definida como:

```text
ScheduleAssembly
        │
        ▼
AssemblyScheduled
        │
        ▼
AssemblyPublished
```

cuando exista un contrato explícito de interoperabilidad que
requiera comunicar externamente ese hecho.

---

# Exclusión de AssemblyCreated

Debe mantenerse:

```text
AssemblyCreated
    ≠
AssemblyPublished
```

El hecho:

```text
AssemblyCreated
```

representa exclusivamente que una Assembly existe formalmente
dentro del dominio.

No significa:

```text
la Assembly fue programada
```

ni:

```text
la Assembly debe ser publicada externamente
```

Por lo tanto:

```text
CreateAssembly
        │
        ▼
AssemblyCreated
        │
        ✕
AssemblyPublished
```

`AssemblyCreated` queda excluido como origen semántico de
`AssemblyPublished`.

---

# Semántica de AssemblyScheduled

`AssemblyScheduled` representa que una Assembly previamente
existente alcanzó válidamente una programación formal aceptada por
el dominio.

Conceptualmente:

```text
Draft
    │
    ▼
ScheduleAssembly
    │
    ▼
AssemblyScheduled
    │
    ▼
Scheduled
```

Este hecho proporciona la condición semántica necesaria para que
una Assembly pueda ser comunicada mediante:

```text
AssemblyPublished
```

cuando el contrato de interoperabilidad correspondiente así lo
requiera.

---

# Publicación Condicional

La existencia de:

```text
AssemblyScheduled
```

no obliga automáticamente a producir:

```text
AssemblyPublished
```

Debe mantenerse:

```text
AssemblyScheduled
    ≠
Mandatory AssemblyPublished
```

La publicación externa continúa siendo condicional.

Solo corresponde cuando exista un contrato explícito de
interoperabilidad que requiera comunicar el hecho.

---

# No Publicación Automática

Esta decisión no establece:

```text
every AssemblyScheduled
        │
        ▼
AssemblyPublished
```

como comportamiento obligatorio.

La relación normativa establece únicamente el origen semántico
permitido.

Por lo tanto:

```text
AssemblyScheduled
        │
        ▼
explicit integration contract
        │
        ▼
AssemblyPublished
```

representa la relación válida.

---

# Naturaleza de AssemblyPublished

`AssemblyPublished` permanece definido como:

```text
Integration Event
```

No se convierte en:

```text
Domain Event
```

No constituye:

```text
AssemblyStatus
```

No introduce un nuevo estado:

```text
Published
```

dentro del Lifecycle de Assembly.

---

# Commands

Esta decisión no introduce:

```text
PublishAssembly
```

ni ningún otro Command adicional.

El Command relacionado con el hecho origen continúa siendo:

```text
ScheduleAssembly
```

cuyo Domain Event correspondiente es:

```text
AssemblyScheduled
```

---

# Domain Events

Esta decisión no introduce ningún nuevo Domain Event.

Se mantiene:

```text
ScheduleAssembly
        │
        ▼
AssemblyScheduled
```

como comportamiento oficial del Aggregate Assembly.

`AssemblyPublished` permanece fuera del catálogo de Domain Events.

---

# Integration Events

La decisión únicamente determina el origen semántico del contrato
existente:

```text
AssemblyPublished
```

No crea un nuevo Integration Event.

No modifica su naturaleza contractual.

No obliga a su publicación ante cada ocurrencia de
`AssemblyScheduled`.

---

# Lifecycle

Esta decisión no modifica el Lifecycle de Assembly.

No introduce:

```text
Published
```

como estado.

La transición relacionada continúa siendo:

```text
Draft
    │
    ▼
Scheduled
```

mediante:

```text
ScheduleAssembly
```

y:

```text
AssemblyScheduled
```

---

# Consistency Boundary

Esta decisión no modifica el Consistency Boundary de Assembly.

Debe mantenerse:

```text
Aggregate Boundary
    =
Immediate Consistency Boundary
```

y:

```text
Cross-Boundary Communication
    =
Eventual Consistency
```

`AssemblyPublished` permanece fuera del estado interno del
Aggregate Assembly.

---

# Regla Normativa

El mapping oficial queda establecido como:

```text
ScheduleAssembly
    │
    ▼
AssemblyScheduled
    │
    ▼
AssemblyPublished
```

sujeto a:

```text
explicit integration contract
```

Debe mantenerse:

```text
AssemblyCreated
    ✕
AssemblyPublished
```

---

# Restricciones

Esta decisión no autoriza:

* crear un estado Published;
* crear PublishAssembly;
* crear un nuevo Domain Event de publicación;
* transformar AssemblyPublished en Domain Event;
* publicar AssemblyPublished automáticamente ante todo
  AssemblyScheduled;
* utilizar AssemblyCreated como origen de AssemblyPublished;
* modificar el Lifecycle de Assembly;
* modificar el Consistency Boundary;
* introducir nuevos Aggregates;
* introducir nuevos contratos de integración.

---

# Decisiones Técnicas Fuera de Alcance

Esta resolución no define:

* broker;
* transport;
* topic;
* queue;
* Outbox;
* Inbox;
* retry;
* delivery guarantees;
* serialization;
* protocolo;
* mecanismo de idempotencia;
* consumidores concretos;
* infraestructura de publicación.

Estas decisiones no forman parte de TA-001.

---

# Impacto Documental

La resolución debe mantenerse coherente en:

```text
DOMAIN-006K-Integration-Events.md

CROSS-001-Transversal-Audit.md

CROSS-004-Cross-Domain-Contracts.md

event-catalog.md
```

Ninguno de estos documentos debe volver a presentar como
indeterminado el origen semántico de:

```text
AssemblyPublished
```

---

# Baseline

El tag:

```text
domain-model-v1.0.0
```

permanece como referencia histórica inmutable.

Esta resolución no modifica retrospectivamente el contenido del
baseline etiquetado.

La decisión corresponde a la consolidación documental posterior de
los contratos transversales.

---

# Resolución

TA-001 queda:

```text
Resolved
```

con la siguiente regla normativa:

```text
AssemblyPublished
    ←
AssemblyScheduled
```

y:

```text
AssemblyPublished
    ←
AssemblyCreated
```

queda expresamente excluido.

La publicación de `AssemblyPublished` continúa siendo condicional
al contrato explícito de interoperabilidad correspondiente.

No se modifica el Aggregate Assembly, su Lifecycle, sus Commands,
sus Domain Events ni su Consistency Boundary.