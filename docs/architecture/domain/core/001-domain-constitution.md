# CORE-001 — Domain Constitution

Versión: 2.0

Estado: Ratificado

Proyecto: AURA Core

ADR relacionados:

- ADR-001 — Domain-Driven Design
- ADR-002 — Hexagonal Architecture
- ADR-003 — Event Boundaries

## Propósito

AURA Core modela el dominio de organizaciones y participación
ciudadana. El dominio es el centro de la arquitectura y permanece
independiente de transporte, persistencia, frameworks y proveedores.

## Principios obligatorios

1. Cada Bounded Context posee su modelo, lenguaje y contratos.
2. Cada Aggregate protege una única frontera de consistencia inmediata.
3. Una transacción de escritura confirma un solo Aggregate.
4. Las referencias entre Aggregates utilizan identidades, nunca objetos.
5. La colaboración entre Bounded Contexts es explícita y eventualmente
   consistente.
6. Los Read Models son proyecciones y nunca Sources of Truth de escritura.
7. Event Sourcing y CQRS físico son compatibles, pero no obligatorios.

## Arquitectura hexagonal

```text
Inbound Adapter
      │
      ▼
Application Input Port / Use Case
      │
      ▼
Domain
      │
      ▼
Application or Domain Output Port
      │
      ▼
Outbound Adapter
```

Las dependencias de código apuntan hacia Domain y Application. Los
adaptadores implementan o invocan puertos; el núcleo nunca depende de
adaptadores.

### Domain

Contiene:

- Aggregates, Entities y Value Objects;
- Domain Services e invariantes;
- Commands como intención del dominio;
- Domain Events como hechos internos confirmados;
- Repository Contracts requeridos por el modelo de escritura.

No contiene HTTP, SQL, ORM, brokers, DTO de transporte ni SDK externos.

### Application

Contiene casos de uso y puertos de entrada, coordina autorización,
carga un Aggregate, ejecuta un Command, persiste por un puerto de salida
y publica los Domain Events pendientes después del commit.

Puede coordinar procesos que involucren varios Aggregates, pero no crea
una transacción distribuida entre ellos.

### Adapters

Los inbound adapters traducen REST, GraphQL, CLI, mensajes u otros
mecanismos hacia casos de uso. Los outbound adapters implementan
persistencia, publicación, identidad técnica e integraciones externas.

## Bounded Contexts oficiales

El baseline 1.0 reconoce exclusivamente:

1. Organization Management
2. Citizen Management
3. Membership Management
4. Authorization Management
5. Territorial Management
6. Assembly Management
7. Proposal Management
8. Participation Management
9. Voting Management
10. Document Management
11. Notification Management
12. Audit Management
13. Integration Management

Cada contexto contiene un Aggregate oficial del mismo catálogo. Esta
correspondencia no convierte el conjunto en un único Aggregate.

## Ownership

- Organization posee su identidad, configuración, políticas, territorio
  asociado y lifecycle.
- Citizen posee la identidad cívica.
- Membership posee la relación Citizen–Organization.
- Role posee el catálogo de funciones organizacionales.
- Los demás Aggregates poseen exclusivamente su estado y lifecycle.
- Ningún Aggregate Permission forma parte del baseline.

Permission es una capacidad explícita requerida para ejecutar un Command.
Role, Membership y Citizen pueden aportar contexto a una decisión de
autorización, pero nunca conceden permisos implícitamente.

La asignación Membership–Role no posee Source of Truth en la versión 1.0
y no debe inferirse desde ninguno de los dos Aggregates.

## Eventos y contratos

```text
Domain Event != Integration Event != API Contract
```

El Aggregate genera y registra Domain Events. Application los obtiene y
coordina su publicación interna después de persistir exitosamente.

Un Domain Event permanece dentro de su Bounded Context. Cuando un hecho
debe cruzar una frontera se define, versiona y publica un Integration
Event independiente o se expone un API Contract explícito. La conversión
nunca es automática.

## Consistencia y persistencia

El Repository Contract pertenece al núcleo y opera sobre el Aggregate
completo. Su implementación es un outbound adapter.

La consistencia inmediata termina en el Aggregate. Las referencias
externas, proyecciones, notificaciones, auditoría e integración se
coordinan con consistencia eventual.

## Regla de evolución

Toda evolución debe actualizar conjuntamente los contratos A–P afectados,
el Context Map, el lenguaje ubicuo y el manifiesto del Domain Model. Una
capacidad ausente no puede agregarse por analogía o decisión técnica.

## Definición de éxito

AURA Core mantiene un dominio autónomo, consistente y verificable,
rodeado por puertos y adaptadores reemplazables, con ownership explícito
y colaboración cross-boundary mediante contratos deliberados.
