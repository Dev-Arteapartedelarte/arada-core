from dataclasses import dataclass
from datetime import datetime

from arada_core.proposal.domain.value_objects.organization_id import OrganizationId
from arada_core.proposal.domain.value_objects.proposal_id import ProposalId
from arada_core.proposal.domain.value_objects.proposal_version import ProposalVersion


@dataclass(frozen=True, slots=True)
class ProposalSubmitted:
    """
    Domain Event emitido cuando una Proposal es presentada válidamente.

    ProposalSubmitted representa el hecho consumado producido por la
    transición:

        Draft
          |
          | SubmitProposal
          v
        Submitted

    Conforme al modelo normativo de Proposal:

    - describe un hecho ocurrido dentro del Bounded Context Proposal;
    - es producido únicamente como consecuencia de comportamiento válido
      del Aggregate Proposal;
    - no constituye un Command;
    - no ejecuta la transición por sí mismo;
    - no modifica ProposalStatus;
    - no ejecuta persistencia;
    - no coordina autorización;
    - no publica directamente hacia sistemas externos;
    - no constituye un Integration Event;
    - no constituye una notificación NGSI-LD.

    La transformación posterior de este hecho en
    ProposalSubmittedForIntegration pertenece a la coordinación exterior al
    dominio y debe ocurrir respetando el límite transaccional y las reglas
    post-Commit definidas por AURA Core.
    """

    proposal_id: ProposalId
    organization_id: OrganizationId
    occurred_at: datetime
    version: ProposalVersion