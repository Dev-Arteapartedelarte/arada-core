from dataclasses import dataclass
from datetime import datetime

from arada_core.proposal.domain.value_objects.assembly_id import AssemblyId
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


@dataclass(frozen=True, slots=True)
class ProposalResult:
    """
    Resultado de Application para operaciones sobre Proposal.

    ProposalResult representa el estado observable mínimo que Application
    puede devolver después de ejecutar satisfactoriamente un caso de uso sin
    exponer directamente el Aggregate Root.

    Conforme a las reglas de Application Services de AURA Core:

    - pertenece a Application;
    - no representa el Aggregate Proposal;
    - no contiene comportamiento de dominio;
    - no modifica ProposalStatus;
    - no modifica ProposalVersion;
    - no ejecuta persistencia;
    - no publica Domain Events;
    - no sustituye un Read Model especializado;
    - no depende de Infrastructure;
    - no contiene detalles HTTP ni de transporte.

    VS-001 puede utilizar este resultado tanto después de CreateProposal como
    después de SubmitProposal.

    Los campos opcionales conservan únicamente referencias contextuales que
    existen en la Proposal correspondiente.
    """

    proposal_id: ProposalId
    organization_id: OrganizationId
    proposer_reference: ProposerReference
    proposal_name: ProposalName
    proposal_type: ProposalType
    proposal_status: ProposalStatus
    version: ProposalVersion
    territory_id: TerritoryId | None = None
    assembly_id: AssemblyId | None = None
    submitted_at: datetime | None = None