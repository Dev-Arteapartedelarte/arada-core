# DOMAIN-010N — Document Performance Rules

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Document Management

Aggregate:
Document

Documentos relacionados:

- DOMAIN-010-Aggregate.md
- DOMAIN-010G-Repository-Contract.md
- DOMAIN-010J-Consistency-Boundary.md
- DOMAIN-010K-Integration-Events.md
- DOMAIN-010L-Read-Model.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Este documento establece las reglas oficiales de rendimiento
(Performance Rules) para el Aggregate **Document**.

Su propósito es garantizar que el Aggregate mantenga un
comportamiento predecible, escalable y consistente,
independientemente del crecimiento de la plataforma AURA.

Las reglas aquí descritas forman parte de la arquitectura del
dominio y deberán respetarse en todas las implementaciones.

---

# Principios

El Aggregate Document debe cumplir los siguientes principios:

- baja latencia;
- alta cohesión;
- tamaño reducido;
- consistencia inmediata;
- independencia tecnológica;
- escalabilidad horizontal.

---

# Responsabilidad del Aggregate

El Aggregate debe ejecutar únicamente lógica de negocio.

Nunca debe realizar:

- consultas complejas;
- agregaciones;
- búsquedas;
- cálculos estadísticos;
- operaciones analíticas;
- procesamiento masivo;
- llamadas de red;
- acceso a servicios externos.

Estas responsabilidades pertenecen a otros componentes de la
arquitectura.

---

# Tamaño del Aggregate

El Aggregate debe mantenerse pequeño.

Debe contener únicamente:

- identidad;
- estado;
- Content;
- reglas de negocio;
- Value Objects;
- entidades internas indispensables.

Nunca debe incorporar colecciones ilimitadas de objetos.

Content pertenece al Consistency Boundary de Document, pero su
mecanismo técnico de almacenamiento no debe provocar que el
Aggregate absorba responsabilidades de Infrastructure.

---

# Tiempo de Ejecución

La ejecución de un Command debe ser constante y predecible.

Objetivos conceptuales:

- complejidad O(1) para operaciones internas;
- evitar recorridos completos de colecciones;
- evitar algoritmos de crecimiento cuadrático o exponencial.

Los Commands oficiales:

```text
CreateDocument

PublishDocument

ArchiveDocument
```

deben permanecer enfocados en las reglas necesarias para modificar
una única instancia de Document.

---

# Persistencia

Cada Command debe producir como máximo:

- una carga del Aggregate;
- una persistencia del Aggregate.

No deben existir múltiples escrituras parciales durante una misma
operación.

Document debe persistirse como una unidad de consistencia conforme
a:

```text
DOMAIN-010G-Repository-Contract.md
```

---

# Transacciones

Las transacciones deben ser:

- cortas;
- atómicas;
- consistentes;
- aisladas;
- duraderas.

El Aggregate nunca debe mantener transacciones abiertas mientras
espera respuestas externas.

Ningún sistema externo debe formar parte de la transacción interna
de Document.

---

# Consultas

El Aggregate nunca responde consultas complejas.

Ejemplos de consultas que no pertenecen al Aggregate:

- Documents por DocumentType;
- Documents en Draft;
- Documents Published;
- Documents Archived;
- búsquedas documentales;
- listados documentales;
- historial de Documents.

Todas ellas pertenecen a los Read Models.

La definición de las proyecciones se encuentra en:

```text
DOMAIN-010L-Read-Model.md
```

---

# Eventos

Los Domain Events deben generarse durante la ejecución del
Aggregate.

Los Domain Events oficiales son:

```text
DocumentCreated

DocumentPublished

DocumentArchived
```

Su publicación debe realizarse después del commit mediante el
Outbox Pattern o un mecanismo equivalente.

El Aggregate nunca espera la confirmación de los consumidores.

La entrega o procesamiento posterior de un evento no debe mantener
abierta la transacción de Document.

---

# Consistencia

La consistencia inmediata se limita al Aggregate Document.

Las operaciones que involucren múltiples Aggregates utilizarán
consistencia eventual mediante eventos.

Esto evita bloqueos y mejora la escalabilidad.

Debe mantenerse:

```text
Document Consistency Boundary

≠

Distributed Transaction Boundary
```

La definición completa pertenece a:

```text
DOMAIN-010J-Consistency-Boundary.md
```

---

# Concurrencia

El Aggregate utiliza:

```text
Optimistic Concurrency Control
```

No se permiten bloqueos pesimistas como estrategia principal.

Los conflictos deben resolverse mediante control de Version.

Conceptualmente:

```text
PersistedVersion

≠

ExpectedVersion

↓

ConcurrencyConflict
```

Una escritura incompatible nunca debe sobrescribir silenciosamente
una modificación confirmada previamente.

---

# Read Models

Las consultas de alta frecuencia deben dirigirse siempre a los
Read Models.

Nunca deben reconstruirse Aggregates para responder búsquedas o
listados.

Las proyecciones oficiales definidas para Document son:

```text
DocumentSummary

DocumentDetail

DocumentStatus

DocumentHistory
```

Los Read Models absorben las necesidades de consulta sin ampliar el
Consistency Boundary del Aggregate.

---

# Índices

Los índices pertenecen exclusivamente a Infrastructure.

El dominio nunca define:

- índices SQL;
- índices NoSQL;
- motores de búsqueda;
- estructuras de almacenamiento.

La necesidad de optimizar una consulta no modifica el Aggregate.

---

# Caché

El Aggregate no depende de mecanismos de caché.

Si se implementan estrategias de caché, deberán ubicarse en la
capa de Infrastructure o en los Application Services.

La consistencia del dominio no puede depender del caché.

Debe mantenerse:

```text
Cache State

≠

Domain Source of Truth
```

---

# Escalabilidad

El diseño debe permitir:

- múltiples instancias de aplicación;
- procesamiento distribuido;
- particionamiento por Aggregate;
- procesamiento paralelo de eventos;
- escalado horizontal.

No debe existir estado compartido en memoria entre instancias.

Cada Document conserva su propio:

```text
DocumentId

Version

Consistency Boundary
```

---

# Consumo de Memoria

Durante la ejecución de un Command, el Aggregate debe mantener
únicamente el estado necesario para completar la operación.

No debe cargar información perteneciente a otros Aggregates.

En particular, no debe cargar instancias completas de:

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

Notification

Audit

Integration
```

Las relaciones externas se mantienen mediante identificadores y
contratos.

---

# Integración

Las integraciones con:

- FIWARE;
- plataformas municipales;
- servicios de identidad;
- motores de mensajería;
- sistemas analíticos;

deben realizarse fuera del Aggregate mediante Application Services
o Infrastructure Services.

Document no espera respuestas de sistemas externos durante la
ejecución de sus Commands.

Los Integration Events se rigen por:

```text
DOMAIN-010K-Integration-Events.md
```

---

# Métricas Recomendadas

Las implementaciones deberán monitorear, entre otras, las
siguientes métricas:

- tiempo promedio de ejecución por Command;
- tiempo de persistencia;
- tasa de conflictos de concurrencia;
- tiempo de publicación de eventos;
- throughput de Commands;
- latencia de reconstrucción de Read Models;
- utilización de memoria.

Estas métricas no forman parte del dominio, pero permiten verificar
el cumplimiento de las reglas arquitectónicas.

---

# Antipatrones

Las siguientes prácticas están prohibidas dentro del Aggregate:

- consultas SQL;
- acceso directo a MongoDB;
- llamadas HTTP;
- llamadas gRPC;
- acceso a Redis;
- publicación directa en Kafka, RabbitMQ o MQTT;
- lectura directa desde File System como responsabilidad de
  negocio;
- operaciones de entrada/salida;
- lógica de presentación;
- lógica de autenticación.

El mecanismo utilizado para persistir o recuperar técnicamente
Content pertenece a Infrastructure y no modifica la responsabilidad
del Aggregate.

---

# Compatibilidad con CQRS

El lado de escritura permanece optimizado para operaciones
transaccionales.

El lado de lectura absorbe toda la carga de consultas,
estadísticas y búsquedas masivas.

Conceptualmente:

```text
Command

↓

Document

↓

Domain Event
```

y:

```text
Domain Event

↓

Projection

↓

Read Model
```

Las necesidades de lectura no deben incrementar el tamaño del
Aggregate.

---

# Compatibilidad con Event Sourcing

En implementaciones Event Sourcing:

- la reconstrucción del Aggregate debe depender únicamente de
  los eventos asociados a su **DocumentId**;
- el historial de otros Aggregates nunca debe cargarse durante
  la ejecución.

Conceptualmente:

```text
DocumentCreated

↓

DocumentPublished

↓

DocumentArchived
```

puede reconstruir la evolución del mismo Document cuando el modelo
de persistencia adoptado utilice Event Sourcing.

La reconstrucción no debe provocar llamadas a otros Aggregates.

---

# Principios Arquitectónicos

Estas reglas siguen los principios de:

- Domain-Driven Design (DDD);
- CQRS;
- Event Sourcing;
- Clean Architecture;
- SOLID;
- Hexagonal Architecture;
- High Cohesion;
- Low Coupling.

---

# Definición de Éxito

El Aggregate **Document** mantiene un rendimiento constante,
escalable y desacoplado al limitar su responsabilidad a la
ejecución de reglas de negocio.

El modelo garantiza que:

- el Aggregate permanezca pequeño;
- los Commands ejecuten únicamente comportamiento de dominio;
- Document no cargue Aggregates externos;
- la persistencia opere sobre una única unidad de consistencia;
- las transacciones permanezcan cortas;
- las consultas complejas sean atendidas mediante Read Models;
- los Domain Events no bloqueen la ejecución esperando
  consumidores;
- la consistencia inmediata permanezca limitada a Document;
- la coordinación externa utilice consistencia eventual;
- Optimistic Concurrency Control proteja modificaciones
  concurrentes;
- índices y caché permanezcan fuera del dominio;
- las integraciones externas no formen parte de la ejecución
  interna del Aggregate;
- CQRS mantenga separadas las cargas de escritura y lectura;
- Event Sourcing, cuando corresponda, reconstruya Document
  únicamente mediante eventos asociados a su DocumentId;
- Infrastructure no determine las reglas conceptuales de
  rendimiento.

Las consultas, integraciones, proyecciones y operaciones
distribuidas se delegan a los componentes especializados de la
arquitectura, permitiendo que AURA evolucione hacia una plataforma
de alta disponibilidad y capaz de operar a escala municipal,
regional y nacional.