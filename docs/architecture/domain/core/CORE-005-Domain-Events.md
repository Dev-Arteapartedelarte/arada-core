# CORE-005 — Domain Events

Versión: 2.0

Estado: Official

Proyecto: AURA Core

ADR relacionados:

- ADR-001 — Domain-Driven Design
- ADR-002 — Hexagonal Architecture
- ADR-003 — Event Boundaries

## Objetivo

Definir el contrato normativo de Domain Events y su límite respecto de
Integration Events y transporte.

## Definición

Un Domain Event es un hecho significativo, inmutable y confirmado,
generado por una única instancia de Aggregate dentro de su Bounded
Context.

No representa intención, fallo técnico, request, mensaje de broker ni
contrato público.

## Responsabilidades

El Aggregate:

1. valida el Command y sus invariantes;
2. modifica exclusivamente su propio estado;
3. incrementa AggregateVersion cuando corresponde;
4. crea y registra los Domain Events resultantes.

El Aggregate nunca transporta ni publica técnicamente eventos.

Application:

1. carga el Aggregate mediante Repository Contract;
2. ejecuta el comportamiento;
3. persiste el nuevo estado;
4. obtiene los eventos pendientes;
5. coordina su publicación interna después del commit.

Un fallo de persistencia impide tratar el evento como confirmado.

## Envelope conceptual

Todo Domain Event contiene como mínimo:

- EventId;
- EventName;
- AggregateId;
- AggregateType;
- AggregateVersion;
- OccurredAt;
- CorrelationId cuando exista una cadena causal;
- CausationId cuando exista una causa identificable;
- payload mínimo del hecho.

`AggregateVersion` no es `EventContractVersion`.

## Scope y consumidores

Un Domain Event permanece dentro del Bounded Context productor. Puede
alimentar handlers internos y proyecciones propias sin otorgarles
capacidad de modificar el Aggregate directamente.

Otro Bounded Context no consume este contrato interno. Para cruzar la
frontera se define uno de estos contratos:

```text
Integration Event
API Contract
```

La existencia de un Domain Event no obliga a exponerlo, copiar su payload
ni crear un Integration Event.

## Domain Event versus Integration Event

| Aspecto | Domain Event | Integration Event |
|---|---|---|
| Owner | Aggregate/Bounded Context | contrato de integración |
| Scope | interno | cross-boundary |
| Payload | lenguaje interno mínimo | Published Language estable |
| Momento | junto al cambio confirmado | después del commit |
| Transporte | ninguno | responsabilidad de adapters |
| Versionado | AggregateVersion y contrato interno | versión pública propia |

## Entrega e infraestructura

Outbox, broker, retries, deduplicación y orden de entrega son decisiones
de arquitectura. Pueden implementar confiabilidad, pero no forman parte
del Domain Event ni convierten Event Sourcing en obligatorio.

## Replay

Si una arquitectura futura adopta Event Sourcing, reproducir eventos no
genera nuevos hechos ni efectos externos. Sin esa decisión, los Domain
Events no son automáticamente la Source of Truth del Aggregate.

## Reglas obligatorias

- hechos en pasado;
- inmutables;
- un productor Aggregate explícito;
- sin comportamiento ni dependencias técnicas;
- sin consumidores cross-context directos;
- sin publicación antes del commit;
- sin conversión automática a contrato público.

## Definición de éxito

Los Domain Events expresan hechos internos verificables sin acoplar el
dominio a transporte, persistencia o modelos de otros contextos.
