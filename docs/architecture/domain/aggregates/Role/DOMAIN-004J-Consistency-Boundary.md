# DOMAIN-004J — Role Consistency Boundary

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
- DOMAIN-004G-Repository-Contract.md
- DOMAIN-004I-Versioning.md
- DOMAIN-004K-Integration-Events.md
- CORE-008-Aggregate-Design-Rules.md

---

# Objetivo

Este documento define el **límite de consistencia (Consistency
Boundary)** del Aggregate **Role**.

El Aggregate constituye la unidad mínima de consistencia del
dominio. Todas las reglas de negocio que afectan directamente a
un Role deben cumplirse dentro de una única transacción.

Las interacciones con otros Aggregates se realizan mediante
identificadores, Domain Events o Application Services, evitando
transacciones distribuidas.

---

# Principios

El límite de consistencia sigue los siguientes principios:

- un Aggregate por transacción;
- consistencia fuerte dentro del Aggregate;
- consistencia eventual entre Aggregates;
- independencia entre Bounded Contexts;
- ausencia de referencias directas a otros Aggregates;
- preservación permanente de las invariantes.

---

# Límite del Aggregate

El Aggregate **Role** está compuesto exclusivamente por:

```text
Role (Aggregate Root)
```

Toda modificación debe realizarse únicamente a través del
Aggregate Root.

---

# Información Propia

El Aggregate administra exclusivamente información relacionada
con un cargo organizacional.

Ejemplos:

```text
RoleId

OrganizationId

Name

Code

Description

RoleType

Status

IsSystemRole

Version
```

Toda esta información debe mantenerse consistente dentro del
Aggregate.

---

# Información Externa

El Aggregate puede conocer únicamente los identificadores de
otros Aggregates.

Ejemplos:

```text
OrganizationId
```

No mantiene referencias directas a:

```text
Organization

Citizen

Membership

Permission

Committee

Assembly
```

---

# Consistencia Interna

Las siguientes reglas deben cumplirse siempre dentro de la misma
transacción:

- nombre válido;
- nombre único dentro de la Organization;
- código único dentro de la Organization;
- estado válido;
- transición permitida;
- versión consistente;
- preservación de invariantes.

---

# Operaciones Atómicas

Los siguientes Commands modifican el Aggregate en una única
transacción:

```text
CreateRole

RenameRole

ChangeDescription

ActivateRole

DeactivateRole

ArchiveRole
```

Ninguno puede producir cambios parciales.

---

# Operaciones Excluidas

El Aggregate **Role** no ejecuta operaciones sobre:

- Membership;
- Citizen;
- Organization;
- Permission;
- Notification.

Estas operaciones pertenecen a otros Aggregates o a Application
Services.

---

# Relación con Membership

Role no contiene MembershipIds y Membership no contiene RoleIds en el
baseline 1.0. La asignación se difiere hasta definir un Source of Truth
independiente y contratos explícitos.

---

# Relación con Organization

Todo Role pertenece exactamente a una Organization.

La validación de existencia de la Organization ocurre antes de
la creación del Aggregate, normalmente en un Application
Service.

Una vez creado:

```text
OrganizationId
```

es inmutable.

---

# Relación con Permission

Permission es una capacidad exigida para ejecutar Commands; no pertenece
al estado de Role ni constituye un Aggregate del baseline.

---

# Publicación de Eventos

Al finalizar una transacción exitosa:

```text
Persist Aggregate

↓

Commit

↓

Publish Internal Domain Events
```

Nunca deben publicarse eventos antes del commit.

---

# Consistencia Eventual

Los cambios que afectan a otros Aggregates se propagan mediante
Integration Events.

Ejemplo:

```text
RoleActivated

↓

RoleActivatedIntegrationEvent

↓

Membership

↓

Authorization
```

Cada Aggregate mantiene su propia consistencia interna.

---

# Concurrencia

Toda modificación valida:

```text
Version
```

Si la versión esperada no coincide:

```text
ConcurrencyConflict
```

La transacción completa es cancelada.

---

# Reglas de Diseño

El Aggregate **Role**:

- no consulta otros Repositories;
- no modifica otros Aggregates;
- no inicia transacciones distribuidas;
- no contiene lógica de infraestructura;
- no conoce mecanismos de persistencia;
- no depende de servicios externos.

---

# Responsabilidades

Dentro del Aggregate:

- validar invariantes;
- controlar el ciclo de vida;
- administrar el estado;
- generar Domain Events;
- proteger la identidad del Role.

Fuera del Aggregate:

- autenticación;
- autorización técnica;
- consultas complejas;
- integración entre Bounded Contexts;
- envío de notificaciones;
- asignación de Permissions.

---

# Compatibilidad con Event Sourcing

Cuando Event Sourcing está habilitado, el límite de consistencia
permanece inalterado.

La reconstrucción del Aggregate se realiza aplicando únicamente
los Domain Events del propio Role.

No se requieren eventos provenientes de otros Aggregates para
obtener un estado consistente.

---

# Compatibilidad Arquitectónica

Este modelo es compatible con:

- Domain-Driven Design (DDD);
- Clean Architecture;
- CQRS;
- Event Sourcing;
- Event-Driven Architecture.

---

# Definición de Éxito

El límite de consistencia del Aggregate **Role** garantiza que
toda modificación sobre un cargo organizacional se ejecute de
forma atómica, preservando las invariantes del dominio y evitando
acoplamientos con otros Aggregates. La separación entre
consistencia fuerte interna y consistencia eventual externa
proporciona una arquitectura escalable, mantenible y alineada
con los principios de DDD que sustentan el ecosistema AURA.