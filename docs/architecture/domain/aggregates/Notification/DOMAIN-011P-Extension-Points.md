# DOMAIN-011P — Notification Extension Points

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
- DOMAIN-011F-Permissions.md
- DOMAIN-011G-Repository-Contract.md
- DOMAIN-011H-Examples.md
- DOMAIN-011I-Versioning.md
- DOMAIN-011J-Consistency-Boundary.md
- DOMAIN-011K-Integration-Events.md
- DOMAIN-011L-Read-Model.md
- DOMAIN-011M-Test-Scenarios.md
- DOMAIN-011N-Performance-Rules.md
- DOMAIN-011O-Security-Model.md

---

# Objetivo

Este documento define los Extension Points conceptuales del
Aggregate **Notification**.

Su propósito es establecer las áreas donde el dominio puede
evolucionar en el futuro sin romper:

- identidad;
- Lifecycle;
- State Machine;
- Invariants;
- Consistency Boundary;
- Versioning;
- contratos existentes;
- separación entre dominio e Infrastructure.

Los Extension Points no constituyen funcionalidades existentes.

Representan únicamente lugares controlados de evolución futura.

---

# Principio Fundamental

Debe mantenerse:

```text
Extension Point

≠

Existing Domain Capability
```

y:

```text
Possible Extension

≠

Automatic Domain Decision
```

Ningún concepto descrito como extensión queda incorporado
automáticamente al Aggregate.

Toda incorporación futura requiere definición explícita y
consolidación dentro del modelo de dominio de AURA.

---

# Reglas de Extensión

Toda evolución futura debe respetar:

- Ubiquitous Language;
- Aggregate Pattern;
- una única Aggregate Root;
- identidad estable;
- límites de consistencia explícitos;
- independencia de Infrastructure;
- invariantes existentes;
- contratos públicos existentes;
- compatibilidad de Domain Events;
- compatibilidad de Integration Events cuando corresponda;
- evolución controlada de Read Models.

---

# Límite de Extensibilidad

Una extensión puede incorporarse dentro de Notification solamente
cuando su información y comportamiento necesiten consistencia
inmediata con el Aggregate.

Si un concepto futuro adquiere:

- identidad independiente;
- Lifecycle independiente;
- State Machine independiente;
- Invariants independientes;
- Version independiente;
- necesidad de consistencia propia;

debe evaluarse como:

```text
Separate Aggregate
```

o:

```text
Separate Bounded Context
```

según corresponda.

---

# Extensión de Destinatarios

Notification Management ya reconoce conceptualmente:

```text
destinatarios
```

como una de sus responsabilidades.

La representación concreta de destinatarios puede evolucionar sin
cambiar el principio:

```text
Recipient

≠

Embedded External Aggregate
```

Futuras extensiones pueden definir reglas más específicas para:

- representación de destinatarios;
- múltiples destinatarios;
- agrupaciones;
- criterios de selección;
- destinatarios derivados de políticas;
- referencias externas.

Ninguna de estas capacidades queda definida automáticamente por
este documento.

---

# Extensión de Canales

Notification Management reconoce:

```text
canales
```

como concepto del dominio.

La evolución futura puede incorporar nuevos tipos o reglas de canal
manteniendo:

```text
Notification Channel

≠

Infrastructure Provider
```

Un nuevo proveedor técnico no implica por sí mismo un nuevo concepto
de dominio.

---

# Nuevos Canales

Pueden incorporarse nuevos canales cuando exista una necesidad real
del dominio.

La incorporación debe definir explícitamente:

- significado del canal;
- reglas aplicables;
- relación con Notification;
- impacto sobre Invariants;
- impacto sobre Commands;
- impacto sobre Domain Events;
- impacto sobre Read Models;
- impacto sobre integración cuando corresponda.

El mecanismo técnico que implemente el canal permanece fuera del
Aggregate.

---

# Extensión de Plantillas

Notification Management reconoce:

```text
plantillas
```

como una responsabilidad conceptual.

La versión 1.0 no define una arquitectura interna concreta para
templates.

Futuras extensiones pueden definir:

- identidad de plantilla;
- selección de plantilla;
- variables;
- versiones;
- reglas de aplicabilidad;
- localización;
- representación de contenido.

Antes de incorporarlas deberá determinarse si dichas capacidades:

```text
belong inside Notification
```

o requieren:

```text
Separate Aggregate / Context
```

---

# Extensión del Contenido

El contenido de una Notification puede evolucionar conceptualmente
siempre que se preserve:

```text
Notification Communication

≠

Document Aggregate
```

Si el contenido adquiere identidad, Lifecycle, Versioning o reglas
documentales propias, debe permanecer bajo el Aggregate
correspondiente.

Notification puede continuar utilizando referencias como:

```text
DocumentId
```

cuando corresponda.

---

# Extensión de Delivery Policies

Notification Management reconoce:

```text
entrega
```

como responsabilidad del dominio.

Futuras extensiones pueden introducir políticas de entrega cuando
exista una regla explícita.

Podrían existir conceptos relacionados con:

- condiciones de entrega;
- prioridades;
- restricciones;
- ventanas válidas;
- políticas por contexto;
- reglas de selección de canal.

Estos conceptos no quedan definidos como parte de la versión 1.0.

---

# Extensión de Retry Policies

Notification Management reconoce:

```text
reintentos
```

como responsabilidad.

La versión 1.0 define únicamente:

```text
Failed → Pending
```

mediante:

```text
RetryNotification
```

No define:

- número máximo de reintentos;
- intervalos;
- backoff;
- ventanas temporales;
- prioridad;
- estrategia automática.

Cualquiera de estas reglas podrá incorporarse únicamente mediante
una evolución explícita del dominio.

---

# Extensión del Lifecycle

El Lifecycle versión 1.0 contiene:

```text
Draft

Pending

Delivered

Failed
```

No deben añadirse nuevos estados sin actualización coordinada de:

```text
DOMAIN-011A-Lifecycle.md

DOMAIN-011B-State-Machine.md

DOMAIN-011C-Commands.md

DOMAIN-011D-Domain-Events.md

DOMAIN-011E-Invariants.md

DOMAIN-011H-Examples.md

DOMAIN-011M-Test-Scenarios.md
```

---

# Nuevos Estados

Cualquier futuro estado debe representar una condición real y
distinguible del dominio.

Un nuevo estado no puede introducirse únicamente para representar:

- detalles de Infrastructure;
- estados internos de un proveedor;
- estados de una cola técnica;
- estados de transporte;
- estados de un broker;
- métricas operacionales.

Debe mantenerse:

```text
Domain State

≠

Infrastructure State
```

---

# Archived como Posible Evolución

La versión 1.0 no incluye:

```text
Archived
```

como NotificationStatus.

Una futura incorporación requerirá una necesidad explícita de
dominio y deberá definir:

- significado;
- transición de entrada;
- Commands;
- Domain Events;
- Invariants;
- efecto sobre consultas;
- efecto sobre retención histórica.

No puede incorporarse por analogía con otros Aggregates.

---

# Cancelled como Posible Evolución

La versión 1.0 no incluye:

```text
Cancelled
```

como NotificationStatus.

Una futura capacidad de cancelación deberá determinar:

- desde qué estados puede ocurrir;
- si representa un estado terminal;
- qué Command la expresa;
- qué Domain Event confirma el hecho;
- cómo interactúa con Pending;
- cómo interactúa con delivery ya ejecutada.

Hasta dicha definición:

```text
CancelNotification
```

no constituye un Command oficial.

---

# Read como Posible Evolución

La versión 1.0 mantiene:

```text
Delivered

≠

Read
```

Una futura necesidad de representar:

```text
Read

Opened

Acknowledged
```

debe evaluarse explícitamente.

Antes de incorporarla deberá determinarse si constituye:

- parte del Lifecycle de Notification;
- un hecho independiente;
- una proyección;
- una responsabilidad de otro contexto.

Este documento no decide esa clasificación.

---

# Extensión de Commands

Los Commands oficiales versión 1.0 son:

```text
CreateNotification

QueueNotification

ConfirmNotificationDelivery

ReportNotificationDeliveryFailure

RetryNotification
```

Nuevos Commands pueden incorporarse únicamente si representan una
nueva intención real del dominio.

Debe mantenerse:

```text
New Infrastructure Operation

≠

New Domain Command
```

---

# Reglas para Nuevos Commands

Todo nuevo Command deberá definir:

- intención;
- estado requerido;
- condiciones;
- transición cuando corresponda;
- Invariants afectadas;
- Domain Events resultantes;
- Permissions;
- impacto sobre Version;
- escenarios de prueba.

Un nuevo Command no puede ser un setter encubierto.

---

# Extensión de Domain Events

Los Domain Events oficiales versión 1.0 son:

```text
NotificationCreated

NotificationQueued

NotificationDelivered

NotificationDeliveryFailed

NotificationRetried
```

Pueden incorporarse nuevos Domain Events cuando exista un nuevo
hecho significativo del dominio.

Debe mantenerse:

```text
Domain Event

=

Confirmed Domain Fact
```

Nunca:

```text
Domain Event

=

Technical Message
```

---

# Compatibilidad de Domain Events

La evolución de eventos debe preservar:

- significado histórico;
- EventId;
- NotificationId;
- AggregateVersion;
- trazabilidad;
- compatibilidad de consumidores cuando corresponda.

Un evento histórico existente no debe cambiar de significado para
representar una nueva capacidad.

---

# Extensión de Integration Events

Nuevos contratos de Integration Events pueden incorporarse cuando
exista una necesidad explícita de comunicación fuera del Bounded
Context.

Debe mantenerse:

```text
Domain Event

≠

Mandatory Integration Event
```

La existencia de una nueva capacidad interna no obliga
automáticamente a publicar un nuevo contrato externo.

---

# Versionado de Integration Events

Cuando un contrato público evolucione debe mantener versionado
independiente de:

```text
Notification.Version
```

Debe mantenerse:

```text
Integration Contract Version

≠

Aggregate Version
```

---

# Extensión de Read Models

Los Read Models pueden evolucionar libremente para satisfacer nuevas
necesidades de consulta sin modificar automáticamente el Aggregate.

Pueden incorporarse:

- nuevas vistas;
- nuevos filtros;
- nuevas búsquedas;
- nuevas proyecciones;
- vistas históricas;
- vistas analíticas;
- vistas compuestas.

Debe mantenerse:

```text
New Query Requirement

≠

New Aggregate State
```

---

# Extensión de Proyecciones

Nuevas proyecciones pueden consumir Domain Events o Integration
Events según su límite de consumo.

Una proyección nueva:

- no amplía el Consistency Boundary;
- no obtiene autoridad de escritura;
- no crea automáticamente nuevos Commands;
- no modifica Lifecycle.

---

# Extensión de Policies

Notification puede evolucionar mediante Policies cuando una regla
necesite encapsular una decisión de dominio sin convertirse en una
nueva Aggregate Root.

Una Policy futura debe:

- expresar reglas del dominio;
- permanecer independiente de Infrastructure;
- respetar Invariants;
- no almacenar Aggregates externos;
- no modificar directamente otros Aggregates.

La existencia de este Extension Point no define una Policy concreta.

---

# Extensión mediante Value Objects

Nuevos Value Objects pueden incorporarse cuando representen
conceptos del dominio:

- sin identidad propia;
- definidos por sus valores;
- inmutables;
- pertenecientes completamente a Notification.

La clasificación debe decidirse explícitamente para cada concepto.

Este documento no clasifica automáticamente como Value Objects:

- Recipient;
- Channel;
- Template;
- Content;
- Delivery Policy;
- Retry Policy.

---

# Extensión mediante Internal Entities

Una Internal Entity puede incorporarse únicamente cuando:

- pertenece completamente al Aggregate;
- necesita identidad local;
- su consistencia debe protegerse junto con Notification;
- no requiere Lifecycle independiente fuera del Aggregate.

La existencia de un concepto complejo no implica automáticamente
que sea una Internal Entity.

---

# Promoción a Aggregate

Si un concepto inicialmente interno adquiere:

```text
Independent Identity

+

Independent Lifecycle

+

Independent Invariants

+

Independent Consistency Requirements
```

debe evaluarse su promoción hacia un Aggregate independiente.

La evolución no debe mantener artificialmente conceptos autónomos
dentro de Notification.

---

# Extensión de Repository

El Repository Contract puede evolucionar únicamente para soportar
necesidades propias de persistencia del Aggregate.

No debe transformarse en:

- Query Service;
- Reporting Service;
- Analytics Repository;
- Multi-Aggregate Repository;
- Integration Gateway.

Debe mantenerse:

```text
NotificationRepository

=

Notification Aggregate Persistence Contract
```

---

# Extensión de Persistencia

Cambiar:

- base de datos;
- ORM;
- Event Store;
- mecanismo de serialización;
- estrategia física de almacenamiento;

no constituye una evolución del dominio por sí mismo.

Debe mantenerse:

```text
Persistence Technology Change

≠

Domain Extension
```

---

# Extensión de Seguridad

Nuevas políticas de:

- Authentication;
- Authorization;
- RBAC;
- ABAC;
- cifrado;
- gestión de secretos;

pueden evolucionar externamente sin modificar Notification mientras
no introduzcan nuevas reglas del dominio.

Debe mantenerse:

```text
Security Mechanism Evolution

≠

Automatic Aggregate Evolution
```

---

# Extensión de Permissions

Nuevos Roles o políticas externas pueden habilitar o restringir
Commands existentes.

Esto no introduce automáticamente:

- nuevos estados;
- nuevos Commands;
- nuevos Domain Events;
- nuevas Invariants.

---

# Extensión de Audit

Audit puede incorporar nuevas necesidades de trazabilidad sin
expandir Notification.

Notification continúa produciendo hechos propios.

Audit continúa administrando su propia representación.

Debe mantenerse:

```text
Audit Evolution

≠

Notification Aggregate Expansion
```

---

# Extensión de Analytics

Nuevos indicadores o métricas pueden construirse desde:

- Domain Events;
- Integration Events;
- Read Models;
- proyecciones.

No deben incorporarse al Aggregate únicamente para facilitar
reporting.

Debe mantenerse:

```text
Analytics Requirement

≠

Aggregate State Requirement
```

---

# Extensión FIWARE

Nuevas integraciones con FIWARE deben permanecer fuera del
Aggregate.

Pueden evolucionar:

- modelos de contexto;
- adapters;
- contratos de integración;
- mappings;
- proyecciones;

sin introducir dependencias FIWARE dentro de Notification.

Debe mantenerse:

```text
FIWARE Evolution

≠

Notification Domain Dependency
```

---

# Extensión Municipal

La integración con nuevos sistemas municipales puede incorporar
nuevos contratos o adapters.

Esto no cambia por sí mismo:

- Lifecycle;
- Commands;
- Domain Events;
- Invariants;
- Consistency Boundary.

---

# Extensión de Proveedores

La incorporación de un nuevo proveedor de:

- email;
- SMS;
- push;
- mensajería;
- transporte;

pertenece a Infrastructure.

Debe mantenerse:

```text
New Provider

≠

New Notification Domain Model
```

salvo que aparezca una nueva regla real del dominio que requiera
evolución explícita.

---

# Extensión de Performance

Nuevas técnicas de:

- cache;
- batching;
- partitioning;
- sharding;
- asynchronous processing;
- indexing;
- horizontal scaling;

pueden incorporarse sin cambiar Notification mientras preserven sus
contratos e Invariants.

Debe mantenerse:

```text
Performance Strategy

≠

Domain Semantics
```

---

# Extensión para Procesamiento Masivo

Un futuro proceso que coordine múltiples Notifications no convierte
la colección en un único Aggregate.

Debe mantenerse:

```text
Bulk Process

    ├── Notification A
    ├── Notification B
    └── Notification C
```

donde cada Notification conserva:

- NotificationId;
- Version;
- Lifecycle;
- State Machine;
- Consistency Boundary.

---

# Nuevos Aggregates Relacionados

La evolución futura puede introducir nuevos Aggregates relacionados
con comunicación siempre que exista una necesidad real de identidad
y consistencia independiente.

La incorporación de un nuevo Aggregate no cambia automáticamente el
límite de Notification.

La relación deberá mantenerse mediante:

```text
AggregateId

Domain Events

Integration Events

Domain Contracts
```

según corresponda.

---

# Compatibilidad hacia Atrás

Las extensiones deben preservar, cuando corresponda:

- NotificationId;
- significado de estados existentes;
- Commands existentes;
- Domain Events históricos;
- contratos de Integration Events publicados;
- Repository Contract;
- consumidores de Read Models.

Una nueva capacidad no debe reinterpretar silenciosamente un hecho
histórico.

---

# Migración Conceptual

Cuando una extensión requiera modificar reglas existentes deberá
definirse explícitamente:

- impacto en Notifications existentes;
- compatibilidad de estados;
- compatibilidad de eventos;
- compatibilidad de Versioning;
- impacto sobre Read Models;
- impacto sobre Integration Events;
- impacto sobre Test Scenarios.

El mecanismo técnico de migración pertenece a Infrastructure.

---

# ADR

Una extensión que modifique una decisión arquitectónica consolidada
debe documentarse mediante el ADR correspondiente.

Especialmente cuando afecte:

- Consistency Boundary;
- división de Aggregates;
- estrategia de integración;
- modelo de persistencia;
- Event Sourcing;
- contratos públicos.

El ADR documenta la decisión arquitectónica.

Los artefactos DOMAIN documentan las reglas resultantes del dominio.

---

# Restricciones

Ninguna extensión puede:

- modificar NotificationId;
- eliminar Invariants existentes sin decisión explícita;
- evitar State Machine;
- permitir setters públicos;
- introducir Aggregates externos dentro de Notification;
- crear transacciones multi-Aggregate como requisito del dominio;
- trasladar Authentication al Aggregate;
- almacenar credenciales;
- introducir dependencias de Infrastructure;
- convertir Read Models en autoridad de escritura;
- modificar hechos históricos;
- convertir métricas técnicas en estados sin una regla real;
- introducir un estado únicamente por analogía con otro Aggregate;
- convertir un proveedor técnico en concepto de dominio
  automáticamente.

---

# Reglas Fundamentales

Las siguientes reglas son obligatorias para toda extensión futura:

1. Notification continúa siendo la única Aggregate Root.
2. NotificationId permanece inmutable.
3. El Consistency Boundary solamente cambia mediante decisión
   explícita.
4. No se incorporan Aggregates externos como estado interno.
5. Nuevos estados requieren evolución coordinada del Lifecycle y
   State Machine.
6. Nuevos Commands requieren una intención real del dominio.
7. Nuevos Domain Events requieren un hecho real del dominio.
8. Domain Events existentes no cambian retroactivamente de
   significado.
9. Nuevos Integration Events requieren contrato explícito.
10. Domain Event no implica Integration Event automático.
11. Nuevos Value Objects deben ser definidos explícitamente.
12. Nuevas Internal Entities deben pertenecer completamente al
    Consistency Boundary.
13. Conceptos con consistencia independiente deben evaluarse como
    Aggregates.
14. Nuevos proveedores no constituyen automáticamente extensiones
    del dominio.
15. Cambios de persistencia no constituyen automáticamente
    extensiones del dominio.
16. Nuevos Read Models no modifican el Aggregate.
17. Nuevas Queries no implican nuevo estado del Write Model.
18. Nuevas políticas de seguridad no evitan Invariants.
19. Nuevas Permissions no crean automáticamente nuevo
    comportamiento.
20. Audit puede evolucionar sin expandir Notification.
21. Analytics puede evolucionar mediante proyecciones.
22. FIWARE permanece fuera del Aggregate.
23. Los sistemas municipales permanecen fuera del Aggregate.
24. Performance puede evolucionar sin cambiar la semántica.
25. El procesamiento masivo conserva Aggregates independientes.
26. Las extensiones deben preservar trazabilidad.
27. Las extensiones deben mantener Versioning coherente.
28. Las extensiones deben mantener compatibilidad cuando
    corresponda.
29. Cambios arquitectónicos consolidados requieren documentación
    mediante ADR.
30. Toda nueva decisión de dominio debe quedar explícitamente
    consolidada antes de incorporarse.

---

# Compatibilidad Arquitectónica

Los Extension Points mantienen compatibilidad con:

- Domain-Driven Design;
- Aggregate Pattern;
- Clean Architecture;
- Hexagonal Architecture;
- SOLID;
- Open/Closed Principle;
- CQRS;
- Event-Driven Architecture;
- Event Sourcing Compatible;
- Optimistic Concurrency Control;
- High Cohesion;
- Low Coupling.

La extensibilidad no introduce dependencia con ninguna tecnología
concreta.

---

# Definición de Éxito

Los Extension Points del Aggregate **Notification** permiten que el
dominio evolucione de forma controlada sin debilitar las decisiones
consolidadas de AURA Core.

La evolución puede considerar conceptualmente:

```text
Recipients

Channels

Templates

Communication Content

Delivery Policies

Retry Policies

Lifecycle

Commands

Domain Events

Integration Events

Read Models

Value Objects

Internal Entities

Domain Policies
```

sin que ninguno de estos conceptos se incorpore automáticamente por
el solo hecho de aparecer como punto de extensión.

El modelo garantiza que:

- Notification permanece como única Aggregate Root;
- NotificationId permanece inmutable;
- el Consistency Boundary permanece explícito;
- los Aggregates externos continúan separados;
- nuevos estados requieren definición formal;
- Archived no se incorpora por analogía;
- Cancelled no se incorpora sin decisión explícita;
- Read, Opened o Acknowledged no se incorporan automáticamente;
- nuevos Commands representan intenciones reales del dominio;
- nuevos Domain Events representan hechos consumados;
- los contratos públicos evolucionan de forma controlada;
- los Read Models pueden crecer sin ampliar el Write Model;
- Value Objects e Internal Entities requieren clasificación
  explícita;
- conceptos autónomos deben evaluarse como Aggregates separados;
- cambios tecnológicos permanecen fuera del dominio;
- nuevos proveedores no alteran automáticamente Notification;
- FIWARE y sistemas municipales permanecen desacoplados;
- Performance y Security pueden evolucionar sin modificar la
  semántica del Aggregate;
- los hechos históricos conservan su significado;
- las extensiones arquitectónicas relevantes se documentan mediante
  ADR;
- ninguna extensión se consolida sin una decisión explícita del
  dominio.

De esta forma, `DOMAIN-011P-Extension-Points.md` establece los
puntos oficiales de evolución controlada del Aggregate
**Notification** conforme al patrón consolidado de AURA Core.