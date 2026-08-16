# DOMAIN-013 — Integration Aggregate

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Integration Management

Aggregate:
Integration

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
- DOMAIN-011-Aggregate.md
- DOMAIN-012-Aggregate.md

---

# Objetivo

El Aggregate **Integration** representa una unidad formal de
interoperabilidad reconocida por AURA.

Su responsabilidad es preservar el significado de una relación de
integración sin incorporar dentro del dominio los detalles técnicos
utilizados para transportarla o implementarla.

Integration permite que AURA pueda relacionarse conceptualmente con:

- otros Bounded Contexts;
- sistemas municipales;
- plataformas institucionales;
- ecosistemas Smart City;
- FIWARE;
- sistemas externos autorizados.

manteniendo independencia entre el Domain Model y la tecnología de
interoperabilidad.

Debe mantenerse:

```text
Integration

≠

Infrastructure Adapter
```

y:

```text
Integration

≠

External System
```

---

# Propósito

El propósito del Aggregate Integration es proporcionar un límite de
dominio para representar una integración reconocida por AURA sin
transferir ownership entre los contextos involucrados.

Integration debe permitir preservar conceptualmente:

- identidad propia;
- relación con contratos de integración;
- referencias a los contextos involucrados;
- reglas propias de la integración;
- estado propio cuando sea definido formalmente;
- trazabilidad de cambios relevantes;
- Version;
- Domain Events propios cuando sean definidos;
- independencia respecto de Infrastructure.

Integration no constituye una implementación de transporte.

---

# Definición

Una Integration representa una relación formal de interoperabilidad
administrada por AURA.

Puede existir cuando AURA necesita intercambiar información con:

```text
Internal Bounded Context

External Bounded Context

Municipal System

Institutional Platform

Smart City Platform

FIWARE

Authorized External System
```

siempre mediante contratos explícitos.

La existencia de una Integration no implica que los sistemas
relacionados formen parte del mismo Consistency Boundary.

---

# Principio Fundamental

Debe mantenerse:

```text
Integration

=

Domain Representation of Interoperability
```

mientras:

```text
Adapter

Protocol

Broker

Transport

SDK

API Client

=

Infrastructure Concerns
```

---

# Responsabilidades

Integration es responsable conceptualmente de:

- preservar su propia identidad;
- representar una integración reconocida por el dominio;
- mantener referencias necesarias a los participantes de la
  integración;
- proteger sus propias Invariants;
- proteger su propio Lifecycle;
- proteger su propia Version;
- expresar comportamiento mediante Commands;
- producir Domain Events cuando corresponda;
- mantener trazabilidad de su propia evolución;
- colaborar mediante contratos explícitos;
- permanecer independiente de tecnologías concretas.

---

# Responsabilidades Fuera del Aggregate

Integration no es responsable de:

- implementar HTTP;
- implementar REST;
- implementar GraphQL;
- implementar MQTT;
- implementar AMQP;
- administrar brokers;
- administrar bases de datos;
- administrar colas técnicas;
- serializar mensajes;
- administrar SDKs;
- administrar conexiones de red;
- administrar certificados;
- administrar tokens;
- administrar secretos;
- autenticar usuarios;
- autenticar servicios;
- ejecutar lógica propia de otros Aggregates;
- modificar directamente sistemas externos;
- modificar directamente otros Aggregates.

Estas responsabilidades pertenecen a capas o contextos externos.

---

# Aggregate Root

La única Aggregate Root es:

```text
Integration
```

Toda modificación sobre una Integration debe realizarse mediante la
Aggregate Root.

Ningún consumidor externo puede modificar directamente el estado
interno del Aggregate.

La Aggregate Root protege:

- IntegrationId;
- su estado cuando corresponda;
- sus referencias;
- sus Invariants;
- su Version;
- sus timestamps;
- su comportamiento;
- sus Domain Events.

---

# Identidad

La identidad del Aggregate está determinada por:

```text
IntegrationId
```

IntegrationId:

- identifica una única Integration;
- es único;
- es inmutable;
- no debe reutilizarse para representar otra Integration;
- no depende de Infrastructure;
- no depende del identificador de un sistema externo;
- no depende de un Domain Event;
- no depende de un Integration Event.

Debe mantenerse:

```text
IntegrationId

≠

ExternalSystemId
```

cuando exista una identidad externa.

---

# Ownership

Integration posee únicamente la información necesaria para
representar su propia existencia y comportamiento.

No posee:

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

Notification

Audit
```

Estos conceptos permanecen bajo ownership de sus respectivos
Aggregates y Bounded Contexts.

---

# Relación con Sistemas Externos

Un sistema externo no forma parte del Aggregate Integration.

Debe mantenerse:

```text
External System Reference

≠

Embedded External System
```

Integration puede preservar solamente la referencia o información
conceptual necesaria conforme al contrato correspondiente.

---

# Relación con Bounded Contexts

Integration no absorbe los Bounded Contexts que conecta.

Debe mantenerse:

```text
Integration between A and B

≠

Merge A and B
```

Cada Bounded Context conserva:

- ownership;
- identidad;
- reglas;
- Lifecycle;
- Invariants;
- Repository;
- Consistency Boundary.

---

# Contrato de Integración

Toda colaboración de Integration debe basarse en un contrato
explícito.

Debe mantenerse:

```text
Integration

requires

Explicit Contract
```

El contrato define la semántica intercambiada.

La tecnología utilizada para materializarlo pertenece a capas
externas.

---

# Integration Contract

Un Integration Contract no equivale al Aggregate.

Debe mantenerse:

```text
Integration Contract

≠

Integration Aggregate
```

El Aggregate puede gobernar una relación de integración.

El contrato define información o hechos compartidos.

---

# Domain Event

Un Domain Event pertenece al Aggregate que produjo el hecho.

Integration no adquiere ownership sobre eventos de otros Aggregates.

Debe mantenerse:

```text
Source Domain Event

remains owned by

Source Aggregate
```

---

# Domain Event versus Integration Event

Debe mantenerse:

```text
Domain Event

≠

Integration Event
```

Un Domain Event expresa un hecho dentro del dominio productor.

Un Integration Event expresa un contrato destinado a cruzar una
frontera de integración cuando exista una necesidad explícita.

---

# Integration Event

Integration Events permiten comunicar hechos entre Bounded Contexts
o sistemas sin exponer directamente el modelo interno del Aggregate
productor.

Debe mantenerse:

```text
Integration Event

=

Integration Contract Fact
```

y no:

```text
Integration Event

=

Direct Aggregate Mutation
```

---

# No Publicación Automática

La existencia de un Domain Event no obliga automáticamente a generar
un Integration Event.

Debe mantenerse:

```text
Domain Event

≠

Mandatory Integration Event
```

Solamente deben atravesar la frontera los hechos requeridos por un
contrato explícito.

---

# Transformación

Conceptualmente:

```text
Domain Event
    │
    ▼
Integration Boundary
    │
    ▼
Integration Contract
    │
    ▼
Integration Event
    │
    ▼
Consumer
```

Esta representación no define una tecnología de implementación.

---

# Consumo de Información Externa

Un mensaje proveniente de un sistema externo no debe convertirse
automáticamente en un concepto interno de AURA.

Debe mantenerse:

```text
External Message

≠

AURA Domain Fact
```

La equivalencia semántica debe estar definida explícitamente.

---

# Anti-Corruption Boundary

Cuando un modelo externo posea semántica diferente de AURA, debe
preservarse la separación conceptual.

Conceptualmente:

```text
External Model
    │
    ▼
Translation Boundary
    │
    ▼
AURA Contract
```

La traducción no transfiere ownership del modelo externo al
Aggregate Integration.

---

# Independencia Semántica

Integration debe proteger el lenguaje ubicuo de AURA.

Un nombre, estado o estructura externa no debe incorporarse
automáticamente como concepto interno únicamente porque exista en el
sistema integrado.

---

# Atributos Conceptuales

Integration mantiene conceptualmente la información mínima necesaria
para proteger su identidad y evolución.

La versión 1.0 establece como núcleo:

```text
IntegrationId

Version

CreatedAt

UpdatedAt
```

y las referencias o datos adicionales que sean definidos
formalmente por los contratos específicos del dominio.

Este documento no introduce por inferencia atributos específicos de:

- protocolo;
- endpoint;
- broker;
- tópico;
- queue;
- database;
- FIWARE;
- NGSI-LD;
- sistema municipal.

---

# IntegrationId

IntegrationId identifica la unidad Integration.

Es:

- único;
- inmutable;
- independiente de Infrastructure;
- distinto de identidades externas.

---

# Version

Version representa la evolución lógica del Aggregate.

Toda modificación válida que sea definida por el dominio debe
mantener coherencia con:

```text
DOMAIN-013I-Versioning.md
```

La infraestructura no decide arbitrariamente Version.

---

# CreatedAt

CreatedAt representa el momento de creación de la Integration.

Una vez establecido:

```text
CreatedAt
```

permanece inmutable.

---

# UpdatedAt

UpdatedAt representa el momento de la última modificación válida del
Aggregate.

Una lectura o una operación rechazada no debe modificar UpdatedAt.

---

# Atributos no Definidos

Este documento no establece todavía como atributos obligatorios:

```text
Protocol

Endpoint

Topic

Queue

ExternalUrl

AccessToken

ApiKey

Secret

ClientId

ClientSecret

Certificate

FIWAREEntity

NGSI-LDContext
```

La presencia técnica de cualquiera de estos elementos no constituye
una regla del Aggregate.

---

# Credenciales

Integration no almacena credenciales como información de dominio.

Debe mantenerse:

```text
Password

AccessToken

RefreshToken

ApiKey

PrivateKey

Secret

ClientSecret

∉

Integration Aggregate
```

---

# Entidades Internas

La versión 1.0 de este documento no establece entidades internas
concretas para Integration.

Una Internal Entity solamente deberá introducirse cuando exista una
necesidad explícita de:

- identidad interna;
- comportamiento interno;
- Lifecycle interno;
- consistencia dentro del Aggregate.

No debe inventarse una Internal Entity para representar
Infrastructure.

---

# Value Objects

La versión 1.0 de este documento no clasifica todavía Value Objects
específicos de Integration.

Una futura definición deberá justificar cada Value Object mediante
semántica propia de dominio.

No debe utilizarse un Value Object para introducir:

- configuración de framework;
- credenciales;
- objetos SDK;
- conexiones;
- clientes HTTP;
- detalles de broker.

---

# Estado

Integration posee Lifecycle propio.

Los estados concretos, sus significados y transiciones se definen
exclusivamente en:

```text
DOMAIN-013A-Lifecycle.md

DOMAIN-013B-State-Machine.md
```

Este documento no debe utilizarse para inferir estados adicionales.

---

# Regla de Estado

Toda modificación debe:

- partir de un estado válido;
- respetar la State Machine;
- preservar Invariants;
- dejar el Aggregate en un estado válido;
- mantener Version coherente;
- producir Domain Events cuando corresponda.

---

# Estados Técnicos

No deben convertirse automáticamente en estados del Aggregate
conceptos como:

```text
Connected

Disconnected

Retrying

Queued

Processing

DeadLettered

Timeout

BrokerUnavailable
```

salvo que alguno sea definido posteriormente como estado real del
dominio mediante su especificación formal.

---

# Lifecycle versus Conectividad Técnica

Debe mantenerse:

```text
Integration Lifecycle

≠

Network Connection State
```

Una conexión técnica activa o inactiva no determina por sí sola el
estado del Aggregate.

---

# Invariants

Integration debe proteger como mínimo:

- IntegrationId existe;
- IntegrationId permanece inmutable;
- el Aggregate solamente modifica su propio estado;
- referencias externas no transfieren ownership;
- sistemas externos no se embeben como Aggregates internos;
- contratos externos no sustituyen el Domain Model;
- credenciales no forman parte del estado;
- una operación inválida no modifica Version;
- una operación inválida no produce un Domain Event de éxito;
- toda transición debe respetar la State Machine;
- toda modificación válida debe preservar el Consistency Boundary.

La especificación formal pertenece a:

```text
DOMAIN-013E-Invariants.md
```

---

# Identificadores Externos

Cuando una integración requiera preservar una referencia externa, esa
referencia no reemplaza IntegrationId.

Debe mantenerse:

```text
External Identifier

≠

IntegrationId
```

---

# Referencias

Las relaciones con otros dominios deben mantenerse mediante:

- identificadores;
- Domain Events;
- Integration Events;
- contratos explícitos.

No mediante referencias mutables directas a otros Aggregate Roots.

---

# Organization e Integration

Organization puede participar en procesos que requieran
interoperabilidad.

Integration no administra:

- OrganizationStatus;
- estructura de Organization;
- miembros de Organization;
- Lifecycle de Organization;
- Version de Organization.

---

# Citizen e Integration

Integration no administra Citizen.

Una identidad de Citizen puede formar parte de un contrato cuando sea
necesario y permitido.

Esto no incorpora Citizen dentro del Aggregate.

---

# Membership e Integration

Integration no modifica:

- Membership;
- MembershipStatus;
- Membership.Version.

Cualquier intercambio de información ocurre mediante contratos
explícitos.

---

# Role e Integration

Integration no administra:

- definición de Roles;
- asignación de Roles;
- revocación de Roles;
- jerarquía de Roles.

---

# Territory e Integration

Información territorial puede interoperar con sistemas externos
mediante contratos definidos.

Integration no modifica Territory directamente.

---

# Assembly e Integration

Assembly puede producir hechos relevantes para interoperabilidad.

Conceptualmente:

```text
Assembly Domain Event
    │
    ▼
Integration Boundary
    │
    ▼
External Contract
```

Integration no modifica Assembly.

---

# Proposal e Integration

Proposal puede participar en contratos de interoperabilidad.

Integration no modifica su:

- estado;
- contenido;
- Lifecycle;
- Version.

---

# Participation e Integration

Integration puede comunicar hechos relacionados con Participation
cuando exista un contrato explícito.

Debe mantenerse:

```text
Participation Transaction

≠

Integration Transaction
```

---

# Voting e Integration

Integration no:

- registra votos;
- modifica votos;
- abre Voting;
- cierra Voting;
- calcula resultados;
- modifica VotingStatus.

---

# Document e Integration

Integration puede permitir interoperabilidad de hechos relacionados
con Document.

No administra:

- Document content;
- DocumentStatus;
- Document.Version;
- Document Lifecycle.

---

# Notification e Integration

Integration no envía Notification como comportamiento del Aggregate.

Notification mantiene su propio:

- Lifecycle;
- State Machine;
- Version;
- delivery behavior.

---

# Audit e Integration

Audit puede preservar trazabilidad de hechos relacionados con
Integration cuando exista un hecho auditable reconocido.

Debe mantenerse:

```text
Audit

≠

Integration
```

Integration no administra Audit.

Audit no administra Integration.

---

# Integration y Audit

Hechos propios de Integration pueden eventualmente ser consumidos por
Audit mediante los contratos correspondientes.

Esto no incorpora Audit dentro del Consistency Boundary.

---

# Consistency Boundary

Integration constituye su propio límite de consistencia.

Conceptualmente:

```text
Integration
    │
    ├── Internal Concepts formally defined
    │
    └── Value Objects formally defined
```

No incluye:

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

Notification

Audit

External System

FIWARE

Municipal Platform

Broker

Database
```

---

# Consistencia Interna

Las modificaciones internas de Integration deben mantener
consistencia inmediata dentro de su propio Boundary.

Toda operación debe finalizar con el Aggregate en un estado válido.

---

# Consistencia Externa

La consistencia entre Integration y otros Aggregates o sistemas es
eventual.

Debe mantenerse:

```text
Integration Transaction

≠

External System Transaction
```

y:

```text
Integration Transaction

≠

Source Aggregate Transaction
```

---

# No Distributed Aggregate

Integration no debe utilizarse para crear un Aggregate distribuido
que abarque:

```text
AURA

+

External System
```

---

# No Two-Phase Commit de Dominio

Este Aggregate no establece como requisito del dominio una
transacción distribuida o Two-Phase Commit entre AURA y sistemas
externos.

Cualquier coordinación técnica permanece fuera del Aggregate.

---

# Fallo Externo

Un fallo técnico de:

- red;
- protocolo;
- broker;
- proveedor;
- endpoint;
- sistema externo;

no debe reinterpretarse automáticamente como un nuevo estado de
Integration.

La State Machine oficial determina los estados permitidos.

---

# Retry Técnico

Un retry técnico no constituye automáticamente:

```text
Integration Domain Command
```

ni:

```text
Integration Domain Event
```

salvo definición formal posterior.

---

# Idempotencia

El dominio debe permanecer compatible con procesamiento seguro de
mensajes repetidos.

Sin embargo, la estrategia técnica concreta de:

```text
idempotency

deduplication

exactly-once processing
```

no se define en este documento.

---

# Correlation

CorrelationId puede utilizarse cuando un contrato lo defina para
preservar trazabilidad entre procesos.

Debe mantenerse:

```text
Shared CorrelationId

≠

Shared Consistency Boundary
```

---

# Causation

CausationId puede preservar la relación causal entre hechos cuando
corresponda.

Debe mantenerse:

```text
CausationId

≠

Mutation Authority
```

---

# Commands

Integration responde a Commands que expresan intenciones propias del
dominio.

La lista oficial, precondiciones y efectos se encuentran
exclusivamente en:

```text
DOMAIN-013C-Commands.md
```

Este documento no debe utilizarse para inferir Commands adicionales.

---

# Regla de Commands

Todo Command de Integration debe:

- expresar intención;
- operar sobre Integration;
- respetar Permissions;
- respetar State Machine;
- preservar Invariants;
- preservar Consistency Boundary;
- modificar Version solamente cuando la operación sea válida;
- producir Domain Events cuando corresponda.

---

# No Commands Técnicos Implícitos

Este documento no define automáticamente Commands como:

```text
SendHttpRequest

PublishKafkaMessage

OpenSocket

RetryHttpCall

ConnectBroker

RefreshToken

SerializePayload

ExecuteWebhook
```

porque representan acciones técnicas y no intenciones del dominio
Integration por sí mismas.

---

# Operaciones Públicas

La Aggregate Root expone únicamente comportamiento formalmente
definido por Commands y reglas de dominio.

No se exponen setters públicos para modificar directamente:

```text
IntegrationId

State

Version

CreatedAt

UpdatedAt
```

---

# Eventos del Dominio

Integration produce Domain Events solamente cuando ocurre un hecho
propio del Aggregate.

La lista oficial se define en:

```text
DOMAIN-013D-Domain-Events.md
```

Un evento técnico de transporte no constituye automáticamente un
Domain Event.

---

# Regla de Domain Events

Debe mantenerse:

```text
Domain Event

=

Confirmed Domain Fact
```

y no:

```text
Domain Event

=

Infrastructure Activity
```

---

# Eventos Técnicos

Hechos como:

```text
HttpRequestSent

BrokerConnected

MessageSerialized

SocketOpened

DatabaseWriteCompleted

TokenRefreshed
```

no son Domain Events de Integration por definición de este documento.

---

# Lifecycle

Integration posee un Lifecycle formal independiente de:

- conectividad;
- estado del broker;
- disponibilidad de endpoint;
- cola técnica;
- estado de transporte.

La especificación exacta pertenece a:

```text
DOMAIN-013A-Lifecycle.md
```

---

# State Machine

Toda transición válida debe estar explícitamente definida en:

```text
DOMAIN-013B-State-Machine.md
```

No se permiten cambios directos de estado.

---

# Versionado

Integration utiliza Version para representar su evolución lógica.

Una modificación válida debe mantener coherencia con:

```text
DOMAIN-013I-Versioning.md
```

Debe mantenerse:

```text
Integration.Version

≠

External System Version
```

y:

```text
Integration.Version

≠

Integration Contract Version
```

---

# Fuente de Verdad

Integration es fuente de verdad únicamente para su propio estado.

Debe mantenerse:

```text
Integration

=

Source of Truth for Integration
```

pero:

```text
Integration

≠

Source of Truth for External System
```

y:

```text
Integration

≠

Source of Truth for Other Aggregates
```

---

# Repository

Integration dispone de un Repository Contract propio.

Conceptualmente:

```text
IntegrationRepository
```

El contrato exacto se define en:

```text
DOMAIN-013G-Repository-Contract.md
```

Este documento no introduce operaciones adicionales del Repository
fuera de su contrato formal.

---

# Repository Responsibility

El Repository es responsable conceptualmente de persistir y recuperar
Integration como una unidad.

No es responsable de:

- ejecutar Commands;
- decidir Invariants;
- decidir Permissions;
- transformar contratos externos;
- enviar mensajes;
- administrar brokers;
- autenticar sistemas externos.

---

# Persistencia

Integration debe persistirse como una unidad de consistencia.

La persistencia física pertenece a Infrastructure.

El Aggregate no depende directamente de:

```text
SQL

PostgreSQL

MongoDB

EventStoreDB

Redis

Filesystem

Cloud Storage
```

---

# Optimistic Concurrency

Integration debe permanecer compatible con Optimistic Concurrency
conforme al patrón consolidado de AURA.

La definición exacta pertenece a:

```text
DOMAIN-013I-Versioning.md
```

---

# Read Model

Las necesidades de consulta de Integration deben resolverse mediante
Read Models.

Debe mantenerse:

```text
Integration Aggregate

≠

Integration Query Engine
```

---

# Consultas

Búsqueda, filtrado, ordenamiento, paginación, reporting y analytics
pertenecen al Read Side.

La especificación formal se define en:

```text
DOMAIN-013L-Read-Model.md
```

---

# Integration Events

Los hechos que deban cruzar límites de contexto pueden representarse
mediante Integration Events conforme a contratos explícitos.

Debe mantenerse:

```text
Integration Domain Event

≠

Mandatory Integration Event
```

La especificación pertenece a:

```text
DOMAIN-013K-Integration-Events.md
```

---

# Integración Entrante

Una entrada desde un sistema externo no posee autoridad directa sobre
Integration ni sobre otros Aggregates.

Conceptualmente:

```text
External Input
    │
    ▼
Integration Boundary
    │
    ▼
Validated AURA Intent / Fact
```

según el contrato correspondiente.

---

# Integración Saliente

Un hecho de AURA puede cruzar una frontera externa solamente mediante
un contrato explícito.

Conceptualmente:

```text
AURA Domain Fact
    │
    ▼
Integration Boundary
    │
    ▼
External Contract
```

---

# Bidireccionalidad

La existencia de intercambio en más de una dirección no fusiona los
Domain Models involucrados.

Debe mantenerse:

```text
Bidirectional Communication

≠

Bidirectional Ownership
```

---

# FIWARE

Integration permite que AURA pueda interoperar con FIWARE cuando
exista un contrato definido.

Sin embargo:

```text
FIWARE

∉

Integration Aggregate
```

---

# NGSI-LD

NGSI-LD constituye una tecnología o modelo de interoperabilidad
externo respecto del Aggregate.

Debe mantenerse:

```text
AURA Domain Model

≠

NGSI-LD Data Model
```

Las traducciones necesarias pertenecen a la frontera de integración.

---

# Context Broker

Un Context Broker no forma parte del Aggregate.

Integration no administra directamente:

```text
Orion

Context Broker

broker subscriptions

broker connections
```

como estado de dominio por definición de este documento.

---

# FIWARE Entity

Una entidad FIWARE no se convierte automáticamente en una Entity
interna del Aggregate.

Debe mantenerse:

```text
FIWARE Entity

≠

Integration Internal Entity
```

---

# Sistemas Municipales

Integration permite representar interoperabilidad con sistemas
municipales mediante contratos explícitos.

Los modelos municipales permanecen fuera de AURA.

Debe mantenerse:

```text
Municipal Model

≠

AURA Domain Model
```

---

# Sistemas Institucionales

La misma regla se aplica a plataformas institucionales externas.

Integration no absorbe sus:

- estados;
- tablas;
- procesos internos;
- usuarios;
- reglas de negocio.

---

# Smart City

Integration puede permitir interoperabilidad con ecosistemas Smart
City.

El Aggregate no conoce directamente la implementación tecnológica
específica utilizada por dichos ecosistemas.

---

# Transport

Integration no depende conceptualmente de:

```text
HTTP

REST

GraphQL

WebSocket

MQTT

AMQP

TCP

UDP
```

La selección de transporte pertenece a Architecture e
Infrastructure.

---

# Messaging

Integration no depende conceptualmente de:

```text
Kafka

RabbitMQ

NATS

Redis Streams

MQTT Broker
```

ni de una tecnología equivalente.

---

# Serialización

La representación física de contratos no pertenece al Aggregate.

Puede existir una serialización técnica, pero:

```text
JSON

Avro

Protobuf

MessagePack
```

no forman parte de la semántica del dominio por sí mismos.

---

# API

Una API es una forma técnica de exposición o consumo.

Debe mantenerse:

```text
API

≠

Integration Aggregate
```

---

# Endpoint

Un endpoint no representa la identidad del Aggregate.

Debe mantenerse:

```text
Endpoint

≠

IntegrationId
```

---

# SDK

Un SDK puede implementar acceso técnico a una integración.

No constituye una Entity ni Value Object del Aggregate por
definición.

---

# Authentication

Integration no administra Authentication.

Authentication pertenece al contexto de seguridad correspondiente.

---

# Authorization

Los Commands de Integration deben estar sujetos a Permissions
aplicables.

Authorization no puede evitar:

- State Machine;
- Invariants;
- Versioning;
- Consistency Boundary.

---

# Security

Integration no almacena:

- passwords;
- access tokens;
- refresh tokens;
- API keys;
- private keys;
- client secrets;
- secretos;
- sesiones;
- credenciales.

La especificación formal se encuentra en:

```text
DOMAIN-013O-Security-Model.md
```

---

# Permissions

Permissions determinan quién puede intentar ejecutar capacidades
definidas para Integration.

Debe mantenerse:

```text
Permission

≠

Domain Rule
```

y:

```text
Authorized

≠

Automatically Valid
```

La definición formal se encuentra en:

```text
DOMAIN-013F-Permissions.md
```

---

# Data Minimization

Integration debe preservar únicamente información necesaria para su
propósito.

Debe mantenerse:

```text
External Payload

≠

Automatic Integration State
```

y:

```text
Source Aggregate Payload

≠

Automatic Integration State
```

---

# External Payload

Integration no debe almacenar automáticamente un Payload externo
completo.

Solamente debe conservar información de dominio formalmente definida
como necesaria.

---

# Sensitive Data

La presencia de datos sensibles en un sistema externo no obliga a
incorporarlos a Integration.

---

# Tracing

Integration puede participar en trazabilidad mediante:

```text
CorrelationId

CausationId
```

cuando los contratos correspondientes los proporcionen.

Esto no los convierte automáticamente en atributos obligatorios del
Aggregate.

---

# Observability

Integration no es un sistema de Observability.

Debe mantenerse:

```text
Integration

≠

Logging

≠

Metrics

≠

Tracing Infrastructure
```

---

# Logs

Logs técnicos de:

- requests;
- responses;
- brokers;
- conexiones;
- errores;
- retries;

permanecen fuera del Aggregate.

---

# Metrics

Métricas como:

```text
latency

throughput

error rate

queue depth

connection count
```

no son estado del Aggregate por definición.

---

# Technical Health

La salud técnica de una integración no debe confundirse con su
Lifecycle de dominio.

Debe mantenerse:

```text
Technical Health

≠

Integration Lifecycle State
```

salvo definición formal explícita futura.

---

# Errores Técnicos

Errores técnicos de transporte o proveedor no deben introducir
automáticamente Domain Events.

Debe mantenerse:

```text
Technical Error

≠

Domain Fact
```

---

# Performance

Integration debe mantener un Aggregate pequeño.

No debe cargar:

- otros Aggregates completos;
- historial global de integraciones;
- Payloads externos completos innecesarios;
- Read Models;
- información técnica de observabilidad.

Las reglas específicas se definen en:

```text
DOMAIN-013N-Performance-Rules.md
```

---

# Escalabilidad

El crecimiento de integraciones no debe provocar la creación de una
única Aggregate Root que represente todas las integraciones de AURA.

Debe mantenerse:

```text
Many Integrations

≠

One Global Integration Aggregate
```

---

# No Global Integration Aggregate

Una necesidad de:

- búsqueda;
- dashboard;
- monitoreo;
- reporting;
- analytics;

debe resolverse mediante Read Models o capacidades externas
apropiadas.

---

# Auditabilidad

Los cambios relevantes propios de Integration pueden generar hechos
consumibles por Audit cuando exista el contrato correspondiente.

Audit permanece fuera del Aggregate.

---

# Trazabilidad

Integration debe permitir reconstruir conceptualmente su propia
evolución mediante:

- identidad;
- Version;
- Domain Events;
- timestamps;
- contratos definidos.

La trazabilidad técnica de red permanece fuera.

---

# CQRS

Integration es compatible con CQRS.

Conceptualmente:

```text
Command
   │
   ▼
Integration Aggregate
   │
   ├── State Machine
   ├── Invariants
   ├── Version
   └── Domain Events
```

mientras:

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

Integration es compatible con Event Sourcing.

Esto no significa que Event Sourcing sea obligatorio.

Debe mantenerse:

```text
Event Sourcing Compatible

≠

Event Sourcing Required
```

La estrategia de persistencia pertenece a una decisión arquitectónica
separada.

---

# Domain Event Stream

Si Event Sourcing fuese utilizado, solamente los Domain Events
propios de Integration formarían parte de su evolución.

Debe mantenerse:

```text
External Event Stream

≠

Integration Domain Event Stream
```

---

# Integration Event Stream

Un flujo de Integration Events tampoco reemplaza automáticamente el
historial autoritativo del Aggregate.

Debe mantenerse:

```text
Integration Event Stream

≠

Integration Aggregate
```

---

# Rehidratación

La rehidratación debe preservar:

- IntegrationId;
- estado válido;
- Version;
- información formal del Aggregate;
- Invariants.

Rehidratar no constituye una nueva operación de dominio.

---

# Replay

Replay, cuando exista, no debe:

- ejecutar Commands nuevamente;
- producir nuevos hechos por el solo replay;
- incrementar Version artificialmente;
- publicar nuevamente eventos como nuevos hechos de dominio.

---

# Repository versus Transport

Debe mantenerse:

```text
IntegrationRepository

≠

Message Transport
```

El Repository persiste el Aggregate.

El transporte mueve representaciones técnicas conforme a capas
externas.

---

# Aggregate versus Adapter

Debe mantenerse:

```text
Integration

≠

FIWARE Adapter

≠

Municipal Adapter

≠

HTTP Client

≠

Broker Client
```

---

# Aggregate versus Orchestrator Técnico

Integration no debe convertirse en un objeto técnico que coordine
conexiones, sockets, procesos o workers.

Su responsabilidad es de dominio.

---

# Interoperabilidad

Integration constituye el Aggregate orientado a preservar reglas
propias de interoperabilidad dentro de AURA.

Debe mantener separados:

```text
Domain Semantics

Integration Contracts

Infrastructure Implementation
```

---

# Boundary de Interoperabilidad

La frontera de interoperabilidad debe impedir que detalles de un
sistema externo contaminen directamente el Domain Model de AURA.

---

# Contratos Públicos

Los contratos destinados a consumidores externos deben evolucionar
de forma independiente del estado interno del Aggregate.

Debe mantenerse:

```text
Integration Contract Version

≠

Integration.Version
```

---

# Versiones Externas

La versión de:

- API;
- schema;
- protocolo;
- FIWARE Entity;
- contrato municipal;

no representa automáticamente:

```text
Integration.Version
```

---

# Consumo de Integration Events de Otros Aggregates

Integration puede reaccionar a Integration Events publicados por
otros contextos cuando exista un contrato reconocido.

Su recepción:

```text
External Integration Event
```

no permite modificar Integration directamente sin comportamiento
válido.

---

# Consumo de Domain Events

Un Domain Event interno puede originar una coordinación posterior de
integración.

Esto no transfiere ownership del evento a Integration.

---

# Relaciones Estratégicas

Integration constituye un punto de interoperabilidad entre AURA y:

- Bounded Contexts internos;
- ecosistemas municipales;
- plataformas institucionales;
- Smart City;
- FIWARE;
- sistemas externos autorizados.

Su función estratégica es permitir intercambio sin acoplar el Domain
Model con tecnologías o modelos externos.

---

# Reglas de Diseño del Aggregate

Integration debe respetar:

- una única Aggregate Root;
- identidad propia e inmutable;
- alto nivel de cohesión;
- bajo acoplamiento;
- Invariants protegidas;
- comportamiento explícito;
- ausencia de setters públicos;
- referencias externas mediante contratos;
- ausencia de Aggregates externos embebidos;
- consistencia interna inmediata;
- consistencia externa eventual;
- Domain Events para hechos propios;
- Integration Events para contratos externos cuando corresponda;
- Read Models para consultas;
- Repository Contract para persistencia;
- Versioning para evolución lógica;
- independencia tecnológica.

---

# Restricciones

No está permitido:

- modificar IntegrationId;
- modificar directamente el estado;
- modificar directamente Version;
- utilizar setters públicos;
- embebir otros Aggregates;
- embebir sistemas externos completos;
- convertir modelos externos en Domain Model automáticamente;
- ejecutar SQL desde el Aggregate;
- acceder directamente a una base de datos;
- depender de HTTP como regla de dominio;
- depender de REST como regla de dominio;
- depender de GraphQL como regla de dominio;
- depender de MQTT como regla de dominio;
- depender de un broker concreto;
- depender de FIWARE como implementación interna;
- depender de NGSI-LD como modelo interno obligatorio;
- almacenar passwords;
- almacenar tokens;
- almacenar API keys;
- almacenar private keys;
- almacenar secrets;
- almacenar client secrets;
- utilizar un estado de red como estado de dominio sin definición
  explícita;
- utilizar un estado de queue como estado de dominio sin definición
  explícita;
- utilizar retry técnico como Command de dominio sin definición
  explícita;
- convertir errores técnicos automáticamente en Domain Events;
- publicar todos los Domain Events como Integration Events por
  defecto;
- modificar directamente otro Aggregate;
- permitir que un sistema externo modifique directamente el
  Aggregate;
- ampliar el Consistency Boundary para incorporar un sistema externo;
- imponer una transacción distribuida como regla del Aggregate;
- imponer Event Sourcing;
- utilizar Read Models como fuente de verdad de escritura;
- utilizar logs o metrics como estado del Aggregate;
- crear un Aggregate global de todas las integraciones.

---

# Compatibilidad Arquitectónica

Integration está diseñado para cumplir:

- Domain-Driven Design;
- Aggregate Pattern;
- Bounded Context;
- Clean Architecture;
- Hexagonal Architecture;
- SOLID;
- Event-Driven Architecture;
- CQRS;
- Event Sourcing Compatible;
- Optimistic Concurrency Control;
- Anti-Corruption Boundary;
- consistencia eventual;
- High Cohesion;
- Low Coupling.

Estas compatibilidades no imponen:

- protocolo;
- broker;
- framework;
- base de datos;
- proveedor;
- plataforma externa.

---

# Dependencias

Integration depende conceptualmente de:

- Shared Kernel;
- Domain Events;
- Integration Contracts;
- Repository Contracts;
- identificadores;
- contratos definidos por AURA.

Integration no depende directamente de:

```text
Infrastructure

Frameworks

Bases de datos

ORM

HTTP

REST

GraphQL

MQTT

AMQP

Kafka

RabbitMQ

NATS

OAuth

JWT

React

Next.js

FastAPI

Django

FIWARE SDK

NGSI-LD SDK

MongoDB

PostgreSQL
```

---

# Escenarios de Uso Conceptuales

Integration debe poder representar conceptualmente relaciones de
interoperabilidad sin absorber la implementación técnica.

## Integración Municipal

AURA puede intercambiar información con una plataforma municipal
mediante un contrato explícito.

El sistema municipal permanece fuera del Aggregate.

## Integración Smart City

Hechos relevantes de AURA pueden compartirse con un ecosistema Smart
City mediante contratos explícitos.

## Integración FIWARE

AURA puede proyectar o recibir información relacionada con FIWARE
mediante la frontera de integración correspondiente.

FIWARE permanece fuera del Domain Model de Integration.

## Integración entre Bounded Contexts

Dos Bounded Contexts pueden colaborar mediante hechos y contratos sin
compartir Aggregate ni transacción.

## Sistema Externo con Semántica Diferente

Cuando un sistema externo utiliza conceptos distintos de AURA, la
traducción debe preservar el lenguaje ubicuo interno.

---

# Seguridad

Integration debe mantener separación entre:

```text
Authentication

Authorization

Domain Validation

External Credentials
```

El Aggregate solamente protege las reglas propias de Integration.

La definición formal se desarrolla en:

```text
DOMAIN-013O-Security-Model.md
```

---

# Rendimiento

Integration debe mantenerse pequeño y enfocado.

No debe incorporar:

- grandes Payloads externos;
- histórico global;
- conexiones;
- buffers;
- colas;
- logs;
- métricas.

Las necesidades de consulta y análisis pertenecen al Read Side.

La definición formal se desarrolla en:

```text
DOMAIN-013N-Performance-Rules.md
```

---

# Extensibilidad

Integration debe permitir evolución controlada.

Pueden evolucionar, cuando sean definidos formalmente:

```text
Lifecycle

Commands

Domain Events

Integration Contracts

Integration Events

Read Models

Security Rules

Source Types

Target Types
```

sin modificar innecesariamente el núcleo del Aggregate.

La especificación se encuentra en:

```text
DOMAIN-013P-Extension-Points.md
```

---

# Regla de No Inferencia

Este documento define el límite conceptual principal de Integration.

No debe utilizarse para inferir automáticamente:

- estados;
- transiciones;
- Commands;
- Domain Events;
- Internal Entities;
- Value Objects;
- protocolos;
- mecanismos de retry;
- cardinalidades;
- políticas de eliminación;
- políticas de retención;
- mecanismos de idempotencia;
- tecnologías de mensajería;
- tecnologías de persistencia.

Cada una de estas dimensiones debe definirse formalmente en el
documento correspondiente antes de considerarse parte del dominio.

---

# Documentación Asociada

Integration se complementa con:

```text
DOMAIN-013A-Lifecycle.md

DOMAIN-013B-State-Machine.md

DOMAIN-013C-Commands.md

DOMAIN-013D-Domain-Events.md

DOMAIN-013E-Invariants.md

DOMAIN-013F-Permissions.md

DOMAIN-013G-Repository-Contract.md

DOMAIN-013H-Examples.md

DOMAIN-013I-Versioning.md

DOMAIN-013J-Consistency-Boundary.md

DOMAIN-013K-Integration-Events.md

DOMAIN-013L-Read-Model.md

DOMAIN-013M-Test-Scenarios.md

DOMAIN-013N-Performance-Rules.md

DOMAIN-013O-Security-Model.md

DOMAIN-013P-Extension-Points.md
```

Cada documento desarrolla una dimensión específica sin autorizar
inferencias sobre dimensiones todavía no definidas.

---

# Objetivos de Diseño

Integration busca garantizar:

- identidad formal de una Integration;
- separación entre dominio e Infrastructure;
- contratos explícitos;
- independencia entre Bounded Contexts;
- independencia respecto de sistemas externos;
- protección del lenguaje ubicuo de AURA;
- consistencia interna;
- consistencia externa eventual;
- trazabilidad;
- Versioning;
- interoperabilidad;
- Security;
- minimización;
- extensibilidad controlada.

---

# Definición de Éxito

El Aggregate **Integration** representa de forma oficial una unidad de
interoperabilidad reconocida por AURA.

El modelo garantiza que:

```text
Integration

≠

Infrastructure
```

y:

```text
Integration

≠

External System
```

y:

```text
Domain Event

≠

Integration Event
```

Integration preserva:

- identidad propia mediante IntegrationId;
- ownership exclusivamente sobre su propio estado;
- Consistency Boundary independiente;
- Version propia;
- timestamps propios;
- contratos explícitos;
- independencia respecto de protocolos;
- independencia respecto de brokers;
- independencia respecto de bases de datos;
- independencia respecto de FIWARE;
- independencia respecto de sistemas municipales;
- separación entre Domain Model y modelos externos;
- separación entre Authentication, Authorization y Domain
  Validation;
- ausencia de credenciales dentro del Aggregate;
- ausencia de Aggregates externos embebidos;
- consistencia eventual con otros contextos;
- capacidad de producir Domain Events propios;
- capacidad de participar en Integration Events cuando exista un
  contrato explícito;
- Read Models separados del Write Model;
- compatibilidad con CQRS;
- compatibilidad con Event Sourcing sin imponerlo;
- trazabilidad propia;
- evolución controlada.

Integration permite que:

```text
AURA Domain
    │
    ▼
Integration Boundary
    │
    ▼
Explicit Contract
    │
    ▼
External Context
```

ocurra sin que el contexto externo se convierta en parte del Domain
Model de AURA.

De esta forma, `DOMAIN-013-Aggregate.md` establece el límite
conceptual oficial del Aggregate **Integration** conforme al patrón
consolidado de AURA Core.