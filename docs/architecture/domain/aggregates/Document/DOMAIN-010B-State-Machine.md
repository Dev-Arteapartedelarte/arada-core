# DOMAIN-010B — Document State Machine

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
- DOMAIN-010A-Lifecycle.md
- DOMAIN-010C-Commands.md
- DOMAIN-010D-Domain-Events.md
- DOMAIN-010E-Invariants.md
- DOMAIN-010F-Permissions.md
- DOMAIN-010I-Versioning.md
- DOMAIN-010J-Consistency-Boundary.md
- CORE-006-Domain-Invariants.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Definir formalmente la **State Machine** del Aggregate
**Document**.

La State Machine establece los estados válidos y las transiciones
permitidas durante el Lifecycle de Document.

Formaliza las reglas establecidas en:

```text
DOMAIN-010A-Lifecycle.md
```

sin introducir estados ni transiciones adicionales.

---

# Principios

La State Machine de Document cumple los siguientes principios:

- todo Document mantiene un DocumentStatus válido;
- todo Document nuevo comienza en Draft;
- DocumentStatus solamente cambia mediante comportamiento
  explícito de la Aggregate Root;
- ninguna transición puede realizarse mediante modificación
  directa del estado;
- toda transición debe encontrarse definida explícitamente;
- toda transición debe preservar las Invariants;
- toda transición válida incrementa Version;
- toda transición válida produce el Domain Event correspondiente;
- una transición rechazada no modifica el Aggregate;
- una transición rechazada no incrementa Version;
- una transición rechazada no produce el Domain Event de éxito;
- Archived es terminal;
- otros Aggregates no controlan DocumentStatus;
- Infrastructure no controla DocumentStatus.

---

# Estados

La versión 1.0 reconoce exclusivamente:

```text
Draft

Published

Archived
```

No existen estados implícitos.

---

# Estado Inicial

Todo Document creado válidamente comienza en:

```text
Draft
```

La transición inicial es:

```text
No Document → Draft
```

mediante:

```text
CreateDocument
```

y produce:

```text
DocumentCreated
```

---

# Draft

Draft representa un Document existente que todavía no ha
alcanzado Published.

Desde Draft, la transición de Lifecycle definida por la versión
1.0 es:

```text
Draft → Published
```

mediante:

```text
PublishDocument
```

La State Machine no determina en este documento en qué estados
pueden ejecutarse modificaciones que no alteren DocumentStatus.

Esa definición corresponde a:

```text
DOMAIN-010C-Commands.md

DOMAIN-010E-Invariants.md
```

---

# Published

Published representa un Document que alcanzó formalmente la
condición de publicación definida por el dominio.

Desde Published, la transición de Lifecycle definida por la
versión 1.0 es:

```text
Published → Archived
```

mediante:

```text
ArchiveDocument
```

La State Machine no determina en este documento en qué estados
pueden ejecutarse modificaciones que no alteren DocumentStatus.

Esa definición corresponde a:

```text
DOMAIN-010C-Commands.md

DOMAIN-010E-Invariants.md
```

---

# Archived

Archived representa el estado histórico terminal de Document.

Desde Archived no existen transiciones ordinarias.

No están permitidas:

```text
Archived → Draft

Archived → Published
```

Archived no representa eliminación física.

---

# State Machine

La State Machine oficial es:

```text
No Document
     │
     │ CreateDocument
     ▼
   Draft
     │
     │ PublishDocument
     ▼
 Published
     │
     │ ArchiveDocument
     ▼
  Archived
```

---

# Transiciones Permitidas

La versión 1.0 reconoce:

| Estado origen | Command | Estado destino | Domain Event |
| --- | --- | --- | --- |
| No Document | CreateDocument | Draft | DocumentCreated |
| Draft | PublishDocument | Published | DocumentPublished |
| Published | ArchiveDocument | Archived | DocumentArchived |

Toda transición debe:

- originarse desde el estado permitido;
- ejecutarse mediante comportamiento explícito de Document;
- validar las Invariants correspondientes;
- finalizar en un estado válido;
- incrementar Version;
- producir el Domain Event correspondiente.

---

# Transición No Document → Draft

Estado origen:

```text
No Document
```

Command:

```text
CreateDocument
```

Estado destino:

```text
Draft
```

Domain Event:

```text
DocumentCreated
```

Una creación válida establece la existencia formal del Aggregate.

No significa que el Document haya sido Published.

---

# Transición Draft → Published

Estado origen:

```text
Draft
```

Command:

```text
PublishDocument
```

Estado destino:

```text
Published
```

Domain Event:

```text
DocumentPublished
```

La transición solamente puede ejecutarse cuando las Invariants
correspondientes se encuentran satisfechas.

---

# Transición Published → Archived

Estado origen:

```text
Published
```

Command:

```text
ArchiveDocument
```

Estado destino:

```text
Archived
```

Domain Event:

```text
DocumentArchived
```

La transición solamente puede ejecutarse cuando las Invariants
correspondientes se encuentran satisfechas.

Archived constituye el estado terminal.

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
No Document → Published

No Document → Archived
```

Estas transiciones no forman parte del Lifecycle oficial.

---

# Transiciones al Mismo Estado

Una modificación válida que preserve DocumentStatus no constituye
por sí misma una transición del Lifecycle.

Por ejemplo:

```text
Draft → Draft
```

o:

```text
Published → Published
```

pueden representar permanencia de estado durante una modificación
válida cuando las reglas del Command correspondiente lo permitan.

No constituyen nuevas transiciones del Lifecycle.

La definición de dichas operaciones pertenece a:

```text
DOMAIN-010C-Commands.md

DOMAIN-010E-Invariants.md
```

---

# Rechazo de Transiciones

Cuando una transición no sea permitida:

```text
Command

↓

Validate Current State

↓

Rejected
```

debe mantenerse:

```text
DocumentStatus = PreviousStatus

Version = PreviousVersion
```

No debe producirse el Domain Event de éxito correspondiente.

---

# Commands

Las transiciones oficiales se relacionan con:

```text
CreateDocument

PublishDocument

ArchiveDocument
```

Los Commands representan intención.

No modifican directamente DocumentStatus.

La Aggregate Root determina si la transición puede ejecutarse.

La definición completa pertenece a:

```text
DOMAIN-010C-Commands.md
```

---

# Domain Events

Las transiciones válidas producen:

```text
DocumentCreated

DocumentPublished

DocumentArchived
```

Los Domain Events representan hechos consumados.

La relación conceptual es:

```text
Command

↓

Document

↓

Valid State Transition

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

Como mínimo:

- DocumentStatus siempre pertenece al conjunto oficial;
- todo Document nuevo comienza en Draft;
- Published solamente puede alcanzarse desde Draft;
- Archived solamente puede alcanzarse desde Published;
- Archived es terminal;
- DocumentId nunca cambia;
- DocumentStatus no puede modificarse directamente;
- una transición inválida no modifica el Aggregate;
- una transición inválida no incrementa Version;
- una transición inválida no produce el Domain Event de éxito;
- toda transición válida incrementa Version;
- toda transición válida debe finalizar con un Aggregate
  consistente.

Las reglas completas pertenecen a:

```text
DOMAIN-010E-Invariants.md
```

---

# Versioning

Toda transición válida modifica el Aggregate.

Debe mantenerse:

```text
Version N

↓

Valid State Transition

↓

Version N + 1
```

Una transición rechazada mantiene:

```text
Version N
```

El Domain Event correspondiente debe mantener coherencia con la
Version resultante.

La definición formal pertenece a:

```text
DOMAIN-010I-Versioning.md
```

---

# Consistency Boundary

Toda transición ocurre exclusivamente dentro del Consistency
Boundary de Document.

Una transición de Document no modifica directamente:

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

Cada Aggregate mantiene su propia State Machine y su propio
Lifecycle.

La definición formal pertenece a:

```text
DOMAIN-010J-Consistency-Boundary.md
```

---

# Relación con Content

Content pertenece al Aggregate Document.

Una modificación de Content no constituye automáticamente una
transición de Lifecycle.

Debe mantenerse:

```text
Content Change

≠

DocumentStatus Change
```

La posibilidad de modificar Content en un estado determinado
pertenece a las reglas de Commands e Invariants.

---

# Relación con DocumentType

DocumentType no representa un estado.

Debe mantenerse:

```text
DocumentType

≠

DocumentStatus
```

Los estados oficiales continúan siendo:

```text
Draft

Published

Archived
```

---

# Relación con Otros Aggregates

El estado de otro Aggregate no modifica automáticamente
DocumentStatus.

Del mismo modo, una transición de Document no modifica
automáticamente el estado de otro Aggregate.

Debe mantenerse:

```text
Aggregate State Machine

=

Aggregate Responsibility
```

---

# Estado Terminal

Archived es terminal.

La versión 1.0 no define:

```text
RestoreDocument

ReopenDocument

RepublishDocument

UnarchiveDocument
```

ni operaciones equivalentes.

Una evolución que incorpore nuevas transiciones requiere una
modificación explícita de los contratos correspondientes del
Aggregate.

---

# Independencia Tecnológica

La State Machine pertenece al dominio.

No depende de:

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

Ninguno de estos mecanismos determina DocumentStatus ni sus
transiciones.

---

# Definición de Éxito

La State Machine de **Document** formaliza el Lifecycle definido
para la versión 1.0.

Los estados oficiales son:

```text
Draft

Published

Archived
```

Las transiciones oficiales son:

```text
No Document → Draft

Draft → Published

Published → Archived
```

La State Machine garantiza que:

- todo Document comienza en Draft;
- Published solamente puede alcanzarse desde Draft;
- Archived solamente puede alcanzarse desde Published;
- Archived es terminal;
- no existen transiciones implícitas;
- DocumentStatus no se modifica directamente;
- toda transición válida preserva las Invariants;
- toda transición válida incrementa Version;
- toda transición válida produce el Domain Event correspondiente;
- una transición rechazada conserva estado y Version;
- una modificación que preserve DocumentStatus no constituye por
  sí misma una transición del Lifecycle;
- la State Machine no determina en qué estados pueden ejecutarse
  modificaciones que no cambian DocumentStatus;
- DocumentType permanece separado de DocumentStatus;
- otros Aggregates conservan sus propias State Machines;
- Infrastructure no determina el estado del dominio.

De esta forma, `DOMAIN-010B-State-Machine.md` establece
formalmente la máquina de estados del Aggregate **Document**
manteniendo el patrón consolidado de AURA Core.