from dataclasses import dataclass
from datetime import datetime

from arada_core.proposal.domain.value_objects.organization_id import OrganizationId
from arada_core.proposal.domain.value_objects.proposal_id import ProposalId
from arada_core.proposal.domain.value_objects.proposal_name import ProposalName
from arada_core.proposal.domain.value_objects.proposal_type import ProposalType
from arada_core.proposal.domain.value_objects.proposal_version import ProposalVersion


@dataclass(frozen=True, slots=True)
class ProposalCreated:
    """
    Domain Event emitido cuando una Proposal es creada válidamente.

    ProposalCreated representa el hecho consumado producido por la transición:

        Nonexistent
            |
            | CreateProposal
            v
        Draft

    Conforme al modelo normativo de Proposal:

    - describe un hecho ocurrido dentro del Bounded Context Proposal;
    - es producido por el Aggregate Proposal;
    - no constituye un Command;
    - no modifica el Aggregate;
    - no ejecuta persistencia;
    - no publica directamente información hacia sistemas externos;
    - no constituye un Integration Event;
    - no constituye una entidad NGSI-LD;
    - conserva únicamente información necesaria para representar el hecho
      ocurrido.

    La publicación efectiva y cualquier transformación posterior hacia un
    Integration Event pertenecen a capas externas al dominio.
    """

    proposal_id: ProposalId
    organization_id: OrganizationId
    proposal_name: ProposalName
    proposal_type: ProposalType
    occurred_at: datetime
    version: ProposalVersion