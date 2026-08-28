from datetime import UTC, datetime, timedelta

import pytest

from arada_core.proposal.application.integration_events.proposal_created_for_integration import (
    ProposalCreatedForIntegration,
)
from arada_core.proposal.application.integration_events.proposal_submitted_for_integration import (
    ProposalSubmittedForIntegration,
)
from arada_core.proposal.application.mappers.proposal_integration_event_mapper import (
    ProposalIntegrationEventMapper,
)
from arada_core.proposal.domain.events.proposal_created import ProposalCreated
from arada_core.proposal.domain.events.proposal_submitted import ProposalSubmitted
from arada_core.proposal.domain.value_objects.organization_id import OrganizationId
from arada_core.proposal.domain.value_objects.proposal_id import ProposalId
from arada_core.proposal.domain.value_objects.proposal_name import ProposalName
from arada_core.proposal.domain.value_objects.proposal_type import ProposalType
from arada_core.proposal.domain.value_objects.proposal_version import ProposalVersion


def build_proposal_created(
    *,
    occurred_at: datetime,
) -> ProposalCreated:
    return ProposalCreated(
        proposal_id=ProposalId("proposal-001"),
        organization_id=OrganizationId("organization-001"),
        proposal_name=ProposalName(
            "Mejoramiento plaza comunitaria"
        ),
        proposal_type=ProposalType.COMMUNITY,
        occurred_at=occurred_at,
        version=ProposalVersion(1),
    )


def build_proposal_submitted(
    *,
    occurred_at: datetime,
) -> ProposalSubmitted:
    return ProposalSubmitted(
        proposal_id=ProposalId("proposal-001"),
        organization_id=OrganizationId("organization-001"),
        occurred_at=occurred_at,
        version=ProposalVersion(2),
    )


def test_maps_proposal_created_to_canonical_integration_event() -> None:
    occurred_at = datetime(
        2026,
        8,
        26,
        10,
        0,
        tzinfo=UTC,
    )
    published_at = occurred_at + timedelta(seconds=1)

    domain_event = build_proposal_created(
        occurred_at=occurred_at,
    )

    integration_event = (
        ProposalIntegrationEventMapper.from_proposal_created(
            domain_event,
            event_id="integration-event-001",
            published_at=published_at,
            proposer_reference="citizen-001",
            territory_id="territory-001",
            assembly_id="assembly-001",
            proposal_type=ProposalType.COMMUNITY.value,
            proposal_status="Draft",
            correlation_id="correlation-001",
            causation_id="command-001",
        )
    )

    assert isinstance(
        integration_event,
        ProposalCreatedForIntegration,
    )

    assert integration_event.event_id == "integration-event-001"
    assert (
        integration_event.event_type
        == ProposalIntegrationEventMapper.CREATED_EVENT_TYPE
    )
    assert (
        integration_event.event_version
        == ProposalIntegrationEventMapper.CREATED_EVENT_VERSION
    )

    assert integration_event.occurred_at == occurred_at
    assert integration_event.published_at == published_at

    assert integration_event.proposal_id == "proposal-001"
    assert integration_event.organization_id == "organization-001"
    assert integration_event.proposer_reference == "citizen-001"
    assert integration_event.territory_id == "territory-001"
    assert integration_event.assembly_id == "assembly-001"
    assert integration_event.proposal_type == "Community"
    assert integration_event.proposal_status == "Draft"
    assert integration_event.proposal_version == 1

    assert integration_event.correlation_id == "correlation-001"
    assert integration_event.causation_id == "command-001"


def test_maps_proposal_submitted_to_canonical_integration_event() -> None:
    occurred_at = datetime(
        2026,
        8,
        26,
        10,
        5,
        tzinfo=UTC,
    )
    published_at = occurred_at + timedelta(seconds=1)
    submitted_at = occurred_at

    domain_event = build_proposal_submitted(
        occurred_at=occurred_at,
    )

    integration_event = (
        ProposalIntegrationEventMapper.from_proposal_submitted(
            domain_event,
            event_id="integration-event-002",
            published_at=published_at,
            proposer_reference="citizen-001",
            territory_id="territory-001",
            assembly_id="assembly-001",
            proposal_type=ProposalType.COMMUNITY.value,
            proposal_status="Submitted",
            submitted_at=submitted_at,
            correlation_id="correlation-001",
            causation_id="command-002",
        )
    )

    assert isinstance(
        integration_event,
        ProposalSubmittedForIntegration,
    )

    assert integration_event.event_id == "integration-event-002"
    assert (
        integration_event.event_type
        == ProposalIntegrationEventMapper.SUBMITTED_EVENT_TYPE
    )
    assert (
        integration_event.event_version
        == ProposalIntegrationEventMapper.SUBMITTED_EVENT_VERSION
    )

    assert integration_event.occurred_at == occurred_at
    assert integration_event.published_at == published_at

    assert integration_event.proposal_id == "proposal-001"
    assert integration_event.organization_id == "organization-001"
    assert integration_event.proposer_reference == "citizen-001"
    assert integration_event.territory_id == "territory-001"
    assert integration_event.assembly_id == "assembly-001"
    assert integration_event.proposal_type == "Community"
    assert integration_event.proposal_status == "Submitted"
    assert integration_event.submitted_at == submitted_at
    assert integration_event.proposal_version == 2

    assert integration_event.correlation_id == "correlation-001"
    assert integration_event.causation_id == "command-002"


def test_created_mapping_preserves_explicit_event_id() -> None:
    occurred_at = datetime(
        2026,
        8,
        26,
        10,
        0,
        tzinfo=UTC,
    )

    domain_event = build_proposal_created(
        occurred_at=occurred_at,
    )

    integration_event = (
        ProposalIntegrationEventMapper.from_proposal_created(
            domain_event,
            event_id="externally-provided-event-id",
            published_at=occurred_at,
            proposer_reference="citizen-001",
            territory_id=None,
            assembly_id=None,
            proposal_type=ProposalType.COMMUNITY.value,
            proposal_status="Draft",
            correlation_id=None,
            causation_id=None,
        )
    )

    assert (
        integration_event.event_id
        == "externally-provided-event-id"
    )


def test_submitted_mapping_preserves_explicit_event_id() -> None:
    occurred_at = datetime(
        2026,
        8,
        26,
        10,
        5,
        tzinfo=UTC,
    )

    domain_event = build_proposal_submitted(
        occurred_at=occurred_at,
    )

    integration_event = (
        ProposalIntegrationEventMapper.from_proposal_submitted(
            domain_event,
            event_id="externally-provided-event-id",
            published_at=occurred_at,
            proposer_reference="citizen-001",
            territory_id=None,
            assembly_id=None,
            proposal_type=ProposalType.COMMUNITY.value,
            proposal_status="Submitted",
            submitted_at=occurred_at,
            correlation_id=None,
            causation_id=None,
        )
    )

    assert (
        integration_event.event_id
        == "externally-provided-event-id"
    )


def test_created_mapping_does_not_generate_trace_metadata() -> None:
    occurred_at = datetime(
        2026,
        8,
        26,
        10,
        0,
        tzinfo=UTC,
    )

    domain_event = build_proposal_created(
        occurred_at=occurred_at,
    )

    integration_event = (
        ProposalIntegrationEventMapper.from_proposal_created(
            domain_event,
            event_id="integration-event-001",
            published_at=occurred_at,
            proposer_reference="citizen-001",
            territory_id=None,
            assembly_id=None,
            proposal_type=ProposalType.COMMUNITY.value,
            proposal_status="Draft",
            correlation_id=None,
            causation_id=None,
        )
    )

    assert integration_event.correlation_id is None
    assert integration_event.causation_id is None


def test_submitted_mapping_does_not_generate_trace_metadata() -> None:
    occurred_at = datetime(
        2026,
        8,
        26,
        10,
        5,
        tzinfo=UTC,
    )

    domain_event = build_proposal_submitted(
        occurred_at=occurred_at,
    )

    integration_event = (
        ProposalIntegrationEventMapper.from_proposal_submitted(
            domain_event,
            event_id="integration-event-002",
            published_at=occurred_at,
            proposer_reference="citizen-001",
            territory_id=None,
            assembly_id=None,
            proposal_type=ProposalType.COMMUNITY.value,
            proposal_status="Submitted",
            submitted_at=occurred_at,
            correlation_id=None,
            causation_id=None,
        )
    )

    assert integration_event.correlation_id is None
    assert integration_event.causation_id is None


def test_created_mapping_preserves_optional_context_references() -> None:
    occurred_at = datetime(
        2026,
        8,
        26,
        10,
        0,
        tzinfo=UTC,
    )

    domain_event = build_proposal_created(
        occurred_at=occurred_at,
    )

    without_context = (
        ProposalIntegrationEventMapper.from_proposal_created(
            domain_event,
            event_id="integration-event-001",
            published_at=occurred_at,
            proposer_reference="citizen-001",
            territory_id=None,
            assembly_id=None,
            proposal_type=ProposalType.COMMUNITY.value,
            proposal_status="Draft",
            correlation_id=None,
            causation_id=None,
        )
    )

    with_context = (
        ProposalIntegrationEventMapper.from_proposal_created(
            domain_event,
            event_id="integration-event-002",
            published_at=occurred_at,
            proposer_reference="citizen-001",
            territory_id="territory-001",
            assembly_id="assembly-001",
            proposal_type=ProposalType.COMMUNITY.value,
            proposal_status="Draft",
            correlation_id=None,
            causation_id=None,
        )
    )

    assert without_context.territory_id is None
    assert without_context.assembly_id is None

    assert with_context.territory_id == "territory-001"
    assert with_context.assembly_id == "assembly-001"


def test_submitted_mapping_preserves_optional_context_references() -> None:
    occurred_at = datetime(
        2026,
        8,
        26,
        10,
        5,
        tzinfo=UTC,
    )

    domain_event = build_proposal_submitted(
        occurred_at=occurred_at,
    )

    without_context = (
        ProposalIntegrationEventMapper.from_proposal_submitted(
            domain_event,
            event_id="integration-event-001",
            published_at=occurred_at,
            proposer_reference="citizen-001",
            territory_id=None,
            assembly_id=None,
            proposal_type=ProposalType.COMMUNITY.value,
            proposal_status="Submitted",
            submitted_at=occurred_at,
            correlation_id=None,
            causation_id=None,
        )
    )

    with_context = (
        ProposalIntegrationEventMapper.from_proposal_submitted(
            domain_event,
            event_id="integration-event-002",
            published_at=occurred_at,
            proposer_reference="citizen-001",
            territory_id="territory-001",
            assembly_id="assembly-001",
            proposal_type=ProposalType.COMMUNITY.value,
            proposal_status="Submitted",
            submitted_at=occurred_at,
            correlation_id=None,
            causation_id=None,
        )
    )

    assert without_context.territory_id is None
    assert without_context.assembly_id is None

    assert with_context.territory_id == "territory-001"
    assert with_context.assembly_id == "assembly-001"


def test_created_mapping_preserves_correlation_and_causation_separately() -> None:
    occurred_at = datetime(
        2026,
        8,
        26,
        10,
        0,
        tzinfo=UTC,
    )

    domain_event = build_proposal_created(
        occurred_at=occurred_at,
    )

    integration_event = (
        ProposalIntegrationEventMapper.from_proposal_created(
            domain_event,
            event_id="integration-event-001",
            published_at=occurred_at,
            proposer_reference="citizen-001",
            territory_id=None,
            assembly_id=None,
            proposal_type=ProposalType.COMMUNITY.value,
            proposal_status="Draft",
            correlation_id="process-001",
            causation_id="command-001",
        )
    )

    assert integration_event.correlation_id == "process-001"
    assert integration_event.causation_id == "command-001"
    assert (
        integration_event.correlation_id
        != integration_event.causation_id
    )


def test_submitted_mapping_preserves_correlation_and_causation_separately() -> None:
    occurred_at = datetime(
        2026,
        8,
        26,
        10,
        5,
        tzinfo=UTC,
    )

    domain_event = build_proposal_submitted(
        occurred_at=occurred_at,
    )

    integration_event = (
        ProposalIntegrationEventMapper.from_proposal_submitted(
            domain_event,
            event_id="integration-event-002",
            published_at=occurred_at,
            proposer_reference="citizen-001",
            territory_id=None,
            assembly_id=None,
            proposal_type=ProposalType.COMMUNITY.value,
            proposal_status="Submitted",
            submitted_at=occurred_at,
            correlation_id="process-001",
            causation_id="command-002",
        )
    )

    assert integration_event.correlation_id == "process-001"
    assert integration_event.causation_id == "command-002"
    assert (
        integration_event.correlation_id
        != integration_event.causation_id
    )


def test_created_mapping_rejects_empty_event_id() -> None:
    occurred_at = datetime(
        2026,
        8,
        26,
        10,
        0,
        tzinfo=UTC,
    )

    domain_event = build_proposal_created(
        occurred_at=occurred_at,
    )

    with pytest.raises(
        ValueError,
        match="event_id must not be empty",
    ):
        ProposalIntegrationEventMapper.from_proposal_created(
            domain_event,
            event_id="",
            published_at=occurred_at,
            proposer_reference="citizen-001",
            territory_id=None,
            assembly_id=None,
            proposal_type=ProposalType.COMMUNITY.value,
            proposal_status="Draft",
            correlation_id=None,
            causation_id=None,
        )


def test_submitted_mapping_rejects_empty_event_id() -> None:
    occurred_at = datetime(
        2026,
        8,
        26,
        10,
        5,
        tzinfo=UTC,
    )

    domain_event = build_proposal_submitted(
        occurred_at=occurred_at,
    )

    with pytest.raises(
        ValueError,
        match="event_id must not be empty",
    ):
        ProposalIntegrationEventMapper.from_proposal_submitted(
            domain_event,
            event_id="",
            published_at=occurred_at,
            proposer_reference="citizen-001",
            territory_id=None,
            assembly_id=None,
            proposal_type=ProposalType.COMMUNITY.value,
            proposal_status="Submitted",
            submitted_at=occurred_at,
            correlation_id=None,
            causation_id=None,
        )


@pytest.mark.parametrize(
    ("correlation_id", "causation_id"),
    [
        ("", None),
        ("   ", None),
        (None, ""),
        (None, "   "),
    ],
)
def test_created_mapping_rejects_empty_trace_metadata_when_present(
    correlation_id: str | None,
    causation_id: str | None,
) -> None:
    occurred_at = datetime(
        2026,
        8,
        26,
        10,
        0,
        tzinfo=UTC,
    )

    domain_event = build_proposal_created(
        occurred_at=occurred_at,
    )

    with pytest.raises(ValueError):
        ProposalIntegrationEventMapper.from_proposal_created(
            domain_event,
            event_id="integration-event-001",
            published_at=occurred_at,
            proposer_reference="citizen-001",
            territory_id=None,
            assembly_id=None,
            proposal_type=ProposalType.COMMUNITY.value,
            proposal_status="Draft",
            correlation_id=correlation_id,
            causation_id=causation_id,
        )


@pytest.mark.parametrize(
    ("correlation_id", "causation_id"),
    [
        ("", None),
        ("   ", None),
        (None, ""),
        (None, "   "),
    ],
)
def test_submitted_mapping_rejects_empty_trace_metadata_when_present(
    correlation_id: str | None,
    causation_id: str | None,
) -> None:
    occurred_at = datetime(
        2026,
        8,
        26,
        10,
        5,
        tzinfo=UTC,
    )

    domain_event = build_proposal_submitted(
        occurred_at=occurred_at,
    )

    with pytest.raises(ValueError):
        ProposalIntegrationEventMapper.from_proposal_submitted(
            domain_event,
            event_id="integration-event-002",
            published_at=occurred_at,
            proposer_reference="citizen-001",
            territory_id=None,
            assembly_id=None,
            proposal_type=ProposalType.COMMUNITY.value,
            proposal_status="Submitted",
            submitted_at=occurred_at,
            correlation_id=correlation_id,
            causation_id=causation_id,
        )


def test_created_mapping_rejects_publication_before_occurrence() -> None:
    occurred_at = datetime(
        2026,
        8,
        26,
        10,
        0,
        tzinfo=UTC,
    )

    domain_event = build_proposal_created(
        occurred_at=occurred_at,
    )

    with pytest.raises(
        ValueError,
        match="PublishedAt must not precede OccurredAt",
    ):
        ProposalIntegrationEventMapper.from_proposal_created(
            domain_event,
            event_id="integration-event-001",
            published_at=occurred_at - timedelta(seconds=1),
            proposer_reference="citizen-001",
            territory_id=None,
            assembly_id=None,
            proposal_type=ProposalType.COMMUNITY.value,
            proposal_status="Draft",
            correlation_id=None,
            causation_id=None,
        )


def test_submitted_mapping_rejects_publication_before_occurrence() -> None:
    occurred_at = datetime(
        2026,
        8,
        26,
        10,
        5,
        tzinfo=UTC,
    )

    domain_event = build_proposal_submitted(
        occurred_at=occurred_at,
    )

    with pytest.raises(
        ValueError,
        match="PublishedAt must not precede OccurredAt",
    ):
        ProposalIntegrationEventMapper.from_proposal_submitted(
            domain_event,
            event_id="integration-event-002",
            published_at=occurred_at - timedelta(seconds=1),
            proposer_reference="citizen-001",
            territory_id=None,
            assembly_id=None,
            proposal_type=ProposalType.COMMUNITY.value,
            proposal_status="Submitted",
            submitted_at=occurred_at,
            correlation_id=None,
            causation_id=None,
        )


def test_created_mapping_does_not_return_domain_event() -> None:
    occurred_at = datetime(
        2026,
        8,
        26,
        10,
        0,
        tzinfo=UTC,
    )

    domain_event = build_proposal_created(
        occurred_at=occurred_at,
    )

    integration_event = (
        ProposalIntegrationEventMapper.from_proposal_created(
            domain_event,
            event_id="integration-event-001",
            published_at=occurred_at,
            proposer_reference="citizen-001",
            territory_id=None,
            assembly_id=None,
            proposal_type=ProposalType.COMMUNITY.value,
            proposal_status="Draft",
            correlation_id=None,
            causation_id=None,
        )
    )

    assert integration_event is not domain_event
    assert type(integration_event) is ProposalCreatedForIntegration


def test_submitted_mapping_does_not_return_domain_event() -> None:
    occurred_at = datetime(
        2026,
        8,
        26,
        10,
        5,
        tzinfo=UTC,
    )

    domain_event = build_proposal_submitted(
        occurred_at=occurred_at,
    )

    integration_event = (
        ProposalIntegrationEventMapper.from_proposal_submitted(
            domain_event,
            event_id="integration-event-002",
            published_at=occurred_at,
            proposer_reference="citizen-001",
            territory_id=None,
            assembly_id=None,
            proposal_type=ProposalType.COMMUNITY.value,
            proposal_status="Submitted",
            submitted_at=occurred_at,
            correlation_id=None,
            causation_id=None,
        )
    )

    assert integration_event is not domain_event
    assert type(integration_event) is ProposalSubmittedForIntegration