# DOMAIN-008C — Participation Commands

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
- CORE-005-Domain-Events.md
- CORE-006-Domain-Invariants.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Definir los Commands oficiales que representan la intención de
modificar el estado del Aggregate **Participation**.

Un Command expresa una solicitud explícita de cambio sobre una
Participation.

No representa un hecho consumado.

No garantiza que la modificación solicitada pueda ejecutarse.

Antes de ser aceptado, todo Command debe superar las validaciones
correspondientes de:

- identidad;
- estado;
- Permissions;
- Invariants;
- Version;
- consistencia;
- reglas propias del Aggregate.

Los Commands constituyen la entrada conceptual al lado de
escritura del Aggregate Participation.

---

# Propósito

El modelo de Commands permite expresar de manera explícita las
intenciones que pueden modificar una Participation.

Debe mantenerse:

```text
Actor Intent

↓

Command

↓

Participation Aggregate

↓

State Validation

↓

Permission Validation

↓

Invariant Validation

↓

Version Validation

↓

Domain Behavior

↓

Domain Event
```

El Command solicita una operación.

El Aggregate decide si dicha operación puede ejecutarse.

---

# Principios

Todos los Commands de Participation deben cumplir los siguientes
principios:

- representan una intención de cambio;
- modifican exclusivamente un Aggregate Participation;
- son inmutables;
- poseen identidad propia;
- son auditables;
- contienen únicamente la información necesaria para expresar la
  intención;
- identifican el Aggregate objetivo cuando este ya existe;
- identifican al actor que solicita la operación;
- pueden incluir información de correlación y causalidad;
- pueden incluir ExpectedVersion cuando corresponda;
- deben respetar Permissions;
- deben respetar Invariants;
- deben respetar la State Machine;
- pueden producir uno o más Domain Events;
- nunca representan hechos ya consumados;
- nunca modifican directamente otros Aggregates;
- nunca retornan el estado mutable del Aggregate;
- no contienen lógica de Infrastructure.

---

# Commands y Aggregate Root

Todo Command dirigido a una Participation existente debe ejecutarse
a través de:

```text
Participation
```

como Aggregate Root.

No debe existir:

```text
Command

↓

Direct Attribute Mutation
```

Debe existir:

```text
Command

↓

Participation Aggregate Root

↓

Domain Behavior
```

La Aggregate Root constituye la única autoridad para aceptar o
rechazar la intención expresada por el Command.

---

# Estructura General

Todo Command debe contener, como mínimo, información suficiente
para establecer:

```text
CommandId

ParticipationId

OrganizationId

ActorId

Timestamp

CorrelationId

CausationId

ExpectedVersion
```

La obligatoriedad concreta de determinados campos depende de la
naturaleza del Command.

Para creación, `ParticipationId` identifica la nueva instancia que
se pretende registrar.

Para modificaciones sobre una Participation existente,
`ExpectedVersion` permite aplicar las reglas de concurrencia
optimista establecidas para el Aggregate.

---

# CommandId

`CommandId` identifica de forma única la intención enviada al
sistema.

Debe ser:

- único;
- inmutable;
- independiente de ParticipationId;
- utilizable para trazabilidad;
- utilizable para detección de procesamiento duplicado cuando
  corresponda.

Debe mantenerse:

```text
CommandId

≠

ParticipationId
```

---

# ParticipationId

`ParticipationId` identifica la Participation sobre la cual se
pretende ejecutar el comportamiento.

En:

```text
RegisterParticipation
```

representa la identidad de la nueva Participation.

En los demás Commands representa una Participation existente.

Un Command nunca puede utilizarse para modificar simultáneamente
múltiples Participation.

---

# OrganizationId

`OrganizationId` establece el contexto organizacional dentro del
cual se ejecuta la intención.

Debe corresponder al contexto organizacional de Participation.

No puede utilizarse un Command para trasladar una Participation
desde una Organization hacia otra.

Debe mantenerse:

```text
Command.OrganizationId

=

Participation.OrganizationId
```

cuando la Participation ya existe.

---

# ActorId

`ActorId` identifica al actor responsable de solicitar la
operación.

El actor puede participar en:

- autorización;
- trazabilidad;
- auditoría;
- causalidad;
- registro de responsabilidad.

`ActorId` no sustituye:

```text
CitizenId
```

```text
MembershipId
```

ni cualquier otra referencia que represente al participante dentro
del modelo de Participation.

El actor que ejecuta una operación y el sujeto de la Participation
pueden representar conceptos diferentes.

---

# Timestamp

`Timestamp` representa el momento en que la intención fue
registrada o emitida conforme a las reglas temporales del sistema.

No sustituye los timestamps propios del Lifecycle.

Debe mantenerse:

```text
Command.Timestamp

≠

CreatedAt

≠

StartedAt

≠

CompletedAt

≠

WithdrawnAt

≠

InvalidatedAt
```

Los timestamps del Lifecycle son determinados por el
comportamiento del Aggregate conforme a las reglas del dominio.

---

# CorrelationId

`CorrelationId` permite relacionar múltiples operaciones que
pertenecen a un mismo flujo lógico.

Ejemplo conceptual:

```text
Application Workflow

↓

Command A

↓

Domain Event A

↓

Command B
```

Los elementos pueden compartir:

```text
CorrelationId
```

sin perder sus identidades individuales.

---

# CausationId

`CausationId` permite identificar la causa inmediata de un Command.

Puede referenciar conceptualmente:

- otro Command;
- un Domain Event;
- un Integration Event;
- una operación previa del sistema.

La causalidad no reemplaza las validaciones del Aggregate.

---

# ExpectedVersion

`ExpectedVersion` representa la versión del Aggregate sobre la cual
el emisor espera ejecutar la modificación.

Debe validarse conforme a:

```text
DOMAIN-008I-Versioning.md
```

Conceptualmente:

```text
ExpectedVersion

=

CurrentVersion
```

debe cumplirse antes de confirmar una modificación cuando la
operación esté sujeta a concurrencia optimista.

---

# Datos Comunes

La estructura conceptual general puede representarse como:

```text
ParticipationCommand

CommandId

ParticipationId

OrganizationId

ActorId

Timestamp

CorrelationId

CausationId

ExpectedVersion
```

Cada Command añade únicamente los datos específicos necesarios para
expresar su intención.

---

# Commands Oficiales

El Aggregate Participation reconoce los siguientes Commands
principales:

```text
RegisterParticipation

ActivateParticipation

CompleteParticipation

WithdrawParticipation

InvalidateParticipation

ArchiveParticipation

ChangeParticipationType

ChangeParticipationContext

UpdateParticipationMetadata
```

Los Commands relacionados directamente con transiciones de estado
deben respetar:

```text
DOMAIN-008B-State-Machine.md
```

Los Commands no transicionales deben respetar igualmente el estado
actual y las Invariants aplicables.

---

# RegisterParticipation

## Objetivo

Registrar una nueva instancia formal de Participation.

Este Command representa la intención de crear una Participation
dentro del contexto de una Organization y asociarla al actor o
sujeto participativo correspondiente.

---

## Datos mínimos

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

Según el contexto de Participation pueden existir referencias como:

```text
CitizenId

MembershipId

AssemblyId

ProposalId

TerritoryId
```

cuando correspondan al proceso participativo representado.

Estas referencias identifican otros Aggregates.

No los incorporan dentro del límite de consistencia de
Participation.

---

## Precondiciones

Como mínimo:

- ParticipationId es válido;
- ParticipationId no identifica una Participation existente;
- OrganizationId es válido;
- ParticipationType es válido;
- el contexto participativo requerido está definido;
- las referencias externas requeridas son conceptualmente válidas;
- el actor posee Permission para registrar la Participation;
- las Invariants de creación se cumplen.

---

## Estado origen

No aplica.

La Participation todavía no existe.

---

## Estado destino

```text
Registered
```

---

## Evento esperado

```text
ParticipationRegistered
```

---

## Resultado

Cuando el Command es válido:

```text
No Participation

↓

RegisterParticipation

↓

Participation

Status = Registered
```

El Aggregate queda creado con una identidad y contexto definidos.

---

## Rechazo

Debe rechazarse cuando:

- ParticipationId ya existe;
- OrganizationId no es válido;
- ParticipationType no es válido;
- falta contexto requerido;
- las referencias obligatorias no son válidas;
- el actor no posee Permission;
- alguna Invariant de creación es violada.

Ante rechazo:

```text
No Aggregate Created
```

y no se produce:

```text
ParticipationRegistered
```

---

# ActivateParticipation

## Objetivo

Solicitar el inicio formal de una Participation previamente
registrada.

---

## Datos mínimos

```text
CommandId

ParticipationId

OrganizationId

ActorId

Timestamp

CorrelationId

CausationId

ExpectedVersion
```

---

## Estado origen

```text
Registered
```

---

## Estado destino

```text
Active
```

---

## Precondiciones

- Participation existe;
- CurrentStatus es Registered;
- OrganizationId coincide con el Aggregate;
- contexto participativo requerido permanece válido;
- condiciones necesarias para comenzar están satisfechas;
- el actor posee Permission;
- las Invariants aplicables se cumplen;
- ExpectedVersion coincide con CurrentVersion.

---

## Evento esperado

```text
ParticipationActivated
```

---

## Efectos de dominio

Una ejecución válida debe:

```text
Status = Active
```

establecer:

```text
StartedAt
```

incrementar:

```text
Version
```

y producir:

```text
ParticipationActivated
```

---

## Rechazo

Debe rechazarse desde:

```text
Active

Completed

Withdrawn

Invalidated

Archived
```

También debe rechazarse cuando:

- Permission es insuficiente;
- alguna Invariant falla;
- existe conflicto de Version;
- OrganizationId no corresponde al Aggregate.

---

# CompleteParticipation

## Objetivo

Solicitar la finalización normal de una Participation activa.

---

## Datos mínimos

```text
CommandId

ParticipationId

OrganizationId

ActorId

Timestamp

CorrelationId

CausationId

ExpectedVersion
```

---

## Estado origen

```text
Active
```

---

## Estado destino

```text
Completed
```

---

## Precondiciones

- Participation existe;
- CurrentStatus es Active;
- StartedAt existe;
- las condiciones de finalización se cumplen;
- el actor posee Permission;
- las Invariants aplicables se cumplen;
- ExpectedVersion coincide con CurrentVersion.

---

## Evento esperado

```text
ParticipationCompleted
```

---

## Efectos de dominio

Debe establecer:

```text
Status = Completed
```

Debe establecer:

```text
CompletedAt
```

Debe preservar:

```text
StartedAt
```

Debe incrementar:

```text
Version
```

Debe producir:

```text
ParticipationCompleted
```

---

## Rechazo

Debe rechazarse desde:

```text
Registered

Completed

Withdrawn

Invalidated

Archived
```

No existe:

```text
Registered → Completed
```

como transición directa.

---

# WithdrawParticipation

## Objetivo

Solicitar el retiro de una Participation antes de su finalización
normal.

Withdrawal representa retiro.

No representa:

```text
Completion
```

```text
Invalidation
```

```text
Deletion
```

```text
Archive
```

---

## Datos mínimos

```text
CommandId

ParticipationId

OrganizationId

ActorId

Timestamp

CorrelationId

CausationId

ExpectedVersion
```

Cuando las reglas del dominio requieran registrar el contexto del
retiro puede incluirse:

```text
WithdrawalReason
```

La razón debe representar información de dominio y no una
excepción técnica.

---

## Estados origen

```text
Registered

Active
```

---

## Estado destino

```text
Withdrawn
```

---

## Precondiciones

- Participation existe;
- CurrentStatus es Registered o Active;
- el retiro está permitido;
- el actor posee Permission;
- las Invariants aplicables se cumplen;
- ExpectedVersion coincide con CurrentVersion.

---

## Evento esperado

```text
ParticipationWithdrawn
```

---

## Efectos desde Registered

Debe establecer:

```text
Status = Withdrawn
```

Debe establecer:

```text
WithdrawnAt
```

No debe crear:

```text
StartedAt
```

si la Participation nunca fue activada.

---

## Efectos desde Active

Debe establecer:

```text
Status = Withdrawn
```

Debe establecer:

```text
WithdrawnAt
```

Debe preservar:

```text
StartedAt
```

---

## Versionado

En ambos casos debe incrementarse:

```text
Version
```

---

## Rechazo

Debe rechazarse desde:

```text
Completed

Withdrawn

Invalidated

Archived
```

No debe utilizarse Withdrawal para simular una invalidación o
eliminación.

---

# InvalidateParticipation

## Objetivo

Solicitar que una Participation pierda formalmente su validez.

Invalidation representa una decisión explícita del dominio.

No constituye eliminación ni rollback.

---

## Datos mínimos

```text
CommandId

ParticipationId

OrganizationId

ActorId

InvalidationReason

Timestamp

CorrelationId

CausationId

ExpectedVersion
```

---

## Estados origen

```text
Registered

Active

Completed
```

---

## Estado destino

```text
Invalidated
```

---

## Precondiciones

- Participation existe;
- CurrentStatus pertenece a los estados permitidos;
- existe una causa válida de invalidación;
- el actor posee Permission para invalidar;
- las Invariants aplicables se cumplen;
- ExpectedVersion coincide con CurrentVersion.

---

## Evento esperado

```text
ParticipationInvalidated
```

---

## Efectos de dominio

Debe establecer:

```text
Status = Invalidated
```

Debe establecer:

```text
InvalidatedAt
```

Debe conservar todos los timestamps históricos válidos.

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

debe conservar:

```text
CreatedAt

StartedAt

CompletedAt

InvalidatedAt
```

---

## Versionado

Debe incrementar:

```text
Version
```

---

## Rechazo

Debe rechazarse desde:

```text
Withdrawn

Invalidated

Archived
```

También debe rechazarse cuando:

- no existe causa válida;
- Permission es insuficiente;
- alguna Invariant es violada;
- existe conflicto de Version.

---

# ArchiveParticipation

## Objetivo

Solicitar el archivado lógico de una Participation cuyo flujo
operacional ha terminado.

Archive no representa eliminación física.

---

## Datos mínimos

```text
CommandId

ParticipationId

OrganizationId

ActorId

Timestamp

CorrelationId

CausationId

ExpectedVersion
```

---

## Estados origen

```text
Completed

Withdrawn

Invalidated
```

---

## Estado destino

```text
Archived
```

---

## Precondiciones

- Participation existe;
- CurrentStatus es archivable;
- el actor posee Permission;
- las Invariants aplicables se cumplen;
- ExpectedVersion coincide con CurrentVersion.

---

## Evento esperado

```text
ParticipationArchived
```

---

## Efectos de dominio

Debe establecer:

```text
Status = Archived
```

Debe preservar:

- ParticipationId;
- OrganizationId;
- contexto;
- referencias;
- timestamps históricos;
- Version previa como parte de la evolución;
- historia de eventos.

Debe incrementar:

```text
Version
```

---

## Rechazo

Debe rechazarse desde:

```text
Registered

Active

Archived
```

No puede archivarse una Participation que todavía se encuentra en
un estado operacional.

---

# ChangeParticipationType

## Objetivo

Modificar la clasificación conceptual de una Participation cuando
el estado actual y las reglas del dominio lo permitan.

---

## Datos mínimos

```text
CommandId

ParticipationId

OrganizationId

ActorId

ParticipationType

Timestamp

CorrelationId

CausationId

ExpectedVersion
```

---

## Regla

`ParticipationType` debe pertenecer al conjunto de tipos
reconocidos por el Aggregate.

El cambio no modifica:

```text
ParticipationId
```

ni:

```text
OrganizationId
```

---

## Estados permitidos

El cambio debe limitarse a estados en los cuales la clasificación
todavía pueda modificarse conforme al modelo del Aggregate.

Como regla conceptual, las modificaciones estructurales deben
realizarse antes de que el Lifecycle alcance estados de cierre.

La validación exacta corresponde a las Invariants definidas en:

```text
DOMAIN-008E-Invariants.md
```

---

## Evento esperado

```text
ParticipationTypeChanged
```

cuando la modificación sea válida.

---

## Efectos

Debe:

- validar el nuevo tipo;
- mantener identidad;
- mantener contexto organizacional;
- incrementar Version;
- producir el Domain Event correspondiente.

---

# ChangeParticipationContext

## Objetivo

Modificar información contextual de Participation cuando dicha
información sea mutable conforme al estado y a las Invariants.

El contexto puede comprender referencias de dominio como:

```text
TerritoryId

AssemblyId

ProposalId
```

cuando formen parte del modelo establecido para la Participation.

---

## Datos mínimos

```text
CommandId

ParticipationId

OrganizationId

ActorId

ContextChanges

Timestamp

CorrelationId

CausationId

ExpectedVersion
```

---

## Regla de Referencias

ChangeParticipationContext no puede utilizarse para incorporar
Aggregates completos.

Debe utilizar exclusivamente referencias mediante identidad.

Debe mantenerse:

```text
Participation

↓

AggregateId
```

y nunca:

```text
Participation

↓

Mutable External Aggregate
```

---

## Restricciones

No puede utilizarse para modificar:

```text
ParticipationId

OrganizationId

Status

Version
```

directamente.

Tampoco puede utilizarse para sustituir arbitrariamente la
identidad contextual del participante cuando esta se encuentre
protegida por las Invariants del Aggregate.

---

## Evento esperado

Cuando exista una modificación válida debe producirse el Domain
Event definido para el cambio contextual correspondiente.

La definición formal de eventos pertenece a:

```text
DOMAIN-008D-Domain-Events.md
```

---

# UpdateParticipationMetadata

## Objetivo

Actualizar información descriptiva o metadata no estructural de
Participation cuando el estado actual lo permita.

Este Command no debe utilizarse como mecanismo genérico para
evadir comportamientos explícitos del Aggregate.

---

## Datos mínimos

```text
CommandId

ParticipationId

OrganizationId

ActorId

Metadata

Timestamp

CorrelationId

CausationId

ExpectedVersion
```

---

## Restricciones

No puede modificar mediante metadata:

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
```

Tampoco puede modificar indirectamente conceptos que posean un
Command específico.

---

## Evento esperado

```text
ParticipationMetadataUpdated
```

cuando la modificación sea válida y dicho evento forme parte del
modelo oficial de eventos.

---

# Commands Transicionales

Los Commands que modifican `ParticipationStatus` son:

```text
RegisterParticipation

ActivateParticipation

CompleteParticipation

WithdrawParticipation

InvalidateParticipation

ArchiveParticipation
```

Su relación oficial con la State Machine es:

```text
Command                      Origin         Destination

RegisterParticipation        None           Registered

ActivateParticipation        Registered     Active

CompleteParticipation        Active         Completed

WithdrawParticipation        Registered     Withdrawn

WithdrawParticipation        Active         Withdrawn

InvalidateParticipation      Registered     Invalidated

InvalidateParticipation      Active         Invalidated

InvalidateParticipation      Completed      Invalidated

ArchiveParticipation         Completed      Archived

ArchiveParticipation         Withdrawn      Archived

ArchiveParticipation         Invalidated    Archived
```

No existen otras transiciones implícitas.

---

# Commands No Transicionales

Los Commands no transicionales modifican información del Aggregate
sin cambiar `ParticipationStatus`.

Conceptualmente incluyen:

```text
ChangeParticipationType

ChangeParticipationContext

UpdateParticipationMetadata
```

Debe mantenerse:

```text
Valid Non-Transitional Command

↓

Aggregate Modification

↓

Same ParticipationStatus

↓

Version Increment

↓

Domain Event
```

---

# Regla de No Transición Implícita

Un Command no transicional nunca puede cambiar Status como efecto
secundario.

Ejemplo:

```text
ChangeParticipationType
```

no puede producir implícitamente:

```text
Registered → Active
```

Si el dominio requiere una transición, debe utilizarse el Command
transicional correspondiente.

---

# Matriz Command / Estado

```text
Command                      Registered   Active   Completed   Withdrawn   Invalidated   Archived

ActivateParticipation        YES          NO       NO          NO          NO            NO

CompleteParticipation        NO           YES      NO          NO          NO            NO

WithdrawParticipation        YES          YES      NO          NO          NO            NO

InvalidateParticipation      YES          YES      YES         NO          NO            NO

ArchiveParticipation         NO           NO       YES         YES         YES           NO
```

Los Commands no transicionales dependen de las Invariants y reglas
de modificación definidas para cada estado.

---

# Matriz Command / Evento

```text
Command                      Domain Event

RegisterParticipation        ParticipationRegistered

ActivateParticipation        ParticipationActivated

CompleteParticipation        ParticipationCompleted

WithdrawParticipation        ParticipationWithdrawn

InvalidateParticipation      ParticipationInvalidated

ArchiveParticipation         ParticipationArchived

ChangeParticipationType      ParticipationTypeChanged

ChangeParticipationContext   Context-specific Domain Event

UpdateParticipationMetadata  ParticipationMetadataUpdated
```

La definición normativa completa de cada evento corresponde a:

```text
DOMAIN-008D-Domain-Events.md
```

---

# Validación de Commands

Todo Command debe pasar conceptualmente por:

```text
Command Received

↓

Structural Validation

↓

Identity Validation

↓

Aggregate Load

↓

Organization Validation

↓

Permission Validation

↓

State Validation

↓

Invariant Validation

↓

ExpectedVersion Validation

↓

Domain Behavior

↓

Domain Event

↓

Persistence
```

No todos los pasos requieren necesariamente una implementación
técnica separada.

La secuencia representa responsabilidades conceptuales.

---

# Validación Estructural

La validación estructural determina que el Command contenga los
datos mínimos requeridos.

Ejemplos:

- CommandId presente;
- ParticipationId presente;
- OrganizationId presente;
- ActorId presente;
- datos específicos requeridos presentes;
- formatos conceptualmente válidos.

Una estructura inválida no debe llegar a producir una modificación
del Aggregate.

---

# Validación de Identidad

La identidad debe proteger:

```text
ParticipationId
```

Un Command sobre una Participation existente debe dirigirse
exactamente a dicha identidad.

No puede utilizarse un Command para sustituir la identidad del
Aggregate.

---

# Validación Organizacional

Debe mantenerse:

```text
Command.OrganizationId

=

Participation.OrganizationId
```

Una discrepancia debe provocar rechazo.

Esto protege el límite organizacional del Aggregate.

---

# Validación de Permissions

Todo Command debe ejecutarse únicamente cuando el actor posea la
capacidad correspondiente.

Conceptualmente:

```text
Actor

+

Command

+

Participation Context

↓

Permission Evaluation
```

Si el resultado es:

```text
Denied
```

el Command no modifica el Aggregate.

Las reglas completas se definen en:

```text
DOMAIN-008F-Permissions.md
```

---

# Validación de Estado

Los Commands transicionales deben respetar:

```text
DOMAIN-008B-State-Machine.md
```

Debe cumplirse:

```text
CurrentState ∈ AllowedSourceStates
```

Si el estado no permite el Command:

```text
Command Rejected
```

---

# Validación de Invariants

Un Command no puede ejecutarse si deja el Aggregate en un estado
inválido.

Debe mantenerse:

```text
Command

+

Valid State Transition

+

Invariant Violation

=

Rejected
```

Las Invariants se definen formalmente en:

```text
DOMAIN-008E-Invariants.md
```

---

# Validación de Version

Cuando corresponda:

```text
ExpectedVersion

=

CurrentVersion
```

debe cumplirse antes de confirmar la modificación.

Una versión obsoleta debe producir un conflicto de concurrencia y
no una sobrescritura silenciosa.

---

# Orden de Validación

El orden técnico concreto puede variar siempre que no altere las
garantías conceptuales.

Debe asegurarse que ningún Command confirmado haya evitado:

- Permissions;
- State Machine;
- Invariants;
- Versioning;
- consistencia del Aggregate.

---

# Aceptación de Command

Un Command se considera aceptado cuando la intención ha sido
validada y el comportamiento correspondiente puede modificar
válidamente el Aggregate.

Conceptualmente:

```text
Command

↓

Accepted

↓

Domain Behavior

↓

State Change or Valid Mutation

↓

Version Increment

↓

Domain Event
```

---

# Rechazo de Commands

El Aggregate debe rechazar un Command cuando ocurra cualquiera de
las siguientes situaciones:

- ParticipationId no existe cuando debería existir;
- ParticipationId ya existe durante registro;
- OrganizationId no corresponde;
- el estado actual no permite la operación;
- el actor no posee Permission;
- se viola una Invariant;
- ExpectedVersion no coincide;
- faltan datos obligatorios;
- el tipo de Participation no es válido;
- el contexto requerido no es válido;
- una referencia externa requerida es inválida;
- el Aggregate se encuentra Archived;
- el Command intenta modificar identidad;
- el Command intenta modificar Status directamente;
- el Command intenta modificar Version directamente;
- el Command intenta modificar otro Aggregate;
- el Command intenta ejecutar una transición inexistente.

---

# Efectos del Rechazo

Ante un Command rechazado:

```text
Participation State

=

Unchanged
```

```text
Version

=

Unchanged
```

```text
Lifecycle Timestamps

=

Unchanged
```

```text
Success Domain Events

=

None
```

No debe persistirse un estado parcial.

---

# Commands sobre Archived

Una Participation Archived no acepta Commands operacionales
normales.

Debe rechazarse:

```text
ActivateParticipation

CompleteParticipation

WithdrawParticipation

InvalidateParticipation

ArchiveParticipation

ChangeParticipationType

ChangeParticipationContext

UpdateParticipationMetadata
```

cuando el Aggregate ya se encuentra Archived.

Archived constituye el estado terminal del Lifecycle actual.

---

# Commands Duplicados

La repetición de un Command no implica automáticamente una nueva
operación válida.

Ejemplo:

```text
ActivateParticipation
```

ejecutado exitosamente produce:

```text
Registered → Active
```

Un segundo `ActivateParticipation` encuentra:

```text
Status = Active
```

y no representa una nueva transición válida.

---

# Idempotencia

La infraestructura o capa Application puede utilizar `CommandId`
para evitar procesamiento duplicado.

Sin embargo:

```text
Idempotency

≠

State Machine
```

La idempotencia no puede convertir una transición inválida en una
transición válida.

---

# Commands Fuera de Orden

Los Commands recibidos fuera del orden del Lifecycle deben ser
rechazados.

Ejemplo:

```text
RegisterParticipation

↓

CompleteParticipation
```

sin:

```text
ActivateParticipation
```

no constituye una secuencia válida.

Debe mantenerse:

```text
Registered

↓

CompleteParticipation

↓

Rejected
```

---

# Commands Concurrentes

Dos Commands pueden intentar modificar simultáneamente la misma
Participation.

Ejemplo:

```text
Status = Active
Version = 8
```

Command A:

```text
CompleteParticipation
ExpectedVersion = 8
```

Command B:

```text
WithdrawParticipation
ExpectedVersion = 8
```

Solo una modificación puede confirmarse sobre la misma versión.

La segunda debe reevaluarse contra la nueva Version y el nuevo
estado.

---

# Command y Domain Event

Debe mantenerse estrictamente:

```text
Command

=

Intent
```

```text
Domain Event

=

Occurred Fact
```

Ejemplo:

```text
ActivateParticipation
```

no significa:

```text
ParticipationActivated
```

hasta que el Aggregate acepte y ejecute válidamente la operación.

---

# Command Rechazado y Eventos

Un Command rechazado no produce el evento de éxito correspondiente.

Ejemplo:

```text
Status = Completed

Command = ActivateParticipation
```

Resultado:

```text
Rejected
```

No debe producir:

```text
ParticipationActivated
```

---

# Command y Integration Event

Un Command no debe publicarse directamente como Integration Event
para representar un hecho.

Debe mantenerse:

```text
Command

↓

Aggregate

↓

Domain Event

↓

Integration Mapping

↓

Integration Event
```

Los Integration Events se definen en:

```text
DOMAIN-008K-Integration-Events.md
```

---

# Command y Audit

Los Commands pueden formar parte de la trazabilidad del sistema.

Información conceptual relevante:

```text
CommandId

ParticipationId

OrganizationId

ActorId

Timestamp

CorrelationId

CausationId

ExpectedVersion
```

Audit puede utilizar dicha información conforme a sus propias
responsabilidades.

Participation no incorpora el Aggregate Audit dentro de su límite.

---

# Command y Notification

Un Command no envía Notifications directamente.

Ejemplo:

```text
ActivateParticipation
```

puede producir:

```text
ParticipationActivated
```

y posteriormente otro componente puede reaccionar.

Debe mantenerse:

```text
Command

↓

Participation

↓

Domain Event

↓

Notification Process
```

---

# Command y Organization

Participation puede mantener:

```text
OrganizationId
```

pero un Command de Participation nunca modifica Organization.

No debe existir:

```text
Participation Command

↓

Modify Organization
```

---

# Command y Citizen

Cuando Participation referencia:

```text
CitizenId
```

el Command puede utilizar esa identidad como contexto.

No puede modificar:

```text
Citizen
```

El Aggregate Citizen conserva su propio límite de consistencia.

---

# Command y Membership

Cuando Participation referencia:

```text
MembershipId
```

el Command no puede:

- activar Membership;
- suspender Membership;
- cambiar sus Roles;
- modificar su estado;
- alterar su ciclo de vida.

Membership permanece independiente.

---

# Command y Role

Role puede intervenir en la evaluación de Permissions.

No forma parte del Command como Aggregate mutable.

Debe mantenerse:

```text
Role Context

↓

Permission Evaluation
```

No:

```text
Participation Command

↓

Modify Role
```

---

# Command y Territory

Cuando exista contexto territorial, el Command puede contener:

```text
TerritoryId
```

No puede modificar Territory.

La referencia territorial se mantiene mediante identidad.

---

# Command y Assembly

Cuando Participation ocurra en el contexto de una Assembly puede
utilizar:

```text
AssemblyId
```

como referencia.

No puede:

- iniciar Assembly;
- completar Assembly;
- cancelar Assembly;
- modificar su convocatoria;
- modificar su programación.

Assembly mantiene su propia State Machine.

---

# Command y Proposal

Cuando Participation se relacione con Proposal puede utilizar:

```text
ProposalId
```

como referencia contextual.

El Command de Participation no modifica Proposal.

No puede aceptar, rechazar, retirar ni archivar una Proposal.

---

# Command y Voting

Voting mantiene su propio Aggregate y Lifecycle.

Un Command de Participation no ejecuta una votación ni modifica su
resultado.

Debe mantenerse:

```text
Participation Command

≠

Voting Command
```

---

# Command y Document

Un Command de Participation no crea ni modifica directamente un
Document.

Puede originar Domain Events que posteriormente produzcan
coordinaciones documentales.

Document conserva su propio límite.

---

# Command y Notification

Notification no forma parte de Participation.

Un Command puede provocar un Domain Event relevante para
Notification, pero no debe contener lógica de envío.

---

# Command y Audit

Audit registra o consume información de trazabilidad según su
propio modelo.

Participation no debe almacenar el Aggregate Audit como resultado
de ejecutar un Command.

---

# Command e Integration

Los Commands no conocen:

```text
HTTP Endpoints

External APIs

OAuth

JWT

SDKs

Message Brokers

FIWARE

NGSI-LD
```

Estas responsabilidades pertenecen a capas externas.

El Command expresa intención de dominio.

---

# Consistencia

Cada Command debe modificar exclusivamente:

```text
One Participation Aggregate
```

La operación debe mantener una única frontera de consistencia.

Debe evitarse:

```text
Command

↓

Participation + Assembly + Proposal + Voting
```

dentro de una misma transacción de dominio distribuida.

---

# Consistencia Eventual

Cuando un Command produzca efectos relevantes para otros
Aggregates:

```text
Participation Command

↓

Participation Domain Event

↓

External Coordination
```

La coordinación posterior puede utilizar consistencia eventual.

El Command original no amplía el límite de consistencia de
Participation.

---

# Atomicidad

Una ejecución válida debe ser atómica dentro del Aggregate.

Conceptualmente:

```text
Validate

↓

Modify

↓

Increment Version

↓

Register Domain Event
```

debe producir una modificación consistente.

No debe existir:

```text
Status changed

but

Version unchanged
```

ni:

```text
State changed

but

Domain Event represents another result
```

---

# Persistencia

Los Commands no persisten directamente.

Debe mantenerse:

```text
Command

↓

Aggregate Behavior

↓

Repository
```

No:

```text
Command

↓

Database
```

El Repository Contract se define en:

```text
DOMAIN-008G-Repository-Contract.md
```

---

# Repository y Commands

El Repository puede utilizarse para recuperar y persistir el
Aggregate requerido por un Command.

No debe contener métodos que sustituyan comportamiento del
Aggregate.

No debe existir como mecanismo de dominio:

```text
repository.complete_participation()
```

si dicha operación evita ejecutar:

```text
Participation.complete()
```

o el comportamiento equivalente definido por la Aggregate Root.

---

# Commands y Rehidratación

Cargar una Participation desde persistencia no constituye un
Command.

Debe mantenerse:

```text
Repository Load

≠

Domain Intent
```

La rehidratación:

- no incrementa Version;
- no produce nuevos Domain Events;
- no modifica Status;
- no altera timestamps.

---

# Commands y CQRS

Participation utiliza la separación conceptual:

```text
Write Side

Commands

↓

Participation Aggregate

↓

Domain Events
```

y:

```text
Read Side

Read Models
```

Los Commands pertenecen exclusivamente al lado de escritura.

---

# Commands y Read Models

Los Commands no consultan Read Models como autoridad para decidir
la validez interna del Aggregate.

Un Read Model puede ayudar a la capa Application en búsquedas o
presentación.

Sin embargo:

```text
Read Model State

≠

Aggregate State Authority
```

---

# Commands y Event Sourcing

En una implementación compatible con Event Sourcing:

```text
Command

↓

Rehydrated Aggregate

↓

Domain Behavior

↓

New Domain Event
```

Los Commands no forman necesariamente parte de la secuencia de
eventos que reconstruye el estado.

La historia autoritativa está compuesta por hechos ocurridos, no
por intenciones.

---

# Commands y Event-Driven Architecture

Los Commands pueden iniciar comportamientos que produzcan Domain
Events.

Debe mantenerse:

```text
Command

↓

Domain Decision

↓

Domain Event
```

No debe asumirse:

```text
Command

=

Event
```

---

# Commands y Clean Architecture

Los Commands pertenecen conceptualmente al modelo de escritura y
deben permanecer independientes de Infrastructure.

No deben depender de:

```text
Database

ORM

HTTP

REST

GraphQL

FastAPI

Django

React

Message Broker

External API
```

---

# Commands y Hexagonal Architecture

Los mecanismos externos pueden transformar una intención recibida
en un Command.

Ejemplo:

```text
Driving Adapter

↓

Application

↓

Command

↓

Participation Aggregate
```

La semántica del Command no depende del adaptador que lo originó.

---

# Commands y API

Una operación HTTP puede mapearse a un Command.

Sin embargo:

```text
HTTP Request

≠

Command
```

El transporte pertenece a Infrastructure o Interface.

El Command pertenece al modelo de intención del dominio.

---

# Commands y Seguridad

Los Commands deben protegerse contra:

- modificación de OrganizationId;
- suplantación del actor;
- ejecución sin Permission;
- replay indebido;
- Command duplicado;
- manipulación de ExpectedVersion;
- referencias cruzadas entre Organizations;
- modificación directa de Status;
- modificación directa de Version;
- modificación de identidad;
- bypass del Aggregate Root.

El modelo completo se desarrolla en:

```text
DOMAIN-008O-Security-Model.md
```

---

# Commands y Performance

Las optimizaciones no pueden eliminar:

- validación de estado;
- validación de Permission;
- validación de Invariants;
- validación de Version;
- ejecución mediante Aggregate Root.

No debe utilizarse una actualización directa en persistencia como
optimización de un Command.

Las reglas se desarrollan en:

```text
DOMAIN-008N-Performance-Rules.md
```

---

# Commands y Testabilidad

Cada Command debe poder probarse mediante escenarios deterministas.

Como mínimo deben verificarse:

- ejecución válida;
- estado origen correcto;
- estado destino correcto;
- Domain Event esperado;
- incremento de Version;
- timestamps correspondientes;
- rechazo por estado;
- rechazo por Permission;
- rechazo por Invariant;
- rechazo por Version;
- rechazo por Organization incorrecta;
- rechazo sobre Archived;
- ausencia de efectos parciales.

Los escenarios formales se documentan en:

```text
DOMAIN-008M-Test-Scenarios.md
```

---

# Matriz de Responsabilidades

```text
Responsibility                Authority

Express Intent                Command

Identify Target               ParticipationId

Identify Organization         OrganizationId

Identify Requesting Actor     ActorId

Determine Allowed Transition  State Machine

Determine Business Validity   Invariants

Determine Authorization       Permissions

Determine Concurrency         Versioning

Apply Behavior                Participation Aggregate

Represent Occurred Fact       Domain Event

Persist Aggregate             Repository

Expose Queries                Read Model

Publish External Fact         Integration Event

Record External Audit         Audit
```

---

# Regla de Separación de Responsabilidades

No debe trasladarse al Command responsabilidad perteneciente a:

```text
Aggregate

State Machine

Permissions

Invariants

Repository

Domain Events

Integration Events

Read Models

Infrastructure
```

El Command expresa intención y datos necesarios para evaluarla.

No toma la decisión final de dominio.

---

# No Setters mediante Commands

No deben definirse Commands genéricos como:

```text
SetParticipationStatus

SetParticipationVersion

SetParticipationOrganizationId

SetParticipationId
```

porque permitirían bypass de las reglas del Aggregate.

Los Commands deben expresar lenguaje del dominio.

---

# No Generic Update Command

No debe utilizarse:

```text
UpdateParticipation
```

como Command universal capaz de modificar cualquier atributo.

Los cambios relevantes deben expresarse mediante intención
explícita.

Ejemplos:

```text
ActivateParticipation

CompleteParticipation

WithdrawParticipation

InvalidateParticipation

ArchiveParticipation

ChangeParticipationType
```

Esto preserva el lenguaje ubicuo y evita modificaciones ambiguas.

---

# No DeleteParticipation

El modelo actual no define:

```text
DeleteParticipation
```

como Command del Lifecycle.

La finalización lógica se representa mediante los estados y
transiciones oficiales.

Debe mantenerse:

```text
ArchiveParticipation

≠

DeleteParticipation
```

---

# No ReactivateParticipation

La State Machine actual no define:

```text
ReactivateParticipation
```

No puede introducirse este Command sin evolucionar formalmente:

- Lifecycle;
- State Machine;
- Invariants;
- Permissions;
- Domain Events;
- Test Scenarios;
- Read Models;
- Integration Events cuando corresponda.

---

# No RestoreParticipation

El modelo actual tampoco define:

```text
RestoreParticipation
```

Archived permanece como estado terminal.

Una futura restauración requiere una evolución explícita del
dominio.

---

# No Commands Técnicos como Dominio

No deben incorporarse como Commands de dominio:

```text
SaveParticipation

PersistParticipation

SyncParticipation

RetryParticipation

SerializeParticipation

PublishParticipationToQueue

UpdateParticipationRow
```

Estas operaciones representan mecanismos técnicos.

No intenciones del lenguaje ubicuo de Participation.

---

# No Commands entre Aggregates

No debe existir un Command de Participation que intente modificar
simultáneamente:

```text
Participation

+

Assembly
```

o:

```text
Participation

+

Proposal
```

o:

```text
Participation

+

Voting
```

Cada Aggregate mantiene sus propios Commands y su propio límite de
consistencia.

---

# Causalidad entre Aggregates

Un hecho ocurrido en otro Aggregate puede originar una intención
sobre Participation mediante coordinación externa.

Ejemplo conceptual:

```text
External Domain Event

↓

Application Coordination

↓

Participation Command

↓

Participation Aggregate
```

La causalidad puede conservarse mediante:

```text
CorrelationId

CausationId
```

sin acoplar los Aggregates.

---

# Trazabilidad

Todo Command debe permitir reconstruir conceptualmente:

```text
Who

What

When

Target

Organization Context

Correlation

Causation

Expected Version
```

La trazabilidad no significa que Participation deba almacenar
internamente todo el historial de Commands.

Audit mantiene sus propias responsabilidades.

---

# Auditoría

Información de Command útil para Audit puede incluir:

```text
CommandId

CommandType

ParticipationId

OrganizationId

ActorId

Timestamp

CorrelationId

CausationId

ExpectedVersion

Outcome
```

El resultado puede representar:

```text
Accepted

Rejected
```

sin convertir Audit en parte del Aggregate Participation.

---

# Datos Sensibles

Los Commands deben transportar únicamente los datos necesarios para
ejecutar la intención.

No deben incluir por conveniencia:

- credenciales;
- contraseñas;
- tokens;
- JWT;
- claves privadas;
- secretos;
- sesiones;
- información externa irrelevante.

El Command debe minimizar su superficie de datos.

---

# Autenticación

Participation Commands no autentican actores.

La autenticación ocurre fuera del Aggregate.

El Command recibe:

```text
ActorId
```

como referencia del actor autenticado o contextualizado por las
capas correspondientes.

---

# Autorización

La autorización determina si el actor puede solicitar la operación.

El Aggregate mantiene separadas:

```text
Authorization

and

Domain Validity
```

Un actor autorizado todavía puede recibir rechazo cuando:

- el estado no permite la operación;
- una Invariant falla;
- existe conflicto de Version;
- el contexto no es válido.

---

# Regla de Actor Autorizado

Debe mantenerse:

```text
Authorized Actor

≠

Guaranteed Command Success
```

La autorización es necesaria cuando corresponda, pero no suficiente
para ejecutar una modificación.

---

# Regla de Estado Válido

Debe mantenerse:

```text
Valid State

≠

Guaranteed Command Success
```

También deben satisfacerse Permissions, Invariants y Versioning.

---

# Regla de Version Válida

Debe mantenerse:

```text
Valid Version

≠

Guaranteed Command Success
```

La coincidencia de Version no sustituye las demás validaciones.

---

# Resultado Conceptual

El procesamiento de un Command puede terminar conceptualmente en:

```text
Accepted
```

o:

```text
Rejected
```

Cuando es Accepted:

```text
Aggregate Modified

+

Version Incremented

+

Domain Event Registered
```

cuando la operación produzca una modificación válida.

Cuando es Rejected:

```text
Aggregate Unchanged

+

Version Unchanged

+

No Success Domain Event
```

---

# Errores de Dominio

Los motivos de rechazo deben representar conceptos del dominio y
deben poder distinguirse de fallos técnicos.

Ejemplos conceptuales:

```text
InvalidParticipationState

ParticipationInvariantViolation

ParticipationPermissionDenied

ParticipationVersionConflict

ParticipationOrganizationMismatch

ParticipationAlreadyExists

ParticipationNotFound
```

La representación técnica concreta pertenece a capas posteriores.

---

# Fallos Técnicos

Un fallo técnico no debe confundirse con rechazo del dominio.

Ejemplos:

```text
DatabaseUnavailable

NetworkFailure

MessageBrokerUnavailable
```

no representan por sí mismos:

```text
Domain Command Rejected
```

La arquitectura debe mantener esta separación conceptual.

---

# Reintentos

Un reintento técnico no constituye un nuevo comportamiento de
dominio por sí mismo.

Debe preservarse:

```text
CommandId

CorrelationId

CausationId
```

según corresponda para evitar duplicar modificaciones válidas.

La política técnica de reintento pertenece fuera del Aggregate.

---

# Replay

El replay de Domain Events no ejecuta nuevamente Commands.

Debe mantenerse:

```text
Event Replay

≠

Command Replay
```

La reconstrucción del Aggregate aplica hechos históricos.

No vuelve a solicitar las intenciones originales.

---

# Compatibilidad con DDD

Los Commands preservan Domain-Driven Design mediante:

- lenguaje ubicuo;
- intención explícita;
- comportamiento en la Aggregate Root;
- protección de invariantes;
- separación entre Aggregates;
- ausencia de setters genéricos;
- separación entre intención y hecho.

---

# Compatibilidad con CQRS

Los Commands constituyen el lado de escritura:

```text
Command Side

↓

Participation Aggregate

↓

Domain Events
```

Las consultas utilizan:

```text
Read Models
```

y no Commands.

---

# Compatibilidad con Event Sourcing

Los Commands pueden producir eventos que constituyan la historia
del Aggregate.

Debe mantenerse:

```text
Command

↓

Decision

↓

Domain Event
```

La historia se reconstruye desde Domain Events y no desde Commands.

---

# Compatibilidad con Event-Driven Architecture

Los Commands producen decisiones internas.

Los Domain Events resultantes pueden iniciar procesos posteriores.

Esto permite:

```text
Loose Coupling

+

Explicit Causality

+

Independent Aggregates
```

---

# Compatibilidad con Clean Architecture

Los Commands no dependen de detalles tecnológicos.

Pueden ser ejecutados desde distintos adaptadores sin alterar su
semántica.

---

# Compatibilidad con Arquitectura Distribuida

Cada Command mantiene un único Aggregate como frontera de
modificación.

No requiere transacciones distribuidas para modificar otros
Aggregates.

La coordinación externa utiliza eventos y Application Services
cuando corresponda.

---

# Principios Arquitectónicos

El modelo de Commands mantiene:

```text
Command

=

Intent
```

```text
Command

≠

Domain Event
```

```text
Command

≠

HTTP Request
```

```text
Command

≠

Database Operation
```

```text
Command

≠

Integration Event
```

```text
Command

≠

Audit Record
```

```text
Command

≠

Read Model Query
```

```text
Command

≠

Direct Setter
```

```text
Authorized Command

≠

Automatically Valid Command
```

```text
Valid Transition

≠

Automatically Authorized Command
```

```text
One Command

↓

One Aggregate Consistency Boundary
```

---

# Restricciones

No está permitido:

- modificar ParticipationId mediante un Command;
- modificar OrganizationId mediante un Command;
- modificar Version directamente;
- modificar ParticipationStatus directamente;
- ejecutar Commands sobre otro Aggregate desde Participation;
- utilizar Commands como Domain Events;
- utilizar Commands como Integration Events;
- utilizar Commands como operaciones directas de persistencia;
- ejecutar transiciones no definidas;
- ignorar Permissions;
- ignorar Invariants;
- ignorar Versioning;
- omitir la State Machine;
- ejecutar Commands operacionales sobre Archived;
- utilizar un Command genérico para modificar cualquier atributo;
- incorporar setters como lenguaje del dominio;
- introducir Commands técnicos como Commands de negocio;
- almacenar Aggregates externos dentro del Command;
- modificar otros Aggregates en la misma transacción;
- utilizar metadata para evadir Commands específicos;
- producir eventos de éxito ante Commands rechazados;
- incrementar Version ante Commands rechazados;
- modificar timestamps de Lifecycle ante Commands rechazados;
- persistir estados parciales;
- convertir un fallo técnico en una transición de dominio;
- asumir que Permission suficiente garantiza éxito;
- asumir que Version válida garantiza éxito;
- asumir que una transición existente garantiza éxito.

---

# Extension Points

El modelo de Commands puede evolucionar cuando aparezcan nuevas
intenciones reales del dominio.

Una extensión puede incorporar:

- nuevos Commands;
- nuevos datos específicos;
- nuevas causas de modificación;
- nuevos comportamientos no transicionales;
- Commands asociados a nuevas transiciones formalmente aprobadas.

Toda extensión debe respetar:

- lenguaje ubicuo;
- Aggregate Root;
- Lifecycle;
- State Machine;
- Invariants;
- Permissions;
- Versioning;
- Consistency Boundary;
- Domain Events;
- Integration Events;
- Test Scenarios;
- Security Model.

La definición de extensiones se documenta en:

```text
DOMAIN-008P-Extension-Points.md
```

---

# Regla de Evolución

Agregar un nuevo Command no significa automáticamente que exista un
nuevo comportamiento válido.

Debe existir coherencia entre:

```text
Command

↓

Domain Behavior

↓

Invariants

↓

Permissions

↓

State Machine when applicable

↓

Domain Event
```

Un Command sin semántica de dominio definida no debe incorporarse
al modelo oficial.

---

# Documentación Complementaria

Los Commands deben interpretarse conjuntamente con:

```text
DOMAIN-008-Aggregate.md

DOMAIN-008A-Lifecycle.md

DOMAIN-008B-State-Machine.md

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

Cada documento desarrolla una responsabilidad específica del
Aggregate sin alterar la semántica de intención definida en este
documento.

---

# Definición de Éxito

Los Commands del Aggregate **Participation** constituyen el modelo
oficial para expresar toda intención autorizada de modificación
sobre una Participation.

Los Commands transicionales:

```text
RegisterParticipation

ActivateParticipation

CompleteParticipation

WithdrawParticipation

InvalidateParticipation

ArchiveParticipation
```

controlan las intenciones relacionadas con el Lifecycle y deben
respetar estrictamente la State Machine oficial.

Los Commands no transicionales permiten expresar modificaciones
válidas del Aggregate sin alterar implícitamente
`ParticipationStatus`.

Cada Command:

- posee identidad;
- identifica la Participation objetivo;
- identifica su contexto organizacional;
- identifica al actor solicitante;
- mantiene trazabilidad;
- puede mantener correlación y causalidad;
- respeta ExpectedVersion cuando corresponde;
- se ejecuta exclusivamente mediante la Aggregate Root;
- respeta Permissions;
- respeta Invariants;
- respeta State Machine;
- modifica exclusivamente Participation;
- produce Domain Events únicamente después de una modificación
  válida;
- mantiene la consistencia del Aggregate.

Un Command rechazado:

```text
Does Not Modify Participation

Does Not Change Status

Does Not Increment Version

Does Not Modify Lifecycle Timestamps

Does Not Produce Success Domain Events
```

Los Commands no conocen Infrastructure, persistencia, protocolos,
frameworks ni mecanismos externos de integración.

De esta forma,
`DOMAIN-008C-Commands.md` constituye la definición normativa
oficial de las intenciones de modificación del Aggregate
**Participation**, preservando el lenguaje ubicuo, la consistencia
transaccional, la separación entre intención y hecho, la
independencia entre Aggregates y el patrón DDD consolidado de
AURA Core.