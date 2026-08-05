# DOMAIN-001F — Organization Permissions

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
- DOMAIN-001B-State-Machine.md
- DOMAIN-001C-Commands.md
- DOMAIN-001D-Domain-Events.md
- DOMAIN-001E-Invariants.md
- CORE-004-Ubiquitous-Language.md

---

# Objetivo

Definir el modelo de permisos del Aggregate
Organization.

Este documento establece quién puede ejecutar cada
Command del Aggregate desde una perspectiva de dominio.

No define autenticación.

No define autorización técnica.

No depende de JWT, OAuth, Keycloak o cualquier otro
mecanismo de infraestructura.

Únicamente expresa las reglas de negocio relacionadas con
las capacidades que poseen los actores del dominio.

---

# Principios

El modelo de permisos debe cumplir las siguientes reglas.

- basado en capacidades del dominio;
- independiente de la infraestructura;
- explícito;
- auditable;
- determinista;
- extensible;
- consistente con el lenguaje ubicuo.

---

# Conceptos

## Actor

Entidad que ejecuta una acción sobre el dominio.

Ejemplos.

```text
Ciudadano

Miembro

Representante

Administrador Organizacional

Funcionario Municipal

Administrador del Sistema
```

---

## Rol

Conjunto de responsabilidades asignadas a un Actor dentro
de una Organization.

Los roles no representan permisos técnicos.

Representan funciones del dominio.

---

## Permiso

Capacidad para ejecutar un Command específico del
Aggregate.

---

## Política

Regla del dominio que determina si un Actor posee o no un
permiso determinado.

---

# Roles Oficiales

```text
Citizen

Member

Representative

OrganizationAdministrator

MunicipalOfficer

SystemAdministrator
```

---

# Matriz Oficial de Permisos

| Command | Citizen | Member | Representative | Organization Administrator | Municipal Officer | System Administrator |
|----------|:------:|:------:|:--------------:|:--------------------------:|:-----------------:|:--------------------:|
| CreateOrganization | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| SubmitOrganizationForValidation | ✖ | ✖ | ✔ | ✔ | ✖ | ✔ |
| ApproveOrganization | ✖ | ✖ | ✖ | ✖ | ✔ | ✔ |
| RejectOrganization | ✖ | ✖ | ✖ | ✖ | ✔ | ✔ |
| SuspendOrganization | ✖ | ✖ | ✖ | ✔ | ✔ | ✔ |
| ReactivateOrganization | ✖ | ✖ | ✖ | ✔ | ✔ | ✔ |
| ArchiveOrganization | ✖ | ✖ | ✖ | ✔ | ✔ | ✔ |
| DeleteOrganization | ✖ | ✖ | ✖ | ✖ | ✖ | ✔ |
| RenameOrganization | ✖ | ✖ | ✔ | ✔ | ✖ | ✔ |
| ChangeOrganizationAddress | ✖ | ✖ | ✔ | ✔ | ✖ | ✔ |
| ChangeOrganizationPolicies | ✖ | ✖ | ✔ | ✔ | ✖ | ✔ |
| ChangeOrganizationSettings | ✖ | ✖ | ✔ | ✔ | ✖ | ✔ |
| ChangeOrganizationBrand | ✖ | ✖ | ✔ | ✔ | ✖ | ✔ |
| AssignRepresentative | ✖ | ✖ | ✖ | ✔ | ✖ | ✔ |
| RegisterMember | ✖ | ✖ | ✔ | ✔ | ✖ | ✔ |
| RemoveMember | ✖ | ✖ | ✔ | ✔ | ✖ | ✔ |
| ChangeTerritory | ✖ | ✖ | ✔ | ✔ | ✔ | ✔ |

---

# Reglas de Autorización

## REG-001

Todo Command requiere un Actor autenticado.

---

## REG-002

El Actor debe poseer el permiso correspondiente antes de
invocar el Aggregate.

---

## REG-003

El Aggregate nunca consulta sistemas externos para
determinar permisos.

La decisión ya debe haber sido resuelta por la capa de
aplicación.

---

## REG-004

Los permisos nunca dependen de la interfaz de usuario.

---

## REG-005

La existencia de un permiso no garantiza que el Command
sea ejecutable.

Las invariantes y la máquina de estados continúan siendo
la autoridad final.

---

# Ejemplos

## Ejemplo 1

```text
Representative

↓

RenameOrganization
```

Resultado.

```text
Permitido
```

---

## Ejemplo 2

```text
Member

↓

ArchiveOrganization
```

Resultado.

```text
Denegado
```

---

## Ejemplo 3

```text
MunicipalOfficer

↓

ApproveOrganization
```

Resultado.

```text
Permitido
```

---

## Ejemplo 4

```text
Citizen

↓

DeleteOrganization
```

Resultado.

```text
Denegado
```

---

# Relación con Application Services

La validación de permisos ocurre antes de invocar el
Aggregate.

Flujo oficial.

```text
HTTP

↓

Authentication

↓

Authorization

↓

Application Service

↓

Command

↓

Organization Aggregate
```

El Aggregate asume que únicamente recibe Commands cuya
autorización ya fue validada.

No obstante, continúa siendo responsable de proteger sus
invariantes y rechazar operaciones inválidas.

---

# Auditoría

Toda decisión de autorización debe registrar al menos:

```text
ActorId

OrganizationId

Role

Permission

Decision

Timestamp

CorrelationId
```

Esta información permite reconstruir completamente el
historial de decisiones del sistema.

---

# Extensibilidad

Nuevos roles podrán incorporarse sin modificar los
existentes.

Las políticas de autorización deberán implementarse
mediante estrategias (`PermissionPolicy`) o servicios de
dominio especializados, respetando el principio
Open/Closed.

---

# Consideraciones Arquitectónicas

Los permisos del dominio no sustituyen los mecanismos de
seguridad de la infraestructura.

JWT, OAuth2, OpenID Connect, Keycloak o cualquier otro
proveedor únicamente identifican al Actor.

La decisión sobre qué puede hacer ese Actor pertenece al
dominio.

---

# Definición de Éxito

El modelo de permisos del Aggregate Organization garantiza
que toda modificación del dominio sea realizada únicamente
por actores autorizados según las reglas del negocio,
manteniendo una separación clara entre autenticación,
autorización técnica y autorización de dominio, y
preservando la consistencia del modelo de AURA Core.