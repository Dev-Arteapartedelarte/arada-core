# DOMAIN-012O — Audit Security Model

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Audit Management

Aggregate:
Audit

Documentos relacionados:

- DOMAIN-012-Aggregate.md
- DOMAIN-012A-Lifecycle.md
- DOMAIN-012B-State-Machine.md
- DOMAIN-012C-Commands.md
- DOMAIN-012D-Domain-Events.md
- DOMAIN-012E-Invariants.md
- DOMAIN-012F-Permissions.md
- DOMAIN-012G-Repository-Contract.md
- DOMAIN-012H-Examples.md
- DOMAIN-012I-Versioning.md
- DOMAIN-012J-Consistency-Boundary.md
- DOMAIN-012K-Integration-Events.md
- DOMAIN-012L-Read-Model.md
- DOMAIN-012M-Test-Scenarios.md
- DOMAIN-012N-Performance-Rules.md
- DOMAIN-012P-Extension-Points.md

---

# Objetivo

Este documento define formalmente el **Security Model** conceptual
del Aggregate **Audit**.

El Security Model establece las reglas que protegen:

- acceso a capacidades del dominio;
- confidencialidad de la información;
- minimización de datos;
- integridad conceptual;
- trazabilidad;
- separación de responsabilidades;
- exposición controlada hacia Read Models;
- exposición controlada hacia Integration Events.

Security no reemplaza las reglas propias del Aggregate.

---

# Principio Fundamental

Debe mantenerse:

```text
Security

≠

Domain Rule Replacement
```

y:

```text
Authorized

≠

Automatically Valid
```

Una operación autorizada continúa sujeta a:

- State Machine;
- Invariants;
- Versioning;
- Consistency Boundary.

---

# Separation of Concerns

Debe mantenerse separación explícita entre:

```text
Authentication

Authorization

Domain Validation

Data Protection
```

Conceptualmente:

```text
Actor / Process
      │
      ▼
Authentication
      │
      ▼
Authorization
      │
      ▼
Domain Command
      │
      ▼
Audit Validation
      │
      ▼
Audit State
```

---

# Authentication

Authentication permanece fuera del Aggregate.

Audit no:

- valida passwords;
- valida tokens;
- crea sesiones;
- mantiene sesiones;
- autentica usuarios;
- autentica servicios;
- administra proveedores de identidad.

Debe mantenerse:

```text
Authentication

∉

Audit Aggregate
```

---

# Authorization

Authorization determina si un actor o proceso puede solicitar una
capacidad del dominio.

En versión 1.0, la única capacidad de escritura oficial es:

```text
RecordAudit
```

Debe mantenerse:

```text
Authorization

before

Domain Behavior
```

---

# Permissions

Las reglas conceptuales de Permissions se encuentran definidas en:

```text
DOMAIN-012F-Permissions.md
```

El Security Model debe preservar:

```text
Permission

≠

Invariant Override
```

---

# Deny by Default

Debe aplicarse:

```text
No Explicit Authorization

↓

Denied
```

La ausencia de autorización no se interpreta como permiso implícito.

---

# Least Privilege

Toda capacidad debe concederse aplicando:

```text
Least Privilege
```

Un actor o proceso debe disponer únicamente de las capacidades
necesarias para cumplir su responsabilidad.

---

# RecordAudit Security

`RecordAudit` solamente puede ingresar al comportamiento del
Aggregate después de una decisión de autorización válida.

Conceptualmente:

```text
Authorized Actor / Process
    │
    ▼
RecordAudit
    │
    ▼
Audit
```

---

# RecordAudit Rechazado por Seguridad

Si Authorization rechaza:

```text
RecordAudit
```

no debe producirse:

```text
Audit

AuditRecorded

Version = 1
```

para dicha intención.

---

# Security no Introduce Commands

El Security Model no crea nuevos Commands.

La versión 1.0 continúa definiendo únicamente:

```text
RecordAudit
```

---

# Security no Introduce Estados

Security no crea estados como:

```text
Locked

Restricted

Hidden

Redacted

Secured

Blocked
```

dentro del Lifecycle de Audit.

---

# Security no Introduce Domain Events

El Security Model no introduce automáticamente Domain Events como:

```text
AuditAccessDenied

AuditAccessGranted

AuditSecured

AuditRedacted

AuditAnonymized
```

Estos eventos no forman parte del modelo oficial versión 1.0.

---

# Security no Modifica State Machine

Ninguna política de seguridad puede habilitar una transición no
definida.

Debe mantenerse:

```text
Security Policy

≠

State Machine Extension
```

---

# Security no Modifica Lifecycle

El Lifecycle oficial permanece:

```text
No Audit → Recorded
```

con:

```text
Recorded
```

como estado terminal.

---

# Security no Modifica AuditId

Ninguna autorización concede capacidad para cambiar:

```text
AuditId
```

Debe mantenerse:

```text
Security Privilege

≠

Identity Mutation Authority
```

---

# Security no Modifica Version

Ninguna política de seguridad puede establecer directamente:

```text
Audit.Version
```

Version permanece gobernada por el comportamiento del Aggregate.

---

# Security no Modifica CreatedAt

`CreatedAt` permanece inmutable.

Ningún privilegio de seguridad permite alterarlo.

---

# Security no Reescribe Historia

Un actor autorizado no puede reinterpretar o reescribir un hecho
Audit ya confirmado.

Debe mantenerse:

```text
Authorization

≠

Historical Rewrite Authority
```

---

# Data Minimization

Audit debe preservar únicamente información necesaria para su
propósito de trazabilidad.

Debe mantenerse:

```text
Minimum Necessary Data
```

como principio fundamental.

---

# Source Payload

La existencia de información en el Source Payload no implica que deba
formar parte de Audit.

Debe mantenerse:

```text
Source Data Exists

≠

Audit Must Store It
```

---

# Aggregate Payload

Audit no debe almacenar el Aggregate originador completo.

Debe mantenerse:

```text
Source Aggregate

≠

Audit Internal State
```

---

# Datos Opcionales

Información como:

```text
ActorId

CorrelationId

CausationId

SourceEventId
```

solamente se preserva cuando:

- esté disponible;
- sea aplicable;
- forme parte del contrato;
- sea necesaria.

---

# Información Ausente

Debe mantenerse:

```text
Missing Information

≠

Fabricated Information
```

Audit no debe inventar:

- ActorId;
- CorrelationId;
- CausationId;
- SourceEventId;
- SourceAggregateVersion.

---

# Credenciales

Audit no debe almacenar:

```text
Password

AccessToken

RefreshToken

ApiKey

PrivateKey

Secret

Session
```

ni conceptos equivalentes.

---

# Passwords

Debe mantenerse:

```text
Password

∉

Audit Aggregate
```

incluso si aparece en una fuente técnica.

---

# Access Tokens

Los Access Tokens pertenecen a Security o Infrastructure.

No forman parte del estado de Audit.

---

# Refresh Tokens

Los Refresh Tokens no deben incorporarse a:

- Audit;
- AuditRecorded;
- Audit Read Models;
- Audit Integration Events.

---

# API Keys

Las API Keys no representan información de dominio.

Deben permanecer fuera del Aggregate.

---

# Private Keys

Las Private Keys no deben formar parte de:

```text
Audit State
```

ni de sus eventos.

---

# Secrets

Los secretos técnicos permanecen fuera del Domain Model.

Debe mantenerse:

```text
Secret

∉

Domain State
```

---

# Security Claims

Claims técnicos de identidad o autorización no forman parte
automáticamente del estado de Audit.

Debe mantenerse:

```text
Security Claim

≠

Audit Domain State
```

---

# ActorId

ActorId representa información de trazabilidad cuando corresponda.

Debe mantenerse:

```text
ActorId

≠

Authorization
```

---

# Source Actor y Requester

El actor asociado al hecho auditado puede ser distinto del actor o
proceso que presenta:

```text
RecordAudit
```

Debe mantenerse:

```text
Source Actor

≠

Command Requester
```

salvo que el contrato correspondiente establezca equivalencia.

---

# Identity Knowledge

Conocer:

```text
AuditId
```

no concede acceso.

Debe mantenerse:

```text
Knowledge of Identifier

≠

Authorization
```

---

# CorrelationId

CorrelationId permite trazabilidad.

No representa:

- Permission;
- Authentication;
- Authorization;
- ownership.

---

# CausationId

CausationId preserva causalidad cuando corresponde.

No concede autoridad sobre Audit.

---

# SourceEventId

SourceEventId identifica un hecho de origen cuando exista.

No representa:

```text
Permission
```

---

# SourceAggregateId

SourceAggregateId no concede autoridad sobre el Source Aggregate ni
sobre Audit.

---

# External References

Las referencias externas deben tratarse como referencias.

Debe mantenerse:

```text
External Reference

≠

Embedded External Aggregate
```

---

# Consistency Boundary

Security no amplía el Consistency Boundary.

Audit continúa protegiendo únicamente:

```text
Audit
```

dentro de su propia unidad.

---

# Security y Otros Aggregates

Una Permission de Audit no concede autoridad sobre:

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

Integration
```

---

# No Cross-Aggregate Security Authority

Debe mantenerse:

```text
Audit Permission

≠

Permission on Another Aggregate
```

---

# Organization

La autorización sobre Audit no implica autorización sobre
Organization.

---

# Citizen

La existencia de ActorId no concede acceso al Aggregate Citizen.

---

# Membership

Audit no puede modificar Membership mediante una capacidad de
seguridad propia.

---

# Role

Audit no administra:

- asignación de Roles;
- revocación de Roles;
- jerarquía de Roles;
- Permissions globales.

---

# Territory

Las referencias territoriales no incorporan Territory dentro del
Security Boundary de Audit.

---

# Assembly

Una Permission para RecordAudit no concede capacidad para modificar:

```text
AssemblyStatus

Assembly.Version
```

---

# Proposal

Una Permission de Audit no concede autoridad sobre Proposal.

---

# Participation

Audit no utiliza su Security Model para modificar Participation.

---

# Voting

Audit no puede:

- registrar votos;
- modificar votos;
- abrir Voting;
- cerrar Voting;
- modificar resultados;

mediante Permissions propias.

---

# Document

Una Permission de Audit no concede acceso universal al contenido de
Document.

---

# Notification

Una Permission de Audit no concede autoridad sobre:

```text
NotificationStatus

Notification.Version
```

---

# Integration

Integration mantiene sus propias políticas de seguridad.

Audit no administra seguridad de sistemas externos.

---

# Read Security

El acceso a Read Models debe aplicar políticas de lectura.

Debe mantenerse:

```text
Read Permission

≠

Write Permission
```

---

# Read Permission

Un actor autorizado para consultar una vista no obtiene
automáticamente permiso para:

```text
RecordAudit
```

---

# Write Permission

Un actor autorizado para:

```text
RecordAudit
```

no obtiene automáticamente acceso a todos los Read Models.

---

# Public Read Access

La versión 1.0 no establece acceso público universal a Audit.

Debe mantenerse:

```text
Historical Data

≠

Public Data
```

---

# Internal Read Access

Una vista interna tampoco implica acceso irrestricto.

Authorization continúa siendo aplicable.

---

# Read Model Minimization

Cada Read Model debe contener solamente la información necesaria para
su propósito.

Debe mantenerse:

```text
Audit State

≠

Automatic Read Projection
```

---


# ActorId en Read Models

ActorId no debe exponerse automáticamente en todas las vistas.

Su inclusión depende de:

- finalidad;
- necesidad;
- política de acceso;
- minimización.

---

# Source Payload en Read Models

Un Read Model no debe exponer automáticamente:

```text
Entire Source Payload
```

---

# Domain Event Payload en Read Models

La existencia de datos en:

```text
AuditRecorded
```

no obliga a exponerlos todos en lectura.

---

# Integration Security

La publicación externa debe respetar:

- minimización;
- autorización de consumidores;
- ausencia de credenciales;
- confidencialidad;
- trazabilidad.

---

# Integration Event Minimization

Debe mantenerse:

```text
Audit State

≠

Automatic Integration Payload
```

---

# AuditRecordedIntegrationEvent

`AuditRecordedIntegrationEvent` solamente debe contener información
necesaria para su contrato público.

---

# Integration Event y Credenciales

No deben publicarse:

```text
Password

AccessToken

RefreshToken

ApiKey

PrivateKey

Secret
```

dentro del Integration Event.

---

# Consumer Authorization

La recepción de un Integration Event no concede Permission sobre
Audit.

Debe mantenerse:

```text
Integration Event

≠

Authorization Grant
```

---

# External Consumer

Un consumidor externo puede recibir información autorizada.

No puede modificar directamente:

```text
AuditId

AuditStatus

Audit.Version
```

---


# FIWARE

FIWARE permanece fuera del Aggregate.

Una identidad técnica autenticada en FIWARE no constituye
automáticamente:

```text
Audit Permission
```

---


# FIWARE Credentials

Tokens, client secrets o credenciales FIWARE no forman parte de Audit.

---


# NGSI-LD

Una representación NGSI-LD no define políticas de seguridad internas
del Aggregate.

Debe mantenerse:

```text
NGSI-LD Security Model

≠

Audit Domain Security Model
```

---


# Sistemas Municipales

Una identidad o permiso de un sistema municipal no se traduce
automáticamente en una Permission de AURA.

Debe mantenerse:

```text
Municipal Authorization

≠

Automatic Audit Authorization
```

---


# Anti-Corruption Layer

Cuando un sistema externo posea su propio modelo de seguridad, la
traducción de identidades y capacidades debe ocurrir en la frontera
correspondiente.

Audit no incorpora directamente el modelo externo.

---


# RBAC

El modelo es compatible conceptualmente con:

```text
Role-Based Access Control
```

sin que Audit defina Roles internos obligatorios.

---


# ABAC

El modelo es compatible conceptualmente con:

```text
Attribute-Based Access Control
```

sin convertir atributos de autorización en estado obligatorio del
Aggregate.

---


# RBAC y ABAC

Debe mantenerse:

```text
Authorization Model

outside

Audit Aggregate
```

independientemente de la estrategia utilizada.

---


# Delegación

La versión 1.0 no define:

- delegación de autoridad;
- duración de delegación;
- transferencia de Permissions;
- jerarquías de delegación.

Cualquier regla futura requiere definición explícita.

---


# Impersonation

La versión 1.0 no define reglas de impersonation dentro de Audit.

No debe inferirse:

```text
Actor A

may act as

Actor B
```

sin un contrato explícito.

---


# Security y Domain Events

`AuditRecorded` solamente puede producirse después de una operación
válida.

Una operación no autorizada no produce:

```text
AuditRecorded
```

---


# Domain Event no Contiene Credenciales

`AuditRecorded` no debe incluir credenciales técnicas.

---


# Domain Event Minimization

El Payload de AuditRecorded debe contener únicamente información
necesaria para representar el hecho de dominio.

---


# Domain Event no Concede Authority

Consumir:

```text
AuditRecorded
```

no concede capacidad para modificar Audit.

---


# EventId

EventId identifica un Domain Event.

No constituye una Permission.

---


# Event Immutability

Un Domain Event confirmado mantiene significado histórico estable.

Debe mantenerse:

```text
Confirmed Event

≠

Mutable Security Object
```

---


# Security y Versioning

Ningún actor autorizado puede omitir:

```text
Optimistic Concurrency
```

cuando corresponda.

Debe mantenerse:

```text
Authorized Write

≠

Concurrency Bypass
```

---


# ExpectedVersion

La autorización no permite alterar:

```text
ExpectedVersion
```

para evitar un conflicto.

---


# ConcurrencyConflict

Un:

```text
ConcurrencyConflict
```

no debe ignorarse por privilegios de seguridad.

---


# Security no Fuerza Last-Write-Wins

Ninguna política de autorización introduce automáticamente:

```text
Last Write Wins
```

como política de concurrencia.

---


# Repository Security

El Repository no decide Permissions.

Debe mantenerse:

```text
Repository

≠

Authorization Authority
```

---


# Repository Access

El acceso técnico al Repository no equivale a:

```text
Domain Permission
```

---


# Infrastructure Access

Tener acceso a:

- base de datos;
- broker;
- filesystem;
- cache;
- API;
- plataforma externa;

no concede autoridad de dominio.

---


# Direct Database Access

Acceso directo a una base de datos no debe considerarse una vía
válida para evitar:

- Aggregate Root;
- Invariants;
- Versioning;
- Permissions.

Debe mantenerse:

```text
Database Privilege

≠

Domain Authority
```

---


# Direct Broker Access

Publicar directamente un mensaje en un broker no equivale a ejecutar
comportamiento válido de Audit.

---


# Direct API Access

Acceder técnicamente a un endpoint no implica que la operación sea
autorizada o válida en dominio.

---


# Security y Infrastructure

La implementación técnica puede utilizar controles adicionales.

Sin embargo, dichos controles no cambian:

- AuditId;
- Lifecycle;
- State Machine;
- Commands;
- Domain Events;
- Invariants;
- Versioning;
- Consistency Boundary.

---


# Confidentiality

La información Audit debe exponerse únicamente a consumidores
autorizados conforme al contexto aplicable.

Debe mantenerse:

```text
Data Exists

≠

Data Is Visible to Everyone
```

---


# Integrity

Security debe preservar que información confirmada no sea modificada
mediante canales externos que eviten el Aggregate.

---


# Availability

La indisponibilidad técnica no modifica las reglas del Aggregate.

Debe mantenerse:

```text
Security / Infrastructure Failure

≠

AuditStatus Change
```

---


# Security Failure

Un fallo técnico de seguridad no crea:

```text
AuditStatus = Failed
```

---


# Authentication Failure

Un fallo de Authentication no crea una unidad Audit automáticamente.

Debe mantenerse:

```text
AuthenticationFailed

≠

Automatic RecordAudit
```

---


# Authorization Failure

Un rechazo de Authorization tampoco crea Audit automáticamente.

Debe mantenerse:

```text
AuthorizationDenied

≠

Automatic RecordAudit
```

---


# Auditar Eventos de Seguridad

Una decisión o fallo de seguridad puede ser auditable cuando exista
un contrato explícito que lo defina como hecho auditable.

Debe mantenerse:

```text
Security Event

≠

Automatic Audit
```

---


# No Recursividad Automática

El hecho de que Audit registre hechos de seguridad no debe provocar
ciclos automáticos de:

```text
Audit of Audit of Audit
```

sin una definición explícita.

---


# Logs de Seguridad

Los logs de seguridad permanecen separados de Audit.

Debe mantenerse:

```text
Security Log

≠

Audit Aggregate
```

---


# Observability

Metrics, traces y logs técnicos de seguridad permanecen fuera del
Consistency Boundary.

---


# Security Metrics

Información como:

```text
FailedLoginCount

TokenValidationLatency

AuthorizationLatency

BlockedRequestCount
```

no forma parte automáticamente de Audit.

---


# Encryption

El Security Model es compatible con protección criptográfica de datos.

Sin embargo, la versión 1.0 no define:

- algoritmo;
- tamaño de clave;
- proveedor;
- modo de cifrado;
- gestión de claves.

Estas decisiones pertenecen a arquitectura e Infrastructure.

---


# Encryption at Rest

La protección física de datos almacenados puede incluir cifrado.

Esto no modifica el Domain Model.

---


# Encryption in Transit

La protección del transporte puede incluir cifrado.

El Aggregate no conoce el protocolo utilizado.

---


# Hashing

La versión 1.0 no exige:

```text
Hash

Checksum

Digital Signature
```

como atributos obligatorios de Audit.

Introducirlos como parte del dominio requiere definición explícita.

---


# Digital Signature

Una firma técnica puede proteger mensajes o almacenamiento.

No se convierte automáticamente en:

- Value Object de Audit;
- Invariant;
- Domain Event.

---


# Tamper Resistance

El significado histórico de Audit debe permanecer protegido.

Sin embargo, este documento no selecciona una estrategia física
específica de:

- WORM storage;
- blockchain;
- append-only database;
- signature chain;
- hash chain.

---


# Historical Integrity

Debe mantenerse:

```text
Historical Audit Fact

≠

Mutable Operational Data
```

sin imponer una tecnología concreta para garantizar dicha propiedad.

---


# Data Retention

La versión 1.0 no define:

- período de retención;
- vencimiento;
- borrado automático;
- archivado;
- anonimización;
- redacción.

---


# Security no Define Retention

Debe mantenerse:

```text
Security Concern

≠

Automatic Retention Policy
```

---


# Deletion

El Security Model no introduce:

```text
DeleteAudit
```

ni:

```text
AuditDeleted
```

---


# Redaction

La versión 1.0 no define:

```text
RedactAudit

AuditRedacted
```

---


# Anonymization

La versión 1.0 no define:

```text
AnonymizeAudit

AuditAnonymized
```

---


# Security y Repository.delete()

La existencia conceptual de:

```text
Repository.delete()
```

no constituye permiso de dominio para eliminar Audit.

Cualquier utilización requiere una política explícita aplicable.

---


# Read Model Security

Las vistas deben aplicar:

- minimización;
- autorización;
- separación entre usuarios;
- exposición únicamente de campos necesarios.

---


# Cross-Aggregate Read Models

Un Read Model compuesto puede combinar información de múltiples
contextos.

Esto no concede a un consumidor permisos sobre todos los Aggregates
representados.

---


# Projection Security

La proyección no debe ampliar automáticamente la visibilidad del dato.

Debe mantenerse:

```text
Projected

≠

Universally Visible
```

---


# Cache Security

Una cache no cambia las reglas de acceso.

Debe mantenerse:

```text
Cached

≠

Public
```

---


# Replica Security

Una réplica técnica no modifica las Permissions aplicables.

---


# Backup Security

Backup y restore pertenecen a Infrastructure.

No introducen reglas nuevas dentro del Aggregate.

---


# Performance y Security

Ninguna optimización puede omitir controles de seguridad aplicables.

Debe mantenerse:

```text
Performance

≠

Security Bypass
```

---


# Cache de Authorization

Una cache técnica de decisiones de autorización no redefine:

```text
Permission Semantics
```

---


# Rate Limiting

Rate Limiting puede existir como protección técnica.

No constituye:

- AuditStatus;
- Invariant;
- Domain Event.

---


# Throttling

Throttling permanece fuera del Domain Model.

---


# Timeout

Un timeout de seguridad o infraestructura no modifica:

```text
AuditStatus

Audit.Version
```

---


# Retry

Un retry técnico de autenticación, autorización, persistencia o
integración no crea:

```text
RetryAudit
```

ni:

```text
AuditRetried
```

---


# Queue

Estados técnicos:

```text
Queued

Processing

Retrying

DeadLettered
```

no forman parte del Security Model del Aggregate.

---


# Security Tests Conceptuales

Debe verificarse como mínimo:

```text
unauthorized RecordAudit rejected

no Audit on authorization denial

no AuditRecorded on authorization denial

authorized operation still validates invariants

no direct AuditId mutation

no direct Version mutation

no direct State mutation

no credentials stored

no secrets stored

no fabricated ActorId

no fabricated CorrelationId

no fabricated CausationId

read permission separated from write permission

read models expose minimum necessary data

integration events expose minimum necessary data

external consumers cannot mutate Audit

infrastructure access does not bypass domain

FIWARE authorization does not automatically grant Audit permission

municipal authorization does not automatically grant Audit permission
```

---


# Security Test de Historical Integrity

Debe verificarse:

```text
authorized actor cannot rewrite historical Audit

later Source Fact does not modify previous Audit

security policy change does not modify historical Audit

integration consumer cannot mutate historical Audit
```

---


# Security Test de Credenciales

Debe verificarse ausencia de:

```text
Password

AccessToken

RefreshToken

ApiKey

PrivateKey

Secret
```

en:

```text
Audit

AuditRecorded

Audit Read Models

AuditRecordedIntegrationEvent
```

---


# Security Test de Permissions

Debe verificarse:

```text
Read Permission

≠

Write Permission
```

y:

```text
Audit Permission

≠

Permission on Source Aggregate
```

---


# Security Test de Boundary

Debe verificarse que Security no incorpore:

```text
Citizen

Role

Organization

Source Aggregate

External Identity Provider
```

dentro de Audit por conveniencia.

---


# Security Test de Integration

Debe verificarse:

```text
no credential leakage

no automatic full payload exposure

no mutation authority from integration event

consumer failure does not rollback Audit

publication retry does not modify Audit
```

---


# Security Test de Read Model

Debe verificarse:

```text
no unrestricted visibility

no automatic ActorId exposure

no credentials

no write authority

no Aggregate mutation from projection
```

---


# Evolución

Cualquier futura ampliación del Security Model que introduzca:

- nuevas capacidades;
- nuevos datos sensibles;
- nuevas reglas de exposición;
- nuevos eventos auditables;
- nuevas políticas de retención;
- nuevas políticas de anonimización;
- nuevas políticas de redacción;

requiere definición explícita.

---


# Regla de No Inferencia

Debe mantenerse:

```text
Security Requirement

≠

Permission to Invent Domain Behavior
```

Ninguna necesidad técnica de seguridad autoriza introducir nuevos
estados, Commands, Domain Events o Aggregates sin definición formal.

---


# Regla de Evolución de Permissions

Si en una futura versión aparece un nuevo Command, deberá revisarse:

```text
DOMAIN-012C-Commands.md

DOMAIN-012E-Invariants.md

DOMAIN-012F-Permissions.md

DOMAIN-012O-Security-Model.md
```

para definir explícitamente su autorización y seguridad.

---


# Regla de Evolución de Datos

Si una futura versión incorpora nueva información al Aggregate,
deberá evaluarse:

- necesidad;
- minimización;
- sensibilidad;
- visibilidad;
- Read Model exposure;
- Integration Event exposure;
- ownership.

---


# Reglas Fundamentales

El Security Model de Audit debe cumplir:

1. Authentication permanece fuera del Aggregate.
2. Authorization se resuelve antes del comportamiento de dominio.
3. Domain Validation continúa siendo obligatoria después de
   Authorization.
4. Deny by Default permanece aplicable.
5. Least Privilege permanece aplicable.
6. RecordAudit es el único Command oficial de escritura.
7. Una operación no autorizada no crea Audit.
8. Una operación no autorizada no produce AuditRecorded.
9. Security no introduce nuevos Commands.
10. Security no introduce nuevos estados.
11. Security no introduce nuevos Domain Events.
12. Security no modifica Lifecycle.
13. Security no modifica State Machine.
14. Security no modifica AuditId.
15. Security no modifica Version directamente.
16. Security no modifica CreatedAt.
17. Authorization no permite reescribir historia.
18. Data Minimization es obligatoria conceptualmente.
19. Source Payload no se copia automáticamente.
20. Información ausente no se fabrica.
21. Passwords no forman parte del Aggregate.
22. Access Tokens no forman parte del Aggregate.
23. Refresh Tokens no forman parte del Aggregate.
24. API Keys no forman parte del Aggregate.
25. Private Keys no forman parte del Aggregate.
26. Secrets no forman parte del Aggregate.
27. Security Claims no forman parte automáticamente del estado.
28. ActorId no representa Authorization.
29. Source Actor y Command Requester pueden ser identidades distintas.
30. Conocer AuditId no concede acceso.
31. CorrelationId no concede Permission.
32. CausationId no concede Permission.
33. SourceEventId no concede Permission.
34. External References no transfieren ownership.
35. Security no amplía el Consistency Boundary.
36. Audit Permission no concede autoridad sobre otros Aggregates.
37. Organization permanece fuera del Security Boundary de Audit.
38. Citizen permanece fuera del Security Boundary de Audit.
39. Membership permanece fuera del Security Boundary de Audit.
40. Role permanece fuera del Security Boundary de Audit.
41. Territory permanece fuera del Security Boundary de Audit.
42. Assembly permanece fuera del Security Boundary de Audit.
43. Proposal permanece fuera del Security Boundary de Audit.
44. Participation permanece fuera del Security Boundary de Audit.
45. Voting permanece fuera del Security Boundary de Audit.
46. Document permanece fuera del Security Boundary de Audit.
47. Notification permanece fuera del Security Boundary de Audit.
48. Integration permanece fuera del Security Boundary de Audit.
49. Read Permission y Write Permission permanecen separadas.
50. Audit no es información pública automáticamente.
51. Read Models aplican minimización.
52. ActorId no se expone automáticamente.
53. Integration Events aplican minimización.
54. Integration Events no contienen credenciales.
55. Integration Event no concede Authorization.
56. External Consumers no modifican Audit directamente.
57. FIWARE Authentication no concede automáticamente Audit Permission.
58. Credenciales FIWARE permanecen fuera de Audit.
59. Authorization municipal no concede automáticamente Audit
    Permission.
60. Anti-Corruption Layer traduce modelos externos cuando
    corresponda.
61. RBAC es compatible sin imponer Roles internos.
62. ABAC es compatible sin imponer atributos internos obligatorios.
63. Delegación no está definida en versión 1.0.
64. Impersonation no está definida en versión 1.0.
65. AuditRecorded no contiene credenciales.
66. Consumir AuditRecorded no concede autoridad.
67. EventId no representa Permission.
68. Domain Events mantienen significado histórico.
69. Authorization no permite evitar Optimistic Concurrency.
70. ConcurrencyConflict no puede ignorarse por privilegio.
71. Repository no decide Authorization.
72. Acceso a Repository no equivale a Domain Permission.
73. Acceso a Infrastructure no equivale a Domain Authority.
74. Acceso directo a base de datos no evita Aggregate Root.
75. Publicar directamente en broker no equivale a ejecutar Command.
76. Acceso técnico a API no garantiza autorización.
77. Confidentiality limita exposición a consumidores autorizados.
78. Integrity protege contra modificaciones fuera del Aggregate.
79. Fallos técnicos de Security no cambian AuditStatus.
80. AuthenticationFailed no crea Audit automáticamente.
81. AuthorizationDenied no crea Audit automáticamente.
82. Eventos de seguridad no son automáticamente Audit.
83. No existe auditoría recursiva automática.
84. Security Logs permanecen fuera de Audit.
85. Security Metrics permanecen fuera de Audit.
86. Encryption es compatible pero no impuesta.
87. El dominio no define algoritmos criptográficos.
88. Hashing no es obligatorio en versión 1.0.
89. Digital Signature no es obligatoria en versión 1.0.
90. Tamper Resistance no selecciona una tecnología concreta.
91. Historical Integrity debe preservarse.
92. Security no define Retention.
93. Security no introduce DeleteAudit.
94. Security no introduce RedactAudit.
95. Security no introduce AnonymizeAudit.
96. Repository.delete() no representa permiso de dominio.
97. Projection no amplía automáticamente visibilidad.
98. Cache no cambia Permissions.
99. Performance no puede evitar Security.
100. Nuevas necesidades de Security no crean arquitectura de dominio
     automáticamente.

---

# Restricciones

No está permitido:

- autenticar usuarios dentro de Audit;
- validar passwords dentro del Aggregate;
- validar tokens dentro del Aggregate;
- almacenar credenciales;
- almacenar secrets;
- tratar ActorId como Permission;
- tratar CorrelationId como Permission;
- tratar CausationId como Permission;
- tratar SourceEventId como Permission;
- asumir acceso por conocer AuditId;
- permitir RecordAudit sin Authorization aplicable;
- permitir que Authorization evite Invariants;
- permitir que Authorization evite State Machine;
- permitir que Authorization evite Versioning;
- modificar AuditId por privilegio;
- modificar Version por privilegio;
- modificar CreatedAt por privilegio;
- reescribir hechos históricos por privilegio;
- copiar Source Payload completo automáticamente;
- embebir Source Aggregate completo;
- exponer ActorId automáticamente en todas las vistas;
- exponer credenciales en Domain Events;
- exponer credenciales en Integration Events;
- exponer credenciales en Read Models;
- conceder autoridad de escritura por recibir un evento;
- conceder Audit Permission automáticamente desde FIWARE;
- conceder Audit Permission automáticamente desde sistemas
  municipales;
- utilizar RBAC o ABAC para introducir estado de dominio no definido;
- utilizar Infrastructure Access para evitar Aggregate Root;
- utilizar acceso directo a base de datos como Domain Authority;
- convertir Security Failure en AuditStatus;
- crear Audit automáticamente por AuthenticationFailure;
- crear Audit automáticamente por AuthorizationDenied;
- imponer cifrado, hashing, firma o blockchain como regla del dominio
  sin decisión explícita;
- inferir Retention, Redaction o Anonymization;
- introducir DeleteAudit por razones de Security;
- ampliar el Consistency Boundary para resolver seguridad;
- sacrificar minimización por conveniencia técnica;
- sacrificar Security por Performance.

---

# Compatibilidad Arquitectónica

El Security Model de Audit es compatible con:

- Domain-Driven Design;
- Aggregate Pattern;
- Clean Architecture;
- Hexagonal Architecture;
- SOLID;
- CQRS;
- Event-Driven Architecture;
- Event Sourcing Compatible;
- Optimistic Concurrency Control;
- Transactional Outbox;
- Least Privilege;
- Deny by Default;
- RBAC;
- ABAC;
- Data Minimization;
- Separation of Concerns;
- Anti-Corruption Layer;
- High Cohesion;
- Low Coupling.

Estas compatibilidades no imponen tecnologías, algoritmos ni
proveedores concretos.

---

# Definición de Éxito

El Security Model del Aggregate **Audit** protege acceso, exposición
e integridad conceptual sin introducir comportamiento ajeno al dominio.

El modelo garantiza que:

```text
Authentication

≠

Authorization

≠

Domain Validation
```

y que:

- Authentication permanece fuera del Aggregate;
- Authorization precede al comportamiento;
- RecordAudit requiere Permission aplicable;
- Deny by Default y Least Privilege permanecen vigentes;
- una operación autorizada continúa sujeta a State Machine,
  Invariants y Versioning;
- Security no introduce nuevos estados, Commands o Domain Events;
- AuditId, Version y CreatedAt permanecen protegidos;
- ningún privilegio permite reescribir historia;
- Data Minimization limita la información almacenada;
- Source Payload no se copia automáticamente;
- información ausente no se fabrica;
- credenciales, tokens, claves y secrets permanecen fuera de Audit;
- ActorId conserva significado de trazabilidad y no de Permission;
- CorrelationId, CausationId y SourceEventId no conceden autoridad;
- referencias externas no transfieren ownership;
- otros Aggregates mantienen sus propias políticas de seguridad;
- Read Permission y Write Permission permanecen separadas;
- datos históricos no son públicos automáticamente;
- Read Models exponen solamente información necesaria;
- Integration Events exponen solamente información necesaria;
- consumidores externos no obtienen autoridad directa sobre Audit;
- FIWARE y sistemas municipales mantienen sus propios mecanismos de
  identidad y autorización fuera del Aggregate;
- RBAC y ABAC permanecen compatibles sin quedar impuestos;
- Domain Events no contienen credenciales ni conceden autoridad;
- Optimistic Concurrency no puede evitarse mediante privilegios;
- Repository e Infrastructure no deciden Permissions;
- acceso técnico no equivale a autoridad de dominio;
- fallos de Security no crean estados de Audit;
- eventos de seguridad no se convierten automáticamente en Audit;
- no existe recursividad automática;
- encryption, hashing, firmas y mecanismos de tamper resistance
  permanecen decisiones arquitectónicas externas mientras no se
  definan formalmente;
- Retention, Redaction, Anonymization y Deletion no se infieren desde
  Security;
- Performance no puede utilizarse para debilitar Security;
- cualquier evolución futura debe preservar minimización,
  confidencialidad, integridad, autorización y separación de
  responsabilidades.

De esta forma, `DOMAIN-012O-Security-Model.md` establece formalmente
el Security Model del Aggregate **Audit** conforme al patrón
consolidado de AURA Core.