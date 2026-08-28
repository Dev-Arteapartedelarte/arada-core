from dataclasses import FrozenInstanceError

import pytest

from arada_core.proposal.application.commands.create_proposal import CreateProposal
from arada_core.proposal.application.commands.submit_proposal import SubmitProposal
from arada_core.proposal.domain.value_objects.assembly_id import AssemblyId
from arada_core.proposal.domain.value_objects.citizen_id import CitizenId
from arada_core.proposal.domain.value_objects.organization_id import OrganizationId
from arada_core.proposal.domain.value_objects.proposal_content import ProposalContent
from arada_core.proposal.domain.value_objects.proposal_description import (
    ProposalDescription,
)
from arada_core.proposal.domain.value_objects.proposal_id import ProposalId
from arada_core.proposal.domain.value_objects.proposal_name import ProposalName
from arada_core.proposal.domain.value_objects.proposal_purpose import ProposalPurpose
from arada_core.proposal.domain.value_objects.proposal_type import ProposalType
from arada_core.proposal.domain.value_objects.proposal_version import ProposalVersion
from arada_core.proposal.domain.value_objects.proposer_reference import (
    ProposerReference,
)
from arada_core.proposal.domain.value_objects.territory_id import TerritoryId


def test_create_proposal_preserves_intent_data() -> None:
    """
    CreateProposal debe transportar íntegramente la intención necesaria para
    coordinar la creación sin ejecutar comportamiento por sí mismo.
    """
    proposal_id = ProposalId("proposal-001")
    organization_id = OrganizationId("organization-001")
    proposer_reference = ProposerReference(CitizenId("citizen-001"))
    proposal_name = ProposalName("Mejoramiento del espacio comunitario")
    proposal_type = ProposalType.COMMUNITY
    proposal_purpose = ProposalPurpose("Recuperar un espacio comunitario")
    proposal_description = ProposalDescription(
        "Propuesta destinada al mejoramiento del espacio común."
    )
    proposal_content = ProposalContent(
        "Intervención comunitaria para recuperar y mejorar el espacio."
    )
    territory_id = TerritoryId("territory-001")
    assembly_id = AssemblyId("assembly-001")

    command = CreateProposal(
        proposal_id=proposal_id,
        organization_id=organization_id,
        proposer_reference=proposer_reference,
        proposal_name=proposal_name,
        proposal_type=proposal_type,
        proposal_purpose=proposal_purpose,
        proposal_description=proposal_description,
        proposal_content=proposal_content,
        territory_id=territory_id,
        assembly_id=assembly_id,
    )

    assert command.proposal_id == proposal_id
    assert command.organization_id == organization_id
    assert command.proposer_reference == proposer_reference
    assert command.proposal_name == proposal_name
    assert command.proposal_type == proposal_type
    assert command.proposal_purpose == proposal_purpose
    assert command.proposal_description == proposal_description
    assert command.proposal_content == proposal_content
    assert command.territory_id == territory_id
    assert command.assembly_id == assembly_id


def test_create_proposal_accepts_optional_context_as_absent() -> None:
    """
    Los elementos contextuales opcionales no deben ser inventados por el
    Command cuando el caso concreto no los contiene.
    """
    command = CreateProposal(
        proposal_id=ProposalId("proposal-001"),
        organization_id=OrganizationId("organization-001"),
        proposer_reference=ProposerReference(CitizenId("citizen-001")),
        proposal_name=ProposalName("Mejoramiento del espacio comunitario"),
        proposal_type=ProposalType.COMMUNITY,
    )

    assert command.proposal_purpose is None
    assert command.proposal_description is None
    assert command.proposal_content is None
    assert command.territory_id is None
    assert command.assembly_id is None


def test_create_proposal_is_immutable() -> None:
    """
    Un Command representa una intención ya construida y no debe modificarse
    durante su coordinación.
    """
    command = CreateProposal(
        proposal_id=ProposalId("proposal-001"),
        organization_id=OrganizationId("organization-001"),
        proposer_reference=ProposerReference(CitizenId("citizen-001")),
        proposal_name=ProposalName("Mejoramiento del espacio comunitario"),
        proposal_type=ProposalType.COMMUNITY,
    )

    with pytest.raises(FrozenInstanceError):
        command.proposal_name = ProposalName("Nombre modificado")  # type: ignore[misc]


def test_submit_proposal_preserves_identity_and_expected_version() -> None:
    """
    SubmitProposal debe transportar ProposalId y ExpectedVersion sin alterar
    ninguno de los dos valores.
    """
    proposal_id = ProposalId("proposal-001")
    expected_version = ProposalVersion(4)

    command = SubmitProposal(
        proposal_id=proposal_id,
        expected_version=expected_version,
    )

    assert command.proposal_id == proposal_id
    assert command.expected_version == expected_version


def test_submit_proposal_is_immutable() -> None:
    """
    ExpectedVersion pertenece a la intención original de escritura y no debe
    poder modificarse después de construir el Command.
    """
    command = SubmitProposal(
        proposal_id=ProposalId("proposal-001"),
        expected_version=ProposalVersion(1),
    )

    with pytest.raises(FrozenInstanceError):
        command.expected_version = ProposalVersion(2)  # type: ignore[misc]