# TA-002 — ProposalUpdatedForIntegration Origin

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
Proposal

Bounded Context:
Proposal Management

---

# Objetivo

Resolver de forma normativa el conjunto de Domain Events que pueden
constituir origen semántico del Integration Event:

```text
ProposalUpdatedForIntegration
```

preservando el modelo de dominio existente de Proposal y sin
introducir nuevos:

* estados;
* Commands;
* Domain Events;
* Integration Events;
* Aggregates;
* Consistency Boundaries.

---

# Hallazgo

La documentación transversal mantenía una definición abierta para
el origen de:

```text
ProposalUpdatedForIntegration
```

mediante expresiones genéricas como:

```text
cambios relevantes de Proposal
```

o:

```text
cambios permitidos sobre información propia de Proposal
```

Esta formulación no establecía un conjunto cerrado y verificable de
Domain Events origen.

---

# Decisión

El conjunto normativo y cerrado de Domain Events que pueden
constituir origen semántico de:

```text
ProposalUpdatedForIntegration
```

es:

```text
ProposalRenamed

ProposalPurposeChanged

ProposalDescriptionChanged

ProposalTypeChanged

ProposalContentUpdated

ProposalTerritoryChanged

ProposalAssemblyAssociated
```

Ningún otro Domain Event de Proposal queda incluido implícitamente
en este conjunto.

---

# Conjunto Cerrado

Debe mantenerse:

```text
ProposalUpdatedForIntegration
    ←
ProposalRenamed

ProposalUpdatedForIntegration
    ←
ProposalPurposeChanged

ProposalUpdatedForIntegration
    ←
ProposalDescriptionChanged

ProposalUpdatedForIntegration
    ←
ProposalTypeChanged

ProposalUpdatedForIntegration
    ←
ProposalContentUpdated

ProposalUpdatedForIntegration
    ←
ProposalTerritoryChanged

ProposalUpdatedForIntegration
    ←
ProposalAssemblyAssociated
```

Este conjunto es exhaustivo para la resolución TA-002.

---

# Naturaleza de los Hechos Origen

Los siete Domain Events seleccionados representan modificaciones
editoriales o de información propia de Proposal que no corresponden
a una transición específica de Lifecycle con un contrato de
integración dedicado.

Debe mantenerse:

```text
confirmed Proposal change
        │
        ▼
approved editorial Domain Event
        │
        ▼
ProposalUpdatedForIntegration
```

cuando exista un contrato explícito de interoperabilidad que
requiera comunicar externamente ese hecho.

---

# ProposalRenamed

`ProposalRenamed` puede constituir origen de:

```text
ProposalUpdatedForIntegration
```

cuando el cambio de nombre confirmado posea relevancia externa y el
contrato de integración correspondiente requiera comunicarlo.

---

# ProposalPurposeChanged

`ProposalPurposeChanged` puede constituir origen de:

```text
ProposalUpdatedForIntegration
```

cuando el cambio de propósito confirmado posea relevancia externa y
el contrato de integración correspondiente requiera comunicarlo.

---

# ProposalDescriptionChanged

`ProposalDescriptionChanged` puede constituir origen de:

```text
ProposalUpdatedForIntegration
```

cuando el cambio de descripción confirmado posea relevancia externa
y el contrato de integración correspondiente requiera comunicarlo.

---

# ProposalTypeChanged

`ProposalTypeChanged` puede constituir origen de:

```text
ProposalUpdatedForIntegration
```

cuando el cambio de tipo confirmado posea relevancia externa y el
contrato de integración correspondiente requiera comunicarlo.

---

# ProposalContentUpdated

`ProposalContentUpdated` puede constituir origen de:

```text
ProposalUpdatedForIntegration
```

cuando la actualización de contenido confirmada posea relevancia
externa y el contrato de integración correspondiente requiera
comunicarla.

---

# ProposalTerritoryChanged

`ProposalTerritoryChanged` puede constituir origen de:

```text
ProposalUpdatedForIntegration
```

cuando el cambio territorial confirmado posea relevancia externa y
el contrato de integración correspondiente requiera comunicarlo.

---

# ProposalAssemblyAssociated

`ProposalAssemblyAssociated` puede constituir origen de:

```text
ProposalUpdatedForIntegration
```

cuando la asociación confirmada con una Assembly posea relevancia
externa y el contrato de integración correspondiente requiera
comunicarla.

---

# Eventos de Lifecycle Excluidos

Los siguientes Domain Events no forman parte del conjunto origen de:

```text
ProposalUpdatedForIntegration
```

```text
ProposalCreated

ProposalSubmitted

ProposalReviewStarted

ProposalAccepted

ProposalRejected

ProposalWithdrawn

ProposalArchived
```

Estos hechos poseen semántica propia de Lifecycle y contratos de
integración específicos.

---

# ProposalCreated

Debe mantenerse:

```text
ProposalCreated
    ≠
ProposalUpdatedForIntegration
```

El hecho de creación posee su propio contrato de integración.

---

# ProposalSubmitted

Debe mantenerse:

```text
ProposalSubmitted
    ≠
ProposalUpdatedForIntegration
```

La presentación formal de una Proposal no debe degradarse a un
evento genérico de actualización.

---

# ProposalReviewStarted

Debe mantenerse:

```text
ProposalReviewStarted
    ≠
ProposalUpdatedForIntegration
```

El inicio de revisión conserva su propia semántica.

---

# ProposalAccepted

Debe mantenerse:

```text
ProposalAccepted
    ≠
ProposalUpdatedForIntegration
```

La aceptación de una Proposal constituye un hecho específico de
Lifecycle.

---

# ProposalRejected

Debe mantenerse:

```text
ProposalRejected
    ≠
ProposalUpdatedForIntegration
```

El rechazo de una Proposal conserva su propia semántica.

---

# ProposalWithdrawn

Debe mantenerse:

```text
ProposalWithdrawn
    ≠
ProposalUpdatedForIntegration
```

El retiro de una Proposal no debe representarse como modificación
editorial genérica.

---

# ProposalArchived

Debe mantenerse:

```text
ProposalArchived
    ≠
ProposalUpdatedForIntegration
```

El archivado posee semántica propia y contrato específico.

---

# Publicación Condicional

La existencia de cualquiera de los siete Domain Events aprobados no
obliga automáticamente a producir:

```text
ProposalUpdatedForIntegration
```

Debe mantenerse:

```text
approved source Domain Event
    ≠
Mandatory ProposalUpdatedForIntegration
```

La publicación externa continúa siendo condicional.

---

# Condiciones Semánticas

Para que uno de los siete Domain Events aprobados pueda originar:

```text
ProposalUpdatedForIntegration
```

debe existir:

```text
confirmed domain fact
        │
        ▼
external relevance
        │
        ▼
explicit integration contract
```

La pertenencia al conjunto cerrado de orígenes no sustituye estas
condiciones.

---

# No Publicación Automática

Esta decisión no establece:

```text
every ProposalRenamed
        │
        ▼
ProposalUpdatedForIntegration
```

ni equivalente para los demás Domain Events aprobados.

La relación normativa establece únicamente los posibles orígenes
semánticos permitidos.

---

# Naturaleza de ProposalUpdatedForIntegration

`ProposalUpdatedForIntegration` permanece definido como:

```text
Integration Event
```

No se convierte en:

```text
Domain Event
```

No constituye:

```text
ProposalStatus
```

No introduce un nuevo estado en el Lifecycle de Proposal.

---

# Commands

Esta decisión no introduce nuevos Commands.

Los Commands que originan los Domain Events aprobados permanecen
definidos por el modelo oficial de Proposal.

TA-002 no redefine su identidad ni su comportamiento.

---

# Domain Events

Esta decisión no introduce nuevos Domain Events.

El conjunto:

```text
ProposalRenamed

ProposalPurposeChanged

ProposalDescriptionChanged

ProposalTypeChanged

ProposalContentUpdated

ProposalTerritoryChanged

ProposalAssemblyAssociated
```

corresponde exclusivamente a Domain Events ya existentes del
Aggregate Proposal.

---

# Integration Events

Esta resolución únicamente determina el conjunto de posibles
orígenes semánticos del contrato existente:

```text
ProposalUpdatedForIntegration
```

No crea un nuevo Integration Event.

No modifica los Integration Events específicos asociados al
Lifecycle de Proposal.

---

# Lifecycle

Esta decisión no modifica el Lifecycle de Proposal.

Los Domain Events de Lifecycle excluidos mantienen sus propias
transiciones y contratos.

Ningún estado nuevo es introducido por TA-002.

---

# Consistency Boundary

Esta decisión no modifica el Consistency Boundary de Proposal.

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

`ProposalUpdatedForIntegration` permanece fuera del estado interno
del Aggregate Proposal.

---

# Regla Normativa

El conjunto oficial queda establecido como:

```text
ProposalRenamed
                \
ProposalPurposeChanged
                  \
ProposalDescriptionChanged
                    \
ProposalTypeChanged
                      \
ProposalContentUpdated
                        ─────► ProposalUpdatedForIntegration
ProposalTerritoryChanged
                      /
ProposalAssemblyAssociated
                    /
```

sujeto en cada caso a:

```text
confirmed fact
+
external relevance
+
explicit integration contract
```

---

# Regla de Exclusión

Debe mantenerse:

```text
ProposalCreated
ProposalSubmitted
ProposalReviewStarted
ProposalAccepted
ProposalRejected
ProposalWithdrawn
ProposalArchived
        │
        ✕
ProposalUpdatedForIntegration
```

Estos eventos conservan sus contratos específicos.

---

# Restricciones

Esta decisión no autoriza:

* ampliar implícitamente el conjunto de Domain Events origen;
* utilizar eventos de Lifecycle como origen de
  ProposalUpdatedForIntegration;
* publicar ProposalUpdatedForIntegration automáticamente ante todo
  cambio editorial;
* crear nuevos estados;
* crear nuevos Commands;
* crear nuevos Domain Events;
* crear nuevos Integration Events;
* modificar el Lifecycle de Proposal;
* modificar el Consistency Boundary;
* introducir nuevos Aggregates;
* reemplazar contratos específicos de Lifecycle por
  ProposalUpdatedForIntegration.

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

Estas decisiones no forman parte de TA-002.

---

# Impacto Documental

La resolución debe mantenerse coherente en:

```text
DOMAIN-007K-Integration-Events.md

CROSS-001-Transversal-Audit.md

CROSS-004-Cross-Domain-Contracts.md

event-catalog.md
```

Ninguno de estos documentos debe volver a presentar como abierto,
genérico o indeterminado el conjunto de Domain Events origen de:

```text
ProposalUpdatedForIntegration
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

TA-002 queda:

```text
Resolved
```

con el siguiente conjunto cerrado de orígenes semánticos:

```text
ProposalRenamed

ProposalPurposeChanged

ProposalDescriptionChanged

ProposalTypeChanged

ProposalContentUpdated

ProposalTerritoryChanged

ProposalAssemblyAssociated
```

Los Domain Events de Lifecycle:

```text
ProposalCreated

ProposalSubmitted

ProposalReviewStarted

ProposalAccepted

ProposalRejected

ProposalWithdrawn

ProposalArchived
```

quedan expresamente excluidos del mapping hacia
`ProposalUpdatedForIntegration`.

La publicación continúa siendo condicional al hecho confirmado, su
relevancia externa y el contrato explícito de interoperabilidad
correspondiente.

No se modifica el Aggregate Proposal, su Lifecycle, sus Commands,
sus Domain Events ni su Consistency Boundary.