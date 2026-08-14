# DOMAIN-010C — Document Commands

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

Definir los Commands oficiales mediante los cuales se expresan
intenciones de modificación sobre el Aggregate **Document**.

Los Commands representan solicitudes de comportamiento del dominio.

No representan hechos consumados.

La versión 1.0 reconoce los Commands establecidos por el Lifecycle
y la State Machine consolidados de Document:

```text
CreateDocument

PublishDocument

ArchiveDocument
```

Este documento no incorpora Commands adicionales para modificar
Content, DocumentType u otros atributos mientras dichos Commands no
formen parte explícita del modelo consolidado del Aggregate.

---

# Principios

Todo Command de Document debe cumplir:

- expresar una intención explícita del dominio;
- utilizar el lenguaje ubicuo de Document Management;
- ser procesado por la Aggregate Root Document;
- respetar el Lifecycle;
- respetar la State Machine;
- respetar las Invariants;
- respetar Permissions;
- respetar Versioning;
- actuar exclusivamente dentro del Consistency Boundary;
- no modificar directamente atributos internos;
- no modificar directamente otros Aggregates;
- producir un nuevo estado únicamente cuando la operación sea
  válida;
- producir el Domain Event correspondiente cuando el hecho ocurra.

Debe mantenerse:

```text
Command

=

Intent
```

y:

```text
Domain Event

=

Fact
```

Un Command aceptado no evita las reglas internas del Aggregate.

---

# Estructura General

Cada Command debe definir conceptualmente:

- objetivo;
- datos mínimos necesarios;
- precondiciones o validaciones;
- estado origen;
- estado destino;
- Domain Event esperado.

Conceptualmente:

```text
Command
    │
    ▼
Document
    │
    ├── Validate Current State
    ├── Validate Invariants
    └── Apply Domain Behavior
            │
            ▼
      Valid New State
            │
            ▼
       Domain Event
```

Cuando una validación falla:

```text
Command
    │
    ▼
  Rejected
```

sin modificación confirmada del Aggregate.

---

# CreateDocument

## Objetivo

Crear una nueva instancia válida del Aggregate Document.

`CreateDocument` expresa la intención de establecer formalmente la
existencia de un nuevo Document dentro del dominio.

---

## Datos mínimos

El Command debe proporcionar la información necesaria para
constituir un Document válido conforme a las Invariants iniciales.

Conceptualmente:

```text
DocumentId

DocumentType

Content
```

Los valores deben satisfacer las reglas propias de cada concepto.

DocumentStatus no se proporciona como una transición arbitraria.

El estado inicial está determinado por el Lifecycle.

---

## Precondiciones

Debe cumplirse:

- no existe previamente el mismo Document;
- DocumentId es válido;
- DocumentType es válido;
- Content satisface las reglas iniciales aplicables;
- las Invariants de creación se encuentran satisfechas.

La creación no puede utilizarse para establecer directamente un
estado diferente al estado inicial definido por el Lifecycle.

---

## Estado origen

```text
No Document
```

---

## Estado destino

```text
Draft
```

La transición corresponde a:

```text
No Document → Draft
```

---

## Evento esperado

Una creación válida produce:

```text
DocumentCreated
```

Si la creación es rechazada no debe producirse:

```text
DocumentCreated
```

---

# PublishDocument

## Objetivo

Expresar la intención de formalizar un Document Draft como
Published.

`PublishDocument` controla la transición:

```text
Draft → Published
```

---

## Datos mínimos

El Command debe identificar el Document sobre el cual se solicita
la publicación.

Conceptualmente:

```text
DocumentId
```

No introduce directamente un nuevo DocumentStatus.

La transición es responsabilidad de la Aggregate Root.

---

## Precondiciones

Debe cumplirse:

- Document existe;
- DocumentStatus es Draft;
- las Invariants requeridas para publicación están satisfechas.

La autorización para solicitar el Command no sustituye estas
validaciones.

---

## Estado origen

```text
Draft
```

---

## Estado destino

```text
Published
```

La transición corresponde a:

```text
Draft → Published
```

---

## Evento esperado

Una publicación válida produce:

```text
DocumentPublished
```

Cuando el Command sea rechazado no debe producirse:

```text
DocumentPublished
```

---

# ArchiveDocument

## Objetivo

Expresar la intención de retirar un Document Published de su ciclo
operativo y conservarlo como parte del historial del dominio.

`ArchiveDocument` controla la transición:

```text
Published → Archived
```

Archivar no significa eliminar.

---

## Datos mínimos

El Command debe identificar el Document sobre el cual se solicita
el archivado.

Conceptualmente:

```text
DocumentId
```

---

## Precondiciones

Debe cumplirse:

- Document existe;
- DocumentStatus es Published;
- las Invariants requeridas para archivado están satisfechas.

No puede utilizarse ArchiveDocument para realizar una transición
no definida por la State Machine.

---

## Estado origen

```text
Published
```

---

## Estado destino

```text
Archived
```

La transición corresponde a:

```text
Published → Archived
```

Archived es terminal dentro del Lifecycle versión 1.0.

---

## Evento esperado

Un archivado válido produce:

```text
DocumentArchived
```

Cuando el Command sea rechazado no debe producirse:

```text
DocumentArchived
```

---

# Rechazo de Commands

Todo Command debe ser rechazado cuando:

- el estado actual no permite la operación;
- la transición solicitada no pertenece a la State Machine;
- una Invariant no se cumple;
- la operación intentaría modificar directamente DocumentId;
- la operación intentaría evitar la Aggregate Root;
- la operación intentaría modificar directamente otro Aggregate;
- cualquier condición necesaria para mantener un Document válido no
  se encuentra satisfecha.

Ante un Command rechazado debe mantenerse:

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

Por ejemplo:

```text
DocumentStatus = Published

PublishDocument

↓

Rejected
```

porque:

```text
Published → Published
```

no constituye la transición controlada por PublishDocument.

Del mismo modo:

```text
DocumentStatus = Draft

ArchiveDocument

↓

Rejected
```

porque:

```text
Draft → Archived
```

no pertenece a la State Machine versión 1.0.

---

# Consistencia

Todo Command modifica exclusivamente una instancia del Aggregate:

```text
Document
```

Una operación válida debe:

- ejecutarse mediante la Aggregate Root;
- proteger las Invariants;
- respetar DocumentStatus;
- respetar la State Machine;
- mantener DocumentId;
- mantener el Consistency Boundary;
- incrementar Version;
- producir el Domain Event correspondiente.

Un Command de Document no modifica directamente:

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

Cada uno de esos conceptos conserva su propio Aggregate y su
propio límite de consistencia.

---

# Auditoría

Los Commands representan intenciones y no constituyen por sí mismos
el historial de hechos consumados del Aggregate.

La trazabilidad de una modificación aceptada se representa mediante
el Domain Event correspondiente.

Conceptualmente:

```text
Command

↓

Document

↓

Valid Domain Operation

↓

Domain Event
```

Una operación rechazada no debe registrarse como si el hecho de
dominio solicitado hubiese ocurrido.

Debe mantenerse:

```text
Rejected PublishDocument

≠

DocumentPublished
```

y:

```text
Rejected ArchiveDocument

≠

DocumentArchived
```

Audit permanece fuera del Consistency Boundary de Document.

---

# Compatibilidad

Los Commands definidos en este documento deben permanecer
coherentes con:

```text
DOMAIN-010-Aggregate.md

DOMAIN-010A-Lifecycle.md

DOMAIN-010B-State-Machine.md

DOMAIN-010D-Domain-Events.md

DOMAIN-010E-Invariants.md

DOMAIN-010F-Permissions.md

DOMAIN-010G-Repository-Contract.md

DOMAIN-010I-Versioning.md

DOMAIN-010J-Consistency-Boundary.md
```

Debe mantenerse:

```text
Command

↓

Aggregate Root

↓

Domain Validation

↓

Valid Modification

↓

Domain Event
```

Los Commands permanecen independientes de:

- mecanismos de persistencia;
- protocolos de transporte;
- APIs;
- bases de datos;
- frameworks;
- sistemas externos.

La forma técnica mediante la cual un Command llega a la capa de
aplicación no modifica su significado en el dominio.

---

# Definición de Éxito

Los Commands del Aggregate **Document** representan las intenciones
oficiales de modificación establecidas por el Lifecycle y la State
Machine versión 1.0.

El conjunto consolidado es:

```text
CreateDocument

PublishDocument

ArchiveDocument
```

Su relación con las transiciones y Domain Events es:

| Command | Estado origen | Estado destino | Domain Event |
| --- | --- | --- | --- |
| CreateDocument | No Document | Draft | DocumentCreated |
| PublishDocument | Draft | Published | DocumentPublished |
| ArchiveDocument | Published | Archived | DocumentArchived |

El modelo garantiza que:

- todo Command representa intención;
- toda operación es procesada por Document;
- CreateDocument produce un Document Draft cuando es válido;
- PublishDocument solamente opera desde Draft;
- ArchiveDocument solamente opera desde Published;
- Archived permanece terminal;
- ninguna transición implícita es introducida;
- ningún Command modifica DocumentStatus directamente;
- ningún Command modifica DocumentId;
- toda operación válida preserva las Invariants;
- toda operación válida incrementa Version;
- toda operación válida produce el Domain Event correspondiente;
- toda operación rechazada conserva estado y Version;
- toda operación rechazada no produce el Domain Event de éxito;
- ningún Command modifica directamente otros Aggregates;
- no se incorporan Commands adicionales sin una definición
  explícita del dominio.

De esta forma, `DOMAIN-010C-Commands.md` establece los Commands
oficiales del Aggregate **Document** manteniendo el patrón
consolidado de AURA Core.