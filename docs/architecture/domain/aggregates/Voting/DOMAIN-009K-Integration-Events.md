# DOMAIN-009K — Voting Integration Events

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

Documentos relacionados:

- DOMAIN-009-Aggregate.md
- DOMAIN-009A-Lifecycle.md
- DOMAIN-009B-State-Machine.md
- DOMAIN-009C-Commands.md
- DOMAIN-009D-Domain-Events.md
- DOMAIN-009E-Invariants.md
- DOMAIN-009G-Repository-Contract.md
- DOMAIN-009I-Versioning.md
- DOMAIN-009J-Consistency-Boundary.md
- DOMAIN-009L-Read-Model.md
- CORE-008-Aggregate-Design-Rules.md
- CORE-016-Dependency-Rules.md

---

# Objetivo

Definir formalmente los **Integration Events** asociados al
Aggregate **Voting**.

Los Integration Events representan contratos mediante los cuales
hechos confirmados de Voting pueden comunicarse fuera de su
Bounded Context sin exponer directamente el modelo interno del
Aggregate.

Un Integration Event:

- representa un hecho ya confirmado;
- se origina a partir de un hecho relevante del dominio;
- no constituye un Command;
- no constituye una intención;
- no modifica Voting;
- no pertenece al estado interno del Aggregate;
- no reemplaza al Domain Event;
- no amplía el Consistency Boundary;
- no concede autoridad sobre Voting;
- preserva únicamente la información necesaria para comunicar el
  hecho correspondiente.

Debe mantenerse:

```text
Voting

↓

Domain Event

↓

Integration Event
```

y no:

```text
External Consumer

↓

Integration Event

↓

Direct Voting Mutation
```

---

# Principios

Los Integration Events de Voting deben cumplir los siguientes
principios:

- únicamente representan hechos confirmados;
- se derivan de Domain Events relevantes;
- permanecen separados de los Domain Events internos;
- no modifican el Lifecycle;
- no modifican la State Machine;
- no modifican las Invariants;
- no modifican Version;
- no forman parte del Consistency Boundary;
- utilizan identificadores para representar referencias;
- no transportan Aggregates externos completos;
- no exponen innecesariamente el estado interno de Voting;
- preservan la semántica del hecho que comunican;
- permiten evolución controlada de los contratos;
- permanecen independientes del mecanismo concreto de transporte.

---

# Principio Fundamental

Debe mantenerse:

```text
Domain Event

=

Internal Domain Fact
```

mientras:

```text
Integration Event

=

External Integration Contract
```

Por lo tanto:

```text
VotingOpened
```

y:

```text
VotingOpenedIntegrationEvent
```

se encuentran relacionados, pero no representan el mismo contrato.

El primero pertenece al modelo interno de Voting.

El segundo representa la comunicación del hecho hacia fuera del
Bounded Context cuando dicha comunicación sea necesaria.

---

# Domain Events versus Integration Events

Los Domain Events pertenecen al modelo interno del Aggregate.

Ejemplos:

```text
VotingCreated

VotingOpened

VotingClosed

VotingCancelled

VotingArchived
```

Los Integration Events representan contratos derivados para
comunicación entre contextos.

```text
VotingCreatedIntegrationEvent

VotingOpenedIntegrationEvent

VotingClosedIntegrationEvent

VotingCancelledIntegrationEvent

VotingArchivedIntegrationEvent
```

Debe mantenerse:

```text
Domain Event

≠

Integration Event
```

No todo Domain Event necesita transformarse en Integration Event.

Solo los hechos definidos explícitamente por este contrato se
publican como Integration Events de la versión 1.0.

---

# Alcance

Los Integration Events definidos en este documento corresponden
exclusivamente a hechos de Voting que ya fueron aceptados dentro de
su Consistency Boundary.

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

Document

Notification

Audit

Integration
```

Un Integration Event de Voting puede ser utilizado posteriormente
por otros contextos.

Eso no convierte dichos contextos en parte del Aggregate Voting.

---

# Integration Events Oficiales

La versión 1.0 define los siguientes Integration Events:

```text
VotingCreatedIntegrationEvent

VotingOpenedIntegrationEvent

VotingClosedIntegrationEvent

VotingCancelledIntegrationEvent

VotingArchivedIntegrationEvent
```

No se definen Integration Events adicionales en esta versión.

Los eventos de modificación de configuración permanecen como
Domain Events internos mientras no exista un contrato explícito
que requiera su publicación externa.

---

# Relación Oficial con Domain Events

| Domain Event | Integration Event |
| --- | --- |
| VotingCreated | VotingCreatedIntegrationEvent |
| VotingOpened | VotingOpenedIntegrationEvent |
| VotingClosed | VotingClosedIntegrationEvent |
| VotingCancelled | VotingCancelledIntegrationEvent |
| VotingArchived | VotingArchivedIntegrationEvent |

La existencia del Domain Event es condición previa para producir el
Integration Event correspondiente.

No puede existir:

```text
VotingOpenedIntegrationEvent
```

si previamente no ocurrió válidamente:

```text
VotingOpened
```

---

# Flujo Conceptual

La comunicación sigue conceptualmente:

```text
Command

↓

Voting

↓

Valid Domain Modification

↓

Domain Event

↓

Integration Event
```

Ejemplo:

```text
OpenVoting

↓

Voting

↓

Draft → Open

↓

VotingOpened

↓

VotingOpenedIntegrationEvent
```

El Integration Event aparece después de que el hecho de dominio ha
sido confirmado.

---

# VotingCreatedIntegrationEvent

## Origen

```text
VotingCreated
```

---

## Significado

Representa hacia otros contextos el hecho de que un Voting fue
creado válidamente.

El hecho interno correspondiente establece:

```text
VotingStatus = Draft
```

---

## Información Conceptual

Debe comunicar únicamente la información necesaria para identificar
el hecho y su contexto.

Conceptualmente puede preservar:

```text
VotingId

OrganizationId

VotingType

VotingStatus

AggregateVersion

OccurredAt
```

Cuando formen parte del contexto confirmado de Voting pueden
preservarse las referencias correspondientes:

```text
AssemblyId

ProposalId
```

---

## Restricción

El evento no contiene:

```text
Organization Aggregate

Assembly Aggregate

Proposal Aggregate
```

Tampoco permite modificar directamente ninguno de ellos.

---

# VotingOpenedIntegrationEvent

## Origen

```text
VotingOpened
```

---

## Significado

Representa externamente el hecho confirmado de que Voting alcanzó:

```text
Open
```

desde:

```text
Draft
```

---

## Información Conceptual

Puede preservar:

```text
VotingId

OrganizationId

VotingStatus

OpenedAt

AggregateVersion

OccurredAt
```

y las referencias contextuales ya pertenecientes al hecho cuando
corresponda.

---

## Restricción

El evento no significa:

```text
Assembly InProgress
```

ni:

```text
Proposal State Changed
```

ni:

```text
Participation Activated
```

El evento comunica exclusivamente un hecho de Voting.

---

# VotingClosedIntegrationEvent

## Origen

```text
VotingClosed
```

---

## Significado

Representa externamente que Voting terminó válidamente su flujo
normal y alcanzó:

```text
Closed
```

---

## Información Conceptual

Puede preservar:

```text
VotingId

OrganizationId

VotingStatus

OpenedAt

ClosedAt

AggregateVersion

OccurredAt
```

Cuando Result forme parte necesaria del contrato del hecho
confirmado, debe conservar únicamente la representación requerida
para comunicar dicho resultado sin exponer innecesariamente el
estado interno del Aggregate.

---

## Restricción

Debe mantenerse:

```text
VotingClosedIntegrationEvent

≠

Proposal State Transition
```

y:

```text
VotingClosedIntegrationEvent

≠

Assembly State Transition
```

El consumidor conserva la responsabilidad sobre su propio modelo.

---

# VotingCancelledIntegrationEvent

## Origen

```text
VotingCancelled
```

---

## Significado

Representa externamente que Voting terminó mediante la ruta de
cancelación definida por el Lifecycle versión 1.0.

El estado confirmado es:

```text
Cancelled
```

---

## Información Conceptual

Puede preservar:

```text
VotingId

OrganizationId

VotingStatus

CancelledAt

AggregateVersion

OccurredAt
```

---

## Restricción

El evento no representa:

```text
Physical Deletion
```

Tampoco representa:

```text
VotingArchived
```

Cancelled y Archived continúan siendo hechos diferentes.

---

# VotingArchivedIntegrationEvent

## Origen

```text
VotingArchived
```

---

## Significado

Representa externamente el hecho de que Voting alcanzó su estado
histórico terminal:

```text
Archived
```

---

## Información Conceptual

Puede preservar:

```text
VotingId

OrganizationId

VotingStatus

ArchivedAt

AggregateVersion

OccurredAt
```

---

## Restricción

Debe mantenerse:

```text
Archived

≠

Deleted
```

VotingArchivedIntegrationEvent comunica preservación histórica.

No comunica eliminación física.

---

# Identidad del Aggregate

Todos los Integration Events de Voting deben identificar el
Aggregate mediante:

```text
VotingId
```

VotingId:

- identifica el Voting que originó el hecho;
- permanece inmutable;
- no cambia durante la transformación hacia Integration Event;
- no debe sustituirse por un identificador externo.

Debe mantenerse:

```text
Domain Event VotingId

=

Integration Event VotingId
```

---

# Contexto Organizacional

Los Integration Events deben preservar:

```text
OrganizationId
```

cuando dicho identificador forma parte del contexto del hecho.

OrganizationId continúa representando una referencia.

No incorpora:

```text
Organization Aggregate
```

dentro del contrato.

---

# Referencias Contextuales

Cuando el hecho confirmado se encuentre relacionado con:

```text
AssemblyId
```

o:

```text
ProposalId
```

estas referencias pueden preservarse cuando sean necesarias para
interpretar correctamente el Integration Event.

Debe mantenerse:

```text
Aggregate Identifier

≠

Embedded Aggregate
```

Los Integration Events no transportan otros Aggregates completos.

---

# AggregateVersion

Los Integration Events deben preservar la relación con la Version
de Voting que produjo el hecho.

Conceptualmente:

```text
Voting

Version = N

↓

Domain Event

AggregateVersion = N

↓

Integration Event

AggregateVersion = N
```

El Integration Event no incrementa Version.

Debe mantenerse:

```text
Integration Event Publication

≠

Voting Modification
```

La definición formal de Versioning pertenece a:

```text
DOMAIN-009I-Versioning.md
```

---

# OccurredAt

OccurredAt representa el momento del hecho de dominio que originó
la integración.

Debe preservar la semántica temporal del hecho confirmado.

La creación posterior del contrato de integración no debe
reinterpretar cuándo ocurrió el hecho de Voting.

---

# Correlación y Causalidad

Cuando la información de correlación y causalidad forme parte del
hecho disponible, debe preservarse a través del flujo de
integración.

Conceptualmente:

```text
Command

↓

Domain Event

↓

Integration Event
```

puede mantener:

```text
CorrelationId

CausationId
```

para conservar trazabilidad entre la intención, el hecho interno y
su representación externa.

Estos identificadores no modifican Voting.

---

# Payload

El Payload de un Integration Event debe contener únicamente la
información necesaria para comunicar el hecho.

Debe mantenerse:

```text
Minimum Required Integration Information
```

No debe utilizarse:

```text
Complete Voting Aggregate
```

como Payload por defecto.

La separación protege:

- encapsulamiento;
- autonomía del dominio;
- estabilidad del contrato;
- independencia entre Bounded Contexts.

---

# Inmutabilidad

Un Integration Event representa un hecho confirmado.

Una vez emitido, no debe modificarse para representar un estado
posterior de Voting.

Ejemplo:

```text
VotingOpenedIntegrationEvent
```

continúa representando que Voting fue abierto aunque posteriormente
ocurra:

```text
VotingClosedIntegrationEvent
```

Los hechos posteriores no reescriben contratos históricos
anteriores.

---

# Orden

Dentro de los hechos originados por un mismo Voting:

```text
AggregateVersion
```

permite conservar el orden lógico asociado a la evolución del
Aggregate.

Ejemplo:

```text
VotingCreatedIntegrationEvent
AggregateVersion = 1

VotingOpenedIntegrationEvent
AggregateVersion = 2

VotingClosedIntegrationEvent
AggregateVersion = 3

VotingArchivedIntegrationEvent
AggregateVersion = 4
```

La numeración exacta puede contener otras modificaciones válidas
entre estos eventos.

AggregateVersion debe corresponder siempre a la Version real que
produjo el hecho.

---

# Consistency Boundary

Los Integration Events se encuentran fuera del Consistency Boundary
interno de Voting.

Debe mantenerse:

```text
Voting Consistency Boundary

↓

Confirmed Domain Event

↓

Integration Event
```

La creación o publicación de un Integration Event no amplía el
límite hacia:

```text
Organization

Assembly

Proposal

Participation

Notification

Audit

Integration
```

La definición formal del límite pertenece a:

```text
DOMAIN-009J-Consistency-Boundary.md
```

---

# Consistencia entre Aggregates

Un Integration Event comunica un hecho.

No ejecuta una modificación atómica sobre otro Aggregate.

Debe mantenerse:

```text
VotingClosedIntegrationEvent

↓

External Consumer
```

sin interpretar:

```text
VotingClosedIntegrationEvent

=

Atomic External Aggregate Mutation
```

Cada consumidor conserva:

- su Aggregate Root;
- sus Invariants;
- su Lifecycle;
- su Version;
- su Consistency Boundary.

---

# Integration Event y Commands Externos

Un Integration Event puede informar a otro contexto de que un hecho
ocurrió.

No constituye automáticamente un Command válido sobre ese contexto.

Debe mantenerse:

```text
Integration Event

≠

External Aggregate Command
```

El contexto consumidor decide, conforme a sus propias reglas, si
debe producirse una acción posterior.

---

# Integration Event y Permissions

Los Integration Events no conceden Permissions.

Debe mantenerse:

```text
Integration Event Received

≠

Permission Granted
```

Un consumidor no adquiere capacidad para modificar Voting por haber
recibido uno de sus Integration Events.

---

# Integration Event y Read Model

Los Integration Events pueden comunicar hechos fuera del Bounded
Context.

Los Read Models internos definidos para Voting permanecen
conceptualmente separados.

Debe mantenerse:

```text
Integration Contract

≠

Voting Read Model
```

Ninguno de ambos posee autoridad para modificar directamente el
Aggregate.

---

# Domain Events Internos no Expuestos

La versión 1.0 mantiene como Domain Events internos:

```text
VotingTypeChanged

VotingTitleChanged

VotingDescriptionChanged

VotingRulesChanged

VotingOptionAdded

VotingOptionRemoved
```

Este documento no define Integration Events equivalentes para
ellos.

Por lo tanto, no deben inferirse automáticamente:

```text
VotingTypeChangedIntegrationEvent

VotingTitleChangedIntegrationEvent

VotingDescriptionChangedIntegrationEvent

VotingRulesChangedIntegrationEvent

VotingOptionAddedIntegrationEvent

VotingOptionRemovedIntegrationEvent
```

La incorporación futura de alguno de estos contratos requiere una
evolución explícita del modelo de integración.

---

# Lifecycle

Los Integration Events oficiales reflejan los hechos principales
del Lifecycle que han sido seleccionados para integración.

Conceptualmente:

```text
VotingCreated
↓

VotingCreatedIntegrationEvent
```

```text
VotingOpened
↓

VotingOpenedIntegrationEvent
```

```text
VotingClosed
↓

VotingClosedIntegrationEvent
```

```text
VotingCancelled
↓

VotingCancelledIntegrationEvent
```

```text
VotingArchived
↓

VotingArchivedIntegrationEvent
```

Los Integration Events no crean nuevas transiciones.

---

# State Machine

La existencia de un Integration Event de Lifecycle presupone que la
transición correspondiente ya fue aceptada por:

```text
DOMAIN-009B-State-Machine.md
```

No puede utilizarse un Integration Event para crear una transición
no permitida.

Debe mantenerse:

```text
Valid State Transition

↓

Domain Event

↓

Integration Event
```

---

# Invariants

Un Integration Event solamente puede derivarse de un hecho que ya
respetó:

```text
DOMAIN-009E-Invariants.md
```

Por tanto:

```text
Invariant Violation

↓

Rejected Domain Operation

↓

No Success Domain Event

↓

No Success Integration Event
```

---

# Commands Rechazados

Cuando un Command es rechazado no existe el Domain Event de éxito.

En consecuencia tampoco existe el Integration Event derivado.

Ejemplo:

```text
VotingStatus = Closed

↓

OpenVoting

↓

Rejected
```

No debe producirse:

```text
VotingOpened
```

ni:

```text
VotingOpenedIntegrationEvent
```

---

# Concurrencia

Cuando una modificación es rechazada por conflicto de concurrencia,
no existe un nuevo hecho confirmado.

Debe mantenerse:

```text
ConcurrencyConflict

↓

No Confirmed Domain Modification

↓

No Success Domain Event

↓

No Success Integration Event
```

Un Integration Event nunca debe representar una modificación que no
fue confirmada.

---

# Persistencia

La persistencia de Voting y el hecho que origina un Integration
Event deben mantener coherencia con la Version confirmada del
Aggregate.

Debe mantenerse conceptualmente:

```text
Voting Version N

+

Confirmed Domain Event
AggregateVersion = N

↓

Integration Event
AggregateVersion = N
```

La publicación del Integration Event no crea una nueva modificación
de Voting.

---

# Reconstrucción

Los Integration Events no constituyen la fuente de reconstrucción
interna del Aggregate Voting.

Debe mantenerse:

```text
Integration Event

≠

Voting Aggregate Internal State Authority
```

La recuperación y reconstrucción del Aggregate se rigen por sus
contratos de dominio y persistencia.

---

# CQRS

Los Integration Events permanecen fuera del Write Model interno de
Voting.

Conceptualmente:

```text
Command

↓

Voting Write Model

↓

Domain Event

↓

Integration Event
```

Los Integration Events pueden ser consumidos fuera del Bounded
Context sin obtener autoridad sobre el Write Model.

---

# Event Sourcing

Los Integration Events no reemplazan los Domain Events utilizados
para representar la evolución interna de Voting.

Debe mantenerse:

```text
Domain Event History

≠

Integration Event History
```

La compatibilidad de Voting con Event Sourcing continúa basada en
sus hechos de dominio internos.

---

# Evolución del Contrato

Los Integration Events constituyen contratos de comunicación.

Su evolución debe preservar la semántica de los hechos publicados.

Un cambio futuro no puede transformar retroactivamente:

```text
VotingOpenedIntegrationEvent
```

en un hecho diferente.

La incorporación de nuevos Integration Events debe corresponder a
hechos explícitamente reconocidos por el dominio y a una necesidad
de integración formalmente definida.

No deben agregarse contratos externos únicamente porque exista un
Domain Event interno.

---

# Independencia Tecnológica

Los Integration Events definidos por Voting representan contratos
conceptuales.

Su significado no depende del mecanismo concreto utilizado para
transportarlos.

El dominio debe mantener:

```text
Integration Event Semantics

≠

Transport Technology
```

La selección del mecanismo técnico pertenece fuera del Aggregate y
no modifica el contrato conceptual definido en este documento.

---

# Restricciones

No está permitido:

- utilizar un Integration Event como Command de Voting;
- utilizar un Integration Event para modificar directamente Voting;
- producir un Integration Event sin un hecho de dominio confirmado;
- producir un Integration Event para un Command rechazado;
- producir un Integration Event para una modificación rechazada por
  concurrencia;
- modificar VotingStatus mediante un Integration Event;
- modificar Version mediante un Integration Event;
- modificar VotingId mediante un Integration Event;
- modificar OrganizationId mediante un Integration Event;
- convertir un Integration Event en parte del estado interno de
  Voting;
- utilizar un Integration Event para ampliar el Consistency
  Boundary;
- transportar automáticamente Voting completo como Payload;
- transportar Aggregates externos completos;
- interpretar referencias como ownership;
- asumir que un Integration Event modifica automáticamente
  Assembly;
- asumir que un Integration Event modifica automáticamente
  Proposal;
- asumir que un Integration Event modifica automáticamente
  Participation;
- asumir que recibir un Integration Event concede Permissions;
- reemplazar Domain Events con Integration Events;
- utilizar Integration Events como fuente de autoridad interna para
  reconstruir Voting;
- inferir Integration Events adicionales desde Domain Events no
  expuestos;
- introducir contratos para reapertura, reactivación,
  desarchivado, suspensión o eliminación cuando dichos hechos no
  existen en el modelo actual.

---

# Reglas

## REG-001

Todo Integration Event de Voting representa un hecho previamente
confirmado por el dominio.

---

## REG-002

Un Integration Event no constituye un Command.

---

## REG-003

Un Integration Event no reemplaza al Domain Event que originó el
hecho.

---

## REG-004

Los Integration Events oficiales de la versión 1.0 son:

```text
VotingCreatedIntegrationEvent

VotingOpenedIntegrationEvent

VotingClosedIntegrationEvent

VotingCancelledIntegrationEvent

VotingArchivedIntegrationEvent
```

---

## REG-005

Cada Integration Event debe mantener correspondencia semántica con
su Domain Event de origen.

---

## REG-006

Todo Integration Event debe identificar el Voting mediante
VotingId.

---

## REG-007

OrganizationId debe preservarse como contexto organizacional del
hecho cuando corresponda.

---

## REG-008

AggregateVersion debe corresponder a la Version de Voting que
produjo el hecho.

---

## REG-009

La producción o publicación de un Integration Event no incrementa
Voting.Version.

---

## REG-010

Los Integration Events permanecen fuera del Consistency Boundary
de Voting.

---

## REG-011

Los Integration Events no modifican directamente otros Aggregates.

---

## REG-012

Un Command rechazado no produce el Integration Event de éxito
correspondiente.

---

## REG-013

Un conflicto de concurrencia no produce un Integration Event de
éxito.

---

## REG-014

El Payload debe contener únicamente la información necesaria para
comunicar el hecho.

---

## REG-015

Las referencias externas deben mantenerse mediante identificadores
y no mediante Aggregates completos.

---

## REG-016

Los Domain Events internos sin contrato de integración definido no
deben exponerse automáticamente como Integration Events.

---

## REG-017

Los Integration Events deben preservar su significado histórico.

---

## REG-018

La incorporación de nuevos Integration Events requiere evolución
explícita del contrato y coherencia con el modelo del Aggregate.

---

# Definición de Éxito

Los Integration Events del Aggregate **Voting** permiten comunicar
hechos confirmados fuera del Bounded Context sin exponer ni ampliar
el modelo interno del Aggregate.

La versión 1.0 define exclusivamente:

```text
VotingCreatedIntegrationEvent

VotingOpenedIntegrationEvent

VotingClosedIntegrationEvent

VotingCancelledIntegrationEvent

VotingArchivedIntegrationEvent
```

Cada uno mantiene correspondencia con:

```text
VotingCreated

VotingOpened

VotingClosed

VotingCancelled

VotingArchived
```

respectivamente.

Los Integration Events:

- representan hechos confirmados;
- preservan VotingId;
- preservan OrganizationId cuando corresponde;
- mantienen relación con AggregateVersion;
- preservan la semántica temporal del hecho;
- pueden mantener correlación y causalidad;
- utilizan Payloads mínimos;
- no sustituyen Domain Events;
- no constituyen Commands;
- no modifican Voting;
- no modifican otros Aggregates;
- no incrementan Version;
- permanecen fuera del Consistency Boundary;
- no convierten referencias externas en ownership;
- no exponen automáticamente todos los Domain Events internos;
- permanecen independientes del mecanismo tecnológico de
  transporte.

De esta forma, `DOMAIN-009K-Integration-Events.md` establece el
contrato conceptual oficial para comunicar hechos relevantes del
Aggregate **Voting** hacia otros contextos, preservando su autonomía,
su Versioning, su Consistency Boundary y el patrón consolidado de
AURA Core.