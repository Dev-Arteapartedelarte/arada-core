# DOMAIN-013O — Integration Security Model

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

- DOMAIN-013-Aggregate.md
- DOMAIN-013A-Lifecycle.md
- DOMAIN-013B-State-Machine.md
- DOMAIN-013C-Commands.md
- DOMAIN-013D-Domain-Events.md
- DOMAIN-013E-Invariants.md
- DOMAIN-013F-Permissions.md
- DOMAIN-013G-Repository-Contract.md
- DOMAIN-013H-Examples.md
- DOMAIN-013I-Versioning.md
- DOMAIN-013J-Consistency-Boundary.md
- DOMAIN-013K-Integration-Events.md
- DOMAIN-013L-Read-Model.md
- DOMAIN-013M-Test-Scenarios.md
- DOMAIN-013N-Performance-Rules.md
- DOMAIN-013P-Extension-Points.md

---

# Objetivo

Este documento define formalmente el **Security Model** conceptual
asociado al Aggregate **Integration**.

El propósito del modelo es preservar:

- identidad del Aggregate;
- autorización de Commands protegidos;
- separación entre Authentication y Domain Model;
- protección de Permissions;
- protección de Invariants;
- protección de Versioning;
- protección del Consistency Boundary;
- confidencialidad de información;
- Data Minimization;
- separación de credenciales y secretos;
- integridad de Domain Events;
- seguridad de Integration Events;
- separación entre sistemas externos y el dominio AURA.

Este documento define reglas conceptuales.

No selecciona mecanismos técnicos concretos de seguridad.

---

# Principio Fundamental

Debe mantenerse:

```text
Security

protects

Domain Behavior
```

pero:

```text
Security Mechanism

≠

Domain Behavior
```

---

# Security no Sustituye Dominio

Ningún mecanismo de seguridad puede sustituir:

- Lifecycle;
- State Machine;
- Commands;
- Guards;
- Invariants;
- Versioning;
- Consistency Boundary.

---

# Security no Expande Domain Model

La existencia de requisitos de seguridad no autoriza incorporar al
Aggregate:

- usuarios completos;
- perfiles;
- sesiones;
- tokens;
- passwords;
- certificates;
- secret keys;
- identity provider state;
- policy engine state.

---

# Authentication

Authentication permanece fuera del Aggregate Integration.

Debe mantenerse:

```text
Authentication

∉

Integration Aggregate
```

---

# Responsabilidad de Authentication

Authentication determina conceptualmente:

```text
Who is the requester?
```

Integration no determina por sí misma cómo dicha identidad es
autenticada.

---

# Authentication no es Authorization

Debe mantenerse:

```text
Authentication

≠

Authorization
```

---

# Authorization

Authorization determina conceptualmente si un requester autenticado
puede intentar una capacidad protegida.

Debe mantenerse:

```text
Authorization

=

Permission Evaluation
```

en el contexto de las capacidades definidas para Integration.

---

# Authorization no es Domain Validation

Debe mantenerse:

```text
Authorization

≠

Domain Validation
```

Una operación autorizada aún debe cumplir:

- State Machine;
- Guards;
- Invariants;
- Versioning;
- Consistency Boundary.

---

# Authorization no Garantiza Éxito

Debe mantenerse:

```text
Authorized

≠

Successful Domain Operation
```

---

# Permissions Oficiales

Las capacidades protegidas oficiales versión 1.0 son:

```text
Integration.Create

Integration.Activate

Integration.Suspend

Integration.Reactivate

Integration.Archive
```

---

# Permission / Command

La relación oficial es:

```text
Integration.Create
    │
    ▼
CreateIntegration

Integration.Activate
    │
    ▼
ActivateIntegration

Integration.Suspend
    │
    ▼
SuspendIntegration

Integration.Reactivate
    │
    ▼
ReactivateIntegration

Integration.Archive
    │
    ▼
ArchiveIntegration
```

---

# Permission no es Command

Debe mantenerse:

```text
Permission

≠

Command
```

---

# Command no es Authentication

Debe mantenerse:

```text
Command

≠

Authentication Request
```

---

# Command no Transporta Credenciales de Dominio

Los Commands no deben incorporar como estado del dominio:

```text
Password

AccessToken

RefreshToken

ApiKey

PrivateKey

ClientSecret

Secret
```

---

# Permission Evaluation

Una intención protegida debe ser autorizada antes de ejecutarse contra
el comportamiento del Aggregate.

Conceptualmente:

```text
Requester
    │
    ▼
Authentication
    │
    ▼
Authorization
    │
    ▼
Permission
    │
    ▼
Command
    │
    ▼
Integration Aggregate
```

Esta secuencia es conceptual y no define mecanismo técnico.

---

# Domain Validation Posterior

Una vez autorizada la intención:

```text
Command
    │
    ▼
State Machine
    │
    ▼
Guards
    │
    ▼
Invariants
    │
    ▼
Versioning
    │
    ▼
Valid Domain Result
```

---

# Deny by Default

Cuando una capacidad requiera Permission y no exista autorización
válida:

```text
Operation

=

Rejected
```

---

# Least Privilege

Debe aplicarse:

```text
Minimum Required Permission
```

para cada capacidad protegida.

---

# Permission Scope

Una Permission concedida para una capacidad no debe interpretarse como
autoridad universal sobre todas las capacidades de Integration.

---

# Integration.Activate no Implica Integration.Archive

Debe mantenerse:

```text
Integration.Activate

≠

Integration.Archive
```

---

# Integration.Suspend no Implica Integration.Reactivate

Debe mantenerse:

```text
Integration.Suspend

≠

Integration.Reactivate
```

---

# Integration.Create no Implica Administración Completa

Debe mantenerse:

```text
Integration.Create

≠

All Integration Permissions
```

---

# Permission Scope por Aggregate

Una Permission no debe interpretarse automáticamente como aplicable a
todas las Integration.

El alcance concreto pertenece al contexto de Authorization
correspondiente.

---

# No Scope Architecture Decision

Este documento no define cómo se representa técnicamente:

- resource scope;
- tenant scope;
- organization scope;
- instance scope;
- policy scope.

---

# Roles

Role permanece fuera del Aggregate Integration.

Debe mantenerse:

```text
Role

≠

Integration Aggregate State
```

---

# Role no es Permission

Debe mantenerse:

```text
Role

≠

Permission
```

La eventual relación entre Role y Permission pertenece al contexto
correspondiente.

---

# Membership

Membership permanece fuera del Aggregate.

---

# Membership no Concede Permission Automáticamente

Debe mantenerse:

```text
Membership

≠

Automatic Integration Permission
```

---

# Citizen

Citizen permanece fuera del Aggregate Integration.

---

# Citizen no es Security State

Debe mantenerse:

```text
Citizen

≠

Embedded Security State
```

---

# Requester

Requester representa conceptualmente la identidad que intenta una
operación.

El Aggregate no almacena necesariamente al requester como parte de su
estado.

---

# Requester no es ActorId

Debe mantenerse:

```text
Requester

≠

ActorId
```

salvo que un contrato explícito determine que representan la misma
identidad.

---

# ActorId

ActorId puede participar en trazabilidad cuando corresponda.

No representa por sí mismo:

```text
Authentication

Authorization

Permission
```

---

# ActorId no Concede Authority

Debe mantenerse:

```text
ActorId

≠

Mutation Authority
```

---

# CorrelationId

CorrelationId no constituye autorización.

---

# CausationId

CausationId tampoco constituye autorización.

---

# IntegrationId

Conocer IntegrationId no concede Permission.

Debe mantenerse:

```text
IntegrationId Knowledge

≠

Write Authority
```

---

# External Identifier

Conocer un identificador externo tampoco concede autoridad sobre
Integration.

---

# Security y State Machine

Ninguna identidad autorizada puede ejecutar una transición inexistente.

---

# Security y Archived

Aunque exista Permission:

```text
State = Archived

+

Integration.Reactivate

=

Rejected
```

---

# Security no Evita Terminalidad

Ningún privilegio puede convertir:

```text
Archived

→

Active
```

en versión 1.0.

---

# Security y Invariants

Debe mantenerse:

```text
Authorized

+

Invariant Violation

=

Rejected
```

---

# Security y Guards

Debe mantenerse:

```text
Authorized

+

Guard Failure

=

Rejected
```

---

# Security y Versioning

Debe mantenerse:

```text
Authorized

+

ConcurrencyConflict

=

Rejected
```

---

# Permission no Permite setState()

Ninguna Permission autoriza:

```text
setState()
```

---

# Permission no Permite setVersion()

Ninguna Permission autoriza:

```text
setVersion()
```

---

# Permission no Modifica IntegrationId

Ninguna Permission permite modificar:

```text
IntegrationId
```

---

# Permission no Modifica CreatedAt

Ninguna Permission permite modificar:

```text
CreatedAt
```

---

# Permission no Modifica Version Arbitrariamente

Debe mantenerse:

```text
Permission

≠

Version Authority
```

---

# Security Failure

Un Authentication Failure o Authorization Failure no modifica el
Aggregate.

---

# Authentication Failure

Ante Authentication Failure:

```text
State unchanged

Version unchanged

UpdatedAt unchanged

No success Domain Event
```

---

# Authorization Failure

Ante Authorization Failure:

```text
State unchanged

Version unchanged

UpdatedAt unchanged

No success Domain Event
```

---

# Permission Failure no es State

Debe mantenerse:

```text
Permission Denied

≠

Integration State
```

---

# No Security States

No se introducen:

```text
Authorized

Unauthorized

AccessDenied

Locked

Blocked

Compromised
```

como Lifecycle States de Integration.

---

# Security Incident no es State Automático

Un Security Incident no transforma automáticamente Integration a:

```text
Suspended

Archived
```

---

# No Auto-Suspension por Security Incident

Debe mantenerse:

```text
Security Incident

≠

SuspendIntegration
```

---

# No Auto-Archive por Security Incident

Debe mantenerse:

```text
Security Incident

≠

ArchiveIntegration
```

---

# Security Recovery no Reactiva

Debe mantenerse:

```text
Security Recovery

≠

ReactivateIntegration
```

---

# Credentials

Credentials permanecen fuera del Aggregate.

---

# Secrets

Debe mantenerse:

```text
Secrets

∉

Integration Aggregate
```

---

# Password

Password no forma parte del estado de Integration.

---

# AccessToken

AccessToken no forma parte del estado de Integration.

---

# RefreshToken

RefreshToken no forma parte del estado de Integration.

---

# ApiKey

ApiKey no forma parte del estado de Integration.

---

# PrivateKey

PrivateKey no forma parte del estado de Integration.

---

# ClientSecret

ClientSecret no forma parte del estado de Integration.

---

# Certificate

La eventual existencia de un certificate técnico no convierte dicho
certificate en estado del Aggregate.

---

# Credential Rotation

Rotar credenciales externas no modifica automáticamente:

```text
Integration.State

Integration.Version

Integration.UpdatedAt
```

---

# Credential Expiration

La expiración de una credencial técnica no ejecuta automáticamente:

```text
SuspendIntegration
```

---

# Secret Storage

Este documento no define mecanismo de almacenamiento de secretos.

---

# Secret Distribution

Este documento tampoco define mecanismo de distribución de secretos.

---

# No Secret Manager Decision

No se selecciona un Secret Manager concreto.

---

# No Key Management Decision

Este documento no establece una solución concreta de Key Management.

---

# Domain Events y Seguridad

Los Domain Events oficiales:

```text
IntegrationCreated

IntegrationActivated

IntegrationSuspended

IntegrationReactivated

IntegrationArchived
```

deben preservar la semántica del dominio sin exponer información
innecesaria.

---

# Domain Event Data Minimization

Debe mantenerse:

```text
Domain Event Payload

=

Minimum Necessary Domain Fact Information
```

---

# Domain Events no Contienen Secrets

No deben incluir:

```text
Password

AccessToken

RefreshToken

ApiKey

PrivateKey

ClientSecret

Secret
```

---

# EventId

EventId identifica el hecho.

No concede Permission.

---

# AggregateVersion

AggregateVersion preserva evolución lógica.

No concede Authorization.

---

# OccurredAt

OccurredAt representa tiempo del hecho.

No es metadata de autenticación.

---

# ActorId en Domain Events

ActorId puede formar parte de un Domain Event cuando corresponda.

Debe mantenerse:

```text
ActorId

≠

Authentication Credential
```

---

# CorrelationId en Domain Events

CorrelationId puede preservarse cuando corresponda.

No contiene secretos.

---

# CausationId en Domain Events

CausationId puede preservarse cuando corresponda.

No constituye autoridad.

---

# Domain Event Integrity

Un Domain Event confirmado no debe alterarse posteriormente para
representar un hecho diferente.

---

# Event Immutability

Debe mantenerse:

```text
Confirmed Domain Event

=

Immutable Historical Fact
```

en términos conceptuales.

---

# Event Replay

Replay no reevalúa Authentication como si cada evento histórico fuera
una nueva intención.

---

# Replay no es Nueva Authorization

Debe mantenerse:

```text
Replay

≠

New Authorization Decision
```

---

# Rehydration

Rehydration no representa una nueva operación protegida de escritura.

---

# Integration Events y Seguridad

Integration Events solamente existen cuando un contrato explícito lo
requiere.

---

# Integration Event Data Minimization

Debe mantenerse:

```text
Integration Event Payload

=

Minimum Contractually Necessary Information
```

---

# Integration Events no Contienen Secrets

No deben incluir:

```text
Password

AccessToken

RefreshToken

ApiKey

PrivateKey

ClientSecret

Secret
```

---

# Consumer Authorization

Un consumidor puede requerir autorización para recibir información.

El mecanismo concreto queda fuera de este documento.

---

# Consume Event no es Write Authority

Debe mantenerse:

```text
Can Consume Integration Event

≠

Can Modify Integration
```

---

# Incoming Integration Event

Un evento entrante no modifica directamente el Aggregate.

---

# Incoming Event no Bypassea Authorization

Debe mantenerse:

```text
Incoming Integration Event

≠

Authorization Bypass
```

---

# External Message

Un mensaje externo no posee autoridad automática sobre Integration.

---

# External Message no es Permission

Debe mantenerse:

```text
External Message

≠

Permission
```

---

# External Message no es Command Automático

Debe mantenerse:

```text
External Message

≠

Automatic Domain Command
```

---

# External System

Un sistema externo no forma parte del Security State del Aggregate.

---

# External Identity

Una identidad autenticada en un sistema externo no se convierte
automáticamente en una identidad autorizada por AURA.

---

# External Authorization

Debe mantenerse:

```text
External Authorization

≠

AURA Authorization
```

---

# FIWARE Authorization

Una autorización proveniente de FIWARE no concede automáticamente:

```text
Integration.Create

Integration.Activate

Integration.Suspend

Integration.Reactivate

Integration.Archive
```

---

# Municipal Authorization

Una autorización proveniente de un sistema municipal tampoco concede
automáticamente las Permissions internas.

---

# Authorization Mapping

Cualquier equivalencia entre autorizaciones externas y capacidades de
AURA requiere contrato explícito.

Este documento no define el mecanismo técnico de mapping.

---

# No Trust by Location

El origen de red de una solicitud no constituye por sí mismo
Authorization.

---

# No Trust by Infrastructure

El hecho de que una solicitud provenga de Infrastructure interna no
concede por sí mismo Permission.

---

# No Trust by Broker

El hecho de que un mensaje provenga de un broker confiable no
constituye automáticamente Domain Authorization.

---

# No Trust by Database Access

Acceder técnicamente a la base de datos no concede Permissions de
dominio.

---

# No Trust by Service Location

La ubicación de un servicio no sustituye Authentication ni
Authorization.

---

# Security y Repository

IntegrationRepository no es responsable de resolver Authentication.

---

# Repository no Decide Authorization

Debe mantenerse:

```text
IntegrationRepository

≠

Authorization Authority
```

---

# Repository Access no Concede Permission

Poder invocar:

```text
save()
```

no significa poseer una Permission de dominio.

---

# Database Privilege no es Domain Permission

Debe mantenerse:

```text
Database Privilege

≠

Integration Permission
```

---

# Direct Database Mutation

Modificar State directamente en persistencia evita el comportamiento
del Aggregate y no constituye una operación válida del dominio.

---

# Security y Read Model

Read Models pueden requerir políticas de acceso.

---

# Read Permission

Read Permission permanece separada de las Permissions de escritura.

---

# Read Permission no es Write Permission

Debe mantenerse:

```text
Read Permission

≠

Write Permission
```

---

# Read Model no Decide Authorization

Debe mantenerse:

```text
Read Model

≠

Authorization Authority
```

---

# Query no Concede Permission

Obtener información mediante Query no concede autoridad para ejecutar
Commands.

---

# Read Data no Incluye Secrets

El Read Model de dominio no debe exponer credenciales ni secretos.

---

# Read Model Data Minimization

Las vistas deben mostrar únicamente información necesaria para el
propósito de lectura correspondiente.

---


# Joined Read Model

Una vista que combine información de múltiples contextos debe mantener
las reglas de acceso correspondientes sin fusionar ownership.

---

# Security y Consistency Boundary

Security no modifica el límite del Aggregate.

Debe mantenerse:

```text
Security Requirement

≠

Consistency Boundary Expansion
```

---

# Authentication Outside Boundary

Authentication permanece fuera del Boundary.

---

# Authorization Outside Aggregate State

Authorization permanece fuera del estado interno.

---

# Credentials Outside Boundary

Credentials permanecen fuera del Boundary.

---

# Role Outside Boundary

Role mantiene ownership independiente.

---


# Membership Outside Boundary

Membership mantiene ownership independiente.

---

# Identity Provider Outside Boundary

Un eventual Identity Provider permanece fuera del Aggregate.

---

# Policy Engine Outside Boundary

Un eventual mecanismo de políticas permanece fuera del Aggregate.

---

# Security Metadata

Metadata técnica de seguridad no debe incorporarse automáticamente al
Aggregate.

---

# Data Minimization

Integration debe conservar solamente la información necesaria para sus
reglas de dominio.

---

# Personal Data

Información personal no se incorpora al Aggregate por defecto.

Su presencia requiere una necesidad explícita del dominio.

---

# Sensitive Data

Información sensible no se incorpora por conveniencia técnica.

---


# Full User Profile

Debe mantenerse:

```text
Full User Profile

≠

Integration Aggregate State
```

---

# Full External Identity

Debe mantenerse:

```text
Full External Identity

≠

Integration Aggregate State
```

---


# External Payload

El Payload externo completo no forma parte automáticamente del
Aggregate.

---

# Security Context no es Aggregate State

Información utilizada temporalmente para decidir Authorization no debe
convertirse automáticamente en estado persistido de Integration.

---

# Audit

Audit mantiene un Aggregate independiente.

---

# Security Audit

Un hecho relacionado con seguridad puede eventualmente ser observado
por Audit cuando exista el contrato correspondiente.

Esto no incorpora Audit dentro de Integration.

---

# Audit no Decide Authorization

Debe mantenerse:

```text
Audit

≠

Authorization Authority
```

---


# Audit Failure

Un fallo posterior de Audit no revierte una modificación ya confirmada
de Integration.

---

# Notification

Notification permanece independiente.

---

# Security Notification

Una eventual Notification relacionada con seguridad no forma parte de
la transacción de Integration.

---


# Notification Failure

Notification Failure no modifica Integration.

---

# Security y Versioning

Solamente una modificación válida del Aggregate incrementa Version.

---

# Authentication Success no Incrementa Version

Debe mantenerse:

```text
Authentication Success

≠

Integration.Version Increment
```

---

# Authentication Failure no Incrementa Version

Debe mantenerse:

```text
Authentication Failure

≠

Integration.Version Increment
```

---

# Authorization Success no Incrementa Version

Autorizar una intención no modifica por sí mismo Integration.

---

# Authorization Failure no Incrementa Version

Rechazar una intención antes de una modificación válida tampoco
incrementa Version.

---

# Permission Assignment no Incrementa Version

Asignar una Permission externamente no modifica Integration.Version.

---

# Permission Revocation no Incrementa Version

Revocar una Permission externamente tampoco modifica Version.

---

# Security Policy Change no Incrementa Version

Cambiar una política de seguridad no modifica Integration.Version por
sí mismo.

---

# Credential Rotation no Incrementa Version

Credential Rotation no incrementa Version por sí misma.

---

# Token Refresh no Incrementa Version

Un refresh técnico de token no modifica Integration.Version.

---


# Certificate Renewal no Incrementa Version

Una renovación de certificate no modifica Version por sí misma.

---

# Security y Performance

Una optimización no puede evitar controles de seguridad necesarios.

---

# No Security Bypass por Latencia

Debe mantenerse:

```text
Lower Latency

≠

Authorization Bypass
```

---

# No Security Bypass por Throughput

Debe mantenerse:

```text
Higher Throughput

≠

Permission Bypass
```

---

# Cache de Security Decisions

Este documento no define una estrategia de cache para decisiones de
Authorization.

---


# Cache no Cambia Semántica

Si existiera una estrategia técnica:

```text
Cached Authorization Decision

≠

New Domain Permission
```

---


# Performance no Justifica Secrets en Aggregate

No se almacenan credenciales dentro del Aggregate para acelerar
llamadas externas.

---


# Security y External Systems

Cada sistema externo mantiene sus propios mecanismos de seguridad.

---


# External Security Model

Debe mantenerse:

```text
External Security Model

≠

Integration Security Model
```

---

# Interoperability Security

Cualquier interoperabilidad debe preservar separación entre:

```text
AURA Authorization

External Authorization

Domain Contracts

Security Mechanisms
```

---


# No External Credential Ownership

Integration no adquiere ownership de credenciales de sistemas externos.

---


# External Credential Reference

Este documento no define si una implementación utiliza referencias
técnicas hacia credenciales externas.

Tal mecanismo pertenece fuera del Domain Model.

---


# Security y FIWARE

FIWARE permanece fuera del Aggregate.

---


# FIWARE Authentication

Un mecanismo de autenticación utilizado por FIWARE no se convierte en
parte del estado de Integration.

---


# FIWARE Authorization

El modelo de Authorization de FIWARE no reemplaza las Permissions de
AURA.

---


# FIWARE Credentials

Credenciales necesarias para interoperar con FIWARE permanecen fuera
del Aggregate.

---


# Security y Sistemas Municipales

Un sistema municipal puede poseer su propio modelo de seguridad.

Esto no redefine las Permissions de Integration.

---


# Municipal Credentials

Credenciales municipales permanecen fuera del Aggregate.

---


# Municipal Identity

Una identidad municipal no se convierte automáticamente en Citizen,
Role, Membership o Permission dentro de AURA.

---


# Security y Protocolos

Las reglas conceptuales no dependen de:

```text
HTTP

REST

GraphQL

MQTT

AMQP

WebSocket
```

---


# Security y Brokers

Las reglas conceptuales tampoco dependen de:

```text
Kafka

RabbitMQ

NATS
```

---


# Security y Frameworks

Este documento no exige:

- FastAPI;
- Django;
- Next.js;
- otro framework concreto.

---


# Security y Identity Protocols

Este documento no selecciona un protocolo concreto de Authentication o
Authorization.

---


# No OAuth Decision

Este documento no establece OAuth como obligación del dominio.

---


# No OIDC Decision

Este documento no establece OpenID Connect como obligación del dominio.

---


# No JWT Decision

Este documento no establece JWT como obligación del dominio.

---


# No mTLS Decision

Este documento no establece mutual TLS como obligación del dominio.

---


# No API Key Decision

Este documento no establece API Key como mecanismo obligatorio.

---


# No RBAC Decision

RBAC puede ser compatible.

Debe mantenerse:

```text
RBAC Compatible

≠

RBAC Required
```

---


# No ABAC Decision

ABAC puede ser compatible.

Debe mantenerse:

```text
ABAC Compatible

≠

ABAC Required
```

---


# No ACL Decision

Este documento no exige ACL como modelo técnico.

---


# No Policy Engine Decision

Este documento no selecciona un Policy Engine concreto.

---


# No Identity Provider Decision

Este documento no selecciona un Identity Provider concreto.

---


# No Cryptography Decision

Este documento no define:

- algoritmo criptográfico;
- tamaño de key;
- cipher suite;
- certificate authority;
- hashing algorithm.

---


# No Encryption Architecture Decision

La protección de datos puede requerir mecanismos técnicos.

Este documento no selecciona una implementación de encryption.

---


# Integrity

La información del Aggregate debe preservar su integridad.

Ningún mecanismo externo puede modificar directamente su estado
evitando Commands e Invariants.

---


# Confidentiality

Información no necesaria para un consumidor no debe ser expuesta por
defecto.

---


# Availability

La disponibilidad técnica del sistema no se convierte en un Lifecycle
State de Integration.

---


# Security Principles

Conceptualmente deben preservarse:

```text
Integrity

Confidentiality

Authorized Access

Least Privilege

Data Minimization

Boundary Protection
```

sin introducir una arquitectura técnica específica.

---


# Read Confidentiality

El acceso a información de lectura puede requerir reglas específicas de
Authorization.

---


# Write Integrity

Toda modificación debe atravesar comportamiento válido del Aggregate.

---


# Domain Event Integrity

Un Domain Event confirmado debe conservar su significado.

---


# Integration Event Confidentiality

Integration Event Payload debe limitarse a la información necesaria
para el contrato correspondiente.

---


# Integration Event Consumer

Un consumidor autorizado no obtiene ownership del Aggregate.

---


# Consumer Boundary

Debe mantenerse:

```text
Consumer Security Boundary

≠

Integration Consistency Boundary
```

---


# Consumer Failure

Un Consumer Failure relacionado con seguridad no modifica
automáticamente el Aggregate.

---


# Consumer Revocation

Revocar acceso de un consumidor no modifica por sí mismo:

```text
Integration.State

Integration.Version

Integration.UpdatedAt
```

---


# Security y Replay

Replay debe reconstruir hechos ya confirmados.

No crea una nueva identidad autorizada ni una nueva intención.

---


# Security y Event Sourcing

Event Sourcing es compatible.

No modifica las reglas de Authentication, Authorization o Permission.

---


# Event Sourcing no es Security Mechanism

Debe mantenerse:

```text
Event Sourcing

≠

Security Mechanism
```

---


# Security y CQRS

CQRS no cambia la autoridad del Aggregate.

---


# Write Security

Las Permissions de escritura protegen Commands.

---


# Read Security

Las políticas de lectura protegen Queries cuando corresponda.

---


# Read Security no Modifica Write Permissions

Debe mantenerse:

```text
Read Authorization

≠

Write Authorization
```

---


# Security y Repository Round-Trip

Persistir y recuperar Integration debe preservar:

```text
IntegrationId

State

Version

CreatedAt

UpdatedAt

Domain Information
```

sin incorporar credenciales.

---


# Rehydration no Recupera Secrets como Domain State

Un Aggregate rehidratado no debe depender de secretos almacenados como
parte de su estado de dominio.

---


# Security y Read Model Rebuild

Reconstruir un Read Model no debe exponer datos que el contrato de
lectura no deba mostrar.

---


# Security y External Payload

Debe mantenerse:

```text
Incoming External Payload

≠

Trusted Domain State
```

---


# External Input Validation

La información externa debe ser interpretada mediante contratos
explícitos antes de convertirse en una intención de dominio válida.

---


# External Input no Bypassea Invariants

Debe mantenerse:

```text
External Input

≠

Invariant Bypass
```

---


# External Input no Bypassea Permissions

Debe mantenerse:

```text
External Input

≠

Permission Bypass
```

---


# External Input no Bypassea Versioning

Debe mantenerse:

```text
External Input

≠

Versioning Bypass
```

---


# External Input no Expande Boundary

Debe mantenerse:

```text
External Input

≠

Consistency Boundary Expansion
```

---


# Security Event no es Domain Event Automático

Un hecho técnico de seguridad no crea automáticamente:

```text
IntegrationCreated

IntegrationActivated

IntegrationSuspended

IntegrationReactivated

IntegrationArchived
```

---


# No Security Domain Events Adicionales

La versión 1.0 no define:

```text
IntegrationAccessDenied

IntegrationAuthenticationFailed

IntegrationCompromised

IntegrationLocked

IntegrationUnlocked

IntegrationCredentialExpired
```

como Domain Events oficiales.

---


# No Security Commands Adicionales

La versión 1.0 no define:

```text
LockIntegration

UnlockIntegration

RotateIntegrationCredential

RevokeIntegrationToken

CompromiseIntegration

SecureIntegration
```

como Commands de dominio.

---


# No Security States Adicionales

La versión 1.0 no introduce:

```text
Locked

Blocked

Compromised

Unauthorized

Restricted
```

como States.

---


# Security Incident Handling

La respuesta técnica u operacional ante un Security Incident pertenece
fuera del Aggregate salvo que una futura decisión de dominio defina una
intención explícita mediante Commands existentes o nuevos contratos
formalmente aprobados.

---


# Security y ArchiveIntegration

Si una decisión de dominio autorizada requiere archivar una Integration:

```text
ArchiveIntegration
```

debe ejecutarse conforme a:

- Permission;
- State Machine;
- Guards;
- Invariants;
- Versioning.

La causa operacional no evita dichas reglas.

---


# Security y SuspendIntegration

Del mismo modo, una decisión de suspensión requiere:

```text
SuspendIntegration
```

válido desde:

```text
Active
```

---


# No Automatic Security Transition

Un detector técnico no puede realizar:

```text
setState(Suspended)
```

directamente.

---


# Security Logging

Logging técnico de seguridad permanece fuera del Aggregate.

---


# Security Metrics

Métricas de seguridad permanecen fuera del Aggregate.

---


# Security Monitoring

Monitoring de seguridad permanece fuera del Aggregate.

---


# Security Observability

Observability no constituye estado de dominio.

---


# Alert

Una alerta técnica no es un Domain Event de Integration por definición.

---


# Notification from Security Concern

Si una situación requiere Notification, dicho comportamiento pertenece
al Aggregate Notification conforme a sus propios contratos.

---


# Audit from Security Concern

Si un hecho debe registrarse formalmente en Audit, Audit conserva su
propio Consistency Boundary.

---


# Security y Data Ownership

Información de identidad proveniente de otro contexto mantiene su
ownership original.

---


# Identity Reference

Una referencia no convierte al sujeto externo en entidad interna de
Integration.

---


# Authorization Context

El contexto utilizado para tomar una decisión de Permission no se
incorpora automáticamente como parte persistente de Integration.

---


# Policy Snapshot

La versión 1.0 no define una copia persistida de la política de
Authorization dentro del Aggregate.

---


# Permission History

La versión 1.0 no define historial de Permissions como estado interno
de Integration.

---


# Authentication History

La versión 1.0 no define historial de autenticaciones dentro del
Aggregate.

---


# Access History

La versión 1.0 no define historial general de accesos como parte del
Aggregate.

---


# Security Read Model

Este documento no define un Read Model específico obligatorio de
seguridad.

---


# Security Integration Event

Este documento no define un Integration Event específico obligatorio
para incidentes de seguridad.

---


# Security Repository

Este documento no introduce un Repository adicional de seguridad dentro
del dominio Integration.

---


# Security Service

Este documento no introduce una clase o servicio concreto obligatorio
de seguridad.

---


# Security Policy Representation

Este documento no define una representación concreta de policies.

---


# Security Configuration

Configuración técnica de seguridad pertenece fuera del Aggregate.

---


# Security Configuration no Modifica Aggregate

Cambiar configuración técnica no modifica automáticamente:

```text
State

Version

UpdatedAt
```

---


# Security Deployment

Desplegar una nueva configuración de seguridad no produce Domain Event
de Integration.

---


# Security Infrastructure Failure

Un fallo del componente técnico de Authentication o Authorization no
introduce un nuevo State.

---


# Authorization Unavailable

Si no puede determinarse una autorización requerida:

```text
Protected Operation

=

Not Authorized to Proceed
```

sin modificar Integration.

---


# Authentication Unavailable

Si no puede establecerse Authentication requerida, la operación
protegida no debe considerarse autenticada.

Esto no cambia el Aggregate.

---


# Fail Secure Conceptual

Cuando no pueda establecerse una autorización requerida, no debe
asumirse Permission concedida.

---


# No Fail Open Inference

Debe mantenerse:

```text
Authorization Unavailable

≠

Permission Granted
```

---


# Security y Technical Retry

Retry técnico de Authentication o Authorization no constituye una nueva
modificación del Aggregate.

---


# Security y Redelivery

Redelivery de una intención técnica no crea automáticamente una nueva
intención de dominio.

---


# Idempotencia

La estrategia técnica de idempotencia no se define en este documento.

---


# Security y Concurrency

Una intención autorizada debe continuar respetando:

```text
ExpectedVersion

=

PersistedVersion
```

cuando corresponda.

---


# Elevated Privilege no Bypassea Concurrency

Debe mantenerse:

```text
Elevated Privilege

≠

Concurrency Bypass
```

---


# Administrative Access

La existencia de acceso administrativo técnico no concede
automáticamente todas las Permissions del dominio.

---


# Superuser no es Concepto del Aggregate

La versión 1.0 no define:

```text
Superuser
```

como concepto interno de Integration.

---


# Root Access no es Domain Permission

Debe mantenerse:

```text
Root Access

≠

Integration Permission
```

---


# Database Administrator

Un Database Administrator no obtiene por definición autoridad para
ejecutar Commands.

---


# Infrastructure Administrator

Un Infrastructure Administrator tampoco obtiene automáticamente
Domain Permissions.

---


# Security y Multi-Context

La interoperabilidad entre múltiples Bounded Contexts no crea un modelo
de seguridad compartido dentro de Integration.

---


# Cross-Context Identity

Una identidad proveniente de otro Bounded Context requiere
interpretación contractual.

---


# Cross-Context Permission

Una Permission externa no se convierte automáticamente en una
Permission de Integration.

---


# Cross-Context Ownership

Identity, Role, Membership y Permissions conservan ownership según sus
contextos correspondientes.

---


# No Identity Aggregate Embedding

No se embebe un Aggregate de identidad completo dentro de Integration.

---


# No Role Aggregate Embedding

No se embebe Role dentro de Integration.

---


# No Membership Aggregate Embedding

No se embebe Membership dentro de Integration.

---


# Security y Data Minimization en Commands

Un Command debe contener únicamente la información necesaria para
expresar la intención.

---


# Security y Data Minimization en Events

Un Event debe contener únicamente información necesaria para representar
el hecho o contrato.

---


# Security y Data Minimization en Read Models

Un Read Model debe contener únicamente información necesaria para su
finalidad de consulta.

---


# No Credential Propagation

Credentials no deben propagarse:

```text
Aggregate
    ↓
Domain Event
    ↓
Integration Event
    ↓
Read Model
```

como parte del Domain Model.

---


# No Secret Propagation

Debe mantenerse:

```text
Secret

∉

Aggregate

Domain Event

Integration Event

Domain Read Model
```

---


# Security y Performance Rules

Security debe respetar:

```text
DOMAIN-013N-Performance-Rules.md
```

sin aceptar optimizaciones que reduzcan garantías conceptuales.

---


# Security y Test Scenarios

Security debe validarse mediante escenarios coherentes con:

```text
DOMAIN-013M-Test-Scenarios.md
```

---


# Test Conceptual — Authentication Failure

```text
Given

an unauthenticated requester

When

a protected Command is attempted

Then

operation is rejected

And

Integration remains unchanged
```

---


# Test Conceptual — Permission Denied

```text
Given

an authenticated requester

And

required Permission is denied

When

a protected Command is attempted

Then

operation is rejected

And

State remains unchanged

And

Version remains unchanged

And

UpdatedAt remains unchanged

And

no success Domain Event is produced
```

---


# Test Conceptual — Authorized but Invalid State

```text
Given

Integration.Activate is allowed

And

State = Suspended

When

ActivateIntegration is attempted

Then

operation is rejected
```

---


# Test Conceptual — Authorized but Archived

```text
Given

Integration.Reactivate is allowed

And

State = Archived

When

ReactivateIntegration is attempted

Then

operation is rejected

And

Archived remains terminal
```

---


# Test Conceptual — Authorized but Version Conflict

```text
Given

required Permission is allowed

And

PersistedVersion = 6

And

ExpectedVersion = 5

When

a modification is attempted

Then

ConcurrencyConflict occurs
```

---


# Test Conceptual — No Secrets in Aggregate

```text
Given

Infrastructure credentials exist

When

Integration is persisted

Then

Password is absent

And

AccessToken is absent

And

RefreshToken is absent

And

ApiKey is absent

And

PrivateKey is absent

And

ClientSecret is absent

And

Secret is absent
```

---


# Test Conceptual — No Secrets in Domain Event

```text
Given

a valid Integration Domain Event

Then

credentials and secrets are absent from its domain payload
```

---


# Test Conceptual — No Secrets in Integration Event

```text
Given

an explicit Integration Event contract

When

an Integration Event is produced

Then

credentials and secrets are absent
```

---


# Test Conceptual — No Secrets in Read Model

```text
Given

a projected Integration Read Model

Then

credentials and secrets are absent from domain read data
```

---


# Test Conceptual — External Authorization

```text
Given

an actor is authorized in an external system

Then

Integration Permissions are not granted automatically
```

---


# Test Conceptual — FIWARE Authorization

```text
Given

an actor has FIWARE authorization

Then

no Integration Permission is inferred automatically
```

---


# Test Conceptual — Municipal Authorization

```text
Given

an actor has Municipal System authorization

Then

no Integration Permission is inferred automatically
```

---


# Test Conceptual — Incoming Event

```text
Given

an incoming Integration Event

When

it is received

Then

it does not mutate Integration directly

And

it does not bypass Authorization

And

it does not bypass Invariants

And

it does not bypass Versioning
```

---


# Test Conceptual — Security Incident

```text
Given

Integration State = Active

When

a technical Security Incident occurs

Then

State remains Active

unless a separate valid domain Command later changes it
```

---


# Test Conceptual — Credential Expiration

```text
Given

Integration State = Active

When

an external credential expires

Then

no automatic SuspendIntegration occurs
```

---


# Test Conceptual — Security Policy Change

```text
Given

Integration State = Active

And

Version = N

When

an Authorization Policy changes externally

Then

State remains Active

And

Version remains N

And

UpdatedAt remains unchanged
```

---


# Test Conceptual — Repository Access

```text
Given

a technical component can access IntegrationRepository

Then

no Integration Permission is inferred from Repository access alone
```

---


# Test Conceptual — Database Access

```text
Given

an operator has database privileges

Then

no Domain Permission is inferred
```

---


# Test Conceptual — Read Access

```text
Given

a requester can read Integration information

Then

no write Permission is inferred
```

---


# Test Conceptual — Permission does not Expand Boundary

```text
Given

Integration.Archive is allowed

When

ArchiveIntegration succeeds

Then

only the target Integration Aggregate is modified
```

---


# Evolución Futura

La evolución del Security Model puede incorporar nuevos requisitos
solamente cuando exista una necesidad explícita del dominio o de sus
contratos.

---


# Nueva Permission

Una nueva Permission requiere una capacidad real del dominio.

---


# Nuevo Security State

Un nuevo State relacionado con seguridad no debe incorporarse sin una
decisión formal sobre:

- Lifecycle;
- State Machine;
- Commands;
- Domain Events;
- Invariants;
- Permissions;
- Versioning.

---


# Nuevo Security Command

Un nuevo Command relacionado con seguridad requiere una intención real
del dominio y definición coordinada.

---


# Nuevo Security Domain Event

Un nuevo Domain Event relacionado con seguridad requiere un hecho de
dominio confirmado.

---


# Nuevo Security Integration Event

Un Integration Event relacionado con seguridad requiere un contrato
explícito.

---


# Nueva Identity Integration

Una nueva fuente de identidad no modifica por sí misma el Aggregate.

---


# Nuevo Authorization Provider

Cambiar el mecanismo de Authorization no modifica las Permissions
conceptuales del dominio.

---


# Nueva Authentication Technology

Cambiar la tecnología de Authentication no redefine Integration.

---


# Nueva Cryptography Technology

Cambiar mecanismos criptográficos técnicos no modifica:

```text
IntegrationId

State

Version

Lifecycle

Commands

Domain Events
```

por sí mismo.

---


# Nueva Credential Strategy

Una estrategia distinta de credenciales no modifica el Domain Model
mientras las credenciales permanezcan fuera del Aggregate.

---


# Impacto de Evolución

Toda modificación significativa del Security Model debe revisar cuando
corresponda:

```text
DOMAIN-013-Aggregate.md

DOMAIN-013A-Lifecycle.md

DOMAIN-013B-State-Machine.md

DOMAIN-013C-Commands.md

DOMAIN-013D-Domain-Events.md

DOMAIN-013E-Invariants.md

DOMAIN-013F-Permissions.md

DOMAIN-013G-Repository-Contract.md

DOMAIN-013I-Versioning.md

DOMAIN-013J-Consistency-Boundary.md

DOMAIN-013K-Integration-Events.md

DOMAIN-013L-Read-Model.md

DOMAIN-013M-Test-Scenarios.md

DOMAIN-013N-Performance-Rules.md

DOMAIN-013O-Security-Model.md

DOMAIN-013P-Extension-Points.md
```

---

# Regla de No Inferencia

Debe mantenerse:

```text
Security Requirement

≠

New Domain State
```

y:

```text
Security Mechanism

≠

New Domain Command
```

y:

```text
Technical Security Event

≠

Domain Event
```

y:

```text
External Authorization

≠

Automatic AURA Permission
```

y:

```text
Credential

≠

Aggregate State
```

y:

```text
Authentication Technology

≠

Domain Architecture Decision
```

---


# Reglas Fundamentales

El Security Model de Integration debe cumplir:

1. Security protege comportamiento del dominio sin sustituirlo.
2. Authentication permanece fuera del Aggregate.
3. Authentication no es Authorization.
4. Authorization no es Domain Validation.
5. Authorized no significa automáticamente Domain Valid.
6. Permissions oficiales protegen los Commands oficiales.
7. Integration.Create protege CreateIntegration.
8. Integration.Activate protege ActivateIntegration.
9. Integration.Suspend protege SuspendIntegration.
10. Integration.Reactivate protege ReactivateIntegration.
11. Integration.Archive protege ArchiveIntegration.
12. Permission no es Command.
13. Permission no evita State Machine.
14. Permission no evita Guards.
15. Permission no evita Invariants.
16. Permission no evita Versioning.
17. Permission no evita ConcurrencyConflict.
18. Permission no permite setState().
19. Permission no permite setVersion().
20. Permission no permite modificar IntegrationId.
21. Permission no permite modificar CreatedAt.
22. Archived permanece terminal incluso para requesters autorizados.
23. Deny by Default aplica a capacidades protegidas.
24. Least Privilege limita la autoridad a la capacidad necesaria.
25. Role permanece fuera del Aggregate.
26. Role no es Permission.
27. Membership permanece fuera del Aggregate.
28. Membership no concede Permission automáticamente.
29. Citizen permanece fuera del Aggregate.
30. Requester no se confunde automáticamente con ActorId.
31. ActorId no es Permission.
32. ActorId no es Authorization.
33. CorrelationId no concede Permission.
34. CausationId no concede Permission.
35. IntegrationId no concede Permission.
36. Authentication Failure no modifica State.
37. Authentication Failure no modifica Version.
38. Authentication Failure no modifica UpdatedAt.
39. Authorization Failure no modifica State.
40. Authorization Failure no modifica Version.
41. Authorization Failure no modifica UpdatedAt.
42. Authentication Failure no produce Domain Event de éxito.
43. Authorization Failure no produce Domain Event de éxito.
44. Permission Denied no es Lifecycle State.
45. Authorized no es Lifecycle State.
46. Unauthorized no es Lifecycle State.
47. Security Incident no suspende automáticamente Integration.
48. Security Recovery no reactiva automáticamente Integration.
49. Credentials permanecen fuera del Aggregate.
50. Password no forma parte del Aggregate.
51. AccessToken no forma parte del Aggregate.
52. RefreshToken no forma parte del Aggregate.
53. ApiKey no forma parte del Aggregate.
54. PrivateKey no forma parte del Aggregate.
55. ClientSecret no forma parte del Aggregate.
56. Secret no forma parte del Aggregate.
57. Credential Rotation no modifica Integration automáticamente.
58. Credential Expiration no suspende Integration automáticamente.
59. El mecanismo de Secret Storage no se define aquí.
60. El mecanismo de Key Management no se define aquí.
61. Domain Events no contienen Secrets.
62. Domain Events aplican Data Minimization.
63. EventId no concede Authorization.
64. AggregateVersion no concede Authorization.
65. ActorId en Domain Events no es Credential.
66. Confirmed Domain Events preservan integridad histórica.
67. Replay no representa nueva Authorization.
68. Rehydration no representa nueva intención protegida.
69. Integration Events requieren contrato explícito.
70. Integration Event Payload aplica Data Minimization.
71. Integration Events no contienen Secrets.
72. Consumir Integration Event no concede Write Authority.
73. Incoming Integration Event no modifica directamente Integration.
74. Incoming Integration Event no evita Authorization.
75. External Message no es Permission.
76. External Message no es Command automático.
77. External Authorization no es AURA Authorization.
78. FIWARE Authorization no concede Permissions automáticamente.
79. Municipal Authorization no concede Permissions automáticamente.
80. Authorization Mapping requiere contrato explícito.
81. Repository no decide Authorization.
82. Repository Access no concede Permission.
83. Database Privilege no es Domain Permission.
84. Read Permission no es Write Permission.
85. Read Model no decide Authorization.
86. Read Models no exponen Secrets como datos del dominio.
87. Security no expande Consistency Boundary.
88. Authentication permanece fuera del Boundary.
89. Authorization permanece fuera del Aggregate State.
90. Identity Provider permanece fuera del Aggregate.
91. Policy Engine permanece fuera del Aggregate.
92. Authorization Policy Change no modifica State automáticamente.
93. Authorization Policy Change no incrementa Version automáticamente.
94. Authentication o Authorization technology no redefine el Domain
    Model.
95. Security no puede evitarse por Performance.
96. RBAC puede ser compatible pero no es obligatorio.
97. ABAC puede ser compatible pero no es obligatorio.
98. Ningún protocolo o mecanismo técnico de seguridad es impuesto por
    este documento.
99. Toda evolución de Security requiere preservar Lifecycle,
    Invariants, Versioning y Consistency Boundary.
100. Toda evolución futura debe preservar el patrón consolidado de AURA
     Core.

---

# Restricciones

No está permitido:

- incorporar Authentication dentro del Aggregate;
- incorporar Authorization como State;
- incorporar Permissions como State mutable del Aggregate;
- interpretar Authentication como Authorization;
- interpretar Authorization como Domain Validation;
- considerar Permission como garantía de éxito;
- evitar State Machine mediante privilegios;
- evitar Guards mediante privilegios;
- evitar Invariants mediante privilegios;
- evitar Versioning mediante privilegios;
- evitar ConcurrencyConflict mediante privilegios;
- ejecutar setState() mediante Permission;
- ejecutar setVersion() mediante Permission;
- modificar IntegrationId por privilegio;
- modificar CreatedAt por privilegio;
- reactivar Archived mediante privilegio;
- introducir Authorized como State;
- introducir Unauthorized como State;
- introducir Locked como State;
- introducir Blocked como State;
- introducir Compromised como State;
- suspender automáticamente Integration por Authentication Failure;
- suspender automáticamente Integration por Authorization Failure;
- suspender automáticamente Integration por Credential Expiration;
- suspender automáticamente Integration por Security Incident;
- reactivar automáticamente Integration por recuperación técnica;
- almacenar Password dentro del Aggregate;
- almacenar AccessToken dentro del Aggregate;
- almacenar RefreshToken dentro del Aggregate;
- almacenar ApiKey dentro del Aggregate;
- almacenar PrivateKey dentro del Aggregate;
- almacenar ClientSecret dentro del Aggregate;
- almacenar Secret dentro del Aggregate;
- incorporar credenciales en Domain Events;
- incorporar credenciales en Integration Events;
- incorporar credenciales en Domain Read Models;
- exponer Aggregate completo por conveniencia de seguridad;
- copiar perfiles completos de identidad dentro del Aggregate;
- embebir Citizen como Security State;
- embebir Role como Security State;
- embebir Membership como Security State;
- interpretar ActorId como Authorization;
- interpretar CorrelationId como Permission;
- interpretar CausationId como Permission;
- interpretar IntegrationId como Permission;
- interpretar una autorización FIWARE como AURA Permission;
- interpretar una autorización municipal como AURA Permission;
- interpretar acceso técnico a Repository como Permission;
- interpretar acceso de base de datos como Permission;
- interpretar Read Access como Write Access;
- modificar directamente persistencia evitando el Aggregate;
- utilizar Incoming Integration Event para setState();
- utilizar External Message para evitar Authorization;
- utilizar External Payload como Trusted Domain State;
- crear IntegrationAccessDenied como Domain Event sin definición formal;
- crear IntegrationAuthenticationFailed como Domain Event sin definición
  formal;
- crear IntegrationCompromised como Domain Event sin definición formal;
- crear LockIntegration como Command sin definición formal;
- crear UnlockIntegration como Command sin definición formal;
- crear RotateIntegrationCredential como Command sin definición formal;
- introducir Security Repository adicional sin necesidad explícita;
- introducir Security Read Model obligatorio sin necesidad explícita;
- imponer OAuth;
- imponer OpenID Connect;
- imponer JWT;
- imponer mTLS;
- imponer API Key;
- imponer RBAC;
- imponer ABAC;
- imponer ACL;
- imponer Identity Provider;
- imponer Policy Engine;
- imponer Secret Manager;
- imponer algoritmo criptográfico;
- imponer estrategia de encryption;
- imponer mecanismo técnico de Key Management;
- introducir decisiones arquitectónicas nuevas desde este documento.

---

# Compatibilidad Arquitectónica

El Security Model de Integration es compatible conceptualmente con:

- Domain-Driven Design;
- Aggregate Pattern;
- Repository Pattern;
- Command Pattern;
- Domain Event Pattern;
- Clean Architecture;
- Hexagonal Architecture;
- SOLID;
- CQRS Compatible;
- Event-Driven Architecture;
- Event Sourcing Compatible;
- Optimistic Concurrency Control;
- consistencia eventual;
- Least Privilege;
- Deny by Default;
- Data Minimization;
- High Cohesion;
- Low Coupling.

Estas compatibilidades no imponen:

- OAuth;
- OpenID Connect;
- JWT;
- mTLS;
- API Key;
- RBAC;
- ABAC;
- ACL;
- Identity Provider;
- Policy Engine;
- Secret Manager;
- algoritmo criptográfico;
- broker;
- protocolo;
- framework;
- base de datos;
- FIWARE;
- NGSI-LD;
- plataforma municipal.

---

# Definición de Éxito

El Security Model del Aggregate **Integration** protege sus capacidades
de modificación y exposición de información sin incorporar mecanismos
técnicos de seguridad dentro del Domain Model.

El modelo fundamental queda expresado como:

```text
Requester
    │
    ▼
Authentication
    │
    ▼
Authorization
    │
    ▼
Permission
    │
    ▼
Command
    │
    ▼
Integration Aggregate
    │
    ├── State Machine
    ├── Guards
    ├── Invariants
    ├── Versioning
    └── Consistency Boundary
```

mientras:

```text
Credentials

Secrets

Identity Provider

Policy Engine

External Security Infrastructure

∉

Integration Aggregate
```

y:

```text
Authorized

≠

Automatically Valid
```

El modelo garantiza que:

- Authentication permanezca fuera del Aggregate;
- Authorization permanezca separada de Domain Validation;
- Permissions protejan exclusivamente capacidades explícitas;
- Deny by Default preserve operaciones protegidas;
- Least Privilege limite autoridad;
- State Machine no pueda evitarse;
- Invariants no puedan evitarse;
- Versioning no pueda evitarse;
- Archived permanezca terminal;
- IntegrationId permanezca inmutable;
- CreatedAt permanezca inmutable;
- Authentication Failure no modifique el Aggregate;
- Authorization Failure no modifique el Aggregate;
- Security Incident no cree automáticamente nuevos States;
- credenciales permanezcan fuera del Aggregate;
- secretos permanezcan fuera del Aggregate;
- Domain Events no expongan credenciales;
- Integration Events no expongan credenciales;
- Read Models no expongan secretos como información del dominio;
- External Authorization no se convierta automáticamente en AURA
  Authorization;
- FIWARE Authorization permanezca separada;
- Municipal Authorization permanezca separada;
- Repository Access no equivalga a Domain Permission;
- Read Access no equivalga a Write Access;
- Incoming Integration Events no eviten controles de dominio;
- Data Minimization se preserve en Commands, Events y Read Models;
- Security no expanda el Consistency Boundary;
- Role, Membership y Citizen mantengan ownership independiente;
- Audit y Notification mantengan sus propios Boundaries;
- Performance no permita omitir controles;
- Event Sourcing permanezca compatible pero no obligatorio;
- CQRS permanezca compatible pero no obligatorio;
- ninguna tecnología de Authentication, Authorization, criptografía,
  transporte o almacenamiento de secretos sea impuesta;
- cualquier evolución futura de Security preserve Lifecycle,
  Permissions, Invariants, Versioning y Consistency Boundary.

De esta forma, `DOMAIN-013O-Security-Model.md` establece formalmente el
Security Model oficial del Aggregate **Integration** conforme al patrón
consolidado de AURA Core.