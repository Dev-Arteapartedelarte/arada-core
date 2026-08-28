from datetime import UTC, datetime, timedelta

import pytest

from arada_core.proposal.application.integration_events.proposal_created_for_integration import (
    ProposalCreatedForIntegration,
)
from arada_core.proposal.application.integration_events.proposal_submitted_for_integration import (
    ProposalSubmittedForIntegration,
)


def test_proposal_created_for_integration_preserves_contract() -> None:
    occurred_at = datetime(2026, 8, 26, 10, 0, tzinfo=UTC)
    published_at = occurred_at + timedelta(seconds=1)

    event = ProposalCreatedForIntegration(
        event_id="integration-event-001",
        event_type="ProposalCreatedForIntegration",
        event_version=1,
        occurred_at=occurred_at,
        published_at=published_at,
        proposal_id="proposal-001",
        organization_id="organization-001",
        proposer_reference="citizen-001",
        territory_id="territory-001",
        assembly_id=None,
        proposal_type="Community",
        proposal_status="Draft",
        proposal_version=1,
        correlation_id="correlation-001",
        causation_id="command-001",
    )

    assert event.event_id == "integration-event-001"
    assert event.event_type == "ProposalCreatedForIntegration"
    assert event.event_version == 1
    assert event.occurred_at == occurred_at
    assert event.published_at == published_at
    assert event.proposal_id == "proposal-001"
    assert event.organization_id == "organization-001"
    assert event.proposer_reference == "citizen-001"
    assert event.territory_id == "territory-001"
    assert event.assembly_id is None
    assert event.proposal_type == "Community"
    assert event.proposal_status == "Draft"
    assert event.proposal_version == 1
    assert event.correlation_id == "correlation-001"
    assert event.causation_id == "command-001"


def test_proposal_created_for_integration_allows_absent_trace_metadata() -> None:
    occurred_at = datetime(2026, 8, 26, 10, 0, tzinfo=UTC)

    event = ProposalCreatedForIntegration(
        event_id="integration-event-001",
        event_type="ProposalCreatedForIntegration",
        event_version=1,
        occurred_at=occurred_at,
        published_at=occurred_at,
        proposal_id="proposal-001",
        organization_id="organization-001",
        proposer_reference="citizen-001",
        territory_id=None,
        assembly_id=None,
        proposal_type="Community",
        proposal_status="Draft",
        proposal_version=1,
        correlation_id=None,
        causation_id=None,
    )

    assert event.correlation_id is None
    assert event.causation_id is None


def test_proposal_submitted_for_integration_preserves_canonical_payload() -> None:
    occurred_at = datetime(2026, 8, 26, 10, 5, tzinfo=UTC)
    published_at = occurred_at + timedelta(seconds=1)
    submitted_at = occurred_at

    event = ProposalSubmittedForIntegration(
        event_id="integration-event-002",
        event_type="ProposalSubmittedForIntegration",
        event_version=1,
        occurred_at=occurred_at,
        published_at=published_at,
        proposal_id="proposal-001",
        organization_id="organization-001",
        proposer_reference="citizen-001",
        territory_id="territory-001",
        assembly_id="assembly-001",
        proposal_type="Community",
        proposal_status="Submitted",
        submitted_at=submitted_at,
        proposal_version=2,
        correlation_id="correlation-001",
        causation_id="command-002",
    )

    assert event.event_id == "integration-event-002"
    assert event.event_type == "ProposalSubmittedForIntegration"
    assert event.event_version == 1
    assert event.occurred_at == occurred_at
    assert event.published_at == published_at
    assert event.proposal_id == "proposal-001"
    assert event.organization_id == "organization-001"
    assert event.proposer_reference == "citizen-001"
    assert event.territory_id == "territory-001"
    assert event.assembly_id == "assembly-001"
    assert event.proposal_type == "Community"
    assert event.proposal_status == "Submitted"
    assert event.submitted_at == submitted_at
    assert event.proposal_version == 2
    assert event.correlation_id == "correlation-001"
    assert event.causation_id == "command-002"


def test_proposal_submitted_for_integration_allows_optional_context() -> None:
    occurred_at = datetime(2026, 8, 26, 10, 5, tzinfo=UTC)

    event = ProposalSubmittedForIntegration(
        event_id="integration-event-002",
        event_type="ProposalSubmittedForIntegration",
        event_version=1,
        occurred_at=occurred_at,
        published_at=occurred_at,
        proposal_id="proposal-001",
        organization_id="organization-001",
        proposer_reference="membership-001",
        territory_id=None,
        assembly_id=None,
        proposal_type="Organizational",
        proposal_status="Submitted",
        submitted_at=occurred_at,
        proposal_version=2,
        correlation_id=None,
        causation_id=None,
    )

    assert event.territory_id is None
    assert event.assembly_id is None
    assert event.correlation_id is None
    assert event.causation_id is None


@pytest.mark.parametrize(
    "field_name",
    [
        "event_id",
        "event_type",
        "proposal_id",
        "organization_id",
        "proposer_reference",
        "proposal_type",
        "proposal_status",
    ],
)
def test_proposal_created_for_integration_rejects_empty_required_strings(
    field_name: str,
) -> None:
    occurred_at = datetime(2026, 8, 26, 10, 0, tzinfo=UTC)

    values: dict[str, object] = {
        "event_id": "integration-event-001",
        "event_type": "ProposalCreatedForIntegration",
        "event_version": 1,
        "occurred_at": occurred_at,
        "published_at": occurred_at,
        "proposal_id": "proposal-001",
        "organization_id": "organization-001",
        "proposer_reference": "citizen-001",
        "territory_id": None,
        "assembly_id": None,
        "proposal_type": "Community",
        "proposal_status": "Draft",
        "proposal_version": 1,
        "correlation_id": None,
        "causation_id": None,
    }

    values[field_name] = ""

    with pytest.raises(ValueError):
        ProposalCreatedForIntegration(**values)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field_name",
    [
        "event_id",
        "event_type",
        "proposal_id",
        "organization_id",
        "proposer_reference",
        "proposal_type",
        "proposal_status",
    ],
)
def test_proposal_submitted_for_integration_rejects_empty_required_strings(
    field_name: str,
) -> None:
    occurred_at = datetime(2026, 8, 26, 10, 5, tzinfo=UTC)

    values: dict[str, object] = {
        "event_id": "integration-event-002",
        "event_type": "ProposalSubmittedForIntegration",
        "event_version": 1,
        "occurred_at": occurred_at,
        "published_at": occurred_at,
        "proposal_id": "proposal-001",
        "organization_id": "organization-001",
        "proposer_reference": "citizen-001",
        "territory_id": None,
        "assembly_id": None,
        "proposal_type": "Community",
        "proposal_status": "Submitted",
        "submitted_at": occurred_at,
        "proposal_version": 2,
        "correlation_id": None,
        "causation_id": None,
    }

    values[field_name] = ""

    with pytest.raises(ValueError):
        ProposalSubmittedForIntegration(**values)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("event_version", "proposal_version"),
    [
        (0, 1),
        (-1, 1),
        (True, 1),
        (1, 0),
        (1, -1),
        (1, True),
    ],
)
def test_proposal_created_for_integration_rejects_invalid_versions(
    event_version: int,
    proposal_version: int,
) -> None:
    occurred_at = datetime(2026, 8, 26, 10, 0, tzinfo=UTC)

    with pytest.raises(ValueError):
        ProposalCreatedForIntegration(
            event_id="integration-event-001",
            event_type="ProposalCreatedForIntegration",
            event_version=event_version,
            occurred_at=occurred_at,
            published_at=occurred_at,
            proposal_id="proposal-001",
            organization_id="organization-001",
            proposer_reference="citizen-001",
            territory_id=None,
            assembly_id=None,
            proposal_type="Community",
            proposal_status="Draft",
            proposal_version=proposal_version,
            correlation_id=None,
            causation_id=None,
        )


@pytest.mark.parametrize(
    ("event_version", "proposal_version"),
    [
        (0, 2),
        (-1, 2),
        (True, 2),
        (1, 0),
        (1, -1),
        (1, True),
    ],
)
def test_proposal_submitted_for_integration_rejects_invalid_versions(
    event_version: int,
    proposal_version: int,
) -> None:
    occurred_at = datetime(2026, 8, 26, 10, 5, tzinfo=UTC)

    with pytest.raises(ValueError):
        ProposalSubmittedForIntegration(
            event_id="integration-event-002",
            event_type="ProposalSubmittedForIntegration",
            event_version=event_version,
            occurred_at=occurred_at,
            published_at=occurred_at,
            proposal_id="proposal-001",
            organization_id="organization-001",
            proposer_reference="citizen-001",
            territory_id=None,
            assembly_id=None,
            proposal_type="Community",
            proposal_status="Submitted",
            submitted_at=occurred_at,
            proposal_version=proposal_version,
            correlation_id=None,
            causation_id=None,
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "territory_id",
        "assembly_id",
        "correlation_id",
        "causation_id",
    ],
)
def test_proposal_created_for_integration_rejects_empty_optional_identifiers(
    field_name: str,
) -> None:
    occurred_at = datetime(2026, 8, 26, 10, 0, tzinfo=UTC)

    values: dict[str, object] = {
        "event_id": "integration-event-001",
        "event_type": "ProposalCreatedForIntegration",
        "event_version": 1,
        "occurred_at": occurred_at,
        "published_at": occurred_at,
        "proposal_id": "proposal-001",
        "organization_id": "organization-001",
        "proposer_reference": "citizen-001",
        "territory_id": None,
        "assembly_id": None,
        "proposal_type": "Community",
        "proposal_status": "Draft",
        "proposal_version": 1,
        "correlation_id": None,
        "causation_id": None,
    }

    values[field_name] = ""

    with pytest.raises(ValueError):
        ProposalCreatedForIntegration(**values)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field_name",
    [
        "territory_id",
        "assembly_id",
        "correlation_id",
        "causation_id",
    ],
)
def test_proposal_submitted_for_integration_rejects_empty_optional_identifiers(
    field_name: str,
) -> None:
    occurred_at = datetime(2026, 8, 26, 10, 5, tzinfo=UTC)

    values: dict[str, object] = {
        "event_id": "integration-event-002",
        "event_type": "ProposalSubmittedForIntegration",
        "event_version": 1,
        "occurred_at": occurred_at,
        "published_at": occurred_at,
        "proposal_id": "proposal-001",
        "organization_id": "organization-001",
        "proposer_reference": "citizen-001",
        "territory_id": None,
        "assembly_id": None,
        "proposal_type": "Community",
        "proposal_status": "Submitted",
        "submitted_at": occurred_at,
        "proposal_version": 2,
        "correlation_id": None,
        "causation_id": None,
    }

    values[field_name] = ""

    with pytest.raises(ValueError):
        ProposalSubmittedForIntegration(**values)  # type: ignore[arg-type]


def test_proposal_created_for_integration_rejects_publication_before_occurrence() -> None:
    occurred_at = datetime(2026, 8, 26, 10, 0, tzinfo=UTC)

    with pytest.raises(ValueError):
        ProposalCreatedForIntegration(
            event_id="integration-event-001",
            event_type="ProposalCreatedForIntegration",
            event_version=1,
            occurred_at=occurred_at,
            published_at=occurred_at - timedelta(seconds=1),
            proposal_id="proposal-001",
            organization_id="organization-001",
            proposer_reference="citizen-001",
            territory_id=None,
            assembly_id=None,
            proposal_type="Community",
            proposal_status="Draft",
            proposal_version=1,
            correlation_id=None,
            causation_id=None,
        )


def test_proposal_submitted_for_integration_rejects_publication_before_occurrence() -> None:
    occurred_at = datetime(2026, 8, 26, 10, 5, tzinfo=UTC)

    with pytest.raises(ValueError):
        ProposalSubmittedForIntegration(
            event_id="integration-event-002",
            event_type="ProposalSubmittedForIntegration",
            event_version=1,
            occurred_at=occurred_at,
            published_at=occurred_at - timedelta(seconds=1),
            proposal_id="proposal-001",
            organization_id="organization-001",
            proposer_reference="citizen-001",
            territory_id=None,
            assembly_id=None,
            proposal_type="Community",
            proposal_status="Submitted",
            submitted_at=occurred_at,
            proposal_version=2,
            correlation_id=None,
            causation_id=None,
        )


def test_event_version_is_independent_from_proposal_version() -> None:
    occurred_at = datetime(2026, 8, 26, 10, 5, tzinfo=UTC)

    event = ProposalSubmittedForIntegration(
        event_id="integration-event-002",
        event_type="ProposalSubmittedForIntegration",
        event_version=1,
        occurred_at=occurred_at,
        published_at=occurred_at,
        proposal_id="proposal-001",
        organization_id="organization-001",
        proposer_reference="citizen-001",
        territory_id=None,
        assembly_id=None,
        proposal_type="Community",
        proposal_status="Submitted",
        submitted_at=occurred_at,
        proposal_version=15,
        correlation_id=None,
        causation_id=None,
    )

    assert event.event_version == 1
    assert event.proposal_version == 15
    assert event.event_version != event.proposal_version


def test_created_and_submitted_are_distinct_contracts() -> None:
    assert ProposalCreatedForIntegration is not ProposalSubmittedForIntegration
    assert (
        ProposalCreatedForIntegration.__name__
        == "ProposalCreatedForIntegration"
    )
    assert (
        ProposalSubmittedForIntegration.__name__
        == "ProposalSubmittedForIntegration"
    )