# DOMAIN-003H — Membership Examples

Versión: 1.1

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
- DOMAIN-003B-State-Machine.md
- DOMAIN-003C-Commands.md
- DOMAIN-003D-Domain-Events.md
- DOMAIN-003E-Invariants.md
- DOMAIN-003F-Permissions.md
- DOMAIN-003G-Repository-Contract.md

---

# Objetivo

Este documento presenta ejemplos de comportamiento del
Aggregate **Membership**.

Los ejemplos ilustran cómo las reglas del dominio se aplican en
situaciones reales dentro del ecosistema AURA.

No representan casos de implementación, sino escenarios de
negocio.

---

# Ejemplo 1 — Solicitud de incorporación

## Escenario

Un ciudadano desea integrarse a una Junta de Vecinos.

Estado inicial:

```text
Citizen
    ✔ Existe

Organization
    ✔ Existe

Membership
    ✖ No existe
```

Proceso:

```text
CreateMembership

↓

RequestMembership
```

Resultado:

```text
State = PendingApproval
```

Eventos generados:

```text
MembershipCreated

MembershipRequested
```

---

# Ejemplo 2 — Incorporación aprobada

La directiva revisa la solicitud.

Estado:

```text
PendingApproval
```

Proceso:

```text
ApproveMembership

↓

ActivateMembership
```

Resultado:

```text
State = Active
```

Eventos:

```text
MembershipApproved

MembershipActivated
```

---

# Ejemplo 3 — Solicitud rechazada

La organización decide no aceptar la incorporación.

Proceso:

```text
RejectMembership

↓

ArchiveMembership
```

Resultado:

```text
State = Archived
```

Eventos:

```text
MembershipRejected

MembershipArchived
```

---

# Ejemplo 4 — Suspensión temporal

Un socio incumple temporalmente el reglamento interno.

Estado inicial:

```text
Active
```

Proceso:

```text
SuspendMembership
```

Resultado:

```text
State = Suspended
```

Evento:

```text
MembershipSuspended
```

El historial permanece íntegro.

---

# Ejemplo 5 — Reactivación

El ciudadano regulariza su situación.

Estado inicial:

```text
Suspended
```

Proceso:

```text
ReactivateMembership
```

Resultado:

```text
State = Active
```

Evento:

```text
MembershipReactivated
```

---

# Ejemplo 6 — Renuncia voluntaria

El ciudadano decide abandonar la organización.

Estado:

```text
Active
```

Proceso:

```text
TerminateMembership

↓

ArchiveMembership
```

Resultado:

```text
State = Archived
```

Eventos:

```text
MembershipTerminated

MembershipArchived
```

---

# Ejemplo 7 — Intento de duplicar una Membership

Estado existente:

```text
Citizen = Juan Pérez

Organization = Junta Vecinal 12

Membership = Active
```

Se intenta crear una segunda Membership activa.

Resultado esperado:

```text
Command Rejected
```

Motivo:

```text
DuplicateActiveMembership
```

No se generan Domain Events.

La versión permanece sin cambios.

---

# Ejemplo 8 — Activación inválida

Estado:

```text
Draft
```

Se ejecuta:

```text
ActivateMembership
```

Resultado:

```text
InvalidStateTransition
```

El Aggregate permanece sin modificaciones.

---

# Ejemplo 9 — Reactivación inválida

Estado:

```text
Terminated
```

Proceso:

```text
ReactivateMembership
```

Resultado:

```text
Command Rejected
```

Razón:

```text
Una Membership terminada nunca puede volver a Active.
```

Debe crearse una nueva Membership.

---

# Ejemplo 10 — Intento de modificar una Membership archivada

Estado:

```text
Archived
```

Proceso:

```text
SuspendMembership
```

Resultado:

```text
Command Rejected
```

Razón:

```text
Archived es un estado terminal.
```

---

# Ejemplo 11 — Incorporación automática

La organización permite ingreso automático.

Proceso:

```text
CreateMembership

↓

RequestMembership

↓

ApproveMembership (Automation)

↓

ActivateMembership (Automation)
```

Resultado:

```text
State = Active
```

Eventos:

```text
MembershipCreated

MembershipRequested

MembershipApproved

MembershipActivated
```

---

# Ejemplo 12 — Cambio de organización

Un ciudadano deja una organización y se integra a otra.

Estado inicial:

```text
Organization A

↓

Membership Active
```

Proceso:

```text
TerminateMembership

↓

ArchiveMembership

↓

CreateMembership

↓

RequestMembership

↓

ApproveMembership

↓

ActivateMembership
```

Resultado:

```text
Organization A

Membership = Archived

Organization B

Membership = Active
```

No existe reutilización del Aggregate original.

---

# Ejemplo 13 — Participación en una Asamblea

Estado:

```text
Membership = Active
```

El ciudadano intenta ingresar a una Asamblea.

Validación:

```text
Membership Active

↓

Permitir participación
```

Si la Membership está suspendida:

```text
Membership Suspended

↓

Acceso denegado
```

---

# Ejemplo 14 — Asignación no definida

Después de activar una Membership no se asigna automáticamente un Role.
La solicitud se rechaza o se difiere hasta que exista un Source of Truth
explícito para la relación Membership–Role.

---

# Ejemplo 15 — Integración con Notification

Después de aprobar una Membership:

```text
MembershipApproved
```

Otro Bounded Context recibe el evento.

Resultado:

```text
Notification

↓

Enviar correo

↓

Enviar mensaje móvil

↓

Registrar confirmación
```

Membership no conoce la existencia del servicio de
notificaciones.

---

# Ejemplo 16 — Integración con FIWARE

Cuando una Membership pasa a estado:

```text
Active
```

Un Integration Event puede sincronizar la información con la
plataforma Smart City.

Ejemplo conceptual:

```text
MembershipActivated

↓

Integration Event

↓

Citizen Context

↓

Municipal API

↓

FIWARE Context Broker
```

La sincronización ocurre fuera del Aggregate.

---

# Buenas Prácticas

Los ejemplos anteriores muestran que:

- el Aggregate nunca modifica otros Aggregates;
- todas las decisiones pasan por Commands;
- todas las transiciones generan Domain Events;
- las reglas de negocio permanecen dentro del Aggregate;
- las integraciones utilizan eventos, nunca referencias
  directas.

---

# Casos No Permitidos

No forman parte del comportamiento válido:

- dos Membership activas para el mismo Citizen en la misma
  Organization;
- reactivar una Membership terminada;
- modificar una Membership archivada;
- cambiar el Citizen asociado;
- cambiar la Organization asociada;
- omitir Domain Events;
- saltar estados de la máquina de estados.

---

# Definición de Éxito

Los ejemplos del Aggregate **Membership** demuestran cómo se
materializan las reglas del dominio en situaciones reales del
ecosistema AURA. Cada escenario confirma que la pertenencia de
un **Citizen** a una **Organization** evoluciona mediante
Commands explícitos, transiciones válidas y Domain Events,
preservando la consistencia, la trazabilidad y la independencia
entre Aggregates conforme a los principios de Domain-Driven
Design.