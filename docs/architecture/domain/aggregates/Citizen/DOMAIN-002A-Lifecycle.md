# DOMAIN-002A — Citizen Lifecycle

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Citizen Management

Aggregate:
Citizen

Documento relacionado:

- DOMAIN-002-Aggregate.md
- DOMAIN-002B-State-Machine.md
- DOMAIN-002D-Domain-Events.md
- DOMAIN-002E-Invariants.md

---

# Objetivo

Este documento define el ciclo de vida oficial del Aggregate
Citizen.

Describe las etapas por las que transita una identidad
ciudadana desde su creación hasta su retiro permanente del
ecosistema AURA.

El Lifecycle representa únicamente la evolución funcional del
Aggregate. Las reglas de transición se documentan de manera
formal en el State Machine.

---

# Principios

El ciclo de vida debe garantizar:

- identidad única;
- trazabilidad completa;
- evolución controlada;
- cumplimiento de invariantes;
- compatibilidad con Event Sourcing;
- preparación para auditoría.

---

# Etapas del ciclo de vida

El Aggregate Citizen evoluciona mediante las siguientes
etapas.

```text
Draft
    │
    ▼
Pending Verification
    │
    ▼
Verified
    │
    ▼
Active
    │
    ├──────────────┐
    ▼              │
Suspended          │
    │              │
    ▼              │
Active ◄───────────┘
    │
    ▼
Inactive
    │
    ▼
Archived
```

---

# Draft

Representa una identidad recién creada.

Características:

- posee CitizenId;
- aún no es visible para otros Bounded Contexts;
- admite modificaciones completas;
- no participa del dominio.

Eventos típicos:

- CitizenDraftCreated

---

# Pending Verification

La identidad requiere validaciones antes de incorporarse al
ecosistema.

Ejemplos:

- validación documental;
- validación municipal;
- validación mediante proveedor de identidad;
- revisión manual.

Durante este estado no puede participar en procesos
democráticos.

Eventos típicos:

- CitizenVerificationRequested

---

# Verified

La identidad fue validada.

En este estado:

- la identidad es confiable;
- aún no participa;
- puede esperar aprobación administrativa;
- puede activarse automáticamente.

Eventos:

- CitizenVerified

---

# Active

Representa un ciudadano operativo.

Puede:

- integrarse a organizaciones;
- crear propuestas;
- participar en asambleas;
- votar;
- recibir notificaciones;
- interactuar con servicios municipales.

Es el estado normal del Aggregate.

Eventos:

- CitizenActivated

---

# Suspended

La participación queda temporalmente restringida.

Motivos posibles:

- incumplimiento normativo;
- solicitud administrativa;
- investigación;
- protección de la cuenta;
- suspensión voluntaria.

La identidad permanece íntegra.

No se elimina información.

Eventos:

- CitizenSuspended

---

# Reactivation

Un ciudadano suspendido puede volver al estado Active cuando
desaparecen las condiciones que motivaron la suspensión.

Debe existir:

- autorización;
- auditoría;
- evento registrado.

Evento:

- CitizenReactivated

---

# Inactive

El ciudadano deja de utilizar la plataforma sin eliminar su
historial.

Características:

- conserva relaciones históricas;
- no genera nuevas acciones;
- mantiene integridad referencial;
- puede archivarse posteriormente.

Eventos:

- CitizenDeactivated

---

# Archived

Estado final del Aggregate.

Representa una identidad retirada del ecosistema.

Características:

- sólo lectura;
- no admite modificaciones;
- mantiene trazabilidad;
- conserva eventos históricos;
- mantiene referencias válidas.

No implica eliminación física.

Evento:

- CitizenArchived

---

# Eliminación

Citizen nunca se elimina físicamente.

El dominio utiliza:

Soft Archive

La eliminación permanente pertenece exclusivamente a políticas
de infraestructura y cumplimiento normativo.

---

# Reglas generales

Durante el Lifecycle se cumplen las siguientes reglas:

- CitizenId nunca cambia.
- Version aumenta en cada modificación.
- Todo cambio genera Domain Events.
- Ninguna transición ocurre sin validación.
- El historial permanece inmutable.
- Las referencias externas siguen siendo válidas.

---

# Relaciones con otros Aggregates

El estado del Citizen condiciona el comportamiento de otros
Aggregates.

Ejemplos:

Organization

- puede admitir únicamente ciudadanos Active.

Membership

- no puede crearse para ciudadanos Archived.

Voting

- requiere ciudadanos Active.

Participation

- requiere identidad válida.

Notification

- sólo entrega comunicaciones a ciudadanos habilitados.

---

# Compatibilidad con Event Sourcing

Cada transición del Lifecycle puede reconstruirse mediante la
secuencia de Domain Events.

No existe dependencia del estado almacenado.

---

# Compatibilidad con CQRS

Las proyecciones pueden representar el estado actual sin
consultar directamente el Aggregate.

Ejemplos:

- Citizens activos
- Citizens suspendidos
- Citizens pendientes
- Citizens archivados

---

# Objetivos del Lifecycle

El ciclo de vida garantiza:

- evolución consistente;
- identidad persistente;
- auditoría completa;
- integración segura;
- interoperabilidad con Smart Cities;
- compatibilidad con arquitecturas distribuidas.

---

# Definición de éxito

El Lifecycle del Aggregate Citizen proporciona un modelo
predecible y completamente trazable para administrar la
identidad cívica dentro del ecosistema AURA, permitiendo que
todos los procesos posteriores del dominio operen sobre un
estado consistente y verificable.