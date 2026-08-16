# DOMAIN-013H — Integration Examples

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Integration Management

Aggregate:
Integration

Autor:
ARADA

Documentos Relacionados:

- DOMAIN-013-Aggregate.md
- DOMAIN-013A-Lifecycle.md
- DOMAIN-013B-State-Machine.md
- DOMAIN-013C-Commands.md
- DOMAIN-013D-Domain-Events.md
- DOMAIN-013E-Invariants.md
- DOMAIN-013F-Permissions.md
- DOMAIN-013G-Repository-Contract.md
- DOMAIN-013I-Versioning.md
- DOMAIN-013J-Consistency-Boundary.md
- DOMAIN-013K-Integration-Events.md
- DOMAIN-013L-Read-Model.md
- DOMAIN-013M-Test-Scenarios.md
- DOMAIN-013N-Performance-Rules.md
- DOMAIN-013O-Security-Model.md
- DOMAIN-013P-Extension-Points.md

---

# Objetivo

Este documento presenta ejemplos conceptuales del Aggregate
**Integration**.

Los ejemplos tienen como propósito ilustrar las reglas ya definidas
en:

```text
DOMAIN-013-Aggregate.md

DOMAIN-013A-Lifecycle.md

DOMAIN-013B-State-Machine.md

DOMAIN-013C-Commands.md

DOMAIN-013D-Domain-Events.md

DOMAIN-013E-Invariants.md

DOMAIN-013F-Permissions.md

DOMAIN-013G-Repository-Contract.md
```

Los ejemplos no introducen:

- nuevos estados;
- nuevas transiciones;
- nuevos Commands;
- nuevos Domain Events;
- nuevas Permissions;
- nuevas Invariants;
- nuevas políticas de persistencia;
- nuevas decisiones de arquitectura.

---

# Principio Fundamental

Debe mantenerse:

```text
Example

≠

New Domain Rule
```

Un ejemplo solamente demuestra el comportamiento ya definido.

---

# Lifecycle Oficial Utilizado

Todos los ejemplos respetan:

```text
No Integration
      │
      ▼
    Draft
      │
      ├──────────────► Archived
      │
      ▼
    Active
      │
      ├──────────────► Archived
      │
      ▼
  Suspended
      │
      ├──────────────► Active
      │
      └──────────────► Archived
```

---

# Commands Oficiales Utilizados

Los únicos Commands utilizados son:

```text
CreateIntegration

ActivateIntegration

SuspendIntegration

ReactivateIntegration

ArchiveIntegration
```

---

# Domain Events Oficiales Utilizados

Los únicos Domain Events utilizados son:

```text
IntegrationCreated

IntegrationActivated

IntegrationSuspended

IntegrationReactivated

IntegrationArchived
```

---

# Permissions Oficiales Utilizadas

Los ejemplos utilizan únicamente:

```text
Integration.Create

Integration.Activate

Integration.Suspend

Integration.Reactivate

Integration.Archive
```

cuando corresponda.

---

# Ejemplo 1 — Creación de Integration

Estado inicial:

```text
No Integration
```

Intención:

```text
CreateIntegration
```

Permission requerida:

```text
Integration.Create
```

Resultado válido:

```text
State = Draft
```

Domain Event:

```text
IntegrationCreated
```

---

# Ejemplo 1 — Flujo Conceptual

```text
No Integration
      │
      │ CreateIntegration
      ▼
    Draft
      │
      ▼
IntegrationCreated
```

---

# Ejemplo 1 — Identidad

Supóngase:

```text
IntegrationId = INT-001
```

Después de la creación:

```text
IntegrationId = INT-001

State = Draft

Version = Initial Version
```

IntegrationId permanece inmutable.

---

# Ejemplo 1 — Resultado de Repository

Después de creación válida:

```text
save(Integration)
```

puede persistir:

```text
IntegrationId = INT-001

State = Draft

Version = Initial Version
```

El Repository no crea el estado Draft.

El estado fue producido por comportamiento válido del Aggregate.

---

# Ejemplo 2 — Creación Duplicada

Estado persistido:

```text
IntegrationId = INT-001

State = Draft
```

Nueva intención:

```text
CreateIntegration(
    IntegrationId = INT-001
)
```

Resultado:

```text
Rejected
```

No debe existir una segunda Integration con:

```text
IntegrationId = INT-001
```

---

# Ejemplo 2 — No Domain Event

La creación duplicada no produce:

```text
IntegrationCreated
```

como nuevo hecho válido.

---

# Ejemplo 3 — Activación

Estado inicial:

```text
State = Draft
```

Command:

```text
ActivateIntegration
```

Permission:

```text
Integration.Activate
```

Resultado:

```text
State = Active
```

Domain Event:

```text
IntegrationActivated
```

---

# Ejemplo 3 — Flujo

```text
Draft
  │
  │ ActivateIntegration
  ▼
Active
  │
  ▼
IntegrationActivated
```

---

# Ejemplo 3 — Version

Si antes del Command:

```text
Version = N
```

después de una activación válida:

```text
Version = N + 1
```

conforme al contrato de Versioning.

---

# Ejemplo 4 — Activación desde Estado Incorrecto

Estado:

```text
Active
```

Command:

```text
ActivateIntegration
```

Resultado:

```text
Rejected
```

Debe mantenerse:

```text
State = Active

Version unchanged

UpdatedAt unchanged
```

No existe un nuevo:

```text
IntegrationActivated
```

---

# Ejemplo 5 — Permission no Sustituye State Machine

Estado:

```text
Suspended
```

Permission:

```text
Integration.Activate
```

Command:

```text
ActivateIntegration
```

Resultado:

```text
Rejected
```

Aunque la intención esté autorizada, la transición:

```text
Suspended → Active
```

corresponde a:

```text
ReactivateIntegration
```

y no a ActivateIntegration.

---

# Ejemplo 6 — Suspensión

Estado inicial:

```text
State = Active
```

Command:

```text
SuspendIntegration
```

Permission:

```text
Integration.Suspend
```

Resultado:

```text
State = Suspended
```

Domain Event:

```text
IntegrationSuspended
```

---

# Ejemplo 6 — Flujo

```text
Active
  │
  │ SuspendIntegration
  ▼
Suspended
  │
  ▼
IntegrationSuspended
```

---

# Ejemplo 7 — Suspensión no es Fallo Técnico

Estado:

```text
State = Active
```

Condición técnica:

```text
External Endpoint = Unavailable
```

Resultado de dominio:

```text
State remains Active
```

No se ejecuta automáticamente:

```text
SuspendIntegration
```

y no se produce:

```text
IntegrationSuspended
```

---

# Ejemplo 8 — Timeout

Estado:

```text
State = Active
```

Ocurre:

```text
HTTP Timeout
```

Resultado:

```text
Integration remains Active
```

Debe mantenerse:

```text
Timeout

≠

Domain Suspension
```

---

# Ejemplo 9 — Fallo de Broker

Estado:

```text
State = Active
```

Condición:

```text
Broker = Unavailable
```

Resultado:

```text
State remains Active
```

No existe transición automática:

```text
Active → Suspended
```

---

# Ejemplo 10 — Fallo de FIWARE

Estado:

```text
State = Active
```

Condición externa:

```text
FIWARE Context Broker = Unavailable
```

Resultado del Aggregate:

```text
State = Active
```

No se produce automáticamente:

```text
IntegrationSuspended
```

---

# Ejemplo 11 — Fallo de Sistema Municipal

Estado:

```text
State = Active
```

Condición:

```text
Municipal System = Unavailable
```

Resultado:

```text
Integration State remains Active
```

La disponibilidad externa no determina el Lifecycle.

---

# Ejemplo 12 — Reactivación

Estado inicial:

```text
State = Suspended
```

Command:

```text
ReactivateIntegration
```

Permission:

```text
Integration.Reactivate
```

Resultado:

```text
State = Active
```

Domain Event:

```text
IntegrationReactivated
```

---

# Ejemplo 12 — Flujo

```text
Suspended
    │
    │ ReactivateIntegration
    ▼
  Active
    │
    ▼
IntegrationReactivated
```

---

# Ejemplo 13 — Recuperación Técnica no Reactiva

Estado:

```text
State = Suspended
```

Condición:

```text
External System becomes available
```

Resultado:

```text
State remains Suspended
```

Debe existir una intención formal:

```text
ReactivateIntegration
```

para realizar:

```text
Suspended → Active
```

---

# Ejemplo 14 — Archivado desde Draft

Estado:

```text
State = Draft
```

Command:

```text
ArchiveIntegration
```

Permission:

```text
Integration.Archive
```

Resultado:

```text
State = Archived
```

Domain Event:

```text
IntegrationArchived
```

---

# Ejemplo 14 — Flujo

```text
Draft
  │
  │ ArchiveIntegration
  ▼
Archived
  │
  ▼
IntegrationArchived
```

---

# Ejemplo 15 — Archivado desde Active

Estado:

```text
State = Active
```

Command:

```text
ArchiveIntegration
```

Resultado:

```text
State = Archived
```

Domain Event:

```text
IntegrationArchived
```

---

# Ejemplo 16 — Archivado desde Suspended

Estado:

```text
State = Suspended
```

Command:

```text
ArchiveIntegration
```

Resultado:

```text
State = Archived
```

Domain Event:

```text
IntegrationArchived
```

---

# Ejemplo 17 — Archivado no es Eliminación

Estado después del Command:

```text
State = Archived

IntegrationId = INT-001
```

Debe mantenerse:

```text
IntegrationId remains INT-001
```

y:

```text
Archived

≠

Physically Deleted
```

---

# Ejemplo 18 — Intento de Reactivar Archived

Estado:

```text
State = Archived
```

Command:

```text
ReactivateIntegration
```

incluso con:

```text
Permission = Integration.Reactivate
```

resultado:

```text
Rejected
```

---

# Ejemplo 18 — Resultado Inmutable

Debe mantenerse:

```text
State = Archived

Version unchanged

UpdatedAt unchanged
```

No se produce:

```text
IntegrationReactivated
```

---

# Ejemplo 19 — ArchiveIntegration sobre Archived

Estado:

```text
Archived
```

Command:

```text
ArchiveIntegration
```

Resultado:

```text
Rejected
```

No existe:

```text
Archived → Archived
```

como transición de Lifecycle.

---

# Ejemplo 20 — Flujo Completo Válido

Una Integration puede evolucionar conceptualmente:

```text
No Integration
      │
      │ CreateIntegration
      ▼
    Draft
      │
      │ ActivateIntegration
      ▼
    Active
      │
      │ SuspendIntegration
      ▼
  Suspended
      │
      │ ReactivateIntegration
      ▼
    Active
      │
      │ ArchiveIntegration
      ▼
  Archived
```

---

# Ejemplo 20 — Eventos Correspondientes

La misma evolución produce:

```text
IntegrationCreated

IntegrationActivated

IntegrationSuspended

IntegrationReactivated

IntegrationArchived
```

cada uno asociado a la Version resultante correspondiente.

---

# Ejemplo 21 — Flujo Corto Válido

Una Integration puede no activarse nunca.

Flujo:

```text
No Integration
      │
      ▼
    Draft
      │
      ▼
  Archived
```

Commands:

```text
CreateIntegration

ArchiveIntegration
```

Events:

```text
IntegrationCreated

IntegrationArchived
```

---

# Ejemplo 22 — No Toda Integration Debe Suspenderse

Un flujo igualmente válido es:

```text
No Integration
      │
      ▼
    Draft
      │
      ▼
    Active
      │
      ▼
  Archived
```

No existe obligación de transitar por Suspended.

---

# Ejemplo 23 — Versionado

Supóngase:

```text
CreateIntegration
```

establece la Version inicial.

Posteriormente:

```text
ActivateIntegration
```

produce:

```text
Version = PreviousVersion + 1
```

Después:

```text
SuspendIntegration
```

produce nuevamente:

```text
Version = PreviousVersion + 1
```

Cada modificación válida mantiene su propia evolución lógica.

---

# Ejemplo 24 — Rechazo no Incrementa Version

Estado:

```text
State = Draft

Version = N
```

Command inválido:

```text
SuspendIntegration
```

Resultado:

```text
Rejected

State = Draft

Version = N

UpdatedAt unchanged
```

---

# Ejemplo 25 — ConcurrencyConflict

Estado persistido:

```text
IntegrationId = INT-001

Version = 5
```

Una operación intenta persistir con:

```text
ExpectedVersion = 4
```

Resultado:

```text
ConcurrencyConflict
```

No se debe sobrescribir:

```text
Version = 5
```

---

# Ejemplo 25 — No Domain Event de Éxito

Si la modificación no se confirma debido a:

```text
ConcurrencyConflict
```

no debe tratarse como confirmado un nuevo Domain Event de éxito.

---

# Ejemplo 26 — Concurrencia Válida

Estado persistido:

```text
Version = 5
```

Operación válida:

```text
ExpectedVersion = 5
```

Aggregate modificado válidamente:

```text
Version = 6
```

El Repository puede confirmar la persistencia si las demás reglas son
satisfechas.

---

# Ejemplo 27 — Permission Denied

Estado:

```text
State = Draft

Version = N
```

Command:

```text
ActivateIntegration
```

Permission:

```text
Denied
```

Resultado:

```text
Rejected

State = Draft

Version = N

UpdatedAt unchanged
```

No se produce:

```text
IntegrationActivated
```

---

# Ejemplo 28 — Permission Granted pero Invariant Inválida

Permission:

```text
Integration.Activate = Allowed
```

Si una Invariant necesaria para la operación no se cumple:

```text
ActivateIntegration

=

Rejected
```

Debe mantenerse:

```text
Authorized

≠

Automatically Valid
```

---

# Ejemplo 29 — ActorId no es Permission

Un Command puede estar asociado conceptualmente a:

```text
ActorId = ACTOR-001
```

Esto no implica:

```text
ActorId = Authorized
```

La autorización debe resolverse independientemente.

---

# Ejemplo 30 — Requester y ActorId

Puede existir conceptualmente:

```text
Requester = SERVICE-001

ActorId = ACTOR-001
```

cuando el contrato correspondiente así lo permita.

No debe inferirse que ambos identificadores representan
obligatoriamente la misma entidad.

---

# Ejemplo 31 — CorrelationId

Una secuencia puede compartir:

```text
CorrelationId = CORR-001
```

por ejemplo:

```text
CreateIntegration

IntegrationCreated

ActivateIntegration

IntegrationActivated
```

cuando el flujo correspondiente preserve dicha correlación.

---

# Ejemplo 31 — Correlation no Comparte Boundary

Compartir:

```text
CorrelationId = CORR-001
```

con otro Aggregate no significa:

```text
Shared Aggregate

Shared Version

Shared Transaction
```

---

# Ejemplo 32 — CausationId

Cuando una intención se origine en un hecho previo reconocido:

```text
CausationId = EVENT-X
```

puede conservarse para trazabilidad.

CausationId no autoriza por sí mismo la modificación.

---

# Ejemplo 33 — Domain Event

Un evento conceptual puede representarse mediante:

```text
EventId

EventType = IntegrationActivated

IntegrationId = INT-001

AggregateVersion = N

OccurredAt

CorrelationId

CausationId

Payload
```

CorrelationId y CausationId solamente están presentes cuando
corresponda.

---

# Ejemplo 34 — EventId Diferente de IntegrationId

Supóngase:

```text
IntegrationId = INT-001

EventId = EVT-010
```

Debe mantenerse:

```text
INT-001

≠

EVT-010
```

---

# Ejemplo 35 — AggregateVersion

Si:

```text
Integration.Version = 4
```

después de una transición válida, el Domain Event correspondiente
debe representar:

```text
AggregateVersion = 4
```

---

# Ejemplo 36 — Contract Version no es AggregateVersion

Puede existir conceptualmente:

```text
Integration.Version = 7

Integration Contract Version = 3
```

sin contradicción.

Debe mantenerse:

```text
7

≠

3
```

como conceptos semánticamente independientes.

---

# Ejemplo 37 — External System Version

Puede existir:

```text
Integration.Version = 5

External System Version = 21
```

No existe una relación aritmética necesaria entre ambas.

---

# Ejemplo 38 — Payload Mínimo

Para:

```text
IntegrationSuspended
```

un Payload conceptual puede preservar:

```text
IntegrationId

PreviousState = Active

NewState = Suspended
```

y solamente información adicional formalmente necesaria.

No debe incluir automáticamente:

```text
Full External Payload
```

---

# Ejemplo 39 — External Payload no es Aggregate State

Mensaje recibido:

```text
{
    external_status,
    provider_metadata,
    technical_error,
    payload
}
```

no significa que toda esa información pase a formar parte de:

```text
Integration
```

Solamente conceptos explícitamente reconocidos por el dominio pueden
incorporarse conforme a sus contratos.

---

# Ejemplo 40 — Datos Ausentes

Si un contrato no proporciona:

```text
CorrelationId
```

no debe fabricarse uno como supuesto dato histórico del hecho.

---

# Ejemplo 41 — Credenciales Excluidas

Un evento o Aggregate no debe incorporar:

```text
AccessToken = ...

ClientSecret = ...

PrivateKey = ...
```

como estado de dominio.

---

# Ejemplo 42 — Integration no es HTTP Client

Una Integration:

```text
IntegrationId = INT-001

State = Active
```

no implica que el Aggregate contenga:

```text
HttpClient

ConnectionPool

EndpointSession
```

---

# Ejemplo 43 — Integration no es Broker Connection

Una Integration Active no requiere que su State sea:

```text
Connected
```

Debe mantenerse:

```text
Active

≠

Connected
```

---

# Ejemplo 44 — Integration no es FIWARE Entity

Puede existir interoperabilidad con FIWARE.

Sin embargo:

```text
Integration

≠

FIWARE Entity
```

y:

```text
IntegrationId

≠

FIWARE Entity Id
```

salvo coincidencia accidental de representación, que no altera la
diferencia conceptual.

---

# Ejemplo 45 — Integration con Sistema Municipal

Conceptualmente:

```text
AURA
  │
  ▼
Integration
  │
  ▼
Explicit Contract
  │
  ▼
Municipal System
```

La Integration representa la relación reconocida por AURA.

El sistema municipal permanece fuera del Aggregate.

---

# Ejemplo 45 — Sin Ownership Municipal

La Integration no incorpora:

```text
Municipal Aggregate

Municipal Database

Municipal User

Municipal Internal State
```

dentro de su Consistency Boundary.

---

# Ejemplo 46 — Integration con FIWARE

Conceptualmente:

```text
AURA Domain
    │
    ▼
Integration Boundary
    │
    ▼
Explicit Contract
    │
    ▼
FIWARE
```

Esto no significa:

```text
AURA Domain Model

=

FIWARE Data Model
```

---

# Ejemplo 47 — NGSI-LD Externo al Aggregate

Un contrato externo puede utilizar:

```text
NGSI-LD
```

para materializar interoperabilidad.

El Aggregate no se redefine automáticamente mediante tipos,
propiedades o relaciones NGSI-LD.

---

# Ejemplo 48 — External State

Sistema externo:

```text
status = OFFLINE
```

Integration:

```text
State = Active
```

Esta combinación es conceptualmente posible.

Debe mantenerse:

```text
OFFLINE

≠

Suspended
```

---

# Ejemplo 49 — External ENABLED no es Active

Sistema externo:

```text
status = ENABLED
```

Integration:

```text
State = Draft
```

La Integration no pasa automáticamente a Active.

---

# Ejemplo 50 — External DISABLED no es Suspended

Sistema externo:

```text
status = DISABLED
```

Integration:

```text
State = Active
```

No existe transición automática.

---

# Ejemplo 51 — External Message no es Command

Mensaje entrante:

```text
"activate"
```

no equivale automáticamente a:

```text
ActivateIntegration
```

El mensaje debe atravesar el contrato correspondiente y convertirse en
una intención válida antes de alcanzar el Aggregate.

---

# Ejemplo 52 — External Integration Event no Modifica Directamente

Un Integration Event externo puede ser recibido.

Debe mantenerse:

```text
External Integration Event
    │
    ▼
Contract Interpretation
    │
    ▼
Valid Domain Intent
    │
    ▼
Integration
```

No:

```text
External Integration Event
    │
    ▼
setState()
```

---

# Ejemplo 53 — Domain Event de Otro Aggregate

Supóngase:

```text
AssemblyCompleted
```

ocurre en Assembly.

Integration puede participar posteriormente en una coordinación
contractual.

Sin embargo:

```text
AssemblyCompleted

≠

Integration Command
```

y:

```text
AssemblyCompleted

≠

Integration State Change
```

---

# Ejemplo 54 — Source Domain Event Mantiene Ownership

Un evento:

```text
VotingCompleted
```

continúa perteneciendo al Aggregate Voting.

Integration no lo convierte en un Domain Event propio.

---

# Ejemplo 55 — Domain Event versus Integration Event

Hecho interno:

```text
IntegrationActivated
```

es un Domain Event.

Debe mantenerse:

```text
IntegrationActivated

≠

Mandatory Integration Event
```

No existe obligación automática de publicarlo externamente.

---

# Ejemplo 56 — Publicación Externa Opcional por Contrato

Puede existir:

```text
IntegrationActivated
```

sin que ningún consumidor externo necesite dicho hecho.

En ese caso:

```text
No Integration Event required by this example
```

---

# Ejemplo 57 — Fallo de Publicación

Estado confirmado:

```text
State = Active
```

Domain Event confirmado:

```text
IntegrationActivated
```

Posteriormente ocurre:

```text
External Publication Failure
```

Resultado:

```text
Integration remains Active
```

---

# Ejemplo 58 — Retry de Publicación

Una retransmisión técnica posterior no produce:

```text
IntegrationActivated
```

nuevamente como nuevo hecho.

Debe mantenerse:

```text
Technical Retry

≠

New Domain Fact
```

---

# Ejemplo 59 — Repository save()

Aggregate válido:

```text
IntegrationId = INT-001

State = Active

Version = 2
```

Operación:

```text
save(Integration)
```

El Repository persiste el estado.

No ejecuta:

```text
ActivateIntegration
```

---

# Ejemplo 60 — findById()

Persistencia:

```text
IntegrationId = INT-001

State = Suspended

Version = 5
```

Operación:

```text
findById(INT-001)
```

Resultado:

```text
IntegrationId = INT-001

State = Suspended

Version = 5
```

---

# Ejemplo 60 — Sin Modificación por Lectura

`findById()` no produce:

```text
Version = 6
```

ni:

```text
IntegrationSuspended
```

nuevamente.

---

# Ejemplo 61 — exists()

Si:

```text
IntegrationId = INT-001
```

existe:

```text
exists(INT-001)

=

true
```

La operación no modifica el Aggregate.

---

# Ejemplo 62 — IntegrationNotFound

Si:

```text
IntegrationId = INT-404
```

no existe:

```text
findById(INT-404)

→

IntegrationNotFound
```

Esto no crea:

```text
State = Failed
```

---

# Ejemplo 63 — nextIdentity()

Operación:

```text
nextIdentity()
```

puede proporcionar conceptualmente:

```text
IntegrationId = INT-002
```

Esto no crea todavía:

```text
Integration INT-002
```

---

# Ejemplo 64 — delete() no es ArchiveIntegration

Repository Contract:

```text
delete()
```

Domain Command:

```text
ArchiveIntegration
```

Debe mantenerse:

```text
delete()

≠

ArchiveIntegration
```

---

# Ejemplo 65 — Archived no Ejecuta delete()

Después de:

```text
ArchiveIntegration
```

resultado:

```text
State = Archived
```

No debe inferirse automáticamente:

```text
Repository.delete()
```

---

# Ejemplo 66 — No Política de Retención Inferida

Una Integration puede estar:

```text
Archived
```

Este hecho por sí mismo no define:

```text
delete after 30 days

delete after 1 year

automatic purge
```

Ninguna de esas reglas está definida por el dominio versión 1.0.

---

# Ejemplo 67 — Read Model

Un Read Model puede mostrar:

```text
IntegrationId

State

Version
```

para consulta.

No puede ejecutar:

```text
SuspendIntegration
```

directamente sobre el Aggregate.

---

# Ejemplo 68 — Projection Lag

Aggregate:

```text
State = Suspended
```

Read Model temporal:

```text
State = Active
```

bajo consistencia eventual.

La autoridad sigue siendo:

```text
Integration Aggregate
```

---

# Ejemplo 69 — Projection Failure

Ocurre:

```text
IntegrationSuspended
```

pero una Projection falla temporalmente.

Resultado:

```text
Integration remains Suspended
```

El fallo de Projection no revierte el Aggregate.

---

# Ejemplo 70 — Projection Rebuild

Reconstruir una Projection a partir de hechos confirmados no debe
ejecutar nuevamente:

```text
SuspendIntegration

ReactivateIntegration

ArchiveIntegration
```

---

# Ejemplo 71 — Rehydration

Una Integration persistida:

```text
IntegrationId = INT-001

State = Active

Version = 4
```

es rehidratada.

Resultado:

```text
IntegrationId = INT-001

State = Active

Version = 4
```

No se produce un nuevo:

```text
IntegrationActivated
```

---

# Ejemplo 72 — Replay

Si una implementación compatible con Event Sourcing reconstruye:

```text
IntegrationCreated

IntegrationActivated

IntegrationSuspended

IntegrationReactivated
```

el resultado conceptual puede ser:

```text
State = Active
```

Replay no crea hechos nuevos.

---

# Ejemplo 73 — Event Sourcing no Obligatorio

El mismo Aggregate puede ser persistido mediante una estrategia que no
utilice Event Sourcing.

Las reglas de:

- Lifecycle;
- State Machine;
- Commands;
- Domain Events;
- Invariants;
- Permissions;
- Versioning;

permanecen iguales.

---

# Ejemplo 74 — CQRS

Conceptualmente:

```text
ActivateIntegration
        │
        ▼
Integration Aggregate
        │
        ▼
IntegrationActivated
        │
        ▼
    Projection
        │
        ▼
    Read Model
```

La Projection no sustituye al Aggregate.

---

# Ejemplo 75 — No Query desde Write Model para Analytics

Una necesidad como:

```text
"listar todas las integraciones activas por sistema externo"
```

pertenece conceptualmente al Read Side.

No requiere convertir IntegrationRepository en motor analítico.

---

# Ejemplo 76 — No Aggregate Global

Supóngase:

```text
INT-001

INT-002

INT-003
```

Cada identificador representa una Integration independiente.

No debe crearse por esa razón:

```text
GlobalIntegrationAggregate
```

que contenga todas las Integration.

---

# Ejemplo 77 — Consistency Boundary

Una modificación:

```text
ActivateIntegration(INT-001)
```

afecta:

```text
Integration INT-001
```

No modifica atómicamente:

```text
Organization

Assembly

Notification

Audit

FIWARE

Municipal System
```

---

# Ejemplo 78 — Source Aggregate Commit Independiente

Supóngase que:

```text
Assembly
```

confirma un hecho.

Posteriormente Integration procesa una intención relacionada.

Debe mantenerse:

```text
Assembly Commit

≠

Integration Commit
```

---

# Ejemplo 79 — External Commit Independiente

Integration confirma:

```text
State = Active
```

Un sistema externo puede todavía no haber procesado información
relacionada.

Esto no invalida automáticamente la transición interna.

---

# Ejemplo 80 — Sin Distributed Transaction Obligatoria

Conceptualmente puede ocurrir:

```text
Integration Commit
    │
    ▼
External Propagation Later
```

sin que el dominio requiera que ambas operaciones sean una sola
transacción distribuida.

---

# Ejemplo 81 — Notification Independiente

Puede ocurrir:

```text
IntegrationSuspended
```

y posteriormente existir una necesidad de Notification.

Debe mantenerse:

```text
IntegrationSuspended

≠

NotificationDelivered
```

---

# Ejemplo 82 — Audit Independiente

Puede ocurrir:

```text
IntegrationArchived
```

y Audit puede posteriormente preservar una representación auditable
del hecho.

Debe mantenerse:

```text
IntegrationArchived

≠

Audit
```

---

# Ejemplo 83 — Fallo de Audit

Si Integration confirmó:

```text
State = Archived
```

y posteriormente Audit no logra procesar el hecho inmediatamente:

```text
Integration remains Archived
```

El fallo externo no revierte el Aggregate.

---

# Ejemplo 84 — Actor no Embebido

Un hecho puede contener:

```text
ActorId = CIT-001
```

cuando corresponda.

No contiene necesariamente:

```text
Citizen {
    full profile
    memberships
    roles
    credentials
}
```

---

# Ejemplo 85 — Organization no Embebida

Si una Integration se relaciona contractualmente con un contexto
organizacional, no debe incorporar el Aggregate Organization completo
como parte mutable de Integration.

---

# Ejemplo 86 — External System no Embebido

Una Integration con un sistema municipal no contiene conceptualmente:

```text
MunicipalSystem {
    database
    users
    internal workflows
    credentials
    infrastructure
}
```

dentro del Aggregate.

---

# Ejemplo 87 — Technical Health

Puede existir:

```text
State = Active

Technical Health = Degraded
```

fuera del Aggregate.

No existe contradicción porque:

```text
Technical Health

≠

Lifecycle State
```

---

# Ejemplo 88 — Healthy pero Suspended

También puede existir:

```text
State = Suspended

Technical Health = Healthy
```

La salud técnica no reactiva la Integration.

---

# Ejemplo 89 — Credential Expiration

Estado:

```text
State = Active
```

Condición técnica:

```text
Access Token expired
```

Resultado:

```text
State remains Active
```

No se produce automáticamente:

```text
IntegrationSuspended
```

---

# Ejemplo 90 — Credential Rotation

Rotar una credencial técnica no produce por sí mismo:

```text
Integration.Version + 1
```

porque la credencial no forma parte del estado del Aggregate.

---

# Ejemplo 91 — Deployment

Estado antes:

```text
Active
```

Ocurre:

```text
Deployment
```

Estado después:

```text
Active
```

Deployment no constituye transición.

---

# Ejemplo 92 — Restart

Reiniciar un servicio no produce:

```text
IntegrationCreated

IntegrationActivated

IntegrationSuspended

IntegrationReactivated

IntegrationArchived
```

---

# Ejemplo 93 — Cache

Un cache miss no produce:

```text
IntegrationFailed
```

ni otro Domain Event.

---

# Ejemplo 94 — Queue

Un mensaje:

```text
Queued
```

no cambia:

```text
Integration.State
```

---

# Ejemplo 95 — Outbox

Un registro técnico:

```text
Pending Publication
```

no convierte Integration en:

```text
Pending
```

Pending no es State oficial.

---

# Ejemplo 96 — Delivery Failure

Estado:

```text
Active
```

Condición:

```text
Delivery Failed
```

resultado:

```text
State remains Active
```

---

# Ejemplo 97 — No IntegrationFailed

Un error técnico no produce:

```text
IntegrationFailed
```

porque:

```text
Failed

∉

Integration Lifecycle
```

---

# Ejemplo 98 — No IntegrationDeleted

Archivar:

```text
ArchiveIntegration
```

produce:

```text
IntegrationArchived
```

No:

```text
IntegrationDeleted
```

---

# Ejemplo 99 — No IntegrationUpdated Genérico

Activar:

```text
ActivateIntegration
```

produce:

```text
IntegrationActivated
```

No:

```text
IntegrationUpdated
```

porque el evento debe expresar el hecho concreto.

---

# Ejemplo 100 — Nuevo Requerimiento Técnico no Crea Command

Supóngase que una implementación necesita:

```text
Retry HTTP Request
```

Esto no crea automáticamente:

```text
RetryIntegration
```

como Command de dominio.

---

# Ejemplo 101 — Nuevo Endpoint no Crea Permission

Supóngase que se implementa un endpoint:

```text
POST /integrations/{id}/health-check
```

Su existencia técnica no introduce automáticamente:

```text
Integration.HealthCheck
```

como Permission de dominio.

---

# Ejemplo 102 — Nuevo Estado Externo no Crea State Interno

Un proveedor incorpora:

```text
PAUSED
```

como estado externo.

Esto no introduce automáticamente:

```text
Paused
```

en Integration.

---

# Ejemplo 103 — Mapeo Externo no es Identidad

Puede existir:

```text
IntegrationId = INT-001

ExternalSystemId = EXT-923
```

Debe mantenerse:

```text
INT-001

≠

EXT-923
```

conceptualmente.

---

# Ejemplo 104 — No Información Inventada

Si el sistema externo no entrega:

```text
ActorId
```

no debe inventarse:

```text
ActorId = SYSTEM
```

como supuesto hecho de dominio salvo que un contrato explícito defina
esa semántica.

---

# Ejemplo 105 — Read no Incrementa Version

Estado:

```text
Version = 8
```

Operaciones:

```text
findById()

exists()
```

Resultado:

```text
Version = 8
```

---

# Ejemplo 106 — Rechazo no Modifica UpdatedAt

Antes:

```text
State = Archived

UpdatedAt = T1
```

Command:

```text
ActivateIntegration
```

Resultado:

```text
Rejected

UpdatedAt = T1
```

---

# Ejemplo 107 — CreatedAt Inmutable

Creación:

```text
CreatedAt = T1
```

Después de:

```text
ActivateIntegration

SuspendIntegration

ReactivateIntegration

ArchiveIntegration
```

debe mantenerse:

```text
CreatedAt = T1
```

---

# Ejemplo 108 — Identity Round-Trip

Antes:

```text
IntegrationId = INT-001
```

Después de:

```text
save()

findById(INT-001)
```

debe recuperarse:

```text
IntegrationId = INT-001
```

---

# Ejemplo 109 — State Round-Trip

Antes de persistir:

```text
State = Suspended
```

Después de:

```text
save()

findById()
```

debe recuperarse:

```text
State = Suspended
```

---

# Ejemplo 110 — Version Round-Trip

Antes:

```text
Version = 6
```

Después del round-trip de Repository:

```text
Version = 6
```

si no hubo una nueva modificación válida.

---

# Ejemplo 111 — No Persistencia Parcial

Una modificación válida produce:

```text
State = Suspended

Version = 4
```

No debe persistirse:

```text
State = Suspended

Version = 3
```

como resultado parcial de la misma modificación.

---

# Ejemplo 112 — Different IntegrationId

Supóngase:

```text
INT-001 Version = 5

INT-002 Version = 2
```

Ambas secuencias son independientes.

No existe una Version global obligatoria.

---

# Ejemplo 113 — Sin Orden Global

Eventos:

```text
INT-001 / AggregateVersion = 5

INT-002 / AggregateVersion = 8
```

no permiten concluir un orden de negocio global entre ambas
Integration.

---

# Ejemplo 114 — Same IntegrationId

Dos modificaciones concurrentes:

```text
IntegrationId = INT-001
```

deben respetar:

```text
ExpectedVersion
```

del mismo Aggregate.

---

# Ejemplo 115 — Technical Redelivery

Una infraestructura entrega dos veces la misma intención técnica.

Debe mantenerse:

```text
Technical Redelivery

≠

Automatically Two Domain Intentions
```

La estrategia concreta de idempotencia permanece fuera de este
documento.

---

# Ejemplo 116 — No Cardinalidad Inferida

Un mensaje externo no establece por sí mismo una regla:

```text
one external message

=

exactly one Integration
```

salvo que un contrato de dominio lo defina explícitamente.

---

# Ejemplo 117 — Integration Event no Sustituye Domain Event

Si existe posteriormente un contrato externo derivado de:

```text
IntegrationActivated
```

el hecho interno continúa siendo:

```text
IntegrationActivated
```

El contrato externo no reemplaza el evento del dominio.

---

# Ejemplo 118 — Integration Contract no es Aggregate

Puede existir un contrato relacionado con:

```text
INT-001
```

pero:

```text
Contract

≠

Integration Aggregate
```

La Version contractual tampoco sustituye:

```text
Integration.Version
```

---

# Ejemplo 119 — API Version Independiente

Puede existir:

```text
API Version = v2

Integration.Version = 9
```

sin que:

```text
v2
```

determine la Version del Aggregate.

---

# Ejemplo 120 — Security Policy Change

Estado:

```text
State = Active

Version = 5
```

Cambia una Authorization Policy externa.

Resultado:

```text
State = Active

Version = 5
```

por el solo cambio de política.

---

# Ejemplo 121 — Permission Revocation

Si una Permission es revocada externamente, Integration no pasa
automáticamente a:

```text
Suspended
```

---

# Ejemplo 122 — Authentication Failure

Estado:

```text
Active
```

Un requester falla Authentication.

Resultado:

```text
Request rejected
```

pero:

```text
Integration State remains Active
```

---

# Ejemplo 123 — Authorization Failure

Estado:

```text
Active
```

Un requester carece de:

```text
Integration.Suspend
```

`SuspendIntegration` es rechazado.

El Aggregate permanece:

```text
Active
```

---

# Ejemplo 124 — Infrastructure Access no es Permission

Un operador puede poseer acceso técnico a la base de datos.

Esto no concede:

```text
Integration.Archive
```

dentro del dominio.

---

# Ejemplo 125 — Database Update Directo Inválido

Modificar directamente:

```text
State = Archived
```

en persistencia sin ejecutar comportamiento del Aggregate no equivale
a:

```text
ArchiveIntegration
```

y viola el modelo de dominio.

---

# Ejemplo 126 — FIWARE Authorization no es AURA Permission

Un actor puede tener autorización en FIWARE.

Esto no implica automáticamente:

```text
Integration.Activate
```

en AURA.

---

# Ejemplo 127 — Municipal Authorization no es AURA Permission

De manera equivalente:

```text
Municipal Permission

≠

Integration Permission
```

---

# Ejemplo 128 — Read Permission no es Write Permission

Un requester puede estar autorizado para consultar un Read Model.

Esto no implica:

```text
Integration.Suspend
```

---

# Ejemplo 129 — Write Permission no es Autoridad Universal

Poseer:

```text
Integration.Activate
```

no implica automáticamente:

```text
Integration.Suspend

Integration.Archive
```

---

# Ejemplo 130 — Explicit Contract

Una interoperabilidad válida debe basarse en:

```text
Explicit Contract
```

y no simplemente en:

```text
External System has an API
```

---

# Ejemplo 131 — External API no Define Domain Model

Un sistema externo posee:

```text
status

endpoint

retries

connection_state
```

Esto no obliga a incorporar dichos atributos a Integration.

---

# Ejemplo 132 — Protocol Independence

Una Integration puede materializarse externamente mediante un
protocolo.

Cambiar técnicamente:

```text
HTTP

→

MQTT
```

no implica automáticamente cambiar:

```text
IntegrationId

State

Version

Lifecycle

Commands

Domain Events
```

---

# Ejemplo 133 — Broker Independence

Cambiar técnicamente:

```text
Broker A

→

Broker B
```

no representa por sí mismo una modificación del Aggregate.

---

# Ejemplo 134 — Persistence Independence

Cambiar una implementación de Repository:

```text
Persistence A

→

Persistence B
```

debe preservar:

```text
IntegrationId

State

Version

CreatedAt

UpdatedAt

Domain Meaning
```

---

# Ejemplo 135 — Substituibilidad del Repository

Dos implementaciones diferentes de:

```text
IntegrationRepository
```

deben devolver conceptualmente el mismo Aggregate para el mismo estado
persistido.

---

# Ejemplo 136 — No Internal Entity Inventada

Una implementación puede utilizar múltiples tablas o documentos.

Esto no crea automáticamente:

```text
IntegrationConnection

IntegrationEndpoint

IntegrationBroker
```

como Internal Entities del dominio.

---

# Ejemplo 137 — No Value Object Inventado

Utilizar una estructura técnica:

```text
URL
```

no establece automáticamente un Value Object específico de Integration
en versión 1.0.

---

# Ejemplo 138 — No State desde Queue

Estado de Infrastructure:

```text
Queue = Processing
```

no implica:

```text
Integration State = Processing
```

---

# Ejemplo 139 — No State desde Provider

Estado del proveedor:

```text
ERROR
```

no implica:

```text
Integration State = Failed
```

Failed no forma parte del Lifecycle oficial.

---

# Ejemplo 140 — No Auto-Archive por Tiempo

Una Integration permanece Active durante un período prolongado.

El solo paso del tiempo no ejecuta:

```text
ArchiveIntegration
```

porque no existe una transición programada definida.

---

# Ejemplo 141 — No Expired

La versión 1.0 no permite concluir:

```text
State = Expired
```

por fecha, timeout o vencimiento técnico.

---

# Ejemplo 142 — No Cancelled

Una Integration retirada operativamente termina en:

```text
Archived
```

mediante una transición válida.

No se introduce:

```text
Cancelled
```

como State.

---

# Ejemplo 143 — No Deleted

La ausencia de necesidad operativa posterior no transforma:

```text
Archived
```

en:

```text
Deleted
```

dentro del Lifecycle.

---

# Ejemplo 144 — Historical Meaning

Secuencia:

```text
IntegrationCreated

IntegrationActivated

IntegrationSuspended

IntegrationReactivated

IntegrationArchived
```

conserva el significado de cada hecho.

Un evento anterior no se reescribe cuando ocurre uno posterior.

---

# Ejemplo 145 — Archived Histórico

Una Integration que terminó en:

```text
Archived
```

conserva ese resultado histórico.

Una necesidad futura de interoperabilidad no permite mutarla
directamente de nuevo a Active.

---

# Ejemplo 146 — Nueva Integration Posterior

Si el dominio requiere posteriormente una relación independiente:

```text
New Integration
```

deberá poseer:

```text
New IntegrationId
```

conforme a las reglas de identidad aplicables.

Este ejemplo no establece una regla de equivalencia entre la nueva y
la anterior.

---

# Ejemplo 147 — No Global Lifecycle

Puede existir:

```text
INT-001 = Active

INT-002 = Suspended

INT-003 = Archived
```

simultáneamente.

Cada Aggregate mantiene su propio Lifecycle.

---

# Ejemplo 148 — No Global Version

Puede existir:

```text
INT-001 Version = 10

INT-002 Version = 3

INT-003 Version = 17
```

sin requerir una secuencia global compartida.

---

# Ejemplo 149 — IntegrationCreated no Significa Publicado

Después de:

```text
IntegrationCreated
```

solamente se sabe que:

```text
State = Draft
```

No puede inferirse:

```text
Published

Connected

Synchronized

Available Externally
```

---

# Ejemplo 150 — IntegrationActivated no Significa Éxito Externo

Después de:

```text
IntegrationActivated
```

la Integration está formalmente Active.

No puede inferirse:

```text
External operation succeeded
```

---

# Ejemplo 151 — IntegrationSuspended no Significa Error

Después de:

```text
IntegrationSuspended
```

debe interpretarse:

```text
Formal Domain Suspension
```

y no:

```text
Technical Failure
```

---

# Ejemplo 152 — IntegrationReactivated no Significa Reconnect

Después de:

```text
IntegrationReactivated
```

debe interpretarse:

```text
Formal Domain Reactivation
```

y no:

```text
Network Reconnection
```

---

# Ejemplo 153 — IntegrationArchived no Significa Purga

Después de:

```text
IntegrationArchived
```

no debe inferirse:

```text
purge()
```

---

# Ejemplo 154 — Error de Persistencia

Aggregate intenta confirmar una transición válida.

Ocurre:

```text
PersistenceFailure
```

No debe concluirse:

```text
State = Failed
```

porque Failed no pertenece al dominio.

---

# Ejemplo 155 — RepositoryUnavailable

Si:

```text
IntegrationRepository = Unavailable
```

esto no produce:

```text
IntegrationSuspended
```

---

# Ejemplo 156 — DuplicateIntegrationId

Si un nuevo Aggregate intenta persistirse con una identidad ya
existente:

```text
DuplicateIntegrationId
```

representa un conflicto de identidad.

No es un State.

---

# Ejemplo 157 — ConcurrencyConflict no es State

Después de:

```text
ConcurrencyConflict
```

la Integration no pasa a:

```text
Failed
```

ni:

```text
Suspended
```

---

# Ejemplo 158 — Read Model no es Source of Truth de Escritura

Read Model:

```text
State = Draft
```

Aggregate:

```text
State = Active
```

Una nueva intención debe validarse contra el Aggregate autoritativo y
su Version, no mutar desde el valor de la Projection.

---

# Ejemplo 159 — No Command desde Repository

Código conceptual equivalente a:

```text
repository.activate(id)
```

no forma parte del Repository Contract.

La intención correcta pertenece al comportamiento:

```text
ActivateIntegration
```

---

# Ejemplo 160 — No Query Analítica en Repository

Una operación conceptual:

```text
findAllActiveByExternalProviderAndDateRange()
```

no se incorpora automáticamente al Repository del Write Model.

La necesidad pertenece al Read Side.

---

# Ejemplo 161 — No Decisión de Outbox

Si una implementación utiliza un mecanismo técnico para publicación,
este documento no concluye que dicho mecanismo sea obligatorio.

Debe mantenerse:

```text
Integration Domain Rules

independent from

Publication Mechanism
```

---

# Ejemplo 162 — No 2PC Obligatorio

Una integración con un sistema externo no obliga conceptualmente a:

```text
Integration Database Commit

+

External System Commit

=

One Distributed Transaction
```

---

# Ejemplo 163 — Data Minimization

Un sistema externo entrega cien atributos.

Si Integration necesita conceptualmente solo información formal
definida por su contrato:

```text
only required domain information
```

debe preservarse.

Los demás datos no se incorporan automáticamente al Aggregate.

---

# Ejemplo 164 — Sensitive Information

Un External Payload contiene:

```text
AccessToken

PersonalData

ProviderMetadata
```

Esto no significa que esos datos deban persistirse dentro de
Integration.

---

# Ejemplo 165 — Secret no es Trazabilidad

Debe mantenerse:

```text
Secret

≠

Traceability Data
```

No debe almacenarse un secreto solamente para explicar una operación.

---

# Ejemplo 166 — Correlation sin Ownership

Puede existir:

```text
Assembly Event CorrelationId = CORR-100

Integration Event CorrelationId = CORR-100
```

cuando corresponda.

Esto no fusiona:

```text
Assembly

Integration
```

en un mismo Aggregate.

---

# Ejemplo 167 — Audit y Correlation

Audit puede preservar posteriormente el mismo CorrelationId cuando el
hecho fuente lo proporciona.

Esto no modifica Integration.

---

# Ejemplo 168 — EventId no se Reutiliza

Si:

```text
EVT-001 = IntegrationCreated
```

el mismo:

```text
EVT-001
```

no puede representar posteriormente:

```text
IntegrationArchived
```

---

# Ejemplo 169 — Retransmisión del Mismo Evento

Una infraestructura puede entregar:

```text
EVT-001
```

más de una vez.

Esto no crea múltiples hechos:

```text
IntegrationCreated
```

si se trata del mismo evento.

---

# Ejemplo 170 — Dos Hechos Distintos

Dos Integration diferentes pueden producir:

```text
IntegrationActivated
```

con:

```text
EventId = EVT-101

EventId = EVT-205
```

respectivamente.

El EventType puede coincidir.

Los hechos siguen siendo distintos.

---

# Ejemplo 171 — Same Aggregate, Different Events

Una Integration puede producir:

```text
IntegrationActivated

IntegrationSuspended

IntegrationReactivated
```

Cada hecho posee su propio EventId y AggregateVersion.

---

# Ejemplo 172 — Domain Event Inmutable

Después de confirmar:

```text
IntegrationSuspended
```

no debe editarse posteriormente para convertirlo en:

```text
IntegrationArchived
```

---

# Ejemplo 173 — Historical State no es Current State

Históricamente:

```text
IntegrationSuspended
```

puede haber ocurrido.

Estado actual:

```text
Active
```

después de una reactivación válida.

No existe contradicción.

---

# Ejemplo 174 — Archived Terminal

Secuencia inválida:

```text
IntegrationArchived
    │
    ▼
IntegrationReactivated
```

No puede ocurrir en versión 1.0 para la misma Integration.

---

# Ejemplo 175 — Nuevo Requerimiento no Modifica Historial

Si en una versión futura se define nuevo comportamiento, los hechos
históricos existentes no deben reinterpretarse silenciosamente.

---

# Ejemplo 176 — No Arquitectura Inferida

La necesidad:

```text
publish Integration information externally
```

no permite concluir desde este documento:

```text
Kafka

RabbitMQ

MQTT

HTTP

Outbox

Webhook
```

como mecanismo obligatorio.

---

# Ejemplo 177 — No Base de Datos Inferida

La necesidad:

```text
persist Integration
```

no permite concluir:

```text
PostgreSQL

MongoDB

EventStoreDB
```

como tecnología obligatoria.

---

# Ejemplo 178 — No Framework Inferido

La existencia de Commands no implica:

```text
FastAPI

Django

Next.js
```

como tecnología del dominio.

---

# Ejemplo 179 — No Broker Inferido

La existencia de Domain Events no implica:

```text
Kafka

RabbitMQ

NATS
```

---

# Ejemplo 180 — No FIWARE Interno

La necesidad de interoperar con FIWARE no transforma:

```text
Integration
```

en:

```text
FIWARE Adapter
```

---

# Ejemplo 181 — No Modelo Municipal Interno

La necesidad de interoperar con una municipalidad no transforma el
modelo municipal en parte interna del Aggregate.

---

# Ejemplo 182 — Invariant Failure

Estado inicial:

```text
Draft
```

Command:

```text
ActivateIntegration
```

Una Invariant requerida falla.

Resultado:

```text
Rejected

State = Draft

Version unchanged

UpdatedAt unchanged

No IntegrationActivated
```

---

# Ejemplo 183 — Guard Failure

Una precondición formal del Command no se satisface.

Resultado:

```text
Rejected
```

sin modificación parcial.

---

# Ejemplo 184 — No Partial Aggregate

Una operación inválida no puede producir:

```text
State = Active

Version = PreviousVersion

UpdatedAt = PreviousUpdatedAt
```

como una modificación parcialmente confirmada.

---

# Ejemplo 185 — No Partial Creation

Si CreateIntegration no puede completarse válidamente:

```text
No Integration
```

debe continuar representando inexistencia.

No se persiste una Integration parcial.

---

# Ejemplo 186 — IntegrationId Inmutable

Estado inicial:

```text
IntegrationId = INT-001

State = Draft
```

después de:

```text
ActivateIntegration

SuspendIntegration

ReactivateIntegration

ArchiveIntegration
```

debe mantenerse:

```text
IntegrationId = INT-001
```

---

# Ejemplo 187 — No setState()

Una operación:

```text
setState(Active)
```

no forma parte del comportamiento público.

Debe utilizarse:

```text
ActivateIntegration
```

cuando la transición sea válida.

---

# Ejemplo 188 — No setVersion()

Una operación:

```text
setVersion(42)
```

no forma parte del dominio.

Version evoluciona mediante modificaciones válidas.

---

# Ejemplo 189 — No UpdateIntegration Genérico

Una intención:

```text
UpdateIntegration(...)
```

no está definida en versión 1.0.

No debe utilizarse para evitar Commands semánticos.

---

# Ejemplo 190 — No ModifyIntegration Genérico

Tampoco:

```text
ModifyIntegration(...)
```

forma parte del contrato oficial.

---

# Ejemplo 191 — No DeleteIntegration

Una intención:

```text
DeleteIntegration
```

no forma parte de los Commands oficiales.

---

# Ejemplo 192 — No RetryIntegration

Una operación técnica:

```text
retry delivery
```

no produce:

```text
RetryIntegration
```

como Command.

---

# Ejemplo 193 — No ConnectIntegration

Una operación técnica:

```text
connect socket
```

no produce:

```text
ConnectIntegration
```

---

# Ejemplo 194 — No DisconnectIntegration

Una desconexión de red no produce:

```text
DisconnectIntegration
```

---

# Ejemplo 195 — No FailIntegration

Un error del proveedor no produce:

```text
FailIntegration
```

---

# Ejemplo 196 — No IntegrationPublished

Una publicación técnica exitosa no produce automáticamente:

```text
IntegrationPublished
```

como Domain Event.

---

# Ejemplo 197 — No IntegrationSynchronized

Una sincronización técnica no produce automáticamente:

```text
IntegrationSynchronized
```

como Domain Event.

---

# Ejemplo 198 — No IntegrationRetried

Un retry técnico no produce:

```text
IntegrationRetried
```

---

# Ejemplo 199 — No IntegrationConnected

Una conexión técnica exitosa no produce:

```text
IntegrationConnected
```

---

# Ejemplo 200 — No IntegrationDisconnected

Una pérdida de conectividad no produce:

```text
IntegrationDisconnected
```

---

# Ejemplo 201 — No IntegrationFailed

Una operación externa fallida no produce:

```text
IntegrationFailed
```

---

# Ejemplo 202 — No Auto-Mapping de Estado

Sistema externo:

```text
status = DISABLED
```

no debe mapearse automáticamente a:

```text
State = Suspended
```

salvo que una futura regla explícita de dominio defina dicha semántica.

---

# Ejemplo 203 — No Auto-Mapping de Payload

External Payload:

```text
{
    state,
    error_code,
    retries,
    broker,
    timestamp,
    credentials
}
```

no se transforma automáticamente en atributos de Integration.

---

# Ejemplo 204 — No Automatic Integration Event

Domain Event:

```text
IntegrationArchived
```

no implica automáticamente:

```text
IntegrationArchivedIntegrationEvent
```

Este documento no define ese contrato.

---

# Ejemplo 205 — Read Side para Historial

Una consulta:

```text
"mostrar todas las transiciones históricas de INT-001"
```

pertenece al Read Side.

No requiere ampliar el Aggregate con una colección global de historial
de consulta.

---

# Ejemplo 206 — Read Side para Filtrado

Una consulta:

```text
"listar Integration con State = Suspended"
```

pertenece al Read Model.

---

# Ejemplo 207 — Read Side para Reporting

Una consulta:

```text
"cantidad de Integration Active por período"
```

pertenece al Read Side.

---

# Ejemplo 208 — Read Side para Analytics

Una necesidad:

```text
"tasa histórica de suspensiones"
```

no modifica el Aggregate ni sus Commands.

---

# Ejemplo 209 — Performance no Rompe Boundary

Una optimización para procesar muchas Integration no permite fusionar:

```text
INT-001

INT-002

INT-003
```

en una única unidad de consistencia.

---

# Ejemplo 210 — Batch Técnico

Un proceso técnico puede manejar múltiples Integration.

Conceptualmente cada una conserva:

```text
own IntegrationId

own State

own Version

own Consistency Boundary
```

---

# Ejemplo 211 — Security no Rompe Invariants

Un requester con máxima autoridad técnica intenta:

```text
ReactivateIntegration
```

sobre:

```text
State = Archived
```

Resultado:

```text
Rejected
```

Ninguna Permission evita la terminalidad.

---

# Ejemplo 212 — Security no Rompe Versioning

Requester autorizado:

```text
Integration.Suspend
```

pero:

```text
ExpectedVersion = 3

PersistedVersion = 4
```

Resultado:

```text
ConcurrencyConflict
```

---

# Ejemplo 213 — Security no Expande Boundary

Poseer:

```text
Integration.Archive
```

no permite archivar simultáneamente:

```text
Notification

Audit

Assembly
```

---

# Ejemplo 214 — Authentication no es State

Un fallo de autenticación produce rechazo de acceso.

No produce:

```text
State = Suspended
```

---

# Ejemplo 215 — Authorization Denied no es State

Resultado:

```text
Denied
```

pertenece a la decisión de autorización.

No forma parte de:

```text
Draft

Active

Suspended

Archived
```

---

# Ejemplo 216 — Integration Contract Evoluciona Independiente

Una evolución contractual puede cambiar:

```text
Contract Version 1

→

Contract Version 2
```

sin que Integration.Version cambie automáticamente.

---

# Ejemplo 217 — API Evoluciona Independiente

Una API puede cambiar:

```text
v1 → v2
```

sin provocar:

```text
Draft → Active
```

ni otra transición.

---

# Ejemplo 218 — Schema Evoluciona Independiente

Una representación externa puede cambiar schema sin modificar
automáticamente:

```text
Integration.State

Integration.Version
```

---

# Ejemplo 219 — External System Evoluciona Independiente

Un sistema externo puede cambiar su propia Version.

Esto no incrementa automáticamente:

```text
Integration.Version
```

---

# Ejemplo 220 — Explicit Domain Change

Solamente una modificación formalmente reconocida por Integration puede
alterar:

```text
State

Version

UpdatedAt
```

conforme a sus reglas.

---

# Ejemplo 221 — No Retention Rule

Una Integration Archived hace:

```text
365 days
```

no autoriza concluir:

```text
delete()
```

porque no existe una política de retención definida.

---

# Ejemplo 222 — No Anonymization Rule

La versión 1.0 no permite concluir automáticamente que una Integration
Archived deba:

```text
anonymize()
```

---

# Ejemplo 223 — No Redaction Rule

Tampoco existe comportamiento:

```text
redact()
```

definido en el Lifecycle.

---

# Ejemplo 224 — No Scheduled Transition

Una fecha alcanzada no ejecuta automáticamente:

```text
SuspendIntegration

ArchiveIntegration
```

---

# Ejemplo 225 — No Expiration State

Una fecha externa de expiración no crea:

```text
Expired
```

como State de Integration.

---

# Ejemplo 226 — Dominio Independiente de Tecnología

El mismo flujo:

```text
CreateIntegration

ActivateIntegration

SuspendIntegration

ReactivateIntegration

ArchiveIntegration
```

debe conservar la misma semántica aunque cambien tecnologías externas.

---

# Ejemplo 227 — Test Conceptual de Create

```text
Given

No Integration

And

Integration.Create is allowed

When

CreateIntegration succeeds

Then

State = Draft

And

IntegrationCreated exists
```

---

# Ejemplo 228 — Test Conceptual de Activate

```text
Given

State = Draft

And

Integration.Activate is allowed

When

ActivateIntegration succeeds

Then

State = Active

And

IntegrationActivated exists
```

---

# Ejemplo 229 — Test Conceptual de Suspend

```text
Given

State = Active

And

Integration.Suspend is allowed

When

SuspendIntegration succeeds

Then

State = Suspended

And

IntegrationSuspended exists
```

---

# Ejemplo 230 — Test Conceptual de Reactivate

```text
Given

State = Suspended

And

Integration.Reactivate is allowed

When

ReactivateIntegration succeeds

Then

State = Active

And

IntegrationReactivated exists
```

---

# Ejemplo 231 — Test Conceptual de Archive

```text
Given

State ∈ {Draft, Active, Suspended}

And

Integration.Archive is allowed

When

ArchiveIntegration succeeds

Then

State = Archived

And

IntegrationArchived exists
```

---

# Ejemplo 232 — Test Conceptual de Archived Terminal

```text
Given

State = Archived

When

ReactivateIntegration

Then

Rejected

And

State remains Archived

And

Version remains unchanged

And

no IntegrationReactivated
```

---

# Ejemplo 233 — Test Conceptual de Permission

```text
Given

State = Active

And

Integration.Suspend is denied

When

SuspendIntegration

Then

Rejected

And

State remains Active
```

---

# Ejemplo 234 — Test Conceptual de Concurrencia

```text
Given

PersistedVersion = 7

And

ExpectedVersion = 6

When

a modification is persisted

Then

ConcurrencyConflict
```

---

# Ejemplo 235 — Test Conceptual de Rehydration

```text
Given

IntegrationId = INT-001

State = Suspended

Version = 5

When

findById(INT-001)

Then

IntegrationId = INT-001

State = Suspended

Version = 5

And

no new Domain Event
```

---

# Ejemplo 236 — Test Conceptual de External Failure

```text
Given

State = Active

When

External System becomes unavailable

Then

State remains Active

And

no IntegrationSuspended
```

---

# Ejemplo 237 — Test Conceptual de Technical Recovery

```text
Given

State = Suspended

When

External System becomes available

Then

State remains Suspended

And

no IntegrationReactivated
```

---

# Ejemplo 238 — Test Conceptual de Read Model

```text
Given

Aggregate State = Active

And

Read Model State = Draft

When

a Write Command is evaluated

Then

Aggregate State and Version remain authoritative
```

---

# Ejemplo 239 — Test Conceptual de Domain Event versus Integration Event

```text
Given

IntegrationActivated is confirmed

When

no explicit external contract requires publication

Then

no mandatory Integration Event is inferred
```

---

# Ejemplo 240 — Test Conceptual de Credenciales

```text
Given

External credentials exist in Infrastructure

When

Integration is persisted

Then

credentials are not part of Integration domain state
```

---

# Regla de Consistencia de Ejemplos

Todo ejemplo de este documento debe ser interpretado bajo las reglas:

```text
Lifecycle

State Machine

Commands

Domain Events

Invariants

Permissions

Repository Contract

Versioning

Consistency Boundary
```

definidas por el dominio Integration.

---

# Ejemplos no Definen Arquitectura

Ningún ejemplo determina:

- broker;
- base de datos;
- framework;
- protocolo;
- mecanismo de publicación;
- mecanismo de idempotencia;
- tecnología de observabilidad;
- mecanismo de autenticación;
- mecanismo de autorización;
- estrategia de Event Sourcing;
- estrategia de CQRS física;
- mecanismo de traducción externo.

---

# Ejemplos no Definen Nuevos Estados

No debe inferirse desde ningún ejemplo:

```text
Connected

Disconnected

Failed

Pending

Deleted

Cancelled

Expired

Processing

Retrying

Published
```

como State del Aggregate.

---

# Ejemplos no Definen Nuevos Commands

No debe inferirse:

```text
ConnectIntegration

DisconnectIntegration

FailIntegration

RetryIntegration

DeleteIntegration

CancelIntegration

ResetIntegration

UpdateIntegration

ModifyIntegration
```

como Commands oficiales.

---

# Ejemplos no Definen Nuevos Domain Events

No debe inferirse:

```text
IntegrationConnected

IntegrationDisconnected

IntegrationFailed

IntegrationRetried

IntegrationDeleted

IntegrationCancelled

IntegrationPublished

IntegrationSynchronized

IntegrationUpdated
```

como Domain Events oficiales.

---

# Ejemplos no Definen Nuevas Permissions

No debe inferirse:

```text
Integration.Connect

Integration.Disconnect

Integration.Fail

Integration.Retry

Integration.Delete

Integration.Update
```

como Permissions del dominio.

---

# Ejemplos no Definen Retención

Ningún ejemplo introduce:

```text
retention period

expiry

purge

auto-delete

auto-archive
```

---

# Ejemplos no Definen Cardinalidad

Ningún ejemplo introduce una relación obligatoria:

```text
one external system

=

one Integration
```

ni:

```text
one external message

=

one Integration
```

ni otra cardinalidad no definida formalmente.

---

# Ejemplos no Definen Internal Entities

Los ejemplos no crean entidades internas específicas.

---

# Ejemplos no Definen Value Objects

Los ejemplos no crean Value Objects específicos de Integration.

---

# Regla de No Inferencia

Debe mantenerse:

```text
Example Detail

≠

New Domain Contract
```

y:

```text
Technical Example

≠

Architectural Decision
```

---

# Reglas Fundamentales

Los ejemplos de Integration deben cumplir:

1. Toda nueva Integration comienza en Draft.
2. CreateIntegration produce IntegrationCreated cuando es válido.
3. ActivateIntegration solamente opera desde Draft.
4. ActivateIntegration produce IntegrationActivated.
5. SuspendIntegration solamente opera desde Active.
6. SuspendIntegration produce IntegrationSuspended.
7. ReactivateIntegration solamente opera desde Suspended.
8. ReactivateIntegration produce IntegrationReactivated.
9. ArchiveIntegration opera desde Draft, Active o Suspended.
10. ArchiveIntegration produce IntegrationArchived.
11. Archived permanece terminal.
12. Archived no significa Physical Deletion.
13. IntegrationId permanece inmutable.
14. Una modificación válida evoluciona Version.
15. Una operación rechazada no modifica Version.
16. Una operación rechazada no modifica UpdatedAt.
17. Una operación rechazada no produce Domain Event de éxito.
18. Permission no sustituye State Machine.
19. Permission no sustituye Invariants.
20. Permission no sustituye Versioning.
21. Permission no concede autoridad sobre otros Aggregates.
22. ActorId no es Permission.
23. CorrelationId no es Permission.
24. CausationId no es Permission.
25. Domain Event representa un hecho confirmado.
26. EventId no es IntegrationId.
27. AggregateVersion coincide con la Version resultante.
28. Contract Version no es Integration.Version.
29. External Version no es Integration.Version.
30. External State no determina Integration State.
31. Technical Health no determina Integration State.
32. Timeout no suspende automáticamente.
33. Broker Failure no suspende automáticamente.
34. FIWARE Failure no suspende automáticamente.
35. Municipal System Failure no suspende automáticamente.
36. Technical Recovery no reactiva automáticamente.
37. External Message no es automáticamente un Command.
38. External Integration Event no modifica State directamente.
39. Domain Event externo no modifica State directamente.
40. Source Domain Event mantiene ownership de su Aggregate productor.
41. Domain Event no es Integration Event.
42. Domain Event no obliga publicación externa.
43. Publication Failure no revierte el Aggregate.
44. Technical Retry no produce nuevo Domain Event.
45. External Payload no se convierte automáticamente en estado.
46. Información ausente no se fabrica.
47. Credenciales no forman parte de Integration.
48. Integration no es HTTP Client.
49. Integration no es Broker Connection.
50. Integration no es FIWARE Entity.
51. Integration no absorbe Municipal Systems.
52. Repository persiste pero no ejecuta Commands.
53. findById() no modifica el Aggregate.
54. exists() no modifica el Aggregate.
55. nextIdentity() no crea el Aggregate.
56. Repository.delete() no es ArchiveIntegration.
57. Archived no ejecuta delete() automáticamente.
58. No existe política de retención implícita.
59. Read Models no poseen autoridad de escritura.
60. Projection Lag no altera el Aggregate autoritativo.
61. Projection Failure no revierte el Aggregate.
62. Rehydration no genera Domain Events nuevos.
63. Replay no genera hechos nuevos.
64. Event Sourcing es compatible pero no obligatorio.
65. CQRS no cambia las reglas del Aggregate.
66. Cada IntegrationId mantiene su propio Consistency Boundary.
67. No existe un Global Integration Aggregate.
68. Integration Commit no es External System Commit.
69. No se requiere una Distributed Transaction por regla de dominio.
70. Audit permanece fuera del Aggregate.
71. Notification permanece fuera del Aggregate.
72. Technical Health puede diferir del Lifecycle State.
73. Credential Expiration no cambia State automáticamente.
74. Deployment no cambia State.
75. Queue State no cambia State.
76. Outbox State no cambia State.
77. Delivery Failure no cambia State automáticamente.
78. Failed no es State.
79. Deleted no es State.
80. Cancelled no es State.
81. IntegrationUpdated genérico no es Domain Event oficial.
82. RetryIntegration no es Command oficial.
83. ConnectIntegration no es Command oficial.
84. DisconnectIntegration no es Command oficial.
85. FailIntegration no es Command oficial.
86. API Version no es Integration.Version.
87. Schema Version no es Integration.Version.
88. Authorization Policy Change no modifica el Aggregate por sí mismo.
89. Infrastructure Access no es Domain Permission.
90. Database Update directo no sustituye comportamiento de dominio.
91. FIWARE Authorization no es automáticamente AURA Permission.
92. Municipal Authorization no es automáticamente AURA Permission.
93. Read Permission no es Write Permission.
94. Explicit Contract es necesario para interoperabilidad reconocida.
95. External API no define el Domain Model.
96. Persistence Technology no define el Domain Model.
97. Technical Redelivery no implica automáticamente nueva intención.
98. Los ejemplos no crean nuevas cardinalidades.
99. Los ejemplos no crean nuevas decisiones arquitectónicas.
100. Todo ejemplo permanece subordinado a los contratos oficiales del
     Aggregate Integration.

---

# Restricciones

No está permitido interpretar un ejemplo como autorización para:

- introducir un nuevo State;
- introducir una nueva transición;
- introducir un nuevo Command;
- introducir un nuevo Domain Event;
- introducir una nueva Permission;
- introducir una nueva Invariant;
- introducir una nueva Internal Entity;
- introducir un nuevo Value Object;
- modificar IntegrationId;
- reactivar Archived;
- evitar State Machine;
- evitar Invariants;
- evitar Permissions;
- evitar Versioning;
- ignorar ConcurrencyConflict;
- modificar otros Aggregates;
- fusionar Consistency Boundaries;
- convertir estados técnicos en States del dominio;
- convertir errores técnicos en Domain Events;
- convertir External Messages directamente en Commands;
- publicar automáticamente todo Domain Event;
- persistir credenciales;
- persistir External Payload completo por defecto;
- inferir políticas de retención;
- inferir eliminación física;
- inferir cardinalidades;
- imponer Event Sourcing;
- imponer CQRS físico;
- imponer broker;
- imponer protocolo;
- imponer base de datos;
- imponer framework;
- imponer FIWARE como modelo interno;
- imponer un mecanismo de publicación;
- imponer una estrategia de idempotencia;
- transformar Repository en Read Model;
- transformar Integration en Adapter técnico;
- introducir arquitectura nueva desde un ejemplo.

---

# Compatibilidad Arquitectónica

Los ejemplos son compatibles con:

- Domain-Driven Design;
- Aggregate Pattern;
- State Machine Pattern;
- Command Pattern;
- Domain Event Pattern;
- Repository Pattern;
- Clean Architecture;
- Hexagonal Architecture;
- SOLID;
- CQRS;
- Event-Driven Architecture;
- Event Sourcing Compatible;
- Optimistic Concurrency Control;
- consistencia eventual;
- High Cohesion;
- Low Coupling.

La compatibilidad no introduce decisiones técnicas adicionales.

---

# Definición de Éxito

Los ejemplos del Aggregate **Integration** permiten demostrar de forma
coherente el comportamiento definido por los contratos oficiales sin
ampliar el dominio por inferencia.

Los flujos centrales quedan ilustrados mediante:

```text
No Integration
    │
    │ CreateIntegration
    ▼
  Draft
    │
    │ ActivateIntegration
    ▼
  Active
    │
    │ SuspendIntegration
    ▼
Suspended
    │
    │ ReactivateIntegration
    ▼
  Active
    │
    │ ArchiveIntegration
    ▼
Archived
```

junto con:

```text
Draft     → Archived

Active    → Archived

Suspended → Archived
```

El documento demuestra que:

- Commands representan intención;
- Domain Events representan hechos confirmados;
- Permissions habilitan intentos y no garantizan éxito;
- State Machine controla transiciones;
- Invariants protegen validez;
- Versioning protege evolución y concurrencia;
- Repository persiste sin ejecutar comportamiento;
- Read Models consultan sin poseer autoridad de escritura;
- IntegrationId permanece inmutable;
- Archived permanece terminal;
- Technical Failure permanece fuera del Lifecycle;
- External State permanece fuera del Lifecycle;
- Domain Event permanece distinto de Integration Event;
- External Payload no se convierte automáticamente en estado;
- credenciales permanecen fuera del Aggregate;
- FIWARE permanece externo al Domain Model;
- sistemas municipales permanecen externos al Domain Model;
- Audit y Notification mantienen sus propios Consistency Boundaries;
- consistencia externa permanece eventual;
- Event Sourcing permanece compatible pero no obligatorio;
- ninguna tecnología concreta se deriva de los ejemplos;
- ninguna regla de dominio adicional se deriva de los ejemplos.

De esta forma, `DOMAIN-013H-Examples.md` documenta ejemplos oficiales
del Aggregate **Integration** conforme al patrón consolidado de AURA
Core.