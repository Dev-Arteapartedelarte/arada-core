# DOMAIN-001C — Organization Commands

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
- CORE-005-Domain-Events.md
- CORE-013-Application-Services.md

---

# Objetivo

Definir los Commands oficiales que representan las
intenciones de modificación sobre el Aggregate
Organization.

Los Commands expresan decisiones del usuario o de otro
sistema y constituyen la única entrada válida para iniciar
cambios de estado en el Aggregate.

Un Command representa una intención.

No representa un hecho consumado.

---

# Principios

Todo Command debe cumplir las siguientes propiedades.

- expresa una intención;
- posee un único objetivo;
- es inmutable;
- contiene únicamente la información necesaria;
- no contiene reglas de negocio;
- no produce efectos secundarios;
- no modifica directamente el estado.

---

# Flujo General

```text
Usuario

↓

Application Service

↓

Command

↓

Command Handler

↓

Organization Aggregate

↓

Domain Events

↓

Repository

↓

Outbox

↓

Event Bus
```

---

# Catálogo Oficial

El Aggregate Organization reconoce los siguientes
Commands.

```text
CreateOrganization

SubmitOrganizationForValidation

ApproveOrganization

RejectOrganization

ActivateOrganization

SuspendOrganization

ReactivateOrganization

ArchiveOrganization

DeleteOrganization

RenameOrganization

ChangeOrganizationAddress

ChangeOrganizationPolicies

ChangeOrganizationSettings

ChangeOrganizationBrand

AssignRepresentative

RegisterMember

RemoveMember

ChangeTerritory
```

---

# Clasificación

## Creación

```text
CreateOrganization
```

---

## Validación

```text
SubmitOrganizationForValidation

ApproveOrganization

RejectOrganization
```

---

## Ciclo de Vida

```text
ActivateOrganization

SuspendOrganization

ReactivateOrganization

ArchiveOrganization

DeleteOrganization
```

---

## Configuración

```text
RenameOrganization

ChangeOrganizationAddress

ChangeOrganizationPolicies

ChangeOrganizationSettings

ChangeOrganizationBrand

ChangeTerritory
```

---

## Membresía

```text
RegisterMember

RemoveMember

AssignRepresentative
```

---

# Especificación de Commands

## CreateOrganization

### Objetivo

Crear una nueva organización.

### Requiere

```text
OrganizationName

OrganizationType

TerritoryId

RepresentativeId
```

### Estado esperado

```text
Draft
```

### Evento esperado

```text
OrganizationCreated
```

---

## SubmitOrganizationForValidation

### Objetivo

Solicitar la validación institucional.

### Estado origen

```text
Draft
```

### Estado destino

```text
PendingValidation
```

### Evento

```text
OrganizationSubmittedForValidation
```

---

## ApproveOrganization

### Objetivo

Aprobar una organización validada.

### Estado origen

```text
PendingValidation
```

### Estado destino

```text
Active
```

### Evento

```text
OrganizationActivated
```

---

## RejectOrganization

### Objetivo

Rechazar la validación.

### Estado origen

```text
PendingValidation
```

### Estado destino

```text
Draft
```

### Evento

```text
OrganizationValidationRejected
```

---

## SuspendOrganization

### Objetivo

Suspender temporalmente una organización.

### Estado origen

```text
Active
```

### Estado destino

```text
Suspended
```

### Evento

```text
OrganizationSuspended
```

---

## ReactivateOrganization

### Objetivo

Levantar una suspensión.

### Estado origen

```text
Suspended
```

### Estado destino

```text
Active
```

### Evento

```text
OrganizationReactivated
```

---

## ArchiveOrganization

### Objetivo

Cerrar definitivamente la operación.

### Estados válidos

```text
Active

Suspended
```

### Estado destino

```text
Archived
```

### Evento

```text
OrganizationArchived
```

---

## DeleteOrganization

### Objetivo

Eliminar lógicamente la organización.

### Estados válidos

```text
Draft

Archived
```

### Estado destino

```text
Deleted
```

### Evento

```text
OrganizationDeleted
```

---

## RenameOrganization

### Objetivo

Modificar el nombre oficial.

### Evento

```text
OrganizationRenamed
```

---

## ChangeOrganizationAddress

### Objetivo

Modificar la dirección oficial.

### Evento

```text
OrganizationAddressChanged
```

---

## ChangeOrganizationPolicies

### Objetivo

Actualizar las políticas internas.

### Evento

```text
OrganizationPoliciesChanged
```

---

## ChangeOrganizationSettings

### Objetivo

Actualizar la configuración institucional.

### Evento

```text
OrganizationSettingsChanged
```

---

## ChangeOrganizationBrand

### Objetivo

Actualizar la identidad gráfica.

### Evento

```text
OrganizationBrandChanged
```

---

## RegisterMember

### Objetivo

Incorporar un nuevo miembro.

### Evento

```text
MemberRegistered
```

---

## RemoveMember

### Objetivo

Eliminar una membresía.

### Evento

```text
MemberRemoved
```

---

## AssignRepresentative

### Objetivo

Designar un representante oficial.

### Evento

```text
RepresentativeAssigned
```

---

## ChangeTerritory

### Objetivo

Modificar el territorio asociado.

### Evento

```text
TerritoryChanged
```

---

# Reglas del Dominio

## Regla 1

Un Command nunca modifica directamente el Aggregate.

---

## Regla 2

Todo Command es procesado por un único Command Handler.

---

## Regla 3

Todo Command genera cero o más Domain Events.

---

## Regla 4

Un Command puede ser rechazado por el Aggregate.

---

## Regla 5

La validación del dominio ocurre exclusivamente dentro del
Aggregate Root.

---

## Regla 6

Los Commands no contienen lógica de negocio.

---

## Regla 7

Un Command nunca consulta información.

Las consultas pertenecen al modelo de lectura (CQRS).

---

# Idempotencia

Los Commands susceptibles de ser reenviados deben soportar
idempotencia mediante un identificador único de comando
(`CommandId`).

Esto permite evitar ejecuciones duplicadas ante reintentos
o fallos de comunicación.

---

# Trazabilidad

Cada Command debe registrar como mínimo:

```text
CommandId

OrganizationId

ActorId

Timestamp

CorrelationId

CausationId
```

Estos metadatos permiten auditoría, seguimiento distribuido
y correlación de eventos.

---

# Relación con Domain Events

Todo Command exitoso culmina con la emisión de uno o más
Domain Events.

```text
Command

↓

Aggregate

↓

Domain Event
```

Nunca ocurre el proceso inverso.

---

# Definición de Éxito

El modelo de Commands del Aggregate Organization establece
un contrato explícito para todas las modificaciones del
dominio, separando las intenciones de los hechos, alineando
la implementación con CQRS y garantizando que todo cambio
de estado sea procesado de forma consistente, auditable y
controlada exclusivamente por el Aggregate Root.