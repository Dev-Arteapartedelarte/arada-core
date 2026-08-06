# DOMAIN-003I — Membership Versioning

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
- DOMAIN-003G-Repository-Contract.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Este documento define la estrategia oficial de versionado del
Aggregate **Membership**.

El versionado garantiza la consistencia del Aggregate frente a
accesos concurrentes, permite reconstruir su evolución
histórica y proporciona una base estable para CQRS, Event
Sourcing y sincronización entre Bounded Contexts.

---

# Principios

El modelo de versionado sigue los siguientes principios:

- una única versión vigente por Aggregate;
- incremento monotónico;
- inmutabilidad del historial;
- control de concurrencia optimista;
- trazabilidad completa;
- independencia de la infraestructura.

---

# Concepto de Versión

Toda instancia de Membership mantiene un atributo:

```text
Version
```

La versión representa el número de modificaciones exitosas
realizadas sobre el Aggregate.

La versión:

- nunca disminuye;
- nunca se reutiliza;
- nunca se modifica manualmente.

---

# Valor Inicial

Cuando una Membership es creada:

```text
Version = 1
```

Evento asociado:

```text
MembershipCreated
```

---

# Incremento de Versión

Cada Command exitoso incrementa exactamente una unidad.

Ejemplo:

```text
Version 1

↓

CreateMembership

↓

Version 1
```

```text
Version 1

↓

RequestMembership

↓

Version 2
```

```text
Version 2

↓

ApproveMembership

↓

Version 3
```

```text
Version 3

↓

ActivateMembership

↓

Version 4
```

---

# Commands que Incrementan la Versión

Los siguientes Commands modifican el Aggregate y generan una
nueva versión:

| Command | Incrementa versión |
|----------|--------------------|
| CreateMembership | ✔ |
| RequestMembership | ✔ |
| ApproveMembership | ✔ |
| RejectMembership | ✔ |
| ActivateMembership | ✔ |
| SuspendMembership | ✔ |
| ReactivateMembership | ✔ |
| TerminateMembership | ✔ |
| ArchiveMembership | ✔ |

---

# Commands Rechazados

Si un Command es rechazado:

- la versión permanece sin cambios;
- no se generan Domain Events;
- no existe persistencia.

Ejemplo:

```text
Version = 5

↓

SuspendMembership

↓

Estado = Draft

↓

Command Rejected

↓

Version = 5
```

---

# Control de Concurrencia

El Aggregate utiliza:

```text
Optimistic Concurrency Control
```

Proceso conceptual:

```text
Cliente

↓

Version = 7

↓

Command

↓

Repository

↓

Version almacenada = 7

↓

Commit

↓

Version = 8
```

Si la versión almacenada es distinta:

```text
Version Cliente = 7

Version Persistida = 8
```

Resultado:

```text
ConcurrencyConflict
```

---

# Relación con Domain Events

Cada Domain Event registra la versión del Aggregate en el
momento de su emisión.

Ejemplo:

```text
MembershipActivated

AggregateVersion = 4
```

Esto permite:

- reconstrucción cronológica;
- auditoría;
- depuración;
- sincronización.

---

# Relación con Event Sourcing

Cuando se utiliza Event Sourcing:

```text
Version
```

corresponde al número de eventos aplicados al Aggregate.

Ejemplo:

```text
Version = 6

↓

Se aplican seis Domain Events
```

La versión nunca depende del almacenamiento físico.

---

# Relación con Snapshots

Los Snapshots pueden almacenar:

```text
MembershipId

Version

Current State
```

Durante la reconstrucción:

```text
Snapshot

↓

Eventos posteriores

↓

Aggregate reconstruido
```

---

# Compatibilidad con CQRS

El modelo de escritura controla la versión.

Los Read Models pueden conservar una copia para:

- sincronización;
- detección de desfases;
- consistencia eventual.

La versión del Read Model nunca gobierna al Aggregate.

---

# Integración con Repository

El Repository debe verificar la versión antes de persistir.

Proceso:

```text
Load Aggregate

↓

Verificar Version

↓

Aplicar Command

↓

Incrementar Version

↓

Persistir

↓

Commit
```

---

# Integración con Outbox Pattern

Los Domain Events almacenados en Outbox incluyen:

```text
AggregateId

AggregateVersion

OccurredOn
```

Esto garantiza el orden correcto de publicación.

---

# Integración entre Bounded Contexts

Los consumidores externos pueden utilizar la versión para:

- detectar eventos duplicados;
- procesar eventos en orden;
- evitar sobrescrituras;
- reconstruir secuencias.

La versión no reemplaza el identificador del evento.

---

# Reglas de Evolución

La estrategia de versionado debe cumplir:

- compatibilidad hacia atrás;
- incremento monotónico;
- ausencia de reinicios;
- independencia del motor de persistencia.

---

# Errores Relacionados

El modelo puede producir:

```text
ConcurrencyConflict

InvalidVersion

StaleAggregate

PersistenceFailure
```

Estos errores no modifican el estado del Aggregate.

---

# Auditoría

Toda modificación debe registrar:

```text
MembershipId

PreviousVersion

NewVersion

Command

DomainEvent

OccurredOn

ActorId
```

La auditoría facilita el análisis histórico y la trazabilidad
del dominio.

---

# Principios Arquitectónicos

Este modelo sigue:

- Domain-Driven Design (DDD);
- Optimistic Concurrency Control;
- CQRS;
- Event Sourcing;
- Repository Pattern;
- Clean Architecture.

---

# Definición de Éxito

El modelo de versionado del Aggregate **Membership** garantiza
que toda modificación de la relación entre un **Citizen** y una
**Organization** sea consistente, trazable y resistente a
conflictos de concurrencia. Cada cambio incrementa
monótonamente la versión del Aggregate, permitiendo preservar
la integridad del dominio, reconstruir su historia y coordinar
la sincronización con otros Bounded Contexts dentro del
ecosistema AURA.