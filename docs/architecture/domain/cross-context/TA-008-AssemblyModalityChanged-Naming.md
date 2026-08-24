# TA-008 — AssemblyModalityChanged Naming

Versión: 1.0

Estado:
Resolved

Proyecto:
AURA Core

Baseline de referencia:
domain-model-v1.0.0

Alcance:
Transversal

Aggregate:
Assembly

Bounded Context:
Assembly Management

---

# Objetivo

Resolver de forma normativa la inconsistencia documental existente
en el nombre del Domain Event que representa el cambio de modalidad
de una Assembly.

La resolución preserva el modelo de dominio existente y no
introduce nuevos:

* estados;
* Commands;
* Domain Events;
* Integration Events;
* Aggregates;
* Consistency Boundaries.

---

# Hallazgo

La documentación de Assembly presentaba dos denominaciones para el
mismo hecho conceptual:

```text
AssemblyModalityChanged
```

y:

```text
AssemblyModeChanged
```

La documentación formal del Aggregate utiliza además:

```text
AssemblyModality
```

y:

```text
ChangeAssemblyModality
```

como términos del lenguaje ubicuo.

La coexistencia de:

```text
Modality
```

y:

```text
Mode
```

para representar el mismo concepto producía una divergencia
terminológica transversal.

---

# Decisión

El nombre canónico y único del Domain Event que representa el cambio
de modalidad de Assembly es:

```text
AssemblyModalityChanged
```

La cadena normativa queda definida como:

```text
AssemblyModality
        │
        ▼
ChangeAssemblyModality
        │
        ▼
AssemblyModalityChanged
```

---

# Nombre Canónico

Debe utilizarse:

```text
AssemblyModalityChanged
```

en toda referencia al hecho formal mediante el cual cambia la
modalidad de una Assembly.

Este nombre pertenece al lenguaje ubicuo oficial del Aggregate
Assembly.

---

# Terminología Divergente

La denominación:

```text
AssemblyModeChanged
```

no constituye un segundo Domain Event.

Tampoco constituye un alias oficial.

Representa exclusivamente una divergencia documental respecto del
nombre canónico:

```text
AssemblyModalityChanged
```

---

# AssemblyModality

El concepto de dominio utilizado para representar la modalidad de
realización de una Assembly es:

```text
AssemblyModality
```

Ejemplos conceptuales:

```text
InPerson

Remote

Hybrid
```

Debe mantenerse:

```text
AssemblyModality
    ≠
AssemblyMode
```

como regla terminológica normativa.

`AssemblyMode` no constituye un concepto adicional del dominio.

---

# Command Canónico

El Command oficial utilizado para solicitar un cambio de modalidad
es:

```text
ChangeAssemblyModality
```

Debe mantenerse:

```text
ChangeAssemblyModality
        │
        ▼
AssemblyModalityChanged
```

cuando la operación sea válida y el cambio haya sido confirmado por
el Aggregate.

---

# ChangeAssemblyMode

La denominación:

```text
ChangeAssemblyMode
```

no constituye un Command oficial adicional.

No debe utilizarse como equivalente normativo de:

```text
ChangeAssemblyModality
```

---

# Domain Event Canónico

El hecho consumado se expresa exclusivamente mediante:

```text
AssemblyModalityChanged
```

Este Domain Event representa que la modalidad de una Assembly fue
modificada válidamente.

No representa intención.

No representa un Integration Event.

No introduce una nueva transición de Lifecycle.

---

# Payload Conceptual

Cuando corresponda representar el cambio de modalidad, la
terminología debe mantener:

```text
AssemblyId

OrganizationId

PreviousModality

NewModality
```

Debe evitarse utilizar:

```text
PreviousMode

NewMode
```

para representar el mismo hecho.

---

# PreviousModality

`PreviousModality` representa la modalidad existente antes del
cambio confirmado.

Debe utilizar el mismo lenguaje conceptual que:

```text
AssemblyModality
```

---

# NewModality

`NewModality` representa la modalidad válida después del cambio
confirmado.

Debe utilizar el mismo lenguaje conceptual que:

```text
AssemblyModality
```

---

# No Nuevo Domain Event

Esta resolución no crea:

```text
AssemblyModeChanged
```

como Domain Event adicional.

Debe mantenerse:

```text
AssemblyModalityChanged
    =
unique canonical Domain Event
```

para el cambio de modalidad.

---

# No Alias Normativo

No debe mantenerse:

```text
AssemblyModeChanged
    =
alias of AssemblyModalityChanged
```

como contrato oficial.

La normalización documental debe utilizar únicamente:

```text
AssemblyModalityChanged
```

---

# Commands

Esta decisión no introduce nuevos Commands.

Se conserva:

```text
ChangeAssemblyModality
```

como Command oficial.

No se incorpora:

```text
ChangeAssemblyMode
```

al catálogo normativo.

---

# Domain Events

Esta decisión no introduce nuevos Domain Events.

El evento oficial existente permanece:

```text
AssemblyModalityChanged
```

y cualquier referencia documental a:

```text
AssemblyModeChanged
```

que describa el mismo hecho debe normalizarse al nombre canónico.

---

# Integration Events

Esta decisión no introduce ni elimina Integration Events.

Cuando el cambio de modalidad sea relevante para un contrato de
integración existente, el Domain Event origen debe identificarse
como:

```text
AssemblyModalityChanged
```

La resolución TA-008 no modifica la semántica de los Integration
Events existentes.

---

# AssemblyDetailsChanged

Cuando el contrato:

```text
AssemblyDetailsChanged
```

se utilice para comunicar externamente un cambio de modalidad, el
Domain Event relacionado debe ser:

```text
AssemblyModalityChanged
```

sujeto a las reglas condicionales definidas por el contrato de
interoperabilidad correspondiente.

---

# Lifecycle

Esta decisión no modifica el Lifecycle de Assembly.

Un cambio de modalidad no introduce por sí mismo un nuevo estado.

Debe mantenerse:

```text
AssemblyModality
    ≠
AssemblyStatus
```

---

# State Machine

Esta decisión no introduce nuevas transiciones.

Las condiciones que determinan cuándo:

```text
ChangeAssemblyModality
```

puede ejecutarse permanecen definidas por el modelo oficial del
Aggregate Assembly.

---

# Invariantes

Esta resolución no introduce nuevas invariantes.

El cambio de modalidad continúa sujeto a las invariantes ya
establecidas para Assembly.

Si una modificación de modalidad es rechazada:

```text
AssemblyModalityChanged
```

no debe producirse como hecho confirmado.

---

# Consistency Boundary

Esta decisión no modifica el Consistency Boundary de Assembly.

Debe mantenerse:

```text
Aggregate Boundary
    =
Immediate Consistency Boundary
```

El cambio de nombre documental del evento no altera ninguna frontera
de consistencia.

---

# Regla Normativa

La terminología oficial queda establecida como:

```text
AssemblyModality
        │
        ▼
ChangeAssemblyModality
        │
        ▼
AssemblyModalityChanged
```

Deben considerarse divergencias documentales:

```text
AssemblyMode

ChangeAssemblyMode

AssemblyModeChanged

PreviousMode

NewMode
```

cuando se utilicen para representar los mismos conceptos formales.

---

# Regla de Normalización

Toda documentación normativa que describa el hecho formal de cambio
de modalidad debe utilizar:

```text
AssemblyModalityChanged
```

Toda referencia al Command correspondiente debe utilizar:

```text
ChangeAssemblyModality
```

Toda referencia al concepto de modalidad debe utilizar:

```text
AssemblyModality
```

---

# Restricciones

Esta decisión no autoriza:

* crear AssemblyMode como nuevo concepto del dominio;
* crear ChangeAssemblyMode como nuevo Command;
* crear AssemblyModeChanged como nuevo Domain Event;
* mantener AssemblyModeChanged como alias normativo;
* crear PreviousMode o NewMode como terminología normativa paralela;
* modificar el Lifecycle de Assembly;
* modificar la State Machine;
* modificar invariantes;
* modificar Permissions;
* modificar el Consistency Boundary;
* introducir nuevos Integration Events;
* introducir nuevos Aggregates.

---

# Decisiones Técnicas Fuera de Alcance

Esta resolución no define:

* clases;
* nombres de tablas;
* persistencia;
* serialización;
* schemas;
* endpoints;
* APIs;
* brokers;
* transport;
* Outbox;
* Inbox;
* migraciones;
* consumidores;
* mecanismos de compatibilidad técnica.

Estas decisiones no forman parte de TA-008.

---

# Impacto Documental

La resolución debe mantenerse coherente en:

```text
DOMAIN-006-Aggregate.md

DOMAIN-006C-Commands.md

DOMAIN-006D-Domain-Events.md

DOMAIN-006E-Invariants.md

DOMAIN-006H-Examples.md

DOMAIN-006K-Integration-Events.md

DOMAIN-006L-Read-Model.md

DOMAIN-006M-Test-Scenarios.md

CROSS-001-Transversal-Audit.md

event-catalog.md
```

Cuando alguno de estos documentos represente el hecho formal de
cambio de modalidad, debe utilizar:

```text
AssemblyModalityChanged
```

---

# Baseline

El tag:

```text
domain-model-v1.0.0
```

permanece como referencia histórica inmutable.

Esta resolución no modifica retrospectivamente el contenido del
baseline etiquetado.

La normalización corresponde a la consolidación documental posterior
de los contratos de dominio.

---

# Resolución

TA-008 queda:

```text
Resolved
```

con la siguiente terminología normativa:

```text
AssemblyModality

ChangeAssemblyModality

AssemblyModalityChanged

PreviousModality

NewModality
```

La denominación:

```text
AssemblyModeChanged
```

queda clasificada exclusivamente como divergencia documental y no
como Domain Event adicional ni alias oficial.

Esta resolución no modifica el Aggregate Assembly, su Lifecycle,
State Machine, Commands, Domain Events, invariantes, Integration
Events ni Consistency Boundary más allá de la normalización
terminológica del concepto ya existente.