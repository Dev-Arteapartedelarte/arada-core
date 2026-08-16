# DOMAIN-001J — Organization Consistency Boundary

Versión: 2.0

Estado: Official

Proyecto: AURA Core

Bounded Context: Organization Management

Aggregate: Organization

## Dentro del boundary

Identidad, estado, nombre, tipo, dirección, marca, configuración,
políticas, TerritoryId, timestamps, AggregateVersion y Domain Events
pendientes de una única Organization.

## Fuera del boundary

Citizen, Membership, Role, Representative, Territory como objeto,
Assembly, Proposal, Participation, Voting, Document, Notification, Audit,
Integration, Read Models y adapters.

## Regla transaccional

Un Command y `save` confirman una sola Organization. No existe Unit of
Work cross-Aggregate. Las referencias externas se validan antes del
Command o mediante procesos posteriores sin incorporar su estado.

Los efectos cross-boundary usan Integration Events y consistencia
eventual. Un fallo de consumidor no revierte la Organization confirmada.
