# DOMAIN-009O — Voting Security Model

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Voting Management

Aggregate:
Voting

Documentos relacionados:

- DOMAIN-009-Aggregate.md
- DOMAIN-009E-Invariants.md
- DOMAIN-009F-Permissions.md
- DOMAIN-009G-Repository-Contract.md
- DOMAIN-009J-Consistency-Boundary.md
- DOMAIN-009K-Integration-Events.md
- DOMAIN-009L-Read-Model.md
- CORE-016-Dependency-Rules.md

---

# Objetivo

Este documento define el modelo de seguridad del Aggregate
**Voting**.

Su propósito es proteger la integridad del proceso formal de Voting
sin introducir dependencias de infraestructura dentro del dominio.

El Aggregate únicamente protege las reglas de negocio que le
pertenecen.

La autenticación, autorización y mecanismos criptográficos
pertenecen a otras capas de la arquitectura.

---

# Principios

El modelo de seguridad sigue los siguientes principios:

- Security by Design.
- Privacy by Design.
- Least Privilege.
- Defense in Depth.
- Zero Trust.
- Fail Secure.
- Auditability.
- Separation of Concerns.

---

# Responsabilidades del Aggregate

El Aggregate Voting es responsable de:

- proteger sus Invariants;
- impedir transiciones inválidas;
- impedir modificaciones ilegales;
- preservar VotingId;
- preservar OrganizationId;
- preservar la integridad de VotingStatus;
- preservar la coherencia de Rules;
- preservar la coherencia de Options;
- preservar Result cuando corresponda;
- preservar Version;
- garantizar consistencia dentro de su Consistency Boundary.

No es responsable de:

- autenticar actores;
- validar credenciales;
- validar tokens;
- gestionar sesiones;
- cifrar comunicaciones;
- administrar certificados;
- controlar infraestructura de red;
- enviar Notifications;
- administrar otros Aggregates.

---

# Modelo Conceptual

```text
Identity Provider

        │

Authentication

        │

Authorization

        │

Application Service

        │

Voting Aggregate

        │

Repository
```

El Aggregate recibe Commands después de la evaluación de
autorización correspondiente.

Voting conserva siempre la responsabilidad de validar sus propias
reglas de dominio.

Debe mantenerse:

```text
Authorized Command

≠

Valid Domain Operation
```

Una operación autorizada puede ser rechazada por:

- Lifecycle;
- State Machine;
- Invariants;
- estado actual;
- Version;
- reglas propias del Aggregate.

---

# Identidad

Cada Voting posee una identidad única:

```text
VotingId
```

La identidad:

- es inmutable;
- nunca se reutiliza;
- nunca cambia durante el Lifecycle;
- no depende del mecanismo de autenticación;
- no depende del mecanismo de autorización.

OrganizationId representa el contexto organizacional del Voting y
permanece igualmente protegido por las reglas establecidas del
Aggregate.

---

# Integridad

Toda modificación debe preservar:

- VotingId;
- OrganizationId;
- VotingType;
- VotingStatus;
- Rules;
- Options;
- Result cuando corresponda;
- Lifecycle;
- Invariants;
- Version;
- Consistency Boundary.

No pueden existir estados parcialmente válidos.

Debe mantenerse:

```text
Valid Voting Before

↓

Valid Domain Operation

↓

Valid Voting After
```

Una operación que produciría un estado inválido debe ser rechazada.

---

# Autenticación

La autenticación permanece fuera del Aggregate Voting.

Su responsabilidad es determinar la identidad del actor que intenta
realizar una operación.

Voting no conoce ni administra mecanismos concretos de
autenticación.

Debe mantenerse:

```text
Authentication

≠

Voting Domain Behavior
```

El mecanismo utilizado para identificar al actor no modifica:

- Lifecycle;
- State Machine;
- Invariants;
- Commands;
- Domain Events;
- Versioning.

---

# Autorización

La autorización ocurre antes de ejecutar una operación protegida.

El modelo de Permissions de Voting se define en:

```text
DOMAIN-009F-Permissions.md
```

Las Permissions oficiales son:

```text
Voting.Create

Voting.Open

Voting.Close

Voting.Cancel

Voting.Archive

Voting.ChangeType

Voting.ChangeTitle

Voting.ChangeDescription

Voting.ChangeRules

Voting.AddOption

Voting.RemoveOption

Voting.Read
```

La autorización determina si el actor puede solicitar una
operación.

Voting determina posteriormente si dicha operación es válida.

Debe mantenerse:

```text
Permission Granted

↓

Command may be requested

↓

Voting validates domain rules

↓

Accepted or Rejected
```

Nunca:

```text
Permission Granted

=

Invariant Bypass
```

---

# Protección de Datos Personales

Voting debe utilizar únicamente la información necesaria para
representar su propio proceso de dominio.

Los Aggregates externos no deben incorporarse dentro de Voting para
resolver autenticación o autorización.

En particular, Voting no debe almacenar como parte de su estado
interno:

```text
Citizen Aggregate

Membership Aggregate

Role Aggregate
```

Las relaciones necesarias deben mantenerse conforme a los contratos
e identificadores definidos por AURA.

La información que no sea necesaria para proteger el estado y
comportamiento de Voting debe permanecer fuera del Aggregate.

---

# Consentimiento

Voting no define en la versión 1.0 un modelo propio de
consentimiento.

Este documento no introduce:

```text
AcceptConsent

WithdrawConsent

VotingConsent
```

ni conceptos equivalentes.

Cuando otro contexto requiera administrar consentimientos, dicha
responsabilidad permanece bajo el modelo correspondiente y no debe
incorporarse indirectamente al Aggregate Voting mediante reglas de
seguridad.

---

# Auditoría

Las operaciones relevantes sobre Voting deben poder mantenerse
trazables mediante los contratos establecidos por AURA.

La información de trazabilidad puede relacionar conceptualmente:

```text
ActorId

VotingId

Command

Domain Event

OccurredAt

CorrelationId

CausationId

AggregateVersion
```

cuando dichos elementos correspondan a los contratos ya definidos.

La auditoría pertenece a un Bounded Context independiente.

Voting no almacena el Aggregate:

```text
Audit
```

dentro de su estado.

La existencia de auditoría no amplía el Consistency Boundary.

---

# Integración Segura

Los Integration Events de Voting deben contener únicamente la
información necesaria para comunicar el hecho correspondiente.

Nunca deben incluir:

- contraseñas;
- tokens;
- claves privadas;
- secretos criptográficos;
- credenciales de infraestructura;
- sesiones;
- información externa innecesaria.

Los contratos oficiales se definen en:

```text
DOMAIN-009K-Integration-Events.md
```

Debe mantenerse:

```text
Integration Event Payload

≠

Complete Voting Aggregate
```

y:

```text
Aggregate Identifier

≠

Embedded External Aggregate
```

---

# Comunicación entre Contextos

La comunicación entre Voting y otros Bounded Contexts debe realizarse
mediante los contratos establecidos por AURA.

Conceptualmente pueden utilizarse:

- Domain Events;
- Integration Events;
- contratos de aplicación;
- interfaces autorizadas entre contextos.

No debe realizarse mediante acceso directo al estado interno de otro
Aggregate.

Debe mantenerse:

```text
Voting

↓

Explicit Contract

↓

External Context
```

No:

```text
Voting

↓

Direct External Aggregate State Mutation
```

---

# Concurrencia

El modelo utiliza:

```text
Optimistic Concurrency Control
```

según las reglas de Versioning y Repository Contract ya definidas.

Debe mantenerse:

```text
ExpectedVersion

=

PersistedVersion
```

para confirmar una modificación sobre un Voting existente.

Cuando:

```text
ExpectedVersion

!=

PersistedVersion
```

debe producirse el conflicto de concurrencia correspondiente.

Esto evita:

- sobrescrituras incompatibles;
- pérdida silenciosa de modificaciones;
- corrupción del estado del Aggregate;
- violación de la secuencia lógica de Version.

La seguridad no puede utilizarse para evitar el control de
concurrencia.

---

# Protección frente a Errores

Ante una operación que no pueda completarse válidamente:

- no se confirma la modificación del Aggregate;
- VotingStatus conserva su valor anterior;
- Version conserva su valor anterior;
- no se produce el Domain Event de éxito;
- no se produce el Integration Event de éxito derivado.

Debe mantenerse:

```text
Failed Operation

↓

No Confirmed Domain Mutation
```

La operación nunca debe dejar Voting en un estado parcialmente
válido.

---

# Gestión de Secretos

El Aggregate Voting nunca conoce:

- contraseñas;
- claves API;
- certificados;
- secretos criptográficos;
- credenciales de infraestructura;
- tokens;
- sesiones.

La gestión de secretos pertenece fuera del dominio Voting.

Debe mantenerse:

```text
Voting Domain State

≠

Secret Storage
```

---

# Cifrado

El dominio es independiente del mecanismo concreto de cifrado.

Los mecanismos utilizados para proteger:

- datos en tránsito;
- datos persistidos;
- credenciales;
- comunicaciones;
- infraestructura;

permanecen fuera del Aggregate.

Nada de ello modifica:

- VotingId;
- VotingStatus;
- Lifecycle;
- State Machine;
- Invariants;
- Version;
- Domain Events.

Debe mantenerse:

```text
Encryption Mechanism

≠

Voting Domain Rule
```

---

# Trazabilidad

Toda modificación válida de Voting debe poder relacionarse
conceptualmente mediante:

```text
Command

↓

Voting

↓

Domain Event

↓

Integration Event when applicable

↓

Audit
```

La trazabilidad debe preservar el significado de los hechos
confirmados.

AggregateVersion permite relacionar cada hecho con la Version de
Voting que lo produjo.

CorrelationId y CausationId pueden conservar la relación causal
cuando correspondan a los contratos establecidos.

La trazabilidad no permite modificar retroactivamente los hechos
históricos.

---

# Cumplimiento Normativo

Voting debe permitir que las políticas normativas aplicables puedan
ser implementadas sin incorporar legislación o mecanismos técnicos
directamente dentro de la Aggregate Root.

Las obligaciones específicas que correspondan al tratamiento de
información, autorización, conservación, acceso o auditoría deben
ser aplicadas por los contextos y capas responsables.

El Aggregate continúa protegiendo exclusivamente:

- identidad;
- estado;
- Lifecycle;
- Invariants;
- Version;
- Consistency Boundary.

Este documento no introduce nuevas reglas legales específicas dentro
del modelo de Voting.

---

# Compatibilidad con FIWARE

La integración de Voting con FIWARE, cuando corresponda, debe
realizarse mediante contratos externos al Aggregate.

Voting no interactúa directamente con componentes de infraestructura
FIWARE.

Debe mantenerse:

```text
Voting

↓

Domain Event

↓

Integration Contract

↓

External Infrastructure
```

La existencia de una integración FIWARE no modifica:

- Lifecycle;
- State Machine;
- Commands;
- Permissions;
- Invariants;
- Version;
- Consistency Boundary.

---

# Compatibilidad con Event Sourcing

Cuando Voting utilice un historial de Domain Events para
reconstrucción, los hechos históricos deben preservar su significado
e inmutabilidad.

Debe mantenerse:

```text
Historical Domain Event

≠

Mutable Current State Record
```

Las correcciones no deben reescribir arbitrariamente un hecho
histórico ya confirmado.

Replay no constituye una nueva operación de dominio.

Por tanto:

```text
Replay

↓

No New Voting Version
```

y:

```text
Replay

↓

No New Success Domain Event
```

por el solo hecho de reconstruir el Aggregate.

---

# Compatibilidad con CQRS

Las políticas de acceso del Read Side pueden diferir de las
capacidades de modificación del Write Side.

Debe mantenerse:

```text
Write Permission

≠

Read Permission
```

y:

```text
Read Model

≠

Voting Aggregate
```

Los Read Models pueden representar únicamente la información
autorizada para cada necesidad de consulta.

La definición conceptual de lectura pertenece a:

```text
DOMAIN-009L-Read-Model.md
```

Ningún Read Model puede modificar Voting.

---

# Amenazas Mitigadas

Este modelo reduce el riesgo conceptual de:

- modificaciones no autorizadas;
- ejecución de Commands sin la Permission correspondiente;
- bypass de Invariants;
- bypass de Lifecycle;
- bypass de State Machine;
- alteración directa de VotingStatus;
- alteración directa de Version;
- sobrescrituras concurrentes incompatibles;
- pérdida de trazabilidad;
- exposición innecesaria de información;
- incorporación de secretos dentro del Aggregate;
- modificación directa de otros Aggregates;
- expansión indebida del Consistency Boundary;
- acoplamiento entre seguridad e infraestructura.

---

# Principios Arquitectónicos

El modelo mantiene los principios consolidados de AURA:

- Domain-Driven Design;
- Clean Architecture;
- Hexagonal Architecture;
- Security by Design;
- Privacy by Design;
- Zero Trust;
- Least Privilege;
- Separation of Concerns;
- Dependency Inversion Principle.

Debe mantenerse:

```text
Authentication

≠

Authorization

≠

Domain Validation
```

y:

```text
Security Infrastructure

≠

Voting Domain Model
```

Voting conserva la responsabilidad exclusiva sobre la validez de su
propio estado.

Las capas externas conservan la responsabilidad sobre mecanismos de
identidad, autorización, comunicación y protección técnica.

---

# Definición de Éxito

El modelo de seguridad del Aggregate **Voting** garantiza que el
proceso formal de Voting permanezca protegido sin introducir
dependencias de infraestructura dentro del dominio.

El Aggregate protege:

- VotingId;
- OrganizationId;
- VotingStatus;
- VotingType;
- Rules;
- Options;
- Result cuando corresponda;
- Lifecycle;
- State Machine;
- Invariants;
- Version;
- Consistency Boundary.

El modelo mantiene separadas:

```text
Authentication

Authorization

Permissions

Domain Validation

Infrastructure Security
```

Las Permissions determinan quién puede solicitar una operación.

Voting determina si dicha operación puede ejecutarse válidamente.

Los secretos, credenciales, sesiones y mecanismos criptográficos
permanecen fuera del Aggregate.

Los Domain Events e Integration Events preservan trazabilidad sin
ampliar el Consistency Boundary.

Los Read Models permanecen separados de la autoridad de escritura.

El control de concurrencia continúa protegiendo la evolución de
Version.

De esta forma, `DOMAIN-009O-Security-Model.md` establece el modelo
oficial de seguridad del Aggregate **Voting**, preservando la
integridad del dominio, la separación de responsabilidades y el
patrón consolidado de AURA Core.