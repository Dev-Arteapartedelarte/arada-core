# DOMAIN-012A — Audit Lifecycle

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Audit Management

Aggregate:
Audit

Documento relacionado:

- DOMAIN-012-Aggregate.md
- DOMAIN-012B-State-Machine.md
- DOMAIN-012D-Domain-Events.md
- DOMAIN-012E-Invariants.md

---

# Objetivo

Este documento define el ciclo de vida oficial del Aggregate
**Audit**.

Describe la evolución funcional de una unidad Audit desde la
inexistencia hasta la existencia de una representación auditable
confirmada dentro del ecosistema AURA.

Audit representa hechos que ya ocurrieron.

Por esta razón, su Lifecycle no representa el ciclo de vida del
Aggregate originador ni reproduce los estados del proceso que
produjo el hecho auditado.

Debe mantenerse:

```text
Source Aggregate Lifecycle

≠

Audit Lifecycle
```

Las reglas exhaustivas de transición se documentan formalmente en:

```text
DOMAIN-012B-State-Machine.md
```

---

# Principios

El Lifecycle de Audit debe garantizar:

- identidad única;
- trazabilidad;
- preservación del hecho auditado;
- independencia respecto del Aggregate originador;
- inmutabilidad del significado histórico;
- cumplimiento de Invariants;
- Versioning coherente;
- consistencia propia;
- compatibilidad con CQRS;
- compatibilidad con Event Sourcing.

---

# Principio Fundamental

Audit existe como consecuencia de un hecho ya confirmado.

Conceptualmente:

```text
Source Aggregate

    │
    ▼

Confirmed Fact

    │
    ▼

Audit Management

    │
    ▼

Audit
```

El Lifecycle de Audit comienza únicamente después de existir un
hecho auditable válido.

Debe mantenerse:

```text
Audit

≠

Source Fact Preparation
```

y:

```text
Audit

≠

Source Fact Execution
```

---

# Naturaleza del Lifecycle

El Aggregate Audit no representa un proceso operacional con etapas
sucesivas equivalentes a:

```text
Draft

Pending

Active

Completed
```

La versión 1.0 representa una unidad histórica confirmada.

Por lo tanto, su Lifecycle funcional es deliberadamente mínimo.

---

# Etapas del ciclo de vida

El Aggregate Audit evoluciona conceptualmente mediante:

```text
No Audit
    │
    ▼
Recorded
```

`Recorded` constituye el único estado oficial del Lifecycle de
Audit versión 1.0.

---

# No Audit

Representa la inexistencia de una unidad Audit para el hecho que
todavía no ha sido incorporado como representación auditable por
Audit Management.

No constituye un estado persistido del Aggregate.

Conceptualmente:

```text
No Audit

=

Aggregate Does Not Exist
```

---

# Recorded

`Recorded` representa una unidad Audit que existe formalmente y
preserva una representación auditable de un hecho ya confirmado.

En este estado:

- Audit posee AuditId;
- la identidad permanece inmutable;
- la referencia al hecho originador permanece preservada;
- la información histórica confirmada conserva su significado;
- Audit mantiene su propia Version;
- CreatedAt permanece preservado;
- el Aggregate puede ser consultado;
- no se modifica el Aggregate originador;
- no se modifica el Domain Event originador;
- no se reinterpreta retrospectivamente el hecho auditado.

Debe mantenerse:

```text
Recorded

=

Confirmed Audit Representation
```

---

# Estado Inicial

Toda unidad Audit nueva comienza directamente en:

```text
Recorded
```

No existe un estado:

```text
Draft
```

en la versión 1.0.

Un Audit incompleto o todavía no aceptado no constituye una unidad
Audit confirmada.

---

# Razón del Estado Inicial

Audit representa hechos ya ocurridos.

Por lo tanto, no necesita una etapa previa de preparación dentro del
Aggregate.

Debe mantenerse:

```text
Source Fact Confirmed

    │
    ▼

Audit Accepted

    │
    ▼

Recorded
```

y no:

```text
Draft Audit

    │
    ▼

Wait for Source Fact
```

El hecho de origen debe existir antes que su representación Audit.

---

# Estado Terminal

`Recorded` es terminal para el Lifecycle versión 1.0.

Una unidad Audit ya registrada no cambia hacia otro estado
operacional.

Debe mantenerse:

```text
Recorded

=

Terminal State
```

La condición terminal protege el carácter histórico de la unidad
auditable.

---

# Ausencia de Transiciones Posteriores

La versión 1.0 no define transiciones desde:

```text
Recorded
```

hacia ningún otro estado.

No existen oficialmente:

```text
Recorded → Draft

Recorded → Active

Recorded → Archived

Recorded → Deleted

Recorded → Cancelled
```

ni transiciones equivalentes.

---

# Archived

La versión 1.0 no incorpora:

```text
Archived
```

como estado del Lifecycle de Audit.

La naturaleza histórica del Aggregate no permite inferir
automáticamente un estado Archived.

Las políticas de archivo o retención deberán definirse
explícitamente antes de formar parte del dominio.

---

# Deleted

La versión 1.0 no incorpora:

```text
Deleted
```

como estado.

La eliminación física no constituye una transición del Lifecycle.

Debe mantenerse:

```text
Physical Deletion

≠

Audit Lifecycle State
```

Las políticas de eliminación pertenecen a decisiones explícitas de
retención, cumplimiento o Infrastructure cuando corresponda.

---

# Cancelled

La versión 1.0 no incorpora:

```text
Cancelled
```

como estado.

Una unidad Audit representa un hecho ya ocurrido.

No existe una cancelación retrospectiva del hecho auditado mediante
Audit.

Debe mantenerse:

```text
Audit Cancellation

≠

Source Fact Cancellation
```

---

# Active

La versión 1.0 no incorpora:

```text
Active
```

como estado.

Audit no representa una unidad operativa activa.

Representa una unidad de trazabilidad ya confirmada.

---

# Pending

La versión 1.0 no incorpora:

```text
Pending
```

como estado.

La espera técnica para procesar un hecho pertenece a mecanismos
externos al Aggregate.

Debe mantenerse:

```text
Pending Technical Processing

≠

AuditStatus
```

---

# Failed

La versión 1.0 no incorpora:

```text
Failed
```

como estado.

Un fallo técnico al intentar procesar, persistir o transportar
información auditable no constituye estado del Aggregate.

Debe mantenerse:

```text
ProcessingFailure

≠

AuditStatus
```

y:

```text
PersistenceFailure

≠

AuditStatus
```

---

# Flujo Oficial

El flujo completo versión 1.0 es:

```text
Confirmed Source Fact
        │
        ▼
  Audit Management
        │
        ▼
     No Audit
        │
        ▼
     Recorded
```

Una vez alcanzado:

```text
Recorded
```

no existe otra transición de Lifecycle oficial.

---

# Hecho de Origen

El hecho originador debe haber ocurrido antes de que Audit pueda
existir.

Debe mantenerse:

```text
Source Fact

before

Audit Representation
```

Audit no puede anticipar un hecho futuro.

---

# Source Domain Event

Cuando el origen sea un Domain Event:

```text
Source Domain Event

    │
    ▼

Confirmed Fact

    │
    ▼

Audit Management

    │
    ▼

Recorded Audit
```

El evento continúa perteneciendo al Aggregate originador.

Audit mantiene su propia representación.

---

# Independencia del Aggregate Originador

El estado del Aggregate originador puede continuar evolucionando
después de haberse creado una unidad Audit.

Por ejemplo:

```text
Source Aggregate vN

    │
    ▼

Confirmed Domain Event

    │
    ▼

Audit Recorded
```

posteriormente:

```text
Source Aggregate vN+1
```

no modifica retrospectivamente la unidad Audit ya registrada.

---

# Inmutabilidad Histórica

Una vez Recorded, Audit preserva el significado del hecho recibido.

No puede utilizarse una modificación posterior para hacer que el
registro represente un hecho diferente.

Debe mantenerse:

```text
Recorded Fact Meaning

=

Stable Historical Meaning
```

---

# Correcciones del Aggregate Originador

Si el Aggregate originador produce posteriormente un nuevo hecho
que corrige, complementa o modifica su propio estado, dicho hecho es
conceptualmente independiente del Audit anterior.

Audit no reescribe el registro previo para simular que el hecho
original nunca ocurrió.

Debe mantenerse:

```text
New Source Fact

≠

Rewrite Previous Audit
```

---

# Trazabilidad Acumulativa

Múltiples hechos confirmados del mismo Aggregate originador pueden
producir múltiples unidades Audit independientes.

Conceptualmente:

```text
Source Fact A
    │
    ▼
Audit A

Source Fact B
    │
    ▼
Audit B

Source Fact C
    │
    ▼
Audit C
```

Cada unidad mantiene:

```text
Independent AuditId
```

---

# AuditId

AuditId permanece inmutable durante todo el Lifecycle.

Debe mantenerse:

```text
AuditId at Recorded

=

AuditId for Entire Aggregate Existence
```

Ninguna evolución del Aggregate originador modifica AuditId.

---

# Source References

Las referencias al origen preservadas al alcanzar Recorded no
transfieren ownership.

Debe mantenerse:

```text
SourceAggregateId

≠

AuditId
```

y, cuando corresponda:

```text
SourceEventId

≠

AuditId
```

---

# OccurredAt

Cuando el hecho de origen proporciona:

```text
OccurredAt
```

Audit puede preservarlo como información del hecho auditado.

Debe mantenerse separado de:

```text
Audit.CreatedAt
```

porque representan momentos conceptualmente distintos.

---

# CreatedAt

CreatedAt representa la creación de la unidad Audit.

Una vez Recorded:

```text
CreatedAt
```

permanece inmutable.

---

# UpdatedAt

El Lifecycle versión 1.0 no define una transición posterior que
requiera modificar el estado operativo de Audit.

UpdatedAt continúa sujeto a las reglas generales del Aggregate y
solamente puede cambiar como consecuencia de una modificación válida
que sea definida explícitamente por el dominio.

La existencia de UpdatedAt no crea por sí sola una transición de
Lifecycle.

---

# Version

La creación válida de una unidad Audit establece su evolución
lógica inicial.

Conforme al patrón consolidado de AURA:

```text
Recorded Audit

Version = 1
```

Las reglas exhaustivas de Versioning se documentan en:

```text
DOMAIN-012I-Versioning.md
```

---

# Version del Aggregate Originador

Cuando esté disponible:

```text
SourceAggregateVersion
```

representa la Version asociada al hecho originador.

No representa la Version de Audit.

Debe mantenerse:

```text
SourceAggregateVersion

≠

Audit.Version
```

---

# Consistencia

La transición:

```text
No Audit → Recorded
```

debe producir una unidad Audit internamente consistente.

No puede confirmarse parcialmente.

Deben preservarse:

- AuditId;
- referencias de origen aplicables;
- información auditable requerida;
- Version;
- CreatedAt;
- Invariants.

---

# Consistency Boundary

El Lifecycle de Audit pertenece exclusivamente a:

```text
Audit
```

No modifica atómicamente:

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

Document

Notification

Integration
```

Debe mantenerse:

```text
Audit Lifecycle Transition

≠

Source Aggregate Lifecycle Transition
```

---

# Consistencia Eventual

Puede existir una ventana temporal entre:

```text
Source Fact Confirmed
```

y:

```text
Audit Recorded
```

Esta ventana es compatible con el Consistency Boundary independiente
de Audit.

Debe mantenerse:

```text
Source Aggregate Commit

≠

Audit Commit
```

---

# Fallo de Procesamiento

Si un hecho confirmado todavía no puede incorporarse válidamente a
Audit debido a un fallo técnico:

```text
Source Fact Confirmed

    │
    ▼

Processing Failure

    │
    ▼

No Confirmed Audit
```

El Source Fact permanece confirmado.

Debe mantenerse:

```text
Audit Processing Failure

≠

Source Aggregate Rollback
```

---

# Reintentos Técnicos

Los reintentos técnicos destinados a procesar un hecho auditable no
constituyen transiciones del Aggregate.

Debe mantenerse:

```text
Technical Retry

≠

Audit Lifecycle Transition
```

Hasta que exista una unidad Audit confirmada, el Aggregate no se
considera Recorded.

---

# Duplicados Técnicos

La recepción repetida del mismo mensaje técnico no representa
múltiples hechos de origen.

Debe mantenerse:

```text
Duplicate Technical Delivery

≠

New Source Fact
```

La estrategia concreta de idempotencia se define en las capas
correspondientes.

El Lifecycle no crea estados adicionales para representar
duplicados.

---

# Domain Events

Los Domain Events propios de Audit se definen formalmente en:

```text
DOMAIN-012D-Domain-Events.md
```

Este Lifecycle no introduce nombres concretos de Domain Events.

Debe mantenerse:

```text
Lifecycle State

≠

Permission to Infer Event Name
```

y:

```text
Source Domain Event

≠

Audit Domain Event
```

---

# Commands

Los Commands oficiales se definen en:

```text
DOMAIN-012C-Commands.md
```

Este documento no introduce nombres concretos de Commands.

La existencia de:

```text
No Audit → Recorded
```

establece la transición del Lifecycle.

El nombre de la intención que produzca dicha transición pertenece a
la especificación formal de Commands.

---

# State Machine

La State Machine debe formalizar exactamente el Lifecycle:

```text
No Audit → Recorded
```

sin introducir estados adicionales.

La definición exhaustiva pertenece a:

```text
DOMAIN-012B-State-Machine.md
```

---

# Invariants

Durante todo el Lifecycle deben preservarse como mínimo:

- AuditId existe una vez creado el Aggregate;
- AuditId nunca cambia;
- el hecho auditado ya ocurrió;
- Audit no modifica el hecho originador;
- Audit no modifica el Aggregate originador;
- las referencias externas no incorporan Aggregates completos;
- la información faltante no se inventa;
- SourceAggregateVersion y Audit.Version permanecen independientes;
- CreatedAt permanece inmutable;
- toda modificación válida incrementa Version;
- toda operación rechazada conserva Version;
- Recorded permanece terminal en la versión 1.0.

La especificación completa se encuentra en:

```text
DOMAIN-012E-Invariants.md
```

---

# Modificación

El Lifecycle versión 1.0 no define modificaciones ordinarias que
cambien:

```text
Recorded
```

hacia otro estado.

La existencia futura de comportamiento que modifique información de
Audit no autoriza automáticamente un cambio de Lifecycle.

Toda modificación futura debe respetar:

- identidad;
- significado histórico;
- Invariants;
- Versioning;
- State Machine;
- trazabilidad.

---

# Eliminación

La eliminación física no forma parte del Lifecycle versión 1.0.

Debe mantenerse:

```text
Recorded

≠

Physically Deleted
```

como transición de dominio.

Las reglas de retención, eliminación o anonimización deberán
establecerse explícitamente antes de incorporarse al modelo.

---

# Retención

El Lifecycle no establece:

- período mínimo de retención;
- período máximo de retención;
- expiración;
- archivado automático;
- eliminación automática.

Ninguna de estas políticas debe inferirse desde el estado Recorded.

---

# Read Models

Recorded puede ser proyectado hacia Read Models para consultas de
trazabilidad.

Conceptualmente:

```text
Audit Recorded

    │
    ▼

Projection

    │
    ▼

Audit Read Model
```

La proyección no modifica el Lifecycle.

---

# CQRS

En el Write Side:

```text
No Audit

    │
    ▼

Valid Domain Behavior

    │
    ▼

Recorded
```

En el Read Side:

```text
Confirmed Audit Facts

    │
    ▼

Projection

    │
    ▼

Read Model
```

El Read Model no puede cambiar Recorded ni crear transiciones.

---

# Event Sourcing

Audit permanece compatible con Event Sourcing.

La compatibilidad no obliga a utilizarlo.

Si se utiliza, la reconstrucción debe preservar el estado
confirmado:

```text
Recorded
```

sin generar nuevamente comportamiento de dominio.

Los Domain Events propios necesarios para dicha reconstrucción
deberán definirse en:

```text
DOMAIN-012D-Domain-Events.md
```

---

# Rehidratación

Rehidratar un Audit Recorded:

- no crea un nuevo Audit;
- no crea una nueva transición;
- no incrementa Version;
- no modifica CreatedAt;
- no modifica el hecho auditado;
- no produce nuevos Domain Events.

Debe mantenerse:

```text
Rehydration

≠

Lifecycle Transition
```

---

# Integración

La publicación de un Integration Event no constituye una transición
del Lifecycle.

Debe mantenerse:

```text
Integration Event Publication

≠

Audit State Change
```

Audit permanece Recorded independientemente del procesamiento
posterior realizado por consumidores externos.

---

# Audit y Notification

Un hecho proveniente de Notification puede originar una unidad
Audit.

Conceptualmente:

```text
Notification Domain Fact

    │
    ▼

Audit Management

    │
    ▼

Recorded
```

El estado de Notification permanece independiente.

---

# Audit y Assembly

Un Domain Event de Assembly puede constituir un hecho auditable.

Conceptualmente:

```text
Assembly Domain Event

    │
    ▼

Audit Management

    │
    ▼

Recorded
```

Assembly no espera a que Audit alcance Recorded para confirmar su
propio hecho.

---

# Audit y Document

Un hecho de Document puede originar Audit.

Audit Recorded no modifica:

```text
DocumentStatus

Document.Version

Document Lifecycle
```

---

# Audit y Voting

Un hecho confirmado de Voting puede originar Audit.

Audit Recorded no:

- abre Voting;
- cierra Voting;
- modifica votos;
- modifica resultados;
- modifica VotingStatus.

---

# Audit y Source Aggregate Lifecycle

Un mismo Source Aggregate puede producir hechos auditables en
distintas etapas de su propio Lifecycle.

Por ejemplo:

```text
Source State A
    │
    ▼
Source Fact A
    │
    ▼
Audit A = Recorded

Source State B
    │
    ▼
Source Fact B
    │
    ▼
Audit B = Recorded
```

Audit A y Audit B mantienen Lifecycle independiente.

---

# No Herencia de Estado

Audit no hereda el estado del Aggregate originador.

Si un hecho proviene de:

```text
NotificationStatus = Failed
```

el Audit correspondiente no adquiere:

```text
AuditStatus = Failed
```

Si un hecho proviene de:

```text
DocumentStatus = Archived
```

el Audit correspondiente no adquiere:

```text
AuditStatus = Archived
```

Debe mantenerse:

```text
Source Status

≠

Audit Status
```

---

# Estados Técnicos

Estados técnicos como:

```text
Queued

Processing

Retrying

DeliveryFailed

Persisting

Published
```

no forman parte del Lifecycle de Audit versión 1.0.

Pertenecen a procesos externos cuando correspondan.

---

# Reglas Generales

Durante el Lifecycle se cumplen las siguientes reglas:

- Audit solamente existe después de un hecho auditable confirmado;
- toda unidad Audit comienza en Recorded;
- Recorded es terminal;
- no existe Draft;
- no existe Pending;
- no existe Active;
- no existe Failed;
- no existe Cancelled;
- no existe Archived;
- no existe Deleted;
- AuditId nunca cambia;
- el hecho auditado no se reescribe;
- el Aggregate originador no se modifica;
- el Domain Event originador no se modifica;
- SourceAggregateVersion y Audit.Version permanecen independientes;
- CreatedAt permanece inmutable;
- la creación válida establece Version inicial conforme al patrón
  AURA;
- fallos técnicos no crean estados de dominio;
- reintentos técnicos no crean transiciones;
- publicación de Integration Events no cambia el estado;
- Read Models no modifican el Lifecycle;
- Audit mantiene consistencia independiente del Aggregate
  originador.

---

# Diagrama Completo

```text
┌───────────────────────────────┐
│      Source Aggregate         │
└───────────────┬───────────────┘
                │
                ▼
     ┌─────────────────────┐
     │   Confirmed Fact    │
     └──────────┬──────────┘
                │
                ▼
     ┌─────────────────────┐
     │  Audit Management   │
     └──────────┬──────────┘
                │
                ▼
          ┌──────────┐
          │ No Audit │
          └─────┬────┘
                │
                ▼
          ┌──────────┐
          │ Recorded │
          └──────────┘

          Terminal v1.0
```

---

# Definición de Éxito

El Lifecycle del Aggregate **Audit** representa de manera explícita
y mínima la existencia de una unidad histórica de trazabilidad.

La versión 1.0 define:

```text
No Audit → Recorded
```

donde:

- No Audit representa inexistencia del Aggregate;
- Recorded representa una unidad Audit confirmada;
- Recorded constituye el único estado oficial;
- Recorded es terminal;
- Audit no posee una etapa Draft;
- Audit no representa procesamiento técnico;
- Audit no hereda estados del Aggregate originador;
- el hecho de origen debe estar confirmado antes de Audit;
- AuditId permanece inmutable;
- la información histórica mantiene su significado;
- un nuevo hecho originador no reescribe un Audit anterior;
- diferentes hechos pueden generar unidades Audit independientes;
- el Aggregate originador mantiene Lifecycle y Version propios;
- SourceAggregateVersion permanece separado de Audit.Version;
- los fallos de procesamiento no constituyen estados del dominio;
- las políticas de retención, archivo y eliminación no se infieren;
- Read Models permanecen fuera de la autoridad de escritura;
- Integration Events no modifican el Lifecycle;
- CQRS permanece compatible;
- Event Sourcing permanece compatible sin quedar impuesto.

De esta forma, `DOMAIN-012A-Lifecycle.md` establece el Lifecycle
oficial y mínimo del Aggregate **Audit** conforme al patrón
consolidado de AURA Core.