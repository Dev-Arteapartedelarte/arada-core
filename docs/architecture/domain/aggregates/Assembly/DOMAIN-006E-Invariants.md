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
* Commands Handlers;
* APIs;
* interfaces gráficas;
* adapters;
* servicios externos;
* mecanismos de integración;

pueden mejorar eficiencia o experiencia de usuario, pero nunca
sustituyen las validaciones del dominio.

Una Assembly no debe confiar en que una capa externa ya verificó
una regla cuya protección pertenece al Aggregate.

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

Por ejemplo, si una Assembly es recuperada como:

```text
AssemblyStatus = InProgress

StartedAt = null
```

existe una violación previa de invariantes.

La operación siguiente no debe normalizar silenciosamente el
estado.

La inconsistencia debe ser detectada.

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

sin establecer también las propiedades requeridas por dicho
estado.

El resultado debe mantener simultáneamente:

```text
AssemblyStatus = InProgress

StartedAt != null

Version = PreviousVersion + 1
```

y registrar el Domain Event correspondiente.

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

es una precondición para:

```text
StartAssembly
```

Mientras:

```text
CompletedAt >= StartedAt
```

es una invariante temporal cuando ambos timestamps existen.

Las precondiciones pueden variar entre Commands.

Las invariantes protegen permanentemente la validez del modelo.

---

# Invariantes versus Guards

Los Guards definidos por la State Machine protegen transiciones
específicas.

Ejemplo conceptual:

```text
CanStartAssembly
```

puede comprobar:

```text
Status == Convoked

ConvocationValid == true

ScheduleValid == true

ExecutionConditionsSatisfied == true
```

Las invariantes continúan siendo obligatorias aunque un Guard
haya sido superado.

Un Guard no sustituye una invariante.

Una invariante tampoco sustituye la definición explícita de una
transición dentro de la State Machine.

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

Ejemplo:

un Actor puede poseer:

```text
Assembly.Start
```

pero si:

```text
AssemblyStatus = Draft
```

la operación debe ser rechazada.

La autorización nunca permite violar una invariante.

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

Estas reglas no poseen autoridad para anular invariantes
estructurales del Aggregate.

Una política configurable nunca puede permitir, por ejemplo:

```text
Archived -> InProgress
```

si dicha transición se encuentra prohibida por el modelo oficial.

Las invariantes estructurales poseen precedencia sobre
configuraciones mutables.

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
* no depende de la persistencia;
* no puede reutilizarse.

Una Assembly no puede existir sin AssemblyId.

---

# Inmutabilidad de AssemblyId

Después de crear la Assembly:

```text
AssemblyId(t0) = AssemblyId(t1)
```

para cualquier momento posterior de su existencia.

No está permitido:

```text
ChangeAssemblyId
```

No existe un Command de dominio para modificar AssemblyId.

Ningún Repository, mapper, integración o proceso de migración
funcional puede cambiar silenciosamente la identidad del
Aggregate.

---

# Unicidad de AssemblyId

Dos Aggregates distintos no pueden compartir:

```text
AssemblyId
```

Conceptualmente:

```text
AssemblyA.AssemblyId != AssemblyB.AssemblyId
```

cuando representan reuniones diferentes.

La verificación técnica global puede requerir colaboración con el
Repository, pero la regla de unicidad pertenece al modelo de
dominio.

---

# No Reutilización de Identidad

Una identidad utilizada por una Assembly no puede asignarse
posteriormente a otra Assembly.

Esto continúa siendo válido después de:

```text
Cancelled

Archived
```

El archivado no libera la identidad.

La eliminación física eventual de información, cuando una
política externa la permita, tampoco convierte automáticamente la
identidad en reutilizable.

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

Dos reuniones pueden compartir atributos descriptivos sin
representar el mismo Aggregate.

La identidad permanece independiente del contenido mutable.

---

# Invariante de Organization

Toda Assembly pertenece exactamente a una:

```text
Organization
```

La relación se mantiene mediante:

```text
OrganizationId
```

OrganizationId es obligatorio.

No existe una Assembly válida sin Organization propietaria.

---

# Inmutabilidad de OrganizationId

Una vez creada la Assembly:

```text
OrganizationId
```

no puede cambiar.

Conceptualmente:

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

La Organization asociada constituye parte del contexto
fundamental de Assembly.

Una Assembly creada para:

```text
Organization A
```

no puede convertirse posteriormente en una Assembly de:

```text
Organization B
```

mediante simple modificación de referencia.

Si el dominio requiriera esta capacidad en el futuro deberá
modelarse explícitamente y revisar:

* Aggregate;
* Lifecycle;
* State Machine;
* Commands;
* Domain Events;
* Invariants;
* Permissions;
* Audit;
* Integration Events;
* Read Models.

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

La existencia de la relación no permite modificar Organization
desde Assembly.

---

# Existencia de Organization

Cuando una operación requiera comprobar que Organization existe,
la validación debe realizarse mediante la coordinación externa
correspondiente.

Assembly no consulta directamente:

* OrganizationRepository;
* bases de datos;
* APIs;
* servicios remotos.

La referencia validada puede ser suministrada a la operación sin
expandir el límite del Aggregate.

---

# Coherencia Organizacional de Commands

Para una Assembly existente, el:

```text
OrganizationId
```

incluido en un Command debe corresponder al OrganizationId del
Aggregate.

Conceptualmente:

```text
Command.OrganizationId
=
Assembly.OrganizationId
```

Una discrepancia debe provocar rechazo del contexto de la
operación.

El Command nunca puede utilizar OrganizationId para cambiar la
propiedad de Assembly.

---

# Invariante Territorial

Territory constituye un Aggregate independiente.

Assembly puede mantener:

```text
TerritoryId
```

cuando exista contexto territorial.

TerritoryId puede ser opcional dependiendo de:

* AssemblyType;
* propósito;
* reglas organizacionales;
* naturaleza de la reunión.

Cuando exista debe:

* ser válido;
* representar exclusivamente una referencia;
* no incorporar Territory completo;
* no otorgar a Assembly autoridad sobre Territory.

---

# Independence de Territory

Assembly no puede modificar:

```text
Territory
```

para satisfacer una regla propia.

Si un Territory no cumple una condición necesaria, Assembly debe:

* rechazar la operación; o
* recibir una decisión externa válida;

según corresponda.

Nunca modifica directamente Territory.

---

# TerritoryId versus Location

Debe mantenerse la distinción conceptual entre:

```text
TerritoryId
```

y:

```text
AssemblyLocation
```

TerritoryId representa el contexto territorial.

AssemblyLocation representa el lugar de realización.

No son conceptos equivalentes.

---

# Invariante de Tipo

Toda Assembly debe poseer un:

```text
AssemblyType
```

válido.

Los tipos conceptuales definidos inicialmente son:

```text
Ordinary

Extraordinary

Organizational

Board

Community

Deliberative

Participatory

Territorial

WorkingSession

Consultation
```

No puede utilizarse un valor desconocido sin una extensión formal
del modelo.

---

# Validez de AssemblyType

AssemblyType:

* es obligatorio;
* debe pertenecer al conjunto admitido;
* puede participar en reglas específicas;
* no constituye identidad;
* puede cambiar únicamente mediante comportamiento válido;
* no puede modificarse directamente.

---

# Cambio de AssemblyType

El cambio de tipo solo puede producirse mediante:

```text
ChangeAssemblyType
```

y únicamente cuando:

* el estado lo permita;
* el nuevo tipo sea válido;
* las reglas actuales sean compatibles;
* ExecutionConditions sean compatibles;
* AssemblyModality permanezca válida;
* la convocatoria continúe siendo válida cuando corresponda;
* no se violen invariantes.

Un cambio válido produce:

```text
AssemblyTypeChanged
```

---

# Tipo y Estado Histórico

Una vez que la naturaleza formal de la reunión se encuentre
consolidada por el Lifecycle, AssemblyType no debe modificarse de
forma que reescriba el significado de hechos ya ocurridos.

Por esta razón la mutabilidad de AssemblyType disminuye conforme
avanza el Lifecycle.

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
* debe satisfacer las reglas del Value Object;
* no constituye la identidad del Aggregate.

---

# Cambio de Nombre

AssemblyName puede modificarse únicamente cuando el estado
permita cambios descriptivos.

La modificación debe realizarse mediante:

```text
RenameAssembly
```

Un nombre semánticamente igual al actual no constituye un cambio
real.

Por lo tanto:

```text
CurrentName == NewName
```

no debe producir:

```text
AssemblyRenamed
```

cuando la política oficial considere la operación un No-Op.

---

# Normalización del Nombre

La comparación semántica puede utilizar reglas de normalización
definidas por:

```text
AssemblyName
```

como Value Object.

La normalización no debe destruir información significativa.

La implementación concreta debe permanecer consistente en
creación, modificación y comparación.

---

# Invariante de Propósito

Assembly mantiene:

```text
AssemblyPurpose
```

como propósito formal de la reunión cuando corresponda.

El propósito describe la finalidad de la Assembly.

No representa:

```text
Proposal
```

ni:

```text
Voting
```

ni:

```text
Participation
```

---

# Obligatoriedad del Propósito

AssemblyPurpose puede ser obligatorio según:

* AssemblyType;
* reglas organizacionales;
* etapa del Lifecycle.

Aunque pueda prepararse progresivamente en Draft, antes de
alcanzar un estado que requiera una definición formal completa
debe satisfacer las reglas aplicables.

---

# Cambio de Propósito

ChangeAssemblyPurpose solo puede aceptarse cuando:

* el estado permita el cambio;
* el nuevo propósito sea válido;
* no contradiga AssemblyType;
* no invalide AssemblyRules;
* no reescriba hechos históricos;
* la convocatoria permanezca coherente cuando corresponda.

---

# Invariante de Descripción

Assembly puede mantener:

```text
AssemblyDescription
```

como información contextual complementaria.

Cuando exista debe ser válida según su Value Object.

La ausencia de descripción no invalida por sí misma la Assembly,
salvo que una regla explícita establezca lo contrario.

---

# Description no Sustituye Purpose

Debe mantenerse:

```text
AssemblyDescription != AssemblyPurpose
```

conceptualmente.

Description complementa contexto.

Purpose expresa la finalidad formal de la reunión.

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

No puede existir simultáneamente en múltiples estados.

---

# Estado Único

Debe cumplirse conceptualmente:

```text
count(CurrentStatus) = 1
```

No existe una Assembly:

```text
Scheduled AND Convoked
```

ni:

```text
Completed AND Cancelled
```

El estado representa una única posición del Lifecycle.

---

# Estado Perteneciente al Modelo Oficial

No puede utilizarse un valor como:

```text
Pending

Open

Closed

Deleted

Suspended
```

si no forma parte explícitamente de la versión oficial del
Aggregate.

Estados técnicos, de UI o de integraciones externas no deben
introducirse dentro de AssemblyStatus.

---

# Inmutabilidad Directa del Estado

AssemblyStatus no puede modificarse mediante setter público.

Solo cambia como consecuencia de comportamiento válido.

Ejemplo:

```text
schedule()
```

puede producir:

```text
Draft -> Scheduled
```

pero no se permite:

```text
assembly.status = Scheduled
```

desde fuera del Aggregate.

---

# Invariante de State Machine

Toda transición debe estar expresamente permitida por:

```text
DOMAIN-006B-State-Machine.md
```

Una transición no documentada se considera inválida.

La ausencia de una prohibición explícita no convierte una
transición en válida.

---

# Denegación por Defecto

Debe aplicarse:

```text
deny by default
```

para transiciones de estado.

Solo puede ejecutarse una transición cuando el modelo la define
expresamente como válida.

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

No se permiten transiciones que omitan estados requeridos.

Ejemplos inválidos:

```text
Draft -> Convoked

Draft -> InProgress

Draft -> Completed

Scheduled -> InProgress

Scheduled -> Completed

Convoked -> Completed
```

Cada transición debe respetar la State Machine.

---

# Prohibición de Retroceso Implícito

No se permite regresar arbitrariamente a estados anteriores.

Ejemplos:

```text
InProgress -> Convoked

Completed -> InProgress

Cancelled -> Scheduled

Archived -> Completed
```

Una futura capacidad de reapertura requerirá modelado explícito.

---

# Invariante de Draft

Una Assembly en:

```text
Draft
```

representa una reunión creada pero todavía no programada
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

Puede contener información adicional válida.

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

además de modificaciones configuracionales autorizadas.

---

# Draft no Requiere Ejecución Completa

Una Assembly Draft puede encontrarse todavía en preparación.

Por ello determinados conceptos pueden ser incompletos mientras
las invariantes de creación lo permitan.

Sin embargo, Draft nunca permite ausencia de:

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

Una Assembly en:

```text
Scheduled
```

debe poseer programación formal válida.

Debe existir:

```text
ScheduledStartAt
```

y, cuando corresponda:

```text
ScheduledEndAt
```

Debe existir una modalidad válida.

La ubicación debe satisfacer las reglas correspondientes a la
modalidad.

---

# Scheduled Requiere Programación

No puede existir:

```text
AssemblyStatus = Scheduled
```

con:

```text
ScheduledStartAt = null
```

La transición:

```text
Draft -> Scheduled
```

solo puede completarse cuando la programación sea válida.

---

# Scheduled no Significa Convoked

Debe mantenerse:

```text
Scheduled != Convoked
```

Una Assembly puede poseer programación formal sin haber sido aún
formalmente convocada.

No debe establecerse ConvokedAt únicamente por programar.

---

# Scheduled no Significa Started

Debe mantenerse:

```text
Scheduled != InProgress
```

El paso del tiempo no convierte automáticamente una Assembly
Scheduled en InProgress.

---

# Invariante de Convoked

Una Assembly en:

```text
Convoked
```

debe haber sido previamente:

```text
Scheduled
```

y debe poseer una convocatoria formal válida.

Debe existir:

```text
ConvokedAt
```

La programación requerida debe continuar siendo válida.

---

# Convoked Requiere Convocatoria

No puede existir:

```text
AssemblyStatus = Convoked
```

con:

```text
ConvokedAt = null
```

La convocatoria es un hecho formal requerido para dicho estado.

---

# Convoked no Significa Notificado

Debe mantenerse la separación:

```text
Convoked
```

no significa necesariamente:

```text
NotificationDelivered
```

Assembly representa la condición formal de convocatoria.

Notification mantiene su propio ciclo de vida.

---

# Convoked no Significa InProgress

Una Assembly convocada no se considera iniciada hasta que se
ejecute una transición válida:

```text
Convoked -> InProgress
```

Debe existir:

```text
StartAssembly
```

y el hecho:

```text
AssemblyStarted
```

---

# Invariante de InProgress

Una Assembly en:

```text
InProgress
```

debe haber iniciado formalmente.

Debe existir:

```text
StartedAt
```

Debe provenir de:

```text
Convoked
```

en la versión 1.0.

---

# InProgress Requiere Inicio

No puede existir:

```text
AssemblyStatus = InProgress
```

con:

```text
StartedAt = null
```

La hora programada no sustituye StartedAt.

---

# InProgress no Permite Reescritura Estructural

Una Assembly InProgress representa una reunión que ya comenzó.

Por tanto, modificaciones estructurales que alterarían el
significado de la reunión deben quedar restringidas.

No puede modificarse ordinariamente:

```text
AssemblyId

OrganizationId

AssemblyType

Schedule

Convocation
```

cuando ello reescriba hechos ya ocurridos.

---

# Invariante de Completed

Una Assembly en:

```text
Completed
```

debe haber sido previamente:

```text
InProgress
```

Debe poseer:

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
```

sin:

```text
StartedAt
```

Una reunión no puede completarse si nunca comenzó formalmente.

---

# Completed Requiere Finalización

Debe existir:

```text
CompletedAt
```

cuando:

```text
AssemblyStatus = Completed
```

Además:

```text
CompletedAt >= StartedAt
```

---

# Completed no Significa Archived

Debe mantenerse:

```text
Completed != Archived
```

Completed representa que la reunión terminó.

Archived representa que la reunión salió posteriormente del ciclo
operativo.

---

# Completed es Operativamente Cerrado

Después de Completed no deben permitirse Commands que intenten
continuar o reescribir la realización normal.

No se permite:

```text
StartAssembly

CompleteAssembly

CancelAssembly
```

desde Completed.

---

# Invariante de Cancelled

Una Assembly Cancelled representa una reunión cuyo flujo normal
fue cancelado antes de alcanzar Completion.

En la versión 1.0 puede provenir de:

```text
Draft

Scheduled

Convoked
```

No puede provenir de:

```text
Completed

Archived
```

---

# Cancelled Requiere CancelledAt

Cuando:

```text
AssemblyStatus = Cancelled
```

debe existir:

```text
CancelledAt
```

El timestamp representa el momento en que la cancelación se
convirtió en un hecho del dominio.

---

# Cancelled es Terminal Operativo

Después de:

```text
AssemblyStatus = Cancelled
```

no puede continuar mediante:

```text
ScheduleAssembly

ConvokeAssembly

StartAssembly

CompleteAssembly
```

El único cambio ordinario de Lifecycle permitido es:

```text
Cancelled -> Archived
```

---

# Preservación Histórica al Cancelar

La cancelación no elimina hechos anteriores.

Si existía:

```text
ScheduledStartAt
```

permanece.

Si existía:

```text
ConvokedAt
```

permanece.

La cancelación agrega un hecho nuevo.

No modifica retroactivamente los hechos anteriores.

---

# Cancelled no Representa Interruption

La versión 1.0 no utiliza:

```text
Cancelled
```

para representar una reunión que comenzó y posteriormente fue
interrumpida.

Una interrupción posterior al inicio requiere un concepto
diferente.

No debe reutilizarse Cancelled para introducir implícitamente:

```text
Interrupted

Suspended

Aborted
```

---

# Invariante de Archived

Archived constituye el estado terminal oficial.

Una Assembly Archived no puede modificarse mediante operaciones
ordinarias.

Debe cumplirse:

```text
AssemblyStatus = Archived

ArchivedAt != null
```

---

# Estados Permitidos para Archivar

En la versión 1.0 solo pueden archivarse:

```text
Completed

Cancelled
```

No puede ejecutarse:

```text
Draft -> Archived

Scheduled -> Archived

Convoked -> Archived

InProgress -> Archived
```

---

# Archived es Inmutable

Después de archivar no se permite:

```text
RenameAssembly

ChangeAssemblyType

ChangeAssemblyPurpose

ChangeAssemblyDescription

RescheduleAssembly

ChangeAssemblyModality

ChangeAssemblyLocation

UpdateAssemblyConvocation

UpdateAssemblyRules

UpdateAssemblyExecutionConditions

StartAssembly

CompleteAssembly

CancelAssembly
```

No existen modificaciones funcionales ordinarias posteriores.

---

# Archived no Significa Deleted

Archived representa:

```text
historical terminal state
```

No representa necesariamente:

```text
physical deletion
```

La Assembly conserva identidad e historia dentro del modelo.

---

# Invariante Temporal General

Toda información temporal debe mantener coherencia cronológica.

Los timestamps relevantes incluyen:

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

Cada timestamp posee significado propio y debe ser compatible con
el Lifecycle.

---

# CreatedAt

Toda Assembly debe poseer:

```text
CreatedAt
```

CreatedAt:

* es obligatorio;
* se establece una sola vez;
* es inmutable;
* representa el momento de creación del Aggregate.

---

# CreatedAt y Estados Posteriores

CreatedAt debe conservarse durante toda la existencia de la
Assembly.

Ninguna transición elimina o reemplaza CreatedAt.

---

# Invariante de Programación

Cuando exista:

```text
ScheduledStartAt
```

debe representar una fecha y hora válidas.

Cuando exista:

```text
ScheduledEndAt
```

debe cumplirse:

```text
ScheduledEndAt > ScheduledStartAt
```

No se permite una programación con duración negativa o nula
cuando ScheduledEndAt se encuentra definido.

---

# ScheduledStartAt Obligatorio

ScheduledStartAt es obligatorio para:

```text
Scheduled

Convoked

InProgress
```

y debe preservarse históricamente en estados posteriores cuando
la Assembly haya atravesado programación.

---

# ScheduledEndAt Opcional

Si el dominio permite duración abierta:

```text
ScheduledEndAt = null
```

puede ser válido.

Sin embargo:

```text
ScheduledStartAt
```

continúa siendo obligatorio para una Assembly programada.

---

# Igualdad de Inicio y Fin Programado

La versión 1.0 considera inválido:

```text
ScheduledEndAt = ScheduledStartAt
```

cuando ScheduledEndAt se encuentre definido.

Una programación con período explícito debe poseer duración
positiva.

---

# Programación en el Pasado

La validez de programar una Assembly con:

```text
ScheduledStartAt < CurrentTime
```

debe estar determinada por la política temporal oficial del
dominio.

No debe inferirse desde infraestructura.

Si se prohíbe, la regla debe aplicarse de forma determinista y
consistente.

---

# TimeZone

Toda programación debe interpretarse en un contexto temporal no
ambiguo.

Cuando la arquitectura utilice:

```text
TimeZone
```

este debe ser válido.

No debe mantenerse una hora local ambigua sin información
suficiente para interpretar correctamente su significado.

---

# Invariante de Reprogramación

RescheduleAssembly debe producir una nueva programación válida.

No puede modificar:

```text
CreatedAt

StartedAt

CompletedAt

CancelledAt

ArchivedAt
```

La reprogramación modifica planificación.

No modifica hechos históricos ya ocurridos.

---

# Reprogramación de Assembly Convoked

Cuando una Assembly Convoked sea reprogramada, la operación debe
preservar consistencia entre:

```text
Schedule

Convocation
```

Si la nueva programación invalida la convocatoria existente,
Assembly debe exigir la actualización necesaria o rechazar la
operación.

No puede quedar:

```text
AssemblyStatus = Convoked
```

con una convocatoria incompatible con la nueva programación.

---

# Preservación del Schedule Histórico

Una reprogramación no debe sobrescribir el hecho histórico sin
trazabilidad.

El cambio debe producir:

```text
AssemblyRescheduled
```

con información suficiente para distinguir:

```text
PreviousSchedule

NewSchedule
```

según el contrato oficial del evento.

---

# Invariante de ConvokedAt

Cuando exista:

```text
ConvokedAt
```

representa el momento real de convocatoria.

No puede eliminarse posteriormente para fingir que la
convocatoria nunca ocurrió.

Una actualización posterior de Convocation debe preservar el
hecho histórico original.

---

# Invariante de StartedAt

StartedAt solo puede establecerse mediante una transición válida:

```text
Convoked -> InProgress
```

Una vez establecido:

```text
StartedAt
```

representa un hecho histórico.

No debe modificarse mediante operaciones descriptivas o de
configuración.

---

# Inicio Programado versus Inicio Real

Debe mantenerse la distinción:

```text
ScheduledStartAt
```

representa:

```text
inicio planificado
```

Mientras:

```text
StartedAt
```

representa:

```text
inicio efectivo
```

No existe una invariante que obligue a que ambos sean iguales.

---

# Inicio Real Posterior al Programado

Una Assembly puede iniciar posteriormente a la hora programada.

Ejemplo válido:

```text
ScheduledStartAt = 18:00

StartedAt = 18:17
```

Esto no viola por sí mismo la consistencia del Aggregate.

Representa una diferencia entre planificación y ejecución real.

---

# Inicio Real Anterior al Programado

La posibilidad de:

```text
StartedAt < ScheduledStartAt
```

debe depender de reglas explícitas del dominio.

No debe decidirse accidentalmente por la implementación.

Cuando la política lo prohíba, StartAssembly debe rechazar el
inicio anticipado.

---

# Invariante de CompletedAt

CompletedAt solo puede establecerse mediante:

```text
InProgress -> Completed
```

Debe cumplirse:

```text
CompletedAt >= StartedAt
```

Una vez establecido no puede modificarse mediante operaciones
ordinarias.

---

# Fin Programado versus Fin Real

Debe mantenerse la distinción:

```text
ScheduledEndAt
```

representa:

```text
finalización planificada
```

Mientras:

```text
CompletedAt
```

representa:

```text
finalización efectiva
```

No existe una obligación general de igualdad entre ambos.

---

# Invariante de CancelledAt

Cuando:

```text
AssemblyStatus = Cancelled
```

debe existir:

```text
CancelledAt
```

CancelledAt representa el momento real de cancelación.

No reemplaza:

```text
ScheduledStartAt

ConvokedAt
```

cuando estos hechos existieron anteriormente.

---

# Invariante de ArchivedAt

Cuando:

```text
AssemblyStatus = Archived
```

debe existir:

```text
ArchivedAt
```

Debe ser temporalmente compatible con el estado anterior.

Para una Assembly Completed:

```text
ArchivedAt >= CompletedAt
```

Para una Assembly Cancelled:

```text
ArchivedAt >= CancelledAt
```

---

# Coherencia Temporal de Lifecycle

Cuando los timestamps correspondientes existan deben preservarse
relaciones cronológicas compatibles.

Conceptualmente:

```text
CreatedAt <= ConvokedAt
```

cuando ConvokedAt exista.

También:

```text
StartedAt <= CompletedAt
```

para una Assembly completada.

Y:

```text
CompletedAt <= ArchivedAt
```

para una Assembly archivada desde Completed.

---

# Coherencia Temporal de Cancelación

Para una Assembly cancelada:

```text
CreatedAt <= CancelledAt
```

Debe cumplirse además:

```text
CancelledAt <= ArchivedAt
```

cuando posteriormente alcance Archived.

---

# Invariante de Modalidad

Toda Assembly que alcance:

```text
Scheduled
```

debe poseer:

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

No puede utilizarse una modalidad desconocida sin extensión
formal del dominio.

---

# Invariante InPerson

Cuando:

```text
AssemblyModality = InPerson
```

debe existir una ubicación válida cuando las reglas de la
Organization, AssemblyType o AssemblyRules así lo requieran.

La Location debe ser compatible con realización presencial.

---

# Invariante Remote

Cuando:

```text
AssemblyModality = Remote
```

la ubicación física puede ser opcional.

Assembly no administra:

* plataforma de videoconferencia;
* enlaces de acceso;
* credenciales;
* sesiones;
* tokens;
* infraestructura remota.

Estos conceptos permanecen fuera del Aggregate.

---

# Invariante Hybrid

Cuando:

```text
AssemblyModality = Hybrid
```

las condiciones deben ser compatibles con participación
presencial y remota.

La modalidad no convierte servicios tecnológicos externos en
entidades internas del Aggregate.

---

# Cambio de Modalidad

ChangeAssemblyModality solo puede aceptarse cuando:

* el estado permita cambios;
* la nueva modalidad sea válida;
* Location permanezca compatible;
* AssemblyRules permanezcan válidas;
* ExecutionConditions permanezcan válidas;
* Convocation permanezca consistente cuando corresponda.

---

# Modalidad y Estado

La capacidad de cambiar modalidad disminuye conforme avanza el
Lifecycle.

Una modalidad utilizada durante una reunión ya iniciada no debe
reescribirse arbitrariamente después del hecho.

---

# Invariante de Location

AssemblyLocation pertenece al contexto de la reunión.

No representa:

```text
Territory
```

ni sustituye:

```text
TerritoryId
```

Location debe ser compatible con AssemblyModality.

---

# Validación de Location

Cuando Location sea obligatoria debe ser:

* estructuralmente válida;
* semánticamente válida;
* compatible con la modalidad;
* compatible con las reglas de Assembly.

Una Location inválida debe provocar rechazo de la operación que
la introduce.

---

# Cambio de Location

ChangeAssemblyLocation debe preservar:

* identidad;
* Organization;
* modalidad;
* convocatoria;
* estado;
* historicidad.

Cuando Assembly ya está Convoked, el cambio puede exigir
actualización de Convocation.

---

# Cambio de Location durante InProgress

La modificación de Location durante InProgress solo puede
permitirse cuando representa un cambio real ocurrido durante la
reunión y el modelo lo autoriza explícitamente.

No debe utilizarse para reescribir retroactivamente dónde comenzó
la Assembly.

La trazabilidad del cambio debe preservarse mediante Domain
Events.

---

# Invariante de Convocation

La convocatoria formal debe ser coherente con:

* Organization;
* Assembly;
* programación;
* tipo;
* modalidad;
* ubicación;
* reglas;
* estado;
* plazos aplicables.

Una Assembly no puede alcanzar:

```text
Convoked
```

sin una Convocation válida.

---

# ConvocationStatus

ConvocationStatus debe ser coherente con AssemblyStatus.

No puede existir una combinación conceptualmente
contradictoria.

Ejemplo inválido:

```text
AssemblyStatus = Draft

ConvocationStatus = FormallyConvoked
```

cuando el Lifecycle exige una programación previa.

---

# ConvocationDate

ConvocationDate debe representar una fecha válida asociada a la
convocatoria.

No debe utilizarse para sustituir:

```text
ConvokedAt
```

si ambos conceptos poseen significado distinto dentro del modelo.

---

# ConvocationDeadline

Cuando exista:

```text
ConvocationDeadline
```

debe ser temporalmente coherente con:

```text
ScheduledStartAt
```

No puede representar un plazo incompatible con las reglas de
convocatoria.

---

# ConvocationMethod

ConvocationMethod debe pertenecer al conjunto permitido por el
modelo o por sus extensiones oficiales.

El método formal de convocatoria no implica que Assembly
implemente físicamente el mecanismo de comunicación.

---

# ConvocationReference

Cuando exista:

```text
ConvocationReference
```

debe ser una referencia válida.

No debe utilizarse para introducir un Document completo dentro de
Assembly.

---

# ConvocationRules

Las reglas de convocatoria deben encontrarse satisfechas antes de
producir:

```text
AssemblyConvoked
```

No basta con que un Command solicite la convocatoria.

Assembly debe validar las condiciones internas que le
corresponden.

---

# Convocation versus Notification

La validez de Convocation no convierte Notification en parte del
Aggregate.

Assembly mantiene la condición formal de convocatoria.

Notification administra el proceso de comunicación.

Por lo tanto:

```text
AssemblyConvoked
```

no implica necesariamente:

```text
NotificationDelivered
```

dentro de la misma transacción.

---

# Fallo de Notification

Si posteriormente falla la comunicación de una Notification, el
hecho:

```text
AssemblyConvoked
```

no deja de ser verdadero.

El manejo del fallo corresponde al contexto responsable de
Notification.

Assembly no revierte silenciosamente la convocatoria.

---

# Invariante de AssemblyRules

AssemblyRules representan reglas propias de la reunión.

Deben:

* pertenecer conceptualmente a Assembly;
* ser válidas;
* ser compatibles con AssemblyType;
* ser compatibles con AssemblyModality;
* ser compatibles con ExecutionConditions;
* no contradecir invariantes estructurales;
* no otorgar autoridad sobre otros Aggregates;
* no introducir dependencias tecnológicas.

---

# AssemblyRules Configurables

Las reglas configurables pueden variar entre Assemblies.

Ejemplos conceptuales:

```text
QuorumRequired

RemoteParticipationAllowed

PublicParticipationAllowed

ProposalSubmissionAllowed

VotingAllowed

RecordingAllowed
```

La existencia de estas reglas no implica que Assembly absorba los
Aggregates correspondientes.

---

# AssemblyRules y Proposal

Una regla:

```text
ProposalSubmissionAllowed
```

puede expresar si la reunión permite procesos de Proposal.

No convierte:

```text
Proposal
```

en una entidad interna de Assembly.

---

# AssemblyRules y Voting

Una regla:

```text
VotingAllowed
```

puede expresar si la reunión admite procesos de Voting.

No convierte Voting en parte del límite de consistencia de
Assembly.

---

# Reglas no Pueden Anular Invariantes

Una AssemblyRule nunca puede declarar válido algo prohibido por
una invariante fundamental.

Ejemplo:

una regla configurable no puede permitir:

```text
Archived -> InProgress
```

si la State Machine oficial lo prohíbe.

---

# Cambio de AssemblyRules

UpdateAssemblyRules debe garantizar que las nuevas reglas:

* sean válidas;
* sean coherentes entre sí;
* sean compatibles con AssemblyType;
* sean compatibles con AssemblyModality;
* sean compatibles con ExecutionConditions;
* puedan modificarse en el estado vigente;
* no reescriban hechos históricos.

---

# Invariantes de ExecutionConditions

ExecutionConditions representan requisitos propios de la
realización de la Assembly.

Deben:

* ser evaluables;
* pertenecer al contexto de Assembly;
* no modificar otros Aggregates;
* ser coherentes con AssemblyType;
* ser coherentes con AssemblyModality;
* ser coherentes con AssemblyRules;
* encontrarse satisfechas antes de StartAssembly cuando sean
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

La inclusión de una condición dentro de Assembly debe respetar el
Consistency Boundary oficial.

---

# RequiredQuorum

Cuando el quórum forme parte de las condiciones propias de la
reunión, Assembly puede exigir una decisión válida sobre su
satisfacción antes del inicio.

Esto no obliga a Assembly a administrar:

* Citizen;
* Membership;
* Participation;

como entidades internas.

---

# Dependencias Externas para Validación

Algunas reglas pueden necesitar información que pertenece a otros
Aggregates.

Ejemplo:

```text
Membership is active
```

Assembly no debe cargar ni modificar Membership internamente para
validarlo.

La información o decisión necesaria debe ser coordinada fuera del
Aggregate.

---

# Snapshot de Decisión

Cuando una decisión dependa de información externa, debe evitarse
mantener referencias mutables hacia el Aggregate externo.

Puede utilizarse conceptualmente una decisión validada como:

```text
EligibilityDecision

AuthorizationDecision

ValidatedReference

QuorumDecision
```

cuando el diseño formal lo requiera.

La forma concreta deberá quedar documentada antes de su
implementación.

---

# Invariantes de Realización

Antes de iniciar una Assembly deben encontrarse satisfechas las
condiciones de realización definidas por el dominio.

Como mínimo:

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

StartAssembly solo puede aceptarse cuando:

```text
AssemblyStatus = Convoked
```

y todos los Guards e invariantes aplicables sean verdaderos.

Resultado:

```text
AssemblyStatus = InProgress

StartedAt != null
```

Evento:

```text
AssemblyStarted
```

---

# Prohibición de Inicio Automático

El paso del tiempo no cambia automáticamente:

```text
Scheduled
```

o:

```text
Convoked
```

a:

```text
InProgress
```

Debe existir comportamiento explícito del dominio.

Por lo tanto:

```text
CurrentTime >= ScheduledStartAt
```

no implica:

```text
AssemblyStatus = InProgress
```

---

# Inicio y Permisos

Incluso si todas las invariantes para iniciar están satisfechas,
StartAssembly puede requerir autorización.

Debe cumplirse:

```text
Domain Validity
```

y separadamente:

```text
Authorization
```

La ausencia de permiso rechaza la intención.

La existencia del permiso no elimina las invariantes.

---

# Invariante de Finalización

CompleteAssembly solo puede ejecutarse desde:

```text
InProgress
```

El resultado debe ser:

```text
Completed
```

con:

```text
CompletedAt != null
```

y:

```text
CompletedAt >= StartedAt
```

---

# Finalización no Automática

El paso del tiempo no produce automáticamente Completion.

Por lo tanto:

```text
CurrentTime >= ScheduledEndAt
```

no implica:

```text
AssemblyStatus = Completed
```

La finalización requiere comportamiento explícito.

---

# Finalización no Archiva

Debe mantenerse:

```text
Completed != Archived
```

CompleteAssembly no produce automáticamente:

```text
Archived
```

El archivado constituye una transición posterior y explícita.

---

# Finalización no Modifica Otros Aggregates

AssemblyCompleted no puede modificar directamente:

```text
Proposal

Participation

Voting

Document

Notification

Audit
```

Si dichos procesos deben reaccionar lo hacen mediante coordinación
externa y consistencia eventual.

---

# Invariante de Cancelación

CancelAssembly solo puede ejecutarse desde estados permitidos.

Versión 1.0:

```text
Draft

Scheduled

Convoked
```

La cancelación debe producir:

```text
AssemblyStatus = Cancelled

CancelledAt != null
```

---

# CancellationReason

Cuando las reglas exijan:

```text
CancellationReason
```

este debe ser válido.

El motivo no puede estar vacío cuando sea obligatorio.

Debe formar parte del hecho histórico de cancelación cuando el
modelo así lo determine.

---

# Cancelación desde InProgress

La versión 1.0 no permite:

```text
InProgress -> Cancelled
```

La interrupción de una reunión iniciada representa una semántica
diferente y requiere modelado explícito.

No debe utilizarse Cancelled para incorporar esa capacidad
implícitamente.

---

# Cancelación no Elimina la Assembly

CancelAssembly no destruye el Aggregate.

La Assembly conserva:

* AssemblyId;
* OrganizationId;
* programación histórica;
* convocatoria histórica;
* Version;
* timestamps anteriores;
* Domain Events;
* trazabilidad.

---

# Cancelación no Revierte Domain Events

Si previamente ocurrió:

```text
AssemblyScheduled
```

y luego:

```text
AssemblyConvoked
```

una cancelación posterior agrega:

```text
AssemblyCancelled
```

No elimina los eventos anteriores.

---

# Invariante de Archivado

ArchiveAssembly solo puede ejecutarse desde:

```text
Completed

Cancelled
```

Debe producir:

```text
AssemblyStatus = Archived

ArchivedAt != null
```

Después de la transición el Aggregate es inmutable para
operaciones ordinarias.

---

# ArchiveReason

Cuando el dominio requiera:

```text
ArchiveReason
```

el valor debe ser válido.

El motivo no reemplaza el estado anterior ni elimina información
histórica.

---

# Archivado no es Eliminación

Archived representa una condición del dominio.

No representa:

```text
DELETE FROM assembly
```

ni:

```text
physical deletion
```

La política física de retención pertenece a Infrastructure y a la
gobernanza de datos.

---

# Invariantes de Referencias Externas

Assembly puede relacionarse con otros Aggregates mediante
identificadores.

Ejemplos:

```text
OrganizationId

TerritoryId

MembershipId

CitizenId

ProposalId

ParticipationId

VotingId

DocumentId

NotificationId

AuditId
```

Las referencias no convierten dichos Aggregates en entidades
internas.

---

# Regla de Referencia por Identidad

Cuando Assembly necesite identificar otro Aggregate debe
utilizar:

```text
AggregateId
```

y no:

```text
MutableAggregateReference
```

No debe conservar una referencia mutable hacia otro Aggregate.

---

# Regla de No Absorción

Assembly no puede incorporar dentro de su límite:

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

como Aggregates completos.

La relación contextual no modifica sus límites de consistencia.

---

# Invariante de Membership

Una referencia a Membership no permite:

* activar Membership;
* suspender Membership;
* terminar Membership;
* modificar OrganizationId;
* cambiar su Lifecycle.

Estas responsabilidades permanecen en Membership.

---

# Invariante de Citizen

Una referencia a Citizen no permite:

* modificar identidad;
* modificar información personal;
* cambiar estado;
* administrar credenciales;
* modificar preferencias.

Citizen permanece fuera de Assembly.

---

# Invariante de Role

Role permanece fuera del límite del Aggregate.

Assembly no puede:

* crear Roles;
* modificar Roles;
* archivar Roles;
* asignar Roles a Memberships.

La autorización relacionada con Roles se resuelve mediante los
mecanismos correspondientes fuera de Assembly.

---

# Invariante de Proposal

Una Proposal asociada a Assembly mantiene:

* ProposalId;
* identidad propia;
* Lifecycle propio;
* invariantes propias;
* Repository propio;
* Domain Events propios.

Assembly no modifica Proposal directamente.

---

# Invariante de Participation

Participation mantiene su propio límite de consistencia.

Assembly puede proporcionar contexto mediante:

```text
AssemblyId
```

pero no absorbe Participation.

---

# Invariante de Voting

Voting mantiene:

* VotingId;
* reglas;
* estado;
* Lifecycle;
* votos;
* resultados;
* invariantes;

fuera de Assembly.

Una Voting realizada durante una Assembly no se convierte en una
entidad interna de Assembly.

---

# Invariante de Document

Document mantiene su propio contenido y ciclo de vida.

Assembly puede mantener:

```text
DocumentId
```

cuando corresponda.

No almacena el Aggregate Document completo.

---

# Invariante de Notification

Notification no forma parte de Assembly.

Assembly puede producir hechos como:

```text
AssemblyConvoked

AssemblyRescheduled

AssemblyCancelled
```

que posteriormente originen Notifications.

El fallo de Notification no invalida retroactivamente un hecho de
Assembly ya aceptado.

---

# Invariante de Audit

Audit consume hechos relevantes.

Assembly no mantiene una colección mutable de:

```text
Audit
```

dentro de su límite.

La trazabilidad interna se mantiene mediante:

* Version;
* timestamps;
* Domain Events;
* ActorId cuando corresponda;
* CorrelationId;
* CausationId.

---

# Invariante de Integration

Integration permanece fuera del Aggregate.

Assembly no contiene:

* clientes HTTP;
* adapters FIWARE;
* SDKs externos;
* brokers;
* credenciales;
* conexiones;
* endpoints.

La integración ocurre después de los hechos internos mediante
contratos externos.

---

# Invariante de Consistency Boundary

Assembly constituye un único límite de consistencia.

Toda operación debe dejar internamente consistente:

```text
Identity

Organization

TerritoryReference

Type

Name

Purpose

Description

Schedule

Modality

Location

Convocation

AssemblyRules

ExecutionConditions

Status

Timestamps

Version

PendingDomainEvents
```

cuando dichos conceptos formen parte del estado vigente.

---

# Atomicidad Conceptual

Una modificación válida debe aplicarse como una única unidad de
consistencia.

No puede quedar:

```text
Status = InProgress

StartedAt = null
```

después de StartAssembly.

Tampoco:

```text
Status = Archived

ArchivedAt = null
```

después de ArchiveAssembly.

---

# Prohibición de Estado Parcial

Si una operación requiere modificar múltiples propiedades
internas, todas deben quedar coherentes.

Ejemplo:

```text
StartAssembly
```

debe producir conceptualmente:

```text
Status = InProgress

StartedAt = Timestamp

UpdatedAt = Timestamp

Version = Version + 1

AssemblyStarted
```

No se acepta una actualización parcial.

---

# Rollback Conceptual

Cuando una operación no puede completarse preservando todas las
invariantes, ninguna de sus modificaciones debe formar parte del
estado final aceptado.

Conceptualmente:

```text
all changes
```

o:

```text
no changes
```

dentro del límite de consistencia.

---

# Consistencia entre Aggregates

Assembly no exige una transacción distribuida con otros
Aggregates.

La coordinación se realiza mediante:

```text
Domain Events

Integration Events

Application Services

Domain Policies

Repositories
```

y consistencia eventual cuando corresponda.

---

# Prohibición de Transacción Distribuida Implícita

Un Command de Assembly no puede asumir que la modificación de
Assembly y la modificación de:

```text
Voting

Proposal

Participation

Notification

Document
```

deben confirmarse atómicamente dentro de la misma transacción del
Aggregate.

Cada Aggregate conserva su propio límite.

---

# Invariante de Version

Toda Assembly posee:

```text
Version
```

Version representa la evolución válida del Aggregate.

Debe ser:

* obligatoria;
* válida;
* monotónicamente creciente;
* controlada conforme a la política de Versioning;
* no modificable arbitrariamente desde fuera.

---

# Inicialización de Version

Al crear Assembly debe establecerse una versión inicial
consistente con:

```text
DOMAIN-006I-Versioning.md
```

La elección del valor inicial debe mantenerse uniforme en toda la
arquitectura.

---

# Incremento de Version

Toda modificación semánticamente válida del Aggregate incrementa
Version.

Conceptualmente:

```text
Version(n + 1) = Version(n) + 1
```

conforme a la política oficial.

---

# No Incremento en Operación Rechazada

Si un Command es rechazado:

```text
VersionAfter = VersionBefore
```

No debe publicarse un Domain Event de éxito.

---

# No Incremento por Lectura

Las operaciones de consulta no modifican:

```text
Version
```

Una Query nunca representa evolución del Aggregate.

---

# No-Op

Una operación que no produce cambio semántico puede tratarse como
No-Op.

Ejemplo:

```text
CurrentName = NewName
```

En ese caso:

```text
VersionAfter = VersionBefore
```

y no se produce:

```text
AssemblyRenamed
```

La política debe aplicarse consistentemente en todo el Aggregate.

---

# Invariante de Concurrencia

El Repository debe impedir que una modificación basada en una
versión obsoleta sobrescriba una versión más reciente.

Conceptualmente:

```text
ExpectedVersion == PersistedVersion
```

debe cumplirse antes de aceptar la persistencia de una nueva
versión.

---

# Conflicto de Concurrencia

Si:

```text
ExpectedVersion != PersistedVersion
```

la modificación debe rechazarse.

No se permite:

```text
last write wins
```

como comportamiento silencioso para cambios del Aggregate.

---

# Revalidación después de Conflicto

Después de un conflicto de concurrencia no basta con actualizar
ExpectedVersion y repetir automáticamente la operación.

Debe:

* recuperarse la versión actual;
* reevaluarse AssemblyStatus;
* reevaluarse la intención;
* reevaluarse autorización;
* reevaluarse Guards;
* reevaluarse invariantes.

El dominio debe decidir nuevamente si la operación continúa siendo
válida.

---

# Invariantes de Domain Events

Todo cambio válido que represente un hecho relevante debe producir
el Domain Event correspondiente.

Ejemplo:

```text
Draft -> Scheduled
```

produce:

```text
AssemblyScheduled
```

Mientras:

```text
Convoked -> InProgress
```

produce:

```text
AssemblyStarted
```

---

# Evento después de Estado Válido

Un Domain Event solo puede registrarse después de que la operación
haya producido un estado válido.

Conceptualmente:

```text
Validate
    ↓
Mutate
    ↓
Validate Result
    ↓
Record Domain Event
```

No debe registrarse un evento de éxito antes de comprobar la
consistencia resultante.

---

# No Event on Failure

Si una invariante falla:

```text
Command Rejected

State Unchanged

Version Unchanged

No Success Domain Event
```

Esta regla es obligatoria.

---

# Inmutabilidad de Eventos

Un Domain Event producido representa un hecho histórico.

No puede modificarse posteriormente para ocultar o reinterpretar
un estado anterior.

Si ocurre un nuevo hecho se produce un nuevo Domain Event.

---

# AggregateVersion del Evento

Todo Domain Event debe asociarse a la versión resultante de
Assembly.

Ejemplo:

```text
VersionBefore = 7

StartAssembly accepted

VersionAfter = 8

AssemblyStarted.AggregateVersion = 8
```

---

# Evento Coherente con el Estado

No puede producirse:

```text
AssemblyStarted
```

si el estado resultante no es:

```text
InProgress
```

Tampoco:

```text
AssemblyCompleted
```

si el estado resultante no es:

```text
Completed
```

Event y State deben permanecer semánticamente coherentes.

---

# Invariantes de Commands

Todo Command que modifique Assembly debe:

* expresar una intención explícita;
* dirigirse a la Assembly correspondiente;
* ser evaluado contra el estado actual;
* respetar Guards;
* respetar las invariantes;
* respetar la State Machine;
* no modificar otros Aggregates;
* no producir cambios parciales.

---

# CreateAssembly

CreateAssembly debe producir inicialmente una Assembly válida.

Como mínimo:

```text
AssemblyId != null

OrganizationId != null

AssemblyName valid

AssemblyType valid

AssemblyStatus = Draft

CreatedAt != null

Version valid
```

Si alguna condición falla, la Assembly no debe crearse.

---

# CreateAssembly y Estado Inicial

No puede crearse directamente una Assembly en:

```text
Scheduled

Convoked

InProgress

Completed

Cancelled

Archived
```

Toda Assembly comienza en:

```text
Draft
```

---

# ScheduleAssembly

ScheduleAssembly debe validar:

```text
CurrentStatus = Draft

ScheduledStartAt valid

ScheduledEndAt > ScheduledStartAt
    when ScheduledEndAt exists

AssemblyModality valid

Location valid when required

Schedule rules satisfied
```

Resultado:

```text
Status = Scheduled
```

---

# RescheduleAssembly

RescheduleAssembly debe:

* ejecutarse únicamente desde estados permitidos;
* mantener programación válida;
* preservar timestamps históricos;
* mantener coherencia con Convocation;
* no alterar AssemblyId;
* no alterar OrganizationId;
* incrementar Version cuando exista cambio real;
* producir AssemblyRescheduled.

---

# ConvokeAssembly

ConvokeAssembly debe validar:

```text
CurrentStatus = Scheduled

Schedule valid

Convocation valid

ConvocationRules satisfied
```

Resultado:

```text
Status = Convoked

ConvokedAt != null
```

---

# RenameAssembly

RenameAssembly debe:

* ejecutarse solamente en estados permitidos;
* recibir AssemblyName válido;
* no modificar AssemblyId;
* no modificar OrganizationId;
* no producir evento cuando no exista cambio real;
* producir AssemblyRenamed cuando el cambio sea válido.

---

# ChangeAssemblyType

ChangeAssemblyType debe:

* ejecutarse solo en estados permitidos;
* recibir un AssemblyType válido;
* mantener consistencia con reglas y modalidad;
* no reescribir hechos históricos;
* producir AssemblyTypeChanged cuando exista cambio real.

---

# ChangeAssemblyPurpose

ChangeAssemblyPurpose debe:

* recibir propósito válido;
* ejecutarse en estados permitidos;
* mantener compatibilidad con AssemblyType;
* mantener coherencia con Convocation cuando corresponda;
* producir AssemblyPurposeChanged.

---

# ChangeAssemblyDescription

ChangeAssemblyDescription debe:

* respetar estados permitidos;
* mantener información válida;
* no alterar Purpose;
* no reescribir hechos históricos;
* producir AssemblyDescriptionChanged cuando exista cambio real.

---

# ChangeAssemblyModality

ChangeAssemblyModality debe:

* recibir modalidad válida;
* mantener Location compatible;
* mantener ExecutionConditions compatibles;
* mantener AssemblyRules compatibles;
* mantener Convocation consistente;
* respetar el estado actual;
* producir AssemblyModalityChanged.

---

# ChangeAssemblyLocation

ChangeAssemblyLocation debe:

* recibir Location válida;
* mantener compatibilidad con modalidad;
* respetar restricciones del estado;
* preservar convocatoria histórica;
* producir AssemblyLocationChanged.

---

# UpdateAssemblyConvocation

UpdateAssemblyConvocation debe:

* recibir Convocation válida;
* respetar el estado actual;
* no eliminar ConvokedAt histórico;
* no reescribir convocatoria pasada como si nunca hubiese
  ocurrido;
* producir AssemblyConvocationUpdated cuando exista un cambio
  válido.

---

# UpdateAssemblyRules

UpdateAssemblyRules debe:

* recibir reglas válidas;
* mantener compatibilidad con AssemblyType;
* mantener compatibilidad con AssemblyModality;
* mantener compatibilidad con ExecutionConditions;
* no anular invariantes;
* no reescribir hechos históricos.

---

# UpdateAssemblyExecutionConditions

UpdateAssemblyExecutionConditions debe:

* recibir condiciones válidas;
* mantener compatibilidad con AssemblyRules;
* mantener compatibilidad con AssemblyType;
* mantener compatibilidad con AssemblyModality;
* respetar la etapa del Lifecycle;
* no alterar hechos ya ocurridos.

---

# StartAssembly

StartAssembly debe validar:

```text
CurrentStatus = Convoked

Schedule valid

Convocation valid

ExecutionConditionsSatisfied = true
```

Resultado:

```text
Status = InProgress

StartedAt != null
```

---

# CompleteAssembly

CompleteAssembly debe validar:

```text
CurrentStatus = InProgress

StartedAt != null

CompletedAt >= StartedAt
```

Resultado:

```text
Status = Completed

CompletedAt != null
```

---

# CancelAssembly

CancelAssembly debe validar que CurrentStatus pertenezca a:

```text
Draft

Scheduled

Convoked
```

Resultado:

```text
Status = Cancelled

CancelledAt != null
```

---

# ArchiveAssembly

ArchiveAssembly debe validar que CurrentStatus pertenezca a:

```text
Completed

Cancelled
```

Resultado:

```text
Status = Archived

ArchivedAt != null
```

---

# Invariantes de Modificaciones Descriptivas

Operaciones como:

```text
RenameAssembly

ChangeAssemblyPurpose

ChangeAssemblyDescription

ChangeAssemblyType
```

solo pueden ejecutarse en estados expresamente autorizados.

Nunca pueden ejecutarse cuando:

```text
Status = Archived
```

y no deben utilizarse para alterar hechos históricos.

---

# Mutabilidad Decreciente

La capacidad de modificar Assembly disminuye conforme avanza el
Lifecycle.

Conceptualmente:

```text
Draft
    ↓
high mutability

Scheduled
    ↓
controlled mutability

Convoked
    ↓
restricted mutability

InProgress
    ↓
minimal structural mutability

Completed
    ↓
operational immutability

Cancelled
    ↓
operational immutability

Archived
    ↓
terminal immutability
```

Esta regla protege la historicidad.

---

# Invariantes y Application Services

Application Services coordinan:

```text
Repositories

Authorization

External Validations

Aggregate Invocation

Persistence

Event Dispatch
```

pero no deben reemplazar las invariantes internas.

La regla:

```text
CompletedAt >= StartedAt
```

pertenece al dominio.

No exclusivamente al Application Service.

---

# Regla de No Duplicación de Invariantes como Autoridad

Una regla puede validarse preventivamente en Application Layer
para evitar trabajo innecesario.

Sin embargo, Assembly continúa siendo la autoridad.

No debe existir una arquitectura donde la única protección de una
invariante se encuentre fuera del Aggregate.

---

# Invariantes y Repository

Repository debe persistir solamente estados válidos producidos por
Assembly.

No debe permitir operaciones como:

```text
update_status(id, "Archived")
```

saltándose la Aggregate Root.

El contrato debe trabajar con Assembly como unidad de
consistencia.

---

# Repository no Define Invariantes

El Repository puede verificar:

* existencia;
* versión;
* persistencia;

pero no debe convertirse en propietario de reglas como:

```text
CompletedAt >= StartedAt
```

La regla pertenece al modelo de dominio.

---

# Invariantes y Rehidratación

Una Assembly rehidratada desde persistencia debe satisfacer las
invariantes correspondientes a su estado.

Si la persistencia contiene:

```text
Status = InProgress

StartedAt = null
```

el estado persistido es inconsistente.

La rehidratación no debe normalizar silenciosamente dicha
inconsistencia.

Debe detectarse como corrupción o violación del modelo.

---

# Rehidratación no Ejecuta Transiciones

Restaurar:

```text
Status = Convoked
```

desde persistencia no ejecuta:

```text
ConvokeAssembly
```

ni produce nuevamente:

```text
AssemblyConvoked
```

La rehidratación restaura un estado previamente aceptado.

---

# Invariantes y Event Sourcing

Cuando se utilice Event Sourcing, la aplicación ordenada de
eventos válidos debe producir siempre un Aggregate válido.

Ejemplo:

```text
AssemblyCreated
    ↓
AssemblyScheduled
    ↓
AssemblyConvoked
    ↓
AssemblyStarted
```

debe producir:

```text
Status = InProgress

StartedAt != null
```

---

# Secuencia de Eventos Inválida

La versión 1.0 no admite una secuencia conceptual como:

```text
AssemblyCreated

AssemblyStarted
```

sin:

```text
AssemblyScheduled

AssemblyConvoked
```

porque la State Machine exige estados intermedios.

---

# Replay

El replay de eventos históricos no debe ejecutar nuevamente:

* permisos;
* side effects;
* Notifications;
* Integration Events externos;
* Commands.

Debe reconstruir el estado a partir de hechos previamente
aceptados.

---

# Invariantes de Seguridad

Assembly no almacena:

```text
Password

OAuthToken

JWT

RefreshToken

PrivateKey

ClientSecret

SessionCookie
```

Estos elementos no pertenecen al Aggregate.

Su presencia dentro del estado de Assembly constituye una
violación del límite del dominio.

---

# ActorId

Assembly y sus Commands o Events pueden utilizar:

```text
ActorId
```

para trazabilidad.

ActorId representa una referencia.

No implica almacenar:

* Citizen;
* credenciales;
* sesión;
* token;
* perfil de identidad;

dentro del Aggregate.

---

# Invariantes de Independencia Tecnológica

Ninguna invariante del dominio puede depender directamente de:

```text
HTTP

REST

GraphQL

MongoDB

PostgreSQL

Redis

Kafka

RabbitMQ

NATS

FIWARE

NGSI-LD

FastAPI

Django

React

Next.js
```

Las invariantes expresan reglas del dominio.

No condiciones de tecnología.

---

# Invariantes de Interoperabilidad

La interoperabilidad no puede alterar las reglas internas de
Assembly.

Un sistema externo no puede forzar:

```text
Status = Completed
```

si Assembly no satisface las condiciones de CompleteAssembly.

Toda entrada externa debe traducirse a una intención válida del
dominio.

---

# Anti-Corruption Layer

Cuando un sistema externo posea estados, eventos u operaciones
diferentes, estos deben traducirse antes de interactuar con
Assembly.

Ejemplo externo:

```text
MEETING_OPEN
```

solo puede traducirse a:

```text
StartAssembly
```

si existe equivalencia semántica real.

Después Assembly vuelve a validar todas sus invariantes.

---

# Invariantes y FIWARE

Una actualización recibida desde FIWARE no constituye autoridad
directa sobre el estado interno.

Por ejemplo:

```text
NGSI-LD entity state = completed
```

no puede producir directamente:

```text
AssemblyStatus = Completed
```

Debe existir una traducción válida hacia comportamiento del
dominio y todas las invariantes deben ser verificadas.

---

# FIWARE como Proyección

Cuando Assembly sea proyectada hacia FIWARE, la representación
externa debe reflejar el estado válido del Aggregate.

FIWARE no se convierte en fuente de verdad para las invariantes
internas.

---

# Invariantes y Read Models

Los Read Models pueden contener representaciones desnormalizadas.

No constituyen autoridad para modificar Assembly.

Una inconsistencia en un Read Model no cambia las invariantes del
Aggregate.

La fuente transaccional continúa siendo Assembly.

---

# Read Model Derivable

Un Read Model puede derivar conceptos como:

```text
Upcoming

Past

Editable

Visible
```

sin convertirlos en AssemblyStatus.

Las propiedades derivadas de lectura no modifican las invariantes
del Write Model.

---

# Invariantes y CQRS

Dentro de CQRS:

```text
Command
    │
    ▼
Write Model
    │
    ▼
Assembly Invariants
    │
    ▼
Domain Event
    │
    ▼
Read Model
```

Las invariantes pertenecen al Write Model.

No deben delegarse al Read Model.

---

# Invariantes y Consistencia Eventual

La consistencia eventual entre Aggregates no significa que
Assembly pueda quedar internamente inconsistente.

Debe mantenerse:

```text
Strong Consistency
within Assembly
```

y puede utilizarse:

```text
Eventual Consistency
between Aggregates
```

---

# Fallo de un Consumidor Externo

Después de una operación válida, el fallo de un consumidor de un
Domain Event no invalida retroactivamente el estado de Assembly.

Ejemplo:

```text
AssemblyConvoked
```

ocurrió válidamente.

Si falla un consumidor de Notification, Assembly continúa:

```text
Convoked
```

El fallo debe resolverse fuera del Aggregate.

---

# Invariantes de Orden de Eventos

Para una misma Assembly:

```text
AggregateVersion
```

debe aumentar de manera coherente.

No deben aplicarse hechos en un orden que produzca un estado
imposible.

---

# Evento Duplicado

Una retransmisión del mismo evento no representa un nuevo cambio
del Aggregate.

Los consumidores pueden utilizar:

```text
EventId
```

para detectar duplicados.

La duplicación de transporte no altera las invariantes de
Assembly.

---

# Commands Duplicados

Una retransmisión del mismo:

```text
CommandId
```

puede ser detectada en la frontera de aplicación.

No debe utilizarse una segunda ejecución para producir una nueva
modificación accidental.

La idempotencia técnica no modifica las reglas internas del
Aggregate.

---

# Validación Determinista

Las invariantes internas deben ser deterministas respecto de la
información disponible para Assembly y de las decisiones externas
explícitamente suministradas.

No deben depender directamente de:

* llamadas HTTP;
* consultas de base de datos;
* APIs externas;
* estado global mutable;
* reloj del sistema oculto.

---

# Tiempo como Dependencia Explícita

Cuando una operación requiera el momento actual, este debe
proporcionarse mediante una abstracción o valor explícito.

Conceptualmente:

```text
StartAssembly(
    StartedAt
)
```

o mediante un mecanismo equivalente definido por la arquitectura.

Esto permite:

* determinismo;
* pruebas reproducibles;
* trazabilidad;
* Event Sourcing;
* control temporal.

---

# No Reparación Silenciosa

Assembly no debe corregir silenciosamente datos inválidos cuando
ello cambie su significado.

Ejemplo:

si:

```text
ScheduledEndAt < ScheduledStartAt
```

no debe intercambiar automáticamente las fechas.

Debe rechazar la operación.

---

# Normalización versus Reparación

Puede existir normalización dentro de Value Objects cuando no
altera significado.

Ejemplo conceptual:

```text
trim whitespace
```

puede formar parte de AssemblyName.

Sin embargo, transformar valores contradictorios para hacerlos
válidos constituye una reparación y debe evitarse salvo regla
explícita del dominio.

---

# Violación de Invariantes

Cuando una operación viola una invariante:

```text
Operation Rejected
```

Debe mantenerse:

```text
StateAfter = StateBefore

VersionAfter = VersionBefore
```

y no debe producirse ningún Domain Event de éxito.

---

# Error de Dominio

Una violación debe representarse mediante un error de dominio
semánticamente significativo.

Ejemplos conceptuales:

```text
InvalidAssemblyState

InvalidAssemblySchedule

InvalidAssemblyTransition

InvalidConvocation

InvalidAssemblyModality

InvalidAssemblyLocation

InvalidExecutionConditions

AssemblyAlreadyArchived

AssemblyInvariantViolation
```

La taxonomía definitiva puede desarrollarse en documentación
específica.

---

# Error no es Estado

Los errores de ejecución no deben convertirse automáticamente en
AssemblyStatus.

No deben añadirse estados como:

```text
ValidationFailed

PersistenceError

NetworkError
```

Estos no representan etapas del Lifecycle.

---

# Invariantes y Auditoría

Toda modificación válida debe ser trazable mediante:

```text
AssemblyId

OrganizationId

Version

Domain Event

OccurredAt

ActorId when applicable

CorrelationId

CausationId
```

La auditoría no altera el resultado de las invariantes.

---

# Intentos Rechazados

Una operación rechazada puede ser registrada por mecanismos de:

* seguridad;
* auditoría técnica;
* observabilidad;
* aplicación;

si las políticas lo requieren.

Ese registro no representa un Domain Event de éxito del
Aggregate.

---

# Matriz de Invariantes por Estado

| Invariante             | Draft        | Scheduled    | Convoked    | InProgress       | Completed   | Cancelled            | Archived       |
| ---------------------- | ------------ | ------------ | ----------- | ---------------- | ----------- | -------------------- | -------------- |
| AssemblyId válido      | Obligatoria  | Obligatoria  | Obligatoria | Obligatoria      | Obligatoria | Obligatoria          | Obligatoria    |
| OrganizationId válido  | Obligatoria  | Obligatoria  | Obligatoria | Obligatoria      | Obligatoria | Obligatoria          | Obligatoria    |
| AssemblyName válido    | Obligatoria  | Obligatoria  | Obligatoria | Obligatoria      | Obligatoria | Obligatoria          | Obligatoria    |
| AssemblyType válido    | Obligatoria  | Obligatoria  | Obligatoria | Obligatoria      | Obligatoria | Obligatoria          | Obligatoria    |
| AssemblyStatus válido  | Obligatoria  | Obligatoria  | Obligatoria | Obligatoria      | Obligatoria | Obligatoria          | Obligatoria    |
| Schedule válido        | Opcional     | Obligatoria  | Obligatoria | Obligatoria      | Histórica   | Histórica si existió | Histórica      |
| Modality válida        | Opcional     | Obligatoria  | Obligatoria | Obligatoria      | Histórica   | Histórica si existió | Histórica      |
| Convocation válida     | No requerida | No requerida | Obligatoria | Histórica válida | Histórica   | Histórica si existió | Histórica      |
| StartedAt              | No           | No           | No          | Obligatorio      | Obligatorio | No en v1.0           | Según historia |
| CompletedAt            | No           | No           | No          | No               | Obligatorio | No                   | Según historia |
| CancelledAt            | No           | No           | No          | No               | No          | Obligatorio          | Según historia |
| ArchivedAt             | No           | No           | No          | No               | No          | No                   | Obligatorio    |
| Version válida         | Obligatoria  | Obligatoria  | Obligatoria | Obligatoria      | Obligatoria | Obligatoria          | Obligatoria    |
| Modificación ordinaria | Sí           | Sí           | Restringida | Muy restringida  | No*         | No*                  | No             |

`No*` significa que el estado no admite modificaciones operativas
ordinarias, salvo las transiciones explícitamente definidas, como:

```text
Completed -> Archived

Cancelled -> Archived
```

---

# Matriz de Transiciones e Invariantes

| Transición             | Condiciones mínimas                                |
| ---------------------- | -------------------------------------------------- |
| Creation → Draft       | Identity + Organization + Name + Type válidos      |
| Draft → Scheduled      | Schedule + Modality + Location cuando corresponda  |
| Scheduled → Convoked   | Schedule válido + Convocation válida               |
| Convoked → InProgress  | Guards de inicio + ExecutionConditions satisfechas |
| InProgress → Completed | StartedAt válido + condiciones de cierre           |
| Draft → Cancelled      | Cancelación válida                                 |
| Scheduled → Cancelled  | Cancelación válida + historia preservada           |
| Convoked → Cancelled   | Cancelación válida + convocatoria preservada       |
| Completed → Archived   | Completed válido + ArchivedAt                      |
| Cancelled → Archived   | Cancelled válido + ArchivedAt                      |

---

# Invariantes Iniciales

Al crear Assembly deben satisfacerse como mínimo:

```text
AssemblyId != null

OrganizationId != null

AssemblyName valid

AssemblyType valid

AssemblyStatus = Draft

CreatedAt != null

Version initialized
```

No se permite crear directamente una Assembly en:

```text
Scheduled

Convoked

InProgress

Completed

Cancelled

Archived
```

La creación comienza siempre en Draft.

---

# Invariantes Permanentes

Durante toda la existencia de Assembly deben mantenerse:

```text
AssemblyId immutable

OrganizationId immutable

AssemblyStatus valid

AssemblyType valid

AssemblyName valid

Version valid

Aggregate boundary preserved
```

Estas reglas no dependen del estado.

---

# Invariantes Condicionales

Algunas reglas dependen del estado.

Conceptualmente:

```text
if Status == Scheduled:
    ScheduledStartAt required
    AssemblyModality required

if Status == Convoked:
    ScheduledStartAt required
    ConvokedAt required

if Status == InProgress:
    StartedAt required

if Status == Completed:
    StartedAt required
    CompletedAt required

if Status == Cancelled:
    CancelledAt required

if Status == Archived:
    ArchivedAt required
```

---

# Invariantes Históricas

Los hechos ocurridos no deben desaparecer al avanzar el
Lifecycle.

Ejemplo:

```text
AssemblyStatus = Completed
```

debe conservar:

```text
StartedAt

CompletedAt
```

Una Assembly Archived proveniente de Completed debe conservar
ambos.

---

# Preservación de Historia

Las transiciones no deben limpiar información histórica necesaria.

No debe ocurrir:

```text
Convoked
    ↓
InProgress

ConvokedAt = null
```

ni:

```text
InProgress
    ↓
Completed

StartedAt = null
```

Los timestamps históricos permanecen.

---

# Histórico de Programación

Cuando una Assembly haya sido programada, el hecho de que
posteriormente sea:

```text
Cancelled
```

no debe eliminar automáticamente la programación histórica.

De igual forma, Archived conserva la historia relevante del
camino que llevó al estado terminal.

---

# Histórico de Convocatoria

Una Assembly que haya alcanzado:

```text
Convoked
```

conserva:

```text
ConvokedAt
```

aunque posteriormente alcance:

```text
Cancelled

Archived
```

La convocatoria ocurrió y forma parte de su historia.

---

# Invariantes de Eliminación

La versión 1.0 no define:

```text
DeleteAssembly
```

como comportamiento de dominio.

La eliminación física no forma parte del Lifecycle.

Archived representa la salida operativa definitiva del Aggregate.

---

# Invariantes de Reactivación

La versión 1.0 no permite:

```text
Archived -> ActiveState
```

ni:

```text
Cancelled -> Scheduled
```

ni:

```text
Completed -> InProgress
```

Una futura capacidad de reapertura debe introducirse
explícitamente mediante nuevos:

* Commands;
* Domain Events;
* Guards;
* transiciones;
* invariantes;
* permisos;
* escenarios de prueba.

---

# Reapertura no Implícita

No se permite implementar reapertura mediante:

```text
setStatus(...)
```

ni mediante manipulación directa de persistencia.

El dominio debe evolucionar explícitamente si esa capacidad se
vuelve necesaria.

---

# Invariantes de Integración

Un Integration Event no puede alterar directamente el estado de
Assembly.

Una entrada externa debe convertirse en:

```text
Command
```

o intención equivalente y pasar por la Aggregate Root.

Conceptualmente:

```text
External Event
      │
      ▼
Anti-Corruption Layer
      │
      ▼
Application Service
      │
      ▼
Command
      │
      ▼
Assembly
      │
      ▼
Invariant Validation
```

---

# Integration Event de Salida

Un Domain Event puede originar posteriormente un Integration
Event.

Este proceso no forma parte de la modificación interna que
protege las invariantes.

Conceptualmente:

```text
Assembly
    │
    ▼
Domain Event
    │
    ▼
Integration Handler
    │
    ▼
Integration Event
```

---

# Invariantes y Transactional Outbox

Una estrategia como:

```text
Transactional Outbox
```

puede utilizarse para proteger consistencia entre persistencia y
publicación confiable de eventos.

Assembly no conoce la Outbox.

La existencia de esta infraestructura no modifica las invariantes
del dominio.

---

# Invariantes y Performance

Las optimizaciones no pueden evadir la protección de invariantes.

No debe utilizarse una actualización directa de columnas,
documentos o cachés para evitar cargar el Aggregate cuando la
operación modifica estado protegido.

Ejemplo prohibido conceptualmente:

```text
UPDATE assembly
SET status = 'Completed'
WHERE assembly_id = ...
```

como sustituto de:

```text
CompleteAssembly
```

---

# Caché

Una representación en caché no constituye autoridad para validar
una modificación si puede encontrarse obsoleta respecto de la
Version oficial.

La consistencia de escritura debe utilizar la versión vigente del
Aggregate.

---

# Invariantes de Seguridad del Dominio

Las reglas del Aggregate no deben depender de información de
autenticación técnica.

Assembly recibe una intención cuya autorización ha sido
determinada externamente y protege sus propias invariantes.

No almacena sesiones ni credenciales.

---

# Privacidad

Assembly debe conservar únicamente la información que pertenece a
su responsabilidad.

No debe copiar perfiles completos de Citizen o Membership para
facilitar validaciones futuras.

Debe utilizar referencias y decisiones explícitas cuando
corresponda.

---

# Minimización de Datos

El principio de minimización también protege el Consistency
Boundary.

Si Assembly solo necesita:

```text
CitizenId
```

no debe almacenar:

```text
CitizenFullProfile
```

dentro del Aggregate.

---

# Reglas de Implementación

La implementación futura debe garantizar que:

* constructors o factories creen estados válidos;
* no existan setters públicos que violen encapsulamiento;
* los métodos de dominio validen invariantes;
* los Value Objects validen sus propias reglas;
* las transiciones pasen por la Aggregate Root;
* el Repository no modifique atributos internos directamente;
* la rehidratación detecte estados inválidos;
* los Commands rechazados no generen eventos;
* las modificaciones válidas incrementen Version;
* los timestamps históricos se preserven.

---

# Constructors

La construcción directa no debe permitir crear una Assembly en un
estado arbitrario.

La creación funcional debe producir:

```text
Draft
```

como estado inicial.

Los mecanismos internos de rehidratación pueden restaurar otros
estados, pero deben permanecer diferenciados de la creación de
una nueva Assembly.

---

# Factories

Una Factory de dominio puede utilizarse cuando la creación
requiera lógica adicional.

La Factory no puede devolver una Assembly que viole las
invariantes iniciales.

---

# Value Objects

Las reglas locales de valor deben protegerse mediante Value
Objects cuando corresponda.

Ejemplos:

```text
AssemblyId

AssemblyName

AssemblyType

AssemblyPurpose

AssemblyDescription

AssemblyModality

AssemblyStatus

AssemblySchedule

AssemblyLocation

Version
```

Los Value Objects reducen la posibilidad de representar valores
inválidos.

---

# Value Objects no Sustituyen Aggregate Invariants

Una regla puede involucrar múltiples conceptos.

Ejemplo:

```text
ScheduledEndAt > ScheduledStartAt
```

puede ser responsabilidad de AssemblySchedule.

Pero:

```text
Convoked Assembly requires valid Schedule
```

pertenece al Aggregate.

La responsabilidad debe ubicarse en el nivel que posea toda la
información necesaria para proteger la regla.

---

# Make Invalid States Unrepresentable

El diseño debe aproximarse al principio:

```text
Make Invalid States Unrepresentable
```

cuando sea razonable.

Esto puede lograrse mediante:

* Value Objects;
* constructors restringidos;
* factories;
* comportamiento explícito;
* enums cerrados;
* encapsulación.

Sin embargo, las invariantes del Aggregate continúan siendo
necesarias para reglas que cruzan múltiples Value Objects,
estados y comportamientos.

---

# Excepciones de Dominio

La implementación puede utilizar excepciones o resultados
tipados para representar violaciones.

La estrategia concreta no debe cambiar el significado del error.

Debe diferenciarse entre:

```text
Domain Rule Violation
```

y:

```text
Infrastructure Failure
```

---

# Dominio versus Infraestructura

Ejemplo de error de dominio:

```text
CannotCompleteAssemblyFromConvoked
```

Ejemplo de error de infraestructura:

```text
DatabaseUnavailable
```

No deben tratarse como si fueran la misma categoría conceptual.

---

# Escenarios Obligatorios de Validación

Como mínimo deben existir escenarios de prueba para:

```text
crear Assembly válida;

rechazar Assembly sin OrganizationId;

rechazar Assembly sin nombre válido;

rechazar AssemblyType inválido;

rechazar modificación de AssemblyId;

rechazar modificación de OrganizationId;

rechazar Schedule sin ScheduledStartAt;

rechazar ScheduledEndAt anterior a ScheduledStartAt;

rechazar ScheduledEndAt igual a ScheduledStartAt;

rechazar modalidad inválida;

rechazar Location incompatible con modalidad;

rechazar convocatoria desde Draft;

rechazar convocatoria inválida;

rechazar inicio desde Draft;

rechazar inicio desde Scheduled;

permitir inicio desde Convoked válido;

rechazar inicio sin ExecutionConditions satisfechas;

rechazar finalización sin StartedAt;

rechazar finalización desde Convoked;

permitir finalización desde InProgress;

rechazar CompletedAt anterior a StartedAt;

rechazar cancelación desde InProgress en versión 1.0;

rechazar cancelación desde Completed;

rechazar cancelación desde Archived;

permitir archivado desde Completed;

permitir archivado desde Cancelled;

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

Estas pruebas permiten verificar amplios conjuntos de estados y
secuencias.

---

# Pruebas de Secuencias

Debe verificarse que secuencias completas mantengan las
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

Ejemplo:

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

Los timestamps y hechos históricos previos deben permanecer.

---

# Secuencia Inválida

Ejemplo:

```text
Create
    ↓
Draft

Start
    ↓
InProgress
```

debe ser imposible.

La prueba debe verificar que:

```text
Status remains Draft

StartedAt remains null

Version unchanged

AssemblyStarted not generated
```

---

# Invariantes y Test Fixtures

Las herramientas de prueba no deben construir estados imposibles
mediante setters públicos.

Cuando una prueba necesite una Assembly en determinado estado debe
alcanzarlo mediante:

* comportamiento válido; o
* mecanismo de rehidratación controlado;

manteniendo las invariantes.

---

# Evolución de Invariantes

Una nueva regla puede incorporarse cuando exista una necesidad
real del dominio.

Toda nueva invariante debe analizar su impacto sobre:

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

No debe introducirse una invariante aislada que contradiga el
resto del modelo.

---

# Cambio de Invariante

Modificar una invariante existente constituye una modificación
del comportamiento del dominio.

Debe evaluarse:

* compatibilidad con Aggregates existentes;
* datos persistidos;
* eventos históricos;
* Commands;
* State Machine;
* Read Models;
* Integration Events;
* tests;
* versionado;
* migraciones.

---

# Invariantes y Versionado de Dominio

Cuando una nueva invariante haga inválidos estados previamente
aceptados debe existir una estrategia explícita.

No debe suponerse que todos los Aggregates históricos cumplen
automáticamente una regla introducida posteriormente.

La evolución se desarrolla conforme a:

```text
DOMAIN-006I-Versioning.md
```

y las decisiones arquitectónicas correspondientes.

---

# Reglas de Prioridad

Cuando existan múltiples capas de reglas debe respetarse la
siguiente autoridad conceptual:

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

Una regla inferior no puede anular una regla superior del modelo.

---

# Regla de Consistencia Documental

Este documento debe mantenerse consistente con:

```text
DOMAIN-006-Aggregate.md

DOMAIN-006A-Lifecycle.md

DOMAIN-006B-State-Machine.md

DOMAIN-006C-Commands.md

DOMAIN-006D-Domain-Events.md
```

Cuando exista contradicción entre artefactos oficiales, esta debe
resolverse antes de implementación.

No debe seleccionarse arbitrariamente una regla durante el
desarrollo.

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
* mantener una modalidad inválida;
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
* utilizar caché obsoleta para evadir control de Version;
* reescribir hechos históricos para simplificar el estado actual.

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
* Transactional Outbox;
* arquitectura distribuida;
* consistencia eventual entre Aggregates;
* consistencia fuerte dentro del Aggregate.

---

# Principios de Diseño

Las invariantes de Assembly cumplen los siguientes principios:

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

Las transiciones del Lifecycle permanecen subordinadas a la
State Machine y sus Guards. Los cambios válidos producen un
estado completo y consistente, incrementan Version y registran los
Domain Events correspondientes. Las operaciones rechazadas no
modifican estado, no incrementan Version y no publican eventos de
éxito.

Assembly mantiene consistencia fuerte dentro de su propio límite
y utiliza identificadores, Domain Events, Integration Events y
coordinación externa para relacionarse con Organization,
Territory, Membership, Citizen, Role, Proposal, Participation,
Voting, Document, Notification, Audit e Integration sin absorber
sus responsabilidades.

Los estados terminales preservan la historia del Aggregate:
Cancelled no elimina los hechos anteriores y Archived no
representa eliminación física. Los timestamps históricos,
AssemblyId, OrganizationId, Version y Domain Events permanecen
trazables durante toda la existencia de Assembly.

La configuración mediante AssemblyRules y ExecutionConditions no
puede anular las invariantes estructurales. La autorización no
puede convertir una operación inválida en válida. La
infraestructura no puede modificar el estado saltándose la
Aggregate Root. Los sistemas externos no pueden imponer su
semántica sobre el modelo interno.

De esta forma, las invariantes constituyen la barrera fundamental
que impide representar estados inválidos dentro de Assembly y
preservan la integridad conceptual del Aggregate bajo
Domain-Driven Design, Clean Architecture, CQRS,
Event-Driven Architecture y una arquitectura distribuida.
