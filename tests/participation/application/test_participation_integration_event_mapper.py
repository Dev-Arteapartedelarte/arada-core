from datetime import UTC, datetime

import pytest

from arada_core.participation.application.integration_events.participation_activated_integration_event import (
    ParticipationActivatedIntegrationEvent,
)
from arada_core.participation.application.integration_events.participation_registered_integration_event import (
    ParticipationRegisteredIntegrationEvent,
)
from arada_core.participation.application.mappers.participation_integration_event_mapper import (
    ParticipationIntegrationEventMapper,
)
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


def test_mapper_maps_participation_registered_to_integration_event() -> None:
    occurred_at = datetime(2026, 8, 29, 12, 0, tzinfo=UTC)

    domain_event = ParticipationRegistered(
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

    mapper = ParticipationIntegrationEventMapper()

    integration_event = mapper.map(domain_event)

    assert isinstance(
        integration_event,
        ParticipationRegisteredIntegrationEvent,
    )
    assert integration_event.event_id == "EVT-001"
    assert (
        integration_event.event_type
        == "ParticipationRegisteredIntegrationEvent"
    )
    assert integration_event.event_version == 1
    assert integration_event.aggregate_id == ParticipationId("PAR-001")
    assert integration_event.aggregate_type == "Participation"
    assert integration_event.aggregate_version == ParticipationVersion(1)
    assert integration_event.occurred_at == occurred_at
    assert integration_event.correlation_id == "CORR-001"
    assert integration_event.causation_id == "CMD-001"
    assert integration_event.organization_id == OrganizationId("ORG-001")
    assert integration_event.participation_type is ParticipationType.ATTENDANCE


def test_mapper_maps_participation_activated_to_integration_event() -> None:
    occurred_at = datetime(2026, 8, 29, 12, 30, tzinfo=UTC)

    domain_event = ParticipationActivated(
        event_id="EVT-002",
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        started_at=occurred_at,
        occurred_at=occurred_at,
        aggregate_version=ParticipationVersion(2),
        actor_id="ACTOR-002",
        correlation_id="CORR-001",
        causation_id="CMD-002",
    )

    mapper = ParticipationIntegrationEventMapper()

    integration_event = mapper.map(domain_event)

    assert isinstance(
        integration_event,
        ParticipationActivatedIntegrationEvent,
    )
    assert integration_event.event_id == "EVT-002"
    assert (
        integration_event.event_type
        == "ParticipationActivatedIntegrationEvent"
    )
    assert integration_event.event_version == 1
    assert integration_event.aggregate_id == ParticipationId("PAR-001")
    assert integration_event.aggregate_type == "Participation"
    assert integration_event.aggregate_version == ParticipationVersion(2)
    assert integration_event.occurred_at == occurred_at
    assert integration_event.correlation_id == "CORR-001"
    assert integration_event.causation_id == "CMD-002"
    assert integration_event.organization_id == OrganizationId("ORG-001")


def test_mapper_preserves_optional_trace_metadata() -> None:
    domain_event = ParticipationRegistered(
        event_id="EVT-001",
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        participation_type=ParticipationType.CONSULTATION,
        occurred_at=datetime(2026, 8, 29, 12, 0, tzinfo=UTC),
        aggregate_version=ParticipationVersion(1),
        actor_id="ACTOR-001",
        correlation_id=None,
        causation_id=None,
    )

    mapper = ParticipationIntegrationEventMapper()

    integration_event = mapper.map(domain_event)

    assert isinstance(
        integration_event,
        ParticipationRegisteredIntegrationEvent,
    )
    assert integration_event.correlation_id is None
    assert integration_event.causation_id is None


def test_mapper_keeps_event_version_independent_from_aggregate_version() -> None:
    domain_event = ParticipationActivated(
        event_id="EVT-007",
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        started_at=datetime(2026, 8, 29, 13, 0, tzinfo=UTC),
        occurred_at=datetime(2026, 8, 29, 13, 0, tzinfo=UTC),
        aggregate_version=ParticipationVersion(7),
        actor_id="ACTOR-001",
    )

    mapper = ParticipationIntegrationEventMapper()

    integration_event = mapper.map(domain_event)

    assert isinstance(
        integration_event,
        ParticipationActivatedIntegrationEvent,
    )
    assert integration_event.event_version == 1
    assert integration_event.aggregate_version == ParticipationVersion(7)


def test_mapper_preserves_domain_event_id() -> None:
    domain_event = ParticipationRegistered(
        event_id="DOMAIN-EVENT-123",
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        participation_type=ParticipationType.CONTRIBUTION,
        occurred_at=datetime(2026, 8, 29, 12, 0, tzinfo=UTC),
        aggregate_version=ParticipationVersion(1),
        actor_id="ACTOR-001",
    )

    mapper = ParticipationIntegrationEventMapper()

    integration_event = mapper.map(domain_event)

    assert isinstance(
        integration_event,
        ParticipationRegisteredIntegrationEvent,
    )
    assert integration_event.event_id == domain_event.event_id


def test_mapper_preserves_occurred_at() -> None:
    occurred_at = datetime(2026, 8, 29, 12, 0, tzinfo=UTC)

    domain_event = ParticipationRegistered(
        event_id="EVT-001",
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        participation_type=ParticipationType.DELIBERATION,
        occurred_at=occurred_at,
        aggregate_version=ParticipationVersion(1),
        actor_id="ACTOR-001",
    )

    mapper = ParticipationIntegrationEventMapper()

    integration_event = mapper.map(domain_event)

    assert isinstance(
        integration_event,
        ParticipationRegisteredIntegrationEvent,
    )
    assert integration_event.occurred_at is domain_event.occurred_at


def test_mapper_does_not_introduce_published_at() -> None:
    domain_event = ParticipationRegistered(
        event_id="EVT-001",
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        participation_type=ParticipationType.ASSEMBLY_PARTICIPATION,
        occurred_at=datetime(2026, 8, 29, 12, 0, tzinfo=UTC),
        aggregate_version=ParticipationVersion(1),
        actor_id="ACTOR-001",
    )

    mapper = ParticipationIntegrationEventMapper()

    integration_event = mapper.map(domain_event)

    assert not hasattr(integration_event, "published_at")


def test_mapper_rejects_unsupported_domain_event() -> None:
    mapper = ParticipationIntegrationEventMapper()

    with pytest.raises(
        TypeError,
        match=(
            "Unsupported Participation domain event for integration mapping: "
            "object."
        ),
    ):
        mapper.map(object())