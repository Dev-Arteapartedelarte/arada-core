# CORE-007 — Strategic Design

Versión: 2.0

Estado: Official

Proyecto: AURA Core

## Objetivo

Definir cómo se dividen y colaboran los Bounded Contexts de AURA Core
aplicando DDD y Hexagonal Architecture.

## Diseño estratégico

Cada Bounded Context posee:

- lenguaje y modelo propios;
- Aggregate, Repository Contract y Domain Events propios;
- lifecycle y versionado independientes;
- puertos explícitos para necesidades externas;
- libertad para evolucionar sin compartir objetos internos.

Los trece contextos oficiales se definen en
`CORE-002-Bounded-Context-Map.md`.

## Ownership y referencias

El dueño de una identidad controla su significado y lifecycle. Un
consumidor sólo mantiene el ID requerido por su propio modelo. Referenciar
un ID no autoriza a modificar, reconstruir ni validar internamente el
Aggregate dueño.

## Relaciones permitidas

- Customer/Supplier mediante API Contract o Integration Event explícito;
- Open Host Service con Published Language estable;
- Anti-Corruption Layer para modelos externos;
- Partnership sólo cuando una decisión futura documente evolución
  coordinada.

No se permiten imports de modelos internos, bases de datos compartidas
como contrato, ni navegación de grafos de objetos entre contextos.

## Consistencia

La consistencia inmediata existe dentro de un Aggregate. Entre contextos
se utiliza consistencia eventual. Un Application Service puede coordinar
un proceso, pero cada commit modifica un solo Aggregate.

## Eventos

Domain Events permanecen dentro del contexto productor. Integration
Events constituyen Published Language cross-boundary y se definen por
separado. API Contracts representan otra frontera y no son eventos.

Notification, Audit e Integration reaccionan a contratos recibidos por
inbound adapters; Application los traduce a Commands propios.

## Hexagonal Architecture

Los casos de uso son input ports. Repository Contracts y publicadores de
Integration Events son output ports. HTTP, persistencia, brokers,
Identity Providers, FIWARE y NGSI-LD son adapters reemplazables.

El dominio no decide protocolos, productos ni topología de despliegue.

## Shared Kernel

Debe permanecer mínimo y no contener Aggregates, Permissions, contratos
públicos ni conceptos específicos de un contexto.

## Evolución

CQRS físico, Event Sourcing, outbox y sagas técnicas requieren ADRs
separados. La mera existencia de Commands o Domain Events no adopta esas
arquitecturas.

## Definición de éxito

Los contextos colaboran mediante contratos deliberados, preservan su
autonomía y nunca forman una transacción distribuida accidental.
