import pytest

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


def test_participation_id_accepts_non_empty_value() -> None:
    participation_id = ParticipationId("PAR-001")

    assert participation_id.value == "PAR-001"
    assert str(participation_id) == "PAR-001"


def test_participation_id_strips_surrounding_whitespace() -> None:
    participation_id = ParticipationId("  PAR-001  ")

    assert participation_id.value == "PAR-001"


@pytest.mark.parametrize(
    "value",
    [
        "",
        " ",
        "\t",
        "\n",
    ],
)
def test_participation_id_rejects_empty_value(value: str) -> None:
    with pytest.raises(
        ValueError,
        match="ParticipationId must not be empty.",
    ):
        ParticipationId(value)


def test_organization_id_accepts_non_empty_value() -> None:
    organization_id = OrganizationId("ORG-001")

    assert organization_id.value == "ORG-001"
    assert str(organization_id) == "ORG-001"


def test_organization_id_strips_surrounding_whitespace() -> None:
    organization_id = OrganizationId("  ORG-001  ")

    assert organization_id.value == "ORG-001"


@pytest.mark.parametrize(
    "value",
    [
        "",
        " ",
        "\t",
        "\n",
    ],
)
def test_organization_id_rejects_empty_value(value: str) -> None:
    with pytest.raises(
        ValueError,
        match="OrganizationId must not be empty.",
    ):
        OrganizationId(value)


def test_participation_status_exposes_canonical_values() -> None:
    assert ParticipationStatus.REGISTERED.value == "Registered"
    assert ParticipationStatus.ACTIVE.value == "Active"
    assert ParticipationStatus.COMPLETED.value == "Completed"
    assert ParticipationStatus.WITHDRAWN.value == "Withdrawn"
    assert ParticipationStatus.INVALIDATED.value == "Invalidated"
    assert ParticipationStatus.ARCHIVED.value == "Archived"


def test_participation_type_exposes_canonical_values() -> None:
    assert ParticipationType.ATTENDANCE.value == "Attendance"
    assert ParticipationType.INTERVENTION.value == "Intervention"
    assert ParticipationType.DELIBERATION.value == "Deliberation"
    assert ParticipationType.CONTRIBUTION.value == "Contribution"
    assert ParticipationType.CONSULTATION.value == "Consultation"
    assert (
        ParticipationType.PROPOSAL_PARTICIPATION.value
        == "ProposalParticipation"
    )
    assert (
        ParticipationType.ASSEMBLY_PARTICIPATION.value
        == "AssemblyParticipation"
    )
    assert (
        ParticipationType.TERRITORIAL_PARTICIPATION.value
        == "TerritorialParticipation"
    )


def test_participation_version_accepts_initial_version() -> None:
    version = ParticipationVersion(1)

    assert version.value == 1
    assert int(version) == 1


def test_participation_version_initial_returns_version_one() -> None:
    version = ParticipationVersion.initial()

    assert version == ParticipationVersion(1)


def test_participation_version_next_increments_once() -> None:
    version = ParticipationVersion(7)

    next_version = version.next()

    assert next_version == ParticipationVersion(8)
    assert version == ParticipationVersion(7)


@pytest.mark.parametrize(
    "value",
    [
        0,
        -1,
        -10,
    ],
)
def test_participation_version_rejects_values_lower_than_one(
    value: int,
) -> None:
    with pytest.raises(
        ValueError,
        match="ParticipationVersion must be greater than or equal to 1.",
    ):
        ParticipationVersion(value)