# DOMAIN-002D — Citizen Domain Events

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
- DOMAIN-002A-Lifecycle.md
- DOMAIN-002B-State-Machine.md
- DOMAIN-002C-Commands.md
- CORE-005-Domain-Events.md

---

# Objetivo

Este documento define los Domain Events oficiales emitidos por
el Aggregate Citizen.

Los Domain Events representan hechos de negocio que ya han
ocurrido y forman parte permanente de la historia del dominio.

Una vez publicados son inmutables y nunca pueden modificarse.

---

# Principios

Los Domain Events cumplen los siguientes principios:

- describen hechos pasados;
- son inmutables;
- representan lenguaje del dominio;
- pueden consumirse por múltiples Bounded Contexts;
- son independientes de la infraestructura;
- forman parte de la auditoría del sistema.

---

# Flujo General

```text
Application Service

        │

        ▼

Citizen Aggregate

        │

        ▼

Domain Validation

        │

        ▼

Domain Event

        │

        ▼

Event Bus

        │

        ├──────── Organization
        ├──────── Membership
        ├──────── Participation
        ├──────── Notification
        ├──────── Audit
        ├──────── Integration
        └──────── Read Models
```

---

# Eventos Oficiales

El Aggregate Citizen puede emitir los siguientes eventos.

```text
CitizenRegistered

CitizenVerificationRequested

CitizenVerified

CitizenActivated

CitizenSuspended

CitizenReactivated

CitizenDeactivated

CitizenArchived

CitizenProfileUpdated

CitizenContactInformationUpdated

CitizenAddressUpdated

CitizenLanguageChanged

CitizenPrivacyPolicyAccepted

CitizenConsentWithdrawn
```

---

# CitizenRegistered

## Descripción

Indica que una nueva identidad cívica ha sido creada.

## Origen

```text
RegisterCitizen
```

## Estado

```text
Draft
```

## Consumidores habituales

- Audit
- Notification
- Analytics

---

# CitizenVerificationRequested

## Descripción

Se ha iniciado el proceso de validación de identidad.

## Estado

```text
PendingVerification
```

## Consumidores

- Identity
- Integration
- Notification

---

# CitizenVerified

## Descripción

La identidad fue validada correctamente.

## Estado

```text
Verified
```

## Consumidores

- Organization
- Membership
- Participation

---

# CitizenActivated

## Descripción

El ciudadano quedó habilitado para participar en el
ecosistema.

## Estado

```text
Active
```

## Consumidores

- Membership
- Voting
- Assembly
- Participation

---

# CitizenSuspended

## Descripción

La participación del ciudadano fue suspendida.

## Estado

```text
Suspended
```

## Consumidores

- Membership
- Voting
- Governance
- Notification

---

# CitizenReactivated

## Descripción

El ciudadano recuperó su estado operativo.

## Estado

```text
Active
```

## Consumidores

- Participation
- Voting
- Membership

---

# CitizenDeactivated

## Descripción

El ciudadano dejó de participar activamente en la plataforma.

## Estado

```text
Inactive
```

## Consumidores

- Notification
- Analytics
- Audit

---

# CitizenArchived

## Descripción

El ciclo de vida del Aggregate finalizó.

## Estado

```text
Archived
```

## Consumidores

- Audit
- Analytics
- Integration

---

# CitizenProfileUpdated

## Descripción

Se modificó información general del ciudadano.

Ejemplos:

- nombre;
- fotografía;
- preferencias públicas.

## Consumidores

- Read Models
- Notification

---

# CitizenContactInformationUpdated

## Descripción

Cambiaron los datos oficiales de contacto.

Ejemplos:

- email;
- teléfono.

## Consumidores

- Notification
- Identity

---

# CitizenAddressUpdated

## Descripción

El domicilio registrado fue actualizado.

## Consumidores

- Territory
- Integration

---

# CitizenLanguageChanged

## Descripción

El ciudadano modificó su idioma preferido.

## Consumidores

- Notification
- UI Preferences

---

# CitizenPrivacyPolicyAccepted

## Descripción

El ciudadano aceptó una nueva versión de la política de
privacidad o tratamiento de datos.

## Consumidores

- Audit
- Compliance

---

# CitizenConsentWithdrawn

## Descripción

El ciudadano retiró un consentimiento previamente otorgado.

Puede desencadenar procesos de anonimización o restricciones
de tratamiento de datos conforme a la normativa aplicable.

## Consumidores

- Compliance
- Integration
- Audit

---

# Estructura General

Todos los Domain Events siguen una estructura lógica similar.

```text
EventId

AggregateId

AggregateType

EventType

OccurredOn

Version

Payload
```

La representación física del evento depende de la
infraestructura y no forma parte del dominio.

---

# Versionado

Cada Domain Event posee:

```text
Version
```

La versión permite evolucionar el contrato sin afectar a los
consumidores existentes.

Los cambios incompatibles requieren una nueva versión del
evento.

---

# Orden

Los eventos emitidos por un mismo Aggregate mantienen orden
estricto.

```text
CitizenRegistered

↓

CitizenVerified

↓

CitizenActivated

↓

CitizenProfileUpdated

↓

CitizenSuspended
```

No existe garantía de orden entre Aggregates diferentes.

---

# Persistencia

Los Domain Events pueden almacenarse en:

- Event Store;
- Outbox;
- cola de mensajería;
- sistema de auditoría.

La decisión corresponde a la infraestructura.

---

# Reglas

Los Domain Events:

- nunca contienen lógica de negocio;
- nunca modifican Aggregates;
- nunca realizan consultas;
- nunca invocan servicios externos.

Representan únicamente hechos consumados.

---

# Compatibilidad con Event Sourcing

Los eventos permiten reconstruir completamente el estado del
Aggregate Citizen mediante la reproducción cronológica de la
secuencia de eventos.

---

# Compatibilidad con CQRS

Los Domain Events alimentan las proyecciones utilizadas por el
lado de lectura.

Ejemplos:

- ciudadanos activos;
- ciudadanos suspendidos;
- ciudadanos por territorio;
- ciudadanos verificados;
- indicadores estadísticos.

---

# Integración

Los Domain Events pueden transformarse posteriormente en
Integration Events para comunicarse con otros Bounded Contexts
o sistemas externos.

La transformación ocurre fuera del Aggregate.

---

# Principios Arquitectónicos

Los Domain Events cumplen:

- Domain-Driven Design;
- Event-Driven Architecture;
- Clean Architecture;
- Open/Closed Principle;
- Single Responsibility Principle.

---

# Definición de Éxito

Los Domain Events del Aggregate Citizen constituyen el registro
oficial de todos los hechos relevantes relacionados con una
identidad cívica dentro del ecosistema AURA. Permiten auditoría,
trazabilidad, integración entre contextos, construcción de
proyecciones y compatibilidad con arquitecturas distribuidas
basadas en eventos, manteniendo al Aggregate completamente
desacoplado de la infraestructura.