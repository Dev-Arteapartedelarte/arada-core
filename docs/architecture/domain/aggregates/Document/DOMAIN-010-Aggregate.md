# DOMAIN-010 — Document Aggregate

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Document Management

Aggregate:
Document

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

---

# Objetivo

El Aggregate **Document** representa una unidad documental formal
dentro del ecosistema AURA.

Document proporciona identidad, contenido, clasificación,
Lifecycle, estado, consistencia y trazabilidad propios para los
documentos utilizados por los procesos del dominio.

Un Document puede ser utilizado como soporte documental de
procesos formales desarrollados en otros Aggregates sin convertirse
en parte interna de ellos.

Entre los documentos utilizados por los procesos de AURA pueden
existir conceptualmente:

- convocatorias;
- agendas;
- actas;
- antecedentes;
- material de trabajo;
- resoluciones;
- documentos de respaldo.

Document mantiene su propio Aggregate Root y su propio
Consistency Boundary.

Los Aggregates que utilizan documentos deben mantener únicamente
las referencias necesarias mediante:

```text
DocumentId
```

No deben almacenar ni administrar directamente el contenido o
Lifecycle del Document.

---

# Propósito

El propósito del Aggregate Document es proporcionar una
representación consistente de una unidad documental con identidad
propia.

Document permite establecer:

- qué Document existe;
- cuál es su identidad;
- cuál es su naturaleza documental;
- cuál es su contenido;
- cuál es su estado;
- cuál es su Lifecycle;
- qué modificaciones relevantes ocurrieron;
- cuál es su Version;
- qué hechos de dominio produjo.

Document constituye el límite de consistencia de la unidad
documental.

No constituye el límite de consistencia de los procesos de
Organization, Assembly, Proposal, Participation, Voting,
Notification, Audit o Integration que puedan utilizarlo.

---

# Definición

Un **Document** representa una unidad documental formal reconocida
por el dominio AURA.

Document posee:

- identidad propia;
- contenido propio;
- clasificación propia;
- Lifecycle propio;
- estado propio;
- Invariants propias;
- Version propia;
- Domain Events propios;
- Consistency Boundary propio.

Document puede representar diferentes clases de documentos según
el contexto del dominio.

Ejemplos conceptuales:

```text
Convocation

Agenda

Minutes

Background

WorkMaterial

Resolution

SupportingDocument
```

Estos valores representan ejemplos conceptuales derivados de los
usos documentales reconocidos por AURA.

El conjunto oficial de DocumentType debe permanecer gobernado por
el lenguaje ubicuo de Document Management.

Document no representa:

- una Organization;
- un Citizen;
- una Membership;
- un Role;
- un Territory;
- una Assembly;
- una Proposal;
- una Participation;
- una Voting;
- una Notification;
- un Audit;
- una Integration.

Estos conceptos permanecen bajo sus respectivos Aggregates y
Bounded Contexts.

---

# Responsabilidades

El Aggregate Document es responsable de:

- mantener su identidad;
- administrar su contenido;
- mantener su clasificación documental;
- administrar su Lifecycle;
- controlar su estado;
- proteger sus Invariants;
- mantener Version;
- mantener trazabilidad de cambios relevantes;
- producir Domain Events;
- preservar su Consistency Boundary;
- representar formalmente la existencia del documento dentro del
  dominio.

Document es responsable de su propio contenido.

Un Aggregate externo que mantenga:

```text
DocumentId
```

no adquiere por ello autoridad sobre dicho contenido.

Document no administra directamente:

- Organizations;
- Citizens;
- Memberships;
- Roles;
- Territories;
- Assemblies;
- Proposals;
- Participations;
- Votings;
- Notifications;
- Audits;
- Integrations.

---

# Responsabilidades Fuera del Aggregate

No es responsabilidad de Document:

- administrar Organization;
- administrar Citizen;
- administrar Membership;
- definir Role;
- administrar Territory;
- ejecutar el Lifecycle de Assembly;
- ejecutar el Lifecycle de Proposal;
- ejecutar procesos de Participation;
- ejecutar procesos de Voting;
- enviar Notifications;
- ejecutar Audit;
- administrar Integrations externas;
- ejecutar autenticación;
- administrar sesiones;
- almacenar credenciales;
- controlar infraestructura de almacenamiento;
- definir protocolos de transporte;
- administrar formatos técnicos de persistencia.

Estas responsabilidades pertenecen a sus respectivos Aggregates,
Bounded Contexts o capas externas.

Document nunca modifica directamente el estado interno de otro
Aggregate.

---

# Aggregate Root

La única Aggregate Root es:

```text
Document
```

Toda modificación de un Document debe realizarse exclusivamente
mediante la Aggregate Root.

Ningún componente interno puede modificar directamente el estado
del Aggregate desde fuera de su Consistency Boundary.

La Aggregate Root controla:

- identidad;
- contenido;
- clasificación;
- estado;
- Lifecycle;
- Invariants;
- Version;
- producción de Domain Events.

No se exponen setters públicos para modificar directamente el
estado documental.

---

# Identidad

La identidad del Aggregate está determinada por:

```text
DocumentId
```

DocumentId:

- siempre existe;
- es único;
- es inmutable;
- nunca cambia durante la vida del Aggregate;
- nunca se sustituye como consecuencia de una modificación;
- no depende del mecanismo concreto de persistencia.

Debe mantenerse:

```text
DocumentId Before

=

DocumentId After
```

durante toda la vida del mismo Document.

El cambio de contenido, clasificación, estado o cualquier otra
propiedad válida no modifica su identidad.

---

# Propietario Organizacional

Document puede existir dentro de un contexto organizacional cuando
el proceso de dominio correspondiente así lo establezca.

La relación con Organization debe mantenerse mediante un
identificador cuando corresponda.

La existencia de una relación organizacional no convierte:

```text
Organization
```

en parte interna de Document.

Document no administra:

- identidad de Organization;
- Lifecycle de Organization;
- Memberships;
- Roles;
- reglas internas de Organization.

Las reglas específicas que determinen la obligatoriedad de una
referencia organizacional deben pertenecer a las Invariants
formales del Aggregate y no deben inferirse desde una relación
documental externa.

---

# Contexto de Assembly

Una Assembly puede utilizar Documents como soporte formal de su
proceso.

La relación establecida por AURA se mantiene mediante:

```text
DocumentId
```

Documents asociados a una Assembly pueden representar
conceptualmente:

- convocatoria;
- agenda;
- acta;
- antecedentes;
- material de trabajo;
- resoluciones;
- documentos de respaldo.

Assembly no almacena ni administra el contenido de Document.

Document conserva:

- identidad propia;
- Lifecycle propio;
- estado propio;
- contenido propio;
- Invariants propias;
- Version propia;
- Consistency Boundary propio.

Debe mantenerse:

```text
Assembly

≠

Document
```

y:

```text
DocumentId

≠

Embedded Document Aggregate
```

---

# Atributos Conceptuales

Un Document mantiene conceptualmente información equivalente a:

```text
DocumentId

DocumentType

Content

Status

Version

CreatedAt

UpdatedAt
```

Los nombres y tipos concretos de implementación deben respetar los
contratos formales definidos para Document Management.

Esta estructura no constituye autorización para exponer setters
públicos ni para persistir partes del Aggregate de manera
independiente.

---

# Descripción de Atributos

## DocumentId

Identificador único del Document.

Es obligatorio e inmutable.

---

## DocumentType

Representa la naturaleza documental del Aggregate.

Puede expresar conceptos documentales reconocidos por el dominio,
tales como:

```text
Convocation

Agenda

Minutes

Background

WorkMaterial

Resolution

SupportingDocument
```

El conjunto definitivo de valores válidos pertenece al lenguaje
ubicuo de Document Management.

DocumentType no representa:

- formato de archivo;
- protocolo;
- mecanismo de persistencia;
- tecnología de almacenamiento.

---

## Content

Representa el contenido perteneciente al Document.

Content forma parte de la responsabilidad del Aggregate Document.

Su significado pertenece al dominio documental y no debe
confundirse con el mecanismo técnico utilizado para:

- persistirlo;
- serializarlo;
- transportarlo;
- almacenarlo físicamente.

La modificación de Content debe realizarse mediante comportamiento
explícito del Aggregate y respetar sus Invariants.

---

## Status

Representa el estado actual de Document dentro de su Lifecycle.

El estado únicamente puede cambiar mediante las transiciones
formalmente reconocidas por el Aggregate.

El conjunto oficial de estados y sus transiciones se define en:

```text
DOMAIN-010A-Lifecycle.md

DOMAIN-010B-State-Machine.md
```

Ningún estado adicional debe inferirse fuera de esos contratos.

---

## Version

Número de versión utilizado por el Aggregate para representar su
evolución y soportar control de concurrencia optimista.

Toda modificación válida incrementa Version.

---

## CreatedAt

Representa el momento de creación del Document.

No cambia durante la vida del Aggregate.

---

## UpdatedAt

Representa el momento de la última modificación válida del
Aggregate.

Se actualiza únicamente como consecuencia de una modificación
aceptada por Document.

---

# Entidades Internas

Document puede contener entidades internas únicamente cuando sean
necesarias para representar conceptos cuya existencia dependa
completamente del propio Document.

Toda Entity interna:

- pertenece exclusivamente al Consistency Boundary de Document;
- no constituye una Aggregate Root independiente;
- no puede modificarse directamente desde fuera de Document;
- debe respetar las Invariants del Aggregate;
- no puede utilizarse para incorporar Aggregates externos.

La existencia de contenido documental no autoriza a convertir
automáticamente cada parte del contenido en una Entity
independiente.

Cuando un concepto requiera:

- identidad propia;
- Lifecycle propio;
- consistencia independiente;
- transacciones independientes;

debe evaluarse conforme a las reglas de diseño de Aggregates de
AURA antes de incorporarse dentro de Document.

---

# Value Objects

Entre los conceptos que pueden representarse mediante Value
Objects del dominio se consideran:

```text
DocumentType

DocumentStatus
```

Los Value Objects:

- representan conceptos del lenguaje ubicuo;
- son inmutables;
- no poseen identidad independiente;
- no pueden modificar Document directamente;
- no dependen de Infrastructure.

La representación concreta del contenido documental debe respetar
las reglas del Aggregate y no debe inferirse como Value Object,
Entity o estructura técnica sin que el modelo correspondiente lo
establezca explícitamente.

---

# Estado

El Lifecycle de Document se representa mediante:

```text
DocumentStatus
```

Todo Document debe mantener en todo momento un estado válido.

El conjunto oficial de estados pertenece a:

```text
DOMAIN-010A-Lifecycle.md

DOMAIN-010B-State-Machine.md
```

Document no admite estados implícitos.

Una implementación no puede introducir valores de estado que no
formen parte del modelo formal.

---

# Reglas de Estado

El Aggregate debe garantizar como mínimo:

- Document mantiene siempre un DocumentStatus válido;
- toda transición debe pertenecer a la State Machine;
- ninguna transición puede realizarse directamente sobre el
  atributo de estado;
- ninguna transición puede evitar las Invariants;
- una operación rechazada no modifica el estado confirmado;
- una transición válida forma parte de una modificación válida del
  Aggregate;
- toda modificación válida actualiza Version conforme al contrato
  de Versioning.

Las reglas exhaustivas se documentan en:

```text
DOMAIN-010B-State-Machine.md

DOMAIN-010E-Invariants.md
```

---

# Invariantes

El Aggregate Document mantiene como mínimo las siguientes
Invariants:

- DocumentId siempre existe;
- DocumentId nunca cambia;
- DocumentType debe ser válido;
- Content pertenece al Aggregate Document;
- DocumentStatus debe ser válido;
- toda transición debe pertenecer a la State Machine;
- ninguna modificación directa puede evitar la Aggregate Root;
- toda modificación válida incrementa Version;
- una operación rechazada no modifica el estado confirmado;
- una operación rechazada no produce el Domain Event de éxito;
- las Invariants deben mantenerse antes y después de cada
  operación válida;
- las relaciones con otros Aggregates utilizan identificadores;
- Document no modifica directamente otros Aggregates.

Las reglas completas se desarrollan en:

```text
DOMAIN-010E-Invariants.md
```

---

# Relaciones

Document mantiene su independencia respecto de los demás
Aggregates de AURA.

Las relaciones externas deben utilizar identificadores y contratos
explícitos.

Conceptualmente:

```text
Document
    │
    └──────── DocumentId
                 │
                 └──────── External Aggregate Reference
```

La referencia a Document desde otro Aggregate no implica:

- composición;
- ownership del contenido;
- acceso directo al estado interno;
- autoridad para ejecutar su Lifecycle.

Document no almacena Aggregates externos completos.

---

# Organization y Document

Cuando un Document se encuentre relacionado con una Organization,
dicha relación debe mantenerse mediante identificadores y contratos
del dominio.

Organization conserva:

- su identidad;
- su Lifecycle;
- sus Invariants;
- su Repository;
- su Consistency Boundary.

Document no administra Organization.

---

# Citizen y Document

Citizen mantiene su propia identidad y Lifecycle.

Document no administra Citizen.

Una relación futura entre ambos conceptos no puede resolverse
incorporando el Aggregate Citizen dentro de Document.

Las referencias, cuando correspondan, deben utilizar
identificadores.

---

# Membership y Document

Membership permanece fuera del Consistency Boundary de Document.

Document no crea, activa, suspende ni termina Memberships.

Las reglas de pertenencia organizacional permanecen bajo el
Aggregate Membership.

---

# Role y Document

Role permanece fuera del Consistency Boundary de Document.

Document no crea ni modifica Roles.

Las reglas de autorización que utilicen Roles no convierten Role
en parte del estado interno del Document.

---

# Territory y Document

Territory conserva su propio Aggregate Root y su propio
Consistency Boundary.

Document no administra:

- jerarquía territorial;
- clasificación territorial;
- geometría;
- estado territorial.

Cualquier relación territorial que pueda definirse deberá
mantenerse mediante identificadores y contratos explícitos.

---

# Assembly y Document

Assembly puede mantener:

```text
DocumentId
```

para asociar documentos formales a su contexto.

Los Documents pueden representar, entre otros:

- convocatorias;
- agendas;
- actas;
- antecedentes;
- material de trabajo;
- resoluciones;
- documentos de respaldo.

Assembly no almacena el contenido del Document.

Assembly no administra el Lifecycle de Document.

Document no administra el Lifecycle de Assembly.

---

# Proposal y Document

Proposal permanece fuera del Consistency Boundary de Document.

Document no administra:

- identidad de Proposal;
- Lifecycle de Proposal;
- estado de Proposal;
- Invariants de Proposal.

Cualquier relación futura debe mantenerse mediante identificadores
y contratos explícitos.

---

# Participation y Document

Participation permanece fuera del Consistency Boundary de
Document.

Document no administra el historial ni Lifecycle de Participation.

Una relación documental con Participation no convierte dicha
Participation en una Entity interna de Document.

---

# Voting y Document

Voting posee:

- identidad propia;
- Lifecycle propio;
- State Machine propia;
- Invariants propias;
- Version propia;
- Consistency Boundary propio.

Document no ejecuta ni modifica el proceso de Voting.

Cualquier relación documental con Voting debe mantenerse mediante
identificadores y contratos explícitos.

---

# Notification y Document

Los hechos de Document pueden producir necesidades posteriores de
Notification cuando los contratos del dominio así lo establezcan.

Document no envía Notifications directamente.

Notification permanece fuera del Consistency Boundary de Document.

---

# Audit y Document

Las modificaciones relevantes de Document pueden producir
información utilizada por Audit.

Audit no forma parte del Aggregate Document.

Document no administra Audit Records.

La trazabilidad se establece mediante Domain Events,
Integration Events, identificadores, Version e información
temporal conforme a los contratos de AURA.

---

# Consistencia

Document constituye un límite de consistencia independiente.

Todas las modificaciones internas deben respetar:

- una única Aggregate Root;
- una única operación válida de dominio;
- Invariants válidas;
- transición válida cuando exista cambio de estado;
- control de Version;
- generación coherente de Domain Events.

No existen actualizaciones parciales que puedan dejar Document en
un estado inválido.

Toda operación válida debe finalizar con un Aggregate consistente.

La consistencia dentro de Document es inmediata.

La coordinación con otros Aggregates permanece fuera de su
Consistency Boundary.

---

# Límite de Consistencia

El Consistency Boundary de Document comprende:

```text
Document
    │
    ├── Internal State
    ├── Content
    ├── Internal Entities
    ├── Value Objects
    └── Version
```

No comprende:

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

Estos conceptos permanecen fuera del límite.

La definición formal se desarrolla en:

```text
DOMAIN-010J-Consistency-Boundary.md
```

---

# Commands

Document responde a Commands que expresan intenciones del dominio
documental.

Todo Command:

- expresa intención;
- es validado por la Aggregate Root;
- debe respetar el estado actual;
- debe respetar el Lifecycle;
- debe respetar las Invariants;
- solamente produce modificaciones cuando el Aggregate las acepta;
- puede producir Domain Events.

El conjunto oficial de Commands se define formalmente en:

```text
DOMAIN-010C-Commands.md
```

Ninguna operación técnica de persistencia o transporte constituye
por sí misma un Command de Document.

---

# Operaciones Públicas

La Aggregate Root expone exclusivamente comportamiento de dominio.

Las operaciones públicas:

- actúan sobre Document;
- validan las Invariants correspondientes;
- preservan DocumentId;
- preservan el Consistency Boundary;
- controlan cualquier modificación de Content;
- controlan cualquier cambio de DocumentStatus;
- incrementan Version cuando producen una modificación válida;
- generan los Domain Events correspondientes.

No se exponen setters públicos.

No se permite modificar directamente:

```text
documentId

content

status

version
```

El contrato completo de operaciones se deriva de:

```text
DOMAIN-010C-Commands.md
```

---

# Eventos del Dominio

Document produce Domain Events cuando ocurre un hecho relevante y
aceptado dentro de su propio Consistency Boundary.

Los Domain Events:

- representan hechos consumados;
- pertenecen a Document;
- no representan Commands;
- preservan la identidad del Aggregate;
- mantienen relación coherente con AggregateVersion;
- conservan significado histórico.

El conjunto oficial de Domain Events se define en:

```text
DOMAIN-010D-Domain-Events.md
```

Un hecho no debe publicarse como Domain Event de éxito cuando la
operación que lo originaría fue rechazada.

---

# Ciclo de Vida

Document posee un Lifecycle propio e independiente de los
Aggregates que puedan utilizarlo.

El Lifecycle controla la evolución formal de:

```text
DocumentStatus
```

Las rutas exactas, estados y condiciones de transición no deben
inferirse desde relaciones con Assembly, Proposal, Voting u otros
Aggregates.

Se encuentran formalmente definidos en:

```text
DOMAIN-010A-Lifecycle.md

DOMAIN-010B-State-Machine.md
```

El cambio de estado de un Aggregate externo no cambia
automáticamente DocumentStatus.

Del mismo modo, un cambio de DocumentStatus no modifica
directamente el estado de otro Aggregate.

---

# Reglas de Modificación

Toda modificación de Document debe cumplir:

- ninguna modificación directa de atributos;
- ninguna modificación fuera de la Aggregate Root;
- ninguna modificación de DocumentId;
- ninguna modificación que viole la State Machine;
- ninguna modificación que deje Document en un estado inválido;
- ninguna modificación de Content que evite las Invariants;
- toda modificación válida incrementa Version;
- toda modificación relevante produce el Domain Event
  correspondiente;
- una operación rechazada conserva el estado confirmado;
- Document nunca modifica directamente otro Aggregate.

Las reglas detalladas se encuentran en:

```text
DOMAIN-010E-Invariants.md
```

---

# Fuente de Verdad

La fuente de verdad de Document es el Aggregate Document y,
cuando corresponda, su historial de Domain Events.

Los Read Models:

- son representaciones derivadas;
- pueden reconstruirse;
- no constituyen fuente de verdad;
- no poseen autoridad para modificar Document.

Debe mantenerse:

```text
Document Aggregate

=

Write Authority
```

---

# Persistencia

El Repository persiste Document como una unidad de consistencia.

Conceptualmente:

```text
Document
    │
    ├── State
    ├── Content
    ├── Value Objects
    ├── Internal Entities
    └── Version
```

No deben persistirse partes del Aggregate de forma independiente
mediante operaciones que permitan violar sus Invariants.

El dominio no conoce el mecanismo técnico utilizado para almacenar
Content.

El Repository Contract formal se define en:

```text
DOMAIN-010G-Repository-Contract.md
```

---

# Versionado

Document utiliza el modelo de Versioning consolidado de AURA.

Toda modificación válida incrementa:

```text
Version
```

Version pertenece al Aggregate.

El Repository debe verificar conceptualmente que la versión
esperada corresponda a la versión persistida antes de aceptar una
escritura.

Ante una concurrencia incompatible:

```text
ConcurrencyConflict
```

debe aplicarse el comportamiento definido por el Repository
Contract.

Una operación rechazada no incrementa Version.

Una operación de lectura no incrementa Version.

La especificación formal pertenece a:

```text
DOMAIN-010I-Versioning.md
```

---

# Seguridad

Document no administra autenticación.

Document no almacena:

- contraseñas;
- tokens;
- claves privadas;
- secretos criptográficos;
- credenciales;
- sesiones.

La autorización de las operaciones se evalúa mediante las
políticas y Permissions definidas por AURA.

Una intención autorizada continúa sujeta a:

- Lifecycle;
- State Machine;
- Invariants;
- Versioning.

Debe mantenerse:

```text
Permission Granted

≠

Domain Operation Guaranteed
```

Las reglas formales se definen en:

```text
DOMAIN-010F-Permissions.md

DOMAIN-010O-Security-Model.md
```

---

# Permisos

Las Permissions determinan quién puede solicitar determinadas
operaciones sobre Document.

Las Permissions:

- no modifican el Lifecycle;
- no modifican la State Machine;
- no sustituyen las Invariants;
- no permiten modificar directamente Content;
- no permiten modificar directamente Version;
- no amplían el Consistency Boundary.

El conjunto oficial de Permissions se define en:

```text
DOMAIN-010F-Permissions.md
```

---

# Integración

Document puede participar en procesos pertenecientes a otros
Bounded Contexts mediante identificadores y contratos explícitos.

Document Management puede relacionarse conceptualmente con:

- Organization Management;
- Assembly Management;
- Proposal Management;
- Participation Management;
- Voting Management;
- Notification Management;
- Audit;
- Integration.

Estas relaciones no deben introducir dependencias directas sobre
la implementación interna de otro Aggregate.

Los sistemas externos no acceden directamente al estado interno
de Document.

---

# Integration Events

Los hechos de dominio que necesiten cruzar el Bounded Context
pueden transformarse en Integration Events conforme al contrato de
AURA.

Los Integration Events:

- derivan de hechos confirmados;
- no reemplazan Domain Events;
- no forman parte del estado interno de Document;
- no modifican Document;
- no incrementan Version;
- no amplían el Consistency Boundary;
- representan contratos de integración.

El conjunto oficial se define en:

```text
DOMAIN-010K-Integration-Events.md
```

No debe inferirse automáticamente un Integration Event por cada
Domain Event.

---

# Read Model

Document puede disponer de Read Models especializados para
consulta.

Los Read Models:

- son proyecciones;
- pueden reconstruirse;
- no son Aggregates;
- no constituyen fuente de verdad;
- no ejecutan Commands;
- no poseen autoridad para modificar Document;
- pueden optimizarse para necesidades de consulta.

La existencia de una necesidad de consulta no debe ampliar
innecesariamente el Aggregate.

El conjunto oficial de Read Models se define en:

```text
DOMAIN-010L-Read-Model.md
```

---

# Rendimiento

Document debe mantenerse enfocado en la consistencia de su propia
unidad documental.

No debe cargar Aggregates externos completos para ejecutar
operaciones ordinarias.

Debe utilizar:

- identificadores;
- Value Objects;
- contratos explícitos;
- Read Models para consultas.

El mecanismo técnico utilizado para persistir o recuperar Content
no altera las reglas del dominio.

Las consultas complejas deben resolverse mediante Read Models y no
mediante expansión innecesaria del Aggregate.

Las reglas específicas se encuentran en:

```text
DOMAIN-010N-Performance-Rules.md
```

---

# Extensibilidad

Document debe permitir evolución controlada sin romper su
Consistency Boundary.

Los puntos de extensión pueden incluir:

```text
DocumentType

Domain Events

Integration Events

Read Models

Value Objects

Domain Policies
```

Las extensiones no deben:

- modificar retrospectivamente DocumentId;
- romper Invariants existentes;
- introducir estados implícitos;
- introducir transiciones implícitas;
- introducir dependencias con Infrastructure;
- convertir otros Aggregates en Entities internas;
- crear acoplamiento directo con sistemas externos;
- modificar hechos históricos confirmados.

La especificación formal pertenece a:

```text
DOMAIN-010P-Extension-Points.md
```

---

# Compatibilidad Arquitectónica

Document está diseñado para mantener compatibilidad con:

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

Document pertenece al dominio.

No depende de tecnologías concretas de Infrastructure.

---

# Dependencias

Document depende conceptualmente de:

- Shared Kernel;
- Value Objects;
- Domain Events;
- Repository Contracts;
- contratos de dominio definidos por AURA.

Document no depende directamente de:

```text
Infrastructure

Frameworks

Bases de datos

File Systems

Object Storage

HTTP

REST

GraphQL

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

El contenido de un Document pertenece al dominio.

El mecanismo utilizado para almacenarlo no pertenece al Aggregate.

---

# Relaciones Estratégicas

Document Management proporciona la responsabilidad documental para
los procesos de AURA que requieran unidades documentales con
identidad, contenido y Lifecycle propios.

Document puede ser utilizado estratégicamente por contextos como:

- Assembly Management;
- Proposal Management;
- Participation Management;
- Voting Management;
- Notification Management;
- Audit;
- Integration.

La relación confirmada con Assembly permite que Documents
representen:

- convocatorias;
- agendas;
- actas;
- antecedentes;
- material de trabajo;
- resoluciones;
- documentos de respaldo.

Ningún consumidor adquiere propiedad sobre el estado interno de
Document por mantener DocumentId.

---

# CQRS

Document es compatible con CQRS.

En el lado de escritura:

```text
Command
   │
   ▼
Document Aggregate
   │
   ├── Invariants
   ├── State Transition
   ├── Content
   ├── Version
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

El Read Side no posee autoridad para modificar Content,
DocumentStatus o Version.

---

# Event Sourcing

Document es compatible conceptualmente con Event Sourcing.

Los Domain Events pueden representar la evolución histórica del
Aggregate cuando la arquitectura adoptada por AURA utilice dicho
mecanismo.

Conceptualmente:

```text
Domain Event History

↓

Document
```

El historial debe permanecer inmutable.

Los eventos representan hechos ocurridos.

No representan instrucciones futuras.

La implementación concreta de Event Sourcing pertenece a
Infrastructure y no debe introducirse dentro del modelo de
dominio.

---

# Trazabilidad

Document debe permitir reconstruir conceptualmente:

- su identidad;
- su clasificación documental;
- su estado;
- las modificaciones relevantes de Content;
- las modificaciones relevantes de su Lifecycle;
- qué Version produjo cada modificación;
- qué hechos de dominio ocurrieron.

La trazabilidad no convierte Audit en una Entity interna de
Document.

Audit permanece separado y puede consumir hechos mediante los
contratos establecidos por AURA.

---

# Reglas de Diseño del Aggregate

Document debe respetar:

- una única Aggregate Root;
- identidad única e inmutable;
- alto nivel de cohesión;
- bajo acoplamiento;
- Invariants protegidas;
- comportamiento de dominio explícito;
- ausencia de setters públicos;
- Content protegido por la Aggregate Root;
- referencias externas mediante identificadores;
- ausencia de Aggregates externos completos;
- consistencia interna inmediata;
- separación de consistencia entre Aggregates;
- Domain Events para hechos del dominio;
- Integration Events para integración externa;
- Read Models para consultas;
- Repository Contract para persistencia;
- Versionado Optimista para concurrencia;
- independencia tecnológica.

---

# Escenarios de Uso Conceptuales

Document debe poder representar escenarios documentales como:

## Documento de Convocatoria

Una Assembly mantiene DocumentId para referenciar un Document que
representa formalmente su convocatoria.

Assembly no almacena el contenido de dicho Document.

## Documento de Agenda

Una Assembly puede asociar un Document utilizado para representar
su agenda.

Document conserva identidad y Lifecycle propios.

## Acta

Una Assembly puede mantener una referencia a un Document que
representa su acta.

El contenido del acta pertenece al Aggregate Document.

## Antecedente

Un Document puede representar antecedentes utilizados por una
Assembly sin convertirse en parte interna del Aggregate Assembly.

## Material de Trabajo

Un Document puede representar material de trabajo asociado a un
proceso formal.

El proceso que lo referencia mantiene únicamente DocumentId.

## Resolución

Un Document puede representar una resolución formal.

La existencia del Document no modifica automáticamente el estado
de Assembly, Proposal, Voting u otro Aggregate.

## Documento de Respaldo

Un Document puede actuar como respaldo documental de un proceso
manteniendo identidad, contenido y Lifecycle propios.

---

# Restricciones Arquitectónicas

No está permitido:

- convertir Organization en Entity interna de Document;
- convertir Citizen en Entity interna de Document;
- convertir Membership en Entity interna de Document;
- convertir Role en Entity interna de Document;
- convertir Territory en Entity interna de Document;
- convertir Assembly en Entity interna de Document;
- convertir Proposal en Entity interna de Document;
- convertir Participation en Entity interna de Document;
- convertir Voting en Entity interna de Document;
- almacenar Aggregates externos completos dentro de Document;
- modificar DocumentId;
- modificar DocumentStatus directamente;
- modificar Version directamente;
- modificar Content evitando la Aggregate Root;
- acceder directamente a Repositories de otros Aggregates desde
  Document;
- realizar llamadas HTTP desde el Aggregate;
- acceder directamente a bases de datos desde el Aggregate;
- acceder directamente a mecanismos de almacenamiento desde el
  Aggregate;
- ejecutar lógica de Infrastructure dentro del Aggregate;
- enviar Notifications directamente desde el Aggregate;
- ejecutar integraciones externas directamente desde el Aggregate;
- modificar el estado de otro Aggregate dentro de la misma
  operación interna de Document;
- convertir el mecanismo técnico de almacenamiento del contenido
  en una regla del dominio.

---

# Objetivos de Diseño

El Aggregate busca garantizar:

- identidad formal del Document;
- propiedad del contenido dentro del Aggregate;
- consistencia de su Lifecycle;
- consistencia de su estado;
- clasificación documental coherente;
- protección de Invariants;
- trazabilidad;
- Versioning;
- independencia tecnológica;
- interoperabilidad;
- bajo acoplamiento;
- alta cohesión;
- evolución controlada;
- compatibilidad con CQRS;
- compatibilidad con Event Sourcing;
- separación entre Document y los procesos que lo referencian.

---

# Definición de Éxito

El Aggregate **Document** representa formalmente una unidad
documental con identidad, contenido, clasificación, Lifecycle,
estado, Invariants, Version y Consistency Boundary propios dentro
del ecosistema AURA.

Document mantiene la responsabilidad exclusiva sobre su contenido
documental.

Los demás Aggregates utilizan:

```text
DocumentId
```

para establecer relaciones sin almacenar ni administrar
directamente el contenido o Lifecycle del Document.

Document puede representar documentos formales como:

- convocatorias;
- agendas;
- actas;
- antecedentes;
- material de trabajo;
- resoluciones;
- documentos de respaldo.

La relación con Assembly preserva la independencia entre ambos
Aggregates.

Document mantiene una única Aggregate Root, identidad inmutable,
Invariants protegidas, Versioning y trazabilidad.

La colaboración con otros Bounded Contexts se realiza mediante
identificadores, Domain Events, Integration Events y contratos
explícitos.

El diseño mantiene los principios consolidados de Domain-Driven
Design, Clean Architecture, Hexagonal Architecture, CQRS y
Event-Driven Architecture sin introducir dependencias tecnológicas
dentro del dominio.