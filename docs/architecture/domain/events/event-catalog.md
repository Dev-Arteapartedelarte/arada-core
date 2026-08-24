# AURA Core — Transversal Event Catalog

Versión: 1.0

Estado: Consolidated

Baseline: `domain-model-v1.0.0`

## Convenciones

- cada fila representa una relación oficial Command → Domain Event;
- `—` significa que no existe Integration Event oficial para ese hecho;
- un contrato público sólo aparece cuando está definido en el documento K;
- `condicional` exige selección explícita después del commit;
- el catálogo no convierte eventos automáticamente ni aprueba consumidores.
- `Domain Event != Integration Event`: un contrato K sólo existe cuando el modelo normativo lo declara explícitamente.

## DOMAIN-001 — Organization

| Command | Domain Event | Integration Event |
|---|---|---|
| CreateOrganization | OrganizationCreated | OrganizationCreatedIntegrationEvent |
| SubmitOrganizationForValidation | OrganizationSubmittedForValidation | OrganizationSubmittedForValidationIntegrationEvent |
| ApproveOrganization | OrganizationApproved | OrganizationApprovedIntegrationEvent |
| RejectOrganization | OrganizationRejected | OrganizationRejectedIntegrationEvent |
| SuspendOrganization | OrganizationSuspended | OrganizationSuspendedIntegrationEvent |
| ReactivateOrganization | OrganizationReactivated | OrganizationReactivatedIntegrationEvent |
| ArchiveOrganization | OrganizationArchived | OrganizationArchivedIntegrationEvent |
| DeleteOrganization | OrganizationDeleted | OrganizationDeletedIntegrationEvent |
| RenameOrganization | OrganizationRenamed | OrganizationRenamedIntegrationEvent |
| ChangeOrganizationAddress | OrganizationAddressChanged | OrganizationAddressChangedIntegrationEvent |
| ChangeOrganizationPolicies | OrganizationPoliciesChanged | OrganizationPoliciesChangedIntegrationEvent |
| ChangeOrganizationSettings | OrganizationSettingsChanged | OrganizationSettingsChangedIntegrationEvent |
| ChangeOrganizationBrand | OrganizationBrandChanged | OrganizationBrandChangedIntegrationEvent |
| ChangeTerritory | OrganizationTerritoryChanged | OrganizationTerritoryChangedIntegrationEvent |

## DOMAIN-002 — Citizen

| Command | Domain Event | Integration Event |
|---|---|---|
| RegisterCitizen | CitizenRegistered | CitizenRegisteredIntegrationEvent |
| RequestCitizenVerification | CitizenVerificationRequested | — |
| VerifyCitizen | CitizenVerified | CitizenVerifiedIntegrationEvent |
| ActivateCitizen | CitizenActivated | CitizenActivatedIntegrationEvent |
| SuspendCitizen | CitizenSuspended | CitizenSuspendedIntegrationEvent |
| ReactivateCitizen | CitizenReactivated | CitizenReactivatedIntegrationEvent |
| DeactivateCitizen | CitizenDeactivated | CitizenDeactivatedIntegrationEvent |
| ArchiveCitizen | CitizenArchived | CitizenArchivedIntegrationEvent |
| UpdateCitizenProfile | CitizenProfileUpdated | CitizenProfileUpdatedIntegrationEvent |
| UpdateCitizenContactInformation | CitizenContactInformationUpdated | CitizenContactInformationUpdatedIntegrationEvent |
| UpdateCitizenAddress | CitizenAddressUpdated | CitizenAddressUpdatedIntegrationEvent |
| ChangePreferredLanguage | CitizenLanguageChanged | CitizenLanguageChangedIntegrationEvent |
| WithdrawConsent | CitizenConsentWithdrawn | CitizenConsentWithdrawnIntegrationEvent |

## DOMAIN-003 — Membership

| Command | Domain Event | Integration Event |
|---|---|---|
| CreateMembership | MembershipCreated | MembershipCreatedIntegrationEvent |
| RequestMembership | MembershipRequested | MembershipRequestedIntegrationEvent |
| ApproveMembership | MembershipApproved | MembershipApprovedIntegrationEvent |
| RejectMembership | MembershipRejected | MembershipRejectedIntegrationEvent |
| ActivateMembership | MembershipActivated | MembershipActivatedIntegrationEvent |
| SuspendMembership | MembershipSuspended | MembershipSuspendedIntegrationEvent |
| ReactivateMembership | MembershipReactivated | MembershipReactivatedIntegrationEvent |
| TerminateMembership | MembershipTerminated | MembershipTerminatedIntegrationEvent |
| ArchiveMembership | MembershipArchived | MembershipArchivedIntegrationEvent |

## DOMAIN-004 — Role

| Command | Domain Event | Integration Event |
|---|---|---|
| CreateRole | RoleCreated | RoleCreatedIntegrationEvent |
| RenameRole | RoleRenamed | RoleRenamedIntegrationEvent |
| ChangeDescription | RoleDescriptionChanged | RoleDescriptionChangedIntegrationEvent |
| ActivateRole | RoleActivated | RoleActivatedIntegrationEvent |
| DeactivateRole | RoleDeactivated | RoleDeactivatedIntegrationEvent |
| ArchiveRole | RoleArchived | RoleArchivedIntegrationEvent |

## DOMAIN-005 — Territory

| Command | Domain Event | Integration Event |
|---|---|---|
| CreateTerritory | TerritoryCreated | — |
| RequestTerritoryValidation | TerritoryValidationRequested | — |
| ApproveTerritory | TerritoryValidated | — |
| RejectTerritory | TerritoryValidationRejected | — |
| RenameTerritory | TerritoryRenamed | — |
| ChangeTerritoryType | TerritoryTypeChanged | — |
| ChangeAdministrativeCode | AdministrativeCodeChanged | — |
| ChangeGeometry | TerritoryGeometryChanged | — |
| ChangeParentTerritory | TerritoryParentChanged | — |
| UpdateTerritoryMetadata | TerritoryMetadataUpdated | — |
| DeactivateTerritory | TerritoryDeactivated | — |
| ActivateTerritory | TerritoryActivated | — |
| ArchiveTerritory | TerritoryArchived | — |

## DOMAIN-006 — Assembly

`AssemblyPublished` tiene como único Domain Event de origen semántico
`AssemblyScheduled`; su publicación permanece condicionada al contrato explícito correspondiente.

| Command | Domain Event | Integration Event |
|---|---|---|
| CreateAssembly | AssemblyCreated | — |
| ScheduleAssembly | AssemblyScheduled | AssemblyPublished, condicional |
| RescheduleAssembly | AssemblyRescheduled | AssemblyRescheduledForIntegration |
| ConvokeAssembly | AssemblyConvoked | AssemblyConvocationPublished |
| RenameAssembly | AssemblyRenamed | AssemblyDetailsChanged, condicional |
| ChangeAssemblyType | AssemblyTypeChanged | AssemblyDetailsChanged, condicional |
| ChangeAssemblyPurpose | AssemblyPurposeChanged | AssemblyDetailsChanged, condicional |
| ChangeAssemblyDescription | AssemblyDescriptionChanged | AssemblyDetailsChanged, condicional |
| ChangeAssemblyModality | AssemblyModalityChanged | AssemblyDetailsChanged, condicional |
| ChangeAssemblyLocation | AssemblyLocationChanged | AssemblyDetailsChanged, condicional |
| UpdateAssemblyConvocation | AssemblyConvocationUpdated | AssemblyConvocationUpdatedForIntegration |
| UpdateAssemblyRules | AssemblyRulesUpdated | — |
| UpdateAssemblyExecutionConditions | AssemblyExecutionConditionsUpdated | — |
| StartAssembly | AssemblyStarted | AssemblyStartedForIntegration |
| CompleteAssembly | AssemblyCompleted | AssemblyCompletedForIntegration |
| CancelAssembly | AssemblyCancelled | AssemblyCancelledForIntegration |
| ArchiveAssembly | AssemblyArchived | AssemblyArchivedForIntegration |

## DOMAIN-007 — Proposal

| Command | Domain Event | Integration Event |
|---|---|---|
| CreateProposal | ProposalCreated | ProposalCreatedForIntegration |
| RenameProposal | ProposalRenamed | ProposalUpdatedForIntegration, condicional |
| ChangeProposalPurpose | ProposalPurposeChanged | ProposalUpdatedForIntegration, condicional |
| ChangeProposalDescription | ProposalDescriptionChanged | ProposalUpdatedForIntegration, condicional |
| ChangeProposalType | ProposalTypeChanged | ProposalUpdatedForIntegration, condicional |
| UpdateProposalContent | ProposalContentUpdated | ProposalUpdatedForIntegration, condicional |
| ChangeProposalTerritory | ProposalTerritoryChanged | ProposalUpdatedForIntegration, condicional |
| AssociateProposalAssembly | ProposalAssemblyAssociated | ProposalUpdatedForIntegration, condicional |
| SubmitProposal | ProposalSubmitted | ProposalSubmittedForIntegration |
| StartProposalReview | ProposalReviewStarted | ProposalReviewStartedForIntegration |
| AcceptProposal | ProposalAccepted | ProposalAcceptedForIntegration |
| RejectProposal | ProposalRejected | ProposalRejectedForIntegration |
| WithdrawProposal | ProposalWithdrawn | ProposalWithdrawnForIntegration |
| ArchiveProposal | ProposalArchived | ProposalArchivedForIntegration |

## DOMAIN-008 — Participation

| Command | Domain Event | Integration Event |
|---|---|---|
| RegisterParticipation | ParticipationRegistered | ParticipationRegisteredIntegrationEvent |
| ActivateParticipation | ParticipationActivated | ParticipationActivatedIntegrationEvent |
| CompleteParticipation | ParticipationCompleted | ParticipationCompletedIntegrationEvent |
| WithdrawParticipation | ParticipationWithdrawn | ParticipationWithdrawnIntegrationEvent |
| InvalidateParticipation | ParticipationInvalidated | ParticipationInvalidatedIntegrationEvent |
| ArchiveParticipation | ParticipationArchived | ParticipationArchivedIntegrationEvent |
| ChangeParticipationType | ParticipationTypeChanged | ParticipationTypeChangedIntegrationEvent |
| ChangeParticipationContext | ParticipationContextChanged | ParticipationContextChangedIntegrationEvent |
| UpdateParticipationMetadata | ParticipationMetadataUpdated | ParticipationMetadataUpdatedIntegrationEvent |

## DOMAIN-009 — Voting

| Command | Domain Event | Integration Event |
|---|---|---|
| CreateVoting | VotingCreated | VotingCreatedIntegrationEvent |
| OpenVoting | VotingOpened | VotingOpenedIntegrationEvent |
| CloseVoting | VotingClosed | VotingClosedIntegrationEvent |
| CancelVoting | VotingCancelled | VotingCancelledIntegrationEvent |
| ArchiveVoting | VotingArchived | VotingArchivedIntegrationEvent |
| ChangeVotingType | VotingTypeChanged | — |
| ChangeVotingTitle | VotingTitleChanged | — |
| ChangeVotingDescription | VotingDescriptionChanged | — |
| ChangeVotingRules | VotingRulesChanged | — |
| AddVotingOption | VotingOptionAdded | — |
| RemoveVotingOption | VotingOptionRemoved | — |

## DOMAIN-010 — Document

| Command | Domain Event | Integration Event |
|---|---|---|
| CreateDocument | DocumentCreated | — |
| PublishDocument | DocumentPublished | — |
| ArchiveDocument | DocumentArchived | — |

## DOMAIN-011 — Notification

| Command | Domain Event | Integration Event |
|---|---|---|
| CreateNotification | NotificationCreated | NotificationCreatedIntegrationEvent |
| QueueNotification | NotificationQueued | NotificationQueuedIntegrationEvent |
| ConfirmNotificationDelivery | NotificationDelivered | NotificationDeliveredIntegrationEvent |
| ReportNotificationDeliveryFailure | NotificationDeliveryFailed | NotificationDeliveryFailedIntegrationEvent |
| RetryNotification | NotificationRetried | NotificationRetriedIntegrationEvent |

## DOMAIN-012 — Audit

| Command | Domain Event | Integration Event |
|---|---|---|
| RecordAudit | AuditRecorded | AuditRecordedIntegrationEvent |

## DOMAIN-013 — Integration

| Command | Domain Event | Integration Event |
|---|---|---|
| CreateIntegration | IntegrationCreated | IntegrationCreatedIntegrationEvent |
| ActivateIntegration | IntegrationActivated | IntegrationActivatedIntegrationEvent |
| SuspendIntegration | IntegrationSuspended | IntegrationSuspendedIntegrationEvent |
| ReactivateIntegration | IntegrationReactivated | IntegrationReactivatedIntegrationEvent |
| ArchiveIntegration | IntegrationArchived | IntegrationArchivedIntegrationEvent |

## Totales

| Concepto | Total |
|---|---:|
| Commands oficiales | 120 |
| Domain Events oficiales | 120 |
| Integration Events nombrados | 83 |

Los contratos condicionales agrupados se cuentan una sola vez por nombre. Los
hechos sin contrato público permanecen internos.

## Regla de publicación

```text
Confirmed Domain Event
    + Explicit Selection
    + Public Contract Version
    + Minimal Published Language
    = Eligible Integration Event
```

La igualdad de nombres, posición en una tabla o similitud de payload nunca
sustituye la selección explícita.