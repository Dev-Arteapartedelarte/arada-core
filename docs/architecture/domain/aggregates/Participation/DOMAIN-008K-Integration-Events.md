# DOMAIN-008K — Participation Integration Events

Versión: 1.0

Estado:
Oficial

Proyecto:
AURA Core

Bounded Context:
Participation Management

Aggregate:
Participation

Autor:
ARADA

Documentos Relacionados:

- DOMAIN-008-Aggregate.md
- DOMAIN-008D-Domain-Events.md
- DOMAIN-008G-Repository-Contract.md
- DOMAIN-008I-Versioning.md
- DOMAIN-008J-Consistency-Boundary.md
- CORE-005-Domain-Events.md
- CORE-011-Repository-Contracts.md
- CORE-016-Dependency-Rules.md

---

# Objetivo

Definir los Integration Events oficiales emitidos a partir
de cambios relevantes del Aggregate Participation.

Los Integration Events permiten:

- comunicar hechos del dominio hacia otros Bounded
  Contexts;
- desacoplar Participation de consumidores externos;
- propagar cambios confirmados;
- mantener consistencia eventual entre contextos;
- soportar integraciones confiables;
- preservar trazabilidad entre Domain Events e
  Integration Events.

---

# Principios

Los Integration Events deben cumplir las siguientes reglas.

- representan hechos ya confirmados;
- se originan a partir de cambios válidos del dominio;
- son inmutables;
- no contienen lógica de negocio;
- no modifican directamente el Aggregate;
- pueden ser consumidos por múltiples Bounded Contexts;
- forman parte de los contratos de integración de AURA
  Core;
- deben permitir identificar el Aggregate que originó el
  evento.

---

# Concepto

Un Integration Event representa un hecho del dominio que
puede ser comunicado fuera del Bounded Context
Participation Management.

Flujo conceptual.

```text
Command

↓

Participation Aggregate

↓

Domain Event

↓

Commit

↓

Integration Event

↓

External Consumer
```

El Integration Event no reemplaza al Domain Event.

Ambos poseen responsabilidades diferentes.

---

# Domain Event

El Domain Event representa un hecho ocurrido dentro del
Bounded Context.

Ejemplo.

```text
ParticipationActivated
```

Su propósito principal es expresar un cambio relevante
dentro del dominio de Participation.

---

# Integration Event

El Integration Event representa el contrato utilizado para
comunicar ese hecho fuera del Bounded Context.

Ejemplo.

```text
ParticipationActivatedIntegrationEvent
```

El Integration Event puede ser consumido por otros
componentes o Bounded Contexts sin acceder directamente al
Aggregate.

---

# Separación entre Domain Events e Integration Events

Debe mantenerse la separación:

```text
Domain Event

↓

Internal Domain Meaning
```

```text
Integration Event

↓

External Integration Contract
```

Un Domain Event no debe utilizarse directamente como
contrato externo.

---

# Eventos Oficiales

Los Integration Events de Participation corresponden a
hechos relevantes producidos por el Aggregate.

```text
ParticipationRegisteredIntegrationEvent

ParticipationActivatedIntegrationEvent

ParticipationCompletedIntegrationEvent

ParticipationWithdrawnIntegrationEvent

ParticipationInvalidatedIntegrationEvent

ParticipationArchivedIntegrationEvent

ParticipationTypeChangedIntegrationEvent

ParticipationContextChangedIntegrationEvent

ParticipationMetadataUpdatedIntegrationEvent
```

Cada Integration Event deriva del Domain Event
correspondiente definido en:

```text
DOMAIN-008D-Domain-Events.md
```

---

# ParticipationRegisteredIntegrationEvent

Se publica cuando una Participation ha sido registrada
correctamente.

Origen.

```text
ParticipationRegistered
```

Representación conceptual.

```text
ParticipationRegisteredIntegrationEvent

ParticipationId

OrganizationId

ParticipationType

Context

AggregateVersion

OccurredAt
```

Permite informar que una nueva Participation existe dentro
del dominio.

---

# ParticipationActivatedIntegrationEvent

Se publica cuando una Participation ha sido activada
correctamente.

Origen.

```text
ParticipationActivated
```

Representación conceptual.

```text
ParticipationActivatedIntegrationEvent

ParticipationId

OrganizationId

AggregateVersion

OccurredAt
```

Permite informar que la Participation ha ingresado al
estado activo definido por su Lifecycle.

---

# ParticipationCompletedIntegrationEvent

Se publica cuando una Participation ha sido completada
correctamente.

Origen.

```text
ParticipationCompleted
```

Representación conceptual.

```text
ParticipationCompletedIntegrationEvent

ParticipationId

OrganizationId

AggregateVersion

OccurredAt
```

Permite comunicar la finalización válida de una
Participation.

---

# ParticipationWithdrawnIntegrationEvent

Se publica cuando una Participation ha sido retirada
correctamente.

Origen.

```text
ParticipationWithdrawn
```

Representación conceptual.

```text
ParticipationWithdrawnIntegrationEvent

ParticipationId

OrganizationId

AggregateVersion

OccurredAt
```

Permite comunicar que la Participation fue retirada de
acuerdo con las reglas del dominio.

---

# ParticipationInvalidatedIntegrationEvent

Se publica cuando una Participation ha sido invalidada.

Origen.

```text
ParticipationInvalidated
```

Representación conceptual.

```text
ParticipationInvalidatedIntegrationEvent

ParticipationId

OrganizationId

AggregateVersion

OccurredAt
```

Permite comunicar que la Participation dejó de ser válida
según las reglas establecidas por el Aggregate.

---

# ParticipationArchivedIntegrationEvent

Se publica cuando una Participation ha sido archivada.

Origen.

```text
ParticipationArchived
```

Representación conceptual.

```text
ParticipationArchivedIntegrationEvent

ParticipationId

OrganizationId

AggregateVersion

OccurredAt
```

Permite informar que la Participation alcanzó su estado
archivado.

---

# ParticipationTypeChangedIntegrationEvent

Se publica cuando el tipo de Participation ha sido
modificado válidamente.

Origen.

```text
ParticipationTypeChanged
```

Representación conceptual.

```text
ParticipationTypeChangedIntegrationEvent

ParticipationId

OrganizationId

ParticipationType

AggregateVersion

OccurredAt
```

Permite comunicar el nuevo tipo de Participation.

---

# ParticipationContextChangedIntegrationEvent

Se publica cuando el contexto de Participation ha sido
modificado válidamente.

Origen.

```text
ParticipationContextChanged
```

Representación conceptual.

```text
ParticipationContextChangedIntegrationEvent

ParticipationId

OrganizationId

Context

AggregateVersion

OccurredAt
```

Permite comunicar el nuevo contexto asociado a la
Participation.

---

# ParticipationMetadataUpdatedIntegrationEvent

Se publica cuando la Metadata de Participation ha sido
modificada válidamente.

Origen.

```text
ParticipationMetadataUpdated
```

Representación conceptual.

```text
ParticipationMetadataUpdatedIntegrationEvent

ParticipationId

OrganizationId

AggregateVersion

OccurredAt
```

La Metadata completa no necesita formar parte del contrato
si no es requerida por los consumidores.

---

# Identidad del Evento

Cada Integration Event debe poder identificarse de forma
única.

Representación conceptual.

```text
EventId
```

Esto permite soportar:

- trazabilidad;
- detección de duplicados;
- procesamiento idempotente;
- diagnóstico de integraciones.

---

# Identidad del Aggregate

Todo Integration Event debe identificar el Aggregate que
originó el hecho.

```text
AggregateId:
ParticipationId
```

Esto permite relacionar el evento con una Participation
específica.

---

# Tipo de Aggregate

El contrato puede identificar el tipo del Aggregate.

```text
AggregateType:
Participation
```

Esto permite interpretar correctamente el origen del
evento dentro del ecosistema AURA.

---

# AggregateVersion

Todo Integration Event debe incluir la versión del
Aggregate que originó el hecho.

Ejemplo.

```text
AggregateVersion:
12
```

La versión corresponde a la definida en:

```text
DOMAIN-008I-Versioning.md
```

Esto permite:

- preservar orden lógico;
- detectar eventos fuera de secuencia;
- facilitar trazabilidad;
- correlacionar eventos con revisiones del Aggregate.

---

# OccurredAt

Todo Integration Event debe indicar cuándo ocurrió el
hecho original.

```text
OccurredAt
```

Este valor corresponde temporalmente al hecho del dominio
que originó el Integration Event.

No representa necesariamente el momento de publicación.

---

# CorrelationId

Cuando una operación forma parte de un flujo distribuido,
el Integration Event puede conservar:

```text
CorrelationId
```

Esto permite relacionar múltiples eventos pertenecientes a
una misma interacción lógica.

---

# CausationId

Cuando corresponda, el Integration Event puede conservar:

```text
CausationId
```

Esto permite identificar el evento o comando que produjo
el hecho comunicado.

---

# Estructura Conceptual

Un Integration Event mantiene conceptualmente:

```text
IntegrationEvent

EventId

EventType

AggregateId

AggregateType

AggregateVersion

OccurredAt

CorrelationId

CausationId

Payload
```

El Payload contiene únicamente la información necesaria
para representar el hecho publicado.

---

# Inmutabilidad

Una vez creado, un Integration Event no puede modificarse.

```text
Integration Event

↓

Published

↓

Immutable
```

Si el dominio cambia posteriormente, debe generarse un
nuevo evento correspondiente al nuevo hecho.

---

# Publicación

Los Integration Events representan únicamente cambios ya
confirmados.

No deben publicarse antes de que la modificación del
Aggregate haya sido persistida correctamente.

Flujo.

```text
Participation

↓

Valid Domain Change

↓

Domain Event

↓

Persist Aggregate

↓

Commit

↓

Integration Event
```

---

# Relación con Outbox

La publicación confiable utiliza el mecanismo de Outbox
consolidado por AURA.

```text
Participation

↓

Domain Event

↓

Commit

↓

Outbox Record

↓

Integration Event

↓

Message Broker
```

El Outbox permite desacoplar la confirmación del Aggregate
de la publicación externa.

---

# Atomicidad con Outbox

El cambio del Aggregate y el registro destinado a
publicación deben mantener coherencia.

Conceptualmente.

```text
Aggregate State

+

Aggregate Version

+

Outbox Record
```

representan la modificación confirmada que posteriormente
será comunicada.

---

# Fallo de Publicación

Un fallo en la publicación no modifica nuevamente el
Aggregate.

```text
Aggregate Commit

↓

Outbox Record

↓

Publication Failure

↓

Retry
```

El evento puede volver a intentarse sin ejecutar
nuevamente la operación de dominio.

---

# Entrega Duplicada

Un Integration Event puede ser entregado más de una vez
por la infraestructura de mensajería.

Los consumidores deben poder procesarlo de forma
idempotente utilizando:

```text
EventId
```

La entrega duplicada no representa un nuevo hecho del
dominio.

---

# Orden de Eventos

AggregateVersion permite establecer el orden lógico de los
eventos pertenecientes a una misma Participation.

Ejemplo.

```text
ParticipationId:
PAR-001

AggregateVersion:
4
```

seguido de:

```text
ParticipationId:
PAR-001

AggregateVersion:
5
```

Los consumidores pueden utilizar esta información para
detectar eventos recibidos fuera de orden.

---

# Consistencia Eventual

Los Integration Events permiten mantener consistencia
eventual entre Bounded Contexts.

```text
Participation

↓

Commit

↓

Integration Event

↓

Consumer

↓

Consumer State Update
```

El estado externo puede actualizarse después de la
confirmación del Aggregate Participation.

---

# Consumidores

Los consumidores de Integration Events no forman parte del
Aggregate Participation.

Pueden incluir:

- otros Bounded Contexts;
- proyecciones;
- servicios de integración;
- procesos de auditoría;
- sistemas externos autorizados.

El consumidor decide cómo reaccionar al evento según su
propio modelo.

---

# Independencia del Consumidor

Participation no debe conocer qué consumidores procesarán
sus Integration Events.

Debe mantenerse:

```text
Participation

↓

Integration Event

↓

Unknown Consumers
```

Esto preserva el desacoplamiento entre Bounded Contexts.

---

# Integración entre Aggregates

Los Integration Events no permiten modificar directamente
otro Aggregate.

Ejemplo.

```text
Participation

↓

ParticipationCompletedIntegrationEvent

↓

Consumer

↓

Application Command

↓

Other Aggregate
```

El Aggregate consumidor conserva sus propias reglas,
Permissions, Invariants y Consistency Boundary.

---

# Read Models

Los Integration Events pueden alimentar proyecciones
externas cuando corresponda.

```text
Integration Event

↓

Projection

↓

Read Model
```

El Read Model resultante continúa siendo una
representación derivada.

---

# Versionado del Evento

La versión del contrato del Integration Event es
independiente de AggregateVersion.

Ejemplo.

```text
EventVersion:
2
```

```text
AggregateVersion:
14
```

Representan conceptos diferentes.

---

# Compatibilidad

La evolución de los Integration Events debe preservar la
compatibilidad necesaria para sus consumidores.

Cambios compatibles pueden incluir:

- incorporación de información opcional;
- extensión del Payload sin modificar el significado del
  evento.

Cambios incompatibles requieren una nueva versión del
contrato.

---

# Información del Payload

El Payload debe contener únicamente información necesaria
para comunicar el hecho.

No debe exponer automáticamente todo el estado interno del
Aggregate.

Esto preserva:

- encapsulamiento;
- seguridad;
- privacidad;
- estabilidad contractual;
- independencia entre Bounded Contexts.

---

# Datos Sensibles

Los Integration Events no deben exponer información
sensible que no sea necesaria para el contrato.

La información publicada debe limitarse al propósito de la
integración.

---

# Domain Events No Publicables

No todo Domain Event necesita convertirse en Integration
Event.

Solo deben publicarse aquellos hechos que formen parte de
los contratos oficiales de integración.

Esto evita exponer detalles internos innecesarios del
Aggregate.

---

# Recuperación ante Fallos

La infraestructura puede volver a intentar la publicación
de un Integration Event.

```text
Outbox Record

↓

Publish

↓

Failure

↓

Retry
```

El reintento no genera:

- una nueva modificación del Aggregate;
- una nueva versión del Aggregate;
- un nuevo Domain Event.

---

# Trazabilidad

Debe poder establecerse la relación conceptual:

```text
Participation

↓

AggregateVersion

↓

Domain Event

↓

Integration Event

↓

External Consumer
```

Esto permite seguir el origen de un cambio a través del
ecosistema AURA.

---

# Restricciones

Los Integration Events:

- representan únicamente hechos confirmados;
- no contienen lógica de negocio;
- no modifican directamente Participation;
- no sustituyen Domain Events;
- no exponen automáticamente el estado completo del
  Aggregate;
- no pueden modificar otros Aggregates;
- no forman parte del Consistency Boundary de
  Participation;
- no pueden publicarse como hechos válidos antes del
  commit correspondiente;
- no deben depender de consumidores específicos;
- deben preservar la identidad del Aggregate;
- deben preservar AggregateVersion;
- deben ser inmutables;
- deben permitir procesamiento idempotente.

---

# Reglas

## REG-001

Todo Integration Event representa un hecho del dominio ya
confirmado.

---

## REG-002

Los Integration Events se originan a partir de Domain
Events relevantes para otros Bounded Contexts o sistemas
externos.

---

## REG-003

Todo Integration Event debe identificar el Aggregate que
originó el hecho.

---

## REG-004

Todo Integration Event debe incluir AggregateVersion.

---

## REG-005

Los Integration Events son inmutables.

---

## REG-006

Un Integration Event no puede modificar directamente otro
Aggregate.

---

## REG-007

La publicación de Integration Events ocurre después de la
confirmación del cambio del Aggregate.

---

## REG-008

La entrega duplicada de un Integration Event no representa
un nuevo hecho del dominio.

---

## REG-009

Los consumidores deben poder identificar eventos
duplicados mediante EventId.

---

## REG-010

Los Integration Events permanecen desacoplados de sus
consumidores.

---

# Definición de Éxito

El Aggregate `Participation` publica Integration Events
inmutables, versionados, trazables y desacoplados que
representan únicamente hechos del dominio previamente
confirmados, permiten comunicar cambios relevantes hacia
otros Bounded Contexts y sistemas externos, preservan la
identidad y versión del Aggregate, soportan procesamiento
idempotente y consistencia eventual y mantienen separados
los contratos internos del dominio de los contratos de
integración de AURA Core.