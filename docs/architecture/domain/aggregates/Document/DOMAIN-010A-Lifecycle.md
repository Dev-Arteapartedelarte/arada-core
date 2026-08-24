# DOMAIN-010A — Document Lifecycle

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Document Management

Aggregate:
Document

Autor:
ARADA

Documentos Relacionados:

- DOMAIN-010-Aggregate.md
- DOMAIN-010B-State-Machine.md
- DOMAIN-010C-Commands.md
- DOMAIN-010D-Domain-Events.md
- DOMAIN-010E-Invariants.md
- DOMAIN-010F-Permissions.md
- DOMAIN-010G-Repository-Contract.md
- DOMAIN-010I-Versioning.md
- DOMAIN-010J-Consistency-Boundary.md
- CORE-006-Domain-Invariants.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Definir formalmente el **Lifecycle** del Aggregate **Document**.

El Lifecycle establece los estados válidos que puede adoptar un
Document y las transiciones mediante las cuales puede evolucionar
durante su existencia dentro del dominio AURA.

El Lifecycle pertenece exclusivamente al Aggregate Document.

No representa:

- el Lifecycle de Assembly;
- el Lifecycle de Proposal;
- el Lifecycle de Participation;
- el Lifecycle de Voting;
- el Lifecycle de Organization;
- el estado de almacenamiento físico;
- el estado de transferencia de archivos;
- el estado de infraestructura.

Debe mantenerse:

```text
Document Lifecycle

≠

Infrastructure Lifecycle
```

---

# Propósito

El Lifecycle permite distinguir claramente entre:

- existencia inicial del Document;
- formalización del Document;
- retiro del ciclo operativo;
- conservación histórica.

Permite responder conceptualmente:

```text
¿El Document existe?

¿Continúa en preparación?

¿Ha sido formalizado?

¿Permanece operativo?

¿Ha sido archivado?
```

Toda evolución debe mantener:

- DocumentId;
- Invariants;
- Consistency Boundary;
- Version;
- trazabilidad;
- coherencia con Domain Events.

---

# Principios

El Lifecycle de Document cumple los siguientes principios:

- todo Document posee un estado válido;
- el estado inicial es explícito;
- toda transición es explícita;
- ninguna transición ocurre mediante modificación directa de
  DocumentStatus;
- toda transición válida es controlada por la Aggregate Root;
- toda transición debe preservar las Invariants;
- toda transición válida incrementa Version;
- toda transición relevante produce el Domain Event
  correspondiente;
- una transición rechazada no modifica el Aggregate;
- una transición rechazada no incrementa Version;
- una transición rechazada no produce el Domain Event de éxito;
- Archived representa una condición histórica;
- Archived no representa eliminación física;
- el Lifecycle de Document permanece independiente del Lifecycle
  de otros Aggregates.

---

# Estados

La versión 1.0 del Lifecycle de Document define los siguientes
estados:

```text
Draft

Published

Archived
```

Cada estado representa una condición válida y explícita del
Aggregate.

No existen estados implícitos.

---

# Estado Inicial

Todo Document creado válidamente comienza en:

```text
Draft
```

La creación establece la existencia formal del Aggregate.

No significa que el Document haya sido Published.

Debe mantenerse:

```text
No Document

↓

CreateDocument

↓

Draft
```

---

# Draft

`Draft` representa un Document que existe formalmente dentro del
dominio pero todavía no ha alcanzado la condición de Published.

En Draft:

- DocumentId ya existe;
- DocumentType debe ser válido;
- Content pertenece al Aggregate;
- DocumentStatus es Draft;
- Version pertenece al Aggregate;
- las modificaciones permitidas deben respetar Commands e
  Invariants.

Draft no significa:

```text
Document does not exist
```

El Aggregate existe desde su creación.

La definición de qué modificaciones de contenido o clasificación
son válidas mientras Document permanece en Draft pertenece a:

```text
DOMAIN-010C-Commands.md

DOMAIN-010E-Invariants.md
```

---

# Published

`Published` representa un Document que ha sido formalizado dentro
del dominio.

La transición hacia Published confirma que el Document alcanzó la
condición requerida para su publicación conforme a sus reglas.

Debe mantenerse:

```text
Draft

↓

PublishDocument

↓

Published
```

Published no significa:

- almacenamiento en una tecnología concreta;
- exposición mediante HTTP;
- publicación en FIWARE;
- envío de Notification;
- modificación automática de otro Aggregate.

Debe mantenerse:

```text
Domain Publication

≠

Technical Distribution
```

Las reglas sobre qué modificaciones pueden realizarse después de
Published pertenecen a Commands e Invariants y no deben inferirse
únicamente desde el nombre del estado.

---

# Archived

`Archived` representa que el Document fue retirado de su ciclo
operativo y permanece como parte del historial del dominio.

Archived:

- conserva DocumentId;
- conserva identidad;
- conserva trazabilidad;
- conserva Version;
- conserva los hechos históricos;
- no equivale a eliminación física.

Debe mantenerse:

```text
Archived

≠

Deleted
```

Archived constituye el estado terminal del Lifecycle versión 1.0.

No existe una transición ordinaria desde Archived hacia otro
estado.

---

# Ciclo de Vida

El Lifecycle principal de Document es:

```text
No Document
     │
     ▼
   Draft
     │
     ▼
 Published
     │
     ▼
  Archived
```

Expresado mediante Commands y hechos:

```text
CreateDocument
     │
     ▼
   Draft
     │
PublishDocument
     │
     ▼
 Published
     │
ArchiveDocument
     │
     ▼
  Archived
```

---

# Transiciones Permitidas

La versión 1.0 reconoce exclusivamente:

```text
No Document → Draft

Draft → Published

Published → Archived
```

Cada transición debe:

- originarse desde el estado permitido;
- ejecutarse mediante comportamiento explícito;
- validar las Invariants correspondientes;
- finalizar en un estado válido;
- incrementar Version;
- producir el Domain Event correspondiente.

---

# Creación

La creación se realiza mediante:

```text
CreateDocument
```

Estado previo:

```text
No Document
```

Estado resultante:

```text
Draft
```

Domain Event esperado:

```text
DocumentCreated
```

Una creación válida:

- establece DocumentId;
- establece los datos iniciales válidos;
- establece DocumentStatus en Draft;
- establece la existencia del Aggregate;
- produce DocumentCreated.

La creación no implica publicación.

Debe mantenerse:

```text
DocumentCreated

≠

DocumentPublished
```

---

# Publicación

La publicación se realiza mediante:

```text
PublishDocument
```

Estado origen:

```text
Draft
```

Estado destino:

```text
Published
```

Domain Event esperado:

```text
DocumentPublished
```

Una publicación válida:

- valida el estado actual;
- valida las Invariants correspondientes;
- cambia DocumentStatus a Published;
- incrementa Version;
- produce DocumentPublished.

Publicar Document no modifica directamente:

- Assembly;
- Proposal;
- Participation;
- Voting;
- Notification;
- Audit.

---

# Archivado

El archivado se realiza mediante:

```text
ArchiveDocument
```

Estado origen:

```text
Published
```

Estado destino:

```text
Archived
```

Domain Event esperado:

```text
DocumentArchived
```

Un archivado válido:

- valida el estado;
- valida las Invariants correspondientes;
- cambia DocumentStatus a Archived;
- incrementa Version;
- produce DocumentArchived.

El archivado conserva la existencia histórica del Document.

---

# Estado Terminal

El estado terminal de Document es:

```text
Archived
```

Desde Archived no existen transiciones ordinarias.

Por lo tanto:

```text
Archived → Draft
```

no está permitido.

```text
Archived → Published
```

no está permitido.

La versión 1.0 no define:

```text
RestoreDocument

ReopenDocument

RepublishDocument

UnarchiveDocument
```

ni transiciones equivalentes.

Cualquier incorporación futura requiere evolución explícita del
modelo.

---

# Transiciones No Permitidas

La versión 1.0 no permite:

```text
Draft → Archived

Published → Draft

Archived → Draft

Archived → Published
```

Tampoco permite:

```text
Draft → Draft
```

como transición de Lifecycle.

Una modificación válida que mantenga Document en Draft no
constituye por sí misma una transición del Lifecycle.

Del mismo modo:

```text
Published → Published
```

puede representar una modificación válida de dominio cuando otro
Command lo permita, pero no constituye una transición de Lifecycle.

---

# Modificaciones sin Cambio de Estado

No toda modificación válida de Document implica un cambio de
DocumentStatus.

Conceptualmente:

```text
Draft

↓

Valid Domain Modification

↓

Draft
```

o:

```text
Published

↓

Valid Domain Modification

↓

Published
```

cuando las reglas de Commands e Invariants permitan dicha
modificación.

Estas operaciones:

- pueden modificar estado interno distinto de DocumentStatus;
- incrementan Version cuando constituyen una modificación válida;
- pueden producir Domain Events;
- no constituyen por sí mismas una transición del Lifecycle.

Las operaciones exactas y los estados desde los cuales son
permitidas pertenecen a:

```text
DOMAIN-010C-Commands.md

DOMAIN-010E-Invariants.md
```

---

# Lifecycle y Content

Content pertenece al Aggregate Document.

El Lifecycle no autoriza modificaciones directas sobre Content.

Debe mantenerse:

```text
Content Change

↓

Explicit Domain Behavior

↓

Validate Invariants

↓

Valid Modification
```

La posibilidad de modificar Content depende de las reglas
establecidas para el Command correspondiente.

Este documento no introduce una transición adicional por el solo
hecho de modificar Content.

---

# Lifecycle y DocumentType

DocumentType no constituye un estado del Lifecycle.

Debe mantenerse:

```text
DocumentType

≠

DocumentStatus
```

Conceptualmente:

```text
Minutes

Resolution

Convocation

Agenda
```

representan naturaleza documental cuando formen parte del
DocumentType.

Mientras:

```text
Draft

Published

Archived
```

representan estados del Lifecycle.

---

# Lifecycle y Otros Aggregates

El Lifecycle de Document es independiente del Lifecycle de los
Aggregates relacionados.

Por ejemplo:

```text
Assembly Completed
```

no implica automáticamente:

```text
Document Published
```

y:

```text
Document Archived
```

no implica automáticamente:

```text
Assembly Archived
```

Debe mantenerse:

```text
Aggregate Lifecycle

=

Aggregate Responsibility
```

---

# Lifecycle y Assembly

Assembly puede mantener:

```text
DocumentId
```

pero no controla DocumentStatus directamente.

Document tampoco controla AssemblyStatus.

Por lo tanto:

```text
Assembly State Transition

≠

Automatic Document State Transition
```

y:

```text
Document State Transition

≠

Automatic Assembly State Transition
```

La coordinación entre ambos Aggregates debe respetar sus límites
de consistencia.

---

# Lifecycle y Proposal

Proposal permanece fuera del Consistency Boundary de Document.

El estado de Proposal no determina directamente DocumentStatus.

Document no modifica Proposal como consecuencia de una transición
propia.

---

# Lifecycle y Voting

Voting mantiene un Lifecycle independiente.

Una transición de Voting no modifica directamente DocumentStatus.

Una transición de Document no modifica directamente VotingStatus.

Debe mantenerse:

```text
Voting Lifecycle

≠

Document Lifecycle
```

---

# Lifecycle y Participation

Participation mantiene sus propias reglas de Lifecycle.

Document no administra Participation.

Ninguna transición del Document crea, modifica o termina
Participation directamente.

---

# Lifecycle y Notification

Una transición de Document puede originar un hecho que
posteriormente genere una necesidad de Notification.

Document no envía Notifications directamente.

Debe mantenerse:

```text
DocumentPublished

↓

Domain Fact
```

sin implicar:

```text
Notification Delivered
```

como parte de la misma transición.

---

# Lifecycle y Audit

Las transiciones relevantes pueden ser observadas posteriormente
por Audit.

Audit no forma parte del Aggregate Document.

El Lifecycle conserva trazabilidad mediante:

- DocumentId;
- DocumentStatus;
- Version;
- Domain Events;
- información temporal correspondiente.

---

# Commands

Las transiciones oficiales se relacionan conceptualmente con:

| Estado origen | Command | Estado destino |
| --- | --- | --- |
| No Document | CreateDocument | Draft |
| Draft | PublishDocument | Published |
| Published | ArchiveDocument | Archived |

Los Commands expresan intención.

No representan hechos consumados.

La definición completa pertenece a:

```text
DOMAIN-010C-Commands.md
```

---

# Domain Events

Cada transición válida produce el hecho correspondiente:

| Transición | Domain Event |
| --- | --- |
| No Document → Draft | DocumentCreated |
| Draft → Published | DocumentPublished |
| Published → Archived | DocumentArchived |

Los Domain Events representan hechos consumados.

Debe mantenerse:

```text
Command

↓

Document

↓

Valid Transition

↓

Domain Event
```

La definición completa pertenece a:

```text
DOMAIN-010D-Domain-Events.md
```

---

# Invariants

Toda transición debe preservar las Invariants de Document.

Entre las reglas aplicables al Lifecycle se mantiene:

- DocumentId nunca cambia;
- DocumentStatus siempre es válido;
- el estado inicial es Draft;
- Published solamente puede alcanzarse desde Draft;
- Archived solamente puede alcanzarse desde Published;
- Archived es terminal;
- ninguna transición puede omitir la Aggregate Root;
- toda modificación válida incrementa Version;
- una transición rechazada conserva el estado anterior;
- una transición rechazada no produce el Domain Event de éxito;
- otros Aggregates permanecen fuera del Consistency Boundary.

Las reglas completas pertenecen a:

```text
DOMAIN-010E-Invariants.md
```

---

# Versioning

Toda transición válida modifica el Aggregate.

Por lo tanto:

```text
Version N

↓

Valid Lifecycle Transition

↓

Version N + 1
```

Una transición rechazada mantiene:

```text
Version N
```

El Domain Event producido por una transición válida debe mantener
una relación coherente con la Version resultante.

La definición formal pertenece a:

```text
DOMAIN-010I-Versioning.md
```

---

# Consistency Boundary

Toda transición del Lifecycle ocurre exclusivamente dentro del
Consistency Boundary de Document.

Una transición puede modificar únicamente el estado perteneciente
al mismo Aggregate.

No puede modificar directamente:

```text
Organization

Citizen

Membership

Role

Territory

Assembly

Proposal

Participation

Voting

Notification

Audit

Integration
```

Debe mantenerse:

```text
Document Lifecycle Transition

↓

Document Consistency Boundary
```

La definición formal pertenece a:

```text
DOMAIN-010J-Consistency-Boundary.md
```

---

# Persistencia

La persistencia debe preservar el DocumentStatus confirmado por el
Aggregate.

El Repository no crea transiciones.

No debe:

- publicar un Document;
- archivar un Document;
- modificar DocumentStatus;
- evitar Invariants.

Debe persistir el resultado de comportamiento válido del
Aggregate.

Conceptualmente:

```text
Command

↓

Document

↓

Valid Transition

↓

Repository
```

No:

```text
Repository

↓

Direct Status Transition
```

---

# Read Models

Los Read Models pueden representar DocumentStatus.

Pueden mostrar conceptualmente:

```text
Draft

Published

Archived
```

pero no controlan el Lifecycle.

Debe mantenerse:

```text
Read Model

≠

Lifecycle Authority
```

Una proyección no puede publicar ni archivar un Document.

---

# Trazabilidad

El Lifecycle debe permitir reconstruir conceptualmente la
evolución de un Document:

```text
DocumentCreated
      │
      ▼
    Draft
      │
      ▼
DocumentPublished
      │
      ▼
  Published
      │
      ▼
DocumentArchived
      │
      ▼
   Archived
```

Los hechos anteriores no se reescriben como consecuencia de
estados posteriores.

Por ejemplo:

```text
DocumentArchived
```

no significa:

```text
Document was never Published
```

La historia completa debe conservarse.

---

# Eliminación

La versión 1.0 no utiliza eliminación física como transición
ordinaria del Lifecycle.

No existe:

```text
Deleted
```

como DocumentStatus oficial.

Tampoco se define:

```text
DeleteDocument
```

como transición del Lifecycle.

El cierre operativo se representa mediante:

```text
Archived
```

sin eliminar la identidad ni la historia del Aggregate.

---

# Independencia Tecnológica

El Lifecycle no depende de:

```text
File System

Object Storage

Database

MongoDB

PostgreSQL

HTTP

REST

GraphQL

Cloud Storage

FIWARE
```

Estos mecanismos pueden persistir, transportar o exponer
representaciones del Document.

No determinan:

```text
DocumentStatus
```

ni sus transiciones.

---

# Compatibilidad Arquitectónica

El Lifecycle mantiene compatibilidad con:

- Domain-Driven Design;
- Aggregate Pattern;
- State Machine explícita;
- Domain Events;
- Optimistic Concurrency Control;
- CQRS;
- Event Sourcing Compatible;
- Consistency Boundary;
- independencia tecnológica.

La State Machine formaliza las transiciones definidas por este
Lifecycle en:

```text
DOMAIN-010B-State-Machine.md
```

---

# Definición de Éxito

El Lifecycle de **Document** representa de manera explícita la
evolución formal de una unidad documental desde su creación hasta
su conservación histórica.

La versión 1.0 establece:

```text
Draft

Published

Archived
```

y las transiciones:

```text
No Document → Draft

Draft → Published

Published → Archived
```

El Lifecycle garantiza que:

- todo Document comienza en Draft;
- Published constituye una condición distinta de Draft;
- Archived constituye el estado terminal;
- Archived no equivale a Deleted;
- toda transición es ejecutada por la Aggregate Root;
- toda transición respeta Invariants;
- toda transición válida incrementa Version;
- toda transición válida produce el Domain Event correspondiente;
- las operaciones rechazadas no modifican estado ni Version;
- las modificaciones que mantienen el mismo DocumentStatus no
  constituyen por sí mismas transiciones de Lifecycle;
- DocumentType permanece separado de DocumentStatus;
- el Lifecycle de Document permanece independiente de otros
  Aggregates;
- ningún mecanismo de Infrastructure determina el estado del
  dominio.

De esta forma, `DOMAIN-010A-Lifecycle.md` establece el ciclo de
vida oficial del Aggregate **Document** manteniendo el patrón
consolidado de AURA Core.