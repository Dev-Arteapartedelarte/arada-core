from datetime import UTC, datetime

from arada_core.participation.application.integration_events.participation_activated_integration_event import (
    ParticipationActivatedIntegrationEvent,
)
from arada_core.participation.application.integration_events.participation_registered_integration_event import (
    ParticipationRegisteredIntegrationEvent,
)
from arada_core.participation.domain.value_objects.organization_id import OrganizationId
from arada_core.participation.domain.value_objects.participation_id import (
    ParticipationId,
)
from arada_core.participation.domain.value_objects.participation_type import (
    ParticipationType,
)
from arada_core.participation.domain.value_objects.participation_version import (
    ParticipationVersion,
)


def test_registered_integration_event_exposes_public_contract() -> None:
    occurred_at = datetime(2026, 8, 29, 12, 0, tzinfo=UTC)

    event = ParticipationRegisteredIntegrationEvent(
        event_id="EVT-001",
        event_type="ParticipationRegisteredIntegrationEvent",
        event_version=1,
        aggregate_id=ParticipationId("PAR-001"),
        aggregate_type="Participation",
        aggregate_version=ParticipationVersion(1),
        occurred_at=occurred_at,
        correlation_id="CORR-001",
        causation_id="CMD-001",
        organization_id=OrganizationId("ORG-001"),
        participation_type=ParticipationType.ATTENDANCE,
    )

    assert event.event_id == "EVT-001"
    assert event.event_type == "ParticipationRegisteredIntegrationEvent"
    assert event.event_version == 1
    assert event.aggregate_id == ParticipationId("PAR-001")
    assert event.aggregate_type == "Participation"
    assert event.aggregate_version == ParticipationVersion(1)
    assert event.occurred_at == occurred_at
    assert event.correlation_id == "CORR-001"
    assert event.causation_id == "CMD-001"
    assert event.organization_id == OrganizationId("ORG-001")
    assert event.participation_type is ParticipationType.ATTENDANCE


def test_registered_integration_event_allows_optional_trace_metadata() -> None:
    event = ParticipationRegisteredIntegrationEvent(
        event_id="EVT-001",
        event_type="ParticipationRegisteredIntegrationEvent",
        event_version=1,
        aggregate_id=ParticipationId("PAR-001"),
        aggregate_type="Participation",
        aggregate_version=ParticipationVersion(1),
        occurred_at=datetime(2026, 8, 29, 12, 0, tzinfo=UTC),
        correlation_id=None,
        causation_id=None,
        organization_id=OrganizationId("ORG-001"),
        participation_type=ParticipationType.INTERVENTION,
    )

    assert event.correlation_id is None
    assert event.causation_id is None


def test_activated_integration_event_exposes_public_contract() -> None:
    occurred_at = datetime(2026, 8, 29, 12, 30, tzinfo=UTC)

    event = ParticipationActivatedIntegrationEvent(
        event_id="EVT-002",
        event_type="ParticipationActivatedIntegrationEvent",
        event_version=1,
        aggregate_id=ParticipationId("PAR-001"),
        aggregate_type="Participation",
        aggregate_version=ParticipationVersion(2),
        occurred_at=occurred_at,
        correlation_id="CORR-001",
        causation_id="CMD-002",
        organization_id=OrganizationId("ORG-001"),
    )

    assert event.event_id == "EVT-002"
    assert event.event_type == "ParticipationActivatedIntegrationEvent"
    assert event.event_version == 1
    assert event.aggregate_id == ParticipationId("PAR-001")
    assert event.aggregate_type == "Participation"
    assert event.aggregate_version == ParticipationVersion(2)
    assert event.occurred_at == occurred_at
    assert event.correlation_id == "CORR-001"
    assert event.causation_id == "CMD-002"
    assert event.organization_id == OrganizationId("ORG-001")


def test_activated_integration_event_allows_optional_trace_metadata() -> None:
    event = ParticipationActivatedIntegrationEvent(
        event_id="EVT-002",
        event_type="ParticipationActivatedIntegrationEvent",
        event_version=1,
        aggregate_id=ParticipationId("PAR-001"),
        aggregate_type="Participation",
        aggregate_version=ParticipationVersion(2),
        occurred_at=datetime(2026, 8, 29, 12, 30, tzinfo=UTC),
        correlation_id=None,
        causation_id=None,
        organization_id=OrganizationId("ORG-001"),
    )

    assert event.correlation_id is None
    assert event.causation_id is None


def test_event_version_is_independent_from_aggregate_version() -> None:
    event = ParticipationActivatedIntegrationEvent(
        event_id="EVT-002",
        event_type="ParticipationActivatedIntegrationEvent",
        event_version=1,
        aggregate_id=ParticipationId("PAR-001"),
        aggregate_type="Participation",
        aggregate_version=ParticipationVersion(7),
        occurred_at=datetime(2026, 8, 29, 12, 30, tzinfo=UTC),
        correlation_id=None,
        causation_id=None,
        organization_id=OrganizationId("ORG-001"),
    )

    assert event.event_version == 1
    assert event.aggregate_version == ParticipationVersion(7)


def test_integration_events_do_not_expose_published_at() -> None:
    event = ParticipationRegisteredIntegrationEvent(
        event_id="EVT-001",
        event_type="ParticipationRegisteredIntegrationEvent",
        event_version=1,
        aggregate_id=ParticipationId("PAR-001"),
        aggregate_type="Participation",
        aggregate_version=ParticipationVersion(1),
        occurred_at=datetime(2026, 8, 29, 12, 0, tzinfo=UTC),
        correlation_id=None,
        causation_id=None,
        organization_id=OrganizationId("ORG-001"),
        participation_type=ParticipationType.CONSULTATION,
    )

    assert not hasattr(event, "published_at")