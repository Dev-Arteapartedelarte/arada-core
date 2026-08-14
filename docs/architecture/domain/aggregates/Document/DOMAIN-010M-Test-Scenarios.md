# DOMAIN-010M — Document Test Scenarios

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Document Management

Aggregate:
Document

Documentos relacionados:

- DOMAIN-010-Aggregate.md
- DOMAIN-010A-Lifecycle.md
- DOMAIN-010B-State-Machine.md
- DOMAIN-010C-Commands.md
- DOMAIN-010D-Domain-Events.md
- DOMAIN-010E-Invariants.md
- DOMAIN-010F-Permissions.md
- DOMAIN-010G-Repository-Contract.md
- DOMAIN-010I-Versioning.md

---

# Objetivo

Este documento define los escenarios oficiales de prueba del
Aggregate **Document**.

Los escenarios verifican el comportamiento esperado del
Aggregate desde la perspectiva del dominio, asegurando que las
reglas de negocio, las Invariants y la State Machine se cumplan
correctamente.

No describen pruebas de Infrastructure, interfaces de usuario
ni APIs.

---

# Principios

Las pruebas del dominio deben validar:

- comportamiento observable;
- Invariants;
- transiciones de estado;
- generación de Domain Events;
- control de versiones;
- consistencia del Aggregate.

Las pruebas nunca dependen de una base de datos, un framework
o una tecnología específica.

---

# Escenario 1 — Crear un Document

## Dado

No existe un Aggregate con el DocumentId solicitado.

## Cuando

```text
CreateDocument
```

## Entonces

- se crea un nuevo Aggregate;
- el estado inicial es:

```text
Draft
```

- la versión es:

```text
Version = 1
```

- se publica:

```text
DocumentCreated
```

---

# Escenario 2 — Publicar un Document

## Dado

Un Document en estado:

```text
Draft
```

## Cuando

```text
PublishDocument
```

## Entonces

- el estado cambia a:

```text
Published
```

- la versión aumenta;
- se publica:

```text
DocumentPublished
```

---

# Escenario 3 — Archivar un Document

## Dado

Un Document en estado:

```text
Published
```

## Cuando

```text
ArchiveDocument
```

## Entonces

- el estado cambia a:

```text
Archived
```

- la versión aumenta;
- se publica:

```text
DocumentArchived
```

---

# Escenario 4 — Publicación inválida desde Published

## Dado

Un Document en estado:

```text
Published
```

## Cuando

```text
PublishDocument
```

## Entonces

La operación es rechazada.

El estado permanece:

```text
Published
```

La versión no aumenta.

No se genera:

```text
DocumentPublished
```

---

# Escenario 5 — Archivado inválido desde Draft

## Dado

Un Document en estado:

```text
Draft
```

## Cuando

```text
ArchiveDocument
```

## Entonces

La operación es rechazada.

El estado permanece:

```text
Draft
```

La versión no aumenta.

No se genera:

```text
DocumentArchived
```

---

# Escenario 6 — Publicación inválida desde Archived

## Dado

Un Document en estado:

```text
Archived
```

## Cuando

```text
PublishDocument
```

## Entonces

La operación es rechazada.

El Aggregate permanece inmutable.

No se genera:

```text
DocumentPublished
```

---

# Escenario 7 — Archivado inválido desde Archived

## Dado

Un Document en estado:

```text
Archived
```

## Cuando

```text
ArchiveDocument
```

## Entonces

La operación es rechazada.

El Aggregate permanece inmutable.

No se genera:

```text
DocumentArchived
```

---

# Escenario 8 — Estado inicial inválido

## Dado

Se intenta crear un Document directamente en:

```text
Published
```

o:

```text
Archived
```

## Cuando

Se intenta ejecutar la creación.

## Entonces

La operación es rechazada.

Todo Document nuevo debe comenzar en:

```text
Draft
```

No se genera:

```text
DocumentCreated
```

---

# Escenario 9 — DocumentId inmutable

## Dado

Un Document existente con:

```text
DocumentId = D1
```

## Cuando

Una operación intenta modificar su identidad a:

```text
DocumentId = D2
```

## Entonces

La operación es rechazada.

El Aggregate conserva:

```text
DocumentId = D1
```

La versión no aumenta.

No se genera ningún Domain Event de éxito.

---

# Escenario 10 — DocumentType inválido

## Dado

Se intenta crear un Document con un DocumentType que no satisface
las reglas del dominio.

## Cuando

```text
CreateDocument
```

## Entonces

La operación es rechazada.

No se crea el Aggregate.

No se incrementa Version.

No se genera:

```text
DocumentCreated
```

---

# Escenario 11 — Modificación directa de DocumentStatus

## Dado

Un Document válido.

## Cuando

Se intenta modificar directamente:

```text
DocumentStatus
```

sin ejecutar el comportamiento definido por la Aggregate Root.

## Entonces

La modificación no está permitida.

El estado permanece sin cambios.

La versión permanece sin cambios.

No se genera Domain Event de éxito.

---

# Escenario 12 — Modificación directa de Content

## Dado

Un Document válido.

## Cuando

Se intenta modificar directamente:

```text
Content
```

evitando el comportamiento explícito de la Aggregate Root.

## Entonces

La modificación no está permitida.

El Aggregate conserva su estado confirmado.

La versión permanece sin cambios.

---

# Escenario 13 — Conflicto de concurrencia

## Dado

```text
Version = 7
```

## Cuando

Otro proceso persiste:

```text
Version = 8
```

y posteriormente se intenta guardar una modificación basada en:

```text
ExpectedVersion = 7
```

## Entonces

El Repository devuelve:

```text
ConcurrencyConflict
```

No se sobrescribe la versión persistida.

No se confirma la modificación incompatible.

---

# Escenario 14 — Violación de Invariant

## Dado

Un Command intenta dejar al Document en un estado que viola una
Invariant.

## Cuando

Se ejecuta el comportamiento correspondiente.

## Entonces

La operación es rechazada.

No se persiste ningún cambio.

La versión no aumenta.

No se generan Domain Events de éxito.

---

# Escenario 15 — Verificación de Permissions

## Dado

Un actor sin autorización.

## Cuando

Intenta ejecutar:

```text
PublishDocument
```

## Entonces

La capa de aplicación rechaza el Command.

El Aggregate nunca es invocado.

DocumentStatus permanece sin cambios.

Version permanece sin cambios.

---

# Escenario 16 — Permission no evita Invariants

## Dado

Un actor autorizado para solicitar:

```text
ArchiveDocument
```

y un Document en estado:

```text
Draft
```

## Cuando

Se intenta ejecutar:

```text
ArchiveDocument
```

## Entonces

El Aggregate rechaza la operación.

La autorización no permite la transición:

```text
Draft → Archived
```

El estado permanece:

```text
Draft
```

La versión no aumenta.

No se genera:

```text
DocumentArchived
```

---

# Escenario 17 — Reconstrucción mediante Event Sourcing

## Dado

La secuencia:

```text
DocumentCreated

DocumentPublished

DocumentArchived
```

## Cuando

Se reproducen todos los eventos correspondientes al mismo
DocumentId.

## Entonces

El Aggregate reconstruido posee:

```text
DocumentStatus = Archived
```

La identidad permanece igual.

La Version corresponde a la posición lógica resultante de la
secuencia aplicada.

La reconstrucción no genera nuevos Domain Events.

---

# Escenario 18 — Reconstrucción de Read Models

## Dado

Una proyección de Document eliminada.

## Cuando

Se ejecuta un replay completo de los Domain Events disponibles.

## Entonces

El Read Model se reconstruye a partir de los hechos confirmados.

El Aggregate Document no es modificado.

No se incrementa Version.

No se generan nuevos Domain Events.

---

# Escenario 19 — Ausencia de Integration Event automático

## Dado

El Aggregate ejecuta correctamente:

```text
PublishDocument
```

y produce:

```text
DocumentPublished
```

## Cuando

La transacción es confirmada.

## Entonces

No debe inferirse automáticamente un Integration Event.

La publicación externa solamente puede ocurrir cuando exista un
contrato de Integration Event explícitamente definido.

Debe mantenerse:

```text
DocumentPublished

≠

Mandatory Integration Event
```

---

# Escenario 20 — Document asociado a Assembly

## Dado

Una Assembly mantiene una referencia:

```text
DocumentId
```

## Cuando

El Document cambia válidamente:

```text
Draft → Published
```

## Entonces

Document produce:

```text
DocumentPublished
```

El cambio no modifica directamente:

```text
AssemblyStatus
```

Assembly permanece fuera del Consistency Boundary de Document.

---

# Escenario 21 — Archivado conserva identidad

## Dado

Un Document Published con:

```text
DocumentId = D1
```

## Cuando

```text
ArchiveDocument
```

## Entonces

el estado resultante es:

```text
Archived
```

y:

```text
DocumentId = D1
```

permanece inmutable.

Se genera:

```text
DocumentArchived
```

Archived no significa eliminación física.

---

# Escenario 22 — Verificación de Domain Event

## Dado

Un Command válido que produce un hecho de dominio.

## Cuando

La operación es aceptada por Document.

## Entonces

el Domain Event correspondiente debe mantener:

```text
correct event type

correct payload

correct aggregate id

correct aggregate version

correct causation

correct correlation
```

El evento solamente existe después de una operación válida.

---

# Escenario 23 — Domain Event no generado después de rechazo

## Dado

```text
DocumentStatus = Published
```

## Cuando

```text
PublishDocument
```

## Entonces

La operación es rechazada.

Debe verificarse:

```text
event not generated after rejected command
```

específicamente:

```text
DocumentPublished
```

no debe existir como resultado de esa operación.

---

# Escenario 24 — Preservación histórica de Domain Events

## Dado

La secuencia:

```text
DocumentCreated

DocumentPublished

DocumentArchived
```

## Cuando

El Document alcanza:

```text
Archived
```

## Entonces

los hechos anteriores permanecen preservados.

`DocumentArchived` no reescribe:

```text
DocumentPublished
```

y `DocumentPublished` no reescribe:

```text
DocumentCreated
```

Debe verificarse:

```text
historical values preserved
```

---

# Escenario 25 — Idempotencia del consumidor

## Dado

Un Integration Event explícitamente definido por un contrato de
integración y recibido más de una vez con el mismo:

```text
EventId
```

## Cuando

El consumidor procesa las entregas repetidas.

## Entonces

debe mantenerse la suposición de:

```text
consumer idempotency
```

Dos entregas con el mismo EventId representan el mismo Integration
Event.

La entrega repetida no constituye automáticamente un nuevo hecho de
dominio.

---

# Cobertura Esperada

El conjunto mínimo de pruebas debe cubrir:

- Commands;
- transiciones de estado;
- Invariants;
- Permissions;
- Versioning;
- Domain Events;
- Integration Events;
- reconstrucción;
- concurrencia;
- consistencia.

---

# Automatización

Estos escenarios deben implementarse como pruebas automatizadas del
dominio.

Cada escenario debe ser:

- independiente;
- repetible;
- determinístico;
- aislado;
- rápido de ejecutar.

---

# Criterios de Aceptación

El Aggregate **Document** será considerado conforme cuando:

- todos los escenarios sean exitosos;
- ninguna Invariant pueda violarse;
- todas las transiciones respeten la State Machine;
- todos los Commands válidos generen los Domain Events esperados;
- los Commands rechazados no generen Domain Events de éxito;
- toda modificación válida incremente Version;
- las operaciones rechazadas conserven Version;
- los conflictos de concurrencia sean detectados correctamente;
- Archived permanezca terminal;
- DocumentId permanezca inmutable;
- los Read Models puedan reconstruirse desde los hechos
  disponibles;
- ningún Integration Event sea inferido automáticamente desde un
  Domain Event;
- otros Aggregates permanezcan fuera del Consistency Boundary.

---

# Principios Arquitectónicos

Este conjunto de pruebas sigue:

- Domain-Driven Design (DDD);
- Behavior-Driven Development (BDD);
- CQRS;
- Event Sourcing;
- Clean Architecture;
- Specification by Example.

---

# Definición de Éxito

Los escenarios definidos en este documento constituyen la
especificación ejecutable del Aggregate **Document**.

Su objetivo es garantizar que la implementación futura preserve
íntegramente:

- la identidad de Document;
- el estado inicial Draft;
- la transición Draft → Published;
- la transición Published → Archived;
- el carácter terminal de Archived;
- las Invariants;
- las Permissions;
- el Versioning;
- los Domain Events;
- el Repository Contract;
- el Consistency Boundary;
- la reconstrucción de Read Models;
- la separación entre Domain Events e Integration Events;
- la independencia respecto de Infrastructure.

De esta forma, `DOMAIN-010M-Test-Scenarios.md` establece los
escenarios oficiales de prueba del Aggregate **Document** conforme
al patrón consolidado de AURA Core.