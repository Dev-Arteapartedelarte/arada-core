from arada_core.participation.application.commands.activate_participation import (
    ActivateParticipation,
)
from arada_core.participation.application.commands.register_participation import (
    RegisterParticipation,
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


def test_register_participation_command_exposes_required_data() -> None:
    command = RegisterParticipation(
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        participation_type=ParticipationType.ATTENDANCE,
    )

    assert command.participation_id == ParticipationId("PAR-001")
    assert command.organization_id == OrganizationId("ORG-001")
    assert command.participation_type is ParticipationType.ATTENDANCE


def test_register_participation_commands_are_value_equal() -> None:
    first = RegisterParticipation(
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        participation_type=ParticipationType.CONTRIBUTION,
    )

    second = RegisterParticipation(
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        participation_type=ParticipationType.CONTRIBUTION,
    )

    assert first == second


def test_activate_participation_command_exposes_required_data() -> None:
    command = ActivateParticipation(
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        expected_version=ParticipationVersion(1),
    )

    assert command.participation_id == ParticipationId("PAR-001")
    assert command.organization_id == OrganizationId("ORG-001")
    assert command.expected_version == ParticipationVersion(1)


def test_activate_participation_commands_are_value_equal() -> None:
    first = ActivateParticipation(
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        expected_version=ParticipationVersion(1),
    )

    second = ActivateParticipation(
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        expected_version=ParticipationVersion(1),
    )

    assert first == second


def test_register_and_activate_commands_represent_different_intentions() -> None:
    register_command = RegisterParticipation(
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        participation_type=ParticipationType.ATTENDANCE,
    )

    activate_command = ActivateParticipation(
        participation_id=ParticipationId("PAR-001"),
        organization_id=OrganizationId("ORG-001"),
        expected_version=ParticipationVersion(1),
    )

    assert type(register_command) is RegisterParticipation
    assert type(activate_command) is ActivateParticipation
    assert type(register_command) is not type(activate_command)