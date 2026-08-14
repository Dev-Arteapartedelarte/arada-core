# DOMAIN-010P — Document Extension Points

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
- DOMAIN-010A-Lifecycle.md
- DOMAIN-010B-State-Machine.md
- DOMAIN-010C-Commands.md
- DOMAIN-010D-Domain-Events.md
- DOMAIN-010E-Invariants.md
- DOMAIN-010F-Permissions.md
- DOMAIN-010G-Repository-Contract.md
- DOMAIN-010I-Versioning.md
- DOMAIN-010J-Consistency-Boundary.md
- DOMAIN-010K-Integration-Events.md
- DOMAIN-010L-Read-Model.md
- DOMAIN-010O-Security-Model.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Definir los puntos oficiales de extensión del Aggregate
**Document** sin alterar las decisiones fundamentales ya
establecidas para su versión 1.0.

Los Extension Points permiten evolucionar el dominio de manera
controlada manteniendo:

- identidad;
- Invariants;
- Lifecycle;
- State Machine;
- Versioning;
- Consistency Boundary;
- separación entre Aggregates;
- independencia tecnológica.

Una extensión no constituye autorización para modificar
implícitamente el modelo existente.

Toda nueva capacidad debe incorporarse mediante una decisión
explícita de dominio y actualizar los contratos afectados.

---

# Principios

Las extensiones de Document deben cumplir:

- Open/Closed Principle;
- evolución explícita;
- compatibilidad controlada;
- preservación de Invariants;
- preservación del Ubiquitous Language;
- separación entre dominio e Infrastructure;
- separación entre Aggregates;
- ausencia de estados implícitos;
- ausencia de Commands implícitos;
- ausencia de Domain Events implícitos;
- ausencia de contratos externos inferidos automáticamente.

Debe mantenerse:

```text
Extension

≠

Implicit Domain Change
```

y:

```text
New Requirement

≠

Automatic Aggregate Responsibility
```

---

# Filosofía

Document debe permitir evolución sin modificar innecesariamente su
núcleo.

La versión 1.0 define como base estable:

```text
DocumentId

DocumentType

Content

DocumentStatus

Version
```

junto con el Lifecycle:

```text
No Document → Draft

Draft → Published

Published → Archived
```

y los Commands:

```text
CreateDocument

PublishDocument

ArchiveDocument
```

con sus Domain Events:

```text
DocumentCreated

DocumentPublished

DocumentArchived
```

Toda extensión futura debe partir de esta definición y no
reinterpretarla retroactivamente.

---

# Punto de Extensión 1 — Nuevos Commands

Pueden incorporarse nuevos Commands cuando aparezca una nueva
intención explícita de negocio perteneciente al Aggregate
Document.

Un nuevo Command debe:

- representar una intención del dominio;
- utilizar Ubiquitous Language;
- pertenecer a Document;
- ser ejecutado mediante la Aggregate Root;
- mantener DocumentId;
- respetar Invariants;
- respetar Lifecycle;
- respetar State Machine;
- respetar Versioning;
- respetar Consistency Boundary;
- definir su comportamiento de rechazo;
- definir los Domain Events correspondientes cuando exista un
  hecho relevante.

Un nuevo Command no puede incorporarse únicamente para:

- facilitar una API;
- reproducir un setter;
- satisfacer una necesidad de UI;
- resolver una consulta;
- adaptar una tecnología;
- modificar directamente un atributo.

La incorporación de un nuevo Command requiere evolución explícita
de:

```text
DOMAIN-010C-Commands.md
```

y de los demás contratos afectados.

---

# Punto de Extensión 2 — Nuevos Domain Events

Pueden incorporarse nuevos Domain Events cuando exista un nuevo
hecho relevante ocurrido dentro de Document.

Un nuevo Domain Event debe:

- representar un hecho consumado;
- pertenecer al Aggregate;
- utilizar Ubiquitous Language;
- ser inmutable;
- mantener DocumentId;
- mantener AggregateVersion coherente;
- preservar causalidad y trazabilidad conforme al modelo de
  eventos;
- producirse únicamente después de comportamiento válido.

No debe incorporarse un Domain Event únicamente por necesidades
de:

- persistencia;
- mensajería;
- UI;
- logging;
- transporte;
- Infrastructure.

Debe mantenerse:

```text
New Domain Fact

↓

New Domain Event
```

y no:

```text
New Technical Need

↓

New Domain Event
```

La definición formal deberá evolucionar:

```text
DOMAIN-010D-Domain-Events.md
```

---

# Punto de Extensión 3 — Nuevos Integration Events

Pueden incorporarse nuevos Integration Events cuando un hecho de
Document necesite ser expuesto explícitamente fuera del Bounded
Context.

Un Integration Event debe:

- derivar de un hecho confirmado;
- poseer contrato explícito;
- poseer identidad propia;
- poseer versión de contrato;
- minimizar su Payload;
- mantener independencia respecto de la estructura interna de
  Document;
- preservar seguridad y privacidad;
- evitar acceso directo al Aggregate.

No todo Domain Event debe transformarse en Integration Event.

Debe mantenerse:

```text
Domain Event

≠

Mandatory Integration Event
```

La incorporación de nuevos contratos debe definirse en:

```text
DOMAIN-010K-Integration-Events.md
```

---

# Punto de Extensión 4 — Nuevos Read Models

Pueden incorporarse nuevos Read Models para satisfacer nuevas
necesidades de consulta.

Una nueva proyección puede:

- combinar información derivada;
- desnormalizar datos;
- optimizar búsquedas;
- optimizar filtros;
- representar nuevas vistas;
- proyectar información histórica.

Una nueva proyección no puede:

- modificar Document;
- ejecutar Commands;
- controlar Lifecycle;
- controlar State Machine;
- crear Invariants;
- modificar Version;
- ampliar Consistency Boundary.

Debe mantenerse:

```text
New Query

↓

New Read Model
```

cuando corresponda, y no:

```text
New Query

↓

Expand Aggregate
```

La definición de nuevos Read Models debe incorporarse en:

```text
DOMAIN-010L-Read-Model.md
```

---

# Punto de Extensión 5 — Nuevos Value Objects

Document puede incorporar nuevos Value Objects cuando un concepto
del dominio:

- carezca de identidad independiente;
- sea definido por sus valores;
- requiera validación propia;
- pertenezca al Consistency Boundary de Document;
- pueda representarse como concepto inmutable.

Los Value Objects ya identificados conceptualmente incluyen:

```text
DocumentType

DocumentStatus
```

La representación de Content no debe clasificarse automáticamente
como Value Object sin una decisión explícita del modelo.

Un nuevo Value Object no puede:

- adquirir Lifecycle independiente implícitamente;
- modificar otros Aggregates;
- contener dependencias de Infrastructure;
- romper Invariants existentes.

Si un concepto requiere identidad, Lifecycle y consistencia
independiente, debe evaluarse conforme a las reglas de diseño de
Aggregates de AURA.

---

# Punto de Extensión 6 — Nuevas Políticas

Pueden incorporarse nuevas Domain Policies cuando una regla:

- pertenezca al dominio;
- no corresponda naturalmente a un único Value Object;
- no requiera convertir otro Aggregate en parte de Document;
- preserve el Consistency Boundary;
- permita expresar reglas explícitas mediante Ubiquitous Language.

Una Domain Policy no puede utilizarse para:

- ocultar una dependencia de Infrastructure;
- modificar directamente otros Aggregates;
- evitar State Machine;
- evitar Invariants;
- introducir transacciones distribuidas dentro de Document.

Las nuevas políticas deben integrarse sin reducir la autoridad de
la Aggregate Root sobre la consistencia de Document.

---

# Punto de Extensión 7 — Nuevas Integraciones

Document puede participar en nuevas integraciones con otros
Bounded Contexts o sistemas externos.

Toda nueva integración debe realizarse mediante:

- contratos explícitos;
- Integration Events cuando corresponda;
- Application Services;
- mecanismos externos compatibles con los límites definidos.

Una integración no puede:

- acceder directamente al estado interno del Aggregate;
- modificar DocumentStatus directamente;
- modificar Content directamente;
- modificar Version directamente;
- evitar Commands;
- evitar Permissions;
- evitar Invariants;
- introducir tecnología externa dentro del dominio.

Debe mantenerse:

```text
New Integration

≠

New Aggregate Dependency
```

---

# Punto de Extensión 8 — Nuevos Bounded Contexts

Cuando una capacidad futura requiera:

- identidad independiente;
- Lifecycle propio;
- reglas propias;
- Invariants propias;
- autoridad de escritura propia;
- consistencia independiente;

debe evaluarse como responsabilidad de un Aggregate o Bounded
Context separado.

Document no debe crecer absorbiendo procesos independientes.

Debe mantenerse:

```text
Independent Lifecycle

+

Independent Consistency

↓

Evaluate Separate Aggregate or Bounded Context
```

La mera relación con Document no convierte un concepto externo en
entidad interna de Document.

---

# Punto de Extensión 9 — Automatización

Pueden incorporarse procesos automatizados que reaccionen a hechos
de Document.

Conceptualmente:

```text
Domain Event

↓

External Process

↓

Authorized Command
```

cuando corresponda.

La automatización no puede modificar directamente el Aggregate.

Todo comportamiento de escritura debe continuar ingresando mediante
Commands válidos y respetando:

- Permissions;
- Lifecycle;
- State Machine;
- Invariants;
- Versioning.

Una automatización no constituye una excepción a las reglas del
dominio.

---

# Punto de Extensión 10 — IA y Automatización Inteligente

Sistemas de IA pueden participar como consumidores o asistentes
externos al Aggregate.

Pueden conceptualmente:

- analizar información autorizada;
- asistir procesos documentales;
- producir recomendaciones;
- apoyar clasificación;
- alimentar procesos externos;
- proponer intenciones que posteriormente puedan convertirse en
  Commands autorizados.

Un sistema de IA no puede:

- modificar directamente Document;
- modificar DocumentId;
- modificar DocumentStatus directamente;
- modificar Content evitando la Aggregate Root;
- incrementar Version;
- omitir Permissions;
- omitir Invariants;
- crear nuevos estados implícitamente;
- crear nuevos Commands implícitamente.

Debe mantenerse:

```text
AI Recommendation

≠

Confirmed Domain Fact
```

y:

```text
AI Decision

≠

Aggregate Authority
```

Toda acción que produzca una modificación del dominio debe seguir
los mismos contratos aplicables a cualquier otra intención.

---

# Restricciones

Ningún Extension Point puede:

- modificar retroactivamente DocumentId;
- romper Invariants existentes;
- introducir estados implícitos;
- introducir transiciones implícitas;
- modificar DocumentStatus directamente;
- evitar la Aggregate Root;
- modificar Version arbitrariamente;
- incorporar Aggregates externos dentro de Document;
- ampliar implícitamente el Consistency Boundary;
- crear transacciones distribuidas dentro del Aggregate;
- introducir dependencias con Infrastructure;
- acoplar Document a bases de datos;
- acoplar Document a frameworks;
- acoplar Document a FIWARE;
- acoplar Document a mecanismos de mensajería;
- almacenar secretos o credenciales;
- convertir Integration Events en Domain Events;
- convertir Read Models en fuente de verdad de escritura;
- modificar hechos históricos ya ocurridos.

---

# Compatibilidad con CQRS

Las extensiones deben preservar la separación:

```text
Write Side

↓

Document Aggregate
```

y:

```text
Read Side

↓

Document Read Models
```

Nuevas necesidades de lectura deben resolverse preferentemente
mediante nuevas proyecciones cuando no representen nueva
responsabilidad de escritura.

Ningún Read Model puede adquirir autoridad de escritura mediante
una extensión.

---

# Compatibilidad con Event Sourcing

Las extensiones deben preservar la inmutabilidad de los hechos
históricos.

Los Domain Events existentes:

```text
DocumentCreated

DocumentPublished

DocumentArchived
```

representan hechos ya ocurridos y no deben reinterpretarse
retroactivamente.

Nuevos hechos futuros deben representarse mediante nuevos Domain
Events cuando correspondan.

Debe mantenerse:

```text
Historical Event

=

Immutable Historical Fact
```

La evolución del modelo no permite reescribir el pasado del
Aggregate.

---

# Estrategia de Evolución

La evolución de Document debe realizarse de forma explícita y
controlada.

Ante una nueva necesidad debe evaluarse:

```text
New Requirement
      │
      ▼
Belongs to Document?
      │
      ├── No ──► External Aggregate / Bounded Context
      │
      └── Yes
             │
             ▼
      Which Contract Changes?
             │
             ├── Command
             ├── Domain Event
             ├── Invariant
             ├── Permission
             ├── Repository Contract
             ├── Versioning
             ├── Integration Event
             ├── Read Model
             └── Security Model
```

La evolución debe actualizar todos los artefactos conceptuales
afectados.

No deben existir decisiones implícitas distribuidas entre
implementaciones.

---

# Principios Arquitectónicos

Los Extension Points de Document mantienen compatibilidad con:

- Domain-Driven Design;
- Aggregate Pattern;
- Open/Closed Principle;
- Clean Architecture;
- Hexagonal Architecture;
- CQRS;
- Event-Driven Architecture;
- Event Sourcing Compatible;
- Optimistic Concurrency;
- High Cohesion;
- Low Coupling;
- evolución controlada.

Las extensiones pertenecen al modelo conceptual y no dependen de
tecnologías concretas.

---

# Definición de Éxito

Los Extension Points del Aggregate **Document** permiten que el
dominio evolucione sin perder las decisiones fundamentales
establecidas en la versión 1.0.

El modelo permite extender:

```text
Commands

Domain Events

Integration Events

Read Models

Value Objects

Domain Policies

Integrations

Bounded Contexts

Automation

AI-assisted processes
```

siempre que dichas extensiones:

- pertenezcan explícitamente al dominio correspondiente;
- preserven DocumentId;
- preserven Invariants;
- preserven Lifecycle;
- preserven State Machine;
- preserven Versioning;
- preserven Consistency Boundary;
- mantengan otros Aggregates fuera de Document;
- no introduzcan dependencias con Infrastructure;
- no creen contratos implícitos;
- no reescriban hechos históricos;
- mantengan CQRS y Event Sourcing compatibles;
- mantengan evolución explícita y controlada.

De esta forma, `DOMAIN-010P-Extension-Points.md` establece los
puntos oficiales de extensión del Aggregate **Document** conforme
al patrón consolidado de AURA Core.