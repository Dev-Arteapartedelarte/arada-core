# DOMAIN-002F — Citizen Permissions

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
- DOMAIN-002A-Lifecycle.md
- DOMAIN-002B-State-Machine.md
- DOMAIN-002C-Commands.md
- DOMAIN-002E-Invariants.md
- CORE-007-Strategic-Design.md

---

# Objetivo

Este documento define el modelo de permisos del Aggregate
Citizen.

Los permisos establecen quién puede ejecutar Commands sobre un
Citizen y bajo qué condiciones.

El Aggregate nunca conoce usuarios, sesiones, JWT, OAuth,
Keycloak o mecanismos de autenticación.

Únicamente recibe una decisión de autorización proveniente de
la capa de aplicación.

---

# Principios

El modelo de permisos sigue los siguientes principios:

- separación entre autenticación y autorización;
- mínimo privilegio;
- denegación por defecto;
- independencia de infraestructura;
- autorización previa a la ejecución del Aggregate;
- trazabilidad completa.

---

# Modelo Conceptual

```text
Identity

        │

        ▼

Authentication

        │

        ▼

Authorization

        │

        ▼

Application Service

        │

        ▼

Citizen Aggregate
```

El Aggregate nunca autentica usuarios.

---

# Responsabilidades

## Infrastructure

Responsable de:

- autenticación;
- emisión de tokens;
- sesiones;
- proveedores de identidad;
- certificados.

---

## Application Layer

Responsable de:

- autorización;
- políticas;
- roles;
- permisos;
- validación previa.

---

## Aggregate

Responsable únicamente de:

- validar reglas de negocio;
- validar invariantes;
- ejecutar Commands válidos.

---

# Actores Conceptuales

El dominio reconoce los siguientes actores.

```text
Citizen

Organization Administrator

Municipal Operator

System Administrator

External System
```

Estos actores representan roles del dominio.

No representan usuarios técnicos.

---

# Matriz de Permisos

| Command | Citizen | Org. Admin | Municipal Operator | System Admin | External System |
|----------|----------|------------|--------------------|--------------|-----------------|
| RegisterCitizen | Sí | Sí | Sí | Sí | Sí |
| RequestCitizenVerification | Sí | Sí | Sí | Sí | No |
| VerifyCitizen | No | No | Sí | Sí | No |
| ActivateCitizen | No | Sí | Sí | Sí | No |
| SuspendCitizen | No | Sí | Sí | Sí | No |
| ReactivateCitizen | No | Sí | Sí | Sí | No |
| DeactivateCitizen | Sí | Sí | Sí | Sí | No |
| ArchiveCitizen | No | No | Sí | Sí | No |
| UpdateCitizenProfile | Sí | Sí* | Sí* | Sí | No |
| UpdateCitizenContactInformation | Sí | No | Sí | Sí | No |
| UpdateCitizenAddress | Sí | No | Sí | Sí | No |
| ChangePreferredLanguage | Sí | No | No | Sí | No |
| AcceptPrivacyPolicy | Sí | No | No | No | No |
| WithdrawConsent | Sí | No | No | Sí | No |

\* Sólo cuando exista autorización explícita definida por las
políticas del dominio.

---

# Principio de Propiedad

Un Citizen puede modificar únicamente su propia información
personal, salvo que una política de negocio otorgue permisos a
otro actor autorizado.

---

# Principio de Delegación

La delegación de permisos pertenece al dominio de
autorización.

El Aggregate Citizen no implementa mecanismos de delegación.

---

# Restricciones

Nunca está permitido:

- activar un Citizen sin verificación;
- modificar un Citizen archivado;
- suspender un Citizen inexistente;
- ejecutar Commands sobre versiones obsoletas;
- omitir la validación de permisos.

---

# Permisos sobre Estados

Algunas operaciones dependen simultáneamente del rol y del
estado del Aggregate.

Ejemplos:

```text
Draft

↓

RequestCitizenVerification
```

Permitido.

---

```text
Archived

↓

UpdateCitizenProfile
```

Prohibido.

---

```text
Suspended

↓

ReactivateCitizen
```

Permitido únicamente para actores autorizados.

---

# Auditoría

Toda decisión de autorización debe ser registrada.

Como mínimo:

- actor;
- AggregateId;
- Command;
- fecha y hora;
- resultado;
- motivo del rechazo (si existe).

La auditoría pertenece a otro Bounded Context y no al
Aggregate Citizen.

---

# Integración con RBAC

El dominio es compatible con modelos Role-Based Access
Control.

Ejemplos:

```text
Citizen

↓

Role

↓

Permissions

↓

Commands
```

La implementación concreta pertenece a la infraestructura o a
un servicio de autorización.

---

# Integración con ABAC

También es compatible con Attribute-Based Access Control.

Ejemplos de atributos:

- estado del Citizen;
- organización;
- territorio;
- tipo de membresía;
- nivel de confianza;
- vigencia de credenciales.

El Aggregate permanece independiente de dichas políticas.

---

# Compatibilidad con Event Sourcing

La autorización nunca modifica el historial del Aggregate.

Únicamente los Commands exitosos generan Domain Events.

---

# Compatibilidad con CQRS

Los permisos se evalúan únicamente en el lado de escritura.

Las consultas no requieren autorización del Aggregate, aunque
pueden estar sujetas a políticas de acceso implementadas por
la capa de aplicación.

---

# Evolución

Nuevos roles y políticas podrán incorporarse sin modificar el
Aggregate, siempre que:

- respeten el Ubiquitous Language;
- mantengan las invariantes;
- no alteren los Commands existentes;
- preserven la compatibilidad con versiones anteriores.

---

# Definición de Éxito

El modelo de permisos del Aggregate Citizen garantiza que toda
modificación de una identidad cívica sea ejecutada únicamente
por actores autorizados, manteniendo una separación estricta
entre autenticación, autorización y reglas de negocio. Esto
preserva la independencia del dominio y facilita su integración
con distintos mecanismos de seguridad sin comprometer la
consistencia del ecosistema AURA.