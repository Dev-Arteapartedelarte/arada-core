# DOMAIN-004G — Role Repository Contract

Versión: 1.1

Estado:
Official

Proyecto:
AURA Core

Bounded Context:
Authorization Management

Aggregate:
Role

Documentos relacionados:

- DOMAIN-004-Aggregate.md
- DOMAIN-004C-Commands.md
- DOMAIN-004D-Domain-Events.md
- DOMAIN-004E-Invariants.md
- DOMAIN-004I-Versioning.md
- DOMAIN-004J-Consistency-Boundary.md
- CORE-011-Repository-Contracts.md

---

# Objetivo

Este documento define el contrato oficial que debe cumplir todo
Repository del Aggregate **Role**.

El Repository constituye el mecanismo de persistencia del
Aggregate Root y garantiza que el dominio permanezca
independiente de cualquier tecnología de almacenamiento.

El dominio únicamente conoce el contrato; la implementación
pertenece a la capa de infraestructura.

---

# Responsabilidades

Un Repository de Role es responsable de:

- recuperar Aggregates;
- persistir Aggregates;
- aplicar control de concurrencia;
- garantizar la consistencia transaccional;
- nunca exponer detalles de infraestructura.

No es responsable de:

- ejecutar lógica de negocio;
- validar Commands;
- aplicar permisos;
- publicar eventos;
- implementar consultas complejas.

---

# Aggregate Root

El Repository administra exclusivamente:

```text
Role
```

Nunca administra entidades internas de forma independiente.

---

# Contrato Conceptual

```text
RoleRepository
```

Operaciones oficiales:

```text
Save()

FindById()

FindByCode()

FindByName()

Exists()

Delete()
```

La nomenclatura puede variar según el lenguaje de programación,
pero el comportamiento funcional debe mantenerse.

---

# Save

## Objetivo

Persistir el Aggregate completo.

## Entrada

```text
Role
```

## Resultado

```text
Role
```

## Reglas

- persiste el Aggregate completo;
- incrementa Version;
- verifica concurrencia optimista;
- persiste cambios de forma atómica.

---

# FindById

## Objetivo

Recuperar un Aggregate mediante:

```text
RoleId
```

## Entrada

```text
RoleId
```

## Resultado

```text
Role | Null
```

---

# FindByCode

## Objetivo

Buscar un Role por su código dentro de una Organization.

## Entrada

```text
OrganizationId

Code
```

## Resultado

```text
Role | Null
```

---

# FindByName

## Objetivo

Buscar un Role por nombre dentro de una Organization.

## Entrada

```text
OrganizationId

Name
```

## Resultado

```text
Role | Null
```

---

# Exists

## Objetivo

Determinar si el Role existe.

## Entrada

```text
RoleId
```

## Resultado

```text
Boolean
```

---

# Delete

## Objetivo

Eliminar físicamente un Aggregate.

## Política del dominio

En AURA los Roles **no se eliminan físicamente**.

La operación existe únicamente para cumplir el contrato
conceptual del Repository.

La política oficial del dominio es:

```text
ArchiveRole
```

Por lo tanto:

```text
Delete()

↓

No soportado
```

La infraestructura podrá lanzar:

```text
UnsupportedOperation
```

o una excepción equivalente.

---

# Consistencia

Todas las operaciones del Repository son:

- atómicas;
- determinísticas;
- consistentes;
- repetibles.

Nunca se persisten cambios parciales.

---

# Control de Concurrencia

El Repository debe validar:

```text
Version
```

Proceso:

```text
Load Aggregate

↓

Validate Version

↓

Persist Aggregate

↓

Commit
```

Si la versión esperada no coincide:

```text
ConcurrencyConflict
```

---

# Integridad

Antes de persistir un Aggregate deben cumplirse todas las
invariantes definidas en:

```text
DOMAIN-004E-Invariants.md
```

El Repository nunca debe almacenar un Aggregate inválido.

---

# Independencia Tecnológica

Este contrato no depende de:

- PostgreSQL;
- MySQL;
- SQL Server;
- MongoDB;
- Cosmos DB;
- EventStore;
- DynamoDB;
- archivos;
- memoria.

Todas las implementaciones deben respetar el mismo contrato.

---

# Relaciones

El Repository no administra directamente:

- Organization;
- Membership;
- Citizen;
- Permission.

Las relaciones se mantienen mediante identificadores.

---

# Caché

Las implementaciones podrán incorporar mecanismos de caché
siempre que:

- no alteren el comportamiento observable;
- respeten Version;
- preserven la consistencia del Aggregate.

---

# Event Sourcing

Cuando se utilice Event Sourcing, el Repository podrá
reconstruir el Aggregate aplicando los Domain Events.

Ejemplo:

```text
RoleCreated

↓

RoleActivated

↓

RoleRenamed

↓

RoleArchived
```

El contrato funcional permanece inalterado.

---

# Pruebas

Toda implementación debe demostrar, como mínimo:

- persistencia correcta;
- recuperación por identificador;
- recuperación por nombre;
- recuperación por código;
- validación de concurrencia;
- preservación de invariantes;
- rechazo de operaciones inválidas.

---

# Compatibilidad Arquitectónica

Este contrato es compatible con:

- Domain-Driven Design (DDD);
- Repository Pattern;
- Clean Architecture;
- CQRS;
- Event Sourcing.

---

# Definición de Éxito

El contrato del Repository del Aggregate **Role** garantiza una
persistencia consistente, desacoplada y tecnológicamente
independiente. Al actuar exclusivamente sobre el Aggregate Root
y respetar las invariantes del dominio, proporciona una base
estable para cualquier implementación de infraestructura sin
comprometer la integridad del modelo de autorización de AURA.