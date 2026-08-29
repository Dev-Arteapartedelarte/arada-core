from datetime import UTC, datetime

from arada_core.participation.application.dto.participation_result import (
    ParticipationResult,
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


def test_participation_result_exposes_confirmed_application_state() -> None:
    created_at = datetime(2026, 8, 29, 12, 0, tzinfo=UTC)
    started_at = datetime(2026, 8, 29, 12, 30, tzinfo=UTC)

    result = ParticipationResult(
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        participation_type=ParticipationType.ATTENDANCE,
        status=ParticipationStatus.ACTIVE,
        version=ParticipationVersion(2),
        created_at=created_at,
        started_at=started_at,
    )

    assert result.participation_id == ParticipationId("PAR-001")
    assert result.organization_id == OrganizationId("ORG-001")
    assert result.participation_type is ParticipationType.ATTENDANCE
    assert result.status is ParticipationStatus.ACTIVE
    assert result.version == ParticipationVersion(2)
    assert result.created_at == created_at
    assert result.started_at == started_at


def test_participation_result_supports_registered_state_without_started_at() -> None:
    created_at = datetime(2026, 8, 29, 12, 0, tzinfo=UTC)

    result = ParticipationResult(
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        participation_type=ParticipationType.INTERVENTION,
        status=ParticipationStatus.REGISTERED,
        version=ParticipationVersion(1),
        created_at=created_at,
        started_at=None,
    )

    assert result.status is ParticipationStatus.REGISTERED
    assert result.version == ParticipationVersion(1)
    assert result.started_at is None


def test_participation_results_are_value_equal_when_payload_is_equal() -> None:
    created_at = datetime(2026, 8, 29, 12, 0, tzinfo=UTC)

    first = ParticipationResult(
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        participation_type=ParticipationType.CONTRIBUTION,
        status=ParticipationStatus.REGISTERED,
        version=ParticipationVersion(1),
        created_at=created_at,
        started_at=None,
    )

    second = ParticipationResult(
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        participation_type=ParticipationType.CONTRIBUTION,
        status=ParticipationStatus.REGISTERED,
        version=ParticipationVersion(1),
        created_at=created_at,
        started_at=None,
    )

    assert first == second