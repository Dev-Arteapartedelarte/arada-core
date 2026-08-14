# DOMAIN-010O — Document Security Model

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Document Management

Aggregate:
Document

Documentos relacionados:

- DOMAIN-010-Aggregate.md
- DOMAIN-010C-Commands.md
- DOMAIN-010D-Domain-Events.md
- DOMAIN-010E-Invariants.md
- DOMAIN-010F-Permissions.md
- DOMAIN-010G-Repository-Contract.md
- DOMAIN-010I-Versioning.md
- DOMAIN-010J-Consistency-Boundary.md
- DOMAIN-010K-Integration-Events.md
- DOMAIN-010L-Read-Model.md

---

# Objetivo

Definir el modelo conceptual de seguridad del Aggregate
**Document**.

El Security Model establece las reglas que protegen la integridad,
confidencialidad, trazabilidad y acceso correcto a Document sin
introducir dentro del Aggregate responsabilidades propias de
autenticación, transporte, infraestructura o gestión de
credenciales.

El Aggregate protege sus Invariants y su estado.

Las capas externas protegen identidad, autenticación,
autorización, comunicación y secretos.

---

# Principios

El modelo de seguridad de Document sigue:

- Security by Design;
- Privacy by Design;
- Least Privilege;
- Defense in Depth;
- Zero Trust;
- Fail Secure;
- Auditability;
- Separation of Concerns.

Ningún principio de seguridad permite evitar:

- Lifecycle;
- State Machine;
- Invariants;
- Versioning;
- Consistency Boundary.

Debe mantenerse:

```text
Security Control

≠

Domain Rule Bypass
```

---

# Responsabilidades del Aggregate

Document es responsable de proteger:

- DocumentId;
- DocumentType;
- Content;
- DocumentStatus;
- Version;
- Invariants;
- transiciones válidas;
- generación coherente de Domain Events;
- Consistency Boundary.

Document no es responsable de:

- autenticar actores;
- emitir tokens;
- validar sesiones;
- gestionar credenciales;
- cifrar comunicaciones;
- administrar certificados;
- gestionar firewalls;
- enviar Notifications.

---

# Modelo Conceptual

```text
Identity

    │
    ▼

Authentication

    │
    ▼

Authorization

    │
    ▼

Application Layer

    │
    ▼

Document Aggregate

    │
    ├── Lifecycle
    ├── State Machine
    ├── Invariants
    └── Versioning
```

La seguridad exterior determina si una intención puede llegar al
Aggregate.

Document determina si dicha intención puede ejecutarse
válidamente dentro del dominio.

---

# Identidad

La identidad del Aggregate está representada por:

```text
DocumentId
```

DocumentId:

- identifica un único Document;
- permanece inmutable;
- no constituye una credencial;
- no autentica actores;
- no representa autorización.

Debe mantenerse:

```text
DocumentId

≠

Authentication Identity
```

y:

```text
DocumentId

≠

Authorization Credential
```

---

# Integridad

La integridad del Aggregate se protege mediante:

- Aggregate Root;
- Invariants;
- State Machine;
- Lifecycle;
- Version;
- Repository Contract;
- control de concurrencia optimista.

Ninguna operación puede modificar directamente:

```text
DocumentId

DocumentStatus

Content

Version
```

evitando el comportamiento válido del Aggregate.

Toda modificación aceptada debe preservar un estado consistente.

---

# Autenticación

Document no administra autenticación.

El Aggregate no conoce:

```text
Password

JWT

OAuth Token

Session

Certificate

Identity Provider
```

La autenticación pertenece a las capas responsables de identidad y
seguridad de AURA.

El Aggregate recibe una intención después de que la identidad haya
sido resuelta por dichas capas.

---

# Autorización

La autorización determina si un actor puede solicitar un Command.

Los Commands oficiales son:

```text
CreateDocument

PublishDocument

ArchiveDocument
```

La autorización se evalúa antes de ejecutar el comportamiento del
Aggregate.

Sin embargo:

```text
Authorized

≠

Domain Operation Guaranteed
```

Un Command autorizado todavía puede ser rechazado por:

- estado incompatible;
- transición inválida;
- violación de Invariant;
- conflicto de Version;
- cualquier regla válida del Aggregate.

Las reglas conceptuales de Permissions pertenecen a:

```text
DOMAIN-010F-Permissions.md
```

---

# Protección de Datos Personales

Document debe respetar el principio de minimización de datos.

Content puede contener información cuyo acceso requiera protección,
pero la naturaleza concreta del Content no se redefine mediante
este documento.

Debe mantenerse:

```text
Data Stored

≠

Data Automatically Exposed
```

La existencia de información dentro de Document no autoriza su
publicación automática mediante:

- Read Models;
- Integration Events;
- APIs;
- sistemas externos.

Cada exposición debe respetar los contratos y políticas
correspondientes.

---

# Consentimiento

Este Security Model no incorpora reglas nuevas de consentimiento
dentro del Aggregate Document.

Cuando una política de consentimiento sea aplicable a información
asociada a Document, dicha política debe ser resuelta por el
contexto responsable antes de utilizar o exponer la información.

Document no debe asumir consentimiento por la sola existencia de
Content.

Debe mantenerse:

```text
Content Exists

≠

Consent Granted
```

---

# Auditoría

Audit permanece fuera del Consistency Boundary de Document.

Document puede producir Domain Events correspondientes a hechos
confirmados:

```text
DocumentCreated

DocumentPublished

DocumentArchived
```

Audit puede observar posteriormente dichos hechos mediante
contratos explícitos.

Document no mantiene logs de auditoría como parte de su estado
interno.

Debe mantenerse:

```text
Domain Event

≠

Audit Log
```

---

# Integración Segura

La integración con otros Bounded Contexts o sistemas externos debe
realizarse mediante contratos explícitos.

Ningún consumidor externo puede:

- acceder directamente al estado interno del Aggregate;
- modificar DocumentStatus;
- modificar Content;
- modificar Version;
- evitar Commands;
- evitar Invariants.

Debe mantenerse:

```text
External Consumer

↓

Explicit Contract

≠

Direct Aggregate Access
```

---

# Comunicación entre Contextos

La comunicación con otros contextos puede realizarse mediante:

- Domain Events;
- Integration Events;
- APIs protegidas;
- mecanismos autenticados de mensajería.

Nunca mediante acceso directo a la persistencia interna de
Document.

Debe mantenerse:

```text
Bounded Context A

≠

Direct Database Access to Bounded Context B
```

Cada contexto conserva su propio modelo y su propia autoridad de
escritura.

---

# Concurrencia

La seguridad de integridad frente a concurrencia utiliza
Optimistic Concurrency Control.

Conceptualmente:

```text
PersistedVersion

≠

ExpectedVersion

↓

ConcurrencyConflict
```

Una modificación obsoleta no puede sobrescribir silenciosamente un
cambio confirmado.

El conflicto de concurrencia debe producir rechazo de la operación.

---

# Protección frente a Errores

Cuando una operación no pueda completarse de forma segura:

```text
Fail Secure
```

debe ser el comportamiento esperado.

Conceptualmente:

```text
Unexpected Condition

↓

Reject Operation

↓

Preserve Confirmed State
```

La operación rechazada:

- no modifica el Aggregate;
- no incrementa Version;
- no produce Domain Events de éxito.

---

# Gestión de Secretos

Document nunca almacena:

- contraseñas;
- tokens;
- claves privadas;
- secretos criptográficos;
- credenciales;
- sesiones;
- secretos de aplicaciones.

Estos elementos pertenecen a Infrastructure o a los servicios de
identidad y seguridad responsables.

Debe mantenerse:

```text
Document Aggregate

≠

Secret Store
```

---

# Cifrado

Document no depende de un mecanismo concreto de cifrado.

El cifrado puede aplicarse en:

- persistencia;
- transporte;
- almacenamiento;
- comunicación entre sistemas.

Sin embargo, la elección tecnológica pertenece a Infrastructure.

Debe mantenerse:

```text
Encryption Mechanism

≠

Domain Semantics
```

El cifrado de Content no modifica su significado dentro del
Aggregate.

---

# Trazabilidad

La trazabilidad conceptual puede representar:

```text
Command

↓

Domain Event

↓

Integration Event

↓

Audit
```

cuando existan los contratos correspondientes.

Para Document, los hechos oficiales son:

```text
DocumentCreated

DocumentPublished

DocumentArchived
```

Cada hecho debe preservar identidad, Version y contexto temporal
conforme a los contratos definidos.

---

# Cumplimiento Normativo

El modelo de seguridad debe permitir que las capas externas
implementen las obligaciones normativas aplicables sin alterar las
Invariants del Aggregate.

Las reglas concretas de:

- retención;
- acceso;
- confidencialidad;
- privacidad;
- exposición;
- eliminación técnica;

deben mantenerse separadas de Document cuando no constituyan una
regla explícita del dominio.

Este documento no introduce una política de eliminación física.

Archived continúa siendo el estado terminal oficial del Lifecycle
versión 1.0.

---

# Compatibilidad con FIWARE

Document puede integrarse con FIWARE mediante capas y contratos
externos.

El Aggregate no conoce:

```text
Keyrock

Wilma PEP Proxy

OAuth2

NGSI-LD

FIWARE SDK
```

Estos mecanismos pueden participar en autenticación, autorización,
protección de APIs o integración.

No modifican:

- DocumentId;
- Lifecycle;
- State Machine;
- Invariants;
- Versioning;
- Consistency Boundary.

Debe mantenerse:

```text
FIWARE Integration

≠

Document Domain Dependency
```

---

# Compatibilidad con Event Sourcing

En una implementación Event Sourcing, el historial de Domain Events
debe permanecer inmutable.

Los hechos:

```text
DocumentCreated

DocumentPublished

DocumentArchived
```

no deben reescribirse para representar estados posteriores.

Las correcciones históricas, cuando correspondan al dominio, deben
representarse mediante nuevos hechos explícitamente definidos y no
mediante alteración retroactiva.

La implementación de Event Sourcing no permite evitar las políticas
de seguridad aplicables al acceso a eventos históricos.

---

# Compatibilidad con CQRS

CQRS permite aplicar controles de seguridad diferenciados entre:

```text
Write Side

Read Side
```

En el Write Side:

- la autorización precede a los Commands;
- Document protege Invariants;
- Document protege State Machine;
- Version protege concurrencia.

En el Read Side:

- las proyecciones pueden limitar información;
- Content puede ocultarse cuando corresponda;
- distintos consumidores pueden disponer de vistas diferentes;
- las políticas de lectura no modifican Document.

Debe mantenerse:

```text
Read Authorization

≠

Write Authorization
```

cuando sus políticas sean diferentes.

---

# Amenazas Mitigadas

El Security Model contribuye a mitigar:

- modificación no autorizada;
- modificación directa del estado;
- bypass de Invariants;
- transiciones inválidas;
- escalamiento de privilegios;
- sobrescritura concurrente;
- corrupción del Aggregate;
- pérdida de trazabilidad;
- exposición innecesaria de Content;
- almacenamiento de secretos dentro del dominio;
- acceso directo entre Bounded Contexts;
- acoplamiento con mecanismos de autenticación;
- acoplamiento con Infrastructure.

La mitigación técnica específica pertenece a las capas
responsables.

---

# Principios Arquitectónicos

El Security Model de Document mantiene compatibilidad con:

- Domain-Driven Design;
- Clean Architecture;
- Hexagonal Architecture;
- CQRS;
- Event-Driven Architecture;
- Event Sourcing Compatible;
- Optimistic Concurrency;
- Security by Design;
- Privacy by Design;
- Least Privilege;
- Defense in Depth;
- Zero Trust;
- Fail Secure;
- Separation of Concerns.

El modelo permanece independiente de mecanismos concretos de
autenticación, autorización, cifrado y transporte.

---

# Definición de Éxito

El Security Model del Aggregate **Document** garantiza que la
seguridad preserve el dominio sin introducir dentro del Aggregate
responsabilidades externas.

El modelo garantiza que:

- Document protege su identidad;
- Document protege Content;
- Document protege DocumentStatus;
- Document protege Invariants;
- Document protege Version;
- la autenticación permanece fuera del Aggregate;
- la autorización precede a los Commands;
- una autorización nunca evita reglas del dominio;
- Content no se expone automáticamente;
- el consentimiento no se presume por la existencia de Content;
- Audit permanece fuera del Consistency Boundary;
- las integraciones utilizan contratos explícitos;
- otros contextos no acceden directamente al estado interno;
- Optimistic Concurrency protege la integridad frente a escrituras
  incompatibles;
- una operación insegura o inválida falla sin modificar el estado
  confirmado;
- Document no almacena secretos;
- el cifrado permanece como responsabilidad externa;
- la trazabilidad se mantiene mediante hechos y contratos;
- Archived continúa siendo el estado terminal oficial;
- FIWARE puede integrarse sin convertirse en dependencia del
  dominio;
- Event Sourcing preserva hechos históricos;
- CQRS permite separar políticas de lectura y escritura;
- Infrastructure no determina la semántica de seguridad del
  Aggregate.

De esta forma, `DOMAIN-010O-Security-Model.md` establece el modelo
oficial de seguridad del Aggregate **Document** conforme al patrón
consolidado de AURA Core.