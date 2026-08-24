# DOMAIN-006O — Assembly Security Model

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Assembly Management

Aggregate:
Assembly

Documentos relacionados:

* DOMAIN-006-Aggregate.md
* DOMAIN-006A-Lifecycle.md
* DOMAIN-006B-State-Machine.md
* DOMAIN-006C-Commands.md
* DOMAIN-006D-Domain-Events.md
* DOMAIN-006E-Invariants.md
* DOMAIN-006F-Permissions.md
* DOMAIN-006G-Repository-Contract.md
* DOMAIN-006H-Examples.md
* DOMAIN-006I-Versioning.md
* DOMAIN-006J-Consistency-Boundary.md
* DOMAIN-006K-Integration-Events.md
* DOMAIN-006L-Read-Model.md
* DOMAIN-006M-Test-Scenarios.md
* DOMAIN-006N-Performance-Rules.md
* CORE-003-Shared-Kernel.md
* CORE-004-Ubiquitous-Language.md
* CORE-006-Domain-Invariants.md
* CORE-008-Aggregate-Design-Rules.md
* CORE-011-Repository-Contracts.md

---

# Objetivo

Definir el modelo conceptual de seguridad aplicable al Aggregate
**Assembly**.

El Security Model establece las reglas que protegen las
operaciones, el estado, la información, las relaciones y los
límites del Aggregate sin introducir responsabilidades de
autenticación, gestión de credenciales, sesiones, criptografía o
infraestructura dentro del dominio.

La seguridad de Assembly debe mantener una separación explícita
entre:

```text
Authentication

Authorization

Permissions

Domain Invariants

Aggregate State

Data Protection

Audit

Infrastructure Security
```

Cada una de estas responsabilidades cumple una función diferente.

Assembly protege sus propias invariantes, su Lifecycle, su State
Machine y la consistencia de su estado.

Los mecanismos técnicos utilizados para autenticar actores,
transportar solicitudes, proteger credenciales o asegurar
comunicaciones permanecen fuera del Aggregate.

---

# Propósito

El propósito del Security Model es garantizar que toda interacción
con Assembly preserve simultáneamente:

* identidad del Aggregate;
* contexto organizacional;
* contexto territorial cuando corresponda;
* Permissions;
* Lifecycle;
* State Machine;
* invariantes;
* Consistency Boundary;
* Versioning;
* trazabilidad;
* integridad del estado;
* confidencialidad de la información cuando corresponda;
* separación entre dominio, autorización e infraestructura.

El Security Model no reemplaza ninguno de los documentos que
definen el comportamiento del Aggregate.

Su responsabilidad es establecer cómo deben relacionarse los
conceptos de seguridad con dichas reglas sin alterar su significado.

---

# Principios

El Security Model de Assembly sigue los siguientes principios:

* Authentication permanece fuera del Aggregate;
* Authorization permanece separada de las invariantes;
* Permissions determinan capacidades de operación;
* un Permission no garantiza que una operación sea válida;
* Lifecycle continúa controlando la evolución de Assembly;
* State Machine continúa controlando las transiciones;
* las invariantes nunca pueden omitirse por privilegios técnicos;
* Versioning continúa protegiendo la concurrencia;
* Assembly mantiene encapsulado su estado;
* otros Aggregates permanecen fuera del Consistency Boundary;
* las credenciales nunca forman parte del Aggregate;
* los secretos pertenecen a Infrastructure;
* los Integration Events no transportan credenciales;
* los Read Models exponen únicamente información autorizada;
* conocer un identificador no concede autoridad;
* una operación rechazada no modifica el Aggregate;
* la seguridad técnica no redefine el modelo del dominio.

---

# Modelo Conceptual

Conceptualmente, una operación protegida sobre Assembly sigue:

```text
Actor

↓

Authentication

↓

Authorization

↓

Permission Validation

↓

Command

↓

Assembly Aggregate

↓

State Machine

↓

Domain Invariants

↓

Valid State Change

↓

Domain Events
```

Cada etapa cumple una responsabilidad específica.

La eliminación de una etapa no puede sustituirse implícitamente por
otra.

---

# Authentication

Authentication responde conceptualmente a:

```text
Who is the actor?
```

Authentication determina la identidad del sujeto que intenta
interactuar con AURA.

Assembly no administra Authentication.

Assembly no valida directamente:

* usuarios;
* contraseñas;
* credenciales;
* factores de autenticación;
* sesiones;
* Access Tokens;
* Refresh Tokens;
* JWT;
* certificados;
* proveedores de identidad.

La autenticación debe resolverse antes de que una intención
protegida alcance el comportamiento correspondiente del dominio.

---

# Authorization

Authorization responde conceptualmente a:

```text
May this actor attempt this operation?
```

Authorization determina si un actor posee la capacidad necesaria
para intentar una operación sobre Assembly.

Authorization no determina que la operación pueda ejecutarse
válidamente dentro del estado actual del Aggregate.

Debe mantenerse:

```text
Authorized
    ≠
Domain Valid
```

---

# Permissions

Los Permissions oficiales de Assembly se definen en:

```text
DOMAIN-006F-Permissions.md
```

Un Permission representa una capacidad autorizada para intentar una
operación determinada.

Debe mantenerse:

```text
Permission

↓

May Attempt Operation
```

No:

```text
Permission

↓

Operation Must Succeed
```

La existencia de Permission no sustituye:

* Lifecycle;
* State Machine;
* Guards;
* invariantes;
* Versioning;
* Consistency Boundary.

---

# Domain Invariants

Las invariantes oficiales se encuentran definidas en:

```text
DOMAIN-006E-Invariants.md
```

Las invariantes responden conceptualmente a:

```text
Is this state transition valid for the domain?
```

Un actor autorizado continúa sujeto a todas las invariantes.

Debe mantenerse:

```text
Permission Granted
    +
Invariant Violated

↓

Operation Rejected
```

No existe un Permission que permita mantener Assembly en un estado
inválido.

---

# Separación entre Permission e Invariant

Debe mantenerse permanentemente:

```text
Permission
    ≠
Invariant
```

Permission determina quién puede intentar una operación.

Invariant determina si la operación puede producir un estado válido.

Ejemplo conceptual:

```text
Actor has permission to StartAssembly

But

AssemblyStatus = Draft

↓

StartAssembly rejected
```

El actor está autorizado.

La operación no es válida desde el estado actual.

---

# Actor

Un Actor representa al sujeto responsable de intentar una
operación.

Conceptualmente puede identificarse mediante:

```text
ActorId
```

ActorId permite mantener referencia y trazabilidad cuando
corresponda.

ActorId:

* no es una credencial;
* no es una sesión;
* no es un token;
* no representa Authentication;
* no representa Permission;
* no forma parte de la identidad de Assembly.

---

# Contexto Organizacional

Cada Assembly pertenece a una única Organization.

La referencia se mantiene mediante:

```text
OrganizationId
```

OrganizationId forma parte del contexto fundamental de Assembly.

Las capacidades organizacionales deben evaluarse dentro del contexto
correspondiente.

Conceptualmente:

```text
Actor

+

Organization Context

+

Permission

+

AssemblyId

↓

Authorized Domain Intent
```

---

# Aislamiento Organizacional

La autoridad correspondiente a una Organization no debe utilizarse
implícitamente para modificar una Assembly perteneciente a otra
Organization.

Debe mantenerse:

```text
Authority in Organization A
    ≠
Authority in Organization B
```

cuando no exista una capacidad explícita que determine lo
contrario en el modelo de autorización correspondiente.

---

# OrganizationId

OrganizationId:

* identifica la Organization propietaria;
* es obligatorio;
* permanece inmutable;
* participa en el contexto de seguridad;
* no representa una copia de Organization;
* no concede autoridad sobre Organization.

Assembly no puede utilizar una operación de actualización para
trasladarse entre Organizations.

---

# TerritoryId

Cuando Assembly mantiene contexto territorial, la relación se
representa mediante:

```text
TerritoryId
```

TerritoryId contextualiza la Assembly.

No concede autoridad para modificar Territory.

Debe mantenerse:

```text
Territory Reference
    ≠
Territory Permission
```

---

# Membership

Membership mantiene su propio Aggregate.

La relación entre un actor y una Organization puede utilizar
Membership como parte del modelo de autorización correspondiente.

Assembly no administra:

* creación de Membership;
* activación de Membership;
* suspensión de Membership;
* terminación de Membership;
* estado interno de Membership.

Debe mantenerse:

```text
Membership
    outside
Assembly Consistency Boundary
```

---

# Role

Role mantiene su propio Aggregate.

Los Roles pueden participar en la determinación de capacidades
organizacionales.

Assembly no administra:

* creación de Role;
* modificación de Role;
* asignaciones de Role;
* estado interno de Role.

Debe mantenerse:

```text
Role
    ≠
Assembly Internal Entity
```

---

# Citizen

Citizen representa identidad cívica bajo su propio Aggregate.

Assembly no autentica Citizen.

Assembly no almacena las credenciales de Citizen.

Assembly no modifica Citizen.

Cuando una relación lo requiera se utiliza:

```text
CitizenId
```

conforme al modelo oficial del dominio.

---

# Principio de Mínimo Privilegio

Un Actor debe poseer únicamente las capacidades necesarias para
realizar las operaciones autorizadas.

Debe mantenerse:

```text
Permission
    scoped to
Required Capability
```

Una necesidad operativa específica no debe utilizarse para
conceder capacidades más amplias que las requeridas.

---

# Denegación de Operaciones

Cuando una operación requiere Permission y el actor no posee dicha
capacidad, la operación debe ser rechazada.

Conceptualmente:

```text
Missing Permission

↓

Operation Rejected

↓

Assembly Unchanged
```

---

# Rechazo Seguro

Toda operación rechazada por razones de autorización debe cumplir:

```text
Assembly State
    =
Unchanged
```

```text
Version
    =
Unchanged
```

```text
Success Domain Event
    =
Not Produced
```

No debe existir modificación parcial.

---

# Seguridad de Commands

Los Commands oficiales se definen en:

```text
DOMAIN-006C-Commands.md
```

Un Command representa una intención de modificación.

Los Commands protegidos deben ser ejecutados únicamente dentro del
contexto de autorización correspondiente.

Conceptualmente pueden mantener información de trazabilidad como:

```text
CommandId

AssemblyId

OrganizationId

ActorId

Timestamp

CorrelationId

CausationId
```

conforme al modelo de Commands establecido.

---

# Datos de un Command

La información recibida por un Command no constituye por sí misma
estado autoritativo del dominio.

Debe mantenerse:

```text
Command Data
    ≠
Trusted Aggregate State
```

Assembly continúa siendo responsable de validar sus propias reglas
antes de confirmar una modificación.

---

# CommandId

CommandId identifica una intención concreta.

No constituye:

* Authentication;
* Authorization;
* Permission;
* identidad del Actor;
* identidad del Aggregate.

Debe mantenerse:

```text
CommandId
    ≠
Credential
```

---

# CorrelationId

CorrelationId permite relacionar múltiples elementos de un mismo
flujo.

No concede autoridad.

No sustituye Authentication.

No sustituye Permission.

---

# CausationId

CausationId permite identificar relaciones causales entre
operaciones y eventos.

Debe mantenerse:

```text
Traceability Metadata
    ≠
Authorization
```

---

# Aggregate Root

La única Aggregate Root continúa siendo:

```text
Assembly
```

Toda modificación debe ejecutarse mediante comportamiento definido
por esta raíz.

No existen modificaciones legítimas del estado interno que eviten
el Aggregate Root.

---

# Encapsulación

Assembly debe mantener encapsulado su estado interno.

No deben existir setters públicos que permitan modificar
directamente:

```text
AssemblyId

OrganizationId

AssemblyStatus

Version
```

ni otros atributos protegidos por el Aggregate.

La encapsulación permite garantizar que cada modificación pase por
las reglas correspondientes.

---

# Seguridad del Estado

La protección del estado de Assembly depende de la combinación de:

```text
Aggregate Root

Lifecycle

State Machine

Permissions

Invariants

Versioning
```

Ninguno de estos mecanismos debe eliminarse porque otro exista.

---

# Lifecycle

El Lifecycle oficial se define en:

```text
DOMAIN-006A-Lifecycle.md
```

Un Actor autorizado continúa limitado por el ciclo de vida.

Debe mantenerse:

```text
Authorized Actor
    +
Invalid Lifecycle State

↓

Operation Rejected
```

---

# State Machine

La State Machine oficial se define en:

```text
DOMAIN-006B-State-Machine.md
```

Ningún privilegio técnico o administrativo permite ejecutar una
transición no definida.

Debe mantenerse:

```text
Permission
    ≠
State Machine Override
```

---

# Estados

Los estados oficiales son:

```text
Draft

Scheduled

Convoked

InProgress

Completed

Cancelled

Archived
```

El Security Model no introduce estados adicionales.

Las reglas de seguridad tampoco modifican la semántica de estos
estados.

---

# Draft

Una Assembly en:

```text
Draft
```

continúa sujeta exclusivamente a las operaciones permitidas para
dicho estado.

Un Permission no permite ejecutar directamente una operación propia
de un estado posterior cuando la State Machine lo prohíbe.

---

# Scheduled

Una Assembly en:

```text
Scheduled
```

solo puede ejecutar las operaciones autorizadas por su State
Machine y sus invariantes.

El actor debe poseer además el Permission requerido para la
operación correspondiente.

---

# Convoked

Una Assembly en:

```text
Convoked
```

mantiene las restricciones propias de dicho estado.

La existencia de Permission no elimina las condiciones necesarias
para iniciar la reunión.

---

# InProgress

Una Assembly en:

```text
InProgress
```

solo puede evolucionar según las reglas definidas en su Lifecycle y
State Machine.

Un actor autorizado no puede reescribir arbitrariamente estados
anteriores.

---

# Completed

Una Assembly en:

```text
Completed
```

representa una reunión formalmente finalizada.

La autorización no permite transformar este hecho consumado en un
estado incompatible con el Lifecycle oficial.

---

# Cancelled

Una Assembly en:

```text
Cancelled
```

mantiene las restricciones definidas para la cancelación.

Debe mantenerse:

```text
Cancelled
    ≠
Temporarily Paused
```

cuando el modelo oficial no defina dicha equivalencia.

La autorización no permite continuar normalmente hacia
InProgress.

---

# Archived

Una Assembly en:

```text
Archived
```

es inmutable conforme a las invariantes oficiales.

Debe mantenerse:

```text
Permission
    ≠
Archived Override
```

Un Permission elevado no permite modificar arbitrariamente una
Assembly archivada.

---

# Seguridad e Invariantes

Toda operación autorizada continúa sujeta a:

```text
DOMAIN-006E-Invariants.md
```

Una invariante nunca puede deshabilitarse por:

* Role;
* Permission;
* privilegio administrativo;
* privilegio técnico;
* acceso a Infrastructure.

Debe mantenerse:

```text
High Privilege
    ≠
Invariant Bypass
```

---

# Seguridad y Versioning

Versioning se define en:

```text
DOMAIN-006I-Versioning.md
```

Toda modificación concurrente debe respetar el modelo establecido.

Un Actor autorizado no puede ignorar un conflicto de Version.

Debe mantenerse:

```text
Authorization
    ≠
Concurrency Override
```

---

# ExpectedVersion

Cuando una operación requiere control de concurrencia debe respetar:

```text
ExpectedVersion
```

frente a:

```text
PersistedVersion
```

según el contrato oficial.

Si las versiones son incompatibles, la operación debe rechazarse
aunque el Actor posea Permission.

---

# Seguridad y Repository

El Repository se define en:

```text
DOMAIN-006G-Repository-Contract.md
```

El acceso técnico al Repository no constituye Permission de
dominio.

Debe mantenerse:

```text
Repository Access
    ≠
Domain Authority
```

---

# Persistencia

La base de datos no representa el Security Model del Aggregate.

Las restricciones de persistencia pueden reforzar integridad
técnica.

No sustituyen:

* Commands;
* Permissions;
* State Machine;
* invariantes;
* Versioning.

---

# Modificación Directa de Persistencia

Una escritura directa sobre persistencia que evite el Aggregate no
constituye una operación válida del dominio.

Debe mantenerse:

```text
Direct Database Mutation
    ≠
Valid Assembly Operation
```

---

# Consistency Boundary

El Consistency Boundary se define en:

```text
DOMAIN-006J-Consistency-Boundary.md
```

Los Permissions de Assembly se limitan a las operaciones propias de
Assembly.

No se propagan automáticamente a otros Aggregates.

---

# Regla de No Propagación

Debe mantenerse:

```text
Permission on Assembly
    ≠
Permission on Organization
```

```text
Permission on Assembly
    ≠
Permission on Territory
```

```text
Permission on Assembly
    ≠
Permission on Proposal
```

```text
Permission on Assembly
    ≠
Permission on Participation
```

```text
Permission on Assembly
    ≠
Permission on Voting
```

```text
Permission on Assembly
    ≠
Permission on Document
```

```text
Permission on Assembly
    ≠
Permission on Notification
```

Cada Aggregate mantiene sus propias reglas.

---

# Organization

Assembly referencia Organization mediante:

```text
OrganizationId
```

Una operación sobre Assembly no modifica:

* OrganizationName;
* OrganizationStatus;
* OrganizationPolicies;
* OrganizationSettings;
* Territory de Organization.

Estas responsabilidades corresponden al Aggregate Organization.

---

# Territory

Assembly referencia Territory mediante:

```text
TerritoryId
```

cuando corresponda.

Una operación sobre Assembly no modifica:

* TerritoryName;
* TerritoryType;
* TerritoryStatus;
* ParentTerritoryId;
* GeometryReference.

---

# Membership

Assembly puede relacionarse con Membership mediante identidad.

Un Permission sobre Assembly no concede capacidad para:

* crear Membership;
* aprobar Membership;
* activar Membership;
* suspender Membership;
* terminar Membership.

---

# Role

Assembly no administra Role.

Una operación autorizada sobre Assembly no puede utilizarse para
modificar:

* RoleName;
* RoleCode;
* RoleStatus;
* asignaciones de Role.

---

# Proposal

Proposal permanece bajo su propio Aggregate.

La relación contextual con Assembly no concede autoridad para:

* crear Proposal;
* modificar Proposal;
* cambiar su estado;
* alterar sus invariantes.

---

# Participation

Participation mantiene sus propias reglas.

Assembly no administra directamente la autorización interna de
Participation.

La coexistencia dentro de una reunión no fusiona sus modelos de
seguridad.

---

# Voting

Voting mantiene:

* identidad;
* Lifecycle;
* State Machine;
* invariantes;
* Permissions;

propios.

Un Permission de Assembly no autoriza automáticamente:

* crear Voting;
* abrir Voting;
* emitir votos;
* cambiar resultados;
* finalizar Voting.

---

# Document

Document mantiene su propio Aggregate.

Un Permission de Assembly no concede automáticamente autorización
para:

* crear Documents;
* modificar contenido;
* publicar Documents;
* archivar Documents.

---

# Notification

Notification permanece fuera del Aggregate.

Assembly puede producir hechos que originen procesos de
Notification.

No administra:

* canales;
* entrega;
* proveedores;
* reintentos;
* credenciales del proveedor.

---

# Audit

Audit mantiene su propia responsabilidad.

Assembly puede producir información utilizada para trazabilidad.

Assembly no modifica directamente registros de Audit.

---

# Trazabilidad

El modelo debe permitir identificar conceptualmente, cuando
corresponda:

```text
ActorId

AssemblyId

OrganizationId

CommandId

Timestamp

CorrelationId

CausationId
```

La trazabilidad permite relacionar la intención, el Aggregate y los
hechos resultantes.

No convierte estos datos en mecanismos de autorización.

---

# Domain Events

Los Domain Events oficiales se definen en:

```text
DOMAIN-006D-Domain-Events.md
```

Un Domain Event representa un hecho consumado.

No debe existir un evento de éxito cuando una operación fue
rechazada.

Debe mantenerse:

```text
Rejected Operation
    ≠
Successful Domain Event
```

---

# Integridad de Domain Events

Un Domain Event debe corresponder a una modificación válidamente
confirmada.

Ejemplo:

```text
AssemblyStarted
```

solo puede existir cuando Assembly alcanzó válidamente:

```text
InProgress
```

---

# Actor en Domain Events

Cuando un contrato de evento requiera identificar al actor puede
utilizar:

```text
ActorId
```

como referencia.

ActorId dentro del evento representa trazabilidad.

No representa una credencial reutilizable.

---

# Integration Events

Los Integration Events oficiales se definen en:

```text
DOMAIN-006K-Integration-Events.md
```

Un Integration Event comunica hechos fuera del límite
correspondiente.

Los Integration Events no deben convertirse en contenedores de
credenciales.

---

# Información Mínima

Los Integration Events deben transportar únicamente la información
necesaria para su contrato.

Debe mantenerse:

```text
Integration Event

=

Relevant Fact
+
Required Context
```

No:

```text
Integration Event

=

Complete Security Context
```

---

# Credenciales en Integration Events

No está permitido transportar mediante Integration Events:

```text
Password

PasswordHash

AccessToken

RefreshToken

JWT

PrivateKey

APISecret

ClientSecret

SessionCredential
```

---

# Seguridad de Read Models

Los Read Models oficiales se definen en:

```text
DOMAIN-006L-Read-Model.md
```

Un Read Model representa información de consulta.

No concede autorización.

Debe mantenerse:

```text
Data Exists
    ≠
Actor May Read Data
```

---

# Exposición de Read Models

La información expuesta debe corresponder a las capacidades y
políticas aplicables al consumidor.

La autorización de lectura pertenece a la capa correspondiente.

Assembly no modifica su estado para ocultar información de
presentación.

---

# Minimización de Datos

Los Read Models no deben incorporar información innecesaria para su
propósito.

La optimización de consulta no justifica copiar datos sensibles de
otros Aggregates dentro de Assembly.

---

# Datos Personales

Assembly no debe absorber automáticamente información personal de
Citizen.

No debe almacenar como estado propio, por el solo hecho de existir
participación:

```text
NationalIdentifier

Email

PhoneNumber

Password

Authentication Data
```

Citizen mantiene su propio Aggregate.

---

# Credenciales

Assembly nunca almacena:

```text
Password

PasswordHash

AccessToken

RefreshToken

JWT

APIKey

ClientSecret

PrivateKey

SessionId
```

Estos elementos no pertenecen al modelo de dominio de Assembly.

---

# Secretos

Los secretos técnicos pertenecen a Infrastructure.

Debe mantenerse:

```text
Secret
    outside
Assembly
```

Assembly debe poder existir conceptualmente sin conocer cómo la
infraestructura almacena o protege secretos.

---

# Criptografía

Assembly no define:

* algoritmos de cifrado;
* algoritmos de hashing;
* longitudes de claves;
* certificados;
* rotación de claves;
* protocolos criptográficos;
* almacenamiento seguro de secretos.

Estas responsabilidades pertenecen a Infrastructure y a los
componentes de seguridad correspondientes.

---

# Sesiones

Assembly no administra sesiones.

No mantiene:

```text
SessionId

SessionExpiration

LoginTime

RefreshToken
```

La sesión pertenece al mecanismo de autenticación correspondiente.

---

# Tokens

Los tokens técnicos no constituyen Value Objects del Aggregate.

Debe mantenerse:

```text
Authentication Token
    ≠
Assembly Domain Value
```

---

# Transporte

Assembly permanece independiente del mecanismo por el cual una
operación llega a la aplicación.

No conoce:

```text
HTTP

HTTPS

REST

GraphQL

gRPC

Message Broker
```

La seguridad del transporte pertenece a Infrastructure.

---

# Infraestructura

Assembly no depende de tecnologías concretas de seguridad.

No depende conceptualmente de:

```text
OAuth

OAuth2

OpenID Connect

JWT

SAML

LDAP

Keycloak

Keyrock

PEP Proxy

TLS

mTLS
```

Estas tecnologías pueden implementar mecanismos de seguridad fuera
del Aggregate.

---

# Sistemas Municipales

Assembly no almacena credenciales utilizadas para acceder a
plataformas municipales.

La autenticación con dichos sistemas pertenece a Integration e
Infrastructure.

Debe mantenerse:

```text
Municipal Credentials
    outside
Assembly
```

---

# FIWARE

Assembly no administra:

* credenciales FIWARE;
* tokens FIWARE;
* usuarios FIWARE;
* políticas técnicas FIWARE;
* autenticación del Context Broker.

La integración se mantiene fuera del Aggregate.

Debe mantenerse:

```text
Assembly
    ≠
FIWARE Security Client
```

---

# Seguridad y Performance

Las reglas de rendimiento se definen en:

```text
DOMAIN-006N-Performance-Rules.md
```

Una optimización no puede eliminar controles de seguridad.

Debe mantenerse:

```text
Performance Optimization
    ≠
Security Bypass
```

---

# Seguridad y Caché

Una caché puede utilizarse para optimizar lectura según la
infraestructura.

No constituye autoridad para determinar por sí sola:

* identidad del Actor;
* Permission;
* Version autoritativa;
* estado transaccional actual.

---

# Fail Secure

Cuando una condición obligatoria de seguridad no puede resolverse
válidamente, la operación protegida debe rechazarse.

Conceptualmente:

```text
Required Security Condition
    =
Unknown or Unsatisfied

↓

Operation Rejected
```

---

# Permission Explícito

Cuando una operación requiere Permission, debe existir una
capacidad válida conforme al modelo correspondiente.

No debe asumirse Permission por ausencia de una denegación
explícita.

---

# Identificadores

Los identificadores de dominio no constituyen secretos.

Conocer:

```text
AssemblyId
```

no concede Permission.

Conocer:

```text
OrganizationId
```

no concede Permission.

Conocer:

```text
TerritoryId
```

no concede Permission.

Conocer:

```text
CitizenId
```

no concede Permission.

Debe mantenerse:

```text
Identifier Knowledge
    ≠
Authorization
```

---

# Seguridad por Oscuridad

El Security Model no depende de ocultar identificadores para
proteger Assembly.

La protección depende de:

* Authentication;
* Authorization;
* Permissions;
* State Machine;
* invariantes;
* Versioning;
* Consistency Boundary;
* seguridad técnica externa.

---

# Operaciones Administrativas

Una capacidad administrativa permite únicamente las operaciones
establecidas por los Permissions correspondientes.

No permite:

* modificar AssemblyId;
* modificar OrganizationId;
* modificar Version directamente;
* omitir State Machine;
* omitir invariantes;
* omitir Versioning;
* modificar otros Aggregates;
* reescribir hechos históricos.

Debe mantenerse:

```text
Administrative Permission
    ≠
Unlimited Domain Mutation
```

---

# Privilegio Técnico

Un actor con privilegios técnicos sobre la infraestructura no se
convierte automáticamente en un actor con autoridad ilimitada de
dominio.

Debe mantenerse:

```text
Infrastructure Privilege
    ≠
Domain Permission
```

---

# Seguridad de Programación

La modificación de:

```text
ScheduledStart

ScheduledEnd
```

debe respetar:

* Permission;
* estado permitido;
* invariantes temporales;
* Versioning.

La autorización no permite confirmar una programación inválida.

---

# Seguridad de Convocatoria

Modificar o ejecutar la convocatoria requiere:

* Permission correspondiente;
* estado compatible;
* condiciones de convocatoria;
* invariantes;
* Versioning.

La convocatoria no puede modificarse directamente evitando el
comportamiento del Aggregate.

---

# Seguridad de Modalidad

Modificar:

```text
AssemblyModality
```

requiere una operación autorizada.

El nuevo valor debe seguir siendo válido conforme a las reglas del
Aggregate.

---

# Seguridad de Ubicación

Modificar:

```text
Location
```

requiere autorización y debe respetar las reglas aplicables.

Location no concede autoridad sobre Territory.

---

# Seguridad del Nombre

Modificar:

```text
AssemblyName
```

requiere la operación y Permission correspondientes.

El cambio continúa sujeto al estado y las invariantes aplicables.

---

# Seguridad del Tipo

Modificar:

```text
AssemblyType
```

requiere autorización.

Un cambio de tipo no puede utilizarse para evitar restricciones
definidas por el Lifecycle o la State Machine.

---

# Seguridad del Propósito

Modificar:

```text
AssemblyPurpose
```

requiere una intención explícita y autorizada.

No debe modificarse mediante actualización directa de
persistencia.

---

# Seguridad de Inicio

Iniciar Assembly requiere conceptualmente:

```text
Authorized Actor

+

Required Permission

+

Valid Current State

+

Satisfied Start Conditions

+

Satisfied Invariants

↓

AssemblyStarted
```

La ausencia de cualquiera de las condiciones impide la transición.

---

# Seguridad de Finalización

Completar Assembly requiere:

```text
Authorized Actor

+

Required Permission

+

AssemblyStatus = InProgress

+

Satisfied Completion Conditions

+

Satisfied Invariants

↓

AssemblyCompleted
```

Permission no garantiza Completion.

---

# Seguridad de Cancelación

Cancelar Assembly requiere una operación explícita.

Conceptualmente:

```text
Authorized Actor

+

Required Permission

+

Valid Current State

+

Satisfied Invariants

↓

AssemblyCancelled
```

---

# Seguridad de Archivado

Archivar Assembly requiere:

* Permission correspondiente;
* estado permitido;
* invariantes satisfechas;
* Version válida.

Archived no representa eliminación física obligatoria.

---

# Seguridad de Hechos Históricos

Los Domain Events representan hechos consumados.

No deben modificarse retrospectivamente para ocultar o cambiar una
operación histórica.

Debe mantenerse:

```text
Historical Domain Event
    =
Immutable Fact
```

conforme al modelo de eventos oficial.

---

# Replay

Cuando Assembly se reconstruye mediante hechos históricos, Replay
no constituye una nueva operación autorizada.

Debe mantenerse:

```text
Replay
    ≠
New Command
```

y:

```text
Replay
    ≠
New Authorization
```

---

# Read Model Reconstruction

Reconstruir una proyección:

* no modifica Assembly;
* no incrementa Version;
* no concede Permissions;
* no ejecuta Commands;
* no modifica hechos históricos.

---

# Auditoría de Seguridad

Los intentos y operaciones relevantes pueden ser utilizados por
Audit.

Conceptualmente pueden existir referencias como:

```text
ActorId

AssemblyId

OrganizationId

CommandId

Timestamp

CorrelationId

CausationId

Result
```

cuando correspondan a los contratos oficiales.

Audit permanece fuera del Aggregate Assembly.

---

# Operaciones Rechazadas y Audit

Una operación rechazada puede resultar relevante para Audit.

Esto no significa que deba producir un Domain Event de cambio de
Assembly.

Debe mantenerse:

```text
Security Audit Fact
    ≠
Assembly State Change
```

---

# Repetición de Commands

La repetición de un Command no implica que la operación continúe
siendo válida.

El estado puede haber cambiado.

Los Permissions pueden haber cambiado.

Version puede haber cambiado.

Debe mantenerse:

```text
Previously Valid
    ≠
Currently Valid
```

---

# Cambio de Permissions

Assembly no almacena una copia permanente de las capacidades
externas de un Actor como mecanismo para evitar su evaluación.

Las operaciones futuras deben utilizar el contexto de autorización
vigente según el modelo correspondiente.

---

# Revocación

La revocación de Permission pertenece al contexto de autorización.

Assembly no administra el ciclo de vida de los Permissions.

Una capacidad previamente disponible puede no estar disponible para
una operación posterior.

---

# Consistencia Eventual y Seguridad

La consistencia eventual entre Aggregates no elimina la necesidad de
contar con información suficientemente válida para una decisión de
autorización.

Debe mantenerse:

```text
Eventually Consistent Domain Collaboration
    ≠
Automatic Security Approval
```

La coordinación necesaria pertenece a las capas correspondientes.

---

# Security Context

Una operación puede mantener conceptualmente contexto como:

```text
ActorId

OrganizationId

Required Permission

CorrelationId

CausationId
```

cuando corresponda.

Este contexto no constituye automáticamente estado persistente de
Assembly.

---

# No Persistencia de Authentication Context

Assembly no almacena permanentemente:

```text
Authentication Session

Access Token

Refresh Token

Authentication Claims

Authentication Provider State
```

como parte de su estado.

Debe mantenerse:

```text
Authentication Context
    ≠
Assembly State
```

---

# Casos de Uso Conceptuales

El Security Model permite verificar conceptualmente:

```text
Autorizar creación de Assembly.

Autorizar programación de Assembly.

Autorizar reprogramación.

Autorizar convocatoria.

Autorizar actualización de convocatoria.

Autorizar inicio.

Autorizar finalización.

Autorizar cancelación.

Autorizar archivado.

Autorizar cambios de nombre.

Autorizar cambios de propósito.

Autorizar cambios de tipo.

Autorizar cambios de modalidad.

Autorizar cambios de ubicación.

Rechazar operaciones sin Permission.

Rechazar operaciones fuera del contexto organizacional.

Rechazar operaciones incompatibles con el estado.

Rechazar operaciones que violen invariantes.

Rechazar modificaciones concurrentes incompatibles.
```

---

# Escenario — Operación Autorizada y Válida

```text
Given

un Actor autenticado

And

el Actor posee el Permission requerido

And

la Assembly pertenece al contexto organizacional autorizado

And

el estado actual permite la operación

And

las invariantes se encuentran satisfechas

And

Version es válida

When

se ejecuta el Command correspondiente

Then

Assembly puede aceptar la modificación

And

Version cambia conforme al modelo oficial

And

se produce el Domain Event correspondiente
```

---

# Escenario — Permission Insuficiente

```text
Given

un Actor que no posee el Permission requerido

When

intenta ejecutar un Command protegido

Then

la operación es rechazada

And

Assembly permanece sin cambios

And

Version permanece sin cambios

And

no se produce Domain Event de éxito
```

---

# Escenario — Actor No Autenticado

```text
Given

una operación que requiere un Actor autenticado

And

no existe una identidad autenticada válida

When

se intenta ejecutar la operación protegida

Then

la solicitud no alcanza válidamente el comportamiento protegido de
Assembly
```

---

# Escenario — Permission Válido e Invariante Violada

```text
Given

un Actor autorizado

And

el Actor posee el Permission requerido

But

la operación viola una invariante

When

el Command es evaluado

Then

Assembly rechaza la operación

And

el estado permanece sin cambios
```

---

# Escenario — Permission Válido y Estado Inválido

```text
Given

un Actor autorizado para iniciar una Assembly

And

AssemblyStatus = Draft

When

intenta ejecutar StartAssembly

Then

la operación es rechazada

Because

Permission no sustituye State Machine
```

---

# Escenario — Contexto Organizacional Incorrecto

```text
Given

Assembly pertenece a Organization A

And

el Actor posee autoridad únicamente en Organization B

When

intenta ejecutar una operación protegida sobre Assembly

Then

la operación es rechazada

And

Assembly permanece sin cambios
```

---

# Escenario — Conocimiento del Identificador

```text
Given

un Actor conoce un AssemblyId válido

And

no posee Permission sobre la Assembly

When

intenta modificarla

Then

la operación es rechazada

Because

AssemblyId no constituye autorización
```

---

# Escenario — Conflicto de Version

```text
Given

un Actor autorizado

And

ExpectedVersion es diferente de PersistedVersion

When

intenta confirmar una modificación

Then

la modificación es rechazada

And

el Permission no elimina el conflicto de concurrencia
```

---

# Escenario — Privilegio Técnico

```text
Given

un operador posee acceso técnico a Infrastructure

But

no posee Permission de dominio sobre Assembly

When

interactúa con el modelo de dominio

Then

su privilegio técnico no se interpreta como autoridad sobre
Assembly
```

---

# Escenario — Permission no se Propaga

```text
Given

un Actor posee Permission para modificar Assembly

And

Assembly se encuentra relacionada con Voting

When

el Actor modifica Assembly

Then

ese Permission no autoriza automáticamente modificar Voting
```

---

# Escenario — Read Model Restringido

```text
Given

un Read Model contiene información de Assembly

And

un consumidor no se encuentra autorizado para acceder a toda la
información

When

la consulta es procesada

Then

la capa correspondiente expone únicamente la información autorizada
```

---

# Escenario — Integration Event Seguro

```text
Given

Assembly produce un hecho confirmado

When

se genera el Integration Event correspondiente

Then

el contrato contiene únicamente la información necesaria

And

no contiene credenciales

And

no contiene secretos

And

no expone el Aggregate completo por defecto
```

---

# Escenario — Credencial de Integración

```text
Given

una integración externa requiere una credencial técnica

When

la infraestructura ejecuta la integración

Then

la credencial permanece fuera de Assembly
```

---

# Escenario — Operación Rechazada

```text
Given

una operación falla por autorización

When

la operación es rechazada

Then

no existe modificación parcial

And

Version permanece sin cambios

And

no existe Domain Event de éxito
```

---

# Escenario — Archived

```text
Given

AssemblyStatus = Archived

And

un Actor posee un Permission administrativo

When

intenta modificar Assembly

Then

la operación continúa sujeta a las invariantes de Archived

And

el Permission no permite ignorar la inmutabilidad
```

---

# Escenario — Cross Aggregate

```text
Given

un cambio autorizado ocurre en Assembly

And

el hecho requiere una reacción de Notification

When

Assembly confirma la modificación

Then

Assembly produce el hecho correspondiente

And

Notification procesa su propia responsabilidad fuera de Assembly

And

Assembly no modifica Notification directamente
```

---

# Escenario — Replay

```text
Given

Assembly debe reconstruirse desde hechos históricos

When

se ejecuta Replay

Then

el estado se reconstruye

And

Replay no constituye una nueva autorización

And

Replay no produce una nueva intención de dominio
```

---

# Amenazas Conceptuales

El modelo debe prevenir conceptualmente:

```text
Unauthorized State Mutation

Cross-Organization Mutation

Permission Bypass

Invariant Bypass

State Machine Bypass

Version Bypass

Direct Aggregate Mutation

Credential Leakage

Cross-Aggregate Authority Propagation

Unauthorized Read Exposure

Historical Fact Manipulation
```

Estas amenazas describen situaciones incompatibles con el modelo
DDD de Assembly.

Los mecanismos técnicos concretos para prevenirlas pertenecen a las
capas correspondientes.

---

# Unauthorized State Mutation

Toda modificación del estado de Assembly debe producirse mediante
una operación autorizada y válida.

Una modificación directa evita las protecciones del Aggregate y no
constituye comportamiento válido.

---

# Cross-Organization Mutation

La autoridad de una Organization no debe utilizarse para modificar
Assemblies pertenecientes a otro contexto organizacional cuando la
operación no se encuentre explícitamente autorizada.

---

# Permission Bypass

No está permitido ejecutar comportamiento protegido evitando la
validación del Permission correspondiente.

---

# Invariant Bypass

No existe una autorización válida para dejar Assembly en un estado
que viole sus invariantes.

---

# State Machine Bypass

No está permitido modificar AssemblyStatus directamente para evitar
las transiciones oficiales.

Debe mantenerse:

```text
State Change

↓

State Machine
```

---

# Version Bypass

No está permitido ignorar Version para sobrescribir cambios
concurrentes incompatibles.

---

# Direct Aggregate Mutation

No deben existir mecanismos públicos que permitan modificar los
atributos internos sin ejecutar comportamiento de Assembly.

---

# Credential Leakage

No deben incorporarse credenciales dentro de:

* Aggregate;
* entidades internas;
* Value Objects;
* Domain Events;
* Integration Events;
* Read Models;
* estado persistente conceptual.

---

# Cross-Aggregate Authority Propagation

La autoridad sobre Assembly no se propaga automáticamente a otros
Aggregates.

---

# Unauthorized Read Exposure

La existencia de una proyección no significa que todo Actor pueda
consultarla íntegramente.

---

# Historical Fact Manipulation

Los hechos históricos no deben alterarse para ocultar operaciones
previas.

La trazabilidad requiere preservar su integridad.

---

# Reglas de Seguridad

El Security Model establece como mínimo:

* toda operación protegida requiere autorización;
* los Permissions se utilizan conforme a
  DOMAIN-006F-Permissions.md;
* Authentication permanece fuera de Assembly;
* Assembly no almacena credenciales;
* Assembly no almacena sesiones;
* Assembly no administra tokens;
* Permission no sustituye State Machine;
* Permission no sustituye invariantes;
* Permission no sustituye Versioning;
* Permission sobre Assembly no concede Permission sobre otros
  Aggregates;
* OrganizationId mantiene el contexto organizacional;
* conocer AssemblyId no concede autoridad;
* una operación rechazada no modifica Assembly;
* una operación rechazada no incrementa Version;
* una operación rechazada no genera Domain Event de éxito;
* los Domain Events representan hechos confirmados;
* Integration Events minimizan la información expuesta;
* Read Models respetan las reglas de acceso;
* Infrastructure administra secretos;
* privilegios técnicos no equivalen a autoridad de dominio;
* Audit permanece fuera del Aggregate;
* la seguridad no modifica el Consistency Boundary.

---

# Restricciones

No está permitido:

* autenticar usuarios dentro de Assembly;
* administrar credenciales dentro de Assembly;
* almacenar passwords;
* almacenar password hashes;
* almacenar Access Tokens;
* almacenar Refresh Tokens;
* almacenar JWT;
* almacenar API Keys;
* almacenar Client Secrets;
* almacenar Private Keys;
* almacenar sesiones;
* modificar Assembly sin pasar por la Aggregate Root;
* modificar Assembly sin el Permission requerido;
* utilizar Permission para evitar invariantes;
* utilizar Permission para evitar State Machine;
* utilizar Permission para evitar Versioning;
* utilizar privilegios técnicos como autoridad de dominio;
* modificar AssemblyId;
* modificar OrganizationId;
* modificar Version directamente;
* propagar autoridad implícitamente hacia otros Aggregates;
* modificar Organization desde Assembly;
* modificar Territory desde Assembly;
* modificar Citizen desde Assembly;
* modificar Membership desde Assembly;
* modificar Role desde Assembly;
* modificar Proposal desde Assembly;
* modificar Participation desde Assembly;
* modificar Voting desde Assembly;
* modificar Document desde Assembly;
* modificar Notification desde Assembly;
* modificar Audit desde Assembly;
* exponer credenciales mediante Domain Events;
* exponer credenciales mediante Integration Events;
* exponer secretos mediante Read Models;
* considerar AssemblyId una credencial;
* utilizar una proyección como mecanismo de autorización;
* utilizar una caché como autoridad de Permission;
* modificar hechos históricos;
* introducir una tecnología de seguridad como parte del Aggregate.

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
Domain Invariants
```

```text
Permission
    ≠
Guaranteed Operation
```

```text
Permission
    ≠
State Machine Override
```

```text
Permission
    ≠
Invariant Bypass
```

```text
Permission
    ≠
Version Override
```

```text
Technical Privilege
    ≠
Domain Authority
```

```text
Identifier
    ≠
Credential
```

```text
Repository Access
    ≠
Domain Permission
```

```text
Permission on Assembly
    ≠
Permission on External Aggregate
```

```text
Security Context
    ≠
Aggregate State
```

```text
Read Model
    ≠
Authorization Model
```

```text
Integration Event
    ≠
Credential Container
```

```text
Infrastructure Security
    ≠
Domain Security Rules
```

```text
Rejected Operation
    =
No Domain Mutation
```

Estas separaciones preservan los límites conceptuales de Assembly.

---

# Compatibilidad Arquitectónica

El Security Model es compatible con:

* Domain-Driven Design;
* Aggregate Pattern;
* Clean Architecture;
* Hexagonal Architecture;
* CQRS;
* Event-Driven Architecture;
* Event Sourcing Compatible;
* Optimistic Concurrency;
* arquitectura distribuida;
* principio de mínimo privilegio;
* aislamiento organizacional;
* separación entre autenticación, autorización y dominio.

La compatibilidad no introduce tecnologías concretas dentro del
Aggregate.

---

# Relación con DOMAIN-006-Aggregate

`DOMAIN-006-Aggregate.md` constituye la fuente conceptual oficial de
Assembly.

Este Security Model protege ese modelo.

No puede redefinir:

* identidad;
* responsabilidades;
* relaciones;
* Lifecycle;
* estado;
* invariantes;
* Consistency Boundary.

---

# Relación con Lifecycle

`DOMAIN-006A-Lifecycle.md` define el ciclo de vida oficial.

Ningún Permission puede crear una transición no contemplada por el
Lifecycle.

---

# Relación con State Machine

`DOMAIN-006B-State-Machine.md` define las transiciones permitidas.

Authorization determina quién puede intentar una transición.

State Machine determina si puede producirse desde el estado actual.

---

# Relación con Commands

`DOMAIN-006C-Commands.md` define las intenciones oficiales de
modificación.

Las reglas de seguridad determinan las condiciones de acceso que
deben cumplirse para ejecutar los Commands protegidos.

---

# Relación con Domain Events

`DOMAIN-006D-Domain-Events.md` define los hechos consumados.

Un Domain Event de éxito solo puede existir después de una operación
válidamente autorizada y aceptada por el dominio.

---

# Relación con Invariants

`DOMAIN-006E-Invariants.md` define las reglas obligatorias.

Permissions nunca sustituyen ni debilitan estas reglas.

---

# Relación con Permissions

`DOMAIN-006F-Permissions.md` constituye la fuente oficial de las
capacidades aplicables sobre Assembly.

El Security Model utiliza esos Permissions.

No introduce una lista alternativa de capacidades.

---

# Relación con Repository Contract

`DOMAIN-006G-Repository-Contract.md` define persistencia y
rehidratación.

El acceso técnico al Repository no concede Permission sobre el
Aggregate.

---

# Relación con Examples

`DOMAIN-006H-Examples.md` documenta escenarios conceptuales.

Las reglas de seguridad deben preservar el comportamiento allí
establecido.

---

# Relación con Versioning

`DOMAIN-006I-Versioning.md` define la concurrencia optimista.

Un Actor autorizado continúa sujeto a los conflictos de Version.

---

# Relación con Consistency Boundary

`DOMAIN-006J-Consistency-Boundary.md` define el límite de
consistencia.

La autorización sobre Assembly no se propaga automáticamente fuera
de dicho límite.

---

# Relación con Integration Events

`DOMAIN-006K-Integration-Events.md` define contratos externos.

Dichos contratos no deben transportar credenciales técnicas ni
información innecesaria.

---

# Relación con Read Model

`DOMAIN-006L-Read-Model.md` define proyecciones de lectura.

Las proyecciones deben exponer únicamente información autorizada
para cada contexto de consumo.

---

# Relación con Test Scenarios

`DOMAIN-006M-Test-Scenarios.md` define escenarios conceptuales de
verificación.

Las pruebas deben verificar tanto operaciones autorizadas como
rechazos por seguridad.

---

# Relación con Performance Rules

`DOMAIN-006N-Performance-Rules.md` define las reglas de rendimiento.

Ninguna optimización puede eliminar una protección establecida por
este Security Model.

---

# Regla de Coherencia Documental

El Security Model debe mantenerse coherente con:

```text
DOMAIN-006-Aggregate.md

DOMAIN-006A-Lifecycle.md

DOMAIN-006B-State-Machine.md

DOMAIN-006C-Commands.md

DOMAIN-006D-Domain-Events.md

DOMAIN-006E-Invariants.md

DOMAIN-006F-Permissions.md

DOMAIN-006G-Repository-Contract.md

DOMAIN-006H-Examples.md

DOMAIN-006I-Versioning.md

DOMAIN-006J-Consistency-Boundary.md

DOMAIN-006K-Integration-Events.md

DOMAIN-006L-Read-Model.md

DOMAIN-006M-Test-Scenarios.md

DOMAIN-006N-Performance-Rules.md
```

Este documento no puede introducir silenciosamente:

* nuevos estados;
* nuevas transiciones;
* nuevos Commands;
* nuevos Domain Events;
* nuevos Permissions;
* nuevas invariantes;
* nuevas Aggregate Roots;
* nuevos Aggregates;
* nuevas relaciones de propiedad;
* nuevas responsabilidades del dominio;
* tecnologías obligatorias de seguridad.

---

# Regla de Evolución

El Security Model puede evolucionar cuando existan nuevas
necesidades conceptuales de protección del dominio.

Toda evolución debe preservar:

* identidad de Assembly;
* Aggregate Root;
* Lifecycle;
* State Machine;
* invariantes;
* Permissions;
* Versioning;
* Consistency Boundary;
* lenguaje ubicuo;
* independencia tecnológica.

Las tecnologías utilizadas para Authentication, criptografía,
gestión de secretos, transporte o proveedores de identidad pueden
evolucionar independientemente sin redefinir Assembly.

---

# Definición de Éxito

El **Security Model** del Aggregate **Assembly** constituye el
modelo conceptual oficial para proteger las operaciones, el estado
y la información de una Asamblea sin introducir dentro del
Aggregate responsabilidades pertenecientes a autenticación,
credenciales, sesiones, criptografía o infraestructura.

Authentication determina quién es el Actor.

Authorization determina si el Actor puede intentar una operación.

Permissions expresan las capacidades aplicables a Assembly.

State Machine determina si la transición corresponde al estado
actual.

Domain Invariants determinan si el resultado preserva las reglas
del dominio.

Versioning protege el Aggregate frente a modificaciones concurrentes
incompatibles.

Estas responsabilidades permanecen separadas y complementarias.

Un Actor autorizado no puede utilizar un Permission para omitir:

* Lifecycle;
* State Machine;
* invariantes;
* Versioning;
* Consistency Boundary.

Una operación rechazada mantiene el estado del Aggregate sin
cambios, no incrementa Version y no produce Domain Events que
representen hechos inexistentes.

Assembly conserva OrganizationId como contexto organizacional
inmutable y las capacidades deben respetar dicho contexto.

Conocer AssemblyId, OrganizationId, TerritoryId o cualquier otro
identificador de dominio no concede autoridad.

Organization, Territory, Citizen, Membership, Role, Proposal,
Participation, Voting, Document, Notification y Audit mantienen sus
propias responsabilidades, límites de consistencia y modelos de
seguridad.

Un Permission sobre Assembly no concede Permission implícito sobre
ninguno de ellos.

Assembly nunca almacena:

```text
Passwords

Password Hashes

Access Tokens

Refresh Tokens

JWT

API Keys

Client Secrets

Private Keys

Session Credentials
```

Las credenciales, secretos, protocolos de autenticación y
mecanismos criptográficos permanecen fuera del Aggregate.

Los Domain Events representan únicamente hechos válidamente
confirmados.

Los Integration Events transportan únicamente la información
necesaria para interoperabilidad y no se utilizan como contenedores
de credenciales.

Los Read Models exponen únicamente la información autorizada para
cada contexto y no constituyen mecanismos de autorización.

Los privilegios técnicos sobre bases de datos, infraestructura,
Frameworks o sistemas externos no equivalen a autoridad dentro del
dominio.

Debe mantenerse permanentemente:

```text
Authentication

↓

Authorization

↓

Permission

↓

Command

↓

Assembly

↓

State Machine

↓

Domain Invariants

↓

Versioning

↓

Valid State Change

↓

Domain Events
```

sin convertir:

```text
Security Infrastructure
```

en:

```text
Assembly Domain Model
```

De esta forma,
**DOMAIN-006O-Security-Model.md** establece el modelo conceptual y
normativo oficial de seguridad del Aggregate Assembly, preservando
la separación entre Authentication, Authorization, Permissions y
Domain Invariants, protegiendo su estado, su Lifecycle, su
Consistency Boundary y su independencia tecnológica conforme a los
principios Domain-Driven Design establecidos para AURA Core.