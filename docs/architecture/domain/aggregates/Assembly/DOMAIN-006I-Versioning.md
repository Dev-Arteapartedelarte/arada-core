# DOMAIN-006I — Assembly Versioning

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Assembly Management

Aggregate:
Assembly

Autor:
ARADA

Documentos relacionados:

* DOMAIN-006-Aggregate.md
* DOMAIN-006A-Lifecycle.md
* DOMAIN-006B-State-Machine.md
* DOMAIN-006C-Commands.md
* DOMAIN-006D-Domain-Events.md
* DOMAIN-006E-Invariants.md
* DOMAIN-006F-Permissions.md
* DOMAIN-006G-Repository-Contract.md
* DOMAIN-006H-Examples.md
* DOMAIN-006J-Consistency-Boundary.md
* DOMAIN-006K-Integration-Events.md
* DOMAIN-006L-Read-Model.md
* CORE-006-Domain-Invariants.md
* CORE-008-Aggregate-Design-Rules.md
* CORE-011-Repository-Contracts.md

---

# Objetivo

Definir las reglas de **Versioning** aplicables al Aggregate
**Assembly**.

El Versioning permite mantener una referencia explícita de la
evolución del estado del Aggregate y controlar modificaciones
concurrentes sobre una misma Assembly.

Toda modificación válida del Aggregate debe producir una nueva
versión.

El Repository debe utilizar la versión para detectar intentos de
persistencia realizados sobre un estado que ya ha sido modificado
por otro proceso.

---

# Propósito

El propósito del Versioning es proteger la consistencia del
Aggregate cuando múltiples procesos pueden intentar modificar una
misma Assembly.

Assembly mantiene:

```text
Version
```

como parte de su estado conceptual.

Version permite determinar si el estado utilizado para ejecutar
una operación continúa correspondiendo al estado actualmente
persistido.

De esta forma se evita que una modificación realizada sobre una
versión anterior del Aggregate sobrescriba silenciosamente una
modificación más reciente.

---

# Principio Fundamental

Toda Assembly mantiene una única versión actual.

Conceptualmente:

```text
Assembly
    │
    ├── AssemblyId
    ├── OrganizationId
    ├── AssemblyStatus
    └── Version
```

Version pertenece al Aggregate Assembly.

No pertenece:

* a Organization;
* a Territory;
* a Membership;
* a Citizen;
* a Proposal;
* a Participation;
* a Voting;
* a Document;
* a Notification;
* a Audit.

Cada Aggregate administra independientemente su propia evolución.

---

# Definición de Version

Version representa la revisión lógica actual del estado del
Aggregate Assembly.

Permite distinguir entre:

```text
AssemblyId
```

y:

```text
Version
```

AssemblyId identifica la Assembly.

Version identifica la evolución del estado de esa misma Assembly.

Debe mantenerse:

```text
AssemblyId
    ≠
Version
```

AssemblyId permanece inmutable durante toda la vida del
Aggregate.

Version cambia cuando el estado del Aggregate cambia válidamente.

---

# Estado Conceptual

Assembly mantiene conceptualmente:

```text
AssemblyId

OrganizationId

AssemblyStatus

Version
```

junto con los demás atributos definidos en:

```text
DOMAIN-006-Aggregate.md
```

Version forma parte de la información necesaria para preservar la
consistencia del Aggregate.

---

# Regla de Incremento

Toda modificación válida del estado de Assembly incrementa:

```text
Version
```

Debe mantenerse conceptualmente:

```text
CurrentVersion
    │
    ▼
Valid Domain Change
    │
    ▼
NextVersion
```

Una modificación válida implica que la operación:

* fue autorizada cuando correspondía;
* era válida para el estado actual;
* respetó la State Machine;
* respetó las invariantes;
* respetó los Guards;
* produjo un nuevo estado consistente;
* pudo ser confirmada como modificación del Aggregate.

---

# Cambio Válido

Se considera cambio válido toda operación aceptada por Assembly
que modifica su estado conceptual.

Ejemplos:

```text
ScheduleAssembly

RescheduleAssembly

ConvokeAssembly

RenameAssembly

ChangeAssemblyType

ChangeAssemblyPurpose

ChangeAssemblyDescription

ChangeAssemblyModality

ChangeAssemblyLocation

UpdateAssemblyConvocation

UpdateAssemblyRules

UpdateAssemblyExecutionConditions

StartAssembly

CompleteAssembly

CancelAssembly

ArchiveAssembly
```

Cuando cualquiera de estas operaciones produce una modificación
válida, Version debe avanzar.

---

# Cambio de Estado de Lifecycle

Una transición válida del Lifecycle modifica Version.

Ejemplo conceptual:

```text
Draft
    │
    ▼
Scheduled
```

produce una nueva versión del Aggregate.

También:

```text
Scheduled
    │
    ▼
Convoked
```

```text
Convoked
    │
    ▼
InProgress
```

```text
InProgress
    │
    ▼
Completed
```

```text
Completed
    │
    ▼
Archived
```

Cada transición constituye una modificación válida del Aggregate.

---

# Modificaciones sin Cambio de Estado

Version también debe incrementarse cuando una modificación válida
cambia información del Aggregate sin modificar AssemblyStatus.

Ejemplo:

```text
Scheduled
```

puede mantenerse como estado mientras ocurre:

```text
RescheduleAssembly
```

La Assembly continúa:

```text
Scheduled
```

pero su programación fue modificada.

Por lo tanto existe una nueva versión del Aggregate.

---

# Cambio de Nombre

Una operación válida:

```text
RenameAssembly
```

modifica:

```text
AssemblyName
```

aunque AssemblyStatus permanezca igual.

La modificación produce una nueva Version.

---

# Cambio de Propósito

Una operación válida:

```text
ChangeAssemblyPurpose
```

modifica el propósito formal de la reunión.

La modificación produce una nueva Version.

---

# Cambio de Descripción

Una modificación válida de:

```text
AssemblyDescription
```

produce una nueva Version cuando cambia efectivamente el estado
conceptual del Aggregate.

---

# Cambio de Tipo

Una modificación válida de:

```text
AssemblyType
```

produce una nueva Version.

El cambio debe continuar respetando las reglas definidas para el
estado actual de Assembly.

---

# Cambio de Modalidad

Una modificación válida de:

```text
AssemblyModality
```

produce una nueva Version.

La modificación debe preservar la coherencia con:

* AssemblyLocation;
* AssemblyRules;
* ExecutionConditions;
* Convocation;
* AssemblyStatus.

---

# Cambio de Ubicación

Una modificación válida de:

```text
AssemblyLocation
```

produce una nueva Version.

La ubicación forma parte del estado conceptual de Assembly cuando
corresponde.

---

# Cambio de Convocatoria

Una modificación válida de la información de convocatoria produce
una nueva Version.

Esto incluye modificaciones aceptadas sobre conceptos definidos
en el modelo de Convocation.

La operación debe preservar el carácter histórico de los hechos
que ya hayan ocurrido.

---

# Cambio de Reglas

Una modificación válida de:

```text
AssemblyRules
```

produce una nueva Version.

Las reglas modificadas deben continuar siendo compatibles con el
estado y las invariantes del Aggregate.

---

# Cambio de Condiciones de Realización

Una modificación válida de:

```text
ExecutionConditions
```

produce una nueva Version cuando dichas condiciones formen parte
del estado oficial del Aggregate.

---

# Operaciones Rechazadas

Una operación rechazada no modifica Version.

Debe mantenerse:

```text
Rejected Operation
    │
    ▼
Aggregate State Unchanged
    │
    ▼
Version Unchanged
```

Esto aplica cuando la operación es rechazada por:

* Permission insuficiente;
* estado inválido;
* transición inválida;
* Guard no satisfecho;
* invariante violada;
* datos inválidos;
* conflicto de concurrencia;
* condición de dominio no satisfecha.

---

# Permission Denied

Si un Actor no posee el Permission requerido:

```text
PermissionDenied
```

Assembly no debe modificarse.

Por lo tanto:

```text
Version
```

permanece sin cambios.

La ausencia de autorización no constituye una nueva versión del
Aggregate.

---

# Transición Inválida

Si una operación intenta una transición no permitida por:

```text
DOMAIN-006B-State-Machine.md
```

debe rechazarse.

Ejemplo:

```text
Draft
    │
    ✕
    ▼
InProgress
```

No se produce modificación.

Version permanece sin cambios.

---

# Invariante Violada

Si una operación viola una regla definida en:

```text
DOMAIN-006E-Invariants.md
```

la operación debe rechazarse.

No debe existir:

```text
partial state change
```

ni:

```text
Version increment
```

como consecuencia de una operación inválida.

---

# Guard no Satisfecho

Cuando un Guard impide una operación, Assembly conserva el estado
anterior.

Ejemplo:

```text
AssemblyStatus:
Convoked
```

pero:

```text
ExecutionConditionsSatisfied:
false
```

Un intento de:

```text
StartAssembly
```

debe ser rechazado.

Version permanece sin cambios.

---

# Lecturas

Las operaciones de lectura no modifican Version.

Ejemplos:

```text
get_by_id()

Assembly.Read

Assembly.List
```

Las lecturas consultan el estado.

No representan evolución del Aggregate.

---

# Read Model

Los Read Models definidos en:

```text
DOMAIN-006L-Read-Model.md
```

no modifican Assembly.Version.

El Read Model puede proyectar información derivada del Aggregate,
pero no constituye la fuente de verdad del Write Model.

---

# Rehidratación

Recuperar una Assembly desde persistencia no constituye una
modificación del dominio.

Por lo tanto la rehidratación debe preservar:

```text
Version
```

exactamente como fue persistida.

Debe mantenerse:

```text
Persisted Version
    =
Rehydrated Version
```

La recuperación del Aggregate no genera una nueva Version.

---

# Persistencia

AssemblyRepository debe preservar Version conforme al contrato
definido en:

```text
DOMAIN-006G-Repository-Contract.md
```

El Repository debe:

* recuperar la Version persistida;
* mantenerla durante rehidratación;
* utilizarla para control de concurrencia;
* persistir la nueva Version después de una modificación válida;
* impedir sobrescrituras silenciosas.

---

# Concurrencia Optimista

Assembly utiliza control de concurrencia optimista.

Conceptualmente:

```text
Load Assembly
    │
    ▼
Read Version
    │
    ▼
Execute Domain Behavior
    │
    ▼
Attempt Persistence
    │
    ▼
Validate Version
```

El Repository debe verificar que la versión utilizada para
realizar la modificación continúe correspondiendo a la versión
persistida.

---

# Versión Esperada

El proceso de modificación debe conservar la versión sobre la cual
se evaluó el Aggregate.

Conceptualmente:

```text
ExpectedVersion
```

representa la versión que el proceso espera encontrar al momento
de persistir.

Debe compararse con:

```text
PersistedVersion
```

---

# Comparación de Versiones

Debe cumplirse:

```text
ExpectedVersion
=
PersistedVersion
```

para confirmar una modificación.

Si ambas versiones coinciden, el Repository puede continuar con la
persistencia del nuevo estado válido.

Si no coinciden, existe un conflicto de concurrencia.

---

# Conflicto de Concurrencia

Debe producirse un conflicto cuando:

```text
ExpectedVersion
≠
PersistedVersion
```

El conflicto significa que la Assembly cambió desde que el
proceso obtuvo la versión utilizada para evaluar la operación.

La modificación no debe sobrescribir el estado persistido más
reciente.

---

# AssemblyConcurrencyConflict

El conflicto puede representarse conceptualmente mediante:

```text
AssemblyConcurrencyConflict
```

Este resultado indica que la modificación no puede confirmarse
sobre la versión esperada.

No representa:

* una transición de estado;
* un Domain Event de Assembly;
* una modificación válida;
* una nueva Version.

---

# Estado después de un Conflicto

Cuando ocurre un conflicto de concurrencia:

* el estado persistido no debe ser sobrescrito;
* la Version persistida no debe modificarse;
* no debe confirmarse el nuevo estado calculado sobre la versión
  anterior;
* no debe publicarse un Domain Event de éxito correspondiente a la
  operación rechazada.

---

# Ejemplo de Concurrencia

Dos procesos recuperan la misma Assembly:

```text
Process A

AssemblyId:
ASM-001

Version:
N
```

```text
Process B

AssemblyId:
ASM-001

Version:
N
```

Process A realiza una modificación válida.

La persistencia confirma una nueva versión:

```text
Version:
N + 1
```

Process B intenta persistir una modificación basada todavía en:

```text
ExpectedVersion:
N
```

pero actualmente existe:

```text
PersistedVersion:
N + 1
```

La persistencia debe ser rechazada.

---

# Lost Update

Versioning evita que ocurra:

```text
Process A modifies Assembly

Process B modifies old Assembly state

Process B overwrites Process A
```

sin detección.

Debe mantenerse:

```text
Stale Version
    │
    ▼
Persistence Rejected
```

---

# Last Write Wins

Assembly no puede utilizar una estrategia que permita que la
última escritura sobrescriba silenciosamente modificaciones
válidas anteriores.

La modificación debe respetar Version.

El Repository no debe convertir:

```text
latest received write
```

en autoridad suficiente para modificar Assembly.

---

# Reevaluación

Después de un conflicto de concurrencia, una futura nueva
ejecución debe considerar el estado actual del Aggregate.

Conceptualmente:

```text
AssemblyConcurrencyConflict
        │
        ▼
Reload Assembly
        │
        ▼
Evaluate Current State
        │
        ▼
Evaluate Domain Rules
```

La intención original no debe suponerse automáticamente válida
sobre el nuevo estado.

---

# State Machine y Concurrencia

La State Machine y Versioning protegen reglas distintas.

State Machine responde:

```text
¿La transición es válida desde este estado?
```

Versioning responde:

```text
¿El estado evaluado continúa siendo la versión actual?
```

Ambos controles deben cumplirse.

---

# Ejemplo — Start versus Cancel

Dos procesos recuperan:

```text
AssemblyStatus:
Convoked

Version:
N
```

Un proceso ejecuta válidamente:

```text
StartAssembly
```

y confirma:

```text
AssemblyStatus:
InProgress

Version:
N + 1
```

Otro proceso había intentado:

```text
CancelAssembly
```

sobre Version N.

Su persistencia debe ser rechazada por conflicto de concurrencia.

La operación no puede sobrescribir:

```text
InProgress
```

con un estado calculado sobre una realidad anterior.

---

# Ejemplo — Cancel versus Start

También puede ocurrir el caso inverso.

Un proceso confirma:

```text
Convoked
    │
    ▼
Cancelled
```

produciendo una nueva Version.

Otro proceso que había evaluado:

```text
StartAssembly
```

sobre la versión anterior debe ser rechazado.

Después de recuperar la nueva Assembly:

```text
AssemblyStatus:
Cancelled
```

StartAssembly ya no corresponde al estado actual.

---

# Ejemplo — Reschedule versus Convoke

Dos procesos recuperan:

```text
AssemblyStatus:
Scheduled

Version:
N
```

Uno ejecuta:

```text
ConvokeAssembly
```

y confirma una nueva Version.

El otro intenta:

```text
RescheduleAssembly
```

utilizando todavía la versión anterior.

Debe detectarse el conflicto antes de confirmar la modificación.

La operación deberá evaluarse nuevamente sobre el estado
actualizado.

---

# Ejemplo — Rename Concurrente

Dos procesos pueden intentar modificar:

```text
AssemblyName
```

sobre la misma Version.

Solo la primera modificación confirmada puede establecer la nueva
Version.

La segunda debe detectar que la versión utilizada ya no es la
actual.

---

# Ejemplo — Cambios Distintos sobre la Misma Assembly

Un proceso puede modificar:

```text
AssemblyDescription
```

mientras otro modifica:

```text
AssemblyPurpose
```

Aunque sean propiedades diferentes, ambas forman parte del mismo
Aggregate.

Por lo tanto ambas operaciones compiten sobre:

```text
Assembly.Version
```

La unidad de concurrencia es Assembly.

---

# Una Version por Aggregate

Assembly posee una única Version para proteger su Consistency
Boundary.

No se versionan de manera independiente conceptos internos como:

```text
AssemblySchedule

Convocation

AssemblyRules

ExecutionConditions

AssemblyLocation
```

cuando forman parte del mismo Aggregate.

La modificación de cualquiera de estos conceptos representa una
modificación de Assembly.

---

# Entidades Internas

Si Assembly contiene entidades internas legítimas, estas
permanecen bajo la misma Version del Aggregate Root.

Debe mantenerse:

```text
Assembly
    │
    ├── Internal Entity
    ├── Internal Value Object
    └── Version
```

No debe romperse el Aggregate creando mecanismos independientes de
concurrencia para sus partes internas.

---

# Otros Aggregates

Los Aggregates externos mantienen sus propias versiones cuando
corresponda.

Assembly.Version no controla:

```text
Organization.Version

Membership.Version

Proposal.Version

Participation.Version

Voting.Version

Document.Version
```

Cada Aggregate posee su propio límite de consistencia.

---

# Relaciones

Las referencias externas mantenidas por Assembly mediante
identificadores no comparten Version con Assembly.

Ejemplo:

```text
AssemblyId

OrganizationId

TerritoryId

ProposalId

VotingId

Version
```

Version pertenece únicamente a Assembly.

---

# Version y OrganizationId

Debe mantenerse:

```text
OrganizationId
    ≠
Version
```

OrganizationId define la Organization propietaria de Assembly.

Version representa la evolución lógica del Aggregate.

OrganizationId permanece inmutable.

Version evoluciona.

---

# Version y AssemblyStatus

Debe mantenerse:

```text
AssemblyStatus
    ≠
Version
```

AssemblyStatus representa el estado del Lifecycle.

Version representa la evolución completa del Aggregate.

Pueden existir múltiples versiones con el mismo AssemblyStatus.

Ejemplo conceptual:

```text
Scheduled
Version N
```

después de una reprogramación:

```text
Scheduled
Version N + 1
```

El estado permanece Scheduled.

El Aggregate cambió.

---

# Version y Timestamp

Version no representa una fecha ni un momento temporal.

Debe mantenerse:

```text
Version
    ≠
Timestamp
```

Los timestamps pertenecientes a Assembly mantienen su propia
semántica.

Ejemplos:

```text
CreatedAt

UpdatedAt

ConvokedAt

StartedAt

CompletedAt

CancelledAt

ArchivedAt
```

Version no reemplaza ninguno de ellos.

---

# Version y UpdatedAt

Debe mantenerse:

```text
Version
    ≠
UpdatedAt
```

Una modificación válida puede afectar ambos conceptos.

Sin embargo:

* Version representa evolución lógica;
* UpdatedAt representa información temporal.

No deben utilizarse como equivalentes.

---

# Version y Domain Events

Los Domain Events definidos en:

```text
DOMAIN-006D-Domain-Events.md
```

representan cambios válidos producidos por Assembly.

Los eventos pueden mantener:

```text
AggregateVersion
```

para identificar la versión resultante del Aggregate asociada al
hecho.

---

# AggregateVersion

AggregateVersion permite relacionar el Domain Event con la
evolución del Aggregate.

Conceptualmente:

```text
Assembly
Version:
N
```

ejecuta una modificación válida.

Después:

```text
Assembly
Version:
N + 1
```

y el evento correspondiente puede registrar:

```text
AggregateVersion:
N + 1
```

---

# Version y EventId

Debe mantenerse:

```text
Version
    ≠
EventId
```

EventId identifica un evento.

Version identifica una revisión del Aggregate.

Una Assembly puede producir múltiples Domain Events durante su
ciclo de vida.

---

# Version y CorrelationId

Debe mantenerse:

```text
Version
    ≠
CorrelationId
```

CorrelationId permite relacionar operaciones dentro de un flujo.

No identifica una revisión del Aggregate.

---

# Version y CausationId

Debe mantenerse:

```text
Version
    ≠
CausationId
```

CausationId representa una relación causal.

No representa la evolución del estado de Assembly.

---

# Version y Commands

Los Commands definidos en:

```text
DOMAIN-006C-Commands.md
```

representan intenciones de modificación.

Una operación de escritura puede requerir la versión esperada
correspondiente a la Assembly sobre la cual se evaluó la
intención.

El Command no determina arbitrariamente la nueva Version.

La nueva Version resulta de una modificación válida del
Aggregate.

---

# CommandId y Version

Debe mantenerse:

```text
CommandId
    ≠
Version
```

CommandId identifica una intención.

Version identifica la revisión del Aggregate.

Una misma Assembly puede recibir múltiples Commands durante su
vida.

---

# Version y Permissions

Los Permissions definidos en:

```text
DOMAIN-006F-Permissions.md
```

controlan quién puede intentar una operación.

Versioning controla si la operación se está confirmando sobre el
estado correcto.

Debe mantenerse:

```text
PermissionGranted
    ≠
VersionValid
```

Un Actor autorizado puede recibir un conflicto de concurrencia.

---

# Permission no Permite Ignorar Version

Ningún Permission puede autorizar:

```text
overwrite current Assembly
```

ignorando la Version persistida.

Esto aplica incluso a actores con capacidades administrativas.

La autorización no elimina las reglas de consistencia.

---

# Version y Invariants

Las invariantes definidas en:

```text
DOMAIN-006E-Invariants.md
```

deben cumplirse para toda versión válida de Assembly.

Debe mantenerse:

```text
Every Persisted Version
    │
    ▼
Valid Aggregate State
```

No debe existir una Version oficialmente persistida que represente
un estado que viole las invariantes del Aggregate.

---

# Version y Consistency Boundary

Version pertenece al límite definido en:

```text
DOMAIN-006J-Consistency-Boundary.md
```

La misma Version protege el conjunto de información que debe
mantenerse consistente dentro de Assembly.

No se utiliza para coordinar transaccionalmente otros Aggregates.

---

# Atomicidad

Cuando una modificación válida produce:

```text
New Assembly State
```

y:

```text
New Version
```

ambos deben confirmarse como una única modificación del Aggregate.

No debe existir:

```text
new state
```

con:

```text
old Version
```

ni:

```text
new Version
```

con:

```text
old state
```

como resultado persistido de una operación exitosa.

---

# Ejemplo — StartAssembly

Antes:

```text
AssemblyStatus:
Convoked

Version:
N
```

Una ejecución válida de:

```text
StartAssembly
```

produce conjuntamente:

```text
AssemblyStatus:
InProgress

StartedAt:
<timestamp>

Version:
NextVersion
```

Estos cambios pertenecen a una única modificación consistente.

---

# Ejemplo — CompleteAssembly

Antes:

```text
AssemblyStatus:
InProgress

Version:
N
```

Una ejecución válida de:

```text
CompleteAssembly
```

produce conjuntamente:

```text
AssemblyStatus:
Completed

CompletedAt:
<timestamp>

Version:
NextVersion
```

---

# Ejemplo — CancelAssembly

Antes:

```text
AssemblyStatus:
Scheduled

Version:
N
```

Una cancelación válida produce:

```text
AssemblyStatus:
Cancelled

CancelledAt:
<timestamp>

Version:
NextVersion
```

---

# Ejemplo — ArchiveAssembly

Antes:

```text
AssemblyStatus:
Completed

Version:
N
```

Una operación válida:

```text
ArchiveAssembly
```

produce:

```text
AssemblyStatus:
Archived

ArchivedAt:
<timestamp>

Version:
NextVersion
```

---

# Archived

Archived constituye un estado terminal del Lifecycle definido para
Assembly.

Una Assembly archivada no admite modificaciones ordinarias.

Por lo tanto una lectura de una Assembly Archived conserva su
Version.

No se incrementa Version por el solo hecho de recuperar o
consultar una Assembly archivada.

---

# Cancelled

Cancelled representa una Assembly cuyo flujo normal fue
interrumpido antes de InProgress conforme al modelo actual.

La transición hacia Cancelled constituye una modificación válida y
por lo tanto produce una nueva Version.

Las consultas posteriores no modifican esa Version.

---

# Repository Contract

AssemblyRepository debe utilizar Version para proteger la
persistencia.

Conceptualmente:

```text
save(
    assembly,
    expected_version
)
```

debe verificar que la versión esperada corresponda a la versión
persistida antes de confirmar el nuevo estado.

---

# Persistencia Condicional

La persistencia debe comportarse conceptualmente como:

```text
AssemblyId matches
AND
PersistedVersion matches ExpectedVersion
```

antes de confirmar la modificación.

La tecnología utilizada para implementar esta regla pertenece a
Infrastructure.

La regla conceptual pertenece al contrato de Versioning.

---

# Infrastructure

Versioning no depende de una tecnología específica.

Assembly no conoce:

* PostgreSQL;
* MongoDB;
* MySQL;
* SQLite;
* ORM;
* Event Store;
* HTTP;
* REST;
* GraphQL.

Infrastructure debe implementar el contrato sin modificar su
semántica.

---

# Persistencia Relacional

Una base de datos relacional puede implementar el control de
Version mediante mecanismos técnicos propios.

Esto no convierte esos mecanismos en parte del dominio.

El concepto oficial continúa siendo:

```text
ExpectedVersion
```

comparada con:

```text
PersistedVersion
```

---

# Persistencia Documental

Una base de datos documental puede implementar una actualización
condicionada por Version.

La estrategia concreta no modifica el modelo conceptual.

---

# Event Sourcing Compatible

Assembly es compatible con Event Sourcing conforme a las reglas
arquitectónicas generales de AURA.

Cuando se utilice Event Sourcing, Version debe continuar
representando la evolución del Aggregate.

La estrategia concreta de reconstrucción y persistencia pertenece
a la implementación adoptada.

Este documento no redefine la arquitectura de persistencia.

---

# Domain Events y Persistencia

La arquitectura debe mantener coherencia entre:

```text
Persisted Assembly State
```

y:

```text
Domain Events
```

producidos por esa modificación.

Un evento de éxito no debe representar como confirmado un cambio
que finalmente no fue persistido.

La estrategia técnica para garantizar esta consistencia pertenece
a Infrastructure y a los patrones establecidos por AURA.

---

# Version y Integration Events

Los Integration Events definidos en:

```text
DOMAIN-006K-Integration-Events.md
```

pueden transportar información asociada a la versión del Aggregate
cuando el contrato correspondiente así lo defina.

Integration Events no modifican Assembly.Version.

---

# Version y Read Model

Los Read Models pueden proyectar Version si resulta necesario para
trazabilidad o consistencia de lectura.

Pero el Read Model no modifica la Version del Write Model.

Debe mantenerse:

```text
Read Model
    ≠
Authority over Assembly Version
```

---

# Consistencia Eventual del Read Model

Puede existir temporalmente una diferencia entre:

```text
Write Model Version
```

y:

```text
Projected Version
```

cuando el Read Model todavía no ha procesado el último cambio.

Esto pertenece a la consistencia eventual de la proyección.

No significa que Assembly posea múltiples versiones oficiales
simultáneamente.

---

# Fuente de Verdad

La fuente oficial del estado de escritura continúa siendo el
Aggregate Assembly y su persistencia conforme al Repository
Contract.

Una proyección retrasada no puede utilizarse para sobrescribir el
estado actual del Aggregate.

---

# Independencia entre Assemblies

Cada Assembly posee su propia Version.

Ejemplo conceptual:

```text
ASM-001
Version:
N
```

y:

```text
ASM-002
Version:
M
```

pueden evolucionar independientemente.

No existe necesidad de compartir Version entre Assemblies
distintas.

---

# Concurrencia entre Aggregates Diferentes

Una modificación sobre:

```text
ASM-001
```

no genera un conflicto de Version con:

```text
ASM-002
```

Version se interpreta siempre dentro de la identidad del
Aggregate correspondiente.

---

# Identidad Compuesta Conceptual

Para control de concurrencia debe considerarse conceptualmente:

```text
AssemblyId

ExpectedVersion
```

No solo Version.

Dos Assemblies diferentes pueden encontrarse en una misma Version
sin representar el mismo estado ni el mismo Aggregate.

---

# Integraciones Externas

Los sistemas externos no administran Assembly.Version.

Una integración externa puede originar una intención que termine
en un Command válido.

El flujo continúa siendo:

```text
External System
      │
      ▼
Integration / Anti-Corruption Layer
      │
      ▼
Application Layer
      │
      ▼
Assembly Command
      │
      ▼
Assembly
      │
      ▼
Version Validation
```

El sistema externo no modifica Version directamente.

---

# FIWARE

Una integración con FIWARE no convierte la versión de una entidad
externa en la Version oficial de Assembly.

Assembly.Version continúa perteneciendo al Aggregate AURA.

Cualquier relación entre versiones externas y Version del
Aggregate deberá definirse explícitamente en el contrato de
integración correspondiente.

---

# API

Una API puede transportar información relacionada con Version.

La representación técnica no forma parte de este documento.

La API no redefine:

```text
Version
```

ni:

```text
ExpectedVersion
```

como conceptos del dominio.

---

# Aplicación

La Application Layer coordina la operación.

Conceptualmente:

```text
Command
    │
    ▼
Load Assembly
    │
    ▼
Obtain Current Version
    │
    ▼
Execute Domain Behavior
    │
    ▼
Persist using ExpectedVersion
```

Application coordina.

Assembly protege sus reglas.

Repository protege la persistencia concurrente.

---

# Repository

El Repository no decide:

* Permissions;
* Lifecycle;
* State Machine;
* Guards;
* invariantes funcionales.

Su responsabilidad respecto de Versioning es garantizar que una
modificación no sobrescriba silenciosamente un estado basado en
otra Version.

---

# Retry

Un conflicto de concurrencia indica que el estado utilizado para
tomar la decisión ya no es el estado actual.

Por lo tanto una nueva ejecución debe considerar nuevamente la
Assembly actual.

Versioning no autoriza a confirmar automáticamente la intención
original sobre un estado distinto.

---

# Trazabilidad

Version permite establecer una secuencia lógica de modificaciones
confirmadas sobre una Assembly.

Conceptualmente:

```text
AssemblyId
    │
    ├── Version
    ├── Domain Events
    └── timestamps
```

contribuyen a mantener trazabilidad.

Cada concepto conserva su propia responsabilidad.

---

# Auditoría

Audit puede utilizar Version como referencia de trazabilidad.

Assembly no absorbe Audit dentro de su Aggregate.

Un registro de Audit puede relacionarse con:

```text
AssemblyId

Version

ActorId

CommandId

Timestamp
```

cuando las reglas de Audit lo requieran.

---

# Version no es Audit

Debe mantenerse:

```text
Version
    ≠
Audit History
```

Version indica la revisión lógica del Aggregate.

Audit puede contener información adicional sobre quién, cuándo y
bajo qué contexto ocurrió una operación.

---

# No Modificación Directa

Version no puede modificarse mediante setters públicos.

No debe existir:

```text
setVersion()
```

como comportamiento público del Aggregate.

Version cambia exclusivamente como consecuencia del procesamiento
de una modificación válida.

---

# No Command de Version

No debe existir:

```text
SetAssemblyVersion
```

como Command funcional del dominio.

Version no representa una propiedad libremente editable.

---

# No Permission de Version

No debe existir:

```text
Assembly.ChangeVersion
```

como Permission de negocio.

Ningún Actor modifica Version directamente.

---

# No Cambio Autónomo del Repository

Repository tampoco debe cambiar Version arbitrariamente sin que
exista una modificación válida del Aggregate.

Debe persistir la evolución determinada por el modelo de
Assembly.

---

# Version y Migraciones Técnicas

Una modificación exclusivamente técnica de la infraestructura no
representa automáticamente una modificación funcional de
Assembly.

El Versioning del Aggregate no debe confundirse con:

* migraciones de base de datos;
* cambios de esquema;
* cambios de ORM;
* cambios de framework;
* despliegues de software.

---

# Version del Documento

La cabecera:

```text
Versión: 1.0
```

de este documento no corresponde a:

```text
Assembly.Version
```

Debe mantenerse:

```text
Document Version
    ≠
Aggregate Version
```

La primera controla la evolución documental.

La segunda controla la evolución de una instancia del Aggregate.

---

# Version del Software

La versión de AURA Core tampoco corresponde a Assembly.Version.

Debe mantenerse:

```text
Software Version
    ≠
Assembly Version
```

Actualizar AURA Core no incrementa automáticamente Version de las
Assemblies persistidas.

---

# Version de API

La versión de una API no corresponde a Assembly.Version.

Ejemplo:

```text
API v1
```

puede operar sobre Assemblies con múltiples Versions.

Los conceptos son independientes.

---

# Reglas de Versioning

Siempre deben cumplirse las siguientes reglas:

* toda Assembly mantiene Version;
* Version pertenece a una única Assembly;
* Version no reemplaza AssemblyId;
* Version cambia únicamente como consecuencia de una modificación
  válida del Aggregate;
* toda modificación válida incrementa Version;
* una operación rechazada no modifica Version;
* una lectura no modifica Version;
* una rehidratación no modifica Version;
* Repository preserva Version;
* Repository valida concurrencia antes de confirmar una
  modificación;
* una versión obsoleta no puede sobrescribir silenciosamente una
  versión más reciente;
* un conflicto de concurrencia no produce una modificación válida;
* un conflicto de concurrencia no produce un Domain Event de éxito;
* Version protege el Consistency Boundary de Assembly;
* otros Aggregates mantienen su propio Versioning;
* Version no puede modificarse directamente por Actors;
* Version no puede modificarse directamente por sistemas externos.

---

# Reglas de Consistencia

Versioning debe preservar:

```text
Assembly State

Assembly Version
```

como parte de la misma modificación consistente.

No debe existir una persistencia parcial en la cual el estado
cambie pero Version no refleje la modificación correspondiente.

Tampoco debe existir una nueva Version confirmada sin el estado
correspondiente.

---

# Reglas de Concurrencia

Debe mantenerse:

```text
ExpectedVersion
=
PersistedVersion
```

antes de confirmar una modificación.

Cuando:

```text
ExpectedVersion
≠
PersistedVersion
```

la modificación debe ser rechazada.

El estado persistido más reciente conserva autoridad.

---

# Reglas de Rechazo

El rechazo por concurrencia debe:

* mantener la Assembly persistida sin cambios;
* mantener su Version actual;
* evitar sobrescritura;
* evitar persistencia parcial;
* evitar Domain Events de éxito correspondientes a la operación no
  confirmada.

---

# Casos de Uso Conceptuales

Versioning protege operaciones como:

```text
Programar una Assembly.

Reprogramar una Assembly.

Convocar una Assembly.

Cambiar su nombre.

Cambiar su propósito.

Cambiar su descripción.

Cambiar su tipo.

Cambiar su modalidad.

Cambiar su ubicación.

Actualizar su convocatoria.

Actualizar sus reglas.

Actualizar sus condiciones de realización.

Iniciar una Assembly.

Finalizar una Assembly.

Cancelar una Assembly.

Archivar una Assembly.
```

Toda modificación debe realizarse sobre la versión actual del
Aggregate.

---

# Ejemplo Conceptual Completo

Estado recuperado:

```text
AssemblyId:
ASM-001

AssemblyStatus:
Convoked

Version:
N
```

Un Actor autorizado solicita:

```text
StartAssembly
```

Assembly valida:

```text
Permission

State Machine

Guards

Invariants
```

El comportamiento produce un nuevo estado válido:

```text
AssemblyStatus:
InProgress
```

y una nueva Version.

Antes de confirmar, Repository verifica que:

```text
ExpectedVersion:
N
```

continúe coincidiendo con la Version persistida.

Si coincide, la nueva modificación puede persistirse.

Si no coincide, la operación debe ser rechazada por conflicto de
concurrencia.

---

# Ejemplo Conceptual de Conflicto

Estado inicial:

```text
AssemblyStatus:
Convoked

Version:
N
```

Dos operaciones se evalúan sobre la misma Version.

Primera operación:

```text
StartAssembly
```

se confirma.

La Assembly cambia a:

```text
AssemblyStatus:
InProgress

Version:
NextVersion
```

La segunda operación intenta persistir utilizando todavía:

```text
ExpectedVersion:
N
```

Debe rechazarse.

La segunda operación no puede devolver la Assembly a un estado
calculado sobre la versión anterior.

---

# Test de Incremento

Escenario conceptual:

```text
Given Assembly Version = N

When valid modification occurs

Then Assembly Version changes
```

La modificación debe representar un cambio real del estado del
Aggregate.

---

# Test de Rechazo

```text
Given Assembly Version = N

When invalid Command is rejected

Then Assembly Version remains N
```

---

# Test de Lectura

```text
Given Assembly Version = N

When Assembly is read

Then Assembly Version remains N
```

---

# Test de Rehidratación

```text
Given persisted Assembly Version = N

When Assembly is rehydrated

Then Assembly Version = N
```

---

# Test de Concurrencia

```text
Given PersistedVersion differs from ExpectedVersion

When persistence is attempted

Then AssemblyConcurrencyConflict
```

---

# Test de Lost Update

Dos procesos basados en la misma Version no pueden confirmar
modificaciones incompatibles sobrescribiéndose silenciosamente.

---

# Test de Permission Denied

```text
Given Version = N

And Actor lacks required Permission

When Command is attempted

Then Version remains N
```

---

# Test de Invariante

```text
Given Version = N

When Command violates an invariant

Then Version remains N
```

---

# Test de State Machine

```text
Given Version = N

When Command requests invalid transition

Then Version remains N
```

---

# Test de Archived

```text
Given AssemblyStatus = Archived

And Version = N

When ordinary modification is attempted

Then operation is rejected

And Version remains N
```

---

# Test de Read Model

Una actualización de una proyección no modifica Assembly.Version.

---

# Test de Repository

Toda implementación de AssemblyRepository debe demostrar que una
escritura basada en una Version obsoleta es rechazada.

---

# Relación con DOMAIN-006-Aggregate

`DOMAIN-006-Aggregate.md` establece:

```text
Version
```

como parte del estado conceptual de Assembly.

Este documento desarrolla exclusivamente las reglas asociadas a
esa Version.

No redefine la identidad ni el Lifecycle del Aggregate.

---

# Relación con Lifecycle

`DOMAIN-006A-Lifecycle.md` define la evolución de estados de
Assembly.

Cada transición válida representa una modificación del Aggregate
y debe reflejarse en Version.

Version no sustituye el Lifecycle.

---

# Relación con State Machine

`DOMAIN-006B-State-Machine.md` determina las transiciones válidas.

Versioning impide confirmar una transición calculada sobre una
versión obsoleta.

Ambas reglas deben cumplirse conjuntamente.

---

# Relación con Commands

`DOMAIN-006C-Commands.md` define las intenciones de modificación.

Versioning protege la ejecución concurrente de esas intenciones.

Un Command puede ser válido conceptualmente y aun así no poder
confirmarse si la Assembly fue modificada desde que fue cargada.

---

# Relación con Domain Events

`DOMAIN-006D-Domain-Events.md` define los hechos del Aggregate.

Los eventos producidos por modificaciones válidas pueden
referenciar AggregateVersion.

Un evento de éxito corresponde siempre a una modificación válida
del Aggregate.

---

# Relación con Invariants

`DOMAIN-006E-Invariants.md` define las reglas que siempre deben
cumplirse.

Versioning protege estas reglas frente a sobrescrituras
concurrentes basadas en estados anteriores.

---

# Relación con Permissions

`DOMAIN-006F-Permissions.md` determina quién puede solicitar cada
operación.

Permissions no sustituyen Versioning.

Versioning no sustituye Permissions.

---

# Relación con Repository Contract

`DOMAIN-006G-Repository-Contract.md` define el mecanismo
conceptual de persistencia.

Repository debe preservar Version y aplicar el control de
concurrencia correspondiente.

---

# Relación con Examples

`DOMAIN-006H-Examples.md` contiene ejemplos conceptuales de
operaciones concurrentes y evolución del Aggregate.

Los ejemplos deben permanecer coherentes con este documento.

---

# Relación con Consistency Boundary

`DOMAIN-006J-Consistency-Boundary.md` define el límite de
consistencia de Assembly.

Version protege ese límite frente a modificaciones concurrentes.

No extiende la consistencia hacia otros Aggregates.

---

# Relación con Integration Events

`DOMAIN-006K-Integration-Events.md` define los contratos utilizados
para interoperabilidad.

Integration Events no administran Assembly.Version.

Cuando transporten AggregateVersion, este valor representa la
Version del Aggregate que originó el hecho.

---

# Relación con Read Model

`DOMAIN-006L-Read-Model.md` define las proyecciones de lectura.

Read Models pueden exponer Version cuando sea útil, pero no
controlan la evolución del Write Model.

---

# Restricciones

No está permitido:

* modificar Version directamente;
* exponer un setter público de Version;
* crear un Command para cambiar Version;
* crear un Permission para cambiar Version;
* utilizar Version como AssemblyId;
* utilizar Version como OrganizationId;
* utilizar Version como Timestamp;
* utilizar Version como EventId;
* incrementar Version por una lectura;
* incrementar Version por una rehidratación;
* incrementar Version después de una operación rechazada;
* confirmar una modificación con una Version obsoleta;
* sobrescribir silenciosamente una Version más reciente;
* permitir que Permissions ignoren Versioning;
* permitir que Repository ignore Versioning;
* permitir que una integración externa cambie Version
  directamente;
* compartir Assembly.Version con otros Aggregates;
* utilizar Assembly.Version como mecanismo de transacción
  distribuida;
* modificar entidades internas fuera del control de
  Assembly.Version;
* permitir que una optimización técnica rompa las reglas de
  concurrencia;
* confundir Version del Aggregate con versiones de documentos,
  software, APIs o contratos externos.

---

# Compatibilidad Arquitectónica

El modelo de Versioning de Assembly es compatible con:

* Domain-Driven Design;
* Aggregate Pattern;
* Repository Pattern;
* Clean Architecture;
* Hexagonal Architecture;
* CQRS;
* Event-Driven Architecture;
* Event Sourcing Compatible;
* Optimistic Concurrency;
* sistemas distribuidos.

La implementación concreta permanece separada del dominio.

---

# Principios Arquitectónicos

Versioning mantiene:

```text
AssemblyId
    ≠
Version
```

```text
AssemblyStatus
    ≠
Version
```

```text
Timestamp
    ≠
Version
```

```text
CommandId
    ≠
Version
```

```text
EventId
    ≠
Version
```

```text
Permission
    ≠
Version
```

```text
Read
    ≠
Domain Change
```

```text
Rehydration
    ≠
Domain Change
```

```text
Permission Granted
    ≠
Concurrency Valid
```

```text
Valid State Transition
    ≠
Valid Concurrent Persistence
```

Estas separaciones preservan la responsabilidad específica de
Versioning dentro del Aggregate.

---

# Reglas de Diseño

El modelo debe garantizar:

* una única Version por Aggregate Assembly;
* evolución controlada de Version;
* incremento ante modificaciones válidas;
* ausencia de incremento ante rechazos;
* ausencia de incremento ante lecturas;
* preservación durante rehidratación;
* validación de concurrencia antes de persistir;
* rechazo de versiones obsoletas;
* prevención de lost updates;
* atomicidad entre estado y Version;
* independencia entre Aggregates;
* independencia tecnológica;
* compatibilidad con Repository Contract;
* compatibilidad con Domain Events;
* compatibilidad con CQRS;
* compatibilidad con Event-Driven Architecture.

---

# Definición de Éxito

El modelo de **Versioning** del Aggregate **Assembly** garantiza
que toda modificación válida de una Assembly produzca una nueva
revisión lógica de su estado y que ninguna modificación basada en
una versión anterior pueda sobrescribir silenciosamente cambios
más recientes.

Version pertenece exclusivamente al Aggregate Assembly y evoluciona
junto con su estado.

AssemblyId permanece como identidad inmutable del Aggregate,
mientras Version representa su evolución.

Toda operación válida que modifica el estado conceptual de
Assembly debe incrementar Version.

Toda operación rechazada, lectura o rehidratación mantiene Version
sin cambios.

El Repository utiliza la versión esperada para comprobar que la
Assembly no haya sido modificada concurrentemente antes de
confirmar una nueva persistencia.

Cuando la versión utilizada por una operación no coincide con la
versión actualmente persistida, la modificación debe ser
rechazada mediante un conflicto de concurrencia y no debe producir
una actualización parcial ni un Domain Event de éxito.

Versioning no reemplaza:

* Permissions;
* State Machine;
* Guards;
* invariantes;
* Repository Contract;
* Consistency Boundary.

Cada uno protege una dimensión distinta del Aggregate.

Versioning tampoco coordina la consistencia de otros Aggregates.
Organization, Membership, Territory, Proposal, Participation,
Voting, Document, Notification y Audit mantienen sus propios
límites y su propia evolución.

De esta forma, **DOMAIN-006I-Versioning.md** establece el contrato
conceptual oficial para controlar la evolución y concurrencia del
Aggregate Assembly, preservando consistencia, trazabilidad,
aislamiento entre Aggregates y los límites definidos por la
arquitectura Domain-Driven Design de AURA Core.
