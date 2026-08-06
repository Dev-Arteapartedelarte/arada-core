# DOMAIN-003F — Membership Permissions

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
- DOMAIN-003C-Commands.md
- DOMAIN-003E-Invariants.md
- DOMAIN-004-Aggregate.md (Role)
- DOMAIN-005-Aggregate.md (Permission)
- CORE-007-Strategic-Design.md

---

# Objetivo

Este documento define el modelo de autorización del Aggregate
**Membership**.

Las reglas aquí descritas determinan **quién puede ejecutar
cada Command** del Aggregate.

El Aggregate **no implementa autenticación** ni administra
usuarios o sesiones.

Su única responsabilidad consiste en exigir que la operación
haya sido autorizada por la capa de aplicación.

---

# Principios

El modelo de permisos sigue los siguientes principios:

- mínimo privilegio;
- separación de responsabilidades;
- autorización previa;
- independencia de la infraestructura;
- políticas explícitas;
- trazabilidad completa.

---

# Alcance

Este documento define permisos sobre:

- creación;
- incorporación;
- aprobación;
- suspensión;
- reactivación;
- finalización;
- archivado.

No define permisos para otros Aggregates.

---

# Modelo Conceptual

La autorización sigue la siguiente cadena conceptual:

```text
Identity

↓

Citizen

↓

Membership

↓

Role

↓

Permission

↓

Command
```

La autenticación identifica al actor.

La autorización determina si dicho actor puede ejecutar el
Command solicitado.

---

# Actores del Dominio

Conceptualmente pueden existir los siguientes actores:

```text
Citizen

Organization Administrator

Board Member

Secretary

Moderator

System Administrator

Automation Process
```

El catálogo definitivo de Roles será definido por el Aggregate
**Role**.

---

# Matriz de Permisos

| Command | Citizen | Organization Administrator | Board Member | Secretary | System Administrator | Automation |
|----------|----------|----------------------------|--------------|-----------|----------------------|------------|
| CreateMembership | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| RequestMembership | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| ApproveMembership | ✖ | ✔ | ✔ | ✖ | ✔ | ✔* |
| RejectMembership | ✖ | ✔ | ✔ | ✖ | ✔ | ✔* |
| ActivateMembership | ✖ | ✔ | ✔ | ✔ | ✔ | ✔ |
| SuspendMembership | ✖ | ✔ | ✔ | ✖ | ✔ | ✔ |
| ReactivateMembership | ✖ | ✔ | ✔ | ✖ | ✔ | ✔ |
| TerminateMembership | ✖ | ✔ | ✔ | ✖ | ✔ | ✔ |
| ArchiveMembership | ✖ | ✔ | ✖ | ✖ | ✔ | ✔ |

\* Sólo cuando exista una política explícita de aprobación automática.

---

# Reglas por Command

## CreateMembership

Puede ejecutarlo:

- el propio Citizen (autoinscripción, cuando esté habilitada);
- un administrador de la organización;
- un proceso automatizado autorizado.

---

## RequestMembership

Puede ejecutarlo:

- el Citizen;
- un representante autorizado de la Organization;
- un proceso de integración.

---

## ApproveMembership

Puede ejecutarlo únicamente un actor con facultades para admitir
nuevos miembros.

Ejemplos:

- Organization Administrator;
- Board Member;
- proceso automático configurado.

---

## RejectMembership

Las mismas reglas que `ApproveMembership`.

La decisión debe quedar registrada mediante un Domain Event.

---

## ActivateMembership

La activación sólo puede realizarse una vez aprobada la
solicitud.

Puede ser ejecutada por:

- Organization Administrator;
- Board Member;
- Secretary (si la política organizacional lo permite);
- proceso automático autorizado.

---

## SuspendMembership

La suspensión requiere privilegios administrativos.

Debe quedar registrada la causa de la suspensión.

---

## ReactivateMembership

Sólo un actor autorizado puede devolver una Membership al
estado **Active**.

Debe existir una Membership previamente suspendida.

---

## TerminateMembership

La finalización puede producirse por:

- renuncia;
- expulsión;
- pérdida de requisitos;
- disolución de la Organization;
- otras causas definidas por la política institucional.

Debe ejecutarla un actor autorizado o un proceso automático
legítimo.

---

## ArchiveMembership

El archivado representa el cierre definitivo del ciclo de vida.

Sólo puede ser ejecutado por:

- Organization Administrator;
- System Administrator;
- procesos automáticos de retención documental.

---

# Delegación

Las organizaciones podrán definir políticas de delegación.

Ejemplos:

```text
Board Member

↓

Secretary
```

o

```text
Organization Administrator

↓

Regional Administrator
```

La delegación será administrada por el Aggregate **Role** y las
políticas de autorización, nunca por Membership.

---

# Autorización Basada en Roles

Membership no conoce nombres concretos de Roles.

Conceptualmente requiere permisos como:

```text
membership.create

membership.request

membership.approve

membership.reject

membership.activate

membership.suspend

membership.reactivate

membership.terminate

membership.archive
```

La asignación de estos permisos a Roles pertenece al Aggregate
**Permission**.

---

# Autorización Basada en Políticas

Además de los Roles, pueden existir políticas adicionales.

Ejemplos:

- antigüedad mínima para aprobar miembros;
- quórum de aprobación;
- aprobación por múltiples revisores;
- aprobación automática bajo determinadas condiciones;
- restricciones territoriales.

Estas políticas son evaluadas antes de invocar el Aggregate.

---

# Auditoría

Toda autorización concedida o denegada debe poder registrarse.

Información mínima:

```text
ActorId

MembershipId

Command

Decision

Timestamp
```

La auditoría pertenece al Bounded Context **Audit**.

---

# Consistencia

La autorización siempre se valida antes de ejecutar un Command.

Si la validación falla:

- no cambia el estado;
- no aumenta la versión;
- no se generan Domain Events.

---

# Integración

El Aggregate puede integrarse con:

- Identity Provider;
- IAM corporativo;
- Keycloak;
- FIWARE Keyrock;
- OAuth2/OpenID Connect;
- otros proveedores compatibles.

La autenticación y autorización permanecen fuera del Aggregate.

---

# Compatibilidad con CQRS

Las reglas de autorización se aplican únicamente sobre el lado
de escritura.

Las consultas pueden aplicar filtros de acceso, pero nunca
modifican el estado del Aggregate.

---

# Compatibilidad con Event Sourcing

Los permisos no forman parte del historial de eventos.

Los Domain Events reflejan únicamente hechos de negocio ya
autorizados.

---

# Principios Arquitectónicos

Este modelo sigue:

- Domain-Driven Design (DDD);
- Role-Based Access Control (RBAC);
- Policy-Based Authorization (PBAC);
- Principle of Least Privilege;
- Clean Architecture;
- CQRS.

---

# Definición de Éxito

El modelo de permisos del Aggregate **Membership** garantiza
que toda modificación sobre la relación entre un **Citizen** y
una **Organization** sea ejecutada únicamente por actores o
procesos autorizados. La autorización permanece desacoplada del
modelo de dominio, permitiendo integrar AURA con distintos
proveedores de identidad y mecanismos de control de acceso sin
comprometer la integridad del Aggregate.