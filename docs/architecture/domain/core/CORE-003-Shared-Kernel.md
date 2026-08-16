# CORE-003 — Shared Kernel

Versión: 2.0

Estado: Official

Proyecto: AURA Core

## Objetivo

Definir el conjunto mínimo de conceptos cuyo significado es idéntico en
los trece Bounded Contexts.

## Contenido permitido

- Identifier y tipos base de identidad;
- Timestamp e Interval;
- AggregateVersion;
- EventId, CorrelationId y CausationId;
- DomainEvent como contrato base interno;
- Result y errores base sin semántica específica;
- primitivas geográficas sin ownership territorial;
- utilidades puras de validación compartida.

## Contenido prohibido

No pertenecen al Shared Kernel:

- Organization, Citizen, Membership, Role o cualquier Aggregate;
- estados, Commands, Permissions o políticas de un contexto;
- Domain Events concretos;
- Integration Events o API Contracts;
- DTO, ORM entities, mensajes de broker o modelos externos;
- conceptos históricos Identity, Community, Requests, Workflow o Smart
  City.

## Identidades

Cada ID concreto pertenece al lenguaje del contexto que posee la entidad.
Compartir la abstracción `Identifier` no autoriza a un contexto a construir
o interpretar identidades ajenas fuera de sus contratos públicos.

## Eventos

El Shared Kernel puede definir la forma base de un Domain Event, pero no
su payload ni sus consumidores. Integration Events utilizan Published
Languages separados y no heredan automáticamente el contrato interno.

## Evolución

Todo cambio requiere acuerdo de todos los contextos consumidores y debe
mantener compatibilidad. Ante significados distintos se crean conceptos
locales, no una abstracción compartida artificial.

## Regla de dependencia

El Shared Kernel no depende de Domain, Application, adapters, frameworks
ni Bounded Contexts. Los contextos pueden depender de él de manera
unidireccional.

## Definición de éxito

El Shared Kernel permanece pequeño, estable, tecnológicamente neutro y
libre de ownership de negocio.
