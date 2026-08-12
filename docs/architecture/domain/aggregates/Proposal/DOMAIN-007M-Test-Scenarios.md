# DOMAIN-007M — Proposal Test Scenarios

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Proposal Management

Aggregate:
Proposal

Autor:
ARADA

Documentos relacionados:

- DOMAIN-007-Aggregate.md
- DOMAIN-007A-Lifecycle.md
- DOMAIN-007B-State-Machine.md
- DOMAIN-007C-Commands.md
- DOMAIN-007D-Domain-Events.md
- DOMAIN-007E-Invariants.md
- DOMAIN-007F-Permissions.md
- DOMAIN-007G-Repository-Contract.md
- DOMAIN-007H-Examples.md
- DOMAIN-007I-Versioning.md
- DOMAIN-007J-Consistency-Boundary.md
- DOMAIN-007K-Integration-Events.md
- DOMAIN-007L-Read-Model.md
- CORE-003-Shared-Kernel.md
- CORE-004-Ubiquitous-Language.md
- CORE-005-Domain-Events.md
- CORE-006-Domain-Invariants.md
- CORE-007-Strategic-Design.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Definir los escenarios conceptuales de prueba del Aggregate
**Proposal**.

Los Test Scenarios establecen las condiciones que deben
verificarse para demostrar que Proposal preserva correctamente:

- identidad;
- ciclo de vida;
- State Machine;
- Commands;
- Domain Events;
- invariantes;
- permisos;
- persistencia;
- versionado;
- límite de consistencia;
- Integration Events;
- Read Models;
- relaciones con otros Aggregates.

Estos escenarios constituyen una especificación verificable del
comportamiento esperado del dominio.

No representan una implementación técnica de pruebas.

No dependen de:

- lenguaje de programación;
- framework de testing;
- base de datos;
- ORM;
- API;
- protocolo;
- infraestructura.

---

# Propósito

Los Test Scenarios permiten verificar que una implementación del
Aggregate Proposal respete el modelo conceptual oficial definido
por AURA Core.

Su propósito es detectar implementaciones que:

- permitan transiciones inválidas;
- violen invariantes;
- modifiquen identidad;
- alteren referencias inmutables;
- omitan Domain Events obligatorios;
- incrementen Version incorrectamente;
- permitan modificaciones sobre estados terminales;
- mezclen autorización con reglas del dominio;
- introduzcan otros Aggregates dentro del límite de Proposal;
- permitan persistencia parcial;
- publiquen hechos externos inexistentes;
- conviertan Read Models en fuentes de verdad;
- introduzcan dependencias tecnológicas dentro del dominio.

Los escenarios de prueba deben validar comportamiento observable
del dominio y no detalles accidentales de implementación.

---

# Principios

Los Test Scenarios siguen los siguientes principios:

- verifican comportamiento de dominio;
- utilizan lenguaje ubicuo;
- prueban reglas conceptuales;
- prueban invariantes;
- prueban transiciones válidas;
- prueban transiciones inválidas;
- prueban Commands aceptados;
- prueban Commands rechazados;
- prueban Domain Events;
- prueban Version;
- prueban límites de consistencia;
- prueban referencias entre Aggregates;
- son independientes de Infrastructure;
- son deterministas cuando las entradas conceptuales son las
  mismas;
- permiten verificar casos positivos y negativos;
- no modifican las reglas del Aggregate;
- no introducen nuevas decisiones arquitectónicas.

---

# Alcance

Los escenarios definidos en este documento cubren:

```text
Creation

Draft Management

Submission

Review

Acceptance

Rejection

Withdrawal

Archival

Identity

Organization Ownership

External References

Invariants

Permissions

Domain Events

Versioning

Repository Behavior

Consistency Boundary

Integration Events

Read Models

Concurrency

Invalid Operations
```

Los escenarios verifican el modelo ya establecido para Proposal.

No amplían el Aggregate.

---

# Estructura Conceptual de un Test Scenario

Cada escenario puede expresarse mediante:

```text
ScenarioId

Objective

Given

When

Then
```

Donde:

```text
Given
```

representa el estado inicial y las precondiciones.

```text
When
```

representa la intención u operación ejecutada.

```text
Then
```

representa el comportamiento observable esperado.

Cuando corresponda, también puede verificarse:

```text
Expected State

Expected Version

Expected Domain Events

Expected Rejection

Expected External Effects
```

---

# Regla Given / When / Then

Los escenarios utilizan conceptualmente:

```text
Given

↓

When

↓

Then
```

Ejemplo:

```text
Given

Proposal = Draft

When

SubmitProposal

Then

Proposal = Submitted
ProposalSubmitted emitted
Version incremented
```

La estructura permite expresar comportamiento sin depender de una
tecnología específica.

---

# Categorías de Escenarios

Los escenarios se organizan conceptualmente en:

```text
Creation Scenarios

Lifecycle Scenarios

State Machine Scenarios

Command Scenarios

Invariant Scenarios

Permission Scenarios

Domain Event Scenarios

Versioning Scenarios

Repository Scenarios

Consistency Boundary Scenarios

Integration Event Scenarios

Read Model Scenarios

Concurrency Scenarios

Negative Scenarios
```

---

# Escenario 001 — Crear una Proposal válida

## Objetivo

Verificar que una Proposal pueda crearse cuando los datos
requeridos y las precondiciones del dominio son válidos.

## Given

```text
OrganizationId válido

ProposerReference válida

Title válido

Description válida cuando corresponda

ProposalType válido

TerritoryId válido cuando corresponda

AssemblyId válido cuando corresponda

Actor autorizado
```

## When

```text
CreateProposal
```

## Then

Debe existir una nueva Proposal con:

```text
ProposalId único

OrganizationId esperado

ProposerReference esperada

ProposalType esperado

ProposalStatus = Draft

Version inicial válida
```

Debe producirse:

```text
ProposalCreated
```

La creación no debe modificar ningún otro Aggregate.

---

# Escenario 002 — Crear Proposal sin OrganizationId

## Objetivo

Verificar que una Proposal no pueda existir sin contexto
organizacional válido.

## Given

```text
OrganizationId ausente
```

## When

```text
CreateProposal
```

## Then

La operación debe ser rechazada.

Debe mantenerse:

```text
No Proposal Created

No Domain Event

No Persistence
```

---

# Escenario 003 — Crear Proposal con tipo inválido

## Objetivo

Verificar que ProposalType respete las clasificaciones definidas
por el dominio.

## Given

```text
ProposalType inválido
```

## When

```text
CreateProposal
```

## Then

La operación debe ser rechazada.

No debe existir:

```text
ProposalCreated
```

---

# Escenario 004 — Crear Proposal con título inválido

## Objetivo

Verificar las reglas de validez de Title establecidas por
Proposal.

## Given

```text
Title inválido
```

## When

```text
CreateProposal
```

## Then

La creación debe rechazarse.

No debe existir un Aggregate parcialmente válido.

---

# Escenario 005 — Proposal inicia en Draft

## Objetivo

Verificar el estado inicial oficial del Aggregate.

## Given

Una creación válida.

## When

```text
CreateProposal
```

## Then

```text
ProposalStatus = Draft
```

Proposal no debe iniciar directamente en:

```text
Submitted

UnderReview

Accepted

Rejected

Withdrawn

Archived
```

---

# Escenario 006 — Modificar Proposal en Draft

## Objetivo

Verificar que los atributos modificables puedan actualizarse
mientras Proposal se encuentre en Draft y las invariantes lo
permitan.

## Given

```text
ProposalStatus = Draft
```

## When

Se ejecuta un Command válido de modificación definido por
Proposal.

## Then

La modificación debe:

- ser aceptada;
- preservar las invariantes;
- actualizar únicamente información permitida;
- incrementar Version;
- producir el Domain Event correspondiente.

---

# Escenario 007 — Presentar Proposal válida

## Objetivo

Verificar la transición formal desde Draft hacia Submitted.

## Given

```text
ProposalStatus = Draft
```

y todas las condiciones necesarias para presentación se
encuentran satisfechas.

## When

```text
SubmitProposal
```

## Then

```text
ProposalStatus = Submitted
```

Debe producirse:

```text
ProposalSubmitted
```

Version debe incrementarse exactamente una vez para la
modificación válida correspondiente.

---

# Escenario 008 — Presentar Proposal desde estado inválido

## Objetivo

Verificar que SubmitProposal solo pueda ejecutarse desde los
estados permitidos por la State Machine.

## Given

Proposal se encuentra en un estado que no permite presentación.

## When

```text
SubmitProposal
```

## Then

La operación debe ser rechazada.

Debe mantenerse:

```text
Status unchanged

Version unchanged

No ProposalSubmitted
```

---

# Escenario 009 — Iniciar revisión

## Objetivo

Verificar la transición hacia UnderReview.

## Given

```text
ProposalStatus = Submitted
```

y las condiciones de revisión se encuentran satisfechas.

## When

```text
StartProposalReview
```

## Then

```text
ProposalStatus = UnderReview
```

Debe producirse:

```text
ProposalReviewStarted
```

Version debe incrementarse.

---

# Escenario 010 — Iniciar revisión desde Draft

## Objetivo

Verificar que una Proposal no pueda ingresar directamente a
revisión omitiendo su presentación formal.

## Given

```text
ProposalStatus = Draft
```

## When

```text
StartProposalReview
```

## Then

La operación debe rechazarse.

Debe mantenerse:

```text
ProposalStatus = Draft

Version unchanged

No ProposalReviewStarted
```

---

# Escenario 011 — Aceptar Proposal

## Objetivo

Verificar la aceptación válida de una Proposal.

## Given

```text
ProposalStatus = UnderReview
```

y todas las precondiciones de aceptación están satisfechas.

## When

```text
AcceptProposal
```

## Then

```text
ProposalStatus = Accepted
```

Debe producirse:

```text
ProposalAccepted
```

Version debe incrementarse.

---

# Escenario 012 — Aceptar Proposal sin revisión

## Objetivo

Verificar que una Proposal no pueda ser aceptada desde un estado
que no permita dicha transición.

## Given

```text
ProposalStatus = Draft
```

o cualquier otro estado no autorizado.

## When

```text
AcceptProposal
```

## Then

La operación debe rechazarse.

No debe producirse:

```text
ProposalAccepted
```

---

# Escenario 013 — Rechazar Proposal

## Objetivo

Verificar el rechazo válido de una Proposal bajo revisión.

## Given

```text
ProposalStatus = UnderReview
```

## When

```text
RejectProposal
```

## Then

```text
ProposalStatus = Rejected
```

Debe producirse:

```text
ProposalRejected
```

Version debe incrementarse.

---

# Escenario 014 — Rechazar Proposal desde estado inválido

## Objetivo

Verificar que RejectProposal respete la State Machine.

## Given

Proposal se encuentra en un estado desde el cual el rechazo no
está permitido.

## When

```text
RejectProposal
```

## Then

La operación debe ser rechazada.

Debe mantenerse:

```text
Status unchanged

Version unchanged

No ProposalRejected
```

---

# Escenario 015 — Retirar Proposal

## Objetivo

Verificar que una Proposal pueda retirarse únicamente cuando su
Lifecycle lo permita.

## Given

Proposal se encuentra en un estado válido para retirada.

## When

```text
WithdrawProposal
```

## Then

```text
ProposalStatus = Withdrawn
```

Debe producirse:

```text
ProposalWithdrawn
```

Version debe incrementarse.

---

# Escenario 016 — Retirar Proposal desde estado terminal incompatible

## Objetivo

Verificar que una Proposal no pueda retirarse cuando ya alcanzó
un estado incompatible con dicha operación.

## Given

Proposal se encuentra en un estado terminal que no permite
WithdrawProposal.

## When

```text
WithdrawProposal
```

## Then

La operación debe rechazarse.

No debe modificarse:

```text
Status

Version
```

No debe producirse:

```text
ProposalWithdrawn
```

---

# Escenario 017 — Archivar Proposal

## Objetivo

Verificar que Proposal pueda alcanzar Archived únicamente desde
los estados permitidos.

## Given

Proposal se encuentra en un estado válido para archivado.

## When

```text
ArchiveProposal
```

## Then

```text
ProposalStatus = Archived
```

Debe producirse:

```text
ProposalArchived
```

Version debe incrementarse.

---

# Escenario 018 — Modificar Proposal archivada

## Objetivo

Verificar la inmutabilidad operacional de una Proposal archivada.

## Given

```text
ProposalStatus = Archived
```

## When

Se intenta ejecutar un Command de modificación.

## Then

La operación debe rechazarse.

Debe mantenerse:

```text
Proposal unchanged

Version unchanged

No modification Domain Event
```

---

# Escenario 019 — ProposalId es inmutable

## Objetivo

Verificar que la identidad del Aggregate nunca pueda modificarse.

## Given

Una Proposal existente:

```text
ProposalId = P-001
```

## When

Se intenta modificar ProposalId.

## Then

La operación debe ser imposible o rechazada.

Debe mantenerse:

```text
ProposalId = P-001
```

durante todo el Lifecycle.

---

# Escenario 020 — OrganizationId es inmutable

## Objetivo

Verificar que la propiedad organizacional de Proposal permanezca
estable durante su existencia.

## Given

```text
OrganizationId = ORG-001
```

## When

Se intenta reemplazar por:

```text
OrganizationId = ORG-002
```

## Then

La operación debe rechazarse.

Debe mantenerse:

```text
OrganizationId = ORG-001
```

---

# Escenario 021 — Referencia territorial no absorbe Territory

## Objetivo

Verificar que una relación territorial no incorpore el Aggregate
Territory dentro de Proposal.

## Given

```text
TerritoryId = TERR-001
```

## When

Proposal utiliza su contexto territorial.

## Then

Proposal debe mantener únicamente la referencia necesaria.

No debe contener:

```text
Territory Aggregate
```

como parte mutable de su límite de consistencia.

---

# Escenario 022 — Referencia a Assembly no absorbe Assembly

## Objetivo

Verificar la independencia entre Proposal y Assembly.

## Given

```text
AssemblyId = ASM-001
```

## When

Proposal se relaciona con una Assembly.

## Then

Debe utilizarse una referencia de identidad.

No debe incorporarse:

```text
Assembly Aggregate
```

dentro de Proposal.

---

# Escenario 023 — Referencia al proponente

## Objetivo

Verificar que el proponente sea representado mediante la
referencia definida por el modelo de Proposal.

## Given

Una Proposal posee:

```text
ProposerReference
```

## When

Se consulta su relación con el proponente.

## Then

Proposal debe utilizar la referencia correspondiente, como:

```text
CitizenId
```

o:

```text
MembershipId
```

según el modelo establecido.

No debe incorporar el Aggregate externo completo.

---

# Escenario 024 — Proposal no modifica Organization

## Objetivo

Verificar la separación entre Aggregates.

## Given

Una Proposal asociada a una Organization.

## When

Proposal ejecuta comportamiento interno.

## Then

No debe modificar directamente:

```text
Organization
```

Toda coordinación externa debe ocurrir fuera del Aggregate.

---

# Escenario 025 — Proposal no modifica Assembly

## Objetivo

Verificar que una operación sobre Proposal no cambie directamente
el estado de Assembly.

## Given

Una Proposal relacionada mediante:

```text
AssemblyId
```

## When

Proposal cambia de estado.

## Then

Assembly debe permanecer fuera de la transacción interna de
Proposal.

---

# Escenario 026 — Proposal no modifica Voting

## Objetivo

Verificar que la aceptación de una Proposal no cree ni modifique
directamente un Aggregate Voting.

## Given

```text
ProposalStatus = UnderReview
```

## When

```text
AcceptProposal
```

## Then

Proposal puede producir el hecho correspondiente.

No debe:

```text
Create Voting inside Proposal

Modify Voting directly
```

Voting conserva su propio límite de consistencia.

---

# Escenario 027 — Proposal no modifica Participation

## Objetivo

Verificar la separación entre Proposal y Participation.

## Given

Una Proposal relacionada con procesos de participación.

## When

Proposal ejecuta una transición válida.

## Then

No debe modificar directamente:

```text
Participation
```

---

# Escenario 028 — Command válido incrementa Version

## Objetivo

Verificar el versionado optimista del Aggregate.

## Given

```text
Version = N
```

## When

Un Command válido modifica Proposal.

## Then

```text
Version = N + 1
```

La modificación debe producir el Domain Event correspondiente.

---

# Escenario 029 — Command rechazado no incrementa Version

## Objetivo

Verificar que una operación inválida no altere la revisión del
Aggregate.

## Given

```text
Version = N
```

## When

Un Command viola una invariante o State Machine.

## Then

```text
Version = N
```

No debe existir modificación parcial.

---

# Escenario 030 — Consulta no incrementa Version

## Objetivo

Verificar que las operaciones de lectura no modifiquen el
Aggregate.

## Given

```text
Version = N
```

## When

Se ejecuta una consulta.

## Then

```text
Version = N
```

No debe producirse ningún Domain Event de modificación.

---

# Escenario 031 — Domain Event después de modificación válida

## Objetivo

Verificar que una modificación válida produzca el hecho de dominio
correspondiente.

## Given

Una operación permitida.

## When

El comportamiento del Aggregate se ejecuta correctamente.

## Then

Debe producirse el Domain Event definido para el hecho.

Ejemplo:

```text
SubmitProposal

↓

ProposalSubmitted
```

---

# Escenario 032 — No Domain Event ante operación rechazada

## Objetivo

Verificar que un hecho inexistente no sea publicado como Domain
Event.

## Given

Una operación inválida.

## When

El Aggregate rechaza el Command.

## Then

Debe mantenerse:

```text
No State Change

No Version Change

No Domain Event
```

---

# Escenario 033 — Domain Event representa hecho consumado

## Objetivo

Verificar la diferencia conceptual entre Command y Domain Event.

## Given

```text
SubmitProposal
```

## When

La operación es aceptada.

## Then

Debe producirse:

```text
ProposalSubmitted
```

No debe tratarse:

```text
SubmitProposal
```

como un hecho consumado.

---

# Escenario 034 — Permiso válido no reemplaza invariantes

## Objetivo

Verificar la separación entre autorización y validez del dominio.

## Given

Un actor posee permiso para ejecutar:

```text
AcceptProposal
```

pero Proposal se encuentra en un estado inválido para aceptación.

## When

El actor ejecuta el Command.

## Then

La operación debe ser rechazada por las reglas del Aggregate.

Debe mantenerse:

```text
Authorized Actor

≠

Automatically Valid Operation
```

---

# Escenario 035 — Actor sin permiso

## Objetivo

Verificar que una operación que requiere autorización no sea
ejecutada por un actor no autorizado.

## Given

El actor no posee la capacidad requerida.

## When

Intenta ejecutar el Command.

## Then

La operación no debe alcanzar una modificación válida del
Aggregate.

No debe producirse un Domain Event que represente una modificación
inexistente.

---

# Escenario 036 — Dominio no administra autenticación

## Objetivo

Verificar que Proposal no dependa de mecanismos técnicos de
autenticación.

## Given

Una operación autorizada por la capa correspondiente.

## When

Proposal recibe la intención válida para evaluación de dominio.

## Then

Proposal debe validar exclusivamente sus reglas e invariantes.

No debe requerir:

```text
Password

JWT

OAuth Token

Session

Authentication Provider
```

como parte de su modelo interno.

---

# Escenario 037 — Repository recupera Proposal por identidad

## Objetivo

Verificar el contrato conceptual de recuperación.

## Given

Una Proposal persistida con:

```text
ProposalId = P-001
```

## When

El Repository recibe la solicitud correspondiente.

## Then

Debe recuperar la unidad de consistencia identificada por:

```text
P-001
```

sin exponer persistencia parcial como si fueran Aggregates
independientes.

---

# Escenario 038 — Repository persiste Aggregate completo

## Objetivo

Verificar que Proposal sea persistida como unidad de consistencia.

## Given

Una modificación válida de Proposal.

## When

El Repository persiste el Aggregate.

## Then

Debe preservarse coherentemente:

```text
Identity

State

Domain Data

Version
```

No debe persistirse una modificación parcial que deje al
Aggregate en un estado inválido.

---

# Escenario 039 — Repository no modifica reglas del dominio

## Objetivo

Verificar que el Repository no contenga decisiones pertenecientes
a Proposal.

## Given

Una Proposal recuperada.

## When

Se ejecuta una transición de dominio.

## Then

La decisión debe ser realizada por Proposal.

No por:

```text
Repository

Database

ORM
```

---

# Escenario 040 — Concurrencia con Version correcta

## Objetivo

Verificar que una modificación pueda persistirse cuando la
versión esperada coincide con la versión persistida.

## Given

```text
PersistedVersion = 5

ExpectedVersion = 5
```

## When

Se persiste una modificación válida.

## Then

La operación puede confirmarse.

La nueva versión debe corresponder a la revisión siguiente según
las reglas de Versioning.

---

# Escenario 041 — Conflicto de concurrencia

## Objetivo

Verificar la detección de modificaciones concurrentes
incompatibles.

## Given

```text
PersistedVersion = 6

ExpectedVersion = 5
```

## When

Se intenta persistir una modificación basada en la versión
obsoleta.

## Then

La operación debe producir un conflicto de concurrencia.

No debe sobrescribirse silenciosamente la revisión más reciente.

---

# Escenario 042 — Conflicto no produce falso Domain Fact

## Objetivo

Verificar que una modificación no confirmada por conflicto de
concurrencia no sea tratada como un hecho externo confirmado.

## Given

Una operación produce un conflicto de Version.

## When

El Commit no puede confirmarse.

## Then

No debe publicarse externamente un Integration Event definitivo
que represente la modificación fallida.

---

# Escenario 043 — Un solo Consistency Boundary

## Objetivo

Verificar que una transacción de Proposal modifique
exclusivamente su propio límite de consistencia.

## Given

Una Proposal relacionada con:

```text
Organization

Territory

Assembly

Participation

Voting

Document
```

## When

Se ejecuta un Command sobre Proposal.

## Then

La transacción interna debe modificar únicamente:

```text
Proposal
```

Los otros Aggregates mantienen sus propios límites.

---

# Escenario 044 — No transacción distribuida entre Aggregates

## Objetivo

Verificar que Proposal no requiera modificar simultáneamente
múltiples Aggregates dentro de una única transacción de dominio.

## Given

Una operación de Proposal genera información relevante para otro
Bounded Context.

## When

La operación es confirmada.

## Then

La coordinación debe realizarse mediante los mecanismos
establecidos fuera del Aggregate.

No debe ampliarse:

```text
Proposal Consistency Boundary
```

---

# Escenario 045 — Integration Event después del Commit

## Objetivo

Verificar que un Integration Event represente únicamente un hecho
confirmado.

## Given

Una transición válida produce:

```text
ProposalSubmitted
```

## When

El estado es persistido y confirmado.

## Then

Puede producirse:

```text
ProposalSubmittedForIntegration
```

La publicación externa no debe preceder conceptualmente al Commit.

---

# Escenario 046 — No Integration Event ante Command rechazado

## Objetivo

Verificar que un Command inválido no produzca comunicación externa
de un hecho inexistente.

## Given

```text
SubmitProposal
```

es inválido en el estado actual.

## When

El Aggregate rechaza la operación.

## Then

Debe mantenerse:

```text
No State Change

No Domain Event

No Integration Event
```

---

# Escenario 047 — Integration Event no contiene Aggregate completo

## Objetivo

Verificar que los contratos de integración no serialicen
Proposal como objeto interno completo.

## Given

Un hecho debe comunicarse externamente.

## When

Se construye el Integration Event.

## Then

El Payload debe contener únicamente información contractual
necesaria.

No debe contener:

```text
Complete Proposal Aggregate
```

---

# Escenario 048 — Integration Event mantiene EventVersion

## Objetivo

Verificar la separación entre versión contractual y versión del
Aggregate.

## Given

```text
ProposalVersion = 12

EventVersion = 1
```

## When

Se publica un Integration Event.

## Then

Debe mantenerse:

```text
ProposalVersion = 12

EventVersion = 1
```

sin interpretar ambos conceptos como equivalentes.

---

# Escenario 049 — Entrega duplicada de Integration Event

## Objetivo

Verificar que una entrega repetida no represente un nuevo hecho
del dominio.

## Given

```text
EventId = EVENT-001
```

ya fue procesado.

## When

El mismo EventId es recibido nuevamente por un consumidor.

## Then

Debe interpretarse como la misma publicación lógica.

Debe mantenerse:

```text
Duplicate Delivery

≠

New Domain Fact
```

---

# Escenario 050 — Falla de consumidor externo

## Objetivo

Verificar que una falla externa no revierta automáticamente el
estado confirmado de Proposal.

## Given

```text
ProposalStatus = Accepted
```

y:

```text
ProposalAcceptedForIntegration
```

fue publicado.

## When

Un consumidor externo falla.

## Then

Proposal debe permanecer:

```text
Accepted
```

La recuperación pertenece al consumidor o mecanismo de
integración.

---

# Escenario 051 — Read Model se actualiza después del hecho

## Objetivo

Verificar la actualización eventual de las proyecciones.

## Given

```text
ProposalStatus = UnderReview
```

## When

```text
AcceptProposal
```

es confirmado y se produce:

```text
ProposalAccepted
```

## Then

las proyecciones afectadas deben converger hacia:

```text
ProposalStatus = Accepted
```

---

# Escenario 052 — Read Model no modifica Proposal

## Objetivo

Verificar la separación entre lectura y escritura.

## Given

Existe:

```text
ProposalDetail
```

## When

La proyección es consultada o reconstruida.

## Then

No debe producirse:

```text
Proposal State Change

ProposalVersion Change

Domain Event
```

---

# Escenario 053 — Read Model puede estar temporalmente atrasado

## Objetivo

Verificar la consistencia eventual del lado de lectura.

## Given

Proposal fue modificada y confirmada.

## When

La proyección todavía no ha procesado el evento correspondiente.

## Then

Puede observarse temporalmente una revisión anterior.

Esto no modifica la fuente de verdad.

---

# Escenario 054 — Reconstrucción de Read Model

## Objetivo

Verificar que una proyección pueda reconstruirse.

## Given

Existe el historial necesario de hechos del dominio.

## When

La proyección es eliminada y regenerada.

## Then

Debe reconstruirse su estado lógico derivado.

Proposal no debe modificarse.

---

# Escenario 055 — Read Model desnormalizado no fusiona Aggregates

## Objetivo

Verificar que una vista compuesta no cambie los límites DDD.

## Given

Una proyección contiene:

```text
ProposalId

OrganizationName

TerritoryName

AssemblyReference
```

## When

La vista es consultada.

## Then

Debe interpretarse como información desnormalizada para lectura.

No debe interpretarse como:

```text
Organization

Territory

Assembly
```

formando parte del Aggregate Proposal.

---

# Escenario 056 — Consulta no ejecuta Command

## Objetivo

Verificar la separación CQRS.

## Given

Una solicitud de lectura.

## When

Se consulta:

```text
ProposalSummary
```

## Then

No debe ejecutarse un Command sobre Proposal.

---

# Escenario 057 — Proposal aceptada no crea Voting automáticamente

## Objetivo

Verificar que la relación futura con Voting respete los límites
entre Aggregates.

## Given

```text
ProposalStatus = UnderReview
```

## When

```text
AcceptProposal
```

## Then

Proposal debe alcanzar:

```text
Accepted
```

y producir:

```text
ProposalAccepted
```

pero no debe crear internamente:

```text
Voting
```

La coordinación correspondiente pertenece fuera del Aggregate.

---

# Escenario 058 — Proposal relacionada con Assembly conserva autonomía

## Objetivo

Verificar que una Proposal asociada a una Assembly conserve
identidad y Lifecycle propios.

## Given

```text
AssemblyId = ASM-001
```

## When

La Assembly cambia de estado.

## Then

Proposal no debe modificar automáticamente su estado interno salvo
que exista un hecho y proceso explícitamente definido por el
modelo correspondiente.

La relación contextual no implica dependencia estructural.

---

# Escenario 059 — Proposal conserva identidad después de cambios

## Objetivo

Verificar continuidad de identidad durante el Lifecycle.

## Given

```text
ProposalId = P-001
```

## When

Proposal atraviesa:

```text
Draft

↓

Submitted

↓

UnderReview

↓

Accepted
```

## Then

Debe mantenerse:

```text
ProposalId = P-001
```

en todas las revisiones.

---

# Escenario 060 — Estados válidos

## Objetivo

Verificar que Proposal únicamente pueda representar estados
definidos por su State Machine.

## Given

Una Proposal válida.

## When

Se intenta establecer un estado inexistente.

## Then

La operación debe rechazarse.

No puede existir:

```text
ProposalStatus = UndefinedDomainState
```

---

# Escenario 061 — Transición inválida no modifica timestamps

## Objetivo

Verificar que una transición rechazada no produzca información
temporal falsa.

## Given

Proposal se encuentra en un estado incompatible con aceptación.

## When

```text
AcceptProposal
```

es rechazado.

## Then

No debe establecerse:

```text
AcceptedAt
```

ni ningún timestamp que represente un hecho inexistente.

---

# Escenario 062 — Presentación establece información temporal válida

## Objetivo

Verificar que una presentación confirmada pueda establecer la
información temporal correspondiente.

## Given

```text
ProposalStatus = Draft
```

## When

```text
SubmitProposal
```

es aceptado.

## Then

Debe existir la información temporal correspondiente a la
presentación conforme al modelo definido.

Debe producirse:

```text
ProposalSubmitted
```

---

# Escenario 063 — Aceptación establece información temporal válida

## Objetivo

Verificar la coherencia entre estado, hecho y tiempo.

## Given

```text
ProposalStatus = UnderReview
```

## When

```text
AcceptProposal
```

es confirmado.

## Then

Debe mantenerse coherencia entre:

```text
ProposalStatus = Accepted

AcceptedAt

ProposalAccepted
```

---

# Escenario 064 — Rechazo establece información temporal válida

## Objetivo

Verificar la coherencia temporal del rechazo.

## Given

```text
ProposalStatus = UnderReview
```

## When

```text
RejectProposal
```

es confirmado.

## Then

Debe mantenerse coherencia entre:

```text
ProposalStatus = Rejected

RejectedAt

ProposalRejected
```

---

# Escenario 065 — Archivado establece información temporal válida

## Objetivo

Verificar la coherencia del archivado.

## Given

Proposal se encuentra en un estado válido para archivado.

## When

```text
ArchiveProposal
```

es confirmado.

## Then

Debe mantenerse coherencia entre:

```text
ProposalStatus = Archived

ArchivedAt

ProposalArchived
```

---

# Escenario 066 — No modificación parcial

## Objetivo

Verificar atomicidad conceptual del Aggregate.

## Given

Una operación requiere modificar múltiples elementos internos de
Proposal.

## When

Una invariante falla antes de completar la operación.

## Then

Debe mantenerse el estado anterior completo.

No debe existir:

```text
Partially Modified Proposal
```

---

# Escenario 067 — Error de persistencia no produce estado confirmado

## Objetivo

Verificar que una operación que no puede persistirse no sea
tratada como modificación confirmada.

## Given

Una modificación válida a nivel de dominio.

## When

La persistencia no puede confirmarse.

## Then

No debe comunicarse externamente el cambio como hecho confirmado.

La gestión técnica del error pertenece fuera del Aggregate.

---

# Escenario 068 — Domain Event mantiene ProposalId

## Objetivo

Verificar trazabilidad entre el hecho y el Aggregate originador.

## Given

```text
ProposalId = P-001
```

## When

Se produce un Domain Event.

## Then

El evento debe poder asociarse inequívocamente con:

```text
ProposalId = P-001
```

según el contrato de eventos establecido.

---

# Escenario 069 — CorrelationId mantiene trazabilidad

## Objetivo

Verificar que un flujo pueda correlacionar intención, hecho e
integración cuando corresponda.

## Given

Una operación posee:

```text
CorrelationId = CORR-001
```

## When

Se generan los artefactos correspondientes al flujo.

## Then

Debe poder reconstruirse conceptualmente:

```text
Command

↓

Domain Event

↓

Integration Event
```

como parte del mismo flujo lógico.

---

# Escenario 070 — CausationId mantiene causalidad

## Objetivo

Verificar la distinción entre correlación y causa inmediata.

## Given

Un Domain Event o Integration Event deriva de una operación
anterior.

## When

El evento es producido.

## Then

CausationId debe permitir identificar su causa inmediata cuando el
contrato correspondiente lo requiera.

Debe mantenerse:

```text
CorrelationId

≠

CausationId
```

---

# Escenario 071 — Datos sensibles no aparecen por defecto en Integration Events

## Objetivo

Verificar que Proposal no exponga información innecesaria mediante
sus contratos externos.

## Given

Una Proposal se relaciona con un Citizen o Membership.

## When

Se genera un Integration Event.

## Then

Debe utilizarse únicamente la información necesaria.

No deben incluirse por defecto:

```text
Passwords

Tokens

JWT

Private Keys

Authentication Secrets

Unnecessary Personal Data
```

---

# Escenario 072 — Proposal no depende de FIWARE

## Objetivo

Verificar independencia tecnológica del Aggregate.

## Given

Proposal debe interoperar posteriormente con FIWARE.

## When

Se ejecuta comportamiento de dominio.

## Then

Proposal no debe depender de:

```text
NGSI-LD

Context Broker

FIWARE APIs

FIWARE Authentication
```

La adaptación ocurre fuera del Aggregate.

---

# Escenario 073 — Proposal no depende de HTTP

## Objetivo

Verificar que el dominio sea independiente del protocolo de
transporte.

## Given

Una operación de Proposal es iniciada desde una API.

## When

La intención alcanza el dominio.

## Then

Proposal no debe conocer:

```text
HTTP Request

HTTP Response

Status Code

REST Route
```

---

# Escenario 074 — Proposal no depende de persistencia específica

## Objetivo

Verificar independencia respecto de Infrastructure.

## Given

Una implementación utiliza un mecanismo de persistencia.

## When

Proposal ejecuta comportamiento.

## Then

El modelo de dominio no debe depender de:

```text
PostgreSQL

MongoDB

MySQL

SQLite

ORM
```

---

# Escenario 075 — Proposal no expone setters para estado protegido

## Objetivo

Verificar encapsulación del Aggregate Root.

## Given

Una Proposal existente.

## When

Un consumidor intenta modificar directamente:

```text
ProposalId

OrganizationId

ProposalStatus

Version
```

## Then

La modificación directa debe ser imposible.

Los cambios válidos deben ocurrir mediante comportamiento del
Aggregate.

---

# Escenario 076 — Cambio válido utiliza comportamiento explícito

## Objetivo

Verificar que Proposal represente comportamiento y no un
contenedor pasivo de datos.

## Given

Una modificación permitida por el dominio.

## When

La modificación es solicitada.

## Then

Debe ejecutarse mediante el comportamiento conceptual definido por
Proposal.

El comportamiento debe validar:

- estado;
- invariantes;
- reglas aplicables;
- consistencia;
- Version.

---

# Escenario 077 — Estado terminal protege operaciones posteriores

## Objetivo

Verificar que los estados terminales mantengan las restricciones
definidas por el Lifecycle.

## Given

Proposal se encuentra en un estado terminal.

## When

Se intenta ejecutar una operación no permitida.

## Then

Debe rechazarse.

No debe modificarse:

```text
State

Version

Domain Data
```

---

# Escenario 078 — Múltiples lecturas no modifican Proposal

## Objetivo

Verificar que la cantidad de consultas no tenga impacto sobre el
Write Model.

## Given

```text
ProposalVersion = N
```

## When

Se ejecutan múltiples consultas.

## Then

Debe mantenerse:

```text
ProposalVersion = N
```

Las consultas no producen hechos de dominio.

---

# Escenario 079 — Nueva proyección no modifica Aggregate

## Objetivo

Verificar la extensibilidad del lado de lectura.

## Given

Existe una nueva necesidad de consulta.

## When

Se incorpora una nueva proyección derivada.

## Then

Proposal no debe modificarse únicamente por la existencia de la
nueva vista.

---

# Escenario 080 — Nueva integración no modifica invariantes

## Objetivo

Verificar que incorporar un nuevo consumidor externo no altere las
reglas fundamentales de Proposal.

## Given

Un nuevo sistema necesita consumir hechos de Proposal.

## When

Se incorpora la integración.

## Then

Las invariantes de Proposal deben permanecer independientes del
consumidor.

---

# Escenario 081 — Domain Event e Integration Event son diferentes

## Objetivo

Verificar la separación entre hechos internos y contratos
externos.

## Given

```text
ProposalAccepted
```

ha ocurrido.

## When

El hecho debe comunicarse externamente.

## Then

Puede derivarse:

```text
ProposalAcceptedForIntegration
```

Debe mantenerse:

```text
ProposalAccepted

≠

ProposalAcceptedForIntegration
```

en responsabilidad contractual.

---

# Escenario 082 — EventVersion no altera ProposalVersion

## Objetivo

Verificar independencia entre versiones.

## Given

```text
ProposalVersion = 15
```

y el contrato externo evoluciona desde:

```text
EventVersion = 1
```

a:

```text
EventVersion = 2
```

## When

Se publica la nueva versión contractual.

## Then

ProposalVersion no debe modificarse únicamente debido al cambio
del contrato de integración.

---

# Escenario 083 — Reproyección no genera Domain Events

## Objetivo

Verificar que reconstruir vistas no produzca nuevos hechos del
dominio.

## Given

Existe una secuencia válida de Domain Events.

## When

Se reconstruyen Read Models.

## Then

No deben generarse nuevos Domain Events de Proposal por el solo
hecho de reproyectar.

---

# Escenario 084 — Read Model no reemplaza Repository

## Objetivo

Verificar separación entre persistencia del Aggregate y
persistencia de lectura.

## Given

Existe:

```text
ProposalDetail
```

## When

Debe ejecutarse un Command sobre Proposal.

## Then

El Write Model debe obtener la unidad de consistencia mediante el
contrato correspondiente del Repository.

No debe utilizarse ProposalDetail como sustituto arbitrario del
Aggregate.

---

# Escenario 085 — Error de proyección no invalida Commit

## Objetivo

Verificar separación entre consistencia interna y disponibilidad
del lado de lectura.

## Given

Proposal confirma una modificación válida.

## When

La actualización de una proyección falla temporalmente.

## Then

El estado confirmado de Proposal no debe revertirse
automáticamente.

El Read Model puede recuperarse posteriormente.

---

# Escenario 086 — Proposal conserva lenguaje ubicuo

## Objetivo

Verificar que la implementación mantenga los conceptos definidos
por el dominio.

## Given

Los conceptos oficiales incluyen:

```text
Proposal

ProposalId

ProposalStatus

ProposalType

SubmitProposal

ProposalSubmitted
```

## When

Se implementa el Aggregate.

## Then

Los conceptos no deben sustituirse arbitrariamente por términos
que cambien su significado de dominio.

---

# Escenario 087 — Caso completo aceptado

## Objetivo

Verificar un flujo completo válido desde creación hasta
aceptación.

## Given

Una Organization válida y un actor autorizado.

## When

Se ejecuta:

```text
CreateProposal

↓

SubmitProposal

↓

StartProposalReview

↓

AcceptProposal
```

## Then

La evolución esperada es:

```text
Draft

↓

Submitted

↓

UnderReview

↓

Accepted
```

Deben existir los hechos correspondientes:

```text
ProposalCreated

ProposalSubmitted

ProposalReviewStarted

ProposalAccepted
```

Version debe evolucionar conforme a cada modificación válida.

---

# Escenario 088 — Caso completo rechazado

## Objetivo

Verificar un flujo completo válido desde creación hasta rechazo.

## Given

Una Proposal válida.

## When

Se ejecuta:

```text
CreateProposal

↓

SubmitProposal

↓

StartProposalReview

↓

RejectProposal
```

## Then

La evolución esperada es:

```text
Draft

↓

Submitted

↓

UnderReview

↓

Rejected
```

Deben existir:

```text
ProposalCreated

ProposalSubmitted

ProposalReviewStarted

ProposalRejected
```

---

# Escenario 089 — Caso completo retirado

## Objetivo

Verificar un flujo válido que finaliza mediante retirada.

## Given

Una Proposal se encuentra en un estado donde WithdrawProposal está
permitido.

## When

```text
WithdrawProposal
```

## Then

Debe alcanzar:

```text
Withdrawn
```

y producir:

```text
ProposalWithdrawn
```

---

# Escenario 090 — Caso completo archivado

## Objetivo

Verificar que una Proposal pueda completar su Lifecycle hasta
Archived conforme a la State Machine.

## Given

Proposal se encuentra en un estado permitido para archivado.

## When

```text
ArchiveProposal
```

## Then

Debe alcanzar:

```text
Archived
```

y producir:

```text
ProposalArchived
```

Después del archivado, las modificaciones no permitidas deben ser
rechazadas.

---

# Matriz de Estados y Escenarios

```text
Estado          Escenarios principales

Draft           Creation
                Editing
                Submission
                Withdrawal cuando corresponda
                Invalid Review
                Invalid Acceptance

Submitted       Review
                Withdrawal cuando corresponda
                Invalid Submission

UnderReview     Acceptance
                Rejection
                Withdrawal cuando corresponda

Accepted        Archival
                Terminal Restrictions

Rejected        Archival
                Terminal Restrictions

Withdrawn       Archival
                Terminal Restrictions

Archived        Immutability
                Read Only
```

La matriz debe interpretarse conjuntamente con:

```text
DOMAIN-007A-Lifecycle.md

DOMAIN-007B-State-Machine.md
```

Las transiciones oficiales son las definidas en dichos documentos.

---

# Matriz Command / Resultado Esperado

```text
Command                     Resultado conceptual

CreateProposal              ProposalCreated

SubmitProposal              ProposalSubmitted

StartProposalReview         ProposalReviewStarted

AcceptProposal              ProposalAccepted

RejectProposal              ProposalRejected

WithdrawProposal            ProposalWithdrawn

ArchiveProposal             ProposalArchived
```

Los Commands adicionales definidos en:

```text
DOMAIN-007C-Commands.md
```

deben verificarse siguiendo el mismo patrón:

```text
Valid Command

↓

Valid State Change

↓

Version Increment

↓

Expected Domain Event
```

---

# Matriz de Rechazo

```text
Condición inválida                  Resultado

Invalid State                       Reject Command

Invariant Violation                 Reject Command

Unauthorized Actor                  No Valid Modification

Archived Proposal                   Reject Modification

Version Conflict                    Reject Persistence

Invalid Identity Change             Reject Operation

Invalid Organization Change         Reject Operation

Invalid ProposalType                Reject Operation
```

En todos los rechazos de dominio debe preservarse:

```text
No Partial State

No Invalid Version Increment

No False Domain Event
```

---

# Matriz de Límites

```text
Concepto         Dentro de Proposal   Referenciado

Proposal         Sí                   No

Organization     No                   Sí

Citizen          No                   Sí

Membership       No                   Sí

Territory        No                   Sí

Assembly         No                   Sí

Participation    No                   Sí

Voting           No                   Sí

Document         No                   Sí

Notification     No                   Mediante eventos

Audit            No                   Mediante eventos

Integration      No                   Mediante contratos
```

Una referencia no implica pertenencia al Aggregate.

---

# Matriz de Versionado

```text
Operación                         Version

Create valid Proposal             Initial Version

Valid modification                +1

Valid state transition            +1

Rejected Command                  unchanged

Query                             unchanged

Read Model rebuild                unchanged

Integration retry                 unchanged

External consumer failure         unchanged

Concurrency conflict              no confirmed overwrite
```

---

# Matriz de Eventos

```text
Operación válida              Domain Event

Create                        ProposalCreated

Submit                        ProposalSubmitted

Start Review                  ProposalReviewStarted

Accept                        ProposalAccepted

Reject                        ProposalRejected

Withdraw                      ProposalWithdrawn

Archive                       ProposalArchived
```

Una operación rechazada no produce el evento que representaría su
éxito.

---

# Matriz de Integración

```text
Domain Event                    Integration Event conceptual

ProposalCreated                 ProposalCreatedForIntegration

ProposalSubmitted               ProposalSubmittedForIntegration

ProposalReviewStarted           ProposalReviewStartedForIntegration

ProposalAccepted                ProposalAcceptedForIntegration

ProposalRejected                ProposalRejectedForIntegration

ProposalWithdrawn               ProposalWithdrawnForIntegration

ProposalArchived                ProposalArchivedForIntegration
```

La existencia del Domain Event no obliga a publicación externa
cuando no exista relevancia de integración.

---

# Matriz de Read Models

```text
Necesidad                      Read Model

Listado                        ProposalSummary

Detalle                        ProposalDetail

Búsqueda                       ProposalDirectory

Estado                         ProposalStatus

Organization                   ProposalOrganization

Territory                      ProposalTerritory

Assembly                       ProposalAssembly

Proponente                     ProposalProposer

Revisión                       ProposalReview

Actividad                      ProposalActivity

Estadísticas                   ProposalStatistics
```

---

# Criterios de Aceptación del Aggregate

Una implementación de Proposal cumple conceptualmente con este
modelo cuando:

- crea Proposals únicamente con información válida;
- inicia en el estado definido por el Lifecycle;
- protege ProposalId;
- protege OrganizationId;
- controla todas las transiciones mediante comportamiento;
- rechaza transiciones inválidas;
- preserva invariantes;
- incrementa Version únicamente ante modificaciones válidas;
- no incrementa Version ante consultas;
- no incrementa Version ante operaciones rechazadas;
- produce Domain Events únicamente ante hechos válidos;
- mantiene otros Aggregates fuera de su límite;
- utiliza referencias por identidad;
- no modifica directamente Aggregates externos;
- persiste Proposal como unidad de consistencia;
- detecta conflictos de concurrencia;
- mantiene separación entre autorización e invariantes;
- mantiene separación entre Domain Events e Integration Events;
- mantiene separación entre Write Model y Read Models;
- mantiene independencia tecnológica;
- permite reconstruir proyecciones;
- mantiene consistencia eventual fuera del Aggregate;
- no expone el Aggregate completo mediante contratos externos.

---

# Criterios de Fallo

Una implementación debe considerarse incompatible con el modelo
oficial cuando permite cualquiera de las siguientes condiciones:

- ProposalId mutable;
- OrganizationId mutable;
- estado modificable directamente;
- Version modificable directamente;
- transición inválida aceptada;
- Aggregate archivado modificable;
- Command rechazado que incrementa Version;
- Command rechazado que produce un falso Domain Event;
- persistencia parcial;
- sobrescritura silenciosa ante conflicto de concurrencia;
- otro Aggregate almacenado como entidad interna de Proposal;
- modificación directa de Organization;
- modificación directa de Territory;
- modificación directa de Assembly;
- modificación directa de Participation;
- modificación directa de Voting;
- lógica de autenticación dentro del Aggregate;
- dependencia de HTTP dentro del dominio;
- dependencia de ORM dentro del dominio;
- dependencia de FIWARE dentro del Aggregate;
- Read Model utilizado como fuente autoritativa de escritura;
- Integration Event publicado como hecho confirmado antes del
  Commit;
- serialización completa del Aggregate como contrato de
  integración.

---

# Pruebas de Regresión

Toda evolución futura de Proposal debe volver a verificar los
escenarios existentes.

Una extensión no debe invalidar silenciosamente:

```text
Identity Rules

Lifecycle

State Machine

Invariants

Versioning

Consistency Boundary

Event Semantics

Aggregate Independence
```

Si una evolución modifica deliberadamente una regla oficial, debe
actualizarse primero la documentación conceptual correspondiente.

Los tests deben reflejar el dominio.

El dominio no debe redefinirse accidentalmente para satisfacer una
implementación defectuosa.

---

# Pruebas de Extensión

Cuando se incorpore una extensión válida deberán agregarse
escenarios para verificar:

- comportamiento nuevo;
- compatibilidad con invariantes existentes;
- compatibilidad con Lifecycle;
- compatibilidad con State Machine;
- nuevos Commands cuando correspondan;
- nuevos Domain Events cuando correspondan;
- impacto sobre Version;
- impacto sobre Read Models;
- impacto sobre Integration Events;
- preservación del Consistency Boundary.

Las reglas de extensión se documentarán en:

```text
DOMAIN-007P-Extension-Points.md
```

---

# Independencia de Implementación

Los escenarios definidos en este documento pueden implementarse
utilizando cualquier tecnología que preserve el comportamiento
conceptual.

No dependen de:

```text
Python

Java

TypeScript

C#

Go

FastAPI

Django

Spring

NestJS

PostgreSQL

MongoDB
```

La tecnología puede cambiar.

El comportamiento esperado del dominio permanece.

---

# Compatibilidad con BDD

Los escenarios pueden expresarse mediante Behaviour-Driven
Development.

Ejemplo conceptual:

```text
Given a Proposal in Draft

When SubmitProposal is accepted

Then Proposal becomes Submitted

And ProposalSubmitted is produced

And Version is incremented
```

BDD constituye una forma de expresar los escenarios.

No modifica el modelo de dominio.

---

# Compatibilidad con TDD

Los escenarios pueden utilizarse como base para Test-Driven
Development.

Conceptualmente:

```text
Domain Rule

↓

Test Scenario

↓

Test

↓

Implementation
```

La implementación debe satisfacer las reglas documentadas.

No debe invertirse la relación de manera que una decisión
accidental del código redefina silenciosamente el dominio.

---

# Compatibilidad con Event Sourcing

Cuando Proposal utilice Event Sourcing, los escenarios deben poder
verificar también:

- reconstrucción desde eventos;
- secuencia válida de hechos;
- Version coherente;
- rechazo de eventos incompatibles;
- reproducción determinista del estado;
- ausencia de efectos externos durante replay;
- reconstrucción de Read Models.

El Event Stream no modifica las invariantes establecidas para
Proposal.

---

# Escenario 091 — Reconstrucción del Aggregate desde eventos

## Objetivo

Verificar que una secuencia válida de Domain Events pueda
reconstruir conceptualmente el estado correspondiente cuando se
utilice Event Sourcing.

## Given

```text
ProposalCreated

ProposalSubmitted

ProposalReviewStarted

ProposalAccepted
```

## When

Se reconstruye Proposal.

## Then

El estado resultante debe representar:

```text
ProposalStatus = Accepted
```

con identidad y Version coherentes con la historia procesada.

---

# Escenario 092 — Replay no produce efectos externos

## Objetivo

Verificar que reconstruir el Aggregate no vuelva a ejecutar
efectos de integración como si fueran hechos nuevos.

## Given

Un historial existente.

## When

Se ejecuta replay.

## Then

No deben producirse automáticamente nuevas comunicaciones
externas equivalentes a hechos ya publicados.

Debe mantenerse:

```text
Replay

≠

New Domain Activity
```

---

# Escenario 093 — Secuencia de eventos inválida

## Objetivo

Verificar que una historia incompatible con la State Machine no
sea interpretada silenciosamente como una evolución válida.

## Given

Una secuencia conceptual incompatible, por ejemplo:

```text
ProposalCreated

↓

ProposalAccepted
```

sin los hechos intermedios requeridos por el modelo consolidado.

## When

La secuencia es evaluada.

## Then

Debe identificarse la incompatibilidad con el Lifecycle y la State
Machine oficiales.

---

# Escenario 094 — Estado y eventos permanecen coherentes

## Objetivo

Verificar que el estado observable corresponda a los hechos
confirmados.

## Given

```text
ProposalStatus = Rejected
```

## When

Se examina la evolución que produjo el estado.

## Then

Debe existir coherencia con:

```text
ProposalRejected
```

y no con un hecho contradictorio utilizado para representar la
misma transición.

---

# Escenario 095 — Timestamp no sustituye State Machine

## Objetivo

Verificar que la presencia de información temporal no determine
por sí sola una transición válida.

## Given

Existe un valor temporal asociado a una operación.

## When

El estado actual no permite la transición.

## Then

La operación continúa siendo inválida.

Debe mantenerse:

```text
Timestamp

≠

State Transition Authorization
```

---

# Escenario 096 — Referencia válida no otorga permiso

## Objetivo

Verificar que poseer una relación con Proposal no autorice
automáticamente operaciones sobre ella.

## Given

Un Citizen o Membership se encuentra relacionado con Proposal.

## When

Intenta ejecutar un Command.

## Then

La autorización debe evaluarse conforme a:

```text
DOMAIN-007F-Permissions.md
```

La relación de dominio por sí sola no sustituye las reglas de
autorización.

---

# Escenario 097 — Autorización no cambia el Lifecycle

## Objetivo

Verificar que Permissions no introduzca transiciones alternativas.

## Given

Un actor posee autorización elevada.

## When

Intenta una transición prohibida por la State Machine.

## Then

La operación debe rechazarse.

Debe mantenerse:

```text
Permission

≠

Lifecycle Override
```

---

# Escenario 098 — Repository no expone modificación parcial

## Objetivo

Verificar que el contrato de persistencia no permita eludir al
Aggregate Root.

## Given

Una Proposal existente.

## When

Un consumidor intenta persistir directamente un cambio aislado de:

```text
ProposalStatus
```

o:

```text
Version
```

sin ejecutar comportamiento del Aggregate.

## Then

El contrato oficial del Repository no debe proporcionar dicho
mecanismo como operación válida de dominio.

---

# Escenario 099 — Cambio de infraestructura preserva comportamiento

## Objetivo

Verificar independencia tecnológica.

## Given

Una implementación cambia su tecnología de persistencia.

## When

Se ejecutan nuevamente los Test Scenarios oficiales.

## Then

El comportamiento de Proposal debe permanecer equivalente.

Debe mantenerse:

```text
Infrastructure Change

≠

Domain Behavior Change
```

---

# Escenario 100 — Nuevo consumidor preserva Proposal

## Objetivo

Verificar que agregar una nueva integración no requiera introducir
al consumidor dentro del Aggregate.

## Given

Un nuevo sistema necesita conocer:

```text
ProposalAccepted
```

## When

Se incorpora el consumidor.

## Then

La integración debe realizarse fuera del Aggregate mediante los
contratos correspondientes.

Proposal no debe adquirir una dependencia directa hacia el nuevo
sistema.

---

# Principios de Verificación

Todo Test Scenario debe verificar una o más de las siguientes
propiedades:

```text
Identity

State

Transition

Invariant

Authorization Boundary

Version

Domain Event

Persistence

Consistency Boundary

Integration Contract

Read Projection

Technology Independence
```

Las pruebas deben concentrarse en resultados observables del
dominio.

---

# Regla de Cobertura Conceptual

La cobertura de pruebas no debe medirse únicamente por líneas de
código.

La cobertura relevante para Proposal comprende:

```text
All Valid State Transitions

All Invalid State Transitions

All Commands

All Critical Invariants

All Terminal States

All Identity Rules

All Version Rules

All Consistency Boundary Rules

All Relevant Domain Events

All Relevant Permission Boundaries

All Integration Publication Rules

All Read Model Separation Rules
```

Una implementación con alta cobertura técnica pero sin cobertura
de estas reglas no demuestra conformidad con el modelo de dominio.

---

# Regla de Escenarios Positivos y Negativos

Toda operación relevante debe disponer conceptualmente de:

```text
Positive Scenario
```

y:

```text
Negative Scenario
```

Ejemplo:

```text
Valid SubmitProposal

Invalid SubmitProposal
```

Esto permite demostrar tanto la capacidad de ejecutar
comportamiento permitido como la capacidad del Aggregate de
protegerse frente a comportamiento inválido.

---

# Regla de Estado Inicial

Cada escenario debe declarar explícitamente el estado relevante
cuando la operación dependa de la State Machine.

No debe suponerse implícitamente que cualquier Command es válido
desde cualquier estado.

---

# Regla de Estado Final

Cuando una operación modifica Proposal, el escenario debe verificar
el estado resultante.

Ejemplo:

```text
Given

ProposalStatus = Submitted

When

StartProposalReview

Then

ProposalStatus = UnderReview
```

---

# Regla de Eventos

Cuando una operación válida produzca un Domain Event definido por
el modelo, el escenario debe verificar:

```text
Event Type

Aggregate Identity

Relevant Domain Data

Version cuando corresponda

Temporal Information cuando corresponda
```

No debe verificarse únicamente que "algún evento" fue producido.

---

# Regla de Ausencia de Eventos

Los escenarios negativos deben verificar explícitamente la ausencia
del evento que habría representado un hecho exitoso.

Ejemplo:

```text
Invalid AcceptProposal

↓

No ProposalAccepted
```

Esta condición protege la semántica del historial de dominio.

---

# Regla de Versionado

Toda modificación válida debe verificarse contra las reglas
definidas en:

```text
DOMAIN-007I-Versioning.md
```

Debe distinguirse entre:

```text
ProposalVersion

EventVersion

Read Model ProjectedVersion
```

Estos conceptos no son intercambiables.

---

# Regla de Consistencia

Los escenarios que involucren otros Aggregates deben verificar que
Proposal no amplíe su transacción para incorporar sus estados
internos.

Debe mantenerse:

```text
Proposal Transaction

=

Proposal Consistency Boundary
```

---

# Regla de Integración

Los escenarios de integración deben verificar:

```text
Domain Fact Confirmed

↓

Integration Mapping

↓

Integration Event
```

Nunca:

```text
Unconfirmed Intent

↓

Integration Event representing success
```

---

# Regla de Lectura

Los escenarios de lectura deben verificar:

```text
Query

↓

Read Model

↓

Result
```

sin producir:

```text
Proposal Modification
```

---

# Regla de Seguridad

Las pruebas relacionadas con seguridad deben verificar que Proposal
no incorpore mecanismos técnicos de autenticación dentro del
Aggregate.

También deben verificar que información expuesta mediante
proyecciones o integraciones respete las responsabilidades
definidas por el modelo de seguridad correspondiente.

La especificación formal se desarrollará en:

```text
DOMAIN-007O-Security-Model.md
```

---

# Regla de Rendimiento

Las pruebas de rendimiento no deben modificar las reglas del
dominio para obtener mejores métricas.

Una optimización no puede permitir:

- omitir invariantes;
- evitar validaciones obligatorias;
- alterar transiciones;
- omitir Version;
- publicar eventos antes de confirmar estado;
- convertir Read Models en Write Models.

Las reglas correspondientes se desarrollarán en:

```text
DOMAIN-007N-Performance-Rules.md
```

---

# Regla de Evolución

Cuando Proposal evolucione, los escenarios existentes constituyen
una protección contra regresiones conceptuales.

Una modificación futura debe determinar explícitamente si:

```text
Existing Scenario remains valid
```

o si existe una modificación deliberada del modelo oficial que
requiere actualizar la documentación correspondiente.

Los escenarios no deben modificarse únicamente para hacer pasar una
implementación que contradiga el dominio documentado.

---

# Compatibilidad Arquitectónica

Los Test Scenarios de Proposal son compatibles con:

- Domain-Driven Design;
- Behaviour-Driven Development;
- Test-Driven Development;
- Clean Architecture;
- Hexagonal Architecture;
- CQRS;
- Event Sourcing;
- Event-Driven Architecture;
- SOLID;
- optimistic concurrency;
- consistencia eventual;
- arquitectura distribuida;
- pruebas independientes de infraestructura.

---

# Principios Arquitectónicos

Los Test Scenarios mantienen:

```text
Domain Specification

≠

Implementation Detail
```

```text
Valid Command

≠

Rejected Command
```

```text
Permission

≠

Invariant
```

```text
Permission

≠

Lifecycle Override
```

```text
Command

≠

Domain Event
```

```text
Domain Event

≠

Integration Event
```

```text
ProposalVersion

≠

EventVersion
```

```text
Query

≠

Command
```

```text
Read Model

≠

Aggregate
```

```text
Read Model

≠

Source of Truth
```

```text
External Reference

≠

Aggregate Membership
```

```text
Consistency Boundary

≠

Distributed Transaction
```

```text
Replay

≠

New Domain Activity
```

```text
Infrastructure Change

≠

Domain Behavior Change
```

```text
Test Coverage

≠

Only Code Coverage
```

---

# Documentación Complementaria

Los Test Scenarios deben interpretarse conjuntamente con:

```text
DOMAIN-007-Aggregate.md

DOMAIN-007A-Lifecycle.md

DOMAIN-007B-State-Machine.md

DOMAIN-007C-Commands.md

DOMAIN-007D-Domain-Events.md

DOMAIN-007E-Invariants.md

DOMAIN-007F-Permissions.md

DOMAIN-007G-Repository-Contract.md

DOMAIN-007H-Examples.md

DOMAIN-007I-Versioning.md

DOMAIN-007J-Consistency-Boundary.md

DOMAIN-007K-Integration-Events.md

DOMAIN-007L-Read-Model.md

DOMAIN-007N-Performance-Rules.md

DOMAIN-007O-Security-Model.md

DOMAIN-007P-Extension-Points.md
```

Estos documentos constituyen conjuntamente la definición
conceptual del Aggregate Proposal.

Los Test Scenarios no sustituyen ninguno de ellos.

Su responsabilidad es expresar de forma verificable el
comportamiento, restricciones y límites establecidos por el modelo
oficial.

---

# Definición de Éxito

Los Test Scenarios del Aggregate **Proposal** constituyen la
especificación conceptual verificable que permite demostrar que
una implementación respeta el modelo oficial definido por AURA
Core.

Los escenarios verifican de forma explícita:

```text
Identity

Lifecycle

State Machine

Commands

Domain Events

Invariants

Permissions

Repository Contract

Versioning

Consistency Boundary

Integration Events

Read Models

Aggregate Independence
```

Una implementación conforme debe demostrar tanto comportamiento
válido como rechazo correcto de operaciones incompatibles con el
dominio.

Las pruebas deben garantizar que:

- Proposal mantiene identidad estable;
- OrganizationId permanece protegido;
- las transiciones respetan la State Machine;
- las invariantes permanecen protegidas;
- los Commands rechazados no modifican estado;
- los Commands rechazados no incrementan Version;
- los Commands rechazados no generan falsos hechos;
- los Domain Events representan únicamente hechos consumados;
- Version evoluciona únicamente ante modificaciones válidas;
- los conflictos de concurrencia no sobrescriben silenciosamente
  revisiones posteriores;
- otros Aggregates permanecen fuera del Consistency Boundary;
- las integraciones no amplían la transacción del Aggregate;
- los Read Models permanecen derivados y reconstruibles;
- las consultas no modifican Proposal;
- las decisiones de infraestructura no redefinen el dominio.

De esta forma, `DOMAIN-007M-Test-Scenarios.md` proporciona la base
conceptual para pruebas unitarias de dominio, pruebas de
comportamiento, pruebas de regresión, pruebas de integración
arquitectónica y validación futura de implementaciones del
Aggregate **Proposal**, preservando la coherencia del lenguaje
ubicuo, los límites DDD y las reglas consolidadas de AURA Core.