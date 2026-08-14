# DOMAIN-010E — Document Invariants

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
- DOMAIN-010B-State-Machine.md
- DOMAIN-010C-Commands.md
- DOMAIN-010D-Domain-Events.md
- DOMAIN-010F-Permissions.md
- DOMAIN-010G-Repository-Contract.md
- DOMAIN-010I-Versioning.md
- DOMAIN-010J-Consistency-Boundary.md
- CORE-006-Domain-Invariants.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Definir formalmente las **Invariants** que deben mantenerse
siempre válidas dentro del Aggregate **Document**.

Las Invariants protegen la consistencia interna de Document antes
y después de cada operación aceptada por la Aggregate Root.

Ningún Command, transición de Lifecycle, modificación interna,
mecanismo de persistencia o integración puede dejar el Aggregate
en un estado que viole estas reglas.

Debe mantenerse:

```text
Valid Document Before

↓

Valid Domain Operation

↓

Valid Document After
```

Una operación que no pueda preservar las Invariants debe ser
rechazada.

---

# Principios

Las Invariants de Document cumplen los siguientes principios:

- pertenecen al dominio;
- son protegidas por la Aggregate Root;
- deben cumplirse durante toda la existencia del Aggregate;
- ninguna operación pública puede evitarlas;
- ninguna transición puede evitarlas;
- ninguna Permission puede evitarlas;
- ninguna implementación del Repository puede evitarlas;
- ninguna integración externa puede evitarlas;
- ninguna optimización puede evitarlas;
- deben mantenerse antes y después de toda modificación válida.

Debe mantenerse:

```text
Permission Granted

≠

Invariant Bypass
```

y:

```text
Infrastructure

≠

Domain Authority
```

---

# Invariantes Oficiales

La versión 1.0 establece las siguientes Invariants para Document:

- DocumentId siempre existe;
- DocumentId nunca cambia;
- DocumentType siempre debe ser válido;
- Content pertenece al Aggregate Document;
- Content solamente puede modificarse mediante comportamiento
  explícito de la Aggregate Root;
- DocumentStatus siempre debe pertenecer al conjunto oficial;
- todo Document nuevo comienza en Draft;
- Published solamente puede alcanzarse desde Draft;
- Archived solamente puede alcanzarse desde Published;
- Archived es terminal;
- toda transición debe pertenecer a la State Machine;
- ninguna transición puede realizarse modificando directamente
  DocumentStatus;
- ninguna modificación puede realizarse evitando la Aggregate Root;
- toda modificación válida incrementa Version;
- una operación rechazada no modifica el estado confirmado;
- una operación rechazada no incrementa Version;
- una operación rechazada no produce el Domain Event de éxito;
- todo Domain Event producido debe corresponder a un hecho
  efectivamente ocurrido;
- las relaciones con otros Aggregates utilizan identificadores y
  contratos explícitos;
- Document no modifica directamente otros Aggregates;
- las Invariants deben mantenerse antes y después de cada operación
  válida.

---

# Identidad

La identidad del Aggregate está determinada por:

```text
DocumentId
```

Debe cumplirse siempre:

```text
DocumentId != null
```

y durante toda la existencia del Aggregate:

```text
DocumentId Before

=

DocumentId After
```

Ninguna operación válida puede modificar DocumentId.

Los cambios de:

- DocumentType;
- Content;
- DocumentStatus;
- Version;

no producen una nueva identidad.

---

# DocumentType

Todo Document debe mantener un:

```text
DocumentType
```

válido conforme al lenguaje ubicuo de Document Management.

DocumentType representa naturaleza documental.

No representa:

- DocumentStatus;
- formato físico de archivo;
- mecanismo de almacenamiento;
- protocolo;
- tecnología.

Debe mantenerse:

```text
DocumentType

≠

DocumentStatus
```

Este documento no incorpora nuevos valores de DocumentType.

---

# Content

Content pertenece al estado protegido por Document.

Debe cumplirse:

- Content pertenece al Consistency Boundary del Aggregate;
- Content no puede modificarse directamente desde fuera de
  Document;
- toda modificación de Content debe realizarse mediante
  comportamiento explícito de la Aggregate Root;
- una modificación de Content debe mantener las demás Invariants
  del Aggregate;
- el mecanismo técnico utilizado para almacenar Content no modifica
  su significado de dominio.

Debe mantenerse:

```text
Content Mutation

↓

Document Aggregate Root

↓

Invariant Validation
```

Nunca:

```text
External Component

↓

Direct Content Mutation
```

Este documento no introduce reglas adicionales sobre estructura,
formato físico o tecnología de almacenamiento de Content.

---

# DocumentStatus

DocumentStatus siempre debe pertenecer al conjunto oficial:

```text
Draft

Published

Archived
```

Ningún otro estado forma parte de la versión 1.0.

Debe mantenerse:

```text
DocumentStatus

∈

{Draft, Published, Archived}
```

DocumentStatus no puede modificarse directamente.

Todo cambio debe producirse mediante una transición válida
controlada por Document.

---

# Estado Inicial

Todo Document creado válidamente debe comenzar en:

```text
Draft
```

Por lo tanto:

```text
CreateDocument

↓

DocumentStatus = Draft
```

No es válido crear directamente un Document en:

```text
Published

Archived
```

La creación válida produce:

```text
DocumentCreated
```

---

# Invariantes de Publicación

Published solamente puede alcanzarse mediante:

```text
Draft → Published
```

utilizando:

```text
PublishDocument
```

Debe cumplirse antes de la transición:

```text
DocumentStatus = Draft
```

Después de una publicación válida:

```text
DocumentStatus = Published
```

y debe producirse:

```text
DocumentPublished
```

No está permitido:

```text
Published → Published
```

mediante `PublishDocument`.

Tampoco:

```text
Archived → Published
```

---

# Invariantes de Archivado

Archived solamente puede alcanzarse mediante:

```text
Published → Archived
```

utilizando:

```text
ArchiveDocument
```

Debe cumplirse antes de la transición:

```text
DocumentStatus = Published
```

Después de un archivado válido:

```text
DocumentStatus = Archived
```

y debe producirse:

```text
DocumentArchived
```

No está permitido:

```text
Draft → Archived
```

ni:

```text
Archived → Archived
```

mediante `ArchiveDocument`.

---

# Archived

Archived constituye el estado terminal del Lifecycle versión 1.0.

Una vez alcanzado:

```text
DocumentStatus = Archived
```

no existe una transición ordinaria hacia otro estado.

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

Archived no significa:

```text
Deleted
```

El Document conserva su identidad y trazabilidad histórica.

---

# Lifecycle

Toda transición debe pertenecer al Lifecycle oficial:

```text
No Document → Draft

Draft → Published

Published → Archived
```

Ninguna operación puede introducir una transición adicional.

Las reglas completas se encuentran en:

```text
DOMAIN-010A-Lifecycle.md
```

---

# State Machine

Toda modificación de DocumentStatus debe corresponder a una
transición definida por:

```text
DOMAIN-010B-State-Machine.md
```

Debe mantenerse:

```text
Requested Transition

∈

Official State Machine
```

Si la transición solicitada no pertenece a la State Machine, la
operación debe ser rechazada.

---

# Commands

Los Commands oficiales establecidos para la versión 1.0 son:

```text
CreateDocument

PublishDocument

ArchiveDocument
```

Cada Command debe mantener las Invariants antes y después de su
ejecución.

La relación oficial es:

| Command | Estado origen | Estado destino |
| --- | --- | --- |
| CreateDocument | No Document | Draft |
| PublishDocument | Draft | Published |
| ArchiveDocument | Published | Archived |

Ningún Command puede:

- modificar DocumentId;
- modificar directamente DocumentStatus;
- evitar las Invariants;
- modificar directamente otro Aggregate.

Las reglas completas se encuentran en:

```text
DOMAIN-010C-Commands.md
```

---

# Domain Events

La versión 1.0 reconoce:

```text
DocumentCreated

DocumentPublished

DocumentArchived
```

Un Domain Event solamente puede producirse después de una
operación válida.

Debe mantenerse:

```text
Valid Command

↓

Valid Aggregate Modification

↓

Domain Event
```

Una operación rechazada no produce el Domain Event de éxito.

Por ejemplo:

```text
DocumentStatus = Published

PublishDocument

↓

Rejected
```

no puede producir:

```text
DocumentPublished
```

Las reglas completas pertenecen a:

```text
DOMAIN-010D-Domain-Events.md
```

---

# Version

Version representa la evolución lógica del Aggregate.

Toda modificación válida debe incrementar:

```text
Version
```

Conceptualmente:

```text
Version N

↓

Valid Modification

↓

Version N + 1
```

Una operación rechazada mantiene:

```text
Version N
```

Las operaciones de lectura no modifican Version.

La definición completa pertenece a:

```text
DOMAIN-010I-Versioning.md
```

---

# CreatedAt

CreatedAt representa el momento de creación del Document.

Una vez establecido:

```text
CreatedAt
```

no cambia durante la existencia del Aggregate.

Una modificación posterior no puede reinterpretar el momento de
creación.

---

# UpdatedAt

UpdatedAt solamente puede reflejar una modificación válida del
Aggregate.

Una operación rechazada no debe representar una modificación
confirmada de Document mediante UpdatedAt.

UpdatedAt no sustituye Version como mecanismo lógico de evolución
del Aggregate.

---

# Reglas de Modificación

Toda modificación debe cumplir:

- ninguna modificación directa de atributos;
- ninguna modificación fuera de la Aggregate Root;
- ninguna modificación de DocumentId;
- ninguna modificación de DocumentStatus fuera de la State Machine;
- ninguna modificación de Content evitando comportamiento de
  dominio;
- ninguna modificación que deje Document en un estado inválido;
- toda modificación válida incrementa Version;
- toda modificación relevante produce el Domain Event
  correspondiente;
- una modificación solamente afecta el Consistency Boundary de
  Document;
- ningún Aggregate externo es modificado directamente.

---

# Operaciones Rechazadas

Cuando una operación viola una Invariant debe ser rechazada.

Una operación rechazada debe mantener:

```text
Document State

=

Previous Document State
```

y:

```text
Version

=

Previous Version
```

No debe producirse el Domain Event de éxito correspondiente.

Debe mantenerse:

```text
Rejected Operation

↓

No Confirmed Domain Mutation
```

---

# Consistency Boundary

Las Invariants de Document solamente gobiernan el estado
perteneciente al Aggregate Document.

El límite comprende conceptualmente:

```text
Document
    │
    ├── Internal State
    ├── Content
    ├── Internal Entities
    ├── Value Objects
    └── Version
```

No comprende:

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

Document no puede proteger una Invariant propia modificando
directamente otro Aggregate.

La definición formal pertenece a:

```text
DOMAIN-010J-Consistency-Boundary.md
```

---

# Relaciones con Otros Aggregates

Las relaciones externas deben mantenerse mediante identificadores
y contratos explícitos.

Una relación externa no implica:

- composición;
- ownership del Aggregate externo;
- acceso directo al estado interno;
- autoridad para modificarlo;
- ampliación del Consistency Boundary.

Debe mantenerse:

```text
External Aggregate Reference

≠

Embedded External Aggregate
```

Document nunca modifica directamente el estado interno de otro
Aggregate.

---

# Assembly

Assembly puede relacionarse con Document mediante:

```text
DocumentId
```

Esta relación no permite que Assembly modifique directamente:

```text
DocumentStatus

Content

Version
```

Del mismo modo, Document no modifica directamente:

```text
AssemblyStatus
```

Cada Aggregate mantiene sus propias Invariants y su propio
Consistency Boundary.

---

# Voting

Voting puede relacionarse con Document mediante identificadores y
contratos explícitos.

Debe mantenerse:

```text
VotingStatus

≠

DocumentStatus
```

Una transición de Voting no constituye una transición automática
de Document.

Una transición de Document no constituye una transición automática
de Voting.

---

# Persistencia

El Repository debe persistir Document como una unidad de
consistencia.

No puede modificar directamente el Aggregate para producir un
estado que no haya sido aceptado por Document.

Debe mantenerse:

```text
Domain Behavior

↓

Valid Document

↓

Repository
```

Nunca:

```text
Repository

↓

Bypass Invariants
```

La persistencia de Content no modifica las reglas conceptuales del
Aggregate.

La definición formal pertenece a:

```text
DOMAIN-010G-Repository-Contract.md
```

---

# Independencia Tecnológica

Las Invariants de Document no dependen de:

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

Ninguna tecnología puede:

- crear nuevos estados;
- crear nuevas transiciones;
- modificar DocumentId;
- evitar la Aggregate Root;
- evitar Versioning;
- evitar las Invariants.

Las reglas del Aggregate pertenecen al dominio.

---

# Reglas

**INV-001**

Todo Document posee DocumentId.

**INV-002**

DocumentId es inmutable.

**INV-003**

DocumentType debe permanecer válido.

**INV-004**

Content pertenece al Aggregate y solamente puede modificarse
mediante comportamiento explícito de Document.

**INV-005**

DocumentStatus solamente puede ser:

```text
Draft

Published

Archived
```

**INV-006**

Todo Document nuevo comienza en Draft.

**INV-007**

Published solamente puede alcanzarse desde Draft.

**INV-008**

Archived solamente puede alcanzarse desde Published.

**INV-009**

Archived es terminal.

**INV-010**

Toda transición debe pertenecer a la State Machine.

**INV-011**

DocumentStatus nunca puede modificarse directamente.

**INV-012**

Toda modificación debe realizarse mediante la Aggregate Root.

**INV-013**

Toda modificación válida incrementa Version.

**INV-014**

Una operación rechazada no modifica el estado confirmado.

**INV-015**

Una operación rechazada no incrementa Version.

**INV-016**

Una operación rechazada no produce el Domain Event de éxito.

**INV-017**

Todo Domain Event debe representar un hecho efectivamente ocurrido.

**INV-018**

CreatedAt permanece inmutable después de la creación.

**INV-019**

Las relaciones externas no incorporan Aggregates externos dentro
de Document.

**INV-020**

Document no modifica directamente otros Aggregates.

**INV-021**

Las Invariants deben mantenerse antes y después de toda operación
válida.

---

# Definición de Éxito

Las Invariants del Aggregate **Document** garantizan que toda
instancia permanezca válida y consistente durante su Lifecycle.

El modelo garantiza:

- identidad inmutable mediante DocumentId;
- DocumentType válido;
- Content protegido por la Aggregate Root;
- DocumentStatus limitado al conjunto oficial;
- estado inicial Draft;
- transición Draft → Published;
- transición Published → Archived;
- estado Archived terminal;
- ausencia de transiciones implícitas;
- ausencia de modificación directa de DocumentStatus;
- ausencia de modificación directa de Content;
- incremento de Version para toda modificación válida;
- preservación de estado y Version ante operaciones rechazadas;
- ausencia de Domain Events de éxito ante operaciones rechazadas;
- correspondencia entre hechos ocurridos y Domain Events;
- preservación de CreatedAt;
- separación entre Document y otros Aggregates;
- Consistency Boundary explícito;
- independencia tecnológica.

Toda operación debe mantener:

```text
Valid Document Before

↓

Domain Operation

↓

Valid Document After
```

De esta forma, `DOMAIN-010E-Invariants.md` establece las
Invariants oficiales del Aggregate **Document**, preservando su
identidad, Lifecycle, State Machine, Versioning y Consistency
Boundary conforme al patrón consolidado de AURA Core.