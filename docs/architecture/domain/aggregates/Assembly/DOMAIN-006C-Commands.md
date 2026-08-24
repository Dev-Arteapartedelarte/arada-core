# DOMAIN-006C — Assembly Commands

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
* CORE-011-Repository-Contracts.md

---

# Objetivo

Definir los **Commands** que representan intenciones explícitas
de modificar el estado o comportamiento del Aggregate
**Assembly**.

Un Command expresa una solicitud de cambio.

No representa un hecho consumado.

No garantiza que la operación solicitada vaya a ejecutarse.

Antes de ser aceptado debe superar:

* validación estructural;
* autorización;
* validación del estado actual;
* precondiciones;
* Guards de la State Machine;
* invariantes del Aggregate;
* reglas de negocio;
* validación de concurrencia;
* políticas de seguridad aplicables.

Los Commands constituyen la entrada autorizada al modelo de
escritura de Assembly.

Ninguna capa externa debe modificar directamente el estado del
Aggregate.

---

# Propósito

El modelo de Commands permite expresar de manera explícita las
intenciones de negocio que pueden afectar una Assembly.

Cada Command:

* posee un significado de dominio concreto;
* identifica la Assembly objetivo cuando esta ya existe;
* identifica al Actor que solicita la operación;
* conserva información de trazabilidad;
* expresa exclusivamente intención;
* puede ser aceptado o rechazado;
* puede producir uno o más Domain Events;
* nunca representa directamente el estado final del Aggregate.

Los Commands permiten mantener separación entre:

```text
intención
```

y:

```text
hecho consumado
```

Por ejemplo:

```text
StartAssembly
```

representa la intención de iniciar una Assembly.

Mientras:

```text
AssemblyStarted
```

representa el hecho de que la Assembly efectivamente comenzó.

---

# Principios

Todos los Commands de Assembly deben cumplir los siguientes
principios:

* representan una intención de cambio;
* son explícitos;
* poseen semántica de dominio;
* son inmutables;
* poseen identidad propia;
* son auditables;
* contienen únicamente los datos necesarios para expresar la
  intención;
* actúan sobre un único Aggregate Assembly;
* no modifican directamente otros Aggregates;
* deben respetar la State Machine;
* deben preservar todas las invariantes;
* deben respetar Versionado Optimista;
* pueden generar uno o más Domain Events;
* nunca retornan el Aggregate como resultado del Command;
* nunca sustituyen comportamiento de dominio por setters;
* nunca contienen lógica de infraestructura;
* nunca representan hechos consumados.

---

# Command como Intención

Un Command responde conceptualmente a:

```text
¿Qué quiere hacer el Actor?
```

Ejemplos:

```text
CreateAssembly

ScheduleAssembly

ConvokeAssembly

StartAssembly

CompleteAssembly
```

Un Domain Event responde a:

```text
¿Qué ocurrió?
```

Ejemplos:

```text
AssemblyCreated

AssemblyScheduled

AssemblyConvoked

AssemblyStarted

AssemblyCompleted
```

La distinción es obligatoria.

No debe utilizarse un Domain Event como solicitud de cambio.

Tampoco debe utilizarse un Command como registro histórico de un
hecho ocurrido.

---

# Estructura General

Todo Command dirigido a una Assembly existente debe contener,
como mínimo:

```text
CommandId

AssemblyId

OrganizationId

ActorId

ExpectedVersion

Timestamp

CorrelationId

CausationId
```

Los Commands pueden incorporar campos adicionales según la
operación.

---

# CommandId

Identificador único del Command.

```text
CommandId
```

CommandId:

* identifica la intención;
* es inmutable;
* permite trazabilidad;
* puede utilizarse en mecanismos de idempotencia de la capa de
  aplicación;
* no sustituye AssemblyId;
* no forma parte de la identidad del Aggregate.

Dos Commands diferentes no deben compartir CommandId.

---

# AssemblyId

Identifica la Assembly objetivo.

```text
AssemblyId
```

Es obligatorio para Commands dirigidos a una Assembly existente.

El Command:

```text
CreateAssembly
```

puede recibir un AssemblyId previamente generado por la
Application Layer o por una Factory de dominio, según la
estrategia oficial del sistema.

AssemblyId nunca puede ser modificado mediante un Command.

---

# OrganizationId

Identifica la Organization propietaria de la Assembly.

```text
OrganizationId
```

Permite:

* establecer contexto organizacional;
* aplicar autorización;
* evitar operaciones fuera de contexto;
* mantener trazabilidad.

OrganizationId recibido en un Command nunca autoriza el cambio de
Organization propietaria.

Para Aggregates existentes debe ser coherente con el
OrganizationId inmutable de Assembly.

---

# ActorId

Identifica al actor que solicita ejecutar la intención.

```text
ActorId
```

ActorId puede representar la identidad utilizada por la capa de
aplicación para resolver autorización.

Assembly no administra la identidad del Actor.

ActorId no convierte a Citizen, Membership o Role en entidades
internas del Aggregate.

---

# ExpectedVersion

Representa la versión del Aggregate sobre la cual el Actor espera
ejecutar la operación.

```text
ExpectedVersion
```

Permite aplicar:

```text
Optimistic Concurrency Control
```

Cuando:

```text
ExpectedVersion != PersistedVersion
```

la modificación debe rechazarse conforme a:

```text
DOMAIN-006I-Versioning.md
```

---

# Timestamp

Representa el momento en que la intención fue emitida o aceptada
por la frontera de aplicación, según el contrato adoptado por
AURA.

```text
Timestamp
```

No debe utilizarse automáticamente como timestamp de un hecho de
dominio sin que el Aggregate acepte la operación.

Por ejemplo:

```text
StartAssembly.Timestamp
```

no implica por sí mismo:

```text
StartedAt
```

StartedAt se establece únicamente cuando el Command es aceptado y
la operación de inicio ocurre realmente.

---

# CorrelationId

Permite correlacionar múltiples operaciones pertenecientes al
mismo flujo.

```text
CorrelationId
```

Puede utilizarse en:

* trazabilidad;
* observabilidad;
* Integration Events;
* procesos distribuidos;
* auditoría.

No modifica las invariantes de Assembly.

---

# CausationId

Identifica la operación o hecho que provocó el Command.

```text
CausationId
```

Permite reconstruir cadenas causales.

Ejemplo conceptual:

```text
ExternalRequest
      │
      ▼
Command
      │
      ▼
Domain Event
```

La causalidad no modifica el límite de consistencia del
Aggregate.

---

# Metadatos y Payload

Debe distinguirse entre:

```text
Command Metadata
```

y:

```text
Command Payload
```

Los metadatos incluyen conceptualmente:

```text
CommandId

ActorId

Timestamp

CorrelationId

CausationId

ExpectedVersion
```

El Payload contiene exclusivamente los datos específicos
necesarios para ejecutar la intención.

Ejemplo:

```text
ChangeAssemblyLocation
```

puede contener:

```text
AssemblyLocation
```

como Payload.

---

# Validación General

Antes de ejecutar cualquier Command deben verificarse, cuando
corresponda:

* estructura válida;
* CommandId válido;
* AssemblyId válido;
* OrganizationId válido;
* ActorId válido;
* ExpectedVersion válida;
* estado actual permitido;
* permisos del Actor;
* Guards de State Machine;
* precondiciones del Command;
* invariantes actuales;
* invariantes posteriores;
* consistencia temporal;
* consistencia organizacional;
* consistencia del Aggregate.

---

# Flujo General de Ejecución

El flujo conceptual es:

```text
Command
    │
    ▼
Application Layer
    │
    ├── Authorization
    ├── Context Validation
    ├── Repository Load
    └── ExpectedVersion
            │
            ▼
        Assembly
            │
            ├── Guard Validation
            ├── Invariant Validation
            ├── Domain Behavior
            └── State Change
                    │
                    ▼
              Domain Event
                    │
                    ▼
                Repository
```

El Command nunca modifica directamente el Repository.

La Application Layer coordina.

Assembly decide si la intención es válida desde la perspectiva
del dominio.

---

# CreateAssembly

## Objetivo

Crear una nueva Assembly dentro del contexto de una
Organization.

---

## Datos mínimos

```text
CommandId

AssemblyId

OrganizationId

ActorId

AssemblyName

AssemblyType

Timestamp

CorrelationId

CausationId
```

Según las reglas del dominio también puede incluir:

```text
TerritoryId

AssemblyPurpose

AssemblyDescription

AssemblyModality

AssemblyLocation

AssemblyRules

ExecutionConditions
```

---

## Estado origen

No aplica.

El Aggregate todavía no existe.

---

## Estado destino

```text
Draft
```

---

## Precondiciones

* AssemblyId es válido.
* AssemblyId no existe.
* OrganizationId es válido.
* Organization existe según validación externa correspondiente.
* AssemblyName es válido.
* AssemblyType es válido.
* TerritoryId es válido cuando corresponda.
* el Actor posee permiso de creación.
* los datos iniciales satisfacen las invariantes de creación.

---

## Comportamiento esperado

Conceptualmente:

```text
Assembly.create(...)
```

La operación debe:

* crear la Aggregate Root;
* establecer AssemblyId;
* establecer OrganizationId;
* establecer estado Draft;
* establecer CreatedAt;
* establecer UpdatedAt cuando corresponda;
* inicializar Version;
* proteger invariantes iniciales.

---

## Evento esperado

```text
AssemblyCreated
```

---

## Rechazo

Debe rechazarse cuando:

* AssemblyId ya existe;
* OrganizationId no es válido;
* AssemblyName no es válido;
* AssemblyType no es válido;
* las invariantes iniciales fallan;
* el Actor no posee permiso.

---

# ScheduleAssembly

## Objetivo

Programar formalmente una Assembly que actualmente se encuentra
en Draft.

---

## Datos mínimos

```text
CommandId

AssemblyId

OrganizationId

ActorId

ExpectedVersion

ScheduledStartAt

TimeZone

Timestamp

CorrelationId

CausationId
```

Puede incluir:

```text
ScheduledEndAt

AssemblyModality

AssemblyLocation
```

según el estado actual y las reglas aplicables.

---

## Estado origen

```text
Draft
```

---

## Estado destino

```text
Scheduled
```

---

## Precondiciones

* Assembly existe.
* Assembly pertenece a OrganizationId.
* estado actual es Draft.
* AssemblyName es válido.
* AssemblyType es válido.
* AssemblyPurpose está definido cuando sea obligatorio.
* ScheduledStartAt es válido.
* ScheduledEndAt es válido cuando exista.
* ScheduledEndAt es posterior a ScheduledStartAt.
* TimeZone es válido.
* AssemblyModality es válida.
* AssemblyLocation es compatible cuando corresponda.
* las reglas mínimas se encuentran satisfechas.
* el Actor posee permiso de programación.
* ExpectedVersion coincide.

---

## Comportamiento esperado

```text
assembly.schedule(...)
```

La operación debe:

* validar programación;
* actualizar AssemblySchedule;
* actualizar modalidad cuando corresponda;
* actualizar ubicación cuando corresponda;
* cambiar Status a Scheduled;
* actualizar UpdatedAt;
* incrementar Version;
* registrar el hecho ocurrido.

---

## Evento esperado

```text
AssemblyScheduled
```

---

# RescheduleAssembly

## Objetivo

Modificar la programación temporal de una Assembly sin crear una
nueva reunión.

---

## Datos

```text
CommandId

AssemblyId

OrganizationId

ActorId

ExpectedVersion

ScheduledStartAt

ScheduledEndAt

TimeZone

Timestamp

CorrelationId

CausationId
```

ScheduledEndAt puede ser opcional cuando las reglas del dominio
lo permitan.

---

## Estados permitidos

```text
Scheduled

Convoked
```

La ejecución en Convoked está sujeta a restricciones
adicionales.

---

## Estado destino

El estado permanece conceptualmente:

```text
Scheduled
```

si el origen es Scheduled.

Y:

```text
Convoked
```

si el origen es Convoked y la convocatoria continúa siendo
válida.

---

## Precondiciones

* Assembly existe.
* estado actual permite reprogramación.
* la reunión no ha comenzado.
* nueva programación es válida.
* ScheduledEndAt es posterior a ScheduledStartAt cuando exista.
* TimeZone es válido.
* la nueva programación no viola invariantes.
* el Actor posee permiso.
* ExpectedVersion coincide.

---

## Validaciones adicionales en Convoked

Cuando Assembly está Convoked debe evaluarse:

* impacto sobre la convocatoria;
* cumplimiento de plazos;
* necesidad de actualizar Convocation;
* necesidad de nueva comunicación;
* reglas organizacionales aplicables.

Assembly no envía directamente Notifications.

---

## Comportamiento esperado

```text
assembly.reschedule(...)
```

---

## Evento esperado

```text
AssemblyRescheduled
```

Puede producirse adicionalmente, cuando la convocatoria sea
modificada:

```text
AssemblyConvocationUpdated
```

---

# ConvokeAssembly

## Objetivo

Formalizar la convocatoria de una Assembly previamente
programada.

---

## Datos mínimos

```text
CommandId

AssemblyId

OrganizationId

ActorId

ExpectedVersion

ConvocationDate

ConvocationMethod

Timestamp

CorrelationId

CausationId
```

Puede incluir:

```text
ConvocationDeadline

ConvocationReference
```

---

## Estado origen

```text
Scheduled
```

---

## Estado destino

```text
Convoked
```

---

## Precondiciones

* Assembly existe.
* Assembly pertenece a OrganizationId.
* estado actual es Scheduled.
* programación es válida.
* AssemblyPurpose es válido.
* AssemblyModality es válida.
* AssemblyLocation es válida cuando corresponda.
* ConvocationDate es válida.
* ConvocationDeadline es válida cuando exista.
* ConvocationMethod es válido.
* reglas de convocatoria se encuentran satisfechas.
* requisitos organizacionales se encuentran satisfechos.
* el Actor posee permiso de convocatoria.
* ExpectedVersion coincide.

---

## Comportamiento esperado

```text
assembly.convoke(...)
```

La operación debe:

* validar las condiciones de convocatoria;
* establecer Convocation;
* establecer ConvokedAt;
* cambiar Status a Convoked;
* actualizar UpdatedAt;
* incrementar Version.

---

## Evento esperado

```text
AssemblyConvoked
```

---

# RenameAssembly

## Objetivo

Modificar el nombre formal de la Assembly.

---

## Datos

```text
CommandId

AssemblyId

OrganizationId

ActorId

ExpectedVersion

AssemblyName

Timestamp

CorrelationId

CausationId
```

---

## Estados permitidos

```text
Draft

Scheduled
```

Puede permitirse condicionalmente en:

```text
Convoked
```

cuando las reglas formales de la reunión y convocatoria lo
permitan.

---

## Precondiciones

* Assembly existe.
* AssemblyName nuevo es válido.
* AssemblyName nuevo representa un cambio real.
* estado actual permite la modificación.
* el Actor posee permiso.
* ExpectedVersion coincide.

---

## Estado destino

No cambia.

---

## Comportamiento esperado

```text
assembly.rename(...)
```

---

## Evento esperado

```text
AssemblyRenamed
```

---

# ChangeAssemblyType

## Objetivo

Modificar la clasificación conceptual de una Assembly.

---

## Datos

```text
CommandId

AssemblyId

OrganizationId

ActorId

ExpectedVersion

AssemblyType

Timestamp

CorrelationId

CausationId
```

---

## Estados permitidos

```text
Draft
```

Puede permitirse condicionalmente en:

```text
Scheduled
```

cuando el cambio no invalide programación, reglas,
convocatoria futura ni otras invariantes.

---

## Estados no permitidos ordinariamente

```text
Convoked

InProgress

Completed

Cancelled

Archived
```

---

## Precondiciones

* Assembly existe.
* AssemblyType nuevo es válido.
* el nuevo tipo es diferente al actual.
* las reglas actuales son compatibles con el nuevo tipo.
* el estado permite la modificación.
* el Actor posee permiso.
* ExpectedVersion coincide.

---

## Estado destino

No cambia.

---

## Comportamiento esperado

```text
assembly.changeType(...)
```

---

## Evento esperado

```text
AssemblyTypeChanged
```

---

# ChangeAssemblyPurpose

## Objetivo

Modificar el propósito formal de la Assembly.

---

## Datos

```text
CommandId

AssemblyId

OrganizationId

ActorId

ExpectedVersion

AssemblyPurpose

Timestamp

CorrelationId

CausationId
```

---

## Estados permitidos

```text
Draft

Scheduled
```

Puede ser condicional en:

```text
Convoked
```

cuando las reglas de convocatoria lo permitan.

---

## Precondiciones

* Assembly existe.
* AssemblyPurpose nuevo es válido.
* existe cambio real.
* el estado actual permite modificación;
* el cambio no contradice AssemblyType;
* el Actor posee permiso;
* ExpectedVersion coincide.

---

## Estado destino

No cambia.

---

## Evento esperado

```text
AssemblyPurposeChanged
```

---

# ChangeAssemblyDescription

## Objetivo

Modificar la descripción complementaria de la Assembly.

---

## Datos

```text
CommandId

AssemblyId

OrganizationId

ActorId

ExpectedVersion

AssemblyDescription

Timestamp

CorrelationId

CausationId
```

---

## Estados permitidos

```text
Draft

Scheduled

Convoked
```

Puede permitirse condicionalmente en:

```text
InProgress
```

únicamente cuando el cambio no reescriba hechos históricos ni
altere el propósito formal de la reunión.

---

## Estados no modificables

```text
Completed

Cancelled

Archived
```

---

## Estado destino

No cambia.

---

## Evento esperado

```text
AssemblyDescriptionChanged
```

---

# ChangeAssemblyModality

## Objetivo

Modificar la modalidad prevista para la realización de la
Assembly.

---

## Datos

```text
CommandId

AssemblyId

OrganizationId

ActorId

ExpectedVersion

AssemblyModality

Timestamp

CorrelationId

CausationId
```

Puede requerir:

```text
AssemblyLocation
```

dependiendo de la nueva modalidad.

---

## Estados permitidos

```text
Draft

Scheduled
```

Puede ser condicional en:

```text
Convoked
```

---

## Estados no permitidos

```text
InProgress

Completed

Cancelled

Archived
```

---

## Precondiciones

* nueva modalidad es válida;
* existe cambio real;
* Location es compatible con la modalidad;
* reglas de convocatoria permanecen válidas o pueden ser
  actualizadas;
* estado permite la operación;
* Actor posee permiso;
* ExpectedVersion coincide.

---

## Estado destino

No cambia.

---

## Evento esperado

```text
AssemblyModalityChanged
```

---

# ChangeAssemblyLocation

## Objetivo

Modificar la ubicación formal de la Assembly.

---

## Datos

```text
CommandId

AssemblyId

OrganizationId

ActorId

ExpectedVersion

AssemblyLocation

Timestamp

CorrelationId

CausationId
```

---

## Estados permitidos

```text
Draft

Scheduled
```

Puede permitirse condicionalmente en:

```text
Convoked
```

y excepcionalmente durante:

```text
InProgress
```

cuando el concepto de Location permita registrar un cambio real
ocurrido durante la reunión sin reescribir su historia.

La regla concreta debe respetar las invariantes oficiales.

---

## Precondiciones

* Location es válida;
* Location es compatible con AssemblyModality;
* existe cambio real;
* estado permite modificación;
* reglas de convocatoria se preservan;
* Actor posee permiso;
* ExpectedVersion coincide.

---

## Estado destino

No cambia.

---

## Evento esperado

```text
AssemblyLocationChanged
```

---

# UpdateAssemblyConvocation

## Objetivo

Actualizar información formal de convocatoria sin representar una
nueva Assembly.

---

## Datos

```text
CommandId

AssemblyId

OrganizationId

ActorId

ExpectedVersion

Convocation

Timestamp

CorrelationId

CausationId
```

---

## Estados permitidos

```text
Draft

Scheduled

Convoked
```

---

## Propósito

Este Command permite preparar o actualizar la información formal
de Convocation.

No sustituye:

```text
ConvokeAssembly
```

cuando la operación requerida es la transición formal:

```text
Scheduled → Convoked
```

---

## Precondiciones

* Assembly existe;
* Convocation es válida;
* estado permite la actualización;
* la actualización no reescribe hechos consumados;
* si Assembly ya está Convoked, ConvokedAt histórico se preserva;
* Actor posee permiso;
* ExpectedVersion coincide.

---

## Estado destino

No cambia.

---

## Evento esperado

```text
AssemblyConvocationUpdated
```

---

# UpdateAssemblyRules

## Objetivo

Modificar las reglas propias de la Assembly.

---

## Datos

```text
CommandId

AssemblyId

OrganizationId

ActorId

ExpectedVersion

AssemblyRules

Timestamp

CorrelationId

CausationId
```

---

## Estados permitidos

```text
Draft

Scheduled
```

Puede permitirse condicionalmente en:

```text
Convoked

InProgress
```

únicamente cuando la modificación sea semánticamente válida y no
reescriba las condiciones bajo las cuales hechos anteriores ya
ocurrieron.

---

## Precondiciones

* AssemblyRules son válidas;
* no contradicen AssemblyType;
* no contradicen AssemblyModality;
* no contradicen ExecutionConditions;
* no vulneran invariantes;
* estado permite la modificación;
* Actor posee permiso;
* ExpectedVersion coincide.

---

## Estado destino

No cambia.

---

## Evento esperado

```text
AssemblyRulesUpdated
```

---

# UpdateAssemblyExecutionConditions

## Objetivo

Modificar las condiciones necesarias para la realización de la
Assembly.

---

## Datos

```text
CommandId

AssemblyId

OrganizationId

ActorId

ExpectedVersion

ExecutionConditions

Timestamp

CorrelationId

CausationId
```

---

## Estados permitidos

```text
Draft

Scheduled
```

Puede permitirse condicionalmente en:

```text
Convoked
```

si la reunión todavía no ha comenzado y las reglas de
convocatoria permanecen válidas.

---

## Estados no permitidos ordinariamente

```text
InProgress

Completed

Cancelled

Archived
```

---

## Precondiciones

* ExecutionConditions son válidas;
* no contradicen AssemblyRules;
* no contradicen AssemblyType;
* estado permite modificación;
* la modificación no invalida hechos consumados;
* Actor posee permiso;
* ExpectedVersion coincide.

---

## Estado destino

No cambia.

---

## Evento esperado

```text
AssemblyExecutionConditionsUpdated
```

---

# StartAssembly

## Objetivo

Iniciar formalmente una Assembly previamente convocada.

---

## Datos mínimos

```text
CommandId

AssemblyId

OrganizationId

ActorId

ExpectedVersion

Timestamp

CorrelationId

CausationId
```

Puede incorporar datos estrictamente necesarios para evaluar
ExecutionConditions cuando dichos datos formen parte del contrato
del Command.

---

## Estado origen

```text
Convoked
```

---

## Estado destino

```text
InProgress
```

---

## Precondiciones

* Assembly existe;
* pertenece a OrganizationId;
* estado actual es Convoked;
* ConvokedAt existe;
* programación es válida;
* AssemblyModality es válida;
* AssemblyLocation es válida cuando corresponda;
* ExecutionConditions se encuentran satisfechas;
* AssemblyRules permiten iniciar;
* requisitos de quórum están satisfechos cuando formen parte del
  límite de consistencia de Assembly;
* la Assembly no está Cancelled;
* la Assembly no está Archived;
* Actor posee permiso de inicio;
* ExpectedVersion coincide.

---

## Comportamiento esperado

```text
assembly.start()
```

La operación debe:

* validar todos los Guards;
* establecer StartedAt;
* cambiar Status a InProgress;
* actualizar UpdatedAt;
* incrementar Version.

---

## Evento esperado

```text
AssemblyStarted
```

---

# Relación entre StartAssembly y ScheduledStartAt

La existencia de:

```text
ScheduledStartAt
```

no ejecuta automáticamente:

```text
StartAssembly
```

El Command representa una intención explícita.

La hora programada es información temporal del dominio.

El inicio efectivo ocurre únicamente cuando el Aggregate acepta:

```text
StartAssembly
```

y publica:

```text
AssemblyStarted
```

---

# CompleteAssembly

## Objetivo

Finalizar formalmente una Assembly que se encuentra en
ejecución.

---

## Datos mínimos

```text
CommandId

AssemblyId

OrganizationId

ActorId

ExpectedVersion

Timestamp

CorrelationId

CausationId
```

---

## Estado origen

```text
InProgress
```

---

## Estado destino

```text
Completed
```

---

## Precondiciones

* Assembly existe;
* estado actual es InProgress;
* StartedAt existe;
* condiciones de finalización están satisfechas;
* AssemblyRules permiten completar;
* Timestamp efectivo mantiene coherencia temporal;
* Actor posee permiso de finalización;
* ExpectedVersion coincide.

---

## Comportamiento esperado

```text
assembly.complete()
```

La operación debe:

* establecer CompletedAt;
* garantizar CompletedAt >= StartedAt;
* cambiar Status a Completed;
* actualizar UpdatedAt;
* incrementar Version.

---

## Evento esperado

```text
AssemblyCompleted
```

---

# Relación entre CompleteAssembly y ScheduledEndAt

La existencia de:

```text
ScheduledEndAt
```

no ejecuta automáticamente:

```text
CompleteAssembly
```

Tampoco:

```text
CurrentTime >= ScheduledEndAt
```

implica que la reunión haya terminado.

La finalización es un hecho explícito del dominio.

---

# CancelAssembly

## Objetivo

Cancelar formalmente una Assembly antes de que complete su flujo
normal de realización.

---

## Datos mínimos

```text
CommandId

AssemblyId

OrganizationId

ActorId

ExpectedVersion

CancellationReason

Timestamp

CorrelationId

CausationId
```

`CancellationReason` debe modelarse como concepto de dominio
cuando sea obligatorio por las reglas vigentes.

---

## Estados origen permitidos

```text
Draft

Scheduled

Convoked
```

---

## Estado destino

```text
Cancelled
```

---

## Estados no permitidos

```text
InProgress

Completed

Cancelled

Archived
```

La versión 1.0 no utiliza Cancelled para representar una
interrupción posterior al inicio.

---

## Precondiciones

* Assembly existe;
* estado actual permite cancelación;
* CancellationReason es válido cuando sea obligatorio;
* la reunión todavía no ha sido completada;
* la reunión no está Archived;
* Actor posee permiso;
* ExpectedVersion coincide.

---

## Comportamiento esperado

```text
assembly.cancel(...)
```

La operación debe:

* preservar el historial previo;
* establecer CancelledAt;
* cambiar Status a Cancelled;
* actualizar UpdatedAt;
* incrementar Version.

---

## Evento esperado

```text
AssemblyCancelled
```

---

# Preservación Histórica durante CancelAssembly

La cancelación nunca debe eliminar hechos previamente ocurridos.

Si una Assembly estaba Scheduled se preservan:

```text
ScheduledStartAt

ScheduledEndAt

TimeZone
```

Si estaba Convoked también debe preservarse:

```text
ConvokedAt

Convocation
```

El Domain Event:

```text
AssemblyCancelled
```

agrega un hecho.

No elimina hechos anteriores.

---

# ArchiveAssembly

## Objetivo

Retirar una Assembly del ciclo operativo manteniendo su identidad,
historial y trazabilidad.

---

## Datos mínimos

```text
CommandId

AssemblyId

OrganizationId

ActorId

ExpectedVersion

Timestamp

CorrelationId

CausationId
```

Puede incluir:

```text
ArchiveReason
```

cuando las reglas del dominio lo requieran.

---

## Estados origen permitidos

```text
Completed

Cancelled
```

---

## Estado destino

```text
Archived
```

---

## Estados no permitidos

```text
Draft

Scheduled

Convoked

InProgress

Archived
```

---

## Precondiciones

* Assembly existe;
* estado actual es Completed o Cancelled;
* información histórica requerida es válida;
* condiciones de archivado se encuentran satisfechas;
* Actor posee permiso;
* ExpectedVersion coincide.

---

## Comportamiento esperado

```text
assembly.archive(...)
```

La operación debe:

* establecer ArchivedAt;
* cambiar Status a Archived;
* preservar información histórica;
* actualizar UpdatedAt;
* incrementar Version.

---

## Evento esperado

```text
AssemblyArchived
```

---

# Commands no Permitidos sobre Archived

Cuando:

```text
AssemblyStatus = Archived
```

deben rechazarse todos los Commands de modificación ordinaria.

Incluyendo:

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

Archived constituye un estado terminal.

---

# Commands no Permitidos sobre Completed

Una Assembly Completed no puede modificarse mediante Commands
operativos ordinarios.

Debe rechazarse:

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

ChangeAssemblyModality
```

La operación ordinaria permitida sobre su Lifecycle es:

```text
ArchiveAssembly
```

Las correcciones documentales posteriores pertenecen a los
Aggregates y procesos correspondientes, no implican reabrir
Assembly.

---

# Commands no Permitidos sobre Cancelled

Una Assembly Cancelled no puede volver al flujo operativo normal.

Deben rechazarse:

```text
ScheduleAssembly

RescheduleAssembly

ConvokeAssembly

StartAssembly

CompleteAssembly
```

El flujo permitido es:

```text
Cancelled
    │
    ▼
ArchiveAssembly
    │
    ▼
Archived
```

---

# Commands y State Machine

Los Commands que modifican el Lifecycle deben respetar
estrictamente:

```text
DOMAIN-006B-State-Machine.md
```

Relación principal:

| Command            | Estado origen | Estado destino |
| ------------------ | ------------- | -------------- |
| CreateAssembly     | No existe     | Draft          |
| ScheduleAssembly   | Draft         | Scheduled      |
| RescheduleAssembly | Scheduled     | Scheduled      |
| RescheduleAssembly | Convoked      | Convoked       |
| ConvokeAssembly    | Scheduled     | Convoked       |
| StartAssembly      | Convoked      | InProgress     |
| CompleteAssembly   | InProgress    | Completed      |
| CancelAssembly     | Draft         | Cancelled      |
| CancelAssembly     | Scheduled     | Cancelled      |
| CancelAssembly     | Convoked      | Cancelled      |
| ArchiveAssembly    | Completed     | Archived       |
| ArchiveAssembly    | Cancelled     | Archived       |

Ningún Command puede utilizarse para evadir una transición
obligatoria.

---

# Commands sin Cambio de Estado

Algunos Commands modifican el Aggregate manteniendo
AssemblyStatus.

Ejemplos:

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

Aunque Status permanezca igual, una modificación válida:

* cambia el estado interno del Aggregate;
* incrementa Version;
* actualiza UpdatedAt;
* puede generar un Domain Event.

---

# No-Op Commands

Un Command cuyo Payload no representa un cambio real puede ser
rechazado.

Ejemplo:

```text
CurrentName = "Asamblea General"

RenameAssembly(
    AssemblyName = "Asamblea General"
)
```

La política oficial puede considerar esta operación:

```text
NoChange
```

y evitar:

* incremento innecesario de Version;
* Domain Events sin cambio semántico;
* auditoría artificial.

La regla concreta debe mantenerse consistente en todos los
Commands equivalentes.

---

# Rechazo de Commands

Assembly debe rechazar un Command cuando ocurra cualquiera de las
siguientes situaciones:

* AssemblyId no existe;
* OrganizationId no corresponde al Aggregate;
* CommandId es inválido;
* ActorId es inválido;
* el Actor no posee permisos;
* ExpectedVersion no coincide;
* estado actual no permite la operación;
* transición no está autorizada por la State Machine;
* faltan datos obligatorios;
* los datos son inválidos;
* una precondición no se cumple;
* una invariante sería violada;
* la operación intenta modificar identidad;
* la operación intenta modificar otro Aggregate;
* la Assembly está Archived;
* el Command pretende reescribir hechos históricos.

---

# Efectos del Rechazo

Cuando un Command es rechazado:

* no se modifica Assembly;
* AssemblyStatus permanece igual;
* Version permanece igual;
* UpdatedAt no cambia debido al Command rechazado;
* no se crean cambios parciales;
* no se publica el Domain Event de éxito;
* no se modifica otro Aggregate;
* no se ejecutan efectos de integración como consecuencia de un
  hecho inexistente.

---

# Error de Estado

Debe rechazarse un Command cuando el estado origen no corresponde.

Ejemplo:

```text
AssemblyStatus = Draft

StartAssembly
```

Resultado:

```text
Rejected
```

porque:

```text
Draft → InProgress
```

no es una transición permitida.

---

# Error de Invariante

Ejemplo:

```text
ScheduleAssembly

ScheduledStartAt = 2026-08-20T20:00

ScheduledEndAt = 2026-08-20T18:00
```

Debe rechazarse porque:

```text
ScheduledEndAt <= ScheduledStartAt
```

viola la consistencia temporal.

No se publica:

```text
AssemblyScheduled
```

---

# Error de Concurrencia

Ejemplo:

```text
PersistedVersion = 12

ExpectedVersion = 11
```

El Command debe rechazarse antes de persistir una nueva versión.

La operación debe ejecutarse nuevamente únicamente después de
recuperar el estado vigente y reevaluar la intención.

---

# Commands e Invariantes

Un Command nunca puede establecer excepciones implícitas a las
invariantes.

Aunque el Command sea estructuralmente válido:

```text
StartAssembly
```

debe rechazarse si:

```text
ExecutionConditionsSatisfied = false
```

cuando dichas condiciones son obligatorias.

La definición formal se encuentra en:

```text
DOMAIN-006E-Invariants.md
```

---

# Commands y Permissions

La autorización se evalúa antes de ejecutar comportamiento
protegido.

Ejemplos conceptuales:

```text
CreateAssembly
    └── Assembly.Create

ScheduleAssembly
    └── Assembly.Schedule

ConvokeAssembly
    └── Assembly.Convoke

StartAssembly
    └── Assembly.Start

CompleteAssembly
    └── Assembly.Complete

CancelAssembly
    └── Assembly.Cancel

ArchiveAssembly
    └── Assembly.Archive
```

Los permisos completos se desarrollan en:

```text
DOMAIN-006F-Permissions.md
```

Poseer un permiso no garantiza que el Command sea válido.

---

# Separación entre Autorización y Dominio

Debe cumplirse:

```text
Authorization
        ≠
Domain Validity
```

Ejemplo:

un Actor puede poseer:

```text
Assembly.Start
```

pero si:

```text
AssemblyStatus = Scheduled
```

`StartAssembly` debe rechazarse.

La autorización responde:

```text
¿Puede este Actor solicitar esta operación?
```

El Aggregate responde:

```text
¿Puede esta operación ocurrir en el estado actual?
```

---

# Commands y Repository

Los Commands no conocen el Repository.

No deben contener lógica como:

```text
database.save(...)

repository.update_status(...)

sql.execute(...)
```

El flujo corresponde a:

```text
Application Service
       │
       ├── load Aggregate
       ▼
     Assembly
       │
       ├── execute behavior
       ▼
Application Service
       │
       └── save Aggregate
```

---

# Commands y Consistency Boundary

Cada Command modifica exclusivamente:

```text
Assembly
```

dentro de su límite de consistencia.

Un Command de Assembly nunca modifica transaccionalmente:

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

La definición formal se desarrolla en:

```text
DOMAIN-006J-Consistency-Boundary.md
```

---

# Commands y Otros Aggregates

Un Command puede necesitar validaciones previas relacionadas con
otros Aggregates.

Ejemplo:

```text
CreateAssembly
```

puede requerir verificar que:

```text
OrganizationId
```

corresponda a una Organization válida.

Esta comprobación no convierte Organization en parte de
Assembly.

La Application Layer o una Domain Policy apropiada resuelve la
coordinación.

---

# Commands y Domain Events

Cuando un Command es aceptado puede producir uno o más Domain
Events.

Relación conceptual:

```text
CreateAssembly
    ↓
AssemblyCreated

ScheduleAssembly
    ↓
AssemblyScheduled

RescheduleAssembly
    ↓
AssemblyRescheduled

ConvokeAssembly
    ↓
AssemblyConvoked

StartAssembly
    ↓
AssemblyStarted

CompleteAssembly
    ↓
AssemblyCompleted

CancelAssembly
    ↓
AssemblyCancelled

ArchiveAssembly
    ↓
AssemblyArchived
```

Los eventos completos se desarrollan en:

```text
DOMAIN-006D-Domain-Events.md
```

---

# Un Command puede producir múltiples Events

Una operación puede producir más de un hecho cuando el dominio lo
requiera.

Ejemplo conceptual:

una reprogramación de una Assembly ya convocada podría producir:

```text
AssemblyRescheduled

AssemblyConvocationUpdated
```

si ambos hechos ocurrieron realmente.

No debe producirse un evento adicional únicamente por
conveniencia técnica.

---

# Domain Event después de una Operación Válida

El Domain Event debe registrarse únicamente después de que:

* Guards fueron satisfechos;
* invariantes fueron validadas;
* comportamiento fue ejecutado;
* estado interno quedó consistente.

No debe existir:

```text
publish event
    ↓
attempt state change
    ↓
validation failure
```

como comportamiento de dominio.

---

# Commands y Audit

Todo Command debe ser trazable.

Conceptualmente puede registrarse:

```text
CommandId

AssemblyId

OrganizationId

ActorId

ExpectedVersion

Timestamp

CorrelationId

CausationId

CommandType
```

Cuando el Command es aceptado, la trazabilidad puede relacionarlo
con:

```text
DomainEventId

NewVersion
```

Audit mantiene su propio Aggregate y límite de consistencia.

---

# Command Rechazado y Auditoría

Un Command rechazado no genera un Domain Event de éxito.

Sin embargo, un intento rechazado puede ser registrado por
mecanismos de:

* seguridad;
* observabilidad;
* auditoría técnica;
* auditoría de aplicación;

cuando la política lo requiera.

Ese registro no debe representarse falsamente como un Domain
Event de Assembly.

---

# Idempotencia

Los Commands poseen:

```text
CommandId
```

para permitir estrategias de idempotencia en la frontera de
aplicación.

La idempotencia de transporte evita procesar accidentalmente dos
veces la misma intención.

No altera las reglas del Aggregate.

Por ejemplo:

```text
StartAssembly
```

aceptado una vez cambia:

```text
Convoked → InProgress
```

Una segunda intención distinta de StartAssembly debe rechazarse
por estado.

Una retransmisión del mismo CommandId puede ser detectada antes de
volver a ejecutar el Aggregate.

---

# Duplicación de Commands

Debe distinguirse:

```text
same CommandId
```

de:

```text
same CommandType
```

Dos Commands:

```text
RenameAssembly
```

pueden ser legítimamente diferentes si poseen CommandId y Payload
diferentes.

Una retransmisión con el mismo CommandId representa la misma
intención lógica.

---

# Orden de Commands

Assembly no debe asumir que Commands distribuidos llegarán en el
orden esperado.

Ejemplo:

```text
ConvokeAssembly
```

puede llegar antes de que:

```text
ScheduleAssembly
```

haya sido procesado.

La State Machine debe rechazar la operación si el estado vigente
no permite ejecutarla.

El sistema no altera el estado para acomodar Commands fuera de
orden.

---

# Commands y Versionado

ExpectedVersion protege la intención contra una representación
obsoleta del Aggregate.

Ejemplo:

```text
Assembly
Status = Scheduled
Version = 5
```

Actor A:

```text
ConvokeAssembly
ExpectedVersion = 5
```

Actor B:

```text
CancelAssembly
ExpectedVersion = 5
```

Si A persiste primero:

```text
Status = Convoked
Version = 6
```

el Command de B con:

```text
ExpectedVersion = 5
```

debe ser rechazado.

---

# Reintento de Command

Después de un conflicto de concurrencia no debe repetirse
ciegamente la misma modificación.

Debe:

1. recuperarse la nueva versión;
2. reevaluarse el estado;
3. reevaluarse la intención;
4. volver a validar permisos;
5. volver a validar invariantes;
6. decidir si la intención continúa siendo válida.

Un retry técnico no puede saltarse el dominio.

---

# Commands y Timestamps

Los timestamps del Command y del Aggregate poseen significados
diferentes.

Ejemplo:

```text
Command.Timestamp
```

representa el momento asociado a la intención.

```text
Assembly.StartedAt
```

representa el momento aceptado como hecho de inicio.

Pueden coincidir, pero no son conceptualmente el mismo dato.

El Aggregate determina qué timestamp utiliza para representar el
hecho de dominio según el contrato establecido.

---

# Commands y TimeZone

Los Commands relacionados con programación deben expresar tiempos
de manera inequívoca.

Ejemplos:

```text
ScheduleAssembly

RescheduleAssembly
```

deben proporcionar:

```text
ScheduledStartAt

ScheduledEndAt

TimeZone
```

conforme a las reglas temporales oficiales.

No se permiten fechas ambiguas.

---

# Commands de Consulta

No existen Commands para operaciones que no modifican estado.

Por ejemplo:

```text
GetAssembly

ListAssemblies

SearchAssemblies
```

no son Commands del Aggregate.

Corresponden a:

```text
Queries
```

dentro del modelo de lectura.

CQRS mantiene separación entre:

```text
Commands
```

y:

```text
Queries
```

---

# Commands y CQRS

En un modelo CQRS:

```text
Command
    │
    ▼
Write Model
    │
    ▼
Assembly
```

Mientras:

```text
Query
    │
    ▼
Read Model
```

Un Command nunca debe utilizar un Read Model como fuente
autoritativa para modificar estado.

El Aggregate es la autoridad transaccional.

---

# Commands y Event Sourcing

En una implementación basada en Event Sourcing:

```text
Command
    │
    ▼
Rehydrated Assembly
    │
    ▼
Domain Behavior
    │
    ▼
New Domain Events
```

Los Commands no forman parte necesariamente del Event Stream de
dominio.

Los hechos consumados son los Domain Events.

La estrategia concreta de almacenamiento permanece fuera del
Aggregate.

---

# Commands e Integration Events

Un Command no debe publicar directamente Integration Events.

El flujo conceptual correcto es:

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
Application / Integration Layer
    │
    ▼
Integration Event
```

La definición formal se desarrolla en:

```text
DOMAIN-006K-Integration-Events.md
```

---

# Commands y Notification

Commands como:

```text
ConvokeAssembly

RescheduleAssembly

CancelAssembly
```

pueden producir eventos que posteriormente originen
Notifications.

Ejemplo:

```text
ConvokeAssembly
        │
        ▼
AssemblyConvoked
        │
        ▼
Notification Handler
        │
        ▼
Notification
```

`ConvokeAssembly` no envía directamente:

* correos;
* SMS;
* WhatsApp;
* push notifications.

---

# Commands y FIWARE

Un sistema externo o FIWARE puede originar una intención que
termine convertida en un Command válido de AURA.

Sin embargo, no debe modificar directamente Assembly.

Flujo:

```text
External System
      │
      ▼
Anti-Corruption Layer
      │
      ▼
Application Layer
      │
      ▼
Assembly Command
      │
      ▼
Assembly
```

Los Commands continúan utilizando el lenguaje ubicuo de AURA.

---

# Anti-Corruption Layer

Si un sistema externo utiliza operaciones como:

```text
OPEN_MEETING

CLOSE_MEETING
```

estas no deben introducirse automáticamente como Commands del
dominio.

La Anti-Corruption Layer debe traducir el significado externo a
Commands oficiales cuando exista correspondencia real.

Por ejemplo:

```text
OPEN_MEETING
```

podría traducirse a:

```text
StartAssembly
```

únicamente si las semánticas son equivalentes.

---

# Commands e Infraestructura

Ningún Command depende de:

```text
HTTP

REST

GraphQL

FastAPI

Django

React

Next.js

MongoDB

PostgreSQL

Redis

OAuth

JWT

FIWARE

NGSI-LD
```

Un endpoint como:

```text
POST /assemblies/{assembly_id}/start
```

es únicamente una representación de transporte.

La intención de dominio continúa siendo:

```text
StartAssembly
```

---

# Commands y Application Layer

La Application Layer es responsable de coordinar la ejecución.

Conceptualmente:

```text
handle(StartAssembly)
```

puede:

1. validar contexto básico;
2. autorizar Actor;
3. cargar Assembly;
4. validar ExpectedVersion;
5. invocar `assembly.start()`;
6. persistir Assembly;
7. publicar eventos después de la persistencia conforme a la
   estrategia arquitectónica.

La Application Layer no debe duplicar las invariantes internas
del Aggregate como sustituto de Assembly.

---

# Commands y Aggregate Root

Cada Command debe terminar ejecutando comportamiento explícito de:

```text
Assembly
```

Ejemplos:

```text
ScheduleAssembly
    ↓
assembly.schedule()

ConvokeAssembly
    ↓
assembly.convoke()

StartAssembly
    ↓
assembly.start()

CompleteAssembly
    ↓
assembly.complete()
```

No debe existir:

```text
handler.status = "InProgress"
```

ni:

```text
repository.update_status(
    assembly_id,
    "InProgress"
)
```

como sustituto del comportamiento de dominio.

---

# Política de Setters

Los Commands no justifican setters públicos.

No deben existir operaciones como:

```text
setStatus()

setStartedAt()

setCompletedAt()

setOrganizationId()

setVersion()
```

para ejecutar Commands.

La modificación ocurre mediante comportamiento semántico.

---

# Atomicidad

Cada Command aceptado produce una modificación atómica dentro del
límite de consistencia de Assembly.

Por ejemplo:

```text
StartAssembly
```

debe producir coherentemente:

```text
Status = InProgress

StartedAt != null

Version = Version + 1

AssemblyStarted registrado
```

No debe persistirse una combinación parcial.

---

# Consistencia

Cada Command debe:

* modificar exclusivamente un Aggregate;
* ejecutarse dentro de una única transacción lógica de Assembly;
* preservar todas las invariantes;
* mantener coherencia temporal;
* mantener coherencia del Lifecycle;
* mantener Version consistente;
* producir únicamente Domain Events válidos.

---

# Tabla Resumen de Commands

| Command                           | Estado origen          | Estado destino | Evento principal                   |
| --------------------------------- | ---------------------- | -------------- | ---------------------------------- |
| CreateAssembly                    | No existe              | Draft          | AssemblyCreated                    |
| ScheduleAssembly                  | Draft                  | Scheduled      | AssemblyScheduled                  |
| RescheduleAssembly                | Scheduled              | Scheduled      | AssemblyRescheduled                |
| RescheduleAssembly                | Convoked               | Convoked       | AssemblyRescheduled                |
| ConvokeAssembly                   | Scheduled              | Convoked       | AssemblyConvoked                   |
| RenameAssembly                    | Permitido según estado | Sin cambio     | AssemblyRenamed                    |
| ChangeAssemblyType                | Permitido según estado | Sin cambio     | AssemblyTypeChanged                |
| ChangeAssemblyPurpose             | Permitido según estado | Sin cambio     | AssemblyPurposeChanged             |
| ChangeAssemblyDescription         | Permitido según estado | Sin cambio     | AssemblyDescriptionChanged         |
| ChangeAssemblyModality            | Permitido según estado | Sin cambio     | AssemblyModalityChanged            |
| ChangeAssemblyLocation            | Permitido según estado | Sin cambio     | AssemblyLocationChanged            |
| UpdateAssemblyConvocation         | Permitido según estado | Sin cambio     | AssemblyConvocationUpdated         |
| UpdateAssemblyRules               | Permitido según estado | Sin cambio     | AssemblyRulesUpdated               |
| UpdateAssemblyExecutionConditions | Permitido según estado | Sin cambio     | AssemblyExecutionConditionsUpdated |
| StartAssembly                     | Convoked               | InProgress     | AssemblyStarted                    |
| CompleteAssembly                  | InProgress             | Completed      | AssemblyCompleted                  |
| CancelAssembly                    | Draft                  | Cancelled      | AssemblyCancelled                  |
| CancelAssembly                    | Scheduled              | Cancelled      | AssemblyCancelled                  |
| CancelAssembly                    | Convoked               | Cancelled      | AssemblyCancelled                  |
| ArchiveAssembly                   | Completed              | Archived       | AssemblyArchived                   |
| ArchiveAssembly                   | Cancelled              | Archived       | AssemblyArchived                   |

---

# Matriz Conceptual por Estado

| Command                           | Draft |   Scheduled |    Convoked |  InProgress | Completed | Cancelled | Archived |
| --------------------------------- | ----: | ----------: | ----------: | ----------: | --------: | --------: | -------: |
| ScheduleAssembly                  |    Sí |          No |          No |          No |        No |        No |       No |
| RescheduleAssembly                |    No |          Sí | Condicional |          No |        No |        No |       No |
| ConvokeAssembly                   |    No |          Sí |          No |          No |        No |        No |       No |
| RenameAssembly                    |    Sí |          Sí | Condicional |          No |        No |        No |       No |
| ChangeAssemblyType                |    Sí | Condicional |          No |          No |        No |        No |       No |
| ChangeAssemblyPurpose             |    Sí |          Sí | Condicional |          No |        No |        No |       No |
| ChangeAssemblyDescription         |    Sí |          Sí |          Sí | Condicional |        No |        No |       No |
| ChangeAssemblyModality            |    Sí |          Sí | Condicional |          No |        No |        No |       No |
| ChangeAssemblyLocation            |    Sí |          Sí | Condicional | Condicional |        No |        No |       No |
| UpdateAssemblyConvocation         |    Sí |          Sí |          Sí |          No |        No |        No |       No |
| UpdateAssemblyRules               |    Sí |          Sí | Condicional | Condicional |        No |        No |       No |
| UpdateAssemblyExecutionConditions |    Sí |          Sí | Condicional |          No |        No |        No |       No |
| StartAssembly                     |    No |          No |          Sí |          No |        No |        No |       No |
| CompleteAssembly                  |    No |          No |          No |          Sí |        No |        No |       No |
| CancelAssembly                    |    Sí |          Sí |          Sí |          No |        No |        No |       No |
| ArchiveAssembly                   |    No |          No |          No |          No |        Sí |        Sí |       No |

`Condicional` significa que deben cumplirse restricciones
adicionales definidas por las invariantes, permisos y reglas
específicas del Aggregate.

---

# Commands Futuros

La versión 1.0 no define Commands como:

```text
SuspendAssembly

ResumeAssembly

InterruptAssembly

AbortAssembly

ReopenAssembly

DeleteAssembly
```

Estos Commands no deben implementarse implícitamente.

Si aparecen necesidades reales del dominio deberán ser evaluados
mediante evolución formal de:

```text
DOMAIN-006-Aggregate.md

DOMAIN-006A-Lifecycle.md

DOMAIN-006B-State-Machine.md

DOMAIN-006C-Commands.md

DOMAIN-006D-Domain-Events.md

DOMAIN-006E-Invariants.md

DOMAIN-006F-Permissions.md
```

---

# Regla para Incorporar un Nuevo Command

Un nuevo Command debe incorporarse solamente cuando represente
una intención real del negocio.

Debe definir como mínimo:

```text
CommandName

Objective

Payload

AllowedSourceStates

Preconditions

RequiredPermission

ExpectedBehavior

ExpectedDomainEvents
```

Además debe analizarse su impacto sobre:

* State Machine;
* Lifecycle;
* Invariants;
* Permissions;
* Versioning;
* Audit;
* Integration Events;
* Read Models;
* Test Scenarios;
* Security Model.

---

# Commands Técnicos Prohibidos

No deben existir Commands de dominio como:

```text
SaveAssembly

PersistAssembly

UpdateDatabase

SyncAssembly

PublishToKafka

SendAssemblyEmail

RefreshCache

CallFIWARE

RetryHTTP
```

Estas son acciones técnicas.

No representan intenciones propias del dominio Assembly.

---

# Naming

Los Commands deben utilizar:

```text
Verb + Aggregate/Concept
```

Ejemplos válidos:

```text
CreateAssembly

ScheduleAssembly

ConvokeAssembly

StartAssembly

CompleteAssembly

CancelAssembly
```

El nombre debe expresar intención inequívoca.

---

# Tiempo Verbal

Los Commands utilizan forma imperativa conceptual:

```text
StartAssembly
```

Los Domain Events utilizan pasado:

```text
AssemblyStarted
```

Esta diferencia forma parte del lenguaje ubicuo.

---

# Inmutabilidad de Commands

Una vez creado un Command no puede modificarse.

Ejemplo conceptual:

```text
ScheduleAssembly
```

con:

```text
ScheduledStartAt = T1
```

no debe cambiar posteriormente a:

```text
ScheduledStartAt = T2
```

dentro de la misma instancia de Command.

Si la intención cambia debe emitirse otro Command.

---

# Auditoría

Todo Command registra conceptualmente:

```text
CommandId

AssemblyId

OrganizationId

ActorId

ExpectedVersion

Timestamp

CorrelationId

CausationId

CommandType
```

Los datos específicos del Payload también pueden formar parte de
la trazabilidad según las políticas de privacidad, seguridad y
auditoría.

Estos registros permiten reconstruir:

```text
quién solicitó qué,
sobre cuál Assembly,
en qué contexto,
sobre qué versión,
y dentro de qué flujo causal.
```

---

# Privacidad

Los Commands deben contener exclusivamente la información
necesaria para ejecutar la intención.

No deben transportar datos personales o sensibles que no sean
requeridos por la operación.

Cuando se utilice ActorId, este debe funcionar como referencia de
identidad.

El Command no debe incorporar arbitrariamente perfiles completos
de Citizen o Membership.

---

# Seguridad

Los Commands no deben transportar:

* contraseñas;
* tokens OAuth;
* JWT de sesión como información de dominio;
* claves privadas;
* secretos criptográficos;
* credenciales de proveedores;
* certificados privados.

La autenticación técnica pertenece a capas externas.

Los aspectos formales se desarrollan en:

```text
DOMAIN-006O-Security-Model.md
```

---

# Compatibilidad

El modelo de Commands es compatible con:

* Domain-Driven Design;
* Tactical DDD;
* CQRS;
* Clean Architecture;
* Hexagonal Architecture;
* Event-Driven Architecture;
* Event Sourcing;
* Optimistic Concurrency;
* arquitectura distribuida.

---

# Dependencias

Los Commands pertenecen al modelo de escritura del dominio y
pueden utilizar conceptos definidos por:

* Shared Kernel;
* Value Objects;
* Aggregate Identifiers;
* Version;
* reglas de dominio.

No dependen directamente de:

```text
HTTP

REST

GraphQL

FastAPI

Django

React

Next.js

MongoDB

PostgreSQL

Redis

OAuth

JWT

FIWARE

NGSI-LD
```

---

# Reglas de Diseño

El modelo de Commands debe garantizar:

* intención explícita;
* nombres semánticos;
* Commands inmutables;
* CommandId único;
* trazabilidad;
* Actor explícito;
* contexto organizacional explícito;
* ExpectedVersion para concurrencia;
* una única Aggregate Root modificada;
* State Machine respetada;
* invariantes protegidas;
* separación entre autorización y dominio;
* separación entre Commands y Domain Events;
* separación entre Commands y Queries;
* separación entre dominio e infraestructura;
* ausencia de setters públicos;
* rechazo atómico;
* Domain Events únicamente después de operaciones válidas.

---

# Relación con Test Scenarios

Cada Command debe poseer escenarios de prueba que cubran, como
mínimo:

```text
successful command

invalid source state

invalid payload

missing precondition

permission denied

invariant violation

concurrency conflict

archived aggregate

no-op operation

event generation

version increment
```

Los escenarios formales se desarrollan en:

```text
DOMAIN-006M-Test-Scenarios.md
```

---

# Definición de Éxito

Los Commands del Aggregate **Assembly** constituyen el mecanismo
oficial para expresar intenciones de modificación sobre una
reunión dentro del ecosistema AURA.

Cada Command representa una intención explícita, inmutable,
trazable y contextualizada, identifica la Assembly y la
Organization correspondientes, mantiene información de Actor,
correlación, causalidad y versión esperada, y solo puede ejecutarse
cuando el estado actual, los permisos, los Guards y las
invariantes permiten la operación.

Los Commands nunca modifican directamente otros Aggregates,
nunca sustituyen comportamiento de dominio por setters y nunca
incorporan responsabilidades de infraestructura.

Cuando una intención es válida, la Aggregate Root ejecuta el
comportamiento correspondiente, preserva la consistencia,
incrementa Version y registra uno o más Domain Events que
representan los hechos realmente ocurridos.

Cuando una intención es inválida, el Command se rechaza de manera
atómica: no se modifica el Aggregate, no se incrementa Version y
no se publica ningún Domain Event de éxito.

De esta forma, el modelo de Commands de Assembly proporciona una
frontera de escritura explícita, consistente, auditable,
desacoplada y compatible con Domain-Driven Design, CQRS,
Optimistic Concurrency y Event-Driven Architecture.