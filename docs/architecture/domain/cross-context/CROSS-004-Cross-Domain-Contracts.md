# CROSS-004 — Cross-Domain Contracts

Versión: 1.0

Estado: Consolidated

Baseline: `domain-model-v1.0.0`

## Objetivo

Inventariar los contratos públicos definidos por los documentos K sin asumir
transporte, consumidor, infraestructura o conversión automática.

## Envelope transversal

Los contratos K convergen conceptualmente en:

```text
EventId
EventType
ContractVersion
AggregateId
AggregateType
AggregateVersion
OccurredAt
CorrelationId
CausationId
MinimalPayload
```

Las diferencias de nombre como `Version`, `EventVersion` u `OccurredOn`
permanecen bajo el contrato propietario; este documento no las normaliza.

## Inventario por productor

| Productor | Contratos públicos v1 | Payload público mínimo | Consumidor aprobado |
|---|---|---|---|
| Organization | 14 contratos `Organization*IntegrationEvent` | OrganizationId, versión y datos propios del cambio | No definido |
| Citizen | 12 contratos `Citizen*IntegrationEvent` | CitizenId y dato minimizado del hecho; sin secretos | No definido |
| Membership | 9 contratos `Membership*IntegrationEvent` | MembershipId, CitizenId, OrganizationId y estado pertinente | No definido |
| Role | 6 contratos `Role*IntegrationEvent` | RoleId, OrganizationId y cambio de catálogo pertinente | No definido |
| Territory | Ninguno | No existe Published Language aprobado | No aplica |
| Assembly | 9 contratos publicados/`ForIntegration` | AssemblyId, OrganizationId, TerritoryId opcional, estado o campos cambiados | No definido |
| Proposal | 8 contratos `ForIntegration` | ProposalId, OrganizationId, referencias mínimas, estado o campos cambiados | No definido |
| Participation | 9 contratos `Participation*IntegrationEvent` | ParticipationId, OrganizationId y referencias contextuales mínimas | No definido |
| Voting | 5 contratos lifecycle `Voting*IntegrationEvent` | VotingId, OrganizationId, referencias contextuales y estado | No definido |
| Document | Ninguno | No existe Published Language aprobado | No aplica |
| Notification | 5 contratos `Notification*IntegrationEvent` | NotificationId, referencia del hecho y estado de entrega minimizado | No definido |
| Audit | AuditRecordedIntegrationEvent | AuditId y referencias mínimas al Aggregate/Event fuente | No definido |
| Integration | 5 contratos `Integration*IntegrationEvent` | IntegrationId, referencia externa y estado; nunca credenciales | No definido |

## Contratos condicionales

| Contrato | Origen permitido por el baseline | Restricción |
|---|---|---|
| AssemblyPublished | `AssemblyScheduled` | sólo cuando exista contrato explícito de interoperabilidad; `AssemblyCreated` no es origen |
| AssemblyDetailsChanged | cambios de detalles enumerados por DOMAIN-006K, incluido `AssemblyModalityChanged` | sólo cuando exista relevancia externa |
| ProposalUpdatedForIntegration | `ProposalRenamed`, `ProposalPurposeChanged`, `ProposalDescriptionChanged`, `ProposalTypeChanged`, `ProposalContentUpdated`, `ProposalTerritoryChanged`, `ProposalAssemblyAssociated` | sólo cuando exista relevancia externa y contrato explícito de interoperabilidad |

## Ausencias explícitas

- `CitizenVerificationRequested` permanece interno.
- los trece Domain Events de Territory permanecen internos.
- `AssemblyRulesUpdated` y `AssemblyExecutionConditionsUpdated` permanecen internos.
- los seis cambios de configuración/opciones de Voting permanecen internos.
- los tres Domain Events de Document permanecen internos.

La ausencia de contrato no es un error y no autoriza usar directamente el
Domain Event.

## Entrada a contextos reactivos

Notification y Audit pueden recibir contratos mediante futuros inbound
adapters, pero el baseline no aprueba una suscripción concreta. Ante una
entrada válida:

```text
External Contract
    → Contract Validation
    → Own Permission and Command
    → Notification or Audit Aggregate
    → Own Domain Event
```

El contrato recibido nunca modifica directamente el Aggregate consumidor.

## Seguridad y privacidad

- Published Language contiene sólo información necesaria;
- Aggregate completo, credenciales, tokens y secretos quedan excluidos;
- actor y datos personales se incluyen únicamente cuando el contrato lo exige;
- conocer un ID no concede Permission;
- autenticación y autorización no forman parte del payload de dominio.

## Fallos y consistencia

- sólo un hecho confirmado es elegible para publicación;
- fallo de publicación o consumo no revierte el productor;
- reintento, orden, deduplicación y transporte se decidirán en arquitectura;
- la versión contractual es independiente de AggregateVersion;
- cambios incompatibles requieren nueva versión del contrato.

## Resultado

El baseline dispone de 83 contratos públicos nombrados. Ninguno posee consumidor
técnico o mecanismo de transporte aprobado en esta fase.