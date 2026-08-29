from datetime import UTC, datetime

import pytest

from arada_core.participation.domain.aggregates.participation import Participation
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
from arada_core.participation.domain.value_objects.participation_status import (
    ParticipationStatus,
)
from arada_core.participation.domain.value_objects.participation_type import (
    ParticipationType,
)
from arada_core.participation.domain.value_objects.participation_version import (
    ParticipationVersion,
)


def _registered_participation() -> Participation:
    participation = Participation.register(
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        participation_type=ParticipationType.ATTENDANCE,
        created_at=datetime(2026, 8, 29, 12, 0, tzinfo=UTC),
        event_id="EVT-001",
        actor_id="ACTOR-001",
        correlation_id="CORR-001",
        causation_id="CMD-001",
    )
    participation.pull_domain_events()
    return participation


def test_register_creates_participation_in_registered_status() -> None:
    created_at = datetime(2026, 8, 29, 12, 0, tzinfo=UTC)

    participation = Participation.register(
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        participation_type=ParticipationType.ATTENDANCE,
        created_at=created_at,
        event_id="EVT-001",
        actor_id="ACTOR-001",
    )

    assert participation.participation_id == ParticipationId("PAR-001")
    assert participation.organization_id == OrganizationId("ORG-001")
    assert participation.participation_type is ParticipationType.ATTENDANCE
    assert participation.status is ParticipationStatus.REGISTERED
    assert participation.version == ParticipationVersion(1)
    assert participation.created_at == created_at
    assert participation.started_at is None


def test_register_records_participation_registered() -> None:
    created_at = datetime(2026, 8, 29, 12, 0, tzinfo=UTC)

    participation = Participation.register(
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        participation_type=ParticipationType.INTERVENTION,
        created_at=created_at,
        event_id="EVT-001",
        actor_id="ACTOR-001",
        correlation_id="CORR-001",
        causation_id="CMD-001",
    )

    events = participation.pull_domain_events()

    assert len(events) == 1
    assert isinstance(events[0], ParticipationRegistered)

    event = events[0]
    assert event.event_id == "EVT-001"
    assert event.participation_id == ParticipationId("PAR-001")
    assert event.organization_id == OrganizationId("ORG-001")
    assert event.participation_type is ParticipationType.INTERVENTION
    assert event.occurred_at == created_at
    assert event.aggregate_version == ParticipationVersion(1)
    assert event.actor_id == "ACTOR-001"
    assert event.correlation_id == "CORR-001"
    assert event.causation_id == "CMD-001"


def test_pull_domain_events_clears_recorded_events() -> None:
    participation = Participation.register(
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        participation_type=ParticipationType.ATTENDANCE,
        created_at=datetime(2026, 8, 29, 12, 0, tzinfo=UTC),
        event_id="EVT-001",
        actor_id="ACTOR-001",
    )

    first_pull = participation.pull_domain_events()
    second_pull = participation.pull_domain_events()

    assert len(first_pull) == 1
    assert second_pull == ()


@pytest.mark.parametrize(
    ("field_name", "event_id", "actor_id", "correlation_id", "causation_id"),
    [
        ("event_id", "", "ACTOR-001", None, None),
        ("event_id", "   ", "ACTOR-001", None, None),
        ("actor_id", "EVT-001", "", None, None),
        ("actor_id", "EVT-001", "   ", None, None),
        ("correlation_id", "EVT-001", "ACTOR-001", "", None),
        ("correlation_id", "EVT-001", "ACTOR-001", "   ", None),
        ("causation_id", "EVT-001", "ACTOR-001", None, ""),
        ("causation_id", "EVT-001", "ACTOR-001", None, "   "),
    ],
)
def test_register_rejects_invalid_event_metadata(
    field_name: str,
    event_id: str,
    actor_id: str,
    correlation_id: str | None,
    causation_id: str | None,
) -> None:
    with pytest.raises(
        ValueError,
        match=rf"{field_name} must not be empty",
    ):
        Participation.register(
            participation_id=ParticipationId("PAR-001"),
            organization_id=OrganizationId("ORG-001"),
            participation_type=ParticipationType.ATTENDANCE,
            created_at=datetime(2026, 8, 29, 12, 0, tzinfo=UTC),
            event_id=event_id,
            actor_id=actor_id,
            correlation_id=correlation_id,
            causation_id=causation_id,
        )


def test_activate_transitions_registered_to_active() -> None:
    participation = _registered_participation()
    started_at = datetime(2026, 8, 29, 12, 30, tzinfo=UTC)

    participation.activate(
        started_at=started_at,
        event_id="EVT-002",
        actor_id="ACTOR-002",
    )

    assert participation.status is ParticipationStatus.ACTIVE
    assert participation.started_at == started_at
    assert participation.version == ParticipationVersion(2)


def test_activate_preserves_created_at() -> None:
    participation = _registered_participation()
    original_created_at = participation.created_at

    participation.activate(
        started_at=datetime(2026, 8, 29, 12, 30, tzinfo=UTC),
        event_id="EVT-002",
        actor_id="ACTOR-002",
    )

    assert participation.created_at == original_created_at


def test_activate_records_participation_activated() -> None:
    participation = _registered_participation()
    started_at = datetime(2026, 8, 29, 12, 30, tzinfo=UTC)

    participation.activate(
        started_at=started_at,
        event_id="EVT-002",
        actor_id="ACTOR-002",
        correlation_id="CORR-001",
        causation_id="CMD-002",
    )

    events = participation.pull_domain_events()

    assert len(events) == 1
    assert isinstance(events[0], ParticipationActivated)

    event = events[0]
    assert event.event_id == "EVT-002"
    assert event.participation_id == ParticipationId("PAR-001")
    assert event.organization_id == OrganizationId("ORG-001")
    assert event.started_at == started_at
    assert event.occurred_at == started_at
    assert event.aggregate_version == ParticipationVersion(2)
    assert event.actor_id == "ACTOR-002"
    assert event.correlation_id == "CORR-001"
    assert event.causation_id == "CMD-002"


def test_activate_increments_version_exactly_once() -> None:
    participation = _registered_participation()

    assert participation.version == ParticipationVersion(1)

    participation.activate(
        started_at=datetime(2026, 8, 29, 12, 30, tzinfo=UTC),
        event_id="EVT-002",
        actor_id="ACTOR-002",
    )

    assert participation.version == ParticipationVersion(2)


def test_activate_rejects_started_at_before_created_at() -> None:
    participation = _registered_participation()

    original_status = participation.status
    original_version = participation.version
    original_started_at = participation.started_at

    with pytest.raises(
        ValueError,
        match="Participation started_at must not be earlier than created_at.",
    ):
        participation.activate(
            started_at=datetime(2026, 8, 29, 11, 59, tzinfo=UTC),
            event_id="EVT-002",
            actor_id="ACTOR-002",
        )

    assert participation.status is original_status
    assert participation.version == original_version
    assert participation.started_at is original_started_at
    assert participation.pull_domain_events() == ()


def test_activate_rejects_second_activation() -> None:
    participation = _registered_participation()

    participation.activate(
        started_at=datetime(2026, 8, 29, 12, 30, tzinfo=UTC),
        event_id="EVT-002",
        actor_id="ACTOR-002",
    )
    participation.pull_domain_events()

    original_version = participation.version
    original_started_at = participation.started_at

    with pytest.raises(
        ValueError,
        match="Participation can only be activated from Registered status.",
    ):
        participation.activate(
            started_at=datetime(2026, 8, 29, 13, 0, tzinfo=UTC),
            event_id="EVT-003",
            actor_id="ACTOR-003",
        )

    assert participation.status is ParticipationStatus.ACTIVE
    assert participation.version == original_version
    assert participation.started_at == original_started_at
    assert participation.pull_domain_events() == ()


@pytest.mark.parametrize(
    ("field_name", "event_id", "actor_id", "correlation_id", "causation_id"),
    [
        ("event_id", "", "ACTOR-002", None, None),
        ("event_id", "   ", "ACTOR-002", None, None),
        ("actor_id", "EVT-002", "", None, None),
        ("actor_id", "EVT-002", "   ", None, None),
        ("correlation_id", "EVT-002", "ACTOR-002", "", None),
        ("correlation_id", "EVT-002", "ACTOR-002", "   ", None),
        ("causation_id", "EVT-002", "ACTOR-002", None, ""),
        ("causation_id", "EVT-002", "ACTOR-002", None, "   "),
    ],
)
def test_activate_rejects_invalid_event_metadata_without_mutation(
    field_name: str,
    event_id: str,
    actor_id: str,
    correlation_id: str | None,
    causation_id: str | None,
) -> None:
    participation = _registered_participation()

    original_status = participation.status
    original_version = participation.version
    original_started_at = participation.started_at

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must not be empty",
    ):
        participation.activate(
            started_at=datetime(2026, 8, 29, 12, 30, tzinfo=UTC),
            event_id=event_id,
            actor_id=actor_id,
            correlation_id=correlation_id,
            causation_id=causation_id,
        )

    assert participation.status is original_status
    assert participation.version == original_version
    assert participation.started_at is original_started_at
    assert participation.pull_domain_events() == ()