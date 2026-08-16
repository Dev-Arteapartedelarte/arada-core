# DOMAIN-013B — Integration State Machine

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
- DOMAIN-013C-Commands.md
- DOMAIN-013D-Domain-Events.md
- DOMAIN-013E-Invariants.md
- DOMAIN-013F-Permissions.md
- DOMAIN-013G-Repository-Contract.md
- DOMAIN-013H-Examples.md
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

Este documento define formalmente la **State Machine** del Aggregate
**Integration**.

La State Machine establece:

- estados válidos;
- transiciones válidas;
- transiciones inválidas;
- condiciones generales de transición;
- terminalidad;
- reglas de preservación de identidad;
- reglas de Versioning asociadas;
- relación con Commands;
- relación con Domain Events;
- relación con Invariants;
- relación con Permissions.

La State Machine formaliza el Lifecycle definido en:

```text
DOMAIN-013A-Lifecycle.md
```

---

# Principio Fundamental

Debe mantenerse:

```text
State Change

=

Explicit Valid Domain Transition
```

y nunca:

```text
State Change

=

Direct Property Mutation
```

---

# Estados Oficiales

La versión 1.0 define exactamente los siguientes estados persistidos:

```text
Draft

Active

Suspended

Archived
```

No existen otros estados oficiales en esta versión.

---

# No Integration

`No Integration` representa inexistencia.

No constituye un estado persistido.

Debe mantenerse:

```text
No Integration

≠

Persisted State
```

---

# Estado Inicial

Toda nueva Integration debe comenzar en:

```text
Draft
```

La única transición desde inexistencia es:

```text
No Integration → Draft
```

---

# Estado Terminal

La versión 1.0 define:

```text
Archived
```

como único estado terminal.

Desde Archived no existe ninguna transición válida.

---

# Diagrama Oficial

```text
                     ┌───────────────┐
                     │ No Integration│
                     └───────┬───────┘
                             │
                             ▼
                        ┌─────────┐
                        │  Draft  │
                        └────┬────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
           ┌─────────┐              ┌──────────┐
           │ Active  │              │ Archived │
           └────┬────┘              └──────────┘
                │
      ┌─────────┴─────────┐
      │                   │
      ▼                   ▼
 ┌───────────┐       ┌──────────┐
 │ Suspended │       │ Archived │
 └─────┬─────┘       └──────────┘
       │
       ├──────────────► Active
       │
       └──────────────► Archived
```

---

# Transiciones Oficiales

La versión 1.0 establece exactamente:

```text
No Integration → Draft

Draft          → Active

Draft          → Archived

Active         → Suspended

Active         → Archived

Suspended      → Active

Suspended      → Archived
```

---

# Matriz Oficial de Transiciones

```text
From             To            Valid

No Integration   Draft         Yes

Draft            Active        Yes

Draft            Suspended     No

Draft            Archived      Yes

Active           Draft         No

Active           Suspended     Yes

Active           Archived      Yes

Suspended        Draft         No

Suspended        Active        Yes

Suspended        Archived      Yes

Archived         Draft         No

Archived         Active        No

Archived         Suspended     No

Archived         Archived      No
```

---

# No Integration → Draft

Esta transición representa la creación formal del Aggregate.

Debe establecer:

```text
IntegrationId

State = Draft

Version

CreatedAt

UpdatedAt
```

conforme a las reglas del Aggregate.

La creación debe ser atómica.

---

# Reglas de Creación

Durante:

```text
No Integration → Draft
```

deben cumplirse:

- IntegrationId válido;
- identidad única;
- Invariants iniciales válidas;
- Version inicial válida;
- CreatedAt establecido;
- UpdatedAt establecido conforme al contrato;
- estado final Draft;
- Domain Event correspondiente cuando sea definido.

---

# Creación Inválida

Si alguna precondición falla:

```text
No Integration
```

permanece:

```text
No Integration
```

No debe existir una Integration parcialmente creada.

---

# Draft → Active

Esta transición representa la habilitación formal de la Integration.

Debe ocurrir únicamente cuando las condiciones de dominio requeridas
hayan sido satisfechas.

---

# Guards de Draft → Active

La transición:

```text
Draft → Active
```

requiere conceptualmente:

- Aggregate existente;
- State actual igual a Draft;
- Command válido;
- Permission válida;
- Invariants satisfechas;
- Version esperada válida cuando corresponda;
- consistencia del Aggregate preservada.

Los Guards específicos se formalizan conjuntamente con Commands e
Invariants.

---

# Draft → Archived

Esta transición representa el retiro formal de una Integration que no
llegó a participar activamente.

Debe mantenerse:

```text
Draft → Archived
```

como transición válida.

---

# Active → Suspended

Esta transición representa suspensión formal.

No representa:

```text
Network Failure

Endpoint Failure

Broker Failure

FIWARE Failure

Timeout
```

---

# Guards de Active → Suspended

Requiere:

- State actual igual a Active;
- intención válida;
- Permission válida;
- Invariants satisfechas;
- Version válida;
- comportamiento explícito del Aggregate.

---

# Active → Archived

Esta transición representa retiro formal desde estado operativo.

Una vez completada:

```text
State = Archived
```

y el Aggregate no vuelve al ciclo operativo.

---

# Suspended → Active

Esta transición representa reactivación formal.

Debe mantenerse:

```text
Suspended → Active
```

como transición válida.

---

# Guards de Suspended → Active

Requiere:

- State actual igual a Suspended;
- intención válida;
- Permission válida;
- Invariants satisfechas;
- Version válida;
- comportamiento explícito del Aggregate.

---

# Suspended → Archived

Esta transición representa retiro definitivo desde suspensión.

Es válida.

---

# Active → Draft Prohibida

No está permitido:

```text
Active → Draft
```

Draft representa exclusivamente etapa inicial.

---

# Suspended → Draft Prohibida

No está permitido:

```text
Suspended → Draft
```

Una Integration que ya salió de Draft no puede regresar a esa etapa.

---

# Archived → Draft Prohibida

No está permitido:

```text
Archived → Draft
```

---

# Archived → Active Prohibida

No está permitido:

```text
Archived → Active
```

---

# Archived → Suspended Prohibida

No está permitido:

```text
Archived → Suspended
```

---

# Archived → Archived

No existe una transición:

```text
Archived → Archived
```

dentro del Lifecycle.

Una operación sin cambio real de dominio no constituye una transición.

---

# Same-State Operations

Una modificación válida futura podría eventualmente mantener el mismo
State si modifica otro aspecto del Aggregate.

Sin embargo:

```text
Same State

≠

Lifecycle Transition
```

Este documento no introduce operaciones adicionales de ese tipo.

---

# Transición y Command

Toda transición debe originarse mediante comportamiento válido del
Aggregate.

Conceptualmente:

```text
Command
    │
    ▼
Integration
    │
    ├── validates current State
    ├── validates Guards
    ├── validates Invariants
    ├── validates Version
    └── performs transition
            │
            ▼
       New State
```

---

# Command no Cambia Estado Directamente

Un Command expresa intención.

Debe mantenerse:

```text
Command

≠

setState()
```

---

# Estado no es Setter Público

No debe existir comportamiento externo equivalente a:

```text
integration.setState(...)
```

que permita evitar reglas del Aggregate.

---

# Relación con Commands

Los Commands oficiales se definen en:

```text
DOMAIN-013C-Commands.md
```

Este documento no inventa nombres de Commands adicionales.

---

# Relación con Domain Events

Una transición confirmada puede producir el Domain Event
correspondiente.

Los eventos oficiales se definen en:

```text
DOMAIN-013D-Domain-Events.md
```

---

# Event after Transition

El Domain Event solamente puede representar una transición que haya
ocurrido realmente.

Debe mantenerse:

```text
Valid Transition
    │
    ▼
New State
    │
    ▼
Domain Event
```

---

# No Event on Rejected Transition

Una transición rechazada no produce un Domain Event de éxito.

Conceptualmente:

```text
Invalid Transition
    │
    ▼
  Rejected
    │
    ├── State unchanged
    ├── Version unchanged
    ├── UpdatedAt unchanged
    └── No success Domain Event
```

---

# Invariants

Toda transición debe preservar:

```text
DOMAIN-013E-Invariants.md
```

Ninguna transición válida puede dejar el Aggregate en un estado que
viole una Invariant.

---

# Permission no Reemplaza State Machine

Debe mantenerse:

```text
Authorized

≠

Transition Allowed
```

Una Permission habilita a intentar una operación.

La State Machine determina si la transición es válida.

---

# State Machine no Reemplaza Permission

Del mismo modo:

```text
Valid State Transition

≠

Authorized Operation
```

Ambos controles son independientes.

---

# Versioning

Toda transición válida modifica el Aggregate.

Por lo tanto debe mantener coherencia con:

```text
DOMAIN-013I-Versioning.md
```

---

# Version Increment

Una transición válida debe provocar:

```text
Version N

→

Version N + 1
```

conforme al contrato de Versioning.

---

# Initial Version

La creación:

```text
No Integration → Draft
```

establece la Version inicial conforme a:

```text
DOMAIN-013I-Versioning.md
```

No debe interpretarse `No Integration` como una entidad persistida con
Version 0.

---

# Rejected Transition y Version

Una operación rechazada:

```text
Version N

→

Version N
```

---

# Optimistic Concurrency

Cuando corresponda:

```text
ExpectedVersion

=

PersistedVersion
```

debe cumplirse antes de confirmar una transición.

---

# Concurrency Conflict

Si:

```text
ExpectedVersion

≠

PersistedVersion
```

la transición debe rechazarse.

El estado persistido no debe sobrescribirse silenciosamente.

---

# State versus Version

Debe mantenerse:

```text
State

≠

Version
```

Version representa evolución lógica.

State representa condición del Lifecycle.

---

# CreatedAt

CreatedAt se establece en creación y permanece inmutable.

Ninguna transición posterior puede modificarlo.

---

# UpdatedAt

Una transición válida actualiza UpdatedAt.

Una transición rechazada no lo modifica.

---

# Identidad

IntegrationId permanece inmutable a través de todas las transiciones.

Conceptualmente:

```text
IntegrationId = X

Draft      X

Active     X

Suspended  X

Archived   X
```

---

# State Transition no Cambia Identidad

Debe mantenerse:

```text
State Change

≠

Identity Change
```

---

# External State

Ningún estado externo puede escribirse directamente como State de
Integration.

Debe mantenerse:

```text
External State

≠

Integration State
```

---

# Source Aggregate State

Un cambio de estado en otro Aggregate no implica automáticamente:

```text
Integration State Change
```

---

# FIWARE State

Un estado proveniente de FIWARE no constituye un State válido de
Integration salvo definición formal explícita.

---

# Municipal State

Un estado proveniente de una plataforma municipal tampoco se convierte
automáticamente en State de Integration.

---

# Technical State

No forman parte de la State Machine:

```text
Connected

Disconnected

Connecting

Reconnecting

Retrying

Queued

Processing

Pending

Published

Failed

Timeout

DeadLettered

Healthy

Unhealthy

Degraded
```

---

# Technical Failure

Debe mantenerse:

```text
Technical Failure

≠

State Transition
```

---

# Timeout

Un timeout no produce:

```text
Active → Suspended
```

automáticamente.

---

# Broker Failure

Una caída de broker no produce:

```text
Active → Suspended
```

automáticamente.

---

# Network Failure

Una caída de red no produce:

```text
Active → Suspended
```

automáticamente.

---

# FIWARE Failure

Una indisponibilidad de FIWARE no produce una transición automática.

---

# Municipal System Failure

Una indisponibilidad municipal no modifica State por sí misma.

---

# External Recovery

El retorno de disponibilidad técnica tampoco produce:

```text
Suspended → Active
```

automáticamente.

---

# Reactivation is Domain Behavior

Debe mantenerse:

```text
Technical Recovery

≠

Domain Reactivation
```

---

# Active State

Active significa:

```text
Formally Enabled
```

No significa:

```text
Technically Reachable
```

---

# Suspended State

Suspended significa:

```text
Formally Suspended
```

No significa:

```text
Temporarily Offline
```

---

# Archived State

Archived significa:

```text
Formally Removed from Operational Lifecycle
```

No significa:

```text
Physically Deleted
```

---

# Draft State

Draft significa:

```text
Formally Defined but Not Active
```

No significa:

```text
Technical Configuration Error
```

---

# State Machine y Consistency Boundary

Toda transición ocurre dentro del Consistency Boundary de Integration.

Debe mantenerse:

```text
Integration State Transition

=

Integration Transaction
```

y no:

```text
Integration State Transition

=

Cross-Aggregate Transaction
```

---

# No Cross-Aggregate Transition

Una transición de Integration no cambia de forma atómica:

```text
Organization

Citizen

Membership

Role

Territory

Assembly

Proposal

Participation

Voting

Document

Notification

Audit
```

---

# External Transaction

Una transición tampoco modifica atómicamente:

```text
FIWARE

Municipal System

External Platform
```

---

# Consistencia Externa

La propagación posterior a otros contextos permanece bajo consistencia
eventual.

Debe mantenerse:

```text
Integration State Commit

before

External Propagation Completion
```

cuando exista propagación.

---

# Publication Failure

Un fallo de publicación posterior no revierte automáticamente una
transición confirmada.

---

# Integration Event

Un Integration Event no forma parte del State de Integration.

Debe mantenerse:

```text
Integration Event

≠

Lifecycle State
```

---

# Domain Event

Un Domain Event representa el hecho de que una transición ocurrió.

No debe utilizarse como mecanismo externo para setear State.

---

# Read Model

El Read Model puede representar State.

No puede modificarlo.

Debe mantenerse:

```text
Read Model State

=

Projection
```

y:

```text
Read Model State

≠

Write Authority
```

---

# Projection Lag

Puede existir temporalmente:

```text
Aggregate State = Active

Read Model State = Draft
```

bajo consistencia eventual.

El Aggregate continúa siendo autoridad.

---

# Repository

El Repository persiste el State.

No decide el State.

Debe mantenerse:

```text
Repository

≠

State Machine
```

---

# Repository Rehydration

Al recuperar el Aggregate:

```text
findById()
```

debe reconstruirse el State confirmado sin ejecutar una nueva
transición.

---

# Rehydration

Debe mantenerse:

```text
Rehydration

≠

State Transition
```

---

# Replay

Cuando Event Sourcing sea utilizado:

```text
Replay

≠

New Transition
```

El replay reconstruye el estado histórico.

---

# Event Sourcing

La State Machine es compatible con Event Sourcing.

Event Sourcing no es obligatorio.

---

# CQRS

En CQRS:

```text
Write Side

owns

State Transitions
```

mientras:

```text
Read Side

projects

State
```

---

# Security

Ningún actor puede modificar State directamente aunque posea
privilegios técnicos elevados.

Debe mantenerse:

```text
Infrastructure Privilege

≠

Domain Transition Authority
```

---

# Authentication

Authentication no modifica la State Machine.

---

# Authorization

Authorization determina si una intención puede ser solicitada.

No modifica las transiciones válidas.

---

# Deny by Default

Una transición que requiera Permission y no esté autorizada debe ser
rechazada.

---

# Direct Database Mutation

No está permitido utilizar modificación directa de persistencia para:

```text
Draft → Active

Active → Suspended

Suspended → Active

* → Archived
```

evitando comportamiento de dominio.

---

# Infrastructure

Infrastructure implementa mecanismos técnicos.

No puede introducir nuevas transiciones.

---

# Adapter

Un Adapter no puede ejecutar:

```text
setState()
```

sobre Integration evitando la Aggregate Root.

---

# Broker

Un Broker no posee autoridad sobre el State.

---

# API

Un endpoint API no constituye una transición.

El endpoint puede representar una entrada hacia un Command, pero la
decisión pertenece al Aggregate.

---

# UI

Una acción de UI tampoco define por sí misma la transición.

---

# Health Check

Un resultado de Health Check:

```text
Healthy

Unhealthy
```

no pertenece a la State Machine.

---

# Deployment

Deployment no cambia State.

---

# Restart

Reiniciar un servicio no cambia State.

---

# Scaling

Escalar horizontalmente Infrastructure no cambia State.

---

# Cache

Cache hit, cache miss o eviction no cambian State.

---

# Replica

Replication no cambia State.

---

# Retry

Retry técnico no cambia State.

---

# Queue

Estados de queue no cambian State.

---

# Outbox

Estados de Outbox no cambian State.

---

# Delivery

Delivery success o delivery failure no cambian State automáticamente.

---

# External Acknowledgement

Un ACK externo no activa automáticamente una Integration.

---

# External Rejection

Un rechazo externo tampoco suspende automáticamente una Integration.

---

# Contract Version

Cambiar una versión de contrato no implica una transición.

Debe mantenerse:

```text
Contract Version Change

≠

State Change
```

---

# API Version

Cambiar API Version no implica State Change.

---

# Schema Version

Cambiar Schema Version no implica State Change.

---

# External Configuration

Cambiar configuración externa no implica State Change.

---

# Credentials

Crear, rotar o expirar credenciales no constituye transición de
Integration.

---

# Security Incident

Un incidente técnico de seguridad no suspende automáticamente la
Integration salvo que una intención formal del dominio provoque dicha
transición.

---

# Audit

Audit puede registrar hechos de transición.

No controla la State Machine.

---

# Notification

Notification puede comunicar cambios.

No controla la State Machine.

---

# Performance

La validación de una transición no debe requerir cargar:

- todos los Integration Aggregates;
- historial global;
- otros Aggregates completos;
- sistemas externos completos;
- Read Models.

---

# No Global State Machine

Cada Integration mantiene su propia State Machine.

Debe mantenerse:

```text
Integration A State

independent from

Integration B State
```

salvo procesos externos explícitos que coordinen comportamientos sin
fusionar Boundaries.

---

# Same IntegrationId

La concurrencia sobre el mismo IntegrationId debe respetar Versioning.

---

# Different IntegrationId

Dos Integration diferentes no comparten State por pertenecer al mismo
Bounded Context.

---

# Illegal Transition

Toda transición no enumerada oficialmente debe considerarse inválida.

Debe mantenerse:

```text
Not Explicitly Allowed

=

Rejected
```

---

# Invalid Transition Result

Ante una transición inválida:

```text
State remains unchanged

Version remains unchanged

UpdatedAt remains unchanged

No success Domain Event
```

---

# Transition Atomicity

Toda transición válida debe ser atómica dentro del Aggregate.

No debe existir:

```text
State changed

but

Version not changed
```

cuando Versioning exija incremento.

Tampoco:

```text
State changed

but

Invariants invalid
```

---

# No Partial State

No deben persistirse estados intermedios como:

```text
Activating

Suspending

Archiving

Reactivating
```

como parte del Lifecycle versión 1.0.

---

# Activating no es State

`Activating` representa como máximo una condición técnica de
procesamiento si alguna implementación la utiliza.

No pertenece al Aggregate.

---

# Suspending no es State

`Suspending` no pertenece al Aggregate.

---

# Archiving no es State

`Archiving` no pertenece al Aggregate.

---

# Reactivating no es State

`Reactivating` no pertenece al Aggregate.

---

# Transition Completion

Una transición válida termina directamente en su estado de destino.

Conceptualmente:

```text
Active
    │
    ▼
Suspended
```

no:

```text
Active
    │
    ▼
Suspending
    │
    ▼
Suspended
```

---

# State Histories

El historial puede registrar transiciones confirmadas.

El historial no es un nuevo State.

---

# Timestamp no Decide State

Un timestamp por sí mismo no produce una transición.

---

# Scheduled Transition

La versión 1.0 no define transiciones automáticas programadas por
tiempo.

Debe mantenerse:

```text
Time Reached

≠

Automatic State Change
```

---

# Expiration

La versión 1.0 no define:

```text
Expired
```

como estado.

---

# Auto-Archive

La versión 1.0 no define archivado automático por tiempo.

---

# Retention

Retention no forma parte de la State Machine.

---

# Deletion

Physical Deletion no forma parte de la State Machine.

---

# Archived y Persistencia

Archived continúa siendo un Aggregate persistido históricamente.

La State Machine no define eliminación posterior.

---

# No State Inference from Provider

Un proveedor externo puede utilizar estados propios.

Por ejemplo:

```text
ENABLED

DISABLED

ERROR

OFFLINE
```

Estos no deben mapearse automáticamente a:

```text
Active

Suspended

Archived
```

sin semántica explícitamente definida.

---

# No State Inference from FIWARE

Un estado FIWARE no redefine la máquina de estados de AURA.

---

# No State Inference from Municipal Systems

Un estado municipal tampoco redefine la máquina.

---

# State Ownership

El State pertenece exclusivamente a:

```text
Integration
```

Debe mantenerse:

```text
External System

does not own

Integration State
```

---

# Transition Ownership

La Aggregate Root es la única autoridad para confirmar una transición.

---

# Guard Ownership

Los Guards de dominio pertenecen al modelo de Integration.

Infrastructure puede validar condiciones técnicas, pero no sustituye
Guards de dominio.

---

# Guard Failure

Ante Guard inválido:

```text
Rejected
```

sin cambio de estado.

---

# Invariant Failure

Ante Invariant inválida:

```text
Rejected
```

sin cambio de estado.

---

# Permission Failure

Ante Permission inválida:

```text
Rejected
```

sin cambio de estado.

---

# Concurrency Failure

Ante ConcurrencyConflict:

```text
Rejected
```

sin sobrescritura silenciosa.

---

# Persistence Failure

Si la transición no logra confirmarse en persistencia:

```text
No Confirmed State Transition
```

no debe considerarse consumada.

---

# Domain Event Failure

No debe considerarse confirmado un nuevo Domain Event de transición si
la modificación del Aggregate no quedó confirmada conforme al contrato
de persistencia.

---

# External Publication Failure

Una vez confirmada una transición, un fallo posterior de publicación
externa no cambia el State.

---

# State Machine y Integration Events

Integration Events pueden reflejar hechos confirmados.

No determinan retrospectivamente si una transición fue válida.

---

# State Machine y Read Models

Un Read Model puede contener una representación desactualizada.

Esto no altera el State del Aggregate.

---

# State Machine y Audit

Audit puede conservar trazabilidad de una transición confirmada.

Audit no puede crear, revertir ni sustituir una transición.

---

# Evolución Futura

Cualquier nuevo State requiere revisión coordinada de:

```text
DOMAIN-013A-Lifecycle.md

DOMAIN-013B-State-Machine.md

DOMAIN-013C-Commands.md

DOMAIN-013D-Domain-Events.md

DOMAIN-013E-Invariants.md

DOMAIN-013F-Permissions.md

DOMAIN-013I-Versioning.md

DOMAIN-013J-Consistency-Boundary.md

DOMAIN-013M-Test-Scenarios.md

DOMAIN-013O-Security-Model.md

DOMAIN-013P-Extension-Points.md
```

---

# Nuevos Estados

No pueden añadirse estados por:

- conveniencia técnica;
- tecnología;
- proveedor;
- broker;
- protocolo;
- UI;
- API;
- framework;
- base de datos.

---

# Nuevas Transiciones

Una nueva transición deberá definir:

- Source State;
- Target State;
- Command;
- Guard;
- Invariants;
- Permission;
- Version impact;
- Domain Event;
- Test Scenarios.

cuando correspondan.

---

# Regla de Exhaustividad

La State Machine opera mediante lista cerrada.

Debe mantenerse:

```text
Allowed Transitions

=

Explicitly Defined Transitions Only
```

---

# Regla de Rechazo por Defecto

Toda transición no declarada debe ser rechazada.

Debe mantenerse:

```text
Unknown Transition

=

Invalid Transition
```

---

# Reglas Fundamentales

La State Machine de Integration debe cumplir:

1. Los únicos estados persistidos oficiales son Draft, Active,
   Suspended y Archived.
2. No Integration representa inexistencia.
3. No Integration no es un State persistido.
4. Toda Integration comienza en Draft.
5. Archived es terminal.
6. No Integration → Draft es válida.
7. Draft → Active es válida.
8. Draft → Archived es válida.
9. Active → Suspended es válida.
10. Active → Archived es válida.
11. Suspended → Active es válida.
12. Suspended → Archived es válida.
13. Active → Draft es inválida.
14. Suspended → Draft es inválida.
15. Archived → Draft es inválida.
16. Archived → Active es inválida.
17. Archived → Suspended es inválida.
18. Archived → Archived no constituye una transición.
19. Toda transición requiere comportamiento explícito.
20. Ningún setter público puede modificar State.
21. Permission no sustituye State Machine.
22. State Machine no sustituye Permission.
23. Toda transición debe preservar Invariants.
24. Toda transición válida debe mantener Versioning.
25. Una transición rechazada no incrementa Version.
26. Una transición rechazada no modifica UpdatedAt.
27. Una transición rechazada no produce Domain Event de éxito.
28. IntegrationId no cambia por transición.
29. CreatedAt no cambia por transición.
30. Technical State no constituye Domain State.
31. Failed no es State oficial.
32. Pending no es State oficial.
33. Connected no es State oficial.
34. Disconnected no es State oficial.
35. Deleted no es State oficial.
36. Cancelled no es State oficial.
37. Activating no es State oficial.
38. Suspending no es State oficial.
39. Archiving no es State oficial.
40. Reactivating no es State oficial.
41. Timeout no produce transición automática.
42. Network Failure no produce transición automática.
43. Broker Failure no produce transición automática.
44. FIWARE Failure no produce transición automática.
45. Municipal System Failure no produce transición automática.
46. Technical Recovery no produce reactivación automática.
47. External Message no cambia State directamente.
48. External Domain Event no cambia State directamente.
49. External Integration Event no cambia State directamente.
50. External State no sustituye Integration State.
51. Source Aggregate State no determina Integration State.
52. FIWARE State no determina Integration State.
53. Municipal State no determina Integration State.
54. Contract Version no determina State.
55. API Version no determina State.
56. Schema Version no determina State.
57. Deployment no cambia State.
58. Restart no cambia State.
59. Scaling no cambia State.
60. Cache no cambia State.
61. Replica no cambia State.
62. Queue State no cambia State.
63. Outbox State no cambia State.
64. Retry técnico no cambia State.
65. Delivery Failure no cambia State automáticamente.
66. Health Check no cambia State.
67. Authentication Failure no cambia State automáticamente.
68. Authorization Failure no cambia State automáticamente.
69. Credentials lifecycle no cambia State automáticamente.
70. Toda transición ocurre dentro del Integration Consistency
    Boundary.
71. Una transición no modifica otros Aggregates atómicamente.
72. Una transición no modifica sistemas externos atómicamente.
73. Consistencia externa permanece eventual.
74. Publication Failure no revierte State confirmado.
75. Integration Event no es Lifecycle State.
76. Read Model no posee autoridad sobre State.
77. Projection Lag no modifica State autoritativo.
78. Repository persiste State pero no lo decide.
79. Rehydration no es transición.
80. Replay no es transición.
81. Event Sourcing permanece compatible pero no obligatorio.
82. Write Side controla transiciones.
83. Query Side proyecta State.
84. No existe Global State Machine compartida entre todos los
    Integration.
85. Cada IntegrationId mantiene su propia State Machine.
86. Same IntegrationId debe respetar Concurrency.
87. Toda transición no declarada explícitamente es inválida.
88. No existen estados intermedios persistidos implícitos.
89. No existen transiciones automáticas programadas por tiempo.
90. Expired no es State oficial.
91. Auto-Archive no está definido.
92. Retention no forma parte de State Machine.
93. Physical Deletion no forma parte de State Machine.
94. Archived conserva significado histórico.
95. Estados de proveedores externos no se mapean automáticamente.
96. La Aggregate Root posee autoridad sobre transiciones.
97. Guard Failure rechaza sin modificar State.
98. Invariant Failure rechaza sin modificar State.
99. ConcurrencyConflict rechaza sin sobrescritura.
100. Nuevos estados o transiciones requieren definición formal.

---

# Restricciones

No está permitido:

- crear Integration en un estado distinto de Draft;
- modificar State directamente;
- exponer setState();
- volver de Active a Draft;
- volver de Suspended a Draft;
- reactivar Archived;
- introducir Failed como State;
- introducir Pending como State;
- introducir Connected como State;
- introducir Disconnected como State;
- introducir Deleted como State;
- introducir Cancelled como State;
- introducir estados técnicos intermedios;
- cambiar State por timeout;
- cambiar State por Network Failure;
- cambiar State por Broker Failure;
- cambiar State por FIWARE Failure;
- cambiar State por Municipal System Failure;
- reactivar por Technical Recovery;
- cambiar State desde Read Model;
- cambiar State desde Repository;
- cambiar State desde Infrastructure;
- cambiar State directamente desde un Adapter;
- cambiar State directamente desde un Integration Event;
- cambiar State directamente desde un Domain Event externo;
- derivar State desde un proveedor externo;
- utilizar Contract Version como State;
- utilizar API Version como State;
- utilizar Health Check como State;
- utilizar Deployment como transición;
- utilizar Retry técnico como transición;
- permitir una transición sin Invariants válidas;
- permitir una transición sin Permission cuando corresponda;
- permitir una transición ignorando Versioning;
- ignorar ConcurrencyConflict;
- persistir un estado intermedio inválido;
- producir un Domain Event de éxito después de una transición
  rechazada;
- ampliar la State Machine por conveniencia técnica;
- introducir nuevos estados o transiciones sin definición formal.

---

# Compatibilidad Arquitectónica

La State Machine de Integration es compatible con:

- Domain-Driven Design;
- Aggregate Pattern;
- State Machine Pattern;
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

Estas compatibilidades no imponen tecnologías ni mecanismos de
Infrastructure.

---

# Definición de Éxito

La State Machine del Aggregate **Integration** protege formalmente la
evolución de una relación de interoperabilidad dentro de AURA.

El modelo queda definido exactamente por:

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

y garantiza que:

- Draft sea el único estado inicial;
- Active represente habilitación formal;
- Suspended represente suspensión formal;
- Archived sea terminal;
- ninguna transición pueda evitar Guards;
- ninguna transición pueda evitar Invariants;
- ninguna transición pueda evitar Permissions;
- ninguna transición pueda evitar Versioning;
- IntegrationId permanezca inmutable;
- CreatedAt permanezca inmutable;
- operaciones rechazadas no cambien State ni Version;
- estados técnicos permanezcan fuera del dominio;
- fallos técnicos no produzcan cambios automáticos;
- recuperación técnica no produzca reactivación automática;
- sistemas externos no posean autoridad sobre State;
- FIWARE no determine State;
- sistemas municipales no determinen State;
- Repository no determine State;
- Read Models no determinen State;
- Infrastructure no determine State;
- cada Integration mantenga su propio Consistency Boundary;
- consistencia externa permanezca eventual;
- Archived no implique eliminación física;
- toda transición no declarada sea inválida;
- toda evolución futura de la State Machine requiera una definición
  formal y coordinada.

De esta forma, `DOMAIN-013B-State-Machine.md` establece formalmente
la State Machine oficial del Aggregate **Integration** conforme al
patrón consolidado de AURA Core.