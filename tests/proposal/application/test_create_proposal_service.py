from collections.abc import Sequence
from datetime import UTC, datetime, timedelta

import pytest

from arada_core.proposal.application.commands.create_proposal import CreateProposal
from arada_core.proposal.application.integration_events.proposal_created_for_integration import (
    ProposalCreatedForIntegration,
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
from arada_core.proposal.application.services.create_proposal_service import (
    CreateProposalService,
)
from arada_core.proposal.domain.aggregates.proposal import Proposal
from arada_core.proposal.domain.events.proposal_created import ProposalCreated
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
from arada_core.proposal.domain.value_objects.territory_id import TerritoryId


class InMemoryProposalRepository(ProposalRepository):
    def __init__(self) -> None:
        self.proposals: dict[ProposalId, Proposal] = {}
        self.save_calls: list[
            tuple[Proposal, ProposalVersion | None]
        ] = []

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


def build_command() -> CreateProposal:
    return CreateProposal(
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


def build_service(
    *,
    repository: ProposalRepository | None = None,
    authorized: bool = True,
) -> tuple[
    CreateProposalService,
    ProposalRepository,
    StubAuthorizationPort,
    StubProposalReferenceValidationPort,
    RecordingDomainEventPublisher,
    RecordingIntegrationEventPublisher,
]:
    resolved_repository = (
        repository
        if repository is not None
        else InMemoryProposalRepository()
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

    service = CreateProposalService(
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


def test_create_proposal_service_creates_and_persists_proposal() -> None:
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

    command = build_command()

    published_at = datetime.now(UTC) + timedelta(
        minutes=1
    )

    result = service.execute(
        command,
        actor_id="actor-001",
        integration_event_id="integration-event-001",
        published_at=published_at,
        correlation_id="process-001",
        causation_id="command-001",
    )

    assert authorization.calls == [
        (
            "actor-001",
            "proposal:create",
        )
    ]

    assert reference_validation.organization_calls == [
        command.organization_id
    ]
    assert reference_validation.proposer_calls == [
        (
            command.proposer_reference,
            command.organization_id,
        )
    ]
    assert reference_validation.territory_calls == [
        command.territory_id
    ]
    assert reference_validation.assembly_calls == [
        (
            command.assembly_id,
            command.organization_id,
        )
    ]

    assert len(repository.save_calls) == 1

    saved_proposal, expected_version = (
        repository.save_calls[0]
    )

    assert saved_proposal.proposal_id == command.proposal_id
    assert expected_version is None

    assert result.proposal_id == command.proposal_id
    assert result.organization_id == command.organization_id
    assert (
        result.proposer_reference
        == command.proposer_reference
    )
    assert result.proposal_name == command.proposal_name
    assert result.proposal_type == command.proposal_type
    assert result.proposal_status.value == "Draft"
    assert result.version == ProposalVersion(1)
    assert result.territory_id == command.territory_id
    assert result.assembly_id == command.assembly_id
    assert result.submitted_at is None

    assert len(domain_event_publisher.published) == 1

    domain_event = domain_event_publisher.published[0]

    assert isinstance(
        domain_event,
        ProposalCreated,
    )
    assert domain_event.proposal_id == command.proposal_id
    assert (
        domain_event.organization_id
        == command.organization_id
    )
    assert domain_event.version == ProposalVersion(1)

    assert len(
        integration_event_publisher.published
    ) == 1

    integration_event = (
        integration_event_publisher.published[0]
    )

    assert isinstance(
        integration_event,
        ProposalCreatedForIntegration,
    )

    assert (
        integration_event.event_id
        == "integration-event-001"
    )
    assert (
        integration_event.event_type
        == "ProposalCreatedForIntegration"
    )
    assert integration_event.event_version == 1
    assert integration_event.published_at == published_at

    assert (
        integration_event.proposal_id
        == str(command.proposal_id)
    )
    assert (
        integration_event.organization_id
        == str(command.organization_id)
    )
    assert (
        integration_event.proposer_reference
        == str(command.proposer_reference)
    )
    assert (
        integration_event.territory_id
        == str(command.territory_id)
    )
    assert (
        integration_event.assembly_id
        == str(command.assembly_id)
    )
    assert (
        integration_event.proposal_type
        == command.proposal_type.value
    )
    assert integration_event.proposal_status == "Draft"
    assert integration_event.proposal_version == 1

    assert integration_event.correlation_id == "process-001"
    assert integration_event.causation_id == "command-001"


def test_create_proposal_service_keeps_actor_separate_from_trace_metadata() -> None:
    (
        service,
        _,
        authorization,
        _,
        _,
        integration_event_publisher,
    ) = build_service()

    published_at = datetime.now(UTC) + timedelta(
        minutes=1
    )

    service.execute(
        build_command(),
        actor_id="actor-001",
        integration_event_id="integration-event-001",
        published_at=published_at,
        correlation_id="process-001",
        causation_id="command-001",
    )

    assert authorization.calls == [
        (
            "actor-001",
            "proposal:create",
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
        ProposalCreatedForIntegration,
    )

    assert integration_event.correlation_id == "process-001"
    assert integration_event.causation_id == "command-001"
    assert integration_event.correlation_id != "actor-001"
    assert integration_event.causation_id != "actor-001"


def test_create_proposal_service_allows_absent_trace_metadata() -> None:
    (
        service,
        _,
        _,
        _,
        _,
        integration_event_publisher,
    ) = build_service()

    published_at = datetime.now(UTC) + timedelta(
        minutes=1
    )

    service.execute(
        build_command(),
        actor_id="actor-001",
        integration_event_id="integration-event-001",
        published_at=published_at,
    )

    assert len(
        integration_event_publisher.published
    ) == 1

    integration_event = (
        integration_event_publisher.published[0]
    )

    assert isinstance(
        integration_event,
        ProposalCreatedForIntegration,
    )
    assert integration_event.correlation_id is None
    assert integration_event.causation_id is None


def test_create_proposal_service_rejects_unauthorized_actor() -> None:
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
            build_command(),
            actor_id="actor-001",
            integration_event_id=(
                "integration-event-001"
            ),
            published_at=datetime(
                2026,
                8,
                26,
                10,
                0,
                tzinfo=UTC,
            ),
            correlation_id="process-001",
            causation_id="command-001",
        )

    assert authorization.calls == [
        (
            "actor-001",
            "proposal:create",
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


def test_create_proposal_service_rejects_existing_identity() -> None:
    repository = InMemoryProposalRepository()

    existing_command = build_command()

    existing_proposal = Proposal.create(
        proposal_id=existing_command.proposal_id,
        organization_id=existing_command.organization_id,
        proposer_reference=(
            existing_command.proposer_reference
        ),
        proposal_name=existing_command.proposal_name,
        proposal_type=existing_command.proposal_type,
        proposal_purpose=(
            existing_command.proposal_purpose
        ),
        proposal_description=(
            existing_command.proposal_description
        ),
        proposal_content=(
            existing_command.proposal_content
        ),
        territory_id=existing_command.territory_id,
        assembly_id=existing_command.assembly_id,
    )

    existing_proposal.pull_domain_events()

    repository.proposals[
        existing_command.proposal_id
    ] = existing_proposal

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
        ValueError,
        match="Proposal already exists",
    ):
        service.execute(
            existing_command,
            actor_id="actor-001",
            integration_event_id=(
                "integration-event-001"
            ),
            published_at=datetime(
                2026,
                8,
                26,
                10,
                0,
                tzinfo=UTC,
            ),
            correlation_id="process-001",
            causation_id="command-001",
        )

    assert (
        reference_validation.organization_calls
        == [existing_command.organization_id]
    )
    assert (
        reference_validation.proposer_calls
        == [
            (
                existing_command.proposer_reference,
                existing_command.organization_id,
            )
        ]
    )

    assert repository.save_calls == []
    assert domain_event_publisher.published == []
    assert integration_event_publisher.published == []


def test_create_proposal_service_does_not_publish_when_persistence_fails() -> None:
    repository = FailingProposalRepository()

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
            build_command(),
            actor_id="actor-001",
            integration_event_id=(
                "integration-event-001"
            ),
            published_at=datetime(
                2026,
                8,
                26,
                10,
                0,
                tzinfo=UTC,
            ),
            correlation_id="process-001",
            causation_id="command-001",
        )

    assert len(repository.save_calls) == 1
    assert domain_event_publisher.published == []
    assert integration_event_publisher.published == []


def test_create_proposal_service_publishes_only_after_save() -> None:
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

    repository = OrderedRepository()
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

    service = CreateProposalService(
        repository=repository,
        authorization=authorization,
        reference_validation=reference_validation,
        domain_event_publisher=domain_event_publisher,
        integration_event_publisher=integration_event_publisher,
    )

    service.execute(
        build_command(),
        actor_id="actor-001",
        integration_event_id="integration-event-001",
        published_at=(
            datetime.now(UTC)
            + timedelta(minutes=1)
        ),
        correlation_id="process-001",
        causation_id="command-001",
    )

    assert call_order == [
        "save",
        "domain_publish",
        "integration_publish",
    ]