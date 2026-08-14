# DOMAIN-011N — Notification Performance Rules

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
- DOMAIN-011L-Read-Model.md
- DOMAIN-011M-Test-Scenarios.md

---

# Objetivo

Este documento define las reglas conceptuales de Performance del
Aggregate **Notification**.

Su propósito es garantizar que el diseño del dominio mantenga un
Consistency Boundary pequeño, predecible y eficiente sin trasladar
responsabilidades de Infrastructure hacia el Aggregate.

Las reglas de Performance establecidas aquí pertenecen al diseño
conceptual del dominio.

No definen:

- tiempos concretos de respuesta;
- número de solicitudes por segundo;
- tamaño de infraestructura;
- configuración de servidores;
- número de workers;
- tecnología de cache;
- broker específico;
- base de datos específica;
- proveedor de entrega;
- estrategia física de escalamiento.

---

# Principio Fundamental

La optimización de Performance nunca puede violar:

- Lifecycle;
- State Machine;
- Invariants;
- Versioning;
- Consistency Boundary;
- Domain Events;
- separación entre Aggregates.

Debe mantenerse:

```text
Performance Optimization

≠

Domain Rule Bypass
```

Ninguna mejora técnica puede convertir una operación inválida en
válida.

---

# Aggregate Pequeño

Notification debe permanecer como un Aggregate pequeño.

Debe contener exclusivamente la información necesaria para mantener
consistente una unidad de Notification.

No debe crecer mediante incorporación de Aggregates externos.

Debe mantenerse:

```text
Notification

=

Small Consistency Boundary
```

---

# Una Notification por Aggregate

Cada instancia del Aggregate representa:

```text
One Notification
```

identificada por:

```text
NotificationId
```

El Aggregate no representa una colección masiva de Notifications.

Debe mantenerse:

```text
Notification Aggregate

≠

Notification Batch
```

y:

```text
Notification Aggregate

≠

Notification Collection
```

---

# No Carga de Aggregates Externos

Para ejecutar comportamiento de Notification no debe ser necesario
cargar como parte de su estado interno:

```text
Organization

Citizen

Membership

Role

Territory

Assembly

Proposal

Participation

Voting

Document

Audit

Integration
```

Las relaciones externas utilizan:

```text
AggregateId

Domain Contract
```

cuando corresponda.

---

# Referencias por Identidad

Las referencias hacia otros Aggregates deben mantenerse mediante
identificadores o contratos explícitos.

Esto evita ampliar innecesariamente:

```text
Aggregate Size

Transaction Scope

Loading Cost

Consistency Scope
```

Debe mantenerse:

```text
External Reference

≠

External Aggregate Loading
```

dentro del estado de Notification.

---

# No Multi-Aggregate Transaction

Una operación sobre Notification no requiere modificar
simultáneamente otro Aggregate.

Debe mantenerse:

```text
Notification Transaction

=

Notification Consistency Boundary
```

y no:

```text
Notification Transaction

=

Notification
+
Assembly
+
Citizen
+
Document
+
Other Aggregates
```

La coordinación externa utiliza consistencia eventual.

---

# Transacciones Cortas

Las operaciones de dominio sobre Notification deben mantenerse
conceptualmente acotadas.

Una operación válida:

```text
Load

↓

Validate

↓

Execute Behavior

↓

Increment Version

↓

Produce Domain Event

↓

Persist
```

no debe requerir procesos externos prolongados dentro de la
transacción del Aggregate.

---

# Entrega Externa fuera de la Transacción

La ejecución técnica de entrega permanece fuera del Consistency
Boundary.

No debe mantenerse abierta una modificación transaccional de
Notification mientras:

- un proveedor externo procesa una solicitud;
- una API remota responde;
- un broker entrega un mensaje;
- un destinatario recibe la comunicación;
- un sistema externo confirma procesamiento.

Debe mantenerse:

```text
Aggregate Transaction

≠

External Delivery Duration
```

---

# Estado Pending

El estado:

```text
Pending
```

permite representar que el resultado de entrega todavía no ha sido
confirmado sin mantener abierta una transacción del Aggregate.

Conceptualmente:

```text
Draft

↓

QueueNotification

↓

Pending

↓

Commit
```

La ejecución técnica ocurre posteriormente fuera del Aggregate.

---

# Confirmación de Resultado

Cuando existe un resultado válido de entrega, se ejecuta una nueva
operación de dominio.

Para éxito:

```text
Pending

↓

ConfirmNotificationDelivery

↓

Delivered
```

Para fallo:

```text
Pending

↓

ReportNotificationDeliveryFailure

↓

Failed
```

Cada transición constituye una modificación independiente y
acotada.

---

# Retry

`RetryNotification` representa una nueva modificación del
Aggregate.

Debe mantenerse:

```text
Failed

↓

RetryNotification

↓

Pending
```

sin ejecutar dentro de la misma modificación el mecanismo técnico
completo de entrega.

Debe mantenerse:

```text
RetryNotification

≠

Synchronous Provider Retry Loop
```

---

# Reintentos Técnicos

Los reintentos técnicos de:

- publicación;
- transporte;
- conexión;
- broker;
- proveedor;

pertenecen a Infrastructure.

No deben provocar por sí mismos:

```text
Notification.Version + 1
```

Debe mantenerse:

```text
Technical Retry

≠

Aggregate Modification
```

salvo que exista una operación de dominio válida como:

```text
RetryNotification
```

---

# Versioning y Performance

Notification utiliza:

```text
Optimistic Concurrency Control
```

para proteger escrituras concurrentes sin ampliar el Consistency
Boundary.

Debe mantenerse:

```text
ExpectedVersion

=

PersistedVersion
```

antes de confirmar una escritura.

Una escritura obsoleta debe producir:

```text
ConcurrencyConflict
```

y no bloqueo semántico del dominio.

---

# Concurrencia

Diferentes Notifications pueden evolucionar independientemente.

Conceptualmente:

```text
Notification A

Notification B

Notification C
```

poseen:

```text
Independent NotificationId

Independent Version

Independent Consistency Boundary
```

Una modificación sobre Notification A no debe requerir bloquear
Notification B o Notification C por regla del Aggregate.

---

# Paralelismo entre Aggregates

Debido a que cada Notification mantiene su propio Consistency
Boundary, operaciones sobre diferentes NotificationId pueden
ejecutarse independientemente desde el punto de vista del dominio.

Debe mantenerse:

```text
Notification A Transaction

≠

Notification B Transaction
```

La estrategia técnica concreta de paralelismo pertenece a
Infrastructure.

---

# Repository

El Repository debe recuperar y persistir una única Notification
como unidad.

Debe mantenerse:

```text
NotificationRepository

↓

NotificationId

↓

Single Aggregate
```

El Repository no debe requerir cargar colecciones completas de
Notifications para modificar una sola Notification.

---

# Consultas fuera del Aggregate

Las necesidades de consulta masiva no deben resolverse cargando
múltiples Aggregates Notification.

Ejemplos:

```text
ListNotifications

FindNotificationsByStatus

SearchNotifications
```

pertenecen al:

```text
Read Side
```

Debe mantenerse:

```text
Aggregate Repository

≠

Analytical Query Engine
```

---

# CQRS

CQRS permite separar:

```text
Write Model

↓

Consistency
```

de:

```text
Read Model

↓

Query Optimization
```

Las consultas de alto volumen no deben ampliar el Aggregate.

El Read Side puede optimizarse independientemente sin alterar:

- Lifecycle;
- State Machine;
- Commands;
- Invariants;
- Consistency Boundary.

---

# Read Models

Los Read Models pueden diseñarse para soportar eficientemente:

- listados;
- filtros;
- búsquedas;
- clasificación por estado;
- trazabilidad;
- información derivada;
- vistas compuestas.

Estas optimizaciones permanecen fuera del Write Model.

Debe mantenerse:

```text
Query Optimization

≠

Aggregate Expansion
```

---

# Denormalización

El Read Side puede utilizar información denormalizada para reducir
costos de consulta.

La denormalización no constituye una razón para copiar esa misma
estructura al Aggregate.

Debe mantenerse:

```text
Read Model Denormalization

≠

Write Model Denormalization Requirement
```

---

# Read Model Lag

La búsqueda de Performance no requiere consistencia inmediata entre
Write Side y Read Side.

Puede existir:

```text
Notification.Version = N

ReadModel.Version = N - 1
```

durante una ventana válida de propagación.

Debe mantenerse:

```text
Aggregate Internal Consistency

=

Immediate
```

mientras:

```text
Read Projection Consistency

=

Eventual
```

---

# Domain Events

Los Domain Events permiten propagar cambios sin incorporar
consumidores dentro de la transacción del Aggregate.

Conceptualmente:

```text
Notification Commit

↓

Domain Event

↓

Independent Consumers
```

Los consumidores no forman parte de la modificación atómica de
Notification.

---

# Integration Events

Los Integration Events permiten comunicar hechos fuera del Bounded
Context sin ampliar el Consistency Boundary.

Debe mantenerse:

```text
Notification Commit

≠

External Consumer Commit
```

La velocidad o disponibilidad del consumidor externo no determina
la validez interna del Aggregate.

---

# Outbox

Cuando exista Outbox, su propósito es permitir publicación
confiable posterior al commit.

El procesamiento del Outbox no debe mantener bloqueada la
transacción de Notification.

Conceptualmente:

```text
Aggregate Commit

↓

Outbox Pending

↓

Asynchronous Publication
```

El Outbox no incrementa Notification.Version durante su
procesamiento.

---

# Consumidores Lentos

Un consumidor lento no debe ampliar el Consistency Boundary de
Notification.

Debe mantenerse:

```text
Slow Consumer

≠

Long Aggregate Transaction
```

El estado confirmado del Aggregate permanece independiente de la
velocidad posterior de procesamiento.

---

# Proveedor de Entrega

Un proveedor externo:

- no pertenece al Aggregate;
- no forma parte de su transacción;
- no determina su estructura interna;
- no modifica NotificationStatus directamente.

Debe mantenerse:

```text
Provider Latency

≠

Aggregate Transaction Duration
```

---

# Fallos de Proveedor

Un fallo técnico externo no debe provocar una transacción larga ni
mantener bloqueada Notification.

Cuando el resultado de dominio correspondiente sea confirmado,
puede producirse:

```text
ReportNotificationDeliveryFailure
```

mediante una operación independiente.

---

# Batching

La agrupación técnica de múltiples entregas puede existir fuera del
Aggregate.

Sin embargo:

```text
Delivery Batch

≠

Notification Aggregate
```

Un batch técnico no fusiona múltiples NotificationId en una única
unidad de consistencia.

---

# Procesamiento Masivo

Un proceso puede coordinar múltiples Notifications.

Conceptualmente:

```text
Process

    ├── Notification A
    ├── Notification B
    └── Notification C
```

pero cada una mantiene:

```text
Independent Aggregate

Independent Version

Independent Transaction
```

El proceso coordinador permanece fuera de cada Aggregate.

---

# Orden

Notification solamente requiere preservar orden lógico dentro de
una misma identidad:

```text
NotificationId
```

mediante:

```text
AggregateVersion
```

El dominio no exige un orden global entre todas las Notifications.

Debe mantenerse:

```text
Per Aggregate Ordering

≠

Global Notification Ordering
```

---

# Event Sourcing

Cuando se utilice Event Sourcing, únicamente deben utilizarse para
reconstruir Notification los hechos correspondientes al mismo:

```text
NotificationId
```

No debe ser necesario reconstruir otros Aggregates para recuperar
una Notification.

Debe mantenerse:

```text
Notification Event Stream

=

Notification History
```

y no:

```text
Notification Event Stream

=

Entire AURA Domain History
```

---

# Reconstrucción

Una reconstrucción válida puede utilizar:

```text
NotificationCreated

NotificationQueued

NotificationDeliveryFailed

NotificationRetried

NotificationDelivered
```

correspondientes exclusivamente al NotificationId reconstruido.

La reconstrucción no ejecuta:

- consultas a otros Aggregates como requisito del modelo;
- proveedores externos;
- entregas;
- Commands nuevos.

---

# Tamaño del Historial

Los reintentos pueden producir múltiples hechos durante la vida de
una Notification.

Esto no autoriza a reescribir ni eliminar hechos históricos para
optimizar Performance.

Debe mantenerse:

```text
Performance Optimization

≠

Historical Fact Mutation
```

Las estrategias técnicas de optimización de reconstrucción
pertenecen a Infrastructure y no cambian la semántica del dominio.

---

# Caches

La utilización de cache puede optimizar lectura o acceso técnico.

Cache no constituye autoridad del Aggregate.

Debe mantenerse:

```text
Cache

≠

Domain Source of Truth
```

y:

```text
Cache Optimization

≠

Invariant Bypass
```

La tecnología y estrategia concreta de cache permanecen fuera del
dominio.

---

# Indexación

Los índices utilizados para mejorar consultas pertenecen al modelo
de persistencia o lectura.

No constituyen conceptos del Aggregate.

Debe mantenerse:

```text
Database Index

≠

Domain Invariant
```

---

# Paginación

La paginación pertenece a las necesidades de consulta de Read
Models.

No forma parte del comportamiento de Notification.

Debe mantenerse:

```text
Pagination

=

Read Concern
```

y no:

```text
Pagination

=

Aggregate Behavior
```

---

# Búsqueda

Las capacidades de búsqueda pertenecen al Read Side.

El Aggregate no debe incorporar estructuras internas destinadas
exclusivamente a optimizar:

- búsqueda textual;
- filtros;
- ordenamiento;
- agregaciones;
- estadísticas.

---

# Analytics

Las necesidades analíticas no deben ejecutarse cargando Aggregates
Notification individualmente como mecanismo principal.

Analytics puede consumir:

- Domain Events;
- Integration Events;
- Read Models;
- proyecciones especializadas.

Analytics permanece fuera del Consistency Boundary.

---

# Audit

Audit no debe ampliar la transacción de Notification.

Conceptualmente:

```text
Notification Domain Event

↓

Audit Processing
```

puede ocurrir posteriormente.

Debe mantenerse:

```text
Audit Processing Time

≠

Notification Transaction Time
```

---

# FIWARE

La integración con FIWARE permanece fuera del Aggregate.

Notification no espera una confirmación de FIWARE para considerar
internamente válida una modificación ya confirmada.

Debe mantenerse:

```text
Notification Commit

≠

FIWARE Commit
```

La propagación se mantiene desacoplada mediante contratos de
integración.

---

# Sistemas Municipales

La velocidad, disponibilidad o latencia de plataformas municipales
no determina el tamaño ni la duración de la transacción interna de
Notification.

La integración permanece eventual cuando cruza el Consistency
Boundary.

---

# Escalabilidad

El modelo permite escalabilidad al mantener:

- una Notification por Aggregate;
- transacciones independientes;
- Version independiente;
- referencias externas por identidad;
- comunicación basada en eventos;
- Read Models desacoplados;
- ejecución técnica fuera del Aggregate.

La estrategia física de escalamiento no forma parte del dominio.

---

# Hotspots

El diseño no debe introducir deliberadamente un Aggregate global
compartido por todas las Notifications.

Debe evitarse conceptualmente:

```text
GlobalNotificationAggregate

↓

All Notifications
```

como mecanismo de consistencia.

Cada Notification mantiene su propia identidad y Version.

---

# Contención

El control de concurrencia se aplica por Aggregate.

Conceptualmente:

```text
NotificationId = A

Version = N
```

constituye una unidad independiente de:

```text
NotificationId = B

Version = M
```

Esto reduce la necesidad de contención entre Notifications
independientes.

---

# Performance y Seguridad

Una optimización no puede eliminar:

- validación de Permission;
- protección de Invariants;
- control de Version;
- minimización de información;
- separación de Consistency Boundaries.

Debe mantenerse:

```text
Faster Execution

≠

Reduced Domain Protection
```

---

# Performance y Trazabilidad

La optimización no debe eliminar:

- Domain Events confirmados;
- Version necesaria;
- CorrelationId cuando corresponda;
- CausationId cuando corresponda;
- identidad del Aggregate.

Debe mantenerse:

```text
Performance

+

Traceability
```

sin sacrificar la semántica del dominio.

---

# Métricas

Las métricas técnicas de Performance pueden existir en
Infrastructure u Observability.

Ejemplos:

- latency;
- throughput;
- queue depth;
- processing time;
- delivery latency;
- projection lag;
- error rate.

Estas métricas no forman parte del estado del Aggregate por el solo
hecho de ser observadas.

Debe mantenerse:

```text
Operational Metric

≠

Notification Domain State
```

---

# Límites Cuantitativos

La versión 1.0 no establece límites cuantitativos concretos sobre:

- número de Notifications por segundo;
- número de Notifications por Organization;
- cantidad máxima de destinatarios;
- tamaño máximo de Payload;
- cantidad máxima de reintentos;
- timeout de proveedor;
- latencia máxima;
- número de consumidores;
- tamaño de batch.

La ausencia de estos valores evita introducir reglas no
consolidadas dentro del dominio.

Cuando un límite cuantitativo constituya una regla real del dominio,
deberá definirse explícitamente en el artefacto correspondiente.

---

# Performance Budget

La versión 1.0 no define un Performance Budget numérico dentro del
Aggregate.

Los objetivos técnicos de capacidad y latencia pertenecen a la
arquitectura operacional.

Debe mantenerse:

```text
Operational SLA

≠

Aggregate Invariant
```

salvo que una futura regla del dominio establezca explícitamente lo
contrario.

---

# Reglas Fundamentales

Las siguientes reglas son obligatorias:

1. Cada Notification constituye un Aggregate independiente.
2. El Aggregate debe permanecer pequeño.
3. No se almacenan Aggregates externos completos.
4. Las referencias externas utilizan identificadores o contratos.
5. Una modificación de Notification no requiere una transacción
   multi-Aggregate.
6. Las transacciones del Aggregate deben permanecer acotadas.
7. La ejecución técnica de entrega ocurre fuera de la transacción.
8. Pending permite desacoplar el resultado de entrega de la
   modificación que prepara la Notification.
9. Confirmar entrega constituye una nueva operación de dominio.
10. Reportar fallo constituye una nueva operación de dominio.
11. RetryNotification constituye una modificación del Aggregate.
12. Los retries técnicos no equivalen a RetryNotification.
13. Diferentes NotificationId poseen concurrencia independiente.
14. Version protege cada Aggregate mediante Optimistic Concurrency.
15. El Repository recupera y persiste una Notification como unidad.
16. Las consultas masivas pertenecen al Read Side.
17. La denormalización pertenece al Read Model cuando corresponda.
18. Los Domain Events desacoplan consumidores.
19. Los Integration Events no amplían el Consistency Boundary.
20. Outbox no amplía la duración de la transacción del Aggregate.
21. Consumidores lentos no mantienen abierta la transacción de
    Notification.
22. La latencia del proveedor no determina la duración de la
    transacción.
23. Los batches técnicos no fusionan Aggregates.
24. El procesamiento masivo conserva una transacción independiente
    por Notification.
25. El dominio requiere orden lógico por NotificationId, no orden
    global.
26. Event Sourcing reconstruye solamente la historia del mismo
    NotificationId.
27. Una optimización no puede modificar hechos históricos.
28. Cache no constituye autoridad del dominio.
29. Indexación, búsqueda y paginación pertenecen a lectura o
    Infrastructure.
30. Analytics permanece fuera del Aggregate.
31. Audit permanece fuera de la transacción del Aggregate.
32. FIWARE permanece fuera del Consistency Boundary.
33. Sistemas externos no determinan la consistencia interna.
34. No existe un Aggregate global para todas las Notifications.
35. Performance no puede evitar seguridad ni Invariants.
36. Performance no puede eliminar trazabilidad requerida.
37. Las métricas operacionales no constituyen automáticamente
    estado del dominio.
38. No se introducen límites cuantitativos no consolidados.
39. SLA técnicos no constituyen automáticamente Invariants.

---

# Compatibilidad con CQRS

El modelo de Performance es compatible con CQRS porque mantiene:

```text
Write Side

↓

Small Aggregate

+

Immediate Internal Consistency
```

separado de:

```text
Read Side

↓

Optimized Queries

+

Denormalized Projections
```

El crecimiento de necesidades de lectura no requiere ampliar el
Write Model.

---

# Compatibilidad con Event Sourcing

El modelo es compatible con Event Sourcing porque cada
Notification mantiene una historia independiente ordenada mediante:

```text
NotificationId

AggregateVersion
```

La estrategia técnica utilizada para optimizar replay no puede
alterar:

- hechos históricos;
- orden lógico;
- NotificationId;
- estado reconstruido;
- Version resultante.

---

# Definición de Éxito

Las Performance Rules del Aggregate **Notification** garantizan que
las necesidades de capacidad, concurrencia e integración puedan
evolucionar sin ampliar innecesariamente su Consistency Boundary ni
debilitar las reglas del dominio.

El modelo garantiza que:

- cada Notification mantiene un Aggregate independiente;
- cada Notification posee NotificationId y Version propios;
- el Aggregate permanece pequeño;
- otros Aggregates no se cargan como estado interno;
- las referencias externas utilizan identificadores o contratos;
- las modificaciones permanecen transaccionalmente acotadas;
- los proveedores externos permanecen fuera de la transacción;
- Pending desacopla la preparación de la Notification del resultado
  de entrega;
- Delivered y Failed se confirman mediante operaciones posteriores;
- RetryNotification no ejecuta un loop técnico dentro del
  Aggregate;
- los reintentos técnicos permanecen fuera del dominio;
- Optimistic Concurrency protege escrituras concurrentes;
- diferentes Notifications pueden evolucionar independientemente;
- Repository persiste una única Notification como unidad;
- las consultas masivas pertenecen al Read Side;
- Read Models pueden optimizarse y denormalizarse;
- Domain Events permiten consumidores desacoplados;
- Integration Events mantienen consistencia eventual;
- Outbox no amplía el Consistency Boundary;
- consumidores lentos no bloquean la consistencia del Aggregate;
- batching técnico no fusiona Aggregates;
- no existe requisito de orden global entre Notifications;
- Event Sourcing reconstruye únicamente la historia del mismo
  NotificationId;
- cache, índices, paginación y búsqueda permanecen fuera de la
  semántica del Aggregate;
- Analytics y Audit no amplían la transacción;
- FIWARE y sistemas municipales permanecen fuera del Boundary;
- Performance nunca permite evitar Invariants, Versioning,
  Permissions o trazabilidad;
- no se introducen límites cuantitativos o SLA como reglas de
  dominio sin definición explícita.

De esta forma, `DOMAIN-011N-Performance-Rules.md` establece las
reglas conceptuales de Performance del Aggregate **Notification**
conforme al patrón consolidado de AURA Core.