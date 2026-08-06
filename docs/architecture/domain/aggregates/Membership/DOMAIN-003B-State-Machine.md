# DOMAIN-003B — Membership State Machine

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

- DOMAIN-003-Aggregate.md
- DOMAIN-003A-Lifecycle.md
- DOMAIN-003C-Commands.md
- DOMAIN-003D-Domain-Events.md
- DOMAIN-003E-Invariants.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Este documento define la máquina de estados oficial del
Aggregate **Membership**.

La State Machine determina todas las transiciones permitidas,
las transiciones prohibidas y los Commands responsables de
modificar el estado de una Membership.

Ningún cambio de estado puede ocurrir fuera de esta máquina.

---

# Principios

La máquina de estados cumple los siguientes principios:

- un único estado activo;
- transiciones explícitas;
- comportamiento determinístico;
- consistencia inmediata;
- trazabilidad completa;
- evolución controlada.

---

# Estados Oficiales

El Aggregate Membership posee los siguientes estados:

```text
Draft

PendingApproval

Approved

Rejected

Active

Suspended

Terminated

Archived
```

Todos los estados son mutuamente excluyentes.

---

# Diagrama Oficial

```text
                    Draft
                      │
      RequestMembership
                      │
                      ▼
             PendingApproval
              ┌──────────────┐
              │              │
ApproveMembership   RejectMembership
              │              │
              ▼              ▼
         Approved        Rejected
              │              │
 ActivateMembership     ArchiveMembership
              │              │
              ▼              ▼
           Active        Archived
          ┌─────┴─────┐
          │           │
SuspendMembership  TerminateMembership
          │           │
          ▼           ▼
     Suspended    Terminated
          │           │
ReactivateMembership │
          │           │
          └─────┬─────┘
                ▼
             Active

Terminated
      │
ArchiveMembership
      │
      ▼
 Archived
```

---

# Estado Draft

Representa una Membership creada pero aún no enviada para
evaluación.

Commands permitidos:

```text
RequestMembership

ArchiveMembership
```

Commands prohibidos:

```text
ApproveMembership

ActivateMembership

SuspendMembership

ReactivateMembership

TerminateMembership
```

---

# Estado PendingApproval

La Membership espera la decisión de la organización.

Commands permitidos:

```text
ApproveMembership

RejectMembership
```

Commands prohibidos:

```text
ActivateMembership

SuspendMembership

TerminateMembership
```

---

# Estado Approved

La Membership ha sido aceptada.

Commands permitidos:

```text
ActivateMembership
```

Commands prohibidos:

```text
SuspendMembership

ReactivateMembership

TerminateMembership
```

---

# Estado Active

Estado operativo normal.

Commands permitidos:

```text
SuspendMembership

TerminateMembership
```

Commands prohibidos:

```text
ApproveMembership

RejectMembership

ActivateMembership
```

---

# Estado Suspended

La Membership conserva su existencia pero pierde
temporalmente sus derechos.

Commands permitidos:

```text
ReactivateMembership

TerminateMembership
```

Commands prohibidos:

```text
ApproveMembership

ActivateMembership
```

---

# Estado Rejected

La solicitud fue rechazada.

Commands permitidos:

```text
ArchiveMembership
```

No existen otros Commands válidos.

---

# Estado Terminated

La relación entre Citizen y Organization ha finalizado.

Commands permitidos:

```text
ArchiveMembership
```

No puede volver al estado Active.

---

# Estado Archived

Estado final.

Commands permitidos:

```text
Ninguno
```

El Aggregate queda completamente inmutable.

---

# Tabla Oficial de Transiciones

| Estado actual | Command | Nuevo estado |
|---------------|---------|--------------|
| Draft | RequestMembership | PendingApproval |
| Draft | ArchiveMembership | Archived |
| PendingApproval | ApproveMembership | Approved |
| PendingApproval | RejectMembership | Rejected |
| Approved | ActivateMembership | Active |
| Active | SuspendMembership | Suspended |
| Active | TerminateMembership | Terminated |
| Suspended | ReactivateMembership | Active |
| Suspended | TerminateMembership | Terminated |
| Rejected | ArchiveMembership | Archived |
| Terminated | ArchiveMembership | Archived |

---

# Transiciones Prohibidas

Las siguientes transiciones nunca pueden ocurrir.

```text
Draft
↓

Active
```

```text
Draft
↓

Approved
```

```text
PendingApproval
↓

Active
```

```text
Rejected
↓

Approved
```

```text
Rejected
↓

Active
```

```text
Archived
↓

Cualquier estado
```

```text
Terminated
↓

Active
```

```text
Approved
↓

Suspended
```

Estas transiciones representan violaciones del dominio.

---

# Domain Events Asociados

Cada transición válida genera exactamente un Domain Event.

| Command | Domain Event |
|----------|--------------|
| CreateMembership | MembershipCreated |
| RequestMembership | MembershipRequested |
| ApproveMembership | MembershipApproved |
| RejectMembership | MembershipRejected |
| ActivateMembership | MembershipActivated |
| SuspendMembership | MembershipSuspended |
| ReactivateMembership | MembershipReactivated |
| TerminateMembership | MembershipTerminated |
| ArchiveMembership | MembershipArchived |

---

# Versionado

Toda transición válida:

- incrementa Version;
- genera un Domain Event;
- preserva el historial.

Las operaciones rechazadas:

- no modifican Version;
- no generan eventos.

---

# Consistencia

Toda transición debe ejecutarse dentro de una única
transacción.

El Aggregate nunca puede quedar en un estado intermedio.

---

# Recuperación mediante Event Sourcing

La reproducción cronológica de los Domain Events reconstruye
exactamente el estado de la Membership.

Ejemplo:

```text
MembershipCreated

↓

MembershipRequested

↓

MembershipApproved

↓

MembershipActivated

↓

MembershipSuspended

↓

MembershipReactivated
```

Resultado:

```text
State = Active
```

---

# Compatibilidad con CQRS

La State Machine pertenece exclusivamente al lado de escritura.

Los Read Models reflejan el estado actual y el historial, pero
nunca ejecutan transiciones.

---

# Validación

Antes de ejecutar cualquier transición deben validarse:

- invariantes;
- permisos;
- versión del Aggregate;
- estado actual;
- reglas de negocio.

Sólo si todas las validaciones son exitosas podrá modificarse el
estado.

---

# Principios Arquitectónicos

La máquina de estados sigue:

- Domain-Driven Design (DDD);
- State Machine Pattern;
- Aggregate Pattern;
- CQRS;
- Event Sourcing;
- Clean Architecture;
- Single Responsibility Principle.

---

# Definición de Éxito

La State Machine del Aggregate **Membership** define de forma
explícita y determinística la evolución de una relación entre
un **Citizen** y una **Organization**. Cada transición está
gobernada por Commands, protegida por invariantes y registrada
mediante Domain Events, garantizando que toda membresía dentro
del ecosistema AURA evolucione de manera consistente,
auditable y alineada con las reglas de negocio.