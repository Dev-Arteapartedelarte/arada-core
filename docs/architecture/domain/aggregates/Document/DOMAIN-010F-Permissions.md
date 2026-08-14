# DOMAIN-010F — Document Permissions

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
- DOMAIN-010A-Lifecycle.md
- DOMAIN-010B-State-Machine.md
- DOMAIN-010C-Commands.md
- DOMAIN-010E-Invariants.md
- CORE-007-Strategic-Design.md

---

# Objetivo

Este documento define el modelo de permisos del Aggregate
Document.

Los permisos establecen quién puede ejecutar Commands sobre un
Document y bajo qué condiciones.

El Aggregate nunca conoce usuarios, sesiones, JWT, OAuth,
proveedores de identidad o mecanismos concretos de autenticación.

Únicamente recibe una decisión de autorización proveniente de la
capa de aplicación.

La autorización no modifica las reglas internas del Aggregate.

---

# Principios

El modelo de permisos sigue los siguientes principios:

- separación entre autenticación y autorización;
- mínimo privilegio;
- denegación por defecto;
- independencia de infraestructura;
- autorización previa a la ejecución del Aggregate;
- trazabilidad completa;
- preservación del Lifecycle;
- preservación de la State Machine;
- preservación de las Invariants.

Una autorización válida permite intentar una operación.

No garantiza que la operación sea aceptada por Document.

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

Application Service

        │

        ▼

Document Aggregate
```

El Aggregate nunca autentica usuarios.

La autorización ocurre antes de la ejecución del Command.

El Aggregate conserva posteriormente la responsabilidad de validar
las reglas del dominio.

---

# Responsabilidades

## Infrastructure

Responsable de:

- autenticación;
- emisión de tokens;
- sesiones;
- proveedores de identidad;
- certificados.

---

## Application Layer

Responsable de:

- autorización;
- políticas;
- roles;
- permisos;
- validación previa.

---

## Aggregate

Responsable únicamente de:

- validar reglas de negocio;
- validar Lifecycle;
- validar State Machine;
- validar Invariants;
- ejecutar Commands válidos.

Debe mantenerse:

```text
Authorization

≠

Domain Validation
```

---

# Actores Conceptuales

Un actor representa la identidad que intenta ejecutar una
operación sobre Document.

La versión 1.0 de Document no introduce una asignación propia de
roles o tipos de actor.

La identidad concreta del actor y su clasificación pertenecen al
modelo de autorización de AURA.

Document recibe exclusivamente el contexto de autorización
necesario para determinar que la intención ya fue autorizada antes
de ejecutar el Command.

Debe mantenerse:

```text
Actor

≠

Document Aggregate
```

El Aggregate no almacena el perfil completo del actor.

---

# Matriz de Permisos

Los Commands oficiales de Document son:

| Command | Requisito de autorización |
| --- | --- |
| CreateDocument | Actor autorizado por la política aplicable |
| PublishDocument | Actor autorizado por la política aplicable |
| ArchiveDocument | Actor autorizado por la política aplicable |

Este documento no asigna estos Commands a roles concretos.

La asignación:

```text
Actor

↓

Role / Policy

↓

Permission

↓

Command
```

pertenece al contexto responsable de autorización.

Document únicamente recibe una intención previamente autorizada.

---

# Principio de Propiedad

La autorización para operar sobre un Document no establece por sí
misma propiedad sobre el Aggregate.

Debe mantenerse:

```text
Permission

≠

Ownership
```

La versión 1.0 no introduce mediante este documento nuevas reglas
de ownership sobre Document.

Cualquier regla de propiedad que deba formar parte del dominio debe
definirse explícitamente en los contratos correspondientes antes de
utilizarse como criterio de autorización.

---

# Principio de Delegación

La delegación de permisos pertenece al dominio de autorización.

El Aggregate Document no implementa mecanismos de delegación.

Una delegación válida puede permitir que un actor obtenga
autorización para intentar un Command.

No permite evitar:

- Lifecycle;
- State Machine;
- Invariants;
- Versioning;
- Consistency Boundary.

---

# Restricciones

Nunca está permitido:

- ejecutar un Command sin autorización previa cuando la operación
  requiera autorización;
- utilizar una Permission para modificar DocumentId;
- utilizar una Permission para modificar directamente
  DocumentStatus;
- utilizar una Permission para modificar directamente Content;
- utilizar una Permission para evitar la Aggregate Root;
- utilizar una Permission para evitar las Invariants;
- utilizar una Permission para crear una transición inexistente;
- utilizar una Permission para modificar directamente otro
  Aggregate;
- utilizar una Permission para evitar las reglas de Versioning;
- publicar un Document desde un estado distinto de Draft;
- archivar un Document desde un estado distinto de Published;
- ejecutar transiciones ordinarias desde Archived.

Una operación autorizada que viole una regla del dominio debe ser
rechazada.

---

# Permisos sobre Estados

Algunas operaciones dependen simultáneamente de la autorización y
del estado del Aggregate.

Ejemplo:

```text
No Document

↓

CreateDocument
```

Puede ejecutarse únicamente cuando la intención se encuentra
autorizada y las condiciones de creación son válidas.

---

```text
Draft

↓

PublishDocument
```

Puede ejecutarse únicamente para un actor autorizado y cuando las
Invariants de publicación se encuentren satisfechas.

---

```text
Published

↓

ArchiveDocument
```

Puede ejecutarse únicamente para un actor autorizado y cuando las
Invariants de archivado se encuentren satisfechas.

---

```text
Archived

↓

PublishDocument
```

No está permitido.

La existencia de autorización no crea la transición:

```text
Archived → Published
```

---

# Auditoría

Toda decisión de autorización debe poder ser registrada.

Como mínimo:

- actor;
- AggregateId;
- Command;
- fecha y hora;
- resultado;
- motivo del rechazo, cuando exista.

Para Document:

```text
AggregateId

=

DocumentId
```

La auditoría pertenece a otro Bounded Context y no al Aggregate
Document.

Document no almacena registros de autorización como parte de su
estado interno.

---

# Integración con RBAC

El dominio es compatible con modelos Role-Based Access Control.

Conceptualmente:

```text
Actor

↓

Role

↓

Permissions

↓

Commands
```

La implementación concreta pertenece a Infrastructure o al
servicio responsable de autorización.

Document no conoce la estructura interna del modelo RBAC.

La incorporación o modificación de Roles no modifica por sí misma
el Aggregate.

---

# Integración con ABAC

El modelo también es compatible con Attribute-Based Access
Control.

Las políticas de autorización pueden considerar atributos del
contexto autorizado, siempre fuera del Aggregate.

Entre los conceptos ya definidos por Document que pueden formar
parte del contexto evaluado se encuentran:

- DocumentStatus;
- DocumentType;
- Command solicitado.

La definición de políticas concretas no pertenece al Aggregate.

Document permanece independiente de dichas políticas.

Debe mantenerse:

```text
Authorization Attributes

≠

Document Invariants
```

---

# Compatibilidad con Event Sourcing

La autorización nunca modifica el historial del Aggregate.

Únicamente los Commands aceptados por Document producen los Domain
Events correspondientes.

Debe mantenerse:

```text
Authorized Command

+

Valid Domain Operation

↓

Domain Event
```

Una autorización concedida seguida de una operación rechazada no
produce el Domain Event de éxito.

---

# Compatibilidad con CQRS

Los permisos de modificación se evalúan en el lado de escritura
antes de ejecutar Commands sobre Document.

Conceptualmente:

```text
Authorization

↓

Command

↓

Document
```

Las consultas no requieren autorización del Aggregate.

Los Read Models pueden estar sujetos a políticas de acceso
implementadas por las capas responsables.

El Aggregate no autoriza consultas.

---

# Evolución

Nuevos roles y políticas pueden incorporarse sin modificar el
Aggregate, siempre que:

- respeten el Ubiquitous Language;
- mantengan las Invariants;
- no alteren implícitamente los Commands existentes;
- no introduzcan nuevas transiciones;
- no modifiquen el Consistency Boundary;
- preserven la compatibilidad con los contratos existentes.

La incorporación de un nuevo Command requiere una evolución
explícita de los documentos de dominio correspondientes.

Una nueva Permission no crea por sí misma un nuevo Command.

Debe mantenerse:

```text
New Permission

≠

New Domain Behavior
```

---

# Definición de Éxito

El modelo de permisos del Aggregate **Document** garantiza que toda
modificación sea intentada únicamente después de una decisión de
autorización, manteniendo una separación estricta entre
autenticación, autorización y reglas de negocio.

El modelo preserva:

- separación entre Identity y Document;
- autorización previa al Command;
- independencia del Aggregate respecto de mecanismos de
  autenticación;
- mínimo privilegio;
- denegación por defecto;
- trazabilidad;
- Lifecycle;
- State Machine;
- Invariants;
- Versioning;
- Consistency Boundary.

Ninguna Permission modifica directamente Document.

Ninguna Permission garantiza la aceptación de un Command.

Debe mantenerse:

```text
Authorized Intent

↓

Document

↓

Domain Validation

↓

Accepted or Rejected
```

De esta forma, el modelo de Permissions mantiene al Aggregate
**Document** independiente del mecanismo concreto de seguridad y
preserva la consistencia del dominio AURA. 