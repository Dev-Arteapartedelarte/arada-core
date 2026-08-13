# DOMAIN-008I — Participation Versioning

Versión: 1.0

Estado:
Oficial

Proyecto:
AURA Core

Bounded Context:
Participation Management

Aggregate:
Participation

Autor:
ARADA

Documentos Relacionados:

- DOMAIN-008-Aggregate.md
- DOMAIN-008D-Domain-Events.md
- DOMAIN-008G-Repository-Contract.md
- DOMAIN-008K-Integration-Events.md
- CORE-011-Repository-Contracts.md
- CORE-016-Dependency-Rules.md

---

# Objetivo

Definir el modelo oficial de versionado del Aggregate
Participation.

El versionado permite:

- garantizar consistencia;
- detectar conflictos de concurrencia;
- preservar el historial del Aggregate;
- soportar Event Sourcing parcial en el futuro;
- permitir integraciones confiables con otros Bounded
  Contexts.

---

# Principios

El modelo de versionado debe cumplir las siguientes reglas.

- cada Aggregate posee una versión;
- la versión pertenece al Aggregate Root;
- toda modificación válida incrementa la versión;
- la versión nunca disminuye;
- la versión nunca se modifica manualmente;
- las entidades internas no poseen versión propia.

---

# Concepto

La versión representa la revisión actual del Aggregate.

Ejemplo.

```text
Participation

Id:
PAR-001

Version:
7
```

No representa una versión del software.

Representa la evolución del estado del Aggregate.

---

# Ciclo de Vida

Creación.

```text
Participation

↓

Version = 1
```

Primera modificación.

```text
Version = 2
```

Nueva modificación.

```text
Version = 3
```

Y así sucesivamente.

```text
1

↓

2

↓

3

↓

4

↓

5
```

---

# Operaciones que Incrementan la Versión

Las siguientes operaciones generan una nueva versión.

- RegisterParticipation
- ActivateParticipation
- CompleteParticipation
- WithdrawParticipation
- InvalidateParticipation
- ArchiveParticipation
- ChangeParticipationType
- ChangeParticipationContext
- UpdateParticipationMetadata

Toda modificación del estado observable del Aggregate
incrementa la versión.

---

# Operaciones que No Incrementan la Versión

Las siguientes acciones no modifican el Aggregate.

- consultas;
- validaciones;
- lectura del Repository;
- proyecciones;
- generación de Read Models.

Estas operaciones no alteran la versión.

---

# Concurrencia Optimista

El Repository debe utilizar la versión para detectar
actualizaciones concurrentes.

Escenario.

Proceso A.

```text
Participation

Version 12
```

Proceso B.

```text
Participation

Version 12
```

Proceso A guarda correctamente.

```text
Version 13
```

Proceso B intenta guardar utilizando la versión 12.

Resultado.

```text
ConcurrencyConflictError
```

La operación debe rechazarse.

---

# Persistencia

La versión forma parte del estado persistente del
Aggregate.

Representación conceptual.

```text
Participation

Id

Version

State

Type

Context

Metadata
```

No puede almacenarse externamente.

---

# Relación con Domain Events

Cada Domain Event referencia la versión del Aggregate que
lo originó.

Ejemplo.

```text
ParticipationActivated

AggregateVersion:
9
```

Esto permite reconstruir la secuencia lógica de cambios.

---

# Relación con Integration Events

Los Integration Events también deben incluir la versión.

Ejemplo.

```text
ParticipationActivatedIntegrationEvent

AggregateVersion:
9
```

Los consumidores pueden detectar eventos fuera de orden o
duplicados.

---

# Relación con Outbox

El patrón Outbox conserva la versión junto con el evento.

```text
Aggregate

↓

Version 18

↓

Outbox Record

↓

AggregateVersion 18
```

Esto garantiza trazabilidad.

---

# Recuperación

Cuando un Aggregate se recupera desde el Repository.

```text
findById()

↓

Participation

↓

Version 24
```

La versión debe corresponder exactamente al estado
persistido.

---

# Integración con Event Store

En una futura evolución hacia Event Sourcing, la versión
podrá calcularse como el número de eventos aplicados.

Ejemplo.

```text
Event 1

↓

Event 2

↓

Event 3

↓

Version = 3
```

El modelo actual mantiene compatibilidad con este enfoque.

---

# Integración con CQRS

El modelo de escritura mantiene la versión del Aggregate.

El modelo de lectura puede utilizarla para:

- sincronización;
- control de consistencia;
- invalidación de caché;
- reconstrucción de proyecciones.

---

# Versionado del Contrato

Debe distinguirse entre:

Versión del Aggregate.

```text
Participation

Version = 14
```

Versión del evento.

```text
ParticipationActivated

EventVersion = 2
```

Versión de la API.

```text
API v1
```

Son conceptos independientes.

---

# Restricciones

La versión:

- nunca puede ser negativa;
- nunca puede ser nula;
- nunca disminuye;
- nunca se reutiliza;
- nunca se reinicia.

---

# Reglas

## REG-001

Todo Aggregate posee exactamente una versión.

---

## REG-002

Toda modificación válida incrementa la versión en una
unidad.

---

## REG-003

Las operaciones de lectura nunca modifican la versión.

---

## REG-004

La versión pertenece únicamente al Aggregate Root.

---

## REG-005

El Repository utiliza la versión para implementar
concurrencia optimista.

---

## REG-006

Todo Domain Event registra la versión que lo originó.

---

## REG-007

Todo Integration Event publica la versión del Aggregate.

---

## REG-008

La versión forma parte del estado persistente del
Aggregate.

---

## REG-009

Una operación con una versión obsoleta debe finalizar con
un error de concurrencia.

---

## REG-010

El mecanismo de versionado debe ser transparente para los
consumidores del dominio.

---

# Definición de Éxito

El Aggregate `Participation` mantiene un mecanismo de
versionado monotónico, persistente y transparente que
garantiza consistencia, soporta concurrencia optimista,
facilita la trazabilidad de Domain Events e Integration
Events y prepara a AURA Core para futuras evoluciones
hacia CQRS avanzado y Event Sourcing sin modificar el
modelo del dominio.