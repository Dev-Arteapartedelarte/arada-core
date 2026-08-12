# DOMAIN-006B — Assembly State Machine

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
* DOMAIN-006C-Commands.md
* DOMAIN-006D-Domain-Events.md
* DOMAIN-006E-Invariants.md
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

---

# Objetivo

Definir formalmente la **State Machine del Aggregate Assembly**,
estableciendo los estados válidos, las transiciones permitidas,
las transiciones prohibidas, las condiciones de entrada y salida,
los Commands asociados, los Domain Events resultantes y las
invariantes que deben preservarse durante cada cambio de estado.

La State Machine constituye la definición normativa de las
transiciones de estado del Aggregate.

Ninguna transición puede ejecutarse fuera de las reglas
establecidas en este documento.

Assembly nunca modifica su estado mediante asignaciones directas.

Toda transición debe producirse mediante comportamiento explícito
de la Aggregate Root.

---

# Propósito

La State Machine protege la evolución consistente de una
Assembly.

Su propósito es impedir estados imposibles o transiciones que
contradigan el significado del dominio.

La State Machine determina:

* qué estados existen;
* cuál es el estado inicial;
* cuáles son los estados terminales;
* desde qué estado puede ejecutarse cada transición;
* hacia qué estado conduce una transición válida;
* qué precondiciones deben cumplirse;
* qué invariantes deben preservarse;
* qué Command solicita la transición;
* qué Domain Event representa el hecho consumado;
* qué timestamps deben establecerse;
* qué cambios de Version deben producirse;
* qué transiciones deben rechazarse.

La State Machine no administra:

* autenticación;
* autorización técnica;
* persistencia;
* infraestructura;
* APIs;
* interfaces gráficas;
* otros Aggregates.

---

# Principio Fundamental

El estado de Assembly representa una condición real del dominio.

No es un valor decorativo ni un atributo de interfaz.

Por lo tanto:

```text
AssemblyStatus
```

solo puede cambiar como consecuencia de una operación válida de
negocio ejecutada por:

```text
Assembly
```

Nunca debe existir lógica externa equivalente a:

```text
assembly.status = targetStatus
```

El cambio debe ejecutarse mediante comportamiento explícito.

Ejemplo:

```text
assembly.start()
```

La Aggregate Root es responsable de:

* comprobar el estado actual;
* comprobar las precondiciones;
* comprobar las invariantes;
* modificar el estado;
* establecer timestamps;
* incrementar Version;
* registrar el Domain Event correspondiente.

---

# Estados Oficiales

La versión 1.0 de Assembly define los siguientes estados:

```text
Draft

Scheduled

Convoked

InProgress

Completed

Cancelled

Archived
```

Estos estados constituyen el conjunto cerrado de estados
oficiales del Aggregate en esta versión.

No deben utilizarse estados adicionales sin una evolución
explícita del modelo.

---

# Estado Inicial

Toda nueva Assembly comienza exclusivamente en:

```text
Draft
```

La creación conceptual es:

```text
CreateAssembly
        │
        ▼
     Assembly
        │
        ▼
      Draft
```

El evento esperado es:

```text
AssemblyCreated
```

No puede crearse directamente una Assembly en:

```text
Scheduled

Convoked

InProgress

Completed

Cancelled

Archived
```

---

# Estados Operativos

Los estados operativos son:

```text
Draft

Scheduled

Convoked

InProgress
```

Representan etapas en las cuales la Assembly todavía participa
activamente en su ciclo de vida.

---

# Estados de Cierre

Los estados que representan cierre de la realización son:

```text
Completed

Cancelled
```

`Completed` representa una reunión que comenzó y terminó
normalmente.

`Cancelled` representa una reunión cuya realización fue
cancelada antes de completar el flujo normal.

---

# Estado Terminal

El estado terminal oficial es:

```text
Archived
```

Una Assembly Archived no admite transiciones ordinarias
posteriores.

Conceptualmente:

```text
Archived
    │
    └── X
```

---

# Diagrama General de Estados

```text
                         ┌─────────────┐
                         │    Draft    │
                         └──────┬──────┘
                                │
                     ScheduleAssembly
                                │
                                ▼
                         ┌─────────────┐
                         │  Scheduled  │
                         └──────┬──────┘
                                │
                      ConvokeAssembly
                                │
                                ▼
                         ┌─────────────┐
                         │  Convoked   │
                         └──────┬──────┘
                                │
                       StartAssembly
                                │
                                ▼
                         ┌─────────────┐
                         │ InProgress  │
                         └──────┬──────┘
                                │
                     CompleteAssembly
                                │
                                ▼
                         ┌─────────────┐
                         │  Completed  │
                         └──────┬──────┘
                                │
                      ArchiveAssembly
                                │
                                ▼
                         ┌─────────────┐
                         │  Archived   │
                         └─────────────┘
```

Rutas alternativas de cancelación:

```text
Draft ────────────────► Cancelled

Scheduled ────────────► Cancelled

Convoked ─────────────► Cancelled

Cancelled ────────────► Archived
```

---

# Matriz General de Transiciones

| Estado origen | Command            | Estado destino | Domain Event        |
| ------------- | ------------------ | -------------- | ------------------- |
| No existe     | CreateAssembly     | Draft          | AssemblyCreated     |
| Draft         | ScheduleAssembly   | Scheduled      | AssemblyScheduled   |
| Draft         | CancelAssembly     | Cancelled      | AssemblyCancelled   |
| Scheduled     | RescheduleAssembly | Scheduled      | AssemblyRescheduled |
| Scheduled     | ConvokeAssembly    | Convoked       | AssemblyConvoked    |
| Scheduled     | CancelAssembly     | Cancelled      | AssemblyCancelled   |
| Convoked      | RescheduleAssembly | Convoked       | AssemblyRescheduled |
| Convoked      | StartAssembly      | InProgress     | AssemblyStarted     |
| Convoked      | CancelAssembly     | Cancelled      | AssemblyCancelled   |
| InProgress    | CompleteAssembly   | Completed      | AssemblyCompleted   |
| Completed     | ArchiveAssembly    | Archived       | AssemblyArchived    |
| Cancelled     | ArchiveAssembly    | Archived       | AssemblyArchived    |

Las operaciones que modifican información pero no cambian el
estado se documentan posteriormente como **self-transitions
semánticas**.

---

# Regla de Transición

Toda transición válida debe satisfacer:

```text
Current State
    +
Command
    +
Authorization
    +
Preconditions
    +
Domain Invariants
    +
Concurrency Validation
    =
Valid Transition
```

Si cualquiera de estas condiciones falla:

```text
Transition = Rejected
```

El estado permanece sin cambios.

No se publica el Domain Event de transición.

---

# Transición de Creación

## Command

```text
CreateAssembly
```

## Estado origen

No existe Aggregate.

## Estado destino

```text
Draft
```

## Evento esperado

```text
AssemblyCreated
```

## Datos conceptuales mínimos

```text
AssemblyId

OrganizationId

AssemblyName

AssemblyType

CreatedAt

Version
```

AssemblyPurpose puede ser obligatorio según las invariantes de
creación definidas para la versión vigente del dominio.

---

# Guards de Creación

La creación debe rechazarse cuando:

* AssemblyId no sea válido;
* AssemblyId ya exista;
* OrganizationId no sea válido;
* AssemblyName no sea válido;
* AssemblyType no sea válido;
* el actor no posea permiso;
* cualquier invariante de creación sea violada.

---

# Efectos de Creación

Una creación válida establece conceptualmente:

```text
AssemblyStatus = Draft

CreatedAt = Timestamp

UpdatedAt = Timestamp

Version = InitialVersion
```

y registra:

```text
AssemblyCreated
```

---

# Estado Draft

## Definición

`Draft` representa una Assembly existente pero todavía no
formalmente programada.

Es el estado inicial obligatorio.

---

# Guards de Draft

Mientras una Assembly permanezca Draft deben cumplirse:

* AssemblyId válido;
* OrganizationId válido;
* AssemblyStatus igual a Draft;
* CreatedAt existente;
* Version válida;
* ausencia de timestamps incompatibles.

Por ejemplo, una Assembly Draft no debe poseer:

```text
StartedAt
```

ni:

```text
CompletedAt
```

como resultado de operaciones ordinarias.

---

# Transición Draft → Scheduled

## Command

```text
ScheduleAssembly
```

## Estado origen

```text
Draft
```

## Estado destino

```text
Scheduled
```

## Evento esperado

```text
AssemblyScheduled
```

---

# Guards de ScheduleAssembly

Antes de programar deben validarse como mínimo:

* estado actual igual a Draft;
* AssemblyName válido;
* AssemblyType válido;
* AssemblyPurpose válido cuando sea obligatorio;
* ScheduledStartAt existente;
* ScheduledStartAt válido;
* ScheduledEndAt coherente cuando exista;
* TimeZone válido;
* AssemblyModality válida;
* AssemblyLocation compatible cuando corresponda;
* reglas mínimas de la Assembly satisfechas;
* condiciones de dominio necesarias satisfechas;
* actor autorizado;
* Version esperada válida.

---

# Efectos de ScheduleAssembly

Una transición válida establece:

```text
AssemblyStatus = Scheduled
```

actualiza:

```text
UpdatedAt
```

incrementa:

```text
Version
```

y registra:

```text
AssemblyScheduled
```

---

# Transición Draft → Cancelled

## Command

```text
CancelAssembly
```

## Estado origen

```text
Draft
```

## Estado destino

```text
Cancelled
```

## Evento esperado

```text
AssemblyCancelled
```

---

# Guards de Cancelación desde Draft

Debe verificarse:

* AssemblyStatus igual a Draft;
* la Assembly no está archivada;
* existe un motivo válido cuando el dominio lo requiera;
* actor autorizado;
* Version válida.

---

# Efectos de Cancelación desde Draft

Debe establecerse:

```text
AssemblyStatus = Cancelled

CancelledAt = Timestamp
```

Debe actualizarse:

```text
UpdatedAt
```

Debe incrementarse:

```text
Version
```

Debe registrarse:

```text
AssemblyCancelled
```

---

# Estado Scheduled

## Definición

`Scheduled` representa una Assembly con programación formal
válida que todavía no ha sido formalmente convocada.

---

# Guards Permanentes de Scheduled

Una Assembly Scheduled debe mantener:

```text
ScheduledStartAt != null

AssemblyStatus = Scheduled
```

y cuando exista ScheduledEndAt:

```text
ScheduledEndAt > ScheduledStartAt
```

Debe existir:

```text
TimeZone
```

cuando la política temporal del dominio así lo requiera.

No debe existir:

```text
StartedAt
```

ni:

```text
CompletedAt
```

---

# Self-Transition Scheduled → Scheduled

## Command

```text
RescheduleAssembly
```

## Estado origen

```text
Scheduled
```

## Estado destino

```text
Scheduled
```

## Evento esperado

```text
AssemblyRescheduled
```

Esta operación modifica la programación sin modificar la etapa
conceptual del Lifecycle.

---

# Guards de RescheduleAssembly en Scheduled

Debe verificarse:

* estado Scheduled;
* nueva fecha de inicio válida;
* nueva fecha de término válida cuando corresponda;
* TimeZone válida;
* la nueva programación mantiene consistencia;
* actor autorizado;
* Version válida.

---

# Efectos de Reprogramación en Scheduled

Puede modificarse:

```text
ScheduledStartAt

ScheduledEndAt

TimeZone
```

Debe conservarse:

```text
AssemblyId

OrganizationId

AssemblyStatus = Scheduled
```

Debe actualizarse:

```text
UpdatedAt
```

Debe incrementarse:

```text
Version
```

Debe registrarse:

```text
AssemblyRescheduled
```

---

# Transición Scheduled → Convoked

## Command

```text
ConvokeAssembly
```

## Estado origen

```text
Scheduled
```

## Estado destino

```text
Convoked
```

## Evento esperado

```text
AssemblyConvoked
```

---

# Guards de ConvokeAssembly

Debe verificarse:

* estado Scheduled;
* programación válida;
* AssemblyPurpose válido;
* AssemblyModality válida;
* AssemblyLocation compatible cuando corresponda;
* Convocation válida;
* ConvocationDeadline válida cuando corresponda;
* reglas de convocatoria satisfechas;
* condiciones organizacionales satisfechas;
* actor autorizado;
* Version válida.

---

# Efectos de ConvokeAssembly

Debe establecerse:

```text
AssemblyStatus = Convoked

ConvokedAt = Timestamp
```

Puede actualizarse:

```text
ConvocationStatus
```

Debe actualizarse:

```text
UpdatedAt
```

Debe incrementarse:

```text
Version
```

Debe registrarse:

```text
AssemblyConvoked
```

---

# Transición Scheduled → Cancelled

## Command

```text
CancelAssembly
```

## Estado origen

```text
Scheduled
```

## Estado destino

```text
Cancelled
```

## Evento esperado

```text
AssemblyCancelled
```

Debe establecerse:

```text
CancelledAt
```

La programación histórica se conserva.

No debe eliminarse:

```text
ScheduledStartAt

ScheduledEndAt

TimeZone
```

por el solo hecho de cancelar.

---

# Estado Convoked

## Definición

`Convoked` representa una Assembly formalmente convocada que
todavía no ha iniciado.

---

# Guards Permanentes de Convoked

Una Assembly Convoked debe satisfacer:

```text
AssemblyStatus = Convoked

ConvokedAt != null
```

Debe mantener una programación válida.

No debe existir:

```text
StartedAt
```

como resultado de un inicio todavía no ocurrido.

No debe existir:

```text
CompletedAt
```

---

# Self-Transition Convoked → Convoked

Una Assembly Convoked puede permanecer en el mismo estado
mientras determinados atributos cambian mediante Commands
permitidos.

Ejemplo:

```text
RescheduleAssembly
```

puede producir:

```text
Convoked
    │
    ▼
Convoked
```

si las reglas del dominio permiten conservar la convocatoria.

Sin embargo, una reprogramación después de Convoked puede exigir
una actualización formal de convocatoria.

---

# Reprogramación de una Assembly Convoked

## Command

```text
RescheduleAssembly
```

## Estado origen

```text
Convoked
```

## Estado destino

```text
Convoked
```

## Evento esperado

```text
AssemblyRescheduled
```

Pueden producirse adicionalmente eventos de actualización de
convocatoria cuando corresponda.

---

# Guards de Reprogramación después de Convocación

Debe verificarse:

* estado Convoked;
* la Assembly todavía no ha iniciado;
* nueva programación válida;
* reglas de convocatoria compatibles;
* cumplimiento de plazos cuando correspondan;
* permisos adecuados;
* Version válida.

El cambio no debe borrar la convocatoria histórica ya realizada.

---

# Actualización de Convocatoria

Cuando una reprogramación exige actualizar la convocatoria puede
utilizarse:

```text
UpdateAssemblyConvocation
```

con evento:

```text
AssemblyConvocationUpdated
```

Esta operación puede mantener:

```text
AssemblyStatus = Convoked
```

La State Machine distingue una modificación de atributos de una
transición real del Lifecycle.

---

# Transición Convoked → InProgress

## Command

```text
StartAssembly
```

## Estado origen

```text
Convoked
```

## Estado destino

```text
InProgress
```

## Evento esperado

```text
AssemblyStarted
```

---

# Guards de StartAssembly

Debe verificarse como mínimo:

* estado Convoked;
* ConvokedAt existente;
* programación válida;
* AssemblyModality válida;
* ubicación válida cuando corresponda;
* ExecutionConditions satisfechas;
* requisitos de quórum satisfechos cuando formen parte de las
  reglas de Assembly;
* la Assembly no está Cancelled;
* la Assembly no está Archived;
* actor autorizado;
* Version válida.

---

# Relación entre Horario Programado e Inicio

El inicio no debe depender exclusivamente de que:

```text
CurrentTime >= ScheduledStartAt
```

El tiempo programado forma parte de las precondiciones temporales
cuando las reglas lo determinen.

El comienzo real se representa mediante:

```text
StartAssembly
```

y:

```text
AssemblyStarted
```

---

# Efectos de StartAssembly

Debe establecerse:

```text
AssemblyStatus = InProgress

StartedAt = Timestamp
```

Debe actualizarse:

```text
UpdatedAt
```

Debe incrementarse:

```text
Version
```

Debe registrarse:

```text
AssemblyStarted
```

---

# Transición Convoked → Cancelled

## Command

```text
CancelAssembly
```

## Estado origen

```text
Convoked
```

## Estado destino

```text
Cancelled
```

## Evento esperado

```text
AssemblyCancelled
```

Esta transición representa la cancelación de una reunión ya
convocada pero todavía no iniciada.

---

# Consecuencias de Cancelación después de Convocación

La cancelación debe conservar:

```text
ConvokedAt

ScheduledStartAt

ScheduledEndAt

Convocation
```

como información histórica.

El cambio de estado no debe sobrescribir hechos previamente
ocurridos.

---

# Estado InProgress

## Definición

`InProgress` representa una Assembly que comenzó formalmente y
se encuentra en desarrollo.

---

# Guards Permanentes de InProgress

Debe cumplirse:

```text
AssemblyStatus = InProgress

StartedAt != null
```

No debe existir:

```text
CompletedAt
```

antes de una finalización válida.

No debe existir:

```text
ArchivedAt
```

---

# Operaciones durante InProgress

Durante InProgress pueden desarrollarse procesos externos como:

```text
Participation

Proposal

Voting

Document
```

Sin embargo, estos procesos no modifican directamente
AssemblyStatus.

La State Machine de Assembly únicamente responde a operaciones
propias de su Aggregate.

---

# Restricción de Modificaciones durante InProgress

Una Assembly InProgress no puede tratarse como una reunión en
preparación.

Cambios estructurales deben restringirse.

En particular, no deben permitirse de forma ordinaria cambios en:

```text
OrganizationId

AssemblyType

ScheduledStartAt

Convocation
```

cuando alteren hechos históricos o el significado de la reunión
en ejecución.

Las restricciones completas pertenecen a:

```text
DOMAIN-006E-Invariants.md
```

---

# Transición InProgress → Completed

## Command

```text
CompleteAssembly
```

## Estado origen

```text
InProgress
```

## Estado destino

```text
Completed
```

## Evento esperado

```text
AssemblyCompleted
```

---

# Guards de CompleteAssembly

Debe verificarse:

* estado InProgress;
* StartedAt existente;
* condiciones de cierre satisfechas;
* reglas propias de finalización satisfechas;
* coherencia temporal;
* actor autorizado;
* Version válida.

---

# Efectos de CompleteAssembly

Debe establecerse:

```text
AssemblyStatus = Completed

CompletedAt = Timestamp
```

Debe garantizarse:

```text
CompletedAt >= StartedAt
```

Debe actualizarse:

```text
UpdatedAt
```

Debe incrementarse:

```text
Version
```

Debe registrarse:

```text
AssemblyCompleted
```

---

# Cancelación desde InProgress

La State Machine versión 1.0 no contempla:

```text
InProgress
    │
    ▼
Cancelled
```

como transición ordinaria.

Una reunión que ya comenzó y posteriormente debe interrumpirse
representa un concepto diferente de una reunión cancelada antes
de su realización.

Si el dominio requiere ese comportamiento deberán evaluarse
estados explícitos como:

```text
Interrupted

Suspended

Aborted
```

Estos estados no pertenecen a la versión 1.0.

No debe reutilizarse `Cancelled` para ocultar dicha diferencia
semántica.

---

# Estado Completed

## Definición

`Completed` representa una Assembly que comenzó y finalizó
formalmente.

---

# Guards Permanentes de Completed

Debe cumplirse:

```text
AssemblyStatus = Completed

StartedAt != null

CompletedAt != null

CompletedAt >= StartedAt
```

Una Assembly Completed no puede:

```text
start()

complete()
```

nuevamente mediante operaciones ordinarias.

---

# Completed como Estado de Negocio

Completed representa:

```text
la reunión terminó formalmente
```

No representa:

```text
la reunión fue eliminada
```

ni:

```text
la reunión fue archivada
```

El estado permanece disponible para procesos posteriores de
dominio e integración.

---

# Transición Completed → Archived

## Command

```text
ArchiveAssembly
```

## Estado origen

```text
Completed
```

## Estado destino

```text
Archived
```

## Evento esperado

```text
AssemblyArchived
```

---

# Guards de ArchiveAssembly desde Completed

Debe verificarse:

* estado Completed;
* StartedAt existente;
* CompletedAt existente;
* condiciones de archivado satisfechas;
* actor autorizado;
* Version válida.

Los procesos externos pendientes no deben alterar directamente la
State Machine.

Si existe una política que obligue a esperar ciertos procesos,
esa política debe expresarse explícitamente.

---

# Efectos del Archivado desde Completed

Debe establecerse:

```text
AssemblyStatus = Archived

ArchivedAt = Timestamp
```

Debe mantenerse:

```text
StartedAt

CompletedAt
```

Debe incrementarse:

```text
Version
```

Debe registrarse:

```text
AssemblyArchived
```

---

# Estado Cancelled

## Definición

`Cancelled` representa una Assembly cuya realización fue
cancelada antes de alcanzar Completion.

---

# Guards Permanentes de Cancelled

Debe cumplirse:

```text
AssemblyStatus = Cancelled

CancelledAt != null
```

Una Assembly Cancelled no puede:

```text
schedule()

convoke()

start()

complete()
```

mediante operaciones ordinarias.

---

# Preservación Histórica de Cancelled

El estado Cancelled no debe eliminar información histórica
válida.

Por ejemplo, una Assembly cancelada desde Convoked debe conservar:

```text
ScheduledStartAt

ScheduledEndAt

ConvokedAt

Convocation
```

La cancelación agrega un hecho nuevo.

No reescribe el pasado.

---

# Transición Cancelled → Archived

## Command

```text
ArchiveAssembly
```

## Estado origen

```text
Cancelled
```

## Estado destino

```text
Archived
```

## Evento esperado

```text
AssemblyArchived
```

---

# Guards de ArchiveAssembly desde Cancelled

Debe verificarse:

* estado Cancelled;
* CancelledAt existente;
* actor autorizado;
* Version válida;
* condiciones de archivado satisfechas.

---

# Efectos del Archivado desde Cancelled

Debe establecerse:

```text
AssemblyStatus = Archived

ArchivedAt = Timestamp
```

Debe conservarse:

```text
CancelledAt
```

Debe incrementarse:

```text
Version
```

Debe registrarse:

```text
AssemblyArchived
```

---

# Estado Archived

## Definición

`Archived` constituye el estado terminal de Assembly.

---

# Guards Permanentes de Archived

Debe cumplirse:

```text
AssemblyStatus = Archived

ArchivedAt != null
```

La identidad y el historial permanecen disponibles.

---

# Operaciones sobre Archived

Una Assembly Archived no admite operaciones ordinarias que
modifiquen su estado o contenido de negocio.

Conceptualmente deben rechazarse:

```text
ScheduleAssembly

RescheduleAssembly

ConvokeAssembly

StartAssembly

CompleteAssembly

CancelAssembly

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

La consulta continúa permitida conforme a las políticas de
seguridad.

---

# Transiciones Prohibidas

Las siguientes transiciones están prohibidas en la versión 1.0.

---

# Draft → Convoked

```text
Draft
    X
Convoked
```

Motivo:

la Assembly debe poseer primero una programación formal válida.

---

# Draft → InProgress

```text
Draft
    X
InProgress
```

Motivo:

no puede iniciar una reunión que no ha sido programada y
convocada conforme al Lifecycle.

---

# Draft → Completed

```text
Draft
    X
Completed
```

Motivo:

una reunión no puede completarse sin haber iniciado.

---

# Draft → Archived

```text
Draft
    X
Archived
```

Motivo:

el archivado está reservado para estados de cierre compatibles.

Cuando una Draft no debe continuar debe utilizar:

```text
CancelAssembly
```

seguido posteriormente por:

```text
ArchiveAssembly
```

---

# Scheduled → InProgress

```text
Scheduled
    X
InProgress
```

La versión 1.0 requiere:

```text
Scheduled
    ↓
Convoked
    ↓
InProgress
```

La convocatoria formal no puede omitirse silenciosamente.

---

# Scheduled → Completed

```text
Scheduled
    X
Completed
```

Motivo:

la reunión no ha iniciado.

---

# Scheduled → Archived

```text
Scheduled
    X
Archived
```

Debe utilizarse primero una transición de cierre válida.

---

# Convoked → Completed

```text
Convoked
    X
Completed
```

Motivo:

debe existir una transición explícita hacia InProgress.

---

# Convoked → Archived

```text
Convoked
    X
Archived
```

Motivo:

una reunión convocada debe ser realizada o cancelada antes de
archivarse.

---

# InProgress → Draft

```text
InProgress
    X
Draft
```

Los hechos ya ocurridos no se revierten mediante cambio de
estado.

---

# InProgress → Scheduled

```text
InProgress
    X
Scheduled
```

La reunión ya comenzó.

No puede convertirse nuevamente en una simple reunión
programada.

---

# InProgress → Convoked

```text
InProgress
    X
Convoked
```

La convocatoria pertenece a una etapa histórica anterior.

---

# InProgress → Cancelled

```text
InProgress
    X
Cancelled
```

No pertenece al modelo 1.0.

Una interrupción posterior al inicio requiere modelado
específico.

---

# InProgress → Archived

```text
InProgress
    X
Archived
```

Una reunión en ejecución debe completar un flujo de cierre antes
del archivado.

---

# Completed → Draft

```text
Completed
    X
Draft
```

Un hecho completado no se revierte.

---

# Completed → Scheduled

```text
Completed
    X
Scheduled
```

La reunión finalizada no se reprograma como si nunca hubiese
ocurrido.

---

# Completed → Convoked

```text
Completed
    X
Convoked
```

La convocatoria pertenece al pasado.

---

# Completed → InProgress

```text
Completed
    X
InProgress
```

La reapertura no pertenece a la versión 1.0.

---

# Completed → Cancelled

```text
Completed
    X
Cancelled
```

Una reunión ya completada no puede convertirse posteriormente en
una reunión cancelada.

---

# Cancelled → Draft

```text
Cancelled
    X
Draft
```

La cancelación es un hecho consumado.

---

# Cancelled → Scheduled

```text
Cancelled
    X
Scheduled
```

No se permite reactivar una reunión cancelada mediante una
transición ordinaria.

---

# Cancelled → Convoked

```text
Cancelled
    X
Convoked
```

No se permite.

---

# Cancelled → InProgress

```text
Cancelled
    X
InProgress
```

Una reunión cancelada no puede iniciar.

---

# Cancelled → Completed

```text
Cancelled
    X
Completed
```

Una reunión cancelada no puede completarse normalmente.

---

# Archived → *

Toda transición desde Archived hacia cualquier estado operativo
está prohibida:

```text
Archived → Draft       X

Archived → Scheduled   X

Archived → Convoked    X

Archived → InProgress  X

Archived → Completed   X

Archived → Cancelled   X
```

Archived constituye un estado terminal.

---

# Self-Transitions Semánticas

Una modificación válida puede mantener el mismo AssemblyStatus.

Esto no significa que no exista cambio de Aggregate.

Ejemplos:

```text
Draft
    │ RenameAssembly
    ▼
Draft
```

```text
Scheduled
    │ RescheduleAssembly
    ▼
Scheduled
```

```text
Convoked
    │ UpdateAssemblyConvocation
    ▼
Convoked
```

Toda modificación válida puede:

* actualizar UpdatedAt;
* incrementar Version;
* producir Domain Events;
* mantener el mismo AssemblyStatus.

---

# Commands sin Cambio Obligatorio de Estado

Los siguientes Commands pueden mantener el estado dependiendo de
las reglas aplicables:

```text
RenameAssembly

ChangeAssemblyType

ChangeAssemblyPurpose

ChangeAssemblyDescription

ChangeAssemblyModality

ChangeAssemblyLocation

UpdateAssemblyConvocation

UpdateAssemblyRules

UpdateAssemblyExecutionConditions

RescheduleAssembly
```

Que un Command esté conceptualmente disponible no significa que
sea válido en todos los estados.

---

# Matriz de Modificaciones por Estado

La matriz siguiente define disponibilidad conceptual inicial.

| Command                           | Draft |   Scheduled |    Convoked |  InProgress | Completed | Cancelled | Archived |
| --------------------------------- | ----: | ----------: | ----------: | ----------: | --------: | --------: | -------: |
| RenameAssembly                    |    Sí |          Sí | Condicional |          No |        No |        No |       No |
| ChangeAssemblyType                |    Sí | Condicional |          No |          No |        No |        No |       No |
| ChangeAssemblyPurpose             |    Sí |          Sí | Condicional |          No |        No |        No |       No |
| ChangeAssemblyDescription         |    Sí |          Sí |          Sí | Condicional |        No |        No |       No |
| ChangeAssemblyModality            |    Sí |          Sí | Condicional |          No |        No |        No |       No |
| ChangeAssemblyLocation            |    Sí |          Sí | Condicional | Condicional |        No |        No |       No |
| UpdateAssemblyConvocation         |    Sí |          Sí |          Sí |          No |        No |        No |       No |
| UpdateAssemblyRules               |    Sí |          Sí | Condicional | Condicional |        No |        No |       No |
| UpdateAssemblyExecutionConditions |    Sí |          Sí | Condicional |          No |        No |        No |       No |
| RescheduleAssembly                |    No |          Sí | Condicional |          No |        No |        No |       No |

`Condicional` significa que la operación debe satisfacer reglas
adicionales formalizadas en:

```text
DOMAIN-006C-Commands.md

DOMAIN-006E-Invariants.md

DOMAIN-006F-Permissions.md
```

---

# Reglas de Mutabilidad por Etapa

La mutabilidad disminuye a medida que la Assembly avanza en su
Lifecycle.

Conceptualmente:

```text
Draft
    ↓
alta capacidad de preparación

Scheduled
    ↓
capacidad de modificación controlada

Convoked
    ↓
capacidad restringida

InProgress
    ↓
capacidad estructural mínima

Completed
    ↓
inmutabilidad operativa

Cancelled
    ↓
inmutabilidad operativa

Archived
    ↓
inmutabilidad terminal
```

Esta regla protege la historicidad de la reunión.

---

# Guard Conditions

Una transición puede ejecutarse únicamente cuando sus Guards se
encuentran satisfechos.

Los Guards pueden depender de:

```text
CurrentStatus

AssemblyType

AssemblyModality

Schedule

Convocation

ExecutionConditions

AssemblyRules

Timestamps

Version
```

Los Guards no deben depender directamente de detalles de
Infrastructure.

---

# Guards Externos

Algunas precondiciones pueden requerir información externa al
Aggregate.

Ejemplos:

* existencia de Organization;
* existencia de Territory;
* validez de Membership;
* autorización mediante Role;
* permisos del Actor.

Estas comprobaciones deben resolverse antes de invocar el
comportamiento del Aggregate o mediante políticas de dominio
adecuadas.

Assembly no carga directamente otros Aggregates para modificar su
estado.

---

# Guards Internos

Los Guards internos pueden ser evaluados completamente por
Assembly.

Ejemplos:

```text
status == Convoked

started_at is null

cancelled_at is null

archived_at is null

schedule.is_valid()

execution_conditions.are_satisfied()
```

Su representación concreta pertenece a la implementación del
dominio.

---

# Separación entre Guard e Invariante

Un Guard determina si una operación puede ejecutarse desde el
estado actual.

Una invariante determina una condición que debe mantenerse válida
en todo momento.

Ejemplo de Guard:

```text
AssemblyStatus == Convoked
```

para ejecutar:

```text
StartAssembly
```

Ejemplo de invariante:

```text
CompletedAt >= StartedAt
```

cuando ambos valores existen.

Ambos conceptos se complementan pero no son equivalentes.

---

# Reglas de Timestamps por Estado

La State Machine establece coherencia entre estado y timestamps.

---

# Draft

Debe existir:

```text
CreatedAt
```

No deben existir como hechos consumados:

```text
StartedAt

CompletedAt

CancelledAt

ArchivedAt
```

---

# Scheduled

Debe existir:

```text
CreatedAt

ScheduledStartAt
```

Puede existir:

```text
ScheduledEndAt
```

No deben existir:

```text
StartedAt

CompletedAt

CancelledAt

ArchivedAt
```

---

# Convoked

Debe existir:

```text
CreatedAt

ScheduledStartAt

ConvokedAt
```

No deben existir:

```text
StartedAt

CompletedAt

CancelledAt

ArchivedAt
```

---

# InProgress

Debe existir:

```text
CreatedAt

ScheduledStartAt

ConvokedAt

StartedAt
```

No debe existir:

```text
CompletedAt
```

como resultado de una Completion todavía no ejecutada.

---

# Completed

Debe existir:

```text
CreatedAt

StartedAt

CompletedAt
```

Debe cumplirse:

```text
CompletedAt >= StartedAt
```

---

# Cancelled

Debe existir:

```text
CreatedAt

CancelledAt
```

Puede conservar:

```text
ScheduledStartAt

ScheduledEndAt

ConvokedAt
```

dependiendo del punto del Lifecycle donde ocurrió la
cancelación.

---

# Archived

Debe existir:

```text
ArchivedAt
```

Además debe conservar los timestamps históricos aplicables al
camino que llevó al archivado.

Si proviene de Completed:

```text
StartedAt != null

CompletedAt != null
```

Si proviene de Cancelled:

```text
CancelledAt != null
```

---

# Coherencia Temporal

Cuando los timestamps correspondientes existan deben respetarse,
como mínimo:

```text
CreatedAt <= ScheduledStartAt
```

cuando la política del dominio impida programar reuniones en el
pasado.

También:

```text
CreatedAt <= ConvokedAt

StartedAt <= CompletedAt

CompletedAt <= ArchivedAt
```

para una Assembly completada y posteriormente archivada.

Para una Assembly cancelada y posteriormente archivada:

```text
CreatedAt <= CancelledAt <= ArchivedAt
```

Las reglas completas pertenecen a:

```text
DOMAIN-006E-Invariants.md
```

---

# Programación versus Ejecución

La State Machine distingue:

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

Las fechas programadas representan planificación.

Los timestamps efectivos representan hechos consumados.

No debe utilizarse:

```text
ScheduledStartAt
```

como evidencia de que la Assembly inició.

Tampoco:

```text
ScheduledEndAt
```

como evidencia de que la Assembly terminó.

---

# Reglas de Versionado

Toda transición válida incrementa:

```text
Version
```

Conceptualmente:

```text
VersionBefore = N

ValidTransition

VersionAfter = N + 1
```

Una transición rechazada no incrementa Version.

---

# Ejemplo de Versionado

```text
AssemblyCreated
Status = Draft
Version = 1

        │
        │ ScheduleAssembly
        ▼

Status = Scheduled
Version = 2

        │
        │ ConvokeAssembly
        ▼

Status = Convoked
Version = 3

        │
        │ StartAssembly
        ▼

Status = InProgress
Version = 4

        │
        │ CompleteAssembly
        ▼

Status = Completed
Version = 5

        │
        │ ArchiveAssembly
        ▼

Status = Archived
Version = 6
```

---

# Concurrencia

La State Machine debe operar conjuntamente con Versionado
Optimista.

Ejemplo:

```text
Assembly
Status = Convoked
Version = 9
```

Dos actores intentan:

```text
Actor A
StartAssembly
ExpectedVersion = 9
```

y:

```text
Actor B
CancelAssembly
ExpectedVersion = 9
```

Una operación válida puede persistirse primero.

Si StartAssembly gana:

```text
Status = InProgress
Version = 10
```

CancelAssembly con:

```text
ExpectedVersion = 9
```

debe fallar por conflicto de concurrencia.

Después de recargar:

```text
Status = InProgress
```

CancelAssembly debe además ser rechazado por la State Machine
versión 1.0.

---

# Atomicidad de una Transición

Una transición válida debe ser atómica dentro del límite de
consistencia.

Ejemplo de StartAssembly:

```text
Status = Convoked
StartedAt = null
Version = 7
```

no puede quedar parcialmente como:

```text
Status = InProgress
StartedAt = null
Version = 7
```

El resultado válido debe ser coherente:

```text
Status = InProgress
StartedAt = Timestamp
Version = 8
```

junto con:

```text
AssemblyStarted
```

registrado como Domain Event pendiente.

---

# Rechazo de una Transición

Una transición debe rechazarse cuando:

* el estado origen no es válido;
* el estado destino no está permitido;
* el Command no corresponde a la transición;
* el actor no posee permisos;
* las precondiciones no se cumplen;
* una invariante sería violada;
* existe conflicto de Version;
* la Assembly está Archived;
* los datos del Command son inválidos.

---

# Efecto del Rechazo

Cuando una transición es rechazada:

* AssemblyStatus permanece igual;
* los atributos permanecen sin cambios;
* Version no incrementa;
* UpdatedAt no cambia como consecuencia de la operación fallida;
* no se registra el Domain Event de éxito;
* ningún otro Aggregate debe modificarse como consecuencia del
  intento rechazado.

---

# Idempotencia Conceptual

Los Commands no deben asumirse automáticamente idempotentes.

Ejemplo:

```text
StartAssembly
```

ejecutado correctamente desde Convoked produce InProgress.

Un segundo:

```text
StartAssembly
```

contra la misma Assembly ahora InProgress debe rechazarse.

No debe tratarse silenciosamente como una operación exitosa sin
efectos.

La política de idempotencia de transporte puede existir fuera del
Aggregate mediante:

```text
CommandId
```

pero no modifica las reglas de la State Machine.

---

# Commands y Transiciones

La relación oficial principal es:

```text
CreateAssembly
    ↓
Draft
    ↓
AssemblyCreated
```

```text
ScheduleAssembly
    ↓
Draft → Scheduled
    ↓
AssemblyScheduled
```

```text
ConvokeAssembly
    ↓
Scheduled → Convoked
    ↓
AssemblyConvoked
```

```text
StartAssembly
    ↓
Convoked → InProgress
    ↓
AssemblyStarted
```

```text
CompleteAssembly
    ↓
InProgress → Completed
    ↓
AssemblyCompleted
```

```text
CancelAssembly
    ↓
Draft | Scheduled | Convoked → Cancelled
    ↓
AssemblyCancelled
```

```text
ArchiveAssembly
    ↓
Completed | Cancelled → Archived
    ↓
AssemblyArchived
```

---

# Domain Events

Una transición válida produce exactamente los hechos de dominio
correspondientes.

Eventos principales:

```text
AssemblyCreated

AssemblyScheduled

AssemblyConvoked

AssemblyStarted

AssemblyCompleted

AssemblyCancelled

AssemblyArchived
```

Los eventos representan hechos consumados.

Nunca deben publicarse para una transición rechazada.

---

# Eventos de Self-Transition

Las modificaciones sin cambio de AssemblyStatus pueden producir:

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

El estado puede permanecer igual mientras Version avanza.

---

# Eventos y Estado Histórico

Los eventos no deben reinterpretarse retroactivamente.

Si se produjo:

```text
AssemblyConvoked
```

y posteriormente:

```text
AssemblyCancelled
```

ambos hechos permanecen verdaderos.

El segundo evento no elimina el primero.

Conceptualmente:

```text
AssemblyConvoked
        ↓
AssemblyCancelled
```

significa:

```text
la reunión fue convocada
y posteriormente fue cancelada.
```

No significa:

```text
la reunión nunca fue convocada.
```

---

# State Machine y Audit

Las transiciones relevantes deben ser auditables.

Conceptualmente pueden registrarse:

```text
AssemblyId

CommandId

ActorId

PreviousStatus

NewStatus

PreviousVersion

NewVersion

Timestamp

CorrelationId

CausationId

DomainEventId
```

Audit consume hechos posteriores.

Assembly no incorpora Audit dentro de su límite de consistencia.

---

# State Machine y Permissions

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

La definición formal pertenece a:

```text
DOMAIN-006F-Permissions.md
```

La autorización no sustituye los Guards.

Un actor autorizado puede igualmente recibir rechazo si la
transición es inválida.

---

# Ejemplo

Un actor posee:

```text
Assembly.Start
```

pero Assembly se encuentra:

```text
Scheduled
```

El Command:

```text
StartAssembly
```

debe rechazarse.

La autorización permite solicitar la operación.

La State Machine determina que:

```text
Scheduled → InProgress
```

no está permitida.

---

# State Machine y Consistency Boundary

Toda transición modifica exclusivamente:

```text
Assembly
```

y sus elementos internos pertenecientes al mismo límite.

No modifica directamente:

```text
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
```

La definición formal pertenece a:

```text
DOMAIN-006J-Consistency-Boundary.md
```

---

# Efectos sobre Otros Aggregates

Una transición puede generar efectos posteriores mediante
eventos.

Ejemplo:

```text
Scheduled
    │
    │ ConvokeAssembly
    ▼
Convoked
    │
    ▼
AssemblyConvoked
```

Posteriormente:

```text
AssemblyConvoked
    │
    ├────────► Notification
    ├────────► Read Model
    ├────────► Audit
    └────────► Integration
```

Estas reacciones ocurren fuera de la transacción de Assembly.

---

# State Machine y Notification

Notification puede reaccionar a eventos como:

```text
AssemblyConvoked

AssemblyRescheduled

AssemblyCancelled
```

Assembly no cambia de estado esperando que Notification termine.

La entrega de una notificación no forma parte del límite
transaccional de la transición.

---

# State Machine y Integration Events

Los Domain Events pueden transformarse posteriormente en
Integration Events.

Ejemplo:

```text
AssemblyStarted
        │
        ▼
AssemblyStartedIntegrationEvent
```

La transformación ocurre fuera de Assembly.

La State Machine no publica directamente contratos externos.

---

# State Machine y FIWARE

FIWARE puede recibir proyecciones del estado de Assembly.

Por ejemplo:

```text
AssemblyStatus = InProgress
```

puede reflejarse externamente.

Pero FIWARE no puede cambiar directamente:

```text
AssemblyStatus
```

El flujo debe permanecer:

```text
External Intent
    │
    ▼
Application Layer
    │
    ▼
Command
    │
    ▼
Assembly State Machine
    │
    ▼
Domain Event
    │
    ▼
Integration
```

---

# State Machine y Read Model

Los Read Models pueden reflejar el estado actual.

Ejemplo:

```text
AssemblyId

AssemblyName

AssemblyStatus

ScheduledStartAt
```

El Read Model no controla transiciones.

No debe existir lógica como:

```text
UPDATE assembly_read_model
SET status = 'Completed'
```

como mecanismo para completar el Aggregate.

La fuente de verdad del cambio es Assembly.

---

# State Machine y Event Sourcing

En una implementación Event Sourcing, los estados pueden
reconstruirse mediante eventos.

Ejemplo:

```text
AssemblyCreated
        ↓
Draft

AssemblyScheduled
        ↓
Scheduled

AssemblyConvoked
        ↓
Convoked

AssemblyStarted
        ↓
InProgress

AssemblyCompleted
        ↓
Completed

AssemblyArchived
        ↓
Archived
```

La reconstrucción no ejecuta nuevamente Commands.

Tampoco genera nuevos Domain Events.

---

# Hidratación desde Persistencia

La hidratación del Aggregate debe restaurar un estado ya válido.

Recuperar:

```text
AssemblyStatus = Completed
```

requiere que la representación persistida también satisfaga las
invariantes de Completed.

No se permite utilizar la hidratación para introducir un estado
que sería imposible mediante la State Machine.

---

# Restauración de Eventos

Cuando se reconstruye Assembly desde eventos históricos:

```text
AssemblyCreated

AssemblyScheduled

AssemblyConvoked

AssemblyStarted

AssemblyCompleted
```

el resultado debe ser:

```text
AssemblyStatus = Completed
```

sin volver a publicar esos eventos como hechos nuevos.

---

# Reglas para Reapertura

La versión 1.0 no contempla:

```text
Completed → InProgress
```

ni:

```text
Cancelled → Scheduled
```

Si el dominio requiere reapertura deberá incorporar un Command
explícito.

Ejemplo conceptual futuro:

```text
ReopenAssembly
```

con evento específico:

```text
AssemblyReopened
```

Solo podrá incorporarse mediante modificación formal de:

```text
DOMAIN-006-Aggregate.md

DOMAIN-006A-Lifecycle.md

DOMAIN-006B-State-Machine.md

DOMAIN-006C-Commands.md

DOMAIN-006D-Domain-Events.md

DOMAIN-006E-Invariants.md

DOMAIN-006F-Permissions.md
```

La reapertura nunca debe implementarse mediante cambio directo de
Status.

---

# Reglas para Interrupción

La versión 1.0 no define un estado para una Assembly iniciada que
deba interrumpirse.

Por lo tanto no existen todavía:

```text
Interrupted

Suspended

Aborted
```

como AssemblyStatus oficiales.

Si el dominio demuestra la necesidad, deberá evolucionarse la
State Machine explícitamente.

No debe reutilizarse Cancelled con múltiples significados.

---

# Regla de Significado Único

Cada estado debe poseer un significado único.

```text
Draft
```

significa preparación.

```text
Scheduled
```

significa programación formal.

```text
Convoked
```

significa convocatoria formal.

```text
InProgress
```

significa ejecución efectiva.

```text
Completed
```

significa finalización normal.

```text
Cancelled
```

significa cancelación antes de Completion.

```text
Archived
```

significa salida del ciclo operativo.

Un mismo estado no debe utilizarse para representar conceptos
diferentes.

---

# Regla de No Inferencia Técnica

No deben agregarse estados de dominio para representar:

```text
Loading

Saving

Syncing

Publishing

FailedRequest

HTTPError

PendingDatabaseWrite
```

Estos son estados técnicos.

No pertenecen a AssemblyStatus.

---

# Regla de No Inferencia desde UI

La interfaz puede mostrar conceptos como:

```text
Upcoming

Today

Past

Editable

Locked
```

Estos pueden ser derivados del estado y de las fechas.

No necesariamente constituyen estados del Aggregate.

Por ejemplo:

```text
Upcoming
```

puede derivarse de:

```text
AssemblyStatus = Scheduled
AND
ScheduledStartAt > CurrentTime
```

sin introducir `Upcoming` en AssemblyStatus.

---

# Regla de No Inferencia desde Integraciones

Un sistema externo puede utilizar estados distintos.

Ejemplo:

```text
OPEN

CLOSED

CANCELLED
```

Estos estados no deben copiarse automáticamente dentro de
AssemblyStatus.

La traducción debe realizarse mediante una Anti-Corruption Layer
cuando corresponda.

---

# Reglas de Evolución

Agregar, eliminar o cambiar un estado constituye una modificación
estructural del dominio.

Debe evaluarse impacto sobre:

* Commands;
* Domain Events;
* Invariants;
* Permissions;
* Repository;
* Versioning;
* Integration Events;
* Read Models;
* Test Scenarios;
* Security Model;
* documentación externa.

---

# Nuevo Estado

Un nuevo estado solo puede incorporarse cuando:

* represente una condición real del negocio;
* tenga significado propio;
* modifique las operaciones disponibles;
* posea Guards específicos;
* participe en transiciones explícitas;
* requiera invariantes específicas;
* pueda producir hechos de dominio propios.

---

# Ejemplo de Estado Futuro

Si el dominio necesitara representar suspensión temporal de una
reunión ya iniciada, podría evaluarse:

```text
Suspended
```

Pero antes de incorporarlo deben definirse preguntas como:

```text
¿Desde qué estados puede alcanzarse?

¿Puede reanudarse?

¿Qué Command lo provoca?

¿Qué Domain Event se publica?

¿Qué ocurre con StartedAt?

¿Qué permisos requiere?

¿Qué invariantes introduce?

¿Qué ocurre con Voting o Participation?
```

Hasta responder formalmente estas preguntas, el estado no debe
incorporarse.

---

# Pruebas de State Machine

Toda transición debe poseer escenarios de prueba.

Como mínimo:

```text
valid transition

invalid source state

missing precondition

invariant violation

permission denied

concurrency conflict

archived aggregate

duplicate command handling at application boundary
```

Los escenarios formales se desarrollan en:

```text
DOMAIN-006M-Test-Scenarios.md
```

---

# Ejemplo de Transición Válida

Estado inicial:

```text
AssemblyStatus = Scheduled
```

Command:

```text
ConvokeAssembly
```

Precondiciones satisfechas:

```text
ScheduleValid = true

ConvocationValid = true

PermissionGranted = true

VersionMatches = true
```

Resultado:

```text
AssemblyStatus = Convoked

ConvokedAt != null

Version = Version + 1
```

Evento:

```text
AssemblyConvoked
```

---

# Ejemplo de Transición Inválida

Estado inicial:

```text
AssemblyStatus = Draft
```

Command:

```text
StartAssembly
```

Resultado esperado:

```text
Rejected
```

El estado permanece:

```text
Draft
```

No se establece:

```text
StartedAt
```

Version no cambia.

No se publica:

```text
AssemblyStarted
```

---

# Ejemplo de Conflicto de Estado

Estado inicial:

```text
AssemblyStatus = Cancelled
```

Command:

```text
StartAssembly
```

Resultado:

```text
Rejected
```

Razón:

```text
Cancelled → InProgress
```

no es una transición válida.

---

# Ejemplo de Aggregate Archivado

Estado:

```text
AssemblyStatus = Archived
```

Command:

```text
RenameAssembly
```

Resultado:

```text
Rejected
```

Una Assembly Archived no admite modificaciones ordinarias.

---

# Tabla de Estados y Propiedades Obligatorias

| Estado     | CreatedAt | ScheduledStartAt |    ConvokedAt | StartedAt | CompletedAt | CancelledAt | ArchivedAt |
| ---------- | --------: | ---------------: | ------------: | --------: | ----------: | ----------: | ---------: |
| Draft      |        Sí |         Opcional |            No |        No |          No |          No |         No |
| Scheduled  |        Sí |               Sí |            No |        No |          No |          No |         No |
| Convoked   |        Sí |               Sí |            Sí |        No |          No |          No |         No |
| InProgress |        Sí |               Sí |            Sí |        Sí |          No |          No |         No |
| Completed  |        Sí |               Sí |            Sí |        Sí |          Sí |          No |         No |
| Cancelled  |        Sí |    Puede existir | Puede existir |       No* |          No |          Sí |         No |
| Archived   |        Sí |        Histórico |     Histórico | Histórico |   Histórico |   Histórico |         Sí |

`No*` corresponde a la versión 1.0, donde Cancelled representa
cancelación antes del inicio.

Una Assembly iniciada que deba interrumpirse requiere evolución
del modelo.

---

# Tabla de Transiciones Permitidas

| Desde      | Hacia      |                              Permitida |
| ---------- | ---------- | -------------------------------------: |
| Draft      | Scheduled  |                                     Sí |
| Draft      | Cancelled  |                                     Sí |
| Scheduled  | Scheduled  |            Sí, mediante reprogramación |
| Scheduled  | Convoked   |                                     Sí |
| Scheduled  | Cancelled  |                                     Sí |
| Convoked   | Convoked   | Sí, mediante modificaciones permitidas |
| Convoked   | InProgress |                                     Sí |
| Convoked   | Cancelled  |                                     Sí |
| InProgress | Completed  |                                     Sí |
| Completed  | Archived   |                                     Sí |
| Cancelled  | Archived   |                                     Sí |

Toda combinación no incluida debe considerarse prohibida salvo
que un documento oficial posterior modifique explícitamente esta
State Machine.

---

# Regla de Denegación por Defecto

La State Machine utiliza una regla de:

```text
deny by default
```

Una transición es válida únicamente cuando está explícitamente
permitida.

No debe asumirse que una transición es válida por no aparecer
como prohibida.

La ausencia de autorización explícita implica rechazo.

---

# Relación con Lifecycle

`DOMAIN-006A-Lifecycle.md` define el significado conceptual de las
etapas.

Este documento define formalmente cómo se transita entre ellas.

Lifecycle responde:

```text
¿Qué significa estar Convoked?
```

State Machine responde:

```text
¿Desde qué estado puede alcanzarse Convoked y mediante qué
Command?
```

Ambos documentos son complementarios y deben permanecer
consistentes.

---

# Relación con Commands

Cada transición debe ser solicitada mediante un Command explícito.

La especificación formal de payloads, actores, precondiciones y
eventos esperados pertenece a:

```text
DOMAIN-006C-Commands.md
```

La State Machine define qué transición puede producir cada
Command.

---

# Relación con Domain Events

Toda transición válida produce hechos consumados.

La definición formal de:

* EventId;
* AggregateId;
* Version;
* Timestamp;
* Payload;
* CorrelationId;
* CausationId;

pertenece a:

```text
DOMAIN-006D-Domain-Events.md
```

---

# Relación con Invariants

Los Guards controlan la posibilidad de una transición.

Las invariantes protegen la validez permanente del Aggregate.

La especificación normativa completa pertenece a:

```text
DOMAIN-006E-Invariants.md
```

Ninguna transición definida aquí puede interpretarse como una
excepción a una invariante.

---

# Relación con Permissions

Una transición permitida por la State Machine puede igualmente
ser rechazada si el Actor no posee permisos.

La especificación pertenece a:

```text
DOMAIN-006F-Permissions.md
```

State Machine y Permissions deben aplicarse conjuntamente.

---

# Relación con Versioning

Toda transición válida modifica Version.

La política completa de concurrencia optimista pertenece a:

```text
DOMAIN-006I-Versioning.md
```

La State Machine debe evaluarse sobre la versión actual del
Aggregate.

---

# Relación con Consistency Boundary

Las transiciones definidas en este documento afectan
exclusivamente el límite de consistencia de Assembly.

La definición formal pertenece a:

```text
DOMAIN-006J-Consistency-Boundary.md
```

Ninguna transición implica actualización transaccional directa de
otro Aggregate.

---

# Relación con Integration Events

Una transición puede producir un Domain Event que posteriormente
sea transformado en Integration Event.

La definición de contratos externos pertenece a:

```text
DOMAIN-006K-Integration-Events.md
```

La State Machine no depende de sistemas externos para aceptar una
transición interna válida.

---

# Relación con Read Model

Los cambios de AssemblyStatus deben reflejarse eventualmente en
Read Models.

La especificación pertenece a:

```text
DOMAIN-006L-Read-Model.md
```

Los Read Models no determinan el estado oficial del Aggregate.

---

# Relación con Security Model

Los intentos de transición deben respetar las políticas de
seguridad establecidas en:

```text
DOMAIN-006O-Security-Model.md
```

La seguridad técnica permanece separada de las invariantes del
dominio.

---

# Compatibilidad Arquitectónica

La State Machine es compatible con:

* Domain-Driven Design;
* Clean Architecture;
* Hexagonal Architecture;
* CQRS;
* Event-Driven Architecture;
* Event Sourcing;
* Optimistic Concurrency;
* arquitectura distribuida.

La representación concreta puede evolucionar sin cambiar el
significado de los estados y transiciones oficiales.

---

# Independencia Tecnológica

La State Machine no depende de:

```text
Python

FastAPI

Django

Java

JavaScript

TypeScript

React

Next.js

SQL

MongoDB

PostgreSQL

Redis

HTTP

REST

GraphQL

OAuth

JWT

FIWARE

NGSI-LD
```

Estos elementos pertenecen a capas externas.

---

# Reglas de Diseño

La State Machine debe cumplir:

* estado inicial único;
* estados con significado de negocio;
* transiciones explícitas;
* denegación por defecto;
* Guards explícitos;
* invariantes protegidas;
* comportamiento mediante Aggregate Root;
* ausencia de setters públicos;
* Version creciente;
* Domain Events únicamente después de cambios válidos;
* estados terminales explícitos;
* separación entre planificación y ejecución;
* separación entre cancelación y completion;
* separación entre completion y archivado;
* independencia tecnológica;
* consistencia dentro de un único Aggregate.

---

# Definición de Éxito

La State Machine del Aggregate **Assembly** constituye la
definición oficial y normativa de las transiciones de estado de
una reunión dentro del ecosistema AURA.

Toda Assembly comienza en **Draft**, puede avanzar a
**Scheduled**, posteriormente a **Convoked**, luego a
**InProgress**, finalizar en **Completed** y finalmente alcanzar
**Archived**.

Antes de su inicio, una Assembly puede abandonar el flujo normal
mediante una transición explícita hacia **Cancelled**, desde
donde posteriormente puede alcanzar **Archived**.

Cada transición se ejecuta exclusivamente mediante la Aggregate
Root, requiere un Command explícito, valida Guards e invariantes,
respeta permisos, controla concurrencia mediante Versionado
Optimista, actualiza los timestamps correspondientes e incrementa
Version.

Una transición rechazada no modifica parcialmente el Aggregate,
no incrementa Version y no publica el Domain Event de éxito.

La State Machine utiliza denegación por defecto: únicamente las
transiciones expresamente definidas como válidas pueden
ejecutarse.

De esta forma, Assembly mantiene una evolución determinista,
trazable, auditable, consistente e independiente de
infraestructura, preservando los límites del Aggregate y los
principios de Domain-Driven Design.
