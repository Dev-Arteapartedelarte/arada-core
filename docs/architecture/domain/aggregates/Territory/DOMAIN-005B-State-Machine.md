# DOMAIN-005B — Territory State Machine

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Territorial Management

Aggregate:
Territory

Documentos relacionados:

- DOMAIN-005-Aggregate.md
- DOMAIN-005A-Lifecycle.md
- DOMAIN-005C-Commands.md
- DOMAIN-005D-Domain-Events.md
- DOMAIN-005E-Invariants.md
- DOMAIN-005J-Consistency-Boundary.md

---

# Objetivo

Definir la máquina de estados oficial del Aggregate
**Territory**, especificando los estados válidos, las
transiciones permitidas, los comandos que las originan y las
restricciones que garantizan la consistencia del dominio.

La máquina de estados representa el único mecanismo autorizado
para modificar el estado operacional de un Territory.

---

# Principios

Toda transición debe cumplir los siguientes principios:

- un único estado activo a la vez;
- transiciones explícitas;
- invariantes verificadas antes de cada cambio;
- cambios atómicos;
- publicación de Domain Events;
- trazabilidad completa.

---

# Estados

El Aggregate puede encontrarse únicamente en uno de los
siguientes estados:

```text
Draft

PendingValidation

Active

Inactive

Archived
```

No existen estados implícitos.

---

# Máquina de Estados

```text
                 create()

                    │
                    ▼

               +-----------+
               |   Draft   |
               +-----------+
                     │
      requestValidation()
                     │
                     ▼
        +------------------------+
        | PendingValidation      |
        +------------------------+
          │                  │
 approve()│                  │reject()
          ▼                  ▼
 +----------------+      +-----------+
 |    Active      |◄─────|   Draft   |
 +----------------+      +-----------+
      │       │
      │       │deactivate()
      │       ▼
      │ +---------------+
      │ |   Inactive    |
      │ +---------------+
      │        │
      │activate()│
      └──────────┘
          │
 archive()│
          ▼
 +----------------+
 |   Archived     |
 +----------------+
```

Archived es un estado terminal.

---

# Estado: Draft

Representa un territorio recién creado.

Características:

- información inicial registrada;
- no puede ser utilizado por otros Aggregates;
- admite edición completa.

Comandos permitidos:

```text
rename()

changeType()

changeAdministrativeCode()

changeGeometry()

changeParent()

updateMetadata()

requestValidation()
```

---

# Estado: PendingValidation

El territorio se encuentra en proceso de validación.

Objetivos:

- validar datos administrativos;
- verificar jerarquía;
- validar geometría;
- comprobar reglas del dominio.

Comandos permitidos:

```text
approve()

reject()

updateMetadata()
```

No admite activación directa.

---

# Estado: Active

Estado operativo.

Puede ser utilizado por:

- Organization;
- Assembly;
- Document;
- otros procesos territoriales.

Comandos permitidos:

```text
rename()

changeType()

changeAdministrativeCode()

changeGeometry()

changeParent()

updateMetadata()

deactivate()

archive()
```

---

# Estado: Inactive

Estado temporal.

Características:

- mantiene identidad;
- conserva relaciones históricas;
- impide nuevas asociaciones operativas.

Comandos permitidos:

```text
activate()

archive()

updateMetadata()
```

---

# Estado: Archived

Estado final.

Características:

- sólo lectura;
- sin modificaciones;
- sin nuevas transiciones;
- preservación histórica.

No existen comandos válidos.

---

# Tabla de Transiciones

| Estado actual | Comando | Estado siguiente |
|----------------|----------|------------------|
| Draft | requestValidation() | PendingValidation |
| PendingValidation | approve() | Active |
| PendingValidation | reject() | Draft |
| Active | deactivate() | Inactive |
| Inactive | activate() | Active |
| Active | archive() | Archived |
| Inactive | archive() | Archived |

Cualquier otra transición debe rechazarse.

---

# Transiciones Prohibidas

Las siguientes transiciones nunca son válidas:

```text
Draft
    │
    ▼
Active
```

```text
Draft
    │
    ▼
Archived
```

```text
PendingValidation
        │
        ▼
Archived
```

```text
Archived
      │
      ▼
Active
```

```text
Archived
      │
      ▼
Inactive
```

```text
Archived
      │
      ▼
Draft
```

---

# Validaciones Previas

Antes de ejecutar cualquier transición deben verificarse:

- estado actual;
- permisos del actor;
- invariantes del Aggregate;
- integridad jerárquica;
- unicidad del código administrativo;
- inexistencia de ciclos territoriales.

Si alguna validación falla:

```text
TransitionRejected
```

La transacción completa debe revertirse.

---

# Eventos Emitidos

Cada transición válida genera un Domain Event.

```text
Draft
        │
TerritoryCreated
        │
PendingValidation
        │
TerritoryValidationRequested
        │
TerritoryValidated
        │
Active
        │
TerritoryActivated
        │
Inactive
        │
TerritoryDeactivated
        │
Archived
        │
TerritoryArchived
```

Nunca se generan eventos para transiciones rechazadas.

---

# Consistencia

Cada transición ocurre dentro de una única transacción del
Aggregate.

El cambio de estado y la publicación del evento asociado forman
parte de la misma unidad lógica de consistencia.

---

# Auditoría

Toda transición registra:

```text
TerritoryId

ActorId

OrganizationId

PreviousState

CurrentState

OccurredOn

CorrelationId

CausationId
```

La información de auditoría es inmutable.

---

# Compatibilidad

La máquina de estados es compatible con:

- Domain-Driven Design (DDD);
- Clean Architecture;
- CQRS;
- Event Sourcing;
- Event-Driven Architecture.

---

# Definición de Éxito

La máquina de estados del Aggregate **Territory** garantiza que
todas las transiciones de estado sean explícitas, auditables y
consistentes, preservando las invariantes del dominio y
asegurando una evolución controlada de cada territorio dentro
del ecosistema AURA.