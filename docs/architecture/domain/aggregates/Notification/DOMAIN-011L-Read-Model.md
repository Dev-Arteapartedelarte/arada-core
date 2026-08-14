# DOMAIN-011L — Notification Read Model

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Notification Management

Aggregate:
Notification

Documentos relacionados:

- DOMAIN-011-Aggregate.md
- DOMAIN-011A-Lifecycle.md
- DOMAIN-011B-State-Machine.md
- DOMAIN-011C-Commands.md
- DOMAIN-011D-Domain-Events.md
- DOMAIN-011E-Invariants.md
- DOMAIN-011G-Repository-Contract.md
- DOMAIN-011I-Versioning.md
- DOMAIN-011J-Consistency-Boundary.md
- DOMAIN-011K-Integration-Events.md

---

# Objetivo

Este documento define el modelo conceptual de lectura del Aggregate
**Notification** dentro de una arquitectura CQRS.

El Read Model permite consultar información derivada del estado y
de los hechos confirmados de Notification sin utilizar el Aggregate
de escritura como mecanismo de consulta.

El Read Model:

- representa información de lectura;
- puede estar denormalizado;
- puede construirse mediante proyecciones;
- puede optimizarse según necesidades de consulta;
- no modifica el Aggregate;
- no ejecuta Commands;
- no aplica transiciones;
- no constituye autoridad sobre las Invariants.

---

# Principio Fundamental

Debe mantenerse:

```text
Write Model

≠

Read Model
```

Notification constituye la autoridad de escritura.

El Read Model constituye una representación derivada para
consultas.

Conceptualmente:

```text
Command

    │
    ▼

Notification Aggregate

    │
    ▼

Domain Event

    │
    ▼

Projection

    │
    ▼

Notification Read Model
```

---

# Responsabilidad

El Read Model es responsable de facilitar consultas sobre
Notifications confirmadas.

Puede representar información necesaria para conocer:

- identidad de la Notification;
- estado actual;
- Version proyectada;
- CreatedAt;
- UpdatedAt;
- referencias externas disponibles;
- información derivada de sus Domain Events;
- información de entrega cuando forme parte del contrato
  proyectado;
- información necesaria para trazabilidad y consulta.

El contenido concreto de cada proyección depende de las necesidades
de lectura oficialmente definidas.

---

# No Responsabilidad

El Read Model no es responsable de:

- crear Notifications;
- modificar Notifications;
- cambiar NotificationStatus;
- validar Commands;
- validar State Machine;
- validar Invariants como autoridad de escritura;
- incrementar Version;
- producir Domain Events;
- producir Integration Events por decisión propia;
- ejecutar entregas;
- ejecutar reintentos;
- modificar otros Aggregates.

---

# Autoridad

La autoridad del dominio permanece en:

```text
Notification Aggregate
```

Nunca en:

```text
Notification Read Model
```

Debe mantenerse:

```text
Read Model State

=

Derived State
```

mientras:

```text
Aggregate State

=

Authoritative Write State
```

---

# Proyección Base

La representación conceptual mínima de una Notification puede
contener:

```text
NotificationReadModel

    NotificationId

    NotificationStatus

    Version

    CreatedAt

    UpdatedAt
```

Esta estructura representa una proyección conceptual.

No constituye una nueva Entity de dominio.

---

# NotificationId

El Read Model mantiene:

```text
NotificationId
```

como referencia al Aggregate originador.

Debe mantenerse:

```text
ReadModel.NotificationId

=

Notification.NotificationId
```

para la Notification proyectada.

NotificationId no adquiere una identidad distinta dentro del Read
Model.

---

# NotificationStatus

El Read Model puede proyectar:

```text
Draft

Pending

Delivered

Failed
```

correspondientes al Lifecycle oficial versión 1.0.

NotificationStatus proyectado representa el último estado conocido
por la proyección.

No permite modificar el Aggregate.

---

# Version

El Read Model puede mantener:

```text
Version
```

correspondiente a la última Version del Aggregate procesada por la
proyección.

Conceptualmente:

```text
Domain Event

AggregateVersion = N

↓

Projection

↓

ReadModel.Version = N
```

cuando la proyección ha procesado correctamente dicho hecho.

---

# Version Proyectada

La Version proyectada permite:

- trazabilidad;
- conocer hasta qué evolución del Aggregate fue procesada;
- detectar conceptualmente retraso de proyección;
- mantener orden lógico de aplicación de hechos.

Sin embargo:

```text
ReadModel.Version

≠

Aggregate Version Authority
```

La Version autoritativa pertenece al Write Model.

---

# CreatedAt

El Read Model puede proyectar:

```text
CreatedAt
```

asociado a la creación de Notification.

CreatedAt permanece conceptualmente inmutable.

---

# UpdatedAt

El Read Model puede proyectar:

```text
UpdatedAt
```

correspondiente a la última modificación válida conocida por la
proyección.

Debido a consistencia eventual, el valor proyectado puede estar
temporalmente atrasado respecto del Write Model.

---

# Proyección desde NotificationCreated

Cuando ocurre:

```text
NotificationCreated
```

una proyección puede crear:

```text
NotificationReadModel

NotificationId = event.NotificationId

NotificationStatus = Draft

Version = event.AggregateVersion

CreatedAt = event.OccurredAt
```

La proyección no vuelve a ejecutar:

```text
CreateNotification
```

---

# Proyección desde NotificationQueued

Cuando ocurre:

```text
NotificationQueued
```

la proyección puede actualizar:

```text
NotificationStatus = Pending

Version = event.AggregateVersion

UpdatedAt = event.OccurredAt
```

La proyección no ejecuta:

```text
QueueNotification
```

ni valida nuevamente la transición como autoridad del dominio.

---

# Proyección desde NotificationDelivered

Cuando ocurre:

```text
NotificationDelivered
```

la proyección puede representar:

```text
NotificationStatus = Delivered

Version = event.AggregateVersion

UpdatedAt = event.OccurredAt
```

Delivered continúa significando exclusivamente entrega confirmada.

El Read Model no debe reinterpretarlo como:

```text
Read

Opened

Acknowledged
```

---

# Proyección desde NotificationDeliveryFailed

Cuando ocurre:

```text
NotificationDeliveryFailed
```

la proyección puede representar:

```text
NotificationStatus = Failed

Version = event.AggregateVersion

UpdatedAt = event.OccurredAt
```

El estado proyectado Failed no implica:

```text
Deleted
```

ni modifica el Aggregate originador.

---

# Proyección desde NotificationRetried

Cuando ocurre:

```text
NotificationRetried
```

la proyección puede representar:

```text
NotificationStatus = Pending

Version = event.AggregateVersion

UpdatedAt = event.OccurredAt
```

El mismo:

```text
NotificationId
```

permanece asociado a la proyección.

---

# Flujo de Proyección

Ejemplo exitoso:

```text
NotificationCreated
        │
        ▼
Draft Projection
        │
        ▼
NotificationQueued
        │
        ▼
Pending Projection
        │
        ▼
NotificationDelivered
        │
        ▼
Delivered Projection
```

Ejemplo con fallo y reintento:

```text
NotificationCreated
        │
        ▼
      Draft
        │
        ▼
NotificationQueued
        │
        ▼
     Pending
        │
        ▼
NotificationDeliveryFailed
        │
        ▼
      Failed
        │
        ▼
NotificationRetried
        │
        ▼
     Pending
        │
        ▼
NotificationDelivered
        │
        ▼
    Delivered
```

---

# Consultas Conceptuales

El Read Side puede soportar consultas conceptuales tales como:

```text
GetNotificationById

ListNotifications

FindNotificationsByStatus
```

cuando dichas consultas sean requeridas por los casos de uso.

Estas operaciones:

- no son Commands;
- no pertenecen a la Aggregate Root;
- no producen Domain Events;
- no modifican Notification.

---

# Consulta por NotificationId

Una consulta puede recuperar la representación proyectada de:

```text
NotificationId
```

Conceptualmente:

```text
GetNotificationById(NotificationId)

↓

NotificationReadModel
```

o ausencia de resultado cuando la proyección no contiene una
Notification correspondiente.

---

# Consulta por Estado

El Read Side puede permitir consultar Notifications según:

```text
Draft

Pending

Delivered

Failed
```

Estas consultas representan necesidades de lectura.

No justifican introducir métodos de búsqueda dentro del Repository
del Aggregate.

Debe mantenerse:

```text
Aggregate Repository

≠

Read Query Repository
```

---

# Listado

Un Read Model puede soportar listados de Notifications.

Los criterios concretos de:

- orden;
- paginación;
- filtrado;
- búsqueda;

pertenecen al modelo de lectura y no modifican el Aggregate.

---

# Información Derivada

Los Read Models pueden contener información derivada de hechos
confirmados.

Por ejemplo, una proyección podría determinar conceptualmente que
una Notification ha experimentado un reintento a partir de:

```text
NotificationRetried
```

sin modificar el estado autoritativo del Aggregate.

Cualquier información derivada:

```text
Derived Data
```

permanece como información de lectura.

---

# Denormalización

Los Read Models pueden denormalizar información para optimizar
consultas.

Esta capacidad no altera el Consistency Boundary del Aggregate.

Debe mantenerse:

```text
Denormalized Read Data

≠

Aggregate State
```

La existencia de información de otros contextos dentro de una
proyección no convierte dichos Aggregates en elementos internos de
Notification.

---

# Información de Otros Aggregates

Una proyección de lectura puede combinar información procedente de
diferentes fuentes cuando exista una necesidad de consulta.

Conceptualmente:

```text
Notification Projection

+

External Context Projection

↓

Composite Read Model
```

Esto no modifica los límites de consistencia.

Debe mantenerse:

```text
Composite Read Model

≠

Multi-Aggregate Write Model
```

---

# Consistencia Eventual

El Read Model puede estar temporalmente desactualizado respecto del
Aggregate.

Conceptualmente:

```text
Notification.Version = N

ReadModel.Version = N - 1
```

puede existir durante una ventana de propagación.

Esto no representa corrupción del Aggregate.

Representa consistencia eventual entre Write Side y Read Side.

---

# Lag de Proyección

El tiempo transcurrido entre:

```text
Domain Event Confirmed
```

y:

```text
Read Model Updated
```

representa un retraso de proyección.

Este retraso:

- no modifica Notification;
- no revierte Domain Events;
- no incrementa Version;
- no altera Lifecycle.

---

# Orden de Aplicación

Para un mismo NotificationId, los eventos deben proyectarse
respetando:

```text
AggregateVersion
```

Conceptualmente:

```text
Version 1

NotificationCreated

↓

Version 2

NotificationQueued

↓

Version 3

NotificationDelivered
```

La proyección no debe interpretar una Version anterior como si
fuera posterior a una Version ya procesada.

---

# Idempotencia de Proyección

Una misma notificación de evento puede ser recibida más de una vez.

El procesamiento repetido del mismo hecho no debe producir un estado
proyectado incorrecto.

Conceptualmente:

```text
Same Event

↓

Projection

↓

Same Read State
```

La estrategia técnica de idempotencia pertenece a Infrastructure.

---

# Reconstrucción

Los Read Models deben poder reconstruirse a partir de hechos
disponibles cuando la arquitectura conserve los eventos necesarios.

Conceptualmente:

```text
Domain Events

↓

Replay

↓

Projection

↓

Rebuilt Read Model
```

La reconstrucción del Read Model:

- no ejecuta Commands;
- no modifica Notification;
- no produce nuevos Domain Events;
- no incrementa Notification.Version.

---

# Rebuild

Un rebuild completo de proyecciones no constituye una operación de
dominio.

Debe mantenerse:

```text
Read Model Rebuild

≠

Notification Modification
```

y:

```text
Read Model Rebuild

↓

No Notification Version Increment
```

---

# Read Model y Repository

El Repository oficial del Aggregate se utiliza para:

```text
Notification Write Model
```

El Read Side puede utilizar mecanismos de consulta distintos.

Debe mantenerse:

```text
NotificationRepository

=

Aggregate Persistence Contract
```

mientras:

```text
Read Store / Projection Store

=

Query Concern
```

El contrato de Repository no debe transformarse en un catálogo de
consultas de lectura.

---

# Read Model y Domain Events

Los Domain Events oficiales que pueden alimentar proyecciones son:

```text
NotificationCreated

NotificationQueued

NotificationDelivered

NotificationDeliveryFailed

NotificationRetried
```

Las proyecciones reaccionan a hechos ya confirmados.

Nunca deben producir esos hechos como autoridad del dominio.

---

# Read Model e Integration Events

Los Read Models internos pueden proyectarse desde Domain Events.

Los Read Models externos o distribuidos pueden utilizar Integration
Events cuando exista el contrato correspondiente.

Debe mantenerse:

```text
Domain Event Projection

≠

Mandatory Integration Event Projection
```

La elección del contrato utilizado depende del límite del
consumidor.

---

# Read Model y Audit

El Read Model no reemplaza Audit.

Puede mostrar información de trazabilidad derivada, pero:

```text
Read Model

≠

Audit Record
```

Audit mantiene su propio modelo y responsabilidad.

---

# Read Model y Historial

Una proyección de estado actual no reemplaza el historial de Domain
Events.

Debe mantenerse:

```text
Current Read State

≠

Complete Domain History
```

Si existe una necesidad de consultar historial, puede definirse una
proyección específica basada en hechos confirmados.

Esa proyección sigue sin convertirse en autoridad de escritura.

---

# Seguridad

Los Read Models deben exponer únicamente la información permitida
por las políticas de lectura aplicables.

La existencia de datos en el Write Model no implica su exposición
automática en una proyección.

Deben respetarse:

- autorización de lectura;
- minimización de información;
- protección de datos;
- contratos de exposición;
- restricciones del consumidor.

El Read Model no almacena credenciales como parte del dominio.

---

# Permissions de Lectura

Las Permissions de lectura pueden diferir de las Permissions de
escritura.

Debe mantenerse:

```text
Read Permission

≠

Write Permission
```

cuando las políticas aplicables así lo determinen.

La autorización de una consulta no habilita la ejecución de un
Command.

---

# Infrastructure

La representación física de los Read Models pertenece a
Infrastructure.

Puede utilizar:

- bases de datos relacionales;
- bases de datos documentales;
- índices de búsqueda;
- caches;
- almacenes analíticos;
- otros mecanismos optimizados para lectura.

Ninguna tecnología concreta forma parte del dominio.

Debe mantenerse:

```text
Read Model Concept

≠

Read Storage Technology
```

---

# CQRS

Notification mantiene separación explícita entre:

```text
Write Side
```

y:

```text
Read Side
```

El Write Side contiene:

```text
Commands

Aggregate

Lifecycle

State Machine

Invariants

Repository Contract
```

El Read Side contiene:

```text
Projections

Read Models

Queries
```

Ambos pueden evolucionar independientemente mientras los contratos
permanezcan coherentes.

---

# Compatibilidad con Event Sourcing

Cuando la arquitectura utilice Event Sourcing, los mismos Domain
Events utilizados para reconstruir Notification pueden alimentar
las proyecciones.

Conceptualmente:

```text
Event Stream

      │
      ├────────► Aggregate Reconstruction
      │
      └────────► Read Model Projection
```

Ambas responsabilidades permanecen separadas.

La reconstrucción del Aggregate produce estado autoritativo.

La proyección produce estado de consulta.

---

# Escenario — Notification Draft

Después de:

```text
NotificationCreated
```

el Read Model puede representar:

```text
NotificationId = N

NotificationStatus = Draft

Version = 1
```

---

# Escenario — Notification Pending

Después de:

```text
NotificationQueued
```

puede representar:

```text
NotificationId = N

NotificationStatus = Pending

Version = 2
```

---

# Escenario — Notification Failed

Después de:

```text
NotificationDeliveryFailed
```

puede representar:

```text
NotificationId = N

NotificationStatus = Failed

Version = 3
```

---

# Escenario — Notification Retried

Después de:

```text
NotificationRetried
```

la misma proyección puede representar:

```text
NotificationId = N

NotificationStatus = Pending

Version = 4
```

---

# Escenario — Notification Delivered

Después de:

```text
NotificationDelivered
```

puede representar:

```text
NotificationId = N

NotificationStatus = Delivered

Version = 5
```

sin modificar la Notification original.

---

# Reglas Fundamentales

El Read Model de Notification debe cumplir:

1. Es una representación derivada.
2. No constituye Aggregate Root.
3. No modifica Notification.
4. No ejecuta Commands.
5. No cambia NotificationStatus autoritativamente.
6. No incrementa Notification.Version.
7. No produce Domain Events como autoridad del dominio.
8. Puede construirse desde hechos confirmados.
9. Puede estar denormalizado.
10. Puede contener información derivada.
11. Puede combinar información externa para lectura sin modificar
    Consistency Boundaries.
12. Puede estar temporalmente desactualizado.
13. Debe respetar AggregateVersion al proyectar hechos del mismo
    NotificationId.
14. Debe tolerar procesamiento idempotente.
15. Puede reconstruirse sin modificar el Write Model.
16. El Repository del Aggregate permanece separado de los
    mecanismos de consulta.
17. Read Model no reemplaza Domain Event History.
18. Read Model no reemplaza Audit.
19. Las Permissions de lectura permanecen separadas de las de
    escritura cuando corresponda.
20. Infrastructure no determina la semántica del dominio.

---

# Definición de Éxito

El Read Model del Aggregate **Notification** proporciona una
representación optimizada y desacoplada para consultar el estado
derivado de las Notifications dentro del ecosistema AURA.

El modelo permite proyectar:

```text
NotificationId

NotificationStatus

Version

CreatedAt

UpdatedAt
```

y otra información de lectura oficialmente requerida sin ampliar
el Consistency Boundary del Aggregate.

El modelo garantiza que:

- Notification permanece como autoridad de escritura;
- el Read Model permanece como representación derivada;
- los Commands no forman parte del Read Side;
- las Queries no forman parte del Aggregate;
- los Domain Events pueden alimentar proyecciones;
- Draft, Pending, Delivered y Failed pueden representarse como
  estados proyectados;
- la Version proyectada indica el último estado lógico procesado;
- las proyecciones pueden estar temporalmente desactualizadas;
- la consistencia entre Write Side y Read Side puede ser eventual;
- el procesamiento debe preservar el orden lógico de los eventos;
- los eventos duplicados no deben producir estados proyectados
  incorrectos;
- los Read Models pueden reconstruirse;
- un rebuild no modifica Notification;
- la denormalización no altera los límites DDD;
- la información de múltiples Aggregates puede combinarse para
  lectura sin crear un Multi-Aggregate Write Model;
- el Repository del Aggregate permanece separado de las consultas;
- los Read Models no reemplazan Audit;
- los Read Models no reemplazan el historial de Domain Events;
- las políticas de lectura permanecen separadas de las reglas del
  Aggregate;
- CQRS mantiene explícitamente separados Write Side y Read Side;
- Event Sourcing puede utilizar los mismos hechos para
  reconstrucción y proyección sin mezclar responsabilidades;
- la tecnología de almacenamiento del Read Side permanece fuera
  del dominio.

De esta forma, `DOMAIN-011L-Read-Model.md` establece el modelo
conceptual de lectura del Aggregate **Notification** conforme al
patrón consolidado de AURA Core.