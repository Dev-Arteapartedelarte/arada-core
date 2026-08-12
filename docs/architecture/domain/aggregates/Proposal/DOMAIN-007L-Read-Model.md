# DOMAIN-007L — Proposal Read Model

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Proposal Management

Aggregate:
Proposal

Autor:
ARADA

Documentos relacionados:

- DOMAIN-007-Aggregate.md
- DOMAIN-007A-Lifecycle.md
- DOMAIN-007B-State-Machine.md
- DOMAIN-007C-Commands.md
- DOMAIN-007D-Domain-Events.md
- DOMAIN-007E-Invariants.md
- DOMAIN-007F-Permissions.md
- DOMAIN-007G-Repository-Contract.md
- DOMAIN-007H-Examples.md
- DOMAIN-007I-Versioning.md
- DOMAIN-007J-Consistency-Boundary.md
- DOMAIN-007K-Integration-Events.md
- CORE-003-Shared-Kernel.md
- CORE-004-Ubiquitous-Language.md
- CORE-005-Domain-Events.md
- CORE-006-Domain-Invariants.md
- CORE-007-Strategic-Design.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Este documento define el modelo oficial de lectura
(**Read Model**) del Aggregate **Proposal**.

Los Read Models representan vistas especializadas y optimizadas
para consulta, visualización, búsqueda, seguimiento y análisis de
Proposals.

No contienen lógica de negocio.

No modifican el Aggregate.

No forman parte del límite de consistencia de Proposal.

Su propósito es proporcionar modelos de consulta eficientes y
escalables sin comprometer la consistencia del lado de escritura
ni convertir las necesidades de lectura en responsabilidades del
Aggregate.

---

# Propósito

El Read Model de Proposal permite representar información derivada
del dominio para satisfacer necesidades de lectura como:

- listar Proposals;
- consultar una Proposal;
- buscar Proposals;
- filtrar Proposals;
- consultar Proposals por Organization;
- consultar Proposals por Territory;
- consultar Proposals relacionadas con una Assembly;
- consultar Proposals por estado;
- consultar Proposals por tipo;
- consultar Proposals por proponente;
- consultar Proposals pendientes de revisión;
- consultar Proposals aceptadas;
- consultar Proposals rechazadas;
- consultar Proposals retiradas;
- consultar Proposals archivadas;
- consultar actividad reciente;
- construir dashboards;
- construir indicadores;
- generar estadísticas;
- alimentar vistas de seguimiento;
- proporcionar información de consulta para integraciones cuando
  corresponda.

Estas necesidades no modifican el modelo de escritura de
Proposal.

---

# Principios

Los Read Models de Proposal siguen los siguientes principios:

- son derivados del dominio;
- son reconstruibles;
- son de solo lectura;
- están desacoplados del Aggregate;
- no contienen lógica de negocio;
- no protegen invariantes;
- no ejecutan Commands;
- no modifican Proposal;
- pueden desnormalizar información;
- pueden mantener estructuras optimizadas para consulta;
- pueden existir múltiples proyecciones para un mismo Aggregate;
- pueden evolucionar independientemente del modelo de escritura;
- utilizan consistencia eventual;
- pueden reconstruirse a partir de hechos del dominio;
- respetan el lenguaje ubicuo de AURA;
- no constituyen la fuente oficial de verdad del Aggregate.

---

# Arquitectura

```text
                    Commands

                        │

                        ▼

                Proposal Aggregate

                        │

                 Domain Events

                        │

                        ▼

                 Projection Engine

                        │

        ┌───────────────┼────────────────┐
        │               │                │
        ▼               ▼                ▼

 Proposal View     Dashboard         Analytics

        │               │                │
        ▼               ▼                ▼

 Search Models    Operational       Statistical
                    Views              Views
```

El lado de escritura mantiene las reglas del dominio.

El lado de lectura mantiene representaciones derivadas optimizadas
para consulta.

---

# Fuente de Verdad

La única fuente oficial de verdad para el estado del Aggregate es:

```text
Proposal Aggregate
```

y, cuando la arquitectura correspondiente utilice historial de
eventos:

```text
Domain Events
```

Los Read Models no sustituyen al Aggregate.

Debe mantenerse:

```text
Proposal Aggregate

=

Authoritative Write Model
```

mientras:

```text
Proposal Read Models

=

Derived Query Models
```

Una proyección puede eliminarse y reconstruirse sin modificar la
identidad ni el estado válido del Aggregate.

---

# Separación entre Write Model y Read Model

El modelo de escritura y el modelo de lectura poseen
responsabilidades diferentes.

```text
Write Model

Proposal Aggregate
```

es responsable de:

- comportamiento;
- invariantes;
- transiciones;
- Lifecycle;
- State Machine;
- consistencia;
- Domain Events;
- Version.

```text
Read Model
```

es responsable de:

- consultas;
- vistas;
- búsquedas;
- filtros;
- ordenamiento;
- paginación;
- agregaciones;
- estadísticas;
- dashboards;
- representación optimizada.

Debe mantenerse:

```text
Write Model

≠

Read Model
```

---

# Regla de No Modificación

Ningún Read Model puede modificar Proposal.

No está permitido:

```text
Read Model

↓

Change Proposal
```

Toda modificación debe seguir el flujo oficial:

```text
Command

↓

Proposal Aggregate

↓

Domain Rules

↓

Domain Event
```

Los Read Models permanecen exclusivamente en el lado de lectura.

---

# Regla de No Lógica de Negocio

Los Read Models no implementan decisiones pertenecientes al
Aggregate.

No deben decidir:

- si una Proposal puede ser presentada;
- si una Proposal puede entrar en revisión;
- si una Proposal puede ser aceptada;
- si una Proposal puede ser rechazada;
- si una Proposal puede ser retirada;
- si una Proposal puede archivarse;
- si una transición de estado es válida;
- si una invariante se cumple;
- si un actor puede ejecutar un Command.

Estas decisiones pertenecen al modelo correspondiente del dominio
y de autorización.

---

# Proyecciones Oficiales

El Bounded Context Proposal mantiene conceptualmente las
siguientes proyecciones:

```text
ProposalSummary

ProposalDetail

ProposalDirectory

ProposalStatus

ProposalOrganization

ProposalTerritory

ProposalAssembly

ProposalProposer

ProposalReview

ProposalActivity

ProposalStatistics
```

Cada proyección responde a una necesidad de consulta específica.

No todas las consultas requieren cargar una representación
completa de Proposal.

---

# ProposalSummary

Vista utilizada para listados rápidos y presentación resumida de
Proposals.

Campos conceptuales:

```text
ProposalId

OrganizationId

Title

ProposalType

ProposalStatus

TerritoryId

AssemblyId

ProposerReference

CreatedAt

SubmittedAt

UpdatedAt

Version
```

Los campos opcionales se incluyen únicamente cuando existan en el
contexto real de la Proposal.

Uso:

- listados;
- paneles;
- resultados de búsqueda;
- selección de Proposals;
- vistas administrativas;
- vistas comunitarias;
- actividad reciente.

ProposalSummary no representa el Aggregate completo.

---

# ProposalDetail

Vista detallada destinada a la consulta de una Proposal
específica.

Campos conceptuales:

```text
ProposalId

OrganizationId

Title

Description

ProposalType

ProposalStatus

ProposerReference

TerritoryId

AssemblyId

CreatedAt

SubmittedAt

ReviewStartedAt

AcceptedAt

RejectedAt

WithdrawnAt

ArchivedAt

UpdatedAt

Version
```

Los valores temporales dependen de los hechos efectivamente
ocurridos durante el Lifecycle.

Uso:

- vista detallada;
- panel administrativo;
- seguimiento de Proposal;
- consulta comunitaria;
- interfaces de revisión;
- visualización del estado actual.

La vista puede contener información derivada para presentación,
pero no modifica las reglas del dominio.

---

# ProposalDirectory

Vista optimizada para búsquedas y filtros.

Campos indexables conceptuales:

```text
ProposalId

OrganizationId

Title

ProposalType

ProposalStatus

ProposerReference

TerritoryId

AssemblyId

CreatedAt

SubmittedAt

UpdatedAt
```

Uso:

- búsqueda rápida;
- autocompletado;
- filtros;
- exploración de Proposals;
- búsqueda por Organization;
- búsqueda por Territory;
- búsqueda por Assembly;
- búsqueda por estado;
- búsqueda por tipo;
- búsqueda por proponente.

La estructura física de índices pertenece a Infrastructure.

---

# ProposalStatus

Vista especializada en el estado operativo y Lifecycle de una
Proposal.

Campos conceptuales:

```text
ProposalId

ProposalStatus

CreatedAt

SubmittedAt

ReviewStartedAt

AcceptedAt

RejectedAt

WithdrawnAt

ArchivedAt

Version
```

Uso:

- seguimiento;
- validaciones de consulta;
- dashboards;
- indicadores operativos;
- vistas de estado;
- monitoreo del Lifecycle.

ProposalStatus representa información derivada.

No controla la State Machine.

---

# ProposalOrganization

Vista especializada en la relación entre Proposal y
Organization.

Campos conceptuales:

```text
ProposalId

OrganizationId

Title

ProposalType

ProposalStatus

CreatedAt

SubmittedAt

UpdatedAt
```

Uso:

- Proposals por Organization;
- dashboards organizacionales;
- listados internos;
- estadísticas organizacionales;
- seguimiento de actividad.

Organization continúa siendo un Aggregate independiente.

Esta proyección no incorpora Organization dentro de Proposal.

---

# ProposalTerritory

Vista especializada en el contexto territorial de las Proposals.

Campos conceptuales:

```text
ProposalId

OrganizationId

TerritoryId

Title

ProposalType

ProposalStatus

CreatedAt

SubmittedAt
```

Uso:

- Proposals por territorio;
- mapas;
- planificación territorial;
- indicadores territoriales;
- estadísticas;
- análisis comunitario;
- interoperabilidad territorial.

Territory continúa siendo un Aggregate independiente.

La proyección puede combinar información destinada a consulta sin
alterar los límites del dominio.

---

# ProposalAssembly

Vista especializada en Proposals relacionadas con una Assembly.

Campos conceptuales:

```text
ProposalId

AssemblyId

OrganizationId

Title

ProposalType

ProposalStatus

SubmittedAt

UpdatedAt
```

Uso:

- Proposals asociadas a una Assembly;
- agendas;
- vistas de deliberación;
- seguimiento de materias;
- interfaces de participación.

Assembly mantiene su propia identidad y Consistency Boundary.

La existencia de esta proyección no convierte Proposal en una
entidad interna de Assembly ni Assembly en una entidad interna de
Proposal.

---

# ProposalProposer

Vista especializada en la relación entre una Proposal y la
referencia de dominio correspondiente a su proponente.

Campos conceptuales:

```text
ProposalId

OrganizationId

ProposerReference

Title

ProposalType

ProposalStatus

CreatedAt

SubmittedAt
```

Uso:

- consultar Proposals por proponente;
- actividad de participación;
- historial de propuestas;
- vistas organizacionales;
- indicadores.

ProposerReference puede representar la referencia establecida por
el modelo de Proposal, como:

```text
CitizenId
```

o:

```text
MembershipId
```

según corresponda.

El Read Model no redefine esta relación.

---

# ProposalReview

Vista especializada en procesos de revisión de Proposal.

Campos conceptuales:

```text
ProposalId

OrganizationId

Title

ProposalType

ProposalStatus

SubmittedAt

ReviewStartedAt

AcceptedAt

RejectedAt

UpdatedAt

Version
```

Uso:

- bandejas de revisión;
- Proposals pendientes;
- Proposals bajo revisión;
- seguimiento de decisiones;
- métricas de revisión;
- dashboards administrativos.

ProposalReview no ejecuta la revisión.

No acepta ni rechaza Proposals.

Representa información derivada del proceso ya ocurrido en el
lado de escritura.

---

# ProposalActivity

Vista orientada a actividad y evolución reciente de Proposals.

Campos conceptuales:

```text
ProposalId

OrganizationId

ProposalStatus

ActivityType

OccurredAt

Version
```

Puede derivarse de hechos como:

```text
ProposalCreated

ProposalSubmitted

ProposalReviewStarted

ProposalAccepted

ProposalRejected

ProposalWithdrawn

ProposalArchived
```

Uso:

- actividad reciente;
- timeline;
- dashboards;
- seguimiento;
- visualización histórica resumida.

ProposalActivity no sustituye el historial oficial de Domain
Events.

---

# ProposalStatistics

Vista agregada destinada a análisis e indicadores.

Ejemplos conceptuales:

```text
Total Proposals

Draft Proposals

Submitted Proposals

Proposals Under Review

Accepted Proposals

Rejected Proposals

Withdrawn Proposals

Archived Proposals

Proposals per Organization

Proposals per Territory

Proposals per Assembly

Proposals per Type

Proposals per Proposer

Proposal Submission Rate

Proposal Acceptance Rate

Proposal Rejection Rate

Proposal Withdrawal Rate

Average Review Time

Proposal Growth Rate
```

Uso:

- BI;
- KPIs;
- dashboards ejecutivos;
- planificación;
- gobierno abierto;
- análisis territorial;
- análisis de participación;
- reportes organizacionales.

Las estadísticas son información derivada.

No constituyen reglas del Aggregate.

---

# Actualización

Los Read Models se actualizan a partir de hechos confirmados del
dominio.

Conceptualmente:

```text
ProposalCreated

↓

Projection

↓

Proposal Read Models
```

```text
ProposalSubmitted

↓

Projection

↓

Proposal Read Models
```

```text
ProposalReviewStarted

↓

Projection

↓

Proposal Read Models
```

```text
ProposalAccepted

↓

Projection

↓

Proposal Read Models
```

```text
ProposalRejected

↓

Projection

↓

Proposal Read Models
```

```text
ProposalWithdrawn

↓

Projection

↓

Proposal Read Models
```

```text
ProposalArchived

↓

Projection

↓

Proposal Read Models
```

Cada evento actualiza únicamente las proyecciones afectadas.

---

# Matriz de Actualización Conceptual

```text
Domain Event                    Proyecciones principales

ProposalCreated                 ProposalSummary
                                ProposalDetail
                                ProposalDirectory
                                ProposalStatus
                                ProposalOrganization
                                ProposalTerritory
                                ProposalAssembly
                                ProposalProposer
                                ProposalActivity
                                ProposalStatistics

ProposalSubmitted               ProposalSummary
                                ProposalDetail
                                ProposalDirectory
                                ProposalStatus
                                ProposalReview
                                ProposalActivity
                                ProposalStatistics

ProposalReviewStarted           ProposalDetail
                                ProposalStatus
                                ProposalReview
                                ProposalActivity
                                ProposalStatistics

ProposalAccepted                ProposalSummary
                                ProposalDetail
                                ProposalDirectory
                                ProposalStatus
                                ProposalReview
                                ProposalActivity
                                ProposalStatistics

ProposalRejected                ProposalSummary
                                ProposalDetail
                                ProposalDirectory
                                ProposalStatus
                                ProposalReview
                                ProposalActivity
                                ProposalStatistics

ProposalWithdrawn               ProposalSummary
                                ProposalDetail
                                ProposalDirectory
                                ProposalStatus
                                ProposalActivity
                                ProposalStatistics

ProposalArchived                ProposalSummary
                                ProposalDetail
                                ProposalDirectory
                                ProposalStatus
                                ProposalActivity
                                ProposalStatistics
```

La matriz expresa las principales relaciones conceptuales.

Una implementación puede actualizar otras proyecciones afectadas
siempre que no altere el significado del dominio.

---

# Flujo de Proyección

El flujo conceptual de actualización es:

```text
Command

↓

Proposal Aggregate

↓

Domain Event

↓

Commit

↓

Projection Engine

↓

Affected Read Models
```

La proyección ocurre después de que el hecho del dominio ha sido
confirmado.

---

# Regla de Confirmación

Un Read Model no debe representar como confirmado un cambio que el
Aggregate todavía no ha aceptado.

Debe mantenerse:

```text
Validate

↓

Modify Proposal

↓

Persist

↓

Commit

↓

Project
```

No:

```text
Project

↓

Attempt Domain Modification
```

---

# Command Rechazado

Cuando un Command es rechazado:

```text
Command

↓

Rejected
```

entonces:

```text
No State Change

No Confirmed Domain Event

No Projection Update
```

El Read Model no debe representar un hecho inexistente.

---

# Reconstrucción

Todas las proyecciones pueden regenerarse.

Proceso conceptual:

```text
Replay

↓

Domain Events

↓

Projection Engine

↓

Proposal Read Models
```

La reconstrucción no modifica Proposal.

No genera nuevos hechos de dominio.

No ejecuta Commands.

No incrementa Version del Aggregate.

No cambia el Lifecycle.

No cambia la State Machine.

---

# Regla de Reconstrucción

Una reconstrucción completa debe producir una representación
equivalente a la derivada del mismo conjunto válido de eventos.

Conceptualmente:

```text
Same Domain History

↓

Same Logical Projection State
```

La representación física puede variar según la infraestructura,
pero el significado de la información debe mantenerse.

---

# Reproyección

Una proyección puede reconstruirse cuando:

- cambia su estructura;
- se incorpora una nueva vista;
- se corrige una proyección;
- se requiere regenerar índices;
- se necesita reconstruir estadísticas;
- se modifica una necesidad de consulta compatible con los hechos
  disponibles.

La reproyección no modifica el historial del Aggregate.

---

# Consistencia

Los Read Models utilizan:

```text
Eventually Consistent
```

Puede existir un pequeño retraso entre:

```text
Command

↓

Commit

↓

Domain Event

↓

Projection Update
```

Este comportamiento es esperado.

Durante ese intervalo, el Write Model continúa siendo la fuente
autoritativa del estado.

---

# Consistencia Eventual

La consistencia eventual significa que una consulta puede observar
temporalmente una versión anterior de una proyección después de
que el Aggregate haya confirmado una nueva modificación.

Ejemplo:

```text
ProposalStatus = UnderReview
```

en el Aggregate puede haber cambiado a:

```text
ProposalStatus = Accepted
```

mientras una proyección todavía muestra temporalmente:

```text
UnderReview
```

hasta procesar el evento correspondiente.

Esto no convierte el Read Model en fuente de verdad.

---

# Version de Proyección

Las proyecciones pueden conservar:

```text
Version
```

para representar la revisión de Proposal utilizada en su última
actualización.

Conceptualmente:

```text
ProposalVersion = 12

↓

Projection

↓

ProjectedVersion = 12
```

Esto permite identificar el estado de actualización de una vista.

ProjectedVersion no modifica ProposalVersion.

---

# Eventos Duplicados

Una proyección debe poder reconocer cuando un mismo hecho ya fue
procesado.

Conceptualmente:

```text
Domain Event X

↓

Projection Updated
```

seguido de:

```text
Domain Event X

↓

Already Applied
```

no debe producir una interpretación duplicada del mismo hecho.

La estrategia técnica pertenece a Infrastructure.

---

# Eventos Fuera de Orden

En arquitecturas distribuidas una proyección puede recibir
información fuera del orden esperado.

La Version asociada a Proposal permite contextualizar la revisión
del Aggregate correspondiente.

Conceptualmente:

```text
Version 9

↓

Version 10

↓

Version 11
```

representa la evolución lógica.

El orden físico de entrega no redefine la secuencia válida del
Aggregate.

---

# Consultas

Los Read Models permiten consultas como:

- todas las Proposals;
- Proposal por ProposalId;
- Proposals activas;
- Proposals por estado;
- Proposals por tipo;
- Proposals por Organization;
- Proposals por Territory;
- Proposals por Assembly;
- Proposals por proponente;
- Proposals creadas en un período;
- Proposals presentadas en un período;
- Proposals bajo revisión;
- Proposals aceptadas;
- Proposals rechazadas;
- Proposals retiradas;
- Proposals archivadas;
- actividad reciente;
- estadísticas por estado;
- estadísticas por Organization;
- estadísticas por Territory;
- estadísticas por tipo;
- métricas de revisión;
- indicadores de participación relacionados con Proposal.

Estas consultas nunca modifican el Aggregate.

---

# Consulta por Identidad

La consulta principal utiliza:

```text
ProposalId
```

Ejemplo conceptual:

```text
ProposalId

↓

ProposalDetail
```

La lectura no requiere obtener el Aggregate cuando únicamente se
necesita información de consulta.

---

# Consulta por Organization

Conceptualmente:

```text
OrganizationId

↓

ProposalOrganization

↓

Proposal List
```

Permite recuperar Proposals pertenecientes al contexto
organizacional correspondiente.

---

# Consulta por Territory

Conceptualmente:

```text
TerritoryId

↓

ProposalTerritory

↓

Proposal List
```

Permite consultas territoriales sin modificar Territory ni
Proposal.

---

# Consulta por Assembly

Conceptualmente:

```text
AssemblyId

↓

ProposalAssembly

↓

Proposal List
```

La consulta representa relaciones derivadas.

No establece propiedad entre Aggregates.

---

# Consulta por Proponente

Conceptualmente:

```text
ProposerReference

↓

ProposalProposer

↓

Proposal List
```

La consulta puede utilizar la referencia definida por Proposal sin
incorporar el Aggregate externo completo.

---

# Consulta por Estado

Conceptualmente:

```text
ProposalStatus

↓

ProposalDirectory

↓

Filtered Proposals
```

Estados definidos por el modelo de Proposal pueden utilizarse como
criterios de consulta.

El Read Model no define nuevos estados.

---

# Consulta por Tipo

Conceptualmente:

```text
ProposalType

↓

ProposalDirectory

↓

Filtered Proposals
```

La clasificación utilizada debe corresponder al lenguaje ubicuo
establecido por Proposal.

---

# Búsqueda

ProposalDirectory puede soportar búsqueda sobre atributos
destinados a consulta.

Conceptualmente:

```text
Search Criteria

↓

ProposalDirectory

↓

Matching Proposal Summaries
```

La búsqueda:

- no modifica Proposal;
- no valida Commands;
- no ejecuta invariantes;
- no altera estados;
- no produce Domain Events.

---

# Filtros

Los Read Models pueden soportar filtros combinados.

Ejemplo conceptual:

```text
OrganizationId

+

TerritoryId

+

ProposalStatus

+

ProposalType
```

para obtener una vista específica de Proposals.

La capacidad de combinar filtros pertenece al modelo de consulta.

No modifica el modelo de dominio.

---

# Ordenamiento

Las proyecciones pueden permitir ordenamiento por atributos de
consulta como:

```text
CreatedAt

SubmittedAt

UpdatedAt

Title

ProposalStatus
```

La definición física de índices pertenece a Infrastructure.

---

# Paginación

Los Read Models pueden soportar paginación para evitar recuperar
conjuntos completos cuando no sea necesario.

Conceptualmente:

```text
Query

↓

Page

↓

ProposalSummary[]
```

La estrategia técnica de paginación pertenece a Infrastructure.

---

# Agregaciones

Las vistas analíticas pueden realizar agregaciones derivadas.

Ejemplos:

```text
COUNT Proposals BY Status

COUNT Proposals BY Territory

COUNT Proposals BY Organization

COUNT Proposals BY Type
```

Estas operaciones no forman parte del comportamiento del
Aggregate.

---

# Relaciones Desnormalizadas

Los Read Models pueden desnormalizar información para facilitar
consultas.

Conceptualmente una vista puede mostrar:

```text
ProposalId

ProposalTitle

OrganizationReference

TerritoryReference

AssemblyReference

ProposalStatus
```

sin que esto implique que esos conceptos pertenezcan al mismo
Aggregate.

Debe mantenerse:

```text
Read Model Composition

≠

Aggregate Composition
```

---

# Regla de No Absorción

La presencia de información relacionada dentro de una proyección
no modifica los límites de consistencia.

Por ejemplo:

```text
ProposalDetail

Organization Information

Territory Information

Assembly Information
```

puede constituir una vista de consulta.

No significa:

```text
Proposal Aggregate
    │
    ├── Organization
    ├── Territory
    └── Assembly
```

Los Aggregates mantienen independencia.

---

# Read Model y Aggregate References

Las referencias externas utilizadas por Proposal pueden
representarse en vistas mediante:

```text
OrganizationId

CitizenId

MembershipId

TerritoryId

AssemblyId
```

según corresponda.

La proyección puede complementar estas referencias con información
destinada exclusivamente a lectura.

Esto no convierte dicha información en estado interno de
Proposal.

---

# Persistencia

Las proyecciones pueden almacenarse en tecnologías optimizadas
para lectura.

Ejemplos:

- PostgreSQL;
- MongoDB;
- Elasticsearch;
- OpenSearch;
- Redis;
- motores especializados de búsqueda;
- almacenes analíticos;
- cualquier motor apropiado para las necesidades de consulta.

La elección pertenece a Infrastructure.

El dominio no depende de una tecnología específica.

---

# Independencia Tecnológica

El modelo conceptual de lectura no depende de:

```text
PostgreSQL

MongoDB

Elasticsearch

OpenSearch

Redis

SQL

NoSQL

ORM
```

Estas tecnologías pueden implementar el Read Model, pero no
definen su significado.

---

# Rendimiento

Las proyecciones están optimizadas para:

- lecturas frecuentes;
- lecturas masivas;
- paginación;
- filtros;
- búsquedas;
- ordenamiento;
- agregaciones;
- dashboards;
- estadísticas;
- consultas territoriales;
- consultas organizacionales;
- seguimiento de estados.

La optimización del Read Model no debe trasladar lógica de negocio
desde Proposal hacia las proyecciones.

---

# Índices

Una implementación puede definir índices para atributos
frecuentemente consultados.

Conceptualmente pueden ser relevantes:

```text
ProposalId

OrganizationId

TerritoryId

AssemblyId

ProposerReference

ProposalStatus

ProposalType

CreatedAt

SubmittedAt
```

La selección y estructura física de índices pertenece a
Infrastructure.

---

# Cache

Las consultas pueden utilizar mecanismos de cache cuando la
arquitectura lo requiera.

Debe mantenerse:

```text
Cache

≠

Source of Truth
```

Una cache puede eliminarse y reconstruirse.

La existencia de cache no modifica Proposal.

---

# Seguridad

Cada Read Model expone únicamente la información autorizada para
el consumidor correspondiente.

Una proyección puede:

- ocultar información;
- excluir atributos no autorizados;
- limitar datos personales;
- anonimizar información cuando corresponda;
- presentar vistas diferentes según el contexto de consulta.

La autorización pertenece a la capa correspondiente del sistema.

El Read Model no redefine permisos del Aggregate.

---

# Información Personal

Cuando Proposal mantenga referencias hacia Citizen o Membership,
las vistas deben evitar replicar información personal innecesaria.

Debe preferirse:

```text
CitizenId
```

o:

```text
MembershipId
```

cuando una referencia sea suficiente.

Una vista destinada a un consumidor autorizado puede enriquecer la
representación de lectura según las políticas aplicables.

Ese enriquecimiento no modifica Proposal.

---

# Vistas Públicas

Una vista pública puede exponer un subconjunto de la información
disponible.

Conceptualmente:

```text
PublicProposalView

ProposalId

Title

ProposalType

ProposalStatus

TerritoryReference

CreatedAt
```

La vista pública no debe exponer automáticamente toda la
información disponible en ProposalDetail.

---

# Vistas Administrativas

Una vista administrativa puede contener información adicional
necesaria para operación y seguimiento.

Conceptualmente:

```text
AdministrativeProposalView

ProposalId

OrganizationId

Title

Description

ProposalType

ProposalStatus

ProposerReference

TerritoryId

AssemblyId

Lifecycle Timestamps

Version
```

La existencia de una vista administrativa no modifica el
Aggregate.

---

# Auditoría

Los Read Models pueden proporcionar vistas de consulta útiles para
Audit.

Sin embargo:

```text
Read Model

≠

Audit Log
```

La auditoría mantiene sus propias responsabilidades.

ProposalActivity puede representar actividad derivada para
consulta, pero no sustituye el registro oficial del contexto de
Audit.

---

# Integration Events

Los Read Models internos no necesitan utilizar Integration Events
cuando pueden proyectarse directamente desde Domain Events.

Los Integration Events poseen otra responsabilidad:

```text
Integration Events

=

Cross-Boundary Contracts
```

mientras:

```text
Read Models

=

Query Projections
```

Debe mantenerse:

```text
Integration Event

≠

Read Model
```

Los contratos de integración se encuentran definidos en:

```text
DOMAIN-007K-Integration-Events.md
```

---

# Proyecciones Externas

Un consumidor externo puede construir sus propias proyecciones a
partir de Integration Events.

Conceptualmente:

```text
Proposal

↓

Domain Event

↓

Integration Event

↓

External Projection
```

La proyección externa no se convierte en fuente oficial de verdad
de Proposal.

---

# Sistemas Municipales

Los sistemas municipales pueden consumir vistas o proyecciones de
Proposal mediante contratos de aplicación o integración.

Conceptualmente:

```text
Proposal Read Model

↓

Application / Integration Layer

↓

Municipal Consumer
```

El Read Model no contiene:

- endpoints municipales;
- credenciales;
- protocolos propietarios;
- autenticación externa;
- reglas específicas de una plataforma municipal.

---

# Smart City

Los Read Models pueden proporcionar información derivada útil para
ecosistemas Smart City.

Ejemplos:

```text
Proposals per Territory

Proposal Status Distribution

Proposal Participation Indicators

Proposal Geographic Distribution
```

Estas vistas no modifican el modelo de dominio.

---

# FIWARE

Una representación destinada a FIWARE puede construirse a partir
de información derivada del dominio.

Conceptualmente:

```text
Proposal

↓

Domain Events

↓

Read Projection / Integration Contract

↓

FIWARE Adapter

↓

NGSI-LD Representation
```

Proposal Read Model no depende directamente de FIWARE.

---

# NGSI-LD

Una representación NGSI-LD constituye una vista externa del
dominio.

Debe mantenerse:

```text
NGSI-LD Entity

≠

Proposal Aggregate
```

y:

```text
NGSI-LD Entity

≠

Authoritative Proposal Read Model
```

La representación puede derivarse de información disponible sin
redefinir el modelo conceptual de Proposal.

---

# Compatibilidad con CQRS

Este documento representa el lado de lectura del patrón CQRS.

```text
Write Side

Proposal Aggregate

↓

Domain Events

↓

Read Side

Proposal Read Models
```

Ambos lados poseen responsabilidades distintas.

El lado de escritura protege el dominio.

El lado de lectura optimiza consultas.

---

# Flujo CQRS

```text
                    COMMAND SIDE

Command
   │
   ▼
Proposal Aggregate
   │
   ▼
Domain Event
   │
   ▼
Commit
   │
   │
   └─────────────────────────────┐
                                 │
                                 ▼
                           Projection
                                 │
                                 ▼
                         QUERY SIDE

              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼

       ProposalSummary    ProposalDetail    ProposalStatistics
```

Las consultas no regresan al Aggregate para ejecutar lógica de
lectura cuando existe una proyección apropiada.

---

# Compatibilidad con Event Sourcing

Cuando AURA utilice Event Sourcing para el Aggregate
correspondiente, los Read Models no almacenan la historia oficial
como responsabilidad propia.

La historia permanece representada por:

```text
Domain Events
```

Las proyecciones constituyen representaciones materializadas de
esa historia.

Conceptualmente:

```text
Event Stream

↓

Replay

↓

Projection Engine

↓

Proposal Read Models
```

---

# Read Model y Event Sourcing

Debe mantenerse:

```text
Event Store

≠

Read Model Store
```

El Event Store, cuando corresponda, mantiene hechos del dominio.

El Read Model Store mantiene vistas derivadas.

Eliminar una proyección no elimina la historia del Aggregate.

---

# Evolución

Nuevas proyecciones pueden incorporarse sin modificar Proposal,
siempre que:

- sean derivadas de información válida del dominio;
- no introduzcan lógica de negocio;
- no modifiquen el Aggregate;
- mantengan independencia del lado de escritura;
- respeten el lenguaje ubicuo;
- respeten las reglas de seguridad;
- no redefinan los límites de consistencia.

Ejemplos conceptuales de nuevas vistas:

```text
ProposalGeographicView

ProposalParticipationView

ProposalTrendView

ProposalMunicipalView
```

La incorporación de una nueva necesidad de consulta no implica
automáticamente una modificación del Aggregate.

---

# Eliminación de Proyecciones

Una proyección puede retirarse cuando deja de ser necesaria.

Eliminar:

```text
ProposalStatistics
```

por ejemplo, no elimina:

```text
Proposal
```

ni sus hechos de dominio.

La vida de una proyección es independiente de la identidad del
Aggregate.

---

# Nuevas Necesidades de Consulta

Cuando aparece una nueva necesidad de consulta debe evaluarse
primero si puede resolverse mediante una nueva proyección.

No debe modificarse Proposal únicamente para satisfacer una
necesidad de presentación.

Debe mantenerse:

```text
Query Requirement

↓

Read Model
```

cuando no exista una nueva regla real del dominio.

---

# Read Model y UI

Las interfaces de usuario pueden consumir Read Models.

Conceptualmente:

```text
UI

↓

Application Query

↓

Read Model
```

La UI no debe definir el estado válido de Proposal.

La forma de presentación no modifica el lenguaje ni las reglas del
Aggregate.

---

# Read Model y API

Una API de consulta puede exponer información derivada de los Read
Models.

Conceptualmente:

```text
Client

↓

Query API

↓

Read Model
```

La API pertenece fuera del dominio.

El Read Model no depende de:

```text
HTTP

REST

GraphQL

Frameworks
```

---

# Regla de No Dependencia Inversa

Proposal no depende de sus Read Models.

No debe existir:

```text
Proposal Aggregate

↓

ProposalSummary
```

ni:

```text
Proposal Aggregate

↓

ProposalStatistics
```

El flujo correcto es:

```text
Proposal

↓

Domain Events

↓

Read Models
```

---

# Regla de Reconstruibilidad

Una proyección oficial debe poder reconstruirse a partir de las
fuentes de dominio disponibles para dicha proyección.

No debe convertirse en el único lugar donde exista información
necesaria para preservar el significado del Aggregate.

Debe mantenerse:

```text
Read Model

=

Derived State
```

No:

```text
Read Model

=

Only Domain Truth
```

---

# Regla de Desnormalización

La desnormalización está permitida en el lado de lectura cuando
mejora la capacidad de consulta.

Ejemplo:

```text
ProposalSummary

ProposalId
OrganizationId
OrganizationName
TerritoryId
TerritoryName
ProposalStatus
```

puede constituir una vista derivada.

La presencia de:

```text
OrganizationName
```

o:

```text
TerritoryName
```

no convierte esos valores en atributos propios del Aggregate
Proposal.

---

# Regla de Derivación

Toda información del Read Model debe poder explicar su origen
conceptual.

Puede provenir de:

- Domain Events de Proposal;
- referencias de dominio;
- proyecciones autorizadas de otros contextos;
- información derivada para consulta;
- agregaciones calculadas.

La combinación de información para lectura no modifica la
propiedad conceptual de los datos originales.

---

# Regla de No Autoridad

Un Read Model no puede utilizarse como autoridad para reconstruir
arbitrariamente una modificación del Aggregate.

No debe ejecutarse:

```text
Read Model State

↓

Overwrite Proposal
```

El flujo de escritura continúa protegido por Commands,
comportamiento del Aggregate e invariantes.

---

# Escenario — Listado de Proposals

```text
User Query

↓

ProposalSummary

↓

Proposal List
```

No se carga el Aggregate para ejecutar una operación de lectura
cuando la proyección satisface la consulta.

---

# Escenario — Consulta Detallada

```text
ProposalId

↓

ProposalDetail

↓

Detailed View
```

La consulta no modifica Proposal.

---

# Escenario — Proposals por Territory

```text
TerritoryId

↓

ProposalTerritory

↓

Matching Proposals
```

Territory no es cargado como parte de Proposal.

---

# Escenario — Proposals por Assembly

```text
AssemblyId

↓

ProposalAssembly

↓

Related Proposals
```

La vista representa la relación de consulta sin fusionar los
Aggregates.

---

# Escenario — Bandeja de Revisión

```text
Query:

ProposalStatus = Submitted
or
ProposalStatus = UnderReview

↓

ProposalReview

↓

Review Queue
```

La bandeja no decide si una Proposal puede ser aceptada o
rechazada.

La decisión pertenece al lado de escritura.

---

# Escenario — Dashboard

```text
Proposal Domain Events

↓

ProposalStatistics

↓

Dashboard
```

El dashboard presenta información derivada.

No modifica el dominio.

---

# Escenario — Actualización Eventual

```text
AcceptProposal

↓

ProposalAccepted

↓

Commit

↓

Proposal = Accepted
```

Durante un intervalo breve:

```text
ProposalSummary = UnderReview
```

Posteriormente:

```text
Projection consumes ProposalAccepted

↓

ProposalSummary = Accepted
```

La diferencia temporal es consecuencia de la consistencia
eventual del Read Model.

---

# Escenario — Reconstrucción

```text
Delete ProposalSummary Projection

↓

Replay Domain Events

↓

Rebuild ProposalSummary

↓

Projection Available
```

Proposal no cambia durante este proceso.

---

# Escenario — Nueva Proyección

Se requiere una vista territorial especializada.

No se modifica Proposal únicamente por esta necesidad.

Conceptualmente:

```text
Existing Domain Facts

↓

New Projection

↓

ProposalGeographicView
```

La nueva proyección permanece fuera del Aggregate.

---

# Escenario — Vista Pública

```text
ProposalDetail

↓

Public Projection Rules

↓

PublicProposalView
```

La vista pública contiene únicamente la información autorizada.

La reducción de información no modifica el estado de Proposal.

---

# Escenario — Sistema Municipal

```text
Municipal Query

↓

Application Layer

↓

Proposal Read Model

↓

Authorized Representation
```

Proposal no incorpora comportamiento específico del sistema
municipal.

---

# Escenario — Estadísticas Territoriales

```text
ProposalTerritory

↓

Aggregation

↓

Proposals per Territory
```

La estadística representa información derivada.

No modifica Territory ni Proposal.

---

# Restricciones

No está permitido:

- modificar Proposal desde un Read Model;
- ejecutar Commands desde una proyección como parte de su
  responsabilidad de lectura;
- introducir invariantes dentro de un Read Model;
- utilizar un Read Model para controlar la State Machine;
- utilizar un Read Model para controlar el Lifecycle;
- utilizar una proyección como fuente oficial de verdad del
  Aggregate;
- almacenar comportamiento del dominio en una proyección;
- convertir necesidades de UI en atributos obligatorios del
  Aggregate sin una razón de dominio;
- fusionar Aggregates mediante una vista desnormalizada;
- interpretar información desnormalizada como propiedad del
  Aggregate;
- depender de una base de datos específica desde el modelo
  conceptual;
- introducir detalles ORM dentro del dominio;
- introducir lógica HTTP dentro del Read Model conceptual;
- introducir lógica FIWARE dentro de Proposal;
- exponer información no autorizada;
- utilizar una cache como fuente oficial de verdad;
- incrementar ProposalVersion debido exclusivamente a una
  actualización de proyección;
- generar Domain Events debido exclusivamente a una consulta;
- modificar el Aggregate durante una reconstrucción;
- utilizar una proyección para sobrescribir el estado válido del
  Aggregate.

---

# Invariantes del Modelo de Lectura

Aunque los Read Models no protegen invariantes del Aggregate,
deben mantener reglas conceptuales propias de su responsabilidad
de lectura:

- una proyección es de solo lectura respecto de Proposal;
- una proyección representa información derivada;
- ProposalId conserva su significado como identidad del Aggregate;
- ProposalStatus utiliza estados definidos por el dominio;
- ProposalType utiliza clasificaciones definidas por el dominio;
- Version representa la revisión correspondiente del Aggregate
  cuando sea incluida;
- una proyección no crea nuevos estados de Proposal;
- una proyección no crea nuevas transiciones;
- una proyección no modifica el Lifecycle;
- una proyección puede ser reconstruida;
- una proyección puede ser reemplazada;
- una proyección puede ser eliminada sin eliminar Proposal;
- la desnormalización no modifica límites de Aggregate;
- una vista combinada no crea propiedad entre Aggregates;
- la consistencia eventual es válida;
- una consulta nunca constituye un Command;
- una consulta no produce por sí misma un Domain Event.

---

# Matriz de Responsabilidades

```text
Responsabilidad                      Proposal   Read Model

Proteger invariantes                 Sí         No

Ejecutar comportamiento              Sí         No

Controlar Lifecycle                  Sí         No

Controlar State Machine              Sí         No

Aceptar Commands                     Sí         No

Generar Domain Events                Sí         No

Mantener Version                     Sí         No

Responder consultas optimizadas      No         Sí

Realizar búsquedas                    No         Sí

Realizar filtros                      No         Sí

Realizar paginación                   No         Sí

Realizar agregaciones                 No         Sí

Mantener estadísticas                No         Sí

Desnormalizar información            No         Sí

Soportar dashboards                   No         Sí

Ser reconstruible                     No         Sí
```

---

# Matriz de Proyecciones

```text
Projection              Responsabilidad principal

ProposalSummary         Listado resumido

ProposalDetail          Consulta detallada

ProposalDirectory       Búsqueda y filtros

ProposalStatus          Estado y Lifecycle

ProposalOrganization    Consulta por Organization

ProposalTerritory       Consulta territorial

ProposalAssembly        Consulta por Assembly

ProposalProposer        Consulta por proponente

ProposalReview          Seguimiento de revisión

ProposalActivity        Actividad derivada

ProposalStatistics      Indicadores y análisis
```

---

# Compatibilidad Arquitectónica

El modelo de lectura de Proposal es compatible con:

- Domain-Driven Design;
- CQRS;
- Clean Architecture;
- Hexagonal Architecture;
- Event Sourcing;
- Event-Driven Architecture;
- SOLID;
- consistencia eventual;
- arquitectura distribuida;
- proyecciones reconstruibles;
- modelos especializados de consulta;
- interoperabilidad mediante capas externas.

---

# Principios Arquitectónicos

Los Read Models mantienen:

```text
Write Model

≠

Read Model
```

```text
Proposal Aggregate

≠

Proposal Projection
```

```text
Query

≠

Command
```

```text
Read Model

≠

Source of Truth
```

```text
Read Model

≠

Aggregate
```

```text
Projection State

≠

Domain Authority
```

```text
Read Model Composition

≠

Aggregate Composition
```

```text
Desnormalization

≠

Domain Ownership
```

```text
ProposalStatus Projection

≠

State Machine
```

```text
ProposalActivity

≠

Audit Log
```

```text
Integration Event

≠

Read Model
```

```text
Cache

≠

Source of Truth
```

```text
NGSI-LD Representation

≠

Proposal Aggregate
```

```text
Infrastructure

≠

Domain Model
```

---

# Documentación Complementaria

El Read Model debe interpretarse conjuntamente con:

```text
DOMAIN-007-Aggregate.md

DOMAIN-007A-Lifecycle.md

DOMAIN-007B-State-Machine.md

DOMAIN-007C-Commands.md

DOMAIN-007D-Domain-Events.md

DOMAIN-007E-Invariants.md

DOMAIN-007F-Permissions.md

DOMAIN-007G-Repository-Contract.md

DOMAIN-007H-Examples.md

DOMAIN-007I-Versioning.md

DOMAIN-007J-Consistency-Boundary.md

DOMAIN-007K-Integration-Events.md

DOMAIN-007M-Test-Scenarios.md

DOMAIN-007N-Performance-Rules.md

DOMAIN-007O-Security-Model.md

DOMAIN-007P-Extension-Points.md
```

Estos documentos desarrollan responsabilidades específicas del
Aggregate Proposal y deben conservar la separación entre el lado
de escritura, el modelo de lectura, los contratos de integración
y la infraestructura.

---

# Definición de Éxito

Los Read Models del Aggregate **Proposal** proporcionan vistas
especializadas, reconstruibles y optimizadas para consulta,
permitiendo que AURA represente y consulte Proposals sin
comprometer la consistencia del modelo de escritura.

Las proyecciones permiten soportar:

```text
Lists

Search

Filters

Detail Views

Review Queues

Organization Views

Territorial Views

Assembly Views

Proposer Views

Activity Views

Statistics

Dashboards

Analytics
```

sin trasladar lógica de negocio fuera del Aggregate.

Proposal continúa siendo responsable de:

```text
Behavior

Lifecycle

State Machine

Invariants

Domain Events

Version

Consistency
```

mientras los Read Models permanecen responsables exclusivamente de
representaciones derivadas para consulta.

La desnormalización, composición de información, optimización de
búsqueda y construcción de estadísticas no modifica los límites
de los Aggregates ni convierte las proyecciones en fuentes
autoritativas del dominio.

De esta forma, el Read Model de **Proposal** constituye el modelo
oficial de lectura del Bounded Context Proposal Management,
manteniendo separación explícita entre escritura y consulta,
compatibilidad con CQRS, reconstruibilidad, consistencia eventual,
independencia tecnológica y capacidad de evolución dentro de la
arquitectura DDD de AURA Core.