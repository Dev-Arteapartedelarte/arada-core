from datetime import UTC, datetime

from arada_core.participation.domain.events.participation_activated import (
    ParticipationActivated,
)
from arada_core.participation.domain.events.participation_registered import (
    ParticipationRegistered,
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


def test_participation_registered_exposes_confirmed_domain_fact() -> None:
    occurred_at = datetime(2026, 8, 29, 12, 0, tzinfo=UTC)

    event = ParticipationRegistered(
        event_id="EVT-001",
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        participation_type=ParticipationType.ATTENDANCE,
        occurred_at=occurred_at,
        aggregate_version=ParticipationVersion(1),
        actor_id="ACTOR-001",
        correlation_id="CORR-001",
        causation_id="CMD-001",
    )

    assert event.event_id == "EVT-001"
    assert event.participation_id == ParticipationId("PAR-001")
    assert event.organization_id == OrganizationId("ORG-001")
    assert event.participation_type is ParticipationType.ATTENDANCE
    assert event.occurred_at == occurred_at
    assert event.aggregate_version == ParticipationVersion(1)
    assert event.actor_id == "ACTOR-001"
    assert event.correlation_id == "CORR-001"
    assert event.causation_id == "CMD-001"


def test_participation_registered_allows_optional_trace_metadata() -> None:
    event = ParticipationRegistered(
        event_id="EVT-001",
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        participation_type=ParticipationType.INTERVENTION,
        occurred_at=datetime(2026, 8, 29, 12, 0, tzinfo=UTC),
        aggregate_version=ParticipationVersion(1),
        actor_id="ACTOR-001",
    )

    assert event.correlation_id is None
    assert event.causation_id is None


def test_participation_activated_exposes_confirmed_domain_fact() -> None:
    started_at = datetime(2026, 8, 29, 12, 30, tzinfo=UTC)

    event = ParticipationActivated(
        event_id="EVT-002",
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        started_at=started_at,
        occurred_at=started_at,
        aggregate_version=ParticipationVersion(2),
        actor_id="ACTOR-002",
        correlation_id="CORR-001",
        causation_id="CMD-002",
    )

    assert event.event_id == "EVT-002"
    assert event.participation_id == ParticipationId("PAR-001")
    assert event.organization_id == OrganizationId("ORG-001")
    assert event.started_at == started_at
    assert event.occurred_at == started_at
    assert event.aggregate_version == ParticipationVersion(2)
    assert event.actor_id == "ACTOR-002"
    assert event.correlation_id == "CORR-001"
    assert event.causation_id == "CMD-002"


def test_participation_activated_allows_optional_trace_metadata() -> None:
    started_at = datetime(2026, 8, 29, 12, 30, tzinfo=UTC)

    event = ParticipationActivated(
        event_id="EVT-002",
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        started_at=started_at,
        occurred_at=started_at,
        aggregate_version=ParticipationVersion(2),
        actor_id="ACTOR-002",
    )

    assert event.correlation_id is None
    assert event.causation_id is None


def test_domain_events_are_value_equal_when_payload_is_equal() -> None:
    occurred_at = datetime(2026, 8, 29, 12, 0, tzinfo=UTC)

    first = ParticipationRegistered(
        event_id="EVT-001",
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        participation_type=ParticipationType.CONTRIBUTION,
        occurred_at=occurred_at,
        aggregate_version=ParticipationVersion(1),
        actor_id="ACTOR-001",
    )

    second = ParticipationRegistered(
        event_id="EVT-001",
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        participation_type=ParticipationType.CONTRIBUTION,
        occurred_at=occurred_at,
        aggregate_version=ParticipationVersion(1),
        actor_id="ACTOR-001",
    )

    assert first == second