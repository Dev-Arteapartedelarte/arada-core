# DOMAIN-003G — Membership Repository Contract

Versión: 1.0

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Membership Management

Aggregate:
Membership

Documentos relacionados:

- DOMAIN-003-Aggregate.md
- DOMAIN-003E-Invariants.md
- CORE-011-Repository-Contracts.md
- DOMAIN-001G-Repository-Contract.md
- DOMAIN-002G-Repository-Contract.md

---

# Objetivo

Este documento define el contrato oficial del Repository del
Aggregate **Membership**.

El Repository constituye el mecanismo mediante el cual la capa
de dominio recupera y persiste Aggregates sin conocer detalles
de infraestructura.

El contrato representa únicamente el comportamiento esperado;
no define tecnologías, motores de base de datos ni protocolos
de acceso.

---

# Responsabilidad

El Repository es responsable de:

- recuperar Memberships;
- persistir Memberships;
- eliminar lógicamente cuando corresponda;
- controlar concurrencia optimista;
- garantizar consistencia del Aggregate.

No es responsable de:

- aplicar reglas de negocio;
- validar permisos;
- ejecutar Commands;
- generar Domain Events;
- construir Read Models;
- realizar consultas analíticas.

---

# Principios

Todo Repository debe cumplir:

- Persistencia transparente.
- Independencia tecnológica.
- Una única responsabilidad.
- Consistencia del Aggregate.
- Control de concurrencia.
- Bajo acoplamiento.
- Alta cohesión.

---

# Contrato Conceptual

```text
MembershipRepository
```

El Repository expone únicamente operaciones compatibles con el
modelo del dominio.

---

# Operaciones Obligatorias

## Save

Persistir un Aggregate.

```text
save(membership)
```

Responsabilidades:

- insertar o actualizar;
- verificar versión;
- persistir eventos pendientes;
- mantener atomicidad.

---

## FindById

Recuperar una Membership mediante su identidad.

```text
find_by_id(MembershipId)
```

Resultado:

```text
Membership | None
```

---

## Exists

Verificar existencia.

```text
exists(MembershipId)
```

Resultado:

```text
Boolean
```

---

## Delete

Eliminar lógicamente el Aggregate cuando la política del dominio
lo permita.

```text
delete(MembershipId)
```

En implementaciones Event Sourcing normalmente equivale a una
marca lógica o a un evento de archivado.

---

# Consultas de Dominio

El contrato admite consultas necesarias para preservar las
invariantes del Aggregate.

## Find Active Membership

```text
find_active_membership(
    CitizenId,
    OrganizationId
)
```

Resultado:

```text
Membership | None
```

Uso:

Verificar la unicidad de membresías activas.

---

## Exists Active Membership

```text
exists_active_membership(
    CitizenId,
    OrganizationId
)
```

Resultado:

```text
Boolean
```

---

## Find By Citizen

```text
find_by_citizen(CitizenId)
```

Resultado:

```text
Collection<Membership>
```

---

## Find By Organization

```text
find_by_organization(
    OrganizationId
)
```

Resultado:

```text
Collection<Membership>
```

---

## Find By Status

```text
find_by_status(Status)
```

Resultado:

```text
Collection<Membership>
```

---

# Operaciones Prohibidas

El Repository nunca debe exponer métodos como:

```text
approve()

activate()

terminate()

suspend()

reactivate()
```

Estos comportamientos pertenecen exclusivamente al Aggregate.

---

# Consistencia

Toda persistencia debe:

- ejecutarse en una única transacción;
- preservar las invariantes;
- respetar la versión del Aggregate;
- impedir escrituras concurrentes inconsistentes.

---

# Concurrencia

El Repository utiliza:

```text
Optimistic Concurrency Control
```

Cada actualización verifica:

```text
Version
```

Si existe conflicto:

```text
ConcurrencyException
```

---

# Event Sourcing

Cuando el sistema utilice Event Sourcing:

El Repository deberá:

- reconstruir el Aggregate aplicando eventos;
- almacenar nuevos eventos;
- actualizar snapshots cuando corresponda.

Nunca modifica eventos históricos.

---

# CQRS

El Repository pertenece únicamente al modelo de escritura.

Las consultas complejas deben resolverse mediante Read Models.

---

# Domain Events

Después de una persistencia exitosa:

- los Domain Events quedan registrados;
- posteriormente pueden publicarse mediante Outbox Pattern.

El Repository no publica eventos.

---

# Errores Esperados

El contrato puede producir:

```text
MembershipNotFound

ConcurrencyConflict

DuplicateActiveMembership

PersistenceFailure
```

Los errores pertenecen al modelo de dominio o infraestructura,
según corresponda.

---

# Independencia Tecnológica

El contrato es compatible con:

- PostgreSQL;
- MongoDB;
- EventStoreDB;
- SQL Server;
- MySQL;
- SQLite;
- almacenamiento distribuido.

La implementación concreta pertenece a Infrastructure.

---

# Responsabilidad Arquitectónica

```text
Application

↓

MembershipRepository

↓

Infrastructure
```

El dominio depende únicamente de la abstracción.

---

# Compatibilidad con Clean Architecture

El contrato reside en:

```text
Domain Layer
```

Las implementaciones viven en:

```text
Infrastructure Layer
```

La dirección de dependencia siempre apunta hacia el dominio.

---

# Ejemplo Conceptual

```text
CreateMembershipCommand

↓

Application Service

↓

MembershipRepository.find_active_membership()

↓

Membership Aggregate

↓

MembershipRepository.save()

↓

Commit
```

---

# Evolución

Las futuras extensiones deberán:

- mantener compatibilidad con el contrato;
- no romper las invariantes;
- conservar la independencia tecnológica;
- preservar la semántica del dominio.

---

# Principios Arquitectónicos

Este contrato sigue:

- Domain-Driven Design (DDD);
- Repository Pattern;
- Clean Architecture;
- CQRS;
- Event Sourcing;
- Dependency Inversion Principle (DIP);
- Interface Segregation Principle (ISP).

---

# Definición de Éxito

El **Membership Repository** proporciona una abstracción única
para recuperar y persistir Aggregates **Membership**,
garantizando consistencia, control de concurrencia e
independencia de la infraestructura. Su contrato protege las
invariantes del dominio y constituye el único punto autorizado
de acceso persistente al Aggregate dentro del modelo de
escritura de AURA.