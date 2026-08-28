from dataclasses import dataclass

from arada_core.proposal.domain.value_objects.assembly_id import AssemblyId
from arada_core.proposal.domain.value_objects.organization_id import OrganizationId
from arada_core.proposal.domain.value_objects.proposal_content import ProposalContent
from arada_core.proposal.domain.value_objects.proposal_description import (
    ProposalDescription,
)
from arada_core.proposal.domain.value_objects.proposal_id import ProposalId
from arada_core.proposal.domain.value_objects.proposal_name import ProposalName
from arada_core.proposal.domain.value_objects.proposal_purpose import ProposalPurpose
from arada_core.proposal.domain.value_objects.proposal_type import ProposalType
from arada_core.proposal.domain.value_objects.proposer_reference import (
    ProposerReference,
)
from arada_core.proposal.domain.value_objects.territory_id import TerritoryId


@dataclass(frozen=True, slots=True)
class CreateProposal:
    """
    Intención de crear una nueva Proposal.

    CreateProposal transporta exclusivamente los datos requeridos por el caso
    de uso de creación dentro de VS-001.

    El Command:

    - expresa intención y no un hecho consumado;
    - no decide si la creación está autorizada;
    - no verifica existencia de Aggregates externos;
    - no persiste información;
    - no establece ProposalStatus;
    - no establece ProposalVersion;
    - no produce ProposalCreated;
    - no contiene lógica de dominio;
    - no depende de Infrastructure.

    Application debe resolver previamente las capacidades externas necesarias
    y posteriormente delegar la creación válida al Aggregate Proposal.

    Los campos opcionales representan información contextual que puede formar
    parte de una Proposal cuando corresponda al caso concreto.
    """

    proposal_id: ProposalId
    organization_id: OrganizationId
    proposer_reference: ProposerReference
    proposal_name: ProposalName
    proposal_type: ProposalType
    proposal_purpose: ProposalPurpose | None = None
    proposal_description: ProposalDescription | None = None
    proposal_content: ProposalContent | None = None
    territory_id: TerritoryId | None = None
    assembly_id: AssemblyId | None = None