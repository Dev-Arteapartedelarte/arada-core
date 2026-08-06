# DOMAIN-003 — Membership Aggregate

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Membership Management

Aggregate:
Membership

Documentos relacionados:

- DOMAIN-001-Aggregate.md
- DOMAIN-002-Aggregate.md
- CORE-002-Bounded-Context-Map.md
- CORE-007-Strategic-Design.md
- CORE-008-Aggregate-Design-Rules.md
- CORE-011-Repository-Contracts.md

---

# Objetivo

El Aggregate **Membership** representa la relación formal entre
un **Citizen** y una **Organization**.

Mientras el Aggregate **Citizen** administra la identidad de una
persona y el Aggregate **Organization** administra la identidad
de una organización, el Aggregate **Membership** administra el
vínculo entre ambos.

Toda participación dentro del ecosistema AURA depende de la
existencia de una Membership válida.

---

# Definición

Una Membership representa la pertenencia oficial de un
ciudadano a una organización.

La Membership es responsable de controlar:

- incorporación;
- aceptación;
- activación;
- suspensión;
- reactivación;
- finalización;
- historial de pertenencia.

No administra directamente:

- roles;
- permisos;
- votaciones;
- documentos;
- propuestas.

Estos pertenecen a otros Aggregates.

---

# Responsabilidades

El Aggregate Membership tiene las siguientes responsabilidades:

- mantener el vínculo Citizen–Organization;
- garantizar una única membresía activa por ciudadano y organización;
- controlar el ciclo de vida de la membresía;
- aplicar las reglas de ingreso y salida;
- generar eventos del dominio;
- preservar la trazabilidad histórica.

---

# Responsabilidades Fuera del Aggregate

No es responsabilidad de Membership:

- administrar organizaciones;
- administrar ciudadanos;
- autenticar usuarios;
- asignar permisos técnicos;
- enviar notificaciones;
- ejecutar procesos de auditoría;
- gestionar sesiones.

---

# Aggregate Root

```text
Membership
```

El Aggregate Root es la única puerta de entrada para modificar
el estado de una Membership.

Ninguna entidad interna puede modificarse directamente.

---

# Identidad

Cada Membership posee una identidad única e inmutable.

```text
MembershipId
```

La identidad nunca cambia durante toda la vida del Aggregate.

---

# Relaciones

El Aggregate mantiene referencias únicamente por identidad.

```text
Membership

│

├── CitizenId

└── OrganizationId
```

Nunca mantiene referencias directas a otros Aggregates.

---

# Estado Principal

Conceptualmente una Membership mantiene:

```text
MembershipId

CitizenId

OrganizationId

Status

AdmissionDate

ActivationDate

TerminationDate

Reason

Version
```

Los detalles de implementación pertenecen al código fuente.

---

# Ciclo de Vida

El ciclo de vida oficial será desarrollado en:

```text
DOMAIN-003A-Lifecycle.md
```

Estados previstos:

```text
Draft

↓

PendingApproval

↓

Approved

↓

Active

↓

Suspended

↓

Terminated

↓

Archived
```

---

# Comportamientos Principales

El Aggregate podrá ejecutar, entre otros, los siguientes
Commands:

```text
CreateMembership

RequestMembership

ApproveMembership

RejectMembership

ActivateMembership

SuspendMembership

ReactivateMembership

TerminateMembership

ArchiveMembership
```

Los Commands completos se documentan en:

```text
DOMAIN-003C-Commands.md
```

---

# Eventos del Dominio

El Aggregate genera hechos relevantes para el resto del sistema.

Ejemplos:

```text
MembershipCreated

MembershipRequested

MembershipApproved

MembershipActivated

MembershipSuspended

MembershipReactivated

MembershipTerminated

MembershipArchived
```

La definición completa vive en:

```text
DOMAIN-003D-Domain-Events.md
```

---

# Invariantes

Entre las principales reglas del dominio:

- una Membership pertenece a un único Citizen;
- una Membership pertenece a una única Organization;
- no pueden existir dos Membership activas para el mismo
  Citizen dentro de la misma Organization;
- una Membership archivada es inmutable;
- toda transición debe respetar la máquina de estados;
- toda modificación incrementa la versión.

Las invariantes completas se describen en:

```text
DOMAIN-003E-Invariants.md
```

---

# Consistencia

El Aggregate constituye un límite de consistencia.

Dentro del Aggregate:

- consistencia inmediata;
- una única transacción;
- invariantes siempre válidas.

Fuera del Aggregate:

- consistencia eventual mediante eventos.

---

# Colaboración con otros Aggregates

Membership colabora conceptualmente con:

```text
Citizen

Organization

Role

Permission

Assembly

Proposal

Vote

Notification
```

La colaboración se realiza mediante:

- referencias por identidad;
- Domain Events;
- Integration Events.

Nunca mediante acceso directo al estado interno de otros
Aggregates.

---

# Versionado

Toda modificación válida incrementa:

```text
Version
```

La concurrencia se controla mediante:

```text
Optimistic Concurrency Control
```

---

# Fuente de Verdad

La fuente oficial de verdad es el propio Aggregate Membership y
su historial de Domain Events.

Los Read Models son proyecciones reconstruibles.

---

# Integración

Los cambios relevantes pueden propagarse mediante
Integration Events hacia:

- Organization Context;
- Identity Context;
- Notification Context;
- Analytics Context;
- FIWARE;
- plataformas municipales;
- sistemas externos.

---

# Principios Arquitectónicos

El Aggregate Membership sigue los principios de:

- Domain-Driven Design (DDD);
- Aggregate Pattern;
- Clean Architecture;
- CQRS;
- Event Sourcing;
- Event-Driven Architecture;
- High Cohesion;
- Low Coupling;
- Open/Closed Principle.

---

# Definición de Éxito

El Aggregate **Membership** constituye el núcleo de la relación
entre ciudadanos y organizaciones dentro del ecosistema AURA.
Su responsabilidad es garantizar que toda pertenencia sea
consistente, trazable y evolucione conforme a las reglas del
dominio, proporcionando la base sobre la cual se construyen los
roles, permisos, procesos de participación y mecanismos de
gobernanza de la plataforma.