# DOMAIN-010L — Document Read Model

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
- DOMAIN-010K-Integration-Events.md
- CORE-005-Domain-Events.md

---

# Objetivo

Este documento define el modelo oficial de lectura (Read
Model) del Aggregate **Document**.

Los Read Models representan vistas optimizadas para consulta y
visualización. No contienen lógica de negocio y no forman parte
del Aggregate.

Su propósito es proporcionar consultas rápidas y escalables sin
afectar la consistencia del lado de escritura.

---

# Principios

Los Read Models siguen los siguientes principios:

- son derivados del dominio;
- son reconstruibles;
- son de solo lectura;
- están desacoplados del Aggregate;
- pueden desnormalizar información;
- pueden existir múltiples proyecciones para un mismo
  Aggregate.

Ningún Read Model puede:

- modificar Document;
- ejecutar Commands;
- cambiar DocumentStatus;
- modificar Content;
- incrementar Version;
- reemplazar las Invariants;
- convertirse en fuente de verdad de escritura.

---

# Arquitectura

```text
                Commands

                    │

                    ▼

            Document Aggregate

                    │

             Domain Events

                    │

                    ▼

             Projection Engine

                    │

      ┌─────────────┼─────────────┐

      ▼             ▼             ▼

 Document View   Status View   History View
```

El mecanismo concreto utilizado para materializar las
proyecciones pertenece a Infrastructure.

---

# Fuente de Verdad

La única fuente oficial de verdad de escritura es:

```text
Document Aggregate
```

y, cuando corresponda al modelo de persistencia adoptado, su
historial de:

```text
Domain Events
```

Los Read Models:

- no constituyen fuente de verdad;
- pueden eliminarse;
- pueden reconstruirse;
- no poseen autoridad para modificar Document.

Debe mantenerse:

```text
Read Model

≠

Document Aggregate
```

---

# Proyecciones Oficiales

El Bounded Context Document Management mantiene las siguientes
proyecciones conceptuales:

```text
DocumentSummary

DocumentDetail

DocumentStatus

DocumentHistory
```

Estas proyecciones utilizan exclusivamente información derivada
de hechos y estado ya definidos por Document.

No introducen nuevos estados, Commands, Domain Events,
Invariants ni responsabilidades dentro del Aggregate.

---

# DocumentSummary

Vista utilizada para listados y consultas resumidas.

Campos conceptuales:

```text
DocumentId

DocumentType

DocumentStatus

Version

CreatedAt

UpdatedAt
```

Uso:

- listados;
- búsquedas;
- selección de Documents;
- navegación documental.

DocumentSummary no contiene autoridad para modificar ninguno de
estos valores.

---

# DocumentDetail

Vista utilizada para representar información detallada de un
Document.

Campos conceptuales:

```text
DocumentId

DocumentType

Content

DocumentStatus

Version

CreatedAt

UpdatedAt
```

Uso:

- consulta detallada;
- visualización documental;
- representación del estado actual del Document.

La presencia de Content en esta proyección no implica que deba
exponerse a todo consumidor.

Las reglas de acceso y seguridad permanecen separadas del Read
Model.

---

# DocumentStatus

Vista especializada en el estado operativo del Document.

Campos conceptuales:

```text
DocumentId

DocumentType

DocumentStatus

Version

UpdatedAt
```

DocumentStatus solamente puede representar los estados oficiales:

```text
Draft

Published

Archived
```

Uso:

- consultas por estado;
- seguimiento del Lifecycle;
- paneles operativos;
- filtros.

Esta proyección no constituye la State Machine.

Debe mantenerse:

```text
DocumentStatus Read Model

≠

State Machine Authority
```

---

# DocumentHistory

Vista utilizada para representar la evolución histórica conocida
del Document a partir de sus Domain Events.

Los hechos oficiales de la versión 1.0 son:

```text
DocumentCreated

DocumentPublished

DocumentArchived
```

Campos conceptuales:

```text
DocumentId

EventType

AggregateVersion

OccurredAt
```

Cuando corresponda:

```text
CorrelationId

CausationId
```

Uso:

- trazabilidad;
- consulta histórica;
- visualización de evolución;
- soporte a auditoría mediante contratos separados.

DocumentHistory no modifica ni reinterpreta hechos históricos.

---

# Actualización

Los Read Models se actualizan mediante Domain Events confirmados.

```text
DocumentCreated

↓

Projection
```

```text
DocumentPublished

↓

Projection
```

```text
DocumentArchived

↓

Projection
```

Cada evento actualiza únicamente las proyecciones afectadas.

Debe preservarse:

```text
AggregateVersion
```

como referencia del orden lógico de evolución del Aggregate.

Una operación rechazada no produce el Domain Event de éxito y,
por lo tanto, no genera una actualización derivada de dicho hecho.

---

# Reconstrucción

Todas las proyecciones pueden regenerarse desde la información
oficial disponible del dominio.

Conceptualmente:

```text
Replay

↓

Domain Events

↓

Projection Engine

↓

Read Models
```

La reconstrucción:

- no ejecuta Commands;
- no modifica Document;
- no incrementa Version;
- no produce nuevos Domain Events;
- no altera hechos históricos.

Debe mantenerse:

```text
Projection Rebuild

≠

Domain Modification
```

---

# Consistencia

Los Read Models utilizan:

```text
Eventually Consistent
```

Puede existir una diferencia temporal entre:

```text
Command

↓

Document Modification

↓

Commit

↓

Domain Event

↓

Projection Update
```

Durante ese intervalo, el Aggregate continúa siendo la autoridad
sobre el estado confirmado del dominio.

La consistencia eventual del Read Model no modifica las
Invariants de Document.

---

# Consultas

Los Read Models permiten consultas conceptuales como:

- Documents por DocumentId;
- Documents por DocumentType;
- Documents en Draft;
- Documents Published;
- Documents Archived;
- detalle de un Document;
- estado actual de un Document;
- historial de evolución de un Document.

Estas consultas no modifican el Aggregate.

Las consultas complejas deben resolverse mediante Read Models y no
mediante expansión del Consistency Boundary.

---

# Persistencia

Las proyecciones pueden almacenarse mediante mecanismos
optimizados para lectura.

La elección concreta pertenece a Infrastructure.

El dominio no exige:

```text
PostgreSQL

MongoDB

Elasticsearch

Redis

OpenSearch
```

ni ningún otro mecanismo concreto.

La tecnología elegida no modifica el significado conceptual de
las proyecciones.

---

# Rendimiento

Las proyecciones pueden optimizarse para:

- lectura;
- paginación;
- filtros;
- búsqueda;
- ordenamiento;
- navegación;
- consulta histórica.

Estas optimizaciones no pueden introducir lógica de negocio.

Debe mantenerse:

```text
Read Optimization

≠

Domain Rule
```

El Aggregate no debe expandirse para satisfacer necesidades
exclusivas de consulta.

---

# Seguridad

Cada Read Model debe exponer únicamente la información autorizada
para su consumidor.

Una proyección puede:

- omitir información;
- limitar atributos;
- aplicar políticas de acceso;
- evitar exposición innecesaria de Content.

La autorización pertenece a las capas responsables.

El Read Model no modifica las Permissions del Aggregate.

Debe mantenerse:

```text
Data Present in Document

≠

Data Automatically Exposed
```

---

# Compatibilidad con CQRS

Este documento representa el lado de lectura del patrón CQRS.

```text
Write Side

Document Aggregate

↓

Domain Events

↓

Read Side

Document Read Models
```

Ambos lados permanecen separados.

El lado de lectura:

- no ejecuta Commands;
- no protege Invariants;
- no controla la State Machine;
- no modifica Version;
- no sustituye al Aggregate.

---

# Compatibilidad con Event Sourcing

Los Read Models no representan por sí mismos la historia oficial
del Aggregate.

Cuando se utiliza Event Sourcing, la historia permanece en los
Domain Events.

Las proyecciones son representaciones materializadas derivadas de
esa historia.

Conceptualmente:

```text
DocumentCreated

↓

DocumentPublished

↓

DocumentArchived

↓

Projection

↓

Read Model
```

La eliminación de una proyección no elimina los hechos del
dominio.

---

# Evolución

Nuevas proyecciones pueden incorporarse sin modificar el
Aggregate, siempre que:

- utilicen hechos ya disponibles mediante contratos válidos;
- no introduzcan lógica de negocio;
- no modifiquen Document;
- no alteren el Lifecycle;
- no alteren la State Machine;
- no creen nuevas Invariants;
- no amplíen el Consistency Boundary;
- mantengan independencia del lado de escritura;
- respeten el lenguaje ubicuo.

Una necesidad de consulta no constituye por sí misma una razón
para modificar el Aggregate.

Debe mantenerse:

```text
New Query Requirement

≠

New Aggregate Responsibility
```

---

# Principios Arquitectónicos

Los Read Models siguen:

- Domain-Driven Design (DDD);
- CQRS;
- Event Sourcing Compatible;
- Event-Driven Architecture;
- Clean Architecture;
- Single Responsibility Principle.

Los Read Models permanecen desacoplados de la implementación
interna de Document.

---

# Definición de Éxito

Los Read Models del Aggregate **Document** proporcionan vistas
especializadas, reconstruibles y optimizadas para consulta sin
comprometer la consistencia del dominio ni acoplar el lado de
lectura al Aggregate de escritura.

Las proyecciones oficiales son:

```text
DocumentSummary

DocumentDetail

DocumentStatus

DocumentHistory
```

El modelo garantiza que:

- Document permanece como fuente de verdad de escritura;
- los Read Models son derivados;
- los Read Models son de solo lectura;
- las proyecciones pueden reconstruirse;
- las proyecciones utilizan consistencia eventual;
- los Domain Events actualizan las vistas afectadas;
- AggregateVersion preserva el orden lógico de evolución;
- DocumentStatus solamente representa estados oficiales;
- DocumentHistory preserva hechos históricos;
- Content no se expone automáticamente;
- las consultas no modifican el Aggregate;
- las optimizaciones de lectura no introducen reglas de dominio;
- CQRS mantiene separados los lados de escritura y lectura;
- Event Sourcing permanece compatible;
- nuevas necesidades de consulta no amplían automáticamente el
  Consistency Boundary;
- Infrastructure no determina la semántica del Read Model.

De esta forma, `DOMAIN-010L-Read-Model.md` establece el modelo
oficial de lectura del Aggregate **Document** conforme al patrón
consolidado de AURA Core.