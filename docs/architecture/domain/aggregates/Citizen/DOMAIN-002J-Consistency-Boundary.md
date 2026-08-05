# DOMAIN-002J — Citizen Consistency Boundary

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
- DOMAIN-002E-Invariants.md
- DOMAIN-002G-Repository-Contract.md
- DOMAIN-002I-Versioning.md
- CORE-003-Shared-Kernel.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Este documento define el **Consistency Boundary** del
Aggregate **Citizen**.

El Aggregate constituye la unidad mínima de consistencia del
dominio. Todas las reglas de negocio que requieren consistencia
inmediata deben ejecutarse dentro de este límite.

Las relaciones con otros Aggregates o Bounded Contexts se
resuelven mediante referencias por identidad y coordinación
asíncrona a través de eventos.

---

# Definición

El límite de consistencia del Aggregate **Citizen** comprende
exclusivamente los elementos necesarios para mantener una
identidad cívica coherente y válida.

Dentro del Aggregate:

- las invariantes se cumplen de forma inmediata;
- los cambios son atómicos;
- existe una única transacción conceptual;
- la consistencia es fuerte.

Fuera del Aggregate:

- la consistencia es eventual;
- la coordinación se realiza mediante Domain Events e
  Integration Events.

---

# Alcance del Aggregate

El Aggregate Citizen incluye conceptualmente:

```text
Citizen (Aggregate Root)

│

├── Personal Identity

├── Contact Information

├── Address

├── Preferred Language

├── Privacy Preferences

├── Consent Records

└── Lifecycle State
```

Todos estos elementos evolucionan bajo una única versión del
Aggregate.

---

# Fuera del Boundary

Los siguientes conceptos pertenecen a otros Aggregates o
Bounded Contexts y **no** forman parte del Aggregate Citizen:

```text
Organization

Membership

Role

Permission

Assembly

Proposal

Vote

Notification

Audit Log

Territory

Document

Device

Credential

Integration Account
```

El Citizen mantiene únicamente referencias por identidad hacia
ellos cuando es necesario.

---

# Referencias

Las relaciones externas siempre utilizan identificadores
inmutables.

Ejemplo:

```text
Citizen

↓

OrganizationId
```

Nunca:

```text
Citizen

↓

Organization Aggregate
```

El Aggregate nunca mantiene referencias directas a otros
Aggregates.

---

# Reglas de Consistencia

Dentro del Aggregate deben cumplirse de forma inmediata:

- identidad única;
- máquina de estados válida;
- invariantes del dominio;
- integridad de los Value Objects;
- incremento de versión;
- generación de Domain Events.

No puede existir un estado parcialmente válido.

---

# Transacción Conceptual

Toda modificación sigue el siguiente flujo:

```text
Command

↓

Load Citizen

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

Si cualquiera de estos pasos falla, la operación completa debe
cancelarse.

---

# Coordinación entre Aggregates

Cuando una operación involucra otros Aggregates, el Citizen no
los modifica directamente.

Ejemplo:

```text
CitizenActivated

↓

Domain Event

↓

Membership Context

↓

Create Membership
```

Cada Aggregate mantiene su propia consistencia.

---

# Consistencia Eventual

Las operaciones distribuidas siguen un modelo de consistencia
eventual.

Ejemplo:

```text
CitizenVerified

↓

Integration Event

↓

Organization Context

↓

Membership Context

↓

Notification Context
```

Es aceptable que estos procesos ocurran con un desfase temporal,
siempre que el estado final sea consistente.

---

# Invariantes dentro del Boundary

Las siguientes reglas deben cumplirse siempre antes de
confirmar una transacción:

- el CitizenId es único e inmutable;
- el estado pertenece a la máquina de estados;
- los Value Objects son válidos;
- la versión se incrementa correctamente;
- los Domain Events representan hechos ocurridos;
- un Citizen archivado no puede modificarse.

---

# Lo que el Aggregate nunca hace

El Aggregate Citizen nunca:

- consulta otros Aggregates;
- modifica otros Aggregates;
- inicia transacciones distribuidas;
- invoca servicios externos;
- envía correos electrónicos;
- publica mensajes directamente;
- consulta bases de datos externas.

Estas responsabilidades pertenecen a la capa de aplicación o a
la infraestructura.

---

# Relación con Event Sourcing

En una implementación basada en Event Sourcing, el límite de
consistencia permanece inalterado.

La reconstrucción del Aggregate se realiza aplicando únicamente
los Domain Events asociados al mismo **CitizenId**.

No se requieren eventos de otros Aggregates para reconstruir su
estado.

---

# Relación con CQRS

El Aggregate pertenece exclusivamente al lado de escritura.

Las consultas que combinan información de varios Aggregates se
resuelven mediante Read Models y proyecciones.

Esto evita ampliar innecesariamente el límite de consistencia.

---

# Escenario de Ejemplo

```text
RegisterCitizen

↓

CitizenRegistered

↓

Citizen Aggregate actualizado

↓

Commit

↓

CitizenRegistered Event

↓

Notification Context

↓

Organization Context

↓

Analytics Context
```

El Aggregate finaliza su transacción antes de que otros
contextos procesen el evento.

---

# Beneficios

Mantener un límite de consistencia reducido permite:

- transacciones pequeñas;
- menor acoplamiento;
- mayor escalabilidad;
- mejor rendimiento;
- evolución independiente de otros contextos;
- compatibilidad con arquitecturas distribuidas.

---

# Principios Arquitectónicos

El Consistency Boundary del Aggregate Citizen sigue:

- Domain-Driven Design (DDD);
- Aggregate Pattern;
- Event-Driven Architecture;
- CQRS;
- Event Sourcing;
- Clean Architecture;
- Single Responsibility Principle;
- Dependency Inversion Principle.

---

# Definición de Éxito

El Aggregate **Citizen** constituye la unidad oficial de
consistencia para la gestión de identidades cívicas en AURA.
Todas las reglas que requieren consistencia inmediata se
ejecutan dentro de este límite, mientras que la colaboración
con otros Aggregates se realiza mediante eventos y referencias
por identidad, garantizando un dominio desacoplado, escalable y
alineado con los principios de Domain-Driven Design.