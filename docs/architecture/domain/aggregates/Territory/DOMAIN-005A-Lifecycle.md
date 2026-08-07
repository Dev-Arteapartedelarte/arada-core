# DOMAIN-005A — Territory Lifecycle

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
- DOMAIN-005B-State-Machine.md
- DOMAIN-005C-Commands.md
- DOMAIN-005D-Domain-Events.md
- DOMAIN-005E-Invariants.md
- DOMAIN-005J-Consistency-Boundary.md

---

# Objetivo

Definir el ciclo de vida oficial del Aggregate **Territory**,
describiendo las etapas que experimenta una unidad territorial
desde su creación hasta su retiro lógico del dominio.

El ciclo de vida garantiza que un territorio evolucione de
forma consistente, preservando las invariantes del dominio y la
integridad de las relaciones con el resto de los Aggregates.

---

# Principios

El ciclo de vida del Aggregate se basa en los siguientes
principios:

- identidad inmutable;
- transiciones controladas;
- preservación de invariantes;
- trazabilidad completa;
- consistencia transaccional;
- publicación de eventos del dominio.

---

# Ciclo de Vida

Todo Territory evoluciona siguiendo el flujo:

```text
Draft
    │
    ▼
PendingValidation
    │
    ▼
Active
    │
    ├──────────────┐
    ▼              │
Inactive           │
    │              │
    └──────► Active│
    │
    ▼
Archived
```

No existen transiciones fuera de este flujo.

---

# Etapa 1 — Draft

Estado inicial del Aggregate.

Características:

- TerritoryId asignado;
- información mínima registrada;
- aún no disponible para uso;
- puede modificarse libremente.

Operaciones permitidas:

- rename();
- changeType();
- changeAdministrativeCode();
- changeGeometry();
- changeParent();
- updateMetadata();
- requestValidation().

Evento asociado:

```text
TerritoryCreated
```

---

# Etapa 2 — PendingValidation

El territorio espera validación administrativa.

Objetivos:

- verificar información territorial;
- validar jerarquía;
- comprobar unicidad del código administrativo;
- revisar integridad de la información geográfica.

Operaciones permitidas:

- approve();
- reject();
- updateMetadata().

Eventos posibles:

```text
TerritoryValidationRequested

TerritoryValidated

TerritoryValidationRejected
```

---

# Etapa 3 — Active

Estado operativo del Aggregate.

El territorio puede ser referenciado por:

- Organization;
- Assembly;
- Document;
- procesos territoriales.

Operaciones permitidas:

- rename();
- changeType();
- changeAdministrativeCode();
- changeGeometry();
- changeParent();
- updateMetadata();
- deactivate();
- archive().

Evento principal:

```text
TerritoryActivated
```

---

# Etapa 4 — Inactive

Estado temporal.

El territorio permanece registrado, pero no admite nuevas
asociaciones operativas.

Puede utilizarse para:

- reorganización territorial;
- procesos administrativos;
- suspensión temporal.

Operaciones permitidas:

- activate();
- archive();
- updateMetadata().

Evento asociado:

```text
TerritoryDeactivated
```

---

# Etapa 5 — Archived

Estado final del ciclo de vida.

El Aggregate conserva únicamente información histórica.

Características:

- no admite modificaciones;
- no puede volver a Active;
- mantiene trazabilidad completa;
- conserva referencias históricas.

Evento asociado:

```text
TerritoryArchived
```

---

# Transiciones Permitidas

| Estado origen | Estado destino |
|----------------|----------------|
| Draft | PendingValidation |
| PendingValidation | Active |
| PendingValidation | Draft |
| Active | Inactive |
| Inactive | Active |
| Active | Archived |
| Inactive | Archived |

Toda transición distinta debe rechazarse.

---

# Transiciones Prohibidas

No están permitidas transiciones como:

```text
Draft
    ▼
Active
```

```text
Archived
    ▼
Active
```

```text
Archived
    ▼
Inactive
```

```text
Draft
    ▼
Archived
```

Estas transiciones violan el modelo del dominio.

---

# Identidad

Durante todo el ciclo de vida permanecen inmutables:

```text
TerritoryId
```

La identidad nunca cambia.

---

# Evolución Permitida

Pueden modificarse únicamente mediante Commands válidos:

- nombre;
- tipo;
- código administrativo;
- referencia geográfica;
- territorio padre;
- metadatos.

Toda modificación genera una nueva versión del Aggregate.

---

# Consistencia

Antes de cada transición deben validarse:

- invariantes;
- reglas jerárquicas;
- unicidad;
- estado actual;
- permisos del actor.

Si alguna validación falla:

```text
TransactionRollback
```

---

# Eventos

Cada transición válida genera un Domain Event.

Ejemplo:

```text
Draft
    │
TerritoryCreated
    │
PendingValidation
    │
TerritoryValidated
    │
Active
    │
TerritoryActivated
```

Nunca se generan eventos para operaciones rechazadas.

---

# Auditoría

Toda transición registra:

```text
ActorId

OrganizationId

TerritoryId

PreviousState

NewState

OccurredOn

CorrelationId

CausationId
```

La auditoría es inmutable.

---

# Compatibilidad

Este ciclo de vida es compatible con:

- Domain-Driven Design (DDD);
- CQRS;
- Event Sourcing;
- Event-Driven Architecture;
- Clean Architecture.

---

# Definición de Éxito

El ciclo de vida del Aggregate **Territory** garantiza que toda
unidad territorial evolucione de forma controlada, preservando
su identidad, respetando las reglas del dominio y manteniendo
la coherencia entre las organizaciones, procesos y estructuras
territoriales que dependen de ella dentro del ecosistema AURA.