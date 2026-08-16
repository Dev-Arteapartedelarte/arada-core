# CORE-004 — Ubiquitous Language

Versión: 2.0

Estado: Official

Proyecto: AURA Core

## Objetivo

Establecer el vocabulario transversal aprobado para AURA Core 1.0. Cada
Bounded Context puede especializar términos sin reutilizar modelos
internos ajenos.

## Términos estructurales

### Aggregate

Unidad de consistencia inmediata modificada exclusivamente mediante su
Aggregate Root.

### Command

Intención explícita de modificar un Aggregate. Puede ser rechazada y no es
un hecho ni una API request.

### Domain Event

Hecho inmutable y confirmado generado por un Aggregate. Permanece interno
al Bounded Context que lo produce.

### Integration Event

Contrato público, explícito y versionado para comunicar un hecho entre
Bounded Contexts o sistemas. No se deriva automáticamente de un Domain
Event.

### API Contract

Contrato síncrono o asíncrono de una interfaz pública. No expone el modelo
interno del Aggregate.

### Permission

Capacidad explícita requerida para ejecutar un Command. No es un
Aggregate, Role, Membership ni Citizen.

### Read Model

Proyección optimizada para consulta sin autoridad de escritura.

## Aggregates oficiales

### Organization

Identidad colectiva con configuración, políticas, territorio asociado y
lifecycle propio. No posee Citizens, Memberships ni Roles.

### Citizen

Identidad cívica de una persona dentro del ecosistema AURA.

### Membership

Relación formal entre un Citizen y una Organization. No concede permisos
por sí misma.

### Role

Función o cargo dentro de una Organization. Es un Aggregate de catálogo,
no un Value Object ni un conjunto de permisos.

La asignación Membership–Role no forma parte del baseline 1.0.

### Territory

Unidad territorial con identidad, jerarquía y vigencia propias.

### Assembly

Sesión formal de deliberación perteneciente a su propia frontera.

### Proposal

Propuesta formal y su evolución de negocio.

### Participation

Instancia formal de participación de un actor habilitado.

### Voting

Proceso formal de votación. `VotingId` identifica el Aggregate; Vote sólo
puede utilizarse para un concepto interno expresamente definido.

### Document

Documento de dominio y sus metadatos; no representa el storage técnico.

### Notification

Unidad de comunicación con estado de dominio. Delivered representa
entrega confirmada, no lectura ni detalle del proveedor.

### Audit

Registro de auditoría bajo un modelo propio; observar un hecho no le
transfiere ownership sobre el Aggregate origen.

### Integration

Relación controlada con un sistema externo, protegida por un
Anti-Corruption Layer.

## Términos no oficiales

Identity, Community, Requests, Workflow, Smart City y Permission
Management no son Bounded Contexts del baseline. Un mecanismo técnico de
identidad se denomina Identity Provider adapter, no dominio Identity.

## Naming

- Commands utilizan verbo imperativo: `CreateProposal`.
- Domain Events utilizan hecho pasado: `ProposalCreated`.
- Integration Events se identifican explícitamente como contrato de
  integración y mantienen su propia versión.
- Identidades utilizan el nombre del dueño: `ProposalId`.

## Definición de éxito

Cada término posee un significado único dentro de su contexto y ninguna
palabra técnica reemplaza un concepto del negocio.
