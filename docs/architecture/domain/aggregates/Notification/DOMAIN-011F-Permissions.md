# DOMAIN-011F — Notification Permissions

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
- DOMAIN-011A-Lifecycle.md
- DOMAIN-011B-State-Machine.md
- DOMAIN-011C-Commands.md
- DOMAIN-011D-Domain-Events.md
- DOMAIN-011E-Invariants.md

---

# Objetivo

Este documento define el modelo conceptual de Permissions aplicado
al Aggregate **Notification**.

Su propósito es establecer cómo las decisiones de autorización se
relacionan con los Commands del Aggregate sin introducir dentro de
Notification responsabilidades de autenticación, identidad,
sesiones, tokens o infraestructura de seguridad.

Permissions determina si una intención puede ser presentada al
Aggregate.

Notification continúa siendo responsable de determinar si dicha
intención es válida conforme a:

- Lifecycle;
- State Machine;
- Invariants;
- Versioning;
- Consistency Boundary.

---

# Principios

El modelo de Permissions sigue los siguientes principios:

- separación entre Authentication y Authorization;
- Least Privilege;
- Deny by Default;
- independencia tecnológica;
- autorización antes de ejecutar el Aggregate;
- trazabilidad de decisiones;
- preservación de Invariants;
- preservación del Lifecycle;
- preservación de la State Machine;
- preservación del Consistency Boundary.

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

---

# Modelo Conceptual

El flujo conceptual de autorización es:

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

Notification Command

    │
    ▼

Notification Aggregate

    │
    ├── Lifecycle
    ├── State Machine
    ├── Invariants
    └── Versioning
```

Notification no decide quién es el actor.

Notification tampoco valida credenciales.

El Aggregate recibe una intención que ya pasó por la capa
responsable de autorización.

---

# Responsabilidades

## Infrastructure

Infrastructure puede ser responsable de:

- autenticación;
- proveedores de identidad;
- tokens;
- sesiones;
- credenciales;
- mecanismos OAuth;
- certificados;
- transporte seguro.

Estas responsabilidades no pertenecen a Notification.

---

## Application Layer

La Application Layer es responsable de:

- resolver la identidad del actor;
- evaluar la política de autorización;
- determinar si el actor puede solicitar un Command;
- rechazar intenciones no autorizadas antes de invocar el
  Aggregate;
- coordinar la ejecución del Command.

---

## Notification Aggregate

Notification es responsable de:

- validar el estado actual;
- validar la transición solicitada;
- validar Invariants;
- proteger NotificationId;
- proteger Version;
- ejecutar comportamiento de dominio;
- producir Domain Events después de operaciones válidas.

El Aggregate no reemplaza el sistema de autorización.

---

# Actores Conceptuales

La versión 1.0 no introduce dentro de Notification una taxonomía
propia de actores.

Notification no define internamente:

```text
Administrator

Operator

Citizen

OrganizationOwner

NotificationManager
```

como roles obligatorios del Aggregate.

La identidad, roles, Memberships y políticas organizacionales
pertenecen a los contextos responsables de AURA.

Por lo tanto, los permisos se expresan conceptualmente como:

```text
Actor authorized by applicable policy
```

sin introducir una nueva jerarquía de roles dentro de Notification.

---

# Matriz de Permisos

La versión 1.0 reconoce los siguientes Commands:

| Command | Requisito de autorización |
|---|---|
| CreateNotification | Actor o proceso autorizado por la política aplicable |
| QueueNotification | Actor o proceso autorizado por la política aplicable |
| ConfirmNotificationDelivery | Actor o proceso autorizado por la política aplicable |
| ReportNotificationDeliveryFailure | Actor o proceso autorizado por la política aplicable |
| RetryNotification | Actor o proceso autorizado por la política aplicable |

La matriz no define roles concretos.

Define únicamente que cada Command requiere una decisión de
autorización previa.

---

# Principio de Propiedad

Permission no implica ownership.

Un actor autorizado para ejecutar un Command sobre una Notification
no se convierte en propietario del Aggregate.

Debe mantenerse:

```text
Authorization

≠

Aggregate Ownership
```

Notification tampoco introduce una regla obligatoria de ownership
organizacional en la versión 1.0.

Cuando una política externa utilice:

```text
OrganizationId

CitizenId

MembershipId

RoleId
```

dicha política permanece fuera del Aggregate salvo que una regla de
dominio explícita indique lo contrario.

---

# Principio de Delegación

La delegación de permisos pertenece al modelo de autorización de
AURA.

Notification no:

- crea delegaciones;
- revoca delegaciones;
- administra Roles;
- administra Memberships;
- administra políticas de acceso.

Si un actor actúa mediante una delegación válida, la Application
Layer debe resolver dicha condición antes de invocar el Aggregate.

Debe mantenerse:

```text
Delegated Authorization

↓

Application Layer

↓

Notification Command
```

---

# Restricciones

Ningún permiso puede permitir:

- modificar NotificationId;
- modificar NotificationStatus directamente;
- modificar Version directamente;
- evitar la Aggregate Root;
- evitar Lifecycle;
- evitar State Machine;
- evitar Invariants;
- ejecutar una transición inexistente;
- modificar directamente otro Aggregate;
- convertir una operación inválida en válida;
- generar un Domain Event de éxito después de una operación
  rechazada.

Debe mantenerse:

```text
Permission Granted

≠

Invariant Bypass
```

---

# Permisos sobre Estados

La autorización de un Command no altera las reglas del estado
actual.

Por ejemplo, un actor autorizado para:

```text
ConfirmNotificationDelivery
```

no puede ejecutarlo si:

```text
NotificationStatus = Draft
```

porque:

```text
Draft → Delivered
```

no forma parte del Lifecycle.

Del mismo modo, un actor autorizado para:

```text
RetryNotification
```

no puede ejecutarlo cuando:

```text
NotificationStatus = Delivered
```

porque Delivered es terminal.

---

# Auditoría

Toda decisión relevante de autorización puede ser registrada por el
contexto responsable de Audit.

Conceptualmente, una entrada de auditoría puede contener:

```text
Actor

AggregateId = NotificationId

Command

OccurredAt

Result

RejectionReason
```

cuando exista un motivo de rechazo.

Audit permanece fuera del Aggregate Notification.

Notification no almacena registros de auditoría como parte de su
estado interno.

Debe mantenerse:

```text
Authorization Decision

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

# Integración con RBAC

Notification es compatible con Role-Based Access Control.

En un modelo RBAC:

```text
Actor

    │
    ▼

Role

    │
    ▼

Permission

    │
    ▼

Command
```

puede determinar si un actor está autorizado.

Notification no conoce:

- estructura interna de Roles;
- asignaciones de Roles;
- jerarquías de Roles;
- almacenamiento de permisos.

El Aggregate recibe únicamente la intención autorizada.

La definición concreta de Roles permanece en el contexto
responsable.

---

# Integración con ABAC

Notification también es compatible con Attribute-Based Access
Control.

Una política ABAC puede considerar atributos externos y atributos
ya existentes del dominio.

Conceptualmente:

```text
Actor Attributes

+

Resource Attributes

+

Context

+

Command

↓

Authorization Decision
```

Entre los atributos de Notification que una política externa puede
considerar se encuentran conceptualmente:

```text
NotificationStatus

Command
```

y otros atributos oficialmente definidos cuando correspondan.

La política ABAC:

- no se almacena dentro del Aggregate;
- no modifica Notification;
- no sustituye Invariants;
- no crea nuevas transiciones.

---

# Compatibilidad con Event Sourcing

Una operación autorizada y válida puede producir un Domain Event.

Conceptualmente:

```text
Authorized Command

↓

Valid Domain Operation

↓

Domain Event
```

Una operación autorizada pero inválida:

```text
Authorized Command

↓

Domain Rejection
```

no produce un Domain Event de éxito.

La autorización no altera la historia del Aggregate.

En una implementación Event Sourcing, los hechos históricos
continúan representando únicamente operaciones de dominio que
realmente ocurrieron.

---

# Compatibilidad con CQRS

El modelo de Permissions es compatible con CQRS.

En el Write Side:

```text
Authorization

↓

Command

↓

Notification
```

La autorización de escritura debe preceder al Command.

En el Read Side pueden existir políticas de autorización
independientes para consultas y proyecciones.

La autorización de lectura no pertenece al Aggregate Notification.

Debe mantenerse:

```text
Read Permission

≠

Write Permission
```

cuando las políticas aplicables sean distintas.

---

# Evolución

El modelo de Permissions puede evolucionar mediante cambios en:

- Roles externos;
- Memberships;
- políticas RBAC;
- políticas ABAC;
- reglas organizacionales;
- políticas de Application Layer.

Estos cambios no requieren modificar Notification mientras no
alteren sus reglas de dominio.

Si se incorpora un nuevo Command al Aggregate, debe definirse
explícitamente:

- su intención;
- su relación con Lifecycle;
- su relación con State Machine;
- sus Invariants;
- su autorización correspondiente.

Un nuevo permiso no crea automáticamente un nuevo Command.

Debe mantenerse:

```text
New Permission

≠

New Domain Behavior
```

---

# Definición de Éxito

El modelo de Permissions del Aggregate **Notification** garantiza
que la autorización permanezca separada de las reglas internas del
dominio.

La versión 1.0 establece que los Commands:

```text
CreateNotification

QueueNotification

ConfirmNotificationDelivery

ReportNotificationDeliveryFailure

RetryNotification
```

requieren autorización previa conforme a la política aplicable.

El modelo garantiza que:

- Authentication permanece fuera del Aggregate;
- Authorization permanece fuera del Aggregate;
- Notification no administra usuarios ni sesiones;
- Notification no almacena tokens ni credenciales;
- no se introducen roles internos obligatorios;
- cada Command requiere autorización previa;
- autorización no implica ownership;
- delegación permanece fuera del Aggregate;
- ningún permiso puede evitar Lifecycle;
- ningún permiso puede evitar State Machine;
- ningún permiso puede evitar Invariants;
- ningún permiso puede modificar directamente NotificationStatus;
- una operación autorizada todavía puede ser rechazada;
- una operación rechazada no modifica estado ni Version;
- una operación rechazada no genera Domain Events de éxito;
- Audit permanece separado;
- RBAC puede aplicarse externamente;
- ABAC puede aplicarse externamente;
- CQRS puede mantener políticas distintas para lectura y escritura;
- Event Sourcing registra únicamente hechos realmente ocurridos;
- la evolución de políticas externas no altera automáticamente el
  dominio Notification.

De esta forma, `DOMAIN-011F-Permissions.md` establece el modelo
conceptual de autorización del Aggregate **Notification** conforme
al patrón consolidado de AURA Core.