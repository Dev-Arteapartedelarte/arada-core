# DOMAIN-006K — Assembly Integration Events

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
* DOMAIN-006I-Versioning.md
* DOMAIN-006J-Consistency-Boundary.md
* DOMAIN-006L-Read-Model.md
* DOMAIN-006M-Test-Scenarios.md
* DOMAIN-006N-Performance-Rules.md
* DOMAIN-006O-Security-Model.md
* DOMAIN-006P-Extension-Points.md
* DOMAIN-001-Aggregate.md
* DOMAIN-002-Aggregate.md
* DOMAIN-003-Aggregate.md
* DOMAIN-004-Aggregate.md
* DOMAIN-005-Aggregate.md
* CORE-002-Bounded-Context-Map.md
* CORE-003-Shared-Kernel.md
* CORE-004-Ubiquitous-Language.md
* CORE-006-Domain-Invariants.md
* CORE-007-Strategic-Design.md
* CORE-008-Aggregate-Design-Rules.md
* CORE-011-Repository-Contracts.md

---

# Objetivo

Definir el modelo conceptual y normativo de los
**Integration Events** asociados al Aggregate **Assembly**.

Los Integration Events permiten comunicar hechos relevantes
ocurridos dentro del Bounded Context **Assembly Management** hacia
otros Bounded Contexts, procesos de aplicación o sistemas externos
sin exponer directamente el estado interno del Aggregate.

Un Integration Event representa un hecho que ya ocurrió.

No representa una intención.

No representa un Command.

No modifica directamente Assembly.

No sustituye los Domain Events.

No forma parte del estado interno del Aggregate.

Su función es permitir interoperabilidad manteniendo desacoplado el
modelo de dominio de sus consumidores.

---

# Propósito

Assembly debe poder participar en procesos distribuidos sin conocer
las implementaciones, tecnologías o modelos internos de los
sistemas que consumen información sobre una Asamblea.

Los Integration Events permiten expresar esta comunicación
mediante contratos explícitos.

Conceptualmente:

```text
Assembly
    │
    ▼
Domain Event
    │
    ▼
Integration Boundary
    │
    ▼
Integration Event
    │
    ├────────► otros Bounded Contexts
    ├────────► sistemas municipales
    ├────────► plataformas ciudadanas
    ├────────► sistemas Smart City
    └────────► integraciones externas
```

Assembly conserva su autonomía.

Los consumidores conservan la suya.

---

# Principio Fundamental

Debe mantenerse:

```text
Domain Event
    ≠
Integration Event
```

Un **Domain Event** representa un hecho interno del modelo de
dominio.

Un **Integration Event** representa un contrato utilizado para
comunicar un hecho fuera del límite donde se originó.

Ejemplo conceptual:

```text
AssemblyCompleted
```

es un Domain Event del Aggregate.

Un contrato externo derivado puede expresarse mediante:

```text
AssemblyCompletedForIntegration
```

Ambos conceptos pueden estar relacionados.

No son el mismo artefacto arquitectónico.

---

# Fuente del Hecho

Todo Integration Event de Assembly debe originarse en un hecho
válidamente confirmado dentro del dominio.

Debe mantenerse:

```text
Valid Domain Change
        │
        ▼
Domain Event
        │
        ▼
Integration Event
```

No:

```text
Command
    │
    ▼
Integration Event
    │
    ▼
Attempt Domain Change
```

La comunicación externa ocurre después de que el dominio haya
determinado que el hecho ocurrió.

---

# Relación con Commands

Los Commands definidos en:

```text
DOMAIN-006C-Commands.md
```

representan intención.

Ejemplos:

```text
CreateAssembly

ScheduleAssembly

ConvokeAssembly

StartAssembly

CompleteAssembly

CancelAssembly

ArchiveAssembly
```

Los Integration Events representan hechos.

Por lo tanto:

```text
ConvokeAssembly
    ≠
AssemblyConvocationPublished
```

```text
StartAssembly
    ≠
AssemblyStartedForIntegration
```

```text
CompleteAssembly
    ≠
AssemblyCompletedForIntegration
```

```text
CancelAssembly
    ≠
AssemblyCancelledForIntegration
```

---

# Relación con Domain Events

Los Domain Events definidos en:

```text
DOMAIN-006D-Domain-Events.md
```

representan hechos ocurridos dentro de Assembly.

Ejemplos:

```text
AssemblyCreated

AssemblyScheduled

AssemblyRescheduled

AssemblyConvoked

AssemblyStarted

AssemblyCompleted

AssemblyCancelled

AssemblyArchived

AssemblyRenamed

AssemblyPurposeChanged

AssemblyDescriptionChanged

AssemblyTypeChanged

AssemblyModeChanged

AssemblyLocationChanged

AssemblyConvocationUpdated
```

Cuando uno de estos hechos deba comunicarse fuera del límite
interno correspondiente, puede originar un Integration Event.

No todos los Domain Events están obligados a producir siempre un
Integration Event.

La necesidad de publicación depende del contrato de
interoperabilidad correspondiente.

---

# Separación entre Modelo Interno y Contrato Externo

El modelo de Assembly no debe deformarse para satisfacer la
estructura requerida por sistemas externos.

Debe mantenerse:

```text
Assembly Domain Model
    ≠
External Integration Model
```

El modelo interno expresa el lenguaje y reglas de AURA.

El Integration Event expresa la información necesaria para
interoperabilidad.

---

# Responsabilidad

El modelo de Integration Events es responsable de:

* comunicar hechos confirmados de Assembly;
* desacoplar el Aggregate de los consumidores externos;
* proporcionar contratos explícitos;
* mantener identidad del evento;
* mantener identidad de Assembly;
* mantener contexto organizacional cuando corresponda;
* mantener contexto territorial cuando corresponda;
* mantener información temporal del hecho;
* permitir trazabilidad;
* permitir correlación;
* permitir causalidad;
* mantener una versión contractual;
* permitir evolución controlada;
* transportar únicamente información necesaria;
* preservar independencia tecnológica;
* permitir consistencia eventual entre límites.

---

# Responsabilidades Fuera del Modelo

No corresponde a los Integration Events:

* ejecutar Commands;
* modificar Assembly;
* validar State Machine;
* validar Guards;
* validar invariantes;
* autorizar Actors;
* autenticar usuarios;
* asignar Roles;
* conceder Permissions;
* modificar otros Aggregates;
* implementar Repository;
* ejecutar persistencia;
* definir transporte;
* seleccionar brokers;
* definir APIs;
* gestionar credenciales;
* administrar sistemas externos;
* sustituir Read Models;
* sustituir Audit.

---

# Límite Arquitectónico

Los Integration Events se encuentran fuera del Consistency
Boundary interno de Assembly.

Debe mantenerse:

```text
Assembly Consistency Boundary
        │
        ▼
Domain Event
        │
        ▼
Integration Boundary
        │
        ▼
Integration Event
```

El Integration Event no amplía el Aggregate.

---

# Consistencia

Dentro de Assembly se mantiene consistencia inmediata.

Entre Assembly y consumidores externos puede existir consistencia
eventual.

Conceptualmente:

```text
Strong Consistency
    inside Assembly
```

```text
Eventual Consistency
    outside Assembly
```

La comunicación externa no debe requerir que todos los sistemas
relacionados cambien dentro de la misma transacción de Assembly.

---

# Consistencia Eventual

Después de un cambio válido puede existir temporalmente una
diferencia entre:

```text
Assembly Write Model
```

y:

```text
External Projection
```

Ejemplo:

```text
AssemblyStatus:
Convoked
```

mientras un consumidor todavía conserva:

```text
AssemblyStatus:
Scheduled
```

hasta recibir y procesar el evento correspondiente.

Esta diferencia temporal no rompe la consistencia del Aggregate.

---

# Inmutabilidad

Todo Integration Event representa un hecho consumado.

Por lo tanto debe ser inmutable.

Después de publicado no deben cambiar:

```text
EventId

EventType

EventVersion

AssemblyId

OrganizationId

OccurredAt

CorrelationId

CausationId

Payload
```

cuando estos campos formen parte del contrato.

Una corrección posterior constituye otro hecho o una evolución
contractual.

---

# Identidad del Evento

Cada Integration Event posee:

```text
EventId
```

EventId identifica de forma única el evento.

Debe ser:

* único;
* inmutable;
* no reutilizable.

Debe mantenerse:

```text
EventId
    ≠
AssemblyId
```

AssemblyId identifica una Assembly.

EventId identifica un evento concreto.

---

# Identidad del Aggregate

Todo Integration Event relacionado directamente con Assembly debe
identificar el Aggregate mediante:

```text
AssemblyId
```

AssemblyId permite que los consumidores conozcan qué Assembly
originó el hecho.

El evento no contiene por ello la Aggregate Root completa.

---

# Contexto Organizacional

Los Integration Events de Assembly deben mantener:

```text
OrganizationId
```

cuando sea necesario para identificar el contexto organizacional
del hecho.

Cada Assembly pertenece a una única Organization.

El evento referencia Organization mediante identidad.

No transporta el Aggregate Organization.

---

# Contexto Territorial

Cuando el hecho requiera contexto territorial puede incluirse:

```text
TerritoryId
```

TerritoryId puede ser opcional cuando Assembly no posea contexto
territorial.

Debe mantenerse:

```text
TerritoryId
    ≠
Territory Aggregate
```

---

# Tipo de Evento

Todo contrato debe identificar claramente su semántica mediante:

```text
EventType
```

Ejemplos conceptuales:

```text
AssemblyPublished

AssemblyRescheduledForIntegration

AssemblyConvocationPublished

AssemblyStartedForIntegration

AssemblyCompletedForIntegration

AssemblyCancelledForIntegration

AssemblyArchivedForIntegration
```

EventType expresa el hecho comunicado.

---

# Version Contractual

Los Integration Events mantienen una versión contractual:

```text
EventVersion
```

EventVersion permite identificar la versión del contrato de
integración.

Debe mantenerse:

```text
EventVersion
    ≠
Assembly.Version
```

Assembly.Version representa la evolución del Aggregate.

EventVersion representa la evolución del contrato externo.

---

# AggregateVersion

Cuando el contrato requiera identificar la versión del Aggregate
que produjo el hecho, puede utilizarse:

```text
AggregateVersion
```

Debe mantenerse:

```text
AggregateVersion
    ≠
EventVersion
```

AggregateVersion pertenece a la evolución de Assembly.

EventVersion pertenece al contrato del Integration Event.

---

# OccurredAt

Todo Integration Event debe mantener el momento del hecho:

```text
OccurredAt
```

OccurredAt representa cuándo ocurrió el hecho del dominio.

No debe confundirse con el momento en que el evento fue
transportado o procesado.

Debe mantenerse:

```text
OccurredAt
    ≠
Processing Time
```

---

# CorrelationId

Los eventos pueden mantener:

```text
CorrelationId
```

para relacionar mensajes y operaciones pertenecientes a un mismo
flujo.

Ejemplo conceptual:

```text
CreateAssembly
        │
        ▼
AssemblyCreated
        │
        ▼
AssemblyPublished
```

puede mantener una misma correlación.

CorrelationId no reemplaza EventId.

---

# CausationId

Los eventos pueden mantener:

```text
CausationId
```

para expresar la relación causal inmediata.

Debe mantenerse:

```text
CorrelationId
    ≠
CausationId
```

CorrelationId agrupa un flujo.

CausationId identifica la causa inmediata.

---

# Estructura General

Todo Integration Event debe contener como mínimo los conceptos
necesarios para identificar:

```text
EventId

EventType

EventVersion

AssemblyId

OrganizationId

OccurredAt

CorrelationId

CausationId
```

Cuando corresponda también puede contener:

```text
AggregateVersion

TerritoryId
```

y los datos específicos del hecho.

---

# Payload

El Payload contiene únicamente la información necesaria para
representar el hecho comunicado.

Debe mantenerse:

```text
Integration Event
    ≠
Complete Aggregate Snapshot
```

El evento no debe convertirse en una copia completa de Assembly
por conveniencia.

---

# Principio de Información Mínima

Todo Integration Event debe transportar únicamente:

* identidad del evento;
* identidad de Assembly;
* contexto necesario;
* hecho comunicado;
* atributos necesarios para interpretar ese hecho;
* metadata contractual necesaria.

No debe transportar información interna que el consumidor no
necesita.

---

# No Exposición del Aggregate Completo

No está permitido utilizar como estrategia general:

```text
publish(assembly)
```

donde `assembly` representa toda la Aggregate Root.

Esto produciría acoplamiento directo entre consumidores y el
modelo interno.

Debe definirse un contrato explícito.

---

# Datos Internos

Los Integration Events no deben exponer automáticamente:

* entidades internas;
* estructuras de persistencia;
* objetos ORM;
* detalles del Repository;
* información privada de implementación;
* colecciones pertenecientes a otros Aggregates.

---

# Datos Personales

Los Integration Events de Assembly no deben utilizarse para
distribuir indiscriminadamente datos de Citizens.

No deben transportar automáticamente:

* FullName;
* Email;
* PhoneNumber;
* NationalIdentifier;
* ProfilePhoto;
* información personal de Membership.

La existencia de participantes en una Assembly no implica que sus
datos personales formen parte del contrato externo.

---

# CitizenId

CitizenId solo debe formar parte de un Integration Event cuando
exista una necesidad contractual explícita.

No debe incluirse por defecto en eventos generales del Lifecycle de
Assembly.

---

# MembershipId

MembershipId solo debe incorporarse cuando el contrato específico
lo requiera.

El Lifecycle general de Assembly no requiere transportar todas las
Memberships relacionadas.

---

# Seguridad

Los Integration Events nunca deben contener:

```text
Password

PasswordHash

AccessToken

RefreshToken

JWT

PrivateKey

OAuthSecret

APISecret

SessionToken
```

Los secretos técnicos pertenecen a Infrastructure.

---

# Autenticación

Integration Events no autentican consumidores.

La autenticación de productor y consumidor pertenece a los
mecanismos de seguridad de Infrastructure.

Assembly no conoce esos mecanismos.

---

# Autorización

Recibir un Integration Event no concede autorización sobre
Assembly.

Debe mantenerse:

```text
Receive Integration Event
    ≠
Permission to Modify Assembly
```

Toda modificación posterior de Assembly debe continuar utilizando:

* Commands;
* Permissions;
* State Machine;
* Guards;
* invariantes;
* Versioning.

---

# AssemblyPublished

## Objetivo

Comunicar la existencia de una Assembly cuando esta deba ser
expuesta hacia otros contextos o sistemas conforme al proceso
establecido.

## Hecho relacionado

Puede relacionarse conceptualmente con la disponibilidad de una
Assembly creada o programada para interoperabilidad.

## Datos conceptuales

```text
EventId

EventType

EventVersion

AssemblyId

OrganizationId

TerritoryId

AssemblyName

AssemblyType

AssemblyPurpose

ScheduledStart

ScheduledEnd

AssemblyMode

AssemblyStatus

AggregateVersion

OccurredAt

CorrelationId

CausationId
```

## Semántica

El evento comunica información básica suficiente para que un
consumidor pueda identificar y proyectar la Assembly.

No concede control sobre ella.

No representa una copia completa del Aggregate.

---

# AssemblyRescheduledForIntegration

## Objetivo

Comunicar un cambio válido en la programación de una Assembly.

## Domain Event relacionado

```text
AssemblyRescheduled
```

## Datos conceptuales

```text
EventId

EventType

EventVersion

AssemblyId

OrganizationId

PreviousScheduledStart

PreviousScheduledEnd

ScheduledStart

ScheduledEnd

AggregateVersion

OccurredAt

CorrelationId

CausationId
```

## Semántica

El evento comunica que la programación oficial cambió.

Permite que consumidores externos actualicen:

* calendarios;
* proyecciones;
* procesos de comunicación;
* sistemas relacionados.

No modifica directamente ninguno de ellos.

---

# AssemblyConvocationPublished

## Objetivo

Comunicar que una Assembly ha alcanzado formalmente la condición
de convocada.

## Domain Event relacionado

```text
AssemblyConvoked
```

## Datos conceptuales

```text
EventId

EventType

EventVersion

AssemblyId

OrganizationId

TerritoryId

AssemblyName

AssemblyType

ScheduledStart

ScheduledEnd

AssemblyMode

ConvokedAt

ConvocationDeadline

AggregateVersion

OccurredAt

CorrelationId

CausationId
```

## Estado relacionado

```text
Convoked
```

## Semántica

El evento representa la existencia formal de una convocatoria.

No significa:

```text
NotificationDelivered
```

Debe mantenerse:

```text
AssemblyConvocationPublished
    ≠
Notification Delivered
```

---

# AssemblyStartedForIntegration

## Objetivo

Comunicar que una Assembly comenzó formalmente.

## Domain Event relacionado

```text
AssemblyStarted
```

## Datos conceptuales

```text
EventId

EventType

EventVersion

AssemblyId

OrganizationId

TerritoryId

StartedAt

AssemblyStatus

AggregateVersion

OccurredAt

CorrelationId

CausationId
```

## Estado relacionado

```text
InProgress
```

## Semántica

El evento comunica que Assembly alcanzó válidamente:

```text
InProgress
```

No implica automáticamente:

* inicio de Voting;
* creación de Participation;
* apertura de Proposal;
* creación de Document;
* envío de Notification.

---

# AssemblyCompletedForIntegration

## Objetivo

Comunicar que una Assembly finalizó formalmente.

## Domain Event relacionado

```text
AssemblyCompleted
```

## Datos conceptuales

```text
EventId

EventType

EventVersion

AssemblyId

OrganizationId

TerritoryId

StartedAt

CompletedAt

AssemblyStatus

AggregateVersion

OccurredAt

CorrelationId

CausationId
```

## Estado relacionado

```text
Completed
```

## Semántica

El evento representa exclusivamente la finalización de Assembly.

Debe mantenerse:

```text
Assembly Completed
    ≠
All Related Processes Completed
```

Por lo tanto no significa automáticamente que:

* Proposal haya finalizado;
* Voting haya finalizado;
* Participation haya finalizado;
* Document haya sido generado;
* Notification haya sido enviada;
* Audit haya terminado de procesar el hecho.

---

# AssemblyCancelledForIntegration

## Objetivo

Comunicar que una Assembly fue cancelada válidamente.

## Domain Event relacionado

```text
AssemblyCancelled
```

## Datos conceptuales

```text
EventId

EventType

EventVersion

AssemblyId

OrganizationId

TerritoryId

CancelledAt

CancellationReason

AssemblyStatus

AggregateVersion

OccurredAt

CorrelationId

CausationId
```

## Estado relacionado

```text
Cancelled
```

## Semántica

El evento permite que otros contextos conozcan la cancelación y
apliquen sus propias reglas.

Assembly no determina directamente qué debe ocurrir en cada
consumidor.

---

# AssemblyArchivedForIntegration

## Objetivo

Comunicar que una Assembly alcanzó el estado Archived.

## Domain Event relacionado

```text
AssemblyArchived
```

## Datos conceptuales

```text
EventId

EventType

EventVersion

AssemblyId

OrganizationId

ArchivedAt

AssemblyStatus

AggregateVersion

OccurredAt

CorrelationId

CausationId
```

## Estado relacionado

```text
Archived
```

## Semántica

El evento comunica el archivado del Aggregate.

No implica:

* eliminación física;
* archivado de Proposal;
* archivado de Voting;
* archivado de Document;
* archivado de Notification;
* eliminación de Audit.

Cada Aggregate conserva su propia semántica.

---

# AssemblyDetailsChanged

## Objetivo

Comunicar cambios de información interoperable de Assembly cuando
exista un consumidor que necesite mantener dicha información
sincronizada.

## Domain Events relacionados

Puede derivarse de hechos como:

```text
AssemblyRenamed

AssemblyPurposeChanged

AssemblyDescriptionChanged

AssemblyTypeChanged

AssemblyModeChanged

AssemblyLocationChanged
```

## Semántica

El contrato debe comunicar exclusivamente la información que
efectivamente cambió y el contexto necesario para interpretarla.

No debe transformarse en un evento genérico que transporte todo el
Aggregate.

---

# AssemblyConvocationUpdatedForIntegration

## Objetivo

Comunicar que la información formal de convocatoria cambió después
de haber sido establecida.

## Domain Event relacionado

```text
AssemblyConvocationUpdated
```

## Datos conceptuales

```text
EventId

EventType

EventVersion

AssemblyId

OrganizationId

ConvocationStatus

ConvokedAt

ConvocationDeadline

AggregateVersion

OccurredAt

CorrelationId

CausationId
```

## Semántica

El evento permite sincronizar consumidores que dependan de la
información formal de convocatoria.

No representa el envío físico de comunicaciones.

---

# Eventos Específicos

Cuando un hecho posea significado propio debe preferirse un
contrato semánticamente explícito.

Ejemplo:

```text
AssemblyRescheduledForIntegration
```

expresa mejor la semántica que:

```text
AssemblyUpdated
```

si lo que realmente ocurrió fue una reprogramación.

Los Integration Events deben utilizar lenguaje de dominio
comprensible.

---

# Eventos Genéricos

Un evento genérico solo debe utilizarse cuando exista una semántica
contractual claramente definida.

No debe convertirse en un mecanismo para evitar diseñar eventos
específicos.

Debe evitarse que un consumidor tenga que comparar estados
completos para determinar qué ocurrió.

---

# Evento como Hecho Consumado

Los nombres deben representar hechos.

Ejemplos correctos:

```text
AssemblyStartedForIntegration

AssemblyCompletedForIntegration

AssemblyCancelledForIntegration
```

No:

```text
StartAssembly

CompleteAssembly

CancelAssembly
```

Los segundos representan Commands.

---

# Mapping desde Domain Events

La transformación desde Domain Event hacia Integration Event debe
ser explícita.

Ejemplo:

```text
AssemblyStarted
        │
        ▼
Integration Mapping
        │
        ▼
AssemblyStartedForIntegration
```

El Mapping puede:

* seleccionar campos;
* adaptar nombres;
* aplicar estructura contractual;
* agregar metadata de integración;
* eliminar información interna innecesaria.

No debe alterar el significado del hecho.

---

# Mapping no es Lógica del Aggregate

El Mapping no debe:

* decidir si la transición era válida;
* validar State Machine;
* cambiar AssemblyStatus;
* recalcular invariantes;
* modificar Assembly;
* ejecutar Commands.

Estas responsabilidades ya fueron resueltas antes dentro del
dominio.

---

# Publicación

La publicación ocurre fuera de la Aggregate Root.

Debe mantenerse:

```text
Assembly
    does not know
    transport
```

Assembly no conoce:

* broker;
* topic;
* queue;
* endpoint;
* webhook;
* protocolo;
* consumidor.

---

# Integridad del Hecho Publicado

Un Integration Event solo puede representar un estado o hecho que
realmente haya sido confirmado.

No debe publicarse:

```text
AssemblyCompletedForIntegration
```

si Assembly nunca alcanzó:

```text
Completed
```

---

# Command Rechazado

Si:

```text
CompleteAssembly
```

es rechazado, no existe:

```text
AssemblyCompleted
```

y tampoco debe existir:

```text
AssemblyCompletedForIntegration
```

como hecho válido.

---

# Invariante Violada

Si una operación viola una invariante:

```text
Aggregate State Unchanged
```

Por lo tanto:

```text
No Integration Event
```

correspondiente a la operación fallida.

---

# State Machine Rechazada

Una transición inválida no produce Integration Event de éxito.

Ejemplo:

```text
Draft
    ✕
    ▼
InProgress
```

no puede originar:

```text
AssemblyStartedForIntegration
```

---

# Permission Denied

Si un Actor carece del Permission requerido, la operación no
modifica Assembly.

Por lo tanto el hecho externo tampoco existe.

---

# Conflicto de Concurrencia

Si Repository rechaza una modificación porque:

```text
ExpectedVersion
    ≠
PersistedVersion
```

no existe un nuevo hecho confirmado.

El Integration Event correspondiente no debe publicarse.

---

# Version de Assembly

Cuando el contrato incluya:

```text
AggregateVersion
```

esta información representa la versión de Assembly asociada al
hecho.

Debe respetar:

```text
DOMAIN-006I-Versioning.md
```

---

# Version del Contrato

Debe mantenerse:

```text
AggregateVersion
    ≠
EventVersion
```

Cambiar EventVersion no modifica Assembly.

Cambiar Assembly.Version no obliga automáticamente a cambiar
EventVersion.

---

# Evolución del Contrato

Los Integration Events deben poder evolucionar sin obligar al
Aggregate a adoptar la misma estructura externa.

La evolución contractual debe preservar:

* identidad semántica;
* significado del evento;
* compatibilidad cuando corresponda;
* documentación explícita.

---

# Cambio Compatible

Una evolución del contrato puede ser compatible cuando mantiene la
semántica esperada por los consumidores actuales.

Los cambios compatibles no deben alterar el significado del hecho.

---

# Cambio Incompatible

Un cambio contractual que altere la interpretación del evento debe
tratarse como una evolución explícita del contrato.

No debe modificarse silenciosamente la semántica de un EventType ya
publicado.

---

# EventId y Reentrega

Los Integration Events pueden ser procesados más de una vez por
determinados mecanismos de transporte.

EventId permite distinguir:

```text
same logical event
```

de:

```text
different events
```

Una reentrega del mismo evento no significa que el hecho del
dominio ocurrió nuevamente.

---

# Duplicados

Debe mantenerse:

```text
Same EventId
    =
Same Integration Event
```

Un consumidor puede utilizar esta identidad para evitar aplicar dos
veces la misma reacción.

La estrategia técnica concreta pertenece al consumidor o a
Infrastructure.

---

# Dos Eventos Diferentes

Dos eventos del mismo tipo pueden existir si representan hechos
distintos.

Ejemplo:

```text
EventId:
EVT-001

EventType:
AssemblyDetailsChanged
```

y posteriormente:

```text
EventId:
EVT-002

EventType:
AssemblyDetailsChanged
```

representan dos hechos diferentes.

---

# Orden

Los Integration Events no deben depender conceptualmente de un
orden global entre todos los eventos de AURA.

Cada evento mantiene identidad y contexto suficiente para ser
interpretado.

Cuando corresponda puede utilizar:

```text
AssemblyId

AggregateVersion

OccurredAt

CorrelationId

CausationId
```

para preservar trazabilidad.

---

# Correlación de Flujo

Ejemplo:

```text
ConvokeAssembly
        │
        ▼
AssemblyConvoked
        │
        ▼
AssemblyConvocationPublished
        │
        ▼
Notification Process
```

puede compartir:

```text
CorrelationId
```

para identificar el flujo completo.

---

# Causalidad

El Integration Event puede mantener la referencia al hecho que lo
originó mediante:

```text
CausationId
```

Esta información permite reconstruir relaciones causales sin
acoplar los componentes.

---

# Notification

Notification permanece fuera del Aggregate.

Puede reaccionar a:

```text
AssemblyConvocationPublished
```

o:

```text
AssemblyCancelledForIntegration
```

según sus propias reglas.

Debe mantenerse:

```text
Assembly
    does not send Notification directly
```

---

# Document

Document permanece fuera del Aggregate.

Puede reaccionar a:

```text
AssemblyCompletedForIntegration
```

cuando exista un proceso documental asociado.

La creación del acta o de otros Documents no forma parte de la
transacción de Assembly.

---

# Audit

Audit permanece fuera del Aggregate.

Puede consumir hechos publicados para mantener trazabilidad.

Assembly no contiene registros de Audit como entidades internas.

---

# Proposal

Proposal puede relacionarse con Assembly mediante AssemblyId u
otros contratos definidos por su propio modelo.

Un Integration Event de Assembly no modifica Proposal
directamente.

---

# Participation

Participation puede reaccionar a hechos como:

```text
AssemblyStartedForIntegration
```

si sus propias reglas requieren conocer el inicio formal de una
reunión.

Participation conserva su propia identidad y consistencia.

---

# Voting

Voting puede utilizar hechos de Assembly como contexto.

Ejemplo conceptual:

```text
AssemblyStartedForIntegration
        │
        ▼
Voting Application Process
```

Esto no significa que toda Assembly deba iniciar automáticamente
una Voting.

---

# Organization

Organization mantiene su propio Aggregate.

Los Integration Events de Assembly pueden utilizar:

```text
OrganizationId
```

como contexto.

No modifican Organization directamente.

---

# Territory

Territory permanece fuera del Aggregate.

Los consumidores pueden utilizar:

```text
TerritoryId
```

para proyecciones territoriales.

El evento no contiene la estructura de Territory.

---

# Sistemas Municipales

Los Integration Events permiten comunicar hechos hacia plataformas
municipales sin introducirlas dentro de Assembly.

Conceptualmente:

```text
Assembly
    │
    ▼
Integration Event
    │
    ▼
Municipal Adapter
    │
    ▼
Municipal System
```

Assembly no conoce la API municipal.

---

# Sistemas Smart City

Los Integration Events pueden permitir que información relevante
de Assembly sea utilizada por ecosistemas Smart City.

La interoperabilidad se mantiene fuera del Aggregate.

---

# FIWARE

Assembly puede participar en integraciones FIWARE a través de la
capa correspondiente.

Conceptualmente:

```text
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
External Representation
```

Assembly no conoce:

* FIWARE;
* Context Broker;
* Orion-LD;
* NGSI-LD;
* endpoints;
* tokens;
* adaptadores.

---

# Representación Externa

Una representación externa de Assembly no constituye el Aggregate.

Debe mantenerse:

```text
Assembly Domain Model
    ≠
External Representation
```

El Adapter puede transformar el Integration Event al formato
requerido por el sistema externo.

---

# APIs

Los Integration Events no dependen de:

```text
REST

GraphQL

gRPC

Webhooks
```

Un mismo contrato conceptual puede ser transportado mediante
diferentes mecanismos.

---

# Mensajería

El modelo conceptual tampoco depende de:

```text
Kafka

RabbitMQ

NATS

MQTT
```

Estas tecnologías pertenecen a Infrastructure.

---

# Serialización

Integration Event no significa necesariamente:

```text
JSON
```

La serialización pertenece a Infrastructure.

Debe mantenerse:

```text
Event Semantics
    ≠
Serialization Format
```

---

# Producer

El productor del Integration Event se encuentra fuera de la
Aggregate Root.

Su responsabilidad es transformar un hecho confirmado del dominio
en un contrato externo.

No debe introducir nuevas reglas de Assembly.

---

# Consumer

El consumidor procesa el contrato externo.

No obtiene una referencia mutable al Aggregate.

No debe depender de:

* clases internas;
* entidades internas;
* Repository interno;
* ORM;
* estructuras privadas del dominio.

---

# Independencia de Consumidores

Assembly no conoce cuántos consumidores existen.

Debe ser posible:

```text
Integration Event
    ├────────► Consumer A
    ├────────► Consumer B
    ├────────► Consumer C
    └────────► Consumer N
```

sin modificar la Aggregate Root por cada nuevo consumidor.

---

# Fallo de Consumidor

Si un consumidor falla después de recibir:

```text
AssemblyCompletedForIntegration
```

Assembly continúa:

```text
Completed
```

cuando el cambio fue válidamente confirmado.

Debe mantenerse:

```text
Consumer Failure
    ≠
Aggregate Rollback
```

---

# Fallo de Integración

Un fallo de un sistema externo no redefine un hecho interno ya
consumado.

Ejemplo:

```text
AssemblyCompleted
```

continúa siendo verdadero aunque un consumidor externo no pueda
procesar inmediatamente el Integration Event.

---

# Reintentos de Publicación

Los reintentos técnicos de publicación no representan nuevos
cambios de Assembly.

No deben:

* incrementar Assembly.Version;
* ejecutar nuevamente el Command original;
* producir un nuevo hecho de dominio por cada intento.

---

# Reintentos de Consumo

Los consumidores pueden necesitar reprocesar un Integration Event.

El reprocesamiento tampoco representa por sí mismo una nueva
modificación de Assembly.

---

# Idempotencia

Los contratos deben permitir que los consumidores puedan
identificar el mismo evento mediante:

```text
EventId
```

La estrategia concreta de idempotencia pertenece al consumidor.

---

# Read Models Externos

Un Integration Event puede alimentar proyecciones externas.

Ejemplo:

```text
AssemblyPublished

AssemblyRescheduledForIntegration

AssemblyConvocationPublished

AssemblyStartedForIntegration

AssemblyCompletedForIntegration
```

pueden mantener una vista externa de una Assembly.

La vista no es fuente transaccional de verdad.

---

# Read Model Interno

El Read Model definido en:

```text
DOMAIN-006L-Read-Model.md
```

permanece conceptualmente separado de los Integration Events.

Ambos pueden consumir hechos.

No representan la misma responsabilidad.

---

# Replay

La eventual capacidad de reprocesar Integration Events no convierte
el Integration Event Stream en el modelo interno del Aggregate.

Debe mantenerse:

```text
Domain History
    ≠
Integration History
```

---

# Event Sourcing

La compatibilidad de Assembly con Event Sourcing no implica que los
Integration Events deban utilizarse para rehidratar el Aggregate.

Debe mantenerse:

```text
Domain Events
    ≠
Integration Events
```

también en escenarios Event Sourced.

---

# Audit y Trazabilidad

Los Integration Events deben permitir trazabilidad suficiente para
relacionar el hecho publicado con su contexto.

Conceptualmente pueden utilizar:

```text
EventId

AssemblyId

OrganizationId

AggregateVersion

OccurredAt

CorrelationId

CausationId

EventVersion
```

La auditoría completa pertenece al contexto Audit.

---

# Observabilidad

Los sistemas técnicos pueden registrar:

```text
PublishedAt

ProcessedAt

DeliveryAttempts

ConsumerId

TransportMetadata
```

cuando corresponda.

Estos conceptos pertenecen a Infrastructure u observabilidad.

No forman parte del Aggregate Assembly.

---

# OccurredAt versus PublishedAt

Debe mantenerse:

```text
OccurredAt
    ≠
PublishedAt
```

OccurredAt representa el momento del hecho.

PublishedAt, cuando exista técnicamente, representa el momento de
publicación.

---

# OccurredAt versus ProcessedAt

Debe mantenerse:

```text
OccurredAt
    ≠
ProcessedAt
```

ProcessedAt pertenece al consumidor.

No modifica la semántica temporal del hecho original.

---

# Seguridad del Payload

El Payload debe limitarse a información necesaria.

No debe exponer información que no tenga relación contractual con
el evento.

---

# Protección del Modelo Interno

Los consumidores nunca deben necesitar conocer:

```text
AssemblySchedule internal implementation

Convocation internal implementation

AssemblyRules internal implementation

Repository implementation

Persistence Model
```

para interpretar un Integration Event.

---

# Regla de No Acoplamiento

Debe mantenerse:

```text
External Consumer
    depends on
Integration Contract
```

No:

```text
External Consumer
    depends on
Assembly Internal Classes
```

---

# Regla de No Modificación Directa

Un consumidor no debe utilizar un Integration Event para modificar
directamente campos internos de Assembly.

Si necesita solicitar un cambio debe utilizar el flujo
correspondiente:

```text
External Intent
      │
      ▼
Integration / Application Boundary
      │
      ▼
Command
      │
      ▼
Assembly
```

---

# Entrada desde Sistemas Externos

Un mensaje externo recibido por AURA no constituye automáticamente
un Integration Event de Assembly.

Puede representar:

* evento externo;
* mensaje de integración;
* solicitud;
* intención.

Debe adaptarse antes de convertirse, cuando corresponda, en un
Command del dominio.

---

# Anti-Corruption Layer

Cuando un modelo externo no coincide con el lenguaje de AURA, la
traducción ocurre fuera del Aggregate.

Conceptualmente:

```text
External Model
      │
      ▼
Translation Boundary
      │
      ▼
AURA Contract
```

El modelo de Assembly no debe copiar estructuras externas.

---

# Entrada no Modifica Assembly Directamente

No debe existir:

```text
External Event
    │
    ▼
assembly.status = ...
```

Debe existir:

```text
External Event
    │
    ▼
Translation
    │
    ▼
Application Command
    │
    ▼
Assembly
```

cuando la semántica lo requiera.

---

# Estructura Conceptual Base

Un Integration Event puede expresarse conceptualmente como:

```text
IntegrationEvent

EventId

EventType

EventVersion

AssemblyId

OrganizationId

TerritoryId

AggregateVersion

OccurredAt

CorrelationId

CausationId

Payload
```

Esta estructura es conceptual.

No prescribe una clase, schema o formato de serialización
específico.

---

# Catálogo Conceptual

El catálogo inicial comprende:

```text
AssemblyPublished

AssemblyRescheduledForIntegration

AssemblyConvocationPublished

AssemblyConvocationUpdatedForIntegration

AssemblyStartedForIntegration

AssemblyCompletedForIntegration

AssemblyCancelledForIntegration

AssemblyArchivedForIntegration

AssemblyDetailsChanged
```

Estos contratos representan hechos de Assembly inicialmente
relevantes para interoperabilidad.

---

# AssemblyPublished — Reglas

Debe:

* identificar Assembly;
* identificar Organization;
* incluir TerritoryId cuando corresponda;
* transportar información necesaria para identificar la reunión;
* representar información ya confirmada;
* evitar información privada innecesaria.

No debe:

* conceder Permissions;
* permitir modificación directa;
* incluir otros Aggregates completos;
* incluir credenciales.

---

# AssemblyRescheduledForIntegration — Reglas

Debe:

* representar una reprogramación ya confirmada;
* identificar la programación anterior cuando forme parte del
  contrato;
* identificar la nueva programación;
* identificar Assembly;
* mantener trazabilidad.

No debe publicarse ante una reprogramación rechazada.

---

# AssemblyConvocationPublished — Reglas

Debe:

* representar una convocatoria válida;
* corresponder a una Assembly que alcanzó la condición formal
  correspondiente;
* mantener información temporal necesaria;
* mantener contexto organizacional.

No debe interpretarse como confirmación de entrega de
Notifications.

---

# AssemblyConvocationUpdatedForIntegration — Reglas

Debe representar una modificación válida de la convocatoria.

No debe utilizarse para ocultar una reprogramación si el hecho
real ocurrido corresponde a:

```text
AssemblyRescheduled
```

Los hechos deben conservar semántica explícita.

---

# AssemblyStartedForIntegration — Reglas

Debe corresponder exclusivamente a una Assembly que alcanzó:

```text
InProgress
```

mediante una operación válida.

No debe publicarse:

* desde Draft;
* desde Scheduled;
* desde Cancelled;
* desde Archived.

---

# AssemblyCompletedForIntegration — Reglas

Debe corresponder a:

```text
Completed
```

No debe utilizarse para representar:

```text
Archived
```

Debe mantenerse:

```text
Completed
    ≠
Archived
```

---

# AssemblyCancelledForIntegration — Reglas

Debe corresponder a:

```text
Cancelled
```

No debe utilizarse como equivalente a:

```text
Deleted
```

Debe mantenerse:

```text
Cancelled
    ≠
Deleted
```

---

# AssemblyArchivedForIntegration — Reglas

Debe corresponder a:

```text
Archived
```

No debe significar eliminación física.

No debe provocar cascadas implícitas sobre otros Aggregates.

---

# AssemblyDetailsChanged — Reglas

Debe representar únicamente cambios válidos de información
interoperable.

No debe convertirse en una copia completa del Aggregate.

El contrato debe poder identificar qué información cambió o
transportar exclusivamente la nueva información necesaria.

---

# Reglas Generales de Publicación

Todo Integration Event debe:

* representar un hecho confirmado;
* poseer EventId;
* poseer EventType;
* poseer EventVersion;
* identificar Assembly;
* mantener OrganizationId cuando corresponda;
* mantener OccurredAt;
* mantener contexto suficiente;
* mantener trazabilidad;
* ser inmutable;
* cumplir su contrato.

---

# Reglas de No Publicación

No debe publicarse el evento correspondiente cuando:

* el Command fue rechazado;
* Permission fue denegado;
* State Machine rechazó la transición;
* un Guard falló;
* una invariante fue violada;
* ocurrió un conflicto de concurrencia;
* la persistencia del cambio no fue confirmada;
* no existió realmente el hecho del dominio.

---

# Reglas de Privacidad

Todo Integration Event debe:

* minimizar información personal;
* limitarse al propósito contractual;
* evitar exposición innecesaria de Citizens;
* evitar exposición innecesaria de Memberships;
* evitar secretos;
* evitar credenciales;
* evitar información interna que no corresponda al consumidor.

---

# Reglas de Independencia

Los Integration Events no deben depender de:

* base de datos;
* ORM;
* framework;
* lenguaje;
* broker;
* API Gateway;
* proveedor cloud;
* protocolo específico;
* sistema municipal específico;
* plataforma Smart City específica.

---

# Reglas de Versionado Contractual

Debe mantenerse:

```text
EventVersion
```

como concepto distinto de:

```text
Assembly.Version
```

Una evolución del contrato debe documentarse.

No debe cambiarse silenciosamente el significado de una versión ya
publicada.

---

# Reglas de Trazabilidad

Los eventos deben permitir relacionar:

```text
Event

Assembly

Organization

Domain Fact

Correlation

Causation
```

sin necesidad de exponer el Aggregate completo.

---

# Reglas de Interacción entre Aggregates

Los Integration Events pueden permitir que otro contexto decida
ejecutar un Command sobre su propio Aggregate.

Conceptualmente:

```text
Assembly Integration Event
        │
        ▼
Consumer
        │
        ▼
Command
        │
        ▼
Other Aggregate
```

Assembly no modifica el otro Aggregate directamente.

---

# Ejemplo — Notification

```text
AssemblyConvocationPublished
        │
        ▼
Notification Consumer
        │
        ▼
CreateNotification
        │
        ▼
Notification
```

Assembly conserva su Boundary.

---

# Ejemplo — Document

```text
AssemblyCompletedForIntegration
        │
        ▼
Document Consumer
        │
        ▼
Document Command
        │
        ▼
Document
```

---

# Ejemplo — Audit

```text
AssemblyStartedForIntegration
        │
        ▼
Audit Consumer
        │
        ▼
Audit Process
```

---

# Ejemplo — Smart City

```text
AssemblyPublished
        │
        ▼
Smart City Adapter
        │
        ▼
External Projection
```

---

# Ejemplo — FIWARE

```text
AssemblyPublished
        │
        ▼
FIWARE Integration Adapter
        │
        ▼
External Context Representation
```

El formato externo no redefine Assembly.

---

# Ejemplo — Reprogramación

Estado anterior:

```text
AssemblyStatus:
Scheduled

ScheduledStart:
T1
```

se ejecuta una reprogramación válida.

Estado nuevo:

```text
AssemblyStatus:
Scheduled

ScheduledStart:
T2
```

Domain Event:

```text
AssemblyRescheduled
```

Integration Event:

```text
AssemblyRescheduledForIntegration
```

El estado permanece Scheduled.

El hecho comunicado es la reprogramación.

---

# Ejemplo — Convocatoria

Assembly:

```text
Scheduled
```

ejecuta una convocatoria válida.

Nuevo estado:

```text
Convoked
```

Domain Event:

```text
AssemblyConvoked
```

Integration Event:

```text
AssemblyConvocationPublished
```

Notification puede reaccionar posteriormente.

---

# Ejemplo — Inicio

Assembly:

```text
Convoked
```

ejecuta StartAssembly válidamente.

Nuevo estado:

```text
InProgress
```

Domain Event:

```text
AssemblyStarted
```

Integration Event:

```text
AssemblyStartedForIntegration
```

---

# Ejemplo — Finalización

Assembly:

```text
InProgress
```

ejecuta CompleteAssembly válidamente.

Nuevo estado:

```text
Completed
```

Domain Event:

```text
AssemblyCompleted
```

Integration Event:

```text
AssemblyCompletedForIntegration
```

---

# Ejemplo — Cancelación

Assembly:

```text
Scheduled
```

o:

```text
Convoked
```

según las reglas vigentes, puede cancelarse.

Domain Event:

```text
AssemblyCancelled
```

Integration Event:

```text
AssemblyCancelledForIntegration
```

---

# Ejemplo — Archivado

Assembly:

```text
Completed
```

o:

```text
Cancelled
```

puede alcanzar:

```text
Archived
```

Domain Event:

```text
AssemblyArchived
```

Integration Event:

```text
AssemblyArchivedForIntegration
```

---

# Ejemplo — Operación Rechazada

Assembly:

```text
Draft
```

recibe:

```text
StartAssembly
```

State Machine rechaza la operación.

No existe:

```text
AssemblyStarted
```

por lo tanto tampoco existe:

```text
AssemblyStartedForIntegration
```

---

# Ejemplo — Concurrency Conflict

Dos procesos modifican la misma Assembly sobre la misma Version.

Uno confirma primero.

El segundo recibe:

```text
AssemblyConcurrencyConflict
```

La segunda operación no produce Domain Event de éxito.

Tampoco produce Integration Event de éxito.

---

# Ejemplo — Fallo Externo

Assembly alcanzó válidamente:

```text
Completed
```

y se produjo:

```text
AssemblyCompletedForIntegration
```

Un consumidor externo falla.

Debe mantenerse:

```text
AssemblyStatus:
Completed
```

El fallo del consumidor pertenece a otro límite.

---

# Ejemplo — Evento Duplicado

Un consumidor recibe dos veces:

```text
EventId:
EVT-100
```

Debe interpretarlos como dos entregas del mismo evento lógico.

No como dos finalizaciones distintas de Assembly.

---

# Ejemplo — Dos Hechos Diferentes

Assembly puede producir en diferentes momentos:

```text
AssemblyDetailsChanged
EventId:
EVT-101
```

y posteriormente:

```text
AssemblyDetailsChanged
EventId:
EVT-102
```

Son eventos diferentes porque representan cambios diferentes.

---

# Ejemplo — Contrato Externo y Versioning

Assembly puede encontrarse en:

```text
AggregateVersion:
N
```

y producir:

```text
AssemblyStartedForIntegration

EventVersion:
1

AggregateVersion:
N
```

Los valores representan dimensiones distintas.

---

# Casos de Uso Conceptuales

Los Integration Events permiten:

```text
Publicar información de una Assembly.

Comunicar una reprogramación.

Comunicar una convocatoria.

Comunicar modificaciones relevantes de convocatoria.

Comunicar el inicio de una Assembly.

Comunicar su finalización.

Comunicar su cancelación.

Comunicar su archivado.

Actualizar proyecciones externas.

Originar procesos de Notification.

Originar procesos de Document.

Proporcionar hechos a Audit.

Proporcionar información a otros Bounded Contexts.

Integrar sistemas municipales.

Integrar plataformas ciudadanas.

Integrar sistemas Smart City.

Integrar adaptadores FIWARE.

Mantener proyecciones externas.
```

---

# Test de Publicación Válida

```text
Given valid Assembly transition

When domain fact is confirmed

Then corresponding Integration Event may be produced

And event represents the confirmed fact
```

---

# Test de Command Rechazado

```text
Given invalid Command

When Aggregate rejects operation

Then no success Integration Event is produced
```

---

# Test de Permission Denied

```text
Given Actor lacks required Permission

When Command is attempted

Then Assembly remains unchanged

And no corresponding Integration Event is produced
```

---

# Test de Invariante

```text
Given Command violates Assembly invariant

When operation is rejected

Then no corresponding Integration Event is produced
```

---

# Test de Concurrencia

```text
Given ExpectedVersion differs from PersistedVersion

When persistence is rejected

Then no Integration Event representing success is produced
```

---

# Test de Inmutabilidad

Después de publicado un Integration Event:

```text
EventId

EventType

EventVersion

AssemblyId

OccurredAt

Payload
```

no deben modificarse.

---

# Test de Información Mínima

El contrato debe contener únicamente la información necesaria para
el hecho.

No debe incluir una serialización completa de Assembly sin
justificación contractual.

---

# Test de No Exposición de Secretos

El Integration Event nunca debe contener:

```text
Password

Token

PrivateKey

Secret
```

---

# Test de Separación de Aggregates

Un Integration Event de Assembly no debe contener Aggregates
completos como:

```text
Organization

Citizen

Membership

Proposal

Voting

Document
```

---

# Test de Consumer Failure

```text
Given confirmed Assembly state

And corresponding Integration Event

When consumer fails

Then Assembly state remains confirmed
```

---

# Test de EventVersion

EventVersion debe representar la versión del contrato.

No debe confundirse con AggregateVersion.

---

# Test de EventId

Dos eventos diferentes deben poseer EventId diferentes.

Una reentrega del mismo evento conserva el mismo EventId.

---

# Relación con DOMAIN-006-Aggregate

`DOMAIN-006-Aggregate.md` constituye la fuente conceptual oficial
del Aggregate Assembly.

Este documento no redefine el Aggregate.

Desarrolla exclusivamente la comunicación externa de hechos
originados en Assembly.

---

# Relación con Lifecycle

`DOMAIN-006A-Lifecycle.md` define los estados y evolución de
Assembly.

Los Integration Events relacionados con transiciones solo pueden
representar transiciones válidamente completadas.

---

# Relación con State Machine

`DOMAIN-006B-State-Machine.md` define las transiciones permitidas.

No puede existir un Integration Event que represente una transición
rechazada por la State Machine.

---

# Relación con Commands

`DOMAIN-006C-Commands.md` define las intenciones de modificación.

Debe mantenerse permanentemente:

```text
Command
    ≠
Integration Event
```

---

# Relación con Domain Events

`DOMAIN-006D-Domain-Events.md` define los hechos internos.

Los Integration Events permiten comunicar hacia fuera hechos que
requieren interoperabilidad.

---

# Relación con Invariants

`DOMAIN-006E-Invariants.md` define las reglas que debe preservar
Assembly.

Solo los hechos producidos después de preservar dichas invariantes
pueden comunicarse como Integration Events válidos.

---

# Relación con Permissions

`DOMAIN-006F-Permissions.md` define quién puede intentar operaciones
sobre Assembly.

Un Integration Event no concede, modifica ni representa
Permissions.

---

# Relación con Repository Contract

`DOMAIN-006G-Repository-Contract.md` define la persistencia de
Assembly.

El Repository no se convierte en productor conceptual de hechos de
negocio.

La publicación de contratos externos permanece separada de su
responsabilidad principal.

---

# Relación con Examples

`DOMAIN-006H-Examples.md` muestra flujos en los cuales Assembly
puede colaborar con otros procesos sin absorberlos.

Los Integration Events permiten materializar dicha separación
conceptual.

---

# Relación con Versioning

`DOMAIN-006I-Versioning.md` define Assembly.Version.

Cuando un Integration Event transporte AggregateVersion debe
mantener exactamente el significado definido allí.

EventVersion continúa siendo independiente.

---

# Relación con Consistency Boundary

`DOMAIN-006J-Consistency-Boundary.md` establece que otros
Aggregates y sistemas externos permanecen fuera de Assembly.

Los Integration Events constituyen uno de los mecanismos para
comunicar hechos a través de esa frontera.

---

# Relación con Read Model

`DOMAIN-006L-Read-Model.md` define las proyecciones utilizadas para
consulta.

Integration Events pueden alimentar proyecciones externas cuando el
diseño correspondiente lo requiera.

Un Read Model no modifica Assembly.

---

# Relación con Test Scenarios

`DOMAIN-006M-Test-Scenarios.md` debe verificar que los Integration
Events solo representen hechos válidamente confirmados.

---

# Relación con Performance Rules

`DOMAIN-006N-Performance-Rules.md` puede establecer reglas de
rendimiento relacionadas con publicación y procesamiento sin
modificar la semántica de los contratos.

---

# Relación con Security Model

`DOMAIN-006O-Security-Model.md` define las reglas de seguridad
aplicables al Aggregate y sus interacciones.

Los Integration Events deben respetar especialmente:

* minimización de datos;
* protección de información sensible;
* ausencia de secretos;
* límites organizacionales;
* trazabilidad.

---

# Relación con Extension Points

`DOMAIN-006P-Extension-Points.md` permite incorporar nuevas
integraciones o contratos cuando aparezcan necesidades reales del
dominio.

Una extensión no debe ampliar implícitamente el Consistency
Boundary de Assembly.

---

# Restricciones

No está permitido:

* utilizar Integration Events como Commands;
* utilizar Commands como Integration Events;
* publicar hechos no confirmados;
* publicar eventos correspondientes a operaciones rechazadas;
* publicar eventos después de una violación de invariante;
* publicar eventos de éxito después de un conflicto de concurrencia;
* modificar Assembly desde un Integration Event sin pasar por el
  flujo de Commands correspondiente;
* publicar el Aggregate completo como contrato general;
* exponer entidades internas;
* exponer Aggregates externos completos;
* exponer estructuras de persistencia;
* exponer objetos ORM;
* incluir credenciales;
* incluir secretos;
* incluir tokens;
* incluir datos personales innecesarios;
* confundir EventVersion con Assembly.Version;
* confundir EventId con AssemblyId;
* confundir OccurredAt con tiempos de procesamiento;
* introducir dependencia de broker dentro del dominio;
* introducir dependencia de HTTP dentro del dominio;
* introducir dependencia de FIWARE dentro del Aggregate;
* introducir dependencia de sistemas municipales dentro del
  Aggregate;
* permitir que consumidores externos formen parte del Consistency
  Boundary;
* permitir que el fallo de un consumidor revierta automáticamente
  Assembly;
* interpretar reentregas como nuevos hechos;
* cambiar silenciosamente la semántica de un contrato publicado;
* utilizar Integration Events como sustituto de Read Models;
* utilizar Integration Events como sustituto de Audit;
* utilizar Integration Events como sustituto del Domain Model.

---

# Invariantes de Integration Events

Todo Integration Event válido debe cumplir:

* posee EventId;
* EventId identifica únicamente ese evento;
* posee EventType;
* EventType representa un hecho consumado;
* posee EventVersion;
* identifica Assembly mediante AssemblyId;
* mantiene OrganizationId cuando corresponde;
* mantiene OccurredAt;
* corresponde a un hecho confirmado;
* es inmutable;
* mantiene un Payload válido;
* contiene únicamente información necesaria;
* no contiene secretos;
* no contiene credenciales;
* no expone el Aggregate completo;
* no modifica otros Aggregates;
* no amplía el Consistency Boundary;
* no sustituye el Domain Event que lo originó.

---

# Reglas de Diseño

Todo Integration Event de Assembly debe:

* representar un hecho real;
* derivarse de una modificación válida cuando corresponda;
* permanecer separado del Command que originó la operación;
* permanecer separado del Domain Event interno;
* poseer identidad propia;
* poseer contrato explícito;
* poseer versión contractual;
* ser inmutable;
* identificar Assembly;
* preservar contexto organizacional necesario;
* preservar contexto territorial cuando corresponda;
* mantener trazabilidad;
* mantener correlación;
* mantener causalidad;
* minimizar información;
* evitar datos sensibles innecesarios;
* mantener independencia tecnológica;
* permitir evolución controlada;
* permitir consumidores independientes;
* preservar consistencia eventual entre límites.

---

# Principios Arquitectónicos

El modelo mantiene:

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
Aggregate
    ≠
Integration Contract
```

```text
Aggregate State
    ≠
Integration Payload
```

```text
Assembly.Version
    ≠
EventVersion
```

```text
EventId
    ≠
AssemblyId
```

```text
OccurredAt
    ≠
PublishedAt
```

```text
OccurredAt
    ≠
ProcessedAt
```

```text
Internal Domain Model
    ≠
External Representation
```

```text
Integration Event
    ≠
Complete Aggregate Snapshot
```

```text
Consumer
    ≠
Aggregate Owner
```

```text
Consumer Failure
    ≠
Aggregate Rollback
```

```text
Integration
    outside
Assembly Consistency Boundary
```

Estas separaciones son fundamentales para mantener el
desacoplamiento del modelo.

---

# Compatibilidad Arquitectónica

El modelo de Integration Events de Assembly es compatible con:

* Domain-Driven Design;
* Strategic DDD;
* Tactical DDD;
* Aggregate Pattern;
* Clean Architecture;
* Hexagonal Architecture;
* CQRS;
* Event-Driven Architecture;
* Event Sourcing Compatible;
* arquitectura distribuida;
* consistencia eventual;
* interoperabilidad basada en contratos;
* integración con sistemas externos;
* proyecciones externas;
* sistemas Smart City;
* adaptadores municipales;
* integración FIWARE.

La compatibilidad no introduce ninguna de estas tecnologías dentro
del Aggregate.

---

# Regla de Coherencia Documental

Todo Integration Event debe mantenerse coherente con:

```text
DOMAIN-006-Aggregate.md

DOMAIN-006A-Lifecycle.md

DOMAIN-006B-State-Machine.md

DOMAIN-006C-Commands.md

DOMAIN-006D-Domain-Events.md

DOMAIN-006E-Invariants.md

DOMAIN-006F-Permissions.md

DOMAIN-006G-Repository-Contract.md

DOMAIN-006H-Examples.md

DOMAIN-006I-Versioning.md

DOMAIN-006J-Consistency-Boundary.md

DOMAIN-006L-Read-Model.md
```

Un Integration Event no puede introducir silenciosamente:

* nuevos estados;
* nuevas transiciones;
* nuevos Commands;
* nuevas invariantes;
* nuevos Permissions;
* nuevas entidades internas;
* nuevas responsabilidades del Aggregate;
* nuevos Aggregates.

---

# Regla de Evolución

Cuando aparezca una nueva necesidad de interoperabilidad debe
evaluarse si existe realmente un hecho de Assembly que requiera
comunicación externa.

La incorporación de un nuevo Integration Event debe preservar:

* semántica del Aggregate;
* Consistency Boundary;
* separación entre Domain Events e Integration Events;
* Versioning;
* seguridad;
* privacidad;
* independencia tecnológica.

Un nuevo consumidor no debe requerir modificar Assembly si el
hecho necesario ya puede expresarse mediante un contrato de
integración apropiado.

---

# Definición de Éxito

Los **Integration Events** del Aggregate **Assembly** constituyen
los contratos oficiales mediante los cuales hechos relevantes de
una Asamblea pueden comunicarse fuera del Bounded Context
**Assembly Management** sin exponer ni acoplar directamente el
modelo interno del Aggregate.

Assembly continúa siendo responsable exclusivamente de:

* identidad;
* estado;
* Lifecycle;
* State Machine;
* Guards;
* invariantes;
* reglas;
* condiciones de realización;
* Version;
* consistencia interna.

Los Integration Events permanecen fuera de la Aggregate Root y del
Consistency Boundary.

Su existencia permite transformar hechos internos como:

```text
AssemblyRescheduled

AssemblyConvoked

AssemblyStarted

AssemblyCompleted

AssemblyCancelled

AssemblyArchived
```

en contratos externos como:

```text
AssemblyRescheduledForIntegration

AssemblyConvocationPublished

AssemblyStartedForIntegration

AssemblyCompletedForIntegration

AssemblyCancelledForIntegration

AssemblyArchivedForIntegration
```

cuando exista una necesidad real de interoperabilidad.

Todo Integration Event representa un hecho ya confirmado.

Una operación rechazada por Permission, State Machine, Guards,
invariantes o Versioning no produce un Integration Event de éxito.

Cada contrato mantiene identidad propia mediante EventId,
identifica Assembly mediante AssemblyId, conserva el contexto
organizacional necesario, puede mantener TerritoryId y
AggregateVersion cuando corresponda, registra OccurredAt y permite
mantener correlación y causalidad.

EventVersion representa exclusivamente la evolución del contrato de
integración y permanece conceptualmente separado de
Assembly.Version.

Los contratos transportan únicamente información necesaria y no
exponen el Aggregate completo, entidades internas, estructuras de
persistencia, credenciales, secretos o datos personales
innecesarios.

Organization, Territory, Citizen, Membership, Role, Proposal,
Participation, Voting, Document, Notification y Audit conservan
sus propios Aggregates y límites de consistencia.

Los consumidores reaccionan a los Integration Events mediante sus
propios procesos y reglas sin obtener acceso mutable a Assembly.

Los fallos, retrasos o reintentos de consumidores externos no
redefinen hechos de Assembly que ya hayan sido válidamente
confirmados.

La interoperabilidad con sistemas municipales, plataformas
ciudadanas, Smart City, FIWARE y otras integraciones se realiza
mediante adaptadores y contratos externos sin introducir
dependencias tecnológicas dentro del dominio.

De esta forma,
**DOMAIN-006K-Integration-Events.md** establece el modelo
conceptual y normativo oficial para comunicar hechos del Aggregate
Assembly más allá de su límite interno, preservando
desacoplamiento, trazabilidad, consistencia eventual entre
contextos, evolución contractual, privacidad, independencia
tecnológica y los principios Domain-Driven Design establecidos para
AURA Core.
