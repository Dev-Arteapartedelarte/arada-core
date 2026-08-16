# DOMAIN-012 — Audit Aggregate

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Audit Management

Aggregate:
Audit

Autor:
ARADA

Documentos Relacionados:

- CORE-002-Bounded-Context-Map.md
- CORE-003-Shared-Kernel.md
- CORE-004-Ubiquitous-Language.md
- CORE-006-Domain-Invariants.md
- CORE-007-Strategic-Design.md
- CORE-008-Aggregate-Design-Rules.md
- CORE-011-Repository-Contracts.md
- DOMAIN-001-Aggregate.md
- DOMAIN-002-Aggregate.md
- DOMAIN-003-Aggregate.md
- DOMAIN-004-Aggregate.md
- DOMAIN-005-Aggregate.md
- DOMAIN-006-Aggregate.md
- DOMAIN-007-Aggregate.md
- DOMAIN-008-Aggregate.md
- DOMAIN-009-Aggregate.md
- DOMAIN-010-Aggregate.md
- DOMAIN-011-Aggregate.md

---

# Objetivo

El Aggregate **Audit** representa una unidad formal de trazabilidad
dentro del ecosistema AURA.

Su responsabilidad es mantener una representación propia de hechos
auditables provenientes de actividades y cambios relevantes
ocurridos dentro del dominio.

Audit permite conservar evidencia conceptual sobre hechos ya
ocurridos sin modificar los Aggregates que los originaron.

Debe mantenerse:

```text
Source Domain Fact

≠

Audit
```

y:

```text
Domain Event

≠

Audit Record
```

Audit mantiene su propio Aggregate y su propio límite de
consistencia.

---

# Propósito

El propósito del Aggregate Audit es proporcionar trazabilidad
independiente sobre hechos relevantes del ecosistema AURA.

Audit permite conservar información necesaria para responder
conceptualmente:

```text
What happened?

When did it happen?

Where did the fact originate?

Who or what participated when that information is available?

What fact or interaction caused it when that information is available?

To which execution flow does it belong when that information is available?
```

sin adquirir autoridad sobre el estado del Aggregate originador.

Audit constituye el límite de consistencia de su propia
representación auditable.

No constituye el límite de consistencia de los Aggregates
auditados.

---

# Definición

Audit representa una unidad de información de trazabilidad creada a
partir de un hecho relevante ya confirmado.

El hecho auditado puede originarse en otro Aggregate o contexto de
AURA.

Conceptualmente:

```text
Source Aggregate

    │
    ▼

Confirmed Domain Fact

    │
    ▼

Audit Management

    │
    ▼

Audit
```

Audit conserva una representación propia del hecho.

No modifica el hecho original.

No adquiere ownership sobre el Aggregate que produjo dicho hecho.

---

# Principio Fundamental

Audit registra hechos.

No crea retrospectivamente los hechos que audita.

Debe mantenerse:

```text
Audited Fact

=

Already Confirmed Fact
```

y nunca:

```text
Audit

↓

Creates Source Domain Fact
```

La existencia de un Audit tampoco convierte el registro auditable
en la fuente transaccional de verdad del Aggregate originador.

---

# Responsabilidades

El Aggregate Audit es responsable de:

- mantener su identidad;
- mantener la referencia al origen del hecho auditado;
- preservar la representación del hecho auditable;
- mantener información temporal asociada;
- preservar información de trazabilidad disponible;
- preservar correlación cuando corresponda;
- preservar causalidad cuando corresponda;
- proteger sus invariantes;
- mantener Version;
- mantener CreatedAt;
- mantener UpdatedAt cuando corresponda;
- mantener su propia consistencia;
- producir sus propios Domain Events cuando exista comportamiento
  de dominio explícitamente definido.

Audit es responsable exclusivamente de su propia representación.

---

# Responsabilidades Fuera del Aggregate

No es responsabilidad de Audit:

- administrar Organizations;
- administrar Citizens;
- administrar Memberships;
- administrar Roles;
- administrar Territories;
- administrar Assemblies;
- administrar Proposals;
- administrar Participations;
- administrar Votings;
- administrar Documents;
- administrar Notifications;
- administrar Integrations;
- ejecutar Authentication;
- administrar Authorization;
- modificar hechos históricos de otros Aggregates;
- corregir el estado de otros Aggregates;
- ejecutar Commands pertenecientes a otros Aggregates;
- reconstruir automáticamente el estado de otros Aggregates;
- reemplazar Domain Events;
- reemplazar Integration Events;
- reemplazar logs técnicos;
- reemplazar sistemas de Observability.

Estas responsabilidades permanecen en sus respectivos Aggregates,
Bounded Contexts o capas.

---

# Aggregate Root

La única Aggregate Root es:

```text
Audit
```

Toda modificación perteneciente al Aggregate debe ocurrir mediante
esta Aggregate Root.

Ningún consumidor externo puede modificar directamente el estado
interno de Audit.

La Aggregate Root protege:

- AuditId;
- referencias del hecho auditado;
- información de trazabilidad;
- invariantes;
- Version;
- timestamps propios;
- comportamiento oficialmente definido.

---

# Identidad

La identidad del Aggregate está determinada por:

```text
AuditId
```

AuditId:

- es único;
- identifica una unidad Audit;
- es inmutable;
- no se modifica durante la existencia del Aggregate;
- no depende del mecanismo de persistencia;
- es distinto de la identidad del hecho o Aggregate originador.

Debe mantenerse:

```text
AuditId

≠

SourceAggregateId
```

y:

```text
AuditId

≠

EventId
```

cuando el hecho auditado provenga de un evento.

---

# Origen del Hecho Auditado

Audit debe poder preservar la referencia necesaria para identificar
el origen conceptual del hecho auditado.

La referencia al origen no convierte el Aggregate externo en una
entidad interna de Audit.

Debe mantenerse:

```text
Source Reference

≠

Embedded Source Aggregate
```

El formato concreto de representación del origen debe permanecer
conforme a los contratos oficiales de AURA.

---

# Source Aggregate

Cuando el hecho auditado proviene de un Aggregate, Audit puede
conservar conceptualmente información suficiente para identificar:

```text
SourceAggregateId

SourceAggregateType
```

cuando dicha información forme parte del contrato que origina la
trazabilidad.

Audit no carga ni almacena como parte de su Consistency Boundary el
Aggregate completo de origen.

---

# Source Event

Los Domain Events constituyen una fuente natural de hechos
auditables.

Cuando un Domain Event origina información para Audit, pueden estar
disponibles conceptualmente:

```text
EventId

EventType

AggregateId

AggregateVersion

OccurredAt

CorrelationId

CausationId
```

según el contrato oficial del evento.

Audit puede mantener su propia representación de la información
requerida para trazabilidad.

Nunca modifica el Domain Event original.

---

# Domain Event y Audit

Debe mantenerse:

```text
Domain Event

≠

Audit
```

Un Domain Event pertenece al Aggregate que produjo el hecho.

Audit pertenece al Bounded Context:

```text
Audit Management
```

Ambos mantienen:

- ownership independiente;
- identidad independiente;
- consistencia independiente;
- persistencia independiente.

---

# Hecho Original

Audit representa información derivada de un hecho confirmado.

La creación, persistencia o posterior procesamiento de Audit no
altera el hecho de origen.

Debe mantenerse:

```text
Audit Failure

≠

Source Aggregate Rollback
```

y:

```text
Audit Commit

≠

Source Aggregate Commit
```

---

# Información Conceptual

Una unidad Audit puede mantener conceptualmente información
equivalente a:

```text
AuditId

SourceAggregateId

SourceAggregateType

SourceEventId

SourceEventType

SourceAggregateVersion

ActorId

OccurredAt

CorrelationId

CausationId

Version

CreatedAt

UpdatedAt
```

únicamente cuando cada elemento se encuentre disponible y sea
aplicable conforme al contrato del hecho auditado.

Esta estructura expresa conceptos de trazabilidad.

No establece tipos físicos de almacenamiento.

No autoriza a incorporar información inexistente en el hecho de
origen.

---

# Descripción de Atributos

## AuditId

Identificador único del Aggregate Audit.

Permanece inmutable.

---

## SourceAggregateId

Identifica el Aggregate que originó el hecho cuando existe un
Aggregate originador identificable.

No representa una referencia directa al objeto Aggregate.

---

## SourceAggregateType

Permite identificar conceptualmente el tipo de Aggregate originador
cuando dicha información pertenece al contrato recibido.

No concede a Audit conocimiento de la implementación interna de ese
Aggregate.

---

## SourceEventId

Identifica el Domain Event originador cuando Audit se deriva de un
evento y el EventId está disponible.

Debe mantenerse:

```text
SourceEventId

≠

AuditId
```

---

## SourceEventType

Representa el tipo del hecho de origen cuando el contrato recibido
lo proporciona.

Audit no redefine retrospectivamente el significado del evento.

---

## SourceAggregateVersion

Puede conservar la Version del Aggregate asociada al hecho
originador cuando esté disponible.

Debe mantenerse:

```text
SourceAggregateVersion

≠

Audit.Version
```

Cada Version pertenece a su respectivo Aggregate.

---

## ActorId

Puede conservar la referencia al actor asociado al hecho cuando esa
información forma parte del contrato auditable.

ActorId no implica que Audit administre:

- Citizen;
- Membership;
- Role;
- Authentication;
- Authorization.

---

## OccurredAt

Representa el momento asociado al hecho auditado cuando se encuentra
disponible en el contrato de origen.

No debe confundirse con:

```text
CreatedAt
```

de Audit.

Debe mantenerse:

```text
OccurredAt

≠

Audit.CreatedAt
```

aunque ambos valores puedan coincidir temporalmente en determinados
casos.

---

## CorrelationId

Permite preservar la correlación del flujo originador cuando se
encuentra disponible.

No representa identidad del Aggregate.

---

## CausationId

Permite preservar información causal del hecho cuando se encuentra
disponible.

No representa identidad del Aggregate.

---

## Version

Representa la evolución lógica del Aggregate Audit.

Toda modificación válida del Aggregate incrementa Version conforme
al patrón consolidado de AURA.

Version de Audit permanece independiente de cualquier Version
perteneciente al Aggregate originador.

---

## CreatedAt

Representa el momento de creación del Aggregate Audit.

Permanece inmutable durante su existencia.

---

## UpdatedAt

Representa el momento de la última modificación válida del
Aggregate cuando exista comportamiento que produzca una modificación.

Una lectura o una operación rechazada no modifica UpdatedAt.

---

# Información No Disponible

Audit no debe inventar información que no exista en el contrato
recibido.

Si un hecho no proporciona:

```text
ActorId

CorrelationId

CausationId
```

u otra referencia opcional, Audit no debe fabricar dichos valores
para completar artificialmente la trazabilidad.

Debe mantenerse:

```text
Missing Source Information

≠

Invented Audit Information
```

---

# Entidades Internas

La versión 1.0 no establece entidades internas concretas para el
Aggregate Audit.

La incorporación de una Internal Entity requerirá una necesidad
explícita de identidad local y consistencia dentro del Aggregate.

No debe inferirse una entidad interna únicamente por conveniencia
de implementación.

---

# Value Objects

Audit puede utilizar Value Objects definidos por el Shared Kernel o
por el propio dominio cuando corresponda.

Todo Value Object:

- es inmutable;
- no posee identidad independiente;
- representa un concepto del dominio;
- debe mantenerse dentro del Consistency Boundary que lo utiliza.

La versión 1.0 no establece una clasificación concreta adicional de
Value Objects específicos de Audit en este documento.

---

# Estado

Este documento no introduce estados concretos para Audit.

El Lifecycle y los estados oficiales deben definirse formalmente en:

```text
DOMAIN-012A-Lifecycle.md

DOMAIN-012B-State-Machine.md
```

No deben inferirse estados por analogía con:

- Assembly;
- Document;
- Notification;
- otros Aggregates.

Hasta su definición formal, este documento únicamente establece que
cualquier estado futuro deberá pertenecer al Aggregate Audit y
respetar sus Invariants.

---

# Lifecycle

El Lifecycle específico de Audit se define exclusivamente en:

```text
DOMAIN-012A-Lifecycle.md
```

Este documento no introduce:

```text
Draft

Active

Recorded

Archived

Deleted
```

ni ningún otro estado como parte oficial del modelo.

Las transiciones no deben inferirse desde este Aggregate document.

---

# State Machine

Las transiciones permitidas, estados terminales y restricciones
relacionadas con estado deben definirse formalmente en:

```text
DOMAIN-012B-State-Machine.md
```

Ninguna transición queda creada por el solo hecho de que Audit
mantenga información histórica.

---

# Commands

Los Commands oficiales de Audit deben definirse en:

```text
DOMAIN-012C-Commands.md
```

Este documento no introduce Commands concretos.

No deben inferirse Commands tales como:

```text
CreateAudit

RecordAudit

ArchiveAudit

DeleteAudit
```

hasta que su intención, precondiciones, efectos y relación con el
Lifecycle hayan sido definidos formalmente.

---

# Operaciones Públicas

La Aggregate Root expone únicamente comportamiento de dominio
definido oficialmente.

No se permiten setters públicos.

No se permite modificar directamente:

```text
AuditId

Version

CreatedAt
```

ni cualquier otro valor protegido por una Invariant.

Las operaciones concretas deberán corresponder a los Commands
oficiales definidos posteriormente.

---

# Domain Events

Los Domain Events propios de Audit deben definirse formalmente en:

```text
DOMAIN-012D-Domain-Events.md
```

Este documento no introduce nombres concretos de Domain Events.

Debe mantenerse:

```text
Source Domain Event

≠

Audit Domain Event
```

Un evento recibido desde otro Aggregate no se convierte
automáticamente en un Domain Event perteneciente a Audit.

---

# Invariantes

El Aggregate Audit mantiene como mínimo las siguientes reglas
conceptuales:

- AuditId debe existir;
- AuditId permanece inmutable;
- AuditId no se confunde con EventId;
- AuditId no se confunde con SourceAggregateId;
- la representación auditable pertenece exclusivamente a Audit;
- Audit no modifica el hecho original;
- Audit no modifica el Aggregate originador;
- las referencias externas no incorporan Aggregates completos;
- la información auditada no puede ser inventada cuando no existe
  en el contrato de origen;
- SourceAggregateVersion y Audit.Version representan evoluciones
  independientes;
- CreatedAt permanece inmutable;
- toda modificación válida incrementa Version;
- una operación rechazada no incrementa Version;
- las Invariants deben cumplirse antes y después de cada operación
  válida.

La definición exhaustiva se encuentra en:

```text
DOMAIN-012E-Invariants.md
```

---

# Trazabilidad

Audit existe para preservar trazabilidad de hechos relevantes.

Conceptualmente puede conservar relaciones como:

```text
Source Aggregate
     │
     ▼
Source Domain Event
     │
     ▼
Audit
```

sin fusionar sus límites de consistencia.

La trazabilidad puede utilizar:

```text
SourceAggregateId

SourceEventId

ActorId

AggregateVersion

OccurredAt

CorrelationId

CausationId
```

cuando estén disponibles conforme al contrato original.

---

# Trazabilidad Causal

CorrelationId y CausationId permiten preservar relaciones
conceptuales entre hechos distribuidos.

Debe mantenerse:

```text
CorrelationId

≠

AuditId
```

y:

```text
CausationId

≠

AuditId
```

salvo coincidencia accidental de representación, la cual no altera
su significado conceptual.

---

# Inmutabilidad del Hecho Auditado

Audit no puede modificar retrospectivamente:

- EventId del hecho originador;
- EventType del hecho originador;
- AggregateId del hecho originador;
- AggregateVersion del hecho originador;
- OccurredAt del hecho originador;
- CorrelationId del hecho originador;
- CausationId del hecho originador;
- Payload original del Domain Event.

Si Audit conserva una representación propia, dicha representación
debe preservar el significado del hecho recibido.

---

# Audit y Organization

Audit puede mantener referencias a hechos originados en
Organization.

Organization permanece fuera del Consistency Boundary.

Audit no:

- crea Organization;
- modifica Organization;
- cambia su Version;
- administra su Lifecycle.

---

# Audit y Citizen

Audit puede preservar ActorId o referencias relacionadas con Citizen
cuando el contrato auditable las proporciona.

Citizen permanece fuera del Aggregate.

Audit no administra:

- identidad cívica;
- estado de Citizen;
- Lifecycle de Citizen.

---

# Audit y Membership

Hechos pertenecientes a Membership pueden ser auditables.

Audit no modifica:

- MembershipStatus;
- relaciones de pertenencia;
- Lifecycle;
- Version.

---

# Audit y Role

Hechos relacionados con Role pueden producir información auditable.

Audit no administra:

- definición de Roles;
- asignación de Roles;
- jerarquías;
- permisos.

---

# Audit y Territory

Territory puede producir hechos auditables.

Audit conserva únicamente referencias necesarias conforme al
contrato recibido.

Territory permanece fuera del Consistency Boundary.

---

# Audit y Assembly

Los Domain Events de Assembly pueden proporcionar hechos relevantes
para trazabilidad.

Conceptualmente:

```text
Assembly

    │
    ▼

Assembly Domain Event

    │
    ▼

Audit Management

    │
    ▼

Audit
```

Audit mantiene su propio Aggregate.

No modifica Assembly.

---

# Audit y Proposal

Los hechos de Proposal pueden ser auditables.

Audit no administra:

- ProposalStatus;
- Proposal Lifecycle;
- Proposal.Version.

Proposal mantiene su propio Consistency Boundary.

---

# Audit y Participation

Participation puede producir hechos relevantes para trazabilidad.

Audit no modifica Participation.

Debe mantenerse:

```text
Participation Transaction

≠

Audit Transaction
```

---

# Audit y Voting

Los hechos confirmados de Voting pueden aportar información
auditable.

Audit no:

- registra votos;
- modifica votos;
- abre Voting;
- cierra Voting;
- modifica resultados;
- modifica VotingStatus.

---

# Audit y Document

Document puede producir hechos auditables.

Audit no modifica:

```text
DocumentStatus

Document.Version

Document Content

Document Lifecycle
```

La relación permanece mediante contratos o identificadores
aplicables.

---

# Audit y Notification

Notification puede producir hechos relevantes para trazabilidad.

Audit no modifica:

```text
NotificationStatus

Notification.Version

Notification Lifecycle
```

Debe mantenerse:

```text
Notification Domain Event

≠

Audit Record
```

---

# Audit e Integration

Integration permanece fuera del Aggregate Audit.

Audit puede participar posteriormente en contratos de integración
cuando exista una necesidad explícita.

Debe mantenerse:

```text
Audit Domain Event

≠

Integration Event
```

y:

```text
Audit

≠

Integration Infrastructure
```

---

# Relaciones

Audit mantiene relaciones con otros Aggregates mediante
identificadores, hechos y contratos.

Conceptualmente:

```text
Audit
    │
    ├──────── Organization
    ├──────── Citizen
    ├──────── Membership
    ├──────── Role
    ├──────── Territory
    ├──────── Assembly
    ├──────── Proposal
    ├──────── Participation
    ├──────── Voting
    ├──────── Document
    ├──────── Notification
    └──────── Integration
```

Estas relaciones no convierten a los Aggregates relacionados en
entidades internas de Audit.

---

# Consistency Boundary

Audit constituye su propia unidad de consistencia.

Debe mantenerse:

```text
Audit Transaction

≠

Source Aggregate Transaction
```

La creación o modificación válida de Audit no requiere una
modificación atómica del Aggregate originador.

La relación entre ambos límites utiliza consistencia eventual cuando
corresponda.

La definición formal se encuentra en:

```text
DOMAIN-012J-Consistency-Boundary.md
```

---

# Consistencia

Dentro de Audit, toda modificación válida debe dejar el Aggregate
internamente consistente.

No debe existir un resultado confirmado con:

- AuditId inválido;
- referencias inconsistentes;
- Version incompatible;
- modificación parcial;
- invariantes incumplidas.

Entre Audit y el Aggregate originador puede existir una ventana
temporal de consistencia eventual.

---

# Independencia Transaccional

Un hecho puede haber sido confirmado en su Aggregate originador
antes de que Audit lo haya procesado.

Conceptualmente:

```text
Source Aggregate

Confirmed Fact
      │
      ▼

Temporal Window
      │
      ▼

Audit Processing
```

Esta separación es coherente con los límites DDD de AURA.

El retraso de Audit no revierte el hecho originador.

---

# Versionado

Audit mantiene su propia:

```text
Version
```

Toda modificación válida incrementa Version.

Toda operación rechazada conserva Version.

La Version de Audit nunca debe utilizarse como sustituto de:

```text
SourceAggregateVersion
```

La definición formal se encuentra en:

```text
DOMAIN-012I-Versioning.md
```

---

# Repository

Audit dispone de un Repository Contract propio.

El Repository:

- persiste Audit como unidad;
- recupera Audit;
- preserva su Version;
- protege su consistencia de persistencia;
- abstrae la tecnología utilizada.

El Repository no:

- crea hechos auditables por decisión propia;
- modifica el Aggregate originador;
- corrige Invariants;
- ejecuta Commands;
- inventa Domain Events.

La definición formal se encuentra en:

```text
DOMAIN-012G-Repository-Contract.md
```

---

# Persistencia

Audit debe persistirse como una unidad de consistencia.

La persistencia física pertenece a Infrastructure.

El Aggregate no conoce:

```text
SQL

MongoDB

PostgreSQL

EventStoreDB

ORM

HTTP

File System
```

ni ninguna tecnología equivalente.

---

# Optimistic Concurrency

Audit es compatible con:

```text
Optimistic Concurrency Control
```

Version permite detectar modificaciones concurrentes
incompatibles conforme al patrón consolidado de AURA.

La estrategia completa se define en:

```text
DOMAIN-012I-Versioning.md
```

---

# Fuente de Verdad

Audit es autoridad únicamente sobre su propio estado.

No es autoridad sobre:

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
```

Debe mantenerse:

```text
Audit

=

Source of Truth for Audit Aggregate State
```

pero:

```text
Audit

≠

Source of Truth for Source Aggregate State
```

---

# Read Models

Audit puede disponer de Read Models especializados para consulta.

Los Read Models pueden facilitar:

- trazabilidad;
- consulta histórica;
- consulta por origen;
- consulta por actor cuando exista ActorId;
- consulta temporal;
- consulta por correlación;
- consulta por causalidad.

Las consultas concretas deberán formalizarse en:

```text
DOMAIN-012L-Read-Model.md
```

Los Read Models:

- son proyecciones;
- no son Aggregates;
- no modifican Audit;
- no modifican el Aggregate originador;
- no constituyen autoridad de escritura.

---

# Consultas

Las necesidades de búsqueda, filtrado, orden, paginación,
reporting o análisis pertenecen al Read Side.

No deben expandir innecesariamente el Aggregate.

Debe mantenerse:

```text
Audit Aggregate

≠

Audit Query Engine
```

---

# Audit y Domain Events de Otros Aggregates

Los Domain Events pueden proporcionar una fuente natural de hechos
auditables.

Audit puede reaccionar a hechos provenientes de:

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
```

cuando exista el contrato correspondiente.

Cada Domain Event continúa perteneciendo al Aggregate que lo
originó.

---

# Ingesta de Hechos

La recepción técnica de un mensaje no constituye por sí sola una
regla del Aggregate.

Debe mantenerse:

```text
Message Received

≠

Automatically Valid Audit Fact
```

La capa correspondiente debe presentar al dominio únicamente la
información conforme a contratos válidos.

La tecnología utilizada para transportar hechos permanece fuera de
Audit.

---

# Integration Events

Los hechos propios de Audit podrán transformarse en Integration
Events únicamente cuando exista un contrato explícito de
integración.

No existe una correspondencia automática:

```text
Audit Domain Event

=

Integration Event
```

Debe mantenerse:

```text
Domain Event

≠

Mandatory Integration Event
```

La definición formal se encuentra en:

```text
DOMAIN-012K-Integration-Events.md
```

---

# Audit e Integration Events de Origen

Un Integration Event recibido desde otro Bounded Context tampoco se
convierte automáticamente en estado de Audit.

Debe existir un contrato reconocido que permita interpretar el hecho
como auditable.

Audit no depende del formato técnico utilizado para transportarlo.

---

# Correlación

Audit puede preservar:

```text
CorrelationId
```

cuando este valor esté disponible.

CorrelationId permite relacionar hechos pertenecientes a un mismo
flujo sin fusionar los Aggregates involucrados.

Debe mantenerse:

```text
Correlated Aggregates

≠

Shared Consistency Boundary
```

---

# Causalidad

Audit puede preservar:

```text
CausationId
```

cuando forme parte del hecho recibido.

CausationId permite expresar relaciones de causa entre hechos o
mensajes sin introducir acoplamiento directo entre los Aggregates.

---

# Actor

Cuando un hecho auditado identifica al actor responsable o
participante, Audit puede preservar:

```text
ActorId
```

según el contrato recibido.

Audit no autentica al Actor.

Audit no autoriza al Actor.

Audit no administra su identidad.

---

# Authentication

Authentication permanece fuera del Aggregate.

Audit no:

- valida credenciales;
- valida passwords;
- valida tokens;
- crea sesiones;
- administra OAuth;
- administra JWT;
- administra proveedores de identidad.

---

# Authorization

Authorization permanece separada del Aggregate.

Los Commands que se definan para Audit deberán estar sujetos a las
Permissions correspondientes.

Una autorización válida nunca permite evitar:

- Invariants;
- Versioning;
- State Machine cuando sea definida;
- Consistency Boundary.

La definición formal pertenece a:

```text
DOMAIN-012F-Permissions.md
```

---

# Seguridad

Audit no debe almacenar:

- passwords;
- access tokens;
- refresh tokens;
- API keys;
- private keys;
- secretos técnicos;
- credenciales de proveedores;
- configuración sensible de Infrastructure.

Debe aplicarse minimización de información conforme a los contratos
y políticas aplicables.

La definición formal se encuentra en:

```text
DOMAIN-012O-Security-Model.md
```

---

# Información Sensible

La existencia de información en un Domain Event de origen no
significa que Audit deba copiarla íntegramente.

Debe mantenerse:

```text
Source Event Payload

≠

Automatic Audit Payload
```

Audit debe conservar únicamente la información necesaria conforme a
sus reglas y contratos.

---

# Logs

Audit no equivale a logging técnico.

Debe mantenerse:

```text
Audit

≠

Application Log
```

y:

```text
Audit

≠

Infrastructure Log
```

Los logs pueden contener información operacional.

Audit representa conceptos auditables del dominio.

---

# Observability

Audit no reemplaza:

- logs;
- metrics;
- traces;
- monitoring;
- alerting.

Debe mantenerse:

```text
Audit

≠

Observability
```

Observability pertenece a responsabilidades técnicas externas.

---

# Historial

Audit existe para preservar trazabilidad.

La información histórica confirmada no debe reescribirse
arbitrariamente para representar un hecho diferente del originalmente
auditado.

Debe mantenerse:

```text
Historical Audit Fact

≠

Mutable Operational Data
```

Las reglas exhaustivas sobre modificación y Lifecycle se definirán
en los artefactos correspondientes.

---

# Eliminación

Este documento no define eliminación física como comportamiento
ordinario del Aggregate.

Tampoco introduce:

```text
Deleted
```

como estado.

Las reglas futuras relativas a:

- retención;
- eliminación;
- anonimización;
- conservación histórica;

deberán definirse explícitamente antes de formar parte del dominio.

No deben inferirse desde la naturaleza histórica de Audit.

---

# Retención

La versión 1.0 no establece:

- período de retención;
- plazo mínimo;
- plazo máximo;
- expiración automática;
- eliminación programada;
- política de archivo.

Estas reglas requieren definición explícita del dominio y de las
políticas aplicables.

---

# Consistencia Eventual

Audit puede procesar hechos de otros Aggregates mediante
consistencia eventual.

Conceptualmente:

```text
Source Aggregate

    │
    ▼

Confirmed Fact

    │
    ▼

Eventual Propagation

    │
    ▼

Audit
```

El Source Aggregate no espera a Audit para confirmar su propia
transacción.

Audit no revierte la transacción de origen si su procesamiento
posterior falla.

---

# Procesamiento Idempotente

Los mecanismos que entregan hechos a Audit pueden presentar el mismo
hecho más de una vez.

La estrategia concreta de idempotencia pertenece a las capas
correspondientes.

El dominio debe preservar el principio:

```text
Duplicate Technical Delivery

≠

New Source Domain Fact
```

La identidad original del hecho debe conservarse cuando el contrato
la proporcione.

---

# Rendimiento

Audit debe mantener un Consistency Boundary pequeño.

No debe cargar otros Aggregates completos para registrar o consultar
una unidad Audit.

Las consultas históricas complejas deben resolverse mediante Read
Models.

Debe mantenerse:

```text
Audit Aggregate

≠

Historical Analytics Engine
```

La definición formal se encuentra en:

```text
DOMAIN-012N-Performance-Rules.md
```

---

# Escalabilidad

Diferentes unidades Audit mantienen identidades y límites de
consistencia independientes.

El procesamiento masivo de hechos auditables no convierte todas las
unidades Audit en un único Aggregate.

Debe mantenerse:

```text
Audit A

≠

Audit B
```

como unidades independientes cuando representan identidades Audit
distintas.

---

# CQRS

Audit es compatible con CQRS.

En el lado de escritura:

```text
Command

    │
    ▼

Audit Aggregate

    │
    ├── Invariants
    ├── Version
    └── Domain Events
```

conforme a los Commands y Domain Events que se definan
oficialmente.

En el lado de lectura:

```text
Confirmed Facts

    │
    ▼

Projection

    │
    ▼

Audit Read Model
```

El Read Model no reemplaza al Aggregate.

---

# Event Sourcing

Audit es compatible conceptualmente con Event Sourcing.

Esta compatibilidad no obliga a utilizar Event Sourcing.

Los Domain Events propios de Audit, una vez definidos, podrán
representar su evolución histórica.

Debe mantenerse:

```text
Source Aggregate Events

≠

Audit Event Stream
```

Los eventos pertenecientes a otros Aggregates no se convierten
automáticamente en el historial autoritativo interno de Audit.

La estrategia concreta de persistencia pertenece a Infrastructure.

---

# Rehidratación

La reconstrucción de Audit debe preservar:

- AuditId;
- Version;
- información confirmada;
- invariantes;
- significado histórico.

La rehidratación no ejecuta nuevos Commands ni crea nuevos hechos
por el solo acto de reconstruir el Aggregate.

---

# Integration

Audit puede integrarse con otros Bounded Contexts y sistemas
externos mediante contratos explícitos.

La integración no accede directamente al estado mutable interno del
Aggregate.

Debe mantenerse:

```text
Audit

↓

Domain Event

↓

Integration Boundary

↓

Integration Event
```

cuando exista un contrato explícito que requiera dicha
transformación.

---

# FIWARE

Audit no depende directamente de:

```text
FIWARE

NGSI-LD

Context Broker

Orion
```

Una eventual proyección o integración con FIWARE pertenece a
Integration e Infrastructure.

Debe mantenerse:

```text
Audit Domain Model

≠

FIWARE Data Model
```

---

# Sistemas Municipales

Audit puede participar en integraciones con plataformas municipales
mediante contratos explícitos.

Audit no depende de:

- APIs municipales;
- protocolos municipales;
- mecanismos de autenticación municipales;
- estructuras propietarias externas.

La transformación entre modelos pertenece a la frontera de
integración.

---

# Anti-Corruption Layer

Cuando un sistema externo utilice una semántica diferente, su
información no debe incorporarse automáticamente al lenguaje ubicuo
de Audit.

La traducción debe realizarse en la frontera correspondiente.

Debe mantenerse:

```text
External Audit Representation

≠

AURA Audit Domain Model
```

salvo equivalencia conceptual explícitamente establecida.

---

# Dependencias

Audit depende conceptualmente de:

- Shared Kernel;
- Value Objects;
- Domain Events;
- Repository Contracts;
- identificadores;
- contratos de dominio definidos por AURA.

Audit no depende directamente de:

```text
Infrastructure

Frameworks

Bases de datos

ORM

HTTP

REST

GraphQL

OAuth

JWT

React

Next.js

FastAPI

Django

FIWARE SDK

MongoDB

PostgreSQL
```

Las implementaciones tecnológicas pertenecen a capas externas.

---

# Compatibilidad Arquitectónica

Audit está diseñado para cumplir:

- Domain-Driven Design;
- Aggregate Pattern;
- Clean Architecture;
- Hexagonal Architecture;
- SOLID;
- Event-Driven Architecture;
- CQRS;
- Event Sourcing Compatible;
- Optimistic Concurrency Control;
- High Cohesion;
- Low Coupling;
- Persistence Ignorance;
- Separation of Concerns.

El Aggregate pertenece al dominio y permanece independiente de
tecnologías de Infrastructure.

---

# Reglas de Diseño del Aggregate

Audit debe cumplir:

- una única Aggregate Root;
- identidad propia mediante AuditId;
- AuditId inmutable;
- invariantes protegidas internamente;
- ausencia de setters públicos;
- referencias externas mediante identificadores y contratos;
- ausencia de acceso directo a otros Aggregates;
- ausencia de modificación directa del Aggregate originador;
- separación entre Domain Event y Audit;
- separación entre Audit e Integration Event;
- Version independiente;
- Repository propio;
- consistencia transaccional propia;
- consistencia eventual con otros Aggregates;
- independencia tecnológica;
- trazabilidad sin ownership sobre el origen.

---

# Límites del Aggregate

El límite de Audit incluye conceptualmente:

```text
Audit

AuditId

Source References

Audit Traceability Information

Version

CreatedAt

UpdatedAt

Value Objects propios

Internal Entities propias
```

únicamente cuando dichos elementos hayan sido definidos
oficialmente.

El límite no incluye:

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

Estos pertenecen a otros Aggregates o contextos.

---

# Ownership

Audit posee exclusivamente el estado necesario para representar su
propia unidad auditable.

No posee:

- el Aggregate originador;
- el Domain Event original;
- la identidad del Actor;
- la Authorization del Actor;
- Read Models externos;
- Integration;
- Infrastructure.

Puede preservar referencias e información necesaria conforme a los
contratos recibidos.

---

# Separación Source Event / Audit

Debe mantenerse:

```text
Source Domain Event
    │
    │ belongs to
    ▼
Source Aggregate
```

separado de:

```text
Audit
    │
    │ belongs to
    ▼
Audit Management
```

Audit puede conservar una representación propia.

No modifica, reemplaza ni reasigna ownership del Domain Event
original.

---

# Separación Audit / Notification

Notification comunica.

Audit preserva trazabilidad.

Debe mantenerse:

```text
Notification

≠

Audit
```

Una Notification puede generar hechos auditables.

Audit no entrega Notifications.

---

# Separación Audit / Document

Document administra documentos con identidad y Lifecycle propios.

Audit preserva trazabilidad.

Debe mantenerse:

```text
Audit

≠

Document Archive
```

Audit no debe convertirse en almacenamiento documental por el solo
hecho de conservar información histórica.

---

# Separación Audit / Integration

Audit representa dominio.

Integration representa contratos y mecanismos de comunicación entre
límites.

Debe mantenerse:

```text
Audit

≠

Integration
```

---

# Separación Audit / Logs

Los logs describen información operacional o técnica.

Audit describe hechos auditables conforme al dominio.

Debe mantenerse:

```text
Technical Log Entry

≠

Audit
```

No todo log es un hecho de dominio auditable.

No todo hecho auditable debe representarse mediante un log.

---

# Separación Audit / Read Model

Audit constituye el Write Model cuando exista comportamiento propio
de escritura.

Las vistas históricas y consultas pertenecen al Read Side.

Debe mantenerse:

```text
Audit Aggregate

≠

Audit Read Model
```

---

# Extension Points

Audit puede evolucionar sin modificar innecesariamente su núcleo.

Los puntos de extensión podrán incluir conceptualmente:

```text
Traceability Information

Source Contracts

Audit Policies

Domain Events

Integration Events

Read Models
```

cuando dichas capacidades sean formalmente definidas.

Una extensión no puede:

- modificar retrospectivamente AuditId;
- alterar el hecho original;
- incorporar Aggregates externos como entidades internas;
- introducir dependencias de Infrastructure;
- convertir logs técnicos en dominio automáticamente;
- crear nuevos estados sin definir Lifecycle;
- crear Commands o Domain Events sin definición explícita.

La especificación completa se encuentra en:

```text
DOMAIN-012P-Extension-Points.md
```

---

# Evolución Controlada

La definición de:

- Lifecycle;
- State Machine;
- Commands;
- Domain Events;
- Permissions;
- reglas completas de Invariants;
- políticas de retención;
- políticas de eliminación;
- Read Models;
- Integration Events;

deberá realizarse en sus artefactos correspondientes.

Este documento no anticipa esas decisiones.

Debe mantenerse:

```text
Aggregate Definition

≠

Permission to Infer Undefined Domain Rules
```

---

# Definición de Éxito

El Aggregate **Audit** proporciona una unidad de dominio
independiente para preservar trazabilidad de hechos relevantes
dentro del ecosistema AURA.

El modelo garantiza que:

- Audit posee identidad propia mediante AuditId;
- AuditId permanece inmutable;
- Audit mantiene su propio Consistency Boundary;
- Audit mantiene Version independiente;
- los hechos auditados ya han ocurrido;
- Domain Event y Audit permanecen conceptos distintos;
- Audit puede conservar una representación propia de hechos
  auditables;
- el Domain Event original no es modificado;
- el Aggregate originador no es modificado por Audit;
- SourceAggregateVersion y Audit.Version permanecen independientes;
- ActorId, CorrelationId y CausationId solamente se conservan cuando
  están disponibles conforme al contrato;
- Audit no inventa información faltante;
- otros Aggregates permanecen fuera del Consistency Boundary;
- Audit no reemplaza Authentication ni Authorization;
- Audit no almacena credenciales ni secretos técnicos;
- Audit no equivale a logging;
- Audit no equivale a Observability;
- Audit no equivale a Document;
- Audit no equivale a Notification;
- Audit no equivale a Integration;
- Read Models permanecen separados del Write Model;
- Repository persiste Audit como una unidad independiente;
- la relación con otros Aggregates puede mantener consistencia
  eventual;
- un fallo posterior de Audit no revierte el hecho originador;
- CQRS permanece compatible;
- Event Sourcing permanece compatible sin quedar impuesto;
- FIWARE y sistemas municipales permanecen fuera del Aggregate;
- Infrastructure no determina el modelo de dominio;
- no se introducen estados, Commands, Domain Events, políticas de
  retención o eliminación sin definición explícita.

De esta forma, `DOMAIN-012-Aggregate.md` establece la definición
oficial del Aggregate **Audit** conforme al patrón consolidado de
AURA Core.