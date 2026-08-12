# DOMAIN-006M — Assembly Test Scenarios

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Assembly Management

Aggregate:
Assembly

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
* DOMAIN-006I-Versioning.md
* DOMAIN-006J-Consistency-Boundary.md
* DOMAIN-006K-Integration-Events.md
* DOMAIN-006L-Read-Model.md
* CORE-006-Domain-Invariants.md
* CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Definir los escenarios conceptuales de prueba del Aggregate
**Assembly**.

Los Test Scenarios permiten verificar que el comportamiento del
Aggregate preserve de forma consistente las reglas establecidas en
su modelo oficial.

Cada escenario debe comprobar que Assembly:

* respeta su Lifecycle;
* respeta su State Machine;
* protege sus invariantes;
* aplica las condiciones definidas para cada operación;
* respeta Permissions;
* mantiene su Consistency Boundary;
* incrementa Version únicamente cuando corresponde;
* produce los Domain Events esperados;
* rechaza operaciones inválidas;
* no modifica otros Aggregates;
* mantiene coherencia con Integration Events y Read Models.

Este documento no introduce nuevas reglas de dominio.

Los escenarios definidos aquí verifican exclusivamente las reglas
establecidas por los documentos oficiales del Aggregate Assembly.

---

# Propósito

El propósito de los Test Scenarios es transformar las reglas
conceptuales de Assembly en condiciones verificables.

Debe mantenerse:

```text
Domain Rule

↓

Test Scenario

↓

Verified Domain Behavior
```

Los escenarios permiten comprobar que una implementación respete el
modelo conceptual definido para Assembly.

No constituyen una nueva fuente de reglas.

La fuente conceptual oficial continúa siendo:

```text
DOMAIN-006-Aggregate.md
```

y sus documentos complementarios.

---

# Principios

Los Test Scenarios deben seguir los siguientes principios:

* verificar comportamiento del dominio;
* utilizar lenguaje ubicuo;
* expresar condiciones observables;
* verificar resultados válidos;
* verificar rechazos;
* verificar invariantes;
* verificar transiciones;
* verificar eventos;
* verificar Version;
* verificar ausencia de efectos inválidos;
* permanecer independientes de Infrastructure;
* permanecer independientes de Frameworks;
* no redefinir el modelo del Aggregate.

---

# Estructura Conceptual

Los escenarios pueden expresarse mediante:

```text
Given

When

Then
```

donde:

```text
Given
```

representa el estado inicial y las precondiciones.

```text
When
```

representa la operación o intención evaluada.

```text
Then
```

representa el resultado esperado del dominio.

---

# Regla Fundamental

Todo Test Scenario debe derivarse de una regla ya establecida en el
modelo oficial de Assembly.

No debe utilizarse este documento para introducir:

* nuevos estados;
* nuevas transiciones;
* nuevos Commands;
* nuevos Domain Events;
* nuevas invariantes;
* nuevos Permissions;
* nuevas entidades internas;
* nuevos Value Objects;
* nuevos Aggregates;
* nuevas responsabilidades.

---

# Ámbito de Pruebas

Los escenarios deben cubrir como mínimo:

```text
Creation

Lifecycle

State Machine

Commands

Domain Events

Invariants

Permissions

Repository Contract

Versioning

Consistency Boundary

Integration Events

Read Model
```

Cada ámbito verifica una dimensión diferente del Aggregate.

---

# Creación de Assembly

## Escenario — Creación válida

```text
Given

una Organization válida para el contexto de la operación

And

datos válidos para crear una Assembly

When

CreateAssembly es aceptado

Then

se crea una nueva Assembly

And

Assembly posee un AssemblyId

And

OrganizationId queda asociado a la Assembly

And

AssemblyStatus corresponde al estado inicial definido

And

Version queda establecida conforme al modelo de Versioning

And

se produce AssemblyCreated
```

---

# Identidad

## Escenario — AssemblyId es único

```text
Given

una Assembly existente

When

se crea otra Assembly válida

Then

ambas Assemblies poseen AssemblyId distintos
```

---

## Escenario — AssemblyId permanece inmutable

```text
Given

una Assembly existente

When

se ejecuta una modificación válida

Then

AssemblyId permanece sin cambios
```

---

## Escenario — AssemblyId no puede modificarse directamente

```text
Given

una Assembly existente

When

se intenta modificar AssemblyId directamente

Then

la operación no está permitida
```

---

# Contexto Organizacional

## Escenario — OrganizationId es obligatorio

```text
Given

una solicitud de creación de Assembly

When

OrganizationId no se encuentra definido

Then

la creación debe ser rechazada

And

no se crea Assembly

And

no se produce AssemblyCreated
```

---

## Escenario — OrganizationId permanece inmutable

```text
Given

una Assembly asociada a OrganizationId A

When

se ejecutan modificaciones válidas sobre la Assembly

Then

OrganizationId permanece igual a A
```

---

## Escenario — No se modifica Organization desde Assembly

```text
Given

una Assembly asociada a una Organization

When

Assembly cambia válidamente

Then

el estado interno de Organization no es modificado por Assembly
```

---

# Contexto Territorial

## Escenario — Assembly puede mantener TerritoryId cuando corresponde

```text
Given

una Assembly cuyo contexto requiere Territory

When

la Assembly es creada o configurada válidamente

Then

TerritoryId identifica el contexto territorial correspondiente
```

---

## Escenario — Territory permanece fuera del Aggregate

```text
Given

una Assembly con TerritoryId

When

Assembly modifica su estado

Then

el Aggregate Territory no es modificado directamente
```

---

# Tipo de Assembly

## Escenario — Tipo válido

```text
Given

una Assembly en un estado que permite modificar su tipo

When

ChangeAssemblyType contiene un AssemblyType válido

Then

AssemblyType cambia

And

Version cambia

And

se produce AssemblyTypeChanged
```

---

## Escenario — Tipo inválido

```text
Given

una Assembly existente

When

se intenta establecer un AssemblyType no válido

Then

la operación es rechazada

And

AssemblyType permanece sin cambios

And

Version permanece sin cambios
```

---

# Nombre de Assembly

## Escenario — Renombrar Assembly

```text
Given

una Assembly en un estado que permite modificar su nombre

When

RenameAssembly contiene un nombre válido

Then

AssemblyName cambia

And

Version cambia

And

se produce AssemblyRenamed
```

---

## Escenario — Rename rechazado

```text
Given

una Assembly en un estado que no permite modificar su nombre

When

RenameAssembly es ejecutado

Then

la operación es rechazada

And

AssemblyName permanece sin cambios

And

Version permanece sin cambios
```

---

# Propósito

## Escenario — Cambiar propósito

```text
Given

una Assembly en un estado válido para modificar su propósito

When

ChangeAssemblyPurpose es aceptado

Then

AssemblyPurpose cambia

And

Version cambia

And

se produce AssemblyPurposeChanged
```

---

# Descripción

## Escenario — Cambiar descripción

```text
Given

una Assembly en un estado válido para modificar su descripción

When

ChangeAssemblyDescription es aceptado

Then

AssemblyDescription cambia

And

Version cambia

And

se produce AssemblyDescriptionChanged
```

---

# Modalidad

## Escenario — Cambio válido de modalidad

```text
Given

una Assembly en un estado que permite modificar su modalidad

When

ChangeAssemblyMode establece una modalidad válida

Then

AssemblyMode cambia

And

la Assembly mantiene consistencia con Location cuando corresponda

And

Version cambia

And

se produce AssemblyModeChanged
```

---

## Escenario — Modalidad inválida

```text
Given

una Assembly existente

When

se intenta establecer una modalidad no definida por el dominio

Then

la operación es rechazada

And

AssemblyMode permanece sin cambios

And

Version permanece sin cambios
```

---

# Ubicación

## Escenario — Cambio válido de ubicación

```text
Given

una Assembly en un estado que permite modificar Location

When

ChangeAssemblyLocation contiene una ubicación válida

Then

Location cambia

And

Version cambia

And

se produce AssemblyLocationChanged
```

---

## Escenario — Ubicación requerida

```text
Given

una Assembly cuya modalidad requiere Location válida

When

se intenta establecer una configuración incompatible con esa regla

Then

la operación es rechazada

And

el Aggregate permanece consistente
```

---

# Programación

## Escenario — Programar Assembly

```text
Given

una Assembly en Draft

When

ScheduleAssembly contiene programación válida

Then

AssemblyStatus cambia a Scheduled

And

ScheduledStart queda establecido

And

ScheduledEnd queda establecido cuando corresponda

And

Version cambia

And

se produce AssemblyScheduled
```

---

## Escenario — ScheduledEnd anterior a ScheduledStart

```text
Given

una Assembly que puede ser programada

When

ScheduledEnd es anterior a ScheduledStart

Then

ScheduleAssembly es rechazado

And

AssemblyStatus permanece sin cambios

And

Version permanece sin cambios

And

no se produce AssemblyScheduled
```

---

## Escenario — Reprogramar Assembly

```text
Given

una Assembly en un estado que permite reprogramación

When

RescheduleAssembly contiene una nueva programación válida

Then

la programación cambia

And

Assembly permanece en un estado válido

And

Version cambia

And

se produce AssemblyRescheduled
```

---

## Escenario — Reprogramación inválida

```text
Given

una Assembly en un estado que no permite reprogramación

When

RescheduleAssembly es ejecutado

Then

la operación es rechazada

And

la programación permanece sin cambios

And

Version permanece sin cambios
```

---

# Convocatoria

## Escenario — Convocar Assembly

```text
Given

una Assembly en Scheduled

And

las condiciones de convocatoria se encuentran satisfechas

When

ConvokeAssembly es aceptado

Then

AssemblyStatus cambia a Convoked

And

la información formal de convocatoria queda establecida

And

ConvokedAt queda registrado cuando corresponde

And

Version cambia

And

se produce AssemblyConvoked
```

---

## Escenario — Convocar desde estado inválido

```text
Given

una Assembly en un estado distinto de aquel permitido para
convocatoria

When

ConvokeAssembly es ejecutado

Then

la operación es rechazada

And

AssemblyStatus permanece sin cambios

And

Version permanece sin cambios

And

no se produce AssemblyConvoked
```

---

## Escenario — Actualizar convocatoria

```text
Given

una Assembly cuya convocatoria puede modificarse

When

UpdateAssemblyConvocation contiene información válida

Then

la información de convocatoria cambia

And

Version cambia

And

se produce AssemblyConvocationUpdated
```

---

## Escenario — Convocation no modifica Notification

```text
Given

una Assembly válida

When

la Assembly es convocada

Then

Assembly mantiene su condición formal de convocatoria

And

Notification no es modificada directamente por Assembly
```

---

# Inicio de Assembly

## Escenario — Inicio válido

```text
Given

una Assembly en Convoked

And

las condiciones necesarias para iniciar se encuentran satisfechas

When

StartAssembly es aceptado

Then

AssemblyStatus cambia a InProgress

And

StartedAt queda establecido cuando corresponde

And

Version cambia

And

se produce AssemblyStarted
```

---

## Escenario — Inicio desde Draft

```text
Given

una Assembly en Draft

When

StartAssembly es ejecutado

Then

la operación es rechazada

And

AssemblyStatus permanece Draft

And

Version permanece sin cambios

And

no se produce AssemblyStarted
```

---

## Escenario — Inicio desde Scheduled

```text
Given

una Assembly en Scheduled

When

StartAssembly es ejecutado sin haber alcanzado Convoked

Then

la operación es rechazada

And

AssemblyStatus permanece Scheduled

And

Version permanece sin cambios
```

---

## Escenario — Inicio desde Cancelled

```text
Given

una Assembly en Cancelled

When

StartAssembly es ejecutado

Then

la operación es rechazada

And

AssemblyStatus permanece Cancelled
```

---

## Escenario — Inicio desde Archived

```text
Given

una Assembly en Archived

When

StartAssembly es ejecutado

Then

la operación es rechazada

And

AssemblyStatus permanece Archived
```

---

# Finalización de Assembly

## Escenario — Finalización válida

```text
Given

una Assembly en InProgress

And

las condiciones necesarias para finalizar se encuentran
satisfechas

When

CompleteAssembly es aceptado

Then

AssemblyStatus cambia a Completed

And

CompletedAt queda establecido cuando corresponde

And

Version cambia

And

se produce AssemblyCompleted
```

---

## Escenario — Completar desde Convoked

```text
Given

una Assembly en Convoked

When

CompleteAssembly es ejecutado

Then

la operación es rechazada

And

AssemblyStatus permanece Convoked

And

Version permanece sin cambios
```

---

## Escenario — Completar desde Scheduled

```text
Given

una Assembly en Scheduled

When

CompleteAssembly es ejecutado

Then

la operación es rechazada

And

AssemblyStatus permanece Scheduled
```

---

## Escenario — Completar desde Cancelled

```text
Given

una Assembly en Cancelled

When

CompleteAssembly es ejecutado

Then

la operación es rechazada

And

AssemblyStatus permanece Cancelled
```

---

# Cancelación

## Escenario — Cancelar Assembly válida

```text
Given

una Assembly en un estado desde el cual la cancelación está
permitida

When

CancelAssembly es aceptado

Then

AssemblyStatus cambia a Cancelled

And

CancelledAt queda establecido cuando corresponde

And

Version cambia

And

se produce AssemblyCancelled
```

---

## Escenario — Cancelled no continúa a InProgress

```text
Given

una Assembly en Cancelled

When

StartAssembly es ejecutado

Then

la operación es rechazada

And

AssemblyStatus permanece Cancelled
```

---

## Escenario — Cancelled no continúa a Completed

```text
Given

una Assembly en Cancelled

When

CompleteAssembly es ejecutado

Then

la operación es rechazada

And

AssemblyStatus permanece Cancelled
```

---

# Archivado

## Escenario — Archivar Assembly completada

```text
Given

una Assembly en Completed

When

ArchiveAssembly es aceptado

Then

AssemblyStatus cambia a Archived

And

ArchivedAt queda establecido cuando corresponde

And

Version cambia

And

se produce AssemblyArchived
```

---

## Escenario — Archivar Assembly cancelada

```text
Given

una Assembly en Cancelled

When

ArchiveAssembly es aceptado

Then

AssemblyStatus cambia a Archived

And

Version cambia

And

se produce AssemblyArchived
```

---

## Escenario — Assembly archivada es inmutable

```text
Given

una Assembly en Archived

When

se intenta ejecutar una modificación ordinaria

Then

la operación es rechazada

And

el estado interno permanece sin cambios

And

Version permanece sin cambios
```

---

# Lifecycle Completo

## Escenario — Camino principal

```text
Given

una nueva Assembly

When

se ejecutan válidamente las operaciones correspondientes

Then

el Lifecycle puede evolucionar:

Draft

↓

Scheduled

↓

Convoked

↓

InProgress

↓

Completed

↓

Archived
```

Cada transición debe:

* respetar la State Machine;
* proteger invariantes;
* modificar Version;
* producir el Domain Event correspondiente.

---

# Lifecycle de Cancelación

## Escenario — Cancelación antes de inicio

```text
Given

una Assembly en un estado desde el cual CancelAssembly está
permitido

When

CancelAssembly es aceptado

Then

AssemblyStatus cambia a Cancelled

And

la Assembly no continúa por el camino normal hacia InProgress

And

puede alcanzar Archived conforme al Lifecycle definido
```

---

# State Machine

## Escenario — No omitir estados obligatorios

```text
Given

una Assembly en Draft

When

se intenta pasar directamente a InProgress

Then

la transición es rechazada
```

---

## Escenario — No volver desde Completed a InProgress

```text
Given

una Assembly en Completed

When

StartAssembly es ejecutado

Then

la operación es rechazada
```

---

## Escenario — Archived es terminal

```text
Given

una Assembly en Archived

When

se intenta ejecutar una transición de Lifecycle

Then

la operación es rechazada
```

---

# Invariantes

## Escenario — AssemblyId no cambia

```text
Given

una Assembly válida

When

se ejecuta cualquier modificación válida

Then

AssemblyId permanece inmutable
```

---

## Escenario — OrganizationId no cambia

```text
Given

una Assembly válida

When

se ejecuta cualquier modificación válida

Then

OrganizationId permanece inmutable
```

---

## Escenario — Estado siempre válido

```text
Given

una Assembly existente

When

una operación válida es confirmada

Then

AssemblyStatus pertenece al conjunto oficial de estados
```

---

## Escenario — Programación temporalmente válida

```text
Given

una Assembly con programación

Then

ScheduledEnd no precede a ScheduledStart
```

---

## Escenario — No modificación de Archived

```text
Given

AssemblyStatus igual a Archived

When

se intenta modificar cualquier propiedad protegida del Aggregate

Then

la modificación es rechazada
```

---

## Escenario — Referencias externas por identidad

```text
Given

una Assembly relacionada con otros Aggregates

Then

las relaciones externas se mantienen mediante identificadores

And

Assembly no contiene Aggregates externos completos
```

---

# Permissions

## Escenario — Actor autorizado

```text
Given

un Actor que posee el Permission requerido

And

la operación es válida según el dominio

When

el Command es ejecutado

Then

el Aggregate evalúa la operación conforme a sus reglas
```

---

## Escenario — Permission insuficiente

```text
Given

un Actor que no posee el Permission requerido

When

intenta ejecutar un Command protegido

Then

la operación es rechazada

And

Assembly permanece sin cambios

And

Version permanece sin cambios

And

no se produce Domain Event de éxito
```

---

## Escenario — Permission no sustituye invariantes

```text
Given

un Actor autorizado

And

una operación que viola una invariante

When

el Actor ejecuta el Command

Then

la operación es rechazada
```

---

## Escenario — Permission no permite transición inválida

```text
Given

un Actor autorizado

And

una Assembly en un estado incompatible con el Command

When

el Command es ejecutado

Then

la State Machine rechaza la operación
```

---

# Commands

## Escenario — Command representa intención

```text
Given

un Command de Assembly

Then

el Command representa una intención de modificación

And

no representa un hecho consumado
```

---

## Escenario — Command aceptado

```text
Given

un Command válido

And

Permission válido

And

estado válido

And

invariantes satisfechas

When

Assembly procesa el Command

Then

el estado cambia conforme al comportamiento definido

And

Version cambia

And

se produce el Domain Event correspondiente
```

---

## Escenario — Command rechazado

```text
Given

un Command inválido

When

Assembly lo evalúa

Then

el estado permanece sin cambios

And

Version permanece sin cambios

And

no se produce Domain Event de éxito
```

---

# Domain Events

## Escenario — Evento posterior a cambio válido

```text
Given

una modificación válida de Assembly

When

el nuevo estado es confirmado

Then

se produce el Domain Event correspondiente
```

---

## Escenario — Domain Event representa hecho consumado

```text
Given

AssemblyStarted

Then

la Assembly ya alcanzó válidamente InProgress
```

---

## Escenario — No Domain Event de éxito ante rechazo

```text
Given

una operación rechazada

Then

no se produce un Domain Event que represente el cambio solicitado
como hecho consumado
```

---

# AssemblyCreated

## Escenario

```text
Given

una nueva Assembly creada válidamente

Then

se produce AssemblyCreated
```

---

# AssemblyScheduled

## Escenario

```text
Given

una Assembly programada válidamente

Then

se produce AssemblyScheduled
```

---

# AssemblyRescheduled

## Escenario

```text
Given

una Assembly reprogramada válidamente

Then

se produce AssemblyRescheduled
```

---

# AssemblyConvoked

## Escenario

```text
Given

una Assembly convocada válidamente

Then

se produce AssemblyConvoked
```

---

# AssemblyStarted

## Escenario

```text
Given

una Assembly iniciada válidamente

Then

se produce AssemblyStarted
```

---

# AssemblyCompleted

## Escenario

```text
Given

una Assembly completada válidamente

Then

se produce AssemblyCompleted
```

---

# AssemblyCancelled

## Escenario

```text
Given

una Assembly cancelada válidamente

Then

se produce AssemblyCancelled
```

---

# AssemblyArchived

## Escenario

```text
Given

una Assembly archivada válidamente

Then

se produce AssemblyArchived
```

---

# Repository Contract

## Escenario — Recuperación por identidad

```text
Given

una Assembly persistida

When

el Repository la recupera mediante AssemblyId

Then

la Assembly mantiene su identidad

And

mantiene su estado

And

mantiene su Version
```

---

## Escenario — Persistencia del Aggregate completo

```text
Given

una Assembly modificada válidamente

When

el Repository persiste el Aggregate

Then

persiste la unidad de consistencia de Assembly

And

no modifica partes externas como Aggregates independientes
```

---

## Escenario — Assembly inexistente

```text
Given

un AssemblyId que no corresponde a una Assembly existente

When

el Repository intenta recuperarla

Then

no se crea una Assembly implícitamente
```

---

## Escenario — Repository no ejecuta reglas del dominio

```text
Given

una Assembly

When

el Repository persiste o recupera el Aggregate

Then

no redefine State Machine

And

no redefine invariantes

And

no concede Permissions
```

---

# Versioning

## Escenario — Modificación válida cambia Version

```text
Given

Assembly Version igual a N

When

ocurre una modificación válida

Then

Assembly Version cambia conforme al modelo de Versioning
```

---

## Escenario — Operación rechazada no cambia Version

```text
Given

Assembly Version igual a N

When

una operación es rechazada

Then

Assembly Version permanece N
```

---

## Escenario — Lectura no cambia Version

```text
Given

Assembly Version igual a N

When

Assembly es consultada

Then

Assembly Version permanece N
```

---

## Escenario — Rehidratación conserva Version

```text
Given

una Assembly persistida con Version N

When

el Repository rehidrata Assembly

Then

Assembly mantiene Version N
```

---

# Concurrencia

## Escenario — Version esperada coincide

```text
Given

ExpectedVersion igual a PersistedVersion

And

la modificación del dominio es válida

When

se intenta persistir la nueva Assembly

Then

la modificación puede ser confirmada conforme al Repository
Contract
```

---

## Escenario — Version esperada no coincide

```text
Given

ExpectedVersion distinta de PersistedVersion

When

se intenta persistir la modificación

Then

la persistencia es rechazada

And

el estado persistido permanece sin cambios

And

no se produce Domain Event de éxito correspondiente a la
operación rechazada
```

---

## Escenario — Prevención de sobrescritura

```text
Given

dos procesos cargan la misma Assembly en la misma Version

And

el primer proceso confirma una modificación válida

When

el segundo proceso intenta confirmar su modificación basada en la
Version anterior

Then

la segunda persistencia es rechazada
```

---

# Consistency Boundary

## Escenario — Una única Aggregate Root

```text
Given

el Aggregate Assembly

Then

Assembly es la única Aggregate Root
```

---

## Escenario — Modificación atómica

```text
Given

una operación que modifica varios conceptos internos de Assembly

When

la operación es confirmada

Then

todos los cambios internos quedan consistentes

Or

ninguno queda confirmado
```

---

## Escenario — No modificación parcial

```text
Given

una operación que no puede completar todas las validaciones

When

la operación falla

Then

Assembly conserva el estado anterior válido
```

---

## Escenario — Proposal permanece fuera

```text
Given

una Proposal relacionada con Assembly

When

Assembly cambia

Then

Proposal no es modificada directamente
```

---

## Escenario — Participation permanece fuera

```text
Given

un proceso de Participation relacionado con Assembly

When

Assembly cambia

Then

Participation no es modificada directamente
```

---

## Escenario — Voting permanece fuera

```text
Given

una Voting relacionada con Assembly

When

Assembly cambia

Then

Voting no es modificada directamente
```

---

## Escenario — Document permanece fuera

```text
Given

un Document relacionado con Assembly

When

Assembly cambia

Then

Document no es modificado directamente
```

---

## Escenario — Notification permanece fuera

```text
Given

una Notification relacionada con Assembly

When

Assembly cambia

Then

Notification no es modificada directamente
```

---

## Escenario — Audit permanece fuera

```text
Given

Audit relacionado con hechos de Assembly

When

Assembly cambia

Then

Audit no es modificado directamente por la Aggregate Root
```

---

# Regla de No Absorción

## Escenario — Relación no implica pertenencia

```text
Given

Assembly relacionada con:

Organization

Territory

Citizen

Membership

Role

Proposal

Participation

Voting

Document

Notification

Audit

Then

estos Aggregates permanecen fuera del Consistency Boundary
```

---

## Escenario — Identificadores externos

```text
Given

Assembly necesita relacionarse con otro Aggregate

Then

la relación se mantiene mediante el identificador correspondiente

And

no mediante una referencia mutable al Aggregate completo
```

---

# Consistencia entre Aggregates

## Escenario — Consistencia eventual

```text
Given

un cambio válido confirmado en Assembly

When

otro Aggregate necesita reaccionar al hecho

Then

la coordinación ocurre fuera de Assembly

And

el otro Aggregate mantiene su propia consistencia
```

---

## Escenario — No transacción distribuida del Aggregate

```text
Given

un proceso que relaciona Assembly con otros Aggregates

When

Assembly ejecuta una modificación

Then

su Consistency Boundary no se amplía para incluir los demás
Aggregates
```

---

# Integration Events

## Escenario — Hecho confirmado puede originar Integration Event

```text
Given

un Domain Event válido de Assembly

And

existe un contrato de interoperabilidad correspondiente

When

el hecho cruza el límite de integración

Then

puede producirse el Integration Event correspondiente
```

---

## Escenario — Operación rechazada no produce Integration Event

```text
Given

un Command rechazado

Then

no se produce un Integration Event que represente el cambio como
hecho confirmado
```

---

## Escenario — AssemblyStartedForIntegration

```text
Given

Assembly alcanzó válidamente InProgress

And

se produjo AssemblyStarted

When

el hecho debe comunicarse externamente

Then

puede producirse AssemblyStartedForIntegration
```

---

## Escenario — AssemblyCompletedForIntegration

```text
Given

Assembly alcanzó válidamente Completed

And

se produjo AssemblyCompleted

When

el hecho debe comunicarse externamente

Then

puede producirse AssemblyCompletedForIntegration
```

---

## Escenario — AssemblyCancelledForIntegration

```text
Given

Assembly alcanzó válidamente Cancelled

And

se produjo AssemblyCancelled

When

el hecho debe comunicarse externamente

Then

puede producirse AssemblyCancelledForIntegration
```

---

## Escenario — Fallo externo no revierte Assembly

```text
Given

un cambio de Assembly válidamente confirmado

And

se produjo el Integration Event correspondiente

When

un consumidor externo falla

Then

el estado confirmado de Assembly permanece sin cambios
```

---

# Read Model

## Escenario — Read Model representa hechos confirmados

```text
Given

una Assembly cuyo estado fue válidamente confirmado

When

el Read Model es actualizado

Then

la proyección representa el estado confirmado
```

---

## Escenario — Lectura no modifica Assembly

```text
Given

una Assembly existente

When

se consulta su Read Model

Then

Assembly permanece sin cambios

And

Version permanece sin cambios

And

no se produce Domain Event de modificación
```

---

## Escenario — Command rechazado no se proyecta

```text
Given

un Command rechazado

When

el Read Model representa los hechos confirmados

Then

el cambio solicitado no aparece como estado válido
```

---

## Escenario — Proyección reconstruible

```text
Given

los Domain Events oficiales necesarios para reconstruir una
proyección

When

se ejecuta la reconstrucción del Read Model

Then

la proyección puede regenerarse

And

Assembly no es modificada
```

---

## Escenario — Consistencia eventual del Read Model

```text
Given

Assembly ha confirmado un nuevo estado

And

la proyección todavía representa el estado anterior

Then

puede existir temporalmente una diferencia entre Write Model y
Read Model

And

esa diferencia no modifica el estado oficial de Assembly
```

---

# Seguridad

## Escenario — Assembly no almacena credenciales

```text
Given

una Assembly válida

Then

su estado no contiene:

Passwords

Tokens

JWT

Private Keys

Secrets

Session Credentials
```

---

## Escenario — Read Model no expone secretos

```text
Given

un Read Model de Assembly

Then

la proyección no contiene credenciales ni secretos del sistema
```

---

## Escenario — Integration Event no expone secretos

```text
Given

un Integration Event de Assembly

Then

el evento no contiene credenciales ni secretos
```

---

# Dependencias

## Escenario — Dominio independiente de Infrastructure

```text
Given

el modelo de Assembly

Then

su comportamiento conceptual no depende de:

Database

ORM

HTTP

OAuth

JWT

Frameworks
```

---

## Escenario — Repository implementable por Infrastructure

```text
Given

el Repository Contract de Assembly

Then

Infrastructure puede implementarlo sin modificar la semántica del
dominio
```

---

# Pruebas de Operaciones Públicas

Las operaciones conceptuales definidas para Assembly deben poseer
escenarios que verifiquen comportamiento válido y comportamiento
rechazado cuando corresponda.

Como mínimo:

```text
create()

schedule()

convoke()

reschedule()

changeType()

rename()

changePurpose()

changeDescription()

changeMode()

changeLocation()

start()

complete()

cancel()

archive()

updateConvocation()

updateRules()
```

Cada prueba debe utilizar las reglas establecidas por los
documentos oficiales del Aggregate.

---

# Test de create()

```text
Given

datos válidos de creación

When

create() es ejecutado

Then

se obtiene una Assembly válida

And

se produce AssemblyCreated
```

---

# Test de schedule()

```text
Given

Assembly en Draft

When

schedule() recibe una programación válida

Then

Assembly alcanza Scheduled

And

se produce AssemblyScheduled
```

---

# Test de reschedule()

```text
Given

Assembly en un estado que permite reprogramación

When

reschedule() recibe nueva programación válida

Then

la programación cambia

And

se produce AssemblyRescheduled
```

---

# Test de convoke()

```text
Given

Assembly en Scheduled

And

condiciones válidas de convocatoria

When

convoke() es ejecutado

Then

Assembly alcanza Convoked

And

se produce AssemblyConvoked
```

---

# Test de start()

```text
Given

Assembly en Convoked

And

condiciones de realización satisfechas

When

start() es ejecutado

Then

Assembly alcanza InProgress

And

se produce AssemblyStarted
```

---

# Test de complete()

```text
Given

Assembly en InProgress

When

complete() es ejecutado válidamente

Then

Assembly alcanza Completed

And

se produce AssemblyCompleted
```

---

# Test de cancel()

```text
Given

Assembly en un estado que permite cancelación

When

cancel() es ejecutado válidamente

Then

Assembly alcanza Cancelled

And

se produce AssemblyCancelled
```

---

# Test de archive()

```text
Given

Assembly en un estado que permite archivado

When

archive() es ejecutado válidamente

Then

Assembly alcanza Archived

And

se produce AssemblyArchived
```

---

# Test de rename()

```text
Given

Assembly en un estado que permite modificar su nombre

When

rename() recibe un nombre válido

Then

AssemblyName cambia

And

se produce AssemblyRenamed
```

---

# Test de changeType()

```text
Given

Assembly en un estado que permite modificar AssemblyType

When

changeType() recibe un tipo válido

Then

AssemblyType cambia

And

se produce AssemblyTypeChanged
```

---

# Test de changePurpose()

```text
Given

Assembly en un estado que permite modificar AssemblyPurpose

When

changePurpose() recibe un propósito válido

Then

AssemblyPurpose cambia

And

se produce AssemblyPurposeChanged
```

---

# Test de changeDescription()

```text
Given

Assembly en un estado que permite modificar AssemblyDescription

When

changeDescription() recibe una descripción válida

Then

AssemblyDescription cambia

And

se produce AssemblyDescriptionChanged
```

---

# Test de changeMode()

```text
Given

Assembly en un estado que permite modificar AssemblyMode

When

changeMode() recibe una modalidad válida

Then

AssemblyMode cambia

And

se produce AssemblyModeChanged
```

---

# Test de changeLocation()

```text
Given

Assembly en un estado que permite modificar Location

When

changeLocation() recibe una ubicación válida

Then

Location cambia

And

se produce AssemblyLocationChanged
```

---

# Test de updateConvocation()

```text
Given

Assembly en un estado que permite actualizar Convocation

When

updateConvocation() recibe información válida

Then

la información formal de convocatoria cambia

And

se produce AssemblyConvocationUpdated
```

---

# Test de updateRules()

```text
Given

Assembly en un estado que permite actualizar sus reglas

When

updateRules() recibe reglas válidas

Then

Assembly mantiene un estado consistente

And

Version cambia
```

---

# Rechazo de Operaciones

Toda operación debe poseer escenarios de rechazo cuando:

* el estado actual no permite la operación;
* Permission es insuficiente;
* una invariante sería violada;
* la programación es inválida;
* la modalidad es inválida;
* la ubicación requerida es inválida;
* las condiciones de convocatoria no se cumplen;
* las condiciones de inicio no se cumplen;
* las condiciones de finalización no se cumplen;
* Assembly se encuentra Archived;
* existe conflicto de Version.

---

# Regla ante Rechazo

Todo escenario de rechazo debe verificar:

```text
Aggregate State
    =
Unchanged
```

y:

```text
Version
    =
Unchanged
```

y:

```text
Success Domain Event
    =
Not Produced
```

---

# Test de Atomicidad

## Escenario

```text
Given

una operación válida que modifica múltiples conceptos internos

When

la operación es confirmada

Then

todos los cambios internos quedan confirmados conjuntamente
```

---

## Escenario de fallo

```text
Given

una operación que falla durante la validación del dominio

Then

ningún cambio parcial queda confirmado
```

---

# Test de Consistencia Interna

Después de cada modificación válida deben verificarse nuevamente
las invariantes aplicables.

Debe mantenerse:

```text
Valid Operation

↓

Valid Aggregate State
```

Nunca:

```text
Valid Operation

↓

Temporarily Invalid Aggregate State
```

como resultado confirmado.

---

# Test de No Absorción

Después de cualquier operación válida de Assembly debe poder
verificarse que continúan fuera del Aggregate:

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

---

# Test de Relaciones por Identidad

Las relaciones externas deben continuar representándose mediante:

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

cuando correspondan al modelo.

La presencia de un identificador no debe introducir el Aggregate
completo dentro de Assembly.

---

# Test de Fuente de Verdad

Debe verificarse que:

```text
Assembly Aggregate
```

continúa siendo la autoridad del Write Model.

El Read Model no puede utilizarse para modificar el dominio.

Un Integration Event tampoco puede sustituir la Aggregate Root.

---

# Test de Coherencia entre Documentos

Todo escenario debe respetar simultáneamente:

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
```

Una prueba no puede considerarse válida si contradice cualquiera de
estos contratos oficiales.

---

# Pruebas Positivas

Las pruebas positivas verifican que una operación válida produzca el
resultado definido por el dominio.

Deben comprobar:

* estado origen válido;
* Permission válido cuando corresponda;
* datos válidos;
* invariantes satisfechas;
* transición válida;
* estado destino correcto;
* Version actualizada;
* Domain Event correcto;
* Consistency Boundary preservado.

---

# Pruebas Negativas

Las pruebas negativas verifican que una operación inválida sea
rechazada.

Deben comprobar:

* estado del Aggregate sin cambios;
* Version sin cambios;
* ausencia del Domain Event de éxito;
* ausencia de modificación parcial;
* ausencia de modificación de otros Aggregates.

---

# Pruebas de Lifecycle

Las pruebas de Lifecycle deben verificar:

```text
Draft

Scheduled

Convoked

InProgress

Completed

Cancelled

Archived
```

según las transiciones establecidas oficialmente.

No deben inventar estados intermedios.

---

# Pruebas de State Machine

Las pruebas de State Machine deben verificar tanto:

```text
Allowed Transitions
```

como:

```text
Rejected Transitions
```

utilizando exclusivamente las reglas definidas en
`DOMAIN-006B-State-Machine.md`.

---

# Pruebas de Invariantes

Toda invariante definida en:

```text
DOMAIN-006E-Invariants.md
```

debe poseer al menos un escenario que demuestre:

```text
Invariant Preserved
```

y cuando corresponda:

```text
Invariant Violation
    ↓
Operation Rejected
```

---

# Pruebas de Permissions

Todo Permission definido en:

```text
DOMAIN-006F-Permissions.md
```

debe verificarse mediante escenarios que demuestren:

```text
Authorized Actor
```

y:

```text
Unauthorized Actor
```

sin confundir autorización con validez del dominio.

---

# Pruebas de Repository

El Repository debe verificarse respecto de:

* recuperación por identidad;
* persistencia del Aggregate completo;
* preservación de Version;
* control de concurrencia;
* ausencia de modificación de otros Aggregates;
* independencia del dominio respecto de Infrastructure.

---

# Pruebas de Versioning

Versioning debe verificarse respecto de:

* modificación válida;
* operación rechazada;
* rehidratación;
* lectura;
* concurrencia;
* persistencia basada en Version obsoleta.

---

# Pruebas de Integration Events

Los Integration Events deben verificarse respecto de:

* origen en hechos confirmados;
* ausencia ante operaciones rechazadas;
* separación respecto de Domain Events;
* ausencia de modificación directa de Assembly;
* ausencia de secretos;
* independencia de consumidores;
* preservación del Consistency Boundary.

---

# Pruebas de Read Model

Los Read Models deben verificarse respecto de:

* solo lectura;
* reconstrucción;
* representación de hechos confirmados;
* ausencia de lógica de negocio;
* ausencia de modificación de Version;
* consistencia eventual cuando corresponda;
* separación respecto del Aggregate.

---

# Independencia Tecnológica

Los Test Scenarios conceptuales no deben depender de:

```text
PostgreSQL

MongoDB

MySQL

SQLite

Redis

Kafka

RabbitMQ

HTTP

REST

GraphQL

ORM

Django

FastAPI

React

Next.js
```

Estas tecnologías pertenecen a Infrastructure.

---

# Implementación de Pruebas

La tecnología utilizada para ejecutar los Test Scenarios pertenece
al código y a la infraestructura de pruebas.

Este documento define qué debe verificarse.

No define:

* framework de testing;
* librería de assertions;
* lenguaje de implementación;
* estructura de carpetas de tests;
* motor de persistencia;
* entorno de ejecución.

---

# Regla de Independencia

Debe ser posible verificar conceptualmente las reglas de Assembly
sin depender de componentes externos no pertenecientes al dominio.

Las pruebas de integración técnica se mantienen separadas de las
pruebas conceptuales del Aggregate.

---

# Regla de Determinismo del Dominio

Dadas las mismas:

```text
Preconditions

Aggregate State

Command

Domain Rules
```

el comportamiento del Aggregate debe producir un resultado
coherente con las reglas oficiales.

La infraestructura no debe alterar el significado del resultado del
dominio.

---

# Regla de Trazabilidad

Cada Test Scenario debe poder relacionarse con al menos una regla
oficial de Assembly.

Conceptualmente:

```text
Domain Rule

↓

Test Scenario

↓

Verified Behavior
```

Esto permite que las pruebas actúen como verificación ejecutable del
modelo documentado sin sustituir la documentación conceptual.

---

# Regla de Cobertura Conceptual

La cobertura no debe evaluarse únicamente por líneas de código.

Debe verificarse que existan escenarios para:

* comportamientos válidos;
* comportamientos inválidos;
* estados;
* transiciones;
* invariantes;
* Permissions;
* Domain Events;
* Versioning;
* Consistency Boundary;
* relaciones externas;
* Integration Events;
* Read Models.

---

# Regla de No Inferencia Arquitectónica

Los Test Scenarios no pueden utilizarse para convertir una
posibilidad técnica en una regla oficial de AURA.

Si un comportamiento no está definido por:

```text
DOMAIN-006-Aggregate.md
```

o sus documentos complementarios oficiales, no debe declararse
como requisito del Aggregate únicamente porque resulte conveniente
para una prueba.

---

# Regla de Coherencia Documental

Este documento debe permanecer subordinado a la fuente conceptual
oficial de Assembly.

Debe mantenerse:

```text
DOMAIN-006-Aggregate.md
    │
    ▼
Domain Rules
    │
    ▼
Complementary Documents
    │
    ▼
Test Scenarios
```

No:

```text
Test Scenario
    │
    ▼
New Domain Rule
```

---

# Restricciones

No está permitido:

* introducir nuevos estados mediante pruebas;
* introducir nuevas transiciones mediante pruebas;
* introducir nuevos Commands mediante pruebas;
* introducir nuevos Domain Events mediante pruebas;
* introducir nuevos Integration Events mediante pruebas;
* introducir nuevos Permissions mediante pruebas;
* introducir nuevas invariantes mediante pruebas;
* introducir nuevos Aggregates mediante pruebas;
* modificar el Consistency Boundary mediante pruebas;
* utilizar una prueba para redefinir Repository Contract;
* utilizar una prueba para redefinir Versioning;
* utilizar una prueba para redefinir Read Model;
* utilizar Infrastructure como fuente de reglas del dominio;
* aceptar una operación que viole una invariante;
* aceptar una transición no definida;
* modificar Version después de una operación rechazada;
* producir un Domain Event de éxito después de una operación
  rechazada;
* modificar directamente otro Aggregate desde Assembly;
* considerar un Integration Event como Command;
* considerar un Read Model como Aggregate Root.

---

# Compatibilidad Arquitectónica

Los Test Scenarios son compatibles con:

* Domain-Driven Design;
* Aggregate Pattern;
* Clean Architecture;
* Hexagonal Architecture;
* CQRS;
* Event-Driven Architecture;
* Event Sourcing Compatible;
* Optimistic Concurrency;
* arquitectura distribuida.

Esta compatibilidad no introduce nuevas reglas dentro del
Aggregate.

---

# Principios Arquitectónicos

Los Test Scenarios deben preservar:

```text
Command
    ≠
Domain Event
```

```text
Domain Event
    ≠
Integration Event
```

```text
Write Model
    ≠
Read Model
```

```text
Aggregate
    ≠
Projection
```

```text
Permission
    ≠
Invariant
```

```text
Valid Transition
    ≠
Authorized Actor
```

```text
Aggregate Boundary
    ≠
Entire Business Process
```

```text
Reference
    ≠
Aggregate Ownership
```

```text
Rejected Operation
    =
No Domain Mutation
```

```text
Read
    =
No Domain Mutation
```

```text
Archived
    =
Immutable Aggregate
```

Estas separaciones deben comprobarse mediante los escenarios
correspondientes.

---

# Criterio de Aceptación del Aggregate

Una implementación de Assembly puede considerarse coherente con el
modelo documental únicamente cuando los escenarios aplicables
demuestran que:

* cada transición válida funciona conforme a la State Machine;
* cada transición inválida es rechazada;
* cada invariante permanece protegida;
* cada Command modifica exclusivamente Assembly;
* cada modificación válida actualiza Version;
* cada operación rechazada conserva Version;
* cada Domain Event corresponde a un hecho consumado;
* cada Permission se aplica sin reemplazar las reglas del dominio;
* Repository preserva el Aggregate completo;
* Consistency Boundary permanece intacto;
* otros Aggregates no son modificados directamente;
* Integration Events representan hechos confirmados;
* Read Models permanecen de solo lectura.

---

# Definición de Éxito

Los **Test Scenarios** del Aggregate **Assembly** constituyen la
especificación conceptual oficial para verificar que una
implementación preserve las reglas establecidas por el modelo DDD
de AURA Core.

Cada escenario deriva de las definiciones existentes del Aggregate
y no introduce comportamiento nuevo.

Los escenarios verifican que Assembly mantenga:

* identidad inmutable;
* contexto organizacional consistente;
* contexto territorial mediante referencias;
* Lifecycle válido;
* State Machine válida;
* programación coherente;
* convocatoria coherente;
* modalidad válida;
* ubicación válida cuando corresponda;
* estado válido;
* invariantes protegidas;
* Versioning consistente;
* Permissions separados de las reglas de dominio;
* Domain Events asociados exclusivamente a hechos confirmados;
* Consistency Boundary claramente definido;
* independencia de otros Aggregates;
* Integration Events derivados de hechos confirmados;
* Read Models de solo lectura.

Las operaciones válidas producen cambios consistentes dentro de una
única Assembly.

Las operaciones inválidas son rechazadas sin producir
modificaciones parciales, sin cambiar Version y sin publicar
Domain Events de éxito.

Las relaciones con Organization, Territory, Citizen, Membership,
Role, Proposal, Participation, Voting, Document, Notification y
Audit permanecen fuera del límite transaccional de Assembly.

Los escenarios de integración y lectura verifican que estas
separaciones continúen siendo respetadas fuera del Write Model.

La tecnología utilizada para implementar y ejecutar las pruebas no
forma parte del dominio y no puede redefinir sus reglas.

De esta forma,
**DOMAIN-006M-Test-Scenarios.md** establece el conjunto conceptual
y normativo de escenarios necesarios para verificar el Aggregate
Assembly sin introducir decisiones arquitectónicas adicionales,
preservando el patrón, profundidad, lenguaje ubicuo y principios
Domain-Driven Design consolidados en AURA Core.
