# DOMAIN-008P — Participation Extension Points

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Participation Management

Aggregate:
Participation

Documentos relacionados:

- DOMAIN-008-Aggregate.md
- DOMAIN-008C-Commands.md
- DOMAIN-008D-Domain-Events.md
- DOMAIN-008K-Integration-Events.md
- DOMAIN-008L-Read-Model.md
- CORE-007-Strategic-Design.md
- CORE-016-Dependency-Rules.md

---

# Objetivo

Este documento identifica los puntos oficiales de extensión
(Extension Points) del Aggregate **Participation**.

Los Extension Points permiten incorporar nuevas capacidades al
dominio sin modificar el núcleo del Aggregate, respetando los
principios de Domain-Driven Design (DDD), Open/Closed Principle
y Clean Architecture.

El Aggregate debe permanecer estable mientras el ecosistema
AURA evoluciona mediante nuevos módulos, Bounded Contexts e
integraciones.

---

# Principios

Toda extensión debe cumplir los siguientes principios:

- no romper las invariantes del Aggregate;
- no modificar el comportamiento histórico;
- preservar el lenguaje ubicuo;
- mantener bajo acoplamiento;
- respetar el Lifecycle existente;
- respetar la State Machine existente;
- preservar el Consistency Boundary;
- mantener la independencia entre Aggregates;
- ser compatible con CQRS y Event Sourcing;
- evolucionar mediante composición y eventos.

---

# Filosofía

El Aggregate **Participation** representa la participación
registrada de un Citizen dentro de un contexto reconocido por
AURA.

Las capacidades pertenecientes a Organization, Citizen,
Membership, Territory, Assembly, Proposal, Voting, Document,
Notification, Audit o Integration no deben incorporarse al
Aggregate Participation si pertenecen a sus respectivos dominios.

La evolución ocurre alrededor del Aggregate, no mediante la
expansión indiscriminada de su límite de consistencia.

---

# Punto de Extensión 1 — Nuevos Commands

Es posible incorporar nuevos Commands cuando representen un
nuevo comportamiento real del dominio Participation.

Todo nuevo Command deberá:

- respetar ParticipationId;
- preservar OrganizationId;
- respetar el Lifecycle;
- respetar la State Machine;
- preservar las invariantes;
- respetar Permissions;
- actualizar la versión cuando corresponda;
- generar Domain Events cuando corresponda;
- mantener la consistencia del Aggregate.

Un nuevo Command no puede utilizarse para introducir una
transición inexistente sin que dicha evolución haya sido definida
formalmente en el modelo del Aggregate.

---

# Punto de Extensión 2 — Nuevos Domain Events

La evolución funcional puede introducir nuevos Domain Events
cuando aparezcan nuevos hechos significativos del dominio.

Todo nuevo Domain Event deberá:

- representar un hecho consumado;
- derivar de una modificación válida;
- respetar el lenguaje ubicuo;
- identificar la Participation correspondiente;
- conservar la versión del Aggregate;
- permanecer inmutable.

Los eventos existentes nunca se modifican para cambiar su
significado histórico.

---

# Punto de Extensión 3 — Nuevos Integration Events

El ecosistema puede requerir nuevos contratos de integración
derivados de hechos relevantes de Participation.

Los nuevos Integration Events pueden permitir comunicar cambios
hacia otros Bounded Contexts o sistemas externos.

Cada contrato debe:

- derivar de hechos confirmados;
- estar versionado;
- ser estable;
- permanecer desacoplado del modelo interno;
- identificar el Aggregate que originó el hecho;
- conservar AggregateVersion;
- exponer únicamente la información necesaria.

Los Integration Events no modifican directamente Participation.

---

# Punto de Extensión 4 — Nuevos Read Models

Pueden crearse nuevas proyecciones sin modificar el Aggregate.

Ejemplos conceptuales:

```text
ParticipationHistory

ParticipationByTerritory

ParticipationByAssembly

ParticipationByProposal

ParticipationActivity

ParticipationDashboard
```

Todas las proyecciones deben alimentarse de los eventos
correspondientes definidos por el modelo.

Los Read Models:

- son derivados;
- son reconstruibles;
- son de solo lectura;
- no contienen lógica de negocio;
- no modifican Participation;
- pueden evolucionar independientemente del Write Side.

---

# Punto de Extensión 5 — Nuevos Value Objects

El Aggregate puede enriquecerse mediante nuevos Value Objects
cuando exista un concepto del dominio que requiera mayor
expresividad y pertenezca realmente al límite de Participation.

Todo nuevo Value Object debe:

- aportar significado al dominio;
- ser inmutable;
- ser autoconsistente;
- carecer de identidad propia;
- preservar las invariantes del Aggregate;
- no representar un Aggregate externo.

No debe introducirse un Value Object únicamente por conveniencia
técnica.

---

# Punto de Extensión 6 — Nuevas Políticas

Las políticas relacionadas con Participation pueden evolucionar
cuando aparezcan reglas del dominio que requieran encapsulación
explícita.

Las políticas pueden colaborar con los casos de uso sin convertir
al Aggregate en responsable de información perteneciente a otros
Bounded Contexts.

Toda política deberá:

- utilizar conceptos del lenguaje ubicuo;
- respetar las invariantes;
- respetar Permissions;
- preservar el Consistency Boundary;
- evitar dependencias de infraestructura;
- no modificar directamente Aggregates externos.

---

# Punto de Extensión 7 — Nuevas Integraciones

Participation puede colaborar con nuevas integraciones mediante
Integration Events y contratos externos.

Las integraciones pueden relacionarse con:

- sistemas municipales;
- ecosistemas de participación ciudadana;
- FIWARE;
- servicios territoriales;
- plataformas de analítica;
- sistemas externos autorizados.

La integración nunca debe realizarse desde el Aggregate mediante
dependencias directas de infraestructura.

Debe mantenerse:

```text
Participation

↓

Domain Event

↓

Integration Event

↓

Integration Layer

↓

External System
```

---

# Punto de Extensión 8 — Nuevos Bounded Contexts

El crecimiento de AURA puede incorporar nuevos Bounded Contexts
que colaboren con Participation.

La colaboración debe realizarse mediante:

```text
Identity References

Domain Events

Integration Events

Application Coordination
```

Participation no debe absorber el modelo interno de otros
Bounded Contexts.

Los Aggregates ya relacionados con el ecosistema mantienen sus
propios límites:

```text
Organization

Citizen

Membership

Role

Territory

Assembly

Proposal

Voting

Document

Notification

Audit

Integration
```

Cada uno conserva su propia identidad, Lifecycle, Version,
Repository e Invariants.

---

# Punto de Extensión 9 — Automatización

Los eventos de Participation pueden activar procesos automáticos
fuera del Aggregate.

Ejemplo conceptual:

```text
ParticipationCompleted

↓

Application Process

↓

Update Projection

↓

Notify Interested Context

↓

Continue External Workflow
```

Estas automatizaciones pertenecen a la capa de aplicación o a
procesos de coordinación.

El Aggregate no debe incorporar directamente la lógica de los
consumidores.

---

# Punto de Extensión 10 — Nuevas Proyecciones Analíticas

La información derivada de Participation puede utilizarse para
nuevas capacidades analíticas sin modificar el Write Model.

Ejemplos conceptuales:

```text
Participation by Organization

Participation by Citizen

Participation by Territory

Participation by Assembly

Participation by Proposal

Participation by Status

Participation by Type
```

Estas capacidades deben construirse sobre Read Models y eventos.

No deben introducir lógica analítica dentro del Aggregate.

---

# Extensión del Lifecycle

El Lifecycle existente no constituye un punto de extensión libre.

Una nueva etapa o transición solo podrá incorporarse cuando exista
una nueva regla explícita del dominio y su incorporación sea
documentada de forma coherente en:

```text
DOMAIN-008-Aggregate.md

DOMAIN-008A-Lifecycle.md

DOMAIN-008B-State-Machine.md

DOMAIN-008C-Commands.md

DOMAIN-008D-Domain-Events.md

DOMAIN-008E-Invariants.md
```

No puede agregarse una transición únicamente por necesidad técnica
o de interfaz.

---

# Extensión de la State Machine

La State Machine puede evolucionar únicamente como consecuencia de
una evolución explícita del dominio.

Toda nueva transición deberá mantener coherencia con:

- estado origen;
- estado destino;
- Command correspondiente;
- Domain Event correspondiente;
- Permissions;
- Invariants;
- Versioning.

Una Extension no puede evitar la State Machine existente.

---

# Extensión de Invariants

Pueden incorporarse nuevas Invariants cuando una nueva regla real
del dominio deba permanecer siempre verdadera.

Una nueva Invariant deberá:

- pertenecer al Aggregate Participation;
- proteger un estado válido;
- ser verificable;
- aplicarse de forma consistente;
- no depender directamente de Infrastructure;
- no ampliar innecesariamente el Consistency Boundary.

Las Invariants existentes no pueden debilitarse mediante un
Extension Point.

---

# Extensión de Permissions

Pueden incorporarse nuevas Permissions únicamente cuando exista un
nuevo comportamiento protegido del dominio.

Debe mantenerse:

```text
New Protected Command

↓

Corresponding Permission
```

La incorporación de una Permission no crea por sí misma un nuevo
comportamiento.

Las Permissions continúan separadas de:

```text
State Machine

Lifecycle

Invariants
```

---

# Extensión del Repository

El Repository Contract puede evolucionar cuando exista una nueva
necesidad real de recuperación o persistencia del Aggregate.

Toda extensión deberá preservar:

- Aggregate Root;
- identidad;
- Version;
- concurrencia optimista;
- Consistency Boundary;
- independencia tecnológica.

Las necesidades de búsqueda, filtrado, paginación, dashboards o
analytics deben resolverse mediante Read Models cuando
correspondan.

---

# Extensión de Versioning

El modelo de Versioning puede evolucionar únicamente sin alterar
su semántica fundamental.

Debe mantenerse:

```text
One Aggregate

↓

One Version
```

y:

```text
Valid Modification

↓

Version + 1
```

Las extensiones no pueden:

- reiniciar Version;
- disminuir Version;
- compartir Version entre Aggregates;
- eliminar el control de concurrencia;
- permitir sobrescrituras silenciosas.

---

# Extensión del Consistency Boundary

El Consistency Boundary no debe ampliarse únicamente para
simplificar una integración o caso de uso.

Debe mantenerse:

```text
Participation

=

Independent Consistency Boundary
```

La necesidad de coordinar Participation con otros Aggregates debe
resolverse mediante los mecanismos de colaboración definidos por
AURA.

---

# Extensión de Integration Events

Pueden incorporarse nuevos Integration Events cuando un hecho de
Participation deba formar parte de un contrato externo.

Todo nuevo Integration Event deberá:

- derivar de un hecho confirmado;
- preservar EventId;
- identificar ParticipationId;
- preservar AggregateVersion;
- permanecer inmutable;
- permanecer desacoplado del consumidor;
- exponer únicamente información necesaria.

---

# Extensión de Read Models

Los Read Models representan uno de los principales puntos de
evolución de Participation.

Pueden incorporarse nuevas vistas para resolver:

- búsquedas;
- listados;
- filtros;
- estadísticas;
- dashboards;
- indicadores;
- necesidades territoriales;
- consultas organizacionales;
- consultas ciudadanas.

La incorporación de un Read Model no requiere modificar el
Aggregate cuando la información necesaria ya puede derivarse de
sus eventos.

---

# Extensión de Test Scenarios

Toda nueva capacidad del dominio debe incorporar los escenarios de
prueba correspondientes.

Una extensión debe verificar como mínimo:

```text
Valid Scenario

Invalid Scenario

Invariant Preservation

Version Evolution

Permission Enforcement

Domain Event

Persistence

Consistency Boundary
```

cuando dichos elementos correspondan.

Los escenarios existentes no deben eliminarse para adaptar el
dominio a una extensión incompatible.

---

# Extensión de Performance

Las optimizaciones futuras pueden incorporarse siempre que
mantengan:

```text
Domain Correctness

+

Performance
```

No constituyen Extension Points válidos:

```text
Skip Aggregate Root

Skip Invariants

Skip Permissions

Skip Versioning

Skip State Machine
```

La optimización pertenece a Infrastructure cuando no modifica el
significado del dominio.

---

# Extensión de Security

Las futuras capacidades de seguridad deben preservar:

- encapsulamiento;
- Permissions;
- aislamiento organizacional;
- Versioning;
- Consistency Boundary;
- protección de información;
- separación entre Read Side y Write Side.

Una extensión de seguridad no debe incorporar dependencias de una
tecnología concreta dentro del Aggregate.

---

# Compatibilidad hacia Atrás

Las extensiones deben preservar el significado de los contratos ya
publicados.

No debe modificarse retroactivamente:

- el significado de un Command existente;
- el significado de un Domain Event existente;
- el significado de un Integration Event existente;
- la identidad de Participation;
- la semántica de Version.

Cuando una evolución requiera un nuevo significado debe expresarse
mediante un nuevo contrato compatible con las reglas de evolución
de AURA.

---

# Open/Closed Principle

Participation debe permanecer:

```text
Open for Extension

Closed for Uncontrolled Modification
```

Esto significa que pueden incorporarse nuevas capacidades sin
alterar arbitrariamente las reglas ya consolidadas.

---

# Bajo Acoplamiento

Toda extensión debe mantener bajo acoplamiento.

Debe evitarse:

```text
Participation

↓

Direct Dependency on External Aggregate
```

Debe preferirse:

```text
Participation

↓

Identity Reference
```

o:

```text
Participation

↓

Event

↓

External Consumer
```

según corresponda.

---

# Alta Cohesión

Toda nueva responsabilidad incorporada directamente a
Participation debe pertenecer realmente al concepto de
Participation.

Si una capacidad pertenece principalmente a:

```text
Organization

Citizen

Membership

Territory

Assembly

Proposal

Voting

Document

Notification

Audit

Integration
```

debe permanecer en su dominio correspondiente.

---

# Independencia de Infrastructure

Los Extension Points no deben introducir dependencias directas
hacia:

- bases de datos;
- frameworks;
- protocolos externos;
- brokers;
- proveedores de identidad;
- sistemas municipales;
- FIWARE;
- mecanismos de caché.

Estas capacidades pertenecen a Infrastructure o Integration.

---

# Restricciones

No constituyen puntos de extensión:

- modificar ParticipationId;
- modificar OrganizationId;
- alterar arbitrariamente la State Machine existente;
- introducir transiciones no documentadas;
- romper Invariants;
- eliminar Domain Events históricos;
- cambiar el significado de Commands ya establecidos;
- cambiar retroactivamente el significado de Integration Events;
- reiniciar Version;
- eliminar el control de concurrencia;
- ampliar el Consistency Boundary por conveniencia;
- incorporar Aggregates externos dentro de Participation;
- introducir dependencias de infraestructura en el dominio;
- convertir Read Models en fuente de escritura;
- utilizar Metadata para introducir comportamiento oculto;
- utilizar Extension Points para evitar Permissions;
- utilizar Extension Points para evitar Lifecycle;
- utilizar Extension Points para evitar State Machine;
- utilizar Extension Points para evitar Invariants;
- utilizar Extension Points para evitar Versioning.

---

# Compatibilidad con CQRS

Las extensiones del lado de lectura pueden evolucionar
independientemente del lado de escritura.

Nuevas consultas, filtros, estadísticas o dashboards no requieren
modificar el Aggregate cuando pueden construirse mediante
proyecciones.

Debe mantenerse:

```text
Write Side

Participation Aggregate
```

separado de:

```text
Read Side

Participation Read Models
```

---

# Compatibilidad con Event Sourcing

Las nuevas funcionalidades compatibles con Event Sourcing deben
expresarse mediante hechos del dominio.

Los Domain Events históricos permanecen inmutables.

Replay no debe reinterpretar eventos existentes utilizando
significados nuevos incompatibles con su definición original.

---

# Estrategia de Evolución

La evolución del Aggregate seguirá el siguiente principio:

```text
Nuevos requisitos

        │

        ▼

Evaluar pertenencia al dominio Participation

        │

        ▼

Nuevo comportamiento cuando corresponda

        │

        ▼

Nuevos Commands

        │

        ▼

Nuevos Domain Events

        │

        ▼

Nuevos Read Models

        │

        ▼

Nuevas Integraciones

        │

        ▼

Nuevo Valor para el Ecosistema
```

El núcleo del Aggregate permanece estable durante todo el proceso.

---

# Principios Arquitectónicos

Los Extension Points siguen:

- Domain-Driven Design (DDD);
- Open/Closed Principle;
- Clean Architecture;
- Hexagonal Architecture;
- CQRS;
- Event Sourcing;
- Event-Driven Architecture;
- Low Coupling;
- High Cohesion.

---

# Definición de Éxito

El Aggregate **Participation** dispone de una estrategia explícita
de extensión que permite incorporar nuevas capacidades funcionales,
proyecciones, integraciones y colaboraciones con otros Bounded
Contexts sin alterar arbitrariamente su núcleo conceptual.

Los Extension Points garantizan que:

- ParticipationId permanezca estable;
- OrganizationId permanezca inmutable;
- Lifecycle y State Machine evolucionen únicamente mediante
  decisiones explícitas del dominio;
- las Invariants permanezcan protegidas;
- Permissions continúe separada de las reglas internas;
- Versioning mantenga concurrencia y trazabilidad;
- el Consistency Boundary no se amplíe por conveniencia;
- los otros Aggregates permanezcan independientes;
- los nuevos Domain Events expresen hechos reales del dominio;
- los Integration Events permanezcan desacoplados;
- los Read Models puedan evolucionar independientemente;
- las integraciones permanezcan fuera del Aggregate;
- las optimizaciones no modifiquen las reglas conceptuales;
- las extensiones respeten bajo acoplamiento y alta cohesión;
- Infrastructure permanezca separada del dominio.

Gracias a estos puntos de extensión, AURA puede evolucionar sus
capacidades de participación ciudadana manteniendo estable el
núcleo de **Participation** y preservando la coherencia del modelo
DDD consolidado de AURA Core.