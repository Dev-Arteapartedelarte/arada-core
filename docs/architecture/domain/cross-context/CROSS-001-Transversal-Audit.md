# CROSS-001 — AURA Core Transversal Audit

Versión: 1.0

Estado: Consolidated

Baseline auditado: `domain-model-v1.0.0`

## Objetivo

Registrar la revisión horizontal de los trece Aggregates sin modificar sus
reglas normativas ni resolver ambigüedades por inferencia.

## Cobertura

| # | Bounded Context | Aggregate | Raíz + A–P | Resultado estructural |
|---:|---|---|---:|---|
| 001 | Organization Management | Organization | 17/17 | Conforme |
| 002 | Citizen Management | Citizen | 17/17 | Conforme |
| 003 | Membership Management | Membership | 17/17 | Conforme |
| 004 | Authorization Management | Role | 17/17 | Conforme |
| 005 | Territorial Management | Territory | 17/17 | Conforme |
| 006 | Assembly Management | Assembly | 17/17 | Conforme |
| 007 | Proposal Management | Proposal | 17/17 | Conforme |
| 008 | Participation Management | Participation | 17/17 | Conforme |
| 009 | Voting Management | Voting | 17/17 | Conforme |
| 010 | Document Management | Document | 17/17 | Conforme |
| 011 | Notification Management | Notification | 17/17 | Conforme |
| 012 | Audit Management | Audit | 17/17 | Conforme |
| 013 | Integration Management | Integration | 17/17 | Conforme |

## Reglas transversales confirmadas

- cada Aggregate Root es su propio límite de consistencia inmediata;
- las referencias externas utilizan IDs y no transfieren ownership;
- una escritura confirma un Aggregate;
- la colaboración cross-Aggregate es eventualmente consistente;
- Domain Event, Integration Event y API Contract son contratos distintos;
- Application autoriza y coordina, pero no redefine dominio;
- Read Models carecen de autoridad de escritura;
- Event Sourcing y CQRS físico no son obligatorios.

## Resoluciones ya consolidadas

| ID | Tema | Resolución del baseline |
|---|---|---|
| DM-001 | Scope de Domain Events | Permanecen dentro del contexto productor |
| DM-002 | Publicación | Application coordina después del commit |
| DM-003 | Escritura múltiple | No existe transacción distribuida |
| DM-004 | Role y Permission | Permission es capacidad, no Aggregate |
| DM-005 | Context Map | Existen trece contextos oficiales |
| DM-006 | Dependencias | Todas apuntan hacia Domain/Application |
| DM-007 | Secuencia documental | Raíz + A–P completa |
| DM-008 | Organization ownership | Membership permanece fuera de Organization |

## Hallazgos abiertos

| ID | Severidad | Hallazgo | Tratamiento |
|---|---|---|---|
| TA-001 | Alta | `AssemblyPublished` puede relacionarse con una Assembly creada o programada, sin seleccionar un Domain Event origen único | No mapear automáticamente; requiere decisión futura |
| TA-002 | Media | `ProposalUpdatedForIntegration` agrupa cambios relevantes sin enumerar un conjunto cerrado de Domain Events origen | Mantener como contrato condicional; requiere selección explícita |
| TA-003 | Informativa | Territory no declara Integration Events oficiales en v1 | Registrar ausencia; no inventar contratos |
| TA-004 | Informativa | Document no declara Integration Events oficiales en v1 | Registrar ausencia; no inventar contratos |
| TA-005 | Media | Los contratos K usan convenciones de nombre distintas: `IntegrationEvent`, `ForIntegration` y nombres publicados | Preservar nombres oficiales; no normalizar sin versionado |
| TA-006 | Media | Varios documentos K mencionan consumidores posibles, no consumidores contractualmente aprobados | Catálogo registra consumidor como no definido |
| TA-007 | Informativa | Los artefactos horizontales y diagramas estaban vacíos al cerrar v1 | Se completan fuera de los 221 documentos normativos |

## Integridad de referencias

El validador confirma:

- secuencia completa por Aggregate;
- hashes del manifest coherentes;
- referencias DOMAIN, CORE y ADR resolubles;
- copia de cierre raíz y canónica equivalentes;
- ausencia de reglas históricas prohibidas.

## Límites del audit

Este documento no:

- modifica Commands, Events, Invariants o Permissions;
- selecciona tecnología;
- define consumidores nuevos;
- convierte eventos internos en públicos;
- corrige los hallazgos TA-001 a TA-006;
- altera el tag o el manifest v1.

## Resultado

El baseline es estructuralmente completo y apto para consolidación horizontal.
Las ambigüedades semánticas identificadas permanecen visibles y no bloquean la
descripción fiel del modelo existente.
