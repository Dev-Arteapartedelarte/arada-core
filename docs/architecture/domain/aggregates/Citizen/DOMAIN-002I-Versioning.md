# DOMAIN-002I — Citizen Versioning

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Citizen Management

Aggregate:
Citizen

Documentos relacionados:

- DOMAIN-002-Aggregate.md
- DOMAIN-002D-Domain-Events.md
- DOMAIN-002E-Invariants.md
- DOMAIN-002G-Repository-Contract.md
- CORE-016-Dependency-Rules.md

---

# Objetivo

Este documento define la estrategia oficial de versionado del
Aggregate **Citizen**.

El versionado garantiza la consistencia del Aggregate frente a
modificaciones concurrentes, permite la evolución controlada
del dominio y asegura la compatibilidad de los contratos entre
los distintos Bounded Contexts del ecosistema AURA.

---

# Principios

El modelo de versionado sigue los siguientes principios:

- una única versión por Aggregate;
- incremento monotónico;
- concurrencia optimista;
- inmutabilidad de eventos;
- compatibilidad evolutiva;
- trazabilidad completa.

---

# Alcance

El versionado aplica a:

- Aggregate Citizen;
- Domain Events;
- Integration Events;
- contratos públicos;
- Read Models derivados.

No aplica a:

- objetos temporales;
- DTO internos;
- infraestructura.

---

# Versionado del Aggregate

Todo Aggregate Citizen posee un atributo:

```text
Version
```

Su finalidad es identificar el estado consistente más reciente
del Aggregate.

Ejemplo:

```text
Citizen

Version = 1
```

Cada modificación válida incrementa la versión.

```text
1

↓

2

↓

3

↓

4
```

Nunca disminuye.

Nunca se reinicia.

---

# Cuándo aumenta la versión

La versión aumenta únicamente cuando el estado del Aggregate
cambia.

Ejemplos:

```text
RegisterCitizen
```

```text
Version

0 → 1
```

---

```text
VerifyCitizen
```

```text
Version

1 → 2
```

---

```text
UpdateCitizenProfile
```

```text
Version

2 → 3
```

---

```text
SuspendCitizen
```

```text
Version

3 → 4
```

---

Si un Command es rechazado:

```text
Version

4 → 4
```

No existe incremento.

---

# Control de Concurrencia

AURA utiliza **Optimistic Concurrency Control**.

Proceso conceptual:

```text
Read Aggregate

↓

Version = 7

↓

Execute Command

↓

Save

↓

Expected Version = 7
```

Si durante ese intervalo otro proceso modifica el Aggregate:

```text
Stored Version = 8
```

la operación debe rechazarse.

---

# Concurrency Conflict

Cuando ocurre un conflicto:

```text
Expected Version

≠

Stored Version
```

el Repository devuelve:

```text
ConcurrencyConflict
```

La capa de aplicación decidirá si:

- reintenta;
- informa al usuario;
- cancela la operación.

---

# Versionado de Domain Events

Cada Domain Event incluye:

```text
EventVersion
```

Ejemplo:

```text
CitizenActivated

Version 1
```

Si el contrato evoluciona de forma incompatible:

```text
CitizenActivated

Version 2
```

Ambas versiones pueden coexistir mientras existan consumidores
que dependan de ellas.

Los eventos publicados nunca se modifican.

---

# Versionado de Integration Events

Los Integration Events mantienen un esquema de versión propio.

Ejemplo:

```text
CitizenVerifiedIntegrationEvent

v1
```

↓

```text
CitizenVerifiedIntegrationEvent

v2
```

La evolución de los eventos de integración es independiente de
los Domain Events.

---

# Versionado del Aggregate Root

La identidad del Aggregate nunca cambia.

```text
CitizenId
```

permanece constante durante toda la vida del Citizen.

Únicamente evoluciona:

```text
Version
```

---

# Versionado de Value Objects

Los Value Objects no poseen versión individual.

Siempre evolucionan junto al Aggregate.

Ejemplo:

```text
Citizen

Version = 9

↓

Address actualizado

↓

Citizen

Version = 10
```

---

# Versionado de Entidades Internas

Las entidades internas tampoco mantienen una versión propia.

Toda modificación incrementa exclusivamente la versión del
Aggregate Root.

---

# Versionado de Read Models

Los Read Models son reconstruibles.

No constituyen la fuente oficial de verdad.

Si una proyección se pierde:

```text
Domain Events

↓

Replay

↓

Read Model
```

La información puede regenerarse completamente.

---

# Compatibilidad

Toda evolución del Aggregate debe preservar:

- CitizenId;
- significado del dominio;
- invariantes;
- semántica de Commands;
- consistencia de Domain Events.

Los cambios incompatibles requieren una nueva versión del
contrato correspondiente.

---

# Compatibilidad con Event Sourcing

En implementaciones Event Sourcing:

```text
Aggregate Version

=

Número de eventos aplicados
```

Ejemplo:

```text
12 eventos

↓

Version = 12
```

---

# Compatibilidad con CQRS

El lado de escritura utiliza la versión para controlar
concurrencia.

El lado de lectura utiliza la versión únicamente para detectar
actualizaciones pendientes o reconstrucciones de proyecciones.

---

# Evolución

La estrategia de versionado permite:

- agregar nuevos Commands;
- incorporar nuevos Domain Events;
- extender Value Objects;
- evolucionar contratos de integración;
- mantener compatibilidad hacia atrás cuando sea posible.

La evolución nunca debe romper la consistencia del Aggregate.

---

# Principios Arquitectónicos

El modelo de versionado sigue:

- Domain-Driven Design (DDD);
- Optimistic Concurrency Control;
- Event Sourcing;
- CQRS;
- Clean Architecture;
- Open/Closed Principle.

---

# Definición de Éxito

El versionado del Aggregate **Citizen** garantiza que toda
modificación ocurra sobre un estado consistente, evita
conflictos de concurrencia, facilita la evolución del dominio y
preserva la trazabilidad histórica de las identidades cívicas
gestionadas por AURA. Constituye el mecanismo oficial para
coordinar la evolución segura del Aggregate, sus eventos y sus
contratos públicos sin depender de una tecnología específica.