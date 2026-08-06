# DOMAIN-003E — Membership Invariants

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
- DOMAIN-003B-State-Machine.md
- DOMAIN-003C-Commands.md
- DOMAIN-003D-Domain-Events.md
- DOMAIN-003F-Permissions.md
- CORE-006-Domain-Invariants.md

---

# Objetivo

Este documento define las **invariantes del dominio** para el
Aggregate **Membership**.

Las invariantes representan reglas de negocio que deben ser
verdaderas en todo momento. Ningún Command puede producir un
estado que las viole.

Las invariantes son responsabilidad exclusiva del Aggregate
Root.

---

# Principios

Toda invariante debe cumplir los siguientes principios:

- proteger la consistencia del dominio;
- ser verificable antes del commit;
- permanecer independiente de la infraestructura;
- representar una regla permanente del negocio;
- impedir estados inválidos.

---

# Invariante 1 — Identidad Inmutable

Toda Membership posee un único:

```text
MembershipId
```

Una vez creada:

- nunca cambia;
- nunca se reutiliza;
- nunca se reasigna.

---

# Invariante 2 — Un Único Citizen

Cada Membership pertenece exactamente a un:

```text
CitizenId
```

No puede existir una Membership asociada simultáneamente a
más de un Citizen.

---

# Invariante 3 — Una Única Organization

Cada Membership pertenece exactamente a una:

```text
OrganizationId
```

La organización asociada nunca cambia durante el ciclo de vida
del Aggregate.

---

# Invariante 4 — Unicidad de Membresía Activa

Para una combinación:

```text
CitizenId

+

OrganizationId
```

puede existir como máximo una Membership en estado:

```text
Active
```

Esta es una de las reglas fundamentales del dominio.

---

# Invariante 5 — Estado Válido

Toda Membership debe encontrarse exactamente en uno de los
estados definidos por la máquina de estados:

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

No existen estados intermedios.

---

# Invariante 6 — Transiciones Permitidas

Los cambios de estado sólo pueden realizarse mediante las
transiciones definidas en:

```text
DOMAIN-003B-State-Machine.md
```

Las transiciones no autorizadas deben rechazarse.

---

# Invariante 7 — Membership Archivada

Una Membership en estado:

```text
Archived
```

es completamente inmutable.

No admite:

- modificaciones;
- reactivaciones;
- cambios de estado;
- nuevos Commands.

---

# Invariante 8 — Membership Terminada

Una Membership en estado:

```text
Terminated
```

no puede volver a:

```text
Active
```

Si el Citizen vuelve a integrarse a la misma Organization,
deberá crearse una nueva Membership.

---

# Invariante 9 — Activación

Una Membership sólo puede pasar a:

```text
Active
```

si previamente se encuentra en:

```text
Approved
```

No existen atajos hacia el estado operativo.

---

# Invariante 10 — Suspensión

Sólo una Membership:

```text
Active
```

puede ser suspendida.

No pueden suspenderse Memberships en otros estados.

---

# Invariante 11 — Reactivación

Sólo una Membership:

```text
Suspended
```

puede volver al estado:

```text
Active
```

---

# Invariante 12 — Historial Inmutable

Todo cambio de estado genera un Domain Event.

Los eventos:

- nunca se eliminan;
- nunca se modifican;
- nunca se reemplazan.

---

# Invariante 13 — Versionado

Toda modificación válida incrementa:

```text
Version
```

Las operaciones rechazadas no modifican la versión.

---

# Invariante 14 — Consistencia Transaccional

Cada Command debe ejecutarse completamente o no ejecutarse.

No pueden existir estados parcialmente actualizados.

---

# Invariante 15 — Integridad Referencial del Dominio

Una Membership sólo puede existir si referencia:

```text
CitizenId
```

y

```text
OrganizationId
```

válidos desde la perspectiva del dominio.

El Aggregate mantiene únicamente las identidades, nunca los
objetos completos.

---

# Invariante 16 — Independencia entre Aggregates

Membership nunca modifica directamente:

- Citizen;
- Organization;
- Role;
- Permission;
- Assembly.

Toda colaboración ocurre mediante:

- Commands;
- Domain Events;
- Integration Events.

---

# Invariante 17 — Permisos

Sólo actores autorizados pueden ejecutar Commands sobre una
Membership.

La autorización se valida antes de invocar el Aggregate.

---

# Invariante 18 — Consistencia Temporal

Las fechas deben mantener coherencia cronológica.

Ejemplo conceptual:

```text
AdmissionDate

≤

ActivationDate

≤

TerminationDate
```

Cuando alguno de estos eventos no haya ocurrido, el valor
correspondiente permanecerá vacío.

---

# Invariante 19 — Inmutabilidad de Referencias

Los siguientes atributos nunca cambian después de la creación:

```text
MembershipId

CitizenId

OrganizationId
```

La pertenencia representa una relación histórica específica y
no puede transferirse a otro ciudadano u organización.

---

# Invariante 20 — Fuente Oficial de Verdad

El estado oficial de una Membership reside únicamente en el
Aggregate.

Los Read Models son proyecciones derivadas y pueden
reconstruirse en cualquier momento.

---

# Validación

Las invariantes deben evaluarse:

- antes de modificar el estado;
- antes de emitir Domain Events;
- antes del commit de la transacción.

Si alguna falla, el Command debe abortarse.

---

# Compatibilidad con CQRS

Las invariantes pertenecen exclusivamente al modelo de
escritura.

Los Read Models no validan reglas de negocio.

---

# Compatibilidad con Event Sourcing

Las invariantes se verifican durante la ejecución del Command.

Los Domain Events válidos se convierten en el registro
histórico permanente del Aggregate.

---

# Principios Arquitectónicos

Estas invariantes siguen:

- Domain-Driven Design (DDD);
- Aggregate Pattern;
- Design by Contract;
- CQRS;
- Event Sourcing;
- Clean Architecture;
- Single Responsibility Principle.

---

# Definición de Éxito

Las invariantes del Aggregate **Membership** garantizan que la
relación entre un **Citizen** y una **Organization** permanezca
siempre consistente, única y trazable. Ninguna operación puede
producir estados inválidos, preservando la integridad del
dominio y proporcionando una base sólida para la gestión de
participación, roles y gobernanza dentro del ecosistema AURA.