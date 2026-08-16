# DOMAIN-001K — Organization Integration Events

Versión: 2.0

Estado: Official

Proyecto: AURA Core

Bounded Context: Organization Management

Aggregate: Organization

## Contratos públicos 1.0

- OrganizationCreatedIntegrationEvent
- OrganizationSubmittedForValidationIntegrationEvent
- OrganizationApprovedIntegrationEvent
- OrganizationRejectedIntegrationEvent
- OrganizationSuspendedIntegrationEvent
- OrganizationReactivatedIntegrationEvent
- OrganizationArchivedIntegrationEvent
- OrganizationDeletedIntegrationEvent
- OrganizationRenamedIntegrationEvent
- OrganizationAddressChangedIntegrationEvent
- OrganizationPoliciesChangedIntegrationEvent
- OrganizationSettingsChangedIntegrationEvent
- OrganizationBrandChangedIntegrationEvent
- OrganizationTerritoryChangedIntegrationEvent

## Reglas

Cada contrato se selecciona explícitamente después del commit, posee
EventId y EventContractVersion propios y expone sólo Published Language.
No hereda automáticamente todo el payload del Domain Event.

Application usa un output port para publicarlo; broker, outbox, retries y
deduplicación pertenecen a adapters/arquitectura.

No existen eventos de integración de membresía o representante bajo
Organization Management.
