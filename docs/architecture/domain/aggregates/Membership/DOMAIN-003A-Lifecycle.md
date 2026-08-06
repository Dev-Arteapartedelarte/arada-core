# DOMAIN-003A — Membership Lifecycle

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
- DOMAIN-003B-State-Machine.md
- DOMAIN-003C-Commands.md
- DOMAIN-003D-Domain-Events.md
- DOMAIN-003E-Invariants.md
- DOMAIN-002-Aggregate.md
- DOMAIN-001-Aggregate.md

---

# Objetivo

Este documento define el ciclo de vida oficial del Aggregate
**Membership**.

El ciclo de vida describe los estados por los que puede
transitar una membresía desde su creación hasta su archivo
definitivo, asegurando que cada transición represente una
decisión de negocio válida y trazable.

Toda Membership debe encontrarse exactamente en un estado del
ciclo de vida.

---

# Principios

El ciclo de vida debe cumplir los siguientes principios:

- una única fuente de verdad;
- estados mutuamente excluyentes;
- transiciones explícitas;
- historial completo;
- consistencia inmediata;
- evolución controlada.

---

# Ciclo de Vida Oficial

```text
                    Draft
                      │
                      ▼
             PendingApproval
               ┌──────┴──────┐
               ▼             ▼
          Approved      Rejected
               │             │
               ▼             ▼
            Active      Archived
           ┌───┴────┐
           ▼        ▼
     Suspended  Terminated
           │        │
           ▼        ▼
        Active   Archived
```

---

# Estado Draft

Representa una Membership recién creada.

Características:

- aún no existe aprobación;
- puede modificarse;
- no genera derechos de participación;
- puede cancelarse.

Transiciones permitidas:

```text
Draft

↓

PendingApproval
```

o

```text
Draft

↓

Archived
```

---

# Estado PendingApproval

La solicitud fue enviada para evaluación.

Características:

- espera decisión;
- no permite participación;
- mantiene consistencia del proceso.

Transiciones permitidas:

```text
PendingApproval

↓

Approved
```

```text
PendingApproval

↓

Rejected
```

---

# Estado Approved

La Membership fue aceptada por la organización.

Características:

- cumple los requisitos de admisión;
- aún no participa activamente;
- está preparada para activarse.

Transiciones permitidas:

```text
Approved

↓

Active
```

---

# Estado Active

Representa una membresía plenamente vigente.

Características:

- habilita participación;
- permite asignación de roles;
- permite acceso a procesos internos;
- constituye el estado operativo normal.

Transiciones permitidas:

```text
Active

↓

Suspended
```

```text
Active

↓

Terminated
```

---

# Estado Suspended

La Membership continúa existiendo, pero sus derechos quedan
temporalmente suspendidos.

Características:

- conserva el historial;
- no permite ejercer derechos;
- puede reactivarse.

Transiciones permitidas:

```text
Suspended

↓

Active
```

```text
Suspended

↓

Terminated
```

---

# Estado Terminated

La relación entre el Citizen y la Organization finalizó.

Características:

- deja de existir la pertenencia activa;
- conserva la trazabilidad histórica;
- no admite reactivación directa.

Transición permitida:

```text
Terminated

↓

Archived
```

---

# Estado Rejected

La solicitud de membresía fue rechazada.

Características:

- nunca llegó a ser una membresía activa;
- conserva evidencia del proceso;
- no puede activarse.

Transición permitida:

```text
Rejected

↓

Archived
```

---

# Estado Archived

Estado final del Aggregate.

Características:

- inmutable;
- histórico;
- sin operaciones permitidas;
- únicamente disponible para consulta.

No existen transiciones de salida.

---

# Estados Terminales

Los siguientes estados son finales:

```text
Archived
```

Una Membership archivada nunca vuelve al ciclo operativo.

---

# Estados Operativos

Participan de la operación diaria:

```text
Approved

Active

Suspended
```

---

# Estados Administrativos

Representan etapas del proceso de incorporación.

```text
Draft

PendingApproval

Rejected
```

---

# Transiciones Permitidas

```text
Draft
    ↓
PendingApproval

PendingApproval
    ↓
Approved

PendingApproval
    ↓
Rejected

Approved
    ↓
Active

Active
    ↓
Suspended

Suspended
    ↓
Active

Active
    ↓
Terminated

Suspended
    ↓
Terminated

Rejected
    ↓
Archived

Terminated
    ↓
Archived

Draft
    ↓
Archived
```

---

# Transiciones Prohibidas

No están permitidas transiciones como:

```text
Draft
↓

Active
```

```text
Rejected
↓

Active
```

```text
Archived
↓

Active
```

```text
Archived
↓

Draft
```

```text
Terminated
↓

Active
```

Estas violan las reglas del dominio.

---

# Persistencia del Historial

Cada transición:

- incrementa la versión;
- genera un Domain Event;
- conserva la trazabilidad.

El historial completo puede reconstruirse mediante Event
Sourcing.

---

# Integración con Citizen

La Membership sólo puede avanzar hacia estados operativos si el
Citizen asociado cumple las políticas definidas por el dominio
(por ejemplo, identidad verificada o estado activo).

Estas validaciones son coordinadas por los servicios de
aplicación y las políticas de dominio, manteniendo el desacople
entre Aggregates.

---

# Integración con Organization

La Organization puede imponer reglas adicionales para admitir
miembros, tales como:

- aprobación por directorio;
- aceptación automática;
- requisitos documentales;
- validaciones territoriales.

La Membership refleja el resultado de dichas decisiones, sin
incorporar la lógica interna de Organization.

---

# Consistencia

Toda transición debe cumplir:

- invariantes válidas;
- autorización previa;
- una única transacción;
- actualización de versión;
- generación de Domain Events.

---

# Compatibilidad con CQRS

El lado de escritura controla las transiciones del ciclo de
vida.

Los Read Models proyectan el estado actual y el historial de
cada Membership para consultas y reportes.

---

# Compatibilidad con Event Sourcing

Cada cambio de estado queda registrado mediante un Domain Event.

La reproducción de la secuencia de eventos permite reconstruir
íntegramente el ciclo de vida de cualquier Membership.

---

# Principios Arquitectónicos

Este ciclo de vida sigue:

- Domain-Driven Design (DDD);
- State Machine Pattern;
- Aggregate Pattern;
- CQRS;
- Event Sourcing;
- Clean Architecture.

---

# Definición de Éxito

El ciclo de vida del Aggregate **Membership** garantiza que la
relación entre un **Citizen** y una **Organization** evolucione
de manera consistente, trazable y controlada. Cada transición
representa una decisión explícita del dominio, preservando la
integridad histórica y proporcionando la base para la gestión
de participación, roles y gobernanza dentro del ecosistema
AURA.