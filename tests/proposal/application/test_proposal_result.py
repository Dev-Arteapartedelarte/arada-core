from datetime import UTC, datetime

from arada_core.proposal.application.dto.proposal_result import ProposalResult
from arada_core.proposal.domain.value_objects.assembly_id import AssemblyId
from arada_core.proposal.domain.value_objects.citizen_id import CitizenId
from arada_core.proposal.domain.value_objects.organization_id import OrganizationId
from arada_core.proposal.domain.value_objects.proposal_id import ProposalId
from arada_core.proposal.domain.value_objects.proposal_name import ProposalName
from arada_core.proposal.domain.value_objects.proposal_status import ProposalStatus
from arada_core.proposal.domain.value_objects.proposal_type import ProposalType
from arada_core.proposal.domain.value_objects.proposal_version import ProposalVersion
from arada_core.proposal.domain.value_objects.proposer_reference import (
    ProposerReference,
)
from arada_core.proposal.domain.value_objects.territory_id import TerritoryId


def test_proposal_result_represents_created_proposal() -> None:
    """
    ProposalResult debe poder representar el resultado observable de una
    creación válida sin exponer directamente el Aggregate Proposal.
    """
    result = ProposalResult(
        proposal_id=ProposalId("proposal-001"),
        organization_id=OrganizationId("organization-001"),
        proposer_reference=ProposerReference(CitizenId("citizen-001")),
        proposal_name=ProposalName("Mejoramiento del espacio comunitario"),
        proposal_type=ProposalType.COMMUNITY,
        proposal_status=ProposalStatus.DRAFT,
        version=ProposalVersion(1),
    )

    assert result.proposal_id == ProposalId("proposal-001")
    assert result.organization_id == OrganizationId("organization-001")
    assert result.proposer_reference == ProposerReference(
        CitizenId("citizen-001")
    )
    assert result.proposal_name == ProposalName(
        "Mejoramiento del espacio comunitario"
    )
    assert result.proposal_type is ProposalType.COMMUNITY
    assert result.proposal_status is ProposalStatus.DRAFT
    assert result.version == ProposalVersion(1)
    assert result.territory_id is None
    assert result.assembly_id is None
    assert result.submitted_at is None


def test_proposal_result_represents_submitted_proposal() -> None:
    """
    ProposalResult debe representar el estado resultante de una presentación
    válida incluyendo SubmittedAt y la nueva Version.
    """
    submitted_at = datetime(
        2026,
        8,
        26,
        6,
        50,
        tzinfo=UTC,
    )

    result = ProposalResult(
        proposal_id=ProposalId("proposal-001"),
        organization_id=OrganizationId("organization-001"),
        proposer_reference=ProposerReference(CitizenId("citizen-001")),
        proposal_name=ProposalName("Mejoramiento del espacio comunitario"),
        proposal_type=ProposalType.COMMUNITY,
        proposal_status=ProposalStatus.SUBMITTED,
        version=ProposalVersion(2),
        territory_id=TerritoryId("territory-001"),
        assembly_id=AssemblyId("assembly-001"),
        submitted_at=submitted_at,
    )

    assert result.proposal_status is ProposalStatus.SUBMITTED
    assert result.version == ProposalVersion(2)
    assert result.territory_id == TerritoryId("territory-001")
    assert result.assembly_id == AssemblyId("assembly-001")
    assert result.submitted_at == submitted_at


def test_proposal_result_preserves_domain_value_objects() -> None:
    """
    El DTO de Application debe conservar los Value Objects entregados sin
    reinterpretar ni reconstruir reglas pertenecientes al dominio.
    """
    proposal_id = ProposalId("proposal-001")
    organization_id = OrganizationId("organization-001")
    proposer_reference = ProposerReference(CitizenId("citizen-001"))
    proposal_name = ProposalName("Mejoramiento del espacio comunitario")
    proposal_type = ProposalType.COMMUNITY
    proposal_status = ProposalStatus.DRAFT
    version = ProposalVersion(1)

    result = ProposalResult(
        proposal_id=proposal_id,
        organization_id=organization_id,
        proposer_reference=proposer_reference,
        proposal_name=proposal_name,
        proposal_type=proposal_type,
        proposal_status=proposal_status,
        version=version,
    )

    assert result.proposal_id is proposal_id
    assert result.organization_id is organization_id
    assert result.proposer_reference is proposer_reference
    assert result.proposal_name is proposal_name
    assert result.proposal_type is proposal_type
    assert result.proposal_status is proposal_status
    assert result.version is version