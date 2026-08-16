# DOMAIN-012B — Audit State Machine

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Audit Management

Aggregate:
Audit

Documentos relacionados:

- DOMAIN-012-Aggregate.md
- DOMAIN-012A-Lifecycle.md
- DOMAIN-012C-Commands.md
- DOMAIN-012D-Domain-Events.md
- DOMAIN-012E-Invariants.md
- DOMAIN-012I-Versioning.md
- DOMAIN-012J-Consistency-Boundary.md

---

# Objetivo

Este documento define formalmente la **State Machine** del
Aggregate **Audit**.

La State Machine establece:

- los estados válidos;
- el estado inicial;
- los estados terminales;
- las transiciones permitidas;
- las transiciones prohibidas;
- las condiciones generales que deben preservarse durante cada
  transición.

La State Machine debe permanecer completamente coherente con:

```text
DOMAIN-012A-Lifecycle.md
```

No introduce estados adicionales.

---

# Principio Fundamental

Audit representa una unidad de trazabilidad de un hecho ya
confirmado.

Por esta razón, la versión 1.0 mantiene una State Machine mínima.

Debe mantenerse:

```text
Source Aggregate State Machine

≠

Audit State Machine
```

Audit no reproduce los estados del Aggregate que originó el hecho
auditable.

---

# Estados Oficiales

La versión 1.0 define un único estado persistido:

```text
Recorded
```

Conceptualmente existe además:

```text
No Audit
```

para representar la inexistencia previa del Aggregate.

`No Audit` no constituye un estado persistido.

---

# Modelo Oficial

La State Machine completa es:

```text
No Audit
    │
    ▼
Recorded
```

No existen otras transiciones oficiales en la versión 1.0.

---

# No Audit

`No Audit` representa:

```text
Aggregate Does Not Exist
```

No posee:

- AuditId;
- Version;
- CreatedAt;
- estado persistido;
- historial propio del Aggregate.

No Audit no es un valor válido de AuditStatus.

Es únicamente la condición conceptual previa a la creación del
Aggregate.

---

# Recorded

`Recorded` representa una unidad Audit formalmente existente y
confirmada.

En este estado:

- AuditId existe;
- AuditId permanece inmutable;
- el hecho auditable ya ocurrió;
- las referencias de origen aplicables están preservadas;
- la representación histórica mantiene su significado;
- Version pertenece a Audit;
- CreatedAt pertenece a Audit;
- las Invariants deben cumplirse;
- el Aggregate puede ser recuperado mediante Repository;
- el Aggregate puede alimentar Read Models;
- el Aggregate originador permanece independiente.

---

# Estado Inicial

El único estado inicial válido es:

```text
Recorded
```

después de la transición conceptual:

```text
No Audit → Recorded
```

No existe una instancia Audit persistida antes de Recorded.

---

# Estado Terminal

`Recorded` es terminal en la versión 1.0.

Debe mantenerse:

```text
Recorded

=

Terminal
```

Ninguna transición ordinaria parte desde Recorded hacia otro estado.

---

# Transición Oficial

La única transición oficial es:

```text
No Audit → Recorded
```

Esta transición representa la creación válida de una unidad Audit
a partir de un hecho auditable ya confirmado.

---

# Condición de Entrada

La transición:

```text
No Audit → Recorded
```

solamente puede ocurrir cuando existe información suficiente para
representar válidamente un hecho auditable.

Debe mantenerse:

```text
Confirmed Auditable Fact

before

Recorded Audit
```

Audit no anticipa hechos futuros.

---

# Resultado de la Transición

Después de:

```text
No Audit → Recorded
```

debe existir un Aggregate válido con:

```text
AuditId

Recorded State

Version

CreatedAt
```

y las referencias auditables requeridas conforme al contrato de
origen.

---

# Atomicidad

La transición debe confirmarse como una única modificación coherente
del Aggregate.

No debe existir un estado confirmado equivalente a:

```text
AuditId exists

+

State missing
```

ni:

```text
State = Recorded

+

Invalid AuditId
```

ni cualquier otra combinación parcial incompatible con las
Invariants.

---

# Version Inicial

Después de una creación válida:

```text
State = Recorded

Version = 1
```

conforme al patrón consolidado de Versioning de AURA.

La definición completa pertenece a:

```text
DOMAIN-012I-Versioning.md
```

---

# CreatedAt

La transición:

```text
No Audit → Recorded
```

establece:

```text
CreatedAt
```

para el Aggregate.

CreatedAt permanece inmutable posteriormente.

---

# Source Fact

La State Machine de Audit no cambia el estado del hecho originador.

Debe mantenerse:

```text
Audit State Transition

≠

Source Fact Transition
```

El hecho auditado ya fue confirmado antes de que Audit alcance
Recorded.

---

# Source Aggregate

Si el origen pertenece a otro Aggregate:

```text
Source Aggregate
    │
    ▼
Confirmed Fact
    │
    ▼
No Audit
    │
    ▼
Recorded
```

la transición solamente afecta a Audit.

No produce una transición simultánea del Source Aggregate.

---

# Independencia de Version

La transición de Audit mantiene su propia Version.

Debe mantenerse:

```text
Audit.Version

≠

SourceAggregateVersion
```

La existencia de:

```text
SourceAggregateVersion = N
```

no obliga a que:

```text
Audit.Version = N
```

Audit comienza su propia evolución conforme a sus reglas.

---

# Transiciones Permitidas

La matriz oficial es:

| Estado previo | Estado resultante |
|---|---|
| No Audit | Recorded |

No existen otras transiciones permitidas en la versión 1.0.

---

# Transiciones Prohibidas

No están permitidas:

```text
Recorded → Recorded
```

como transición de Lifecycle.

Tampoco:

```text
Recorded → Draft

Recorded → Pending

Recorded → Active

Recorded → Failed

Recorded → Cancelled

Recorded → Archived

Recorded → Deleted
```

ni cualquier otro estado no definido oficialmente.

---

# Recorded → Recorded

Una operación futura que preserve el mismo estado no constituye
automáticamente una transición de State Machine.

Debe mantenerse:

```text
Same State Modification

≠

State Transition
```

La versión 1.0 no define comportamiento adicional que modifique
Audit manteniéndolo en Recorded.

---

# Draft

`Draft` no forma parte de la State Machine.

No existe:

```text
No Audit → Draft
```

ni:

```text
Draft → Recorded
```

en la versión 1.0.

---

# Pending

`Pending` no forma parte de la State Machine.

El procesamiento técnico pendiente no debe convertirse en estado de
dominio.

Debe mantenerse:

```text
Technical Pending

≠

Audit State
```

---

# Active

`Active` no forma parte de la State Machine.

Audit no representa una operación activa.

Representa una unidad histórica confirmada.

---

# Failed

`Failed` no forma parte de la State Machine.

Fallos de:

- procesamiento;
- persistencia;
- transporte;
- integración;
- infraestructura;

no producen:

```text
AuditStatus = Failed
```

Debe mantenerse:

```text
Technical Failure

≠

Audit State
```

---

# Cancelled

`Cancelled` no forma parte de la State Machine.

Audit no cancela retrospectivamente un hecho ya ocurrido.

Debe mantenerse:

```text
Audit Cancelled

≠

Source Fact Cancelled
```

---

# Archived

`Archived` no forma parte de la State Machine versión 1.0.

La naturaleza histórica de Audit no permite inferir automáticamente
un estado Archived.

Debe mantenerse:

```text
Historical

≠

Archived State
```

---

# Deleted

`Deleted` no forma parte de la State Machine.

La eliminación física no es una transición de dominio.

Debe mantenerse:

```text
Physical Deletion

≠

State Transition
```

---

# Estados de Infrastructure

No forman parte de la State Machine:

```text
Queued

Processing

Persisting

Retrying

Published

DeliveryFailed

DeadLettered
```

cuando representan estados técnicos.

Estos conceptos pertenecen a procesos externos al Aggregate.

---

# Regla de Validación

Toda operación que pretenda modificar el estado debe validar primero
que la transición exista formalmente.

Conceptualmente:

```text
Requested Transition
    │
    ▼
State Machine
    │
    ├── Allowed
    │       │
    │       ▼
    │   Validate Invariants
    │
    └── Not Allowed
            │
            ▼
         Reject
```

---

# Rechazo

Si una transición no pertenece a la State Machine:

```text
Operation

↓

Rejected
```

y debe mantenerse:

- estado previo;
- Version previa;
- UpdatedAt previo;
- ausencia de Domain Event de éxito.

---

# Operación Rechazada

Una operación rechazada no puede:

- crear Recorded;
- cambiar AuditId;
- incrementar Version;
- modificar CreatedAt;
- producir una transición parcial;
- producir un Domain Event de éxito.

---

# State Mutation

No está permitido:

```text
setState(...)
```

como operación pública arbitraria.

El estado solamente puede establecerse como consecuencia del
comportamiento válido del Aggregate.

Debe mantenerse:

```text
State Mutation

through

Aggregate Behavior
```

---

# State y AuditId

AuditId y State deben permanecer coherentes.

Una vez que:

```text
AuditId = A
```

y:

```text
State = Recorded
```

la identidad no puede cambiar debido a ninguna futura operación.

---

# State y CreatedAt

Recorded implica que el Aggregate ya fue creado.

Por lo tanto:

```text
State = Recorded

requires

CreatedAt
```

conforme a las Invariants oficiales.

---

# State y Source Reference

Recorded debe representar un hecho auditable identificable conforme
al contrato recibido.

La forma concreta de identificación dependerá del hecho de origen.

La State Machine no inventa referencias faltantes.

Debe mantenerse:

```text
Recorded

≠

Permission to Fabricate Source Data
```

---

# State y ActorId

ActorId no determina el estado.

Puede existir cuando el contrato de origen lo proporciona.

Debe mantenerse:

```text
ActorId Presence

≠

Audit State
```

y:

```text
ActorId Absence

≠

New Audit State
```

---

# State y CorrelationId

CorrelationId no determina una transición.

Su presencia o ausencia pertenece a la información de trazabilidad
disponible.

Debe mantenerse:

```text
CorrelationId

≠

State
```

---

# State y CausationId

CausationId no determina una transición.

Debe mantenerse:

```text
CausationId

≠

State
```

---

# State y Domain Events

Los Domain Events propios de Audit deberán corresponder a
comportamiento válido del Aggregate.

La State Machine no introduce nombres de eventos.

Debe mantenerse:

```text
Valid State Transition

may produce

Audit Domain Event
```

únicamente conforme a:

```text
DOMAIN-012D-Domain-Events.md
```

---

# Source Domain Event

Un Source Domain Event no constituye un estado de Audit.

Debe mantenerse:

```text
SourceEventType

≠

Audit State
```

Por ejemplo, un hecho:

```text
NotificationDeliveryFailed
```

no produce:

```text
AuditStatus = Failed
```

El Audit resultante permanece:

```text
Recorded
```

---

# Estado del Aggregate Originador

Audit no hereda estados externos.

Debe mantenerse:

```text
Source Status

≠

Audit Status
```

Ejemplos:

```text
AssemblyStatus = Cancelled

↓

AuditStatus = Recorded
```

```text
DocumentStatus = Archived

↓

AuditStatus = Recorded
```

```text
NotificationStatus = Failed

↓

AuditStatus = Recorded
```

cuando dichos hechos sean auditables.

---

# Estado y Consistency Boundary

La State Machine afecta exclusivamente:

```text
Audit
```

No modifica:

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

Integration
```

---

# Atomicidad entre Aggregates

No existe una transición distribuida equivalente a:

```text
Source Aggregate Transition

+

Audit Transition

=

Single Aggregate Transaction
```

Debe mantenerse:

```text
Source Aggregate Transaction

≠

Audit Transaction
```

---

# Consistencia Eventual

Puede existir:

```text
Source Fact Confirmed

↓

Audit not yet Recorded
```

durante una ventana temporal válida.

Posteriormente:

```text
Audit Recorded
```

completa la representación auditable sin modificar el hecho
original.

---

# Fallo antes de Recorded

Si el procesamiento falla antes de confirmar Audit:

```text
No Audit
```

permanece conceptualmente como inexistencia del Aggregate.

No debe persistirse:

```text
Failed Audit
```

porque Failed no pertenece a la State Machine.

---

# Retry Técnico

Un reintento técnico puede volver a intentar procesar el mismo hecho
auditable.

Mientras no se confirme la creación:

```text
No Audit
```

continúa siendo la condición conceptual.

Cuando la creación es aceptada:

```text
No Audit → Recorded
```

ocurre una sola vez para la unidad Audit correspondiente.

---

# Duplicate Delivery

La entrega técnica duplicada de un mismo hecho no introduce:

```text
Recorded → Recorded
```

como transición.

Debe mantenerse:

```text
Duplicate Delivery

≠

Lifecycle Transition
```

La idempotencia técnica permanece fuera de la State Machine.

---

# Read Models

Los Read Models pueden proyectar:

```text
Recorded
```

como estado conocido de una unidad Audit.

Una proyección:

- no cambia el estado;
- no crea una transición;
- no incrementa Version;
- no reemplaza la State Machine.

---

# Repository

El Repository persiste y recupera Audit.

No decide:

- estados válidos;
- transiciones;
- estados terminales;
- Invariants.

Debe mantenerse:

```text
Repository

≠

State Machine
```

---

# Persistencia

La persistencia no puede modificar arbitrariamente:

```text
Recorded
```

ni crear estados técnicos dentro del Aggregate.

Cualquier representación física debe reconstruir exactamente el
estado válido definido por el dominio.

---

# Versioning

La transición válida:

```text
No Audit → Recorded
```

produce la Version inicial oficial:

```text
Version = 1
```

Una transición rechazada no incrementa Version.

La State Machine y Versioning deben permanecer coherentes.

---

# Optimistic Concurrency

Cualquier modificación futura oficialmente permitida deberá
preservar Optimistic Concurrency mediante Version.

La State Machine no permite utilizar un conflicto de concurrencia
para introducir un nuevo estado.

Debe mantenerse:

```text
ConcurrencyConflict

≠

Audit State
```

---

# Permissions

Una Permission válida no permite ejecutar una transición inexistente.

Debe mantenerse:

```text
Authorized

≠

Valid Transition
```

La operación debe cumplir simultáneamente:

```text
Permission

+

State Machine

+

Invariants
```

---

# Security

Ningún privilegio puede:

- cambiar Recorded a otro estado;
- crear un estado inexistente;
- evitar las Invariants;
- modificar AuditId;
- modificar directamente Version.

Debe mantenerse:

```text
Elevated Privilege

≠

State Machine Override
```

---

# Integration Events

La publicación de un Integration Event no modifica:

```text
State = Recorded
```

Debe mantenerse:

```text
Integration Publication

≠

Audit Transition
```

---

# Outbox

El estado técnico de Outbox no forma parte de Audit.

Valores como:

```text
Pending

Published

Failed

Retrying
```

dentro de una Outbox no pueden reinterpretarse como AuditStatus.

---

# CQRS

En el Write Side:

```text
No Audit
    │
    ▼
Recorded
```

En el Read Side:

```text
Recorded Fact
    │
    ▼
Projection
    │
    ▼
Read Model
```

La State Machine pertenece al Write Model.

---

# Event Sourcing

Si Audit utiliza Event Sourcing, la reconstrucción debe producir un
estado compatible con:

```text
Recorded
```

Los eventos concretos necesarios para la reconstrucción pertenecen
a:

```text
DOMAIN-012D-Domain-Events.md
```

La reconstrucción no genera una nueva transición.

---

# Rehidratación

Cuando Audit es rehidratado:

```text
Recorded
```

debe reconstruirse sin:

- ejecutar Commands;
- producir nuevos Domain Events;
- incrementar Version;
- modificar CreatedAt.

Debe mantenerse:

```text
Rehydration

≠

State Transition
```

---

# Evolución Futura

Cualquier nuevo estado requerirá actualización coordinada de:

```text
DOMAIN-012-Aggregate.md

DOMAIN-012A-Lifecycle.md

DOMAIN-012B-State-Machine.md

DOMAIN-012C-Commands.md

DOMAIN-012D-Domain-Events.md

DOMAIN-012E-Invariants.md

DOMAIN-012H-Examples.md

DOMAIN-012M-Test-Scenarios.md
```

cuando corresponda.

Un estado no puede incorporarse aisladamente.

---

# Estados No Definidos

La versión 1.0 no define:

```text
Draft

Pending

Active

Failed

Cancelled

Archived

Deleted

Suspended

Expired

Invalidated
```

Ninguno debe utilizarse sin una evolución explícita del modelo.

---

# Regla para Incorporar un Nuevo Estado

Un nuevo estado solamente puede incorporarse cuando represente una
condición real y diferenciable del dominio Audit.

Debe responder afirmativamente:

```text
¿Representa una condición real del dominio?

¿Cambia el comportamiento permitido del Aggregate?

¿Requiere Guards o Invariants diferentes?

¿Posee transición explícita de entrada?

¿Posee significado dentro del Ubiquitous Language?

¿No representa solamente un estado técnico?
```

Si estas condiciones no se cumplen, el concepto no debe añadirse a
la State Machine.

---

# Matriz Oficial

| Origen | Destino | Permitida | Significado |
|---|---|---|---|
| No Audit | Recorded | Sí | Creación válida de una unidad Audit |
| Recorded | Recorded | No como transición | No existe transición de Lifecycle |
| Recorded | Draft | No | Estado inexistente |
| Recorded | Pending | No | Estado inexistente |
| Recorded | Active | No | Estado inexistente |
| Recorded | Failed | No | Estado inexistente |
| Recorded | Cancelled | No | Estado inexistente |
| Recorded | Archived | No | Estado inexistente |
| Recorded | Deleted | No | Estado inexistente |

---

# Diagrama Oficial

```text
                     ┌────────────────────────┐
                     │ Confirmed Source Fact  │
                     └────────────┬───────────┘
                                  │
                                  ▼
                          ┌──────────────┐
                          │   No Audit   │
                          └──────┬───────┘
                                 │
                                 │ valid creation
                                 ▼
                          ┌──────────────┐
                          │   Recorded   │
                          └──────────────┘

                              TERMINAL
```

---

# Reglas Fundamentales

La State Machine debe cumplir:

1. Existe un único estado persistido: Recorded.
2. No Audit representa inexistencia y no es un estado persistido.
3. La única transición válida es No Audit → Recorded.
4. Recorded es el estado inicial persistido.
5. Recorded es terminal.
6. No existe Draft.
7. No existe Pending.
8. No existe Active.
9. No existe Failed.
10. No existe Cancelled.
11. No existe Archived.
12. No existe Deleted.
13. Estados técnicos no forman parte del dominio.
14. Audit no hereda estados del Aggregate originador.
15. El hecho de origen debe estar confirmado antes de Recorded.
16. La transición afecta únicamente a Audit.
17. AuditId permanece inmutable.
18. Version pertenece exclusivamente a Audit.
19. SourceAggregateVersion no determina Audit.Version.
20. Una transición rechazada no modifica estado ni Version.
21. Repository no decide transiciones.
22. Permissions no pueden evitar la State Machine.
23. Read Models no modifican estado.
24. Integration Events no modifican estado.
25. Reintentos técnicos no constituyen transiciones.
26. Duplicados técnicos no constituyen transiciones.
27. Rehidratación no constituye transición.
28. Event Sourcing no altera las reglas de estado.
29. Cualquier nuevo estado requiere evolución explícita y coordinada.

---

# Definición de Éxito

La State Machine del Aggregate **Audit** establece formalmente una
máquina de estados mínima y coherente con su responsabilidad de
preservar trazabilidad histórica.

La versión 1.0 define exclusivamente:

```text
No Audit → Recorded
```

donde:

- No Audit representa inexistencia del Aggregate;
- Recorded representa una unidad Audit válida y confirmada;
- Recorded es el único estado persistido;
- Recorded es inicial;
- Recorded es terminal;
- no existen transiciones posteriores;
- no existen estados Draft, Pending, Active, Failed, Cancelled,
  Archived o Deleted;
- los estados técnicos permanecen fuera del dominio;
- Audit no hereda el estado del Aggregate originador;
- la transición solamente ocurre después de un hecho auditable
  confirmado;
- Audit mantiene identidad y Version propias;
- SourceAggregateVersion permanece independiente;
- el Source Aggregate no se modifica;
- las transiciones rechazadas no producen cambios;
- Repository, Read Models, Integration Events y Infrastructure no
  poseen autoridad sobre el estado;
- CQRS y Event Sourcing permanecen compatibles;
- cualquier evolución futura requiere definición explícita y
  coordinada.

De esta forma, `DOMAIN-012B-State-Machine.md` establece la State
Machine oficial del Aggregate **Audit** conforme al patrón
consolidado de AURA Core.