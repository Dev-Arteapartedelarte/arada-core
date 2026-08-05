# DOMAIN-001G — Organization Repository Contract

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
- CORE-011-Repository-Contracts.md
- CORE-016-Dependency-Rules.md

---

# Objetivo

Definir el contrato oficial del Repository del Aggregate
Organization.

El Repository constituye el único mecanismo autorizado
para recuperar y persistir Aggregates del dominio.

No implementa lógica de negocio.

No conoce casos de uso.

No contiene consultas de infraestructura.

Su responsabilidad es preservar la consistencia del
Aggregate.

---

# Responsabilidades

El Repository debe:

- recuperar Aggregates;
- persistir Aggregates completos;
- garantizar consistencia transaccional;
- controlar concurrencia;
- preservar el versionado;
- publicar Domain Events mediante Outbox.

El Repository nunca ejecuta reglas de negocio.

---

# Principios

El contrato del Repository debe cumplir los siguientes
principios.

- pertenece al dominio;
- no depende de infraestructura;
- no depende del ORM;
- no depende de SQL;
- no depende de MongoDB;
- no depende de Frameworks;
- trabaja exclusivamente con Aggregates.

---

# Ubicación

```text
src/

└── domain/

    └── organization/

        └── repositories/

            └── OrganizationRepository.ts
```

---

# Contrato Oficial

```text
OrganizationRepository
```

Operaciones mínimas.

```text
save()

findById()

exists()

delete()
```

No deben existir operaciones que permitan modificar partes
del Aggregate.

---

# save()

## Responsabilidad

Persistir el Aggregate completo.

Debe garantizar:

- atomicidad;
- consistencia;
- incremento de versión;
- almacenamiento de Domain Events.

Firma conceptual.

```text
save(
    organization,
): Promise<void>
```

---

# findById()

## Responsabilidad

Recuperar una Organization mediante su identidad.

Firma conceptual.

```text
findById(
    organizationId,
): Promise<Organization | null>
```

Nunca retorna objetos parciales.

---

# exists()

## Responsabilidad

Verificar la existencia del Aggregate.

Firma conceptual.

```text
exists(
    organizationId,
): Promise<boolean>
```

No debe cargar el Aggregate completo.

---

# delete()

## Responsabilidad

Eliminar lógicamente el Aggregate cuando el dominio lo
permita.

Firma conceptual.

```text
delete(
    organizationId,
): Promise<void>
```

No debe eliminar físicamente los registros históricos.

---

# Consistencia

El Repository trabaja exclusivamente con el Aggregate
completo.

Nunca debe persistir:

- entidades aisladas;
- Value Objects independientes;
- colecciones parciales.

La unidad de persistencia coincide con la unidad de
consistencia.

---

# Concurrencia

El Repository debe soportar concurrencia optimista.

Cada Aggregate posee un número de versión.

```text
Organization

↓

Version = 12
```

Durante la persistencia.

```text
Version 12

↓

Version 13
```

Si la versión almacenada no coincide con la esperada, la
operación debe fallar.

---

# Control de Versiones

Toda modificación válida incrementa la versión.

```text
v1

↓

v2

↓

v3

↓

v4
```

La versión nunca disminuye.

---

# Persistencia de Eventos

El Repository no publica eventos directamente.

El flujo oficial es.

```text
Organization Aggregate

↓

Repository

↓

Outbox

↓

Commit

↓

Event Bus
```

Esto garantiza consistencia entre el estado persistido y
los Domain Events.

---

# Consultas

Las consultas complejas no pertenecen al Repository del
Aggregate.

Ejemplos.

```text
Buscar organizaciones activas.

Buscar organizaciones por comuna.

Buscar organizaciones creadas este año.

Buscar organizaciones por categoría.
```

Estas consultas pertenecen al modelo de lectura (Read
Model) o a servicios especializados de consulta.

---

# Restricciones

El Repository nunca debe:

- ejecutar reglas del dominio;
- modificar entidades internas;
- emitir Domain Events;
- invocar servicios externos;
- realizar validaciones de negocio;
- conocer HTTP;
- conocer UI;
- conocer JWT;
- conocer OAuth;
- conocer Frameworks.

---

# Dependencias Permitidas

El contrato del Repository puede depender únicamente de:

```text
Organization

OrganizationId

Domain Errors

Value Objects
```

No puede depender de:

```text
Infrastructure

Persistence

ORM

MongoDB

PostgreSQL

Redis

REST

GraphQL
```

---

# Implementaciones

El dominio define únicamente el contrato.

Las implementaciones pertenecen a Infrastructure.

Ejemplos.

```text
MongoOrganizationRepository

PostgreSQLOrganizationRepository

MemoryOrganizationRepository

EventStoreOrganizationRepository
```

Todas implementan exactamente el mismo contrato del
dominio.

---

# Pruebas

El contrato debe poder sustituirse por implementaciones
en memoria durante pruebas.

Ejemplo.

```text
OrganizationRepository

↓

InMemoryOrganizationRepository
```

Esto permite probar el Aggregate sin depender de una base
de datos.

---

# Reglas

## REG-001

Un Repository administra un único Aggregate Root.

---

## REG-002

Todo Aggregate se recupera completo.

---

## REG-003

Todo Aggregate se persiste completo.

---

## REG-004

Los Repository son interfaces del dominio.

---

## REG-005

Las implementaciones pertenecen a Infrastructure.

---

## REG-006

El Repository nunca contiene lógica de negocio.

---

## REG-007

La publicación de Domain Events ocurre únicamente después
de una persistencia exitosa mediante el patrón Outbox.

---

## REG-008

El Repository garantiza la integridad transaccional del
Aggregate durante las operaciones de lectura y escritura.

---

# Definición de Éxito

El contrato `OrganizationRepository` establece una
abstracción estable, independiente de la infraestructura y
alineada con Domain-Driven Design. Garantiza que el
Aggregate `Organization` sea recuperado y persistido como
una única unidad de consistencia, preservando sus
invariantes, soportando concurrencia optimista y
habilitando la publicación confiable de Domain Events
mediante el patrón Outbox.