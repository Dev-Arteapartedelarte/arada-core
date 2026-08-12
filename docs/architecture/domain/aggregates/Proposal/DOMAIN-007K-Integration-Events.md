# DOMAIN-007K — Proposal Integration Events

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
- CORE-003-Shared-Kernel.md
- CORE-004-Ubiquitous-Language.md
- CORE-005-Domain-Events.md
- CORE-006-Domain-Invariants.md
- CORE-007-Strategic-Design.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Definir los Integration Events oficiales asociados al Aggregate
**Proposal**.

Los Integration Events representan hechos relevantes del dominio
de Proposal que pueden ser comunicados fuera de su Bounded
Context para permitir interoperabilidad con otros Bounded
Contexts, servicios, plataformas o sistemas externos.

Un Integration Event no representa una intención.

Representa información derivada de un hecho que ya ocurrió y fue
confirmado dentro del Aggregate Proposal.

Los Integration Events permiten que Proposal participe en una
arquitectura distribuida sin exponer su estado interno, sin
compartir su Aggregate Root y sin ampliar su límite de
consistencia.

---

# Propósito

Los Integration Events permiten:

- comunicar hechos relevantes de Proposal fuera de su Bounded
  Context;
- desacoplar Proposal de consumidores externos;
- preservar el límite de consistencia del Aggregate;
- permitir integración entre Bounded Contexts;
- permitir interoperabilidad con sistemas externos;
- mantener independencia tecnológica del dominio;
- evitar dependencias directas entre Aggregates;
- permitir procesamiento asíncrono;
- soportar consistencia eventual;
- mantener trazabilidad entre hechos internos y comunicaciones
  externas;
- evolucionar contratos de integración de forma controlada.

Los Integration Events constituyen contratos de interoperabilidad.

No constituyen el modelo interno de Proposal.

---

# Principio Fundamental

Un Integration Event puede originarse como consecuencia de un
Domain Event confirmado.

Conceptualmente:

```text
Proposal Aggregate

↓

Domain Event

↓

Committed Domain State

↓

Integration Mapping

↓

Integration Event

↓

External Consumer
```

La publicación externa ocurre después de que el hecho del dominio
ha sido aceptado y confirmado.

Un Integration Event nunca debe utilizarse para modificar
directamente el estado interno de Proposal.

---

# Domain Event vs Integration Event

Un Domain Event pertenece al dominio interno del Bounded Context.

Un Integration Event constituye un contrato destinado a cruzar
sus límites.

Conceptualmente:

```text
Domain Event
```

representa:

```text
Internal Domain Fact
```

mientras:

```text
Integration Event
```

representa:

```text
External Integration Contract
```

Ambos pueden describir un mismo hecho desde responsabilidades
diferentes.

---

# Separación de Responsabilidades

Debe mantenerse:

```text
Domain Event

≠

Integration Event
```

Un Domain Event:

- pertenece al modelo de dominio;
- utiliza el lenguaje ubicuo interno;
- puede contener información necesaria para procesos internos;
- evoluciona según las necesidades del dominio.

Un Integration Event:

- cruza límites de Bounded Context;
- constituye un contrato de interoperabilidad;
- expone únicamente información necesaria;
- debe poseer versionado explícito;
- debe evolucionar de forma compatible;
- no expone implementación interna del Aggregate.

---

# Regla de Confirmación

Un Integration Event solo puede representar un hecho confirmado.

No debe publicarse un Integration Event definitivo antes de que
la modificación correspondiente de Proposal haya sido aceptada y
persistida correctamente.

Debe mantenerse:

```text
Validate

↓

Modify Proposal

↓

Persist

↓

Commit

↓

Publish Integration Event
```

No:

```text
Publish Integration Event

↓

Attempt Commit
```

Esta regla evita comunicar externamente hechos que finalmente no
formaron parte del estado válido del dominio.

---

# Regla de No Publicación ante Rechazo

Si un Command es rechazado:

```text
Command

↓

Rejected
```

entonces:

```text
No State Change

No Domain Fact

No Integration Event
```

Una operación inválida no puede producir un Integration Event que
represente un hecho inexistente.

---

# Fuente de los Integration Events

Los Integration Events se derivan de hechos confirmados del
dominio.

La fuente conceptual es:

```text
Proposal Aggregate

↓

Domain Events
```

Los Domain Events oficiales se encuentran definidos en:

```text
DOMAIN-007D-Domain-Events.md
```

El mecanismo de integración transforma únicamente aquellos hechos
que deban ser comunicados fuera del Bounded Context.

No todos los Domain Events deben producir necesariamente un
Integration Event.

---

# Regla de Selección

La existencia de un Domain Event no obliga automáticamente a
publicarlo externamente.

Debe mantenerse:

```text
Domain Event

↓

Integration Relevance Evaluation

↓

Integration Event
```

o:

```text
Domain Event

↓

No External Publication
```

La decisión depende de si el hecho posee relevancia para otros
Bounded Contexts o consumidores externos.

---

# Eventos de Integración Conceptuales

Los Integration Events conceptuales de Proposal incluyen:

```text
ProposalCreatedForIntegration

ProposalSubmittedForIntegration

ProposalReviewStartedForIntegration

ProposalAcceptedForIntegration

ProposalRejectedForIntegration

ProposalWithdrawnForIntegration

ProposalArchivedForIntegration

ProposalUpdatedForIntegration
```

Estos nombres representan contratos conceptuales de integración.

No reemplazan los Domain Events internos.

---

# ProposalCreatedForIntegration

## Objetivo

Comunicar que una Proposal ha sido creada correctamente y existe
como unidad formal del dominio.

## Origen conceptual

```text
ProposalCreated
```

## Condición

El evento solo puede publicarse después de que la nueva Proposal
haya sido confirmada.

## Información conceptual

```text
EventId

EventType

EventVersion

OccurredAt

PublishedAt

ProposalId

OrganizationId

ProposerReference

TerritoryId

AssemblyId

ProposalType

ProposalStatus

ProposalVersion

CorrelationId

CausationId
```

Los campos opcionales se incluyen únicamente cuando correspondan
al contexto real de Proposal.

## Consumidores posibles

- Participation;
- Assembly;
- Notification;
- Audit;
- Integration;
- plataformas municipales;
- sistemas de participación ciudadana;
- servicios de interoperabilidad.

---

# ProposalSubmittedForIntegration

## Objetivo

Comunicar que una Proposal fue formalmente presentada.

## Origen conceptual

```text
ProposalSubmitted
```

## Condición

Proposal debe haber completado correctamente la transición de
dominio correspondiente a presentación.

## Información conceptual

```text
EventId

EventType

EventVersion

OccurredAt

PublishedAt

ProposalId

OrganizationId

ProposerReference

TerritoryId

AssemblyId

ProposalType

ProposalStatus

SubmittedAt

ProposalVersion

CorrelationId

CausationId
```

## Consumidores posibles

- procesos de revisión;
- Notification;
- Audit;
- sistemas municipales;
- plataformas de participación;
- sistemas analíticos;
- Integration.

---

# ProposalReviewStartedForIntegration

## Objetivo

Comunicar que una Proposal ingresó formalmente al proceso de
revisión definido por el dominio.

## Origen conceptual

```text
ProposalReviewStarted
```

## Condición

La transición hacia el estado de revisión debe haber sido
confirmada.

## Información conceptual

```text
EventId

EventType

EventVersion

OccurredAt

PublishedAt

ProposalId

OrganizationId

ProposalStatus

ReviewedAt

ProposalVersion

CorrelationId

CausationId
```

## Consumidores posibles

- Notification;
- Audit;
- sistemas de seguimiento;
- plataformas municipales;
- servicios de interoperabilidad.

---

# ProposalAcceptedForIntegration

## Objetivo

Comunicar que una Proposal fue aceptada conforme a las reglas del
dominio.

## Origen conceptual

```text
ProposalAccepted
```

## Condición

La aceptación debe encontrarse confirmada dentro del Aggregate.

## Información conceptual

```text
EventId

EventType

EventVersion

OccurredAt

PublishedAt

ProposalId

OrganizationId

TerritoryId

AssemblyId

ProposalType

ProposalStatus

AcceptedAt

ProposalVersion

CorrelationId

CausationId
```

## Consumidores posibles

- Participation;
- Voting;
- Assembly;
- Notification;
- Audit;
- Integration;
- sistemas municipales;
- plataformas de participación ciudadana;
- servicios analíticos.

La recepción de este evento no obliga automáticamente a otro
Aggregate a modificar su estado.

Cada consumidor aplica sus propias reglas.

---

# ProposalRejectedForIntegration

## Objetivo

Comunicar que una Proposal fue rechazada.

## Origen conceptual

```text
ProposalRejected
```

## Condición

El rechazo debe encontrarse confirmado dentro del Aggregate.

## Información conceptual

```text
EventId

EventType

EventVersion

OccurredAt

PublishedAt

ProposalId

OrganizationId

ProposalStatus

RejectedAt

ProposalVersion

CorrelationId

CausationId
```

## Consumidores posibles

- Notification;
- Audit;
- sistemas de seguimiento;
- plataformas municipales;
- sistemas analíticos;
- Integration.

El evento comunica el hecho de rechazo.

No expone necesariamente información interna adicional que no sea
requerida por el contrato de integración.

---

# ProposalWithdrawnForIntegration

## Objetivo

Comunicar que una Proposal fue retirada conforme a una transición
válida del dominio.

## Origen conceptual

```text
ProposalWithdrawn
```

## Condición

La retirada debe haber sido confirmada por Proposal.

## Información conceptual

```text
EventId

EventType

EventVersion

OccurredAt

PublishedAt

ProposalId

OrganizationId

ProposalStatus

WithdrawnAt

ProposalVersion

CorrelationId

CausationId
```

## Consumidores posibles

- Notification;
- Audit;
- Assembly;
- sistemas de seguimiento;
- plataformas de participación;
- Integration.

---

# ProposalArchivedForIntegration

## Objetivo

Comunicar que una Proposal alcanzó el estado Archived.

## Origen conceptual

```text
ProposalArchived
```

## Condición

La transición a Archived debe haber sido confirmada.

## Información conceptual

```text
EventId

EventType

EventVersion

OccurredAt

PublishedAt

ProposalId

OrganizationId

ProposalStatus

ArchivedAt

ProposalVersion

CorrelationId

CausationId
```

## Consumidores posibles

- Audit;
- sistemas documentales;
- plataformas municipales;
- servicios analíticos;
- sistemas de archivo;
- Integration.

---

# ProposalUpdatedForIntegration

## Objetivo

Comunicar una modificación relevante de Proposal cuando dicha
modificación deba ser conocida fuera del Bounded Context.

## Origen conceptual

Puede derivarse de Domain Events relacionados con cambios
permitidos sobre información propia de Proposal.

## Condición

La modificación debe:

- haber sido validada;
- respetar el estado actual;
- preservar las invariantes;
- encontrarse persistida;
- haber generado una nueva Version válida;
- poseer relevancia externa.

## Información conceptual

```text
EventId

EventType

EventVersion

OccurredAt

PublishedAt

ProposalId

OrganizationId

ChangedFields

ProposalStatus

ProposalVersion

CorrelationId

CausationId
```

El evento no debe utilizarse como reemplazo indiscriminado de
eventos semánticamente específicos.

Cuando exista un hecho de dominio con significado propio, debe
preferirse su correspondiente contrato de integración.

---

# Envelope de Integración

Todo Integration Event debe poseer una envoltura conceptual
estable.

Como mínimo:

```text
EventId

EventType

EventVersion

OccurredAt

PublishedAt

AggregateType

AggregateId

AggregateVersion

CorrelationId

CausationId

Payload
```

Para Proposal:

```text
AggregateType = Proposal

AggregateId = ProposalId

AggregateVersion = ProposalVersion
```

El Envelope permite transportar metadatos de integración sin
contaminar el modelo interno del Aggregate.

---

# EventId

Cada Integration Event posee:

```text
EventId
```

EventId:

- identifica de forma única la publicación lógica del evento;
- permite detectar duplicados;
- permite trazabilidad;
- no sustituye ProposalId;
- no constituye identidad del Aggregate.

Debe mantenerse:

```text
EventId

≠

ProposalId
```

---

# EventType

EventType identifica el tipo contractual del evento.

Ejemplos:

```text
ProposalSubmittedForIntegration

ProposalAcceptedForIntegration

ProposalArchivedForIntegration
```

EventType debe ser estable dentro de una versión contractual.

---

# EventVersion

Cada Integration Event posee una versión explícita:

```text
EventVersion
```

Ejemplo conceptual:

```text
1
```

La versión corresponde al contrato del evento.

No corresponde a la versión del Aggregate.

Debe mantenerse:

```text
EventVersion

≠

ProposalVersion
```

---

# ProposalVersion

ProposalVersion representa la revisión del Aggregate que produjo
el hecho comunicado.

Conceptualmente:

```text
ProposalVersion
```

permite al consumidor conocer la revisión del Aggregate asociada
al evento.

No debe utilizarse como versión del contrato de integración.

---

# OccurredAt

OccurredAt representa el instante conceptual en que ocurrió el
hecho del dominio.

```text
OccurredAt
```

pertenece al significado temporal del hecho comunicado.

No necesariamente coincide con PublishedAt.

---

# PublishedAt

PublishedAt representa el instante en que el Integration Event
fue publicado hacia el mecanismo de integración.

Debe mantenerse:

```text
OccurredAt

≤

PublishedAt
```

Puede existir una diferencia temporal entre ambos valores.

---

# AggregateType

El Envelope identifica el tipo de Aggregate que originó el hecho.

Para este documento:

```text
AggregateType = Proposal
```

Este valor permite identificar el origen conceptual sin exponer
la implementación interna.

---

# AggregateId

El identificador del Aggregate originador es:

```text
ProposalId
```

El Envelope puede representarlo conceptualmente como:

```text
AggregateId
```

manteniendo ProposalId como identidad oficial del dominio.

---

# CorrelationId

CorrelationId permite relacionar múltiples operaciones y eventos
que forman parte de un mismo flujo lógico.

Conceptualmente:

```text
Command

↓

Domain Event

↓

Integration Event
```

pueden compartir:

```text
CorrelationId
```

Esto permite reconstruir trazabilidad distribuida sin fusionar
los límites de consistencia.

---

# CausationId

CausationId identifica la causa inmediata que originó el evento.

Puede referenciar conceptualmente:

- CommandId;
- DomainEventId;
- otro evento relacionado.

Debe permitir distinguir:

```text
Correlation
```

de:

```text
Causation
```

---

# Payload

Payload contiene exclusivamente la información necesaria para el
contrato específico.

No debe contener automáticamente todo el estado de Proposal.

Debe mantenerse:

```text
Minimum Required Integration Data
```

en lugar de:

```text
Complete Aggregate Serialization
```

---

# Regla de Información Mínima

Los Integration Events deben exponer únicamente la información
necesaria para que el consumidor comprenda y procese el hecho.

No deben utilizarse como mecanismo para replicar indiscriminadamente
el Aggregate completo.

Debe mantenerse:

```text
Integration Contract

≠

Aggregate Serialization
```

---

# Regla de No Exposición del Aggregate

No está permitido publicar:

```text
Proposal Aggregate
```

como Payload completo de un Integration Event.

El evento debe transportar una representación contractual.

Conceptualmente:

```text
Proposal

↓

Integration Mapping

↓

Integration DTO / Event Payload
```

No:

```text
Proposal Object

↓

External Consumer
```

---

# Información Interna

Los detalles internos que no sean necesarios para integración no
deben exponerse.

Esto incluye:

- estructuras internas;
- objetos de infraestructura;
- referencias ORM;
- datos técnicos de persistencia;
- estado transitorio interno;
- información de seguridad;
- secretos;
- credenciales;
- detalles tecnológicos.

---

# Datos Sensibles

Los Integration Events deben evitar transportar información
sensible que no sea necesaria para el consumidor.

En particular, no deben incluir por defecto:

- credenciales;
- tokens;
- JWT;
- secretos;
- claves privadas;
- información técnica de autenticación;
- datos personales innecesarios.

Cuando una referencia sea suficiente, debe preferirse:

```text
CitizenId
```

o:

```text
MembershipId
```

en lugar de replicar información completa perteneciente a otros
Aggregates.

---

# ProposerReference

Cuando el contrato requiera identificar al proponente, debe
utilizarse una referencia de dominio compatible con el modelo de
Proposal.

Conceptualmente puede corresponder a:

```text
CitizenId
```

o:

```text
MembershipId
```

según las reglas establecidas por Proposal.

El Integration Event no debe incluir automáticamente el Aggregate
Citizen o Membership completo.

---

# Referencias Externas

Los Integration Events pueden incluir identificadores como:

```text
OrganizationId

CitizenId

MembershipId

TerritoryId

AssemblyId

ProposalId
```

cuando sean necesarios para establecer contexto.

Estas referencias no transfieren propiedad de los Aggregates
referenciados.

---

# Regla de Independencia

Un consumidor de Integration Events no debe depender del estado
interno de Proposal.

Debe depender únicamente del contrato publicado.

Conceptualmente:

```text
Consumer

↓

Integration Contract
```

No:

```text
Consumer

↓

Proposal Internal Model
```

Esta separación permite que Proposal evolucione internamente sin
romper innecesariamente consumidores externos.

---

# Regla de Desacoplamiento

Proposal no conoce a los consumidores concretos de sus
Integration Events.

Debe mantenerse:

```text
Proposal

↓

Integration Event
```

y no:

```text
Proposal

↓

Specific Consumer
```

El Aggregate no contiene lógica específica para:

- plataformas municipales;
- FIWARE;
- servicios de Notification;
- motores analíticos;
- bases de datos externas;
- aplicaciones móviles;
- sistemas Smart City.

---

# Publicación

La publicación de Integration Events pertenece a la coordinación
externa al Aggregate.

Proposal produce hechos de dominio.

La infraestructura o capa correspondiente transforma y publica
los contratos de integración.

Conceptualmente:

```text
Proposal

↓

Domain Event

↓

Application / Integration Layer

↓

Integration Event

↓

Transport
```

Proposal no publica directamente en:

- message brokers;
- HTTP;
- MQTT;
- AMQP;
- Kafka;
- RabbitMQ;
- FIWARE;
- servicios externos.

---

# Consistencia Transaccional

La modificación de Proposal y la comunicación externa pertenecen
a responsabilidades diferentes.

El Aggregate garantiza:

```text
Proposal Internal Consistency
```

El mecanismo de integración debe garantizar que un hecho
confirmado pueda ser publicado de forma confiable sin ampliar el
Consistency Boundary del Aggregate.

No debe modificarse el modelo conceptual de Proposal para
convertir sistemas externos en participantes de su transacción.

---

# Consistencia Eventual

Los Integration Events operan bajo:

```text
Eventually Consistent
```

Puede existir un intervalo entre:

```text
Proposal Commit

↓

Integration Event Publication

↓

Consumer Processing
```

Durante ese intervalo, el estado interno de Proposal continúa
siendo válido y autoritativo.

---

# Regla de No Rollback Externo

Una falla posterior en un consumidor no revierte automáticamente
el estado confirmado de Proposal.

Ejemplo:

```text
ProposalSubmitted

↓

Proposal Commit

↓

ProposalSubmittedForIntegration

↓

Notification Consumer Failure
```

El resultado no debe ser:

```text
ProposalStatus = Draft
```

por el solo hecho de que Notification haya fallado.

El consumidor administra su propia recuperación.

---

# Entrega Repetida

En una arquitectura distribuida puede producirse más de una
entrega del mismo Integration Event.

Por ello, EventId debe permitir identificar la publicación lógica
del evento.

Conceptualmente:

```text
Same EventId

↓

Duplicate Delivery
```

no significa:

```text
New Domain Fact
```

---

# Idempotencia del Consumidor

Los consumidores deben poder reconocer que múltiples entregas del
mismo EventId representan el mismo hecho de integración.

Conceptualmente:

```text
Receive EventId X

↓

Process
```

y posteriormente:

```text
Receive EventId X

↓

Already Processed
```

La entrega duplicada no debe interpretarse automáticamente como
un nuevo hecho del dominio.

---

# Orden de Eventos

ProposalVersion puede utilizarse como referencia para comprender
la secuencia lógica de revisiones del mismo Aggregate.

Ejemplo:

```text
ProposalVersion 3

↓

ProposalVersion 4

↓

ProposalVersion 5
```

Esto no implica que el transporte distribuido garantice por sí
solo el mismo orden de recepción.

Los consumidores no deben inferir consistencia interna de Proposal
exclusivamente desde el orden físico de llegada.

---

# Eventos Fuera de Orden

Un consumidor puede recibir conceptualmente:

```text
ProposalVersion 8
```

antes de:

```text
ProposalVersion 7
```

dependiendo del mecanismo de integración.

ProposalVersion permite detectar esta condición.

La estrategia concreta de procesamiento pertenece al consumidor y
a la infraestructura correspondiente.

---

# Reprocesamiento

Un Integration Event puede requerir reprocesamiento cuando un
consumidor no pudo procesarlo correctamente.

El reprocesamiento:

- no crea un nuevo hecho del dominio;
- no modifica Proposal;
- no incrementa ProposalVersion;
- no genera por sí mismo un nuevo Domain Event;
- mantiene el EventId cuando representa la misma publicación
  lógica.

---

# Trazabilidad

Los Integration Events deben permitir reconstruir la relación
entre:

```text
Command

↓

Domain Event

↓

Proposal Version

↓

Integration Event

↓

External Processing
```

Los identificadores conceptuales utilizados para ello incluyen:

```text
CommandId

DomainEventId

EventId

ProposalId

ProposalVersion

CorrelationId

CausationId

OccurredAt

PublishedAt
```

cuando correspondan.

---

# Auditoría

Audit puede consumir Integration Events de Proposal cuando estos
sean relevantes para procesos de trazabilidad externa.

Audit permanece fuera del Aggregate Proposal.

Debe mantenerse:

```text
Proposal Integration Event

↓

Audit
```

No:

```text
Audit

inside

Proposal
```

---

# Notification

Notification puede reaccionar ante Integration Events relevantes.

Ejemplo:

```text
ProposalSubmittedForIntegration

↓

Notification
```

o:

```text
ProposalAcceptedForIntegration

↓

Notification
```

Proposal no administra:

- canales;
- plantillas;
- destinatarios técnicos;
- reintentos;
- entrega;
- confirmación de lectura.

Estas responsabilidades permanecen fuera del Aggregate.

---

# Assembly

Assembly puede consumir información relacionada con Proposal
cuando exista una relación de dominio válida.

Ejemplo conceptual:

```text
ProposalAcceptedForIntegration

↓

Assembly-related Process
```

Esto no permite que Proposal modifique Assembly directamente.

Assembly conserva su propio Consistency Boundary.

---

# Participation

Participation puede utilizar eventos de integración de Proposal
para contextualizar procesos de participación.

Conceptualmente:

```text
Proposal

↓

Integration Event

↓

Participation
```

Participation aplica sus propias reglas e invariantes.

Proposal no controla su Lifecycle.

---

# Voting

Voting puede reaccionar a un hecho de Proposal cuando el proceso
de negocio correspondiente lo requiera.

Ejemplo conceptual:

```text
ProposalAcceptedForIntegration

↓

Voting Process
```

El evento no crea automáticamente una Voting dentro de Proposal.

Voting mantiene:

- identidad propia;
- Lifecycle propio;
- State Machine propia;
- invariantes propias;
- Repository propio;
- Version propia.

---

# Document

Document puede relacionarse con Proposal mediante identificadores
o eventos.

Los Integration Events no deben transportar el Aggregate Document
completo.

Cuando corresponda, puede utilizarse:

```text
DocumentId
```

como referencia.

Document permanece fuera del límite de Proposal.

---

# Sistemas Municipales

Los Integration Events permiten comunicar hechos relevantes de
Proposal a plataformas municipales sin introducir dependencias
municipales dentro del Aggregate.

Conceptualmente:

```text
Proposal

↓

Integration Event

↓

Municipal Integration Adapter

↓

Municipal System
```

Proposal no conoce:

- endpoints municipales;
- formatos propietarios;
- credenciales;
- mecanismos de autenticación;
- protocolos específicos.

---

# Smart City

Los Integration Events pueden permitir que hechos de Proposal sean
consumidos por ecosistemas Smart City.

Debe mantenerse:

```text
Proposal Domain Model

↓

Integration Contract

↓

Smart City Adapter
```

La arquitectura Smart City no redefine Proposal.

---

# FIWARE

La interoperabilidad con FIWARE puede realizarse a partir de
Integration Events.

Conceptualmente:

```text
Proposal

↓

Domain Event

↓

Integration Event

↓

FIWARE Adapter

↓

NGSI-LD Representation
```

Proposal no depende de:

```text
NGSI-LD

Context Broker

FIWARE APIs

FIWARE Authentication
```

Estas responsabilidades pertenecen a integración e
infraestructura.

---

# NGSI-LD

Una entidad NGSI-LD derivada de Proposal constituye una
representación externa.

Debe mantenerse:

```text
Proposal Aggregate

≠

NGSI-LD Entity
```

La representación NGSI-LD puede proyectar información publicada
mediante Integration Events.

No constituye la fuente de verdad interna del Aggregate Proposal.

---

# APIs

Los Integration Events son independientes de APIs HTTP.

Un mismo contrato conceptual puede ser transportado mediante
distintos mecanismos de infraestructura.

Proposal no conoce:

```text
REST

HTTP

Webhooks

Message Brokers
```

La elección del transporte no modifica el significado del evento.

---

# Message Brokers

La utilización de un message broker constituye una decisión de
infraestructura.

Conceptualmente:

```text
Integration Event
```

permanece independiente de:

```text
Kafka

RabbitMQ

NATS

MQTT

AMQP
```

El contrato de dominio no debe depender de un proveedor
específico.

---

# Serialización

La representación serializada de un Integration Event pertenece a
la capa de integración.

Puede utilizar formatos como:

```text
JSON

JSON-LD
```

u otros formatos compatibles con los consumidores.

El formato físico no redefine el significado conceptual del
evento.

---

# Contrato Conceptual

Un Integration Event debe mantener una estructura semántica
estable.

Ejemplo conceptual:

```text
ProposalAcceptedForIntegration

EventId

EventVersion

OccurredAt

PublishedAt

ProposalId

OrganizationId

ProposalStatus

AcceptedAt

ProposalVersion

CorrelationId

CausationId
```

La representación técnica puede variar sin alterar el significado
del contrato.

---

# Versionado de Contratos

Los Integration Events evolucionan mediante:

```text
EventVersion
```

Una modificación compatible puede mantener la misma versión cuando
no altera el significado contractual existente.

Una modificación incompatible requiere una nueva versión del
contrato.

Debe evitarse que cambios internos de Proposal produzcan
automáticamente cambios incompatibles en consumidores externos.

---

# Compatibilidad hacia Atrás

La evolución de un Integration Event debe preservar compatibilidad
cuando sea posible.

Ejemplos conceptuales de cambios potencialmente compatibles:

- agregar información opcional;
- agregar metadatos no obligatorios;
- extender el Payload sin cambiar el significado existente.

Los consumidores existentes no deben requerir cambios cuando el
contrato continúa siendo semánticamente compatible.

---

# Cambios Incompatibles

Cambios que alteren el significado contractual pueden requerir una
nueva EventVersion.

Ejemplos conceptuales:

- eliminar un campo obligatorio;
- cambiar el significado de un campo;
- cambiar el tipo conceptual de un valor;
- cambiar una semántica de estado;
- reutilizar un nombre existente para representar otro hecho.

No debe reutilizarse una versión contractual para representar una
semántica incompatible.

---

# Inmutabilidad

Un Integration Event publicado es inmutable.

Después de su publicación no debe modificarse.

Si posteriormente ocurre un nuevo hecho, debe producirse un nuevo
evento.

Debe mantenerse:

```text
Published Event

=

Immutable Fact Representation
```

---

# Eventos Correctivos

Si un hecho posterior modifica una situación previamente
comunicada, debe publicarse el evento correspondiente al nuevo
hecho.

No debe editarse retroactivamente un Integration Event ya
publicado.

Ejemplo:

```text
ProposalSubmittedForIntegration
```

seguido posteriormente por:

```text
ProposalWithdrawnForIntegration
```

representa dos hechos diferentes.

---

# Relación con Commands

Los Commands representan intención.

Los Integration Events representan hechos comunicables.

Debe mantenerse:

```text
Command

≠

Integration Event
```

Ejemplo:

```text
SubmitProposal
```

es una intención.

```text
ProposalSubmittedForIntegration
```

representa la comunicación de un hecho confirmado.

---

# Relación con Domain Events

La relación conceptual puede representarse como:

```text
SubmitProposal

↓

Proposal Aggregate

↓

ProposalSubmitted

↓

Commit

↓

ProposalSubmittedForIntegration
```

Cada elemento posee una responsabilidad distinta.

---

# Relación con Versioning

ProposalVersion incluida en un Integration Event debe corresponder
a la revisión del Aggregate asociada al hecho.

Las reglas internas de versionado se encuentran en:

```text
DOMAIN-007I-Versioning.md
```

EventVersion continúa siendo independiente de ProposalVersion.

---

# Relación con Consistency Boundary

Los Integration Events se encuentran fuera del límite interno de
consistencia de Proposal.

El límite oficial se encuentra definido en:

```text
DOMAIN-007J-Consistency-Boundary.md
```

Debe mantenerse:

```text
Proposal Consistency Boundary

↓

Committed Domain Fact

↓

Integration Event
```

La comunicación externa no amplía la frontera transaccional.

---

# Relación con Read Models

Los Integration Events pueden alimentar proyecciones externas.

Los Read Models internos pueden derivarse directamente de Domain
Events según el modelo CQRS correspondiente.

Debe mantenerse:

```text
Integration Event

≠

Read Model
```

El Read Model se desarrolla en:

```text
DOMAIN-007L-Read-Model.md
```

---

# Relación con Security Model

Los Integration Events deben respetar las reglas de seguridad y
exposición definidas para Proposal.

No deben convertirse en un mecanismo para eludir controles de
información.

Las reglas correspondientes se desarrollarán en:

```text
DOMAIN-007O-Security-Model.md
```

---

# Relación con Performance Rules

Las decisiones de rendimiento no pueden alterar el significado de
los Integration Events.

Optimizar:

- serialización;
- transporte;
- particionamiento;
- almacenamiento temporal;
- distribución;
- consumo;

no autoriza a eliminar semántica necesaria del contrato.

Las reglas correspondientes se desarrollarán en:

```text
DOMAIN-007N-Performance-Rules.md
```

---

# Flujo General

```text
Command
    │
    ▼
Proposal Aggregate
    │
    ├── Validate State
    │
    ├── Validate Invariants
    │
    ├── Execute Behavior
    │
    ├── Increment Version
    │
    └── Produce Domain Event
    │
    ▼
Repository
    │
    ▼
Commit
    │
    ▼
Confirmed Domain Event
    │
    ▼
Integration Mapping
    │
    ▼
Integration Event
    │
    ▼
External Consumers
```

---

# Flujo de ProposalSubmitted

```text
SubmitProposal
        │
        ▼
Proposal
        │
        ▼
ProposalSubmitted
        │
        ▼
Commit
        │
        ▼
ProposalSubmittedForIntegration
        │
        ├────────► Notification
        │
        ├────────► Audit
        │
        ├────────► Municipal Systems
        │
        ├────────► Participation Systems
        │
        └────────► Integration
```

---

# Flujo de ProposalAccepted

```text
AcceptProposal
        │
        ▼
Proposal
        │
        ▼
ProposalAccepted
        │
        ▼
Commit
        │
        ▼
ProposalAcceptedForIntegration
        │
        ├────────► Voting
        │
        ├────────► Assembly
        │
        ├────────► Notification
        │
        ├────────► Audit
        │
        ├────────► Municipal Systems
        │
        └────────► Integration
```

Cada consumidor mantiene su propio límite de consistencia.

---

# Escenario — Creación

```text
CreateProposal

↓

ProposalCreated

↓

Proposal Persisted

↓

Commit

↓

ProposalCreatedForIntegration
```

El evento comunica que Proposal existe formalmente.

No comunica una intención de creación.

---

# Escenario — Presentación

```text
Proposal = Draft

↓

SubmitProposal

↓

Proposal = Submitted

↓

ProposalSubmitted

↓

Commit

↓

ProposalSubmittedForIntegration
```

El Integration Event solo existe después de la confirmación del
nuevo estado.

---

# Escenario — Aceptación

```text
Proposal = UnderReview

↓

AcceptProposal

↓

Proposal = Accepted

↓

ProposalAccepted

↓

Commit

↓

ProposalAcceptedForIntegration
```

Los consumidores pueden reaccionar al hecho.

Ningún consumidor forma parte del Aggregate Proposal.

---

# Escenario — Rechazo

```text
Proposal = UnderReview

↓

RejectProposal

↓

Proposal = Rejected

↓

ProposalRejected

↓

Commit

↓

ProposalRejectedForIntegration
```

La comunicación externa refleja el estado confirmado.

---

# Escenario — Retiro

```text
WithdrawProposal

↓

ProposalWithdrawn

↓

Commit

↓

ProposalWithdrawnForIntegration
```

El evento no modifica otros Aggregates.

---

# Escenario — Archivado

```text
ArchiveProposal

↓

ProposalArchived

↓

Commit

↓

ProposalArchivedForIntegration
```

Los consumidores pueden actualizar sus propias proyecciones o
procesos conforme a sus reglas.

---

# Escenario — Command Rechazado

```text
Invalid Command

↓

Proposal Rejects Operation

↓

No State Change

↓

No Commit

↓

No Integration Event
```

No existe hecho externo que comunicar.

---

# Escenario — Fallo de Publicación

Conceptualmente puede ocurrir:

```text
Proposal Commit

↓

Integration Publication Failure
```

El fallo de publicación no invalida automáticamente el estado
interno ya confirmado de Proposal.

La recuperación pertenece al mecanismo de integración.

Proposal no modifica su Lifecycle debido exclusivamente a un fallo
del transporte externo.

---

# Escenario — Entrega Duplicada

```text
ProposalAcceptedForIntegration
EventId = E-100
```

puede ser recibido más de una vez:

```text
Consumer receives E-100

↓

Consumer receives E-100 again
```

Ambas entregas representan el mismo hecho.

---

# Escenario — Eventos Fuera de Orden

Un consumidor puede observar:

```text
ProposalVersion = 12
```

antes de:

```text
ProposalVersion = 11
```

El consumidor debe poder identificar las revisiones.

No debe interpretarse el orden físico de recepción como autoridad
sobre la secuencia interna del Aggregate.

---

# Escenario — Consumidor No Disponible

```text
ProposalSubmittedForIntegration

↓

Consumer unavailable
```

Proposal continúa en su estado confirmado.

El consumidor o mecanismo de integración debe recuperar el
procesamiento posteriormente según sus propias reglas.

---

# Escenario — Sistema Municipal

```text
ProposalAcceptedForIntegration

↓

Municipal Integration Adapter

↓

Municipal Platform
```

La adaptación de formato ocurre fuera del Aggregate.

Proposal no contiene lógica municipal específica.

---

# Escenario — FIWARE

```text
ProposalAcceptedForIntegration

↓

FIWARE Integration Adapter

↓

NGSI-LD Mapping

↓

Context Broker
```

La representación NGSI-LD es externa.

Proposal permanece independiente de FIWARE.

---

# Escenario — Read Projection Externa

```text
ProposalSubmittedForIntegration

↓

External Projection

↓

Proposal External View
```

La proyección puede ser eventualmente consistente.

No constituye la fuente oficial de verdad del Aggregate.

---

# Restricciones

No está permitido:

- publicar Integration Events antes del Commit correspondiente;
- publicar hechos derivados de Commands rechazados;
- utilizar Integration Events como Commands;
- utilizar Integration Events para modificar directamente
  Proposal;
- exponer el Aggregate Proposal completo como Payload;
- exponer objetos internos de dominio;
- exponer estructuras ORM;
- exponer detalles de persistencia;
- incluir credenciales;
- incluir tokens;
- incluir secretos;
- incluir información personal innecesaria;
- acoplar Proposal a consumidores concretos;
- introducir lógica FIWARE dentro de Proposal;
- introducir lógica municipal dentro de Proposal;
- introducir protocolos de transporte dentro del Aggregate;
- utilizar EventVersion como ProposalVersion;
- utilizar ProposalVersion como EventVersion;
- modificar un Integration Event después de publicado;
- interpretar una entrega duplicada como un nuevo hecho;
- asumir que el transporte garantiza siempre el orden del
  dominio;
- ampliar el Consistency Boundary mediante Integration Events;
- utilizar un Integration Event como serialización completa del
  estado interno.

---

# Invariantes de Integración

Los Integration Events mantienen como mínimo las siguientes
reglas conceptuales:

- todo Integration Event representa un hecho confirmado;
- un Command rechazado no produce Integration Event;
- un Integration Event publicado es inmutable;
- EventId identifica la publicación lógica;
- EventVersion identifica la versión contractual;
- ProposalVersion identifica la revisión del Aggregate;
- EventVersion y ProposalVersion son conceptos diferentes;
- ProposalId identifica el Aggregate originador;
- OccurredAt representa el momento del hecho;
- PublishedAt representa el momento de publicación;
- PublishedAt no precede conceptualmente al hecho comunicado;
- CorrelationId permite trazabilidad de flujo;
- CausationId permite identificar causalidad;
- el Payload contiene únicamente información necesaria;
- otros Aggregates se representan mediante referencias cuando
  corresponda;
- el Aggregate completo no se expone;
- los consumidores permanecen desacoplados;
- la publicación externa no amplía el Consistency Boundary;
- una falla externa no revierte automáticamente Proposal;
- la integración opera mediante consistencia eventual;
- los contratos pueden evolucionar mediante versionado explícito.

---

# Matriz Domain Event / Integration Event

```text
Domain Event                    Integration Event

ProposalCreated                 ProposalCreatedForIntegration

ProposalSubmitted               ProposalSubmittedForIntegration

ProposalReviewStarted           ProposalReviewStartedForIntegration

ProposalAccepted                ProposalAcceptedForIntegration

ProposalRejected                ProposalRejectedForIntegration

ProposalWithdrawn               ProposalWithdrawnForIntegration

ProposalArchived                ProposalArchivedForIntegration

Relevant Proposal Changes       ProposalUpdatedForIntegration
```

La existencia de esta correspondencia conceptual no obliga a
publicar externamente todos los Domain Events en todos los
escenarios.

---

# Matriz de Responsabilidades

```text
Responsabilidad                         Proposal   Integration

Proteger invariantes                    Sí         No

Modificar Proposal                      Sí         No

Controlar Lifecycle                     Sí         No

Controlar State Machine                 Sí         No

Incrementar ProposalVersion             Sí         No

Generar Domain Events                   Sí         No

Mapear contratos externos               No         Sí

Publicar Integration Events             No         Sí

Adaptar formatos externos               No         Sí

Comunicar con FIWARE                    No         Sí

Comunicar con sistemas municipales      No         Sí

Gestionar transporte                    No         Sí

Gestionar serialización                 No         Sí

Gestionar reintentos externos           No         Sí
```

---

# Matriz de Identificadores

```text
Identificador       Propósito

ProposalId          Identidad del Aggregate

ProposalVersion     Revisión del Aggregate

EventId             Identidad lógica del Integration Event

EventVersion        Versión del contrato

CorrelationId       Relación entre operaciones del mismo flujo

CausationId         Causa inmediata del evento
```

Cada identificador posee una responsabilidad distinta.

No deben utilizarse como conceptos intercambiables.

---

# Compatibilidad Arquitectónica

Los Integration Events de Proposal son compatibles con:

- Domain-Driven Design;
- Clean Architecture;
- Hexagonal Architecture;
- CQRS;
- Event Sourcing;
- Event-Driven Architecture;
- SOLID;
- consistencia eventual;
- arquitectura distribuida;
- interoperabilidad basada en contratos;
- integración con sistemas municipales;
- integración con ecosistemas Smart City;
- integración mediante adaptadores;
- FIWARE mediante capa de integración;
- NGSI-LD mediante representación externa.

---

# Principios Arquitectónicos

Los Integration Events mantienen:

```text
Domain Fact

≠

External Contract
```

```text
Domain Event

≠

Integration Event
```

```text
Command

≠

Integration Event
```

```text
Proposal Aggregate

≠

Integration Payload
```

```text
EventId

≠

ProposalId
```

```text
EventVersion

≠

ProposalVersion
```

```text
OccurredAt

≠

PublishedAt
```

```text
Integration Relationship

≠

Aggregate Membership
```

```text
External Consumer

≠

Proposal Dependency
```

```text
Integration Failure

≠

Automatic Proposal Rollback
```

```text
Duplicate Delivery

≠

New Domain Fact
```

```text
Transport Order

≠

Domain Authority
```

```text
NGSI-LD Representation

≠

Proposal Aggregate
```

```text
Infrastructure

≠

Domain Model
```

---

# Documentación Complementaria

Los Integration Events deben interpretarse conjuntamente con:

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

DOMAIN-007L-Read-Model.md

DOMAIN-007M-Test-Scenarios.md

DOMAIN-007N-Performance-Rules.md

DOMAIN-007O-Security-Model.md

DOMAIN-007P-Extension-Points.md
```

Estos documentos desarrollan responsabilidades específicas del
Aggregate sin alterar la separación entre el modelo interno de
Proposal y sus contratos externos de interoperabilidad.

---

# Definición de Éxito

Los Integration Events del Aggregate **Proposal** constituyen los
contratos oficiales mediante los cuales hechos relevantes de
Proposal pueden ser comunicados fuera de su Bounded Context.

Cada Integration Event representa un hecho previamente confirmado
por el dominio y mantiene separación explícita respecto de:

```text
Commands

Domain Events

Proposal Aggregate

Read Models

Infrastructure

External Systems
```

Los eventos exponen únicamente la información necesaria para la
interoperabilidad y mantienen identificadores explícitos para:

```text
Event Identity

Contract Version

Proposal Identity

Proposal Revision

Correlation

Causation

Temporal Traceability
```

La comunicación externa ocurre sin ampliar el Consistency
Boundary de Proposal y sin introducir referencias mutables,
dependencias tecnológicas o transacciones distribuidas dentro del
Aggregate.

Los consumidores pueden reaccionar a estos contratos manteniendo
sus propios:

```text
Consistency Boundaries

Lifecycles

State Machines

Invariants

Repositories

Versions
```

Una falla de transporte o de un consumidor externo no modifica
automáticamente un hecho ya confirmado dentro de Proposal.

De esta forma, los Integration Events permiten que Proposal
participe de manera desacoplada, trazable y evolutiva en la
arquitectura distribuida de AURA Core, preservando la autonomía
del dominio y proporcionando una base estable para la
interoperabilidad con otros Bounded Contexts, plataformas
municipales, ecosistemas Smart City y mecanismos externos de
integración.