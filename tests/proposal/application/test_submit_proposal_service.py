from collections.abc import Sequence
from datetime import UTC, datetime

import pytest

from arada_core.proposal.application.commands.submit_proposal import SubmitProposal
from arada_core.proposal.application.integration_events.proposal_submitted_for_integration import (
    ProposalSubmittedForIntegration,
)
from arada_core.proposal.application.ports.authorization_port import (
    AuthorizationPort,
)
from arada_core.proposal.application.ports.domain_event_publisher import (
    DomainEventPublisher,
)
from arada_core.proposal.application.ports.integration_event_publisher import (
    IntegrationEventPublisher,
)
from arada_core.proposal.application.ports.proposal_reference_validation_port import (
    ProposalReferenceValidationPort,
)
from arada_core.proposal.application.services.submit_proposal_service import (
    SubmitProposalService,
)
from arada_core.proposal.domain.aggregates.proposal import Proposal
from arada_core.proposal.domain.events.proposal_submitted import ProposalSubmitted
from arada_core.proposal.domain.repositories.proposal_repository import (
    ProposalRepository,
)
from arada_core.proposal.domain.value_objects.assembly_id import AssemblyId
from arada_core.proposal.domain.value_objects.citizen_id import CitizenId
from arada_core.proposal.domain.value_objects.organization_id import OrganizationId
from arada_core.proposal.domain.value_objects.proposal_description import (
    ProposalDescription,
)
from arada_core.proposal.domain.value_objects.proposal_id import ProposalId
from arada_core.proposal.domain.value_objects.proposal_name import ProposalName
from arada_core.proposal.domain.value_objects.proposal_type import ProposalType
from arada_core.proposal.domain.value_objects.proposal_version import ProposalVersion
from arada_core.proposal.domain.value_objects.proposer_reference import (
    ProposerReference,
)
from arada_core.proposal.domain.value_objects.submitted_at import SubmittedAt
from arada_core.proposal.domain.value_objects.territory_id import TerritoryId


class InMemoryProposalRepository(ProposalRepository):
    def __init__(
        self,
        proposal: Proposal | None = None,
    ) -> None:
        self.proposals: dict[ProposalId, Proposal] = {}
        self.save_calls: list[
            tuple[Proposal, ProposalVersion | None]
        ] = []

        if proposal is not None:
            self.proposals[proposal.proposal_id] = proposal

    def get_by_id(
        self,
        proposal_id: ProposalId,
    ) -> Proposal | None:
        return self.proposals.get(proposal_id)

    def exists(
        self,
        proposal_id: ProposalId,
    ) -> bool:
        return proposal_id in self.proposals

    def save(
        self,
        proposal: Proposal,
        expected_version: ProposalVersion | None,
    ) -> None:
        self.save_calls.append(
            (
                proposal,
                expected_version,
            )
        )
        self.proposals[proposal.proposal_id] = proposal


class FailingProposalRepository(InMemoryProposalRepository):
    def save(
        self,
        proposal: Proposal,
        expected_version: ProposalVersion | None,
    ) -> None:
        self.save_calls.append(
            (
                proposal,
                expected_version,
            )
        )
        raise RuntimeError("Persistence failure.")


class StubAuthorizationPort(AuthorizationPort):
    def __init__(
        self,
        *,
        authorized: bool,
    ) -> None:
        self.authorized = authorized
        self.calls: list[tuple[str, str]] = []

    def is_authorized(
        self,
        actor_id: str,
        permission: str,
    ) -> bool:
        self.calls.append(
            (
                actor_id,
                permission,
            )
        )
        return self.authorized


class StubProposalReferenceValidationPort(
    ProposalReferenceValidationPort
):
    def __init__(self) -> None:
        self.organization_calls: list[OrganizationId] = []
        self.proposer_calls: list[
            tuple[ProposerReference, OrganizationId]
        ] = []
        self.territory_calls: list[TerritoryId] = []
        self.assembly_calls: list[
            tuple[AssemblyId, OrganizationId]
        ] = []

    def validate_organization(
        self,
        organization_id: OrganizationId,
    ) -> None:
        self.organization_calls.append(
            organization_id
        )

    def validate_proposer(
        self,
        proposer_reference: ProposerReference,
        organization_id: OrganizationId,
    ) -> None:
        self.proposer_calls.append(
            (
                proposer_reference,
                organization_id,
            )
        )

    def validate_territory(
        self,
        territory_id: TerritoryId,
    ) -> None:
        self.territory_calls.append(
            territory_id
        )

    def validate_assembly(
        self,
        assembly_id: AssemblyId,
        organization_id: OrganizationId,
    ) -> None:
        self.assembly_calls.append(
            (
                assembly_id,
                organization_id,
            )
        )


class RecordingDomainEventPublisher(
    DomainEventPublisher
):
    def __init__(self) -> None:
        self.published: list[object] = []

    def publish(
        self,
        events: Sequence[object],
    ) -> None:
        self.published.extend(events)


class RecordingIntegrationEventPublisher(
    IntegrationEventPublisher
):
    def __init__(self) -> None:
        self.published: list[object] = []

    def publish(
        self,
        events: Sequence[object],
    ) -> None:
        self.published.extend(events)


def build_draft_proposal() -> Proposal:
    proposal = Proposal.create(
        proposal_id=ProposalId("proposal-001"),
        organization_id=OrganizationId(
            "organization-001"
        ),
        proposer_reference=ProposerReference(
            CitizenId("citizen-001")
        ),
        proposal_name=ProposalName(
            "Mejoramiento plaza comunitaria"
        ),
        proposal_type=ProposalType.COMMUNITY,
        proposal_description=ProposalDescription(
            "Mejorar la plaza central del sector."
        ),
        territory_id=TerritoryId("territory-001"),
        assembly_id=AssemblyId("assembly-001"),
    )

    proposal.pull_domain_events()

    return proposal


def build_submitted_at() -> SubmittedAt:
    return SubmittedAt(
        datetime(
            2026,
            8,
            26,
            10,
            0,
            tzinfo=UTC,
        )
    )


def build_service(
    *,
    repository: ProposalRepository | None = None,
    authorized: bool = True,
) -> tuple[
    SubmitProposalService,
    ProposalRepository,
    StubAuthorizationPort,
    StubProposalReferenceValidationPort,
    RecordingDomainEventPublisher,
    RecordingIntegrationEventPublisher,
]:
    resolved_repository = (
        repository
        if repository is not None
        else InMemoryProposalRepository(
            build_draft_proposal()
        )
    )

    authorization = StubAuthorizationPort(
        authorized=authorized
    )
    reference_validation = (
        StubProposalReferenceValidationPort()
    )
    domain_event_publisher = (
        RecordingDomainEventPublisher()
    )
    integration_event_publisher = (
        RecordingIntegrationEventPublisher()
    )

    service = SubmitProposalService(
        repository=resolved_repository,
        authorization=authorization,
        reference_validation=reference_validation,
        domain_event_publisher=domain_event_publisher,
        integration_event_publisher=integration_event_publisher,
    )

    return (
        service,
        resolved_repository,
        authorization,
        reference_validation,
        domain_event_publisher,
        integration_event_publisher,
    )


def test_submit_proposal_service_submits_and_persists_proposal() -> None:
    (
        service,
        repository,
        authorization,
        reference_validation,
        domain_event_publisher,
        integration_event_publisher,
    ) = build_service()

    assert isinstance(
        repository,
        InMemoryProposalRepository,
    )

    command = SubmitProposal(
        proposal_id=ProposalId("proposal-001"),
        expected_version=ProposalVersion(1),
    )

    submitted_at = build_submitted_at()

    published_at = datetime(
        2026,
        8,
        26,
        10,
        1,
        tzinfo=UTC,
    )

    result = service.execute(
        command,
        actor_id="actor-001",
        submitted_at=submitted_at,
        integration_event_id="integration-event-002",
        published_at=published_at,
        correlation_id="process-001",
        causation_id="command-002",
    )

    assert authorization.calls == [
        (
            "actor-001",
            "proposal:submit",
        )
    ]

    assert reference_validation.organization_calls == [
        OrganizationId("organization-001")
    ]
    assert reference_validation.proposer_calls == [
        (
            ProposerReference(
                CitizenId("citizen-001")
            ),
            OrganizationId("organization-001"),
        )
    ]
    assert reference_validation.territory_calls == [
        TerritoryId("territory-001")
    ]
    assert reference_validation.assembly_calls == [
        (
            AssemblyId("assembly-001"),
            OrganizationId("organization-001"),
        )
    ]

    assert len(repository.save_calls) == 1

    saved_proposal, expected_version = (
        repository.save_calls[0]
    )

    assert saved_proposal.proposal_id == command.proposal_id
    assert expected_version == command.expected_version

    assert result.proposal_id == command.proposal_id
    assert result.organization_id == OrganizationId(
        "organization-001"
    )
    assert result.proposer_reference == ProposerReference(
        CitizenId("citizen-001")
    )
    assert result.proposal_name == ProposalName(
        "Mejoramiento plaza comunitaria"
    )
    assert result.proposal_type == ProposalType.COMMUNITY
    assert result.proposal_status.value == "Submitted"
    assert result.version == ProposalVersion(2)
    assert result.territory_id == TerritoryId(
        "territory-001"
    )
    assert result.assembly_id == AssemblyId(
        "assembly-001"
    )
    assert result.submitted_at == submitted_at.value

    assert len(domain_event_publisher.published) == 1

    domain_event = domain_event_publisher.published[0]

    assert isinstance(
        domain_event,
        ProposalSubmitted,
    )
    assert domain_event.proposal_id == command.proposal_id
    assert domain_event.organization_id == OrganizationId(
        "organization-001"
    )
    assert domain_event.version == ProposalVersion(2)

    assert len(
        integration_event_publisher.published
    ) == 1

    integration_event = (
        integration_event_publisher.published[0]
    )

    assert isinstance(
        integration_event,
        ProposalSubmittedForIntegration,
    )

    assert (
        integration_event.event_id
        == "integration-event-002"
    )
    assert (
        integration_event.event_type
        == "ProposalSubmittedForIntegration"
    )
    assert integration_event.event_version == 1
    assert integration_event.published_at == published_at

    assert integration_event.proposal_id == "proposal-001"
    assert (
        integration_event.organization_id
        == "organization-001"
    )
    assert (
        integration_event.proposer_reference
        == str(
            ProposerReference(
                CitizenId("citizen-001")
            )
        )
    )
    assert (
        integration_event.territory_id
        == "territory-001"
    )
    assert (
        integration_event.assembly_id
        == "assembly-001"
    )
    assert integration_event.proposal_type == "Community"
    assert integration_event.proposal_status == "Submitted"
    assert integration_event.submitted_at == submitted_at.value
    assert integration_event.proposal_version == 2
    assert integration_event.correlation_id == "process-001"
    assert integration_event.causation_id == "command-002"


def test_submit_proposal_service_keeps_actor_separate_from_trace_metadata() -> None:
    (
        service,
        _,
        authorization,
        _,
        _,
        integration_event_publisher,
    ) = build_service()

    service.execute(
        SubmitProposal(
            proposal_id=ProposalId("proposal-001"),
            expected_version=ProposalVersion(1),
        ),
        actor_id="actor-001",
        submitted_at=build_submitted_at(),
        integration_event_id="integration-event-002",
        published_at=datetime(
            2026,
            8,
            26,
            10,
            1,
            tzinfo=UTC,
        ),
        correlation_id="process-001",
        causation_id="command-002",
    )

    assert authorization.calls == [
        (
            "actor-001",
            "proposal:submit",
        )
    ]

    assert len(
        integration_event_publisher.published
    ) == 1

    integration_event = (
        integration_event_publisher.published[0]
    )

    assert isinstance(
        integration_event,
        ProposalSubmittedForIntegration,
    )

    assert integration_event.correlation_id == "process-001"
    assert integration_event.causation_id == "command-002"
    assert integration_event.correlation_id != "actor-001"
    assert integration_event.causation_id != "actor-001"


def test_submit_proposal_service_allows_absent_trace_metadata() -> None:
    (
        service,
        _,
        _,
        _,
        _,
        integration_event_publisher,
    ) = build_service()

    service.execute(
        SubmitProposal(
            proposal_id=ProposalId("proposal-001"),
            expected_version=ProposalVersion(1),
        ),
        actor_id="actor-001",
        submitted_at=build_submitted_at(),
        integration_event_id="integration-event-002",
        published_at=datetime(
            2026,
            8,
            26,
            10,
            1,
            tzinfo=UTC,
        ),
    )

    assert len(
        integration_event_publisher.published
    ) == 1

    integration_event = (
        integration_event_publisher.published[0]
    )

    assert isinstance(
        integration_event,
        ProposalSubmittedForIntegration,
    )
    assert integration_event.correlation_id is None
    assert integration_event.causation_id is None


def test_submit_proposal_service_rejects_unauthorized_actor() -> None:
    (
        service,
        repository,
        authorization,
        reference_validation,
        domain_event_publisher,
        integration_event_publisher,
    ) = build_service(
        authorized=False
    )

    assert isinstance(
        repository,
        InMemoryProposalRepository,
    )

    with pytest.raises(PermissionError):
        service.execute(
            SubmitProposal(
                proposal_id=ProposalId("proposal-001"),
                expected_version=ProposalVersion(1),
            ),
            actor_id="actor-001",
            submitted_at=build_submitted_at(),
            integration_event_id="integration-event-002",
            published_at=datetime(
                2026,
                8,
                26,
                10,
                1,
                tzinfo=UTC,
            ),
            correlation_id="process-001",
            causation_id="command-002",
        )

    assert authorization.calls == [
        (
            "actor-001",
            "proposal:submit",
        )
    ]

    assert (
        reference_validation.organization_calls
        == []
    )
    assert reference_validation.proposer_calls == []
    assert reference_validation.territory_calls == []
    assert reference_validation.assembly_calls == []

    assert repository.save_calls == []
    assert domain_event_publisher.published == []
    assert integration_event_publisher.published == []


def test_submit_proposal_service_rejects_missing_proposal() -> None:
    repository = InMemoryProposalRepository()

    (
        service,
        _,
        _,
        reference_validation,
        domain_event_publisher,
        integration_event_publisher,
    ) = build_service(
        repository=repository
    )

    with pytest.raises(
        LookupError,
        match="Proposal not found",
    ):
        service.execute(
            SubmitProposal(
                proposal_id=ProposalId(
                    "proposal-missing"
                ),
                expected_version=ProposalVersion(1),
            ),
            actor_id="actor-001",
            submitted_at=build_submitted_at(),
            integration_event_id="integration-event-002",
            published_at=datetime(
                2026,
                8,
                26,
                10,
                1,
                tzinfo=UTC,
            ),
            correlation_id="process-001",
            causation_id="command-002",
        )

    assert (
        reference_validation.organization_calls
        == []
    )
    assert reference_validation.proposer_calls == []
    assert reference_validation.territory_calls == []
    assert reference_validation.assembly_calls == []

    assert repository.save_calls == []
    assert domain_event_publisher.published == []
    assert integration_event_publisher.published == []


def test_submit_proposal_service_does_not_publish_when_persistence_fails() -> None:
    repository = FailingProposalRepository(
        build_draft_proposal()
    )

    (
        service,
        _,
        _,
        _,
        domain_event_publisher,
        integration_event_publisher,
    ) = build_service(
        repository=repository
    )

    with pytest.raises(
        RuntimeError,
        match="Persistence failure",
    ):
        service.execute(
            SubmitProposal(
                proposal_id=ProposalId("proposal-001"),
                expected_version=ProposalVersion(1),
            ),
            actor_id="actor-001",
            submitted_at=build_submitted_at(),
            integration_event_id="integration-event-002",
            published_at=datetime(
                2026,
                8,
                26,
                10,
                1,
                tzinfo=UTC,
            ),
            correlation_id="process-001",
            causation_id="command-002",
        )

    assert len(repository.save_calls) == 1
    assert domain_event_publisher.published == []
    assert integration_event_publisher.published == []


def test_submit_proposal_service_publishes_only_after_save() -> None:
    call_order: list[str] = []

    class OrderedRepository(
        InMemoryProposalRepository
    ):
        def save(
            self,
            proposal: Proposal,
            expected_version: ProposalVersion | None,
        ) -> None:
            call_order.append("save")
            super().save(
                proposal,
                expected_version,
            )

    class OrderedDomainEventPublisher(
        RecordingDomainEventPublisher
    ):
        def publish(
            self,
            events: Sequence[object],
        ) -> None:
            call_order.append(
                "domain_publish"
            )
            super().publish(events)

    class OrderedIntegrationEventPublisher(
        RecordingIntegrationEventPublisher
    ):
        def publish(
            self,
            events: Sequence[object],
        ) -> None:
            call_order.append(
                "integration_publish"
            )
            super().publish(events)

    repository = OrderedRepository(
        build_draft_proposal()
    )
    authorization = StubAuthorizationPort(
        authorized=True
    )
    reference_validation = (
        StubProposalReferenceValidationPort()
    )
    domain_event_publisher = (
        OrderedDomainEventPublisher()
    )
    integration_event_publisher = (
        OrderedIntegrationEventPublisher()
    )

    service = SubmitProposalService(
        repository=repository,
        authorization=authorization,
        reference_validation=reference_validation,
        domain_event_publisher=domain_event_publisher,
        integration_event_publisher=integration_event_publisher,
    )

    service.execute(
        SubmitProposal(
            proposal_id=ProposalId("proposal-001"),
            expected_version=ProposalVersion(1),
        ),
        actor_id="actor-001",
        submitted_at=build_submitted_at(),
        integration_event_id="integration-event-002",
        published_at=datetime(
            2026,
            8,
            26,
            10,
            1,
            tzinfo=UTC,
        ),
        correlation_id="process-001",
        causation_id="command-002",
    )

    assert call_order == [
        "save",
        "domain_publish",
        "integration_publish",
    ]


def test_submit_proposal_service_increments_version_exactly_once() -> None:
    (
        service,
        _,
        _,
        _,
        _,
        _,
    ) = build_service()

    result = service.execute(
        SubmitProposal(
            proposal_id=ProposalId("proposal-001"),
            expected_version=ProposalVersion(1),
        ),
        actor_id="actor-001",
        submitted_at=build_submitted_at(),
        integration_event_id="integration-event-002",
        published_at=datetime(
            2026,
            8,
            26,
            10,
            1,
            tzinfo=UTC,
        ),
        correlation_id="process-001",
        causation_id="command-002",
    )

    assert result.version == ProposalVersion(2)


def test_submit_proposal_service_rejects_second_submission() -> None:
    (
        service,
        repository,
        _,
        _,
        domain_event_publisher,
        integration_event_publisher,
    ) = build_service()

    assert isinstance(
        repository,
        InMemoryProposalRepository,
    )

    submitted_at = build_submitted_at()

    service.execute(
        SubmitProposal(
            proposal_id=ProposalId("proposal-001"),
            expected_version=ProposalVersion(1),
        ),
        actor_id="actor-001",
        submitted_at=submitted_at,
        integration_event_id="integration-event-002",
        published_at=datetime(
            2026,
            8,
            26,
            10,
            1,
            tzinfo=UTC,
        ),
        correlation_id="process-001",
        causation_id="command-002",
    )

    domain_event_publisher.published.clear()
    integration_event_publisher.published.clear()
    repository.save_calls.clear()

    with pytest.raises(ValueError):
        service.execute(
            SubmitProposal(
                proposal_id=ProposalId("proposal-001"),
                expected_version=ProposalVersion(2),
            ),
            actor_id="actor-001",
            submitted_at=submitted_at,
            integration_event_id="integration-event-003",
            published_at=datetime(
                2026,
                8,
                26,
                10,
                2,
                tzinfo=UTC,
            ),
            correlation_id="process-001",
            causation_id="command-003",
        )

    assert repository.save_calls == []
    assert domain_event_publisher.published == []
    assert integration_event_publisher.published == []