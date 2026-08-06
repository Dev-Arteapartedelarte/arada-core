# DOMAIN-004K — Role Integration Events

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Authorization Management

Aggregate:
Role

Documentos relacionados:

- DOMAIN-004-Aggregate.md
- DOMAIN-004D-Domain-Events.md
- DOMAIN-004J-Consistency-Boundary.md
- DOMAIN-005-Aggregate.md
- CORE-009-Domain-Events.md
- CORE-013-Integration-Events.md

---

# Objetivo

Este documento define los **Integration Events** publicados por
el Aggregate **Role**.

Mientras los Domain Events permanecen dentro del Bounded
Context, los Integration Events representan contratos públicos
utilizados para comunicar cambios relevantes a otros Bounded
Contexts y servicios del ecosistema AURA.

Los Integration Events constituyen la frontera oficial de
integración del Aggregate.

---

# Principios

Los Integration Events siguen los siguientes principios:

- representan hechos ya confirmados;
- se publican únicamente después del commit;
- son inmutables;
- están versionados;
- son independientes de la infraestructura;
- constituyen contratos públicos.

---

# Diferencia entre Domain Event e Integration Event

```text
Command

↓

Aggregate

↓

Domain Event

↓

Commit

↓

Integration Event

↓

Otros Bounded Contexts
```

Los Domain Events pertenecen al dominio.

Los Integration Events pertenecen a la integración entre
contextos.

---

# Integration Events Oficiales

| Integration Event | Propósito |
|-------------------|-----------|
| RoleCreatedIntegrationEvent | Nuevo Role disponible |
| RoleActivatedIntegrationEvent | Role habilitado |
| RoleDeactivatedIntegrationEvent | Role suspendido |
| RoleArchivedIntegrationEvent | Role archivado |
| RoleRenamedIntegrationEvent | Cambio de nombre |
| RoleDescriptionChangedIntegrationEvent | Cambio de descripción |

---

# RoleCreatedIntegrationEvent

## Disparador

```text
RoleCreated
```

## Consumidores posibles

- Membership
- Permission
- Audit
- Notification
- Reporting

## Payload conceptual

```text
EventId

RoleId

OrganizationId

Name

Code

RoleType

IsSystemRole

OccurredOn

Version
```

---

# RoleActivatedIntegrationEvent

## Disparador

```text
RoleActivated
```

## Consumidores posibles

- Membership
- Authorization
- Notification
- Audit

## Payload conceptual

```text
EventId

RoleId

OrganizationId

OccurredOn

Version
```

---

# RoleDeactivatedIntegrationEvent

## Disparador

```text
RoleDeactivated
```

## Consumidores posibles

- Membership
- Authorization
- Audit

## Payload conceptual

```text
EventId

RoleId

OrganizationId

OccurredOn

Version
```

---

# RoleArchivedIntegrationEvent

## Disparador

```text
RoleArchived
```

## Consumidores posibles

- Membership
- Authorization
- Notification
- Audit
- Analytics

## Payload conceptual

```text
EventId

RoleId

OrganizationId

OccurredOn

Version
```

---

# RoleRenamedIntegrationEvent

## Disparador

```text
RoleRenamed
```

## Consumidores posibles

- Search
- Notification
- Reporting

## Payload conceptual

```text
EventId

RoleId

OrganizationId

OldName

NewName

OccurredOn

Version
```

---

# RoleDescriptionChangedIntegrationEvent

## Disparador

```text
RoleDescriptionChanged
```

## Consumidores posibles

- Search
- Audit
- Reporting

## Payload conceptual

```text
EventId

RoleId

OccurredOn

Version
```

---

# Flujo de Publicación

```text
Execute Command

↓

Update Aggregate

↓

Generate Domain Event

↓

Commit Transaction

↓

Publish Integration Event

↓

Event Bus
```

Nunca debe publicarse un Integration Event antes de que la
transacción haya finalizado correctamente.

---

# Garantías

Todo Integration Event garantiza:

- que el Aggregate quedó consistente;
- que la transacción fue confirmada;
- que el cambio es irreversible;
- que puede ser consumido de forma asíncrona.

---

# Versionado

Todo Integration Event incluye:

```text
EventVersion
```

Ejemplo:

```text
RoleActivatedIntegrationEvent

EventVersion = 1
```

Cambios incompatibles generan una nueva versión del contrato.

---

# Idempotencia

Los consumidores deben considerar:

```text
EventId
```

como identificador único.

Procesar el mismo evento varias veces debe producir exactamente
el mismo resultado observable.

---

# Orden

Para un mismo Aggregate:

```text
RoleCreated

↓

RoleActivated

↓

RoleRenamed

↓

RoleArchived
```

el orden de publicación debe preservarse.

Entre distintos Aggregates no existe garantía de orden global.

---

# Seguridad

Los Integration Events no deben exponer:

- credenciales;
- secretos;
- información sensible;
- datos internos del Aggregate;
- referencias a infraestructura.

Únicamente deben contener la información necesaria para los
consumidores.

---

# Consistencia Eventual

Los consumidores mantienen su propia consistencia mediante:

```text
Receive Event

↓

Validate

↓

Update Local Model
```

No existen transacciones distribuidas entre Bounded Contexts.

---

# Consumidores Conceptuales

Los eventos publicados por **Role** pueden ser consumidos por:

```text
Membership

Permission

Authorization

Notification

Audit

Reporting

Search

Analytics
```

Cada consumidor decide cómo reaccionar al evento sin acoplarse
al Aggregate.

---

# Compatibilidad Arquitectónica

Este modelo es compatible con:

- Domain-Driven Design (DDD);
- Event-Driven Architecture (EDA);
- CQRS;
- Outbox Pattern;
- Event Bus;
- Clean Architecture.

---

# Definición de Éxito

Los **Integration Events** del Aggregate **Role** establecen el
contrato oficial de comunicación entre el Bounded Context de
**Authorization Management** y el resto del ecosistema AURA.
Garantizan una integración desacoplada, versionada y basada en
consistencia eventual, permitiendo que otros Aggregates y
servicios reaccionen a la evolución de los Roles sin comprometer
la integridad del dominio ni introducir dependencias directas.