# DOMAIN-011O — Notification Security Model

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Notification Management

Aggregate:
Notification

Documentos relacionados:

- DOMAIN-011-Aggregate.md
- DOMAIN-011C-Commands.md
- DOMAIN-011D-Domain-Events.md
- DOMAIN-011E-Invariants.md
- DOMAIN-011F-Permissions.md
- DOMAIN-011G-Repository-Contract.md
- DOMAIN-011I-Versioning.md
- DOMAIN-011J-Consistency-Boundary.md
- DOMAIN-011K-Integration-Events.md
- DOMAIN-011L-Read-Model.md
- DOMAIN-011N-Performance-Rules.md

---

# Objetivo

Este documento define el Security Model conceptual del Aggregate
**Notification**.

Su propósito es establecer las reglas que protegen la integridad,
confidencialidad, trazabilidad y acceso autorizado a Notification
sin introducir dentro del Aggregate responsabilidades propias de
Authentication, Infrastructure o mecanismos criptográficos
concretos.

El Security Model protege las reglas del dominio.

No sustituye:

- Lifecycle;
- State Machine;
- Invariants;
- Permissions;
- Versioning;
- Consistency Boundary.

---

# Principio Fundamental

Ninguna decisión de seguridad puede permitir que una operación
viole el dominio.

Debe mantenerse:

```text
Authorized

≠

Automatically Valid
```

y:

```text
Security Mechanism

≠

Domain Rule
```

El Aggregate continúa siendo responsable de validar:

- estado actual;
- transición;
- Invariants;
- Version;
- consistencia interna.

---

# Alcance

El Security Model de Notification protege conceptualmente:

```text
NotificationId

NotificationStatus

Version

CreatedAt

UpdatedAt

Domain State

Domain Events

External References
```

y cualquier elemento interno oficialmente definido dentro del
Aggregate.

La protección física o tecnológica pertenece a Infrastructure.

---

# Separación de Responsabilidades

Debe mantenerse separación entre:

```text
Authentication

Authorization

Domain Validation

Infrastructure Security
```

Cada responsabilidad pertenece a su capa o contexto correspondiente.

Notification no debe absorberlas como una única responsabilidad.

---

# Authentication

Notification no autentica actores.

El Aggregate no:

- valida contraseñas;
- valida tokens;
- crea sesiones;
- mantiene sesiones;
- administra proveedores de identidad;
- gestiona certificados;
- administra OAuth;
- administra JWT.

Debe mantenerse:

```text
Authentication

∉

Notification Aggregate
```

---

# Authorization

La autorización se resuelve antes de ejecutar un Command sobre
Notification.

Conceptualmente:

```text
Actor

↓

Authentication

↓

Authorization

↓

Command

↓

Notification
```

La definición conceptual de Permissions pertenece a:

```text
DOMAIN-011F-Permissions.md
```

Notification no mantiene una matriz interna de usuarios y
permisos.

---

# Domain Validation

Después de una autorización válida, Notification todavía debe
validar:

- estado;
- State Machine;
- Invariants;
- Version;
- Consistency Boundary.

Debe mantenerse:

```text
Authorization Passed

↓

Domain Validation Required
```

Nunca:

```text
Authorization Passed

↓

Direct State Mutation
```

---

# Deny by Default

Toda capacidad que no haya sido explícitamente autorizada debe
considerarse no permitida.

Debe mantenerse:

```text
No Explicit Permission

↓

Denied
```

Este principio no introduce nuevos Commands ni Roles dentro del
Aggregate.

---

# Least Privilege

Los actores y procesos deben recibir únicamente las capacidades
necesarias para ejecutar las operaciones que les correspondan.

Debe mantenerse:

```text
Required Capability

=

Minimum Authorized Capability
```

La política concreta permanece fuera de Notification.

---

# Commands Protegidos

Los Commands oficiales:

```text
CreateNotification

QueueNotification

ConfirmNotificationDelivery

ReportNotificationDeliveryFailure

RetryNotification
```

requieren autorización previa conforme a la política aplicable.

Ningún Command obtiene autoridad para evitar las Invariants.

---

# Modificación Directa Prohibida

Ningún actor, proceso o mecanismo técnico puede modificar
directamente:

```text
NotificationId

NotificationStatus

Version

CreatedAt

UpdatedAt
```

cuando dichos valores estén protegidos por las reglas del
Aggregate.

Toda modificación válida debe atravesar comportamiento explícito de:

```text
Notification
```

---

# Protección de NotificationId

NotificationId:

- identifica el Aggregate;
- es obligatorio;
- permanece inmutable;
- no puede reasignarse;
- no puede utilizarse para fusionar Aggregates distintos.

Debe mantenerse:

```text
NotificationId at Creation

=

NotificationId for Entire Lifecycle
```

---

# Protección del Estado

NotificationStatus solamente puede cambiar mediante transiciones
válidas.

No está permitido:

```text
Direct Set Status
```

aunque el actor tenga autorización general sobre Notification.

Debe mantenerse:

```text
Permission

≠

State Machine Bypass
```

---

# Protección de Version

Version protege la evolución lógica y la concurrencia del
Aggregate.

No puede:

- modificarse arbitrariamente;
- disminuir;
- reiniciarse durante Retry;
- incrementarse por una operación rechazada.

Debe mantenerse:

```text
ExpectedVersion

=

PersistedVersion
```

antes de confirmar una escritura compatible.

---

# Concurrencia como Protección

Optimistic Concurrency Control protege contra sobrescritura
silenciosa de modificaciones confirmadas.

Si:

```text
ExpectedVersion

≠

PersistedVersion
```

debe producirse:

```text
ConcurrencyConflict
```

Una escritura obsoleta no puede reemplazar una escritura ya
confirmada.

---

# Protección de Invariants

Ningún mecanismo externo puede evitar:

```text
DOMAIN-011E-Invariants.md
```

Las Invariants deben cumplirse:

```text
Before Operation

AND

After Operation
```

Si no pueden preservarse:

```text
Operation

↓

Rejected
```

---

# Protección del Lifecycle

El Security Model no crea estados adicionales.

Los únicos estados oficiales permanecen:

```text
Draft

Pending

Delivered

Failed
```

No pueden incorporarse mediante una política de seguridad:

```text
Archived

Cancelled

Deleted
```

como estados del Aggregate versión 1.0.

---

# Delivered

Delivered permanece terminal independientemente de quién solicite
una nueva operación.

Un actor con privilegios elevados no puede realizar:

```text
Delivered → Pending
```

ni:

```text
Delivered → Failed
```

mediante una operación ordinaria.

Debe mantenerse:

```text
Privilege

≠

Lifecycle Override
```

---

# Failed y Retry

Una Notification Failed solamente puede reingresar mediante:

```text
RetryNotification
```

produciendo:

```text
Failed → Pending
```

Un actor autorizado no puede convertir directamente:

```text
Failed → Delivered
```

---

# Credenciales

Notification nunca almacena:

- passwords;
- access tokens;
- refresh tokens;
- API keys;
- private keys;
- secrets;
- credentials;
- session identifiers con semántica de autenticación.

Debe mantenerse:

```text
Credentials

∉

Notification Aggregate
```

---

# Secretos

Ningún secreto técnico pertenece al estado de Notification.

Los secretos necesarios para:

- proveedores de email;
- proveedores SMS;
- Push Providers;
- APIs externas;
- FIWARE;
- sistemas municipales;

permanecen fuera del Aggregate.

---

# Canal y Seguridad

Un canal de Notification es un concepto de dominio.

No contiene automáticamente:

- credenciales del proveedor;
- endpoints privados;
- secretos;
- certificados;
- configuración técnica sensible.

Debe mantenerse:

```text
Notification Channel

≠

Provider Security Configuration
```

---

# Proveedor Externo

Un proveedor externo no recibe autoridad sobre el Aggregate.

Puede producir información que posteriormente sea interpretada por
Application y convertida en una intención válida.

Conceptualmente:

```text
External Provider

↓

Adapter / Application

↓

Command

↓

Notification
```

Nunca:

```text
External Provider

↓

Direct Notification Mutation
```

---

# Confirmación de Entrega

Un resultado técnico solamente puede modificar el dominio después
de atravesar el comportamiento correspondiente.

Para una entrega exitosa:

```text
ConfirmNotificationDelivery
```

Para una entrega fallida:

```text
ReportNotificationDeliveryFailure
```

El resultado externo no modifica NotificationStatus directamente.

---

# External References

Las relaciones con otros Aggregates utilizan:

```text
AggregateId

Domain Contract
```

cuando corresponda.

No deben incorporarse Aggregates externos completos dentro de
Notification.

Esto protege:

- encapsulamiento;
- ownership;
- límites de consistencia;
- independencia entre contextos.

---

# Protección de Citizen

Cuando una Notification se relaciona con un destinatario asociado a
Citizen, debe mantenerse:

```text
Recipient Reference

≠

Embedded Citizen Aggregate
```

Notification no adquiere autoridad sobre Citizen.

---

# Protección de Organization

Una referencia organizacional no permite que Notification:

- modifique Organization;
- cambie su estructura;
- modifique su Version;
- administre su Lifecycle.

Debe mantenerse:

```text
Notification Authorization

≠

Organization Mutation Authority
```

---

# Protección de Assembly

Un hecho de Assembly puede originar una necesidad de comunicación.

Notification permanece separada.

Debe mantenerse:

```text
Assembly Fact

↓

Notification Management
```

pero nunca:

```text
Notification

↓

Direct Assembly State Mutation
```

---

# Protección de Document

Cuando exista relación mediante:

```text
DocumentId
```

Notification no obtiene autoridad para modificar:

```text
DocumentStatus

Document.Version

Document Content

Document Lifecycle
```

---

# Consistency Boundary

El Security Model debe respetar el límite definido en:

```text
DOMAIN-011J-Consistency-Boundary.md
```

Ningún mecanismo de seguridad puede ampliar implícitamente el
Aggregate.

Debe mantenerse:

```text
Security Context

≠

Expanded Aggregate Boundary
```

---

# Multi-Aggregate Security

Una autorización sobre Notification no equivale a autorización
sobre otros Aggregates.

Debe mantenerse:

```text
Permission on Notification

≠

Permission on Assembly

≠

Permission on Document

≠

Permission on Citizen
```

Cada contexto aplica sus propias políticas.

---

# Domain Events

Los Domain Events oficiales:

```text
NotificationCreated

NotificationQueued

NotificationDelivered

NotificationDeliveryFailed

NotificationRetried
```

representan hechos consumados.

Deben protegerse contra:

- modificación retroactiva;
- fabricación desde Infrastructure;
- exposición innecesaria de información;
- incorporación de secretos.

---

# Inmutabilidad de Eventos

Una vez confirmado:

```text
Domain Event
```

representa un hecho histórico.

No puede modificarse para ocultar o alterar un resultado previo.

Debe mantenerse:

```text
Historical Fact

=

Immutable
```

---

# Event Payload

El Payload de un Domain Event debe contener únicamente información
necesaria para representar el hecho.

No debe contener:

- passwords;
- API keys;
- access tokens;
- refresh tokens;
- secretos;
- claves privadas;
- configuración interna de proveedores;
- información no necesaria para expresar el hecho.

---

# Integration Events

Los Integration Events constituyen contratos públicos cuando existe
una necesidad explícita de integración.

Su publicación debe aplicar minimización de información.

Debe mantenerse:

```text
Aggregate Data

≠

Automatically Public Integration Data
```

La existencia de información dentro de Notification no implica que
deba propagarse fuera del Bounded Context.

---

# Protección de Integration Events

Los contratos de integración no deben exponer:

- secretos;
- credenciales;
- tokens;
- claves privadas;
- datos no requeridos;
- estructuras internas innecesarias del Aggregate.

Debe mantenerse:

```text
Integration Payload

=

Minimum Required Information
```

---

# Publicación después del Commit

Un Integration Event solamente puede publicarse después de que el
hecho originador haya sido confirmado.

Debe mantenerse:

```text
Confirmed Commit

↓

Integration Publication
```

Nunca:

```text
Integration Publication

↓

Try Aggregate Commit
```

---

# Outbox

Cuando se utilice Outbox, el registro asociado a publicación
representa un mecanismo de confiabilidad técnica.

Outbox:

- no obtiene autoridad sobre Notification;
- no modifica NotificationStatus;
- no incrementa Notification.Version durante publicación;
- no crea nuevos hechos del dominio.

---

# Idempotencia

Los mecanismos externos deben soportar procesamiento idempotente
cuando un mensaje pueda recibirse más de una vez.

Un duplicado técnico no debe convertirse en un nuevo hecho de
dominio automáticamente.

Debe mantenerse:

```text
Duplicate Technical Message

≠

New Domain Fact
```

---

# Replay Protection

El reprocesamiento técnico de un mensaje previamente procesado no
debe permitir aplicar nuevamente una transición que ya no sea
válida.

La protección se mantiene mediante:

- estado actual;
- State Machine;
- Invariants;
- Versioning;
- idempotencia en las capas correspondientes.

---

# Read Models

Los Read Models no constituyen autoridad de seguridad sobre el
Aggregate.

Una proyección:

- no modifica Notification;
- no ejecuta Commands;
- no concede permisos;
- no evita autorización;
- no sustituye políticas de lectura.

---

# Seguridad de Lectura

La exposición de un Read Model debe respetar políticas de lectura
aplicables.

Debe mantenerse:

```text
Data Exists

≠

Data May Be Read By Everyone
```

La política concreta permanece fuera del Aggregate.

---

# Minimización de Información

Las proyecciones deben exponer únicamente la información necesaria
para su caso de uso.

La existencia de un campo en el Write Model no obliga a incorporarlo
en todos los Read Models.

Debe mantenerse:

```text
Read Projection

=

Purpose-Bounded Information
```

---

# Audit

Audit permanece fuera de Notification.

Puede registrar información relativa a:

- actor;
- Command;
- autorización;
- resultado;
- NotificationId;
- Version;
- Domain Event;
- timestamp;

cuando corresponda.

Debe mantenerse:

```text
Audit Record

≠

Notification State
```

y:

```text
Audit Record

≠

Domain Event
```

---

# Trazabilidad

El Security Model debe preservar trazabilidad suficiente para
relacionar:

```text
Actor / Process

Command

NotificationId

Version

Domain Event

CorrelationId

CausationId
```

cuando dichos conceptos correspondan al flujo.

La trazabilidad no requiere almacenar credenciales dentro del
Aggregate.

---

# CorrelationId

CorrelationId puede utilizarse para seguir una interacción a través
de límites distribuidos.

No constituye:

- credencial;
- permiso;
- NotificationId;
- autoridad de modificación.

---

# CausationId

CausationId permite mantener relación causal entre mensajes o
hechos.

No permite:

- ejecutar Commands;
- evitar autorización;
- evitar Versioning;
- modificar otro Aggregate.

---

# Protección de Datos

Notification debe seguir el principio conceptual de minimización.

Debe mantener únicamente la información necesaria para cumplir su
responsabilidad de dominio.

No debe absorber información externa simplemente por conveniencia
técnica.

Debe mantenerse:

```text
Required Domain Information

⊆

Stored Notification Information
```

sin incorporar información innecesaria.

---

# Datos Personales

Cuando Notification maneje referencias o información asociada a
personas, dicha información debe utilizarse exclusivamente conforme
a los contratos y políticas aplicables.

La existencia de una relación con Citizen no implica que
Notification deba replicar toda su información.

Debe mantenerse:

```text
Citizen Information

≠

Automatic Notification Copy
```

---

# Sensitive Data

El Security Model no introduce una clasificación concreta adicional
de datos sensibles dentro del Aggregate versión 1.0.

Cuando exista una clasificación oficial de datos aplicable, deberá
respetarse sin ampliar automáticamente el modelo de Notification.

---

# Logs

Los logs pertenecen a Observability e Infrastructure.

No constituyen estado del Aggregate.

Los logs no deben utilizarse como mecanismo para evitar las reglas
de minimización.

Debe mantenerse:

```text
Operational Log

≠

Domain State
```

---

# Observability

Métricas, traces y logs pueden utilizarse para observar el sistema.

No pueden:

- modificar Notification;
- producir transiciones;
- alterar Version;
- reemplazar Domain Events;
- reemplazar Audit.

---

# Infrastructure

Infrastructure puede implementar:

- cifrado;
- seguridad de transporte;
- almacenamiento seguro;
- secret management;
- token validation;
- identity providers;
- firewalls;
- network policies;
- access controls técnicos.

Ningún mecanismo concreto forma parte del Aggregate.

Debe mantenerse:

```text
Security Requirement

≠

Infrastructure Implementation Detail
```

---

# Cifrado

El dominio puede requerir protección de información, pero el
algoritmo, protocolo, librería o mecanismo concreto de cifrado
pertenece a Infrastructure.

Notification no depende de una tecnología criptográfica específica.

---

# Transporte

El mecanismo de transporte de Commands, eventos o integraciones no
forma parte del Aggregate.

El Security Model no depende de:

```text
HTTP

REST

GraphQL

AMQP

MQTT

SMTP
```

ni de protocolos equivalentes.

---

# FIWARE

La integración con FIWARE permanece fuera del Aggregate.

Credenciales, tokens, mecanismos de autenticación y políticas de
seguridad FIWARE no forman parte del estado de Notification.

Debe mantenerse:

```text
FIWARE Security

≠

Notification Domain State
```

---

# Sistemas Municipales

Las credenciales necesarias para interoperar con sistemas
municipales permanecen fuera del Aggregate.

Notification solamente participa mediante contratos de dominio e
integración definidos.

La autenticación externa no modifica las Invariants internas.

---

# Fallos de Seguridad

Un fallo de Authentication o Authorization no debe transformarse
automáticamente en:

```text
NotificationStatus = Failed
```

Failed representa un resultado de entrega.

Debe mantenerse:

```text
AuthenticationFailure

≠

NotificationDeliveryFailed
```

y:

```text
AuthorizationFailure

≠

NotificationDeliveryFailed
```

---

# Fallos de Infrastructure

Un fallo técnico de seguridad, transporte o almacenamiento no crea
automáticamente un nuevo estado del Aggregate.

Por ejemplo:

```text
TokenExpired

RepositoryUnavailable

NetworkFailure
```

no equivalen a:

```text
NotificationStatus = Failed
```

salvo que exista una operación de dominio válida que incorpore un
resultado de entrega correspondiente.

---

# Security y Performance

Ninguna optimización de Performance puede eliminar:

- Authentication requerida;
- Authorization requerida;
- control de Version;
- Invariants;
- minimización de información;
- protección de límites.

Debe mantenerse:

```text
Performance Optimization

≠

Security Bypass
```

---

# Security y Event Sourcing

Cuando se utilice Event Sourcing:

- los hechos históricos permanecen inmutables;
- los Payloads deben respetar minimización;
- los eventos no deben contener secretos;
- la reconstrucción no evita autorización para nuevas operaciones;
- el replay no constituye una nueva acción autorizada del actor.

Debe mantenerse:

```text
Event Replay

≠

New Authorized Command
```

---

# Security y CQRS

CQRS permite mantener políticas diferentes para:

```text
Write Side
```

y:

```text
Read Side
```

cuando corresponda.

Una autorización de lectura no implica autorización de escritura.

Debe mantenerse:

```text
Read Permission

≠

Write Permission
```

---

# Security y Repository

El Repository no decide políticas de autorización.

Su responsabilidad permanece limitada al contrato de persistencia.

No debe:

- autenticar actores;
- conceder Roles;
- decidir Permissions;
- evitar Invariants;
- modificar estado por razones de autorización.

---

# Security y Domain Events

El Aggregate solamente produce Domain Events después de una
operación válida.

Debe mantenerse:

```text
Unauthorized Operation

↓

No Aggregate Execution
```

y:

```text
Invalid Authorized Operation

↓

Rejected

↓

No Success Domain Event
```

---

# Security y Integration Events

La publicación externa debe preservar el principio de mínima
información necesaria.

Un consumidor externo no debe depender de:

- secretos internos;
- estructura privada del Aggregate;
- credenciales del productor;
- detalles de persistencia;
- detalles del proveedor de entrega.

---

# Threat Boundaries Conceptuales

El modelo reconoce como límites relevantes:

```text
External Actor
    │
    ▼
Authentication Boundary
    │
    ▼
Authorization Boundary
    │
    ▼
Application Boundary
    │
    ▼
Notification Consistency Boundary
    │
    ▼
Integration Boundary
    │
    ▼
External Systems
```

Cada límite mantiene responsabilidades diferenciadas.

---

# Protección frente a Operaciones No Válidas

Deben rechazarse conceptual o técnicamente los intentos de:

- modificar directamente NotificationId;
- modificar directamente NotificationStatus;
- modificar directamente Version;
- evitar State Machine;
- evitar Invariants;
- usar un Read Model como Write Model;
- incrustar Aggregates externos;
- modificar otros Aggregates mediante Notification;
- reutilizar credenciales como datos del dominio;
- publicar secretos mediante eventos;
- utilizar un proveedor externo para mutar estado directamente;
- reinterpretar fallos técnicos como estados de dominio sin una
  operación válida.

---

# Reglas Fundamentales

Las siguientes reglas son obligatorias:

1. Notification no realiza Authentication.
2. Notification no administra Authorization.
3. Authorization ocurre antes del Command.
4. Authorization no evita Domain Validation.
5. Se aplica Deny by Default.
6. Se aplica Least Privilege.
7. Ningún permiso permite evitar Lifecycle.
8. Ningún permiso permite evitar State Machine.
9. Ningún permiso permite evitar Invariants.
10. NotificationId permanece protegido e inmutable.
11. NotificationStatus no puede modificarse directamente.
12. Version no puede modificarse arbitrariamente.
13. Optimistic Concurrency protege escrituras concurrentes.
14. Delivered permanece terminal incluso ante actores privilegiados.
15. Failed solamente puede volver a Pending mediante RetryNotification.
16. Notification no almacena credenciales.
17. Notification no almacena secretos técnicos.
18. Channel no equivale a configuración segura del Provider.
19. External Providers no modifican Notification directamente.
20. Los resultados externos ingresan mediante Commands válidos.
21. Las referencias externas utilizan identificadores o contratos.
22. Notification no adquiere ownership sobre otros Aggregates.
23. Los Domain Events son hechos inmutables.
24. Los Domain Event Payloads no contienen secretos.
25. Los Integration Events aplican minimización de información.
26. Integration Events solamente se publican después del commit.
27. Outbox no obtiene autoridad sobre Notification.
28. Duplicados técnicos no crean automáticamente nuevos hechos.
29. Replay no evita State Machine, Invariants ni Versioning.
30. Read Models no conceden autoridad de escritura.
31. La exposición de lectura requiere políticas aplicables.
32. Audit permanece fuera del Aggregate.
33. Trazabilidad no requiere almacenar credenciales.
34. La información personal no se replica automáticamente.
35. Logs y Observability permanecen fuera del estado del dominio.
36. Cifrado y transporte pertenecen a Infrastructure.
37. FIWARE Security permanece fuera del Aggregate.
38. Las credenciales de sistemas municipales permanecen fuera del
    Aggregate.
39. AuthenticationFailure no equivale a Notification Failed.
40. AuthorizationFailure no equivale a Notification Failed.
41. Fallos técnicos no crean automáticamente estados del dominio.
42. Performance no puede evitar Security.
43. Event Sourcing debe preservar inmutabilidad y minimización.
44. CQRS puede mantener políticas diferentes para lectura y
    escritura.
45. Repository no decide autorización.
46. Una operación rechazada no produce Domain Event de éxito.

---

# Compatibilidad Arquitectónica

El Security Model de Notification es compatible con:

- Domain-Driven Design;
- Clean Architecture;
- Hexagonal Architecture;
- SOLID;
- CQRS;
- Event-Driven Architecture;
- Event Sourcing;
- Optimistic Concurrency Control;
- Least Privilege;
- Deny by Default;
- Separation of Concerns;
- Defense in Depth.

Estas compatibilidades no introducen una dependencia tecnológica en
el Aggregate.

---

# Definición de Éxito

El Security Model del Aggregate **Notification** garantiza que la
protección del dominio permanezca separada de los mecanismos
tecnológicos utilizados para implementar seguridad.

El modelo protege:

```text
NotificationId

NotificationStatus

Version

Lifecycle

State Machine

Invariants

Commands

Domain Events

Consistency Boundary
```

y garantiza que:

- Authentication permanece fuera del Aggregate;
- Authorization se evalúa antes del Command;
- autorización no convierte automáticamente una operación en válida;
- Deny by Default y Least Privilege pueden aplicarse sin introducir
  Roles internos adicionales;
- ningún privilegio evita Lifecycle, State Machine o Invariants;
- NotificationId permanece inmutable;
- NotificationStatus solamente cambia mediante comportamiento de
  dominio;
- Version protege concurrencia y evolución lógica;
- Notification no almacena credenciales ni secretos;
- proveedores externos permanecen fuera del Aggregate;
- resultados técnicos ingresan mediante Commands válidos;
- otros Aggregates mantienen sus propios límites y políticas;
- Domain Events permanecen inmutables;
- eventos y proyecciones aplican minimización de información;
- Integration Events se publican solamente después del commit;
- Read Models no obtienen autoridad de escritura;
- Audit permanece independiente;
- datos personales no se replican automáticamente;
- logs, traces y métricas permanecen fuera del estado del dominio;
- cifrado, transporte y secret management pertenecen a
  Infrastructure;
- FIWARE y sistemas municipales no introducen credenciales dentro
  de Notification;
- fallos de Authentication, Authorization o Infrastructure no se
  confunden con Notification Failed;
- CQRS y Event Sourcing preservan las mismas reglas de seguridad;
- Performance no puede utilizarse para reducir las protecciones del
  dominio.

De esta forma, `DOMAIN-011O-Security-Model.md` establece el modelo
conceptual de seguridad del Aggregate **Notification** conforme al
patrón consolidado de AURA Core.