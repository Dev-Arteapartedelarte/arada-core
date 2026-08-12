# DOMAIN-007P — Proposal Extension Points

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
- DOMAIN-007L-Read-Model.md
- DOMAIN-007M-Test-Scenarios.md
- DOMAIN-007N-Performance-Rules.md
- DOMAIN-007O-Security-Model.md
- CORE-003-Shared-Kernel.md
- CORE-004-Ubiquitous-Language.md
- CORE-005-Domain-Events.md
- CORE-006-Domain-Invariants.md
- CORE-007-Strategic-Design.md
- CORE-008-Aggregate-Design-Rules.md
- CORE-011-Repository-Contracts.md

---

# Objetivo

Definir los puntos oficiales de extensión del Aggregate
**Proposal**.

Los Extension Points establecen los lugares conceptuales en los
cuales el modelo puede evolucionar sin alterar su identidad,
responsabilidades fundamentales, invariantes estructurales ni
límite de consistencia.

Este documento define cómo pueden incorporarse nuevas capacidades
al Aggregate manteniendo el modelo DDD consolidado de AURA.

Los Extension Points no constituyen mecanismos para introducir
comportamiento arbitrario.

Toda extensión debe preservar las reglas oficiales establecidas
por el Aggregate Proposal.

---

# Propósito

El propósito de los Extension Points es permitir que Proposal
evolucione de manera controlada frente a nuevas necesidades del
dominio.

La evolución puede requerir:

- nuevos tipos de Proposal;
- nuevas reglas de negocio;
- nuevas transiciones válidas;
- nuevos Commands;
- nuevos Domain Events;
- nuevas Permissions;
- nuevas proyecciones;
- nuevos Integration Events;
- nuevas políticas de dominio;
- nuevas capacidades de interoperabilidad;
- nuevas reglas organizacionales;
- nuevas relaciones mediante identificadores;
- nuevas necesidades de consulta;
- nuevas reglas de seguridad;
- nuevas reglas de rendimiento.

Estas extensiones deben incorporarse sin romper los principios
fundamentales del Aggregate.

---

# Principio Fundamental

Una extensión es válida únicamente cuando preserva:

```text
Proposal Identity

+

Proposal Aggregate Root

+

Consistency Boundary

+

Domain Invariants

+

Lifecycle

+

State Machine

+

Versioning

+

Domain Events

+

Repository Contract

+

Security Model
```

Una extensión que requiera violar alguno de estos elementos no
constituye una extensión válida del modelo existente.

Debe evaluarse como una modificación explícita del modelo de
dominio.

---

# Regla de Extensibilidad

Proposal debe permanecer:

```text
Open for Domain Evolution

Closed against Boundary Violation
```

Esto significa que el Aggregate puede incorporar nuevos
comportamientos y conceptos cuando el dominio evoluciona.

Sin embargo, ninguna extensión puede utilizarse para:

- absorber otros Aggregates;
- modificar directamente otros Aggregates;
- introducir dependencias de Infrastructure;
- evadir invariantes;
- evadir la State Machine;
- evadir Permissions;
- modificar Version directamente;
- modificar identidad;
- convertir Read Models en modelos de escritura;
- utilizar Integration Events como Commands;
- introducir dependencias tecnológicas en el dominio.

---

# Modelo Conceptual de Extensión

```text
                    Proposal

                       │

        ┌──────────────┼──────────────┐

        │              │              │

        ▼              ▼              ▼

   Behavior        Policies       Value Objects

        │              │              │

        ├──────────────┼──────────────┤

        │              │              │

        ▼              ▼              ▼

    Commands      Domain Events    Permissions

        │              │              │

        └──────────────┼──────────────┘

                       │

                       ▼

                Proposal Contract

                       │

        ┌──────────────┼──────────────┐

        ▼              ▼              ▼

   Read Models    Integration     Application
                    Events          Services
```

Las extensiones internas deben preservar el límite del Aggregate.

Las extensiones externas deben utilizar contratos explícitos.

---

# Clasificación de Extension Points

Los puntos de extensión de Proposal se clasifican
conceptualmente en:

```text
Domain Extension Points

Behavior Extension Points

Lifecycle Extension Points

Command Extension Points

Domain Event Extension Points

Permission Extension Points

Repository Extension Points

Read Model Extension Points

Integration Extension Points

Security Extension Points

Performance Extension Points

Policy Extension Points
```

Cada categoría posee reglas específicas.

---

# Domain Extension Points

Los Domain Extension Points permiten incorporar nuevos conceptos
que pertenezcan legítimamente a la responsabilidad de Proposal.

Una extensión de dominio puede incorporar:

- nuevos Value Objects;
- nuevas reglas;
- nuevos comportamientos;
- nuevas clasificaciones;
- nuevas políticas;
- nuevos atributos conceptuales.

La incorporación debe responder a una necesidad real del dominio.

No debe realizarse únicamente por conveniencia técnica.

---

# Regla de Pertenencia al Aggregate

Antes de incorporar un nuevo concepto dentro de Proposal debe
verificarse:

```text
Does the concept require strong consistency
with Proposal?
```

y:

```text
Does Proposal own the lifecycle
of the concept?
```

y:

```text
Can the concept exist independently
from Proposal?
```

Si el concepto posee:

- identidad independiente;
- ciclo de vida independiente;
- Repository independiente;
- invariantes independientes;
- comportamiento independiente;

debe evaluarse como un Aggregate separado.

No debe incorporarse automáticamente dentro de Proposal.

---

# Regla de No Absorción

Proposal no absorbe otros Aggregates debido a que participen en
el mismo proceso.

Por lo tanto:

```text
Proposal

    │

    ├── Assembly

    ├── Participation

    ├── Voting

    ├── Document

    ├── Notification

    └── Audit
```

representa relaciones conceptuales.

No representa:

```text
Proposal

    └── Assembly

          └── Participation

                └── Voting

                      └── Document
```

Cada Aggregate conserva su propio límite de consistencia.

---

# Nuevos Atributos Conceptuales

Proposal puede incorporar nuevos atributos cuando estos sean
necesarios para representar correctamente el concepto de
Proposal.

Todo nuevo atributo debe definir:

- significado dentro del lenguaje ubicuo;
- propiedad dentro del Aggregate;
- obligatoriedad;
- mutabilidad;
- validaciones;
- relación con el Lifecycle;
- relación con las invariantes;
- relación con Version;
- impacto sobre Domain Events;
- impacto sobre Read Models;
- impacto sobre Integration Events.

No debe agregarse información únicamente porque resulte
conveniente para una interfaz o integración.

---

# Nuevos Value Objects

Proposal puede incorporar nuevos Value Objects cuando exista un
concepto del dominio que requiera:

- validación propia;
- semántica propia;
- inmutabilidad;
- comportamiento asociado al valor.

Ejemplos conceptuales:

```text
ProposalCategory

ProposalPriority

ProposalScope

ProposalReference

ProposalMetadata
```

Estos nombres representan posibles puntos de evolución y no
implican que deban incorporarse al modelo actual sin una necesidad
formal del dominio.

Todo nuevo Value Object debe permanecer independiente de
Infrastructure.

---

# Regla de Value Objects

Un nuevo Value Object debe:

- representar un concepto del lenguaje ubicuo;
- ser inmutable;
- validar sus propias reglas de valor;
- no poseer identidad independiente;
- no depender de bases de datos;
- no depender de APIs;
- no depender de Frameworks;
- no contener Aggregates externos.

Si requiere identidad y ciclo de vida propios debe reconsiderarse
su clasificación.

---

# Tipos de Proposal

El modelo puede evolucionar incorporando nuevas clasificaciones de
Proposal.

Ejemplos conceptuales:

```text
Community

Organizational

Territorial

Governance

Operational
```

La incorporación de un nuevo tipo debe preservar:

- ProposalId;
- Aggregate Root;
- Lifecycle;
- invariantes comunes;
- Version;
- Repository;
- consistencia.

Un nuevo tipo no debe crear implícitamente un Aggregate diferente
sin evaluación del dominio.

---

# Extensión de Clasificaciones

Una nueva clasificación puede incorporarse cuando represente una
distinción significativa dentro del dominio.

No debe utilizarse una clasificación para introducir
comportamientos incompatibles ocultos.

Cuando una clasificación requiera:

- Lifecycle completamente diferente;
- invariantes incompatibles;
- identidad distinta;
- consistencia diferente;
- responsabilidades diferentes;

debe evaluarse si continúa perteneciendo al mismo Aggregate.

---

# Behavior Extension Points

Proposal puede incorporar nuevos comportamientos de dominio.

Ejemplos conceptuales:

```text
changeCategory()

changePriority()

associateTerritory()

associateAssembly()

requestAdditionalReview()
```

Todo nuevo comportamiento debe:

- ejecutarse mediante Proposal;
- proteger invariantes;
- respetar la State Machine;
- respetar Permissions;
- incrementar Version cuando modifique estado;
- producir Domain Events cuando corresponda;
- permanecer dentro del límite de consistencia.

---

# Regla de Comportamiento

No debe incorporarse comportamiento únicamente como setter.

No debe utilizarse:

```text
setStatus()

setVersion()

setOrganizationId()
```

Debe preferirse comportamiento expresivo del dominio.

Ejemplo:

```text
submit()

withdraw()

accept()

reject()
```

El comportamiento debe expresar intención y significado.

---

# Nuevas Operaciones

Una nueva operación sobre Proposal debe responder a una capacidad
real del dominio.

Antes de incorporarla deben definirse:

```text
Intent

Preconditions

Allowed States

Permission

Invariants

State Change

Version Change

Domain Events
```

La ausencia de alguno de estos elementos puede producir
comportamiento ambiguo.

---

# Lifecycle Extension Points

El Lifecycle puede evolucionar cuando aparezcan nuevos estados o
fases legítimas del dominio.

Toda extensión debe mantener coherencia con:

```text
DOMAIN-007A-Lifecycle.md
```

y:

```text
DOMAIN-007B-State-Machine.md
```

No debe incorporarse un nuevo estado únicamente porque una
interfaz necesite mostrar una etiqueta diferente.

---

# Nuevos Estados

Un nuevo estado debe representar una condición significativa del
Aggregate.

Debe responder como mínimo:

```text
What does the state mean?

How is it entered?

How is it exited?

What operations are allowed?

What operations are forbidden?

Is it terminal?

What events produce the transition?
```

Un estado sin comportamiento o restricciones diferenciables puede
no justificar su existencia dentro de la State Machine.

---

# Extensión de Transiciones

Una nueva transición debe definir:

```text
Source State

Command

Permission

Preconditions

Invariants

Destination State

Domain Event
```

Ejemplo conceptual:

```text
CurrentState

↓

NewCommand

↓

Validation

↓

NewState

↓

NewDomainEvent
```

No se permiten transiciones implícitas.

---

# Estados Terminales

La incorporación de nuevos estados terminales debe definir
explícitamente:

- posibilidad de archivado;
- operaciones permitidas;
- operaciones prohibidas;
- efectos sobre integraciones;
- efectos sobre Read Models;
- comportamiento ante nuevos Commands.

Un estado terminal no debe volver a un estado anterior salvo que
el dominio defina explícitamente dicha transición.

---

# Command Extension Points

Proposal puede incorporar nuevos Commands.

Todo nuevo Command representa una intención explícita de modificar
el Aggregate.

Debe mantener el patrón conceptual:

```text
CommandId

ProposalId

OrganizationId

ActorId

Timestamp

CorrelationId

CausationId
```

más los datos específicos de la operación.

---

# Reglas para Nuevos Commands

Todo nuevo Command debe:

- poseer identidad;
- ser inmutable;
- representar una única intención;
- dirigirse a un único Aggregate;
- identificar al actor cuando corresponda;
- respetar Permissions;
- respetar Version;
- respetar Lifecycle;
- respetar State Machine;
- preservar invariantes;
- producir Domain Events cuando la operación sea aceptada.

---

# Commands y Límites

Un Command de Proposal no debe modificar simultáneamente:

```text
Assembly

Participation

Voting

Document

Notification

Audit
```

Cuando una operación de aplicación requiera coordinación entre
múltiples Aggregates, dicha coordinación debe ocurrir fuera del
Aggregate Proposal.

---

# Commands Genéricos

No deben incorporarse Commands genéricos como:

```text
UpdateProposal

PatchProposal

ModifyProposal

SetProposalState
```

cuando permitan modificar arbitrariamente múltiples conceptos sin
expresar intención del dominio.

Deben preferirse Commands explícitos.

Ejemplo:

```text
RenameProposal

ChangeProposalDescription

SubmitProposal

WithdrawProposal
```

---

# Domain Event Extension Points

Proposal puede incorporar nuevos Domain Events cuando aparezcan
nuevos hechos relevantes.

Todo nuevo evento debe representar:

```text
Something that already happened
```

No una intención.

---

# Reglas para Nuevos Domain Events

Todo nuevo Domain Event debe:

- utilizar lenguaje ubicuo;
- representar un hecho consumado;
- originarse en comportamiento válido;
- poseer identidad cuando el contrato lo requiera;
- mantener trazabilidad;
- permitir evolución;
- evitar información técnica innecesaria;
- evitar credenciales;
- no modificar otros Aggregates.

---

# Correspondencia Command-Event

Una extensión debe mantener una relación conceptual clara entre
intención y resultado.

Ejemplo:

```text
ChangeProposalPriority

↓

ProposalPriorityChanged
```

No todo Command debe producir exactamente un evento.

Una operación puede producir varios hechos cuando el dominio así
lo requiera.

Sin embargo, cada evento debe corresponder a un hecho real.

---

# Eventos Históricos

Una extensión no debe modificar retroactivamente el significado de
eventos históricos existentes.

Cuando una nueva necesidad requiera representar un hecho diferente,
debe definirse un nuevo evento cuando corresponda.

Esto permite preservar:

- trazabilidad;
- reconstrucción;
- compatibilidad;
- significado histórico.

---

# Permission Extension Points

Proposal puede incorporar nuevas capacidades de autorización.

Las extensiones deben mantener el modelo definido en:

```text
DOMAIN-007F-Permissions.md
```

Una nueva Permission debe corresponder a una capacidad concreta del
dominio.

---

# Nuevas Permissions

Ejemplos conceptuales:

```text
ChangeProposalCategory

ChangeProposalPriority

RequestProposalReview

AssociateProposalTerritory
```

Estos ejemplos representan posibles extensiones y no establecen
nuevas capacidades oficiales hasta que sean incorporadas
formalmente al modelo de permisos.

---

# Regla de Mínimo Privilegio

Una nueva Permission debe representar la capacidad mínima necesaria
para una operación.

No debe introducirse una Permission excesivamente amplia como:

```text
ManageEverything
```

cuando puedan expresarse capacidades específicas.

La extensión debe mantener separación entre:

```text
Create

Modify

Submit

Review

Accept

Reject

Withdraw

Archive
```

según el modelo oficial.

---

# Roles y Nuevas Permissions

Una nueva Permission no debe acoplar Proposal directamente a un
Role específico.

Debe mantenerse:

```text
Role

↓

Permission Assignment

↓

Permission

↓

Command Authorization
```

Proposal conoce la capacidad autorizada necesaria.

No necesita conocer la estructura completa del Aggregate Role.

---

# Policy Extension Points

Las reglas que dependan de criterios variables del dominio pueden
evolucionar mediante políticas explícitas.

Una política puede representar decisiones como:

- elegibilidad;
- revisión;
- clasificación;
- condiciones organizacionales;
- condiciones territoriales;
- condiciones de presentación.

Las políticas deben permanecer expresadas en lenguaje del dominio.

---

# Domain Policies

Una Domain Policy puede utilizarse cuando una regla:

- pertenece al dominio;
- no corresponde naturalmente a una única propiedad;
- requiere evaluar varios conceptos;
- permanece independiente de Infrastructure.

Una política no debe utilizarse para extraer arbitrariamente
comportamiento que pertenece al Aggregate Root.

---

# Políticas Organizacionales

Proposal puede requerir reglas variables según Organization.

Estas reglas pueden determinar:

- condiciones de presentación;
- requisitos de revisión;
- clasificaciones permitidas;
- restricciones operacionales.

La variabilidad organizacional no debe permitir modificar
invariantes estructurales del Aggregate.

---

# Políticas Territoriales

Cuando Proposal se relacione con Territory pueden existir reglas
específicas del contexto territorial.

Estas reglas no convierten Territory en una entidad interna de
Proposal.

Debe mantenerse:

```text
Proposal

↓

TerritoryId
```

y no:

```text
Proposal

↓

Mutable Territory Aggregate
```

---

# Repository Extension Points

El Repository puede evolucionar para soportar nuevas necesidades de
persistencia del Aggregate.

La extensión debe respetar:

```text
DOMAIN-007G-Repository-Contract.md
```

El Repository continúa representando un contrato de persistencia.

---

# Nuevas Operaciones de Repository

Una nueva operación puede incorporarse cuando sea necesaria para:

- obtener Proposal por identidad;
- verificar existencia;
- persistir el Aggregate;
- controlar Version;
- resolver necesidades propias del contrato.

No debe incorporarse una operación que permita modificar atributos
internos directamente.

---

# Repository Queries

Las consultas complejas orientadas a visualización, estadísticas o
búsqueda no deben convertir el Repository del Aggregate en un
servicio de reporting.

Dichas necesidades pertenecen preferentemente a:

```text
Read Models
```

cuando el modelo CQRS así lo establece.

---

# Repository y Nuevos Motores

Cambiar:

```text
PostgreSQL
```

por:

```text
MongoDB
```

o cualquier otra tecnología no constituye una extensión del
dominio.

Es una decisión de Infrastructure.

El Repository Contract debe permanecer independiente de dicha
decisión.

---

# Versioning Extension Points

Toda extensión que modifique estado debe integrarse con:

```text
DOMAIN-007I-Versioning.md
```

Una nueva operación válida debe respetar el modelo de Version
establecido.

---

# Regla de Version

Debe mantenerse:

```text
Valid State Change

↓

Version Increment
```

Una extensión no puede crear una ruta alternativa de escritura que
evite Version.

---

# Evolución del Aggregate y Version

La incorporación de nuevos atributos o comportamientos no debe
confundirse con la Version de concurrencia del Aggregate.

```text
Domain Model Version

≠

Aggregate Concurrency Version
```

La Version del Aggregate continúa representando el mecanismo
conceptual establecido para concurrencia optimista.

---

# Consistency Extension Points

Toda extensión debe respetar:

```text
DOMAIN-007J-Consistency-Boundary.md
```

Una nueva capacidad no puede ampliar implícitamente la transacción
de Proposal hacia otros Aggregates.

---

# Regla de Consistencia

Debe mantenerse:

```text
One Proposal

=

One Aggregate Consistency Boundary
```

La coordinación con otros Aggregates utiliza los mecanismos
definidos por la arquitectura.

---

# Nuevas Relaciones

Proposal puede incorporar nuevas relaciones con otros Aggregates
cuando el dominio lo requiera.

La relación debe representarse mediante identidad.

Ejemplo conceptual:

```text
ExternalAggregateId
```

No mediante inclusión del Aggregate completo.

---

# Regla para Nuevas Relaciones

Antes de incorporar una relación debe determinarse:

- significado dentro del dominio;
- dirección conceptual;
- cardinalidad cuando corresponda;
- obligatoriedad;
- momento del Lifecycle en que puede establecerse;
- posibilidad de modificación;
- impacto sobre invariantes;
- impacto sobre eventos.

La relación no debe introducir dependencia mutable entre
Aggregates.

---

# Assembly Extension Point

Proposal puede evolucionar en su relación contextual con Assembly.

Puede existir:

```text
AssemblyId
```

cuando una Proposal se origine, presente, discuta o relacione con
una Assembly.

Assembly continúa siendo un Aggregate independiente.

Proposal no administra el Lifecycle de Assembly.

---

# Participation Extension Point

Proposal puede relacionarse con procesos de Participation.

La relación puede utilizar:

```text
ParticipationId
```

cuando el dominio lo requiera.

Proposal no administra Participation.

La participación conserva sus propias reglas e invariantes.

---

# Voting Extension Point

Proposal puede relacionarse con uno o más procesos de Voting.

La relación puede utilizar:

```text
VotingId
```

Voting conserva:

- identidad;
- Lifecycle;
- State Machine;
- invariantes;
- Permissions;
- Repository;
- Domain Events.

Proposal no absorbe Voting.

---

# Document Extension Point

Proposal puede relacionarse con Documents mediante:

```text
DocumentId
```

La extensión puede permitir nuevos tipos de asociación documental.

Document continúa administrando:

- identidad documental;
- contenido;
- Lifecycle;
- metadata propia;
- reglas propias.

Proposal no almacena el Aggregate Document completo.

---

# Notification Extension Point

Nuevos Domain Events de Proposal pueden originar nuevas necesidades
de Notification.

Ejemplo conceptual:

```text
ProposalReviewRequested

↓

Notification Process
```

Proposal no envía Notifications directamente.

La reacción pertenece al contexto correspondiente.

---

# Audit Extension Point

Nuevos comportamientos pueden producir nueva información relevante
para Audit.

La extensión debe preservar:

```text
Proposal

↓

Domain Event

↓

Audit
```

cuando corresponda.

Audit no se incorpora dentro del Aggregate Proposal.

---

# Integration Extension Points

Proposal puede incorporar nuevas capacidades de interoperabilidad.

Estas extensiones se desarrollan mediante:

```text
Domain Events

↓

Integration Mapping

↓

Integration Events

↓

Adapters

↓

External Systems
```

El Aggregate no depende directamente del sistema externo.

---

# Nuevos Integration Events

Todo nuevo Integration Event debe:

- representar información relevante para consumidores externos;
- derivarse de un estado confirmado;
- poseer contrato explícito;
- minimizar información;
- mantener trazabilidad;
- evitar credenciales;
- permitir evolución contractual.

La definición debe incorporarse en:

```text
DOMAIN-007K-Integration-Events.md
```

---

# Nuevos Consumidores

La incorporación de un nuevo consumidor no requiere modificar el
Aggregate cuando puede utilizar contratos existentes.

Ejemplos:

```text
Municipality

Smart City Platform

Analytics Platform

Open Government Platform

Notification Platform
```

La responsabilidad de adaptación pertenece a Integration e
Infrastructure.

---

# Interoperabilidad Municipal

Proposal puede extender su interoperabilidad con plataformas
municipales.

Una integración municipal puede requerir:

- publicación de propuestas;
- actualización de estado;
- referencias territoriales;
- identificadores de interoperabilidad;
- seguimiento de procesos.

Estas necesidades no convierten el sistema municipal en parte del
Aggregate.

---

# Smart City Extension Point

Proposal puede participar en ecosistemas Smart City.

El modelo puede proyectar información necesaria hacia contratos
externos sin modificar su estructura fundamental.

Debe mantenerse:

```text
Proposal Domain Model

≠

Smart City External Model
```

La transformación ocurre fuera del Aggregate.

---

# FIWARE Extension Point

La integración con FIWARE constituye un punto de extensión de
interoperabilidad.

Conceptualmente:

```text
Proposal

↓

Domain Event

↓

Integration Event

↓

FIWARE Adapter

↓

NGSI-LD Entity
```

Proposal no conoce directamente:

- Context Broker;
- endpoints NGSI-LD;
- autenticación FIWARE;
- Keyrock;
- PEP Proxy;
- HTTP.

---

# NGSI-LD

Una representación NGSI-LD de Proposal constituye una proyección o
contrato externo.

No constituye el Aggregate.

Debe mantenerse:

```text
Proposal Aggregate

≠

NGSI-LD Entity
```

La representación externa puede evolucionar independientemente
mientras preserve el significado contractual requerido.

---

# Nuevos Protocolos

La incorporación de nuevos protocolos de integración no modifica
el dominio.

Pueden existir adaptadores para:

```text
HTTP

Messaging

NGSI-LD

Event Streams

External APIs
```

sin introducir dichas tecnologías dentro de Proposal.

---

# Read Model Extension Points

Proposal puede incorporar nuevas proyecciones de lectura.

Estas extensiones deben respetar:

```text
DOMAIN-007L-Read-Model.md
```

Los Read Models permanecen:

- derivados;
- reconstruibles;
- de solo lectura;
- desacoplados del Aggregate.

---

# Nuevas Proyecciones

Pueden incorporarse nuevas vistas cuando exista una necesidad
concreta de consulta.

Ejemplos conceptuales:

```text
ProposalByTerritory

ProposalByAssembly

ProposalReviewQueue

ProposalParticipationSummary

ProposalVotingSummary

ProposalTimeline
```

Estas vistas representan posibles extensiones.

No modifican el Aggregate.

---

# Proyecciones Analíticas

Pueden incorporarse vistas para:

- indicadores;
- estadísticas;
- tendencias;
- distribución territorial;
- participación;
- seguimiento organizacional.

Estas proyecciones no deben introducir lógica de negocio en el lado
de lectura.

---

# Nuevas Consultas

La incorporación de una consulta no requiere agregar comportamiento
al Aggregate cuando la consulta puede resolverse mediante un Read
Model.

Debe mantenerse:

```text
Query Requirement

↓

Read Model
```

y no:

```text
Query Requirement

↓

Aggregate Expansion
```

cuando la necesidad sea exclusivamente de lectura.

---

# Reconstrucción de Nuevas Proyecciones

Toda nueva proyección debe poder reconstruirse desde las fuentes
oficiales definidas por la arquitectura.

Conceptualmente:

```text
Domain Events

↓

Projection

↓

New Read Model
```

Una proyección no debe convertirse en una segunda fuente de verdad
del lado de escritura.

---

# Security Extension Points

Las extensiones de seguridad deben respetar:

```text
DOMAIN-007O-Security-Model.md
```

Pueden evolucionar:

- Permissions;
- políticas de lectura;
- políticas de privacidad;
- tipos de actor;
- capacidades organizacionales;
- contratos de exposición.

No pueden eliminarse las protecciones estructurales del Aggregate.

---

# Nuevos Tipos de Actor

El modelo de autorización puede evolucionar incorporando nuevos
tipos de actor.

La incorporación no debe modificar el significado de Proposal.

Los nuevos actores continúan sujetos a:

- Permissions;
- Lifecycle;
- State Machine;
- Invariants;
- Version;
- Consistency Boundary.

---

# Nuevas Políticas de Privacidad

Las necesidades de privacidad pueden evolucionar.

Pueden incorporarse:

- nuevas vistas limitadas;
- anonimización;
- reducción de campos;
- políticas de exposición;
- contratos especializados.

Estas capacidades deben permanecer separadas de la identidad y
consistencia del Aggregate.

---

# Nuevos Mecanismos Técnicos de Seguridad

Cambiar o incorporar:

```text
OAuth

JWT

MFA

Identity Provider

PEP Proxy
```

no constituye una extensión del Aggregate.

Estas tecnologías pertenecen a Infrastructure.

Proposal permanece independiente de ellas.

---

# Performance Extension Points

Las optimizaciones deben respetar:

```text
DOMAIN-007N-Performance-Rules.md
```

Pueden incorporarse:

- nuevas proyecciones;
- índices;
- cachés;
- estrategias de consulta;
- particionamiento;
- procesamiento asíncrono;
- optimizaciones de persistencia.

Estas decisiones no deben modificar el significado del dominio.

---

# Regla de Performance

Debe mantenerse:

```text
Optimization

≠

Domain Model Change
```

Una optimización no puede justificar:

- bypass del Aggregate;
- eliminación de invariantes;
- eliminación de Version;
- modificación directa de persistencia;
- absorción de otros Aggregates.

---

# Caché como Extension Point

La incorporación de caché pertenece a Infrastructure o al lado de
lectura.

La caché no constituye:

```text
Proposal Source of Truth
```

ni:

```text
Authorization Source
```

El Aggregate continúa siendo la fuente conceptual de verdad del
lado de escritura.

---

# Event-Driven Extension Points

Nuevos consumidores pueden reaccionar a Domain Events sin
modificar Proposal.

Ejemplo:

```text
ProposalAccepted

        │

        ├── Notification

        ├── Audit

        ├── Analytics

        └── Integration
```

La incorporación de nuevos consumidores no amplía el límite del
Aggregate.

---

# Nuevas Reacciones

Una nueva reacción a un evento debe pertenecer al componente o
Bounded Context responsable.

Proposal no debe incorporar comportamiento externo únicamente para
coordinar consumidores.

La arquitectura Event-Driven permite extender reacciones sin
modificar el productor cuando el contrato existente es suficiente.

---

# Application Extension Points

Los Application Services pueden evolucionar para coordinar nuevos
casos de uso.

Un Application Service puede:

- cargar Proposal;
- resolver autorización;
- ejecutar Commands;
- coordinar otros Aggregates;
- persistir;
- publicar eventos;
- iniciar integraciones.

No debe contener invariantes que pertenecen al Aggregate.

---

# Orquestación

Cuando un nuevo caso de uso requiera múltiples Aggregates:

```text
Application Service

        │

        ├── Proposal

        ├── Assembly

        ├── Participation

        └── Voting
```

la coordinación ocurre fuera de Proposal.

Esto preserva los límites de consistencia.

---

# Coordinación Eventual

Una extensión puede requerir coordinación eventual entre
Aggregates.

Conceptualmente:

```text
Proposal Domain Event

↓

External Reaction

↓

Command to Another Aggregate
```

El segundo Aggregate evalúa sus propias:

- Permissions;
- invariantes;
- State Machine;
- Version;
- consistencia.

---

# Saga y Procesos Distribuidos

Si una futura necesidad requiere coordinación distribuida de larga
duración, dicha coordinación no debe incorporarse como estado
interno de Proposal salvo que el concepto pertenezca realmente a
su responsabilidad.

Proposal continúa representando su propio límite.

La coordinación pertenece al nivel arquitectónico correspondiente.

---

# Extension Points y Ubiquitous Language

Toda extensión debe incorporarse primero al lenguaje ubicuo.

Un nuevo concepto debe poseer:

- nombre claro;
- significado único;
- contexto;
- responsabilidad;
- relación con conceptos existentes.

No deben incorporarse términos técnicos como sustitutos de
conceptos del dominio.

---

# Regla de Lenguaje

Debe preferirse:

```text
SubmitProposal
```

sobre:

```text
UpdateStatusToSubmitted
```

y:

```text
ProposalAccepted
```

sobre:

```text
ProposalRowUpdated
```

El lenguaje de extensión debe expresar el dominio.

---

# Extension Points y Bounded Context

Una extensión debe evaluarse dentro del Bounded Context:

```text
Proposal Management
```

Si el concepto pertenece principalmente a otro contexto, debe
mantenerse fuera de Proposal.

La proximidad funcional no implica propiedad del modelo.

---

# Criterios para Crear un Nuevo Aggregate

Una extensión debe evaluarse como nuevo Aggregate cuando el nuevo
concepto posea:

- identidad propia;
- Lifecycle propio;
- State Machine propia;
- invariantes propias;
- Repository propio;
- consistencia propia;
- comportamiento independiente;
- capacidad de existir fuera de Proposal.

En ese caso no debe incorporarse como entidad interna por
conveniencia.

---

# Criterios para Crear un Nuevo Value Object

Un concepto puede incorporarse como Value Object cuando:

- no posee identidad;
- su valor define completamente su significado;
- es inmutable;
- pertenece a Proposal;
- protege reglas propias de valor.

---

# Criterios para Crear una Entidad Interna

Una entidad interna solo puede incorporarse cuando:

- pertenece exclusivamente a Proposal;
- su Lifecycle está controlado por Proposal;
- no requiere Repository propio;
- no puede existir independientemente;
- requiere consistencia fuerte con Proposal.

La entidad permanece inaccesible para modificación externa.

---

# Criterios para Mantener una Referencia Externa

Debe utilizarse una referencia mediante identificador cuando el
concepto:

- pertenece a otro Aggregate;
- posee identidad independiente;
- posee Lifecycle independiente;
- puede evolucionar separadamente;
- no requiere consistencia transaccional interna con Proposal.

Ejemplo:

```text
AssemblyId

TerritoryId

DocumentId

VotingId
```

---

# Compatibilidad hacia Atrás

Las extensiones deben preservar el significado de contratos
existentes cuando sea posible.

No debe cambiarse silenciosamente:

- significado de Commands;
- significado de Domain Events;
- significado de estados;
- significado de Permissions;
- significado de campos;
- semántica de Version.

Cuando una evolución sea incompatible debe tratarse explícitamente
como evolución contractual.

---

# Evolución de Commands

Un Command existente no debe adquirir silenciosamente una
responsabilidad diferente.

Si una nueva intención posee significado distinto debe evaluarse
la creación de un nuevo Command.

Esto preserva:

- claridad;
- trazabilidad;
- auditoría;
- lenguaje ubicuo.

---

# Evolución de Domain Events

Un Domain Event histórico conserva su significado.

No debe reutilizarse el mismo nombre para representar un hecho
diferente.

Cuando el dominio evolucione debe mantenerse la semántica histórica
necesaria para reconstrucción y consumo.

---

# Evolución de Read Models

Los Read Models pueden evolucionar con mayor libertad debido a su
naturaleza derivada.

Pueden:

- incorporar campos;
- eliminar campos;
- dividirse;
- combinarse;
- reconstruirse;
- optimizarse.

Estas modificaciones no cambian el Aggregate.

---

# Evolución de Integration Events

Los Integration Events deben evolucionar como contratos externos.

Una modificación debe considerar:

- consumidores existentes;
- significado;
- compatibilidad;
- versionado contractual;
- minimización de información.

El Aggregate no debe modificarse únicamente para mantener una forma
específica de Payload externo.

---

# Evolución de Permissions

Las Permissions pueden ampliarse conforme aparezcan nuevas
capacidades.

Una Permission existente no debe reinterpretarse arbitrariamente
para otorgar capacidades no relacionadas.

Debe mantenerse el principio de mínimo privilegio.

---

# Evolución de Invariantes

Las invariantes representan reglas fundamentales del dominio.

Modificar una invariante no constituye una extensión trivial.

Debe evaluarse explícitamente su impacto sobre:

```text
Aggregate

Lifecycle

State Machine

Commands

Domain Events

Repository

Versioning

Read Models

Integrations

Tests

Security
```

Una modificación de invariantes representa una evolución
significativa del modelo.

---

# Evolución del Lifecycle

Agregar, eliminar o reinterpretar estados requiere revisar:

```text
DOMAIN-007A-Lifecycle.md

DOMAIN-007B-State-Machine.md

DOMAIN-007C-Commands.md

DOMAIN-007D-Domain-Events.md

DOMAIN-007E-Invariants.md

DOMAIN-007F-Permissions.md

DOMAIN-007M-Test-Scenarios.md
```

El Lifecycle no debe evolucionar de manera aislada.

---

# Evolución del Consistency Boundary

Modificar el límite de consistencia constituye una decisión
arquitectónica significativa.

No debe realizarse como extensión ordinaria.

Debe evaluarse explícitamente:

- propiedad del concepto;
- atomicidad requerida;
- invariantes;
- tamaño del Aggregate;
- acoplamiento;
- concurrencia;
- transacciones;
- comportamiento.

El límite existente debe preservarse mientras no exista una razón
de dominio formal para modificarlo.

---

# Extension Points Prohibidos

No constituyen Extension Points válidos:

```text
Direct Database Mutation

Generic Aggregate Patch

SetStatus

SetVersion

ForceTransition

SkipInvariantValidation

SkipPermissionValidation

CrossAggregateTransaction by Convenience

Embed External Aggregate

Infrastructure Dependency in Domain
```

Estos mecanismos rompen las reglas consolidadas del Aggregate.

---

# Regla de No Bypass

Ninguna extensión puede crear una ruta alternativa:

```text
External Input

↓

Direct Proposal State
```

Debe mantenerse:

```text
External Intent

↓

Application

↓

Authorized Command

↓

Proposal Behavior

↓

Invariant Validation

↓

State Change

↓

Domain Event
```

---

# Regla de No Infraestructura

Una extensión del dominio no debe incorporar dependencias hacia:

- HTTP;
- REST;
- GraphQL;
- FastAPI;
- Django;
- React;
- Flutter;
- MongoDB;
- PostgreSQL;
- Redis;
- Kafka;
- RabbitMQ;
- FIWARE;
- Keyrock;
- PEP Proxy;
- OAuth;
- JWT.

Estas tecnologías pueden implementar Ports y Adapters.

No forman parte de Proposal.

---

# Regla de No Framework

El significado de una extensión no debe depender de un Framework.

Debe ser posible describir el nuevo comportamiento utilizando
únicamente lenguaje del dominio.

Si una extensión solo puede explicarse mediante una tecnología,
probablemente no pertenece al Aggregate.

---

# Regla de No Persistencia como Dominio

Una necesidad de base de datos no constituye por sí misma una
necesidad del dominio.

Ejemplo:

```text
Need New Database Index
```

no implica:

```text
Need New Proposal Attribute
```

Las decisiones deben permanecer separadas.

---

# Regla de No UI como Dominio

Una necesidad visual no debe introducir automáticamente nuevos
estados o atributos.

Ejemplo:

```text
UI needs a blue badge
```

no implica:

```text
ProposalStatus = Blue
```

Un nuevo concepto debe existir primero dentro del lenguaje del
dominio.

---

# Regla de No Integración como Dominio

Un sistema externo puede requerir un campo que no pertenece a
Proposal.

En ese caso debe evaluarse:

```text
Integration Mapping
```

antes de modificar el Aggregate.

El dominio no debe deformarse para reproducir modelos externos.

---

# Regla de No Analytics como Dominio

Las necesidades analíticas no deben introducir agregaciones
estadísticas dentro de Proposal.

Debe preferirse:

```text
Domain Events

↓

Analytics Projection
```

Las estadísticas permanecen fuera del Aggregate.

---

# Regla de No Auditoría como Estado Interno

La necesidad de mayor auditoría no debe convertir el historial de
Audit en una colección interna de Proposal.

Debe mantenerse:

```text
Proposal

↓

Domain Events

↓

Audit
```

---

# Regla de No Notification como Estado Interno

Agregar un nuevo canal de comunicación no modifica Proposal.

Ejemplo:

```text
Email

SMS

Push

Messaging
```

pertenece a Notification o Infrastructure.

Proposal únicamente produce los hechos correspondientes.

---

# Regla de No Voting como Estado Interno

Nuevas modalidades de votación no deben incorporarse dentro de
Proposal.

Voting mantiene su propio Aggregate.

Proposal puede mantener la relación necesaria mediante identidad.

---

# Regla de No Participation como Estado Interno

Nuevos mecanismos participativos no convierten Participation en
parte de Proposal.

Ambos Aggregates pueden evolucionar de manera independiente.

---

# Regla de No Assembly como Estado Interno

La existencia de una Proposal dentro del contexto de una Assembly
no convierte Assembly en parte de Proposal.

La relación debe preservar los límites establecidos.

---

# Regla de No Document como Estado Interno

Agregar archivos, actas, anexos o evidencias no debe convertir el
Aggregate Document en una entidad interna de Proposal.

Proposal puede mantener:

```text
DocumentId
```

cuando corresponda.

---

# Regla de No Territory como Estado Interno

La relación territorial no permite que Proposal administre:

- geometría;
- jerarquía territorial;
- límites;
- clasificación territorial;
- Lifecycle de Territory.

Estas responsabilidades permanecen en Territory.

---

# Testing de Extensiones

Toda extensión debe incorporar escenarios de prueba conceptuales
cuando modifique comportamiento.

Debe verificarse:

- camino válido;
- estado inválido;
- permiso inválido;
- invariante violada;
- Version incorrecta;
- estado terminal;
- aislamiento organizacional;
- eventos generados;
- ausencia de efectos inválidos;
- preservación del Consistency Boundary.

Los escenarios deben incorporarse conforme a:

```text
DOMAIN-007M-Test-Scenarios.md
```

---

# Performance de Extensiones

Toda extensión debe evaluar su impacto sobre:

- tamaño del Aggregate;
- frecuencia de escritura;
- frecuencia de lectura;
- concurrencia;
- número de eventos;
- proyecciones;
- integraciones.

La optimización debe respetar:

```text
DOMAIN-007N-Performance-Rules.md
```

---

# Seguridad de Extensiones

Toda extensión debe evaluar:

```text
Who can execute it?

What information can it expose?

What state can it modify?

What invariants protect it?

What events does it produce?

What external consumers receive it?
```

Las respuestas deben mantenerse coherentes con:

```text
DOMAIN-007O-Security-Model.md
```

---

# Checklist Conceptual de Extensión

Antes de aceptar una extensión debe verificarse:

```text
[ ] El concepto pertenece a Proposal.

[ ] Utiliza lenguaje ubicuo.

[ ] No absorbe otro Aggregate.

[ ] Mantiene Proposal como Aggregate Root.

[ ] Preserva ProposalId.

[ ] Preserva OrganizationId según sus reglas.

[ ] Respeta Lifecycle.

[ ] Respeta State Machine.

[ ] Respeta Invariants.

[ ] Respeta Permissions.

[ ] Respeta Version.

[ ] Respeta Consistency Boundary.

[ ] Define Commands cuando corresponde.

[ ] Define Domain Events cuando corresponde.

[ ] Evalúa Read Models.

[ ] Evalúa Integration Events.

[ ] Evalúa Security.

[ ] Evalúa Performance.

[ ] Evalúa Test Scenarios.

[ ] No introduce Infrastructure en Domain.

[ ] No introduce Frameworks en Domain.

[ ] No crea setters genéricos.

[ ] No crea bypass de comportamiento.

[ ] No utiliza modelos externos como modelo interno.

[ ] Mantiene trazabilidad.
```

---

# Proceso Conceptual de Extensión

```text
New Domain Requirement

        │

        ▼

Ubiquitous Language Analysis

        │

        ▼

Ownership Analysis

        │

        ├──────── Belongs to another Aggregate
        │
        │
        └────────► External Reference / Event
        │

        ▼

Belongs to Proposal

        │

        ▼

Consistency Analysis

        │

        ▼

Behavior / Value Object / Policy

        │

        ▼

Lifecycle Impact

        │

        ▼

Invariant Impact

        │

        ▼

Permission Impact

        │

        ▼

Command

        │

        ▼

Domain Event

        │

        ▼

Version Impact

        │

        ▼

Read Model Impact

        │

        ▼

Integration Impact

        │

        ▼

Security Impact

        │

        ▼

Test Scenarios

        │

        ▼

Official Domain Extension
```

---

# Escenario — Nuevo Tipo de Proposal

## Given

El dominio identifica una nueva clasificación legítima de
Proposal.

## When

Se incorpora el nuevo tipo.

## Then

Debe mantenerse:

- ProposalId;
- Aggregate Root;
- OrganizationId;
- Lifecycle;
- State Machine;
- Version;
- Repository;
- Consistency Boundary.

Las reglas específicas del nuevo tipo deben documentarse cuando
corresponda.

---

# Escenario — Nuevo Command

## Given

El dominio requiere una nueva operación.

## When

Se incorpora un nuevo Command.

## Then

deben definirse:

```text
Intent

Actor

Permission

Allowed State

Preconditions

Invariants

State Change

Version Change

Domain Event
```

La operación no puede introducir modificación directa.

---

# Escenario — Nuevo Estado

## Given

El dominio identifica una nueva condición significativa del
Lifecycle.

## When

Se incorpora un nuevo estado.

## Then

deben actualizarse coherentemente:

```text
Lifecycle

State Machine

Commands

Domain Events

Invariants

Permissions

Tests
```

No debe agregarse el estado aisladamente.

---

# Escenario — Nueva Relación con Otro Aggregate

## Given

Proposal requiere relacionarse con otro Aggregate.

## When

Se incorpora la relación.

## Then

debe utilizarse:

```text
ExternalAggregateId
```

cuando corresponda.

El Aggregate externo no se incorpora dentro de Proposal.

---

# Escenario — Nueva Integración Municipal

## Given

Una plataforma municipal requiere información de Proposal.

## When

se incorpora la integración.

## Then

debe utilizarse:

```text
Proposal

↓

Domain Event

↓

Integration Event

↓

Municipal Adapter
```

Proposal no depende de la API municipal.

---

# Escenario — Nueva Representación FIWARE

## Given

AURA necesita representar Proposal mediante NGSI-LD.

## When

se crea la representación.

## Then

debe mantenerse:

```text
Proposal Aggregate

≠

NGSI-LD Entity
```

La transformación pertenece al Adapter correspondiente.

---

# Escenario — Nueva Vista Analítica

## Given

Se requiere conocer propuestas por territorio.

## When

se incorpora la consulta.

## Then

puede crearse:

```text
ProposalByTerritory
```

como Read Model.

No debe incorporarse una colección estadística dentro de cada
Proposal.

---

# Escenario — Nueva Regla Organizacional

## Given

Una Organization requiere una condición adicional para presentar
Proposal.

## When

la regla pertenece al dominio y es compatible con Proposal.

## Then

puede representarse mediante una política explícita.

La política no puede violar invariantes estructurales.

---

# Escenario — Nuevo Sistema Externo

## Given

Un nuevo sistema necesita consumir información de Proposal.

## When

el contrato existente resulta suficiente.

## Then

el nuevo consumidor puede incorporarse sin modificar Proposal.

La extensibilidad ocurre fuera del Aggregate.

---

# Escenario — Concepto con Identidad Propia

## Given

Una nueva necesidad introduce un concepto que posee:

- identidad;
- Lifecycle;
- invariantes;
- Repository;
- comportamiento independiente.

## When

se evalúa su incorporación.

## Then

no debe introducirse automáticamente como entidad interna.

Debe evaluarse como Aggregate independiente.

---

# Escenario — Necesidad Exclusiva de UI

## Given

una interfaz necesita una nueva forma de representar Proposal.

## When

la necesidad no corresponde a un concepto del dominio.

## Then

no debe modificarse Proposal.

La solución pertenece a Presentation o Read Model.

---

# Escenario — Necesidad Exclusiva de Persistencia

## Given

la base de datos requiere una optimización.

## When

la optimización no modifica el significado del dominio.

## Then

no debe modificarse Proposal.

La decisión pertenece a Infrastructure.

---

# Escenario — Necesidad Exclusiva de Integración

## Given

un sistema externo requiere una estructura distinta.

## When

la estructura no pertenece al dominio.

## Then

debe utilizarse un Adapter o Integration Mapping.

Proposal permanece sin cambios.

---

# Escenario — Extensión que Viola Invariantes

## Given

una nueva capacidad requiere ignorar una invariante existente.

## When

se intenta incorporarla como Extension Point.

## Then

no debe considerarse una extensión ordinaria.

Debe revisarse explícitamente el modelo de dominio y la invariante
afectada.

---

# Escenario — Extensión que Amplía la Transacción

## Given

una nueva operación pretende modificar Proposal y Voting dentro de
la misma frontera por conveniencia.

## When

se evalúa la extensión.

## Then

debe rechazarse como extensión ordinaria del Aggregate.

Proposal y Voting conservan sus límites de consistencia.

---

# Escenario — Extensión de Seguridad

## Given

se incorpora una nueva Permission.

## When

se aplica a un nuevo Command.

## Then

el Command continúa sujeto a:

```text
Permission

+

Lifecycle

+

State Machine

+

Invariants

+

Version
```

La nueva Permission no crea una excepción estructural.

---

# Escenario — Extensión de Performance

## Given

se incorpora una caché para mejorar consultas.

## When

la caché contiene información de Proposal.

## Then

debe mantenerse:

```text
Cache

≠

Proposal Aggregate
```

y:

```text
Cache

≠

Write Source of Truth
```

---

# Gobernanza de Extensiones

Toda extensión conceptual debe mantener coherencia con la
documentación oficial del Aggregate.

Cuando una extensión afecte varios artefactos, todos los documentos
afectados deben evolucionar de forma consistente.

No debe existir una definición oficial en:

```text
DOMAIN-007C-Commands.md
```

que contradiga:

```text
DOMAIN-007B-State-Machine.md
```

o:

```text
DOMAIN-007E-Invariants.md
```

La documentación conceptual constituye una unidad coherente.

---

# Coherencia Documental

Una extensión puede requerir actualizar:

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

DOMAIN-007L-Read-Model.md

DOMAIN-007M-Test-Scenarios.md

DOMAIN-007N-Performance-Rules.md

DOMAIN-007O-Security-Model.md

DOMAIN-007P-Extension-Points.md
```

Solo deben modificarse los documentos realmente afectados por la
extensión.

---

# Regla de Fuente Conceptual

La definición del Aggregate permanece distribuida entre los
documentos oficiales de DOMAIN-007.

Los Extension Points no sustituyen las reglas existentes.

Este documento define únicamente cómo puede evolucionar el modelo
sin violar dichas reglas.

Una posibilidad de extensión no constituye automáticamente una
capacidad existente.

Debe mantenerse:

```text
Extension Point

≠

Implemented Domain Capability
```

---

# Regla de No Inferencia

La existencia de un Extension Point no autoriza a incorporar
automáticamente nuevas reglas al Aggregate.

Toda nueva capacidad debe surgir de una definición explícita del
dominio.

No debe inferirse una decisión arquitectónica únicamente porque
sea técnicamente posible o común en otros sistemas.

---

# Regla de Evolución Explícita

Toda evolución que modifique conceptos oficiales debe declararse
explícitamente.

No debe modificarse silenciosamente:

- identidad;
- responsabilidad;
- Lifecycle;
- estados;
- transiciones;
- invariantes;
- Permissions;
- consistencia;
- significado de eventos;
- significado de Commands.

La evolución del dominio debe permanecer trazable.

---

# Límites de Extensibilidad

Proposal puede evolucionar ampliamente mientras continúe
representando la misma responsabilidad fundamental.

La extensibilidad termina cuando el nuevo concepto exige cambiar
sustancialmente:

```text
Identity

Ownership

Lifecycle

Consistency Boundary

Responsibility
```

En ese punto debe evaluarse una nueva separación de dominio en
lugar de continuar ampliando Proposal.

---

# Principios Arquitectónicos

Los Extension Points mantienen:

```text
Extension

≠

Boundary Violation
```

```text
New Requirement

≠

Automatic Aggregate Expansion
```

```text
External Model

≠

Domain Model
```

```text
New Integration

≠

New Domain Dependency
```

```text
New Query

≠

New Aggregate Behavior
```

```text
New UI Requirement

≠

New Domain State
```

```text
New Database Requirement

≠

New Domain Concept
```

```text
New Consumer

≠

Aggregate Modification
```

```text
New Permission

≠

Invariant Exception
```

```text
New Command

≠

Generic Mutation
```

```text
New State

≠

Presentation Label
```

```text
New Relationship

≠

Aggregate Absorption
```

```text
Extension Point

≠

Existing Capability
```

```text
Optimization

≠

Consistency Reduction
```

```text
Interoperability

≠

Domain Coupling
```

---

# Compatibilidad Arquitectónica

Los Extension Points de Proposal son compatibles con:

- Domain-Driven Design;
- Clean Architecture;
- Hexagonal Architecture;
- SOLID;
- CQRS;
- Event Sourcing;
- Event-Driven Architecture;
- arquitectura distribuida;
- interoperabilidad basada en contratos.

La extensibilidad se obtiene mediante evolución explícita del
dominio y desacoplamiento de responsabilidades.

No mediante relajación de límites.

---

# Documentación Complementaria

Los Extension Points deben interpretarse conjuntamente con:

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

DOMAIN-007L-Read-Model.md

DOMAIN-007M-Test-Scenarios.md

DOMAIN-007N-Performance-Rules.md

DOMAIN-007O-Security-Model.md
```

Cada documento protege una dimensión específica del Aggregate.

Las extensiones deben mantener coherencia entre todas las
dimensiones afectadas.

---

# Definición de Éxito

Los Extension Points del Aggregate **Proposal** permiten que el
modelo evolucione frente a nuevas necesidades organizacionales,
territoriales, participativas, municipales, de interoperabilidad y
de consulta sin comprometer los principios fundamentales del
dominio.

Una extensión válida mantiene:

```text
ProposalId

Aggregate Root

Organization Boundary

Lifecycle

State Machine

Invariants

Permissions

Version

Consistency Boundary

Repository Contract

Domain Events

Security Model
```

Proposal puede incorporar nuevos comportamientos, Value Objects,
Commands, Domain Events, Permissions, políticas, relaciones por
identidad, Read Models e Integration Events cuando el dominio lo
requiera explícitamente.

Las extensiones externas pueden incorporar nuevos consumidores,
proyecciones, plataformas municipales, sistemas Smart City,
representaciones FIWARE y contratos de interoperabilidad sin
introducir dependencias tecnológicas dentro del Aggregate.

Los Extension Points no autorizan inferencias automáticas ni
decisiones arquitectónicas implícitas.

Toda evolución debe surgir de una necesidad explícita del dominio,
utilizar el lenguaje ubicuo, preservar la responsabilidad de
Proposal y mantener separados los Aggregates Organization,
Citizen, Membership, Role, Territory, Assembly, Participation,
Voting, Document, Notification, Audit e Integration.

De esta forma, `DOMAIN-007P-Extension-Points.md` constituye la
definición conceptual oficial para la evolución controlada del
Aggregate **Proposal**, garantizando que AURA pueda ampliar sus
capacidades sin degradar los límites de consistencia, la
independencia tecnológica, la trazabilidad ni la arquitectura DDD
consolidada de AURA Core.