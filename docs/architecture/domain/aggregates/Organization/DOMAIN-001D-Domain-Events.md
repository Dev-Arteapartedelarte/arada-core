# DOMAIN-001D — Organization Domain Events

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

- DOMAIN-001-Aggregate.md
- DOMAIN-001A-Lifecycle.md
- DOMAIN-001B-State-Machine.md
- DOMAIN-001C-Commands.md
- CORE-005-Domain-Events.md

---

# Objetivo

Definir los Domain Events oficiales emitidos por el
Aggregate Organization.

Los Domain Events representan hechos consumados del
dominio. Son inmutables y describen cambios de estado que
ya ocurrieron exitosamente dentro del Aggregate.

Constituyen el mecanismo oficial mediante el cual otros
Bounded Contexts conocen la evolución de una organización.

---

# Principios

Todo Domain Event debe cumplir las siguientes reglas.

- representa un hecho pasado;
- es inmutable;
- posee identidad propia;
- pertenece al lenguaje ubicuo;
- nunca contiene comportamiento;
- nunca modifica el dominio;
- puede ser consumido por múltiples contextos.

---

# Flujo General

```text
Command

↓

Application Service

↓

Organization Aggregate

↓

State Transition

↓

Domain Event

↓

Repository

↓

Outbox

↓

Event Bus

↓

Subscribers
```

---

# Catálogo Oficial

El Aggregate Organization puede emitir los siguientes
Domain Events.

```text
OrganizationCreated

OrganizationSubmittedForValidation

OrganizationActivated

OrganizationValidationRejected

OrganizationSuspended

OrganizationReactivated

OrganizationArchived

OrganizationDeleted

OrganizationRenamed

OrganizationAddressChanged

OrganizationPoliciesChanged

OrganizationSettingsChanged

OrganizationBrandChanged

RepresentativeAssigned

MemberRegistered

MemberRemoved

TerritoryChanged
```

---

# Eventos del Ciclo de Vida

## OrganizationCreated

### Descripción

La organización fue creada exitosamente.

### Origen

```text
CreateOrganization
```

### Estado

```text
Draft
```

### Consumidores posibles

- Identity
- Audit
- Notification

---

## OrganizationSubmittedForValidation

### Descripción

La organización solicitó validación.

### Estado origen

```text
Draft
```

### Estado destino

```text
PendingValidation
```

---

## OrganizationActivated

### Descripción

La organización quedó oficialmente habilitada para operar.

### Estado destino

```text
Active
```

### Consumidores posibles

- Membership
- Assembly
- Voting
- Notification
- Audit

---

## OrganizationValidationRejected

### Descripción

La solicitud de validación fue rechazada.

### Estado destino

```text
Draft
```

---

## OrganizationSuspended

### Descripción

La organización quedó suspendida temporalmente.

### Estado destino

```text
Suspended
```

---

## OrganizationReactivated

### Descripción

La suspensión fue levantada.

### Estado destino

```text
Active
```

---

## OrganizationArchived

### Descripción

La organización terminó su operación.

### Estado destino

```text
Archived
```

---

## OrganizationDeleted

### Descripción

La organización fue eliminada lógicamente.

### Estado destino

```text
Deleted
```

---

# Eventos de Configuración

## OrganizationRenamed

Describe un cambio del nombre oficial.

---

## OrganizationAddressChanged

Describe un cambio de dirección institucional.

---

## OrganizationPoliciesChanged

Describe una actualización de políticas internas.

---

## OrganizationSettingsChanged

Describe una modificación de configuración.

---

## OrganizationBrandChanged

Describe un cambio en la identidad institucional.

---

## TerritoryChanged

Describe una modificación del territorio asociado.

---

# Eventos de Membresía

## RepresentativeAssigned

Indica la asignación de un representante oficial.

---

## MemberRegistered

Indica la incorporación de un nuevo miembro.

---

## MemberRemoved

Indica la eliminación de una membresía.

---

# Estructura Base de un Domain Event

Todos los Domain Events deberán implementar el siguiente
contrato conceptual.

```text
EventId

AggregateId

AggregateType

EventType

OccurredOn

Version

ActorId

CorrelationId

CausationId

Metadata

Payload
```

---

# Payload

Cada evento define únicamente la información necesaria
para que otros Bounded Contexts comprendan el hecho
ocurrido.

Ejemplo conceptual.

```text
OrganizationActivated

OrganizationId

ActivatedAt

ActivatedBy
```

El payload nunca contiene lógica de negocio.

---

# Versionado

Los Domain Events son contratos públicos.

Una vez publicados:

- no se eliminan;
- no cambian su significado;
- deben versionarse cuando exista un cambio incompatible.

Ejemplo.

```text
OrganizationActivated v1

↓

OrganizationActivated v2
```

---

# Publicación

Los eventos son emitidos exclusivamente por el Aggregate
Organization.

El Aggregate no publica directamente al Event Bus.

El flujo oficial es:

```text
Organization

↓

Repository

↓

Outbox

↓

Event Bus
```

Este mecanismo garantiza consistencia transaccional y evita
la pérdida de eventos.

---

# Orden de Publicación

Los eventos deben conservar el orden exacto en que fueron
generados dentro de la transacción.

Ejemplo.

```text
OrganizationCreated

↓

RepresentativeAssigned

↓

OrganizationSubmittedForValidation
```

El orden forma parte del significado del dominio.

---

# Consumo por Otros Contextos

Los Domain Events podrán ser utilizados por contextos como:

- Membership
- Assembly
- Voting
- Identity
- Notification
- Document
- Transparency
- Audit
- Analytics

Cada contexto es responsable de interpretar el evento
según sus propias reglas, sin modificar el Aggregate de
origen.

---

# Reglas del Dominio

## Regla 1

Todo cambio exitoso del Aggregate genera al menos un
Domain Event.

---

## Regla 2

Un Domain Event nunca inicia una transacción sobre el
Aggregate que lo produjo.

---

## Regla 3

Los Domain Events son inmutables.

---

## Regla 4

Los nombres de los eventos deben expresarse en pasado.

---

## Regla 5

Los eventos utilizan exclusivamente términos del lenguaje
ubicuo.

---

## Regla 6

Todo Domain Event pertenece a un único Aggregate.

---

## Regla 7

Los eventos representan hechos, nunca intenciones.

---

# Definición de Éxito

El modelo de Domain Events del Aggregate Organization
garantiza que toda evolución del dominio quede registrada
como un hecho inmutable, auditable y desacoplado,
permitiendo la integración consistente entre Bounded
Contexts mediante un modelo orientado a eventos y
preservando la integridad del ecosistema AURA.