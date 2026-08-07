# DOMAIN-005E — Territory Invariants

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
- DOMAIN-005B-State-Machine.md
- DOMAIN-005C-Commands.md
- DOMAIN-005D-Domain-Events.md
- DOMAIN-005F-Permissions.md
- DOMAIN-005G-Repository-Contract.md
- DOMAIN-005J-Consistency-Boundary.md

---

# Objetivo

Definir las invariantes que deben cumplirse durante toda la
vida del Aggregate **Territory**.

Las invariantes representan reglas que nunca pueden ser
violadas por una operación válida del dominio.

Toda modificación del Aggregate debe preservar estas reglas
antes de confirmar el nuevo estado.

---

# Principios

Las invariantes de Territory deben garantizar:

- identidad consistente;
- integridad territorial;
- coherencia jerárquica;
- validez del ciclo de vida;
- unicidad de identificadores administrativos;
- integridad de las relaciones;
- consistencia transaccional.

---

# Invariant 01 — Identidad

Todo Territory debe poseer exactamente un:

```text
TerritoryId
```

El identificador:

- es obligatorio;
- es único;
- es inmutable;
- no puede reutilizarse para otro Territory.

Una operación nunca puede modificar el TerritoryId.

---

# Invariant 02 — Nombre

Todo Territory debe poseer un nombre válido.

El nombre:

- es obligatorio;
- no puede estar vacío;
- no puede contener únicamente espacios;
- debe cumplir las reglas de longitud establecidas por el
  dominio.

No puede existir un Territory sin nombre válido.

---

# Invariant 03 — Tipo Territorial

Todo Territory debe poseer un:

```text
TerritoryType
```

El tipo debe pertenecer al conjunto de tipos territoriales
válidos definido por AURA.

No se permite un Territory sin clasificación territorial.

---

# Invariant 04 — Estado

Todo Territory debe poseer exactamente un estado válido.

Los únicos estados permitidos son:

```text
Draft

PendingValidation

Active

Inactive

Archived
```

Nunca puede existir un Territory con un estado desconocido o
nulo.

---

# Invariant 05 — Código Administrativo

Cuando un Territory posee:

```text
AdministrativeCode
```

el código debe ser único dentro del ámbito administrativo
correspondiente.

No pueden coexistir dos territorios activos con el mismo
código dentro del mismo ámbito.

---

# Invariant 06 — Jerarquía Territorial

Cuando un Territory posee:

```text
ParentTerritoryId
```

el territorio padre debe existir.

No se permite una referencia hacia un Territory inexistente.

---

# Invariant 07 — Autorreferencia

Un Territory nunca puede ser su propio padre.

Por lo tanto:

```text
TerritoryId != ParentTerritoryId
```

Una operación que intente establecer esta relación debe ser
rechazada.

---

# Invariant 08 — Ausencia de Ciclos

La jerarquía territorial debe formar una estructura acíclica.

No se permite:

```text
Territory A
    ↓
Territory B
    ↓
Territory C
    ↓
Territory A
```

Toda modificación de `ParentTerritoryId` debe verificar que no
introduzca un ciclo.

---

# Invariant 09 — Integridad Geográfica

Cuando existe:

```text
GeometryReference
```

debe apuntar a una representación geográfica válida según las
reglas del dominio.

La referencia geográfica no puede invalidar la identidad ni la
clasificación del Territory.

---

# Invariant 10 — Estado Draft

Un Territory en:

```text
Draft
```

puede ser modificado para completar su información.

No puede utilizarse como territorio operativo para procesos
que requieran un Territory activo.

---

# Invariant 11 — Estado PendingValidation

Un Territory en:

```text
PendingValidation
```

se encuentra sujeto al proceso de validación.

No puede activarse mediante una operación que omita la
validación correspondiente.

---

# Invariant 12 — Estado Active

Un Territory en:

```text
Active
```

es operacionalmente válido.

Puede ser referenciado por otros componentes del dominio que
requieran un territorio activo.

---

# Invariant 13 — Estado Inactive

Un Territory en:

```text
Inactive
```

mantiene su identidad y trazabilidad.

No debe utilizarse para nuevas asociaciones operativas que
requieran un Territory activo.

Puede retornar a:

```text
Active
```

mediante la transición correspondiente.

---

# Invariant 14 — Estado Archived

Un Territory en:

```text
Archived
```

es inmutable.

No puede:

- cambiar de nombre;
- cambiar de tipo;
- cambiar de geometría;
- cambiar de padre;
- cambiar de código;
- volver a Active;
- volver a Inactive;
- volver a Draft.

El estado Archived es terminal.

---

# Invariant 15 — Transiciones de Estado

Las únicas transiciones válidas son:

```text
Draft
    ↓
PendingValidation
    ↓
Active
    ↓
Inactive
    ↓
Active
```

y:

```text
Active
    ↓
Archived
```

o:

```text
Inactive
    ↓
Archived
```

Cualquier transición fuera de este conjunto debe ser
rechazada.

---

# Invariant 16 — Integridad del Aggregate

Toda modificación de Territory debe ejecutarse a través de la
Aggregate Root.

No se permite modificar directamente:

```text
TerritoryName

TerritoryType

TerritoryStatus

AdministrativeCode

ParentTerritoryId

GeometryReference

Metadata
```

desde fuera del Aggregate.

---

# Invariant 17 — Referencias Externas

Territory puede relacionarse con otros Aggregates únicamente
mediante identificadores.

Ejemplos:

```text
OrganizationId

AssemblyId

DocumentId

AuditId
```

No se permiten referencias directas a objetos pertenecientes
a otros Aggregates.

---

# Invariant 18 — Integridad de Organization

Cuando el dominio requiera una organización asociada al
contexto territorial, el:

```text
OrganizationId
```

debe corresponder a una Organization válida.

Territory no puede modificar directamente la Organization.

---

# Invariant 19 — Atomicidad

Toda operación sobre Territory debe ser atómica.

Si alguna invariante falla:

```text
OperationRejected
```

El Aggregate conserva exactamente el estado anterior.

No se permite persistir un estado parcialmente modificado.

---

# Invariant 20 — Domain Events

Un Domain Event sólo puede emitirse después de que:

1. las invariantes hayan sido satisfechas;
2. la operación haya sido aceptada;
3. el nuevo estado sea consistente.

Una operación rechazada no genera Domain Events de éxito.

---

# Invariant 21 — Versionado

Cada modificación válida del Aggregate debe incrementar su
versión.

Ejemplo:

```text
Version 1
TerritoryCreated

Version 2
TerritoryRenamed

Version 3
TerritoryActivated
```

No pueden existir dos versiones diferentes para el mismo
estado lógico del Aggregate.

---

# Invariant 22 — Concurrencia

Una modificación no puede sobrescribir silenciosamente un
cambio realizado por otra operación concurrente.

El mecanismo de persistencia debe detectar conflictos de
versión.

Ejemplo:

```text
ExpectedVersion = 5

CurrentVersion = 6

        ↓

ConcurrencyConflict
```

---

# Invariant 23 — Inmutabilidad Histórica

Los eventos ya publicados y los estados históricos del
Aggregate no pueden modificarse retroactivamente.

Las correcciones deben realizarse mediante nuevas operaciones
válidas del dominio.

---

# Invariant 24 — Consistencia Transaccional

El nuevo estado de Territory y su correspondiente conjunto de
Domain Events deben pertenecer a la misma operación lógica de
dominio.

No debe confirmarse un cambio de estado sin registrar los
eventos correspondientes.

---

# Invariant 25 — Integridad del Parent Territory

Un cambio de:

```text
ParentTerritoryId
```

debe garantizar simultáneamente:

- existencia del nuevo padre;
- ausencia de autorreferencia;
- ausencia de ciclos;
- compatibilidad jerárquica entre tipos territoriales;
- preservación de la integridad territorial.

---

# Invariant 26 — Compatibilidad de Tipos

La relación entre un Territory y su Parent Territory debe
respetar las reglas jerárquicas definidas por el dominio.

Por ejemplo, una clasificación territorial que sólo pueda
existir como unidad hija no puede convertirse en padre de un
territorio incompatible con su jerarquía.

Las reglas concretas de compatibilidad pertenecen al modelo
territorial y no deben resolverse mediante referencias
directas a otros Aggregates.

---

# Invariant 27 — Modificación Controlada

Toda modificación debe ejecutarse mediante un Command válido.

El flujo obligatorio es:

```text
Command
    ↓
Authorization
    ↓
Validation
    ↓
Invariant Check
    ↓
State Change
    ↓
Domain Event
    ↓
Persistence
```

Una operación que falle en cualquier etapa anterior al cambio
de estado no puede modificar el Aggregate.

---

# Invariant 28 — Auditoría

Toda operación que modifique Territory debe permitir
identificar:

```text
ActorId

TerritoryId

PreviousState

CurrentState

OccurredOn

CorrelationId

CausationId
```

La trazabilidad no puede depender exclusivamente del estado
actual del Aggregate.

---

# Violación de Invariantes

Cuando una operación viola una invariante, el dominio debe
rechazarla.

Ejemplo:

```text
Command
   │
   ▼
Invariant Check
   │
   ├── Valid
   │     │
   │     ▼
   │   State Change
   │
   └── Invalid
         │
         ▼
   OperationRejected
```

No se genera un Domain Event de éxito.

---

# Regla Fundamental

La prioridad del Aggregate es:

```text
Invariant Preservation
        >
State Transition
        >
Event Publication
        >
External Integration
```

Ninguna integración externa puede justificar la violación de
una invariante interna de Territory.

---

# Definición de Éxito

Las invariantes del Aggregate **Territory** garantizan que
cada territorio mantenga una identidad única, una clasificación
válida, una jerarquía territorial consistente, un ciclo de vida
controlado y un estado transaccional íntegro durante toda su
existencia.

Toda operación que no pueda preservar estas condiciones debe
ser rechazada antes de modificar el Aggregate.