# DOMAIN-008E — Participation Invariants

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
- DOMAIN-008A-Lifecycle.md
- DOMAIN-008B-State-Machine.md
- DOMAIN-008C-Commands.md
- DOMAIN-008D-Domain-Events.md
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
- CORE-005-Domain-Events.md
- CORE-006-Domain-Invariants.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Definir las Invariants oficiales del Aggregate
**Participation**.

Una Invariant representa una condición del dominio que debe
mantenerse verdadera durante toda modificación válida del
Aggregate.

Las Invariants protegen:

- identidad;
- propiedad organizacional;
- contexto participativo;
- clasificación;
- estado;
- ciclo de vida;
- referencias de dominio;
- coherencia temporal;
- versionado;
- consistencia interna;
- límites entre Aggregates.

Una operación que viole una Invariant debe ser rechazada.

El Aggregate nunca puede quedar persistido en un estado que
contradiga las reglas establecidas en este documento.

---

# Propósito

Las Invariants establecen las condiciones que determinan cuándo
una Participation constituye un estado válido del dominio.

Debe mantenerse:

```text
Valid Command

↓

Permission Validation

↓

State Validation

↓

Invariant Validation

↓

Domain Behavior

↓

Valid Participation State
```

Si una Invariant no puede preservarse:

```text
Command

↓

Invariant Violation

↓

Rejected

↓

No State Change
```

---

# Autoridad del Aggregate

La autoridad para proteger las Invariants internas corresponde al
Aggregate Root:

```text
Participation
```

Ningún componente externo puede modificar directamente el estado
interno y posteriormente considerar que las Invariants fueron
satisfechas.

Debe existir:

```text
Application Service

↓

Participation Behavior

↓

Invariant Protection

↓

State Change
```

No debe existir:

```text
Application Service

↓

Direct Attribute Mutation

↓

Persistence
```

---

# Principios

Las Invariants de Participation cumplen los siguientes principios:

- deben ser verdaderas después de toda modificación válida;
- deben protegerse dentro del límite de consistencia;
- no dependen de Infrastructure;
- no dependen de frameworks;
- no dependen de protocolos;
- no pueden omitirse por conveniencia técnica;
- no pueden ser ignoradas por el Repository;
- no pueden ser modificadas por Read Models;
- no pueden ser reemplazadas por validaciones de interfaz;
- no deben confundirse con Permissions;
- no deben confundirse con reglas de presentación;
- no deben depender de Aggregates externos cargados de forma
  mutable;
- deben expresarse mediante lenguaje del dominio;
- deben ser verificables;
- deben producir resultados deterministas para el mismo estado y
  las mismas condiciones de dominio.

---

# Invariant y Validation

Una validación determina si un dato o una operación satisface una
condición.

Una Invariant protege una condición que debe permanecer verdadera
en el Aggregate.

Ejemplo:

```text
ParticipationId must be valid
```

puede implicar validación de formato.

Mientras:

```text
ParticipationId never changes
```

constituye una Invariant de identidad.

Las validaciones apoyan la protección del dominio.

No sustituyen las Invariants.

---

# Invariant y Permission

Debe mantenerse la separación:

```text
Permission

=

Who May Attempt an Operation
```

```text
Invariant

=

Whether the Resulting Domain State Is Valid
```

Un actor autorizado puede ejecutar una intención que igualmente
sea rechazada por una Invariant.

Ejemplo:

```text
Actor Authorized

↓

CompleteParticipation

↓

Current Status = Registered

↓

Invariant / State Rule Violation

↓

Rejected
```

La autorización no convierte una transición inválida en válida.

---

# Invariant y State Machine

La State Machine define las transiciones permitidas.

Las Invariants protegen que el estado resultante sea coherente con
el resto del Aggregate.

Debe mantenerse:

```text
State Transition Rule

+

Invariant Protection

=

Valid Lifecycle Modification
```

Una transición reconocida por la State Machine no puede ejecutarse
si otras Invariants requeridas no se cumplen.

---

# Invariant y Lifecycle

El Lifecycle oficial de Participation utiliza:

```text
Registered

Active

Completed

Withdrawn

Invalidated

Archived
```

Toda Participation debe encontrarse en exactamente uno de estos
estados después de su creación.

No puede encontrarse simultáneamente en múltiples estados.

No puede poseer un estado fuera del modelo oficial.

---

# Clasificación de Invariants

Las Invariants de Participation se organizan conceptualmente en:

```text
Identity Invariants

Organizational Invariants

Reference Invariants

Type Invariants

Lifecycle Invariants

State Invariants

Temporal Invariants

Mutation Invariants

Version Invariants

Consistency Invariants

Aggregate Boundary Invariants

Event Invariants

Archival Invariants
```

Estas categorías permiten documentar las reglas sin fragmentar el
límite de consistencia.

---

# Identity Invariants

La identidad de Participation está determinada por:

```text
ParticipationId
```

Debe cumplirse:

- ParticipationId es obligatorio;
- ParticipationId es único;
- ParticipationId es inmutable;
- ParticipationId no depende de persistencia;
- ParticipationId no depende de OrganizationId;
- ParticipationId no depende de CitizenId;
- ParticipationId no depende de MembershipId;
- ParticipationId no depende de AssemblyId;
- ParticipationId no depende de ProposalId;
- ParticipationId no depende de TerritoryId;
- ParticipationId no depende de ParticipationType;
- ParticipationId no depende de ParticipationStatus;
- ParticipationId no se reutiliza después del archivado lógico.

---

# Inmutabilidad de ParticipationId

Una vez creada la Participation:

```text
ParticipationId = P
```

debe mantenerse:

```text
ParticipationId = P
```

durante toda su existencia.

No está permitido:

```text
ParticipationId = P

↓

ChangeParticipationId

↓

ParticipationId = Q
```

No existe un Command válido para modificar ParticipationId.

---

# Unicidad de ParticipationId

Dos Participation distintas no pueden compartir:

```text
ParticipationId
```

Debe mantenerse:

```text
Participation A

ParticipationId = P1
```

```text
Participation B

ParticipationId = P2
```

con:

```text
P1 ≠ P2
```

cuando representan Aggregates diferentes.

---

# No Reutilización de Identidad

Una Participation archivada conserva su identidad histórica.

No debe permitirse:

```text
ParticipationId = P

↓

Archived

↓

New Participation

ParticipationId = P
```

La desaparición operacional del Aggregate no libera su identidad.

---

# Organizational Invariants

Cada Participation pertenece exactamente a una:

```text
Organization
```

mediante:

```text
OrganizationId
```

Debe cumplirse:

- OrganizationId es obligatorio;
- OrganizationId se establece al crear Participation;
- OrganizationId permanece inmutable;
- una Participation no puede cambiar de Organization;
- OrganizationId representa una referencia de identidad;
- Organization no forma parte del Aggregate Participation.

---

# Inmutabilidad de OrganizationId

Debe mantenerse:

```text
OrganizationId = O1
```

durante toda la vida del Aggregate.

No está permitido:

```text
OrganizationId = O1

↓

ChangeOrganization

↓

OrganizationId = O2
```

La transferencia de una Participation entre Organizations no forma
parte del modelo actual.

---

# Separación Organizacional

Una Participation no puede utilizar una modificación interna para
cambiar silenciosamente su contexto organizacional.

No debe permitirse que:

```text
ChangeParticipationContext
```

modifique:

```text
OrganizationId
```

Debe mantenerse:

```text
Context Change

≠

Organization Ownership Change
```

---

# Reference Invariants

Participation puede mantener referencias hacia otros Aggregates
mediante identificadores de dominio.

Conceptualmente pueden existir referencias como:

```text
CitizenId

MembershipId

AssemblyId

ProposalId

TerritoryId
```

Estas referencias deben respetar las reglas definidas por el
Aggregate.

---

# Regla de Referencias Externas

Las referencias externas se mantienen mediante identidad.

Debe existir:

```text
Participation

↓

AggregateId
```

No:

```text
Participation

↓

Mutable External Aggregate
```

Participation no almacena otros Aggregates completos dentro de su
límite de consistencia.

---

# CitizenId

Cuando una Participation se encuentra asociada a un Citizen, la
relación se representa mediante:

```text
CitizenId
```

CitizenId:

- identifica al Citizen relacionado;
- no incorpora Citizen dentro de Participation;
- no permite modificar Citizen;
- no transfiere la responsabilidad de identidad cívica a
  Participation.

---

# MembershipId

Cuando la Participation requiere contexto de pertenencia
organizacional puede mantener:

```text
MembershipId
```

MembershipId:

- referencia Membership;
- no convierte Membership en entidad interna;
- no permite modificar Membership;
- no permite modificar sus Roles;
- no permite modificar su Lifecycle.

---

# AssemblyId

Cuando Participation ocurre en el contexto de una Assembly puede
mantener:

```text
AssemblyId
```

AssemblyId:

- identifica la Assembly relacionada;
- no incorpora Assembly;
- no permite modificar su programación;
- no permite modificar su convocatoria;
- no permite modificar su estado;
- no permite modificar su modalidad.

---

# ProposalId

Cuando Participation ocurre en relación con una Proposal puede
mantener:

```text
ProposalId
```

ProposalId:

- identifica la Proposal relacionada;
- no incorpora Proposal dentro del Aggregate;
- no permite modificar Proposal;
- no permite ejecutar Commands de Proposal;
- no permite alterar su Lifecycle.

---

# TerritoryId

Cuando la Participation posee contexto territorial puede mantener:

```text
TerritoryId
```

TerritoryId:

- identifica el Territory relacionado;
- no incorpora Territory;
- no permite modificar geometría;
- no permite modificar jerarquía;
- no permite modificar clasificación;
- no permite modificar estado territorial.

---

# Coherencia de Referencias

Las referencias utilizadas por Participation deben ser coherentes
con el contexto definido por el dominio.

Una referencia no puede utilizarse para representar un concepto
distinto de aquel cuya identidad expresa.

Debe mantenerse:

```text
CitizenId

=

Citizen Identity Reference
```

```text
MembershipId

=

Membership Identity Reference
```

```text
AssemblyId

=

Assembly Identity Reference
```

```text
ProposalId

=

Proposal Identity Reference
```

```text
TerritoryId

=

Territory Identity Reference
```

---

# No Mutación Externa

Participation nunca puede modificar directamente:

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

Integration
```

Una operación sobre Participation debe modificar exclusivamente el
estado interno perteneciente a Participation.

---

# Type Invariants

Participation mantiene una clasificación conceptual mediante:

```text
ParticipationType
```

ParticipationType debe:

- ser válido;
- pertenecer al conjunto reconocido por el dominio;
- existir cuando sea obligatorio;
- modificarse únicamente mediante comportamiento explícito;
- respetar el estado actual;
- no modificar implícitamente ParticipationId;
- no modificar OrganizationId;
- no modificar implícitamente ParticipationStatus.

---

# Cambio de ParticipationType

Cuando el Lifecycle permita cambiar ParticipationType debe
utilizarse:

```text
ChangeParticipationType
```

o el comportamiento conceptual equivalente definido por el
Aggregate.

No debe existir:

```text
Participation.Type = NewType
```

como modificación directa desde el exterior.

---

# Cambio Real de Tipo

Una modificación de ParticipationType debe representar un cambio
real.

No debe considerarse una modificación válida:

```text
CurrentType = T

NewType = T
```

cuando no existe diferencia conceptual.

En ese caso no debe producirse:

```text
Version Increment
```

ni:

```text
ParticipationTypeChanged
```

por una operación sin efecto.

---

# Lifecycle Invariants

El Lifecycle oficial debe respetarse en toda operación.

La secuencia normal es:

```text
Registered

↓

Active

↓

Completed

↓

Archived
```

Existen caminos alternativos:

```text
Registered

↓

Withdrawn

↓

Archived
```

```text
Registered

↓

Invalidated

↓

Archived
```

```text
Registered

↓

Active

↓

Withdrawn

↓

Archived
```

```text
Registered

↓

Active

↓

Invalidated

↓

Archived
```

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

No deben inferirse transiciones adicionales.

---

# Estado Inicial

Toda Participation creada válidamente debe comenzar en:

```text
Registered
```

No puede crearse directamente en:

```text
Active

Completed

Withdrawn

Invalidated

Archived
```

---

# Registered Invariants

Cuando:

```text
ParticipationStatus = Registered
```

debe cumplirse:

- la Participation existe;
- ParticipationId está definido;
- OrganizationId está definido;
- ParticipationType es válido;
- CreatedAt está definido;
- StartedAt no existe si nunca fue activada;
- CompletedAt no existe;
- WithdrawnAt no existe;
- InvalidatedAt no existe;
- ArchivedAt no existe.

Registered representa una Participation registrada pero todavía no
activa.

---

# Active Invariants

Cuando:

```text
ParticipationStatus = Active
```

debe cumplirse:

- la Participation fue previamente Registered;
- StartedAt está definido;
- CompletedAt no existe;
- WithdrawnAt no existe;
- InvalidatedAt no existe;
- ArchivedAt no existe;
- el estado anterior válido fue Registered.

Debe existir:

```text
CreatedAt <= StartedAt
```

---

# Completed Invariants

Cuando:

```text
ParticipationStatus = Completed
```

debe cumplirse:

- la Participation fue previamente Active;
- StartedAt está definido;
- CompletedAt está definido;
- WithdrawnAt no existe;
- ArchivedAt no existe;
- la transición hacia Completed ocurrió desde Active.

Debe mantenerse:

```text
CreatedAt <= StartedAt <= CompletedAt
```

Una Participation no puede completarse directamente desde
Registered.

---

# Withdrawn Invariants

Cuando:

```text
ParticipationStatus = Withdrawn
```

debe cumplirse:

- WithdrawnAt está definido;
- ArchivedAt no existe;
- el estado anterior fue Registered o Active;
- CompletedAt no representa una finalización normal posterior al
  retiro;
- la Participation no puede continuar normalmente hacia Active o
  Completed después del retiro.

Si el retiro ocurrió desde Registered:

```text
StartedAt = None
```

cuando nunca existió activación.

Si ocurrió desde Active:

```text
StartedAt
```

debe preservarse como parte de la historia.

---

# Invalidated Invariants

Cuando:

```text
ParticipationStatus = Invalidated
```

debe cumplirse:

- InvalidatedAt está definido;
- la invalidación proviene de un estado permitido;
- la historia anterior permanece preservada;
- ArchivedAt no existe hasta que ocurra el archivado;
- la Participation no puede continuar normalmente hacia Active o
  Completed después de la invalidación.

Los estados origen reconocidos son:

```text
Registered

Active

Completed
```

---

# Invalidation después de Completion

Una Participation completada puede ser invalidada cuando las reglas
del dominio así lo determinen.

Debe mantenerse:

```text
Registered

↓

Active

↓

Completed

↓

Invalidated
```

En este caso:

```text
StartedAt
```

y:

```text
CompletedAt
```

permanecen preservados.

La invalidación no reescribe la historia.

---

# Archived Invariants

Cuando:

```text
ParticipationStatus = Archived
```

debe cumplirse:

- ArchivedAt está definido;
- el estado anterior fue Completed, Withdrawn o Invalidated;
- la identidad permanece preservada;
- OrganizationId permanece preservado;
- la historia permanece preservada;
- el Aggregate no admite nuevas modificaciones ordinarias.

Archived constituye un estado terminal del Lifecycle actual.

---

# Estado Único

Una Participation debe poseer exactamente un:

```text
ParticipationStatus
```

No puede encontrarse simultáneamente en:

```text
Active

and

Completed
```

ni:

```text
Withdrawn

and

Invalidated
```

ni cualquier otra combinación de estados.

Los timestamps históricos no representan estados simultáneos.

---

# State Invariants

Toda modificación de ParticipationStatus debe producirse mediante
una transición reconocida.

No está permitido modificar directamente:

```text
ParticipationStatus
```

Debe existir comportamiento del Aggregate.

---

# Transiciones Permitidas

Las transiciones oficiales son:

```text
None          → Registered

Registered    → Active

Registered    → Withdrawn

Registered    → Invalidated

Active        → Completed

Active        → Withdrawn

Active        → Invalidated

Completed     → Invalidated

Completed     → Archived

Withdrawn     → Archived

Invalidated   → Archived
```

Estas transiciones constituyen la base del modelo actual.

---

# Transiciones No Permitidas

No están permitidas, entre otras:

```text
Registered    → Completed

Registered    → Archived

Active        → Registered

Active        → Archived

Completed     → Active

Completed     → Withdrawn

Withdrawn     → Active

Withdrawn     → Completed

Withdrawn     → Invalidated

Invalidated   → Active

Invalidated   → Completed

Invalidated   → Withdrawn

Archived      → Registered

Archived      → Active

Archived      → Completed

Archived      → Withdrawn

Archived      → Invalidated
```

No deben inferirse transiciones por conveniencia operacional.

---

# No Reactivación después de Withdrawal

Una Participation retirada no puede volver a:

```text
Active
```

mediante el Lifecycle actual.

Debe mantenerse:

```text
Withdrawn

↓

Archived
```

No:

```text
Withdrawn

↓

Active
```

---

# No Reactivación después de Invalidation

Una Participation invalidada no puede reactivarse.

Debe mantenerse:

```text
Invalidated

↓

Archived
```

No:

```text
Invalidated

↓

Active
```

---

# No Reactivación después de Completion

Una Participation completada no vuelve a Active.

Puede:

```text
Completed

↓

Archived
```

o:

```text
Completed

↓

Invalidated

↓

Archived
```

No puede:

```text
Completed

↓

Active
```

---

# No Modificación después de Archive

Una Participation archivada no puede modificarse mediante Commands
ordinarios.

Debe mantenerse:

```text
Archived

=

Terminal State
```

No pueden ejecutarse válidamente sobre una Participation archivada:

```text
ActivateParticipation

CompleteParticipation

WithdrawParticipation

InvalidateParticipation

ChangeParticipationType

ChangeParticipationContext

UpdateParticipationMetadata
```

ni cualquier comportamiento que modifique su estado ordinario.

---

# Temporal Invariants

Participation mantiene timestamps relacionados con su Lifecycle.

Conceptualmente:

```text
CreatedAt

StartedAt

CompletedAt

WithdrawnAt

InvalidatedAt

ArchivedAt
```

Cada timestamp debe corresponder a un hecho real del Lifecycle.

---

# CreatedAt

`CreatedAt`:

- es obligatorio;
- se establece al registrar Participation;
- permanece inmutable;
- representa el momento de creación del Aggregate.

Debe existir desde:

```text
Registered
```

y conservarse durante toda la vida del Aggregate.

---

# StartedAt

`StartedAt` se establece únicamente cuando ocurre:

```text
Registered

↓

Active
```

Debe corresponder al evento:

```text
ParticipationActivated
```

Una Participation nunca activada no debe poseer StartedAt.

---

# CompletedAt

`CompletedAt` se establece únicamente cuando ocurre:

```text
Active

↓

Completed
```

Debe corresponder al evento:

```text
ParticipationCompleted
```

Una Participation que nunca fue completada normalmente no debe
recibir CompletedAt por conveniencia técnica.

---

# WithdrawnAt

`WithdrawnAt` se establece cuando ocurre:

```text
Registered

↓

Withdrawn
```

o:

```text
Active

↓

Withdrawn
```

Debe corresponder al evento:

```text
ParticipationWithdrawn
```

---

# InvalidatedAt

`InvalidatedAt` se establece cuando ocurre una transición válida
hacia:

```text
Invalidated
```

Debe corresponder al evento:

```text
ParticipationInvalidated
```

---

# ArchivedAt

`ArchivedAt` se establece únicamente cuando ocurre:

```text
Completed

↓

Archived
```

```text
Withdrawn

↓

Archived
```

o:

```text
Invalidated

↓

Archived
```

Debe corresponder al evento:

```text
ParticipationArchived
```

---

# Coherencia Temporal General

Los timestamps existentes deben mantener orden cronológico
compatible con la historia real del Aggregate.

Como mínimo:

```text
CreatedAt <= StartedAt
```

cuando StartedAt exista.

Debe mantenerse:

```text
StartedAt <= CompletedAt
```

cuando CompletedAt exista.

También debe mantenerse que:

```text
CreatedAt <= WithdrawnAt
```

```text
CreatedAt <= InvalidatedAt
```

```text
CreatedAt <= ArchivedAt
```

cuando dichos timestamps existan.

---

# Coherencia Temporal de Completion

Para una Participation completada:

```text
CreatedAt

<=

StartedAt

<=

CompletedAt
```

Debe cumplirse siempre.

No puede existir:

```text
CompletedAt < StartedAt
```

---

# Coherencia Temporal de Withdrawal

Si Withdrawal ocurre desde Registered:

```text
CreatedAt <= WithdrawnAt
```

Si Withdrawal ocurre desde Active:

```text
CreatedAt <= StartedAt <= WithdrawnAt
```

---

# Coherencia Temporal de Invalidation

Si Invalidation ocurre desde Registered:

```text
CreatedAt <= InvalidatedAt
```

Si ocurre desde Active:

```text
CreatedAt <= StartedAt <= InvalidatedAt
```

Si ocurre desde Completed:

```text
CreatedAt <= StartedAt <= CompletedAt <= InvalidatedAt
```

---

# Coherencia Temporal de Archive

Si Archive ocurre desde Completed:

```text
CreatedAt

<=

StartedAt

<=

CompletedAt

<=

ArchivedAt
```

Si Archive ocurre desde Withdrawn:

```text
CreatedAt

<=

WithdrawnAt

<=

ArchivedAt
```

y si existió StartedAt antes del retiro:

```text
StartedAt <= WithdrawnAt
```

Si Archive ocurre desde Invalidated:

```text
InvalidatedAt <= ArchivedAt
```

manteniendo además toda la secuencia histórica anterior.

---

# Preservación de Timestamps Históricos

Una transición posterior no elimina timestamps históricos válidos.

Ejemplo:

```text
Registered

↓

Active

↓

Completed

↓

Invalidated
```

debe preservar:

```text
CreatedAt

StartedAt

CompletedAt

InvalidatedAt
```

Invalidation no elimina CompletedAt.

Archive tampoco elimina los timestamps anteriores.

---

# No Timestamps Futuros de Lifecycle

Un estado no puede poseer anticipadamente el timestamp de un hecho
que todavía no ocurrió.

Ejemplo:

```text
Status = Registered
```

no debe contener:

```text
CompletedAt
```

como si Completion ya hubiese ocurrido.

---

# Mutation Invariants

Toda modificación debe ejecutarse mediante comportamiento explícito
del Aggregate.

No se permiten setters públicos para modificar directamente:

```text
ParticipationId

OrganizationId

ParticipationStatus

Version

CreatedAt

StartedAt

CompletedAt

WithdrawnAt

InvalidatedAt

ArchivedAt
```

---

# Modificación Significativa

Una operación que no produce ningún cambio real no debe
considerarse una modificación válida del Aggregate.

Debe mantenerse:

```text
No Effective Change

↓

No Version Increment

↓

No Domain Event
```

cuando la intención no altera el estado conceptual.

---

# Atomicidad de Modificación

Una operación válida debe dejar el Aggregate completamente
consistente.

No puede ocurrir:

```text
Status = Completed
```

sin:

```text
CompletedAt
```

si el modelo exige ambos como resultado de Completion.

Tampoco puede existir:

```text
CompletedAt
```

nuevo mientras:

```text
Status = Active
```

después de confirmar la misma operación.

---

# Version Invariants

Participation utiliza:

```text
Version
```

para representar la evolución confirmada del Aggregate.

Debe cumplirse:

- Version pertenece al Aggregate;
- Version no puede modificarse directamente;
- toda modificación válida incrementa Version;
- una operación rechazada no incrementa Version;
- una consulta no incrementa Version;
- una rehidratación no introduce incrementos adicionales;
- una persistencia sin cambio no incrementa Version;
- el incremento debe ser monotónico.

---

# Incremento de Version

Conceptualmente:

```text
CurrentVersion = N

↓

Valid Domain Change

↓

Version = N + 1
```

No debe existir:

```text
Version = N

↓

Valid Domain Change

↓

Version = N
```

---

# No Incremento por Rechazo

Cuando una operación es rechazada:

```text
CurrentVersion = N

↓

Rejected Command

↓

Version = N
```

La Version no representa intentos.

Representa evolución confirmada.

---

# No Decremento

Version nunca puede disminuir.

No debe existir:

```text
Version = 8

↓

Version = 7
```

como evolución válida del mismo Aggregate.

---

# No Modificación Arbitraria de Version

No existe un comportamiento de dominio como:

```text
setVersion(100)
```

Version se modifica únicamente como consecuencia del mecanismo de
versionado establecido.

La definición completa se desarrolla en:

```text
DOMAIN-008I-Versioning.md
```

---

# Concurrency Invariants

Cuando una modificación utiliza versión esperada debe cumplirse:

```text
ExpectedVersion

=

CurrentVersion
```

antes de confirmar la modificación.

Si:

```text
ExpectedVersion

≠

CurrentVersion
```

debe producirse un conflicto de concurrencia.

La operación no puede sobrescribir silenciosamente una evolución
confirmada por otro proceso.

---

# Consistency Invariants

Participation constituye un límite de consistencia propio.

Toda modificación debe preservar simultáneamente:

```text
ParticipationId

OrganizationId

ParticipationType

ParticipationStatus

Domain References

Lifecycle Timestamps

Version
```

y cualquier otro estado interno perteneciente al Aggregate.

---

# Estado Parcialmente Válido

No debe persistirse un estado parcialmente actualizado.

Ejemplo inválido:

```text
Status = Active

StartedAt = None
```

después de una activación confirmada.

Ejemplo inválido:

```text
Status = Archived

ArchivedAt = None
```

después de un archivado confirmado.

---

# Consistencia Fuerte Interna

Dentro de Participation debe existir consistencia fuerte.

Conceptualmente:

```text
Participation Modification

=

Single Logical Consistency Unit
```

No debe dividirse una modificación interna requerida en múltiples
transacciones independientes que permitan observar estados
intermedios inválidos.

---

# Consistencia Eventual Externa

La coordinación con otros Aggregates puede utilizar consistencia
eventual.

Debe mantenerse:

```text
Participation

↓

Domain Event

↓

External Coordination
```

No se amplía el límite de consistencia para modificar
simultáneamente otros Aggregates.

---

# Aggregate Boundary Invariants

El límite de Participation comprende únicamente conceptos
necesarios para proteger su propia consistencia.

No forman parte de este límite:

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

Integration
```

---

# Regla de No Absorción

La relación contextual con otros Aggregates no convierte esos
Aggregates en entidades internas.

No debe modelarse:

```text
Participation
    │
    └── Assembly
          │
          └── Proposal
```

como una estructura de propiedad.

Debe mantenerse:

```text
Participation
    │
    ├── AssemblyId
    ├── ProposalId
    ├── CitizenId
    ├── MembershipId
    └── TerritoryId
```

cuando dichas referencias correspondan.

---

# No Transacción Distribuida

Una Invariant interna de Participation no debe requerir una
transacción distribuida que modifique múltiples Aggregates.

No debe existir como mecanismo normal:

```text
Participation Transaction

+

Assembly Transaction

+

Proposal Transaction

+

Voting Transaction
```

para considerar válida una modificación interna de Participation.

La coordinación entre Aggregates ocurre fuera de su límite.

---

# External Aggregate State

Cuando una regla requiera conocimiento sobre otro Aggregate, la
coordinación correspondiente debe resolverse fuera del límite de
consistencia de Participation mediante los mecanismos establecidos
por la arquitectura.

Participation no obtiene una referencia mutable a otro Aggregate
para proteger sus propias Invariants.

---

# Event Invariants

Toda modificación significativa aceptada debe producir los Domain
Events definidos por el modelo cuando corresponda.

Debe existir coherencia entre:

```text
Command

Domain Behavior

State Change

Version

Domain Event
```

---

# Evento y Estado

Un evento transicional debe corresponder al estado resultante.

Debe mantenerse:

```text
ParticipationActivated

↓

Status = Active
```

```text
ParticipationCompleted

↓

Status = Completed
```

```text
ParticipationWithdrawn

↓

Status = Withdrawn
```

```text
ParticipationInvalidated

↓

Status = Invalidated
```

```text
ParticipationArchived

↓

Status = Archived
```

---

# Evento y Version

Cuando una modificación válida produce un evento:

```text
DomainEvent.AggregateVersion

=

Participation.Version
```

para la versión resultante de esa modificación.

---

# Evento y Timestamp

Los eventos del Lifecycle deben ser coherentes con los timestamps
del Aggregate.

Debe mantenerse:

```text
ParticipationActivated

↓

StartedAt
```

```text
ParticipationCompleted

↓

CompletedAt
```

```text
ParticipationWithdrawn

↓

WithdrawnAt
```

```text
ParticipationInvalidated

↓

InvalidatedAt
```

```text
ParticipationArchived

↓

ArchivedAt
```

---

# No Evento ante Rechazo

Si una Invariant falla:

```text
Command

↓

Rejected

↓

No State Change

↓

No Version Increment

↓

No Success Domain Event
```

No debe registrarse el evento como si el hecho hubiese ocurrido.

---

# Archival Invariants

Archived constituye un estado terminal.

Una Participation archivada:

- conserva ParticipationId;
- conserva OrganizationId;
- conserva sus referencias históricas;
- conserva sus timestamps;
- conserva Version;
- conserva su historia;
- no puede volver a estados operacionales;
- no puede recibir modificaciones ordinarias.

---

# Archive no es Delete

Debe mantenerse:

```text
Archive

≠

Delete
```

Archivar no significa eliminar la identidad ni borrar la historia
del Aggregate.

No debe reutilizarse ParticipationId después del archivado.

---

# Archive no Reescribe Historia

Cuando:

```text
Completed

↓

Archived
```

se conserva:

```text
CompletedAt
```

Cuando:

```text
Withdrawn

↓

Archived
```

se conserva:

```text
WithdrawnAt
```

Cuando:

```text
Invalidated

↓

Archived
```

se conserva:

```text
InvalidatedAt
```

Archive agrega un nuevo hecho.

No reemplaza los hechos anteriores.

---

# Invariants de Registro

Para crear una Participation válida deben cumplirse como mínimo:

- ParticipationId válido;
- OrganizationId definido;
- ParticipationType válido;
- contexto requerido válido;
- referencias requeridas válidas según el modelo;
- CreatedAt definido;
- estado inicial Registered;
- Version inicial válida;
- ausencia de timestamps pertenecientes a hechos futuros.

Si cualquiera de estas condiciones requeridas falla, la
Participation no debe quedar creada parcialmente.

---

# Invariants de Activación

Para ejecutar:

```text
ActivateParticipation
```

debe cumplirse como mínimo:

```text
CurrentStatus = Registered
```

y las condiciones requeridas por el contexto deben encontrarse
satisfechas.

El resultado debe ser coherente:

```text
Status = Active

StartedAt = Activation Time

Version = PreviousVersion + 1
```

y debe corresponder:

```text
ParticipationActivated
```

---

# Invariants de Completion

Para ejecutar:

```text
CompleteParticipation
```

debe cumplirse:

```text
CurrentStatus = Active
```

Debe existir:

```text
StartedAt
```

El resultado debe mantener:

```text
CompletedAt >= StartedAt
```

y:

```text
Status = Completed
```

---

# Invariants de Withdrawal

Para ejecutar:

```text
WithdrawParticipation
```

el estado debe ser:

```text
Registered
```

o:

```text
Active
```

El resultado debe establecer:

```text
Status = Withdrawn
```

y:

```text
WithdrawnAt
```

sin borrar información histórica previa.

---

# Invariants de Invalidation

Para ejecutar:

```text
InvalidateParticipation
```

el estado debe ser:

```text
Registered

Active

Completed
```

El resultado debe establecer:

```text
Status = Invalidated
```

y:

```text
InvalidatedAt
```

preservando los hechos históricos anteriores.

---

# Invariants de Archive

Para ejecutar:

```text
ArchiveParticipation
```

el estado debe ser:

```text
Completed

Withdrawn

Invalidated
```

El resultado debe establecer:

```text
Status = Archived

ArchivedAt = Archive Time
```

sin eliminar información histórica.

---

# Invariants de Cambio de Tipo

Para ejecutar:

```text
ChangeParticipationType
```

debe cumplirse:

- el estado permite modificación;
- el nuevo ParticipationType es válido;
- existe un cambio real;
- ParticipationId no cambia;
- OrganizationId no cambia;
- ParticipationStatus no cambia implícitamente;
- Version se incrementa únicamente si el cambio es aceptado.

---

# Invariants de Cambio de Contexto

Para ejecutar:

```text
ChangeParticipationContext
```

debe cumplirse:

- el estado permite modificación;
- las nuevas referencias son válidas según el modelo;
- OrganizationId no cambia;
- ParticipationId no cambia;
- no se incorporan Aggregates externos;
- no se modifican Aggregates externos;
- la modificación no introduce una transición implícita;
- el estado resultante continúa siendo válido.

---

# Invariants de Metadata

Para ejecutar:

```text
UpdateParticipationMetadata
```

debe cumplirse:

- el estado permite modificación;
- la metadata pertenece al concepto Participation;
- no se utiliza metadata para modificar atributos protegidos;
- no se utiliza metadata para cambiar ParticipationStatus;
- no se utiliza metadata para cambiar ParticipationId;
- no se utiliza metadata para cambiar OrganizationId;
- no se utiliza metadata para alterar Version directamente;
- existe una modificación efectiva antes de incrementar Version.

---

# Invariants de Referencias Organizacionales

Cuando se utilicen simultáneamente referencias como:

```text
OrganizationId

MembershipId

AssemblyId

ProposalId
```

la coordinación necesaria para verificar coherencia organizacional
debe respetar los límites entre Aggregates.

Participation mantiene las identidades necesarias.

No absorbe el estado completo de los Aggregates referenciados.

---

# Invariants y Membership

La existencia de:

```text
MembershipId
```

no autoriza a Participation a:

- activar Membership;
- suspender Membership;
- asignar Role;
- remover Role;
- cambiar OrganizationId de Membership.

Las reglas propias de Membership permanecen en DOMAIN-003.

---

# Invariants y Role

Role puede formar parte de reglas de autorización externas al
Aggregate.

Participation no modifica:

```text
Role
```

ni convierte Roles en estado interno.

Debe mantenerse:

```text
Authorization Rule

≠

Participation Structural Ownership
```

---

# Invariants y Assembly

Cuando:

```text
AssemblyId
```

forme parte del contexto de Participation, la Participation no
puede utilizarlo para alterar el Lifecycle de Assembly.

No debe existir:

```text
Participation.activate()

↓

Assembly.start()
```

dentro del mismo Aggregate.

---

# Invariants y Proposal

Cuando:

```text
ProposalId
```

forme parte del contexto, Participation no puede alterar Proposal.

No debe existir:

```text
Participation.complete()

↓

Proposal.approve()
```

como comportamiento interno de Participation.

La coordinación corresponde fuera del Aggregate.

---

# Invariants y Voting

Participation no debe absorber las reglas de Voting.

No corresponde a Participation garantizar internamente:

- apertura de una votación;
- emisión de votos;
- conteo;
- resultado;
- cierre de Voting.

Estas responsabilidades pertenecen al Aggregate Voting.

---

# Invariants y Document

Participation no mantiene el contenido completo de Document como
estado interno.

Puede existir una referencia cuando el modelo lo requiera.

La integridad documental pertenece al Aggregate Document.

---

# Invariants y Notification

Participation no garantiza el envío de Notification como parte de
su consistencia interna.

Debe mantenerse:

```text
Valid Participation Change

↓

Domain Event

↓

Notification Process
```

La eventual falla de Notification no revierte automáticamente el
hecho válido ocurrido dentro de Participation.

---

# Invariants y Audit

Audit no forma parte del límite de consistencia de Participation.

Participation produce información trazable mediante:

```text
ParticipationId

Version

Domain Events

Timestamps

Actor References
```

cuando corresponda.

La persistencia y explotación de auditoría pertenece a su propio
modelo.

---

# Invariants e Integration

Una Integration externa no determina directamente la validez
interna de Participation.

Debe mantenerse:

```text
External System Availability

≠

Participation Invariant
```

La indisponibilidad temporal de una plataforma externa no debe
corromper el estado interno del Aggregate.

---

# Invariants y Commands

Todo Command debe ser evaluado contra las Invariants aplicables.

Debe mantenerse:

```text
Command

↓

Applicable Invariants

↓

Accept or Reject
```

La existencia formal de un Command no garantiza su ejecución.

---

# Invariants y Domain Events

Un Domain Event solo puede representar un hecho que haya preservado
las Invariants.

Debe mantenerse:

```text
Invariant Validation

↓

Valid State Change

↓

Domain Event
```

No:

```text
Domain Event

↓

Hope State Is Valid
```

---

# Invariants y Repository

El Repository debe persistir únicamente estados válidos producidos
por Participation.

El Repository no puede corregir silenciosamente un Aggregate
inválido.

No debe existir:

```text
Invalid Participation

↓

Repository Normalization

↓

Valid Database Record
```

como sustituto de las reglas del dominio.

---

# Invariants y Read Model

Los Read Models no protegen las Invariants del Aggregate.

Debe mantenerse:

```text
Write Model

Participation Aggregate

↓

Invariant Protection
```

y:

```text
Read Model

=

Derived Representation
```

Una proyección inconsistente debe corregirse o reconstruirse.

No modifica las reglas del Write Model.

---

# Invariants y Event Sourcing

Cuando Event Sourcing sea utilizado, la secuencia de eventos
aplicada debe reconstruir un estado compatible con las Invariants
históricas correspondientes.

La rehidratación no debe ejecutar nuevamente decisiones de negocio
como si cada evento fuese un Command nuevo.

Debe mantenerse:

```text
Historical Event

↓

Apply Historical Fact

↓

Reconstructed State
```

---

# Rehidratación

La rehidratación de Participation:

- no representa una nueva modificación;
- no incrementa Version adicionalmente;
- no genera nuevos Domain Events;
- no modifica timestamps históricos;
- no ejecuta Permissions nuevamente;
- no altera identidades.

El resultado debe corresponder al estado histórico persistido.

---

# Invariants y CQRS

Las Invariants pertenecen al lado de escritura.

Debe mantenerse:

```text
Command

↓

Participation Aggregate

↓

Invariants

↓

Domain Events
```

Las consultas no pueden modificar el Aggregate ni decidir nuevas
reglas de consistencia.

---

# Invariants y Event-Driven Architecture

La reacción a un Domain Event ocurre después de que Participation
haya preservado sus Invariants.

Debe mantenerse:

```text
Valid Aggregate State

↓

Domain Event

↓

External Reaction
```

No debe dependerse de una reacción externa posterior para completar
una Invariant interna que debería haberse satisfecho antes del
commit.

---

# Invariants y Clean Architecture

Las Invariants pertenecen al dominio.

No deben depender de:

```text
Controller

HTTP Request

Database

ORM

Framework

Message Broker

External API
```

La misma regla debe conservar su significado independientemente del
mecanismo técnico utilizado.

---

# Invariants y Hexagonal Architecture

Los Adapters pueden proporcionar información necesaria a los casos
de uso.

No definen las Invariants del Aggregate.

Debe mantenerse:

```text
Domain Rule

Inside Domain
```

```text
Technical Adapter

Outside Domain
```

---

# Invariants y Persistencia

Una base de datos puede complementar determinadas restricciones
técnicas.

Sin embargo:

```text
Database Constraint

≠

Domain Invariant Definition
```

La regla conceptual debe existir independientemente de la
tecnología de persistencia.

---

# Invariants y Frameworks

Las anotaciones o validaciones de un framework no constituyen la
fuente oficial de las Invariants.

No debe dependerse exclusivamente de:

```text
ORM Validation

HTTP Schema Validation

Frontend Validation
```

para proteger el dominio.

---

# Invariants y UI

La interfaz puede impedir que un usuario seleccione una operación
inválida.

Eso no elimina la obligación del Aggregate de proteger la misma
regla.

Debe mantenerse:

```text
UI Restriction

≠

Domain Protection
```

---

# Invariants y API

Una API puede validar formato y autorización.

Participation continúa siendo responsable de garantizar que el
estado resultante sea válido.

No debe asumirse:

```text
Valid HTTP Request

=

Valid Domain Operation
```

---

# Failure Semantics

Cuando una Invariant falla:

```text
Operation

↓

Rejected
```

El resultado debe preservar el estado anterior.

No debe existir una modificación parcial.

Debe mantenerse:

```text
Previous State

=

Current State
```

después del rechazo.

---

# Estado ante Rechazo

Ante una violación de Invariant no deben modificarse:

```text
ParticipationId

OrganizationId

ParticipationType

ParticipationStatus

Domain References

Lifecycle Timestamps

Version
```

ni cualquier otro estado interno perteneciente a la operación
rechazada.

---

# Evento ante Rechazo

Una violación de Invariant no produce el Domain Event de éxito.

Ejemplo:

```text
Status = Registered

↓

CompleteParticipation

↓

Rejected
```

No debe producir:

```text
ParticipationCompleted
```

---

# Version ante Rechazo

Debe mantenerse:

```text
Version Before = N

↓

Invariant Violation

↓

Version After = N
```

---

# Determinismo

Dado el mismo estado del Aggregate y las mismas condiciones
relevantes del dominio, una Invariant debe producir el mismo
resultado conceptual.

No debe depender de efectos técnicos accidentales para determinar
si el estado es válido.

---

# Observabilidad

La observabilidad técnica de una violación puede incluir:

- logs;
- métricas;
- trazas;
- registros operacionales.

Estos mecanismos pertenecen fuera del Aggregate.

No modifican la semántica de la Invariant.

---

# Seguridad

Las Invariants no deben depender de secretos o credenciales
almacenados dentro de Participation.

Participation no almacena:

```text
Passwords

Tokens

JWT

Private Keys

API Keys

Sessions
```

La seguridad completa se desarrolla en:

```text
DOMAIN-008O-Security-Model.md
```

---

# Protección contra Bypass

No debe existir una ruta de modificación que permita evitar las
Invariants.

Todas las modificaciones válidas deben pasar por:

```text
Participation Aggregate Root
```

Esto incluye modificaciones originadas desde:

- APIs;
- procesos internos;
- jobs;
- integraciones;
- consumidores de eventos;
- herramientas administrativas.

El origen técnico de una intención no modifica las reglas del
dominio.

---

# Bulk Operations

Una operación masiva no puede ignorar las Invariants individuales
de cada Participation.

Conceptualmente:

```text
Bulk Request

↓

Participation A Validation

Participation B Validation

Participation C Validation
```

Cada Aggregate mantiene su propio límite de consistencia.

Una operación masiva no convierte múltiples Participation en un
único Aggregate.

---

# Importaciones

La importación de información externa debe respetar exactamente las
mismas Invariants.

No está permitido:

```text
Import Mode

↓

Disable Domain Rules
```

Los datos importados deben ingresar mediante mecanismos que
preserven el modelo oficial.

---

# Migraciones

Una migración técnica no redefine las Invariants del dominio.

Si una evolución conceptual requiere modificar una Invariant, dicha
modificación debe ser tratada como evolución explícita del modelo.

No debe ocultarse como una simple decisión de persistencia.

---

# Testabilidad

Todas las Invariants deben poder verificarse mediante escenarios
deterministas.

Como mínimo deben existir escenarios para:

```text
Valid Registration

Invalid Registration

Valid Activation

Invalid Activation

Valid Completion

Invalid Completion

Withdrawal from Registered

Withdrawal from Active

Invalid Withdrawal

Invalidation from Registered

Invalidation from Active

Invalidation from Completed

Invalid Invalidation

Archive from Completed

Archive from Withdrawn

Archive from Invalidated

Invalid Archive

Immutable ParticipationId

Immutable OrganizationId

Valid Type Change

Invalid Type Change

Valid Context Change

Invalid Context Change

No Modification after Archive

Temporal Consistency

Version Increment

No Version Increment on Rejection

Concurrency Conflict

External Aggregate Isolation
```

La especificación formal de escenarios corresponde a:

```text
DOMAIN-008M-Test-Scenarios.md
```

---

# Matriz de Invariants por Estado

```text
Invariant                         Registered  Active  Completed  Withdrawn  Invalidated  Archived

ParticipationId immutable         Yes         Yes     Yes        Yes        Yes          Yes

OrganizationId immutable          Yes         Yes     Yes        Yes        Yes          Yes

Valid ParticipationType           Yes         Yes     Yes        Yes        Yes          Yes

CreatedAt required                Yes         Yes     Yes        Yes        Yes          Yes

StartedAt required                No          Yes     Yes        Conditional Conditional  Historical

CompletedAt required              No          No      Yes        No         Conditional  Historical

WithdrawnAt required              No          No      No         Yes        No           Conditional

InvalidatedAt required            No          No      No         No         Yes          Conditional

ArchivedAt required               No          No      No         No         No           Yes

Version valid                     Yes         Yes     Yes        Yes        Yes          Yes

Ordinary mutation allowed         Yes         Yes     Limited    Limited    Limited      No
```

`Conditional` indica que el timestamp depende de la historia
concreta recorrida por la Participation.

`Historical` indica que el valor puede existir y debe preservarse
cuando el estado anterior correspondiente ocurrió.

La matriz no reemplaza las reglas detalladas de este documento ni
la State Machine.

---

# Matriz de Transiciones e Invariants Principales

```text
Transition                    Required Conditions

None → Registered             Valid identity
                              Valid organization
                              Valid type
                              Valid required context
                              Valid creation timestamp

Registered → Active           Current state Registered
                              Valid activation conditions
                              Valid StartedAt

Registered → Withdrawn        Current state Registered
                              Valid withdrawal conditions
                              Valid WithdrawnAt

Registered → Invalidated      Current state Registered
                              Valid invalidation conditions
                              Valid InvalidatedAt

Active → Completed            Current state Active
                              StartedAt exists
                              CompletedAt >= StartedAt

Active → Withdrawn            Current state Active
                              StartedAt preserved
                              WithdrawnAt >= StartedAt

Active → Invalidated          Current state Active
                              StartedAt preserved
                              InvalidatedAt >= StartedAt

Completed → Invalidated       Current state Completed
                              Completion history preserved
                              InvalidatedAt >= CompletedAt

Completed → Archived          Current state Completed
                              CompletedAt preserved
                              ArchivedAt >= CompletedAt

Withdrawn → Archived          Current state Withdrawn
                              WithdrawnAt preserved
                              ArchivedAt >= WithdrawnAt

Invalidated → Archived        Current state Invalidated
                              InvalidatedAt preserved
                              ArchivedAt >= InvalidatedAt
```

---

# Matriz Command / Invariants

```text
Command                      Principal Invariants

RegisterParticipation        Identity
                             Organization
                             Type
                             Required Context
                             Initial State
                             Temporal
                             Version

ActivateParticipation        State
                             Activation Conditions
                             Temporal
                             Version

CompleteParticipation        State
                             StartedAt
                             Temporal
                             Version

WithdrawParticipation        State
                             Temporal
                             Historical Preservation
                             Version

InvalidateParticipation      State
                             Temporal
                             Historical Preservation
                             Version

ArchiveParticipation         State
                             Terminal Transition
                             Historical Preservation
                             Version

ChangeParticipationType      State
                             Valid Type
                             Effective Change
                             Identity Preservation
                             Version

ChangeParticipationContext   State
                             Reference Validity
                             Organization Preservation
                             Aggregate Boundary
                             Version

UpdateParticipationMetadata  State
                             Protected Attributes
                             Effective Change
                             Version
```

---

# Matriz Invariant / Autoridad

```text
Invariant                         Authority

ParticipationId immutable         Participation Aggregate

OrganizationId immutable          Participation Aggregate

ParticipationType valid           Participation Aggregate

ParticipationStatus valid         Participation Aggregate

State transition valid            Participation Aggregate / State Machine

Lifecycle timestamps valid        Participation Aggregate

Version evolution valid           Participation Aggregate / Repository Contract

Aggregate boundary preserved      Participation Aggregate

External reference identity       Participation Aggregate

External Aggregate lifecycle      External Aggregate

Actor authorization               Authorization / Application Layer

Read access authorization         Application Layer

Persistence concurrency           Repository Contract

Projection consistency            Read Side
```

Esta separación evita convertir una regla externa en estado interno
del Aggregate.

---

# Reglas No Negociables

Las siguientes condiciones constituyen reglas fundamentales del
Aggregate Participation:

```text
ParticipationId never changes
```

```text
OrganizationId never changes
```

```text
ParticipationStatus changes only through valid transitions
```

```text
Archived Participation cannot be ordinarily modified
```

```text
Valid modification increments Version
```

```text
Rejected modification does not increment Version
```

```text
External Aggregates are referenced by identity
```

```text
Participation never directly modifies another Aggregate
```

```text
Lifecycle timestamps must reflect actual occurred facts
```

```text
Historical facts are preserved
```

```text
Invariant violation never leaves partial state
```

---

# Restricciones

No está permitido:

- modificar ParticipationId;
- reutilizar ParticipationId;
- modificar OrganizationId;
- modificar ParticipationStatus directamente;
- modificar Version directamente;
- modificar timestamps del Lifecycle directamente;
- crear una Participation en un estado distinto de Registered;
- activar una Participation desde un estado no permitido;
- completar una Participation que no esté Active;
- completar una Participation sin StartedAt;
- retirar una Participation desde un estado no permitido;
- invalidar una Participation desde un estado no permitido;
- archivar una Participation desde un estado no permitido;
- reactivar una Participation Completed;
- reactivar una Participation Withdrawn;
- reactivar una Participation Invalidated;
- modificar ordinariamente una Participation Archived;
- borrar timestamps históricos válidos;
- crear timestamps de hechos que todavía no ocurrieron;
- persistir estados parciales;
- incrementar Version por Commands rechazados;
- incrementar Version por consultas;
- incrementar Version por rehidratación;
- incrementar Version por persistencia sin modificación;
- disminuir Version;
- modificar Aggregates externos;
- almacenar Aggregates externos completos;
- ampliar el límite de consistencia por conveniencia;
- utilizar transacciones distribuidas para proteger una Invariant
  interna;
- delegar la autoridad de las Invariants al Repository;
- delegar la autoridad de las Invariants a la UI;
- delegar la autoridad de las Invariants a la API;
- delegar la autoridad de las Invariants a la base de datos;
- considerar Permission como sustituto de Invariant;
- considerar una validación técnica como sustituto de una regla de
  dominio;
- emitir Domain Events de éxito cuando una Invariant falla;
- utilizar metadata para modificar atributos protegidos;
- utilizar importaciones para omitir reglas del dominio;
- utilizar operaciones masivas para omitir límites de Aggregate;
- depender de Infrastructure para definir la validez conceptual de
  Participation.

---

# Compatibilidad con DDD

Las Invariants de Participation cumplen Domain-Driven Design porque:

- pertenecen al Aggregate;
- protegen su límite de consistencia;
- utilizan lenguaje del dominio;
- preservan identidad;
- protegen Lifecycle;
- protegen comportamiento;
- evitan mutaciones externas;
- mantienen independencia entre Aggregates.

---

# Compatibilidad con Clean Architecture

Las Invariants permanecen independientes de detalles técnicos.

No conocen:

```text
HTTP

Database

ORM

Framework

Message Broker

UI

External Provider
```

---

# Compatibilidad con Hexagonal Architecture

Las Invariants pertenecen al núcleo del dominio.

Los Ports y Adapters pueden facilitar la ejecución de casos de uso,
pero no redefinen las reglas que determinan un estado válido de
Participation.

---

# Compatibilidad con CQRS

Las Invariants protegen exclusivamente el Write Model.

Debe mantenerse:

```text
Command

↓

Participation

↓

Invariant Protection

↓

Domain Event
```

Los Read Models no modifican estas reglas.

---

# Compatibilidad con Event Sourcing

El modelo permite reconstruir la evolución del Aggregate mediante
hechos históricos cuando Event Sourcing sea utilizado.

Las Invariants gobiernan nuevas decisiones.

Los eventos históricos representan decisiones ya ocurridas.

---

# Compatibilidad con Event-Driven Architecture

Las Invariants se satisfacen antes de que un Domain Event
represente el hecho.

Debe mantenerse:

```text
Invariant Valid

↓

State Changed

↓

Domain Event
```

---

# Compatibilidad con Arquitectura Distribuida

Las Invariants internas no dependen de una transacción global entre
servicios o Aggregates.

Participation mantiene consistencia fuerte dentro de su límite y
utiliza coordinación eventual fuera de él.

---

# Evolución

Las Invariants pueden evolucionar cuando cambie explícitamente el
modelo de dominio.

Una nueva regla debe revisarse contra:

```text
Aggregate

Lifecycle

State Machine

Commands

Domain Events

Permissions

Repository Contract

Versioning

Consistency Boundary

Integration Events

Read Models

Test Scenarios

Security Model

Extension Points
```

Una modificación de Invariant no debe introducirse silenciosamente
como una optimización técnica.

---

# Extension Points

Las extensiones futuras pueden incorporar nuevas Invariants cuando
aparezcan nuevos conceptos oficiales de Participation.

Las extensiones deben:

- preservar ParticipationId;
- preservar OrganizationId;
- respetar el Aggregate Root;
- respetar el límite de consistencia;
- mantener independencia entre Aggregates;
- mantener coherencia con Lifecycle;
- mantener coherencia con State Machine;
- mantener coherencia con Commands;
- mantener coherencia con Domain Events;
- mantener coherencia con Versioning.

La definición formal corresponde a:

```text
DOMAIN-008P-Extension-Points.md
```

---

# Documentación Complementaria

Las Invariants deben interpretarse conjuntamente con:

```text
DOMAIN-008-Aggregate.md

DOMAIN-008A-Lifecycle.md

DOMAIN-008B-State-Machine.md

DOMAIN-008C-Commands.md

DOMAIN-008D-Domain-Events.md

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

Cada documento desarrolla una responsabilidad específica sin
reemplazar las Invariants establecidas en este documento.

---

# Principios Arquitectónicos

El modelo oficial de Invariants de Participation mantiene:

```text
Aggregate Root

=

Invariant Authority
```

```text
Permission

≠

Invariant
```

```text
Validation

≠

Invariant
```

```text
Read Model

≠

Invariant Authority
```

```text
Repository

≠

Invariant Authority
```

```text
External Aggregate

≠

Internal Consistency State
```

```text
Valid Domain Change

↓

Invariant Preservation

↓

Version Increment

↓

Domain Event
```

```text
Invariant Violation

↓

No State Change

↓

No Version Increment

↓

No Success Domain Event
```

---

# Definición de Éxito

Las Invariants del Aggregate **Participation** constituyen el
conjunto oficial de condiciones que determinan cuándo su estado es
válido dentro del dominio AURA.

Estas reglas garantizan que:

- Participation posee identidad única e inmutable;
- OrganizationId permanece obligatorio e inmutable;
- las referencias externas se mantienen mediante identificadores;
- otros Aggregates permanecen fuera del límite de consistencia;
- ParticipationType permanece válido;
- ParticipationStatus pertenece al Lifecycle oficial;
- toda transición respeta la State Machine;
- los timestamps representan hechos realmente ocurridos;
- la historia del Aggregate permanece preservada;
- Archived constituye un estado terminal;
- toda modificación válida incrementa Version;
- toda modificación rechazada preserva Version;
- los Domain Events corresponden a hechos válidos;
- ninguna operación deja un estado parcialmente consistente;
- ningún componente externo puede evitar las reglas del Aggregate;
- la coordinación con otros Aggregates permanece fuera de la
  transacción interna de Participation.

La regla fundamental es:

```text
Valid Participation

=

Valid Identity

+

Valid Organization Context

+

Valid Domain References

+

Valid Type

+

Valid Lifecycle State

+

Valid Temporal State

+

Valid Version

+

Preserved Aggregate Boundary
```

Toda operación debe preservar esta condición.

Cuando no pueda preservarse:

```text
Reject Operation

↓

Preserve Previous State

↓

Preserve Version

↓

Emit No Success Domain Event
```

De esta forma,
`DOMAIN-008E-Invariants.md` constituye la definición normativa
oficial de las condiciones de consistencia del Aggregate
**Participation**, preservando su identidad, Lifecycle, State
Machine, referencias, evolución, trazabilidad, independencia entre
Aggregates y límite transaccional conforme al patrón DDD
consolidado de AURA Core.