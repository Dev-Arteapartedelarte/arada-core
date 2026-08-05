# DOMAIN-002K — Citizen Integration Events

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Citizen Management

Aggregate:
Citizen

Documentos relacionados:

- DOMAIN-002-Aggregate.md
- DOMAIN-002D-Domain-Events.md
- DOMAIN-002I-Versioning.md
- DOMAIN-002J-Consistency-Boundary.md
- CORE-005-Domain-Events.md

---

# Objetivo

Este documento define los **Integration Events** publicados por
el Aggregate **Citizen** para permitir la comunicación con
otros Bounded Contexts y sistemas externos.

A diferencia de los Domain Events, los Integration Events
constituyen contratos públicos y estables orientados a la
integración.

Su publicación ocurre únicamente después de que la transacción
del Aggregate haya sido confirmada exitosamente.

---

# Principios

Los Integration Events cumplen los siguientes principios:

- representan hechos ya confirmados;
- son inmutables;
- poseen contratos públicos versionados;
- son independientes del dominio interno;
- son consumidos por otros Bounded Contexts;
- pueden ser enviados a sistemas externos.

---

# Flujo General

```text
Citizen Aggregate

        │

        ▼

Domain Event

        │

        ▼

Outbox Pattern

        │

        ▼

Integration Event

        │

        ▼

Message Broker

        │

        ├──────── Organization
        ├──────── Membership
        ├──────── Territory
        ├──────── Notification
        ├──────── Analytics
        ├──────── Identity
        └──────── Sistemas Externos
```

---

# Relación Domain Event → Integration Event

```text
CitizenRegistered
        │
        ▼
CitizenRegisteredIntegrationEvent
```

```text
CitizenVerified
        │
        ▼
CitizenVerifiedIntegrationEvent
```

```text
CitizenActivated
        │
        ▼
CitizenActivatedIntegrationEvent
```

```text
CitizenSuspended
        │
        ▼
CitizenSuspendedIntegrationEvent
```

```text
CitizenReactivated
        │
        ▼
CitizenReactivatedIntegrationEvent
```

```text
CitizenDeactivated
        │
        ▼
CitizenDeactivatedIntegrationEvent
```

```text
CitizenArchived
        │
        ▼
CitizenArchivedIntegrationEvent
```

```text
CitizenProfileUpdated
        │
        ▼
CitizenProfileUpdatedIntegrationEvent
```

```text
CitizenAddressUpdated
        │
        ▼
CitizenAddressUpdatedIntegrationEvent
```

---

# Eventos Oficiales

El Aggregate Citizen puede publicar los siguientes contratos
de integración:

```text
CitizenRegisteredIntegrationEvent

CitizenVerifiedIntegrationEvent

CitizenActivatedIntegrationEvent

CitizenSuspendedIntegrationEvent

CitizenReactivatedIntegrationEvent

CitizenDeactivatedIntegrationEvent

CitizenArchivedIntegrationEvent

CitizenProfileUpdatedIntegrationEvent

CitizenContactInformationUpdatedIntegrationEvent

CitizenAddressUpdatedIntegrationEvent

CitizenLanguageChangedIntegrationEvent

CitizenConsentWithdrawnIntegrationEvent
```

---

# Contrato Conceptual

Todo Integration Event contiene conceptualmente:

```text
EventId

EventType

AggregateId

AggregateType

OccurredOn

Version

CorrelationId

CausationId

Payload
```

El formato físico (JSON, Avro, Protobuf, etc.) pertenece a la
infraestructura.

---

# Payload

El Payload debe contener únicamente la información necesaria
para que otros contextos reaccionen al evento.

Debe evitar:

- lógica de negocio;
- objetos completos;
- referencias circulares;
- información redundante.

Ejemplo conceptual:

```text
CitizenActivatedIntegrationEvent

CitizenId

OrganizationId

OccurredOn

Version
```

---

# Consumidores

Los principales consumidores son:

## Organization Context

- creación de relaciones;
- sincronización de miembros.

---

## Membership Context

- habilitación de membresías;
- suspensión de acceso;
- reactivación.

---

## Territory Context

- actualización territorial;
- estadísticas geográficas.

---

## Notification Context

- envío de correos;
- SMS;
- notificaciones push.

---

## Analytics Context

- indicadores;
- métricas;
- tableros.

---

## Identity Context

- sincronización de identidad;
- actualización de atributos.

---

## Sistemas Externos

Ejemplos:

- FIWARE;
- CRM;
- plataformas municipales;
- servicios gubernamentales;
- motores de BI.

---

# Publicación

Los Integration Events se publican únicamente después del
commit del Aggregate.

```text
Command

↓

Aggregate

↓

Repository

↓

Commit

↓

Outbox

↓

Broker

↓

Consumers
```

Nunca antes.

---

# Garantías

El modelo garantiza:

- entrega eventual;
- consistencia transaccional;
- independencia entre productores y consumidores;
- reintentos seguros;
- idempotencia.

---

# Idempotencia

Todo consumidor debe asumir que un mismo Integration Event
puede recibirse más de una vez.

La identidad del evento está determinada por:

```text
EventId
```

Los consumidores deben ignorar duplicados.

---

# Versionado

Cada contrato posee:

```text
Version
```

Ejemplo:

```text
CitizenActivatedIntegrationEvent

Version 1
```

Los cambios incompatibles generan una nueva versión del
contrato.

Los contratos existentes nunca se modifican.

---

# Compatibilidad

La evolución de los eventos debe preservar:

- compatibilidad hacia atrás cuando sea posible;
- estabilidad de nombres;
- significado del dominio;
- trazabilidad histórica.

---

# Relación con Event Sourcing

Los Integration Events no forman parte del historial del
Aggregate.

El historial oficial continúa siendo la secuencia de
Domain Events.

---

# Relación con CQRS

Los Integration Events pueden alimentar:

- Read Models;
- Data Warehouse;
- motores de búsqueda;
- sistemas analíticos;
- proyecciones distribuidas.

---

# Seguridad

Los eventos nunca deben exponer:

- credenciales;
- secretos;
- tokens;
- información sensible innecesaria;
- datos personales no autorizados.

Cuando sea necesario compartir información protegida, deberán
aplicarse las políticas de anonimización, minimización o
cifrado definidas por el dominio y la normativa vigente.

---

# Principios Arquitectónicos

Los Integration Events siguen:

- Domain-Driven Design (DDD);
- Event-Driven Architecture;
- Outbox Pattern;
- CQRS;
- Event Sourcing;
- Clean Architecture;
- Open/Closed Principle.

---

# Definición de Éxito

Los **Integration Events** del Aggregate **Citizen** constituyen
la interfaz oficial de comunicación entre el Bounded Context
Citizen y el resto del ecosistema AURA. Permiten la integración
con otros Aggregates, plataformas municipales, FIWARE y
servicios externos mediante contratos públicos estables,
versionados e independientes de la implementación interna del
dominio, garantizando escalabilidad, desacoplamiento y
consistencia eventual.