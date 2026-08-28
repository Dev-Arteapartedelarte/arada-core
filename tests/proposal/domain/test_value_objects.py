from datetime import UTC, datetime

import pytest

from arada_core.proposal.domain.value_objects.assembly_id import AssemblyId
from arada_core.proposal.domain.value_objects.citizen_id import CitizenId
from arada_core.proposal.domain.value_objects.membership_id import MembershipId
from arada_core.proposal.domain.value_objects.organization_id import OrganizationId
from arada_core.proposal.domain.value_objects.proposal_content import ProposalContent
from arada_core.proposal.domain.value_objects.proposal_description import (
    ProposalDescription,
)
from arada_core.proposal.domain.value_objects.proposal_id import ProposalId
from arada_core.proposal.domain.value_objects.proposal_name import ProposalName
from arada_core.proposal.domain.value_objects.proposal_purpose import ProposalPurpose
from arada_core.proposal.domain.value_objects.proposal_status import ProposalStatus
from arada_core.proposal.domain.value_objects.proposal_version import ProposalVersion
from arada_core.proposal.domain.value_objects.proposer_reference import (
    ProposerReference,
)
from arada_core.proposal.domain.value_objects.submitted_at import SubmittedAt
from arada_core.proposal.domain.value_objects.territory_id import TerritoryId


@pytest.mark.parametrize(
    ("value_object_type", "raw_value", "expected_value"),
    [
        (ProposalId, " proposal-001 ", "proposal-001"),
        (ProposalName, " Iniciativa comunitaria ", "Iniciativa comunitaria"),
        (ProposalPurpose, " Mejorar el entorno ", "Mejorar el entorno"),
        (
            ProposalDescription,
            " Descripción de la iniciativa ",
            "Descripción de la iniciativa",
        ),
        (
            ProposalContent,
            " Contenido de la iniciativa ",
            "Contenido de la iniciativa",
        ),
        (OrganizationId, " organization-001 ", "organization-001"),
        (CitizenId, " citizen-001 ", "citizen-001"),
        (MembershipId, " membership-001 ", "membership-001"),
        (TerritoryId, " territory-001 ", "territory-001"),
        (AssemblyId, " assembly-001 ", "assembly-001"),
    ],
)
def test_string_value_objects_normalize_surrounding_whitespace(
    value_object_type: type,
    raw_value: str,
    expected_value: str,
) -> None:
    """
    Los Value Objects textuales deben normalizar exclusivamente espacios
    exteriores y conservar el valor semántico resultante.
    """
    value_object = value_object_type(raw_value)

    assert value_object.value == expected_value
    assert str(value_object) == expected_value


@pytest.mark.parametrize(
    "value_object_type",
    [
        ProposalId,
        ProposalName,
        ProposalPurpose,
        ProposalDescription,
        ProposalContent,
        OrganizationId,
        CitizenId,
        MembershipId,
        TerritoryId,
        AssemblyId,
    ],
)
@pytest.mark.parametrize(
    "invalid_value",
    [
        "",
        " ",
        "   ",
        "\t",
        "\n",
    ],
)
def test_string_value_objects_reject_empty_normalized_values(
    value_object_type: type,
    invalid_value: str,
) -> None:
    """
    Los Value Objects textuales existentes en VS-001 no deben aceptar un valor
    que resulte vacío después de la normalización definida por su contrato.
    """
    with pytest.raises(ValueError):
        value_object_type(invalid_value)


def test_proposer_reference_accepts_citizen_id() -> None:
    """
    ProposerReference puede conservar una referencia CitizenId.
    """
    citizen_id = CitizenId("citizen-001")

    reference = ProposerReference(citizen_id)

    assert reference.value == citizen_id
    assert reference.is_citizen is True
    assert reference.is_membership is False
    assert str(reference) == "citizen-001"


def test_proposer_reference_accepts_membership_id() -> None:
    """
    ProposerReference puede conservar una referencia MembershipId.
    """
    membership_id = MembershipId("membership-001")

    reference = ProposerReference(membership_id)

    assert reference.value == membership_id
    assert reference.is_citizen is False
    assert reference.is_membership is True
    assert str(reference) == "membership-001"


def test_proposer_reference_rejects_unsupported_reference_type() -> None:
    """
    ProposerReference no debe aceptar referencias externas diferentes de las
    representadas explícitamente por su contrato actual.
    """
    with pytest.raises(
        TypeError,
        match="ProposerReference must contain a CitizenId or MembershipId.",
    ):
        ProposerReference(OrganizationId("organization-001"))  # type: ignore[arg-type]


def test_proposal_version_accepts_positive_integer() -> None:
    """
    ProposalVersion debe representar una versión lógica positiva.
    """
    version = ProposalVersion(1)

    assert version.value == 1
    assert int(version) == 1
    assert str(version) == "1"


@pytest.mark.parametrize(
    "invalid_version",
    [
        0,
        -1,
        -100,
    ],
)
def test_proposal_version_rejects_non_positive_integer(
    invalid_version: int,
) -> None:
    """
    La versión lógica de una Proposal persistida no puede ser menor que 1.
    """
    with pytest.raises(
        ValueError,
        match="ProposalVersion must be greater than or equal to 1.",
    ):
        ProposalVersion(invalid_version)


@pytest.mark.parametrize(
    "invalid_version",
    [
        True,
        False,
        1.0,
        "1",
    ],
)
def test_proposal_version_rejects_non_integer_values(
    invalid_version: object,
) -> None:
    """
    ProposalVersion debe impedir que bool u otros tipos sean tratados como
    versiones enteras válidas.
    """
    with pytest.raises(
        TypeError,
        match="ProposalVersion must be an integer.",
    ):
        ProposalVersion(invalid_version)  # type: ignore[arg-type]


def test_proposal_version_next_returns_new_value_object() -> None:
    """
    next() debe producir la versión inmediatamente posterior sin mutar el
    Value Object original.
    """
    version = ProposalVersion(1)

    next_version = version.next()

    assert version == ProposalVersion(1)
    assert next_version == ProposalVersion(2)
    assert next_version is not version


def test_submitted_at_preserves_datetime_value() -> None:
    """
    SubmittedAt debe conservar el instante recibido sin introducir una
    transformación temporal adicional.
    """
    instant = datetime(2026, 8, 26, 6, 30, tzinfo=UTC)

    submitted_at = SubmittedAt(instant)

    assert submitted_at.value == instant
    assert str(submitted_at) == instant.isoformat()


def test_submitted_at_rejects_non_datetime_value() -> None:
    """
    SubmittedAt no debe aceptar valores que no sean datetime.
    """
    with pytest.raises(
        TypeError,
        match="SubmittedAt must contain a datetime.",
    ):
        SubmittedAt("2026-08-26T06:30:00+00:00")  # type: ignore[arg-type]


def test_proposal_status_exposes_vs001_states() -> None:
    """
    ProposalStatus debe conservar los estados utilizados por VS-001 con sus
    valores canónicos.
    """
    assert ProposalStatus.DRAFT.value == "Draft"
    assert ProposalStatus.SUBMITTED.value == "Submitted"