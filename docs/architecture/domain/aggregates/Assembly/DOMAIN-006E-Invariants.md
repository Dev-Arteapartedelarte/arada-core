# DOMAIN-006E — Assembly Invariants

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
* DOMAIN-006F-Permissions.md
* DOMAIN-006G-Repository-Contract.md
* DOMAIN-006I-Versioning.md
* DOMAIN-006J-Consistency-Boundary.md
* DOMAIN-006K-Integration-Events.md
* DOMAIN-006L-Read-Model.md
* DOMAIN-006M-Test-Scenarios.md
* DOMAIN-006O-Security-Model.md
* CORE-006-Domain-Invariants.md
* CORE-008-Aggregate-Design-Rules.md
* CORE-011-Repository-Contracts.md

---

# Objetivo

Definir formalmente las **invariantes** que protegen la
consistencia del Aggregate **Assembly**.

Una invariante representa una condición del dominio que debe
permanecer verdadera en todo estado válido del Aggregate.

Assembly nunca puede aceptar una operación que produzca un estado
que viole alguna de sus invariantes.

Las invariantes constituyen reglas internas y normativas del
Aggregate y deben ser protegidas por la Aggregate Root
independientemente de:

* Application Services;
* Command Handlers;
* Controllers;
* APIs;
* persistencia;
* interfaces de usuario;
* sistemas externos;
* infraestructura.

Las validaciones ejecutadas fuera del Aggregate pueden anticipar
errores o mejorar la experiencia de uso, pero nunca sustituyen las
reglas que Assembly debe proteger por sí misma.

---

# Propósito

Las invariantes garantizan que toda instancia de Assembly
permanezca conceptualmente válida durante todo su ciclo de vida.

Protegen:

* identidad;
* propiedad organizacional;
* contexto territorial;
* clasificación;
* nombre;
* propósito;
* descripción;
* estado;
* programación;
* modalidad;
* ubicación;
* convocatoria;
* reglas propias;
* condiciones de realización;
* timestamps;
* ciclo de vida;
* versionado;
* referencias externas;
* límites del Aggregate;
* consistencia interna;
* historicidad;
* publicación de Domain Events.

Las invariantes no representan permisos.

Las invariantes determinan:

```text
si una operación puede producir un estado válido del dominio
```

Los permisos determinan:

```text
si un Actor está autorizado a solicitar una operación
```

Ambos conceptos deben permanecer separados.

---

# Principio Fundamental

Una Assembly válida debe satisfacer todas las invariantes
aplicables a su estado actual.

Conceptualmente:

```text
ValidAssembly =
    IdentityInvariant
    AND OrganizationInvariant
    AND ClassificationInvariant
    AND StateInvariant
    AND TemporalInvariant
    AND LifecycleInvariant
    AND ConsistencyInvariant
```

Una operación que produzca:

```text
ValidAssembly = false
```

debe ser rechazada.

No existe autorización, integración, privilegio técnico ni
mecanismo de persistencia que permita legítimamente mantener una
Assembly en un estado inválido.

---

# Autoridad de las Invariantes

La Aggregate Root:

```text
Assembly
```

constituye la autoridad final para proteger las invariantes
internas del Aggregate.

Las validaciones realizadas previamente por:

* Application Services;
* Command Handlers;
* APIs;
* interfaces gráficas;
* adapters;
* servicios externos;
* mecanismos de integración;

pueden anticipar errores, pero nunca sustituyen las validaciones
propias del dominio.

---

# Momento de Validación

Las invariantes deben encontrarse satisfechas antes y después de
toda modificación válida.

Conceptualmente:

```text
Command
    │
    ▼
Validate Preconditions
    │
    ▼
Validate Current State
    │
    ▼
Execute Domain Behavior
    │
    ▼
Validate Resulting State
    │
    ▼
Record Domain Event
```

Si alguna condición necesaria falla:

```text
Reject Command
```

El Aggregate permanece sin modificaciones.

---

# Estado Válido antes de una Operación

Assembly no debe ejecutar comportamiento ordinario partiendo de
un estado internamente inconsistente.

Ejemplo:

```text
AssemblyStatus = InProgress

StartedAt = null
```

representa una violación de invariantes.

La operación siguiente no debe normalizar silenciosamente ese
estado.

---

# Estado Válido después de una Operación

Toda operación aceptada debe producir un estado completo y
consistente.

Ejemplo:

```text
StartAssembly
```

no puede producir solamente:

```text
AssemblyStatus = InProgress
```

Debe mantener simultáneamente:

```text
AssemblyStatus = InProgress

StartedAt != null

Version = PreviousVersion + 1
```

y registrar:

```text
AssemblyStarted
```

---

# Invariantes versus Precondiciones

Una precondición determina si una operación concreta puede
ejecutarse.

Una invariante determina si el Aggregate puede existir
válidamente en un estado determinado.

Ejemplo:

```text
AssemblyStatus = Convoked
```

es precondición de:

```text
StartAssembly
```

Mientras:

```text
CompletedAt >= StartedAt
```

es una invariante temporal cuando ambos timestamps existen.

---

# Invariantes versus Guards

Los Guards definidos por la State Machine protegen transiciones
específicas.

Ejemplo:

```text
CanStartAssembly
```

puede requerir:

```text
Status == Convoked

ConvocationValid == true

ScheduleValid == true

ExecutionConditionsSatisfied == true
```

Un Guard no sustituye una invariante.

Una invariante tampoco sustituye la definición explícita de una
transición.

---

# Invariantes versus Permisos

La autorización responde:

```text
¿Puede este Actor intentar ejecutar esta operación?
```

Las invariantes responden:

```text
¿Puede esta operación producir un estado válido del Aggregate?
```

Poseer un permiso nunca permite violar una invariante.

---

# Invariantes versus Políticas Configurables

Assembly puede poseer:

```text
AssemblyRules
```

y:

```text
ExecutionConditions
```

configurables.

Estas reglas no pueden anular invariantes estructurales.

Por ejemplo, ninguna configuración puede permitir:

```text
Archived -> InProgress
```

---

# Clasificación de Invariantes

Las invariantes de Assembly se clasifican conceptualmente en:

```text
Identity Invariants

Ownership Invariants

Territorial Invariants

Classification Invariants

Descriptive Invariants

State Invariants

Lifecycle Invariants

Temporal Invariants

Scheduling Invariants

Modality Invariants

Location Invariants

Convocation Invariants

Assembly Rules Invariants

Execution Invariants

Closure Invariants

Cancellation Invariants

Archival Invariants

Reference Invariants

Versioning Invariants

Consistency Boundary Invariants

Domain Event Invariants

Historical Invariants

Security Boundary Invariants

Technology Independence Invariants
```

Esta clasificación organiza las reglas.

No crea nuevos límites de consistencia.

---

# Invariante de Identidad

Toda Assembly debe poseer:

```text
AssemblyId
```

válido.

AssemblyId:

* es obligatorio;
* es único;
* es inmutable;
* identifica permanentemente al Aggregate;
* no depende de atributos descriptivos;
* no depende de AssemblyStatus;
* no depende de persistencia;
* no puede reutilizarse.

---

# Inmutabilidad de AssemblyId

Debe mantenerse:

```text
AssemblyId(t0) = AssemblyId(t1)
```

durante toda la existencia del Aggregate.

No existe:

```text
ChangeAssemblyId
```

---

# Unicidad de AssemblyId

Dos Assemblies diferentes deben poseer identidades diferentes.

Conceptualmente:

```text
AssemblyA.AssemblyId != AssemblyB.AssemblyId
```

cuando representan reuniones distintas.

---

# No Reutilización de Identidad

AssemblyId no puede reutilizarse después de:

```text
Cancelled

Archived
```

El archivado no libera identidad.

---

# Identidad no Derivada

AssemblyId no debe derivarse de:

```text
AssemblyName

OrganizationId

ScheduledStartAt

AssemblyType

AssemblyStatus
```

La identidad permanece independiente del contenido mutable.

---

# Invariante de Organization

Toda Assembly pertenece exactamente a una:

```text
Organization
```

mediante:

```text
OrganizationId
```

No existe una Assembly válida sin Organization propietaria.

---

# Inmutabilidad de OrganizationId

Debe mantenerse:

```text
Assembly.OrganizationId(t0)
=
Assembly.OrganizationId(t1)
```

durante toda la vida del Aggregate.

No existe:

```text
TransferAssemblyToOrganization
```

en la versión 1.0.

---

# Propiedad Organizacional

Una Assembly creada para:

```text
Organization A
```

no puede transformarse mediante modificación ordinaria en una
Assembly de:

```text
Organization B
```

---

# Referencia a Organization

Assembly mantiene:

```text
OrganizationId
```

No mantiene:

```text
Organization
```

como entidad interna.

---

# Existencia de Organization

Cuando una operación requiera comprobar la existencia de
Organization, dicha comprobación no amplía el límite del
Aggregate Assembly.

Assembly no modifica Organization.

---

# Coherencia Organizacional de Commands

Para una Assembly existente:

```text
Command.OrganizationId
=
Assembly.OrganizationId
```

debe mantenerse.

Una discrepancia invalida el contexto del Command.

---

# Invariante Territorial

Territory constituye un Aggregate independiente.

Assembly puede mantener:

```text
TerritoryId
```

cuando corresponda.

Cuando exista, TerritoryId:

* debe ser válido;
* representa exclusivamente una referencia;
* no incorpora Territory completo;
* no otorga autoridad sobre Territory.

---

# Independence de Territory

Assembly no modifica:

```text
Territory
```

para satisfacer reglas propias.

Territory conserva su propio Aggregate y Consistency Boundary.

---

# TerritoryId versus Location

Debe mantenerse:

```text
TerritoryId

≠

AssemblyLocation
```

TerritoryId representa contexto territorial.

AssemblyLocation representa lugar de realización.

---

# Invariante de Tipo

Toda Assembly debe poseer:

```text
AssemblyType
```

válido.

No puede utilizarse un tipo no reconocido por el modelo vigente.

---

# Validez de AssemblyType

AssemblyType:

* es obligatorio;
* debe pertenecer al conjunto admitido;
* puede participar en reglas específicas;
* no constituye identidad;
* solo cambia mediante comportamiento válido.

---

# Cambio de AssemblyType

El cambio de tipo solo puede producirse mediante:

```text
ChangeAssemblyType
```

y debe preservar:

* estado válido;
* AssemblyRules;
* ExecutionConditions;
* AssemblyModality;
* Convocation cuando corresponda;
* invariantes.

Un cambio válido produce:

```text
AssemblyTypeChanged
```

---

# Tipo y Estado Histórico

AssemblyType no debe modificarse de forma que reescriba el
significado de hechos ya ocurridos.

Su mutabilidad disminuye conforme avanza el Lifecycle.

---

# Invariante de Nombre

Toda Assembly debe poseer:

```text
AssemblyName
```

válido.

AssemblyName:

* no puede ser nulo;
* no puede ser vacío;
* no puede consistir exclusivamente en espacios;
* debe respetar su Value Object;
* no constituye identidad.

---

# Cambio de Nombre

El nombre solo cambia mediante:

```text
RenameAssembly
```

y cuando el estado lo permita.

Debe existir cambio semántico real.

---

# Normalización del Nombre

La comparación semántica debe respetar las reglas de:

```text
AssemblyName
```

sin destruir información significativa.

---

# Invariante de Propósito

Assembly puede mantener:

```text
AssemblyPurpose
```

como finalidad formal de la reunión.

No representa:

```text
Proposal

Voting

Participation
```

---

# Obligatoriedad del Propósito

AssemblyPurpose puede ser obligatorio según:

* AssemblyType;
* reglas organizacionales;
* etapa del Lifecycle.

Antes de una transición que requiera propósito formal, este debe
satisfacer las reglas aplicables.

---

# Cambio de Propósito

`ChangeAssemblyPurpose` solo puede aceptarse cuando:

* el estado permita el cambio;
* el nuevo propósito sea válido;
* no contradiga AssemblyType;
* no invalide AssemblyRules;
* no reescriba hechos históricos;
* Convocation permanezca coherente cuando corresponda.

---

# Invariante de Descripción

Assembly puede mantener:

```text
AssemblyDescription
```

como información contextual.

Cuando exista debe ser válida.

---

# Description no Sustituye Purpose

Debe mantenerse:

```text
AssemblyDescription

≠

AssemblyPurpose
```

---

# Invariante de Estado

Toda Assembly debe poseer exactamente un:

```text
AssemblyStatus
```

válido.

Estados oficiales:

```text
Draft

Scheduled

Convoked

InProgress

Completed

Cancelled

Archived
```

---

# Estado Único

Debe cumplirse:

```text
count(CurrentStatus) = 1
```

Una Assembly no puede encontrarse simultáneamente en múltiples
estados.

---

# Estado Perteneciente al Modelo Oficial

No puede utilizarse un estado fuera del modelo vigente.

Estados técnicos o de representación externa no forman
automáticamente parte de AssemblyStatus.

---

# Inmutabilidad Directa del Estado

AssemblyStatus no puede modificarse mediante setter público.

Solo cambia como resultado de comportamiento de dominio válido.

---

# Invariante de State Machine

Toda transición debe estar expresamente permitida por:

```text
DOMAIN-006B-State-Machine.md
```

La ausencia de prohibición explícita no convierte una transición
en válida.

---

# Denegación por Defecto

Debe aplicarse:

```text
deny by default
```

para transiciones no definidas.

---

# Transiciones Principales Permitidas

```text
Draft
    -> Scheduled

Scheduled
    -> Convoked

Convoked
    -> InProgress

InProgress
    -> Completed

Draft
    -> Cancelled

Scheduled
    -> Cancelled

Convoked
    -> Cancelled

Completed
    -> Archived

Cancelled
    -> Archived
```

---

# Prohibición de Saltos de Estado

No se permiten transiciones como:

```text
Draft -> Convoked

Draft -> InProgress

Draft -> Completed

Scheduled -> InProgress

Scheduled -> Completed

Convoked -> Completed
```

---

# Prohibición de Retroceso Implícito

No se permite:

```text
InProgress -> Convoked

Completed -> InProgress

Cancelled -> Scheduled

Archived -> Completed
```

sin evolución formal del dominio.

---

# Invariante de Draft

Draft representa una Assembly creada pero aún no programada
formalmente.

Debe poseer como mínimo:

```text
AssemblyId

OrganizationId

AssemblyName

AssemblyType

AssemblyStatus = Draft

CreatedAt

Version
```

---

# Restricciones de Draft

Desde Draft no puede ejecutarse directamente:

```text
ConvokeAssembly

StartAssembly

CompleteAssembly

ArchiveAssembly
```

Puede permitirse:

```text
ScheduleAssembly

CancelAssembly
```

además de modificaciones permitidas.

---

# Draft no Requiere Ejecución Completa

Draft puede encontrarse en preparación.

Sin embargo, nunca permite ausencia de:

```text
AssemblyId

OrganizationId

AssemblyName

AssemblyType

CreatedAt

AssemblyStatus

Version
```

---

# Invariante de Scheduled

Una Assembly Scheduled debe poseer programación formal válida.

Debe existir:

```text
ScheduledStartAt
```

y una:

```text
AssemblyModality
```

válida.

---

# Scheduled Requiere Programación

No puede existir:

```text
AssemblyStatus = Scheduled

ScheduledStartAt = null
```

---

# Scheduled no Significa Convoked

Debe mantenerse:

```text
Scheduled != Convoked
```

No debe establecerse ConvokedAt únicamente por programar.

---

# Scheduled no Significa Started

Debe mantenerse:

```text
Scheduled != InProgress
```

El paso del tiempo no inicia automáticamente una Assembly.

---

# Invariante de Convoked

Una Assembly Convoked debe haber sido previamente Scheduled y
poseer Convocation válida.

Debe existir:

```text
ConvokedAt
```

---

# Convoked Requiere Convocatoria

No puede existir:

```text
AssemblyStatus = Convoked

ConvokedAt = null
```

---

# Convoked no Significa Notificado

Debe mantenerse:

```text
Convoked

≠

NotificationDelivered
```

Notification conserva su propio Aggregate.

---

# Convoked no Significa InProgress

Debe mantenerse:

```text
Convoked

≠

InProgress
```

El inicio requiere:

```text
StartAssembly
    ↓
AssemblyStarted
```

---

# Invariante de InProgress

Una Assembly InProgress debe haber iniciado formalmente.

Debe existir:

```text
StartedAt
```

y debe provenir de:

```text
Convoked
```

en la versión 1.0.

---

# InProgress Requiere Inicio

No puede existir:

```text
AssemblyStatus = InProgress

StartedAt = null
```

---

# InProgress no Permite Reescritura Estructural

Una Assembly ya iniciada no debe modificarse de forma que
reescriba hechos consolidados.

No puede cambiar ordinariamente:

```text
AssemblyId

OrganizationId

AssemblyType

Schedule

Convocation
```

cuando ello altere hechos ya ocurridos.

---

# Invariante de Completed

Completed requiere una Assembly previamente InProgress.

Deben existir:

```text
StartedAt

CompletedAt
```

válidos.

---

# Completed Requiere Inicio Previo

No puede existir:

```text
AssemblyStatus = Completed

StartedAt = null
```

---

# Completed Requiere Finalización

Debe cumplirse:

```text
CompletedAt != null

CompletedAt >= StartedAt
```

---

# Completed no Significa Archived

Debe mantenerse:

```text
Completed != Archived
```

---

# Completed es Operativamente Cerrado

Desde Completed no se permite:

```text
StartAssembly

CompleteAssembly

CancelAssembly
```

El flujo ordinario posterior permitido es:

```text
Completed -> Archived
```

---

# Invariante de Cancelled

Cancelled representa una Assembly cuyo flujo normal fue
cancelado antes de Completion.

Puede provenir de:

```text
Draft

Scheduled

Convoked
```

---

# Cancelled Requiere CancelledAt

Debe cumplirse:

```text
AssemblyStatus = Cancelled

CancelledAt != null
```

---

# Cancelled es Terminal Operativo

Desde Cancelled no puede continuarse mediante:

```text
ScheduleAssembly

ConvokeAssembly

StartAssembly

CompleteAssembly
```

El flujo ordinario permitido es:

```text
Cancelled -> Archived
```

---

# Preservación Histórica al Cancelar

Cancelled no elimina programación ni convocatoria previas.

Los hechos anteriores permanecen verdaderos.

---

# Cancelled no Representa Interruption

La versión 1.0 no utiliza Cancelled para representar una reunión
iniciada y posteriormente interrumpida.

No se introducen implícitamente:

```text
Interrupted

Suspended

Aborted
```

---

# Invariante de Archived

Archived constituye el estado terminal oficial.

Debe cumplirse:

```text
AssemblyStatus = Archived

ArchivedAt != null
```

---

# Estados Permitidos para Archivar

Solo pueden archivarse:

```text
Completed

Cancelled
```

---

# Archived es Inmutable

Después de Archived no se permiten modificaciones funcionales
ordinarias.

---

# Archived no Significa Deleted

Debe mantenerse:

```text
Archived

≠

Deleted
```

Archived representa estado histórico terminal.

---

# Invariante Temporal General

Toda información temporal debe mantener coherencia cronológica.

Timestamps relevantes:

```text
CreatedAt

ScheduledStartAt

ScheduledEndAt

ConvokedAt

StartedAt

CompletedAt

CancelledAt

ArchivedAt
```

---

# CreatedAt

CreatedAt:

* es obligatorio;
* se establece una sola vez;
* es inmutable;
* representa creación del Aggregate.

---

# CreatedAt y Estados Posteriores

CreatedAt debe conservarse durante toda la existencia de
Assembly.

---

# Invariante de Programación

Cuando exista ScheduledEndAt:

```text
ScheduledEndAt > ScheduledStartAt
```

debe cumplirse.

---

# ScheduledStartAt Obligatorio

ScheduledStartAt es obligatorio en:

```text
Scheduled

Convoked

InProgress
```

y se preserva históricamente cuando corresponda.

---

# ScheduledEndAt Opcional

Cuando el dominio permita duración abierta:

```text
ScheduledEndAt = null
```

puede ser válido.

---

# Igualdad de Inicio y Fin Programado

Si ScheduledEndAt existe, es inválido:

```text
ScheduledEndAt = ScheduledStartAt
```

---

# Programación en el Pasado

La validez de:

```text
ScheduledStartAt < CurrentTime
```

depende de la política temporal explícita del dominio.

No debe inferirse desde infraestructura.

---

# TimeZone

La programación debe poseer significado temporal no ambiguo.

Cuando se utilice:

```text
TimeZone
```

debe ser válido.

---

# Invariante de Reprogramación

RescheduleAssembly debe producir una nueva programación válida y
no puede modificar:

```text
CreatedAt

StartedAt

CompletedAt

CancelledAt

ArchivedAt
```

---

# Reprogramación de Assembly Convoked

Una reprogramación en Convoked debe preservar coherencia entre:

```text
Schedule

Convocation
```

No puede quedar Convoked con una convocatoria incompatible.

---

# Preservación del Schedule Histórico

Una reprogramación produce:

```text
AssemblyRescheduled
```

sin reescribir el hecho histórico anterior.

---

# Invariante de ConvokedAt

ConvokedAt representa un hecho histórico y no puede eliminarse
posteriormente para fingir que la convocatoria nunca ocurrió.

---

# Invariante de StartedAt

StartedAt solo puede establecerse mediante:

```text
Convoked -> InProgress
```

y posteriormente permanece como hecho histórico.

---

# Inicio Programado versus Inicio Real

Debe mantenerse:

```text
ScheduledStartAt

≠

StartedAt
```

El primero representa planificación.

El segundo representa inicio efectivo.

---

# Inicio Real Posterior al Programado

Puede existir:

```text
StartedAt > ScheduledStartAt
```

sin que ello constituya por sí mismo una inconsistencia.

---

# Inicio Real Anterior al Programado

La validez de:

```text
StartedAt < ScheduledStartAt
```

depende de una regla explícita del dominio.

---

# Invariante de CompletedAt

CompletedAt solo puede establecerse mediante:

```text
InProgress -> Completed
```

y debe cumplir:

```text
CompletedAt >= StartedAt
```

---

# Fin Programado versus Fin Real

Debe mantenerse:

```text
ScheduledEndAt

≠

CompletedAt
```

---

# Invariante de CancelledAt

Cancelled requiere:

```text
CancelledAt != null
```

y no reemplaza timestamps históricos anteriores.

---

# Invariante de ArchivedAt

Archived requiere:

```text
ArchivedAt != null
```

y:

```text
ArchivedAt >= CompletedAt
```

cuando proviene de Completed;

o:

```text
ArchivedAt >= CancelledAt
```

cuando proviene de Cancelled.

---

# Coherencia Temporal de Lifecycle

Cuando correspondan deben mantenerse relaciones como:

```text
CreatedAt <= ConvokedAt

StartedAt <= CompletedAt

CompletedAt <= ArchivedAt
```

---

# Coherencia Temporal de Cancelación

Debe mantenerse:

```text
CreatedAt <= CancelledAt
```

y, cuando posteriormente se archive:

```text
CancelledAt <= ArchivedAt
```

---

# Invariante de Modalidad

Toda Assembly que alcance Scheduled debe poseer:

```text
AssemblyModality
```

válida.

Modalidades oficiales:

```text
InPerson

Remote

Hybrid
```

---

# Invariante InPerson

Cuando:

```text
AssemblyModality = InPerson
```

Location debe satisfacer las reglas aplicables para realización
presencial.

---

# Invariante Remote

Cuando:

```text
AssemblyModality = Remote
```

la ubicación física puede ser opcional.

Assembly no incorpora infraestructura tecnológica de reunión
remota dentro del Aggregate.

---

# Invariante Hybrid

Cuando:

```text
AssemblyModality = Hybrid
```

las condiciones deben ser compatibles con realización presencial
y remota.

---

# Cambio de Modalidad

El cambio de modalidad se expresa exclusivamente mediante:

```text
ChangeAssemblyModality
```

y debe preservar:

* estado permitido;
* modalidad válida;
* Location compatible;
* AssemblyRules válidas;
* ExecutionConditions válidas;
* Convocation coherente cuando corresponda.

Un cambio válido produce:

```text
AssemblyModalityChanged
```

Debe mantenerse el lenguaje canónico:

```text
AssemblyModality
    │
    ▼
ChangeAssemblyModality
    │
    ▼
AssemblyModalityChanged
```

---

# Modalidad y Estado

La modalidad no debe reescribirse arbitrariamente después de que
la reunión haya iniciado.

Su mutabilidad disminuye conforme avanza el Lifecycle.

---

# Invariante de Location

Debe mantenerse:

```text
AssemblyLocation

≠

Territory
```

y:

```text
AssemblyLocation

≠

TerritoryId
```

Location debe ser compatible con AssemblyModality.

---

# Validación de Location

Cuando Location sea obligatoria debe ser:

* estructuralmente válida;
* semánticamente válida;
* compatible con AssemblyModality;
* compatible con AssemblyRules.

---

# Cambio de Location

ChangeAssemblyLocation debe preservar:

* identidad;
* Organization;
* modalidad;
* convocatoria;
* estado;
* historicidad.

---

# Cambio de Location durante InProgress

Solo puede permitirse cuando representa un cambio real ocurrido
durante la reunión y el modelo vigente lo autoriza.

No puede utilizarse para reescribir la ubicación histórica de
inicio.

---

# Invariante de Convocation

Convocation debe ser coherente con:

* Organization;
* Assembly;
* Schedule;
* AssemblyType;
* AssemblyModality;
* Location;
* AssemblyRules;
* AssemblyStatus;
* plazos aplicables.

---

# ConvocationStatus

ConvocationStatus debe ser coherente con AssemblyStatus.

No puede representar una combinación contradictoria con el
Lifecycle.

---

# ConvocationDate

ConvocationDate debe poseer significado temporal válido.

No sustituye automáticamente:

```text
ConvokedAt
```

---

# ConvocationDeadline

Cuando exista debe ser compatible con:

```text
ScheduledStartAt
```

y con las reglas de convocatoria.

---

# ConvocationMethod

ConvocationMethod debe pertenecer al conjunto permitido por el
dominio.

No implica que Assembly ejecute físicamente la comunicación.

---

# ConvocationReference

Cuando exista:

```text
ConvocationReference
```

debe ser válida y no incorpora un Document completo al
Aggregate.

---

# ConvocationRules

Las reglas de convocatoria deben estar satisfechas antes de
producir:

```text
AssemblyConvoked
```

---

# Convocation versus Notification

Debe mantenerse:

```text
Convocation

≠

Notification
```

Convocation pertenece a Assembly.

Notification mantiene su propio Aggregate.

---

# Fallo de Notification

Un fallo posterior de Notification no revierte el hecho:

```text
AssemblyConvoked
```

ya confirmado.

---

# Invariante de AssemblyRules

AssemblyRules deben:

* pertenecer a Assembly;
* ser válidas;
* ser coherentes;
* respetar AssemblyType;
* respetar AssemblyModality;
* respetar Lifecycle;
* preservar invariantes superiores;
* no introducir responsabilidades externas.

---

# AssemblyRules Configurables

Las reglas configurables pueden variar entre Assemblies sin
alterar las invariantes estructurales.

---

# AssemblyRules y Proposal

Una regla relacionada con Proposal no convierte Proposal en
entidad interna de Assembly.

---

# AssemblyRules y Voting

Una regla relacionada con Voting no convierte Voting en entidad
interna de Assembly.

---

# Reglas no Pueden Anular Invariantes

Ninguna AssemblyRule puede declarar válida una transición
prohibida por el modelo.

---

# Cambio de AssemblyRules

UpdateAssemblyRules debe garantizar que las nuevas reglas:

* sean válidas;
* sean coherentes;
* sean compatibles con AssemblyType;
* sean compatibles con AssemblyModality;
* sean compatibles con ExecutionConditions;
* puedan modificarse en el estado vigente;
* no reescriban hechos históricos.

---

# Invariantes de ExecutionConditions

ExecutionConditions:

* deben ser evaluables;
* pertenecen al contexto de Assembly;
* no modifican otros Aggregates;
* deben ser coherentes con AssemblyType;
* deben ser coherentes con AssemblyModality;
* deben ser coherentes con AssemblyRules;
* deben satisfacerse antes de StartAssembly cuando sean
  obligatorias.

---

# Ejemplos de ExecutionConditions

Pueden existir conceptos como:

```text
RequiredConvocation

RequiredSchedule

RequiredLocation

RequiredDocumentation

MinimumAttendance

RequiredQuorum
```

siempre dentro del Consistency Boundary definido.

---

# RequiredQuorum

Cuando el quórum forme parte de las condiciones propias de
Assembly, debe existir una decisión válida sobre su cumplimiento
antes del inicio.

Esto no incorpora Citizen, Membership o Participation al
Aggregate.

---

# Dependencias Externas para Validación

Algunas reglas pueden necesitar información perteneciente a
otros Aggregates.

Assembly no adquiere ownership sobre dicha información.

---

# Snapshot de Decisión

Cuando una decisión dependa de información externa puede
representarse conceptualmente mediante una decisión validada,
sin incorporar el Aggregate externo.

Esto no modifica el Consistency Boundary de Assembly.

---

# Invariantes de Realización

Antes de iniciar debe cumplirse como mínimo:

```text
AssemblyStatus = Convoked

ScheduleValid = true

ConvocationValid = true

ModalityValid = true

LocationValid = true when required

ExecutionConditionsSatisfied = true
```

---

# StartAssembly

StartAssembly solo puede aceptarse desde:

```text
Convoked
```

y debe producir:

```text
AssemblyStatus = InProgress

StartedAt != null
```

junto con:

```text
AssemblyStarted
```

---

# Prohibición de Inicio Automático

Debe mantenerse:

```text
CurrentTime >= ScheduledStartAt

≠

AssemblyStatus = InProgress
```

El inicio requiere comportamiento explícito.

---

# Inicio y Permisos

Deben satisfacerse independientemente:

```text
Authorization
```

y:

```text
Domain Validity
```

Ninguna sustituye a la otra.

---

# Invariante de Finalización

CompleteAssembly solo puede ejecutarse desde:

```text
InProgress
```

y debe producir:

```text
AssemblyStatus = Completed

CompletedAt != null

CompletedAt >= StartedAt
```

---

# Finalización no Automática

Debe mantenerse:

```text
CurrentTime >= ScheduledEndAt

≠

AssemblyStatus = Completed
```

---

# Finalización no Archiva

Debe mantenerse:

```text
Completed

≠

Archived
```

---

# Finalización no Modifica Otros Aggregates

AssemblyCompleted no modifica directamente:

```text
Proposal

Participation

Voting

Document

Notification

Audit
```

---

# Invariante de Cancelación

CancelAssembly solo puede ejecutarse desde:

```text
Draft

Scheduled

Convoked
```

y debe producir:

```text
AssemblyStatus = Cancelled

CancelledAt != null
```

---

# CancellationReason

Cuando sea obligatorio:

```text
CancellationReason
```

debe ser válido y formar parte del hecho de cancelación según el
contrato vigente.

---

# Cancelación desde InProgress

La versión 1.0 no permite:

```text
InProgress -> Cancelled
```

No debe introducirse implícitamente una semántica de interrupción.

---

# Cancelación no Elimina la Assembly

CancelAssembly conserva:

* AssemblyId;
* OrganizationId;
* programación histórica;
* convocatoria histórica;
* Version;
* timestamps;
* Domain Events;
* trazabilidad.

---

# Cancelación no Revierte Domain Events

Si ocurrieron:

```text
AssemblyScheduled

AssemblyConvoked
```

una cancelación posterior agrega:

```text
AssemblyCancelled
```

sin eliminar los hechos previos.

---

# Invariante de Archivado

ArchiveAssembly solo puede ejecutarse desde:

```text
Completed

Cancelled
```

y debe producir:

```text
AssemblyStatus = Archived

ArchivedAt != null
```

---

# ArchiveReason

Cuando sea requerido, ArchiveReason debe ser válido.

No reemplaza ni modifica el estado histórico anterior.

---

# Archivado no es Eliminación

Debe mantenerse:

```text
Archived

≠

Physical Deletion
```

---

# Invariantes de Referencias Externas

Assembly puede relacionarse mediante IDs con otros Aggregates.

Las referencias no convierten esos Aggregates en entidades
internas.

---

# Regla de Referencia por Identidad

Debe utilizarse:

```text
AggregateId
```

y no una referencia mutable hacia otro Aggregate.

---

# Regla de No Absorción

Assembly no incorpora:

```text
Organization

Citizen

Membership

Role

Territory

Proposal

Participation

Voting

Document

Notification

Audit

Integration
```

como Aggregates internos.

---

# Invariante de Membership

Assembly no administra el Lifecycle de Membership.

---

# Invariante de Citizen

Assembly no administra identidad, datos personales, estado ni
credenciales de Citizen.

---

# Invariante de Role

Assembly no crea, modifica, archiva ni asigna Roles.

---

# Invariante de Proposal

Proposal conserva:

```text
ProposalId

Lifecycle

Invariants

Repository

Domain Events
```

propios.

Assembly no modifica Proposal directamente.

---

# Invariante de Participation

Participation mantiene su propio Consistency Boundary.

Assembly proporciona contexto mediante AssemblyId cuando
corresponda.

---

# Invariante de Voting

Voting mantiene identidad, reglas, estado, Lifecycle e Invariants
propios.

---

# Invariante de Document

Document mantiene su contenido y Lifecycle fuera de Assembly.

Assembly puede mantener únicamente referencias cuando
corresponda.

---

# Invariante de Notification

Notification conserva:

```text
NotificationId

Notification Lifecycle

Notification State

Notification Consistency Boundary
```

fuera de Assembly.

---

# Invariante de Audit

Audit conserva su propio Aggregate.

Un hecho de Assembly puede ser utilizado para trazabilidad sin
incorporar Audit dentro del Aggregate.

---

# Invariante de Integration

Integration mantiene su propio Aggregate y no constituye una
entidad interna de Assembly.

---

# Invariante de Consistency Boundary

Debe mantenerse:

```text
One AssemblyId

=

One Immediate Consistency Boundary
```

---

# Atomicidad Conceptual

Una operación válida sobre Assembly debe dejar simultáneamente:

* estado coherente;
* timestamps coherentes;
* Version coherente;
* invariantes satisfechas;
* Domain Events coherentes.

---

# Prohibición de Estado Parcial

No debe persistirse conceptualmente:

```text
Status = InProgress

StartedAt = null
```

ni ninguna combinación parcial equivalente.

---

# Rollback Conceptual

Si una operación no puede completar todas sus reglas, el
Aggregate debe permanecer sin modificación.

---

# Consistencia entre Aggregates

La consistencia inmediata termina en Assembly.

Debe mantenerse:

```text
Cross-Aggregate Collaboration

=

Eventual Consistency
```

---

# Prohibición de Transacción Distribuida Implícita

No debe asumirse:

```text
Assembly Transaction
    +
Other Aggregate Transaction
    =
One Domain Transaction
```

---

# Invariante de Version

Assembly mantiene:

```text
Version
```

como versión monotónicamente creciente del Aggregate.

---

# Inicialización de Version

La creación válida inicializa Version conforme al contrato
oficial de Versioning.

---

# Incremento de Version

Toda modificación semántica válida incrementa:

```text
Version = PreviousVersion + 1
```

conforme al contrato vigente.

---

# No Incremento en Operación Rechazada

Un Command rechazado no incrementa Version.

---

# No Incremento por Lectura

Una Query o lectura no modifica Version.

---

# No-Op

Una operación sin cambio semántico real no debe producir
artificialmente:

```text
Version Increment

Domain Event
```

conforme a la regla oficial de No-Op.

---

# Invariante de Concurrencia

Una escritura debe operar sobre una versión vigente del
Aggregate.

---

# Conflicto de Concurrencia

Cuando:

```text
ExpectedVersion != PersistedVersion
```

la modificación no debe aceptarse como si operara sobre el estado
vigente.

---

# Revalidación después de Conflicto

Después de un conflicto debe recuperarse el estado vigente y
reevaluarse la intención.

---

# Invariantes de Domain Events

Los Domain Events:

* representan hechos consumados;
* se generan únicamente después de comportamiento válido;
* mantienen coherencia con el estado resultante;
* preservan identidad y Version;
* no se generan después de rechazo;
* son inmutables.

---

# Evento después de Estado Válido

Debe mantenerse:

```text
Valid State Change
    │
    ▼
Domain Event
```

y no el orden contrario.

---

# No Event on Failure

Una operación rechazada no produce Domain Event de éxito.

---

# Inmutabilidad de Eventos

Un Domain Event ocurrido no se modifica para representar un hecho
posterior diferente.

---

# AggregateVersion del Evento

El Domain Event debe reflejar la versión correspondiente al hecho
confirmado.

---

# Evento Coherente con el Estado

No puede existir:

```text
AssemblyStarted
```

si el estado resultante no satisface las invariantes de
InProgress.

---

# Invariantes de Commands

Cada Command debe:

* expresar intención válida;
* respetar estado;
* preservar identidad;
* preservar ownership;
* preservar invariantes;
* respetar Version;
* modificar únicamente Assembly.

---

# CreateAssembly

CreateAssembly debe producir una Assembly válida con:

```text
AssemblyId

OrganizationId

AssemblyName

AssemblyType

AssemblyStatus = Draft

CreatedAt

Version
```

---

# CreateAssembly y Estado Inicial

Debe mantenerse:

```text
CreateAssembly
    ↓
Draft
```

No puede crearse directamente en otro estado.

---

# ScheduleAssembly

ScheduleAssembly requiere Draft y programación válida.

Produce:

```text
Draft -> Scheduled

AssemblyScheduled
```

---

# RescheduleAssembly

RescheduleAssembly modifica planificación sin reescribir hechos
históricos.

Produce:

```text
AssemblyRescheduled
```

cuando existe cambio real.

---

# ConvokeAssembly

ConvokeAssembly requiere:

```text
AssemblyStatus = Scheduled
```

y una Convocation válida.

Produce:

```text
AssemblyConvoked
```

---

# RenameAssembly

RenameAssembly requiere nombre válido, cambio real y estado
modificable.

Produce:

```text
AssemblyRenamed
```

---

# ChangeAssemblyType

ChangeAssemblyType debe preservar todas las invariantes
relacionadas con clasificación, reglas, modalidad y estado.

Produce:

```text
AssemblyTypeChanged
```

---

# ChangeAssemblyPurpose

ChangeAssemblyPurpose debe preservar propósito válido y coherencia
con las reglas existentes.

Produce:

```text
AssemblyPurposeChanged
```

---

# ChangeAssemblyDescription

ChangeAssemblyDescription solo puede modificar información
descriptiva permitida.

Produce:

```text
AssemblyDescriptionChanged
```

---

# ChangeAssemblyModality

ChangeAssemblyModality debe mantener:

```text
AssemblyModality
```

válida y compatible con Location, Rules, ExecutionConditions y
estado.

Produce exclusivamente:

```text
AssemblyModalityChanged
```

No se introduce:

```text
AssemblyModeChanged
```

como Domain Event paralelo.

---

# ChangeAssemblyLocation

ChangeAssemblyLocation debe preservar coherencia con
AssemblyModality, estado y Convocation.

Produce:

```text
AssemblyLocationChanged
```

---

# UpdateAssemblyConvocation

UpdateAssemblyConvocation debe preservar:

* ConvokedAt histórico cuando exista;
* Schedule;
* State;
* coherencia de Convocation.

Produce:

```text
AssemblyConvocationUpdated
```

---

# UpdateAssemblyRules

UpdateAssemblyRules debe mantener reglas válidas y compatibles con
todas las invariantes superiores.

Produce:

```text
AssemblyRulesUpdated
```

---

# UpdateAssemblyExecutionConditions

UpdateAssemblyExecutionConditions debe preservar compatibilidad
con AssemblyRules, AssemblyType, AssemblyModality y estado.

Produce:

```text
AssemblyExecutionConditionsUpdated
```

---

# StartAssembly

StartAssembly requiere:

```text
AssemblyStatus = Convoked
```

y todas las condiciones de realización satisfechas.

Produce:

```text
AssemblyStatus = InProgress

StartedAt != null

AssemblyStarted
```

---

# CompleteAssembly

CompleteAssembly requiere:

```text
AssemblyStatus = InProgress
```

y produce:

```text
AssemblyStatus = Completed

CompletedAt != null

AssemblyCompleted
```

---

# CancelAssembly

CancelAssembly solo puede aplicarse desde:

```text
Draft

Scheduled

Convoked
```

y produce:

```text
Cancelled

AssemblyCancelled
```

---

# ArchiveAssembly

ArchiveAssembly solo puede aplicarse desde:

```text
Completed

Cancelled
```

y produce:

```text
Archived

AssemblyArchived
```

---

# Invariantes de Modificaciones Descriptivas

Las modificaciones descriptivas no pueden:

* cambiar AssemblyId;
* cambiar OrganizationId;
* saltar State Machine;
* reescribir hechos históricos;
* ampliar Consistency Boundary.

---

# Mutabilidad Decreciente

Conforme avanza el Lifecycle, disminuye el conjunto de
propiedades modificables.

Debe mantenerse conceptualmente:

```text
Draft
    >
Scheduled
    >
Convoked
    >
InProgress
    >
Completed / Cancelled
    >
Archived
```

en términos de capacidad ordinaria de modificación.

---

# Invariantes y Application Services

Application puede coordinar una intención, pero no sustituye la
autoridad del Aggregate sobre sus invariantes.

---

# Regla de No Duplicación de Invariantes como Autoridad

Una validación externa puede repetir una comprobación para
anticipar errores, pero Assembly continúa siendo la autoridad
normativa.

---

# Invariantes y Repository

Repository recupera y persiste Assembly como unidad.

No define las reglas que hacen válida una Assembly.

---

# Repository no Define Invariantes

Debe mantenerse:

```text
Persistence Constraint

≠

Domain Invariant
```

aunque ambos puedan reforzarse mutuamente.

---

# Invariantes y Rehidratación

Una Assembly rehidratada debe satisfacer las invariantes
correspondientes a su estado.

Una inconsistencia no debe corregirse silenciosamente.

---

# Rehidratación no Ejecuta Transiciones

Restaurar un estado histórico válido no equivale a ejecutar
Commands o generar nuevos Domain Events.

---

# Invariantes y Event Sourcing

Cuando Event Sourcing sea utilizado, la secuencia de eventos debe
reconstruir únicamente estados válidos.

La compatibilidad con Event Sourcing no obliga su adopción.

---

# Secuencia de Eventos Inválida

Una secuencia como:

```text
AssemblyCreated
    ↓
AssemblyStarted
```

sin hechos requeridos por el Lifecycle no representa una
evolución válida.

---

# Replay

Un replay restaura hechos históricos.

No debe producir nuevas decisiones de dominio ni modificar la
semántica del historial.

---

# Invariantes de Seguridad

Las invariantes del Aggregate deben cumplirse independientemente
del origen de la intención.

Ningún sistema externo puede saltarse Assembly.

---

# ActorId

ActorId representa una referencia cuando corresponda.

No incorpora Citizen dentro de Assembly ni modifica las
invariantes de identidad.

---

# Invariantes de Independencia Tecnológica

Ninguna invariante depende de:

```text
HTTP

REST

GraphQL

Kafka

RabbitMQ

MQTT

MongoDB

PostgreSQL

Redis

FIWARE

NGSI-LD
```

---

# Invariantes de Interoperabilidad

Una representación externa de Assembly debe respetar los hechos
válidos del dominio.

Un modelo externo no redefine las invariantes internas.

---

# Anti-Corruption Layer

Una semántica externa diferente debe traducirse antes de
convertirse en intención válida de AURA.

No se incorpora automáticamente al lenguaje ubicuo.

---

# Invariantes y FIWARE

FIWARE permanece fuera del Aggregate.

Debe mantenerse:

```text
FIWARE Entity

≠

Assembly Aggregate
```

---

# FIWARE como Proyección

Una representación externa puede reflejar información de
Assembly sin convertirse en fuente de verdad del Aggregate.

---

# Invariantes y Read Models

Los Read Models representan información derivada.

Debe mantenerse:

```text
Read Model

≠

Write Authority
```

---

# Read Model Derivable

Una vista puede reconstruirse o actualizarse a partir de hechos
válidos sin modificar Assembly.

---

# Invariantes y CQRS

La separación conceptual entre Commands y Queries no modifica las
invariantes.

Las invariantes pertenecen al Write Model de Assembly.

---

# Invariantes y Consistencia Eventual

Otros Aggregates pueden observar hechos de Assembly
posteriormente.

Esta demora no altera la consistencia inmediata interna de
Assembly.

---

# Fallo de un Consumidor Externo

Un fallo posterior de un consumidor no convierte en falso un
hecho ya confirmado por Assembly.

---

# Invariantes de Orden de Eventos

Dentro de una Assembly, AggregateVersion preserva el orden lógico
de sus modificaciones.

No se establece un orden global entre distintos Aggregates.

---

# Evento Duplicado

Una repetición técnica del mismo evento no representa un nuevo
Domain Fact.

Dos hechos reales diferentes deben mantener identidad y Version
propias.

---

# Commands Duplicados

Una retransmisión de una misma intención no debe convertirse por
sí sola en una segunda modificación semántica.

Las reglas del Aggregate continúan siendo autoridad.

---

# Validación Determinista

Dado el mismo estado de Assembly y las mismas decisiones de
dominio requeridas, la evaluación de invariantes debe producir el
mismo resultado conceptual.

---

# Tiempo como Dependencia Explícita

Cuando una invariante dependa del tiempo, el valor temporal
utilizado debe formar parte explícita del contexto de la
decisión.

---

# No Reparación Silenciosa

Un estado inválido no debe corregirse automáticamente cambiando
su significado histórico.

La inconsistencia debe detectarse y tratarse mediante un proceso
explícito.

---

# Normalización versus Reparación

Normalizar una representación equivalente no debe confundirse con
reparar un estado semánticamente inválido.

Debe preservarse el significado original.

---

# Violación de Invariantes

Toda violación de invariante provoca rechazo de la operación.

El Aggregate permanece sin modificación.

---

# Error de Dominio

Una violación debe expresarse mediante el modelo de errores de
dominio correspondiente.

No se convierte en un estado válido adicional.

---

# Error no es Estado

Debe mantenerse:

```text
Domain Error

≠

AssemblyStatus
```

---

# Invariantes y Auditoría

Los hechos válidos y los intentos rechazados pueden ser
trazables, pero Audit conserva su propio Aggregate.

---

# Intentos Rechazados

Un intento rechazado:

```text
≠

Successful Assembly Domain Event
```

No modifica Assembly.

---

# Matriz de Invariantes por Estado

| Invariante | Draft | Scheduled | Convoked | InProgress | Completed | Cancelled | Archived |
|---|---:|---:|---:|---:|---:|---:|---:|
| AssemblyId válido | Sí | Sí | Sí | Sí | Sí | Sí | Sí |
| OrganizationId válido | Sí | Sí | Sí | Sí | Sí | Sí | Sí |
| AssemblyName válido | Sí | Sí | Sí | Sí | Sí | Sí | Sí |
| AssemblyType válido | Sí | Sí | Sí | Sí | Sí | Sí | Sí |
| ScheduledStartAt requerido | No | Sí | Sí | Sí | Histórico | Histórico | Histórico |
| AssemblyModality requerida | Condicional | Sí | Sí | Sí | Histórica | Histórica | Histórica |
| ConvokedAt requerido | No | No | Sí | Sí | Histórico | Condicional | Histórico |
| StartedAt requerido | No | No | No | Sí | Sí | No | Condicional |
| CompletedAt requerido | No | No | No | No | Sí | No | Condicional |
| CancelledAt requerido | No | No | No | No | No | Sí | Condicional |
| ArchivedAt requerido | No | No | No | No | No | No | Sí |
| Modificación ordinaria | Sí | Sí | Limitada | Muy limitada | No | No | No |

`Condicional` depende del camino histórico recorrido por la
instancia.

---

# Matriz de Transiciones e Invariantes

| Transición | Requisito fundamental |
|---|---|
| No existe → Draft | identidad, Organization, tipo y nombre válidos |
| Draft → Scheduled | Schedule y AssemblyModality válidos |
| Scheduled → Convoked | Convocation válida |
| Convoked → InProgress | ExecutionConditions satisfechas |
| InProgress → Completed | StartedAt existente y CompletedAt válido |
| Draft → Cancelled | cancelación válida |
| Scheduled → Cancelled | cancelación válida preservando Schedule |
| Convoked → Cancelled | cancelación válida preservando Convocation |
| Completed → Archived | archivado válido |
| Cancelled → Archived | archivado válido |

---

# Invariantes Iniciales

Toda nueva Assembly debe garantizar:

```text
AssemblyId valid

OrganizationId valid

AssemblyName valid

AssemblyType valid

AssemblyStatus = Draft

CreatedAt valid

Version valid
```

---

# Invariantes Permanentes

Deben mantenerse durante toda la existencia:

```text
AssemblyId immutable

OrganizationId immutable

AssemblyStatus valid

Version valid

CreatedAt immutable

Consistency Boundary preserved
```

---

# Invariantes Condicionales

Algunas invariantes se activan según estado o historial.

Ejemplos:

```text
Scheduled => ScheduledStartAt != null

Convoked => ConvokedAt != null

InProgress => StartedAt != null

Completed => CompletedAt != null

Cancelled => CancelledAt != null

Archived => ArchivedAt != null
```

---

# Invariantes Históricas

Los hechos ocurridos no se eliminan cuando el Aggregate avanza de
estado.

---

# Preservación de Historia

Cancelled o Archived no eliminan timestamps ni hechos previos
válidos.

---

# Histórico de Programación

Una reprogramación no elimina el hecho de que existió una
programación anterior.

---

# Histórico de Convocatoria

Una actualización de Convocation no elimina:

```text
ConvokedAt
```

cuando la convocatoria formal ya ocurrió.

---

# Invariantes de Eliminación

La versión 1.0 no define:

```text
DeleteAssembly
```

como comportamiento ordinario de dominio.

Archived no equivale a Deleted.

---

# Invariantes de Reactivación

La versión 1.0 no define reactivación de:

```text
Completed

Cancelled

Archived
```

---

# Reapertura no Implícita

No se introduce:

```text
ReopenAssembly
```

por inferencia.

Una capacidad futura requiere evolución formal del dominio.

---

# Invariantes de Integración

Un Integration Event no puede representar un hecho que no haya
sido confirmado por el dominio.

Debe mantenerse:

```text
Domain Event

≠

Integration Event
```

---

# Integration Event de Salida

La existencia de un mapping no modifica el Aggregate ni crea una
nueva transición.

En particular:

```text
AssemblyScheduled
    │
    ▼
AssemblyPublished
```

representa un mapping contractual cuando corresponda.

Debe mantenerse:

```text
AssemblyScheduled

≠

Mandatory AssemblyPublished
```

y:

```text
AssemblyCreated

≠

AssemblyPublished Source Domain Event
```

---

# Invariantes y Transactional Outbox

La protección de invariantes no depende de la adopción de
Transactional Outbox.

La elección de mecanismos técnicos de publicación permanece fuera
del dominio.

---

# Invariantes y Performance

Una optimización no puede debilitar una invariante.

Debe mantenerse:

```text
Performance Optimization

≠

Permission to Bypass Domain Rules
```

---

# Caché

Una representación en caché no constituye autoridad para aceptar
una escritura cuando contradice la versión vigente del Aggregate.

---

# Invariantes de Seguridad del Dominio

Assembly protege sus invariantes incluso frente a una intención
técnicamente autenticada o autorizada.

---

# Privacidad

Las reglas de dominio deben evitar incorporar información que no
pertenece a Assembly.

---

# Minimización de Datos

Las referencias externas deben utilizar identificadores cuando
sean suficientes.

El Aggregate no incorpora perfiles completos sin necesidad de
dominio.

---

# Reglas de Implementación

Toda implementación de Assembly debe preservar las invariantes
definidas en este documento.

La tecnología utilizada no puede redefinirlas.

---

# Constructors

Un constructor no debe permitir crear una Assembly que viole las
invariantes iniciales.

---

# Factories

Una Factory de dominio, cuando exista, debe producir únicamente
Aggregates inicialmente válidos.

---

# Value Objects

Los Value Objects deben proteger la validez de sus propios
valores.

Ejemplos:

```text
AssemblyName

AssemblyType

AssemblyModality

AssemblyLocation
```

---

# Value Objects no Sustituyen Aggregate Invariants

Un Value Object válido no garantiza por sí solo que el estado
completo del Aggregate sea válido.

Ejemplo:

una AssemblyModality individualmente válida puede ser
incompatible con el estado o Location actual.

---

# Make Invalid States Unrepresentable

Cuando sea posible, el modelo debe evitar representar estados
inválidos.

Esto no elimina la obligación de validar invariantes que dependen
de múltiples conceptos del Aggregate.

---

# Excepciones de Dominio

Las violaciones deben utilizar el modelo de errores definido por
AURA.

No se deben introducir errores técnicos como sustituto de
significado de dominio.

---

# Dominio versus Infraestructura

Debe mantenerse:

```text
Domain Invariant

≠

Infrastructure Constraint
```

El dominio define la regla.

La infraestructura puede reforzarla, pero no sustituirla.

---

# Escenarios Obligatorios de Validación

Deben existir escenarios que validen al menos:

```text
crear Assembly válida;

rechazar identidad inválida;

rechazar OrganizationId inválido;

rechazar cambio de OrganizationId;

programar Assembly válida;

rechazar Schedule inválido;

convocar Assembly válida;

rechazar convocatoria inválida;

iniciar Assembly convocada;

rechazar inicio desde Draft;

rechazar inicio desde Scheduled;

completar Assembly InProgress;

rechazar Completion sin StartedAt;

cancelar desde Draft;

cancelar desde Scheduled;

cancelar desde Convoked;

rechazar cancelación desde InProgress;

archivar desde Completed;

archivar desde Cancelled;

rechazar archivado desde Scheduled;

rechazar modificación de Archived;

preservar AssemblyId;

preservar OrganizationId;

preservar CreatedAt;

preservar ConvokedAt histórico;

preservar StartedAt histórico;

preservar CompletedAt histórico;

preservar programación después de cancelación;

incrementar Version después de modificación válida;

no incrementar Version después de rechazo;

no incrementar Version después de No-Op;

no publicar Domain Event después de rechazo;

publicar Domain Event después de transición válida;

rechazar conflicto de concurrencia;

rechazar estado rehidratado inconsistente;

no absorber Aggregates externos;

no permitir infraestructura dentro del dominio.
```

Los escenarios formales se desarrollan en:

```text
DOMAIN-006M-Test-Scenarios.md
```

---

# Property-Based Testing

Las invariantes fundamentales son candidatas a pruebas basadas en
propiedades.

Ejemplos:

```text
AssemblyId never changes

OrganizationId never changes

Version never decreases

Archived never transitions

CompletedAt is never before StartedAt

ScheduledEndAt is always after ScheduledStartAt
    when ScheduledEndAt exists
```

---

# Pruebas de Secuencias

Debe verificarse que las secuencias completas mantengan las
invariantes.

Ejemplo válido:

```text
Create
    ↓
Draft

Schedule
    ↓
Scheduled

Convoke
    ↓
Convoked

Start
    ↓
InProgress

Complete
    ↓
Completed

Archive
    ↓
Archived
```

---

# Secuencia Cancelada Válida

```text
Create
    ↓
Draft

Schedule
    ↓
Scheduled

Convoke
    ↓
Convoked

Cancel
    ↓
Cancelled

Archive
    ↓
Archived
```

Los hechos históricos previos permanecen.

---

# Secuencia Inválida

```text
Create
    ↓
Draft

Start
    ↓
InProgress
```

debe ser imposible.

Debe verificarse:

```text
Status remains Draft

StartedAt remains null

Version unchanged

AssemblyStarted not generated
```

---

# Invariantes y Test Fixtures

Las pruebas no deben construir estados imposibles mediante
setters públicos.

Los estados deben alcanzarse mediante comportamiento válido o
rehidratación controlada.

---

# Evolución de Invariantes

Una nueva invariante solo puede incorporarse por una necesidad
real del dominio.

Debe revisarse su impacto sobre:

```text
DOMAIN-006-Aggregate.md

DOMAIN-006A-Lifecycle.md

DOMAIN-006B-State-Machine.md

DOMAIN-006C-Commands.md

DOMAIN-006D-Domain-Events.md

DOMAIN-006E-Invariants.md

DOMAIN-006F-Permissions.md

DOMAIN-006G-Repository-Contract.md

DOMAIN-006I-Versioning.md

DOMAIN-006J-Consistency-Boundary.md

DOMAIN-006K-Integration-Events.md

DOMAIN-006L-Read-Model.md

DOMAIN-006M-Test-Scenarios.md

DOMAIN-006N-Performance-Rules.md

DOMAIN-006O-Security-Model.md

DOMAIN-006P-Extension-Points.md
```

cuando corresponda.

---

# Cambio de Invariante

Modificar una invariante existente constituye una modificación
del comportamiento del dominio.

Debe evaluarse su coherencia con:

* Aggregates existentes;
* datos vigentes;
* hechos históricos;
* Commands;
* State Machine;
* Read Models;
* Integration Events;
* tests;
* versionado.

---

# Invariantes y Versionado de Dominio

Una nueva invariante no debe reinterpretar automáticamente como
inválidos hechos históricos aceptados bajo reglas anteriores.

La evolución requiere tratamiento explícito.

---

# Reglas de Prioridad

Debe mantenerse la autoridad conceptual:

```text
Fundamental Aggregate Invariants
        │
        ▼
Lifecycle / State Machine Rules
        │
        ▼
Assembly Rules
        │
        ▼
Execution Conditions
        │
        ▼
Application Policies
        │
        ▼
Presentation Constraints
```

Una regla inferior no puede anular una regla superior.

---

# Regla de Consistencia Documental

Este documento debe permanecer coherente con:

```text
DOMAIN-006-Aggregate.md

DOMAIN-006A-Lifecycle.md

DOMAIN-006B-State-Machine.md

DOMAIN-006C-Commands.md

DOMAIN-006D-Domain-Events.md
```

Ante una contradicción documental, esta debe resolverse
explícitamente.

No debe seleccionarse una regla arbitrariamente durante la
implementación.

El lenguaje canónico de modalidad permanece:

```text
AssemblyModality

ChangeAssemblyModality

AssemblyModalityChanged
```

---

# Restricciones

No está permitido:

* crear una Assembly sin AssemblyId;
* crear una Assembly sin OrganizationId;
* crear una Assembly sin AssemblyName válido;
* crear una Assembly sin AssemblyType válido;
* crear una Assembly en un estado distinto de Draft;
* modificar AssemblyId;
* reutilizar AssemblyId;
* modificar OrganizationId;
* establecer directamente AssemblyStatus;
* utilizar estados no definidos;
* ejecutar transiciones no definidas;
* omitir estados requeridos;
* iniciar una Assembly no Convoked;
* iniciar una Assembly sin satisfacer ExecutionConditions;
* completar una Assembly no InProgress;
* completar una Assembly sin StartedAt;
* establecer CompletedAt anterior a StartedAt;
* archivar una Assembly no Completed o Cancelled;
* modificar una Assembly Archived;
* continuar normalmente una Assembly Cancelled;
* utilizar Cancelled como Interrupted en versión 1.0;
* eliminar timestamps históricos;
* establecer ScheduledEndAt anterior o igual a ScheduledStartAt;
* mantener una AssemblyModality inválida;
* mantener una Location incompatible;
* mantener una Convocation incompatible con el estado;
* permitir que AssemblyRules anulen invariantes fundamentales;
* modificar otro Aggregate desde Assembly;
* incorporar otros Aggregates como entidades internas;
* producir estados parciales;
* incrementar Version después de una operación rechazada;
* publicar Domain Events de éxito después de una operación
  rechazada;
* permitir que permisos anulen invariantes;
* permitir que Read Models modifiquen el Aggregate;
* permitir que sistemas externos establezcan directamente el
  estado interno;
* depender de Infrastructure para definir una invariante;
* corregir silenciosamente datos inválidos alterando su
  significado;
* utilizar información obsoleta para evadir control de Version;
* reescribir hechos históricos para simplificar el estado actual;
* utilizar `AssemblyModeChanged` como Domain Event oficial;
* utilizar `AssemblyModeChanged` como alias normativo;
* introducir `ChangeAssemblyMode`;
* introducir `AssemblyMode` como concepto paralelo;
* introducir `PreviousMode`;
* introducir `NewMode`.

---

# Compatibilidad Arquitectónica

Las invariantes de Assembly son compatibles con:

* Domain-Driven Design;
* Tactical DDD;
* Clean Architecture;
* Hexagonal Architecture;
* SOLID;
* CQRS;
* Event-Driven Architecture;
* Event Sourcing;
* Optimistic Concurrency;
* arquitectura distribuida;
* consistencia eventual entre Aggregates;
* consistencia fuerte dentro del Aggregate.

La compatibilidad no obliga la adopción de una implementación
física específica.

---

# Principios de Diseño

Las invariantes de Assembly cumplen:

* identidad inmutable;
* propiedad organizacional inmutable;
* estado siempre válido;
* transiciones explícitas;
* denegación por defecto;
* encapsulación mediante Aggregate Root;
* comportamiento semántico;
* ausencia de setters públicos;
* preservación de historia;
* timestamps con significado independiente;
* Version monotónicamente creciente;
* atomicidad dentro del Aggregate;
* consistencia fuerte interna;
* consistencia eventual externa;
* referencias mediante identificadores;
* no absorción de otros Aggregates;
* separación entre autorización y dominio;
* separación entre dominio e infraestructura;
* independencia tecnológica;
* evolución controlada.

---

# Definición de Éxito

Las invariantes del Aggregate **Assembly** constituyen las reglas
normativas que garantizan que toda reunión representada por AURA
permanezca en un estado válido, coherente y consistente durante
todo su ciclo de vida.

Assembly protege permanentemente su identidad, propiedad
organizacional, clasificación, nombre, propósito, estado,
programación, modalidad, ubicación, convocatoria, reglas,
condiciones de realización, información temporal, Version y
límite de consistencia.

Ningún Command, permiso, Application Service, Repository,
integración, Read Model, sistema externo o componente de
Infrastructure puede producir legítimamente un estado que viole
estas reglas.

Las transiciones del Lifecycle permanecen subordinadas a la State
Machine y sus Guards. Los cambios válidos producen un estado
completo y consistente, incrementan Version y registran los
Domain Events correspondientes. Las operaciones rechazadas no
modifican estado, no incrementan Version y no producen eventos de
éxito.

Assembly mantiene consistencia inmediata dentro de su propio
límite y utiliza identificadores, Domain Events, Integration
Events y coordinación externa para relacionarse con Organization,
Territory, Membership, Citizen, Role, Proposal, Participation,
Voting, Document, Notification, Audit e Integration sin absorber
sus responsabilidades.

Los estados terminales preservan la historia del Aggregate:
Cancelled no elimina los hechos anteriores y Archived no
representa eliminación física.

La configuración mediante AssemblyRules y ExecutionConditions no
puede anular las invariantes estructurales. La autorización no
puede convertir una operación inválida en válida. Los sistemas
externos no pueden imponer su semántica sobre el modelo interno.

El lenguaje ubicuo de modalidad permanece:

```text
AssemblyModality
    │
    ▼
ChangeAssemblyModality
    │
    ▼
AssemblyModalityChanged
```

`AssemblyModeChanged` no representa un segundo Domain Event ni un
alias normativo.

De esta forma, las invariantes constituyen la barrera fundamental
que impide representar estados inválidos dentro de Assembly y
preservan la integridad conceptual del Aggregate sin redefinir su
Consistency Boundary ni introducir decisiones de arquitectura.