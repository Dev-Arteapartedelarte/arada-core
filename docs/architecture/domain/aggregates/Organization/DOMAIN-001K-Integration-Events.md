# DOMAIN-001K — Organization Integration Events

Versión: 1.0

Estado:
Oficial

Proyecto:
AURA Core

Bounded Context:
Organization Management

Aggregate:
Organization

Autor:
ARADA

Documentos Relacionados:

- DOMAIN-001D-Domain-Events.md
- CORE-005-Domain-Events.md
- CORE-007-Strategic-Design.md
- CORE-015-Package-Architecture.md
- DOMAIN-001G-Repository-Contract.md

---

# Objetivo

Definir los Integration Events emitidos por el Aggregate
Organization.

Estos eventos representan la información pública que el
Bounded Context expone al resto de la plataforma AURA y a
los sistemas externos.

Los Integration Events son independientes de los Domain
Events y constituyen el contrato oficial de integración.

---

# Motivación

Un Domain Event describe un hecho ocurrido dentro del
dominio.

Un Integration Event comunica un hecho consumible por
otros Bounded Contexts o plataformas externas.

Esta separación evita acoplamiento entre dominios y
permite evolucionar el modelo interno sin romper
integraciones existentes.

---

# Principios

Los Integration Events deben cumplir las siguientes
reglas.

- ser públicos;
- ser estables;
- ser versionados;
- ser inmutables;
- contener únicamente información necesaria;
- nunca exponer entidades internas;
- nunca depender de clases del dominio.

---

# Diferencia entre Domain Event e Integration Event

```text
Organization Aggregate

↓

OrganizationApproved
(Domain Event)

↓

Event Mapper

↓

OrganizationActivatedIntegrationEvent

↓

Outbox

↓

Event Bus

↓

Consumidores
```

El Domain Event pertenece al dominio.

El Integration Event pertenece al contrato de
integración.

---

# Flujo Oficial

```text
Command

↓

Aggregate

↓

Domain Event

↓

Repository

↓

Outbox

↓

Commit

↓

Integration Event

↓

Event Bus

↓

Consumidores
```

Nunca se publica un Integration Event antes de confirmar
la persistencia del Aggregate.

---

# Catálogo Oficial

## OrganizationCreatedIntegrationEvent

Se publica cuando una organización es creada.

Consumidores posibles.

```text
Identity Context

Notification Context

Audit Context
```

---

## OrganizationSubmittedIntegrationEvent

Se publica cuando una organización solicita validación.

Consumidores.

```text
Municipal Validation

Workflow Engine

Notification Context
```

---

## OrganizationApprovedIntegrationEvent

Se publica cuando la organización queda oficialmente
validada.

Consumidores.

```text
FIWARE Gateway

Municipality Connector

Citizen Portal

Analytics
```

---

## OrganizationRejectedIntegrationEvent

Consumidores.

```text
Notification Context

Workflow Context
```

---

## OrganizationActivatedIntegrationEvent

Consumidores.

```text
Participation Context

Territory Context

Identity Context

FIWARE
```

---

## OrganizationSuspendedIntegrationEvent

Consumidores.

```text
Notification Context

Permissions Context

Audit Context
```

---

## OrganizationReactivatedIntegrationEvent

Consumidores.

```text
Permissions Context

Participation Context

Analytics
```

---

## OrganizationArchivedIntegrationEvent

Consumidores.

```text
Archive Context

Analytics

Backup
```

---

## OrganizationDeletedIntegrationEvent

Consumidores.

```text
Audit

Synchronization

Data Lake
```

---

## RepresentativeAssignedIntegrationEvent

Consumidores.

```text
Identity Context

Notification Context
```

---

## MemberRegisteredIntegrationEvent

Consumidores.

```text
Identity

Participation

Statistics
```

---

# Contrato Conceptual

Todo Integration Event comparte la siguiente estructura.

```text
EventId

EventType

EventVersion

OccurredOn

AggregateId

AggregateType

CorrelationId

CausationId

Payload
```

---

# Metadata Obligatoria

Cada evento debe incluir:

```text
eventId

aggregateId

aggregateVersion

occurredAt

eventVersion

correlationId

causationId

producer

tenantId
```

---

# Versionado

Los Integration Events son contratos públicos.

Toda modificación incompatible requiere una nueva versión.

Ejemplo.

```text
OrganizationApproved v1

↓

OrganizationApproved v2
```

Las versiones anteriores deben mantenerse durante el
período de compatibilidad definido por la plataforma.

---

# Idempotencia

Cada evento debe poder procesarse múltiples veces sin
producir efectos secundarios.

Para ello:

- EventId debe ser único.
- AggregateVersion debe acompañar al evento.
- Los consumidores deben detectar duplicados.

---

# Orden

El orden de publicación debe respetar el orden lógico del
Aggregate.

Ejemplo.

```text
OrganizationCreated

↓

OrganizationSubmitted

↓

OrganizationApproved

↓

OrganizationActivated
```

Nunca debe observarse un evento de activación antes de la
creación.

---

# Integración con FIWARE

Cuando una organización es activada.

```text
OrganizationActivatedIntegrationEvent
```

El FIWARE Gateway podrá transformar el evento en una
entidad NGSI-LD.

Ejemplo conceptual.

```text
Organization

↓

NGSI-LD Entity

↓

Orion Context Broker
```

El Aggregate no conoce FIWARE.

La transformación ocurre fuera del dominio.

---

# Integración con Municipios

Cuando una organización cambia de estado.

```text
OrganizationApprovedIntegrationEvent
```

Puede ser consumido por:

```text
Municipality Connector

↓

Registro Municipal

↓

Sistema Documental

↓

Portal Ciudadano
```

El Aggregate desconoce completamente estos sistemas.

---

# Integración con Blockchain

En futuras etapas, determinados eventos podrán registrarse
en una cadena de bloques.

Ejemplo.

```text
OrganizationApproved

↓

Blockchain Adapter

↓

Hash Persistido
```

El dominio permanece independiente de esta decisión.

---

# Reglas

## REG-001

Todo Integration Event deriva de uno o más Domain Events.

---

## REG-002

Los Integration Events nunca son generados directamente
por el Aggregate.

---

## REG-003

La publicación ocurre únicamente después de una
persistencia exitosa.

---

## REG-004

Los Integration Events son inmutables.

---

## REG-005

Todo evento posee identificador global único.

---

## REG-006

Todo evento está versionado.

---

## REG-007

Los consumidores nunca dependen de clases del dominio.

---

## REG-008

Los contratos públicos deben permanecer estables a lo
largo del tiempo.

---

# Relación con Event Mapper

La transformación entre Domain Events e Integration Events
es responsabilidad de un componente especializado.

```text
Domain Event

↓

Integration Event Mapper

↓

Integration Event
```

Este componente pertenece a la capa de Application o
Infrastructure, nunca al dominio.

---

# Definición de Éxito

El Aggregate `Organization` publica únicamente Domain
Events internos. Tras una persistencia exitosa, dichos
eventos son transformados mediante un Event Mapper en
Integration Events públicos, versionados e inmutables,
que constituyen el contrato oficial de interoperabilidad
de AURA Core con otros Bounded Contexts, municipios,
FIWARE y futuras plataformas externas, preservando la
independencia y evolución del modelo de dominio.