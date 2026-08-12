# DOMAIN-007O — Proposal Security Model

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
- CORE-003-Shared-Kernel.md
- CORE-004-Ubiquitous-Language.md
- CORE-005-Domain-Events.md
- CORE-006-Domain-Invariants.md
- CORE-007-Strategic-Design.md
- CORE-008-Aggregate-Design-Rules.md
- CORE-011-Repository-Contracts.md

---

# Objetivo

Definir el modelo conceptual de seguridad del Aggregate
**Proposal**.

Este documento establece las reglas que protegen la identidad,
estado, comportamiento, información, trazabilidad y límites de
consistencia de Proposal frente a operaciones no autorizadas,
modificaciones inválidas, exposición indebida de información y
violaciones de las reglas del dominio.

El Security Model forma parte de la definición conceptual del
Aggregate.

No constituye una especificación de infraestructura de seguridad.

Proposal protege sus propias invariantes y exige que toda
intención de modificación haya superado los controles de
autorización correspondientes antes de ejecutar comportamiento
del dominio.

---

# Propósito

El propósito del Security Model es establecer una separación
explícita entre:

```text
Authentication

Authorization

Domain Validation

Infrastructure Security
```

Cada concepto posee una responsabilidad diferente.

Proposal no debe asumir responsabilidades pertenecientes a
autenticación, gestión de credenciales, transporte seguro,
gestión de sesiones o infraestructura.

Al mismo tiempo, Proposal nunca debe confiar en que una operación
es válida únicamente porque el actor haya sido autenticado o
autorizado.

Toda operación debe preservar también:

- invariantes;
- State Machine;
- Lifecycle;
- Version;
- consistencia;
- límites del Aggregate;
- reglas de modificación;
- reglas de trazabilidad.

---

# Principios

El modelo de seguridad de Proposal sigue los siguientes
principios:

- autenticación y autorización son responsabilidades separadas;
- autenticación no implica autorización;
- autorización no sustituye las invariantes;
- las invariantes no sustituyen la autorización;
- Proposal no almacena credenciales;
- Proposal no administra sesiones;
- Proposal no valida tokens técnicos;
- Proposal no conoce protocolos de autenticación;
- todo Command identifica al actor cuando corresponda;
- toda modificación debe respetar permisos;
- toda modificación debe respetar invariantes;
- toda modificación debe respetar Version;
- toda transición debe respetar la State Machine;
- los datos expuestos deben limitarse al propósito autorizado;
- los Read Models deben respetar políticas de acceso;
- los Integration Events deben exponer únicamente información
  necesaria;
- los Domain Events no deben utilizarse para evadir controles;
- la infraestructura de seguridad permanece fuera del Aggregate;
- ningún mecanismo técnico puede redefinir las reglas del dominio.

---

# Modelo Conceptual de Seguridad

```text
Actor

  │

  ▼

Authentication

  │

  ▼

Authorization

  │

  ▼

Command

  │

  ▼

Proposal Aggregate

  │

  ├── Lifecycle
  │
  ├── State Machine
  │
  ├── Invariants
  │
  ├── Version
  │
  └── Consistency Boundary

  │

  ▼

Domain Event
```

La autenticación establece quién es el actor.

La autorización establece qué operación puede intentar.

Proposal determina si dicha operación es válida dentro del
dominio.

---

# Regla Fundamental

La regla fundamental del Security Model es:

```text
Authenticated

≠

Authorized
```

y:

```text
Authorized

≠

Domain Valid
```

Una operación válida requiere conceptualmente:

```text
Authenticated Actor

+

Authorized Intent

+

Valid Domain State

+

Valid Invariants

+

Valid Version

=

Accepted Domain Operation
```

---

# Separación de Responsabilidades

El modelo distingue cuatro responsabilidades principales.

```text
Authentication
```

determina la identidad del actor.

```text
Authorization
```

determina si el actor puede intentar ejecutar una operación.

```text
Proposal
```

determina si la operación es válida según el dominio.

```text
Infrastructure Security
```

protege los mecanismos técnicos utilizados para ejecutar y
transportar las operaciones.

Estas responsabilidades no deben fusionarse.

---

# Autenticación

Proposal no administra autenticación.

No es responsabilidad del Aggregate:

- autenticar usuarios;
- validar contraseñas;
- emitir credenciales;
- validar JWT;
- administrar OAuth;
- administrar sesiones;
- administrar MFA;
- almacenar secretos;
- gestionar proveedores de identidad;
- renovar tokens;
- revocar tokens;
- implementar Single Sign-On.

La autenticación debe resolverse antes de que una intención
autorizada alcance el comportamiento del Aggregate.

---

# Identidad del Actor

Cuando una operación requiera conocer al actor responsable, la
identidad se representa mediante:

```text
ActorId
```

ActorId representa la identidad utilizada para trazabilidad y
autorización.

ActorId no representa:

- contraseña;
- token;
- JWT;
- sesión;
- credencial;
- secreto;
- clave privada.

El Aggregate puede utilizar una referencia de actor cuando dicha
información forme parte de una regla de dominio o de
trazabilidad.

---

# ActorId y CitizenId

ActorId y CitizenId no deben considerarse automáticamente el mismo
concepto.

```text
ActorId
```

representa la identidad que ejecuta una intención dentro del
sistema.

```text
CitizenId
```

representa la identidad del Aggregate Citizen dentro del dominio.

Una implementación puede relacionar ambos conceptos cuando
corresponda, pero Proposal no debe asumir dicha equivalencia como
regla implícita.

---

# ActorId y MembershipId

Una autorización organizacional puede estar relacionada con una:

```text
MembershipId
```

cuando el actor actúa dentro del contexto de una Organization.

La Membership representa la relación organizacional.

Proposal no administra Membership.

Proposal no modifica Membership.

Proposal puede recibir las referencias necesarias para evaluar las
reglas conceptuales que le correspondan.

---

# ActorId y Role

Los Roles pertenecen al modelo organizacional y de autorización
correspondiente.

Proposal no administra Roles.

La existencia de un Role puede contribuir a determinar si un actor
posee autorización para ejecutar un Command.

Sin embargo:

```text
Role

≠

Permission
```

y:

```text
Role

≠

Domain Invariant
```

Las responsabilidades permanecen separadas.

---

# Autorización

La autorización determina si un actor puede intentar ejecutar una
operación sobre Proposal.

Ejemplos conceptuales:

```text
CreateProposal

SubmitProposal

StartProposalReview

AcceptProposal

RejectProposal

WithdrawProposal

ArchiveProposal

RenameProposal

ChangeProposalDescription
```

La autorización debe evaluarse conforme al modelo definido en:

```text
DOMAIN-007F-Permissions.md
```

---

# Regla de Autorización

Toda operación protegida debe cumplir:

```text
Actor

+

Requested Operation

+

Authorization Context

↓

Permission Evaluation
```

Si el actor no posee autorización:

```text
Reject
```

El Aggregate no debe modificarse.

No debe publicarse un Domain Event que represente una modificación
que no ocurrió.

---

# Autorización y Estado

Un actor puede poseer permiso para ejecutar una categoría de
operación y aun así no poder ejecutarla debido al estado actual
del Aggregate.

Ejemplo conceptual:

```text
Actor can AcceptProposal
```

pero:

```text
ProposalStatus = Draft
```

Si la State Machine no permite aceptar una Proposal desde Draft,
la operación debe rechazarse.

Por lo tanto:

```text
Permission Granted

≠

Transition Allowed
```

---

# Autorización e Invariantes

La autorización nunca permite violar invariantes.

Debe mantenerse:

```text
Authorized Actor

+

Invariant Violation

=

Rejected Operation
```

Un actor con privilegios elevados continúa sujeto a las
invariantes oficiales del Aggregate.

---

# Autorización y Version

La autorización tampoco permite ignorar conflictos de
concurrencia.

Debe mantenerse:

```text
Authorized Actor

+

Incorrect ExpectedVersion

=

Concurrency Conflict
```

La autorización no convierte una versión obsoleta en una
modificación válida.

---

# Modelo de Permisos

Las capacidades específicas de autorización se encuentran
definidas en:

```text
DOMAIN-007F-Permissions.md
```

El Security Model no redefine dichas capacidades.

Su responsabilidad es establecer cómo los permisos se relacionan
con:

- Commands;
- estado;
- invariantes;
- identidad del actor;
- trazabilidad;
- exposición de información;
- límites del Aggregate.

---

# Commands

Los Commands constituyen intenciones de modificación y deben
llegar al dominio con el contexto necesario para identificar la
operación solicitada.

La estructura conceptual definida para los Commands incluye:

```text
CommandId

ProposalId

OrganizationId

ActorId

Timestamp

CorrelationId

CausationId
```

junto con los datos específicos de cada operación.

Los Commands no deben transportar credenciales técnicas.

---

# Seguridad de Commands

Un Command no debe contener:

- contraseñas;
- secretos;
- claves privadas;
- tokens de acceso;
- refresh tokens;
- cookies de sesión;
- credenciales OAuth;
- información técnica innecesaria de autenticación.

La capa correspondiente debe resolver la autenticación antes de
construir la intención de dominio.

---

# CommandId

Cada Command posee:

```text
CommandId
```

CommandId permite identificar una intención específica.

Su presencia facilita:

- trazabilidad;
- auditoría;
- correlación;
- diagnóstico;
- prevención de procesamiento ambiguo.

CommandId no constituye una credencial.

Conocer un CommandId no otorga autorización para ejecutar un
Command.

---

# CorrelationId

CorrelationId permite relacionar operaciones pertenecientes a un
mismo flujo lógico.

Ejemplo:

```text
User Intent

↓

Command

↓

Domain Event

↓

Integration Event
```

puede mantener:

```text
CorrelationId
```

La correlación facilita trazabilidad.

No concede permisos.

---

# CausationId

CausationId permite identificar la causa inmediata de una
operación o evento cuando corresponda.

Debe mantenerse:

```text
CausationId

≠

Authorization Proof
```

La causalidad permite trazabilidad.

No sustituye autenticación ni autorización.

---

# Timestamp

Timestamp representa información temporal asociada a la intención
o hecho correspondiente.

No debe utilizarse por sí solo como mecanismo de seguridad.

La presencia de un timestamp no demuestra:

- identidad;
- autenticidad;
- autorización;
- integridad criptográfica.

Estas responsabilidades pertenecen a las capas correspondientes.

---

# Protección del Aggregate Root

Toda modificación del estado interno debe realizarse mediante:

```text
Proposal
```

como Aggregate Root.

No debe existir acceso externo que permita modificar directamente:

```text
ProposalId

OrganizationId

Status

Version

Lifecycle State
```

ni cualquier otra propiedad protegida por el Aggregate.

---

# Regla de No Bypass

No está permitido:

```text
External Caller

↓

Direct State Mutation
```

Debe mantenerse:

```text
Authorized Command

↓

Proposal Behavior

↓

Invariant Validation

↓

State Change
```

La modificación directa representa una violación del límite de
seguridad y consistencia del Aggregate.

---

# Protección de Identidad

ProposalId es inmutable.

Ningún permiso permite modificar:

```text
ProposalId
```

Debe mantenerse:

```text
ProposalId at Creation

=

ProposalId throughout Lifecycle
```

La identidad no puede sustituirse mediante una operación
administrativa.

---

# Protección de OrganizationId

OrganizationId identifica la Organization propietaria de la
Proposal.

Cuando el modelo oficial establece su inmutabilidad, ningún actor
puede modificarlo mediante una operación ordinaria.

Debe mantenerse:

```text
OrganizationId

Immutable
```

La autorización administrativa no permite romper esta regla.

---

# Protección de Version

Version no puede modificarse directamente.

Debe cambiar únicamente como consecuencia de una modificación
válida del Aggregate.

No está permitido:

```text
SetVersion(100)
```

como operación de dominio.

Debe mantenerse:

```text
Valid Change

↓

Version Increment
```

---

# Protección de Status

ProposalStatus no puede modificarse directamente.

No está permitido:

```text
SetStatus(Accepted)
```

La modificación debe ocurrir mediante comportamiento explícito.

Ejemplo:

```text
AcceptProposal

↓

Validate Permission

↓

Validate State

↓

Validate Invariants

↓

Apply Transition

↓

ProposalAccepted
```

---

# Protección del Lifecycle

El Lifecycle definido en:

```text
DOMAIN-007A-Lifecycle.md
```

constituye una regla de seguridad del estado del Aggregate.

Ningún actor puede utilizar permisos elevados para crear
transiciones inexistentes.

Debe mantenerse:

```text
Authorization

does not override

Lifecycle
```

---

# Protección de la State Machine

La State Machine definida en:

```text
DOMAIN-007B-State-Machine.md
```

controla las transiciones permitidas.

No debe existir una operación técnica genérica como:

```text
ForceStatus
```

que permita omitir la State Machine.

Toda transición debe ejecutarse mediante comportamiento válido del
Aggregate.

---

# Protección de Invariantes

Las invariantes definidas en:

```text
DOMAIN-007E-Invariants.md
```

constituyen reglas obligatorias.

No existen excepciones implícitas basadas en:

- privilegios administrativos;
- acceso directo a base de datos;
- procesos internos;
- integraciones externas;
- scripts;
- operaciones masivas;
- sincronizaciones;
- migraciones operativas.

Cualquier modificación conceptual debe preservar las invariantes.

---

# Defensa en Profundidad

La seguridad del dominio no depende de un único control.

Conceptualmente:

```text
Authentication

↓

Authorization

↓

Command Validation

↓

Aggregate State Validation

↓

Invariant Validation

↓

Version Validation

↓

Persistence Validation

↓

Event Publication
```

Cada nivel protege una responsabilidad distinta.

La existencia de un control anterior no elimina los posteriores.

---

# Security Boundary

El límite de seguridad del Aggregate coincide con la necesidad de
proteger su consistencia interna.

Dentro del límite se protegen:

```text
ProposalId

OrganizationId

ProposalType

Title

Description

Purpose

Status

Lifecycle

Version

Internal Domain State
```

según el modelo oficial del Aggregate.

Los sistemas externos no pueden modificar estos elementos sin
pasar por comportamiento válido de Proposal.

---

# Consistency Boundary y Seguridad

El límite de consistencia definido en:

```text
DOMAIN-007J-Consistency-Boundary.md
```

también impide que una operación sobre Proposal modifique
directamente otros Aggregates.

Proposal no puede modificar:

```text
Organization

Citizen

Membership

Role

Territory

Assembly

Participation

Voting

Document

Notification

Audit

Integration
```

Esta separación reduce el alcance de una operación y protege los
límites de responsabilidad.

---

# Referencias Externas

Las referencias a otros Aggregates se mantienen mediante
identificadores.

Ejemplos:

```text
OrganizationId

CitizenId

MembershipId

TerritoryId

AssemblyId

ParticipationId

VotingId

DocumentId
```

Poseer un identificador externo no concede permiso para acceder ni
modificar el Aggregate correspondiente.

Debe mantenerse:

```text
Reference

≠

Authorization
```

---

# Organization Boundary

Proposal pertenece al contexto de una Organization.

Las operaciones deben respetar el contexto organizacional
correspondiente.

Una autorización válida dentro de una Organization no debe
interpretarse automáticamente como autorización sobre Proposal
pertenecientes a otra Organization.

Debe mantenerse:

```text
Organization A Authorization

≠

Organization B Authorization
```

salvo que exista una capacidad explícita definida por el modelo de
autorización.

---

# Aislamiento Organizacional

Cuando AURA opere con múltiples Organizations, las consultas y
operaciones deben preservar el aislamiento conceptual entre ellas.

Una operación dirigida a:

```text
OrganizationId = A
```

no debe modificar una Proposal cuyo:

```text
OrganizationId = B
```

La identidad organizacional forma parte del contexto de seguridad.

---

# Validación de Contexto Organizacional

Cuando un Command contenga:

```text
OrganizationId
```

debe existir coherencia con la Organization propietaria de la
Proposal.

Debe evitarse:

```text
Command.OrganizationId = A

Proposal.OrganizationId = B
```

seguido de una modificación aceptada.

La inconsistencia debe producir rechazo.

---

# Proponente

Cuando Proposal mantenga una referencia al proponente, dicha
referencia forma parte del contexto del dominio.

La identidad del proponente puede participar en reglas como:

- modificación de borradores;
- presentación de la Proposal;
- retiro de la Proposal;
- consulta de información propia.

Las capacidades concretas permanecen definidas en:

```text
DOMAIN-007F-Permissions.md
```

---

# Propiedad y Autorización

Ser proponente de una Proposal no implica automáticamente
autorización ilimitada.

Debe mantenerse:

```text
Proposer

≠

Unlimited Owner
```

El proponente continúa sujeto a:

- Lifecycle;
- State Machine;
- Permissions;
- Invariants;
- Version;
- reglas organizacionales.

---

# Revisión

Las operaciones de revisión deben respetar las capacidades
definidas para los actores autorizados.

Un proponente no debe obtener automáticamente capacidades de
revisión por ser autor de la Proposal.

Debe mantenerse separación entre:

```text
Proposal Creation
```

y:

```text
Proposal Review
```

cuando el modelo de permisos así lo establece.

---

# Aceptación

La aceptación de una Proposal constituye una operación protegida.

Conceptualmente debe requerir:

```text
Authorized Actor

+

Valid Proposal State

+

Satisfied Invariants

+

Valid Version
```

La aceptación no puede producirse mediante modificación directa
del Status.

---

# Rechazo

El rechazo de una Proposal constituye una operación protegida.

Debe respetar:

- autorización;
- estado permitido;
- invariantes;
- trazabilidad;
- Version.

El rechazo debe producir el Domain Event correspondiente únicamente
después de una transición válida.

---

# Retiro

El retiro de una Proposal debe respetar las reglas establecidas
para:

```text
WithdrawProposal
```

Un actor no puede retirar arbitrariamente cualquier Proposal por
poseer acceso de lectura.

Debe mantenerse:

```text
Read Permission

≠

Withdraw Permission
```

---

# Archivado

ArchiveProposal constituye una operación protegida.

Archivar no equivale a eliminar físicamente información.

El archivado debe respetar:

- permisos;
- estado;
- invariantes;
- Version;
- trazabilidad.

Una Proposal archivada queda sujeta a las restricciones definidas
por el Aggregate.

---

# Eliminación

La eliminación física no debe utilizarse como mecanismo ordinario
para evadir:

- Lifecycle;
- Audit;
- trazabilidad;
- archivado;
- invariantes.

Cuando el modelo oficial utilice archivado lógico, debe respetarse
dicha semántica.

La infraestructura no debe interpretar:

```text
Delete Row
```

como equivalente automático de:

```text
ArchiveProposal
```

---

# Seguridad del Repository

El contrato del Repository definido en:

```text
DOMAIN-007G-Repository-Contract.md
```

debe preservar el Aggregate como unidad.

El Repository no debe proporcionar operaciones que permitan
evadir comportamiento de dominio.

Ejemplos conceptualmente inválidos:

```text
repository.set_status()

repository.set_version()

repository.change_organization_id()

repository.force_accept()
```

El Repository persiste estado válido.

No crea validez de dominio.

---

# Repository y Autorización

El Repository no constituye el componente responsable de decidir
los permisos del actor.

Debe mantenerse:

```text
Repository

=

Persistence Contract
```

No:

```text
Repository

=

Authorization Engine
```

La separación evita mezclar persistencia con políticas de acceso.

---

# Persistencia

La tecnología de persistencia no define la seguridad conceptual
del Aggregate.

Proposal no depende de:

- PostgreSQL;
- MongoDB;
- MySQL;
- Redis;
- Elasticsearch;
- ORM;
- drivers;
- procedimientos almacenados.

Las restricciones de dominio deben permanecer válidas
independientemente de la tecnología utilizada.

---

# Escritura Directa en Persistencia

Una escritura directa sobre almacenamiento que modifique el estado
de Proposal sin pasar por comportamiento válido constituye una
violación del modelo conceptual.

No debe ocurrir:

```text
Database Update

↓

ProposalStatus = Accepted
```

sin ejecutar las reglas correspondientes.

La capacidad técnica de realizar una modificación no implica que
la modificación sea válida dentro del dominio.

---

# Concurrencia

Proposal utiliza concurrencia optimista mediante:

```text
Version
```

La protección contra lost updates forma parte del modelo de
consistencia y seguridad del estado.

La especificación completa se encuentra en:

```text
DOMAIN-007I-Versioning.md
```

---

# Lost Updates

No está permitido aceptar silenciosamente una modificación basada
en una versión obsoleta.

Ejemplo:

```text
Stored Version = 8

Command ExpectedVersion = 7
```

La operación debe producir:

```text
Concurrency Conflict
```

cuando corresponda.

No debe sobrescribirse la versión 8 con información derivada de la
versión 7.

---

# Reintentos

Los reintentos técnicos no conceden autorización adicional.

Debe mantenerse:

```text
Rejected Unauthorized Command

↓

Retry

↓

Still Unauthorized
```

mientras no cambie legítimamente el contexto de autorización.

Un reintento tampoco debe ignorar Version.

---

# Domain Events

Los Domain Events representan hechos ocurridos dentro del
Aggregate.

Ejemplos:

```text
ProposalCreated

ProposalSubmitted

ProposalReviewStarted

ProposalAccepted

ProposalRejected

ProposalWithdrawn

ProposalArchived
```

La definición oficial se encuentra en:

```text
DOMAIN-007D-Domain-Events.md
```

---

# Seguridad de Domain Events

Un Domain Event debe publicarse únicamente como consecuencia de
una operación válida.

No debe utilizarse:

```text
Publish ProposalAccepted
```

como mecanismo para simular una transición que no fue ejecutada por
el Aggregate.

Debe mantenerse:

```text
Valid Domain Behavior

↓

State Change

↓

Domain Event
```

---

# Información en Domain Events

Los Domain Events deben contener la información necesaria para
representar el hecho ocurrido.

No deben utilizarse como mecanismo indiscriminado para exponer:

- datos personales innecesarios;
- credenciales;
- secretos;
- tokens;
- información privada no relacionada;
- datos técnicos internos.

La información incluida debe responder al significado del evento.

---

# Event Replay

Cuando se utilice Event Sourcing, el replay de eventos representa
reconstrucción de estado.

No constituye una nueva operación autorizada.

Debe mantenerse:

```text
Replay

≠

New Command
```

Durante replay no deben ejecutarse nuevamente:

- autorizaciones de usuario como nuevas operaciones;
- Notifications externas;
- Integration Events como hechos nuevos;
- llamadas externas;
- efectos secundarios de negocio.

---

# Manipulación del Historial

El historial de Domain Events no debe modificarse arbitrariamente
para alterar el estado reconstruido del Aggregate.

Cuando Event Sourcing forme parte de una implementación, la
integridad del historial debe preservarse conforme a las reglas de
persistencia y versionado.

La infraestructura concreta utilizada para garantizar dicha
integridad permanece fuera del Aggregate.

---

# Integration Events

Los Integration Events representan contratos destinados a otros
Bounded Contexts o sistemas externos.

La definición oficial se encuentra en:

```text
DOMAIN-007K-Integration-Events.md
```

Los Integration Events no deben exponer automáticamente todo el
estado de Proposal.

---

# Minimización de Información

Todo contrato externo debe aplicar el principio:

```text
Minimum Necessary Information
```

La información publicada debe limitarse a la necesaria para el
propósito del contrato.

No debe utilizarse:

```text
Complete Proposal Aggregate
```

como Payload predeterminado de integración.

---

# Información Sensible

La información que pueda requerir protección adicional no debe
exponerse simplemente porque exista dentro de una representación
interna o proyección.

La exposición debe considerar:

- propósito;
- consumidor;
- autorización;
- contexto organizacional;
- política de privacidad;
- contrato de integración.

---

# Integration Boundary

Los sistemas externos no adquieren capacidad de modificar
Proposal directamente por consumir Integration Events.

Debe mantenerse:

```text
Integration Event Consumer

≠

Proposal Writer
```

Si un sistema externo necesita solicitar una modificación, debe
utilizar el contrato de entrada autorizado correspondiente.

---

# Integraciones Municipales

Proposal puede interoperar con plataformas municipales.

La integración no convierte al sistema municipal en parte del
Aggregate.

Debe mantenerse:

```text
Proposal

↓

Integration Contract

↓

Municipal Platform
```

El sistema externo no obtiene acceso directo al estado interno del
Aggregate.

---

# Integraciones Smart City

Proposal puede participar en ecosistemas Smart City mediante los
mecanismos de integración definidos por AURA.

La interoperabilidad no modifica:

- ProposalId;
- Lifecycle;
- State Machine;
- Invariants;
- Version;
- Permissions;
- Consistency Boundary.

La representación externa puede adaptarse sin alterar el dominio.

---

# FIWARE

Una integración con FIWARE pertenece a Infrastructure e
Integration.

Proposal no conoce directamente:

- Context Broker;
- NGSI-LD endpoints;
- HTTP;
- OAuth;
- Keyrock;
- PEP Proxy;
- tokens;
- credenciales FIWARE.

Debe mantenerse:

```text
Proposal Domain

↓

Integration Contract

↓

Adapter

↓

FIWARE
```

---

# Seguridad de Integraciones

Los mecanismos técnicos utilizados para proteger integraciones
pertenecen a Infrastructure.

Pueden existir mecanismos como:

```text
Authentication

Authorization

Transport Security

Credential Management

Message Integrity

Secret Management
```

pero estos no se incorporan como comportamiento interno de
Proposal.

---

# Read Models

Los Read Models definidos en:

```text
DOMAIN-007L-Read-Model.md
```

son representaciones derivadas.

No forman parte del Aggregate.

Su condición de solo lectura no significa que toda información
contenida en ellos deba ser visible para cualquier consumidor.

---

# Seguridad de Read Models

Cada Read Model debe exponer únicamente la información permitida
para el consumidor correspondiente.

Una proyección puede:

- excluir atributos;
- limitar campos;
- ocultar información;
- anonimizar información cuando corresponda;
- utilizar vistas específicas por propósito.

La autorización de lectura pertenece a la capa correspondiente.

---

# Read Permission

Poseer autorización para consultar una vista no concede permiso
para modificar Proposal.

Debe mantenerse:

```text
Read Permission

≠

Write Permission
```

Una operación de lectura tampoco debe modificar:

```text
Version

Status

UpdatedAt
```

como consecuencia de la consulta.

---

# Read Models y Fuente de Verdad

Una proyección no debe utilizarse para evadir las reglas de
escritura.

No debe ocurrir:

```text
Modify Read Model

↓

Assume Proposal Modified
```

La fuente conceptual de verdad del lado de escritura permanece en:

```text
Proposal Aggregate
```

---

# Datos Desnormalizados

Los Read Models pueden contener información desnormalizada.

La duplicación orientada a lectura no concede propiedad sobre los
datos originales.

Ejemplo:

```text
OrganizationName
```

dentro de una proyección de Proposal no convierte a Proposal en
propietario del estado de Organization.

---

# Caché

Una caché de lectura no constituye fuente de autorización ni de
verdad del Aggregate.

Debe mantenerse:

```text
Cache

≠

Authorization Source
```

y:

```text
Cache

≠

Write Source of Truth
```

Una copia obsoleta no debe permitir sobrescribir una versión más
reciente.

---

# Seguridad de Proyecciones

Una proyección reconstruida debe conservar las reglas de exposición
definidas para su propósito.

La reconstrucción no debe producir una vista más permisiva
simplemente por procesar información histórica.

Las reglas de lectura permanecen independientes del mecanismo de
reconstrucción.

---

# Auditoría

Las operaciones relevantes sobre Proposal deben proporcionar la
información necesaria para trazabilidad.

Conceptualmente pueden participar:

```text
CommandId

ProposalId

OrganizationId

ActorId

Timestamp

CorrelationId

CausationId

Version

Domain Event
```

La auditoría completa pertenece al contexto correspondiente.

---

# Seguridad de Auditoría

Los registros de auditoría no deben permitir modificar
retroactivamente el estado del Aggregate.

Debe mantenerse:

```text
Audit Record

≠

Proposal Command
```

La auditoría observa y registra hechos.

No sustituye el comportamiento de Proposal.

---

# Trazabilidad

Una modificación válida debe poder relacionarse conceptualmente
con:

```text
Actor

Intent

Aggregate

Version

Resulting Event
```

Esto permite reconstruir el contexto de una operación sin
incorporar credenciales dentro del dominio.

---

# No Repudio Conceptual

La trazabilidad debe permitir identificar qué actor fue asociado a
una intención cuando dicha información sea requerida por el
dominio.

Los mecanismos criptográficos específicos utilizados para
garantizar autenticidad o no repudio técnico pertenecen a
Infrastructure.

Proposal no implementa criptografía.

---

# Privacidad

Proposal debe mantener únicamente la información necesaria para su
responsabilidad de dominio.

No debe almacenar datos personales completos de Citizen cuando una
referencia sea suficiente.

Debe preferirse:

```text
CitizenId
```

sobre:

```text
Complete Citizen Profile
```

cuando el perfil no sea necesario para proteger una invariante del
Aggregate.

---

# Minimización de Datos

La minimización de datos reduce exposición y acoplamiento.

Proposal no debe copiar por conveniencia:

- dirección completa de Citizen;
- información de contacto completa;
- credenciales;
- historial completo de Membership;
- información privada de Organization;
- contenido completo de otros Aggregates.

Las necesidades de lectura pueden resolverse mediante proyecciones
autorizadas.

---

# Separación de Datos de Dominio y Credenciales

Debe mantenerse:

```text
Domain Data

≠

Authentication Data
```

Proposal puede mantener información necesaria para representar una
Proposal.

No debe convertirse en repositorio de identidad técnica.

---

# Secretos

Proposal nunca almacena:

```text
Passwords

API Keys

Private Keys

Client Secrets

Access Tokens

Refresh Tokens

Session Tokens

Encryption Keys
```

Estos elementos pertenecen a mecanismos técnicos externos al
Aggregate.

---

# OAuth

OAuth no forma parte del Aggregate Proposal.

Proposal no debe conocer:

- authorization codes;
- client credentials;
- access tokens;
- scopes técnicos;
- refresh tokens;
- endpoints OAuth.

Las capacidades de autorización del dominio deben permanecer
independientes del protocolo utilizado para transportar o
representar autorización técnica.

---

# JWT

JWT no forma parte del dominio.

El Aggregate no debe:

- decodificar JWT;
- validar firmas JWT;
- interpretar claims técnicos;
- almacenar JWT;
- renovar JWT.

La capa correspondiente puede transformar una identidad
autenticada y autorizada en el contexto requerido para ejecutar un
Command.

---

# PEP Proxy

Un PEP Proxy puede proteger técnicamente puntos de acceso.

No forma parte del Aggregate.

Debe mantenerse:

```text
PEP Authorization

≠

Proposal Invariants
```

Aunque una solicitud supere un PEP Proxy, Proposal continúa
obligado a validar su estado e invariantes.

---

# Keyrock

Un Identity Manager como Keyrock pertenece a Infrastructure o al
contexto de identidad correspondiente.

Proposal no depende de Keyrock.

Una futura sustitución del proveedor de identidad no debe requerir
modificar:

```text
Proposal Aggregate

Lifecycle

State Machine

Commands

Domain Events

Invariants
```

---

# Transporte

La seguridad del transporte pertenece a Infrastructure.

Conceptos como:

```text
TLS

HTTPS

Certificates

Network Encryption
```

no forman parte del estado de Proposal.

Su utilización técnica no debe introducir dependencias dentro del
Aggregate.

---

# Cifrado

El cifrado de datos en tránsito o reposo pertenece a
Infrastructure.

Proposal no define:

- algoritmos criptográficos;
- tamaños de clave;
- proveedores de claves;
- rotación de secretos;
- protocolos de cifrado.

Estas decisiones no modifican el significado conceptual del
Aggregate.

---

# Protección contra Manipulación Técnica

La infraestructura debe impedir modificaciones no autorizadas de
persistencia, mensajes y comunicaciones.

Sin embargo, el dominio no debe depender exclusivamente de dicha
protección.

Proposal continúa validando:

- identidad contextual;
- estado;
- invariantes;
- Version;
- transición;
- comportamiento.

---

# Entrada de Datos

Toda información utilizada para construir Value Objects o ejecutar
comportamiento debe respetar las reglas conceptuales
correspondientes.

Datos inválidos no deben incorporarse al Aggregate.

Debe mantenerse:

```text
External Input

↓

Validation

↓

Domain Value
```

No:

```text
External Input

↓

Direct Internal State
```

---

# Validación Sintáctica y Semántica

La validación puede existir en distintos niveles.

```text
Transport Validation
```

puede verificar formato técnico.

```text
Application Validation
```

puede verificar estructura de una solicitud.

```text
Domain Validation
```

protege reglas conceptuales e invariantes.

La existencia de validaciones externas no elimina la validación
del dominio.

---

# Value Objects

Los Value Objects deben proteger sus propias reglas de valor.

Un Value Object inválido no debe existir como estado válido del
Aggregate.

Esta propiedad contribuye a la seguridad del modelo al impedir que
información conceptualmente inválida ingrese al estado interno.

---

# Mass Assignment

La infraestructura no debe mapear indiscriminadamente todos los
campos externos hacia el estado interno de Proposal.

Debe evitarse conceptualmente:

```text
External Payload

↓

Automatic Aggregate Mutation
```

Debe mantenerse:

```text
External Payload

↓

Command

↓

Domain Behavior
```

---

# Campos Protegidos

Campos como:

```text
ProposalId

OrganizationId

Status

Version
```

no deben poder modificarse por aparecer accidentalmente en un
Payload externo.

La capacidad de serializar un campo no implica capacidad para
modificarlo.

---

# Elevación de Privilegios

Un actor no debe obtener nuevas capacidades mediante modificación
de datos pertenecientes a Proposal.

Proposal no almacena Roles ni Permissions como atributos
modificables por el proponente.

Debe mantenerse:

```text
Proposal Modification

≠

Permission Modification
```

---

# Confused Deputy

Una integración o servicio autorizado para una responsabilidad no
debe utilizar dicha capacidad para ejecutar operaciones diferentes
en nombre de otro actor sin el contexto correspondiente.

La arquitectura debe preservar la identidad y causalidad necesarias
para distinguir:

```text
Original Actor

Service Actor

Requested Operation
```

cuando corresponda.

Proposal recibe el contexto autorizado requerido por el dominio,
pero no administra credenciales entre servicios.

---

# Suplantación

La prevención técnica de suplantación pertenece a autenticación e
Infrastructure.

Dentro del dominio, ActorId debe representar la identidad
establecida por el contexto confiable correspondiente.

Proposal no debe aceptar identidad arbitraria proveniente
directamente de un Payload no confiable como prueba suficiente de
autenticación.

---

# Operaciones Administrativas

Las operaciones administrativas continúan sujetas al dominio.

Debe mantenerse:

```text
Administrator

≠

Invariant Exemption
```

Un administrador puede poseer capacidades adicionales según
Permissions.

No puede modificar:

- ProposalId;
- OrganizationId cuando sea inmutable;
- Version directamente;
- State Machine arbitrariamente;
- hechos históricos;
- límites de consistencia.

---

# Operaciones de Emergencia

Este documento no introduce Commands especiales de emergencia ni
mecanismos de bypass.

Si en el futuro el dominio requiere una capacidad excepcional,
deberá definirse explícitamente mediante:

- Command;
- Permission;
- invariantes;
- Domain Event;
- trazabilidad;
- documentación arquitectónica correspondiente.

No debe implementarse implícitamente como acceso directo.

---

# Operaciones Masivas

Una operación masiva a nivel de Application no crea una
autorización colectiva automática sobre todos los Aggregates.

Cada Proposal debe conservar su contexto.

Conceptualmente:

```text
Bulk Request

↓

Proposal A Authorization

Proposal B Authorization

Proposal C Authorization
```

cuando las reglas de autorización requieran evaluación individual.

---

# Seguridad en Procesamiento Masivo

El procesamiento masivo no puede:

- omitir permisos;
- omitir Version;
- omitir invariantes;
- modificar múltiples Aggregates como si fueran uno;
- ocultar fallos individuales;
- generar estados parciales inválidos dentro de una Proposal.

Las reglas definidas para una operación individual continúan
vigentes.

---

# Seguridad y Performance

Las optimizaciones definidas en:

```text
DOMAIN-007N-Performance-Rules.md
```

no pueden reducir controles de seguridad.

No está permitido optimizar mediante:

- omisión de autorización;
- omisión de invariantes;
- eliminación de Version;
- exposición excesiva de información;
- acceso directo a persistencia;
- bypass del Aggregate Root.

Debe mantenerse:

```text
Performance Optimization

≠

Security Reduction
```

---

# Caché de Autorización

Una implementación puede optimizar técnicamente la evaluación de
permisos.

Sin embargo:

```text
Authorization Cache

≠

Permission Definition
```

La caché no redefine capacidades.

Una decisión almacenada temporalmente debe respetar las reglas
vigentes del modelo de autorización.

---

# Seguridad y Disponibilidad

Una falla de un componente externo de seguridad no debe producir
automáticamente una operación permisiva.

No debe utilizarse conceptualmente:

```text
Authorization Service unavailable

↓

Allow Operation
```

como comportamiento predeterminado del dominio.

La política técnica concreta de disponibilidad pertenece a la capa
correspondiente.

---

# Fail Secure

Cuando no pueda determinarse de forma válida que una operación
protegida está autorizada, dicha incertidumbre no debe convertirse
en autorización implícita.

Conceptualmente:

```text
Authorization Unknown

≠

Authorization Granted
```

---

# Errores

Los errores devueltos por las capas externas no deben exponer
información innecesaria sobre:

- credenciales;
- secretos;
- infraestructura;
- detalles internos de persistencia;
- datos de otros actores;
- información privada de otras Organizations.

La representación técnica del error pertenece a Application e
Infrastructure.

---

# Rechazo Seguro

Cuando una operación sea rechazada:

```text
Aggregate State

=

Unchanged
```

y:

```text
ProposalVersion

=

Unchanged
```

No debe publicarse un Domain Event que represente una modificación
inexistente.

---

# Intentos No Autorizados

Un intento no autorizado no constituye una modificación de
Proposal.

Por lo tanto:

```text
Unauthorized Attempt

≠

Proposal State Change
```

La observación o auditoría del intento puede pertenecer al contexto
correspondiente sin modificar el Aggregate.

---

# Seguridad de Logs

Los logs técnicos no forman parte del Aggregate.

No deben utilizarse como sustituto de Domain Events ni Audit.

La infraestructura debe evitar registrar innecesariamente:

- tokens;
- contraseñas;
- secretos;
- credenciales;
- información privada completa.

Las políticas técnicas concretas pertenecen fuera del dominio.

---

# Audit y Security

Audit puede recibir información derivada de hechos y operaciones
relevantes.

Debe mantenerse:

```text
Proposal

↓

Domain Event

↓

Audit
```

cuando corresponda.

Proposal no absorbe Audit para obtener seguridad.

---

# Notification y Security

Notification puede reaccionar a hechos de Proposal.

Ejemplo:

```text
ProposalAccepted

↓

Notification Process
```

La Notification no forma parte de la transacción interna del
Aggregate.

Un fallo en Notification no debe revertir una transición válida de
Proposal únicamente porque el canal de comunicación haya fallado.

---

# Document y Security

Cuando Proposal referencia Documents, la existencia de:

```text
DocumentId
```

no implica autorización automática para acceder al contenido del
Document.

Document conserva sus propias reglas de acceso y ciclo de vida.

Debe mantenerse:

```text
Proposal Reference to Document

≠

Document Access Permission
```

---

# Assembly y Security

Cuando una Proposal se relaciona con:

```text
AssemblyId
```

la relación contextual no concede automáticamente permisos sobre
Assembly.

Proposal y Assembly mantienen sus propios límites y reglas.

Debe mantenerse:

```text
Proposal Permission

≠

Assembly Permission
```

---

# Voting y Security

Cuando una Proposal se relaciona con Voting, las capacidades sobre
Proposal no conceden automáticamente capacidades sobre el proceso
de votación.

Debe mantenerse:

```text
Proposal Authorization

≠

Voting Authorization
```

Voting conserva:

- identidad;
- Lifecycle;
- invariantes;
- Permissions;
- Repository;
- Domain Events.

---

# Participation y Security

Una relación con Participation no convierte las capacidades de
participación en permisos de modificación sobre Proposal.

Ambos conceptos mantienen sus responsabilidades independientes.

---

# Territory y Security

La relación mediante:

```text
TerritoryId
```

no concede capacidad para modificar Territory.

Proposal utiliza la referencia únicamente conforme a su propio
modelo.

---

# Seguridad entre Aggregates

Las relaciones entre Aggregates no transfieren permisos
automáticamente.

Debe mantenerse:

```text
Permission in Aggregate A

≠

Permission in Aggregate B
```

salvo que una política explícita del modelo de autorización defina
dicha capacidad.

---

# Domain Event Consumer

Consumir un Domain Event no concede capacidad de modificar
Proposal.

Un consumidor puede reaccionar al hecho conforme a su propia
responsabilidad.

Si necesita solicitar un cambio sobre Proposal, debe utilizar el
mecanismo autorizado correspondiente.

---

# Integration Event Consumer

Un consumidor externo de Integration Events tampoco obtiene
capacidad implícita de escritura.

Debe mantenerse:

```text
Event Consumption

≠

Write Authorization
```

---

# Idempotencia

Los mecanismos de idempotencia pueden evitar procesamiento
duplicado de una misma intención o evento.

La idempotencia no debe permitir reutilizar una identidad para
ejecutar una operación diferente.

Debe mantenerse:

```text
Same CommandId

≠

Different Authorized Intent
```

---

# Replay Attack Conceptual

La repetición técnica de una solicitud previamente válida no debe
interpretarse automáticamente como una nueva intención válida.

Los mecanismos concretos para evitar repetición indebida
pertenecen a Application e Infrastructure.

El dominio mantiene:

- CommandId;
- Version;
- estado;
- invariantes;
- trazabilidad;

según corresponda al contrato definido.

---

# Integridad de Mensajes

La verificación criptográfica de integridad pertenece a
Infrastructure.

Proposal no implementa:

- firmas digitales;
- HMAC;
- certificados;
- validación criptográfica.

Una vez establecida la confianza técnica correspondiente, el
Aggregate continúa validando las reglas del dominio.

---

# Seguridad de APIs

Las APIs no forman parte del Aggregate.

Una API puede:

- autenticar;
- autorizar;
- validar formato;
- aplicar límites técnicos;
- transformar solicitudes en Commands.

Pero no debe reemplazar:

```text
Proposal Invariants

Proposal State Machine

Proposal Versioning
```

La existencia de validación en API no permite eliminarla del
dominio cuando corresponda a una regla conceptual.

---

# Rate Limiting

Rate Limiting pertenece a Infrastructure o Application.

No forma parte de Proposal.

Conceptos como:

```text
Requests per second

Requests per minute

Burst limits
```

no constituyen atributos del Aggregate.

La protección técnica contra abuso no modifica el modelo del
dominio.

---

# Protección contra Denegación de Servicio

Las medidas contra abuso de recursos pertenecen a Infrastructure.

Pueden existir controles sobre:

- tráfico;
- concurrencia;
- tamaño de Payload;
- frecuencia de solicitudes;
- recursos computacionales.

Estas medidas no forman parte del estado de Proposal.

---

# Tamaño de Payload

Los Commands e Integration Events deben transportar únicamente la
información necesaria para su responsabilidad.

Esta regla reduce simultáneamente:

- exposición;
- acoplamiento;
- superficie de ataque;
- costo de procesamiento.

La minimización de Payload no puede eliminar información requerida
para validar el dominio.

---

# Seguridad por Diseño

Proposal debe mantenerse seguro por construcción mediante:

- encapsulación;
- Aggregate Root;
- Value Objects;
- invariantes;
- State Machine;
- Commands explícitos;
- permisos explícitos;
- Version;
- referencias por identidad;
- límites de consistencia;
- separación de infraestructura.

La seguridad no debe depender exclusivamente de convenciones
externas.

---

# Principio de Mínimo Privilegio

Los actores deben recibir únicamente las capacidades necesarias
para sus responsabilidades.

Conceptualmente:

```text
Actor

↓

Minimum Required Permission

↓

Allowed Command
```

No debe utilizarse una autorización global cuando una capacidad
específica sea suficiente.

La definición concreta de permisos pertenece a:

```text
DOMAIN-007F-Permissions.md
```

---

# Principio de Necesidad de Conocer

La información expuesta debe limitarse a lo necesario para el
propósito autorizado.

Una vista de listado puede requerir menos información que una vista
detallada.

Una integración puede requerir menos información que un Read
Model interno.

Debe mantenerse:

```text
Consumer Purpose

↓

Necessary Information
```

---

# Default Deny

Una capacidad no definida explícitamente no debe considerarse
automáticamente permitida.

Conceptualmente:

```text
Permission Not Established

↓

Operation Not Authorized
```

Las excepciones deben formar parte del modelo oficial y no surgir
de comportamiento implícito.

---

# Separation of Duties

Cuando el modelo de permisos diferencie responsabilidades, estas no
deben fusionarse accidentalmente.

Ejemplo conceptual:

```text
Propose

≠

Review

≠

Accept
```

La capacidad de crear una Proposal no implica necesariamente la
capacidad de revisarla o aceptarla.

Las reglas concretas permanecen definidas en Permissions.

---

# Seguridad de Estados Terminales

Los estados terminales o restringidos definidos por el Lifecycle
deben protegerse especialmente frente a modificaciones
posteriores.

Una Proposal:

```text
Archived
```

no debe modificarse mediante operaciones ordinarias cuando las
invariantes establezcan su inmutabilidad.

Un permiso administrativo no elimina esta restricción.

---

# Seguridad de Proposal Cancelada o Retirada

Cuando el modelo contemple un estado como:

```text
Withdrawn
```

las operaciones posteriores deben respetar las transiciones
definidas.

No debe utilizarse una modificación directa para reactivar una
Proposal si la State Machine no contempla dicha transición.

---

# Seguridad de Proposal Rechazada

Una Proposal rechazada permanece sujeta al Lifecycle oficial.

No debe aceptarse posteriormente mediante modificación directa de
Status.

Cualquier evolución permitida debe existir explícitamente en la
State Machine.

---

# Seguridad de Proposal Aceptada

Una Proposal aceptada no puede volver arbitrariamente a estados
anteriores.

Debe respetarse el comportamiento definido por el dominio.

La autorización no permite reescribir la historia conceptual del
Aggregate.

---

# Protección de Hechos Consumados

Los Domain Events representan hechos consumados.

No deben modificarse semánticamente después de publicados para
hacer parecer que ocurrió un hecho diferente.

Ejemplo:

```text
ProposalAccepted
```

no debe reinterpretarse posteriormente como:

```text
ProposalRejected
```

La evolución posterior debe representarse mediante nuevos hechos
válidos cuando el dominio los contemple.

---

# Seguridad de Versionado de Contratos

Los contratos externos pueden evolucionar.

La evolución no debe alterar silenciosamente el significado de
campos existentes.

Un consumidor debe poder distinguir versiones incompatibles cuando
la evolución contractual lo requiera.

La estrategia técnica concreta pertenece a Integration.

---

# Seguridad de Extension Points

Los puntos de extensión futuros no pueden utilizarse para evadir el
Security Model.

Una extensión debe respetar:

- Authentication separation;
- Authorization;
- Permissions;
- Invariants;
- State Machine;
- Version;
- Consistency Boundary;
- data minimization;
- Aggregate Root protection.

La especificación correspondiente se documentará en:

```text
DOMAIN-007P-Extension-Points.md
```

---

# Nuevos Commands

Todo nuevo Command debe definir explícitamente:

- intención;
- actor cuando corresponda;
- permiso requerido;
- estados permitidos;
- invariantes aplicables;
- efectos sobre Version;
- Domain Events resultantes;
- información de trazabilidad.

Un nuevo Command no puede introducir un bypass genérico.

---

# Nuevos Domain Events

Todo nuevo Domain Event debe:

- representar un hecho consumado;
- originarse en comportamiento válido;
- evitar exposición innecesaria;
- mantener trazabilidad;
- respetar el lenguaje ubicuo;
- no transportar credenciales.

---

# Nuevos Read Models

Todo nuevo Read Model debe definir:

- propósito;
- consumidor;
- información expuesta;
- fuente de actualización;
- reglas de acceso aplicables;
- posibilidad de reconstrucción.

Una nueva proyección no debe ampliar implícitamente los permisos de
lectura.

---

# Nuevas Integraciones

Toda nueva integración debe mantener:

```text
Proposal

↓

Domain Contract

↓

Integration Contract

↓

Adapter

↓

External System
```

La integración no puede introducir una dependencia técnica dentro
del Aggregate.

---

# Nuevos Proveedores de Identidad

La sustitución o incorporación de un proveedor de identidad no debe
modificar el Aggregate Proposal.

Puede cambiar:

```text
Identity Provider
```

sin cambiar:

```text
ProposalId

Lifecycle

State Machine

Commands

Domain Events

Invariants

Version

Consistency Boundary
```

---

# Nuevos Mecanismos de Autorización

Una implementación técnica de autorización puede evolucionar.

Sin embargo, las capacidades conceptuales definidas por el dominio
deben permanecer explícitas.

Debe mantenerse:

```text
Authorization Technology

≠

Domain Permission Model
```

---

# Amenazas Conceptuales

El modelo debe protegerse frente a situaciones como:

- modificación directa de estado;
- modificación de identidad;
- modificación directa de Version;
- bypass de State Machine;
- bypass de invariantes;
- ejecución sin autorización;
- acceso cruzado entre Organizations;
- lost updates;
- exposición excesiva de información;
- publicación prematura de eventos;
- manipulación de referencias externas;
- utilización de Read Models como Write Models;
- incorporación de credenciales al dominio;
- utilización de integraciones como acceso directo;
- repetición indebida de operaciones;
- elevación de privilegios;
- confusión entre identidad técnica y dominio.

---

# Matriz Conceptual de Protección

```text
Elemento                 Protección Principal

ProposalId               Inmutabilidad

OrganizationId           Contexto organizacional e inmutabilidad

Status                   State Machine

Lifecycle                Transiciones válidas

Version                   Concurrencia optimista

Commands                  Authorization + Domain Validation

Domain Events             Valid Domain Behavior

Integration Events        Minimum Necessary Contract

Read Models               Read Authorization

Repository                Aggregate Persistence Contract

External References       Identity-only Relationship

Credentials               Outside Aggregate

Permissions               Authorization Model

Invariants                Aggregate Root
```

---

# Flujo Seguro de Escritura

```text
Authenticated Actor

        │
        ▼

Authorization Context

        │
        ▼

Command

        │
        ▼

Permission Validation

        │
        ▼

Load Proposal

        │
        ▼

Version Validation

        │
        ▼

State Machine Validation

        │
        ▼

Invariant Validation

        │
        ▼

Domain Behavior

        │
        ▼

New Valid State

        │
        ▼

Version Increment

        │
        ▼

Persistence

        │
        ▼

Domain Event
```

Ninguna etapa posterior convierte en válida una operación que haya
fallado en una etapa anterior.

---

# Flujo Seguro de Lectura

```text
Authenticated Consumer

        │
        ▼

Read Authorization

        │
        ▼

Authorized Projection

        │
        ▼

Field Selection

        │
        ▼

Read Model
```

El flujo de lectura no atraviesa comportamiento de modificación del
Aggregate.

---

# Flujo Seguro de Integración

```text
Proposal

        │
        ▼

Domain Event

        │
        ▼

Confirmed State

        │
        ▼

Integration Mapping

        │
        ▼

Minimum Necessary Payload

        │
        ▼

Integration Event

        │
        ▼

Authorized External Consumer
```

El consumidor externo permanece fuera del límite de Proposal.

---

# Escenario — Command Autorizado y Estado Válido

## Given

Un actor autenticado posee permiso para ejecutar:

```text
SubmitProposal
```

y Proposal se encuentra en un estado que permite la operación.

## When

El Command es ejecutado con una Version válida.

## Then

Proposal valida sus invariantes.

Si todas las reglas se cumplen:

- modifica su estado;
- incrementa Version;
- publica el Domain Event correspondiente.

---

# Escenario — Actor No Autorizado

## Given

Un actor autenticado no posee permiso para ejecutar:

```text
AcceptProposal
```

## When

Intenta ejecutar el Command.

## Then

La operación debe rechazarse.

Debe mantenerse:

```text
Proposal State unchanged

ProposalVersion unchanged
```

No se publica:

```text
ProposalAccepted
```

---

# Escenario — Actor Autorizado con Estado Inválido

## Given

Un actor posee permiso para:

```text
AcceptProposal
```

pero Proposal se encuentra en un estado desde el cual la
State Machine no permite aceptación.

## When

El actor ejecuta el Command.

## Then

La operación se rechaza por regla de dominio.

La autorización no modifica la State Machine.

---

# Escenario — Actor Autorizado con Invariante Inválida

## Given

El actor posee autorización.

## When

La operación produciría una violación de una invariante.

## Then

Proposal rechaza la operación.

No existe excepción por privilegio.

---

# Escenario — Version Obsoleta

## Given

```text
Stored Version = 12

ExpectedVersion = 11
```

## When

Un actor autorizado intenta modificar Proposal.

## Then

La operación debe detectar el conflicto de concurrencia.

No se sobrescribe silenciosamente la revisión actual.

---

# Escenario — Organization Incorrecta

## Given

```text
Proposal.OrganizationId = Organization-A
```

y el Command declara:

```text
OrganizationId = Organization-B
```

## When

Se intenta modificar Proposal.

## Then

La inconsistencia organizacional debe impedir la modificación.

---

# Escenario — Lectura Autorizada

## Given

Un consumidor posee autorización para consultar:

```text
ProposalSummary
```

## When

Solicita una vista de Proposal.

## Then

Recibe únicamente los campos definidos para dicha proyección y
permitidos por el contexto de lectura.

---

# Escenario — Lectura No Autorizada

## Given

Un consumidor no posee autorización para una vista protegida.

## When

Solicita la información.

## Then

La capa de autorización debe impedir la exposición.

Proposal no debe modificarse como consecuencia del intento.

---

# Escenario — Integración Externa

## Given

Una Proposal produce un hecho que debe comunicarse externamente.

## When

El estado se confirma.

## Then

La integración publica únicamente la información definida por el
contrato correspondiente.

No expone automáticamente el Aggregate completo.

---

# Escenario — FIWARE

## Given

Una integración necesita representar información de Proposal en
FIWARE.

## When

Se procesa el hecho correspondiente.

## Then

Debe mantenerse:

```text
Proposal

↓

Domain Event

↓

Integration Event

↓

FIWARE Adapter

↓

NGSI-LD
```

Proposal no procesa directamente autenticación FIWARE ni conoce el
Context Broker.

---

# Escenario — Escritura Directa

## Given

Un componente técnico posee acceso a persistencia.

## When

Intenta modificar directamente:

```text
ProposalStatus
```

sin ejecutar comportamiento del Aggregate.

## Then

La operación viola el Security Model aunque sea técnicamente
posible.

La capacidad de infraestructura no constituye autorización de
dominio.

---

# Escenario — Replay

## Given

Se reconstruye Proposal desde su historial.

## When

Los eventos históricos son aplicados.

## Then

El estado se reconstruye.

No deben generarse como nuevas operaciones:

- Notifications;
- Integration Events;
- Commands;
- autorizaciones;
- efectos externos.

---

# Escenario — Read Model Manipulado

## Given

Una proyección contiene:

```text
ProposalStatus = Accepted
```

mientras el Aggregate mantiene otro estado.

## When

La proyección es modificada directamente.

## Then

el estado de Proposal no cambia.

El Read Model no constituye fuente de escritura.

---

# Escenario — Referencia a Document

## Given

Proposal contiene:

```text
DocumentId
```

## When

Un actor posee permiso para leer Proposal.

## Then

no debe inferirse automáticamente que posee permiso para leer el
Document.

El acceso documental se evalúa según las reglas correspondientes.

---

# Escenario — Operación Masiva

## Given

Una operación intenta procesar múltiples Proposals.

## When

los actores, Organizations, estados o Versions difieren.

## Then

cada Proposal debe mantener su propia evaluación de seguridad y
consistencia.

La operación masiva no crea un bypass colectivo.

---

# Escenario — Administrador

## Given

Un actor posee capacidades administrativas.

## When

intenta modificar directamente:

```text
ProposalId
```

o:

```text
Version
```

## Then

la operación debe continuar siendo inválida.

Los privilegios no eliminan invariantes estructurales.

---

# Escenario — Integración Lenta

## Given

Proposal confirma una modificación válida.

## When

un consumidor externo procesa lentamente el Integration Event.

## Then

la lentitud del consumidor no amplía el límite transaccional ni
modifica las reglas de seguridad internas de Proposal.

---

# Escenario — Intento Repetido

## Given

Una intención ya fue procesada.

## When

el mismo CommandId es recibido nuevamente.

## Then

el mecanismo correspondiente debe evitar interpretar
arbitrariamente la repetición como una nueva intención distinta.

La estrategia técnica de idempotencia pertenece fuera del
Aggregate.

---

# Reglas de Seguridad para Tests

Los escenarios definidos en:

```text
DOMAIN-007M-Test-Scenarios.md
```

deben incluir validaciones que permitan comprobar:

- rechazo de actores no autorizados;
- rechazo de transiciones inválidas;
- protección de invariantes;
- protección de Version;
- protección de identidad;
- aislamiento organizacional;
- ausencia de modificaciones directas;
- ausencia de exposición innecesaria;
- independencia de Infrastructure;
- separación entre lectura y escritura;
- separación entre Domain Events e Integration Events;
- preservación de límites entre Aggregates.

---

# Reglas de Seguridad para Performance

Las optimizaciones definidas en:

```text
DOMAIN-007N-Performance-Rules.md
```

deben mantener todos los controles establecidos en este documento.

No existe una ruta de alto rendimiento que pueda omitir:

```text
Authorization

State Validation

Invariant Validation

Version Validation
```

cuando dichas validaciones correspondan a la operación.

---

# Restricciones

No está permitido:

- almacenar contraseñas en Proposal;
- almacenar tokens en Proposal;
- almacenar secretos en Proposal;
- administrar sesiones desde Proposal;
- validar JWT dentro del Aggregate;
- implementar OAuth dentro del Aggregate;
- depender de Keyrock;
- depender de PEP Proxy;
- depender de FIWARE para validar invariantes;
- modificar ProposalId;
- modificar OrganizationId cuando sea inmutable;
- modificar Version directamente;
- modificar Status directamente;
- evadir la State Machine;
- evadir el Lifecycle;
- evadir invariantes;
- considerar autenticación equivalente a autorización;
- considerar autorización equivalente a validez de dominio;
- transferir permisos automáticamente entre Aggregates;
- utilizar Read Models para modificar Proposal;
- utilizar Repository como motor de autorización;
- publicar Domain Events sin comportamiento válido;
- publicar Integration Events como sustituto del Commit;
- exponer el Aggregate completo por defecto;
- incluir credenciales en Commands;
- incluir credenciales en Domain Events;
- incluir credenciales en Integration Events;
- permitir acceso cruzado entre Organizations sin capacidad
  explícita;
- aceptar lost updates;
- utilizar permisos administrativos para romper invariantes;
- incorporar decisiones técnicas de seguridad como estado del
  dominio.

---

# Compatibilidad con DDD

El Security Model mantiene los principios de Domain-Driven Design.

La seguridad del dominio se expresa mediante:

- Aggregate Root;
- encapsulación;
- Value Objects;
- invariantes;
- comportamiento;
- límites de consistencia;
- lenguaje ubicuo;
- referencias por identidad.

Los mecanismos técnicos permanecen fuera del modelo del dominio.

---

# Compatibilidad con Clean Architecture

Proposal no depende de mecanismos externos de seguridad.

Debe mantenerse:

```text
Infrastructure

↓

Application

↓

Domain
```

Las dependencias apuntan hacia el dominio.

El dominio no depende de:

```text
OAuth Provider

JWT Library

Identity Server

Database

API Gateway

PEP Proxy
```

---

# Compatibilidad con Arquitectura Hexagonal

Los mecanismos de seguridad externos pueden conectarse mediante
Ports y Adapters.

Conceptualmente:

```text
External Request

↓

Authentication Adapter

↓

Authorization Adapter

↓

Application Service

↓

Proposal
```

El Adapter puede cambiar sin modificar el Aggregate.

---

# Compatibilidad con CQRS

El Security Model distingue las capacidades de:

```text
Write Authorization
```

y:

```text
Read Authorization
```

Los Commands y Read Models pueden aplicar políticas diferentes
según su responsabilidad.

La separación CQRS no elimina la necesidad de seguridad en ninguno
de los lados.

---

# Compatibilidad con Event Sourcing

Cuando se utilice Event Sourcing:

- los eventos históricos representan hechos;
- el replay no representa una nueva operación;
- Version debe preservarse;
- la historia no debe alterarse arbitrariamente;
- los efectos externos no se repiten durante reconstrucción;
- los eventos no deben contener credenciales.

---

# Compatibilidad con Event-Driven Architecture

Los consumidores de eventos permanecen desacoplados del Aggregate.

Debe mantenerse:

```text
Event Consumer

≠

Implicitly Authorized Proposal Writer
```

Toda nueva intención de modificación debe ingresar por el contrato
autorizado correspondiente.

---

# Compatibilidad con Arquitectura Distribuida

La distribución técnica no modifica las reglas de seguridad del
dominio.

Proposal puede ejecutarse en múltiples instancias de aplicación sin
perder:

- Version;
- aislamiento organizacional;
- autorización;
- invariantes;
- State Machine;
- trazabilidad.

---

# Principios Arquitectónicos

El Security Model mantiene:

```text
Authentication

≠

Authorization
```

```text
Authorization

≠

Domain Validation
```

```text
Permission

≠

Invariant
```

```text
Role

≠

Permission
```

```text
ActorId

≠

Credential
```

```text
CitizenId

≠

Automatically ActorId
```

```text
Read Permission

≠

Write Permission
```

```text
Proposal Permission

≠

Other Aggregate Permission
```

```text
Reference

≠

Authorization
```

```text
Repository

≠

Authorization Engine
```

```text
Read Model

≠

Write Model
```

```text
Cache

≠

Authorization Source
```

```text
Domain Event

≠

Command
```

```text
Integration Event

≠

Write Permission
```

```text
Administrator

≠

Invariant Exemption
```

```text
Infrastructure Access

≠

Domain Authorization
```

```text
Technical Security

≠

Domain Security
```

```text
Performance Optimization

≠

Security Reduction
```

---

# Extension Points de Seguridad

El Security Model puede evolucionar mediante nuevas capacidades sin
alterar sus principios fundamentales.

Pueden incorporarse:

- nuevas Permissions;
- nuevos tipos de actor;
- nuevos Read Models protegidos;
- nuevas políticas organizacionales;
- nuevos contratos de integración;
- nuevos mecanismos técnicos de autenticación;
- nuevos mecanismos técnicos de autorización;
- nuevas políticas de privacidad;
- nuevas capacidades de auditoría.

Toda extensión debe mantener:

- separación de responsabilidades;
- Aggregate Root;
- invariantes;
- Lifecycle;
- State Machine;
- Version;
- Consistency Boundary;
- minimización de datos;
- independencia tecnológica.

La definición formal de extensibilidad se documentará en:

```text
DOMAIN-007P-Extension-Points.md
```

---

# Documentación Complementaria

El Security Model debe interpretarse conjuntamente con:

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

DOMAIN-007P-Extension-Points.md
```

Estos documentos constituyen conjuntamente la definición
conceptual del Aggregate Proposal.

El Security Model no reemplaza Permissions, Invariants, Lifecycle
ni State Machine.

Define cómo estos elementos participan conjuntamente en la
protección conceptual del Aggregate.

---

# Definición de Éxito

El Security Model del Aggregate **Proposal** garantiza que toda
interacción con el Aggregate preserve la separación entre
identidad, autenticación, autorización, comportamiento del dominio,
persistencia e infraestructura.

El modelo protege:

```text
ProposalId

OrganizationId

Proposal State

Lifecycle

State Machine

Invariants

Version

Commands

Domain Events

Integration Events

Read Models

Consistency Boundary

External References
```

Toda modificación válida requiere una intención autorizada y un
estado compatible con las reglas del dominio.

La autenticación identifica al actor.

La autorización determina qué operación puede intentar.

Proposal determina si la operación puede ocurrir conforme a su
estado, Lifecycle, State Machine, invariantes y Version.

La infraestructura protege credenciales, transporte, persistencia,
mensajería y mecanismos técnicos sin convertirse en parte del
Aggregate.

Las relaciones con Organization, Citizen, Membership, Role,
Territory, Assembly, Participation, Voting, Document,
Notification, Audit e Integration se mantienen desacopladas y no
transfieren permisos implícitamente entre Aggregates.

De esta forma, `DOMAIN-007O-Security-Model.md` constituye el modelo
conceptual oficial de seguridad del Aggregate **Proposal**,
preservando encapsulación, autorización, consistencia,
trazabilidad, privacidad, aislamiento organizacional,
interoperabilidad e independencia tecnológica dentro de la
arquitectura DDD consolidada de AURA Core.