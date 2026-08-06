# DOMAIN-003M — Membership Test Scenarios

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Membership Management

Aggregate:
Membership

Documentos relacionados:

- DOMAIN-003-Aggregate.md
- DOMAIN-003A-Lifecycle.md
- DOMAIN-003B-State-Machine.md
- DOMAIN-003C-Commands.md
- DOMAIN-003D-Domain-Events.md
- DOMAIN-003E-Invariants.md
- DOMAIN-003F-Permissions.md
- DOMAIN-003G-Repository-Contract.md
- DOMAIN-003L-Read-Model.md
- CORE-014-Domain-Error-Model.md

---

# Objetivo

Este documento define los escenarios oficiales de prueba para el
Aggregate **Membership**.

Los escenarios verifican que el Aggregate implemente correctamente
las reglas del dominio, preserve sus invariantes y mantenga un
comportamiento determinístico frente a comandos válidos e
inválidos.

Las pruebas descritas son independientes del lenguaje de
programación, framework o mecanismo de persistencia.

---

# Principios

Los escenarios de prueba siguen los principios de:

- Domain-Driven Design (DDD);
- Specification by Example;
- Behavior Driven Development (BDD);
- Given / When / Then;
- determinismo;
- repetibilidad.

---

# Cobertura

Las pruebas validan:

- creación;
- ciclo de vida;
- transiciones de estado;
- invariantes;
- autorización;
- concurrencia;
- persistencia;
- emisión de eventos;
- consistencia.

---

# Escenario 1 — Crear una Membership

## Given

```text
Citizen existente

Organization existente

No existe Membership activa
```

## When

```text
CreateMembership
```

## Then

```text
Membership creada

Version = 1

State = Draft

Evento:

MembershipCreated
```

---

# Escenario 2 — Solicitar incorporación

## Given

```text
Membership = Draft
```

## When

```text
RequestMembership
```

## Then

```text
State = PendingApproval

Evento:

MembershipRequested
```

---

# Escenario 3 — Aprobar solicitud

## Given

```text
State = PendingApproval
```

## When

```text
ApproveMembership
```

## Then

```text
State = Approved

Evento:

MembershipApproved
```

---

# Escenario 4 — Activar Membership

## Given

```text
State = Approved
```

## When

```text
ActivateMembership
```

## Then

```text
State = Active

ActivationDate definida

Evento:

MembershipActivated
```

---

# Escenario 5 — Rechazar solicitud

## Given

```text
State = PendingApproval
```

## When

```text
RejectMembership
```

## Then

```text
State = Rejected

Evento:

MembershipRejected
```

---

# Escenario 6 — Suspender Membership

## Given

```text
State = Active
```

## When

```text
SuspendMembership
```

## Then

```text
State = Suspended

Evento:

MembershipSuspended
```

---

# Escenario 7 — Reactivar Membership

## Given

```text
State = Suspended
```

## When

```text
ReactivateMembership
```

## Then

```text
State = Active

Evento:

MembershipReactivated
```

---

# Escenario 8 — Finalizar Membership

## Given

```text
State = Active
```

## When

```text
TerminateMembership
```

## Then

```text
State = Terminated

TerminationDate definida

Evento:

MembershipTerminated
```

---

# Escenario 9 — Archivar Membership

## Given

```text
State = Terminated
```

## When

```text
ArchiveMembership
```

## Then

```text
State = Archived

ArchiveDate definida

Evento:

MembershipArchived
```

---

# Escenario 10 — Evitar Membership duplicada

## Given

```text
Citizen = Juan Pérez

Organization = Junta Vecinal Norte

Membership existente = Active
```

## When

```text
CreateMembership
```

## Then

```text
Command Rejected

DuplicateActiveMembership
```

No debe persistirse ningún cambio.

---

# Escenario 11 — Activación inválida

## Given

```text
State = Draft
```

## When

```text
ActivateMembership
```

## Then

```text
InvalidStateTransition
```

No cambia el estado.

No cambia la versión.

No se generan eventos.

---

# Escenario 12 — Reactivación inválida

## Given

```text
State = Terminated
```

## When

```text
ReactivateMembership
```

## Then

```text
Command Rejected
```

La Membership permanece terminada.

---

# Escenario 13 — Modificar Membership archivada

## Given

```text
State = Archived
```

## When

```text
SuspendMembership
```

## Then

```text
Command Rejected
```

El Aggregate permanece inmutable.

---

# Escenario 14 — Verificar incremento de versión

## Given

```text
Version = 4
```

## When

```text
SuspendMembership
```

## Then

```text
Version = 5
```

---

# Escenario 15 — Command rechazado

## Given

```text
Version = 8
```

## When

```text
ApproveMembership
```

sobre una Membership ya activa.

## Then

```text
Version = 8
```

No se generan eventos.

---

# Escenario 16 — Concurrencia optimista

## Given

```text
Cliente A

Version = 12

Cliente B

Version = 12
```

## When

```text
Cliente A guarda correctamente.
```

Posteriormente:

```text
Cliente B intenta guardar.
```

## Then

```text
ConcurrencyConflict
```

---

# Escenario 17 — Validación de permisos

## Given

```text
Citizen común
```

## When

```text
ApproveMembership
```

## Then

```text
AccessDenied
```

El Aggregate nunca es ejecutado.

---

# Escenario 18 — Persistencia

## Given

```text
Membership modificada
```

## When

```text
Repository.save()
```

## Then

```text
Aggregate persistido

Eventos persistidos

Commit exitoso
```

---

# Escenario 19 — Reconstrucción mediante eventos

## Given

```text
Historial completo de Domain Events
```

## When

```text
Replay
```

## Then

```text
Aggregate reconstruido

Estado consistente

Version correcta
```

---

# Escenario 20 — Actualización del Read Model

## Given

```text
MembershipActivated
```

## When

```text
Projection Handler
```

## Then

```text
Read Model actualizado

Estado = Active
```

---

# Escenario 21 — Publicación de Integration Event

## Given

```text
Commit exitoso
```

## When

```text
Outbox Processor
```

## Then

```text
MembershipActivatedIntegrationEvent publicado
```

Nunca antes del commit.

---

# Escenario 22 — Integración con FIWARE

## Given

```text
MembershipActivatedIntegrationEvent
```

## When

```text
Integration Adapter
```

## Then

```text
Actualización del contexto ciudadano
en FIWARE NGSI-LD.
```

La operación no modifica el Aggregate.

---

# Escenario 23 — Auditoría

## Given

```text
TerminateMembership
```

## When

```text
Commit exitoso
```

## Then

Debe registrarse:

```text
ActorId

MembershipId

Command

Version

OccurredOn
```

---

# Escenario 24 — Recuperación tras fallo

## Given

```text
Persistencia del Aggregate exitosa

Falla temporal del Broker
```

## When

```text
Outbox Retry
```

## Then

```text
Integration Event publicado

Sin duplicar el Aggregate

Sin pérdida de información
```

---

# Escenario 25 — Inmutabilidad del historial

## Given

```text
Membership con múltiples Domain Events
```

## When

```text
Consulta histórica
```

## Then

Todos los eventos:

- conservan su orden;
- permanecen inmutables;
- mantienen la versión original;
- conservan su marca temporal.

---

# Criterios de Aceptación

El Aggregate supera la validación cuando:

- todas las invariantes permanecen satisfechas;
- toda transición sigue la máquina de estados;
- ningún Command inválido modifica el Aggregate;
- cada cambio exitoso incrementa la versión;
- todos los Domain Events son emitidos correctamente;
- los Integration Events se publican únicamente tras el commit;
- el Read Model refleja los cambios mediante consistencia eventual;
- la concurrencia optimista impide sobrescrituras;
- el historial puede reconstruirse íntegramente.

---

# Automatización Recomendada

Se recomienda implementar estos escenarios mediante:

- pruebas unitarias del Aggregate;
- pruebas de integración del Repository;
- pruebas de contratos para Integration Events;
- pruebas de proyección para Read Models;
- pruebas de aceptación basadas en BDD;
- pruebas de concurrencia;
- pruebas de rendimiento para consultas y persistencia.

---

# Principios Arquitectónicos

Este documento sigue:

- Domain-Driven Design (DDD);
- Behavior Driven Development (BDD);
- Specification by Example;
- CQRS;
- Event Sourcing;
- Clean Architecture;
- Test Pyramid.

---

# Definición de Éxito

Los escenarios de prueba del Aggregate **Membership** validan
que toda relación entre un **Citizen** y una **Organization**
evolucione conforme a las reglas del dominio AURA. Las pruebas
garantizan la preservación de las invariantes, la consistencia
transaccional, la correcta emisión de eventos y la capacidad de
integración con arquitecturas basadas en **CQRS**, **Event
Sourcing** y **Event-Driven Architecture**, proporcionando una
base verificable y confiable para la evolución del sistema.