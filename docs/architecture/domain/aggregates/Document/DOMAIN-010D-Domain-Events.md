# DOMAIN-010D — Document Domain Events

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
- DOMAIN-010E-Invariants.md
- DOMAIN-010F-Permissions.md
- DOMAIN-010I-Versioning.md
- DOMAIN-010J-Consistency-Boundary.md
- DOMAIN-010K-Integration-Events.md
- DOMAIN-010L-Read-Model.md
- DOMAIN-010M-Test-Scenarios.md
- DOMAIN-010O-Security-Model.md
- CORE-006-Domain-Invariants.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Definir formalmente los **Domain Events** producidos por el
Aggregate **Document**.

Los Domain Events representan hechos relevantes que ya ocurrieron
dentro del Consistency Boundary de Document como consecuencia de
comportamiento válido del dominio.

La versión 1.0 reconoce exclusivamente los hechos establecidos por
el Lifecycle, la State Machine y los Commands consolidados de
Document.

Este documento no introduce nuevos Commands, estados,
transiciones ni responsabilidades.

---

# Propósito

Los Domain Events permiten expresar mediante el lenguaje ubicuo los
hechos relevantes ocurridos durante la evolución de un Document.

Permiten representar conceptualmente:

```text
DocumentCreated

DocumentPublished

DocumentArchived
```

Cada Domain Event expresa algo que ya ocurrió.

Los eventos permiten:

- preservar trazabilidad;
- representar la evolución del Aggregate;
- comunicar hechos dentro del dominio;
- alimentar Read Models;
- soportar procesos posteriores;
- permitir integración desacoplada;
- mantener coherencia con Versioning;
- preservar el significado histórico del Aggregate.

Los Domain Events no modifican directamente otros Aggregates.

---

# Principio Fundamental

Un Domain Event representa:

```text
Fact
```

No representa:

```text
Intent
```

Por lo tanto:

```text
PublishDocument
```

representa un Command.

Mientras:

```text
DocumentPublished
```

representa un Domain Event.

La relación conceptual es:

```text
Command
    │
    ▼
Document
    │
    ├── valida estado
    ├── valida State Machine
    ├── valida Invariants
    └── ejecuta comportamiento
            │
            ▼
       Domain Event
```

El Domain Event solamente existe cuando el hecho ocurrió
válidamente.

---

# Commands versus Domain Events

Los Commands expresan intención en forma imperativa:

```text
CreateDocument

PublishDocument

ArchiveDocument
```

Los Domain Events expresan hechos consumados:

```text
DocumentCreated

DocumentPublished

DocumentArchived
```

Nunca debe utilizarse:

```text
DocumentPublished
```

como solicitud de publicación.

Tampoco debe utilizarse:

```text
PublishDocument
```

como registro histórico de que un Document fue publicado.

Debe mantenerse:

```text
Command

≠

Domain Event
```

---

# Propiedad del Evento

Los Domain Events definidos en este documento pertenecen
conceptualmente al Aggregate:

```text
Document
```

La Aggregate Root es responsable de producirlos cuando una
operación válida confirma el hecho correspondiente.

Otros Aggregates o Bounded Contexts pueden reaccionar
posteriormente a esos hechos.

No son propietarios del Domain Event original.

Debe mantenerse:

```text
Document Domain Event

=

Fact owned by Document
```

---

# Alcance

Los Domain Events de Document describen exclusivamente hechos
pertenecientes al Aggregate Document.

No representan directamente hechos internos de:

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

Cuando un hecho pertenece a otro Aggregate debe ser representado
por el Aggregate responsable.

Por ejemplo:

```text
DocumentPublished
```

no significa:

```text
NotificationSent
```

ni:

```text
AssemblyChanged
```

ni:

```text
VotingChanged
```

---

# Eventos Oficiales

La versión 1.0 define los siguientes Domain Events:

```text
DocumentCreated

DocumentPublished

DocumentArchived
```

Estos eventos corresponden exactamente a los hechos de Lifecycle
consolidados en:

```text
DOMAIN-010A-Lifecycle.md

DOMAIN-010B-State-Machine.md

DOMAIN-010C-Commands.md
```

No se incorporan Domain Events adicionales mediante este
documento.

---

# Categorías de Eventos

Los Domain Events definidos por la versión 1.0 pertenecen a:

```text
Lifecycle Events
```

Esta clasificación permite identificar que los eventos oficiales
actuales representan cambios relevantes dentro del Lifecycle de
Document.

La clasificación no modifica la identidad individual ni el
significado de cada evento.

---

# Lifecycle Events

Los Lifecycle Events oficiales son:

```text
DocumentCreated

DocumentPublished

DocumentArchived
```

Su relación con DocumentStatus es:

| Domain Event | Estado previo | Estado resultante |
| --- | --- | --- |
| DocumentCreated | No Document | Draft |
| DocumentPublished | Draft | Published |
| DocumentArchived | Published | Archived |

Ningún evento puede representar una transición no definida por la
State Machine.

---

# Estructura General

Todo Domain Event de Document debe contener conceptualmente como
mínimo:

```text
EventId

EventType

DocumentId

AggregateVersion

OccurredAt

CorrelationId

CausationId
```

Además contiene el Payload necesario para representar el hecho
correspondiente.

El Payload debe contener únicamente información con significado
para el hecho representado.

---

# EventId

EventId identifica de manera única un Domain Event.

```text
EventId
```

Debe:

- existir;
- ser único;
- ser inmutable;
- identificar un único hecho;
- no reutilizarse;
- permanecer independiente de DocumentId.

Dos hechos distintos no comparten el mismo EventId.

---

# EventType

EventType representa el nombre semántico del hecho ocurrido.

Ejemplos:

```text
DocumentCreated

DocumentPublished

DocumentArchived
```

EventType debe utilizar el lenguaje ubicuo del dominio.

No debe representar:

- tablas;
- endpoints;
- frameworks;
- mecanismos de persistencia;
- mecanismos de transporte;
- tecnologías de Infrastructure.

---

# DocumentId

DocumentId identifica el Aggregate que produjo el Domain Event.

```text
DocumentId
```

Permite relacionar el evento con:

```text
Document
```

DocumentId conserva el mismo significado que dentro del
Aggregate.

Un Domain Event no puede utilizar una identidad diferente para
representar el mismo Document.

---

# AggregateVersion

AggregateVersion representa la Version resultante del Aggregate
asociada al hecho producido.

```text
AggregateVersion
```

Toda modificación válida incrementa Version.

El Domain Event correspondiente debe mantener coherencia con la
Version resultante de esa modificación.

Conceptualmente:

```text
Valid Modification

↓

Version changes

↓

Domain Event

↓

AggregateVersion = resulting Version
```

La definición completa pertenece a:

```text
DOMAIN-010I-Versioning.md
```

---

# OccurredAt

OccurredAt representa el momento en que ocurrió el hecho de
dominio.

```text
OccurredAt
```

Pertenece al Domain Event.

No representa necesariamente:

- momento de persistencia;
- momento de entrega;
- momento de consumo;
- momento de proyección.

Representa temporalmente el hecho ocurrido dentro del dominio.

---

# CorrelationId

CorrelationId permite relacionar conceptualmente varios hechos que
pertenezcan al mismo flujo.

```text
CorrelationId
```

Su existencia permite mantener trazabilidad sin incorporar dentro
de Document los procesos completos que puedan reaccionar al hecho.

CorrelationId no modifica el significado del Domain Event.

---

# CausationId

CausationId identifica conceptualmente la causa inmediata del
Domain Event cuando corresponda.

```text
CausationId
```

Permite mantener la relación causal entre una intención aceptada y
el hecho resultante.

Conceptualmente:

```text
Command

↓

Causation

↓

Domain Event
```

CausationId no convierte el Command en parte del Domain Event.

---

# Event Payload

El Payload representa la información necesaria para describir el
hecho específico.

Debe:

- utilizar conceptos del dominio;
- contener información coherente con el hecho ocurrido;
- mantener DocumentId cuando corresponda;
- preservar valores históricos necesarios;
- evitar datos que no pertenezcan al significado del evento;
- evitar Aggregates externos completos;
- evitar información técnica de Infrastructure.

Debe mantenerse:

```text
Event Payload

≠

Complete Aggregate Snapshot
```

y:

```text
Event Payload

≠

Infrastructure Message
```

---

# Inmutabilidad

Un Domain Event representa un hecho ocurrido.

Por lo tanto, una vez producido:

```text
Domain Event
```

es inmutable.

No debe modificarse posteriormente para representar el estado
actual del Aggregate.

Si un hecho posterior cambia el estado de Document, dicho cambio
debe quedar representado por un nuevo hecho cuando corresponda.

---

# Historicidad

Los Domain Events preservan la historia de Document.

Un evento posterior no reescribe el significado de un evento
anterior.

Por ejemplo:

```text
DocumentCreated

↓

DocumentPublished

↓

DocumentArchived
```

conserva tres hechos diferentes.

`DocumentArchived` no significa que el Document nunca haya sido
Published.

`DocumentPublished` no elimina el hecho previo de creación.

Debe mantenerse:

```text
Past Fact

=

Preserved Past Fact
```

---

# DocumentCreated

## Definición

Representa el hecho de que un nuevo Document fue creado
válidamente dentro del dominio.

---

## Command origen

```text
CreateDocument
```

---

## Estado previo

No existe Aggregate.

Conceptualmente:

```text
No Document
```

---

## Estado resultante

```text
Draft
```

---

## Payload mínimo

```text
DocumentId

DocumentType

DocumentStatus

CreatedAt
```

El Payload representa la existencia inicial válida del Document.

No representa un snapshot completo del Aggregate.

---

## Invariantes

Antes de producir `DocumentCreated` debe haberse validado:

- DocumentId válido;
- DocumentType válido;
- estado inicial válido;
- Content válido conforme a las reglas de creación;
- Invariants iniciales satisfechas.

El estado resultante debe ser:

```text
Draft
```

---

## Significado

```text
DocumentCreated
```

significa:

```text
el Document existe formalmente dentro del dominio
```

No significa:

```text
el Document fue Published
```

Tampoco significa:

```text
el Document fue Archived
```

---

# DocumentPublished

## Definición

Representa el hecho de que un Document Draft alcanzó válidamente
la condición de Published.

---

## Command origen

```text
PublishDocument
```

---

## Estado previo

```text
Draft
```

---

## Estado resultante

```text
Published
```

---

## Payload mínimo

```text
DocumentId

PreviousStatus

DocumentStatus
```

Debe mantenerse:

```text
PreviousStatus = Draft
```

y:

```text
DocumentStatus = Published
```

---

## Invariantes

Antes de producir `DocumentPublished` debe haberse validado:

- Document existe;
- DocumentStatus previo es Draft;
- DocumentId permanece inmutable;
- las Invariants requeridas para publicación están satisfechas;
- la transición Draft → Published pertenece a la State Machine.

---

## Significado

```text
DocumentPublished
```

significa:

```text
el Document alcanzó formalmente Published dentro del dominio
```

No significa:

```text
NotificationSent
```

ni:

```text
ExternalSystemUpdated
```

ni una modificación automática de otro Aggregate.

---

# DocumentArchived

## Definición

Representa el hecho de que un Document Published fue retirado
válidamente de su ciclo operativo y pasó a su estado histórico
terminal.

---

## Command origen

```text
ArchiveDocument
```

---

## Estado previo

```text
Published
```

---

## Estado resultante

```text
Archived
```

---

## Payload mínimo

```text
DocumentId

PreviousStatus

DocumentStatus
```

Debe mantenerse:

```text
PreviousStatus = Published
```

y:

```text
DocumentStatus = Archived
```

---

## Invariantes

Antes de producir `DocumentArchived` debe haberse validado:

- Document existe;
- DocumentStatus previo es Published;
- DocumentId permanece inmutable;
- las Invariants requeridas para archivado están satisfechas;
- la transición Published → Archived pertenece a la State Machine.

---

## Significado

```text
DocumentArchived
```

significa:

```text
el Document pasó a su condición histórica terminal
```

No significa:

```text
DocumentDeleted
```

Archived conserva:

- DocumentId;
- identidad;
- historia;
- Version;
- hechos previamente ocurridos.

---

# Eventos Duplicados

Un mismo hecho de dominio no debe originar múltiples Domain Events
conceptualmente distintos que pretendan representar exactamente el
mismo hecho.

Cada hecho posee su propio:

```text
EventId
```

La repetición de una representación externa no crea por sí misma
un nuevo hecho dentro del Aggregate.

Debe mantenerse:

```text
Same Domain Fact

≠

New Domain Fact
```

---

# Nombres de Eventos

Los nombres de Domain Events deben:

- utilizar lenguaje ubicuo;
- representar hechos en pasado;
- describir el significado del dominio;
- evitar nombres técnicos;
- evitar nombres de infraestructura;
- evitar nombres ambiguos.

Correcto:

```text
DocumentCreated

DocumentPublished

DocumentArchived
```

Los nombres no deben representar intenciones.

---

# Granularidad de Eventos

Cada Domain Event debe representar un hecho con significado propio.

No debe utilizarse un evento genérico como sustituto de los hechos
específicos del dominio cuando ello destruya su significado.

Debe mantenerse:

```text
DocumentPublished
```

como hecho diferente de:

```text
DocumentArchived
```

aun cuando ambos modifiquen DocumentStatus.

La granularidad debe preservar el lenguaje ubicuo y la trazabilidad
histórica.

---

# Eventos Técnicos Prohibidos

No deben introducirse como Domain Events hechos puramente técnicos
como:

```text
DocumentRowInserted

DocumentDatabaseUpdated

DocumentCacheInvalidated

DocumentHttpRequestProcessed

DocumentFileStored
```

cuando dichos nombres representen exclusivamente mecanismos de
Infrastructure.

Un Domain Event representa un hecho del dominio.

No representa una operación técnica.

---

# Eventos Futuros

La versión 1.0 reconoce exclusivamente:

```text
DocumentCreated

DocumentPublished

DocumentArchived
```

Nuevos Domain Events solamente pueden incorporarse cuando exista
un nuevo hecho explícito del dominio Document.

No debe agregarse un nuevo evento únicamente por conveniencia de:

- persistencia;
- transporte;
- integración;
- UI;
- reporting;
- Infrastructure.

Una nueva necesidad externa no constituye automáticamente un nuevo
Domain Event.

---

# Regla para Incorporar un Nuevo Domain Event

Un nuevo Domain Event debe incorporarse únicamente cuando:

- exista un hecho nuevo del dominio;
- el hecho pertenezca a Document;
- el hecho pueda expresarse mediante lenguaje ubicuo;
- la operación que lo produce esté definida explícitamente;
- las Invariants correspondientes estén establecidas;
- su relación con Lifecycle y State Machine esté definida cuando
  corresponda;
- su impacto sobre Versioning sea coherente;
- su impacto sobre contratos relacionados sea evaluado.

No debe utilizarse un Domain Event para introducir indirectamente
una decisión de arquitectura no definida.

---

# Impacto de un Nuevo Evento

Antes de incorporar un nuevo Domain Event debe revisarse su
coherencia con:

```text
DOMAIN-010-Aggregate.md

DOMAIN-010A-Lifecycle.md

DOMAIN-010B-State-Machine.md

DOMAIN-010C-Commands.md

DOMAIN-010E-Invariants.md

DOMAIN-010F-Permissions.md

DOMAIN-010I-Versioning.md

DOMAIN-010J-Consistency-Boundary.md

DOMAIN-010K-Integration-Events.md

DOMAIN-010L-Read-Model.md

DOMAIN-010M-Test-Scenarios.md

DOMAIN-010O-Security-Model.md
```

cuando corresponda.

Un evento no debe agregarse de forma aislada rompiendo la
consistencia documental del Aggregate.

---

# No Event on Failure

Una operación rechazada nunca produce el Domain Event de éxito.

Ejemplo:

```text
DocumentStatus = Published

PublishDocument
```

debe resultar:

```text
Rejected
```

y no debe producir:

```text
DocumentPublished
```

Del mismo modo:

```text
DocumentStatus = Draft

ArchiveDocument
```

no debe producir:

```text
DocumentArchived
```

porque:

```text
Draft → Archived
```

no pertenece a la State Machine.

---

# Auditoría

Los Domain Events representan hechos auditables del Aggregate.

Conceptualmente permiten relacionar:

```text
EventId

EventType

DocumentId

AggregateVersion

OccurredAt

CorrelationId

CausationId
```

Audit puede reaccionar posteriormente a estos hechos conforme a sus
propios contratos.

Audit no modifica el Domain Event original.

Audit permanece fuera del Consistency Boundary de Document.

---

# Trazabilidad Causal

Los Domain Events permiten mantener la relación entre una intención
válida y el hecho producido.

Conceptualmente:

```text
PublishDocument
      │
      ▼
DocumentPublished
```

CausationId permite mantener la relación causal correspondiente.

CorrelationId permite relacionar el evento con un flujo más amplio
cuando corresponda.

La trazabilidad no requiere incorporar dentro de Document los
Aggregates o procesos externos que posteriormente reaccionen.

---

# Ejemplo de Flujo Completo

```text
CreateDocument
      │
      ▼
DocumentCreated
      │
      ▼
Status = Draft

PublishDocument
      │
      ▼
DocumentPublished
      │
      ▼
Status = Published

ArchiveDocument
      │
      ▼
DocumentArchived
      │
      ▼
Status = Archived
```

La secuencia representa hechos distintos.

Cada evento preserva su propio significado histórico.

---

# Relación con Lifecycle

Los eventos de transición deben preservar la semántica definida en:

```text
DOMAIN-010A-Lifecycle.md
```

Relación oficial:

```text
DocumentCreated

No Document → Draft
```

```text
DocumentPublished

Draft → Published
```

```text
DocumentArchived

Published → Archived
```

Un evento no puede reinterpretar una transición diferente de la
definida por el Lifecycle.

---

# Relación con State Machine

Los Domain Events de cambio de estado solamente pueden producirse
después de transiciones permitidas por:

```text
DOMAIN-010B-State-Machine.md
```

Un Domain Event no puede utilizarse para introducir una transición
no permitida.

Debe mantenerse:

```text
Valid State Transition

↓

Domain Event
```

No:

```text
Domain Event

↓

Invent New State Transition
```

---

# Relación con Commands

Cada evento oficial corresponde a un Command consolidado:

| Command | Domain Event |
| --- | --- |
| CreateDocument | DocumentCreated |
| PublishDocument | DocumentPublished |
| ArchiveDocument | DocumentArchived |

La definición de Commands pertenece a:

```text
DOMAIN-010C-Commands.md
```

Command y Domain Event deben permanecer semánticamente separados y
coherentes.

---

# Relación con Invariants

Ningún Domain Event puede representar un estado que viole:

```text
DOMAIN-010E-Invariants.md
```

Por ejemplo:

```text
DocumentArchived
```

no puede existir válidamente como resultado directo de:

```text
Draft → Archived
```

porque esa transición no pertenece a la State Machine versión 1.0.

Las Invariants deben encontrarse satisfechas antes y después de la
operación que produce el evento.

---

# Relación con Permissions

Permissions determinan quién puede solicitar las operaciones
correspondientes.

Su definición pertenece a:

```text
DOMAIN-010F-Permissions.md
```

Los Domain Events no contienen lógica de autorización.

Representan hechos posteriores a la evaluación de autorización y a
la validación de las reglas del Aggregate.

Debe mantenerse:

```text
Permission

≠

Domain Event
```

---

# Relación con Versioning

Todo Domain Event debe mantener una relación coherente con:

```text
DOMAIN-010I-Versioning.md
```

Toda modificación válida incrementa Version.

El evento producido representa la AggregateVersion resultante de
dicha modificación.

Una operación rechazada:

- no incrementa Version;
- no produce el Domain Event de éxito.

---

# Relación con Consistency Boundary

Los Domain Events permiten comunicar hechos fuera de Document sin
expandir su Consistency Boundary.

La definición pertenece a:

```text
DOMAIN-010J-Consistency-Boundary.md
```

Un Domain Event de Document no modifica directamente:

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

Cada Aggregate conserva su propia autoridad de escritura.

---

# Relación con Integration Events

Los Domain Events que necesiten comunicar hechos fuera del Bounded
Context pueden participar en la generación de Integration Events
conforme a:

```text
DOMAIN-010K-Integration-Events.md
```

Domain Event e Integration Event permanecen separados.

Debe mantenerse:

```text
Domain Event

≠

Integration Event
```

No todo Domain Event requiere automáticamente un Integration
Event.

La selección de hechos expuestos externamente pertenece al contrato
de Integration Events.

---

# Relación con Read Model

Las proyecciones definidas en:

```text
DOMAIN-010L-Read-Model.md
```

pueden consumir Domain Events para representar el estado derivado
de Document.

Conceptualmente:

```text
Domain Event

↓

Projection

↓

Read Model
```

Los Read Models:

- no modifican Document;
- no generan transiciones;
- no reemplazan el Aggregate;
- no constituyen fuente de verdad de escritura.

---

# Relación con Test Scenarios

Los escenarios definidos en:

```text
DOMAIN-010M-Test-Scenarios.md
```

deben permitir comprobar como mínimo:

- tipo correcto del evento;
- Payload coherente;
- DocumentId correcto;
- AggregateVersion correcta;
- causalidad coherente;
- correlación coherente;
- evento producido después de un Command válido;
- ausencia del evento de éxito después de un Command rechazado;
- preservación de valores históricos.

Cada evento debe mantener la semántica definida en este documento.

---

# Relación con Security Model

Los Domain Events deben respetar:

```text
DOMAIN-010O-Security-Model.md
```

Un Domain Event no debe utilizarse para transportar secretos,
credenciales o información técnica de seguridad que no pertenezca
al hecho del dominio.

La seguridad no modifica el significado histórico del evento.

---

# Compatibilidad Arquitectónica

El modelo de Domain Events de Document mantiene compatibilidad con:

- Domain-Driven Design;
- Aggregate Pattern;
- Clean Architecture;
- Hexagonal Architecture;
- CQRS;
- Event-Driven Architecture;
- Event Sourcing Compatible;
- Optimistic Concurrency;
- Consistency Boundary;
- independencia tecnológica.

Esta compatibilidad no introduce dependencias concretas con
Infrastructure.

Los Domain Events pertenecen al dominio.

---

# Definición de Éxito

Los Domain Events del Aggregate **Document** representan de manera
explícita los hechos oficiales derivados de su Lifecycle versión
1.0:

```text
DocumentCreated

DocumentPublished

DocumentArchived
```

Cada evento:

- representa un hecho consumado;
- pertenece al Aggregate Document;
- mantiene EventId propio;
- mantiene DocumentId;
- mantiene AggregateVersion coherente;
- registra OccurredAt;
- permite correlación y causalidad;
- utiliza un Payload con significado de dominio;
- permanece inmutable;
- preserva historicidad;
- no representa Commands;
- no introduce nuevas transiciones;
- no modifica otros Aggregates;
- no reemplaza Integration Events;
- puede alimentar Read Models;
- puede ser utilizado por Audit sin ampliar el Consistency
  Boundary;
- solamente se produce después de comportamiento válido del
  Aggregate;
- no se produce como evento de éxito cuando la operación es
  rechazada.

La relación oficial permanece:

```text
CreateDocument
      │
      ▼
DocumentCreated

PublishDocument
      │
      ▼
DocumentPublished

ArchiveDocument
      │
      ▼
DocumentArchived
```

De esta forma, `DOMAIN-010D-Domain-Events.md` establece los Domain
Events oficiales del Aggregate **Document**, preservando el
lenguaje ubicuo, la trazabilidad histórica, las Invariants, la
State Machine, Versioning y el Consistency Boundary consolidado de
AURA Core.