# DOMAIN-006A — Assembly Lifecycle

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
* DOMAIN-006B-State-Machine.md
* DOMAIN-006C-Commands.md
* DOMAIN-006D-Domain-Events.md
* DOMAIN-006E-Invariants.md
* DOMAIN-006F-Permissions.md
* DOMAIN-006G-Repository-Contract.md
* DOMAIN-006I-Versioning.md
* DOMAIN-006J-Consistency-Boundary.md
* DOMAIN-006K-Integration-Events.md
* DOMAIN-006L-Read-Model.md
* DOMAIN-006O-Security-Model.md
* CORE-006-Domain-Invariants.md
* CORE-008-Aggregate-Design-Rules.md
* CORE-011-Repository-Contracts.md

---

# Objetivo

Definir formalmente el **ciclo de vida del Aggregate Assembly**,
estableciendo las etapas conceptuales por las que puede transitar
una reunión desde su creación hasta su cierre operativo y
posterior archivado.

El Lifecycle determina:

* las etapas de existencia de Assembly;
* el significado de cada etapa;
* las condiciones conceptuales para avanzar;
* las condiciones que permiten cancelar una reunión;
* las condiciones que permiten archivar una reunión;
* las restricciones aplicables durante cada etapa;
* los hechos de dominio asociados a cada transición;
* las responsabilidades del Aggregate durante su evolución.

El ciclo de vida forma parte del modelo de dominio de Assembly.

No representa una implementación técnica ni una máquina de
estados de infraestructura.

La definición exacta de estados, transiciones y restricciones
formales se desarrolla en:

```text
DOMAIN-006B-State-Machine.md
```

---

# Principio Fundamental

Una Assembly no constituye únicamente un registro de una reunión.

Posee una existencia temporal y organizacional explícita.

Desde la perspectiva del dominio, una Assembly:

```text
se crea;

se prepara;

se programa;

se convoca;

se inicia;

se desarrolla;

se completa;

y finalmente puede archivarse.
```

Alternativamente, determinadas etapas pueden terminar mediante
cancelación.

Cada etapa posee significado propio dentro del dominio y
determina qué comportamientos pueden ejecutarse sobre el
Aggregate.

El estado de Assembly nunca debe utilizarse únicamente como un
atributo informativo.

El estado participa directamente en la protección de las
invariantes y en la determinación de las operaciones permitidas.

---

# Alcance del Lifecycle

El Lifecycle administra exclusivamente la evolución de:

```text
Assembly
```

No administra el ciclo de vida de:

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

Aunque estos Aggregates puedan relacionarse con una Assembly,
sus ciclos de vida permanecen independientes.

La evolución de Assembly nunca debe utilizarse para modificar
directamente el estado interno de otro Aggregate.

---

# Estados del Ciclo de Vida

El ciclo de vida oficial de Assembly utiliza los siguientes
estados:

```text
Draft

Scheduled

Convoked

InProgress

Completed

Cancelled

Archived
```

Cada estado representa una condición real y significativa de la
reunión dentro del dominio.

Los estados no representan:

* estados de interfaz;
* estados de persistencia;
* estados HTTP;
* estados de sincronización;
* estados de infraestructura.

Representan exclusivamente estados del negocio.

---

# Flujo Principal

El ciclo de vida principal es:

```text
Draft
    │
    ▼
Scheduled
    │
    ▼
Convoked
    │
    ▼
InProgress
    │
    ▼
Completed
    │
    ▼
Archived
```

Este flujo representa la evolución normal de una Assembly que se
crea, se programa, se convoca, se realiza, se completa y
posteriormente se archiva.

Cada transición requiere que las invariantes correspondientes se
encuentren satisfechas.

---

# Flujo de Cancelación

Una Assembly puede abandonar el flujo principal mediante
cancelación mientras todavía no haya sido completada.

Conceptualmente:

```text
Draft ─────────────► Cancelled

Scheduled ─────────► Cancelled

Convoked ──────────► Cancelled
```

Una Assembly cancelada puede posteriormente ser archivada:

```text
Cancelled
    │
    ▼
Archived
```

La cancelación representa un hecho explícito del dominio.

No equivale a:

* eliminar la Assembly;
* borrar su historial;
* archivar automáticamente;
* completar la reunión;
* suspender temporalmente la reunión.

---

# Creación del Aggregate

El Lifecycle comienza cuando se crea una nueva Assembly.

La operación conceptual es:

```text
create()
```

El Command correspondiente es:

```text
CreateAssembly
```

El hecho resultante es:

```text
AssemblyCreated
```

El estado inicial es:

```text
Draft
```

Una Assembly nunca comienza directamente en:

```text
Scheduled

Convoked

InProgress

Completed

Cancelled

Archived
```

La creación establece la identidad inicial y el contexto
organizacional necesario para que el Aggregate exista.

---

# Estado Draft

## Definición

`Draft` representa una Assembly que existe formalmente dentro del
dominio pero cuya preparación todavía no ha alcanzado las
condiciones necesarias para ser considerada programada.

En este estado la reunión puede encontrarse en preparación.

---

## Significado de Dominio

Una Assembly Draft:

* posee AssemblyId;
* pertenece a una Organization;
* posee identidad propia;
* existe dentro del dominio;
* puede todavía requerir información adicional;
* no se considera formalmente programada;
* no se considera formalmente convocada;
* no ha comenzado;
* no ha finalizado.

Draft permite construir de manera controlada la definición de la
reunión sin confundir su existencia con su programación formal.

---

## Información Existente

Como mínimo deben existir:

```text
AssemblyId

OrganizationId

AssemblyStatus

CreatedAt

Version
```

Dependiendo de las invariantes de creación también pueden existir:

```text
AssemblyName

AssemblyType

AssemblyPurpose

TerritoryId

AssemblyDescription
```

---

## Operaciones Conceptualmente Permitidas

Mientras permanezca en Draft pueden permitirse operaciones como:

```text
rename()

changeType()

changePurpose()

changeDescription()

changeModality()

changeLocation()

updateRules()

updateExecutionConditions()

schedule()

cancel()
```

Cada operación continúa sujeta a:

* permisos;
* invariantes;
* reglas del Aggregate;
* Versionado Optimista.

---

## Operaciones No Permitidas

Una Assembly Draft no puede:

```text
convoke()

start()

complete()

archive()
```

salvo que una regla futura del dominio modifique expresamente el
Lifecycle mediante un cambio versionado de la arquitectura.

---

## Salidas de Draft

Las salidas conceptuales son:

```text
Draft
    │
    ├────────► Scheduled
    │
    └────────► Cancelled
```

---

# Programación

Programar una Assembly significa establecer formalmente las
condiciones temporales necesarias para su futura realización.

La operación conceptual es:

```text
schedule()
```

El Command correspondiente es:

```text
ScheduleAssembly
```

El evento esperado es:

```text
AssemblyScheduled
```

La transición es:

```text
Draft
    │
    ▼
Scheduled
```

---

# Condiciones para Programar

Antes de abandonar Draft deben encontrarse satisfechas las
condiciones requeridas por el Aggregate.

Conceptualmente pueden incluir:

* AssemblyName válido;
* AssemblyType válido;
* AssemblyPurpose válido cuando sea obligatorio;
* ScheduledStartAt válido;
* ScheduledEndAt coherente cuando exista;
* TimeZone válido;
* AssemblyModality válida;
* AssemblyLocation válida cuando corresponda;
* reglas obligatorias definidas;
* condiciones organizacionales satisfechas.

La definición definitiva pertenece a:

```text
DOMAIN-006E-Invariants.md
```

---

# Estado Scheduled

## Definición

`Scheduled` representa una Assembly que posee una programación
formal válida pero todavía no ha sido formalmente convocada.

---

## Significado de Dominio

Una Assembly Scheduled:

* existe formalmente;
* posee programación válida;
* tiene definida una fecha de inicio;
* puede poseer una fecha estimada de finalización;
* posee modalidad compatible;
* mantiene las condiciones necesarias para preparar su
  convocatoria;
* todavía no se encuentra InProgress.

La programación no equivale a convocatoria.

---

# Programación y Ejecución

La existencia de:

```text
ScheduledStartAt
```

no provoca automáticamente:

```text
InProgress
```

cuando llega la fecha indicada.

La programación expresa una intención temporal.

El inicio de la reunión constituye un hecho distinto del dominio
y requiere una transición explícita.

Por lo tanto:

```text
CurrentTime >= ScheduledStartAt
```

no implica:

```text
AssemblyStatus = InProgress
```

La transición debe producirse mediante comportamiento del
Aggregate.

---

# Reprogramación

Una Assembly Scheduled puede requerir modificación de su
programación.

La operación conceptual es:

```text
reschedule()
```

El Command correspondiente es:

```text
RescheduleAssembly
```

El evento esperado es:

```text
AssemblyRescheduled
```

La operación puede mantener el estado:

```text
Scheduled
```

mientras modifica información temporal válida.

Conceptualmente:

```text
Scheduled
    │
    │ RescheduleAssembly
    ▼
Scheduled
```

La reprogramación no crea una nueva Assembly.

AssemblyId permanece inmutable.

---

# Reprogramación después de Convocación

Una Assembly ya convocada puede requerir reprogramación en
situaciones permitidas por el dominio.

Esta operación posee consecuencias adicionales debido a que la
convocatoria formal ya ocurrió.

La reprogramación de una Assembly Convoked debe:

* mantener la identidad;
* validar que la reunión todavía no haya comenzado;
* validar las reglas de convocatoria;
* determinar si se requiere una nueva convocatoria;
* producir los Domain Events correspondientes;
* preservar la trazabilidad del cambio.

Las reglas específicas se desarrollan en:

```text
DOMAIN-006B-State-Machine.md

DOMAIN-006C-Commands.md

DOMAIN-006E-Invariants.md
```

---

# Salidas de Scheduled

Conceptualmente:

```text
Scheduled
    │
    ├────────► Convoked
    │
    └────────► Cancelled
```

La reprogramación no constituye necesariamente un cambio de
estado.

---

# Convocación

Convocar una Assembly significa declarar formalmente que la
reunión ha sido convocada conforme a las reglas aplicables.

La operación conceptual es:

```text
convoke()
```

El Command correspondiente es:

```text
ConvokeAssembly
```

El evento esperado es:

```text
AssemblyConvoked
```

La transición principal es:

```text
Scheduled
    │
    ▼
Convoked
```

---

# Convocatoria como Concepto de Dominio

La convocatoria pertenece al Aggregate Assembly porque
representa una condición formal de existencia de la reunión.

Assembly debe conocer si la reunión:

```text
hasBeenConvoked
```

en términos conceptuales.

Sin embargo, Assembly no es responsable de enviar mensajes,
correos electrónicos, SMS, notificaciones push u otros mecanismos
de comunicación.

Debe distinguirse:

```text
Convocation
```

de:

```text
Notification
```

Convocation representa una condición formal de Assembly.

Notification representa un proceso de comunicación perteneciente
a otro Aggregate o Bounded Context.

---

# Condiciones para Convocar

Antes de alcanzar Convoked pueden requerirse:

* programación válida;
* fecha de convocatoria válida;
* plazo de convocatoria válido;
* modalidad definida;
* ubicación definida cuando corresponda;
* propósito definido;
* reglas obligatorias satisfechas;
* condiciones organizacionales satisfechas;
* permisos correspondientes.

La convocatoria no puede violar las invariantes temporales del
Aggregate.

---

# Estado Convoked

## Definición

`Convoked` representa una Assembly formalmente convocada que
todavía no ha comenzado.

---

## Significado de Dominio

Una Assembly Convoked:

* posee identidad;
* pertenece a una Organization;
* posee programación válida;
* posee convocatoria formal;
* conserva su modalidad;
* mantiene las condiciones necesarias para su realización;
* todavía no se encuentra en ejecución.

Debe existir:

```text
ConvokedAt
```

---

# Modificaciones después de Convocación

La convocatoria aumenta el nivel de formalidad de la Assembly.

Por esta razón, modificaciones que eran simples durante Draft o
Scheduled pueden requerir reglas adicionales cuando la Assembly
se encuentra Convoked.

Ejemplos:

```text
changeScheduledStartAt

changeLocation

changeModality

changePurpose

changeAssemblyRules
```

pueden requerir:

* validación adicional;
* nueva convocatoria;
* emisión de eventos;
* notificación posterior mediante otro contexto;
* registro de auditoría.

El Lifecycle no permite asumir que una propiedad modificable en
Draft continúe siendo libremente modificable en Convoked.

---

# Salidas de Convoked

Conceptualmente:

```text
Convoked
    │
    ├────────► InProgress
    │
    └────────► Cancelled
```

---

# Inicio de la Assembly

Iniciar una Assembly significa declarar que la reunión comenzó
efectivamente.

La operación conceptual es:

```text
start()
```

El Command correspondiente es:

```text
StartAssembly
```

El evento esperado es:

```text
AssemblyStarted
```

La transición es:

```text
Convoked
    │
    ▼
InProgress
```

---

# Condiciones para Iniciar

Antes de iniciar deben encontrarse satisfechas todas las
condiciones requeridas por el Aggregate.

Conceptualmente pueden incluir:

* estado Convoked;
* programación válida;
* convocatoria válida;
* modalidad válida;
* ubicación válida cuando corresponda;
* condiciones de realización satisfechas;
* reglas organizacionales satisfechas;
* requisitos de quórum cuando pertenezcan al límite de
  consistencia de Assembly;
* permisos correspondientes.

La fecha programada por sí sola no inicia la Assembly.

---

# StartedAt

Al comenzar formalmente la reunión debe establecerse:

```text
StartedAt
```

StartedAt representa el momento efectivo de inicio.

Debe distinguirse de:

```text
ScheduledStartAt
```

Por lo tanto:

```text
ScheduledStartAt
```

representa planificación.

Mientras:

```text
StartedAt
```

representa un hecho ocurrido.

Ambos conceptos pueden poseer valores diferentes sin perder su
significado de dominio.

---

# Estado InProgress

## Definición

`InProgress` representa una Assembly que se encuentra formalmente
en desarrollo.

---

## Significado de Dominio

Una Assembly InProgress:

* fue creada;
* fue programada;
* fue convocada;
* comenzó formalmente;
* posee StartedAt;
* todavía no ha sido completada;
* todavía no ha sido archivada.

Este estado representa la realización efectiva de la reunión.

---

# Assembly como Contexto de Procesos

Durante InProgress pueden desarrollarse procesos pertenecientes a
otros Aggregates.

Ejemplos:

```text
Participation

Proposal

Voting

Document
```

Sin embargo, estos procesos no pasan a formar parte del
Aggregate Assembly.

Conceptualmente:

```text
Assembly
    │
    ├──────── Participation
    ├──────── Proposal
    ├──────── Voting
    └──────── Document
```

representa colaboración contextual.

No representa composición estructural.

---

# Participación durante InProgress

Una Assembly puede proporcionar el contexto para registrar
participación.

Participation conserva:

* ParticipationId;
* ciclo de vida propio;
* invariantes propias;
* Repository propio;
* Domain Events propios.

Assembly no incorpora cada Participation como entidad interna.

---

# Propuestas durante InProgress

Una Proposal puede ser presentada, tratada o deliberada en el
contexto de una Assembly.

Proposal conserva su propio Aggregate.

Assembly puede ser utilizada como referencia mediante:

```text
AssemblyId
```

La existencia de una Proposal durante la reunión no modifica el
límite de consistencia de Assembly.

---

# Votaciones durante InProgress

Una Voting puede desarrollarse dentro de una Assembly.

Voting administra:

* identidad de la votación;
* opciones;
* elegibilidad;
* votos;
* apertura;
* cierre;
* resultados;
* invariantes propias.

Assembly no absorbe esas responsabilidades.

El Lifecycle de Voting es independiente del Lifecycle de
Assembly.

---

# Documentos durante InProgress

Una Assembly puede originar Documents.

Ejemplos:

```text
actas parciales;

documentos presentados;

antecedentes;

acuerdos;

anexos.
```

Document mantiene su propio ciclo de vida.

Assembly no almacena el contenido documental como estado interno.

---

# Restricciones durante InProgress

Una Assembly InProgress no debe ser tratada como una reunión
todavía libremente configurable.

Cambios estructurales pueden quedar restringidos.

Conceptualmente deben controlarse operaciones sobre:

```text
OrganizationId

AssemblyType

ScheduledStartAt

AssemblyModality

AssemblyLocation

Convocation
```

La modificación permitida o prohibida de cada concepto se define
mediante las invariantes y Commands correspondientes.

---

# Finalización de la Assembly

Completar una Assembly significa declarar que la reunión terminó
formalmente.

La operación conceptual es:

```text
complete()
```

El Command correspondiente es:

```text
CompleteAssembly
```

El evento esperado es:

```text
AssemblyCompleted
```

La transición es:

```text
InProgress
    │
    ▼
Completed
```

---

# Condiciones para Completar

Antes de completar una Assembly deben satisfacerse las
condiciones definidas por el dominio.

Conceptualmente pueden incluir:

* estado InProgress;
* StartedAt existente;
* condiciones de cierre satisfechas;
* ausencia de inconsistencias internas;
* reglas obligatorias de finalización satisfechas;
* permisos correspondientes.

Assembly no debe finalizar automáticamente porque:

```text
CurrentTime >= ScheduledEndAt
```

ScheduledEndAt representa planificación.

Completed representa un hecho explícito del dominio.

---

# CompletedAt

Al finalizar debe establecerse:

```text
CompletedAt
```

CompletedAt:

* representa el momento efectivo de finalización;
* debe ser posterior o igual a StartedAt;
* no debe confundirse con ScheduledEndAt;
* forma parte de la trazabilidad del Aggregate.

---

# Estado Completed

## Definición

`Completed` representa una Assembly que terminó formalmente y
cuya ejecución ya no continúa.

---

## Significado de Dominio

Una Assembly Completed:

* conserva su identidad;
* conserva su OrganizationId;
* conserva su contexto histórico;
* conserva su programación;
* conserva su convocatoria;
* conserva StartedAt;
* posee CompletedAt;
* no vuelve a InProgress mediante una transición ordinaria.

Completed representa el cierre de la realización de la reunión.

No representa todavía necesariamente el archivado histórico.

---

# Completed no Equivale a Archived

Debe mantenerse una separación explícita entre:

```text
Completed
```

y:

```text
Archived
```

Completed significa:

```text
la reunión terminó.
```

Archived significa:

```text
la reunión salió del ciclo operativo y permanece como registro
histórico.
```

Esta separación permite ejecutar procesos posteriores al cierre
sin reabrir la reunión.

---

# Procesos Posteriores a Completed

Después de Completed pueden existir procesos relacionados como:

* generación de actas;
* publicación documental;
* consolidación de resultados;
* procesamiento de Voting;
* emisión de Notifications;
* procesos de Audit;
* generación de Integration Events;
* actualización de Read Models.

Estos procesos no implican que Assembly continúe InProgress.

Tampoco implican que dichos procesos formen parte del Aggregate.

---

# Archivado

Archivar una Assembly significa retirarla del ciclo operativo
manteniendo su identidad y trazabilidad histórica.

La operación conceptual es:

```text
archive()
```

El Command correspondiente es:

```text
ArchiveAssembly
```

El evento esperado es:

```text
AssemblyArchived
```

Las transiciones conceptuales son:

```text
Completed
    │
    ▼
Archived
```

y:

```text
Cancelled
    │
    ▼
Archived
```

---

# Condiciones para Archivar

Una Assembly puede archivarse únicamente desde estados
terminales compatibles.

Los estados conceptualmente archivables son:

```text
Completed

Cancelled
```

No debe archivarse directamente una Assembly:

```text
Draft

Scheduled

Convoked

InProgress
```

sin completar previamente el flujo de dominio correspondiente.

---

# Estado Archived

## Definición

`Archived` representa el estado terminal histórico del
Lifecycle.

---

## Significado de Dominio

Una Assembly Archived:

* conserva AssemblyId;
* conserva OrganizationId;
* conserva su historial;
* conserva sus referencias;
* conserva su Version;
* posee ArchivedAt;
* no participa normalmente en operaciones activas;
* no admite modificaciones ordinarias.

Archived no significa eliminación física.

---

# Archivado y Persistencia

El archivado es un concepto de dominio.

No equivale necesariamente a:

```text
DELETE
```

en una base de datos.

La implementación puede utilizar:

* soft delete;
* estado persistido;
* event stream;
* almacenamiento histórico;
* mecanismos equivalentes.

Estas decisiones pertenecen a Infrastructure.

Desde el dominio, la Assembly continúa existiendo como una
entidad histórica identificable.

---

# Cancelación

Cancelar una Assembly significa declarar formalmente que la
reunión no continuará hacia su realización normal.

La operación conceptual es:

```text
cancel()
```

El Command correspondiente es:

```text
CancelAssembly
```

El evento esperado es:

```text
AssemblyCancelled
```

---

# Estados Cancelables

Conceptualmente pueden cancelarse:

```text
Draft

Scheduled

Convoked
```

Las transiciones son:

```text
Draft
    │
    ▼
Cancelled
```

```text
Scheduled
    │
    ▼
Cancelled
```

```text
Convoked
    │
    ▼
Cancelled
```

---

# Cancelación durante InProgress

Una Assembly que ya se encuentra:

```text
InProgress
```

no debe utilizar automáticamente el mismo concepto de
cancelación que una reunión que todavía no comenzó.

Una interrupción de una reunión ya iniciada constituye un
problema de dominio distinto.

Si AURA requiere representar conceptos como:

```text
Suspended

Interrupted

Aborted
```

deberán incorporarse mediante una evolución explícita del modelo,
sus invariantes y su State Machine.

No deben introducirse implícitamente utilizando Cancelled con un
significado diferente.

---

# Estado Cancelled

## Definición

`Cancelled` representa una Assembly cuya realización fue
cancelada antes de completarse normalmente.

---

## Significado de Dominio

Una Assembly Cancelled:

* conserva su identidad;
* conserva su contexto organizacional;
* conserva la información histórica previa;
* posee CancelledAt;
* no puede iniciar;
* no puede completarse normalmente;
* puede posteriormente archivarse.

La cancelación no elimina la reunión.

---

# CancelledAt

Toda cancelación válida establece:

```text
CancelledAt
```

CancelledAt representa el momento efectivo en que la cancelación
fue aceptada por el dominio.

Cuando las reglas lo requieran también puede existir un concepto
de motivo de cancelación, modelado mediante un Value Object
específico.

---

# Reapertura

El Lifecycle oficial no contempla una transición ordinaria:

```text
Cancelled
    │
    ▼
Scheduled
```

ni:

```text
Completed
    │
    ▼
InProgress
```

La reapertura de una reunión cancelada o completada cambia el
significado histórico de hechos ya consumados.

Si en el futuro el dominio requiere reapertura, deberá
introducirse explícitamente mediante:

* Command específico;
* invariantes específicas;
* Domain Event específico;
* reglas de autorización;
* reglas de auditoría;
* actualización de la State Machine;
* estrategia de versionado del dominio.

No debe implementarse mediante modificación directa del estado.

---

# Eliminación

El Lifecycle oficial de Assembly no contempla un estado:

```text
Deleted
```

La eliminación física no forma parte del ciclo de vida del
Aggregate.

Una Assembly que debe conservar trazabilidad termina mediante:

```text
Archived
```

La política técnica de retención o eliminación de información
pertenece a responsabilidades externas al Aggregate y debe
respetar las obligaciones aplicables al sistema.

---

# Timestamps del Lifecycle

Assembly utiliza timestamps distintos para diferenciar
planificación de hechos ocurridos.

Conceptualmente:

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

Cada timestamp posee significado propio.

---

# CreatedAt

Representa el momento en que nació el Aggregate.

Debe existir desde:

```text
Draft
```

y permanecer inmutable.

---

# ScheduledStartAt

Representa el momento previsto para comenzar.

No demuestra que la reunión haya comenzado.

---

# ScheduledEndAt

Representa el momento previsto para finalizar.

No demuestra que la reunión haya finalizado.

---

# ConvokedAt

Representa el momento en que la convocatoria se formalizó.

Debe existir cuando el estado es:

```text
Convoked

InProgress

Completed
```

y puede conservarse posteriormente en:

```text
Archived
```

---

# StartedAt

Representa el momento efectivo de inicio.

Debe existir en:

```text
InProgress

Completed
```

y conservarse posteriormente en Archived.

---

# CompletedAt

Representa el momento efectivo de finalización normal.

Debe existir en:

```text
Completed
```

y conservarse posteriormente en Archived.

---

# CancelledAt

Representa el momento efectivo de cancelación.

Debe existir en:

```text
Cancelled
```

y conservarse posteriormente en Archived cuando la Assembly
provenga de una cancelación.

---

# ArchivedAt

Representa el momento en que Assembly abandonó el ciclo
operativo.

Debe existir exclusivamente cuando:

```text
AssemblyStatus = Archived
```

---

# Coherencia Temporal

Los timestamps deben mantener coherencia con el Lifecycle.

Ejemplos de reglas conceptuales:

```text
CreatedAt <= ConvokedAt

CreatedAt <= StartedAt

StartedAt <= CompletedAt

CreatedAt <= CancelledAt

CompletedAt <= ArchivedAt
```

cuando los valores correspondientes existan.

Para una Assembly cancelada:

```text
CancelledAt <= ArchivedAt
```

cuando posteriormente sea archivada.

La coherencia temporal completa se define como parte de las
invariantes.

---

# Programación versus Hechos Reales

El modelo diferencia explícitamente:

```text
ScheduledStartAt
```

de:

```text
StartedAt
```

y:

```text
ScheduledEndAt
```

de:

```text
CompletedAt
```

Esto permite representar situaciones reales como:

```text
ScheduledStartAt = 18:00

StartedAt = 18:17
```

sin alterar la semántica del dominio.

De la misma forma:

```text
ScheduledEndAt = 20:00

CompletedAt = 20:36
```

representa una reunión que terminó después de lo programado.

El dominio no debe sobrescribir la programación histórica con los
timestamps efectivos.

---

# Cambios sin Transición de Estado

No toda modificación del Aggregate produce una transición del
Lifecycle.

Ejemplos:

```text
rename()

changeDescription()

changePurpose()

changeLocation()

updateRules()
```

pueden mantener el estado actual cuando las invariantes lo
permitan.

Conceptualmente:

```text
Scheduled
    │
    │ RenameAssembly
    ▼
Scheduled
```

La ausencia de cambio de estado no significa ausencia de cambio
del Aggregate.

Toda modificación válida:

* incrementa Version;
* actualiza UpdatedAt cuando corresponda;
* puede producir Domain Events.

---

# Commands del Lifecycle

Los Commands directamente relacionados con transiciones
principales son:

```text
CreateAssembly

ScheduleAssembly

ConvokeAssembly

StartAssembly

CompleteAssembly

CancelAssembly

ArchiveAssembly
```

Los Commands relacionados con evolución sin cambio obligatorio
de estado pueden incluir:

```text
RescheduleAssembly

RenameAssembly

ChangeAssemblyType

ChangeAssemblyPurpose

ChangeAssemblyDescription

ChangeAssemblyModality

ChangeAssemblyLocation

UpdateAssemblyConvocation

UpdateAssemblyRules

UpdateAssemblyExecutionConditions
```

La definición formal pertenece a:

```text
DOMAIN-006C-Commands.md
```

---

# Domain Events del Lifecycle

Las transiciones principales producen hechos como:

```text
AssemblyCreated

AssemblyScheduled

AssemblyConvoked

AssemblyStarted

AssemblyCompleted

AssemblyCancelled

AssemblyArchived
```

Las modificaciones durante el Lifecycle pueden producir:

```text
AssemblyRescheduled

AssemblyRenamed

AssemblyTypeChanged

AssemblyPurposeChanged

AssemblyDescriptionChanged

AssemblyModalityChanged

AssemblyLocationChanged

AssemblyConvocationUpdated

AssemblyRulesUpdated

AssemblyExecutionConditionsUpdated
```

La definición formal pertenece a:

```text
DOMAIN-006D-Domain-Events.md
```

---

# Relación entre Command, Estado y Evento

Una transición válida sigue conceptualmente:

```text
Command
    │
    ▼
Assembly
    │
    │ valida estado actual
    │ valida invariantes
    │ ejecuta comportamiento
    ▼
Nuevo Estado
    │
    ▼
Domain Event
```

Ejemplo:

```text
StartAssembly
    │
    ▼
Assembly[Convoked]
    │
    │ start()
    ▼
Assembly[InProgress]
    │
    ▼
AssemblyStarted
```

El Command expresa intención.

El estado representa la condición actual.

El Domain Event representa el hecho ocurrido.

Estos conceptos nunca deben intercambiarse.

---

# Estado como Resultado del Comportamiento

El estado no debe modificarse mediante:

```text
assembly.status = InProgress
```

El cambio debe ocurrir mediante comportamiento:

```text
assembly.start()
```

El comportamiento:

* valida el estado actual;
* valida invariantes;
* establece StartedAt;
* cambia AssemblyStatus;
* incrementa Version;
* registra el Domain Event correspondiente.

Esta regla preserva el modelo rico de dominio.

---

# Invariantes del Lifecycle

El Lifecycle debe preservar, como mínimo:

* toda Assembly comienza en Draft;
* AssemblyId permanece inmutable durante todo el Lifecycle;
* OrganizationId permanece inmutable durante todo el Lifecycle;
* Draft no puede pasar directamente a InProgress;
* Scheduled no puede pasar directamente a Completed;
* Convoked no puede pasar directamente a Completed;
* InProgress no puede regresar a Convoked;
* Completed no puede regresar a InProgress;
* Cancelled no puede pasar a InProgress;
* Archived constituye un estado terminal;
* una Assembly Archived no admite transiciones ordinarias;
* StartedAt solo existe después de un inicio válido;
* CompletedAt solo existe después de una finalización válida;
* CancelledAt solo existe después de una cancelación válida;
* ArchivedAt solo existe después de un archivado válido;
* toda transición válida incrementa Version;
* toda transición válida produce el Domain Event correspondiente.

Las invariantes formales se desarrollan en:

```text
DOMAIN-006E-Invariants.md
```

---

# Consistencia del Lifecycle

Cada transición ocurre dentro de una única modificación
consistente del Aggregate.

Una transición como:

```text
Convoked
    │
    ▼
InProgress
```

debe actualizar de manera atómica, desde la perspectiva del
dominio:

```text
AssemblyStatus

StartedAt

UpdatedAt

Version

PendingDomainEvents
```

No debe existir un estado observable donde:

```text
AssemblyStatus = InProgress
```

pero:

```text
StartedAt = null
```

si StartedAt es obligatorio para dicho estado.

---

# Fallo de una Transición

Cuando una transición viola:

* el estado actual;
* una invariante;
* una precondición;
* una regla de dominio;

la operación debe rechazarse completamente.

El Aggregate conserva su estado anterior.

No debe existir una transición parcial.

No debe publicarse un Domain Event que represente una operación
que no ocurrió.

---

# Versionado durante el Lifecycle

Toda transición válida incrementa:

```text
Version
```

Ejemplo conceptual:

```text
Draft
Version 1

    │ ScheduleAssembly
    ▼

Scheduled
Version 2

    │ ConvokeAssembly
    ▼

Convoked
Version 3

    │ StartAssembly
    ▼

InProgress
Version 4
```

Version no representa el estado.

Representa la evolución consistente del Aggregate.

La especificación completa pertenece a:

```text
DOMAIN-006I-Versioning.md
```

---

# Concurrencia

El Lifecycle debe protegerse frente a modificaciones
concurrentes.

Ejemplo:

```text
Actor A
    │
    └── CancelAssembly

Actor B
    │
    └── StartAssembly
```

Si ambos utilizan la misma versión inicial de Assembly, solamente
una modificación compatible con la versión persistida debe
aceptarse primero.

La segunda operación debe reevaluarse contra el nuevo estado del
Aggregate.

Esto evita resultados incompatibles como una Assembly
simultáneamente:

```text
Cancelled
```

e:

```text
InProgress
```

---

# Permisos y Lifecycle

Los permisos determinan quién puede solicitar una transición.

Ejemplos:

```text
Assembly.Create

Assembly.Schedule

Assembly.Convoke

Assembly.Start

Assembly.Complete

Assembly.Cancel

Assembly.Archive
```

Sin embargo, poseer un permiso no garantiza que la transición sea
válida.

Debe cumplirse:

```text
Authorization
        +
Current State
        +
Domain Invariants
        +
Business Rules
        =
Valid Transition
```

La autorización y las invariantes son responsabilidades
diferentes.

---

# Auditoría del Lifecycle

Las transiciones relevantes deben ser trazables.

La trazabilidad puede utilizar:

```text
AssemblyId

CommandId

ActorId

Timestamp

CorrelationId

CausationId

PreviousVersion

NewVersion

DomainEventId
```

Audit puede consumir los eventos resultantes.

Assembly no incorpora el Aggregate Audit dentro de su límite de
consistencia.

---

# Notifications y Lifecycle

Algunas transiciones pueden requerir comunicación hacia actores
del ecosistema.

Ejemplos:

```text
AssemblyConvoked

AssemblyRescheduled

AssemblyCancelled
```

pueden originar Notifications.

El flujo conceptual es:

```text
Assembly
    │
    │ Domain Event
    ▼
Application / Event Handler
    │
    ▼
Notification
```

Assembly no envía directamente:

* correos electrónicos;
* SMS;
* mensajes push;
* mensajes de WhatsApp;
* comunicaciones externas.

---

# Integration Events y Lifecycle

Los cambios del Lifecycle pueden originar Integration Events.

Ejemplo:

```text
AssemblyCompleted
        │
        ▼
Integration Event
        │
        ▼
External System
```

La transformación de Domain Event a Integration Event ocurre
fuera del Aggregate.

La definición formal pertenece a:

```text
DOMAIN-006K-Integration-Events.md
```

---

# Read Models y Lifecycle

Los cambios de estado pueden proyectarse hacia Read Models.

Ejemplos:

```text
AssemblyCalendar

AssemblyDirectory

AssemblyTimeline

AssemblyPublicView
```

Una proyección puede mostrar:

```text
AssemblyId

AssemblyName

ScheduledStartAt

AssemblyStatus
```

El Read Model refleja el Lifecycle.

No lo controla.

---

# Lifecycle y Event Sourcing

El Lifecycle es compatible con Event Sourcing.

Conceptualmente una Assembly puede reconstruirse desde hechos
como:

```text
AssemblyCreated

AssemblyScheduled

AssemblyConvoked

AssemblyStarted

AssemblyCompleted

AssemblyArchived
```

produciendo:

```text
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

La utilización efectiva de Event Sourcing es una decisión
arquitectónica independiente.

El Lifecycle no depende de dicha estrategia de persistencia.

---

# Lifecycle e Infraestructura

El Lifecycle no conoce:

```text
HTTP

REST

GraphQL

MongoDB

PostgreSQL

ORM

OAuth

JWT

FIWARE

NGSI-LD

React

Next.js

FastAPI

Django
```

Ninguna transición depende directamente de infraestructura.

Por ejemplo:

```text
POST /assemblies/{id}/start
```

puede ser una representación HTTP de una intención.

Pero el concepto del dominio continúa siendo:

```text
StartAssembly
```

y el comportamiento:

```text
assembly.start()
```

---

# Lifecycle y FIWARE

Una proyección FIWARE puede reflejar el estado de Assembly.

Por ejemplo:

```text
AssemblyStatus = Convoked
```

puede proyectarse hacia una entidad NGSI-LD.

Sin embargo, FIWARE no controla el Lifecycle del Aggregate.

El flujo correcto es:

```text
Command
    │
    ▼
Assembly
    │
    ▼
Domain Event
    │
    ▼
Integration Event
    │
    ▼
FIWARE Adapter
    │
    ▼
NGSI-LD Entity
```

La fuente de verdad permanece en Assembly.

---

# Recuperación del Aggregate

Cuando Assembly es recuperada desde su Repository debe
restaurarse en un estado válido del Lifecycle.

Una Assembly persistida como:

```text
AssemblyStatus = Completed
```

debe cumplir también las invariantes correspondientes, incluyendo
la existencia de:

```text
StartedAt

CompletedAt
```

La persistencia no puede utilizarse para construir estados que el
Aggregate no permitiría mediante su comportamiento normal.

---

# Reconstrucción

La reconstrucción desde persistencia no representa una nueva
transición del Lifecycle.

Por ejemplo, recuperar:

```text
Assembly[Convoked]
```

no debe producir nuevamente:

```text
AssemblyConvoked
```

La hidratación restaura hechos previamente ocurridos.

No genera nuevos hechos de dominio.

---

# Estado Terminal

El estado terminal oficial del Lifecycle es:

```text
Archived
```

Una vez alcanzado:

```text
Archived
```

no existen transiciones ordinarias posteriores.

Conceptualmente:

```text
Archived
    │
    └── X
```

Cualquier futura necesidad de restauración o reapertura debe
modelarse explícitamente y no mediante modificación directa.

---

# Extensión del Lifecycle

El Lifecycle puede evolucionar si aparecen necesidades reales del
dominio.

Ejemplos futuros podrían incluir:

```text
Suspended

Postponed

Interrupted

Aborted
```

Estos estados no forman parte de la versión 1.0.

No deben utilizarse hasta ser incorporados formalmente.

Agregar un nuevo estado exige revisar, como mínimo:

```text
DOMAIN-006-Aggregate.md

DOMAIN-006A-Lifecycle.md

DOMAIN-006B-State-Machine.md

DOMAIN-006C-Commands.md

DOMAIN-006D-Domain-Events.md

DOMAIN-006E-Invariants.md

DOMAIN-006F-Permissions.md

DOMAIN-006K-Integration-Events.md

DOMAIN-006L-Read-Model.md
```

La extensión del Lifecycle constituye una modificación del modelo
de dominio y no un simple cambio de implementación.

---

# Regla de Evolución Controlada

No se deben introducir estados nuevos para resolver necesidades
de interfaz o infraestructura.

Un nuevo estado solo debe incorporarse cuando represente una
condición del negocio que:

* posea significado propio;
* modifique comportamientos permitidos;
* introduzca invariantes específicas;
* participe en transiciones explícitas;
* requiera trazabilidad como hecho de dominio.

Estados puramente técnicos deben permanecer fuera del Aggregate.

---

# Casos de Uso del Lifecycle

El Lifecycle soporta conceptualmente:

```text
Crear una Assembly.

Preparar su información.

Programar la reunión.

Reprogramar la reunión cuando esté permitido.

Convocar formalmente la reunión.

Modificar información permitida antes del inicio.

Iniciar la reunión.

Desarrollar la reunión.

Completar la reunión.

Cancelar una reunión que todavía no comenzó.

Archivar una reunión completada.

Archivar una reunión cancelada.
```

Cada caso de uso debe respetar el estado actual y las invariantes
del Aggregate.

---

# Restricciones

No está permitido:

* crear una Assembly en un estado distinto de Draft;
* modificar AssemblyStatus directamente;
* omitir transiciones obligatorias;
* iniciar una Assembly Draft;
* iniciar una Assembly Scheduled sin convocatoria cuando la
  convocatoria sea obligatoria;
* completar una Assembly que no esté InProgress;
* continuar normalmente una Assembly Cancelled;
* modificar ordinariamente una Assembly Archived;
* utilizar Archived como sinónimo de Deleted;
* utilizar Completed como sinónimo de Archived;
* utilizar Cancelled como sinónimo de Interrupted;
* utilizar ScheduledStartAt como StartedAt;
* utilizar ScheduledEndAt como CompletedAt;
* publicar eventos de transiciones rechazadas;
* alterar Version directamente;
* utilizar infraestructura para evadir las invariantes del
  Lifecycle.

---

# Relación con State Machine

Lifecycle y State Machine representan conceptos relacionados pero
no idénticos.

**Lifecycle** define:

* las etapas significativas de existencia;
* la semántica de cada estado;
* el significado de las transiciones;
* la evolución conceptual del Aggregate.

**State Machine** define formalmente:

* estados origen;
* estados destino;
* transiciones permitidas;
* transiciones prohibidas;
* guards;
* condiciones;
* Commands asociados;
* Events resultantes.

La definición formal se encuentra en:

```text
DOMAIN-006B-State-Machine.md
```

---

# Relación con Invariants

El Lifecycle establece qué significa cada etapa.

Las invariantes determinan qué condiciones deben mantenerse
siempre.

Ejemplo:

```text
AssemblyStatus = Completed
```

requiere conceptualmente:

```text
StartedAt != null

CompletedAt != null

CompletedAt >= StartedAt
```

La definición normativa completa se encuentra en:

```text
DOMAIN-006E-Invariants.md
```

---

# Relación con Consistency Boundary

Todas las transiciones del Lifecycle ocurren dentro del límite de
consistencia de Assembly.

La transición:

```text
Convoked
    ↓
InProgress
```

no modifica simultáneamente:

```text
Participation

Proposal

Voting

Document
```

Los efectos sobre otros Aggregates ocurren posteriormente
mediante coordinación eventual.

La definición formal del límite se encuentra en:

```text
DOMAIN-006J-Consistency-Boundary.md
```

---

# Principios del Lifecycle

El Lifecycle cumple los siguientes principios:

* toda Assembly comienza en Draft;
* todo estado posee significado de negocio;
* toda transición expresa un cambio real del dominio;
* toda transición es explícita;
* ninguna transición válida viola invariantes;
* ninguna transición modifica otro Aggregate;
* las transiciones son consistentes;
* las transiciones son auditables;
* los hechos consumados producen Domain Events;
* los estados terminales preservan trazabilidad;
* planificación y ejecución real son conceptos diferentes;
* cancelación y finalización son conceptos diferentes;
* finalización y archivado son conceptos diferentes;
* el dominio permanece independiente de infraestructura.

---

# Definición de Éxito

El Lifecycle del Aggregate **Assembly** representa de forma
oficial, explícita y consistente la evolución de una reunión
dentro del ecosistema AURA.

Toda Assembly nace en estado **Draft**, puede ser preparada y
programada hasta alcanzar **Scheduled**, formalmente convocada
hasta alcanzar **Convoked**, iniciada hasta alcanzar
**InProgress**, finalizada hasta alcanzar **Completed** y
posteriormente archivada hasta alcanzar **Archived**.

Cuando la reunión no debe continuar antes de su inicio, el
Lifecycle permite una transición explícita hacia **Cancelled**,
preservando su identidad, información histórica y trazabilidad.

El Lifecycle distingue planificación, convocatoria, ejecución,
finalización, cancelación y archivado como conceptos diferentes
del dominio, evitando que estados técnicos o decisiones de
infraestructura alteren su significado.

Cada transición es controlada por la Aggregate Root, protege las
invariantes, mantiene la consistencia del Aggregate, incrementa
Version y produce los Domain Events correspondientes.

De esta forma, Assembly conserva una evolución determinista,
auditable, tecnológicamente independiente y compatible con
Domain-Driven Design, CQRS, Event-Driven Architecture y una
arquitectura distribuida.
