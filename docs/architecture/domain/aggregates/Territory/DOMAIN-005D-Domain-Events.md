# DOMAIN-005D — Territory Domain Events

Versión: 1.1

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
- DOMAIN-005B-State-Machine.md
- DOMAIN-005C-Commands.md
- DOMAIN-005E-Invariants.md
- DOMAIN-005J-Consistency-Boundary.md
- DOMAIN-005K-Integration-Events.md

---

# Objetivo

Definir los Domain Events generados y registrados por el Aggregate
**Territory** cuando ocurre un cambio significativo y
válidamente confirmado dentro del dominio.

Un Domain Event representa un hecho que ya ocurrió.

Los eventos no representan intenciones ni solicitudes.

---

# Principios

Los Domain Events de Territory deben cumplir:

- representar hechos consumados;
- ser inmutables;
- poseer identidad propia;
- identificar al Aggregate que los originó;
- contener la información necesaria para comprender el hecho;
- mantener trazabilidad;
- respetar el límite del Aggregate;
- no contener lógica de negocio.

---

# Estructura Común

Todo Domain Event de Territory debe contener como mínimo:

```text
EventId

AggregateId

AggregateType

EventType

OccurredOn

AggregateVersion

CorrelationId

CausationId
```

Cuando corresponda, puede incluir:

```text
ActorId

OrganizationId
```

---

# TerritoryCreated

Representa la creación exitosa de un Territory.

```text
EventType:
TerritoryCreated
```

Datos principales:

```text
TerritoryId

TerritoryName

TerritoryType

AdministrativeCode

ParentTerritoryId

OccurredOn
```

Este evento se emite cuando el Aggregate pasa a:

```text
Draft
```

---

# TerritoryValidationRequested

Representa la solicitud formal de validación de un Territory.

```text
EventType:
TerritoryValidationRequested
```

Datos:

```text
TerritoryId

ActorId

OccurredOn
```

El evento indica que el Territory entró en:

```text
PendingValidation
```

---

# TerritoryValidated

Representa la validación exitosa de un Territory.

```text
EventType:
TerritoryValidated
```

Datos:

```text
TerritoryId

ActorId

OccurredOn
```

Este evento precede la activación operacional del territorio.

---

# TerritoryValidationRejected

Representa el rechazo de la validación de un Territory.

```text
EventType:
TerritoryValidationRejected
```

Datos:

```text
TerritoryId

ActorId

Reason

OccurredOn
```

El Territory retorna a:

```text
Draft
```

---

# TerritoryActivated

Representa la activación de un Territory.

```text
EventType:
TerritoryActivated
```

Datos:

```text
TerritoryId

ActorId

OccurredOn
```

El nuevo estado es:

```text
Active
```

---

# TerritoryDeactivated

Representa la desactivación temporal de un Territory.

```text
EventType:
TerritoryDeactivated
```

Datos:

```text
TerritoryId

ActorId

Reason

OccurredOn
```

El nuevo estado es:

```text
Inactive
```

---

# TerritoryArchived

Representa el archivado definitivo del Territory.

```text
EventType:
TerritoryArchived
```

Datos:

```text
TerritoryId

ActorId

Reason

OccurredOn
```

El nuevo estado es:

```text
Archived
```

Después de este evento no existen nuevas transiciones del
Aggregate.

---

# TerritoryRenamed

Representa un cambio válido del nombre del territorio.

```text
EventType:
TerritoryRenamed
```

Datos:

```text
TerritoryId

PreviousName

NewName

ActorId

OccurredOn
```

---

# TerritoryTypeChanged

Representa un cambio de clasificación territorial.

```text
EventType:
TerritoryTypeChanged
```

Datos:

```text
TerritoryId

PreviousType

NewType

ActorId

OccurredOn
```

---

# AdministrativeCodeChanged

Representa un cambio válido del código administrativo.

```text
EventType:
AdministrativeCodeChanged
```

Datos:

```text
TerritoryId

PreviousCode

NewCode

ActorId

OccurredOn
```

El nuevo código debe haber superado previamente las reglas
de unicidad correspondientes.

---

# TerritoryGeometryChanged

Representa una modificación de la referencia geográfica del
territorio.

```text
EventType:
TerritoryGeometryChanged
```

Datos:

```text
TerritoryId

PreviousGeometryReference

NewGeometryReference

ActorId

OccurredOn
```

El evento no contiene necesariamente la geometría completa si
esta pertenece a un sistema GIS externo.

---

# TerritoryParentChanged

Representa un cambio en la jerarquía territorial.

```text
EventType:
TerritoryParentChanged
```

Datos:

```text
TerritoryId

PreviousParentTerritoryId

NewParentTerritoryId

ActorId

OccurredOn
```

El cambio sólo puede producirse cuando las reglas de jerarquía
territorial hayan sido satisfechas.

---

# TerritoryMetadataUpdated

Representa una modificación de metadatos del Territory.

```text
EventType:
TerritoryMetadataUpdated
```

Datos:

```text
TerritoryId

ChangedFields

ActorId

OccurredOn
```

No debe utilizarse para ocultar cambios estructurales que
requieran eventos específicos.

---

# Relación Command → Event

Los Commands expresan intención.

Los Domain Events representan el resultado confirmado.

```text
CreateTerritory
        │
        ▼
TerritoryCreated
```

```text
RequestTerritoryValidation
        │
        ▼
TerritoryValidationRequested
```

```text
ApproveTerritory
        │
        ├── TerritoryValidated
        │
        └── TerritoryActivated
```

```text
RejectTerritory
        │
        ▼
TerritoryValidationRejected
```

```text
RenameTerritory
        │
        ▼
TerritoryRenamed
```

```text
ChangeTerritoryType
        │
        ▼
TerritoryTypeChanged
```

```text
ChangeAdministrativeCode
        │
        ▼
AdministrativeCodeChanged
```

```text
ChangeGeometry
        │
        ▼
TerritoryGeometryChanged
```

```text
ChangeParentTerritory
        │
        ▼
TerritoryParentChanged
```

```text
UpdateTerritoryMetadata
        │
        ▼
TerritoryMetadataUpdated
```

```text
DeactivateTerritory
        │
        ▼
TerritoryDeactivated
```

```text
ActivateTerritory
        │
        ▼
TerritoryActivated
```

```text
ArchiveTerritory
        │
        ▼
TerritoryArchived
```

---

# Regla Fundamental

Un Command rechazado **no genera Domain Event**.

Ejemplo:

```text
RenameTerritory
      │
      ▼
Invariant violation
      │
      ▼
Rejected
      │
      X
No Domain Event
```

Los eventos sólo se publican después de que:

1. el Command haya sido autorizado;
2. las invariantes hayan sido verificadas;
3. la transición haya sido aceptada;
4. el nuevo estado haya sido confirmado.

---

# Inmutabilidad

Una vez publicado un Domain Event:

```text
EventId
EventType
AggregateId
OccurredOn
Payload
```

no pueden modificarse.

Si existe un error, debe generarse un nuevo evento correctivo
según las reglas de versionado del dominio.

---

# Orden de Eventos

Los eventos pertenecientes a un mismo Aggregate deben mantener
un orden lógico determinado por:

```text
AggregateVersion
```

Ejemplo:

```text
Version 1
TerritoryCreated

Version 2
TerritoryValidationRequested

Version 3
TerritoryValidated

Version 4
TerritoryActivated
```

No debe existir una versión posterior aplicada antes que una
versión anterior.

---

# Consistencia

Los Domain Events se generan como consecuencia de una
transacción válida del Aggregate.

El estado del Aggregate y los eventos correspondientes deben
representar la misma operación de dominio.

La publicación hacia otros sistemas puede utilizar mecanismos
de entrega eventual.

---

# CorrelationId

Todos los eventos relacionados con una misma operación
distribuida deben compartir:

```text
CorrelationId
```

Esto permite reconstruir un flujo completo a través de
múltiples Aggregates y Bounded Contexts.

---

# CausationId

Cuando un evento provoca posteriormente otra operación, el
evento derivado debe conservar la relación causal mediante:

```text
CausationId
```

Esto permite reconstruir:

```text
Command
   ↓
Domain Event
   ↓
Application Handler
   ↓
New Command
   ↓
New Domain Event
```

---

# Eventos y otros Aggregates

Los Domain Events de Territory permanecen dentro de Territorial
Management. Otros contextos sólo reciben Integration Events explícitos
definidos en DOMAIN-005K.

Ejemplo:

```text
TerritoryActivated
        │
        ├── Organization
        ├── Assembly
        ├── Participation
        ├── Read Models
        └── Audit
```

Los consumidores no modifican directamente el Aggregate
Territory.

---

# Domain Events vs Integration Events

Los Domain Events representan hechos dentro del dominio.

Los Integration Events representan hechos preparados para
ser comunicados fuera del límite del Bounded Context.

Por lo tanto:

```text
Domain Event
      │
      ▼
Integration Boundary
      │
      ▼
Integration Event
```

La definición específica de Integration Events pertenece a:

```text
DOMAIN-005K-Integration-Events.md
```

---

# Auditoría

Los Domain Events deben permitir reconstruir:

```text
qué ocurrió;

sobre qué Territory ocurrió;

cuándo ocurrió;

quién originó la operación;

qué versión del Aggregate produjo el evento;

qué operación causó el evento.
```

Los eventos no deben depender de un mecanismo externo de
auditoría para conservar su significado de dominio.

---

# Compatibilidad

El modelo de Domain Events es compatible con:

- Domain-Driven Design (DDD);
- CQRS;
- Event Sourcing;
- Event-Driven Architecture;
- Clean Architecture;
- arquitecturas distribuidas.

---

# Definición de Éxito

Los Domain Events del Aggregate **Territory** representan de
forma inmutable, trazable y consistente todos los hechos
significativos producidos por el territorio.

Permiten desacoplar Aggregates y Bounded Contexts, mantener la
trazabilidad del dominio y habilitar mecanismos de integración
sin introducir referencias directas entre los componentes de
AURA.