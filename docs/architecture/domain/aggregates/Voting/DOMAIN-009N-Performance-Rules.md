# DOMAIN-009N — Voting Performance Rules

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Voting Management

Aggregate:
Voting

Documentos relacionados:

- DOMAIN-009-Aggregate.md
- DOMAIN-009G-Repository-Contract.md
- DOMAIN-009J-Consistency-Boundary.md
- DOMAIN-009K-Integration-Events.md
- DOMAIN-009L-Read-Model.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Este documento establece las reglas oficiales de rendimiento
(Performance Rules) para el Aggregate **Voting**.

Su propósito es garantizar que el Aggregate mantenga un
comportamiento predecible, acotado y consistente
independientemente del crecimiento de la plataforma AURA.

Las reglas de rendimiento no pueden alterar:

- identidad;
- Lifecycle;
- State Machine;
- Invariants;
- Permissions;
- Versioning;
- Consistency Boundary;
- Domain Events;
- contratos establecidos del Aggregate.

El rendimiento debe obtenerse preservando el modelo de dominio y
no debilitando sus reglas.

---

# Principios

El Aggregate Voting debe cumplir los siguientes principios:

- alta cohesión;
- tamaño reducido;
- operaciones acotadas;
- consistencia inmediata dentro del Aggregate;
- independencia tecnológica;
- referencias externas mediante identificadores;
- separación entre escritura y consulta;
- ausencia de procesamiento perteneciente a otros Aggregates.

Debe mantenerse:

```text
Performance

≠

Bypass Domain Rules
```

Ninguna optimización puede evitar las Invariants ni la Aggregate
Root.

---

# Responsabilidad del Aggregate

Voting debe ejecutar exclusivamente el comportamiento necesario
para proteger su propio estado y sus reglas de dominio.

Entre sus responsabilidades se encuentran:

- validar Commands;
- validar VotingStatus;
- validar transiciones;
- proteger Invariants;
- mantener Rules;
- mantener Options;
- mantener Result cuando corresponda;
- mantener Lifecycle;
- mantener Version;
- producir Domain Events correspondientes.

Voting no debe asumir responsabilidades de:

- búsquedas complejas;
- listados;
- agregaciones entre múltiples Voting;
- estadísticas;
- análisis histórico global;
- procesamiento de información perteneciente a otros
  Aggregates;
- consultas destinadas exclusivamente a presentación.

Estas necesidades deben permanecer fuera del comportamiento
transaccional del Aggregate.

---

# Tamaño del Aggregate

Voting debe mantenerse pequeño y enfocado en su propio
Consistency Boundary.

Debe contener únicamente el estado necesario para proteger:

```text
Voting Identity

Organization Context

Voting Context

VotingType

VotingStatus

Rules

Options

Result when applicable

Lifecycle Timestamps

Version
```

junto con los Value Objects y entidades internas que realmente
pertenezcan al Aggregate.

No debe incorporar Aggregates completos como:

```text
Organization

Citizen

Membership

Role

Territory

Assembly

Proposal

Participation

Document

Notification

Audit

Integration
```

Las relaciones externas deben mantenerse mediante los
identificadores establecidos por el modelo.

---

# Tiempo de Ejecución

La ejecución de un Command debe depender únicamente del estado
necesario para evaluar la operación correspondiente sobre Voting.

Debe evitarse que una operación ordinaria requiera recorrer,
cargar o procesar información perteneciente a un número
indeterminado de Aggregates externos.

Conceptualmente:

```text
Command

↓

Voting

↓

Validate Current State

Validate Invariants

Apply Domain Behavior

↓

Result
```

El crecimiento global del número de Citizens, Assemblies,
Proposals o Participations no debe ampliar automáticamente el
trabajo interno requerido por una operación ordinaria de Voting.

---

# Persistencia

Voting debe persistirse mediante:

```text
VotingRepository
```

como una unidad de consistencia.

Debe mantenerse:

```text
Load Voting

↓

Execute Domain Behavior

↓

Persist Voting
```

La persistencia no debe dividir una modificación válida en
escrituras independientes capaces de dejar el Aggregate en un
estado inconsistente.

No debe utilizarse persistencia parcial para modificar
directamente:

```text
VotingStatus

Rules

Options

Result

Version
```

evitando la Aggregate Root.

Las reglas completas pertenecen a:

```text
DOMAIN-009G-Repository-Contract.md
```

---

# Transacciones

La unidad lógica de modificación corresponde exclusivamente al
Aggregate:

```text
Voting
```

Una operación válida debe concluir con:

```text
Valid Voting
```

y una operación rechazada debe conservar:

```text
Previous Voting State

Previous Version
```

La modificación de Voting no debe mantener dentro de su misma
unidad de consistencia modificaciones sobre:

```text
Assembly

Proposal

Participation

Organization
```

ni sobre otros Aggregates.

Debe mantenerse:

```text
One Aggregate

=

One Consistency Boundary
```

---

# Consultas

Voting no debe expandirse para responder necesidades complejas de
consulta.

Consultas como:

```text
Voting by Organization

Voting by Assembly

Voting by Proposal

Voting by Status

Voting history

Voting results

Voting summaries
```

deben poder resolverse mediante los Read Models definidos para
Voting.

No debe reconstruirse ni ampliar innecesariamente el Aggregate
para satisfacer necesidades que pertenecen exclusivamente al
Read Side.

Debe mantenerse:

```text
Complex Query

↓

Read Model
```

y no:

```text
Complex Query

↓

Expand Voting Aggregate
```

---

# Eventos

Los Domain Events deben producirse como consecuencia de
modificaciones válidas del Aggregate.

Conceptualmente:

```text
Command

↓

Voting

↓

Valid Modification

↓

Domain Event
```

La producción del Domain Event pertenece al comportamiento de
Voting.

Los procesos posteriores asociados a:

- integración;
- proyecciones;
- Notification;
- Audit;
- otros Bounded Contexts;

no deben ampliar la operación interna del Aggregate.

Voting no debe esperar que otros Aggregates cambien de estado para
considerar válido un hecho ya confirmado dentro de su propio
Consistency Boundary.

---

# Consistencia

La consistencia inmediata se limita a:

```text
Voting
```

Dentro de ese límite deben permanecer coherentes:

- identidad;
- OrganizationId;
- VotingStatus;
- VotingType;
- Rules;
- Options;
- Result cuando corresponda;
- timestamps;
- Version;
- Invariants.

La relación con otros Aggregates no debe aumentar el tamaño del
límite de consistencia.

Debe mantenerse:

```text
Voting Internal Consistency

=

Immediate
```

mientras la coordinación con otros Aggregates permanece separada
conforme a los contratos establecidos por AURA.

Las reglas completas pertenecen a:

```text
DOMAIN-009J-Consistency-Boundary.md
```

---

# Concurrencia

Voting utiliza el modelo de Versioning establecido para el
Aggregate.

Debe mantenerse:

```text
ExpectedVersion

=

PersistedVersion
```

para confirmar una modificación sobre un Voting existente.

Cuando:

```text
ExpectedVersion

!=

PersistedVersion
```

la modificación debe ser rechazada mediante el conflicto de
concurrencia correspondiente.

Una estrategia de rendimiento no puede sustituir este control por
sobrescrituras silenciosas.

Debe mantenerse:

```text
Performance Optimization

≠

Concurrency Bypass
```

---

# Read Models

Las consultas de alta frecuencia o que requieran información
derivada deben utilizar los Read Models definidos para Voting.

La versión 1.0 reconoce:

```text
VotingSummary

VotingDetailView

VotingHistoryView

VotingResultView
```

Los Read Models:

- pueden optimizarse para consulta;
- pueden reconstruirse;
- no constituyen fuente de verdad;
- no ejecutan Commands;
- no modifican Voting;
- no incrementan Voting.Version;
- permanecen fuera del Consistency Boundary de escritura.

Debe mantenerse:

```text
Write Optimization

↓

Small Aggregate
```

y:

```text
Read Optimization

↓

Read Models
```

---

# Índices

Los mecanismos utilizados para optimizar búsquedas sobre
representaciones de lectura permanecen fuera del modelo interno de
Voting.

Voting no define estructuras de búsqueda o almacenamiento como
parte de sus Invariants.

Debe mantenerse:

```text
Query Optimization Structure

≠

Voting Domain State
```

Una optimización de consulta no puede modificar:

```text
VotingId

VotingStatus

Rules

Options

Result

Version
```

ni convertirse en fuente de verdad del Aggregate.

---

# Caché

La validez de Voting no puede depender de una representación de
lectura temporal o derivada.

Debe mantenerse:

```text
Voting Domain Consistency

≠

Cached Representation
```

Cualquier representación utilizada para acelerar una consulta
continúa siendo derivada y no puede sustituir:

```text
Voting Aggregate
```

como autoridad de escritura.

Tampoco puede utilizarse una representación desactualizada para
evitar:

- Versioning;
- Invariants;
- State Machine;
- Repository Contract.

---

# Escalabilidad

El crecimiento de AURA no debe provocar una expansión proporcional
del Consistency Boundary de cada Voting.

Debe mantenerse:

```text
More Organizations

More Assemblies

More Proposals

More Participations

More Voting Instances
```

sin convertir una instancia individual de Voting en un Aggregate
que deba contener o procesar todos esos elementos.

La escalabilidad del dominio se obtiene manteniendo:

```text
Independent Voting Aggregates

+

Explicit Identifiers

+

Read Models

+

Domain Events

+

Integration Events
```

conforme a los contratos ya establecidos.

---

# Consumo de Memoria

Durante la ejecución de una operación, Voting debe mantener
únicamente el estado perteneciente a su propio Consistency
Boundary.

No debe cargar Aggregates externos completos para ejecutar
operaciones ordinarias.

Debe mantenerse:

```text
Voting

+

External Aggregate Identifiers
```

y no:

```text
Voting

+

Organization Aggregate

+

Assembly Aggregate

+

Proposal Aggregate

+

Participation Aggregates
```

La existencia de relaciones no implica carga conjunta del estado
completo de los Aggregates relacionados.

---

# Integración

Voting comunica hechos relevantes hacia otros contextos mediante
los contratos definidos en:

```text
DOMAIN-009K-Integration-Events.md
```

La integración no debe ampliar el comportamiento interno del
Aggregate con responsabilidades pertenecientes al consumidor.

Debe mantenerse:

```text
Voting

↓

Domain Event

↓

Integration Event when applicable
```

Voting no debe modificar directamente:

```text
Assembly

Proposal

Participation

Notification

Audit

Integration
```

como parte de una operación interna.

La indisponibilidad o demora de un proceso externo no modifica por
sí sola un hecho de Voting que ya fue válidamente confirmado.

---

# Métricas Recomendadas

El cumplimiento de las Performance Rules puede observarse mediante
dimensiones asociadas a:

- duración de ejecución de Commands;
- duración de recuperación y persistencia del Aggregate;
- frecuencia de conflictos de Version;
- tamaño del estado necesario para operar sobre un Voting;
- tiempo de actualización de Read Models;
- tiempo de reconstrucción de Read Models;
- volumen de Domain Events asociados a Voting;
- volumen de Integration Events derivados.

Estas observaciones no modifican el dominio.

No establecen nuevos estados, Commands, Events ni Invariants.

Cualquier objetivo cuantitativo concreto pertenece a la definición
operacional correspondiente y no se incorpora mediante este
documento.

---

# Antipatrones

Las siguientes prácticas están prohibidas dentro del Aggregate
Voting:

- cargar Aggregates externos completos para operaciones
  ordinarias;
- utilizar Voting para realizar búsquedas globales;
- realizar estadísticas dentro de la Aggregate Root;
- utilizar el Repository como motor de consultas especializadas;
- modificar Read Models desde Voting como parte de su estado;
- ampliar Voting para resolver necesidades exclusivas de lectura;
- modificar directamente estado persistido evitando la Aggregate
  Root;
- dividir una modificación válida en actualizaciones parciales que
  puedan romper Invariants;
- utilizar optimizaciones para evitar Versioning;
- utilizar optimizaciones para evitar State Machine;
- utilizar optimizaciones para evitar Permissions;
- modificar otros Aggregates dentro del Consistency Boundary de
  Voting;
- considerar una referencia externa como ownership;
- introducir dependencias tecnológicas dentro de las reglas de
  dominio para resolver rendimiento.

---

# Compatibilidad con CQRS

Voting mantiene la separación entre Write Side y Read Side.

Write Side:

```text
Command
   │
   ▼
Voting Aggregate
   │
   ├── Invariants
   ├── State Machine
   ├── Version
   └── Domain Events
```

Read Side:

```text
Domain Events
      │
      ▼
Projection
      │
      ▼
Read Model
```

El Write Side debe mantenerse enfocado en comportamiento y
consistencia.

El Read Side absorbe las necesidades de:

- búsqueda;
- listado;
- representación resumida;
- representación detallada;
- representación histórica;
- representación de Result.

El rendimiento de las consultas no debe obtenerse ampliando el
Aggregate.

---

# Compatibilidad con Event Sourcing

La compatibilidad de Voting con Event Sourcing no modifica las
reglas de rendimiento del Aggregate.

Cuando Voting sea reconstruido a partir de hechos históricos debe
utilizar exclusivamente la información correspondiente al mismo:

```text
VotingId
```

La reconstrucción de Voting no debe requerir reconstruir
simultáneamente:

```text
Organization

Assembly

Proposal

Participation
```

como parte del mismo Aggregate.

Debe mantenerse:

```text
Voting Event History

↓

Voting
```

Replay no constituye una nueva modificación del dominio y no
incrementa Version por sí mismo.

---

# Principios Arquitectónicos

Las Performance Rules de Voting mantienen los principios
consolidados de AURA:

- Domain-Driven Design;
- Aggregate Pattern;
- alta cohesión;
- bajo acoplamiento;
- Consistency Boundary explícito;
- referencias externas mediante identificadores;
- Repository Contract;
- Optimistic Concurrency Control;
- Domain Events;
- Integration Events;
- Read Models;
- CQRS;
- compatibilidad con Event Sourcing;
- independencia tecnológica.

Debe mantenerse:

```text
Small Aggregate

+

Explicit Consistency Boundary

+

Bounded Domain Operations

+

Specialized Read Models
```

sin debilitar ninguna regla del dominio.

---

# Definición de Éxito

El Aggregate **Voting** mantiene un comportamiento predecible y
acotado al limitar su responsabilidad a la protección y evolución
de su propio estado de dominio.

Las Performance Rules garantizan que:

- Voting permanece pequeño;
- Voting conserva una única Aggregate Root;
- las operaciones se limitan al Consistency Boundary;
- las relaciones externas utilizan identificadores;
- otros Aggregates no se cargan como parte interna de Voting;
- las consultas complejas se resuelven mediante Read Models;
- el Repository permanece orientado a persistir y recuperar el
  Aggregate;
- las modificaciones válidas permanecen completas y consistentes;
- Versioning continúa protegiendo la concurrencia;
- los Domain Events permanecen separados del procesamiento
  posterior;
- los Integration Events no amplían el Consistency Boundary;
- las optimizaciones de lectura no se convierten en fuente de
  verdad;
- CQRS mantiene separadas lectura y escritura;
- la compatibilidad con Event Sourcing no requiere reconstruir
  Aggregates externos;
- ninguna optimización puede evitar Lifecycle, State Machine,
  Invariants, Permissions o Versioning;
- el crecimiento global de AURA no expande automáticamente el
  estado interno de cada Voting.

De esta forma, `DOMAIN-009N-Performance-Rules.md` establece las
reglas oficiales de rendimiento del Aggregate **Voting**,
preservando su cohesión, su Consistency Boundary y el patrón
consolidado de AURA Core.