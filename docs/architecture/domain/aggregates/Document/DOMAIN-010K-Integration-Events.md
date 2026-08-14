# DOMAIN-010K — Document Integration Events

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
- DOMAIN-010D-Domain-Events.md
- DOMAIN-010I-Versioning.md
- DOMAIN-010J-Consistency-Boundary.md
- CORE-005-Domain-Events.md

---

# Objetivo

Este documento define las reglas de **Integration Events**
utilizadas por el Aggregate **Document** para permitir la
comunicación de hechos confirmados hacia otros Bounded Contexts
y sistemas externos.

A diferencia de los Domain Events, los Integration Events
constituyen contratos públicos y estables orientados a la
integración.

Su publicación ocurre únicamente después de que la modificación
correspondiente del Aggregate haya sido confirmada exitosamente.

Este documento no establece una equivalencia automática entre
Domain Events e Integration Events.

La existencia de un Domain Event no implica por sí misma la
existencia de un contrato público de integración.

---

# Principios

Los Integration Events cumplen los siguientes principios:

- representan hechos ya confirmados;
- son inmutables;
- poseen contratos públicos versionados;
- permanecen separados de los Domain Events;
- son independientes de la implementación interna del Aggregate;
- pueden ser consumidos por otros Bounded Contexts;
- pueden ser consumidos por sistemas externos;
- no modifican directamente Document;
- no modifican directamente otros Aggregates;
- respetan el Consistency Boundary;
- solamente exponen la información necesaria para integración.

Debe mantenerse:

```text
Domain Event

≠

Integration Event
```

y:

```text
Domain Event

≠

Mandatory Integration Event
```

---

# Flujo General

```text
Document Aggregate

        │

        ▼

Domain Event

        │

        ▼

Confirmed Transaction

        │

        ▼

Integration Event

        │

        ▼

External Consumers
```

La traducción de un Domain Event hacia un Integration Event
solamente ocurre cuando existe un contrato de integración
explícitamente definido para el hecho correspondiente.

---

# Relación Domain Event → Integration Event

Los Domain Events oficiales de Document son:

```text
DocumentCreated

DocumentPublished

DocumentArchived
```

Estos hechos pertenecen al Aggregate Document.

Su existencia no implica automáticamente:

```text
DocumentCreated
        │
        ▼
Integration Event
```

ni:

```text
DocumentPublished
        │
        ▼
Integration Event
```

ni:

```text
DocumentArchived
        │
        ▼
Integration Event
```

La exposición de cualquiera de estos hechos fuera del Bounded
Context requiere un contrato de Integration Event definido
explícitamente.

Debe mantenerse:

```text
Internal Domain Fact

↓

Explicit Integration Contract

↓

External Publication
```

---

# Eventos Oficiales

La versión 1.0 no deriva automáticamente contratos de Integration
Events a partir de los Domain Events existentes.

Los hechos internos actualmente definidos permanecen:

```text
DocumentCreated

DocumentPublished

DocumentArchived
```

como Domain Events.

Un contrato público de Integration Event solamente forma parte del
modelo cuando:

- exista una necesidad explícita de comunicación externa;
- el hecho a publicar esté confirmado;
- el consumidor externo necesite conocer dicho hecho;
- el contrato haya sido definido explícitamente;
- el Payload haya sido delimitado;
- su versión haya sido establecida;
- las reglas de seguridad hayan sido consideradas.

No debe inferirse un Integration Event únicamente mediante una
convención de nombres.

---

# Contrato Conceptual

Todo Integration Event definido para Document debe contener
conceptualmente:

```text
EventId

EventType

AggregateId

AggregateType

OccurredOn

Version

CorrelationId

CausationId

Payload
```

Para Document:

```text
AggregateId = DocumentId
```

y:

```text
AggregateType = Document
```

El formato físico pertenece a Infrastructure.

---

# Payload

El Payload debe contener únicamente la información necesaria para
que el consumidor comprenda y procese el contrato de integración.

Debe evitar:

- lógica de negocio;
- Aggregates completos;
- objetos internos innecesarios;
- referencias circulares;
- información redundante;
- detalles de persistencia;
- detalles de Infrastructure;
- información sensible no requerida.

Debe mantenerse:

```text
Integration Event Payload

≠

Document Aggregate Snapshot
```

y:

```text
Integration Event Payload

≠

Domain Internal Model
```

Content no debe exponerse automáticamente como parte de un
Integration Event.

Su inclusión requeriría una necesidad explícita del contrato y el
cumplimiento de las reglas de seguridad correspondientes.

---

# Consumidores

Los Integration Events de Document pueden ser consumidos por otros
Bounded Contexts o sistemas externos únicamente cuando exista un
contrato explícito entre productor y consumidor.

Un consumidor:

- no adquiere ownership sobre Document;
- no accede directamente al estado interno del Aggregate;
- no puede modificar Document mediante el Integration Event;
- mantiene su propio Consistency Boundary;
- procesa el hecho conforme a sus propias reglas.

La existencia de una relación conceptual con otro Aggregate no
constituye por sí misma una obligación de publicar un Integration
Event.

---

# Document y Assembly

Assembly puede mantener:

```text
DocumentId
```

como referencia a un Document.

Esta relación no implica que cada Domain Event de Document deba ser
publicado hacia Assembly.

Debe mantenerse:

```text
Assembly references DocumentId

≠

Assembly owns Document
```

y:

```text
Document Integration Event

≠

Direct Assembly Mutation
```

Cualquier reacción de Assembly debe respetar su propio Aggregate y
Consistency Boundary.

---

# Document y Notification

Un hecho de Document puede resultar relevante para Notification
cuando exista un proceso explícitamente definido.

Sin embargo:

```text
DocumentPublished

≠

NotificationSent
```

Document no envía Notifications directamente.

Notification conserva su propio modelo, Lifecycle e Invariants.

La comunicación entre ambos contextos debe realizarse mediante
contratos explícitos cuando corresponda.

---

# Sistemas Externos

Document puede participar en integraciones con sistemas externos
únicamente mediante contratos definidos fuera de su estado interno.

La integración no permite que sistemas externos:

- modifiquen directamente DocumentStatus;
- modifiquen directamente Content;
- modifiquen Version;
- eviten Commands;
- eviten Invariants;
- amplíen el Consistency Boundary.

Debe mantenerse:

```text
External System

↓

Explicit Contract

≠

Direct Aggregate Access
```

---

# Publicación

Los Integration Events solamente pueden publicarse después de que
la modificación que originó el hecho haya sido confirmada.

Conceptualmente:

```text
Command

↓

Document

↓

Domain Validation

↓

Domain Event

↓

Repository

↓

Commit

↓

Integration Event

↓

Consumer
```

Nunca:

```text
Integration Event

↓

Before Commit
```

porque una operación todavía no confirmada no constituye un hecho
externo estable.

---

# Garantías

El modelo de Integration Events debe preservar:

- hechos confirmados;
- desacoplamiento entre productor y consumidores;
- consistencia eventual;
- identidad propia del evento;
- trazabilidad;
- versionado del contrato;
- procesamiento idempotente;
- independencia tecnológica.

La entrega técnica de mensajes no modifica el significado del
contrato.

---

# Idempotencia

Un consumidor debe asumir que un mismo Integration Event puede ser
recibido más de una vez.

La identidad del evento está determinada por:

```text
EventId
```

Dos entregas con el mismo EventId representan el mismo Integration
Event.

El procesamiento repetido no debe reinterpretarse automáticamente
como un nuevo hecho de dominio.

Debe mantenerse:

```text
Same EventId

=

Same Integration Event
```

---

# Versionado

Todo contrato de Integration Event debe poseer:

```text
Version
```

Version representa la versión del contrato público de integración.

No debe confundirse con:

```text
Document.Version
```

ni con:

```text
AggregateVersion
```

Debe mantenerse:

```text
Integration Contract Version

≠

Aggregate Version
```

Los cambios incompatibles de un contrato deben tratarse mediante
evolución explícita del contrato.

El Versioning del Aggregate se encuentra definido en:

```text
DOMAIN-010I-Versioning.md
```

---

# Compatibilidad

La evolución de los Integration Events debe preservar:

- significado del contrato;
- estabilidad semántica;
- trazabilidad histórica;
- compatibilidad con consumidores existentes cuando corresponda;
- separación respecto del modelo interno;
- independencia del mecanismo técnico de transporte.

Un cambio interno de Document no obliga automáticamente a cambiar
un Integration Event.

Debe mantenerse:

```text
Internal Model Evolution

≠

Automatic Public Contract Change
```

---

# Relación con Domain Events

Los Domain Events representan hechos dentro del Aggregate:

```text
DocumentCreated

DocumentPublished

DocumentArchived
```

Los Integration Events representan hechos seleccionados y
transformados para comunicación fuera del Bounded Context.

Conceptualmente:

```text
Domain Event

↓

Integration Mapping

↓

Integration Event
```

solamente cuando exista una definición explícita de dicho mapping.

No todo Domain Event necesita transformarse en Integration Event.

---

# Relación con Consistency Boundary

Los Integration Events permiten comunicar hechos fuera de Document
sin ampliar su Consistency Boundary.

Debe mantenerse:

```text
Document Transaction

↓

Commit

↓

Integration Event

↓

External Reaction
```

Ningún consumidor externo participa dentro de la transacción
interna del Aggregate.

La definición formal del límite pertenece a:

```text
DOMAIN-010J-Consistency-Boundary.md
```

---

# Relación con Event Sourcing

Los Integration Events no forman parte del historial interno
obligatorio de Document.

El historial del Aggregate continúa representándose mediante sus
Domain Events.

Debe mantenerse:

```text
Domain Event History

≠

Integration Event History
```

Un Integration Event puede derivarse de un hecho persistido sin
reemplazar el Domain Event que representa ese hecho dentro del
dominio.

---

# Relación con CQRS

Los Integration Events pueden ser utilizados por consumidores
externos para alimentar:

- Read Models;
- proyecciones distribuidas;
- motores de búsqueda;
- sistemas analíticos;
- otras vistas externas.

Estos consumidores no adquieren autoridad sobre Document.

Debe mantenerse:

```text
Integration Event Consumer

≠

Document Write Authority
```

El lado de escritura continúa bajo responsabilidad del Aggregate.

---

# Seguridad

Los Integration Events nunca deben exponer:

- credenciales;
- secretos;
- tokens;
- claves privadas;
- información técnica de autenticación;
- información sensible innecesaria;
- Content completo sin una necesidad explícitamente definida.

Todo Payload debe aplicar el principio de minimización.

Debe mantenerse:

```text
Published Information

=

Minimum Information Required by Contract
```

La existencia de información dentro de Document no significa que
dicha información deba exponerse externamente.

---

# Principios Arquitectónicos

Los Integration Events de Document siguen:

- Domain-Driven Design (DDD);
- Event-Driven Architecture;
- CQRS;
- Event Sourcing Compatible;
- Clean Architecture;
- Consistency Boundary;
- contratos públicos versionados;
- independencia tecnológica.

La implementación concreta del transporte y persistencia de los
Integration Events pertenece a Infrastructure.

---

# Definición de Éxito

Los **Integration Events** del Aggregate **Document** constituyen
el mecanismo conceptual para publicar hechos confirmados hacia
otros Bounded Contexts y sistemas externos mediante contratos
explícitos, estables y versionados.

El modelo garantiza que:

- Domain Events e Integration Events permanecen separados;
- ningún Domain Event genera automáticamente un Integration Event;
- solamente hechos confirmados pueden exponerse externamente;
- los contratos públicos poseen identidad y versión propias;
- los Payloads contienen únicamente información necesaria;
- Content no se expone automáticamente;
- los consumidores no modifican directamente Document;
- otros Aggregates conservan sus propios Consistency Boundaries;
- la publicación ocurre después de la confirmación de la
  modificación;
- los consumidores deben soportar idempotencia;
- la evolución interna del Aggregate no modifica automáticamente
  contratos públicos;
- Integration Events no reemplazan Domain Events;
- Integration Events no forman parte del estado interno de
  Document;
- la integración mantiene consistencia eventual;
- Infrastructure no determina la semántica del contrato.

De esta forma, `DOMAIN-010K-Integration-Events.md` establece las
reglas de integración del Aggregate **Document** sin inferir
contratos públicos que no hayan sido definidos explícitamente por
el dominio AURA.