# DOMAIN-003J — Membership Consistency Boundary

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
- DOMAIN-003E-Invariants.md
- DOMAIN-003G-Repository-Contract.md
- DOMAIN-001J-Consistency-Boundary.md
- DOMAIN-002J-Consistency-Boundary.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Este documento define el límite oficial de consistencia
(**Consistency Boundary**) del Aggregate **Membership**.

El Aggregate constituye la unidad mínima de consistencia
transaccional del dominio. Todas las reglas críticas que afectan
a una Membership deben preservarse dentro de este límite y
garantizarse mediante una única transacción.

Fuera de este límite sólo existe consistencia eventual.

---

# Definición del Límite

El Aggregate Membership encapsula completamente:

- identidad de la Membership;
- estado del ciclo de vida;
- relación entre Citizen y Organization;
- historial de versiones;
- reglas de transición;
- invariantes propias.

Todo cambio sobre estos elementos ocurre de forma atómica.

---

# Responsabilidad del Aggregate

El Aggregate es responsable de garantizar:

- identidad única;
- unicidad de la Membership activa;
- transiciones válidas;
- consistencia del ciclo de vida;
- emisión de Domain Events;
- incremento de versión.

Ningún otro Aggregate puede modificar estas reglas.

---

# Información Interna

Forma parte del límite de consistencia:

```text
MembershipId

CitizenId

OrganizationId

Status

AdmissionDate

ActivationDate

TerminationDate

ArchiveDate

Version

Pending Domain Events
```

Toda esta información debe permanecer consistente después de
cada Command.

---

# Información Externa

Los siguientes elementos pertenecen a otros Aggregates y sólo
son conocidos mediante sus identidades:

```text
CitizenId

OrganizationId

```

Membership nunca mantiene referencias directas a objetos
externos.

---

# Relaciones entre Aggregates

```text
Citizen
        │
        │ Identity Only
        ▼
+-------------------------+
|      Membership         |
+-------------------------+
        ▲
        │ Identity Only
        │
Organization
```

La relación se mantiene exclusivamente mediante identificadores.

---

# Operaciones Atómicas

Las siguientes operaciones deben ejecutarse completamente o no
ejecutarse:

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

Cada operación representa una única transacción.

---

# Consistencia Inmediata

Debe existir consistencia inmediata para:

- estado actual;
- versión;
- identidad;
- invariantes;
- Domain Events pendientes.

El Aggregate nunca puede quedar parcialmente actualizado.

---

# Consistencia Eventual

La colaboración con otros Bounded Contexts ocurre mediante Integration
Events explícitos y consistencia eventual. Membership no participa en asignaciones de Role ni concede autorización
implícita.

Ejemplos:

```text
Membership

↓

Notification
```

```text
Membership

↓

Audit
```

```text
Membership

↓

Analytics
```

```text
Membership

↓

FIWARE Integration
```

Estos procesos consumen Integration Events y no forman parte de
la transacción del Aggregate.

---

# Reglas que Deben Permanecer Internas

Nunca deben salir del Aggregate:

- validación del estado;
- transición de estados;
- incremento de versión;
- generación de Domain Events;
- validación de invariantes.

Estas responsabilidades pertenecen exclusivamente al Aggregate
Root.

---

# Reglas que Pueden Delegarse

Las siguientes decisiones pueden delegarse a otros componentes:

- autenticación;
- autorización;
- envío de notificaciones;
- indexación para búsquedas;
- generación de estadísticas;
- sincronización con sistemas externos.

La delegación nunca compromete la consistencia del Aggregate.

---

# Colaboración entre Aggregates

La colaboración ocurre mediante:

```text
Commands
```

y

```text
Domain Events
```

Cuando un evento abandona el Bounded Context se transforma en:

```text
Integration Event
```

No existen llamadas directas entre Aggregates.

---

# Consistencia y Repository

El Repository garantiza que:

```text
Load Aggregate

↓

Validate Version

↓

Execute Command

↓

Validate Invariants

↓

Persist Aggregate

↓

Persist Domain Events

↓

Commit
```

Todo ocurre dentro de una única unidad de trabajo.

---

# Consistencia y CQRS

El modelo de escritura mantiene la consistencia inmediata.

Los Read Models son proyecciones derivadas y pueden presentar
consistencia eventual.

Si un Read Model se pierde, puede reconstruirse a partir de los
Domain Events.

---

# Consistencia y Event Sourcing

Cuando Event Sourcing está habilitado:

- el Aggregate se reconstruye aplicando Domain Events;
- las invariantes se verifican durante la ejecución de los
  Commands;
- el historial nunca se modifica.

La consistencia permanece en el Aggregate, no en el Event Store.

---

# Escenario de Consistencia

Ejemplo:

```text
ApproveMembership

↓

MembershipApproved

↓

ActivateMembership

↓

MembershipActivated
```

Resultado:

```text
Membership

State = Active

Version = Incrementada

Eventos = Persistidos
```

Si cualquiera de estos pasos falla:

```text
Rollback
```

No existe estado intermedio.

---

# Operaciones Fuera del Límite

Las siguientes acciones nunca forman parte de la transacción del
Aggregate:

- envío de correos electrónicos;
- notificaciones móviles;
- actualización de dashboards;
- sincronización con FIWARE;
- actualización de motores de búsqueda;
- generación de reportes.

Todas se ejecutan después del commit.

---

# Beneficios del Límite de Consistencia

El diseño permite:

- alta cohesión;
- bajo acoplamiento;
- escalabilidad;
- paralelismo;
- independencia tecnológica;
- trazabilidad completa;
- facilidad para Event Sourcing;
- compatibilidad con microservicios.

---

# Principios Arquitectónicos

Este documento sigue:

- Domain-Driven Design (DDD);
- Aggregate Pattern;
- Consistency Boundary;
- CQRS;
- Event Sourcing;
- Clean Architecture;
- Transactional Consistency.

---

# Definición de Éxito

El **Consistency Boundary** del Aggregate **Membership**
garantiza que toda modificación sobre la relación entre un
**Citizen** y una **Organization** ocurra de manera atómica,
consistente y verificable. Todas las reglas críticas del dominio
permanecen encapsuladas dentro del Aggregate, mientras que la
colaboración con otros Bounded Contexts se realiza mediante
eventos y consistencia eventual, asegurando la integridad y la
escalabilidad del ecosistema AURA.