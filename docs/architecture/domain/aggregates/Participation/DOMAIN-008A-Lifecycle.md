# DOMAIN-008A — Participation Lifecycle

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Participation Management

Aggregate:
Participation

Autor:
ARADA

Documentos relacionados:

- DOMAIN-008-Aggregate.md
- DOMAIN-008B-State-Machine.md
- DOMAIN-008C-Commands.md
- DOMAIN-008D-Domain-Events.md
- DOMAIN-008E-Invariants.md
- DOMAIN-008F-Permissions.md
- DOMAIN-008G-Repository-Contract.md
- DOMAIN-008H-Examples.md
- DOMAIN-008I-Versioning.md
- DOMAIN-008J-Consistency-Boundary.md
- DOMAIN-008K-Integration-Events.md
- DOMAIN-008L-Read-Model.md
- DOMAIN-008M-Test-Scenarios.md
- DOMAIN-008N-Performance-Rules.md
- DOMAIN-008O-Security-Model.md
- DOMAIN-008P-Extension-Points.md
- CORE-003-Shared-Kernel.md
- CORE-004-Ubiquitous-Language.md
- CORE-006-Domain-Invariants.md
- CORE-007-Strategic-Design.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Definir el ciclo de vida oficial del Aggregate
**Participation**.

El Lifecycle establece las etapas conceptuales por las cuales una
Participation puede evolucionar desde su creación hasta su
conservación lógica final.

El ciclo de vida determina:

- estado inicial;
- estados intermedios;
- estados terminales;
- estados de conservación;
- caminos principales;
- caminos alternativos;
- condiciones generales de transición;
- restricciones posteriores a cada estado;
- coherencia temporal;
- relación entre estado, Commands y Domain Events.

El Lifecycle no reemplaza la State Machine.

Este documento define el significado conceptual de cada etapa y la
evolución general del Aggregate.

La definición formal de transiciones permitidas y prohibidas se
establece en:

```text
DOMAIN-008B-State-Machine.md
```

---

# Propósito

El propósito del Lifecycle es garantizar que una Participation no
pueda evolucionar arbitrariamente.

Toda Participation debe atravesar únicamente estados reconocidos
por el dominio.

El ciclo de vida protege:

- identidad;
- contexto organizacional;
- actor participante;
- contexto participativo;
- estado;
- temporalidad;
- trazabilidad;
- Version;
- coherencia entre hechos;
- restricciones de modificación.

El Lifecycle permite distinguir entre:

```text
Participation Registered

Participation Active

Participation Completed

Participation Withdrawn

Participation Invalidated

Participation Archived
```

Cada estado representa una condición diferente del Aggregate.

---

# Principios

El Lifecycle de Participation sigue los siguientes principios:

- toda Participation comienza en un estado definido;
- ningún estado se asigna directamente;
- toda transición representa comportamiento de dominio;
- toda transición debe respetar invariantes;
- toda transición debe respetar Permissions;
- toda transición válida produce una nueva revisión del Aggregate;
- toda transición válida incrementa Version;
- toda transición válida puede producir Domain Events;
- toda transición rechazada mantiene el estado anterior;
- toda transición rechazada mantiene Version;
- los estados terminales restringen comportamiento posterior;
- Archived representa conservación lógica;
- el Lifecycle no modifica otros Aggregates;
- los estados de otros Aggregates no modifican automáticamente
  Participation;
- la evolución del Aggregate permanece independiente de
  Infrastructure.

---

# Regla Fundamental

Debe mantenerse:

```text
Current State

+

Valid Command

+

Valid Permission

+

Valid Invariants

↓

Valid Transition

↓

New State
```

No debe existir:

```text
Current State

↓

Direct Status Assignment

↓

New State
```

El estado no puede modificarse mediante asignación arbitraria.

---

# Estados Oficiales

El Lifecycle oficial de Participation utiliza:

```text
Registered

Active

Completed

Withdrawn

Invalidated

Archived
```

Estos estados constituyen las condiciones conceptuales oficiales
del Aggregate definidas en:

```text
DOMAIN-008-Aggregate.md
```

No deben incorporarse estados adicionales sin una evolución
explícita del dominio.

---

# Estado Inicial

Toda Participation creada válidamente inicia en:

```text
Registered
```

Conceptualmente:

```text
RegisterParticipation

↓

ParticipationRegistered

↓

Registered
```

Registered representa la primera revisión válida del Aggregate.

Una Participation no puede crearse directamente como:

```text
Active

Completed

Withdrawn

Invalidated

Archived
```

salvo una futura evolución explícita del dominio que modifique esta
regla.

---

# Lifecycle Principal

El camino principal del ciclo de vida es:

```text
Registered
     │
     ▼
  Active
     │
     ▼
 Completed
     │
     ▼
 Archived
```

Este camino representa una Participation que:

- fue registrada;
- comenzó formalmente;
- se desarrolló;
- finalizó correctamente;
- posteriormente fue archivada.

---

# Caminos Alternativos

El Aggregate contempla caminos alternativos controlados.

Desde Registered:

```text
Registered
     │
     ├──────────────► Withdrawn
     │
     └──────────────► Invalidated
```

Desde Active:

```text
Active
     │
     ├──────────────► Withdrawn
     │
     └──────────────► Invalidated
```

Desde Completed:

```text
Completed
     │
     └──────────────► Invalidated
```

Desde estados terminales:

```text
Completed
     │
     ▼
 Archived
```

```text
Withdrawn
     │
     ▼
 Archived
```

```text
Invalidated
     │
     ▼
 Archived
```

No todas las transiciones son válidas desde todos los estados.

---

# Diagrama General

```text
                     ┌──────────────┐
                     │  Registered  │
                     └──────┬───────┘
                            │
                            │ Activate
                            ▼
                     ┌──────────────┐
                     │    Active    │
                     └──────┬───────┘
                            │
                            │ Complete
                            ▼
                     ┌──────────────┐
                     │  Completed   │
                     └──────┬───────┘
                            │
                            │ Archive
                            ▼
                     ┌──────────────┐
                     │   Archived   │
                     └──────────────┘


Registered ───────────────► Withdrawn
     │                         │
     │                         │ Archive
     │                         ▼
     │                    ┌──────────┐
     │                    │ Archived │
     │                    └──────────┘
     │
     └────────────────────► Invalidated
                               │
                               │ Archive
                               ▼
                          ┌──────────┐
                          │ Archived │
                          └──────────┘


Active ───────────────────► Withdrawn

Active ───────────────────► Invalidated

Completed ────────────────► Invalidated
```

---

# Registered

## Definición

Registered representa una Participation que existe formalmente
dentro del dominio pero cuyo ejercicio participativo aún no ha
comenzado.

En este estado el Aggregate posee:

```text
ParticipationId

OrganizationId

Actor Reference

ParticipationType

Context References

CreatedAt

Version
```

y:

```text
Status = Registered
```

---

# Significado de Registered

Registered significa:

- la Participation fue creada correctamente;
- posee identidad;
- pertenece a una Organization;
- posee un actor identificable;
- posee contexto participativo suficiente;
- todavía no se considera activa;
- todavía no se considera completada;
- todavía no ha sido retirada;
- todavía no ha sido invalidada;
- todavía no ha sido archivada.

---

# Entrada a Registered

Registered solo se alcanza mediante la creación válida del
Aggregate.

Conceptualmente:

```text
No Participation

↓

RegisterParticipation

↓

ParticipationRegistered

↓

Registered
```

No existe una transición desde otro estado hacia Registered dentro
del Lifecycle actual.

---

# Salidas de Registered

Desde Registered pueden existir las siguientes evoluciones
conceptuales:

```text
Registered

↓

Active
```

```text
Registered

↓

Withdrawn
```

```text
Registered

↓

Invalidated
```

La transición específica debe estar permitida por la State
Machine.

---

# Restricciones de Registered

Mientras Participation se encuentra en Registered:

- no puede considerarse completada;
- no puede poseer CompletedAt válido;
- no puede poseer WithdrawnAt salvo que se produzca retiro;
- no puede poseer InvalidatedAt salvo que se produzca
  invalidación;
- no puede poseer estado Archived;
- no puede omitir las condiciones necesarias para activación.

---

# Active

## Definición

Active representa una Participation cuyo ejercicio participativo
ha comenzado formalmente y se encuentra en curso.

Conceptualmente:

```text
Registered

↓

ActivateParticipation

↓

ParticipationActivated

↓

Active
```

---

# Significado de Active

Active significa:

- la Participation existe;
- la Participation fue activada válidamente;
- el actor se encuentra participando dentro del contexto
  correspondiente;
- StartedAt debe ser coherente con la transición;
- el Aggregate continúa abierto a comportamiento permitido;
- todavía no se encuentra completado;
- todavía no se encuentra retirado;
- todavía no se encuentra invalidado;
- todavía no se encuentra archivado.

---

# Entrada a Active

Active se alcanza desde:

```text
Registered
```

mediante una transición válida.

Debe cumplirse:

```text
CurrentState = Registered
```

antes de una activación normal.

La State Machine define formalmente las condiciones exactas.

---

# Salidas de Active

Desde Active pueden existir:

```text
Active

↓

Completed
```

```text
Active

↓

Withdrawn
```

```text
Active

↓

Invalidated
```

Cada transición representa un significado diferente.

---

# Restricciones de Active

Mientras Participation se encuentra Active:

- no puede volver directamente a Registered;
- no puede considerarse Archived;
- no puede poseer CompletedAt antes de completar;
- no puede poseer WithdrawnAt sin transición a Withdrawn;
- no puede poseer InvalidatedAt sin transición a Invalidated;
- no puede modificar su identidad;
- no puede modificar OrganizationId;
- no puede sustituir arbitrariamente al actor.

---

# Completed

## Definición

Completed representa una Participation que finalizó correctamente
su propio ciclo participativo.

Conceptualmente:

```text
Active

↓

CompleteParticipation

↓

ParticipationCompleted

↓

Completed
```

---

# Significado de Completed

Completed significa:

- la Participation fue activada previamente;
- el ejercicio participativo fue finalizado válidamente;
- existe coherencia temporal con CompletedAt;
- el Aggregate ya no se encuentra Active;
- la Participation conserva identidad e historia;
- puede ser archivada posteriormente;
- puede ser invalidada posteriormente cuando el dominio lo
  permita.

Completed no representa el resultado de procesos externos.

---

# Completed no Implica Resultado Externo

Debe mantenerse:

```text
ParticipationCompleted

≠

ProposalAccepted
```

```text
ParticipationCompleted

≠

ProposalRejected
```

```text
ParticipationCompleted

≠

VotingCompleted
```

```text
ParticipationCompleted

≠

VoteAccepted
```

```text
ParticipationCompleted

≠

AssemblyCompleted
```

Completed significa únicamente que el Lifecycle propio de la
Participation alcanzó una finalización válida.

---

# Entrada a Completed

Completed se alcanza desde:

```text
Active
```

mediante:

```text
CompleteParticipation
```

cuando las reglas correspondientes se encuentran satisfechas.

---

# Salidas de Completed

Desde Completed pueden existir conceptualmente:

```text
Completed

↓

Archived
```

y:

```text
Completed

↓

Invalidated
```

No puede volver normalmente hacia:

```text
Active

Registered
```

---

# Restricciones de Completed

Una Participation Completed:

- no puede reiniciarse arbitrariamente;
- no puede volver a Registered;
- no puede volver a Active mediante modificación directa;
- no puede volver a ejecutar su participación como si no hubiese
  finalizado;
- conserva su ParticipationId;
- conserva su OrganizationId;
- conserva trazabilidad;
- conserva Version;
- puede evolucionar únicamente por transiciones expresamente
  permitidas.

---

# Withdrawn

## Definición

Withdrawn representa una Participation retirada de forma explícita
conforme a las reglas del dominio.

Conceptualmente puede alcanzarse desde:

```text
Registered
```

o:

```text
Active
```

cuando la State Machine permita el retiro.

---

# Significado de Withdrawn

Withdrawn significa:

- la Participation existió formalmente;
- dejó de continuar su ciclo normal por una decisión de retiro
  válida;
- debe conservar WithdrawnAt;
- mantiene identidad;
- mantiene contexto;
- mantiene historia;
- mantiene trazabilidad;
- no desaparece del dominio.

---

# Withdrawn no es Eliminación

Debe mantenerse:

```text
Withdrawn

≠

Deleted
```

El retiro no elimina:

```text
ParticipationId

OrganizationId

Actor Reference

Context References

History

Version
```

La Participation continúa existiendo como hecho histórico del
dominio.

---

# Entrada a Withdrawn

Withdrawn puede alcanzarse desde:

```text
Registered
```

o:

```text
Active
```

mediante:

```text
WithdrawParticipation
```

cuando el estado y las reglas lo permitan.

---

# Salida de Withdrawn

El camino posterior permitido conceptualmente es:

```text
Withdrawn

↓

Archived
```

Withdrawn no retorna al ciclo normal.

---

# Restricciones de Withdrawn

Una Participation Withdrawn:

- no puede activarse;
- no puede completarse;
- no puede volver a Registered;
- no puede volver a Active;
- no puede continuar como si nunca hubiese sido retirada;
- conserva su historia;
- puede archivarse cuando corresponda.

---

# Invalidated

## Definición

Invalidated representa una Participation que dejó de ser válida
como instancia participativa conforme a una regla explícita del
dominio.

La invalidación constituye un hecho formal.

No equivale a eliminación.

---

# Significado de Invalidated

Invalidated significa:

- la Participation existió;
- una regla del dominio determinó que su validez debía cesar;
- la invalidación fue realizada mediante comportamiento válido;
- existe coherencia con InvalidatedAt;
- la identidad permanece;
- la historia permanece;
- la trazabilidad permanece;
- el ciclo normal deja de continuar.

---

# Invalidated no es Withdrawn

Debe mantenerse:

```text
Invalidated

≠

Withdrawn
```

Withdrawn representa retiro.

Invalidated representa pérdida formal de validez.

Ambos estados poseen semánticas diferentes.

---

# Invalidated no es Deleted

Debe mantenerse:

```text
Invalidated

≠

Deleted
```

La Participation invalidada continúa existiendo para:

- historia;
- auditoría;
- trazabilidad;
- reconstrucción;
- análisis;
- referencias del dominio.

---

# Entrada a Invalidated

Invalidated puede alcanzarse conceptualmente desde:

```text
Registered
```

```text
Active
```

```text
Completed
```

cuando la State Machine y las invariantes lo permitan.

---

# Salida de Invalidated

La evolución posterior permitida es:

```text
Invalidated

↓

Archived
```

No retorna al flujo normal.

---

# Restricciones de Invalidated

Una Participation Invalidated:

- no puede activarse;
- no puede completarse;
- no puede retirarse como si continuara válida;
- no puede volver a Registered;
- no puede volver a Active;
- no puede revertirse mediante asignación directa de Status;
- conserva su identidad e historia;
- puede archivarse.

---

# Archived

## Definición

Archived representa el estado final de conservación lógica del
Aggregate.

Participation continúa existiendo conceptualmente, pero deja de
participar en el flujo operativo normal.

---

# Significado de Archived

Archived significa:

- el ciclo operativo terminó;
- el Aggregate se conserva;
- la identidad permanece;
- la historia permanece;
- la trazabilidad permanece;
- Version permanece;
- no pueden ejecutarse modificaciones ordinarias;
- el Aggregate continúa disponible para lectura autorizada,
  reconstrucción, auditoría o referencias históricas cuando
  corresponda.

---

# Entrada a Archived

Archived puede alcanzarse desde:

```text
Completed
```

```text
Withdrawn
```

```text
Invalidated
```

mediante:

```text
ArchiveParticipation
```

cuando las reglas correspondientes se encuentran satisfechas.

---

# Estado Terminal

Archived constituye el estado terminal del Lifecycle actual.

Conceptualmente:

```text
Archived

↓

No Normal Transition
```

No existen transiciones ordinarias desde Archived hacia otros
estados.

---

# Restricciones de Archived

Una Participation Archived:

- no puede volver a Registered;
- no puede volver a Active;
- no puede volver a Completed;
- no puede volver a Withdrawn;
- no puede volver a Invalidated;
- no puede modificar identidad;
- no puede modificar OrganizationId;
- no puede modificar el actor;
- no puede modificar su contexto mediante operaciones ordinarias;
- no puede ejecutar Commands operacionales normales.

---

# Estados Operacionales

Conceptualmente pueden considerarse estados operacionales:

```text
Registered

Active
```

Estos estados permiten que Participation continúe evolucionando
dentro de su ciclo normal.

---

# Estados de Finalización

Conceptualmente:

```text
Completed

Withdrawn

Invalidated
```

representan formas diferentes de finalizar la evolución
operacional normal.

Cada uno conserva una semántica distinta.

---

# Estado de Conservación

```text
Archived
```

representa conservación lógica posterior a una condición de
finalización.

---

# Clasificación Conceptual de Estados

```text
Registered
    =
Created / Not Yet Active
```

```text
Active
    =
Participation In Progress
```

```text
Completed
    =
Successfully Finished Participation
```

```text
Withdrawn
    =
Explicitly Withdrawn Participation
```

```text
Invalidated
    =
Participation No Longer Considered Valid
```

```text
Archived
    =
Logically Preserved Terminal State
```

---

# Transiciones Principales

Las transiciones principales son:

```text
Registered → Active
```

```text
Active → Completed
```

```text
Completed → Archived
```

---

# Transiciones Alternativas

Las transiciones alternativas reconocidas son:

```text
Registered → Withdrawn
```

```text
Registered → Invalidated
```

```text
Active → Withdrawn
```

```text
Active → Invalidated
```

```text
Completed → Invalidated
```

```text
Withdrawn → Archived
```

```text
Invalidated → Archived
```

---

# Transiciones No Implícitas

La existencia de dos estados no significa que exista una
transición entre ellos.

Por ejemplo:

```text
Registered

↓

Completed
```

no debe asumirse válida.

Tampoco:

```text
Completed

↓

Active
```

ni:

```text
Withdrawn

↓

Active
```

ni:

```text
Invalidated

↓

Registered
```

ni:

```text
Archived

↓

Active
```

La State Machine constituye la autoridad formal sobre estas
relaciones.

---

# Relación con Commands

Cada transición debe originarse en un Command válido.

Conceptualmente:

```text
RegisterParticipation
```

produce la creación del Aggregate en:

```text
Registered
```

```text
ActivateParticipation
```

solicita:

```text
Registered → Active
```

```text
CompleteParticipation
```

solicita:

```text
Active → Completed
```

```text
WithdrawParticipation
```

solicita una transición hacia:

```text
Withdrawn
```

desde estados permitidos.

```text
InvalidateParticipation
```

solicita una transición hacia:

```text
Invalidated
```

desde estados permitidos.

```text
ArchiveParticipation
```

solicita una transición hacia:

```text
Archived
```

desde estados permitidos.

---

# Relación con Domain Events

Cada transición válida produce el hecho correspondiente.

Conceptualmente:

```text
RegisterParticipation

↓

ParticipationRegistered
```

```text
ActivateParticipation

↓

ParticipationActivated
```

```text
CompleteParticipation

↓

ParticipationCompleted
```

```text
WithdrawParticipation

↓

ParticipationWithdrawn
```

```text
InvalidateParticipation

↓

ParticipationInvalidated
```

```text
ArchiveParticipation

↓

ParticipationArchived
```

La definición formal de los eventos se encuentra en:

```text
DOMAIN-008D-Domain-Events.md
```

---

# Regla Command / Event

Debe mantenerse:

```text
Command

≠

Domain Event
```

Un Command expresa intención.

Un Domain Event representa una transición efectivamente ocurrida.

Un Command puede ser rechazado.

Un Domain Event de éxito no debe producirse cuando la transición
fue rechazada.

---

# Información Temporal del Lifecycle

Participation mantiene información temporal asociada a hechos del
Lifecycle.

Conceptualmente:

```text
CreatedAt

StartedAt

CompletedAt

WithdrawnAt

InvalidatedAt

UpdatedAt
```

Cada timestamp debe representar un hecho real.

---

# CreatedAt

CreatedAt se establece durante la creación válida.

Conceptualmente:

```text
ParticipationRegistered

↓

CreatedAt
```

CreatedAt no cambia durante el Lifecycle.

---

# StartedAt

StartedAt se establece cuando Participation entra válidamente en:

```text
Active
```

Debe mantenerse:

```text
Status = Active
```

coherente con la existencia de StartedAt después de la activación.

---

# CompletedAt

CompletedAt se establece cuando ocurre:

```text
ParticipationCompleted
```

Debe mantenerse:

```text
Status = Completed
```

coherente con el hecho de finalización.

---

# WithdrawnAt

WithdrawnAt se establece cuando ocurre:

```text
ParticipationWithdrawn
```

Debe mantenerse coherente con:

```text
Status = Withdrawn
```

---

# InvalidatedAt

InvalidatedAt se establece cuando ocurre:

```text
ParticipationInvalidated
```

Debe mantenerse coherente con:

```text
Status = Invalidated
```

---

# UpdatedAt

UpdatedAt representa la última modificación válida del Aggregate.

Debe actualizarse cuando una transición válida modifica
Participation.

Una operación rechazada no debe representar una nueva
modificación válida.

---

# Coherencia Temporal

Los timestamps deben mantener coherencia causal.

Para el camino principal:

```text
CreatedAt
    │
    ▼
StartedAt
    │
    ▼
CompletedAt
```

Debe cumplirse conceptualmente:

```text
CreatedAt

≤

StartedAt

≤

CompletedAt
```

cuando todos estos valores existan.

---

# Coherencia Temporal en Withdrawal

Cuando Withdrawal ocurre desde Registered:

```text
CreatedAt

≤

WithdrawnAt
```

Cuando Withdrawal ocurre desde Active:

```text
CreatedAt

≤

StartedAt

≤

WithdrawnAt
```

---

# Coherencia Temporal en Invalidation

Si Invalidated ocurre desde Registered:

```text
CreatedAt

≤

InvalidatedAt
```

Si ocurre desde Active:

```text
CreatedAt

≤

StartedAt

≤

InvalidatedAt
```

Si ocurre desde Completed:

```text
CreatedAt

≤

StartedAt

≤

CompletedAt

≤

InvalidatedAt
```

La especificación formal corresponde a:

```text
DOMAIN-008E-Invariants.md
```

---

# Lifecycle y Version

Toda transición válida representa una nueva revisión lógica del
Aggregate.

Conceptualmente:

```text
State N

Version N
```

seguido de:

```text
Valid Transition
```

produce:

```text
State N+1

Version N+1
```

La notación representa evolución conceptual.

La regla formal de Version se desarrolla en:

```text
DOMAIN-008I-Versioning.md
```

---

# Transición Rechazada

Cuando una transición es inválida:

```text
Current State

↓

Invalid Command

↓

Rejected
```

debe mantenerse:

```text
State unchanged
```

y:

```text
Version unchanged
```

No debe establecerse ningún timestamp que represente un hecho que
no ocurrió.

No debe producirse un Domain Event de éxito.

---

# Lifecycle e Invariantes

Toda transición debe preservar las invariantes definidas en:

```text
DOMAIN-008E-Invariants.md
```

Una transición formalmente conocida por la State Machine puede
ser rechazada si las invariantes requeridas no se encuentran
satisfechas.

Debe mantenerse:

```text
Known Transition

≠

Automatically Valid Transition
```

---

# Lifecycle y Permissions

La existencia de una transición válida dentro del Lifecycle no
significa que cualquier actor pueda ejecutarla.

Debe mantenerse:

```text
Valid Transition

≠

Authorized Actor
```

La autorización se define en:

```text
DOMAIN-008F-Permissions.md
```

---

# Permission no Reemplaza Lifecycle

Un actor autorizado tampoco puede ignorar el Lifecycle.

Debe mantenerse:

```text
Authorized Actor

+

Invalid Transition

=

Rejected Operation
```

La autorización determina quién puede intentar una operación.

El Lifecycle y la State Machine determinan si la evolución es
válida.

---

# Lifecycle y Consistency Boundary

Todas las transiciones modifican únicamente:

```text
Participation
```

No deben modificar dentro de la misma consistencia interna:

```text
Organization

Citizen

Membership

Role

Territory

Assembly

Proposal

Voting

Document

Notification

Audit
```

El límite formal se documenta en:

```text
DOMAIN-008J-Consistency-Boundary.md
```

---

# Lifecycle y Organization

Participation pertenece durante todo su Lifecycle a la misma:

```text
OrganizationId
```

Debe mantenerse:

```text
OrganizationId at Registered

=

OrganizationId at Active

=

OrganizationId at Completed

=

OrganizationId at Withdrawn

=

OrganizationId at Invalidated

=

OrganizationId at Archived
```

La evolución del estado no modifica la propiedad organizacional.

---

# Lifecycle y Actor

La identidad contextual del participante debe mantenerse durante
el Lifecycle.

La transición de estado no convierte una Participation en la
participación de otro actor.

Debe mantenerse la referencia correspondiente según el modelo
establecido:

```text
CitizenId
```

o:

```text
MembershipId
```

cuando corresponda.

---

# Lifecycle y Membership

El estado de Membership no constituye el estado de Participation.

Debe mantenerse:

```text
Membership.Active

≠

Participation.Active
```

Una Membership puede continuar Active después de que una
Participation se encuentre:

```text
Completed

Withdrawn

Invalidated

Archived
```

Ambos Aggregates poseen Lifecycles independientes.

---

# Lifecycle y Assembly

La evolución de Assembly no modifica automáticamente el estado de
Participation.

Debe mantenerse:

```text
Assembly State Change

≠

Automatic Participation State Change
```

Cualquier consecuencia sobre Participation debe producirse
mediante un Command válido dirigido al propio Aggregate.

---

# Lifecycle y Proposal

La evolución de Proposal tampoco modifica directamente
Participation.

Debe mantenerse:

```text
Proposal Accepted

≠

Participation Completed
```

```text
Proposal Rejected

≠

Participation Invalidated
```

Toda transición de Participation requiere comportamiento propio.

---

# Lifecycle y Voting

Participation y Voting mantienen ciclos independientes.

Debe mantenerse:

```text
Voting Started

≠

Participation Active
```

```text
Voting Completed

≠

Participation Completed
```

La relación contextual no fusiona Lifecycles.

---

# Lifecycle y Territory

Territory puede proporcionar contexto a Participation.

Los cambios en Territory no modifican automáticamente el estado de
Participation.

Participation conserva su propio Lifecycle.

---

# Lifecycle y Document

La creación, modificación o archivado de un Document relacionado
no constituye una transición de Participation.

Debe mantenerse:

```text
Document Lifecycle

≠

Participation Lifecycle
```

---

# Lifecycle y Notification

Notification puede reaccionar a hechos producidos durante el
Lifecycle.

Ejemplo:

```text
ParticipationActivated

↓

Notification Process
```

El éxito o fallo de Notification no redefine automáticamente el
estado de Participation.

---

# Lifecycle y Audit

Audit puede registrar hechos producidos por las transiciones.

Conceptualmente:

```text
ParticipationRegistered

ParticipationActivated

ParticipationCompleted

ParticipationWithdrawn

ParticipationInvalidated

ParticipationArchived
```

pueden contribuir a trazabilidad.

Audit no controla el Lifecycle.

---

# Lifecycle e Integration

Los estados confirmados pueden originar Integration Events.

Conceptualmente:

```text
ParticipationCompleted

↓

Integration Mapping

↓

ParticipationCompletedForIntegration
```

cuando corresponda.

La publicación externa no forma parte de la transición interna.

---

# Regla de Independencia Externa

Una transición válida de Participation no debe depender de que
sistemas externos completen operaciones secundarias que no formen
parte de una invariante inmediata.

Ejemplo:

```text
CompleteParticipation

↓

ParticipationCompleted

↓

Commit
```

puede originar posteriormente:

```text
Notification

Audit

Integration

Projection
```

sin ampliar el Lifecycle del Aggregate.

---

# Registered a Active

La transición:

```text
Registered

↓

Active
```

representa el inicio formal de Participation.

Debe ocurrir únicamente mediante:

```text
ActivateParticipation
```

y producir:

```text
ParticipationActivated
```

cuando sea válida.

---

# Precondiciones Conceptuales de Activación

La activación requiere como mínimo:

- Participation existente;
- estado Registered;
- OrganizationId válido;
- actor identificado;
- ParticipationType válido;
- contexto participativo válido;
- invariantes satisfechas;
- actor autorizado;
- Version compatible.

Las reglas exactas se desarrollan en los documentos
correspondientes.

---

# Efectos Conceptuales de Activación

Una activación válida produce:

```text
Status = Active
```

```text
StartedAt = Timestamp
```

```text
Version = Version + 1
```

y:

```text
ParticipationActivated
```

---

# Active a Completed

La transición:

```text
Active

↓

Completed
```

representa la finalización válida.

Debe ocurrir mediante:

```text
CompleteParticipation
```

y producir:

```text
ParticipationCompleted
```

---

# Precondiciones Conceptuales de Completion

Como mínimo:

- Participation existe;
- estado actual es Active;
- las condiciones de finalización se cumplen;
- invariantes permanecen válidas;
- actor autorizado;
- Version compatible.

---

# Efectos Conceptuales de Completion

Una finalización válida produce:

```text
Status = Completed
```

```text
CompletedAt = Timestamp
```

```text
Version = Version + 1
```

```text
ParticipationCompleted
```

---

# Registered a Withdrawn

La transición:

```text
Registered

↓

Withdrawn
```

representa el retiro antes del inicio efectivo de la
Participation.

Debe ocurrir mediante:

```text
WithdrawParticipation
```

cuando las reglas lo permitan.

---

# Efectos del Withdrawal desde Registered

Debe producir conceptualmente:

```text
Status = Withdrawn
```

```text
WithdrawnAt = Timestamp
```

```text
Version = Version + 1
```

```text
ParticipationWithdrawn
```

StartedAt debe permanecer sin representar una activación que nunca
ocurrió.

---

# Active a Withdrawn

La transición:

```text
Active

↓

Withdrawn
```

representa el retiro después de haber comenzado la Participation.

Debe existir coherencia entre:

```text
StartedAt

WithdrawnAt
```

y el historial del Aggregate.

---

# Efectos del Withdrawal desde Active

Conceptualmente:

```text
Status = Withdrawn
```

```text
WithdrawnAt = Timestamp
```

```text
Version = Version + 1
```

```text
ParticipationWithdrawn
```

La transición conserva evidencia de que la Participation estuvo
previamente Active.

---

# Registered a Invalidated

La transición:

```text
Registered

↓

Invalidated
```

representa que una Participation registrada fue invalidada antes
de comenzar.

Debe utilizar:

```text
InvalidateParticipation
```

y producir:

```text
ParticipationInvalidated
```

cuando sea válida.

---

# Active a Invalidated

La transición:

```text
Active

↓

Invalidated
```

representa que una Participation que se encontraba en curso fue
invalidada.

La invalidación no debe borrar:

```text
StartedAt
```

ni la historia previa.

---

# Completed a Invalidated

La transición:

```text
Completed

↓

Invalidated
```

representa que una Participation previamente finalizada dejó de
ser considerada válida según una regla explícita del dominio.

Esta transición preserva el hecho histórico de que la
Participation fue completada antes de ser invalidada.

No debe eliminarse:

```text
CompletedAt
```

por el solo hecho de invalidar posteriormente.

---

# Efectos Conceptuales de Invalidation

Una invalidación válida produce:

```text
Status = Invalidated
```

```text
InvalidatedAt = Timestamp
```

```text
Version = Version + 1
```

```text
ParticipationInvalidated
```

---

# Completed a Archived

La transición:

```text
Completed

↓

Archived
```

representa conservación lógica posterior a finalización válida.

Debe utilizar:

```text
ArchiveParticipation
```

---

# Withdrawn a Archived

La transición:

```text
Withdrawn

↓

Archived
```

conserva una Participation retirada como parte de la historia del
dominio.

---

# Invalidated a Archived

La transición:

```text
Invalidated

↓

Archived
```

conserva una Participation invalidada.

Invalidation no elimina la Participation.

---

# Efectos Conceptuales de Archive

Una transición válida a Archived produce:

```text
Status = Archived
```

```text
Version = Version + 1
```

```text
ParticipationArchived
```

La información histórica anterior permanece.

---

# No Reactivación Implícita

El Lifecycle actual no contempla reactivación desde:

```text
Completed

Withdrawn

Invalidated

Archived
```

hacia:

```text
Active
```

No debe crearse implícitamente comportamiento como:

```text
ReactivateParticipation
```

sin una evolución explícita del modelo de dominio.

---

# No Reinicio

Una Participation completada no se reinicia.

Debe mantenerse:

```text
Completed

≠

Reusable Active Instance
```

Si el dominio requiere una nueva instancia participativa, debe
representarse mediante una nueva Participation cuando corresponda.

---

# No Reutilización del Aggregate

Participation representa una instancia específica.

No debe reutilizarse el mismo ParticipationId para representar una
participación posterior independiente.

Debe mantenerse:

```text
New Participation Instance

↓

New ParticipationId
```

cuando corresponda a un nuevo hecho participativo.

---

# Prohibición de Salto de Estados

No está permitido asumir transiciones no definidas para
simplificar operaciones.

Ejemplo:

```text
Registered

↓

Completed
```

no forma parte del camino principal.

Debe respetarse la State Machine oficial.

---

# Prohibición de Retroceso

No deben existir retrocesos arbitrarios como:

```text
Completed → Active
```

```text
Withdrawn → Registered
```

```text
Invalidated → Active
```

```text
Archived → Completed
```

El Lifecycle preserva la historia y causalidad del Aggregate.

---

# Prohibición de Modificación Directa

No está permitido:

```text
participation.status = Completed
```

como comportamiento de dominio.

Debe utilizarse:

```text
CompleteParticipation
```

y las validaciones correspondientes.

---

# Prohibición de Bypass Administrativo

Un actor administrativo no puede ignorar el Lifecycle.

Debe mantenerse:

```text
Administrator

≠

Lifecycle Bypass
```

Los permisos adicionales no convierten transiciones inválidas en
válidas.

---

# Prohibición de Bypass de Infrastructure

La infraestructura tampoco puede modificar Status directamente
para acelerar una operación.

No debe ocurrir:

```text
UPDATE participation
SET status = 'Completed'
```

como sustituto del comportamiento de dominio.

El modelo de persistencia implementa el Lifecycle.

No lo reemplaza.

---

# Prohibición de Estados Técnicos

No deben incorporarse al Lifecycle estados técnicos como:

```text
Processing

Retrying

DatabaseError

SyncPending

HttpFailed

MessageQueued
```

salvo que en una evolución futura alguno de estos conceptos se
convierta explícitamente en un concepto real del dominio.

Los estados técnicos pertenecen a Application o Infrastructure.

---

# Prohibición de Inferencia desde UI

Una etiqueta visual no constituye un nuevo estado del Lifecycle.

Ejemplo:

```text
Pending Badge
```

no implica automáticamente:

```text
Status = Pending
```

El Lifecycle debe evolucionar únicamente por necesidades reales
del dominio.

---

# Prohibición de Inferencia desde Integraciones

Un sistema externo no puede introducir estados propios dentro de
Participation por conveniencia de sincronización.

Debe mantenerse:

```text
External System State

≠

Participation Status
```

La traducción corresponde a Integration.

---

# Lifecycle y Persistencia

El Repository debe preservar exactamente el estado confirmado del
Aggregate.

Cuando una Participation es recuperada:

```text
Persisted Status

↓

Rehydrated Participation Status
```

deben representar la misma revisión lógica.

La recuperación no constituye una transición.

---

# Rehidratación

Rehidratar una Participation:

```text
Registered
```

no la convierte en:

```text
Active
```

Rehidratar una Participation:

```text
Completed
```

no incrementa Version.

Debe mantenerse:

```text
Rehydration

≠

Lifecycle Transition
```

---

# Event Sourcing

Cuando se utilice Event Sourcing, el Lifecycle puede reconstruirse
mediante sus eventos.

Ejemplo:

```text
ParticipationRegistered

↓

ParticipationActivated

↓

ParticipationCompleted

↓

ParticipationArchived
```

produce conceptualmente una Participation:

```text
Status = Archived
```

con historia de finalización válida.

---

# Replay

El replay de Domain Events no constituye nuevas transiciones
operacionales.

Debe mantenerse:

```text
Historical Event Replay

≠

New Lifecycle Change
```

Durante reconstrucción no deben producirse nuevamente efectos
externos como si los hechos acabaran de ocurrir.

---

# Reconstrucción del Estado

Ejemplo:

```text
ParticipationRegistered
```

produce durante reconstrucción:

```text
Registered
```

seguido por:

```text
ParticipationActivated
```

produce:

```text
Active
```

seguido por:

```text
ParticipationWithdrawn
```

produce:

```text
Withdrawn
```

El resultado debe corresponder a la historia oficial.

---

# Historial Incompatible

Una secuencia como:

```text
ParticipationRegistered

↓

ParticipationCompleted
```

sin la transición requerida por el Lifecycle debe considerarse
incompatible con el modelo actual cuando la State Machine exija
activación previa.

La implementación no debe normalizar silenciosamente una historia
inválida.

---

# Lifecycle y Read Models

Los Read Models pueden proyectar el estado del Lifecycle.

Conceptualmente:

```text
ParticipationRegistered

↓

Projection

↓

Status = Registered
```

```text
ParticipationActivated

↓

Projection

↓

Status = Active
```

```text
ParticipationCompleted

↓

Projection

↓

Status = Completed
```

Las proyecciones no controlan el Lifecycle.

---

# Read Model Desactualizado

Debido a consistencia eventual, una proyección puede mostrar
temporalmente un estado anterior.

Ejemplo:

```text
Aggregate Status = Completed
```

mientras:

```text
Read Model Status = Active
```

durante un intervalo de proyección.

La autoridad del Lifecycle permanece en el Write Model.

---

# Lifecycle e Integration Events

Los estados relevantes pueden comunicarse mediante contratos de
integración.

Conceptualmente:

```text
ParticipationActivated

↓

ParticipationActivatedForIntegration
```

o:

```text
ParticipationCompleted

↓

ParticipationCompletedForIntegration
```

cuando corresponda.

Integration Events no modifican el Lifecycle.

---

# Fallo de Integration

Si Participation alcanza:

```text
Completed
```

y posteriormente falla una integración externa:

```text
Integration Failure
```

el Lifecycle no debe retroceder automáticamente.

Debe mantenerse:

```text
External Failure

≠

Automatic Participation Rollback
```

---

# Fallo de Notification

De forma equivalente:

```text
ParticipationCompleted

↓

Notification Failure
```

no implica:

```text
ParticipationStatus = Active
```

Notification posee responsabilidad independiente.

---

# Lifecycle y Concurrencia

Toda transición debe validar Version conforme a:

```text
DOMAIN-008I-Versioning.md
```

Ejemplo:

```text
Process A

Active Version 4

↓

CompleteParticipation
```

y:

```text
Process B

Active Version 4

↓

WithdrawParticipation
```

no pueden confirmarse silenciosamente ambas sobre la misma
revisión.

---

# Concurrencia y Estado

Cuando una transición ya fue confirmada, otra operación basada en
la revisión anterior debe reevaluarse.

Ejemplo:

```text
Active Version 4

↓

Process A completes

↓

Completed Version 5
```

Un intento posterior basado en:

```text
ExpectedVersion = 4
```

debe detectar conflicto.

La operación debe volver a evaluar el estado actual antes de
continuar.

---

# Consistencia de Estado y Version

Una transición confirmada debe mantener coherencia entre:

```text
Status

Lifecycle Timestamp

Version
```

Ejemplo:

```text
Status = Completed

CompletedAt = T

Version = 8
```

deben pertenecer a la misma revisión lógica.

---

# Atomicidad del Lifecycle

Una transición válida debe ser atómica dentro del límite de
Participation.

No debe confirmarse:

```text
Status = Completed
```

sin:

```text
CompletedAt
```

cuando dicho timestamp sea obligatorio para el hecho.

Tampoco debe confirmarse el timestamp sin el cambio de estado
correspondiente.

---

# Rechazo Atómico

Si una transición falla:

```text
Previous State

=

Preserved
```

No debe existir:

```text
Partial Transition
```

Ejemplo inválido:

```text
CompletedAt set

but

Status remains Active
```

como resultado confirmado de un `CompleteParticipation` fallido.

---

# Lifecycle y Seguridad

El Security Model debe proteger el Lifecycle frente a:

- cambios directos;
- actores no autorizados;
- bypass de Commands;
- bypass del Aggregate Root;
- conflictos de Version;
- modificación cruzada de Organizations;
- manipulación de referencias.

La especificación completa se desarrolla en:

```text
DOMAIN-008O-Security-Model.md
```

---

# Lifecycle y Performance

Las optimizaciones no pueden eliminar etapas ni validaciones del
Lifecycle.

Debe mantenerse:

```text
Performance Optimization

≠

Lifecycle Simplification
```

No debe aceptarse:

```text
Registered → Completed
```

únicamente para reducir procesamiento si la State Machine no
define esa transición.

---

# Lifecycle y Tests

Los Test Scenarios deben verificar:

- creación en Registered;
- activación válida;
- activación inválida;
- finalización válida;
- finalización inválida;
- retiro desde estados permitidos;
- retiro desde estados prohibidos;
- invalidación válida;
- invalidación inválida;
- archivado válido;
- archivado inválido;
- prohibición de retrocesos;
- timestamps;
- Version;
- Domain Events;
- estados terminales;
- independencia respecto de otros Aggregates.

La especificación se desarrolla en:

```text
DOMAIN-008M-Test-Scenarios.md
```

---

# Casos de Uso del Lifecycle

El Lifecycle permite representar conceptualmente:

```text
Registrar una nueva Participation.

Activar una Participation registrada.

Completar una Participation activa.

Retirar una Participation registrada.

Retirar una Participation activa.

Invalidar una Participation registrada.

Invalidar una Participation activa.

Invalidar una Participation completada.

Archivar una Participation completada.

Archivar una Participation retirada.

Archivar una Participation invalidada.
```

---

# Caso — Participación Completada

Flujo:

```text
RegisterParticipation

↓

Registered

↓

ActivateParticipation

↓

Active

↓

CompleteParticipation

↓

Completed

↓

ArchiveParticipation

↓

Archived
```

Eventos:

```text
ParticipationRegistered

ParticipationActivated

ParticipationCompleted

ParticipationArchived
```

---

# Caso — Participación Retirada antes de Activación

Flujo:

```text
RegisterParticipation

↓

Registered

↓

WithdrawParticipation

↓

Withdrawn

↓

ArchiveParticipation

↓

Archived
```

Eventos:

```text
ParticipationRegistered

ParticipationWithdrawn

ParticipationArchived
```

No debe existir:

```text
ParticipationActivated
```

ni:

```text
ParticipationCompleted
```

en este recorrido.

---

# Caso — Participación Retirada estando Activa

Flujo:

```text
RegisterParticipation

↓

Registered

↓

ActivateParticipation

↓

Active

↓

WithdrawParticipation

↓

Withdrawn

↓

ArchiveParticipation

↓

Archived
```

Eventos:

```text
ParticipationRegistered

ParticipationActivated

ParticipationWithdrawn

ParticipationArchived
```

---

# Caso — Participation Invalidated antes de Activación

Flujo:

```text
Registered

↓

InvalidateParticipation

↓

Invalidated

↓

ArchiveParticipation

↓

Archived
```

La historia conserva el hecho de que nunca llegó a Active.

---

# Caso — Participation Invalidated durante Active

Flujo:

```text
Registered

↓

Active

↓

Invalidated

↓

Archived
```

Debe conservarse:

```text
StartedAt
```

porque la Participation sí estuvo activa antes de invalidarse.

---

# Caso — Participation Invalidated después de Completed

Flujo:

```text
Registered

↓

Active

↓

Completed

↓

Invalidated

↓

Archived
```

La invalidación posterior no elimina:

```text
CompletedAt
```

ni:

```text
ParticipationCompleted
```

de la historia.

El nuevo hecho:

```text
ParticipationInvalidated
```

expresa la evolución posterior.

---

# Caso — Intento de Completar Registered

Given:

```text
Status = Registered
```

When:

```text
CompleteParticipation
```

Then:

La operación debe rechazarse si la State Machine exige Active como
estado origen.

Debe mantenerse:

```text
Status = Registered

Version unchanged

CompletedAt = null

No ParticipationCompleted
```

---

# Caso — Intento de Activar Completed

Given:

```text
Status = Completed
```

When:

```text
ActivateParticipation
```

Then:

La operación debe rechazarse.

Completed no retorna al flujo Active.

---

# Caso — Intento de Activar Withdrawn

Given:

```text
Status = Withdrawn
```

When:

```text
ActivateParticipation
```

Then:

Debe rechazarse.

Debe mantenerse:

```text
Status = Withdrawn
```

---

# Caso — Intento de Activar Invalidated

Given:

```text
Status = Invalidated
```

When:

```text
ActivateParticipation
```

Then:

La operación debe rechazarse.

---

# Caso — Intento de Modificar Archived

Given:

```text
Status = Archived
```

When:

Se intenta una operación normal de Lifecycle.

Then:

Debe rechazarse.

Debe mantenerse:

```text
Status = Archived

Version unchanged
```

---

# Matriz Conceptual de Estados

```text
State          Meaning

Registered     Participation exists but has not started

Active         Participation is currently in progress

Completed      Participation finished validly

Withdrawn      Participation was explicitly withdrawn

Invalidated    Participation is no longer considered valid

Archived       Participation is logically preserved and closed
```

---

# Matriz Conceptual de Transiciones

```text
Origin         Command                      Destination

None           RegisterParticipation        Registered

Registered     ActivateParticipation        Active

Active         CompleteParticipation        Completed

Registered     WithdrawParticipation        Withdrawn

Active         WithdrawParticipation        Withdrawn

Registered     InvalidateParticipation      Invalidated

Active         InvalidateParticipation      Invalidated

Completed      InvalidateParticipation      Invalidated

Completed      ArchiveParticipation         Archived

Withdrawn      ArchiveParticipation         Archived

Invalidated    ArchiveParticipation         Archived
```

La definición formal y las condiciones exactas corresponden a:

```text
DOMAIN-008B-State-Machine.md
```

---

# Matriz de Domain Events

```text
Transition                Domain Event

None → Registered         ParticipationRegistered

Registered → Active       ParticipationActivated

Active → Completed        ParticipationCompleted

Registered → Withdrawn    ParticipationWithdrawn

Active → Withdrawn        ParticipationWithdrawn

Registered → Invalidated  ParticipationInvalidated

Active → Invalidated      ParticipationInvalidated

Completed → Invalidated   ParticipationInvalidated

Completed → Archived      ParticipationArchived

Withdrawn → Archived      ParticipationArchived

Invalidated → Archived    ParticipationArchived
```

---

# Matriz Temporal

```text
State          Required Temporal Meaning

Registered     CreatedAt

Active         CreatedAt + StartedAt

Completed      CreatedAt + StartedAt + CompletedAt

Withdrawn      CreatedAt + WithdrawnAt
               StartedAt when withdrawal occurred from Active

Invalidated    CreatedAt + InvalidatedAt
               Previous timestamps preserved when they existed

Archived       Previous lifecycle timestamps preserved
```

---

# Matriz de Operaciones Generales

```text
State          Normal Evolution

Registered     Activate
               Withdraw
               Invalidate

Active         Complete
               Withdraw
               Invalidate

Completed      Invalidate
               Archive

Withdrawn      Archive

Invalidated    Archive

Archived       No normal lifecycle transition
```

---

# Invariantes del Lifecycle

El Lifecycle mantiene como mínimo:

- toda Participation válida comienza en Registered;
- Registered es el único estado inicial;
- Active requiere una activación válida;
- Completed requiere una finalización válida;
- Withdrawn requiere un retiro válido;
- Invalidated requiere una invalidación válida;
- Archived requiere archivado válido;
- Archived no admite transiciones normales posteriores;
- Completed no retorna arbitrariamente a Active;
- Withdrawn no retorna al flujo normal;
- Invalidated no retorna al flujo normal;
- Status no se modifica directamente;
- timestamps representan hechos realmente ocurridos;
- timestamps mantienen coherencia temporal;
- toda transición válida incrementa Version;
- toda transición rechazada mantiene Version;
- toda transición válida produce el hecho correspondiente cuando
  el contrato así lo establece;
- una transición de Participation no modifica directamente otros
  Aggregates;
- el estado de otros Aggregates no sustituye el estado de
  Participation.

Las invariantes completas se desarrollan en:

```text
DOMAIN-008E-Invariants.md
```

---

# Restricciones

No está permitido:

- crear Participation directamente en Active;
- crear Participation directamente en Completed;
- crear Participation directamente en Withdrawn;
- crear Participation directamente en Invalidated;
- crear Participation directamente en Archived;
- modificar Status directamente;
- saltar estados mediante operaciones no definidas;
- volver de Completed a Active;
- volver de Withdrawn a Active;
- volver de Withdrawn a Registered;
- volver de Invalidated a Active;
- volver de Invalidated a Registered;
- salir de Archived mediante operaciones normales;
- eliminar timestamps históricos válidos para simular otro
  recorrido;
- incrementar Version ante una transición rechazada;
- generar eventos de éxito ante una transición rechazada;
- modificar OrganizationId durante una transición;
- sustituir al actor durante una transición ordinaria;
- modificar otros Aggregates como efecto interno del Lifecycle;
- utilizar estados técnicos como estados del dominio;
- utilizar estados externos como sustitutos de Status;
- utilizar Infrastructure para bypass del Aggregate Root.

---

# Compatibilidad con DDD

El Lifecycle mantiene:

- Aggregate Root única;
- estado encapsulado;
- comportamiento explícito;
- transiciones controladas;
- invariantes;
- identidad estable;
- independencia entre Aggregates;
- consistencia interna fuerte.

Participation controla exclusivamente su propio Lifecycle.

---

# Compatibilidad con CQRS

En CQRS:

```text
Command

↓

Participation Aggregate

↓

Lifecycle Transition

↓

Domain Event

↓

Read Projection
```

Los Read Models reflejan el Lifecycle.

No lo controlan.

---

# Compatibilidad con Event Sourcing

El Lifecycle puede reconstruirse mediante Domain Events.

Los eventos preservan la secuencia de hechos que explica el estado
actual.

Debe mantenerse:

```text
Event History

↓

Lifecycle Reconstruction
```

sin producir nuevas operaciones de negocio durante replay.

---

# Compatibilidad con Event-Driven Architecture

Los Domain Events del Lifecycle pueden ser observados por otros
contextos.

Debe mantenerse:

```text
Participation State Change

↓

Domain Event

↓

External Reaction
```

La reacción externa no forma parte de la transición interna.

---

# Compatibilidad con Clean Architecture

El Lifecycle pertenece al dominio.

No depende de:

```text
HTTP

Database

ORM

Framework

Message Broker

External API
```

La infraestructura implementa persistencia y transporte.

No determina las transiciones válidas.

---

# Compatibilidad con Arquitectura Hexagonal

Los Commands pueden ingresar mediante Application Ports.

El Repository puede persistir mediante Ports y Adapters.

El Lifecycle permanece dentro del núcleo del dominio.

Conceptualmente:

```text
Adapter

↓

Application

↓

Participation

↓

Lifecycle

↓

Repository Port

↓

Adapter
```

---

# Principios Arquitectónicos

El Lifecycle mantiene:

```text
Status

≠

Directly Mutable Attribute
```

```text
Command

≠

Domain Event
```

```text
Authorized

≠

Automatically Valid Transition
```

```text
Registered

≠

Active
```

```text
Completed

≠

Proposal Accepted
```

```text
Completed

≠

Voting Completed
```

```text
Withdrawn

≠

Deleted
```

```text
Invalidated

≠

Deleted
```

```text
Invalidated

≠

Withdrawn
```

```text
Archived

≠

Physical Deletion
```

```text
Membership Lifecycle

≠

Participation Lifecycle
```

```text
Assembly Lifecycle

≠

Participation Lifecycle
```

```text
Proposal Lifecycle

≠

Participation Lifecycle
```

```text
Voting Lifecycle

≠

Participation Lifecycle
```

```text
Read Model State

≠

Lifecycle Authority
```

```text
External System State

≠

Participation Status
```

```text
Replay

≠

New Lifecycle Transition
```

```text
Infrastructure

≠

Lifecycle Definition
```

---

# Documentación Complementaria

El Lifecycle debe interpretarse conjuntamente con:

```text
DOMAIN-008-Aggregate.md

DOMAIN-008B-State-Machine.md

DOMAIN-008C-Commands.md

DOMAIN-008D-Domain-Events.md

DOMAIN-008E-Invariants.md

DOMAIN-008F-Permissions.md

DOMAIN-008G-Repository-Contract.md

DOMAIN-008H-Examples.md

DOMAIN-008I-Versioning.md

DOMAIN-008J-Consistency-Boundary.md

DOMAIN-008K-Integration-Events.md

DOMAIN-008L-Read-Model.md

DOMAIN-008M-Test-Scenarios.md

DOMAIN-008N-Performance-Rules.md

DOMAIN-008O-Security-Model.md

DOMAIN-008P-Extension-Points.md
```

Estos documentos desarrollan dimensiones específicas de
Participation sin sustituir el significado del Lifecycle definido
en este archivo.

---

# Definición de Éxito

El Lifecycle del Aggregate **Participation** define oficialmente la
evolución de una instancia formal de participación dentro de AURA
Core.

Toda Participation comienza en:

```text
Registered
```

y puede evolucionar mediante caminos válidos hacia:

```text
Active

Completed

Withdrawn

Invalidated

Archived
```

El camino principal es:

```text
Registered

↓

Active

↓

Completed

↓

Archived
```

mientras los caminos alternativos permiten representar de forma
explícita retiro e invalidación sin eliminar la identidad ni la
historia del Aggregate.

Cada transición:

- expresa comportamiento del dominio;
- protege invariantes;
- respeta Permissions;
- mantiene coherencia temporal;
- preserva OrganizationId;
- preserva la identidad del actor;
- incrementa Version cuando es válida;
- produce Domain Events cuando corresponde;
- mantiene otros Aggregates fuera de su límite de consistencia.

Los estados:

```text
Completed

Withdrawn

Invalidated
```

representan condiciones diferentes y no deben confundirse entre
sí.

Archived constituye el estado terminal de conservación lógica y
no representa eliminación física.

De esta forma, `DOMAIN-008A-Lifecycle.md` constituye la definición
conceptual oficial del ciclo de vida de **Participation** y
proporciona la base normativa para la State Machine, Commands,
Domain Events, Invariants, Permissions, Versioning, Test Scenarios,
Security Model y demás artefactos de DOMAIN-008, manteniendo la
coherencia de la arquitectura DDD consolidada de AURA Core.