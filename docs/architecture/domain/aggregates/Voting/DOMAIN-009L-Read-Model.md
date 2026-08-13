# DOMAIN-009L — Voting Read Model

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Voting Management

Aggregate:
Voting

Autor:
ARADA

Documentos Relacionados:

- DOMAIN-009-Aggregate.md
- DOMAIN-009D-Domain-Events.md
- DOMAIN-009F-Permissions.md
- DOMAIN-009G-Repository-Contract.md
- DOMAIN-009I-Versioning.md
- DOMAIN-009J-Consistency-Boundary.md
- DOMAIN-009K-Integration-Events.md
- DOMAIN-009M-Test-Scenarios.md
- DOMAIN-009N-Performance-Rules.md
- DOMAIN-009O-Security-Model.md
- CORE-008-Aggregate-Design-Rules.md
- CORE-011-Repository-Contracts.md

---

# Objetivo

Definir los **Read Models** oficiales asociados al Aggregate
**Voting**.

Los Read Models representan información derivada y optimizada para
consulta.

Permiten consultar Voting sin utilizar la Aggregate Root como modelo
de lectura ni ampliar innecesariamente su Consistency Boundary.

Los Read Models:

- representan información derivada;
- no son Aggregates;
- no son Aggregate Roots;
- no constituyen fuente de verdad;
- no protegen las Invariants de escritura;
- no ejecutan Commands;
- no modifican Voting;
- no modifican VotingStatus;
- no incrementan Version;
- pueden reconstruirse;
- pueden actualizarse a partir de hechos confirmados del dominio.

Debe mantenerse:

```text
Write Model

≠

Read Model
```

y:

```text
Voting Aggregate

≠

Voting Projection
```

---

# Principios

Los Read Models de Voting cumplen los siguientes principios:

- están orientados a consulta;
- derivan de información autorizada del dominio;
- no sustituyen al Aggregate;
- no modifican el Write Model;
- pueden presentar subconjuntos diferentes de información;
- pueden representar información histórica;
- pueden reconstruirse desde fuentes autorizadas;
- respetan el orden lógico de AggregateVersion cuando corresponda;
- respetan las reglas de acceso a la información;
- no incorporan autoridad sobre otros Aggregates;
- no convierten referencias externas en ownership;
- permanecen separados del Repository Contract del Aggregate;
- pueden evolucionar sin alterar las Invariants de Voting.

---

# Arquitectura

Conceptualmente:

```text
Command
    │
    ▼
Voting Aggregate
    │
    ▼
Domain Event
    │
    ▼
Projection
    │
    ▼
Read Model
```

El Write Model mantiene:

```text
Identity

Lifecycle

State Machine

Invariants

Consistency Boundary

Version
```

El Read Model mantiene:

```text
Derived Query Representation
```

La separación debe conservarse permanentemente.

---

# Fuente de Verdad

La fuente de verdad de Voting permanece en:

```text
Voting Aggregate
```

y en los hechos de dominio autorizados que representan su evolución
cuando corresponda.

Los Read Models no constituyen la fuente de verdad.

Debe mantenerse:

```text
Voting Aggregate

=

Write Authority
```

y:

```text
Voting Read Model

=

Derived Representation
```

Una diferencia temporal entre una proyección y el estado confirmado
de Voting no otorga autoridad de escritura al Read Model.

---

# Proyecciones Oficiales

La versión 1.0 define las siguientes proyecciones conceptuales de
Voting:

```text
VotingSummary

VotingDetailView

VotingHistoryView

VotingResultView
```

Cada proyección responde a una necesidad de consulta diferente sin
modificar el modelo de escritura.

No constituyen nuevos Aggregates.

No poseen Lifecycle independiente.

No poseen State Machine independiente.

No poseen Version de dominio independiente de Voting.

---

# VotingSummary

## Objetivo

Representar una vista resumida de Voting adecuada para consultas
donde no sea necesario reconstruir el Aggregate completo.

---

## Información Conceptual

Puede representar información derivada equivalente a:

```text
VotingId

OrganizationId

AssemblyId

ProposalId

VotingType

Title

VotingStatus

AggregateVersion
```

cuando dichos elementos correspondan al Voting consultado.

La proyección puede omitir información que no sea necesaria para su
propósito.

---

## Regla

VotingSummary no debe interpretarse como una instancia parcial del
Aggregate capaz de recibir Commands.

Debe mantenerse:

```text
VotingSummary

↓

Query
```

No:

```text
VotingSummary

↓

Domain Mutation
```

---

# VotingDetailView

## Objetivo

Representar una vista detallada del estado observable de un Voting.

---

## Información Conceptual

Puede representar información derivada equivalente a:

```text
VotingId

OrganizationId

AssemblyId

ProposalId

VotingType

Title

Description

VotingStatus

Rules

Options

Result

CreatedAt

OpenedAt

ClosedAt

CancelledAt

ArchivedAt

AggregateVersion
```

cuando estos elementos correspondan al estado y contexto del
Voting.

---

## Regla

VotingDetailView puede presentar información detallada sin adquirir
autoridad sobre el Aggregate.

Debe mantenerse:

```text
Detailed Read Representation

≠

Aggregate Root
```

La existencia de una propiedad en la proyección no autoriza su
modificación directa.

---

# VotingHistoryView

## Objetivo

Representar la evolución histórica observable de Voting.

Permite consultar hechos relevantes ocurridos durante la vida del
Aggregate sin convertir la proyección en fuente transaccional de
verdad.

---

## Información Conceptual

Puede representar una secuencia derivada de hechos como:

```text
VotingCreated

VotingOpened

VotingClosed

VotingCancelled

VotingArchived

VotingTypeChanged

VotingTitleChanged

VotingDescriptionChanged

VotingRulesChanged

VotingOptionAdded

VotingOptionRemoved
```

según los hechos realmente ocurridos para el Voting consultado.

---

## Orden

La evolución histórica debe respetar:

```text
AggregateVersion
```

cuando se utilice para establecer el orden lógico de modificaciones
del mismo Voting.

Conceptualmente:

```text
AggregateVersion = 1

↓

AggregateVersion = 2

↓

AggregateVersion = 3
```

La representación histórica no debe reescribir hechos anteriores
para reflejar únicamente el estado actual.

---

## Regla

VotingHistoryView representa historia derivada.

No puede:

- ejecutar Commands;
- cambiar eventos históricos;
- modificar Voting;
- alterar AggregateVersion;
- crear hechos inexistentes.

---

# VotingResultView

## Objetivo

Representar información de consulta relacionada con el resultado de
Voting cuando dicho Result exista conforme al modelo del Aggregate.

---

## Información Conceptual

Puede representar:

```text
VotingId

OrganizationId

VotingStatus

Result

ClosedAt

AggregateVersion
```

cuando estos elementos formen parte del estado confirmado del
Voting.

Puede mantener referencias contextuales ya pertenecientes al
Voting cuando sean necesarias para interpretar la consulta.

---

## Regla

VotingResultView no calcula ni establece por sí misma el Result del
Aggregate.

Debe mantenerse:

```text
Voting Result

↓

Confirmed Domain State

↓

VotingResultView
```

No:

```text
VotingResultView

↓

Set Voting Result
```

---

## Result y Estado

Debe mantenerse:

```text
Result

≠

VotingStatus
```

VotingResultView no introduce estados adicionales de Lifecycle.

Los estados oficiales continúan siendo:

```text
Draft

Open

Closed

Cancelled

Archived
```

---

# Actualización

Los Read Models pueden actualizarse a partir de hechos confirmados
de Voting.

Conceptualmente:

```text
Voting

↓

Domain Event

↓

Projection Update
```

Ejemplo:

```text
VotingOpened

↓

Update VotingSummary

Update VotingDetailView

Update VotingHistoryView
```

según las proyecciones afectadas por el hecho.

La actualización de una proyección no constituye una modificación
del Aggregate.

---

# Actualización desde VotingCreated

Cuando ocurre:

```text
VotingCreated
```

las proyecciones correspondientes pueden representar la existencia
inicial del Voting.

Conceptualmente:

```text
VotingCreated

↓

VotingStatus = Draft

AggregateVersion = 1
```

Las vistas aplicables pueden reflejar dicho estado confirmado.

---

# Actualización desde VotingOpened

Cuando ocurre:

```text
VotingOpened
```

las proyecciones correspondientes pueden reflejar:

```text
VotingStatus = Open

OpenedAt

AggregateVersion
```

La proyección no ejecuta:

```text
OpenVoting
```

El hecho ya ocurrió dentro del Aggregate.

---

# Actualización desde VotingClosed

Cuando ocurre:

```text
VotingClosed
```

las proyecciones aplicables pueden reflejar:

```text
VotingStatus = Closed

ClosedAt

Result when applicable

AggregateVersion
```

VotingResultView puede reflejar Result únicamente cuando dicho
resultado forma parte del estado confirmado de Voting.

---

# Actualización desde VotingCancelled

Cuando ocurre:

```text
VotingCancelled
```

las proyecciones correspondientes pueden reflejar:

```text
VotingStatus = Cancelled

CancelledAt

AggregateVersion
```

No debe inferirse:

```text
VotingStatus = Archived
```

hasta que ocurra el hecho correspondiente.

---

# Actualización desde VotingArchived

Cuando ocurre:

```text
VotingArchived
```

las proyecciones pueden reflejar:

```text
VotingStatus = Archived

ArchivedAt

AggregateVersion
```

Archived continúa representando preservación histórica.

No equivale a eliminación de los Read Models cuando las consultas
históricas deban conservarse.

---

# Actualización desde Eventos de Configuración

Los hechos:

```text
VotingTypeChanged

VotingTitleChanged

VotingDescriptionChanged

VotingRulesChanged

VotingOptionAdded

VotingOptionRemoved
```

pueden actualizar las proyecciones que representen la información
afectada.

Debe respetarse siempre:

```text
Domain Event

↓

Projection Update
```

No:

```text
Projection Change

↓

Voting Domain Event
```

---

# AggregateVersion

Cuando una proyección preserve:

```text
AggregateVersion
```

esta debe corresponder a la Version del hecho confirmado que produjo
la representación observada.

Conceptualmente:

```text
Domain Event

AggregateVersion = N

↓

Projection

AggregateVersion = N
```

La actualización de la proyección no incrementa:

```text
Voting.Version
```

---

# Eventos Fuera de Orden

Cuando una secuencia de hechos del mismo Voting sea observada fuera
de orden, AggregateVersion permite determinar el orden lógico
correspondiente.

Ejemplo:

```text
VotingClosed
AggregateVersion = 7
```

no debe proyectarse conceptualmente como anterior a:

```text
VotingOpened
AggregateVersion = 5
```

para el mismo Voting.

Debe mantenerse la evolución real del Aggregate.

---

# Eventos Duplicados

El reprocesamiento del mismo hecho no debe producir una
representación semánticamente duplicada o contradictoria.

Debe distinguirse:

```text
Same Event
```

de:

```text
Different Domain Event of Same Type
```

Dos eventos diferentes pueden compartir EventType y representar
modificaciones reales distintas.

La identidad del hecho y AggregateVersion permiten mantener dicha
distinción.

---

# Reconstrucción

Los Read Models deben poder reconstruirse a partir de las fuentes
autorizadas correspondientes.

Conceptualmente:

```text
Confirmed Domain History

↓

Replay for Projection

↓

Rebuilt Read Model
```

La reconstrucción:

- no modifica Voting;
- no ejecuta Commands;
- no incrementa Voting.Version;
- no produce nuevos hechos de dominio;
- no altera el historial original.

---

# Reconstrucción de VotingSummary

VotingSummary puede reconstruirse aplicando los hechos relevantes
hasta alcanzar la representación resumida correspondiente al estado
actual conocido.

Conceptualmente:

```text
VotingCreated

↓

VotingTitleChanged

↓

VotingOpened

↓

VotingSummary
```

La proyección resultante representa el estado derivado.

No reemplaza al Aggregate.

---

# Reconstrucción de VotingDetailView

VotingDetailView puede reconstruirse a partir de los hechos y datos
autorizados necesarios para representar detalladamente el estado
observable.

Debe preservar la semántica final resultante de la evolución
confirmada de Voting.

---

# Reconstrucción de VotingHistoryView

VotingHistoryView conserva la secuencia histórica correspondiente.

La reconstrucción no debe colapsar:

```text
Event A

Event B

Event C
```

en un único hecho ficticio.

Cada hecho mantiene su identidad y significado.

---

# Reconstrucción de VotingResultView

VotingResultView puede reconstruirse cuando el historial confirmado
permita representar el Result existente.

No puede crear Result cuando el dominio no lo haya establecido.

Debe mantenerse:

```text
No Confirmed Result

↓

No Invented Result
```

---

# Consistencia

Los Read Models representan información derivada y pueden existir
fuera del Consistency Boundary del Aggregate.

Debe mantenerse:

```text
Voting Internal Consistency

=

Protected by Voting
```

mientras:

```text
Read Model Consistency

=

Derived from Confirmed Facts
```

La consistencia interna del Aggregate no depende de que una
proyección se encuentre actualizada.

---

# Consistencia Eventual

Puede existir una diferencia temporal entre:

```text
Current Voting State
```

y:

```text
Current Read Model State
```

mientras la proyección correspondiente aún no haya incorporado el
hecho confirmado más reciente.

Esta diferencia no modifica la validez del Aggregate.

Debe mantenerse:

```text
Projection Delay

≠

Voting State Rollback
```

---

# Read Model y Consistency Boundary

Los Read Models permanecen fuera de:

```text
DOMAIN-009J-Consistency-Boundary.md
```

No participan en la modificación interna atómica de Voting.

Debe mantenerse:

```text
Voting Command

↓

Voting Consistency Boundary

↓

Domain Event
```

y posteriormente:

```text
Domain Event

↓

Read Model
```

---

# Consultas

Las consultas sobre Voting deben ser operaciones de lectura.

Conceptualmente pueden responder necesidades como:

```text
obtener resumen de Voting

obtener detalle de Voting

consultar historia de Voting

consultar resultado de Voting cuando exista
```

Las consultas no deben modificar:

```text
VotingStatus

VotingType

Rules

Options

Result

Version

Lifecycle Timestamps
```

---

# Consultas por Identidad

Las proyecciones pueden permitir localizar información mediante:

```text
VotingId
```

VotingId continúa identificando el mismo Aggregate conceptual.

La consulta no modifica su identidad.

---

# Consultas por Contexto Organizacional

Las proyecciones pueden representar:

```text
OrganizationId
```

para consultar Voting dentro de su contexto organizacional.

OrganizationId continúa siendo una referencia.

El Read Model no contiene por ello el Aggregate Organization como
parte de Voting.

---

# Consultas por Contexto

Cuando Voting mantenga:

```text
AssemblyId
```

o:

```text
ProposalId
```

las proyecciones pueden utilizar dichas referencias para representar
el contexto correspondiente.

Esto no modifica la separación entre Aggregates.

Debe mantenerse:

```text
Reference

≠

Ownership
```

---

# Consultas por Estado

Los Read Models pueden representar:

```text
VotingStatus
```

para responder consultas relacionadas con el Lifecycle.

Los estados permanecen:

```text
Draft

Open

Closed

Cancelled

Archived
```

La consulta por estado no modifica la State Machine.

---

# Repository y Read Model

El contrato:

```text
VotingRepository
```

pertenece al Write Model y se define en:

```text
DOMAIN-009G-Repository-Contract.md
```

Los Read Models no deben convertir el Repository del Aggregate en
un mecanismo general de consulta especializada.

Debe mantenerse:

```text
VotingRepository

=

Aggregate Persistence Contract
```

y:

```text
Voting Read Model

=

Query Representation
```

---

# Persistencia

Los Read Models pueden poseer una representación persistida para
atender consultas.

Dicha persistencia:

- pertenece al modelo de lectura;
- no sustituye la persistencia del Aggregate;
- no constituye fuente de verdad;
- puede reconstruirse;
- no modifica Voting;
- no incrementa Voting.Version.

Debe mantenerse:

```text
Read Model Persistence

≠

Aggregate Persistence
```

---

# Independencia de Persistencia

La definición conceptual del Read Model no requiere una tecnología
concreta de almacenamiento.

Debe mantenerse:

```text
Read Model Semantics

≠

Persistence Technology
```

La elección del mecanismo concreto no altera el dominio Voting.

---

# Rendimiento

Los Read Models permiten resolver necesidades de consulta sin
expandir innecesariamente el Aggregate.

Debe mantenerse:

```text
Complex Query

↓

Read Model
```

en lugar de utilizar:

```text
Complex Query

↓

Expand Voting Consistency Boundary
```

Voting debe mantenerse orientado a proteger consistencia y
comportamiento.

Los Read Models pueden orientarse específicamente a las necesidades
de lectura definidas por cada proyección.

Las reglas específicas se desarrollan en:

```text
DOMAIN-009N-Performance-Rules.md
```

---

# Seguridad

La existencia de un Read Model no significa que toda su información
sea accesible para cualquier actor.

Las consultas deben respetar las reglas definidas para el acceso a
Voting.

Cuando corresponda:

```text
Voting.Read
```

determina la capacidad de solicitar acceso a información de Voting.

La Permission no implica acceso automático a toda representación ni
a toda información derivada.

Las reglas específicas se desarrollan en:

```text
DOMAIN-009O-Security-Model.md
```

---

# Minimización

Cada proyección debe contener únicamente la información necesaria
para su propósito de consulta.

Debe evitarse:

```text
One Read Model Contains Everything
```

cuando una vista más limitada sea suficiente.

La minimización preserva:

- encapsulamiento;
- claridad semántica;
- separación de responsabilidades;
- control de acceso;
- evolución independiente de consultas.

---

# Información de Otros Aggregates

Los Read Models de Voting pueden representar identificadores
externos necesarios para contextualizar la consulta.

No deben utilizarse para convertir en estado interno de Voting:

```text
Organization

Citizen

Membership

Role

Territory

Assembly

Proposal

Participation

Document

Notification

Audit

Integration
```

La composición de información proveniente de distintos contextos no
modifica los respectivos Consistency Boundaries.

---

# Read Model y Domain Events

Los Domain Events definidos en:

```text
DOMAIN-009D-Domain-Events.md
```

pueden alimentar las proyecciones correspondientes.

Debe mantenerse:

```text
Domain Event

↓

Projection
```

Los Read Models no producen retroactivamente el hecho que consumen.

---

# Read Model e Integration Events

Los Integration Events definidos en:

```text
DOMAIN-009K-Integration-Events.md
```

representan contratos de comunicación entre contextos.

No reemplazan necesariamente los Domain Events utilizados por las
proyecciones internas.

Debe mantenerse:

```text
Internal Projection Contract

≠

External Integration Contract
```

---

# Compatibilidad con CQRS

Voting es compatible con separación entre escritura y lectura.

Write Side:

```text
Command
    │
    ▼
Voting Aggregate
    │
    ├── Invariants
    ├── State Machine
    ├── Version
    └── Domain Events
```

Read Side:

```text
Domain Events
      │
      ▼
Projection
      │
      ▼
Read Model
```

Debe mantenerse:

```text
Write Side Authority

≠

Read Side Representation
```

El Read Side no ejecuta Commands sobre sí mismo para modificar
Voting.

---

# Compatibilidad con Event Sourcing

Los Read Models pueden reconstruirse mediante Replay de hechos
históricos cuando estos se encuentren disponibles como fuente
autorizada.

Conceptualmente:

```text
Domain Event History

↓

Replay

↓

Read Model
```

Replay para proyecciones:

- no modifica Voting;
- no crea nuevas Version del Aggregate;
- no produce nuevos Domain Events;
- no reescribe hechos históricos.

La compatibilidad no convierte al Read Model en un Event Store.

---

# Evolución

Los Read Models pueden evolucionar conforme aparezcan nuevas
necesidades de consulta.

Una nueva proyección no modifica automáticamente:

```text
Voting Aggregate

Lifecycle

State Machine

Commands

Invariants

Consistency Boundary
```

Debe mantenerse:

```text
New Query Requirement

↓

Read Model Evolution
```

sin convertir una necesidad de lectura en una nueva responsabilidad
del Aggregate.

---

# Evolución de Proyecciones

Una proyección puede evolucionar cuando cambie la información
necesaria para su propósito.

La evolución debe preservar:

- semántica del dominio;
- identidad de Voting;
- significado de los hechos;
- separación entre lectura y escritura;
- reglas de seguridad;
- reconstruibilidad cuando corresponda.

Una modificación del Read Model no autoriza alterar retrospectivamente
los Domain Events históricos.

---

# Nuevas Proyecciones

Una nueva proyección solo debe incorporarse cuando exista una
necesidad explícita de consulta que no requiera modificar las reglas
internas de Voting.

Debe mantenerse:

```text
New Read Model

≠

New Aggregate Behavior
```

Si la necesidad implica una nueva regla de dominio, debe evaluarse
en el artefacto normativo correspondiente y no introducirse
indirectamente mediante un Read Model.

---

# Principios Arquitectónicos

Los Read Models de Voting deben mantener:

```text
Read Model != Aggregate

Projection != Source of Truth

Query != Command

Read != Write

Reference != Ownership
```

Además:

- Voting conserva autoridad de escritura;
- el Read Model permanece derivado;
- la consulta no modifica Version;
- la proyección no modifica Lifecycle;
- la proyección no modifica State Machine;
- la proyección no evita Invariants;
- la proyección no amplía el Consistency Boundary;
- los Read Models pueden reconstruirse;
- las necesidades de lectura no deben inflar el Aggregate;
- las proyecciones deben respetar seguridad y minimización;
- la persistencia concreta permanece fuera de la semántica del
  dominio.

---

# Definición de Éxito

El Read Model de **Voting** proporciona representaciones derivadas
para consulta manteniendo completamente separadas las
responsabilidades de lectura y escritura.

La versión 1.0 define:

```text
VotingSummary

VotingDetailView

VotingHistoryView

VotingResultView
```

Estas proyecciones permiten representar respectivamente:

- información resumida de Voting;
- información detallada del estado observable;
- evolución histórica;
- Result cuando exista conforme al dominio.

Los Read Models:

- no son Aggregates;
- no son Aggregate Roots;
- no constituyen fuente de verdad;
- no ejecutan Commands;
- no modifican Voting;
- no modifican Version;
- no modifican Lifecycle;
- no modifican State Machine;
- no evitan Invariants;
- permanecen fuera del Consistency Boundary;
- pueden actualizarse desde hechos confirmados;
- pueden reconstruirse;
- respetan AggregateVersion cuando corresponde;
- mantienen referencias externas como identificadores;
- permanecen separados del Repository Contract;
- permiten optimizar consultas sin expandir Voting;
- respetan las reglas de seguridad y acceso;
- pueden evolucionar independientemente del Write Model cuando no
  cambie la semántica del dominio.

De esta forma, `DOMAIN-009L-Read-Model.md` establece el modelo
conceptual oficial de lectura para **Voting**, manteniendo la
separación CQRS, la reconstruibilidad, la independencia tecnológica
y el patrón consolidado de AURA Core.