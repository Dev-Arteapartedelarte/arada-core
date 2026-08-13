# DOMAIN-008J — Participation Consistency Boundary

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
- DOMAIN-008E-Invariants.md
- DOMAIN-008G-Repository-Contract.md
- DOMAIN-008I-Versioning.md
- CORE-011-Repository-Contracts.md
- CORE-016-Dependency-Rules.md

---

# Objetivo

Definir el límite oficial de consistencia del Aggregate
Participation.

El Consistency Boundary determina:

- qué estado pertenece al Aggregate;
- qué reglas deben mantenerse de forma atómica;
- qué elementos pueden modificarse dentro de una misma
  transacción;
- qué referencias pertenecen a otros Aggregates;
- qué operaciones requieren consistencia inmediata;
- qué interacciones utilizan consistencia eventual.

---

# Principio Fundamental

Participation constituye una única unidad de consistencia.

```text
Participation Aggregate

=

Consistency Boundary
```

Toda modificación del Aggregate debe preservar sus
Invariants antes de finalizar la operación.

No puede existir un estado parcialmente válido.

---

# Aggregate Root

El límite de consistencia está controlado exclusivamente
por:

```text
Participation
```

como Aggregate Root.

Toda modificación del estado interno debe realizarse a
través del Aggregate Root.

Los consumidores externos no pueden modificar
directamente elementos internos del Aggregate.

---

# Estado Dentro del Boundary

El estado perteneciente a Participation debe mantenerse
consistente como una única unidad.

Representación conceptual.

```text
Participation

Id

Version

State

Type

Context

Metadata

Lifecycle Information
```

Estos elementos forman parte del estado observable del
Aggregate y deben respetar conjuntamente sus Invariants.

---

# Consistencia Inmediata

Las reglas internas de Participation requieren
consistencia inmediata.

Ejemplo.

```text
Command

↓

Participation

↓

Validate Invariants

↓

Modify State

↓

Increment Version

↓

Persist
```

Al finalizar la operación, el Aggregate debe encontrarse
en un estado válido.

---

# Atomicidad

Una modificación válida de Participation debe persistirse
atómicamente.

```text
Current Participation

↓

Domain Operation

↓

New Participation State

↓

New Version

↓

Domain Events

↓

Commit
```

No puede persistirse únicamente una parte de la
modificación.

---

# Fallo de Operación

Si una operación viola una Invariant, ninguna modificación
debe confirmarse.

```text
Command

↓

Invariant Violation

↓

Reject

↓

No State Change
```

El Aggregate conserva su estado anterior.

---

# Versionado

La versión forma parte del límite de consistencia.

Toda modificación válida debe mantener la relación:

```text
Current Version

↓

Valid Modification

↓

Version + 1
```

El estado y la nueva versión deben confirmarse como una
misma modificación lógica.

---

# Concurrencia

La concurrencia se controla dentro del límite del
Aggregate.

Dos operaciones concurrentes sobre la misma Participation
no pueden sobrescribirse silenciosamente.

```text
Participation

Version 8

↓

Process A

Process B
```

Si Process A confirma primero:

```text
Version 9
```

Process B debe detectar:

```text
ConcurrencyConflictError
```

si intenta persistir utilizando Version 8.

---

# Repository

El Repository opera sobre Participation como una unidad
completa de persistencia.

```text
ParticipationRepository

↓

Participation Aggregate
```

No debe exponer mecanismos que permitan modificar
directamente partes internas evitando las reglas del
Aggregate Root.

---

# Persistencia

La persistencia debe respetar el límite del Aggregate.

Conceptualmente.

```text
load()

↓

Participation

↓

Domain Operation

↓

save()

↓

Participation
```

El Repository recupera y persiste el Aggregate respetando
su estado y versión.

---

# Referencias a Otros Aggregates

Participation puede mantener referencias hacia otros
Aggregates mediante sus identificadores.

Ejemplo.

```text
Participation

↓

OrganizationId

CitizenId

AssemblyId

ProposalId
```

Estas referencias no incorporan los otros Aggregates
dentro del Consistency Boundary de Participation.

---

# Independencia de Aggregates

Los Aggregates relacionados mantienen sus propios límites
de consistencia.

```text
Organization

↓

Own Consistency Boundary
```

```text
Citizen

↓

Own Consistency Boundary
```

```text
Assembly

↓

Own Consistency Boundary
```

```text
Proposal

↓

Own Consistency Boundary
```

```text
Participation

↓

Own Consistency Boundary
```

Una modificación de Participation no debe modificar
directamente el estado interno de otro Aggregate.

---

# Consistencia entre Aggregates

Las operaciones que afectan múltiples Aggregates no forman
una única transacción de dominio.

Ejemplo.

```text
Participation

↓

Domain Event

↓

Other Bounded Context
```

La coordinación entre límites independientes utiliza
eventos y consistencia eventual.

---

# Domain Events

Los Domain Events representan cambios confirmados dentro
del Consistency Boundary.

```text
Participation

↓

Valid State Change

↓

Domain Event
```

El evento solo representa un hecho válido producido por
el Aggregate.

---

# Integration Events

Los Integration Events permiten comunicar cambios de
Participation fuera de su Bounded Context.

```text
Participation

↓

Domain Event

↓

Integration Event

↓

External Consumer
```

Los consumidores externos no forman parte del límite de
consistencia del Aggregate.

---

# Consistencia Eventual

Las proyecciones y consumidores externos pueden
actualizarse mediante consistencia eventual.

Ejemplo.

```text
Participation

↓

Commit

↓

Domain Event

↓

Projection

↓

Read Model
```

El Read Model puede actualizarse después de que el cambio
del Aggregate haya sido confirmado.

---

# Read Models

Los Read Models no forman parte del Consistency Boundary.

```text
Participation Aggregate

↓

Domain Events

↓

Read Models
```

Las proyecciones son derivadas y no pueden utilizarse como
fuente de verdad para modificar el Aggregate.

---

# Transacciones

Una transacción de escritura sobre Participation debe
abarcar únicamente su propio límite de consistencia.

```text
Transaction

↓

Participation

↓

Commit
```

No debe extenderse automáticamente hacia otros
Aggregates.

---

# Validación de Referencias

La existencia de referencias externas puede validarse
antes de ejecutar una operación.

Sin embargo, los Aggregates referenciados continúan fuera
del límite de consistencia de Participation.

```text
External Aggregate

↓

Reference Validation

↓

Participation Command

↓

Participation Aggregate
```

La validación de una referencia no convierte al Aggregate
externo en parte de Participation.

---

# Invariants

Las Invariants de Participation deben cumplirse dentro de
su propio Consistency Boundary.

```text
Command

↓

Aggregate Root

↓

Invariant Validation

↓

State Change
```

Ninguna operación puede confirmar un estado que viole las
Invariants oficiales del Aggregate.

---

# Operaciones Internas

Las operaciones internas que modifican Participation deben
mantener:

- identidad válida;
- estado válido;
- tipo válido;
- contexto válido;
- metadata válida;
- reglas del Lifecycle;
- versión consistente.

Estas reglas se verifican antes de confirmar la
modificación.

---

# Operaciones Externas

Los sistemas externos no pueden:

- modificar directamente el estado interno;
- alterar directamente la versión;
- persistir parcialmente el Aggregate;
- evitar las Invariants;
- modificar entidades internas de forma independiente;
- incorporar otros Aggregates dentro del mismo límite de
  consistencia.

Toda intención de modificación debe ingresar mediante los
contratos definidos por AURA Core.

---

# Relación con Outbox

Cuando una modificación genera eventos destinados a
integraciones, el estado del Aggregate y el registro
correspondiente para publicación deben conservar la
coherencia de la operación.

Representación conceptual.

```text
Participation

↓

State Change

↓

Version

↓

Domain Event

↓

Outbox Record
```

La publicación externa ocurre posteriormente.

---

# Fallo de Publicación

Un fallo al publicar un Integration Event no invalida una
modificación del Aggregate que ya fue confirmada.

```text
Participation

↓

Commit

↓

Outbox

↓

Publication Failure
```

El Aggregate permanece confirmado.

La publicación puede continuar posteriormente desde el
mecanismo de integración establecido.

---

# Límites Transaccionales

El límite transaccional coincide con el Aggregate.

```text
Transaction Boundary

=

Participation Consistency Boundary
```

Esto evita transacciones distribuidas entre Aggregates.

---

# Restricciones

El Consistency Boundary:

- contiene únicamente el estado perteneciente a
  Participation;
- es controlado por el Aggregate Root;
- debe preservar todas las Invariants;
- debe persistirse atómicamente;
- mantiene una única versión del Aggregate;
- no incluye Read Models;
- no incluye otros Aggregates;
- no incluye consumidores externos;
- no incluye Integration Events ya publicados;
- no permite modificaciones parciales;
- no permite escrituras directas sobre elementos internos;
- no permite transacciones distribuidas entre Aggregates.

---

# Reglas

## REG-001

Participation constituye una única unidad de
consistencia.

---

## REG-002

Toda modificación interna debe realizarse a través del
Aggregate Root.

---

## REG-003

Todas las Invariants deben cumplirse antes de confirmar
una modificación.

---

## REG-004

El estado y la versión del Aggregate deben persistirse de
forma atómica.

---

## REG-005

Los otros Aggregates nunca forman parte del Consistency
Boundary de Participation.

---

## REG-006

Las referencias hacia otros Aggregates deben realizarse
mediante identificadores.

---

## REG-007

Una modificación de Participation no puede modificar
directamente otro Aggregate.

---

## REG-008

La coordinación entre Aggregates utiliza consistencia
eventual.

---

## REG-009

Los Read Models permanecen fuera del límite de
consistencia.

---

## REG-010

El Repository debe respetar el Aggregate como unidad de
persistencia.

---

# Definición de Éxito

El Aggregate `Participation` mantiene un límite de
consistencia explícito, independiente y protegido que
garantiza que todas sus Invariants, estado y versión se
modifiquen de forma atómica a través del Aggregate Root,
manteniendo separados los demás Aggregates, Read Models e
integraciones y permitiendo que AURA Core coordine cambios
entre Bounded Contexts mediante Domain Events,
Integration Events y consistencia eventual sin romper los
límites definidos por el modelo de dominio.