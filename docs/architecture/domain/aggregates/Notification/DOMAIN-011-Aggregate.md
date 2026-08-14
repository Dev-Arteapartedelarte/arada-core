# DOMAIN-011 — Notification Aggregate

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Notification Management

Aggregate:
Notification

Autor:
ARADA

Documentos Relacionados:

- CORE-002-Bounded-Context-Map.md
- CORE-003-Shared-Kernel.md
- CORE-004-Ubiquitous-Language.md
- CORE-006-Domain-Invariants.md
- CORE-007-Strategic-Design.md
- CORE-008-Aggregate-Design-Rules.md
- CORE-011-Repository-Contracts.md
- DOMAIN-001-Aggregate.md
- DOMAIN-002-Aggregate.md
- DOMAIN-003-Aggregate.md
- DOMAIN-004-Aggregate.md
- DOMAIN-005-Aggregate.md
- DOMAIN-006-Aggregate.md
- DOMAIN-007-Aggregate.md
- DOMAIN-008-Aggregate.md
- DOMAIN-009-Aggregate.md
- DOMAIN-010-Aggregate.md

---

# Objetivo

El Aggregate **Notification** representa una unidad formal de
notificación dentro del ecosistema AURA.

Notification permite gestionar la existencia, preparación,
destinatarios, canal, entrega, reintentos y estado de una
comunicación originada como consecuencia de una necesidad de
notificación reconocida por el dominio.

El Aggregate mantiene la consistencia de cada Notification como
unidad independiente.

Los hechos que originan la necesidad de una notificación pueden
pertenecer a otros Aggregates.

Notification no absorbe dichos Aggregates ni modifica directamente
su estado.

---

# Propósito

El propósito del Aggregate Notification es proporcionar una
representación consistente y trazable de una comunicación que debe
ser gestionada por Notification Management.

Notification permite representar conceptualmente:

- identidad de la Notification;
- destinatarios;
- canal;
- contenido o representación comunicacional;
- plantilla cuando corresponda;
- estado de la Notification;
- entrega;
- reintentos;
- trazabilidad de modificaciones relevantes;
- Version;
- Domain Events.

Notification constituye el límite de consistencia de la unidad de
notificación.

No constituye el límite de consistencia del hecho de dominio que
originó la necesidad de comunicación.

---

# Definición

Una Notification representa una comunicación administrada por el
Bounded Context:

```text
Notification Management
```

La Notification puede originarse como consecuencia de hechos
pertenecientes a otros contextos del ecosistema AURA.

Conceptualmente:

```text
Domain Fact

    │
    ▼

Notification Need

    │
    ▼

Notification Management

    │
    ▼

Notification
```

El Aggregate responsable del hecho original publica el hecho.

Notification Management determina las condiciones necesarias para
gestionar la comunicación correspondiente.

La existencia de un hecho en otro Aggregate no significa que dicho
Aggregate envíe directamente la Notification.

---

# Aggregate Root

La única Aggregate Root es:

```text
Notification
```

Toda modificación del estado interno debe realizarse mediante
comportamiento expuesto por esta Aggregate Root.

Ninguna Entity, Value Object o elemento interno puede modificarse
directamente desde fuera del Aggregate.

Debe mantenerse:

```text
External Actor

    │
    ▼

Notification Aggregate Root

    │
    ▼

Internal State
```

Nunca:

```text
External Actor

    │
    ▼

Internal State
```

---

# Identidad

Cada Notification posee identidad propia:

```text
NotificationId
```

NotificationId:

- identifica de forma única la Notification;
- existe durante toda la vida del Aggregate;
- permanece inmutable;
- no puede reutilizarse para representar otra Notification;
- no puede ser sustituido por identificadores de otros Aggregates.

Debe mantenerse:

```text
NotificationId

≠

CitizenId

≠

OrganizationId

≠

AssemblyId

≠

DocumentId
```

La relación con otros conceptos nunca reemplaza la identidad
propia de Notification.

---

# Responsabilidad

Notification Management es responsable conceptualmente de:

```text
destinatarios

canales

plantillas

entrega

reintentos

estado de envío
```

Estas responsabilidades pertenecen al dominio Notification y no
al Aggregate que produjo el hecho originador.

Por ejemplo:

```text
Assembly

    │
    ▼

Domain Event

    │
    ▼

Notification Management
```

Assembly comunica el hecho.

Notification Management administra la Notification.

---

# Origen de una Notification

Una Notification puede surgir como consecuencia de hechos
relevantes producidos por otros Aggregates.

El Aggregate de origen conserva la responsabilidad sobre su propio
hecho.

Notification conserva la responsabilidad sobre la comunicación.

Debe mantenerse:

```text
Source Aggregate Fact

≠

Notification
```

y:

```text
Source Aggregate Lifecycle

≠

Notification Lifecycle
```

Notification no cambia retrospectivamente el hecho que originó la
necesidad de comunicación.

---

# Destinatarios

Notification Management determina los destinatarios que
corresponden a una Notification.

La definición concreta de las reglas de destinatarios pertenece al
dominio Notification y deberá mantenerse bajo sus Invariants y
contratos específicos.

Una Notification no incorpora el Aggregate completo correspondiente
al destinatario.

Cuando exista una relación con otro Aggregate debe utilizarse una
referencia por identidad o un contrato explícito.

Debe mantenerse:

```text
Recipient Reference

≠

Embedded External Aggregate
```

---

# Canal

Notification Management determina el canal correspondiente para la
comunicación.

El concepto de canal pertenece al dominio Notification.

La elección conceptual del canal no debe confundirse con una
implementación tecnológica concreta.

Debe mantenerse:

```text
Notification Channel

≠

Infrastructure Provider
```

El dominio no depende directamente de proveedores, SDKs, APIs o
protocolos concretos utilizados para ejecutar técnicamente la
entrega.

---

# Plantillas

Notification Management puede utilizar plantillas cuando
corresponda a la comunicación.

Una plantilla representa una estructura conceptual utilizada para
formar la comunicación.

Su utilización no autoriza a incorporar dentro de Notification
responsabilidades pertenecientes a:

- Document;
- sistemas de presentación;
- proveedores externos;
- Infrastructure.

La estructura concreta, reglas y clasificación de las plantillas
deberán definirse explícitamente en los artefactos correspondientes
del Aggregate y no deben inferirse desde este documento.

---

# Contenido de la Comunicación

Notification mantiene únicamente la información necesaria para
representar consistentemente la comunicación bajo responsabilidad
del Aggregate.

El contenido comunicacional no convierte Notification en
Document.

Debe mantenerse:

```text
Notification Communication

≠

Document Aggregate
```

Cuando una Notification necesite referenciar un Document, la
relación debe realizarse mediante identificadores o contratos.

Notification no almacena ni administra el Lifecycle del Aggregate
Document.

---

# Entrega

La entrega de una Notification pertenece a Notification
Management.

El Aggregate debe poder representar conceptualmente el resultado
relevante de su proceso de entrega conforme al Lifecycle,
State Machine e Invariants que se definan para Notification.

La ejecución técnica de la entrega pertenece a capas externas.

Debe mantenerse:

```text
Notification Delivery Domain

≠

External Provider Implementation
```

El dominio expresa el significado de la entrega.

Infrastructure ejecuta los mecanismos técnicos necesarios para
realizarla.

---

# Reintentos

Los reintentos forman parte de las responsabilidades reconocidas
para Notification Management.

Las condiciones exactas bajo las cuales una Notification puede ser
reintentada deben definirse explícitamente mediante:

```text
DOMAIN-011A-Lifecycle.md

DOMAIN-011B-State-Machine.md

DOMAIN-011C-Commands.md

DOMAIN-011E-Invariants.md
```

Este documento no introduce una cantidad máxima de reintentos, una
política temporal ni una estrategia de backoff.

Dichas reglas no deben inferirse sin una definición explícita del
dominio.

---

# Estado

Notification posee estado propio.

El estado representa la posición actual del Aggregate dentro de su
Lifecycle.

Este documento no introduce implícitamente el conjunto oficial de
valores de NotificationStatus.

Los estados, su significado y las transiciones válidas deben
definirse formalmente en:

```text
DOMAIN-011A-Lifecycle.md

DOMAIN-011B-State-Machine.md
```

Debe cumplirse:

- Notification siempre mantiene un estado válido;
- el estado solamente cambia mediante comportamiento de dominio;
- ninguna transición puede inventarse desde Infrastructure;
- ninguna transición puede omitir las Invariants;
- una operación rechazada no modifica el estado confirmado.

---

# Reglas de Estado

El Aggregate debe garantizar:

- que NotificationStatus pertenezca al conjunto oficial definido
  por su State Machine;
- que toda transición posea un estado de origen válido;
- que toda transición produzca un estado destino válido;
- que ninguna transición pueda realizarse mediante modificación
  directa;
- que una transición rechazada conserve el estado confirmado;
- que una transición rechazada no genere un Domain Event de éxito.

Las reglas exactas pertenecen a:

```text
DOMAIN-011B-State-Machine.md
```

---

# Version

Notification utiliza:

```text
Version
```

para representar la evolución lógica del Aggregate y soportar
Optimistic Concurrency Control.

Toda modificación válida incrementa Version.

Una operación rechazada no incrementa Version.

Una operación de lectura no incrementa Version.

Conceptualmente:

```text
Notification vN

    │
    ▼

Valid Modification

    │
    ▼

Notification vN+1
```

Las reglas completas se especifican en:

```text
DOMAIN-011I-Versioning.md
```

---

# CreatedAt

Notification mantiene conceptualmente:

```text
CreatedAt
```

CreatedAt representa el momento de creación de la Notification.

Una vez establecido no cambia durante la vida del Aggregate.

---

# UpdatedAt

Notification mantiene conceptualmente:

```text
UpdatedAt
```

UpdatedAt representa el momento de la última modificación válida
del Aggregate.

Se actualiza únicamente como consecuencia de una modificación
aceptada por la Aggregate Root.

Una operación rechazada no debe modificar UpdatedAt.

---

# Entidades Internas

Notification puede contener conceptos internos únicamente cuando
sean necesarios para mantener su propia consistencia.

Un concepto interno:

- pertenece completamente a Notification;
- no posee Lifecycle independiente fuera del Aggregate;
- no puede modificarse directamente desde otro Aggregate;
- debe respetar las Invariants de Notification.

Este documento no establece entidades internas concretas
adicionales.

Cuando un concepto requiera:

- identidad independiente;
- Lifecycle propio;
- Invariants propias;
- Consistency Boundary propio;

debe evaluarse explícitamente conforme a las reglas de diseño de
AURA antes de incorporarlo al Aggregate.

---

# Value Objects

Notification puede utilizar Value Objects para representar
conceptos propios del dominio.

Todo Value Object:

- se define por sus valores;
- carece de identidad independiente;
- es inmutable;
- protege sus propias reglas de validez;
- pertenece al modelo de dominio.

La clasificación concreta de destinatarios, canales, plantillas,
contenido y demás conceptos como Value Objects o Entities no debe
inferirse desde este documento.

Dicha clasificación requiere definición explícita conforme al
patrón consolidado de AURA.

---

# Invariantes

Notification debe mantener como mínimo:

- NotificationId existe;
- NotificationId permanece inmutable;
- Notification mantiene un estado válido;
- toda transición pertenece a su State Machine;
- ninguna modificación evita la Aggregate Root;
- las referencias externas utilizan identificadores o contratos;
- ningún Aggregate externo se incorpora dentro de Notification;
- Notification no modifica directamente otros Aggregates;
- toda modificación válida incrementa Version;
- una operación rechazada conserva el estado confirmado;
- una operación rechazada conserva Version;
- una operación rechazada no produce un Domain Event de éxito;
- CreatedAt permanece inmutable;
- UpdatedAt solamente cambia después de una modificación válida;
- las Invariants deben cumplirse antes y después de cada operación.

Las Invariants completas se especifican en:

```text
DOMAIN-011E-Invariants.md
```

---

# Relaciones entre Aggregates

Notification puede relacionarse con otros Aggregates mediante:

```text
AggregateId

Domain Events

Integration Events

contratos de dominio
```

Nunca mediante referencias mutables al estado interno de otro
Aggregate.

Notification no contiene instancias completas de:

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

Cada uno conserva su propio:

- Aggregate Root;
- identidad;
- Lifecycle;
- Invariants;
- Repository;
- Version;
- Consistency Boundary.

---

# Notification y Organization

Una Notification puede existir en un contexto relacionado con una
Organization.

Notification no administra:

- identidad de Organization;
- estructura organizacional;
- Lifecycle de Organization;
- Roles;
- Memberships.

La necesidad concreta de una referencia organizacional debe
depender del caso de dominio correspondiente y no debe inferirse
como obligatoria desde este documento.

---

# Notification y Citizen

Una Notification puede estar destinada a actores cuya identidad
cívica sea representada por Citizen.

Notification no contiene el Aggregate Citizen.

Notification no modifica:

- CitizenStatus;
- identidad de Citizen;
- datos propios del Lifecycle de Citizen.

Cuando corresponda una relación con Citizen, deberá realizarse
mediante identidad o contratos explícitos.

---

# Notification y Membership

Membership puede aportar contexto organizacional cuando una
comunicación dependa de una relación formal entre Citizen y
Organization.

Notification no:

- crea Membership;
- activa Membership;
- suspende Membership;
- termina Membership;
- modifica Membership.

Las reglas de Membership permanecen en su Aggregate.

---

# Notification y Role

Role puede participar en las políticas que determinen
destinatarios cuando el dominio correspondiente así lo establezca.

Notification no crea ni modifica Roles.

La existencia de un Role no convierte dicho Role en parte interna
del Aggregate Notification.

---

# Notification y Territory

Una Notification puede utilizar contexto territorial cuando una
regla explícita del dominio lo requiera.

Notification no administra Territory.

No modifica:

- estructura territorial;
- jerarquía territorial;
- Lifecycle de Territory.

---

# Notification y Assembly

Assembly puede producir hechos que generen necesidades de
notificación.

Entre ellos pueden existir hechos relacionados con:

- creación;
- convocatoria;
- modificación;
- cancelación;
- otros hechos explícitamente definidos por Assembly.

Assembly publica el hecho.

Notification Management decide:

```text
destinatarios

canales

plantillas

entrega

reintentos

estado de envío
```

Debe mantenerse:

```text
Assembly Fact

    │
    ▼

Notification Management
```

y nunca:

```text
Assembly

    │
    ▼

Direct Notification Delivery
```

Convocar una Assembly no equivale a enviar una Notification.

La convocatoria pertenece a Assembly.

La entrega efectiva de la comunicación pertenece a Notification.

---

# Notification y Proposal

Proposal conserva su identidad, Lifecycle e Invariants.

Si un hecho de Proposal origina una necesidad de comunicación,
Notification puede reaccionar mediante los contratos
correspondientes.

Notification no modifica directamente Proposal.

---

# Notification y Participation

Participation conserva su propio modelo de dominio.

Cuando un hecho de Participation origine una necesidad de
comunicación, Notification puede gestionarla mediante los
mecanismos de coordinación definidos por AURA.

Notification no administra el proceso de Participation.

---

# Notification y Voting

Voting conserva:

- VotingId;
- Lifecycle;
- State Machine;
- Invariants;
- Version;
- Consistency Boundary.

Un hecho de Voting puede generar una necesidad de notificación
cuando exista una regla o proceso explícitamente definido.

Notification no:

- abre Voting;
- cierra Voting;
- registra votos;
- modifica resultados;
- altera VotingStatus.

---

# Notification y Document

Document conserva su propio:

- DocumentId;
- Content;
- DocumentType;
- Lifecycle;
- State Machine;
- Version;
- Consistency Boundary.

Notification puede referenciar información documental cuando un
contrato explícito lo requiera.

Notification no almacena el Aggregate Document ni administra su
contenido.

La publicación de un Document no equivale por sí misma a la
entrega de una Notification.

---

# Notification y Audit

Audit permanece fuera del Aggregate Notification.

Los hechos relevantes de Notification pueden ser utilizados por el
contexto de Audit mediante eventos y contratos.

Notification no almacena Audit Records como entidades internas.

Debe mantenerse:

```text
Notification Domain Event

≠

Audit Record
```

---

# Consistencia

Notification constituye un límite de consistencia independiente.

Dentro del Aggregate deben mantenerse de forma inmediata:

- identidad;
- estado;
- reglas propias de la Notification;
- elementos internos pertenecientes al Aggregate;
- Version;
- Invariants.

La consistencia entre Notification y otros Aggregates es eventual.

Debe mantenerse:

```text
Notification Consistency

=

Internal Immediate Consistency
```

y:

```text
Notification

+

External Aggregate

=

Separate Consistency Boundaries
```

---

# Límite de Consistencia

El Consistency Boundary comprende:

```text
Notification
    │
    ├── State
    ├── Value Objects
    ├── Internal Entities
    └── Version
```

cuando dichos elementos hayan sido definidos explícitamente como
pertenecientes al Aggregate.

El límite no comprende:

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

La definición formal se desarrolla en:

```text
DOMAIN-011J-Consistency-Boundary.md
```

---

# Commands

Notification responde a Commands que expresan intenciones del
dominio.

Los Commands oficiales no deben inferirse desde responsabilidades
conceptuales, nombres de estados o mecanismos técnicos.

La definición exacta pertenece a:

```text
DOMAIN-011C-Commands.md
```

Todo Command:

- expresa una intención;
- debe atravesar la Aggregate Root;
- debe respetar las Invariants;
- debe respetar la State Machine;
- solamente modifica el Aggregate cuando la operación es válida;
- puede producir Domain Events cuando ocurra un hecho relevante.

---

# Operaciones Públicas

La Aggregate Root expone comportamiento de dominio.

No se exponen setters públicos.

No puede modificarse directamente:

```text
NotificationId

NotificationStatus

Version

CreatedAt

UpdatedAt
```

ni ningún otro elemento protegido por las Invariants del
Aggregate.

Las operaciones públicas concretas deben derivarse únicamente de
los Commands oficialmente definidos.

---

# Eventos del Dominio

Notification produce Domain Events cuando ocurren hechos
significativos aceptados por el Aggregate.

Un Domain Event:

- representa un hecho consumado;
- pertenece a Notification;
- se genera después de comportamiento válido;
- mantiene la identidad del Aggregate;
- mantiene coherencia con Version;
- no constituye un Command;
- no modifica directamente otros Aggregates.

El conjunto oficial de Domain Events se define exclusivamente en:

```text
DOMAIN-011D-Domain-Events.md
```

Este documento no introduce nombres de eventos no consolidados.

---

# Ciclo de Vida

Notification posee Lifecycle propio e independiente del Aggregate
que originó la necesidad de comunicación.

Las etapas oficiales, estados terminales, rutas alternativas y
condiciones de transición deben definirse explícitamente en:

```text
DOMAIN-011A-Lifecycle.md

DOMAIN-011B-State-Machine.md
```

No debe inferirse que:

- una necesidad de comunicación equivale a una Notification
  entregada;
- una ejecución técnica exitosa define por sí sola un estado de
  dominio;
- un error técnico define automáticamente un estado nuevo;
- un reintento constituye necesariamente una transición;
- una Notification posee un estado Archived por analogía con otros
  Aggregates.

Toda decisión de Lifecycle debe pertenecer explícitamente al modelo
Notification.

---

# Persistencia

Notification se persiste mediante un Repository Contract.

El Repository:

- recupera Notification por identidad;
- persiste el Aggregate como unidad;
- protege la concurrencia optimista;
- oculta el mecanismo de almacenamiento;
- no ejecuta reglas de negocio;
- no modifica directamente el estado.

Conceptualmente:

```text
Application Service

    │
    ▼

Notification Repository

    │
    ▼

Notification Aggregate
```

El contrato formal se define en:

```text
DOMAIN-011G-Repository-Contract.md
```

---

# Versionado

Notification utiliza Optimistic Concurrency Control.

Cada modificación válida incrementa:

```text
Version
```

Ante una escritura incompatible debe producirse el comportamiento
definido por el Repository Contract.

Una modificación obsoleta no puede sobrescribir silenciosamente
una modificación previamente confirmada.

La especificación formal se encuentra en:

```text
DOMAIN-011I-Versioning.md
```

---

# Reglas de Modificación

Toda modificación de Notification debe cumplir:

- ninguna modificación directa de atributos protegidos;
- ninguna modificación fuera de la Aggregate Root;
- ninguna modificación de NotificationId;
- ninguna transición fuera de la State Machine;
- ninguna operación que deje el Aggregate en estado inválido;
- toda modificación válida incrementa Version;
- toda modificación relevante produce el Domain Event
  correspondiente cuando éste exista en el contrato oficial;
- toda operación rechazada conserva el estado confirmado;
- toda operación rechazada conserva Version;
- toda operación rechazada no genera un Domain Event de éxito.

---

# Fuente de Verdad

La fuente de verdad de Notification es el Aggregate Notification
y, cuando corresponda a la estrategia de persistencia adoptada, su
historial de Domain Events.

Los Read Models:

- no constituyen fuente de verdad de escritura;
- pueden reconstruirse;
- no modifican Notification;
- no controlan su State Machine.

La definición de lectura pertenece a:

```text
DOMAIN-011L-Read-Model.md
```

---

# Seguridad

Notification no administra autenticación.

Notification no almacena:

- contraseñas;
- tokens;
- claves privadas;
- secretos criptográficos;
- credenciales;
- sesiones.

La autorización de operaciones pertenece al modelo de seguridad y
Permissions de AURA.

Una intención autorizada todavía debe superar:

- Lifecycle;
- State Machine;
- Invariants;
- Versioning.

Las reglas formales se encuentran en:

```text
DOMAIN-011F-Permissions.md

DOMAIN-011O-Security-Model.md
```

---

# Integración

Notification constituye un punto especializado de comunicación
dentro del ecosistema AURA, pero el Aggregate permanece
independiente de los mecanismos tecnológicos utilizados para
ejecutar las integraciones.

Notification puede participar conceptualmente en procesos
relacionados con:

- Organization Management;
- Citizen Management;
- Membership Management;
- Role Management;
- Territory Management;
- Assembly Management;
- Proposal Management;
- Participation Management;
- Voting Management;
- Document Management;
- Audit;
- Smart City Integration;
- plataformas municipales;
- otros sistemas externos mediante contratos.

Estas relaciones no convierten los sistemas o Aggregates externos
en elementos internos de Notification.

---

# Integration Events

Los hechos de Notification que necesiten cruzar límites de contexto
pueden transformarse en Integration Events mediante contratos
explícitos.

Domain Event e Integration Event representan conceptos diferentes.

Debe mantenerse:

```text
Domain Event

≠

Integration Event
```

La existencia de un Domain Event no implica automáticamente la
existencia de un Integration Event.

El conjunto y contratos formales se definen en:

```text
DOMAIN-011K-Integration-Events.md
```

---

# Read Model

Notification puede disponer de Read Models especializados para
consulta.

Los Read Models:

- son proyecciones;
- pueden reconstruirse;
- no constituyen fuente de verdad de escritura;
- no poseen autoridad para modificar Notification;
- pueden optimizarse para necesidades concretas de consulta.

Las proyecciones oficiales no deben inferirse desde este documento.

Su definición pertenece a:

```text
DOMAIN-011L-Read-Model.md
```

---

# Rendimiento

Notification debe mantenerse pequeño y enfocado en su propio
Consistency Boundary.

No debe cargar Aggregates externos para ejecutar comportamiento
ordinario.

Debe utilizar:

- identificadores;
- Value Objects;
- contratos de dominio;
- eventos;
- Read Models para consultas.

Las operaciones técnicas de entrega no deben ampliar
innecesariamente el Aggregate ni introducir dependencias de
proveedores externos.

Las reglas específicas se encuentran en:

```text
DOMAIN-011N-Performance-Rules.md
```

---

# Extensibilidad

Notification debe permitir evolución controlada sin modificar
innecesariamente su núcleo.

Los puntos de extensión pueden incluir conceptualmente:

```text
destinatarios

canales

plantillas

políticas de entrega

políticas de reintento

Domain Events

Integration Events

Read Models

Value Objects

Domain Policies
```

Estas posibilidades no constituyen definiciones automáticas de
nuevos elementos del modelo.

Toda extensión debe:

- preservar NotificationId;
- preservar Invariants;
- preservar Consistency Boundary;
- evitar estados implícitos;
- evitar Commands implícitos;
- evitar dependencias con Infrastructure;
- evitar incorporar Aggregates externos;
- evitar acoplamiento directo con proveedores.

La definición formal se encuentra en:

```text
DOMAIN-011P-Extension-Points.md
```

---

# Compatibilidad Arquitectónica

Notification está diseñado para cumplir:

- Domain-Driven Design;
- Aggregate Pattern;
- Clean Architecture;
- Hexagonal Architecture;
- SOLID;
- Event-Driven Architecture;
- CQRS;
- Event Sourcing Compatible;
- Optimistic Concurrency Control;
- High Cohesion;
- Low Coupling.

El Aggregate pertenece al dominio y no depende de tecnologías de
Infrastructure.

---

# Dependencias

Notification depende conceptualmente de:

- Shared Kernel;
- Value Objects;
- Domain Events;
- Repository Contracts;
- contratos de dominio definidos por AURA.

Notification no depende directamente de:

```text
Infrastructure

Frameworks

Bases de datos

HTTP

REST

GraphQL

SMTP

SMS Providers

Push Providers

Messaging Providers

OAuth

JWT

React

Next.js

FastAPI

Django

FIWARE SDK

MongoDB

PostgreSQL
```

Las implementaciones tecnológicas pertenecen a capas externas.

---

# Relaciones Estratégicas

Notification puede ser utilizado por procesos pertenecientes a
distintos Bounded Contexts cuando éstos generen hechos que
requieran comunicación.

Notification mantiene separada:

```text
Domain Fact

from

Communication Delivery
```

El Aggregate que produce un hecho conserva ownership sobre dicho
hecho.

Notification conserva ownership sobre la unidad de notificación y
su proceso de comunicación.

Esta separación permite que los demás Aggregates permanezcan
enfocados en sus propias responsabilidades.

---

# CQRS

Notification es compatible con CQRS.

En el lado de escritura:

```text
Command
   │
   ▼
Notification Aggregate
   │
   ├── Invariants
   ├── State Transition
   └── Domain Events
```

En el lado de lectura:

```text
Domain Events
      │
      ▼
Projection
      │
      ▼
Read Model
```

El Read Model no reemplaza al Aggregate.

---

# Event Sourcing

Notification es compatible con Event Sourcing.

Cuando esta estrategia sea adoptada, los Domain Events oficiales
definidos para Notification pueden representar la evolución
histórica del Aggregate.

El conjunto de eventos no debe inferirse desde este documento.

La reconstrucción debe utilizar únicamente hechos pertenecientes al
mismo:

```text
NotificationId
```

El historial debe ser inmutable.

Los eventos representan hechos ocurridos y no instrucciones
futuras.

La implementación concreta de Event Sourcing pertenece a
Infrastructure.

---

# Trazabilidad

Notification debe permitir reconstruir conceptualmente:

- identidad de la Notification;
- estado;
- modificaciones relevantes;
- Version;
- hechos de dominio;
- evolución de la entrega cuando ésta sea definida por el
  Lifecycle oficial;
- reintentos cuando formen parte de hechos explícitamente
  modelados.

La trazabilidad puede utilizar:

```text
NotificationId

Version

Domain Events

timestamps

correlation

causation
```

conforme a los contratos oficiales del Aggregate.

Audit permanece fuera de Notification.

---

# Reglas Fundamentales del Aggregate

Las siguientes reglas son obligatorias:

1. Notification es la única Aggregate Root del Aggregate.
2. NotificationId es inmutable.
3. Notification posee Lifecycle propio.
4. Notification posee State Machine propia.
5. Los estados oficiales no deben inferirse fuera de su
   especificación formal.
6. Los Commands oficiales no deben inferirse desde mecanismos
   técnicos.
7. Los Domain Events oficiales deben representar hechos consumados.
8. Las referencias externas utilizan identificadores o contratos.
9. Ningún Aggregate externo se almacena dentro de Notification.
10. Notification no modifica directamente otros Aggregates.
11. Los elementos internos no pueden modificarse desde fuera.
12. Toda modificación debe ejecutarse mediante la Aggregate Root.
13. Toda modificación válida incrementa Version.
14. Una operación rechazada no modifica el estado confirmado.
15. Una operación rechazada no incrementa Version.
16. Una operación rechazada no genera Domain Events de éxito.
17. Las Invariants deben cumplirse antes y después de toda
    operación.
18. Los Read Models no modifican Notification.
19. El Repository persiste Notification como una unidad.
20. Notification no depende de Infrastructure.
21. Notification no administra autenticación.
22. Notification no almacena credenciales ni secretos.
23. Notification Management es responsable de destinatarios,
    canales, plantillas, entrega, reintentos y estado de envío.
24. El Aggregate que origina un hecho no envía directamente la
    Notification.
25. La ejecución técnica de la entrega no define por sí sola reglas
    nuevas de dominio.
26. Las extensiones no pueden romper el Consistency Boundary.

---

# Objetivos de Diseño

El Aggregate busca garantizar:

- identidad propia de cada Notification;
- separación entre hechos de dominio y comunicaciones;
- separación entre comunicación y mecanismos técnicos de entrega;
- destinatarios gestionados por Notification Management;
- canales gestionados por Notification Management;
- plantillas gestionadas por Notification Management;
- entrega bajo responsabilidad de Notification Management;
- reintentos bajo responsabilidad de Notification Management;
- estado propio de la Notification;
- Lifecycle independiente;
- encapsulamiento;
- Invariants protegidas;
- consistencia transaccional;
- trazabilidad;
- independencia tecnológica;
- interoperabilidad;
- compatibilidad con CQRS;
- compatibilidad con Event Sourcing;
- integración mediante eventos y contratos;
- evolución controlada;
- bajo acoplamiento;
- alta cohesión.

---

# Definición de Éxito

El Aggregate **Notification** representa de forma oficial,
consistente y trazable una unidad de notificación dentro del
ecosistema AURA.

Notification mantiene identidad y Consistency Boundary propios y
separa claramente:

```text
Source Domain Fact

≠

Notification

≠

Technical Delivery Mechanism
```

Notification Management conserva la responsabilidad conceptual
sobre:

```text
destinatarios

canales

plantillas

entrega

reintentos

estado de envío
```

sin absorber los Aggregates que originan las necesidades de
comunicación.

El modelo garantiza que:

- Notification posee NotificationId propio e inmutable;
- Notification posee Lifecycle propio;
- Notification posee State Machine propia;
- estados, Commands y Domain Events no se infieren implícitamente;
- otros Aggregates publican sus propios hechos;
- Notification no modifica directamente otros Aggregates;
- las referencias externas utilizan identificadores y contratos;
- las Invariants permanecen encapsuladas;
- toda modificación válida incrementa Version;
- las operaciones rechazadas conservan el estado confirmado;
- los Read Models permanecen fuera de la autoridad de escritura;
- Audit permanece fuera del Aggregate;
- los Integration Events respetan los límites entre contextos;
- los mecanismos técnicos de entrega pertenecen a capas externas;
- proveedores, protocolos y frameworks no se convierten en
  dependencias del dominio;
- CQRS y Event Sourcing permanecen compatibles;
- el Aggregate puede evolucionar sin romper sus límites de
  consistencia.

De esta forma, Notification constituye el Aggregate responsable de
representar y proteger la unidad de comunicación dentro de AURA,
manteniendo separados el hecho que origina la necesidad de
notificación, la semántica propia de Notification y los mecanismos
tecnológicos utilizados para realizar su entrega.