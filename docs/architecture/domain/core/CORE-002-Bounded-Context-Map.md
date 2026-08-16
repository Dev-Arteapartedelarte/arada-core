# CORE-002 — Bounded Context Map

Versión: 2.0

Estado: Official

Proyecto: AURA Core

ADR relacionados:

- ADR-001 — Domain-Driven Design
- ADR-002 — Hexagonal Architecture
- ADR-003 — Event Boundaries

## Objetivo

Definir los trece Bounded Contexts oficiales, su ownership y la dirección
semántica de sus relaciones. Este mapa no define infraestructura.

## Contextos oficiales

| Bounded Context | Aggregate | Ownership principal |
|---|---|---|
| Organization Management | Organization | identidad, configuración, políticas y lifecycle organizacional |
| Citizen Management | Citizen | identidad cívica |
| Membership Management | Membership | relación Citizen–Organization |
| Authorization Management | Role | catálogo de funciones organizacionales |
| Territorial Management | Territory | identidad, jerarquía y lifecycle territorial |
| Assembly Management | Assembly | sesión formal de asamblea |
| Proposal Management | Proposal | propuesta y su lifecycle |
| Participation Management | Participation | instancia formal de participación |
| Voting Management | Voting | proceso de votación |
| Document Management | Document | documento y metadatos de dominio |
| Notification Management | Notification | intención y resultado de notificación |
| Audit Management | Audit | registro de auditoría bajo su propio modelo |
| Integration Management | Integration | vínculo y estado de integración externa |

## Reglas del mapa

- Una referencia por ID no transfiere ownership.
- Una dependencia de lectura no amplía la transacción del consumidor.
- Un contexto no importa Aggregates, Entities o Value Objects internos de
  otro contexto.
- Todo efecto cross-context es eventual y utiliza Integration Event o API
  Contract explícito.
- Domain Events no constituyen Published Language entre contextos.

## Relaciones explícitas

La flecha apunta desde el consumidor semántico hacia el contexto dueño de
la identidad referenciada.

```text
Membership ─────► Citizen
Membership ─────► Organization
Role ───────────► Organization
Organization ───► Territory
Assembly ───────► Organization / Territory
Proposal ───────► Organization / Territory / Assembly
Participation ─► Organization / Citizen / Membership
Participation ─► Assembly / Proposal / Voting
Voting ─────────► Organization / Assembly / Proposal
Document ───────► contexto dueño del hecho documentado
Notification ──► identidad del hecho o destinatario referenciado
Audit ──────────► identidad del hecho auditado
Integration ───► sistema externo identificado por su propio contrato
```

Las relaciones opcionales sólo existen cuando el Aggregate consumidor
mantiene explícitamente el identificador correspondiente.

## Contextos reactivos

Notification y Audit no consumen directamente Domain Events ajenos.
Reciben un Integration Event por un inbound adapter; Application valida
el contrato y ejecuta un Command propio. El nuevo Aggregate produce sus
propios Domain Events internos.

Integration Management protege el dominio mediante Anti-Corruption
Layers. Ningún modelo de FIWARE, NGSI-LD, municipio o proveedor ingresa
directamente en un Aggregate.

## Role y Permission

Role es un Aggregate organizacional. Permission no es un Bounded Context
ni un Aggregate del baseline; es una capacidad explícita vinculada a un
Command. La asignación Membership–Role se difiere hasta contar con un
Source of Truth aprobado.

## Consistencia

```text
Inside Aggregate  = Immediate Consistency
Across Aggregates = Eventual Consistency
```

Un caso de uso puede leer referencias o coordinar pasos, pero cada commit
de escritura confirma un solo Aggregate.

## Contextos retirados del baseline

Identity, Community, Requests, Workflow y Smart City no son Bounded
Contexts oficiales de AURA Core 1.0. Capacidades técnicas de identidad o
integraciones Smart City pertenecen a adapters o sistemas externos hasta
que una decisión futura defina un modelo de dominio explícito.

## Definición de éxito

Cada relación posee dueño, dirección y mecanismo explícitos sin fusionar
Aggregates ni introducir consistencia distribuida.
