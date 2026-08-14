# DOMAIN-010J — Document Consistency Boundary

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
- DOMAIN-010E-Invariants.md
- DOMAIN-010G-Repository-Contract.md
- DOMAIN-010I-Versioning.md
- CORE-003-Shared-Kernel.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Este documento define el **Consistency Boundary** del
Aggregate **Document**.

El Aggregate constituye la unidad mínima de consistencia del
dominio. Todas las reglas de negocio que requieren consistencia
inmediata deben ejecutarse dentro de este límite.

Las relaciones con otros Aggregates o Bounded Contexts se
resuelven mediante referencias por identidad y coordinación
mediante eventos y contratos explícitos.

---

# Definición

El límite de consistencia del Aggregate **Document** comprende
exclusivamente los elementos necesarios para mantener una unidad
documental coherente y válida.

Dentro del Aggregate:

- las Invariants se cumplen de forma inmediata;
- los cambios son atómicos;
- existe una única transacción conceptual;
- la consistencia es fuerte.

Fuera del Aggregate:

- la consistencia es eventual;
- la coordinación se realiza mediante Domain Events e
  Integration Events.

---

# Alcance del Aggregate

El Aggregate Document incluye conceptualmente:

```text
Document (Aggregate Root)

│

├── DocumentId

├── DocumentType

├── Content

├── DocumentStatus

├── Internal Entities

├── Value Objects

└── Version
```

Todos estos elementos evolucionan dentro del mismo
Consistency Boundary.

Ningún elemento interno puede ser modificado directamente desde
fuera de la Aggregate Root.

---

# Fuera del Boundary

Los siguientes conceptos pertenecen a otros Aggregates o
Bounded Contexts y **no** forman parte del Aggregate Document:

```text
Organization

Citizen

Membership

Role

Territory

Assembly

Proposal

Participation

Voting

Notification

Audit

Integration
```

Document mantiene únicamente referencias por identidad y
contratos cuando sea necesario.

Ninguno de estos Aggregates se almacena dentro de Document.

---

# Referencias

Las relaciones externas utilizan identificadores.

Ejemplo:

```text
Assembly

↓

DocumentId
```

Nunca:

```text
Assembly

↓

Document Aggregate embedded inside Assembly
```

Del mismo modo, Document no incorpora instancias completas de
otros Aggregates.

Debe mantenerse:

```text
External Aggregate Reference

≠

Aggregate Composition
```

---

# Reglas de Consistencia

Dentro del Aggregate deben cumplirse de forma inmediata:

- identidad válida e inmutable;
- DocumentType válido;
- integridad de Content;
- DocumentStatus válido;
- State Machine válida;
- Lifecycle válido;
- Invariants del dominio;
- integridad de los Value Objects;
- incremento correcto de Version;
- generación coherente de Domain Events.

No puede existir un Document parcialmente válido.

Toda modificación debe dejar el Aggregate en un estado consistente.

---

# Transacción Conceptual

Toda modificación sigue conceptualmente el siguiente flujo:

```text
Command

↓

Load Document

↓

Validate Invariants

↓

Execute Behavior

↓

Update Version

↓

Generate Domain Events

↓

Persist Aggregate

↓

Commit
```

Si cualquiera de las condiciones requeridas falla, la operación
completa debe cancelarse.

Una operación rechazada:

- no modifica el estado confirmado;
- no incrementa Version;
- no produce el Domain Event de éxito.

---

# Coordinación entre Aggregates

Cuando una operación involucra otros Aggregates, Document no los
modifica directamente.

Conceptualmente:

```text
DocumentPublished

↓

Domain Event

↓

External Context
```

Cada Aggregate conserva:

- identidad propia;
- Lifecycle propio;
- State Machine propia;
- Invariants propias;
- Version propia;
- Consistency Boundary propio.

Un hecho ocurrido en Document puede ser observado posteriormente
por otros contextos sin ampliar la transacción de Document.

---

# Consistencia Eventual

Las operaciones distribuidas entre Document y otros Aggregates
siguen un modelo de consistencia eventual.

Conceptualmente:

```text
DocumentPublished

↓

Integration Event

↓

External Bounded Context
```

La modificación del Aggregate Document finaliza dentro de su
propio Consistency Boundary.

Los procesos externos pueden reaccionar posteriormente.

Debe mantenerse:

```text
Document Transaction

≠

Distributed Aggregate Transaction
```

---

# Invariantes dentro del Boundary

Antes de confirmar una modificación deben mantenerse como mínimo:

- DocumentId existe;
- DocumentId es inmutable;
- DocumentType es válido;
- Content pertenece a Document;
- Content solamente se modifica mediante comportamiento del
  Aggregate;
- DocumentStatus pertenece al conjunto oficial;
- toda transición pertenece a la State Machine;
- Archived permanece como estado terminal;
- Version se incrementa correctamente ante modificaciones válidas;
- los Domain Events representan hechos ocurridos;
- ningún Aggregate externo es modificado directamente.

Las reglas completas pertenecen a:

```text
DOMAIN-010E-Invariants.md
```

---

# Lo que el Aggregate nunca hace

El Aggregate Document nunca:

- modifica otros Aggregates;
- incorpora otros Aggregates dentro de su estado;
- inicia transacciones distribuidas;
- invoca servicios externos;
- envía Notifications directamente;
- ejecuta integraciones externas directamente;
- publica mensajes de Infrastructure directamente;
- accede directamente a bases de datos;
- depende de mecanismos concretos de almacenamiento de Content.

Estas responsabilidades pertenecen a otros contextos o a capas
externas.

---

# Relación con Event Sourcing

En una implementación basada en Event Sourcing, el Consistency
Boundary permanece inalterado.

La reconstrucción del Aggregate se realiza utilizando únicamente
los Domain Events correspondientes al mismo:

```text
DocumentId
```

Conceptualmente:

```text
DocumentCreated

↓

DocumentPublished

↓

DocumentArchived
```

No se requieren Domain Events pertenecientes a otros Aggregates
para reconstruir el estado de Document.

La implementación concreta de Event Sourcing pertenece a
Infrastructure.

---

# Relación con CQRS

Document pertenece al lado de escritura como autoridad sobre su
estado.

Conceptualmente:

```text
Command

↓

Document Aggregate

↓

Domain Events
```

Las consultas que combinan información de Document con otros
Aggregates se resuelven mediante Read Models y proyecciones.

Debe mantenerse:

```text
Cross-Aggregate Query

↓

Read Model
```

y no:

```text
Cross-Aggregate Query

↓

Expand Document Consistency Boundary
```

Los Read Models no pueden modificar Document.

---

# Escenario de Ejemplo

```text
PublishDocument

↓

Validate Document

↓

Draft → Published

↓

Version N + 1

↓

DocumentPublished

↓

Persist Document

↓

Commit

↓

External Contexts react
```

El Aggregate finaliza su modificación antes de que otros contextos
procesen el hecho.

Ningún Aggregate externo forma parte de la misma unidad de
consistencia.

---

# Beneficios

Mantener un Consistency Boundary reducido permite:

- proteger las Invariants de Document;
- mantener transacciones conceptuales pequeñas;
- reducir acoplamiento;
- preservar autonomía entre Aggregates;
- permitir evolución independiente;
- mantener consistencia interna fuerte;
- utilizar consistencia eventual entre Aggregates;
- facilitar compatibilidad con arquitecturas distribuidas;
- evitar transacciones distribuidas innecesarias.

---

# Principios Arquitectónicos

El Consistency Boundary del Aggregate Document sigue:

- Domain-Driven Design (DDD);
- Aggregate Pattern;
- Event-Driven Architecture;
- CQRS;
- Event Sourcing Compatible;
- Clean Architecture;
- Single Responsibility Principle;
- Dependency Inversion Principle.

El límite pertenece al dominio y no depende de una tecnología
concreta de persistencia, mensajería o almacenamiento.

---

# Definición de Éxito

El Aggregate **Document** constituye la unidad oficial de
consistencia para la gestión documental dentro de AURA.

Todas las reglas que requieren consistencia inmediata se ejecutan
dentro de este límite.

El Consistency Boundary contiene:

```text
Document

DocumentId

DocumentType

Content

DocumentStatus

Internal Entities

Value Objects

Version
```

y mantiene fuera:

```text
Organization

Citizen

Membership

Role

Territory

Assembly

Proposal

Participation

Voting

Notification

Audit

Integration
```

El modelo garantiza que:

- Document protege sus propias Invariants;
- toda modificación se ejecuta mediante la Aggregate Root;
- DocumentId permanece inmutable;
- Content permanece bajo responsabilidad de Document;
- DocumentStatus solamente cambia mediante la State Machine;
- toda modificación válida incrementa Version;
- los Domain Events representan hechos confirmados;
- ninguna operación modifica directamente otros Aggregates;
- las relaciones externas utilizan identificadores y contratos;
- la consistencia interna es inmediata;
- la consistencia entre Aggregates es eventual;
- Event Sourcing no modifica el límite;
- CQRS no amplía el límite;
- Read Models no poseen autoridad de escritura;
- Infrastructure no determina el Consistency Boundary.

De esta forma, `DOMAIN-010J-Consistency-Boundary.md` establece el
límite oficial de consistencia del Aggregate **Document** conforme
al patrón consolidado de AURA Core.