# DOMAIN-008 Participation — VS-001

## Nombre

**VS-001 — Register and Activate Participation**

## Objetivo

Implementar el primer vertical slice ejecutable del Aggregate `Participation`, cubriendo su creación válida y su primera transición oficial de lifecycle:

```text
Nonexistent
    │
    │ RegisterParticipation
    ▼
Registered
    │
    │ ActivateParticipation
    ▼
Active
```

VS-001 debe demostrar de extremo a extremo que AURA Core puede:

* crear una `Participation`;
* validar identidad, organización, actor, tipo y contexto;
* aplicar autorización;
* preservar invariantes;
* persistir el Aggregate;
* controlar concurrencia mediante `ExpectedVersion`;
* incrementar `Version` correctamente;
* producir Domain Events;
* mapear los hechos confirmados hacia Integration Events;
* mantener separados Domain, Application, Infrastructure e Interfaces.

---

# Alcance funcional

VS-001 incluye exclusivamente:

```text
RegisterParticipation
ActivateParticipation
```

con los correspondientes hechos:

```text
ParticipationRegistered
ParticipationActivated
```

y contratos públicos:

```text
ParticipationRegisteredIntegrationEvent
ParticipationActivatedIntegrationEvent
```

No se implementarán en este slice:

```text
CompleteParticipation
WithdrawParticipation
InvalidateParticipation
ArchiveParticipation
ChangeParticipationType
ChangeParticipationContext
UpdateParticipationMetadata
```

aunque los tipos y contratos estructurales necesarios podrán quedar preparados cuando formen parte del núcleo estable del Aggregate.

---

# Estados incluidos

VS-001 reconoce operacionalmente:

```text
Registered
Active
```

La implementación del tipo `ParticipationStatus` puede representar el conjunto canónico completo:

```text
Registered
Active
Completed
Withdrawn
Invalidated
Archived
```

pero VS-001 sólo ejecutará las transiciones:

```text
None       → Registered
Registered → Active
```

No deberá existir comportamiento ejecutable para las demás transiciones dentro de este slice.

---

# Aggregate Root

La Aggregate Root es:

```text
Participation
```

Su identidad es:

```text
ParticipationId
```

Su propiedad organizacional es:

```text
OrganizationId
```

Debe preservarse:

```text
ParticipationId = immutable
OrganizationId  = immutable
```

La Aggregate Root será la única autoridad capaz de ejecutar las modificaciones de estado incluidas en VS-001.

---

# Registro — RegisterParticipation

## Intención

`RegisterParticipation` solicita crear una nueva instancia formal de Participation.

## Estado origen

```text
Nonexistent
```

## Estado destino

```text
Registered
```

## Resultado mínimo

Después de un registro válido debe cumplirse:

```text
Participation exists

ParticipationStatus = Registered

Version = 1

ParticipationRegistered produced
```

La documentación de Test Scenarios establece explícitamente que un registro válido produce `Registered`, `Version = 1` y `ParticipationRegistered`.

---

# Datos mínimos de RegisterParticipation

El Command deberá representar conceptualmente:

```text
CommandId

ParticipationId

OrganizationId

ActorId

ParticipationType

Timestamp

CorrelationId

CausationId
```

y podrá contener las referencias contextuales necesarias:

```text
CitizenId

MembershipId

TerritoryId

AssemblyId

ProposalId

VotingId
```

cuando correspondan al contexto real.

VS-001 **no impondrá artificialmente que todas estas referencias existan**.

---

# Actor de Participation

VS-001 debe respetar la semántica documental:

```text
CitizenId
MembershipId
```

pueden identificar al participante según el contexto.

No se establecerá como invariante nueva:

```text
exactly one of CitizenId or MembershipId
```

porque DOMAIN-008 no la declara.

Tampoco se introducirá como lenguaje canónico un Value Object:

```text
ParticipantReference
```

sin una decisión documental adicional.

La implementación deberá representar las referencias documentadas sin inventar cardinalidad nueva.

---

# Contexto

Una Participation debe poseer contexto suficiente y válido.

Las referencias reconocidas incluyen:

```text
TerritoryId
AssemblyId
ProposalId
VotingId
```

VS-001 deberá permitir únicamente las referencias que efectivamente correspondan al registro solicitado.

Debe mantenerse:

```text
External Aggregate Reference

≠

External Aggregate Inclusion
```

Ningún Aggregate externo pasa a formar parte del Consistency Boundary de Participation.

---

# ParticipationType

VS-001 debe implementar `ParticipationType` como concepto de dominio válido.

La taxonomía deberá provenir exclusivamente de DOMAIN-008.

No se crearán tipos nuevos por conveniencia técnica.

Un `ParticipationType` inválido debe impedir la creación del Aggregate.

---

# CreatedAt

Un registro válido debe definir:

```text
CreatedAt
```

como timestamp de creación del Aggregate.

Debe mantenerse:

```text
Status = Registered
```

sin timestamps correspondientes a hechos futuros.

Por ejemplo, una Participation recién registrada no debe poseer anticipadamente:

```text
StartedAt
CompletedAt
WithdrawnAt
InvalidatedAt
ArchivedAt
```

---

# Activation — ActivateParticipation

## Intención

`ActivateParticipation` solicita iniciar formalmente una Participation registrada.

## Estado origen

```text
Registered
```

## Estado destino

```text
Active
```

## Resultado mínimo

Después de una activación válida:

```text
ParticipationStatus = Active

StartedAt defined

Version = 2

ParticipationActivated produced
```

Esto constituye el segundo comportamiento funcional de VS-001.

---

# Precondiciones de ActivateParticipation

Como mínimo deben cumplirse:

```text
Participation exists

CurrentStatus = Registered

OrganizationId matches

Participation.Activate = Granted

Required context remains valid

ExpectedVersion = CurrentVersion

Applicable invariants hold
```

Si cualquiera de estas condiciones falla, la activación debe rechazarse.

---

# StartedAt

La transición:

```text
Registered
    ↓
Active
```

debe establecer:

```text
StartedAt
```

`StartedAt` pertenece al estado resultante y debe preservarse posteriormente.

La activación no debe modificar `CreatedAt`.

---

# Prohibición de doble activación

Una vez:

```text
ParticipationStatus = Active
```

otro:

```text
ActivateParticipation
```

debe ser rechazado.

Debe mantenerse:

```text
Active
    ↓
ActivateParticipation
    ↓
Rejected
```

con:

```text
State unchanged
Version unchanged
No ParticipationActivated
```

No debe modelarse la segunda activación como no-op exitoso.

---

# Permissions

VS-001 incluye exactamente:

```text
Participation.Register
Participation.Activate
```

La autorización deberá evaluarse antes de permitir el comportamiento solicitado.

Debe preservarse:

```text
Authorized
≠
Domain-valid
```

Un actor autorizado todavía puede recibir rechazo por:

* estado inválido;
* invariante;
* referencia inválida;
* organización incorrecta;
* conflicto de Version.

---

# Validación de referencias

La capa Application debe poder validar las referencias externas necesarias sin incorporar los Aggregates referenciados dentro de Participation.

Conceptualmente:

```text
RegisterParticipation
        │
        ├── validate Organization
        ├── validate participant references
        └── validate contextual references
                │
                ▼
        Participation.register(...)
```

La validación externa no debe trasladar comportamiento de Organization, Citizen, Membership, Territory, Assembly, Proposal o Voting a Participation.

---

# Invariantes incluidas en VS-001

Como mínimo:

## Identidad

```text
ParticipationId valid
ParticipationId unique
ParticipationId immutable
```

## Organización

```text
OrganizationId required
OrganizationId valid
OrganizationId immutable
```

## Actor

Debe existir un actor válido según el contexto de Participation.

VS-001 no redefine la cardinalidad documental de `CitizenId` y `MembershipId`.

## Tipo

```text
ParticipationType valid
```

## Contexto

El contexto requerido para el tipo concreto debe ser válido.

## Estado inicial

```text
new Participation
→ Registered
```

## Activación

Sólo:

```text
Registered → Active
```

es aceptada por `ActivateParticipation`.

## Temporalidad

Debe mantenerse:

```text
CreatedAt <= StartedAt
```

cuando exista `StartedAt`.

Una Participation `Registered` no debe contener timestamps de lifecycle futuros.

## Version

```text
RegisterParticipation → Version 1
ActivateParticipation → Version 2
```

## Rechazo

Toda operación rechazada debe producir:

```text
State unchanged
Version unchanged
Lifecycle timestamps unchanged
No success Domain Event
```

---

# Versioning

VS-001 establece explícitamente:

```text
Creation
    ↓
Version = 1
```

y:

```text
Registered
Version = 1
    │
    │ ActivateParticipation
    ▼
Active
Version = 2
```

Toda mutación válida incrementa Version exactamente una vez.

No debe ocurrir:

```text
one command
→ multiple Version increments
```

---

# ExpectedVersion

`ActivateParticipation` debe utilizar concurrencia optimista.

Debe cumplirse:

```text
ExpectedVersion = PersistedVersion
```

antes de confirmar la modificación.

Ejemplo válido:

```text
PersistedVersion = 1
ExpectedVersion  = 1

→ activate
→ Version = 2
```

Ejemplo rechazado:

```text
PersistedVersion = 2
ExpectedVersion  = 1

→ Version conflict
→ no mutation
```

---

# Repository Contract

VS-001 utilizará conceptualmente:

```text
ParticipationRepository

getById()
exists()
save(... ExpectedVersion)
```

## RegisterParticipation

Debe comprobar:

```text
exists(ParticipationId) = false
```

antes de confirmar la creación.

## ActivateParticipation

Debe:

```text
getById(ParticipationId)
```

y posteriormente persistir respetando:

```text
ExpectedVersion
```

El Repository no puede ejecutar comportamiento de dominio.

---

# Participación inexistente

`ActivateParticipation` sobre una identidad inexistente debe ser rechazado como ausencia del Aggregate.

El Application Service debe distinguir este caso de:

```text
Invalid Participation State
```

porque representan causas diferentes.

---

# Domain Events incluidos

## ParticipationRegistered

Debe producirse únicamente después de una creación válida.

Datos conceptuales mínimos:

```text
EventId

ParticipationId

OrganizationId

ParticipationType

OccurredAt

AggregateVersion

CorrelationId

CausationId
```

y, cuando corresponda:

```text
CitizenId
MembershipId
AssemblyId
ProposalId
TerritoryId
ActorId
```

Para VS-001:

```text
AggregateVersion = 1
```

---

## ParticipationActivated

Debe producirse únicamente después de:

```text
Registered → Active
```

Datos conceptuales:

```text
EventId

ParticipationId

OrganizationId

StartedAt

OccurredAt

ActorId

AggregateVersion

CorrelationId

CausationId
```

Para VS-001:

```text
AggregateVersion = 2
```

---

# Domain Event identity

`EventId` debe permanecer separado de:

```text
ParticipationId
CommandId
CorrelationId
CausationId
```

No debe reutilizarse alguno de estos identificadores como sustituto implícito de otro.

---

# Integration Events incluidos

VS-001 incluye:

```text
ParticipationRegisteredIntegrationEvent
ParticipationActivatedIntegrationEvent
```

No cambiarán de nombre a:

```text
ParticipationRegisteredForIntegration
ParticipationActivatedForIntegration
```

porque ese patrón no pertenece al contrato propietario de DOMAIN-008.

---

# Envelope de Integration Events

Los Integration Events de VS-001 deben respetar:

```text
EventId
EventType
EventVersion
AggregateId
AggregateType
AggregateVersion
OccurredAt
CorrelationId
CausationId
Payload
```

Para Participation:

```text
AggregateType = Participation
AggregateId   = ParticipationId
```

Debe mantenerse:

```text
EventVersion
≠
AggregateVersion
```

VS-001 no introducirá:

```text
PublishedAt
```

porque DOMAIN-008 no lo declara como parte de su contrato propietario.

---

# Mapping de integración

Debe existir una transformación explícita:

```text
ParticipationRegistered
        ↓
Integration Mapping
        ↓
ParticipationRegisteredIntegrationEvent
```

y:

```text
ParticipationActivated
        ↓
Integration Mapping
        ↓
ParticipationActivatedIntegrationEvent
```

No debe existir conversión genérica automática de cualquier Domain Event.

---

# Confirmación antes de integración

El orden conceptual obligatorio será:

```text
Command
    ↓
Participation
    ↓
Domain Event
    ↓
Repository Save
    ↓
Commit
    ↓
Integration Mapping
    ↓
Integration Event
```

Un Command rechazado no produce Integration Event.

Un fallo de publicación externo no debe revertir el estado confirmado de Participation.

---

# Payload mínimo

`ParticipationRegisteredIntegrationEvent` deberá comunicar como mínimo la información necesaria para identificar:

```text
ParticipationId
OrganizationId
ParticipationType
context required by contract
AggregateVersion
OccurredAt
```

`ParticipationActivatedIntegrationEvent` deberá comunicar como mínimo:

```text
ParticipationId
OrganizationId
AggregateVersion
OccurredAt
```

El Aggregate completo no debe serializarse como Payload.

---

# Application Services incluidos

VS-001 requiere conceptualmente dos casos de aplicación:

```text
RegisterParticipationService
ActivateParticipationService
```

Sus responsabilidades serán coordinar, no contener reglas propias del Aggregate.

## RegisterParticipationService

Responsabilidades conceptuales:

```text
authorize Participation.Register

validate external references

ensure identity does not exist

construct/register Participation

persist Aggregate

publish confirmed Domain Event

map/publish eligible Integration Event
```

## ActivateParticipationService

Responsabilidades conceptuales:

```text
authorize Participation.Activate

load Participation

validate external context when required

execute activate()

persist using ExpectedVersion

publish confirmed Domain Event

map/publish eligible Integration Event
```

---

# Orden de responsabilidades

Debe mantenerse:

```text
Application
    │
    ├── authorization
    ├── reference validation
    ├── repository coordination
    └── integration coordination
          │
          ▼
Domain
    │
    ├── identity
    ├── state
    ├── lifecycle
    ├── invariants
    ├── timestamps
    ├── version
    └── domain events
```

Application no debe reconstruir la State Machine fuera del Aggregate.

---

# Puertos mínimos

VS-001 necesitará conceptualmente puertos para:

```text
ParticipationRepository

Authorization

ReferenceValidation

DomainEventPublication

IntegrationEventPublication
```

La denominación técnica concreta se resolverá durante el diseño de archivos, preservando los patrones ya utilizados en AURA Core.

---

# Infrastructure mínima

La implementación de VS-001 puede proporcionar adaptadores de prueba/in-memory necesarios para demostrar:

```text
repository behavior
authorization behavior
reference validation
event publication
```

No forman parte del alcance:

```text
PostgreSQL
MongoDB
HTTP API
FIWARE
NGSI-LD
message broker
real Outbox infrastructure
```

salvo infraestructura transversal que ya exista y sea obligatoria en el repositorio.

---

# Consistency Boundary

Cada operación modifica exactamente:

```text
One Participation Aggregate
```

No debe existir:

```text
RegisterParticipation
    ↓
modify Membership
    +
modify Assembly
    +
modify Proposal
```

Las referencias externas sólo se validan.

No se modifican.

---

# Atomicidad

En una mutación válida deben mantenerse conjuntamente:

```text
State
Lifecycle Timestamp
Version
Domain Event
```

Ejemplo de Activation:

```text
Status = Active
StartedAt defined
Version = 2
ParticipationActivated.AggregateVersion = 2
```

No puede persistirse un estado parcial.

---

# Escenarios mínimos obligatorios

VS-001 debe cubrir mediante tests, como mínimo:

## RegisterParticipation

```text
1. valid registration
2. invalid ParticipationId
3. missing OrganizationId
4. invalid ParticipationType
5. duplicate ParticipationId
6. permission denied
7. invalid required context/reference
```

Para un registro rechazado:

```text
no Aggregate
no valid Version
no ParticipationRegistered
no Integration Event
```

---

## ActivateParticipation

Debe cubrir:

```text
1. valid Registered → Active
2. activation from Active rejected
3. activation from Completed rejected
4. activation from Withdrawn rejected
5. activation from Invalidated rejected
6. activation from Archived rejected
7. permission denied
8. Organization mismatch
9. ExpectedVersion conflict
10. Participation not found
11. invalid required contextual condition
```

En todos los rechazos:

```text
State unchanged
Version unchanged
StartedAt unchanged
No ParticipationActivated
No ParticipationActivatedIntegrationEvent
```

---

# Persistencia y publicación

Debe demostrarse que un Integration Event elegible no sea tratado como hecho confirmado antes de persistir exitosamente el Aggregate.

Conceptualmente:

```text
Aggregate Mutation
    ↓
save
    ↓
commit confirmed
    ↓
Integration Event
```

No:

```text
Integration Event
    ↓
attempt save
```

---

# Read Side

VS-001 no requiere implementar el Read Model completo de DOMAIN-008L.

Puede devolver un resultado de aplicación suficiente para confirmar la operación, pero no debe crear prematuramente:

```text
ParticipationSummary
ParticipationStatistics
ParticipationByTerritory
...
```

como parte del slice si no son necesarios para demostrar Register/Activate.

---

# Out of Scope

Queda explícitamente fuera de VS-001:

```text
CompleteParticipation

WithdrawParticipation

InvalidateParticipation

ArchiveParticipation

ChangeParticipationType

ChangeParticipationContext

UpdateParticipationMetadata

ParticipationCompleted

ParticipationWithdrawn

ParticipationInvalidated

ParticipationArchived

ParticipationTypeChanged

ParticipationContextChanged

ParticipationMetadataUpdated
```

y sus Integration Events correspondientes.

También quedan fuera:

```text
REST API
database-specific repository
FIWARE adapter
NGSI-LD mapping
real message broker
distributed consumer implementation
full Read Model
analytics
Notification consumer
Audit consumer
```

---

# No decisiones nuevas permitidas

Durante VS-001 no se deberá introducir de forma implícita:

```text
exactly-one-of CitizenId/MembershipId

PublishedAt

*ForIntegration naming

automatic DomainEvent → IntegrationEvent mapping

generic UpdateParticipation

ReactivateParticipation

RestoreParticipation

DeleteParticipation
```

Cualquiera de estas decisiones requeriría evolución documental previa.

---

# Estructura arquitectónica esperada

Sin crear todavía archivos, el slice deberá respetar:

```text
src/arada_core/participation/
├── domain/
├── application/
├── infrastructure/
└── interfaces/
```

siguiendo el mismo criterio arquitectónico ya consolidado para AURA Core.

La estructura concreta de archivos se definirá antes de implementación para evitar crear módulos innecesarios.

---

# Secuencia funcional completa

## Registro

```text
RegisterParticipation
        │
        ▼
Authorization
        │
        ▼
Reference Validation
        │
        ▼
Duplicate Identity Check
        │
        ▼
Participation.register(...)
        │
        ├── Status = Registered
        ├── CreatedAt
        ├── Version = 1
        └── ParticipationRegistered
        │
        ▼
Repository Save
        │
        ▼
Commit
        │
        ▼
ParticipationRegisteredIntegrationEvent
```

---

## Activación

```text
ActivateParticipation
        │
        ▼
Authorization
        │
        ▼
Repository.getById
        │
        ▼
Organization / Context Validation
        │
        ▼
ExpectedVersion Validation
        │
        ▼
Participation.activate(...)
        │
        ├── Registered → Active
        ├── StartedAt
        ├── Version 1 → 2
        └── ParticipationActivated
        │
        ▼
Repository Save
        │
        ▼
Commit
        │
        ▼
ParticipationActivatedIntegrationEvent
```

---

# Criterios de aceptación de VS-001

VS-001 podrá considerarse completo únicamente cuando quede demostrado que:

```text
[ ] Participation puede registrarse válidamente.

[ ] El estado inicial es Registered.

[ ] La Version inicial es 1.

[ ] CreatedAt se establece correctamente.

[ ] ParticipationRegistered se produce exactamente una vez.

[ ] Una identidad duplicada es rechazada.

[ ] OrganizationId es obligatorio e inmutable.

[ ] ParticipationType inválido es rechazado.

[ ] Actor/contexto inválido requerido es rechazado.

[ ] Participation.Register es exigido.

[ ] Registered puede transicionar a Active.

[ ] Ningún otro estado puede ejecutar ActivateParticipation.

[ ] StartedAt se establece al activar.

[ ] Version pasa exactamente de 1 a 2.

[ ] ParticipationActivated se produce exactamente una vez.

[ ] Participation.Activate es exigido.

[ ] ExpectedVersion protege la activación concurrente.

[ ] Un Command rechazado no modifica estado.

[ ] Un Command rechazado no modifica Version.

[ ] Un Command rechazado no modifica timestamps.

[ ] Un Command rechazado no produce Domain Event de éxito.

[ ] Repository persiste el Aggregate completo.

[ ] Ningún Aggregate externo se incorpora al Consistency Boundary.

[ ] Domain Events permanecen separados de Integration Events.

[ ] ParticipationRegisteredIntegrationEvent respeta DOMAIN-008K.

[ ] ParticipationActivatedIntegrationEvent respeta DOMAIN-008K.

[ ] EventVersion permanece separado de AggregateVersion.

[ ] EventId permanece separado de AggregateId y metadata de trazabilidad.

[ ] No se introduce PublishedAt.

[ ] Integration Event sólo representa un hecho confirmado.

[ ] Ninguna funcionalidad fuera del slice se implementa accidentalmente.
```

---

# Quality Gates

La implementación sólo podrá considerarse cerrada después de superar:

```text
ruff check src tests
```

```text
mypy src
```

y únicamente después:

```text
python3 -m pytest -q
```

No se realizará commit hasta que los tres gates hayan sido verificados.

---

# Definición formal final

```text
PARTICIPATION VS-001

Scope:
    RegisterParticipation
    ActivateParticipation

State Coverage:
    Nonexistent
        ↓
    Registered
        ↓
    Active

Domain Events:
    ParticipationRegistered
    ParticipationActivated

Integration Events:
    ParticipationRegisteredIntegrationEvent
    ParticipationActivatedIntegrationEvent

Permissions:
    Participation.Register
    Participation.Activate

Version:
    Registration = 1
    Activation   = 2

Repository:
    getById()
    exists()
    save(... ExpectedVersion)

Consistency:
    One Participation Aggregate per mutation

External Aggregates:
    referenced and validated only

Out of Scope:
    Complete
    Withdraw
    Invalidate
    Archive
    ChangeType
    ChangeContext
    UpdateMetadata
```

## Veredicto

**Participation VS-001 queda formalmente definido como el slice `RegisterParticipation → ActivateParticipation`.**

Es suficientemente pequeño para mantener control arquitectónico y suficientemente completo para validar el patrón vertical de DOMAIN-008: identidad, ownership organizacional, actor/contexto, autorización, invariantes, State Machine, temporalidad, Versioning, concurrencia, Repository, Domain Events e Integration Events.

No requiere ninguna nueva decisión semántica para comenzar su diseño técnico.
