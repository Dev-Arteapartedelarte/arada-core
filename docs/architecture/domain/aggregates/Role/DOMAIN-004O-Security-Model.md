# DOMAIN-004O — Role Security Model

Versión: 1.0

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
- DOMAIN-004F-Permissions.md
- DOMAIN-004G-Repository-Contract.md
- DOMAIN-004J-Consistency-Boundary.md
- DOMAIN-004K-Integration-Events.md
- DOMAIN-005-Aggregate.md
- CORE-017-Security-Principles.md

---

# Objetivo

Este documento define el modelo oficial de seguridad del
Aggregate **Role**.

Su propósito es proteger la integridad de los cargos
organizacionales, garantizar que únicamente actores autorizados
puedan administrarlos y asegurar que toda modificación sea
auditada y trazable.

El modelo es independiente del mecanismo de autenticación
utilizado por la plataforma.

---

# Principios

La seguridad del Aggregate sigue los principios de:

- Zero Trust;
- Least Privilege;
- Defense in Depth;
- Separation of Duties;
- Auditability;
- Secure by Default.

---

# Alcance

El Aggregate protege únicamente:

- identidad del Role;
- ciclo de vida;
- nombre;
- código;
- descripción;
- estado;
- metadatos del Aggregate.

No administra:

- autenticación;
- sesiones;
- credenciales;
- tokens;
- permisos funcionales;
- políticas IAM.

---

# Modelo Conceptual

```text
Identity

↓

Authentication

↓

Membership

↓

Authorization

↓

Role Aggregate

↓

Repository
```

Toda modificación requiere completar exitosamente esta cadena de
validación.

---

# Autenticación

La autenticación ocurre antes del dominio.

Puede realizarse mediante:

- OpenID Connect;
- OAuth2;
- Keycloak;
- Keyrock (FIWARE);
- Active Directory;
- LDAP;
- otros proveedores compatibles.

El Aggregate no conoce el mecanismo utilizado.

---

# Autorización

La autorización se basa en la Membership del actor y en las
políticas definidas para la Organization.

Antes de ejecutar un Command se valida que el actor posea los
privilegios correspondientes.

Si la validación falla:

```text
PermissionDenied
```

---

# Protección de Commands

Todos los Commands requieren autorización explícita.

| Command | Requiere autorización |
|----------|:---------------------:|
| CreateRole | ✓ |
| RenameRole | ✓ |
| ChangeDescription | ✓ |
| ActivateRole | ✓ |
| DeactivateRole | ✓ |
| ArchiveRole | ✓ |

No existen Commands públicos.

---

# Protección de System Roles

Cuando:

```text
IsSystemRole = true
```

el Aggregate aplica restricciones adicionales.

Ejemplos:

- impedir archivado;
- impedir cambio de código;
- impedir cambio de nombre;
- limitar modificaciones al Platform Administrator.

Estas reglas preservan la estabilidad del sistema.

---

# Integridad del Aggregate

Toda modificación debe respetar:

- invariantes;
- máquina de estados;
- control de versión;
- unicidad de nombre;
- unicidad de código.

Si alguna validación falla:

```text
TransactionRollback
```

---

# Concurrencia

El Aggregate utiliza:

```text
Optimistic Concurrency Control
```

mediante:

```text
Version
```

Ante conflicto:

```text
ConcurrencyConflict
```

No se aceptan sobrescrituras silenciosas.

---

# Auditoría

Toda modificación registra conceptualmente:

```text
ActorId

MembershipId

OrganizationId

RoleId

Command

PreviousVersion

NewVersion

OccurredOn

CorrelationId

CausationId
```

La auditoría debe ser inmutable.

---

# Eventos

Los Domain Events únicamente se generan después de una operación
válida.

Los Integration Events únicamente se publican después del commit.

Nunca deben publicarse eventos para operaciones rechazadas.

---

# Protección del Repository

El Repository debe garantizar:

- persistencia atómica;
- validación de versión;
- preservación de invariantes;
- ausencia de cambios parciales.

Nunca debe aceptar un Aggregate inválido.

---

# Información Sensible

El Aggregate no almacena:

- contraseñas;
- claves privadas;
- secretos;
- tokens;
- certificados;
- información biométrica.

Toda la información administrada es de naturaleza organizacional.

---

# Protección de Identificadores

Los identificadores del dominio:

```text
RoleId

OrganizationId
```

son inmutables.

Nunca pueden reutilizarse.

Nunca deben modificarse después de la creación.

---

# Consistencia

Toda operación sigue el flujo:

```text
Authenticate

↓

Authorize

↓

Load Aggregate

↓

Validate Invariants

↓

Execute Command

↓

Persist

↓

Commit

↓

Publish Events
```

No existen estados intermedios visibles.

---

# Integración

Los consumidores externos únicamente reciben:

```text
Integration Events
```

No acceden directamente al Aggregate ni a su estado interno.

---

# Amenazas Mitigadas

El modelo protege frente a:

- modificaciones no autorizadas;
- escalamiento de privilegios;
- cambios concurrentes;
- duplicidad de Roles;
- corrupción del Aggregate;
- publicación de eventos inconsistentes;
- pérdida de trazabilidad.

---

# Responsabilidades

## Aggregate

- proteger invariantes;
- validar estado;
- generar Domain Events.

## Application Service

- autenticar;
- autorizar;
- coordinar transacciones;
- invocar el Repository.

## Infraestructura

- persistencia;
- cifrado en tránsito;
- cifrado en reposo;
- gestión de identidades;
- monitoreo;
- registro de auditoría.

---

# Compatibilidad Arquitectónica

Este modelo es compatible con:

- Domain-Driven Design (DDD);
- Zero Trust Architecture;
- Role-Based Access Control (RBAC);
- OAuth2;
- OpenID Connect;
- FIWARE Keyrock;
- CQRS;
- Event Sourcing;
- Clean Architecture.

---

# Definición de Éxito

El modelo de seguridad del Aggregate **Role** garantiza que toda
administración de cargos organizacionales se realice únicamente
por actores autorizados, preservando la integridad del dominio,
la trazabilidad completa de las operaciones y la protección de
los Roles críticos del ecosistema AURA. La separación entre
autenticación, autorización y lógica de negocio mantiene un
diseño seguro, desacoplado y alineado con los principios de
arquitectura empresarial y Smart Cities.