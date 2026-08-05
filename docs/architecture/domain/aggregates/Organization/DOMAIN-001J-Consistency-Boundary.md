# DOMAIN-001J — Organization Consistency Boundary

Versión: 1.0

Estado:
Oficial

Proyecto:
AURA Core

Bounded Context:
Organization Management

Aggregate:
Organization

Autor:
ARADA

Documentos Relacionados:

- DOMAIN-001-Aggregate.md
- DOMAIN-001E-Invariants.md
- DOMAIN-001G-Repository-Contract.md
- DOMAIN-001I-Versioning.md
- DOMAIN-001K-Integration-Events.md
- CORE-007-Strategic-Design.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Definir el límite de consistencia (Consistency Boundary)
del Aggregate Organization.

Este documento establece qué información debe mantenerse
consistente mediante una transacción única y qué cambios
pueden propagarse posteriormente mediante eventos.

---

# Definición

Un Aggregate representa una frontera de consistencia.

Todo lo que ocurre dentro de esa frontera debe permanecer
consistente inmediatamente.

Todo lo que queda fuera de esa frontera puede alcanzar
consistencia eventual.

---

# Principio Fundamental

```text
Una transacción

↓

Un Aggregate

↓

Una única garantía de consistencia
```

Nunca una transacción de dominio debe modificar múltiples
Aggregates simultáneamente.

---

# Alcance del Aggregate

El Aggregate Organization garantiza consistencia sobre:

- identidad;
- nombre;
- estado;
- representante activo;
- territorio asignado;
- políticas internas;
- versión;
- invariantes.

Todo lo anterior pertenece a una única unidad de
consistencia.

---

# Elementos Dentro del Boundary

```text
Organization

├── OrganizationId
├── OrganizationName
├── OrganizationType
├── OrganizationStatus
├── Representative
├── TerritoryReference
├── Policies
├── Metadata
└── Version
```

Todos estos elementos se modifican mediante un único
Aggregate Root.

---

# Elementos Fuera del Boundary

Los siguientes elementos pertenecen a otros Bounded
Contexts.

```text
User

Citizen

Municipality

Notification

Participation

Identity

Analytics

FIWARE

Blockchain

Documents

Audit

Payments
```

El Aggregate Organization nunca modifica directamente
ninguno de ellos.

---

# Ejemplo

Incorrecto.

```text
Approve Organization

↓

Actualizar usuario

↓

Actualizar permisos

↓

Actualizar municipio

↓

Actualizar FIWARE
```

Esta operación rompe el límite de consistencia.

---

Correcto.

```text
Approve Organization

↓

OrganizationApproved

↓

Commit

↓

Integration Event

↓

Cada contexto actualiza
su propio modelo
```

---

# Consistencia Inmediata

Debe garantizarse inmediatamente:

- una organización tiene un único estado;
- una organización posee un único representante activo;
- la transición de estado es válida;
- el nombre cumple las reglas;
- la versión aumenta correctamente.

Estas reglas nunca pueden quedar en un estado
intermedio.

---

# Consistencia Eventual

Puede alcanzarse posteriormente:

- envío de correos;
- notificaciones;
- actualización municipal;
- sincronización con FIWARE;
- generación de reportes;
- proyecciones CQRS;
- Data Lake;
- Blockchain.

---

# Ejemplo de Flujo

```text
Create Organization

↓

Aggregate

↓

Persist

↓

Commit

↓

OrganizationCreated

↓

Outbox

↓

Event Bus

↓

Notification

↓

Municipality

↓

Analytics

↓

FIWARE
```

El Aggregate finaliza antes de iniciar las integraciones.

---

# Transacciones

Cada Command produce una única transacción.

```text
Command

↓

Aggregate

↓

Repository

↓

Commit
```

No existen transacciones distribuidas entre Bounded
Contexts.

---

# Reglas para Referencias

Los Aggregates sólo conservan referencias.

Ejemplo.

Correcto.

```text
RepresentativeId
```

Incorrecto.

```text
Representative Entity
```

Correcto.

```text
TerritoryId
```

Incorrecto.

```text
Territory Aggregate
```

---

# Comunicación Entre Contextos

La comunicación ocurre únicamente mediante eventos.

```text
Aggregate

↓

Domain Event

↓

Integration Event

↓

Consumers
```

Nunca mediante llamadas directas entre Aggregates.

---

# Consistencia y Versionado

Cada modificación válida:

```text
Version + 1
```

La versión identifica un estado consistente del
Aggregate.

---

# Consistencia y Repositorio

El Repository siempre persiste el Aggregate completo.

Nunca persiste únicamente una parte del Aggregate.

```text
Organization

↓

Repository

↓

Atomic Save
```

---

# Consistencia y CQRS

Write Model.

```text
Consistencia inmediata
```

Read Model.

```text
Consistencia eventual
```

Los modelos de lectura pueden tardar algunos segundos en
reflejar el cambio.

---

# Consistencia y FIWARE

El Aggregate nunca conoce:

- Orion Context Broker;
- NGSI-LD;
- IoT Agents;
- Smart Data Models.

El evento de integración es el único punto de conexión.

```text
Organization

↓

Integration Event

↓

FIWARE Adapter
```

---

# Consistencia y Municipalidad

La actualización del registro municipal ocurre después
del Commit.

Nunca durante la ejecución del Aggregate.

---

# Reglas

## REG-001

El Aggregate Organization constituye una única frontera
de consistencia.

---

## REG-002

Toda modificación del Aggregate ocurre dentro de una
única transacción.

---

## REG-003

Las integraciones externas utilizan consistencia
eventual.

---

## REG-004

Ningún Aggregate modifica directamente otro Aggregate.

---

## REG-005

Los Aggregates se relacionan mediante identificadores.

---

## REG-006

Toda comunicación entre Bounded Contexts ocurre mediante
Integration Events.

---

## REG-007

El Repository persiste el Aggregate completo.

---

## REG-008

Las invariantes siempre se validan antes del Commit.

---

## REG-009

La versión representa un estado consistente del
Aggregate.

---

## REG-010

Las dependencias hacia infraestructura, APIs externas,
FIWARE o municipios quedan completamente fuera del
Consistency Boundary.

---

# Diagrama Conceptual

```text
                 CONSISTENCY BOUNDARY

        ┌───────────────────────────────────────┐
        │                                       │
        │            Organization               │
        │                                       │
        │  Id                                   │
        │  Name                                 │
        │  Status                               │
        │  Representative                       │
        │  TerritoryId                          │
        │  Policies                             │
        │  Version                              │
        │                                       │
        └───────────────────────────────────────┘
                         │
                  Domain Events
                         │
                         ▼
                  Integration Events
                         │
      ┌──────────┬──────────┬──────────┬──────────┐
      ▼          ▼          ▼          ▼
 Municipality  FIWARE  Notifications Analytics
```

---

# Definición de Éxito

El Aggregate `Organization` define una única frontera de consistencia donde todas las reglas de negocio, invariantes, estado y versionado se mantienen mediante una transacción atómica. Toda interacción con otros Bounded Contexts, municipios, FIWARE, servicios de notificación o futuras plataformas ocurre exclusivamente mediante Integration Events, garantizando un dominio desacoplado, consistente y preparado para escalar dentro de la arquitectura de AURA Core.