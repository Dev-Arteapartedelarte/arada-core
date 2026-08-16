# AURA Core — Domain Model Closure

Versión: 1.0

Estado: Approved

Release: `domain-model-v1.0.0`

## Resultado

El Domain Model de AURA Core queda formalmente cerrado sobre trece
Bounded Contexts y trece Aggregates. La arquitectura normativa es
Hexagonal Architecture con Domain-Driven Design.

```text
Aggregate Boundary = Immediate Consistency Boundary
Cross-Aggregate Collaboration = Eventual Consistency
```

```text
Domain Event != Integration Event != API Contract
```

## Baseline consolidado

| # | Bounded Context | Aggregate | Documentos | Estado |
|---:|---|---|---:|---|
| 001 | Organization Management | Organization | 17/17 | Closed |
| 002 | Citizen Management | Citizen | 17/17 | Closed |
| 003 | Membership Management | Membership | 17/17 | Closed |
| 004 | Authorization Management | Role | 17/17 | Closed |
| 005 | Territorial Management | Territory | 17/17 | Closed |
| 006 | Assembly Management | Assembly | 17/17 | Closed |
| 007 | Proposal Management | Proposal | 17/17 | Closed |
| 008 | Participation Management | Participation | 17/17 | Closed |
| 009 | Voting Management | Voting | 17/17 | Closed |
| 010 | Document Management | Document | 17/17 | Closed |
| 011 | Notification Management | Notification | 17/17 | Closed |
| 012 | Audit Management | Audit | 17/17 | Closed |
| 013 | Integration Management | Integration | 17/17 | Closed |

La secuencia obligatoria por Aggregate contiene el documento raíz y los
contratos A–P: Lifecycle, State Machine, Commands, Domain Events,
Invariants, Permissions, Repository Contract, Examples, Versioning,
Consistency Boundary, Integration Events, Read Model, Test Scenarios,
Performance Rules, Security Model y Extension Points.

## Arquitectura ratificada

### DDD

- una Aggregate Root y un Repository Contract por Aggregate;
- ownership, identidad, lifecycle y versión propios;
- referencias externas sólo mediante IDs;
- una transacción de escritura confirma un Aggregate;
- los Read Models no poseen autoridad de escritura;
- colaboración cross-context eventualmente consistente.

### Hexagonal Architecture

- Domain contiene el modelo y sus contratos internos;
- Application expone input ports y usa output ports;
- inbound adapters traducen transporte a casos de uso;
- outbound adapters implementan persistencia, publicación e integración;
- todas las dependencias apuntan hacia Domain/Application;
- frameworks y proveedores no forman parte del modelo.

## Resolución de inconsistencias

### DM-001 — Scope de Domain Events: Resolved

Los Domain Events permanecen dentro del Bounded Context productor. Un
efecto cross-boundary requiere Integration Event o API Contract explícito.
No existe conversión automática.

### DM-002 — Creación y publicación: Resolved

El Aggregate genera y registra Domain Events. Application coordina su
publicación interna después de persistir exitosamente. Los adapters
implementan cualquier transporte.

### DM-003 — Transacciones multi-Aggregate: Resolved

Un caso de uso puede coordinar varios Aggregates, pero cada commit modifica
uno. Los procesos posteriores usan consistencia eventual; no se define una
transacción distribuida.

### DM-004 — Role y Permission: Resolved

Role es un Aggregate de catálogo organizacional, no un Value Object ni un
contenedor de permisos. Permission es una capacidad explícita vinculada a
un Command y no constituye un Aggregate. Role, Membership y Citizen no
conceden autorización implícita.

La asignación Membership–Role queda fuera del baseline 1.0 hasta definir
un Source of Truth, Commands, Events y consistency boundary propios.

### DM-005 — Context Map: Resolved

CORE-002 contiene los trece contextos declarados. Identity, Community,
Requests, Workflow y Smart City no son Bounded Contexts de este baseline.
Los servicios técnicos correspondientes son adapters o sistemas externos.

### DM-006 — Dependencias: Resolved

La Constitución, Package Architecture y Dependency Rules expresan puertos
y adapters. Domain nunca depende de Infrastructure o Interfaces.

### DM-007 — Secuencia y referencias: Resolved

Se crearon `DOMAIN-001H-Examples.md` y
`DOMAIN-011B-State-Machine.md`. Las referencias CORE históricas de Role se
reemplazaron por contratos normativos existentes. ADR-001, ADR-002 y
ADR-003 documentan las decisiones vigentes.

### DM-008 — Organization 2.0: Resolved

Organization conserva validación, lifecycle, dirección, marca, políticas,
configuración y territorio. Membership y Representative fueron retirados
de su ownership, Commands, Events, Permissions, Integration Events,
Examples y pruebas.

## Contratos transversales

### Permission → Command → Aggregate

Cada documento F define Permissions explícitas para Commands del mismo
Aggregate. Application decide autorización; el Aggregate protege estado e
invariantes.

### Domain Event → Integration Event

Los documentos D son internos. Los documentos K son contratos públicos
versionados de manera independiente. Notification y Audit reciben
contratos mediante inbound adapters y ejecutan Commands propios.

### Write Model → Read Model

El Write Model es la Source of Truth del Aggregate. Los documentos L
describen proyecciones eventualmente consistentes que no ejecutan Commands.

## Versionado y evidencia

`domain-model-baseline.json` utiliza schema 2 y registra por documento:

- versión documental;
- hash SHA-256;
- Aggregate y Bounded Context dueño.

El release se identifica mediante el tag anotado local
`domain-model-v1.0.0`. El tag no implica publicación remota.

Event Sourcing y CQRS físico permanecen compatibles, pero no obligatorios.
Outbox, broker, persistencia, APIs, FIWARE, NGSI-LD y seguridad técnica
requieren decisiones arquitectónicas posteriores.

## Criterios de aceptación

- 13 Aggregates y 221 documentos de Aggregate;
- secuencia raíz + A–P completa;
- referencias DOMAIN, CORE y ADR resolubles;
- manifiesto y hashes coherentes;
- copia de este informe en la raíz idéntica al documento canónico;
- validador con `0 errors, 0 warnings`;
- pruebas automatizadas exitosas;
- commit y tag local exclusivos del cierre.

## Definición de éxito

AURA Core dispone de un Domain Model versionado, con ownership y
consistencia explícitos, lenguaje ubicuo estable y fronteras que permiten
construir Application e Infrastructure mediante puertos y adapters sin
redefinir el dominio.
